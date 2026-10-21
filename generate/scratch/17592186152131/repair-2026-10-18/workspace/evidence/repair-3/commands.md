Run from the supplied workspace with no database or publication access:

```sh
bash run-repair-checks.sh > evidence/repair-3/checks.log 2>&1
# Visually inspect render/question-001.png through question-009.png;
# record findings in visual-inspection.json.
/home/jake/Developer/Course_Academy/.venv/bin/python finalize_repair.py
```

`run-repair-checks.sh` contains the exact commands: `repair_checks.py build`, a seeded CLI batch, four calls to the shared `check_delivery.py`, `repair_checks.py delivered`, `finish_checks.py`, three batched native `check-engine` suites, and the unmodified application `render_preview.py`. Outputs stay in evidence/repair-3. The job Python is 3.13.5; no third-party runtime dependencies. `run-checks.sh` delegates to the current repair script.

The complete sequence above exited successfully after generator 1.2.0 and all implementation/check changes. Source fidelity, exact arithmetic, delivered conditional probes, native grading, deterministic relocation, count boundaries and renderer checks passed. All nine screenshots were subsequently inspected visually. `finalize_repair.py` links both directions of each of 168 same-bank target swaps to native acceptance of the current key and rejection of the former key. It compares the preserved repair-2 raw/delivered samples against repair-3 to reproduce the original avoid-4 defect (16/16 after delivery) and its repair (16/32).

The regression sample retains earlier seeds, adds review seed 92718, and adds seed 25 (first target-4 reachability found in seeds 0..29). Full square coverage is 336 bank configurations representing 23 numerical tasks; the 168 same-bank groups are paired decision assignments, not additional mathematical tasks. Every displayed square-practice base is correct and incorrect across its matching complete banks. All 336 configurations survive the actual shared delivery filter: 381 input records -> 362 accepted, 19 duplicate samples. Captured inventory basis: 3777. Native suites: 404 accepted/1617 rejected; delivered 474 accepted/1755 rejected; original delivered controls 9 accepted/36 rejected. No unresolved outcomes.

Generator rejection is examined separately: square practice admits 2 and 4; original source-bank degeneracies reject them only when replaying that profile. Four outward partner directions reject; the sampler chooses compatible values and uses the opposite direction if a batch has exhausted one direction. Full 126-instance capacity sampling succeeds; over-capacity and unsupported difficulty requests reject. The practice-bank arithmetic and every compatible direction are independently checked exactly.

Selection limitation: inspected engine/rust/question_selection.rs read-only. Learner history can remove questions; configured positive-weight bands use uniform hashed selection; unconfigured policies select the first candidate. Captured delivery cannot reproduce unknown learner history, actual weights, future database identities or publication. Existing indexed coverage and source evidence remain intact. No published images or database content were changed.
