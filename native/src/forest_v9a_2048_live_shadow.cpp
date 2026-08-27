#include "llama.h"
#include "llama-ext.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr uint32_t DIM = 2048;
constexpr uint32_t GROUP_SIZE = 64;
constexpr uint32_t GROUP_COUNT = 32;
constexpr uint32_t LAYER_COUNT = 36;

constexpr size_t HEADER_BYTES = 24;
constexpr size_t MAP_BYTES = DIM * sizeof(uint32_t);
constexpr size_t GLOBAL_RANK_BYTES = GROUP_COUNT * sizeof(uint32_t);

constexpr size_t EXPECTED_BYTES =
    HEADER_BYTES + MAP_BYTES + GLOBAL_RANK_BYTES;

struct FrozenForest {
    std::vector<uint32_t> dimension_map;
    std::vector<uint32_t> global_ranking;
};

uint32_t read_u32_le(
    const uint8_t * p
) {
    return
        static_cast<uint32_t>(p[0]) |
        (static_cast<uint32_t>(p[1]) << 8) |
        (static_cast<uint32_t>(p[2]) << 16) |
        (static_cast<uint32_t>(p[3]) << 24);
}


float read_f32_le(
    const uint8_t * p
) {
    const uint32_t raw =
        read_u32_le(p);

    float value = 0.0f;

    std::memcpy(
        &value,
        &raw,
        sizeof(value)
    );

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
            "unable to open frozen artifact"
        );
    }

    const auto end = f.tellg();

    if (end < 0) {
        throw std::runtime_error(
            "unable to determine artifact size"
        );
    }

    std::vector<uint8_t> data(
        static_cast<size_t>(end)
    );

    f.seekg(0);

    if (!f.read(
            reinterpret_cast<char *>(
                data.data()
            ),
            static_cast<std::streamsize>(
                data.size()
            )
        )) {
        throw std::runtime_error(
            "artifact read failed"
        );
    }

    return data;
}


FrozenForest load_frozen(
    const std::string & path
) {
    const auto data =
        read_file(path);

    if (data.size() != EXPECTED_BYTES) {
        throw std::runtime_error(
            "OMFRST01 byte size mismatch"
        );
    }

    const uint8_t expected_magic[8] = {
        'O', 'M', 'F', 'R',
        'S', 'T', '0', '1'
    };

    if (!std::equal(
            data.begin(),
            data.begin() + 8,
            expected_magic
        )) {
        throw std::runtime_error(
            "OMFRST01 magic mismatch"
        );
    }

    if (read_u32_le(
            data.data() + 8
        ) != 1) {
        throw std::runtime_error(
            "OMFRST01 version mismatch"
        );
    }

    if (
        read_u32_le(data.data() + 12) != DIM ||
        read_u32_le(data.data() + 16) != GROUP_SIZE ||
        read_u32_le(data.data() + 20) != GROUP_COUNT
    ) {
        throw std::runtime_error(
            "OMFRST01 geometry mismatch"
        );
    }

    FrozenForest forest;

    forest.dimension_map.resize(DIM);
    forest.global_ranking.resize(GROUP_COUNT);

    size_t offset = HEADER_BYTES;

    for (uint32_t i = 0; i < DIM; ++i) {
        forest.dimension_map[i] =
            read_u32_le(data.data() + offset + i * 4);
    }

    offset += MAP_BYTES;

    for (uint32_t i = 0; i < GROUP_COUNT; ++i) {
        forest.global_ranking[i] =
            read_u32_le(data.data() + offset + i * 4);
    }

    return forest;
}


double cosine(
    const std::vector<float> & a,
    const std::vector<float> & b
) {
    double dot = 0.0;
    double aa = 0.0;
    double bb = 0.0;

    for (size_t i = 0; i < a.size(); ++i) {
        const double x = a[i];
        const double y = b[i];

        dot += x * y;
        aa += x * x;
        bb += y * y;
    }

    if (aa == 0.0 || bb == 0.0) {
        return 0.0;
    }

    return dot /
        (
            std::sqrt(aa) *
            std::sqrt(bb)
        );
}


