#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>


namespace {

constexpr uint32_t DIM = 1536;
constexpr uint32_t GROUP_COUNT = 24;
constexpr uint32_t LAYER_COUNT = 28;

constexpr size_t HEADER_BYTES = 68;
constexpr size_t CENTROID_BYTES =
    DIM * sizeof(float);

constexpr size_t MAP_BYTES =
    DIM * sizeof(uint32_t);

constexpr size_t LAYER_ID_BYTES =
    LAYER_COUNT * sizeof(uint32_t);

constexpr size_t LAYER_RANK_BYTES =
    LAYER_COUNT *
    GROUP_COUNT *
    sizeof(uint32_t);

constexpr size_t GLOBAL_RANK_BYTES =
    GROUP_COUNT * sizeof(uint32_t);

constexpr size_t EXPECTED_BYTES =
    HEADER_BYTES +
    CENTROID_BYTES +
    MAP_BYTES +
    LAYER_ID_BYTES +
    LAYER_RANK_BYTES +
    GLOBAL_RANK_BYTES;


uint32_t read_u32_le(
    const uint8_t * p
) {
    return
        static_cast<uint32_t>(p[0]) |
        (
            static_cast<uint32_t>(p[1])
            << 8
        ) |
        (
            static_cast<uint32_t>(p[2])
            << 16
        ) |
        (
            static_cast<uint32_t>(p[3])
            << 24
        );
}


uint64_t fnv1a64(
    const uint8_t * data,
    size_t size
) {
    uint64_t value =
        UINT64_C(14695981039346656037);

    constexpr uint64_t prime =
        UINT64_C(1099511628211);

    for (size_t i = 0; i < size; ++i) {
        value ^= data[i];
        value *= prime;
    }

    return value;
}


std::vector<uint8_t> read_file(
    const std::string & path
) {
    std::ifstream f(
        path,
        std::ios::binary |
        std::ios::ate
    );

    if (!f) {
        throw std::runtime_error(
            "unable to open artifact"
        );
    }

    const std::streamsize size =
        f.tellg();

    if (size < 0) {
        throw std::runtime_error(
            "unable to determine artifact size"
        );
    }

    f.seekg(
        0,
        std::ios::beg
    );

    std::vector<uint8_t> data(
        static_cast<size_t>(size)
    );

    if (!f.read(
            reinterpret_cast<char *>(
                data.data()
            ),
            size
        )) {
        throw std::runtime_error(
            "artifact read failed"
        );
    }

    return data;
}


std::vector<uint32_t> read_u32_array(
    const uint8_t * data,
    size_t count
) {
    std::vector<uint32_t> out(
        count
    );

    for (size_t i = 0; i < count; ++i) {
        out[i] = read_u32_le(
            data + i * 4
        );
    }

    return out;
}


bool valid_permutation(
    const uint32_t * begin,
    size_t count
) {
    std::vector<uint32_t> values(
        begin,
        begin + count
    );

    std::sort(
        values.begin(),
        values.end()
    );

    for (
        size_t i = 0;
        i < count;
        ++i
    ) {
        if (
            values[i] !=
            static_cast<uint32_t>(i)
        ) {
            return false;
        }
    }

    return true;
}


void print_hash(
    const char * name,
    const uint8_t * data,
    size_t size
) {
    std::cout
        << name
        << "="
        << std::hex
        << std::setw(16)
        << std::setfill('0')
        << fnv1a64(
            data,
            size
        )
        << std::dec
        << std::setfill(' ')
        << "\n";
}

}  // namespace


