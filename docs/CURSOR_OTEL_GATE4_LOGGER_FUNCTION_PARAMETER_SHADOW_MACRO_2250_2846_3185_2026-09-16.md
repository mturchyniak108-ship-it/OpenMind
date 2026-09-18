# Cursor OTEL Gate-4 logger function parameter shadow macro

Date: 2026-09-16

## Status

- logger function parameter hazards qualified in this macro: 3
- qualified offsets: 2250, 2846, 3185
- each n binding is a local function parameter: YES
- any qualified binding targets webpack header n: NO
- logger child recursion performed: NO
- logger complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `9a6cc0ec151686c1e43f6078755f1d0d0243233c8d50c5da3e8dfc14c74ac3c2`

```json
{"logger_frontier_contract_sha256":"2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e","module":"../context/dist/logger.js","prior_shadow_contract_sha256":["0e37682d9b99c0838bf76453f4fdbed28a22979d3efa00ac57f9d101fe084e15","9266dbad2adb3ce824091194deb2ccdb5917c71d5e88d765f9278008156d5dcc","be03782de1b123bf6e08760b995cb13bab0f7166a7c55fd847dbc6fabb218165"],"qualified_function_parameter_shadows":[{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":2832,"function_body_start":2272,"function_name":null,"function_signature_end":2272,"function_signature_start":2250,"parameters":["e","t","n","r","s","i"],"prior_shadow_containers":[1],"source_window":{"end":2810,"sha256":"8fcfc82e0b21535c14cedb24369c84b636fb7f0ecac0c1179ed85ccad7b037fc","start":2070,"text":"... ${a.length-l} more`));const c=n.dim(\", \"),d=`${n.dim(\"Map{\")}${u.join(c)}${n.dim(\"}\")}`;return s.delete(e),d}(e,t,n,r,s,u):e instanceof Set?l(Array.from(e.values()),t,n,r,s,u):function(e,t,n,r,s,i){var a,l;if(r>=t.maxDepth){const t=null!==(l=null===(a=null==e?void 0:e.constructor)||void 0===a?void 0:a.name)&&void 0!==l?l:\"Object\";return n.dim(`[${t}]`)}if(s.has(e))return n.dim(\"[Circular]\");s.add(e);const u=Object.entries(e);if(0===u.length){const t=n.dim(\"{}\");return s.delete(e),t}const c=Math.min(u.length,t.maxEntries),d=u.slice(0,c).map((([e,a])=>{const l=o(a,t,n,r+1,s,i.concat(e));return`${n.cyan(e)}: ${l}`}));u.length>c&&d.push(n.dim(`... ${u.length-c} more`));const m=n.dim(\", \"),p=`${n.dim(\"{\")}${d.join(m)}${n.dim(\"}\")}`"},"targets_webpack_header_binding":false},{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":3185,"function_body_start":2870,"function_name":"a","function_signature_end":2870,"function_signature_start":2846,"parameters":["e","t","n","r","s","i"],"prior_shadow_containers":[],"source_window":{"end":3406,"sha256":"1a6e052d6bfb34aeeac6041827cfb45863cdc97001cd3c293ff4d73c4a24f61b","start":2666,"text":"return`${n.cyan(e)}: ${l}`}));u.length>c&&d.push(n.dim(`... ${u.length-c} more`));const m=n.dim(\", \"),p=`${n.dim(\"{\")}${d.join(m)}${n.dim(\"}\")}`;return s.delete(e),p}(e,t,n,r,s,u)}function a(e,t,n,r,s,i){const a=e;if(s.has(a))return n.dim(\"[Circular]\");s.add(a);const l=\"string\"==typeof e.name?e.name:\"Error\",u=\"string\"==typeof e.message?e.message:\"\",c=u?`${l}: ${u}`:l;let d=n.red(c);if(\"cause\"in e&&void 0!==e.cause){const a=o(e.cause,t,n,r+1,s,i.concat(\"cause\"));d=`${d} ${n.dim(\"cause=\")}${a}`}return s.delete(a),d}function l(e,t,n,r,s,i){if(r>=t.maxDepth)return n.dim(`[Array(${e.length})]`);if(s.has(e))return n.dim(\"[Circular]\");if(s.add(e),0===e.length){const t=n.dim(\"[]\");return s.delete(e),t}const a=Math.min(e.length,t.maxArrayL"},"targets_webpack_header_binding":false},{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":3605,"function_body_start":3209,"function_name":"l","function_signature_end":3209,"function_signature_start":3185,"parameters":["e","t","n","r","s","i"],"prior_shadow_containers":[],"source_window":{"end":3745,"sha256":"888c6eb8ad575e0ad99834256fc72f064da47184cd6ce6205f7656db5c313ba9","start":3005,"text":".message:\"\",c=u?`${l}: ${u}`:l;let d=n.red(c);if(\"cause\"in e&&void 0!==e.cause){const a=o(e.cause,t,n,r+1,s,i.concat(\"cause\"));d=`${d} ${n.dim(\"cause=\")}${a}`}return s.delete(a),d}function l(e,t,n,r,s,i){if(r>=t.maxDepth)return n.dim(`[Array(${e.length})]`);if(s.has(e))return n.dim(\"[Circular]\");if(s.add(e),0===e.length){const t=n.dim(\"[]\");return s.delete(e),t}const a=Math.min(e.length,t.maxArrayLength),l=e.slice(0,a).map(((e,a)=>o(e,t,n,r+1,s,i.concat(a))));e.length>a&&l.push(n.dim(`... ${e.length-a} more`));const u=n.dim(\", \"),c=`${n.dim(\"[\")}${l.join(u)}${n.dim(\"]\")}`;return s.delete(e),c}function u(e={}){var t;const n=function(e){var t,n,r,s,i,o,a;return{indent:\" \".repeat(null!==(t=e.indent)&&void 0!==t?t:2),maxDepth:null!==("},"targets_webpack_header_binding":false}],"record_sha256":"e517cf1a35e54a43eb35c23045c3e2ab88b47e6a99ec6d8c0f089531cbeb57e4","target_starts":[2250,2846,3185],"version":"GATE4_LOGGER_FUNCTION_PARAMETER_SHADOW_MACRO_2250_2846_3185_V1"}
```

## Evidence

Evidence SHA256: `9a745debd06a977a1c3c11664651fa03fc260328156d1feb36691db334c05f04`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"9a6cc0ec151686c1e43f6078755f1d0d0243233c8d50c5da3e8dfc14c74ac3c2","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_child_recursion_performed":false,"logger_complete":false,"qualified_shadow_count":3,"targets_webpack_header_binding_count":0,"version":"GATE4_LOGGER_FUNCTION_PARAMETER_SHADOW_MACRO_2250_2846_3185_EVIDENCE_V1"}
```

## Boundary

This macro consumes the next three already identified logger function-parameter hazards in strict source order. Each recovered function binds its own parameter named n and therefore excludes the webpack header binding throughout that function body. The macro stops before the next source-order binding frontier at the const declaration beginning at body offset 3628.
