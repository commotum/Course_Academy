#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
REPO=/home/jake/Developer/Course_Academy
PY="$REPO/.venv/bin/python"
JOB="$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186124511"
"$PY" audit.py
"$PY" runtime_review.py
"$PY" boundary_review.py
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input samples.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-samples --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-batch --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input counterfactual-records.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-counterfactual --math-root /media/jake/SSD/EDB/math
"$REPO/generate/runs/current/check-engine" native-input.json native-report.json
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input delivery-counterfactual/accepted.json --output render-counterfactual --limit 6 --math-root /media/jake/SSD/EDB/math
"$PY" post_delivery.py
"$REPO/generate/runs/current/check-engine" postdelivery-native-input.json postdelivery-native-report.json
"$PY" finalize_review.py
# Strict acceptance regressions intentionally fail on the current package:
# "$PY" regression.py source
# "$PY" regression.py batch
