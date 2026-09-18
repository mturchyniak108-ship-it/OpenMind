# Cursor / OTEL Gate 4 — varint function l nested helper and lexical n completion — Gold Standard V2

## Source authority

- Source HEAD: `a33dd40a937167b2cc345071a580df0629af3235`
- Child body SHA256: `3a783b63472c069fef7a31224cdb25e79db2df4e2241a4438feddf6a205b9038`
- Child webpack owner SHA256: `f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c`
- Prior function-a completion authority SHA256: `761babb6a734ec1085d226d14a55bedce56061cbaa3722e39bc06124f8e3aff5`

## Function l

- Function start: `1102`
- Function close: `1422`
- Signature SHA256: `a6a330917c6007c0433d67f2b6ea741266a51a40760b092bb20067480a1116b2`
- n declaration kind: `const`
- n declaration coordinate: `1213`
- n binding coordinate: `1219`
- TDZ ownership from function-body entry: `true`
- Function-l owner SHA256: `48b4b0b37724195043a45280124a0dee9f8d837fd8f288b81433c26973294e5f`
- Outer n references: `[1285, 1299]`
- Function-l owner authority SHA256: `b7fd4917ecaeaf43b5a12a9b090a3ba13d1014552f8f742f7c43057318ff7a8c`

## Nested anonymous helper

- Nested start: `1134`
- Nested close: `1173`
- Parameters: `["e", "t"]`
- Signature SHA256: `dd9095817569527296ba308d6fdc92b851bb60554591c14aea5368ae8195d2b4`
- Local n parameter: `false`
- Local n declaration: `false`
- Captured n references: `[]`
- Capture owner SHA256: `48b4b0b37724195043a45280124a0dee9f8d837fd8f288b81433c26973294e5f`
- Nested capture authority SHA256: `2e7f0388bf1e7e2397601d863ac1eb62a11dc03eeb7cc7a683fcc05c49e8013e`

## Function l completion

- Completion authority SHA256: `4c5e34d3634259efd3a93c6730e9d01232a730519246667d8d13f2d4fb8c99d9`
- Webpack restore coordinate: `1423`
- Restored webpack owner SHA256: `f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c`

## Next function frontier

- Next function name: `u`
- Next function start: `1423`
- Next signature SHA256: `2715502e5546b3c3fce8b4f9c6f0eca25bce08ba5311fcd4d75f02c8e7cdc41d`
- Stop kind: `NEXT_FUNCTION_SIMPLE_COMPLETION_ELIGIBLE`
- Stop coordinate: `1460`
- Stop-window SHA256: `4969a7c5c5e743ab8fbed0f227e285d276d077dadf740e9e4ad0ee9dfdb395be`
- Frontier-source SHA256: `931bb291eeeacb311369277fa1586041bdc4b71817b4f97f55a2d75633012d9d`
- Frontier source JSON: `"}function c(e,t){return t=~t,e?e=1+~e:t+=1,u(e,t)}const d=e=>{const t=String(e);return\"0000000\".slice(t.length)+t};function m(e,t){if(e>=0){for(;e>127;)t.push(127&e|128),e>>>=7;t.push(e)}else{for(let n=0;n<9;n++)t.push(127&e|128),e>>=7;t.pu"`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`d9a4ccbce34af9163e0170bb9e84b256060c2ddc4938da29ee0a6557d681763f`

## Authorization boundary

- Nested anonymous helper classification: `AUTHORIZED AND PERFORMED`
- Function-l body lexical n qualification: `AUTHORIZED AND PERFORMED`
- Nested capture qualification: `AUTHORIZED AND PERFORMED`
- Function-l completion: `AUTHORIZED AND PERFORMED`
- Child webpack owner restoration: `AUTHORIZED AND PERFORMED`
- Qualification beyond next frontier: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resolve the frozen NEXT_FUNCTION_SIMPLE_COMPLETION_ELIGIBLE in varint function u at child-body coordinate 1460, preserving completed function-l authority 4c5e34d3634259efd3a93c6730e9d01232a730519246667d8d13f2d4fb8c99d9.
