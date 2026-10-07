#include "openmind/named_registry_broker.hpp"

#include "openmind/unix_fd_transport.hpp"

#include <array>
#include <cerrno>
#include <chrono>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <poll.h>
#include <string_view>
#include <sys/socket.h>
#include <unistd.h>

namespace openmind::secure_memory {
namespace {

constexpr std::array<unsigned char, 4> kMagic{{'O', 'M', 'S', 'H'}};
constexpr unsigned char kVersion = 1U;
constexpr unsigned char kOpenOperation = 1U;
constexpr unsigned char kUnlinkOperation = 2U;
constexpr unsigned char kCreateFlag = 1U;
constexpr unsigned char kExclusiveFlag = 2U;
constexpr std::size_t kRequestSize = 20U;
constexpr std::size_t kResponseSize = 8U;
constexpr std::size_t kMaxNameSize = 255U;

enum class IoResult {
    ok,
    timed_out,
    failed,
};

bool same_magic(const unsigned char* data) noexcept {
    return data[0] == kMagic[0] &&
           data[1] == kMagic[1] &&
           data[2] == kMagic[2] &&
           data[3] == kMagic[3];
}

void put_u16(unsigned char* out, std::uint16_t value) noexcept {
    out[0] = static_cast<unsigned char>(value & 0xffU);
    out[1] = static_cast<unsigned char>((value >> 8U) & 0xffU);
}

std::uint16_t get_u16(const unsigned char* in) noexcept {
    return static_cast<std::uint16_t>(
        static_cast<std::uint16_t>(in[0]) |
        (static_cast<std::uint16_t>(in[1]) << 8U));
}

void put_u64(unsigned char* out, std::uint64_t value) noexcept {
    for (unsigned int index = 0U; index < 8U; ++index) {
        out[index] =
            static_cast<unsigned char>(
                (value >> (index * 8U)) & 0xffU);
    }
}

std::uint64_t get_u64(const unsigned char* in) noexcept {
    std::uint64_t value = 0U;
    for (unsigned int index = 0U; index < 8U; ++index) {
        value |=
            static_cast<std::uint64_t>(in[index])
            << (index * 8U);
    }
    return value;
}

IoResult wait_ready_until(
    int fd,
    short events,
    BrokerDeadline deadline) noexcept {
    for (;;) {
        const auto now = std::chrono::steady_clock::now();
        if (now >= deadline) {
            return IoResult::timed_out;
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
        const int rc =
            ::poll(&item, 1, static_cast<int>(remaining));
        if (rc < 0 && errno == EINTR) {
            continue;
        }
        if (rc == 0) {
            return IoResult::timed_out;
        }
        if (rc < 0) {
            return IoResult::failed;
        }
        if ((item.revents & events) != 0) {
            return IoResult::ok;
        }
        if ((item.revents & (POLLERR | POLLHUP | POLLNVAL)) != 0) {
            return IoResult::failed;
        }
    }
}

bool send_all(
    int socket_fd,
    const unsigned char* data,
    std::size_t size) noexcept {
    std::size_t offset = 0U;
    while (offset < size) {
        const ssize_t result =
            ::send(
                socket_fd,
                data + offset,
                size - offset,
                MSG_NOSIGNAL);
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result <= 0) {
            return false;
        }
        offset += static_cast<std::size_t>(result);
    }
    return true;
}

bool receive_all(
    int socket_fd,
    unsigned char* data,
    std::size_t size) noexcept {
    std::size_t offset = 0U;
    while (offset < size) {
        const ssize_t result =
            ::recv(
                socket_fd,
                data + offset,
                size - offset,
                0);
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result <= 0) {
            return false;
        }
        offset += static_cast<std::size_t>(result);
    }
    return true;
}

IoResult send_all_until(
    int socket_fd,
    const unsigned char* data,
    std::size_t size,
    BrokerDeadline deadline) noexcept {
    std::size_t offset = 0U;
    while (offset < size) {
        if (std::chrono::steady_clock::now() >= deadline) {
            return IoResult::timed_out;
        }
        const ssize_t result =
            ::send(
                socket_fd,
                data + offset,
                size - offset,
                MSG_NOSIGNAL | MSG_DONTWAIT);
        if (result > 0) {
            offset += static_cast<std::size_t>(result);
            continue;
        }
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result < 0 &&
            (errno == EAGAIN || errno == EWOULDBLOCK)) {
            const IoResult waited =
                wait_ready_until(socket_fd, POLLOUT, deadline);
            if (waited != IoResult::ok) {
                return waited;
            }
            continue;
        }
        return IoResult::failed;
    }
    return IoResult::ok;
}

