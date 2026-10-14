# Template extraction — four stages

Frozen provenance matches source.json; every practice record is listed. Raw profile mathematics is derived from h and c, not a returned source payload. Source correct refs are preserved only when present.

## Stage 1: specific observations

### q-235904

Captured level: absent (unrated). Variable y, half-coefficient h=9, constant c=64, residual c−h²=-17.

Exact prompt: Complete the square on the quadratic expression $y^{2} - 18y + 64$.$y^{2} - 18y + 64 = ($ {{field-1}} $)^{2} -$
{{field-2}}

Solution: attribute absent. Fields in captured pull order: field-2 (:answer-field.type/blank), field-1 (:answer-field.type/blank).

### q-25253

Captured level: absent (unrated). Variable y, half-coefficient h=4, constant c=12, residual c−h²=-4.

Exact prompt: If the expression $y^{2} - 8y + 12$ is written as $(y + p)^{2} + q$, then what are the values of $p$ and $q$?

Solution: attribute absent. Fields in captured pull order: selection (:answer-field.type/radio).

### q-141615

Captured level: :question.difficulty/easy. Variable x, half-coefficient h=6, constant c=28, residual c−h²=-8.

Exact prompt: Complete the square on the quadratic expression ${x}^{2}-12x+28.$

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: .

### q-141611

Captured level: :question.difficulty/easy. Variable x, half-coefficient h=5, constant c=19, residual c−h²=-6.

Exact prompt: Complete the square on the quadratic expression ${x}^{2}-10x+19.$

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: selection (:answer-field.type/radio).

### q-141612

Captured level: :question.difficulty/easy. Variable y, half-coefficient h=2, constant c=10, residual c−h²=6.

Exact prompt: Complete the square on the quadratic expression ${y}^{2}-4y+10.$

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: selection (:answer-field.type/radio).

### q-250465

Captured level: :question.difficulty/easy. Variable y, half-coefficient h=12, constant c=44, residual c−h²=-100.

Exact prompt: Complete the square on the quadratic expression ${y}^{2}-24y+44.$

${y}^{2}-24y+44=(${{field-1}}${)}^{2}\,-$
{{field-2}}

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: field-1 (:answer-field.type/blank), field-2 (:answer-field.type/blank).

### q-250466

Captured level: :question.difficulty/easy. Variable y, half-coefficient h=5, constant c=53, residual c−h²=28.

Exact prompt: Complete the square on the quadratic expression ${y}^{2}-10y+53.$

${y}^{2}-10y+53=(${{field-1}}${)}^{2}\,+$
{{field-2}}

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: field-2 (:answer-field.type/blank), field-1 (:answer-field.type/blank).

### q-250517

Captured level: :question.difficulty/moderate. Variable x, half-coefficient h=5, constant c=0, residual c−h²=-25.

Exact prompt: If the expression ${x}^{2}-10x$ is written as $(x-p{)}^{2}+q$, then what are the values of $p$ and $q?$

$p=$
{{field-1}},
$\,q=$
{{field-2}}

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: field-1 (:answer-field.type/blank), field-2 (:answer-field.type/blank).

### q-3662

Captured level: :question.difficulty/moderate. Variable x, half-coefficient h=1, constant c=0, residual c−h²=-1.

Exact prompt: If the expression ${x}^{2}-2x$ is written as $(x+p{)}^{2}+q$, then what are the values of $p$ and $q?$

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: selection (:answer-field.type/radio).

### q-141622

Captured level: :question.difficulty/moderate. Variable y, half-coefficient h=5, constant c=30, residual c−h²=5.

Exact prompt: If the expression ${y}^{2}-10y+30$ is written as $(y+p{)}^{2}+q,$ then what are the values of $p$ and $q?$

Solution: four displayed stages with fixed instructional prose. Fields in captured pull order: selection (:answer-field.type/radio).

## Stage 2: generalized pattern

For positive integer h, rewrite the monic quadratic v²−2hv+c as (v−h)²+(c−h²). Assess either the complete expression, the binomial plus residual magnitude after a supplied sign, or the two scalar parameters p/q under an explicitly supplied plus/minus binomial convention. Preserve four stages: rewrite the linear coefficient as 2·h; insert +h²−h²; factor the first three terms; collect the two constant components. Omitted zero source q-3662 has no redundant +0 or constant-term sentence; q-250517 explicitly writes +0 at the first three stages. Its final row lacks a period, unlike other examples. Normal p/q-minus at zero preserves that source sequence.

## Stage 3: every component and complete bank

In all recipes r=c−h². Tuple values are ordered (p,q), and source bank order is recorded below solely for mapping; output shuffles radio choices without changing identity. Historical scalar distractor intention is not recoverable from a single value. The two opaque banks expose four integer scalar components o1..o4 (magnitude≤300), with source anchors below. They are independently supplied bank evidence parameters, not inferred learner error recipes. No opaque profile is eligible for normal sampling.

### source:q-235904 — fragment

Field field-2 (:answer-field.type/blank).

