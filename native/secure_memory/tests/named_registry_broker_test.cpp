#include "openmind/named_registry_broker.hpp"

#include <array>
#include <chrono>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

namespace {

constexpr std::size_t kSize = 4096U;
constexpr int kRequestCount = 7;

[[noreturn]] void fail(const char* gate) {
    std::fprintf(stderr, "FAIL=%s errno=%d (%s)\n", gate, errno, std::strerror(errno));
    std::exit(2);
}

void require(bool condition, const char* gate) {
    if (!condition) {
        fail(gate);
    }
}

void child_require(bool condition, int code) {
    if (!condition) {
        _exit(code);
    }
}

void receive_exact_child(int fd, unsigned char* data, std::size_t size, int code) {
    std::size_t offset = 0U;
    while (offset < size) {
        const ssize_t rc = ::recv(fd, data + offset, size - offset, 0);
        if (rc < 0 && errno == EINTR) {
            continue;
        }
        child_require(rc > 0, code);
        offset += static_cast<std::size_t>(rc);
    }
}

void send_exact_child(
    int fd,
    const unsigned char* data,
    std::size_t size,
    int code) {
    std::size_t offset = 0U;
    while (offset < size) {
        const ssize_t rc = ::send(fd, data + offset, size - offset, MSG_NOSIGNAL);
        if (rc < 0 && errno == EINTR) {
            continue;
        }
        child_require(rc > 0, code);
        offset += static_cast<std::size_t>(rc);
    }
}

[[noreturn]] void fake_response_peer(int fd, unsigned char has_fd, int base_code) {
    std::array<unsigned char, 20> request{};
    receive_exact_child(fd, request.data(), request.size(), base_code);
    const std::size_t name_size =
        static_cast<std::size_t>(request[16]) |
        (static_cast<std::size_t>(request[17]) << 8U);
    child_require(name_size > 0U && name_size <= 255U, base_code + 1);
    std::array<unsigned char, 255> name{};
    receive_exact_child(fd, name.data(), name_size, base_code + 2);

    const std::array<unsigned char, 8> response{{
        'O', 'M', 'S', 'H', 1U, 0U, has_fd, 0U}};
    send_exact_child(fd, response.data(), response.size(), base_code + 3);
    ::close(fd);
    _exit(0);
}

void wait_clean(pid_t child, const char* gate) {
    int status = 0;
    require(::waitpid(child, &status, 0) == child, gate);
    require(WIFEXITED(status) && WEXITSTATUS(status) == 0, gate);
}

void test_response_fd_flag_validation(uid_t uid) {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::RegistryError;
    using openmind::secure_memory::RegistryOpenOptions;
    using openmind::secure_memory::broker_open;
    using openmind::secure_memory::broker_unlink;

    int open_sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, open_sockets) == 0,
        "FD_FLAG_OPEN_SOCKETPAIR");
    const pid_t open_child = ::fork();
    require(open_child >= 0, "FD_FLAG_OPEN_FORK");
    if (open_child == 0) {
        ::close(open_sockets[0]);
        fake_response_peer(open_sockets[1], 0U, 40);
    }
    ::close(open_sockets[1]);
    const auto open_result = broker_open(
        open_sockets[0],
        "/bad-open",
        RegistryOpenOptions{},
        uid);
    require(
        open_result.fd < 0 &&
            open_result.broker_error == BrokerError::protocol_error &&
            open_result.registry_error == RegistryError::ok,
        "FD_FLAG_OPEN_REJECTED");
    require(::close(open_sockets[0]) == 0, "FD_FLAG_OPEN_CLOSE");
    wait_clean(open_child, "FD_FLAG_OPEN_CHILD");

    int unlink_sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, unlink_sockets) == 0,
        "FD_FLAG_UNLINK_SOCKETPAIR");
    const pid_t unlink_child = ::fork();
    require(unlink_child >= 0, "FD_FLAG_UNLINK_FORK");
    if (unlink_child == 0) {
        ::close(unlink_sockets[0]);
        fake_response_peer(unlink_sockets[1], 1U, 50);
    }
    ::close(unlink_sockets[1]);
    const auto unlink_result = broker_unlink(unlink_sockets[0], "/bad-unlink", uid);
    require(
        unlink_result.broker_error == BrokerError::protocol_error &&
            unlink_result.registry_error == RegistryError::ok,
        "FD_FLAG_UNLINK_REJECTED");
    require(::close(unlink_sockets[0]) == 0, "FD_FLAG_UNLINK_CLOSE");
    wait_clean(unlink_child, "FD_FLAG_UNLINK_CHILD");

    std::printf("P3E_RESPONSE_FD_FLAG_VALIDATION=PASS\n");
}


