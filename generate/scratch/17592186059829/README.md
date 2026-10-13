# Closed-interval generator

`.venv/bin/python generate/scratch/17592186059829/validate.py`

`.venv/bin/python generate/scratch/17592186059829.py --difficulty all --count 2 --seed 5 --format markdown`

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus easy/moderate/hard wrappers. Templates: inequality_to_interval, interval_to_inequality. Profiles: observed_interval / observed_inequality (normal independent keys and authored solutions/levels), raw_interval / raw_inequality (public parameterized evidence replay preserving missing rating/key/solution). Explicit endpoints use canonical strings, e.g. `{'a':'-sqrt(2)','b':'1/2'}` at hard. No solving or nonclosed correct-set branch.

Two unrated originals, ten complete choice values; all three levels are authored and curriculum-grounded. Validation exhausts every finite eligible endpoint pair in both directions, reads actual displayed sets/solution stages, replays raw sources, and grades every owned choice ID through the real native engine on representative normal instances. Correct-designation fidelity has zero present-source denominator; independently derived keys are reported separately. No unresolved findings; no database writes. Parent QA is still required. `freeze.json` records artifact hashes.
