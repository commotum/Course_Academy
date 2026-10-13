# Classification at math basis 1356

Captured lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw source wrapper is copied unchanged in `source.json`.

| Source | Captured level | Family and response | Bank | Plot |
|---|---|---|---|---|
| q-122271 | hard | implicit parabola, x/y scalar; exact evaluated scalar radio | 5 rational values, opaque numerators | none |
| q-122579 | absent | square-root curve, xy scalar; exact evaluated scalar radio | 5 rational values, opaque | light |
| q-122574 | moderate | explicit parabola, x/y scalar; exact evaluated scalar radio | 5 radicals/factored radicals | light |
| q-122593 | moderate | reciprocal curve, xy^6 scalar; exact evaluated scalar radio | 5 rational/radical values | light |
| q-149727 | moderate | line, 1/(y-x) scalar; exact evaluated scalar radio | 5 logarithm/radical values | light |
| q-149745 | hard | exponential curve, x^6 exponential scalar; exact evaluated scalar radio | 5 radical endpoint differences | none |

Each source is a distinct Markdown/value template with one observed complete bank. There are three observed moderate and two observed hard templates; no observed easy questions. The unrated question has a radio field with all five choices, but no correct reference and no worked solution. Raw replay omits all three missing attributes and preserves its malformed `\int_(C)4xyds` notation. The exact integral is 149/15, independently computed; that does not create a matched original designation.

The lesson route, followed through first-step/next references, is Introduction → constructing the integral (KP17592186179709) → evaluating it (this KP). Prerequisite topic links include line integrals in x and parametric parabolas; the canonical evaluation example uses x=ln y, y³e^-x, then a square-root u-substitution. This KP always requests the final scalar; setup-only sibling questions are excluded.

Authored easy uses a straight line x=2y+k, scalar cy, constant speed, and one power primitive. It reduces derivative/substitution algebra without introducing a different integral type. Authored moderate also includes the canonical log-curve family with the same t√(t²+1) substitution. Unrated square-root questions are assigned authored hard because substituting u=4t+k requires distributing two primitive components and evaluating both at both endpoints; this label is a design claim. Observed hard implicit parabolas require solving the curve for x and tracking fraction factors; exponentials require composing and reducing the exponents before substitution. Every family in a level has the same method and workload at its sampled parameters; there is no progression.

Normal implicit-parabola and square-root questions require positive lower y. Raw source q-122271 has x/y undefined at the origin; raw q-122579 has a singular parametrization derivative there. Their pulled-back integrands have convergent improper limits. Raw evidence preserves those endpoints and is ineligible for learner generation; metadata diagnoses the endpoint interpretation. No claim of ordinary defined/C1 substitution at zero is made.
