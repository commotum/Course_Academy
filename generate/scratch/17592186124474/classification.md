# Classification at math basis 1356

The capture contains 12 practice questions: four easy linear formulas and eight moderate folded formulas (four quadratic and four absolute-value). Eleven have one `selection` radio field with five text choices; q-66785 has no answer-fields attribute. There are no hard examples. Every prompt supplies a formula and three intervals. Every raster is in the worked solution: the assessed input is the description, not an unreadably scaled graph. Plot rating is light for lines and moderate for folded-function explanations.

| Source/template | Observed level | Formula family | Plot panels/files | Bank |
|---|---|---|---|---|
| q-66723 | easy | positive line | 1/1 | all three, no Oxford comma in option |
| q-66483 | easy | decreasing constant-first line | 1/1 | all three, Oxford comma |
| q-66725 | easy | decreasing line; decimal/radical interval bounds | 1/1 | all three, Oxford comma |
| q-66724 | easy | positive line; explicit Roman labels | 1/1 | all three, no Oxford comma in option |
| q-66482 | moderate | vertically shifted quadratic | 4/3 | II and III |
| q-66785 | moderate | translated absolute value | 1/1 | absent; raw ineligible |
| q-36010 | moderate | translated absolute value | 4/3 | I and III |
| q-66669 | moderate | horizontally shifted quadratic; numbered construction | 4/3 | I and III |
| q-66679 | moderate | doubly translated quadratic; numbered construction | 4/3 | I and II |
| q-66687 | moderate | reflected/vertically shifted quadratic; subset inference | 3/3 | I |
| q-66729 | moderate | translated absolute value | 4/3 | I and II |
| q-66778 | moderate | translated absolute value; III then II plotted | 4/3 | II and III |

Templates retain individual source masks where full prose/layout differs. There are four observed easy masks, seven complete moderate masks, and one fieldless moderate evidence mask. Bank profiles are complete per-source selector banks, not pooled options. Difficulty remains the captured label for source replays.

## Curriculum anchor and authored levels

The lesson route is reconstructed from `activity/first-step` 17592186125322 and `step/next`: Introduction → KP 17592186124472 (invertible graph) → KP 17592186124473 (intervals from graph) → this KP 17592186124474 (intervals from description). Pull collection order is not used. The introduction explicitly defines invertibility on a restricted domain as one-to-one and uses a restricted quadratic; canonical e-3963 supplies a shifted absolute-value formula. Key prerequisites are elementary quadratic graphs, absolute-value graphs, vertical quadratic reflections, and lines in slope-intercept form.

The authored easy constant-line contrast applies the same one-to-one test with slope zero; it adds the empty selector subset. Nonzero lines have only one semantic task here: all three nondegenerate listed intervals work. Coefficient, sign, letter, and endpoint-number aliases are not counted as new tasks. Easy's honest semantic catalog has two tasks.

The authored moderate `integer_quadratic` and `integer_absolute` masks supply an integer vertex (|h|≤6, |k|≤6), exactly one half-infinite interval, one finite single-branch interval, and one finite crossing interval. They reuse the source branch/domain restriction method with simple integer comparisons. Their catalog contains 72 meaningful ordered domain structures, covering branch choice, finite/unbounded domains, vertex inclusion, and Roman positions. The complete five-option authored bank contains the true pair, omission of either true interval, and replacement of either true interval by the crossing interval. No arbitrary numeric distractors occur.

The missing hard level is explicitly authored, not a recovered label: `rational_quadratic` and `rational_absolute` require a reduced noninteger vertex of denominator 2, 3, or 4, |h|≤4, |k|≤4, and three finite intervals. Each instance compares exact rational bounds, checks whether the vertex is included as an endpoint, and distinguishes a crossing interval. All variants use the same branch test and a symmetric-input witness; there are no derivatives, inverse calculations, or additional function classes. The honest hard structural catalog has 90 ordered domains; denominator/translation/scaling and the quadratic/absolute-value realization do not increase that count. Each level has equal-demand variations, not an instructional progression.

## Source anomaly

q-66785 is missing exactly `:question/answer-fields`. It remains a public `profile="raw"` replay with that attribute absent, `evidence_only=true`, and `eligible_for_learning=false`. Its supplied solution establishes I only, independently verified by intervals relative to vertex 4. `profile="repaired"` adds a clearly authored five-choice radio bank and inferred designation; neither the new bank nor designation counts toward observed fidelity. No source mathematics required repair.
