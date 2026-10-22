All commands run from evidence_root. The package and database were read only.
Use `/home/jake/Developer/Course_Academy/.venv/bin/python` as `$JOB_PYTHON` below.
The exact commands and old/current failing-test stdout/stderr are also retained
in retained-regression-results.json and runtime-results.json.

1. `$JOB_PYTHON -B audit.py`
   Reused independent visible-proposition parser and source replay checks;
   recreated 15 source replays, 87 controls (seed 763019), four controlled cases
   (seed 319), and copied exact runner batch. No key mismatch in 111 records.
2. `$JOB_PYTHON -B runtime_review.py`
   Manifest-only relocation, isolated import path, deterministic seed 763019,
   exact Python 3.13.5, invalid difficulty/count, zero count; retained original
   dynamic-import failure reproduced outside repository ancestry. The launcher
   maps only old entrypoint resolve ancestry because evidence_root is itself
   inside the repository. See runtime-results.json for the full command.
3. `$JOB_PYTHON -B sampler_review.py`
   Strict retained failing_batch_check.py exits 1 for prior 2.0.0 generator and
   0 for current 2.0.1. The retained old executable equals the prior independent
   manifest-only relocated executable byte-for-byte (repair-audit.json).
   Exact runner batch replay seed 2086806769; first selection pass count 73;
   fresh small batch seeds 927461, 34017, 85901. Old/current full-domain
   comparison checks preservation of 606 semantic instances, not a repeated
   exhaustive correctness audit.
4. For each input/output pair below:

   `$JOB_PYTHON -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output OUTPUT --math-root /media/jake/SSD/EDB/math`

   - `runner-batch.json` / `delivery-batch`: 5/5 survive.
   - `independent-samples.json` / `delivery-samples`: 87/87 survive.
   - `decision-prefix.json` / `delivery-prefix`: 73/73 survive.

   Preparation file is absent; these are actual shared publisher read-only
   prepare_records calls against captured inventory basis 5418. Reports retain
   implementation hashes, input paths and stage counts.
5. `$JOB_PYTHON -B current_checks.py`
   Adds independent visible-proposition checks for changed 73-record selection
   pass, current counterfactual assertions, stage comparisons, inventory and
   static learner-selection analysis. Builds one combined native grader input.
6. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine native-input.json native-report.json`
   184 cases / 1,002 submissions: 348 accepted, 654 rejected, zero unresolved;
   database writes 0. No free-entry response fields exist in this package.
7. Renderer input is exact five-record batch, four controls and first two
   source replays. Recreate after audit.py with:

   `python3 -c 'import json;json.dump(json.load(open("runner-batch.json"))+json.load(open("counterfactual-records.json"))+json.load(open("source-replays.json"))[:2],open("render-records.json","w"),indent=2)'`

   `$JOB_PYTHON -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math --limit 11`

   All 11 pass. All screenshots were actually inspected, including controlled
   pairs: 006 base; 007 determinant polarity; 008 equivalent nullity premise;
   009 deficient-rank premise retaining all three printed conclusions.
8. `$JOB_PYTHON -B finish_checks.py`
   Rechecks all source worked implication paragraphs, four explicit rejection
   boundaries, moderate scope, and package hashes (158 unchanged files).
   Inherited screenshot assertion was removed; fresh inspection is recorded
   separately in visual-inspection.json.
9. `python3 write_report.py`
   Assembles report and decision evidence from completed results. Source account
   and reusable scripts have provenance.json; runtime-delta.diff confirms only
   version and batch selection changed in the executable closure.

Run evidence_validation.py last. It checks the pedagogical schema, all cited
local evidence, summary counts and final package integrity. No publishing or
database commands are used.
