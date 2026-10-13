# Four-stage extraction

## 1. Describe each source

Every tank has equal inflow and outflow, constant volume, homogeneous mixing, and positive dissolved initial mass and incoming concentration. All source masses are kilograms, volumes litres, and times minutes. Expression questions ask Q(t); numerical questions explicitly require two decimal places. No source asks for concentration rather than amount.

| Source db ID / MA ID | Volume V | Flow r (both directions) | Feed c | Initial Q0 | Requested time | Observed label |
|---|---:|---:|---:|---:|---:|---|
| 17592186229724 / q-339385 | 750 | 30 | .03 | 6 | function | absent |
| 17592186229725 / q-339392 | 900 | 30 | .02 | 10 | 6 | absent |
| 17592186377242 / q-336734 | 720 | 12 | .03 | 3 | 5 | moderate |
| 17592186377256 / q-336750 | 500 | 25 | .02 | 7 | function | easy |
| 17592186377263 / q-336753 | 400 | 20 | .03 | 3 | function | easy |
| 17592186377279 / q-339382 | 450 | 30 | .02 | 2 | function | easy |
| 17592186377286 / q-339390 | 350 | 25 | .02 | 8 | 4 | moderate |

The five worked solutions preserve complete original prose and stages: formal derivative; rate-in minus rate-out; units; concentration×flow with cancellations; Q/V; flow×Q/V with cancellations and two reductions; net rate; linear equation; homogeneous equation; complementary exponential; particular constant assumption; zero derivative substitution; solve alpha; general complementary-plus-particular family; initial condition with three rows; fixed final function. Moderate adds one displayed Q(T) substitution/approximation and rounding sentence. The coefficient 1 is omitted in source q-339390’s final exponential, but included as A=1 in its initial-condition row. The source tau=14 is retained unreduced in the Q(4) exponent, and no redundant extra simplification row is added.

## 2. Generalize only the shared assessment

With equal flows, V stays constant. The entering mass rate is rc, the exiting mass rate is rQ/V, hence Q′+(r/V)Q=rc. The complementary solution is A exp(−rt/V), the particular solution is cV, and the initial condition gives A=Q0−cV. The requested solution is cV+(Q0−cV)exp(−rt/V). Moderate additionally substitutes the requested time and rounds only the final mass.

## 3. Account for every component and complete source bank

`masks.json` records every original value, source answer UUID, complete answer mask, coefficient values and correct index (only where present). `source-cases.json` routes each practice through the normal public API. The tables below account for the complete banks in original capture order, not a pool of independently selected choices. All values reproduce exactly at unit scaling. Opaque interpretations are retained explicitly and are never promoted to default learner generation.

- q-339385: `22.5−16.5e^(−t/25)` [derived correct, designation absent]; `22.5−16.5e^(−t/20)` [alternate decay time 20, original operational derivation unknown]; `22.5−16.5e^(t/25)` [reverse decay sign]; `6−22.5e^(−t/25)` [initial mass as constant and equilibrium as negative amplitude]; `22.5+16.5e^(−t/25)` [reverse initial subtraction]. All are full `Q(t)=…` equations.
- q-339392: `11.83kg`, `11.02kg`, `12.11kg`, `11.45kg` [independently derived correct, designation absent], `10.76kg`. Four rounded scalar distractors underdetermine the error operations; no operation is asserted.
- q-336734: `4.17`, `3.96`, `4.49` [captured correct], `5.02`, `4.83`, each followed by the raw captured single-backslash kilogram suffix. Four opaque scalars; correct value independently verified from 21.6−18.6 exp(−5/60).
- q-336750: `12−5e^(t/20)`, `8−e^(−t/20)`, `10−3e^(−t/20)` [captured correct], `−9+16e^(−t/20)`, `9−2e^(−t/20)`. The alternatives mostly preserve Q(0)=7 but their particular constants are not determined by a defensible common error operation. Complete observed coefficients and signs remain explicit evidence.
- q-336753: `10−7e^(t/20)`, `12−9e^(−t/20)` [captured correct], `−1+4e^(t/20)`, `4−e^(−t/20)`, `−9+12e^(−t/20)`. All initial values are 3 but four different erroneous particular constants are opaque. No arbitrary equilibrium-offset polynomial fit is used.
- q-339382: `9−7e^(t/15)` [reverse decay]; `9−7e^(−t/20)` [alternate decay time unknown]; `2−9e^(−t/15)` [initial as particular and equilibrium as amplitude]; `9−7e^(−t/15)` [captured correct]; `9+7e^(−t/15)` [reverse initial subtraction].
- q-339390: `7.32`, `8.21`, `7.98`, `7.54`, `7.75` [captured correct], each with raw doubled-backslash kilogram suffix. Four opaque scalars; correct verified from 7+exp(−4/14).

