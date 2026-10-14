# Template extraction

Database `math`, basis1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Source/topic/lesson wrappers copied without changes. Canonical example e-9557 is contextual evidence, not a practice question.

## 1. Specific source descriptions

| Source | Label | Family | Supplied values | Orientation corrections | Solution rows |
|---|---|---|---|---|---|
| q-126558 | unrated | positive_legacy | 10, -4, -2 | (1, 1, 1) | absent |
| q-126654 | :question.difficulty/moderate | all_ccw | 1, 5, -3 | (1, -1, -1) | symbolic positive sum → signed substitution → collected scalar |
| q-126862 | :question.difficulty/easy | positive | 9, -4, -6 | (1, 1, 1) | symbolic positive sum → signed substitution → collected scalar |
| q-126863 | :question.difficulty/easy | positive | 1, 7, -4 | (1, 1, 1) | symbolic positive sum → signed substitution → collected scalar |
| q-126865 | :question.difficulty/moderate | inner3_reverse | 7, -9, 1 | (1, 1, -1) | symbolic positive sum → signed substitution → collected scalar |
| q-126867 | :question.difficulty/moderate | all_reverse | 6, 2, -10 | (-1, -1, -1) | symbolic positive sum → signed substitution → collected scalar |
| q-126870 | :question.difficulty/moderate | outer_inner3_reverse | 5, -2, -9 | (-1, 1, -1) | symbolic positive sum → signed substitution → collected scalar |
| q-126868 | :question.difficulty/moderate | outer_reverse | 4, -6, -8 | (-1, 1, 1) | symbolic positive sum → signed substitution → collected scalar |
| q-126864 | :question.difficulty/moderate | inner2_reverse | 2, 9, 8 | (1, -1, 1) | symbolic positive sum → signed substitution → collected scalar |
| q-126855 | :question.difficulty/easy | positive | 4, 9, -5 | (1, 1, 1) | symbolic positive sum → signed substitution → collected scalar |
| q-126861 | :question.difficulty/easy | positive | 7, -3, 2 | (1, 1, 1) | symbolic positive sum → signed substitution → collected scalar |

All original supplied numbers are nonzero integers of magnitude≤10. C1 is the outer curve; C2/C3 are distinct holes. The vector field is arbitrary, defined on the shown region; no formula for it is used. Every modern prompt has one display equation block with three supplied circulations, then an orientation sentence and a requested boundary circulation. The legacy prompt uses one inline math expression and malformed parenthesized underscore notation; raw replay preserves it exactly, while normal completion uses canonical braced subscripts and the differential text command.

## 2. Shared pattern

Add the circulations along the positively oriented components of the boundary: outer CCW and holes CW. Each supplied circulation is kept or negated according to its stated traversal. The response is one exact scalar. Geometry distinguishes the outer curve and hole labels; shape/size has no role in the arithmetic.

## 3. Components and complete bank mappings

The following recipes instantiate every option through the normal public generator. A coefficient triple means c1*a+c2*b+c3*c, with a,b,c the actual displayed circulation operands in order. The matched numeric scalar underdetermines author intent even when a natural sign-mask recipe exists. Correct-ref fidelity is counted separately from inferred mathematics. Opaque scaled values are restricted to common scaling of the complete displayed source operand triple; this is a transparent evidence parameterization, not a recovered mistake model. These profiles are never selected by default.

### q-126558

Profile `observed:q-126558`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $2π$ | original key absent | 2π*k, values=k*(10,-4,-2) |
| $10$ | original key absent | (1, 0, 0) |
| $4$ | original key absent | (1, 1, 1) |
| $16$ | original key absent | (1, -1, -1) |
| $0$ | original key absent | (0, 0, 0) |

### q-126654

Profile `observed:q-126654`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $1$ | incorrect | (-1, 1, 1) |
| $9$ | incorrect | (1, 1, -1) |
| $-1$ | correct | (1, -1, -1) |
| $-6$ | incorrect | (-1, -1, 0) |
| $3$ | incorrect | (1, 1, 1) |

### q-126862

Profile `observed:q-126862`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $11$ | incorrect | (1, 1, -1) |
| $19$ | incorrect | (1, -1, -1) |
| $7$ | incorrect | (1, -1, 1) |
| $1$ | incorrect | (-1, -1, -1) |
| $-1$ | correct | (1, 1, 1) |

### q-126863

