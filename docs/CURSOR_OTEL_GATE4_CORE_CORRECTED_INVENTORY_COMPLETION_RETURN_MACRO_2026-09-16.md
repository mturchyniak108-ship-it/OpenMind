# Cursor OTEL Gate-4 core corrected inventory completion return macro

Date: 2026-09-16

## Status

- core n parameter origins: 254, 1604
- corrected simple n keyword starts: 585, 754, 1963, 2087
- corrected simple n identifier starts: 591, 777, 1967, 2091
- committed destructuring n binding start: 1161
- core n assignments: 591, 777, 1494, 1988
- webpack n assignments: 0
- webpack n calls: 0
- core true dependencies: 0
- core complete: YES
- logger complete: YES
- local-worker dependency 9 complete: YES
- local-worker dependency 10 complete by reuse: YES
- local-worker resolved prefix count: 10
- next dependency index: 11
- next dependency: ../cursor-config/dist/dashboard.js
- dependency 11 source read: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `c92dd5bb032e4e14539dfd8ac5db3156c94770b9354d7adf668b8abc87f2e4d4`

```json
{"core_completed_state":"d635948c0eaaa02ec9aabc540194f070b6408cc4abc5bf9230dec78252432a37","core_completion_payload":{"complete":true,"completed_state_sha256":"2a898b3da31629ff97c44da615be78c8af7461b719b54ddc1b69a4b83be95f23","module":"../context/dist/core.js","record_sha256":"e0b0b92764d3e198f2ef5974e3835caf739391e996642d85b94bc18591c6df8a","true_static_dependencies":[],"version":"CORE_COMPLETION_CORRECTED_INVENTORY_V1"},"core_return_state":"773d1ec9f5956d455c4c24a33af7803cab0a9e0b3ce5eb3df46705c6b627db2d","core_scope":{"assignments":[{"assignment_start":591,"classification":"DECLARATION_INITIALIZER","owner_end":660,"owner_kind":"BLOCK_SCOPE","owner_start":585,"targets_webpack_header_binding":false},{"assignment_start":777,"classification":"DECLARATION_INITIALIZER","owner_end":950,"owner_kind":"BLOCK_SCOPE","owner_start":754,"targets_webpack_header_binding":false},{"assignment_start":1494,"classification":"ASSIGNMENT_EXPRESSION","owner_end":2099,"owner_kind":"VAR_SIMPLE_DECLARATION","owner_start":1487,"targets_webpack_header_binding":false},{"assignment_start":1988,"classification":"ASSIGNMENT_EXPRESSION","owner_end":2053,"owner_kind":"VAR_SIMPLE_DECLARATION","owner_start":1963,"targets_webpack_header_binding":false}],"corrected_inventory_diagnostic_reference_sha256":"9314364db2f4c068c8f62080690d7c807daaa312b2a4725d71af9671550c7bc6","corrected_inventory_sha256":"78e14b766a56dd9421053b35f2408dae31903ca5083ee148c08a94605aa482fd","declarations":[{"binding_form":"SIMPLE","declaration_end":613,"declaration_keyword_start":585,"declarator_raw":"n=new Map(this.values)","identifier_start":591,"initializer_present":true,"kind":"const","owner_end":660,"owner_kind":"BLOCK_SCOPE","owner_start":585,"targets_webpack_header_binding":false},{"binding_form":"SIMPLE","declaration_end":871,"declaration_keyword_start":754,"declarator_raw":"n=new i(this,t.signal)","identifier_start":777,"initializer_present":true,"kind":"const","owner_end":950,"owner_kind":"BLOCK_SCOPE","owner_start":754,"targets_webpack_header_binding":false},{"binding_form":"DESTRUCTURING","declaration_end":1184,"declaration_keyword_start":1156,"declarator_raw":"[t,n]=this.withCancel()","identifier_start":1161,"initializer_present":true,"kind":"const","owner_end":1212,"owner_kind":"BLOCK_SCOPE","owner_start":1156,"targets_webpack_header_binding":false},{"binding_form":"SIMPLE","declaration_end":1968,"declaration_keyword_start":1963,"declarator_raw":"n","identifier_start":1967,"initializer_present":false,"kind":"var","owner_end":2053,"owner_kind":"FUNCTION_SCOPE","owner_start":1963,"targets_webpack_header_binding":false},{"binding_form":"SIMPLE","declaration_end":2098,"declaration_keyword_start":2087,"declarator_raw":"n","identifier_start":2091,"initializer_present":false,"kind":"var","owner_end":2099,"owner_kind":"FUNCTION_SCOPE","owner_start":1487,"targets_webpack_header_binding":false}],"destructuring_authority_sha256":"2255755a7701fba0c7e7834caa9b83158971ad1c10c5b52c40fc3434302ad0aa","module":"../context/dist/core.js","parameter_bindings":[{"binding_kind":"METHOD_PARAMETER","name":"constructor","origin":254,"owner_end":382,"owner_start":276,"targets_webpack_header_binding":false},{"binding_kind":"ARROW_PARAMETER","name":null,"origin":1604,"owner_end":1808,"owner_start":1612,"targets_webpack_header_binding":false}],"record_sha256":"e0b0b92764d3e198f2ef5974e3835caf739391e996642d85b94bc18591c6df8a","true_static_dependencies":[],"version":"CORE_SCOPE_CLOSED_CORRECTED_INVENTORY_V1","webpack_assignment_count":0,"webpack_call_count":0},"core_scope_state":"2a898b3da31629ff97c44da615be78c8af7461b719b54ddc1b69a4b83be95f23","core_zero_dependency_leaf":true,"local_worker_next_dependency":"../cursor-config/dist/dashboard.js","local_worker_next_dependency_index":11,"local_worker_resolved_prefix":["node:url","node:http","../context/dist/otel.js","../utils/dist/file-url.js","node:crypto","node:fs","node:fs/promises","node:os","../context/dist/logger.js","../context/dist/core.js"],"local_worker_resolved_prefix_count":10,"logger_completed_state":"a3e9c25fd58e17810d10f18f3aa59782413e82329c729641db333c16baf21b86","logger_completion_payload":{"complete":true,"core_completed_state":"d635948c0eaaa02ec9aabc540194f070b6408cc4abc5bf9230dec78252432a37","logger_scope_contract_sha256":"8697094db58055e9f5474f0f63f199a01f11b9a90c8d5b7c0ddf6941b6722d91","module":"../context/dist/logger.js","true_static_dependencies":["../context/dist/core.js"],"version":"LOGGER_COMPLETION_FROM_CORRECTED_CORE_V1"},"logger_return_state":"420b77189c5cef1d2fc7e994bfaa6036a53df62469264933b1ce755a797e968e","version":"GATE4_CORE_CORRECTED_INVENTORY_COMPLETION_RETURN_MACRO_V1"}
```

## Evidence

Evidence SHA256: `1931ec394d08652c6864e34d4e994cc42ada1e9cece5855e9bf29653807a8ede`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"c92dd5bb032e4e14539dfd8ac5db3156c94770b9354d7adf668b8abc87f2e4d4","core_complete":true,"core_dependency_count":0,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_11_source_read":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"local_worker_resolved_prefix_count":10,"logger_complete":true,"next_dependency":"../cursor-config/dist/dashboard.js","next_dependency_index":11,"version":"GATE4_CORE_CORRECTED_INVENTORY_COMPLETION_RETURN_MACRO_EVIDENCE_V1"}
```

## Boundary

The corrected declaration inventory adds the previously omitted const n declarator at keyword offset 754 and identifier offset 777. The committed destructuring ownership at 1161 and the method parameter correction at 254 are incorporated. Every frozen n assignment is locally owned and the webpack require parameter has zero assignments and zero calls. Core therefore completes as a zero-dependency leaf. Logger completes from core, and local-worker advances through dependency 10 only. Dependency 11 is not read.
