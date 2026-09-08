# OpenMind Phase 6E-D Class-A MAF-backed tensor provider V1.
#
# Construction authority only.
#
# This module implements the frozen provider callback contract. It does not
# invoke llama_model_init_from_user, load a model, open a source GGUF, or run
# inference. A later qualified bridge must invoke the user-init API and must
# call model_acceptance_gate immediately after that API returns and before a
# returned model handle is accepted for any use.

from __future__ import annotations

import ctypes
import hashlib
import json
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import maf_object_v1 as maf_object
import maf_resident_pk_directory_v1 as resident
import maf_segment_reader_v1 as segment_reader


SCHEMA = "openmind.maf_phase_6e_d_class_a_maf_backed_tensor_provider.v1"

EXPECTED_MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
EXPECTED_GENERATION_PK = "mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2"
EXPECTED_GENERATION_MANIFEST_SHA256 = "a79b012f10904a5e0540076a8443007344ada4e11e3846d817201b43583fedff"

PROVIDER_CONTRACT_SHA256 = "2782678c5153761e028f29f35d7275b019590af5a35391ea967c71c027c2ebb2"
JOIN_AUTHORITY_SHA256 = "34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709"
METADATA_AUTHORITY_SHA256 = "bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966"

EXPECTED_TENSOR_COUNT = 339
EXPECTED_MAF_HEADER_SIZE = 96
EXPECTED_GGML_MAX_DIMS = 4

_REPO_ROOT = Path(__file__).resolve().parents[2]

_PROVIDER_CONTRACT_PATH = (
    _REPO_ROOT
    / "experiments/model_fractal/MAF_PHASE_6E_D_CLASS_A_MAF_BACKED_TENSOR_PROVIDER_CONTRACT_V1.md"
)

_JOIN_AUTHORITY_PATH = (
    _REPO_ROOT
    / "experiments/model_fractal/maf_phase_6e_d_class_a_tensor_object_segment_join_v1.json"
)

_METADATA_AUTHORITY_PATH = (
    _REPO_ROOT
    / "experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json"
)


class ClassAProviderError(RuntimeError):
    pass


class ClassAProviderAuthorityError(ClassAProviderError):
    pass


class ClassAProviderTensorError(ClassAProviderError):
    pass


class ClassAProviderResidentError(ClassAProviderError):
    pass


class ClassAProviderObjectError(ClassAProviderError):
    pass


class ClassAProviderTransferError(ClassAProviderError):
    pass


class ClassAProviderInitializationError(ClassAProviderError):
    pass


class ClassAProviderFailureStateError(ClassAProviderError):
    pass


@dataclass
class ProviderState:
    callback_count: int = 0
    resolved_count: int = 0
    transfer_count: int = 0
    unique_callback_names: set[str] = field(default_factory=set)
    callback_name_counts: dict[str, int] = field(default_factory=dict)
    duplicate_name_counts: dict[str, int] = field(default_factory=dict)
    resolution_results: list[dict[str, Any]] = field(default_factory=list)
    failed: bool = False
    failure_tensor: str | None = None
    failure_type: str | None = None
    failure_message: str | None = None


class _GGMLTensorPrefix(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("buffer", ctypes.c_void_p),
        ("ne", ctypes.c_int64 * EXPECTED_GGML_MAX_DIMS),
    ]


class _LlamaModelParams(ctypes.Structure):
    _fields_ = [
        ("devices", ctypes.c_void_p),
        ("tensor_buft_overrides", ctypes.c_void_p),
        ("n_gpu_layers", ctypes.c_int32),
        ("split_mode", ctypes.c_int),
        ("load_mode", ctypes.c_int),
        ("main_gpu", ctypes.c_int32),
        ("tensor_split", ctypes.c_void_p),
        ("progress_callback", ctypes.c_void_p),
        ("progress_callback_user_data", ctypes.c_void_p),
        ("kv_overrides", ctypes.c_void_p),
        ("vocab_only", ctypes.c_bool),
        ("check_tensors", ctypes.c_bool),
        ("use_extra_bufts", ctypes.c_bool),
        ("no_host", ctypes.c_bool),
        ("no_alloc", ctypes.c_bool),
        ("load_mtp", ctypes.c_bool),
    ]


