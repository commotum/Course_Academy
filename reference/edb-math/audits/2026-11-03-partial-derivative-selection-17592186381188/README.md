# Partial-derivative practice selection audit

Read-only audit at math T12481. Reported question 17592186381188 is imported q-159592 in KP 17592186124643, Partial Derivatives as Limits of Difference Quotients, within topic 17592186048707, Introduction to Partial Derivatives. Shared lesson activity: 17592186124722. Current learner task: 17592186675844.

The canonical example asks for an x derivative. The first three actual practice presentations requested y (easy, hard, moderate); the fourth, 17592186562843, requests x. Native selection logic was independently replayed from the task/KP/slot SHA-256 seeds, matching all four actual question IDs. Pool usage shows no earlier-task exposures to exclude, and no pool questions are multipart or retired. No lesson state was changed.

| Rated band | x questions | y questions |
| --- | ---: | ---: |
| Easy | 9 | 3 |
| Moderate | 0 | 6 |
| Hard | 4 | 2 |

There is also one unrated y question. The selector uses unrated questions only when no positively weighted rated band is available, so that question does not affect these draws. Lesson weights are 45% easy, 40% moderate, 15% hard in both initial and remedial phases. Selection is stable and random within the chosen band, with no requested-variable coverage rule. Three initial y practice draws have probability about 17.1% under this pool and without-replacement selection. This is not an intended y-only teaching stage.

All five moderate imported anchors target y. The newer generated moderate question also targets y. The current v6 generator alternates physical target variables within generated batches and can swap roles while retaining the requested substitution workload, but these capabilities have not balanced the existing live pool. Inventory refill measures counts by difficulty and stops at five available questions per band; it does not measure coordinate coverage. There are already six moderate questions, so the missing x coverage does not itself trigger replenishment.

Question 17592186562843 was reproduced exactly, including UUID c62e1658-4438-5b1a-b0a2-228bb5838b57 and stem, using generate/scratch/17592186124643-draft.py, version partial-quotient-v1, point_monomial, parameters a=1, X=1, Y=2, swap=false. Its original additive publication is documented at basis 2750 in that draft's reference/replenishment/basis-2749/verification.json. The v1 hard sampler permits coefficient 1, then prints str(a) in both the polynomial and every substituted product; it does not omit multiplicative identities or combine constant numeric factors. This yields an unnecessary leading 1 and repetitive 1(...) products throughout the choices and solution.

A unit coefficient is legitimate for a difference-quotient concept question. Several imported anchors have implied unit coefficients, such as x^y and sin(xy). It does not remove the need to increment the requested coordinate and hold the other fixed. The defect is literal parameter printing, combined with continued availability of an older authored point-substitution hard family. Five v1 point questions remain in the active hard pool, despite the registered generator now being partial-quotient-v6 (generators/e1/e18ef6e597f04130371003fd697cf44bf9908f8d9c73aba9679c73a14382bf3c/generator.py). The current generator explicitly omits unit coefficients and no longer generates that point-specialized family.

Recommended repair: balance coordinate roles within each difficulty band while retaining each band's substitution workload; replenish by coverage as well as count; retire superseded generated material from fresh selection while preserving saved presentations; normalize neutral numeric factors rather than banning coefficient 1. Coordinate coverage should describe the mathematical role, rather than assuming a letter determines difficulty.

Evidence: capture.json, kp.json, the other two KP captures, lesson.json, policy.json, served-owners.json, pool-usage.json, source-exclusions.json, selection-replay.json, old-generator-replay.json, and the audit copy current-generator.py. No database mutations or learner attempt writes were performed.
