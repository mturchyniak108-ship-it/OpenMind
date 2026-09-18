#!/usr/bin/env python3

import ctypes
import dataclasses
import hashlib
import importlib.util
import json
import os
import stat
import struct
import subprocess
import sys
import tempfile
import threading
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import MappingProxyType

import math
import struct

BRANCH="labs/multidimensional-maf"

PROTOCOL_FREEZE_HEAD='d06c0752b57cadd5c18e86200b1ec27025e7ddc3'

RUNNER_COMMIT_SUBJECT='research: freeze Phase 6E-D Class-A inference logit parity validation V1 runner'

RUNNER_PATH=Path('experiments/model_fractal/maf_phase_6e_d_class_a_inference_logit_parity_validation_v1.py')

RESULT_PATH=Path('experiments/model_fractal/maf_phase_6e_d_class_a_inference_logit_parity_validation_v1.json')

PROTOCOL_PATH=Path('experiments/model_fractal/MAF_PHASE_6E_D_CLASS_A_INFERENCE_LOGIT_PARITY_VALIDATION_PROTOCOL_V1.md')

PROTOCOL_SHA256='c9cb726835ce347eb5cafde37faba7e2393fb3f98474f1f224fa2908ec93d7bc'

PROTOCOL_BLOB='64f8b3918cc56920141d689a23dcdd1f5f525f69'

PROVIDER_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_maf_backed_tensor_provider_v1.py")

PROVIDER_SHA256="e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec"

PROVIDER_BLOB="14fa6be4a2cf69b8125e6540e0a808bd2758f792"

RESIDENT_PATH=Path("experiments/model_fractal/maf_resident_pk_directory_v1.py")

RESIDENT_SHA256="4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"

SEGMENT_READER_PATH=Path("experiments/model_fractal/maf_segment_reader_v1.py")

SEGMENT_READER_SHA256="3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369"

METADATA_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json")

METADATA_SHA256="bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966"

JOIN_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_tensor_object_segment_join_v1.json")

JOIN_SHA256="34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709"

GENERATION_PATH=Path("results/runtime/maf_full_model_persistent_generation_v1/generation.manifest.json")

GENERATION_SHA256="a79b012f10904a5e0540076a8443007344ada4e11e3846d817201b43583fedff"

RECOVERY_QUALIFICATION_PATH=Path("experiments/model_fractal/maf_phase_6e_d_partial_state_recovery_qualification_v1.json")

RECOVERY_QUALIFICATION_SHA256="94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6"

NEGATIVE_RESULT_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_provider_execution_preflight_negative_path_qualification_v1.json")

NEGATIVE_RESULT_SHA256="ec23ed47ca813792ff3fedf9e7b08e16140d265a5a88c4908082dde250f399d5"

MODEL_PK="mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"

GENERATION_PK="mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2"

DERIVED_ACTIVE_SHA256="82bc4bc0975eb9c02e8600baafbd982a577490252dd0eb3a0d274e7368a08b18"

SEGMENT_ID="segment:00000000"

SEGMENT_PATH=Path("results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg")

SEGMENT_BYTES=1888934699

SEGMENT_SHA256="a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9"

SOURCE_GGUF=Path.home()/"qwen2.5-coder-q8_0.gguf"

LLAMA_ROOT=Path.home()/"llama.cpp"

LLAMA_HEAD="4cf5cab65d5257be31e7623eb552b1861e969c75"

SHARED_LIBRARY=Path("/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libllama.so.0.0.10318")

SHARED_LIBRARY_BYTES=3613896

SHARED_LIBRARY_SHA256="a56bdf41b3409ae870c584ecf23e7e65915451ae313d057d92958be0d94af802"

