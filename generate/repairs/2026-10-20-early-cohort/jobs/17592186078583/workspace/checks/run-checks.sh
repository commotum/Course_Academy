#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
repo=/home/jake/Developer/Course_Academy
py="$repo/.venv/bin/python"
mkdir -p evidence/assets
"$py" checks/repair_checks.py > evidence/regression-stdout.txt 2>&1
"$repo/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json > evidence/grader-stdout.txt 2>&1
for level in easy moderate; do
  "$py" "$repo/generate/pipeline/check_delivery.py" --input "evidence/samples-$level.json" --source ../source/source.json --inventory ../source/inventory.json --difficulty "$level" --output "evidence/delivery-$level" --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math > "evidence/delivery-$level-stdout.txt" 2>&1
done
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math > evidence/delivery-batch-stdout.txt 2>&1
"$py" checks/delivery_inventory_package.py > evidence/delivery-inventory-package-stdout.txt 2>&1
"$repo/generate/runs/current/check-engine" evidence/delivered-grader-input.json evidence/delivered-grader-report.json > evidence/delivered-grader-stdout.txt 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math > evidence/render-stdout.txt 2>&1
# Inspect all four question-00N.png screenshots after this command; rendering.json
# alone is not visual inspection. This driver repeats commands already run
# individually during the targeted repair; it is provided for reproducibility.
