# Classification — math basis 1356

## Current-source addendum — basis 2712

This section supersedes the earlier difficulty capabilities below. A fresh,
single-basis pull contains 12 practice questions: six easy and six moderate, all
one five-choice radio field named `selection`, with no plots. There are five easy
Markdown/value families (sin has two banks) and six moderate families, each with
its own bank. The full records and per-question decisions are retained in
`reference/replenishment/initial/kp.json` and `source-audit.json`.

Easy families: sin (q-39054, q-39058), exp (q-161880), log (q-39057), cos2
(q-161879), affine sum (q-161868). Moderate families: sqrt (q-38941), ratio/product
(q-161892), x/product (q-161871), difference/log (q-161889), triple-product/exp
(q-39062), difference/sinh (q-39056). All require no new plot assets.

The source now rates sqrt moderate. The generator uses that level and retains
canonical product moderate. No harder source-backed backbone has been validated;
hard is unsupported. Current source keys and solutions retain mathematical
errors; source preservation does not certify their correctness. Only q-39054,
q-39058, q-161868 and q-39056 pass the conservative usable-inventory audit.
Others remain unchanged and are excluded, with exact reasons in the audit.

The existing five historical replay profiles remain evidence-only. Newly seen
source banks are classified and preserved, without an exhaustive generator
fidelity claim. Replenishment uses the previously validated method banks only.

## Historical classification

Provenance: `source.json` retains the full capture wrapper, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Five practice questions, all one radio field named `selection`, five mathematical choices each. Three easy-labelled sources; two unrated sources. There are five prompt/solution families and five complete observed banks. None require plots. The canonical two rasters were visually inspected: they are coordinate-vector mapping formula images, with no region geometry or numerical parameters. Generated formulas use TeX.

| Source | Source difficulty | Family | Source solution | Correct designation |
|---|---|---|---|---|
| q-38941 | absent | square-root third coordinate; whole repeated integral | absent | absent |
| q-39054 | absent | sine-cosine fragment; constant determinant | absent | absent |
| q-161880 | easy | exponential fragment; linear coordinates | full four steps | present |
| q-39057 | easy | logarithmic fragment; nonlinear first coordinate | full four steps | present |
| q-161879 | easy | cosine-squared fragment; linear coordinates | full four steps | present |

Raw profiles are public through `generate(level, template=source_id, parameters={scale,height}, profile='raw')`; they are evidence-only and not eligible for learning. Absent difficulty, solution and correct attributes remain absent. `source-cases.json` records a working difficulty solely to call the API for unrated records: easy for q-39054, hard for q-38941. This does not add original difficulty attributes.

Normal easy sampling chooses exp/log/cos2/sin equally before parameters. Normal defaults use separately authored method banks. Moderate is authored from the canonical setup u=xy,v=y,w=2z: variable Jacobian, two-term integrand, known positive or negative y branch, and full repeated-integral response. Hard is an authored difficulty label for the observed unrated square-root family: a dependent upper bound and variable Jacobian require one more coordinate/bound substitution than moderate. All questions stop at setup. They do not evaluate the triple integral or ask for volume.

The lesson route is Introduction → this setup KP → Evaluating a Triple Integral Using a Change of Variables → Computing the Volume of a Region Using a Change of Variables, reconstructed from activity/first-step and step/next. Prerequisites are rectangular triple integrals, three-dimensional Jacobians and double-integral change of variables. Constant easy determinants and familiar linear coefficient arithmetic use those prerequisites. Moderate and hard workload remains fixed within each family; neither introduces a new integration technique.

Documented source anomalies are in template-extraction.md and validation.json. No source has been omitted.
