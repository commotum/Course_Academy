# Cosine periodicity scratch generator

Run `.venv/bin/python generate/scratch/17592186176048/validate.py` for independent display/source/native checks and review regeneration. Preview with `.venv/bin/python generate/scratch/17592186176048.py --difficulty all --seed 42 --count 2 --format markdown` (or json).

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus all three level entrypoints. Parameters contain c,n,a,b. Every source replays through the same parameterized API using source-cases.json. Six templates, seven observed banks, separately authored default banks; no plots, no database writes.

Read classification.md for level scope and actual lesson route; template-extraction.md for all source components, banks and repairs. validation.json separates exact source fidelity, correctness, missing-source authorship and real native grading. review.md/review.json show each source replay and every observed bank variant, plus two default examples per level. The explicit raw q103242 profile preserves duplicate equivalent wrong options only as review evidence; use authored_direct or the minimal repaired observed_q103242 bank for learner output. Source missing correct refs/solutions remain missing in source.json. freeze-hashes.json captures reviewed artifacts and native grader provenance.
