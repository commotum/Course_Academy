# Compound-interest answer spacing

Published and live-verified at EDB basis T8285. Updated the three
generators in Continuously Compounded Interest (topic 17592186051065). Replaced
ten generated initial-amount and rate/time questions; preserved all five valid
final-amount questions, six imported practice questions, three canonical examples,
and saved learner references. Reported question 17592186676330 is retired;
its pool replacement is 17592186718510.

The root cause in the initial-amount generator was random numeric jitter around
the rounded key. It limited offsets to approximately 2.5% of that key and could
choose consecutive cents. The reported calculation is
2.23 exp(0.022 × 6) = 2.544671551965934…; 2.54 is correct, but offering 2.55 beside
it makes incidental rounding determine the selection. Imported q-69937 uses
3.05, 3.19, 3.27, 3.37 and 3.43, with a minimum six-cent separation.

The initial-amount generator now derives alternatives from sign, duration,
percentage-conversion and simple-interest mistakes. It rejects collisions and
insufficiently separated banks instead of filling them with tiny offsets.
Choices are at least five rounding units apart, scaled upward to 0.1% of the key
for large dollar amounts. Gas prices therefore have a minimum five-cent gap.
Full-precision decimal exponentiation is used until final rounding, and feedback
shows the unrounded amount. Fresh random cases avoid a narrow half-unit boundary;
explicit source replay remains available. A requested numerical rank is a
preference rather than permission to fabricate implausible mistakes.

The rate/time generator had the same adjacent-integer issue. Its independent
bank-first sampling now enforces the imported families' minimum separations:
two years or three percentage points. The final-amount generator received the
same amount-spacing guard for future draws; its existing banks already passed.
The existing moderate-only generator scope was retained.

The real Publisher preparation path checks displayed values in their rounding
units, including wrong-choice-to-wrong-choice gaps. Recipe metadata cannot hide
a one-cent alternative. Author/reviewer prompts and generator documentation now
require source-supported spacing, final-only rounding and resampling when a
complete eligible bank cannot be formed.

Verification passed: 56 Python tests; independent high-precision calculations
from printed problem data for 285 current/sample record instances; all 75 native
choice-grading checks and all 75 read-only live choice-grading checks; 15 rendered
question previews with selected screenshots inspected; and relocated immutable
package reproduction. The original reported parameters have an explicit
regression: the key remains 2.54 and 2.55 is absent from the rebuilt bank.

Evidence: `completion.json`, `reported-case-regression.json`, `tests.json`,
`generator-verification.json`, `grader-verification.json`,
`live-grading-verification.json`, `render/`, `replacement-map.json`, and each KP's
`publication/` preparation, request, receipt and exact readback verification.
Earlier lesson/source-currency repairs were retained; this repair addresses
answer-bank pedagogy rather than changing imported source answers.
