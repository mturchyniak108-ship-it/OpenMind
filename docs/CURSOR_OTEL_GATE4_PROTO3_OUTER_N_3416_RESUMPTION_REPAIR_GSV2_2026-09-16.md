# Cursor OTEL Gate-4 proto3 outer n 3416 resumption repair GSV2

Date: 2026-09-16

## Status

- token 3416: OUTER_PARAMETER_REFERENCE_RESUMED
- owning parameter origin: 2929
- nested const n scope ended before token: YES
- intervening frozen n tokens after nested scope: 0
- next frontier token: 3486
- next frontier qualified: NO
- deeper source read: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `0ef68445d07f252391a34a31c6bd1a28d10f5f3b66ef89a30d3ea14240f68877`

```json
{"current_authority":{"block_sha256":"586c03a4051b5ec585a138b22d231fb30e73a560e8dc1466e72319bd5b59ab7c","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N2929_NESTED_SHADOW_MACRO_GSV2_2026-09-16.md","document_sha256":"26e1814418bf8b26f40fda4c0c12d54a21a286787de140d8a55fd12f0afb4a97"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","state":{"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"UNRESOLVED_NONCALL_TOKEN","source_window":{"end":3696,"sha256":"2085b0d9e7d5c697eb233ad14ef45966c3f62885785bd029f1decf15a242396b","start":3366,"text":"{},t.field),{opt:!0})),t.runtime.bin.writeField(a,n,o,i);const l=s.readerFactory(o.finish());for(;l.pos<l.len;){const[t,n]=l.tag(),r=l.skip(n,t);e.getType().runtime.bin.onUnknownField(e,t,n,r)}}function _(e,t){const n=e.getType();return t.extendee.typeName===n.typeName&&!!n.runtime.bin.listUnknownFields(e).find((e=>e.no==t.field"},"token_start":3486},"qualified_token":{"classification":"OUTER_PARAMETER_REFERENCE_RESUMED","nested_scope_end":3242,"owner":{"binding_kind":"FUNCTION_PARAMETER","origin":2929,"owner_end":3560,"owner_start":2934,"signature_start":2914},"source_window":{"end":3626,"sha256":"9c6d550f73d1e6874a324988742ca353af676961085ea65772f47f985306fdb1","start":3296,"text":"ted||\"enum\"!=a.kind&&\"scalar\"!=a.kind||(a=Object.assign(Object.assign({},t.field),{opt:!0})),t.runtime.bin.writeField(a,n,o,i);const l=s.readerFactory(o.finish());for(;l.pos<l.len;){const[t,n]=l.tag(),r=l.skip(n,t);e.getType().runtime.bin.onUnknownField(e,t,n,r)}}function _(e,t){const n=e.getType();return t.extendee.typeName===n"},"token_start":3416},"version":"PROTO3_OUTER_N_3416_RESUMPTION_REPAIR_GSV2_V1"},"state_sha256":"2bdaecf5860ff6fb9f43971bfaa89a5f414212311da4ffcbdc9c09e5d45d88b9","version":"GATE4_PROTO3_OUTER_N_3416_RESUMPTION_REPAIR_GSV2_V1"}
```

## Evidence

Evidence SHA256: `c3eb1744ab3e7c69cfa6c2bc347bef67aa1edcae47e5fc6f86298d2eb74b17f4`

```json
{"authority_sha256":"0ef68445d07f252391a34a31c6bd1a28d10f5f3b66ef89a30d3ea14240f68877","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","deeper_source_read":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"nested_scope_ended_before_3416":true,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","outer_parameter_2929_active_at_3416":true,"proto3_complete":false,"token_3416_qualified":true,"version":"GATE4_PROTO3_OUTER_N_3416_RESUMPTION_REPAIR_GSV2_V1_EVIDENCE"}
```

## Boundary

The previously qualified nested const n scope ends before token 3416. The previously qualified outer function parameter n at 2929 remains active through token 3416. No frozen n token occurs between the end of the nested scope and token 3416. Therefore token 3416 resumes ownership by the outer parameter. Only token 3416 is qualified by this repair. Token 3486 remains unresolved.
