# Cursor / OTEL Gate 4 — proto3 class ne byMember and class completion — Gold Standard V2

## Source authority

- Source HEAD: `014cd0701b378d4f355770e457d967bdf178257a`
- Class structure authority SHA256: `8477c94f531bd876da01f4afe37705b96388c4b3f94e75a6ca559c7ab6bbffcb`
- Prior method authority SHA256: `a9657eef19e19f537e96b4d4b3ff92a4db56a95ff5e592167699edf0d3d264b6`
- byMember boundary authority SHA256: `b30ce25ff62b2efe49617b7a07e0f88c22a0b9dcde249513f33d98a1b7b54146`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## byMember

- Start: `19000`
- Body start: `19011`
- Close: `19171`
- Parameters: `[]`
- Parameter n present: `false`
- Body SHA256: `b21abdf06db68f33714ff2c80feef630c0ae941e31695ab6fb150a71db7bc123`
- Other local bindings: `[{"name": "e", "declaration_kind": "const", "keyword_coordinate": 19045, "binding_coordinate": 19051}, {"name": "t", "declaration_kind": "let", "keyword_coordinate": 19066, "binding_coordinate": 19070}]`

## for-of lexical n owner

- For statement start: `19072`
- Binding coordinate: `19082`
- Binding kind: `const`
- Loop body start: `19099`
- Loop body end: `19151`
- Bare n references owned by loop binding: `[19099, 19107, 19123, 19149]`
- Bare n references outside loop owner: `[]`
- n owner SHA256: `ab1ed7225ad9cc8bbdf82e7811657da045a66efb9c61cf3904fa370db71e821b`
- n binding authority SHA256: `46d0acea5394cbcb328399bd0caea95cc082c4c670a597a16ee0045486a7cd33`

## Method completion

- byMember completion authority SHA256: `35adfd42351ed0b45adbad8580ca3df221eef4aed2405c2cf2f918c8a395ac57`

## Class ne completion

- Class start: `18496`
- Class close: `19172`
- Class completion authority SHA256: `091d69fcca969cd143d01a238b20796f7914845e02bb320a878e92af21e4d90c`
- Restored webpack owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`

## Frozen frontier

- Stop kind: `CLASS_NE_COMPLETE_NEXT_MODULE_FRONTIER`
- Stop coordinate: `19173`
- Frontier owner kind: `WEBPACK_HEADER_BINDING`
- Frontier owner SHA256: `e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8`
- Stop-window SHA256: `dfa0967651e63f7bc37b29398df5e1035413318b92032a749a5a951a30840f02`
- Frontier-source SHA256: `53fca0632240cb175790c8197d124459e5372b0c84ecca82ae0231a67e5d0ae0`
- Frontier source JSON: `"function re(e,t){const n=ie(e);return t?n:ce(ue(n))}const se=ie;function ie(e){let t=!1;const n=[];for(let r=0;r<e.length;r++){let s=e.charAt(r);switch(s){case\"_\":t=!0;break;case\"0\":case\"1\":case\"2\":case\"3\":case\"4\":case\"5\":case\"6\":case\"7\":case\"8\":case\"9\":n.push(s),t=!1;break;default:t&&(t=!1,s=s.toUpperCase()),n.push(s)}}return n.join(\"\")}new Set([\"break\",\"case\",\"catch\",\"class\",\"const\",\"continue\",\""`

## Batch authority

- Prior batch authority SHA256: `209d8300365b409c172e214a0d90b6bc0076c9c35d9e9f0ce60272aa8c9cffff`
- Batch authority SHA256: `4c576c94126299f539fe12626f1e40bbf22889ce42d14e336a4daf73a05fd3e2`

The byMember for-of lexical n binding was qualified before its n references were assigned. Class ne was then closed and webpack ownership restored.

## Canonical evidence SHA256

`5724190effdf5c4c98d6a418d29bee370418e138103b52749743f5887bf4cd01`

## Authorization boundary

- byMember static qualification: `AUTHORIZED AND PERFORMED`
- for-of lexical n owner qualification: `AUTHORIZED AND PERFORMED`
- Class-ne completion: `AUTHORIZED AND PERFORMED`
- Next module-level structure: `NOT ENTERED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Resume proto3 module qualification at body coordinate 19173 under restored webpack owner e72696543faa77cdb85b3b55a2153e96f5955f35f50d07aa5b5efc65f03f4bf8, using completed class-ne authority 091d69fcca969cd143d01a238b20796f7914845e02bb320a878e92af21e4d90c; discover the next module-level structure without entering unresolved ownership.
