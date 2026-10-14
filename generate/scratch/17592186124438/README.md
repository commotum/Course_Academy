# Tangent-line generator

Run `.venv/bin/python generate/scratch/17592186124438/validate.py` for complete source replay, independent mathematical checks, boundary cases, deterministic replay, and actual learner grading. Run `.venv/bin/python generate/scratch/17592186124438.py --difficulty all --count 2 --seed 7 --format json` for previews.

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and named difficulty entrypoints. Supported levels are easy, moderate, hard; field type is radio. All 16 current moderate families are normal defaults. `raw_q-…` profiles retain complete observed banks and are evidence-only. `authored_operations` is an explicitly labeled extension using complete method-derived banks. See classification.md and template-extraction.md for exact slots and difficulty evidence.

Source snapshot is database math, basis 2267. Historical evidence at basis 1356 remains under reference/legacy-basis-1356. The deterministic generator UUID is 004c08d0-a323-5f8e-9da1-7f9ed62ba16b; registration reuses any existing KP generator identity. `replenish.py` uses the existing EDB integration, serializes writes with api.lock, rechecks current inventory, validates every accepted instance, saves exact intent and preview, and verifies the receipt at its exact database basis. It only adds generated content and this KP's registration.
