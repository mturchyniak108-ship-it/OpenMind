#include <vulkan/vulkan.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr uint32_t DIM = 1536;
constexpr uint32_t GROUP_SIZE = 64;
constexpr uint32_t BLOCKS = DIM / GROUP_SIZE;

struct Push {
    uint32_t blocks_per_item;
    uint32_t selected_blocks;
    uint32_t dimensions;
    uint32_t batch;
};

struct Buffer {
    VkBuffer buffer = VK_NULL_HANDLE;
    VkDeviceMemory memory = VK_NULL_HANDLE;
    VkDeviceSize size = 0;
    void * mapped = nullptr;
};

void check(VkResult result, const char * what) {
    if (result != VK_SUCCESS) {
        throw std::runtime_error(
            std::string(what) +
            " failed, VkResult=" +
            std::to_string(result)
        );
    }
}

std::vector<uint32_t> read_spv(const std::string & path) {
    std::ifstream f(path, std::ios::binary | std::ios::ate);

    if (!f) {
        throw std::runtime_error(
            "cannot open SPIR-V: " + path
        );
    }

    const auto bytes = static_cast<size_t>(
        f.tellg()
    );

    if (bytes == 0 || bytes % 4 != 0) {
        throw std::runtime_error(
            "invalid SPIR-V byte count"
        );
    }

    f.seekg(0);

    std::vector<uint32_t> code(
        bytes / sizeof(uint32_t)
    );

    f.read(
        reinterpret_cast<char *>(code.data()),
        static_cast<std::streamsize>(bytes)
    );

    return code;
}

uint32_t memory_type(
    VkPhysicalDevice physical,
    uint32_t bits,
    VkMemoryPropertyFlags required
) {
    VkPhysicalDeviceMemoryProperties props{};
    vkGetPhysicalDeviceMemoryProperties(
        physical,
        &props
    );

    for (uint32_t i = 0; i < props.memoryTypeCount; ++i) {
        if ((bits & (1u << i)) &&
            (props.memoryTypes[i].propertyFlags & required)
                == required) {
            return i;
        }
    }

    throw std::runtime_error(
        "suitable Vulkan memory type not found"
    );
}

Buffer make_buffer(
    VkPhysicalDevice physical,
    VkDevice device,
    VkDeviceSize size
) {
    Buffer out;
    out.size = size;

    VkBufferCreateInfo b{
        VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO
    };

    b.size = size;
    b.usage =
        VK_BUFFER_USAGE_STORAGE_BUFFER_BIT |
        VK_BUFFER_USAGE_TRANSFER_DST_BIT;
    b.sharingMode = VK_SHARING_MODE_EXCLUSIVE;

    check(
        vkCreateBuffer(
            device,
            &b,
            nullptr,
            &out.buffer
        ),
        "vkCreateBuffer"
    );

    VkMemoryRequirements req{};
    vkGetBufferMemoryRequirements(
        device,
        out.buffer,
        &req
    );

    VkMemoryAllocateInfo a{
        VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO
    };

    a.allocationSize = req.size;
    a.memoryTypeIndex = memory_type(
        physical,
        req.memoryTypeBits,
        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT |
        VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
    );

    check(
        vkAllocateMemory(
            device,
            &a,
            nullptr,
            &out.memory
        ),
        "vkAllocateMemory"
    );

    check(
        vkBindBufferMemory(
            device,
            out.buffer,
            out.memory,
            0
        ),
        "vkBindBufferMemory"
    );

    check(
        vkMapMemory(
            device,
            out.memory,
            0,
            size,
            0,
            &out.mapped
        ),
        "vkMapMemory"
    );

    return out;
}

void destroy_buffer(
    VkDevice device,
    Buffer & b
) {
    if (b.mapped) {
        vkUnmapMemory(
            device,
            b.memory
        );
    }

    if (b.buffer) {
        vkDestroyBuffer(
            device,
            b.buffer,
            nullptr
        );
    }

    if (b.memory) {
        vkFreeMemory(
            device,
            b.memory,
            nullptr
        );
    }

    b = {};
}

