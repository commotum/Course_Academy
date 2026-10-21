Run from this evidence directory. No command publishes assets or accesses the database.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review_tests.py
```

This creates the independent source replay, samples, mathematical checks, native grader input, controlled pairs, boundary tests, relocation and inventory evidence. Expected summary: 12 source replays; four unsupported; 65 mathematical cases with zero failures; package unchanged.

For each `(input, difficulty, output)` below, run:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty DIFFICULTY --output OUTPUT
```

| INPUT | DIFFICULTY | OUTPUT | Accepted/input |
|---|---|---|---|
| easy-records.json | easy | delivery-easy | 20/25 |
| moderate-records.json | moderate | delivery-moderate | 28/35 |
| runner-batch.json | easy | delivery-batch | 3/5 |

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root . --limit 13
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input irrelevant-row-pair.json --output render-irrelevant --asset-root . --limit 2
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python delivery_tests.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine counterfactual-grader-input.json counterfactual-grader-results.json
```

Actual UI: 13+2 passing renders; native grader: 129 accepted / 309 rejected, plus controlled cross-response cases: 2 accepted / 2 rejected. `delivery_tests.py` also faithfully reproduces the inspected learner-selection rule with explicit seeds and stand-in new entity IDs; it does not claim a live learner-policy snapshot.

The following are **failing acceptance tests**, retained so a repair can adopt them. Each currently exits 1 with a concrete assertion:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failure.py --case shortcut
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failure.py --case source-replay
```

The minimal shortcut pair fixes q-73743 and seed 71923, changing only rhs_scale between +1 and -1. Full records and test results are saved in `minimal-shortcut-records.json` and `minimal-shortcut-results.json`. Omissions are saved in `minimal-source-results.json`.

`sampler-stage-results.json` and the two `sampler-stage-*-records.json` files record actual `g.batch(level,10000,71923)` results. Before internal fingerprint collapse there are 5×8 easy and 7×8 moderate instances; afterward 40 easy and 48 moderate remain. This enumeration examines filtering, while independent mathematical checks remain the selected 60 records plus 5 runner records.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python write_report.py
python3 validate_evidence.py
```

Final report: `review.json`. Full source interpretation preceded package inspection and remains in `source-analysis.json`. Source/inventory/batch bindings and absence of optional repair/publication inputs are recorded in `review-context.json`.
