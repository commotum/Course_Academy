#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
REVIEW_REPO=/home/jake/Developer/Course_Academy
REVIEW_PYTHON="$REVIEW_REPO/.venv/bin/python"
REVIEW_JOB="$REVIEW_REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186147456"
"$REVIEW_PYTHON" -B review.py > review-run.log 2>&1
"$REVIEW_PYTHON" -B package-review.py > packaging-run.log 2>&1
"$REVIEW_PYTHON" -B finish-checks.py > finish-checks-run.log 2>&1
"$REVIEW_REPO/generate/runs/current/check-engine" native-input.json native-report.json > native-run.log 2>&1
"$REVIEW_PYTHON" -B - <<'PY'
import json,pathlib
E=pathlib.Path('.')
rs=json.load(open('samples.json'))+json.load(open('normal-samples.json'))
for level in ['easy','moderate']:
 (E/f'delivery-input-{level}.json').write_text(json.dumps([r for r in rs if r['question'][':question/difficulty']==':question.difficulty/'+level],indent=2)+'\n')
p=json.load(open('counterfactual-records.json'));b=json.load(open('batch.json'))
(E/'render-records.json').write_text(json.dumps(p[:3]+p[-3:]+b[:2],indent=2)+'\n')
PY
for REVIEW_KIND in easy moderate batch; do
 REVIEW_INPUT="delivery-input-$REVIEW_KIND.json"
 REVIEW_DIFFICULTY="$REVIEW_KIND"
 if [ "$REVIEW_KIND" = batch ]; then REVIEW_INPUT=batch.json; REVIEW_DIFFICULTY=easy; fi
 "$REVIEW_PYTHON" -B "$REVIEW_REPO/generate/pipeline/check_delivery.py" --input "$REVIEW_INPUT" --source "$REVIEW_JOB/source/source.json" --inventory "$REVIEW_JOB/source/inventory.json" --difficulty "$REVIEW_DIFFICULTY" --output "delivery-$REVIEW_KIND" --asset-root . --math-root /media/jake/SSD/EDB/math > "delivery-$REVIEW_KIND-run.log" 2>&1
done
"$REVIEW_PYTHON" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --asset-root . --math-root /media/jake/SSD/EDB/math --limit 6 > render-run.log 2>&1
"$REVIEW_PYTHON" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" --input delivery-batch/accepted.json --output render-batch --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math --limit 5 > render-batch-run.log 2>&1
# Inspect screenshots as described in render-inspection.json; a successful renderer alone is insufficient.
"$REVIEW_PYTHON" -B variation-review.py > variation-run.log 2>&1
"$REVIEW_PYTHON" -B make-report.py
python3 -B validate-contract.py
