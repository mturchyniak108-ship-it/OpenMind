cmake_minimum_required(VERSION 3.22)

project(OpenMindNative LANGUAGES CXX)

find_package(Threads REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(OPENMIND_ROOT "${CMAKE_CURRENT_LIST_DIR}/..")
set(LLAMA_ROOT "${OPENMIND_ROOT}/llama.cpp")
set(LLAMA_LIB_DIR "${LLAMA_ROOT}/build-vulkan/bin")

add_library(openmind_inference STATIC
    src/inference.cpp
)

target_include_directories(openmind_inference
    PUBLIC
        "${CMAKE_CURRENT_LIST_DIR}/include"
        "${LLAMA_ROOT}/include"
        "${LLAMA_ROOT}/ggml/include"
)

target_link_libraries(openmind_inference
    PUBLIC
        Threads::Threads
)

add_executable(openmind_inference_test
    src/inference_test.cpp
)

add_executable(openmind_inference_benchmark
    src/inference_benchmark.cpp
)

add_executable(openmind_activation_probe
    src/activation_probe.cpp
)

target_include_directories(openmind_activation_probe
    PRIVATE
        "${LLAMA_ROOT}/include"
        "${LLAMA_ROOT}/ggml/include"
        "${LLAMA_ROOT}/src"
)

target_link_libraries(openmind_inference_benchmark
    PRIVATE
        openmind_inference
        "${LLAMA_LIB_DIR}/libllama.so"
        "${LLAMA_LIB_DIR}/libggml.so"
        "${LLAMA_LIB_DIR}/libggml-base.so"
        "${LLAMA_LIB_DIR}/libggml-cpu.so"
        "${LLAMA_LIB_DIR}/libggml-vulkan.so"
        dl
        m
)

target_link_libraries(openmind_activation_probe
    PRIVATE
        "${LLAMA_LIB_DIR}/libllama.so"
        "${LLAMA_LIB_DIR}/libggml.so"
        "${LLAMA_LIB_DIR}/libggml-base.so"
        "${LLAMA_LIB_DIR}/libggml-cpu.so"
        "${LLAMA_LIB_DIR}/libggml-vulkan.so"
        dl
        m
)

set_target_properties(openmind_activation_probe PROPERTIES
    BUILD_RPATH "${LLAMA_LIB_DIR}"
    INSTALL_RPATH "${LLAMA_LIB_DIR}"
)

set_target_properties(openmind_inference_benchmark PROPERTIES
    BUILD_RPATH "${LLAMA_LIB_DIR}"
    INSTALL_RPATH "${LLAMA_LIB_DIR}"
)

target_link_libraries(openmind_inference_test
    PRIVATE
        openmind_inference
        "${LLAMA_LIB_DIR}/libllama.so"
        "${LLAMA_LIB_DIR}/libggml.so"
        "${LLAMA_LIB_DIR}/libggml-base.so"
        "${LLAMA_LIB_DIR}/libggml-cpu.so"
        "${LLAMA_LIB_DIR}/libggml-vulkan.so"
        dl
        m
)

set_target_properties(openmind_inference_test PROPERTIES
    BUILD_RPATH "${LLAMA_LIB_DIR}"
    INSTALL_RPATH "${LLAMA_LIB_DIR}"
)


enable_testing()

set(OPENMIND_TEST_MODEL "" CACHE FILEPATH
    "GGUF model used by the native inference integration test")

if(OPENMIND_TEST_MODEL)
    add_test(
        NAME openmind_inference_test
        COMMAND openmind_inference_test "${OPENMIND_TEST_MODEL}"
    )
endif()
