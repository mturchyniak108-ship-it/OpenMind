#ifndef _GNU_SOURCE
#define _GNU_SOURCE 1
#endif

#include "openmind/registry_endpoint.hpp"

#include "openmind/named_registry_broker.hpp"
#include "openmind/unix_fd_transport.hpp"

#include <atomic>
#include <cerrno>
#include <chrono>
#include <climits>
#include <cstddef>
#include <cstring>
#include <fcntl.h>
#include <new>
#include <poll.h>
#include <string>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <unistd.h>

namespace openmind::secure_memory {
namespace {

constexpr const char* kEndpointName = "registry.sock";
constexpr const char* kLockName = "registry.lock";
std::atomic<pid_t> g_local_lock_owner_pid{0};

struct UnixAddress {
    sockaddr_un address{};
    socklen_t length = 0;
};

struct ParentCapability {
    int fd = -1;
    std::string canonical_path;
    dev_t device = 0;
    ino_t inode = 0;
};

enum class WaitResult {
    ready,
    timed_out,
    failed,
};

enum class ProbeResult {
    live,
    refused,
    missing,
    timed_out,
    failed,
};

void close_ignored(int fd) noexcept {
    if (fd >= 0) {
        (void)::close(fd);
    }
}

EndpointError close_owned(int& fd) noexcept {
    if (fd < 0) {
        return EndpointError::ok;
    }
    const int owned = fd;
    fd = -1;
    return ::close(owned) == 0
        ? EndpointError::ok
        : EndpointError::cleanup_failed;
}

bool reserve_local_lock_owner(pid_t self) noexcept {
    pid_t expected = 0;
    if (g_local_lock_owner_pid.compare_exchange_strong(
            expected,
            self,
            std::memory_order_acq_rel,
            std::memory_order_acquire)) {
        return true;
    }
    if (expected == self) {
        return false;
    }
    return g_local_lock_owner_pid.compare_exchange_strong(
        expected,
        self,
        std::memory_order_acq_rel,
        std::memory_order_acquire);
}

void release_local_lock_owner(pid_t owner_pid) noexcept {
    pid_t expected = owner_pid;
    (void)g_local_lock_owner_pid.compare_exchange_strong(
        expected,
        0,
        std::memory_order_acq_rel,
        std::memory_order_acquire);
}

class LocalLockReservation final {
public:
    static std::pair<LocalLockReservation, bool> acquire() noexcept {
        const pid_t self = ::getpid();
        if (!reserve_local_lock_owner(self)) {
            return {LocalLockReservation{}, false};
        }
        return {LocalLockReservation(self), true};
    }

    LocalLockReservation() noexcept = default;
    ~LocalLockReservation() {
        if (active_) {
            release_local_lock_owner(owner_pid_);
        }
    }
    LocalLockReservation(const LocalLockReservation&) = delete;
    LocalLockReservation& operator=(const LocalLockReservation&) = delete;
    LocalLockReservation(LocalLockReservation&& other) noexcept
        : owner_pid_(other.owner_pid_),
          active_(other.active_) {
        other.owner_pid_ = -1;
        other.active_ = false;
    }
    LocalLockReservation& operator=(LocalLockReservation&&) = delete;

    void commit() noexcept {
        active_ = false;
    }

private:
    explicit LocalLockReservation(pid_t owner_pid) noexcept
        : owner_pid_(owner_pid),
          active_(true) {}

