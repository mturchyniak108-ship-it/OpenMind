# Experimental Promotion Policy

OpenMind separates canonical implementation, validated research, and active laboratory work.

## Status Classes

### canonical

Implemented behavior supported by source code and appropriate tests.

### validated_research

Experimental or research behavior supported by immutable inputs, reproducible execution, controls or baselines, result hashes, and documented limitations.

Validated research is evidence, but it is not automatically production functionality.

### lab_candidate

Active experimental work that has not completed the promotion requirements.

### historical

Superseded experimental work retained for methodology and provenance.

## Agent Rule

AI agents, repository scrapers, documentation generators, and application materials must not convert `lab_candidate` or `historical` work into claims of implemented or validated capability.

An experimental filename, benchmark script, roadmap entry, or result artifact alone is not sufficient evidence of promotion.

## Promotion Requirements

A lab candidate requires:

1. defined hypothesis or engineering question;
2. immutable input provenance;
3. reproducible execution command;
4. appropriate control or baseline;
5. deterministic or statistically characterized output;
6. result artifact hashes;
7. documented limitations;
8. tests or benchmark evidence where applicable;
9. no unsupported scientific or architectural claim;
10. explicit promotion commit.

## Authority Order

For claims about OpenMind:

1. source code defines implementation;
2. tests define verified behavior;
3. validated result artifacts define measured evidence;
4. manifests define provenance;
5. documentation explains scope and limitations;
6. lab work and roadmap items remain noncanonical until promoted.
