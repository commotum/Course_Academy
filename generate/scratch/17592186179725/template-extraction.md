# Template extraction

## 1. Describe each original before generalizing

q123128 supplies endpoints(1,0,1)→(2,3,0), f=x+y+z, and asks for the equivalent definite integral. Its bank mixes linear integrands and square-root speed coefficients. It has no rating, correct ref, or solution.

q123431 supplies(-4,1,5)→(-2,3,3), f=(y+z)/x, easy. The parameterization has three nonzero increments; y(t)+z(t)=6; x(t)=2t−4 has no zero along the segment. Pullback stages retain the combined numerator, then constant numerator, then cancellation by2. Speed has an explicit sqrt(12) row before2sqrt(3). Its three integral setup rows end in6sqrt(3)∫₀¹1/(t−2)dt. No learner evaluation is required.

q123387 supplies(3,−2,3)→(5,−1,7), sqrt(2x+y−z), easy. All coordinates change; the combined substituted radicand simplifies to t+1. Two pullback rows and three integral rows end in sqrt(21)∫₀¹sqrt(t+1)dt. No learner evaluation is required.

q76569 supplies(1,2,0)→(2,1,3), xy², moderate. The actual factors(1+t)(2−t)² are displayed before the collected cubic t³−3t²+4. The six integral rows preserve setup, speed multiplication, factored speed, primitive bracket, signed endpoint components, final13sqrt(11)/4. z affects full speed despite being absent from f. Normal versions add two labeled explanatory masks for the expanded square and distribution; these do not replace the observed product or collected row.

q123434 supplies(2,−2,4)→(4,−1,5), x exp(yz), hard. Simultaneous substitution must replace the implicit product yz. The product exponent(t−2)(t+4) is expanded to t²+2t−8; x(t)=2t+2 equals its derivative. Setup is three rows; u substitution is five rows: transformed bounds−8..−5, exp primitive, individual exponentials at both endpoints, reciprocal exponential difference, common denominator. A generic exponential family that loses derivative matching is outside the profile.

q76577 supplies(−1,2,1)→(1,2,5), cos(π(x+z)/4), hard. y is constant but its derivative0 is shown in the 3D norm; sqrt(20) is retained before2sqrt(5). Pullback first substitutes x+z as two complete coordinate expressions, then simplifies angle3πt/2. u substitution retains transformed bounds, sine primitive, both trigonometric endpoint arguments, each familiar value, final scalar. This is a single real trigonometric branch.

q76200 supplies(1,0,1)→(2,2,3), sin(πy/4), with all coordinates changing and speed3. The bank's correct scalar6/π is independently inferred. No observed solution/rating/key exists; authored hard completion uses the same bounded familiar-angle backbone as cosine, retaining the sine primitive−cos and both endpoint terms.

## 2. Generalized stable backbone

Each instance is a scalar arc-length integral on one nonzero straight segment in3D. Let a,b be integer endpoint triples and d=b−a. The fixed parameterization is r(t)=a+t(b−a),0≤t≤1; x=x₀+dₓt, y=y₀+dᵧt, z=z₀+d_z t. The formal coordinate derivative row precedes the actual differentiated-coordinate row and vector derivative. The formal three-square norm precedes its numerical squares and simplified speed sqrt(dₓ²+dᵧ²+d_z²). The original function is pulled back simultaneously, including implicit products. Three setup rows express ∫C f ds=∫₀¹ f(r(t))||r′||dt, actual substituted integrand times speed, and speed factored outside. Easy ends here; moderate/hard continue through their fixed method. One worked solution per instance is independent of selected response. All field shapes remain five-option radio.

## 3. Components and complete bank maps

Write s=sqrt(N), N=dₓ²+dᵧ²+d_z², h=f(r(t)), I=∫₀¹h dt, J=sI. `fidelity.json` records every original full choice value, the generated full value, and its one-to-one mathematical match. Recipes below are entire banks, selected before parameters. Historical structural mappings reproduce every option, but intent is unresolved; scalar data cannot establish a misconception from the numeric match alone. No learner feedback or distractor diagnosis is invented.

| Public historical profile | Five recipe values in original bank order (designated key bold) |
|---|---|
| source-q-123128 | **s∫(A+Bt)**; sqrt(dₓ²+(dᵧ+d_z)²)∫(x₀−(dᵧ+d_z)t); same speed∫(x₀−dₓt); sqrt(N+2|dₓ|)∫(x₀+(B−dₓ)t); s∫(x₀+Bt), with A=sum(a), B=sum(d) |
| source-q-123431 | sq∫1/(t²−c); s∫1/(dₓt−1); s∫t/(t+c); **sq∫1/(t+c)**; sq∫(dₓt+y₀)/(t+c+1), c=x₀/dₓ, q=(y₀+z₀)/dₓ |
| source-q-123387 | s∫sqrt(2Bt+A); s∫sqrt(B²t²+2Bt+A); sqrt(N−1)∫t sqrt(Bt−A); sqrt(N−1)∫sqrt((B+4)t−3A); **s∫sqrt(Bt+A)**, A=2x₀+y₀−z₀, B=2dₓ+dᵧ−d_z |
| source-q-76569 | 4J; **J**; sqrt(N+2)/4; s/4; I |
| source-q-123434 | s/sqrt(2)(exp(Δ)+2)/exp(−u₀); s(exp(Δ−1)−1)/exp(Δ); **J**; J/s; (exp(Δ)+1)/exp(−u₁), u=y(t)z(t), Δ=u₁−u₀ |
| source-q-76577 | **J**; J/2; −2sqrt(N−8)/((B−1)π); s/(π/2); −J/4, B=dₓ+d_z |
| source-q-76200 | 4α; **J**; α; 1/dᵧ; J/4, α=πdᵧ/4 |