    pid_t owner_pid_ = -1;
    bool active_ = false;
};

bool valid_components(std::string_view path) noexcept {
    if (path.empty() || path.front() != '/') {
        return false;
    }
    std::size_t pos = 1U;
    while (pos < path.size()) {
        const std::size_t slash = path.find('/', pos);
        const std::size_t end =
            slash == std::string_view::npos ? path.size() : slash;
        if (end == pos) {
            return false;
        }
        const std::string_view component =
            path.substr(pos, end - pos);
        if (component == "." || component == "..") {
            return false;
        }
        if (slash == std::string_view::npos) {
            return true;
        }
        pos = slash + 1U;
    }
    return false;
}

EndpointError qualify_parent(
    std::string_view path,
    uid_t expected_uid,
    std::string& owned_path,
    ParentCapability& parent,
    UnixAddress& address) {
    if (path.find('\0') != std::string_view::npos ||
        !valid_components(path)) {
        return EndpointError::invalid_argument;
    }
    if (path.size() >= sizeof(address.address.sun_path)) {
        return EndpointError::path_too_long;
    }

    const std::size_t slash = path.rfind('/');
    if (slash == std::string_view::npos ||
        slash == 0U ||
        slash + 1U >= path.size()) {
        return EndpointError::invalid_argument;
    }
    if (path.substr(slash + 1U) != kEndpointName) {
        return EndpointError::invalid_argument;
    }

    std::string parent_input;
    try {
        owned_path.assign(path.data(), path.size());
        parent_input.assign(path.data(), slash);
    } catch (const std::bad_alloc&) {
        return EndpointError::cleanup_failed;
    }

    struct stat before {};
    if (::lstat(parent_input.c_str(), &before) != 0) {
        return EndpointError::parent_stat_failed;
    }
    if (!S_ISDIR(before.st_mode)) {
        return EndpointError::parent_not_directory;
    }
    if (before.st_uid != expected_uid) {
        return EndpointError::parent_owner_mismatch;
    }
    if ((before.st_mode & 0777) != 0700) {
        return EndpointError::parent_permissions_insecure;
    }

    char resolved[PATH_MAX]{};
    if (::realpath(parent_input.c_str(), resolved) == nullptr) {
        return EndpointError::parent_stat_failed;
    }

    int parent_fd = ::open(
        resolved,
        O_RDONLY | O_DIRECTORY | O_CLOEXEC | O_NOFOLLOW);
    if (parent_fd < 0) {
        return EndpointError::parent_stat_failed;
    }

    struct stat pinned {};
    if (::fstat(parent_fd, &pinned) != 0) {
        close_ignored(parent_fd);
        return EndpointError::parent_stat_failed;
    }
    if (!S_ISDIR(pinned.st_mode)) {
        close_ignored(parent_fd);
        return EndpointError::parent_not_directory;
    }
    if (pinned.st_uid != expected_uid) {
        close_ignored(parent_fd);
        return EndpointError::parent_owner_mismatch;
    }
    if ((pinned.st_mode & 0777) != 0700) {
        close_ignored(parent_fd);
        return EndpointError::parent_permissions_insecure;
    }
    if (pinned.st_dev != before.st_dev ||
        pinned.st_ino != before.st_ino) {
        close_ignored(parent_fd);
        return EndpointError::parent_identity_changed;
    }

    try {
        parent.canonical_path.assign(resolved);
    } catch (const std::bad_alloc&) {
        close_ignored(parent_fd);
        return EndpointError::cleanup_failed;
    }

    parent.fd = parent_fd;
    parent.device = pinned.st_dev;
    parent.inode = pinned.st_ino;

    address.address.sun_family = AF_UNIX;
    std::memcpy(
        address.address.sun_path,
        owned_path.data(),
        owned_path.size());
    address.address.sun_path[owned_path.size()] = '\0';
    address.length =
        static_cast<socklen_t>(
            offsetof(sockaddr_un, sun_path) +
            owned_path.size() +
            1U);
    return EndpointError::ok;
}

bool parent_identity_matches(
    int parent_fd,
    const std::string& canonical_parent,
    uid_t expected_uid,
    dev_t expected_device,
    ino_t expected_inode) noexcept {
    if (parent_fd < 0 || canonical_parent.empty()) {
        return false;
    }
    struct stat pinned {};
    if (::fstat(parent_fd, &pinned) != 0 ||
        !S_ISDIR(pinned.st_mode) ||
        pinned.st_uid != expected_uid ||
        (pinned.st_mode & 0777) != 0700 ||
        pinned.st_dev != expected_device ||
        pinned.st_ino != expected_inode) {
        return false;
    }
    struct stat current {};
    if (::stat(canonical_parent.c_str(), &current) != 0 ||
        !S_ISDIR(current.st_mode) ||
        current.st_uid != expected_uid ||
        (current.st_mode & 0777) != 0700 ||
        current.st_dev != expected_device ||
        current.st_ino != expected_inode) {
        return false;
    }
    return true;
}

bool endpoint_identity_matches(
    const std::string& path,
    uid_t expected_uid,
    dev_t expected_device,
    ino_t expected_inode) noexcept {
    struct stat current {};
    if (::lstat(path.c_str(), &current) != 0) {
        return false;
    }
    return S_ISSOCK(current.st_mode) &&
           current.st_uid == expected_uid &&
           current.st_dev == expected_device &&
           current.st_ino == expected_inode;
}

EndpointError unlink_owned_endpoint(
    const std::string& path,
    uid_t expected_uid,
    dev_t expected_device,
    ino_t expected_inode) noexcept {
    if (!endpoint_identity_matches(
            path,
            expected_uid,
            expected_device,
            expected_inode)) {
        return EndpointError::stale_endpoint_unsafe;
    }
    return ::unlink(path.c_str()) == 0
        ? EndpointError::ok
        : EndpointError::cleanup_failed;
}

EndpointError acquire_lifecycle_lock(
    int parent_fd,
    uid_t expected_uid,
    int& lock_fd) noexcept {
    lock_fd = -1;
    int fd = ::openat(
        parent_fd,
        kLockName,
        O_RDWR | O_CLOEXEC | O_NOFOLLOW);
    if (fd < 0 && errno == ENOENT) {
        fd = ::openat(
            parent_fd,
            kLockName,
            O_RDWR | O_CLOEXEC | O_NOFOLLOW | O_CREAT | O_EXCL,
            0600);
        if (fd < 0 && errno == EEXIST) {
            fd = ::openat(
                parent_fd,
                kLockName,
                O_RDWR | O_CLOEXEC | O_NOFOLLOW);
        }
    }
    if (fd < 0) {
        return EndpointError::lock_open_failed;
    }

    struct stat lock_stat {};
    if (::fstat(fd, &lock_stat) != 0 ||
        !S_ISREG(lock_stat.st_mode) ||
        lock_stat.st_uid != expected_uid ||
        (lock_stat.st_mode & 0777) != 0600 ||
        lock_stat.st_nlink != 1) {
        close_ignored(fd);
        return EndpointError::lock_unsafe;
    }

    flock lock {};
    lock.l_type = F_WRLCK;
    lock.l_whence = SEEK_SET;
    lock.l_start = 0;
    lock.l_len = 0;
    if (::fcntl(fd, F_SETLK, &lock) != 0) {
        const int saved = errno;
        close_ignored(fd);
        return saved == EACCES || saved == EAGAIN
            ? EndpointError::lock_busy
            : EndpointError::lock_open_failed;
    }

    lock_fd = fd;
    return EndpointError::ok;
}

bool still_holds_lifecycle_lock(int lock_fd) noexcept {
    if (lock_fd < 0) {
        return false;
    }
    flock lock {};
    lock.l_type = F_WRLCK;
    lock.l_whence = SEEK_SET;
    lock.l_start = 0;
    lock.l_len = 0;
    return ::fcntl(lock_fd, F_SETLK, &lock) == 0;
}

WaitResult wait_fd(
    int fd,
    short events,
    const std::chrono::steady_clock::time_point* deadline) noexcept {
    for (;;) {
        int timeout_ms = -1;
        if (deadline != nullptr) {
            const auto now = std::chrono::steady_clock::now();
            if (now >= *deadline) {
                return WaitResult::timed_out;
            }
            auto remaining =
                std::chrono::duration_cast<std::chrono::milliseconds>(
                    *deadline - now).count();
            if (remaining <= 0) {
                remaining = 1;
            }
            if (remaining > INT_MAX) {
                remaining = INT_MAX;
            }
            timeout_ms = static_cast<int>(remaining);
        }

        pollfd item{fd, events, 0};
        const int rc = ::poll(&item, 1, timeout_ms);
        if (rc < 0 && errno == EINTR) {
            continue;
        }
        if (rc == 0) {
            return WaitResult::timed_out;
        }
        if (rc < 0) {
            return WaitResult::failed;
        }
        if ((item.revents & events) != 0) {
            return WaitResult::ready;
        }
        if ((item.revents & (POLLERR | POLLHUP | POLLNVAL)) != 0) {
            return WaitResult::failed;
        }
    }
}

std::pair<int, EndpointError> accept_client(
    int listener_fd,
    const std::chrono::steady_clock::time_point* deadline) noexcept {
    for (;;) {
        const WaitResult waited =
            wait_fd(listener_fd, POLLIN, deadline);
        if (waited == WaitResult::timed_out) {
            return {-1, EndpointError::timed_out};
        }
        if (waited == WaitResult::failed) {
            return {-1, EndpointError::accept_failed};
        }

        const int client =
            ::accept4(
                listener_fd,
                nullptr,
                nullptr,
                SOCK_CLOEXEC);
        if (client >= 0) {
            return {client, EndpointError::ok};
        }
        if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
            continue;
        }
        return {-1, EndpointError::accept_failed};
    }
}

ProbeResult probe_endpoint_until(
    const UnixAddress& address,
    std::chrono::steady_clock::time_point deadline) noexcept {
    const int fd =
        ::socket(
            AF_UNIX,
            SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK,
            0);
    if (fd < 0) {
        return ProbeResult::failed;
    }

    const int rc =
        ::connect(
            fd,
            reinterpret_cast<const sockaddr*>(&address.address),
            address.length);
    if (rc == 0) {
        close_ignored(fd);
        return ProbeResult::live;
    }

    const int first_error = errno;
    if (first_error == ECONNREFUSED) {
        close_ignored(fd);
        return ProbeResult::refused;
    }
    if (first_error == ENOENT) {
        close_ignored(fd);
        return ProbeResult::missing;
    }
    if (first_error == EAGAIN) {
        close_ignored(fd);
        return ProbeResult::live;
    }
    if (first_error != EINPROGRESS && first_error != EALREADY) {
        close_ignored(fd);
        return ProbeResult::failed;
    }

    const WaitResult waited =
        wait_fd(fd, POLLOUT, &deadline);
    if (waited == WaitResult::timed_out) {
        close_ignored(fd);
        return ProbeResult::timed_out;
    }
    if (waited == WaitResult::failed) {
        close_ignored(fd);
        return ProbeResult::failed;
    }

    int socket_error = 0;
    socklen_t error_size =
        static_cast<socklen_t>(sizeof(socket_error));
    if (::getsockopt(
            fd,
            SOL_SOCKET,
            SO_ERROR,
            &socket_error,
            &error_size) != 0 ||
        error_size != sizeof(socket_error)) {
        close_ignored(fd);
        return ProbeResult::failed;
    }
    close_ignored(fd);

    if (socket_error == 0) {
        return ProbeResult::live;
    }
    if (socket_error == ECONNREFUSED) {
        return ProbeResult::refused;
    }
    if (socket_error == ENOENT) {
        return ProbeResult::missing;
    }
    if (socket_error == ETIMEDOUT) {
        return ProbeResult::timed_out;
    }
    if (socket_error == EAGAIN) {
        return ProbeResult::live;
    }
    return ProbeResult::failed;
}

std::pair<int, EndpointError> connect_bounded_impl(
    const UnixAddress& address,
    uid_t expected_server_uid,
    std::chrono::steady_clock::time_point deadline) {
    const int fd =
        ::socket(
            AF_UNIX,
            SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK,
            0);
    if (fd < 0) {
        return {-1, EndpointError::socket_create_failed};
    }

    const int rc =
        ::connect(
            fd,
            reinterpret_cast<const sockaddr*>(&address.address),
            address.length);
    if (rc != 0) {
        if (errno != EINPROGRESS && errno != EALREADY) {
            const int saved = errno;
            close_ignored(fd);
            return {
                -1,
                saved == ETIMEDOUT
                    ? EndpointError::timed_out
                    : EndpointError::connect_failed};
        }

        const WaitResult waited =
            wait_fd(fd, POLLOUT, &deadline);
        if (waited == WaitResult::timed_out) {
            close_ignored(fd);
            return {-1, EndpointError::timed_out};
        }
        if (waited == WaitResult::failed) {
            close_ignored(fd);
            return {-1, EndpointError::connect_failed};
        }

        int socket_error = 0;
        socklen_t error_size =
            static_cast<socklen_t>(sizeof(socket_error));
        if (::getsockopt(
                fd,
                SOL_SOCKET,
                SO_ERROR,
                &socket_error,
                &error_size) != 0 ||
            error_size != sizeof(socket_error)) {
            close_ignored(fd);
            return {-1, EndpointError::connect_failed};
        }
        if (socket_error != 0) {
            close_ignored(fd);
            return {
                -1,
                socket_error == ETIMEDOUT
                    ? EndpointError::timed_out
                    : EndpointError::connect_failed};
        }
    }

    const int flags = ::fcntl(fd, F_GETFL);
    if (flags < 0 ||
        ::fcntl(fd, F_SETFL, flags & ~O_NONBLOCK) != 0) {
        close_ignored(fd);
        return {-1, EndpointError::connect_failed};
    }

    const auto peer = query_peer_credentials(fd);
    if (peer.second != TransportError::ok ||
        peer.first.uid != expected_server_uid) {
        close_ignored(fd);
        return {-1, EndpointError::peer_auth_failed};
    }
    return {fd, EndpointError::ok};
}

} // namespace

