# Current state — 2026-10-22, author-312

No implementation changes. Preserved runtime, manifest and strict registered
regressions. Read latest feedback and both retained findings, prior state,
required guidance, source questions, canonical example, lessons and prerequisite
context. Existing instructional account remains applicable; no new generator
defect was demonstrated.

Reproduced latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1 before regressions or sampling. The current byte-identical-package gate
conflicts with the evidence-only finding's explicit runtime-preservation request.

Fresh verification: `evidence/author312-verification.json` contains exact commands,
exit codes, log paths and unchanged runtime hashes.

- Batch-selection regression: PASS; exact seed 4258185931 has 1/5 shortcut hits
  raw and delivered, all five target ranks/positions, 25 native grader checks.
- Evidence-contract regression: FAIL solely at strict installed handoff. The
  83-file bundle validates after relocation; historical missing-provenance and
  wrong-root controls reject; current records and three affected stored generated
  records remain bound. No external installation was attempted.
- CLI contract: PASS; relocated runtime, deterministic exact counts and finite
  limits.
- Source/render binding: PASS; ten complete banks and two unchanged rendered
  endpoints match. Visually inspected question-001.png: readable and unclipped.

No package, engine, database, publication, external runner or other-job edits.
No checks weakened. Avoid repeating identical author validation without an
external state change.

## Next unfinished step

The runner owner must review/apply `runner-fix/evidence-only-rejection.patch`
to `scripts/generator_pipeline.py` outside the authorized workspace, then rerun
`checks/check_current_handoff.py` and retained regressions before independent
review. The patch remains uninstalled; offline proposal checks do not establish
an installed repair. External evidence installation is also runner-owned.
