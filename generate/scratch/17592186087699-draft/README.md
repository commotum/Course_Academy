# Direct-verification inverse2x2 draft

Owned implementation: `generate/scratch/17592186087699-draft.py`, with evidence under this folder. No registration/database/engine edits. Numeric script/tree/pycs were absent at pre-import baseline; frozen dispatch reports no generator. Root QA approval remains pending.

```bash
.venv/bin/python generate/scratch/17592186087699-draft/validate.py
.venv/bin/python generate/scratch/17592186087699-draft/render.py
.venv/bin/python generate/scratch/17592186087699-draft.py --difficulty all --seed 0 --count 1 --format json
```

The last command returns a list of exactly3 records. API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus easy/moderate/hard entrypoints. Template IDs are the original q-IDs or e-4499; profiles are observed/completed and raw-source evidence. `original_parameters(template)` supplies original rational matrices and witness slots. All raw-source output is explicitly ineligible; normal canonical output remains fieldless/ineligible and excluded from defaults.

`source-cases.json` preserves all original practice records; `templates.json` contains reusable complete masks; `source-fidelity.json` reports complete original prompt/solution/bank checks separately from source omissions and normal completions. `review.md/json` compares originals with variants of every profile/family at every level. `validation.json`, `negative-controls.json`, `engine-report.json`, `render-report.json` and `variety.json` contain checks actually run. `reference/grader-verification.json` verifies all42 current native helper provenance hashes. A preserved initial submission-format diagnostic records that grade_field expects authored answer IDs for checkboxes too; corrected checks follow the actual player's explicit true/false answer-entity contract.

Moderate/hard are authored uncalibrated rational-arithmetic workload placements within direct multiplication verification. They introduce no new inversion method. Matrix-entry equivalent blank grading does not apply: the original fields are Boolean checkbox entities or a text radio bank. No numerical blank field has been invented merely for grading probes.