V2_BUILD_AUTHORITY_PATH=Path('experiments/model_fractal/maf_phase_6e_d_class_a_compatibility_build_authority_v1.json')
V2_BUILD_AUTHORITY_BYTES=2072
V2_BUILD_AUTHORITY_SHA256='557d9140e9fb946e028185ae7fdcda851a1f3b231772f56768f46c541a5ebaa6'
V2_BUILD_AUTHORITY_GIT_BLOB='9ab1acb42edd149fa055f4ce42f9dbe58f142519'
V2_COMPATIBILITY_BUILD_ROOT=Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan')
V2_RUNTIME_POLICY='SELF-CONTAINED-RUNPATH'
V2_RUNTIME_CLOSURE=(
    (Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libggml-base.so.0.19.0'), 844216, 'fef82c67f833e96bbde5119e0069845b0bfcd6e7cdfc476dcc20d0758d28e43a', 'libggml-base.so.0'),
    (Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libggml-cpu.so.0.19.0'), 1018200, '4d99c30967217a2aa7a5dab35b2ab860c473742d4da9666786b63c25d2ef40a1', 'libggml-cpu.so.0'),
    (Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libggml-vulkan.so.0.19.0'), 51164696, '58ea5461858079ba84b0bce10f95a9f2a085803f29e14be57be26dd6750b9fee', 'libggml-vulkan.so.0'),
    (Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libggml.so.0.19.0'), 82152, 'b4c9363cb62a44c60b59bb9d104adfa4a4f41fd8798bff2ed048b40f9dc45474', 'libggml.so.0'),
    (Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libllama.so.0.0.10318'), 3613896, 'a56bdf41b3409ae870c584ecf23e7e65915451ae313d057d92958be0d94af802', 'libllama.so.0'),
)
_V2_RUNTIME_AUTHORITY_VERIFIED=False

def _v2_runtime_sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block=stream.read(1024*1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()

def _v2_verify_runtime_authorities():
    global _V2_RUNTIME_AUTHORITY_VERIFIED
    if _V2_RUNTIME_AUTHORITY_VERIFIED:
        return

    authority=V2_BUILD_AUTHORITY_PATH
    if not authority.is_file() or authority.is_symlink():
        raise RuntimeError("V2 build authority missing or symlink")
    if authority.stat().st_size != V2_BUILD_AUTHORITY_BYTES:
        raise RuntimeError("V2 build authority byte mismatch")
    if _v2_runtime_sha256(authority) != V2_BUILD_AUTHORITY_SHA256:
        raise RuntimeError("V2 build authority SHA mismatch")

    repo_root=Path(__file__).resolve().parents[2]
    blob_check=subprocess.run(
        ["git","rev-parse","HEAD:"+str(V2_BUILD_AUTHORITY_PATH)],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if blob_check.returncode != 0:
        raise RuntimeError("V2 build authority Git lookup failed")
    if blob_check.stdout.decode().strip() != V2_BUILD_AUTHORITY_GIT_BLOB:
        raise RuntimeError("V2 build authority Git blob mismatch")

    payload=json.loads(authority.read_text(encoding="utf-8"))
    library=payload.get("library",{})
    if library.get("sha256") != SHARED_LIBRARY_SHA256:
        raise RuntimeError("V2 manifest/libllama SHA mismatch")
    if library.get("bytes") != SHARED_LIBRARY_BYTES:
        raise RuntimeError("V2 manifest/libllama bytes mismatch")
    if Path(library.get("path","")).resolve() != SHARED_LIBRARY.resolve():
        raise RuntimeError("V2 manifest/libllama path mismatch")

    root=V2_COMPATIBILITY_BUILD_ROOT.resolve()
    sonames=[]
    expected_by_soname={}

    for path,size,digest,soname in V2_RUNTIME_CLOSURE:
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("V2 runtime file missing/symlink: "+str(path))
        real=path.resolve()
        if not real.is_relative_to(root):
            raise RuntimeError("V2 runtime file escapes compatibility build: "+str(path))
        if path.stat().st_size != size:
            raise RuntimeError("V2 runtime byte mismatch: "+str(path))
        if _v2_runtime_sha256(path) != digest:
            raise RuntimeError("V2 runtime SHA mismatch: "+str(path))
        if soname in expected_by_soname:
            raise RuntimeError("V2 duplicate runtime SONAME: "+soname)
        expected_by_soname[soname]=real
        sonames.append(soname)

    if len(V2_RUNTIME_CLOSURE) != 5 or len(expected_by_soname) != 5:
        raise RuntimeError("V2 runtime closure cardinality mismatch")

    vulkan=payload.get("vulkan_backend",{})
    vr=[item for item in V2_RUNTIME_CLOSURE if item[3] == "libggml-vulkan.so.0"]
    if len(vr) != 1:
        raise RuntimeError("V2 Vulkan closure cardinality mismatch")
    vp,vs,vd,_=vr[0]
    if vulkan.get("sha256") != vd or vulkan.get("bytes") != vs:
        raise RuntimeError("V2 manifest/Vulkan authority mismatch")
    if Path(vulkan.get("path","")).resolve() != vp.resolve():
        raise RuntimeError("V2 manifest/Vulkan path mismatch")

    ld=os.environ.get("LD_LIBRARY_PATH","")
    if ld:
        for raw_dir in ld.split(":"):
            if not raw_dir:
                continue
            directory=Path(raw_dir).expanduser()
            try:
                directory=directory.resolve()
            except OSError:
                continue
            if directory == root or directory == (root/"bin"):
                continue
            for soname in sonames:
                candidate=directory/soname
                if candidate.exists():
                    raise RuntimeError("V2 conflicting LD_LIBRARY_PATH SONAME: "+str(candidate))

    maps_path=Path("/proc/self/maps")
    if not maps_path.is_file():
        raise RuntimeError("V2 cannot inspect /proc/self/maps before CDLL")

    maps_text=maps_path.read_text(encoding="utf-8",errors="replace")
    for line in maps_text.splitlines():
        fields=line.split()
        if len(fields) < 6:
            continue
        raw_path=fields[-1]
        if not raw_path.startswith("/"):
            continue
        mapped=Path(raw_path)
        name=mapped.name
        for soname,expected in expected_by_soname.items():
            if not name.startswith(soname):
                continue
            try:
                resolved=mapped.resolve()
            except OSError:
                resolved=mapped
            if resolved != expected:
                raise RuntimeError("V2 conflicting preloaded SONAME: "+str(mapped))

    _V2_RUNTIME_AUTHORITY_VERIFIED=True

def _v2_verified_cdll(path,*args,**kwargs):
    _v2_verify_runtime_authorities()
    requested=Path(os.fspath(path)).resolve()
    if requested != SHARED_LIBRARY.resolve():
        raise RuntimeError("V2 unauthorized CDLL path: "+str(requested))
    return ctypes.CDLL(path,*args,**kwargs)


JOIN_OBJECT_FIELD="object_pk"

JOIN_OFFSET_FIELD="object_offset"

JOIN_LENGTH_FIELD="object_length"

JOIN_SEGMENT_FIELD="segment_id"

JOIN_TENSOR_FIELD="tensor_name"

BASELINE_UNTRACKED_COUNT=440

BASELINE_UNTRACKED_RAW_SHA256='f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd'

SCHEMA='openmind.maf.phase_6e_d.class_a_inference_logit_parity_validation.v1'

PASS_DISPOSITION='PASS — CLASS-A INFERENCE LOGIT PARITY VALIDATED'

FAIL_DISPOSITION='FAIL — CLASS-A INFERENCE LOGIT PARITY VALIDATION'

REQUIRED_SYMBOLS=(
    "ggml_get_name",
    "ggml_nelements",
    "ggml_nbytes",
    "ggml_backend_tensor_set",
    "llama_model_default_params",
    "llama_model_init_from_user",
    "llama_model_free",
    "gguf_init_empty",
    "gguf_free",
    "gguf_set_val_u32",
    "gguf_set_val_f32",
    "gguf_set_val_bool",
    "gguf_set_val_str",
    "gguf_set_arr_data",
    "gguf_set_arr_str",
    "ggml_init",
    "ggml_free",
    "ggml_new_tensor",
    "ggml_set_name",
    "gguf_add_tensor",
    "gguf_set_tensor_type",
)

class PositiveValidationError(RuntimeError):
    pass

class PositiveValidationSpentError(PositiveValidationError):
    pass

class _GGMLInitParams(ctypes.Structure):
    _fields_=(
        ("mem_size",ctypes.c_size_t),
        ("mem_buffer",ctypes.c_void_p),
        ("no_alloc",ctypes.c_bool),
    )

def need(value,message):
    if not value:
        raise PositiveValidationError(message)

def run(*args,cwd=None,check=True):
    result=subprocess.run(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check and result.returncode!=0:
        raise PositiveValidationError(
            "command failed: "
            +" ".join(args)
            +" | "
            +result.stderr.decode(errors="replace").strip()
        )

    return result

def git(*args,check=True):
    return run(
        "git",
        *args,
        check=check,
    )

def sha_file(path):
    digest=hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            block=stream.read(1024*1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()

def canonical_json_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",",":"),
    ).encode("utf-8")

def jsonable(value):
    if dataclasses.is_dataclass(value):
        return jsonable(
            dataclasses.asdict(value)
        )

    if isinstance(value,dict):
        return {
            str(key):jsonable(item)
            for key,item in value.items()
        }

    if isinstance(value,(list,tuple,set)):
        return [
            jsonable(item)
            for item in value
        ]

    if isinstance(value,Path):
        return str(value)

    if isinstance(value,(str,int,float,bool)) or value is None:
        return value

    if isinstance(value,bytes):
        return {
            "bytes_length":len(value),
            "sha256":hashlib.sha256(value).hexdigest(),
        }

    return repr(value)

def as_void_p(value):
    if isinstance(value,ctypes.c_void_p):
        return value

    return ctypes.c_void_p(value)

def atomic_write_result(value):
    need(
        not RESULT_PATH.exists(),
        "result path already exists",
    )

    raw=canonical_json_bytes(
        value
    )

    temp_name=None

    try:
        fd,temp_name=tempfile.mkstemp(
            prefix=RESULT_PATH.name+".building.",
            dir=str(RESULT_PATH.parent),
        )

        with os.fdopen(fd,"wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(
                stream.fileno()
            )

        os.replace(
            temp_name,
            RESULT_PATH,
        )

        temp_name=None

    finally:
        if (
            temp_name is not None
            and Path(temp_name).exists()
        ):
            Path(temp_name).unlink()

    reopened=RESULT_PATH.read_bytes()

    need(
        reopened==raw,
        "result reopen mismatch",
    )

    need(
        not reopened.endswith(b"\n"),
        "result contains trailing newline",
    )

    return (
        len(reopened),
        hashlib.sha256(reopened).hexdigest(),
    )

def runner_commit_checkpoint():
    need(
        git(
            "branch",
            "--show-current",
        ).stdout.decode().strip()==BRANCH,
        "branch mismatch",
    )

    execution_head=git(
        "rev-parse",
        "HEAD",
    ).stdout.decode().strip()

    need(
        git(
            "merge-base",
            PROTOCOL_FREEZE_HEAD,
            "HEAD",
        ).stdout.decode().strip()==PROTOCOL_FREEZE_HEAD,
        "frozen protocol commit is not an ancestor of execution HEAD",
    )

    need(
        git(
            "show",
            "-s",
            "--format=%s",
            "HEAD",
        ).stdout.decode().strip()==RUNNER_COMMIT_SUBJECT,
        "runner freeze commit subject mismatch",
    )

    expected_status=(
        "A\t"
        +str(RUNNER_PATH)
        +"\n"
    )

    need(
        git(
            "diff-tree",
            "--no-commit-id",
            "--name-status",
            "-r",
            "HEAD",
        ).stdout.decode()==expected_status,
        "runner freeze is not exact one-file ADD",
    )

    expected_paths=str(
        RUNNER_PATH
    ).encode()+b"\0"

    need(
        git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "-z",
            "HEAD",
        ).stdout==expected_paths,
        "runner freeze path set mismatch",
    )

    need(
        git(
            "diff",
            "--name-only",
            "-z",
        ).stdout==b"",
        "tracked worktree dirty",
    )

    need(
        git(
            "diff",
            "--cached",
            "--name-only",
            "-z",
        ).stdout==b"",
        "index not empty",
    )

    current_runner=Path(
        __file__
    ).resolve().read_bytes()

    runner_sha=hashlib.sha256(
        current_runner
    ).hexdigest()

    committed_runner=git(
        "show",
        "HEAD:"+str(RUNNER_PATH),
    ).stdout

    need(
        committed_runner==current_runner,
        "executing runner bytes differ from frozen commit",
    )

    for path,digest in (
        (PROTOCOL_PATH,PROTOCOL_SHA256),
        (PROVIDER_PATH,PROVIDER_SHA256),
        (RESIDENT_PATH,RESIDENT_SHA256),
        (SEGMENT_READER_PATH,SEGMENT_READER_SHA256),
        (METADATA_PATH,METADATA_SHA256),
        (JOIN_PATH,JOIN_SHA256),
        (GENERATION_PATH,GENERATION_SHA256),
        (RECOVERY_QUALIFICATION_PATH,RECOVERY_QUALIFICATION_SHA256),
        (NEGATIVE_RESULT_PATH,NEGATIVE_RESULT_SHA256),
    ):
        need(
            path.is_file(),
            "missing frozen authority: "+str(path),
        )

        need(
            sha_file(path)==digest,
            "authority SHA mismatch: "+str(path),
        )

    need(
        git(
            "rev-parse",
            "HEAD:"+str(PROTOCOL_PATH),
        ).stdout.decode().strip()==PROTOCOL_BLOB,
        "protocol blob mismatch",
    )

    need(
        git(
            "rev-parse",
            "HEAD:"+str(PROVIDER_PATH),
        ).stdout.decode().strip()==PROVIDER_BLOB,
        "provider blob mismatch",
    )

    need(
        run(
            "git",
            "rev-parse",
            "HEAD",
            cwd=LLAMA_ROOT,
        ).stdout.decode().strip()==LLAMA_HEAD,
        "llama.cpp HEAD mismatch",
    )

    need(
        run(
            "git",
            "status",
            "--porcelain=v1",
            "-uno",
            cwd=LLAMA_ROOT,
        ).stdout==b"",
        "llama.cpp tracked tree dirty",
    )

    library_stat=os.lstat(
        SHARED_LIBRARY
    )

    need(
        stat.S_ISREG(
            library_stat.st_mode
        )
        and not stat.S_ISLNK(
            library_stat.st_mode
        ),
        "shared library is not regular nonsymlink file",
    )

    need(
        library_stat.st_size==SHARED_LIBRARY_BYTES,
        "shared-library byte count mismatch",
    )

    need(
        sha_file(
            SHARED_LIBRARY
        )==SHARED_LIBRARY_SHA256,
        "shared-library SHA mismatch",
    )

    segment_stat=os.lstat(
        SEGMENT_PATH
    )

    need(
        stat.S_ISREG(
            segment_stat.st_mode
        )
        and not stat.S_ISLNK(
            segment_stat.st_mode
        ),
        "qualified segment is not regular nonsymlink file",
    )

    need(
        segment_stat.st_size==SEGMENT_BYTES,
        "qualified segment byte count mismatch",
    )

    need(
        not RESULT_PATH.exists(),
        "positive result already exists",
    )

    raw_untracked=git(
        "ls-files",
        "-z",
        "--others",
        "--exclude-standard",
    ).stdout

    paths=[
        item
        for item in raw_untracked.split(b"\0")
        if item
    ]

    need(
        len(paths)==BASELINE_UNTRACKED_COUNT,
        "untracked count mismatch",
    )

    need(
        hashlib.sha256(
            raw_untracked
        ).hexdigest()==BASELINE_UNTRACKED_RAW_SHA256,
        "raw-NUL untracked baseline mismatch",
    )

    sentinel=(
        Path.home()
        /".openmind_authoritative_slots"
        /(
            "phase_6e_d_class_a_inference_logit_parity_v1_"
            +runner_sha
            +".spent"
        )
    )

    if sentinel.exists():
        raise PositiveValidationSpentError(
            "positive runner slot already spent"
        )

    return (
        execution_head,
        runner_sha,
        sentinel,
    )

class ProtectedIOGuard:
    def __init__(self):
        self.lock=threading.RLock()

        self.segment_window_depth=0

        self.source_gguf_opens=0
        self.authorized_segment_opens=0
        self.unauthorized_segment_opens=0
        self.conventional_complete_gguf_files_created=0

        self.source_path=SOURCE_GGUF.expanduser().resolve(
            strict=False
        )

        self.segment_path=SEGMENT_PATH.resolve(
            strict=True
        )

        self.source_identity=None

        try:
            source_stat=os.stat(
                SOURCE_GGUF,
                follow_symlinks=True,
            )

            self.source_identity=(
                source_stat.st_dev,
                source_stat.st_ino,
            )

        except FileNotFoundError:
            pass

        segment_stat=os.stat(
            SEGMENT_PATH,
            follow_symlinks=True,
        )

        self.segment_identity=(
            segment_stat.st_dev,
            segment_stat.st_ino,
        )

    def path_value(self,value):
        if isinstance(value,int):
            return None

        try:
            return Path(
                os.fsdecode(
                    os.fspath(value)
                )
            )
        except Exception:
            return None

    def same_identity(self,path,identity):
        if identity is None:
            return False

        try:
            current=os.stat(
                path,
                follow_symlinks=True,
            )
        except OSError:
            return False

        return (
            current.st_dev,
            current.st_ino,
        )==identity

    def write_intent(self,mode,flags):
        if isinstance(mode,str):
            if any(
                token in mode
                for token in (
                    "w",
                    "a",
                    "x",
                    "+",
                )
            ):
                return True

        if isinstance(flags,int):
            mask=(
                os.O_WRONLY
                |os.O_RDWR
                |os.O_CREAT
                |os.O_TRUNC
                |os.O_APPEND
            )

            if flags&mask:
                return True

        return False

    def audit_hook(self,event,args):
        if event!="open" or not args:
            return

        path=self.path_value(
            args[0]
        )

        if path is None:
            return

        mode=args[1] if len(args)>1 else None
        flags=args[2] if len(args)>2 else None

        resolved=path.expanduser().resolve(
            strict=False
        )

        source_match=(
            resolved==self.source_path
            or self.same_identity(
                path,
                self.source_identity,
            )
        )

        if source_match:
            with self.lock:
                self.source_gguf_opens+=1

            raise PermissionError(
                "source GGUF access prohibited"
            )

        if (
            path.suffix.lower()==".gguf"
            and self.write_intent(
                mode,
                flags,
            )
        ):
            with self.lock:
                self.conventional_complete_gguf_files_created+=1

            raise PermissionError(
                "conventional GGUF creation prohibited"
            )

        segment_match=(
            resolved==self.segment_path
            or self.same_identity(
                path,
                self.segment_identity,
            )
        )

        if segment_match:
            with self.lock:
                if self.segment_window_depth>0:
                    self.authorized_segment_opens+=1
                    return

                self.unauthorized_segment_opens+=1

            raise PermissionError(
                "qualified segment access outside guarded reader window"
            )

        if path.suffix.lower()==".mafseg":
            with self.lock:
                self.unauthorized_segment_opens+=1

            raise PermissionError(
                "unauthorized MAF segment access"
            )

    @contextmanager
    def authorized_segment_window(self):
        with self.lock:
            self.segment_window_depth+=1

        try:
            yield

        finally:
            with self.lock:
                self.segment_window_depth-=1

def load_single_library():
    library=_v2_verified_cdll(
        str(SHARED_LIBRARY)
    )

    missing=[]

    for symbol in REQUIRED_SYMBOLS:
        try:
            getattr(
                library,
                symbol,
            )
        except AttributeError:
            missing.append(
                symbol
            )

    need(
        not missing,
        "qualified library missing symbols: "
        +",".join(missing),
    )

    return library

def bind_construction_ffi(library):
    library.gguf_init_empty.argtypes=[]
    library.gguf_init_empty.restype=ctypes.c_void_p

    library.gguf_free.argtypes=[
        ctypes.c_void_p
    ]
    library.gguf_free.restype=None

    library.gguf_set_val_u32.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_uint32,
    ]
    library.gguf_set_val_u32.restype=None

    library.gguf_set_val_f32.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_float,
    ]
    library.gguf_set_val_f32.restype=None

    library.gguf_set_val_bool.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_bool,
    ]
    library.gguf_set_val_bool.restype=None

    library.gguf_set_val_str.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    library.gguf_set_val_str.restype=None

    library.gguf_set_arr_data.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_size_t,
    ]
    library.gguf_set_arr_data.restype=None

    library.gguf_set_arr_str.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.POINTER(
            ctypes.c_char_p
        ),
        ctypes.c_size_t,
    ]
    library.gguf_set_arr_str.restype=None

    library.ggml_init.argtypes=[
        _GGMLInitParams
    ]
    library.ggml_init.restype=ctypes.c_void_p

    library.ggml_free.argtypes=[
        ctypes.c_void_p
    ]
    library.ggml_free.restype=None

    library.ggml_new_tensor.argtypes=[
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(
            ctypes.c_int64
        ),
    ]
    library.ggml_new_tensor.restype=ctypes.c_void_p

    library.ggml_set_name.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
    ]
    library.ggml_set_name.restype=ctypes.c_void_p

    library.gguf_add_tensor.argtypes=[
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    library.gguf_add_tensor.restype=None

    library.gguf_set_tensor_type.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    library.gguf_set_tensor_type.restype=None

    library.llama_model_free.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_model_free.restype=None

def encode_utf8(value,label):
    need(
        isinstance(value,str),
        label+" must be string",
    )

    raw=value.encode(
        "utf-8"
    )

    need(
        b"\0" not in raw,
        label+" contains embedded NUL",
    )

    return raw

def float32_from_authority(record):
    hex_value=record.get(
        "ieee754_hex"
    )

    need(
        isinstance(hex_value,str),
        "float metadata lacks ieee754_hex",
    )

    normalized=hex_value.lower()

    if normalized.startswith("0x"):
        normalized=normalized[2:]

    need(
        len(normalized)==8,
        "float metadata ieee754_hex length mismatch",
    )

    raw=bytes.fromhex(
        normalized
    )

    decimal=record.get(
        "value"
    )

    need(
        isinstance(decimal,(int,float))
        and not isinstance(decimal,bool),
        "float decimal companion invalid",
    )

    little_value=struct.unpack(
        "<f",
        raw,
    )[0]

    big_value=struct.unpack(
        ">f",
        raw,
    )[0]

    little_match=(
        struct.pack(
            "<f",
            ctypes.c_float(
                float(decimal)
            ).value,
        )==raw
    )

    big_match=(
        struct.pack(
            ">f",
            ctypes.c_float(
                float(decimal)
            ).value,
        )==raw
    )

    need(
        little_match or big_match,
        "float ieee754_hex does not match decimal companion",
    )

    if little_match:
        return little_value

    return big_value

def build_metadata_context(library):
    authority=json.loads(
        METADATA_PATH.read_text()
    )

    records=authority.get(
        "metadata"
    )

    tensors=authority.get(
        "tensors"
    )

    need(
        isinstance(records,list)
        and len(records)==26,
        "metadata record count mismatch",
    )

    need(
        isinstance(tensors,list)
        and len(tensors)==339,
        "tensor declaration count mismatch",
    )

    need(
        [
            row.get("ordinal")
            for row in records
        ]==list(range(26)),
        "metadata ordinal mismatch",
    )

    need(
        [
            row.get("ordinal")
            for row in tensors
        ]==list(range(339)),
        "tensor ordinal mismatch",
    )

    gguf_context=library.gguf_init_empty()

    need(
        bool(gguf_context),
        "gguf_init_empty returned null",
    )

    ggml_context=None

    try:
        root_counts=Counter()
        array_counts=Counter()

        for record in records:
            key=encode_utf8(
                record.get("key"),
                "metadata key",
            )

            value_type=record.get(
                "gguf_value_type"
            )

            root_counts[
                value_type
            ]+=1

            if value_type==4:
                value=record.get(
                    "value"
                )

                need(
                    isinstance(value,int)
                    and not isinstance(value,bool)
                    and 0<=value<=0xffffffff,
                    "UINT32 metadata invalid",
                )

                library.gguf_set_val_u32(
                    gguf_context,
                    key,
                    ctypes.c_uint32(value),
                )

            elif value_type==6:
                value=float32_from_authority(
                    record
                )

                library.gguf_set_val_f32(
                    gguf_context,
                    key,
                    ctypes.c_float(value),
                )

            elif value_type==7:
                value=record.get(
                    "value"
                )

                need(
                    isinstance(value,bool),
                    "BOOL metadata invalid",
                )

                library.gguf_set_val_bool(
                    gguf_context,
                    key,
                    ctypes.c_bool(value),
                )

            elif value_type==8:
                value=encode_utf8(
                    record.get("value"),
                    "STRING metadata",
                )

                library.gguf_set_val_str(
                    gguf_context,
                    key,
                    value,
                )

            elif value_type==9:
                element_type=record.get(
                    "array_element_type"
                )

                values=record.get(
                    "value"
                )

                need(
                    isinstance(values,list),
                    "ARRAY metadata invalid",
                )

                array_counts[
                    element_type
                ]+=1

                if element_type==5:
                    need(
                        all(
                            isinstance(value,int)
                            and not isinstance(value,bool)
                            and -2147483648<=value<=2147483647
                            for value in values
                        ),
                        "INT32 metadata array invalid",
                    )

                    array_type=ctypes.c_int32*len(
                        values
                    )

                    array_value=array_type(
                        *values
                    )

                    library.gguf_set_arr_data(
                        gguf_context,
                        key,
                        ctypes.c_int(5),
                        ctypes.cast(
                            array_value,
                            ctypes.c_void_p,
                        ),
                        ctypes.c_size_t(
                            len(values)
                        ),
                    )

                elif element_type==8:
                    encoded=[
                        encode_utf8(
                            value,
                            "STRING array element",
                        )
                        for value in values
                    ]

                    array_type=ctypes.c_char_p*len(
                        encoded
                    )

                    array_value=array_type(
                        *encoded
                    )

                    library.gguf_set_arr_str(
                        gguf_context,
                        key,
                        array_value,
                        ctypes.c_size_t(
                            len(encoded)
                        ),
                    )

                else:
                    raise PositiveValidationError(
                        "unsupported frozen array type"
                    )

            else:
                raise PositiveValidationError(
                    "unsupported frozen GGUF root type"
                )

        need(
            dict(root_counts)=={
                4:11,
                6:2,
                7:1,
                8:9,
                9:3,
            },
            "root metadata type distribution mismatch",
        )

        need(
            dict(array_counts)=={
                5:1,
                8:2,
            },
            "array element type distribution mismatch",
        )

        ggml_context=library.ggml_init(
            _GGMLInitParams(
                64*1024*1024,
                None,
                True,
            )
        )

        need(
            bool(ggml_context),
            "temporary ggml_init returned null",
        )

        names=set()

        for record in tensors:
            name=record.get(
                "name"
            )

            need(
                isinstance(name,str)
                and name
                and name not in names,
                "tensor name missing or duplicated",
            )

            names.add(
                name
            )

            dims=record.get(
                "dims"
            )

            need(
                isinstance(dims,list)
                and 1<=len(dims)<=4
                and all(
                    isinstance(value,int)
                    and value>0
                    for value in dims
                ),
                "tensor dimensions invalid",
            )

            ggml_type=record.get(
                "ggml_type"
            )

            need(
                isinstance(ggml_type,int)
                and ggml_type>=0,
                "tensor GGML type invalid",
            )

            ne_type=ctypes.c_int64*len(
                dims
            )

            ne=ne_type(
                *dims
            )

            tensor=library.ggml_new_tensor(
                ggml_context,
                ctypes.c_int(
                    ggml_type
                ),
                ctypes.c_int(
                    len(dims)
                ),
                ne,
            )

            need(
                bool(tensor),
                "ggml_new_tensor returned null",
            )

            name_raw=encode_utf8(
                name,
                "tensor name",
            )

            named=library.ggml_set_name(
                tensor,
                name_raw,
            )

            need(
                bool(named),
                "ggml_set_name returned null",
            )

            library.gguf_add_tensor(
                gguf_context,
                tensor,
            )

            library.gguf_set_tensor_type(
                gguf_context,
                name_raw,
                ctypes.c_int(
                    ggml_type
                ),
            )

        return (
            gguf_context,
            ggml_context,
            {
                "metadata_records":26,
                "tensor_declarations":339,
                "root_type_counts":{
                    str(key):value
                    for key,value in sorted(
                        root_counts.items()
                    )
                },
                "array_element_type_counts":{
                    str(key):value
                    for key,value in sorted(
                        array_counts.items()
                    )
                },
                "temporary_ggml_no_alloc":True,
                "provider_model_no_alloc_required":False,
            },
        )

    except BaseException:
        if ggml_context:
            library.ggml_free(
                ggml_context
            )

        library.gguf_free(
            gguf_context
        )

        raise

def import_frozen_provider():
    module_directory=str(
        PROVIDER_PATH.parent.resolve()
    )

    if module_directory not in sys.path:
        sys.path.insert(
            0,
            module_directory,
        )

    spec=importlib.util.spec_from_file_location(
        "openmind_phase_6e_d_positive_provider",
        PROVIDER_PATH,
    )

    need(
        spec is not None
        and spec.loader is not None,
        "provider import specification unavailable",
    )

    module=importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        spec.name
    ]=module

    spec.loader.exec_module(
        module
    )

    need(
        hasattr(
            module,
            "ClassAMAFBackedTensorProvider",
        ),
        "provider class unavailable",
    )

    return module

