# Cursor / OTEL Gate 4 — proto3 recursive ownership super batch — Gold Standard V2

## Source authority

- Source HEAD: `1d53397a419289e63b13ddb69561c98cfbed19b2`
- Source tree: `e204e89c01bb5cf308a395367a80f5cba382e4a6`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_D_COMPLETION_RECURSIVE_MODULE_BATCH_GSV2_2026-09-16.md`
- Prior document SHA256: `9d1a43dd250aa0c663ee77ce775148e29a866c43e02f0b171c87db4c291fade3`
- Prior evidence SHA256: `563b3800c217e6e1adbabf5ed88f9e798a8fbe3c2ea6ddef01cf180f0040d94e`
- Prior frontier: `FUNCTION_PARAMETER_N_BINDING @ 9023`

## Starting frontier qualification

- Function: `x`
- Signature: `function x(e,t,n){`
- Signature SHA256: `290969de010f20f335d15d56a998b672deb6728fb237c1ead6314175bdd59aa1`
- Parameter n coordinate: `9023`
- Parameter n index: `2`

## Webpack-header authority

- Owner kind: `WEBPACK_HEADER_BINDING`
- Owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Token-13 classification: `WEBPACK_HEADER_PROPERTY_ACCESS`
- Token-13 window SHA256: `b5062e37b5676c6fcf03c6b2fe648ac835b036e777f2eeccac8caee6a598a0e2`

Committed restoration authority reused:

- `docs/CURSOR_OTEL_GATE4_PROTO3_WEBPACK_HEADER_N_RESTORATION_Q_RECURSIVE_BATCH_GSV2_2026-09-16.md`

## Recursive super-batch

- Transition ceiling: `64`
- Transitions completed: `1`
- Functions completed: `0`
- Function-local n bindings qualified: `1`
- Webpack owner restorations: `0`

## Function-local n owners

- `x.n@9023`
  - parameter index: `2`
  - owner SHA256: `5d78aab364ca504dab04225fbed78c91a2b8149263e3f191910af8eb3242a5f4`

## Owner restorations

- No local owner restoration was required before the stop frontier.

## Completed functions

- No function completed before the frozen frontier.

## Qualified n references

- None qualified before the frozen stop.

## Current frontier

- Function: `x`
- Function start: `9008`
- Signature: `function x(e,t,n){`
- Signature SHA256: `290969de010f20f335d15d56a998b672deb6728fb237c1ead6314175bdd59aa1`
- Frontier owner kind: `FUNCTION_PARAMETER`
- Frontier owner SHA256: `5d78aab364ca504dab04225fbed78c91a2b8149263e3f191910af8eb3242a5f4`

## Frozen stop frontier

- Stop kind: `UNSUPPORTED_DESTRUCTURING_DECLARATION`
- Stop coordinate: `9152`
- Stop detail: `const`
- Stop window: `9072–9233`
- Stop-window SHA256: `cd2a51c2f6579dd5e4ce044fc146a712f3744e79313462143627dc3354456e87`
- Qualified n references: `0`
- Property-name n tokens excluded: `0`
- Completed template regions: `0`

No semantic qualification was performed beyond the frozen stop frontier.

## Proto3 identity

- Record SHA256: `fdd6e029c7990fa35cf52ab0b0f3eb0b347d95d74d6105c831dd8ce8650dd56d`
- Record end semantics: `END_EXCLUSIVE`
- Body offset inside record: `111`
- Body chars: `28454`
- Body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Simple function parameter-n owner qualification: `AUTHORIZED AND PERFORMED`
- Recursive body scanning: `AUTHORIZED AND PERFORMED`
- Function completion freezing: `AUTHORIZED AND PERFORMED`
- Webpack-header owner restoration: `AUTHORIZED AND PERFORMED`
- Dependency traversal after require-like call: `NOT PERFORMED`
- Exact-path staging and commit: `AUTHORIZED AND PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Canonical evidence SHA256

`b707aae625e7e26eddbcbcd93e1bfcdd7fbadc74118e699d523a3013c9e9c28c`

## Next eligible step

Resolve only the frozen UNSUPPORTED_DESTRUCTURING_DECLARATION frontier inside function x at coordinate 9152 under owner FUNCTION_PARAMETER.
