# Moderate variations

Approved authored extensions to the two captured moderate sources, q-102687 and q-15759; source classifications and exact choice banks remain unchanged as evidence. Curriculum placement is checked in [lesson-context.md](lesson-context.md).

## 1. Features and scope

All questions use one scaled sine or cosine for x and one scaled tangent or cotangent for y, sharing the same parameter t. Coefficients a and b are positive integers 1–4. The parameter interval is exactly one open quadrant; its endpoints are excluded. Answer fields remain radio with five mathematical equations and no option feedback or plots.

The two cotangent families, non-first-quadrant intervals, and new banks are authored variations, not recovered moderate examples. Families, coefficients, and quadrants are sampled without learner state or an instructional sequence. Shifts, double angles, signed scales, intervals spanning quadrants, and piecewise answers are excluded from moderate.

## 2. Shared skill and response

Isolate the scaled functions, recover the missing sine or cosine from the Pythagorean identity, choose its sign using the interval, substitute into a tangent or cotangent quotient, and simplify to y=f(x). Every family has this same operation sequence and comparable algebra; changing a reciprocal or root sign supplies variation at the same level.

## 3. Components and calculations

Let R=√(a²−x²), with s and c the signs of sine and cosine in the specified quadrant.

| Family | Correct answer | Recovered function sign |
|---|---|---|
| x=a sin t, y=b tan t | y=bcx/R | c |
| x=a cos t, y=b tan t | y=bsR/x | s |
| x=a sin t, y=b cot t | y=bcR/x | c |
| x=a cos t, y=b cot t | y=bsx/R | s |

The x-domain is (0,a) when the given function is positive and (−a,0) when negative. The y-sign is the sine sign times the cosine sign for either quotient. R is strictly positive on both domains. This excludes zero denominators and determines one branch.

Each authored bank contains exactly these four errors, computed from the correct answer C and the recovered function:

| Error | Expression |
|---|---|
| Wrong square-root branch | −C |
| Inverted trigonometric quotient | b²/C |
| Omitted square root | Replace the recovered signed √(1−x²/a²) with its signed radicand in the quotient before simplification. |
| Incorrect y-scale | C/b for b>1; 2C for b=1, where omitting b would leave the correct answer. |

These recipes describe the deliberate authored transformations. They do not assert how a learner reached an answer. All four options must be real on the whole x-domain, mathematically incorrect, and pairwise distinct as functions. Any failed member rejects the complete instance. Individual options may intersect at isolated x-values; comparison concerns their full equations on the domain.

The two observed profiles remain first-quadrant-only and reproduce all original choices, including the captured non-real sine/tangent options. They are selected explicitly for replay; normal moderate generation uses the authored bank for its chosen family. This is one normal sampling policy, not a unit/scaled or pedagogical-stage mode.

## 4. Markdown and solution template

Keep the original prompt, five whole-equation choices, opening sentence, Pythagorean derivation, sign-justification sentence, quotient-definition sentence, substitution block, and concluding equation. Change “tangent” to “cotangent” only for the cotangent families. Insert the appropriate minus sign and parameter interval wherever needed; use the same substitution/isolation block for nonunit coefficients. One worked solution serves every selected option; recipe labels stay in author metadata.

The interval appears in the learner's prompt. Full curve restrictions remain in author metadata and the author preview, following the existing scratch convention. Generation metadata distinguishes authored banks from observed banks and identifies both captured moderate questions as method references without inventing source question IDs for extensions.

## Validation and review

[Validation](moderate-variation-validation.json) checks every family and quadrant with the four coefficient-boundary pairs, using independent exact points on each curve, displayed answer values, branch and domain assertions, deterministic identity, rejection of unsupported parameters, and actual radio grading. The shared oracle also proves the selected root on the whole open quadrant using an exact rational parametrization. Original full-bank replay remains a separate requirement.

[Moderate review](moderate-review.md) displays all sixteen family/quadrant combinations at the same moderate difficulty. No database preparation or commit is included.
