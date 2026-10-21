# Reproduction

Run all commands from this evidence directory. All generated files remain here.
Use `PYTHONDONTWRITEBYTECODE=1` for Python entry points.

```sh
export PYTHONDONTWRITEBYTECODE=1
/home/jake/Developer/Course_Academy/.venv/bin/python audit_revision.py
/home/jake/Developer/Course_Academy/.venv/bin/python delivery_revision.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine delivered-grader-input.json delivered-grader-results.json
```

`audit_revision.py` records the copied author preflight commands, environment,
old failing outputs and current passing outputs in `preflight-verification.json`.
Its original independent tests demonstrate both retained defects against the
previous captured package and rerun them against the current package. Fresh seed
846271, explicit boundary/sign parameters and every controlled bank are saved in
complete generated records. `reused-evidence-provenance.json` identifies inherited
independent helpers; `source-analysis.json` records source-account verification.

Before running `delivery_revision.py`, concatenate the easy/moderate sampled
records and matching-difficulty `counterfactual-records.json` into
`delivery-easy-input.json` and `delivery-moderate-input.json` respectively. These
inputs are retained. For each LEVEL in easy, moderate and batch run:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py \
  --input delivery-easy-input.json \
  --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105745/source/source.json \
  --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105745/source/inventory.json \
  --difficulty easy --output delivery-easy --math-root /media/jake/SSD/EDB/math
```

For moderate replace the input, difficulty and output with their moderate paths.
For batch use `runner-batch.json`, difficulty easy and output `delivery-batch`.
The helper reads the actual publisher preparation implementation; no publication
or database operation is invoked. Its JSON reports retain hashes, counts and
captured basis.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py \
  --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py \
  --input render-remaining-records.json --output render-remaining --limit 15 --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python finish_review.py
/home/jake/Developer/Course_Academy/.venv/bin/python validate_review.py
```

The first renderer command uses its default six-record limit. The second input
is `render-records.json[6:]`, so together they render all 21 chosen instances.
Visual inspection is recorded separately from programmatic render success.
`finish_review.py` checks native before/after outcomes and actual UI ordering,
then writes the pedagogical analysis and final result. `validate_review.py`
validates the supplied pedagogical schema, relative nonempty evidence paths,
eight-check contract and package hash equality.
