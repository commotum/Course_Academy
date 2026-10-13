# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw capture is preserved in `source.json`.

All nine practice questions use one radio field `selection` and **five whole definite-integral choices**. There are nine Markdown/value templates and nine complete observed banks. The two old unrated records have no correct designation or worked solution; their authoritative lesson widgets confirm the same five choices, but contain no answer key/solution either. Derived keys and new solutions are supported authorship, not recovered evidence.

| Observed rating | Template | Source db id | Integrand / disk |
|---|---|---|---|
| Unrated → authored moderate assignment | difference | 17592186129513 | x²−y²; full right disk, radius3 |
| Unrated → authored hard assignment | xsqrt | 17592186129628 | x√(x²+y²); upper half of right disk, radius1 |
| Moderate | linear | 17592186278369 | x; full upper disk, radius1 |
| Moderate | x2y | 17592186278370 | x²y; full right disk, radius2 |
| Hard | expdiff | 17592186278371 | exp(x²−y²); lower half right disk, radius4 |
| Hard | sqrt | 17592186351514 | √(x²+y²); right half upper disk, radius2 |
| Hard | xy2 | 17592186394504 | xy²; lower half left disk, radius1/2 |
| Hard | radial2 | 17592186394545 | x²+y²; left half upper disk, radius1/2 |
| Hard | log | 17592186394552 | ln(x²+y²+1); lower half right disk, radius1 |

Plot rating **moderate**: each available solution has three figures (region, radial bound, angular interval), all dependent on radius. No plot appears in practice prompts or choices. The canonical prompt's two SVGs are MathJax formulas, not figures. See `plot-spec.md` for decoded formulas and figure inspection.

# Curriculum and authored easy scope

Following `activity/first-step` and `step/next` gives: Introduction → Rewriting over origin-centered circles → Writing More Complex Regions in Polar Coordinates → this KP → Evaluating Repeated Integrals Expressed in Polar Coordinates → Evaluating a Double Integral by Converting To Polar Coordinates. This ordering is not Pull collection order.

Prerequisites include Polar Coordinate Transformations, Double Integrals Over Type I Regions, Properties of Double Integrals, and Integration Using the Double-Angle Formulas. The neighboring rewriting KP handles constant-radius disks centered at the origin; the present KP adds completing the polar circle substitution and a trigonometric radial upper bound. Integral evaluation belongs to other KPs and is not assessed here.

Missing easy: a constant integrand over a full off-center disk tangent to the origin. The learner still substitutes the circle, factors r(r−2a cosθ) or the corresponding signed sine form, chooses the nonnegative-r interval and includes the Jacobian. It removes polynomial/composite integrand manipulation and half-plane intersection. Four axis orientations and integer radii1–5 give20 meaningful easy tasks without a progression. Moderate/hard radii are integers/halves from1/2 through5 (10 values per observed template), retaining the observed algebraic workload. No general offset requiring a quadratic formula, arbitrary angular cut, rotated center, or integral evaluation is introduced.

# Response criterion

These are rewriting/setup questions. Eligibility means the bounds represent the actual D with r≥0 and the density equals the transformed integrand times r. The two moderate source banks contain multiple scalar-zero integrals. That numerical coincidence does not make a wrong region/Jacobian a valid answer to this requested setup. Normal `setup` presentation makes this criterion explicit; observed replay preserves the original prompt aside from presentation repairs. Scalar coincidence is separately recorded, never used to claim a mathematically unique scalar-evaluation bank.
