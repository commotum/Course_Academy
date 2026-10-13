# Product-rule generator

Local generator and evidence for KP 17592186096618, math basis 1356. No database writes.

Run `.venv/bin/python generate/scratch/17592186096618/validate.py` from the repository root. Additional explicit boundary/identity checks: `.venv/bin/python generate/scratch/17592186096618/boundary.py`. Preview: `.venv/bin/python generate/scratch/17592186096618.py --difficulty all --seed 4 --count 2 --format json`.

The API exposes generate_easy, generate_moderate, generate_hard, and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Explicit parameters reject invalid/ambiguous inputs. source-cases.json lists all 13 replay calls. Twelve observed templates and five complete source radio profiles are preserved; moderate/hard add two authored templates each. Eight observed blanks require fragments; authored blanks require the full derivative.

validation.json separates exact prompts/banks/solutions, observed correct references, two mathematically inferred missing references, actual printed-math readback, changed-parameter tests, and real learning::grade_field checks. readback.py parses displayed products, u/v definitions, formal derivatives, component derivatives, distributed sums, choices, and reinserted blank fragments without reading generation parameters. Raw source/topic/lesson wrappers retain capture provenance. Review examples label source replays and authored/generated variants explicitly. No plots or image models are used.
