# Cursor OTEL Gate-4 diag types first static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 1
- Second item classified: NO
- Source executed: NO
- Parent diag.js advanced: NO
- OTEL authority mutated: NO

## First static item

- Kind: `DIRECTIVE`
- Boundary kind: `STATEMENT_SEMICOLON`
- Binding: `None`
- Dependency module: `None`
- Body offsets: 0:12
- Terminator offset: 12
- Source SHA256: `4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741`
- Canonical row SHA256: `a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621`
- Source: `"use strict"`

## Evidence

Evidence SHA256: `56a0781ba77df3d2969c926cdb237398fb3e1119ad52c5f0ba4a242891114dee`

```json
{"authorization_commit":"afe4770af318a78d4f1ba30f2230d126b0b0d420","authorization_contract_sha256":"a1c4acc5ed1b3859cf7d3fc856b09fb88e602a7ad77e4307b35a3c180ec730fd","authorization_document_sha256":"5f9b54fa06b0f8ecb74cad1fed10979970b665387a172a0170bb6805d6238ac3","authorization_evidence_sha256":"0bdbd38db0a0edde2018f3c2ba16fb0c243ae792b33e3a5d3941dcf0124d2e2f","body_chars":208,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","classification_count_this_gate":1,"cumulative_classified_rows":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_item":{"binding":null,"boundary_kind":"STATEMENT_SEMICOLON","dependency_module":null,"end":12,"kind":"DIRECTIVE","ordinal":1,"source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"terminator":12},"first_item_sha256":"a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","second_item_classified":false,"source_executed":false,"version":"GATE4_DIAG_TYPES_FIRST_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one first static item from the frozen types.js body was classified. No second item was recovered or classified. No JavaScript was executed. The parent diag.js frontier and OTEL authority were not advanced or mutated.
