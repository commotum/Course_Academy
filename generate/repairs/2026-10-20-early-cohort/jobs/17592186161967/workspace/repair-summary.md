# Targeted repair result

Finding d02e8980f26ead535fe5 is fixed. The original reproduction went from 36/36 leaking records to 9/36 satisfying its first-coefficient predicate; the minimal seed-472 case no longer reveals the answer by frequency. All 52 generalized extra-option sign/role patterns have a stronger counterexample: one identical ordered answer bank accompanies four different correct sign pairs. All 208 controlled records survive shared delivery filtering, with modal-coefficient inference at exactly 50% wherever defined. Swap-profile signs were repaired as well after seven concrete bank-only sign-inference failures were reproduced.

Fidelity: all ten source questions / twelve complete banks replay, including both captured duplicate banks. Explicit replay preserves original source choices; CLI sampling uses generalized banks, including when forced to sample an original matrix. Easy workload and five-choice radio contract are unchanged.

Correctness: independent integer arithmetic evaluated every choice and every solution stage in 300 records. Target changes and irrelevant-entry preservation passed. The 300 include the targeted finite bank-domain checks, a small 30-record fresh sample, source replays, boundary cases, counterfactuals and a five-record candidate batch; this count is not a claim of 300 unrelated semantic instances.

Grading: native grader accepted 300 correct choices and rejected 1,200 distractors, with no unresolved checks. Rendering: two actual Learning UI screenshots inspected; existing long solution chains require horizontal scrolling. Packaging: only the entrypoint, source data and pinned requirements are runtime files; exact Python 3.13.5 / SymPy 1.14.0 declarations; relocated five-record CLI output matches.

Delivery: 300 input records, 270 accepted, 30 duplicates. All 208 fixed-bank counterfactuals and all 30 fresh records survive. Normalized explicit source replays also survive text deduplication; they are fidelity-test artifacts, not the candidate batch. Do not publish the validation corpus. The candidate batch is evidence/candidate-batch.json; the runner should resample through the CLI as usual. Live learner history, concurrent publication, and database collisions were not simulated. The provided question_selection.rs weights difficulty bands and then selects by seeded uniform index from fresh usable candidates; it does not inspect bank features.

Inventory: verified all ten captured records are original source questions, zero generated records. No eligible historical generated defect is demonstrated; evidence/affected-inventory.json is empty. Database and image publication remain untouched.

Reproduction commands: evidence/commands.sh. Retained runner regression: check_repair.py, declared in repair-regressions.json. Current instructional specification: instructional-account.md supplements the preserved original extraction documents.
