# Targeted repair verification

Finding `6900891930e4bdc756fa`: fixed the shuffled-prefix selection rule,
preserving the question catalog, banks, IDs, source replay and earlier repairs.
Repeated questions from one profile now share a recognizable subgroup and
vary each eligible qualifying label. `runtime.patch` records the runtime change.

The exact reviewed batch fails the old review checker and the retained visible
matrix audit. Its original records reproduce exactly from the current catalog.
Replaying that candidate prefix through the current sampler preserves four of
five records and replaces the A+C answer with an existing C-only case. The same
B-excluded subgroup therefore requires inspecting A as well as C. Per-record
seed 0 describes catalog construction; the unknown runner shuffle seed is not
claimed recovered. The regression explicitly restores the recorded prefix order.

- Fidelity: ten complete original questions, 15 banks, 54 choices replayed
  against the supplied source; source data remains unchanged. Two incomplete
  originals remain excluded from fidelity/grading claims.
- Correctness: exact Fraction elimination reads visible matrices, keys and
  solution assertions. Controlled A-only, C-only and A+C cases hold assignment
  and excluded B fixed; nonzero coefficient scaling preserves the response.
- Grading: native learner grader accepted 31 expected responses and rejected
  76 expected wrong responses, with no unresolved checks. Hardcoding A while
  inspecting C is accepted on the retained A-only item and rejected on C-only.
- Decision variation: seven sampler controls include three five-question seeds,
  counts 2/3/4, and all 24 semantic classes. Repeated subgroup checks cover
  eligible labels, full responses, correct positions and response counts.
  Singleton groups make no conditional-variation claim. Actual delivery checks
  retain all 44 records across the replay, three small batches and full-capacity
  batch. The complete 39-presentation catalog remains unchanged.
- Rendering: two affected actual-UI screenshots were visually inspected;
  matrices, controls and worked solutions are readable and unclipped.
- Packaging: isolated declared-file relocation runs twice deterministically.
  Installed Python 3.13.5 and SymPy 1.14.0 match the unchanged manifest pins.
- Inventory: all 12 stored items are original sources, with no stored generated
  items affected by this batch-selection defect. Ten complete originals were
  checked independently; two missing keys/solutions remain unverified.

Commands run from the workspace (PY is
`/home/jake/Developer/Course_Academy/.venv/bin/python`):

```sh
python3 -B ../review-1-policy-2-36e1ecca399a86e2/check_batch_decisions.py --input ../review-1-policy-2-36e1ecca399a86e2/batch.json --report evidence/latest-failure-reproduced.json
$PY -B checks/check_batch_decisions.py
$PY -B checks/check_runtime.py
$PY -B checks/audit_inventory.py
$PY -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair-2/render-records.json --output evidence/repair-2/render --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math
```

The first command exits 1 as the retained negative control. All current checks
pass. Exact delivery and native-grader subprocess commands are recorded in
`batch-regression.json`; complete records and native results are adjacent.

Selection limits: `question_selection.rs::select` draws uniformly within a
configured positive-weight fresh easy band; its unconfigured fallback picks the
first sorted entity. It does not guarantee an alternating learner sequence.
Live histories, reservations and future inventory are unavailable. This repair
verifies conditional support in the delivered pool at the captured inventory,
not every possible learner history. Finite capacity remains 24 semantic classes.
No database, engine, publication, or other-job changes were made.
