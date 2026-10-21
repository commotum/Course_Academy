# Reproduction and results

Run `bash checks/validate.sh` from this workspace. It contains exact commands for
regressions, source/inventory/relocation checks, shared delivery filtering, native
learner grading and actual Learning.html rendering. Latest run:
`evidence/validation-command.log`. Python is
`/home/jake/Developer/Course_Academy/.venv/bin/python`.

| Claim | Evidence within evidence/ | Result |
|---|---|---|
| Latest failure reproduced | before-number-match.json | Exact seed3/deer/capacity60 numeral-copy failure, exit1 |
| Earlier repairs preserved before this change | before-retained-regressions.json, before-current-records.json | 114 records passed |
| All retained defects repaired | regression-results.json, after-shortcut.json, after-number-match.json | Three history IDs covered; original minimal probes now exit0 |
| Independent mathematics | math-results.json, regression-records.json | 122 records have five distinct equations and exactly one correct model |
| Source fidelity | source-replay-results.json, source-math-results.json, source-replay-records.json | 14 banks/70 choices, prompts, solutions, keys/absences and ratings/absences preserved |
| Relevant variation | pedagogical-variation.json, operation-coverage.json | 68 fixed-bank target assignments; all three extra operations and both assignments tested independently from visible equations |
| Small normal regression sample | fresh-records.json, normal-coverage.json | Retained 40 reviewer seeds plus 3 targeted rank/position witnesses; 2 further default witnesses fill computer/direct-mixed profile coverage |
| Publication delivery | delivery/delivery.json, delivery-regressions/delivery.json, delivery-batch/delivery.json, delivery-coverage/delivery.json | 43/43 fresh, 119/122 regression (3 duplicates), 5/5 CLI batch, 2/2 coverage witnesses survive |
| Post-filter math and cues | delivery-variation.json, delivery-regressions-variation.json, delivery-batch-variation.json, filtered-coverage-variation.json | No unique-shortest correct normal item; mixed numeral matching and numeral-then-length never uniquely select correctness |
| Strict delivered numeral probe | delivered-number-match.json | 0/5 delivered choices solved by unique numeral match |
| Actual native grading | grader-input.json, grader-results.json, batch-grader-input.json, batch-grader-results.json | 86 correct selections accepted, 344 wrong selections rejected; zero unexpected results |
| Actual UI | render/rendering.json, visual-inspection.json, render-records.json | Three screenshots inspected: mixed equilibrium60/95 fixed bank and original tutoring capacity60 repair |
| Captured inventory | inventory-results.json, generated-records.json, affected-inventory.json | All10 non-source generated records reproduced exactly; all moderate/hard; none in demonstrated easy defect; no untested non-source entries |
| Packaging | packaging-results.json, batch.json | Exact Python3.13.5/SymPy1.14.0 declarations; relocated five-question CLI agrees with local generation |

All three finding IDs in repair-regressions.json map to checks/repair.py. It uses
visible prompt capacities and symbolic equation witnesses, with strict per-item
mixed-bank checks, rather than trusting recipe metadata. The unchanged reviewer
numeral probe is retained as checks/reproduce_number_match.py with only workspace
and output path adaptation. The earlier strict length probe remains in
checks/reproduce_shortcut.py. Tests write evidence only and never modify runtime
files, contact services, or write database content.

A mixed bank has two positive-gap candidates, each with a reversed-gap twin and
an independently assigned extra equation. Capacity matching still requires sign
reasoning; structural recognition still leaves two equilibrium candidates. Fixed
bank counterfactual pairs demonstrate that no prompt-independent cue (length,
frequency, option identity or position) can solve both assignments. Capacity-only
banks legitimately test the stated equilibrium. Cue counts are grouped by visible
bank kind and source/direct prompt template, with finite-sample limits stated in
pedagogical-variation.json. The initial 40-seed sample happened to have uniform
ranks in three small mixed subgroups. Additional default seeds3,22,25 directly
resolve those uncertainties without changing sampler probabilities. These are
coverage witnesses, not estimates of population frequencies.

The actual publisher's offline filter is used with captured inventory basis5380.
Generator construction has no easy rejection loop: invalid explicit calls raise
ValueError; normal roles are constructed compatibly. Read-only inspection of
engine/rust/question_selection.rs confirms freshness exclusions, difficulty
weighting and a uniform seeded draw within a selected rated band. An unconfigured
policy instead chooses the first candidate by entity ID. All tested survivors are
easy; no bank-kind content restriction exists in selection. Future entity IDs,
learner history, configured policy and post-capture inventory are unavailable, so
no live selection draw is claimed. The inventory audit excludes source originals
rather than relabeling them as generated.

All evidence stays under the workspace to honor its write boundary; the supplied
external author-2 evidence_root was not written. No images were published, database
content changed, engine edited, or other job modified. Source gaps and the factory
unit correction are documented in instructional-account.md.
