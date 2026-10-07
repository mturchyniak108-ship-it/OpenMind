#pragma once

#include "openmind/named_registry.hpp"

#include <chrono>
#include <string>
#include <string_view>
#include <sys/types.h>
#include <utility>

namespace openmind::secure_memory {

enum class EndpointError {
    ok,
    invalid_argument,
    path_too_long,
    parent_stat_failed,
    parent_not_directory,
    parent_owner_mismatch,
    parent_permissions_insecure,
    parent_identity_changed,
    lock_open_failed,
    lock_unsafe,
    lock_busy,
    socket_create_failed,
    endpoint_exists,
    bind_failed,
    chmod_failed,
    listen_failed,
    accept_failed,
    connect_failed,
    peer_auth_failed,
    broker_failed,
    stale_endpoint_unsafe,
    stale_recovery_deferred,
    endpoint_live,
    timed_out,
    cleanup_failed,
};

class RegistryEndpointListener {
public:
    RegistryEndpointListener() noexcept = default;
    ~RegistryEndpointListener();

    RegistryEndpointListener(const RegistryEndpointListener&) = delete;
    RegistryEndpointListener& operator=(const RegistryEndpointListener&) = delete;
    RegistryEndpointListener(RegistryEndpointListener&& other) noexcept;
    RegistryEndpointListener& operator=(RegistryEndpointListener&& other) = delete;

    static std::pair<RegistryEndpointListener, EndpointError> create(
        std::string_view path,
        uid_t expected_uid,
        int backlog = 8);

    int native_handle() const noexcept;

    EndpointError serve_once(
        NamedRegistry& registry,
        uid_t expected_peer_uid) noexcept;

    EndpointError serve_once_bounded(
        NamedRegistry& registry,
        uid_t expected_peer_uid,
        std::chrono::milliseconds timeout) noexcept;

    EndpointError close_and_unlink() noexcept;

private:
    RegistryEndpointListener(
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
        pid_t creator_pid) noexcept;

    int fd_ = -1;
    int parent_fd_ = -1;
    int lock_fd_ = -1;
    std::string path_;
    std::string canonical_parent_;
    dev_t parent_device_ = 0;
    ino_t parent_inode_ = 0;
    dev_t path_device_ = 0;
    ino_t path_inode_ = 0;
    uid_t path_uid_ = static_cast<uid_t>(-1);
    pid_t creator_pid_ = -1;
};

std::pair<int, EndpointError> connect_registry_endpoint(
    std::string_view path,
    uid_t expected_server_uid);

std::pair<int, EndpointError> connect_registry_endpoint_bounded(
    std::string_view path,
    uid_t expected_server_uid,
    std::chrono::milliseconds timeout);

EndpointError remove_stale_registry_endpoint(
    std::string_view path,
    uid_t expected_uid);

EndpointError remove_stale_registry_endpoint_bounded(
    std::string_view path,
    uid_t expected_uid,
    std::chrono::milliseconds timeout);

} // namespace openmind::secure_memory
