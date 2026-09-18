#!/usr/bin/env python3
"""
OpenMind / Phase 6F V2

Current persistent MAF access/provisioning performance benchmark.

CONSTRUCTION STATUS:
    Source-only construction does not authorize execution.

SCIENTIFIC BOUNDARY:
    Baseline characterization only. No superiority claim.

EXECUTION BOUNDARY:
    Authoritative execution requires separate exact-once authorization.

The spent Phase 6E-D runner is never imported or invoked. Required
low-level definitions are copied statically only after exact frozen
source verification.
"""

from __future__ import annotations

import argparse
import math
import resource
import statistics
import time

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

sys.dont_write_bytecode = True

# ===== FROZEN 6E-D DEPENDENCY CLOSURE =====

PROVIDER_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_maf_backed_tensor_provider_v1.py")


METADATA_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json")


JOIN_PATH=Path("experiments/model_fractal/maf_phase_6e_d_class_a_tensor_object_segment_join_v1.json")


GENERATION_PATH=Path("results/runtime/maf_full_model_persistent_generation_v1/generation.manifest.json")


GENERATION_SHA256="a79b012f10904a5e0540076a8443007344ada4e11e3846d817201b43583fedff"


MODEL_PK="mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"


GENERATION_PK="mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2"


DERIVED_ACTIVE_SHA256="82bc4bc0975eb9c02e8600baafbd982a577490252dd0eb3a0d274e7368a08b18"


SEGMENT_ID="segment:00000000"


SEGMENT_PATH=Path("results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg")


SEGMENT_BYTES=1888934699


SEGMENT_SHA256="a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9"


SOURCE_GGUF=Path.home()/"qwen2.5-coder-q8_0.gguf"


SHARED_LIBRARY=Path("/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libllama.so.0.0.10318")


SHARED_LIBRARY_BYTES=3613896


SHARED_LIBRARY_SHA256="a56bdf41b3409ae870c584ecf23e7e65915451ae313d057d92958be0d94af802"


V2_BUILD_AUTHORITY_PATH=Path('experiments/model_fractal/maf_phase_6e_d_class_a_compatibility_build_authority_v1.json')


V2_BUILD_AUTHORITY_BYTES=2072


V2_BUILD_AUTHORITY_SHA256='557d9140e9fb946e028185ae7fdcda851a1f3b231772f56768f46c541a5ebaa6'


V2_BUILD_AUTHORITY_GIT_BLOB='9ab1acb42edd149fa055f4ce42f9dbe58f142519'


V2_COMPATIBILITY_BUILD_ROOT=Path('/data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan')


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


class _GGMLInitParams(ctypes.Structure):
    _fields_=(
        ("mem_size",ctypes.c_size_t),
        ("mem_buffer",ctypes.c_void_p),
        ("no_alloc",ctypes.c_bool),
    )


def need(value,message):
    if not value:
        raise PositiveValidationError(message)


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


# ===========================================================================
# PHASE 6F V2 PERFORMANCE ORCHESTRATION
# ===========================================================================

ROOT = Path(__file__).resolve().parents[2]

PHASE6F_EXPECTED_BRANCH = "labs/multidimensional-maf"

PHASE6F_PREREG_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_PHASE_6F_CURRENT_ACCESS_PROVISIONING_"
    "PERFORMANCE_PREREGISTRATION_V2.md"
)
PHASE6F_PREREG_SHA256 = (
    "b54009487a3668b1a81afa50f5ff1b46"
    "b8b3a8cdd878fff3d468e619eae42791"
)

PHASE6F_BINDING_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_PHASE_6F_CURRENT_ACCESS_PROVISIONING_"
    "PERFORMANCE_ARTIFACT_BINDING_V1.md"
)
PHASE6F_BINDING_SHA256 = (
    "79ae8028d8f1cfcbab7da3670c4e8637"
    "932707f46410f3fd7265bdc2e7133091"
)

PHASE6F_THERMAL_CORRECTION_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_PHASE_6F_THERMAL_QUALIFICATION_"
    "CORRECTION_ADDENDUM_V1.md"
)

PHASE6F_THERMAL_CORRECTION_SHA256 = (
    "bd51a098999067fdf3a3bf224e0237f7"
    "6a10dd01aa6e33aaa7c58709ac63d063"
)

PHASE6F_6ED_RUNNER_SHA256 = (
    "57616a1e188f24cefec4f3431d652d37"
    "c3ce27594695372bebb35021507f08b2"
)

PHASE6F_PROVIDER_SHA256 = (
    "e436bbf14e34dfb1c46a6d947b66788"
    "fcf85fe3a0c9f8312ff3963ab6155e3ec"
)

PHASE6F_6ED_RESULT_PATH = ROOT / (
    "experiments/model_fractal/"
    "maf_phase_6e_d_class_a_inference_logit_parity_validation_v1.json"
)
PHASE6F_6ED_RESULT_SHA256 = (
    "f3100df4ebef840f816a0450a0289a78"
    "7d38354648f15508ba533966a0b5a217"
)

PHASE6F_RUNNER_PATH = ROOT / (
    "experiments/model_fractal/"
    "maf_phase_6f_current_access_provisioning_performance_v2.py"
)

PHASE6F_RESULT_PATH = ROOT / (
    "results/runtime/"
    "maf_phase_6f_current_access_provisioning_performance_v2/"
    "result.json"
)

PHASE6F_SENTINEL_PATH = ROOT / (
    "results/runtime/"
    "maf_phase_6f_current_access_provisioning_performance_v2/"
    ".spent"
)

PHASE6F_RESULT_SCHEMA = (
    "openmind.maf_phase_6f_current_access_"
    "provisioning_performance.v2"
)

PHASE6F_CACHE_REGIME = "BALANCED_NATURAL_CACHE_V1"

PHASE6F_PAIR_SEQUENCE = (
    ("T", "C"),
    ("C", "T"),
    ("T", "C"),
    ("C", "T"),
    ("T", "C"),
    ("C", "T"),
    ("T", "C"),
    ("C", "T"),
    ("T", "C"),
    ("C", "T"),
)

