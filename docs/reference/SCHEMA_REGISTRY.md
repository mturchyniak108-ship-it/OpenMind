# MAF Schema Registry

This document is the human-facing entry point for schema
compatibility.

It does not redefine frozen schemas.

## Discovery baseline

The post-Phase-6 documentation audit found:

- 231 distinct `openmind.*` schema identifiers in scanned
  repository text;
- 6 schema identifiers appearing in frozen-provenance
  surfaces;
- 181 appearing in historical-research surfaces;
- 52 appearing in active-rebrand candidate surfaces.

A schema may appear in more than one role.

## Policy

Existing schema identifiers remain authoritative for the
artifacts that use them.

Do not replace an `openmind.*` schema identifier merely to
align naming with MAF.

## Future registry fields

A fully enumerated machine-derived registry should eventually
record:

- schema identifier;
- version;
- defining path;
- historical/current status;
- frozen status;
- readers/writers;
- compatibility aliases;
- successor schema, if any;
- migration policy;
- deprecation policy.

## Compatibility requirement

Any new MAF schema namespace must be introduced as a
versioned successor, never as an in-place mutation of frozen
evidence.
