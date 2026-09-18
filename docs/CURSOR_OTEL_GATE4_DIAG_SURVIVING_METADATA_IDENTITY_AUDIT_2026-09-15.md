# Cursor OTEL Gate-4 diag.js surviving metadata identity audit

Date: 2026-09-15

## Status

- Audit status: PASS
- Adjudication: `NO_SURVIVING_DIAG_BODY_IDENTITY`
- Body identity ready: NO
- Metadata conflict: NO
- Metadata absence proven: YES
- Identity bootstrap required: YES
- Source read performed: NO
- Source executed: NO
- OTEL authority mutated: NO

## Generic JSON metadata

- JSON files seen: 966
- JSON files parsed: 958
- JSON parse failures: 8
- Target-bearing JSON scopes: 0
- Structured complete body identity candidates: 0
- Structured partial metadata records: 0

## Non-bundle qualification text

- Text files scanned: 1998
- Files containing diag.js: 0
- Strong diag-scoped identity candidates: 0

## Tracked repository metadata

- Text files scanned: 833
- Files containing diag.js: 2
- Strong diag-scoped identity candidates: 0

## Identity adjudication

- Strong candidate count: 0
- Unique identity pair count: 0
- Authorized body chars: `None`
- Authorized body SHA256: `None`
- Next authority: `IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_AUDIT`

## Evidence

Evidence SHA256: `0b38a7ada35d2f0bf1010d0e277a063231c4fa814423d1f02f0d5b97d80dde62`

```json
{"adjudication":"NO_SURVIVING_DIAG_BODY_IDENTITY","api_context_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","authorized_body_chars":null,"authorized_body_sha256":null,"body_identity_ready":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","identity_bootstrap_required":true,"json_failures":8,"json_parsed":958,"json_seen":966,"json_target_scope_count":0,"metadata_absence_proven":true,"metadata_conflict":false,"next_authority":"IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_AUDIT","parent_frontier_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","prior_diag_authorization_evidence_sha256":"a9517a6e689cb5697327072d570137c51eb94576ef4f22772ba21100aee1033d","qualification_target_files":0,"qualification_text_pairs":[],"qualification_text_scanned":1998,"qualification_weak_hints":[],"repo_target_files":2,"repo_text_pairs":[],"repo_text_scanned":833,"repo_weak_hints":[{"body_chars":[2365],"body_shas":["d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e"],"diag_scoped_filename":false,"file":"docs/CURSOR_OTEL_GATE4_API_CONTEXT_FIRST_STATIC_FRONTIER_2026-09-15.md"},{"body_chars":[256],"body_shas":[],"diag_scoped_filename":true,"file":"docs/CURSOR_OTEL_GATE4_DIAG_DEPENDENCY_PRE_SOURCE_AUTHORIZATION_2026-09-15.md"}],"source_read_authorized_this_gate":false,"strong_candidates":[],"structured_candidates":[],"structured_partial_metadata":[],"unique_identity_pairs":[],"version":"GATE4_DIAG_SURVIVING_METADATA_IDENTITY_AUDIT_V1"}
```

## Strict boundary

The Cursor package source tree was excluded from metadata scanning. No diag.js module body was read or extracted by this gate. No source was executed and the OTEL authority was not mutated.
