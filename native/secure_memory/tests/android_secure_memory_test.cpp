#include "openmind/android_secure_memory.hpp"

#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

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

namespace {

constexpr std::size_t kSize = 4096U;

[[noreturn]] void fail(const char* gate) {
    std::fprintf(stderr, "FAIL=%s errno=%d (%s)\n", gate, errno, std::strerror(errno));
    std::exit(2);
}

void require(bool condition, const char* gate) {
    if (!condition) {
        fail(gate);
    }
}

bool blocked_errno(int value) {
    return value == EPERM || value == EACCES;
}

void test_memfd() {
    using openmind::secure_memory::Error;
    using openmind::secure_memory::Region;

    auto created = Region::create_memfd(kSize);
    require(created.first.has_value() && created.second == Error::ok, "MEMFD_CREATE");
    Region region = std::move(*created.first);

    struct stat st {};
    require(::fstat(region.native_handle(), &st) == 0, "MEMFD_FSTAT");
    require((st.st_mode & (S_IXUSR | S_IXGRP | S_IXOTH)) == 0, "MEMFD_NOEXEC_MODE");

    errno = 0;
    const int chmod_rc = ::fchmod(region.native_handle(), S_IRUSR | S_IWUSR | S_IXUSR);
    require(chmod_rc != 0 && blocked_errno(errno), "MEMFD_EXEC_BIT_ESCALATION");

    std::memcpy(region.writable_data(), "BEFORE", 6U);
    require(region.publish_read_only() == Error::ok, "MEMFD_PUBLISH");
    std::printf("P3A_MEMFD_PUBLICATION=PASS\n");

    std::memcpy(region.writable_data(), "AFTER!", 6U);
    require(std::memcmp(region.writable_data(), "AFTER!", 6U) == 0, "MEMFD_EXISTING_WRITER");
    std::printf("P3A_EXISTING_WRITER=PASS\n");

    errno = 0;
    const ssize_t direct_rc = ::write(region.native_handle(), "X", 1U);
    require(direct_rc == -1 && blocked_errno(errno), "MEMFD_DIRECT_WRITE");

    errno = 0;
    void* rw = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        region.native_handle(),
        0);
    require(rw == MAP_FAILED && blocked_errno(errno), "MEMFD_NEW_RW_MAP");
    std::printf("P3A_NEW_RW_BLOCKED=PASS\n");

    auto transferred = region.duplicate_for_transfer();
    require(transferred.first >= 0 && transferred.second == Error::ok, "MEMFD_DUPLICATE");
    const int consumer_fd = transferred.first;
    require((::fcntl(consumer_fd, F_GETFL) & O_ACCMODE) == O_RDWR, "MEMFD_DUPLICATE_ACCESS_MODE");

    void* ro = ::mmap(nullptr, kSize, PROT_READ, MAP_SHARED, consumer_fd, 0);
    require(ro != MAP_FAILED, "MEMFD_RO_MAP");
    require(std::memcmp(ro, "AFTER!", 6U) == 0, "MEMFD_RO_CONTENT");

    errno = 0;
    const int upgrade_rc = ::mprotect(ro, kSize, PROT_READ | PROT_WRITE);
    require(upgrade_rc != 0 && blocked_errno(errno), "MEMFD_RO_UPGRADE");
    std::printf("P3A_RO_UPGRADE_BLOCKED=PASS\n");

    require(::munmap(ro, kSize) == 0, "MEMFD_RO_UNMAP");
    require(::close(consumer_fd) == 0, "MEMFD_DUP_CLOSE");

    require(region.finalize_publication() == Error::ok, "MEMFD_FINALIZE");
    const int seals = ::fcntl(region.native_handle(), F_GET_SEALS);
    const int required =
        F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW |
        F_SEAL_FUTURE_WRITE | F_SEAL_EXEC;
    require(seals >= 0 && (seals & required) == required, "MEMFD_FINAL_SEALS");
    std::printf("P3A_FINAL_SEALS=PASS(0x%x)\n", seals);
}

void test_ashared_memory() {
    using openmind::secure_memory::Error;
    using openmind::secure_memory::Region;

    auto created = Region::create_ashared_memory(kSize);
#if defined(__ANDROID__)
    require(created.first.has_value() && created.second == Error::ok, "ASHAREDMEM_CREATE");
    Region region = std::move(*created.first);
    std::memcpy(region.writable_data(), "ASHMEM", 6U);

    require(region.publish_read_only() == Error::ok, "ASHAREDMEM_PUBLISH");
    std::memcpy(region.writable_data(), "LOCKED", 6U);

    errno = 0;
    void* rw = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        region.native_handle(),
        0);
    require(rw == MAP_FAILED && blocked_errno(errno), "ASHAREDMEM_NEW_RW_MAP");

    auto transferred = region.duplicate_for_transfer();
    require(transferred.first >= 0 && transferred.second == Error::ok, "ASHAREDMEM_DUPLICATE");
    const int consumer_fd = transferred.first;
    void* ro = ::mmap(nullptr, kSize, PROT_READ, MAP_SHARED, consumer_fd, 0);
    require(ro != MAP_FAILED, "ASHAREDMEM_RO_MAP");
    require(std::memcmp(ro, "LOCKED", 6U) == 0, "ASHAREDMEM_RO_CONTENT");

    errno = 0;
    const int upgrade_rc = ::mprotect(ro, kSize, PROT_READ | PROT_WRITE);
    require(upgrade_rc != 0 && blocked_errno(errno), "ASHAREDMEM_RO_UPGRADE");

    require(::munmap(ro, kSize) == 0, "ASHAREDMEM_RO_UNMAP");
    require(::close(consumer_fd) == 0, "ASHAREDMEM_DUP_CLOSE");
    require(region.finalize_publication() == Error::ok, "ASHAREDMEM_FINALIZE");
    std::printf("P3A_ASHAREDMEM_PUBLICATION=PASS\n");
#else
    require(!created.first.has_value() && created.second == Error::unsupported, "ASHAREDMEM_NON_ANDROID");
    std::printf("P3A_ASHAREDMEM_PUBLICATION=SKIP_NON_ANDROID\n");
#endif
}

} // namespace

int main() {
    test_memfd();
    test_ashared_memory();
    std::printf("STATUS=PASS\n");
    return 0;
}
