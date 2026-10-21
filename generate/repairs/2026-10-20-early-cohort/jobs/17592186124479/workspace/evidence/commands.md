Run all affected checks with `bash checks/run_checks.sh` from the workspace. The constituent commands and their input/output paths are in that script. Runtime package files are never modified by these checks.

Exact retained failure (executed before changing generator.py):
`/home/jake/Developer/Course_Academy/.venv/bin/python checks/check_batch_shortcut.py --input evidence/original-delivered.json`
Exited 1 with every rank equal to row count minus one. Full original records and result are retained in original-delivered.json, original-failure.json and original-failure.txt. Original implementation is generator-before.py.

Affected regression: `.../.venv/bin/python checks/repair_checks.py` passes 21 batches: original CLI seed/count, three small boundary/count checks, and contrasting-case pairs for each of the 17 retained source workloads. It executes the actual shared delivery filter on the original-seed repaired batch, requiring all five survive and every shape and workload/active-row group vary rank. Additional strict rows-minus-one acceptance test: `.../.venv/bin/python checks/check_batch_shortcut.py --input evidence/delivery/accepted.json` exits 0.

`checks/validate.py` passes all 17 complete source replays, 89 visible mathematical/row-annotation checks, all allowed ranks per workload, controlled one-cell rank reversal and irrelevant name/rescaling changes, dependency pins and relocated deterministic execution. Native grading subsequently accepts 89 correct selections and rejects 356 distractors (445 total, zero unresolved).

`checks/probes.py` passes the actual delivered batch against all nine named cue strategies in each recognizable workload/shape/active-row group, before and after filtering. The broader control collection has 67 records, 66 retained. One identical visible record had two source aliases, so post-filter grouping uses visible workload signatures instead of source IDs. Conditional rank coverage survives. Fractions for option-position coincidences in tiny control subsets are reported without claiming they demonstrate a sampler rule. Controlled label witnesses prevent treating unique labels as proof of variation.

All 22 captured inventory questions tested: rows-minus-one succeeds on 5/22 overall and 1/5 stored generated questions. No corresponding pool-wide defect; old failed-batch IDs are absent. affected-inventory.json is empty for that verified reason, not because the inventory was untested.

Actual UI renderer passes three representative records; all three screenshots visually inspected. No images published, no database writes, no engine edits. All authored files and evidence are inside this workspace.
