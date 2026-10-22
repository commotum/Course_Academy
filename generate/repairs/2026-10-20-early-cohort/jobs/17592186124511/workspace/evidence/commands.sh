#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
task_python=/home/jake/Developer/Course_Academy/.venv/bin/python
task_repo=/home/jake/Developer/Course_Academy
task_source=../source/source.json
task_inventory=../source/inventory.json
"$task_python" checks/check_runtime.py
"$task_python" checks/check_content.py
"$task_python" checks/check_batch.py
"$task_python" checks/check_boundaries.py
"$task_repo/generate/runs/current/check-engine" evidence/native-input.json evidence/native-report.json
"$task_python" "$task_repo/generate/pipeline/check_delivery.py" --input evidence/probe-records.json --source "$task_source" --inventory "$task_inventory" --difficulty moderate --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$task_python" checks/check_content.py --accepted evidence/delivery/accepted.json
"$task_python" "$task_repo/generate/pipeline/check_delivery.py" --input evidence/counterfactual-records.json --source "$task_source" --inventory "$task_inventory" --difficulty moderate --output evidence/counterfactual-delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$task_python" checks/check_delivery_paths.py
"$task_repo/generate/runs/current/check-engine" evidence/postdelivery-native-input.json evidence/postdelivery-native-report.json
"$task_python" "$task_repo/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
