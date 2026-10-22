All commands ran from the supplied workspace. P below denotes
`/home/jake/Developer/Course_Academy/.venv/bin/python`, and R denotes
`/home/jake/Developer/Course_Academy`. These are documentation abbreviations,
not runtime package dependencies.

- Initial AST closure reproduction: evidence/latest-failure.json. The original
  file imported scripts.generator_policy, absent from the workspace closure.
- `P checks/reproduce_legacy_failure.py`: the preserved original also fails in
  a relocated runtime with the exact undeclared scripts import; traceback in
  evidence/legacy-runtime-failure.json. This is an expected-failure reproducer.
- `P checks/package_check.py`: passed; exact dependency versions, declared
  runtime import closure, repository imports denied, two identical five-item
  `--difficulty easy --seed 42 --count 5 --format json` runs after relocation.
- Validation parser setup (test-only, already vendored):
  `uv --cache-dir .validation-cache pip install --python /home/jake/Developer/Course_Academy/.venv/bin/python --target checks/vendor antlr4-python3-runtime==4.11.1`.
- `P checks/validate.py`: passed all 8 source families and complete banks,
  53 generated records, 18 one-row counterfactual pairs, scalar boundaries,
  rejection of invalid scalars and hard band, and stale-key/solution mutations.
  This batches native grading through `R/generate/runs/current/check-engine
  evidence/native-input.json evidence/native-report.json`.
  Native result: 189 accepted, 243 rejected, zero unresolved.
- `P checks/inventory.py`: 17 captured items inspected, 7 non-source records
  mathematically reconstructed at explicit recovered parameters, 2 with no
  correct selectable checkbox. Raw captured question IDs, fields and choices
  retained in evidence/generated-records.json. Historical generation metadata
  was not captured: seeds/version are not invented. affected-inventory.json
  paths are relative to the job's author-1 evidence root, while all files remain
  in the authorized workspace.
- For each B in easy, moderate:
  `P R/generate/pipeline/check_delivery.py --input evidence/B-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty B --output evidence/delivery-B --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math`.
  Accepted 34/34 easy and 19/19 moderate; no duplicates, invalid records or
  lost cases. These files are split from evidence/records.json by difficulty.
- `P checks/shortcuts.py`: passed before/after delivery comparison, fixed
  coefficient-vector counterexamples, changing labels/counts/correct positions
  within each family, and ordinary seeded sampling. 54 ordinary generator
  draws covered all 35 feasible subsets across the 8 families. Records for
  the first occurrence of each case: evidence/normal-sampler-records.json.
- `python3 R/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math`:
  4/4 passed. All four screenshots visually inspected. Radio placeholder was
  removed after the first rendering, then validation, delivery and previews
  refreshed; final radio screenshots have no extra input line. Equations,
  fractional derivative multipliers, None choices and worked solutions are
  legible, with no clipped math or missing content.

Separate claims:

- Fidelity: original equations, difficulty ratings, whole Boolean/radio banks
  and keys replay; deliberate punctuation, equation-reference and None-policy
  presentation repairs are explained in instructional-account.md.
- Correctness: visible LaTeX is parsed independently; constant logarithmic
  derivatives characterize powers, and solution coefficients/exponents and
  normalized equations are checked symbolically.
- Grading: real native grader accepts/rejects owned choices across source,
  decision and counterfactual cases; no engine modification needed.
- Variation: 35 feasible decision subsets, 18 controlled answer-changing pairs,
  irrelevant-scalar preservation, normal seeded coverage and delivery survival.
  No incidental label/position/coefficient/count predictor found in these tests.

Limits: hard and two unrated/incomplete radio drafts unsupported; positive
x,y intervals as in the instructional account. Captured delivery filters and
inventory are verified, but live learner history/weights and future inventory
are unavailable. The Rust selection implementation selects a difficulty band
then uniformly among eligible items, without inspecting the correct subset;
that read-only inspection does not simulate any live learner. No publication,
image upload, database content change or engine change occurred.
