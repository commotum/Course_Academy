# Form-sensitive decimal grading repair

`compare_math_in_context` intentionally compares answer form when a question requests rounding or a particular number of decimal places. Previously that strict normalized-text comparison rejected equivalent decimal numeral spellings.

`normalize_answer_form` now applies only to a complete decimal numeral with optional sign, zero or more ASCII digits before one decimal point, and one or more ASCII digits after it. It removes an optional positive sign, removes redundant integer leading zeroes, and supplies zero for an omitted/all-zero integer part. It preserves a minus sign and every fractional digit. Fractions, arithmetic, scientific notation, unsupported expressions, and wrong precision are not made equivalent.

The actual `learning::grade` regression verifies both directions, positive/negative spellings, omitted and redundant integer zeroes, nonzero integer parts, and rejection of wrong value, sign, or fractional precision. All 32 learning-module tests pass using `/tmp/course-academy-leading-dot-tests`, including existing exact-answer and rounding-form tests.

The shared grading harness is rebuilt to a temporary sibling executable, checked through its actual `grade_field` entry point, then atomically renamed. `leading-dot-rebuild-grader.json` records source/library/binary hashes, compiler versions, command, times, and smoke input/result hashes. Intermediate observed failures and build provenance were retained separately.

No database operations, question wording edits, author workspace changes, app rebuild, or app restart were performed by this repair. The reviewer files are read-only inputs; replay outputs are written in this evidence folder.

## Commands

Shared reviewer grader (already rebuilt by this task):

```bash
python3 reference/generated/topic-17592186048470-2026-10-17/rebuild-leading-dot.py --target grader
```

Build a versioned app engine for later parent-owned deployment, without restarting the running application:

```bash
python3 reference/generated/topic-17592186048470-2026-10-17/rebuild-leading-dot.py --target app
```

This delegates to the repository `build_learning` helper, which uses `cargo build --release --lib --offline` and atomic staging for the native app binary. The app continues using its existing executable until separately restarted.
