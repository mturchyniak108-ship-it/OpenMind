# Cursor OTEL Gate-4 logger first n parameter shadow ownership

Date: 2026-09-15

## Status

- first logger binding hazard qualified: YES
- hazard start: 290
- binding kind: function parameter
- targets webpack header n: NO
- logger child recursion performed: NO
- logger complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `0e37682d9b99c0838bf76453f4fdbed28a22979d3efa00ac57f9d101fe084e15`

```json
{"logger_frontier_contract_sha256":"2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e","module":"../context/dist/logger.js","ownership":{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":2846,"function_body_start":314,"function_name":"o","function_signature_end":314,"function_signature_start":290,"parameters":["e","t","n","r","s","u"],"shadows_webpack_header_binding_within_function":true,"targets_webpack_header_binding":false},"record_sha256":"e517cf1a35e54a43eb35c23045c3e2ab88b47e6a99ec6d8c0f089531cbeb57e4","source_window":{"end":710,"sha256":"66912eda1839b14e7d1d4abc2f0e358aab3683287a79a498b71b33c330cef634","start":150,"text":"\"in e&&\"function\"==typeof e.getPath}function i(e){return\"object\"==typeof e&&null!==e&&(\"message\"in e||\"stack\"in e||\"name\"in e||\"cause\"in e)}function o(e,t,n,r,s,u){var c,d;const m=function(e,t,n,r){if(!t.inlineSerializer)return e;try{const s=t.inlineSerializer(e,{path:n,depth:r});return void 0===s?e:s}catch(t){return e}}(e,t,u,r);if(function(e){return\"object\"==typeof e&&null!==e&&\"summary\"===e.kind&&\"string\"==typeof e.summary}(m))return n.dim(`<${m.summary}>`);if(null===(e=m))return n.gray(\"null\");if(void 0===e)return n.gray(\"undefined\");if(\"string\"==typ"},"target_hazard_start":290,"version":"GATE4_LOGGER_FIRST_N_PARAMETER_SHADOW_OWNERSHIP_V1"}
```

## Evidence

Evidence SHA256: `5ca54e763f150e3cecbad3c9194b4810b5785eabd48a13fbbfdab409ca0c95ac`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"0e37682d9b99c0838bf76453f4fdbed28a22979d3efa00ac57f9d101fe084e15","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_child_recursion_performed":false,"logger_complete":false,"targets_webpack_header_binding":false,"version":"GATE4_LOGGER_FIRST_N_PARAMETER_SHADOW_OWNERSHIP_EVIDENCE_V1"}
```

## Boundary

The n identifier in the function signature beginning at logger body offset 290 is a local function parameter. Its ownership is restricted to that recovered function body and therefore does not mutate or replace the outer webpack require parameter n. Only this first logger binding hazard is resolved in this authority.
