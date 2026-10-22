#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
REVIEW_PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REVIEW_REPO=/home/jake/Developer/Course_Academy
REVIEW_JOB=$(dirname "$PWD")
"$REVIEW_PY" -B review.py
"$REVIEW_REPO/generate/runs/current/check-engine" grader-input.json grader-report.json
for REVIEW_STAGE in independent batch; do
  REVIEW_INPUT=delivery-input.json
  if [ "$REVIEW_STAGE" = batch ]; then REVIEW_INPUT=batch-records.json; fi
  "$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/check_delivery.py" --input "$REVIEW_INPUT" --source "$REVIEW_JOB/source/source.json" --inventory "$REVIEW_JOB/source/inventory.json" --difficulty easy --output "delivery-$REVIEW_STAGE" --asset-root "$REVIEW_JOB/workspace" --math-root /media/jake/SSD/EDB/math
done
"$REVIEW_PY" -B decision_checks.py
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --limit 12 --asset-root "$REVIEW_JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" --input batch-records.json --output render-batch --limit 5 --asset-root "$REVIEW_JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" -B finish_review.py