def derive_active_provenance():
    record={
        "schema":"openmind.maf_active_generation.v1",
        "active_generation_version":"maf_active_generation_v1",
        "model_pk":MODEL_PK,
        "generation_pk":GENERATION_PK,
        "generation_manifest_sha256":GENERATION_SHA256,
    }

    raw=canonical_json_bytes(
        record
    )

    digest=hashlib.sha256(
        raw
    ).hexdigest()

    need(
        digest==DERIVED_ACTIVE_SHA256,
        "derived active provenance SHA mismatch",
    )

    return digest

def build_direct_resident_directory(provider_module):
    generation=json.loads(
        GENERATION_PATH.read_text()
    )

    join=json.loads(
        JOIN_PATH.read_text()
    )

    need(
        generation.get(
            "generation_pk"
        )==GENERATION_PK,
        "generation PK mismatch",
    )

    descriptor=generation.get(
        "descriptor"
    )

    need(
        isinstance(descriptor,dict)
        and descriptor.get(
            "model_pk"
        )==MODEL_PK,
        "generation model PK mismatch",
    )

    objects=descriptor.get(
        "objects"
    )

    segments=descriptor.get(
        "segments"
    )

    need(
        isinstance(objects,list)
        and len(objects)==339,
        "generation object count mismatch",
    )

    need(
        isinstance(segments,list)
        and len(segments)==1,
        "generation segment count mismatch",
    )

    segment=segments[0]

    need(
        segment.get(
            "segment_id"
        )==SEGMENT_ID,
        "generation segment ID mismatch",
    )

    need(
        segment.get(
            "segment_length"
        )==SEGMENT_BYTES,
        "generation segment length mismatch",
    )

    need(
        segment.get(
            "segment_sha256"
        )==SEGMENT_SHA256,
        "generation segment SHA mismatch",
    )

    records=join.get(
        "records"
    )

    need(
        isinstance(records,list)
        and len(records)==339,
        "join record count mismatch",
    )

    join_by_pk={}

    for record in records:
        object_pk=record.get(
            JOIN_OBJECT_FIELD
        )

        need(
            isinstance(object_pk,str)
            and object_pk
            and object_pk not in join_by_pk,
            "join object PK invalid or duplicated",
        )

        join_by_pk[
            object_pk
        ]=record

    entries={}

    segment_path_string=str(
        SEGMENT_PATH.resolve(
            strict=True
        )
    )

    for row in objects:
        object_pk=row.get(
            "object_pk"
        )

        need(
            isinstance(object_pk,str)
            and object_pk
            and object_pk in join_by_pk,
            "generation object PK missing from join",
        )

        join_record=join_by_pk[
            object_pk
        ]

        need(
            row.get(
                "segment_id"
            )==join_record.get(
                JOIN_SEGMENT_FIELD
            ),
            "segment ID placement mismatch",
        )

        need(
            row.get(
                "offset"
            )==join_record.get(
                JOIN_OFFSET_FIELD
            ),
            "object offset placement mismatch",
        )

        need(
            row.get(
                "length"
            )==join_record.get(
                JOIN_LENGTH_FIELD
            ),
            "object length placement mismatch",
        )

        entry=provider_module.resident.ResidentPKEntry(
            model_pk=MODEL_PK,
            generation_pk=GENERATION_PK,
            generation_manifest_sha256=GENERATION_SHA256,
            object_pk=object_pk,
            segment_id=row["segment_id"],
            offset=row["offset"],
            length=row["length"],
            object_file_sha256=row["object_file_sha256"],
            payload_sha256=row["payload_sha256"],
            segment_length=SEGMENT_BYTES,
            segment_sha256=SEGMENT_SHA256,
            segment_path=segment_path_string,
        )

        key=(
            MODEL_PK,
            provider_module.resident.OBJECT_PK_KIND,
            object_pk,
        )

        need(
            key not in entries,
            "resident key duplicated",
        )

        entries[
            key
        ]=entry

    need(
        len(entries)==339,
        "resident entry count mismatch",
    )

    active_sha=derive_active_provenance()

    snapshot=provider_module.resident.ResidentPKSnapshot(
        model_pk=MODEL_PK,
        generation_pk=GENERATION_PK,
        generation_manifest_sha256=GENERATION_SHA256,
        active_record_sha256=active_sha,
        entries=MappingProxyType(
            entries
        ),
    )

    need(
        snapshot.entry_count==339,
        "snapshot entry count mismatch",
    )

    directory=provider_module.resident.ResidentPKDirectory()

    need(
        directory._snapshot is None,
        "fresh ResidentPKDirectory unexpectedly contains snapshot",
    )

    directory._snapshot=snapshot

    need(
        directory.snapshot is snapshot,
        "direct snapshot publication mismatch",
    )

    lookup_count=0

    for object_pk in sorted(
        join_by_pk
    ):
        entry=directory.lookup(
            model_pk=MODEL_PK,
            pk_kind=provider_module.resident.OBJECT_PK_KIND,
            logical_pk=object_pk,
            expected_generation_pk=GENERATION_PK,
        )

        need(
            entry.object_pk==object_pk,
            "resident lookup object PK mismatch",
        )

        need(
            entry.generation_manifest_sha256==GENERATION_SHA256,
            "resident generation manifest SHA mismatch",
        )

        need(
            entry.segment_id==SEGMENT_ID,
            "resident segment ID mismatch",
        )

        need(
            entry.segment_length==SEGMENT_BYTES,
            "resident segment length mismatch",
        )

        need(
            entry.segment_sha256==SEGMENT_SHA256,
            "resident segment SHA mismatch",
        )

        lookup_count+=1

    need(
        lookup_count==339,
        "resident pre-provider lookup qualification count mismatch",
    )

    return (
        directory,
        join_by_pk,
        {
            "mode":"direct_in_memory_frozen_snapshot",
            "entry_count":339,
            "pre_provider_lookup_count":lookup_count,
            "generation_manifest_sha256":GENERATION_SHA256,
            "derived_active_record_sha256":active_sha,
            "active_record_file_created":False,
            "activation_api_called":False,
        },
    )

