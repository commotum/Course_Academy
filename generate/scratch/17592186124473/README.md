# Graph interval invertibility draft

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124473.py --difficulty all --seed 31 --count 2 --format json
.venv/bin/python generate/scratch/17592186124473/validate.py
```

API: `generate_easy`, `generate_moderate`, `generate_hard`, or `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Only radio fields are supported, matching every source. Normal templates: easy `single_turn`; moderate `two_turns`, `jump_ranges`; hard `union_ranges`, `disconnected_ranges`, `plateau_interval`, `plateau_union`. Complete defaults use `authored_method`. Explicit input guards match sampling. Seed changes shuffle options without changing content identity.

Public original profiles are source IDs q-36039, q-36941, q-108667, q-108673, q-108791, q-108795, q-36002, q-36004, q-36008, q-36011, q-36061, q-36066, q-36934. Use its observed difficulty and `parameters={'x_shift':0}` to replay raw full prose/bank/raster evidence; x_shift -2..2 gives explicitly qualitative evidence translations. Every such profile is evidence-only/ineligible, because the original analytic formulas are underidentified and raw endpoint prose typos/global-largest ambiguity remain documented.

Normal templates are exact authored analytic plots. Easy is a missing-level design claim, anchored to the canonical/lesson route. Normal mathematical identities normalize coordinate translation, output reflection and common horizontal scaling; presentation IDs retain actual text, graph, full bank, worked solution, level and version. Source profile fingerprints deliberately cannot inflate normal diversity. Every independent checker treats the actual requested set/maximal criterion as part of answer eligibility.

Validation separates raw fidelity (13 complete banks, 65 choices), branch/domain mathematics, actual rendered PNG/label checks, strict guards and native radio grading. Native ID selection verifies engine compatibility; it does not replace displayed mathematics checks. See `validation.json`, `engine-results.json`, `review.md`, and `review.json`. Source anomalies and geometry limitations are explicit, never hidden as successful formula recovery. All work stops after step 7; no database transactions, registrations or engine changes.
