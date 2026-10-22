# State

2026-10-22 targeted continuation for finding 9e827407d5429a1f8827. Read feedback and full repair history. Exact reviewer reproduction at batch(easy,5,4258185931) fails before repair: pivot/rank shortcut 5/5, q-73439 3/3. Archived original visible records in evidence/batch-shortcut-before-records.json; strict new check also exits 1 on them (evidence/strict-retained-failure.log). All earlier registered regressions passed before this change (evidence/before-batch-repair-regressions.log).

Instructional account updated before implementation. Only runtime change: version 1.1.1 and batch selection prefers intact five-target contrast banks, rotating shuffled source families, retaining incomplete banks after full ones. Existing construction, source replay, finite semantic catalog, inventory exclusions, notation and runtime closure preserved. Exact original reviewer test now scores 1/5 (evidence/batch-shortcut-after.log).

New executable checks/check_batch_selection.py inspects visible matrices and choices, tests the original cue, independent elimination, rank/position changes with fixed bank and upper row, full catalog preservation, actual delivery and native grading. Registered the exact retained finding ID in repair-regressions.json; packaging/count event checks remain.

Validation running: job Python -B checks/check_batch_selection.py and checks/check_all.py, logs evidence/batch-selection-regression.log and evidence/after-batch-repair-regressions.log. Next: finish checks, render and inspect representative current batch, refresh inventory latest-cue audit and final repair report. No publication, database changes, engine changes, service calls, or other-job writes.
