#include "openmind/named_registry.hpp"

#ifndef _GNU_SOURCE
#define _GNU_SOURCE 1
#endif

#include <cerrno>
#include <fcntl.h>
#include <limits>
#include <linux/memfd.h>
#include <new>
#include <sys/syscall.h>
#include <unistd.h>

#ifndef MFD_NOEXEC_SEAL
#define MFD_NOEXEC_SEAL 0x0008U
#endif

namespace openmind::secure_memory {
namespace {

std::pair<int, RegistryError> create_master_fd(std::size_t initial_size) noexcept {
#if defined(SYS_memfd_create)
    const long raw_fd = ::syscall(
        SYS_memfd_create,
        "openmind-named-shm",
        MFD_CLOEXEC | MFD_ALLOW_SEALING | MFD_NOEXEC_SEAL);
    if (raw_fd < 0 || raw_fd > std::numeric_limits<int>::max()) {
        return {-1, RegistryError::create_failed};
    }
    const int fd = static_cast<int>(raw_fd);
    if (initial_size != 0U) {
        if (initial_size > static_cast<std::size_t>(std::numeric_limits<off_t>::max()) ||
            ::ftruncate(fd, static_cast<off_t>(initial_size)) != 0) {
            ::close(fd);
            return {-1, RegistryError::create_failed};
        }
    }
    return {fd, RegistryError::ok};
#else
    (void)initial_size;
    return {-1, RegistryError::create_failed};
#endif
}

} // namespace

NamedRegistry::~NamedRegistry() {
    for (auto& entry : entries_) {
        if (entry.second >= 0) {
            ::close(entry.second);
        }
    }
}

bool NamedRegistry::valid_name(std::string_view name) noexcept {
    if (name.size() < 2U || name.size() > 255U || name.front() != '/' ||
        name.find('\0') != std::string_view::npos) {
        return false;
    }
    return name.find('/', 1U) == std::string_view::npos;
}

std::pair<int, RegistryError> NamedRegistry::duplicate_cloexec(int fd) noexcept {
    if (fd < 0) {
        return {-1, RegistryError::duplicate_failed};
    }
    const int duplicate = ::fcntl(fd, F_DUPFD_CLOEXEC, 0);
    if (duplicate < 0) {
        return {-1, RegistryError::duplicate_failed};
    }
    return {duplicate, RegistryError::ok};
}

std::pair<int, RegistryError> NamedRegistry::open(
    std::string_view name,
    RegistryOpenOptions options) {
    if (!valid_name(name)) {
        return {-1, RegistryError::invalid_name};
    }
    if (!options.create && options.exclusive) {
        return {-1, RegistryError::invalid_argument};
    }

    std::lock_guard<std::mutex> lock(mutex_);

    try {
        const std::string key(name);
        const auto found = entries_.find(key);
        if (found != entries_.end()) {
            if (options.create && options.exclusive) {
                return {-1, RegistryError::already_exists};
            }
            return duplicate_cloexec(found->second);
        }

        if (!options.create) {
            return {-1, RegistryError::not_found};
        }

        if (entries_.size() >= max_linked_entries_) {
            return {-1, RegistryError::resource_exhausted};
        }

        auto master = create_master_fd(options.size);
        if (master.second != RegistryError::ok) {
            return master;
        }

        int pending_master = master.first;
        try {
            const auto inserted = entries_.emplace(key, pending_master);
            if (!inserted.second) {
                ::close(pending_master);
                return {-1, RegistryError::already_exists};
            }
            pending_master = -1;

            auto client = duplicate_cloexec(inserted.first->second);
            if (client.second != RegistryError::ok) {
                ::close(inserted.first->second);
                entries_.erase(inserted.first);
                return client;
            }
            return client;
        } catch (const std::bad_alloc&) {
            if (pending_master >= 0) {
                ::close(pending_master);
            }
            return {-1, RegistryError::resource_exhausted};
        }
    } catch (const std::bad_alloc&) {
        return {-1, RegistryError::resource_exhausted};
    }
}

RegistryError NamedRegistry::unlink_name(std::string_view name) {
    if (!valid_name(name)) {
        return RegistryError::invalid_name;
    }

    std::lock_guard<std::mutex> lock(mutex_);
    try {
        const std::string key(name);
        const auto found = entries_.find(key);
        if (found == entries_.end()) {
            return RegistryError::not_found;
        }

        const int master_fd = found->second;
        entries_.erase(found);
        if (master_fd >= 0 && ::close(master_fd) != 0) {
            return RegistryError::close_failed;
        }
        return RegistryError::ok;
    } catch (const std::bad_alloc&) {
        return RegistryError::resource_exhausted;
    }
}

bool NamedRegistry::contains(std::string_view name) const {
    if (!valid_name(name)) {
        return false;
    }
    std::lock_guard<std::mutex> lock(mutex_);
    try {
        return entries_.find(std::string(name)) != entries_.end();
    } catch (const std::bad_alloc&) {
        return false;
    }
}

std::size_t NamedRegistry::linked_count() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return entries_.size();
}

} // namespace openmind::secure_memory
