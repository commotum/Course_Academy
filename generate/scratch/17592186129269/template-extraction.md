# Template extraction (four stages)

Provenance is the captured math wrapper at basis 1356. All source fields are complete; all original question/field/answer attributes and omission presence remain in `source.json`. Local generated UUIDs replace source IDs, while the field-owned shape and correct lookup refs follow the generator interface. There are no response fragments, blanks, plots, distractor feedback, or omitted worked solutions.

## 1. Describe the sources before generalizing

Every moderate prompt gives three explicit inverse-coordinate equations, using integer coefficients. q-161798 includes a quadratic term whose derivative drops out of the sparse determinant; q-161802 includes a product term that similarly drops out. They remain genuine displayed derivative tasks and cannot be reduced to their final constant answer alone. All hard prompts show the inverse map as ordered three-row columns. The hard bank uses reciprocals, a square-root/shear, exponentials, pairwise products, cyclic cubics, or a quotient. Branch hints are part of the prompt.

Each source retains the formal forward-map introduction, forward Jacobian determinant formula, reciprocal-method prose with two bullets, nine partials (zeros included), formal inverse matrix, numeric matrix, cofactor-minor expansion, individual arithmetic stages and final inverse determinant. Hard additionally includes component assignments and an ordered `u,v,w` rewriting block before the reciprocal. The arithmetic row counts and optional reciprocal reduction rows below are source-specific; none are merged.

### q-39300

