Both retained failures are repaired. The easy source now has its own guarded
complete-bank profile; the moderate source has been appended to the existing
source-bank data. Existing random sampling, mathematical rules, other source banks,
and formatting helpers are preserved. Generator version is 1.2.1. The manifest
declares the added local JSON file; runtime dependencies remain Python 3.13.5 and
the standard library.

`checks/latest_failure.py` retains the original twelve scaling candidates and
tests the newly available explicit profile with the same strict bank comparison.
It also retains the original row-addition counterexample. Both historical finding
IDs point to this executable regression in repair-regressions.json. The broader
source check parses original source questions rather than trusting runtime bank
metadata. No source evidence changed.

Validation results:

- Fidelity: all 13 source cases replay; all 12 captured practice banks match all
  five mathematical choices and captured keys where supplied. All captured worked
  solution stages match after mathematical parsing. The canonical example lacks
  a captured bank. q-10252 lacks a captured key and solution; these are inferred
  as explained in instructional-account.md.
- Mathematics: 82 records pass independent visible-prompt computation, unique-key
  and final-solution checks (13 source replays, 58 small regression samples, 11
  controlled variants). Both newly added source profiles reject changed inputs.
- Grading: native grader accepts 13 and rejects 52 raw source/control responses;
  after delivery, it accepts seven and rejects 28 control responses. Zero unexpected
  outcomes. Radio notation equivalence is inapplicable.
- Variation: controlled pair/target/coefficient changes alter the result and key;
  matrix renaming preserves the mathematical result. All three easy swap pairs
  and all three scaling targets occur. Conditional positions, matrix names, and
  magnitude probes are recorded. No tested incidental predictor applies throughout
  an easy template; sparse subgroups do not establish universal absence of cues.
- Delivery: 47 easy input records yield 45 accepted records and two duplicates;
  all seven distinct easy control decisions survive canonical ID reassignment.
  The requested five-record batch yields five accepted records. Counts and
  within-template probes are compared before and after filtering.
- Packaging: deterministic relocated execution passes in all three supported
  bands; nine easy/moderate source profiles also build from relocated declared
  files. Runtime hashes are saved. Rendering passes for both changed profiles;
  both actual UI screenshots were visually inspected.

Reproduce from this workspace with `bash checks/reproduce.sh`. The individual
commands and scripts are retained; do not rerun unrelated historical large audits.
Earlier review evidence is read-only at ../review-0-policy-2-3edbf008895863aa.

Inventory: evidence/affected-inventory.json is empty because these replay-profile
omissions demonstrate no affected generated stored question. All 12 stored source
originals remain source originals. Eight other captured records have no generation
metadata; a verified absence of other inventory defects is not claimed. Conditional
selection follows question_selection.rs for positive easy weighting; unavailable
learner history, policy and future allocated IDs prevent claiming the actual next
learner draw. Nothing was published and no database or engine content was changed.
