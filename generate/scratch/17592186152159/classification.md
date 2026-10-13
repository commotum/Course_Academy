# Classification

Capture: math database, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the full immutable wrapper and record. Owning topic 17592186048645 / MA 2635, “Line Integrals of Scalar Functions Over Paths Expressed as Functions of X.”

The lesson route follows `activity/first-step` 17592186153058, then `step/next` 17592186153060, then 17592186153059: Introduction → **Reducing…** → Computing a Line Integral… . Pull collection order lists the computing step earlier; it is not the lesson order. Introduction teaches x=t, r(t)=⟨t,y(t)⟩ and ds=√(1+y′(t)²)dt. The canonical example e-6310 uses y=x³/3 and scalar y²/x, and stops at a definite integral. Computing its value is the sibling KP's demand. The following topic uses graphs expressed as functions of y and is outside this generator. Key prerequisite: Line Integrals of Scalar Functions (topic 17592186050289 / MA 2107).

All nine practice questions are single-field five-choice radio questions (`selection`) with full definite integral options; no missing answer fields or duplicate legacy fields. Eight are labeled easy. q-76188 is unrated and lacks both a correct designation and solution; its easy assignment is authored, justified by its simpler quadratic graph and single y/x substitution. No moderate or hard practice examples exist. No practice/canonical example plot occurs. The introductory narrative plot illustrates the graph but is not included or needed in questions: plot rating **none**, steps 5/7 need no rendering.

| Template / profile | Source | Curve | Scalar | Source level | Solution shape |
|---|---|---|---|---|---|
| quadratic_ratio / observed | q-76188 | x²/2 | y/x | unrated | absent; authored supplied |
| exponential_cancel / observed | q-76189 | eˣ | 5ye⁻ˣ | easy | cancellation + three final integral rows |
| cubic_product / observed | q-148206 | x³ | xy | easy | product + two final integral rows |
| reciprocal_product / observed | q-148208 | 1/x | 2x³y | easy | rational norm normalization + cancellation |
| linear_exponential / observed | q-76414 | 5x+2 | yeˣ | easy | constant norm pulled outside |
| linear_difference / observed | q-148199 | 2−x/2 | x³−2y | easy | rational slope norm + signed substitution |
| exponential_cosine / observed | q-148205 | 2eˣ | y cos x | easy | unchanged trig input + three integral rows |
| quadratic_sine / observed | q-76415 | 2x² | y sin x | easy | unchanged trig input + three integral rows |
| log_exponential / observed | q-76416 | ln x | 2x²eʸ | easy | derivative 1/t and exp/log cancellation |

Nine Markdown/value templates, nine observed complete banks. There is no merging of their distinct solution structures. All raw choices are mapped in `bank-map.json`; `source-cases.json` includes every source UUID and exact replay parameters.

## Source anomalies and repairs

1. q-76188: no correct ref, difficulty or solution in capture. Original MA lesson JSON at `/home/jake/Developer/MA/DATA/Lessons/2635/Source/2635.json` confirms five-choice widget, with a different display order, but provides no correct designation. `authoritative-widget.json` preserves the relevant record. Independent derivation gives (1/2)∫₀²t√(1+t²)dt as the unique correct choice. This is an inferred designation, never a matched original designation. A shared-method solution is authored. Legacy `\int_(C)` is normalized to `\int_{C}` in generated replay; raw string remains in source.json. Count: 8/9 raw-exact prompts, 1 supported presentation repair.
2. q-76188: two *incorrect* choices have equal complete scalar values. ∫₀²√(1+t²)dt = ∫₀²t√(1+t⁴/4)dt by u=t²/2. The original bank violates distinct-option requirements even though its correct choice remains unique.
3. q-148199: √5/2 ∫₀²(t−4)dt and √5/2 ∫₀²(2t³+t−8)dt both equal −3√5. Again these are equal incorrect choices, not two correct choices.

All 45 original values and 8 present correct designations replay exactly. Both banks remain callable through `generate(..., profile='observed_evidence')`, labeled evidence-only, with their collisions recorded. `profile='observed'` rejects an ambiguous instance; default `authored_operations` supplies a complete separately authored bank and rejects any collision. Raw evidence is not silently removed, and radio ID grading does not establish mathematical option distinctness.

## Authored missing levels and variety bounds

Normal easy variants independently scale the source curve and scalar by positive integers 1..3, with x bounds in 0..6 (strict positive lower bound for logarithm/reciprocal, sine upper bound ≤3). These retain each family's differentiation and substitution workload. Observed replay profiles only vary bounds and endpoints: one source cannot identify how its wrong-expression constants should change when curve coefficients change.

Moderate peers: shifted quadratic y=cx²+k, scalar xy or y sin x; nonzero positive c,k in 1..3 and 1≤a<b≤3. These add an additive component within the same substitution, preserving source quadratic and trig rules. Hard peers: y=cx³+kx, scalar y²/x or xy² under the same bounds. Canonical squared-y quotient anchors the squared substitution; nonzero linear term adds one derivative component. These are design claims, not recovered level labels. No antiderivative, endpoint evaluation, reparameterization or new path branch is assessed. Both templates within each authored level have equal peer workload, not a progression. The sampler enumerates all integer bound pairs (1,2), (1,3), (2,3), yielding exactly 27 candidate substantive parameter objects per family, 54 per authored level. Validation enumerates these whole domains: all 27 tasks per family are admitted, with zero whole-bank rejections, so each authored level has 54 substantive tasks. Variety is finite. Easy sampling has 468 candidate curve/scalar/interval objects before whole-bank rejection (eight families with six bound pairs, sine with four, times nine independent scale pairs); it does not claim unlimited diversity. Source quotient curves touching x=0 use the source/canonical convention of the removable singularity in the pulled-back integrand; authored hard quotient tasks have strictly positive bounds.
