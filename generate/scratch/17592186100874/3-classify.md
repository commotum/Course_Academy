# Classification at basis 2275

Source: frozen `source.json`, database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Thirteen practice questions have MA IDs. There are no non-MA records; `independent-inventory.json` therefore has an empty `questions` array. Canonical e-455 is context, not a fourteenth practice question.

| Level | MA questions | Fields | Mathematical backbones | Plot rating |
|---|---:|---|---|---|
| unrated | 1 | radio | affine square-root q-49527 | none |
| easy | 5 | 2 radio, 3 blank | affine power q-49610/q-336783/q-336788; affine square-root q-49622/q-336603 | none |
| moderate | 1 | radio | affine base raised to 3/2 q-49613 | none |
| hard | 6 | 2 radio, 4 blank | polynomial inner substitution, matching derivative factor, integer power or square-root cube | none |

Each source ID is a replay specialization so original wording, field placement, bank profile and solution sequence remain available. The shared mathematical pattern is `c*x^(n-1)*(a*x^n+b)^r`, with `u=a*x^n+b` and multiplier `c/(a*n)`. Displayed square-root and square-root-of-cube forms stay visible. Distinct exponents, substitution degrees, negative derivative, and field contracts are retained; no difficulty progression is created.

The actual activity chain is read by `:activity/first-step` followed by `:step/next`: tutorial 17592186101673 → this KP 17592186101682 → rational-function KP 17592186101687. The tutorial changes variables, changes the two limits individually, then evaluates in u. It explicitly says substitution back to x is unnecessary. Canonical e-455 demonstrates decreasing transformed bounds. Rational/logarithmic primitives belong to the following KP. Downstream topic relations include improper, inverse-trigonometric, algebraic, exponential, trigonometric and logarithmic integration. None is introduced here.

q-49527 has neither difficulty nor correct designation nor worked solution. Raw replay preserves all three absences and remains evidence-only. Independent evaluation gives sqrt(3)-1/3, the fourth choice. The separate authored completion places it conservatively at easy and supplies the source-compatible four-stage solution; this is not evidence of an observed easy assignment.
