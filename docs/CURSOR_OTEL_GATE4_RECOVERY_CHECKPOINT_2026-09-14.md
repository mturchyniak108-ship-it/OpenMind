# Cursor / OTEL Gate-4 Recovery Checkpoint

Date: 2026-09-14
Branch: labs/multidimensional-maf
Pre-checkpoint HEAD: 0741b75774938b88412eeb648fb80c67a4e4ed96

## Purpose

This local checkpoint freezes the qualified Cursor and OpenTelemetry Gate-4 recovery state.
It does not authorize Cursor execution or a remote Git push.

## MAF packaging delta

The pre-existing pyproject.toml delta adds the MAF namespace to setuptools package discovery.

Expected worktree SHA256: 3418787c4becb74b875c5766193171d131fa2382ff1fbfe504e7a1287c767e6f
Expected whole tracked diff SHA256: fe96666c436388ebacbc8ac5db6e6d15ccbede58e8971a2ed651e5d6ae17b018

## Frozen Cursor authority

Cursor package path:
/data/data/com.termux/files/home/.local/share/cursor-native-port/qualification/2026.09.10-fd3934a-linux-arm64-20260912T233604/package/dist-package/index.js

Cursor package SHA256:
890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054

Isolated OTEL global-utils webpack record SHA256:
ac0b3280fe5d4e8debe9f330dcc16138422565b618e96bf08a505cace837cc72

Recovered original global-utils body SHA256:
4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16

## Recovered original Gate-4 contract

Original helper: OTEL_GLOBAL_UTILS_MACRO_GSV2
Gate 3: ANDROID globalThis/global HOST IDENTITY
Gate 4: global-utils RECURSIVE MACRO

Gate 4 called qualify_module on the exact global-utils module.
It then collected declarators whose kind was HOST_GLOBAL_SELECTION.
It required exactly one such declarator.

Recovered frontier declarator SHA256:
6adba4073746c617b4ef724887ae4fdd72cb5073f5694176777a63fea650f6b3

Recovered frontier declarator:
r="object"==typeof globalThis?globalThis:global

The packaged Cursor source independently qualifies exactly one host-global selector expression.
Therefore raw globalThis or global token counting is not the proven defect.

The unresolved defect is bounded to the original parser, classifier, or row-emission path.
The original observed HOST_GLOBAL_SELECTION row count remains unknown.

## Next defined frontier

After Gate 4 passes, the recovered next gate is API/OTEL DOWNSTREAM PROPAGATION GATE.
The historical path continues through api/context.js, context-api.js, otel.js, file-url, and local-worker.

Cursor must not be rerun until the static qualification chain authorizes it.

## Safety boundary

- Cursor execution: NO
- Cursor bundle execution: NO
- Cursor source modification: NO
- Remote Git push: NO
- Force push: NO
- Unrelated untracked-file mutation: NO

## 2026-09-15 — global-utils dual-completion in-memory qualification

Status: PASS — static recovery only. No completion persistence, next-module read, Gate 5 evaluation, source execution, or Cursor execution was authorized.

Frozen evidence:

- Detailed-field audit SHA256: `8fb234c640aac2a06e1beba14c08fa514a0b6f6d368377549fa3bc86814f54fe`
- Body-chars evidence SHA256: `0319e2fba2c41058de19bdfe0b3ca5f56e8c40f42ea7ba4be8cfbe36699a92ad`
- State-shape evidence SHA256: `8a1ec745b85e4dc7d4d4356e2b8523dafc150e28b379deca4c61fa1ae966e4a9`
- Relationship evidence SHA256: `02700b77185c2bf1ad150195ec3de02f06dddfe43993954a0aa4380f152bd344`
- Completion evidence SHA256: `339fed2b2ab78fb33c5f7d55e567a4a63a505967ca90faf02e2a3ce07df4f678`
- Twelve-row sequence SHA256: `79294f5863f7bb3c4617e77e8bb87bbc395064071c856be3f5a97c423d1aff73`
- Initialized mapping SHA256: `978d80437883468abcae3e2db253d73bf2f5ecec792c0f16ba0ff65d66f9bd0b`
- Dual-representation contract SHA256: `7e961379694c133a42d64c4af4bd4f2232f43e616301d7acb3f6ce1124749c91`
- Proposed summary-state SHA256: `31de44f1ad75d37e58713527f7aed71d15fa7ac2af4bf2ce641c093019d1a945`
- Proposed recursive-state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Completion-state evidence SHA256: `ae914b7644b9ab937bbc8e58609d53a034af5e06d04a3e1cdfd43fb75d955634`

Qualified in-memory recursive completion:

- body_chars: `1377`
- rows: `12`
- initialized: `["r","s","i","o","a","l","u","c","d","m"]`
- exports: `{"$G":"()=>c","kv":"()=>m","mS":"()=>d"}`
- class_like: `{}`
- bundle_code_executed: `false`
- function_bodies_executed: `false`
- dependency omitted in completed recursive representation
- terminal next fields omitted from recursive representation

Qualified summary completion:

- advanced_items: `12`
- completed: `true`
- next_kind: `null`
- next_sha256: `null`
- next_source: `null`

Strict frontier remains closed at completion persistence authorization.
