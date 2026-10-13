# Bounded open interval generator

Run `.venv/bin/python generate/scratch/17592186059826/validate.py` from repository root. It exhaustively parses the displayed mathematics of 4116 finite tasks, compares both original complete banks, checks the canonical solution, tests guards and stable identities, and invokes the real native radio grader on originals plus every family and level.

Preview: `.venv/bin/python generate/scratch/17592186059826.py --difficulty all --seed 7 --count 2 --format markdown`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Templates: `inequality_to_interval`, `interval_to_inequality`; profiles: `original_bank` (normal independently enriched output), `source_raw` (public parameterized replay of original missing attributes). Exact parameters use `a`, `b`, optional `variable` in x/y/t/z. Equivalent rational spellings canonicalize. Both profiles accept the same authored level domains.

Two unrated captured practice questions have complete five-option radio banks but no keys or solutions. Those omissions are preserved in raw replay and reported separately from derived keys/authored solutions. All levels and endpoint sampling policies are authored and documented in classification; only bounded open intervals are assessed. No plots, engine edits, database operations or registration. Native equivalent free-entry submissions are inapplicable to radio fields; independent set-semantic parsing establishes displayed-value equivalence separately from selection grading.
