# Three-coefficient linear combination generator

Script: `generate/scratch/17592186119854.py`. Registered UUID: `12b9727c-8650-5b8b-a2a5-255818e1f719`. Supports moderate and hard; easy is a bounded unsupported band, with five questions still missing. See capabilities.json.

Run `.venv/bin/python generate/scratch/17592186119854.py --difficulty moderate --count 5 --seed 123 --format json`. Run the adjacent validate.py to reproduce exact-math, rendered-matrix, source-bank and actual learner-grading checks.

Validation: 318 distinct instances (168 moderate, 150 hard), 12/12 complete source banks and 48/48 distractors; 318 accepted and 1272 rejected learner-grading checks. Source prose is normalized and concrete arithmetic wording standardized; fidelity is reported separately from correctness. Side-by-side originals and variants, every original choice mapping, and slot coverage remain in this package.

Classification source basis 2584; registration committed and verified at basis 2585, under the application api.lock held from current-inventory recheck through submission and readback. Contributor application/ca-engine. Exact prepared EDN, durable intent/request key, preview, receipt, and exact-basis verification are under reference/replenishment/basis-2584/.

Fresh validated inventory after verification: moderate 5, hard 6, easy 0. The 13 source questions and canonical example are unchanged; q-34243 remains incomplete/unrated and q-74032 remains unchanged with its faulty intermediate matrix documented and excluded from validated reserves. No new questions were inserted because supported reserves already met the target. Generator registration is the only durable content change; no learner/history datoms changed. Repeated preparation has zero further changes.

Outcome `unsupported` refers to the easy band, not the validated moderate/hard generator. The exact requested job result is saved in the inventory job's .result file, with evidence and verified basis.
