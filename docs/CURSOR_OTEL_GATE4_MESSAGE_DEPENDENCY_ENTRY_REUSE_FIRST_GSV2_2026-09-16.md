# Cursor OTEL Gate-4 message dependency entry reuse-first GSV2

Date: 2026-09-16

## Status

- parent module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/is-message.js
- authorized parent call: 36
- dependency: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js
- entry mode: FRESH_RECORD_ENTRY
- committed completion searched first: YES
- committed entry authority searched second: YES
- fresh message source read: YES
- require identifier: n
- require token count: 17
- require call count: 0
- returned frontier kind: UNRESOLVED_NONCALL_TOKEN
- returned frontier token: 13
- JavaScript executed: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `ab726cc93c7aa995052af732a3ceefa59d484c36f71b0dc5de8e4240922bfac9`

```json
{"state":{"authorized_by":{"call36_authority":{"block_sha256":"0daedaa02244d15b9dc5b1c7db08eb39e50d57c1b9bfd3949970a5cc53075c48","document":"docs/CURSOR_OTEL_GATE4_IS_MESSAGE_CALL36_MESSAGE_GSV2_2026-09-16.md","document_sha256":"3835ad2531d03f66e5b33640176ab1da9563bdce051b6e561e10662d6f55a970"},"is_message_completion_authority":{"block_sha256":"d0e401663be7d0e68440c56434b8c209e64e6689bc20aec578c07cb39d484e4e","document":"docs/CURSOR_OTEL_GATE4_IS_MESSAGE_N306_OWNERSHIP_COMPLETION_GSV2_2026-09-16.md","document_sha256":"939a8ad3d8d9a994656ade1fbf06178078ba0a48a5edd2e118eb31f1157edfcc"}},"entry_mode":"FRESH_RECORD_ENTRY","message_frontier":{"frontier_kind":"UNRESOLVED_NONCALL_TOKEN","source_window":{"end":233,"sha256":"af26e74494b2110663522a3cef78fbfd4c2a3d302627238661767f2a105e8fff","start":0,"text":"\"use strict\";n.d(t,{Q:()=>r});class r{equals(e){return this.getType().runtime.util.equals(this.getType(),this,e)}clone(){return this.getType().runtime.util.clone(this)}fromBinary(e,t){const n=this.getType().runtime.bin,r=n.makeReadOp"},"token_start":13},"message_inventory":{"calls":[],"frontier":{"frontier_kind":"UNRESOLVED_NONCALL_TOKEN","source_window":{"end":233,"sha256":"af26e74494b2110663522a3cef78fbfd4c2a3d302627238661767f2a105e8fff","start":0,"text":"\"use strict\";n.d(t,{Q:()=>r});class r{equals(e){return this.getType().runtime.util.equals(this.getType(),this,e)}clone(){return this.getType().runtime.util.clone(this)}fromBinary(e,t){const n=this.getType().runtime.bin,r=n.makeReadOp"},"token_start":13},"regex_count":0,"template_count":1,"tokens":[13,190,221,249,328,347,406,447,453,612,664,690,737,797,848,879,918]},"message_module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","message_record":{"body_bytes":1093,"body_chars":1093,"body_sha256":"2ebcc3eb97d4981d4162bde34f8410350b801dda22e5a0211d33834a32ffccb9","header_end":3352739,"header_start":3352627,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","next_character":",","record_end":3353833,"record_sha256":"a9f324429ad4e207e8b9cf06af05273d5304d4e5fca2e4bb381b89d3f5e68600","record_start":3352627,"require_identifier":"n"},"message_source_read":true,"reused_authority":null,"version":"MESSAGE_DEPENDENCY_ENTRY_REUSE_FIRST_GSV2_V1"},"state_sha256":"60e5e764c7acc8853a43a0e27090efcfe81cd6d4a108125d3ed24c93cc8fe76c","version":"GATE4_MESSAGE_DEPENDENCY_ENTRY_REUSE_FIRST_GSV2_V1"}
```

## Evidence

Evidence SHA256: `cefd8e67b2d1915e3fe2ec8ac75e87318e200bcff44b0d1d61318195f82238a5`

```json
{"authority_sha256":"ab726cc93c7aa995052af732a3ceefa59d484c36f71b0dc5de8e4240922bfac9","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","entry_mode":"FRESH_RECORD_ENTRY","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"message_completion_reused":false,"message_entry_reused":false,"message_source_read":true,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"version":"GATE4_MESSAGE_DEPENDENCY_ENTRY_REUSE_FIRST_GSV2_V1_EVIDENCE"}
```

## Boundary

Committed full completion authority for message.js is checked before any fresh child source read. If no completion authority exists, committed frozen entry authority is checked next. Only when neither authority exists is the frozen Cursor bundle read to bound the exact message.js webpack record and inventory its require identifier. No message.js ownership frontier is qualified by this entry step. No JavaScript is executed.
