# Repair summary

Preserved direct-product, square and reciprocal-denominator families. Removed a printed neutral 1 multiplier in solution evaluation and clarified source-family metadata. Independently checked the source-typo counterexample: minus-square at 165 degrees is 3/2; plus-square is 1/2. The imported record is unchanged and its false conclusion is absent from generated solutions.

The required learner move and matched progression are in `instructional-account.md`. Runtime closure and exact dependencies are in `runtime-manifest.json`; `generator-package.json` binds every runtime file by hash. Only listed runtime files are needed for relocation.

Validation: 86 current CLI records from all three bands at seeds 47, 83 and 109; independent visible-TeX key and all-pairs choice checks; 1680 worked-solution equality witnesses including available replays; deterministic CLI replay, zero count, semantic batch uniqueness, source key witnesses, deliberate wrong-key rejection and runtime-only relocation. `evidence/counterfactuals.json` records controlled relevant and irrelevant changes; `evidence/choice-probes.json` records position/rank/length observations without claiming exhaustive shortcut absence. `evidence/*-47.json` and `*-83.json` are five-question batches for each band.

Reproduce from repository root:

```sh
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059674/evidence/check.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059674/evidence/counterfactuals.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059674/evidence/choice_probe.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059674/generator.py --difficulty moderate --count 5 --seed 47 --format json
```

Limits: numeric witnesses are independent checks, not universal symbolic proofs. Root owner performs actual UI rendering, native learner grading, inventory filtering and publication. No imported question, live registration, database or shared implementation was changed.
