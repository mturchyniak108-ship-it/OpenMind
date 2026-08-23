#include "llama.h"
#include "llama-ext.h"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

struct VectorStats {
    double norm = 0.0;
    double mean = 0.0;
    double stddev = 0.0;
};

static VectorStats stats(
    const float * data,
    size_t n) {

    VectorStats s;

    if (!data || n == 0) {
        return s;
    }

    double sum = 0.0;

    for (size_t i = 0; i < n; ++i) {
        sum += data[i];
    }

    s.mean = sum / static_cast<double>(n);

    double variance = 0.0;

    for (size_t i = 0; i < n; ++i) {
        const double d =
            static_cast<double>(data[i]) - s.mean;

        variance += d * d;

        s.norm +=
            static_cast<double>(data[i]) *
            static_cast<double>(data[i]);
    }

    variance /= static_cast<double>(n);

    s.stddev = std::sqrt(variance);
    s.norm = std::sqrt(s.norm);

    return s;
}

static double cosine(
    const float * a,
    const float * b,
    size_t n) {

    if (!a || !b || n == 0) {
        return 0.0;
    }

    double dot = 0.0;
    double na = 0.0;
    double nb = 0.0;

    for (size_t i = 0; i < n; ++i) {
        const double av = a[i];
        const double bv = b[i];

        dot += av * bv;
        na += av * av;
        nb += bv * bv;
    }

    if (na <= 0.0 || nb <= 0.0) {
        return 0.0;
    }

    return dot / std::sqrt(na * nb);
}

static double l2_distance(
    const float * a,
    const float * b,
    size_t n) {

    if (!a || !b || n == 0) {
        return 0.0;
    }

    double sum = 0.0;

    for (size_t i = 0; i < n; ++i) {
        const double d =
            static_cast<double>(a[i]) -
            static_cast<double>(b[i]);

        sum += d * d;
    }

    return std::sqrt(sum);
}

