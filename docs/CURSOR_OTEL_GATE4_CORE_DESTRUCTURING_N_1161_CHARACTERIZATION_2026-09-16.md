# Cursor OTEL Gate-4 core destructuring n 1161 characterization

Date: 2026-09-16

## Status

- target offset: 1161
- genuine destructuring LHS: YES
- bound n count: 1
- ownership qualified: YES
- targets webpack header n: NO
- core completion rerun: NO
- logger completion: NO
- dependency 11 source read: NO
- local-worker complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Contract

Contract SHA256: `2255755a7701fba0c7e7834caa9b83158971ad1c10c5b52c40fc3434302ad0aa`

```json
{"binding_identifiers":["t","n"],"bound_n_count":1,"declarator":{"declaration_end":1184,"declaration_kind":"const","declaration_start":1156,"declarator_end":1184,"declarator_raw":"[t,n]=this.withCancel()","declarator_start":1161,"initializer_present":true,"lhs_masked":"[t,n]","lhs_raw":"[t,n]","rhs_raw":"this.withCancel()"},"lhs_is_destructuring":true,"module":"../context/dist/core.js","ownership":{"binding_identifier":"n","binding_kind":"CONST_DESTRUCTURING_BINDING","declaration_kind":"const","declaration_start":1156,"declarator_start":1161,"lexical_scope_end":1212,"lexical_scope_start":1156,"owner_kind":"BLOCK_SCOPE","targets_webpack_header_binding":false},"record_sha256":"e0b0b92764d3e198f2ef5974e3835caf739391e996642d85b94bc18591c6df8a","source_window":{"end":1721,"sha256":"66f136acea35ffd55fd39969ae63aeb60157d3b3be7b55533577fb994ceb68f6","start":981,"text":"me()-Date.now();if(t<=0){const e=s(this.signal);return e.abort(new Error(\"context deadline exceeded\")),new i(this,e.signal)}return this.withTimeout(t)}withTimeoutAndCancel(e){const[t,n]=this.withCancel();return[t.withTimeout(e),n]}withName(e){return new i(this,void 0,void 0,e)}withDetached(){return new i(this,(new AbortController).signal)}getParent(){return this.parent}getPath(){const e=[];let t=this;for(;t;)t.name&&e.unshift(t.name),t=t.getParent();return e}}function o(){return new i}function a(e,t){return n=this,r=void 0,i=function*(){if(e.canceled)throw e.reason||new Error(\"context canceled\");return new Promise(((n,r)=>{const s=()=>{r(e.reason||new Error(\"context canceled\"))};e.signal.aborted?s():(e.signal.addEventListener(\"abo"},"target_offset":1161,"version":"GATE4_CORE_DESTRUCTURING_N_1161_CHARACTERIZATION_V1"}
```

## Evidence

Evidence SHA256: `e876c25a37038924210886bdbcab8fc51573ef2f03ac1956f9e7ed5aa3f7db50`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","contract_sha256":"2255755a7701fba0c7e7834caa9b83158971ad1c10c5b52c40fc3434302ad0aa","core_complete":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_11_source_read":false,"gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"local_worker_complete":false,"logger_complete":false,"targets_webpack_header_binding":false,"version":"GATE4_CORE_DESTRUCTURING_N_1161_CHARACTERIZATION_EVIDENCE_V1"}
```

## Boundary

This authority repairs only the first unsupported core construct returned by the prior completion macro. The declarator at body offset 1161 is separated into binding LHS and initializer before destructuring analysis. The actual bound identifiers are enumerated, and the n binding is assigned only to its lexical declaration scope. No core completion rerun or dependency advancement occurs.
