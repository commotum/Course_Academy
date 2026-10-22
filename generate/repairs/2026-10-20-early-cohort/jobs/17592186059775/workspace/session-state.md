# Current state — 2026-10-22, author-235

Read feedback and full repair history (two findings, 235 events). Preserved the
runtime, manifest, instructional specification and completed repairs.

First reproduced the exact latest failure:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. Actual installed runner calls `repair` before regressions or sampling:
“Candidate is byte-identical to the rejected package.”

Commands, log paths, exit codes, hashes and separate claims are recorded in
`evidence/current-author-verification.json`.

Affected checks rerun:
- Historical shortcut remains a strict failing negative control (5/5).
- Current shortcut/delivery check passes: 1/5 raw and delivered; all five answer
  ranks/positions and ten retained profiles; 25 native grades pass.
- Corrected evidence bundle passes the real validator, including relocation and
  missing-provenance/wrong-root negative controls. Its registered regression
  exits 1 because the installed runner handoff remains failing.
- Relocated CLI counts/determinism/finite limit and source/render binding pass:
  ten complete source banks / 50 choices. Both retained actual-UI screenshots
  were visually inspected and remain bound to current delivered endpoints.
- Manifest dependency versions and both retained finding registrations checked.
  Runtime and manifest bytes unchanged. Earlier broad validation retained.

Remaining action: the runner owner must resolve the evidence-only rejection gate
at `scripts/generator_pipeline.py:720-727`. A concrete, previously tested proposal
is retained at `runner-fix/evidence-only-rejection.patch`; it is not installed.
The authorized workspace excludes that target. No workspace runtime edit repairs
that runner rule, and altering runtime bytes solely to evade it is not a fix.

No database, publication, engine, runner, other-job or external evidence-root
writes occurred. Status remains unsupported for end-to-end handoff; easy source
support and the completed generator repairs remain preserved.
