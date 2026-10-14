# Template extraction

## 1. Specific source descriptions

| Source | Observed level | Ordered matrix rows | Fields and complete banks | Stages |
|---|---|---|---|---|
| q-20051 | unrated | [(3, 1, -3), (2, 6, -2), (0, 1, -4)] (a,b,c) | radio selection: [-68, -58, -64, -72, -70]; correct=ABSENT | 0 |
| q-20056 | moderate | [(1, -4, 1), (3, -3, 2), (2, -1, 0)] (r,q,p) | radio selection: [-8, 14, -13, 11, -11]; correct=ABSENT; radio selection: [-11, -8, 11, 14, -13]; correct=-11 | 5 |
| q-128107 | easy | [(0, 9, 3), (3, 2, 0), (-1, 1, 1)] (a,b,c) | radio selection: [12, -27, 15, -12, 42]; correct=-12 | 5 |
| q-128347 | moderate | [(1, 2, -2), (3, 0, 5), (7, 4, 9)] (q,r,p) | radio selection: [-60, -28, 12, 20, -20]; correct=-28 | 5 |
| q-18657 | easy | [(-2, 0, 1), (5, 2, -4), (1, 0, 3)] (a,b,c) | radio selection: [-2, 12, 2, -14, 0]; correct=-14 | 5 |
| q-20050 | easy | [(1, 3, 2), (3, 4, 1), (2, 0, 1)] (a,b,c) | radio selection: [-15, -17, 17, -14, -19]; correct=-15 | 5 |
| q-20054 | easy | [(1, -1, 2), (2, 0, 3), (2, 4, 2)] (a,b,c) | radio selection: [-3, -4, 2, -12, 0]; correct=2 | 5 |
| q-317312 | moderate | [(2, -1, 3), (0, 4, 1), (-2, 1, 5)] (a,b,c) | blank field-1: [64]; correct=64 | 6 |
| q-317315 | moderate | [(1, 2, 3), (4, 0, 1), (-2, -1, 5)] (a,b,c) | blank field-1: [-55]; correct=-55 | 6 |
| q-317316 | moderate | [(0, 2, 5), (3, 1, 0), (4, -1, -2)] (a,b,c) | blank field-1: [-23]; correct=-23 | 6 |
| q-317317 | easy | [(1, 2, 3), (4, 0, -2), (5, 6, 1)] (a,b,c) | blank field-1: [56]; correct=56 | 6 |
| q-317319 | easy | [(2, 1, 3), (1, 4, 0), (6, -1, 2)] (a,b,c) | blank field-1: [-61]; correct=-61 | 6 |
| q-317320 | easy | [(1, 0, 2), (3, 1, 0), (4, 2, 5)] (a,b,c) | blank field-1: [9]; correct=9 | 6 |
| q-317322 | easy | [(2, 1, 0), (0, 3, 4), (5, 2, 1)] (a,b,c) | blank field-1: [10]; correct=10 | 6 |
| q-317325 | moderate | [(-1, -2, 3), (4, -1, -2), (1, 2, -3)] (a,b,c) | blank field-1: [0]; correct=0 | 6 |
| q-73461 | moderate | [(2, -1, 0), (1, -2, 4), (3, -2, 1)] (q,r,p) | radio selection: [1, 23, -23, 12, -11]; correct=1 | 5 |
| q-73462 | moderate | [(4, 1, -2), (1, -2, 1), (3, 1, 2)] (r,q,p) | radio selection: [-14, 10, -30, -33, -20]; correct=-33 | 5 |
| q-317321 | easy | [(0, 2, 1), (2, 0, 3), (1, 4, 5)] (a,b,c) | blank field-1: [-6]; correct=-6 | 6 |
| q-275350 | moderate | [(-4, -1, 2), (-2, 3, 1), (5, -2, -1)] (r,q,p) | blank field-1: [-21]; correct=-21 | 6 |
| q-20053 | easy | [(-2, 2, -3), (2, -1, 2), (-2, 1, 1)] (a,b,c) | radio selection: [-6, 8, -10, 6, -4]; correct=-6 | 5 |
| q-317318 | easy | [(-1, 2, 4), (0, 3, 1), (2, 5, 0)] (a,b,c) | blank field-1: [-15]; correct=-15 | 6 |
| q-317313 | moderate | [(1, -3, 0), (-2, 2, 0), (2, 0, -4)] (a,b,c) | blank field-1: [16]; correct=16 | 6 |
| q-317326 | moderate | [(-2, 0, -1), (-3, -1, 4), (5, -2, -2)] (a,b,c) | blank field-1: [-31]; correct=-31 | 6 |

