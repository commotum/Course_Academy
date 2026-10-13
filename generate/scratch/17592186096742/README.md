# Repeated chain-rule generator

Registered script: `generate/scratch/17592186096742.py`. Stable generator identity is UUIDv5 of the existing KP UUID and `question-generator`; all generated question/field/answer UUIDs are deterministic and field-owned.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096742.py --difficulty all --count 5 --seed 1959 --format json
.venv/bin/python generate/scratch/17592186096742/validate.py
.venv/bin/python generate/scratch/17592186096742/replenish.py
```

The package supports easy, moderate and hard. Easy is an authored classification of two unrated linear-phase cubic trig-power families, with independently derived keys and separately authored missing solutions. Moderate and hard retain source labels. There are 20/44/11 bounded fresh parameter candidates, excluding originals. These are policy bounds, not claims that the mathematical families are finite. One fieldless hard source is preserved and excluded. The exponential-log zero-at-origin family is replay-only because base changes leave the evaluated derivative zero.

Eight complete source banks are replayed with exact prompts, all source option values, present canonical keys and present whole solutions. Validation independently parses printed functions, options, blank fragments and surrounding factors, composition assignments, all three component derivatives, chain products and evaluation stages; it tests actual learner grading through `learning::grade_field`. Original/variant comparisons are in review.md and review.json. No plots are required.

Replenishment uses the existing native inventory reader, EDB integration and deployed native preview. It takes api.lock through current-basis recheck, source comparison, preview, saved basis-guarded request, submission, exact-basis readback and final inventory. It retains original EDN and receipts under reference/replenishment/, uses :application/ca-engine, and checks all transaction datoms for scoped additive content changes. Source question identities/content, canonical example and learner history are preserved.

Verified replenishment: preparation basis 1960, committed/readback basis 1961. Added five easy, one moderate and three hard questions; current distinct available inventory is five at every supported level. All nine source questions and the canonical example are unchanged, no learner facts changed, and the final native inventory reports no remaining jobs for this KP. The exact transaction, guarded durable request, preview, receipt, verification and outcome are retained under `reference/replenishment/basis-1960/`.
