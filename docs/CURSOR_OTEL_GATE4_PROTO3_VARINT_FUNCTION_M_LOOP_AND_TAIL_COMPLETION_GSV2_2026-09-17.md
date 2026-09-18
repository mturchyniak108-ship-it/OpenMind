# Cursor / OTEL Gate 4 — varint function m loop and tail completion — Gold Standard V2

## Source authority

- Source HEAD: `97209cdebe82daea50a5733fbe1c290dc7c3dcf3`
- Child body SHA256: `3a783b63472c069fef7a31224cdb25e79db2df4e2241a4438feddf6a205b9038`
- Child webpack owner SHA256: `f1acfdf38ae1bff96f2b950296378388edeb04e57ec954e189bd5f299352578c`
- Prior macro authority SHA256: `0d9d589bbe9997d559b5538762e9d0ab33cc242cc4c5a7410f802bfd5335486a`

## Function m for-loop lexical n

- Function start: `1575`
- Function close: `1706`
- Signature SHA256: `a90bb9e02d203ece3a0ebf4138a07bd024bbe569c9d051567348a178194dce3b`
- for start: `1652`
- for header range: `1655–1671`
- n binding coordinate: `1660`
- Loop body kind: `SINGLE_STATEMENT`
- Loop body range: `1672–1695`
- Lexical scope end: `1696`
- Loop n references: `[1664, 1668]`
- Loop owner SHA256: `13a1ffb5568aa39f696b9e8c5818934b0e929d6132bd0f9f49ac9e5e6775db59`

## Function m completion

- Pre-loop outer n references: `[]`
- Post-loop outer n references: `[]`
- Function-m completion authority SHA256: `6e502123b275be8b0c4dddcfa463b47b4a0e7d2e604c3f143ec44daee3b1ccee`
- Webpack restore coordinate: `1707`

## Tail scan

- Completed tail functions: `p`
- Tail function count: `1`
- Stop kind: `CHILD_MODULE_COMPLETE`
- Stop coordinate: `2196`
- Frontier name: `NONE`
- Stop-window SHA256: `fe8edcc12b12410dccb44547c1ec9b130f23d6edf69a8931dd4a1309b948da45`
- Frontier-source SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Frontier source JSON: `""`

## Child completion and parent return

- Child completion authority SHA256: `d4874df645c0750c444546c15698d15ae662030595d430a4f477f298f8f4aa72`
- Parent return state: `READY`
- Proto3 resume coordinate: `10799`

No ownership was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`dcf3f8905c46f169d1c2fbaffff6ecc8ecbde9c7452902c93d5ee28062cb1662`

## Authorization boundary

- Function-m for-let n scope qualification: `AUTHORIZED AND PERFORMED`
- Function-m completion: `AUTHORIZED AND PERFORMED`
- Simple tail-function qualification: `AUTHORIZED WHEN PROVEN`
- Proto3 parent return: `AUTHORIZED ONLY IF CHILD COMPLETION PROVEN`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 static qualification at body coordinate 10799 under its webpack owner using completed varint child authority d4874df645c0750c444546c15698d15ae662030595d430a4f477f298f8f4aa72.