IoResult receive_all_until(
    int socket_fd,
    unsigned char* data,
    std::size_t size,
    BrokerDeadline deadline) noexcept {
    std::size_t offset = 0U;
    while (offset < size) {
        if (std::chrono::steady_clock::now() >= deadline) {
            return IoResult::timed_out;
        }
        const ssize_t result =
            ::recv(
                socket_fd,
                data + offset,
                size - offset,
                MSG_DONTWAIT);
        if (result > 0) {
            offset += static_cast<std::size_t>(result);
            continue;
        }
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result < 0 &&
            (errno == EAGAIN || errno == EWOULDBLOCK)) {
            const IoResult waited =
                wait_ready_until(socket_fd, POLLIN, deadline);
            if (waited != IoResult::ok) {
                return waited;
            }
            continue;
        }
        return IoResult::failed;
    }
    return IoResult::ok;
}

BrokerError broker_error_from_io(
    IoResult result,
    bool sending) noexcept {
    if (result == IoResult::ok) {
        return BrokerError::ok;
    }
    if (result == IoResult::timed_out) {
        return BrokerError::timed_out;
    }
    return sending
        ? BrokerError::send_failed
        : BrokerError::receive_failed;
}

BrokerError authenticate_peer(
    int socket_fd,
    uid_t expected_uid) noexcept {
    const auto peer = query_peer_credentials(socket_fd);
    if (peer.second != TransportError::ok ||
        peer.first.uid != expected_uid) {
        return BrokerError::peer_auth_failed;
    }
    return BrokerError::ok;
}

bool encode_registry_error(RegistryError error, unsigned char& encoded) noexcept {
    switch (error) {
        case RegistryError::ok: encoded = 0U; return true;
        case RegistryError::invalid_name: encoded = 1U; return true;
        case RegistryError::invalid_argument: encoded = 2U; return true;
        case RegistryError::already_exists: encoded = 3U; return true;
        case RegistryError::not_found: encoded = 4U; return true;
        case RegistryError::create_failed: encoded = 5U; return true;
        case RegistryError::duplicate_failed: encoded = 6U; return true;
        case RegistryError::resource_exhausted: encoded = 7U; return true;
        case RegistryError::close_failed: encoded = 8U; return true;
    }
    return false;
}

bool decode_registry_error(unsigned char encoded, RegistryError& error) noexcept {
    switch (encoded) {
        case 0U: error = RegistryError::ok; return true;
        case 1U: error = RegistryError::invalid_name; return true;
        case 2U: error = RegistryError::invalid_argument; return true;
        case 3U: error = RegistryError::already_exists; return true;
        case 4U: error = RegistryError::not_found; return true;
        case 5U: error = RegistryError::create_failed; return true;
        case 6U: error = RegistryError::duplicate_failed; return true;
        case 7U: error = RegistryError::resource_exhausted; return true;
        case 8U: error = RegistryError::close_failed; return true;
        default: return false;
    }
}