int main(int argc, char ** argv) {

    if (argc < 2) {
        std::cerr
            << "Usage: "
            << argv[0]
            << " <model.gguf>\n";
        return 2;
    }

    const char * model_path = argv[1];

    std::cout
        << "============================================================\n"
        << " OPENMIND / NATIVE ACTIVATION PROBE\n"
        << "============================================================\n\n";

    std::cout
        << "Model: "
        << model_path
        << "\n";

    llama_backend_init();

    llama_model_params model_params =
        llama_model_default_params();

    model_params.n_gpu_layers = 99;

    llama_model * model =
        llama_model_load_from_file(
            model_path,
            model_params);

    if (!model) {
        std::cerr
            << "ERROR: model load failed\n";

        llama_backend_free();
        return 1;
    }

    const llama_model_params & mp = model_params;

    (void) mp;

    llama_context_params ctx_params =
        llama_context_default_params();

    ctx_params.n_ctx = 512;
    ctx_params.n_batch = 512;

    /*
     * Enable layer-input extraction.
     *
     * llama.cpp indexes the repeating transformer layers
     * from 0 through n_layer()-1.
     */
    const uint32_t n_layers =
        static_cast<uint32_t>(llama_model_n_layer(model));

    llama_context * ctx =
        llama_init_from_model(
            model,
            ctx_params);

    if (!ctx) {
        std::cerr
            << "ERROR: context creation failed\n";

        llama_model_free(model);
        llama_backend_free();

        return 1;
    }

    /*
     * Probe every transformer layer.
     *
     * Discover the layer count from the loaded model so the
     * probe works across different model sizes.
     */
    std::vector<uint32_t> probe_layers;
    probe_layers.reserve(n_layers);

    for (uint32_t layer = 0; layer < n_layers; ++layer) {
        probe_layers.push_back(layer);
    }

    std::cout
        << "\nProbing "
        << n_layers
        << " transformer layer inputs:\n";

    for (uint32_t layer : probe_layers) {

        llama_set_embeddings_layer_inp(
            ctx,
            layer,
            true);

        std::cout
            << "  L"
            << std::setw(2)
            << std::setfill('0')
            << layer
            << std::setfill(' ')
            << "\n";
    }

    /*
     * Tokenize a deterministic probe prompt.
     *
     * argv[2] optionally overrides the default control prompt.
     * Keeping the default unchanged preserves compatibility with
     * the original baseline experiment.
     */
    const std::string prompt =
        argc >= 3
            ? argv[2]
            : "The purpose of this experiment is to measure "
              "representation recurrence across transformer layers.";

    const llama_vocab * vocab =
        llama_model_get_vocab(model);

    int n_tokens =
        -llama_tokenize(
            vocab,
            prompt.c_str(),
            prompt.size(),
            nullptr,
            0,
            true,
            true);

    if (n_tokens <= 0) {
        std::cerr
            << "ERROR: tokenization sizing failed\n";

        llama_free(ctx);
        llama_model_free(model);
        llama_backend_free();

        return 1;
    }

    std::vector<llama_token> tokens(
        static_cast<size_t>(n_tokens));

    if (llama_tokenize(
            vocab,
            prompt.c_str(),
            prompt.size(),
            tokens.data(),
            tokens.size(),
            true,
            true) < 0) {

        std::cerr
            << "ERROR: tokenization failed\n";

        llama_free(ctx);
        llama_model_free(model);
        llama_backend_free();

        return 1;
    }

    llama_batch batch =
        llama_batch_get_one(
            tokens.data(),
            tokens.size());

    std::cout
        << "\nDecoding "
        << n_tokens
        << " prompt tokens...\n";

    if (llama_decode(ctx, batch) != 0) {

        std::cerr
            << "ERROR: llama_decode failed\n";

        llama_free(ctx);
        llama_model_free(model);
        llama_backend_free();

        return 1;
    }

    /*
     * Determine embedding dimension.
     *
     * llama_get_embeddings_layer_inp() returns the host-side
     * vector for the selected layer.
     */
    const size_t n_embd =
        llama_model_n_embd(model);

    /*
     * Preserve the layer number together with its captured vector.
     */
    struct LayerVector {
        uint32_t layer;
        const float * data;
    };

    std::vector<LayerVector> vectors;

    std::cout
        << "\n============================================================\n"
        << " LAYER INPUT EXTRACTION\n"
        << "============================================================\n";

    for (uint32_t layer : probe_layers) {

        const float * data =
            llama_get_embeddings_layer_inp(
                ctx,
                layer);

        if (!data) {
            std::cout
                << "L"
                << std::setw(2)
                << std::setfill('0')
                << layer
                << std::setfill(' ')
                << " -> unavailable\n";

            continue;
        }

        vectors.push_back({
            layer,
            data
        });

        std::cout
            << "L"
            << std::setw(2)
            << std::setfill('0')
            << layer
            << std::setfill(' ')
            << " -> captured\n";
    }

    std::cout
        << "\nEmbedding dimension: "
        << n_embd
        << "\n";

    /*
     * Compare the same final prompt-token position across
     * every captured layer.
     */
    const size_t token_index =
        static_cast<size_t>(n_tokens - 1);

    struct Activation {
        uint32_t layer;
        const float * data;
    };

    std::vector<Activation> activations;

    for (const LayerVector & v : vectors) {
        activations.push_back({
            v.layer,
            v.data + token_index * n_embd
        });
    }

    /*
     * Export final-token layer-input vectors.
     *
     * These are the exact vectors used by the recurrence scan below.
     */
    {
        std::ofstream out("activation_vectors.csv");

        if (!out) {
            std::cerr
                << "ERROR: unable to open activation_vectors.csv\n";

            llama_free(ctx);
            llama_model_free(model);
            llama_backend_free();

            return 1;
        }

        out << "layer,token_index,embedding_dimension";

        for (size_t d = 0; d < n_embd; ++d) {
            out << ",v" << d;
        }

        out << "\n";

        for (const Activation & activation : activations) {

            out
                << activation.layer
                << ","
                << token_index
                << ","
                << n_embd;

            for (size_t d = 0; d < n_embd; ++d) {
                out
                    << ","
                    << std::setprecision(9)
                    << activation.data[d];
            }

            out << "\n";
        }

        out.close();

        std::cout
            << "\nExported "
            << activations.size()
            << " final-token activation vectors to "
            << "activation_vectors.csv\n";
    }

    std::cout
        << "\n============================================================\n"
        << " FULL CROSS-LAYER RECURRENCE SCAN\n"
        << "============================================================\n";

    struct PairScore {
        uint32_t layer_a;
        uint32_t layer_b;
        double cosine;
        double distance;
    };

    std::vector<PairScore> scores;

    for (size_t i = 0; i < activations.size(); ++i) {
        for (size_t j = i + 1; j < activations.size(); ++j) {

            const double cos =
                cosine(
                    activations[i].data,
                    activations[j].data,
                    n_embd);

            const double distance =
                l2_distance(
                    activations[i].data,
                    activations[j].data,
                    n_embd);

            /*
             * Adjacent layers are expected to be highly similar.
             * Exclude them from the recurrence ranking so that
             * non-local representation relationships dominate.
             */
            if (activations[j].layer ==
                activations[i].layer + 1) {
                continue;
            }

            scores.push_back({
                activations[i].layer,
                activations[j].layer,
                cos,
                distance
            });
        }
    }

    std::sort(
        scores.begin(),
        scores.end(),
        [](const PairScore & a, const PairScore & b) {
            return a.cosine > b.cosine;
        });

    const size_t top_n =
        std::min<size_t>(20, scores.size());

    std::cout
        << "\nTop "
        << top_n
        << " non-adjacent layer similarities:\n";

    for (size_t i = 0; i < top_n; ++i) {

        const PairScore & s = scores[i];

        std::cout
            << std::setw(2)
            << std::setfill('0')
            << s.layer_a
            << " <-> "
            << std::setw(2)
            << s.layer_b
            << std::setfill(' ')
            << " | cosine="
            << std::fixed
            << std::setprecision(9)
            << s.cosine
            << " | distance="
            << std::setprecision(6)
            << s.distance
            << "\n";
    }

    /*
     * Analyze similarity as a function of layer separation.
     *
     * This controls for the fact that nearby layers are naturally
     * expected to have similar representations.
     */
    struct GapStats {
        size_t count = 0;
        double sum = 0.0;
        double min = 1.0;
        double max = -1.0;
    };

    std::vector<GapStats> gap_stats(36);

    for (const PairScore & s : scores) {
        const size_t gap =
            static_cast<size_t>(s.layer_b - s.layer_a);

        if (gap >= gap_stats.size()) {
            continue;
        }

        GapStats & g = gap_stats[gap];

        g.count++;
        g.sum += s.cosine;
        g.min = std::min(g.min, s.cosine);
        g.max = std::max(g.max, s.cosine);
    }

    std::cout
        << "\n============================================================\n"
        << " LAYER-GAP SIMILARITY PROFILE\n"
        << "============================================================\n";

    std::cout
        << "gap | count | mean_cosine | min_cosine | max_cosine\n";

    for (size_t gap = 2; gap < gap_stats.size(); ++gap) {

        const GapStats & g = gap_stats[gap];

        if (g.count == 0) {
            continue;
        }

        const double mean =
            g.sum / static_cast<double>(g.count);

        std::cout
            << std::setw(3)
            << gap
            << " | "
            << std::setw(5)
            << g.count
            << " | "
            << std::fixed
            << std::setprecision(9)
            << mean
            << " | "
            << g.min
            << " | "
            << g.max
            << "\n";
    }

    /*
     * Find the strongest genuinely non-local relationships.
     *
     * Ignore gaps <= 3 so that the ranking is not dominated by
     * ordinary local layer continuity.
     */
    std::vector<PairScore> nonlocal;

    for (const PairScore & s : scores) {
        const uint32_t gap =
            s.layer_b - s.layer_a;

        if (gap >= 4) {
            nonlocal.push_back(s);
        }
    }

    const size_t nonlocal_n =
        std::min<size_t>(20, nonlocal.size());

    std::cout
        << "\nTop "
        << nonlocal_n
        << " pairs with layer gap >= 4:\n";

    for (size_t i = 0; i < nonlocal_n; ++i) {

        const PairScore & s = nonlocal[i];

        std::cout
            << "L"
            << std::setw(2)
            << std::setfill('0')
            << s.layer_a
            << " <-> L"
            << std::setw(2)
            << s.layer_b
            << std::setfill(' ')
            << " | gap="
            << (s.layer_b - s.layer_a)
            << " | cosine="
            << std::fixed
            << std::setprecision(9)
            << s.cosine
            << " | distance="
            << std::setprecision(6)
            << s.distance
            << "\n";
    }

    std::cout
        << "\n============================================================\n"
        << " ACTIVATION PROBE COMPLETE\n"
        << "============================================================\n";

    llama_free(ctx);
    llama_model_free(model);
    llama_backend_free();

    return 0;
}
