# MAF Activation V1.1 Corrective Protocol

Status: Preregistered Phase 6B.7 corrective research protocol.

## 1. Purpose

This protocol defines the narrow additive correction required before
Activation V1 may be validated as enforcing the frozen catalog rule:

    only a completely validated candidate generation may be activated

The frozen Activation V1 protocol remains historical evidence.

The frozen Activation V1 implementation remains historical evidence.

Neither artifact is rewritten.

Activation V1.1 corrects only the enforceable candidate-eligibility
boundary.

## 2. Historical V1 boundary

Frozen Activation V1 protocol:

    experiments/model_fractal/
    MAF_ACTIVATION_V1_PROTOCOL.md

Frozen Activation V1 implementation:

    experiments/model_fractal/
    maf_activation_v1.py

Frozen implementation SHA256:

    76d79f90d9bc30118a6dfe0297beacd9
    b323aed9f56876881f653a2c01c1f210

No activate_generation call was executed before discovery of the
corrective requirement.

No Activation V1 validation runner or raw result was frozen.

Therefore V1 remains preserved as an unexecuted reference implementation,
not as validated activation evidence.

## 3. Gap discovered before validation-runner freeze

Generation Engine V1:

    verify_manifest(...)

validates canonical generation structure and identity.

It does not independently reopen adopted segment bytes.

A structurally valid synthetic manifest can therefore reproduce a valid:

    generation_pk

without the physical segment or object evidence existing.

Frozen Activation V1 delegates candidate acceptance to verify_manifest.

It consequently cannot, by itself, enforce the stronger catalog
precondition that the generation currently corresponds to validated
physical MAF evidence.

This is the V1 corrective gap.

## 4. Correction type

The correction is additive.

Activation V1.1 must not:

- rewrite Activation V1 history;
- rewrite Generation Engine V1;
- change generation identity semantics;
- add physical paths to generation identity;
- add physical paths to active authority bytes;
- claim unverifiable historical provenance.

Instead V1.1 establishes current physical validity immediately before
the authority transition.

## 5. Current-validity boundary

Activation V1.1 defines an eligible activation target as one for which:

1. the candidate manifest is canonical and structurally valid;
2. the candidate generation_pk is valid;
3. every descriptor segment is mapped to current physical evidence;
4. the frozen Generation Engine reconstructs the candidate descriptor
   from that physical evidence;
5. the reconstructed descriptor exactly equals the candidate descriptor;
6. reconstructed canonical descriptor bytes exactly equal candidate
   canonical descriptor bytes;
7. reconstructed generation_pk exactly equals the requested and candidate
   generation_pk;
8. all required checks complete before the active-authority commit point.

This is an enforceable current-validity rule.

It is not a claim about unverifiable historical execution provenance.

## 6. Frozen reconstruction evidence

The read-only Phase 6B.7c3 audit demonstrated that the frozen known-good
candidate can be independently reconstructed from current physical MAF
evidence using:

    maf_generation_engine_v1.build_descriptor(...)

The reconstruction produced:

    descriptor exact = true
    canonical descriptor bytes exact = true
    generation_pk exact = true

No physical path entered descriptor identity.

This establishes that the corrective mechanism is compatible with the
already frozen generation identity.

## 7. V1.1 implementation target

The additive reference implementation must be:

    experiments/model_fractal/
    maf_activation_v1_1.py

Activation V1 remains unchanged.

## 8. V1.1 validation target

The preregistered validation runner must be:

    experiments/model_fractal/
    maf_activation_validation_v1_1.py

Expected raw result:

    experiments/model_fractal/
    maf_activation_validation_v1_1.json

Expected runtime:

    results/runtime/
    maf_activation_validation_v1_1

The runner and implementation must be frozen before validation execution.

The raw result must be frozen before interpretation.

## 9. Activation request

Activation V1.1 must accept at minimum:

    model_pk
    generation_pk
    candidate_manifest_path
    active_record_path
    segment_paths

where:

    segment_paths

is execution metadata mapping each canonical descriptor:

    segment_id

to one physical segment path.

The path mapping is not authority identity.

## 10. Exact segment-mapping rule

Let the candidate descriptor contain the set:

    descriptor_segment_ids

The supplied mapping must satisfy:

    set(segment_paths) == descriptor_segment_ids

No required segment may be absent.

No extra segment mapping may be accepted.

