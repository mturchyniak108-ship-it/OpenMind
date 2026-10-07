#include "openmind/named_registry_broker.hpp"
#include "openmind/registry_endpoint.hpp"

#include <cerrno>
#include <chrono>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <string>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <unistd.h>
#include <vector>

namespace {

constexpr std::size_t kSize = 4096U;
constexpr int kRequestCount = 6;

[[noreturn]] void fail(const char* gate) {
    std::fprintf(
        stderr,
        "FAIL=%s errno=%d (%s)\n",
        gate,
        errno,
        std::strerror(errno));
    std::exit(2);
}

void require(bool condition, const char* gate) {
    if (!condition) {
        fail(gate);
    }
}

std::string make_temp_dir() {
    const char* tmp = std::getenv("TMPDIR");
    const std::string base =
        tmp != nullptr && tmp[0] != '\0' ? tmp : "/tmp";
    std::string pattern = base + "/openmind-p3f-r2a-rebase-XXXXXX";
    std::vector<char> writable(pattern.begin(), pattern.end());
    writable.push_back('\0');
    char* made = ::mkdtemp(writable.data());
    require(made != nullptr, "MKDTEMP");
    require(::chmod(made, 0700) == 0, "TMP_CHMOD");
    return std::string(made);
}

int connect_or_fail(
    const std::string& path,
    uid_t uid,
    const char* gate) {
    const auto connected =
        openmind::secure_memory::connect_registry_endpoint(path, uid);
    require(
        connected.first >= 0 &&
            connected.second ==
                openmind::secure_memory::EndpointError::ok,
        gate);
    return connected.first;
}

void child_flow(const std::string& path, uid_t uid) {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::RegistryError;
    using openmind::secure_memory::RegistryOpenOptions;
    using openmind::secure_memory::broker_open;
    using openmind::secure_memory::broker_unlink;

    int socket_fd =
        connect_or_fail(path, uid, "CLIENT_CONNECT_CREATE");
    auto created = broker_open(
        socket_fd,
        "/endpoint",
        RegistryOpenOptions{true, true, 0U},
        uid);
    require(
        created.fd >= 0 &&
            created.broker_error == BrokerError::ok &&
            created.registry_error == RegistryError::ok,
        "CLIENT_CREATE");
    require(::close(socket_fd) == 0, "CLIENT_CREATE_SOCKET_CLOSE");

    require(
        ::ftruncate(created.fd, static_cast<off_t>(kSize)) == 0,
        "CLIENT_FTRUNCATE");

    void* writer = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        created.fd,
        0);
    require(writer != MAP_FAILED, "CLIENT_WRITER_MAP");
    std::memcpy(writer, "ENDPOINT", 8U);

    socket_fd = connect_or_fail(path, uid, "CLIENT_CONNECT_REOPEN");
    auto reopened = broker_open(
        socket_fd,
        "/endpoint",
        RegistryOpenOptions{},
        uid);
    require(
        reopened.fd >= 0 &&
            reopened.broker_error == BrokerError::ok &&
            reopened.registry_error == RegistryError::ok,
        "CLIENT_REOPEN");
    require(::close(socket_fd) == 0, "CLIENT_REOPEN_SOCKET_CLOSE");

    void* reader = ::mmap(
        nullptr,
        kSize,
        PROT_READ,
        MAP_SHARED,
        reopened.fd,
        0);
    require(reader != MAP_FAILED, "CLIENT_READER_MAP");
    require(
        std::memcmp(reader, "ENDPOINT", 8U) == 0,
        "CLIENT_REOPEN_CONTENT");

    socket_fd = connect_or_fail(path, uid, "CLIENT_CONNECT_UNLINK");
    const auto unlinked = broker_unlink(socket_fd, "/endpoint", uid);
    require(
        unlinked.broker_error == BrokerError::ok &&
            unlinked.registry_error == RegistryError::ok,
        "CLIENT_UNLINK");
    require(::close(socket_fd) == 0, "CLIENT_UNLINK_SOCKET_CLOSE");
    require(
        std::memcmp(reader, "ENDPOINT", 8U) == 0,
        "CLIENT_LIVE_MAP");

    socket_fd = connect_or_fail(path, uid, "CLIENT_CONNECT_MISSING");
    auto missing = broker_open(
        socket_fd,
        "/endpoint",
        RegistryOpenOptions{},
        uid);
    require(
        missing.fd < 0 &&
            missing.broker_error == BrokerError::ok &&
            missing.registry_error == RegistryError::not_found,
        "CLIENT_MISSING");
    require(::close(socket_fd) == 0, "CLIENT_MISSING_SOCKET_CLOSE");

