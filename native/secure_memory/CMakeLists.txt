cmake_minimum_required(VERSION 3.22)
project(OpenMindSecureMemory LANGUAGES CXX)

include(CheckCXXSourceCompiles)
check_cxx_source_compiles(
    "#ifndef __ANDROID__\n#error not android\n#endif\nint main(){return 0;}"
    OPENMIND_SECURE_MEMORY_ANDROID_TARGET)

add_library(openmind_android_secure_memory STATIC
    src/android_secure_memory.cpp
    src/unix_fd_transport.cpp
    src/named_registry.cpp
    src/named_registry_broker.cpp
    src/registry_endpoint.cpp
)
add_library(OpenMind::android_secure_memory ALIAS openmind_android_secure_memory)
target_include_directories(openmind_android_secure_memory
    PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_compile_features(openmind_android_secure_memory PUBLIC cxx_std_17)
set_target_properties(openmind_android_secure_memory PROPERTIES CXX_EXTENSIONS OFF)
if(OPENMIND_SECURE_MEMORY_ANDROID_TARGET)
    target_link_libraries(openmind_android_secure_memory PUBLIC android)
endif()

option(OPENMIND_SECURE_MEMORY_BUILD_TESTS "Build secure Android memory tests" OFF)
if(OPENMIND_SECURE_MEMORY_BUILD_TESTS)
    enable_testing()

    add_executable(openmind_android_secure_memory_test
        tests/android_secure_memory_test.cpp
    )
    target_link_libraries(openmind_android_secure_memory_test
        PRIVATE OpenMind::android_secure_memory
    )
    set_target_properties(openmind_android_secure_memory_test PROPERTIES CXX_EXTENSIONS OFF)
    add_test(NAME openmind_android_secure_memory_test COMMAND openmind_android_secure_memory_test)

    add_executable(openmind_unix_fd_transport_test
        tests/unix_fd_transport_test.cpp
    )
    target_link_libraries(openmind_unix_fd_transport_test
        PRIVATE OpenMind::android_secure_memory
    )
    set_target_properties(openmind_unix_fd_transport_test PROPERTIES CXX_EXTENSIONS OFF)
    add_test(NAME openmind_unix_fd_transport_test COMMAND openmind_unix_fd_transport_test)

    add_executable(openmind_named_registry_test
        tests/named_registry_test.cpp
    )
    target_link_libraries(openmind_named_registry_test
        PRIVATE OpenMind::android_secure_memory
    )
    set_target_properties(openmind_named_registry_test PROPERTIES CXX_EXTENSIONS OFF)
    add_test(NAME openmind_named_registry_test COMMAND openmind_named_registry_test)

    add_executable(openmind_named_registry_broker_test
        tests/named_registry_broker_test.cpp
    )
    target_link_libraries(openmind_named_registry_broker_test
        PRIVATE OpenMind::android_secure_memory
    )
    set_target_properties(openmind_named_registry_broker_test PROPERTIES CXX_EXTENSIONS OFF)
    add_test(NAME openmind_named_registry_broker_test COMMAND openmind_named_registry_broker_test)

    add_executable(openmind_registry_endpoint_test
        tests/registry_endpoint_test.cpp
    )
    target_link_libraries(openmind_registry_endpoint_test
        PRIVATE OpenMind::android_secure_memory
    )
    set_target_properties(openmind_registry_endpoint_test PROPERTIES CXX_EXTENSIONS OFF)
    add_test(NAME openmind_registry_endpoint_test COMMAND openmind_registry_endpoint_test)

    set_tests_properties(
        openmind_android_secure_memory_test
        openmind_unix_fd_transport_test
        openmind_named_registry_test
        openmind_named_registry_broker_test
        openmind_registry_endpoint_test
        PROPERTIES TIMEOUT 30
    )
endif()
