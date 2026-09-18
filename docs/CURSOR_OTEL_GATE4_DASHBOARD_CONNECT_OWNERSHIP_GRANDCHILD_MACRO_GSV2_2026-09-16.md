# Cursor OTEL Gate-4 dashboard connect ownership grandchild macro GSV2

Date: 2026-09-16

## Status

- dashboard_connect token 13: WEBPACK_HEADER_PROPERTY_ACCESS
- dashboard_connect genuine static requires: 5
- dashboard_connect require binding closed: YES
- first grandchild: ../proto/dist/generated/aiserver/v1/dashboard_pb.js
- completion search before source read: YES
- mode: GRANDCHILD_RECORD_BOUNDED
- grandchild source read: YES
- deeper grandchild source read: NO
- dashboard complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `5235bd9e37c2765ebcc68c65ec7d579ea1aaf8c93dbb6df4b01841e5997767af`

```json
{"child_module":"../proto/dist/generated/aiserver/v1/dashboard_connect.js","child_ownership_state":"848eb4cb2e504c6f96601947585097da97d47c624c2ee0bd6b26b04ccd48f5b1","child_require_binding_closed":true,"child_static_dependencies":["../proto/dist/generated/aiserver/v1/dashboard_pb.js","../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/service-type.js","../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto-int64.js"],"completion_candidates":[],"grandchild_index":1,"grandchild_module":"../proto/dist/generated/aiserver/v1/dashboard_pb.js","grandchild_record":{"body_chars":1049793,"body_sha256":"d986ee486b320a5e17a417cb3000ee4825c07ca08d63a0a1f09a496b181be6be","header_end":6842338,"header_sha256":"4db136e864a1365dadf379a9bda3f802fe365722fbb11b5143dd3bea0ce5eea4","header_start":6842277,"next_module":"../proto/dist/generated/aiserver/v1/docs_pb.js","record_end":7892132,"record_sha256":"ec8ea93d545207c309836b846a955e7f8e95e0248fee091db4322e3e30d17c82","record_start":6842277,"require_identifier":"n"},"grandchild_require_identifier_tokens":[13,20,61271,61380,61490,61604,61732,61863,65199,65249,65322,65377,65432,65487,65549,100489,100544],"grandchild_return_state":null,"grandchild_source_read":true,"mode":"GRANDCHILD_RECORD_BOUNDED","ownership_rows":[{"classification":"WEBPACK_HEADER_PROPERTY_ACCESS","token_start":13},{"classification":"WEBPACK_STATIC_REQUIRE","static_module":"../proto/dist/generated/aiserver/v1/dashboard_pb.js","token_start":36},{"classification":"WEBPACK_STATIC_REQUIRE","static_module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/service-type.js","token_start":95},{"classification":"WEBPACK_STATIC_REQUIRE","static_module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","token_start":210},{"classification":"WEBPACK_STATIC_REQUIRE","static_module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","token_start":320},{"classification":"WEBPACK_STATIC_REQUIRE","static_module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto-int64.js","token_start":429}],"version":"GATE4_DASHBOARD_CONNECT_OWNERSHIP_GRANDCHILD_MACRO_GSV2_V1"}
```

## Evidence

Evidence SHA256: `81479526161196411c1f42fbc34990e73c44e90c41335a21dde74e6ef65de3a0`

```json
{"child_require_binding_closed":true,"contract_sha256":"5235bd9e37c2765ebcc68c65ec7d579ea1aaf8c93dbb6df4b01841e5997767af","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dashboard_complete":false,"gate4_closed":false,"gate5_evaluated":false,"grandchild_deeper_source_read":false,"grandchild_source_read":true,"javascript_executed":false,"local_worker_complete":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","version":"GATE4_DASHBOARD_CONNECT_OWNERSHIP_GRANDCHILD_MACRO_GSV2_EVIDENCE_V1"}
```

## Boundary

The dashboard_connect webpack require binding is closed before any grandchild recursion. Exactly five literal static dependencies are frozen. Completion authority for dashboard_pb is searched before any bounded source read. If no reusable completion exists, only the dashboard_pb webpack record is bounded. No deeper source is opened.