PHASE6F_TREATMENT_TRIALS = 10
PHASE6F_CONTROL_TRIALS = 10
PHASE6F_MEASURED_TOTAL = 20

PHASE6F_CHILD_TIMEOUT_SECONDS = 300

# Statically bound construction choice.
#
# Qualified thermal method:
#   /sys/class/thermal/thermal_zone*/temp
#
# Values with magnitude > 1000 are normalized from milli-Celsius.
# Execution is unacceptable if there is no readable zone or if the
# maximum normalized readable zone temperature is >= 85 C.
PHASE6F_THERMAL_ABORT_C = 85.0

PHASE6F_EXPECTED_UNTRACKED_COUNT = 440
PHASE6F_EXPECTED_UNTRACKED_RAW_NUL_SHA256 = (
    "f206c0eed32daef9ed0cfaae195aa56a"
    "343a85437ebd3135aeafdb4c1ffacddd"
)

PHASE6F_CHILD_ENV = "OPENMIND_PHASE_6F_CHILD_AUTH"
PHASE6F_HEAD_ENV = "OPENMIND_PHASE_6F_FROZEN_HEAD"
PHASE6F_RUNNER_SHA_ENV = "OPENMIND_PHASE_6F_RUNNER_SHA256"

PHASE6F_CORRECTNESS_TOL_ABS = 1e-5
PHASE6F_CORRECTNESS_TOL_REL = 1e-5
PHASE6F_EXPECTED_TOKEN_COUNT = 28
PHASE6F_EXPECTED_VOCAB = 151936
PHASE6F_EXPECTED_BACKEND_COPIES = 339


class Phase6FError(RuntimeError):
    pass


class Phase6FIntegrityError(Phase6FError):
    pass


class Phase6FExecutionError(Phase6FError):
    pass


def phase6f_need(condition, message):
    if not condition:
        raise Phase6FIntegrityError(message)


def phase6f_sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def phase6f_canonical_json_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def phase6f_git(*args):
    cp = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if cp.returncode != 0:
        raise Phase6FIntegrityError(
            "git failed: "
            + " ".join(args)
            + " :: "
            + cp.stderr.decode(errors="replace").strip()
        )

    return cp.stdout


def phase6f_raw_untracked():
    return phase6f_git(
        "ls-files",
        "-z",
        "--others",
        "--exclude-standard",
    )


def phase6f_runtime_authority():
    expected_head = os.environ.get(
        PHASE6F_HEAD_ENV,
        "",
    )

    expected_runner_sha = os.environ.get(
        PHASE6F_RUNNER_SHA_ENV,
        "",
    )

    phase6f_need(
        len(expected_head) == 40,
        PHASE6F_HEAD_ENV + " missing/invalid",
    )

    phase6f_need(
        len(expected_runner_sha) == 64,
        PHASE6F_RUNNER_SHA_ENV + " missing/invalid",
    )

    branch = phase6f_git(
        "branch",
        "--show-current",
    ).decode().strip()

    head = phase6f_git(
        "rev-parse",
        "HEAD",
    ).decode().strip()

    phase6f_need(
        branch == PHASE6F_EXPECTED_BRANCH,
        "execution branch mismatch",
    )

    phase6f_need(
        head == expected_head,
        "execution HEAD mismatch",
    )

    phase6f_need(
        phase6f_git(
            "diff",
            "--name-only",
            "-z",
        ) == b"",
        "tracked worktree dirty before execution",
    )

    phase6f_need(
        phase6f_git(
            "diff",
            "--cached",
            "--name-only",
            "-z",
        ) == b"",
        "index dirty before execution",
    )

    untracked = phase6f_raw_untracked()

    phase6f_need(
        len(
            [
                item
                for item
                in untracked.split(b"\0")
                if item
            ]
        )
        == PHASE6F_EXPECTED_UNTRACKED_COUNT,
        "untracked count mismatch before execution",
    )

    phase6f_need(
        hashlib.sha256(untracked).hexdigest()
        == PHASE6F_EXPECTED_UNTRACKED_RAW_NUL_SHA256,
        "untracked raw-NUL SHA mismatch before execution",
    )

    phase6f_need(
        PHASE6F_RUNNER_PATH.is_file(),
        "Phase 6F runner missing",
    )

    runner_sha = phase6f_sha256_file(
        PHASE6F_RUNNER_PATH
    )

    phase6f_need(
        runner_sha == expected_runner_sha,
        "runner SHA differs from execution authority",
    )

    phase6f_need(
        phase6f_sha256_file(
            PHASE6F_PREREG_PATH
        )
        == PHASE6F_PREREG_SHA256,
        "Phase 6F preregistration SHA mismatch",
    )

    phase6f_need(
        phase6f_sha256_file(
            PHASE6F_BINDING_PATH
        )
        == PHASE6F_BINDING_SHA256,
        "Phase 6F artifact-binding SHA mismatch",
    )

    phase6f_need(
        phase6f_sha256_file(
            PHASE6F_THERMAL_CORRECTION_PATH
        )
        == PHASE6F_THERMAL_CORRECTION_SHA256,
        "Phase 6F thermal-correction SHA mismatch",
    )

    phase6f_need(
        phase6f_sha256_file(
            PROVIDER_PATH
        )
        == PHASE6F_PROVIDER_SHA256,
        "MAF provider SHA mismatch",
    )

    phase6f_need(
        phase6f_sha256_file(
            PHASE6F_6ED_RESULT_PATH
        )
        == PHASE6F_6ED_RESULT_SHA256,
        "Phase 6E-D frozen result SHA mismatch",
    )

    phase6f_need(
        not PHASE6F_RESULT_PATH.exists(),
        "Phase 6F result already exists",
    )

    phase6f_need(
        not PHASE6F_SENTINEL_PATH.exists(),
        "Phase 6F sentinel already exists",
    )

    return {
        "branch": branch,
        "head": head,
        "runner_sha256": runner_sha,
        "preregistration_sha256":
            PHASE6F_PREREG_SHA256,
        "artifact_binding_sha256":
            PHASE6F_BINDING_SHA256,
        "thermal_correction_path":
            str(
                PHASE6F_THERMAL_CORRECTION_PATH.relative_to(
                    ROOT
                )
            ),
        "thermal_correction_sha256":
            PHASE6F_THERMAL_CORRECTION_SHA256,
        "phase_6e_d_runner_sha256":
            PHASE6F_6ED_RUNNER_SHA256,
        "provider_sha256":
            PHASE6F_PROVIDER_SHA256,
        "phase_6e_d_result_sha256":
            PHASE6F_6ED_RESULT_SHA256,
        "untracked_count":
            PHASE6F_EXPECTED_UNTRACKED_COUNT,
        "untracked_raw_nul_sha256":
            PHASE6F_EXPECTED_UNTRACKED_RAW_NUL_SHA256,
    }


