# Classification

Snapshot: math / basis 1356 / lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Captured source.json is unchanged.

| Level | Practices | Observed Markdown/value templates | Field | Plot rating |
|---|---:|---:|---|---|
| easy | 9 | 8 | One five-choice text radio, key selection | none |
| moderate | 8 | 7 | One five-choice text radio, key selection | none |
| hard | 0 | 0 | One five-choice text radio, key selection | none |

There are 15 observed structural templates, 8 complete bank profiles, and 18 raw fields across 17 questions. Templates distinguish statement order/type, bullet/roman/roman-spaced layout, difficulty, and the compact five-stage versus full six-stage solution. Changed matrix values are variants, not separate templates. Easy bullet det/singular/det and moderate bullet singular/det/det each combine two sources.

Hard has one authored template, not an observed level label. It keeps the same three-statement radio task and top-row cofactor method. Dense nonzero entries use signed fractions and one repeated radical family: fraction minors are present in q-77478 and q-38187, fraction/radical cancellation in q-128490, and squared radicals in q-128491. The repeated radical follows those existing arithmetic operations, without introducing a new radical-combination branch. Easy uses small signed integers; moderate uses fraction columns, radical columns, or a combination as in the originals. Each level samples singular/nonsingular matrices without a progression.

The lesson route (followed via first-step and next) is Introduction → Calculating the Determinant → Singular Matrices → Identifying Singular Matrices → Solving for a Variable → Solving for an Unknown. This KP stops at numeric determinant and singularity. The key prerequisite is Introduction to the Inverse of a Matrix; the singular tutorial defines det=0 and no multiplicative inverse. Unknown entries, inverses, and row reduction are excluded.

## Source-format anomaly

q-128490 contains two raw selection fields; legacy field 3834be7c-3d92-5a42-ba11-b5873d0a2001 has no correct reference. The captured original MA lesson widget (q-128490-authoritative-widget.json and /home/jake/Developer/MA/DATA/Lessons/153/Source/Sections/08-question-128490.png, inspected) contains one five-choice bank. Both raw fields have the identical complete value set, with the newer field carrying correct III only. Exact expansion derives 0. Normal generation produces one assessment; source replay profiles retain both field banks. The missing legacy designation is inferred, never counted as matched. The newer raw field resolves the assessment; no source is excluded.

q-77477 and q-128491 have malformed bold **not ** in their closing sentence; generated prose repairs **not**. q-77477 answer whitespace (I  only / I and III  only) remains exactly captured. Mathematical typography, whitespace, coefficient sign/parentheses, and commuted products are normalized, separately from bank fidelity. All arithmetic rows are independently verified as exact equalities.

## Templates

| Template | Sources | Stages |
|---|---|---:|
| moderate_bullets_det_det_singular_6 | q-128490 | 6 |
| easy_bullets_det_singular_det_6 | q-9838, q-9835 | 6 |
| easy_bullets_det_det_nonsingular_6 | q-128474 | 6 |
| easy_bullets_singular_nonsingular_det_6 | q-128476 | 6 |
| moderate_bullets_singular_det_det_6 | q-128484, q-77478 | 6 |
| moderate_bullets_singular_nonsingular_det_6 | q-38179 | 6 |
| easy_bullets_nonsingular_singular_det_6 | q-38182 | 6 |
| easy_bullets_singular_det_det_6 | q-69834 | 6 |
| moderate_roman-spaced_nonsingular_singular_det_5 | q-77477 | 5 |
| moderate_bullets_nonsingular_singular_det_6 | q-77479 | 6 |
| easy_roman_det_nonsingular_det_6 | q-128478 | 6 |
| easy_roman_singular_det_det_6 | q-128480 | 6 |
| moderate_roman_singular_nonsingular_det_6 | q-128491 | 6 |
| moderate_roman_nonsingular_singular_det_6 | q-38187 | 6 |
| easy_roman_singular_det_nonsingular_6 | q-69835 | 6 |
| dense_exact | authored | 6 |