class SerializedReadTelemetry:
    def __init__(
        self,
        guard,
        provider_module,
        join_by_pk,
    ):
        self.guard=guard
        self.provider_module=provider_module
        self.join_by_pk=join_by_pk

        self.reader_calls=0
        self.serialized_bytes=0
        self.object_pks=[]
        self.tensor_names=[]

        self.original=(
            provider_module
            .segment_reader
            .read_serialized_object
        )

    def wrapper(
        self,
        entry,
        expected_generation_pk,
    ):
        need(
            expected_generation_pk==GENERATION_PK,
            "serialized reader generation request mismatch",
        )

        need(
            entry.model_pk==MODEL_PK,
            "serialized reader model PK mismatch",
        )

        need(
            entry.generation_pk==GENERATION_PK,
            "serialized reader generation PK mismatch",
        )

        need(
            entry.generation_manifest_sha256==GENERATION_SHA256,
            "serialized reader generation manifest SHA mismatch",
        )

        need(
            Path(
                entry.segment_path
            ).resolve(
                strict=True
            )==SEGMENT_PATH.resolve(
                strict=True
            ),
            "serialized reader segment path mismatch",
        )

        need(
            entry.segment_length==SEGMENT_BYTES,
            "serialized reader segment length mismatch",
        )

        need(
            entry.segment_sha256==SEGMENT_SHA256,
            "serialized reader segment SHA mismatch",
        )

        record=self.join_by_pk.get(
            entry.object_pk
        )

        need(
            record is not None,
            "serialized reader object PK absent from join",
        )

        need(
            entry.segment_id==record.get(
                JOIN_SEGMENT_FIELD
            ),
            "serialized reader segment ID mismatch",
        )

        need(
            entry.offset==record.get(
                JOIN_OFFSET_FIELD
            ),
            "serialized reader object offset mismatch",
        )

        need(
            entry.length==record.get(
                JOIN_LENGTH_FIELD
            ),
            "serialized reader object length mismatch",
        )

        need(
            entry.offset>=0
            and entry.length>0
            and entry.offset+entry.length<=SEGMENT_BYTES,
            "serialized reader object range outside segment",
        )

        with self.guard.authorized_segment_window():
            raw=self.original(
                entry,
                expected_generation_pk,
            )

        need(
            isinstance(raw,(bytes,bytearray)),
            "serialized reader returned nonbytes",
        )

        need(
            len(raw)==entry.length,
            "serialized reader byte count mismatch",
        )

        self.reader_calls+=1
        self.serialized_bytes+=len(raw)
        self.object_pks.append(
            entry.object_pk
        )
        self.tensor_names.append(
            record.get(
                JOIN_TENSOR_FIELD
            )
        )

        return raw

    def install(self):
        (
            self.provider_module
            .segment_reader
            .read_serialized_object
        )=self.wrapper

    def restore(self):
        (
            self.provider_module
            .segment_reader
            .read_serialized_object
        )=self.original

    def record(self):
        object_counts=Counter(
            self.object_pks
        )

        tensor_counts=Counter(
            self.tensor_names
        )

        return {
            "reader_calls":self.reader_calls,
            "serialized_bytes":self.serialized_bytes,
            "object_pks":list(
                self.object_pks
            ),
            "unique_object_pks":len(
                object_counts
            ),
            "repeated_object_pks":{
                key:value
                for key,value in sorted(
                    object_counts.items()
                )
                if value>1
            },
            "tensor_names":list(
                self.tensor_names
            ),
            "unique_tensor_names":len(
                tensor_counts
            ),
            "duplicate_tensor_names":{
                key:value
                for key,value in sorted(
                    tensor_counts.items()
                )
                if value>1
            },
        }