Each segment_id must resolve to exactly one supplied physical path.

The mapping itself must not enter:

- generation_pk;
- generation manifest bytes;
- active authority record bytes.

## 11. Candidate canonical verification

Before physical reconstruction, V1.1 must independently:

- require the candidate manifest to be a regular file;
- read exact candidate manifest bytes;
- decode valid JSON;
- call the frozen Generation Engine V1 verify_manifest contract;
- require canonical persisted bytes;
- verify requested model_pk;
- verify requested generation_pk.

Failure must occur before authority mutation.

## 12. Physical segment reconstruction inputs

For every descriptor segment, V1.1 must construct Generation Engine input
evidence using:

    segment_path
    segment_length
    segment_sha256

The path comes only from caller-supplied execution metadata.

The declared length and SHA256 come only from the immutable candidate
descriptor.

V1.1 must not allow the supplied path metadata to replace descriptor
integrity values.

## 13. Physical object reconstruction inputs

For every descriptor object, V1.1 must reconstruct Generation Engine
object-placement input using:

    model_pk
    object_pk
    segment_path
    offset
    length
    object_file_sha256
    payload_sha256

The segment path is resolved from:

    object.segment_id
        ->
    segment_paths[segment_id]

All other fields come from the immutable candidate descriptor.

## 14. Frozen Generation Engine reuse

V1.1 must call:

    maf_generation_engine_v1.build_descriptor(...)

for physical reconstruction.

It must not duplicate or fork Generation Engine normalization rules.

This reuses the frozen checks for:

- segment regular-file existence;
- segment length;
- segment SHA256;
- canonical segment normalization;
- object placement bounds;
- object byte-range SHA256;
- canonical object ordering;
- generation descriptor construction;
- generation_pk derivation.

## 15. Payload-hash claim boundary

Generation Engine V1 validates the format and preservation of:

    payload_sha256

but its build_descriptor physical reconstruction does not independently
derive payload_sha256 from raw segment bytes.

Activation V1.1 therefore must not claim that it independently recomputes
payload_sha256 during activation eligibility validation.

V1.1 preserves that field exactly as frozen generation evidence.

Any stronger payload-specific revalidation requires separately frozen
evidence.

## 16. Descriptor equivalence requirement

The return from:

    build_descriptor(...)

must provide a reconstructed descriptor.

V1.1 must require:

    reconstructed_descriptor
        ==
    candidate_manifest.descriptor

Structural similarity is insufficient.

The full normalized dictionaries must be equal.

## 17. Canonical-byte equivalence

V1.1 must independently canonicalize both descriptors using the frozen
Generation Engine canonical JSON convention.

It must require:

    canonical(reconstructed_descriptor)
        ==
    canonical(candidate_descriptor)

This makes the equivalence requirement byte-reproducible.

## 18. Generation identity equivalence

The generation_pk returned by frozen Generation Engine reconstruction must
equal:

    candidate manifest generation_pk
    requested generation_pk

The descriptor SHA256 returned by reconstruction must correspond exactly
to the reconstructed canonical descriptor bytes.

Activation must fail closed on any mismatch.

## 19. Physical substitution rejection

A supplied physical segment must be rejected if its current:

- existence;
- regular-file status;
- length;
- SHA256;

does not match the immutable candidate descriptor.

A different file with identical required bytes remains equivalent physical
evidence because physical filesystem path is not identity.

## 20. Object-range rejection

Every descriptor object must resolve through its declared segment_id.

The exact current physical byte range at:

    offset
    length

must reproduce:

    object_file_sha256

under the frozen Generation Engine rules.

A mismatch must fail before active-authority replacement.

## 21. Synthetic-manifest rejection

A canonical generation manifest whose segment/object integrity values are
syntactically valid but have no matching current physical evidence must
not be activatable under V1.1.

This is a required negative control.

Possession of canonical JSON alone is not sufficient activation
eligibility evidence.

## 22. Manifest-path independence

candidate_manifest_path is execution metadata.

segment_paths is execution metadata.

active_record_path is execution metadata.

None may enter:

- model_pk;
- object_pk;
- generation_pk;
- generation manifest identity;
- active-record canonical fields.

## 23. Active authority record

V1.1 retains the V1 canonical authority record unchanged:

    schema
    active_generation_version
    model_pk
    generation_pk
    generation_manifest_sha256

No segment path or manifest path is added.

