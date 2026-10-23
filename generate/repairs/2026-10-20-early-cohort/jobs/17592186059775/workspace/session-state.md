# Current state — 2026-10-22, author-278

Read latest feedback, retained findings, final history event, existing session state,
and required generation/validation guidance. Reproduced the latest failure first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. Installed runner rejects this byte-identical package before retained checks
or sampling (`scripts/generator_pipeline.py:723`).

Executed every registration in repair-regressions.json. Results and commands:
`evidence/author278-regressions.json`, `evidence/author278-verification.json`.

- check_all.py: exit 0; CLI relocation, exact complete source replay, independent
  mathematics, native grading, shared delivery and historical inventory pass.
- check_batch_selection.py: exit 0; original seed and within-profile controlled
  answer-role changes pass before and after shared filtering; native grades agree.
- check_evidence_contract.py: exit 1; staged bundle validates at both relocated
  roots with failing negative controls, but installed runner handoff still fails.
- check_render_binding.py: exit 0; ten complete source banks and two actual UI
  previews bind to current output. Inspected question-001.png: readable prompt,
  five choices and full solution. Reused the unchanged actual UI rendering.

All runtime/package bytes match author-277. Strict regressions remain intact.
No generator defect justifies changing runtime bytes to evade the runner gate.
The retained evidence-only finding explicitly requests preserving those bytes.
No publication, database, engine, external runner, or other-job edits occurred.

Unfinished: runner owner must review and apply the already staged
`runner-fix/evidence-only-rejection.patch` outside this workspace, verify its
strict handoff regression, and route corrected evidence to fresh review.
Current workspace-only authorization cannot install it. Further identical
workspace author retries cannot change the external predicate; do not substitute
cosmetic package changes, historical acceptance, or weakened tests for repair.
