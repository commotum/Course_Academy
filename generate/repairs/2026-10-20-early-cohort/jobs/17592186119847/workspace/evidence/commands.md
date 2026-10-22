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

History has no numbered findings (`findings: []`), and two count-feedback events; the initial event supplies reason code `legacy_packaging_or_sampling`. repair-regressions.json uses that retained code as its identifier and runs check_repair.py. It actually invokes the current CLI and independently reads visible records, including the original oversized counterexample, full capacities, negative requests, replay, controlled evidence changes and bank-cue checks. No unconditional success or copied expected record is used.

Inventory: all 13 captured records inspected; 11 are originals, two generated records replay exactly with the archived generator and seeds. One generated q-79405 instance has the demonstrated second-smallest-option invariant. affected-inventory.json's evidence_path is relative to the supplied evidence_root (`author-2`), pointing back into this workspace; this respects workspace-only writes. Source originals are not marked generated. Sampling truncation has no individual-record manifestation. No database or service operations occurred.

The random probes covered rows 4..15; explicit independently checked/native-graded row=3 boundary records for both bands are saved in boundary-records.json. Combined with probes they exercise every permitted row dimension. The source and prompt dimensions never require a diagram.

## Resumed verification of the existing repaired candidate

Read both current feedback and history first. Reran the minimal oversized request before edits: exit 2, no stdout, explicit capacity 12. No current silent truncation was reproduced. Runtime files and manifest remain intact. The source evidence and repaired scope are unchanged.

Reran `check_repair.py`, the native source/control grader, `check_inventory.py`, and `check_variation.py` using the commands above. All pass. The regenerated raw probe records are deterministic; retained accepted probe records still cover all 11 profiles with variable positions and numerical order. Re-inspected existing `render/question-001.png` and `render/question-003.png`: visible prompts, choices and solutions have no clipping or malformed math. Existing four-case renderer evidence is retained because the runtime did not change.

Reran the exact five-record generation and requested-five delivery commands above: 5/5 accepted, zero duplicates. For a small fresh delivery regression, prepare the seven controlled records from the just-regenerated validation output:

```sh
$PY - <<'PY'
import json
from pathlib import Path
p = Path('evidence')
records = json.loads((p / 'validation-records.json').read_text())[11:18]
assert len(records) == 7
for level in ('easy', 'moderate'):
    group = [r for r in records if r['question'][':question/difficulty'].endswith('/' + level)]
    (p / f'continuation-controls-{level}.json').write_text(json.dumps(group, indent=2) + '\n')
PY
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/continuation-controls-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/continuation-delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/continuation-controls-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/continuation-delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY evidence/verify-continuation.py
```

Results: easy controls 3/3 and moderate controls 4/4 survive actual delivery; relevant count/column changes change rank, and irrelevant name/feasible-row changes preserve it. `verify-continuation.py` independently parses their visible records, replays them against the current generator, and tests every choice of those seven plus the exact requested five with the native grader: 12 accepted, 48 rejected, zero unresolved/mismatched. Runtime hashes, commands and results are in continuation-results.json. These are additional checks, separate from the earlier 30 accepted/120 rejected grader checks. No publication, database writes, or engine changes occurred.