def reserve_sentinel(
    sentinel,
    runner_sha,
    execution_head,
):
    sentinel.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload=canonical_json_bytes(
        {
            "execution_head":execution_head,
            "protocol_sha256":PROTOCOL_SHA256,
            "runner_sha256":runner_sha,
            "slot":"phase_6e_d_class_a_inference_logit_parity",
        }
    )

    try:
        fd=os.open(
            sentinel,
            os.O_WRONLY
            |os.O_CREAT
            |os.O_EXCL,
            0o600,
        )

    except FileExistsError as exc:
        raise PositiveValidationSpentError(
            "positive execution slot already spent"
        ) from exc

    with os.fdopen(
        fd,
        "wb",
    ) as stream:
        stream.write(
            payload
        )
        stream.flush()
        os.fsync(
            stream.fileno()
        )

def base_result(
    execution_head,
    runner_sha,
    sentinel,
):
    return {
        "schema":SCHEMA,
        "protocol_sha256":PROTOCOL_SHA256,
        "runner_sha256":runner_sha,
        "provider_sha256":PROVIDER_SHA256,
        "provider_git_blob":PROVIDER_BLOB,
        "negative_result_sha256":NEGATIVE_RESULT_SHA256,
        "metadata_authority_sha256":METADATA_SHA256,
        "join_authority_sha256":JOIN_SHA256,
        "generation_manifest_sha256":GENERATION_SHA256,
        "generation_qualification_sha256":RECOVERY_QUALIFICATION_SHA256,
        "derived_active_record_sha256":DERIVED_ACTIVE_SHA256,
        "model_pk":MODEL_PK,
        "generation_pk":GENERATION_PK,
        "llama_cpp_head":LLAMA_HEAD,
        "execution_head":execution_head,
        "sentinel":{
            "path":str(sentinel),
            "reserved":True,
        },
        "shared_library":{
            "path":str(SHARED_LIBRARY),
            "bytes":SHARED_LIBRARY_BYTES,
            "sha256":SHARED_LIBRARY_SHA256,
            "required_symbols":list(REQUIRED_SYMBOLS),
            "single_explicit_handle":True,
        },
    }


class _ParityLlamaContextParams(ctypes.Structure):
    _fields_=[
        ("n_ctx",ctypes.c_uint32),
        ("n_batch",ctypes.c_uint32),
        ("n_ubatch",ctypes.c_uint32),
        ("n_seq_max",ctypes.c_uint32),
        ("n_rs_seq",ctypes.c_uint32),
        ("n_outputs_max",ctypes.c_uint32),
        ("n_threads",ctypes.c_int32),
        ("n_threads_batch",ctypes.c_int32),
        ("ctx_type",ctypes.c_int),
        ("rope_scaling_type",ctypes.c_int),
        ("pooling_type",ctypes.c_int),
        ("attention_type",ctypes.c_int),
        ("flash_attn_type",ctypes.c_int),
        ("rope_freq_base",ctypes.c_float),
        ("rope_freq_scale",ctypes.c_float),
        ("yarn_ext_factor",ctypes.c_float),
        ("yarn_attn_factor",ctypes.c_float),
        ("yarn_beta_fast",ctypes.c_float),
        ("yarn_beta_slow",ctypes.c_float),
        ("yarn_orig_ctx",ctypes.c_uint32),
        ("defrag_thold",ctypes.c_float),
        ("cb_eval",ctypes.c_void_p),
        ("cb_eval_user_data",ctypes.c_void_p),
        ("type_k",ctypes.c_int),
        ("type_v",ctypes.c_int),
        ("abort_callback",ctypes.c_void_p),
        ("abort_callback_data",ctypes.c_void_p),
        ("embeddings",ctypes.c_bool),
        ("offload_kqv",ctypes.c_bool),
        ("no_perf",ctypes.c_bool),
        ("op_offload",ctypes.c_bool),
        ("swa_full",ctypes.c_bool),
        ("kv_unified",ctypes.c_bool),
        ("samplers",ctypes.c_void_p),
        ("n_samplers",ctypes.c_size_t),
        ("ctx_other",ctypes.c_void_p),
    ]


class _ParityLlamaBatch(ctypes.Structure):
    _fields_=[
        ("n_tokens",ctypes.c_int32),
        ("token",ctypes.POINTER(ctypes.c_int32)),
        ("embd",ctypes.POINTER(ctypes.c_float)),
        ("pos",ctypes.POINTER(ctypes.c_int32)),
        ("n_seq_id",ctypes.POINTER(ctypes.c_int32)),
        (
            "seq_id",
            ctypes.POINTER(
                ctypes.POINTER(
                    ctypes.c_int32
                )
            ),
        ),
        ("logits",ctypes.POINTER(ctypes.c_int8)),
    ]


PARITY_REQUIRED_SYMBOLS=(
    "llama_context_default_params",
    "llama_init_from_model",
    "llama_free",
    "llama_model_get_vocab",
    "llama_tokenize",
    "llama_batch_get_one",
    "llama_decode",
    "llama_synchronize",
    "llama_get_logits_ith",
    "llama_vocab_n_tokens",
    "llama_model_default_params",
    "llama_model_load_from_file",
    "llama_model_free",
)


PARITY_PROTOCOL_PREDECESSOR_RUNNER=Path(
    "experiments/model_fractal/"
    "maf_phase_6e_d_class_a_"
    "positive_model_load_validation_v4.py"
)

PARITY_PROTOCOL_PREDECESSOR_RUNNER_SHA256=(
    "a0c419924ba561b5ef51b1903a4c69bc"
    "4a7490b2bc55f3eb4973b634c381008d"
)

PARITY_PROTOCOL_PREDECESSOR_RESULT=Path(
    "experiments/model_fractal/"
    "maf_phase_6e_d_class_a_"
    "positive_model_load_validation_v4.json"
)

PARITY_PROTOCOL_PREDECESSOR_RESULT_SHA256=(
    "e0903000538df22f61d3b2bff5b97b67"
    "b798d742e856b08ecab0b4520daa0d08"
)

PARITY_PROTOCOL_PREDECESSOR_RESULT_BLOB=(
    "6eb7b87f827d0c7efaca9521e7442ae799fb0f26"
)


CONTROL_SOURCE_BYTES=1894532160

CONTROL_SOURCE_SHA256=(
    "507de59046601282ba768a9789900e6c"
    "cf60ed93ddf346730b7c68eb0715bc47"
)


PARITY_PROMPT=(
    "OpenMind MAF parity probe.\n"
    "Given integers 17 and 25, compute their sum "
    "and explain the result in one sentence."
)

PARITY_PROMPT_BYTES=PARITY_PROMPT.encode(
    "utf-8"
)

PARITY_PROMPT_SHA256=(
    "a79091472f58689a015e1e38947f9713"
    "fb9542211db99d2c911e41d58b40acfd"
)

PARITY_EXPECTED_VOCAB=151936
PARITY_TOKEN_CAP=128

PARITY_N_CTX=128
PARITY_N_BATCH=128
PARITY_N_UBATCH=128
PARITY_N_SEQ_MAX=1
PARITY_N_THREADS=1
PARITY_N_THREADS_BATCH=1

PARITY_ABS_TOL=1e-5
PARITY_REL_TOL=1e-5


class ParityProtectedIOGuard(
    ProtectedIOGuard
):
    def __init__(self):
        super().__init__()

        self.source_window_depth=0
        self.authorized_source_gguf_opens=0

    def audit_hook(
        self,
        event,
        args,
    ):
        if (
            event!="open"
            or not args
        ):
            return super().audit_hook(
                event,
                args,
            )

        path=self.path_value(
            args[0]
        )

        if path is None:
            return super().audit_hook(
                event,
                args,
            )

        mode=(
            args[1]
            if len(args)>1
            else None
        )

        flags=(
            args[2]
            if len(args)>2
            else None
        )

        resolved=(
            path
            .expanduser()
            .resolve(
                strict=False
            )
        )

        source_match=(
            resolved==self.source_path
            or self.same_identity(
                path,
                self.source_identity,
            )
        )

        if source_match:
            with self.lock:
                if self.write_intent(
                    mode,
                    flags,
                ):
                    self.source_gguf_opens+=1

                    raise PermissionError(
                        "source GGUF write "
                        "access prohibited"
                    )

                if (
                    self.source_window_depth
                    >0
                ):
                    self.authorized_source_gguf_opens+=1
                    return

                self.source_gguf_opens+=1

            raise PermissionError(
                "source GGUF access prohibited"
            )

        return super().audit_hook(
            event,
            args,
        )

    @contextmanager
    def authorized_source_window(self):
        with self.lock:
            self.source_window_depth+=1

        try:
            yield

        finally:
            with self.lock:
                self.source_window_depth-=1


