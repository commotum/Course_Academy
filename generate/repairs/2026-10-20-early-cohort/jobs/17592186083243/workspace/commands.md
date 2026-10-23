# Reproduction and validation

Run from `/home/jake/Developer/Course_Academy`. Let `W=generate/repairs/2026-10-20-early-cohort/jobs/17592186083243/workspace`.

- Initial exact reproduction: `generate/runs/current/check-engine generate/repairs/2026-10-20-early-cohort/jobs/17592186083243/review-0-policy-2-da51d3ee0942346e/minimal-grader-input.json "$W/before-grader-result.json"`. Exit 1, valid fractional exp unresolved. See before-grader-execution.json; the harness does not write a report on failure.
- Current-generator retained regression: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python "$W/check_fractional_exp.py"`. Verified exit 1 with old harness (regression-before.log), exit 0 with rebuilt harness (regression-after.log). Complete subprocess commands and actual outputs are in regression-commands.jsonl. Tests do not mutate runtime package files.
- Targeted engine test: `CARGO_TARGET_DIR="$W/build" cargo test --offline --lib symbolic::tests::fractional_exp_constants_share_exact_power_form`. See engine-test.log.
- Affected engine suite: `CARGO_TARGET_DIR="$W/build" cargo test --offline --lib symbolic::tests`. All 17 pass; symbolic-tests.log.
- Library rebuild: `CARGO_TARGET_DIR="$W/build" cargo build --offline --lib`. See engine-build.log. Exact rustc harness command and status are in harness-rebuild.json. The shared executable generate/runs/current/check-engine was rebuilt, not substituted with a test grader. Binding hashes are in engine-binding.json.
- Exact historical reproduction after repair: retained-minimal-execution.json records the command and success: 3 accepted, 2 rejected. Its result is retained-minimal-result.json.
- Current CLI/batch/controlled variation: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python "$W/validate_current.py"`. Current output, independently parsed math, strict grading and shared delivery filtering all pass. The script runs `generator.py --difficulty easy --count 5 --seed 3175644378 --format json` twice with COURSE_ACADEMY_GENERATOR_OUTPUT_DIR under workspace/assets; cli-execution.json records replay equality. It does not read or alter the retained samples.json.
- Actual UI: `python3 generate/pipeline/render_preview.py --input "$W/render-records.json" --output "$W/render" --asset-root "$W/assets" --math-root /media/jake/SSD/EDB/math`. All three rendered; screenshots visually inspected (render-inspection.json).

No database writes, publication, live-service restarts, or other job edits. Only engine/rust/symbolic.rs and the explicitly authorized shared harness rebuild are outside this workspace. Runtime package files are byte-for-byte unchanged.
