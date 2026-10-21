Current status (author repair 2026-10-18): UNSUPPORTED because valid logarithm-equivalent blank entries remain unresolved by the native learner grader. The scaled-linear repair is complete and retained. Nothing published and no database writes. The earlier readiness statement below is superseded by review feedback and this repair.

Repair milestone:
- Read ../feedback.json first; preserved all candidate runtime files and earlier evidence.
- Added e-728 (canonical y=3·2^(1-x)) with original prompt/solution and authored full-derivative blank. Small signed linear variants, including unit inner derivatives and c=1..5, are sampled normally. q-107461 now permits and samples c=1..5 as a same-method extension.
- Appended the review repair instructional specification before implementation.
- Ran `/home/jake/Developer/Course_Academy/.venv/bin/python repair_checks.py`. Commands and logs: evidence/repair/commands.json. All 13 old source replay questions are exactly unchanged; canonical original parameters replay; 31 targeted records pass independent calculus; native ordinary checks: 124 accepted / 128 rejected. Post-delivery ordinary checks: 52 accepted / 82 rejected. Delivery accepts 28 easy, 2 moderate, 1 hard; five-question CLI batch and relocation pass. Within-template probes before/after filtering find no deterministic tested cue in the repaired families, with small-sample limits recorded.
- The required ln(4)=2ln(2) acceptance test FAILS as expected in evidence/repair/required-acceptance-failure.log. Adding an alternative to blank choices does not change grading; switching the single canonical reference reverses which valid expression is unresolved. Delivery retains the defect (2 unresolved checks in the delivered diagnostic variants). These are blocking failures, not passing learner checks.
- Actual UI renderer passes 6 cases; all 6 screenshots visually inspected: canonical, two scale-only pairs, and the factor-only defect instance. See evidence/repair/visual-inspection.json.

Next unfinished step: native learner engine must support this logarithm identity or accepted blank alternatives. learning.rs::grade_field only reads answer-field/correct for blanks; adding stored choices cannot repair it. Engine changes and recompilation outside this workspace are not authorized. Retain base-4 practice and the original response contract; do not mark ready or publish this package until the acceptance test passes with the real engine.

Earlier author history (retained; readiness claim superseded):

Package: package.json -> generator.py, with local source.json, math_format.py and pinned requirements.txt. Default easy; easy/moderate/hard supported. Source historical profiles are evidence-only. Preserved useful chain-rule/rendering helpers from existing_entrypoint, added the missing source families and actual hard tangent equation, retained all captured banks and repaired missing fields/designations. Final normal coefficient banks use variable pair/singleton assignments, rather than the draft's option-length cue or a same-sign bank.

Completed commands (job Python = /home/jake/Developer/Course_Academy/.venv/bin/python):
- python run_checks.py: source replay, independent math, shared delivery for all bands, before/after cue probes, native grader, solution stages, relocated CLI and actual UI rendering. Full commands are in evidence/commands.json.
- python audit_variation.py evidence/test-records.json evidence/variation-before.json and the equivalent accepted.json/variation-after.json command after adding pair/singleton probes: no deterministic tested cues overall or in coefficient-sign subgroups.
- python final_regression.py: all 13 original source designations, unchanged five-record default output, and relocated five-record CLI pass after preserving the original designation among equivalent blank answers.
- python finalize_evidence.py: separate claims, scope limits, hashes and manual visual-inspection record.

Results: 13 source cases, 12 complete captured banks, 49/49 source options; 146 test records, 138 semantic instances, 17 counterfactual pairs. All three bank roles and all five bases occur in each applicable family. Delivery accepts 100 easy, 34 moderate, 12 hard and the separate five-record default batch. Native grader: 347 accept/514 reject; delivered: 202 accept/416 reject; solution stages: 222 accept; no unresolved checks. All 12 UI screenshots visually inspected, with final revised radio screenshots rechecked. Runtime manifest and exact installed dependencies verified. See evidence/pedagogical-variation.json for qualifications about nonzero-slope scope, native logarithm identities and unavailable personalized selection state.

Next unfinished step: independent runner review/publication, outside this author job's authorization.
