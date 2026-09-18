# Cursor / OTEL Gate 4 — proto3 function dollar frontier 17045 diagnostic — Gold Standard V2

## Frozen source

- Source HEAD: `c2c5e766b21ce0cc0db2732128a0b5f2298ec719`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Function dollar start: `16793`
- Function dollar close: `17369`
- Nested function start: `16970`
- Nested function body start: `16988`
- Nested function close: `17101`

## Coordinate 17045

- Character JSON: `"["`
- Character ordinal: `91`
- Token: `"["`
- Classification: `EXACT_DESTRUCTURING_OPEN_CANDIDATE`
- Candidate count through frontier: `1`
- Exact candidate at target: `[{"coordinate": 17045, "char": "[", "declaration_kind": "let", "keyword_coordinate": 17042, "paren_depth": 0, "bracket_depth": 0, "block_depth": 0}]`
- Nearest candidate: `{"coordinate": 17045, "char": "[", "declaration_kind": "let", "keyword_coordinate": 17042, "paren_depth": 0, "bracket_depth": 0, "block_depth": 0}`
- Declaration snapshot: `{"coordinate": 17045, "char": "[", "paren_depth": 0, "bracket_depth": 0, "block_depth": 0, "declaration": {"kind": "let", "keyword_coordinate": 17042, "state": "EXPECT_BINDING", "paren_depth": 0, "bracket_depth": 0, "block_depth": 0}, "previous_significant": "t"}`

## Source context

- Context range: `16988–17101`
- Context SHA256: `9ffaa8aa2a5e97343585ccb93b299413295baa8d6dd3ccc15e4831fa3905dcb6`
- Before JSON: `"if(!r.length)return;e.tag(n,O.LengthDelimited).fork();let"`
- After JSON: `"[,s]=X(t);for(let t=0;t<r.length;t++)e[s](r[t]);e.join()"`
- Full context JSON: `"if(!r.length)return;e.tag(n,O.LengthDelimited).fork();let[,s]=X(t);for(let t=0;t<r.length;t++)e[s](r[t]);e.join()"`

## Recent parser events

`[{"coordinate": 17042, "event": "DECLARATION_KEYWORD", "token": "let", "paren_depth": 0, "bracket_depth": 0, "block_depth": 0}, {"coordinate": 17045, "event": "DESTRUCTURING_CANDIDATE", "char": "[", "declaration_kind": "let"}]`

## Diagnostic authority

- Diagnostic SHA256: `bd711d64e154c2cb75b758ba7ae777d4a166a4b66fcd946c1086ac72ccafdfef`

## Authorization boundary

- Frozen static source read: `AUTHORIZED AND PERFORMED`
- Parser state reconstruction: `AUTHORIZED AND PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify the exact destructuring pattern opening at proto3 body coordinate 17045 using the recovered declaration state and pattern token.
