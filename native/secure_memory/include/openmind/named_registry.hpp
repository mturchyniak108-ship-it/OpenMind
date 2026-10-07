#pragma once

#include <cstddef>
#include <mutex>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>

namespace openmind::secure_memory {

enum class RegistryError {
    ok,
    invalid_name,
    invalid_argument,
    already_exists,
    not_found,
    create_failed,
    duplicate_failed,
    resource_exhausted,
    close_failed,
};

struct RegistryOpenOptions {
    bool create = false;
    bool exclusive = false;
    std::size_t size = 0;
};

// App-private named compatibility registry.
//
// Names are local compatibility identifiers only. They must not cross an
// Android trust boundary; transfer file descriptors across such boundaries.
//
// The registry owns one master descriptor per linked name. unlink_name()
// removes that namespace/master reference only. Duplicates already returned
// from open() remain valid until their individual owners close them.
class NamedRegistry final {
public:
    explicit NamedRegistry(std::size_t max_linked_entries = 256U) noexcept
        : max_linked_entries_(max_linked_entries) {}
    ~NamedRegistry();

    NamedRegistry(const NamedRegistry&) = delete;
    NamedRegistry& operator=(const NamedRegistry&) = delete;
    NamedRegistry(NamedRegistry&&) = delete;
    NamedRegistry& operator=(NamedRegistry&&) = delete;

    std::pair<int, RegistryError> open(
        std::string_view name,
        RegistryOpenOptions options);

    RegistryError unlink_name(std::string_view name);

    bool contains(std::string_view name) const;
    std::size_t linked_count() const;

private:
    static bool valid_name(std::string_view name) noexcept;
    static std::pair<int, RegistryError> duplicate_cloexec(int fd) noexcept;

    mutable std::mutex mutex_;
    std::unordered_map<std::string, int> entries_;
    std::size_t max_linked_entries_ = 256U;
};

} // namespace openmind::secure_memory
