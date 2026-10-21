# Generator engine blocker audit — 2026-10-19

This records the original findings before repair. All four blockers have since been fixed and the generators published; see [repair results](../2026-10-19-engine-generators/README.md). Rerunning `audit.py` with the upgraded engine now passes all 18 checks; `results.json` contains that latest result.

At the time of the initial audit, four other saved generator builds reproduced grading failures. That audit made no engine/generator changes and launched no generator jobs or learner attempts.

| Knowledge point | Topic | Current engine blocker |
| --- | --- | --- |
| 17592186096617 — Product containing a trigonometric function | 17592186048813 | Valid `2*4^x*ln(2)*sin(x)` cannot be established equivalent to `4^x*ln(4)*sin(x)`. Both TeX and plain input fail. |
| 17592186096618 — Product containing an exponential or logarithmic function | 17592186048813 | Valid `4^x/(2x ln2)` compared with `4^x/(x ln4)` produces unresolved domain differences. |
| 17592186092261 — General exponential function using the chain rule | 17592186050271 | Valid `-30x^2 ln2` compared with `-15x^2 ln4` is unresolved. Switching canonical form reverses the failure. |
| 17592186096842 — Radical function using the chain rule | 17592186051084 | Wrong answer `0` for `-x/sqrt(1-x^2)` produces unresolved domain differences rather than an incorrect grade. The saved reciprocal fractional-power equivalence failures now pass. |

The logarithm-identity limitation differs from the logarithm interval-range limitation already repaired for knowledge point 17592186087689. The first three require symbolic logarithm normalization, including domain constraint normalization when the logarithm occurs in a denominator. The fourth requires domain-aware rejection of an unequal function.

Scope: inspected current inventory job metadata (7,963 entries), including 88 rejected builds and 364 repair-needed jobs. All 364 repair-needed jobs concern missing approvals or source changes. Reviewed the rejected-build reasons and replayed the four remaining mathematics-engine candidates. Checked pending build jobs' saved errors for engine/grader failures. This does not prove that generators without a saved failing test have no engine limitations. Historical asset-path failures are separate from these confirmed grading failures.

Reproduction: `python3 generate/repairs/2026-10-19-engine-blocker-audit/audit.py`. It runs saved checks individually through `generate/runs/current/check-engine`, records its SHA-256, and preserves intended accepted/rejected outcomes. Diagnostic historical expectations of `unresolved` for mathematically valid answers are strengthened to `accepted`. See `results.json` for individual results and saved source paths.

Read-only EDB registration evidence is in `live/` at basis 5027. The trigonometric product knowledge point still points to its old scratch generator; the other three have no registered generator. Automatic generation remains disabled in `.local/ui.env`.