## 4. Extract masks, calculations and constraints

All source prompt masks retain their punctuation, inline-math style, unit spelling, container, substance and field layout. All five present solutions retain full fixed prose and mathematical sequence. Slots are complete numeric components with dimensions: V, r, c, initial amount, incoming mass rate rc, equilibrium cV, integration constant, coefficient magnitude/optional unit coefficient, requested time, and rounded amount. Fixed zero derivatives, degree zero, initial time zero, one-over-tau numerators, and step numbers are not replaced. The flow rate 20 and decay time 20 in q-336753 are separate roles even though their original numbers coincide. Decimal masks were extracted with exact Decimal arithmetic, avoiding 21.6 versus binary 21.599999999… mismatches.

Raw profiles are parameterized by dimensional similarity: V→fV, r→fr, c→mc/f, Q0→mQ0. Therefore tau stays fixed and every mass coefficient scales by m. This is a real scaling symmetry of the source IVP, not a literal-answer branch or inferred distractor algorithm. Opaque wrong scalar values are scaled and rounded to two decimals; the mathematically correct scalar is recalculated from the unrounded model. Original unit-scale strings remain exact. Every raw profile has `evidence_only=true` and `eligible_for_learning=false`, including unchanged originals.

Normal authored banks are computed from one complete five-model profile, with E=cV, A=Q0−E, k=r/V: `(E,A,k)` correct; `(E/2,Q0−E/2,2k)` add equal inflow and outflow as removal rates then solve that erroneous IVP; `(2E,Q0−2E,k/2)` double the mixed-volume denominator then solve that erroneous IVP; `(rc,Q0−rc,k)` use forcing rc as the particular constant without dividing by k; `(E,−A,k)` reverse initial subtraction. The same full expressions are evaluated at T for numeric fields. These are actual operations on the displayed method, without arbitrary numeric perturbations. The whole bank is rejected on symbolic equivalence, rounded collisions, zero complementary coefficients, nonpositive requested quantities, or differing numeric digit lengths. Every numeric option has exactly two decimal places and the same unit suffix. Choice order is seeded and shuffled; content identity uses the sorted complete bank, prompt, fixed solution, actual difficulty and version. Mathematical identity uses normalized E, k, Q0 and requested time/demand, excluding context, source aliases, bank and option order.

Normal solution masks keep the source’s complementary/particular derivation, cancellation rows, formal operators, and initial-value stages. Slot changes affect mathematical rows and prose rate/time statements. For positive A, the moderate mask preserves coefficient omission at magnitude 1. Final function and finite-time substitution components are rendered independently to cover their different source spellings.

## Raw anomalies and normal treatment

Two originals omit difficulty, solution and correct reference; the authoritative original lesson capture does not supply them either. Raw replay preserves attribute absence. Inference identifies their unique correct mathematical choice without counting a matched designation. Normal records use explicitly authored supported fields, label and full worked solution.

Decoded source strings contain no adjacent backslash bytes. The kilogram suffixes use single LaTeX commands; JSON serialization escaping is not an anomaly. Raw strings are preserved in ineligible evidence, and normal amount choices use the same valid command form. No numerical source answer or worked-solution mathematical error was found. Opaque distractor interpretation limits and physically implausible source functions are reasons not to use raw banks for practice, not grounds to discard them.

There are no graphical components; step 5 and step 7 require no renderer. All work stops before database preparation.

Normal source-context adaptation also inflects “supplements enter/leave/exit” to the chosen substance with enters/leaves/exits; raw source prose remains exact.
