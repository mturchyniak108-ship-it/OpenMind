#!/data/data/com.termux/files/usr/bin/bash

set +e

echo "============================================================"
echo " OPENMIND / VULKAN GPU PROBE"
echo "============================================================"
echo "Date: $(date -Is)"
echo

echo "DEVICE"
echo "------------------------------------------------------------"
echo "Model:        $(getprop ro.product.model)"
echo "SoC:          $(getprop ro.soc.manufacturer) $(getprop ro.soc.model)"
echo "Android:      $(getprop ro.build.version.release)"
echo "Architecture: $(uname -m)"
echo

echo "GPU PROPERTIES"
echo "------------------------------------------------------------"
for key in \
    ro.hardware \
    ro.board.platform \
    ro.hardware.egl \
    ro.hardware.vulkan \
    ro.vendor.gpu \
    ro.soc.manufacturer \
    ro.soc.model
do
    printf "%-24s : " "$key"
    getprop "$key" 2>/dev/null
done
echo

echo "ANDROID GPU LIBRARIES"
echo "------------------------------------------------------------"
find /vendor/lib64 /vendor/lib /system/vendor/lib64 /system/vendor/lib \
    -maxdepth 2 \
    \( -iname '*vulkan*' -o -iname '*adreno*' -o -iname '*freedreno*' \) \
    -print 2>/dev/null | head -n 100

echo

echo "TERMUX VULKAN COMMANDS"
echo "------------------------------------------------------------"

if command -v vulkaninfo >/dev/null 2>&1; then
    echo "[FOUND] vulkaninfo"
    vulkaninfo --summary 2>&1 | head -n 120
else
    echo "[MISSING] vulkaninfo"
fi

echo

if command -v vkmark >/dev/null 2>&1; then
    echo "[FOUND] vkmark"
else
    echo "[MISSING] vkmark"
fi

echo

echo "VULKAN LIBRARIES IN TERMUX"
echo "------------------------------------------------------------"

find "$PREFIX/lib" "$PREFIX/lib64" "$PREFIX/libexec" \
    -maxdepth 2 \
    -iname '*vulkan*' \
    -print 2>/dev/null | head -n 100

echo

echo "VULKAN ICD FILES"
echo "------------------------------------------------------------"

find "$PREFIX/share" \
    -path '*vulkan*' \
    -type f \
    -print 2>/dev/null | head -n 100

echo

echo "DEVICE NODES"
echo "------------------------------------------------------------"

ls -l /dev/dri 2>/dev/null || echo "/dev/dri unavailable to Termux"

echo

echo "RELEVANT ENVIRONMENT"
echo "------------------------------------------------------------"

env | grep -Ei 'vulkan|mesa|gpu|egl|icd|termux' || true

echo

echo "OPENCL"
echo "------------------------------------------------------------"

if command -v clinfo >/dev/null 2>&1; then
    clinfo 2>&1 | head -n 60
else
    echo "[MISSING] clinfo"
fi

echo

echo "============================================================"
echo " PROBE COMPLETE"
echo "============================================================"
