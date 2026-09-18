# Cursor / OTEL Gate 4 — proto3 function P completion and next region frontier — Gold Standard V2

## Source authority

- Source HEAD: `96f2fedba670f57b7d29df480f2c304fd526a960`
- Source tree: `a9683cee7de28db9b5512e09820a4af10ce63f91`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_P_PARAMETER_BINDING_RECURSIVE_BATCH_GSV2_2026-09-16.md`
- Prior document SHA256: `430f99fea891ea54af238d1a1a47214bcef04ce32fee96cc225a0a1517f10795`
- Prior evidence SHA256: `1cc25934b405f8a2fa93927329a0309990531b63bab2d894f57aad1e4021736f`
- Prior function-P owner SHA256: `67b952f9c1c9d1a0ecb64bfd27166e7d4e1aeb0fc00eb1bdf2ef29e46401b74b`

## Function P completion

- Function start: `8601`
- Signature: `function P(e,t,n,r){`
- Signature SHA256: `fc10d5c2f34c34af3f9cf68e9d5601198aaf1a528d57f62f97e83b11d93af7f9`
- Local `n` origin: `8616`
- Local `n` parameter index: `2`
- Local owner SHA256: `67b952f9c1c9d1a0ecb64bfd27166e7d4e1aeb0fc00eb1bdf2ef29e46401b74b`
- Exact closing delimiter coordinate: `8913`
- Exact closing delimiter: `}`
- Prior stop kind: `FUNCTION_P_SCOPE_END_REACHED`
- Prior stop window: `8843–8984`
- Prior stop-window SHA256: `31be69f676bdad5ff9e2e41e412115557386592404cfddc92c4d10054190cc8e`
- Function-P completion authority SHA256: `f50237f1490b9c825de04179f9803c8affb9b9972de30ba39fdc44f423abb501`

Function `P` is complete. Its function-parameter `n` owner ends at coordinate `8913`.

## Restored webpack-header n owner

- Restored owner kind: `WEBPACK_HEADER_BINDING`
- Restored immediately after coordinate: `8913`
- Restored owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Token-13 classification: `WEBPACK_HEADER_PROPERTY_ACCESS`
- Token-13 window SHA256: `b5062e37b5676c6fcf03c6b2fe648ac835b036e777f2eeccac8caee6a598a0e2`
- Restored-owner evidence SHA256: `60ae68400a2e6c5736b9865cf6888890ec02044478cfd8a8ff01085dff8a8f13`

Committed restoration authority reused:

- `docs/CURSOR_OTEL_GATE4_PROTO3_WEBPACK_HEADER_N_RESTORATION_Q_RECURSIVE_BATCH_GSV2_2026-09-16.md`

## Dynamically discovered next region

- Function name: `D`
- Function start: `8914`
- Signature: `function D(e){`
- Signature SHA256: `325dc143549a298c3a62597ed3d6ff7b0a56ccba429c3e3759490f3b903ca542`
- Parameter list open: `8924`
- Parameter list close: `8926`
- Body open: `8927`
- Body start: `8928`

Parameters:

- `e` @ `8925–8926` ; index `0`

## New n binding frontier

- New function-parameter `n` binding: `NONE BEFORE FROZEN STOP`

## Qualified webpack-header n references

- None qualified before the frozen stop.

## Non-owner property-name n tokens

- None encountered before the frozen stop.

## Completed template regions

- None completed before the frozen stop.

## Frozen stop frontier

- Stop kind: `DISCOVERED_FUNCTION_SCOPE_END_REACHED`
- Stop coordinate: `9007`
- Stop detail: `exact discovered function closing delimiter`
- Stop window: `8937–9078`
- Stop-window SHA256: `f23fbf942c5df12b1944d3a7b5b384d83e74ea3dca1acc1faeee56a93d8db109`
- Next-function body scan performed: `true`
- Qualified webpack-owner references: `0`
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
- Function-P completion freeze: `AUTHORIZED AND PERFORMED`
- Webpack-header owner restoration from committed authority: `AUTHORIZED AND PERFORMED`
- Dynamic next-region discovery: `AUTHORIZED AND PERFORMED`
- Recursive next-function scan only when no parameter-n shadow exists: `AUTHORIZED AND PERFORMED`
- Exact-path staging and commit: `AUTHORIZED AND PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Canonical evidence SHA256

`e2368abeb9e30f1036869ae3e7eab4f900f5c1f9a360e85518721d69f87eea63`

## Next eligible step

Freeze completion of function D at coordinate 9007, restore the webpack-header n owner, and discover the following module-level region.
