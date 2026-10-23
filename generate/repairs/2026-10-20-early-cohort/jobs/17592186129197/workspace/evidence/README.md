# Repair evidence

The generator repair is complete for requested easy output. It preserves the eight normal families and their prior mathematical/plot repairs. The manifest contains only the entry point, historical source, current source and pinned requirements.

## Findings and outcomes

- `bfb40e768b17052babbc`: reproduced the seed 8191 simple a=1,h=1,k=0 failure before editing (before-shortcut.log and before-shortcut-record.json). Replaced the family-wide fixed method bank with five compatible instance areas followed by target selection. The original strict signed-pair regression passes. Each of eight families has a common-bank witness requiring all five different answers. Independent integration of printed maps/boundaries checks 67 records, their keys and final worked answers. This is 40 controlled target cases, 24 normal sampled cases and three explicit counterfactual cases; it is not a claim of 67 unique underlying tasks.
- `1ce536ab6304867dd083`: before-source-replay.json reproduces five unsupported current profiles and the obsolete extra q-82874 field. Current raw replay now matches all 12 supplied question contracts, including keys, complete banks, field ownership, available solutions and omissions. Historical replay separately preserves the two-field q-82874 record. These replay repairs do not claim five new generalized families.
- `2185805fc9fcc95ab6b5` (inventory): inventory-status.json inspects all 23 current records at basis 5602. All eleven previously demonstrated generated defects are now retired; the twelve remaining records are supplied source questions. No active generated inventory defects remain in this capture. affected-inventory.json is therefore empty. Historical evidence remains in the previous independent review. No database content was changed.

Fidelity, math, grading and decision variation are separate checks: source-replay.json establishes exact source contracts; math.json integrates visible prompts; native reports establish real selection grading; shortcut-results.json and post-delivery-shortcuts.json establish bank-role variation. The latter do not prove the absence of every possible shortcut.

## Reproduction commands

Run from the workspace. All output stays under evidence. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO=/home/jake/Developer/Course_Academy`.

```sh
$PY evidence/repair_checks.py all
COURSE_ACADEMY_GENERATOR_OUTPUT_DIR="$PWD/evidence/original-retest-runtime" $PY evidence/original-regression-shortcut.py "$PWD/17592186129197.py"
$REPO/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/samples-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence/runtime --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/samples-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-moderate --asset-root evidence/runtime --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/samples-hard.json --source ../source/source.json --inventory ../source/inventory.json --difficulty hard --output evidence/delivery-hard --asset-root evidence/runtime --math-root /media/jake/SSD/EDB/math
$PY evidence/post_delivery.py
$REPO/generate/runs/current/check-engine evidence/delivery-grader-input.json evidence/delivery-grader-report.json
python3 $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/runtime --math-root /media/jake/SSD/EDB/math
$PY evidence/package_checks.py
$PY $REPO/generate/pipeline/check_delivery.py --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/cli-assets --math-root /media/jake/SSD/EDB/math
$REPO/generate/runs/current/check-engine evidence/batch-grader-input.json evidence/batch-grader-report.json
```

All listed checks passed. Native grading before and after delivery each accepted 67 correct and rejected 268 incorrect selections. Filters retained 11 easy, eight moderate and 48 hard records; all eight common-bank five-target witnesses survive. The relocated CLI produced five deterministic easy records, all five survived delivery, with correct-value ranks 0,3,4,2,3. Its additional native grading accepted five correct and rejected 20 incorrect selections. Four invalid boundary cases are rejected. The final explicit-parameter bank provenance adjustment changes metadata only and is checked in package_checks.py; it does not change prompt, key, bank or solution.

## Rendering and limitations

Visually inspected render/question-001.png and question-002.png from the unmodified application UI. Easy area 288 and a hard logarithmic area have legible five-choice banks and corresponding shaded regions; mathematical notation and images decoded without DOM errors. The existing long hard worked-solution equations use the UI's horizontal overflow area. No plot geometry or solution layout was changed in this repair.

Candidate construction rejects duplicate areas before choosing a target, so that rejection cannot prefer a correct rank. Five positive distinct values are then kept; explicit parameter calls insert their own area only when needed. Relevant h changes affect the visible problem, final answer and native grading; unit-determinant shear changes preserve the area. Current source profiles are evidence-only and are excluded from normal generation.

The delivery helper examines captured inventory, difficulty, image localization, schema and deduplication; it does not simulate a live learner's history or database identity collisions. question_selection.rs selects within already fresh usable candidates, using difficulty weights; no learner-specific snapshot was provided. Active captured generated inventory is empty after retirement. Publication and new independent review remain runner steps. Evidence was saved inside the supplied writable workspace, not the outside author-1 path.