def parity_preflight_authorities():
    for path,digest in (
        (
            PARITY_PROTOCOL_PREDECESSOR_RUNNER,
            PARITY_PROTOCOL_PREDECESSOR_RUNNER_SHA256,
        ),
        (
            PARITY_PROTOCOL_PREDECESSOR_RESULT,
            PARITY_PROTOCOL_PREDECESSOR_RESULT_SHA256,
        ),
    ):
        need(
            path.is_file(),
            "missing parity predecessor authority: "
            +str(path),
        )

        need(
            sha_file(path)==digest,
            "parity predecessor SHA mismatch: "
            +str(path),
        )

    need(
        git(
            "rev-parse",
            "HEAD:"
            +str(
                PARITY_PROTOCOL_PREDECESSOR_RESULT
            ),
        ).stdout.decode().strip()
        ==PARITY_PROTOCOL_PREDECESSOR_RESULT_BLOB,
        "parity predecessor result blob mismatch",
    )

    need(
        len(PARITY_PROMPT_BYTES)==110,
        "parity prompt byte count mismatch",
    )

    need(
        PARITY_PROMPT_BYTES.isascii(),
        "parity prompt is not ASCII",
    )

    need(
        hashlib.sha256(
            PARITY_PROMPT_BYTES
        ).hexdigest()
        ==PARITY_PROMPT_SHA256,
        "parity prompt SHA mismatch",
    )


def bind_parity_ffi(
    library,
    provider_module,
):
    missing=[
        name
        for name in PARITY_REQUIRED_SYMBOLS
        if not hasattr(
            library,
            name,
        )
    ]

    need(
        not missing,
        "qualified library missing parity symbols: "
        +",".join(missing),
    )

    need(
        hasattr(
            provider_module,
            "_LlamaModelParams",
        ),
        "provider model params ABI class missing",
    )

    library.llama_context_default_params.argtypes=[]
    library.llama_context_default_params.restype=(
        _ParityLlamaContextParams
    )

    library.llama_init_from_model.argtypes=[
        ctypes.c_void_p,
        _ParityLlamaContextParams,
    ]
    library.llama_init_from_model.restype=(
        ctypes.c_void_p
    )

    library.llama_free.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_free.restype=None

    library.llama_model_get_vocab.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_model_get_vocab.restype=(
        ctypes.c_void_p
    )

    library.llama_tokenize.argtypes=[
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_int32,
        ctypes.POINTER(
            ctypes.c_int32
        ),
        ctypes.c_int32,
        ctypes.c_bool,
        ctypes.c_bool,
    ]
    library.llama_tokenize.restype=(
        ctypes.c_int32
    )

    library.llama_batch_get_one.argtypes=[
        ctypes.POINTER(
            ctypes.c_int32
        ),
        ctypes.c_int32,
    ]
    library.llama_batch_get_one.restype=(
        _ParityLlamaBatch
    )

    library.llama_decode.argtypes=[
        ctypes.c_void_p,
        _ParityLlamaBatch,
    ]
    library.llama_decode.restype=(
        ctypes.c_int32
    )

    library.llama_synchronize.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_synchronize.restype=None

    library.llama_get_logits_ith.argtypes=[
        ctypes.c_void_p,
        ctypes.c_int32,
    ]
    library.llama_get_logits_ith.restype=(
        ctypes.POINTER(
            ctypes.c_float
        )
    )

    library.llama_vocab_n_tokens.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_vocab_n_tokens.restype=(
        ctypes.c_int32
    )

    model_params_type=(
        provider_module
        ._LlamaModelParams
    )

    library.llama_model_default_params.argtypes=[]
    library.llama_model_default_params.restype=(
        model_params_type
    )

    library.llama_model_load_from_file.argtypes=[
        ctypes.c_char_p,
        model_params_type,
    ]
    library.llama_model_load_from_file.restype=(
        ctypes.c_void_p
    )

    library.llama_model_free.argtypes=[
        ctypes.c_void_p
    ]
    library.llama_model_free.restype=None


def parity_token_hash(tokens):
    raw=bytearray()

    for token in tokens:
        raw.extend(
            struct.pack(
                "<i",
                token,
            )
        )

    return hashlib.sha256(
        raw
    ).hexdigest()


def parity_float_record(values):
    need(
        values,
        "empty logit vector",
    )

    need(
        all(
            math.isfinite(value)
            for value in values
        ),
        "nonfinite logit detected",
    )

    raw=bytearray(
        4*len(values)
    )

    for index,value in enumerate(values):
        struct.pack_into(
            "<f",
            raw,
            index*4,
            value,
        )

    argmax_id=max(
        range(len(values)),
        key=values.__getitem__,
    )

    top_ids=sorted(
        range(len(values)),
        key=lambda index:(
            -values[index],
            index,
        ),
    )[:10]

    sum_values=math.fsum(
        values
    )

    l2=math.sqrt(
        math.fsum(
            value*value
            for value in values
        )
    )

    return {
        "float_count":len(values),

        "canonical_little_endian_float32_sha256":
            hashlib.sha256(
                raw
            ).hexdigest(),

        "min":min(values),
        "max":max(values),

        "mean":
            sum_values
            /len(values),

        "l2":l2,

        "argmax_id":
            argmax_id,

        "argmax_value":
            values[argmax_id],

        "top10":[
            {
                "id":index,
                "value":values[index],
            }
            for index in top_ids
        ],

        "nonfinite_count":0,
    }


def parity_inference_probe(
    library,
    model_handle,
    arm,
):
    vocab=library.llama_model_get_vocab(
        as_void_p(
            model_handle
        )
    )

    need(
        bool(vocab),
        arm+" vocab pointer is null",
    )

    token_buffer=(
        ctypes.c_int32
        *PARITY_TOKEN_CAP
    )()

    token_count=library.llama_tokenize(
        vocab,
        PARITY_PROMPT_BYTES,
        len(PARITY_PROMPT_BYTES),
        token_buffer,
        PARITY_TOKEN_CAP,
        False,
        False,
    )

    need(
        token_count>0,
        arm+" tokenization failed",
    )

    need(
        token_count
        <PARITY_TOKEN_CAP,
        arm+" token count is not <128",
    )

    tokens=[
        int(
            token_buffer[index]
        )
        for index in range(
            token_count
        )
    ]

    params=(
        library
        .llama_context_default_params()
    )

    params.n_ctx=PARITY_N_CTX
    params.n_batch=PARITY_N_BATCH
    params.n_ubatch=PARITY_N_UBATCH
    params.n_seq_max=PARITY_N_SEQ_MAX
    params.n_threads=PARITY_N_THREADS
    params.n_threads_batch=(
        PARITY_N_THREADS_BATCH
    )

    ctx=library.llama_init_from_model(
        as_void_p(
            model_handle
        ),
        params,
    )

    need(
        bool(ctx),
        arm+" context creation returned null",
    )

    result=None
    values=None
    context_free_calls=0

    try:
        batch=(
            library
            .llama_batch_get_one(
                token_buffer,
                token_count,
            )
        )

        decode_rc=(
            library
            .llama_decode(
                ctx,
                batch,
            )
        )

        need(
            decode_rc==0,
            arm
            +" llama_decode return "
            "code is not zero",
        )

        library.llama_synchronize(
            ctx
        )

        vocab_count=(
            library
            .llama_vocab_n_tokens(
                vocab
            )
        )

        need(
            vocab_count
            ==PARITY_EXPECTED_VOCAB,
            arm
            +" vocabulary length mismatch",
        )

        logits=(
            library
            .llama_get_logits_ith(
                ctx,
                -1,
            )
        )

        need(
            bool(logits),
            arm
            +" final-token logits "
            "pointer is null",
        )

        values=[
            float(
                logits[index]
            )
            for index in range(
                vocab_count
            )
        ]

        result={
            "arm":arm,

            "prompt_sha256":
                PARITY_PROMPT_SHA256,

            "prompt_utf8_bytes":
                len(PARITY_PROMPT_BYTES),

            "tokenization":{
                "add_special":False,
                "parse_special":False,
                "call_count":1,
                "token_count":
                    token_count,
                "tokens":
                    tokens,
                "canonical_little_endian_int32_sha256":
                    parity_token_hash(
                        tokens
                    ),
            },

            "context":{
                "n_ctx":
                    PARITY_N_CTX,
                "n_batch":
                    PARITY_N_BATCH,
                "n_ubatch":
                    PARITY_N_UBATCH,
                "n_seq_max":
                    PARITY_N_SEQ_MAX,
                "n_threads":
                    PARITY_N_THREADS,
                "n_threads_batch":
                    PARITY_N_THREADS_BATCH,
                "creation_calls":1,
            },

            "decode":{
                "batch_calls":1,
                "decode_calls":1,
                "decode_return_code":
                    decode_rc,
                "synchronize_calls":1,
                "logits_calls":1,
                "evidence_scope":
                    "FULL_VOCABULARY_"
                    "FINAL_PROMPT_TOKEN",
            },

            "logits":
                parity_float_record(
                    values
                ),
        }

    finally:
        if ctx:
            library.llama_free(
                ctx
            )

            context_free_calls=1
            ctx=None

    need(
        result is not None
        and values is not None,
        arm+" probe produced no result",
    )

    result[
        "context"
    ][
        "free_calls"
    ]=context_free_calls

    need(
        context_free_calls==1,
        arm+" context free count mismatch",
    )

    return (
        result,
        values,
    )


def parity_verify_control_source(
    guard,
):
    source_stat=os.lstat(
        SOURCE_GGUF
    )

    need(
        stat.S_ISREG(
            source_stat.st_mode
        )
        and not stat.S_ISLNK(
            source_stat.st_mode
        ),
        "control source GGUF is not "
        "regular nonsymlink file",
    )

    need(
        source_stat.st_size
        ==CONTROL_SOURCE_BYTES,
        "control source GGUF "
        "byte count mismatch",
    )

    opens_before=(
        guard
        .authorized_source_gguf_opens
    )

    with guard.authorized_source_window():
        digest=sha_file(
            SOURCE_GGUF
        )

    need(
        digest
        ==CONTROL_SOURCE_SHA256,
        "control source GGUF SHA mismatch",
    )

    need(
        guard.authorized_source_gguf_opens
        >opens_before,
        "control source hash did not "
        "pass through authorized "
        "source window",
    )

    return {
        "path":
            str(SOURCE_GGUF),

        "bytes":
            CONTROL_SOURCE_BYTES,

        "sha256":
            CONTROL_SOURCE_SHA256,

        "regular_nonsymlink":
            True,

        "verified_after_treatment_cleanup":
            True,
    }


