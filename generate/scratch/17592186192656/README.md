# Full first-variable elimination generator

Run validation with the existing real native grader:

```sh
.venv/bin/python generate/scratch/17592186192656/validate.py
.venv/bin/python generate/scratch/17592186192656.py --difficulty all --seed 2 --count 2 --format json
.venv/bin/python generate/scratch/17592186192656.py --difficulty easy --profile raw-q-208816
.venv/bin/python generate/scratch/17592186192656.py --difficulty moderate --profile raw-q-18787
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Layouts `radio_solution` and `blank_solution` both participate in every normal difficulty sampler. Explicit invalid parameters/profile/layout requests fail rather than resample. Raw originals are evidence only; field/answer enums use local ident strings, and every literal source value/layout and absent choice/rating/ref/solution attribute is preserved. The completed opaque historical radio bank is also evidence only. Normal choices use a separate complete method-error bank. Every normal record is an explicitly authored completion with native-supported radio/two-scalar-blank fields.

Scope: signed integer two-variable linear systems, one integer scaling to eliminate the first variable, solve the other variable and back-substitute for the first. No second-variable elimination, two-row scaling, singular systems or database transactions. All level labels are authored design claims because both captured originals are unrated. All answer math is exact.

`source.json` preserves basis1356 provenance. `source-cases.json` describes every public replay. `source-fidelity.json` reports raw attribute/bank fidelity after exact enum projection separately from absent designation/solution evidence. `review.md`/`review.json` contain both originals, supported completions, changed-parameter evidence profiles, and at least two normal variants per layout per level. `validation.json` reports actual native results and independent displayed-system/bank/stage/prose checks; `engine-input.json` and `engine-report.json` retain fixtures/results. Runtime versions and native binary hash are captured.

Unresolved historical interpretation: four observed wrong tuples lack defensible error operations; their explicit recipe patterns are retained without a learner-default claim. Source braces and blank punctuation are malformed in raw evidence; normal supported completions repair presentation. Missing source refs/ratings/solutions cannot be counted as recovered data. No registration/preparation work occurs after step7.

Displayed and independently primitive-normalized rows must both satisfy their authored level bounds. Global or individual factors cannot promote an easy task to moderate/hard. Same-level row factors remain allowed but deduplicate canonically; learner solutions gain no preliminary simplification step.

Normal authored radio banks retain their five method-derived recipes and reject the whole instance unless at least one wrong tuple is entirely integer, preventing selection by the correct pair's integer form alone. Rational wrong tuples can remain; this is an authored bank extension. `integer-shortcut-regression.json` contains four rejected parent parameter sets and proofs that their blank instances remain eligible.

## Inventory registration and live source refresh

`replenish.py` uses the existing EDB integration and application contributor, obtains `api.lock`, captures current inventory, deduplicates mathematical tasks, tests selected records with the native engine, previews with deployed validation predicates, persists exact basis-guarded intent, submits, and verifies exact receipt-basis readback. `freeze.json` records the registered UUID and executable/validation hashes. The script falls back to the repository Python environment when the application's ordinary Python lacks SymPy.

Current source evidence at basis 2154 updates the radio original to easy and adds a moderate two-blank source. Those captured ratings supersede the old source-label suggestions. `current-source-validation.json` and its native report verify their complete banks/fields and worked arithmetic. New moderate sampling uses multipliers 3–4. Exact fidelity to the newly captured aligned b=13 blank template is outside this generator's narrower policy; that valid source still contributes to inventory. Hard remains an authored, source-anchored workload band.

## Current system display repair (2026-10-16)

The registered generator now constructs systems with the shared `system_tex` helper: separate equation rows, explicit equation-label columns, and a single operation bar where applicable. Whole-equation multiplication stays grouped. The change preserves sampling, difficulty, mathematical task fingerprints, complete answer banks, and correct keys. Original source snapshots and raw replay prompts remain historical evidence.

Run the current presentation regression and native grading checks from the repository root:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/verify.py
```

That harness compares retained pre-repair generators with current output across every supported template and difficulty, invokes the historical mathematical validators on the baseline, checks arithmetic and answer equivalence, and grades current output with the native engine. It avoids the historical validators' semicolon-only display parsers. Current render evidence is in `reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/`.
