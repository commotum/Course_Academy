# Eliminating the Second Variable

The generator produces local previews and performs no database writes. `replenish.py` handles stages 8–9 through the existing application EDB integration, under `api.lock`, with retained exact requests, basis guards, and verified receipts.

```bash
.venv/bin/python generate/scratch/17592186192655/validate.py
.venv/bin/python generate/scratch/17592186192655.py --difficulty all --seed 8 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186192655.py --difficulty easy --template compact --profile raw-q-210947 --parameters '{"a1":9,"b1":10,"c1":3,"a2":-2,"b2":-1,"c2":3,"variables":["x","y"]}' --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Two paragraph masks; paired select fields; supported normal complete profiles `difference` and `coefficient` (nonunit only). Raw and completed historical profiles are explicit parameterized evidence-only requests; the raw profile preserves missing rating/solution/correct refs. See `source-cases.json` for both original parameter sets. Explicit invalid parameters fail without resampling.

All three normal levels are authored within one integer scaling/addition operation; no solving, extra row operations or other KP branches. `classification.md` distinguishes the source evidence from difficulty design, `template-extraction.md` maps all components/banks and scopes finite meaningful variety, `review.md`/`review.json` contain raw originals, supported completions, changed public replay profiles and all-level normal examples. The raw original system glyphs are malformed TeX and ineligible; normalized normal presentation escapes the glyph, and the canonical marked-row stray parenthesis is repaired. Source1 historical wrong-value intention remains opaque and evidence-only.

Validation independently reads displayed prompt and worked math, checks entire paired banks, omission parity, source fidelity, native grade outcomes, content/task identities, complete finite target domains, actual enum strings and operative solution stages. `validation.json` separates zero original correct designation/solution denominators from authored inference and native grading. Engine source and executable are read-only shared fixtures at `generate/runs/current/check-engine.rs` and `check-engine`; no engine changes are made.

## Verified replenishment

`reference/replenishment/basis-2149/` retains the preparation, source comparison, mathematical task deduplication, native grading, speculative preview, exact commit intent, durable receipt, and readback. Basis **2149 → 2150** added **5 easy, 5 moderate, and 5 hard** questions and registered generator UUID `835d8836-7a8d-5bd9-ad81-8fb2ebfafdee` at `generate/scratch/17592186192655.py`.

All 15 selected instances passed displayed-equation and worked-solution checks. Actual learner grading accepted all 30 correct field selections and rejected all 60 incorrect selections, both before commit and on exact-basis readback. Both incomplete source questions and the canonical example remain unchanged; only additive facts for this KP and its new generated entities were committed. Available inventory is five distinct tasks per authored level, with no remaining KP jobs.

Finite task domains remain bounded as documented in `template-extraction.md`; exhausted tasks cannot be replenished by incidental coefficients, variables, bank profiles, seed, or option ordering. An exhausted domain leaves an explicit finite-limit outcome. The generator's difficulty labels are authored workload classifications, not recovered source labels.

## Current system display repair (2026-10-16)

The registered generator now constructs systems with the shared `system_tex` helper: separate equation rows, explicit equation-label columns, and a single operation bar where applicable. Whole-equation multiplication stays grouped. The change preserves sampling, difficulty, mathematical task fingerprints, complete answer banks, and correct keys. Original source snapshots and raw replay prompts remain historical evidence.

Run the current presentation regression and native grading checks from the repository root:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/verify.py
```

That harness compares retained pre-repair generators with current output across every supported template and difficulty, invokes the historical mathematical validators on the baseline, checks arithmetic and answer equivalence, and grades current output with the native engine. It avoids the historical validators' semicolon-only display parsers. Current render evidence is in `reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/`.