double relative_l2(
    const std::vector<float> & a,
    const std::vector<float> & b
) {
    double numerator = 0.0;
    double denominator = 0.0;

    for (size_t i = 0; i < a.size(); ++i) {
        const double delta =
            static_cast<double>(a[i]) -
            static_cast<double>(b[i]);

        numerator += delta * delta;

        denominator +=
            static_cast<double>(a[i]) *
            static_cast<double>(a[i]);
    }

    if (denominator == 0.0) {
        return 0.0;
    }

    return std::sqrt(
        numerator / denominator
    );
}


double max_abs_error(
    const std::vector<float> & a,
    const std::vector<float> & b
) {
    double result = 0.0;

    for (size_t i = 0; i < a.size(); ++i) {
        result = std::max(
            result,
            std::abs(
                static_cast<double>(a[i]) -
                static_cast<double>(b[i])
            )
        );
    }

    return result;
}


double energy_fraction(
    const std::vector<float> & original,
    const std::vector<float> & reconstructed
) {
    double a = 0.0;
    double b = 0.0;

    for (size_t i = 0; i < original.size(); ++i) {
        a +=
            static_cast<double>(original[i]) *
            static_cast<double>(original[i]);

        b +=
            static_cast<double>(reconstructed[i]) *
            static_cast<double>(reconstructed[i]);
    }

    if (a == 0.0) {
        return 1.0;
    }

    return b / a;
}


struct QuantizedBlock {
    float scale = 0.0f;
    std::array<int8_t, GROUP_SIZE> q{};
};


QuantizedBlock quantize_block(
    const float * values
) {
    QuantizedBlock result;

    float peak = 0.0f;

    for (
        uint32_t i = 0;
        i < GROUP_SIZE;
        ++i
    ) {
        peak = std::max(
            peak,
            std::abs(values[i])
        );
    }

    if (peak == 0.0f) {
        result.scale = 0.0f;
        result.q.fill(0);

        return result;
    }

    result.scale =
        peak / 127.0f;

    for (
        uint32_t i = 0;
        i < GROUP_SIZE;
        ++i
    ) {
        long q =
            std::lround(
                values[i] /
                result.scale
            );

        q = std::max<long>(
            -127,
            std::min<long>(
                127,
                q
            )
        );

        result.q[i] =
            static_cast<int8_t>(q);
    }

    return result;
}

}  // namespace


