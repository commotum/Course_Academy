# Matrix index generator

Validated finite easy generator: `generate/scratch/17592186100990.py`. Stable UUID is derived once from the existing KP identity and reused upon registration. No EDB writes occur in the generator.

Run with the project environment:

```sh
.venv/bin/python generate/scratch/17592186100990.py --difficulty easy --seed 11 --count 9
.venv/bin/python generate/scratch/17592186100990.py --difficulty easy --format markdown
.venv/bin/python generate/scratch/17592186100990/validate.py
```

Finite limit: nine genuinely distinct highlighted cells. One unchanged source cell is excluded from import. Increasing seeds, changing names, or shuffling choices cannot expand this set. Only the observed easy two-numeric-blank template is certified. Other easy templates, unrated banks and unobserved moderate/hard levels are bounded capability exceptions; no unsupported level is filled.

Evidence: source.json, classification.json/md, template-extraction.md, plot-extraction.md, review.json/md, validation.json, engine-report.json. Commit preparation, exact EDN, native preview, durable request, receipt and exact readback are retained under reference/. The commit worker locks the application's api.lock, rechecks current inventory and basis, and holds the lock through guarded submission/readback. It adds content only to this KP and attributes it to :application/ca-engine.