RegistryEndpointListener::RegistryEndpointListener(
    int fd,
    int parent_fd,
    int lock_fd,
    std::string path,
    std::string canonical_parent,
    dev_t parent_device,
    ino_t parent_inode,
    dev_t path_device,
    ino_t path_inode,
    uid_t path_uid,
    pid_t creator_pid) noexcept
    : fd_(fd),
      parent_fd_(parent_fd),
      lock_fd_(lock_fd),
      path_(std::move(path)),
      canonical_parent_(std::move(canonical_parent)),
      parent_device_(parent_device),
      parent_inode_(parent_inode),
      path_device_(path_device),
      path_inode_(path_inode),
      path_uid_(path_uid),
      creator_pid_(creator_pid) {}

RegistryEndpointListener::~RegistryEndpointListener() {
    (void)close_and_unlink();
}

RegistryEndpointListener::RegistryEndpointListener(
    RegistryEndpointListener&& other) noexcept
    : fd_(other.fd_),
      parent_fd_(other.parent_fd_),
      lock_fd_(other.lock_fd_),
      path_(std::move(other.path_)),
      canonical_parent_(std::move(other.canonical_parent_)),
      parent_device_(other.parent_device_),
      parent_inode_(other.parent_inode_),
      path_device_(other.path_device_),
      path_inode_(other.path_inode_),
      path_uid_(other.path_uid_),
      creator_pid_(other.creator_pid_) {
    other.fd_ = -1;
    other.parent_fd_ = -1;
    other.lock_fd_ = -1;
    other.path_.clear();
    other.canonical_parent_.clear();
    other.parent_device_ = 0;
    other.parent_inode_ = 0;
    other.path_device_ = 0;
    other.path_inode_ = 0;
    other.path_uid_ = static_cast<uid_t>(-1);
    other.creator_pid_ = -1;
}

