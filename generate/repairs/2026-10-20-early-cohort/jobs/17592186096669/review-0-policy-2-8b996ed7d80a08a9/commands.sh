#!/bin/bash
set -eu
cd "$(dirname "$0")"
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
PYTHONDONTWRITEBYTECODE=1 "$PY" review.py > review-run.log
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-samples --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$PY" probe_shortcuts.py
"$REPO/generate/runs/current/check-engine" all-grader-input.json all-grader-report.json
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --limit 6 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-delivered-pairs.json --output render-delivered-pairs --limit 7 --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math
# Expected failure demonstrating the current construction defect:
"$PY" probe_shortcuts.py --strict > strict-shortcut.log 2>&1
