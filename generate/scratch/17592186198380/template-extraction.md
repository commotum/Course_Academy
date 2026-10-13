# Four-stage template extraction

Provenance: `source.json` is the untouched basis-1356 wrapper, including IDs, answer fields, original choices, correct designations and all source prose. `extraction.json` contains declarative calculation templates; `source-cases.json` supplies all ten normal-generator replay inputs. No source record is returned literally by a generator branch.

## 1. Describe each original before generalization

Every source evaluates `∬_S F·dS` on a polynomial parameterization over a closed rectangle. All displayed values are exact integers or rationals, with no answer fragment or equation-valued field. Source IDs, bounds, fixed polynomial expressions and full banks follow. The complete original prompt/solution are preserved in source.json; extraction.json retains their fixed wording, tangent/cross-product/substitution/dot-product calculation prefix, and final evaluation order. Geometry and field stay fixed inside a structural recipe while bounds vary, so all prefix calculations remain valid for every variant.

### q-160845

Question UUID `69fe42a1-24c6-5f53-90f3-883e2fa5e193`, database id 17592186198586, level hard.

- Surface: `['u-1', '2*v', '2-3*u-2*v']`.
- Field: `['3*x+y+z', 'y/2-2', '-3*x-z']`.
- Bounds: `{'u_min': -1, 'u_max': 1, 'v_min': 0, 'v_max': 3}`.
- Inner integration variable `u`; extracted scalar factor `1`; final sequence `separable_v`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$10$ | False | `10` | `(10) * area / (6)` | empirical area-density replay; underlying error unresolved |
| `$2$ | False | `2` | `(2) * area / (6)` | empirical area-density replay; underlying error unresolved |
| `$8$ | False | `8` | `(8) * area / (6)` | empirical area-density replay; underlying error unresolved |
| `$4$ | False | `4` | `(4) * area / (6)` | empirical area-density replay; underlying error unresolved |
| `$6$ | True | `6` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
### q-160886

Question UUID `e6b5a3a2-513f-5721-bf54-260cfc8a8f5a`, database id 17592186198592, level moderate.

