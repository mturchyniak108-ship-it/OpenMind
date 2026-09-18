# Cursor OTEL Gate-4 logger second n parameter shadow ownership

Date: 2026-09-15

## Status

- second logger binding hazard qualified: YES
- hazard start: 330
- binding kind: function parameter
- nested inside first qualified function: YES
- targets webpack header n: NO
- logger child recursion performed: NO
- logger complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `9266dbad2adb3ce824091194deb2ccdb5917c71d5e88d765f9278008156d5dcc`

```json
{"first_shadow_contract_sha256":"0e37682d9b99c0838bf76453f4fdbed28a22979d3efa00ac57f9d101fe084e15","logger_frontier_contract_sha256":"2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e","module":"../context/dist/logger.js","ownership":{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":472,"function_body_start":348,"function_name":null,"function_signature_end":348,"function_signature_start":330,"nested_within_first_shadow":true,"parameters":["e","t","n","r"],"parent_function_body_end":2846,"parent_function_body_start":314,"shadows_outer_function_n_within_body":true,"shadows_webpack_header_binding_within_body":true,"targets_webpack_header_binding":false},"record_sha256":"e517cf1a35e54a43eb35c23045c3e2ab88b47e6a99ec6d8c0f089531cbeb57e4","source_window":{"end":830,"sha256":"ea722b9ec49ef46ed9093dfed120af40d738c0bcfd40060183d9d160e44cd11f","start":180,"text":"tPath}function i(e){return\"object\"==typeof e&&null!==e&&(\"message\"in e||\"stack\"in e||\"name\"in e||\"cause\"in e)}function o(e,t,n,r,s,u){var c,d;const m=function(e,t,n,r){if(!t.inlineSerializer)return e;try{const s=t.inlineSerializer(e,{path:n,depth:r});return void 0===s?e:s}catch(t){return e}}(e,t,u,r);if(function(e){return\"object\"==typeof e&&null!==e&&\"summary\"===e.kind&&\"string\"==typeof e.summary}(m))return n.dim(`<${m.summary}>`);if(null===(e=m))return n.gray(\"null\");if(void 0===e)return n.gray(\"undefined\");if(\"string\"==typeof e){const r=function(e,t){return e.length<=t?e:`${e.slice(0,t)}...`}(e,t.maxStringLength);return n.green(JSON.stringi"},"target_hazard_start":330,"version":"GATE4_LOGGER_SECOND_N_PARAMETER_SHADOW_OWNERSHIP_V1"}
```

## Evidence

Evidence SHA256: `af3c49aa7ceae945a8b43605431f307706e7ec4875ec975598f683ec94762f61`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"9266dbad2adb3ce824091194deb2ccdb5917c71d5e88d765f9278008156d5dcc","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_child_recursion_performed":false,"logger_complete":false,"targets_webpack_header_binding":false,"version":"GATE4_LOGGER_SECOND_N_PARAMETER_SHADOW_OWNERSHIP_EVIDENCE_V1"}
```

## Boundary

The n identifier in the function signature beginning at logger body offset 330 is a local parameter binding. The complete recovered function is nested inside the already qualified function beginning at offset 290. The nested parameter therefore shadows both its parent function n binding and the webpack header parameter throughout its own body. No later logger hazard is advanced in this authority.
