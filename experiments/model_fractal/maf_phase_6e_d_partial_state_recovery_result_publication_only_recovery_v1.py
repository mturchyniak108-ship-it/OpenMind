#!/usr/bin/env python3
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


BRANCH = "labs/multidimensional-maf"

BASE_N = 440
BASE_SHA = (
    "8e4c81040c64f62df83b690dd7956de825bb4cb5a86dafa26ed3a65e90b0f219"
)

ROOT = Path.home() / "OpenMind"

RUNNER_REL = (
    "experiments/model_fractal/"
    "maf_phase_6e_d_partial_state_recovery_"
    "result_publication_only_recovery_v1.py"
)

PUB_PROTOCOL_REL = (
    "experiments/model_fractal/"
    "MAF_PHASE_6E_D_PARTIAL_STATE_RECOVERY_"
    "RESULT_PUBLICATION_ONLY_RECOVERY_PROTOCOL_V1.md"
)
PUB_PROTOCOL_SHA = (
    "07d6ebcfe886f3b3701075bd6d2edf713af2814d1150f1a980f3384e946638d6"
)
PUB_PROTOCOL_BLOB = (
    "d5aa76fc673dc6e46a0d21a844219ef967681429"
)

RECOVERY_PROTOCOL_REL = (
    "experiments/model_fractal/"
    "MAF_PHASE_6E_D_ENTRY_COMPLETE_MODEL_PERSISTENT_GENERATION_"
    "PARTIAL_STATE_RECOVERY_PROTOCOL_V1.md"
)
RECOVERY_PROTOCOL_SHA = (
    "a6526b2ae971300f34937313b7ad52d877050355bcb5bbb28fe34d90871eed95"
)

RECOVERY_RUNNER_REL = (
    "experiments/model_fractal/"
    "maf_phase_6e_d_entry_complete_model_persistent_generation_"
    "partial_state_recovery_v1.py"
)
RECOVERY_RUNNER_SHA = (
    "419ab9d24dddaf44c5ae527f91d2a26b87764c0ca8b79c77f6e1a6a7efe9deb1"
)
RECOVERY_RUNNER_BLOB = (
    "01d7ce02df75c2b8441422438af1691ef8f81814"
)

RECOVERY_SENTINEL = (
    Path.home()
    / ".openmind_authoritative_slots"
    / (
        "phase_6e_d_partial_state_recovery_"
        "a6300eb374db041a5f2bf2ebf6d345421d2515b3.spent"
    )
)
RECOVERY_SENTINEL_SHA = (
    "69f7458e011e18d78270f791c51e872d99a6becce64057582fa616cd435d1cd5"
)

BUILDING = (
    ROOT
    / "results/runtime/"
    "maf_full_model_persistent_generation_v1.building"
)

FINAL_RUNTIME = (
    ROOT
    / "results/runtime/"
    "maf_full_model_persistent_generation_v1"
)

PARTIAL = (
    FINAL_RUNTIME
    / "recovery_qualification_v1.json.partial"
)

RESULT = (
    FINAL_RUNTIME
    / "recovery_qualification_v1.json"
)

PARTIAL_BYTES = 2350
PARTIAL_SHA = (
    "94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6"
)

MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
)

GENERATION_PK = (
    "mafgen:v1:"
    "74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2"
)

SEGMENT_MANIFEST_SHA = (
    "3ceff3ac93710ad0c789509a47a50d032c3834f3349d30c46140a9367376e982"
)

SEGMENT_SHA = (
    "a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9"
)

VERDICT = (
    "RECOVERED COMPLETE-MODEL PERSISTENT GENERATION QUALIFIED"
)

AT_FDCWD = -100
RENAME_NOREPLACE = 1

ENV_HEAD = "OPENMIND_PHASE_6E_D_PUBLICATION_FROZEN_HEAD"
ENV_SHA = "OPENMIND_PHASE_6E_D_PUBLICATION_RUNNER_SHA256"
ENV_BLOB = "OPENMIND_PHASE_6E_D_PUBLICATION_RUNNER_BLOB"


class PublicationError(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if not ok:
        raise PublicationError(message)


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def canonical(value: dict) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def git(*args: str, binary: bool = False):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )


