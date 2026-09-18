# MAF Object Model

This document provides a conceptual reference for MAF object
relationships.

Frozen protocol versions remain authoritative for exact
serialized representations.

## Model object

A MAF object is an addressable model-related object governed
by explicit identity and provenance rules.

## Identity

Identity must be stable enough to distinguish an object from
its physical placement.

Moving data between storage locations must not silently
redefine the logical object.

## Addressing

MAF separates logical object identity/addressing from the
physical location used to retrieve serialized payload data.

## Tensor relationship

MAF research includes tensor ↔ object relationships that
allow model tensors or tensor fragments to be associated with
persistent object identities.

## Segment relationship

Serialized objects may reside in segments.

Segment placement is a storage concern and does not by itself
define the logical identity of the object.

## Provenance

Provenance records where an object/payload came from and what
authority governs its interpretation.

## Reconstruction

Reconstruction is the process of recovering the required
model-facing representation from governed MAF object/payload
data.

## PK

PK is an established MAF identifier/addressing term used by
the existing catalog, selection and resident-directory work.

This post-Phase-6 reference does not rewrite the exact
semantics frozen by earlier protocols.

## Fail-closed rule

If identity, authority, provenance, version, or reconstruction
requirements cannot be established, the operation must not
silently assume validity.
