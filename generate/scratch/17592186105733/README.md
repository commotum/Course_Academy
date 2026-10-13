# Triangle area from three vertices

Run `.venv/bin/python generate/scratch/17592186105733/validate.py` from the repository root. It checks all original banks/prose/stages, changed parameters, authored peers at all three levels, complete-bank rejection, reduced-workload guards, task/content identity and actual native grading. Results and freeze hashes are in validation.json. Review originals and generated peers in review.md or review.json.

Preview: `.venv/bin/python generate/scratch/17592186105733.py --difficulty all --seed 12 --count 2 --format json`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters are `{"vertices": [[x,y,z],[x,y,z],[x,y,z]]}`. Source templates are their q- IDs, all assigned moderate; profile is `observed/q-ID`, `raw/q-ID` or `blank`. Normal default templates are `authored_LEVEL_radio|blank`, with complete operation banks. `raw/q-127908` is the documented duplicate-wrong-choice evidence profile. No source error is silently copied into normal output. No database writes or plots.

Easy/hard are authored workload policies grounded in the canonical method, route and prerequisite; scalar source distractor interpretation remains limited. q-20016's missing solution/designation/difficulty are derived separately. See classification.md and template-extraction.md.