def parity_compare(
    treatment_record,
    treatment_values,
    control_record,
    control_values,
):
    treatment_tokens=(
        treatment_record[
            "tokenization"
        ][
            "tokens"
        ]
    )

    control_tokens=(
        control_record[
            "tokenization"
        ][
            "tokens"
        ]
    )

    need(
        treatment_tokens
        ==control_tokens,
        "treatment/control "
        "token vector mismatch",
    )

    need(
        treatment_record[
            "tokenization"
        ][
            "canonical_little_endian_int32_sha256"
        ]
        ==
        control_record[
            "tokenization"
        ][
            "canonical_little_endian_int32_sha256"
        ],
        "treatment/control token hash mismatch",
    )

    need(
        len(treatment_values)
        ==len(control_values),
        "logit vector length mismatch",
    )

    need(
        len(control_values)
        ==PARITY_EXPECTED_VOCAB,
        "comparison vocabulary "
        "length mismatch",
    )

    exact_equal_count=0
    tolerance_failures=0

    max_abs_error=0.0
    sum_abs_error=0.0
    sum_sq_error=0.0
    max_relative_error=0.0

    dot=0.0
    treatment_norm_sq=0.0
    control_norm_sq=0.0

    for (
        treatment_value,
        control_value,
    ) in zip(
        treatment_values,
        control_values,
    ):
        if (
            treatment_value
            ==control_value
        ):
            exact_equal_count+=1

        absolute_error=abs(
            treatment_value
            -control_value
        )

        allowed_error=(
            PARITY_ABS_TOL
            +PARITY_REL_TOL
            *abs(control_value)
        )

        if (
            absolute_error
            >allowed_error
        ):
            tolerance_failures+=1

        max_abs_error=max(
            max_abs_error,
            absolute_error,
        )

        sum_abs_error+=(
            absolute_error
        )

        sum_sq_error+=(
            absolute_error
            *absolute_error
        )

        max_relative_error=max(
            max_relative_error,
            absolute_error
            /max(
                abs(control_value),
                1e-30,
            ),
        )

        dot+=(
            treatment_value
            *control_value
        )

        treatment_norm_sq+=(
            treatment_value
            *treatment_value
        )

        control_norm_sq+=(
            control_value
            *control_value
        )

    need(
        treatment_norm_sq>0.0
        and control_norm_sq>0.0,
        "zero logit norm in cosine",
    )

    cosine=(
        dot
        /math.sqrt(
            treatment_norm_sq
            *control_norm_sq
        )
    )

    treatment_argmax=(
        treatment_record[
            "logits"
        ][
            "argmax_id"
        ]
    )

    control_argmax=(
        control_record[
            "logits"
        ][
            "argmax_id"
        ]
    )

    need(
        tolerance_failures==0,
        "one or more logits exceed "
        "frozen numerical tolerance",
    )

    need(
        treatment_argmax
        ==control_argmax,
        "treatment/control "
        "argmax ID mismatch",
    )

    treatment_top10=[
        row["id"]
        for row in treatment_record[
            "logits"
        ][
            "top10"
        ]
    ]

    control_top10=[
        row["id"]
        for row in control_record[
            "logits"
        ][
            "top10"
        ]
    ]

    count=len(
        control_values
    )

    return {
        "absolute_tolerance":
            PARITY_ABS_TOL,

        "relative_tolerance":
            PARITY_REL_TOL,

        "nan_equality":
            False,

        "float_count":
            count,

        "exact_equality_count":
            exact_equal_count,

        "tolerance_failure_count":
            tolerance_failures,

        "max_absolute_error":
            max_abs_error,

        "mean_absolute_error":
            sum_abs_error
            /count,

        "rmse":
            math.sqrt(
                sum_sq_error
                /count
            ),

        "max_relative_error_safe_denominator":
            max_relative_error,

        "cosine_similarity":
            cosine,

        "treatment_argmax_id":
            treatment_argmax,

        "control_argmax_id":
            control_argmax,

        "argmax_id_equal":
            True,

        "treatment_top10_ids":
            treatment_top10,

        "control_top10_ids":
            control_top10,

        "top10_id_order_equal":
            treatment_top10
            ==control_top10,

        "all_elements_within_tolerance":
            True,
    }



