Completed author repair and validation.

Three retained regressions are executable in repair-regressions.json: check_repair.py --check shortcut, --check grading, --check source. Each generates current output. All passed. Source replay covers nine sources plus all 16 targets in the restored 4x4 source. The final source-specific changes (field order, spacing, provenance) were checked separately; the resulting UI screenshot was inspected.

The reported CLI seed 3782988951/count 5/easy produces evidence/prospective-batch.json. All five records survive shared delivery. It contains two contrasting radio groups and a symbolic blank. The reported q-13498 shape does not happen to occur in this regenerated five-item sample; forced source-profile batches retain it, and the original cue succeeds only 2/5 there and 1/5 in all-target controls, before and after filtering. No seed special cases. Identical visible arrangements from two source profiles deduplicate; all target roles survive. Three additional default five-item batches passed.

Engine fix: engine/rust/symbolic.rs handles indexed formal symbols. Native grader rebuilt in place. Strict original test passes 10 accepted/10 rejected; 19 symbolic and 46 learning unit tests pass. Broader generated checks: source-control-grader-report.json has 140 accepted/323 rejected over 80 records; entry-control-grader-report.json covers entry-preservation controls and the small fresh sample. Final restored 4x4 record passes the native grader. No unresolved outcomes were accepted as success.

Package is portable with exact dependency pins and only three runtime files. Final relocated current CLI matches the prospective batch; hashes and exact commands are in evidence/final-package.json and evidence/commands-final.json. Renderer uses unmodified UI; all screenshots inspected. Captured inventory has nine originals and one correct two-index non-source record without generation metadata; no demonstrated affected generated stored record. No database changes, image publication, or service restart.

No unfinished author action. Independent review and publication remain runner responsibilities.
