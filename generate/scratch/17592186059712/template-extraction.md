# Four-stage template extraction

## 1. Specific originals

- **q-18040:** a=(4,-2), b=(3,3), c=(-8,4), `a - (2b - 3c)`. Three bmatrix columns, signed integers; two scales 2 and 3, outer and inner subtraction. One five-option math radio, key selection. Difficulty, correct reference and worked solution absent. Independently derived result (-26,4).
- **q-18041:** a=(1,1), b=(4,1), c=(-1,2), `a - (2b + 5c)`. Same bmatrix prompt/field layout; inner addition, outer subtraction, scales 2 and 5. Independently derived result (-2,-11). Same attribute omissions.
- **q-70412:** a=(4,-7), b=(2,4), c=(4,-6), `3a-(b+4c)`. Compact bracketed aligned column notation, source moderate. No fields. Shared componentwise opening; formal substituted column expression → evaluated (12,-21), (2,4), (16,-24) → inner (18,-20) → final (-6,-1). Four rows exactly.
- **q-70414:** a=(-1,1), b=(2,5), c=(1,2), `a+(2b-2c)`. Same compact notation, source moderate. No fields. Same opening; substituted expression → individually evaluated (-1,1), (4,10), (2,4) → collected inner (2,6) → final (1,7). Four rows exactly.

No source math error was found in either complete solution or any inferred correct value. Missing attributes are source-format anomalies, distinct from mathematics. Decoded source commands have one ord-92 byte; matrix row separators have two. JSON/tool escaping does not establish any doubled-command anomaly; no TeX escape repair is claimed.

## 2. Shared mathematical pattern

Compute `k a + o(q b + i r c)` componentwise, with outer/inner signs o,i in {−1,+1}, three supplied 2D columns, and exactly two nonunit factors at observed moderate. One complete column is the requested answer. Keep source signs/unit placement as family masks; vector components and actual nonunit coefficients are complete slots. The two source presentation styles are retained. The shared solution performs exactly substitution, scalar products, collection of the inner vector, and the final outer component operation. There is one fixed solution independent of chosen distractor.

The authored easy mask is `a+qb` with one nonunit factor and three corresponding stages. Authored hard uses the same nested masks with all three scales nonunit and at least one negative; coefficient grouping prevents ambiguous numeric juxtaposition and bare double signs.

## 3. Components and every source choice

`R = k a + o(q b + i r c)` is independently calculated. Historical options are represented by exact parameterized residual-vector operations `R + d`. This reproduces the bank for changed operands without a source-answer lookup or literal question-return branch. It does **not** establish the historical author’s intended mistake: residuals have no general misconception claim and both banks are evidence-only, including completed versions.

| Source/profile | Field | Exact observed choice | Parameterized operation | Independent designation |
|---|---|---|---|---|
| raw-q-18040 | selection/radio | (-26,4) | R+(0,0) | correct, inferred |
| raw-q-18040 | selection/radio | (-21,6) | R+(5,2) | wrong; opaque |
| raw-q-18040 | selection/radio | (34,-8) | R+(60,-12) | wrong; opaque |
| raw-q-18040 | selection/radio | (34,4) | R+(60,0) | wrong; opaque |
| raw-q-18040 | selection/radio | (-26,-8) | R+(0,-12) | wrong; opaque |
| raw-q-18041 | selection/radio | (-2,-13) | R+(0,-2) | wrong; opaque |
| raw-q-18041 | selection/radio | (4,13) | R+(6,24) | wrong; opaque |
| raw-q-18041 | selection/radio | (-1,-11) | R+(1,0) | wrong; opaque |
| raw-q-18041 | selection/radio | (-4,-11) | R+(-2,0) | wrong; opaque |
| raw-q-18041 | selection/radio | (-2,-11) | R+(0,0) | correct, inferred |

Every option matches its whole two-component vector; 10/10 displayed values, 8/8 independently wrong vectors and 2/2 complete banks. Zero original correct designations exist to match. The authoritative widgets independently confirm each value. No modern source options exist to extract.

Normal nested **authored-component-operations** bank is chosen whole before parameters:

1. `k a + o(q b + i r c)` (correct).
2. `k a - o(q b + i r c)` (reverse outer operation).
3. `k a + o(q b - i r c)` (reverse inner operation).
4. `k a + o(b + i r c)` (omit b scale), except the observed unit-b family uses `a + o(q b + i r c)` (omit left scale). Eligibility is selected by family before parameters.
5. `k a + o(q b + i c)` (omit c scale).

Normal easy whole bank: `a+qb`, `a-qb`, `a+b`, `a+(q b_x,b_y)`, `a+(b_x,q b_y)`. All errors concern the actual required sum/scalar multiplication. No arbitrary perturbation of correct values appears in learning banks, no added distractor diagnosis appears in learner prose. Any collision rejects the whole parameter instance, including explicit calls; no replacement from a pooled list.

## 4. Reusable masks, constraints and validation

Fixed: original prose layout, variable letters a/b/c, column notation, exact response shape, source shared opening and ordered stages. Variable: complete vector columns and coefficient tokens. Conditional: omit printing unit factor 1; group negative factors; source raw presence follows the snapshot. `source-cases.json` maps all four original cases through public `generate` with raw profiles. `completed-<source-id>` keeps the original bank when present and adds clearly inferred fields/ref/solution; these records are evidence-only.

For every normal and explicit authored input, enforce classification workload and magnitude bounds. Finite witness enumeration uses component set {−2,1} and bounded coefficient sets, counts valid complete banks, and canonicalizes effective coefficients of each supplied vector: scalar/sign spelling aliases and presentation/profile aliases never inflate task counts. Production integer domains are larger. Content identity separately includes actual difficulty, prompt, fixed solution, complete bank, attribute presence and version; seed/order cannot alter it. Field and answer UUIDs are owned under content identity. Complete bank changes alter identity.

`validate.py` independently parses actual printed prompt columns and coefficients, each substituted operand, each separately evaluated scalar product, each collected inner component, final column and every displayed equality. Authored wrong banks are separately recomputed from the printed operands and published operation. Exact source prose/stage sequence, field types, answer types, option counts, bank values and attribute presence are compared. Formatting, scope, deterministic identity, default family/position coverage, rejected explicit workload collapse, and native radio grading are checked separately. Source omissions and opaque interpretation limits cannot count as recovered fidelity.