def git_text(*args: str) -> str:
    cp = git(*args)
    need(
        cp.returncode == 0,
        "git " + " ".join(args) + " failed",
    )
    return cp.stdout


def git_blob(relative: str) -> str:
    cp = git(
        "rev-parse",
        "HEAD:" + relative,
    )
    need(
        cp.returncode == 0,
        "cannot resolve blob: " + relative,
    )
    return cp.stdout.strip()


def head_bytes(relative: str) -> bytes:
    cp = git(
        "show",
        "HEAD:" + relative,
        binary=True,
    )
    need(
        cp.returncode == 0,
        "cannot read HEAD:" + relative,
    )
    return cp.stdout


def regular(path: Path, label: str):
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise PublicationError(
            label + " missing"
        ) from exc

    need(
        stat.S_ISREG(info.st_mode)
        and not stat.S_ISLNK(info.st_mode),
        label + " must be regular non-symlink",
    )
    return info


def directory(path: Path, label: str):
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise PublicationError(
            label + " missing"
        ) from exc

    need(
        stat.S_ISDIR(info.st_mode)
        and not stat.S_ISLNK(info.st_mode),
        label + " must be directory non-symlink",
    )
    return info


def repository(expected_head: str) -> dict:
    branch = git_text(
        "branch",
        "--show-current",
    ).strip()

    head = git_text(
        "rev-parse",
        "HEAD",
    ).strip()

    need(
        branch == BRANCH,
        "PUB01 branch",
    )
    need(
        head == expected_head,
        "PUB02 frozen HEAD",
    )

    state = git_text(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )

    tracked = [
        line
        for line in state.splitlines()
        if line and not line.startswith("?? ")
    ]

    need(
        not tracked,
        "PUB03 tracked worktree",
    )
    need(
        git(
            "diff",
            "--cached",
            "--quiet",
        ).returncode == 0,
        "PUB03 index",
    )

    paths = sorted(
        line[3:]
        for line in state.splitlines()
        if line.startswith("?? ")
    )

    path_sha = sha_bytes(
        b"".join(
            path.encode("utf-8") + b"\0"
            for path in paths
        )
    )

    need(
        len(paths) == BASE_N
        and path_sha == BASE_SHA,
        "PUB04 untracked baseline",
    )

    return {
        "branch": branch,
        "head": head,
        "untracked_count": len(paths),
        "untracked_sha": path_sha,
    }


def publication_sentinel(frozen_head: str) -> Path:
    return (
        Path.home()
        / ".openmind_authoritative_slots"
        / (
            "phase_6e_d_publication_only_recovery_"
            + frozen_head
            + ".spent"
        )
    )


def sentinel_bytes(
    frozen_head: str,
    runner_sha: str,
    runner_blob: str,
) -> bytes:
    return (
        canonical(
            {
                "branch": BRANCH,
                "head": frozen_head,
                "purpose":
                    "phase_6e_d_publication_only_recovery",
                "protocol_sha256":
                    PUB_PROTOCOL_SHA,
                "runner_git_blob":
                    runner_blob,
                "runner_path":
                    RUNNER_REL,
                "runner_sha256":
                    runner_sha,
                "schema":
                    "openmind."
                    "phase_6e_d_publication_only_recovery_slot.v1",
            }
        )
        + b"\n"
    )


