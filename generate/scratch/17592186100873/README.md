# Finding an Entry of the Product of Two Matrices

`../17592186100873.py` generates bounded Easy matrix-entry questions from fixed
source operand matrices and eligible queried cells. It supports radio and blank
fields. Moderate and Hard remain unsupported, not filled. There are 90 distinct
selected-vector tasks before excluding existing/shown/reserved content.

```
.venv/bin/python generate/scratch/17592186100873/validate.py
.venv/bin/python generate/scratch/17592186100873.py --difficulty easy --count 5 --seed 23 --format json
.venv/bin/python generate/scratch/17592186100873/replenish.py
```

`generate(level, seed=0, template=None, parameters=None, profile=None, replay=False)`
accepts parameters row/column with one-based integer indices, source question ID
as template, and its source-bank profile. `easy`, `candidates`, and Markdown/JSON
CLI previews are available. CLI counts exceeding the finite domain fail explicitly.
Source replays are evidence-only; stable generated UUIDs and field-owned answer
UUIDs never depend on seed or choice order. See classification, template extraction,
complete source-bank mapping, side-by-side review, validation and freeze evidence.

Replenishment rechecks the configured math inventory, native pool and actual grader,
excludes every historical presentation/reservation and current mathematical task,
then adds only the supported shortages. It retains exact basis-guarded EDN and
requests, previews installed specs, commits as :application/ca-engine, and verifies
source records, membership, registered generator and attribution at the receipt
basis while holding the application's api.lock. It touches no learner or engine
facts. Incomplete unrated originals remain explicit and unchanged.
