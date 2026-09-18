# Cursor / OTEL Gate 4 — proto3 function x structural scope repair V2 — Gold Standard V2

## Source authority

- Source HEAD: `484081c163ce48b8675428734f99fe35c423dc0d`
- Source tree: `25490240f4f10c69dc728c0675f57ac7daaba7d5`
- Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- OTEL SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`
- Prior authority document: `docs/CURSOR_OTEL_GATE4_PROTO3_MODULE_LEVEL_RECURSIVE_SUPER_BATCH_GSV2_2026-09-17.md`
- Prior document SHA256: `dfbf904b05153ecb4fb9281530e94342f8a275a0b979f49ed1dbc1fce47218e2`
- Prior evidence SHA256: `21feda2a53bf58264d444463a6eda930812db1ee13fa18c5e5ea6e2ce3475d25`

## Structural correction

- Function: `x`
- Function body open: `9025`
- Frontier coordinate: `9393`
- Frontier is inside function x: `true`
- Frontier open-brace stack: `[9025]`
- Frontier inner brace depth: `0`
- Structural function-x close: `9846`
- Correct owner at frontier: `FUNCTION_PARAMETER`
- Correct owner SHA256: `5d78aab364ca504dab04225fbed78c91a2b8149263e3f191910af8eb3242a5f4`
- Previous module-level classification: `SUPERSEDED`
- Structural authority SHA256: `47f4d0e941ecf4d3bf66cd35eb42bf0bed2907b758058f47bc993e882e950335`

## First n binding

- Kind: `DIRECT_N_BINDING`
- Resolution: `FOR_LEXICAL_BINDING_SCOPE_QUALIFIED`
- Binding coordinate: `9482`
- Declaration kind: `let`
- Declaration coordinate: `9478`
- For open: `9477`
- Loop owner SHA256: `e91118553756ee57d1873addfd32deb1474031be5f43b7515e92f90822726fd5`
- Loop scope: `9477–9520`
- Loop n references: `[9486, 9497, 9516]`

## Corrected resume state

- Resume start: `9521`
- Resume open-brace stack: `[9025, 9407, 9460]`
- Resume inner brace depth: `2`
- Restored outer owner: `FUNCTION_PARAMETER`
- Restored owner SHA256: `5d78aab364ca504dab04225fbed78c91a2b8149263e3f191910af8eb3242a5f4`
- Qualified outer n references: `[9583, 9667, 9678, 9789, 9843]`
- Next binding kind: `NO_BINDING`
- Next binding coordinate: `9846`
- Binding authority SHA256: `1d7189679478496a450efd5c2f9bdeee0ac6ed1f267ebb1296cd26c254d9b310`

## Frozen frontier

- Stop kind: `FUNCTION_X_STRUCTURAL_CLOSE_REACHED`
- Stop coordinate: `9846`
- Stop-window SHA256: `75ab00af45a3206a7daf024b136ab5425134c4cf3e438af813ac2d33df99dc43`

The resumed scanner carried the structural brace baseline instead of resetting it to zero.

No qualification was performed beyond the frozen frontier.

## Canonical evidence SHA256

`b840fee2a5f33116f6a2ddd054f2302ebcf5d73b720a489a2baf58d36e83c55a`

## Authorization boundary

- Static source reads: `AUTHORIZED AND PERFORMED`
- Structural replay: `AUTHORIZED AND PERFORMED`
- Brace-baseline repair: `AUTHORIZED AND PERFORMED`
- Simple for lexical n qualification: `AUTHORIZED AND PERFORMED WHEN PROVEN`
- Function-x continuation: `AUTHORIZED AND PERFORMED`
- JavaScript execution: `PROHIBITED AND NOT PERFORMED`
- Cursor execution: `PROHIBITED AND NOT PERFORMED`
- Gate 5 evaluation: `PROHIBITED AND NOT PERFORMED`
- Git push: `PROHIBITED AND NOT PERFORMED`

## Next eligible step

Freeze corrected function x completion at coordinate 9846, restore the webpack-header owner only after that close, then resume proto3 module-level qualification.
