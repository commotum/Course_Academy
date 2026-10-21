#!/usr/bin/env bash
set -euo pipefail
repo_root="$1"
source_file="$2"
inventory_file="$3"
python_bin="$repo_root/.venv/bin/python"
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
"$python_bin" validate.py --source "$source_file"
for sample in test normal; do
  destination=evidence/delivery
  if [ "$sample" = normal ]; then destination=evidence/delivery-normal; fi
  "$python_bin" "$repo_root/generate/pipeline/check_delivery.py" \
    --input "evidence/$sample-records.json" --source "$source_file" --inventory "$inventory_file" \
    --difficulty moderate --output "$destination" --asset-root evidence --math-root /media/jake/SSD/EDB/math
done
"$python_bin" validate.py --after-delivery evidence/delivery/accepted.json --normal-accepted evidence/delivery-normal/accepted.json
"$python_bin" repair_checks.py
"$repo_root/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$repo_root/generate/runs/current/check-engine" evidence/filtered-grader-input.json evidence/filtered-grader-report.json
"$repo_root/generate/runs/current/check-engine" evidence/shortcut-grader-input.json evidence/shortcut-grader-report.json
"$python_bin" verify_package.py
"$python_bin" generator.py --difficulty moderate --count 5 --seed 20261020 --format json > evidence/runner-sample.json
python3 "$repo_root/generate/pipeline/render_preview.py" --limit 7 --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
