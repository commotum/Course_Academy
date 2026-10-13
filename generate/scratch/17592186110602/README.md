# Axis-perpendicular equation generator

Step 3–7 scratch artifact, math basis 1356. No database writes/registration, engine edits or commits.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186110602/validate.py
.venv/bin/python generate/scratch/17592186110602.py --difficulty all --seed 14 --count 2 --format markdown
```

The interface supports generate_easy, generate_moderate, generate_hard and generate(level, seed, template, field_type, parameters, profile). Parameters are c (reference constant), a/b (point coordinates), and optional fraction/decimal style. Use exact strings for rational values. Explicit invalid inputs fail; normal samplers reject whole invalid banks. Six observed radio profiles imply their corresponding template; authored_coordinate_sign/authored_zero_coordinate are complete default banks. Blanks preserve two fields and canonical primitive integer standard-form fragments.

Eight source prompts/field layouts, six full banks (30 choices, 24 distractors), six available correct designations and six worked solutions are replayed exactly. Four missing blank correct references are derived from inspected original two-field widgets; missing values/solutions cannot count as matches. Review shows originals, each bank/template variant and two generated instances per template per level.

Moderate/hard are authored exact-coordinate representation bounds, with the same categorical orientation/coordinate method. This KP has a low intrinsic difficulty ceiling; see extraction for the finite variety policy and limited workload claim. Native blank grading is per fragment, so whole-equation rescaling that changes both fragments cannot be accepted as one coupled equivalence. Equivalent and incorrect fragments are tested directly through real learning::grade_field. Full equation equivalence is independently checked for radios and assembled blanks.

Source.json is unchanged raw evidence. Original-widgets.json and original-widget PNGs preserve authoritative layouts. Classification/extraction, source-cases, validation, native grading/provenance, review and freeze evidence live here. No generated plot is needed.
