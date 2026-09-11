# MAF Phase 6F Current Access / Provisioning Performance Preregistration V2

Protocol status: CONSTRUCTION-ONLY PREREGISTRATION  
Scientific branch authority: `labs/multidimensional-maf`  
Scientific HEAD at construction authorization: `35d9bf7e0f0a364929a139feda952e084edf5fc1`  
Workflow: `OPENMIND / GOLD STANDARD V2`

## 1. Supersession and provenance

This V2 protocol supersedes one planned but never-materialized V1 preconstruction identity.

Aborted/unrecoverable planned V1 evidence:

- Intended path: `experiments/model_fractal/MAF_PHASE_6F_CURRENT_ACCESS_PROVISIONING_PERFORMANCE_PREREGISTRATION_V1.md`
- Frozen planned bytes: `21633`
- Frozen planned SHA-256: `46c15687a53aded95679bd25753348a4484c33ce9728859641e6b35c0ba22566`
- Repository materialization: `NO`
- Persisted shell-history recovery: `FAILED`
- Live Bash-history recovery: `FAILED`
- Status: `ABORTED / UNRECOVERABLE PRECONSTRUCTION IDENTITY`

V2 does not claim byte continuity with V1. V1 remains frozen historical evidence of an attempted preconstruction payload identity and must not be silently recreated, reassigned, or reported as constructed.

## 2. Authorization boundary

This protocol construction authorizes one V2 Markdown protocol file and static validation only.

NO BENCHMARK EXECUTION AUTHORIZED.

Not authorized by this protocol construction:

- runner creation or runner execution;
- source GGUF or MAF payload open/read/hash/scan/mmap;
- model loading, inference, token generation, or prompt decode;
- sentinel reservation;
- result creation;
- Git stage, commit, push, reset, rebase, branch switch, or history rewrite;
- native MAFDB construction;
- ARM64/NEON optimization;
- Vulkan optimization;
- GPT-OSS execution;
- external collaboration work.

Any later action requires its own explicit authorization and gate.

## 3. Scientific purpose

Phase 6F follows the closed Phase 6E-D correctness result. Its purpose is performance characterization after correctness, not a new correctness claim.

The first benchmark question is:

> Under one frozen Qwen-based workload and correctness boundary, what measurable cost/benefit does the current persistent MAF access/provisioning path have versus the frozen reference path in elapsed time, serialized I/O, and peak/working memory?

This V2 is a baseline-characterization preregistration. It does not preregister a superiority claim.

## 4. Correctness authority from Phase 6E-D

Phase 6E-D is CLOSED — PASS under its pinned runtime, fixed prompt, and fixed single-decode procedure.

The spent Phase 6E-D exact-once runner MUST NOT be rerun for Phase 6F.

The bounded inherited correctness claim is only:

> Under the pinned runtime, fixed prompt and fixed single-decode procedure, the 339-tensor MAF-loaded model produced identical tokenization and numerically equivalent full-vocabulary last-prompt-token logits to the original GGUF control.

Phase 6F must not broaden that statement into claims about general prompts, models, hardware, native MAF compute, zero-copy compute, or performance advantage.

## 5. Frozen treatment identity

Treatment is the current persistent 339-tensor MAF provisioning path built from the qualified Phase 6E-D components.

Treatment authority includes:

- provider: `experiments/model_fractal/maf_phase_6e_d_class_a_maf_backed_tensor_provider_v1.py`
- resident directory: `experiments/model_fractal/maf_resident_pk_directory_v1.py`
- segment reader: `experiments/model_fractal/maf_segment_reader_v1.py`
- model PK: `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- generation PK: `mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`
- segment: `results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg`
- segment bytes: `1888934699`
- tensor count: `339`

No reconstructed complete GGUF and no source-GGUF fallback are allowed in the treatment arm.

## 6. Frozen control identity

Control is the original conventional GGUF reference path:

`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Frozen control metadata:

