# Invertible matrix theorem generator

Validated moderate radio/checkbox generator for KP 17592186124511.
Public script: `generate/scratch/17592186124511.py`.

```sh
.venv/bin/python generate/scratch/17592186124511.py --difficulty moderate --count 5 --seed 1930 --format json
.venv/bin/python generate/scratch/17592186124511/validate.py
.venv/bin/python generate/scratch/17592186124511/replenish.py
```

Twelve full source banks replay exactly. Independent rendered-math validation
passed 960 sampled instances and actual grading passed 2,270 acceptance checks
and 3,248 rejection checks with zero unresolved checks. Native build provenance,
source mappings, mathematical classification and side-by-side review are local.
The source bank has one incomplete unrated member and one malformed moderate
bank; both remain unchanged and are explicitly excluded from generator fidelity.

The application inventory recheck found 13 available moderate questions at basis
2275. Twelve are independently replayed source banks; the native application also
counts the malformed-label bank. Either count exceeds the reserve target. No
practice questions were committed. Registration of generator UUID
2c8a204b-6657-54da-84cb-6832f441443e was confirmed at basis 2276, attributed to
`:application/ca-engine`. The exact request, preview, receipt and scoped readback
are under `reference/generated/17592186124511/job-05ddcd18/basis-2275/`.
All 14 original members, the canonical example and learner history are unchanged.

Easy/hard are unsupported by this bounded package, with five-question reserve
shortages still explicit for each. Changing determinant magnitude, seed, identity,
choice order or an equivalent basis does not add inventory. Finite domains and
bounded-sampling failures are recorded in capabilities.json. Source evidence can
reopen classification; the package makes no claim that other bands are impossible.

replenish.py acquires the application api.lock before its fresh captured inventory
and holds it through basis-guarded submission and readback. It recovers the exact
saved intent before selecting new work. Its existing job is already verified;
re-running it reconciles the retained receipt without a new durable transaction.
