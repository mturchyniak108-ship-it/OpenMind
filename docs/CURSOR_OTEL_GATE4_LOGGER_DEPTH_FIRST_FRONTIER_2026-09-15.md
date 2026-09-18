# Cursor OTEL Gate-4 logger depth-first frontier

Date: 2026-09-15

## Status

- mode: LOGGER_RECORD_CHARACTERIZED
- parent dependency index: 9
- module: ../context/dist/logger.js
- committed completion authority search performed: YES
- logger bundled source read: YES
- dependency recursion performed: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e`

```json
{"binding_hazards":{"assignments":[3634,3745,4179,4600,6165],"declarations":[{"kind":"const","start":3628},{"kind":"const","start":6159}],"named_classes":[],"named_functions":[],"parameter_shadows":[{"kind":"FUNCTION_PARAMETER","start":290},{"kind":"FUNCTION_PARAMETER","start":330},{"kind":"FUNCTION_PARAMETER","start":1716},{"kind":"FUNCTION_PARAMETER","start":2250},{"kind":"FUNCTION_PARAMETER","start":2846},{"kind":"FUNCTION_PARAMETER","start":3185},{"kind":"ARROW_PARAMETER","start":6281},{"kind":"ARROW_PARAMETER","start":6349},{"kind":"ARROW_PARAMETER","start":6416},{"kind":"ARROW_PARAMETER","start":6484},{"kind":"SINGLE_ARROW_PARAMETER","start":4144}]},"completion_candidates":[],"logger_record":{"body_chars":6558,"body_sha256":"79531c6e162feb4c119602c5f88011684ea6397495cca63f5334f2313a4d41d3","header_end":4059546,"header_sha256":"e9fb29de2070de7b3c1cce201e8efa13d21ab7273483f71c5f4f77b99f393132","header_start":4059511,"next_module":"../context/dist/otel.js","record_end":4066105,"record_sha256":"e517cf1a35e54a43eb35c23045c3e2ab88b47e6a99ec6d8c0f089531cbeb57e4","record_start":4059511,"require_identifier":"n"},"mode":"LOGGER_RECORD_CHARACTERIZED","parent_contract_sha256":"9b7827271d0455dc0b01975a67e3c23e0a45e3457e5f01355f3b2222432df31a","require_like_calls":[{"argument":"\"../context/dist/core.js\"","call_end":91,"call_sha256":"323745cb9531fc192b253854de642b55203511a7450182a1c385bd2bcdd36193","call_start":63,"static_module":"../context/dist/core.js"}],"reusable_completion":null,"source_read":true,"static_dependencies":[],"static_frontier_clean":false,"template_hazards":[],"version":"GATE4_LOGGER_DEPTH_FIRST_FRONTIER_V1"}
```

## Evidence

Evidence SHA256: `e6a844d2ab29508afac32c55f65bcbebd7363c3e6afb5cc808acf9d7f7d53ac6`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_recursion_performed":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_complete":false,"logger_source_read":true,"mode":"LOGGER_RECORD_CHARACTERIZED","version":"GATE4_LOGGER_DEPTH_FIRST_FRONTIER_EVIDENCE_V1"}
```

## Boundary

Committed completion evidence is searched before any bundled logger source read. If no reusable completion authority is proven, only the exact frozen logger webpack record is read and its immediate require-like frontier is characterized. No logger child dependency is recursively opened in this block. Local-worker and Gate 4 remain open.
