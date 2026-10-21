#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
JOB_PYTHON=/home/jake/Developer/Course_Academy/.venv/bin/python
GENERATOR_REPO=/home/jake/Developer/Course_Academy
JOB_SOURCE=../source/source.json
JOB_INVENTORY=../source/inventory.json
export PYTHONDONTWRITEBYTECODE=1
export COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/assets"
"$JOB_PYTHON" -B checks/reproduce.py evidence/after-failures.json > evidence/reproduction-output.txt
"$JOB_PYTHON" -B checks/inventory_reproduction.py
"$JOB_PYTHON" -B checks/validate_repair.py
"$JOB_PYTHON" -B checks/role_counterfactuals.py
"$JOB_PYTHON" -B checks/solution_steps.py
"$JOB_PYTHON" -B checks/coverage.py
"$JOB_PYTHON" -B checks/packaging.py
"$GENERATOR_REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$GENERATOR_REPO/generate/runs/current/check-engine" evidence/role-grader-input.json evidence/role-grader-results.json
for DELIVERY_GROUP in fresh batch controlled; do
  case "$DELIVERY_GROUP" in
    fresh) DELIVERY_INPUT=evidence/fresh.json ;;
    batch) DELIVERY_INPUT=evidence/samples.json ;;
    controlled) DELIVERY_INPUT=evidence/controlled-records.json ;;
  esac
  "$JOB_PYTHON" -B "$GENERATOR_REPO/generate/pipeline/check_delivery.py" --input "$DELIVERY_INPUT" --source "$JOB_SOURCE" --inventory "$JOB_INVENTORY" --difficulty easy --output "evidence/delivery-$DELIVERY_GROUP" --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
done
"$JOB_PYTHON" -B checks/post_delivery.py
"$JOB_PYTHON" -B checks/delivery_controlled.py
"$GENERATOR_REPO/generate/runs/current/check-engine" evidence/post-grader-input.json evidence/post-grader-results.json
"$GENERATOR_REPO/generate/runs/current/check-engine" evidence/controlled-grader-input.json evidence/controlled-grader-results.json
"$JOB_PYTHON" -B "$GENERATOR_REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render-final --limit 9 --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
