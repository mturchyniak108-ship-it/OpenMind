# Cursor / OTEL Gate 4 — proto3 function N completion and next function binding frontier — Gold Standard V2

## Qualification state

- Source HEAD: `ede59c1ec9f308e5cf5ce60f9b497b4f7e2b7481`
- Source tree: `3d34ed6c02aeb463e590e6954db213df7bc18cef`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_N_PARAMETER_BINDING_RECURSIVE_BATCH_GSV2_2026-09-16.md`
- Prior document SHA256: `f7a2696d428551886f44ba3fbe4596191da5473d30f1d974ef081f797f80ed6f`
- Prior authority SHA256: `be5506e2486f4119cf345c34f5b21b2f90f415a96252eace5cfe1a61fe4cb805`
- Prior evidence SHA256: `3766c7e1b058f077b0e8fff191f9cc80443a1ed1d71c20bef872acfdf07ed037`

## Function N completion

- Function start: `7366`
- Signature: `function N(e,t,n,s){`
- Signature SHA256: `fada0f439f1b8aa390e6b746cee7ba22469b6b2f02bbfc77355dfc14f8cc5c77`
- Local parameter `n` origin: `7381`
- Local owner SHA256: `bee66a40a7d4e4996419e207c008bcbbb24005b6799902edd2a8eefba0662b47`
- Previously qualified references: `7411, 8183, 8306`
- Exact closing delimiter coordinate: `8600`
- Exact closing delimiter: `}`
- Frozen stop kind: `FUNCTION_N_SCOPE_END_REACHED`
- Frozen stop window: `8530–8670`
- Frozen stop-window SHA256: `120dbbd9b981d2cb87c2e44ea8499b2d588517e8f36efc6a7b9ba970b869ca5e`
- Function N completion authority SHA256: `123f635211a51982c049d3677a59e9650f26c7bef31b41dc1e840acf75f06b33`

Function `N` is complete at coordinate `8600`. Its function-parameter `n` owner ends at that delimiter.

## Restored webpack-header n owner

- Restored owner kind: `WEBPACK_HEADER_BINDING`
- Restored owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Token-13 classification: `WEBPACK_HEADER_PROPERTY_ACCESS`
- Token-13 window SHA256: `b5062e37b5676c6fcf03c6b2fe648ac835b036e777f2eeccac8caee6a598a0e2`
- Restored-owner evidence SHA256: `4d18ad8239a3df69c8a203a16e94e834293f8d059328f1d8612cfc05f6fb4b72`

Committed restoration authority reused:

- `docs/CURSOR_OTEL_GATE4_PROTO3_WEBPACK_HEADER_N_RESTORATION_Q_RECURSIVE_BATCH_GSV2_2026-09-16.md`

No token-13 declaration reinterpretation was performed. The committed property-access correction remains authoritative.

## Dynamically discovered next module-level function

- Function name: `P`
- Function start: `8601`
- Signature: `function P(e,t,n,r){`
- Signature SHA256: `fc10d5c2f34c34af3f9cf68e9d5601198aaf1a528d57f62f97e83b11d93af7f9`
- Parameter list open: `8611`
- Parameter list close: `8619`
- Body open: `8620`
- Body start: `8621`

Parameters:

- e @ 8612–8613 ; index 0
- t @ 8614–8615 ; index 1
- n @ 8616–8617 ; index 2
- r @ 8618–8619 ; index 3

## New binding frontier

- Stop kind: `FUNCTION_PARAMETER_N_BINDING`
- New local `n` coordinate: `8616`
- New local `n` end: `8617`
- New local `n` parameter index: `2`
- Binding kind: `FUNCTION_PARAMETER`
- Binding authority SHA256: `116210df9671555d7cd274c1ef36d1fd65fd1a440c1eb8cb5ad07cc65e40e9a0`
- Function body scanned: `false`

The helper stopped before scanning the new function body. The webpack-header owner is restored only across the module-level interval after function `N` and before entry into this newly discovered parameter scope.

## Proto3 source identity

- Record: `3357553–3386119`
- Record end interpretation: `END_EXCLUSIVE`
- Record SHA256: `fdd6e029c7990fa35cf52ab0b0f3eb0b347d95d74d6105c831dd8ce8650dd56d`
- Body offset inside matched record: `111`
- Body chars: `28454`
- Body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Evidence document creation: `AUTHORIZED AND PERFORMED`
- Exact-path staging: `AUTHORIZED AND PERFORMED`
- Exact-path commit: `AUTHORIZED AND PERFORMED`
- New function body scan: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Canonical evidence SHA256

`8f64550a13cabb3d8c7b1e7e98de3f3256a69713e2cc4c5cc8b02e2ed452b8ad`

## Next eligible step

Qualify the newly frozen function-parameter `n` owner and recursively scan only that function body, stopping at the first unresolved semantic boundary.
