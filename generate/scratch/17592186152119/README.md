# Three-polynomial LCM scratch generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186152119/validate.py
.venv/bin/python generate/scratch/17592186152119.py --difficulty all --count 2 --seed 42
.venv/bin/python generate/scratch/17592186152119.py --difficulty moderate --profile observed-q-112230 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), with generate_easy/moderate/hard entrypoints. Explicit parameters are never silently changed. Records are local review JSON with UUID strings, schema enum strings and owned correct lookup refs, not transaction EDN.

Basis1356. All8 sources are included;2 lack captured answers/difficulties/solutions and receive documented authored assignments and completions. q-222132 has one known raw prose typo; its explicit `-raw-error` profile retains evidence, while normal output corrects it. Three observed complete five-entry radio banks replay; default authored banks use GCF/product contents and minimum/sum powers, avoiding uncertain source mistake interpretations. Hard is an explicitly authored three-factor extension of the same lesson rule, in two variables. No plots, network access or database operations.

`validation.json` distinguishes captured bank/solution fidelity from completions/repairs and actual native grading. `review.md` shows raw originals and labeled changed-parameter variants; `review.json` holds the generated review records. `masks.json` stores fixed source prose and ordered complete-math slots; it is not an answer lookup sampler. Native engine fixture and report are private artifacts. Implementation version is frozen for parent QA after validation; frozen.json records SHA256 hashes.

Public `raw-q-218518`/`raw-q-218519` profiles preserve all original omissions. Separate `completion-q-218518`/`completion-q-218519` profiles supply normal authored answers/solutions. Raw omission/error and observed scalar bank profiles are evidence-only, ineligible for learning. Canonical task hashes ignore consistent variable aliases and input order. The native grader has a512token input cap: factored and partially factor-expanded answers pass; oversized full expansions remain explicitly documented unresolved checks.
