# Cursor / OTEL Gate 4 — proto3 re and se complete; ie frontier — Gold Standard V2

## Source authority

- Source HEAD: `ba178e84bb1f03783674408b15a1ce5aaa6ae832`
- Prior class-ne completion authority SHA256: `091d69fcca969cd143d01a238b20796f7914845e02bb320a878e92af21e4d90c`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## function re

- Start: `19173`
- Close: `19224`
- Parameters: `["e", "t"]`
- Local const n binding: `19196`
- Local n references: `[19213, 19221]`
- Webpack n references: `[]`
- Local n owner SHA256: `3992242f759d8ec58836728041253b368c9ec1e1f97d20846170c88d1ab752ca`
- Local n authority SHA256: `e038fc9137f33003e23528d03f9b553fdf75c293c839ccb820ad1dc8a6417e2f`
- Function authority SHA256: `727cb221aee46d193efc9afeffc9b9dfb6ee7dc47945574bb04ed9f806086919`

## module alias

- Source: `const se=ie;`
- Start: `19225`
- End: `19237`
- Binding name: `se`
- Contains n binding: `false`
- Contains n reference: `false`
- Alias authority SHA256: `c72692e5e96c83751c003749e8b18c5aca291cee34df9c39e157af7656559863`

## function ie boundary

- Start: `19237`
- Parameters: `["e"]`
- Parameter n present: `false`
- Body open: `19251`
- Body start: `19252`
- Signature SHA256: `091ce99069c22edb56c3182cc32899aa9f51392d0b747ee576bb53820128b5d3`
- Boundary authority SHA256: `c6142bd2efc15c831dcef05cf6165046478eb5bf593e238c718e2d61f7987706`
- Visible body prefix: `let t=!1;const n=[];`

## Frozen frontier

- Stop kind: `FUNCTION_IE_BODY_LOCAL_N_FRONTIER`
- Stop coordinate: `19252`
- Frontier owner kind: `FUNCTION_IE_UNQUALIFIED_SCOPE`
- Frontier owner SHA256: `c6142bd2efc15c831dcef05cf6165046478eb5bf593e238c718e2d61f7987706`
- Stop-window SHA256: `fb8b54904d2eeffb3303090d4a740a639c15ff1fec1424c011adbd53f5de46f5`
- Frontier-source SHA256: `f1f5fff39708d9a658982da35d7cd65b0fba0a48c1252e9ab159383c4f6fa5d2`
- Frontier source JSON: `"let t=!1;const n=[];for(let r=0;r<e.length;r++){let s=e.charAt(r);switch(s){case\"_\":t=!0;break;case\"0\":case\"1\":case\"2\":case\"3\":case\"4\":case\"5\":case\"6\":case\"7\":case\"8\":case\"9\":n.push(s),t=!1;break;default:t&&(t=!1,s=s.toUpperCase()),n.push(s)}}return n.join(\"\")}new Set([\"break\",\"case\",\"catch\",\"class\",\"const\",\"continue\",\"debugger\",\"default\",\"delete\",\"do\",\"else\",\"export\",\"extends\",\"false\",\"finally\",\"for\",\"function\",\"if\""`

## Batch authority

- Prior batch authority SHA256: `4c576c94126299f539fe12626f1e40bbf22889ce42d14e336a4daf73a05fd3e2`
- Batch authority SHA256: `830ced7a4f6b044995020c876d5cd56efeb332cee3ac24221506d89b0d601380`

function re and const se=ie were fully qualified. function ie was frozen before its body-level const n ownership was entered.

## Canonical evidence SHA256

`a0837db48657f5c248fb169742e14ceaa0851c55c5beb9c65c236d63666a7c08`

## Authorization boundary

- function re qualification: `AUTHORIZED AND PERFORMED`
- const se=ie qualification: `AUTHORIZED AND PERFORMED`
- function ie header qualification: `AUTHORIZED AND PERFORMED`
- function ie body semantic qualification: `NOT PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify function ie beginning at proto3 body coordinate 19252; freeze its body-level const n owner before assigning any n references. The visible prefix is let t=!1;const n=[];.
