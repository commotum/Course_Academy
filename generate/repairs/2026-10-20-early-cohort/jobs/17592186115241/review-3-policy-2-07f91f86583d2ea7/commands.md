All commands run from this evidence_root using /home/jake/Developer/Course_Academy/.venv/bin/python and -B. Nothing is published or written to the database.

- `python -B review.py`: independent source replay, fresh seeds 93210..93245, rational/source controls, explicit boundaries, mathematical checks, deterministic replay and relocation.
- `python -B regression_checks.py`: retained original failures and exact historical inventory reproduction.
- `python -B changed_probes.py`: strict fraction repair and template controls.
- `python -B solution_checks.py`: independent row-operation transitions and final solution checks.
- `python -B author-checks/validate_repair.py`, `python -B author-checks/rational_support.py`, `python -B author-checks/unit_support.py`: copied author suites redirected entirely into author-results/.
- `python -B focused_audit.py`: changed supplied-coordinate banks, retained strict unit/fraction regressions on failing and repaired executables, homogeneous signs and fixed-bank role changes.
- `python -B focused_solution_checks.py`: new supplied-coordinate and fixed-bank solution steps.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json` and the corresponding focused-grader-input/results: actual native grading.
- `python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output OUTPUT --math-root /media/jake/SSD/EDB/math`: INPUT/OUTPUT pairs listed in delivery-stages.json. This uses actual shared filtering read-only.
- `python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --math-root /media/jake/SSD/EDB/math` (six default cases); repeat with `--input render-remaining-records.json --output render-remaining --limit 18`, then `--input focused-render-records.json --output render-focused --limit 6`.
- `python -B finish_evidence.py`: stage/cue measurements, selection formulas, pedagogical schema/ref validation, rendering account and full package byte integrity.
- `python -B record_result.py`: independent captured-correct-link comparison and final report contract.

Copied-script provenance is in provenance.json; only evidence-root paths and fresh review seeds were changed. Strict historical failure commands deliberately return 1. Full records, seeds/parameters and actual outcomes are retained. The interrupted first attempts to redirect copied author fraction imports were corrected before successful runs; no package path was written.
