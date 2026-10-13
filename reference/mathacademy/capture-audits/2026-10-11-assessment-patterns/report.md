# Math Academy quiz availability: observations and best explanation

Reviewed October 11, 2026. Read-only investigation; no runners were started, no website settings were changed, and no database facts were written.

The strongest explanation is **an XP threshold combined with a separate eligibility condition for the quiz's topic pool, with queue changes applied at activity completion**. Completing a stuck activity can expose a quiz that elapsed time has made eligible. The subsequent [topic-by-topic analysis](topic-age-report.md) strongly supports a roughly **48-hour learned-topic age boundary in both first and later quizzes**: all 325 traceable question appearances satisfy it after checking two delayed recovery snapshots against original completion evidence. This remains an inferred boundary, not a published backend rule; age alone does not explain every absence. There is no established fixed overnight batch or requirement to stop using the website.

## Which courses actually served quizzes?

These are observed course enrollments, not runner names. An account changed courses several times. Numbers count distinct completed original quiz tasks; retakes are separate. Historical rows for Calculus I/II and early Foundations II come from the exported progress history, not the automated runners.

| Course | Original quizzes completed | Retakes completed | Availability evidence |
|---|---:|---:|---|
| Mathematical Foundations II | 10 | 3 | Quiz 1–10 in historical and capture evidence |
| Mathematical Foundations III | 25 | 2 | Quiz 1–25 in the main account's captures |
| Calculus I | 3 | 0 | Quiz 1–3 in historical progress |
| Calculus II | 3 | 1 | Quiz 1–3 in historical progress |
| Linear Algebra | 2 | 1 | Original linear account, before its course switches |
| Multivariable Calculus | 4 | 0 | Original multivariable account |
| Differential Equations | 4 | 1 | Original differential account |
| Methods of Proof | 6 | 0 | Linear account; includes the requested Quiz 6 |
| Mathematical Methods for the Physical Sciences I | 2 | 0 | Quiz 1–2 completed; Quiz 3 also appears offered in saved Learn HTML |
| Mathematical Methods for the Physical Sciences II | 0 | 0 | No assessment offered in 72 saved full Learn queue pages |
| Mathematics for Machine Learning | 0 | 0 | No assessment offered in 62 saved full Learn queue pages |

“Assessment” is the website's activity type for these quizzes. This dataset does not establish that formal midterms or finals were offered. Math Academy says midterms/finals are assigned for students taking courses for credit; that is a different condition from ordinary quizzes. [Official FAQ](https://mathacademy.com/faq).

The exported history also contains lessons attributed to Foundations I, Precalculus, and Algebra II. Those can be prerequisite activities within another enrollment. They do not establish separate course enrollments without quizzes.

There are short additional enrollment episodes that should not be merged with the original accounts' experiences:

- The linear account answered all 49 recorded Multivariable diagnostic questions correctly, then switched to Proof roughly 12 minutes later. No sustained post-diagnostic practice window exists for that Multivariable enrollment.
- The multivariable account answered all 19 recorded Proof diagnostic questions correctly, then moved on to Differential Equations. There are no captured ordinary learning activities in that Proof episode. Its lack of quizzes is weak evidence about quiz availability.
- The multivariable account's later Differential Equations diagnostic has 46 Correct, 3 Incorrect, and 1 No Credit records, but no captured ordinary learning activities before the next course switch. Its absence of quizzes cannot be compared directly with the original differential account's hundreds of learning tasks.

## The XP counter is much clearer than the first-quiz trigger

There are 32 observable intervals from completion of one original quiz to the first saved offer of the next. Thirteen early Foundations intervals have incomplete XP-ledger coverage and are excluded from the calculation. **All 19 intervals with complete coverage satisfy:**

`earned lesson/review/multistep XP since the preceding original quiz completed + displayed optional XP remaining = 150`

Examples:

| Account/course | Next quiz | Learning XP | Optional XP remaining | Sum |
|---|---|---:|---:|---:|
| Linear / Linear Algebra | Quiz 2 | 124 | 26 | 150 |
| Multivariable / Multivariable Calculus | Quiz 2 | 122 | 28 | 150 |
| Differential / Differential Equations | Quiz 2 | 129 | 21 | 150 |
| Linear / Methods of Proof | Quiz 2 | 120 | 30 | 150 |
| Main / Foundations III | Quiz 25 | 124 | 26 | 150 |

