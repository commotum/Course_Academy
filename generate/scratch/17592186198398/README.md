# Triple integral evaluation generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186198398/validate.py
.venv/bin/python generate/scratch/17592186198398.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186198398.py --difficulty moderate --profile raw-17592186374125 --format json
```

`generate_easy`, `generate_moderate`, `generate_hard` and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` return local schema-shaped review records. Normal fields are five-choice radios. `method` is the complete authored method bank for the selected family, chosen before sampling. Explicit parameters are validated and never resampled; ambiguous complete banks raise `SampleRejected`. Raw profiles accept `parameters={"scale": integer}` (nonzero, absolute value at most 6), preserve source missing attributes and are evidence-only. They cannot be promoted to learner content.

Seven captured practice families at math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; five observed moderate and two unrated. No observed easy/hard questions. Easy and hard are authored workload policies grounded in the same supplied-substitution evaluation skill. All maps are globally invertible polynomial or linear shears with constant nonzero determinant: no root-branch or singular-endpoint assumptions. No plot rendering is needed. No database or engine changes.

`raw-recipes.json` contains extracted prompt/solution masks, complete scalar atoms and actual ordered arithmetic nodes. `extract.py` creates this recipe evidence from the frozen source; `source-cases.json` replays every practice source through the public API. Normal worked solutions preserve the shared four-step prose and expand all successive primitive endpoint components. They are explicitly authored expansions; raw replay preserves the exact original mathematical sequence. Opaque banks have no claimed recovered author intention. `validation.json` separates original fidelity, mathematical correctness and native radio grading. Missing raw correct refs prevent grading two original records; their normal authored family records are graded.

`domain-counts.json` gives the exact finite default sampler capacity: 21,699 tasks after complete-bank collisions, excluding unused parameters/raw bank scales. The 360-instance validation sweep measures sampled task uniqueness separately, rather than treating each seed as a new task.
