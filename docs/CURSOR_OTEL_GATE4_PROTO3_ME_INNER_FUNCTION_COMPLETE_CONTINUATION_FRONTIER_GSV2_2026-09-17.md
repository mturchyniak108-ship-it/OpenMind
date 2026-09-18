# Cursor / OTEL Gate 4 — proto3 me inner function complete and actual continuation frontier — Gold Standard V2

## Source authority

- Source HEAD: `4ce02970141d8e9a28b8abe43e518161d3ea6cde`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`
- Prior me binding authority SHA256: `caec2d6842e800fb9f146de58e86f1e27b9f4574b9a940f20b02e9fd00689173`

## Outer ownership chain

- pe assignment coordinate: `20704`
- pe parameter coordinate: `20707`
- pe arrow coordinate: `20708`
- pe owner SHA256: `54db362666ee7245115d05ad859e47ff2aa55324a2ed7f1c8c6eb2ec7e886b1a`
- Nested arrow group open: `20719`
- Nested arrow parameter coordinate: `20720`
- Nested arrow coordinate: `20721`
- Nested arrow owner SHA256: `d3887371200a101a29a122b847701fee23f8745856fc358ec269beb714adf3d2`

## Inner function completion

- Function start: `20723`
- Parameter: `e`
- Parameter n present: `false`
- Body start: `20735`
- Function close: `21391`
- Signature SHA256: `533e41f43994a1b9f6bfa8ce70e82522336b151b9edbce4e3f2861c836350542`
- Body SHA256: `16cb8b1e4075e8513a8a7fd8d39153a3634a94fc03bcbb4d3b4eeb39e58963c2`
- Function boundary authority SHA256: `d322b5eebf0c9e0ae38902af845c43b9f98aaffeec1d17a6207293641fbe7822`

## Function-scoped var n

- Binding coordinate: `20741`
- n owner SHA256: `a8880309746e4439e4876cd8391ecaf2db482dad99fe63b0dc90554ea96cb3db`
- n reference coordinates: `[20940, 20964, 20967]`
- Property n tokens: `[]`
- Other simple bindings: `[{"name": "t", "coordinate": 20739, "declaration_kind": "var", "keyword_coordinate": 20735, "paren_depth": 0, "block_depth": 0}, {"name": "r", "coordinate": 20743, "declaration_kind": "var", "keyword_coordinate": 20735, "paren_depth": 0, "block_depth": 0}, {"name": "s", "coordinate": 20745, "declaration_kind": "var", "keyword_coordinate": 20735, "paren_depth": 0, "block_depth": 0}, {"name": "i", "coordinate": 20747, "declaration_kind": "var", "keyword_coordinate": 20735, "paren_depth": 0, "block_depth": 0}, {"name": "o", "coordinate": 20749, "declaration_kind": "var", "keyword_coordinate": 20735, "paren_depth": 0, "block_depth": 0}, {"name": "a", "coordinate": 20757, "declaration_kind": "const", "keyword_coordinate": 20751, "paren_depth": 0, "block_depth": 0}, {"name": "c", "coordinate": 20766, "declaration_kind": "let", "keyword_coordinate": 20762, "paren_depth": 0, "block_depth": 0}, {"name": "d", "coordinate": 20778, "declaration_kind": "const", "keyword_coordinate": 20772, "paren_depth": 1, "block_depth": 0}, {"name": "e", "coordinate": 20816, "declaration_kind": "const", "keyword_coordinate": 20810, "paren_depth": 0, "block_depth": 1}, {"name": "t", "coordinate": 21273, "declaration_kind": "const", "keyword_coordinate": 21267, "paren_depth": 0, "block_depth": 2}]`
- n reference authority SHA256: `80e19d41753ccb1efcae65f3e6db97129da7f8f90a7445e741dbe1a2608fbf76`
- Function completion authority SHA256: `892a3e3ab0177a3eb85ee930a05416087625691f18f1983d03e37e736384623b`

## Actual continuation

- Continuation coordinate: `21392`
- Continuation character JSON: `"("`
- Continuation kind: `CALL_OR_GROUP_CONTINUATION_FRONTIER`
- Continuation prefix JSON: `"(e))),Ae=e=>{for(const t of e.getType().fields.byMember()){if(t.opt)continue;const n=t.localName"`
- Continuation prefix SHA256: `879f993d1c6b12cc2a2b0ae084f08e63201d87b5d8c7c7eb50874e02d1f3a672`
- Continuation authority SHA256: `ecc90768aac97e98bad98727a5a6a64ecf52924d7ba97dada96ab7e3cc60d2ad`
- Continuation semantically entered: `false`

## Frozen frontier

- Stop kind: `ME_INNER_FUNCTION_COMPLETE_CALL_OR_GROUP_CONTINUATION_FRONTIER`
- Stop coordinate: `21392`
- Frontier owner kind: `ME_NESTED_ARROW_CONTINUATION_UNQUALIFIED`
- Frontier owner SHA256: `ecc90768aac97e98bad98727a5a6a64ecf52924d7ba97dada96ab7e3cc60d2ad`
- Stop-window SHA256: `35d3fb90c94d9286dfac5e4812b4f8ee19963aadaf88299fc8f89609c0f3e554`
- Frontier-source SHA256: `8ec8d85ccf461644d3060d28d0df186e5dfca555c9a3b1f600293be37eb5b039`
- Frontier source JSON: `"(e))),Ae=e=>{for(const t of e.getType().fields.byMember()){if(t.opt)continue;const n=t.localName,r=e;if(t.repeated)r[n]=[];else switch(t.kind){case\"oneof\":r[n]={case:void 0};break;case\"enum\":r[n]=0;break;case\"map\":r[n]={};break;case\"scalar\":r[n]=p(t.T,t.L)}}},{syntax:\"proto3\",json:{makeReadOptions:function(e){return e?Object.assign(Object.assign({},S),e):S},makeWriteOptions:function(e){return e?Object.assign(Object.assign({},T),e):T},readMessage(e,t,n,r){if(null==t||Array.isArray(t)||\"object\"!=typeof t)throw new Error(\`cannot decode message ${e.typeName} from JSON: ${B(t)}\`);r=null!=r?r:new e;const s=new Map,i=n.typeRegistry;for(const[o,a]of Object.entries(t)){const t=e.fields.findJsonName(o"`

## Batch authority

- Prior batch authority SHA256: `425e890832e7547772479c5b1da555335453c69162f9d637df2c13aaa769fbea`
- Batch authority SHA256: `2ee17c6980fdfe17b6519820065d73185777617fa74f2c6ae14349998459084c`

The inner function was fully qualified, including its function-scoped var n. No assumption was made about the syntax following the function expression; the actual continuation was frozen exactly where encountered.

## Canonical evidence SHA256

`39f96b858ab579b4068edddffc54b21b50f7b8450368f5cbde7a88776089c05d`

## Authorization boundary

- pe owner replay: `AUTHORIZED AND PERFORMED`
- nested arrow owner replay: `AUTHORIZED AND PERFORMED`
- inner function qualification: `AUTHORIZED AND PERFORMED`
- function-scoped var n qualification: `AUTHORIZED AND PERFORMED`
- continuation discovery: `AUTHORIZED AND PERFORMED`
- continuation semantic entry: `NOT PERFORMED`
- nested arrow completion: `NOT CLAIMED`
- pe arrow completion: `NOT CLAIMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify only the actual continuation at proto3 body coordinate 21392 after completed inner function authority 892a3e3ab0177a3eb85ee930a05416087625691f18f1983d03e37e736384623b. Continuation kind is CALL_OR_GROUP_CONTINUATION_FRONTIER; do not assume nested-arrow or pe-arrow closure until this continuation is structurally resolved.
