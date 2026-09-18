# Cursor OTEL Gate-4 diag seventh static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen diag rows: 7
- Eighth item classified: NO
- Completed types.js source reread: NO
- Source executed: NO
- OTEL authority mutated: NO

## Seventh static item

- Kind: `STATIC_FUNCTION_BINDING`
- Boundary kind: `DECLARATION_BODY_END`
- Declaration prefix: `var`
- Binding: `a`
- Dependency module: `None`
- Initializer present: `True`
- Body offsets: 1547:3461
- Terminator offset: None
- Source SHA256: `882d1762e1fe2853ae4e21ebbb560874d88e091a87c4415ac92325aa3d068d43`
- Canonical row SHA256: `11404136848cfc6ee252624f4b29124011756e126ce389cc4e979ab328cf32ba`
- Source: `a=function(){function e(){function e(e){return function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];var s=(0,r.mS)("diag");if(s)return s[e].apply(s,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([],function(e,t){var n="function"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(t),!1))}}var t=this;t.setLogger=function(e,n){var s,i,a;if(void 0===n&&(n={logLevel:o.u.INFO}),e===t){var l=new Error("Cannot use diag as the logger for itself. Please use a DiagLogger implementation like ConsoleDiagLogger or a custom implementation");return t.error(null!==(s=l.stack)&&void 0!==s?s:l.message),!1}"number"==typeof n&&(n={logLevel:n});var u=(0,r.mS)("diag"),c=function(e,t){function n(n,r){var s=t[n];return"function"==typeof s&&e>=r?s.bind(t):function(){}}return e<o.u.NONE?e=o.u.NONE:e>o.u.ALL&&(e=o.u.ALL),t=t||{},{error:n("error",o.u.ERROR),warn:n("warn",o.u.WARN),info:n("info",o.u.INFO),debug:n("debug",o.u.DEBUG),verbose:n("verbose",o.u.VERBOSE)}}(null!==(i=n.logLevel)&&void 0!==i?i:o.u.INFO,e);if(u&&!n.suppressOverrideMessage){var d=null!==(a=(new Error).stack)&&void 0!==a?a:"<failed to generate stacktrace>";u.warn("Current logger will be overwritten from "+d),c.warn("Current logger will overwrite one already registered from "+d)}return(0,r.$G)("diag",c,t,!0)},t.disable=function(){(0,r.kv)("diag",t)},t.createComponentLogger=function(e){return new s(e)},t.verbose=e("verbose"),t.debug=e("debug"),t.info=e("info"),t.warn=e("warn"),t.error=e("error")}return e.instance=function(){return this._instance||(this._instance=new e),this._instance},e}()`

## Completed child prerequisite

- Completed diag/types.js state SHA256: `33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23`
- Child source reread: NO

## Classification evidence

Evidence SHA256: `adcbc46f37b63564273f99cc09528c8aa7166565e1f060432c1a2d4698905066`

```json
{"authorization_commit":"f1fe31b0d34666fdbce580e600a829a5c439459f","authorization_contract_sha256":"9bdbd82780febd834c630343dc8cbefde7e5999fef4b0cfdd36dfe57c67798d6","authorization_document_sha256":"233eb82f1fab54e2317158a06d741ba86c8f53353009865debae8ed4d0f66851","authorization_evidence_sha256":"a0877f3c0aaf9e7b1523f6f436e960984f832bde37ac0962c5959e1bac0bee2f","body_chars":3461,"body_end_reached":true,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_source_reread":false,"classification_count_this_gate":1,"cumulative_classified_rows":7,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","eighth_item_classified":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","row6_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","seventh_item":{"binding":"a","body_end_reached":true,"boundary_kind":"DECLARATION_BODY_END","declaration_prefix":"var","dependency_module":null,"end":3461,"initializer_present":true,"kind":"STATIC_FUNCTION_BINDING","ordinal":7,"source":"a=function(){function e(){function e(e){return function(){for(var t=[],n=0;n<arguments.length;n++)t[n]=arguments[n];var s=(0,r.mS)(\"diag\");if(s)return s[e].apply(s,function(e,t,n){if(n||2===arguments.length)for(var r,s=0,i=t.length;s<i;s++)!r&&s in t||(r||(r=Array.prototype.slice.call(t,0,s)),r[s]=t[s]);return e.concat(r||Array.prototype.slice.call(t))}([],function(e,t){var n=\"function\"==typeof Symbol&&e[Symbol.iterator];if(!n)return e;var r,s,i=n.call(e),o=[];try{for(;(void 0===t||t-- >0)&&!(r=i.next()).done;)o.push(r.value)}catch(e){s={error:e}}finally{try{r&&!r.done&&(n=i.return)&&n.call(i)}finally{if(s)throw s.error}}return o}(t),!1))}}var t=this;t.setLogger=function(e,n){var s,i,a;if(void 0===n&&(n={logLevel:o.u.INFO}),e===t){var l=new Error(\"Cannot use diag as the logger for itself. Please use a DiagLogger implementation like ConsoleDiagLogger or a custom implementation\");return t.error(null!==(s=l.stack)&&void 0!==s?s:l.message),!1}\"number\"==typeof n&&(n={logLevel:n});var u=(0,r.mS)(\"diag\"),c=function(e,t){function n(n,r){var s=t[n];return\"function\"==typeof s&&e>=r?s.bind(t):function(){}}return e<o.u.NONE?e=o.u.NONE:e>o.u.ALL&&(e=o.u.ALL),t=t||{},{error:n(\"error\",o.u.ERROR),warn:n(\"warn\",o.u.WARN),info:n(\"info\",o.u.INFO),debug:n(\"debug\",o.u.DEBUG),verbose:n(\"verbose\",o.u.VERBOSE)}}(null!==(i=n.logLevel)&&void 0!==i?i:o.u.INFO,e);if(u&&!n.suppressOverrideMessage){var d=null!==(a=(new Error).stack)&&void 0!==a?a:\"<failed to generate stacktrace>\";u.warn(\"Current logger will be overwritten from \"+d),c.warn(\"Current logger will overwrite one already registered from \"+d)}return(0,r.$G)(\"diag\",c,t,!0)},t.disable=function(){(0,r.kv)(\"diag\",t)},t.createComponentLogger=function(e){return new s(e)},t.verbose=e(\"verbose\"),t.debug=e(\"debug\"),t.info=e(\"info\"),t.warn=e(\"warn\"),t.error=e(\"error\")}return e.instance=function(){return this._instance||(this._instance=new e),this._instance},e}()","source_sha256":"882d1762e1fe2853ae4e21ebbb560874d88e091a87c4415ac92325aa3d068d43","start":1547,"terminator":null},"seventh_item_sha256":"11404136848cfc6ee252624f4b29124011756e126ce389cc4e979ab328cf32ba","source_executed":false,"version":"GATE4_DIAG_SEVENTH_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one inherited var declarator from the resumed diag.js parent frontier was classified. No eighth parent item was recovered or classified. The completed diag/types.js source was not reread. No JavaScript was executed and the OTEL authority was not mutated.
