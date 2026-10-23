# Comma-index grading repair

Fixed retained finding `34e5515d1b3374bbde8b` in `engine/rust/symbolic.rs`; rebuilt the shared native grader. The supplied source is unchanged. The old engine unit expectation that `a_{12}` differs from `a_{1,2}` was incorrect for the lesson's ordered pair of row/column indices; it is now an acceptance regression. Wrong coordinates, bases, entry values, multidigit boundaries and extra components remain rejected. The engine patch contains only this rule and its tests. Generator runtime files are byte-for-byte unchanged, preserving all completed repairs.

Reproduction: `before.json` records the exact review failure. `commands-before.json` and `regression-before.log` show the new retained check failing on the current CLI's output. Run from the workspace: `.venv` Python at the repository root with `-B check_index_notation.py`. It generates seed 3782988951/count 5/easy, retains `prospective-batch.json`, applies the shared filter, and runs the original reviewer's check on raw and delivered records. It then grades independent visible-coordinate cases across every easy 4x4 target and both symbolic source examples. All expectations are strict accepted/rejected.

Fidelity and mathematics: prior source and shortcut regressions passed on current output (105 records), preserving all nine source replays and all 16 restored 4x4 positions. The engine change does not alter generation.

Grading: the original historical counterexample passes (1 accepted/1 rejected). Expanded raw and delivered checks each pass 4 accepted/7 rejected. The 18 symbolic controls pass 72 accepted/139 rejected, with zero unresolved outcomes. Existing grading regressions pass after rebuilding. Symbolic unit suite: 20 passed; learning unit suite: 46 passed.

Decision variation: retained current-output bank-role, target-counterfactual and incidental-entry controls pass before/after filtering; see ../shortcut-results.json and ../commands-all.json. The prospective batch still has five delivered records and contrasting targets for each radio bank. No favorable seed selection or runtime hash-only change.

Rendering: two current delivered examples rendered through the unmodified UI; both screenshots visually inspected and readable.

Inventory: all ten captured records inspected. Nine are original sources; the only other record has correct separate numeric indices, and no captured generation metadata. No eligible generated stored record with this symbolic defect was demonstrated. `affected-inventory.json` is empty; originals are not marked generated. Live learner histories and post-capture database content were not inspected.

Package manifest and runtime hashes are preserved (`package-integrity.json`). All four finding IDs have executable current-output checks in `repair-regressions.json`. No database changes, image publication or live service restarts. Independent review/publication remain with the runner.
