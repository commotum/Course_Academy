# Classification — KP 17592186059711

Frozen capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; `source.json` is an unchanged copy of the wrapper. KP UUID `1735c445-9c97-5aa7-83d6-7dee23993153`, topic244 / topic database17592186050136.

| Source | Observed difficulty | Mathematical / Markdown family | Captured fields | Captured solution | Plot rating |
|---|---|---|---|---|---|
| q1304 | absent (unrated) | `subtract`: two integer pairs; “If … then u−v=” | one radio, selection, five math vectors; correct ref absent | absent | none |
| q17611 | absent (unrated) | `linear`: signed integer pairs; “Let … Find a+2b” | one radio, selection, five math vectors; correct ref absent | absent | none |
| q1301 | easy | `sum`: “What is the sum”, overset arrows, two integer pairs | answer-fields attribute absent | two-row substitution/evaluation chain | none |
| q1389 | easy | `scalar`: “If … then”, integer + positive half, negative scalar | answer-fields attribute absent | three-row substitution/component products/evaluation chain | none |

Observed easy: two fieldless Markdown/value templates, zero observed choice banks. Observed unrated: two radio templates and two separate complete banks. Observed moderate and hard: zero. Canonical e4293 is an example, not a practice source, and is excluded from practice fidelity denominators.

Each practice prompt, every captured choice and both complete worked solutions have no image references. The assigned canonical example also has none. Other topic/sibling illustrations are context, not assets in this assessed task. No source graphics need reconstruction; no plot generator or SVG is used.

## Source anomalies and authoritative widget inspection

The captured authoritative `/home/jake/Developer/MA/DATA/Lessons/244/Source/244.json` entries with question_id1304 and17611 confirm five-choice radio widgets. Their full option sets agree with frozen EDB, ignoring ordering. The source HTML confirms actual radio table structure. Neither widget captures a correct marker or worked solution; these cannot count as recovered designations or exact worked-solution replay. That lesson snapshot has no q1301/q1389 widget. Frozen EDB supplies their observed easy labels and exact solutions, but no fields.

Raw profiles `raw_q1304`, `raw_q17611`, `raw_q1301`, `raw_q1389` remain public through `generate`; they preserve absence of difficulty, fields, refs and worked solutions individually. They are explicitly evidence_only/ineligible. They are parameterized recipes, not copied question payload branches.

Normal completion adds independently derived radio correct refs to the existing banks, and source-style authored worked solutions for the two unrated questions. q1301/q1389 receive explicitly authored five-choice radio fields, using the owning KP's supported observed radio response. No source bank or field is silently dropped. The two missing original correct designations remain denominator0/0, while ten displayed source options and two complete banks are compared independently.

Decoded source strings were checked for adjacent U+005C characters, using ord92. Prompt commands use one backslash; adjacent-backslash counts are0 for all four prompts. Solution row separators use two backslashes as expected. No TeX escape anomaly or repair is claimed.

## Curriculum anchoring and level design

The activity route is followed by activity/first-step and step/next: introduction → component-form KP59710 → angle/column arithmetic tutorial → this KP59711 → column KP59712 → notation tutorial → diagram/alternative notation KP59713. The prerequisite topic is “Two-Dimensional Vectors Expressed in Component Form”. The subsequent topics include direction, magnitude and 3D vectors; those are outside this generator.

Easy defaults uniformly select all three single-operation families: sum, subtraction (authored assignment of unrated q1304), scalar multiplication. Two component additions/subtractions OR two products are assessed. Scalar multiplication preserves q1389's integer first component and noninteger half second component. This difference is an observed equal-level family, not an authored progression.

Moderate has exactly two component scalar products and two component additions/subtractions, one vector unscaled; q17611 and canonical e4293 anchor this workload. Its difficulty is authored because no captured moderate label exists. Hard has exactly four component products and two additions/subtractions, both vectors with nonunit scalars; canonical e4293 and neighboring column example e4294 support this bookkeeping extension, while the response and input stay in angle brackets and two dimensions. Hard does not add a third vector, nested expression, dot/cross product, geometry, equation-solving or another representation. Equal-level sign and operand changes are unordered variants.
