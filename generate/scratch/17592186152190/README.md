# Part-of-ellipse generator

Scope: standard positive cosine/sine axis-aligned quarter/half ellipse parametrizations. Easy: origin first-quarter/upper half; moderate: origin other quarters and left/lower halves; hard: translated arcs. All levels are observed. Source snapshots are math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186152190/validate.py
.venv/bin/python generate/scratch/17592186152190.py --difficulty all --seed 42 --count 2 --format json
```

Validation uses the actual in-memory application grader at generate/runs/current/check-engine. It separately validates every source value/designation, printed prompt/solution mathematics, field layouts, domain restrictions, curve endpoints, asset parameter specs, stable identities and explicit-invalid-input rejection. Replays use the normal generator and original complete bank profile. No EDB access/writes, engine edits, registration or commits.

Evidence: source.json retains raw originals; source-cases.json supplies 18 parameterized replays; templates.json contains 15 extracted prose/layout skeletons and 10 full geometric interval banks; choice-mapping.json lists every field/value/recipe. review.md shows originals, repaired parameter replays and generated variants. review.json includes at least two generated instances per observed template/bank and every difficulty. validation.json separates 69/69 answer-value matches, 25/25 correct designations and 0/18 exact worked prose from 18/18 supported repaired solutions.

Repairs: every solution's central-angle claim is replaced with the exact normalized-unit-circle parameter-angle interpretation. q-274866 copied center/radii, q-327831 variable names and q-79282 missing separator are also repaired. Historical distractor error intent is unknown, but its complete categorical geometric banks are reproduced and independently checked. There are no unresolved fidelity or grading comparisons.

Matplotlib PNG generation uses the exact mathematical instance. The primary environment lacks Matplotlib; render.py uses already cached Python 3.10 wheels read-only without installation, with provenance recorded. All artifacts stay in this owned evidence folder. plot-extraction.md and plot-qa.md describe source and generated visual review. plot asset/spec files are deterministic by mathematical object plus prompt-context presentation.
