# Surface-area generator

This package belongs only to KP `17592186119888`, Finding the Surface Area of a Parametric Surface. Generator UUID: `92f3e1ca-f67b-5933-9d82-67166ccbf4d0`; script: `generate/scratch/17592186119888.py`.

`classification.md`, `template-extraction.md`, and `capabilities.json` describe the evidence and conservative domain-size policy. All eight original profiles are retained. Moderate and hard are supported; easy is unsupported and never reported filled. The finite implementation domain has 24 tasks per supported band, including four source tasks; further changes to seed or choice order do not create tasks.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186119888.py --difficulty moderate --count 5 --seed 119888 --format json
.venv/bin/python generate/scratch/17592186119888/validate.py
.venv/bin/python generate/scratch/17592186119888/replenish.py
```

The generator emits JSON records or Markdown. An unsupported level or count beyond its finite capacity raises an error. It does not transact. `validate.py` independently reads mathematical objects from the rendered text and uses the existing native application grader. `review.md` pairs every source with a changed-domain example. `source-replay.json`, `choice-recipes.json`, `slot-coverage.json`, `native-report.json`, and `validation.json` retain separate fidelity, correctness, variation and grading results.

`replenish.py` reuses the configured math EDB transport and application contributor `:application/ca-engine`. It holds `.local/learning/requests/math/api.lock` from its fresh inventory read through preview, durable submission, exact-basis readback and final inventory check. It only asserts new questions/fields/answers, generator registration, and this KP's membership/reference, with installed entity validation specs. A request and receipt already saved in `reference/replenishment/basis-*` are recovered before new intent. Exact transaction text, basis, lineage, source, request key, UUIDs, preview and receipt are retained there. Verification checks datom scope/attribution, unchanged originals, stable registration, current counts and repeat preparation.

No source question, learner history, scheduler or application code is changed. The job's JSON result is saved at the user-specified `.result` path; the package retains the same outcome alongside its commit evidence.
