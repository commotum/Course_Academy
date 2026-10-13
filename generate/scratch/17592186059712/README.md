# Column-vector generator

Local steps 3–7 only; frozen `math` basis 1356. No database writes/registration, shared engine changes or commits.

```sh
.venv/bin/python generate/scratch/17592186059712/validate.py
.venv/bin/python generate/scratch/17592186059712.py --difficulty all --seed 20 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186059712.py --difficulty moderate --profile raw-q-18040 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are exact integer-vector/scalar dictionaries, documented in `source-cases.json`; invalid explicit parameters raise rather than change silently. Template names and bounds are in classification/extraction and the script. Normal profile is `authored-component-operations`. `raw-<source-id>` reproduces all original attribute omissions; `completed-<source-id>` adds independently inferred assessment fields/refs where missing. Both historical replay modes are evidence-only, never default learning output. Raw original unrated questions retain absent difficulty.

Validation covers 450 default records, all four raw source cases and their changed-parameter variants, four completions and eight additional source-mask variants. Native grader checks all five options on 450 normal records plus four completions: 2,270 checks, 454 accepted/1,816 rejected, zero unresolved. Radio selection does not prove mathematical correctness; the independent printed-token validator establishes each row and complete authored choice bank. All four prompts, both existing solutions, both existing banks (10 choices) and optional-attribute presence match exactly. Missing original refs/fields/labels are explicitly documented and never counted as recovered matches.

`review.md`/`review.json` label captured originals, raw changed evidence, inferred completions, and generated variants, with at least two examples at every level and for every observed mask. `validation.json` holds exact runtime versions, native binary hash and finite meaningful witness counts. No plots. Easy and hard are authored scope extensions; opaque historical wrong-operation intent remains unknown.
