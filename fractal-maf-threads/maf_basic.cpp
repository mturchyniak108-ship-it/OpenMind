#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <random>

using namespace std;

static const string PI_FILE = "pi_10M.txt";

// Load digits from file into memory
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
        if (c >= '0' && c <= '9') {
            digits.push_back(c - '0');
        }
    }

    cout << "Loaded " << digits.size() << " digits." << endl;
    return digits;
}

// O(1) lookup
uint8_t maf_lookup(const vector<uint8_t>& digits, size_t idx) {
    if (idx >= digits.size()) {
        cerr << "Index out of range." << endl;
        return 0;
    }
    return digits[idx];
}

// Simple benchmark: random lookups
void benchmark_lookup(const vector<uint8_t>& digits, size_t n) {
    mt19937_64 rng(123456);
    uniform_int_distribution<size_t> dist(0, digits.size() - 1);

    auto t0 = chrono::high_resolution_clock::now();
    uint64_t sum = 0;

    for (size_t i = 0; i < n; ++i) {
        size_t idx = dist(rng);
        sum += maf_lookup(digits, idx);
    }

    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double> dt = t1 - t0;

    cout << "Benchmark: " << n << " lookups in "
         << dt.count() << " s (sum=" << sum << ")" << endl;
}

// Known first digits of pi for accuracy testing
static const uint8_t PI_KNOWN[20] = {
    3,1,4,1,5,9,2,6,5,3,
    5,8,9,7,9,3,2,3,8,4
};

// Bombardment test: massive random lookups
void bombard_lookup(const vector<uint8_t>& digits, size_t n) {
    mt19937_64 rng(987654321);
    uniform_int_distribution<size_t> dist(0, digits.size() - 1);

    auto t0 = chrono::high_resolution_clock::now();
    uint64_t sum = 0;

    for (size_t i = 0; i < n; ++i) {
        sum += digits[dist(rng)];
    }

    auto t1 = chrono::high_resolution_clock::now();
    chrono::duration<double> dt = t1 - t0;

    cout << "Bombardment: " << n << " random lookups in "
         << dt.count() << " s (sum=" << sum << ")" << endl;
}

// Accuracy test: compare against known pi digits
void accuracy_test(const vector<uint8_t>& digits) {
    cout << "Accuracy test against first 20 digits of pi:" << endl;

    bool ok = true;
    for (size_t i = 0; i < 20; ++i) {
        uint8_t d = digits[i];
        cout << "Index " << i << ": got " << int(d)
             << ", expected " << int(PI_KNOWN[i]);

        if (d == PI_KNOWN[i]) cout << " ✓" << endl;
        else {
            cout << " ✗" << endl;
            ok = false;
        }
    }

    if (ok) cout << "All known digits match. MAF accuracy: PERFECT." << endl;
    else    cout << "Mismatch detected. Check pi_10M.txt integrity." << endl;
}

// Combined torture test: accuracy + heavy bombardment
void torture_test(const vector<uint8_t>& digits) {
    cout << "=== MAF Torture Test ===" << endl;
    accuracy_test(digits);
    bombard_lookup(digits, 5000000);   // 5 million random lookups
    bombard_lookup(digits, 10000000);  // 10 million random lookups
    cout << "Torture test complete." << endl;
}

int main(int argc, char** argv) {
    auto digits = load_pi_digits();

    if (argc < 2) {
        cout << "Usage:\n"
             << "  ./maf_basic lookup <idx>\n"
             << "  ./maf_basic bench <n>\n"
             << "  ./maf_basic bombard <n>\n"
             << "  ./maf_basic accuracy\n"
             << "  ./maf_basic torture\n";
        return 0;
    }

    string cmd = argv[1];

    if (cmd == "lookup" && argc >= 3) {
        size_t idx = stoull(argv[2]);
        uint8_t d = maf_lookup(digits, idx);
        cout << "Digit[" << idx << "] = " << int(d) << endl;
    } else if (cmd == "bench" && argc >= 3) {
        size_t n = stoull(argv[2]);
        benchmark_lookup(digits, n);
    } else if (cmd == "bombard" && argc >= 3) {
        size_t n = stoull(argv[2]);
        bombard_lookup(digits, n);
    } else if (cmd == "accuracy") {
        accuracy_test(digits);
    } else if (cmd == "torture") {
        torture_test(digits);
    } else {
        cout << "Invalid command.\n";
    }

    return 0;
}