def main():
    execution_head=None
    runner_sha=None
    sentinel=None
    sentinel_reserved=False

    guard=None
    library=None

    gguf_context=None
    ggml_context=None

    provider_module=None
    provider=None
    read_telemetry=None

    treatment_model_handle=None
    control_model_handle=None

    treatment_record={}
    control_record={}
    comparison_record={}
    control_source_record={}

    metadata_record={}
    resident_record={}
    provider_record={}
    provider_state_record={}

    real_user_init_calls=0
    provider_internal_model_free_calls=0
    backend_copy_calls=0

    accepted_real_model_handles=0

    treatment_model_free_calls=0

    control_model_load_calls=0
    control_model_free_calls=0

    try:
        (
            execution_head,
            runner_sha,
            sentinel,
        )=runner_commit_checkpoint()

        parity_preflight_authorities()

        guard=ParityProtectedIOGuard()

        sys.addaudithook(
            guard.audit_hook
        )

        library=load_single_library()

        bind_construction_ffi(
            library
        )

        (
            gguf_context,
            ggml_context,
            metadata_record,
        )=build_metadata_context(
            library
        )

        provider_module=import_frozen_provider()

        (
            directory,
            join_by_pk,
            resident_record,
        )=build_direct_resident_directory(
            provider_module
        )

        provider=(
            provider_module
            .ClassAMAFBackedTensorProvider(
                directory=directory,
                ggml_library=library,
            )
        )

        bind_parity_ffi(
            library,
            provider_module,
        )

        read_telemetry=SerializedReadTelemetry(
            guard,
            provider_module,
            join_by_pk,
        )

        read_telemetry.install()

        original_user_init=(
            provider
            ._llama_model_init_from_user
        )

        original_provider_free=(
            provider
            ._llama_model_free
        )

        original_backend_copy=(
            provider
            ._ggml_backend_tensor_set
        )

        def counted_user_init(*args):
            nonlocal real_user_init_calls

            real_user_init_calls+=1

            return original_user_init(
                *args
            )

        def counted_provider_free(*args):
            nonlocal provider_internal_model_free_calls

            provider_internal_model_free_calls+=1

            return original_provider_free(
                *args
            )

        def counted_backend_copy(*args):
            nonlocal backend_copy_calls

            backend_copy_calls+=1

            return original_backend_copy(
                *args
            )

        provider._llama_model_init_from_user=(
            counted_user_init
        )

        provider._llama_model_free=(
            counted_provider_free
        )

        provider._ggml_backend_tensor_set=(
            counted_backend_copy
        )

        reserve_sentinel(
            sentinel,
            runner_sha,
            execution_head,
        )

        sentinel_reserved=True

        treatment_model_handle=(
            provider.initialize_model(
                ctypes.c_void_p(
                    gguf_context
                )
            )
        )

        need(
            bool(
                treatment_model_handle
            ),
            "provider returned null "
            "treatment model",
        )

        accepted_real_model_handles=1

        provider_record=jsonable(
            provider.qualification_record()
        )

        provider_state_record=jsonable(
            provider.state
        )

        (
            treatment_record,
            treatment_values,
        )=parity_inference_probe(
            library,
            treatment_model_handle,
            "treatment_maf",
        )

        library.llama_model_free(
            as_void_p(
                treatment_model_handle
            )
        )

        treatment_model_free_calls=1
        treatment_model_handle=None

        read_record=(
            read_telemetry.record()
        )

        read_telemetry.restore()

        need(
            real_user_init_calls==1,
            "real llama user-init count "
            "is not exactly one",
        )

        need(
            provider_internal_model_free_calls==0,
            "provider freed accepted "
            "treatment model unexpectedly",
        )

        need(
            accepted_real_model_handles==1,
            "accepted treatment "
            "model count mismatch",
        )

        need(
            treatment_model_free_calls==1,
            "treatment model "
            "free count mismatch",
        )

        need(
            read_record[
                "reader_calls"
            ]>0,
            "no persistent MAF "
            "serialized-object reads occurred",
        )

        need(
            read_record[
                "serialized_bytes"
            ]>0,
            "no persistent MAF bytes were read",
        )

        need(
            backend_copy_calls>0,
            "no backend tensor copies occurred",
        )

        need(
            guard.source_gguf_opens==0,
            "source GGUF access "
            "occurred during treatment",
        )

        need(
            guard.conventional_complete_gguf_files_created==0,
            "conventional GGUF creation "
            "occurred during treatment",
        )

        need(
            guard.unauthorized_segment_opens==0,
            "unauthorized segment "
            "access occurred",
        )

        library.gguf_free(
            gguf_context
        )

        gguf_context=None

        library.ggml_free(
            ggml_context
        )

        ggml_context=None

        need(
            treatment_model_handle is None,
            "treatment model still "
            "live before control",
        )

        need(
            gguf_context is None
            and ggml_context is None,
            "treatment construction "
            "contexts still live before control",
        )

        need(
            treatment_record[
                "context"
            ][
                "free_calls"
            ]==1,
            "treatment inference "
            "context not freed before control",
        )

        control_source_record=(
            parity_verify_control_source(
                guard
            )
        )

        control_params=(
            library
            .llama_model_default_params()
        )

        control_model_load_calls+=1

        control_model_handle=(
            library
            .llama_model_load_from_file(
                os.fsencode(
                    SOURCE_GGUF
                ),
                control_params,
            )
        )

        need(
            bool(
                control_model_handle
            ),
            "control llama_model_load_from_file "
            "returned null",
        )

        need(
            control_model_load_calls==1,
            "control conventional "
            "loader count mismatch",
        )

        (
            control_record,
            control_values,
        )=parity_inference_probe(
            library,
            control_model_handle,
            "control_gguf",
        )

        library.llama_model_free(
            as_void_p(
                control_model_handle
            )
        )

        control_model_free_calls=1
        control_model_handle=None

        comparison_record=parity_compare(
            treatment_record,
            treatment_values,
            control_record,
            control_values,
        )

        need(
            control_model_free_calls==1,
            "control model "
            "free count mismatch",
        )

        need(
            control_record[
                "context"
            ][
                "free_calls"
            ]==1,
            "control inference context "
            "free count mismatch",
        )

        result=base_result(
            execution_head,
            runner_sha,
            sentinel,
        )

        result.update(
            {
                "experiment":{
                    "name":
                        "Phase 6E-D Class-A "
                        "inference logit "
                        "parity validation",

                    "evidence_scope":
                        "FULL_VOCABULARY_"
                        "FINAL_PROMPT_TOKEN",

                    "prompt":
                        PARITY_PROMPT,

                    "prompt_utf8_bytes":
                        len(
                            PARITY_PROMPT_BYTES
                        ),

                    "prompt_sha256":
                        PARITY_PROMPT_SHA256,

                    "sampling":
                        False,

                    "generated_tokens":
                        0,
                },

                "resident_directory":
                    resident_record,

                "metadata_reconstruction":
                    metadata_record,

                "provider_execution":{
                    "initialize_model_calls":
                        1,

                    "real_llama_user_init_calls":
                        real_user_init_calls,

                    "accepted_real_model_handles":
                        accepted_real_model_handles,

                    "backend_tensor_copy_calls":
                        backend_copy_calls,

                    "qualification_record":
                        provider_record,

                    "state":
                        provider_state_record,
                },

                "treatment":
                    treatment_record,

                "control_source":
                    control_source_record,

                "control":
                    control_record,

                "comparison":
                    comparison_record,

                "protected_io":{
                    "prohibited_source_gguf_opens":
                        guard.source_gguf_opens,

                    "authorized_source_gguf_opens":
                        guard.authorized_source_gguf_opens,

                    "conventional_complete_gguf_files_created":
                        guard.conventional_complete_gguf_files_created,

                    "conventional_loader_calls":
                        control_model_load_calls,

                    "authorized_segment_opens":
                        guard.authorized_segment_opens,

                    "unauthorized_segment_opens":
                        guard.unauthorized_segment_opens,

                    "serialized_object_reader_calls":
                        read_record[
                            "reader_calls"
                        ],

                    "authorized_persistent_bytes_read":
                        read_record[
                            "serialized_bytes"
                        ],

                    "serialized_read_telemetry":
                        read_record,
                },

                "cleanup":{
                    "treatment_context_free_calls":
                        treatment_record[
                            "context"
                        ][
                            "free_calls"
                        ],

                    "treatment_model_free_calls":
                        treatment_model_free_calls,

                    "control_context_free_calls":
                        control_record[
                            "context"
                        ][
                            "free_calls"
                        ],

                    "control_model_free_calls":
                        control_model_free_calls,

                    "provider_internal_model_free_calls":
                        provider_internal_model_free_calls,

                    "escaped_treatment_model_handles":
                        0,

                    "escaped_control_model_handles":
                        0,
                },

                "summary":{
                    "exact_token_vector_parity":
                        True,

                    "treatment_decode_calls":
                        treatment_record[
                            "decode"
                        ][
                            "decode_calls"
                        ],

                    "control_decode_calls":
                        control_record[
                            "decode"
                        ][
                            "decode_calls"
                        ],

                    "treatment_logits_calls":
                        treatment_record[
                            "decode"
                        ][
                            "logits_calls"
                        ],

                    "control_logits_calls":
                        control_record[
                            "decode"
                        ][
                            "logits_calls"
                        ],

                    "vocabulary_length":
                        PARITY_EXPECTED_VOCAB,

                    "tolerance_failure_count":
                        comparison_record[
                            "tolerance_failure_count"
                        ],

                    "argmax_id_equal":
                        comparison_record[
                            "argmax_id_equal"
                        ],

                    "all_pass":
                        True,

                    "fatal_error":
                        None,
                },

                "disposition":
                    PASS_DISPOSITION,
            }
        )

        (
            result_bytes,
            result_sha,
        )=atomic_write_result(
            result
        )

        print(
            "🟨🟨🟨 OPENMIND / "
            "GOLD STANDARD V2 🟨🟨🟨"
        )

        print(
            "PHASE 6E-D — CLASS-A "
            "INFERENCE LOGIT PARITY VALIDATION"
        )

        print()
        print(
            "STATUS             : "
            +PASS_DISPOSITION
        )
        print(
            "GATE FAILURE       : NONE"
        )
        print(
            "EXECUTION HEAD     : "
            +execution_head
        )
        print(
            "RUNNER SHA         : "
            +runner_sha
        )
        print(
            "PROTOCOL SHA       : "
            +PROTOCOL_SHA256
        )
        print(
            "TOKEN COUNT        : "
            +str(
                treatment_record[
                    "tokenization"
                ][
                    "token_count"
                ]
            )
        )
        print(
            "VOCAB LENGTH       : "
            +str(
                PARITY_EXPECTED_VOCAB
            )
        )
        print(
            "TOL FAILURES       : "
            +str(
                comparison_record[
                    "tolerance_failure_count"
                ]
            )
        )
        print(
            "MAX ABS ERROR      : "
            +repr(
                comparison_record[
                    "max_absolute_error"
                ]
            )
        )
        print(
            "COSINE             : "
            +repr(
                comparison_record[
                    "cosine_similarity"
                ]
            )
        )
        print(
            "ARGMAX EQUAL       : YES"
        )
        print(
            "CONTROL LOADS      : "
            +str(
                control_model_load_calls
            )
        )
        print(
            "RESULT PATH        : "
            +str(
                RESULT_PATH
            )
        )
        print(
            "RESULT SHA         : "
            +result_sha
        )
        print(
            "RESULT BYTES       : "
            +str(
                result_bytes
            )
        )

        return 0

    except PositiveValidationSpentError as exc:
        print(
            "🟨🟨🟨 OPENMIND / "
            "GOLD STANDARD V2 🟨🟨🟨"
        )

        print(
            "PHASE 6E-D — CLASS-A "
            "INFERENCE LOGIT PARITY VALIDATION"
        )

        print()
        print(
            "STATUS             : "
            "EXECUTION REFUSED — "
            "PARITY SLOT ALREADY SPENT"
        )
        print(
            "GATE FAILURE       : "
            +str(exc)
        )
        print(
            "RESULT WRITTEN     : NO"
        )
        print(
            "RERUN              : PROHIBITED"
        )

        return 2

    except BaseException as exc:
        if read_telemetry is not None:
            try:
                read_telemetry.restore()
            except BaseException:
                pass

        if (
            treatment_model_handle
            is not None
            and library is not None
        ):
            try:
                library.llama_model_free(
                    as_void_p(
                        treatment_model_handle
                    )
                )

                treatment_model_free_calls+=1
                treatment_model_handle=None

            except BaseException:
                pass

        if (
            control_model_handle
            is not None
            and library is not None
        ):
            try:
                library.llama_model_free(
                    as_void_p(
                        control_model_handle
                    )
                )

                control_model_free_calls+=1
                control_model_handle=None

            except BaseException:
                pass

        if (
            gguf_context is not None
            and library is not None
        ):
            try:
                library.gguf_free(
                    gguf_context
                )

                gguf_context=None

            except BaseException:
                pass

        if (
            ggml_context is not None
            and library is not None
        ):
            try:
                library.ggml_free(
                    ggml_context
                )

                ggml_context=None

            except BaseException:
                pass

        if (
            sentinel_reserved
            and execution_head is not None
            and runner_sha is not None
            and sentinel is not None
            and not RESULT_PATH.exists()
        ):
            try:
                failure=base_result(
                    execution_head,
                    runner_sha,
                    sentinel,
                )

                failure.update(
                    {
                        "experiment":{
                            "name":
                                "Phase 6E-D "
                                "Class-A inference "
                                "logit parity validation",

                            "evidence_scope":
                                "FULL_VOCABULARY_"
                                "FINAL_PROMPT_TOKEN",

                            "prompt_sha256":
                                PARITY_PROMPT_SHA256,
                        },

                        "provider_execution":{
                            "real_llama_user_init_calls":
                                real_user_init_calls,

                            "accepted_real_model_handles":
                                accepted_real_model_handles,

                            "backend_tensor_copy_calls":
                                backend_copy_calls,

                            "qualification_record":
                                provider_record,

                            "state":
                                provider_state_record,
                        },

                        "treatment":
                            treatment_record,

                        "control_source":
                            control_source_record,

                        "control":
                            control_record,

                        "comparison":
                            comparison_record,

                        "cleanup":{
                            "treatment_model_free_calls":
                                treatment_model_free_calls,

                            "control_model_free_calls":
                                control_model_free_calls,

                            "provider_internal_model_free_calls":
                                provider_internal_model_free_calls,

                            "escaped_treatment_model_handles":
                                (
                                    1
                                    if treatment_model_handle
                                    is not None
                                    else 0
                                ),

                            "escaped_control_model_handles":
                                (
                                    1
                                    if control_model_handle
                                    is not None
                                    else 0
                                ),
                        },

                        "summary":{
                            "all_pass":
                                False,

                            "fatal_error":{
                                "type":
                                    type(exc).__name__,

                                "message":
                                    str(exc),
                            },
                        },

                        "disposition":
                            FAIL_DISPOSITION,
                    }
                )

                atomic_write_result(
                    failure
                )

            except BaseException:
                pass

        print(
            "🟨🟨🟨 OPENMIND / "
            "GOLD STANDARD V2 🟨🟨🟨"
        )

        print(
            "PHASE 6E-D — CLASS-A "
            "INFERENCE LOGIT PARITY VALIDATION"
        )

        print()

        print(
            "STATUS             : "
            +FAIL_DISPOSITION
        )

        print(
            "GATE FAILURE       : "
            +type(exc).__name__
            +" — "
            +str(exc)
        )

        print(
            "SENTINEL RESERVED  : "
            +(
                "YES"
                if sentinel_reserved
                else "NO"
            )
        )

        print(
            "RESULT PRODUCED    : "
            +(
                "YES"
                if RESULT_PATH.exists()
                else "NO"
            )
        )

        print(
            "RERUN              : "
            "PROHIBITED IF SENTINEL RESERVED"
        )

        return 1

if __name__=="__main__":
    raise SystemExit(
        main()
    )