def phase6f_reserve_sentinel(authority):
    PHASE6F_SENTINEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "schema":
            "openmind.maf_phase_6f_current_access_"
            "provisioning_performance.spent.v1",
        "phase": "6F",
        "head": authority["head"],
        "runner_sha256":
            authority["runner_sha256"],
        "reserved_unix_ns": time.time_ns(),
        "purpose":
            "exact-once Phase 6F V2 benchmark authority",
    }

    raw = phase6f_canonical_json_bytes(
        payload
    )

    fd = os.open(
        PHASE6F_SENTINEL_PATH,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL,
        0o600,
    )

    try:
        offset = 0

        while offset < len(raw):
            count = os.write(
                fd,
                raw[offset:],
            )

            if count <= 0:
                raise Phase6FExecutionError(
                    "short sentinel write"
                )

            offset += count

        os.fsync(fd)

    finally:
        os.close(fd)

    return payload


def phase6f_verify_child_authority():
    child_auth = os.environ.get(
        PHASE6F_CHILD_ENV,
        "",
    )

    expected_head = os.environ.get(
        PHASE6F_HEAD_ENV,
        "",
    )

    expected_runner_sha = os.environ.get(
        PHASE6F_RUNNER_SHA_ENV,
        "",
    )

    phase6f_need(
        child_auth == expected_runner_sha,
        "child authorization mismatch",
    )

    phase6f_need(
        len(expected_head) == 40,
        "child frozen HEAD missing",
    )

    phase6f_need(
        phase6f_sha256_file(
            PHASE6F_RUNNER_PATH
        )
        == expected_runner_sha,
        "child runner SHA mismatch",
    )

    phase6f_need(
        PHASE6F_SENTINEL_PATH.is_file(),
        "child invoked before sentinel reservation",
    )


def phase6f_read_proc_status():
    record = {
        "VmRSS_kB": None,
        "VmHWM_kB": None,
    }

    path = Path("/proc/self/status")

    if not path.is_file():
        return record

    for line in path.read_text(
        errors="strict"
    ).splitlines():
        if line.startswith("VmRSS:"):
            parts = line.split()

            if len(parts) >= 2:
                record["VmRSS_kB"] = int(
                    parts[1]
                )

        elif line.startswith("VmHWM:"):
            parts = line.split()

            if len(parts) >= 2:
                record["VmHWM_kB"] = int(
                    parts[1]
                )

    return record


def phase6f_read_proc_io():
    record = {}
    path = Path("/proc/self/io")

    if not path.is_file():
        return record

    for line in path.read_text(
        errors="strict"
    ).splitlines():
        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1,
        )

        value = value.strip()

        if value.isdigit():
            record[key.strip()] = int(
                value
            )

    return record


def phase6f_resource_record():
    usage = resource.getrusage(
        resource.RUSAGE_SELF
    )

    return {
        "ru_minflt":
            int(usage.ru_minflt),
        "ru_majflt":
            int(usage.ru_majflt),
    }


def phase6f_process_snapshot():
    return {
        "status":
            phase6f_read_proc_status(),
        "io":
            phase6f_read_proc_io(),
        "resource":
            phase6f_resource_record(),
    }


def phase6f_counter_delta(
    before,
    after,
):
    output = {}

    for key in sorted(
        set(before) | set(after)
    ):
        first = before.get(key)
        second = after.get(key)

        if (
            isinstance(first, int)
            and isinstance(second, int)
        ):
            output[key] = second - first

    return output


def phase6f_process_delta(
    before,
    after,
):
    return {
        "VmRSS_before_kB":
            before["status"].get(
                "VmRSS_kB"
            ),
        "VmRSS_after_kB":
            after["status"].get(
                "VmRSS_kB"
            ),
        "VmHWM_before_kB":
            before["status"].get(
                "VmHWM_kB"
            ),
        "VmHWM_after_kB":
            after["status"].get(
                "VmHWM_kB"
            ),
        "io_delta":
            phase6f_counter_delta(
                before["io"],
                after["io"],
            ),
        "page_fault_delta":
            phase6f_counter_delta(
                before["resource"],
                after["resource"],
            ),
    }