BrokerError send_response_impl(
    int socket_fd,
    RegistryError registry_error,
    bool has_fd,
    const BrokerDeadline* deadline) noexcept {
    std::array<unsigned char, kResponseSize> response{};
    response[0] = kMagic[0];
    response[1] = kMagic[1];
    response[2] = kMagic[2];
    response[3] = kMagic[3];
    response[4] = kVersion;
    if (!encode_registry_error(registry_error, response[5])) {
        return BrokerError::protocol_error;
    }
    response[6] = has_fd ? 1U : 0U;
    response[7] = 0U;

    if (deadline == nullptr) {
        return send_all(socket_fd, response.data(), response.size())
            ? BrokerError::ok
            : BrokerError::send_failed;
    }
    return broker_error_from_io(
        send_all_until(
            socket_fd,
            response.data(),
            response.size(),
            *deadline),
        true);
}

BrokerStatusResult receive_response_impl(
    int socket_fd,
    bool& has_fd,
    const BrokerDeadline* deadline) noexcept {
    has_fd = false;
    std::array<unsigned char, kResponseSize> response{};

    if (deadline == nullptr) {
        if (!receive_all(socket_fd, response.data(), response.size())) {
            return {BrokerError::receive_failed, RegistryError::ok};
        }
    } else {
        const IoResult received =
            receive_all_until(
                socket_fd,
                response.data(),
                response.size(),
                *deadline);
        if (received != IoResult::ok) {
            return {
                broker_error_from_io(received, false),
                RegistryError::ok};
        }
    }

    if (!same_magic(response.data()) ||
        response[4] != kVersion ||
        response[7] != 0U ||
        response[6] > 1U) {
        return {BrokerError::protocol_error, RegistryError::ok};
    }
    RegistryError registry_error = RegistryError::ok;
    if (!decode_registry_error(response[5], registry_error)) {
        return {BrokerError::protocol_error, RegistryError::ok};
    }
    if (registry_error != RegistryError::ok && response[6] != 0U) {
        return {BrokerError::protocol_error, RegistryError::ok};
    }
    has_fd = response[6] == 1U;
    return {BrokerError::ok, registry_error};
}

BrokerError send_request_impl(
    int socket_fd,
    unsigned char operation,
    std::string_view name,
    RegistryOpenOptions options,
    const BrokerDeadline* deadline) noexcept {
    if (socket_fd < 0 || name.empty() || name.size() > kMaxNameSize) {
        return BrokerError::invalid_argument;
    }
    if (options.size > static_cast<std::size_t>(
            std::numeric_limits<std::uint64_t>::max())) {
        return BrokerError::invalid_argument;
    }

    std::array<unsigned char, kRequestSize> request{};
    request[0] = kMagic[0];
    request[1] = kMagic[1];
    request[2] = kMagic[2];
    request[3] = kMagic[3];
    request[4] = kVersion;
    request[5] = operation;
    request[6] =
        (options.create ? kCreateFlag : 0U) |
        (options.exclusive ? kExclusiveFlag : 0U);
    request[7] = 0U;
    put_u64(request.data() + 8U, static_cast<std::uint64_t>(options.size));
    put_u16(
        request.data() + 16U,
        static_cast<std::uint16_t>(name.size()));
    request[18] = 0U;
    request[19] = 0U;

    if (deadline == nullptr) {
        if (!send_all(socket_fd, request.data(), request.size()) ||
            !send_all(
                socket_fd,
                reinterpret_cast<const unsigned char*>(name.data()),
                name.size())) {
            return BrokerError::send_failed;
        }
        return BrokerError::ok;
    }

    IoResult sent =
        send_all_until(
            socket_fd,
            request.data(),
            request.size(),
            *deadline);
    if (sent != IoResult::ok) {
        return broker_error_from_io(sent, true);
    }
    sent =
        send_all_until(
            socket_fd,
            reinterpret_cast<const unsigned char*>(name.data()),
            name.size(),
            *deadline);
    return broker_error_from_io(sent, true);
}

