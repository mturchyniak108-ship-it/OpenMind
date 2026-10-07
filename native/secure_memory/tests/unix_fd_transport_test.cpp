#include "openmind/android_secure_memory.hpp"
#include "openmind/unix_fd_transport.hpp"

#include <array>
#include <cerrno>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

namespace {

constexpr std::size_t kSize = 4096U;

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

bool blocked_errno(int value) {
    return value == EPERM || value == EACCES;
}

int child_consume(int socket_fd, uid_t expected_uid) {
    using openmind::secure_memory::TransportError;
    using openmind::secure_memory::receive_fd_from_uid;

    const auto received = receive_fd_from_uid(socket_fd, expected_uid);
    if (received.second != TransportError::ok || received.first < 0) {
        return 41;
    }
    const int fd = received.first;

    const int descriptor_flags = ::fcntl(fd, F_GETFD);
    if (descriptor_flags < 0 || (descriptor_flags & FD_CLOEXEC) == 0) {
        ::close(fd);
        return 42;
    }

    errno = 0;
    const ssize_t direct_write = ::write(fd, "X", 1U);
    if (direct_write != -1 || !blocked_errno(errno)) {
        ::close(fd);
        return 43;
    }

    errno = 0;
    void* rw = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        fd,
        0);
    if (rw != MAP_FAILED || !blocked_errno(errno)) {
        if (rw != MAP_FAILED) {
            ::munmap(rw, kSize);
        }
        ::close(fd);
        return 44;
    }

    void* ro = ::mmap(nullptr, kSize, PROT_READ, MAP_SHARED, fd, 0);
    if (ro == MAP_FAILED) {
        ::close(fd);
        return 45;
    }
    if (std::memcmp(ro, "P3B-RO", 6U) != 0) {
        ::munmap(ro, kSize);
        ::close(fd);
        return 46;
    }

    errno = 0;
    const int upgrade = ::mprotect(ro, kSize, PROT_READ | PROT_WRITE);
    if (upgrade == 0 || !blocked_errno(errno)) {
        ::munmap(ro, kSize);
        ::close(fd);
        return 47;
    }

    if (::munmap(ro, kSize) != 0) {
        ::close(fd);
        return 48;
    }
    if (::close(fd) != 0) {
        return 49;
    }
    return 0;
}

void test_wrong_uid_rejected() {
    using openmind::secure_memory::TransportError;
    using openmind::secure_memory::send_fd_to_uid;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "WRONG_UID_SOCKETPAIR");

    const int fd = ::open("/dev/null", O_RDONLY | O_CLOEXEC);
    require(fd >= 0, "WRONG_UID_OPEN");

    const uid_t impossible_uid =
        static_cast<uid_t>(::getuid() == static_cast<uid_t>(-2)
                               ? ::getuid() - 1U
                               : ::getuid() + 1U);

    require(
        send_fd_to_uid(sockets[0], fd, impossible_uid) ==
            TransportError::peer_uid_mismatch,
        "WRONG_UID_REJECT");

    require(::close(fd) == 0, "WRONG_UID_FD_CLOSE");
    require(::close(sockets[0]) == 0, "WRONG_UID_SOCK0_CLOSE");
    require(::close(sockets[1]) == 0, "WRONG_UID_SOCK1_CLOSE");
    std::printf("P3B_WRONG_UID_REJECTED=PASS\n");
}

