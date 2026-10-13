# Common denominator and Pythagorean identity generator

Run `.venv/bin/python generate/scratch/17592186059643/validate.py` for complete exact source replay, omission parity, displayed-math checks, finite arithmetic-domain enumeration, deterministic identity, explicit bound rejection and the real native grader.

Preview: `.venv/bin/python generate/scratch/17592186059643.py --difficulty all --seed 18 --count 2 --format json`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`; easy/moderate/hard wrappers are available. Authored templates: `one_denominator`, `crossed_fractions`, `squared_shift`, `linear_plus_quotient`. Profile `authored-operations` is eligible practice. Every observed source identifier is in `source-cases.json`; profiles `raw-observed` and `repaired-observed` are evidence only.

Captured math basis 1356 is frozen in source/topic/lesson evidence. Missing easy is explicitly authored. Two source questions lack correct references, solutions and difficulty. Source error repairs and opaque distractor interpretations are documented; native radio selection checks do not establish displayed mathematical correctness. `validation.json` reports those separate results. No EDB access, transactions, registration, engine edits or plots.

Markdown CLI and review previews label every record's level, origin and attribute status, and mark the correct option. When an unrated raw source omits its correct key, the preview identifies an independently inferred answer without inserting that key into the raw API record. q23522 routes as inferred Easy, q1579 as inferred Moderate; both remain unrated originals in source counts.

Preview the unrated one-denominator source with `.venv/bin/python generate/scratch/17592186059643.py --difficulty easy --template observed_q_23522 --profile raw-observed --format markdown`; use `--profile repaired-observed` to view its explicitly inferred Easy evidence.
