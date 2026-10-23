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

## Follow-up repair f1db9b4f2ce0efa72b7b (2026-10-22)

All paths below use the same W and repository working directory defined above.

- Exact latest failure generated at seed 66081, reciprocal_exp_root_blank, a=b=c=1, u=2; visible differentiation gives 8*sqrt(5)/(25*sqrt(e)). Exact command and output: repeated-exp-before-execution.json. Exit 1 for repeated quarter factors. No historical batch modified.
- Before editing, the earlier check_fractional_exp.py passed 8 fresh and 8 delivered records. After adding the new strict acceptance and wrong-answer controls, `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python "$W/check_fractional_exp.py" > "$W/repeated-regression-before.log" 2>&1` exited 1 on the latest failure with the old native harness.
- `CARGO_TARGET_DIR="$PWD/$W/build" cargo test --offline --lib symbolic::tests > "$W/repeated-symbolic-tests.log" 2>&1`: exit 0, 18 passed, including repeated factors/powers across degrees 2–8, signed/reduced/whole exponents, wrong answers and domain guards.
- `CARGO_TARGET_DIR="$PWD/$W/build" cargo build --offline --lib > "$W/repeated-engine-build.log" 2>&1`: exit 0. Exact native harness rebuild command/result: repeated-harness-rebuild.json. Patch: repeated-engine-repair.patch; source/harness hashes: repeated-engine-binding.json.
- Exact same native input after rebuilding: repeated-exp-after-execution.json, exit 0; repeated-exp-after-result.json confirms acceptance.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python "$W/check_fractional_exp.py" > "$W/repeated-regression-after.log" 2>&1`: exit 0, 8 fresh and 8 delivered records. Both history IDs map to this executable in repair-regressions.json. Native response details: regression-grader-result.json and regression-delivered-grader-result.json.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python "$W/validate_current.py" > "$W/repeated-current-validation.log" 2>&1`: exit 0. Fresh requested CLI uses --difficulty easy --count 5 --seed 3175644378 --format json, explicit workspace/assets output, and deterministic replay. Five batch and 22 probe records survive shared delivery; visible math, real grading, controlled target/translation changes and per-template shortcut checks pass. Exact subprocess commands: regression-commands.jsonl; CLI command: cli-execution.json; samples: prospective-batch.json and probes.json.
- `PYTHONDONTWRITEBYTECODE=1 python3 generate/pipeline/render_preview.py --input "$W/render-records.json" --output "$W/render-repeated" --asset-root "$W/assets" --math-root /media/jake/SSD/EDB/math > "$W/repeated-render.log" 2>&1`: exit 0, 3 rendered and visually inspected; repeated-render-inspection.json.
- `git diff --check -- engine/rust/symbolic.rs`: exit 0. Package pins match installed versions and runtime files match runtime-before.json. Retained prior source replay, relocation, and full scope evidence applies to unchanged package.

No images published, database writes, service restarts or other job edits. All author evidence is under W; only the explicitly authorized engine repair and grader rebuild occurred outside W.
