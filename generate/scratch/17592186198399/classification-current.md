# Current-source supplement — basis 2625

This supplements the immutable basis-1356 extraction and replay package. The live KP has 12 practice questions: six moderate and six hard, all radio, with 13 five-choice field banks. No source easy question exists. The affine easy family is an explicitly authored simplification already validated in the frozen package: a constant Jacobian with two nonunit scales, simple integer box lengths, and no nonlinear primitive. The same volume/change-of-variables method and four solution stages remain intact.

Every source was read at basis 2625 with prompt, solution, fields, choices, correct references, difficulty and canonical example. See reference/replenishment/initial/source.edn and source-validation.json. The six original backbone families and their seven banks remain in template-extraction.md. The reciprocal source now has its hard rating, solution and correct reference; the original snapshot remains historical evidence. Its introductory double-integral dA formula is an error; volume requires a triple integral dV. The source is preserved and excluded from audited supply. The linear_yz source retains a duplicate selection key and a missing correct reference; exclude it without altering it.

| New source | Level | Supplied map coordinates | Inverse / volume | Plot rating |
|---|---|---|---|---|
| 17592186482547 | hard | y, x-z, (z-1)/y | (v+uw+1,u,uw+1); J=u; V=32 | none |
| 17592186482580 | moderate | x, y, z-ln(y²+1) | (u,v,w+ln(v²+1)); J=1; V=8 | none |
| 17592186482615 | hard | x, y+3z, z³ | (u,v-3w^(1/3),w^(1/3)); J=1/(3w^(2/3)); V=4 | none |
| 17592186482616 | hard | y²-x, y, z | (v²-u,v,w); J=1; V=2(e-1) | none |
| 17592186499512 | moderate | y-e^x, y, ze^(-x) | (ln(v-u),v,w(v-u)); J=1; V=1; v>u in box interior | none |
| 17592186499523 | moderate | x²-y, x, z | (v,v²-u,w); J=1; V=6 | none |

These are separate source backbone/bank profiles, each with one five-choice selection field, one designated scalar answer, and the same ordered four stages: image box, forward determinant, reciprocal determinant, separated triple integration. The exact domains, values, complete banks and rendered solutions are retained in source.edn. `inventory_validation.py` parses each displayed region, checks inverse composition and branch, integrates the independently derived absolute inverse determinant, checks every choice for distinctness and the designated answer and final solution value, and emits source-specific findings. Native grading exercises every owned option for counted source questions.

The six new profiles are outside the frozen generator's sampling domain. They are not merged into its historical choice recipes, and no fidelity claim is made for generating them. This bounded template exclusion does not exclude any difficulty level: eight validated generation families support easy, moderate and hard. No new plots are required; all 12 practice questions are mathematical text. Canonical notation assets remain unchanged.

Preparation counts only fresh, distinct, audited, gradable tasks, excluding shown/reserved questions. It compares regions normalized under positive/negative scaling and inequality permutation, excluding source and canonical equivalents regardless of choices, UUIDs or seed. Complete native validation specs run in preview and on the writer. The API lock and basis guard protect durable submission and exact-basis readback.
