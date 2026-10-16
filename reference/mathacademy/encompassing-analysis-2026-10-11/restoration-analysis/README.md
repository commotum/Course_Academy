# Large band changes, reassessment, and activity type

## Working explanation

The critique identifies a real distinction: **a temporary displayed rise and a persistent post-diagnostic revalidation should not be fitted as the same ordinary repetition increment**. Large jumps also occur after ordinary reviews, so removing diagnostic activities alone does not remove the behavior.

For the potential-functions example, keep the encompassing relationship stable and model the late jump as a reassessment of component knowledge. The earlier jump belongs to a transient displayed-state sequence. The mathematical question content explains which component skills the activity exercises; diagnostic context and prior learner state explain why similar practice can produce different visible outcomes.

## Verified example

The [case study](case-study.md) checks the original HTML and uses only the multivariable account's frozen captures.

- Review 14068004 changes potential functions from 1 to 3. The band returns to 1 after **32.6 minutes**, then changes 1→3→1→3 during subsequent activities.
- Lesson 14119320 changes potential functions and conservative vector fields from 1 to 6 together. Both were 1 in **28 preceding original observations** and remain 6 in **40 observations including completion**, spanning **6.10 hours**. Copied before-snapshots do not count twice.
- The late lesson changes only four topics: source 2110 from 0 to 1, the two components from 1 to 6, and gradient vector 1934 from 4 to 5.
- The earlier and later lessons have identical KP-level performance: **3/5 correct on each of three KPs**. The flat and temporarily rising reviews also match: **3/3 correct when the potential is supplied, 0/2 correct when reconstruction is required**.

One detail changes the interpretation of “restoration”: the older component bands of **5 and 6 were themselves assigned after diagnostic 14097559**. They were both 3 in the preceding saved profile. They are HTML display bands, not independently observed numerical repetition counters. The next diagnostic and course change are followed by 1/1 on a different course page. Thus the strongest description is **post-diagnostic revalidation or recomputation**, rather than exact restoration of five or six earned repetitions.

The new diagnostic even contains a correctly answered potential-reconstruction question before the source is subsequently shown white and the components at 1. Diagnostic placement does not act like a simple ordinary positive-credit update after each correct question.

## Large jumps with diagnostics excluded

The original timing analysis already excludes diagnostic activities. Restricting it further to **passed reviews**, while retaining directly reviewed topics and their structural prerequisites, gives:

| Account | Reviews producing a jump of at least two bands | Topic jumps | Such reviews before the first captured diagnostic |
|---|---:|---:|---:|
| Foundations | 92 | 155 | 79 |
| Linear | 23 | 42 | 0 |
| Multivariable | 21 | 49 | 12 |
| Differential | 14 | 35 | 0 |

One review can change several targets. “Before the first captured diagnostic” describes the recorded window; it does not assert that the learner never took a diagnostic before capture began. Linear and differential begin with captured diagnostics, so their zero counts in that column are expected.

Examples at 60% review accuracy include foundations task14029846, source760→target1686 **1→6**, and task14043117, source850→target3842 **1→6**. Both precede the account's first captured diagnostic. Multivariable task14078784, source2110→target1837, also produces **1→6** before that account's first captured diagnostic. Their captured target-direct ages are approximately 63.9, 84.2, and 23.6 hours. Those are time since direct practice, not known times since the last implicit memory update.

The answer to “do large jumps remain after excluding diagnostics?” is therefore **yes**. The further questions are which gains persist, which return toward an earlier high state, and how those patterns differ between reviews, lessons, and assessments.

## Comparing activity types

These comparisons use the **same observation rules for all activity types**: matching account/course/topic, starting band 1–5, known ending color, a before/after interval of at most 30 minutes, and exactly one captured activity in that interval. Agreeing copies of a topic across courses count once; conflicting course displays are excluded. Unchanged topics stay in the denominator. Diagnostics are excluded, but completed assessments are retained even though their task-level pass/fail field is empty. Multistep tasks remain a separate category.

The common comparison includes **all comparable topics on the captured progress pages**. It measures changes observed after an activity, not proof that the activity supplied mathematical practice to every changed topic. This wider scope explains why these counts exceed the prerequisite-only review counts above.

### How often an activity is followed by a multi-band rise

Each cell is activities with at least one rise of two or more bands / eligible activities, followed by the percentage.

| Account | Reviews | Lessons | Assessments |
|---|---:|---:|---:|
| Foundations | 237/594 — **39.9%** | 215/526 — **40.9%** | 12/30 — **40.0%** |
| Linear | 42/339 — **12.4%** | 42/296 — **14.2%** | 0/8 — **0%** |
| Multivariable | 51/246 — **20.7%** | 50/290 — **17.2%** | 0/4 — **0%** |
| Differential | 25/234 — **10.7%** | 33/244 — **13.5%** | 1/5 — **20.0%** |

