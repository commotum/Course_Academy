All commands run from this evidence directory. PY=/home/jake/Developer/Course_Academy/.venv/bin/python; REPO=/home/jake/Developer/Course_Academy; JOB is this directory's parent. No package or DB writes.

- `$PY -B retained_checks.py` (author regression copied with output/workspace paths redirected; retained-check-output.txt)
- `$PY -B audit.py` (fresh seeds2026102107/2026102173; original counterexample913771 and batch4221100018; source banks, exact arithmetic, fixed-bank pairs, relocation/resampling)
- `$REPO/generate/runs/current/check-engine grader-cases.json grader-results.json`
- `$PY -B $REPO/generate/pipeline/check_delivery.py --input batch.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math`
- Same delivery command with `fresh-easy.json` / `delivery-fresh`, and `delivery-boundary-records.json` / `delivery-boundaries`.
- `$PY -B $REPO/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math` (default first6)
- Same renderer with `render-extra-records.json` / `render-extra` (remaining6).
- `$PY -B post_audit.py` (conditional probes, historical inventory reconstruction and selection simulation; rerun after UI outputs exist)
- `$PY -B strict_regressions.py historical` expected exit1, current expected exit0; results saved in strict-regression-results.json.
- `$PY -B finish_report.py` (final vector verification, schema-shaped report and package hashes).
- `python3 validate_evidence.py` (independent contract validation).
