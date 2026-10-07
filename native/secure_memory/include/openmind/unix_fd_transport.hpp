#pragma once

#include <chrono>
#include <sys/types.h>
#include <utility>

namespace openmind::secure_memory {

enum class TransportError {
    ok,
    invalid_argument,
    peer_query_failed,
    peer_uid_mismatch,
    send_failed,
    receive_failed,
    protocol_error,
    cloexec_failed,
    timed_out,
};

struct PeerCredentials {
    pid_t pid = -1;
    uid_t uid = static_cast<uid_t>(-1);
    gid_t gid = static_cast<gid_t>(-1);
};

using IoDeadline = std::chrono::steady_clock::time_point;

std::pair<PeerCredentials, TransportError> query_peer_credentials(
    int socket_fd) noexcept;

TransportError send_fd_to_uid(
    int socket_fd,
    int fd,
    uid_t expected_peer_uid) noexcept;

std::pair<int, TransportError> receive_fd_from_uid(
    int socket_fd,
    uid_t expected_peer_uid) noexcept;

TransportError send_fd_to_uid_until(
    int socket_fd,
    int fd,
    uid_t expected_peer_uid,
    IoDeadline deadline) noexcept;

std::pair<int, TransportError> receive_fd_from_uid_until(
    int socket_fd,
    uid_t expected_peer_uid,
    IoDeadline deadline) noexcept;

} // namespace openmind::secure_memory
