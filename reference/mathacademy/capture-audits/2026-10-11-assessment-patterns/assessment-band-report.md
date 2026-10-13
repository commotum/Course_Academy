# Displayed bands before quiz offers

Date: 2026-10-11. Read-only analysis of saved captures.

## Finding

The captures contradict a rule requiring displayed band 2 or higher, either at the time a topic is first quizzed or at some captured time after its lesson. The lowest blue band is enough in observed cases. A successful lesson followed by roughly 48 hours is consistent with the evidence even when we observe no direct review and no subsequent displayed progress.

This does **not** prove that the topic received zero implicit repetition credit. Credit can change without crossing a color threshold. Display bands are ordinal observations, not measured continuous repetition counts, mastery probabilities, or backend eligibility flags.

## Method and coverage

The analysis read 3,076 saved knowledge/post-activity snapshot files across the four accounts. It indexed each selected topic under its own account and used the course page's `captured_at`, not the enclosing snapshot completion time. For each question it selected the latest observation strictly at or before the first saved quiz offer. Later observations are retained separately and are not used as pre-offer evidence. Thus an assessment's results cannot supply its own eligibility evidence.

There were 416 ordinary quiz question appearances (retakes excluded). Of these, 384 had a numeric prior band; 368 had a numeric observation within an hour before the first saved offer. The latter distribution was:

| Band | Question appearances |
|---:|---:|
| 0 / white | 0 |
| 1 / lightest blue | 36 |
| 2 | 175 |
| 3 | 34 |
| 4 | 14 |
| 5 | 16 |
| 6 / darkest blue | 93 |

All 36 recent band-1 cases are distinct account/topic pairs at their **first observed ordinary quiz appearance**, spread across 14 quizzes. They are not repeated questions inflating a count. Membership checks against the enrolled courses' `Topics.csv` files identify **10 native-course topics and 26 prerequisite topics**. Thus the low current band is not confined to prerequisite questions. Thirty-six examples reject a current displayed-band threshold of 2 or 3, but cannot on their own reject a threshold reached earlier and subsequently reduced.

## Strongest cases: no direct review, never observed above band 1

The earlier review audit identifies 58 traceable first-quiz topics without any captured intervening direct review. Five of these never exceed band 1 in their captured post-lesson histories:

| Account | Topic | Lesson task | Quiz task | Lesson age at offer | Saved band observations |
|---|---|---:|---:|---:|---|
| foundations | 1609 — Properties of Transformed Exponential Functions | 13943819 | 14003941 | 49.17 h | 356 at band 1 |
| foundations | 5088 — Finding Zeros and Extrema of Transformed Sine and Cosine Functions | 13944893 | 14006735 | 50.55 h | 376 at band 1 |
| foundations | 6351 — Combining Graph Transformations of Exponential Functions | 13943741 | 14006735 | 51.94 h | 387 at band 1 |
| differential | 2153 — The Pythagorean Theorem and the Triangle Inequality | 14040753 | 14096983 | 55.97 h | 390 at band 1 |
| foundations | 2979 — Solving Exponential Equations Using the Zero-Product Property | 13932983 | 14003941 | 61.27 h | One initial white observation, then 411 at band 1 |

The four constant-band cases are the cleanest. Each also has a **white, band-0 observation immediately before its lesson**, in the previous-activity snapshot linked by its original `state.json`: tasks `13941628`, `13944891`, `13942892`, and `14040677`, respectively. Their observed trajectory is therefore white → successful lesson → lightest blue throughout the captured interval → quiz. The fifth likely has a delayed post-lesson display update, but the capture alone does not establish why the initial snapshot was white. Each final pre-offer band was read 62–79 seconds before the first saved offer. **All five are prerequisites outside the enrolled course's native topic list.** The native-topic subgroup is tested separately below.

For topic 1609, the lesson-completion text explicitly says the lesson was completed and awarded 6 of 10 XP. Its original saved course HTML shows `rgb(210, 231, 249)` (band 1) immediately after the lesson and immediately before the quiz offer:

- [Immediate post-lesson snapshot](../../question-capture/13943819/knowledge-state/lesson-completed.json).
- [Latest pre-offer snapshot](../../question-capture/13981762/knowledge-state/lesson-completed.json).
- [Quiz source](../../question-capture/14003941/content.json).

Topic 2153 supplies an independent-account example. Its lesson is explicitly `passed`, with 8 of 14 XP, and its original saved course HTML likewise shows the same lightest blue immediately after the lesson and before the quiz:

