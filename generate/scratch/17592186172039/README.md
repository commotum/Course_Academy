# Quadrant slope-sign generator

Current version: `quadrant-sign-checkbox-v3`, reviewed against math basis 2771. The registered script is `generate/scratch/17592186172039.py`.

Run `.venv/bin/python generate/scratch/17592186172039/validate.py` to replay all current source prompts, eight worked solutions, 24 boolean banks (48 values), independently check every one of the 320 meaningful tasks, exercise changed targets and parameter boundaries, and grade every checkbox choice through the actual engine.

Run `.venv/bin/python generate/scratch/17592186172039/replenish.py` to recheck current inventory, exclude all previously used/reserved or mathematically duplicated tasks, and publish only the shortages. It serializes through the application's `api.lock`, saves the exact basis-guarded request, verifies every new record and preserved source at the committed basis, then writes the requested job outcome.

Supported levels: easy cx, moderate cxy, hard cxy²/cx²y/cx²y². Limits: 64, 64, 192 meaningful tasks respectively. Current questions use three checkbox fields keyed I/II/III. Historical v2 radio evidence is preserved under `reference/legacy-v2/`. No source questions or learner records are revised.
