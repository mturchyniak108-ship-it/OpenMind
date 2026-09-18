# MAF Query Capsule Attach / Detach / Cleanup Validation V1.1 Verdict

**Status:** PASS

**Phase:** OpenMind Phase 6D-Q3 — Attach / Detach / Cleanup

**Scientific execution:** Complete

**V1.1 namespace:** Permanently spent; automatic and manual scientific retry are forbidden.

## Authority and frozen evidence

- Original Q3 scientific protocol SHA256: `323c0d4e0cbd5327382e3762e4d9529fba48f3748699861d96b31920db5b0363`
- V1.1 correction protocol SHA256: `27c820f292fae9bbbfe032d722da4d6ecadc237ca47b8119c82e93313a0d78af`
- V1.1 runner SHA256: `26b4bef94fa5f063f7340190879d37b124bba305da60ac0abc12e83433159f99`
- V1.1 runner freeze commit: `d6da1a7d1fe505b62044ca1e15444f490c85b305`
- V1.1 exact-once evidence freeze commit: `7485fad23791ca5676c26cdda890b1a1c32b6272`
- V1.1 permanent slot SHA256: `d20826af7c080b8660233ae9790fc761cbcd81d4bb45e9e033177f981455fa95`
- V1.1 published result SHA256: `2db54aca02c913ff9c54728aeb63bca6f280296a8564ef6a388be2e994290690`
- V1.1 result schema: `openmind.maf_query_capsule_attach_detach_cleanup_validation.v1_1`
- Independent V1 to V1.1 diff SHA256: `55b82175f1d50aeaf161dd2466ff4ee019f0cf318b5d4e1c2ce26bcd16777643`

Failed V1 remains immutable provenance:

- Failed V1 runner SHA256: `b3a0812f5abe7549ce2282efce78b33628d7cbc42689ba236c43ec1b767d4638`
- Failed V1 runner SHA-authority file SHA256: `7d1b08467817553d735106fd6d423f6e90057232aaf913d0ba9ba4c575778eaf`
- Failed V1 spent slot SHA256: `17cc5ac3ecd2caf6822dd6fb36b8c0273dda5bbde6791b598a51b933bb079a33`
- Failed V1 empty partial SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Failed V1 final result: absent

## Correction basis

The frozen V1 exact-once namespace was spent by a validation-harness Python class-identity mismatch before scientific result publication. The resident-directory implementation and the runtime observed different `ResidentPKEntry` class identities because the resident source was loaded under a separate dynamic module identity.

V1.1 corrected only the preregistered dependency-loading defect. The resident-directory implementation was loaded under canonical module identity before the runtime import, and prequalification required:

`resident.ResidentPKEntry is runtime.ResidentPKEntry`

The correction did not change the frozen Q3 scientific lifecycle question, the 48 scientific acceptance-check identifiers, the query cases, failure injections, budgets, lifecycle semantics, exact-once durability order, source evidence, or scientific claim boundary.

## Exact-once outcome

- Non-spending readiness: PASS.
- Fresh pre-arm readiness immediately before the scientific arm: PASS.
- Exact-once V1.1 run return code: `0`.
- Scientific checks: `48/48 PASS`.
- Failed checks: `[]`.
- Published result `all_pass`: `true`.
- Resident/runtime `ResidentPKEntry` identity provenance: `true`.
- V1.1 permanent slot: present and frozen.
- V1.1 partial after successful publication: absent.
- V1.1 namespace: permanently spent.
- V1.1 retry: forbidden.

The permanent slot journal contains the required three durable states in order:

1. `RESERVATION_PREPARED`
2. `RESERVED_DURABLE`
3. `PUBLISHED_DURABLE`

## Scientific conclusion

Within the frozen Q3 fixture, preregistered query cases, source generation, resident directory, selector authorities, and runtime semantics, V1.1 validates the attach / detach / cleanup lifecycle for query-scoped selected MAF objects.

The accepted evidence supports the following lifecycle conclusions:

- capsule-selected objects can be registered and attached from `COLD_DISK` to `MAPPED` in the required route order;
- one ownership lease per selected object is enforced and duplicate ownership is rejected;
- pinned demotion is rejected while ownership remains active;
- the required `HOT_MAF` and lifecycle-only synthetic `HOT_DENSE` transitions are exercised where preregistered;
- cleanup occurs in reverse route order;
- successful cleanup releases ownership leases, serialized bytes, dense bytes, and returns registered objects to `COLD_DISK`;
- preregistered failures before attach, after partial attach, after pin, after `HOT_MAF`, after `HOT_DENSE`, and during multi-object ownership clean back to the required baseline;
- close semantics remain terminal and idempotent as preregistered;
- the active record, generation manifest, physical segment, frozen Q1/Q2 evidence, and other canonical authorities remain unchanged under the validation.

## Claim boundary

This PASS supports **Q3 attach / detach / cleanup lifecycle, ownership, source-binding, cleanup, and failure-atomicity validation only**.

It does **not** establish:

- query route caching or Phase 6D-Q4;
- route expansion;
- inference or generation capability;
- answer correctness or answer quality;
- selective working-set sufficiency or Phase 6E;
- avoidance, parity, or replacement of a standard LLM inference pipeline;
- performance, latency, throughput, memory, or efficiency improvement;
- MAF-native model computation.

No inference, sufficiency, replacement, parity, quality, or performance claim follows from this Q3 verdict.

## Final verdict

**PASS — Q3 V1.1 Attach / Detach / Cleanup Validation is accepted.**

The V1 harness failure remains immutable failed provenance. The V1.1 class-identity correction is validated by the successful exact-once result. V1.1 must never be rerun because its namespace is permanently spent.

At this verdict boundary, Phase 6D-Q4 and Phase 6E remain **not entered**.
