#include "openmind/named_registry.hpp"

#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

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

void test_registry_lifecycle() {
    using openmind::secure_memory::NamedRegistry;
    using openmind::secure_memory::RegistryError;
    using openmind::secure_memory::RegistryOpenOptions;

    NamedRegistry registry;

    require(
        registry.open("alpha", RegistryOpenOptions{true, true, 0U}).second ==
            RegistryError::invalid_name,
        "INVALID_NAME_NO_LEADING_SLASH");
    require(
        registry.open("/", RegistryOpenOptions{true, true, 0U}).second ==
            RegistryError::invalid_name,
        "INVALID_NAME_EMPTY_COMPONENT");
    require(
        registry.open("/a/b", RegistryOpenOptions{true, true, 0U}).second ==
            RegistryError::invalid_name,
        "INVALID_NAME_SECOND_SLASH");

    const std::string embedded_nul("/a\0b", 4U);
    require(
        registry.open(
            std::string_view(embedded_nul.data(), embedded_nul.size()),
            RegistryOpenOptions{true, true, 0U}).second ==
            RegistryError::invalid_name,
        "INVALID_NAME_EMBEDDED_NUL");
    std::printf("R2C_EMBEDDED_NUL_REJECTED=PASS\n");

    auto missing = registry.open("/alpha", RegistryOpenOptions{});
    require(
        missing.first < 0 && missing.second == RegistryError::not_found,
        "OPEN_MISSING");

    auto first = registry.open(
        "/alpha",
        RegistryOpenOptions{true, true, 0U});
    require(first.first >= 0 && first.second == RegistryError::ok, "CREATE_ALPHA");
    const int first_fd = first.first;

    struct stat zero_stat {};
    require(::fstat(first_fd, &zero_stat) == 0, "ZERO_FSTAT");
    require(zero_stat.st_size == 0, "NEW_OBJECT_ZERO_LENGTH");
    std::printf("P3D_ZERO_LENGTH_CREATE=PASS\n");

    require(::ftruncate(first_fd, static_cast<off_t>(kSize)) == 0, "CALLER_FTRUNCATE");

    struct stat first_stat {};
    require(::fstat(first_fd, &first_stat) == 0, "FIRST_FSTAT");
    require(first_stat.st_size == static_cast<off_t>(kSize), "FIRST_SIZE");

    void* old_rw = ::mmap(
        nullptr,
        kSize,
        PROT_READ | PROT_WRITE,
        MAP_SHARED,
        first_fd,
        0);
    require(old_rw != MAP_FAILED, "FIRST_RW_MAP");
    std::memcpy(old_rw, "OLDOBJ", 6U);

    auto existing = registry.open("/alpha", RegistryOpenOptions{});
    require(
        existing.first >= 0 && existing.second == RegistryError::ok,
        "OPEN_EXISTING");
    const int existing_fd = existing.first;

    struct stat reopened_stat {};
    require(::fstat(existing_fd, &reopened_stat) == 0, "REOPEN_FSTAT");
    require(reopened_stat.st_size == static_cast<off_t>(kSize), "REOPEN_SEES_RESIZE");
    std::printf("P3D_REOPEN_SEES_FTRUNCATE=PASS\n");

    void* old_ro = ::mmap(nullptr, kSize, PROT_READ, MAP_SHARED, existing_fd, 0);
    require(old_ro != MAP_FAILED, "EXISTING_RO_MAP");
    require(std::memcmp(old_ro, "OLDOBJ", 6U) == 0, "EXISTING_CONTENT");

    auto duplicate_create = registry.open(
        "/alpha",
        RegistryOpenOptions{true, true, 0U});
    require(
        duplicate_create.first < 0 &&
            duplicate_create.second == RegistryError::already_exists,
        "O_CREAT_O_EXCL_EQUIVALENT");
    std::printf("P3D_CREATE_EXCLUSIVE=PASS\n");

    auto pre_sized = registry.open(
        "/beta",
        RegistryOpenOptions{true, true, kSize});
    require(
        pre_sized.first >= 0 && pre_sized.second == RegistryError::ok,
        "OPTIONAL_INITIAL_SIZE");
    struct stat beta_stat {};
    require(::fstat(pre_sized.first, &beta_stat) == 0, "BETA_FSTAT");
    require(beta_stat.st_size == static_cast<off_t>(kSize), "BETA_SIZE");
    require(::close(pre_sized.first) == 0, "BETA_CLOSE");
    require(registry.unlink_name("/beta") == RegistryError::ok, "UNLINK_BETA");

    require(registry.unlink_name("/alpha") == RegistryError::ok, "UNLINK_ALPHA");
    require(!registry.contains("/alpha"), "UNLINK_REMOVES_NAMESPACE");

    auto after_unlink = registry.open("/alpha", RegistryOpenOptions{});
    require(
        after_unlink.first < 0 && after_unlink.second == RegistryError::not_found,
        "OPEN_AFTER_UNLINK");
    require(std::memcmp(old_ro, "OLDOBJ", 6U) == 0, "OLD_MAP_SURVIVES_UNLINK");
    std::printf("P3D_UNLINK_LIVE_FD_SURVIVES=PASS\n");

    auto recreated = registry.open(
        "/alpha",
        RegistryOpenOptions{true, true, 0U});
    require(
        recreated.first >= 0 && recreated.second == RegistryError::ok,
        "RECREATE_ALPHA");
    const int new_fd = recreated.first;

    struct stat new_stat {};
    require(::fstat(new_fd, &new_stat) == 0, "NEW_FSTAT");
    require(new_stat.st_size == 0, "RECREATE_ZERO_LENGTH");
    require(
        first_stat.st_dev != new_stat.st_dev ||
            first_stat.st_ino != new_stat.st_ino,
        "RECREATE_DISTINCT_OBJECT");
    std::printf("P3D_RECREATE_DISTINCT_ZERO_OBJECT=PASS\n");

    require(::close(new_fd) == 0, "NEW_FD_CLOSE");
    require(registry.unlink_name("/alpha") == RegistryError::ok, "UNLINK_RECREATED");

    require(::munmap(old_ro, kSize) == 0, "OLD_RO_UNMAP");
    require(::munmap(old_rw, kSize) == 0, "OLD_RW_UNMAP");
    require(::close(existing_fd) == 0, "EXISTING_FD_CLOSE");
    require(::close(first_fd) == 0, "FIRST_FD_CLOSE");

    NamedRegistry limited(2U);
    auto q1 = limited.open("/q1", RegistryOpenOptions{true, true, 0U});
    auto q2 = limited.open("/q2", RegistryOpenOptions{true, true, 0U});
    auto q3 = limited.open("/q3", RegistryOpenOptions{true, true, 0U});
    require(q1.first >= 0 && q1.second == RegistryError::ok, "QUOTA_Q1");
    require(q2.first >= 0 && q2.second == RegistryError::ok, "QUOTA_Q2");
    require(
        q3.first < 0 && q3.second == RegistryError::resource_exhausted,
        "QUOTA_Q3_REJECTED");
    require(limited.linked_count() == 2U, "QUOTA_LINKED_COUNT");
    require(::close(q1.first) == 0, "QUOTA_Q1_CLOSE");
    require(::close(q2.first) == 0, "QUOTA_Q2_CLOSE");
    require(limited.unlink_name("/q1") == RegistryError::ok, "QUOTA_UNLINK_Q1");
    auto q3_retry = limited.open("/q3", RegistryOpenOptions{true, true, 0U});
    require(
        q3_retry.first >= 0 && q3_retry.second == RegistryError::ok,
        "QUOTA_RECOVERY");
    require(::close(q3_retry.first) == 0, "QUOTA_Q3_CLOSE");
    require(limited.unlink_name("/q2") == RegistryError::ok, "QUOTA_UNLINK_Q2");
    require(limited.unlink_name("/q3") == RegistryError::ok, "QUOTA_UNLINK_Q3");
    std::printf("R2C_LINKED_ENTRY_FD_QUOTA=PASS\n");
}

} // namespace

int main() {
    test_registry_lifecycle();
    std::printf("STATUS=PASS\n");
    return 0;
}