int main(
    int argc,
    char ** argv
) {
    try {
        if (argc != 5) {
            std::cerr
                << "usage: "
                << argv[0]
                << " MODEL ARTIFACT LAYER PROMPT\n";

            return 2;
        }

        const std::string model_path =
            argv[1];

        const std::string artifact_path =
            argv[2];

        const uint32_t target_layer =
            static_cast<uint32_t>(
                std::stoul(argv[3])
            );

        const std::string prompt =
            argv[4];

        if (target_layer >= LAYER_COUNT) {
            throw std::runtime_error(
                "target layer out of range"
            );
        }

        const FrozenForest forest =
            load_frozen(
                artifact_path
            );

        llama_backend_init();

        llama_model_params model_params =
            llama_model_default_params();

        model_params.n_gpu_layers =
            99;

        llama_model * model =
            llama_model_load_from_file(
                model_path.c_str(),
                model_params
            );

        if (!model) {
            throw std::runtime_error(
                "model load failed"
            );
        }

        llama_context_params ctx_params =
            llama_context_default_params();

        ctx_params.n_ctx = 512;
        ctx_params.n_batch = 512;

        llama_context * ctx =
            llama_init_from_model(
                model,
                ctx_params
            );

        if (!ctx) {
            llama_model_free(model);
            throw std::runtime_error(
                "context creation failed"
            );
        }

        const size_t n_embd =
            llama_model_n_embd(model);

        if (n_embd != DIM) {
            throw std::runtime_error(
                "model embedding dimension != 2048"
            );
        }

        llama_set_embeddings_layer_inp(
            ctx,
            target_layer,
            true
        );

        const llama_vocab * vocab =
            llama_model_get_vocab(model);

        const int token_count =
            -llama_tokenize(
                vocab,
                prompt.c_str(),
                prompt.size(),
                nullptr,
                0,
                true,
                true
            );

        if (token_count <= 0) {
            throw std::runtime_error(
                "tokenization sizing failed"
            );
        }

        std::vector<llama_token> tokens(
            static_cast<size_t>(
                token_count
            )
        );

        if (
            llama_tokenize(
                vocab,
                prompt.c_str(),
                prompt.size(),
                tokens.data(),
                tokens.size(),
                true,
                true
            ) < 0
        ) {
            throw std::runtime_error(
                "tokenization failed"
            );
        }

        llama_batch batch =
            llama_batch_get_one(
                tokens.data(),
                tokens.size()
            );

        if (llama_decode(
                ctx,
                batch
            ) != 0) {
            throw std::runtime_error(
                "llama_decode failed"
            );
        }

        const float * layer_data =
            llama_get_embeddings_layer_inp(
                ctx,
                target_layer
            );

        if (!layer_data) {
            throw std::runtime_error(
                "layer activation unavailable"
            );
        }

        const size_t token_index =
            tokens.size() - 1;

        const float * live =
            layer_data +
            token_index *
            DIM;

        /*
         * Critical V9A boundary:
         * immediately copy authoritative llama activation.
         */
        std::vector<float> original(
            live,
            live + DIM
        );

        /*
         * Re-check source after copy.
         * No Forest operation has permission to mutate this memory.
         */
        std::vector<float> source_recheck(
            live,
            live + DIM
        );

        const double source_copy_error =
            max_abs_error(
                original,
                source_recheck
            );

        /*
         * V9A-2048 baseline:
         * operate directly on the copied live activation.
         * OMFRST01 contains no centroid.
         */
        const std::vector<float> & residual =
            original;

        /*
         * V9A uses every Orange group.
         * There is deliberately no routing loss.
         */
        std::vector<float> reconstructed_residual(
            DIM,
            0.0f
        );

        size_t encoded_bytes = 0;

        for (
            uint32_t block = 0;
            block < GROUP_COUNT;
            ++block
        ) {
            std::array<float, GROUP_SIZE>
                values{};

            for (
                uint32_t lane = 0;
                lane < GROUP_SIZE;
                ++lane
            ) {
                const uint32_t dimension =
                    forest.dimension_map[
                        block *
                        GROUP_SIZE +
                        lane
                    ];

                values[lane] =
                    residual[dimension];
            }

            const QuantizedBlock quantized =
                quantize_block(
                    values.data()
                );

            encoded_bytes +=
                GROUP_SIZE +
                sizeof(float);

            for (
                uint32_t lane = 0;
                lane < GROUP_SIZE;
                ++lane
            ) {
                const uint32_t dimension =
                    forest.dimension_map[
                        block *
                        GROUP_SIZE +
                        lane
                    ];

                reconstructed_residual[
                    dimension
                ] =
                    static_cast<float>(
                        quantized.q[lane]
                    ) *
                    quantized.scale;
            }
        }

        std::vector<float> reconstructed(
            DIM
        );

        for (
            uint32_t i = 0;
            i < DIM;
            ++i
        ) {
            reconstructed[i] =
                reconstructed_residual[i];
        }

        /*
         * Ensure llama-owned activation still did not change.
         */
        std::vector<float> source_after(
            live,
            live + DIM
        );

        const double source_mutation_error =
            max_abs_error(
                original,
                source_after
            );

        const double cos =
            cosine(
                original,
                reconstructed
            );

        const double l2 =
            relative_l2(
                original,
                reconstructed
            );

        const double max_error =
            max_abs_error(
                original,
                reconstructed
            );

        const double residual_energy =
            energy_fraction(
                residual,
                reconstructed_residual
            );

        /*
         * Standard sampler.
         * Shadow data is not consumed anywhere here.
         */
        llama_sampler * sampler =
            llama_sampler_init_greedy();

        if (!sampler) {
            throw std::runtime_error(
                "sampler creation failed"
            );
        }

        const llama_token next_token =
            llama_sampler_sample(
                sampler,
                ctx,
                -1
            );

        std::string piece;

        {
            std::vector<char> buffer(256);

            int n =
                llama_token_to_piece(
                    vocab,
                    next_token,
                    buffer.data(),
                    buffer.size(),
                    0,
                    true
                );

            if (n < 0) {
                buffer.resize(
                    static_cast<size_t>(
                        -n
                    )
                );

                n = llama_token_to_piece(
                    vocab,
                    next_token,
                    buffer.data(),
                    buffer.size(),
                    0,
                    true
                );
            }

            if (n > 0) {
                piece.assign(
                    buffer.data(),
                    static_cast<size_t>(n)
                );
            }
        }

        std::cout
            << "====================================================================\n"
            << " OPENMIND / FOREST V9A — LIVE FULL-ACCESS SHADOW RECONSTRUCTION\n"
            << "====================================================================\n\n";

        std::cout
            << "LIVE ACTIVATION\n"
            << "--------------------------------------------------------------------\n"
            << "target layer             : "
            << target_layer
            << "\n"
            << "prompt tokens            : "
            << tokens.size()
            << "\n"
            << "target token index        : "
            << token_index
            << "\n"
            << "dimensions                : "
            << DIM
            << "\n"
            << "source copy max error     : "
            << std::scientific
            << source_copy_error
            << "\n"
            << "source mutation max error : "
            << source_mutation_error
            << "\n\n";

        std::cout
            << std::fixed
            << std::setprecision(9)
            << "FOREST FULL ACCESS\n"
            << "--------------------------------------------------------------------\n"
            << "selected groups           : "
            << GROUP_COUNT
            << " / "
            << GROUP_COUNT
            << "\n"
            << "encoded payload bytes     : "
            << encoded_bytes
            << "\n"
            << "residual energy fraction  : "
            << residual_energy
            << "\n"
            << "activation cosine         : "
            << cos
            << "\n"
            << "activation relative L2    : "
            << l2
            << "\n"
            << "activation max abs error  : "
            << max_error
            << "\n\n";

        std::cout
            << "GENERATION CONTROL\n"
            << "--------------------------------------------------------------------\n"
            << "next token id             : "
            << next_token
            << "\n"
            << "next token piece          : "
            << std::quoted(piece)
            << "\n"
            << "shadow consumed by llama  : NO\n"
            << "llama activation written  : NO\n\n";

        const bool source_unchanged =
            source_mutation_error == 0.0;

        const bool reconstruction_valid =
            std::isfinite(cos) &&
            std::isfinite(l2) &&
            std::isfinite(max_error);

        std::cout
            << "V9A DECISION\n"
            << "--------------------------------------------------------------------\n"
            << "live activation capture   : PASS\n"
            << "Forest artifact read      : PASS\n"
            << "source activation intact  : "
            << (
                source_unchanged
                    ? "PASS"
                    : "FAIL"
            )
            << "\n"
            << "full-access reconstruction: "
            << (
                reconstruction_valid
                    ? "PASS"
                    : "FAIL"
            )
            << "\n";

        if (
            source_unchanged &&
            reconstruction_valid
        ) {
            std::cout
                << "result                    : V9A SHADOW PASS\n";
        }
        else {
            std::cout
                << "result                    : V9A REVIEW REQUIRED\n";
        }

        std::cout
            << "\nINTERPRETATION BOUNDARY\n"
            << "--------------------------------------------------------------------\n"
            << "The live llama activation is observed but never overwritten.\n"
            << "All 32 Orange groups are used, so routing loss is intentionally absent.\n"
            << "Any reconstruction difference is primarily BLOCK_INT8_64 quantization.\n"
            << "The standard sampler consumes only the untouched llama decode result.\n"
            << "V9A does not establish selective Forest inference replacement.\n";

        llama_sampler_free(
            sampler
        );

        llama_free(ctx);
        llama_model_free(model);
        llama_backend_free();

        return (
            source_unchanged &&
            reconstruction_valid
        )
            ? 0
            : 1;
    }
    catch (
        const std::exception & exc
    ) {
        std::cerr
            << "forest V9A error: "
            << exc.what()
            << "\n";

        return 1;
    }
}