std::pair<RegistryEndpointListener, EndpointError>
RegistryEndpointListener::create(
    std::string_view path,
    uid_t expected_uid,
    int backlog) {
    if (backlog <= 0 || backlog > SOMAXCONN) {
        return {RegistryEndpointListener{}, EndpointError::invalid_argument};
    }

    std::string owned_path;
    ParentCapability parent{};
    UnixAddress address{};
    const EndpointError qualified =
        qualify_parent(
            path,
            expected_uid,
            owned_path,
            parent,
            address);
    if (qualified != EndpointError::ok) {
        return {RegistryEndpointListener{}, qualified};
    }

    auto local_pair = LocalLockReservation::acquire();
    LocalLockReservation local = std::move(local_pair.first);
    if (!local_pair.second) {
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::lock_busy};
    }

    int lock_fd = -1;
    const EndpointError locked =
        acquire_lifecycle_lock(parent.fd, expected_uid, lock_fd);
    if (locked != EndpointError::ok) {
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, locked};
    }

    struct stat existing {};
    if (::lstat(owned_path.c_str(), &existing) == 0) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::endpoint_exists};
    }
    if (errno != ENOENT) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::bind_failed};
    }

    const int fd =
        ::socket(
            AF_UNIX,
            SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK,
            0);
    if (fd < 0) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::socket_create_failed};
    }

    if (::bind(
            fd,
            reinterpret_cast<const sockaddr*>(&address.address),
            address.length) != 0) {
        const int saved = errno;
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {
            RegistryEndpointListener{},
            saved == EADDRINUSE
                ? EndpointError::endpoint_exists
                : EndpointError::bind_failed};
    }

    struct stat bound {};
    if (::lstat(owned_path.c_str(), &bound) != 0 ||
        !S_ISSOCK(bound.st_mode) ||
        bound.st_uid != expected_uid) {
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::bind_failed};
    }

    const dev_t bound_device = bound.st_dev;
    const ino_t bound_inode = bound.st_ino;

    if (!parent_identity_matches(
            parent.fd,
            parent.canonical_path,
            expected_uid,
            parent.device,
            parent.inode)) {
        (void)unlink_owned_endpoint(
            owned_path,
            expected_uid,
            bound_device,
            bound_inode);
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::parent_identity_changed};
    }

    if (::chmod(owned_path.c_str(), 0600) != 0) {
        (void)unlink_owned_endpoint(
            owned_path,
            expected_uid,
            bound_device,
            bound_inode);
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::chmod_failed};
    }

    if (!endpoint_identity_matches(
            owned_path,
            expected_uid,
            bound_device,
            bound_inode)) {
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::stale_endpoint_unsafe};
    }

    if (::listen(fd, backlog) != 0) {
        (void)unlink_owned_endpoint(
            owned_path,
            expected_uid,
            bound_device,
            bound_inode);
        close_ignored(fd);
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return {RegistryEndpointListener{}, EndpointError::listen_failed};
    }

    local.commit();
    return {
        RegistryEndpointListener(
            fd,
            parent.fd,
            lock_fd,
            std::move(owned_path),
            std::move(parent.canonical_path),
            parent.device,
            parent.inode,
            bound_device,
            bound_inode,
            expected_uid,
            ::getpid()),
        EndpointError::ok};
}

