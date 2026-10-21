# Reproduction and validation commands

Run from the supplied workspace. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python` and `REPO=/home/jake/Developer/Course_Academy` below are abbreviations only; no installation or publication was performed.

```sh
$PY -B reproduce_original.py
```

Exit 1, expected: both missing source-bank profiles raise ValueError; exact hard seeds 72011–72070 exhibit only one destination. This uses the unchanged original package copied from the supplied review's relocated package into evidence/original-package. Result: ../reproduction-before.json relative to this file.

```sh
$PY -B reproduce_review.py
$PY -B regressions.py
```

Both exit 0. Exact review counterexamples pass. Regressions cover both retained finding IDs, all eleven complete source banks, the canonical example without an invented answer bank, 127 independent visible-record arithmetic checks, hard intermediate matrices, both role relationships over the exact review seeds, all six row assignments per hard relationship, controlled factor changes, commuting-operation and letter invariance, legacy API compatibility, explicit operations overriding legacy row fields, and invalid operation rejection. Results: regression-results.json, math-results.json, source-replays.json, control-records.json, and ../reproduction-after.json.

```sh
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/easy-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/hard-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty hard --output evidence/delivery-hard --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B audit_delivery.py
```

Exit 0. Shared publication preparation accepts 23/23 easy records and 84/87 hard records, skipping three duplicates. All tested profiles and both hard role relationships survive. Each hard family retains all five different keys over a fixed input matrix and answer bank. Within-profile shortcut probes run before and after filtering. Captured selection and inventory limits are recorded; there are no demonstrated affected stored instances, and sixteen records without generation metadata remain unverified. Audit also checks exact Python 3.13.5, declared files, seeded CLI determinism and relocation for normal easy/hard generation and both new replay profiles. Reports: shortcut-results.json, inventory-inspection.json, selection-results.json, packaging-results.json and ../affected-inventory.json.

```sh
$REPO/generate/runs/current/check-engine evidence/combined-grader-input.json evidence/combined-grader-results.json
```

Exit 0: 60 correct-choice acceptances, 240 wrong-choice rejections, zero unexpected or unresolved outcomes. Includes all source banks and controlled tasks before delivery, then the ten fixed-bank hard controls and five-item easy batch after delivery. Outcomes are computed independently from visible prompt operations, not copied keys.

```sh
$PY -B $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/render_preview.py --input evidence/render-shared-donor.json --output evidence/render-shared-donor --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Exit 0. Both new source replays and both hard relationships use the unmodified application UI. Screenshots were opened with view_image. The initial fourth capture was incomplete despite a successful DOM report, so only that case was recaptured and inspected; the final screenshot is complete. See visual-inspection.json for the four inspected screenshot paths.

Runtime changes are recorded in changes.diff. Final runtime/input hashes and separate fidelity, correctness, grading, variation, packaging and rendering claims are in validation-summary.json. All edits and outputs are in this workspace; no database or published image writes were made.
