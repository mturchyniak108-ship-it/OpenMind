# Cursor / OTEL Gate 4 — proto3 class ne structure and first method boundary — Gold Standard V2

## Source authority

- Source HEAD: `ad88d31a5b74ea88e6e5abed2b2a8996ec397e7a`
- Prior class-frontier authority SHA256: `5c90e7eb080f55acf8305a0aed5758bd5e3765e60d829901d65e303a99c04b25`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## Class ne structure

- Class start: `18496`
- Class body open: `18504`
- Class body close: `19172`
- Class header SHA256: `6987f3c81aa2d846d0736235a32519e5f32c7563600271e15f4826c05cbb53a6`
- Class structure authority SHA256: `8477c94f531bd876da01f4afe37705b96388c4b3f94e75a6ca559c7ab6bbffcb`

## First method boundary

- Method name: `constructor`
- Method start: `18505`
- Parameters: `["e", "t"]`
- Parameter n present: `false`
- Method body open: `18521`
- Method body start: `18522`
- Signature SHA256: `b4b4c2abb1a6768c0ce35368d60c905c1e56b23617d8099cd74f1968155c5905`
- Method boundary authority SHA256: `8a9cae341259e4cf887a5e51a8e9433b09ba116653a1cd276528369855d29dcc`

## Frozen frontier

- Stop kind: `CLASS_NE_CONSTRUCTOR_BODY_FRONTIER`
- Stop coordinate: `18522`
- Frontier owner kind: `CLASS_NE_CONSTRUCTOR_UNQUALIFIED_METHOD_SCOPE`
- Frontier owner SHA256: `8a9cae341259e4cf887a5e51a8e9433b09ba116653a1cd276528369855d29dcc`
- Stop-window SHA256: `9ca060cc1c01cbb2636a5b11e3dbf3897cf608635ce4b4acb10324f36481a7a3`
- Frontier-source SHA256: `1d6d496100ce03a85ac90b3c7412b80f642d081a6a74134b08111fa7b2124f82`
- Frontier source JSON: `"this._fields=e,this._normalizer=t}findJsonName(e){if(!this.jsonNames){const e={};for(const t of this.list())e[t.jsonName]=e[t.name]=t;this.jsonNames=e}return this.jsonNames[e]}find(e){if(!this.numbers){const e={};for(const t of this.list())e[t.no]=t;this.numbe"`

## Batch authority

- Batch authority SHA256: `be60ff2e79af68ba0798966454d7b8e7ba550fbc45a81b36fe2ba3361912ebb9`

The class close was discovered structurally. No class method body was semantically scanned.

## Canonical evidence SHA256

`165add05d66edab8524da468e2c690b05634fe13be173a8acf5c8bc32ffebc29`

## Authorization boundary

- Class-ne structural qualification: `AUTHORIZED AND PERFORMED`
- Constructor header qualification: `AUTHORIZED AND PERFORMED`
- Constructor body semantic qualification: `NOT PERFORMED`
- Later class methods: `NOT ENTERED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify only class-ne constructor body beginning at proto3 body coordinate 18522 with parameters ["e", "t"] and no parameter n; exclude constructor-local n bindings before assigning any bare n token to webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8.