Quiz and retake rewards are excluded from these learning-XP sums. Their exclusion, and measuring from the previous original quiz's completion, fits every fully covered interval. This is strong evidence for how the ongoing counter behaves, not direct access to the implementation.

Offers usually first appear around 120 learning XP, with up to 30 XP of optional grace. At the deadline the quiz can become the sole offered task. Discrete task awards explain first observations at 121, 124, 129, etc. The website's description of a quiz every approximately 150 XP fits these observations. [Official FAQ](https://mathacademy.com/faq).

The first Proof quiz is particularly informative:

- Diagnostic task **14095701** earned **4 XP**.
- The account completed **31 ordinary learning activities**, earning **120 XP**, before the first saved quiz offer.
- Only **45 XP** of those activities belonged to topics in the retained Proof course graph; **75 XP** belonged to topics outside that graph.
- Quiz 1, task **14097922**, appeared with **26 XP remaining** before it became required.
- **4 + 120 + 26 = 150** exactly. Using only the 45 XP from Proof topics does not fit the countdown.

This strongly contradicts a universal rule that only enrolled-course-topic XP counts toward the 150-XP counter. It also suggests diagnostic XP entered the initial counter in this particular episode. It does not prove that every course/reset treats diagnostic XP identically.

Topic membership uses the retained `/home/jake/Developer/MA/COURSES/Math-Academy/University/*/GRAPH-*/Topics.csv` files. Membership in a course is different from the historical course label of a shared topic. The first Proof comparison is independent of the uncertain early Foundations course-switch boundary.

## First quizzes have an additional condition

The original Linear Algebra and Differential Equations accounts first show quizzes about **56.4** and **56.1 hours** after their diagnostic-completion snapshots. The multivariable account's first authoritative diagnostic timestamp was not retained, so its exact diagnostic-to-quiz delay is not calculated. Its first quiz appears alongside theirs.

Before their first quizzes, the accounts had already earned approximately:

| Account/course | Ordinary learning XP | XP on enrolled-course topics |
|---|---:|---:|
| Linear Algebra | 2,015 | 1,443 |
| Multivariable Calculus | 2,614 | 1,777 |
| Differential Equations | 2,349 | 1,633 |

These sums exclude diagnostic rewards. They are observed reward totals, not the service's internal counters. Nevertheless, they show that neither “reach 150 total XP” nor “reach 150 course-topic XP” alone explains the first quiz.

Methods I first appears with Quiz 1 in an authoritative saved dashboard about **49.2 hours** after its final diagnostic reset. By contrast, Proof offered Quiz 1 only **2.52 hours** after its diagnostic. A universal minimum wait of a week—or even two days after every diagnostic—is therefore inconsistent with the records.

The courses still without quizzes have shorter follow-up:

| Course | Ordinary completed learning activities | Earned XP | XP on course topics | Time from diagnostic completion through last captured learning activity |
|---|---:|---:|---:|---:|
| Methods II | 67 | 796 | 762 | 8.8 hours |
| Machine Learning | 59 | 516 | 469 | 9.8 hours |

Most of their captured work is already on enrolled-course topics. “They are only doing prerequisites” does not explain these two absences. But their follow-up is much shorter than the roughly two-day delay seen in several courses that eventually served quizzes. Absence in these records does not establish missing quiz support.

