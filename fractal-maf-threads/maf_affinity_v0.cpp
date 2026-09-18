#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>
#include <random>
#include <cstdint>
#include <algorithm>

using namespace std;

using Clock = chrono::steady_clock;

static constexpr size_t REGIONS = 1024;

struct Result {
    double seconds;
    uint64_t checksum;
};

struct Region {
    size_t begin;
    size_t end;
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

vector<Region> make_regions(size_t n) {
    vector<Region> r;
    r.reserve(REGIONS);

    size_t base = n / REGIONS;
    size_t rem = n % REGIONS;

    size_t pos = 0;

    for (size_t i = 0; i < REGIONS; ++i) {
        size_t len = base + (i < rem ? 1 : 0);

        r.push_back({
            pos,
            pos + len
        });

        pos += len;
    }

    return r;
}

/*
 * Deterministic random workload.
 */
vector<size_t> random_workload(
    size_t n,
    size_t data_size
) {
    vector<size_t> w(n);

    mt19937_64 rng(0xCAFEBABE12345678ULL);

    uniform_int_distribution<size_t>
        dist(0, data_size - 1);

    for (auto& x : w)
        x = dist(rng);

    return w;
}

/*
 * Locality workload:
 *
 * each thread receives a fixed region group.
 */
Result local_worker(
    const vector<uint8_t>& data,
    const vector<Region>& regions,
    size_t total,
    unsigned threads
) {
    vector<thread> ts;
    vector<uint64_t> sums(threads);

    size_t regions_per_thread =
        REGIONS / threads;

    size_t base =
        total / threads;

    size_t rem =
        total % threads;

    auto t0 = Clock::now();

    for (unsigned t = 0; t < threads; ++t) {

        size_t lookup_count =
            base + (t < rem ? 1 : 0);

        size_t region_begin =
            t * regions_per_thread;

        size_t region_end =
            (t == threads - 1)
                ? REGIONS
                : (t + 1) * regions_per_thread;

        ts.emplace_back(
            [&, t,
             lookup_count,
             region_begin,
             region_end]() {

                mt19937_64 rng(
                    0xABCDEF00ULL + t
                );

                size_t first =
                    regions[region_begin].begin;

                size_t last =
                    regions[region_end - 1].end - 1;

                uniform_int_distribution<size_t>
                    dist(first, last);

                uint64_t sum = 0;

                for (size_t i = 0;
                     i < lookup_count;
                     ++i) {

                    size_t index = dist(rng);

                    sum += data[index];
                }

                sums[t] = sum;
            }
        );
    }

    for (auto& t : ts)
        t.join();

    auto t1 = Clock::now();

    uint64_t checksum = 0;

    for (auto s : sums)
        checksum += s;

    return {
        chrono::duration<double>(t1 - t0).count(),
        checksum
    };
}

Result flat_random(
    const vector<uint8_t>& data,
    const vector<size_t>& work,
    unsigned threads
) {
    vector<thread> ts;
    vector<uint64_t> sums(threads);

    size_t base = work.size() / threads;
    size_t rem = work.size() % threads;

    auto t0 = Clock::now();

    for (unsigned t = 0; t < threads; ++t) {

        size_t begin =
            t * base + min<size_t>(t, rem);

        size_t count =
            base + (t < rem ? 1 : 0);

        size_t end = begin + count;

        ts.emplace_back(
            [&, t, begin, end]() {

                uint64_t sum = 0;

                for (size_t i = begin;
                     i < end;
                     ++i) {

                    sum += data[work[i]];
                }

                sums[t] = sum;
            }
        );
    }

    for (auto& t : ts)
        t.join();

    auto t1 = Clock::now();

    uint64_t checksum = 0;

    for (auto s : sums)
        checksum += s;

    return {
        chrono::duration<double>(t1 - t0).count(),
        checksum
    };
}

void print(
    const char* name,
    Result r,
    size_t n
) {
    cout << name
         << " | "
         << r.seconds
         << " s | "
         << (double)n / r.seconds / 1e6
         << " M/s | checksum="
         << r.checksum
         << '\n';
}

int main(int argc, char** argv) {

    size_t n = 100'000'000;

    if (argc >= 2)
        n = stoull(argv[1]);

    auto data = load_pi();
    auto regions = make_regions(data.size());

    cout << "============================================================\n";
    cout << " FRACTAL MAF / REGION AFFINITY BENCHMARK\n";
    cout << "============================================================\n";
    cout << "Data: " << data.size() << '\n';
    cout << "Lookups: " << n << '\n';
    cout << "Regions: " << REGIONS << "\n\n";

    auto random_work =
        random_workload(n, data.size());

    for (unsigned threads :
         {1u, 2u, 4u, 6u, 8u}) {

        cout << "\n===== "
             << threads
             << " THREADS =====\n";

        auto flat =
            flat_random(
                data,
                random_work,
                threads
            );

        print(
            "FLAT RANDOM ",
            flat,
            n
        );

        auto local =
            local_worker(
                data,
                regions,
                n,
                threads
            );

        print(
            "FRACTAL LOCAL",
            local,
            n
        );
    }

    cout << "\nComplete.\n";
}