int RegistryEndpointListener::native_handle() const noexcept {
    return fd_;
}

EndpointError RegistryEndpointListener::serve_once(
    NamedRegistry& registry,
    uid_t expected_peer_uid) noexcept {
    if (fd_ < 0 || ::getpid() != creator_pid_) {
        return EndpointError::invalid_argument;
    }

    const auto accepted = accept_client(fd_, nullptr);
    if (accepted.second != EndpointError::ok) {
        return accepted.second;
    }

    const BrokerError result =
        serve_registry_request_once(
            accepted.first,
            registry,
            expected_peer_uid);
    const int close_result = ::close(accepted.first);
    if (result == BrokerError::peer_auth_failed) {
        return EndpointError::peer_auth_failed;
    }
    if (result != BrokerError::ok) {
        return EndpointError::broker_failed;
    }
    return close_result == 0
        ? EndpointError::ok
        : EndpointError::cleanup_failed;
}

EndpointError RegistryEndpointListener::serve_once_bounded(
    NamedRegistry& registry,
    uid_t expected_peer_uid,
    std::chrono::milliseconds timeout) noexcept {
    if (fd_ < 0 ||
        ::getpid() != creator_pid_ ||
        timeout.count() <= 0) {
        return EndpointError::invalid_argument;
    }

    const auto deadline =
        std::chrono::steady_clock::now() + timeout;
    const auto accepted =
        accept_client(fd_, &deadline);
    if (accepted.second != EndpointError::ok) {
        return accepted.second;
    }

    const BrokerError result =
        serve_registry_request_once_until(
            accepted.first,
            registry,
            expected_peer_uid,
            deadline);
    const int close_result = ::close(accepted.first);
    if (result == BrokerError::timed_out) {
        return EndpointError::timed_out;
    }
    if (result == BrokerError::peer_auth_failed) {
        return EndpointError::peer_auth_failed;
    }
    if (result != BrokerError::ok) {
        return EndpointError::broker_failed;
    }
    return close_result == 0
        ? EndpointError::ok
        : EndpointError::cleanup_failed;
}