    socket_fd = connect_or_fail(path, uid, "CLIENT_CONNECT_RECREATE");
    auto recreated = broker_open(
        socket_fd,
        "/endpoint",
        RegistryOpenOptions{true, true, 0U},
        uid);
    require(
        recreated.fd >= 0 &&
            recreated.broker_error == BrokerError::ok &&
            recreated.registry_error == RegistryError::ok,
        "CLIENT_RECREATE");
    require(::close(socket_fd) == 0, "CLIENT_RECREATE_SOCKET_CLOSE");

    struct stat old_stat {};
    struct stat new_stat {};
    require(::fstat(created.fd, &old_stat) == 0, "CLIENT_OLD_FSTAT");
    require(::fstat(recreated.fd, &new_stat) == 0, "CLIENT_NEW_FSTAT");
    require(new_stat.st_size == 0, "CLIENT_RECREATE_ZERO");
    require(
        old_stat.st_dev != new_stat.st_dev ||
            old_stat.st_ino != new_stat.st_ino,
        "CLIENT_RECREATE_DISTINCT");

    socket_fd = connect_or_fail(path, uid, "CLIENT_CONNECT_FINAL_UNLINK");
    const auto final_unlink = broker_unlink(socket_fd, "/endpoint", uid);
    require(
        final_unlink.broker_error == BrokerError::ok &&
            final_unlink.registry_error == RegistryError::ok,
        "CLIENT_FINAL_UNLINK");
    require(::close(socket_fd) == 0, "CLIENT_FINAL_SOCKET_CLOSE");

    require(::munmap(reader, kSize) == 0, "CLIENT_READER_UNMAP");
    require(::munmap(writer, kSize) == 0, "CLIENT_WRITER_UNMAP");
    require(::close(recreated.fd) == 0, "CLIENT_RECREATE_CLOSE");
    require(::close(reopened.fd) == 0, "CLIENT_REOPEN_CLOSE");
    require(::close(created.fd) == 0, "CLIENT_CREATE_CLOSE");
}

} // namespace

