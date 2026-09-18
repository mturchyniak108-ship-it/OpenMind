# OpenMind MAF Query-to-PK Selection Validation V1.4 — Authoritative Verdict

## Verdict

**PASS — authoritative Q2 V1.4 query-to-PK selection validation.**

The frozen V1.4 exact-once execution completed successfully and durably published its final result. All 74 preregistered checks passed in their exact frozen order.

- `all_pass`: `true`
- `failed_checks`: `[]`
- `auditor_error`: `null`
- check count: `74 / 74 PASS`
- exact-once namespace: `PERMANENTLY SPENT`
- scientific retry: `FORBIDDEN`

## Frozen authority bindings

- V1.4 protocol SHA256: `a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699`
- V1.4 runner SHA256: `7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030`
- authoritative result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- permanent slot journal SHA256: `0545bba0abcf73e5235d639b0d4390a1e3c01011b1ff0cc9d0372eaf5eb8716a`
- prepared journal record SHA256: `ced2fd836aa80f28ff072d03df2cc07a3f39de48b111aec60b5c5431edfb0e96`
- reserved-durable journal record SHA256: `0e7ed4793613c3600e9cda0e3a62930e40e4a2d10ee67149fa0a014029cabe64`

## Durable publication proof

The permanent slot journal contains exactly three records in the required order:

1. `RESERVATION_PREPARED`
2. `RESERVED_DURABLE`
3. `PUBLISHED_DURABLE`

The reserved record binds the prepared record hash. The published record binds the reserved-durable record hash and the final result SHA256. The partial publication file is absent and the final result is present.

## V01–V74

Every frozen validation check from `V01_v1_protocol_binding` through `V74_result_binds_validation_runner_sha256` is present exactly once, in the frozen runner order, with `passed: true`.

## Authoritative metrics

```json
{
  "budget_violation_count": 0,
  "duplicate_selection_count": 0,
  "evaluation_query_count": 40,
  "fallback_query_count": 8,
  "generation_binding_violation_count": 0,
  "manifest_binding_violation_count": 0,
  "maximum_selected_candidate_count": 4,
  "mean_selected_candidate_count": 1.925,
  "metadata_eligible_query_count": 32,
  "oracle_input_violation_count": 0,
  "random_baseline_top1_accuracy": 0.041666666666666664,
  "selector_minus_baseline_top1_difference": 0.9583333333333334,
  "specific_intent_query_count": 24,
  "specific_intent_top1_accuracy": 1.0,
  "supported_intent_precision": 1.0,
  "supported_intent_target_hit_rate": 1.0,
  "unique_expected_object_pk_count": 12
}
```

The acceptance decision is determined by the frozen V01–V74 checks and thresholds encoded by the V1.4 runner and protocol. This verdict does not introduce new thresholds or reinterpret the preregistered acceptance rule.

## Post-run forensic correction

A separate post-run shell auditor initially emitted `POST_SLOT_FAILURE_NAMESPACE_SPENT_NO_RETRY` because that auditor incorrectly assumed that the result `checks` field was a dictionary. The frozen V1.4 result schema actually represents `checks` as a 74-entry list of objects with `id`, `passed`, and `detail`.

That shell-auditor classification was not produced by the V1.4 runner and is superseded by the forensic audit:

- runner return code: `0`
- runner output: `ALL_PASS=True`
- runner output: `FAILED_CHECKS=[]`
- authoritative result: `all_pass: true`
- authoritative result: `failed_checks: []`
- exact V01–V74 order: `PASS`
- all 74 check values: `PASS`
- permanent journal hash chain: `PASS`

Therefore the authoritative scientific classification is **PASS**, not post-slot failure.

## Claim boundary

This result validates the frozen **Q2 query-to-PK selection experiment only**.

It does **not** establish inference, answer generation, selective working-set sufficiency, tensor/object avoidance, output parity, answer quality, performance superiority, MAF-native compute, or replacement of a conventional LLM.

## Final disposition

Q2 V1.4 is complete.

The result and permanent slot journal are authoritative and must not be regenerated. The V1.4 namespace is permanently spent and the experiment must not be rerun.
