# Circulation Over Space Curves generator

Script: `../17592186133926.py`. Frozen math basis **1356**. Direct closed-curve circulation only. The original frozen package stopped at step 7; its replenishment was subsequently committed and verified at basis **2687** (from 2686). No plot assets are required.

```sh
.venv/bin/python generate/scratch/17592186133926/validate.py
.venv/bin/python generate/scratch/17592186133926.py --difficulty all --seed 9 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186133926.py --difficulty easy --profile raw:q-161925 --format json
```

Import the script with importlib and call `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` or `generate_easy`, `generate_moderate`, `generate_hard`. `field_type` supports only `radio`. Normal profile is `authored-method`; source profiles are `raw:q-N`. Normal explicit parameters are `{a,b,sign}` for easy and `{a,b}` for moderate/hard. Positive primitive axis pairs must satisfy 1..4 (easy/moderate), 1..6 (hard). Raw explicit parameters are `{force_scale: integer}`, nonzero and bounded by absolute value 4; the original scale is 1. Profiles and level/template mismatches fail rather than silently changing parameters.

`source-cases.json` covers all eight originals through the public API. `extraction.json` maps every source choice and ordered calculation component. Classification and four-stage extraction are in their Markdown files. `review.md` / `review.json` contain each original plus two generated raw variants for each observed mask, and two normal authored examples for every family (including all three levels). Correct choices, original/generated provenance, actual difficulty, and eligibility are labeled. q-162238 stays unrated with no key/solution in raw replay; its hard rating and −1/60 key are authored/inferred in normal records.

`validation.json` reports exhaustive independent checks over 111 normal tasks, exact source fidelity (8 prompts, 7 present solutions, 40 choice values, 7 present correct designations), key-presence parity, seed/order-independent identities, source stage errors, frozen/runtime hashes and Python/SymPy versions. `native-input.json` and `native-results.json` use the actual learning::grade_field through the shared check-engine: all five choices of 111 normal tasks and seven keyed originals. The missing-key raw original cannot be submitted to that native harness and is explicitly counted separately.

Every raw historical scalar bank is **opaque evidence only**. The two captured intermediate solution errors are documented and preserved there; normal generation recomputes correct signs and arguments. No source error, absent key, unsupported bank intention, or authored difficulty is counted as an observed repair match. Normal default sampling covers every supported family and chooses its complete method-error profile before parameters.

## Inventory publication at basis 2687

The unchanged generator is registered as `c3c4b7ba-f69a-55fc-8713-34995bc1ce9b`, with repository path `generate/scratch/17592186133926.py`. The application contributor `:application/ca-engine` authored four new moderate questions and five new hard questions. Independent validation and the native grader check all selected questions. Five validated fresh tasks are available at each difficulty. The easy reserve needed no additions.

All nine existing source questions, the canonical example, learner history, and unrelated facts are unchanged. The exact request, preview, receipt and committed-basis readback are retained under `reference/replenishment/basis-2686/`. Application `api.lock` covered the current-basis check through submission, readback and inventory recheck.

Live source refresh found one additional easy source, q-162232. Its independent polynomial calculation is recorded in `source-refresh-validation.json`; it supports existing inventory only, without expanding the generator or claiming fidelity for an unimplemented source bank. The two historical intermediate solution errors and incomplete unrated q-162238 remain preserved and are excluded from the validated counts. The final application inventory reports no remaining jobs for this KP; the incomplete source remains unchanged and excluded from the validated counts.

Run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186133926/replenish.py` to recover the saved exact intent and verification. Finite domains remain 66 easy, 22 moderate and 23 hard tasks; this commit does not claim an unlimited supply.
