Commands are run from the supplied workspace. All outputs are local; no publication or database mutation is performed. Python is `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5). Set `PYTHONDONTWRITEBYTECODE=1` for the Python commands.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/regressions.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/validate.py > evidence/validation-summary.txt
/home/jake/Developer/Course_Academy/.venv/bin/python checks/inventory.py > evidence/inventory-summary.txt
```

The original failures are retained in `regressions-before.txt`; current regressions pass (3 tests). The independent review's original `regressions.py` was also run unchanged and passed (3 tests). Source replay checks 15 complete banks and 75 choices. The current runtime is matched exactly to all 32 saved fresh records by `checks/finalize.py`. Mathematical checks also cover five CLI records and five controlled counterfactuals. Relocation and deterministic CLI replay passed.

Delivery command, repeated with `(input, output)` equal to `(fresh-records.json, delivery-fresh)`, `(batch-records.json, delivery-batch)`, and `(counterfactual-records.json, delivery-cf)` below `evidence/`:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/fresh-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-fresh --asset-root evidence --math-root /media/jake/SSD/EDB/math
```

All 32 fresh, five CLI and five counterfactual records survived delivery, with zero duplicates. `checks/finalize.py` compares independently parsed matrices, complete banks and keys, coverage and shortcut probes before/after filtering. It also checks all 747 finite catalogue structures and 4,667 admissible correct operations have at least four matched incorrect alternatives (minimum observed: 14). This finite test resolves a possible sampler exhaustion gap in the new operation construction, without rendering or grading hundreds of interchangeable records.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/finalize.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/delivered-grader-input.json evidence/delivered-grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
```

Native raw grading: 29 correct accepted, 116 wrong rejected. Delivered batch and controlled cases: 10 correct accepted, 40 wrong rejected. Rendering passed for four records; screenshots 001, 002, and 004 were visually inspected. No clipping, overlapping content or unreadable notation was observed.

Fidelity, mathematical correctness, actual grading and tested decision variation are separate claims in `pedagogical-variation.json`. Counterfactuals change the offered successful operation on a fixed matrix, switch the answer by changing one matrix entry with a fixed bank, and preserve responses under nonzero rescaling. Shortcut probes cover position, length, coordinate ordering, no-op count and first-row-coordinate count, including recognizable leading-column and zero-row subgroups. No deterministic incidental predictor was found among these probes; this does not certify all possible strategies.

Inventory: inspected all 20 captured questions, excluded 15 original source records, observed five stored generated prompts with optimization wording. Historical metadata is missing and exact old-generator identity replay failed. `affected-inventory.json` is empty because identity-bound complete reproductions were not certified; it does not assert absence of affected stored questions. See `inventory-inspection.json` and `inventory-attempt-records.json`.

Learner selection: inspected `engine/rust/question_selection.rs` lines 123–190. Configured selection requires fresh usable candidates and positive band weights; no-policy selection returns the first candidate. No live learner history, future allocated entity IDs or policy state was supplied, so future selection frequencies remain unverified. Runtime file hashes are in `runtime-hashes.json`.
