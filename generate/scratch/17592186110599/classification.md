# Classification

Capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the immutable wrapper. Seven practice questions: four easy, one moderate, two unrated, zero hard. Canonical e-14359 is contextual evidence, not an eighth practice question.

| Observed label | Source IDs | Fields/layout | Markdown/value templates | Complete banks | New plots |
|---|---|---|---:|---:|---|
| Easy | q-215888, q-215890, q-72527, q-72528 | one `selection` math-radio field, five full equations | compact: 1 | 4 | none |
| Moderate | q-72524 | same field/layout | compact: 1 | 1 | none |
| Unrated | q-72453, q-72525 | same field/layout; correct designation absent | spaced: 1 | 2 | none |
| Hard | none | authored same math-radio response | compact reused | 1 authored | none |

The compact family places the question mark inside the inline equation. The spaced unrated family places it after the closing delimiter and uses spaced equations. Their answer shapes are full `y=mx+b` equations. Compact solutions have five paragraph breaks and the same six stages: product criterion; given-line slope; chosen-line slope; introduction to multiplication; displayed product; perpendicular conclusion. Unrated sources have no observed solution and receive a clearly authored solution with the shared stages.

The raw moderate bank q-72524 contains two degree-two options `y=-\frac{x}{2}x+5` and `y=-\frac{x}{2}x-1`. They are preserved only in the explicit `observed-q-72524` evidence profile. They fail the line-only scope condition; normal random generation never selects this profile. `repaired-q-72524` removes the duplicated trailing x factors, preserving all other mathematical components. Repairs are separate from raw fidelity denominators.

For unrated q-72453 and q-72525, inspected original widget JSON and both screenshot sections confirm five math-radio options and no correct annotation/worked solution. Their captures reorder options but retain their complete values. The product criterion independently determines `y=-x/3+6` and `y=-2x+3`. Neither derived designation is counted as a matched original designation. The easy/moderate assignments for these two sources are authored scope decisions.

# Equal-level scope and curriculum grounding

Lesson route was reconstructed from `activity/first-step` and `step/next`: introduction → this KP → standard-form perpendicularity → unknown parameters → horizontal/vertical lines. The prerequisite is slope-intercept equations (topic 1240). Thus all authored targets and options remain explicit slope-intercept equations; no rearranging standard form, solving unknown coefficients, point constraints, or vertical-line branches are introduced.

Easy defaults use signed integer slopes of absolute value 2..12; moderate defaults use signed unit fractions with denominator 2..12. Every question within a level reads one coefficient, recognizes a negative reciprocal among five full equations, and confirms one exact product. The two observed unit-slope easy profiles remain explicit replay profiles; their finite ±1 slope structures are not used to inflate normal variety. Hard is an authored difficulty allocation, not an observed label: coprime non-unit numerator and denominator 2..9 require reversing both fractional components and sign. Canonical e-14359 already demonstrates precisely this workload at -2/5; hard does not move into another KP. Both proper/improper and signed rational slopes have identical operation count. There is no within-level progression or mixture of further algebra demands.

The assessed mathematical fingerprint contains the target slope only, canonicalized as a reduced rational. All intercepts, banks, notation, profiles, and answer ordering belong to presentation/content identity. Meaningful finite domain counts are reported by the validator; hundreds of changed intercepts are not claimed as new mathematical tasks.
