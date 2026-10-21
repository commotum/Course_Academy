#!/usr/bin/env bash
set -euo pipefail
repo_root="$1"
python_bin="$repo_root/.venv/bin/python"
"$python_bin" repair_checks.py
"$repo_root/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$repo_root/generate/runs/current/check-engine" evidence/filtered-grader-input.json evidence/filtered-grader-report.json
"$repo_root/generate/runs/current/check-engine" evidence/shortcut-grader-input.json evidence/shortcut-grader-report.json
"$python_bin" verify_package.py
"$python_bin" generator.py --difficulty moderate --count 5 --seed 20261020 --format json > evidence/runner-sample.json
python3 "$repo_root/generate/pipeline/render_preview.py" --limit 7 --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
