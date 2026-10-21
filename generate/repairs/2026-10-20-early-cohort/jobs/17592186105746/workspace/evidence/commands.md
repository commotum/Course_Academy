All commands were run from the supplied workspace. No publication, database operation, engine edit, image upload, or other job edit was performed.

```bash
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746

"$PY" checks/repair_checks.py
# PASS: 17 source replays; 51 controlled pairs; 202 independently checked records.
# Covers both retained finding IDs; each source profile's default sampler also
# produces both decisions with and without a non-original rhs_scale. The
# original review eight-scale probe passes. All complete mathematical banks replay.
# Saved metadata replays each prompt, bank and worked solution.

"$PY" 17592186105746.py --difficulty easy --seed 7331 --count 5 --format json --output evidence/batch.json

"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# PASS: 54 input, 54 accepted, 0 rejected/deduplicated at captured basis 5364.
# These contain 48 distinct mathematical tasks; source profiles are not counted
# as semantic variation when their supplied equations differ only by row scaling.

"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# PASS: all five accepted, all five semantically distinct.

"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
# PASS: 202 correct responses accepted; 808 wrong choices rejected; no unresolved checks.

"$PY" checks/delivery_checks.py
# PASS: all controlled cue groups have both decisions before and after delivery;
# original coefficient-only strategy 27/54 on controlled records, 2/5 on the batch.
# The small default-constructor sample happens to score 19/24 for the old strategy
# (16 inconsistent, 8 consistent). This skew is retained, not hidden or resampled.
# It is not a fixed per-profile rule: controlled pairs and normal seeds 0/1 in
# every profile independently demonstrate both decisions. No arbitrary balancing
# or filtering by answer was introduced. Inventory has 17 original source IDs,
# and a verified absence of stored generated records at the captured basis.

"$PY" checks/package_checks.py
# PASS: isolated declared-runtime-only relocation; five questions each in easy
# and moderate, deterministic CLI replay, invalid parameters rejected, no files
# generated inside runtime. Prepares native cases for actual delivered records.

"$REPO/generate/runs/current/check-engine" evidence/grader-delivered-input.json evidence/grader-delivered-results.json
# PASS: 7 correct responses accepted; 28 alternatives rejected after delivery.

"$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# PASS: five actual UI renders. Screenshots question-001.png through
# question-005.png were visually inspected; see visual-review.json.
```

Before implementation, an inline Python import of the original workspace entrypoint reproduced the exact feedback:

```python
g.generate('easy', 7331, 'q-20964', {'rhs_scale': 1})
# ValueError('Template difficulty mismatch')
g.generate('easy', 7331, 'q-42157', {'rhs_scale': 2})
# Complete original record retained in baseline-reproduction.json:
# x-6y=4; -4x+24y=-20, keyed No solution.
# All eight supported RHS scales of that profile were also keyed No solution.
```

The current executable regression repeats the old nonzero-scale case and tests the exact new relevant change: x-6y=2 stays fixed; second RHS -10 -> -8 changes the key from No solution to x=2+6y, y free, while preserving the entire mathematical bank. It also tests irrelevant nonzero-residual changes that preserve No solution. Source q-20964 is compared against the independent supplied capture, not merely the generator's expanded source snapshot.

Final audit repair: rhs_scale=1 alone retains exact source replay; other scale controls now choose consistency independently. The old scale-2 matrix is reproduced explicitly with `rhs_scale=2, second_rhs=-20`. An isolated bank-shuffle seed fixes generation-metadata replay. After these changes, all commands above were rerun and all five new screenshots were visually reinspected. The updated regression count is 202 records, including 51 controlled pairs, all 17 source cases, both default/scaled decisions in every source profile, and the exact eight-scale review probe.
