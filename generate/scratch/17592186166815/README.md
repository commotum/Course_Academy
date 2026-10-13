# First-order IVP recognition generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186166815/validate.py
.venv/bin/python generate/scratch/17592186166815.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186166815.py --difficulty easy --template source_q-96987 --profile observed_domain_repair --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None,
parameters=None, profile=None)` and `generate_easy`, `generate_moderate`,
`generate_hard`. Source replay recipes and original parameters are in
`source-cases.json`; use its `bank_profile` as `profile`. `observed_raw` is always
evidence-only and defaults to its original parameters when omitted.
`observed_regular` samples complete changed-parameter recipes.
`observed_domain_repair` is limited to q-96987. Defaults are the authored
recognition templates with the original three-checkbox layout.

All 11 raw prompts and fixed solutions, 33 full field banks, 66 choice values,
and 33 designations are matched. One raw domain-wording issue is isolated and
minimally repaired. Missing moderate/hard levels are authored. Meaningful finite
catalogs are 9/12/12 category multisets, with 36/54/54 ordered display layouts;
incidental numeric changes and equation order do not inflate semantic counts.
See `classification.md`, `template-extraction.md`, `review.md`, and
`validation.json` for the boundaries and exact frozen test results.

The validator reads displayed ODEs/initial conditions independently and calls
the real `learning::grade_field` in memory. `engine-input.json` and
`engine-report.json` preserve all native checks. No EDB transactions, engine
changes, plots, or commits are performed by the validator or generator.

`replenish.py` implements steps 8–9 through the existing EDB integration. It
holds the application's `api.lock` through the current inventory read, guarded
submission and exact-basis readback, retaining the request and receipt under
`reference/replenishment/`. Re-running it recovers the saved request before
creating new intent.

The review job based on 1831 was rechecked at 2016 and committed at **2017**.
Existing topic inventory supplied 22 easy and 10 moderate questions; five
distinct hard category multisets were generated, independently checked, graded
and committed. The verified topic pool is 22/10/5 with no remaining shortage.
All eleven original practice questions and the canonical example are unchanged;
the receipt contains only additive content and generator-registration facts.

Registered generator UUID: `c24b0381-d948-51ca-bb46-4fb8e8e5ca18`; script:
`generate/scratch/17592186166815.py`. Attribution is `:application/ca-engine`.
The exact request, receipt and verification are in
`reference/replenishment/basis-2016/`; `capabilities.json` retains the finite
catalog bounds. Incidental numbers, system ordering and choice ordering never
increase the distinct task count.
