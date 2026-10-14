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

The generator itself performs no database operations and needs no plots. Source collection order is not used to derive the curriculum route. Frozen hashes, runtime versions, and independent primary-agent QA are recorded in `frozen.json`.

`replenish.py` uses the existing application database integration, locks `.local/learning/requests/math/api.lock`, and retains exact guarded requests and verified receipts under `reference/replenishment/`. It reuses the registered generator UUID from `registration.json`. Basis 2261 → 2262 added 3 easy, 5 authored moderate, and 2 hard questions, leaving five fresh distinct tasks at every supported level. All seven captured sources and learner history were preserved. The two incomplete unrated sources remain excluded. The native inventory recheck has no remaining jobs for this KP.
