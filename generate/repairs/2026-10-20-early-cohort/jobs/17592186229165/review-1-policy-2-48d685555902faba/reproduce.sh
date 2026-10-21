#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
repo=/home/jake/Developer/Course_Academy
job="$repo/generate/repairs/2026-10-20-early-cohort/jobs/17592186229165"
py="$repo/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$py" audit.py > audit.log 2>&1
"$py" targeted.py > targeted.log 2>&1
"$py" package_checks.py > package-checks.log 2>&1
"$py" test_role_exchange.py > independent-role-test.log 2>&1
if "$py" "$job/workspace/checks/test_role_exchange.py" --entry "$job/workspace/evidence/generator-before.py" --output "$PWD/retained-before" > retained-before.log 2>&1; then
  echo 'Prior counterexample unexpectedly passed' >&2
  exit 1
fi
"$py" "$job/workspace/checks/test_role_exchange.py" --output "$PWD/retained-current" > retained-current.log 2>&1
for case in batch independent hard stored; do
  case "$case" in
    batch) input=runner-batch.json; difficulty=easy;;
    independent) input=independent-easy.json; difficulty=easy;;
    hard) input=hard-samples.json; difficulty=hard;;
    stored) input=generated-records.json; difficulty=hard;;
  esac
  "$py" "$repo/generate/pipeline/check_delivery.py" --input "$input" --source "$job/source/source.json" --inventory "$job/source/inventory.json" --difficulty "$difficulty" --output "delivery-$case" --asset-root . --math-root /media/jake/SSD/EDB/math > "delivery-$case.log" 2>&1
done
"$py" variation.py > variation.log 2>&1
"$repo/generate/runs/current/check-engine" grader-input.json grader-report.json > grader.log 2>&1
"$py" verify_delivery_and_scroll.py > delivery-scroll.log 2>&1
"$repo/generate/runs/current/check-engine" grader-delivered-input.json grader-delivered-report.json > grader-delivered.log 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input render-records.json --output render --limit 13 --asset-root . --math-root /media/jake/SSD/EDB/math > render.log 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input render-regression-records.json --output render-regression --limit 2 --asset-root . --math-root /media/jake/SSD/EDB/math > render-regression.log 2>&1
# Screenshots require human inspection; observations are retained in render-inspection.json.
python3 finish_report.py