def phase6f_thermal_snapshot():
    root = Path(
        "/sys/class/thermal"
    )

    zones = []

    if root.is_dir():
        for zone in sorted(
            root.glob("thermal_zone*"),
            key=lambda item: item.name,
        ):
            try:
                raw = (
                    zone / "temp"
                ).read_text(
                    errors="strict"
                ).strip()

                value = float(raw)

            except (
                OSError,
                UnicodeError,
                ValueError,
            ):
                continue

            if abs(value) > 1000.0:
                celsius = value / 1000.0
                source_unit = (
                    "milli_celsius"
                )
            else:
                celsius = value
                source_unit = "celsius"

            zone_type = None

            try:
                zone_type = (
                    zone / "type"
                ).read_text(
                    errors="strict"
                ).strip()

            except (
                OSError,
                UnicodeError,
            ):
                pass

            zone_mode = None

            try:
                zone_mode = (
                    zone / "mode"
                ).read_text(
                    errors="strict"
                ).strip()

            except (
                OSError,
                UnicodeError,
            ):
                pass

            normalized_type = (
                zone_type.casefold()
                if zone_type is not None
                else ""
            )

            normalized_mode = (
                zone_mode.casefold()
                if zone_mode is not None
                else ""
            )

            excluded = (
                "hw-trip"
                in normalized_type
                and normalized_mode
                == "disabled"
            )

            zones.append(
                {
                    "zone": zone.name,
                    "type": zone_type,
                    "mode": zone_mode,
                    "raw": raw,
                    "source_unit":
                        source_unit,
                    "normalized_celsius":
                        celsius,
                    "live_observation_eligible":
                        not excluded,
                    "exclusion_reason":
                        (
                            "disabled_hw_trip_zone"
                            if excluded
                            else None
                        ),
                }
            )

    eligible_zones = [
        item
        for item in zones
        if item[
            "live_observation_eligible"
        ]
    ]

    all_readable_maximum = None

    if zones:
        all_readable_maximum = max(
            item[
                "normalized_celsius"
            ]
            for item in zones
        )

    qualified_live_maximum = None

    if eligible_zones:
        qualified_live_maximum = max(
            item[
                "normalized_celsius"
            ]
            for item in eligible_zones
        )

    return {
        "method":
            "sysfs_thermal_zone_temp_v1",
        "zone_count": len(zones),
        "eligible_zone_count":
            len(eligible_zones),
        "excluded_zone_count":
            len(zones)
            - len(eligible_zones),
        "maximum_celsius":
            all_readable_maximum,
        "all_readable_maximum_celsius":
            all_readable_maximum,
        "qualified_live_maximum_celsius":
            qualified_live_maximum,
        "abort_threshold_celsius":
            PHASE6F_THERMAL_ABORT_C,
        "zones": zones,
    }


def phase6f_thermal_acceptable(snapshot):
    maximum = snapshot.get(
        "qualified_live_maximum_celsius"
    )

    return (
        snapshot.get(
            "eligible_zone_count",
            0,
        ) > 0
        and maximum is not None
        and maximum
        < PHASE6F_THERMAL_ABORT_C
    )


