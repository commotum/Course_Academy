# Classification — math basis 1356

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
