#!/usr/bin/env bash
# Run from this evidence directory; all writes stay here. No database operations.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119854
"$PY" prior-regressions.py
"$PY" audit.py
"$PY" author-check-current.py
if "$PY" author-check-historical.py > author-historical.stdout 2> author-historical.stderr; then exit 1; fi
"$PY" review_checks.py
"$REPO/generate/runs/current/check-engine" grader-input.json grader-results.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-batch --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input fresh-moderate.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-moderate --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input fresh-hard.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty hard --output delivery-hard --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-input.json --output render --limit 6 --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-more-input.json --output render-more --limit 8 --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" summarize.py
"$PY" finalize.py
