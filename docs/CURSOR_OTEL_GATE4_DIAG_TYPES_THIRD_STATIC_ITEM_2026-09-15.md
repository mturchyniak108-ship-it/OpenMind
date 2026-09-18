# Cursor OTEL Gate-4 diag types third static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 3
- Body end reached: YES
- Fourth item classified: NO
- Source executed: NO
- Parent diag.js advanced: NO
- OTEL authority mutated: NO

## Third static item

- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Boundary kind: `BODY_END`
- Declaration prefix: `None`
- Binding: `None`
- Dependency module: `None`
- Initializer present: `None`
- Body offsets: 19:208
- Terminator offset: None
- Source SHA256: `be801bd5e6688f2cf80791f06de520a97ee5bcfe8853f896f1d7e6219fe6accb`
- Canonical row SHA256: `32a021524e3d3a1e693ab2d6aed1d3bfbb136d5947a744a913155f1340b5b499`
- Source: `n.d(t,{u:()=>r}),function(e){e[e.NONE=0]="NONE",e[e.ERROR=30]="ERROR",e[e.WARN=50]="WARN",e[e.INFO=60]="INFO",e[e.DEBUG=70]="DEBUG",e[e.VERBOSE=80]="VERBOSE",e[e.ALL=9999]="ALL"}(r||(r={}))`

## Evidence

Evidence SHA256: `52cfc61de760d8ded674a41c55b6bda935182f5adb31a92f7e7a23b564dbbf4c`

```json
{"authorization_commit":"7f938ecee1f9eb6fb307d0ad9156c15adeafdd26","authorization_contract_sha256":"bca89a05031664ed58aaee78b72cf500483aa12154e673097f846d091b0e1573","authorization_document_sha256":"a462e7ad3674c0584cc9ac3d032cb5842ec7496bfacb91df47c72c0b8e44e51c","authorization_evidence_sha256":"2cc4f113081f3aed7c354521b88d119eb535c1261ecec0dc92b4ff51208ccb13","body_chars":208,"body_end_reached":true,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","classification_count_this_gate":1,"corrected_row2_sha256":"785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c","cumulative_classified_rows":3,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","fourth_item_classified":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_executed":false,"third_item":{"binding":null,"body_end_reached":true,"boundary_kind":"BODY_END","declaration_prefix":null,"dependency_module":null,"end":208,"initializer_present":null,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","ordinal":3,"source":"n.d(t,{u:()=>r}),function(e){e[e.NONE=0]=\"NONE\",e[e.ERROR=30]=\"ERROR\",e[e.WARN=50]=\"WARN\",e[e.INFO=60]=\"INFO\",e[e.DEBUG=70]=\"DEBUG\",e[e.VERBOSE=80]=\"VERBOSE\",e[e.ALL=9999]=\"ALL\"}(r||(r={}))","source_sha256":"be801bd5e6688f2cf80791f06de520a97ee5bcfe8853f896f1d7e6219fe6accb","start":19,"terminator":null},"third_item_sha256":"32a021524e3d3a1e693ab2d6aed1d3bfbb136d5947a744a913155f1340b5b499","version":"GATE4_DIAG_TYPES_THIRD_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one third static item was classified after the corrected row-2 boundary. No fourth item was recovered or classified. No JavaScript was executed. The parent diag.js frontier and OTEL authority were not advanced or mutated.
