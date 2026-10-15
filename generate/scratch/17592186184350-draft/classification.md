# Classification, basis 2275

The exact refreshed source wrapper, topic wrapper and lesson wrapper are retained
as `source.json`, `topic.json` and `lesson.json`. There are eight MA-identified
practice records, four independently authored inventory records, and canonical
example e-14403. Canonical and independent inventory are not practice-difficulty
observations.

| Band | Observed structure | Original sources | Field | Plots |
|---|---|---|---|---|
| Easy | scaled quadratic exponent | q-31420 | selection, radio, five math choices | none |
| Easy | shifted quadratic exponent, two banks | q-31419, q-73802 | same | none |
| Easy | rational quadratic exponent | q-31426 | same | none |
| Easy | outer scalar and shifted quadratic | q-73665 | same | none |
| Easy | exact differential, no redundant extraction row | q-73801 | same | none |
| Moderate | rational cubic exponent | q-211989 | same | none |
| Unrated | direct cubic differential, missing solution/key | q-73800 | five choices; correct absent | none |
| Hard | no observed practice | none | authored source-shaped radio | none |

Thus the rated source pool has six mathematical/solution templates and seven
complete rated profiles, plus an incomplete seventh template/profile. Every
original option is accounted for in `source-components.json`, including all five
q-73800 options with unknown original designations. Full raw omissions are
preserved through the public API.

The four non-MA records are base-only copies of q-211989 at bases 2,3,5,6.
`independent-inventory.json` contains their full original records with exact
basis and lineage and the concrete relationship to that original family.

Lesson order follows `activity/first-step` and successive `step/next` references:
Introduction → Products Containing the Exponential Function → this KP → More
Complex Cases → Definite Integrals tutorial → Evaluating Definite Integrals.
The predecessor topic is Integrating Exponential Functions Using Linear
Substitution. The tutorial explicitly supplies the derivative rules for e^x
and a^x. Canonical e-14403 is x³·3^(1−x⁴), solved through a negative quartic
substitution and the −1/4 differential ratio. This is the hard authoring anchor;
logarithmic denominators depending on x, roots, definite bounds and integration
by parts belong elsewhere and are not introduced.

Normal easy retains the observed workloads and supported coefficient/shift
slots. The q-73800 normal completion receives an explicitly authored easy label
because its supplied 3x² is already the complete derivative of the exponent,
matching q-73801's direct-differential workload. Moderate keeps a positive cubic
exponent divided by 2,4,5,7,8, with coprime numerator derivative 3 and denominator;
the nonunit rational ratio cannot disappear through a hidden common factor.
Hard uses a negative quartic coefficient −1,−2,−3 and a nonzero integer shift
between −5 and 5. Every hard item has that same single substitution and signed
reciprocal-factor workload. It is a design claim anchored to the canonical
example, not a recovered hard band or a progression inside a difficulty.