- bytes: `1894532160`
- SHA-256: `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

During later authorized execution, the control arm must use the intended conventional loader and must not use the MAF provider path.

## 7. Runtime and device boundary

The runtime reference remains the pinned Phase 6E-D llama.cpp lineage and Vulkan configuration already qualified for correctness.

Device boundary:

- Samsung Galaxy S26 Ultra SM-S948W
- Android 16
- Adreno 840
- Vulkan / Mesa Turnip environment used by the qualified runtime

The existing Vulkan backend is a frozen runtime component for this baseline. This protocol does not authorize new Vulkan optimization.

## 8. Prompt and inference configuration

Use the same Phase 6E-D prompt:

`OpenMind MAF parity probe.\nGiven integers 17 and 25, compute their sum and explain the result in one sentence.`

Frozen prompt metadata:

- UTF-8 bytes: `110`
- SHA-256: `a79091472f58689a015e1e38947f9713fb9542211db99d2c911e41d58b40acfd`

Tokenization/configuration boundary:

- add_special: false
- parse_special: false
- no template
- no explicit BOS/EOS
- requested n_ctx: 128
- requested n_batch: 128
- requested n_ubatch: 128
- n_seq_max: 1
- threads: 1
- threads_batch: 1
- no generation
- no sampling

The previously explained internal llama.cpp context padding to 256 is permitted if the same pinned runtime behavior remains in both arms.

## 9. Benchmark unit and primary metric

Primary metric: `model_ready_elapsed_ns`.

Timing source: `time.perf_counter_ns()`.

Treatment timing interval starts immediately before MAF provider/model construction that populates the pinned model and stops when the model handle is ready for context creation.

Control timing interval starts immediately before conventional GGUF model load and stops when the model handle is ready for context creation.

The primary timing interval excludes:

- Python or child-process startup;
- argument parsing;
- result serialization;
- context creation;
- tokenization;
- prompt decode;
- correctness comparison;
- cleanup after the model-ready boundary.

## 10. Process isolation

Every warmup, correctness arm, and measured trial must run in a fresh child process.

The parent process must not retain a loaded treatment or control model between trials.

Fresh-process isolation is part of the preregistered benchmark design and may not be removed after observing results.

## 11. Cache and residency regime

Cache regime identifier: `BALANCED_NATURAL_CACHE_V1`.

This protocol makes no true-cold-cache claim and does not authorize privileged kernel cache dropping.

Before measured trials:

1. run one untimed treatment warmup in a fresh child and fully release it;
2. run one untimed control warmup in a fresh child and fully release it.

The benchmark must describe the regime as balanced natural cache/residency, not as controlled physical cold-cache I/O.

## 12. Measured trial count and order

Exactly `10` measured treatment trials and exactly `10` measured control trials are required.

Total measured trials: `20`.

Pair order is frozen:

1. T -> C
2. C -> T
3. T -> C
4. C -> T
5. T -> C
6. C -> T
7. T -> C
8. C -> T
9. T -> C
10. C -> T

No adaptive stopping is allowed.

No replacement trials are allowed.

A slow trial, failed trial, or timeout must not be silently discarded and replaced.

## 13. Failure, timeout, retry, and outlier policy

The future runner must preregister explicit timeout behavior before execution.

Measured-trial failures must be preserved in raw trial evidence.

There is no automatic whole-run retry after exact-once execution authority is spent.

There is no outlier deletion based on observed performance.

Any excluded event must be governed by a predeclared non-performance reason and preserved in evidence; otherwise the run disposition is invalid.

## 14. Thermal and environment policy

The future runner must bind a statically qualified thermal observation method before execution.

Required:

- pre-run thermal/environment snapshot;
- snapshots around measured work as qualified by the runner design;
- post-run snapshot;
- explicit acceptable/abort threshold policy established before execution.

If the environment becomes unacceptable, stop according to the preregistered rule. Do not discard only slow trials and continue.

Thermal handling is governance, not a mechanism for selecting favorable measurements.

## 15. Host-process memory measurement

Primary host-process memory surfaces:

- `VmRSS`
- `VmHWM`

Capture the relevant before/after process values for each child where applicable.

`VmHWM` is the primary process peak-memory evidence.

Python `tracemalloc`, if used at all, is supplemental and must not be presented as total process or system memory.

No GPU-memory or total-system-memory claim is allowed unless a separately qualified measurement surface is added before execution.

## 16. I/O and page-fault measurement

Observable host-process I/O surfaces:

- `/proc/self/io`
- `ru_minflt`
- `ru_majflt`

Where available, `/proc/self/io` fields include:

- rchar
- wchar
- syscr
- syscw
- read_bytes
- write_bytes

Treatment may additionally report logical payload/copy/resolution/reader counters when already exposed by qualified components.

These measurements must not be described as exact physical-storage I/O. Page faults and `/proc/self/io` are observable process/kernel counters only.

## 17. Correctness preflight

Before any measured trials, run a new Phase 6F correctness preflight using fresh treatment and control children.

Do not invoke the spent Phase 6E-D runner.

Preflight must use the frozen prompt/configuration and full-vocabulary last-prompt-token logits.

Required conditions:

- treatment/control tokenization exact;
- token count 28 / 28;
- vocab size 151936 in both arms;
- all compared logits finite;
- tolerance: `abs(T-C) <= 1e-5 + 1e-5*abs(C)`;
- tolerance failures: 0;
- same argmax;
- equal top-10 token-ID order;
- treatment MAF backend copies: 339;
- treatment prohibited source-GGUF opens: 0;
- control uses intended conventional loader;
- no generation.

If correctness preflight fails, measured trials must not begin.

## 18. Correctness postflight

After the complete measured trial set, run the same Phase 6F correctness guard again in fresh treatment and control children.

If postflight fails:

- preserve all raw measurements;
- disposition the benchmark as INVALID;
- do not rerun the whole benchmark to repair the outcome;
- do not substitute the spent Phase 6E-D result for the failed postflight.

Correctness preflight and correctness postflight are both mandatory.

## 19. Statistics and raw evidence

Preserve every raw measured trial.

For each arm report at minimum:

- count
- minimum
- maximum
- mean
- median
- nearest-rank p95

For `model_ready_elapsed_ns` additionally report:

- treatment median;
- control median;
- absolute median delta;
- treatment/control median ratio;
- paired trial ratios using the frozen pair order.

No directional p-value threshold or post-hoc significance gate is preregistered.

A valid result is baseline characterization, not proof of superiority.

## 20. Result schema and disposition

The future immutable machine-readable result must contain:

- scientific/repository identity;
- runtime/device/config identity;
- treatment/control identities;
- cache/warmup/trial-order contract;
- correctness preflight;
- every raw measured trial;
- elapsed-time aggregates;
- memory observations;
- I/O/page-fault observations;
- thermal/environment observations;
- correctness postflight;
- governance/failure evidence;
- final disposition.

Allowed successful disposition:

`VALID - BASELINE CHARACTERIZATION COMPLETE`

Invalid dispositions must distinguish at least:

- correctness preflight failure;
- measurement failure;
- correctness postflight failure;
- governance failure;
- thermal/environment failure;
- other fatal failure.

`VALID` does not mean treatment superiority.

## 21. Exact-once execution and sentinel

Future execution must be separately authorized.

Future sentinel path:

`results/runtime/maf_phase_6f_current_access_provisioning_performance_v2/.spent`

Do not reserve the sentinel during protocol construction, static validation, protocol freeze, or runner construction.

When execution is later authorized, reserve the sentinel immediately before the first authorized GGUF/MAF/model payload access.

After reservation, the benchmark is spent. No automatic whole-run rerun and no replacement trials are permitted.

## 22. Historical benchmark methodology relationship

PF07/PF08 statically qualified prior benchmark families as methodology evidence.

Historical benchmark results remain historical evidence and must not be substituted for this V2 measurement.

Useful inherited methodological features include:

- high-resolution monotonic timing;
- explicit warmups;
- fixed repetition counts;
- raw-trial preservation;
- median/p95-style summaries;
- seeded randomness where randomness exists;
- process/resource counters;
- correctness guards;
- thermal observation where qualified.

V2 is not a rerun of those historical benchmark protocols.

## 23. MAFDB, native, ARM64, Vulkan, and GPT-OSS boundaries

MAFDB is not preselected.

Potential storage/control-plane candidates may include:

- binary/RAM index plus external segments;
- SQLite control plane plus external MAF segments;
- a purpose-built MAFDB;
- another measured embedded engine.

Any MAFDB must earn promotion through reproducible MAF-specific advantage.

Native progression remains:

`Python research -> validated component -> native C++ -> ARM64/NEON -> Vulkan`

Vulkan optimization is not justified merely to compensate for an inferior storage or representation architecture.

GPT-OSS-20B remains prospective and excluded from this benchmark. It requires a separate correctness, memory, and execution gate.

## 24. Interpretation limits and next optimization gate

This benchmark may characterize the current treatment/control baseline in:

- model-ready elapsed time;
- observable host-process memory;
- observable serialized/process I/O and page faults.

It must not claim:

- general MAF superiority;
- native MAF compute;
- zero-copy compute;
- universal low-RAM advantage;
- energy advantage without a qualified energy surface;
- cross-device generality;
- cross-model generality.

After a valid result is frozen, a separate read-only interpretation gate must decide the next optimization target from the measured bottleneck.

## 25. Lifecycle and authorization sequence

The required lifecycle is:

1. construct this V2 protocol;
2. static-validate the protocol;
3. separately authorize protocol stage/commit freeze;
4. perform read-only runner design;
5. separately authorize runner construction;
6. static-validate the runner;
7. separately authorize runner stage/commit freeze;
8. separately authorize exact-once execution, including any required GGUF/MAF/model payload access;
9. qualify the immutable result;
10. separately authorize result stage/commit freeze;
11. interpret only frozen evidence;
12. authorize any successor optimization separately.

Construction does not imply execution.
Validation does not imply stage/commit.
Commit does not imply push.
A valid benchmark does not imply a superiority claim.

End of Phase 6F Current Access / Provisioning Performance Preregistration V2.
