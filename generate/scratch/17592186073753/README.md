# Challenging integer-coefficient substitution systems

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186073753/validate.py
.venv/bin/python generate/scratch/17592186073753.py --difficulty all --seed 12 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`.
Default profile `method` creates valid five-choice radio assessments. All levels
are author-designed because the three captured originals are unrated. Source
profiles are explicit empirical replay, not recovered authoring algorithms.
`source_q12457_raw` is incomplete evidence with five wrong options and no correct
ref; `source_q12457_repaired` is the supported minimal bank repair. Raw anomalies
are documented, never silently counted as valid native assessments.

Validation independently reads the printed equations, all isolate/substitute/
distribute/collect/back-substitute rows, final tuple or scalar and complete banks.
It also checks source fidelity, level guards, content identities, genuine task
variety, source malformed-brace repair and real application native grading.
`source.json` and `authoritative-lesson-487.json` preserve raw evidence. See
`validation.json`, `review.md`, `source-choice-map.json` and extraction documents
for fidelity counts and limitations. No plots, database writes or registration.

## Current system display repair (2026-10-16)

The registered generator now constructs systems with the shared `system_tex` helper: separate equation rows, explicit equation-label columns, and a single operation bar where applicable. Whole-equation multiplication stays grouped. The change preserves sampling, difficulty, mathematical task fingerprints, complete answer banks, and correct keys. Original source snapshots and raw replay prompts remain historical evidence.

Run the current presentation regression and native grading checks from the repository root:

```sh
.venv/bin/python reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/verify.py
```

That harness compares retained pre-repair generators with current output across every supported template and difficulty, invokes the historical mathematical validators on the baseline, checks arithmetic and answer equivalence, and grades current output with the native engine. It avoids the historical validators' semicolon-only display parsers. Current render evidence is in `reference/mathacademy/repairs/2026-10-16-system-equations-display/generators/`.
