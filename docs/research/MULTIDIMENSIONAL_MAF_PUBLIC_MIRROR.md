# Multidimensional MAF Public Research Mirror

This branch is a publication snapshot of OpenMind's local
multidimensional-MAF research.

## Canonical lineage

- Canonical local branch: `labs/multidimensional-maf`
- Canonical local HEAD: `620d13747e34c637afbda029fd0857541e1d5536`
- Public mirror branch: `research/multidimensional-maf-public`
- Public mirror base: `origin/main@aa17ed954b07372d321b280b4bc7449869fefd52`

The canonical local research history is intentionally **not rewritten**
to satisfy hosting limits. This public branch is therefore a derived
publication snapshot rather than a byte-identical Git-history mirror.

## Excluded heavyweight benchmark

The following reproducible result is intentionally not stored in normal
Git on this branch:

- Path: `experiments/model_fractal/maf_segment_reader_benchmark_v1_2.json`
- Size: `323334664` bytes
- Reference SHA256: `44b15ba5a02492f9a7c79cda3120c0cb4b6b398201eacb5f5249f38a281e5a54`
- Canonical Git blob: `efaa5121816581ffa59937b2e45d63f5a1326801`
- Canonical introducing commit: `a524d71d46090a42a7ac6b69582ca79ca699e65f`

The exact path is listed in `.gitignore`.

## Reproduce locally

1. Clone OpenMind and check out `research/multidimensional-maf-public`.
2. Install the runtime/model prerequisites required by:
   `experiments/model_fractal/MAF_SEGMENT_READER_BENCHMARK_V1_2_PROTOCOL.md`.
3. Obtain the required model/data locally. Large model files remain
   outside Git.
4. Follow the frozen V1.2 benchmark protocol exactly.
5. Generate `experiments/model_fractal/maf_segment_reader_benchmark_v1_2.json` locally.
6. Confirm the output remains ignored by Git.
7. In the frozen reference environment, compare the generated artifact
   with the reference metadata in `experiments/model_fractal/MAF_PUBLICATION_MIRROR_MANIFEST_V1.json`. Where platform
   differences are permitted by the protocol, compare the
   protocol-defined scientific fields rather than assuming a
   cross-platform byte-identical result.


Tracked candidate runner(s) associated with the V1.2 benchmark:

- `experiments/model_fractal/benchmark_maf_segment_reader_v1_2.py`

Use the exact invocation and prerequisites defined by the frozen protocol.

## Frozen-byte policy

Historical whitespace in frozen evidence and source is preserved rather
than silently normalized by the publication process. The exact known
`git diff --check` exceptions are recorded in the publication manifest.

Any **new** whitespace exception blocks future mirror publication.

## Promotion policy

This research branch does not modify `main`. Stable documentation or
implementation should be promoted later through a separate integration
branch/review after its scientific dependency gates are satisfied.

## Download frozen reference evidence

The frozen V1.2 benchmark payload is available as a GitHub Release asset so
the exact reference evidence can be inspected without placing the 308 MiB raw
JSON object in normal Git history.

- Release: `openmind-maf-segment-reader-benchmark-v1.2-artifact`
- Release URL: https://github.com/mturchyniak108-ship-it/OpenMind/releases/tag/openmind-maf-segment-reader-benchmark-v1.2-artifact
- Release target commit: `5c50452b200e78f0864fa72e2e5cf0c78bde1c55`
- Compressed asset: `maf_segment_reader_benchmark_v1_2.json.gz`
- Compressed bytes: `4546962`
- Compressed SHA256: `9bf27fcefbed59d8f372dd18e0b31b547f3ba8fd94556ea9f4b6fbc729f12fc2`
- Frozen raw bytes after decompression: `323334664`
- Frozen raw SHA256 after decompression: `44b15ba5a02492f9a7c79cda3120c0cb4b6b398201eacb5f5249f38a281e5a54`

GitHub CLI download:

    gh release download openmind-maf-segment-reader-benchmark-v1.2-artifact --repo mturchyniak108-ship-it/OpenMind --pattern 'maf_segment_reader_benchmark_v1_2.json.gz'

Verification:

    sha256sum maf_segment_reader_benchmark_v1_2.json.gz
    gzip -dc maf_segment_reader_benchmark_v1_2.json.gz > maf_segment_reader_benchmark_v1_2.json
    sha256sum maf_segment_reader_benchmark_v1_2.json

Researchers may download the frozen reference evidence or independently
reproduce the benchmark using the frozen protocol and runner.
