# Cursor OTEL Gate-4 diag.js fifth static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 5
- Sixth item classified: NO
- Source executed: NO
- OTEL authority mutated: NO

## Fifth static item

- Kind: `FUNCTION_DECLARATION_CREATION`
- Boundary kind: `FUNCTION_DECLARATION_END`
- Declaration prefix: `None`
- Binding: `i`
- Dependency module: `None`
- Body offsets: 868:1430
- Terminator offset: 1429
- Source SHA256: `c73b0d45bea2bbad245cba2d9ebe66d893d4c8f4d89ef132c744e4dfec6fd26c`
- Canonical row SHA256: `fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283`
- Source: `function i(e,t,n){var s=(0,r.mS)("diag");if(s)return n.unshift(t),s[e].apply(s,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([],function(e,t){var n="function"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(n),!1))}`

## Evidence

Evidence SHA256: `abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b`

```json
{"authorization_commit":"faf93cf5d94395e2d52c908bca3f216efbffd00b","authorization_contract_sha256":"e9ee8cbddd413427e6b8cd53b60b0fa50ac2cb2b0eeecaee5a6d4f79e02a4fec","authorization_document_sha256":"3d9e33bb83ca1bc64e9e6e9567da22f368eed28a2a428256ad8b048f31081055","authorization_evidence_sha256":"cc195cac85bcd690d358b01462898e7c13408a2715b1438ef816a8c9a9dcd5d4","body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","classification_count_this_gate":1,"completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","cumulative_classified_rows":5,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","fifth_item":{"binding":"i","boundary_kind":"FUNCTION_DECLARATION_END","declaration_prefix":null,"dependency_module":null,"end":1430,"kind":"FUNCTION_DECLARATION_CREATION","ordinal":5,"source":"function i(e,t,n){var s=(0,r.mS)(\"diag\");if(s)return n.unshift(t),s[e].apply(s,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([],function(e,t){var n=\"function\"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(n),!1))}","source_sha256":"c73b0d45bea2bbad245cba2d9ebe66d893d4c8f4d89ef132c744e4dfec6fd26c","start":868,"terminator":1429},"fifth_item_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283","fourth_row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","sixth_item_classified":false,"source_executed":false,"version":"GATE4_DIAG_FIFTH_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one declaration-aware diag.js static item was classified. A function or class declaration was bounded at its structural closing brace when applicable. A multi-declarator variable declaration was limited to its first declarator when applicable. No sixth item was classified. No JavaScript was executed and no OTEL authority state was mutated.
