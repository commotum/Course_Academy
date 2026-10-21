Run from the supplied workspace. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python` and `R=/home/jake/Developer/Course_Academy` below are abbreviations for the actual absolute commands run. All commands are offline/read-only except workspace evidence writes.

```sh
$PY checks/reproduce_before.py
$PY checks/regressions.py
$R/generate/runs/current/check-engine evidence/grader-cases.json evidence/grader-results.json
$PY $R/generate/pipeline/check_delivery.py --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $R/generate/pipeline/check_delivery.py --input evidence/fresh-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-fresh --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $R/generate/pipeline/check_delivery.py --input evidence/counterfactual-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-counterfactual --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY checks/post_delivery.py
$PY checks/inventory.py
$PY checks/packaging.py
$PY $R/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

`counterfactual-easy.json` is the first 24 records of counterfactual-records.json, excluding each sixth scale-only control (20 easy records). Runtime CLI example: `$PY generator.py --difficulty easy --count 5 --seed 4221100018 --format json`. It returns the same records saved in evidence/batch.json.

Results: original failures reproduced before edits and again against the saved snapshot. Current retained regressions pass both finding IDs; replay 16/16 banks, 80/80 choices; independent RREF, substitution and displayed operation checks 103/103 records. Native grader: 103 accepted and 412 rejected, zero mismatches. Delivery: 5/5 reported-seed batch, 24/24 fresh, 20/20 controlled. Sign-only unique selection: zero successes on every repaired tested set before and after filtering. Controlled fixed banks admit each of five correct members for each of four profiles, both bands (40 records), plus eight irrelevant scaling controls. The 20 easy decision controls remain selectable after filtering. Packaging relocation, deterministic CLI, bounded duplicate rejection, invalid requests and runtime dependency checks pass under Python 3.13.5.

Actual Learning.html/learning.js renderer passed all five records. Visually inspected question-001.png, question-003.png, question-004.png and question-005.png: equations, complete banks, radio controls, negative coefficients, fractions, augmentation dividers and moderate free-variable vectors are legible; no clipping or overlap observed. The restored source visibly subtracts 16R1. Controlled first/last members visibly change equations, final matrix, key and solution together.

Inventory: five non-source captured records independently reconstructed with stable publication IDs, complete prompt/bank/key matching, and all demonstrate the old sign-only shortcut. The saved records retain complete captured solutions. Original generation seed/draw/version was not captured; explicit inferred reconstruction parameters are disclosed. No historical seed provenance is claimed. affected-inventory.json uses ../workspace/generated-records.json relative to the job's supplied author-1 evidence_root, since workspace-only writes are required.

Learner selection: engine/rust/question_selection.rs was read. Positively weighted all-easy candidates are uniform within band; the test reproduces 25 seeded draws using UUID order as a permutation. Entity order, live weights, history and current-prefix exclusions are unavailable. The sign ambiguity is within every surviving question, so it does not depend on pool ordering. Unconfigured policies select the first eligible entity; zero easy weight excludes this pool. No live service, database write, image publication or other job edit occurred.
