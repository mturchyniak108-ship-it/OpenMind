# Phase 6F Current Access / Provisioning Performance — Artifact Binding Addendum V1

Addendum status: PRE-EXECUTION ARTIFACT-BINDING AUTHORITY

## 1. Scope

This addendum supplements, and does not modify or supersede, the frozen Phase 6F V2 preregistration protocol:

`experiments/model_fractal/MAF_PHASE_6F_CURRENT_ACCESS_PROVISIONING_PERFORMANCE_PREREGISTRATION_V2.md`

Frozen protocol authority:

- branch: `labs/multidimensional-maf`
- protocol-freeze commit: `44297c04f940148106aebbbd340b53a3d1a2c23a`
- protocol bytes: `15471`
- protocol SHA256: `b54009487a3668b1a81afa50f5ff1b46b8b3a8cdd878fff3d468e619eae42791`
- protocol Git blob: `330835bfef439392b153e97ad118aa2da50ebeab`

The sole purpose of this addendum is to bind exact future artifact identities that V2 left unnamed.

## 2. Binding authority

The Phase 6F V2 future runner source path is exactly:

`experiments/model_fractal/maf_phase_6f_current_access_provisioning_performance_v2.py`

The Phase 6F V2 immutable machine-readable result path is exactly:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/result.json`

The Phase 6F V2 exact-once sentinel path remains exactly the already-preregistered V2 path:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/.spent`

These three identities are authoritative only after this addendum itself is statically validated and separately frozen in Git.

## 3. No semantic modification

This addendum introduces no change to any Phase 6F V2 scientific or operational rule.

It does not change:

- the research question;
- treatment or control semantics;
- the 339-tensor treatment boundary;
- the conventional GGUF reference/control boundary;
- the fixed prompt or correctness boundary;
- correctness preflight or postflight requirements;
- `BALANCED_NATURAL_CACHE_V1`;
- fresh-child process isolation;
- one untimed warmup per arm;
- exactly 10 measured treatment trials;
- exactly 10 measured control trials;
- the derived total of 20 measured trials;
- alternating-pair order;
- `model_ready_elapsed_ns` as the primary metric;
- `time.perf_counter_ns()` timing;
- VmRSS or VmHWM measurement;
- `/proc/self/io` measurement;
- `ru_minflt` or `ru_majflt` page-fault measurement;
- raw-trial retention;
- aggregate-statistic requirements;
- timeout qualification;
- thermal-observation qualification;
- no-adaptive-stopping policy;
- no-replacement-trial policy;
- exact-once execution policy;
- result validity/disposition rules;
- bounded-claim policy;
- MAFDB exclusion/not-preselection;
- GPT-OSS prospective-only status;
- native C++ / ARM64 / NEON / Vulkan roadmap boundaries.

If any future runner or result conflicts with frozen V2, frozen V2 controls and the conflicting artifact is invalid.

## 4. Authorization boundaries

Construction or freeze of this addendum does not authorize any successor action.

In particular, this addendum does not authorize:

- runner construction;
- runner execution;
- result creation;
- sentinel reservation or creation;
- benchmark execution;
- source GGUF open/read/hash;
- MAF model or segment payload access;
- repository-module imports that may initialize model/native runtimes;
- llama/native runtime initialization;
- GPU or Vulkan initialization;
- inference;
- Git staging or commit of the future runner;
- Git staging or commit of the future result;
- Git fetch;
- Git push;
- Phase 6F publication.

Runner construction, runner freeze, execution, result qualification, result freeze, and publication remain separate authorization gates.

## 5. Historical V1 provenance

The earlier planned V1 preregistration identity remains historical evidence only:

- planned path: `experiments/model_fractal/MAF_PHASE_6F_CURRENT_ACCESS_PROVISIONING_PERFORMANCE_PREREGISTRATION_V1.md`
- planned bytes: `21633`
- planned SHA256: `46c15687a53aded95679bd25753348a4484c33ce9728859641e6b35c0ba22566`
- status: `ABORTED / UNRECOVERABLE PRECONSTRUCTION`
- materialized: `NO`

This addendum does not reconstruct, repair, or supersede that historical V1 identity.

## 6. Fail-closed rule

Before runner construction, the frozen V2 protocol identity and the frozen identity of this addendum must both be proven exact.

If the addendum is absent, modified, ambiguous, or not frozen, runner construction must not begin.

If any of the three bound artifact paths differs from this addendum, fail closed.

## 7. Bound artifact summary

Runner:

`experiments/model_fractal/maf_phase_6f_current_access_provisioning_performance_v2.py`

Result:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/result.json`

Sentinel:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/.spent`

End of Phase 6F Artifact Binding Addendum V1.
