# Cursor OTEL Gate-4 is-message call 36 message GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/is-message.js
- token 36 classification: QUALIFIED_STATIC_REQUIRE_CALL
- static target: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js
- call end: 143
- statement delimiter: semicolon
- next frontier token: 306
- next frontier qualified: NO
- message.js source read: NO
- is-message complete: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `0daedaa02244d15b9dc5b1c7db08eb39e50d57c1b9bfd3949970a5cc53075c48`

```json
{"state":{"current_authority":{"block_sha256":"fd3a8473fec3bd5cf2597d44de241c93a97829c615060939647642b6acd8ff91","document":"docs/CURSOR_OTEL_GATE4_IS_MESSAGE_TOKEN13_RUNTIME_HELPER_GSV2_2026-09-16.md","document_sha256":"3b4e984876b9a2b86b41031f9572efb32bd8ab950db3b37690a3490c2f69b374"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/is-message.js","next_frontier":{"frontier_kind":"UNRESOLVED_NONCALL_TOKEN","source_window":{"end":441,"sha256":"68070c14a4f48546606216fd52c0c744e0c7543f0612bd94738002af0f3b145a","start":206,"text":"bject.getOwnPropertyNames(r.Q.prototype).every((t=>t in e&&\"function\"==typeof e[t])))return!1;const n=e.getType();return null!==n&&\"function\"==typeof n&&\"typeName\"in n&&\"string\"==typeof n.typeName&&(void 0===t||n.typeName==t.typeName)}"},"token_start":306},"qualified_call":{"call_end":143,"call_sha256":"e9930b772b99c47af365ce4a33b1e52dfe71cfd5e1d84bd7bc901670446595af","call_start":36,"classification":"QUALIFIED_STATIC_REQUIRE_CALL","source_window":{"end":246,"sha256":"0ae45784b1e2d2bb5e4d814cb70f66f4502dce19404df7bc5f88c1752780df63","start":0,"text":"\"use strict\";n.d(t,{K:()=>s});var r=n(\"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js\");function s(e,t){if(null===e||\"object\"!=typeof e)return!1;if(!Object.getOwnPropertyNames(r.Q.prototype)"},"statement_delimiter":";","static_module_candidate":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js"},"record":{"body_bytes":441,"body_chars":441,"body_sha256":"ab6d0caa19c5c58ef6c1db6baf42312cfa63d5fcd55afdf72602192b47938834","header_end":3352184,"header_start":3352069,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/is-message.js","next_character":",","record_end":3352626,"record_sha256":"cdf10ed3a162c268672cdcc01a3e2f822c989a698c0c2012c949996dfa403f31","record_start":3352069,"require_identifier":"n"},"version":"IS_MESSAGE_CALL36_MESSAGE_GSV2_V1"},"state_sha256":"cb2eee83925e0ee9c66c3a6a48d386bf0d47515d24fe61232aaf2b6216920eaf","version":"GATE4_IS_MESSAGE_CALL36_MESSAGE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `23dd5efab3f5781b216abab622230a03d631963b8722f27d003f7e67ddd8c349`

```json
{"authority_sha256":"0daedaa02244d15b9dc5b1c7db08eb39e50d57c1b9bfd3949970a5cc53075c48","call_36_qualified":true,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"is_message_complete":false,"javascript_executed":false,"message_child_source_read":false,"next_token_306_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"static_target":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","version":"GATE4_IS_MESSAGE_CALL36_MESSAGE_GSV2_V1_EVIDENCE"}
```

## Boundary

Frozen is-message.js token 36 is qualified as the exact static require call to message.js. The semicolon immediately after the call is proven at the frozen call boundary. No message.js source is read. Frozen token 306 is preserved as the next unresolved is-message.js ownership frontier.