EndpointError RegistryEndpointListener::close_and_unlink() noexcept {
    EndpointError result = close_owned(fd_);

    if (::getpid() != creator_pid_) {
        close_ignored(lock_fd_);
        close_ignored(parent_fd_);
        lock_fd_ = -1;
        parent_fd_ = -1;
        path_.clear();
        canonical_parent_.clear();
        creator_pid_ = -1;
        return result;
    }

    if (!path_.empty()) {
        if (!parent_identity_matches(
                parent_fd_,
                canonical_parent_,
                path_uid_,
                parent_device_,
                parent_inode_) ||
            !still_holds_lifecycle_lock(lock_fd_)) {
            result = EndpointError::stale_endpoint_unsafe;
        } else {
            struct stat current {};
            if (::lstat(path_.c_str(), &current) == 0) {
                const EndpointError removed =
                    unlink_owned_endpoint(
                        path_,
                        path_uid_,
                        path_device_,
                        path_inode_);
                if (removed != EndpointError::ok) {
                    result = removed;
                }
            } else if (errno != ENOENT) {
                result = EndpointError::cleanup_failed;
            }
        }
    }

    close_ignored(lock_fd_);
    release_local_lock_owner(creator_pid_);
    close_ignored(parent_fd_);

    lock_fd_ = -1;
    parent_fd_ = -1;
    path_.clear();
    canonical_parent_.clear();
    parent_device_ = 0;
    parent_inode_ = 0;
    path_device_ = 0;
    path_inode_ = 0;
    path_uid_ = static_cast<uid_t>(-1);
    creator_pid_ = -1;
    return result;
}

