# Classification at basis 1356

Snapshot: math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
The complete five-question practice collection is retained in source.json. There
are no missing fields, unreadable assets, unrated sources or mathematical errors.
The canonical example e-17212 is context, not a sixth practice question.

| Level | Practice | Markdown/value templates | Complete banks | Fields | Plots |
| --- | ---: | --- | --- | --- | --- |
| easy | 4 | scale_radio (3); shift_radio (1) | observed_ratio, observed_scale, observed_signed, observed_shift | one radio, key selection, 5 math choices | none |
| moderate | 1 | affine_blank | blank (one correct fragment) | one blank, key field-1, p supplied in prompt | none |
| hard | 0 observed | fraction_affine_blank (authored) | blank | one blank, field-1, parameter name supplied | none |

Scale and shift differ in the coefficient expression, inverse operation and
parenthesized prompt, but share the final single solving row. Affine keeps a
nonunit coefficient and nonzero shift, requiring two inverse operations and two
aligned solving rows. All source banks are separate; three scale radios are
number/profile variants of one template, not three new skills. The hard template
changes number form, not the condition or number of unknowns.

Lesson route is reconstructed from activity/first-step and step/next in
lesson-route.json. It runs Introduction → Identifying Equations With Infinitely
Many Solutions → Conditions for an Equation To Have Infinitely Many Solutions
→ Problems Involving Unknown Parameters → this KP. Only afterwards does it
introduce a general linear equation and the separate two-parameter KP10721.
The live capture explicitly identifies prerequisite topic343, Solving Linear
Equations With Variables on Both Sides. The conditions tutorial explicitly shows
1/3 as an x coefficient. These facts, the canonical (5s+4)x=9x and the observed
two-step moderate source anchor the authored hard design: equate one affine
coefficient to the other, subtract a small rational, divide by a small rational.

The hard label is a design claim, not recovered source difficulty. It retains
exactly one parameter in a homogeneous equation and the same ax=bx argument.
No independent x-constant term, simultaneous matching, parameter sum, nonlinear
parameter, distribution branch, or subsequent KP's method is introduced.
All hard instances use three noninteger reduced coefficients, unequal offset/RHS
denominators, noninteger reduced subtraction and noninteger result; none may
collapse into a source easy or moderate arithmetic workload. There is no
within-level progression. The same bounds apply to explicit inputs and sampling.
