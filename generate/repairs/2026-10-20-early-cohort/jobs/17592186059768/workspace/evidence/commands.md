All commands run from workspace. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python`, `REPO=/home/jake/Developer/Course_Academy`, and `JOB` is the supplied job directory (workspace's parent). All output paths below are relative to workspace.

Initial reproduction before edits: import the existing entrypoint and call `generate('easy',941713401,profile='q-71722',parameters={'2':2,'3':4})`; save output to evidence/before-minimal.json. Its sole negative corner selects the key. `generate('moderate',941713201,template='q-1068')` raised the reported ValueError. Details: before-failure-results.json.

```sh
$PY -B checks/regression.py
$PY -B 17592186059768.py --difficulty easy --seed 941713401 --count 5 --format json > evidence/batch.json
$PY -B checks/finish.py
$REPO/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/easy.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/moderate.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty moderate --output evidence/delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/batch.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B checks/post_delivery.py
$REPO/generate/runs/current/check-engine evidence/boundary-grader-input.json evidence/boundary-grader-results.json
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/duplicate-input.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output evidence/delivery-duplicates --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-input.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-remaining.json --output evidence/render-remaining --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B checks/relocation.py
```

The renderer's default limit is six; render-remaining.json contains the last six records of render-input.json, so no first-half rerender was needed. Eight representative PNGs were inspected with view_image; exact list in visual-inspection.json.

Final affected checks: regression.py rerun after changing its source-fidelity oracle to the supplied independent source file; relocation.py rerun after a documentation-only generator-header clarification. No behavior changed after native grading or rendering.
