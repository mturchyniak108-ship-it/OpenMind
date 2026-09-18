# Cursor / OTEL Gate 4 — proto3 function x n9186 declaration grammar audit — Gold Standard V2

## Source authority

- Source HEAD: `be578174d6f1bc45b40f33ec2006d413fa7315bb`
- Source tree: `9ade1a3591eee2b31758de27971634dceb85cae3`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_FUNCTION_X_INNER_N_DECLARATION_FRONTIER_GSV2_2026-09-17.md`
- Prior document SHA256: `d12224f4ff846449af8d69a1ae3c634ab2a0607c23b3a30eb5b92f0e09b1634f`
- Prior evidence SHA256: `3a75947747c99ee0da960bd1fe16a99bfc9b8faeb3fe26cac688537e0c395b07`
- Prior binding authority SHA256: `c3e8a310f6e93e72dff65bc38092520f5e1a2c67024c782251d84d336b8ef7fe`

## Exact declaration grammar

- Declaration keyword: `const`
- Declaration coordinate: `9147`
- Pattern source: `[t,n]`
- Pattern SHA256: `2b17f8a45fe7a1ca4879aaa6a6b6c9ca91640b55cc20a259d50f74008c0dfc94`
- Token immediately after pattern: `of`
- Token kind: `IDENT`
- Token coordinate: `9157`
- Active for-header at declaration: `true`
- Active for-header open: `9146`
- Active for-header close: `9161`
- Grammar classification: `FOR_OF_LEXICAL_DECLARATION`
- n@9186 relative region: `FOR_RIGHT_HAND_EXPRESSION_OR_HEADER`
- Top-level commas before n@9186: `[]`
- Top-level semicolons before n@9186: `[]`
- Newlines before n@9186: `[]`
- Grammar authority SHA256: `258f519deb4b0f775e78053584598d644f0e38892a4f899d1f8ef42e7e5ac2c5`

## Frozen source windows

- Main window: `9100–9245`
- Main window SHA256: `8e81f773073c52c68fefd1de8aebc9d49ae6d07a427d936934096a587700f6cc`
- Main window JSON: `"t.entries(t);switch(e.V.kind){case\"scalar\":for(const[t,n]of i)s[t.toString()]=L(e.V.T,n);break;case\"message\":for(const[e,t]of i)s[e.toString()]=t"`
- Target window: `9129–9257`
- Target window SHA256: `69f51f1935ed1ae248b657e62403b392d1db3692c40434f46eaf4d3b21999739`
- Target window JSON: `"{case\"scalar\":for(const[t,n]of i)s[t.toString()]=L(e.V.T,n);break;case\"message\":for(const[e,t]of i)s[e.toString()]=t.toJson(n);b"`

No ownership assertion for n@9186 beyond this exact grammar classification is made by this audit.

## Canonical evidence SHA256

`38d55171cbaed7f553952193a3cec26502cb0c64a6661e9744ae6749f41a79dc`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Exact source-window freeze: `AUTHORIZED AND PERFORMED`
- Declaration grammar classification: `AUTHORIZED AND PERFORMED`
- Reference qualification after n@9186: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Use the frozen exact source grammar to replace the simplistic declaration-state assumption, classify n@9186 authoritatively, and resume the large recursive ownership macro without redoing completed work.
