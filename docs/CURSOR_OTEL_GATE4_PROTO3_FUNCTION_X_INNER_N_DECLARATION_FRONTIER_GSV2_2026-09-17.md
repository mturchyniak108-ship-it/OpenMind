# Cursor / OTEL Gate 4 — proto3 function x inner n declaration frontier — Gold Standard V2

## Source authority

- Source HEAD: `f8631f9f469b20b4bae8ca7bc8312492981aca49`
- Source tree: `fa7adc58cfb49ef565fafdcbdfeafa27862a6775`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior scope authority: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_X_DESTRUCTURING_N_BINDING_SCOPE_GSV2_2026-09-17.md`
- Prior scope document SHA256: `7549aaa14b7ac03c2bbe250a91709b7c000a418e341d943f860cafebc18ded54`
- Prior scope evidence SHA256: `9256a0465e0ef2e4c5316640664d15e0094f652f5b66bd0a79b7b3c55b46e0ce`
- Prior binding authority SHA256: `ae45df6153e6d504c475dc931d898817f5e51f0249f8150fd8b9a51a5c10db6a`

## Existing ownership stack

- Function-x owner SHA256: `5d78aab364ca504dab04225fbed78c91a2b8149263e3f191910af8eb3242a5f4`
- Existing lexical shadow owner SHA256: `b302109d03f5d30421e8e11301744621723af568ab83d0834fe28a0b5f0de2de`
- Existing lexical shadow scope: `9129–9344`

## First newly encountered n declaration

- Discovery kind: `DIRECT_N_BINDING`
- Declaration kind: `const`
- Declaration keyword coordinate: `9147`
- Binding n coordinate: `9186`
- Enclosing scope open: `9129`
- Context window: `9129–9286`
- Context SHA256: `807d90f74440387c1a8ae9ac25ef7c7bff641f159b9e6ecb325736e36e4cafd9`

## Binding semantics

- Binding relation: `SAME_SCOPE_LEXICAL_N_REDECLARATION_FRONTIER`
- Owner effect: `REDECLARATION_REQUIRES_DEDICATED_SOURCE_SEMANTIC_PROOF`
- Qualified owner kind: `LEXICAL_N_BINDING`
- Qualified owner SHA256: `UNRESOLVED`
- Scope kind: `EXISTING_SHADOW_SCOPE`
- Scope close proven: `true`
- Scope close: `9344`
- Binding authority SHA256: `c3e8a310f6e93e72dff65bc38092520f5e1a2c67024c782251d84d336b8ef7fe`

## Frozen frontier

- Stop kind: `SAME_SCOPE_LEXICAL_N_REDECLARATION`

No source beyond this newly discovered binding frontier was qualified.

## Canonical evidence SHA256

`3a75947747c99ee0da960bd1fe16a99bfc9b8faeb3fe26cac688537e0c395b07`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Reproduction of first new n declaration: `AUTHORIZED AND PERFORMED`
- Declaration-kind classification: `AUTHORIZED AND PERFORMED`
- Enclosing-scope characterization: `AUTHORIZED AND PERFORMED`
- Reference scan after the new binding: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Audit the same-scope lexical n redeclaration at coordinate 9186 before any farther scan; do not create a second owner without proving the source semantics.
