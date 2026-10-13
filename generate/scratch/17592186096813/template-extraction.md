# Template extraction: four stages

Source provenance is the unchanged math basis-1356 wrapper in `source.json`; canonical and lesson-context provenance are the same captured basis. Practice sources have no worked solutions. The canonical solution supplies shared prose for separately authored normal output, not recovered practice solutions.

## 1. Specific descriptions before generalization

**q-11376:** “The vector $a$ has magnitude $5$. Find a unit vector that is parallel to $a$.” One radio field (`selection`, UUID `45156f70-5185-5291-966e-5fa7eea23fa2`). Five mathematical answer expressions, one scalar and four scalar multiples of a. Positive integer magnitude 5; no coordinates, diagrams, components, sums, or hidden magnitude computation. No correct lookup, solution or difficulty attribute.

**q-12202:** “The vector $AB^(→)$ has magnitude $7$. Which of the following is a unit vector that is parallel to $AB^(→)$?” One radio field (`selection`, UUID `ffccd89c-0549-5a01-82df-21cfa90868da`). Five mathematical answer expressions: original direction, its negative, one reciprocal multiple, and two signed multiples of the reversed directed vector BA. Positive integer magnitude 7. No correct lookup, solution or difficulty attribute. Literal `AB^(→)` is raw captured notation; reversed BA denotes -AB.

**Canonical e-4282:** Bold abstract a, supplied magnitude 3, and prose “To obtain the unit vector that is parallel to …, we divide … by its length:” followed by `u=a/|a|=(1/3)a`. It is not counted as a practice question. Its one normalization operation anchors authored solutions and levels.

## 2. Shared mathematical pattern and purpose

Given a nonzero abstract vector v whose positive magnitude m is already stated, identify a scalar multiple with magnitude 1. Parallelism is guaranteed for nonzero multiples; unit length requires absolute scalar 1/m. Both orientations are eligible. No bank has -v/m, so the selected displayed answer is uniquely v/m.

Named and endpoint-arrow prompt structures remain distinct observed templates even though they share the operation. All choices are whole vector expressions or whole scalar expressions, not answer fragments. Both fields are radio fields, not blanks.

## 3. Complete component and choice-bank mapping

Every row below belongs to the single original selection field of its question. Full source UUIDs, answer types and unmodified question fields are retained in `source.json` and each `source-cases.json` raw source. Recipes are expression masks over supplied magnitude m and the complete vector slot; replay never returns source payloads or uses a numerical answer lookup.

| Source/profile | Exact observed value | Complete mask | Mathematical object at original m | Interpretation status |
|---|---|---|---|---|
| q-11376 / raw_named | `5a` | m·a | magnitude 25 | multiplying instead of dividing is defensible; raw bank remains evidence-only |
| q-11376 / raw_named | `\frac{1}{5}` | 1/m | scalar, not a vector | omitted vector factor |
| q-11376 / raw_named | `\frac{1}{10}a` | a/(2m) | magnitude 1/2 | observed mask; intended error unresolved |
| q-11376 / raw_named | `\frac{1}{20}a` | a/(4m) | magnitude 1/4 | observed mask; intended error unresolved |
| q-11376 / raw_named | `\frac{1}{5}a` | a/m | magnitude 1 | mathematically inferred unique eligible option; observed key absent |
| q-12202 / raw_directed | `AB^(→)` | v | magnitude 7 | no normalization |
| q-12202 / raw_directed | `7BA^(→)` | m·reverse(v) = -m·v | magnitude 49 | reverse and multiply |
| q-12202 / raw_directed | `-AB^(→)` | -v | magnitude 7 | negate without normalization |
| q-12202 / raw_directed | `\frac{1}{7}AB^(→)` | v/m | magnitude 1 | mathematically inferred unique eligible option; observed key absent |
| q-12202 / raw_directed | `-7BA^(→)` | -m·reverse(v) = m·v | magnitude 49 | negate reversed multiple |

The two magnitude-49 directed choices have opposite directions and are unequal vectors. Magnitude equality alone cannot establish vector equality. All ten whole displayed source objects match raw replay exactly. Correct-designation fidelity has denominator zero (two missing), rather than claiming a 2/2 key match.

## 4. Reusable templates, slots and constraints

Fixed source prompt sentences use complete vector and magnitude slots. Named: `The vector $VECTOR$ has magnitude $MAGNITUDE$. Find a unit vector that is parallel to $VECTOR$.` Directed: the same introduction followed by `Which of the following is a unit vector that is parallel to $VECTOR$?` Only full slots are substituted; vector letters are never replaced across commands such as `\frac`.

Raw evidence profiles require matching named/directed template, authored easy context and integer magnitude 2…30. They preserve no correct ref, no solution and no question rating. Full masks above also generate changed-parameter evidence variants, but unresolved source error intent does not become a normal teaching recipe.

Normal **normalization** bank: `[m·v, 1/m (scalar), v/m², v, v/m]`; each wrong operation is explicitly authored from the normalization method. Normal **direction_errors** bank: `[v, -v, m·v, -m·v, v/m]`; these are no normalization, sign reversal, multiplication, negated multiplication, and correct normalization. Exactly five complete choices are derived together. m>1 makes all complete expressions distinct and leaves only v/m eligible; the scalar is never misclassified as a vector. No random unrelated offsets or polynomial interpolation is used.

Normal solution uses the canonical shared sentence and equality sequence. Easy: `u=v/|v|=(1/m)v`. Moderate/hard: `u=v/|v|=(1/m)v=(simplified reciprocal)v`. The first substituted reciprocal remains structurally unsimplified, including the stated rational or radical magnitude. Every actual printed row is independently checked. No chosen-answer-dependent feedback or diagnosis is invented.

All bounds in classification apply to explicit inputs and sampling. Names (`a,b,c,v,w`) and endpoints (`AB,CD,PQ,RS`) are complete notation variants. Seed changes cannot alter identity at fixed components; the mathematical fingerprint excludes these aliases and complete answer banks. Presentation identity includes actual prompt, solution, full answer bank, type and authored rating. All normal outputs use balanced math delimiters/braces and valid LaTeX directed-vector notation. Sources with missing keys remain excluded from normal learning eligibility, while normal authored questions receive independently verified keys and solutions.