std::pair<int, EndpointError> connect_registry_endpoint(
    std::string_view path,
    uid_t expected_server_uid) {
    std::string owned_path;
    ParentCapability parent{};
    UnixAddress address{};
    const EndpointError qualified =
        qualify_parent(
            path,
            expected_server_uid,
            owned_path,
            parent,
            address);
    if (qualified != EndpointError::ok) {
        return {-1, qualified};
    }
    close_ignored(parent.fd);

    const int fd =
        ::socket(
            AF_UNIX,
            SOCK_STREAM | SOCK_CLOEXEC,
            0);
    if (fd < 0) {
        return {-1, EndpointError::socket_create_failed};
    }

    if (::connect(
            fd,
            reinterpret_cast<const sockaddr*>(&address.address),
            address.length) != 0) {
        close_ignored(fd);
        return {-1, EndpointError::connect_failed};
    }

    const auto peer = query_peer_credentials(fd);
    if (peer.second != TransportError::ok ||
        peer.first.uid != expected_server_uid) {
        close_ignored(fd);
        return {-1, EndpointError::peer_auth_failed};
    }
    return {fd, EndpointError::ok};
}

std::pair<int, EndpointError> connect_registry_endpoint_bounded(
    std::string_view path,
    uid_t expected_server_uid,
    std::chrono::milliseconds timeout) {
    if (timeout.count() <= 0) {
        return {-1, EndpointError::invalid_argument};
    }

    std::string owned_path;
    ParentCapability parent{};
    UnixAddress address{};
    const EndpointError qualified =
        qualify_parent(
            path,
            expected_server_uid,
            owned_path,
            parent,
            address);
    if (qualified != EndpointError::ok) {
        return {-1, qualified};
    }
    close_ignored(parent.fd);

    return connect_bounded_impl(
        address,
        expected_server_uid,
        std::chrono::steady_clock::now() + timeout);
}