Choices and correct ref absent. Inferred fragment: |r|. No choice-value fidelity denominator is fabricated.

Field field-1 (:answer-field.type/blank).

Choices and correct ref absent. Inferred fragment: v−h. No choice-value fidelity denominator is fabricated.

### source:q-25253 — pq_plus

Field selection (:answer-field.type/radio).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| c55f4bcc-ccdb-5fb3-99a9-81cf0e13f2e2 | `p =-4, q = 4` | (-h,−r) | absent |

| 3e0cd0b1-c599-5aa4-860c-0d1885312374 | `p =-4, q =-4` | (-h,r) | absent |

| 488f232a-a7e6-50aa-9fda-1554ef507144 | `p = 4, q = 4` | (h,−r) | absent |

| 662bfae3-69e7-54db-8c75-f8a1607c939f | `p = 4, q =-4` | (h,r) | absent |

| 769708f3-d1e7-531e-be51-742113b7b61a | `p =-4, q =-16` | (-h,−h²) | absent |

### source:q-141615 — direct

Answer fields attribute absent; normal direct radio or blank assessment is authored completion, not source fidelity.

### source:q-141611 — direct

Opaque bank anchors o1..o4: [-12, 9, 3, -5]. These are structural bank components without a claimed error interpretation. Changing h changes the binomial factors and computed correct residual; changed opaque components require explicit input.

Field selection (:answer-field.type/radio).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 2c357baf-37ee-59ff-b900-a32da3e0955f | `(x-5{)}^{2}-12` | (v−h)²+o1 | incorrect |

| 483df771-1e1b-56ba-bd41-370566736e50 | `(x-5{)}^{2}+9` | (v−h)²+o2 | incorrect |

| 57316dd8-97c9-5036-80fa-245ab789f57e | `(x-5{)}^{2}-6` | (v−h)²+r | correct |

| b54b1ed7-1a5c-532c-9b56-213f971511e7 | `(x-5{)}^{2}+3` | (v−h)²+o3 | incorrect |

| f79469df-027d-5f1b-b7e1-dc88f72d1a36 | `(x-10{)}^{2}-5` | (v−2h)²+o4 | incorrect |

### source:q-141612 — direct

Opaque bank anchors o1..o4: [1, -4, 3, 5]. These are structural bank components without a claimed error interpretation. Changing h changes the binomial factors and computed correct residual; changed opaque components require explicit input.

Field selection (:answer-field.type/radio).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 4b8b2afd-fb57-5e61-8b75-209b9cfb00a6 | `(y-4{)}^{2}+1` | (v−2h)²+o1 | incorrect |

| 56189019-79f9-5478-aff6-fce083001fda | `(y-2{)}^{2}-4` | (v−h)²+o2 | incorrect |

| 5b5b5397-8f7e-5320-893a-7dfa34d502d5 | `(y-2{)}^{2}+3` | (v−h)²+o3 | incorrect |

| b8a21ffd-56c6-5136-bf66-bc5dc8d6441d | `(y-2{)}^{2}+6` | (v−h)²+r | correct |

| e1c6894a-0f18-540f-812c-d0d96b4ec938 | `(y-4{)}^{2}+5` | (v−2h)²+o4 | incorrect |

### source:q-250465 — fragment

Field field-1 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 32e0e5d7-fdb8-59c1-ad92-627588672552 | `y-12` | v−h | correct |

Field field-2 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 316891ce-732f-5962-81c6-6104eaf74326 | `100` | |r| | correct |

### source:q-250466 — fragment

Field field-2 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| b74e78a8-3b6b-549a-b92d-4c311cd6b49b | `28` | |r| | correct |

Field field-1 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 000ea0dc-e83d-59b3-891d-03ba54bde6ba | `y-5` | v−h | correct |

### source:q-250517 — pq_minus

Field field-1 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 4ae8278a-b8a2-5f12-b4e0-1ae6448bf12f | `5` | h | correct |

Field field-2 (:answer-field.type/blank).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| bbe62bcf-2c19-5db0-aa2d-28c8e425c32e | `-25` | r | correct |

### source:q-3662 — pq_plus

Field selection (:answer-field.type/radio).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 05dc7c32-8d37-5398-be0e-018937be178c | `p=-1,\text{ }q=-1` | (-h,r) | correct |

| 3a24431c-0458-5079-ba01-2125d8265013 | `p=-1,\text{ }q=-2` | (-h,−2h) | incorrect |

| 87a74df6-aa5b-55d1-9195-ebca010ca76f | `p=-2,\text{ }q=-1` | (-2h,r) | incorrect |

| 87e87cc0-c65e-58b9-830c-9fa8d6110c04 | `p=-2,\text{ }q=1` | (-2h,−r) | incorrect |

| c83b2264-9101-5cd8-bf5b-2f9a1b4b64c0 | `p=-1,\text{ }q=2` | (-h,2h) | incorrect |

### source:q-141622 — pq_plus

Field selection (:answer-field.type/radio).

| Source answer UUID | Exact source value | Parameterized component | Captured designation |

|---|---|---|---|

