#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>
#include <random>
#include <cstdint>
#include <algorithm>
#include <cmath>

using namespace std;

using Clock = chrono::steady_clock;

static const size_t REGION_COUNT = 1024;
static const size_t SUBREGION_COUNT = 16;

struct Region {
    size_t begin;
    size_t end;
};

struct Result {
    double seconds;
    uint64_t checksum;
};

vector<uint8_t> load_pi() {
    ifstream f("pi_10M.txt");

    if (!f) {
        cerr << "Cannot open pi_10M.txt\n";
        exit(1);
    }

    vector<uint8_t> d;
    d.reserve(10'000'010);

    char c;
    while (f.get(c)) {
        if (c >= '0' && c <= '9')
            d.push_back(static_cast<uint8_t>(c - '0'));
    }

    return d;
}

/*
 * Generate ONE deterministic workload.
 *
 * Every architecture and every thread count uses
 * exactly these same indices.
 */
vector<size_t> make_workload(size_t n, size_t data_size) {
    vector<size_t> work;
    work.resize(n);

    mt19937_64 rng(0x123456789ABCDEF0ULL);
    uniform_int_distribution<size_t> dist(0, data_size - 1);

    for (size_t i = 0; i < n; ++i)
        work[i] = dist(rng);

    return work;
}

/*
 * Flat MAF:
 *
 * global index -> data[index]
 */
Result flat_lookup(
    const vector<uint8_t>& data,
    const vector<size_t>& work,
    unsigned threads
) {
    vector<thread> ts;
    vector<uint64_t> sums(threads, 0);

    size_t total = work.size();
    size_t base = total / threads;
    size_t rem = total % threads;

    auto start = Clock::now();

    for (unsigned t = 0; t < threads; ++t) {
        size_t begin = t * base + min<size_t>(t, rem);
        size_t count = base + (t < rem ? 1 : 0);
        size_t end = begin + count;

        ts.emplace_back([&, t, begin, end]() {
            uint64_t sum = 0;

            for (size_t i = begin; i < end; ++i)
                sum += data[work[i]];

            sums[t] = sum;
        });
    }

    for (auto& t : ts)
        t.join();

    auto stop = Clock::now();

    uint64_t checksum = 0;
    for (auto s : sums)
        checksum += s;

    return {
        chrono::duration<double>(stop - start).count(),
        checksum
    };
}

/*
 * Build first-level fractal regions.
 */
vector<Region> build_regions(size_t data_size) {
    vector<Region> regions;
    regions.reserve(REGION_COUNT);

    size_t base = data_size / REGION_COUNT;
    size_t rem = data_size % REGION_COUNT;

    size_t pos = 0;

    for (size_t i = 0; i < REGION_COUNT; ++i) {
        size_t size = base + (i < rem ? 1 : 0);

        regions.push_back({
            pos,
            pos + size
        });

        pos += size;
    }

    return regions;
}

/*
 * Binary-search region selection.
 *
 * global index
 *      ↓
 * region
 *      ↓
 * local offset
 */
size_t find_region(
    const vector<Region>& regions,
    size_t index
) {
    size_t lo = 0;
    size_t hi = regions.size();

    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;

        if (index < regions[mid].begin)
            hi = mid;
        else if (index >= regions[mid].end)
            lo = mid + 1;
        else
            return mid;
    }

    return regions.size() - 1;
}

/*
 * Fractal MAF level 1.
 */
Result fractal_lookup(
    const vector<uint8_t>& data,
    const vector<size_t>& work,
    const vector<Region>& regions,
    unsigned threads
) {
    vector<thread> ts;
    vector<uint64_t> sums(threads, 0);

    size_t total = work.size();
    size_t base = total / threads;
    size_t rem = total % threads;

    auto start = Clock::now();

    for (unsigned t = 0; t < threads; ++t) {
        size_t begin = t * base + min<size_t>(t, rem);
        size_t count = base + (t < rem ? 1 : 0);
        size_t end = begin + count;

        ts.emplace_back([&, t, begin, end]() {
            uint64_t sum = 0;

            for (size_t i = begin; i < end; ++i) {
                size_t index = work[i];

                size_t region =
                    find_region(regions, index);

                size_t local =
                    index - regions[region].begin;

                sum += data[
                    regions[region].begin + local
                ];
            }

            sums[t] = sum;
        });
    }

    for (auto& t : ts)
        t.join();

    auto stop = Clock::now();

    uint64_t checksum = 0;
    for (auto s : sums)
        checksum += s;

    return {
        chrono::duration<double>(stop - start).count(),
        checksum
    };
}

