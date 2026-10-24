# Original source bank repair

Original question q-107463 asks for the tangent to `y=4^(2x+1)` at `x=-1`.
Its correct answer was already mathematically correct. The distractors exposed
the key through repeated slope coefficients and intercept form, so the learner
could choose it without using the curve.

Four wrong-choice values were changed so all five lines pass through `(-1,1/4)`.
Their distinct slopes are `ln(2)`, `2ln(2)`, `-ln(2)`, `-2ln(2)`, and `ln(2)/2`.
Only the unchanged key has the correct derivative. The old bank-only rule now
abstains. The same complete bank also supports different curves and keys; this
single source repair does not certify a universal generator sampling rule.

Independent review bound the exact before/candidate hashes and checked the
displayed mathematics, native radio grading, counterexamples, and actual UI
render. Commit required fresh checks that the question had no saved task items
or answer responses. The guarded native transaction changed exactly four
answer-value facts at basis 6468. Exact readback passed; question, key, solution,
difficulty, identities, learner facts, and engine facts were preserved.

Evidence: `before.json`, `candidate.json`, `independent-review.json`,
`grader-verification.json`, `render/rendering.json`, and `verification.json`.
