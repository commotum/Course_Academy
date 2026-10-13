# Template extraction

## Stage1: individual source descriptions

All sources show finite xyz-space constraints, supplied u/v/w coordinates and a change-of-variables setup request. Source exact number forms, TeX/Unicode spelling, all fields and complete prose are retained in source.json. Original component masks are in raw-templates.json. q-38941 uses positive square-root z, source rectangular u,v ranges1..2 and dependent original z≤uv. q-39054 uses familiar pi endpoints and a constant positive determinant2. q-161880 uses u=x+y,v=y-x,w=z, determinant2, and a polynomial-times-exponential integrand. q-39057 uses u=x²+y,v=2x+z,w=z, determinant-2, logarithm with positive argument, and originally inconsistent repeated limits. q-161879 uses u=x+3y,v=z-3y,w=z, determinant-3, two trigonometric argument substitutions. No source plots occur.

## Stage2: generalized family descriptions

Easy fragments substitute each integrand argument and multiply by the absolute reciprocal of the full3×3 determinant. Supplied integral bounds constrain the response to the missing integrand. The square-root family asks for the whole integral: derive the positive w branch, transform the dependent bound and integrand, and include its variable determinant. The canonical product family transforms xy² and yz and cancels a variable determinant with an explicit sign branch.

## Stage3: component and complete-bank mapping

For each raw bank below, every expression is an independently retained complete source component. Public replay applies the same common integral-amplitude factor to every expression and to the original integral/solution components. The factor equals1 at source parameters; altered amplitudes are evidence variants. This construction is a parameterized scaling operation, not an answer lookup. It does **not** recover original distractor intent. All historical banks are explicitly opaque/evidence-only. Bank order may shuffle; values and designation presence do not change.

### q-38941 — raw profile

- `\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}3 wdwdvdu` — no recovered error interpretation
- `\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}3 w 2dwdvdu` — no recovered error interpretation
- `\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}3 w 2dwdvdu` — no recovered error interpretation
- `\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}3 wdwdvdu` — no recovered error interpretation
- `\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u + v}3 wdwdvdu` — no recovered error interpretation
### q-39054 — raw profile

- `\sin u\cos v` — no recovered error interpretation
- `2\sin u\cos v` — no recovered error interpretation
- `\frac{1}{2}\sin u\cos v` — no recovered error interpretation
- `3\sin u\cos v` — no recovered error interpretation
- `\frac{1}{3}\sin u\cos v` — no recovered error interpretation
### q-161880 — raw profile

- `\frac{{e}^{u}}{2}` — no recovered error interpretation
- `u{e}^{v}` — source correct
- `\frac{v{e}^{u}}{2}` — no recovered error interpretation
- `\frac{{e}^{v}}{2}` — no recovered error interpretation
- `2u{e}^{v}` — no recovered error interpretation
### q-39057 — raw profile

- `\frac{1}{3}v\operatorname{ln}⁡u` — no recovered error interpretation
- `\frac{1}{2}v\operatorname{ln}⁡u` — source correct
- `u\operatorname{ln}⁡v` — no recovered error interpretation
- `2u\operatorname{ln}⁡v` — no recovered error interpretation
- `3v\operatorname{ln}⁡u` — no recovered error interpretation
### q-161879 — raw profile

- `\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v` — source correct
- `\frac{1}{2}{cos}^{2}⁡v\operatorname{cos}⁡v` — no recovered error interpretation
- `\frac{1}{2}{cos}^{2}⁡(u-v)\operatorname{cos}⁡v` — no recovered error interpretation
- `\frac{1}{3}{cos}^{2}⁡(u)\operatorname{cos}⁡v` — no recovered error interpretation
- `\frac{1}{4}{cos}^{2}⁡(uv)\operatorname{cos}⁡v-u` — no recovered error interpretation

Normal complete method banks (chosen before sampling; all5 members must pass):

