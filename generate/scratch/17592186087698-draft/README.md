# Identifying Other Matrices isolated draft

Draft script: ../17592186087698-draft.py. Raw source/context are immutable basis-2275 copies. The registered numeric generator and its entire existing evidence tree remain untouched. No database reads/writes, registration, engine edits or commits are performed.

```sh
.venv/bin/python generate/scratch/17592186087698-draft/validate.py
.venv/bin/python generate/scratch/17592186087698-draft.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186087698-draft.py --difficulty easy --profile row_sets_raw --count 2 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None); generate_easy, generate_moderate and generate_hard. Complete profiles are documented in classification.md; source-cases.json replays all seven originals through this public API. Raw missing-key profiles are evidence-only; repaired profiles derive keys/solutions independently. Names and exact TeX string matrices are the parameter contract. Explicit invalid requests fail.

Fidelity: 7/7 complete prompts/banks, 37/37 options; 9/9 stored designations and 5/5 existing complete solutions. Two missing designations/solutions remain absent in raw replays and are separately authored in repaired records. Moderate/hard are uncertain authored inspection bands 7–8 / 9–10, preserving every source field contract and classification method. No new linear algebra classes or operations.

validation.json separates fidelity, rendered mathematical checks, finite-domain probes and native categorical grading. review.json contains original records/replays and two variants of every profile at every level; review.md is the readable preview. registered-baseline.json verifies all registered files remain unchanged. artifact-hashes.json freezes private deliverables after validation; parent independent QA is still required.
