#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

import maf_generation_engine_v1 as gen
import maf_object_v1 as obj
import maf_resident_pk_directory_v1 as resident
import maf_segment_reader_v1 as reader


BRANCH = "labs/multidimensional-maf"

BASE_N = 440
BASE_SHA = (
    "8e4c81040c64f62df83b690dd7956de825bb4cb5a86dafa26ed3a65e90b0f219"
)

RUNNER_REL = (
    "experiments/model_fractal/"
    "maf_phase_6e_d_entry_complete_model_persistent_generation_"
    "partial_state_recovery_v1.py"
)

PROTO_REL = (
    "experiments/model_fractal/"
    "MAF_PHASE_6E_D_ENTRY_COMPLETE_MODEL_PERSISTENT_GENERATION_"
    "PARTIAL_STATE_RECOVERY_PROTOCOL_V1.md"
)

PROTO_SHA = (
    "a6526b2ae971300f34937313b7ad52d877050355bcb5bbb28fe34d90871eed95"
)

ORIG_REL = (
    "experiments/model_fractal/"
    "maf_phase_6e_d_entry_complete_model_persistent_"
    "maf_payload_generation_v1.py"
)

ORIG_SHA = (
    "e0c9d56adc35b4e34603ba8d031cb6569246c0d8d6775bc0d86ac074225e63a4"
)

ORIG_BLOB = (
    "e2c407e72ec45cfc32e8ef2b70f81b7f49ed3758"
)

FAILED_HEAD = (
    "f386695eb0769a5367c42ed00d02a2f12181acbd"
)

ORIG_SENT = Path(
    "/data/data/com.termux/files/home/"
    ".openmind_authoritative_slots/"
    "phase_6e_d_complete_model_persistent_generation_"
    "f386695eb0769a5367c42ed00d02a2f12181acbd.spent"
)

ORIG_SENT_SHA = (
    "abd8b27a648048d59a8cd9ab9e5fd2fb65ecaf3067d202ff31124da3f5519bfb"
)

MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
)

N = 339

SEG_LEN = 1888934699

SM_SHA = (
    "3ceff3ac93710ad0c789509a47a50d032c3834f3349d30c46140a9367376e982"
)

SEG_SHA = (
    "a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9"
)

CHUNK = 4 * 1024 * 1024

E_HEAD = "OPENMIND_PHASE_6E_D_RECOVERY_FROZEN_HEAD"
E_SHA = "OPENMIND_PHASE_6E_D_RECOVERY_RUNNER_SHA256"
E_BLOB = "OPENMIND_PHASE_6E_D_RECOVERY_RUNNER_BLOB"

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "experiments/model_fractal"

RUNNER = ROOT / RUNNER_REL
PROTO = ROOT / PROTO_REL
ORIG = ROOT / ORIG_REL

INV = D / "gguf_tensor_inventory_v1.json"
IDENT = D / "maf_full_model_identity_validation_v1.json"
RECIPES = D / "maf_compile_recipe_validation_v1.json"
REP = D / "maf_representation_v1.json"

CONSTR = (
    D
    / "MAF_PHASE_6E_D_ENTRY_COMPLETE_MODEL_PERSISTENT_MAF_PAYLOAD_GENERATION_CONSTRUCTION_PROTOCOL_V1.md"
)

OBJECT_API = D / "maf_object_v1.py"
SEG_BUILDER = D / "maf_segment_builder_v1.py"
GEN_ENGINE = D / "maf_generation_engine_v1.py"
SEG_READER = D / "maf_segment_reader_v1.py"
RESIDENT = D / "maf_resident_pk_directory_v1.py"

FROZEN = {
    INV:
        "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee",
    IDENT:
        "ef954f38e16ccbc73211c503d7d9c9b8462028d6222fb32fb9b15eb59615d25d",
    RECIPES:
        "ceed863754a119fc59b6fdeb80b9a6d1766bfa47e33992315536669f58331ccd",
    REP:
        "0e70bc32fb76945d7c684b3d73d5598f587fd17c6bda77b32db3e601af3f8dbe",
    CONSTR:
        "f599a652ae88bcf7ae193bdc26e42fdde89b6bef21a98012a061e55bb48919bb",
    OBJECT_API:
        "eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b",
    SEG_BUILDER:
        "f063c87989f9a646497743034e85d3f4674a7b45cf88df754b669d6621cc28f0",
    GEN_ENGINE:
        "8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51",
    SEG_READER:
        "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369",
    RESIDENT:
        "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6",
    PROTO: PROTO_SHA,
    ORIG: ORIG_SHA,
}

RP = ROOT / "results/runtime"

B = (
    RP
    / "maf_full_model_persistent_generation_v1.building"
)

F = (
    RP
    / "maf_full_model_persistent_generation_v1"
)

OD = B / "objects"

BS = B / "segment_00000000.mafseg"
BM = B / "segment_00000000.manifest.json"

