#pragma once

#include "openmind/named_registry.hpp"

#include <chrono>
#include <string_view>
#include <sys/types.h>

namespace openmind::secure_memory {

enum class BrokerError {
    ok,
    invalid_argument,
    peer_auth_failed,
    send_failed,
    receive_failed,
    protocol_error,
    fd_transfer_failed,
    timed_out,
};

struct BrokerOpenResult {
    int fd = -1;
    BrokerError broker_error = BrokerError::ok;
    RegistryError registry_error = RegistryError::ok;
};

struct BrokerStatusResult {
    BrokerError broker_error = BrokerError::ok;
    RegistryError registry_error = RegistryError::ok;
};

using BrokerDeadline =
    std::chrono::steady_clock::time_point;

BrokerError serve_registry_request_once(
    int socket_fd,
    NamedRegistry& registry,
    uid_t expected_peer_uid) noexcept;

BrokerOpenResult broker_open(
    int socket_fd,
    std::string_view name,
    RegistryOpenOptions options,
    uid_t expected_peer_uid) noexcept;

BrokerStatusResult broker_unlink(
    int socket_fd,
    std::string_view name,
    uid_t expected_peer_uid) noexcept;

BrokerError serve_registry_request_once_until(
    int socket_fd,
    NamedRegistry& registry,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept;

BrokerOpenResult broker_open_until(
    int socket_fd,
    std::string_view name,
    RegistryOpenOptions options,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept;

BrokerStatusResult broker_unlink_until(
    int socket_fd,
    std::string_view name,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept;

} // namespace openmind::secure_memory