/*
 * Fractal MAF level 2.
 *
 * First map to region, then to subregion.
 */
Result fractal2_lookup(
    const vector<uint8_t>& data,
    const vector<size_t>& work,
    const vector<Region>& regions,
    unsigned threads
) {
    vector<vector<Region>> subregions(REGION_COUNT);

    for (size_t r = 0; r < REGION_COUNT; ++r) {
        const auto& R = regions[r];

        size_t size = R.end - R.begin;
        size_t base = size / SUBREGION_COUNT;
        size_t rem = size % SUBREGION_COUNT;

        size_t pos = R.begin;

        for (size_t s = 0; s < SUBREGION_COUNT; ++s) {
            size_t n = base + (s < rem ? 1 : 0);

            subregions[r].push_back({
                pos,
                pos + n
            });

            pos += n;
        }
    }

    vector<thread> ts;
    vector<uint64_t> sums(threads, 0);

    size_t total = work.size();
    size_t base = total / threads;
    size_t rem = total % threads;

    auto start = Clock::now();

    for (unsigned t = 0; t < threads; ++t) {
        size_t begin = t * base + min<size_t>(t, rem);
        size_t count = base + (t < rem ? 1 : 0);
        size_t end = begin + count;

        ts.emplace_back([&, t, begin, end]() {
            uint64_t sum = 0;

            for (size_t i = begin; i < end; ++i) {
                size_t index = work[i];

                size_t r =
                    find_region(regions, index);

                const auto& R = regions[r];

                size_t region_size = R.end - R.begin;
                size_t local = index - R.begin;

                size_t sub =
                    min(
                        SUBREGION_COUNT - 1,
                        local * SUBREGION_COUNT /
                        region_size
                    );

                const auto& S =
                    subregions[r][sub];

                size_t offset =
                    index - S.begin;

                sum += data[S.begin + offset];
            }

            sums[t] = sum;
        });
    }

    for (auto& t : ts)
        t.join();

    auto stop = Clock::now();

    uint64_t checksum = 0;
    for (auto s : sums)
        checksum += s;

    return {
        chrono::duration<double>(stop - start).count(),
        checksum
    };
}

void print_result(
    const char* name,
    Result r,
    size_t lookups,
    double baseline
) {
    double rate =
        static_cast<double>(lookups) / r.seconds / 1e6;

    double speedup =
        baseline / r.seconds;

    cout << name
         << " | "
         << r.seconds << " s | "
         << rate << " M/s | "
         << "speedup=" << speedup
         << "x | checksum=" << r.checksum
         << '\n';
}

int main(int argc, char** argv) {
    size_t lookups = 100'000'000;

    if (argc >= 2)
        lookups = stoull(argv[1]);

    auto data = load_pi();

    cout << "============================================================\n";
    cout << " FRACTAL MAF / CONTROLLED ARCHITECTURE BENCHMARK\n";
    cout << "============================================================\n";
    cout << "Data: " << data.size() << " digits\n";
    cout << "Lookups: " << lookups << "\n";
    cout << "Regions: " << REGION_COUNT << "\n";
    cout << "Subregions: " << SUBREGION_COUNT << "\n\n";

    auto work = make_workload(lookups, data.size());

    auto regions = build_regions(data.size());

    /*
     * Establish single-thread flat baseline.
     */
    Result baseline_result =
        flat_lookup(data, work, 1);

    double baseline =
        baseline_result.seconds;

    cout << "===== FLAT MAF =====\n";

    for (unsigned threads : {1u, 2u, 4u, 6u, 8u}) {
        Result r =
            flat_lookup(data, work, threads);

        print_result(
            "FLAT",
            r,
            lookups,
            baseline
        );
    }

    cout << "\n===== FRACTAL MAF LEVEL 1 =====\n";

    for (unsigned threads : {1u, 2u, 4u, 6u, 8u}) {
        Result r =
            fractal_lookup(
                data,
                work,
                regions,
                threads
            );

        print_result(
            "FRACTAL-1",
            r,
            lookups,
            baseline
        );
    }

    cout << "\n===== FRACTAL MAF LEVEL 2 =====\n";

    for (unsigned threads : {1u, 2u, 4u, 6u, 8u}) {
        Result r =
            fractal2_lookup(
                data,
                work,
                regions,
                threads
            );

        print_result(
            "FRACTAL-2",
            r,
            lookups,
            baseline
        );
    }

    cout << "\n===== WORKLOAD INTEGRITY =====\n";

    cout << "Flat checksum: "
         << baseline_result.checksum
         << "\n";

    cout << "\nComplete.\n";
}
