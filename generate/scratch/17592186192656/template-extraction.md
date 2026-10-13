# Template extraction

## Stage1: each source before generalization

**q-18787** asks for the ordered pair `(x,y)` solving `4x-5y=0; 2x-3y=2`, with the hint to eliminate x. Its single radio field is named `selection`; five math values are complete ordered tuples, not independently selectable coordinates. The source has no rating, correct ref, or worked solution. Scaling the second equation by-2 produces `-4x+6y=-4`; addition gives `y=-4`; substitution in the second gives `2x+12=2`, hence `x=-5`. Only `(-5,-4)` satisfies both original rows.

**q-208816** presents `4x+3y=5; -x+7y=-9`, then asks for the solution by eliminating x. Two blanks occur inside the supplied tuple punctuation: field-1 is x and field-2 is y. Neither field has a choice bank or correct value in the snapshot. Multiplication of the second equation by4 gives `-4x+28y=-36`; addition gives `31y=-31`, hence `y=-1`; substitution gives `-x-7=-9`, hence `x=2`. Source tuple punctuation is malformed and is repaired only for normal authored records.

All source coefficients/constants are signed integers; the solution pairs happen to be integers. No fractions, nonlinear equations, plots, singular systems, or double scaling are observed. Canonical e-13999 solves `2x+3y=8; x-2y=-3` by one scaling-2, five ordered elimination rows and four back-substitution rows. It supplies the common solution prose used below; practice solution prose is absent, not silently synthesized as observed.

## Stage2: common pattern and purpose

For `a1*x+b1*y=c1; a2*x+b2*y=c2`, multiply exactly one equation by `m=-a_other/a_scaled`, add the rows to eliminate x, solve for y, and substitute y in an original equation to find x. The learner gives either the full tuple through radio or each scalar coordinate through the two source blanks. It is a full solve task, not merely identifying a row/multiplier or forming an eliminated equation.

## Stage3: complete components and source banks

Prompt slots are entire coefficients, constants, variable pair and complete system equations. No blind short-expression substitution is used. Every absent source question/field attribute remains absent in public raw replay. Source IDs, literal prompt/answer values, layouts and absent attributes are retained exactly at source parameters after projecting pulled field/answer enum refs to local ident strings, while all prompt mathematics and available choices are rendered by the same parameterized recipes used at changed parameters.

Let `(X,Y)` be the independently solved full pair. The complete observed bank is mapped one-to-one in source option order:

| Source answer UUID | Exact original value | Parameterized replay expression | Status |
|---|---|---|---|
| b07de6e3-d564-59dd-ab2b-f52b2f6a8dce | `(-5, 3)` | `(X,-Y-1)` | opaque wrong pattern; intent unresolved |
| f9dc4fdb-fc7f-57b9-bbcb-171440bb6b43 | `(-5,-4)` | `(X,Y)` | valid complete solution, original designation absent |
| 04165ac7-0685-5e0f-84da-400e81b14bf8 | `(-5, 1)` | `(X,-Y-3)` | opaque wrong pattern; intent unresolved |
| 0bb7d195-ce50-55d4-aa09-3ee5c62715d6 | `(4, 5)` | `(-Y,-X)` | opaque wrong pattern; intent unresolved |
| 5bc0bdd0-bb80-5744-9913-d84b487d2594 | `(-5, 2)` | `(X,-Y-2)` | opaque wrong pattern; intent unresolved |

These offsets reproduce the observed whole bank but do **not** infer error intent. `raw-q-18787` and `completed-opaque-q-18787` are public parameterized evidence profiles with `evidence_only=true`, `eligible_for_learning=false`. This explicitly avoids promoting fitted numerical patterns to defaults. Whole-bank duplicates or a second valid tuple reject the complete instance. A changed-constant evidence variant proves mathematical slots vary without a literal-source return branch. The blank raw profile `raw-q-208816` preserves absent choices and keys; there is no distractor bank to recover.

The source contains no available practice worked-solution prose to match. The canonical supplied prose is used for noticing coefficients, multiplying a row, adding equations, continuing to find x by substitution, and concluding the full tuple. Its initial literal brace/unmatched parenthesis is presentation-normalized into a balanced one-row scaling display. Normal stage recipes retain distribution, grouped addition, collection, solving, substitution and multiplication before the final result. Spaces before negative coefficients normalize notation without changing the ordered mathematics.

## Stage4: reusable masks, constraints and computations

`radio_solution` retains the source opening, system and first-variable hint. `blank_solution` retains the source system-first opening and the two field keys/coordinate order, with minimally balanced supplied punctuation. Variable aliases xy/ab/uv/st are curriculum-supported notation, excluded from task counts. Independent default layout choice covers both families.

Normal supported radio profile **authored-method-errors** is selected before sampling. Let scaled row be `(a,b,c)`, other row `(A,B,C)`, intended multiplier m and `D=B+m*b`. The whole five-tuple bank contains:

1. Correct `(X,Y)`.
2. Omit scaling the selected RHS: `w=(C+c)/D`, then `( (c-b*w)/a,w )`.
3. Omit scaling its y coefficient: `w=(C+m*c)/(B+b)`, then `( (c-b*w)/a,w )`.
4. Subtract the scaled RHS while still adding its coefficients: `w=(C-m*c)/D`, then `( (c-b*w)/a,w )`.
5. Reverse subtraction during back-substitution: `( (c+b*Y)/a,Y )`.

