# Classification

Source: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the complete captured wrapper and record. There are 15 practice questions: 13 explicitly easy, two unrated. No moderate or hard source examples were captured. Canonical examples are context, not counted as practice.

| Source label | Fields | Markdown/value templates | Complete radio banks | Plot rating |
|---|---|---:|---:|---|
| Easy | one radio or one integer blank | 3 | 7 | none |
| Unrated, assigned easy for replay | one radio | 1 | 2 | none |
| Moderate, authored | same radio and integer blank | 3 available | 1 authored | none |
| Hard, authored | same radio and integer blank | 3 available | 1 authored | none |

Four observed value/layout templates: `legacy_radio` uses `vmatrix` notation and has no supplied worked solution/correct ref; `aligned_radio` uses absolute-value aligned notation and the shared cofactor explanation; `matrix_blank` names the matrix, expects only the integer determinant, and starts arithmetic from evaluated products; `matrix_blank_products` has the same blank layout but includes an explicit multiplication row before evaluating the three minors. Zero entries control optional omitted arithmetic terms; they do not create another skill.

Every radio has exactly five math choices. Every blank has `field-1`, one expected integer answer, and the original `det(A)=` fragment outside the field. Source blank matrix names A/H/Q/R/W are variable letters. Radio sources use `selection` without an explicit placeholder. All source choices are mapped below, including the two unrated sources.

The only referenced asset in this KP's canonical example was inspected at `/media/jake/SSD/EDB/math/images/8e/8e7935fce161e2a1ed706ec03bb5cd202e8c4650ba01ca5e4633f9f1c121d04a.png`. It displays the numeric determinant `[0,-3,6;8,8,8;-6,-12,1]`, matching the canonical solution. It is standalone typeset mathematics, not a graph or diagram. No source practice item references an image. Plot extraction and parameterized rendering are consequently unnecessary.

## Curriculum and authored missing levels

The prerequisite is **The Minors of a 3x3 Matrix** (topic 17592186048965). The linked lesson route is 60808 Introduction → 60809 this KP → 60810 Singular Matrices → 60811 Identifying Singular Matrices → 60812 Solving for a Variable → 60813 Solving for an Unknown Given the Determinant (IDs share prefix 175921860). This order follows `activity/first-step` and successive `step/next`, not collection order. The introduction explicitly teaches `a(ei-fh)-b(di-fg)+c(dh-eg)` and warns about the second-term minus sign. Its worked example has a zero entry and signed values. The canonical example includes values through 12 in magnitude.

Missing-level labels are authored design claims. Moderate uses dense signed integer matrices with magnitudes 2..8: all three minors normally contribute, with the same three cofactor terms and no new method. Hard uses dense signed integer magnitudes 4..12, retaining the canonical range and the same operation count while demanding more signed product and subtraction arithmetic. Within a level, matrices, letters, field formats and banks are unordered variations with the same method. There are no variables to solve, singularity questions, determinant identities, inverses, or higher-dimensional matrices. Those belong to sibling or later KPs. The levels do not add algebraic branches. Explicit replay accepts all exact integer matrices; the narrower magnitude ranges are sampling policy, not a claim that integer determinant calculation has strict mathematical difficulty boundaries.

## Source anomalies and interpretation limits

`q-128309`: the source's first arithmetic row has `-1(-3-20)` where the cofactor expansion and all later rows require `+1(-3-20)`. The incorrect row evaluates to 14; the determinant and stated answer are -32. The evidence is preserved in `source.json`, `source-cases.json`, and the original section of the review. Generated solutions use the corrected positive third coefficient.

`q-38128` and `q-9841` omit difficulty, worked solution, and correct refs. Independent mathematics identifies -42 and -13; these are existing displayed choices. They remain in fidelity analysis, assigned easy only for replay. A source-style worked solution is authored for them. These missing fields are not counted as observed correct-ref matches.

All displayed bank values are reproduced, but scalar distractors do not uniquely identify original authoring algorithms. Index/product formulas are explicitly inferred parameter generalizations, with uncertain pedagogical intent, particularly `legacy_zero_diagonal`. They are not claimed as recovered source code. Worked solutions keep the exact opening and cofactor calculation stages; uniform signed-factor parentheses and zero simplification normalize notation. Byte-for-byte worked-solution fidelity is not claimed.


## Default distractor policy

Default radio generation uses the authored `cofactor_signs` bank at every level: its wrong answers represent identifiable cofactor-sign or minor-subtraction errors. Observed scalar-bank generalizations remain available through explicit template/profile selection for fidelity replay; exact values do not establish their original error intent. The legacy radio template is excluded from automatic template selection. Thus uncertain polynomial fits cannot silently supply default learner choices.
