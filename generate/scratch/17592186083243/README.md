# Finite slope at a supplied parameter

Implements steps 3–7 only, with no database access or writes. Basis 1356; 18 sources across easy (8), moderate (4), hard (6), grouped into 16 field/value templates. All seven blank sources expect only the slope fragment. Eleven radio banks have five choices.

```sh
.venv/bin/python generate/scratch/17592186083243.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186083243/validate.py
```

The sibling script exposes `generate`, `generate_easy`, `generate_moderate`, `generate_hard`, explicit parameters and complete profiles. `source-cases.json` replays every source through that API. `review.md` shows raw originals, replay records and generated variants. `validation.json` separates full-bank fidelity, independently parsed displayed mathematics, identity/scope checks and real native grading.

All levels are observed. Authored extensions vary coefficients, standard angles and evaluation values within the same methods, and supply complete operation-based default radio banks. Uncertain original scalar banks remain explicit empirical replay profiles, not inferred author intent. Two source domain errors (q-20991, q-348305) are corrected to t>0. Standard equivalent LaTeX and factorizations normalize source mathematical blocks; exact source strings are not claimed as preserved. Shared worked-solution wording, derivative/ratio/evaluation sequence and field layouts remain intact. Normal blanks use “Give an exact answer.” so the native grader accepts meaningful algebraically equivalent entries; `profile="observed"` retains original “Do not round” wording and its native exact-form rejection limitation in separate evidence. Source cases contain `profile` for this presentation replay, separately from nullable `bank_profile`. See template-extraction.md for sampling/eligibility bounds and plot-extraction.md for inspected source plots and renderer specifications.