_LLAMA_SET_TENSOR_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p,
    ctypes.c_void_p,
)


_PY_BYTES_AS_STRING = ctypes.pythonapi.PyBytes_AsString
_PY_BYTES_AS_STRING.argtypes = [ctypes.py_object]
_PY_BYTES_AS_STRING.restype = ctypes.c_void_p


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _read_frozen_json(
    path: Path,
    expected_sha256: str,
) -> dict[str, Any]:
    if not path.is_file():
        raise ClassAProviderAuthorityError(
            "frozen authority is not a regular file: "
            + str(path)
        )

    observed_sha256 = _sha256_file(path)

    if observed_sha256 != expected_sha256:
        raise ClassAProviderAuthorityError(
            "frozen authority SHA256 mismatch: "
            + str(path)
        )

    raw = path.read_bytes()

    try:
        value = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        raise ClassAProviderAuthorityError(
            "frozen authority JSON decode failed: "
            + str(path)
        ) from exc

    if not isinstance(value, dict):
        raise ClassAProviderAuthorityError(
            "frozen authority root is not an object: "
            + str(path)
        )

    if _canonical_json_bytes(value) != raw:
        raise ClassAProviderAuthorityError(
            "frozen authority is not canonical JSON: "
            + str(path)
        )

    return value


def _require_plain_int(
    name: str,
    value: Any,
) -> int:
    if type(value) is not int:
        raise ClassAProviderAuthorityError(
            name + " must be a plain int"
        )

    return value


def _require_nonempty_text(
    name: str,
    value: Any,
) -> str:
    if not isinstance(value, str) or not value:
        raise ClassAProviderAuthorityError(
            name + " must be a non-empty string"
        )

    return value