void test_bounded_partial_header_timeout(uid_t uid) {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::NamedRegistry;
    using openmind::secure_memory::serve_registry_request_once_until;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "R2B_PARTIAL_SOCKETPAIR");

    const unsigned char byte = 'O';
    require(
        ::send(sockets[0], &byte, 1U, MSG_NOSIGNAL) == 1,
        "R2B_PARTIAL_SEND");

    NamedRegistry registry;
    const auto start = std::chrono::steady_clock::now();
    const BrokerError result =
        serve_registry_request_once_until(
            sockets[1],
            registry,
            uid,
            start + std::chrono::milliseconds(120));
    const auto elapsed =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now() - start);

    require(
        result == BrokerError::timed_out,
        "R2B_PARTIAL_TIMEOUT_RESULT");
    require(
        elapsed.count() >= 50 &&
            elapsed.count() < 1500,
        "R2B_PARTIAL_TIMEOUT_BOUND");

    require(::close(sockets[0]) == 0, "R2B_PARTIAL_CLOSE0");
    require(::close(sockets[1]) == 0, "R2B_PARTIAL_CLOSE1");
    std::printf("R2B_ABSOLUTE_REQUEST_DEADLINE=PASS\n");
}

void test_slow_drip_total_deadline(uid_t uid) {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::NamedRegistry;
    using openmind::secure_memory::serve_registry_request_once_until;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "R2B_DRIP_SOCKETPAIR");

    const pid_t child = ::fork();
    require(child >= 0, "R2B_DRIP_FORK");
    if (child == 0) {
        ::close(sockets[1]);
        const unsigned char byte = 'O';
        for (int index = 0; index < 6; ++index) {
            const ssize_t rc =
                ::send(sockets[0], &byte, 1U, MSG_NOSIGNAL);
            if (rc == 1) {
                ::usleep(40000);
                continue;
            }
            if (rc < 0 &&
                (errno == EPIPE ||
                 errno == ECONNRESET ||
                 errno == ENOTCONN ||
                 errno == EAGAIN ||
                 errno == EWOULDBLOCK)) {
                ::close(sockets[0]);
                _exit(0);
            }
            _exit(71);
        }
        ::close(sockets[0]);
        _exit(0);
    }

    ::close(sockets[0]);
    NamedRegistry registry;
    const auto start = std::chrono::steady_clock::now();
    const BrokerError result =
        serve_registry_request_once_until(
            sockets[1],
            registry,
            uid,
            start + std::chrono::milliseconds(120));
    const auto elapsed =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now() - start);

    require(
        result == BrokerError::timed_out,
        "R2B_DRIP_TIMEOUT_RESULT");
    require(
        elapsed.count() >= 50 &&
            elapsed.count() < 1500,
        "R2B_DRIP_TIMEOUT_BOUND");

    require(::close(sockets[1]) == 0, "R2B_DRIP_CLOSE");
    wait_clean(child, "R2B_DRIP_CHILD");
    std::printf("R2B_SLOW_DRIP_TOTAL_DEADLINE=PASS\n");
}

