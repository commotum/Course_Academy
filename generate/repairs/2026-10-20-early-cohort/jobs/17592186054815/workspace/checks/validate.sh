#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
"$PYTHON" -B checks/repair_check.py
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$PYTHON" "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PYTHON" -B checks/finish_checks.py
"$PYTHON" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
