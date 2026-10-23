All commands run from evidence_root. Package/database content was not modified. PYTHONDONTWRITEBYTECODE=1 was used for package imports.

Python: /home/jake/Developer/Course_Academy/.venv/bin/python

- `python -B audit.py` saves deterministic samples, 17 replays, target/order pairs and packaging tests.
- `python -B verify_saved.py` independently checks displayed functions and positive-domain symbolic equivalents, then saves native-grader input. The initial audit parser did not simplify sqrt(u^3) versus u^(3/2); verify_saved.py explicitly corrects that review-tool limitation without changing package outputs.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json`
- `python -B shortcut_probe.py CANDIDATE_RECORDS.json` fails with exit 1 when the option-spacing cue succeeds. Used with independent-samples.json, batch-records.json, delivery-independent/accepted.json and delivery-batch/accepted.json.
- `python -B inventory_probe.py` reproduces affected stored IDs and complete normalized content.
- `python -B summarize_evidence.py` saves coverage, counterfactual, delivery-selection and pedagogical reports.

Shared delivery commands (no writes to database):

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

Repeat with `--input independent-easy.json --output delivery-independent`.

Actual renderer commands:

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-extra-records.json --output render-extra --limit 9 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

Default first render handles six records; second handles the remaining nine. Screenshot inspection is recorded in visual-inspection.json.

No repair_history_file, repair_preflight_file, previous_review or publication preparation existed for this captured job; this was an initial independent review.
