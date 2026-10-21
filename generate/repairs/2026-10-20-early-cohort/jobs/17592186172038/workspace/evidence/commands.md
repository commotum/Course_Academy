# Current asset-reference repair

Run from the workspace:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_asset_reference_repair.py
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_inventory.py
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/asset-reference-repair/render-records.json --output evidence/asset-reference-repair/render --asset-root evidence/assets --asset-root evidence/asset-reference-repair/separate/deep/outputs-b --math-root /media/jake/SSD/EDB/math
```

The runner lookup defect is reproduced in `before-result.json`, using `generator_pipeline.asset_hashes` on `before.json` with the pre-fix generator. The PNGs existed in the configured output directory but emitted basenames pointed to nonexistent runtime files. The generator now emits configured absolute asset paths and uses basenames only for content/answer identity. No bank, equation, sampled role, arithmetic domain, source replay profile, or worked-solution stage changed.

`result.json` saves exact CLI, delivery and grader commands plus runtime hashes. Two relocated four-file packages, each run twice with fresh output directories (seed 71, count 5), pass the actual runner asset-binding function. Repeated records/bytes match; output-normalized records match across package roots and the previous batch, including IDs. The bundled runtime files remain unchanged when run. Seven source banks/35 choices replay with complete geometry and five observed/two inferred keys. The bounded regression contains 56 records and six controlled sign/point/presentation groups; independent Fraction evaluation, parsed displayed substitutions and endpoint slopes agree. Four domain/ambiguity rejections remain strict. Native grading passes 113 accepted/452 rejected choices (565 checks), including normalized delivery. Delivery accepts 50 mathematical instances from 56 records; the six skips are duplicate presentations, with no semantic instance lost.

`pedagogical-variation.json` compares within-form position/count/sign/magnitude cues before/after the shared delivery filters. No tested cue predicts all answers within a form. These controls are not a random frequency estimate; the prior 240 normal-bank probes remain in `../bank-probes-before.json`. Samplers and rejection rules are unchanged. Read-only `question_selection.rs` inspection confirms configured weighted band selection then uniform within-band selection; unconfigured policy chooses the smallest candidate entity. Live learner history, policy configuration, future IDs, and concurrent inventory changes remain untested.

`render-records.json` has a fresh relocated record, a changed-point case, and q-49811 vertical-distractor replay. All three actual Learning.html screenshots (`render/question-001.png` through `question-003.png`) passed and were visually inspected: references resolve, mathematical stages and plotted geometry agree, and no clipping or broken math was observed. All seven original source contact sheets were also inspected. `../inventory-audit.json` checks all 17 captured stored records for canonical asset resolution/hash and missing keys: no asset-reference failure demonstrated; two pre-existing missing correct references remain recorded in `../../affected-inventory.json`. No claim of an exhaustive raster-bank pedagogical audit or live inventory verification is made.

Full reports and samples stay local. Nothing was published, uploaded, or written to a database. Earlier reports below describe earlier repairs and are retained as history; this section and `asset-reference-repair/result.json` describe the current runtime.

# Reproduction commands

Current classification feedback repair (the runtime files are unchanged):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/check_classification_repair.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/classification-repair/render-records.json --output evidence/classification-repair/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

The manifest declares `default_difficulty: "easy"`, justified by five original easy labels. Source replay: seven unchanged complete banks, 35 options. Manifest-selected CLI: five easy records, identical to the preserved relocated run. Controlled sign, point and presentation checks passed for all six equation forms. Delivery accepted 23 semantic instances from 29 records (six presentation duplicates), retaining all six forms and every semantic instance. Native grading passed 59 accepted and 236 rejected responses, including normalized delivered records. Both actual Learning.html screenshots in `classification-repair/render/` were visually inspected: readable diagrams, correct orientations and substitutions, no clipping, broken images or math errors. Full commands and exact runtime hashes are in `classification-repair/result.json`; the source labels and runtime files were preserved.

`classification-repair/shortcut-probes.json` repeats within-form cue checks before and after delivery. These controlled samples are not random frequency estimates; retain the earlier 240 ordinary-bank probes and coverage limits below. Classification metadata has no per-question inventory counterpart; the existing read-only inventory findings remain in `../affected-inventory.json`.

Run from the workspace with `PY=/home/jake/Developer/Course_Academy/.venv/bin/python` and `REPO=/home/jake/Developer/Course_Academy`.

- `$PY evidence/probe_banks.py`: 40 valid ordinary easy banks per equation form; choice position and min/max horizontal-count, positive-count, angle magnitude/sign and distance-to-others probes. Full results: bank-probes-before.json. Highest per-form tested cue rate in this sample: 0.25–0.408; no deterministic predictor demonstrated.
- `$PY evidence/validate_repair.py`: source bank replay, independent Fractions/printed-TeX/segment checks, controlled sign/point changes and presentation invariance, all five choices through one native grader batch, and actual shared delivery filtering. Results: source-replay.json, counterfactuals.json, validation.json, engine-report.json, delivery/delivery.json. Samples: source-replays.json, generated.json, delivery/accepted.json. Initial fixture-only failures were repaired: one alleged invalid parameter set was valid, and probe parsing needed to support source vertical slopes (`oo`). No generator acceptance criterion was weakened.
- `$PY evidence/check_relocation.py`: copies exactly four manifest files to two distinct locations; runs `--difficulty easy --count 5 --seed 71 --format json` with separate `COURSE_ACADEMY_GENERATOR_OUTPUT_DIR`; compares outputs and checks runtime files unchanged. Results: relocation.json; samples: relocated-a-records.json and relocated-b-records.json.
- `$PY evidence/check_delivered.py`: all 225 normalized choice responses through the native grader; shared delivery on the five CLI records from the relocated package. Results: delivered-engine-report.json and relocated-delivery/delivery.json.
- `$PY evidence/check_inventory.py`: 17 stored records, canonical-image resolution/hash checks and missing correct references. Results: inventory-audit.json and ../affected-inventory.json. Does not mutate any record.
- `$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math`: six ordinary equation forms (the renderer defaults to six). Actual Learning.html screenshots question-001.png through question-006.png were all visually inspected.
- `$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-source-records.json --output evidence/render-source --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math`: source q-49811 with vertical distractors. Screenshot inspected separately.
- `$PY evidence/finish_audit.py`: summarizes parameter/sign/target/choice-position coverage before and after delivery, isolates normal authored profile probes, and hashes runtime files. Results: pedagogical-variation.json and validation.json.

No database writes, publication or image upload occurred. Existing legacy reports are retained but new reports above are authoritative for this repair. Native grading and delivery tests are database-free. Source snapshots, inventory, live UI code and native grader binaries are read from the supplied paths only during author validation, and are not runtime dependencies.
