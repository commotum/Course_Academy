# Classification (math basis 1356)

The immutable capture contains **11 practice questions**, all labeled moderate,
with one `selection` radio field and **five text choices** each. The canonical
example `e-9978` is context, not part of any practice fidelity denominator.
`source.json` preserves the complete capture wrapper, database, basis, lineage,
and attribute-presence evidence. There are no missing fields or plot references.

All questions ask whether each of three *given* functions satisfies the ODE and
then require the **complete subset** of valid proposed functions. A correct
single function is insufficient if another proposed function also works. Each
bank is a set of five different subsets; the computed subset occurs exactly once.
The complete source banks are extracted in `template-extraction.md`.

| Observed component template / bank profile | Family | Correct subset | Source |
|---|---|---|---|
| source_q-141096 / q-141096 | exponential, one shifted candidate | I | q-141096 |
| source_q-79335 / q-79335 | affine y/x, monomial candidates | I | q-79335 |
| source_q-141091 / q-141091 | sine / cotangent, shift | I and III | q-141091 |
| source_q-141092 / q-141092 | cosine / tangent, scalar candidates | all three | q-141092 |
| source_q-141093 / q-141093 | logarithms / exponential denominator | II | q-141093 |
| source_q-141098 / q-141098 | positive power / y/x | none | q-141098 |
| source_q-141099 / q-141099 | reciprocal powers / y/x | II and III | q-141099 |
| source_q-141101 / q-141101 | power / y/x | I | q-141101 |
| source_q-141103 / q-141103 | logarithms / exponential denominator | none | q-141103 |
| source_q-79330 / q-79330 | exponential, unshifted | II | q-79330 |
| source_q-79333 / q-79333 | reciprocal / y/x | all three | q-79333 |

These are **11 extracted component masks and 11 complete bank profiles**, across
six mathematical families. Separate masks preserve differing ordered solution
row counts, optional intermediate substitutions and prose judgments; changed
numbers alone are not claimed as new source families. Plot requirement: **none**
for every template and difficulty. Steps 5 and 7 require no image work.

# Authored missing levels and curriculum boundary

The linked lesson route follows actual `first-step` and `next` edges:
Introduction → Identifying a Solution → this multiple-solution KP → Initial Value
Problems. The introduction explicitly reserves *solving* ODEs for future lessons.
Prerequisites captured in topic context are Introduction to Differential
Equations and chain rules with exponential and trigonometric functions. Sibling
initial-value matching is excluded from every generated question.

**Easy is authored**, anchored to the canonical y'=y example: three unit-slope
exponentials, nonzero signed amplitudes up to 3, slopes ±1, constant shifts of
magnitude at most 2, and y'=±y. It checks all three simple derivatives and global
identities. No arbitrary harder algebra is added. The fixed workload stays three
independent one-exponential checks, whether a candidate is valid or shifted.

**Moderate observed methods receive authored variety:** exponentials, powers,
sines and cosines. Signed exponential/power rates have magnitude 2–5; candidate
rates/powers have magnitude 1–6; trig slopes are 2–4. Amplitudes have magnitude
1–4 and shifts at most 2. Trig candidates share the displayed inner slope. Every
instance still requires three derivative/substitution tests and a complete subset.

**Hard is authored**, not a relabeling of observed moderate questions. It uses
three shifted logarithms in an exponential RHS (a=2–4, b=1/a, log coefficients
nonzero and magnitude at most 5, shifts ±1 or zero), or three two-term polynomial
candidates in an affine y/x RHS (powers 2–4; both polynomial coefficients nonzero,
constant shifts ±1 or zero). Each candidate requires substituting the complete
sum; log questions display the log-power identity before exponential reduction.
Affine questions retain both derivative contributions and the full substituted
polynomial. These are unordered same-method alternatives, without ODE solving,
initial conditions, products requiring a new differentiation branch or integrations.
All guards apply equally to random sampling and explicit API parameters.

Dependent scaling of an observed question is a fidelity stress test, not evidence
of meaningful variety. Common dependent scaling and candidate-order aliases are
removed from mathematical fingerprints; full displayed content and banks remain
in content identities. The validator reports actual sampled unique tasks, not an
unbounded claim. Authored defaults are sampled from complete candidate catalogs
within these bounds and reject the whole instance on equivalent functions.
