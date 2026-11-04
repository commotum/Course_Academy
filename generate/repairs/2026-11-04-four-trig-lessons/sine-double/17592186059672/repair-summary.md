# Repair summary

Removed the easy identity and substitution sequence. Easy keeps independent two-application recognition with coefficients 4/8 and positive familiar endpoints. Moderate ordinary sampling now includes reciprocal cancellation and both evaluated and symbolic-terminal plain products. Hard retains the two reciprocal quotient orientations. Removed generated prototypes from the source-replay catalog. Preserved original source replay banks as evidence; source 17592186233282 has two equivalent wrong choices, while ordinary generated banks reject all pairwise equivalences.

The required learner move and matched progression are in `instructional-account.md`. Runtime closure and exact dependencies are in `runtime-manifest.json`; `generator-package.json` binds every runtime file by hash. Only listed runtime files are needed for relocation.

Validation: 70 current CLI records from all three bands at seeds 47, 83 and 109; independent visible-TeX key and all-pairs choice checks; 1578 worked-solution equality witnesses including available replays; deterministic CLI replay, zero count, semantic batch uniqueness, source key witnesses, deliberate wrong-key rejection and runtime-only relocation. `evidence/counterfactuals.json` records controlled relevant and irrelevant changes; `evidence/choice-probes.json` records position/rank/length observations without claiming exhaustive shortcut absence. `evidence/*-47.json` and `*-83.json` are five-question batches for each band.

Reproduce from repository root:

```sh
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059672/evidence/check.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059672/evidence/counterfactuals.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059672/evidence/choice_probe.py
.venv/bin/python generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059672/generator.py --difficulty moderate --count 5 --seed 47 --format json
```

Limits: numeric witnesses are independent checks, not universal symbolic proofs. Root owner performs actual UI rendering, native learner grading, inventory filtering and publication. No imported question, live registration, database or shared implementation was changed.

Final presentation refinement verified by the current CLI: `evidence/presentation-refinement.json`. The relevant full CLI regression, numeric/choice/solution checks, controlled pairs, and choice observations were regenerated.
