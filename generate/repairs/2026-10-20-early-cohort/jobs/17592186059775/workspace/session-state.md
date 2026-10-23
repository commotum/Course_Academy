# Current state — 2026-10-22, author-275

Read latest feedback, both retained findings and history (275 prior events).
Reproduced exact latest failure first: job Python `-B checks/check_current_handoff.py`
exits 1. Installed sample-stage runner rejects byte-identical package before
regressions and sampling. Confirmed actual gate in scripts/generator_pipeline.py.

Targeted verification (job Python, `-B`):

- checks/check_evidence_contract.py: fails strictly with exit 1 only at installed
  handoff. Bundle validates under two relocated roots; wrong-root and missing
  provenance controls reproduce. Twelve captures and three generated records bind.
- checks/check_batch_selection.py: passes. Exact seed 4258185931: five accepted
  after shared delivery; pivot/rank cue 1/5 raw and delivered. All ten profiles
  checked; native grader accepts five correct and rejects twenty incorrect choices.
- checks/check_cli_contract.py: passes relocated deterministic CLI, requested
  counts 0/1/5, supported bands and finite-limit rejection.
- checks/check_render_binding.py: passes ten complete banks and current UI input
  binding. Reinspected author8-render/question-001.png: readable matrix notation,
  five choices, controls, and correct elimination solution. Reused unchanged UI.

Commands, logs, claims and runtime hashes: evidence/author275-verification.json.
All six manifest/runtime files exactly match preserved baseline. No new defect
justifies changing instructional construction. Existing instructional account,
package and strict registered regressions preserved.

Unfinished action is outside permitted writes: runner owner must install the
reviewable evidence-only gate repair (runner-fix/evidence-only-rejection.patch)
in scripts/generator_pipeline.py and install the evidence bundle using the
runner-supplied evidence root. Then rerun strict handoff/evidence regressions and
fresh independent review. Proposed fix remains uninstalled. Do not weaken tests,
change runtime bytes to evade the gate, or repeat author-only retries expecting
external state to change. No database, publication, engine or other-job edits.
