Commands were run from the supplied workspace. `PY` below denotes `/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO` denotes `/home/jake/Developer/Course_Academy`.

Initial exact reproduction (before repair):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B -c 'import generator; generator.generate(seed=0, profile="observed-q-139628")'
```

Exit 1: `ValueError: Unknown source profile`, raised by generator.py:103. The registry had eight source cases at basis 3966; the supplied capture has nine at basis 5665. No historical sample was edited.

After refreshing source-cases.json, adding the replay recipe, and implementing the Chelsea template:

```sh
$PY -B checks/replay_completeness.py > evidence/source-replay-results.json
$PY -B ../review-0-policy-2-8040d13f050e26af/replay_regression.py --package . > evidence/original-regression.log
COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/assets" $PY -B generator.py --difficulty easy --count 5 --seed 928264887 --format json > evidence/prospective-batch.json
$PY -B checks/validate_repair.py
$REPO/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/prospective-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-controls --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/render_preview.py --input evidence/render-input.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B checks/check_delivered.py
```

All commands passed. Replay: 9/9 complete sources, original reviewer counterexample passed. Independent visible-matrix math: 87 records. Native grading: 298 assertions, 163 accepted and 135 rejected, no unexpected outcomes. Delivery: 5/5 prospective records and 73/73 controls/sample records retained. Chelsea: all 25 ordered shapes remain after filtering. Both axes vary independently in all four templates; irrelevant entries and labels preserve answers. Runtime dependency versions match the manifest, and the current requested CLI output replays exactly after relocation with only declared files. No generated question assets are required.

Actual UI: six screenshots inspected (restored source, independent row and column controls, unchanged-shape control with radicals/fractions, representative radio). Text, matrix brackets/alignment, ordered blanks, five-choice bank and worked solutions are legible with no clipping or broken mathematics. See visual-inspection.json.

Stored pool: all 14 captured records have correct displayed dimensions, answers and solutions. The omitted source profile is a runtime registry defect; the original source is not a generated stored defect. affected-inventory.json is empty for this demonstrated finding. The capture cannot establish future learner-history selection or changes after basis 5665. No publication, database writes, engine edits, or changes outside the workspace occurred.