| 7d53fe67-7a37-5135-9bda-59dc26da7eba | `p=-5,\text{ }q=10` | (-h,2r) | incorrect |

| 9b5c7488-0854-5209-9e72-78867a6a1be6 | `p=5,\text{ }q=5` | (h,r) | incorrect |

| a2ec775e-a603-50a4-a821-b02cc8bdf4a2 | `p=-10,\text{ }q=5` | (-2h,r) | incorrect |

| 91f01cc1-7dda-5a0a-a09b-a1edcdb5224f | `p=-5,\text{ }q=5` | (-h,r) | correct |

| c0e81c67-49e3-5deb-9f3d-4bfdd5f4f433 | `p=5,\text{ }q=-5` | (h,−r) | incorrect |

## Stage 4: reusable masks, constraints, calculations

`raw_prompt`, `raw_values`, and `worked` build complete mathematical components: polynomial, square binomial, inserted h², constant and collected residual. Numeric slot substitution is never global prose replacement. Raw exact punctuation includes source `{)}` exponent grouping and the combining underbrace subscript; decoded bytes were inspected, with no alleged doubled-backslash or C0 repair. Normal direct completion adopts the grouped form of the radio/blank sources; q-141615 raw replay retains its ungrouped form. No source solution sequence is collapsed by CAS.

Normal complete radio bank is chosen as a unit before sampling: (v−h)²+r; (v+h)²+r (binomial sign error); (v−h)²+c (omit subtracting the inserted square); (v−h)²+(c−h) (subtract h rather than h²); (v−2h)²+(c−4h²) (fail to halve linear coefficient). Tuple banks convert these same whole expressions to the prompt’s plus/minus p convention. These are separately authored method errors, not claimed original bank recovery. A colliding bank rejects the whole instance. h1 radio collides, because h=h². No first-valid distractor replacement exists.

Blanks supply a single canonical required fragment per field. Normal binomial blanks add “Use a binomial whose coefficient of v is positive.” Raw source blanks omit that convention and the grader rejects h−v even though squaring it gives the same complete expression; this is a fragment-equality limitation of the observed layout. Equivalent unreduced entries equal to v−h are accepted. The convention clarifies normal output without changing raw evidence.

Finite default scope: h1..12, easy c1..144, moderate c0..144, residual nonzero; hard h3..12,c−60..−1. Same four operations at every level. Variables are aliases, excluded from task counts. Distinct eligible polynomials: easy1716, moderate1728, hard600; radio h1 is excluded by the complete bank, blank remains eligible. Positive constants up to144 and h up to12 are anchored by source c64/h9 and observed h12/c44; the ceiling keeps square arithmetic familiar and every half-coefficient integer. Hard extends familiar signed constant arithmetic, with at most60 in the original constant. It does not introduce odd-halves, fractional work, nonmonic quadratics or solving equations.

`source:<id>` profiles preserve every available original field, bank, correct designation, difficulty and solution. They are evidence-only, ineligible records. Unrated source cases receive metadata-only authored level assignments; their question difficulty attribute remains absent. Explicit source replay never fills missing fields or refs. Profile-specific guards protect spaced positive-constant masks and the absent-constant profile; complete banks reject duplicate choices. Seed changes only order, not content identity.

Content identity includes version, actual displayed prompt, full fixed solution, difficulty presence/value, field/key/type/choice presence and complete sorted banks, plus correct designation presence/value. Parameters already incorporated in displayed content do not add unused bank/profile aliases to identity. Mathematical fingerprint is independent of bank/profile/spelling and uses the assessed polynomial plus completed-expression versus p/q demand. p-sign convention and variable aliases are conservatively excluded from distinct polynomial task counts.

## Source anomalies, supported completion and fidelity denominators

q-235904: raw unrated two-blank widget, no choices, no correct refs, no worked solution. The source screenshot confirms field1 is the full binomial and field2 is after a supplied minus. Independently, y²−18y+64=(y−9)²−17, hence inferred fragments y−9 and17. Authored completion uses a supported two-blank field layout and preserves the method.

q-25253: raw unrated five-option tuple bank, no correct ref or solution. Independently expanding (y−4)²−4 gives y²−8y+12, hence p=−4,q=−4. This is an inferred correct designation, never counted as captured-ref fidelity. Its original five choices are all reproduced.

q-141615: captured easy with prompt and full solution, answer-fields absent. Independent result (x−6)²−8. Normal five-choice radio completion is authored; the raw question continues to omit answer-fields entirely.

Exact fidelity: 10/10 prompt strings, 8/8 present solution strings, 11/11 present complete field banks (31/31 exact values, including20/20 radio distractors), 10/10 present correct refs. Missing bank denominator2, missing correct-ref denominator3, fieldless denominator1, absent solutions2, unrated2. Omission parity is asserted individually, including absent choices on each q-235904 field. No mathematical source error was found. Opaque distractor intention remains unresolved evidence, not an unmatched bank. Native grading of seven complete raw questions plus three authored anomaly completions is separate from these fidelity counts.
