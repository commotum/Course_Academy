# Four generator repairs and answer-checking upgrades

All four repaired generator candidates are published, registered and approved. Each has five new questions. Live verification at EDB basis 5053 confirms all three affected topics are available for study, valid answers and equivalents accept, and wrong answers reject. No learner attempts were created by verification.

| Knowledge point | Topic | Certificate | Published basis |
| --- | --- | --- | --- |
| 17592186096617 — Trigonometric product differentiation | 17592186048813 | easy | 5050 |
| 17592186096618 — Exponential/logarithmic product differentiation | 17592186048813 | easy | 5051 |
| 17592186092261 — General exponential chain rule | 17592186050271 | easy | 5052 |
| 17592186096842 — Radical chain rule | 17592186051084 | moderate | 5053 |

The prior generator authors had already repaired the source-family omissions, missing solution stages and radical answer-bank shortcut in their isolated candidates. Those runtime packages were preserved and published after the engine limitations were removed. The source families and learner input forms were not narrowed to avoid grading failures.

`engine/rust/symbolic.rs` now expands logarithms of positive rational constants into exact sums of logarithms, with bounded factorization. This proves identities such as `ln(4)=2ln(2)` in numerators and denominators. Symbolic product-log identities with potentially negative factors are not assumed. Exact fractional counterexamples allow rejecting wrong radical derivatives inside bounded domains, including `0` versus `-x/sqrt(1-x^2)`. These witnesses prove inequality only; answer acceptance still requires exact symbolic equivalence and matching domain obligations.

Validation: all 163 Rust library tests pass, including new identity/domain regressions. The four generator reviews include 2,651 native grading checks with zero unresolved outcomes and 53 successful actual-UI renders; representative blank and radio screenshots were visually inspected. Saved source-replay, math, canonical, decision-variation, filtering, relocation and rendering evidence lives in each knowledge point's `independent-review/`. `summary.json` records counts and package registrations; `verification.json` records live checks on published and original source questions.

Review provenance: the current Codex session reviewed candidates authored by earlier, separate generator sessions, reusing their previous independent reviewers' parsers and source accounts and rerunning the checks against fresh source/inventory snapshots at basis 5048. Source changes were presentation repairs. The current session authored the engine changes. No new author or reviewer agents were launched. `publish_reviewed.py` consumes these completed review records through the existing pipeline's review contract, package hashing, guarded publication, receipt verification and approval recording.

The live application uses `.local/graph-explorer/learning-50ea46b0b29cfe88`. Automatic generation remains disabled both in `.local/ui.env` and the running service environment. `service-verification.json` confirms the service is active and no generator/scoped publication jobs remain. The broader automatic pipeline was not restarted.