- Surface: `['2*u-1', 'u*v', '3*v']`.
- Field: `['2*x', 'x*z/3-2*y', '2*z']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': -1, 'v_max': 2}`.
- Inner integration variable `u`; extracted scalar factor `1`; final sequence `terms`.
- Supplied normal: yes.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$48$ | False | `48` | `(48) * area / (3)` | empirical area-density replay; underlying error unresolved |
| `$18$ | True | `18` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$36$ | False | `36` | `(36) * area / (3)` | empirical area-density replay; underlying error unresolved |
| `$72$ | False | `72` | `(72) * area / (3)` | empirical area-density replay; underlying error unresolved |
| `$24$ | False | `24` | `(24) * area / (3)` | empirical area-density replay; underlying error unresolved |
### q-161260

Question UUID `24885575-8fa2-5424-9a08-3593cc23273c`, database id 17592186278448, level moderate.

- Surface: `['u-v', '2', 'v**2']`.
- Field: `['y+z', 'x+z', '1']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `u`; extracted scalar factor `1`; final sequence `terms`.
- Supplied normal: yes.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$-\frac{1}{3}$ | True | `-1/3` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$-1$ | False | `-1` | `(-1) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{5}{6}$ | False | `-5/6` | `(-5/6) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$2$ | False | `2` | `(2) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$4$ | False | `4` | `(4) * area / (1)` | empirical area-density replay; underlying error unresolved |
### q-161262

Question UUID `627dbfaa-1fc7-5620-9101-9c85744bbe99`, database id 17592186278449, level moderate.

- Surface: `['3*u*v**2', 'u-v', '2']`.
- Field: `['x**2', 'x+y', 'z']`.
- Bounds: `{'u_min': -2, 'u_max': 0, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `v`; extracted scalar factor `-6`; final sequence `terms`.
- Supplied normal: yes.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$11$ | False | `11` | `(11) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$\frac{9}{4}$ | False | `9/4` | `(9/4) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$5$ | False | `5` | `(5) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$\frac{5}{3}$ | False | `5/3` | `(5/3) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$8$ | True | `8` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
### q-161263

Question UUID `c5de597f-04b0-56f5-aa9e-d79ce26e7706`, database id 17592186278450, level hard.

- Surface: `['u**2', 'v', 'u*v']`.
- Field: `['3', 'z', 'y']`.
- Bounds: `{'u_min': -1, 'u_max': 1, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `u`; extracted scalar factor `1`; final sequence `none`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$4$ | False | `4` | `(4) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$-3$ | True | `-3` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$-\frac{1}{2}$ | False | `-1/2` | `(-1/2) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$\frac{5}{2}$ | False | `5/2` | `(5/2) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$-1$ | False | `-1` | `(-1) * area / (2)` | empirical area-density replay; underlying error unresolved |
### q-161273

Question UUID `75e371a5-e04a-5fb9-938c-f538e06e2f93`, database id 17592186278455, level hard.

- Surface: `['u-v', 'v-u', '-2*u*v']`.
- Field: `['x', '0', 'y']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': 0, 'v_max': 2}`.
- Inner integration variable `u`; extracted scalar factor `2`; final sequence `terms`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$2$ | False | `2` | `(2) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$-4$ | True | `-4` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$\frac{1}{3}$ | False | `1/3` | `(1/3) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{4}{3}$ | False | `-4/3` | `(-4/3) * area / (2)` | empirical area-density replay; underlying error unresolved |
| `$-1$ | False | `-1` | `(-1) * area / (2)` | empirical area-density replay; underlying error unresolved |
### q-161278

Question UUID `5f5f7b83-0f5c-511f-9e98-a4ae85732cc3`, database id 17592186278459, level hard.

- Surface: `['u+v', 'v-u', '-v']`.
- Field: `['-x-z', 'x-y', '-z']`.
- Bounds: `{'u_min': -1, 'u_max': 0, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `v`; extracted scalar factor `1`; final sequence `terms`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$3$ | False | `3` | `(3) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-4$ | False | `-4` | `(-4) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$\frac{5}{4}$ | False | `5/4` | `(5/4) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{3}{2}$ | False | `-3/2` | `(-3/2) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$\frac{1}{2}$ | True | `1/2` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
### q-161283

Question UUID `d4391484-a70c-5d5d-8147-34baf59f21fd`, database id 17592186278461, level hard.

- Surface: `['u*v**2', '-1', '1-2*u']`.
- Field: `['z', '2', '-3*x*y']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `v`; extracted scalar factor `-8`; final sequence `separable_uv`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$3$ | False | `3` | `(3) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-4$ | False | `-4` | `(-4) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-2$ | True | `-2` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$\frac{5}{4}$ | False | `5/4` | `(5/4) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{3}{2}$ | False | `-3/2` | `(-3/2) * area / (1)` | empirical area-density replay; underlying error unresolved |
### q-161258

Question UUID `4c963e37-fb2b-5cec-bc6e-5cbde0fb10aa`, database id 17592186421784, level moderate.

- Surface: `['3*u*v', 'u', '-v']`.
- Field: `['3*x', '-y**2', '2']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `u`; extracted scalar factor `1`; final sequence `terms`.
- Supplied normal: yes.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$3$ | False | `3` | `(3) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{23}{4}$ | True | `-23/4` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$\frac{17}{2}$ | False | `17/2` | `(17/2) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-5$ | False | `-5` | `(-5) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{22}{3}$ | False | `-22/3` | `(-22/3) * area / (1)` | empirical area-density replay; underlying error unresolved |
### q-162593

Question UUID `f3288098-3c26-556d-b6c9-f206da47adfb`, database id 17592186421785, level moderate.

- Surface: `['-v', '-u', 'u**2']`.
- Field: `['3*z', '-2*x', '-y']`.
- Bounds: `{'u_min': 0, 'u_max': 1, 'v_min': 0, 'v_max': 1}`.
- Inner integration variable `u`; extracted scalar factor `-1`; final sequence `none`.
- Supplied normal: no.

| Original option | Correct? | Exact value | Parameterized expression | Interpretation |
|---|---|---|---|---|
| `$-\frac{3}{2}$ | True | `-3/2` | `integral(F(r) dot (r_u cross r_v), rectangle)` | evaluated flux |
| `$\frac{1}{3}$ | False | `1/3` | `(1/3) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{1}{3}$ | False | `-1/3` | `(-1/3) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{1}{4}$ | False | `-1/4` | `(-1/4) * area / (1)` | empirical area-density replay; underlying error unresolved |
| `$-\frac{1}{8}$ | False | `-1/8` | `(-1/8) * area / (1)` | empirical area-density replay; underlying error unresolved |

## 2. Generalized mathematical pattern

Compose the vector field with the supplied parameterization, obtain the oriented area vector `r_u cross r_v` (either supplied or derived), form their dot product, and evaluate the resulting polynomial double integral on a rectangle. Response: one exact scalar in a single five-option radio field. The worked solution follows this fixed route independent of the selected answer. Hinted, full-derivative, factor-out, separated-product and direct-iterated source sequences remain distinct.

## 3. Component accounting and complete banks

Every original choice is mapped in the tables above and in extraction.json, including the correct designation and original answer UUID. No scalar numerical answer by itself identifies an author's wrong operation. For that reason observed banks are kept as **explicit empirical replay profiles**, one bank per original structural recipe. Their wrong expressions are constant areal densities times the new rectangle area. This is a transparent finite-data extrapolation, **not recovered distractor intent** and **not a default instructional bank**. It is not a polynomial numerical fit to arbitrary inputs, but its use outside the original rectangle is still an authored empirical extension with limited pedagogical evidence. Two such variants per profile are labeled in the review. Correct flux always comes from the actual composition/dot-product/integral and is never scaled from an answer lookup.

Normal generation selects one entire authored bank before sampling. It then computes the correct answer and all four required wrong values. The whole instance is rejected if any two values are equivalent, nonreal or nonscalar, or if a wrong value equals the correct one; no options are pooled or truncated.

| Authored complete bank | Four parameterized wrong operations |
|---|---|
| authored_primitive | reverse cross-product orientation; omit both monomial antiderivative divisors; use `(i+2)(j+2)` instead of `(i+1)(j+1)` in each monomial divisor; multiply the integrand by the squared norm of the area vector again |
| authored_weighted | reverse cross-product orientation; erroneously integrate `u*f`, `v*f`, and `u*v*f` as if these factors were part of the area measure |
| authored_rectangle | reverse cross-product orientation; replace the double integral by lower-corner, upper-corner and quarter-point rectangular evaluations |

Here `f=F(r)·(r_u cross r_v)` and `(i,j)` is the exponent pair of a term `c*u^i*v^j`. These recipe descriptions are author metadata. No distractor-specific diagnosis is inserted in learner content. Authored banks are explicitly labeled; they are not presented as recovered original authoring logic.

## 4. Reusable template and constraints

Fixed components: source field/surface polynomial structures, prompt paragraphs, hint presence, shared worked-solution sentences, tangent/cross-product/composition/dot-product calculations, and final evaluation sequence. Variable components: four rational rectangle bounds, dependent inner reduction, outer primitive, endpoint evaluation, scalar flux and all owned answer values/IDs. There are no optional plot components. Source spelling aliases are retained only when symbolic equivalence proves the calculated expression equals the original expression. Each placeholder is filled from the same exact SymPy parameter instance.

The generator uses rational exact bounds of magnitude at most six, rejects nonpositive rectangle area, and enforces the geometric sampling restrictions in classification.md. The normal is `r_u cross r_v`, as the lesson specifies; no new orientation branch is introduced. Changing seed or choice order with fixed mathematical parameters/template/bank leaves content identity unchanged. The parameter fingerprint excludes the bank; the content fingerprint includes the whole displayed bank, prompt and solution. Field-owned answer IDs are UUID5 strings and correct answers are lookup refs.

## Source geometric limitation

No incorrect scalar answer, wrong displayed algebra or designation was found among the ten originals. q-161262 has `r_u cross r_v=(0,0,-6uv-3v²)`, which vanishes along `v=0` and `2u+v=0`; the latter intersects the original rectangle. The parameterization is therefore not globally regular and can cover a planar patch with opposing orientations. We preserve the source's signed **parameterized-patch** integral convention and do not claim it specifies a globally regular one-to-one oriented surface. Its formal integral and bank designation 8 are independently correct. This geometric limitation is retained in validation findings; it is not silently excluded. Other observed edge degeneracies are retained under the usual measure-zero boundary convention. There is no observed answer-field anomaly or format repair.

## Parent variety extension

Normal sampling uses translated integer rectangles: u lower bound −3..2 and v lower bound −2..2, independently chosen widths1..4. This offers480 affine easy domains rather than54, with the same two linear antiderivatives and short exact arithmetic. Families already restricted to nonnegative parameters keep lower bounds0..2; q-161262 retains u_max=v_min=0 with widths1..4. Geometry, field, orientation, question demand and every source replay remain the same. These are authored sampling bounds, not new observed templates or a within-level progression.
