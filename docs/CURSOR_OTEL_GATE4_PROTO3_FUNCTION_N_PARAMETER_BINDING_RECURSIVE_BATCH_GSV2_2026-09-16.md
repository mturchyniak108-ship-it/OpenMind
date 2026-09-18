# Cursor OTEL Gate-4 proto3 function N parameter binding recursive batch GSV2

Date: 2026-09-16

## Status

- function: N
- signature: function N(e,t,n,s){
- n parameter origin: 7381
- n parameter index: 2
- qualified item count: 3
- stop kind: FUNCTION_N_SCOPE_END_REACHED
- stop coordinate: 8600
- proto3 source read count: 1
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `be5506e2486f4119cf345c34f5b21b2f90f415a96252eace5cfe1a61fe4cb805`

```json
{"state":{"current_authority":{"authority_sha256":"c01b54174bfefcfbc848cc0bd338c01622098c7dd4587b87d12ec1fd4184e154","document":"docs/CURSOR_OTEL_GATE4_PROTO3_WEBPACK_HEADER_N_RESTORATION_Q_RECURSIVE_BATCH_GSV2_2026-09-16.md","document_sha256":"1e89067725544b160d851077b13556839dff23def803849b9b2a8bde92492b7d"},"function_n_owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"N","origin":7381,"parameter_index":2,"parameters":[{"end":7378,"index":0,"start":7377,"text":"e"},{"end":7380,"index":1,"start":7379,"text":"t"},{"end":7382,"index":2,"start":7381,"text":"n"},{"end":7384,"index":3,"start":7383,"text":"s"}],"signature_end":7386,"signature_sha256":"fada0f439f1b8aa390e6b746cee7ba22469b6b2f02bbfc77355dfc14f8cc5c77","signature_start":7366},"function_n_owner_sha256":"bee66a40a7d4e4996419e207c008bcbbb24005b6799902edd2a8eefba0662b47","module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","proto3_source_read_count":1,"qualified_end":8307,"qualified_item_count":3,"qualified_items":[{"classification":"FUNCTION_PARAMETER_REFERENCE","end":7412,"next_significant":")","owner_origin":7381,"previous_significant":",","scope_depth":1,"start":7411,"type":"TOKEN","window":{"end":7456,"sha256":"0e2843893a2a77a7b0f67fde0867c539629259c4862fc4802c50ff62a2ae96e1","start":7366,"text":"function N(e,t,n,s){if(null===t)return s?p(e,n):k;switch(e){case l.DOUBLE:case l.FLOAT:if("}},{"classification":"FUNCTION_PARAMETER_REFERENCE","end":8184,"next_significant":"?","owner_origin":7381,"previous_significant":"n","scope_depth":2,"start":8183,"type":"TOKEN","window":{"end":8228,"sha256":"a5ce5116ddc5f8fea47a87b0abcbc181fe3507b66ba14636b89afe4ffc07fbb2","start":8138,"text":"!=typeof t)break;const o=d.M.parse(t);return n?o.toString():o;case l.FIXED64:case l.UINT64"}},{"classification":"FUNCTION_PARAMETER_REFERENCE","end":8307,"next_significant":"?","owner_origin":7381,"previous_significant":"n","scope_depth":2,"start":8306,"type":"TOKEN","window":{"end":8351,"sha256":"be484affbb1bcd417f8968772aace6f3e422c82b5214eae135810e26ea61ff0a","start":8261,"text":"=typeof t)break;const a=d.M.uParse(t);return n?a.toString():a;case l.BOOL:if(\"boolean\"!=ty"}}],"qualified_span_sha256":"fc0205e533f4b0e02fa21e03cdc8a3b56d13e8f3363c7ecadf8bb756375579a3","qualified_start":7411,"region":{"body_open":7385,"body_start":7386,"function_start":7366,"name":"N","parameter_close":7384,"parameter_open":7376,"parameters":[{"end":7378,"index":0,"start":7377,"text":"e"},{"end":7380,"index":1,"start":7379,"text":"t"},{"end":7382,"index":2,"start":7381,"text":"n"},{"end":7384,"index":3,"start":7383,"text":"s"}],"signature_end":7386,"signature_sha256":"fada0f439f1b8aa390e6b746cee7ba22469b6b2f02bbfc77355dfc14f8cc5c77","signature_text":"function N(e,t,n,s){"},"source_record_body_end":28565,"source_record_body_start":111,"stop":{"coordinate":8600,"detail":"function N lexical scope closes here","kind":"FUNCTION_N_SCOPE_END_REACHED","window":{"end":8670,"sha256":"120dbbd9b981d2cb87c2e44ea8499b2d588517e8f36efc6a7b9ba970b869ca5e","start":8530,"text":"Array(0);if(\"string\"!=typeof t)break;return h.K.dec(t)}throw new Error}function P(e,t,n,r){if(null===t)return\"google.protobuf.NullValue\"==e."}},"version":"PROTO3_FUNCTION_N_PARAMETER_BINDING_RECURSIVE_BATCH_GSV2_V1"},"state_sha256":"9b8e9015970b091082dca5bb8268f28c6ecbe5e32d49f370817bcbb526b1d344","version":"GATE4_PROTO3_FUNCTION_N_PARAMETER_BINDING_RECURSIVE_BATCH_GSV2_V1"}
```

## Evidence

Evidence SHA256: `3766c7e1b058f077b0e8fff191f9cc80443a1ed1d71c20bef872acfdf07ed037`

```json
{"authority_sha256":"be5506e2486f4119cf345c34f5b21b2f90f415a96252eace5cfe1a61fe4cb805","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","function_n_parameter_binding_qualified":true,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_read_count":1,"qualified_item_count":3,"stop_coordinate":8600,"stop_kind":"FUNCTION_N_SCOPE_END_REACHED","version":"GATE4_PROTO3_FUNCTION_N_PARAMETER_BINDING_RECURSIVE_BATCH_GSV2_V1_EVIDENCE"}
```

## Boundary

The previously frozen frontier proves that the function beginning at 7366 introduces parameter n. This macro parses the signature dynamically and qualifies the unique n parameter as parameter index 2. All subsequent safe n references inside function N are bound to that local function parameter. The macro stops before rebinding, require-like invocation, ambiguous syntax, or the function N closing frontier. No JavaScript or Cursor execution occurs.
