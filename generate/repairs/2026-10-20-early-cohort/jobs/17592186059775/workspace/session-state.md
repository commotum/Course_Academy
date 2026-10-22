# Current state — 2026-10-22, author-32

The Gaussian-elimination runtime and manifest are preserved byte for byte.
Package hash: 38c685ce1e5bd4f89ac79b6ab3d31a4a81f2b77c9f4bb6f0abcab5c20640f626.

Feedback/history read first. Exact wrong-root provenance failure and current
unchanged-package gate reproduced. Source replay (10 banks/50 choices), exact
mathematics, native grading, CLI, delivery, inventory and batch-selection checks
pass. Report and exact commands: evidence/author32-report.json. Runtime/UI are
unchanged; fresh render binding passes and one retained screenshot was visually
reinspected. No new renders were needed for this check-only change.

Completed regression repair: checks/check_current_handoff.py executes installed
runner sample-stage control flow with actual current inputs. Writes, process
launches, sampling and service boundaries are instrumented. It exits 1 because
the runner actually rejects before regressions/sampling. The registered
checks/check_evidence_contract.py now propagates that failure, instead of
passing on an uninstalled proposed patch. Its local evidence bundle still
passes validation; its combined result correctly reports passed=false.
Evidence: evidence/current-handoff-regression.json,
evidence/author32-evidence-strict.log. This is a strict failing regression,
not a completed handoff repair. Other registered checks still pass.

Status: unsupported because the current handoff remains unresolved. The
existing runner-fix/evidence-only-rejection.patch is only staged. The runner
owner must review/install a correction outside this workspace, rerun the strict
current check and retained regressions, then sample and obtain fresh independent
review. Do not edit working runtime solely to obtain a new package hash, install
historical acceptance as new approval, or repeat unaffected tests. No engine,
database, publication, services, other-job or outside-workspace writes occurred.
