# Cursor / OTEL Gate 4 — proto3 class ne list complete and byNumber frontier — Gold Standard V2

## Source authority

- Source HEAD: `375db19a15850f122aef2c2e4b97ede155b4df2b`
- Class structure authority SHA256: `8477c94f531bd876da01f4afe37705b96388c4b3f94e75a6ca559c7ab6bbffcb`
- Prior method authority SHA256: `db7fa28925cdf8cd1795cff475d67d38eae7da9e08ba7676a85f8c7cc6c06b1b`
- list boundary authority SHA256: `f27a84e8a6d5a9e396ed1eea6e12196b3bae5e13c35893792e0c6fb7ed3eb0a2`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## list

- Start: `18810`
- Body start: `18817`
- Close: `18884`
- Parameters: `[]`
- Parameter n present: `false`
- Local n bindings: `[]`
- Bare n references: `[]`
- Completion authority SHA256: `19acff3e2b89ea0412b5280725f329aa458a24963bdf0b1c69e9c908d0e8e115`

## Next method boundary

- Method name: `byNumber`
- Method start: `18885`
- Parameters: `[]`
- Parameter n present: `false`
- Method body open: `18895`
- Method body start: `18896`
- Signature SHA256: `82bf340543dca340898b900c0a6401b7f71952b19147213c5f2ebd7306dc0d7a`
- Boundary authority SHA256: `9d1de65774faa658d84fe3764dde6de21d039269bcf8aca6fc89d8211f764158`

## Frozen frontier

- Stop kind: `CLASS_NE_BYNUMBER_BODY_FRONTIER`
- Stop coordinate: `18896`
- Frontier owner kind: `CLASS_NE_BYNUMBER_UNQUALIFIED_METHOD_SCOPE`
- Frontier owner SHA256: `9d1de65774faa658d84fe3764dde6de21d039269bcf8aca6fc89d8211f764158`
- Stop-window SHA256: `a386efde31a4dac3adf7b9334fbaf01ec1c9ee52d3b16f9f7ab0bbafd6cdac4b`
- Frontier-source SHA256: `a22634d629142f3633bdd5d358090c2f3bc66d8fee185cdabcf688fe24fc1ca5`
- Frontier source JSON: `"return this.numbersAsc||(this.numbersAsc=this.list().concat().sort(((e,t)=>e.no-t.no))),this.numbersAsc}byMember(){if(!this.members){this.members=[];const e=this.members;let t;for(const n of this.list())n.oneof?n.oneof!==t&&(t=n.oneof,e.push(t)):e.push(n)}return this.members}"`

## Batch authority

- Batch authority SHA256: `d7352cef701a4b8356ae1e2a7f8ba1e52daac334f2ee3be2380495db23be6753`

The list body was fully qualified. The byNumber body and its nested arrow were not semantically entered.

## Canonical evidence SHA256

`3a744ab3d08a1b79b07d97719ffb9b190883dd2691d90fcb745eb88fc178aab6`

## Authorization boundary

- list semantic qualification: `AUTHORIZED AND PERFORMED`
- list local-n exclusion: `PASS`
- byNumber header qualification: `AUTHORIZED AND PERFORMED`
- byNumber body semantic qualification: `NOT PERFORMED`
- byNumber nested arrow: `NOT ENTERED`
- Later methods: `NOT ENTERED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify class-ne byNumber method from proto3 body coordinate 18896; freeze and qualify its nested arrow ownership before continuing beyond that arrow, because byNumber contains an arrow expression.