void test_promised_fd_stall_deadline(uid_t uid) {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::RegistryError;
    using openmind::secure_memory::RegistryOpenOptions;
    using openmind::secure_memory::broker_open_until;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "R2B_PROMISED_FD_SOCKETPAIR");

    const pid_t child = ::fork();
    require(child >= 0, "R2B_PROMISED_FD_FORK");
    if (child == 0) {
        ::close(sockets[0]);

        std::array<unsigned char, 20> request{};
        receive_exact_child(
            sockets[1],
            request.data(),
            request.size(),
            81);
        const std::size_t name_size =
            static_cast<std::size_t>(request[16]) |
            (static_cast<std::size_t>(request[17]) << 8U);
        child_require(
            name_size > 0U && name_size <= 255U,
            82);
        std::array<unsigned char, 255> name{};
        receive_exact_child(
            sockets[1],
            name.data(),
            name_size,
            83);

        const std::array<unsigned char, 8> response{{
            'O', 'M', 'S', 'H', 1U, 0U, 1U, 0U}};
        send_exact_child(
            sockets[1],
            response.data(),
            response.size(),
            84);

        ::usleep(400000);
        ::close(sockets[1]);
        _exit(0);
    }

    ::close(sockets[1]);

    const auto result =
        broker_open_until(
            sockets[0],
            "/fd-stall",
            RegistryOpenOptions{},
            uid,
            std::chrono::steady_clock::now() +
                std::chrono::milliseconds(120));

    require(
        result.fd < 0 &&
            result.broker_error == BrokerError::timed_out &&
            result.registry_error == RegistryError::ok,
        "R2B_PROMISED_FD_TIMEOUT");

    require(
        ::close(sockets[0]) == 0,
        "R2B_PROMISED_FD_CLOSE");
    wait_clean(child, "R2B_PROMISED_FD_CHILD");
    std::printf("R2B_PROMISED_FD_STAGE_DEADLINE=PASS\n");
}

} // namespace

