# Reproduction and validation commands

Run from the workspace with `PY=/home/jake/Developer/Course_Academy/.venv/bin/python` and `REPO=/home/jake/Developer/Course_Academy`.

```sh
$PY 17592186119847.py --difficulty easy --count 13 --seed 0 --format json
```

Before: exit 0 and 12 records (`before-count.json`). After: exit 2, explicitly reports 12 distinct semantic tasks, no partial JSON (`count-regression.json`). The feedback supplies no exact seed or count; this is the minimal oversized easy request.

```sh
$PY check_repair.py
$REPO/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/easy-delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/moderate-delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY check_variation.py
$REPO/generate/runs/current/check-engine evidence/delivery-grader-input.json evidence/delivery-grader-report.json
$PY check_inventory.py
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/delivery-easy/assets --asset-root evidence/delivery-moderate/assets --math-root /media/jake/SSD/EDB/math
$PY 17592186119847.py --difficulty easy --count 5 --seed 0 --format json > evidence/sample-output.json
```

`requested-five.json` is the `instances` array from sample-output.json. `easy-delivery-input.json` and `moderate-delivery-input.json` partition probe-records.json by difficulty.

```sh
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/requested-five.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-requested-five --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Results: 11 source banks, all 55 choices matched; 10 exact existing source solutions plus one independently repaired absent source key/solution. Full returned finite batches independently checked: 12 easy + 91 moderate distinct mathematical tasks. Requested-five delivery: 5 input, 5 accepted, 0 duplicates. Probe delivery: 200/200 easy and 209/240 moderate retained; all 11 profiles retain variable answer position and numerical rank order. Native grader: 30 accepted, 120 rejected, zero mismatches/unresolved across pre/post delivery cases. Relocation with only the three manifest files passes. Four actual UI screenshots passed DOM checks and were visually inspected: no clipping, broken glyphs, malformed TeX, or missing solution content.

History has no numbered findings (`findings: []`), only one event with reason code `legacy_packaging_or_sampling`. repair-regressions.json uses that retained code as its identifier and runs check_repair.py. It actually invokes the current CLI and independently reads visible records, including the original oversized counterexample, full capacities, negative requests, replay, controlled evidence changes and bank-cue checks. No unconditional success or copied expected record is used.

Inventory: all 13 captured records inspected; 11 are originals, two generated records replay exactly with the archived generator and seeds. One generated q-79405 instance has the demonstrated second-smallest-option invariant. affected-inventory.json's evidence_path is relative to the supplied evidence_root (`author-1`), pointing back into this workspace; this respects workspace-only writes. Source originals are not marked generated. Sampling truncation has no individual-record manifestation. No database or service operations occurred.

The random probes covered rows 4..15; explicit independently checked/native-graded row=3 boundary records for both bands are saved in boundary-records.json. Combined with probes they exercise every permitted row dimension. The source and prompt dimensions never require a diagram.
