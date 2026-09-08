#!/usr/bin/env bash

set -u

export PAGER=cat
export GIT_PAGER=cat
export PYTHONDONTWRITEBYTECODE=1

ARMED=1

EXPECTED_BRANCH="labs/multidimensional-maf"

EXPECTED_RUNNER_COMMIT="426ac118b14feb0e999784ef11290a5bc13fbba8"

EXPECTED_RUNNER_SHA="b63eee6938aaabaa8c2362803db60385354ae2cab9bafb9963a0c6bd522b455e"

EXPECTED_PROTOCOL_SHA="736ba16bb6406334e0fef0d4e002f2dd82b37398247b3e7cb1d4c81fd7d534af"

RUNNER="experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1_3.py"

PROTOCOL="experiments/model_fractal/MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_3_PROTOCOL.md"

RESULT="experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1_3.json"

TEMP="${RESULT}.tmp"

OK=1
FIRST_FAILURE="NONE"
INVOKED="NO"
RUNNER_RETURN="NOT INVOKED"

main() {
    ROOT="$(
        cd "$(dirname "$0")/../.." &&
        pwd -P
    )"

    cd "$ROOT" || {
        printf 'SAFETY STOP: repository root unavailable\n'
        return 1
    }

    BRANCH="$(
        git branch --show-current 2>/dev/null
    )"

    TRACKED_STATUS="$(
        git status \
            --short \
            --untracked-files=no \
            2>/dev/null
    )"

    CURRENT_RUNNER_SHA="$(
        sha256sum "$RUNNER" |
        awk '{print $1}'
    )"

    CURRENT_PROTOCOL_SHA="$(
        sha256sum "$PROTOCOL" |
        awk '{print $1}'
    )"

    COMMITTED_RUNNER_SHA="$(
        git show \
            "${EXPECTED_RUNNER_COMMIT}:${RUNNER}" |
        sha256sum |
        awk '{print $1}'
    )"

    RUNNER_LAST_COMMIT="$(
        git log \
            -1 \
            --format='%H' \
            -- "$RUNNER"
    )"

    if [ "$BRANCH" != "$EXPECTED_BRANCH" ]; then
        OK=0
        FIRST_FAILURE="BRANCH_MISMATCH"
    fi

    if [ "$OK" -eq 1 ] &&
       [ -n "$TRACKED_STATUS" ]
    then
        OK=0
        FIRST_FAILURE="TRACKED_WORKTREE_DIRTY"
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$CURRENT_RUNNER_SHA" != "$EXPECTED_RUNNER_SHA" ]
    then
        OK=0
        FIRST_FAILURE="RUNNER_SHA_MISMATCH"
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$COMMITTED_RUNNER_SHA" != "$EXPECTED_RUNNER_SHA" ]
    then
        OK=0
        FIRST_FAILURE="FROZEN_RUNNER_SHA_MISMATCH"
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$RUNNER_LAST_COMMIT" != "$EXPECTED_RUNNER_COMMIT" ]
    then
        OK=0
        FIRST_FAILURE="RUNNER_COMMIT_MISMATCH"
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$CURRENT_PROTOCOL_SHA" != "$EXPECTED_PROTOCOL_SHA" ]
    then
        OK=0
        FIRST_FAILURE="PROTOCOL_SHA_MISMATCH"
    fi

    if [ "$OK" -eq 1 ] &&
       [ -e "$RESULT" ]
    then
        OK=0
        FIRST_FAILURE="FINAL_RESULT_ALREADY_EXISTS"
    fi

    if [ "$OK" -eq 1 ] &&
       [ -e "$TEMP" ]
    then
        OK=0
        FIRST_FAILURE="RESERVATION_ALREADY_EXISTS"
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$ARMED" -ne 1 ]
    then
        printf '\n'
        printf 'V1.3 EXACT-ONCE WRAPPER: UNARMED\n'
        printf 'scientific invocation : NOT PERMITTED\n'
        printf 'runner commit         : %s\n' "$RUNNER_LAST_COMMIT"
        printf 'runner SHA            : %s\n' "$CURRENT_RUNNER_SHA"
        printf 'protocol SHA          : %s\n' "$CURRENT_PROTOCOL_SHA"
        printf 'result slot           : ABSENT\n'
        printf 'reservation           : ABSENT\n'
        return 0
    fi

    if [ "$OK" -eq 1 ] &&
       [ "$ARMED" -eq 1 ]
    then
        INVOKED="YES"

        python "$RUNNER"

        RUNNER_RETURN="$?"
    fi

    printf '\n'
    printf '===== EXACT-ONCE WRAPPER OUTCOME =====\n'
    printf 'gate failure  : %s\n' "$FIRST_FAILURE"
    printf 'invoked       : %s\n' "$INVOKED"
    printf 'runner return : %s\n' "$RUNNER_RETURN"

    if [ -e "$RESULT" ]; then
        printf 'result        : PRESENT\n'
        printf 'result SHA256 : %s\n' \
            "$(sha256sum "$RESULT" | awk '{print $1}')"
    else
        printf 'result        : ABSENT\n'
    fi

    if [ -e "$TEMP" ]; then
        printf 'reservation   : PRESENT\n'
        printf 'temp SHA256   : %s\n' \
            "$(sha256sum "$TEMP" | awk '{print $1}')"
    else
        printf 'reservation   : ABSENT\n'
    fi

    if [ "$OK" -ne 1 ]; then
        return 1
    fi

    return 0
}

main "$@"
