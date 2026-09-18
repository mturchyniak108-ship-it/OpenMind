#!/data/data/com.termux/files/usr/bin/bash

set -u

if [ "$#" -lt 1 ]; then
    printf "usage: %s <command> [args...]\n" "$0"
    exit 2
fi

# OpenMind Lodgepole compute policy.
# Lodgepole owns ODD logical CPUs only.
ODD_CPUS="1,3,5,7"

# Prevent numerical runtimes from unexpectedly creating
# large thread pools. Explicit experiment settings may
# override these later when scientifically justified.
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-1}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-1}"
export VECLIB_MAXIMUM_THREADS="${VECLIB_MAXIMUM_THREADS:-1}"

printf "OpenMind Lodgepole CPU policy: odd CPUs %s\n" "$ODD_CPUS" >&2

exec taskset -c "$ODD_CPUS" "$@"
