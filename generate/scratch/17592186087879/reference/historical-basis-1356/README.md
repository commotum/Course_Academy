# Integrating-factor initial value problems

Draft generator at math basis 1356, steps 3–7 only; no database operations. Eight observed presentation templates and seven authored templates cover easy/moderate/hard. No plots.

```sh
.venv/bin/python generate/scratch/17592186087879.py --difficulty all --seed 3 --count 2 --format json
.venv/bin/python generate/scratch/17592186087879/validate.py
```

Use `--template q-335829 --difficulty moderate --profile observed` for explicit captured-bank replay; normal output defaults to authored banks. API accepts explicit parameters and rejects unsupported values/collisions without changing them. See classification.md, template-extraction.md, source-cases.json, review.md/review.json and validation.json.

The two unrated records lack correct references/solutions; their correct values and solutions are independently derived. Two source solution banks contain duplicate correct choices and remain evidence-only. These findings are not concealed by native ID-grading success.

Verified: 8/8 exact prompts; 71/71 option values in 16/16 complete mathematical banks (14/16 unambiguous); 12/12 available correct designations, four absent designations independently derived. Six captured worked sequences pass: 1/6 raw-exact, 5/6 presentation-normalized, zero mathematical solution repairs. Native grading: 146 accepted, 509 rejected, zero unresolved. Signed boundary sweep: 39 valid instances, nine whole-bank rejections; authored sweep: 84 instances and 21 invalid explicit-input rejections; 1,994 displayed algebra rows checked.
