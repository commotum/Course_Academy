Completed repair for ad7e55b230ca82a0d63b. Runtime: existing and missing easy targets share default banks; larger missing cases use an explicit bank anchor; CLI constructs shuffled decision pairs plus a blank when odd. Source profiles retained. package.json now lists only runtime entrypoint and pinned requirements.

Validation completed:
- .venv/bin/python validate_repair.py: passed exact current CLI easy/count5/seed3302362091, boundary counterfactual, six source banks (26 choices), independent matrix/solution checks, current-batch and sample delivery, 18 finite batches, 65 controlled witnesses, native grader (80 accepted/295 rejected), captured inventory and relocation.
- Shared render_preview.py: 3/3 passed; all 3 screenshots visually inspected, see evidence/visual-inspection.json.
- shortcut_regression.py reports corrected to distinguish vacuous batch from nonvacuous sample; four affected report calls passed. The exact batch contains two larger radio pairs, while the 48-record sample includes 6 existing and 6 missing 2x2 radios. No historical batch edits.

Evidence/results.md summarizes separate fidelity/correctness/grading/variation claims and limits. repair-regressions.json points to validate_repair.py, which regenerates current output and uses shared delivery filtering. No unfinished author implementation or validation remains. Runner fresh review/publication is the next normal workflow stage, not an author blocker.
