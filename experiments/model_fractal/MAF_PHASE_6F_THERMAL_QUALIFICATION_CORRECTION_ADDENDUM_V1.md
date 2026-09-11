# Phase 6F Thermal-Qualification Correction Addendum V1

Addendum status: PRE-REPAIR / PRE-EXECUTION THERMAL-QUALIFICATION AUTHORITY

## 1. Scope

This addendum supplements the frozen Phase 6F V2 preregistration and its artifact-binding addendum.

It does not modify the Phase 6F scientific question, treatment, control, workload, timing boundary, trial count, pair order, correctness boundary, result path, sentinel path, or bounded claim.

Frozen Phase 6F V2 preregistration SHA256:

`b54009487a3668b1a81afa50f5ff1b46b8b3a8cdd878fff3d468e619eae42791`

Frozen artifact-binding addendum SHA256:

`79ae8028d8f1cfcbab7da3670c4e8637932707f46410f3fd7265bdc2e7133091`

## 2. Historical pre-sentinel execution evidence

The first frozen Phase 6F V2 runner identity was:

- Git-frozen HEAD: `972c29d07ac207148dc12213accfe65510e18de7`
- runner path: `experiments/model_fractal/maf_phase_6f_current_access_provisioning_performance_v2.py`
- runner SHA256: `89b1a5211685b70bf4967d8cbb7a195bb36d0113bea701cf1f667ff5596222a8`
- runner Git blob: `ec3acc058bc0208dc22895e30faf40c69baccdca`

One execution invocation reached the pre-run thermal/environment qualification gate and terminated there.

Observed execution state:

- runner return code: `1`;
- exact-once sentinel reserved: `NO`;
- Phase 6F result created: `NO`;
- correctness preflight executed: `NO`;
- warmup executed: `NO`;
- measured treatment/control trial executed: `NO`;
- model/performance evidence produced: `NO`.

The historical runner and its Git commit remain preserved evidence and MUST NOT be rewritten, amended, deleted, or represented as a successful Phase 6F execution.

Because the exact-once sentinel was not reserved, the Phase 6F execution slot was not spent.

## 3. Proven thermal-observation defect

The historical runner used:

`/sys/class/thermal/thermal_zone*/temp`

and defined the environmental maximum as the maximum normalized temperature over every readable thermal-zone `temp` value.

Subsequent read-only diagnosis observed:

- thermal-zone directories: `77`;
- readable temperatures: `77`;
- unreadable temperatures: `0`;
- abort threshold: `85.0 C`;
- zones at or above the abort threshold: `2`;
- non-trip zones at or above the abort threshold: `0`;
- all-zone maximum: `105.0 C`;
- observed non-trip maximum during the classification diagnostic: `48.4 C`.

The two threshold-dominating zones were:

1. `type = cpu-hw-trip-0`, `mode = disabled`, `temp = 105.0 C`;
2. `type = cpu-hw-trip-1`, `mode = disabled`, `temp = 105.0 C`.

Both expose `trip_point_*` metadata and were identified as disabled hardware-trip thermal zones.

This proves a runner thermal-sensor-population defect: the historical all-readable-zone maximum can treat disabled hardware-trip/threshold telemetry as if it were a live thermal observation.

This finding does NOT establish that the device was at 105 C during the failed invocation, because the failed pre-run snapshot was not published as a Phase 6F result.

It establishes that the frozen observation rule is not sufficiently qualified for this host and can fail because of non-live hardware-trip telemetry.

## 4. Preserved thermal safety threshold

The Phase 6F thermal abort threshold remains exactly:

`85.0 C`

This addendum does NOT authorize:

- increasing the threshold;
- weakening the thermal abort policy;
- discarding slow trials;
- selecting favorable trials;
- adaptive stopping;
- replacement trials.

The correction changes only the population from which the live environmental maximum is derived.

## 5. Qualified live thermal-zone rule

A future repaired Phase 6F runner MUST continue to enumerate the available:

`/sys/class/thermal/thermal_zone*`

entries and MUST preserve every readable zone in thermal evidence.

For each readable zone the runner MUST record, at minimum:

- thermal-zone name;
- zone `type` when readable;
- zone `mode` when readable;
- raw `temp`;
- source unit;
- normalized Celsius value;
- live-observation eligibility;
- exclusion reason when ineligible.

A readable zone is excluded from the live maximum only when BOTH are true:

