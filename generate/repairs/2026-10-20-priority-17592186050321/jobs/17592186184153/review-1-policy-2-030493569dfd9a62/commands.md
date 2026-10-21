Run from this evidence directory. Python below is /home/jake/Developer/Course_Academy/.venv/bin/python; all Python calls use -B and PYTHONDONTWRITEBYTECODE=1. No script writes into the reviewed package.

1. python -B review.py > review-run.log 2>&1 (seeds20261020,9817301,458729;240 records each;96 explicit boundaries;14 controlled records; source and packaging checks).
2. python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery --asset-root .
3. Same delivery command with --input runner-batch.json --output batch-delivery.
4. python -B variation_checks_fast.py > variation-fast-run.log 2>&1 (cached exact same independent cue tests as variation_checks.py); its initial all-inventory candidate assumption is superseded by selection_check.py.
5. python -B additional_pairs.py (three reciprocal controlled pairs; grader-input-complete.json).
6. python -B shortcut_confirmation.py > shortcut-confirmation-run.log 2>&1 (fresh seed86184906,count240; exact factor-domain proof).
7. Same delivery command with --input shortcut-holdout-records.json --output holdout-delivery.
8. python -B confirm_delivery_grading.py; /home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input-final.json grading-final.json > grading-final-run.log 2>&1 (one final batched run of all794 responses).
9. python -B selection_check.py > selection-run.log 2>&1 (supersedes initial candidate assumption; captured usable inventory and1000 synthetic task seeds per policy/history scenario).
10. python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-full --asset-root . --limit 24; Likewise --input reciprocal-counterfactual-records.json --output render-reciprocal --limit 6, and --input shortcut-render-records.json --output render-shortcut --limit 2. Initial render/ directory covers first6 only and is superseded by render-full/.
11. python -B finalize_review.py (41 supplementary exact checks and final JSON contract artifacts, including package hash equality).

Visual QA: inspected render/contact.png, render-full/contact-2.png through contact-4.png and question-018.png, render-reciprocal/contact.png, both render-shortcut screenshots. Contact sheets are only resized actual-UI screenshots; underlying full-size screenshots and HTML are retained.

Authoritative corrected selection snapshot is selection-final.json. It is copied after selection_check.py succeeds and excludes the four captured unusable source records. selection-results.json may also contain the superseded broad-inventory experiment.
