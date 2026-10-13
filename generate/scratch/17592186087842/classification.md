# Classification at math basis 1356

KP 17592186087842 / 60c99086-75e7-5d91-b425-4e1b6f582bcc, “Calculating the Vertical Asymptotes of a Rational Function.” Capture lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` preserves the complete capture wrapper and record, including all missing attributes. Ten practice sources, separate from canonical e-5299.

| Source | Observed level | Field layout | Family | Supplied solution | Bank |
|---|---|---|---|---|---|
| q-39796 | missing; authored hard | mixed math/text radio, five | two proper fractions, reversed linear denominator | missing | observed_39796 |
| q-4629 | missing; authored moderate | mixed math/text radio, five | numerator GCF quadratic / monic quadratic | missing | observed_4629 |
| q-6908 | missing; authored easy | math radio, five | constant / monic quadratic | missing | observed_6908 |
| q-278249 | easy | two ascending scalar blanks | linear numerator / repeated-root cubic | yes | observed_278249 |
| q-39790 | easy | missing; authored two blanks | linear numerator / nonunit-leading quadratic | yes | observed_39790 |
| q-269955 | moderate | two ascending scalar blanks, field-2 captured first | numerator GCF quadratic / difference of squares | yes | observed_269955 |
| q-278534 | hard | two ascending scalar blanks, field-2 captured first | sum of two proper fractions | yes | observed_278534 |
| q-39791 | easy | math radio, five | constant / quadratic with numerical GCF | yes | observed_39791 |
| q-80669 | moderate | mixed math/text radio, five | numerator GCF quadratic / monic quadratic | yes | observed_80669 |
| q-39793 | easy | math radio, five | three already factored distinct real poles | yes | observed_39793 |

The ten public replay masks preserve exact source presentation and bank profiles; they are not ten distinct skills. The meaningful families are denominator quadratic factoring (including a nonunit linear factor), repeated root, supplied three factors, numerator factoring plus denominator factoring, and addition of two fractions. Field layouts and supplied/missing solution sequences remain separate. No practice prompt, option, or solution contains a plot: plot rating **none** for every family, no plot extractor/renderer required. The lesson’s introductory graph teaches terminology and is not an assessment asset.

The actual route follows first-step 17592186088763, then next links 88764 (this KP), 88765 (common factors), 88766 (complex roots), 88767 (common factors plus complex roots). Neither collection order nor generic “harder” algebra determines scope. This KP’s key prerequisites are solving quadratics by factoring (topic 375) and solving quadratics with leading coefficients by factoring (1422). All generated reduced denominators split over real rational roots, and no numerator cancels a denominator factor.

MA lesson 807 captured JSON independently confirms the complete banks and multiple-choice widgets of q-6908, q-4629, q-39796. It has no source solution/key for these; those additions are authored mathematical derivations, not recovered labels. It does not contain q-39790. Therefore q-39790 receives an explicit authored two-blank layout and minimal ascending-order instruction instead of claiming an authoritative recovered widget. No existing original correct ref is replaced. Missing correct designations never count as matched source designations.


## Public raw evidence replay

Every `observed_<id>_raw` profile is available through the same `generate` API, selected using `source-cases.json`’s `raw_bank_profile`. It performs the same positive dilation of mathematical components and all choices while preserving attribute absence: missing original difficulty, worked solution, field layout and correct references remain absent. Raw q-39790 remains fieldless. All raw profiles are evidence-only and ineligible for learning; completed `observed_<id>` profiles separately carry supported authored repairs. `raw-source-replays.json` contains all ten original raw public replays and ten changed variants. Validation checks the absent attributes, exact available strings/full banks, changed actual function names/poles and deterministic identities. Raw records with absent assessment attributes are not passed to the native grader as if complete learner records.
