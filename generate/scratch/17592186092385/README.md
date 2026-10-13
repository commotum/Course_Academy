# Normal-line intercept generator

Repository script: `generate/scratch/17592186092385.py`. KP UUID:
`3ba61258-92a9-511e-891f-9e6adce2edb0`. Its deterministic generator UUID is
reused across runs; current registration is rechecked before submission.

Run `.venv/bin/python generate/scratch/17592186092385.py --difficulty easy
--count 5 --seed 0 --format json` (on one line). Moderate is also supported.
Hard fails explicitly. Requesting more than a band's finite catalog returns
only the available distinct catalog; replenishment documents any shortfall.

`validate.py` replays every supported source bank and original Markdown, checks
all 84 mathematical tasks and displayed solution results, and exercises the
actual application grader, including equivalent and incorrect blank responses
for both coordinates. `validation.json` freezes script, validator and source
hashes; `preview.json` and `review.md` retain reproducible variants for review.
Dependencies and domains are recorded with each instance. Seeds change traversal
order, not mathematical identity. SymPy performs exact calculations.

`replenish.py` uses the existing EDB transport and contributor
`:application/ca-engine`, holds the application `api.lock` from fresh inventory
through commit/readback, applies the expected-basis guard, and retains exact
intent and receipts. It only adds validated questions and generator registration
for this KP. Existing source questions, canonical example and learner history
are preserved and checked. See `reference/replenishment/` for preparation,
previews, request keys, complete EDN, receipts, attribution and exact-basis
verification. No application or scheduler code is changed.
