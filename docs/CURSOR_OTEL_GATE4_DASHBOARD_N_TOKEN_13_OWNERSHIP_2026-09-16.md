# Cursor OTEL Gate-4 dashboard n token 13 ownership

Date: 2026-09-16

## Status

- dashboard body token: n at offset 13
- prefix before token: strict-mode directive only
- local n shadow before token: NO
- syntactic use: property access
- targets webpack header binding: YES
- dependency require call: NO
- dashboard child recursion: NO
- dependency 12 source read: NO
- dashboard complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `fd2c822b17fbcbd13467b51242fe13c8fef234c7f429c1b11d876246d4c80e2c`

```json
{"module":"../cursor-config/dist/dashboard.js","ownership":{"classification":"WEBPACK_HEADER_PROPERTY_ACCESS","next_nonspace_character":".","next_nonspace_index":14,"prefix":"\"use strict\";","prefix_shadow_hazards":[],"previous_nonspace_character":";","previous_nonspace_index":12,"property_name":"d","require_identifier":"n","targets_webpack_header_binding":true,"token_start":13,"treat_as_dependency_require_call":false},"record_sha256":"518aa703ce42e37e5284725ab3cab3b31236a33ef603c3b6d5e282236605b9a4","source_window":{"end":233,"sha256":"bf62586e65917fd0a275d865ca6aa307813c4574f4874fe4a3f35780c8a8f96c","start":0,"text":"\"use strict\";n.d(t,{m:()=>A});var r=n(\"../proto/dist/generated/aiserver/v1/dashboard_connect.js\"),s=n(\"../../node_modules/.pnpm/@connectrpc+connect@1.6.1_patch_hash=c9c7616ccfc0246b19c6537f56676d8501713cb6c94b440d13_ef7275568c8b1f1f4"},"version":"GATE4_DASHBOARD_N_TOKEN_13_OWNERSHIP_V1"}
```

## Evidence

Evidence SHA256: `a83f7018eaf11f9c7f4921837429d6da00a1c06a9b050139789bd34eebda878f`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"fd2c822b17fbcbd13467b51242fe13c8fef234c7f429c1b11d876246d4c80e2c","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dashboard_child_recursion":false,"dashboard_complete":false,"dependency_12_source_read":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"token_13_owned":true,"version":"GATE4_DASHBOARD_N_TOKEN_13_OWNERSHIP_EVIDENCE_V1"}
```

## Boundary

This authority resolves only the first dashboard require-identifier ownership frontier at body offset 13. The token follows only the strict-mode directive, has no preceding local n binding, and is immediately followed by a static property access. It therefore targets the webpack header n binding but is not a dependency require call. No later dashboard ownership hazard, nonliteral call, child dependency, or local-worker dependency 12 is qualified here.
