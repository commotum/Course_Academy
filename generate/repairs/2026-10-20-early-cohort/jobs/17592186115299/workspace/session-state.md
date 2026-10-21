Implementation complete: classification-3 closes repository imports, bundles generator_policy, updates supplied 17 source banks, retains q-32242 and TeX repairs, and chooses moderate rank/consistency cases before numbers. Source replay and generic sampling remain distinct explicit parameter modes.

Passed commands:
- .venv/bin/python checks/package_relocation.py: 15 records across all bands; seeded byte reproducibility; no package writes after relocation using only manifest files.
- .venv/bin/python checks/validate_repair.py: 17 source replays, 109 sampled records, 51 controlled records, 274 native cases (862 accepted/1006 rejected); 97/97 moderate records accepted by check_delivery, no deduplication or case loss. Full logs in evidence/validation-console.txt. Later change reduced only render selection from 19 to seven representative records.
- .venv/bin/python checks/inventory_audit.py: ten generated stored easy/hard records independently checked; 30 native accepted/30 rejected. No generated moderate records at captured basis 5374. affected-inventory.json is an empty verified finding set for this scope.

History has no formal finding IDs; repair-regressions.json uses the retained event's reason code legacy_packaging_or_sampling for its executable relocation regression. Supplemental source/math/variation/native regression is checks/validate_repair.py. No database content, publication, engine changes or outside-workspace writes.

Next unfinished step: inspect actual UI screenshots from render_preview, then record final bounded validation results.

Final milestone: all implementation/validation steps completed. Actual UI rendering produced six default-limited screenshots from evidence/render-records.json; all six visually inspected. A later source-only q-74638 echelon-description correction was verified with checks/final_focus.py (17 replays, 12 native records: 29 accepted/47 rejected), rerendered separately, and visually inspected in evidence/render-source-correction/question-001.png. The newer image supersedes the earlier q-74638 screenshot. All package files are hashed in evidence/final-summary.json. Python/sympy/mpmath versions inspected: 3.13.5/1.14.0/1.3.0.

Final seeded CLI batch: seed 20261021, count five, moderate, evidence/final-batch.json; shared delivery accepted all five. Conditional shortcut probes and final grading are recorded in evidence/shortcut-probes.json and evidence/final-batch-native-report.json. General coverage sample has 97 moderate records but 43 semantic equation-system instances; both counts are explicit. All supported rank/consistency cases remain after delivery. No pending implementation work. Ready for independent review; nothing published.
