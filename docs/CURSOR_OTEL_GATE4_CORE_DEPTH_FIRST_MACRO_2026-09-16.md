# Cursor OTEL Gate-4 core depth-first macro

Date: 2026-09-16

## Status

- logger require binding closed: YES
- logger true dependency: ../context/dist/core.js
- committed core completion search performed first: YES
- mode: CORE_RECORD_CHARACTERIZED
- core bundled source read: YES
- logger formally completed: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `a866f96b79f6e6a78c73c75a96e362ad0e936e7917fe18678eaca61614115e2b`

```json
{"binding_hazards":{"assignments":[591,777,1494,1988],"declarations":[{"kind":"const","start":585},{"kind":"var","start":1963},{"kind":"var","start":2087}],"named_functions":[],"parameter_shadows":[{"kind":"ARROW_PARAMETER","start":1604}]},"completion_candidates":[],"core_record":{"body_chars":2210,"body_sha256":"522300d5636c02aa28153f54588732e8bd481beaf92173a59eaaf67d7ed4f7e3","header_end":4057299,"header_sha256":"de014992de9b319f83ee90dc087cc752b7b4f55c0118c5fe1bfdbcf95ac9bdd1","header_start":4057266,"next_module":"../context/dist/logger.js","record_end":4059510,"record_sha256":"e0b0b92764d3e198f2ef5974e3835caf739391e996642d85b94bc18591c6df8a","record_start":4057266,"require_identifier":"n"},"core_source_read":true,"logger_completed_state":null,"logger_formally_completed":false,"logger_return_state":null,"logger_scope_contract_sha256":"8697094db58055e9f5474f0f63f199a01f11b9a90c8d5b7c0ddf6941b6722d91","mode":"CORE_RECORD_CHARACTERIZED","require_like_calls":[],"reusable_core_completion":null,"static_dependencies":[],"static_frontier_clean":false,"template_hazards":[],"version":"GATE4_CORE_DEPTH_FIRST_MACRO_V1"}
```

## Evidence

Evidence SHA256: `7a22505a8b6224260ad79c70c3fe57c4f6283614b7138b3c89d1885840b0e718`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"a866f96b79f6e6a78c73c75a96e362ad0e936e7917fe18678eaca61614115e2b","core_source_read":true,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_complete":false,"mode":"CORE_RECORD_CHARACTERIZED","version":"GATE4_CORE_DEPTH_FIRST_MACRO_EVIDENCE_V1"}
```

## Boundary

Committed completion evidence for core.js is searched before any core source read. If reusable completion exists, core source is not reread and logger.js is formally completed from its frozen one-dependency authority. Otherwise only the exact core webpack record and immediate require frontier are characterized. No unresolved core child is recursively opened in this block.
