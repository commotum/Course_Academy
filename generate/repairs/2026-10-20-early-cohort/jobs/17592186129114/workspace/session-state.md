# Current milestone

Read the current feedback and retained finding d72e0c903f2371587a3b. The exact
reviewed delivery batch reproduces the frozen-C failure (strict probe exits 1).
The matrix sampler and original-parameter replay are unchanged. `generator.py`
now checks complete pools for constant label actions globally, by polarity, and
by visible shape/polarity groups of at least three items, and continues sampling
when such a pool fails. The original seed rejects three candidate pools before
returning ABC, BC, B, A, C.

Completed commands (job Python 3.13.5):

- `python checks/regression_pool.py`: passed; four current five-item batches
  before/after actual delivery filtering, exact ABC -> AB C-pivot counterexample,
  irrelevant trailing-entry edit, and 138 native grader acceptance/rejection
  checks. Historical failure remains a strict failure.
- `python checks/validate_repair.py`: passed; 13 complete source banks, retained
  source corrections, 26 exact individual-sampler preservation checks, seven
  fixed-shape nonempty subsets after filtering, counts 0/1/2/3/12, 120 additional
  native grader checks, five reconstructed affected inventory records, and clean
  relocation with exact manifest Python version.

The small-batch validator initially combined same-seed prefixes and correctly
encountered delivery deduplication; its corrected test uses distinct documented
seeds for independent batch sizes. No generator change was needed for that test.

All outputs stay in this workspace. `affected-inventory.json` points to
`../workspace/evidence/generated-records.json` relative to the requested external
author evidence root; that runner-owned directory was not written. Source IDs
are excluded from the affected generated cohort. Original generation seeds were
not captured, so stored records use explicit matrix reconstruction, not invented
original seed metadata.

Final validation completed:

- `python checks/shortcut_probes.py`: passed; six delivered pools and 12 groups
  with at least three items have counterexamples to label/position, fixed subset,
  and fixed selection-count actions. The controlled triple survives delivery and
  adds 18 native checks (276 native checks total, 138 accepted / 138 rejected).
- Shared `render_preview.py` command in `evidence/commands.md`: four UI records
  passed; all four PNGs visually inspected, including the exact C pivot pair.
- Counts 32/48/64 at seed 920113 construct successfully; bounded rejection
  results and limitations saved in `evidence/larger-pool-results.json`.

Separate fidelity/correctness/grading/variation/rendering claims and finite-pool
limits are in `evidence/pedagogical-variation.json`. No runtime edits remain
unvalidated. Ready for independent review; no publication was performed.