BrokerError serve_request_impl(
    int socket_fd,
    NamedRegistry& registry,
    uid_t expected_peer_uid,
    const BrokerDeadline* deadline) noexcept {
    if (socket_fd < 0) {
        return BrokerError::invalid_argument;
    }
    const BrokerError auth =
        authenticate_peer(socket_fd, expected_peer_uid);
    if (auth != BrokerError::ok) {
        return auth;
    }

    std::array<unsigned char, kRequestSize> request{};
    if (deadline == nullptr) {
        if (!receive_all(socket_fd, request.data(), request.size())) {
            return BrokerError::receive_failed;
        }
    } else {
        const IoResult received =
            receive_all_until(
                socket_fd,
                request.data(),
                request.size(),
                *deadline);
        if (received != IoResult::ok) {
            return broker_error_from_io(received, false);
        }
    }

    if (!same_magic(request.data()) ||
        request[4] != kVersion ||
        request[7] != 0U ||
        request[18] != 0U ||
        request[19] != 0U) {
        return BrokerError::protocol_error;
    }

    const unsigned char operation = request[5];
    const unsigned char flags = request[6];
    if ((flags & ~(kCreateFlag | kExclusiveFlag)) != 0U) {
        return BrokerError::protocol_error;
    }
    const std::uint16_t name_size =
        get_u16(request.data() + 16U);
    if (name_size == 0U || name_size > kMaxNameSize) {
        return BrokerError::protocol_error;
    }

    std::array<char, kMaxNameSize> name{};
    if (deadline == nullptr) {
        if (!receive_all(
                socket_fd,
                reinterpret_cast<unsigned char*>(name.data()),
                name_size)) {
            return BrokerError::receive_failed;
        }
    } else {
        const IoResult received =
            receive_all_until(
                socket_fd,
                reinterpret_cast<unsigned char*>(name.data()),
                name_size,
                *deadline);
        if (received != IoResult::ok) {
            return broker_error_from_io(received, false);
        }
    }

    const std::string_view name_view(name.data(), name_size);

    if (operation == kOpenOperation) {
        const std::uint64_t size = get_u64(request.data() + 8U);
        if (size > static_cast<std::uint64_t>(
                std::numeric_limits<std::size_t>::max())) {
            return BrokerError::protocol_error;
        }
        RegistryOpenOptions options{};
        options.create = (flags & kCreateFlag) != 0U;
        options.exclusive = (flags & kExclusiveFlag) != 0U;
        options.size = static_cast<std::size_t>(size);

        auto opened = registry.open(name_view, options);
        if (opened.second != RegistryError::ok) {
            return send_response_impl(
                socket_fd,
                opened.second,
                false,
                deadline);
        }

        const BrokerError response =
            send_response_impl(
                socket_fd,
                RegistryError::ok,
                true,
                deadline);
        if (response != BrokerError::ok) {
            ::close(opened.first);
            return response;
        }

        const TransportError transfer =
            deadline == nullptr
                ? send_fd_to_uid(
                    socket_fd,
                    opened.first,
                    expected_peer_uid)
                : send_fd_to_uid_until(
                    socket_fd,
                    opened.first,
                    expected_peer_uid,
                    *deadline);
        ::close(opened.first);
        if (transfer == TransportError::timed_out) {
            return BrokerError::timed_out;
        }
        return transfer == TransportError::ok
            ? BrokerError::ok
            : BrokerError::fd_transfer_failed;
    }

    if (operation == kUnlinkOperation) {
        if (flags != 0U || get_u64(request.data() + 8U) != 0U) {
            return BrokerError::protocol_error;
        }
        const RegistryError result = registry.unlink_name(name_view);
        return send_response_impl(
            socket_fd,
            result,
            false,
            deadline);
    }

    return BrokerError::protocol_error;
}