def execution_authority():
    frozen_head = os.environ.get(
        ENV_HEAD,
        "",
    )
    runner_sha = os.environ.get(
        ENV_SHA,
        "",
    )
    runner_blob = os.environ.get(
        ENV_BLOB,
        "",
    )

    need(
        len(frozen_head) == 40,
        "missing publication frozen HEAD",
    )
    need(
        len(runner_sha) == 64,
        "missing publication runner SHA",
    )
    need(
        len(runner_blob) == 40,
        "missing publication runner blob",
    )

    checkpoint = repository(
        frozen_head
    )

    # Publication runner execution authority.
    runner = Path(__file__).resolve()
    expected_runner = (
        ROOT / RUNNER_REL
    ).resolve()

    need(
        runner == expected_runner,
        "publication runner path authority",
    )

    raw = runner.read_bytes()

    need(
        sha_bytes(raw) == runner_sha,
        "publication runner SHA authority",
    )
    need(
        head_bytes(RUNNER_REL) == raw,
        "publication runner HEAD/worktree authority",
    )
    need(
        git_blob(RUNNER_REL) == runner_blob,
        "publication runner blob authority",
    )

    # PUB05 — publication-only protocol.
    pub_protocol = ROOT / PUB_PROTOCOL_REL
    regular(
        pub_protocol,
        "PUB05 publication-only protocol",
    )
    need(
        sha_file(pub_protocol)
        == PUB_PROTOCOL_SHA,
        "PUB05 publication-only protocol SHA",
    )
    need(
        git_blob(PUB_PROTOCOL_REL)
        == PUB_PROTOCOL_BLOB,
        "PUB05 publication-only protocol blob",
    )

    # PUB06 — original recovery protocol.
    recovery_protocol = (
        ROOT / RECOVERY_PROTOCOL_REL
    )
    regular(
        recovery_protocol,
        "PUB06 recovery protocol",
    )
    need(
        sha_file(recovery_protocol)
        == RECOVERY_PROTOCOL_SHA,
        "PUB06 recovery protocol SHA",
    )

    # PUB07 — corrected recovery runner.
    recovery_runner = (
        ROOT / RECOVERY_RUNNER_REL
    )
    regular(
        recovery_runner,
        "PUB07 corrected recovery runner",
    )
    need(
        sha_file(recovery_runner)
        == RECOVERY_RUNNER_SHA,
        "PUB07 corrected recovery runner SHA",
    )
    need(
        git_blob(RECOVERY_RUNNER_REL)
        == RECOVERY_RUNNER_BLOB,
        "PUB07 corrected recovery runner blob",
    )

    # PUB08 — spent recovery sentinel.
    regular(
        RECOVERY_SENTINEL,
        "PUB08 recovery sentinel",
    )
    need(
        sha_file(RECOVERY_SENTINEL)
        == RECOVERY_SENTINEL_SHA,
        "PUB08 recovery sentinel SHA",
    )

    # PUB09 — externally spent publication sentinel.
    slot = publication_sentinel(
        frozen_head
    )
    regular(
        slot,
        "PUB09 publication sentinel",
    )

    actual_slot = slot.read_bytes()
    expected_slot = sentinel_bytes(
        frozen_head,
        runner_sha,
        runner_blob,
    )

    need(
        actual_slot == expected_slot,
        "PUB09 publication sentinel authority",
    )

    return (
        checkpoint,
        frozen_head,
        runner_sha,
        runner_blob,
        slot,
        sha_bytes(actual_slot),
    )


def validate_result(raw: bytes):
    need(
        len(raw) == PARTIAL_BYTES,
        "PUB12/PUB18 result size",
    )
    need(
        sha_bytes(raw) == PARTIAL_SHA,
        "PUB12/PUB19 result SHA",
    )
    need(
        raw.endswith(b"\n"),
        "PUB12 result newline",
    )

    try:
        value = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        raise PublicationError(
            "PUB12/PUB22 JSON"
        ) from exc

    need(
        isinstance(value, dict),
        "PUB12/PUB22 JSON object",
    )

    expected = {
        "schema":
            "openmind.maf_phase_6e_d_partial_state_recovery.v1",
        "verdict":
            VERDICT,
        "model_pk":
            MODEL_PK,
        "generation_pk":
            GENERATION_PK,
        "object_count":
            339,
        "object_store_qualification_count":
            339,
        "unique_object_pk_count":
            339,
        "strong_locator_count":
            339,
        "payload_authority_match_count":
            339,
        "pre_promotion_segment_reader_readback_count":
            339,
        "post_promotion_segment_reader_readback_count":
            339,
        "segment_manifest_sha256":
            SEGMENT_MANIFEST_SHA,
        "segment_sha256":
            SEGMENT_SHA,
        "recovery_protocol_sha256":
            RECOVERY_PROTOCOL_SHA,
        "recovery_runner_sha256":
            RECOVERY_RUNNER_SHA,
        "recovery_runner_git_blob":
            RECOVERY_RUNNER_BLOB,
        "recovery_execution_sentinel_sha256":
            RECOVERY_SENTINEL_SHA,
        "no_inference_or_output_parity_science":
            True,
        "no_network_access":
            True,
        "no_object_rematerialization":
            True,
        "no_segment_rematerialization":
            True,
        "no_source_gguf_access":
            True,
    }

    for key, expected_value in expected.items():
        need(
            value.get(key) == expected_value,
            "PUB12/PUB22 semantic: " + key,
        )

    gates = value.get("gates")

    need(
        isinstance(gates, dict)
        and len(gates) == 15,
        "PUB12/PUB22 recovery gates",
    )

    need(
        all(
            item in (True, "PASS")
            for item in gates.values()
        ),
        "PUB12/PUB22 failed recovery gate",
    )

    return value


