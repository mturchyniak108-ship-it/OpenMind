# Cursor / OTEL Gate 4 — proto3 first new Set complete and const oe frontier — Gold Standard V2

## Source authority

- Source HEAD: `7149f3fc8ee0cb0c0e5d55682a74854ee5e271bc`
- Prior function-ie authority SHA256: `1026fd192d753b0b20fe0989b8cc0a619dc7e7fd35435b7c6270d21f213e1792`
- Proto3 body SHA256: `d51e58ac78ef5cd18697bb86ba0eab16cdf875d9cc62ef3ef6fb64baf5a0d3a1`

## Standalone new Set expression

- Start: `19513`
- Parenthesis open: `19520`
- Parenthesis close: `19991`
- Semicolon: `19992`
- End: `19993`
- Source SHA256: `7844b7a999ebd9ec6d3b7d8f77868b9d0b533ccef53b6b9bbbcad948befd7b16`
- Executable identifiers: `["new", "Set"]`
- Bare n references: `[]`
- Authority SHA256: `70ce25e58d3ba373a55392bf174755f3d9e637979fdfd9e861606b435a2cb10a`

## const oe boundary

- Declaration start: `19993`
- Binding coordinate: `19999`
- Binding name: `oe`
- Initializer start: `20002`
- Initializer kind: `new Set`
- Initializer parenthesis open: `20009`
- Binding authority SHA256: `f32e6eb674fe5a5238bad965c1397f297e101f41822879fe2a39d74f85fe3e39`
- Initializer semantically entered: `false`

## Frozen frontier

- Stop kind: `MODULE_CONST_OE_NEW_SET_INITIALIZER_FRONTIER`
- Stop coordinate: `20010`
- Frontier owner kind: `MODULE_CONST_OE_INITIALIZER_UNQUALIFIED`
- Frontier owner SHA256: `f32e6eb674fe5a5238bad965c1397f297e101f41822879fe2a39d74f85fe3e39`
- Stop-window SHA256: `fd329c0830f323593ab5b49906d2161653864dc92aef12628ec52fe95c1bedaf`
- Frontier-source SHA256: `3188c343137c1bf117f73711cf9f6fc1cc873ae999bb5c8cc4372b5aa66de3b2`
- Frontier source JSON: `"[\"constructor\",\"toString\",\"toJSON\",\"valueOf\"]),ae=new Set([\"getType\",\"clone\",\"equals\",\"fromBinary\",\"fromJson\",\"fromJsonString\",\"toBinary\",\"toJson\",\"toJsonString\",\"toObject\"]),le=e=>\`${e}$\`,ue=e=>ae.has(e)?le(e):e,ce=e=>oe.has(e)?le(e):e;class de{constructor(e){this.kind=\"oneof\",this.repeated=!1,this.packed=!1,this.opt=!1,this.req=!1,this.default=void 0,this.fields=[],this.name=e,this.localName=re(e,!1)}addField(e){(0,r.vA)(e.oneof===this,\`field ${e.name} not one of ${this.name}\`),this.fields.pus"`

## Batch authority

- Prior batch authority SHA256: `c86ad33ebcb161d81862b1ad879c7413af295867e513691638de010f14b0a9c0`
- Batch authority SHA256: `aa8fe27e49d49394adc5d137834aea6ce3251fd3a4c32f7de846e296686b3eb1`

The standalone new Set expression was fully qualified with no executable n reference. The following const oe binding was frozen before its new Set initializer contents were entered.

## Canonical evidence SHA256

`435383e27cbe1d07771dd1ad361d2db98ed583f21c16576901391b05bc21bc90`

## Authorization boundary

- Standalone new Set qualification: `AUTHORIZED AND PERFORMED`
- const oe binding qualification: `AUTHORIZED AND PERFORMED`
- const oe initializer contents: `NOT ENTERED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Qualify only the const oe new Set initializer beginning inside its argument list at proto3 body coordinate 20010; determine the exact Set-expression close, prove whether any executable n ownership or references occur, then restore module-level webpack ownership before advancing.
