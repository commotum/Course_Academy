#!/usr/bin/env bash
# Current review repair checks; all outputs remain in this workspace.
set -euo pipefail
cd "$(dirname "$0")"
repo=/home/jake/Developer/Course_Academy
job_python="$repo/.venv/bin/python"
evidence=evidence/repair-3
"$job_python" repair_checks.py build
"$job_python" generator.py --difficulty easy --count 5 --seed 1033798965 --format json > "$evidence/runner-sample.json"
for target in test counterfactual bank-counterfactual runner
 do
  input="$evidence/$target-records.json"
  output="$evidence/$target-delivery"
  if [ "$target" = test ]; then output="$evidence/delivery"; fi
  if [ "$target" = runner ]; then input="$evidence/runner-sample.json"; fi
  "$job_python" "$repo/generate/pipeline/check_delivery.py" --input "$input" --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output "$output" --asset-root "$evidence/assets" --math-root /media/jake/SSD/EDB/math
 done
"$job_python" repair_checks.py delivered
COURSE_ACADEMY_VALIDATION_EVIDENCE_DIR="$evidence" "$job_python" finish_checks.py
for target in native-grader delivered-native-grader counterfactual-native-grader
 do
  "$repo/generate/runs/current/check-engine" "$evidence/$target-input.json" "$evidence/$target.json"
 done
"$job_python" "$repo/generate/pipeline/render_preview.py" --input "$evidence/render-records.json" --output "$evidence/render" --asset-root "$evidence/assets" --math-root /media/jake/SSD/EDB/math --limit 9
# Visually inspect all nine screenshots after this command.
