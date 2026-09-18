# Cursor / OTEL Gate 4 — proto3 function H local n owners recursive qualification — Gold Standard V2

## Source authority

- Source HEAD: `edde7a2adf1ec4ec473f9dad69b53c959f75dfa3`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Function H signature SHA256: `aea24cf2f04b14a9e9b5c19c2826e1e36db473e38c4d369003f471fc0a45adf7`
- Function H parameter-n owner SHA256: `7278c1a3bf7a4141daa1c0114ab269a6686a9df8edc9ba1ec2dfeff58baf23d8`

## Parameter owner continuity

- Parameter n coordinate: `14986`
- Previously qualified references: `[15021, 15030, 15045, 15109, 15157, 15172, 15197, 15205]`
- Parameter references through this batch: `[15021, 15030, 15045, 15109, 15157, 15172, 15197, 15205, 15399, 15427, 15456, 15477, 15497, 15506]`

## Local n owners

- Proven local lexical owner count: `1`
- var-n redeclaration count: `0`
- Current frontier binding coordinate: `15225`
- Current frontier owner SHA256: `1b0369783297f83177c02a3f637cad02a80affc902d76e1b4b60042e1a1712ff`
- Current frontier owner authority SHA256: `c191f31753147053b7f3701a5c8e80457478be68d9feefad41a999bca2727670`

- Owner 1 source: `SIMPLE_IDENTIFIER`
  - declaration: `let`
  - binding coordinate: `15225`
  - lexical scope: `15220–15353`
  - owner SHA256: `1b0369783297f83177c02a3f637cad02a80affc902d76e1b4b60042e1a1712ff`
  - owner authority SHA256: `c191f31753147053b7f3701a5c8e80457478be68d9feefad41a999bca2727670`
  - n references: `[15319, 15339]`
  - restore coordinate: `15354`

## Function H completion state

- Function-H completion authority SHA256: `NOT_COMPLETE`
- Frozen stop kind: `FUNCTION_H_NESTED_FUNCTION_OWNERSHIP_BOUNDARY`
- Frozen stop coordinate: `15584`
- Frontier owner kind: `FUNCTION_H_PARAMETER_N_BINDING`
- Frontier owner SHA256: `7278c1a3bf7a4141daa1c0114ab269a6686a9df8edc9ba1ec2dfeff58baf23d8`
- Stop-window SHA256: `3fa69be86dc4d3438f79f8165f7c3a3e28d484f78c038a9609602c6136fe5f1d`
- Frontier-source SHA256: `d2300307d81725ee59b9299af0d3f90f5b7b324ba55f043e6768daed32491e0a`
- Frontier source JSON: `"function(e,t,n){const r=t.uint32(),s=t.pos+r;let i,o;for(;t.pos<s;){const[r]=t.tag();switch(r){case 1:i=W(t,e.K);break;case 2:switch(e.V.kind){case\"scalar\":o=W(t,e.V.T);break;case\"enum\":o=t.int32();break;case\"message\":o=Y(t,new e.V.T,n,void"`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`1210955fc7b7990300f37540a2dbec701b5e0d2a1e6cc363f79e515b17dae5bb`

## Authorization boundary

- Function-H parameter owner replay: `AUTHORIZED AND PERFORMED`
- Function-H local lexical n scope qualification: `AUTHORIZED AND PERFORMED WHEN STRUCTURALLY PROVEN`
- Innermost lexical-owner reference assignment: `AUTHORIZED AND PERFORMED`
- Function-H owner restoration: `AUTHORIZED AND PERFORMED WHEN PROVEN`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resolve only the frozen FUNCTION_H_NESTED_FUNCTION_OWNERSHIP_BOUNDARY at proto3 body coordinate 15584 under active owner 7278c1a3bf7a4141daa1c0114ab269a6686a9df8edc9ba1ec2dfeff58baf23d8.
