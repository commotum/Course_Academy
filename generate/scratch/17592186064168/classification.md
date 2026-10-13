# Classification — Finding the Antiderivative of a Radical Function

Capture: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; unmodified wrapper in `source.json`. Eight practice questions are counted; canonical e-367 is curriculum evidence, not another practice question.

| Observed difficulty | Sources | Layouts and templates | Plot rating |
|---|---|---|---|
| Easy | q-113674, q-71096 | Fieldless rational-power prompt; same complete three-row primitive and five-row derivative solution | none |
| Easy | q-143041 | One `blank`, supplied `+C`; compact root prompt; complete solution | none |
| Easy | q-167564 | One `blank`, supplied `+C`; whitespace-expanded root prompt; complete solution | none |
| Hard | q-113680 | Fieldless root prompt using “Calculate the integral”; four-row primitive and five-row derivative solution | none |
| Hard | q-113695 | Fieldless root prompt using “Find the antiderivative”; same solution method | none |
| Unrated | q-2023 | Five-choice `radio`, radical prompt; absent correct ref and worked solution | none |
| Unrated | q-29635 | Five-choice `radio`, rational-power prompt; absent correct ref and worked solution | none |

There are seven observed Markdown/value templates (the two direct-power sources share one), two complete radio profiles and two one-choice blank banks. There are **zero observed moderate labels**. The two unrated sources remain unrated in raw replay. Their completed design levels are explicitly authored: q-2023 moderate, q-29635 easy. Source omissions are not repaired inside raw evidence. All eight raw records have `evidence_only=true`, `eligible_for_learning=false`, `ineligible_for_learning=true`.

Four fieldless sources receive an authored primitive-fragment blank in normal completion. Two radios receive mathematically inferred correct refs and complete authored worked solutions. q-29635's bank is structurally parameterized but its original intent is opaque; both raw and completed opaque replay remain ineligible. Its normal default template uses a separately labeled authored bank.

# Curriculum and level bounds

`lesson.json` is traversed from `:activity/first-step` along `:step/next`, giving 65001 (introduction) → 65154 (power rule) → 65002 (monomial KP64167) → 65003 (this radical KP64168) → 65004 (reciprocal KP64169) → 65005 (recap), with the common db-id prefix 175921860. Collection order is ignored. The topic prerequisite is “The Power Rule for Differentiation”; the next topic includes “The Constant Multiple Rule for Indefinite Integrals.” The canonical example converts a square root to exponent 1/2, increases the exponent by one, divides by that new exponent, then checks by differentiating.

All levels assess this same single power-rule method. No sums, external coefficients, negative integrand powers, substitutions, definite integrals or logarithms are added. The sibling reciprocal method stays outside this generator.

- **Easy:** either an already supplied positive reduced exponent p/d, d=2–5, p=1–5, p/d≤5/2 (14 tasks, including both direct-power sources), or a root of x with p=1, d=2–5 (4 tasks). Source unit-root rewriting is one immediate conversion.
- **Moderate, authored:** one nonunit power under a root, d=2–4, 2≤p≤20, gcd(p,d)=1, p+d≤24, p/d≤5. There are **22 finite tasks**, comprising 2 proper and 20 improper fractions. Small root indices keep the root-to-power conversion familiar. The unrated cube root of x² anchors the representation; no observed moderate label is claimed. Every instance has one radical conversion, one numerator-plus-index addition, and one reciprocal coefficient, followed by the same derivative check.
- **Hard:** d=5–8 with the same bounds 2≤p≤20, gcd(p,d)=1, p+d≤24, p/d≤5. There are **41 finite tasks**, comprising 12 proper and 29 improper fractions. Larger familiar root indices retain the observed fifth-root representation demand; improper fractions are peer variants of the same rule. Every instance has exactly the same conversion, exponent-successor division and derivative stages as the observed hard sources. There is no within-level progression. Degree 9 was considered and rejected because the native grader supports root degrees only 2–8; no unsupported normal outputs remain.

The source q-71096 already uses the improper exponent 5/2 and its successor 7/2. The ordered lesson states the power rule for every n≠−1 and demonstrates the same successor/divisor calculation for n=3; it introduces no branch at n=1 or at improper fractions. This supports varying proper and improper positive fractions under a root without a new integration rule. The authored cap n≤5 is a modest magnitude extension, and the independent caps p≤20 and p+d≤24 keep the only addition and reciprocal reduction within small two-digit arithmetic. These caps are design workload policies, not recovered source bounds. They apply to both root levels; the distinction between those levels remains root index, rather than an extra operation or a progression in numerator size. Equivalent unreduced root ratios are excluded, so every added pair changes the assessed exponent, successor and final coefficient.

These finite bounds apply identically to sampling and explicit calls. Unreduced ratios, out-of-range powers and unit-power moderate/hard inputs fail. Opaque evidence profiles additionally require p=1,d=2–5. Normal questions explicitly use x>0, making even-root conversion, quotient powers, and formal differentiation branch-consistent. Raw source wording is unchanged; its mathematical evidence is checked on that positive interior branch.

Meaningful tasks distinguish whether a root-to-power conversion is requested, while excluding variable-bank, layout, option order and source/profile aliases. There are **18 easy, 22 moderate and 41 hard tasks** across the normal templates. Layout variants do not increase these counts. This is finite variation, not an unlimited numerical family.
