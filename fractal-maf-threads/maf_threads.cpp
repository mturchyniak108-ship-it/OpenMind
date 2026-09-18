#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <random>
#include <chrono>
#include <cstdint>
#include <algorithm>

using namespace std;

static const string PI_FILE = "pi_10M.txt";

vector<uint8_t> load_pi_digits() {
    ifstream f(PI_FILE);
    if (!f.is_open()) {
        cerr << "Cannot open " << PI_FILE << endl;
        exit(1);
    }

    vector<uint8_t> digits;
    digits.reserve(10'000'000);

    char c;
    while (f.get(c)) {
        if (c >= '0' && c <= '9')
            digits.push_back(static_cast<uint8_t>(c - '0'));
    }

    cout << "Loaded " << digits.size() << " digits." << endl;
    return digits;
}

struct ThreadResult {
    uint64_t sum = 0;
    size_t lookups = 0;
};

void worker(
    const vector<uint8_t>& digits,
    size_t lookups,
    size_t thread_id,
    ThreadResult& result
) {
    mt19937_64 rng(987654321ULL + thread_id * 0x9E3779B97F4A7C15ULL);
    uniform_int_distribution<size_t> dist(0, digits.size() - 1);

    uint64_t sum = 0;

    for (size_t i = 0; i < lookups; ++i)
        sum += digits[dist(rng)];

    result.sum = sum;
    result.lookups = lookups;
}

void run_test(
    const vector<uint8_t>& digits,
    unsigned threads,
    size_t total_lookups
) {
    vector<thread> workers;
    vector<ThreadResult> results(threads);

    size_t base = total_lookups / threads;
    size_t remainder = total_lookups % threads;

    auto t0 = chrono::steady_clock::now();

    for (unsigned i = 0; i < threads; ++i) {
        size_t n = base + (i < remainder ? 1 : 0);

        workers.emplace_back(
            worker,
            cref(digits),
            n,
            i,
            ref(results[i])
        );
    }

    for (auto& t : workers)
        t.join();

    auto t1 = chrono::steady_clock::now();

    double seconds =
        chrono::duration<double>(t1 - t0).count();

    uint64_t checksum = 0;
    size_t completed = 0;

    for (const auto& r : results) {
        checksum += r.sum;
        completed += r.lookups;
    }

    double rate =
        static_cast<double>(completed) / seconds;

    cout << threads << " thread"
         << (threads == 1 ? "" : "s")
         << " | "
         << completed << " lookups | "
         << seconds << " s | "
         << rate / 1e6 << " M lookups/s"
         << " | checksum=" << checksum
         << endl;
}

int main(int argc, char** argv) {
    auto digits = load_pi_digits();

    size_t total = 10'000'000;

    if (argc >= 2)
        total = stoull(argv[1]);

    cout << "\n===== FRACTAL MAF THREAD SCALING =====\n";
    cout << "Total lookups: " << total << "\n\n";

    vector<unsigned> thread_counts = {1, 2, 4, 6, 8};

    for (unsigned n : thread_counts)
        run_test(digits, n, total);

    cout << "\nComplete.\n";
    return 0;
}
