#pragma once

#include <cstddef>
#include <optional>
#include <utility>

namespace openmind::secure_memory {

enum class Backend {
    memfd,
    ashared_memory,
};

enum class Error {
    ok,
    invalid_argument,
    unsupported,
    create_failed,
    resize_failed,
    map_failed,
    publication_failed,
    verification_failed,
    duplicate_failed,
    state,
};

class Region final {
public:
    static std::pair<std::optional<Region>, Error> create_memfd(std::size_t size) noexcept;
    static std::pair<std::optional<Region>, Error> create_ashared_memory(std::size_t size) noexcept;

    Region(Region&& other) noexcept;
    Region& operator=(Region&& other) noexcept;
    ~Region();

    Region(const Region&) = delete;
    Region& operator=(const Region&) = delete;

    void* writable_data() noexcept { return writer_; }
    const void* writable_data() const noexcept { return writer_; }
    std::size_t size() const noexcept { return size_; }
    Backend backend() const noexcept { return backend_; }
    bool published() const noexcept { return published_; }
    bool finalized() const noexcept { return finalized_; }

    // Borrowed descriptor for native integration. Region retains ownership.
    int native_handle() const noexcept { return fd_; }

    // Publication is monotonic for future mappings/FD consumers while any
    // producer mapping created before publication remains usable.
    Error publish_read_only() noexcept;

    // Returns a CLOEXEC duplicate only after publication. The duplicate may
    // retain O_RDWR status flags, but the published kernel object prevents new
    // writable mappings and direct writes on the generic memfd backend.
    std::pair<int, Error> duplicate_for_transfer() const noexcept;

    // Closes the publication lifecycle. Generic memfd adds F_SEAL_SEAL;
    // ASharedMemory has no equivalent file-seal API, so its prior setProt()
    // restriction remains the final publication state.
    Error finalize_publication() noexcept;

private:
    Region(int fd, void* writer, std::size_t size, Backend backend) noexcept;
    void reset() noexcept;

    int fd_ = -1;
    void* writer_ = nullptr;
    std::size_t size_ = 0;
    Backend backend_ = Backend::memfd;
    bool published_ = false;
    bool finalized_ = false;
};

} // namespace openmind::secure_memory
