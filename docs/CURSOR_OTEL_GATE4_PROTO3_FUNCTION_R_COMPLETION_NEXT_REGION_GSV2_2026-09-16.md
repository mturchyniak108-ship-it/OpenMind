# Cursor OTEL Gate-4 proto3 function R completion and next region GSV2

Date: 2026-09-16

## Status

- function R closing coordinate: 7249
- function R scope complete: YES
- next function: Q
- next function start: 7250
- next function parameters: ["e","t"]
- next function body start: 7266
- next owner assigned: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `dda0241d8f263ff011615a760d565dab4552f01c6a30458bb6fb3f86f549d3fe`

```json
{"state":{"current_authority":{"authority_sha256":"927633cb209d9d9766f3a30dca5528a0976c676546a595a82f1e05cd9df7fab2","document":"docs/CURSOR_OTEL_GATE4_PROTO3_RECURSIVE_BATCH_FROM6296_GSV2_2026-09-16.md","document_sha256":"9739d31b895e0fe01965b3372e37781a0e7169521d38256b05461dc8291d0306"},"function_r_completion":{"closing_coordinate":7249,"closing_delimiter":"}","closing_window_sha256":"49c8d13e80bfcbb365bf5c630be27286c86bfb357539a74cc0d2d742fc96eb85","closing_window_start":7217,"function_name":"R","owner_origin":5099,"qualified_frontiers_before_close":17,"status":"FUNCTION_SCOPE_COMPLETE"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"NEXT_FUNCTION_BODY_OWNERSHIP_DISCOVERY_REQUIRED","function_body_start":7266,"function_name":"Q","function_start":7250,"n_parameter_rows":[],"owner_assigned":false,"parameters":["e","t"],"signature_end":7266,"signature_sha256":"7f0a9dc3c5c8cacb23f6b983d2c216d34668b80bf1d393f3e192387d58cbad6b","source_reread":true,"start":7266},"next_region":{"body_open":7265,"body_start":7266,"function_start":7250,"name":"Q","name_end":7260,"parameter_end":7264,"parameter_open":7260,"parameter_start":7261,"parameters":["e","t"],"signature_end":7266,"signature_sha256":"7f0a9dc3c5c8cacb23f6b983d2c216d34668b80bf1d393f3e192387d58cbad6b","signature_text":"function Q(e,t){"},"proto3_source_read_count":1,"source_record_body_end":28565,"source_record_body_start":111,"version":"PROTO3_FUNCTION_R_COMPLETION_NEXT_REGION_GSV2_V1"},"state_sha256":"07753fd93c1f6d296cb4ec5ac97f4dc43775283055d0b3c24f2107e5813cba4b","version":"GATE4_PROTO3_FUNCTION_R_COMPLETION_NEXT_REGION_GSV2_V1"}
```

## Evidence

Evidence SHA256: `63663488a77fb810730600d82bf1a1728bebc1b14980513c2f15325d81d2e970`

```json
{"authority_sha256":"dda0241d8f263ff011615a760d565dab4552f01c6a30458bb6fb3f86f549d3fe","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","function_r_complete":true,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_owner_assigned":false,"next_region_discovered":true,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_read_count":1,"version":"GATE4_PROTO3_FUNCTION_R_COMPLETION_NEXT_REGION_GSV2_V1_EVIDENCE"}
```

## Boundary

The prior recursive authority proves function R reaches its lexical scope end at coordinate 7249. This authority freezes that closing delimiter and discovers only the immediately following function declaration and signature. No ownership is assigned inside the next function body. No n reference after function R is qualified. No JavaScript or Cursor execution occurs.
