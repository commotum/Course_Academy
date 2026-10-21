Run from the supplied workspace; all outputs remain here. CA_PY is the supplied Python executable; CA_REPO is the supplied read-only repository.

```bash
CA_PY=/home/jake/Developer/Course_Academy/.venv/bin/python
CA_REPO=/home/jake/Developer/Course_Academy
$CA_PY validate.py
$CA_PY check_source_fidelity.py
$CA_PY check_equivalent_responses.py
$CA_REPO/generate/runs/current/check-engine evidence/engine-input.json evidence/engine-report.json
$CA_PY check_review_repairs.py
$CA_REPO/generate/runs/current/check-engine evidence/author-2/linear-grader-input.json evidence/author-2/linear-grader-report.json
$CA_PY $CA_REPO/generate/pipeline/check_delivery.py --input evidence/test-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$CA_PY audit_variation.py
$CA_REPO/generate/runs/current/check-engine evidence/counterfactual-engine-input.json evidence/counterfactual-engine-report.json
$CA_PY $CA_REPO/generate/pipeline/check_delivery.py --input evidence/author-2/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/author-2/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$CA_PY audit_review_variation.py
$CA_PY check_relocation.py
$CA_PY $CA_REPO/generate/pipeline/check_delivery.py --input evidence/runner-five.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/runner-delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
python3 $CA_REPO/generate/pipeline/render_preview.py --input evidence/author-2/render-records.json --output evidence/author-2/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

The following required test FAILS (exit 1); it is intentionally retained as expected accepted:

```bash
$CA_REPO/generate/runs/current/check-engine evidence/author-2/log-required-input.json evidence/author-2/log-required-report.json
```

check_review_repairs.py captures that failure and then runs a diagnostic batch with expected unresolved solely to observe both input notations and reversed-key behavior. Its own exit 0 means the investigation ran; repair-summary.json explicitly records required acceptance false and delivery status unsupported. No successful mandatory grading report is created for the failed log test.

Results:
- Fidelity: all 11 original questions, 102 math fragments, all 30 bank values pass. Canonical e-3634 now generates x cos x and cos x - x sin x using an explicitly authored q-1907 radio response design; historical answer fields are absent.
- Correctness: 75 regression/probe records, 12 controlled pairs; degree-1 boundary now included in each polynomial profile. Targeted checks add 32 boundary/presentation records and 27 fixed-data degree counterfactual pairs. Sampled degree 1 is reachable in all four public polynomial profiles. Degrees 0 and 5 reject.
- Grading: regression has 201 accepted and 342 rejected; targeted degree cases have 59 accepted and 200 rejected; missing-target stale keys reject 10/10. Separately, mandatory base-4 equivalence fails. Diagnostic: canonical accepted, two valid alternative spellings unresolved, original value unresolved with expanded key. These are a blocking failure, not passing equivalence coverage.
- Variation: regression delivery retains 70/75 and 58 semantic instances. Focused delivery retains 31/33, all 16 semantic instances, both completion roles and each allowed trig assignment. New degree-1 within-template/trig position and length/minus probes find no perfect tested predictor; finite sample limits remain. The grading failure itself survives filtering.
- Rendering: five actual UI screenshots covering canonical and other linear banks plus both completion roles passed renderer checks and were visually inspected. Readable math, distinct controls, correct displayed solutions, no clipping observed at the tested desktop viewport.
- Relocation: five deterministic easy records, declared files only, no writes; all five survive runner delivery. Manifest versions match supplied interpreter.

No database writes, publication, image upload or edits to another job. Native grader was inspected read-only and remains unchanged. Delivery is unsupported until the required equivalent answer can be graded successfully; no request to expand authorization was made.