There is **no consistent lesson-over-review multiplier** in these rates. Foundations is almost identical; lessons are somewhat higher in linear and differential, while reviews are higher in multivariable. Assessment samples outside foundations are small. Multistep tasks show large rises after 6/20 foundations activities and 1/9 multivariable activities.

Per-topic denominators reach the same broad conclusion without treating an assessment as a one-topic event:

| Account | Review jumps / topic opportunities | Lesson jumps / topic opportunities | Assessment jumps / topic opportunities |
|---|---:|---:|---:|
| Foundations | 786/166,799 — 0.471% | 705/121,859 — 0.579% | 31/9,068 — 0.342% |
| Linear | 98/61,754 — 0.159% | 89/37,459 — 0.238% | 0/1,768 |
| Multivariable | 106/42,137 — 0.252% | 74/42,069 — 0.176% | 0/830 |
| Differential | 56/39,759 — 0.141% | 61/33,320 — 0.183% | 3/980 — 0.306% |

The topic opportunities include many unrelated and unchanged page entries, so these percentages are **display-change rates**, not encompassing weights. The machine-readable outputs also stratify by starting band, accuracy, outcome, and capture pipeline. These observational activity groups are not matched randomized treatments.

### Directly practiced topics behave differently

For a review or lesson, the direct topic is the activity's topic. For an assessment, it is a topic named by an actual saved question. The extraction uses explicit numeric topic IDs and the question header's topic link, not incidental prerequisite links in solutions.

| Account | Direct review topics with a multi-band rise / eligible observations | Direct assessment topics with a multi-band rise / eligible observations |
|---|---:|---:|
| Foundations | 9/576 | 5/195 |
| Linear | 2/277 | 0/22 |
| Multivariable | 5/208 | 0/36 |
| Differential | 4/192 | 0/25 |

**All five multi-band direct assessment gains are +2, after correct answers.** Larger assessment-associated changes occur on other displayed topics. The signed behavior of directly assessed topics is particularly clear:

| Account | Correct assessed topics: flat / rise / fall | Incorrect assessed topics: flat / rise / fall |
|---|---:|---:|
| Foundations | 118 / 55 / 0 | 19 / 0 / 3 |
| Linear | 12 / 6 / 0 | 4 / 0 / 0 |
| Multivariable | 21 / 12 / 0 | 3 / 0 / 0 |
| Differential | 13 / 5 / 0 | 5 / 0 / 2 |

This supports ordinary **signed per-question assessment credit** as a distinct mechanism. It does not support assigning a large activity-wide multiplier to every assessment. Reviews can contain incorrect questions but still pass; their completion and ability updates must not be conflated with the sign of one assessment question.

Most directly learned lesson topics start white, so the blue-start comparison contains only one eligible direct lesson topic in foundations and none in the other accounts. Compare those initialization events separately:

| Account | Eligible source-white lessons | End at band 1 | End at band 2–6 | Still white at completion capture |
|---|---:|---:|---:|---:|
| Foundations | 497 | 316 | 60 | 121 |
| Linear | 244 | 180 | 23 | 41 |
| Multivariable | 242 | 166 | 43 | 33 |
| Differential | 199 | 112 | 33 | 54 |

White-to-blue initialization is a different question from an existing topic gaining several bands. A topic still appearing white in its completion capture is also not proof that the system permanently failed to learn it; these are immediate observed displays. White-start lesson cases are not silently added to the blue-start denominators.

### Persistence distinguishes durable changes from temporary ones

Follow each changed topic on the **same course page**. Deduplicate copied baselines by original course-read timestamp. Stop follow-up at the next diagnostic boundary; use the first captured diagnostic question time when available, otherwise explicitly mark the legacy completion-capture boundary as a fallback. Quarantine contradictory same-time reads.

The first number below is gains observed returning to or below their starting band within six hours / all multi-band gains. The second is gains confirmed at or above their ending band throughout follow-up and the first nearby six-hour boundary read / gains with that follow-up coverage.

| Account | Review: returned to baseline | Review: full endpoint persisted | Lesson: returned to baseline | Lesson: full endpoint persisted |
|---|---:|---:|---:|---:|
| Foundations | 617/786 | 80/597 | 601/705 | 39/429 |
| Linear | 47/98 | 17/42 | 63/89 | 11/72 |
| Multivariable | 48/106 | 18/71 | 46/74 | 17/48 |
| Differential | 15/56 | 26/30 | 15/61 | 19/35 |

The return-to-baseline fractions are observed minima: some events lack a full six hours of follow-up. Persistence requires actual reads, including a boundary read within six to seven hours; a distant later capture or an empty observation window does not prove persistence. A retained endpoint is only an observation of the later state, not proof that the initial activity alone maintained it through intervening practice.

Assessment-associated gains also reverse: foundations has 22/31 returns to baseline and 3/18 confirmed endpoint retentions; differential has 2/3 returns and 0/3 endpoint retentions. No multi-band assessment gains were observed in the other two accounts.

