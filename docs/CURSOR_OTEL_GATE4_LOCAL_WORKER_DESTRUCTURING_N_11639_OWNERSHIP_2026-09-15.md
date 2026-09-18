# Cursor OTEL Gate-4 local-worker destructuring n ownership at 11639

Date: 2026-09-15

## Status

- destructured n lexical ownership qualified: YES
- declaration kind: const
- owner: block scope 11576 to 11896
- targets webpack header require parameter: NO
- dependency recursion performed: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Semantic basis

The pattern `{promise:n,timer:r}` is the binding target of a `const` declaration. The identifier `n` is therefore a block-scoped lexical binding owned by the immediately containing block from body offset 11576 through 11896. References to `n` within that lexical scope resolve to this local binding rather than the outer webpack module parameter named `n`.

## Contract

Contract SHA256: `b4b0d1d0d3ce9b21ce5bccae18f12650c6bf12d8f23f1d02c991b8b6998dfc0d`

```json
{"characterization_contract_sha256":"bc7923b3f93de7de15f06a033cb33f48576812777bffa76a3259a6fdf259cdc9","module":"../local-worker/dist/index.js","ownership":{"binding_identifier":"n","binding_kind":"CONST_DESTRUCTURING_BINDING","declaration_start":11634,"declarator_start":11639,"lexical_scope_end":11896,"lexical_scope_start":11576,"owner_kind":"BLOCK_SCOPE","shadows_webpack_header_parameter_within_scope":true,"targets_webpack_header_binding":false},"record_sha256":"37c6490d700381266b16041a5c312bec7f042c2180813a708e47f3d21d31cdff","target_offset":11639,"version":"GATE4_LOCAL_WORKER_DESTRUCTURING_N_11639_OWNERSHIP_V1"}
```

## Evidence

Evidence SHA256: `80ba912294be54c8f3cd0456c769dcfcffea1aacc6fee1884b4be8ae38eaa758`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","binding_ownership_qualified":true,"contract_sha256":"b4b0d1d0d3ce9b21ce5bccae18f12650c6bf12d8f23f1d02c991b8b6998dfc0d","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_recursion_performed":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"targets_webpack_header_binding":false,"version":"GATE4_LOCAL_WORKER_DESTRUCTURING_N_11639_OWNERSHIP_EVIDENCE_V1"}
```

## Boundary

This authority qualifies only the ownership of the destructured n binding at body offset 11639. It does not rerun the complete local-worker scope model and does not recurse any dependency.