BrokerOpenResult broker_open_impl(
    int socket_fd,
    std::string_view name,
    RegistryOpenOptions options,
    uid_t expected_peer_uid,
    const BrokerDeadline* deadline) noexcept {
    const BrokerError auth =
        authenticate_peer(socket_fd, expected_peer_uid);
    if (auth != BrokerError::ok) {
        return {-1, auth, RegistryError::ok};
    }
    const BrokerError sent =
        send_request_impl(
            socket_fd,
            kOpenOperation,
            name,
            options,
            deadline);
    if (sent != BrokerError::ok) {
        return {-1, sent, RegistryError::ok};
    }

    bool has_fd = false;
    const BrokerStatusResult response =
        receive_response_impl(
            socket_fd,
            has_fd,
            deadline);
    if (response.broker_error != BrokerError::ok) {
        return {-1, response.broker_error, RegistryError::ok};
    }
    if (response.registry_error != RegistryError::ok) {
        return {-1, BrokerError::ok, response.registry_error};
    }
    if (!has_fd) {
        return {-1, BrokerError::protocol_error, RegistryError::ok};
    }

    const auto received =
        deadline == nullptr
            ? receive_fd_from_uid(
                socket_fd,
                expected_peer_uid)
            : receive_fd_from_uid_until(
                socket_fd,
                expected_peer_uid,
                *deadline);
    if (received.second == TransportError::timed_out) {
        return {-1, BrokerError::timed_out, RegistryError::ok};
    }
    if (received.second != TransportError::ok) {
        return {-1, BrokerError::fd_transfer_failed, RegistryError::ok};
    }
    return {received.first, BrokerError::ok, RegistryError::ok};
}

BrokerStatusResult broker_unlink_impl(
    int socket_fd,
    std::string_view name,
    uid_t expected_peer_uid,
    const BrokerDeadline* deadline) noexcept {
    const BrokerError auth =
        authenticate_peer(socket_fd, expected_peer_uid);
    if (auth != BrokerError::ok) {
        return {auth, RegistryError::ok};
    }

    const BrokerError sent =
        send_request_impl(
            socket_fd,
            kUnlinkOperation,
            name,
            RegistryOpenOptions{},
            deadline);
    if (sent != BrokerError::ok) {
        return {sent, RegistryError::ok};
    }

    bool has_fd = false;
    const BrokerStatusResult response =
        receive_response_impl(
            socket_fd,
            has_fd,
            deadline);
    if (response.broker_error != BrokerError::ok) {
        return response;
    }
    if (has_fd) {
        return {BrokerError::protocol_error, RegistryError::ok};
    }
    return response;
}

} // namespace

BrokerError serve_registry_request_once(
    int socket_fd,
    NamedRegistry& registry,
    uid_t expected_peer_uid) noexcept {
    return serve_request_impl(
        socket_fd,
        registry,
        expected_peer_uid,
        nullptr);
}

BrokerOpenResult broker_open(
    int socket_fd,
    std::string_view name,
    RegistryOpenOptions options,
    uid_t expected_peer_uid) noexcept {
    return broker_open_impl(
        socket_fd,
        name,
        options,
        expected_peer_uid,
        nullptr);
}

BrokerStatusResult broker_unlink(
    int socket_fd,
    std::string_view name,
    uid_t expected_peer_uid) noexcept {
    return broker_unlink_impl(
        socket_fd,
        name,
        expected_peer_uid,
        nullptr);
}

BrokerError serve_registry_request_once_until(
    int socket_fd,
    NamedRegistry& registry,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept {
    return serve_request_impl(
        socket_fd,
        registry,
        expected_peer_uid,
        &deadline);
}

BrokerOpenResult broker_open_until(
    int socket_fd,
    std::string_view name,
    RegistryOpenOptions options,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept {
    return broker_open_impl(
        socket_fd,
        name,
        options,
        expected_peer_uid,
        &deadline);
}

BrokerStatusResult broker_unlink_until(
    int socket_fd,
    std::string_view name,
    uid_t expected_peer_uid,
    BrokerDeadline deadline) noexcept {
    return broker_unlink_impl(
        socket_fd,
        name,
        expected_peer_uid,
        &deadline);
}

} // namespace openmind::secure_memory
