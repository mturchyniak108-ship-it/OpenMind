# Cursor OTEL Gate-4 local-worker destructuring n at 11639

Date: 2026-09-15

## Status

- target destructuring declaration characterized: YES
- binding identifiers enumerated: YES
- immediate lexical block recorded: YES
- dependency recursion performed: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `bc7923b3f93de7de15f06a033cb33f48576812777bffa76a3259a6fdf259cdc9`

```json
{"immediate_block":{"end":11896,"open":11575,"start":11576},"module":"../local-worker/dist/index.js","record_sha256":"37c6490d700381266b16041a5c312bec7f042c2180813a708e47f3d21d31cdff","row":{"binding_identifiers":["n","r"],"declaration_end":11788,"declaration_kind":"const","declaration_start":11634,"declarator_end":11788,"declarator_raw":"{promise:n,timer:r}=function(e){let t=()=>{};const n=new Promise((e=>{t=e})),r=new T(e,t);return r.delay(),{promise:n,timer:r}}(this.debounceTimeout)","declarator_sha256":"af65323bcb0f81eea62dd23af863e246186f7767bc5d93c140bfb0638932af33","declarator_start":11639,"lhs_masked":"{promise:n,timer:r}","lhs_raw":"{promise:n,timer:r}","lhs_sha256":"00d570c660bd65bba618bf5df90833b1e7af49cc2bbf7aa64bd6da1bc1ca0851","n_binding_count":1,"rhs_raw":"function(e){let t=()=>{};const n=new Promise((e=>{t=e})),r=new T(e,t);return r.delay(),{promise:n,timer:r}}(this.debounceTimeout)"},"source_window":{"end":12159,"sha256":"d2f1ee8ccbabb6e7c134338b18bbd61485cc7b33ef2d66d01def9daf0e8dc02b","start":11459,"text":"onnection.onNotification(I.PublishDiagnosticsNotification.type,this.onDiagnostics.bind(this))}getDiagnosticsEntry(e){const t=this.diagnosticsMap.get(e);if(void 0!==t)return t;const{promise:n,timer:r}=function(e){let t=()=>{};const n=new Promise((e=>{t=e})),r=new T(e,t);return r.delay(),{promise:n,timer:r}}(this.debounceTimeout);r.delay();const s={diagnostics:[],debounceTimer:r,debouncePromise:n};return this.diagnosticsMap.set(e,s),s}onDiagnostics(e){const t=this.getDiagnosticsEntry(e.uri);t.diagnostics=e.diagnostics,t.debounceTimer.delay()}open(e,t){return k(this,void 0,void 0,(function*(){const n=yield f.promises.readFile(t.toPath(),\"utf8\"),r={uri:t.toString(),languageId:this.getLanguageId("},"target_offset":11639,"version":"GATE4_LOCAL_WORKER_DESTRUCTURING_N_11639_CHARACTERIZATION_V1"}
```

## Evidence

Evidence SHA256: `3333f46f6da683983f9ffca121df123b8bbedcfbc3d7a90308fe7cb496daddbc`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"bc7923b3f93de7de15f06a033cb33f48576812777bffa76a3259a6fdf259cdc9","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_recursion_performed":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"n_binding_count":1,"version":"GATE4_LOCAL_WORKER_DESTRUCTURING_N_11639_CHARACTERIZATION_EVIDENCE_V1"}
```

## Boundary

This authority resolves only the first genuine destructuring binding containing n encountered at local-worker body offset 11639. The left-hand binding pattern is separated from its initializer and recursively enumerated for bound identifiers. No complete-scope rerun or dependency recursion occurs in this block.