def phase6f_child_treatment(mode):
    phase6f_verify_child_authority()

    library = None
    gguf_context = None
    ggml_context = None
    model_handle = None
    telemetry = None
    guard = None
    backend_copy_calls = 0

    try:
        library = load_single_library()

        bind_construction_ffi(
            library
        )

        (
            gguf_context,
            ggml_context,
            metadata_record,
        ) = build_metadata_context(
            library
        )

        provider_module = (
            import_frozen_provider()
        )

        (
            directory,
            join_by_pk,
            resident_record,
        ) = build_direct_resident_directory(
            provider_module
        )

        if mode == "correctness":
            guard = ParityProtectedIOGuard()

            sys.addaudithook(
                guard.audit_hook
            )

            telemetry = SerializedReadTelemetry(
                guard,
                provider_module,
                join_by_pk,
            )

            telemetry.install()

        before = (
            phase6f_process_snapshot()
        )

        # V2 treatment model-ready timing begins immediately
        # before provider/model construction.
        start_ns = time.perf_counter_ns()

        provider = (
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

        if mode == "correctness":
            original_backend_copy = (
                provider
                ._ggml_backend_tensor_set
            )

            def counted_backend_copy(*args):
                nonlocal backend_copy_calls

                backend_copy_calls += 1

                return original_backend_copy(
                    *args
                )

            provider._ggml_backend_tensor_set = (
                counted_backend_copy
            )

        model_handle = provider.initialize_model(
            ctypes.c_void_p(
                gguf_context
            )
        )

        phase6f_need(
            bool(model_handle),
            "treatment provider returned null model",
        )

        stop_ns = time.perf_counter_ns()

        after = (
            phase6f_process_snapshot()
        )

        provider_record = jsonable(
            provider.qualification_record()
        )

        correctness_record = None
        logits = None

        if mode == "correctness":
            (
                correctness_record,
                logits,
            ) = parity_inference_probe(
                library,
                model_handle,
                "treatment_maf",
            )

        telemetry_record = None

        if telemetry is not None:
            telemetry_record = (
                telemetry.record()
            )

            telemetry.restore()
            telemetry = None

        source_gguf_opens = None

        if guard is not None:
            source_gguf_opens = int(
                guard.source_gguf_opens
            )

        return {
            "status": "OK",
            "arm": "treatment",
            "mode": mode,
            "cache_regime":
                PHASE6F_CACHE_REGIME,
            "model_ready_elapsed_ns":
                int(stop_ns - start_ns),
            "process":
                phase6f_process_delta(
                    before,
                    after,
                ),
            "provider_qualification":
                provider_record,
            "resident":
                resident_record,
            "metadata":
                metadata_record,
            "backend_copy_calls":
                backend_copy_calls
                if mode == "correctness"
                else None,
            "source_gguf_opens":
                source_gguf_opens,
            "telemetry":
                telemetry_record,
            "correctness_record":
                jsonable(
                    correctness_record
                )
                if correctness_record
                is not None
                else None,
            "logits":
                [
                    float(value)
                    for value in logits
                ]
                if logits is not None
                else None,
        }

    finally:
        if telemetry is not None:
            try:
                telemetry.restore()
            except Exception:
                pass

        if (
            library is not None
            and model_handle
        ):
            try:
                library.llama_model_free(
                    as_void_p(
                        model_handle
                    )
                )
            except Exception:
                pass

        if (
            library is not None
            and gguf_context
        ):
            try:
                library.gguf_free(
                    gguf_context
                )
            except Exception:
                pass

        if (
            library is not None
            and ggml_context
        ):
            try:
                library.ggml_free(
                    ggml_context
                )
            except Exception:
                pass


def phase6f_child_control(mode):
    phase6f_verify_child_authority()

    library = None
    model_handle = None

    try:
        library = load_single_library()

        provider_module = (
            import_frozen_provider()
        )

        bind_construction_ffi(
            library
        )

        bind_parity_ffi(
            library,
            provider_module,
        )

        control_params = (
            library
            .llama_model_default_params()
        )

        before = (
            phase6f_process_snapshot()
        )

        # V2 control model-ready timing begins immediately
        # before the conventional GGUF load.
        start_ns = time.perf_counter_ns()

        model_handle = (
            library
            .llama_model_load_from_file(
                os.fsencode(
                    SOURCE_GGUF
                ),
                control_params,
            )
        )

        phase6f_need(
            bool(model_handle),
            "control conventional loader returned null",
        )

        stop_ns = time.perf_counter_ns()

        after = (
            phase6f_process_snapshot()
        )

        correctness_record = None
        logits = None

        if mode == "correctness":
            (
                correctness_record,
                logits,
            ) = parity_inference_probe(
                library,
                model_handle,
                "control_gguf",
            )

        return {
            "status": "OK",
            "arm": "control",
            "mode": mode,
            "cache_regime":
                PHASE6F_CACHE_REGIME,
            "loader":
                "llama_model_load_from_file",
            "model_ready_elapsed_ns":
                int(stop_ns - start_ns),
            "process":
                phase6f_process_delta(
                    before,
                    after,
                ),
            "correctness_record":
                jsonable(
                    correctness_record
                )
                if correctness_record
                is not None
                else None,
            "logits":
                [
                    float(value)
                    for value in logits
                ]
                if logits is not None
                else None,
        }

    finally:
        if (
            library is not None
            and model_handle
        ):
            try:
                library.llama_model_free(
                    as_void_p(
                        model_handle
                    )
                )
            except Exception:
                pass


def phase6f_emit_child(value):
    raw = phase6f_canonical_json_bytes(
        value
    )

    print(
        "PHASE6F_CHILD_JSON="
        + raw.decode("utf-8")
    )


def phase6f_child_main(
    arm,
    mode,
):
    phase6f_need(
        arm in (
            "treatment",
            "control",
        ),
        "invalid child arm",
    )

    phase6f_need(
        mode in (
            "warmup",
            "measure",
            "correctness",
        ),
        "invalid child mode",
    )

    if arm == "treatment":
        value = phase6f_child_treatment(
            mode
        )
    else:
        value = phase6f_child_control(
            mode
        )

    phase6f_emit_child(
        value
    )


def phase6f_run_child(
    arm,
    mode,
):
    env = os.environ.copy()

    env[
        PHASE6F_CHILD_ENV
    ] = env[
        PHASE6F_RUNNER_SHA_ENV
    ]

    command = [
        sys.executable,
        str(PHASE6F_RUNNER_PATH),
        "--child",
        arm,
        "--mode",
        mode,
    ]

    parent_start = (
        time.perf_counter_ns()
    )

    try:
        cp = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=
                PHASE6F_CHILD_TIMEOUT_SECONDS,
            check=False,
        )

    except subprocess.TimeoutExpired as exc:
        return {
            "status": "TIMEOUT",
            "arm": arm,
            "mode": mode,
            "timeout_seconds":
                PHASE6F_CHILD_TIMEOUT_SECONDS,
            "parent_elapsed_ns":
                int(
                    time.perf_counter_ns()
                    - parent_start
                ),
            "stdout":
                (exc.stdout or b"").decode(
                    errors="replace"
                ),
            "stderr":
                (exc.stderr or b"").decode(
                    errors="replace"
                ),
        }

    parent_elapsed = (
        time.perf_counter_ns()
        - parent_start
    )

    stdout = cp.stdout.decode(
        errors="replace"
    )

    stderr = cp.stderr.decode(
        errors="replace"
    )

    if cp.returncode != 0:
        return {
            "status": "FAILED",
            "arm": arm,
            "mode": mode,
            "returncode":
                cp.returncode,
            "parent_elapsed_ns":
                int(parent_elapsed),
            "stdout": stdout,
            "stderr": stderr,
        }

    prefix = "PHASE6F_CHILD_JSON="

    payloads = [
        line[len(prefix):]
        for line in stdout.splitlines()
        if line.startswith(prefix)
    ]

    if len(payloads) != 1:
        return {
            "status":
                "FAILED_CHILD_PROTOCOL",
            "arm": arm,
            "mode": mode,
            "returncode":
                cp.returncode,
            "parent_elapsed_ns":
                int(parent_elapsed),
            "stdout": stdout,
            "stderr": stderr,
        }

    try:
        value = json.loads(
            payloads[0]
        )

    except json.JSONDecodeError:
        return {
            "status":
                "FAILED_CHILD_JSON",
            "arm": arm,
            "mode": mode,
            "returncode":
                cp.returncode,
            "parent_elapsed_ns":
                int(parent_elapsed),
            "stdout": stdout,
            "stderr": stderr,
        }

    value["parent_elapsed_ns"] = int(
        parent_elapsed
    )

    value["child_stderr"] = stderr

    return value


def phase6f_find_numeric(
    value,
    keys,
):
    wanted = {
        str(key).lower()
        for key in keys
    }

    stack = [value]

    while stack:
        current = stack.pop()

        if isinstance(current, dict):
            for key, item in current.items():
                if (
                    str(key).lower()
                    in wanted
                    and isinstance(
                        item,
                        (int, float),
                    )
                    and not isinstance(
                        item,
                        bool,
                    )
                ):
                    return item

                stack.append(item)

        elif isinstance(current, list):
            stack.extend(current)

    return None


