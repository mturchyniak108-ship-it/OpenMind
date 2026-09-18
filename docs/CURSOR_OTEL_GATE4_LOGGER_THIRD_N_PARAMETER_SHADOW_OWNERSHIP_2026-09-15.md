# Cursor OTEL Gate-4 logger third n parameter shadow ownership

Date: 2026-09-15

## Status

- third logger binding hazard qualified: YES
- hazard start: 1716
- binding kind: function parameter
- inside first qualified shadow: YES
- inside second qualified shadow: NO
- targets webpack header n: NO
- logger child recursion performed: NO
- logger complete: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `be03782de1b123bf6e08760b995cb13bab0f7166a7c55fd847dbc6fabb218165`

```json
{"first_shadow_contract_sha256":"0e37682d9b99c0838bf76453f4fdbed28a22979d3efa00ac57f9d101fe084e15","logger_frontier_contract_sha256":"2f222a025bf69758b96c6c8ff41bf01eee84d1191d7832ad0d1a30e398a96a3e","module":"../context/dist/logger.js","ownership":{"binding_identifier":"n","binding_kind":"FUNCTION_PARAMETER","function_body_end":2183,"function_body_start":1738,"function_name":null,"function_signature_end":1738,"function_signature_start":1716,"inside_first_shadow":true,"inside_second_shadow":false,"parameters":["e","t","n","r","s","i"],"targets_webpack_header_binding":false},"record_sha256":"e517cf1a35e54a43eb35c23045c3e2ab88b47e6a99ec6d8c0f089531cbeb57e4","second_shadow_contract_sha256":"9266dbad2adb3ce824091194deb2ccdb5917c71d5e88d765f9278008156d5dcc","source_window":{"end":2236,"sha256":"67fcc30a4a058f6857c1a7c8e441d971ecd205b22197a3010be62966a401dda9","start":1546,"text":"ew(e)){const t=e,r=null!==(d=null===(c=t.constructor)||void 0===c?void 0:c.name)&&void 0!==d?d:\"TypedArray\";return n.dim(`${r}(${t.byteLength})`)}return e instanceof Map?function(e,t,n,r,s,i){if(r>=t.maxDepth)return n.dim(`Map(${e.size})`);if(s.has(e))return n.dim(\"[Circular]\");s.add(e);const a=Array.from(e.entries()),l=Math.min(a.length,t.maxEntries),u=a.slice(0,l).map((([e,a])=>{const l=o(e,t,n,r+1,s,i.concat(\"<key>\")),u=o(a,t,n,r+1,s,i.concat(String(e)));return`${l} ${n.dim(\"=>\")} ${u}`}));a.length>l&&u.push(n.dim(`... ${a.length-l} more`));const c=n.dim(\", \"),d=`${n.dim(\"Map{\")}${u.join(c)}${n.dim(\"}\")}`;return s.delete(e),d}(e,t,n,r,s,u):e instanceof Set?l(Array.from(e.values("},"target_hazard_start":1716,"version":"GATE4_LOGGER_THIRD_N_PARAMETER_SHADOW_OWNERSHIP_V1"}
```

## Evidence

Evidence SHA256: `bbf10cd92cea241340c5df5156969f5a05b31d5a40087e88145c84df0f938aa3`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"be03782de1b123bf6e08760b995cb13bab0f7166a7c55fd847dbc6fabb218165","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_child_recursion_performed":false,"logger_complete":false,"targets_webpack_header_binding":false,"version":"GATE4_LOGGER_THIRD_N_PARAMETER_SHADOW_OWNERSHIP_EVIDENCE_V1"}
```

## Boundary

The n identifier in the function signature beginning at logger body offset 1716 is a local function parameter. Its complete body is contained by the previously qualified outer function beginning at 290, but it is not inside the nested function beginning at 330. This binding therefore remains independent of the webpack require parameter n.
