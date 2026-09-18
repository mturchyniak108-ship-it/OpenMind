# Cursor / OTEL Gate 4 — proto3 class ne byNumber arrow complete and byMember frontier — Gold Standard V2

## Source authority

- Source HEAD: `8cdd410ed0963dc6a0f6b4bcddb7d5fec38e6857`
- Class structure authority SHA256: `8477c94f531bd876da01f4afe37705b96388c4b3f94e75a6ca559c7ab6bbffcb`
- Prior method authority SHA256: `19acff3e2b89ea0412b5280725f329aa458a24963bdf0b1c69e9c908d0e8e115`
- byNumber boundary authority SHA256: `9d1de65774faa658d84fe3764dde6de21d039269bcf8aca6fc89d8211f764158`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## byNumber

- Start: `18885`
- Body start: `18896`
- Close: `18999`
- Parameters: `[]`
- Parameter n present: `false`
- Local n bindings outside nested arrow: `[]`
- Outer bare n references: `[]`
- Method completion authority SHA256: `a9657eef19e19f537e96b4d4b3ff92a4db56a95ff5e592167699edf0d3d264b6`

## Nested arrow

- Parameter open: `18964`
- Parameters: `["e", "t"]`
- Parameter n present: `false`
- Arrow operator coordinate: `18969`
- Expression start: `18971`
- Expression end: `18980`
- Expression SHA256: `c91ae8220e5bff0d68bedc1f02e6455848e91523ef3f493f15864fe25ba7cbe9`
- Bare n references: `[]`
- Arrow owner SHA256: `7ea88f113e1a9c9d31c25f3158222c39d007770af59fcfadc210eb8577080a7a`
- Arrow authority SHA256: `dac5836a3fe7a3362dac76fca412d0135931d7ea52c62a42918812f09abe0881`

## Next method boundary

- Method name: `byMember`
- Method start: `19000`
- Parameters: `[]`
- Method body open: `19010`
- Method body start: `19011`
- Signature SHA256: `3f2e8a23ac770036fa70d880185ca1e80026ec1992a5a7c5d1c46ce290dbec06`
- Boundary authority SHA256: `b30ce25ff62b2efe49617b7a07e0f88c22a0b9dcde249513f33d98a1b7b54146`

## Frozen frontier

- Stop kind: `CLASS_NE_BYMEMBER_BODY_FRONTIER`
- Stop coordinate: `19011`
- Frontier owner kind: `CLASS_NE_BYMEMBER_UNQUALIFIED_METHOD_SCOPE`
- Frontier owner SHA256: `b30ce25ff62b2efe49617b7a07e0f88c22a0b9dcde249513f33d98a1b7b54146`
- Stop-window SHA256: `91ef825ab960d3f707e31a858fb497aeb4d1b80883d3cdcf0c22de68c9a5692b`
- Frontier-source SHA256: `b72a86fabe7117e16c596e1c6441d153bfbfb1c36f699f3f6bb9bde0ac7b7afb`
- Frontier source JSON: `"if(!this.members){this.members=[];const e=this.members;let t;for(const n of this.list())n.oneof?n.oneof!==t&&(t=n.oneof,e.push(t)):e.push(n)}return this.members}"`

## Batch authority

- Prior batch authority SHA256: `d7352cef701a4b8356ae1e2a7f8ba1e52daac334f2ee3be2380495db23be6753`
- Batch authority SHA256: `209d8300365b409c172e214a0d90b6bc0076c9c35d9e9f0ce60272aa8c9cffff`

The byNumber method and its single nested arrow were fully qualified. The byMember body was not entered.

## Canonical evidence SHA256

`4ce2a8afcd6c5ea56f60a7d7904e905ddfefc4b0b0640dac0740a8046f71fca7`

## Authorization boundary

- byNumber semantic qualification: `AUTHORIZED AND PERFORMED`
- Nested arrow qualification: `AUTHORIZED AND PERFORMED`
- byMember header qualification: `AUTHORIZED AND PERFORMED`
- byMember body semantic qualification: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify class-ne byMember method beginning at proto3 body coordinate 19011; freeze its lexical for-of binding n before assigning any n references, because the visible body contains for(const n of this.list()).
