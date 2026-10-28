# Current source audit for inventory replenishment

The native inventory and scoped EDB pull at basis 2610 have lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The current KP contains twelve
practice questions, all with one five-choice mathematical radio field named
`selection`. Six have moderate difficulty and six have hard difficulty. No
source is rated easy. Every prompt, complete bank, correct reference, solution,
and the canonical example is retained in `reference/initial/before.edn`.

The historical basis-1356 generator remains the supported generation package:
its nine authored operation templates span easy, moderate, and hard, with the
authored easy policy explained in `classification.md`. Its eight complete
historical source banks and forty options passed exact replay again. Current
labels and completed solutions for the formerly unrated q-36247 and q-36253
are additional evidence; their function, curve, evaluation time, and complete
mathematical banks agree with the historical capture. q-36253 now spells cosine with `\operatorname{cos}` rather than `\cos`; complete-bank comparison uses exact mathematical equivalence rather than literal spelling. The current audit checks
all twelve current banks and every printed solution calculation independently.
The new source evidence does not require a new mathematical scope for the
already validated generator.

| Additional source | Level | Template backbone | Bank profile | Plots |
| --- | --- | --- | --- | --- |
| q-36234 / 17592186445680 | moderate | f=x² sin y; r=⟨ln t,2t⟩; t=π | 2 ln²π; 4 lnπ; −lnπ; 2 ln²(2π); −ln²π | none |
| q-94885 / 17592186479863 | moderate | f=arctan(x+y); r=⟨2t,3t⟩; t=1 | 7/13; 5/26; π/2−1; −2/13; π+2 | none |
| q-167500 / 17592186479876 | hard | f=cos(xy+z); r=⟨t²,1/t,t⟩; t=π/4 | 0; 1; −2; 2; −√2 | none |
| q-94889 / 17592186479889 | hard | f=x exp(y)+z; r=⟨4,ln t,exp(t)⟩; t=2 | 0; 4+exp(2); exp(2)−3; 2 exp(2)−1; 2 | none |

These add two moderate and two hard templates, each with one observed bank.
The source operations are, in order, gradient, substitution of all coordinates,
curve differentiation, dot product including zero terms, and evaluation. Domains
are t>0 for logarithms, t≠0 for the reciprocal, and the displayed evaluation
points satisfy them. Correct answers are respectively 2 ln²π, 5/26, −2, and
4+exp(2). Every displayed incorrect scalar is compared with the independent
answer; its original value is retained without inventing an error recipe.
These four additional families are classified and checked for existing
inventory, but excluded from the frozen generator's sampling scope. No source
replay or generation fidelity is claimed for them. The selected existing
generator is sufficient for the per-difficulty replenishment target; expanding
its family coverage is not needed to fill a supported band.

Current template counts: easy 0 observed (1 authored); moderate 6 observed
(4 supported by the existing generator); hard 6 observed (4 supported).
All plots are none: the content is mathematical text, with no image assets.

`reference/initial/source-audit.json` records twelve independent full-bank
checks and solution-row checks. q-94888 and q-94891 still contain the previously
documented false initial curve-derivative row. They are preserved and excluded
from validated inventory. Ten source questions pass mathematical validation
before learner exposure/reservation exclusions. Apparent doubled backslashes
in serialized CLI output are EDN escaping; decoded source strings are valid.
Dimension-label defects remain documented separately from false mathematics.

`inventory_validation.py` reads actual printed functions, curves, evaluation
times, complete banks and solution rows. It does not use generator metadata to
derive the correct scalar. Native grading then checks all owned choices of
every counted source and every proposed generated instance. Historical source
captures, current source questions, and learner history are never rewritten.
