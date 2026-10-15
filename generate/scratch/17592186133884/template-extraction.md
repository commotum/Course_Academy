# Extraction and bounded generator

Source-specific descriptions, complete original values, field ownership, diagrams,
and full worked solutions are preserved in source-components.json at basis 2677.
The two implemented families retain different instructional backbones. All other
observed templates remain classified but are not claimed as generated families.

## Moderate: q-108467, triangle-polynomial

Original P=xy², Q=2x²y; vertices (0,0),(1,0),(1,2), counterclockwise.
One radio field `selection`, five math choices. Type I region x∈[0,1],
y∈[0,2x]. Source curl is 2xy. The full observed bank, ignoring order, is:

| Recipe | Integrand | Outer x limits | Inner y limits | Status |
|---|---|---|---|---|
| curl | 2a xy | 0,1 | 0,2x | correct |
| source pattern 2 | a x²y | 0,1 | 0,2x | incorrect |
| source pattern 3 | a x²y² | 0,2 | 0,2x | incorrect |
| source pattern 4 | a xy² | 0,1 | 0,2x | incorrect |
| source pattern 5 | 2a x | 0,2 | 0,x | incorrect |

Original a=1. Conservative same-method extension: P=a xy², Q=2a x²y,
integer a=1..12. Both partials and every option scale by a. Error psychology is
unresolved; the expressions, including altered limits, are retained as complete
observed patterns rather than invented cognitive explanations. All five recipes
must occur together. No choice mixing or new response type.

## Hard: q-109263, parabola-vector

Original F=⟨ln(2+x)-y²,x²+y²⟩. Curves y=x² and y=x+2 intersect at -1 and 2;
the logarithm is smooth because x≥-1 throughout the region. One radio field
`selection`, five math choices. Type I region x∈[-1,2], y∈[x²,x+2].
The source log typo is corrected everywhere in the new instance to ln(2+x).

| Recipe | Integrand | Outer x limits | Inner y limits | Status |
|---|---|---|---|---|
| curl | 2(x+a y) | -1,2 | x²,x+2 | correct |
| shifted inner strip | 2(x+a y) | -1,2 | x+2,x²+x+2 | incorrect |
| negative parabola | 2(x+a y) | 0,2 | -x²,x+2 | incorrect |
| changed sign and outer limit | 2(x-a y) | 0,2 | x²,x+2 | incorrect |
| changed x coefficient | 2a y-x | -1,2 | x²,x+2 | incorrect |

Original a=1 is retained for complete source replay only. Its second and third
choices both evaluate to 168/5, so it is not eligible for normal generation.
Conservative extension: P=ln(2+x)-a y², Q=x²+y², integer a=2..12. The y-derived
terms vary together throughout the complete bank. These are observed expression
patterns with a same-method coefficient generalization, not claims of known error
psychology. Every source option maps exactly once at a=1 with its designation.
Normal output requires all five represented integrals to have distinct values.

## Prompt, solution and asset contracts

Moderate: triangle description → differential line integral → repeated integral.
Hard: two curves → vector-field line integral → repeated integral. Orientation is
explicitly counterclockwise, matching the source plots. The output asks for a
complete repeated integral, not its evaluated scalar. The source field key and
five-choice response shape are fixed.

Both solutions preserve the ordered operative sentences and stages: Green
hypotheses/theorem; region diagram; (hard only) vector-to-differential rewrite;
concrete P,Q; partial derivatives; type I region; Green identity; concrete partial
subtraction; simplified curl; complete repeated integral. No evaluation stage is
added. The generator renders one concrete solution independent of selection.

Only slot a varies. It is positive integral to preserve nonzero derivative stages
and comparable workload. Moderate has a common positive field scale; hard varies
only the negative y² coefficient. Integer bounds are an explicitly narrow sampling
policy, not an asserted finite limit of Green's theorem. Fixed geometry retains
source assets and region-bound derivation; source repetition is not the reason
for calling it essential. There is no varying target or position slot.

Assets: q-108467 images/2e/2e63a57e50b60d7f0c6a3ce12d164716e2cba71c6bd4c6df10460a35beba4209.png
and q-109263 images/e3/e32b8e7d6ce80d7cedad928f9a2f7acc3c3d7f06add7909e856db27d154068d6.png.
Axes, labels, region, boundaries and arrows are fixed and visually verified; only
vector-field coefficients change. Byte hashes and availability are verified in
validation.json. Plot rating none because both unchanged assets are reusable.

Normal sampling covers every declared coefficient: 12 moderate and 11 hard
mathematical tasks, deduplicated by field and region rather than seed or UUID.
Validators parse displayed P,Q, partials, curl, all integral limits and all five
options independently, integrate each option, and exercise the actual learner
radio grader for acceptance and rejection. Replay compares complete integral
objects (limits, variables, integrands), with exact value checks on generated
banks. Fidelity and correctness are recorded separately in source-fidelity.json
and validation.json. See review.md alongside source-components.json.
