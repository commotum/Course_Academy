#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
py=/home/jake/Developer/Course_Academy/.venv/bin/python
repo=/home/jake/Developer/Course_Academy
"$py" -B checks/repair.py
"$py" -B checks/source_package_inventory.py
"$py" -B checks/reproduce_number_match.py --output after-number-match.json
for pair in 'fresh-records.json delivery' 'regression-records.json delivery-regressions' 'batch.json delivery-batch'; do
  read -r input output <<< "$pair"
  "$py" -B "$repo/generate/pipeline/check_delivery.py" --input "evidence/$input" --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output "evidence/$output" --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
  "$py" -B checks/repair.py --records "evidence/$output/accepted.json" --output "$output-variation.json"
done
"$py" -B checks/reproduce_number_match.py --input delivery-batch/accepted.json --output delivered-number-match.json
"$repo/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$py" -B checks/batch_checks.py
"$py" -B "$repo/generate/pipeline/check_delivery.py" --input evidence/normal-coverage-witness.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-coverage --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$py" -B checks/repair.py --records evidence/delivery-coverage/accepted.json --output filtered-coverage-variation.json
"$repo/generate/runs/current/check-engine" evidence/batch-grader-input.json evidence/batch-grader-results.json
"$py" -B checks/reproduce_shortcut.py --input evidence/regression-records.json --index 0 --output evidence/after-shortcut.json
python3 "$repo/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
