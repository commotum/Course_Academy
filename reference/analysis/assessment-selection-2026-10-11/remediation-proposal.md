# Assessment remedial weights: revised proposal

Assessments should have both initial and remedial distributions. Reuse the six
existing `question-weights/initial-*` and `question-weights/remedial-*` attributes
and the existing `:question-weights/validate` entity spec. The earlier proposal
to omit assessment remedial fields and introduce a separate validation spec is
withdrawn. This document proposes changes; it does not change the schema,
database, seed, or engine.

## Captured evidence

The analysis uses the 66 captured assessments already indexed in the assessment
report. Assessment difficulty ratings were verified against EDB at basis 1171.
Intervening practice uses the earlier rated-question snapshot at basis 1149.
Source documents provide activity type, quiz title, grades, topic and knowledge
point links, and human completion timestamps. This is a frozen snapshot analysis,
not a fresh live database read.

| Question population | DB-rated questions | Easy | Moderate | Hard |
| --- | ---: | ---: | ---: | ---: |
| Eight named quiz retakes | 67 | 43.28% | 40.30% | 16.42% |
| Retakes excluding an expired, unanswered original quiz | 59 | 42.37% | 42.37% | 15.25% |
| Retake questions on topics marked incorrect on their original quiz | 33 | 42.42% | 39.39% | 18.18% |
| Same missed-topic subset, excluding the expired original | 25 | 40.00% | 44.00% | 16.00% |
| Three human retakes | 25 | 56.00% | 28.00% | 16.00% |
| First subsequent captured regular-quiz question on a previously missed topic | 17 | 88.24% | 5.88% | 5.88% |
| Human reviews on missed topics between original quiz and retake | 27 | 51.85% | 40.74% | 7.41% |
| Human lessons on missed topics between original quiz and retake | 18 | 44.44% | 38.89% | 16.67% |

All eight retakes used only topics from the corresponding original quiz and
used fresh question IDs. Retakes covered 6–10 topics, including topics previously
answered correctly. All 33 rechecks of originally missed topics used the same
knowledge point as the original question. Excluding the expired original leaves
25 such rechecks. Remedial assessment selection should therefore be a deliberate
retake/recheck mode; it should not be activated after an arbitrary number of
questions in an ordinary quiz.

One original (`13933898`) expired with zero of nine questions answered. Although
its source history labels every question incorrect, that is not evidence of nine
attempted mistakes. Its retake contributes eight questions to the totals above.
Excluding the one later regular-quiz recheck traced to this expired quiz leaves
16 questions: 87.50% easy, 6.25% moderate, 6.25% hard.

The later regular-quiz sample is small and mixes accounts and intervals. It links
an observed miss to the first subsequently captured assessment question on that
topic, whether or not intervening practice already resolved the miss. Only five
of these 17 questions are human-history examples. This is evidence that missed
topics return later, but it does not establish a special remedial sampling rule
for regular quizzes. Do not pool it with whole retakes to claim a single recovered
Math Academy distribution.

The three human retake sequences contain nine recorded reviews and two lessons
on missed topics between quizzes. All eleven practice tasks have captured source
questions. The reviews contain 30 source-rated questions, of which 27 were rated
in the database snapshot; the remaining three must not be included in the
DB-rated percentages. Their source-only mix is 50.00/36.67/13.33. Practice history
and source capture are incomplete, so these counts are not the full remediation
inventory and temporal matching alone does not prove why a task was scheduled.

For example, human quiz `13553418` missed topics 88 (multiplicities of polynomial
roots), 161 (rules of sum and product), and 1610 (transformed logarithmic
functions). Reviews `13675888`, `13675890`, and `13675889` subsequently practiced
those topics. Retake `13682227` contained fresh questions for topics 88 and 1610,
rated easy and hard respectively, plus six previously tested topics. Retakes
are therefore neither exclusively missed-topic quizzes nor necessarily easier
on every repeated topic.

## Proposed database record

Keep initial weights at 50/40/10. Use **45/40/15 as a provisional remedial baseline**
for assessment retakes. It approximates the pooled retake observations while
retaining meaningful moderate and hard question supply. The smaller human sample
differs, and observed difficulty mixes depend on topic and available questions;
this is a design default, not a recovered Math Academy formula.

Add the following child alongside the policy's existing lesson and review children:

```edn
{:question-weights/activity-type :activity.type/assessment
 :question-weights/initial-easy 50.0
 :question-weights/initial-moderate 40.0
 :question-weights/initial-hard 10.0
 :question-weights/remedial-easy 45.0
 :question-weights/remedial-moderate 40.0
 :question-weights/remedial-hard 15.0
 :db/ensure :question-weights/validate}
```

This uses existing attributes, an existing activity enum, and an existing
validation spec. Update schema documentation to include assessments and explain
their remedial phase; no additional attribute or validation spec is needed for
storing these distributions.

## Engine integration

The shared reader currently accepts only lessons and reviews and rejects an
assessment child even when reading a lesson/review distribution. Extend its
supported activity types before adding the assessment child. Validate all six
assessment weights using the same numeric, total, ownership, and uniqueness
checks as the other activities.

For ordinary assessments, replace the hardcoded 50/40/10 distribution with the
policy's assessment initial distribution. Introduce an explicit phase argument
for assessment selection when adding retakes or designated assessment rechecks;
those use the remedial distribution. Preserve the existing lesson/review stopping
rules. Passing the assessment question count into the current lesson/review
phase rule would incorrectly turn the later questions of an ordinary assessment
into remedial questions.

Follow-up tasks served as reviews or lessons use their respective activity
weights. An assessment miss is the scheduling reason, not automatically a
reason to override those tasks with assessment weights. The current engine
already schedules reviews for assessment misses, but has no dedicated named
retake builder. Storing both distributions now does not itself implement retakes.

Existing API snapshot synchronization makes database weight changes available
to new selections. Already assembled assessment question sets remain fixed.
The difficulty controller and dedicated retake scheduling remain later work.

## Reproduction and detailed evidence

Run `.venv/bin/python reference/analysis/assessment-selection-2026-10-11/analyze_remediation.py`.
The script checks unique retake appearances, fresh IDs, topic overlap, and
agreement between rated database questions and source difficulty labels.

- [Summary and eight original/retake source pairs](remediation-summary.json)
- [All 67 retake questions and original-miss links](assessment-retake-questions.csv)
- [Later assessment rechecks of previously missed topics](assessment-later-missed-topic-rechecks.csv)
- [Intervening human review and lesson tasks](assessment-intervening-practice-tasks.csv)
- [Intervening practice question details](assessment-intervening-practice-questions.csv)
- [Analysis script](analyze_remediation.py)
