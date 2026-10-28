# Classification

Snapshot: math database, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the captured wrapper. Eight practice sources have one five-choice math radio field with key `selection`. Six carry a difficulty and correct reference; two carry neither a difficulty, correct reference, nor worked solution. No figures or plots occur: rating **none** for all templates.

| Source | Template | Observed level | Authored assignment if absent | Function / curve structure |
|---|---|---|---|---|
| q-36247 | mixed_product | unrated | hard | x²+3xyz; quadratic, shifted linear, signed linear coordinates |
| q-36253 | sine_difference | unrated | moderate | sin(x−y); square-root and linear coordinates |
| q-167499 | quotient | moderate | — | x/y; linear and square-root coordinates; positive perfect-square time |
| q-36227 | trig_powers | moderate | — | x³+y²; sine/cosine coordinates; familiar angle |
| q-94884 | square_difference | moderate | — | x²−y²; quadratic and shifted linear coordinates |
| q-94887 | triple_product | hard | — | xyz; linear, square-root, shifted linear coordinates |
| q-94888 | radical_square | hard | — | xz²+y³; linear, constant, square-root-of-quadratic coordinates |
| q-94891 | log_norm | hard | — | ln(x²+y²+z²); affine, constant, linear coordinates |

Observed: easy 0 templates; moderate 3; hard 3; unrated 2. Each template has one observed complete bank. Authored: easy adds one quadratic/affine template; moderate retains three observed templates and assigns the unrated sine template; hard retains three observed templates and assigns the unrated mixed-product template. Every template gets one separately labeled complete method-operation bank. There is no branch progression within a level.

The route was reconstructed using `activity/first-step` and `step/next`, rather than collection order: introduction → two-variable chain rule (24469) → three-variable chain rule (24470) → supplied-gradient evaluation (24593) → derivative-as-rate tutorial → this KP (24471) → vector-form intuition. Prerequisites are vector-valued differentiation, the multivariable chain rule, and the gradient vector. This KP supplies f and a curve and requests a scalar rate with respect to t at a specified t; it requires computing the gradient. Supplied-gradient-only questions, directional derivatives per unit arclength, and tangent-plane questions are excluded.

Easy is an authored design claim: two quadratic partial derivatives, two nonconstant affine curve derivatives, two dot contributions, and integer evaluation. Moderate preserves nonlinear/quotient/trigonometric component evaluation without increasing algebraic degree. Hard follows the observed three-variable product, cross-power/radical, or logarithmic structures, including explicit zero contributions for constant coordinates. The unrated mixed-product question involves three partial derivatives and contributions and fits hard; sine-of-difference with two coordinates fits moderate. Neither assignment is claimed as an observed label.

`authoritative-widgets.json` copies the owning MA lesson capture for q-36247/q-36253. It confirms five-choice multiple-choice widgets and the complete banks; it does not supply a solution or correct designation. Their correct values −17 and −3 cos 2 are independently derived. These two are included in all fidelity denominators except the absent-designation/absent-solution denominator.
