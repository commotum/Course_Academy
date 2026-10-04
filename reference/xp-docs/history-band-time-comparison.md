# Comparing 60/120/180 seconds across Jake's activity history

The candidate assigns Easy questions 60 seconds, Moderate questions 120 seconds,
and Hard questions 180 seconds. Its question-only XP estimate is `E + 2*M + 3*H`.
This comparison uses all 211 activities in `progress.csv` with recorded base XP,
containing 1,384 question occurrences. Eight diagnostics lack base XP and cannot
be compared. No coefficient is refitted, no holdout is used, and earned XP and
actual learner durations do not enter the estimate.

| Type | Activities | Actual base XP total | Estimated XP total | Net difference | Mean absolute error per activity |
|---|---:|---:|---:|---:|---:|
| Lesson | 135 | 1,443 | 1,679 | +236 (+16.4%) | 4.13 XP |
| Review | 53 | 227 | 298 | +71 (+31.3%) | 1.72 XP |
| Quiz | 13 | 177 | 188 | +11 (+6.2%) | 1.46 XP |
| Multistep | 10 | 101 | 107 | +6 (+5.9%) | 1.60 XP |
| All comparable history | 211 | 1,948 | 2,272 | +324 (+16.6%) | 3.24 XP |

There are 133 overestimates, 56 underestimates, and 22 exact matches. 101 of 211
estimates are within two XP. The largest errors are 13 XP in either direction:

- The Chain Rule With Trigonometric Functions, task 12230045: actual 15,
  estimated 28. This attempt contained 12 questions, including additional
  practice after incorrect answers.
- Trigonometric Equations Containing Transformed Tangent Functions, task
  12023822: actual 25, estimated 12. All six answers were correct.

Actual question counts reflect the learner's adaptive route. Base XP is an
expected activity workload and need not grow with remedial question count or
shrink after early failure. Nevertheless, additional practice is not the sole
cause of lesson error: the 89 lessons with every answer correct still have
3.90 XP mean absolute error, compared with 4.59 for the other 46 lessons.

## Adding the previous fitted instructional contribution

For each lesson, the second comparison adds
`0.07513004637186382 * prose_words / 100 + 0.034422123109798704 * example_equals`
minutes, measured from all authored tutorials/examples in its existing reference
lesson archive. It rounds the combined estimate once, using `floor(x + 0.5)`.
It does not add a seven-XP floor. The archive describes captured reference
content, not a confirmed historical version of every lesson.

Adding this contribution increases the total estimate to **2,422 XP**, versus
1,948 actual: **24.3% high**. Overall mean absolute error becomes **3.52 XP**;
lesson mean absolute error becomes **4.56 XP**. This direct combination performs
worse than question bands alone. The old instructional coefficients were fitted
jointly with a different question-complexity model and were not measured reading
times.

## Interpretation

The quiz-derived constants approximate the quiz and multistep samples reasonably
at this scale. Reviews have a substantial upward bias relative to their small
bases. Lessons have much larger errors, including all-correct attempts; global
difficulty bands omit topic-specific computation and setup. The result supports
a coarse question allowance rather than a complete replacement for lesson base
XP prediction. No engine formula or database record was changed.

Sources and reproducibility:

- [Historical capture](../mathacademy/progress-history-2026-10-04/README.md)
- [Detailed per-activity results](history-band-time-comparison.json)
- [Comparison script](compare-history-band-times.py)
- [Original fitted lesson formula](base-xp-formula-report.md)

```sh
/home/jake/Developer/MA/.venv/bin/python reference/xp-docs/compare-history-band-times.py
```
