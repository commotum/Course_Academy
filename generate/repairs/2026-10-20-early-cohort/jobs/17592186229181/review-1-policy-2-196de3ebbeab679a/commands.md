All commands run from this evidence_root. Only evidence_root receives writes. Python bytecode writes are disabled in review import scripts.

```sh
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
$PY prepare_review.py
$PY acceptance_regressions.py > acceptance-current.txt
cp acceptance-regressions.json acceptance-current.json
$PY acceptance_regressions.py negative-fixture > acceptance-negative.txt
# Expected exit 1: original bank shortcut, missing attributes and three missing profiles.
cp acceptance-regressions.json acceptance-negative.json
$PY author-check/validate_repair.py > author-check/stdout.txt
$PY independent_checks.py
$PY "$REPO/generate/pipeline/check_delivery.py" --input easy-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --math-root /media/jake/SSD/EDB/math
$PY "$REPO/generate/pipeline/check_delivery.py" --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
$PY "$REPO/generate/pipeline/check_delivery.py" --input counterfactual-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-counterfactual --math-root /media/jake/SSD/EDB/math
$PY delivery_checks.py > delivery-checks-output.json
"$REPO/generate/runs/current/check-engine" grader-input.json grader-report.json
$PY "$REPO/generate/pipeline/render_preview.py" --input render-input.json --output render-all --math-root /media/jake/SSD/EDB/math --limit 12
node ui_order_check.cjs
PYTHONDONTWRITEBYTECODE=1 $PY relocated/17592186229181.py --difficulty easy --seed 519401 --count 2 --format json > cli-samples.json
$PY finish_report.py
```

The copied author preflight uses the same test body and candidate path; output paths were redirected into author-check. Original independent regression scripts come from the prior review with unchanged source binding. Negative-fixture is the prior review's retained executable snapshot, not a mutation of the current generator. Earlier source-math evidence is reused with provenance. Screenshot inspection is recorded in render-inspection.json.
