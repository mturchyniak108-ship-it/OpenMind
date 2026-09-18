# Cursor / OTEL Gate 4 — proto3 class U skip all n owners and tail — Gold Standard V2

## Source authority

- Source HEAD: `5a956082a97768001f5bdf57c04b31f1371b4e9d`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Proto3 webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## skip ownership

- skip method start: `13459`
- skip method close: `13925`
- skip signature SHA256: `aa803089e39f1bd118665e58fe4ab0150e3b6addb4ddca64c634faa7e999137e`
- Proven n binding count: `3`
- Frozen destructuring pattern coordinate: `13694`
- skip authority SHA256: `4ed2152426d6b251332a0f88ec153e951fb43f5f12e85d7b8beaa9b28e6c0385`

- Binding 1: source=`SIMPLE_IDENTIFIER`, declaration=`let`, coordinate=`13473`
  - scope=`METHOD_BODY_LEXICAL` `13468–13925`
  - owner SHA256=`2e7ebb1f614c4cc505f1375b1cb5e89d581f9b20739715c0ad65cd08db0661e5`
  - n references=`[13914]`
- Binding 2: source=`SIMPLE_IDENTIFIER`, declaration=`let`, coordinate=`13629`
  - scope=`NESTED_BLOCK_LEXICAL` `13493–13868`
  - owner SHA256=`88f6069a470b6fcccd65091a309fd46e009a4c64bb8c70b4a8de9c768f1f82c7`
  - n references=`[13655]`
- Binding 3: source=`ARRAY_DESTRUCTURING`, declaration=`const`, coordinate=`13697`
  - scope=`NESTED_BLOCK_LEXICAL` `13688–13812`
  - owner SHA256=`eeebf2b49ca14eabd1962d4d6d0bfafb9ab030e96157230ccc3b76a6433618c3`
  - n references=`[13714, 13808]`

## Class U tail

- Transition ceiling: `64`
- Transitions completed: `24`
- Tail methods completed: `15`
- Completed method names: `assertBounds,int32,sint32,int64,uint64,sint64,bool,fixed32,sfixed32,fixed64,sfixed64,float,double,bytes,string`
- Total local n owners in this batch: `4`
- Total owner restorations in this batch: `4`

## Frozen frontier

- Stop kind: `CLASS_U_COMPLETE`
- Stop coordinate: `14817`
- Frontier method: `NONE`
- Stop-window SHA256: `36c1c536f3c451bb103cceea530ce7530bb035c06a1e9abc6a44708a8afe3580`
- Frontier-source SHA256: `4b479b721d21149311ce8bd16d369fe9b105dc7af19cc81e7cfa498b65ebcf95`
- Frontier source JSON: `"}const q=Symbol(\"@bufbuild/protobuf/unknown-fields\"),j={readUnknownFields:!0,readerFactory:e=>new U(e)},G={writeUnknownFields:!0,writerFactory:()=>new M};function H(e,t,n,r,s){let{repeated:i,localName:o}=n;switch(n.oneof&&((e=e[n.oneof.loca"`

## Class completion

- Class completion authority SHA256: `32690f7963c62cf94cf6dbd4280f2250f63822699177ccee9e240488adf631a5`
- Next module coordinate: `14818`

No ownership or dependency traversal was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`5e630a9d99ddbd2dd548075195e2320f15877cdee2255539dafe7996f9320daa`

## Authorization boundary

- All three skip n bindings: `AUTHORIZED AND QUALIFIED ONLY FROM STRUCTURALLY DERIVED LEXICAL SCOPES`
- Innermost-owner reference assignment: `AUTHORIZED AND PERFORMED`
- Exact owner restoration: `AUTHORIZED AND PERFORMED`
- Remaining class-U methods: `AUTHORIZED WHEN THE SAME SCOPE DERIVATION PASSES`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 module qualification at body coordinate 14818 under webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8, using completed class-U authority 32690f7963c62cf94cf6dbd4280f2250f63822699177ccee9e240488adf631a5.
