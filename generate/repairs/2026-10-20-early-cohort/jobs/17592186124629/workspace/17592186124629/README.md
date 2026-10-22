# KP 17592186124629

Validated moderate generator: `generate/scratch/17592186124629.py`.
Stable generator UUID: `c3528424-1166-5f5e-a67b-38fc540dcd76`.

Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186124629.py --difficulty moderate --count 5 --seed 24629 --format json
.venv/bin/python generate/scratch/17592186124629.py --difficulty moderate --count 5 --seed 24629 --format markdown
.venv/bin/python generate/scratch/17592186124629/validate.py
.venv/bin/python generate/scratch/17592186124629/replenish.py
```

The worker interface returns a JSON list. There are 18 certified distinct questions: nine source replays and nine changed-premise variants. Counts exceeding that finite domain return at most 18, without padding. Preparation deduplicates against all original and generated questions, preserves their identities, and selects only fresh questions needed to reach five moderate tasks. A seed affects sampling order and metadata, not question identity.

Easy and hard remain unsupported, each with a nominal shortage of five. Source evidence can reopen classification; changing a difficulty label cannot fill either band. The incomplete q-47586 and contradictory worked solution q-141342 are retained unchanged and excluded from the validated inventory count. No application, scheduler, other KP, source-question or learner-state edits are part of this package.

The initial registration committed under the application `api.lock` at basis 2658, from basis 2657, attributed to `:application/ca-engine`. Nine fresh moderate originals already met the reserve; no new question was committed. Exact EDN, preview, request, receipt and exact-basis readback are in `reference/replenishment/basis-2657/`. `reference/committed-generator-1.0.0.py` and its validation preserve the artifact whose hash appears in that request. Version 1.0.1 adds the worker's `--format` interface; its mathematics and stable identities are unchanged. `cli-verification.json` verifies the actual worker arguments. Current and retained historical presentation/reservation facts are checked by replenishment; an exact saved durable request is reconciled before new intent.

Dependencies: Python standard library for generation; SymPy for exact validation. Native grading uses the existing `generate/runs/current/check-engine` application harness. No plots, asset publishing, or network services beyond the configured EDB integration are needed.
