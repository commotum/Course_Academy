# Current state — 2026-10-22, author-45

Preserved completed generator repairs, runtime files, manifest, scripts and
regression registrations. Read feedback and the two retained findings in the
45-event history. Reused existing source analysis and instructional account;
no runtime or instructional change is justified by an evidence-only defect.

Exact latest reproduction:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`

Exit 1. The installed runner calls repair before regressions or sampling because
package, source and engine match the last rejected binding. Responsible rule:
`scripts/generator_pipeline.py:723`. Finding 9b8cb52352b8ca3e790e explicitly requests
an evidence-only correction and preservation of runtime. The runner and requested
external evidence installation destination are outside authorized writable roots.

Fresh commands, logs, exit codes and unchanged runtime hashes:
`evidence/current-verification.json` and `evidence/current-check-commands.json`.

- Evidence correction validates at its own root and two arbitrary relocated
  roots; wrong-root and missing-provenance controls fail correctly. Current-record
  and three historical generated-record bindings pass. Registered check remains
  exit 1 because its strict installed-runner check fails.
- Batch regression: exit 0; exact seed 4258185931 shortcut scores 1/5 raw and
  delivered, five records survive actual filtering, ten profiles pass, and
  25 native grading responses match expected outcomes.
- CLI regression: exit 0; relocation, requested counts, determinism and finite
  limit preserved.
- Source/UI binding: exit 0; ten complete source banks and 50 choices replay.
  Retained actual UI records match current delivered endpoints. Reinspected
  `evidence/author8-render/question-001.png`; prompt, choices and solution readable.

No runtime, runner, engine, other-job, database, publication, or live-service
changes. The existing runner patch is an uninstalled proposal; its prior 23-case
verification remains available. That unchanged patch test was not repeated.

Unfinished: runner owner must install the corrected evidence bundle at the proper
root or correct its evidence-only rejection routing, then rerun the strict handoff
and fresh independent review. Bundle: `evidence/contract-correction`; copy plan:
`evidence/contract-installation.json`; proposed routing correction:
`runner-fix/evidence-only-rejection.patch`. Do not mutate runtime to evade the
identity gate, weaken the strict regression, or treat historical acceptance as
fresh approval. Handoff status remains unsupported; targeted content checks pass.
