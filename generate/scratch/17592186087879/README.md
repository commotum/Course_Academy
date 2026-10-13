# Integrating-factor initial value problems

Validated generator version ivp-integrating-factors-2 at source math basis 2010. Historical source.json and reference/historical-basis-1356 preserve the earlier evidence. Nine observed presentations and seven default authored templates cover easy/moderate/hard. No plots are required.

```sh
.venv/bin/python generate/scratch/17592186087879.py --difficulty all --seed 3 --count 2 --format json
.venv/bin/python generate/scratch/17592186087879/validate.py
.venv/bin/python generate/scratch/17592186087879/replenish.py
```

Normal generation defaults to authored whole banks. Explicit observed profiles replay captured evidence, including documented ambiguous or redundant banks; those evidence-only outputs must never enter replenishment. Easy is an authored unit-coefficient workload; moderate/hard follow labeled sources and the canonical cubic example. See classification.md, template-extraction.md, current-source.json, review.md and validation.json.

Validated: 9/9 source prompts, 80/80 choices across 18 complete banks, 16/16 supplied designations, two separately derived missing refs, eight worked sequences, 2,098 displayed algebra rows. Native learner grading: 152 accepted and 530 rejected with zero unresolved checks. Replenishment independently validates every selected instance, compares normalized ODE/IC tasks against all existing questions and the canonical example, checks actual grading, and retains exact additive transactions, basis guards, source attribution, requests, receipts and readback in reference/replenishment. It acquires the application api.lock before current inventory reads and holds it through commit/readback.
