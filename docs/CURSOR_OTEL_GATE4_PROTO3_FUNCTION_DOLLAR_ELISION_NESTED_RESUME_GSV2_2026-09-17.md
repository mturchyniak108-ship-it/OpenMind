# Cursor / OTEL Gate 4 — proto3 function dollar elision nested resume — Gold Standard V2

## Adopted diagnostic authority

- Source HEAD: `c5ada35f3f937f1125441118af118dcb6ce1dddc`
- Diagnostic document SHA256: `5390ec99aaa09d11cd067564ac2b4bd0610f5897c57b71eb541a873fceb8be18`
- Diagnostic authority SHA256: `bd711d64e154c2cb75b758ba7ae777d4a166a4b66fcd946c1086ac72ccafdfef`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## Exact elision pattern

- Source: `let[,s]`
- Keyword coordinate: `17042`
- Pattern start: `17045`
- Pattern close: `17048`
- Bound names: `["s"]`
- Binds n: `false`
- Elision authority SHA256: `c79b0f537ac714cf1d4387a0bac31f152eae17903a553d767951508be82d13e5`

## Nested anonymous function

- Start: `16970`
- Close: `17101`
- Body SHA256: `9ffaa8aa2a5e97343585ccb93b299413295baa8d6dd3ccc15e4831fa3905dcb6`
- Parameter-n owner SHA256: `fa82288792e92d089ece49d2b6ba1260267591dfaf0dbc6cec893b1db8caa8da`
- Parameter-n references: `[17014]`
- Parameter authority SHA256: `3f5b77648b49bc1579a34f468f565cd6adf093f687a96fc913082dcd00e4e6d3`
- Completion authority SHA256: `b57347c8727fedf855847788a3e0400d3c708fc14bd783b14c03f1e13d03f487`

## Function dollar resumed state

- Start: `16793`
- Close: `17369`
- Parameter-n owner SHA256: `98631248dcd12fcd1269cadd639c23f3b36734f6d32e0acbef3d81e5bfdf1a16`
- Parameter-n references through frontier: `[17103, 17139, 17158, 17242, 17258]`
- Parameter authority SHA256: `9865e9246e5d586619b63106c1587c582520241c6fe447128d960361ac01782c`
- Completion authority SHA256: `NOT_COMPLETE`

## Frozen frontier

- Stop kind: `FUNCTION_DOLLAR_NEW_DESTRUCTURING_FRONTIER`
- Stop coordinate: `17330`
- Frontier owner kind: `FUNCTION_DOLLAR_PARAMETER_N_BINDING`
- Frontier owner SHA256: `98631248dcd12fcd1269cadd639c23f3b36734f6d32e0acbef3d81e5bfdf1a16`
- Stop-window SHA256: `2ca78963909a4eb2594d42850a78fb8515aef8ebb0b0498befcfbbcbddd942d4`
- Frontier-source SHA256: `3012879d7af0cb739f3f2be99ccd1948e54f5e19f4f7cbb6a05d84adcb88c8d3`
- Frontier source JSON: `"[r,i]of Object.entries(t))z(n,s,e,r,i)}}function z(e,t,n,s,i){e.tag(n.no,O.LengthDelimited),e.fork();let o=s;switch(n.K){case l.INT32:case l.FIXED32:case l.UINT32:case l.SFIXED32:case l.SINT32:o=Number.parseInt(s);break;case l.BOOL:(0,r.vA)"`

## Batch authority

- Batch authority SHA256: `9fea9deba104b0b88942b126ea05d277bbfc2210cdbdf656d3c6fe83fcb37004`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`f80a4619abf9d145c295aea2cf7da9bb92624cdaef95f8be65ba7ee5235a16ae`

## Authorization boundary

- Exact diagnostic replay: `AUTHORIZED AND PERFORMED`
- Exact let array elision: `AUTHORIZED AND PERFORMED`
- Pattern n binding: `NONE`
- Nested function completion: `AUTHORIZED AND PERFORMED`
- Function-dollar resume: `AUTHORIZED TO NEXT PROVEN FRONTIER`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resolve only the frozen FUNCTION_DOLLAR_NEW_DESTRUCTURING_FRONTIER at proto3 body coordinate 17330 under function-dollar parameter-n owner 98631248dcd12fcd1269cadd639c23f3b36734f6d32e0acbef3d81e5bfdf1a16.
