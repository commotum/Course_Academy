# Current source classification and bounded generator reuse

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1; current capture basis 2696. `initial/kp.edn` contains all eleven current practice questions and the canonical example, including every complete field, bank, solution and image reference. Capture is separate from the frozen basis-1356 `source.json`; no source or learner facts are revised.

The existing validated cylindrical-solid-2 generator is reused. Its source replay covers eight historical practice sources, nine banks, 45 exact displayed options (35 modern, 10 legacy), seven original correct designations and seven original worked solutions. Two historical missing correct designations are omissions, not successful matches. The new current evidence does not change the frozen sampler's mathematical families. Current complete-bank fidelity is not claimed for the three later families below. Its easy and moderate source families and explicitly authored hard extension remain supported, with actual generated-instance checks required before preparation. No new operations, shifted cylinders or requests to evaluate integrals are added.

| Current source | Difficulty and template | Field/bank | Decision |
|---|---|---|---|
| q-161520 | moderate, right-half xz with sloping top | one radio, five options; now rated, complete solution and correct ref | Independent prompt, complete integral bank, solution and grader validation |
| q-39481 | easy, full disk z times radial root | two radio fields sharing selection; legacy flattened math, one missing correct | Excluded; retain both fields/history unchanged |
| q-161605 | easy, full disk z² times radial root | radio, five options | Independently validate |
| q-161607 | easy, full disk inverse sqrt(1+z), spherical top | radio, five options; current initial solution LHS now repaired | Independently validate |
| q-161611 | moderate, left-half difference squares, two nonconstant heights | radio, five options | Independently validate |
| q-161612 | moderate, upper half z times difference squares | radio, five options | Excluded: extra r in expanded solution stage; normal generated solution already repairs it |
| q-161613 | moderate, upper-left spherical-top volume | radio, five options | Independently validate |
| q-161604 | easy, cone lower height and radial-root integrand | radio, five options | Independently validate |
| q-161603 | easy, full disk, z, spherical top | radio, five options | Excluded: a nonreal distractor integral; classify only, generator not extended |
| q-161609 | moderate, first-quadrant 2xy, constant lower and paraboloid top | radio, five options | Excluded: two equivalent zero distractors; classify only, generator not extended |
| q-161602 | easy, full disk z², lower constant and sloping top | radio, five options | Excluded: stated upper/lower ordering reverses inside projection; classify only, generator not extended |

The canonical e-11470 is context and never practice inventory. Actual pool availability also excludes any previously shown or reserved content, using historical question exposure reads and current reservation reads at the same captured basis. Native `assessment_sampling::pool` supplies gradability exclusions; independent mathematics imposes the additional exclusions above. No flawed existing question is deleted or silently corrected.

## Later source component and bank extraction

All three later sources ask to rewrite a complete triple integral with order dz dr dtheta, use a single five-choice mathematical radio field named selection, and show the same coordinate-substitution opening, projection, two height descriptions, a cylindrical region set and a final substitution chain. Their plots occur only in the solution and require parameter-dependent geometry if generation is later supported. All three are rated moderate in plot workload: full disks for q-161603 and q-161602, first quadrant for q-161609. These are distinct Markdown/value templates because the integrands/heights and simplification stages differ. Each has one source bank profile; none is silently merged into the frozen bank.

Tuple notation below is `(theta lower, theta upper, radial upper, z lower, z upper, integrand)` with radial lower zero. Every original displayed option maps to the following whole object; exact UUIDs and strings are retained in the current capture.

q-161603: observed S=16, K=25, supplied z, requested converted integral, full disk. Generic correct tuple C=(0,2pi,sqrt(S),0,sqrt(K-r²),rz). Ordered by captured answer UUID, bank operations are: C with upper sqrt(K-r); C with radial upper S and integrand z; C with integrand z; C itself (designated correct); C with radial upper S and upper sqrt(K-r). First and last errors drop the square in the upper height; the last also uses squared radius as radial upper. The squared-radius distractor retaining sqrt(K-r²) leaves its real height domain at r>sqrt(K); the other squared-radius distractor uses sqrt(K-r), which remains real at the observed parameters. Solving that requires a bank repair or explicit exclusion, not counting them as valid source replay.

q-161609: observed S=2, L=1, H=4, supplied 2xy, quadrant x>=0,y>=0, lower L and upper x²+y²+H. C=(0,pi/2,sqrt(S),L,r²+H,r³ sin(2theta)). Bank: C with integrand r²sin(2theta); C with theta upper pi; C itself (correct); C with theta upper pi, height r+H and integrand r²sin(2theta); C with height r+H. The two options with theta upper pi both integrate to zero because the remaining factors are independent of theta. Preserving the source strings is fidelity evidence, not proof of bank uniqueness. No repaired sampler for this template is claimed.

q-161602: observed S=5, L=2, H=4, supplied z² and top H+y on a full disk. Formally C=(0,2pi,sqrt(S),L,H+r sin(theta),rz²). Bank: C with radial upper S and sin->cos in height; C with integrand z²; C with constant height H; C itself (correct designation); C with radial upper S, constant height H and integrand r²z². Since H-L=2<sqrt(5), the purported upper surface crosses the lower one. The solid between the surfaces has min/max heights, so the displayed one-piece region and its key do not express that solid. No correct repair is inferred or committed. A future same-method sampler would need H-L>sqrt(S), with full replay/repair evidence before support.

Current q-161520's complete bank matches the historical interpreted xz bank. Its source repair now supplies the correct r²z cos(theta) and the same right-half bounds. Frozen historical omissions and flattened bytes remain preserved for audit; they are not copied into normal output.

## Capability and variation

Supported levels are easy and moderate observed workloads and the existing authored hard `quarter_zdifference`: upper-left quadrant, z(x²-y²), lower x, upper H+y² with H>=1. It combines quadrant bounds, the difference-square identity, an unchanged z factor, and two nonconstant heights. This is a local workload classification anchored in the original canonical/lesson/prerequisite evidence, not an empirical difficulty calibration. Heights remain ordered throughout the sector. The sampler has finite radius/height domains and rejects entire banks when any option is equivalent, nonreal or invalid. Neither source profile aliases nor option order count as new tasks.

The requested rewrite is identified by its six exact cylindrical bounds/integrand components, excluding difficulty, identity, solution, seed and bank. All source questions and canonical context participate in deduplication even when ineligible as fresh inventory. Generated variants change actual cylinder/height parameters; no cosmetic replay is admitted. Normal output uses existing supported radio grading, field-owned answers and one concrete worked solution. Source and generated projection plots are inspected separately.
