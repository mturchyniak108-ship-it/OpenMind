# Cursor OTEL Gate-4 diag.js fourth static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 4
- Fifth item classified: NO
- Global-utils source reread: NO
- Source executed: NO
- OTEL authority mutated: NO

## Fourth static item

- Kind: `STATIC_FUNCTION_BINDING`
- Boundary kind: `DECLARATION_STATEMENT_END`
- Binding: `s`
- Dependency module: `None`
- Body offsets: 158:867
- Terminator offset: 867
- Source SHA256: `3f28234a0e2aacda1136fcbb7a7a5d3f8b56efca4282f3ea0d6d66fa660ece4c`
- Canonical row SHA256: `0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d`
- Source: `s=function(){function e(e){this._namespace=e.namespace||"DiagComponentLogger"}return e.prototype.debug=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i("debug",this._namespace,e)},e.prototype.error=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i("error",this._namespace,e)},e.prototype.info=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i("info",this._namespace,e)},e.prototype.warn=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i("warn",this._namespace,e)},e.prototype.verbose=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i("verbose",this._namespace,e)},e}()`

## Evidence

Evidence SHA256: `8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81`

```json
{"authorization_commit":"94fbff0cf3c518431b10286fcd9ffd869ebd81d6","authorization_contract_sha256":"fc9d64d7818f61515aff374c331f843522834fe51db7a894e36645e720c818c8","authorization_document_sha256":"57fc590630365ae42cd608f66d8a53de1244b6e82577aa39f96ad3ffe236797f","authorization_evidence_sha256":"8ebc4e5186bc525fe70ebbe8f6ad45883629b1809bef823af53391f80901b5a7","body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","classification_count_this_gate":1,"completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","cumulative_classified_rows":4,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","fifth_item_classified":false,"fourth_item":{"binding":"s","boundary_kind":"DECLARATION_STATEMENT_END","dependency_module":null,"end":867,"kind":"STATIC_FUNCTION_BINDING","ordinal":4,"source":"s=function(){function e(e){this._namespace=e.namespace||\"DiagComponentLogger\"}return e.prototype.debug=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i(\"debug\",this._namespace,e)},e.prototype.error=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i(\"error\",this._namespace,e)},e.prototype.info=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i(\"info\",this._namespace,e)},e.prototype.warn=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i(\"warn\",this._namespace,e)},e.prototype.verbose=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return i(\"verbose\",this._namespace,e)},e}()","source_sha256":"3f28234a0e2aacda1136fcbb7a7a5d3f8b56efca4282f3ea0d6d66fa660ece4c","start":158,"terminator":867},"fourth_item_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_executed":false,"version":"GATE4_DIAG_FOURTH_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one declarator after the completed global-utils dependency boundary was classified. No fifth item was recovered or classified. The completed global-utils source was not reread. No JavaScript was executed and no OTEL authority state was mutated.
