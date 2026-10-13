# Trigonometric parametric range generator

Local, frozen step-7 candidate. No EDB writes or registration.

```sh
.venv/bin/python generate/scratch/17592186087736/validate.py
.venv/bin/python generate/scratch/17592186087736.py --difficulty all --seed 5 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087736.py --difficulty moderate --template q-70523 --profile observed:q-70523 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters have exactly a,b,h,k and accept exact rational strings. Source replay cases use every original bank/profile. Normal radio defaults use complete authored method banks; observed residual banks remain explicit.

All levels keep full-period sine/cosine coordinate ranges. Hard is authored with both negative fractional scales and both nonzero fractional shifts, two inequality reversals and four rational endpoint additions. See `classification.md` for exact guards and curriculum rationale. `template-extraction.md` distinguishes defensible wrong operations from underidentified source expression patterns.

`validation.json` separates 16 source prompts/banks, 15 available exact solutions, 55 available source correct designations, and the one independently inferred designation/one authored missing solution. Native grading is `course_academy_engine::learning::grade_field`, using the shared memory-only harness. The validator parses actual displayed mathematics and every intermediate inequality, not just generation metadata. Review includes every original, source replay and generated profile plus at least two examples per level. No plots.
