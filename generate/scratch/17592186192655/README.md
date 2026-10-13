# Eliminating the Second Variable

Local review generator only; stops after step7, performs no database writes.

```bash
.venv/bin/python generate/scratch/17592186192655/validate.py
.venv/bin/python generate/scratch/17592186192655.py --difficulty all --seed 8 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186192655.py --difficulty easy --template compact --profile raw-q-210947 --parameters '{"a1":9,"b1":10,"c1":3,"a2":-2,"b2":-1,"c2":3,"variables":["x","y"]}' --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Two paragraph masks; paired select fields; supported normal complete profiles `difference` and `coefficient` (nonunit only). Raw and completed historical profiles are explicit parameterized evidence-only requests; the raw profile preserves missing rating/solution/correct refs. See `source-cases.json` for both original parameter sets. Explicit invalid parameters fail without resampling.

All three normal levels are authored within one integer scaling/addition operation; no solving, extra row operations or other KP branches. `classification.md` distinguishes the source evidence from difficulty design, `template-extraction.md` maps all components/banks and scopes finite meaningful variety, `review.md`/`review.json` contain raw originals, supported completions, changed public replay profiles and all-level normal examples. The raw original system glyphs are malformed TeX and ineligible; normalized normal presentation escapes the glyph, and the canonical marked-row stray parenthesis is repaired. Source1 historical wrong-value intention remains opaque and evidence-only.

Validation independently reads displayed prompt and worked math, checks entire paired banks, omission parity, source fidelity, native grade outcomes, content/task identities, complete finite target domains, actual enum strings and operative solution stages. `validation.json` separates zero original correct designation/solution denominators from authored inference and native grading. Engine source and executable are read-only shared fixtures at `generate/runs/current/check-engine.rs` and `check-engine`; no engine changes are made.
