Run from the workspace with `PYTHONDONTWRITEBYTECODE=1` and `/home/jake/Developer/Course_Academy/.venv/bin/python` (abbreviated `$PY` below).

- Baseline: `$PY checks/shortcut_reproduction.py` exited 1 before repair, fresh 13/13, archived batch 1/1, archived delivered controls 5/5. `evidence/before-fraction-shortcut-results.json` and `evidence/before-minimal-failing-record.json` preserve that evidence. After repair the same script exits 0, fresh 0/13; its archived batch/control inputs deliberately remain the historical failing records, not regenerated output.
- Required regression: `$PY checks/repair_regression.py` (30 current-generator cases, independent rendered-equation checks).
- Additional demonstrated cue: `$PY checks/radical_regression.py` (four boundaries; fraction counts, equal-length wrong alternative, independent math).
- Focused validation: `$PY checks/validate_repair.py` (10 complete source banks; visible-math/stages; all-choice native grader; relevant/irrelevant counterfactuals; regenerated actual batch; captured inventory; relocation). Native command batched internally: `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json`.
- `$PY /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --math-root /media/jake/SSD/EDB/math`
- `$PY /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/replacement-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --math-root /media/jake/SSD/EDB/math`
- `$PY checks/inventory_check.py` (both demonstrated fraction-layout cues on all 16 captured records; six generated, none affected).
- `$PY checks/post_delivery.py` (conditional cues and coverage on actual accepted records, selector limits).
- `$PY /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render-final --math-root /media/jake/SSD/EDB/math` then inspect all screenshots.

No publication, image upload, service contact, or database mutation is performed by these checks. All test outputs stay in the workspace. Runtime manifest was reduced to the existing entrypoint, its required local math helper, and pinned requirements; legacy publication logs/scripts are retained on disk but excluded from runtime packaging.

Revision 2 supersedes the quotient profiles and final evidence above. Current reproducible commands and results: [revision-2/commands.md](revision-2/commands.md). Previous author reports are retained under revision-2/previous-*.json. Current consolidated report is author-report.json.