Math Academy describes quizzes as drawing from previously learned topics, prioritizing the enrolled course, and reducing priority for topics already quizzed or encompassed by other eligible topics. That supports a topic-pool explanation, but it does not disclose the exact eligibility test or counter. [Official algorithm description](https://mathacademy.com/how-our-ai-works).

## Did the pause cause the synchronized first quizzes?

On October 10, the three original university accounts resumed after approximately 12 hours without saved queue observations. Their first loads at roughly **01:12 PDT** still showed the old queues and unfinished activities, with no quiz. After each finished an activity, Quiz 1 appeared:

| Account | Completed task immediately before the quiz appeared | First saved Quiz 1 offer, PDT |
|---|---|---|
| Multivariable | 14071855, Tangent Lines to Level Curves review | 01:13:14 |
| Linear | 14074772, Ranks of Generalized Eigenvectors lesson | 01:16:25 |
| Differential | 14071771, Falling Body Problems With Linear Drag lesson | 01:20:24 |

The quizzes' task IDs were newly clustered: 14093183, 14093211, and 14093248. Their appearance follows completion on each account; it was not simply visible on the first read after the pause. A synchronized runner restart is a substantial confound for any supposed synchronized backend batch.

The best programming explanation is that eligibility depends on elapsed time or topic history, but the queue is refreshed/generated when an activity finishes. Time passed during the pause; finishing the saved activity applied the next scheduling decision. A background job remains possible, but these observations do not require one and do not show that the engine must be idle to calculate weights.

This also directly supports `capture/principles.md` principle 1: an unfinished activity can block the queue. It does **not** establish that every unfinished activity blocks every other activity; the multivariable account had several unfinished tasks and exposed a quiz after resolving one.

Math Academy says new lessons unlock immediately after completion, which also argues against the whole scheduling engine waiting for an idle period to update. [Official algorithm description](https://mathacademy.com/how-our-ai-works).

## Does diagnostic accuracy explain it?

There is no convincing evidence of an acceptable diagnostic-accuracy band that switches quizzes on.

- The Proof account had only **3 Correct out of 8** saved diagnostic question records, yet got a quiz about 2.5 hours later.
- The new Methods II diagnostic analysis contains **58 Correct / 22 Incorrect** entries, and Machine Learning contains **52 Correct / 17 Incorrect** entries. Both are comparatively balanced, yet neither served a quiz in its short follow-up.
- All-correct diagnostic episodes without quizzes were followed by immediate course changes and little or no ordinary work, rather than a comparable sustained capture window.

These are adaptive diagnostic records, not comparable standardized exam scores. Some diagnostics deliberately answered prerequisite questions and skipped course material, the main Methods diagnostic was reset, and retries/answer timing affected the evidence. A raw correct fraction cannot represent the resulting knowledge profile.

My judgment is that diagnostic calibration acts **indirectly**: it changes which topics are marked known, which need remediation, and which topics can contribute to a quiz. Overestimating knowledge can leave less newly practiced material to audit; underestimating it can create substantial prerequisite remediation. Either could alter the initial eligible pool without any special accuracy switch. Math Academy explicitly describes diagnosis as weighted evidence, including response time, and describes approximately 80% as a target for **quiz difficulty**, not a diagnostic gate. [Official algorithm description](https://mathacademy.com/how-our-ai-works).

## Ranked explanation

1. **High confidence: XP controls the regular cadence, with an optional window around 120–150 learning XP.** The complete intervals match exactly, across several accounts and courses.
2. **Strong observational evidence: individual learned topics satisfy an approximately 48-hour age boundary before quiz selection, including later quizzes.** The [subsequent analysis](topic-age-report.md) checks the selected topics directly, across account course switches. Additional mastery or selection requirements remain unresolved, and age is not a sufficient predictor by itself.
3. **High confidence as an observed trigger; moderate confidence about implementation: finishing an activity causes the next queue decision to appear.** The three synchronized restarts show this directly. A pause could help by allowing time to pass, rather than by allowing the engine to think.
4. **Certain confound: our selection policy delays optional quizzes.** The old selector prefers eligible lessons/reviews to optional quizzes and can take an optional quiz only as a fallback; the new selector likewise ranks unstarted assessments below learning activities. A completed-quiz count alone does not reveal when a quiz was first available. Methods I already has an offered, uncompleted Quiz 3 in saved evidence.
5. **Possible, currently weak evidence: per-course configuration, content eligibility, or feature support.** Methods II and Machine Learning might differ in configuration, but their roughly 9–10-hour follow-up is too short to distinguish that from delayed eligibility. Differential Equations demonstrably served quizzes despite being described publicly as in development, so a development label is not sufficient evidence of disabled quizzes.
6. **Low confidence: an idle-only weight calculation, a universal daily batch, or a diagnostic accuracy sweet spot.** The observations do not require these explanations, and the fast Proof quiz contradicts a universal post-diagnostic delay.

From a learning-design perspective, a quiz is most useful after enough practice to make unaided retrieval meaningful, across a diverse pool of topics. That is a plausible rationale for the extra eligibility condition, not proof of a specific scheduler implementation. Their adult-student page describes reviews beginning after a few days and quizzes within roughly a week under ordinary usage. That timing is descriptive, not a documented hard gate. [Adult-student introduction](https://mathacademy.com/adult-students).

## What would distinguish the remaining possibilities?

### Preliminary follow-up: estimating an initial and recurring time requirement

The course-level estimates below preceded the [topic-by-topic follow-up](topic-age-report.md). The newer evidence supports topic aging for every quiz, rather than a time gate limited to the first quiz.

The last timestamped Methods I dashboard without an unlocked Assessment is the post-activity observation for task 14114664, at **45.87 hours** after its final diagnostic. The first quiz offer is at **49.21 hours**. If a simple initial time gate explains this episode, **48 hours** is a plausible working estimate within that bracket. There is a gap in observed activity across the bracket, so it does not establish the gate or its precise anchor.

Across **41** consecutive original-quiz intervals with saved offer times, the shortest completion-snapshot-to-next-offer gap is **84.38 minutes** (Foundations III Quiz 23 → Quiz 24). The old pacing record places actual completion about 16 seconds before that snapshot, giving approximately **84.65 minutes**. Multivariable Quiz 3 → Quiz 4 was offered after about **88 minutes**, and Quiz 1 → Quiz 2 actually started about **101 minutes** after the previous completion snapshot. Thus a universal recurring gate of two hours or more, measured from quiz completion to availability/start, is inconsistent with these observations. A minimum measured from start to start would use a different clock.

There is no clear evidence of a separate shorter recurring quiz-to-quiz timer: the intervals are already explained by earning roughly 120 XP before the optional offer. The newer preferred model is a roughly two-day age condition on selected learned topics in every quiz, combined with XP-driven cadence. Later quizzes can use topics that have already aged. The observations bound any universal completion-to-offer minimum to at most approximately 85 minutes; they do not establish a one-hour timer. Proof's first quiz after 2.52 hours prevents treating 48 hours as a universal post-diagnostic rule: its seven selected topics had been learned under the same account's previous course more than 48 hours earlier. Derived intervals are retained in `quiz-time-intervals.json`.

The next observation should record the first quiz **offer**, its optional-XP countdown, and the preceding task's completion, separately from when our runner chooses to take it. Keep account, enrolled course, total learning XP, course-topic XP, diagnostic reset, and any unfinished tasks explicit.

For the two courses without quizzes, a clean pause with no unfinished activities is the useful comparison. At the next authorized session, read the queue before doing anything, then again after the first completed activity. An offer on the first read supports a time-triggered/background update; an offer only after completion supports a completion-triggered refresh of time-dependent eligibility. If quizzes stay absent after a follow-up comparable to the positive courses and substantial native-topic practice, course-specific configuration becomes a stronger hypothesis. This investigation did not initiate that experiment.

## Evidence and limits

- `evidence.json`: 3,041 distinct account/task capture records, 3,778 structured queue observations or original Learn pages, enrollment summaries, diagnostic summaries, and XP/topic-membership metrics. The 219-row historical progress export supplies additional earlier quiz history. Timestamped new post-activity dashboards are analyzed separately.
- `quiz-intervals.json`: every interval, including missing-XP counts. The 19 exact matches refer only to the fully covered intervals; the other 13 are not treated as zero-XP periods.
- `new-dashboard-offers.json`: seven distinct assessment tasks observed in timestamped new-engine post-activity dashboards.
- `topic-age-report.md`, `topic-age-evidence.json`, `topic-ages.csv`, and `topic-age-controls.json`: subsequent direct topic-age analysis, exclusions, original completion bounds, negative controls, and remaining eligibility uncertainties.
- `analyze.py` and `details.py`: reproducible, read-only source analysis. They write only derived files in this audit directory.
- Old non-diagnostic enrollment associations are inferred from diagnostic transitions and retained course profiles. The main Foundations II → III boundary is inferred from the quiz-number restart and later MF III profile, not an exact saved enrollment event. Progress-snapshot course lists are deliberately not used as enrollment IDs: some old snapshots tracked Foundations courses even on university accounts.
- Old post-activity snapshot timestamps can be late when recovered. New hashed queue file mtimes are not used as authoritative offer times. A first saved offer bounds observation, not the exact server-side generation time.
- Source archives, activity questions, native database records, capture code, and principles were not modified.
