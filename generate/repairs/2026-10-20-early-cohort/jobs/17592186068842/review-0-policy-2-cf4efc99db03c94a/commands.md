Run from this evidence directory. Python is `/home/jake/Developer/Course_Academy/.venv/bin/python`; set `PYTHONDONTWRITEBYTECODE=1` to avoid package bytecode writes.

1. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py`
   Independent source replay, boundary/fresh generation, runtime, rejection, relocation, and initial package hash binding.
2. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python independent_checks.py`
   Independent displayed-equation math, all-choice native grader input, controlled pairs, sample render input, and raw cue probes. The review parser was corrected to separate an adjacent `y` from the `sin` token for n=1; the final 51 records pass. No generator change was involved.
3. Delivery, separately for `easy-records.json` and `batch.json`:
   `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input easy-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-control --math-root /media/jake/SSD/EDB/math`
   Substitute `--input batch.json --output delivery-batch` for the actual batch.
4. Minimal defect / additional independent seeds:
   `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python shortcut_reproduction.py`
   Complete failing n=1, seed=17 record is `minimal-failing-record.json`. Additional seed records and individual outcomes are `shortcut-records.json` and `fraction-shortcut-results.json`.
5. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-complete-input.json grader-complete-report.json`
   64 complete records, every option: 64 accepted, 256 rejected. This includes 13 additional shortcut records. All fields are source-style radio; free-entry notation tests are inapplicable.
6. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --limit 19 --math-root /media/jake/SSD/EDB/math`
   Unmodified UI. All five batch records, all three controlled pair records, one instance of each template. Screenshot inspections are recorded in `visual-inspection.json`.
7. `python3 delivery_analysis.py` and `python3 finalize_evidence.py`
   Captured-inventory probe, conditional learner-selection simulation, pedagogical report, schema-compatible counts, and final package integrity check. Learner-specific policy/history/IDs were not supplied; all simulations identify their assumptions.

No database or publication command was run. Original source items were excluded from the affected generated-inventory list. The absence of prior repair-history and preflight files was checked before testing.
