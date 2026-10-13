# Classification

Database **math**, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The untouched captured wrapper/record is `source.json`. There are **two practice questions**, both unrated, both with two select fields, both without a worked solution or correct designation in either field. Missing attributes remain missing in public `raw-*` replay. There are no plots; rating **none** for every mask and level. Math text is not a plot.

| Source | Markdown mask | Fields in capture order | Full source banks | Missing attributes |
|---|---|---|---|---|
| q-210947 | `compact`: system directly after opening paragraph | field-2: math/select, four choices; field-1: text/select, two choices | field-2 `10, -10, -9, 9`; field-1 `second, first` | difficulty, worked solution, both correct refs |
| q-211000 | `spaced`: blank line before system | same paired-select layout | field-2 `10, -5, 5, -10`; field-1 `second, first` | same |

There is one mathematical family and two observed Markdown masks, with one complete bank profile per source. Original select-list widgets in `/home/jake/Developer/MA/DATA/Lessons/4026/Source/4026.json` confirm exactly those two fields and those complete banks, so no legacy field is removed. A compact copy of the authoritative original widgets and canonical example is `original-layout.json`.

## Curriculum boundaries and authored levels

Owning topic: **Solving Systems of Linear Equations Using Elimination: One Transformation**, MA4026 / DB17592186050190. The lesson linked route, followed using `:activity/first-step` / `:step/next`, is tutorial → Eliminating the First Variable (192654) → **Eliminating the Second Variable (192655)** → Solving a System by Eliminating the First Variable (192656) → Solving a System by Eliminating the Second Variable (192657). We stop at elimination and never solve for either variable or substitute back. The official course capture identifies **Introduction to the Elimination Method**, MA742, as the prerequisite. Two transformations is a later topic, not a branch of this generator.

No observed difficulty labels exist. Normal easy/moderate/hard labels are explicitly **authored workload claims**, coordinated with sibling 192654. All perform exactly one integer row multiplication then add the two rows:

| Authored level | Smaller absolute target coefficient | Integer multiplier magnitude | Reasoning/workload |
|---|---:|---:|---|
| easy | 1 | 2–7 | Unit-coefficient comparison, choose correct row and sign |
| moderate | 2–4 | 2–4 | Nonunit exact integer coefficient division and sign |
| hard | 2–4 | 5–7 | Same nonunit division, larger coefficient/product bookkeeping, up to28 for target coefficients |

All non-target coefficients/constants are nonzero integers of magnitude≤10; all multiplication products≤70. Signs and row directions vary within every level without a progression or added method. Parameters cannot reduce a moderate/hard instance into unit arithmetic merely by introducing a global common factor. The canonical `(3x+4y=2; x−2y=4)` anchors the one-row method, prose and exact solution stages. The observed unit-source ratio10 remains supported in explicit evidence/completed source profiles but is outside the conservative easy default range. q-210947 gets an authored easy evidence assignment; q-211000 gets an authored hard evidence assignment. Neither is represented as an observed rating.

## Source anomalies

Both source system glyphs start with the unmatched literal `{` in math. Public raw replay retains the exact string and is evidence-only/ineligible. Normal output renders the literal glyph as `\{`; this is presentation normalization, not a mathematical repair. The canonical marked-row system additionally has an unmatched `(` before the unchanged first row; the smallest repair removes that stray parenthesis. At canonical parameters, the **entire** worked solution is byte-identical after those two presentation normalizations. The practice-source solution fidelity denominator is zero because neither practice source has a solution.

Correct answers are independently inferred: q-210947 **second,10**; q-211000 **first,−5**. There are zero original correct refs, so zero correct designations can be counted as matched. Supported `completed-*` profiles add authored fields' correct refs, authored difficulty and a canonical-derived worked solution, escape the system glyph, and clarify the integer single-row operation; their historical banks stay evidence-only.
