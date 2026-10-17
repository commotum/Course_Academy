Recommended generator ordering for the supplied topics

Historical design note: the later discussion moved relevance ahead of purpose.
The implemented policy and live queue verification are in
[the relevance-v2 deployment report](../generator-priority-update-2026-10-17/summary.md).
The bounded graph evidence below is retained unchanged.

Replace the additive score with an ordered priority key: purpose category, relevance group, global prerequisite layer ascending, distinct queued/target topics supported descending, engine priority descending, waiting time ascending, stable topic ID, KP shortage descending, stable KP ID. Order topics before their KP deficits so earlier lessons are completed before later lessons scatter into the work queue.

Relevance group 0 contains explicitly queued/target lessons and their unmet necessary prerequisites; speculative downstream lessons rank afterward. Explicit lesson demand is assessed independently of inferred review/assessment demand and imported mastery. Preserve completed local lesson history; explicit relearning still establishes lesson demand. Keep the existing purpose-category precedence. Use the same key in discovery and the live worker; reconcile pending or uncertain publication first, while unfinished author/review drafts keep their current rank.

Layer and support are different measures. Layer is the longest path from any root through topic/next, matching the app’s L01-based display. Support is the number of distinct selected goal IDs reachable downstream, not the number of paths. In production count across the deduplicated union of learner/queue and learner/targets. The support figures in this check cover only the 16 supplied unique topics; they are not global support counts.

Read-only graph check at basis 3431: 436 small topic records, including necessary ancestors; zero question records, global attribute scans, or writes. All 16 supplied unique topics are selected: 12 queued and 4 targets. The duplicate 17592186049570 is counted once. No supplied group places a topic before one of its prerequisites from a later group.

| Display layer | Topic ID | Topic | Selection | Listed selected topics downstream |
|---|---|---|---|---:|
| L35 | 17592186050283 | Triangular Matrices | :learner/queue | 0 |
| L38 | 17592186048470 | The Change of Base Formula for Logarithms | :learner/queue | 2 |
| L38 | 17592186051059 | Rewriting Radical Expressions Using the Laws of Exponents | :learner/queue | 0 |
| L39 | 17592186049879 | The Power Rule for Logarithms | :learner/queue | 3 |
| L39 | 17592186050375 | The Product Rule for Logarithms | :learner/queue | 2 |
| L40 | 17592186049053 | Solving Exponential Equations Using Logarithms | :learner/queue | 1 |
| L40 | 17592186050542 | The Quotient Rule for Logarithms | :learner/queue | 1 |
| L41 | 17592186049195 | Combining the Laws of Logarithms | :learner/queue | 0 |
| L41 | 17592186050649 | Solving Equations Containing the Exponential Function | :learner/queue | 0 |
| L43 | 17592186050245 | Parallel Lines in the Coordinate Plane | :learner/queue | 1 |
| L44 | 17592186049930 | Finding Equations of Parallel Lines | :learner/queue | 0 |
| L44 | 17592186050473 | Finding Equations of Perpendicular Lines | :learner/queue | 0 |
| L46 | 17592186049456 | Equations of Ellipses Centered at the Origin | :learner/targets | 0 |
| L46 | 17592186049570 | Equations of Circles | :learner/targets | 0 |
| L48 | 17592186050149 | The Area of a General Triangle | :learner/targets | 0 |
| L51 | 17592186049488 | Simplifying Expressions Using the Pythagorean Identity | :learner/targets | 0 |

The six shortages established by the earlier readiness audit fall into L39, L40, and L41:

- L39: Power Rule (17592186049879), Product Rule (17592186050375).
- L40: Solving Exponential Equations Using Logarithms (17592186049053), Quotient Rule (17592186050542).
- L41: Combining the Laws of Logarithms (17592186049195), Solving Equations Containing the Exponential Function (17592186050649).

Topics with sufficient question banks do not need urgent generator work, even if they are earlier in the study order. The final four distinct target topics were checked for graph position only; this read did not audit their question supply. No scoring code or live queue was changed.

Source graph evidence: [result.json](result.json). Reproducible bounded read: [check_graph.py](check_graph.py). Existing native layer/queue implementation: [learning.rs](../../../engine/rust/learning.rs).
