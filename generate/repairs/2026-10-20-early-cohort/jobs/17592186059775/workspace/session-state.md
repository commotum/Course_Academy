# Current state — 2026-10-22, author-178

Read feedback, both retained findings, history and previous state first. Preserve
the completed generator repairs: no new source or runtime defect is demonstrated.
Runtime files and manifest remain byte-identical; hashes are recorded in
`evidence/author178-verification.json`.

Latest failure reproduced first:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_current_handoff.py`
exits 1. The installed `scripts/generator_pipeline.py:723` rejects the unchanged
package before regressions or sampling. Workspace evidence changes cannot affect
this predicate. Changing runtime bytes solely to evade it is not a repair.

Affected checks rerun with the same Python and `-B`:

- `checks/check_evidence_contract.py`: exit 1 at the installed handoff. The real
  review validator accepts the corrected bundle and two relocated copies.
  Missing-provenance and wrong-root controls fail as required. Fresh records match
  retained evidence; 12 source captures and three affected generated inventory
  records bind. No installation is claimed.
- `checks/check_batch_selection.py`: exit 0. At the reported seed, the shortcut
  succeeds 1/5 before and after shared delivery. All five target ranks and
  positions occur; ten profiles are checked. All five records survive delivery
  and 25 actual native grader responses pass.

Commands, exit codes, logs and hashes: `evidence/author178-verification.json`.
Strict regressions remain in `repair-regressions.json`. Prior CLI, source replay
and actual-UI checks are retained; they were not repeated because neither runtime
nor rendering changed.

Next unfinished action belongs to the runner owner: review/apply the staged
`runner-fix/evidence-only-rejection.patch` to `scripts/generator_pipeline.py`, then
resume retained checks, sampling and fresh independent review. Corrected historical
evidence and installation map remain at `evidence/contract-correction` and
`evidence/contract-installation.json`. Historical acceptance is not fresh approval.
The patch is uninstalled.

External runner edits and installation at the runner-supplied evidence root are
outside this session's workspace-only authorization. No external writes,
publication, database writes or engine edits occurred. Another identical author
retry cannot resolve this boundary; do not repeat broad audits or alter working
generator behavior to manufacture a new digest.
