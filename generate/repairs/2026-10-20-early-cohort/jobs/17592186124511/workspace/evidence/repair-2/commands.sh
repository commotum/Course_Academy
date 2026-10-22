#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
task_python=/home/jake/Developer/Course_Academy/.venv/bin/python
task_repo=/home/jake/Developer/Course_Academy
export PYTHONDONTWRITEBYTECODE=1
export COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/repair-2/assets"
"$task_python" checks/check_repairs.py source
"$task_python" checks/check_repairs.py batch
"$task_python" checks/check_repair_validation.py
"$task_python" checks/check_runtime.py
"$task_python" checks/check_batch.py
"$task_repo/generate/runs/current/check-engine" evidence/repair-2/native-input.json evidence/repair-2/native-report.json
"$task_python" "$task_repo/generate/pipeline/render_preview.py" --input evidence/repair-2/render-records.json --output evidence/repair-2/render --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math
