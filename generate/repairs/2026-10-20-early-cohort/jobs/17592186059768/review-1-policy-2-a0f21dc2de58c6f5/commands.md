All commands run from evidence_root. Use /home/jake/Developer/Course_Academy/.venv/bin/python with -B for review scripts. Only evidence_root receives writes.

1. python -B review.py
   Replays ten complete supplied banks, samples fresh seeds 623981101+107*profile_index+offset (8 per profile), tests explicit boundaries and controlled dependencies, exact old witnesses, author checks redirected here, manifest-only relocation and runtime versions. Results in source-replay-results.json, math-results.json, boundaries.json, retained-regression-results.json, author-*-command.json and packaging-results.json. The independent parser was copied verbatim to independent-witnesses.py with provenance; prior main is never run.
2. /home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
3. python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input independent-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-easy --math-root /media/jake/SSD/EDB/math
   Same invocation for independent-moderate.json/moderate/delivery-moderate and runner-batch.json/easy/delivery-batch.
4. python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render --math-root /media/jake/SSD/EDB/math
   Default limit is six. Remainder saved separately, then:
   python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-remaining-input.json --output render-remaining --limit 15 --math-root /media/jake/SSD/EDB/math
5. python -B reproduce_inventory.py
   Historical executable archived by previous independent review reconstructs all seven generated stored records from original source and archived parameters. Full publisher-normalized content and identities compared to captured inventory. No source question marked generated.
6. python -B variation.py
   Saves coverage, finite conditional shortcut probes, before/after delivery comparison, captured learner-selection limits, affected-inventory.json and controlled boundary counterexample. Inspect individual per-profile and mode subgroups, not only totals.
7. python -B boundary_regression.py
   STRICT ACCEPTANCE TEST, currently intentionally exits 1 with ValueError. Exact valid case: generate('easy',941713401,profile='q-71722',parameters={'2':1,'3':4}). Must return five distinct source-scope choices with expected correct matrix [[1,-1,4],[1,1,-1]]. Do not weaken to accept the exception. Negative unit case also reproduced by variation.py. Original pre-repair corner witness and omitted source failures separately reproduced against previous independent archived package in retained-regression-results.json.
8. Delivery duplicate and difficulty controls: exact commands and output retained in delivery-duplicate-command.json and delivery-wrong-difficulty-result.json. One stored duplicate and one repeated new record removed, one new record retained; requesting moderate for easy records rejected.
9. python -B finish_review.py
   Assembles results from completed evidence, rendered text dependency checks, and manual screenshot observations; checks all package hashes. Does not resample.
10. System python3 with jsonschema validates pedagogical-variation.json against generate/pipeline/pedagogical-variation.schema.json. Final evidence reference and integrity validation saved in evidence-contract.json.