## 2. Shared mathematical pattern

For actual requested order (u,v,w), form rows u,v,w, expand +u₁M₁−u₂M₂+u₃M₃, evaluate each 2×2 determinant by ad−bc, collect signed cofactor terms, return a scalar integer. Preserve each family’s optional evaluated-minor/product stage and zero/unit reduction. Scalar blank values contain no delimiters. Radio banks contain five scalar integers.

## 3. Components and complete choice mapping

Each source has its own observed:<source_id> bank profile. At replay scale s, the first requested row stays fixed and both lower rows multiply by s; individual lower entries multiply by s, every minor/product/collected scalar multiplies by s². Every historical scalar option is the homogeneous evidence recipe source_value×s². This reproduces its complete source bank without claiming the original author’s error intent. These opaque profiles are evidence_only=true and eligible_for_learning=false even when mathematically valid. They are never normal defaults. This finite replay domain {1,2} is not claimed as sufficient normal practice variety.

### q-20051

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: False.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -68 | (-68)s² | historical scalar; error operation unresolved |
| -58 | (-58)s² | historical scalar; error operation unresolved |
| -64 | (-64)s² | historical scalar; error operation unresolved |
| -72 | (-72)s² | historical scalar; error operation unresolved |
| -70 | (-70)s² | historical scalar; error operation unresolved |
### q-20056

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: False.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -8 | (-8)s² | historical scalar; error operation unresolved |
| 14 | (14)s² | historical scalar; error operation unresolved |
| -13 | (-13)s² | historical scalar; error operation unresolved |
| 11 | (11)s² | historical scalar; error operation unresolved |
| -11 | (-11)s² | historical scalar; error operation unresolved |

Field 1 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -11 | (-11)s² | correct determinant |
| -8 | (-8)s² | historical scalar; error operation unresolved |
| 11 | (11)s² | historical scalar; error operation unresolved |
| 14 | (14)s² | historical scalar; error operation unresolved |
| -13 | (-13)s² | historical scalar; error operation unresolved |
### q-128107

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 12 | (12)s² | historical scalar; error operation unresolved |
| -27 | (-27)s² | historical scalar; error operation unresolved |
| 15 | (15)s² | historical scalar; error operation unresolved |
| -12 | (-12)s² | correct determinant |
| 42 | (42)s² | historical scalar; error operation unresolved |
### q-128347

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -60 | (-60)s² | historical scalar; error operation unresolved |
| -28 | (-28)s² | correct determinant |
| 12 | (12)s² | historical scalar; error operation unresolved |
| 20 | (20)s² | historical scalar; error operation unresolved |
| -20 | (-20)s² | historical scalar; error operation unresolved |
### q-18657

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -2 | (-2)s² | historical scalar; error operation unresolved |
| 12 | (12)s² | historical scalar; error operation unresolved |
| 2 | (2)s² | historical scalar; error operation unresolved |
| -14 | (-14)s² | correct determinant |
| 0 | (0)s² | historical scalar; error operation unresolved |
### q-20050

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -15 | (-15)s² | correct determinant |
| -17 | (-17)s² | historical scalar; error operation unresolved |
| 17 | (17)s² | historical scalar; error operation unresolved |
| -14 | (-14)s² | historical scalar; error operation unresolved |
| -19 | (-19)s² | historical scalar; error operation unresolved |
### q-20054

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -3 | (-3)s² | historical scalar; error operation unresolved |
| -4 | (-4)s² | historical scalar; error operation unresolved |
| 2 | (2)s² | correct determinant |
| -12 | (-12)s² | historical scalar; error operation unresolved |
| 0 | (0)s² | historical scalar; error operation unresolved |
### q-317312

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 64 | (64)s² | correct determinant |
### q-317315

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -55 | (-55)s² | correct determinant |
### q-317316

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -23 | (-23)s² | correct determinant |
### q-317317

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 56 | (56)s² | correct determinant |
### q-317319

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -61 | (-61)s² | correct determinant |
### q-317320

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 9 | (9)s² | correct determinant |
### q-317322

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 10 | (10)s² | correct determinant |
### q-317325

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 0 | (0)s² | correct determinant |
### q-73461

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 1 | (1)s² | correct determinant |
| 23 | (23)s² | historical scalar; error operation unresolved |
| -23 | (-23)s² | historical scalar; error operation unresolved |
| 12 | (12)s² | historical scalar; error operation unresolved |
| -11 | (-11)s² | historical scalar; error operation unresolved |
### q-73462

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -14 | (-14)s² | historical scalar; error operation unresolved |
| 10 | (10)s² | historical scalar; error operation unresolved |
| -30 | (-30)s² | historical scalar; error operation unresolved |
| -33 | (-33)s² | correct determinant |
| -20 | (-20)s² | historical scalar; error operation unresolved |
### q-317321

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -6 | (-6)s² | correct determinant |
### q-275350

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -21 | (-21)s² | correct determinant |
### q-20053

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (selection), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -6 | (-6)s² | correct determinant |
| 8 | (8)s² | historical scalar; error operation unresolved |
| -10 | (-10)s² | historical scalar; error operation unresolved |
| 6 | (6)s² | historical scalar; error operation unresolved |
| -4 | (-4)s² | historical scalar; error operation unresolved |
### q-317318

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -15 | (-15)s² | correct determinant |
### q-317313

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| 16 | (16)s² | correct determinant |
### q-317326