1. its normalized `type` contains the substring `hw-trip`; and
2. its normalized `mode` is exactly `disabled`.

Such a zone MUST remain present in the recorded thermal snapshot with:

`live_observation_eligible = false`

and exclusion reason:

`disabled_hw_trip_zone`

Every other readable thermal zone remains eligible for the live environmental maximum.

The runner MUST fail closed if zero live-observation-eligible zones remain.

The qualified environmental maximum is:

`maximum(normalized_celsius for live_observation_eligible zones)`

Execution is thermally acceptable only when:

1. at least one live-observation-eligible zone exists;
2. the qualified maximum is present; and
3. the qualified maximum is strictly less than `85.0 C`.

## 6. Evidence-preservation rule

Excluded disabled hardware-trip zones MUST NOT be hidden or discarded from telemetry.

The result must preserve:

- complete readable-zone records;
- eligible-zone count;
- excluded-zone count;
- excluded-zone names/types/modes/reasons;
- all-readable-zone maximum;
- qualified live-zone maximum;
- unchanged abort threshold.

This distinction is governance evidence only.

It MUST NOT be used to select, remove, replace, or rescue individual performance trials.

## 7. Snapshot schedule remains unchanged

The Phase 6F thermal/environment schedule remains the frozen V2 schedule:

- pre-run snapshot;
- snapshots around measured work as qualified by the runner design;
- post-run snapshot.

If the qualified live environment becomes unacceptable, the run MUST stop according to the frozen fail-closed policy.

No slow trial may be selectively discarded and continued.

## 8. CPU topology, rotation, affinity, and multithreading boundary

This correction addendum does NOT change CPU execution topology.

It does NOT authorize:

- CPU affinity changes;
- CPU-core rotation;
- workload migration policy;
- thread-count changes;
- multithreading experiments;
- NEON optimization;
- Vulkan/GPU execution.

Prior CPU-role and thermal experiments remain separate historical methodology evidence.

Phase 6F V2 continues to characterize the already-frozen current access/provisioning path only.

CPU topology and multithreaded scaling remain separate successor optimization experiments and MUST NOT be introduced as part of this thermal correction.

## 9. Runner-repair boundary

This addendum does not itself modify the frozen historical runner.

A future runner repair, if separately authorized, MUST be minimal and limited to implementing the thermal qualification defined here plus any directly necessary result-schema evidence for that qualification.

The repaired runner MUST preserve all unrelated frozen Phase 6F semantics.

The repaired runner MUST receive a new source SHA256 and Git blob identity.

The historical runner SHA256 `89b1a5211685b70bf4967d8cbb7a195bb36d0113bea701cf1f667ff5596222a8` remains historical evidence and MUST NOT be reused as the repaired-runner identity.

## 10. Execution boundary

Construction or Git freeze of this correction addendum does NOT authorize execution.

After this addendum is separately validated and frozen, the required successor gates remain:

1. separately authorize the minimal runner thermal repair;
2. statically validate the repaired runner;
3. separately freeze the repaired runner in Git;
4. perform a new read-only execution-authority preflight;
5. separately authorize a new execution attempt.

No execution may occur before those gates pass.

## 11. Result and sentinel continuity

The bound Phase 6F result path remains:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/result.json`

The bound exact-once sentinel path remains:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/.spent`

Both are absent at construction of this addendum.

The historical pre-sentinel failed invocation does not consume the exact-once slot.

A future authorized runner must still fail closed if either path exists before sentinel reservation.

## 12. Provenance rule

The final Phase 6F evidence chain MUST distinguish:

- frozen V2 preregistration;
- original artifact-binding addendum;
- historical runner identity;
- pre-sentinel thermal-qualification failure;
- this thermal-qualification correction addendum;
- later repaired runner identity;
- later execution result, if one is validly produced.

No later successful result may erase or rewrite the historical pre-sentinel failure.

## 13. Narrow correction claim

This addendum establishes only that Phase 6F thermal qualification on this host must distinguish disabled `hw-trip` threshold telemetry from live thermal observations before deriving the environmental maximum.

It does not establish:

- treatment superiority;
- latency improvement;
- memory improvement;
- energy improvement;
- CPU-topology superiority;
- multithreading benefit;
- NEON benefit;
- Vulkan benefit;
- MAF-native compute benefit.

End of Phase 6F Thermal-Qualification Correction Addendum V1.
