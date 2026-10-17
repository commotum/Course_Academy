The six blocked lessons are **not at the front of the existing generator build queue**. This inspection reads saved queue files only: zero database reads, queue writes, or worker starts. The accepted ranking cursor is EDB basis 3429.

The queue contains individual knowledge-point jobs. There are 6519 pending/running build jobs in this snapshot. Positions below reproduce worker ordering before locked-KP skips and future queue refreshes.

| Topic ID | Topic | Deficient KP positions | Next activity | Build score |
|---|---|---|---|---:|
| 17592186049053 | Solving Exponential Equations Using Logarithms | 2816, 2817, 2818 | review | 500 |
| 17592186049195 | Combining the Laws of Logarithms | 2137, 2138, 2139 | lesson | 63,300 |
| 17592186049879 | The Power Rule for Logarithms | 2805, 2806, 2807 | review | 500 |
| 17592186050375 | The Product Rule for Logarithms | 2808, 2811 | review | 500 |
| 17592186050542 | The Quotient Rule for Logarithms | 2812, 2813, 2814, 2815 | review | 500 |
| 17592186050649 | Solving Equations Containing the Exponential Function | 2819 | review | 500 |

Five topics have urgency value 5, meaning the ranking classifies them as studied; their next activity is review. Review inventory pools the topic, so those topics have no review shortage despite their per-KP lesson shortages. Their only winning reason is advance-build (500 points). Studied status can be established by imported learned progress; it does not require a completed local lesson attempt.

Combining the Laws of Logarithms has three deficient KPs with lesson-shortage scores of 63,300: 60,000 purpose points + 3,000 for three missing questions + 300 for queued urgency. There are 2,136 higher-scoring build jobs ahead of these: 2,116 score 65,100, 19 score 64,100, and one scores 64,200. The top score group is descendant lesson work with zero usable questions.

The scoring rule puts purpose first, shortage size second, and urgency third. It does not automatically elevate explicitly queued lessons above all descendant shortages. Saved unfinished pipeline recovery also precedes normal scoring. Unchanged rejected jobs, backoff, and locked KPs affect execution.

Source rules: [finder ranking](../../../generate/scripts/find_candidates.py), [activity inference](../../../generate/scripts/find_candidates_ranking.rs), and [worker ordering](../../../scripts/inventory_jobs.py). Raw snapshot: [queue-snapshot.json](queue-snapshot.json).

The small follow-up title/membership lookup at the same basis resolved these examples ahead of the six lessons:

| Topic ID | Topic | Usable per competing KP | Missing toward five |
|---|---|---:|---:|
| 17592186048190 | K Permutations of N With Repetition | 0 | 5 |
| 17592186048196 | Euler's Totient Function | 0 | 5 |
| 17592186048198 | Addition and Subtraction in Scientific Notation | 0 | 5 |
| 17592186048199 | Calculating Arc Lengths of Circular Sectors | 0 | 5 |

The exact membership lookup confirms that all six blocked topics are in `learner/queue`, and none is in `learner/targets`. None of the four competing example topics is in either set. A target-only priority filter would therefore miss the six requested lessons. Membership/name evidence: [example-titles.json](example-titles.json).

Recommended policy: treat queued/requested lessons and direct targets without completed local lessons as explicit lesson-supply needs, independently of imported mastery. Prioritize those needs ahead of speculative descendant preparation; use shortage size within the priority group. Local completion means a completed learner-owned lesson task for that topic, not any completed review or assessment. Preserve other activity replenishment and allow explicit relearning even after prior local completion. No policy or queue changes have been made.
