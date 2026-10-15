# Half-open interval generator

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186059827/validate.py
.venv/bin/python generate/scratch/17592186059827.py --difficulty all --seed 17 --count 2 --format json
```

No EDB reads or writes are performed. Two observed radio templates and full five-choice banks are replayed through the public generator. Raw profiles preserve missing difficulty, correct ref and worked solution. Normal output derives the key mathematically and supplies an explicitly authored canonical-anchored solution. All easy/moderate/hard workload assignments are authored. Scope is bounded half-open interval↔compound inequality translation; no graphing or solving is introduced.

`source.json` is the exact basis1356 capture. `source-cases.json` exposes raw replay parameters. `classification.md` and `template-extraction.md` explain source coverage, all ten choices, lesson route, guards and authorship. `review.md` includes both originals, each observed bank's changed-parameter replay/completion, and two generated examples per level (one per direction). `validation.json` reports separate exact prompt/bank, missing-key/solution, derived mathematics and real native grader counts, plus final artifact hashes. The grader input/report are saved. Final parent independent QA is still required.

Current reclassification and independent parent QA: `.venv/bin/python generate/scratch/17592186059827/validate-current.py`. This includes the two additional sources captured at basis 2081 and both new profiles. `current-validation.json` is the authoritative final validation. Replenishment uses `replenish.py`, the existing Database integration, native preview predicates, the application contributor, and api.lock through exact-basis receipt verification.
