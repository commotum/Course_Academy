#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
REPO=/home/jake/Developer/Course_Academy
REVIEW_PY="$REPO/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PWD/tmp"
export COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/assets"
mkdir -p "$TMPDIR" "$COURSE_ACADEMY_GENERATOR_OUTPUT_DIR"
# Source analysis and copied-script provenance are retained in source-analysis.json
# and provenance.json. All executable review outputs stay in this directory.
"$REVIEW_PY" audit.py
"$REVIEW_PY" boundary_review.py
"$REVIEW_PY" runtime_review.py
"$REVIEW_PY" author-current/checks/check_repairs.py source
"$REVIEW_PY" author-current/checks/check_repairs.py batch
for stage in samples runner-batch counterfactual-records; do
  case "$stage" in
    samples) output=delivery-samples ;;
    runner-batch) output=delivery-batch ;;
    counterfactual-records) output=delivery-counterfactual ;;
  esac
  "$REVIEW_PY" "$REPO/generate/pipeline/check_delivery.py" --input "$stage.json" --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output "$output" --asset-root assets --math-root /media/jake/SSD/EDB/math
done
"$REPO/generate/runs/current/check-engine" native-input.json native-report.json
"$REVIEW_PY" targeted_tests.py
"$REVIEW_PY" "$REPO/generate/pipeline/check_delivery.py" --input sampling-cycle.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery-cycle --asset-root assets --math-root /media/jake/SSD/EDB/math
"$REPO/generate/runs/current/check-engine" postdelivery-native-input.json postdelivery-native-report.json
# render-records.json is retained: 5 current batch + 6 controlled + 2 restored.
"$REVIEW_PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math --limit 13
"$REVIEW_PY" finish_review.py
python3 validate_evidence.py
