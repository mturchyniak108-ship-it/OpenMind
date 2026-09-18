# Cursor / OTEL Gate 4 — proto3 class M sfixed64 and tail recursive qualification — Gold Standard V2

## Source authority

- Source HEAD: `fcda7cb076d666dcfd8d247c69004e7c3620e74c`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Proto3 webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## Corrected sfixed64 frontier

- Prior frozen coordinate: `12645`
- Correct classification: `BODY_LEVEL_LET_N_BINDING_TOKEN`
- Binding coordinate equals prior frontier: `true`
- Binding counted as reference: `false`
- Method start: `12609`
- Method close: `12745`
- Signature SHA256: `c63252d125b51e0b460dc1c6e9b32982a80a059ecc474eee5ab77d2a89cba142`
- n binding kind: `let`
- n binding coordinate: `12645`
- Qualified n references: `[12690, 12712]`
- Owner SHA256: `83a41e4aa77f8eaebae99ff3e2e9cf8414df056ee15b6f5460cad46614683fd9`
- sfixed64 completion authority SHA256: `361f3370a263d0e20cbd024d3a0d18cc1ec1afadeaac87104e3396720a5a9818`

## Class M tail

- Transition ceiling: `64`
- Transitions completed: `11`
- Methods completed in this batch: `5`
- Completed method names: `sfixed64,fixed64,int64,sint64,uint64`
- Local n owners proven: `3`
- Owner restorations: `3`

## Frozen frontier

- Stop kind: `CLASS_M_COMPLETE`
- Stop coordinate: `13125`
- Frontier method: `NONE`
- Stop-window SHA256: `20c2ae077adc57790992bd73433ea847cd6512d52d03847c3cb3d0a1a71bcefa`
- Frontier-source SHA256: `e9262b86474f728e9e9741c14b104adf4da12454ad10858d83f31170054e9d4f`
- Frontier source JSON: `"}class U{constructor(e,t){this.varint64=F.ls,this.uint32=F.Gn,this.buf=e,this.len=e.length,this.pos=0,this.view=new DataView(e.buffer,e.byteOffset,e.byteLength),this.textDecoder=null!=t?t:new TextDecoder}tag(){let e=this.uint32(),t=e>>>3,n="`

## Class completion

- Class completion authority SHA256: `d02ca92a128d8c34d72e5af322b437c1031bad4926bc447be12658dbf8a6e247`
- Next module coordinate: `13126`

No ownership or dependency traversal was inferred beyond the frozen frontier.

## Canonical evidence SHA256

`45db82b4518ae1d2527f6211a415bd4c5de9b848b5164aa6c0d1ab7bf6078895`

## Authorization boundary

- sfixed64 frontier reclassification: `AUTHORIZED AND PERFORMED`
- sfixed64 body-level let-n qualification: `AUTHORIZED AND PERFORMED`
- Subsequent single body-level let/const n qualification: `AUTHORIZED ONLY WHEN STRUCTURALLY UNAMBIGUOUS`
- Method parameter-n qualification: `AUTHORIZED WHEN STRUCTURALLY UNAMBIGUOUS`
- Nested lexical or dependency ambiguity traversal: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 module qualification at body coordinate 13126 under webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8, using completed class-M authority d02ca92a128d8c34d72e5af322b437c1031bad4926bc447be12658dbf8a6e247.
