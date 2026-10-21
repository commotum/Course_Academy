Run from this evidence directory. All writes stay here; imports use -B to avoid package bytecode writes.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input fresh-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-fresh --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --limit 6 --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input counterfactual-records.json --output render-pairs --limit 3 --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation.py
python3 finalize.py
```

Fresh random seeds: 824031 through 824150. Explicit structural and counterfactual parameters are retained in complete generated records. Source replay: all 17 supplied source question IDs, each using its original matrix, letter, complete Boolean column bank, and replay=True. Runtime relocation copies package files beneath this evidence directory and executes from here, writing relocated-batch.json here. The maximum finite batch test uses seed 824031 and count 58; exact resampling proposals and accept/reject decisions are retained.

No repair history, repair preflight, previous review, author validation report, or preparation.json exists at the supplied paths. This is an initial source-first review. Source-analysis.json was written and read back successfully before any package implementation was inspected. Inventory basis 5362 contains 22 stored questions; all were checked directly for REF, vectors, Boolean keys, complete column banks and solution conclusions. No such defect was demonstrated; affected-inventory.json is therefore empty, not an assertion that every possible defect or historical generation lineage was audited. Stored questions lack generation metadata; originals were not marked generated.

Selection evidence faithfully reproduces the inspected easy-only path of engine/rust/question_selection.rs using actual captured entity IDs and stable hash draws, with representative seen-history exclusions. No active learner or policy snapshot was supplied. Results are conditional on an easy-positive configured policy; the explicit unconfigured-first and zero-easy-weight behavior is documented. No live learner session, publication or database write occurred.
