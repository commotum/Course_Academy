# Assessment topic sampling

October 12, 2026. Analysis of saved evidence and published explanations. The sampling rule below is now agreed, including a smooth encompassing discount that reaches its 5% minimum only at full coverage. This records the policy decision; engine, schema, and database implementation remains pending.

## Finding

Use weighted random sampling without replacement. Give never-assessed topics higher weight, and discount topics whose skills another eligible assessment topic would cover. Keep both discounts soft so older and simpler topics remain eligible.

The strongest correction to the earlier framing is **coverage by another quizzable topic**, rather than a general penalty for having recently received implicit practice. Actual implicit practice already influences retention and review timing. Whether a skill would be redundantly tested on this assessment is a different question.

The evidence supports those directions much more confidently than exact numerical weights. A four-to-one preference for never-assessed topics is a reasonable initial choice. The encompassing discount accounts for fractional coverage and retains a positive minimum weight. The chosen formula below is an application choice, not a recovered Math Academy algorithm.

## Published policy

[Math Academy's explanation](https://mathacademy.com/how-our-ai-works) specifies random selection from previously learned topics, lower priority for previously quizzed topics, and lower priority for topics encompassed by other quizzable topics. It also describes an enrolled-course preference. Our approved policy deliberately omits that preference; course membership is used here only to control the observational comparison.

The [authors' book](https://www.justinmath.com/files/the-math-academy-way.pdf), in the [practice-experience FAQ](../../The%20Math%20Academy%20Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-Practice-Experience.md), explains that quizzes can cover older learned material, not just material learned since the preceding quiz. Its [technical discussion](../../The%20Math%20Academy%20Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md) explains fractional encompassing weights and why prerequisite links alone do not establish implicit practice. Neither source provides numerical quiz-selection multipliers.

## Coverage and method

The saved run reads **3,532 activity records** and **3,565 knowledge/post-activity snapshot files** across the four separate accounts. It analyzes **61 assessments**, including five retakes: **508 attributed question appearances**, of which **466 belong to 56 ordinary assessments**. One additional slot in Foundations assessment `14131041` lacks a question/topic binding in the capture and is explicitly retained as unattributed. A standalone older assessment without a dated completion was excluded from chronological comparisons.

For each assessment, use its first saved offer, not its eventual completion. Only completed prior assessments establish previous testing. Retakes count as prior testing but are excluded from ordinary-selection outcome counts. Diagnostics remain separate.

Reconstruct an observable candidate pool using:

1. A successful captured lesson for the same account/topic, at least 48 hours before the offer. Retain the two original-completion timestamp corrections documented in [the age audit](../../../timed-delay-report.md).
2. The latest observation of each topic from progress pages saved before the offer, with each page no more than one hour old. Require a positive numeric display band; prefer the newest topic observation if several pages show it.
3. Native-course membership from the retained course topic lists, used as an analysis control.

This yields **45 usable ordinary-assessment pools**, **6,230 candidate appearances**, and **305 selected topics within those pools**. Another **57 selected topics** in those assessments are outside the observable pool, usually because their learning dates or fresh display evidence are missing. They remain in the assessment history; their missing candidate information is not invented. Candidate appearances repeat topics across assessments and are not 6,230 independent skills or experiments.

For encompassing comparisons, use account-local relationships with at least one observed positive exposure before the offer. Compute their crossing-frequency estimates only from earlier exposures. Propagate coverage using the engine's max-product rule, with explicit direct edges overriding inferred paths before further propagation. The strongest coverage from another candidate is retained. This is an incomplete empirical graph, not Math Academy's backend graph. A second sensitivity comparison uses all approved shared relationships retrospectively; it never substitutes future learner state for pre-offer state.

The positive relationship set was discovered in the encompassing study, so candidate discovery and its observation regimes remain limitations. A missing relationship means no qualifying observed edge, not proven zero coverage. Color bands are ordinal repetition proxies, not exact repetition counts or retention probabilities.

## Previously tested topics: lower priority, continued eligibility

Across all 56 ordinary assessments, **135 of 466 question appearances (29%)** revisit a previously captured assessment topic. The accounts remain separate:

| Account | Ordinary assessments | Questions | Previously assessed appearances |
|---|---:|---:|---:|
| Foundations | 40 | 337 | 105 |
| Linear | 8 | 69 | 17 |
| Multivariable | 4 | 38 | 11 |
| Differential | 4 | 22 | 2 |

The separately retained [human history](../assessment-selection-2026-10-11/topic-repetition.csv) also contains 36 repeated topic appearances across 93 questions in ten ordinary assessments. It has no reconstructed candidate denominator and is not pooled into the four-account learner histories.

Within the observable pools:

| Prior ordinary-quiz/retake exposure | Candidate appearances | Selected | Selection rate |
|---|---:|---:|---:|
| No captured previous test | 3,970 | 263 | 6.62% |
| Previously tested | 2,260 | 42 | 1.86% |

These are observed inclusion rates, not per-draw selection weights. They reflect pool size, question count, and other preferences. Conditional comparisons within the same quiz and course-membership group give a previous-testing odds ratio of **0.28**. Matching learning-age bands gives **0.32**; matching age and observed encompassing status gives **0.26**. Restricting to topics learned after the latest captured diagnostic gives **0.26**. These checks support a meaningful preference rather than a hard exclusion.

The account-specific pattern is uneven: conditional odds ratios are approximately **0.16 Foundations, 1.59 Linear, 1.51 Multivariable, and 0.46 Differential**. The smaller accounts do not independently establish a shared numerical penalty. Foundations dominates the sample; the public policy supplies stronger evidence for the general direction than those small samples do.

Concrete examples reject a strict new-topics-first interpretation of the observable pool:

- Multivariable Quiz 2, `14094319`, retests Double Summations and Moments and Center of Mass just **1.67 hours** after the preceding assessment. Both were previously answered correctly. Several untested native topics are already blue and 48–50 hours old, including Limits and Continuity of Multivariable Functions and Ellipsoids.
- Foundations Quiz 17, `14040402`, retests Implicit Differentiation while multiple untested native topics have captured successful lessons 55–74 hours earlier.
- Foundations Methods I Quiz 2, `14121671`, retests the 2×2 eigenvalue topic **7.43 hours** after its preceding assessment while older untested native topics remain observable.

The evidence contains 26 same-membership comparison groups with a selected repeat and an unselected untested candidate. Question supply and hidden admission conditions remain unknown, so these are candidate-pool counterexamples rather than proofs of exact backend eligibility. Together with the public policy, they favor randomized preference over a deterministic tier.

There is also no demonstrated minimum time between testing the same topic on successive ordinary assessments. The original 48-hour learning-age floor remains satisfied. A new quiz cooldown or resetting that age after an assessment would contradict the close repeat examples.

## Encompassing coverage: a substantial discount

For the account-local graph available before each offer:

| Strongest observed coverage by another candidate | Candidate appearances | Selected | Selection rate |
|---|---:|---:|---:|
| No observed relationship in that pool | 4,687 | 293 | 6.25% |
| Positive, below one-half | 246 | 3 | 1.22% |
| At least one-half | 1,297 | 9 | 0.69% |

The one-half boundary is an analysis grouping, **not a demonstrated Math Academy cutoff**. Among previously untested topics, controlling quiz and course membership gives a covered-topic odds ratio of **0.10**; matching learning-age bands leaves it at **0.10**. Using the retrospective shared graph gives **0.13**. This is consistent with avoiding redundant coverage, even before previous-testing preference can explain the difference.

Matching display bands weakens the covered-topic comparison to **0.30**. Coverage and repetition state overlap: component skills that receive implicit practice often become darker. This argues against interpreting the raw tenfold difference as an isolated causal multiplier or applying an additional arbitrary dark-band penalty on top of encompassing coverage.

There are 89 instances where the strongest observed encompassing candidate is selected and its component is not. For example, Foundations Quiz 18 (`14041922`) selects Equations of Ellipses Centered at the Origin while the eligible, blue, aged circle-equation topic is not selected. This is a useful content-level illustration, not proof that the sampled ellipse question necessarily exercises every circle KP. Topic-level coverage remains fractional and question dependent.

The captures do not establish a blanket suppression after recent practice. A recent successful direct review can precede a quiz by minutes, as the existing age analysis shows. Within these pools, a direct review in the preceding 24 hours has an odds ratio of **1.44**, controlling quiz, membership, learning age, and prior testing. That association is not causal, but it gives no support for adding a universal practice cooldown.

## Replay and what it does not identify

Seeded weighted draws without replacement condition on each assessment's selected-question count inside the observable pool. The comparisons use a course factor of four solely as a sensitivity control for Math Academy's course preference. That factor is not estimated or proposed for our engine.

Across the 305 matched selections, 42 are repeats and nine have at least one-half observed coverage. Uniform topic weights with that course control predict about **97 repeats and 51 covered selections**. A previous-testing multiplier of **one-quarter**, plus a linear coverage discount reaching one-quarter at full coverage, predicts about **38 repeats and 29 covered selections**. Stronger linear coverage discounts still overpredict covered selections. Different accounts also need different effective history penalties to match their observed counts.

The [additional sensitivity results](sensitivity.json) compare stronger linear, squared, and coarse coverage discounts and match learning age and display bands. The earlier squared-discount proposal with a 10% floor predicts **39 repeats and 13 covered selections**, compared with the observed 42 and nine. Those replay counts describe the original 10% floor, not the subsequently chosen smooth curve with a 5% minimum. It is a more plausible compromise than the linear discount, without introducing a hard coverage cutoff. It still underpredicts native-course selections and differs across accounts. An overall count can look plausible while account-level behavior differs; neither a fitted exact multiplier nor a recovered selection algorithm is justified. The captures establish sensible directions and useful starting ranges; question-bank availability, diagnostic admission, incomplete coverage edges, and unobserved topic priorities still matter.

## Chosen starting rule

The sampling rule is agreed. Category 4 still needs an implementation design.

1. Assemble all learned, sufficiently aged topics across courses and study modes. Apply existing fresh-question eligibility and inventory handling. A topic with no available questions cannot suppress another topic as a quizzable encompassing candidate.
2. Give a never-assessed topic base weight **4**, and a previously assessed topic base weight **1**. Use finalized assessment history, including completed retakes, rather than a second stored count. Do not add a repeated-failure bonus: required remediation already handles weaknesses.
3. Let `c` be its strongest existing encompassing coverage from another topic in the current eligible pool. Multiply its base weight by **`0.05 + 0.95 * (1 - c)^2`**. This single smooth curve decreases throughout the coverage range, from 1 at no coverage to 0.05 at full coverage. The minimum is part of the curve, so there is no flat interval for partially covered topics. The curve is an initial product choice, not a documented Math Academy parameter.
4. Draw topics randomly without replacement, then choose a fresh question using the existing database difficulty distribution. Freeze the route once created. Retakes continue to follow the approved original-KP route rather than this ordinary sampling rule.

| Topic state | No coverage | Half coverage | 80% coverage | Full coverage |
|---|---:|---:|---:|---:|
| Never assessed | 4 | 1.15 | 0.352 | 0.2 |
| Previously assessed | 1 | 0.2875 | 0.088 | 0.05 |

These table entries illustrate the function rather than defining coverage categories. At 80% coverage the multiplier is 0.088; full coverage gives 0.05. The positive minimum allows repeat audits and protects against an overly confident encompassing estimate. It does not guarantee selection within a fixed number of assessments. This rule uses the eligible pool to determine coverage, matching the published wording; it does not infer that every component will actually be tested by the questions ultimately selected.

Use the existing encompassing graph and learner assessment history. Preserve course-independent scope, the 48-hour admission floor, and the existing 50/40/10 ordinary question-difficulty weights. No new repetition-band threshold, last-practice wait, age bonus, or difficulty controller is implied. How to expose the two new topic-priority tuning values in policy configuration belongs in the implementation proposal, rather than silently reusing question-difficulty weights.

## Evidence and reproduction

- [Analysis script](analyze.py), [assessment/pool evidence](evidence.json), and [input hashes](input-manifest.json).
- [Sensitivity script](sensitivity.py) and [conditional comparisons and replays](sensitivity.json).

```bash
python3 reference/analysis/assessment-topic-sampling-2026-10-12/analyze.py
python3 reference/analysis/assessment-topic-sampling-2026-10-12/sensitivity.py
```

The first script reads frozen earlier audit metadata and current saved captures. Captures are still arriving, so rerunning can change coverage; the saved evidence and manifest identify this run. The second reads only that saved derived evidence and records its SHA-256. All learner-state comparisons stay within an account. Aggregate counts summarize evidence without merging their histories or pretending repeated observations are independent. Assertions check question/topic attribution, pre-offer timestamps, the 48-hour candidate floor, bounded coverage, and acyclic propagation.