class ClassAMAFBackedTensorProvider:
    def __init__(
        self,
        *,
        directory: resident.ResidentPKDirectory,
        ggml_library: Any,
    ) -> None:
        if not isinstance(
            directory,
            resident.ResidentPKDirectory,
        ):
            raise ClassAProviderAuthorityError(
                "directory must be ResidentPKDirectory"
            )

        if resident.OBJECT_PK_KIND != "object_pk":
            raise ClassAProviderAuthorityError(
                "resident OBJECT_PK_KIND mismatch"
            )

        if maf_object.HEADER_SIZE != EXPECTED_MAF_HEADER_SIZE:
            raise ClassAProviderAuthorityError(
                "MAF HEADER_SIZE mismatch"
            )

        self._directory = directory
        self._ggml_library = ggml_library
        self._state = ProviderState()
        self._state_lock = threading.Lock()
        self._initialization_started = False

        self._bind_ggml_api()
        self._load_and_validate_authorities()

        self._callback = _LLAMA_SET_TENSOR_CALLBACK(
            self._callback_entry
        )

    @property
    def callback(self) -> Any:
        return self._callback

    @property
    def userdata(self) -> ctypes.c_void_p:
        return ctypes.c_void_p()

    @property
    def state(self) -> ProviderState:
        return self._state

    def _bind_ggml_api(self) -> None:
        required = (
            "ggml_get_name",
            "ggml_nelements",
            "ggml_nbytes",
            "ggml_backend_tensor_set",
            "llama_model_default_params",
            "llama_model_init_from_user",
            "llama_model_free",
        )

        for name in required:
            if not hasattr(
                self._ggml_library,
                name,
            ):
                raise ClassAProviderAuthorityError(
                    "required GGML symbol missing: "
                    + name
                )

        self._ggml_get_name = (
            self._ggml_library.ggml_get_name
        )
        self._ggml_get_name.argtypes = [
            ctypes.c_void_p
        ]
        self._ggml_get_name.restype = (
            ctypes.c_char_p
        )

        self._ggml_nelements = (
            self._ggml_library.ggml_nelements
        )
        self._ggml_nelements.argtypes = [
            ctypes.c_void_p
        ]
        self._ggml_nelements.restype = (
            ctypes.c_int64
        )

        self._ggml_nbytes = (
            self._ggml_library.ggml_nbytes
        )
        self._ggml_nbytes.argtypes = [
            ctypes.c_void_p
        ]
        self._ggml_nbytes.restype = (
            ctypes.c_size_t
        )

        self._ggml_backend_tensor_set = (
            self._ggml_library.ggml_backend_tensor_set
        )
        self._ggml_backend_tensor_set.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_size_t,
        ]
        self._ggml_backend_tensor_set.restype = (
            None
        )

        self._llama_model_default_params = (
            self._ggml_library.llama_model_default_params
        )
        self._llama_model_default_params.argtypes = []
        self._llama_model_default_params.restype = (
            _LlamaModelParams
        )

        self._llama_model_init_from_user = (
            self._ggml_library.llama_model_init_from_user
        )
        self._llama_model_init_from_user.argtypes = [
            ctypes.c_void_p,
            _LLAMA_SET_TENSOR_CALLBACK,
            ctypes.c_void_p,
            _LlamaModelParams,
        ]
        self._llama_model_init_from_user.restype = (
            ctypes.c_void_p
        )

        self._llama_model_free = (
            self._ggml_library.llama_model_free
        )
        self._llama_model_free.argtypes = [
            ctypes.c_void_p
        ]
        self._llama_model_free.restype = None

    def _load_and_validate_authorities(
        self,
    ) -> None:
        if not _PROVIDER_CONTRACT_PATH.is_file():
            raise ClassAProviderAuthorityError(
                "provider contract is absent"
            )

        if (
            _sha256_file(
                _PROVIDER_CONTRACT_PATH
            )
            != PROVIDER_CONTRACT_SHA256
        ):
            raise ClassAProviderAuthorityError(
                "provider contract SHA256 mismatch"
            )

        join = _read_frozen_json(
            _JOIN_AUTHORITY_PATH,
            JOIN_AUTHORITY_SHA256,
        )

        metadata = _read_frozen_json(
            _METADATA_AUTHORITY_PATH,
            METADATA_AUTHORITY_SHA256,
        )

        if (
            join.get("schema")
            != "openmind.maf_phase_6e_d_class_a_tensor_object_segment_join.v1"
        ):
            raise ClassAProviderAuthorityError(
                "join schema mismatch"
            )

        if (
            metadata.get("schema")
            != "openmind.maf_phase_6e_d_class_a_gguf_metadata_authority.v1"
        ):
            raise ClassAProviderAuthorityError(
                "metadata authority schema mismatch"
            )

        if (
            join.get("model_pk")
            != EXPECTED_MODEL_PK
        ):
            raise ClassAProviderAuthorityError(
                "join model PK mismatch"
            )

        if (
            join.get("generation_pk")
            != EXPECTED_GENERATION_PK
        ):
            raise ClassAProviderAuthorityError(
                "join generation PK mismatch"
            )

        records = join.get("records")
        declarations = metadata.get("tensors")

        if (
            not isinstance(records, list)
            or len(records)
            != EXPECTED_TENSOR_COUNT
        ):
            raise ClassAProviderAuthorityError(
                "join tensor count mismatch"
            )

        if (
            not isinstance(declarations, list)
            or len(declarations)
            != EXPECTED_TENSOR_COUNT
        ):
            raise ClassAProviderAuthorityError(
                "metadata tensor count mismatch"
            )

        declaration_by_name: dict[
            str,
            dict[str, Any],
        ] = {}

        for declaration in declarations:
            if not isinstance(
                declaration,
                dict,
            ):
                raise ClassAProviderAuthorityError(
                    "metadata tensor declaration is not an object"
                )

            name = _require_nonempty_text(
                "metadata tensor name",
                declaration.get("name"),
            )

            if name in declaration_by_name:
                raise ClassAProviderAuthorityError(
                    "duplicate metadata tensor name"
                )

            declaration_by_name[
                name
            ] = declaration

        record_by_name: dict[
            str,
            dict[str, Any],
        ] = {}

        object_pks: set[str] = set()

        for record in records:
            if not isinstance(
                record,
                dict,
            ):
                raise ClassAProviderAuthorityError(
                    "join record is not an object"
                )

            name = _require_nonempty_text(
                "join tensor name",
                record.get("tensor_name"),
            )

            object_pk = _require_nonempty_text(
                "join object PK",
                record.get("object_pk"),
            )

            if name in record_by_name:
                raise ClassAProviderAuthorityError(
                    "duplicate join tensor name"
                )

            if object_pk in object_pks:
                raise ClassAProviderAuthorityError(
                    "duplicate join object PK"
                )

            declaration = (
                declaration_by_name.get(
                    name
                )
            )

            if declaration is None:
                raise ClassAProviderAuthorityError(
                    "join tensor absent from metadata authority"
                )

            for key in (
                "dims",
                "element_count",
                "ggml_type",
                "ggml_type_name",
            ):
                metadata_key = key

                if (
                    declaration.get(
                        metadata_key
                    )
                    != record.get(key)
                ):
                    raise ClassAProviderAuthorityError(
                        "metadata/join disagreement for "
                        + name
                        + ": "
                        + key
                    )

            dims = record.get("dims")

            if (
                not isinstance(dims, list)
                or not dims
                or len(dims)
                > EXPECTED_GGML_MAX_DIMS
            ):
                raise ClassAProviderAuthorityError(
                    "invalid frozen tensor dimensions"
                )

            for dim in dims:
                if (
                    type(dim) is not int
                    or dim <= 0
                ):
                    raise ClassAProviderAuthorityError(
                        "invalid frozen tensor dimension"
                    )

            expected_payload_length = (
                _require_plain_int(
                    "expected_payload_length",
                    record.get(
                        "expected_payload_length"
                    ),
                )
            )

            if expected_payload_length <= 0:
                raise ClassAProviderAuthorityError(
                    "non-positive frozen payload length"
                )

            record_by_name[
                name
            ] = record
            object_pks.add(
                object_pk
            )

        if (
            len(record_by_name)
            != EXPECTED_TENSOR_COUNT
            or len(object_pks)
            != EXPECTED_TENSOR_COUNT
        ):
            raise ClassAProviderAuthorityError(
                "frozen authority cardinality mismatch"
            )

        self._join = join
        self._metadata = metadata
        self._record_by_name = (
            record_by_name
        )

    def _tensor_name(
        self,
        tensor_ptr: ctypes.c_void_p,
    ) -> str:
        raw = self._ggml_get_name(
            tensor_ptr
        )

        if raw is None:
            raise ClassAProviderTensorError(
                "GGML tensor name is null"
            )

        try:
            name = raw.decode("utf-8")
        except Exception as exc:
            raise ClassAProviderTensorError(
                "GGML tensor name is not UTF-8"
            ) from exc

        if not name:
            raise ClassAProviderTensorError(
                "GGML tensor name is empty"
            )

        return name

    def _record_callback(
        self,
        name: str | None,
    ) -> None:
        with self._state_lock:
            self._state.callback_count += 1

            if name is None:
                return

            count = (
                self._state.callback_name_counts.get(
                    name,
                    0,
                )
                + 1
            )

            self._state.callback_name_counts[
                name
            ] = count

            self._state.unique_callback_names.add(
                name
            )

            if count > 1:
                self._state.duplicate_name_counts[
                    name
                ] = count - 1

    def _record_success(
        self,
        *,
        name: str,
        object_pk: str,
        payload_bytes: int,
    ) -> None:
        with self._state_lock:
            self._state.resolved_count += 1
            self._state.transfer_count += 1

            self._state.resolution_results.append(
                {
                    "status": "PASS",
                    "tensor_name": name,
                    "object_pk": object_pk,
                    "payload_bytes": payload_bytes,
                }
            )

    def _record_failure(
        self,
        *,
        name: str | None,
        exc: BaseException,
    ) -> None:
        with self._state_lock:
            if self._state.failed:
                return

            self._state.failed = True
            self._state.failure_tensor = name
            self._state.failure_type = (
                type(exc).__name__
            )
            self._state.failure_message = (
                str(exc)
            )

            self._state.resolution_results.append(
                {
                    "status": "FAIL",
                    "tensor_name": name,
                    "failure_type": (
                        type(exc).__name__
                    ),
                    "failure_message": (
                        str(exc)
                    ),
                }
            )

    def _already_failed(self) -> bool:
        with self._state_lock:
            return self._state.failed

    def _resolve_record(
        self,
        name: str,
    ) -> dict[str, Any]:
        try:
            return self._record_by_name[
                name
            ]
        except KeyError as exc:
            raise ClassAProviderTensorError(
                "callback tensor is absent from frozen authority: "
                + name
            ) from exc

    def _validate_tensor(
        self,
        *,
        tensor_ptr: ctypes.c_void_p,
        name: str,
        record: dict[str, Any],
    ) -> int:
        prefix = ctypes.cast(
            tensor_ptr,
            ctypes.POINTER(
                _GGMLTensorPrefix
            ),
        ).contents

        if not prefix.buffer:
            raise ClassAProviderTensorError(
                "callback tensor has no allocated backend buffer"
            )

        expected_type = _require_plain_int(
            "ggml_type",
            record.get("ggml_type"),
        )

        if int(prefix.type) != expected_type:
            raise ClassAProviderTensorError(
                "GGML tensor type mismatch: "
                + name
            )

        frozen_dims = tuple(
            int(v)
            for v in record["dims"]
        )

        actual_dims = tuple(
            int(prefix.ne[i])
            for i in range(
                len(frozen_dims)
            )
        )

        if actual_dims != frozen_dims:
            raise ClassAProviderTensorError(
                "GGML tensor dimension mismatch: "
                + name
            )

        for i in range(
            len(frozen_dims),
            EXPECTED_GGML_MAX_DIMS,
        ):
            if int(prefix.ne[i]) != 1:
                raise ClassAProviderTensorError(
                    "GGML trailing dimension mismatch: "
                    + name
                )

        actual_elements = int(
            self._ggml_nelements(
                tensor_ptr
            )
        )

        expected_elements = (
            _require_plain_int(
                "element_count",
                record.get(
                    "element_count"
                ),
            )
        )

        if actual_elements != expected_elements:
            raise ClassAProviderTensorError(
                "GGML tensor element-count mismatch: "
                + name
            )

        actual_nbytes = int(
            self._ggml_nbytes(
                tensor_ptr
            )
        )

        expected_nbytes = (
            _require_plain_int(
                "expected_payload_length",
                record.get(
                    "expected_payload_length"
                ),
            )
        )

        if actual_nbytes != expected_nbytes:
            raise ClassAProviderTensorError(
                "GGML tensor byte-span mismatch: "
                + name
            )

        return actual_nbytes

    def _resolve_resident_entry(
        self,
        record: dict[str, Any],
    ) -> resident.ResidentPKEntry:
        object_pk = _require_nonempty_text(
            "object_pk",
            record.get("object_pk"),
        )

        try:
            entry = self._directory.lookup(
                model_pk=EXPECTED_MODEL_PK,
                pk_kind=resident.OBJECT_PK_KIND,
                logical_pk=object_pk,
                expected_generation_pk=(
                    EXPECTED_GENERATION_PK
                ),
            )
        except Exception as exc:
            raise ClassAProviderResidentError(
                "resident object lookup failed: "
                + object_pk
            ) from exc

        if entry.model_pk != EXPECTED_MODEL_PK:
            raise ClassAProviderResidentError(
                "resident model PK mismatch"
            )

        if (
            entry.generation_pk
            != EXPECTED_GENERATION_PK
        ):
            raise ClassAProviderResidentError(
                "resident generation PK mismatch"
            )

        if (
            entry.generation_manifest_sha256
            != EXPECTED_GENERATION_MANIFEST_SHA256
        ):
            raise ClassAProviderResidentError(
                "resident generation-manifest SHA256 mismatch"
            )

        exact_pairs = (
            (
                entry.object_pk,
                record["object_pk"],
                "object PK",
            ),
            (
                entry.segment_id,
                record["segment_id"],
                "segment ID",
            ),
            (
                entry.offset,
                record["object_offset"],
                "object offset",
            ),
            (
                entry.length,
                record["object_length"],
                "object length",
            ),
            (
                entry.object_file_sha256,
                record["object_file_sha256"],
                "object-file SHA256",
            ),
            (
                entry.payload_sha256,
                record["payload_sha256"],
                "payload SHA256",
            ),
            (
                entry.segment_length,
                record["segment_length"],
                "segment length",
            ),
            (
                entry.segment_sha256,
                record["segment_sha256"],
                "segment SHA256",
            ),
        )

        for observed,expected,label in exact_pairs:
            if observed != expected:
                raise ClassAProviderResidentError(
                    "resident "
                    + label
                    + " mismatch"
                )

        expected_segment_path = (
            _REPO_ROOT
            / record["segment_path"]
        ).resolve()

        observed_segment_path = Path(
            entry.segment_path
        ).resolve()

        if (
            observed_segment_path
            != expected_segment_path
        ):
            raise ClassAProviderResidentError(
                "resident segment path mismatch"
            )

        return entry

    def _verify_serialized_object(
        self,
        *,
        serialized: bytes,
        record: dict[str, Any],
        tensor_name: str,
    ) -> tuple[int, int]:
        if not isinstance(
            serialized,
            bytes,
        ):
            raise ClassAProviderObjectError(
                "segment reader did not return bytes"
            )

        expected_object_length = (
            _require_plain_int(
                "object_length",
                record.get(
                    "object_length"
                ),
            )
        )

        if len(serialized) != expected_object_length:
            raise ClassAProviderObjectError(
                "serialized object length mismatch"
            )

        if (
            maf_object.HEADER_SIZE
            != EXPECTED_MAF_HEADER_SIZE
        ):
            raise ClassAProviderObjectError(
                "MAF header-size authority mismatch"
            )

        if (
            len(serialized)
            < EXPECTED_MAF_HEADER_SIZE
        ):
            raise ClassAProviderObjectError(
                "serialized object shorter than MAF header"
            )

        try:
            header = maf_object.unpack_header(
                serialized[
                    :EXPECTED_MAF_HEADER_SIZE
                ]
            )
        except Exception as exc:
            raise ClassAProviderObjectError(
                "serialized object header validation failed"
            ) from exc

        metadata_length = _require_plain_int(
            "metadata_length",
            header.get("metadata_length"),
        )

        payload_length = _require_plain_int(
            "payload_length",
            header.get("payload_length"),
        )

        if metadata_length < 0:
            raise ClassAProviderObjectError(
                "negative MAF metadata length"
            )

        expected_payload_length = (
            _require_plain_int(
                "expected_payload_length",
                record.get(
                    "expected_payload_length"
                ),
            )
        )

        if payload_length != expected_payload_length:
            raise ClassAProviderObjectError(
                "MAF payload length mismatch"
            )

        if (
            header.get("payload_sha256")
            != record.get("payload_sha256")
        ):
            raise ClassAProviderObjectError(
                "MAF header payload SHA256 mismatch"
            )

        metadata_start = (
            EXPECTED_MAF_HEADER_SIZE
        )

        metadata_end = (
            metadata_start
            + metadata_length
        )

        if metadata_end > len(serialized):
            raise ClassAProviderObjectError(
                "MAF metadata exceeds serialized object range"
            )

        payload_start = metadata_end
        payload_end = (
            payload_start
            + payload_length
        )

        if payload_end != len(serialized):
            raise ClassAProviderObjectError(
                "MAF payload does not exactly close serialized object range"
            )

        metadata_raw = serialized[
            metadata_start:metadata_end
        ]

        observed_metadata_sha256 = (
            hashlib.sha256(
                metadata_raw
            ).hexdigest()
        )

        if (
            observed_metadata_sha256
            != header.get(
                "metadata_sha256"
            )
        ):
            raise ClassAProviderObjectError(
                "MAF metadata SHA256 mismatch"
            )

        try:
            metadata = json.loads(
                metadata_raw.decode(
                    "utf-8"
                )
            )
        except Exception as exc:
            raise ClassAProviderObjectError(
                "MAF metadata JSON decode failed"
            ) from exc

        if not isinstance(
            metadata,
            dict,
        ):
            raise ClassAProviderObjectError(
                "MAF metadata root is not an object"
            )

        if (
            maf_object.canonical_json_bytes(
                metadata
            )
            != metadata_raw
        ):
            raise ClassAProviderObjectError(
                "MAF metadata is not canonical"
            )

        try:
            maf_object.validate_metadata(
                metadata,
                header,
            )
        except Exception as exc:
            raise ClassAProviderObjectError(
                "MAF metadata/header validation failed"
            ) from exc

        exact_metadata_pairs = (
            (
                metadata.get(
                    "tensor_name"
                ),
                tensor_name,
                "tensor name",
            ),
            (
                metadata.get(
                    "tensor_type"
                ),
                record.get(
                    "ggml_type_name"
                ),
                "tensor type",
            ),
            (
                metadata.get(
                    "dims"
                ),
                record.get("dims"),
                "dimensions",
            ),
            (
                metadata.get(
                    "element_count"
                ),
                record.get(
                    "element_count"
                ),
                "element count",
            ),
            (
                metadata.get(
                    "payload_length"
                ),
                expected_payload_length,
                "payload length",
            ),
            (
                metadata.get(
                    "payload_sha256"
                ),
                record.get(
                    "payload_sha256"
                ),
                "payload SHA256",
            ),
        )

        for observed,expected,label in exact_metadata_pairs:
            if observed != expected:
                raise ClassAProviderObjectError(
                    "MAF object metadata "
                    + label
                    + " mismatch"
                )

        payload_view = memoryview(
            serialized
        )[
            payload_start:payload_end
        ]

        observed_payload_sha256 = (
            hashlib.sha256(
                payload_view
            ).hexdigest()
        )

        if (
            observed_payload_sha256
            != record.get(
                "payload_sha256"
            )
        ):
            raise ClassAProviderObjectError(
                "MAF payload SHA256 mismatch"
            )

        return (
            payload_start,
            payload_length,
        )

    def _load_payload_and_transfer(
        self,
        *,
        tensor_ptr: ctypes.c_void_p,
        tensor_name: str,
        record: dict[str, Any],
        expected_nbytes: int,
    ) -> None:
        entry = self._resolve_resident_entry(
            record
        )

        try:
            serialized = (
                segment_reader.read_serialized_object(
                    entry,
                    EXPECTED_GENERATION_PK,
                )
            )
        except Exception as exc:
            raise ClassAProviderObjectError(
                "qualified serialized-object read failed"
            ) from exc

        (
            payload_start,
            payload_length,
        ) = self._verify_serialized_object(
            serialized=serialized,
            record=record,
            tensor_name=tensor_name,
        )

        if payload_length != expected_nbytes:
            raise ClassAProviderTransferError(
                "verified payload length differs from GGML byte span"
            )

        base_address = (
            _PY_BYTES_AS_STRING(
                serialized
            )
        )

        if not base_address:
            raise ClassAProviderTransferError(
                "unable to obtain stable provider-byte address"
            )

        payload_address = ctypes.c_void_p(
            int(base_address)
            + payload_start
        )

        self._ggml_backend_tensor_set(
            tensor_ptr,
            payload_address,
            0,
            payload_length,
        )

        # serialized remains strongly referenced until the synchronous
        # ggml_backend_tensor_set call above returns. No provider-owned
        # payload pointer is assigned to tensor.data.

    def _callback_entry(
        self,
        tensor_ptr: ctypes.c_void_p,
        userdata: ctypes.c_void_p,
    ) -> None:
        del userdata

        name: str | None = None

        try:
            if not tensor_ptr:
                self._record_callback(
                    None
                )
                raise ClassAProviderTensorError(
                    "null callback tensor"
                )

            name = self._tensor_name(
                tensor_ptr
            )

            self._record_callback(
                name
            )

            if self._already_failed():
                return

            record = self._resolve_record(
                name
            )

            expected_nbytes = (
                self._validate_tensor(
                    tensor_ptr=tensor_ptr,
                    name=name,
                    record=record,
                )
            )

            self._load_payload_and_transfer(
                tensor_ptr=tensor_ptr,
                tensor_name=name,
                record=record,
                expected_nbytes=(
                    expected_nbytes
                ),
            )

            self._record_success(
                name=name,
                object_pk=record[
                    "object_pk"
                ],
                payload_bytes=(
                    expected_nbytes
                ),
            )

        except BaseException as exc:
            self._record_failure(
                name=name,
                exc=exc,
            )

            # ctypes callbacks must not unwind Python exceptions through
            # the C ABI. Failure is retained explicitly and the provider
            # performs no substitute copy. A qualified caller must invoke
            # model_acceptance_gate after llama user-init returns.

    def initialize_model(
        self,
        metadata_ptr: ctypes.c_void_p,
    ) -> ctypes.c_void_p:
        if not metadata_ptr:
            raise ClassAProviderInitializationError(
                "in-memory GGUF metadata pointer is null"
            )

        with self._state_lock:
            if self._initialization_started:
                raise ClassAProviderInitializationError(
                    "provider initialization is one-shot"
                )

            self._initialization_started = True

        params = self._llama_model_default_params()

        # Frozen Class-A safety requirements. The pinned
        # llama_model_init_from_user implementation additionally forces
        # LLAMA_LOAD_MODE_NONE and use_extra_bufts=false internally.
        params.vocab_only = False
        params.use_extra_bufts = False
        params.no_alloc = False

        model_ptr = self._llama_model_init_from_user(
            metadata_ptr,
            self._callback,
            self.userdata,
            params,
        )

        if not model_ptr:
            if self._already_failed():
                self.model_acceptance_gate()

            raise ClassAProviderInitializationError(
                "llama_model_init_from_user returned null"
            )

        try:
            self.model_acceptance_gate()
        except BaseException:
            self._llama_model_free(
                model_ptr
            )
            raise

        return ctypes.c_void_p(
            model_ptr
        )

    def model_acceptance_gate(
        self,
    ) -> dict[str, Any]:
        with self._state_lock:
            if self._state.failed:
                raise ClassAProviderFailureStateError(
                    "provider callback failure: "
                    + str(
                        self._state.failure_type
                    )
                    + ": "
                    + str(
                        self._state.failure_message
                    )
                )

            if self._state.callback_count <= 0:
                raise ClassAProviderFailureStateError(
                    "provider received no tensor callbacks"
                )

            if (
                self._state.transfer_count
                != self._state.resolved_count
            ):
                raise ClassAProviderFailureStateError(
                    "provider resolution/transfer count mismatch"
                )

            if (
                self._state.transfer_count
                != self._state.callback_count
            ):
                raise ClassAProviderFailureStateError(
                    "provider callback/transfer count mismatch"
                )

            return self._qualification_record_locked()

    def qualification_record(
        self,
    ) -> dict[str, Any]:
        with self._state_lock:
            return self._qualification_record_locked()

    def _qualification_record_locked(
        self,
    ) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "model_pk": EXPECTED_MODEL_PK,
            "generation_pk": (
                EXPECTED_GENERATION_PK
            ),
            "provider_contract_sha256": (
                PROVIDER_CONTRACT_SHA256
            ),
            "join_authority_sha256": (
                JOIN_AUTHORITY_SHA256
            ),
            "metadata_authority_sha256": (
                METADATA_AUTHORITY_SHA256
            ),
            "callback_count": (
                self._state.callback_count
            ),
            "resolved_count": (
                self._state.resolved_count
            ),
            "transfer_count": (
                self._state.transfer_count
            ),
            "unique_callback_names": sorted(
                self._state.unique_callback_names
            ),
            "unique_callback_name_count": len(
                self._state.unique_callback_names
            ),
            "duplicate_name_counts": dict(
                sorted(
                    self._state.duplicate_name_counts.items()
                )
            ),
            "failed": self._state.failed,
            "failure_tensor": (
                self._state.failure_tensor
            ),
            "failure_type": (
                self._state.failure_type
            ),
            "failure_message": (
                self._state.failure_message
            ),
            "resolution_results": list(
                self._state.resolution_results
            ),
        }


__all__ = [
    "SCHEMA",
    "ClassAProviderError",
    "ClassAProviderAuthorityError",
    "ClassAProviderTensorError",
    "ClassAProviderResidentError",
    "ClassAProviderObjectError",
    "ClassAProviderTransferError",
    "ClassAProviderInitializationError",
    "ClassAProviderFailureStateError",
    "ProviderState",
    "ClassAMAFBackedTensorProvider",
]
