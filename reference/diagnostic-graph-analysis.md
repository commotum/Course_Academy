# Diagnostic graph reconstruction from completed exams

Analysis date: September 27, 2026, Pacific time. New browser observations were captured September 28 UTC. No schemas or application algorithms were changed.

The evidence supports a prepared collection of representative topics with deliberately selected diagnostic questions, followed by adaptive selection across that collection. It does not support treating the displayed question sequence as the complete compressed graph. The strongest new finding is stable question identity: all 26 topics that recur across different diagnostics include the same question ID each time that topic recurs.

The [question observations](diagnostic-observations-2026-09-27.json) preserve all eight events, 254 displayed question occurrences, results, difficulty labels, timing, and new response-region observations. The [graph comparison](diagnostic-graph-comparison-2026-09-27.json) preserves graph input fingerprints, generated candidate sets, course membership comparisons, and the conditional coverage calculations described below.

**Exams and observed results**

Dates below are activity-feed dates. Counts are displayed rows, not inferred from XP. Course/foundation classifications use the current local catalog and prerequisite graph, not a recovered exam-time graph.

| Feed date | Exam | Task ID | Questions | Correct / incorrect | Distinct topics | In course / foundations / unmatched |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 2025-02-27 | Mathematical Foundations II | [3506021](https://mathacademy.com/learn?taskId=3506021) | 56* | 37 / 19 | 55 | 29 / 25 / 1 |
| 2025-02-28 | Mathematical Foundations III | [3513719](https://mathacademy.com/learn?taskId=3513719) | 55* | 13 / 42 | 52 | 19 / 33 / 0 |
| 2025-07-29 | MF2 supplemental | [5454029](https://mathacademy.com/learn?taskId=5454029) | 5 | 3 / 2 | 5 | 2 / 3 / 0 |
| 2026-01-09† | Multivariable Calculus | [4748206](https://mathacademy.com/learn?taskId=4748206) | 9 | 3 / 6 | 8 | 0 / 8 / 0 |
| 2026-04-02 | MF2 supplemental | [9319474](https://mathacademy.com/learn?taskId=9319474) | 3 | 2 / 1 | 3 | 2 / 1 / 0 |
| 2026-07-14 | Calculus II | [11604423](https://mathacademy.com/learn?taskId=11604423) | 45 | 20 / 25 | 43 | 9 / 34 / 0 |
| 2026-08-18 | Calculus I | [12563189](https://mathacademy.com/learn?taskId=12563189) | 16 | 3 / 13 | 16 | 14 / 2 / 0 |
| 2026-09-17 | Mathematical Foundations II | [13469233](https://mathacademy.com/learn?taskId=13469233) | 65 | 39 / 26 | 61 | 54 / 7 / 0 |

*The first MF2 result page omits displayed ordinal 51. MF3 omits 28–29. Both end at ordinal 57. Those missing entries are not classified as skips, deleted questions, or answers. Adjacent-transition analysis excludes the gaps.

†MVC question labels say “Thu, Jun 5th,” whereas the feed says January 9, 2026. The labels omit a year. This discrepancy prevents reliable placement of those answers on the feed timeline. Summed question elapsed times are not total task duration.

**Evidence for designated questions, rather than arbitrary draws from ordinary banks**

There are 227 distinct question IDs and 216 distinct topic IDs in the 254 occurrences. Twenty-six question IDs recur across tasks; 25 occur twice and question 112044 occurs three times. Every pair of exams sharing a topic also shares the same primary question ID for that topic. The two full MF2 exams share ten topics and all ten corresponding question IDs, despite occurring about nineteen months apart.

Question 112044, on factoring higher-order polynomials as a difference of squares, appears in MF3, Calculus II, and the later MF2 placement. Question 78257 appears in MF3 and MVC. This strongly supports stable diagnostic item choices attached to topics, with alternate items available for reassessment. It does not prove that only one primary item can ever exist, reveal tie-breaking, or establish zero randomness in every part of the algorithm.

Diagnostic suitability is not synonymous with the H label. Observed labels are 65 E, 139 M, and 50 H. The book describes choosing a relatively simple question that demonstrates topic mastery and exercises its prerequisites; that is different from choosing the hardest numerical instance. See the [diagnostic question-selection criteria](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md>), lines 89–98.

**Evidence about adaptive branching**

There are 11 immediate same-topic reassessments. Every one follows an incorrect answer, uses a different question ID, and retains the same example-content anchor and E/M/H label. Ten second answers are correct; one is incorrect. There are no observed three-question runs or later nonconsecutive returns to the same topic within an exam.

The response regions distinguish a useful branch:

| Incorrect response evidence | Immediate same-topic retry | Next question is another topic | Gap or no successor |
| --- | ---: | ---: | ---: |
| Explicit “No answer” | 0 | 111 | 4 |
| Submitted text/selection or image | 11 | 5 | 0 |
| Empty response region, meaning unknown | 0 | 3 | 0 |

Thus no explicit unanswered question with a visible successor is followed by an immediate same-topic retry, while 11 submitted mistakes are. Five other submitted mistakes have no recorded retry. This does not establish whether a retry was offered and declined: completed question histories record the selected path, not the offer. “No answer” is the observed result-page label; it does not independently prove which button was pressed or whether time expired.

For example, Calculus II question 112044 receives a submitted incorrect answer, followed immediately by question 31366 on the same topic and example. The latter has “No answer,” after which the next question is on a different topic.

**Follow-up: the “silly mistake” retry mechanism**

On September 28, 2026, I inspected Math Academy's publicly served [student-diagnostic.js](https://mathacademy.com/js/student-diagnostic.js), [question-widget.js](https://mathacademy.com/js/question-widget.js), and [api.js](https://mathacademy.com/js/api.js), without starting or answering a diagnostic. The diagnostic client provides a direct explanation of how the offer and the learner's choice are separated:

- After answer submission, the question widget passes the server's task result to the diagnostic controller. The controller assigns `event.task.allowRetry` to its local `allowRetry` flag (student-diagnostic.js, lines 139–145).
- Clicking Next opens the retry screen when that flag is true; otherwise it requests the next question normally (lines 51–60). A completed task displays Done instead of Next (lines 159–168).
- Yes requests the next question with `retry=true`; No requests it with `retry=false` (lines 188–199). The API wrapper forwards this choice to the server (api.js, lines 701–702).
- The client records separate retry-screen view, Yes, and No events (student-diagnostic.js, lines 175–199). Those events are not included in our completed-question captures.

There is no elapsed-time eligibility calculation in this diagnostic client. The server decides `allowRetry`; the conditions used to compute that flag are not exposed by these files. Timing, availability of an alternate question, previous retries, or other eligibility rules therefore remain unconfirmed. The public script also does not contain the prompt's wording, which comes from the page's retry-screen markup.

The 11 submitted wrong answers followed by retries took 17–109 seconds (mean 51 seconds). The five without recorded retries took 8–83 seconds (mean 50 seconds). For example, question 125550 took eight seconds with no recorded retry, while question 119805 took 109 seconds and was followed by a correct answer to alternate question 19276. These observations cannot identify the offer rule or exclude timing relative to a question-specific expected duration.

**Expected time versus elapsed time: working inference**

Relative time is a credible input to retry eligibility. Math Academy explicitly compares diagnostic response time with the expected time for a student who has mastered the topic when weighting correct answers ([official algorithm explanation](https://www.mathacademy.com/how-our-ai-works)). Justin Skycak also describes question-time estimates initially averaged across content writers and then calibrated using student results ([October 2024 interview](https://www.justinmath.com/golden-nuggets-podcast-39/), paragraphs beginning “We have time estimates for questions”). These establish that the baseline exists and already serves diagnostic inference; applying it to retry eligibility is our inference.

The normalized local corpus supplies no such baselines: 2,964 lesson JSONs containing 19,646 question occurrences have no timing fields, and none of the 16 submitted-wrong diagnostic question IDs occurs in those question records or Questions.csv. As a limited comparison, two of the 16 have a correct answer to the exact same question elsewhere in the captured diagnostic histories:

| Question | Submitted wrong | Correct on another diagnostic | Wrong / observed correct duration | Recorded same-topic retry |
| --- | ---: | ---: | ---: | --- |
| 112044: factoring higher-order polynomials | 73 s, July 2026 | 129 s, September 2026 | 0.57 | Yes |
| 43575: lowest common multiples | 56 s, September 2026 | 50 s, July 2025 | 1.12 | No |

The direction fits a relative-speed hypothesis, but these are two personal observations across different dates, not MA's expected times. They cannot establish a threshold or distinguish timing-based offers from offers on every submitted mistake followed by a learner choice. Successful alternate retries are also a poor calibration source: they happen after feedback and only for accepted retries. Seven of the ten initial mistakes took longer than their subsequent correct retry, so “must be faster than a competent solution” would be an unnecessarily strict interpretation.

For our reproduction, a reasonable working rule is: offer one alternate probe after a submitted wrong answer when a retry is available and the response was not excessively slow relative to the question's expected time; the learner decides whether to take it. This treats timing as evidence against prolonged struggle, not proof that a quick wrong answer reflects confidence or knowledge. Implement the comparison as `elapsed_seconds / expected_seconds` with an adjustable tolerance. No numerical tolerance is inferred from these observations. When an expected time is unavailable, do not substitute E/M/H or earned XP as if either were a duration; offer the alternate without a timing gate until a usable estimate exists. The alternate answer, rather than the learner's declaration alone, supplies the confirming evidence. This is a practical local policy grounded in MA's diagnostic purpose, not a recovered eligibility formula.

For our proposed probe model, `on-silly-mistake` can mean **the learner accepted an offered reassessment**, rather than a correctness category inferred from speed. Eligibility belongs in the application; the branch points to an alternate probe on the same topic. The original wrong response remains part of the attempt history. No schema changes were made in this investigation.

The broader order is not a simple walk along prerequisite edges. Of 244 observed consecutive transitions without numbering gaps, 11 repeat the topic, seven move between topics connected by a prerequisite path, and 226 have no prerequisite path in either direction in the saved graph. A selector considering the whole current diagnostic frontier is a better working hypothesis than “always follow the next prerequisite or postrequisite.” A separately authored routing tree could still reproduce an observed path; these results do not identify hidden routing edges.

**What is disclosed about creating the compressed graph**

The [technical chapter](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md>), line 17, gives a concrete construction objective: reduce the course and relevant foundations to a small representative set, with each covered topic bracketed by a representative ancestor and descendant within three prerequisite edges. The [public algorithm description](https://mathacademy.com/how-our-ai-works) separately describes repeatedly choosing the topic expected to give the most information about the current knowledge profile.

This separates three decisions:

1. Choose representative topics that cover the diagnostic scope.
2. Associate suitable diagnostic questions with those topics.
3. During an attempt, choose which representative topic and question to present next, based on accumulated evidence.

For our reconstruction, the third step can update the learner profile after each answer without changing the shared compressed graph. A compressed graph can be prepared and stored in advance even though its use is adaptive.

The publication does not specify the exact minimization solver, tie-breaking, treatment of graph endpoints, or exact foundation boundary. A strict requirement for both an ancestor and descendant cannot hold at roots and terminal topics without a boundary convention. Historical mastery-floor descriptions also indicate that “relevant foundations” need not mean the entire transitive prerequisite closure. See the [spaced-repetition chapter](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md>), lines 85–88.

**A concrete construction experiment**

The saved global data contains 2,971 catalog topics and 6,560 unique prerequisite edges. Including four referenced topics missing from the catalog, the graph has 2,975 nodes and no cycles. The CSV stores advanced-topic → prerequisite, the reverse of the original SVG arrow direction. Course membership comes from [Catalog.csv](/home/jake/Developer/MA/DATA/Catalog.csv).

I implemented a scratch greedy coverage calculation with these explicit local choices:

- Include the course and its full prerequisite closure.
- A selected topic covers itself.
- Every unselected topic needs a selected prerequisite ancestor and selected postrequisite descendant, each within three original graph edges.
- Select topics to satisfy uncovered coverage requirements, then remove redundant selections.

| Scope | Course topics | Full closure | Feasible representative set |
| --- | ---: | ---: | ---: |
| MF2 | 357 | 810 | 179 |
| MF3 | 323 | 1,102 | 214 |
| Calculus I | 175 | 871 | 161 |
| Calculus II | 160 | 1,031 | 187 |
| Multivariable Calculus | 187 | 1,224 | 206 |

These are generated candidate pools, not reconstructed MA pools, question counts, or proven minima. Their selected topic IDs are retained in the graph-comparison artifact. A learner may need to visit only a fraction of a prepared pool.

A useful negative result prevents overfitting the old exams: under this exact scope and coverage interpretation, forcing all 52 early MF3 tested topics into an exactly minimum representative set requires at least 220 nodes, while an explicit feasible set contains only 214. The lower bound uses mandatory nodes plus disjoint outstanding coverage requirements; its witness sets are preserved in the artifact. Therefore the combination of this current graph, scope, boundary rule, exact optimality, and fixed-pool membership cannot describe that historical attempt. The evidence does not isolate which assumption differs.

**What cross-course comparisons add**

The early MF2 exam tested 29 current-course topics and 25 foundations; the later MF2 exam tested 54 and seven, respectively. Their topic intersection is only ten out of a union of 106. This is consistent with changed learner knowledge and/or a changed candidate graph; it cannot establish which caused the difference.

The MVC attempt's eight distinct topics are all foundations under the current catalog. Calculus II tests nine course topics and 34 foundations, while the later Calculus I exam tests 14 course topics and only two foundations. These patterns show why the course title alone does not identify the actual territory explored. Existing evidence, enrollment changes, diagnostic mode, and curriculum updates all matter.

Both MF2 supplemental diagnostics ask topics absent from the first MF2 diagnostic, and the two supplements do not overlap each other. This matches the published purpose of filling evidence gaps, but we lack the historical balances and graph changes needed to reproduce their exact selection. Supplemental diagnosis can still use the same content schema with different eligibility rules. The book's rule considers topics not directly tested initially whose evidence balance remains zero after accounting for subsequent assessment evidence; see the [diagnostic chapter](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md>), line 85.

**Limits that affect implementation**

The available prerequisite CSV is a union of SVG and lesson sources. Fourteen retained SVG edges disagree with prerequisites in available lesson JSON. It is not a clean historical snapshot. More concretely, the current result page for old task 3506021 links question 68517 to topic 7011, absent from the local catalog; local [Questions.csv](/home/jake/Developer/MA/DATA/Lesson-Data/Questions.csv) instead associates it with topic 2558. The live link is not proof of the mapping that existed in 2025, and it should not be silently remapped.

We also do not know whether each diagnostic started from a clean slate or was blended with an existing learner profile. Both modes are described in the [XP FAQ](<The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-XP-and-Practice-Schedules/FAQ-XP-and-Practice-Schedules.md>), line 120. The source does not specify how those modes affect candidate construction versus online selection.

The completed paths do not expose unasked candidate nodes, coverage witnesses, starting balances, or the information score for alternatives. Our construction objective is well grounded; exact historical representative sets remain underdetermined.

For the proposed model, a shared compressed diagnostic graph with topic references, diagnostic question choices, and meaningful coverage relationships is justified. Its links should represent diagnostic coverage or topic relationships, rather than assuming every edge is a fixed correct/incorrect next-question branch. The application can update learner evidence, select across that graph, and record presented questions and any explicit bypass decisions on the attempt. That is a practical implementation direction supported by both the published construction and the observed histories.