These are concrete operations on the displayed system; no random perturbations or pooled first-valid replacements are used. Undefined denominator, duplicate full tuple, extra valid solution or a correct-only integer tuple rejects the whole sampled instance. At least one wrong complete tuple must have both coordinates integer after exact reduction. Wrong coordinates can otherwise be fractions; they are complete exact tuples with no domain restriction beyond rational linear-system arithmetic. There is no invented option-specific feedback. Both blanks use exact scalar math values as authored supported answer fragments.

Normal scope bounds apply to both random sampling and explicit parameters:

| Level | Smaller absolute x coefficient | Absolute integer multiplier | y coefficient magnitudes | RHS magnitude ceiling | Solution coordinates |
|---|---|---|---|---|---|
| easy | 1 | 2–7 | 1–7, nonzero | 25 | nonzero integers of magnitude1–5 |
| moderate | 2–3 | 2–4 | 1–7, nonzero | 35 | same |
| hard | 2–3 | 5–7 | 1–7, nonzero | 40 | same |

The signed coefficient ratio is integral and determinant nonzero at every level. Scaling only the smaller first-variable coefficient requires exactly one nontrivial multiplication. Back-substitution uses that original row: easy unit coefficient permits direct sign isolation; moderate/hard require explicit final division by2 or3. Moderate/hard are separated by multiplication bookkeeping, with hard using familiar multipliers5–7. These are authored missing-level policies, not recovered ratings. Their bounds are grounded in the owning lesson's unit coefficient, coefficients2/3/4 and7, source multiplier4, first-variable setup multiplier7, and prerequisite integer linear-equation solving. Products up to21 for the hard first-variable coefficient are explicitly authored combinations of those familiar integers; no new mathematical method or rational-answer branch is added. Within a level, signed choices, orientation, layout and integer coordinates are unordered peer instances at the same reasoning workload.

Solution masks: notice source coefficients → one-row multiplication display → unchanged row/scaled row → grouped y and RHS additions → collected linear equation → y value → original scaled row → y substituted as grouped factor → product evaluated → x isolation when nonunit → x value → both coordinates in concluding prose. Intermediate grouped and product stages are structural masks, not eager SymPy simplifications. Each displayed operation and concluding coordinate is independently verified from the displayed prompt. Full-bank equivalence uses whole ordered pairs, and exactly one pair satisfies both rows. No arbitrary source-answer lookup is used.

Content identity includes version, displayed prompt, difficulty, fixed solution and entire displayed bank, with choice order excluded. Mathematical fingerprint uses primitive sign-normalized equation triples, canonical row order and their reduced elimination multiplier magnitude, excluding variable aliases, fields and bank profiles. Changing seed cannot alter fixed-parameter content identity. Changing bank/layout changes content identity while preserving mathematical-task identity. The independently enumerated strict subset in `variety-domain.json` excludes aliases and banks, providing a lower bound beyond sampled QA; it is not claimed to be the whole domain.


## Primitive workload guard and presentation equivalence

The table's smaller-coefficient and ratio bounds apply **both** to the displayed equations and to each equation divided by its own integer GCF (including RHS), with leading sign normalized. This catches whole-system factors and individual row factors. Multiplying all six entries of an easy system by2 can produce displayed smaller coefficient2 while leaving equivalent primitive smaller coefficient1; moderate generation rejects it. A factor on only the substituted row can similarly manufacture nonunit back-substitution; a factor on the other row can hide a smaller ratio or direct cancellation. Such easy or lower-level aliases reject the entire instance before learner content is emitted. Raw evidence profiles retain their separate source constraints and all original omission flags.

Individual row factors that preserve the same primitive level demands remain legitimate numerical presentations. For example `4x+y=5; 2x-3y=-1` and `8x+2y=10; 2x-3y=-1` both meet moderate bounds (primitive ratio2, displayed ratios2/4 respectively); their worked calculations use the actual printed multiplier, but their canonical mathematical fingerprint is identical. A hard printed ratio6 reducing to primitive ratio3 is outside hard scope. For easy, a primitive ratio1 is excluded because its transformed workload collapses to direct addition/subtraction. These checks do not require the learner to perform a GCF step: the presented solution still multiplies exactly one printed equation, adds, solves and substitutes as before.

`validate.py` independently applies reduced-equation scope guards to actual displayed rows and includes a global2×easy moderate mutation, an individually factored easy-collapse explicit request, and an accepted same-level row-rescaling identity regression. Source comparisons project exactly the two enum-ref attributes to strings and compare the complete question object thereafter. Literal mathematical payloads and missing choices/correct refs/difficulty/solution attributes are unchanged.


## Authored option-number-form eligibility

The observed opaque radio bank has five integer tuples. The authored method-derived bank can contain rational wrong tuples because omitting coefficient/RHS scaling or reversing back-subtraction changes exact divisions. These rational distractors are an explicitly authored number-form extension, not recovered source-bank values or source calibration. Normal correct answers remain signed integers. To prevent immediate selection by integer form, the entire normal radio instance is rejected unless **at least one wrong complete ordered pair is also entirely integer**. Neither component alone is sufficient; exact simplification determines integrality. The five error recipes stay intact, with no replacement or first-valid pool. Blank questions are unaffected, and raw/opaque evidence profiles retain their complete original banks.

The four stored parent parameter sets in `integer-shortcut-regression.json` each have a mathematically valid complete bank but only one integer tuple. Explicit radio requests now fail; their unchanged blank instances remain eligible. Independent validation reads the actual displayed tuples and catches the same shortcut without using answer metadata. Sample and finite-domain counts incorporate this whole-bank guard. This policy does not require all five choices to be integers; rational options can remain, but integer form alone cannot identify the correct answer.