int main() {
    using openmind::secure_memory::EndpointError;
    using openmind::secure_memory::NamedRegistry;
    using openmind::secure_memory::RegistryEndpointListener;
    using openmind::secure_memory::remove_stale_registry_endpoint;
    using openmind::secure_memory::remove_stale_registry_endpoint_bounded;

    const uid_t uid = ::getuid();
    const std::string dir = make_temp_dir();
    const std::string path = dir + "/registry.sock";
    const std::string lock_path = dir + "/registry.lock";

    auto made = RegistryEndpointListener::create(path, uid, 8);
    require(
        made.second == EndpointError::ok &&
            made.first.native_handle() >= 0,
        "LISTENER_CREATE");
    RegistryEndpointListener listener = std::move(made.first);

    NamedRegistry registry;
    require(
        listener.serve_once_bounded(
            registry,
            uid,
            std::chrono::milliseconds(120)) ==
            EndpointError::timed_out,
        "R2B_ACCEPT_TIMEOUT");
    std::printf("R2B_BOUNDED_ACCEPT=PASS\n");

    require(
        remove_stale_registry_endpoint_bounded(
            path,
            uid,
            std::chrono::milliseconds(120)) ==
            EndpointError::lock_busy,
        "R2B_LIVE_LOCK_PROTECTED");
    std::printf("R2B_LIVE_ENDPOINT_LOCK_PROTECTED=PASS\n");

    struct stat endpoint_stat {};
    require(::lstat(path.c_str(), &endpoint_stat) == 0, "ENDPOINT_LSTAT");
    require(S_ISSOCK(endpoint_stat.st_mode), "ENDPOINT_IS_SOCKET");
    require(endpoint_stat.st_uid == uid, "ENDPOINT_OWNER");
    require((endpoint_stat.st_mode & 0777) == 0600, "ENDPOINT_MODE_0600");

    struct stat lock_stat {};
    require(::lstat(lock_path.c_str(), &lock_stat) == 0, "LOCK_LSTAT");
    require(S_ISREG(lock_stat.st_mode), "LOCK_IS_REGULAR");
    require(lock_stat.st_uid == uid, "LOCK_OWNER");
    require((lock_stat.st_mode & 0777) == 0600, "LOCK_MODE_0600");
    require(lock_stat.st_nlink == 1, "LOCK_NLINK_ONE");
    std::printf("R2A_DIRECTORY_LOCK_CAPABILITY=PASS\n");

    const auto same_process = RegistryEndpointListener::create(path, uid, 8);
    require(
        same_process.second == EndpointError::lock_busy,
        "SAME_PROCESS_SECOND_OWNER_REJECTED");
    std::printf("R2A_SAME_PROCESS_LOCK_GUARD=PASS\n");

    const pid_t contender = ::fork();
    require(contender >= 0, "CONTENDER_FORK");
    if (contender == 0) {
        const auto result = RegistryEndpointListener::create(path, uid, 8);
        _exit(result.second == EndpointError::lock_busy ? 0 : 8);
    }
    int contender_status = 0;
    require(
        ::waitpid(contender, &contender_status, 0) == contender,
        "CONTENDER_WAIT");
    require(
        WIFEXITED(contender_status) &&
            WEXITSTATUS(contender_status) == 0,
        "CROSS_PROCESS_LOCK_BUSY");
    std::printf("R2A_CROSS_PROCESS_F_SETLK=PASS\n");

    const pid_t cleanup_child = ::fork();
    require(cleanup_child >= 0, "CLEANUP_FORK");
    if (cleanup_child == 0) {
        const auto result = listener.close_and_unlink();
        _exit(result == EndpointError::ok ? 0 : 7);
    }
    int cleanup_status = 0;
    require(
        ::waitpid(cleanup_child, &cleanup_status, 0) == cleanup_child,
        "CLEANUP_WAIT");
    require(
        WIFEXITED(cleanup_status) &&
            WEXITSTATUS(cleanup_status) == 0,
        "CLEANUP_CHILD_STATUS");
    require(::lstat(path.c_str(), &endpoint_stat) == 0, "CHILD_DID_NOT_UNLINK");
    std::printf("R2A_CHILD_CLEANUP_GUARD=PASS\n");

    const pid_t child = ::fork();
    require(child >= 0, "FORK");
    if (child == 0) {
        child_flow(path, uid);
        _exit(0);
    }

    for (int index = 0; index < kRequestCount; ++index) {
        require(
            listener.serve_once(registry, uid) == EndpointError::ok,
            "SERVE_ONCE");
    }

    int status = 0;
    require(::waitpid(child, &status, 0) == child, "WAITPID");
    require(
        WIFEXITED(status) &&
            WEXITSTATUS(status) == 0,
        "CHILD_STATUS");
    std::printf("R2A_NAMESPACE_LIFECYCLE=PASS\n");

    require(
        listener.close_and_unlink() == EndpointError::ok,
        "LISTENER_CLOSE");
    require(
        ::access(path.c_str(), F_OK) != 0 &&
            errno == ENOENT,
        "ENDPOINT_REMOVED");
    require(::access(lock_path.c_str(), F_OK) == 0, "LOCKFILE_PERSISTS");
    std::printf("R2A_OWNED_ENDPOINT_CLEANUP=PASS\n");

    int stale = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    require(stale >= 0, "STALE_SOCKET");

    sockaddr_un stale_address {};
    stale_address.sun_family = AF_UNIX;
    require(path.size() < sizeof(stale_address.sun_path), "STALE_PATH_LENGTH");
    std::memcpy(stale_address.sun_path, path.c_str(), path.size() + 1U);
    require(
        ::bind(
            stale,
            reinterpret_cast<const sockaddr*>(&stale_address),
            static_cast<socklen_t>(
                offsetof(sockaddr_un, sun_path) + path.size() + 1U)) == 0,
        "STALE_BIND");
    require(::chmod(path.c_str(), 0600) == 0, "STALE_CHMOD");
    require(::close(stale) == 0, "STALE_CLOSE");

    require(
        remove_stale_registry_endpoint(path, uid) ==
            EndpointError::stale_recovery_deferred,
        "STALE_RECOVERY_DEFERRED");
    require(::access(path.c_str(), F_OK) == 0, "STALE_PRESERVED");
    std::printf("R2A_STALE_RECOVERY_DEFERRED=PASS\n");

    require(
        remove_stale_registry_endpoint_bounded(
            path,
            uid,
            std::chrono::milliseconds(250)) ==
            EndpointError::ok,
        "R2B_STALE_REMOVE");
    require(
        ::access(path.c_str(), F_OK) != 0 &&
            errno == ENOENT,
        "R2B_STALE_GONE");
    std::printf("R2B_BOUNDED_STALE_RECOVERY=PASS\n");

    int regular = ::open(
        path.c_str(),
        O_CREAT | O_EXCL | O_WRONLY | O_CLOEXEC,
        0600);
    require(regular >= 0, "UNSAFE_FILE_CREATE");
    require(::close(regular) == 0, "UNSAFE_FILE_CLOSE");
    require(
        remove_stale_registry_endpoint(path, uid) ==
            EndpointError::stale_endpoint_unsafe,
        "UNSAFE_FILE_REJECTED");
    require(::unlink(path.c_str()) == 0, "UNSAFE_FILE_CLEANUP");
    std::printf("R2A_NONSOCKET_STALE_PATH_REJECTED=PASS\n");

    std::string long_path(108U, 'x');
    long_path.front() = '/';
    const auto too_long = RegistryEndpointListener::create(long_path, uid, 8);
    require(
        too_long.second == EndpointError::path_too_long,
        "PATH_LIMIT");
    std::printf("R2A_PATH_LIMIT_FAIL_CLOSED=PASS\n");

    const auto wrong_basename =
        RegistryEndpointListener::create(dir + "/other.sock", uid, 8);
    require(
        wrong_basename.second == EndpointError::invalid_argument,
        "FIXED_BASENAME_REQUIRED");

    const auto dot_component =
        RegistryEndpointListener::create(dir + "/../registry.sock", uid, 8);
    require(
        dot_component.second == EndpointError::invalid_argument,
        "DOT_DOT_REJECTED");
    std::printf("R2A_PATH_SYNTAX_POLICY=PASS\n");

    require(::chmod(dir.c_str(), 0755) == 0, "INSECURE_PARENT_CHMOD");
    const auto insecure_parent = RegistryEndpointListener::create(path, uid, 8);
    require(
        insecure_parent.second == EndpointError::parent_permissions_insecure,
        "0755_PARENT_REJECTED");
    require(::chmod(dir.c_str(), 0700) == 0, "SECURE_PARENT_RESTORE");

    require(::chmod(dir.c_str(), 0600) == 0, "NONEXEC_PARENT_CHMOD");
    const auto nonexec_parent = RegistryEndpointListener::create(path, uid, 8);
    require(
        nonexec_parent.second == EndpointError::parent_permissions_insecure,
        "0600_PARENT_REJECTED");
    require(::chmod(dir.c_str(), 0700) == 0, "NONEXEC_PARENT_RESTORE");
    std::printf("R2A_EXACT_0700_PARENT_REQUIRED=PASS\n");

    regular = ::open(
        path.c_str(),
        O_CREAT | O_EXCL | O_WRONLY | O_CLOEXEC,
        0600);
    require(regular >= 0, "POSTLOCK_FAILURE_FIXTURE_CREATE");
    require(::close(regular) == 0, "POSTLOCK_FAILURE_FIXTURE_CLOSE");

    const auto endpoint_exists = RegistryEndpointListener::create(path, uid, 8);
    require(
        endpoint_exists.second == EndpointError::endpoint_exists,
        "POSTLOCK_ENDPOINT_EXISTS");

    require(::unlink(path.c_str()) == 0, "POSTLOCK_FAILURE_FIXTURE_REMOVE");

    auto retry_after_failure = RegistryEndpointListener::create(path, uid, 8);
    require(
        retry_after_failure.second == EndpointError::ok &&
            retry_after_failure.first.native_handle() >= 0,
        "POSTLOCK_RESERVATION_RELEASED");
    require(
        retry_after_failure.first.close_and_unlink() == EndpointError::ok,
        "POSTLOCK_RETRY_CLOSE");
    std::printf("R2A_LOCAL_RESERVATION_RAII=PASS\n");

    require(::chmod(lock_path.c_str(), 0644) == 0, "LOCK_INSECURE_CHMOD");
    const auto unsafe_lock = RegistryEndpointListener::create(path, uid, 8);
    require(
        unsafe_lock.second == EndpointError::lock_unsafe,
        "LOCK_INSECURE_REJECTED");
    require(::chmod(lock_path.c_str(), 0600) == 0, "LOCK_SECURE_RESTORE");

    auto retry_after_lock_repair =
        RegistryEndpointListener::create(path, uid, 8);
    require(
        retry_after_lock_repair.second == EndpointError::ok,
        "LOCK_REPAIR_RETRY");
    require(
        retry_after_lock_repair.first.close_and_unlink() == EndpointError::ok,
        "LOCK_REPAIR_RETRY_CLOSE");
    std::printf("R2A_LOCK_IDENTITY_POLICY=PASS\n");

    require(::unlink(lock_path.c_str()) == 0, "LOCK_FINAL_REMOVE_TEST_ONLY");
    require(::rmdir(dir.c_str()) == 0, "TMP_RMDIR");

    std::printf("STATUS=PASS\n");
    return 0;
}
