# Cursor OTEL Gate-4 local-worker expression arrow shadows

Date: 2026-09-15

## Status

- First expression-bodied arrow ambiguity closed: YES
- Second expression-bodied arrow ambiguity closed: YES
- Remaining expression-bodied arrow ambiguity count: 0
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `9f69bb69d1672e2935e0d007359cc40ba7b9477f5233638c7b3daffa8d62508a`

```json
{"first_arrow_state":{"arrow":{"arrow_end":8663,"arrow_sha256":"f6c61eb61b4addb65e31b70ecfc151fb377516e06e731eb7f4975504b0d144a8","arrow_start":8654,"boundary":"BASE_COMMA","expression_end":8692,"expression_sha256":"48dea69ae13ebaecdc9aed389592b9358e275d7d92064f8912c22a9a5d30ead2","expression_start":8663,"parameter_shadow":"n","parameters":["e","t","n"],"shadowed_n_call_count":0,"shadowed_n_calls":[],"status":"CLOSED"},"module":"../local-worker/dist/index.js","result":"PARAMETER_N_SHADOWS_WEBPACK_REQUIRE_FOR_COMPLETE_EXPRESSION_BODY","version":"GATE4_LOCAL_WORKER_FIRST_EXPRESSION_ARROW_SHADOW_V1"},"first_arrow_state_sha256":"d32669a5d1c27e3468b2df97cd5c49f99ba527c757675e1ebdd607098168b4d9","local_worker_body_sha256":"abe009d6f721a416f0aa0a0e1472ec3c4391f56e0822d7ec2ddcc55497d9cf7e","local_worker_record_sha256":"37c6490d700381266b16041a5c312bec7f042c2180813a708e47f3d21d31cdff","module":"../local-worker/dist/index.js","second_arrow_state":{"arrow":{"arrow_end":21929,"arrow_sha256":"53109ae3359d94032df038d7b475d1ede43b7450e2e4c9fdef18498c0e99a119","arrow_start":21926,"boundary":"UNMATCHED_CLOSE_BRACE","expression_end":22283,"expression_sha256":"45171ac856ca37ac6a9dc11a4b61d56d80f128c2067474f3a307b81db5704d7d","expression_start":21929,"parameter_shadow":"n","parameters":["n"],"shadowed_n_call_count":0,"shadowed_n_calls":[],"status":"CLOSED"},"module":"../local-worker/dist/index.js","result":"PARAMETER_N_SHADOWS_WEBPACK_REQUIRE_FOR_COMPLETE_EXPRESSION_BODY","version":"GATE4_LOCAL_WORKER_SECOND_EXPRESSION_ARROW_SHADOW_V1"},"second_arrow_state_sha256":"8cfb4992b73ffd29baf70c68d1089c2075155fe79ef214ad47696c57f46ed63a","unresolved_expression_arrow_ambiguity_count":0,"version":"GATE4_LOCAL_WORKER_EXPRESSION_ARROW_SHADOWS_V1"}
```

## Evidence

Evidence SHA256: `c648dc2a80871f9803eaf4c24333f18a938d48a9999faa3a328a72ba3e97cfa8`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"9f69bb69d1672e2935e0d007359cc40ba7b9477f5233638c7b3daffa8d62508a","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"module":"../local-worker/dist/index.js","version":"GATE4_LOCAL_WORKER_EXPRESSION_ARROW_SHADOWS_EVIDENCE_V1"}
```

## Boundary

The first expression-bodied arrow is characterized before the second. For each arrow, the complete expression body is bounded statically and the parameter named n is proven to shadow the webpack header require identifier for that expression body. No local-worker completion is claimed here. The remaining unshadowed identifier mutation and nonliteral-call frontier is intentionally left unresolved. Gate 5 is not evaluated and Cursor is not executed.
