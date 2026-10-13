# Second-order direct integration

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096697.py --difficulty all --seed 21 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186096697/validate.py
```

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Only radio fields are supported because all source fields are radio. Default profiles use a complete authored bank with eligible_for_learning=true and evidence_only=false. Observed and completed opaque expression banks expose eligible_for_learning=false and evidence_only=true; all records also expose bank_eligible_default. observed-q-ID profiles are raw evidence replays; completed-q-ID profiles repair presentation and remove redundant legacy fields. Explicit source replay parameters are {"scale":1}; any positive rational scale<=8 is supported.

The source snapshot, topic context and linked lesson route are basis 1356. Original sources are in source.json; source-cases.json replays all eleven through the public API. source-masks.json accounts for every original bank and mathematical stage. review.md/review.json include every source profile at original and changed parameters, every completion and two examples of every authored template at each difficulty. Hard is explicitly authored because no observed hard label exists. No plots, database writes, shared edits, or nested agents.

build-evidence.py is the private evidence producer; finish it before the final validation pass. validation.json reports frozen producer/artifact hashes and distinct source fidelity, completion, mathematical readback and real-engine grading counts. Raw legacy fields and the source's intermediate constant omission remain evidence; normal/completed output is checked separately. Decoded byte inspection finds no doubled macro-backslash or literal Unicode-escape anomaly. Missing correct references remain absent and never count as inferred matches.
