The exact latest reviewer regression was reproduced before edits: q-129207 raised
ValueError at seed 817 with its original parameters. Logs: reproduction-before.txt
and evidence/regression-before.txt. The strict local regression also failed before
the repair. Instructional analysis was written before runtime changes.

Bundled source refreshed from supplied basis 5355; all 14 previous question records
are unchanged, and q-129207 with its complete bank and solution is added. Existing
sampling, math formatting and decision variation retained; version is 1.1.1.
Regression: .venv/bin/python -B checks/source_coverage.py. Completed: 15/15 banks,
75/75 choices replayed; original reviewer regression passes. Focused validation:
44 normal records (30 new-profile, one each prior profile), six counterfactuals,
five same-task anchor cases, deterministic five-question CLI and relocation pass.
Shared delivery retained 44/44 normal and 5/5 CLI records. Independent coverage and
shortcut results unchanged after filtering. Native grading: 81 correct selections
accepted and 324 distractors rejected, including 11 normalized delivered records.
Actual UI: four previews rendered and all screenshots visually inspected.

Read-only inventory audit inspected 20 records: 15 sources and five nonsource
records without generation metadata. None demonstrated affected by the omitted
profile finding; historical replay and live learner policy remain limited.
Full commands/results: evidence/commands.json and evidence/repair-report.json.
Executable retained finding: repair-regressions.json. No unfinished implementation
or required checks remain; next step is the runner's independent review. No database
content, engine files, published images or other jobs were changed.
