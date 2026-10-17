# Finding the Number of Solutions to a System

Validated generator using source evidence at basis 1356, rechecked unchanged against live basis 2486. The generator itself performs no database I/O; `replenish.py` uses the existing database integration and application lock for additive replenishment.

```sh
.venv/bin/python generate/scratch/17592186073776.py --difficulty all --seed 0 --count 2
.venv/bin/python generate/scratch/17592186073776.py --difficulty hard --format json
.venv/bin/python generate/scratch/17592186073776/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Only the observed select type is supported. Explicit six-integer coefficient dictionaries use a,b,c,d,e,f for ax+by=c, dx+ey=f. Standard form is easy/moderate; y-first zero-RHS form is hard. Level claims and arithmetic guards are authored, because no captured practice question has a difficulty.

Profiles `raw_211984`, `raw_237043`, `raw_237046` preserve all raw missing-key conditions and exact original prompts at their source parameters. They are evidence-only and omit correct refs/solution/difficulty. Use `source-cases.json` to replay them. Profile `counts` is eligible normal output: same complete textual bank, inferred keys and authored elimination solutions, plus escaped literal system-brace presentation.

Validation independently parses the displayed system and every solution stage, checks coefficient/augmented ranks, all answer concepts, source complete banks/omissions, identity/aliases, bounds, format, generated family/outcome coverage, and corruption regressions. Native `course_academy_engine::learning::grade_field` checks all choices using memory-only fixtures. `validation.json` distinguishes zero present source keys/solutions from authored completion, and reports empirical canonical task counts honestly. Review includes all originals, inferred completions, changed variants, and at least two variants per level. No practice plots are needed.

Durable replenishment: `.venv/bin/python generate/scratch/17592186073776/replenish.py`. This validates every selected instance, checks current/historical availability and identity collisions, previews with installed validation specs, retains exact basis-guarded requests, and verifies additive scoped datoms/readback before saving the job result. `capabilities.json` and `release.json` record supported levels and frozen hashes.

## Current system display repair (2026-10-16)

The registered generator now constructs systems with the shared `system_tex` helper: separate equation rows, explicit equation-label columns, and a single operation bar where applicable. Whole-equation multiplication stays grouped. The change preserves sampling, difficulty, mathematical task fingerprints, complete answer banks, and correct keys. Original source snapshots and raw replay prompts remain historical evidence.

Run the current presentation regression and native grading checks from the repository root:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/verify.py
```

That harness compares retained pre-repair generators with current output across every supported template and difficulty, invokes the historical mathematical validators on the baseline, checks arithmetic and answer equivalence, and grades current output with the native engine. It avoids the historical validators' semicolon-only display parsers. Current render evidence is in `reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/`.
