# Cursor / OTEL Gate 4 — proto3 function X — Gold Standard V2

## Source authority

- Source HEAD: `a22b36045122d5ae588999745e62dbeb1338464b`
- Prior function-K authority SHA256: `596e44928f7c8c50aa2b1e4fe8875123bd7c8e11422465549a06b437d821370c`
- Prior function-Z authority SHA256: `c89fa4a28cec4cbb3b126009e1bd326ab5d663ed3b629f3987ebfe68d4017864`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## Function X

- Start: `18033`
- Close: `18268`
- Signature SHA256: `578152f43786c7e9c0b8c8855905cdc63290d32d5519dca79dd82737d97c2934`
- Parameters: `["e"]`
- Parameter n present: `false`
- Bare n references through frontier: `[]`
- Local n bindings: `[]`
- Non-n destructuring patterns: `[]`
- Webpack reference authority SHA256: `8ac0473a60d0ef45680a9864d91a185d4ffe8a3aa0a095ae69d08fd681663033`
- Completion authority SHA256: `b8a71e4928e868765536df72bc430a33eb42a94df5e7d33e517a3694d7d7396f`

## Frozen frontier

- Stop kind: `FUNCTION_X_COMPLETE_NEXT_MODULE_FRONTIER`
- Stop coordinate: `18269`
- Frontier owner kind: `WEBPACK_HEADER_BINDING`
- Frontier owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Stop-window SHA256: `6fefbfc8bbecfb6698e26e21c88f409481412b12ca6209f3392143ee1de726a1`
- Frontier-source SHA256: `a38128ea62a346f2a8c30fa56966c62d08e7a346b9b55108bacbe8f78d6c1c38`
- Frontier source JSON: `"function ee(e){if(void 0===e)return e;if((0,v.K)(e))return e.clone();if(e instanceof Uint8Array){const t=new Uint8Array(e.byteLength);return t.set(e),t}return e}function te(e){return e instanceof Uint8Array?e:new Uint8Array(e)}class ne{cons"`

## Batch authority

- Batch authority SHA256: `58803b81e4c1e7d6dfb228c74ac6afd9211a156a5ceededc2c9d245235c24ba6`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`8c62130e92274a2cf684c579fa9ed572b2924fc8abb7fc16b81a0da5f8adc111`

## Authorization boundary

- Function-X static qualification: `AUTHORIZED TO NEXT PROVEN FRONTIER`
- Function-X parameter n: `ABSENT`
- Free n ownership: `WEBPACK ONLY AFTER WHOLE-FUNCTION LOCAL-BINDING EXCLUSION`
- Local n binding: `FROZEN BEFORE ASSIGNMENT`
- Nested function/class/catch/arrow: `FROZEN BEFORE OWNERSHIP CHANGE`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 module qualification at body coordinate 18269 under webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8, using completed function-X authority b8a71e4928e868765536df72bc430a33eb42a94df5e7d33e517a3694d7d7396f.
