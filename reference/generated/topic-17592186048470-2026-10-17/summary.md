The question shortages blocking **The Change of Base Formula for Logarithms** (`17592186048470`) are cleared. Two generators passed all eight independent review checks, were published with verified registration/readback, and added ten questions.

| KP | Skill | Usable before | Usable after | Published band |
|---|---|---:|---:|---|
| 17592186054744 | Rewriting with change of base | 2 | 7 | Moderate |
| 17592186054745 | Calculator evaluation | 3 | 8 | Easy |
| 17592186054746 | Exact evaluation | 7 | 7 | No new generator required for admission |

The final native `lesson_ready` check passed at basis 3427 with no shortages. It read only these three KP banks and the learner's own relevant history: zero global attribute scans, zero writes, and zero learner attempts created. See [final readiness](after-readiness-3427.json) and [publication summary](summary.json).

The running app includes two tested grading repairs: equivalent decimal spellings such as `.850`, `+0.850`, and `00.850` preserve required precision; MathLive fraction spellings such as `\frac14` match `\frac{1}{4}` while unreduced answers remain rejected. The app was rebuilt, restarted, and checked against the expected native binary. See [runtime verification](final-app-verification.json).

The inventory finder also received a two-clause ordering fix to prevent an accidental Cartesian product. The original broad finder read was not repeated manually; the fix passed an offline reproduction and all 11 native finder tests plus 19 ranking tests. The grading repairs passed 36 learning tests and targeted native/UI regressions.

The optional exact-evaluation generator remains a local draft. Its new answer banks need further design to remove sampling shortcuts without distorting the lesson's workload. It was not published; existing question stock already satisfies admission. Its source and independent-review evidence are retained under `.local/generation/math/17592186054746-auto/`. Source captures were not recaptured or overwritten by this work.
