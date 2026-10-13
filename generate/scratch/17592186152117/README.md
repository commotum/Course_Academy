# Single-variable polynomial LCM generator

Script: `generate/scratch/17592186152117.py`. Complete local E/M/H generator; source snapshots are from math basis1356. Exactly two positive-content polynomials with unequal powers of one visible common monic binomial. Integer content is retained: LCM(9B^4,12B^2)=36B^4.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186152117.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186152117.py --difficulty hard --profile observed_q-76457 --format json
.venv/bin/python generate/scratch/17592186152117/validate.py
```

`source.json` preserves the captured wrapper; `source-cases.json` includes raw source records, exact parameters and public replay profiles. `observed_q-222016` and `observed_q-76460` preserve absent keys/solutions/ratings. `derived_<id>` fills these omissions with independently verified, clearly authored answers and solutions. Moderate's missing-level definition and normal complete radio bank are authored same-method extensions. Explicit replay banks remain separate. All five captured solutions, all seven prompts and all14 available source choice values are exact; five available correct designations match, two omissions remain honest omissions.

`classification.md`, `template-extraction.md`, and `plot-spec.md` describe scope and evidence. `review.md` / `review.json` show originals, per-profile variants, completions, and at least two instances of each layout at each level. `validation.json` separates source fidelity, 600 sampled displayed-math checks, invalid-input/identity checks, and real `learning::grade_field` tests. Expanded, reordered and uncollected equivalent polynomials are accepted; monic normalization and wrong scalar multiples are rejected. Python `**` is not learner math notation; tests use `^`.

No plots, database access, transactions, shared writes or registration. Source collection order is not used to derive the curriculum route. Frozen hashes and runtime versions are recorded in `frozen.json`; independent parent QA is still required.
