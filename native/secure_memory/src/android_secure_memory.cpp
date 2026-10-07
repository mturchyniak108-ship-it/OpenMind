#ifndef _GNU_SOURCE
#define _GNU_SOURCE 1
#endif

#include "openmind/android_secure_memory.hpp"

#if defined(__ANDROID__)
#include <android/sharedmem.h>
#endif

#include <cerrno>
#include <cstdint>
#include <fcntl.h>
#include <limits>
#include <linux/memfd.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>

#ifndef F_ADD_SEALS
#define F_ADD_SEALS 1033
#endif
#ifndef F_GET_SEALS
#define F_GET_SEALS 1034
#endif
#ifndef F_SEAL_SEAL
#define F_SEAL_SEAL 0x0001
#endif
#ifndef F_SEAL_SHRINK
#define F_SEAL_SHRINK 0x0002
#endif
#ifndef F_SEAL_GROW
#define F_SEAL_GROW 0x0004
#endif
#ifndef F_SEAL_FUTURE_WRITE
#define F_SEAL_FUTURE_WRITE 0x0010
#endif
#ifndef F_SEAL_EXEC
#define F_SEAL_EXEC 0x0020
#endif
#ifndef MFD_NOEXEC_SEAL
#define MFD_NOEXEC_SEAL 0x0008U
#endif

namespace openmind::secure_memory {
namespace {

constexpr int kPublicationSeals =
    F_SEAL_FUTURE_WRITE | F_SEAL_GROW | F_SEAL_SHRINK;
constexpr int kRequiredPublishedSeals = kPublicationSeals | F_SEAL_EXEC;
constexpr int kRequiredFinalSeals = kRequiredPublishedSeals | F_SEAL_SEAL;

bool valid_size(std::size_t size) noexcept {
    if (size == 0) {
        return false;
    }
    using OffLimit = std::numeric_limits<off_t>;
    if constexpr (OffLimit::is_signed) {
        return size <= static_cast<std::size_t>(OffLimit::max());
    }
    return size <= OffLimit::max();
}



} // namespace

Region::Region(int fd, void* writer, std::size_t size, Backend backend) noexcept
    : fd_(fd), writer_(writer), size_(size), backend_(backend) {}

Region::Region(Region&& other) noexcept
    : fd_(other.fd_),
      writer_(other.writer_),
      size_(other.size_),
      backend_(other.backend_),
      published_(other.published_),
      finalized_(other.finalized_) {
    other.fd_ = -1;
    other.writer_ = nullptr;
    other.size_ = 0;
    other.published_ = false;
    other.finalized_ = false;
}

Region& Region::operator=(Region&& other) noexcept {
    if (this != &other) {
        reset();
        fd_ = other.fd_;
        writer_ = other.writer_;
        size_ = other.size_;
        backend_ = other.backend_;
        published_ = other.published_;
        finalized_ = other.finalized_;
        other.fd_ = -1;
        other.writer_ = nullptr;
        other.size_ = 0;
        other.published_ = false;
        other.finalized_ = false;
    }
    return *this;
}

Region::~Region() {
    reset();
}

void Region::reset() noexcept {
    if (writer_ != nullptr && size_ != 0) {
        ::munmap(writer_, size_);
    }
    if (fd_ >= 0) {
        ::close(fd_);
    }
    fd_ = -1;
    writer_ = nullptr;
    size_ = 0;
    published_ = false;
    finalized_ = false;
}

std::pair<std::optional<Region>, Error> Region::create_memfd(
    std::size_t size) noexcept {
    if (!valid_size(size)) {
        return {std::optional<Region>{}, Error::invalid_argument};
    }
#if defined(SYS_memfd_create)
    const long raw_fd = ::syscall(
        SYS_memfd_create,
        "openmind-secure-memory",
        MFD_CLOEXEC | MFD_ALLOW_SEALING | MFD_NOEXEC_SEAL);
    if (raw_fd < 0 || raw_fd > std::numeric_limits<int>::max()) {
        return {std::optional<Region>{}, Error::create_failed};
    }
    const int fd = static_cast<int>(raw_fd);
    if (::ftruncate(fd, static_cast<off_t>(size)) != 0) {
        ::close(fd);
        return {std::optional<Region>{}, Error::resize_failed};
    }
    void* writer = ::mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (writer == MAP_FAILED) {
        ::close(fd);
        return {std::optional<Region>{}, Error::map_failed};
    }
    return {std::optional<Region>(Region(fd, writer, size, Backend::memfd)), Error::ok};
#else
    (void)size;
    return {std::optional<Region>{}, Error::unsupported};
#endif
}

std::pair<std::optional<Region>, Error> Region::create_ashared_memory(
    std::size_t size) noexcept {
    if (!valid_size(size)) {
        return {std::optional<Region>{}, Error::invalid_argument};
    }
#if defined(__ANDROID__)
    const int fd = ::ASharedMemory_create(
        "openmind-secure-memory",
        static_cast<std::size_t>(size));
    if (fd < 0) {
        return {std::optional<Region>{}, Error::create_failed};
    }
    if (::ASharedMemory_getSize(fd) != static_cast<std::size_t>(size)) {
        ::close(fd);
        return {std::optional<Region>{}, Error::verification_failed};
    }
    void* writer = ::mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (writer == MAP_FAILED) {
        ::close(fd);
        return {std::optional<Region>{}, Error::map_failed};
    }
    return {std::optional<Region>(Region(fd, writer, size, Backend::ashared_memory)), Error::ok};
#else
    (void)size;
    return {std::optional<Region>{}, Error::unsupported};
#endif
}

Error Region::publish_read_only() noexcept {
    if (fd_ < 0 || writer_ == nullptr || size_ == 0 || published_) {
        return Error::state;
    }

    if (backend_ == Backend::memfd) {
        if (::fcntl(fd_, F_ADD_SEALS, kPublicationSeals) != 0) {
            return Error::publication_failed;
        }
        const int seals = ::fcntl(fd_, F_GET_SEALS);
        if (seals < 0 || (seals & kRequiredPublishedSeals) != kRequiredPublishedSeals) {
            return Error::verification_failed;
        }
    } else {
#if defined(__ANDROID__)
        if (::ASharedMemory_setProt(fd_, PROT_READ) != 0) {
            return Error::publication_failed;
        }
#else
        return Error::unsupported;
#endif
    }

    published_ = true;
    return Error::ok;
}

std::pair<int, Error> Region::duplicate_for_transfer() const noexcept {
    if (fd_ < 0 || !published_) {
        return {-1, Error::state};
    }
    const int duplicate = ::fcntl(fd_, F_DUPFD_CLOEXEC, 0);
    if (duplicate < 0) {
        return {-1, Error::duplicate_failed};
    }
    return {duplicate, Error::ok};
}

Error Region::finalize_publication() noexcept {
    if (fd_ < 0 || !published_) {
        return Error::state;
    }
    if (finalized_) {
        return Error::ok;
    }

    if (backend_ == Backend::memfd) {
        if (::fcntl(fd_, F_ADD_SEALS, F_SEAL_SEAL) != 0) {
            return Error::publication_failed;
        }
        const int seals = ::fcntl(fd_, F_GET_SEALS);
        if (seals < 0 || (seals & kRequiredFinalSeals) != kRequiredFinalSeals) {
            return Error::verification_failed;
        }
    }

    finalized_ = true;
    return Error::ok;
}

} // namespace openmind::secure_memory