EndpointError remove_stale_registry_endpoint(
    std::string_view path,
    uid_t expected_uid) {
    std::string owned_path;
    ParentCapability parent{};
    UnixAddress address{};
    const EndpointError qualified =
        qualify_parent(
            path,
            expected_uid,
            owned_path,
            parent,
            address);
    if (qualified != EndpointError::ok) {
        return qualified;
    }

    struct stat current {};
    if (::lstat(owned_path.c_str(), &current) != 0) {
        close_ignored(parent.fd);
        return errno == ENOENT
            ? EndpointError::ok
            : EndpointError::cleanup_failed;
    }
    if (!S_ISSOCK(current.st_mode) ||
        current.st_uid != expected_uid) {
        close_ignored(parent.fd);
        return EndpointError::stale_endpoint_unsafe;
    }

    close_ignored(parent.fd);
    return EndpointError::stale_recovery_deferred;
}

EndpointError remove_stale_registry_endpoint_bounded(
    std::string_view path,
    uid_t expected_uid,
    std::chrono::milliseconds timeout) {
    if (timeout.count() <= 0) {
        return EndpointError::invalid_argument;
    }

    std::string owned_path;
    ParentCapability parent{};
    UnixAddress address{};
    const EndpointError qualified =
        qualify_parent(
            path,
            expected_uid,
            owned_path,
            parent,
            address);
    if (qualified != EndpointError::ok) {
        return qualified;
    }

    auto local_pair = LocalLockReservation::acquire();
    LocalLockReservation local = std::move(local_pair.first);
    if (!local_pair.second) {
        close_ignored(parent.fd);
        return EndpointError::lock_busy;
    }

    int lock_fd = -1;
    const EndpointError locked =
        acquire_lifecycle_lock(parent.fd, expected_uid, lock_fd);
    if (locked != EndpointError::ok) {
        close_ignored(parent.fd);
        return locked;
    }

    struct stat before {};
    if (::lstat(owned_path.c_str(), &before) != 0) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return errno == ENOENT
            ? EndpointError::ok
            : EndpointError::cleanup_failed;
    }
    if (!S_ISSOCK(before.st_mode) ||
        before.st_uid != expected_uid) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::stale_endpoint_unsafe;
    }

    const auto deadline =
        std::chrono::steady_clock::now() + timeout;
    const ProbeResult probe =
        probe_endpoint_until(address, deadline);

    if (probe == ProbeResult::live) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::endpoint_live;
    }
    if (probe == ProbeResult::timed_out) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::timed_out;
    }
    if (probe == ProbeResult::missing) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::ok;
    }
    if (probe != ProbeResult::refused) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::connect_failed;
    }

    if (!parent_identity_matches(
            parent.fd,
            parent.canonical_path,
            expected_uid,
            parent.device,
            parent.inode) ||
        !still_holds_lifecycle_lock(lock_fd) ||
        !endpoint_identity_matches(
            owned_path,
            expected_uid,
            before.st_dev,
            before.st_ino)) {
        close_ignored(lock_fd);
        close_ignored(parent.fd);
        return EndpointError::stale_endpoint_unsafe;
    }

    const EndpointError removed =
        unlink_owned_endpoint(
            owned_path,
            expected_uid,
            before.st_dev,
            before.st_ino);

    close_ignored(lock_fd);
    close_ignored(parent.fd);
    return removed;
}

} // namespace openmind::secure_memory
