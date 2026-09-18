# Cursor / OTEL Gate 4 — proto3 function x destructuring n binding scope repair — Gold Standard V2

## Source authority

- Source HEAD: `6a94c7d4d1c614f04d85ffe84d9a566bf5b27312`
- Source tree: `2962ad0eeeb77a8815abe610454a63eb4e5884e4`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_X_DESTRUCTURING_N_CLASSIFICATION_GSV2_2026-09-16.md`
- Prior document SHA256: `8d49b51a15aea7311abbf7f2402494850cf2784b21010a5f2f80131ac86aa8ff`
- Prior classification authority SHA256: `cc76a0bac1e96af90e5edf165c967a8e55461e694964adbb56aeeed5184db9cc`

## Corrected pattern validation

- Pattern start: `9152`
- Pattern end: `9157`
- Exact recovered pattern: `[t,n]`
- Pattern SHA256: `2b17f8a45fe7a1ca4879aaa6a6b6c9ca91640b55cc20a259d50f74008c0dfc94`
- Binding n coordinate: `9155`

The pattern is validated by its committed coordinates and SHA256. No literal pattern text was assumed by the helper.

## Declaration and ownership semantics

- Declaration kind: `const`
- Declaration keyword coordinate: `9147`
- Binding relation: `NEW_BLOCK_SCOPED_SHADOW_BINDING`
- Qualified owner kind: `DESTRUCTURING_BINDING`
- Qualified owner SHA256: `b302109d03f5d30421e8e11301744621723af568ab83d0834fe28a0b5f0de2de`
- Scope kind: `LEXICAL_BLOCK_SCOPE`
- Scope open: `9129`
- Scope close proven: `true`
- Scope close: `9344`
- Binding authority SHA256: `ae45df6153e6d504c475dc931d898817f5e51f0249f8150fd8b9a51a5c10db6a`

## Frozen frontier

- Stop kind: `DESTRUCTURING_BLOCK_SHADOW_SCOPE_QUALIFIED`
- Frontier coordinate: `9344`
- Scope window: `9274–9415`
- Scope-window SHA256: `426969b03934177cb69e2ffcf62dc20bc68246ebb458d36ed31a120a708e62f9`

No n reference after the destructuring declaration was qualified by this repair step.

## Proto3 identity

- Record SHA256: `fdd6e029c7990fa35cf52ab0b0f3eb0b347d95d74d6105c831dd8ce8650dd56d`
- Record end semantics: `END_EXCLUSIVE`
- Body offset inside record: `111`
- Body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Committed pattern coordinates and SHA validation: `AUTHORIZED AND PERFORMED`
- Declaration-kind replay: `AUTHORIZED AND PERFORMED`
- Binding relationship qualification: `AUTHORIZED AND PERFORMED`
- Scope characterization: `AUTHORIZED AND PERFORMED`
- Reference scan beyond this binding frontier: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Canonical evidence SHA256

`9256a0465e0ef2e4c5316640664d15e0094f652f5b66bd0a79b7b3c55b46e0ce`

## Next eligible step

Resume the recursive ownership super-macro with the destructuring n shadow active through coordinate 9344, then restore the function-x parameter owner.
