#!/usr/bin/env python3

from __future__ import annotations

import ctypes
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


SCHEMA = "openmind.maf_phase_6e_d_class_a_provider_execution_preflight_negative_path_qualification.v1"

PROTOCOL_SHA256 = "f89a4e3303c8e04e9fd3fc9b6378b13f3efec6b9706f814bc665b7458f104123"
PROVIDER_SHA256 = "e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec"
PROVIDER_GIT_BLOB = "14fa6be4a2cf69b8125e6540e0a808bd2758f792"
JOIN_SHA256 = "34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709"
LLAMA_CPP_HEAD = "4cf5cab65d5257be31e7623eb552b1861e969c75"

EXPECTED_MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
EXPECTED_GENERATION_PK = "mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2"

EXPECTED_NEGATIVE_TESTS = 9
EXPECTED_TENSOR_COUNT = 339
EXPECTED_HEADER_SIZE = 96

REQUIRED_SHARED_SYMBOLS = (
    "ggml_get_name",
    "ggml_nelements",
    "ggml_nbytes",
    "ggml_backend_tensor_set",
    "llama_model_default_params",
    "llama_model_init_from_user",
    "llama_model_free",
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MODEL_DIR = _REPO_ROOT / "experiments/model_fractal"

_PROTOCOL_PATH = (
    _MODEL_DIR
    / "MAF_PHASE_6E_D_CLASS_A_PROVIDER_EXECUTION_PREFLIGHT_NEGATIVE_PATH_QUALIFICATION_PROTOCOL_V1.md"
)

_PROVIDER_PATH = (
    _MODEL_DIR
    / "maf_phase_6e_d_class_a_maf_backed_tensor_provider_v1.py"
)

_JOIN_PATH = (
    _MODEL_DIR
    / "maf_phase_6e_d_class_a_tensor_object_segment_join_v1.json"
)

_RESULT_PATH = (
    _MODEL_DIR
    / "maf_phase_6e_d_class_a_provider_execution_preflight_negative_path_qualification_v1.json"
)

_LLAMA_ROOT = Path.home() / "llama.cpp"

_PROTECTED_SEGMENT = (
    _REPO_ROOT
    / "results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg"
)

_PROTECTED_SEGMENT_LENGTH = 1888934699

_SOURCE_GGUF = (
    Path.home()
    / "qwen2.5-coder-q8_0.gguf"
)


class RunnerError(RuntimeError):
    pass


class QualificationFailure(RunnerError):
    pass


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
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _run_git(
    *args: str,
    cwd: Path | None = None,
) -> bytes:
    result = subprocess.run(
        ("git",) + args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RunnerError(
            "git command failed: "
            + " ".join(args)
            + " | "
            + result.stderr.decode(
                errors="replace"
            ).strip()
        )

    return result.stdout


def _verify_execution_checkpoint() -> str:
    branch = _run_git(
        "branch",
        "--show-current",
        cwd=_REPO_ROOT,
    ).decode().strip()

    if branch != "labs/multidimensional-maf":
        raise QualificationFailure(
            "OpenMind branch mismatch"
        )

    if (
        _run_git(
            "diff",
            "--name-only",
            "-z",
            cwd=_REPO_ROOT,
        )
        != b""
    ):
        raise QualificationFailure(
            "tracked worktree is dirty"
        )

    if (
        _run_git(
            "diff",
            "--cached",
            "--name-only",
            "-z",
            cwd=_REPO_ROOT,
        )
        != b""
    ):
        raise QualificationFailure(
            "index is not empty"
        )

    head = _run_git(
        "rev-parse",
        "HEAD",
        cwd=_REPO_ROOT,
    ).decode().strip()

    if (
        _sha256_file(
            _PROTOCOL_PATH
        )
        != PROTOCOL_SHA256
    ):
        raise QualificationFailure(
            "protocol SHA256 mismatch"
        )

    if (
        _sha256_file(
            _PROVIDER_PATH
        )
        != PROVIDER_SHA256
    ):
        raise QualificationFailure(
            "provider SHA256 mismatch"
        )

    provider_blob = _run_git(
        "rev-parse",
        "HEAD:"
        + str(
            _PROVIDER_PATH.relative_to(
                _REPO_ROOT
            )
        ),
        cwd=_REPO_ROOT,
    ).decode().strip()

    if (
        provider_blob
        != PROVIDER_GIT_BLOB
    ):
        raise QualificationFailure(
            "provider Git blob mismatch"
        )

    if (
        _sha256_file(
            _JOIN_PATH
        )
        != JOIN_SHA256
    ):
        raise QualificationFailure(
            "join authority SHA256 mismatch"
        )

    llama_head = _run_git(
        "rev-parse",
        "HEAD",
        cwd=_LLAMA_ROOT,
    ).decode().strip()

    if llama_head != LLAMA_CPP_HEAD:
        raise QualificationFailure(
            "llama.cpp HEAD mismatch"
        )

    if (
        _run_git(
            "status",
            "--porcelain=v1",
            "-uno",
            cwd=_LLAMA_ROOT,
        )
        != b""
    ):
        raise QualificationFailure(
            "llama.cpp tracked tree dirty"
        )

    if _RESULT_PATH.exists():
        raise QualificationFailure(
            "qualification result already exists"
        )

    return head


class ProtectedIOGuard:
    def __init__(self) -> None:
        self.segment_open_count = 0
        self.source_gguf_open_count = 0

        segment_stat = os.stat(
            _PROTECTED_SEGMENT,
            follow_symlinks=True,
        )

        if (
            not stat.S_ISREG(
                segment_stat.st_mode
            )
            or segment_stat.st_size
            != _PROTECTED_SEGMENT_LENGTH
        ):
            raise QualificationFailure(
                "protected segment metadata mismatch"
            )

        self.segment_identity = (
            segment_stat.st_dev,
            segment_stat.st_ino,
        )

        self.segment_path = (
            _PROTECTED_SEGMENT.resolve()
        )

        self.source_gguf_path = (
            _SOURCE_GGUF.resolve()
        )

    def _candidate_path(
        self,
        value: Any,
    ) -> Path | None:
        if isinstance(
            value,
            int,
        ):
            return None

        try:
            raw = os.fspath(
                value
            )
        except TypeError:
            return None

        if isinstance(
            raw,
            bytes,
        ):
            raw = os.fsdecode(
                raw
            )

        if not isinstance(
            raw,
            str,
        ):
            return None

        try:
            path = Path(
                raw
            ).expanduser()

            if not path.is_absolute():
                path = (
                    Path.cwd()
                    / path
                )

            return path.resolve(
                strict=False
            )

        except Exception:
            return None

    def _same_segment_inode(
        self,
        path: Path,
    ) -> bool:
        try:
            st = os.stat(
                path,
                follow_symlinks=True,
            )
        except OSError:
            return False

        return (
            st.st_dev,
            st.st_ino,
        ) == self.segment_identity

    def audit(
        self,
        event: str,
        args: tuple[Any, ...],
    ) -> None:
        if event != "open":
            return

        if not args:
            return

        candidate = self._candidate_path(
            args[0]
        )

        if candidate is None:
            return

        if (
            candidate
            == self.source_gguf_path
        ):
            self.source_gguf_open_count += 1

            raise PermissionError(
                "source GGUF open prohibited"
            )

        if (
            candidate
            == self.segment_path
            or self._same_segment_inode(
                candidate
            )
        ):
            self.segment_open_count += 1

            raise PermissionError(
                "persistent MAF segment open prohibited"
            )


def _install_audit_guard() -> ProtectedIOGuard:
    guard = ProtectedIOGuard()

    sys.addaudithook(
        guard.audit
    )

    return guard


def _import_frozen_provider() -> Any:
    if str(_MODEL_DIR) not in sys.path:
        sys.path.insert(
            0,
            str(_MODEL_DIR),
        )

    if (
        _sha256_file(
            _PROVIDER_PATH
        )
        != PROVIDER_SHA256
    ):
        raise QualificationFailure(
            "provider changed before import"
        )

    module_name = (
        "_openmind_phase_6e_d_frozen_provider"
    )

    spec = importlib.util.spec_from_file_location(
        module_name,
        _PROVIDER_PATH,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise QualificationFailure(
            "provider import specification unavailable"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        module_name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    except BaseException:
        sys.modules.pop(
            module_name,
            None,
        )
        raise

    if (
        module.SCHEMA
        != "openmind.maf_phase_6e_d_class_a_maf_backed_tensor_provider.v1"
    ):
        raise QualificationFailure(
            "provider schema mismatch"
        )

    if (
        module.PROVIDER_CONTRACT_SHA256
        != "2782678c5153761e028f29f35d7275b019590af5a35391ea967c71c027c2ebb2"
    ):
        raise QualificationFailure(
            "provider contract binding mismatch"
        )

    if (
        module.JOIN_AUTHORITY_SHA256
        != JOIN_SHA256
    ):
        raise QualificationFailure(
            "provider join binding mismatch"
        )

    if (
        module.METADATA_AUTHORITY_SHA256
        != "bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966"
    ):
        raise QualificationFailure(
            "provider metadata binding mismatch"
        )

    if (
        module.EXPECTED_MODEL_PK
        != EXPECTED_MODEL_PK
        or module.EXPECTED_GENERATION_PK
        != EXPECTED_GENERATION_PK
    ):
        raise QualificationFailure(
            "provider model or generation PK mismatch"
        )

    if (
        module.EXPECTED_TENSOR_COUNT
        != EXPECTED_TENSOR_COUNT
        or module.EXPECTED_MAF_HEADER_SIZE
        != EXPECTED_HEADER_SIZE
    ):
        raise QualificationFailure(
            "provider tensor or header authority mismatch"
        )

    if (
        module.resident.OBJECT_PK_KIND
        != "object_pk"
    ):
        raise QualificationFailure(
            "provider resident PK kind mismatch"
        )

    return module


def _select_shared_library() -> Path:
    candidates: list[Path] = []

    for path in _LLAMA_ROOT.rglob(
        "libllama.so*"
    ):
        try:
            st = os.lstat(
                path
            )
        except OSError:
            continue

        if not stat.S_ISREG(
            st.st_mode
        ):
            continue

        if stat.S_ISLNK(
            st.st_mode
        ):
            continue

        candidates.append(
            path.resolve()
        )

    unique = sorted(
        {
            str(path): path
            for path in candidates
        }.values(),
        key=lambda item: str(item),
    )

    if not unique:
        raise QualificationFailure(
            "no regular llama shared-library artifact found"
        )

    return unique[0]


def _preflight_real_library() -> tuple[Any, dict[str, Any]]:
    selected = _select_shared_library()

    st = os.stat(
        selected
    )

    if not stat.S_ISREG(
        st.st_mode
    ):
        raise QualificationFailure(
            "selected shared library is not regular"
        )

    digest = _sha256_file(
        selected
    )

    library = ctypes.CDLL(
        str(selected)
    )

    available: list[str] = []

    for symbol in REQUIRED_SHARED_SYMBOLS:
        try:
            getattr(
                library,
                symbol,
            )
        except AttributeError as exc:
            raise QualificationFailure(
                "selected shared library lacks required symbol: "
                + symbol
            ) from exc

        available.append(
            symbol
        )

    return (
        library,
        {
            "path": str(selected),
            "bytes": st.st_size,
            "sha256": digest,
            "llama_cpp_head": LLAMA_CPP_HEAD,
            "loaded": True,
            "required_symbols": list(
                REQUIRED_SHARED_SYMBOLS
            ),
            "available_symbols": available,
            "complete_interface": (
                tuple(available)
                == REQUIRED_SHARED_SYMBOLS
            ),
        },
    )


class FakeCallable:
    def __init__(
        self,
        fn: Callable[..., Any],
    ) -> None:
        self.fn = fn
        self.calls = 0
        self.argtypes: Any = None
        self.restype: Any = None

    def __call__(
        self,
        *args: Any,
    ) -> Any:
        self.calls += 1

        return self.fn(
            *args
        )


class FakeLibrary:
    def __init__(
        self,
        provider_module: Any,
        *,
        missing_symbol: str | None = None,
        mode: str = "null",
        name_bytes: bytes = b"unknown.tensor",
        nelements: int = 0,
        nbytes: int = 0,
        tensor_ptr: ctypes.c_void_p | None = None,
    ) -> None:
        self.provider_module = (
            provider_module
        )
        self.mode = mode
        self.name_bytes = name_bytes
        self.nelements_value = nelements
        self.nbytes_value = nbytes
        self.tensor_ptr = tensor_ptr
        self.freed_models: list[int] = []

        functions = {
            "ggml_get_name": FakeCallable(
                self._get_name
            ),
            "ggml_nelements": FakeCallable(
                self._nelements
            ),
            "ggml_nbytes": FakeCallable(
                self._nbytes
            ),
            "ggml_backend_tensor_set": FakeCallable(
                self._backend_set
            ),
            "llama_model_default_params": FakeCallable(
                self._default_params
            ),
            "llama_model_init_from_user": FakeCallable(
                self._user_init
            ),
            "llama_model_free": FakeCallable(
                self._model_free
            ),
        }

        for name,value in functions.items():
            if name == missing_symbol:
                continue

            setattr(
                self,
                name,
                value,
            )

    def _get_name(
        self,
        tensor: Any,
    ) -> bytes:
        del tensor
        return self.name_bytes

    def _nelements(
        self,
        tensor: Any,
    ) -> int:
        del tensor
        return self.nelements_value

    def _nbytes(
        self,
        tensor: Any,
    ) -> int:
        del tensor
        return self.nbytes_value

    def _backend_set(
        self,
        tensor: Any,
        data: Any,
        offset: Any,
        size: Any,
    ) -> None:
        del tensor
        del data
        del offset
        del size

        raise QualificationFailure(
            "backend tensor copy invoked by negative-path qualification"
        )

    def _default_params(
        self,
    ) -> Any:
        return (
            self.provider_module
            ._LlamaModelParams()
        )

    def _user_init(
        self,
        metadata: Any,
        callback: Any,
        userdata: Any,
        params: Any,
    ) -> int:
        del metadata
        del params

        if self.mode == "null":
            return 0

        if self.mode == "model_no_callback":
            return 0x1010

        if self.mode == "callback_null":
            callback(
                None,
                userdata,
            )
            return 0x2020

        if self.mode == "callback_tensor":
            if self.tensor_ptr is None:
                raise QualificationFailure(
                    "fake callback tensor pointer missing"
                )

            callback(
                self.tensor_ptr,
                userdata,
            )
            return 0x3030

        raise QualificationFailure(
            "unknown fake user-init mode"
        )

    def _model_free(
        self,
        model: Any,
    ) -> None:
        value = (
            model.value
            if isinstance(
                model,
                ctypes.c_void_p,
            )
            else int(model)
        )

        self.freed_models.append(
            int(value)
        )

    def count(
        self,
        name: str,
    ) -> int:
        value = getattr(
            self,
            name,
            None,
        )

        if value is None:
            return 0

        return int(
            value.calls
        )


class ReaderCounter:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> bytes:
        del args
        del kwargs

        self.calls += 1

        raise QualificationFailure(
            "real serialized-object reader invoked during negative qualification"
        )


def _expect_exception(
    fn: Callable[[], Any],
) -> tuple[str | None, bool]:
    try:
        value = fn()
    except BaseException as exc:
        return (
            type(exc).__name__,
            False,
        )

    del value

    return (
        None,
        True,
    )


def _empty_directory(
    provider_module: Any,
) -> Any:
    return (
        provider_module
        .resident
        .ResidentPKDirectory()
    )


def _counts(
    fake: FakeLibrary,
) -> dict[str, int]:
    return {
        "default_params_calls": fake.count(
            "llama_model_default_params"
        ),
        "user_init_calls": fake.count(
            "llama_model_init_from_user"
        ),
        "model_free_calls": fake.count(
            "llama_model_free"
        ),
        "backend_copy_calls": fake.count(
            "ggml_backend_tensor_set"
        ),
    }


def _result_record(
    *,
    test_id: str,
    expected_failure_class: str,
    observed_failure_class: str | None,
    provider: Any | None,
    fake: FakeLibrary,
    reader_calls: int,
    model_handle_escaped: bool,
    extra_pass: bool,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    callback_calls = (
        provider.state.callback_count
        if provider is not None
        else 0
    )

    counts = _counts(
        fake
    )

    passed = (
        observed_failure_class
        == expected_failure_class
        and not model_handle_escaped
        and counts[
            "backend_copy_calls"
        ]
        == 0
        and reader_calls == 0
        and extra_pass
    )

    record: dict[str, Any] = {
        "test_id": test_id,
        "expected_failure_class": (
            expected_failure_class
        ),
        "observed_failure_class": (
            observed_failure_class
        ),
        "user_init_calls": counts[
            "user_init_calls"
        ],
        "callback_calls": (
            callback_calls
        ),
        "model_free_calls": counts[
            "model_free_calls"
        ],
        "backend_copy_calls": counts[
            "backend_copy_calls"
        ],
        "serialized_object_reader_calls": (
            reader_calls
        ),
        "model_handle_escaped": (
            model_handle_escaped
        ),
        "provider_failed": (
            provider.state.failed
            if provider is not None
            else False
        ),
        "provider_failure_type": (
            provider.state.failure_type
            if provider is not None
            else None
        ),
        "pass": passed,
    }

    if extra:
        record.update(
            extra
        )

    return record


def _make_tensor(
    provider_module: Any,
    record: dict[str, Any],
    *,
    wrong_type: bool,
) -> tuple[Any, ctypes.c_void_p]:
    tensor = (
        provider_module
        ._GGMLTensorPrefix()
    )

    tensor.type = int(
        record["ggml_type"]
    )

    if wrong_type:
        tensor.type = int(
            record["ggml_type"]
        ) + 1

    tensor.buffer = 1

    for i in range(
        provider_module
        .EXPECTED_GGML_MAX_DIMS
    ):
        tensor.ne[i] = 1

    for i,value in enumerate(
        record["dims"]
    ):
        tensor.ne[i] = int(
            value
        )

    ptr = ctypes.cast(
        ctypes.pointer(
            tensor
        ),
        ctypes.c_void_p,
    )

    return (
        tensor,
        ptr,
    )


def _run_negative_tests(
    provider_module: Any,
    reader_counter: ReaderCounter,
) -> list[dict[str, Any]]:
    join = json.loads(
        _JOIN_PATH.read_text()
    )

    records = join.get(
        "records"
    )

    if (
        not isinstance(
            records,
            list,
        )
        or len(records)
        != EXPECTED_TENSOR_COUNT
    ):
        raise QualificationFailure(
            "join record count mismatch"
        )

    frozen = records[0]

    tests: list[dict[str, Any]] = []

    # NP01
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
        missing_symbol=(
            "llama_model_free"
        ),
    )

    observed,escaped = _expect_exception(
        lambda: provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    tests.append(
        _result_record(
            test_id="NP01",
            expected_failure_class=(
                "ClassAProviderAuthorityError"
            ),
            observed_failure_class=observed,
            provider=None,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                fake.count(
                    "llama_model_init_from_user"
                )
                == 0
                and fake.count(
                    "llama_model_free"
                )
                == 0
            ),
        )
    )

    # NP02
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p()
        )
    )

    tests.append(
        _result_record(
            test_id="NP02",
            expected_failure_class=(
                "ClassAProviderInitializationError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                fake.count(
                    "llama_model_default_params"
                )
                == 0
                and fake.count(
                    "llama_model_init_from_user"
                )
                == 0
                and fake.count(
                    "llama_model_free"
                )
                == 0
                and provider.state.callback_count
                == 0
            ),
        )
    )

    # NP03
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
        mode="null",
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    tests.append(
        _result_record(
            test_id="NP03",
            expected_failure_class=(
                "ClassAProviderInitializationError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                fake.count(
                    "llama_model_init_from_user"
                )
                == 1
                and fake.count(
                    "llama_model_free"
                )
                == 0
                and provider.state.callback_count
                == 0
            ),
        )
    )

    # NP04
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
        mode="model_no_callback",
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    tests.append(
        _result_record(
            test_id="NP04",
            expected_failure_class=(
                "ClassAProviderFailureStateError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                fake.count(
                    "llama_model_init_from_user"
                )
                == 1
                and fake.count(
                    "llama_model_free"
                )
                == 1
                and provider.state.callback_count
                == 0
            ),
        )
    )

    # NP05
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
        mode="callback_null",
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    tests.append(
        _result_record(
            test_id="NP05",
            expected_failure_class=(
                "ClassAProviderFailureStateError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                provider.state.failed
                and provider.state.failure_type
                == "ClassAProviderTensorError"
                and provider.state.callback_count
                == 1
                and fake.count(
                    "llama_model_free"
                )
                == 1
            ),
        )
    )

    # NP06
    before = reader_counter.calls

    dummy = (
        provider_module
        ._GGMLTensorPrefix()
    )

    dummy.buffer = 1

    dummy_ptr = ctypes.cast(
        ctypes.pointer(
            dummy
        ),
        ctypes.c_void_p,
    )

    fake = FakeLibrary(
        provider_module,
        mode="callback_tensor",
        name_bytes=(
            b"openmind.invalid.tensor"
        ),
        tensor_ptr=dummy_ptr,
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    tests.append(
        _result_record(
            test_id="NP06",
            expected_failure_class=(
                "ClassAProviderFailureStateError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                provider.state.failed
                and provider.state.failure_type
                == "ClassAProviderTensorError"
                and provider.state.callback_count
                == 1
                and fake.count(
                    "llama_model_free"
                )
                == 1
            ),
        )
    )

    # NP07
    before = reader_counter.calls

    wrong_tensor,wrong_ptr = _make_tensor(
        provider_module,
        frozen,
        wrong_type=True,
    )

    fake = FakeLibrary(
        provider_module,
        mode="callback_tensor",
        name_bytes=(
            frozen[
                "tensor_name"
            ].encode(
                "utf-8"
            )
        ),
        nelements=int(
            frozen[
                "element_count"
            ]
        ),
        nbytes=int(
            frozen[
                "expected_payload_length"
            ]
        ),
        tensor_ptr=wrong_ptr,
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    del wrong_tensor

    tests.append(
        _result_record(
            test_id="NP07",
            expected_failure_class=(
                "ClassAProviderFailureStateError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                provider.state.failed
                and provider.state.failure_type
                == "ClassAProviderTensorError"
                and fake.count(
                    "llama_model_free"
                )
                == 1
            ),
        )
    )

    # NP08
    before = reader_counter.calls

    valid_tensor,valid_ptr = _make_tensor(
        provider_module,
        frozen,
        wrong_type=False,
    )

    fake = FakeLibrary(
        provider_module,
        mode="callback_tensor",
        name_bytes=(
            frozen[
                "tensor_name"
            ].encode(
                "utf-8"
            )
        ),
        nelements=int(
            frozen[
                "element_count"
            ]
        ),
        nbytes=int(
            frozen[
                "expected_payload_length"
            ]
        ),
        tensor_ptr=valid_ptr,
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    del valid_tensor

    tests.append(
        _result_record(
            test_id="NP08",
            expected_failure_class=(
                "ClassAProviderFailureStateError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                provider.state.failed
                and provider.state.failure_type
                == "ClassAProviderResidentError"
                and fake.count(
                    "llama_model_free"
                )
                == 1
                and reader_counter.calls
                == before
            ),
        )
    )

    # NP09
    before = reader_counter.calls

    fake = FakeLibrary(
        provider_module,
        mode="null",
    )

    provider = (
        provider_module
        .ClassAMAFBackedTensorProvider(
            directory=_empty_directory(
                provider_module
            ),
            ggml_library=fake,
        )
    )

    first_failure,first_escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    user_init_before_second = fake.count(
        "llama_model_init_from_user"
    )

    callback_before_second = (
        provider.state.callback_count
    )

    backend_before_second = fake.count(
        "ggml_backend_tensor_set"
    )

    observed,escaped = _expect_exception(
        lambda: provider.initialize_model(
            ctypes.c_void_p(1)
        )
    )

    tests.append(
        _result_record(
            test_id="NP09",
            expected_failure_class=(
                "ClassAProviderInitializationError"
            ),
            observed_failure_class=observed,
            provider=provider,
            fake=fake,
            reader_calls=(
                reader_counter.calls
                - before
            ),
            model_handle_escaped=escaped,
            extra_pass=(
                first_failure
                == "ClassAProviderInitializationError"
                and not first_escaped
                and fake.count(
                    "llama_model_init_from_user"
                )
                == user_init_before_second
                and provider.state.callback_count
                == callback_before_second
                and fake.count(
                    "ggml_backend_tensor_set"
                )
                == backend_before_second
                and user_init_before_second
                == 1
            ),
            extra={
                "first_attempt_failure_class": (
                    first_failure
                ),
                "second_user_init_increment": (
                    fake.count(
                        "llama_model_init_from_user"
                    )
                    - user_init_before_second
                ),
                "second_callback_increment": (
                    provider.state.callback_count
                    - callback_before_second
                ),
                "second_backend_copy_increment": (
                    fake.count(
                        "ggml_backend_tensor_set"
                    )
                    - backend_before_second
                ),
            },
        )
    )

    if len(tests) != EXPECTED_NEGATIVE_TESTS:
        raise QualificationFailure(
            "negative test count mismatch"
        )

    return tests


def _write_result(
    result: dict[str, Any],
) -> None:
    if _RESULT_PATH.exists():
        raise QualificationFailure(
            "qualification result path already exists"
        )

    raw = _canonical_json_bytes(
        result
    )

    tmp_name: str | None = None

    try:
        fd,tmp_name = tempfile.mkstemp(
            prefix=(
                _RESULT_PATH.name
                + ".building."
            ),
            dir=str(
                _RESULT_PATH.parent
            ),
        )

        with os.fdopen(
            fd,
            "wb",
        ) as stream:
            stream.write(
                raw
            )
            stream.flush()
            os.fsync(
                stream.fileno()
            )

        os.replace(
            tmp_name,
            _RESULT_PATH,
        )

        tmp_name = None

    finally:
        if (
            tmp_name is not None
            and Path(
                tmp_name
            ).exists()
        ):
            Path(
                tmp_name
            ).unlink()

    reopened = _RESULT_PATH.read_bytes()

    if reopened != raw:
        raise QualificationFailure(
            "result reopen mismatch"
        )


def main() -> int:
    sys.dont_write_bytecode = True

    openmind_head = (
        _verify_execution_checkpoint()
    )

    guard = _install_audit_guard()

    provider_module = (
        _import_frozen_provider()
    )

    original_reader = (
        provider_module
        .segment_reader
        .read_serialized_object
    )

    reader_counter = ReaderCounter()

    provider_module.segment_reader.read_serialized_object = (
        reader_counter
    )

    real_library = None
    shared_library: dict[str, Any] = {}

    tests: list[
        dict[str, Any]
    ] = []

    fatal_error: dict[
        str,
        Any,
    ] | None = None

    try:
        (
            real_library,
            shared_library,
        ) = _preflight_real_library()

        tests = _run_negative_tests(
            provider_module,
            reader_counter,
        )

    except BaseException as exc:
        fatal_error = {
            "type": type(exc).__name__,
            "message": str(exc),
        }

    finally:
        provider_module.segment_reader.read_serialized_object = (
            original_reader
        )

    del real_library

    passed = sum(
        1
        for record in tests
        if record.get(
            "pass"
        )
        is True
    )

    protected_io = {
        "segment_opens": (
            guard.segment_open_count
        ),
        "source_gguf_opens": (
            guard.source_gguf_open_count
        ),
        "serialized_object_reader_calls": (
            reader_counter.calls
        ),
    }

    global_zero_io = (
        guard.segment_open_count == 0
        and guard.source_gguf_open_count
        == 0
        and reader_counter.calls == 0
    )

    complete_pass = (
        fatal_error is None
        and len(tests)
        == EXPECTED_NEGATIVE_TESTS
        and passed
        == EXPECTED_NEGATIVE_TESTS
        and global_zero_io
        and shared_library.get(
            "complete_interface"
        )
        is True
    )

    disposition = (
        "CLASS-A PROVIDER EXECUTION PREFLIGHT + NEGATIVE-PATH QUALIFICATION PASS"
        if complete_pass
        else
        "CLASS-A PROVIDER EXECUTION PREFLIGHT + NEGATIVE-PATH QUALIFICATION FAIL"
    )

    result = {
        "schema": SCHEMA,
        "protocol_sha256": (
            PROTOCOL_SHA256
        ),
        "provider_sha256": (
            PROVIDER_SHA256
        ),
        "provider_git_blob": (
            PROVIDER_GIT_BLOB
        ),
        "join_sha256": JOIN_SHA256,
        "openmind_head": (
            openmind_head
        ),
        "llama_cpp_head": (
            LLAMA_CPP_HEAD
        ),
        "shared_library": (
            shared_library
        ),
        "protected_io": (
            protected_io
        ),
        "negative_tests": (
            tests
        ),
        "summary": {
            "negative_tests_expected": (
                EXPECTED_NEGATIVE_TESTS
            ),
            "negative_tests_observed": (
                len(tests)
            ),
            "negative_tests_passed": (
                passed
            ),
            "segment_opens": (
                guard.segment_open_count
            ),
            "source_gguf_opens": (
                guard.source_gguf_open_count
            ),
            "serialized_object_reader_calls": (
                reader_counter.calls
            ),
            "real_llama_user_init_calls": 0,
            "real_model_loads": 0,
            "inference_calls": 0,
            "fatal_error": (
                fatal_error
            ),
            "all_pass": (
                complete_pass
            ),
        },
        "disposition": (
            disposition
        ),
    }

    _write_result(
        result
    )

    print(
        "STATUS             : "
        + disposition
    )
    print(
        "GATE FAILURE       : "
        + (
            "NONE"
            if complete_pass
            else (
                fatal_error[
                    "type"
                ]
                if fatal_error
                else
                "NEGATIVE_PATH_FAILURE"
            )
        )
    )
    print(
        "OPENMIND HEAD      : "
        + openmind_head
    )
    print(
        "PROTOCOL SHA       : "
        + PROTOCOL_SHA256
    )
    print(
        "PROVIDER SHA       : "
        + PROVIDER_SHA256
    )
    print(
        "NEGATIVE EXPECTED  : "
        + str(
            EXPECTED_NEGATIVE_TESTS
        )
    )
    print(
        "NEGATIVE PASSED    : "
        + str(
            passed
        )
    )
    print(
        "SEGMENT OPENS      : "
        + str(
            guard.segment_open_count
        )
    )
    print(
        "SOURCE GGUF OPENS  : "
        + str(
            guard.source_gguf_open_count
        )
    )
    print(
        "SERIALIZED READS   : "
        + str(
            reader_counter.calls
        )
    )
    print(
        "REAL USER-INIT     : 0"
    )
    print(
        "MODEL LOAD         : 0"
    )
    print(
        "INFERENCE          : 0"
    )
    print(
        "RESULT PATH        : "
        + str(
            _RESULT_PATH.relative_to(
                _REPO_ROOT
            )
        )
    )
    print(
        "RESULT SHA         : "
        + _sha256_file(
            _RESULT_PATH
        )
    )
    print(
        "RESULT BYTES       : "
        + str(
            _RESULT_PATH.stat().st_size
        )
    )
    print(
        "PHASE 6E-D SCIENCE : NOT AUTHORIZED"
    )

    return (
        0
        if complete_pass
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