- exp: correct c u exp(v)/(a+1); omit Jacobian; exchange u,v arguments; omit linear u; substitute u into the exponential. Uses u=x+a y,v=y-x and determinant a+1.
- sin: correct c sin(u)cos(v)/a; omit reciprocal determinant; multiply by forward determinant; exchange function arguments; use sin in the second factor.
- log: correct c v ln(u)/a; omit reciprocal determinant; multiply by forward determinant; replace the linear v with u; use the signed inverse determinant without its absolute value.
- cos2: correct c cos²(u+v)cos(v)/a; omit reciprocal determinant; multiply by forward determinant; change sum to difference; omit v from the squared-cosine argument.
- product: correct (c u v+d v w/a)/(a|v|); omit determinant; use forward determinant magnitude; omit v from xy² substitution; omit z=w/a scaling. Every term defining this workload is nonzero. Negative v intervals retain their negative reciprocal determinant until the absolute value is applied.
- sqrt: correct c w²/a with w upper bound sqrt(uv); omit variable Jacobian; omit square root in bound; use sum in place of product in bound; use constant planar Jacobian only. All5 complete integrals must have different exact values, not merely different formulas.

## Stage4: reusable masks, restrictions and solution sequence

`raw-templates.json` contains whole-component slots, complete original prompt and solution masks, exact original bank fragments and attribute presence. There is no literal source-question return branch. Original fixed prose and every mathematical stage replay exactly. General source amplitude multiplication slots do not alter coordinates or independently perturb wrong numbers. Raw height must equal the captured fixed value.

Normal templates use shared original instructional sentences and the same four named steps: transformation/change-of-variables formula; transformed domain; all9 formal partials and9 evaluated entries plus a complete cofactor expansion and every2×2 minor; forward determinant and transformed-coordinate determinant; reciprocal determinant/noncritical condition; integrand substitution, absolute determinant application, final repeated integral. Full cofactor expansion is an authored explanatory supplement to sources that show one nonzero minor. Final setup is never evaluated.

Normal easy a∈[2,5],c∈[1,4],height∈[2,5]. The nonunit determinant arithmetic remains familiar; functions/argument structures match observed demand. These yield16 substantive coefficient tasks per family,64 total before incidental rectangle-height presentations. Moderate a∈[2,4],c,d∈[1,4],sign(v)∈{-1,1},z-upper∈[1,3]; hard a∈[1,3],c∈[1,4],u/v-upper∈[2,4]. Nonzero components and distinct level-specific coordinate/bound operations are enforced for explicit calls. Parameters outside these guards fail; ambiguous complete banks fail rather than replacing individual choices. Missing-level definitions are authored claims anchored to the canonical product setup and observed unrated square-root setup. No neighbouring evaluation/volume demand is introduced.

Fingerprints exclude incidental easy rectangle height, but include coefficients that affect assessed substitution/Jacobian. Whole-integral response fingerprints retain bounds. Content identities include actual prompt, complete fixed solution, difficulty and complete displayed bank; seed, option order and unused metadata cannot change them.

## Source repairs and limitations

- q-38941: w=sqrt(z) means w≤sqrt(uv), not uv; absolute inverse determinant is w (for source a=1), so the integrand is3w². Source `3 w 2` decodes as literal multiplication tokens, not an exponent. None of its original five integrals is a correct setup. Original capture has no correct designation and no solution. Public raw evidence preserves this. Normal hard uses an independently authored correct bank.
- q-39054: absent correct designation/solution/difficulty are preserved in raw evidence. Independent determinant calculation gives sin(u)cos(v)/2. Normal easy supplies a mathematically justified designation, fixed worked solution and authored easy assignment. Source A A A A A A placeholder becomes a visible missing-integrand box in normal presentation.
- q-161880: Step1 has0≤u≤1 whereas prompt and final integral have1≤u≤2. Normal Step1 follows the prompt. Raw entire solution stays exact.
- q-39057: x∈[-1,1],z∈[1,4] implies w-2≤v≤w+2, not a rectangle -1≤v≤6. Retaining that region would require an integration-order/bound rearrangement outside the easy missing-fragment demand. Normal **premise repair** replaces the x constraint with the supplied v constraint (-1≤2x+z≤6 at a=2), keeping all supplied integral limits and the original assessed fragment. This changes the region, and is expressly not raw fidelity. The stray first transformed sin(u)cos(v) solution row is replaced by v ln(u). Original wrong choices involving ln(v) are also undefined on the stated region where v can be negative; normal banks use ln(u) only and derive their wrong values from linear-coordinate or determinant operations.
- q-161879: transformed-domain tuple erroneously says(x,y,z); normal uses(u,v,w).

Exact source fidelity is separate from correctness:5/5 original banks,25/25 values,3/3 present designations and3/3 entire present solutions. The two missing designations are not credited as matches. Raw mathematical anomalies remain ineligible. Normal corrected examples and native grading are reported separately in validation.json; original anomalous statements are never silently presented as validated mathematics.