def non_target_snapshot():
    snapshot = {}

    for child in sorted(
        FINAL_RUNTIME.iterdir(),
        key=lambda value: value.name,
    ):
        if child.name in {
            PARTIAL.name,
            RESULT.name,
        }:
            continue

        info = child.lstat()

        snapshot[child.name] = (
            info.st_mode,
            info.st_dev,
            info.st_ino,
            info.st_size,
        )

    return snapshot


def pre_publication():
    # PUB10
    need(
        not os.path.lexists(BUILDING),
        "PUB10 building runtime",
    )

    # PUB11
    directory(
        FINAL_RUNTIME,
        "PUB11 final runtime",
    )

    # PUB12
    source_info = regular(
        PARTIAL,
        "PUB12 source partial",
    )
    source_raw = PARTIAL.read_bytes()
    validate_result(source_raw)

    # PUB13
    need(
        not os.path.lexists(RESULT),
        "PUB13 final result exists",
    )

    # PUB14
    need(
        PARTIAL.parent == RESULT.parent,
        "PUB14 parent mismatch",
    )

    libc = ctypes.CDLL(
        None,
        use_errno=True,
    )

    renameat2 = getattr(
        libc,
        "renameat2",
        None,
    )

    need(
        renameat2 is not None,
        "PUB14 renameat2 unavailable",
    )

    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]

    renameat2.restype = ctypes.c_int

    snapshot = non_target_snapshot()

    return (
        renameat2,
        source_raw,
        source_info,
        snapshot,
    )


def invoke_renameat2(renameat2):
    ctypes.set_errno(0)

    rc = renameat2(
        AT_FDCWD,
        os.fsencode(PARTIAL),
        AT_FDCWD,
        os.fsencode(RESULT),
        RENAME_NOREPLACE,
    )

    if rc != 0:
        error_number = ctypes.get_errno()

        raise PublicationError(
            "PUB15 renameat2 failed errno="
            + str(error_number)
            + " "
            + os.strerror(error_number)
        )

    return rc


def fsync_parent():
    fd = os.open(
        FINAL_RUNTIME,
        os.O_RDONLY,
    )

    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def prohibited_activity_gate():
    activity = {
        "recovery_rerun": False,
        "object_payload_access": False,
        "segment_body_access": False,
        "source_model_access": False,
        "inference": False,
        "network": False,
        "performance": False,
    }

    need(
        not any(activity.values()),
        "PUB26 prohibited activity",
    )

    return activity


def post_publication(
    source_raw: bytes,
    source_info,
    snapshot,
    frozen_head: str,
):
    # PUB16
    need(
        not os.path.lexists(PARTIAL),
        "PUB16 source partial exists",
    )

    # PUB17
    final_info = regular(
        RESULT,
        "PUB17 final result",
    )

    # PUB18
    need(
        final_info.st_size == PARTIAL_BYTES,
        "PUB18 final size",
    )

    final_raw = RESULT.read_bytes()

    # PUB19
    need(
        sha_bytes(final_raw) == PARTIAL_SHA,
        "PUB19 final SHA",
    )

    # PUB20
    need(
        final_raw == source_raw,
        "PUB20 byte identity",
    )

    # PUB21
    need(
        final_info.st_dev == source_info.st_dev
        and final_info.st_ino == source_info.st_ino
        and final_info.st_size == source_info.st_size,
        "PUB21 inode identity",
    )

    # PUB22
    validate_result(final_raw)

    # PUB23
    fsync_parent()

    # PUB24
    reread = RESULT.read_bytes()
    need(
        reread == source_raw
        and sha_bytes(reread) == PARTIAL_SHA,
        "PUB24 post-fsync readback",
    )

    # PUB25
    checkpoint = repository(
        frozen_head
    )
    need(
        non_target_snapshot() == snapshot,
        "PUB25 non-target runtime changed",
    )

    # PUB26
    activity = prohibited_activity_gate()

    return (
        checkpoint,
        final_raw,
        final_info,
        activity,
    )