def phase6f_correctness_guard(label):
    treatment = phase6f_run_child(
        "treatment",
        "correctness",
    )

    control = phase6f_run_child(
        "control",
        "correctness",
    )

    failures = []

    if treatment.get("status") != "OK":
        failures.append(
            "treatment child did not complete"
        )

    if control.get("status") != "OK":
        failures.append(
            "control child did not complete"
        )

    if failures:
        return {
            "label": label,
            "valid": False,
            "failures": failures,
            "treatment": treatment,
            "control": control,
        }

    treatment_logits = treatment.get(
        "logits"
    )

    control_logits = control.get(
        "logits"
    )

    if not isinstance(
        treatment_logits,
        list,
    ):
        failures.append(
            "treatment logits missing"
        )

    if not isinstance(
        control_logits,
        list,
    ):
        failures.append(
            "control logits missing"
        )

    if failures:
        return {
            "label": label,
            "valid": False,
            "failures": failures,
            "treatment": treatment,
            "control": control,
        }

    if len(
        treatment_logits
    ) != PHASE6F_EXPECTED_VOCAB:
        failures.append(
            "treatment vocab mismatch"
        )

    if len(
        control_logits
    ) != PHASE6F_EXPECTED_VOCAB:
        failures.append(
            "control vocab mismatch"
        )

    tolerance_failures = 0
    max_abs_error = 0.0
    sum_abs_error = 0.0
    sum_square_error = 0.0

    if (
        len(treatment_logits)
        == len(control_logits)
        == PHASE6F_EXPECTED_VOCAB
    ):
        for (
            treatment_value,
            control_value,
        ) in zip(
            treatment_logits,
            control_logits,
        ):
            if (
                not math.isfinite(
                    treatment_value
                )
                or not math.isfinite(
                    control_value
                )
            ):
                tolerance_failures += 1
                continue

            delta = abs(
                treatment_value
                - control_value
            )

            max_abs_error = max(
                max_abs_error,
                delta,
            )

            sum_abs_error += delta
            sum_square_error += (
                delta * delta
            )

            limit = (
                PHASE6F_CORRECTNESS_TOL_ABS
                + PHASE6F_CORRECTNESS_TOL_REL
                * abs(control_value)
            )

            if delta > limit:
                tolerance_failures += 1

    if tolerance_failures:
        failures.append(
            "logit tolerance failure"
        )

    treatment_argmax = max(
        range(len(treatment_logits)),
        key=treatment_logits.__getitem__,
    )

    control_argmax = max(
        range(len(control_logits)),
        key=control_logits.__getitem__,
    )

    if (
        treatment_argmax
        != control_argmax
    ):
        failures.append(
            "argmax mismatch"
        )

    treatment_top10 = sorted(
        range(len(treatment_logits)),
        key=treatment_logits.__getitem__,
        reverse=True,
    )[:10]

    control_top10 = sorted(
        range(len(control_logits)),
        key=control_logits.__getitem__,
        reverse=True,
    )[:10]

    if (
        treatment_top10
        != control_top10
    ):
        failures.append(
            "top-10 order mismatch"
        )

    treatment_tokens = (
        phase6f_find_numeric(
            treatment.get(
                "correctness_record"
            ),
            (
                "token_count",
                "prompt_token_count",
                "n_tokens",
            ),
        )
    )

    control_tokens = (
        phase6f_find_numeric(
            control.get(
                "correctness_record"
            ),
            (
                "token_count",
                "prompt_token_count",
                "n_tokens",
            ),
        )
    )

    if (
        int(treatment_tokens)
        if treatment_tokens
        is not None
        else None
    ) != PHASE6F_EXPECTED_TOKEN_COUNT:
        failures.append(
            "treatment token count not 28"
        )

    if (
        int(control_tokens)
        if control_tokens
        is not None
        else None
    ) != PHASE6F_EXPECTED_TOKEN_COUNT:
        failures.append(
            "control token count not 28"
        )

    if treatment.get(
        "backend_copy_calls"
    ) != PHASE6F_EXPECTED_BACKEND_COPIES:
        failures.append(
            "treatment backend copies not 339"
        )

    if treatment.get(
        "source_gguf_opens"
    ) != 0:
        failures.append(
            "treatment source-GGUF opens nonzero"
        )

    if control.get(
        "loader"
    ) != "llama_model_load_from_file":
        failures.append(
            "control loader mismatch"
        )

    count = len(
        treatment_logits
    )

    mean_abs_error = (
        sum_abs_error / count
        if count
        else None
    )

    rmse = (
        math.sqrt(
            sum_square_error / count
        )
        if count
        else None
    )

    treatment.pop(
        "logits",
        None,
    )

    control.pop(
        "logits",
        None,
    )

    return {
        "label": label,
        "valid": not failures,
        "failures": failures,
        "token_count_treatment":
            treatment_tokens,
        "token_count_control":
            control_tokens,
        "vocab_size_treatment":
            PHASE6F_EXPECTED_VOCAB,
        "vocab_size_control":
            PHASE6F_EXPECTED_VOCAB,
        "tolerance_failures":
            tolerance_failures,
        "max_abs_error":
            max_abs_error,
        "mean_abs_error":
            mean_abs_error,
        "rmse": rmse,
        "same_argmax":
            treatment_argmax
            == control_argmax,
        "argmax_treatment":
            treatment_argmax,
        "argmax_control":
            control_argmax,
        "top10_equal":
            treatment_top10
            == control_top10,
        "top10_treatment":
            treatment_top10,
        "top10_control":
            control_top10,
        "treatment_backend_copies":
            treatment.get(
                "backend_copy_calls"
            ),
        "treatment_source_gguf_opens":
            treatment.get(
                "source_gguf_opens"
            ),
        "control_loader":
            control.get("loader"),
        "generation": False,
        "treatment": treatment,
        "control": control,
    }


def phase6f_nearest_rank_p95(values):
    if not values:
        return None

    ordered = sorted(values)

    rank = math.ceil(
        0.95 * len(ordered)
    )

    rank = max(
        1,
        min(
            rank,
            len(ordered),
        ),
    )

    return ordered[
        rank - 1
    ]


def phase6f_summary(values):
    if not values:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
            "median": None,
            "p95_nearest_rank": None,
        }

    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean":
            statistics.fmean(values),
        "median":
            statistics.median(values),
        "p95_nearest_rank":
            phase6f_nearest_rank_p95(
                values
            ),
    }


