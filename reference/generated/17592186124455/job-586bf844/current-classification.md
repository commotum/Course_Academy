# Current tangent-vector inventory classification

The job was queued at basis 1831. The live pre-generation inventory and complete KP pull record the newer basis and the same math lineage, `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The original generator snapshot remains frozen at basis 1356. All fifteen current practice records, complete answer banks, correct references, solutions, difficulty facts and the canonical example are retained in `pre-generation/kp.edn`; the authoritative preparation copy is `basis-*/before.edn`. Pull explicitly disables the default membership limit.

Every current practice question is rated moderate, with one radio field and five choices. Each source ID below is retained as an individual prompt/solution/bank profile. None requires a plot. The source templates already extracted for the first eleven questions retain their complete original-bank replay evidence. The four later source questions are added evidence; they do not expand the generator's bounded authored sampling domain.

| Source | Implicit expression or supplied equation | Point | Template and plot requirement |
| --- | --- | --- | --- |
| q-36391 | x²y − xy = 4 | (2,2) | Mixed polynomial; none |
| q-65204 | cos(x)cos(y) = sin(xy) | (0,π/2) | Trigonometric product and chain rule; none |
| q-130198 | x cos(y) + y sin(x) = π/2 | (π/2,0) | Trigonometric mixed products; none |
| q-130200 | x exp(y²+1) + y = e | (1,0) | Exponential chain rule; none |
| q-37516 | 2x ln(y) − 8xy = 2−8e | (1,e) | Logarithmic product; none |
| q-72400 | x²+y²−2xy = 9 | (−1,2) | Quadratic difference; none |
| q-72463 | 2x³y²−4xy+3x = 1 | (1,1) | Higher mixed polynomial; none |
| q-130201 | xy+x²+y³ = 3 (source) | (−1,−1) | Mixed polynomial with source point-membership error; none |
| q-72388 | x²y−x = 1 | (1,2) | Mixed polynomial; none |
| q-130192 | x²y−y² = 3 | (2,1) | Mixed polynomial; none |
| q-130194 | x ln(y)−x² = −1 | (−1,1) | Logarithmic product; none |
| q-72403 | (x−y)² = 2x−y | (2,0) | Squared difference and rearrangement; none |
| q-130203 | y² = 1−x²+2y | (−1,2) | Rearranged sum of squares; none |
| q-65205 | x exp(y)−1 = xy | (1,0) | Exponential mixed product; none |
| q-72389 | 2 exp(xy) = x+y+1 | (0,1) | Exponential chain rule and rearrangement; none |

The new profiles retain their exact five choices and correct designations in the pull evidence. Their historical distractor intentions remain unasserted. Their solutions rearrange the equation, define a level function, apply `(f_y,−f_x)`, differentiate, substitute the supplied point, and state the resulting vector. No new template or distractor recipe is inferred from their literals.

Current validation reports each question separately. q-72463 has a false level statement; q-130201 supplies a point outside the displayed curve. q-72403 cannot pass the full displayed-math parse. These source records are preserved and excluded from the validated reserve. The remaining moderate questions are checked mathematically and through the current native learner grader. Historical task-item exposure and active reservations are excluded at the same captured basis. Exact counts and exclusion evidence are in `current-pool/available-counts.json` and `final-pool/available-counts.json` under the committed batch.

The validated generator retains three separate authored templates: easy quadratic, moderate mixed polynomial, and hard logarithmic product. Each uses the same tangent-vector method, one field, five complete choices and the original ordered solution stages. Easy and hard labels are workload classifications, not claims about observed source labels. Coefficient, evaluation-point, domain and arithmetic bounds remain those in the original classification and extraction. The authored bank is the complete `method-bank` profile; historical opaque banks remain evidence-only. No plot or asset publication is required.

Source fidelity, mathematical correctness and native grading remain separate evidence. The full replay validation checks eleven original questions, twelve original banks and sixty options, plus 240 authored samples. Every selected instance receives a fresh displayed-math audit, deterministic replay, a changed-seed identity check, a complete-bank native grading check, and a mathematical fingerprint check against all existing practice questions and the canonical example. Fingerprints normalize the implicit equation up to a nonzero constant and retain the exact evaluation point; choice order, seed and identity cannot create inventory.

The commit adds only selected fresh instances and generator registration. Exact EDN, contributor, expected basis, request key, preview, durable receipt and exact-basis readback are retained in the batch directory. The application lock covers the current inventory recheck through submission and readback. The receipt audit permits only additive facts on the requested KP and its new generated content, plus transaction time; all existing questions and the canonical example must compare unchanged.