Profile `observed:q-126863`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $12$ | incorrect | (1, 1, -1) |
| $-10$ | incorrect | (1, -1, 1) |
| $2$ | incorrect | (-1, 1, 1) |
| $4$ | correct | (1, 1, 1) |
| $-2$ | incorrect | (1, -1, -1) |

### q-126865

Profile `observed:q-126865`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $-5$ | incorrect | −5*k, values=k*(7,-9,1) |
| $15$ | incorrect | (1, -1, -1) |
| $17$ | incorrect | (1, -1, 1) |
| $-3$ | correct | (1, 1, -1) |
| $-1$ | incorrect | (1, 1, 1) |

### q-126867

Profile `observed:q-126867`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $12$ | incorrect | (0, 1, -1) |
| $14$ | incorrect | (1, -1, -1) |
| $2$ | correct | (-1, -1, -1) |
| $-2$ | incorrect | (1, 1, 1) |
| $-6$ | incorrect | (1, -1, 1) |

### q-126870

Profile `observed:q-126870`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $12$ | incorrect | (1, 1, -1) |
| $-16$ | incorrect | (-1, 1, 1) |
| $16$ | incorrect | (1, -1, -1) |
| $2$ | correct | (-1, 1, -1) |
| $6$ | incorrect | (-1, -1, -1) |

### q-126868

Profile `observed:q-126868`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $10$ | incorrect | (-1, -1, -1) |
| $-6$ | incorrect | (-1, -1, 1) |
| $-2$ | incorrect | (-1, 1, -1) |
| $-18$ | correct | (-1, 1, 1) |
| $-10$ | incorrect | (1, 1, 1) |

### q-126864

Profile `observed:q-126864`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $1$ | correct | (1, -1, 1) |
| $3$ | incorrect | (1, 1, -1) |
| $19$ | incorrect | (1, 1, 1) |
| $-1$ | incorrect | (-1, 1, -1) |
| $-15$ | incorrect | (1, -1, -1) |

### q-126855

Profile `observed:q-126855`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $8$ | correct | (1, 1, 1) |
| $18$ | incorrect | (1, 1, -1) |
| $-10$ | incorrect | (1, -1, 1) |
| $-4$ | incorrect | (0, -1, -1) |
| $12$ | incorrect | 12*k, values=k*(4,9,-5) |

### q-126861

Profile `observed:q-126861`, radio `selection`, exactly five choices.

| Original value | Designation | Parameterized recipe |
|---|---|---|
| $8$ | incorrect | (1, -1, -1) |
| $6$ | correct | (1, 1, 1) |
| $12$ | incorrect | (1, -1, 1) |
| $3$ | incorrect | (0, -1, 0) |
| $2$ | incorrect | (1, 1, -1) |

## 4. Reusable masks and constraints

Fixed: all shared prose, variable/curve notation, diagram geometry and placement, per-family orientation sentences, reversal notices, radio shape, number of choices, and three ordered worked-solution stages. Variable: complete RHS circulation scalars, the signed substitution operands, and collected scalar. Conditional: parentheses around each negative operand, omission of legacy raw difficulty/key/solution, and authored completion for default legacy output. Original source prefixes/suffixes are operative masks; numeric RHS slots are replaced only after complete circulation equations, never globally across text.

Every family’s symbolic sum keeps its own ordered signs. Default solutions retain the entire corresponding source prose and reversal notice at changed values; they do not introduce helper letters or collapse the sum. Hard keeps the three source stages and adds an explicit common-denominator row with each individually scaled signed numerator before final collection.

Authored banks are selected whole: `method_signs` = correct plus individually reversed C1/C2/C3 contribution signs and complete traversal reversal; `method_omissions` = correct plus each individually omitted component and complete traversal reversal. All five results must be pairwise unequal, and exactly one must equal the positive sum; otherwise the whole parameter instance is rejected. No individual option replacement or distractor diagnoses.

Easy: mixed signed nonzero integers |v|≤10 and all-positive supplied traversals. Moderate: same numeric bounds and six observed reversal arrangements. Hard: all operands reduced noninteger halves/thirds, both denominators represented, mixed signs, |v|≤10 and |numerator|≤29. Public explicit inputs enforce the same guards. Raw profiles are separate evidence and permit bounded rational scaling, preserving original attribute presence.

Presentation identity includes actual prompt, solution, difficulty presence, correct-ref presence and sorted complete bank. Mathematical fingerprints retain the outer operand/orientation and the unordered hole operand/orientation pairs; diagram, profile, aliases and simultaneous C2/C3 relabeling are excluded. Finite eligible counts appear in validation.json.
