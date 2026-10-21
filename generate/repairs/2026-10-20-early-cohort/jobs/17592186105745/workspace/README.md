# Repaired generator

Current package: `package.json`, `17592186105745.py`, `17592186105745/source.json`, and `requirements.txt`. Earlier v1 reports under `17592186105745/` are historical evidence, not current validation or runtime dependencies. Current design and constraints are in `instructional-account.md`.

Use the job Python:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186105745.py --difficulty easy --count 5 --seed 71923 --format json
```

The normal sampler uses compatible five-choice banks whose target is chosen after the bank. All five options can become the correct answer when the prompt changes. `generate(level, seed, template, {'bank_profile':'source','rhs_scale':1})` replays a source bank, its keyed field and its complete worked solution; it is not the normal practice bank. All 16 current source profiles are supported. Easy and moderate are supported; hard is rejected. Generated content IDs and generation metadata are separate from source IDs.

Run the retained findings and offline checks:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python regression_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python delivery_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python boundary_checks.py
```

`repair-regressions.json` binds the two history IDs to the specific regression cases. `independent_math.py` retains the earlier review's visible-record parsing, exact mathematical witnesses, and bank-only heuristic, with no dependency on the runtime module. Tests write evidence only. `delivery_checks.py` uses the shared delivery helper and native grader, compares surviving banks, audits the captured inventory, and relocates only declared runtime files.

Actual UI command (screenshots inspected):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Current results: 16 complete source replays, 80 identical-bank decision cases, 15 fresh samples, five runner samples, and eight signed boundary cases pass independent math checks. Native grading passes 630 option checks across raw, delivered, and boundary records. Delivery retains all 80 controlled, 15 fresh, and five runner records. Four actual UI screenshots pass and were visually inspected. No images were generated or published, no database content changed, and no engine files changed.

Fidelity is exact in explicit replay mode except for selecting q-42156's single authoritative keyed field from a duplicate capture. Default banks are documented conservative extensions. Grading is radio-only, so valid equivalent free-text notation is not part of this response contract. Post-filter identical-bank tests establish resistance to deterministic bank-only selection within the tested families; they do not prove the absence of every conceivable strategy. Live learner history and future entity assignments are unavailable; selection evidence is an explicitly bounded offline reproduction.