- [Immediate post-lesson snapshot](../../question-capture-workers/differential/14040753/knowledge-state/lesson-completed.json).
- [Latest pre-offer snapshot](../../question-capture-workers/differential/14096823/knowledge-state/lesson-completed.json).
- [Quiz source](../../question-capture-workers/differential/14096983/content.json).

## Useful contrast: band reduction does not necessarily exclude a topic

Differential Equations Quiz 1 (`14093248`) tested topic 1989, Introduction to Recurrence Relations, at band 1, 54.26 hours after lesson `14036387`, without a captured direct review. Its post-lesson history includes 2 → 1 → 2 → 1. The final band 1 was observed 71.76 seconds before the offer. This rejects a current-band-2 gate, but its earlier band 2 makes it weaker evidence against a historical threshold than the constant-band-1 cases above.

## Native-course topics give the same answer about display thresholds

Six of the ten native-course band-1 cases also never exceed band 1 in their recorded post-lesson histories:

| Account / native course | Topic | First quiz | Observed history |
|---|---|---:|---|
| linear / Linear Algebra | 1735 — Partitioned and Block Matrices | 14094504 | 364 band-1 readings |
| multivariable / Multivariable Calculus | 1999 — The Jacobian | 14095129 | 394 band-1 readings |
| multivariable / Multivariable Calculus | 1898 — Identifying Quadric Surfaces | 14095129 | 404 band-1 readings |
| multivariable / Multivariable Calculus | 3235 — Velocity and Acceleration as Functions of Displacement | 14095129 | Initial white, then 404 band-1 readings |
| differential / Differential Equations | 2522 — Bernoulli Differential Equations | 14095468 | Initial white, then 328 band-1 readings |
| differential / Differential Equations | 3235 — Velocity and Acceleration as Functions of Displacement | 14094356 | 650 band-1 readings across two course pages |

These six had one or two captured direct reviews. Therefore they reject a native-course historical displayed-band-2 requirement, but cannot independently rule out some hidden credit requirement earned through those reviews. The observation counts are evidence coverage, not independent experiments; the last row includes repeated observations of the same account/topic on two course pages.

Conversely, four clean native-topic examples had **no direct review and no displayed increase after the successful lesson**:

| Native course / topic | Lesson → quiz | Initial → pre-offer band | Post-lesson history |
|---|---|---|---|
| Differential Equations / 290 — The Floor and Ceiling Functions | 14036384 → 14093248 | 2 → 2 | 359 readings, all band 2 |
| Differential Equations / 650 — Differential Operators | 14036386 → 14093248 | 2 → 2 | 352 readings, all band 2 |
| Foundations III / 1535 — Systems of Linear Inequalities | 13996965 → 14064989 | 2 → 2 | 390 readings, all band 2 |
| Methods I / 1738 — Differentiation Rules for Vector-Valued Functions | 14077032 → 14121671 | 2 → 2 | 210 readings, all band 2 |

All four have a white pre-lesson observation and an explicitly passed lesson. In these cases the lesson itself supplies the highest band seen before assessment. Native and prerequisite evidence together argue against adding a requirement for a direct review, a displayed level above lightest blue, or a subsequent visible improvement. Fractional implicit credit remains unobserved and cannot be excluded.

## Interpretation and limits

A separate requirement to complete a direct review is contradicted by the no-review cases, within the limits of captured history. A separate requirement to progress to a higher **displayed** band after learning is likewise unnecessary in the constant-band cases. We cannot rule out a small hidden repetition threshold that a lesson already satisfies, fractional implicit credit within band 1, or a distinct backend state such as successful acquisition/known status. Those possibilities should not be described as a demonstrated requirement for additional spaced practice.

No selected white topic was found among 368 fresh pre-offer observations. This is consistent with requiring the topic to be known, although absence alone does not prove the exact known-state test. The analysis does not show why all older blue topics are not selected: qualification, selection preference, quiz capacity, prior testing, encompassing relationships, and course-level scheduling remain distinct issues.

The first saved offer can be later than the actual creation of the quiz. Selection may have been fixed before we observed it. Therefore these are observations near first visibility, not recovered backend decision timestamps. Several hundred unchanged snapshots improve evidence coverage but are not independent experiments or proof that no hidden credit was earned.

## Reproduction

- [Analysis script](assessment-band-analysis.py).
- [Per-question evidence](assessment-band-evidence.json), including exact source files and observation gaps.
- [Complete histories for the 58 no-direct-review topics](assessment-band-no-review-histories.json).
- [Native low-band histories](assessment-band-native-low-histories.json) and [their analysis script](assessment-band-native-analysis.py), including membership checks against course topic lists.

No source capture, database fact, operational policy, or runner was changed.
