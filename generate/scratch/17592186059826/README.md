# Open interval generator

Run `.venv/bin/python generate/scratch/17592186059826/validate-current.py`, then `.venv/bin/python generate/scratch/17592186059826/replenish.py` for locked, scoped replenishment through existing EDB integration.

Preview: `.venv/bin/python generate/scratch/17592186059826.py --difficulty easy --count 5 --seed 2091 --format json`. `all` means all supported levels (easy); explicit moderate/hard fail with a capability error. Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`.

Two directions: inequality_to_interval, interval_to_inequality. Complete profiles: original_bank; source_raw for original missing-attribute replay; signed_source and surd_source for compact reverse source layouts. See classification.md and template-extraction.md for exact domains, eligibility and source fidelity. `capabilities.json` records unsupported bands and finite limits. Stable generator UUID is derived from the existing KP UUID and reused in registration. Mathematical fingerprints exclude seed, variable aliases, choice order and bank identity. Prior classification and validation are retained under reference/legacy-basis-1356/.
