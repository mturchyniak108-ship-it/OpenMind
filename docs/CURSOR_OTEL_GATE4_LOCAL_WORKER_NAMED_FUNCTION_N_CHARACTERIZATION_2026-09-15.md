# Cursor OTEL Gate-4 local-worker named function n characterization

Date: 2026-09-15

## Status

- named function n declarations characterized: YES
- semantic binding effect qualified: NO
- dependency recursion performed: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `cb0f2474417c144a776c1777fc7480f445b89751c09bb79f6bf2f5016044ac06`

```json
{"module":"../local-worker/dist/index.js","named_function_n_count":1,"named_function_n_rows":[{"body_end":3683,"body_sha256":"191ea2b468568f6a2f814033bfd0f5ed8230b4c12d4f64201aa07b6108734090","body_start":3588,"generator":false,"parameters_masked":"n","parent_brace":{"end":4060,"open":3573,"start":3574},"signature_end":3588,"signature_sha256":"bdbda21338dc8a4785e23a057ba48cd807c5ee6d578da4e2a8a48120381d6ece","signature_start":3574,"source_window":{"end":3834,"sha256":"4f78537e7c1791c608cbd5b1a36a2ef0f385e9cae7d8885065b72af7b1d9b93f","start":3474,"text":"(function(e){e(t)}))).then(o,a)}l((r=r.apply(e,t||[])).next())}))},c=function(e){return function(t){function n(n){t.error=t.hasError?new e(n,t.error,\"An error was suppressed during disposal.\"):n,t.hasError=!0}var r,s=0;return function e(){for(;r=t.stack.pop();)try{if(!r.async&&1===s)return s=0,t.stack.push(r),Promise.resolve().then(e);if(r.dispose){var i=r.d"}}],"record_sha256":"37c6490d700381266b16041a5c312bec7f042c2180813a708e47f3d21d31cdff","require_identifier":"n","semantic_binding_effect_qualified":false,"template_function_n_hazard_count":0,"template_function_n_hazards":[],"version":"GATE4_LOCAL_WORKER_NAMED_FUNCTION_N_CHARACTERIZATION_V1"}
```

## Evidence

Evidence SHA256: `a51fe55dbe8fd2594009e766d990c50cfebd4b1590c9a61d6bf7f7d3dbfb5f48`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"cb0f2474417c144a776c1777fc7480f445b89751c09bb79f6bf2f5016044ac06","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_recursion_performed":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"named_function_n_characterized":true,"semantic_binding_effect_qualified":false,"version":"GATE4_LOCAL_WORKER_NAMED_FUNCTION_N_CHARACTERIZATION_EVIDENCE_V1"}
```

## Boundary

This authority resolves only the previously unsupported syntactic construct consisting of named local functions n. Every such declaration is located against the frozen local-worker body and its function body boundary is proven from the static brace map. The JavaScript binding semantics of those declarations relative to the webpack header parameter n are intentionally not concluded in this document. No dependency recursion or Gate-4 advancement occurs.