void test_same_uid_transfer() {
    using openmind::secure_memory::Error;
    using openmind::secure_memory::Region;
    using openmind::secure_memory::TransportError;
    using openmind::secure_memory::query_peer_credentials;
    using openmind::secure_memory::send_fd_to_uid;

    auto created = Region::create_memfd(kSize);
    require(
        created.first.has_value() && created.second == Error::ok,
        "REGION_CREATE");
    Region region = std::move(*created.first);
    std::memcpy(region.writable_data(), "P3B-RO", 6U);
    require(region.publish_read_only() == Error::ok, "REGION_PUBLISH");

    auto transfer = region.duplicate_for_transfer();
    require(
        transfer.first >= 0 && transfer.second == Error::ok,
        "REGION_DUPLICATE");
    const int transfer_fd = transfer.first;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "SOCKETPAIR");

    const auto parent_peer = query_peer_credentials(sockets[0]);
    require(
        parent_peer.second == TransportError::ok &&
            parent_peer.first.uid == ::getuid(),
        "PARENT_PEER_UID");
    std::printf("P3B_SO_PEERCRED=PASS\n");

    const pid_t child = ::fork();
    require(child >= 0, "FORK");

    if (child == 0) {
        ::close(sockets[0]);
        ::close(transfer_fd);
        const int child_rc = child_consume(sockets[1], ::getuid());
        ::close(sockets[1]);
        _exit(child_rc);
    }

    require(::close(sockets[1]) == 0, "PARENT_CHILD_SOCKET_CLOSE");
    require(
        send_fd_to_uid(sockets[0], transfer_fd, ::getuid()) ==
            TransportError::ok,
        "SCM_RIGHTS_SEND");
    require(::close(transfer_fd) == 0, "TRANSFER_FD_CLOSE");
    require(::close(sockets[0]) == 0, "PARENT_SOCKET_CLOSE");

    int status = 0;
    require(::waitpid(child, &status, 0) == child, "WAITPID");
    require(
        WIFEXITED(status) && WEXITSTATUS(status) == 0,
        "CHILD_CONSUMER");

    require(region.finalize_publication() == Error::ok, "REGION_FINALIZE");

    std::printf("P3B_SCM_RIGHTS=PASS\n");
    std::printf("P3B_RECEIVER_CLOEXEC=PASS\n");
    std::printf("R2C_MSG_CMSG_CLOEXEC=PASS\n");
    std::printf("P3B_TRANSFERRED_FD_EFFECTIVE_READONLY=PASS\n");
}


void test_bounded_fd_receive_timeout() {
    using openmind::secure_memory::TransportError;
    using openmind::secure_memory::receive_fd_from_uid_until;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "R2B_FD_TIMEOUT_SOCKETPAIR");

    const auto start = std::chrono::steady_clock::now();
    const auto received =
        receive_fd_from_uid_until(
            sockets[0],
            ::getuid(),
            start + std::chrono::milliseconds(120));
    const auto elapsed =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now() - start);

    require(
        received.first < 0 &&
            received.second == TransportError::timed_out,
        "R2B_FD_RECEIVE_TIMEOUT_RESULT");
    require(
        elapsed.count() >= 50 &&
            elapsed.count() < 1500,
        "R2B_FD_RECEIVE_TIMEOUT_BOUND");

    require(::close(sockets[0]) == 0, "R2B_FD_TIMEOUT_CLOSE0");
    require(::close(sockets[1]) == 0, "R2B_FD_TIMEOUT_CLOSE1");
    std::printf("R2B_SCM_RIGHTS_RECEIVE_DEADLINE=PASS\n");
}

void test_bounded_fd_send_timeout() {
    using openmind::secure_memory::TransportError;
    using openmind::secure_memory::send_fd_to_uid_until;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "R2B_FD_SEND_SOCKETPAIR");

    std::array<unsigned char, 4096> filler{};
    for (;;) {
        const ssize_t rc =
            ::send(
                sockets[0],
                filler.data(),
                filler.size(),
                MSG_DONTWAIT | MSG_NOSIGNAL);
        if (rc > 0) {
            continue;
        }
        require(
            rc < 0 &&
                (errno == EAGAIN || errno == EWOULDBLOCK),
            "R2B_FILL_SEND_BUFFER");
        break;
    }

    const int fd = ::open("/dev/null", O_RDONLY | O_CLOEXEC);
    require(fd >= 0, "R2B_FD_SEND_OPEN");

    const auto start = std::chrono::steady_clock::now();
    const TransportError sent =
        send_fd_to_uid_until(
            sockets[0],
            fd,
            ::getuid(),
            start + std::chrono::milliseconds(120));
    const auto elapsed =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now() - start);

    require(
        sent == TransportError::timed_out,
        "R2B_FD_SEND_TIMEOUT_RESULT");
    require(
        elapsed.count() >= 50 &&
            elapsed.count() < 1500,
        "R2B_FD_SEND_TIMEOUT_BOUND");

    require(::close(fd) == 0, "R2B_FD_SEND_FD_CLOSE");
    require(::close(sockets[0]) == 0, "R2B_FD_SEND_CLOSE0");
    require(::close(sockets[1]) == 0, "R2B_FD_SEND_CLOSE1");
    std::printf("R2B_SCM_RIGHTS_SEND_DEADLINE=PASS\n");
}

} // namespace

int main() {
    test_wrong_uid_rejected();
    test_same_uid_transfer();
    test_bounded_fd_receive_timeout();
    test_bounded_fd_send_timeout();
    std::printf("STATUS=PASS\n");
    return 0;
}
