All commands run from the supplied workspace, with PYTHONDONTWRITEBYTECODE=1. Python below is /home/jake/Developer/Course_Academy/.venv/bin/python. No publication or database writes were performed.

1. Exact latest failure, before editing: `python evidence/revision-2/before/minimal_repro.py "$PWD"` exited 1; both modal and repeated-left shortest attacks selected the correct equation. Copies were necessary because the supplied reviewer script writes its own directory. Its complete records/results remain under before/.
2. Retained baseline: `python checks/repair_regression.py` passed 30 cases before editing; this showed the first repair was already intact.
3. `python checks/bank_signature_regression.py` passed 6 fixed-bank/four-target groups (26 records), including both exact latest witnesses. Both exact reported attacks fail. Independent visible equations and worked stages checked. The same check_group function rejected the prior reviewed generator in review-1-policy-2-800c03f7bd804ec6/relocated, with assertion “correct power leaks into visible bank construction”; see retained-test-strength.json.
4. `python evidence/revision-2/after/minimal_repro.py "$PWD"` exited 0: neither attack selected the correct minimal answer.
5. `python checks/repair_regression.py` passed 30 current cases; `python checks/radical_regression.py` passed 4 retained layout cases and 2 added same-bank radical groups. The latter was strengthened after the independently demonstrated modal-root cue (4/4 before; complete evidence in before-radical-modal-records.json/results.json).
6. `python checks/validate_repair.py` passed 10/10 complete source banks (50 choices), 72 independently parsed records and all worked stages, native grading (72 accepted, 288 rejected), controlled relevant/irrelevant changes, deterministic relocation of five records, and exact dependency versions. Rerun after the radical follow-through to keep the evidence current.
7. `python checks/revision_delivery.py` wrote the expanded affected sample and ran native grading for 34 additional controlled records: 34 accepted and 136 rejected. Native commands are batched, via `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json` and the corresponding revision-2 paths.
8. Actual delivery commands:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/revision-2/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/revision-2/delivery --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/replacement-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --math-root /media/jake/SSD/EDB/math
```

Results: 46→38 original controls; 80→49 expanded affected controls; 5→5 replacement batch. Duplicates only were skipped. All six easy families, both quotient profiles, all six quotient four-target groups and both radical two-target groups survive.

9. `python checks/post_delivery.py` and `python checks/revision_delivery.py check` passed. The latter checks visible banks/keys after actual filtering. Chance modal hits are reported, not hidden: among accepted quotient records the attack succeeds on 1/4, 2/4, 2/12, 2/12 in the four family/profile groups; repeated-LHS-shortest succeeds on none. Controlled identical-bank groups establish that no deterministic answer-bank strategy can identify all four keys. Five-option random baseline is 1/5; after excluding an unseparated row using the target definition it is 1/4. No arbitrary balance quota is imposed.
10. `python checks/inventory_check.py` and `python checks/revision_inventory.py` tested all 16 captured entries, distinguishing the 10 original sources and 6 generated. No generated record demonstrates any of the named cues. No generated quotient instance occurs in that captured pool. The affected-inventory arrays are empty verified results, not untested inventory. Latest results are revision-2/inventory-probe.json.
11. Actual final UI render:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/revision-2/render-final --math-root /media/jake/SSD/EDB/math
```

All five pass. Four quotient screenshots were visually inspected; final bytes match those inspected screenshots. The changed final radical screenshot was separately inspected. All prompts, radio controls, exponents, fractions and worked solutions are readable and unclipped.

The selector was read at engine/rust/question_selection.rs:125-196. It deduplicates/sorts supplied fresh usable IDs, selects a positive-weight nonempty band, then uniformly selects within it from hash-derived values; unconfigured policies take the first sorted ID. Upstream learner history, live weights and future IDs are unavailable. Their personalized execution is not claimed. Generator code has no rejection/resampling loop; invalid explicit parameters or ambiguous banks raise errors. The same-bank constructions test all supported target powers rather than relying on rejection to hide a case.
