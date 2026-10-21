#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
JOB_PYTHON=/home/jake/Developer/Course_Academy/.venv/bin/python
GENERATOR_REPO=/home/jake/Developer/Course_Academy
export PYTHONDONTWRITEBYTECODE=1
export COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/assets"
"$JOB_PYTHON" -B checks/fraction_shortcut.py
"$JOB_PYTHON" -B checks/validate_repair.py
"$JOB_PYTHON" -B checks/rational_support.py
"$JOB_PYTHON" -B checks/role_counterfactuals.py
"$JOB_PYTHON" -B checks/solution_steps.py
"$JOB_PYTHON" -B checks/coverage.py
"$JOB_PYTHON" -B checks/packaging.py
for DELIVERY_GROUP in rational fresh batch controlled; do
 case "$DELIVERY_GROUP" in
  rational) DELIVERY_INPUT=evidence/rational-records.json ;;
  fresh) DELIVERY_INPUT=evidence/fresh.json ;;
  batch) DELIVERY_INPUT=evidence/samples.json ;;
  controlled) DELIVERY_INPUT=evidence/controlled-records.json ;;
 esac
 "$JOB_PYTHON" -B "$GENERATOR_REPO/generate/pipeline/check_delivery.py" --input "$DELIVERY_INPUT" --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output "evidence/delivery-$DELIVERY_GROUP" --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
done
"$JOB_PYTHON" -B checks/rational_support.py evidence/delivery-rational/accepted.json
"$JOB_PYTHON" -B checks/post_delivery.py
"$JOB_PYTHON" -B checks/delivery_controlled.py
"$JOB_PYTHON" -B checks/batch_grading.py
"$GENERATOR_REPO/generate/runs/current/check-engine" evidence/repair2-grader-input.json evidence/repair2-grader-results.json
"$JOB_PYTHON" -B "$GENERATOR_REPO/generate/pipeline/render_preview.py" --input evidence/rational-render-records.json --output evidence/render-rational --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
