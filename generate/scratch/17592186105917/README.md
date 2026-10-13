# Calculating a Scalar Projection Using Components

Local draft only. Stops after generator validation; no database writes.

```sh
.venv/bin/python generate/scratch/17592186105917.py --difficulty all --count 2 --seed 0 --format markdown
.venv/bin/python generate/scratch/17592186105917/validate.py
.venv/bin/python generate/scratch/17592186105917/domain_audit.py
```

The public API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, and `generate_hard`.

Normal defaults choose integer/radical single-projection easy families, sum/difference moderate families with integer dot product and norms, and authored hard sum/difference families with an irrational dot product and two distinct nonsquare norms. They use supported radio/blank shapes and complete method-derived five-option banks. Explicit parameters receive the same difficulty/domain/collision guards as samples.

All 24 captured source recipes remain public through `template='q-...'`, `profile='observed:q-...'`, and the source-case level. They render parameterized component/ordered-arithmetic masks. Their complete historical banks use documented expression-ratio profiles where mistake intent is underdetermined; **all observed profiles are evidence-only and ineligible for learning**, including changed examples. This intentionally conservative policy does not claim recovered distractor intent. Default practice uses assessed-method operations instead. The raw unrated source keeps its missing difficulty, correct designation, and solution; its mathematically derived answer is 8/3.

`recipes.json` is required runtime data, not a literal source-answer lookup: component masks and stage renderers recompute every actual solution row; source answers are whole-expression parameterized ratio recipes. `extract.py` documents and reproduces extraction from the frozen source wrapper. Source replay preserves present/absent schema attributes, source notation, prose, arithmetic stages and values. It creates new owned UUIDs and converts captured enum maps/correct objects to the established local enum-string/lookup-ref shape; database identity keys are deliberately omitted.

`review.md` has all originals, changed instances for all historical banks, and labeled authored E/M/H examples. `validation.json` reports source fidelity separately from mathematical correctness and actual native grading. `domain-audit.json` enumerates conservative lower bounds without counting common positive vector scaling, names, bank variants, or option order. No component-question plots are present or needed; scalar-projection lesson illustrations belong to surrounding tutorials/sibling perpendicular-vector content.
