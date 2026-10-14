# Classification at math basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen source, topic and lesson wrappers are `source.json`, `topic.json`, and `lesson.json`. Old evidence under `reference/` belongs to earlier work and is not the current source basis.

There are nine practice sources: eight labeled easy, one labeled hard, none labeled moderate. All fields are radio with five complete-equation choices. q-16400 has two legacy fields sharing `selection`; the first lacks a correct reference. Raw replay preserves both and this missing attribute. Normal output uses one supported five-choice field. No blank field is present; native complete-equation blank parser restrictions therefore do not affect this generator.

| Level | Source / template | Mathematical backbone | Rows | Banks | Plots |
|---|---|---|---:|---:|---|
| easy | q-16400 | Move forcing and y term; divide constant leading coefficient | 3 | 2 legacy layouts | none |
| easy | q-8359 | Split quotient; move y term; cancel x in forcing | 4 | 1 | none |
| easy | q-103349 | Move forcing; divide exponential leading coefficient | 3 | 1 | none |
| easy | q-103354 | Move forcing; divide cosine; double-angle expansion/cancellation | 5 | 1 | none |
| easy | q-16396 | Collect; factor y; cancel nonzero y; isolate forcing | 6 | 1 | none |
| easy | q-79697 | Invert derivative coefficient; cancel x; distribute; collect | 6 | 1 | none |
| easy | q-79699 | Collect; factor -y; cancel y; multiply inverse exponential; collect | 8 | 1 | none |
| easy | q-8360 | Move forcing; identify coefficient/forcing | 3 | 1 | none |
| hard | q-16401 | Expand a square, cancel matching quadratic terms, collect linear term | 4 | 1 | none |
| moderate, authored | rational-collect | Collect y terms from both sides, divide ax; two nontrivial rational coefficients | 3 | 1 authored | none |

The raw source field count is ten; nine have original correct designations. Every source option is retained and compared, including the missing-correct legacy bank. Values are full equations; strict standard-form eligibility is distinct from ODE equivalence. q-8359 and q-8360 intentionally contain equivalent rearrangements which are not in the requested standard form. They are legitimate distractors, not ambiguous correct answers.

Lesson order follows first-step/next: Introduction → Standard Form tutorial → this KP → Identifying First-Order Linear ODEs → Homogeneous/Inhomogeneous tutorial → Identifying Homogeneous/Inhomogeneous ODEs. The prerequisite is Introduction to Differential Equations (topic 3215). Integrating factors belong to a later topic and are excluded, as are solving equations, classifying linearity, and homogeneous/inhomogeneous classification.

Moderate is an explicit design claim, not a recovered source label: the canonical example collects a constant forcing term; the lesson defines P=b/a and Q=f/a; the authored moderate combines collection from both sides with division by a nonconstant ax. Nonzero d and c ensure neither rational coefficient loses its reciprocal-x contribution. There is no within-level progression.
