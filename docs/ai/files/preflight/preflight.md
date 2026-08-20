# preflight/preflight.sh

## Purpose

Performs the initial OpenMind environment readiness check.

It verifies that required commands, packages, directories, and basic system capabilities are available before development or benchmarking begins.

## Architectural Role

This script is the first environment validation layer.

It should be run before attempting native builds, Vulkan diagnostics, model inference, or large knowledge-processing workloads.

## Responsibilities

- Check required command-line tools.
- Check required development packages.
- Check SQLite availability.
- Inspect basic system information.
- Record environment information.
- Produce a reproducible preflight report.

## Usage

Run from the repository root:

cd ~/OpenMind
bash preflight/preflight.sh

The generated report is stored in:

preflight/report.txt

## Required Tooling

The current environment checks include tools such as:

- git
- python
- curl
- wget
- jq
- sqlite3
- clang
- cmake
- ninja
- make
- pkg-config

The exact requirements are defined by the script and should be treated as the authoritative source.

## SQLite

SQLite is currently available in the development environment.

Its presence supports lightweight local persistence and future graph/index experiments.

It does not establish SQLite as the final OpenMind vector database.

The roadmap requires benchmarking SQLite-backed storage against specialized vector/index structures.

## Agent Workflow

Recommended order:

preflight -> resource_profile -> Vulkan probe -> build -> smoke test -> CTest -> benchmark

If preflight fails, resolve the environment problem before changing application code.
