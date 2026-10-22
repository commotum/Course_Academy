#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=$(dirname "$PWD")
"$PY" -B check_restriction.py
"$PY" -B check_repair.py
"$PY" -B prepare_root_checks.py
for level in easy moderate; do
  "$PY" -B "$REPO/generate/pipeline/check_delivery.py" --input "evidence/root-cause/$level-delivery-input.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty "$level" --output "evidence/root-cause/delivery-$level" --math-root /media/jake/SSD/EDB/math
done
for profile in q-139950 q-34805 q-79157 q-79405 q-34825 q-34806 q-139953 q-34826 q-79408 q-79409 q-79407; do
  case "$profile" in
    q-139950|q-34805|q-79157|q-79405|q-34825) level=easy ;;
    *) level=moderate ;;
  esac
  "$PY" -B "$REPO/generate/pipeline/check_delivery.py" --input "evidence/root-cause/isolated-$profile.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty "$level" --output "evidence/root-cause/isolated-$profile" --math-root /media/jake/SSD/EDB/math
done
"$PY" -B check_post_delivery.py
"$REPO/generate/runs/current/check-engine" evidence/root-cause/grader-input.json evidence/root-cause/grader-report.json
"$PY" -B "$REPO/generate/pipeline/check_delivery.py" --input evidence/root-cause/requested-five.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/root-cause/delivery-requested-five --math-root /media/jake/SSD/EDB/math
"$PY" -B check_inventory.py
python3 "$REPO/generate/pipeline/render_preview.py" --input evidence/root-cause/render-records.json --output evidence/root-cause/render --math-root /media/jake/SSD/EDB/math
