# Matrix-product dimension generator

Registered script: `generate/scratch/17592186100870.py`.

Supports easy (forward order) and moderate (reverse order), each with radio and two-blank templates. Hard remains unsupported under the bounded evidence in `capabilities.json`; its nominal five-question shortage is explicit. The two incomplete unrated source questions and the source display error are preserved.

Run from any directory:

```sh
python3 /home/jake/Developer/Course_Academy/generate/scratch/17592186100870.py --difficulty easy --count 5 --seed 2636 --format json
```

The script reuses repository-installed SymPy when the invoking Python lacks it. The JSON retains template, complete bank profile, parameters, generator identity, dependency version, and source references outside learner content. Ordered factor shapes define distinct tasks across seeds, labels, banks, field types, and difficulties.

`source.json`, `classification.json`, and `template-extraction.md` retain the frozen sources and derivation. `validate.py`, `validation.json`, `source-cases.json`, `slot-coverage.json`, `review.md`, and `engine-report.json` cover source fidelity, mathematical validation, domain limits, deterministic identity, one-slot changes, and actual learner grading. `runtime-compatibility.json` verifies matching output from system and repository Python.

`replenish.py` uses the existing application integration, serializes durable work under `api.lock`, rechecks current inventory and basis, previews native validation, saves exact requests before submission, and verifies the receipt's exact after-basis. `reference/replenishment/basis-2636/` retains the exact transaction, intent, preview, committed receipt, content readback, attribution/scope checks, final inventory, and original generator artifact at commit. The subsequent runtime import fallback changes no generated question records; its current hash is retained separately from the commit artifact hash.

Replenishment committed two questions at basis 2637 and independently verified five available distinct questions per supported level. The source q-70702 with swapped display labels is excluded from those validated counts. The native inventory may retain its unclassified-source job because incomplete originals were intentionally preserved.