def phase6f_measurement_aggregates(trials):
    treatment_values = [
        row[
            "model_ready_elapsed_ns"
        ]
        for row in trials
        if (
            row.get("status") == "OK"
            and row.get("arm")
            == "treatment"
        )
    ]

    control_values = [
        row[
            "model_ready_elapsed_ns"
        ]
        for row in trials
        if (
            row.get("status") == "OK"
            and row.get("arm")
            == "control"
        )
    ]

    treatment_summary = (
        phase6f_summary(
            treatment_values
        )
    )

    control_summary = (
        phase6f_summary(
            control_values
        )
    )

    treatment_median = (
        treatment_summary["median"]
    )

    control_median = (
        control_summary["median"]
    )

    absolute_delta = None
    median_ratio = None

    if (
        treatment_median is not None
        and control_median is not None
    ):
        absolute_delta = (
            treatment_median
            - control_median
        )

        if control_median != 0:
            median_ratio = (
                treatment_median
                / control_median
            )

    by_pair = {}

    for row in trials:
        if row.get("status") != "OK":
            continue

        pair_index = row.get(
            "pair_index"
        )

        by_pair.setdefault(
            pair_index,
            {},
        )[
            row["arm"]
        ] = row[
            "model_ready_elapsed_ns"
        ]

    paired_ratios = []

    for pair_index in range(
        1,
        len(PHASE6F_PAIR_SEQUENCE) + 1,
    ):
        pair_record = by_pair.get(
            pair_index,
            {},
        )

        treatment_value = (
            pair_record.get(
                "treatment"
            )
        )

        control_value = (
            pair_record.get(
                "control"
            )
        )

        ratio = None

        if (
            treatment_value is not None
            and control_value
            not in (
                None,
                0,
            )
        ):
            ratio = (
                treatment_value
                / control_value
            )

        paired_ratios.append(
            {
                "pair_index":
                    pair_index,
                "ratio_treatment_over_control":
                    ratio,
            }
        )

    return {
        "treatment":
            treatment_summary,
        "control":
            control_summary,
        "model_ready_elapsed_ns": {
            "treatment_median":
                treatment_median,
            "control_median":
                control_median,
            "absolute_median_delta":
                absolute_delta,
            "treatment_control_median_ratio":
                median_ratio,
            "paired_trial_ratios":
                paired_ratios,
        },
    }


def phase6f_write_result_exclusive(result):
    raw = phase6f_canonical_json_bytes(
        result
    )

    fd = os.open(
        PHASE6F_RESULT_PATH,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL,
        0o600,
    )

    try:
        offset = 0

        while offset < len(raw):
            count = os.write(
                fd,
                raw[offset:],
            )

            if count <= 0:
                raise Phase6FExecutionError(
                    "short result write"
                )

            offset += count

        os.fsync(fd)

    finally:
        os.close(fd)

    return {
        "bytes": len(raw),
        "sha256":
            hashlib.sha256(
                raw
            ).hexdigest(),
    }