**Transient changes are common after both lessons and reviews.** Foundations is particularly volatile, while differential has more persistent gains among events with follow-up. We therefore should not convert every immediate multi-band rise into lasting repetition credit. Even in the original passed-review prerequisite panel, foundations has 99/155 large target jumps returning to baseline within six hours.

### Relearning and returns toward earlier high states

Classify a lesson as an observed post-diagnostic return when its source was successfully practiced before the latest captured diagnostic and is white before the new lesson. This identifies 17 foundations lessons and 26 multivariable lessons. It identifies none in linear or differential within the captured history; that does not establish an absence of pre-capture learning.

| Account | Returning-source lessons with a large jump | Other lessons with a large jump |
|---|---:|---:|
| Foundations | 7/17 — 41.2% | 208/509 — 40.9% |
| Multivariable | 10/26 — 38.5% | 40/264 — 15.2% |

The multivariable difference supports treating the motivating revalidation case as a distinct context; foundations does not show a corresponding activity-rate difference.

For a descriptive return-toward-prior-high marker, require an earlier band of at least 4, a starting band at most 2, and an ending band at least one below that prior high. Keep same-course history separate from other-course history. Among large review jumps, the marker appears on the same course in 279/786 foundations, 41/98 linear, 18/106 multivariable, and 5/56 differential cases. Many of those old highs themselves belong to fluctuating display sequences, so this marker alone is not proof of diagnostic restoration.

Requiring the old high to precede the latest captured diagnostic makes the same-course review counts much smaller: 20, 6, 0, and 0. Separately, an earlier high on another course page appears in 19, 0, 2, and 5 review cases. The two multivariable lesson components in the motivating case have earlier highs on the **other** course page, so they remain a cross-context revalidation example rather than a proved same-course restoration of a saved counter.

The best working model therefore needs all three mechanisms: **ordinary signed practice credit, diagnostic/course reassessment, and transient displayed-state changes**. A diagnostic-restoration explanation is useful for the specific persistent lesson event, but does not explain all large jumps.

## What the engine should distinguish

Math Academy documents both **diagnostic blending into an existing profile** and a **clean-slate reset followed by recalibration**. It also documents conditional credit being pruned back, diagnostic balances becoming repetition credit, and course-based mastery floors. These are substantive state mechanisms, not changes to the mathematical overlap of two topics. The [mechanism review](mechanisms.md) gives exact local source references and distinguishes those documented behaviors from our implementation.

Our current native diagnostic initialization skips topics already marked learned. The progressive API's preservation of banked imported repetitions applies to the directly learned topic. Neither implements the full component-revalidation mechanism suggested by this case. Making encompassing weights larger to compensate would put the missing behavior into the wrong parameter.

Use the following distinctions in calibration:

1. **Ordinary review or practice:** estimate the usual spacing, ability and coverage response within the same course and diagnostic context.
2. **Diagnostic assignment or post-diagnostic revalidation:** allow a separate reassessment of existing knowledge. Prior observed high bands are evidence for this classification, not an instruction to reset repetitions to a historical maximum.
3. **Transient displayed change:** retain it as an observation, but do not equate its jump magnitude with lasting credit.

The useful evidence fields are account, course, task type, diagnostic epoch, direct question topics, KP correctness, source relearning status, same-course prior peak, separately recorded other-course peaks, co-changing topics, and observed persistence. The fraction choices for encompassing weights remain independent of those learner-state updates.

No engine policy, encompassing value or database state was changed in this analysis. The earlier pilot's held-out scores remain its original results; it did not distinguish all these regimes, so those results do not validate an ordinary-credit interpretation of the anomalous jumps.

## Reproduction

The frozen account reports supply the complete path manifests. The analysis never joins learner histories across accounts or treats an old course page as the same longitudinal observation series as a new course page.

- [case-study.json](case-study.json): course reads, raw HTML checks, correctness and exact persistence counts for the motivating example.
- [assessment-topics.json](assessment-topics.json): the directly assessed topics from saved question metadata or question-header links. All 674 saved assessment and multistep questions have resolved topic IDs; assessment and multistep task types remain separate.
- `*-patterns.json`: per-account activity comparisons, previous-high evidence and follow-up classifications.
- [extract_assessed_topics.py](../../../../capture/scripts/extract_assessed_topics.py) and [analyze_band_restoration.py](../../../../capture/scripts/analyze_band_restoration.py): reproducible extraction and analysis.

From the repository root:

```sh
python3 capture/scripts/extract_assessed_topics.py
PYTHONPATH=capture python3 -m scripts.analyze_band_restoration reference/mathacademy/encompassing-analysis-2026-10-11
PYTHONPATH=capture python3 -m unittest scripts.tests.test_band_restoration
```

Sixteen dedicated checks cover assessment inclusion, equal comparison scopes, question-topic extraction, account/course isolation, baseline deduplication, timestamp conflicts, initialization, and follow-up boundaries. They pass alongside the earlier analysis checks: **47 tests passed**. The four account outputs have no missing source paths, unmatched candidate events, or contradictory same-time topic reads.
