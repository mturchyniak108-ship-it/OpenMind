# Cursor OTEL Gate-4 proto3 early lexical ownership macro GSV2

Date: 2026-09-16

## Status

- record provenance: immediate dashboard_pb parent authority
- token and call provenance: committed proto3 initial authority
- call 37: WEBPACK_STATIC_REQUIRE
- token 214: LOCAL_BINDING_ORIGIN
- token 228: LOCAL_REFERENCE owned by parameter 214
- token 298: LOCAL_BINDING_ORIGIN
- next frontier: frozen call 585
- deeper source read: NO
- proto3 complete: NO
- dashboard_pb complete: NO
- dashboard complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `0178e0b6d839ba8b417e6078fd87391bd559a45ad69ae00f43b5bee8c019fae8`

```json
{"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","parent_record_authority":{"contract_sha256":"b980767f3586301ce7469c600ee54d14d2ad9aa8933e5dc0485658cbedfe4a4e","document":"docs/CURSOR_OTEL_GATE4_DASHBOARD_PB_OWNERSHIP_DEPTH_MACRO_GSV2_2026-09-16.md","document_sha256":"3c0ee031a1b8bc0e5305c548f746d5a80ec5af13073b1ef93285dc57563cddf1"},"proto3_frontier_authority":{"contract_sha256":"736dab4ebd6d12de3ff20597380176b56d461f60e49b9780feaf6d7f91b1c631","document":"docs/CURSOR_OTEL_GATE4_PROTO3_INITIAL_OWNERSHIP_MACRO_GSV2_2026-09-16.md","document_sha256":"3d386df599d4ddd18cf87d68c199ec883f72f0e5ebef7f2612ca9c342e3c1657"},"state":{"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier_call":{"argument":"\"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js\"","call_end":692,"call_sha256":"e9930b772b99c47af365ce4a33b1e52dfe71cfd5e1d84bd7bc901670446595af","call_start":585,"definition_prefix":false,"next_nonspace_after_call":{"character":",","index":692},"source_window":{"end":775,"sha256":"ada28e145b1c47313fb39d3a518e6f81de08be2ff02b7ad978fa68cfe9f3731e","start":485,"text":"nction a(e){return\"localName\"in e?e:Object.assign(Object.assign({},e),{localName:e.name})}var l,u,c=n(\"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js\"),d=n(\"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/pro"},"static_module_candidate":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js"},"next_frontier_token":585,"qualified_call_37":{"classification":"WEBPACK_STATIC_REQUIRE","module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/private/assert.js","prefix_shadow_hits":[],"source_window":{"end":227,"sha256":"3ab677e821f43ae77451c3d06bb3aa29ccc995b00f38c0f1c934cde0ae1accb4","start":0,"text":"\"use strict\";n.d(t,{C:()=>me});var r=n(\"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/private/assert.js\");const s=Symbol(\"@bufbuild/protobuf/enum-type\");function i(e,t,n,r){e[s]=o(t"},"token_start":37},"resolved_early_noncall_tokens":[{"classification":"LOCAL_BINDING_ORIGIN","direct_bindings":[{"binding_kind":"FUNCTION_PARAMETER","origin":214,"owner_end":283,"owner_start":219,"signature_start":199}],"owner":null,"source_window":{"end":394,"sha256":"5647d822e3e23d2ea652cdeb665d476cb2b9fa842b43dc054962faca43ed0c1e","start":124,"text":"ist/esm/private/assert.js\");const s=Symbol(\"@bufbuild/protobuf/enum-type\");function i(e,t,n,r){e[s]=o(t,n.map((t=>({no:t.no,name:t.name,localName:e[t.no]}))))}function o(e,t,n){const r=Object.create(null),s=Object.create(null),i=[];for(const e of t){const t=a(e);i.push("},"targets_webpack_header_binding":false,"token_start":214},{"classification":"LOCAL_REFERENCE","direct_bindings":[],"owner":{"binding_kind":"FUNCTION_PARAMETER","origin":214,"owner_end":283,"owner_start":219,"signature_start":199},"source_window":{"end":408,"sha256":"f382e8445c8dfc11a7e9377e3d0d2ae2235334c6ccdca958ca5a15d6d1b0726c","start":138,"text":"e/assert.js\");const s=Symbol(\"@bufbuild/protobuf/enum-type\");function i(e,t,n,r){e[s]=o(t,n.map((t=>({no:t.no,name:t.name,localName:e[t.no]}))))}function o(e,t,n){const r=Object.create(null),s=Object.create(null),i=[];for(const e of t){const t=a(e);i.push(t),r[e.name]=t"},"targets_webpack_header_binding":false,"token_start":228},{"classification":"LOCAL_BINDING_ORIGIN","direct_bindings":[{"binding_kind":"FUNCTION_PARAMETER","origin":298,"owner_end":483,"owner_start":301,"signature_start":283}],"owner":null,"source_window":{"end":478,"sha256":"17a8f899d5934896bee3a679fc50d2166d6494e6bc8204bfc6e2c54ec15430d4","start":208,"text":"i(e,t,n,r){e[s]=o(t,n.map((t=>({no:t.no,name:t.name,localName:e[t.no]}))))}function o(e,t,n){const r=Object.create(null),s=Object.create(null),i=[];for(const e of t){const t=a(e);i.push(t),r[e.name]=t,s[e.no]=t}return{typeName:e,values:i,findName:e=>r[e],findNumber:e=>s"},"targets_webpack_header_binding":false,"token_start":298}],"version":"PROTO3_EARLY_LEXICAL_OWNERSHIP_GSV2_V2"},"state_sha256":"dff1b48d23ac0d8f9deaf8bfbc3e72c21865aa62911130564f62d08057ca5769","version":"GATE4_PROTO3_EARLY_LEXICAL_OWNERSHIP_MACRO_GSV2_V2"}
```

## Evidence

Evidence SHA256: `db8296633303116d4e1368f62b193e137dd657ceb173cbea0d0bd9f970105bb7`

```json
{"authority_sha256":"0178e0b6d839ba8b417e6078fd87391bd559a45ad69ae00f43b5bee8c019fae8","call_37_qualified":true,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","deeper_source_read":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"record_recovered_from_parent_authority":true,"tokens_214_228_298_qualified":true,"version":"GATE4_PROTO3_EARLY_LEXICAL_OWNERSHIP_MACRO_GSV2_V2_EVIDENCE"}
```

## Boundary

The current proto3 frontier authority supplies the frozen token and call population. The immediate dashboard_pb parent authority supplies the frozen proto3 record coordinates and hashes. No record identity is inferred from a contract that does not contain it. Qualification stops before call 585 and performs no deeper source read.
