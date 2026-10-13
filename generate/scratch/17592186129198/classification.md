# Classification

Capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` retains the full provenance wrapper, raw EDB records, question/field/answer IDs, original values and correct objects. All ten captured practice questions are covered. Plot rating is **none** throughout; there are no prompt, answer or solution assets in this KP.

| Level | Source | Field | Mathematical / layout family | Observed complete bank |
|---|---|---|---|---|
| easy | q-38133 | radio, 5 choices | cosine-double-angle upper radial bound; full angular interval; half-angle evaluation | q-38133_observed |
| easy | q-83511 | radio, 5 choices | fixed positive radial bounds, cubic radial monomial, cosine-sine product | q-83511_observed |
| easy | q-83957 | radio, 5 choices | fixed positive radial bounds, linear radial monomial, cosine with familiar endpoints | q-83957_observed |
| easy | q-161048 | radio, 5 choices | fixed radial bounds including zero, fourth power, sine with full half-circle endpoints | q-161048_observed |
| moderate | q-38031 | radio, 5 choices | sine radial upper bound with cosine factor; sine cube primitive | q-38031_observed |
| moderate | q-161049 | radio, 5 choices | cosine radial upper bound with cosine factor; cosine cube identity then primitive | q-161049_observed |
| moderate | q-83958 | radio, 5 choices | offset-cosine radial lower bound; square expansion, cosine-square reduction | q-83958_observed |
| moderate | q-83514 | radio, 5 choices | cosecant radial lower bound; cosecant-square angular primitive | q-83514_observed |
| moderate | q-83966 | radio, 5 choices | constant lower/cosine upper bound and sine integrand; two primitive terms, signed endpoints | q-83966_observed |
| unrated → authored easy | q-38127 | radio, 5 choices | fixed radial bounds, squared radial monomial, sine with familiar endpoints | q-38127_observed |

Each source has a distinct worked-solution/layout template. The two constant-sine sources share a mathematical family but keep different original wording/stage structures in replay. Counting those source layouts gives 5 easy templates (one authored level assignment), 5 moderate templates and 10 observed banks. No hard practice label was captured. Two authored hard templates use sine/cosine double-angle upper bounds on a partial familiar-angle interval; both share the canonical example's method, with no progression between them.

## Curriculum and authored difficulty bounds

The owning topic is **Double Integrals in Plane Polar Coordinates**, db `17592186049084`, MA 2030. Following `activity/first-step` and `step/next` gives:

1. Introduction (17592186130085)
2. Rewriting over a circle/part-circle centered at origin (17592186130087)
3. Writing more complex regions (17592186130093)
4. Rewriting over a circle/part-circle not centered at origin (17592186130219)
5. **This KP** (17592186130086)
6. Evaluating by converting to polar coordinates (17592186130088)

The siblings own Cartesian conversion and deriving polar regions. Here the repeated integral, integrand, order and limits are already supplied. No generated question assesses those sibling operations, geometry interpretation, improper integrals, integration by parts or an additional substitution method.

The exact prerequisites are **Integration Using the Double-Angle Formulas** (1038) and **Integrating Trigonometric Functions Using Substitution** (478). The canonical example e-7346 is `int_0^(pi/8) int_0^(sin 2theta) r dr dtheta`: radial primitive, squared upper bound, sine-square half-angle identity, angular primitive, both endpoint substitutions, familiar-angle arithmetic, exact final answer `(pi-2)/32`.

Authored hard questions use that same radial power, double-angle argument 2theta, sine or cosine upper bound, and upper angle pi/12, pi/8 or pi/6. The sine endpoint term is nonzero, so the same identity/primitive must be retained through exact endpoint arithmetic instead of disappearing over the full interval in observed easy q-38133. The hard label is a design claim rather than a recovered source label. Every hard variant has the same operations; c and radial amplitude A are integers 1..4. No arbitrary higher frequency or algebraic branch is added. These guards also apply to explicit calls. There are 96 meaningful parameter triples per hard family, 192 before equivalence across families.

Easy defaults use a monomial radial power 1..4, coefficient 1..4, integer bounds 0<=a<b<=4 and familiar angular endpoints. Product angles stay in the first quadrant. Full cosine-square defaults use frequency 1..3 with the original full angular interval, so all endpoint sine values are familiar zeros. Moderate defaults preserve their original family, c,A in 1..4, source-comparable familiar angular intervals; cosecant upper A is 2..4 and angles stay away from poles. Complete-bank collisions reject the whole sampled candidate.

## Captured anomalies

q-38127 has no difficulty, correct designation or worked solution. Direct calculation is `(2^3-1^3)/3 * (cos(pi/3)-cos(pi/2)) = 7/3 * 1/2 = 7/6`. The supplied bank contains that value once. The generator authors that key, an easy rating and a source-style solution; those are excluded from observed designation/solution denominators. All five original choices and exact original prompt are retained.

q-38133 has upper radial limit 2cos(2theta) on -pi/2..pi/2, which is negative on portions of the interval. This is a supplied oriented repeated integral and is mathematically well defined. It evaluates to pi. There is no physical-region claim and no exclusion/repair of its bounds.
