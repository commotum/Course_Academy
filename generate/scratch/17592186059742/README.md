# Linear combination of two matrices

Private local draft only; stops at guide step 7. Immutable source basis 2275. Parent QA has not approved this worker artifact.

Validate: `.venv/bin/python generate/scratch/17592186059742/validate.py`

Preview: `.venv/bin/python generate/scratch/17592186059742.py --difficulty all --seed 2 --count 2 --format json`

Replay: load `source-cases.json` and call `generate(case['level'], template=case['template'], parameters=case['parameters'], profile=case['bank_profile'])`.

Nine families: one authored easy, five moderate (two unrated originals explicitly assigned only in normal output), three observed hard. Five observed radio banks and two four-scalar-blank layouts are public evidence profiles; normal radio banks use the two-product combine method. No plots, DB writes, registration or commits. Raw missing attributes are preserved; three missing solutions/fields are completed only in normal authored records. See template-extraction.md for underidentified banks and the q-320671 table padding repair.

Validation separately reports 8 exact prompts, 6/6 available full solutions, 7/7 complete source banks, 33/33 values and 11/11 available designations. Two missing designations cannot be called source matches. The private validator reads actual printed stages/target columns, exercises every family and profile, fixed-matrix changed targets, negative controls, identity and memory-only native grading. `level-capacity.json` gives exact valid counts within conservative finite subdomains, not a claim to enumerate the entire domain. Calculator requirements unknown.
