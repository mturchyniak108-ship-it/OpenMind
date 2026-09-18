# Cursor / OTEL Gate 4 — varint nested o capture and outer o completion — Gold Standard V2

## Source authority

- Source HEAD: `902c7e1f78466c378f20fc33ffa9b6b98e96b149`
- Child body SHA256: `3a783b63472c069fef7a31224cdb25e79db2df4e2241a4438feddf6a205b9038`
- Child webpack owner SHA256: `f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c`

## Outer function o

- Function start: `775`
- Function close: `990`
- Body lexical n binding: `832`
- Outer n owner SHA256: `c21f44359fae3cb4cf4b1b9a6da2bec0231e58476d6a2331f7c1e0651c437a8f`
- Outer owner authority SHA256: `5756e98147117e4aa7ea09f114fefb1a46e0e19b046db787af623ddb84cdf298`

## Nested function o capture

- Nested function start: `850`
- Nested function close: `929`
- Parameters: `["t", "o"]`
- Local n parameter: `false`
- Local n declaration: `false`
- Capture owner SHA256: `c21f44359fae3cb4cf4b1b9a6da2bec0231e58476d6a2331f7c1e0651c437a8f`
- Captured n references: `[898, 904]`
- Nested capture authority SHA256: `1a7c5d58dc171234e96619432df595d8c99c028744cb34ccebae845321c87408`

## Outer function continuation

- Resume coordinate after nested close: `930`
- Post-nested n references: `[]`
- Post-nested n declarations: `[]`
- Outer function completed: `true`
- Outer completion authority SHA256: `bfdcaa39ed9a3627915c958bdcecdea78fc137ed0fbc0f98108d6163a9569726`

## Frozen frontier

- Stop kind: `OUTER_FUNCTION_O_COMPLETED`
- Stop coordinate: `991`
- Stop-window SHA256: `14cc6024f6953dca39c743c96e08b41a2c1d74337f70c9fec7efad596beb9b0b`
- Next child coordinate: `991`
- Next-source SHA256: `87176e0a483f87d31fce4aa41231ba02955a3d38533b62016f816c29880044a2`
- Next-source JSON: `"function a(e,t){let n=u(e,t);const r=2147483648&n.hi;r&&(n=c(n.lo,n.hi));const s=l(n.lo,n.hi);return r?\"-\"+s:s}function l(e,t){if(({lo:e,hi:t}=function(e,t){return{lo:e>>>0,hi:t>>>0}}(e,t)),t<=2097151)return String(i*t+e);const n=16777215&("`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`64716d167c71de1c11a1a531ecbab9306e755438efa94b3382144c88463d2326`

## Authorization boundary

- Nested function local-n classification: `AUTHORIZED AND PERFORMED`
- Nested captured-n qualification: `AUTHORIZED AND PERFORMED`
- Outer function-o continuation: `AUTHORIZED AND PERFORMED`
- Webpack owner restoration after outer close: `AUTHORIZED WHEN COMPLETION PROVEN`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume varint child module qualification at child-body coordinate 991 under restored webpack owner f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c.
