# Classification

Snapshot: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw wrapper copied unchanged to `source.json`. All ten practice questions are represented; canonical e-6810 is context, not an eleventh practice case.

| Captured level | Sources | Field layout | Markdown/value templates | Banks | Plot rating |
|---|---:|---|---:|---:|---|
| easy | 5 | one `selection` radio, five math choices, whole determinant expression | 5 | 5 | none |
| moderate | 4 | same | 4 | 4 | none |
| absent | 1 | same, correct ref absent | 1 | 1 | none |
| hard | 0 | authored same field shape | 1 authored | 1 authored default | none |

Easy families: `polar` q-38078; `linear` q-160381; `linear_log` q-160404; `tan_product` q-38241; `quadratic` q-81264. Moderate: `exp_log` q-160403; `cos_linear` q-160405; `trig_pair` q-81252; `exp_quadratic` q-160406. The unrated `log_product` q-38244 receives an **authored moderate** assignment: differentiating a logarithm of a linear form and a product, then simplifying the rational determinant, comparable to the observed exp/log family. This is not a recovered original rating.

All templates use four first partials and the 2x2 determinant, but retain different transformations, symbolic answer shapes and simplification rows. All source profiles are five-option banks. Source order is irrelevant to the bank comparison. Each profile is complete; no recipe pooling occurs. Separate authored method-error defaults avoid treating sparse observed error hypotheses as recovered intent.

`hard/powers` is supported by canonical e-6810: x=(u+v)^3 and y=(u-v)^2. Allowed outer powers (3,2), (2,3), (3,3) and scales 1..3 require the same four chain-rule derivatives and determinant factorization. The task stays symbolic: no evaluation at points, integration, orientation, area or inverse-function work. This is an authored missing-level design claim, not a source difficulty label.

Practice sources contain no mathematical figures. The canonical prompt bitmap was inspected and shows only the transformation vector. No plot renderer is needed; its content is recreated in native LaTeX. The introductory and downstream lesson illustrations are curriculum context, not parameter-dependent question assets.

Two source issues: q-38078 has a `cos² v + cos² v` solution typo (must be `cos² v + sin² v`); its determinant and all choices are correct. q-38244 lacks rating, worked solution and correct ref; the authoritative local MA widget confirms the same five choices, without a designation. The normal generator derives the correct determinant independently, and does not count its new designation as an original designation match.


## Parent variety review

Hard retains the canonical powers-of-linear-forms method and adds inner coefficients 1 or 2: x=a(pu+qv)^m, y=b(ru-sv)^n. Outer scales remain 1..3 and powers (3,2),(2,3),(3,3). All-one inner coefficients reproduce the canonical form. These 432 bounded parameter combinations vary the four chain-rule factors without adding a mathematical branch, evaluation, orientation, or area scaling. This extension addresses the initial 27-combination limit; it is authored variation rather than an observed template.
