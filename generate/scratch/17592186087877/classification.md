# Classification: Transforming First-Order Linear ODEs Using Integrating Factors

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; `source.json` retains the entire unmodified capture wrapper. Canonical example e-21741 is context, not a practice source. Seven practice questions, all one radio field `selection`, five complete equation choices each, no plots.

| Template | Source | Captured rating | Generator assignment | Supplied equation / integrating-factor shape |
|---|---|---|---|---|
| constant_cos | q-17540 | Unrated | Easy, authored assignment | Standard constant P, trigonometric Q, exponential factor |
| linear_exp | q-8546 | Unrated | Moderate, authored assignment | Standard P=2ax, Q=2bx exp(-cx²), exponential quadratic factor |
| scaled_constant_power | q-17533 | Easy | Easy | Divide by x, constant P, power Q |
| signed_constant_power | q-335278 | Easy | Easy | Signed rational constant P, power Q |
| scaled_reciprocal_cos | q-17539 | Moderate | Moderate | Divide by x², reciprocal P, cosine Q |
| reciprocal_exp | q-79818 | Moderate | Moderate | Standard reciprocal P, exponential Q |
| scaled_reciprocal_rhs | q-79819 | Moderate | Moderate | Divide by x, reciprocal P and Q |
| polynomial_transform | None | Missing hard | Hard, authored extension | Nonunit constant multiple of y′, signed monomial P, product Q |

Observed templates: two rated easy, three rated moderate, two unrated. Separate template names preserve normalization step presence, final RHS collection, and original logarithmic row counts. Complete raw source profiles remain separate even when factor families overlap; they are never merged into an option pool. The seven source profiles are identified by `(template, observed_raw)`.

The lesson route was reconstructed from `:activity/first-step` and each `:step/next`, not pull-array order: 88817 Introduction → 88818 Integrating Factor Method → 88819 this KP → 88820 Solving → 88821 Initial Value Problems → 88822 Derivation (IDs share prefix 175921860). The current KP stops at step 4, before integration of I Q. Prerequisites include constant-multiple integration, product rule, reciprocal integration and first-order linear standard form. The canonical next IVP uses P=3x²; the unrated transformation uses P=2x. These support power-rule integrating factors without any need to solve the ODE.

All templates have plot rating **none**. Question 1/2 section PNGs in the owning lesson are raster page captures of text/equations/widgets, not mathematical diagrams. The authoritative local lesson source `MA/DATA/Lessons/877/Source/877.json` and 877.md reproduce q17540/q8546 as five-choice radio widgets without keys or worked solutions. No missing correct designation is claimed as matched.

Hard questions all perform the same bounded workload: divide three terms by one small constant, integrate one signed monomial, exponentiate, multiply, and identify a product derivative. d=2 and d=3 are unordered variations of that workload. Bounds: d∈{2,3}, nonzero integer |a|≤3, nonzero |b|≤4, scale∈{2,3,4}. They add neither general solutions, initial conditions, variable substitutions, nor new integral techniques. This level assignment is a design claim, not observed Math Academy evidence.


## Current-source extension at basis 2009

`source-current.json` retains all eight live practice questions and the canonical example at math basis 2009, with the same lineage as the historical capture. The historical seven-question analysis above remains provenance. One additional rated moderate source, q-335274, adds `linear_sin`: standard-form y′+2ax y=sin(bx), with a quadratic exponential integrating factor. Its one `selection` radio field has five complete equation choices. Plot requirement is none. This is a separate value template and complete bank profile from `linear_exp`, because its forcing term and bank differ.

Eight observed templates now have eight complete source banks: two rated easy, four rated moderate, two unrated with contextual assignments. The ninth template is the bounded authored hard extension. The native inventory reports two easy and four moderate available questions at this basis; hard is unobserved and classified here as supported by the previously reviewed transformation-only workload. No source questions are rerated or edited. Missing source fields remain historical exceptions, not available generated questions.
