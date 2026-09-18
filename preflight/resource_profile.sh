#!/data/data/com.termux/files/usr/bin/bash

set +e

BASE="$HOME/OpenMind/preflight"
REPORT="$BASE/resource_profile.txt"

mkdir -p "$BASE"

exec > >(tee "$REPORT") 2>&1

echo "============================================================"
echo " OPENMIND / KMS RESOURCE PROFILE"
echo "============================================================"
echo "Timestamp : $(date -Is)"
echo "Hostname  : $(hostname)"
echo

section() {
    echo
    echo "------------------------------------------------------------"
    echo " $1"
    echo "------------------------------------------------------------"
}

cmd_exists() {
    command -v "$1" >/dev/null 2>&1
}

version() {
    local cmd="$1"
    case "$cmd" in
        ssh) "$cmd" -V 2>&1 | head -n 1 ;;
        python) "$cmd" --version 2>&1 | head -n 1 ;;
        git) "$cmd" --version 2>&1 | head -n 1 ;;
        *) "$cmd" --version 2>&1 | head -n 1 ;;
    esac
}

check_cmd() {
    local cmd="$1"

    if cmd_exists "$cmd"; then
        echo "[FOUND]   $cmd -> $(command -v "$cmd")"
        version "$cmd"
    else
        echo "[MISSING] $cmd"
    fi
}

section "IDENTITY"

echo "OS:"
uname -a

echo
echo "Architecture:"
uname -m

echo
echo "Kernel:"
uname -r

echo
echo "Android:"
getprop ro.build.version.release 2>/dev/null

echo
echo "Device:"
getprop ro.product.model 2>/dev/null

echo
echo "Manufacturer:"
getprop ro.product.manufacturer 2>/dev/null

section "CPU"

echo "Logical CPU count:"
nproc 2>/dev/null

echo
echo "CPU information:"
if [ -r /proc/cpuinfo ]; then
    grep -E '^(processor|model name|Hardware|CPU architecture|Features)' \
        /proc/cpuinfo | head -n 40
fi

echo
echo "CPU frequencies:"
for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq; do
    [ -r "$f" ] && echo "$f: $(cat "$f") kHz"
done

section "MEMORY"

free -h 2>/dev/null

echo
echo "Detailed memory:"
grep -E '^(MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree)' \
    /proc/meminfo 2>/dev/null

section "STORAGE"

df -h "$HOME"

echo
echo "Termux storage:"
df -h /data/data/com.termux 2>/dev/null

echo
echo "Filesystem type:"
stat -f -c '%T' "$HOME" 2>/dev/null

section "BATTERY"

if cmd_exists termux-battery-status; then
    termux-battery-status
else
    echo "[UNAVAILABLE] termux-battery-status"
fi

section "THERMAL"

if [ -d /sys/class/thermal ]; then
    for zone in /sys/class/thermal/thermal_zone*; do
        [ -r "$zone/type" ] || continue
        TYPE=$(cat "$zone/type" 2>/dev/null)
        TEMP=$(cat "$zone/temp" 2>/dev/null)
        echo "$TYPE : $TEMP"
    done
else
    echo "[UNAVAILABLE] thermal information"
fi

section "NETWORK"

echo "Interfaces:"
ip addr 2>/dev/null | grep -E '^[0-9]+:|inet ' || true

echo
echo "Routes:"
ip route 2>/dev/null || true

echo
echo "Listening TCP sockets:"
ss -lnt 2>/dev/null || true

section "DEVELOPMENT TOOLCHAIN"

for cmd in \
    git \
    python \
    clang \
    gcc \
    g++ \
    cmake \
    ninja \
    make \
    pkg-config \
    sqlite3 \
    ssh \
    curl \
    wget \
    jq
do
    check_cmd "$cmd"
done

section "AI TOOLCHAIN"

for cmd in \
    ollama \
    llama-cli \
    llama-server
do
    check_cmd "$cmd"
done

section "PYTHON"

if cmd_exists python; then
    python - <<'PY'
import sys
print("Executable:", sys.executable)
print("Version:", sys.version)
print()
print("Prefix:", sys.prefix)
PY
fi

section "PYTHON INSTALLED PACKAGES"

if cmd_exists python; then
    python -m pip list 2>/dev/null | head -n 80
fi

section "TERMUX PACKAGE STATUS"

if cmd_exists dpkg; then
    dpkg-query -W -f='${binary:Package}\t${Version}\n' 2>/dev/null \
        | sort \
        | grep -E \
        '^(git|python|openssh|curl|wget|jq|sqlite|clang|cmake|ninja|make|pkg-config)'
fi

section "GPU / COMPUTE CAPABILITIES"

echo "OpenCL:"
if cmd_exists clinfo; then
    clinfo 2>/dev/null | head -n 60
else
    echo "[NOT INSTALLED]"
fi

echo
echo "Vulkan:"
if cmd_exists vulkaninfo; then
    vulkaninfo 2>/dev/null | head -n 60
else
    echo "[NOT INSTALLED]"
fi

section "CURRENT LOAD"

echo "Uptime:"
uptime 2>/dev/null

echo
echo "Top processes:"
ps -eo pid,pcpu,pmem,rss,args 2>/dev/null \
    | sort -k2 -nr \
    | head -n 15

section "OPENMIND"

echo "Project:"
echo "$HOME/OpenMind"

echo
echo "Files:"
find "$HOME/OpenMind" -maxdepth 3 -type f \
    -not -path '*/.git/*' \
    -print 2>/dev/null

section "RESOURCE PROFILE SUMMARY"

echo "Device: $(getprop ro.product.model 2>/dev/null)"
echo "Architecture: $(uname -m)"
echo "CPU cores: $(nproc 2>/dev/null)"
echo "Memory available:"
free -h 2>/dev/null | head -n 3

echo
echo "Storage available:"
df -h "$HOME" | tail -n 1

echo
echo "Profile saved:"
echo "$REPORT"

echo
echo "============================================================"
echo " PROFILE COMPLETE"
echo " No packages installed."
echo " No configuration changed."
echo "============================================================"