int main() {
    using openmind::secure_memory::BrokerError;
    using openmind::secure_memory::NamedRegistry;
    using openmind::secure_memory::RegistryError;
    using openmind::secure_memory::RegistryOpenOptions;
    using openmind::secure_memory::broker_open;
    using openmind::secure_memory::broker_unlink;
    using openmind::secure_memory::serve_registry_request_once;

    int sockets[2] = {-1, -1};
    require(
        ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) == 0,
        "SOCKETPAIR");

    const uid_t uid = ::getuid();
    const pid_t child = ::fork();
    require(child >= 0, "FORK");

    if (child == 0) {
        ::close(sockets[0]);
        NamedRegistry registry;
        for (int index = 0; index < kRequestCount; ++index) {
            if (serve_registry_request_once(sockets[1], registry, uid) !=
                BrokerError::ok) {
                ::close(sockets[1]);
                _exit(10 + index);
            }
        }
        ::close(sockets[1]);
        _exit(0);
    }

    ::close(sockets[1]);

    auto created = broker_open(
        sockets[0],
        "/broker",
        RegistryOpenOptions{true, true, 0U},
        uid);
    require(
        created.fd >= 0 &&
            created.broker_error == BrokerError::ok &&
            created.registry_error == RegistryError::ok,
        "BROKER_CREATE");

    struct stat initial_stat {};
    require(::fstat(created.fd, &initial_stat) == 0, "CREATE_FSTAT");
    require(initial_stat.st_size == 0, "CREATE_ZERO_LENGTH");
    require(
        (::fcntl(created.fd, F_GETFD) & FD_CLOEXEC) != 0,
        "CREATE_CLOEXEC");
    std::printf("P3E_BROKER_CREATE_ZERO_LENGTH=PASS\n");

    require(
        ::ftruncate(created.fd, static_cast<off_t>(kSize)) == 0,
        "CALLER_FTRUNCATE");
    void* writer = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        created.fd,
        0);
    require(writer != MAP_FAILED, "WRITER_MAP");
    std::memcpy(writer, "BROKER", 6U);

    auto reopened = broker_open(
        sockets[0],
        "/broker",
        RegistryOpenOptions{},
        uid);
    require(
        reopened.fd >= 0 &&
            reopened.broker_error == BrokerError::ok &&
            reopened.registry_error == RegistryError::ok,
        "BROKER_REOPEN");

    struct stat reopened_stat {};
    require(::fstat(reopened.fd, &reopened_stat) == 0, "REOPEN_FSTAT");
    require(
        reopened_stat.st_size == static_cast<off_t>(kSize),
        "REOPEN_SEES_RESIZE");
    void* reader = ::mmap(
        nullptr,
        kSize,
        PROT_READ,
        MAP_SHARED,
        reopened.fd,
        0);
    require(reader != MAP_FAILED, "READER_MAP");
    require(std::memcmp(reader, "BROKER", 6U) == 0, "REOPEN_CONTENT");
    std::printf("P3E_BROKER_REOPEN_SHARED_OBJECT=PASS\n");

    auto duplicate = broker_open(
        sockets[0],
        "/broker",
        RegistryOpenOptions{true, true, 0U},
        uid);
    require(
        duplicate.fd < 0 &&
            duplicate.broker_error == BrokerError::ok &&
            duplicate.registry_error == RegistryError::already_exists,
        "BROKER_CREATE_EXCLUSIVE");

    auto unlinked = broker_unlink(sockets[0], "/broker", uid);
    require(
        unlinked.broker_error == BrokerError::ok &&
            unlinked.registry_error == RegistryError::ok,
        "BROKER_UNLINK");

    auto missing = broker_open(
        sockets[0],
        "/broker",
        RegistryOpenOptions{},
        uid);
    require(
        missing.fd < 0 &&
            missing.broker_error == BrokerError::ok &&
            missing.registry_error == RegistryError::not_found,
        "BROKER_OPEN_AFTER_UNLINK");
    require(std::memcmp(reader, "BROKER", 6U) == 0, "LIVE_MAP_SURVIVES_UNLINK");
    std::printf("P3E_BROKER_UNLINK_LIVE_FD_SURVIVES=PASS\n");

    auto recreated = broker_open(
        sockets[0],
        "/broker",
        RegistryOpenOptions{true, true, 0U},
        uid);
    require(
        recreated.fd >= 0 &&
            recreated.broker_error == BrokerError::ok &&
            recreated.registry_error == RegistryError::ok,
        "BROKER_RECREATE");

    struct stat recreated_stat {};
    require(::fstat(recreated.fd, &recreated_stat) == 0, "RECREATE_FSTAT");
    require(recreated_stat.st_size == 0, "RECREATE_ZERO_LENGTH");
    require(
        initial_stat.st_dev != recreated_stat.st_dev ||
            initial_stat.st_ino != recreated_stat.st_ino,
        "RECREATE_DISTINCT_OBJECT");

    auto final_unlink = broker_unlink(sockets[0], "/broker", uid);
    require(
        final_unlink.broker_error == BrokerError::ok &&
            final_unlink.registry_error == RegistryError::ok,
        "BROKER_FINAL_UNLINK");

    require(::munmap(reader, kSize) == 0, "READER_UNMAP");
    require(::munmap(writer, kSize) == 0, "WRITER_UNMAP");
    require(::close(recreated.fd) == 0, "RECREATE_CLOSE");
    require(::close(reopened.fd) == 0, "REOPEN_CLOSE");
    require(::close(created.fd) == 0, "CREATE_CLOSE");
    require(::close(sockets[0]) == 0, "SOCKET_CLOSE");

    int status = 0;
    require(::waitpid(child, &status, 0) == child, "WAITPID");
    require(WIFEXITED(status) && WEXITSTATUS(status) == 0, "BROKER_CHILD_STATUS");

    std::printf("P3E_SAME_UID_CROSS_PROCESS_NAMESPACE=PASS\n");
    test_response_fd_flag_validation(uid);
    test_bounded_partial_header_timeout(uid);
    test_slow_drip_total_deadline(uid);
    test_promised_fd_stall_deadline(uid);

    {
        int nul_sockets[2] = {-1, -1};
        require(
            ::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, nul_sockets) == 0,
            "R2C_NUL_SOCKETPAIR");
        const pid_t nul_child = ::fork();
        require(nul_child >= 0, "R2C_NUL_FORK");
        if (nul_child == 0) {
            ::close(nul_sockets[0]);
            NamedRegistry nul_registry;
            const auto served =
                serve_registry_request_once(nul_sockets[1], nul_registry, uid);
            ::close(nul_sockets[1]);
            _exit(served == BrokerError::ok ? 0 : 91);
        }
        ::close(nul_sockets[1]);

        const std::string nul_name("/a\0b", 4U);
        const auto nul_result =
            broker_open(
                nul_sockets[0],
                std::string_view(nul_name.data(), nul_name.size()),
                RegistryOpenOptions{true, true, 0U},
                uid);
        require(
            nul_result.fd < 0 &&
                nul_result.broker_error == BrokerError::ok &&
                nul_result.registry_error == RegistryError::invalid_name,
            "R2C_BROKER_NUL_REJECTED");
        require(::close(nul_sockets[0]) == 0, "R2C_NUL_PARENT_CLOSE");
        wait_clean(nul_child, "R2C_NUL_CHILD");
        std::printf("R2C_BROKER_EMBEDDED_NUL_REJECTED=PASS\n");
    }
    std::printf("STATUS=PASS\n");
    return 0;
}
