#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import os
import runpy
import stat
import sys
from pathlib import Path


PREFLIGHT_HEAD = 'b3920e0b9e8d819b881cc02d23779245e01949d7'
LLAMA_HEAD = '4cf5cab65d5257be31e7623eb552b1861e969c75'
EXTRACTOR_SHA256 = '12d1289636057b659a8e5769ab76c68a02ee4e53ca4044e949aef7fe69e62110'
PROTOCOL_SHA256 = '5d3063745be9b036769d73726830a11d9458f4a447daf09ac22c6c045c2e6af4'
INVENTORY_SHA256 = '7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee'
EXPECTED_SOURCE_SIZE = 1894532160

ROOT = Path(__file__).resolve().parents[2]
LLAMA = ROOT / 'llama.cpp'

EXTRACTOR = ROOT / 'experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_extractor_v1.py'
PROTOCOL = ROOT / 'experiments/model_fractal/MAF_PHASE_6E_D_CLASS_A_GGUF_METADATA_AUTHORITY_CONSTRUCTION_PROTOCOL_V1.md'
INVENTORY = ROOT / 'experiments/model_fractal/gguf_tensor_inventory_v1.json'

SOURCE = Path.home() / 'qwen2.5-coder-q8_0.gguf'

AUTHORITY = ROOT / (
    'experiments/model_fractal/'
    'maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json'
)

BUILDING = AUTHORITY.with_name(
    AUTHORITY.name + '.building'
)

SLOT_DIR = Path.home() / '.openmind_authoritative_slots'

SENTINEL = SLOT_DIR / 'phase_6e_d_class_a_gguf_metadata_authority_b3920e0b9e8d819b881cc02d23779245e01949d7.spent'


class WrapperError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WrapperError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            block = f.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def verify_regular(path: Path, label: str) -> os.stat_result:
    st = os.lstat(path)
    require(stat.S_ISREG(st.st_mode), label + ' is not regular')
    require(not stat.S_ISLNK(st.st_mode), label + ' is symlink')
    return st


def verify_llama_detached_head() -> None:
    git_dir = LLAMA / '.git'
    require(git_dir.is_dir(), 'llama .git directory missing')
    require(not git_dir.is_symlink(), 'llama .git is symlink')
    head_path = git_dir / 'HEAD'
    st = verify_regular(head_path, 'llama HEAD')
    require(st.st_size <= 256, 'llama HEAD unexpectedly large')
    value = head_path.read_text(encoding='ascii').strip()
    require(value == LLAMA_HEAD, 'llama detached HEAD mismatch')


def preflight() -> None:
    require(EXTRACTOR.is_file(), 'frozen extractor missing')
    require(not EXTRACTOR.is_symlink(), 'extractor is symlink')
    require(sha256_file(EXTRACTOR) == EXTRACTOR_SHA256, 'extractor SHA mismatch')

    require(PROTOCOL.is_file(), 'protocol missing')
    require(not PROTOCOL.is_symlink(), 'protocol is symlink')
    require(sha256_file(PROTOCOL) == PROTOCOL_SHA256, 'protocol SHA mismatch')

    require(INVENTORY.is_file(), 'inventory missing')
    require(not INVENTORY.is_symlink(), 'inventory is symlink')
    require(sha256_file(INVENTORY) == INVENTORY_SHA256, 'inventory SHA mismatch')

    verify_llama_detached_head()

    source_st = os.lstat(SOURCE)
    require(stat.S_ISREG(source_st.st_mode), 'source is not regular')
    require(not stat.S_ISLNK(source_st.st_mode), 'source is symlink')
    require(source_st.st_size == EXPECTED_SOURCE_SIZE, 'source stat size mismatch')

    require(not AUTHORITY.exists(), 'authority output already exists')
    require(not BUILDING.exists(), 'authority building path already exists')

    slot_st = os.lstat(SLOT_DIR)
    require(stat.S_ISDIR(slot_st.st_mode), 'slot namespace not directory')
    require(not stat.S_ISLNK(slot_st.st_mode), 'slot namespace is symlink')
    require(SENTINEL.parent.resolve() == SLOT_DIR.resolve(), 'sentinel namespace mismatch')
    require(not SENTINEL.exists(), 'one-shot sentinel already spent')

def execute_frozen_extractor() -> None:
    old_argv = list(sys.argv)
    try:
        sys.argv = [
            str(EXTRACTOR),
            '--sentinel',
            str(SENTINEL),
        ]
        try:
            runpy.run_path(
                str(EXTRACTOR),
                run_name='__main__',
            )
        except SystemExit as exc:
            code = exc.code
            if code is None:
                code = 0
            require(isinstance(code, int), 'extractor returned non-integer status')
            require(code == 0, 'extractor failed with status ' + str(code))
    finally:
        sys.argv = old_argv

def postflight() -> str:
    sentinel_st = os.lstat(SENTINEL)
    require(stat.S_ISREG(sentinel_st.st_mode), 'spent sentinel not regular')
    require(not stat.S_ISLNK(sentinel_st.st_mode), 'spent sentinel is symlink')

    authority_st = os.lstat(AUTHORITY)
    require(stat.S_ISREG(authority_st.st_mode), 'authority not regular')
    require(not stat.S_ISLNK(authority_st.st_mode), 'authority is symlink')
    require(authority_st.st_size > 0, 'authority is empty')
    require(not BUILDING.exists(), 'authority building residue remains')
    return sha256_file(AUTHORITY)

def main() -> int:
    preflight()
    print('ONE-SHOT PREFLIGHT : PASS')
    print('PREFLIGHT HEAD     :', PREFLIGHT_HEAD)
    print('SENTINEL           :', SENTINEL)
    print('SOURCE OPENED      : NO')
    execute_frozen_extractor()
    authority_sha = postflight()
    print('ONE-SHOT EXECUTION : PASS')
    print('AUTHORITY          :', AUTHORITY)
    print('AUTHORITY SHA256   :', authority_sha)
    print('SENTINEL SPENT     : PASS')
    print('MODEL EXECUTION    : NO')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except WrapperError as exc:
        print('CLASS-A METADATA ONE-SHOT WRAPPER FAILED')
        print('ERROR:', exc)
        raise SystemExit(1)
