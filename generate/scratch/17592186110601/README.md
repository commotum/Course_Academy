# Perpendicular unknown-parameter generator

Local steps 3–7 only. Generate E/M/H peers with 0/1/2 slope-intercept conversions. Ten source prompts and all captured solutions are preserved at original parameters; q-72548 appends its supported blank placeholder. Three unrated missing-answer blanks and one fieldless moderate question have explicitly authored repairs; their absent designations are excluded from fidelity denominators.

```sh
.venv/bin/python generate/scratch/17592186110601/validate.py
.venv/bin/python generate/scratch/17592186110601.py --difficulty all --seed 42 --count 2 --format markdown
```

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard` return the local question shape. Source replay is defined by `source-cases.json`. Source IDs select fully parameterized prose/layout recipes, never literal-answer lookups. Normal radio output uses whole authored banks. `--profile observed` selects a complete observed bank and is explicitly restricted to evidence replay because some distractor intentions are underdetermined.

Coefficients are integers with absolute value ≤24; the easy known rational slope may have denominator ≤12. Random coefficients use 2–12 and intercept magnitudes 1–12; easy rational known slopes use signed numerators 1–6 and denominators 2–9. Exact source values remain eligible. Family-specific sign, unit-coefficient and zero-constant guards preserve original workload on explicit input as well as sampling. Required coefficients are nonzero. These bounds preserve linear parameter isolation without roots, systems, graph construction or vertical-slope branches.

A complete bank is selected before calculation. All options must be finite exact rational and pairwise different; a collision rejects the whole instance. Seeds cannot change identity for fixed parameters/template/profile. Mathematical identity is the normalized perpendicular constraint coefficient; incidental intercepts, equation scaling, names, answer banks and layout are excluded. Presentation identity additionally includes all learner-facing prompt, solution, level, field and bank content.

Read `classification.md`, `template-extraction.md`, `review.md` and `validation.json` for evidence and limitations. `review.json` includes two authored variants of every source renderer and two changed-parameter variants of every observed radio bank. Native engine fixtures and report are retained separately. No database writes or registration occurred; no plots are needed.