def phase6f_parent_main():
    authority = (
        phase6f_runtime_authority()
    )

    pre_run_thermal = (
        phase6f_thermal_snapshot()
    )

    phase6f_need(
        phase6f_thermal_acceptable(
            pre_run_thermal
        ),
        "pre-run thermal/environment "
        "qualification failed",
    )

    sentinel_record = (
        phase6f_reserve_sentinel(
            authority
        )
    )

    correctness_preflight = (
        phase6f_correctness_guard(
            "preflight"
        )
    )

    if not correctness_preflight[
        "valid"
    ]:
        result = {
            "schema":
                PHASE6F_RESULT_SCHEMA,
            "phase": "6F",
            "authority": authority,
            "cache_regime":
                PHASE6F_CACHE_REGIME,
            "pair_sequence": [
                list(pair)
                for pair
                in PHASE6F_PAIR_SEQUENCE
            ],
            "correctness_preflight":
                correctness_preflight,
            "warmups": [],
            "raw_trials": [],
            "aggregates": None,
            "correctness_postflight":
                None,
            "thermal": {
                "pre_run":
                    pre_run_thermal,
                "around_pairs": [],
                "post_run": None,
            },
            "governance": {
                "timeout_seconds":
                    PHASE6F_CHILD_TIMEOUT_SECONDS,
                "sentinel":
                    sentinel_record,
                "adaptive_stopping":
                    False,
                "replacement_trials":
                    False,
                "outlier_deletion":
                    False,
            },
            "final_disposition":
                "INVALID - CORRECTNESS PREFLIGHT FAILURE",
        }

        phase6f_write_result_exclusive(
            result
        )

        return 2

    warmups = []

    for arm in (
        "treatment",
        "control",
    ):
        warmup = phase6f_run_child(
            arm,
            "warmup",
        )

        warmups.append(
            warmup
        )

        if warmup.get("status") != "OK":
            result = {
                "schema":
                    PHASE6F_RESULT_SCHEMA,
                "phase": "6F",
                "authority":
                    authority,
                "cache_regime":
                    PHASE6F_CACHE_REGIME,
                "pair_sequence": [
                    list(pair)
                    for pair
                    in PHASE6F_PAIR_SEQUENCE
                ],
                "correctness_preflight":
                    correctness_preflight,
                "warmups":
                    warmups,
                "raw_trials": [],
                "aggregates":
                    None,
                "correctness_postflight":
                    None,
                "thermal": {
                    "pre_run":
                        pre_run_thermal,
                    "around_pairs": [],
                    "post_run": None,
                },
                "governance": {
                    "timeout_seconds":
                        PHASE6F_CHILD_TIMEOUT_SECONDS,
                    "sentinel":
                        sentinel_record,
                    "adaptive_stopping":
                        False,
                    "replacement_trials":
                        False,
                    "outlier_deletion":
                        False,
                },
                "final_disposition":
                    "INVALID - MEASUREMENT FAILURE",
            }

            phase6f_write_result_exclusive(
                result
            )

            return 3

    raw_trials = []
    thermal_pairs = []
    thermal_abort = False
    treatment_ordinal = 0
    control_ordinal = 0

    for (
        pair_index,
        pair,
    ) in enumerate(
        PHASE6F_PAIR_SEQUENCE,
        1,
    ):
        before_thermal = (
            phase6f_thermal_snapshot()
        )

        before_acceptable = (
            phase6f_thermal_acceptable(
                before_thermal
            )
        )

        thermal_record = {
            "pair_index":
                pair_index,
            "before":
                before_thermal,
            "before_acceptable":
                before_acceptable,
            "after":
                None,
            "after_acceptable":
                None,
        }

        thermal_pairs.append(
            thermal_record
        )

        if not before_acceptable:
            thermal_abort = True
            break

        for (
            pair_position,
            code,
        ) in enumerate(
            pair,
            1,
        ):
            if code == "T":
                arm = "treatment"
                treatment_ordinal += 1
                arm_ordinal = (
                    treatment_ordinal
                )
            else:
                arm = "control"
                control_ordinal += 1
                arm_ordinal = (
                    control_ordinal
                )

            trial = phase6f_run_child(
                arm,
                "measure",
            )

            trial[
                "pair_index"
            ] = pair_index

            trial[
                "pair_position"
            ] = pair_position

            trial[
                "arm_trial_ordinal"
            ] = arm_ordinal

            trial[
                "frozen_pair_order"
            ] = list(pair)

            raw_trials.append(
                trial
            )

        after_thermal = (
            phase6f_thermal_snapshot()
        )

        after_acceptable = (
            phase6f_thermal_acceptable(
                after_thermal
            )
        )

        thermal_record[
            "after"
        ] = after_thermal

        thermal_record[
            "after_acceptable"
        ] = after_acceptable

        if not after_acceptable:
            thermal_abort = True
            break

    post_run_thermal = (
        phase6f_thermal_snapshot()
    )

    complete_trial_count = (
        len(raw_trials)
        == PHASE6F_MEASURED_TOTAL
        and treatment_ordinal
        == PHASE6F_TREATMENT_TRIALS
        and control_ordinal
        == PHASE6F_CONTROL_TRIALS
    )

    measurement_failures = [
        row
        for row in raw_trials
        if row.get("status") != "OK"
    ]

    aggregates = (
        phase6f_measurement_aggregates(
            raw_trials
        )
    )

    correctness_postflight = None

    if (
        not thermal_abort
        and complete_trial_count
    ):
        correctness_postflight = (
            phase6f_correctness_guard(
                "postflight"
            )
        )

    if thermal_abort:
        disposition = (
            "INVALID - THERMAL/ENVIRONMENT FAILURE"
        )

    elif not complete_trial_count:
        disposition = (
            "INVALID - MEASUREMENT FAILURE"
        )

    elif measurement_failures:
        disposition = (
            "INVALID - MEASUREMENT FAILURE"
        )

    elif (
        correctness_postflight
        is None
        or not correctness_postflight[
            "valid"
        ]
    ):
        disposition = (
            "INVALID - CORRECTNESS POSTFLIGHT FAILURE"
        )

    else:
        disposition = (
            "VALID - BASELINE CHARACTERIZATION COMPLETE"
        )

    result = {
        "schema":
            PHASE6F_RESULT_SCHEMA,
        "phase": "6F",
        "scientific_purpose":
            "baseline performance characterization after correctness",
        "claim_boundary": {
            "superiority_claim":
                False,
            "native_maf_compute_claim":
                False,
            "zero_copy_claim":
                False,
            "cross_device_generality":
                False,
            "cross_model_generality":
                False,
            "energy_claim":
                False,
        },
        "authority":
            authority,
        "runtime": {
            "python":
                sys.version,
            "executable":
                sys.executable,
            "platform":
                sys.platform,
            "pid":
                os.getpid(),
        },
        "benchmark_contract": {
            "primary_metric":
                "model_ready_elapsed_ns",
            "timer":
                "time.perf_counter_ns",
            "cache_regime":
                PHASE6F_CACHE_REGIME,
            "fresh_child_process":
                True,
            "warmup_treatment":
                1,
            "warmup_control":
                1,
            "measured_treatment":
                PHASE6F_TREATMENT_TRIALS,
            "measured_control":
                PHASE6F_CONTROL_TRIALS,
            "measured_total":
                PHASE6F_MEASURED_TOTAL,
            "pair_sequence": [
                list(pair)
                for pair
                in PHASE6F_PAIR_SEQUENCE
            ],
            "adaptive_stopping":
                False,
            "replacement_trials":
                False,
            "timeout_seconds":
                PHASE6F_CHILD_TIMEOUT_SECONDS,
        },
        "thermal_policy": {
            "method":
                "sysfs_thermal_zone_temp_v1",
            "abort_threshold_celsius":
                PHASE6F_THERMAL_ABORT_C,
            "slow_trial_selection":
                False,
        },
        "correctness_preflight":
            correctness_preflight,
        "warmups":
            warmups,
        "raw_trials":
            raw_trials,
        "aggregates":
            aggregates,
        "thermal": {
            "pre_run":
                pre_run_thermal,
            "around_pairs":
                thermal_pairs,
            "post_run":
                post_run_thermal,
            "abort_triggered":
                thermal_abort,
        },
        "correctness_postflight":
            correctness_postflight,
        "governance": {
            "sentinel":
                sentinel_record,
            "whole_run_retry":
                False,
            "adaptive_stopping":
                False,
            "replacement_trials":
                False,
            "outlier_deletion":
                False,
            "raw_failed_trials_preserved":
                True,
        },
        "final_disposition":
            disposition,
    }

    write_record = (
        phase6f_write_result_exclusive(
            result
        )
    )

    print(
        json.dumps(
            {
                "disposition":
                    disposition,
                "result":
                    write_record,
                "measured_records":
                    len(raw_trials),
                "treatment_records":
                    treatment_ordinal,
                "control_records":
                    control_ordinal,
            },
            sort_keys=True,
        )
    )

    if disposition == (
        "VALID - BASELINE CHARACTERIZATION COMPLETE"
    ):
        return 0

    return 4


def phase6f_cli():
    parser = argparse.ArgumentParser(
        description=(
            "OpenMind Phase 6F V2 "
            "access/provisioning benchmark"
        )
    )

    parser.add_argument(
        "--child",
        choices=(
            "treatment",
            "control",
        ),
    )

    parser.add_argument(
        "--mode",
        choices=(
            "warmup",
            "measure",
            "correctness",
        ),
    )

    args = parser.parse_args()

    if args.child is not None:
        phase6f_need(
            args.mode is not None,
            "--mode required for child",
        )

        phase6f_child_main(
            args.child,
            args.mode,
        )

        return 0

    phase6f_need(
        args.mode is None,
        "--mode is child-only",
    )

    return phase6f_parent_main()


if __name__ == "__main__":
    raise SystemExit(
        phase6f_cli()
    )
