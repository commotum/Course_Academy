Current milestone: v1.2.0 implementation and validation complete; ready for independent runner review.

Read feedback first. Retained the repaired workspace, bundled original source, full source banks, math formatter, blank contract and prior evidence. Wrote the instructional repair specification before implementation. No publishing, database operations or edits outside this workspace.

Implementation: P and R radio grids have three constant rows and two competing coefficients, omitting one wrong-constant cell. Choose wrong coefficient side first (equal probability), then a compatible value; choose constant rank and omission independently. This removes the reported quadratic maximum-magnitude bias and additional reciprocal frequency/type cues. P/B n=2..6; R n=3 or 7. The unobserved R5 extension is explicitly rejected. All seven original source cases, including complete original R bank, still replay. Moderate supported; easy/hard unsupported.

Reproduce: evidence/repair-3/commands.md. Script: rank_repair_validate.py, reusing retained validate.py independent parser/grader cases. Runtime manifest: package.json, three standard-library files, Python 3.13.5.

Final checks passed:
- Seven source antiderivatives and 21/21 captured choices; source snapshot equality.
- 840 exact P banks, 64 exact R banks, 300 offset assignments, 43 independently parsed printed banks; 185 fresh P / 126 fresh R, 16 P boundaries, 63 controlled records, four blank regressions.
- Fresh seed 94172863: 480 -> 432 delivered after 48 duplicates; all 311 radios and 233 semantic instances preserved. Reported quadratic maximum-coefficient cue: 17/43 successes vs 1/2 conditional baseline. Exact Fraction-weighted enumeration shows conditional magnitude and frequency strategies each have expected success 1/2 per supported exponent.
- Native grading: 1,526 accepted / 2,639 rejected checks; zero unresolved/unexpected. Includes complete delivered banks and all seven tested cue selections.
- Read-only positive-moderate selector reproduction: 1,024 draws over 432 normal delivered items, 393 unique / 219 semantic instances; no targeted controls added to pool. Live-state/no-policy/zero-weight limits recorded.
- Actual UI: six representatives passed renderer and full screenshot visual inspection (quadratic coefficient sides, P6, R3, R7, blank). No math or layout defects observed.
- Deterministic CLI, relocated declared files, invalid assignments and unsupported bands pass.

Current final reports: evidence/repair-3/pedagogical-variation.json, visual-inspection.json, sampler-probabilities.json and artifact-hashes.json. Historical root evidence and evidence/repair/ are preserved. No unfinished author step remains; runner must independently review before any publication.
