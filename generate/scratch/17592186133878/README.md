# Local generator evidence

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133878/validate.py
.venv/bin/python generate/scratch/17592186133878/write_evidence.py
.venv/bin/python generate/scratch/17592186133878.py --difficulty all --seed 9 --count 2 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), with generate_easy/generate_moderate/generate_hard wrappers.
`observed_scale` is the explicitly limited complete source bank replay profile;
`authored_endpoint_bank` is the normal default. Explicit parameters fail on
unknown keys, wrong levels, bounds, zero defining coefficients or bank collisions.
Source cases reproduce all twelve originals with symbolic mathematics and their
complete banks. Full prompt/solution prose and stage order are checked after
whitespace normalization, with two documented solution repairs. Review covers
each observed family/profile plus two examples for each of fourteen templates.
Question identity includes actual prompt, solution, complete displayed bank and
mathematical parameters; option shuffling/seed does not create a new identity.
Distinct task counts omit bank/profile/seed. Actual displayed TeX is parsed for
all endpoint, substituted-arithmetic, intermediate and final values; native
memory-only grading accepts the designated option and rejects all four others.

Source.json retains math basis 1356 and lineage unchanged. Hard difficulty and
normal operation banks are explicitly authored. Only steps 3–7 are implemented;
there are no database transactions, registration, shared edits or plots.
