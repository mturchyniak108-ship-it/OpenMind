# Cursor / OTEL Gate 4 — varint u, c, arrow d, and function m n frontier — Gold Standard V2

## Source authority

- Source HEAD: `c6f0d740b87651dcaca39eb5e78fc32c4921bf36`
- Child body SHA256: `3a783b63472c069fef7a31224cdb25e79db2df4e2241a4438feddf6a205b9038`
- Child webpack owner SHA256: `f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c`
- Prior function-l completion authority SHA256: `4c5e34d3634259efd3a93c6730e9d01232a730519246667d8d13f2d4fb8c99d9`

## Function u completion

- Start: `1423`
- Close: `1460`
- Signature SHA256: `2715502e5546b3c3fce8b4f9c6f0eca25bce08ba5311fcd4d75f02c8e7cdc41d`
- Qualified n references: `[]`
- Completion authority SHA256: `9db018c82c1640d9b36e049610508d8425abbb433719909cf1cd67276f3e74ae`

## Function c completion

- Start: `1461`
- Close: `1509`
- Signature SHA256: `b02074ac6e3b14707583fdd33181a452666556c83dd33e5a7eeaf55002feb473`
- Qualified n references: `[]`
- Completion authority SHA256: `a86c43db5effcf22a26d773a13c1cc27f20317ae34706a8a16391629c18917dd`

## Arrow d completion

- Start: `1510`
- End: `1574`
- Parameter: `e`
- Signature SHA256: `13ad1cdec6a128cdc1fb11b4a0e65b6c5f6f05606c7f33350f71ec0a12d20edf`
- Qualified n references: `[]`
- Arrow authority SHA256: `97b14c78450f5230faa149fcf71d056c34fffa55e32e743026d380bccfe86901`

## Function m frozen ownership frontier

- Function start: `1575`
- Function close: `1706`
- Signature SHA256: `a90bb9e02d203ece3a0ebf4138a07bd024bbe569c9d051567348a178194dce3b`
- Stop kind: `FUNCTION_M_LET_N_BINDING_FRONTIER`
- n declaration kind: `let`
- n binding coordinate: `1660`
- Binding paren depth: `1`
- Binding brace depth: `1`
- Stop-window SHA256: `d5c027c41987f026c428df6e704210ecaa44c21fae28a1ddb99e03ac77d18b6b`
- Frontier-source SHA256: `1755a7438c5552d7afae4feb799fc8cdd676a77bdc498d03c2801724b6520145`
- Frontier source JSON: `"n=0;n<9;n++)t.push(127&e|128),e>>=7;t.push(1)}}function p(){let e=this.buf[this.pos++],t=127&e;if(!(128&e))return this.assertBounds(),t;if(e=this.buf[this.pos++],t|=(127&e)<<7,!(128&e))return this.assertBounds(),t;if(e=this.buf[this.pos++],"`

## Macro authority

- Macro authority SHA256: `0d9d589bbe9997d559b5538762e9d0ab33cc242cc4c5a7410f802bfd5335486a`

No function-m n ownership was inferred beyond the frozen binding frontier.

## Canonical evidence SHA256

`e0e4c5572bd17a8e87a8273098acd07705ec3b246f5741ac6eb67f1474ca1f3d`

## Authorization boundary

- Function-u completion: `AUTHORIZED AND PERFORMED`
- Function-c completion: `AUTHORIZED AND PERFORMED`
- Arrow-d qualification and completion: `AUTHORIZED AND PERFORMED`
- Function-m structural discovery: `AUTHORIZED AND PERFORMED`
- Function-m let-n scope qualification: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify the let n binding in varint function m at child-body coordinate 1660 with its exact for-loop lexical scope, then continue m under restored ownership after that loop.
