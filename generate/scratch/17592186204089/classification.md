# Identifying an Equation With No Solutions

Captured `math` at basis 1842, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The full frozen record is in `source.json`; exact query, inputs and EDN response are under `reference/initial/`. All seven practice questions are present and readable. The canonical example is evidence only and does not count toward inventory.

Five practice questions are rated easy. Two legacy questions, q-287964 and q-288058, are unrated and remain excluded from inventory. Each question has three checkbox fields keyed I, II and III. Every field owns two text answers, `false` and `true`, and selects `true` exactly when the corresponding real affine equation has no solutions. This is the current migrated database representation; the historical radio subset banks are retained in database history and are not reproduced as new radio questions.

| Difficulty evidence | Template | Representative practice IDs | Response fields | Plot rating |
|---|---|---|---|---|
| Easy | detailed-scaled | q-288066, q-288070, q-288072, q-288074 | I/II/III checkbox | none |
| Easy | detailed-unit | q-288073 | I/II/III checkbox | none |
| Unrated; local replay assigned easy | summary-spaced | q-287964, q-288058 | I/II/III checkbox | none |

These are three distinct Markdown/value templates. The detailed-unit sequence reaches the isolated variable directly after adding terms to both sides. The detailed-scaled sequence also displays the intermediate coefficient equation and divides. The legacy summary template uses spaced expressions and one prose reduction sentence. Two contradiction patterns occur: one contradiction, one identity and one unique solution; or two contradictions and one unique solution. Preserve their ordered placement.

All three templates share one complete source bank profile, `boolean-per-equation`. There are 21 field banks and 42 source values; `choice-mapping.json` assigns every value and correct designation to its source field and coefficient parameters. There are no omitted distractors or unresolved mathematical values.

No prompt, choice or solution contains a plot. Standalone LaTeX is mathematical notation, not an image. Plot extraction and generation therefore require no assets.

Moderate and hard are unsupported by this validated package. All available source evidence assesses direct cancellation of simple integer affine terms, including signed constants, signed coefficients, zero solutions of a uniquely solvable equation, and noninteger rational unique solutions. No source or validated higher-demand template establishes moderate or hard. This is a bounded capability exception, not a claim that such questions are mathematically impossible. Each unproduced band retains its nominal shortage of five; new source evidence reopens classification.