- Observed difficulty: hard. Inverse components: `('1/x', 'sqrt(y) + z', 'y**2')`.
- Source component domains and hints: x != 0, y > 0; u != 0, w > 0.
- Derived inverse determinant in xyz: `$\frac{2 y}{x^{2}}$`; in uvw: `$2 u^{2} \sqrt{w}$`.
- Solution rows after partials: determinant 4; coordinate rewrite 3; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-\frac{{u}^{2}}{2\sqrt{w}}$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{\sqrt{w}{u}^{2}}{2}$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{{u}^{2}}{2\sqrt{w}}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{2{u}^{2}\sqrt{w}}$` | correct | `B_3(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$-\frac{1}{2{u}^{2}\sqrt{w}}$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-39669

- Observed difficulty: moderate. Inverse components: `('2*x + y', '-x + 3*y - 2*z', '3*y + 4*z')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$40$`; in uvw: `$40$`.
- Solution rows after partials: determinant 5; no coordinate rewrite; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$8$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$16$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{16}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{40}$` | correct | `B_3(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$40$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161798

- Observed difficulty: moderate. Inverse components: `('x + y', 'z', '4*y - 2*z**2')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$-4$`; in uvw: `$-4$`.
- Solution rows after partials: determinant 5; no coordinate rewrite; reciprocal 3. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-\frac{1}{2}$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-\frac{1}{4}$` | correct | `B_1(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$2$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{8}$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-8$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161800

- Observed difficulty: moderate. Inverse components: `('-y + z', 'x + z', '-3*x')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$3$`; in uvw: `$3$`.
- Solution rows after partials: determinant 5; no coordinate rewrite; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-2$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{3}$` | correct | `B_1(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$1$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-\frac{1}{6}$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$6$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161801

- Observed difficulty: moderate. Inverse components: `('y - 3*z', 'x + 2*z', '3*x - y')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$9$`; in uvw: `$9$`.
- Solution rows after partials: determinant 6; no coordinate rewrite; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$3$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-\frac{1}{6}$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$1$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-2$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{9}$` | correct | `B_4(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
### q-161802

- Observed difficulty: moderate. Inverse components: `('3*x + y*z', 'z', '-y')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$3$`; in uvw: `$3$`.
- Solution rows after partials: determinant 5; no coordinate rewrite; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-3$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$3$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-\frac{1}{3}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-1$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{3}$` | correct | `B_4(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
### q-161804

- Observed difficulty: hard. Inverse components: `('exp(x)', 'exp(x + y)', 'exp(x + y + z)')`.
- Source component domains and hints: x,y,z real; u,v,w > 0.
- Derived inverse determinant in xyz: `$e^{3 x} e^{2 y} e^{z}$`; in uvw: `$u v w$`.
- Solution rows after partials: determinant 5; coordinate rewrite 3; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$\frac{1}{u+v+w}$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `${e}^{u+v+w}$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `${e}^{uvw}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$u+v+w$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{uvw}$` | correct | `B_4(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
### q-161805

- Observed difficulty: hard. Inverse components: `('x', '-y + z', 'x*y')`.
- Source component domains and hints: x != 0; u != 0.
- Derived inverse determinant in xyz: `$- x$`; in uvw: `$- u$`.
- Solution rows after partials: determinant 5; coordinate rewrite 1; reciprocal 3. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-\frac{1}{u}$` | correct | `B_0(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$-\frac{v+w}{u}$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$u(w-v)$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$uv$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{{u}^{2}}$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161806

- Observed difficulty: hard. Inverse components: `('x*y', 'y*z', 'x*z')`.
- Source component domains and hints: x,y,z > 0; u,v,w > 0.
- Derived inverse determinant in xyz: `$2 x y z$`; in uvw: `$2 \sqrt{u v w}$`.
- Solution rows after partials: determinant 6; coordinate rewrite 4; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$\frac{2}{\sqrt{uvw}}$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{2\sqrt{uvw}}$` | correct | `B_1(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$\sqrt{uvw}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$4uvw$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{uvw}$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161807

- Observed difficulty: hard. Inverse components: `('y*z**2', 'x**2*z', 'x*y**2')`.
- Source component domains and hints: normal: x,y,z > 0; raw source: x,y,z != 0, fractional powers use real cube roots.
- Derived inverse determinant in xyz: `$9 x^{2} y^{2} z^{2}$`; in uvw: `$9 \left(u v w\right)^{\frac{2}{3}}$`.
- Solution rows after partials: determinant 6; coordinate rewrite 3; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$3(uvw)^{1/3}$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{9(uvw)^{2/3}}$` | correct | `B_1(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$3(uvw)^{3}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$(uvw)^{2/3}$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{9}{(uvw)^{2}}$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161808

- Observed difficulty: hard. Inverse components: `('z/y', 'y', 'x*z')`.
- Source component domains and hints: y,z != 0; u,v != 0.
- Derived inverse determinant in xyz: `$- \frac{z}{y}$`; in uvw: `$- u$`.
- Solution rows after partials: determinant 5; coordinate rewrite 1; reciprocal 3. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$-\frac{1}{u}$` | correct | `B_0(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$\frac{4}{vw}$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{v}{{u}^{2}}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{2u}{v-w}$` | wrong | `B_3(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$-\frac{w}{v}$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
### q-161797

- Observed difficulty: moderate. Inverse components: `('x', '2*y', '3*z')`.
- Source component domains and hints: x,y,z real; nonzero constant inverse determinant.
- Derived inverse determinant in xyz: `$6$`; in uvw: `$6$`.
- Solution rows after partials: determinant 5; no coordinate rewrite; reciprocal 2. All nine partials and every source sentence are replayed.
- Single field key `selection`, type `radio`, five complete scalar function expressions. Original bank below is exhaustive.

| Original option | Designation | Exact coordinate-transport recipe | Historical error intention |
|---|---|---|---|
| `$6$` | wrong | `B_0(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$3$` | wrong | `B_1(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{3}$` | wrong | `B_2(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |
| `$\frac{1}{6}$` | correct | `B_3(u/a,v/b,w/c)/(abc)` | verified inverse determinant reciprocal |
| `$12$` | wrong | `B_4(u/a,v/b,w/c)/(abc)` | unresolved; expression preserved, no inferred cognitive diagnosis |

## 2. Generalized mathematical pattern

Given an invertible local three-dimensional map in inverse coordinates, differentiate its three component functions with respect to x,y,z, compute that inverse map's determinant by its sparse cofactor structure, rewrite it in u,v,w when it is not constant, and take the reciprocal. The response is a whole scalar expression for the forward Jacobian, not the inverse determinant, not its absolute value, and not a set of critical points.

## 3. Component and complete-bank mapping

For a source inverse map `(f,g,h)` the parameterized map is `(a f,b g,c h)`. Its derivative matrix has rows scaled by a,b,c, so `Dxyz=abc*D0xyz`. Its determinant expressed in target coordinates is `Duvw=abc*D0uvw(u/a,v/b,w/c)`. Every observed option is transported by `B(u/a,v/b,w/c)/(abc)`. This is one coherent coordinate change applied to the whole original bank, with no interpolation, answer table, perturbation, option dropping or first-valid replacement. It reproduces every original at a=b=c=1 and defines changed-coordinate variants through the public API. Opaque distractor intention remains unresolved even though the exact mathematical expression transport is established. Both `observed` and `source-repaired` profiles are evidence-only and ineligible for normal learning.

The authored complete method bank derives from the actual displayed derivative matrix: correct reciprocal `C=1/Duvw`; omitting the reciprocal gives `Duvw`; reversing cofactor signs gives `-C`; removing the scale a from the actual first derivative row gives `aC`; applying that scale a twice gives `C/a`. Its complete eligibility guard requires a≥2 for source scales (and |a|≥2 for authored signed diagonals) and all five functions pairwise unequal. These are derivative operations on the printed inverse map, not unrelated doubling/halving of a final answer. The easy family replaces the omitted-row-scaling option with 1, obtained by omitting its only nonunit derivative factor; its duplicated coefficient still gives `C/a`. Signed easy/moderate integer coefficients are guarded by magnitude, not just upper bounds.

## 4. Reusable Markdown/value masks, bounds and validation

Complete-component masks preserve the source's function assignments, field shape, common prose and all ordered stages. The numeric matrix scales individual rows; each cofactor/arithmetic mask gets the determinant's full row-scale factor, with explicit row-scaling explanation for changed-coordinate variants. The final collected determinant and reciprocal reduce at their appropriate last stages. Coordinate rewriting replaces mathematical u,v,w tokens inside grouped powers and function arguments while protecting command names; it does not blindly replace short substrings in prose. Unit scales naturally preserve the original mask's spelling and whitespace; there is no branch returning a source question payload. Option shuffling is seeded; question identity includes actual difficulty, complete prompt, fixed solution and entire displayed bank and excludes shuffle order. Mathematical fingerprints exclude bank/profile aliases and retain the actual inverse components/domain.

Source scales are positive integers 1..4, product≤32. Moderate source variants additionally require every derivative coefficient magnitude≤12 and constant determinant magnitude≤120, preserving source integer arithmetic. Default moderate generation first chooses uniformly among the six observed source-shaped method families, then samples that complete family’s finite eligible parameters. Coupling, sparse zeros, vanishing cofactor contributions and the original per-family solution stages remain; there is no new mathematical branch. The originally observed moderate rating grounds each family; all within-family coordinate scales preserve its derivative/cofactor demand with the coefficient and determinant ceilings above. The authored `moderate_diagonal` family is an explicit option and cannot monopolize the default. Default-seed coverage and native checks appear in `validation.json` and the review.

Easy authored defaults have exactly one nonunit diagonal factor with 2≤|a|≤12. The explicit authored moderate diagonal option has exactly two nonunit diagonal factors with 2≤|a|,|b|≤8 and |ab|≤40. Hard consists only of the observed nonlinear structures and the additional coordinate rewrite, never integrations, critical sets or arbitrary new algebraic branches. Every guard also applies to explicit parameters. The exact finite catalogs are enumerated in `validation.json`; notation, bank aliases and shuffle seeds do not inflate counts. Output scaling affects actual differentiated rows and inverse substitutions even in the exponential family where those factors cancel in the final determinant.

Easy is authored from the observed moderate diagonal source's inverse-Jacobian method: its unit minor removes two nontrivial factor calculations. Moderate's two nonunit derivatives cannot be generated at easy, and hard requires nonlinear inverse-coordinate rewriting. The canonical `(x²,xy,yz)` map independently anchors differentiating inverse components then substituting into uvw before inversion. The inverse function theorem and determinant prerequisites justify the method; sibling critical-point and direct-forward-Jacobian skills are explicitly excluded.

### Source teaching/presentation findings

- q-39300 component prose names the second and third functions `y(x,y,z)`/`z(x,y,z)` rather than `v(x,y,z)`/`w(x,y,z)`. Raw profiles preserve those bytes; repaired and normal profiles correct the labels without changing mathematics or row count.
- q-161807's first cofactor minor has `2xy` instead of `2xz`. Because that entry multiplies zero, the displayed determinant values remain correct. Raw evidence preserves the incorrect matrix entry; repaired and normal profiles correct that complete minor. Structural minor checking catches this error even though scalar determinant checking cannot.
- q-161807 advertises nonzero coordinates. Its `(uvw)^(2/3)` is correct using real cube roots: setting t=xyz gives uvw=t³ and real-root(t³)²=t² for either sign. Principal complex-power interpretation is not asserted. The validator independently evaluates printed source answers and rewrite rows at all eight signed nonzero octants. Normal and repaired output state positive x,y,z, the branch used in symbolic radical normalization. `powdenest(force=True)` is only an equality helper under those recorded branch conventions, not the sign proof.
- q-161808 raw wrong options have extra denominators `v-w` and `w` that can vanish within the source's advertised domain. Those opaque historical functions remain evidence-only, while the normal method bank has exactly the correct determinant's nonzero-domain restrictions.

Exact original prompt/solution reproduction and complete bank/value/designation matches have denominators 12/12, 60/60 and 12/12. Raw component-label and cofactor-minor structural correctness are separate denominators (11/12 each); all raw final values are correct under the stated real-root convention. Repaired structural correctness is 12/12. No missing field/difficulty/correct attributes or TeX escape repairs were required. Decoded bytes were inspected; the two adjacent slashes found in source displays are ordinary aligned-row separators.

Independent QA reconstructs the actual printed inverse components, differentiates them, reads all nine displayed partials, verifies every numeric Jacobian/cofactor minor and all ordered arithmetic/rewrite/reciprocal rows, evaluates all displayed options, and reconstructs each normal wrong derivative operation. The native `grade_field` harness separately accepts the owned correct UUID and rejects all four wrong UUIDs for originals, repaired evidence and generated variants. Source correctness is never inferred from radio UUID selection. The final validator binds artifact hashes and dependency provenance.
