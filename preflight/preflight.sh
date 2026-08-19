#!/data/data/com.termux/files/usr/bin/bash

set +e

REPORT_DIR="$HOME/OpenMind/preflight"
REPORT="$REPORT_DIR/report.txt"

mkdir -p "$REPORT_DIR"

exec > >(tee "$REPORT") 2>&1

echo "============================================================"
echo " OPENMIND / KMS PREFLIGHT"
echo "============================================================"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "OS: $(uname -a)"
echo

section() {
    echo
    echo "------------------------------------------------------------"
    echo " $1"
    echo "------------------------------------------------------------"
}

check_cmd() {
    local cmd="$1"
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "[FOUND]   $cmd -> $(command -v "$cmd")"
        "$cmd" --version 2>&1 | head -n 1
    else
        echo "[MISSING] $cmd"
    fi
}

check_pkg() {
    local pkg="$1"
    if command -v dpkg >/dev/null 2>&1 && dpkg -s "$pkg" >/dev/null 2>&1; then
        echo "[FOUND]   package: $pkg"
    else
        echo "[MISSING] package: $pkg"
    fi
}

section "SYSTEM"

echo "Architecture : $(uname -m)"
echo "Kernel       : $(uname -r)"
echo "CPU cores    : $(nproc 2>/dev/null || echo unknown)"
echo "Memory       :"
free -h 2>/dev/null || cat /proc/meminfo | head -n 5

echo
echo "Storage:"
df -h "$HOME"

section "TERMUX"

check_cmd pkg
check_cmd apt
check_cmd git
check_cmd python
check_cmd ssh
check_cmd curl
check_cmd wget
check_cmd jq
check_cmd sqlite3

section "PYTHON"

if command -v python >/dev/null 2>&1; then
    python --version
    python - <<'PY'
import sys
print("Python executable:", sys.executable)
print("Python version   :", sys.version)
PY
fi

section "BUILD TOOLCHAIN"

check_cmd clang
check_cmd gcc
check_cmd g++
check_cmd cmake
check_cmd ninja
check_cmd make
check_cmd pkg-config

section "OPTIONAL AI TOOLCHAIN"

check_cmd ollama
check_cmd llama-cli
check_cmd llama-server

section "NETWORK"

check_cmd ip
check_cmd ping
check_cmd ss

echo
echo "Interfaces:"
ip addr 2>/dev/null | grep -E '^[0-9]+:|inet ' || true

echo
echo "Listening sockets:"
ss -lnt 2>/dev/null || true

section "SSH"

if command -v ssh >/dev/null 2>&1; then
    ssh -V 2>&1
fi

if [ -d "$HOME/.ssh" ]; then
    echo "[FOUND] SSH directory: $HOME/.ssh"
    ls -la "$HOME/.ssh"
else
    echo "[MISSING] SSH directory"
fi

section "TERMUX PACKAGES RELEVANT TO OPENMIND"

for pkg in \
    git \
    python \
    openssh \
    curl \
    wget \
    jq \
    sqlite \
    clang \
    cmake \
    ninja \
    pkg-config \
    make
do
    check_pkg "$pkg"
done

section "PROJECT DIRECTORY"

if [ -d "$HOME/OpenMind" ]; then
    echo "[FOUND] $HOME/OpenMind"
    find "$HOME/OpenMind" -maxdepth 2 -type f -print 2>/dev/null
else
    echo "[MISSING] $HOME/OpenMind"
fi

section "SUMMARY"

echo "Preflight report saved to:"
echo "$REPORT"

echo
echo "IMPORTANT:"
echo "This script ONLY inspected the system."
echo "No packages were installed."
echo "No configuration was changed."
echo "============================================================"