uint32_t pack4(
    int8_t a,
    int8_t b,
    int8_t c,
    int8_t d
) {
    return
        static_cast<uint8_t>(a) |
        (static_cast<uint32_t>(
            static_cast<uint8_t>(b)
        ) << 8) |
        (static_cast<uint32_t>(
            static_cast<uint8_t>(c)
        ) << 16) |
        (static_cast<uint32_t>(
            static_cast<uint8_t>(d)
        ) << 24);
}

double elapsed_ns(
    const std::chrono::steady_clock::time_point & a,
    const std::chrono::steady_clock::time_point & b
) {
    return std::chrono::duration<double, std::nano>(
        b - a
    ).count();
}

}  // namespace

int main(int argc, char ** argv) {
    try {
        if (argc != 2) {
            std::cerr
                << "usage: "
                << argv[0]
                << " shader.spv\n";
            return 2;
        }

        const std::string shader_path = argv[1];

        VkApplicationInfo app{
            VK_STRUCTURE_TYPE_APPLICATION_INFO
        };

        app.pApplicationName =
            "OpenMind Forest V8";

        app.applicationVersion = 1;
        app.pEngineName = "OpenMind";
        app.engineVersion = 1;
        app.apiVersion = VK_API_VERSION_1_1;

        VkInstanceCreateInfo ici{
            VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        };

        ici.pApplicationInfo = &app;

        VkInstance instance = VK_NULL_HANDLE;

        check(
            vkCreateInstance(
                &ici,
                nullptr,
                &instance
            ),
            "vkCreateInstance"
        );

        uint32_t physical_count = 0;

        check(
            vkEnumeratePhysicalDevices(
                instance,
                &physical_count,
                nullptr
            ),
            "vkEnumeratePhysicalDevices(count)"
        );

        if (physical_count == 0) {
            throw std::runtime_error(
                "no Vulkan physical device"
            );
        }

        std::vector<VkPhysicalDevice> physicals(
            physical_count
        );

        check(
            vkEnumeratePhysicalDevices(
                instance,
                &physical_count,
                physicals.data()
            ),
            "vkEnumeratePhysicalDevices"
        );

        VkPhysicalDevice physical =
            physicals.front();

        VkPhysicalDeviceProperties physical_props{};
        vkGetPhysicalDeviceProperties(
            physical,
            &physical_props
        );

        uint32_t family_count = 0;

        vkGetPhysicalDeviceQueueFamilyProperties(
            physical,
            &family_count,
            nullptr
        );

        std::vector<VkQueueFamilyProperties>
            families(family_count);

        vkGetPhysicalDeviceQueueFamilyProperties(
            physical,
            &family_count,
            families.data()
        );

        uint32_t compute_family = UINT32_MAX;

        for (uint32_t i = 0; i < family_count; ++i) {
            if (
                families[i].queueFlags &
                VK_QUEUE_COMPUTE_BIT
            ) {
                compute_family = i;
                break;
            }
        }

        if (compute_family == UINT32_MAX) {
            throw std::runtime_error(
                "no Vulkan compute queue"
            );
        }

        const float priority = 1.0f;

        VkDeviceQueueCreateInfo qci{
            VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO
        };

        qci.queueFamilyIndex = compute_family;
        qci.queueCount = 1;
        qci.pQueuePriorities = &priority;

        VkDeviceCreateInfo dci{
            VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO
        };

        dci.queueCreateInfoCount = 1;
        dci.pQueueCreateInfos = &qci;

        VkDevice device = VK_NULL_HANDLE;

        check(
            vkCreateDevice(
                physical,
                &dci,
                nullptr,
                &device
            ),
            "vkCreateDevice"
        );

        VkQueue queue = VK_NULL_HANDLE;

        vkGetDeviceQueue(
            device,
            compute_family,
            0,
            &queue
        );

        VkDescriptorSetLayoutBinding bindings[4]{};

        for (uint32_t i = 0; i < 4; ++i) {
            bindings[i].binding = i;
            bindings[i].descriptorType =
                VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
            bindings[i].descriptorCount = 1;
            bindings[i].stageFlags =
                VK_SHADER_STAGE_COMPUTE_BIT;
        }

        VkDescriptorSetLayoutCreateInfo dlci{
            VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO
        };

        dlci.bindingCount = 4;
        dlci.pBindings = bindings;

        VkDescriptorSetLayout descriptor_layout =
            VK_NULL_HANDLE;

        check(
            vkCreateDescriptorSetLayout(
                device,
                &dlci,
                nullptr,
                &descriptor_layout
            ),
            "vkCreateDescriptorSetLayout"
        );

        VkPushConstantRange push_range{};
        push_range.stageFlags =
            VK_SHADER_STAGE_COMPUTE_BIT;
        push_range.offset = 0;
        push_range.size = sizeof(Push);

        VkPipelineLayoutCreateInfo plci{
            VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO
        };

        plci.setLayoutCount = 1;
        plci.pSetLayouts = &descriptor_layout;
        plci.pushConstantRangeCount = 1;
        plci.pPushConstantRanges = &push_range;

        VkPipelineLayout pipeline_layout =
            VK_NULL_HANDLE;

        check(
            vkCreatePipelineLayout(
                device,
                &plci,
                nullptr,
                &pipeline_layout
            ),
            "vkCreatePipelineLayout"
        );

        const auto code = read_spv(
            shader_path
        );

        VkShaderModuleCreateInfo smci{
            VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO
        };

        smci.codeSize =
            code.size() * sizeof(uint32_t);
        smci.pCode = code.data();

        VkShaderModule shader = VK_NULL_HANDLE;

        check(
            vkCreateShaderModule(
                device,
                &smci,
                nullptr,
                &shader
            ),
            "vkCreateShaderModule"
        );

        VkPipelineShaderStageCreateInfo stage{
            VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO
        };

        stage.stage =
            VK_SHADER_STAGE_COMPUTE_BIT;
        stage.module = shader;
        stage.pName = "main";

        VkComputePipelineCreateInfo cpci{
            VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO
        };

        cpci.stage = stage;
        cpci.layout = pipeline_layout;

        VkPipeline pipeline = VK_NULL_HANDLE;

        check(
            vkCreateComputePipelines(
                device,
                VK_NULL_HANDLE,
                1,
                &cpci,
                nullptr,
                &pipeline
            ),
            "vkCreateComputePipelines"
        );

        VkDescriptorPoolSize pool_size{};
        pool_size.type =
            VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
        pool_size.descriptorCount = 4;

        VkDescriptorPoolCreateInfo dpci{
            VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO
        };

        dpci.maxSets = 1;
        dpci.poolSizeCount = 1;
        dpci.pPoolSizes = &pool_size;

        VkDescriptorPool descriptor_pool =
            VK_NULL_HANDLE;

        check(
            vkCreateDescriptorPool(
                device,
                &dpci,
                nullptr,
                &descriptor_pool
            ),
            "vkCreateDescriptorPool"
        );

        VkDescriptorSetAllocateInfo dsai{
            VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO
        };

        dsai.descriptorPool =
            descriptor_pool;
        dsai.descriptorSetCount = 1;
        dsai.pSetLayouts =
            &descriptor_layout;

        VkDescriptorSet descriptor_set =
            VK_NULL_HANDLE;

        check(
            vkAllocateDescriptorSets(
                device,
                &dsai,
                &descriptor_set
            ),
            "vkAllocateDescriptorSets"
        );

        VkCommandPoolCreateInfo cpooli{
            VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO
        };

        cpooli.queueFamilyIndex =
            compute_family;
        cpooli.flags =
            VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;

        VkCommandPool command_pool =
            VK_NULL_HANDLE;

        check(
            vkCreateCommandPool(
                device,
                &cpooli,
                nullptr,
                &command_pool
            ),
            "vkCreateCommandPool"
        );

        VkCommandBufferAllocateInfo cbai{
            VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO
        };

        cbai.commandPool = command_pool;
        cbai.level =
            VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        cbai.commandBufferCount = 1;

        VkCommandBuffer command =
            VK_NULL_HANDLE;

        check(
            vkAllocateCommandBuffers(
                device,
                &cbai,
                &command
            ),
            "vkAllocateCommandBuffers"
        );

        VkFenceCreateInfo fci{
            VK_STRUCTURE_TYPE_FENCE_CREATE_INFO
        };

        VkFence fence = VK_NULL_HANDLE;

        check(
            vkCreateFence(
                device,
                &fci,
                nullptr,
                &fence
            ),
            "vkCreateFence"
        );

        const uint32_t max_batch = 256;

        const VkDeviceSize packed_size =
            static_cast<VkDeviceSize>(
                max_batch
            ) *
            BLOCKS *
            16 *
            sizeof(uint32_t);

        const VkDeviceSize scales_size =
            static_cast<VkDeviceSize>(
                max_batch
            ) *
            BLOCKS *
            sizeof(float);

        const VkDeviceSize map_size =
            DIM * sizeof(uint32_t);

        const VkDeviceSize output_size =
            static_cast<VkDeviceSize>(
                max_batch
            ) *
            DIM *
            sizeof(float);

        Buffer packed = make_buffer(
            physical,
            device,
            packed_size
        );

        Buffer scales = make_buffer(
            physical,
            device,
            scales_size
        );

        Buffer map = make_buffer(
            physical,
            device,
            map_size
        );

        Buffer output = make_buffer(
            physical,
            device,
            output_size
        );

        auto * packed_words =
            static_cast<uint32_t *>(
                packed.mapped
            );

        auto * scale_values =
            static_cast<float *>(
                scales.mapped
            );

        auto * dimension_map =
            static_cast<uint32_t *>(
                map.mapped
            );

        auto * gpu_output =
            static_cast<float *>(
                output.mapped
            );

        std::mt19937 rng(1337);

        std::uniform_int_distribution<int>
            qdist(-127, 127);

        std::uniform_real_distribution<float>
            sdist(0.001f, 0.1f);

        for (
            uint32_t item = 0;
            item < max_batch;
            ++item
        ) {
            for (
                uint32_t block = 0;
                block < BLOCKS;
                ++block
            ) {
                scale_values[
                    item * BLOCKS + block
                ] = sdist(rng);

                const size_t base =
                    (
                        static_cast<size_t>(item) *
                        BLOCKS +
                        block
                    ) * 16;

                for (
                    uint32_t word = 0;
                    word < 16;
                    ++word
                ) {
                    packed_words[
                        base + word
                    ] = pack4(
                        static_cast<int8_t>(
                            qdist(rng)
                        ),
                        static_cast<int8_t>(
                            qdist(rng)
                        ),
                        static_cast<int8_t>(
                            qdist(rng)
                        ),
                        static_cast<int8_t>(
                            qdist(rng)
                        )
                    );
                }
            }
        }

        std::vector<uint32_t> permutation(
            DIM
        );

        for (
            uint32_t i = 0;
            i < DIM;
            ++i
        ) {
            permutation[i] = i;
        }

        std::shuffle(
            permutation.begin(),
            permutation.end(),
            rng
        );

        std::copy(
            permutation.begin(),
            permutation.end(),
            dimension_map
        );

        VkDescriptorBufferInfo infos[4]{};

        infos[0] = {
            packed.buffer,
            0,
            packed.size
        };

        infos[1] = {
            scales.buffer,
            0,
            scales.size
        };

        infos[2] = {
            map.buffer,
            0,
            map.size
        };

        infos[3] = {
            output.buffer,
            0,
            output.size
        };

        VkWriteDescriptorSet writes[4]{};

        for (
            uint32_t i = 0;
            i < 4;
            ++i
        ) {
            writes[i].sType =
                VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
            writes[i].dstSet =
                descriptor_set;
            writes[i].dstBinding = i;
            writes[i].descriptorCount = 1;
            writes[i].descriptorType =
                VK_DESCRIPTOR_TYPE_STORAGE_BUFFER;
            writes[i].pBufferInfo =
                &infos[i];
        }

        vkUpdateDescriptorSets(
            device,
            4,
            writes,
            0,
            nullptr
        );

        std::cout
            << "============================================================\n"
            << " OPENMIND / FOREST TOPOLOGY V8 — VULKAN DECODE + SCATTER\n"
            << "============================================================\n\n";

        std::cout
            << "VULKAN DEVICE\n"
            << "------------------------------------------------------------\n"
            << "name                 : "
            << physical_props.deviceName
            << "\n"
            << "api version          : "
            << VK_VERSION_MAJOR(
                physical_props.apiVersion
            )
            << "."
            << VK_VERSION_MINOR(
                physical_props.apiVersion
            )
            << "."
            << VK_VERSION_PATCH(
                physical_props.apiVersion
            )
            << "\n"
            << "compute queue family : "
            << compute_family
            << "\n\n";

        std::cout
            << "KERNEL CONTRACT\n"
            << "------------------------------------------------------------\n"
            << "dimensions           : "
            << DIM
            << "\n"
            << "blocks/item          : "
            << BLOCKS
            << "\n"
            << "values/block         : "
            << GROUP_SIZE
            << "\n"
            << "encoded bytes/block  : 68\n"
            << "scatter map          : non-contiguous permutation\n\n";

        const uint32_t batches[] = {
            1,
            4,
            16,
            64,
            256
        };

        const double fractions[] = {
            0.125,
            0.250,
            0.500,
            0.750,
            1.000
        };

        std::cout
            << "BENCHMARK\n"
            << "------------------------------------------------------------\n"
            << "batch request blocks cpu_mean_ns gpu_mean_ns gpu/cpu "
               "cpu_vec_s gpu_vec_s max_abs_error\n";

        for (
            uint32_t batch :
            batches
        ) {
            for (
                double fraction :
                fractions
            ) {
                const uint32_t selected =
                    std::max<uint32_t>(
                        1,
                        static_cast<uint32_t>(
                            std::ceil(
                                BLOCKS *
                                fraction
                            )
                        )
                    );

                std::vector<float> cpu_output(
                    static_cast<size_t>(
                        batch
                    ) * DIM,
                    0.0f
                );

                auto cpu_decode = [&]() {
                    std::fill(
                        cpu_output.begin(),
                        cpu_output.end(),
                        0.0f
                    );

                    for (
                        uint32_t item = 0;
                        item < batch;
                        ++item
                    ) {
                        for (
                            uint32_t block = 0;
                            block < selected;
                            ++block
                        ) {
                            const float scale =
                                scale_values[
                                    item *
                                    BLOCKS +
                                    block
                                ];

                            const size_t base =
                                (
                                    static_cast<size_t>(
                                        item
                                    ) *
                                    BLOCKS +
                                    block
                                ) * 16;

                            for (
                                uint32_t lane = 0;
                                lane < 64;
                                ++lane
                            ) {
                                const uint32_t word =
                                    packed_words[
                                        base +
                                        lane / 4
                                    ];

                                const uint32_t shift =
                                    (lane % 4) * 8;

                                const uint32_t raw =
                                    (
                                        word >>
                                        shift
                                    ) & 0xffu;

                                const int q =
                                    raw >= 128
                                        ? static_cast<int>(
                                            raw
                                        ) - 256
                                        : static_cast<int>(
                                            raw
                                        );

                                const uint32_t d =
                                    dimension_map[
                                        block * 64 +
                                        lane
                                    ];

                                cpu_output[
                                    static_cast<size_t>(
                                        item
                                    ) *
                                    DIM +
                                    d
                                ] =
                                    static_cast<float>(
                                        q
                                    ) *
                                    scale;
                            }
                        }
                    }
                };

                Push push{
                    BLOCKS,
                    selected,
                    DIM,
                    batch
                };

                auto record_command = [&]() {
                    check(
                        vkResetCommandBuffer(
                            command,
                            0
                        ),
                        "vkResetCommandBuffer"
                    );

                    VkCommandBufferBeginInfo bi{
                        VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO
                    };

                    bi.flags =
                        VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;

                    check(
                        vkBeginCommandBuffer(
                            command,
                            &bi
                        ),
                        "vkBeginCommandBuffer"
                    );

                    const VkDeviceSize active_output_bytes =
                        static_cast<VkDeviceSize>(
                            batch
                        ) *
                        DIM *
                        sizeof(float);

                    vkCmdFillBuffer(
                        command,
                        output.buffer,
                        0,
                        active_output_bytes,
                        0u
                    );

                    VkBufferMemoryBarrier clear_barrier{
                        VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER
                    };

                    clear_barrier.srcAccessMask =
                        VK_ACCESS_TRANSFER_WRITE_BIT;

                    clear_barrier.dstAccessMask =
                        VK_ACCESS_SHADER_WRITE_BIT;

                    clear_barrier.srcQueueFamilyIndex =
                        VK_QUEUE_FAMILY_IGNORED;

                    clear_barrier.dstQueueFamilyIndex =
                        VK_QUEUE_FAMILY_IGNORED;

                    clear_barrier.buffer =
                        output.buffer;

                    clear_barrier.offset = 0;

                    clear_barrier.size =
                        active_output_bytes;

                    vkCmdPipelineBarrier(
                        command,
                        VK_PIPELINE_STAGE_TRANSFER_BIT,
                        VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                        0,
                        0,
                        nullptr,
                        1,
                        &clear_barrier,
                        0,
                        nullptr
                    );

                    vkCmdBindPipeline(
                        command,
                        VK_PIPELINE_BIND_POINT_COMPUTE,
                        pipeline
                    );

                    vkCmdBindDescriptorSets(
                        command,
                        VK_PIPELINE_BIND_POINT_COMPUTE,
                        pipeline_layout,
                        0,
                        1,
                        &descriptor_set,
                        0,
                        nullptr
                    );

                    vkCmdPushConstants(
                        command,
                        pipeline_layout,
                        VK_SHADER_STAGE_COMPUTE_BIT,
                        0,
                        sizeof(Push),
                        &push
                    );

                    vkCmdDispatch(
                        command,
                        selected,
                        batch,
                        1
                    );

                    check(
                        vkEndCommandBuffer(
                            command
                        ),
                        "vkEndCommandBuffer"
                    );
                };

                record_command();

                VkSubmitInfo submit{
                    VK_STRUCTURE_TYPE_SUBMIT_INFO
                };

                submit.commandBufferCount = 1;
                submit.pCommandBuffers =
                    &command;

                check(
                    vkResetFences(
                        device,
                        1,
                        &fence
                    ),
                    "vkResetFences"
                );

                check(
                    vkQueueSubmit(
                        queue,
                        1,
                        &submit,
                        fence
                    ),
                    "vkQueueSubmit warmup"
                );

                check(
                    vkWaitForFences(
                        device,
                        1,
                        &fence,
                        VK_TRUE,
                        UINT64_MAX
                    ),
                    "vkWaitForFences warmup"
                );

                cpu_decode();

                double max_error = 0.0;

                for (
                    size_t i = 0;
                    i <
                    static_cast<size_t>(
                        batch
                    ) * DIM;
                    ++i
                ) {
                    max_error = std::max(
                        max_error,
                        std::abs(
                            static_cast<double>(
                                cpu_output[i]
                            ) -
                            static_cast<double>(
                                gpu_output[i]
                            )
                        )
                    );
                }

                const int repeats =
                    batch <= 4
                        ? 100
                        : batch <= 16
                            ? 60
                            : batch <= 64
                                ? 30
                                : 12;

                double cpu_total = 0.0;

                for (
                    int r = 0;
                    r < repeats;
                    ++r
                ) {
                    const auto t0 =
                        std::chrono::steady_clock::now();

                    cpu_decode();

                    const auto t1 =
                        std::chrono::steady_clock::now();

                    cpu_total +=
                        elapsed_ns(
                            t0,
                            t1
                        );
                }

                double gpu_total = 0.0;

                for (
                    int r = 0;
                    r < repeats;
                    ++r
                ) {
                    record_command();

                    check(
                        vkResetFences(
                            device,
                            1,
                            &fence
                        ),
                        "vkResetFences"
                    );

                    const auto t0 =
                        std::chrono::steady_clock::now();

                    check(
                        vkQueueSubmit(
                            queue,
                            1,
                            &submit,
                            fence
                        ),
                        "vkQueueSubmit"
                    );

                    check(
                        vkWaitForFences(
                            device,
                            1,
                            &fence,
                            VK_TRUE,
                            UINT64_MAX
                        ),
                        "vkWaitForFences"
                    );

                    const auto t1 =
                        std::chrono::steady_clock::now();

                    gpu_total +=
                        elapsed_ns(
                            t0,
                            t1
                        );
                }

                const double cpu_mean =
                    cpu_total / repeats;

                const double gpu_mean =
                    gpu_total / repeats;

                const double cpu_vec_s =
                    1.0e9 *
                    static_cast<double>(
                        batch
                    ) /
                    cpu_mean;

                const double gpu_vec_s =
                    1.0e9 *
                    static_cast<double>(
                        batch
                    ) /
                    gpu_mean;

                std::cout
                    << std::fixed
                    << std::setprecision(3)
                    << std::setw(5)
                    << batch
                    << " "
                    << std::setw(7)
                    << fraction
                    << " "
                    << std::setw(6)
                    << selected
                    << " "
                    << std::setw(11)
                    << cpu_mean
                    << " "
                    << std::setw(11)
                    << gpu_mean
                    << " "
                    << std::setw(8)
                    << gpu_mean /
                       cpu_mean
                    << " "
                    << std::setw(10)
                    << cpu_vec_s
                    << " "
                    << std::setw(10)
                    << gpu_vec_s
                    << " "
                    << std::scientific
                    << max_error
                    << std::fixed
                    << "\n";
            }
        }

        std::cout
            << "\nVALIDATION\n"
            << "------------------------------------------------------------\n"
            << "CPU/GPU comparison   : performed for every benchmark shape\n"
            << "expected tolerance   : <= 1e-6 absolute\n"
            << "\n"
            << "INTERPRETATION BOUNDARY\n"
            << "------------------------------------------------------------\n"
            << "V8 isolates BLOCK_INT8_64 decode and non-contiguous scatter.\n"
            << "The map is deterministic synthetic Orange-like geometry.\n"
            << "No llama.cpp graph or model inference is modified.\n"
            << "Queue submission + fence wait are included in GPU latency.\n"
            << "This intentionally exposes dispatch overhead at small batches.\n";

        vkDeviceWaitIdle(device);

        destroy_buffer(
            device,
            output
        );

        destroy_buffer(
            device,
            map
        );

        destroy_buffer(
            device,
            scales
        );

        destroy_buffer(
            device,
            packed
        );

        vkDestroyFence(
            device,
            fence,
            nullptr
        );

        vkDestroyCommandPool(
            device,
            command_pool,
            nullptr
        );

        vkDestroyDescriptorPool(
            device,
            descriptor_pool,
            nullptr
        );

        vkDestroyPipeline(
            device,
            pipeline,
            nullptr
        );

        vkDestroyShaderModule(
            device,
            shader,
            nullptr
        );

        vkDestroyPipelineLayout(
            device,
            pipeline_layout,
            nullptr
        );

        vkDestroyDescriptorSetLayout(
            device,
            descriptor_layout,
            nullptr
        );

        vkDestroyDevice(
            device,
            nullptr
        );

        vkDestroyInstance(
            instance,
            nullptr
        );

        return 0;
    }
    catch (const std::exception & exc) {
        std::cerr
            << "forest_v8 error: "
            << exc.what()
            << "\n";

        return 1;
    }
}