The active-record schema remains:

    openmind.maf_active_generation.v1

The active-record version remains:

    maf_active_generation_v1

The corrective change concerns activation eligibility, not active-record
identity.

## 24. Manifest integrity binding

After successful physical reconstruction, the active record continues to
bind the exact canonical candidate manifest bytes through:

    generation_manifest_sha256

Physical path metadata is not included in this digest beyond whatever
immutable generation content is already represented in the manifest.

## 25. Atomicity boundary

All V1.1 candidate and physical reconstruction checks must complete before
the authority linearization point.

The research file implementation may retain:

    sibling .partial
        ->
    fsync
        ->
    os.replace

as the authority-transition mechanism.

The successful os.replace remains the single authority commit point.

## 26. Failed activation

Any failure before os.replace must leave the previously valid active
record byte-for-byte unchanged.

A failed first activation must leave no completed active record.

Partial cleanup is permitted.

No generation, segment, object, descriptor, or candidate manifest may be
modified by failure handling.

## 27. Idempotence

Same-generation reactivation remains idempotent only after V1.1 has
revalidated the target's current physical evidence.

An existing identical active record must not allow physical validation to
be skipped.

If current physical evidence no longer reconstructs the active
generation, reactivation must fail closed rather than return success
solely from record equality.

## 28. Replacement activation

Replacement:

    active generation A
        ->
    candidate generation B

must first establish V1.1 current physical validity for B.

Only then may the new active record be prepared and atomically replace A.

Failure before the commit point must preserve A exactly.

## 29. Existing-active validation

V1.1 retains V1's requirement that an existing active record be canonical
and model-consistent before replacement.

Corrupted authority state must not be silently overwritten.

## 30. Old generation boundary

V1.1 current physical reconstruction is required for the target being
activated.

V1.1 does not delete the previously active generation.

V1.1 does not implement retirement.

V1.1 does not implement rollback.

## 31. Source-GGUF independence

V1.1 must not require source GGUF access.

Physical reconstruction uses MAF segment evidence only.

The implementation and runner must not derive activation truth by:

- opening source GGUF;
- reading source GGUF;
- hashing source GGUF;
- statting source GGUF;
- resolving a source-GGUF path.

## 32. Storage-engine neutrality

V1.1 selects no production catalog storage engine.

It must not add:

- SQLite;
- mmap;
- MAFDB;
- a compiled catalog requirement.

The canonical file authority record remains a correctness research
mechanism only.

## 33. Compute boundary

V1.1 must not:

- perform inference;
- enable MAF-native computation;
- load tensors for compute;
- allocate Vulkan resources;
- construct dense compute views;
- populate the resident PK directory.

Activation changes authority only.

## 34. Concurrency claim boundary

V1.1 establishes physical validity during the single-process reference
activation operation.

It does not by itself establish hostile or concurrent external mutation
safety between validation and the authority commit point.

Multi-writer locking and adversarial concurrent filesystem mutation remain
outside the V1.1 claim unless separately validated.

Immutable-segment semantics remain a prerequisite of the MAF storage
model.

## 35. Positive validation requirements

The V1.1 runner must establish at minimum:

- known-good physical evidence reconstructs the candidate descriptor;
- reconstructed descriptor equals candidate descriptor;
- reconstructed canonical bytes equal candidate descriptor bytes;
- reconstructed generation_pk equals candidate generation_pk;
- first activation succeeds;
- exact five-field active record;
- exact model_pk;
- exact generation_pk;
- exact generation_manifest_sha256;
- independent active-record reopen;
- candidate manifest path absent from authority bytes;
- segment physical paths absent from authority bytes;
- same-generation reactivation revalidates physical evidence;
- valid same-generation reactivation is idempotent;
- idempotent authority bytes remain unchanged;
- replacement activation A -> B succeeds;
- old candidate evidence remains unchanged;
- new candidate evidence remains unchanged;
- logical PKs remain unchanged;
- source GGUF is not required.

## 36. Required corrective negative controls

V1.1 validation must fail closed for at least:

