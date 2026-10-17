# Strict fraction notation repair

The exact-KP reviewer captured the actual MathLive input control serializing typed `1/4` as `\frac14` and typed `3/4` as `\frac34`. Both were rejected against stored braced TeX answers when the prompt requested simplest form. Evidence is in `.local/generation/math/17592186054746-auto/review-2-policy-2-1f9300337b6137df/ui-input-render/input-probe.json` and `input-grading-results.json`.

The strict answer-form path now canonicalizes complete integer fractions from braced/unbraced TeX or slash notation. Each unbraced TeX argument consumes exactly one token; grouped multi-digit integers remain intact. Integer numerator/denominator values are compared without rational reduction or expression evaluation, so `2/8` still fails against `1/4`, and `0.25` still fails a required fraction answer. Existing decimal precision normalization remains intact.

The actual `learning::grade` regression reproduced the failure before the fix and verifies the actual UI spellings, mixed grouping, slash notation, signs, multi-digit boundaries, and unreduced/expression/decimal rejection after the fix. All 36 current learning-module tests pass in the isolated Cargo target.

Review-history files remain unchanged. Their grading inputs deliberately expected known erroneous rejections; copies under this evidence folder change only those documented expectations to acceptance. `fraction-form-input-provenance.json` binds each copied input to its original SHA256 and records the expectation changes (1 + 1 actual UI, 28 slash cases). This is regression evidence, not a revised independent review certificate.

`rebuild-fraction-form.py --target grader` compiles a staged executable, runs the fraction and existing decimal native smoke checks, then atomically replaces the shared grader. Build provenance is in `fraction-form-rebuild-grader.json`. No app restart, database access, source-question edit, or author-workspace edit is performed.

The parent may separately build the updated app without starting it:

```bash
python3 reference/generated/topic-17592186048470-2026-10-17/rebuild-fraction-form.py --target app
```
