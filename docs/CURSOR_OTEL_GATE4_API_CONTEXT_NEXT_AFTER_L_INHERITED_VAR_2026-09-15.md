# Cursor OTEL Gate-4 api context next inherited var after l

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Additional item classified: NO
- Completed diag source reread: NO
- Source executed: NO
- OTEL authority mutated: NO

## Classified item

- Sequence role: `NEXT_AFTER_CONTEXT_BINDING_L`
- Kind: `STATIC_FUNCTION_BINDING`
- Boundary kind: `DECLARATION_BODY_END`
- Declaration prefix: `var`
- Binding: `u`
- Dependency module: `None`
- Initializer present: `True`
- Body offsets: 1216:2365
- Terminator offset: None
- Source SHA256: `d4d365601fc083152d6263c5455c21ca92fcc7afcb4242a440f833fa82a966ef`
- Canonical row SHA256: `bebedf0bb38b789d0a6e78a841cd741ff945a1070f43f7c6cbaa432a72eab1c9`
- Source: `u=function(){function e(){}return e.getInstance=function(){return this._instance||(this._instance=new e),this._instance},e.prototype.setGlobalContextManager=function(e){return(0,i.$G)(a,e,o.K.instance())},e.prototype.active=function(){return this._getContextManager().active()},e.prototype.with=function(e,t,n){for(var r,s=[],i=3;i<arguments.length;i++)s[i-3]=arguments[i];return(r=this._getContextManager()).with.apply(r,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([e,t,n],function(e,t){var n="function"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(s),!1))},e.prototype.bind=function(e,t){return this._getContextManager().bind(e,t)},e.prototype._getContextManager=function(){return(0,i.mS)(a)||l},e.prototype.disable=function(){this._getContextManager().disable(),(0,i.kv)(a,o.K.instance())},e}()`

## Classification evidence

Evidence SHA256: `cceee0466675d49dce54a0fa7beec4764359d5c26b02f299a89fe69d8648c59d`

```json
{"authorization_commit":"4c95b3426e64a0133a13674ce0db869b4638ac1e","authorization_contract_sha256":"575e38d7ac535f501e46a17c95c9601e2231459f69bbe9108f3d758e95edff78","authorization_document_sha256":"80175dbf449b3719780a002dea47920493eb69b1faa2adc0fe62414759af9cc2","authorization_evidence_sha256":"65ae4fae02e5438ec9c6d5166a6f463a751b74a1ba115b313c6c6dc519cb3de3","body_chars":2365,"body_end_reached":true,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","classification_count_this_gate":1,"completed_diag_source_reread":false,"completed_diag_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","next_additional_item_classified":false,"next_item":{"binding":"u","body_end_reached":true,"boundary_kind":"DECLARATION_BODY_END","declaration_prefix":"var","dependency_module":null,"end":2365,"initializer_present":true,"kind":"STATIC_FUNCTION_BINDING","sequence_role":"NEXT_AFTER_CONTEXT_BINDING_L","source":"u=function(){function e(){}return e.getInstance=function(){return this._instance||(this._instance=new e),this._instance},e.prototype.setGlobalContextManager=function(e){return(0,i.$G)(a,e,o.K.instance())},e.prototype.active=function(){return this._getContextManager().active()},e.prototype.with=function(e,t,n){for(var r,s=[],i=3;i<arguments.length;i++)s[i-3]=arguments[i];return(r=this._getContextManager()).with.apply(r,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([e,t,n],function(e,t){var n=\"function\"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(s),!1))},e.prototype.bind=function(e,t){return this._getContextManager().bind(e,t)},e.prototype._getContextManager=function(){return(0,i.mS)(a)||l},e.prototype.disable=function(){this._getContextManager().disable(),(0,i.kv)(a,o.K.instance())},e}()","source_sha256":"d4d365601fc083152d6263c5455c21ca92fcc7afcb4242a440f833fa82a966ef","start":1216,"terminator":null},"next_item_sha256":"bebedf0bb38b789d0a6e78a841cd741ff945a1070f43f7c6cbaa432a72eab1c9","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","previous_row_sha256":"0b96fb7f6596f33758dc5b6d2b4c20d5e4e9c77e727428ebe51efd97566888c0","source_executed":false,"version":"GATE4_API_CONTEXT_NEXT_AFTER_L_INHERITED_VAR_V1"}
```

## Strict boundary

Exactly one inherited var declarator after frozen binding l was classified. No additional api/context item was recovered or classified. Completed diag source was not reread. No JavaScript was executed and the OTEL authority was not mutated.
