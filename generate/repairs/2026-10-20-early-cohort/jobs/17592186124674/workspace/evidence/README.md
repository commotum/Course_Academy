# Reproduction and results

All paths below are relative to the workspace. Python is
`/home/jake/Developer/Course_Academy/.venv/bin/python`; repository tools are under
`/home/jake/Developer/Course_Academy`. Nothing here publishes or changes a database.

`checks/validate.sh` contains the complete command sequence, including shared
delivery, actual native grader, and actual Learning.html renderer invocations.
It regenerates the test data. Visual inspection must still follow rendering.

| Claim | Evidence | Observed result |
|---|---|---|
| Original failure reproduced | before-shortcut.json, before-records.json, before-restriction.json | Strict shortest-option probe exit 1; tutoring capacity60/initial10 rejected by old ratios |
| Findings repaired | regression-results.json, math-results.json, after-shortcut.json | 114 visible records checked; exact minimal no longer uniquely shortest; capacity60 accepted |
| Source fidelity | source-replay-results.json, source-math-results.json | 14 complete banks, 70 choices; exact prompts, solutions, keys/absences, ratings/absences |
| Decision variation | pedagogical-variation.json, counterfactual-records.json | 64 controlled assignments, all eligible choices in each fixed test bank; changed equilibrium changes response/solution; changed initial preserves them |
| Normal sampling | fresh-records.json, normal-coverage.json | 40 original reviewer seeds plus 2 targeted default calls; both profiles and all 15 prompt templates exercised |
| Delivery | delivery/delivery.json, delivery-batch/delivery.json, delivery-coverage/delivery.json, delivery-regressions/delivery.json | 40/40 fresh, 5/5 batch, 2/2 witnesses, 113/114 regression records survive (one duplicate) |
| Post-filter math/shortcuts | filtered-variation.json, filtered-batch-variation.json, filtered-coverage-variation.json, filtered-regression-variation.json | Unique-shortest strategy never identifies a correct normal item; controlled position/rank variation survives |
| Actual grading | grader-results.json, batch-grader-results.json | 81 accepted, 324 rejected; zero unexpected outcomes |
| Actual rendering | render/rendering.json, visual-inspection.json | Three actual UI cases render and were visually inspected |
| Stored generated inventory | inventory-results.json, generated-records.json, affected-inventory.json | All 10 non-source records reproduce exactly; all moderate/hard; no demonstrated affected easy records; no untested non-source entries |
| Relocation and dependencies | packaging-results.json, batch.json | Relocated five-question CLI output equals local output; exact Python/SymPy versions match |

The regression command is `python -B checks/repair.py`; both retained finding IDs
map to it in repair-regressions.json. It parses visible equations and prompt capacity
with an independent symbolic witness. `python -B checks/source_package_inventory.py`
checks source replay, stored generated records, exact runtime versions and relocation.
`python -B checks/batch_checks.py` reconstructs the current batch grading cases plus
normal coverage witnesses. Grader inputs test every option in each selected bank.

The unchanged strict reviewer probe was retained as checks/reproduce_shortcut.py.
It was run before repair with
`--input ../review-0-policy-2-2563c730827bc9a7/boundary-records.json --index 0 --output evidence/before-shortcut.json`
and after repair with
`--input evidence/regression-records.json --index 0 --output evidence/after-shortcut.json`.
Its exit codes were 1 and 0. The stronger regression also requires no unique-shortest
correct normal item across each tested bank.

The source's structural-only banks are preserved by replay. New mixed banks are an
explicit same-method extension, not a claim of exact new-source bank fidelity.
Eliminating a wrong sign or population factor is legitimate mathematical work; three
positive linear-gap candidates still require the equilibrium. Mixed-bank baseline
after that legitimate elimination is 1/3, while five-capacity banks have baseline 1/5.
Exactly one correct choice is the source radio contract, not a variable response count.
Numerical capacity models are the semantic instances; contexts, seeds, UUIDs and
shuffles are not counted as new models. The semantic count is in pedagogical-variation.json.

Selection limits: check_delivery uses the real publisher normalization, rejection,
difficulty and captured-inventory deduplication rules (basis 5380). Inspection of
engine/rust/question_selection.rs shows sorting of already-fresh candidates followed
by difficulty weighting and a seeded uniform draw inside the chosen band. All
accepted records are easy, so that mechanism has no content-based exclusion of
either bank kind. Actual future entity IDs, learner history, configured weights and
post-capture inventory are unavailable offline; no live learner draw is claimed.

Canonical fish choices were not captured. Rehabilitation replay preserves missing
key/solution/rating; normal generation independently derives its unique model and
solution. Factory replay retains the source units discrepancy; served prompt and
solution use consistent stock units. Other defects in retained moderate/hard extensions
are outside this targeted easy repair. Evidence is saved inside the workspace to honor
the workspace-only constraint.