- missing candidate manifest;
- malformed candidate JSON;
- invalid candidate manifest schema;
- invalid candidate manifest version;
- malformed requested model_pk;
- malformed requested generation_pk;
- requested model_pk mismatch;
- requested generation_pk mismatch;
- generation_pk derivation mismatch;
- missing segment_paths mapping;
- missing descriptor segment mapping;
- extra descriptor segment mapping;
- mapped segment path missing;
- mapped segment not a regular file;
- mapped segment length mismatch;
- mapped segment SHA256 mismatch;
- object byte-range SHA256 mismatch;
- synthetic canonical manifest without matching physical evidence;
- malformed existing active record;
- cross-model existing active record;
- pre-existing partial active target;
- injected failure before os.replace.

## 37. Synthetic-manifest mandatory control

The runner must construct or supply a canonical manifest that passes:

    generation.verify_manifest(...)

while lacking matching physical MAF evidence.

V1.1 activation must reject it before authority mutation.

This control directly tests the corrective gap discovered before runner
freeze.

## 38. Physical-mutation control

The runner must establish a valid candidate against controlled physical
evidence, then alter or substitute the physical evidence before activation.

Activation V1.1 must reject the target.

No active authority transition may occur.

The test must not mutate the repository's frozen source evidence.

Controlled copies must be used.

## 39. Segment-mapping permutation boundary

For a multi-segment controlled candidate, mapping dictionary iteration
order must not affect reconstructed generation identity.

Mapping a segment_id to the wrong physical content must fail closed.

Correct segment_id-to-content association must be determined by immutable
descriptor integrity, not caller order.

## 40. Fault-injection boundary

The runner may replace or intercept:

    os.replace

only inside the controlled validation process to demonstrate pre-commit
failure behavior.

No test-only failure API is required in the production V1.1 activation
module.

The failed replacement must preserve old active bytes exactly.

## 41. Static policy controls

The runner must establish that V1.1:

- leaves Activation V1 unchanged;
- leaves Generation Engine V1 unchanged;
- reuses Generation Engine build_descriptor;
- does not implement rollback;
- does not delete generations;
- does not select SQLite;
- does not select mmap;
- does not enable MAF-native compute;
- does not perform inference;
- contains no source-GGUF operational dependency;
- contains no physical path field in active authority.

## 42. Aggregate rule

The raw V1.1 activation result may record:

    all_pass = true

only when every required:

- positive control;
- corrective physical-validity control;
- negative control;
- atomicity control;
- integrity control;
- static policy control;
- scope-boundary control;

passes.

No failed control may be hidden by aggregate success.

## 43. Freeze order

The required order is:

    frozen Activation V1 history
        ->
    frozen Activation V1.1 corrective protocol
        ->
    implement Activation V1.1
        ->
    preregister/freeze V1.1 validation runner
        ->
    freeze implementation and runner
        ->
    execute frozen runner exactly once
        ->
    freeze raw result
        ->
    interpret
        ->
    document Phase 6B.7 result

No V1.1 activation execution may occur before the implementation and
runner are frozen.

## 44. Historical-evidence rule

Activation V1 remains frozen at its existing commit and SHA.

Its provenance gap is not erased.

V1.1 is an additive correction discovered before V1 activation execution
or validation-runner freeze.

A future V1.1 pass must not retroactively label V1 as validated.

## 45. Phase boundary

Freezing this corrective protocol does not complete Phase 6B.7.

Phase 6B.7 remains:

    Atomic activation — INCOMPLETE / CURRENT

The next controlled action after this protocol freeze is:

    implement Activation V1.1 only

The validation runner follows in a separate freeze stage.

Rollback remains:

    Phase 6B.8 — NOT STARTED

## 46. Nonclaims

This protocol alone does not establish:

- corrected activation implementation;
- executed activation;
- validated atomic authority replacement;
- historical provenance receipts;
- concurrent mutation safety;
- multi-writer safety;
- rollback;
- retirement;
- production catalog storage;
- resident-directory performance;
- inference-hot-path lookup;
- MAF-native compute;
- Vulkan execution.

## 47. Corrective invariant summary

Activation eligibility becomes:

    canonical candidate manifest
        +
    exact segment_id -> physical path execution mapping
        +
    frozen Generation Engine physical reconstruction
        +
    exact descriptor equality
        +
    exact generation_pk equality
        =
    currently valid activation target

while:

    physical paths remain execution metadata
    generation identity remains unchanged
    active-record schema remains unchanged
    generation manifests remain immutable
    segment/object bytes remain immutable
    all eligibility checks precede os.replace
    failed pre-commit activation preserves prior authority
    source GGUF remains unnecessary
    rollback remains separate
