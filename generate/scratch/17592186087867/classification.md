# Classification

Source: database math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Capture wrapper is preserved in `source.json`. All 12 practice sources are rated and have one `selection` radio field containing five whole equations. No field anomaly was found. Canonical e-6600 supplies the method but is excluded from practice counts.

| Level | Sources | Worked-solution/value families | Complete banks | Plot rating |
|---|---|---|---|---|
| easy | q-8349, q-103551, q-103554, q-79753 | 1 standard-form recognition sentence layout, with four structurally different complete categorical banks | 4 | none |
| moderate | q-103560, q-103557, q-103559, q-79750, q-79752 | 3: direct nonlinear-power recognition, direct nonlinear RHS recognition, rational rearrangement | 5 | none |
| hard | q-8352, q-79754, q-103567 | 3: dividing a y-dependent coefficient remains nonlinear; clearing a reciprocal y factor with collection; clearing a reciprocal y factor with exponential coefficient | 3 | none |

The implementation uses 12 bank-specific recipe identifiers rather than conflating bank count with shared sentence layouts. This preserves each observed function/object structure and the worked-stage differences. q-79750 also contains a linear option with an apparent y-dependent derivative coefficient that cancels locally; this feature must be retained, rather than automatically marking every y-dependent coefficient nonlinear.

Owning topic 17592186050608 is Introduction to First-Order Linear ODEs. Following `activity/first-step` then `step/next`, the route defines general and standard forms, teaches Writing First-Order Linear ODEs in Standard Form, then this KP, then homogeneous/inhomogeneous classification. This generator assesses recognition and local algebra only. It never asks for an integrating factor, solution curve, integration, initial condition, or homogeneous classification.

All levels have observed sources. There are no authored missing-level assignments. Easy selects the already-standard-form linear equation against higher-order/nonlinear forms. Moderate identifies the sole nonlinear equation among standard or simply normalizable equations. Hard retains cancellation and rearrangement of y-dependent factors, including coefficient functions whose complexity alone does not imply nonlinearity. Affine changes of the independent-variable functions preserve these demands; level variants are unordered instances, not a progression.

## Parent solution correction

q-79750’s original rationale says dependence on y prevents linearity, which is incomplete: a linear y term on the right can be collected. The generated sentence now specifies the nonlinear y² term. All12 source prompts,60 options and12 designations remain exact;11 supplied worked solutions remain byte-exact and one has this documented correction. Original evidence remains unchanged.
