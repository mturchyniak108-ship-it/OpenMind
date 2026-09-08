# OpenMind Compatibility

MAF documentation uses the successor project identity while
preserving compatibility-bearing OpenMind identifiers.

## Compatibility surfaces

Current discovery identified OpenMind-era naming in:

- Python package/import paths;
- native include paths and symbols;
- tests;
- CLI surfaces;
- documentation;
- configuration/manifests;
- schema identifiers;
- repository and remote names.

## Schema rule

Existing `openmind.*` schema identifiers are not cosmetic
strings.

Historical and frozen data may depend on them.

They must not be bulk-renamed.

A successor namespace, if introduced, requires:

1. a versioned compatibility contract;
2. explicit reader behavior;
3. migration rules;
4. backward-compatibility tests;
5. provenance preservation;
6. rollback criteria.

## Package rule

The existing `openmind` Python package remains unchanged
until a package/API migration is separately designed and
authorized.

## Native rule

Existing native OpenMind include and symbol surfaces remain
unchanged until a native API migration is separately designed
and authorized.

## Repository rule

Repository/remote naming is a publication operation and is
separate from documentation terminology.
