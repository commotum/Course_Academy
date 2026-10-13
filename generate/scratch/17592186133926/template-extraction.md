# Template extraction

## 1. Specific source descriptions

`classification.md` describes all eight individual prompts, intervals, number forms, force components, and observed difficulty attributes. `extraction.json` preserves every complete original answer, answer UUID, correct-presence fact, all prompt math spans, and every ordered worked-solution RHS and LHS independently. This is the component-level extraction, not an answer lookup table. Five source banks contain π multiples mixed with rational/integer options; two contain zero as the correct value; the unrated polynomial bank contains −1/60, −1/6, −1/100, 10, 100. All are exact-answer radios; there are no supplied-fragment blanks or plots.

The source solutions share their opening definition, “Along the curve”, “So”, derivative, “Therefore”, and final-integration prose. Their arithmetic stages differ: some constant primitives factor out their coefficient, q-162220 introduces cos(2t) and omits an explicit endpoint row, and q-162235 has an additional force-component simplification. Raw masks preserve these differences and their original row counts rather than replacing every source with a generic solution.

## 2. Shared pattern and purpose

Calculate Γ=∫ F(r(t))·r′(t)dt over one complete specified closed traversal. Substitute each coordinate into the force, independently differentiate each coordinate, take the three component products (including zero contributions), simplify by a familiar trig identity or polynomial distribution, find a primitive, and evaluate the endpoints. These are direct circulation calculations at every difficulty. Field interpretation, parameter interval, sign, and closure are part of the task.

## 3. Components and complete banks

All eight banks are fully mapped in `extraction.json`: the evidence recipe for each scalar is `force_scale * source_scalar`. At force_scale=1 every original value is reproduced byte-for-byte. The original correct designation is preserved for seven banks and is absent for q-162238. At other permitted nonzero integer scales the prompt force and all force-dependent solution expressions scale by the same factor. The opaque options scale as complete exact scalar expressions. Their historical error intentions are **unresolved**; fitting these scalar patterns does not establish recovered error operations. Every raw profile, including mathematically sound source banks, is explicitly evidence-only and ineligible for normal learner generation.

The source arithmetic component masks are independent: force definition and each substituted force RHS; each formal coordinate derivative and each evaluated derivative; first vector dot product; each distributed/reduced scalar product; formal definite integral; every numerical integrand; primitive; endpoint arithmetic when present; final equation. General symbolic F(r(t)) references are left symbolic because F already incorporates the selected force scale. Derivative/coordinate masks do not receive the force scale. Thus changed-force replay does not double-scale a symbolic integral. Ordinary prose and all nonforce math stay fixed.

Normal authored profiles are complete, chosen before parameters, and never assembled from a pool. Their recipes are:

| Family | Complete five-value method bank |
| --- | --- |
| xy_rotation, xy_rotation_z, yz_rotation | correct Γ; reverse orientation −Γ; omit one rotating component Γ/2; reverse one rotating derivative sign so the rotating sum cancels, 0; traverse the interval twice, 2Γ |
| xy_symmetric | correct 0; change the difference of square terms to a sum, 2πab; reverse both signs after that mistake, −2πab; omit the negative component, πab; omit the positive component, −πab |
| polynomial_sine | correct 0; add the two x primitive endpoints instead of subtracting, −2a²; reverse the resulting sign, 2a²; evaluate the z primitive at both interior peaks and add, −b²; reverse that erroneous sign, b² |
| polynomial_loop | correct −a²b/60; reverse orientation +a²b/60; omit y from F, 0; omit the cubic term in y before substitution, −a²b/6; omit the constant −a in dx/dt, −a²b/10 |

Each wrong value arises from the displayed components or endpoint operations. Compound mistakes are labeled as such in author metadata only. No learner-facing distractor diagnosis is added. The normal validator derives these alternatives independently from the actual printed prompt. The entire bank is rejected on invalid/equivalent values or missing choices; there is no arbitrary perturbation or first-valid fallback.

## 4. Reusable masks, constraints, and calculations

The public generator contains eight raw masks under `raw:q-N` profiles and six authored normal family masks. The raw parameter is force_scale in {−4,−3,−2,−1,1,2,3,4}. Every original replays through `generate`, with `source-cases.json` giving the exact calls. Raw solution omissions and unrated difficulty omission remain visible; the normal hard rating is recorded separately.

Normal family parameters are positive integers a,b with gcd(a,b)=1. This removes common scaling aliases, while the remaining ratio changes the actual curve/component substitution. No phase/start point, coordinate names, option order, profile name, or common reparameterization is sampled or counted as a mathematical task. Fixed interval bounds give exactly one complete traversal, and all curves have equal limiting endpoints. Every force is a polynomial on all R³, hence its domain contains the full curve.

| Actual normal level | Bounds and fixed workload | Meaningful tasks |
| --- | --- | --- |
| easy | a,b=1..4 primitive; sign ±1; two rotating products with a square identity, optional observed z polynomial contribution | 22 for each of three families, 66 total |
| moderate | a,b=1..4 primitive; either symmetric trig cancellation plus double angle, or x+y substitution plus a sine-cosine product and two primitive terms | 11 for each of two families, 22 total |
| hard | a,b=1..6 primitive; x=a(t²−t), y=b(t³−t), F=(ay−bx)i; linear force terms cancel, retaining precisely three nonzero polynomial terms of degrees 2,3,4 | 23 |

The 1..4 axes extend the observed ellipse scale 2 while retaining small-integer component products. Hard axes 1..6 extend the actual polynomial source without introducing different functions, more terms, different primitive exponents, or a theorem. Its collected integrand is a²b(2t⁴−3t³+t²), so arithmetic still has the fixed denominators 5,4,3. All bounds apply to explicit calls and random sampling. All 111 finite tasks are enumerated and verified, rather than reporting only a small sampled threshold. Intermediate trigonometric or polynomial coefficients are derived from those bounded displayed axes; incidental unused coordinates are fixed.

The normal solution uses the original common prose but is explicitly authored. It prints the formal circulation definition, three coordinate substitutions, force definition/substitution, all three formal derivatives, all three evaluated derivatives, both vectors in the dot product, all three scalar products, expanded products, reduced integrand, formal integral, actual definite integrand, primitive, individually evaluated components at both endpoints, and final scalar. Negative coefficients and implicit numerical factors are grouped. Source-only compressed endpoint layouts remain confined to raw fidelity replay.

Raw exact fidelity, mathematical correctness, and native grading are separate metrics. Raw q-162230 and q-162235 fail their independently parsed intermediate stages as documented. The validator requires exactly those expected failures; unlisted failures abort validation. Native radios grade answer identities but do not establish their displayed mathematics. q-162238 is excluded from native raw checks because its correct ref is absent. The inferred normal hard record has a supported key and is checked through the real grader. No engine changes are needed.