All integrals above have bounds0..1; prefactors, bounds and integrands jointly define the answer. Historical q123128 and q76200 bold keys are authored inference, not observed correct designations. The source polynomial bank's fixed quarters and radical offset and exponential/cosine irregular scalars are structural public evidence recipes, never asserted to be inferred mistakes. Changed-parameter replay may still be ineligible as learning content and stays explicitly evidence-only.

Normal authored complete banks use the actual assessed method:

- Setup families: J; omit speed I; use squared norm NI; omit d_z² from norm; hold y at its initial value while substituting x,z. Every complete definite integral is compared by its evaluated value. The frozen-y operation keeps the function form and wrong coordinate substitution, rather than a random numerical shift.
- Polynomial: J; omit speed I; use squared norm NI; omit the square on y in the actual product; freeze x at x₀. Same actual linear factors and signed primitive components drive solutions.
- Exponential: J; omit speed I; add instead of subtract endpoint exponentials; omit lower endpoint; incorrectly use du=dₓx(t)dt instead of the actual du=x(t)dt. The last wrong scalar is J/dₓ and depends on the displayed derivative relation.
- Trigonometric: J; omit speed I; reverse endpoint subtraction; omit inner-derivative division; double the inner derivative in that division. Family-specific sine/cosine primitives determine all values. No pooled replacement recipes are used.

A bank collision or nonreal/divergent learner option rejects the whole instance, and explicit invalid inputs raise ValueError. Raw historical banks preserve documented invalid choices but reject duplicate displayed identities or equivalent options; they never become defaults.

## 4. Slots, guards, stage masks and dependencies

Only endpoint coordinates are numerical slots; functions, integration branches, field shape, segment count, parameter interval, method and level are fixed. Endpoint slots update prompt triples, prose vectors, all four parameterization rows, all coordinate substitutions, every derivative and squared speed component, pullback stages, bounds after substitution, primitive/endpoints, complete answer bank, identity and task fingerprint together. There are no function-name or incidental label aliases.

Global explicit and sampled inputs require two integer triples, each |coordinate|≤24, |increment|≤8, nonzero segment. Family bounds further enforce:

- Sum: all three increments nonzero, nonzero pulled slope, |sum(a)|≤12, |sum(d)|≤9.
- Quotient: x₀x₁>0 (denominator pole-free on entire path), all increments nonzero, dᵧ+d_z=0, y₀+z₀≠0, |x endpoints|≤8. The two numerator-cancellation stages remain.
- Radical: all increments nonzero, endpoint radicands between1 and8, distinct. A linear radicand reaches its extrema at endpoints, proving whole-path positivity. No new root branch/evaluation is taught.
- Polynomial: x and y endpoints in1..4, nonzero x and y increments, all three increments nonzero with magnitude≤3. The nonzero cubic leading coefficient dₓdᵧ² cannot disappear. z translations do not count as variety.
- Exponential: dₓ=2dᵧd_z and x₀=dᵧz₀+d_z y₀; |dᵧ|,|d_z| in1..2; x₀ in1..6 and x₁ in1..14; −24≤u₀<u₁≤−1 and2≤Δ≤9. This explicitly constrained endpoint recipe preserves x=u′ and the source's reciprocal/common-denominator exponent stages, with no integration-by-parts or generic new exponential branch.
- Trig: nonzero dₓ and d_z, all increments magnitude≤4, initial/final argument numerators within−8..8, nonzero numerator change magnitude≤6; sine requires dᵧ≠0. Endpoint angles are integer multiples ofπ/4, so exact familiar values require no inverse trigonometry. y may be constant in cosine, retaining its derivative0 in the speed formula.

Sampling bounds are narrower than the public explicit guards: sum/radical/trig starts−4..4 and increments−3..3; quotient x₀ in{−6,−5,−4,2,3,4}, dₓ,dᵧ in{−2,−1,1,2}, y₀−3..4,z₀1..6; polynomial z starts−3..3 with d_z±1..3; exponential y₀−4..−2,z₀2..7 and dᵧ,d_z1..2. All explicit calls use identical workload guards. Families and complete banks are chosen before parameters; failure resamples the full instance, never individual options.

Ordered source stage masks: parameterization4; derivative3; magnitude3 (quotient/cosine4); pullback2 (quotient3); easy setup3; polynomial integral6; exponential/cosine setup3 plus substitution5. Unrated originals preserve absent solution; normal authored completion uses the same masks. Polynomial normal pullback adds square-expansion and distribution masks between the observed first substituted product and collected cubic. Every primitive component is individually rendered at both endpoints, including zeros, before final collection. Source prose is preserved; notation is normalized to explicit grouped component coefficients, full three-component vectors, SymPy TeX spacing and grouped signed arithmetic. This is five normalized solution reproductions, not five byte-exact solution copies. No mathematical source correction is silently presented as fidelity.

Mathematical fingerprints use family/workload, full speed, and pulled scalar function, canonicalized across t↔1−t. Thus incidental coordinates, unused z translations, orientation, seed/order and banks are excluded. z increments still count through their squared speed contribution. Full content identity hashes version, actual difficulty, actual prompt/fixed solution and complete displayed values; seed/order/profile aliases do not alter content identities. Banks are excluded from mathematical fingerprints and included in content identity. Review and validation counts are sampled task counts, not a claim of an exhaustively enumerated continuous family.
