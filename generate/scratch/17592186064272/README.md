# Derivative-to-supplied-rate generator

Script: `../17592186064272.py`. Read-only math snapshot basis 1356. All writes are confined to this KP's evidence; no database operations.

```sh
.venv/bin/python generate/scratch/17592186064272/validate.py
.venv/bin/python generate/scratch/17592186064272.py --difficulty all --count 2 --seed 42 --format markdown
.venv/bin/python generate/scratch/17592186064272.py --difficulty easy --template q_112518 --profile single_reciprocal --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard wrappers. `field_type` supports radio only. Source cases replay exact original parameters through the normal API. See `source-cases.json`; `templates.json` contains slotted masks, not literal source-return branches. Explicit parameters must have exactly the documented source case keys, or authored keys `Q,T,unit,context` plus `R` for easy single-rate or `I,L` for net-rate. Function names are distinct single letters, time is t/u/s, and source time units are fixed. Authored context is water/grain/fuel/inventory with corresponding physical units.

Coverage: nine exact prompts; six complete raw-exact banks, 30/30 raw-exact choices and 5/5 existing correct designations. Three absent fields and one absent designation/solution receive supported authored repairs. Two physical-time/context solution typos are repaired; 6/8 original solution bodies are exact and 8/8 match after declared repairs, before the universally appended instantaneous-rate clarification. Hard is entirely authored; no observed hard labels are inferred.

Verification independently parses the actual displayed equations and rate definitions, checks every complete choice and mathematical solution relation, rejects equivalent full-equation banks, checks ordered source prose/stages, parameter guards, formatting and stable identities. It invokes the actual `learning::grade_field` through the shared memory-only check-engine. No blank questions exist, so blank-equivalence grading is inapplicable. `engine-report.json` and `validation.json` keep native grading separate from mathematical and fidelity results.

`review.md` pairs every raw original with two changed-parameter source-template peers and labels all authored presentations; `review.json` has those generated records. `replay.json` holds all supported source replays. Mathematical diversity is explicitly finite: growth, positive loss, positive net magnitude and signed net contribution (four structures). Letters, stories and physical units provide presentation variety; they do not increase the four-task count. Choices are shuffled deterministically without changing content IDs. Full presentation identities include actual prompt/solution/bank, mathematical fingerprints exclude bank and incidental notation.
