# Constant multiple of ln x generator

`../17592186096613.py` generates easy questions for KP 17592186096613. It uses the registered UUID derived from the existing KP identity if no generator is already registered. Later replenishment reuses the registered identity. JSON CLI output is a list compatible with the existing inventory worker:

```bash
.venv/bin/python generate/scratch/17592186096613.py --difficulty easy --count 5 --seed 42 --format json
.venv/bin/python generate/scratch/17592186096613.py --difficulty easy --template blank --profile canonical --count 2 --seed 42 --format markdown
.venv/bin/python generate/scratch/17592186096613/validate.py
.venv/bin/python generate/scratch/17592186096613/replenish.py
```

Supported level: easy. Moderate and hard are bounded unsupported capabilities with nominal shortages of five each. Do not treat those as filled. The exhaustive finite parameter catalog is deduplicated by normalized displayed coefficient c, independently of bank/layout/seed/order. `batch` never pads exhausted requests; the CLI reports a finite shortage on stderr and returns only distinct records.

Source replay, independent differentiated prompt/solution checks, source bank coverage, boundary checks and current application grader results are saved in validation.json and native-report.json. Review originals and variants in review.md. `replenish.py` reads live inventory and captures one current basis before selecting content. It holds the application's api.lock from inventory recheck through exact request submission and readback. It adds only new question components, membership and generator registration, checks writer validation specs, retains requests/receipts under reference/replenishment, and verifies old source records and learner history are unchanged. An unknown commit outcome is recovered using the original exact saved intent before new work.