Fixed components: original prose, operator order, scalar layout, optional stage sequence. Variable slots: three bottom-row components per lower vector, matrices/minors, substituted products, evaluated minor/products, collected terms and scalar answer. Raw replay uses only scale to avoid inventing opaque distractor transformations.

Field 0 (field-1), presence of correct ref: True.

| Original complete value | Parameterized evidence recipe | Interpretation |
|---|---|---|
| -31 | (-31)s² | correct determinant |

## 4. Reusable masks and normal extension

Prompt masking acts only within complete vector components. Raw digit-degree masks preserve exact anchor whitespace, prose and arithmetic-stage expressions. No literal source-payload or answer-table branch supplies the answer. Raw source keys retain individual presence: q-20051 omits difficulty, worked solution and correct ref; q-20056 preserves both duplicate fields and its missing legacy correct ref. Changed scale replay is independently checked from displayed vectors and every operative arithmetic row.

Normal defaults select a source family and complete bank before independent integer coordinates. Signed/zero coordinate forms are retained; omitted top-row unit coefficients stay fixed. Samples use magnitudes1…6; explicit inputs permit observed arithmetic ceiling9 for easy/moderate. Hard uses signed nonzero magnitudes2…6, with first-row magnitudes4…6. Explicit calls enforce all bounds. Normal solutions retain the common source opening, row-order statement, determinant/cofactor/substituted minor/collection sequence. Blank source masks include an evaluated-minor row; q-275350 includes evaluated individual products instead. Safe grouping/visible multiplication normalize notation under changed signs.

Authored cofactor_signs bank: det; −det (swap two rows/columns); det−2Tⱼ for the first structurally active cofactor (wrong cofactor sign); M₁−M₂+M₃ (omit first-row coefficients); and expansion using ad+bc for each minor. Authored omit_terms bank: det; −det; det−Tⱼ for the first structurally active cofactor; det−Tₖ for the second active cofactor; M₁−M₂+M₃. T=(u₁M₁,−u₂M₂,u₃M₃). These five options are fixed together before parameters; any equality rejects the whole instance. No first-valid pool or generic scalar perturbation is used. Source field type/count stays the default for each family. Explicit field_type overrides are authored layouts.

## Source anomalies, repairs and denominators

- q-20051: EDB prompt has b·c, so its nested scalar dot product is undefined; no difficulty, solution or key. The authoritative lesson widget question20051 shows b×c, identical bank. Direct SymPy determinant is −64. Raw evidence retains all omissions and malformed text; normal prompt repairs ×, adds an authored moderate label and computed solution/field. No absent original key counts as a matched designation.
- q-20056: authoritative lesson widget is one five-choice radio. Two captured fields have identical complete value sets; first is legacy and lacks a key. Raw preserves both; normal uses one supported field and independently computed −11. Both raw banks are counted, the absent key is not fabricated.
- q-275350 and q-317318: captured blank prompts end with the displayed answer (−21 / −15), missing {{field-1}}. Raw evidence preserves this presentation error; normal replaces the answer disclosure with the matching placeholder. All raw original values and present solution strings still match exactly.

Counts:23 exact raw prompts,22 exact present solutions,24 complete raw fields/banks,68 complete values,22 present correct designations,2 absent correct refs preserved. Source mathematics denominator22 excludes the malformed q-20051 record. Normal repairs are counted separately from raw reproduction. Lesson widget evidence is copied privately as lesson-widget-source.json. No plots or image assets appear in prompt/banks/solutions.

Authored hard is disjoint from normal observed families: all moderate source forms retain a unit/zero first-row component; easy dense q-20053 caps all first-row magnitudes at3, enforced in sampling and explicit calls. Hard requires all first-row magnitudes4…6 and every lower entry magnitude2…6.
