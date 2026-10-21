#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
REPO=/home/jake/Developer/Course_Academy
JOB="$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186059772"
PY="$REPO/.venv/bin/python"
"$PY" audit.py
"$REPO/generate/runs/current/check-engine" grader-input.json grader-results.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input easy-samples.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output delivery-sample --math-root /media/jake/SSD/EDB/math
"$PY" delivery-analysis.py
"$PY" packaging-check.py
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render-all --limit 25 --math-root /media/jake/SSD/EDB/math
"$PY" finalize-evidence.py
# This is a strict acceptance regression and should exit 1 on this package.
"$PY" source-replay-regression.py
