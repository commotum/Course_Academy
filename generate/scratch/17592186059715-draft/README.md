# KP17592186059715 local all-three-level draft

Script: `generate/scratch/17592186059715-draft.py`; evidence/assets stay in this private directory. Registered numeric generator and its evidence remain unchanged. Stop at generator/plot creation, no publication, registration, database transactions, shared engine edits or commits.

Verify:

```sh
.venv/bin/python generate/scratch/17592186059715-draft/validate.py
.venv/bin/python generate/scratch/17592186059715-draft/summarize-domains.py
.venv/bin/python generate/scratch/17592186059715-draft.py --difficulty all --seed 0 --count 2 --format json
.venv/bin/python generate/scratch/17592186059715-draft.py --difficulty moderate --profile evidence:q-18051 --parameters '{"scale":1}' --format markdown --count 1
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Normal explicit parameters are `{"points":[[px,py],[qx,qy]]}` and must obey the same per-level rules as sampling. Families: `coordinate_ab`, `coordinate_pq`, `coordinate_pq_signed`, `coordinate_cd`, `graph_read`. Hard supports graph_read only; easy supports the four printed-coordinate families. Source aliases q-* are accepted. `field_type` supports radio. Raw original replay uses `evidence:q-*`; q-18051/q-18052 have scale1..4 evidence parameters, the other three use endpoint tuples. Evidence records are `evidence_only=true`, `eligible_for_learning=false` and retain original field/key/solution/difficulty/calculator absence. CLI handles omissions. All source cases use the public API.

At basis2275 there are five original MA records (two unrated radios without keys/solutions; three moderate records without fields) plus five independently authored records. Exact wrapper copied unchanged; complete independent inventory is retained separately. Full original available-bank replay is10/10 values,8/8 distractors,2/2 banks;5/5 exact prompts and3/3 exact present solutions, with all absence preserved. No original correct designations exist to match. Historical distractor intent remains unresolved, so opaque homogeneous evidence profiles are excluded from normal sampling. Source notation remains exact in raw replay, and normal radio fields/keys/solutions are explicitly authored completions.

Authored easy prints small nonnegative endpoints0..6; moderate uses observed signed-coordinate/unit-grid families; authored hard reads signed coordinates from two-unit ticks (including odd integers between ticks). All keep directed endpoint subtraction followed by Euclidean norm and the same ordered solution stages. No direct supplied displacement, unit vectors, 3D, dot products or angles. Workload/domain rationale is in classification/template extraction. Full finite enumeration excludes common translations, names, option order and bank aliases:280 easy meaningful tasks;1560 signed-coordinate moderate tasks plus24 graph tasks;4520 hard graph tasks. Do not sum the cosmetic coordinate-family copies.

Normal bank is a complete method-derived profile: correct norm, norm of added position vectors, Manhattan sum, omitted-root squared norm, and omitted-squares root of absolute-component sum. All ten pairs must differ as exact scalar responses; whole-instance collisions are rejected. Reverse displacement has equal magnitude and is never a wrong scalar option. Answer feedback is absent in the sources and remains absent.

`validate.py` independently reads displayed endpoint coordinates or calibrated actual graph PNG marker pixels, position vectors, formal direction, numeric vector subtraction, each signed component, each square, square sum and final radical. It tests original masks under changed parameters, all default families, bounds on explicit calls, stable seed/shuffle identity, control-character/omitted-stage/wrong-square regressions, and fresh same-directory concurrent identical/different renders. Real native grading is a separate memory-only radio field-owned ID compatibility test; it cannot prove the mathematics of a choice. `native-report.json` reports all results honestly. Source plot inspection is native-resolution and separately calibrated from image provenance hashes.

Changed parameters retain the explicit collected radicand `\sqrt{dx²+dy²}` after individually evaluated squares. A conditional terminal simplification row is added only when the exact radical reduces (already required by the source bank 5√2); original three-row norm blocks remain exact at their anchors. This prevents CAS simplification from hiding the square-sum stage.

Final local validation:180 normal sampled instances,5 original replays,9 changed evidence instances and4 arithmetic/plot boundaries; native memory fixtures195 accepted/780 rejected/0 unresolved. Parent independent QA is deferred while the user’s13 new priority KPs run; this draft is ready for later QA and is not approved or registered.
