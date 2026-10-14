# Midline generator

Knowledge point 17592186129123; math basis 1356. Run:

```sh
.venv/bin/python generate/scratch/17592186129123/validate.py
.venv/bin/python generate/scratch/17592186129123.py --difficulty all --count 2 --seed 17 --format json
.venv/bin/python generate/scratch/17592186129123.py --difficulty easy --profile raw_q-236892 --parameters '{"minimum":0,"maximum":4}' --format markdown
```

`generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` return local schema-shaped records. Explicit parameters are exactly minimum/maximum. Raw profiles preserve missing attributes and are evidence-only; default authored profiles are learner eligible. All normal fields are five-option radios containing complete equations. Moderate/hard are disjoint authored arithmetic extensions of the source average-of-extrema method. No plots, database reads/writes, registration, or commits.

Validation checks 8/8 prompts, 7/7 supplied solutions, 6/6 banks, 30/30 choices, 5/5 available correct designations, source key-presence parity, 720 sampled records plus 30 explicit bank/domain boundary records, full domain workload disjointness/meaningful task counts, identities, collisions, all actual printed equations and conclusions, and native radio grading. q236750's missing key/solution/difficulty and the two fieldless records are preserved in raw API output and separately repaired for learning. Opaque historical bank intent remains unresolved; those profiles are intentionally ineligible for defaults. Native results: 74 accepted and 296 rejected, zero unresolved. Run validation to refresh current implementation/engine hashes and review artifacts. The original draft stopped at step 7; replenishment evidence below records steps 8–9.

## Verified replenishment

Run `.venv/bin/python generate/scratch/17592186129123/replenish.py` to recover the retained request and verify its outcome. The application lock covers the fresh inventory recheck, preview, basis-guarded submission, and exact-basis readback.

Committed at math basis **2484** from basis **2483**, attributed to `:application/ca-engine`. Registered generator UUID `9623a13b-4578-5bf9-b125-66c10695906a` at `generate/scratch/17592186129123.py`. Added five moderate and five hard questions with ten distinct extrema pairs; the five fresh valid easy originals already met the reserve. All eight source questions, the canonical example, and learner history are unchanged. The three incomplete/unrated originals remain excluded. The post-commit native inventory reports no remaining jobs for this KP.

Exact EDN, durable request, speculative preview, receipt, actual grader results, preparation, readback, and outcome are in `reference/replenishment/basis-2483/`. There was no supplied `.generated` file.
