# KP 17592186133882 generator package

`../17592186133882.py` produces easy, single-field radio questions for the
q-109111 polynomial triangle family. It supports 41 distinct coefficient pairs.
The source pair is a replay, not a fresh question. Moderate/hard and other source
families are outside v1 capability. See classification and extraction for evidence
and bounded exceptions. Unsupported bands must never be reported filled.

Run from the repository root:

```sh
python3 generate/scratch/17592186133882.py --difficulty easy --count 5 --seed 123 --format json
.venv/bin/python generate/scratch/17592186133882/validate.py
.venv/bin/python generate/scratch/17592186133882/replenish.py
```

The CLI reexecutes the repository venv if the inventory worker's system Python
lacks the declared SymPy dependency. Validation exhausts the domain, independently
parses displayed prompts/solutions/choices, replays the complete supported source
bank, checks actual learner grading, and verifies the unchanged stored asset.
JSON retains version, seed, coefficients, dependencies and source lineage apart
from database entities. Questions, fields and field-owned answers have stable
UUIDs based on mathematics, never seed or option order. Seeds select parameters.

Replenishment uses the existing Database/EDN/native-preview integration. It checks
current inventory, acquires the application's api.lock, rechecks basis and lineage,
and holds the lock through guarded submission and exact-basis readback. Durable
requests/receipts and inventory evidence are under
`reference/generated/17592186133882/`. It preserves all original content and
learner history. A registration alone does not certify arbitrary future output.
