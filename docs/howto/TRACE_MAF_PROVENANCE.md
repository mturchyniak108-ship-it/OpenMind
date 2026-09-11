# How to Trace MAF Provenance

MAF provenance should be followed from the artifact back to
its governing authority.

## Basic method

1. Identify the artifact path.
2. Identify its schema or protocol version.
3. Identify its Git commit and parent.
4. Verify any frozen SHA256 or Git blob identity.
5. Locate the governing preregistration/protocol.
6. Distinguish successful evidence from frozen failure or
   corrective evidence.
7. Preserve the original artifact identity.

## Important rule

Historical OpenMind paths and `openmind.*` schema identifiers
are provenance-bearing identifiers.

A future MAF-facing alias must not make the historical
identifier disappear from the evidence chain.
