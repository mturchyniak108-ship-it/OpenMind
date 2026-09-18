# Cursor / OTEL Gate 4 — proto3 functions K and Z — Gold Standard V2

## Source authority

- Source HEAD: `da81d40ea1961ee78b93c8b44c9e7e33b5fe6b5b`
- Prior function-z authority SHA256: `0f4848271663a96e6274aea9dbcd60b641dee0fa283566011bea9695eba40dba`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## Function K

- Start: `17796`
- Close: `17960`
- Signature SHA256: `db9f47e48162b17b2700f947ca6971f4092bf01f7dce14b839031379fd19caee`
- Parameters: `["e", "t", "n", "r"]`
- Parameter-n owner SHA256: `b8ba3e1ede4e0ebd96d609b86e3f29d2c00f8ff0190730a6a55df522552978cc`
- Parameter-n references: `[17826, 17833, 17851, 17893, 17916]`
- Parameter authority SHA256: `99ad27c376e30440c265c521ce1b0a0431c0ff928cd9cddaa8aab8787ec7a060`
- Completion authority SHA256: `596e44928f7c8c50aa2b1e4fe8875123bd7c8e11422465549a06b437d821370c`

## Function Z

- Start: `17961`
- Close: `18032`
- Signature SHA256: `ac5936ea7394f1e83b2c18b06ce856366f017d1d1d31e88f3bfb8f0abd635fdf`
- Parameters: `["e", "t", "n", "s"]`
- Parameter-n owner SHA256: `7d17cef02368e3bd4f8f14871469f92fa30aeb02e65421c52e7eca1965c1e233`
- Parameter-n references through frontier: `[18022]`
- Non-n destructuring patterns: `[{"declaration_kind": "let", "keyword_coordinate": 18002, "pattern_start": 18005, "pattern_close": 18009, "names": ["i", "o"], "coords": [18006, 18008], "entries": [{"kind": "IDENTIFIER", "name": "i", "coordinate": 18006}, {"kind": "IDENTIFIER", "name": "o", "coordinate": 18008}], "paren_depth": 0, "bracket_depth": 0, "block_depth": 0}]`
- Parameter authority SHA256: `239d125fd90659bc98446906a81606190f3b73b00dd9b83851736645878e35d4`
- Completion authority SHA256: `c89fa4a28cec4cbb3b126009e1bd326ab5d663ed3b629f3987ebfe68d4017864`

## Frozen frontier

- Stop kind: `FUNCTION_CAPITAL_Z_COMPLETE_NEXT_MODULE_FRONTIER`
- Stop coordinate: `18033`
- Frontier owner kind: `WEBPACK_HEADER_BINDING`
- Frontier owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Stop-window SHA256: `682cf266d501d6ae497a834fd051ac9a9b1c3bf5bbd9a0e925cc5e682a1e059e`
- Frontier-source SHA256: `c7dd1d66b9596045739485d0ae354593f4c270b9252b7a162468a0980ffc932d`
- Frontier source JSON: `"function X(e){let t=O.Varint;switch(e){case l.BYTES:case l.STRING:t=O.LengthDelimited;break;case l.DOUBLE:case l.FIXED64:case l.SFIXED64:t=O.Bit64;break;case l.FIXED32:case l.SFIXED32:case l.FLOAT:t=O.Bit32}return[t,l[e].toLowerCase()]}func"`

## Batch authority

- Batch authority SHA256: `e7d03588085115855c39bc832590db130bc060c73d7b53acac2f139fb149e05a`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`458a3ca3abb5a7081b4071f37ead5ea5f57657cf0db1aab4013ec1f93a595aef`

## Authorization boundary

- Function K static qualification: `AUTHORIZED AND PERFORMED`
- Function Z static qualification: `AUTHORIZED TO NEXT PROVEN FRONTIER`
- Parameter-n ownership: `AUTHORIZED WHEN STRUCTURALLY PROVEN`
- Non-n simple destructuring: `AUTHORIZED AND RECORDED`
- n destructuring or lexical shadow: `FROZEN BEFORE OWNERSHIP CHANGE`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 module qualification at body coordinate 18033 under webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8, using completed function-K authority 596e44928f7c8c50aa2b1e4fe8875123bd7c8e11422465549a06b437d821370c and completed function-Z authority c89fa4a28cec4cbb3b126009e1bd326ab5d663ed3b629f3987ebfe68d4017864.
