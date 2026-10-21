#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TASK_PY=/home/jake/Developer/Course_Academy/.venv/bin/python
TASK_REPO=/home/jake/Developer/Course_Academy
export PYTHONDONTWRITEBYTECODE=1
"$TASK_PY" checks/repair_checks.py
"$TASK_PY" checks/validate.py
"$TASK_PY" "$TASK_REPO/generate/pipeline/check_delivery.py" --input evidence/control-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-controls --asset-root . --math-root /media/jake/SSD/EDB/math
"$TASK_PY" checks/probes.py
"$TASK_REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$TASK_PY" "$TASK_REPO/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render --asset-root evidence/delivery/assets --math-root /media/jake/SSD/EDB/math
