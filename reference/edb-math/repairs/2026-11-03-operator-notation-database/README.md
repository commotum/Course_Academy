# Database-wide named-operator repair

Completed on 2026-11-03, with the final bulk transaction at **math T12364**. A fresh whole-database census at that basis found **zero remaining identified operator-notation errors**.

The [reported lesson](../2026-11-03-latex-17592186247132/README.md) exposed two related failures: conversion lost the role of a named MathML operator, and some saved TeX assumed nonstandard macros that this renderer does not define. This left expressions such as `arccscx`, `{sin}^{2}⁡x`, `det(A)`, and `\sech x` as ordinary letters or undefined commands. Function names can display incorrectly even when MathJax reports no parse error.

The complete census covered **707,986 content facts** across question prompts, worked solutions, answer values and feedback, checkbox labels, tutorials and multistep contexts. Answer types were resolved before treating any bare answer string as mathematics. Raw learner submissions were checked separately and preserved.

The database-wide pass repaired **9,560 attributes across 7,971 entities**. Including the earlier lesson repair and accounting for three overlapping attributes, the combined repair covers **9,692 distinct attributes across 8,074 entities**.

| Attribute | Database-wide repairs |
| --- | ---: |
| Worked solutions | 4,209 |
| Question prompts | 1,848 |
| Answer values | 3,248 |
| Tutorials | 158 |
| Checkbox labels | 93 |
| Multistep contexts | 4 |

The changes preserve mathematical operands, constants, argument/power/subscript scope, identities, correct-answer links, response ownership, saved grades, difficulty and all other attributes. Literal prose, unrelated variable products and descriptive subscripts are excluded. Exact native Pull readback recursively verifies component entities as well as top-level attributes. Requests are durable, basis guarded and recoverable under their original keys.

A first-batch check exposed an overbroad treatment of the valid binary command `\div`. All **712 affected attributes were restored with a verified compensating transaction** before the corrected repair continued. Valid division and modulo commands are now protected explicitly, and the mathematical comparison preserves their operator roles. The original request and reconciliation remain in `initial-batch-reconciled/`, `compensation/`, and `compensation-summary.json`; they are not counted as successful notation repairs.

Prevention is shared across producers:

- Live and historical DOM extractors retain known named MathML nodes even without a function-application marker. The archived HTML converter and instruction reconciler use the same operator registry.
- The formatter recognizes the supported named-function families, powered/subscripted names, escaped application markers and joined legacy controls. Nonstandard functions use portable `\operatorname{...}` notation.
- Publication repairs operators in prompts, solutions, choices, feedback and checkbox statements **before stable identities are assigned**, including output from packages carrying older formatter copies.
- Import matching compares structural operator typography, preserving mathematical scope and existing answer identities across command/style aliases. All **3,248 repaired answer values** retain the same matching identity before and after formatting.
- Generator author/reviewer instructions require visible upright operators and preservation of argument and neighboring-factor scope. A successful TeX parse alone is insufficient.

Verification:

- **136 regression checks passed** across operator normalization, publication/delivery, capture preparation, mathematical formatting, existing equilibrium/fraction repairs, and function-boundary identities. A stale invalid-spacing fixture was corrected only after the prior immutable formatter demonstrated that its concrete `5pt` form was already intentionally repairable; an unknown-length negative control remains.
- **52 browser extraction cases passed** across both capture implementations, including marker-free and powered function nodes.
- **47 operator names and 60 notation patterns** passed actual learner UI/glyph checks, reusing only identical previously passing previews. The lesson separately rendered all 37 changed questions/examples and four phone cases. Representative inverse and inverse-hyperbolic results were visually inspected.
- **918 affected radio/select banks** checked: no newly identical choices. Existing used answers were checked; no raw learner submissions required rewriting.
- **150 live grading checks passed on all 50 complete practice questions** in the reported lesson. Seven partial imports were retained without guessed keys. No learner attempts were created.
- The final independent read covered all **707,986 content facts / 707,979 distinct entity-attribute pairs**, resolved answer types, and found **zero residual errors under the implemented operator checks**. The service was reloaded for the shared publication/import changes.

`verification.json` contains the six corrected bulk batches: 8,896 newly written attributes and 664 already repaired by the reconciled initial batch. Their sum is the 9,560 planned database-wide repairs. `totals.json` accounts for the earlier lesson repair. `final-census.json`, `preflight.json`, `reimport-verification.json`, `render-verification.json`, and `live-verification.json` retain the checks. Compressed initial/final snapshots and hashes preserve the complete read evidence. The executable workflow is `export.rs`, `build.py`, `preflight.py`, `render.py`, `deploy.py`, `final_scan.py`, and `verify_live.py`.

The residual result is scoped to named-operator defects identified by the source/notation rules. It does not claim that every other possible formatting or mathematical defect in the database has been reviewed.
