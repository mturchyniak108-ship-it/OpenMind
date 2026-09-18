# Cursor OTEL Gate-4 diag.js second static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 2
- Third item classified: NO
- Source executed: NO
- OTEL authority mutated: NO

## Frozen authorization

- Authorization commit: `b6a176513afbb697bcca9acedaee343ef5a5cae9`
- Authorization document SHA256: `defd37b6da159ddbec6738a8400e75437535dec2b9101eb2257be8fb70c9603e`
- Authorization contract SHA256: `91157757c99be8ad7f5dce7da2c044e3ea1cd8d80a468b1c0726279a1a54ece3`
- Authorization evidence SHA256: `f4f53e13b1d5ae4743f5c0c0648e4e136c3867828109a0eec9f96b800c59e664`

## Second static item

- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Binding: `None`
- Dependency module: `None`
- Body offsets: 13:29
- Terminator offset: 29
- Source SHA256: `d41aef0a2ccd7c947917b8a8a26effdaa0044282edc64edd4474b510ba829609`
- Canonical row SHA256: `0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da`
- Source: `n.d(t,{K:()=>a})`

## Evidence

Evidence SHA256: `8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b`

```json
{"authorization_commit":"b6a176513afbb697bcca9acedaee343ef5a5cae9","authorization_contract_sha256":"91157757c99be8ad7f5dce7da2c044e3ea1cd8d80a468b1c0726279a1a54ece3","authorization_document_sha256":"defd37b6da159ddbec6738a8400e75437535dec2b9101eb2257be8fb70c9603e","authorization_evidence_sha256":"f4f53e13b1d5ae4743f5c0c0648e4e136c3867828109a0eec9f96b800c59e664","body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","classification_count_this_gate":1,"cumulative_classified_rows":2,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","second_item":{"binding":null,"dependency_module":null,"end":29,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","ordinal":2,"source":"n.d(t,{K:()=>a})","source_sha256":"d41aef0a2ccd7c947917b8a8a26effdaa0044282edc64edd4474b510ba829609","start":13,"terminator":29},"second_item_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da","source_executed":false,"third_item_classified":false,"version":"GATE4_DIAG_SECOND_STATIC_ITEM_V1"}
```

## Strict boundary

Only the second top-level diag.js static item was classified by this gate. No third item was recovered or classified. No JavaScript was executed and no OTEL authority state was mutated.
