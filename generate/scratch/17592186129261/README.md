# Given transformation area generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186129261/validate.py
.venv/bin/python generate/scratch/17592186129261.py --difficulty all --seed 7 --count 2 --format json
```

Scope: given-map boundary mapping, determinant, reciprocal determinant, scalar area; five-choice radio only. All three levels implemented. Hard is explicitly authored scaled cubic reciprocal, absent from source ratings. Moderate quotient and easy legacy have authored ratings because captures omit them. Complete historical banks remain public `observed-*` profiles with evidence-only flags and raw omissions; defaults use method-derived complete banks.

Four source banks, twenty values, two observed correct refs, two absent refs; source prompt/solution/presence fidelity is tested separately from normal mathematics and native grading. Source easy quadrant inconsistency and moderate sign/differential errors are documented in extraction; raw evidence is ineligible for learning. Normal records repair them. Native fixtures use the actual `learning::grade_field`, no DB. Initial generator validation made no database writes. See the verified replenishment below for its subsequent registration and additive content commit.

Review: `review.json` and `review.md`; exact raw captures: `source.json`; replay parameters: `source-cases.json`; machine evidence: `validation.json`, `engine-report.json`, render PNG/sidecars and `plot-review.png`.

## Verified replenishment, 2026-10-15

`replenish.py` reuses the application EDB reader, contributor, native preview, durable request handling, content-addressed image store and learner grader. It holds `.local/learning/requests/math/api.lock` from fresh inventory through receipt/readback. The exact request and receipts are under `reference/replenishment/basis-2660/`. Commit **2660 → 2661** added **11** distinct questions: 4 easy, 2 moderate, 5 authored hard. Exact-basis readback verified five mathematically validated, gradable, unseen/unreserved tasks per level, generator UUID `fa49723a-10c7-5b96-9133-32d3b1b78e99`, preservation of all seven previous questions and canonical example, and no learner/history changes.

`reference/replenishment/current-classification.md` reconciles all seven current sources, including three newly captured families. `capabilities.json` retains their bounded sampling exclusions, the incomplete unrated source and two source quadrant/key errors. No source repair is included in this commit. `reference/replenishment/basis-2660/outcome.json` and the requested job `.result` contain the verified outcome and evidence links.
