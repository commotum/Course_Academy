# Four-stage template extraction

## 1. Describe the original questions

`source-cases.json` records all eleven practice instances, their exact six ordered numerical slots and names. `bank-map.json` records each of the51 displayed values, its owning field, original UUID, complete expression recipe, original correct-ref presence and designation. The ten original solutions all use the same shared prose and two separate aligned equations: first-row substitution → first-row reduction with a star retained below → second-row substitution with first result retained above → full result → Therefore conclusion. Named-blank alone prefixes both equations with the matrix/vector label. Inline families conclude with the full matrix product; named families conclude with the named product.

Four source masks condition negative-factor grouping: q-13555 and q-13565 print negative vector entries without parentheses; q-275589 prints its negative first coefficient in the second row without parentheses; the other masks parenthesize negative factors. Positive factors always retain visible `\cdot`, so changed signs cannot turn a product into concatenation. These styles are parameterized, not literal anchor payloads.

q-13566 has no solution at all. Its evidence replay omits it and its original difficulty. New normal what-radio instances receive a clearly authored solution using the established two-row backbone. The two inline blank captures list field-2 before field-1; faithful replay retains this collection order while its actual table placeholders preserve top/bottom roles.

Decoded-byte inspection found exactly **one** actual slash before each source bank's begin command. JSON/tool escaping is not an anomaly. No doubled-command repair is claimed. Shared `normalize_prose`, `normalize_tex`, and `matrix_tex` run before content identity; normalized source prompt and all ten existing solutions compare exactly at anchors.

## 2. Generalized family

Supply a2×2 numeric matrix and ordered2×1 numeric column vector; calculate both row dot products and return the complete ordered column vector through five-choice radio or two scalar blanks. The source named/inline/what masks preserve their original instructional wording and answer shapes. Every sampled instance has one complete worked solution independent of any chosen error.

## 3. Component and bank mapping

The six mathematical slots are a,b in the first row, c,d in the second row, and u,v in the column. Define r=a·u+b·v and t=c·u+d·v. `bank-map.json` maps every original value to its expression and owner. The complete original banks are:

| Profile | Complete ordered expression bank (choice order may shuffle) |
|---|---|
| q-13564 | (r,t), (-r,-t), (r,-t), (-r,t), (v,u) |
| q-126511 | (r,t), (a+b,c+d), (-a-b,-c-d), (t,r), (a,c) |
| q-126512 | (r,t), opaque slot z=(1,-2), (a·u,c·u), (b·u,d·u), (a·u+c·v,b·u+d·v) |
| q-13555 | (r,t), (r,r), (r,-t), (-r,-t), (-r,t) |
| q-13565 | (r,t), (-t,-r), (r,-t), (-r,-t), (-t,r) |
| q-13629 | (r,t), (r+1,t), (r,t-1), (r,t+1), (r-1,t-1) |
| q-13560 | (r,t), (r+1,t), (t,r), (r,r), (t,t) |
| q-13566 | (r,t), (r,-t), (-r,-t), (t,r), opaque slot z=(19,12) |
| scalar blanks | field-1=r; field-2=t |

Expression agreement is evidence of numerical reproduction, not proof of the original author's intended learner mistake. In particular the unexplained offsets and opaque slots are never promoted to normal learning. Every observed bank remains available through `generate(..., profile='observed:<id>', parameters=...)`, including changed parameters, and is marked `evidence_only=true` and `eligible_for_learning=false`. Opaque vector slots must be explicitly supplied; there is no source-ID answer lookup and no source-payload return branch.

Normal radio sampling selects a complete eligible bank before parameters. Named-radio serves the defensible complete q-13564, q-126511 and q-13565 operation patterns, alongside the authored-method bank. Inline-radio serves q-13555 plus authored-method. What-radio serves authored-method. The latter bank is (r,t), the transposed-matrix product, the first-column contribution, the second-column contribution, and swapped outputs. All wrong values come from actual displayed operands. Source-specific prose and operative stages remain intact for recovered normal profiles at changed values. Blank layouts preserve scalar answer fragments and exact field-key roles.

## 4. Reusable backbone and slots

**Fixed:** dimensions2×2 and2×1, right multiplication, two ordered output components, source-shaped prompt mask/response contract, complete chosen bank size, first-row then second-row staged solution and concluding product. Requesting the complete vector is essential to this KP: there is no eligible cell/target-selection slot and no invitation to vary the requested operation.

**Variable:** the six numeric slots under the per-level bounds in classification; supported matrix names A,Z,X,H and vector names x,y,n,a for named masks; complete eligible bank profile; deterministic displayed choice order. Matrix and vector roles are checked from actual learner text. Labels change the prompt and final named conclusion together while math-task identity remains fixed. A simultaneous column swap accompanied by the same vector-coordinate swap has the same row-dot-product task fingerprint. Labels, layout, profile and option shuffle are excluded from task counts.

**Conditional:** negative-parenthesis source style; omitted difficulty/solution/correct attributes and duplicated field only in raw observed evidence; empty answer-bank profile for scalar blanks. **Dependent:** both outputs, each individual factor, all multiply signs/addition signs, retained first-row result, final vector and all normal wrong operations. Whole instances are rejected when any two complete bank values are equal, including two wrong answers. No first-valid distractor replacement is used.

Validation reads displayed matrices and exact term tokens independently, checks their dimensions and roles, evaluates all four cell products and the two row sums, checks every retained component and final conclusion, and validates every full-bank pair. Removing a required multiply stage while preserving final answers is a failing mutation. Ordinary newline/tab layout is permitted; unintended C0 characters fail the public guard. Content identity includes normalized displayed prompt, fixed solution, actual level and complete field-owned bank with attribute presence; equivalent numeric spellings and seed/option order preserve IDs.
