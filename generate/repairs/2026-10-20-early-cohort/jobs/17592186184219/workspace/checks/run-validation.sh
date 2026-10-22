#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TASK_REPO=/home/jake/Developer/Course_Academy
TASK_PY="$TASK_REPO/.venv/bin/python"
TASK_JOB="$(dirname "$PWD")"
"$TASK_PY" -B checks/regressions.py > evidence/repair-regressions.txt 2>&1
"$TASK_PY" -B checks/validate.py prepare
for task_kind in controls batch small; do
  task_input="evidence/$task_kind.json"
  if [ "$task_kind" = small ]; then task_input=evidence/small-sample.json; fi
  "$TASK_PY" "$TASK_REPO/generate/pipeline/check_delivery.py" \
    --input "$task_input" --source "$TASK_JOB/source/source.json" \
    --inventory "$TASK_JOB/source/inventory.json" --difficulty easy \
    --output "evidence/delivery-$task_kind" --asset-root evidence/assets \
    --math-root /media/jake/SSD/EDB/math > "evidence/delivery-$task_kind-stdout.txt" 2>&1
done
"$TASK_PY" -B checks/validate.py finish
"$TASK_PY" -B checks/selection.py
"$TASK_REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json > evidence/grader-stdout.txt 2>&1
"$TASK_PY" "$TASK_REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json \
  --output evidence/render --asset-root evidence/delivery-batch/assets \
  --math-root /media/jake/SSD/EDB/math > evidence/render-stdout.txt 2>&1