int main(
    int argc,
    char ** argv
) {
    try {
        if (argc != 2) {
            std::cerr
                << "usage: "
                << argv[0]
                << " forest_frozen_v1.bin\n";

            return 2;
        }

        const auto data =
            read_file(argv[1]);

        if (
            data.size() !=
            EXPECTED_BYTES
        ) {
            throw std::runtime_error(
                "artifact size mismatch"
            );
        }

        const uint8_t * p =
            data.data();

        std::array<uint8_t, 8>
            magic{};

        std::copy_n(
            p,
            magic.size(),
            magic.begin()
        );

        const uint32_t version =
            read_u32_le(p + 8);

        const uint32_t dimensions =
            read_u32_le(p + 12);

        const uint32_t group_size =
            read_u32_le(p + 16);

        const uint32_t group_count =
            read_u32_le(p + 20);

        const uint32_t layer_count =
            read_u32_le(p + 24);

        const uint32_t training_rows =
            read_u32_le(p + 28);

        const uint32_t training_tokens =
            read_u32_le(p + 32);

        const uint8_t * dataset_sha =
            p + 36;

        size_t offset =
            HEADER_BYTES;

        const uint8_t * centroid =
            p + offset;

        offset +=
            CENTROID_BYTES;

        const uint8_t * dimension_map_blob =
            p + offset;

        offset +=
            MAP_BYTES;

        const uint8_t * layer_ids_blob =
            p + offset;

        offset +=
            LAYER_ID_BYTES;

        const uint8_t * layer_rankings_blob =
            p + offset;

        offset +=
            LAYER_RANK_BYTES;

        const uint8_t * global_ranking_blob =
            p + offset;

        offset +=
            GLOBAL_RANK_BYTES;

        const auto dimension_map =
            read_u32_array(
                dimension_map_blob,
                DIM
            );

        const auto layer_ids =
            read_u32_array(
                layer_ids_blob,
                LAYER_COUNT
            );

        const auto layer_rankings =
            read_u32_array(
                layer_rankings_blob,
                LAYER_COUNT *
                GROUP_COUNT
            );

        const auto global_ranking =
            read_u32_array(
                global_ranking_blob,
                GROUP_COUNT
            );

        bool layers_valid = true;

        for (
            uint32_t layer = 0;
            layer < LAYER_COUNT;
            ++layer
        ) {
            const uint32_t * ranking =
                layer_rankings.data() +
                layer * GROUP_COUNT;

            if (!valid_permutation(
                    ranking,
                    GROUP_COUNT
                )) {
                layers_valid = false;
                break;
            }
        }

        std::cout
            << "magic_hex=";

        for (uint8_t value : magic) {
            std::cout
                << std::hex
                << std::setw(2)
                << std::setfill('0')
                << static_cast<unsigned>(
                    value
                );
        }

        std::cout
            << std::dec
            << std::setfill(' ')
            << "\n";

        std::cout
            << "version="
            << version
            << "\n";

        std::cout
            << "dimensions="
            << dimensions
            << "\n";

        std::cout
            << "group_size="
            << group_size
            << "\n";

        std::cout
            << "group_count="
            << group_count
            << "\n";

        std::cout
            << "layer_count="
            << layer_count
            << "\n";

        std::cout
            << "training_rows="
            << training_rows
            << "\n";

        std::cout
            << "training_tokens="
            << training_tokens
            << "\n";

        std::cout
            << "dataset_sha256=";

        for (
            size_t i = 0;
            i < 32;
            ++i
        ) {
            std::cout
                << std::hex
                << std::setw(2)
                << std::setfill('0')
                << static_cast<unsigned>(
                    dataset_sha[i]
                );
        }

        std::cout
            << std::dec
            << std::setfill(' ')
            << "\n";

        std::cout
            << "artifact_bytes="
            << data.size()
            << "\n";

        std::cout
            << "payload_end="
            << offset
            << "\n";

        std::cout
            << "dimension_map_valid="
            << (
                valid_permutation(
                    dimension_map.data(),
                    DIM
                )
                    ? "PASS"
                    : "FAIL"
            )
            << "\n";

        std::cout
            << "layer_rankings_valid="
            << (
                layers_valid
                    ? "PASS"
                    : "FAIL"
            )
            << "\n";

        std::cout
            << "global_ranking_valid="
            << (
                valid_permutation(
                    global_ranking.data(),
                    GROUP_COUNT
                )
                    ? "PASS"
                    : "FAIL"
            )
            << "\n";

        std::cout
            << "layer_first="
            << layer_ids.front()
            << "\n";

        std::cout
            << "layer_last="
            << layer_ids.back()
            << "\n";

        print_hash(
            "centroid_fnv64",
            centroid,
            CENTROID_BYTES
        );

        print_hash(
            "dimension_map_fnv64",
            dimension_map_blob,
            MAP_BYTES
        );

        print_hash(
            "layer_ids_fnv64",
            layer_ids_blob,
            LAYER_ID_BYTES
        );

        print_hash(
            "layer_rankings_fnv64",
            layer_rankings_blob,
            LAYER_RANK_BYTES
        );

        print_hash(
            "global_ranking_fnv64",
            global_ranking_blob,
            GLOBAL_RANK_BYTES
        );

        print_hash(
            "artifact_fnv64",
            data.data(),
            data.size()
        );

        return 0;
    }
    catch (
        const std::exception & exc
    ) {
        std::cerr
            << "forest frozen reader error: "
            << exc.what()
            << "\n";

        return 1;
    }
}
