# Captured assessment retake behavior

Analysis of eight captured original/retake pairs: three human-history retakes and five automated retakes, containing 67 questions. This is source analysis only; no retake scheduling, engine, schema, or database changes were made.

## The eight pairs

| Original → retake task | Stream | Original result | Original → retake questions | Originally missed topics retested | Previously correct topics retested |
| --- | --- | --- | ---: | ---: | ---: |
| 13933898 → 13938136 | Automated | Expired; 0 answered | 9 → 8 | 8/9 | 0 |
| 13980518 → 13980882 | Automated | 7/11 (63.6%) | 11 → 10 | 4/4 | 6 |
| 14003941 → 14004701 | Automated | 7/10 (70.0%) | 10 → 9 | 3/3 | 6 |
| 14093248 → 14093489 | Automated | 5/7 (71.4%) | 7 → 6 | 2/2 | 4 |
| 14094504 → 14094745 | Automated | 6/9 (66.7%) | 9 → 9 | 3/3 | 6 |
| 12225370 → 12228526 | Human | 2/8 (25.0%) | 8 → 8 | 6/6 | 2 |
| 13553418 → 13682227 | Human | 7/10 (70.0%) | 10 → 8 | 2/3 | 6 |
| 4833336 → 4833693 | Human | 4/9 (44.4%) | 9 → 9 | 5/5 | 4 |

## What changes on a retake

All 67 retake questions have fresh question IDs, and every one links to the same knowledge point as its corresponding original question. No new topics appear. Three retakes cover the entire original topic set; five omit one or two topics. Of the 67 retake questions, 34 revisit previously correct topics and 33 revisit topics marked incorrect. Eight of the latter came from an expired original with no attempted answers, so they must not be treated as eight ordinary attempted mistakes.

This is a broad recheck of the original quiz’s knowledge points, not repetition of identical questions and not a quiz containing only missed topics. The captured retakes do not always include every missed topic: human original 13553418 missed three topics, but retake 13682227 retested only two; topic 161 (The Rules of Sum and Product) was omitted. The expiration pair also omitted one topic marked incorrect. The captures do not identify the selection rule that omitted these topics.

## What appears to trigger the offer

Four automated sequences have complete post-original and post-review queues. Each original scored 63.64–71.43%, immediately offered one review for each missed topic, and offered its named retake only after all those reviews were completed. The final review queue then contained the retake alongside other available work.

For comparison, 22 other automated original quizzes scored 76.92–90.91%, had missed-topic reviews captured through completion, and showed no named retake in their post-review queues. This supports a cutoff near 75%. The exact threshold, rounding, and inclusive/exclusive rule are not established: our nearest cases are 5/7 (71.43%, offered) and 10/13 (76.92%, no offer). A threshold of 80% is not consistent with these sequences because the 76.92% and 77.78% cases showed no offer.

A below-threshold original without a completed captured retake is not proof that no retake was offered. In particular, human original quizzes 13467292 (62.5%) and 6907144 (66.7%) have no matching completed retake in this history. That history lacks full offer queues.

## Timing and required status

In the four fully traced automated sequences, the first captured retake offer is the queue immediately after the final missed-topic review. The worker starts the retake about 7–13 minutes after the original completion capture, and approximately 47–58 seconds after the final-review completion capture. These are observation/start timestamps, not exact server unlock timestamps or prescribed delays. There is no observed need to earn another 150 XP before a retake.

Human completion-to-completion intervals are 34 minutes (4833336 → 4833693), 1 hour 57 minutes (12225370 → 12228526), and 5 hours 40 minutes (13553418 → 13682227). These intervals include review, other activity, idle time, and the retake itself; they are not unlock cooldowns. The expired original was recovered later, so its recovery capture time cannot establish the actual completion-to-retake interval.

All five automated retakes have source-backed `assessment_requirement: unknown`, no optional-XP countdown, and a note explaining that retake XP is additional to original quiz XP. All five appear alongside other offered tasks before starting. Our capture worker explicitly prioritizes `quiz_retake` independently of requirement status; its immediate selection therefore does not prove Math Academy required the retake. No optional-to-required transition or future retake deadline is captured. Ordinary quiz notices such as “optional until 18 more XP” must not be applied to retakes without evidence.

## If the retake still has mistakes

Three automated retakes had wrong answers: 13980882 scored 90% with one miss, 14093489 scored 33.33% with four misses, and 14094745 scored 88.89% with one miss. Each immediately offered one review per missed topic. After all those reviews were completed, captured queues returned to lessons and showed no second retake of the same quiz. This supports one offered retake per original in this sample; it does not establish that a later second retake is impossible.

## Detailed evidence

- [Structured pair, queue, timing, and trigger evidence](retake-behavior.json)
- [26 post-review trigger comparisons](retake-trigger-comparison.csv)
- [All 67 retake questions](assessment-retake-questions.csv)
- [Reproducible analysis script](analyze_retakes.py)

The structured evidence links every original/retake source and every reviewed queue. Representative final-review queues:

- [Four missed reviews completed; Quiz 7 retake offered alongside lessons](../../mathacademy/question-capture/13980754/queue-after.json)
- [Three missed reviews completed; Quiz 10 retake offered alongside lessons](../../mathacademy/question-capture/14004556/queue-after.json)
- [Two missed reviews completed; differential Quiz 1 retake offered](../../mathacademy/question-capture-workers/differential/14093410/queue-after.json)
- [Three missed reviews completed; linear Quiz 2 retake offered](../../mathacademy/question-capture-workers/linear/14094691/queue-after.json)
- [After reviews for the 33% retake, the queue returns to lessons](../../mathacademy/question-capture-workers/differential/14093672/queue-after.json)
- [Capture worker’s retake-priority and requirement parsing](../../../scripts/question_capture/core.py)