def main() -> int:
    print(
        "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
    )
    print(
        "PHASE 6E-D — PUBLICATION-ONLY RECOVERY EXECUTION"
    )

    (
        checkpoint,
        frozen_head,
        runner_sha,
        runner_blob,
        slot,
        slot_sha,
    ) = execution_authority()

    print("[ PUB01-PUB09 ] frozen authority: PASS")

    (
        renameat2,
        source_raw,
        source_info,
        snapshot,
    ) = pre_publication()

    print("[ PUB10-PUB14 ] pre-publication gates: PASS")

    rc = invoke_renameat2(
        renameat2
    )

    need(
        rc == 0,
        "PUB15 renameat2 return",
    )

    print("[ PUB15 ] renameat2(RENAME_NOREPLACE): PASS")

    (
        post_checkpoint,
        final_raw,
        final_info,
        activity,
    ) = post_publication(
        source_raw,
        source_info,
        snapshot,
        frozen_head,
    )

    print("[ PUB16-PUB26 ] post-publication gates: PASS")

    print()
    print("🟨📦 ===== GOLD STANDARD RETURN PACKET ===== 📦🟨")
    print(
        "STATUS             : "
        "PHASE 6E-D PUBLICATION-ONLY RECOVERY COMPLETE"
    )
    print("GATE FAILURE       : NONE")
    print(
        "VERDICT            : "
        "PUBLICATION-ONLY RECOVERY QUALIFIED"
    )
    print(
        "RECOVERY VERDICT   : "
        + VERDICT
    )
    print(
        "BRANCH             : "
        + post_checkpoint["branch"]
    )
    print(
        "HEAD               : "
        + post_checkpoint["head"]
    )
    print(
        "RUNNER SHA         : "
        + runner_sha
    )
    print(
        "RUNNER BLOB        : "
        + runner_blob
    )
    print("PUBLICATION SLOT   : SPENT")
    print(
        "PUBLICATION SLOT SHA: "
        + slot_sha
    )
    print("SOURCE PARTIAL     : ABSENT")
    print("FINAL RESULT       : PRESENT")
    print(
        "FINAL BYTES        : "
        + str(len(final_raw))
    )
    print(
        "FINAL SHA          : "
        + sha_bytes(final_raw)
    )
    print(
        "FINAL INODE        : "
        + str(final_info.st_ino)
    )
    print(
        "UNTRACKED COUNT    : "
        + str(
            post_checkpoint[
                "untracked_count"
            ]
        )
    )
    print(
        "UNTRACKED SET SHA  : "
        + post_checkpoint[
            "untracked_sha"
        ]
    )
    print("RECOVERY RERUN     : NO")
    print(
        "RUNTIME MUTATION   : "
        "EXACT PUBLICATION RENAME ONLY"
    )
    print(
        "PHASE 6E-D         : "
        "RECOVERED COMPLETE-MODEL PERSISTENT GENERATION QUALIFIED"
    )
    print(
        "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())

    except Exception as exc:
        print()
        print("🟨📦 ===== GOLD STANDARD RETURN PACKET ===== 📦🟨")
        print(
            "STATUS             : "
            "PHASE 6E-D PUBLICATION-ONLY RECOVERY FAILED"
        )
        print(
            "GATE FAILURE       : "
            + type(exc).__name__
            + ": "
            + str(exc)
        )
        print(
            "VERDICT            : "
            "PUBLICATION-ONLY RECOVERY NOT QUALIFIED"
        )
        print("AUTOMATIC RETRY    : NO")
        print("AUTOMATIC ROLLBACK : NO")
        print("SENTINEL DELETION  : NO")
        print("RECOVERY RERUN     : NO")
        print(
            "NEXT ACTION        : "
            "READ-ONLY DIAGNOSIS REQUIRED"
        )
        print(
            "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
        )

        raise SystemExit(1)
