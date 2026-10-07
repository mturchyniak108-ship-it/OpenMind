#ifndef _GNU_SOURCE
#define _GNU_SOURCE 1
#endif

#include "openmind/unix_fd_transport.hpp"

#include <array>
#include <cerrno>
#include <chrono>
#include <climits>
#include <cstring>
#include <fcntl.h>
#include <poll.h>
#include <sys/socket.h>
#include <unistd.h>

namespace openmind::secure_memory {
namespace {

constexpr unsigned char kMarker = 0x4fU;

enum class WaitResult {
    ready,
    timed_out,
    failed,
};

bool valid_socket(int socket_fd) noexcept {
    return socket_fd >= 0;
}

bool valid_fd(int fd) noexcept {
    return fd >= 0;
}

WaitResult wait_until(
    int fd,
    short events,
    IoDeadline deadline) noexcept {
    for (;;) {
        const auto now = std::chrono::steady_clock::now();
        if (now >= deadline) {
            return WaitResult::timed_out;
        }

        auto remaining =
            std::chrono::duration_cast<std::chrono::milliseconds>(
                deadline - now).count();
        if (remaining <= 0) {
            remaining = 1;
        }
        if (remaining > INT_MAX) {
            remaining = INT_MAX;
        }

        pollfd item{fd, events, 0};
        const int rc = ::poll(
            &item,
            1,
            static_cast<int>(remaining));
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

TransportError send_fd_impl(
    int socket_fd,
    int fd,
    uid_t expected_peer_uid,
    const IoDeadline* deadline) noexcept {
    if (!valid_socket(socket_fd) || !valid_fd(fd)) {
        return TransportError::invalid_argument;
    }

    const auto peer = query_peer_credentials(socket_fd);
    if (peer.second != TransportError::ok) {
        return peer.second;
    }
    if (peer.first.uid != expected_peer_uid) {
        return TransportError::peer_uid_mismatch;
    }

    unsigned char marker = kMarker;
    iovec iov{};
    iov.iov_base = &marker;
    iov.iov_len = 1U;

    alignas(cmsghdr)
        std::array<unsigned char, CMSG_SPACE(sizeof(int))> control{};

    msghdr message{};
    message.msg_iov = &iov;
    message.msg_iovlen = 1U;
    message.msg_control = control.data();
    message.msg_controllen = control.size();

    cmsghdr* cmsg = CMSG_FIRSTHDR(&message);
    if (cmsg == nullptr) {
        return TransportError::protocol_error;
    }
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));
    std::memcpy(CMSG_DATA(cmsg), &fd, sizeof(fd));

    for (;;) {
        if (deadline != nullptr &&
            std::chrono::steady_clock::now() >= *deadline) {
            return TransportError::timed_out;
        }

        const int flags =
            MSG_NOSIGNAL |
            (deadline != nullptr ? MSG_DONTWAIT : 0);
        const ssize_t result =
            ::sendmsg(socket_fd, &message, flags);

        if (result == 1) {
            return TransportError::ok;
        }
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (deadline != nullptr &&
            result < 0 &&
            (errno == EAGAIN || errno == EWOULDBLOCK)) {
            const WaitResult waited =
                wait_until(socket_fd, POLLOUT, *deadline);
            if (waited == WaitResult::timed_out) {
                return TransportError::timed_out;
            }
            if (waited == WaitResult::failed) {
                return TransportError::send_failed;
            }
            continue;
        }
        return TransportError::send_failed;
    }
}

std::pair<int, TransportError> receive_fd_impl(
    int socket_fd,
    uid_t expected_peer_uid,
    const IoDeadline* deadline) noexcept {
    if (!valid_socket(socket_fd)) {
        return {-1, TransportError::invalid_argument};
    }

    const auto peer = query_peer_credentials(socket_fd);
    if (peer.second != TransportError::ok) {
        return {-1, peer.second};
    }
    if (peer.first.uid != expected_peer_uid) {
        return {-1, TransportError::peer_uid_mismatch};
    }

    unsigned char marker = 0U;
    iovec iov{};
    iov.iov_base = &marker;
    iov.iov_len = 1U;

    constexpr std::size_t kMaxReceivedFds = 4U;
    alignas(cmsghdr)
        std::array<
            unsigned char,
            CMSG_SPACE(sizeof(int) * kMaxReceivedFds)> control{};

    msghdr message{};
    message.msg_iov = &iov;
    message.msg_iovlen = 1U;
    message.msg_control = control.data();
    message.msg_controllen = control.size();

    ssize_t result = -1;
    for (;;) {
        if (deadline != nullptr &&
            std::chrono::steady_clock::now() >= *deadline) {
            return {-1, TransportError::timed_out};
        }

        const int flags =
            MSG_CMSG_CLOEXEC |
            (deadline != nullptr ? MSG_DONTWAIT : 0);
        result = ::recvmsg(socket_fd, &message, flags);
        if (result >= 0) {
            break;
        }
        if (errno == EINTR) {
            continue;
        }
        if (deadline != nullptr &&
            (errno == EAGAIN || errno == EWOULDBLOCK)) {
            const WaitResult waited =
                wait_until(socket_fd, POLLIN, *deadline);
            if (waited == WaitResult::timed_out) {
                return {-1, TransportError::timed_out};
            }
            if (waited == WaitResult::failed) {
                return {-1, TransportError::receive_failed};
            }
            continue;
        }
        return {-1, TransportError::receive_failed};
    }

    std::array<int, kMaxReceivedFds> received_fds{};
    received_fds.fill(-1);
    std::size_t received_count = 0U;
    bool control_valid = true;

    for (cmsghdr* cmsg = CMSG_FIRSTHDR(&message);
         cmsg != nullptr;
         cmsg = CMSG_NXTHDR(&message, cmsg)) {
        if (cmsg->cmsg_level != SOL_SOCKET ||
            cmsg->cmsg_type != SCM_RIGHTS) {
            control_valid = false;
            continue;
        }
        if (cmsg->cmsg_len < CMSG_LEN(0)) {
            control_valid = false;
            continue;
        }
        const std::size_t bytes =
            static_cast<std::size_t>(
                cmsg->cmsg_len - CMSG_LEN(0));
        if (bytes == 0U || bytes % sizeof(int) != 0U) {
            control_valid = false;
            continue;
        }
        const std::size_t count = bytes / sizeof(int);
        if (count > kMaxReceivedFds - received_count) {
            control_valid = false;
            continue;
        }
        const unsigned char* data =
            static_cast<const unsigned char*>(
                CMSG_DATA(cmsg));
        for (std::size_t index = 0; index < count; ++index) {
            std::memcpy(
                &received_fds[received_count],
                data + index * sizeof(int),
                sizeof(int));
            ++received_count;
        }
    }

    const bool message_valid =
        result == 1 &&
        marker == kMarker &&
        (message.msg_flags & (MSG_CTRUNC | MSG_TRUNC)) == 0 &&
        control_valid &&
        received_count == 1U;

    if (!message_valid) {
        for (std::size_t index = 0;
             index < received_count;
             ++index) {
            if (received_fds[index] >= 0) {
                ::close(received_fds[index]);
            }
        }
        return {
            -1,
            result == 1
                ? TransportError::protocol_error
                : TransportError::receive_failed};
    }

    const int received_fd = received_fds[0];

    const int verified_flags =
        ::fcntl(received_fd, F_GETFD);
    if (verified_flags < 0 ||
        (verified_flags & FD_CLOEXEC) == 0) {
        ::close(received_fd);
        return {-1, TransportError::cloexec_failed};
    }

    return {received_fd, TransportError::ok};
}

} // namespace

std::pair<PeerCredentials, TransportError> query_peer_credentials(
    int socket_fd) noexcept {
    if (!valid_socket(socket_fd)) {
        return {
            PeerCredentials{},
            TransportError::invalid_argument};
    }

    ucred credentials{};
    socklen_t length =
        static_cast<socklen_t>(sizeof(credentials));
    if (::getsockopt(
            socket_fd,
            SOL_SOCKET,
            SO_PEERCRED,
            &credentials,
            &length) != 0 ||
        length != sizeof(credentials)) {
        return {
            PeerCredentials{},
            TransportError::peer_query_failed};
    }

    PeerCredentials result{};
    result.pid = credentials.pid;
    result.uid = credentials.uid;
    result.gid = credentials.gid;
    return {result, TransportError::ok};
}

TransportError send_fd_to_uid(
    int socket_fd,
    int fd,
    uid_t expected_peer_uid) noexcept {
    return send_fd_impl(
        socket_fd,
        fd,
        expected_peer_uid,
        nullptr);
}

std::pair<int, TransportError> receive_fd_from_uid(
    int socket_fd,
    uid_t expected_peer_uid) noexcept {
    return receive_fd_impl(
        socket_fd,
        expected_peer_uid,
        nullptr);
}

TransportError send_fd_to_uid_until(
    int socket_fd,
    int fd,
    uid_t expected_peer_uid,
    IoDeadline deadline) noexcept {
    return send_fd_impl(
        socket_fd,
        fd,
        expected_peer_uid,
        &deadline);
}

std::pair<int, TransportError> receive_fd_from_uid_until(
    int socket_fd,
    uid_t expected_peer_uid,
    IoDeadline deadline) noexcept {
    return receive_fd_impl(
        socket_fd,
        expected_peer_uid,
        &deadline);
}

} // namespace openmind::secure_memory