BG = B / "generation.manifest.json"
BGP = B / "generation.manifest.json.partial"

BR = B / "recovery_qualification_v1.json"
BRP = B / "recovery_qualification_v1.json.partial"

FS = F / "segment_00000000.mafseg"
FM = F / "segment_00000000.manifest.json"
FG = F / "generation.manifest.json"

FR = F / "recovery_qualification_v1.json"


class R(RuntimeError):
    pass


def need(value, message):
    if not value:
        raise R(message)


def canon(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def hbytes(value):
    return hashlib.sha256(value).hexdigest()


def hfile(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        while True:
            block = handle.read(CHUNK)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def git(*args, binary=False):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )


def gtext(*args):
    cp = git(*args)

    need(
        cp.returncode == 0,
        "git "
        + " ".join(args)
        + " failed",
    )

    return cp.stdout


def head():
    return gtext(
        "rev-parse",
        "HEAD",
    ).strip()


def branch():
    return gtext(
        "branch",
        "--show-current",
    ).strip()


def status():
    return gtext(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )


def untracked(text):
    return sorted(
        line[3:]
        for line in text.splitlines()
        if line.startswith("?? ")
    )


def usha(items):
    return hbytes(
        b"".join(
            item.encode("utf-8") + b"\0"
            for item in items
        )
    )


def blob(path):
    text = gtext(
        "ls-tree",
        "HEAD",
        "--",
        path,
    ).strip()

    need(
        text,
        "missing tracked " + path,
    )

    return text.split()[2]


def headbytes(path):
    cp = git(
        "show",
        f"HEAD:{path}",
        binary=True,
    )

    need(
        cp.returncode == 0,
        "cannot read HEAD:" + path,
    )

    return cp.stdout


def reg(path, label):
    path = Path(path)

    try:
        info = path.lstat()

    except FileNotFoundError as exc:
        raise R(
            label + " missing"
        ) from exc

    need(
        not stat.S_ISLNK(info.st_mode)
        and stat.S_ISREG(info.st_mode),
        label + " not regular non-symlink",
    )

    return info


def direc(path, label):
    path = Path(path)

    try:
        info = path.lstat()

    except FileNotFoundError as exc:
        raise R(
            label + " missing"
        ) from exc

    need(
        not stat.S_ISLNK(info.st_mode)
        and stat.S_ISDIR(info.st_mode),
        label + " not directory non-symlink",
    )


def load(path):
    path = Path(path)

    try:
        value = json.loads(
            path.read_bytes().decode("utf-8")
        )

    except Exception as exc:
        raise R(
            "invalid JSON " + str(path)
        ) from exc

    need(
        isinstance(value, dict),
        "JSON root invalid " + str(path),
    )

    return value


def pk(row):
    value = row.get(
        "pk",
        row.get("object_pk"),
    )

    need(
        isinstance(value, str)
        and value.startswith("mafobj:v1:"),
        "invalid object PK",
    )

    return value


def repo():
    current_status = status()

    tracked = [
        line
        for line in current_status.splitlines()
        if line
        and not line.startswith("?? ")
    ]

    current_untracked = untracked(
        current_status
    )

    index_cp = git(
        "diff",
        "--cached",
        "--quiet",
    )

    whitespace_cp = git(
        "diff",
        "--check",
    )

    need(
        branch() == BRANCH,
        "branch mismatch",
    )

    need(
        not tracked,
        "tracked worktree dirty",
    )

    need(
        index_cp.returncode == 0,
        "index not empty",
    )

    need(
        whitespace_cp.returncode == 0
        and not whitespace_cp.stdout.strip()
        and not whitespace_cp.stderr.strip(),
        "diff-check failed",
    )

    need(
        len(current_untracked) == BASE_N
        and usha(current_untracked) == BASE_SHA,
        "untracked baseline mismatch",
    )

    return {
        "branch": BRANCH,
        "head": head(),
        "status": current_status,
        "n": len(current_untracked),
        "usha": usha(current_untracked),
    }


def slot_gate(repository):
    expected_head = os.environ.get(
        E_HEAD,
        "",
    )

    expected_sha = os.environ.get(
        E_SHA,
        "",
    )

    expected_blob = os.environ.get(
        E_BLOB,
        "",
    )

    need(
        expected_head
        and expected_sha
        and expected_blob,
        "missing frozen execution authority env",
    )

    need(
        repository["head"] == expected_head,
        "frozen recovery HEAD mismatch",
    )

    worktree_bytes = RUNNER.read_bytes()

    head_bytes = headbytes(
        RUNNER_REL
    )

    need(
        worktree_bytes == head_bytes
        and hbytes(worktree_bytes) == expected_sha
        and hbytes(head_bytes) == expected_sha,
        "runner SHA/HEAD mismatch",
    )

    need(
        blob(RUNNER_REL) == expected_blob,
        "runner blob mismatch",
    )

    sentinel = (
        Path.home()
        / ".openmind_authoritative_slots"
        / (
            "phase_6e_d_partial_state_recovery_"
            f"{expected_head}.spent"
        )
    )

    reg(
        sentinel,
        "recovery sentinel",
    )

    expected = canon(
        {
            "branch": BRANCH,
            "head": expected_head,
            "purpose":
                "phase_6e_d_partial_state_recovery",
            "protocol_sha256":
                PROTO_SHA,
            "runner_git_blob":
                expected_blob,
            "runner_path":
                RUNNER_REL,
            "runner_sha256":
                expected_sha,
            "schema":
                "openmind."
                "phase_6e_d_partial_state_recovery_slot.v1",
        }
    ) + b"\n"

    raw = sentinel.read_bytes()

    need(
        raw == expected,
        "recovery sentinel content mismatch",
    )

    return {
        "head": expected_head,
        "sha": expected_sha,
        "blob": expected_blob,
        "sentinel": str(sentinel),
        "sentinel_sha": hbytes(raw),
    }


def frozen():
    for path, expected_sha in FROZEN.items():
        reg(
            path,
            "frozen authority",
        )

        need(
            hfile(path) == expected_sha,
            "frozen SHA mismatch " + str(path),
        )

    need(
        blob(ORIG_REL) == ORIG_BLOB,
        "original runner blob mismatch",
    )

    reg(
        ORIG_SENT,
        "original spent sentinel",
    )

    need(
        hfile(ORIG_SENT) == ORIG_SENT_SHA,
        "original sentinel SHA mismatch",
    )


def maps():
    inventory = load(INV)
    identity = load(IDENT)
    recipe_doc = load(RECIPES)

    tensors = inventory.get("tensors")
    objects = identity.get("objects")
    recipes = recipe_doc.get("recipes")
    model = identity.get("model")

    need(
        isinstance(tensors, list)
        and len(tensors) == N,
        "inventory count",
    )

    need(
        isinstance(objects, list)
        and len(objects) == N,
        "identity count",
    )

    need(
        isinstance(recipes, list)
        and len(recipes) == N,
        "recipe count",
    )

    need(
        isinstance(model, dict)
        and model.get("pk") == MODEL_PK,
        "model PK",
    )

    inventory_by_name = {}
    identity_by_name = {}
    recipe_by_name = {}
    pks = set()

    for row in tensors:
        name = row.get("name")

        need(
            isinstance(name, str)
            and name
            and name not in inventory_by_name,
            "inventory name",
        )

        inventory_by_name[name] = row

    for row in objects:
        name = row.get(
            "tensor_name"
        )

        need(
            isinstance(name, str)
            and name
            and name not in identity_by_name,
            "identity name",
        )

        object_pk = pk(row)

        need(
            object_pk not in pks,
            "duplicate identity PK",
        )

        pks.add(
            object_pk
        )

        identity_by_name[name] = row

    for row in recipes:
        name = row.get("name")

        need(
            isinstance(name, str)
            and name
            and name not in recipe_by_name,
            "recipe name",
        )

        recipe_by_name[name] = row

    need(
        set(inventory_by_name)
        == set(identity_by_name)
        == set(recipe_by_name),
        "authority name sets differ",
    )

    for name, identity_row in identity_by_name.items():
        object_pk = pk(
            identity_row
        )

        inventory_row = inventory_by_name[
            name
        ]

        recipe = recipe_by_name[
            name
        ]

        need(
            recipe.get("object_pk") == object_pk
            and recipe.get("model_pk") == MODEL_PK,
            "recipe PK/model",
        )

        need(
            recipe.get("tensor_type")
            == identity_row.get("tensor_type")
            and tuple(
                recipe.get(
                    "dims",
                    [],
                )
            )
            == tuple(
                identity_row.get(
                    "dims",
                    [],
                )
            ),
            "recipe metadata",
        )

        need(
            inventory_row.get("type")
            == identity_row.get("tensor_type")
            and tuple(
                inventory_row.get(
                    "dims",
                    [],
                )
            )
            == tuple(
                identity_row.get(
                    "dims",
                    [],
                )
            ),
            "inventory metadata",
        )

        need(
            inventory_row.get("payload_sha256")
            == identity_row.get("payload_sha256"),
            "payload authority",
        )

    return (
        inventory_by_name,
        identity_by_name,
        recipe_by_name,
        pks,
    )


def manifest():
    raw = BM.read_bytes()

    need(
        hbytes(raw) == SM_SHA,
        "segment manifest SHA",
    )

    value = json.loads(
        raw.decode("utf-8")
    )

    need(
        canon(value) == raw,
        "segment manifest noncanonical",
    )

    need(
        set(value)
        == {
            "schema",
            "builder_version",
            "placement_policy",
            "model_pk",
            "object_count",
            "segment_length",
            "segment_sha256",
            "objects",
        },
        "manifest fields",
    )

    need(
        value["schema"]
        == "openmind.maf_segment_manifest.v1"
        and value["builder_version"]
        == "maf_segment_builder_v1",
        "manifest schema/version",
    )

    need(
        value["placement_policy"]
        == "sequential_exact_object_pack"
        and value["model_pk"] == MODEL_PK,
        "manifest policy/model",
    )

    need(
        value["object_count"] == N
        and value["segment_length"] == SEG_LEN
        and value["segment_sha256"] == SEG_SHA,
        "manifest cardinality/segment",
    )

    rows = value["objects"]

    need(
        isinstance(rows, list)
        and len(rows) == N,
        "placement count",
    )

    by_pk = {}
    cursor = 0

    for ordinal, row in enumerate(rows):
        need(
            set(row)
            == {
                "ordinal",
                "object_pk",
                "offset",
                "length",
                "object_file_sha256",
                "payload_sha256",
            },
            "placement fields",
        )

        need(
            row["ordinal"] == ordinal
            and type(row["offset"]) is int
            and type(row["length"]) is int
            and row["offset"] == cursor
            and row["length"] > 0,
            "placement geometry",
        )

        object_pk = row[
            "object_pk"
        ]

        need(
            isinstance(object_pk, str)
            and object_pk.startswith("mafobj:v1:")
            and object_pk not in by_pk,
            "placement PK",
        )

        need(
            row["offset"]
            + row["length"]
            <= SEG_LEN,
            "placement bounds",
        )

        by_pk[
            object_pk
        ] = row

        cursor = (
            row["offset"]
            + row["length"]
        )

    need(
        cursor == SEG_LEN
        and len(by_pk) == N,
        "placement coverage",
    )

    return raw, by_pk


def qualify_objects(
    by_pk,
    inventory_by_name,
    identity_by_name,
    recipe_by_name,
    pks,
):
    direc(
        OD,
        "object store",
    )

    with os.scandir(OD) as iterator:
        entries = list(
            iterator
        )

    regular = []
    partial = 0
    symlinks = 0
    other = 0

    for entry in entries:
        if entry.is_symlink():
            symlinks += 1

        elif entry.name.endswith(
            ".partial"
        ):
            partial += 1

        elif entry.is_file(
            follow_symlinks=False
        ):
            regular.append(
                Path(entry.path)
            )

        else:
            other += 1

    need(
        len(regular) == N
        and partial == 0
        and symlinks == 0
        and other == 0,
        "object-store shape",
    )

    need(
        sum(
            path.stat().st_size
            for path in regular
        )
        == SEG_LEN,
        "object aggregate bytes",
    )

    authority = {}
    names = set()

    for path in regular:
        reg(
            path,
            "serialized object",
        )

        view = obj.inspect_object(
            path,
            chunk_bytes=CHUNK,
        )

        name = view.tensor_name

        need(
            name in identity_by_name
            and name in inventory_by_name
            and name in recipe_by_name
            and name not in names,
            "object tensor mapping",
        )

        object_pk = pk(
            identity_by_name[
                name
            ]
        )

        need(
            object_pk in pks
            and object_pk in by_pk
            and object_pk not in authority,
            "object PK mapping",
        )

        placement = by_pk[
            object_pk
        ]

        serialized_sha = hfile(
            path
        )

        inventory_row = inventory_by_name[
            name
        ]

        recipe = recipe_by_name[
            name
        ]

        need(
            serialized_sha
            == placement["object_file_sha256"]
            and path.stat().st_size
            == placement["length"],
            "object file authority",
        )

        need(
            view.tensor_type
            == identity_by_name[
                name
            ].get("tensor_type")
            and tuple(view.dims)
            == tuple(
                identity_by_name[
                    name
                ].get(
                    "dims",
                    [],
                )
            ),
            "object identity metadata",
        )

        need(
            view.element_count
            == inventory_row.get("elements")
            and view.payload_length
            == inventory_row.get("span_bytes"),
            "object length/elements",
        )

        need(
            view.payload_sha256
            == inventory_row.get("payload_sha256")
            == identity_by_name[
                name
            ].get("payload_sha256")
            == placement["payload_sha256"],
            "object payload SHA",
        )

        need(
            recipe.get("object_pk")
            == object_pk
            and recipe.get("tensor_type")
            == view.tensor_type
            and tuple(
                recipe.get(
                    "dims",
                    [],
                )
            )
            == tuple(view.dims),
            "object recipe binding",
        )

        authority[
            object_pk
        ] = {
            "name": name,
            "type": view.tensor_type,
            "dims": tuple(view.dims),
            "plen": view.payload_length,
            "psha": view.payload_sha256,
            "osha": serialized_sha,
        }

        names.add(
            name
        )

    need(
        set(authority) == pks
        and names == set(identity_by_name),
        "qualified object set",
    )

    return authority


def inspect_bytes(serialized):
    header_size = int(
        obj.HEADER_SIZE
    )

    need(
        type(serialized) is bytes
        and len(serialized) >= header_size,
        "serialized bytes",
    )

    header = obj.unpack_header(
        serialized[
            :header_size
        ]
    )

    metadata_start = header_size

    metadata_end = (
        metadata_start
        + int(
            header[
                "metadata_length"
            ]
        )
    )

    payload_end = (
        metadata_end
        + int(
            header[
                "payload_length"
            ]
        )
    )

    need(
        payload_end == len(serialized)
        and metadata_end >= metadata_start,
        "serialized ranges",
    )

    metadata_raw = serialized[
        metadata_start:
        metadata_end
    ]

    need(
        hbytes(metadata_raw)
        == header[
            "metadata_sha256"
        ],
        "metadata SHA",
    )

    metadata = json.loads(
        metadata_raw.decode(
            "utf-8"
        )
    )

    need(
        isinstance(metadata, dict)
        and obj.canonical_json_bytes(
            metadata
        )
        == metadata_raw,
        "metadata canonical",
    )

    obj.validate_metadata(
        metadata,
        header,
    )

    payload_sha = hbytes(
        memoryview(
            serialized
        )[
            metadata_end:
            payload_end
        ]
    )

    need(
        payload_sha
        == header[
            "payload_sha256"
        ],
        "payload SHA",
    )

    return {
        "name": metadata[
            "tensor_name"
        ],
        "type": metadata[
            "tensor_type"
        ],
        "dims": tuple(
            metadata[
                "dims"
            ]
        ),
        "plen": int(
            header[
                "payload_length"
            ]
        ),
        "psha": payload_sha,
    }


def placements(
    by_pk,
    pks,
    segment_path,
):
    output = [
        {
            "model_pk":
                MODEL_PK,
            "object_pk":
                object_pk,
            "segment_path":
                str(segment_path),
            "offset":
                by_pk[
                    object_pk
                ]["offset"],
            "length":
                by_pk[
                    object_pk
                ]["length"],
            "object_file_sha256":
                by_pk[
                    object_pk
                ][
                    "object_file_sha256"
                ],
            "payload_sha256":
                by_pk[
                    object_pk
                ][
                    "payload_sha256"
                ],
        }
        for object_pk in sorted(
            pks
        )
    ]

    need(
        len(output) == N
        and {
            row["object_pk"]
            for row in output
        }
        == pks,
        "reconstructed placements",
    )

    return output


def generation(
    value,
    pks,
):
    generation_pk = gen.verify_manifest(
        value
    )

    descriptor = value.get(
        "descriptor"
    )

    need(
        isinstance(descriptor, dict)
        and descriptor.get(
            "model_pk"
        )
        == MODEL_PK,
        "generation descriptor",
    )

    segments = descriptor.get(
        "segments"
    )

    objects = descriptor.get(
        "objects"
    )

    need(
        isinstance(segments, list)
        and len(segments) == 1
        and isinstance(objects, list)
        and len(objects) == N,
        "generation cardinality",
    )

    segment = segments[
        0
    ]

    need(
        segment.get(
            "segment_id"
        )
        == "segment:00000000"
        and segment.get(
            "segment_length"
        )
        == SEG_LEN
        and segment.get(
            "segment_sha256"
        )
        == SEG_SHA,
        "generation segment",
    )

    locator_pks = []

    for row in objects:
        need(
            set(row)
            == {
                "object_pk",
                "segment_id",
                "offset",
                "length",
                "object_file_sha256",
                "payload_sha256",
            }
            and row.get(
                "segment_id"
            )
            == "segment:00000000",
            "locator",
        )

        locator_pks.append(
            row[
                "object_pk"
            ]
        )

    need(
        len(
            set(locator_pks)
        )
        == N
        and set(locator_pks)
        == pks,
        "locator PKs",
    )

    return (
        generation_pk,
        segments,
        objects,
    )


def readback(
    value,
    manifest_path,
    segment_path,
    root,
    authority,
    identity_by_name,
    recipe_by_name,
    pks,
):
    (
        generation_pk,
        segments,
        objects,
    ) = generation(
        value,
        pks,
    )

    manifest_sha = hfile(
        manifest_path
    )

    segment_by_id = {
        row[
            "segment_id"
        ]: row
        for row in segments
    }

    seen = set()

    for locator in objects:
        object_pk = locator[
            "object_pk"
        ]

        need(
            object_pk not in seen
            and object_pk in authority,
            "readback PK",
        )

        object_authority = authority[
            object_pk
        ]

        segment_id = locator[
            "segment_id"
        ]

        segment_authority = segment_by_id[
            segment_id
        ]

        need(
            locator[
                "object_file_sha256"
            ]
            == object_authority[
                "osha"
            ]
            and locator[
                "payload_sha256"
            ]
            == object_authority[
                "psha"
            ],
            "locator authority",
        )

        entry = resident.ResidentPKEntry(
            model_pk=
                MODEL_PK,
            generation_pk=
                generation_pk,
            generation_manifest_sha256=
                manifest_sha,
            object_pk=
                object_pk,
            segment_id=
                segment_id,
            offset=
                locator[
                    "offset"
                ],
            length=
                locator[
                    "length"
                ],
            object_file_sha256=
                locator[
                    "object_file_sha256"
                ],
            payload_sha256=
                locator[
                    "payload_sha256"
                ],
            segment_length=
                segment_authority[
                    "segment_length"
                ],
            segment_sha256=
                segment_authority[
                    "segment_sha256"
                ],
            segment_path=
                str(
                    segment_path
                ),
        )

        serialized = (
            reader.read_serialized_object(
                entry,
                generation_pk,
            )
        )

        need(
            type(serialized) is bytes
            and len(serialized)
            == entry.length
            and hbytes(serialized)
            == entry.object_file_sha256,
            "segment read",
        )

        decoded = inspect_bytes(
            serialized
        )

        need(
            decoded["name"]
            == object_authority["name"]
            and decoded["type"]
            == object_authority["type"]
            and decoded["dims"]
            == object_authority["dims"]
            and decoded["plen"]
            == object_authority["plen"]
            and decoded["psha"]
            == object_authority["psha"],
            "decoded authority",
        )

        identity = identity_by_name[
            decoded[
                "name"
            ]
        ]

        need(
            pk(identity)
            == object_pk
            and recipe_by_name[
                decoded[
                    "name"
                ]
            ].get(
                "object_pk"
            )
            == object_pk,
            "decoded PK binding",
        )

        need(
            decoded["type"]
            == identity.get(
                "tensor_type"
            )
            and decoded["dims"]
            == tuple(
                identity.get(
                    "dims",
                    [],
                )
            )
            and decoded["psha"]
            == identity.get(
                "payload_sha256"
            ),
            "decoded frozen identity",
        )

        need(
            Path(
                entry.segment_path
            ).resolve().parent
            == root.resolve(),
            "locator confinement",
        )

        seen.add(
            object_pk
        )

        del decoded
        del serialized

    need(
        seen == pks,
        "readback set",
    )

    return len(
        seen
    )


def publish(
    path,
    value,
):
    raw = (
        canon(value)
        + b"\n"
    )

    partial = path.with_name(
        path.name
        + ".partial"
    )

    need(
        not path.exists()
        and not partial.exists(),
        "recovery result exists",
    )

    with partial.open(
        "xb"
    ) as handle:
        handle.write(
            raw
        )

        handle.flush()

        os.fsync(
            handle.fileno()
        )

    need(
        partial.read_bytes()
        == raw,
        "result partial readback",
    )

    os.link(
        partial,
        path,
    )

    os.unlink(
        partial
    )

    directory_fd = os.open(
        path.parent,
        os.O_RDONLY,
    )

    try:
        os.fsync(
            directory_fd
        )

    finally:
        os.close(
            directory_fd
        )

    need(
        path.read_bytes()
        == raw,
        "result final readback",
    )

    return hfile(
        path
    )


def main():
    print(
        "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
    )
    print(
        "PHASE 6E-D — PARTIAL-STATE RECOVERY EXECUTION"
    )

    before = repo()

    authority = slot_gate(
        before
    )

    frozen()

    print(
        "[ RCV01 ] "
        "frozen repository/runner/protocol/original sentinel: PASS"
    )

    direc(
        B,
        "building runtime",
    )

    direc(
        OD,
        "object store",
    )

    need(
        not F.exists(),
        "final runtime exists",
    )

    reg(
        BS,
        "segment",
    )

    reg(
        BM,
        "segment manifest",
    )

    need(
        BS.stat().st_size
        == SEG_LEN,
        "segment stat",
    )

    need(
        not BG.exists()
        and not BGP.exists()
        and not BR.exists()
        and not BRP.exists(),
        "preexisting recovery output",
    )

    with os.scandir(OD) as iterator:
        entries = list(
            iterator
        )

    regular_count = sum(
        1
        for entry in entries
        if not entry.is_symlink()
        and not entry.name.endswith(
            ".partial"
        )
        and entry.is_file(
            follow_symlinks=False
        )
    )

    partial_count = sum(
        1
        for entry in entries
        if entry.name.endswith(
            ".partial"
        )
    )

    symlink_count = sum(
        1
        for entry in entries
        if entry.is_symlink()
    )

    need(
        regular_count == N,
        "regular object count",
    )

    need(
        partial_count == 0
        and symlink_count == 0,
        "partial/symlink count",
    )

    need(
        len(entries) == N,
        "unexpected object-store entry",
    )

    need(
        sorted(
            B.glob(
                "segment_*.mafseg"
            )
        )
        == [BS]
        and sorted(
            B.glob(
                "segment_*.manifest.json"
            )
        )
        == [BM],
        "segment/manifest cardinality",
    )

    print(
        "[ RCV02 ] preserved building state: PASS"
    )

    manifest_raw, by_pk = manifest()

    (
        inventory_by_name,
        identity_by_name,
        recipe_by_name,
        pks,
    ) = maps()

    need(
        set(by_pk) == pks,
        "manifest/frozen PK set",
    )

    print(
        "[ RCV03 ] 339 unique manifest placements: PASS"
    )

    print(
        "[ RCV04 ] source GGUF/rematerialization: NO"
    )

    object_authority = (
        qualify_objects(
            by_pk,
            inventory_by_name,
            identity_by_name,
            recipe_by_name,
            pks,
        )
    )

    print(
        "[ RCV05 ] "
        "339 preserved objects qualified: PASS"
    )

    need(
        hfile(BS) == SEG_SHA
        and BS.stat().st_size
        == SEG_LEN,
        "segment cryptographic authority",
    )

    print(
        "[ RCV06 ] "
        "full segment authority: PASS; "
        "range hashes delegated to frozen generation engine"
    )

    placement_rows = placements(
        by_pk,
        pks,
        BS,
    )

    print(
        "[ RCV07 ] "
        "manifest-only placement reconstruction: PASS"
    )

    segment_record = {
        "segment_path":
            str(BS),
        "segment_length":
            SEG_LEN,
        "segment_sha256":
            SEG_SHA,
    }

    generation_result = (
        gen.build_generation(
            model_pk=
                MODEL_PK,
            segments=[
                segment_record
            ],
            objects=
                placement_rows,
            manifest_path=
                BG,
            chunk_bytes=
                CHUNK,
        )
    )

    generation_value = (
        gen.reopen_candidate_manifest(
            BG
        )
    )

    (
        generation_pk,
        generation_segments,
        generation_objects,
    ) = generation(
        generation_value,
        pks,
    )

    need(
        generation_result.generation_pk
        == generation_pk,
        "generation PK reopen",
    )

    print(
        "[ RCV06 ] "
        "frozen generation-engine full/range hashes: PASS"
    )

    print(
        "[ RCV08 ] "
        "generation manifest + 339 strong locators: PASS"
    )

    print(
        "[ RCV09 ] deterministic generation PK:",
        generation_pk,
    )

    pre_readback = readback(
        generation_value,
        BG,
        BS,
        B,
        object_authority,
        identity_by_name,
        recipe_by_name,
        pks,
    )

    need(
        pre_readback == N,
        "pre-readback count",
    )

    print(
        "[ RCV10 ] "
        "pre-promotion readback 339/339: PASS"
    )

    need(
        not F.exists()
        and BS.is_file()
        and BM.is_file()
        and BG.is_file()
        and not BR.exists(),
        "no-overwrite boundary",
    )

    print(
        "[ RCV11 ] "
        "create-once/no-overwrite boundary: PASS"
    )

    building_fd = os.open(
        B,
        os.O_RDONLY,
    )

    try:
        os.fsync(
            building_fd
        )

    finally:
        os.close(
            building_fd
        )

    os.rename(
        B,
        F,
    )

    runtime_fd = os.open(
        RP,
        os.O_RDONLY,
    )

    try:
        os.fsync(
            runtime_fd
        )

    finally:
        os.close(
            runtime_fd
        )

    need(
        not B.exists(),
        "building remained after rename",
    )

    direc(
        F,
        "final runtime",
    )

    reg(
        FS,
        "final segment",
    )

    reg(
        FM,
        "final manifest",
    )

    reg(
        FG,
        "final generation",
    )

    need(
        hfile(FM) == SM_SHA
        and hfile(FS) == SEG_SHA,
        "post-promotion authority",
    )

    print(
        "[ RCV12 ] one atomic os.rename promotion: PASS"
    )

    generation_after = (
        gen.reopen_candidate_manifest(
            FG
        )
    )

    need(
        generation_after
        == generation_value,
        "generation changed on promotion",
    )

    post_readback = readback(
        generation_after,
        FG,
        FS,
        F,
        object_authority,
        identity_by_name,
        recipe_by_name,
        pks,
    )

    need(
        post_readback == N,
        "post-readback count",
    )

    print(
        "[ RCV13 ] "
        "post-promotion readback 339/339: PASS"
    )

    after = repo()

    need(
        after["status"]
        == before["status"]
        and after["head"]
        == before["head"],
        "Git state changed",
    )

    print(
        "[ RCV14 ] "
        "tracked/index/untracked baseline invariant: PASS"
    )

    print(
        "[ RCV15 ] "
        "inference/network/source-GGUF/performance activity: NO"
    )

    result = {
        "schema":
            "openmind."
            "maf_phase_6e_d_partial_state_recovery.v1",

        "verdict":
            "RECOVERED COMPLETE-MODEL "
            "PERSISTENT GENERATION QUALIFIED",

        "recovery_protocol_sha256":
            PROTO_SHA,

        "recovery_runner_head":
            authority[
                "head"
            ],

        "recovery_runner_sha256":
            authority[
                "sha"
            ],

        "recovery_runner_git_blob":
            authority[
                "blob"
            ],

        "recovery_execution_sentinel":
            authority[
                "sentinel"
            ],

        "recovery_execution_sentinel_sha256":
            authority[
                "sentinel_sha"
            ],

        "original_failed_run_head":
            FAILED_HEAD,

        "original_spent_sentinel":
            str(
                ORIG_SENT
            ),

        "original_spent_sentinel_sha256":
            ORIG_SENT_SHA,

        "segment_manifest_sha256":
            SM_SHA,

        "segment_sha256":
            SEG_SHA,

        "model_pk":
            MODEL_PK,

        "generation_pk":
            generation_pk,

        "object_count":
            N,

        "unique_object_pk_count":
            len(pks),

        "strong_locator_count":
            len(
                generation_objects
            ),

        "object_store_qualification_count":
            len(
                object_authority
            ),

        "pre_promotion_segment_reader_readback_count":
            pre_readback,

        "post_promotion_segment_reader_readback_count":
            post_readback,

        "payload_authority_match_count":
            len(
                object_authority
            ),

        "pg14_repository_state": {
            "branch":
                after[
                    "branch"
                ],

            "head":
                after[
                    "head"
                ],

            "tracked_worktree_clean":
                True,

            "index_empty":
                True,

            "untracked_count":
                after[
                    "n"
                ],

            "untracked_set_sha256":
                after[
                    "usha"
                ],
        },

        "no_source_gguf_access":
            True,

        "no_object_rematerialization":
            True,

        "no_segment_rematerialization":
            True,

        "no_network_access":
            True,

        "no_inference_or_output_parity_science":
            True,

        "gates": {
            f"RCV{i:02d}":
                True
            for i in range(
                1,
                16,
            )
        },
    }

    result_sha = publish(
        FR,
        result,
    )

    final = repo()

    need(
        final["status"]
        == before["status"]
        and final["head"]
        == before["head"],
        "Git changed after result",
    )

    print(
        "[ FINAL GOLD STANDARD SELF-CHECK ] "
        "RCV01-RCV15: PASS"
    )

    print(
        "🟨📦 ===== GOLD STANDARD RETURN PACKET ===== 📦🟨"
    )

    print(
        "STATUS             : "
        "PHASE 6E-D PARTIAL-STATE RECOVERY COMPLETE"
    )

    print(
        "GATE FAILURE       : NONE"
    )

    print(
        "VERDICT            : "
        "RECOVERED COMPLETE-MODEL "
        "PERSISTENT GENERATION QUALIFIED"
    )

    print(
        "HEAD               :",
        final[
            "head"
        ],
    )

    print(
        "RUNNER SHA         :",
        authority[
            "sha"
        ],
    )

    print(
        "RUNNER BLOB        :",
        authority[
            "blob"
        ],
    )

    print(
        "GENERATION PK      :",
        generation_pk,
    )

    print(
        "OBJECT COUNT       :",
        N,
    )

    print(
        "PRE READBACK       :",
        pre_readback,
    )

    print(
        "POST READBACK      :",
        post_readback,
    )

    print(
        "RESULT SHA         :",
        result_sha,
    )

    print(
        "RCV01-RCV15        : PASS"
    )

    print(
        "GGUF ACCESSED      : NO"
    )

    print(
        "NETWORK ACCESS     : NO"
    )

    print(
        "PHASE 6E-D SCIENCE : "
        "STILL BLOCKED PENDING RECOVERY EVIDENCE REVIEW"
    )

    print(
        "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(
            main()
        )

    except Exception as exc:
        print(
            "🟨📦 ===== GOLD STANDARD RETURN PACKET ===== 📦🟨"
        )

        print(
            "STATUS             : "
            "PHASE 6E-D PARTIAL-STATE RECOVERY FAILED"
        )

        print(
            "GATE FAILURE       :",
            type(exc).__name__
            + ":",
            exc,
        )

        print(
            "VERDICT            : "
            "PARTIAL-STATE RECOVERY NOT QUALIFIED"
        )

        print(
            "AUTOMATIC ROLLBACK : NO"
        )

        print(
            "AUTOMATIC RERUN    : NO"
        )

        print(
            "RECOVERY SENTINEL  : MUST REMAIN SPENT"
        )

        print(
            "NEXT ACTION        : "
            "READ-ONLY DIAGNOSIS REQUIRED"
        )

        print(
            "🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨"
        )

        raise SystemExit(
            1
        )
