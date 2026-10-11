# Capture rebuild

Design a fresh capture system with small, clearly separated modules. Use the existing script and saved captures to understand Math Academy and preserve useful evidence. Existing behavior is not automatically a requirement for the new build.

The six stage documents in `docs/` describe the agreed design. Follow [principles.md](principles.md) when building the modules in `scripts/`.

Lesson and Review priority scores are based on the downstream targets their topics support through the prerequisite graph. Both activity types use the same scoring policy.

## What we have agreed

- Build fresh rather than continue adding exceptions to the old script.
- Give each stage a clear job and a defined record to pass to the next stage.
- Prioritize progress, fault tolerance, and resumability. Math Academy limits which activities appear in the queue; leaving one unfinished can prevent new work from appearing.
- Queue Processing handles the activity queue only. Course summaries, the completed-activity list, and XP tracking belong to Post-Activity Processing.
- Activity Capture includes doing the activity and reviewing its activity history page afterward. Each activity type has its own capture path.
- Post-Activity Processing contains the general actions shared by all activity types and has its own separate stage.
- Never quit, defer, or abandon an activity because of runtime problems. Every failure has a default next action. Recover and continue; after an external interruption or manual stop, resume that activity when operation resumes.
- Finish each activity and its question judgments together. A competent agent resolves every question within that process; genuine ambiguity or unavailable evidence receives a final, reasoned finding. Nothing waits for Jake's judgment or a held-question queue.
- Apply each activity type's answer policy as a default. Override correctness sequences when disagreement, ambiguity, timing, or unexpected behavior requires it to continue; record the planned response, actual response, and reason.
- Save enough progress to continue after an external interruption or manual stop. After an interruption, check what Math Academy already accepted before repeating an action.
- Resolve source-content gaps during Activity Capture's final history and lesson-page review. Database Preparation receives checked source content and handles database mapping and transaction construction.
- Diagnostic behavior uses course membership and shortest prerequisite distance, with the answer probabilities and timing recorded in `docs/3-Activity-Capture.md`.
- Keep **Activity Capture** in one design file with the shared process followed by each activity type. Draw Post-Activity Processing separately.
- Keep the writing and charts understandable without reading the code.
- Resolve runtime ambiguity through scripted defaults and focused agent judgment. Never make asking Jake a requirement for continuing an activity.

The existing source rules still apply: preserve Math Academy's original content, including its errors. Keep our corrections separate and apply them later under the appropriate source. A guess submitted to finish an activity does not by itself establish a correct answer for the database.

## Shared foundations

**One way to work with Math Academy.** A shared browser module reads pages and performs actions such as opening an activity, filling an answer field, submitting, and continuing. It returns the same kinds of records to every activity module. Page selectors, HTML parsing, and browser details live here.

**One capture record.** Use a consistent record for original page evidence, questions, answer fields, submissions, grades, worked solutions, images, lesson structure, and completion. Keep source observations distinguishable from the agent's reasoning and conclusions.

**One way to save and resume progress.** Every activity uses the same mechanism to save its position and record actions before submitting them. Save question evidence, response decisions, agent judgments, and external action outcomes. Browser or process failures trigger automatic recovery; check accepted actions before retrying them. An unavailable dependency triggers retries with backoff, preserving progress. Respect manual stops and resume when operation restarts.

**Shared tools, separate activity rules.** Reuse answer-field handling, image collection, page reading, and saved progress. Each activity type specifies its own sequence and answer policy. Avoid one large function containing every activity's exceptions.

The shared process and activity-specific behavior are described in `docs/3-Activity-Capture.md`, including navigation, answer/skip policy, submission timing, and history-page review.

**Python controls the workflow and detects exceptions.** It reads and validates captures, applies policies, performs browser actions, matches known database identities, and builds and submits transactions. It calls agents for mathematical answers, interpretation of source evidence, or ambiguous database identity matches. Each call includes the specific question or detected exception and relevant evidence; the agent returns a structured result that Python checks before acting. Database Commit is entirely scripted.

**Every failure has a next action.** Python retries or changes the failed operation, replaces an unavailable solver, or requests a focused agent decision. Truly unanswerable questions receive a final finding and the best valid response or offered Don't Know/skip. Unexpected exceptions return control to recovery with saved state instead of exiting the capture loop. Repeating the same failed reasoning indefinitely is not progress. See Activity Capture's default actions for question and page failures.

**Keep capture moving after resolution.** Save the completed capture, question judgments, and original images before starting another activity. Pending database work retries automatically in saved order through one database worker while capture continues. Only the capture loop selects activities; background workers report their status. Nonessential account observations also retry without blocking the queue or interfering with the active page. Capture completion and verified import are distinct states. If durable storage is unavailable, retain state and retry saving before advancing.

**One way to read and write the database.** Selection and preparation receive the database information they need through a shared interface. Transaction/Commit owns database writes. Keep account login, queue state, and activity progress separate for each account while sharing the content database and image library.

Choose implementation details within these boundaries.

## 1. Queue Processing

**Job:** produce a reliable record of what the account's queue page shows.

Agreed actions:

- Read the activities in their displayed order, keeping Math Academy's identifiers and wording.
- Default to expanding every activity in the queue, collecting its links, and recording any details.
- Record each activity's type, title, links, progress, and available details, including assessment question counts, time limits, requirements, and retake labels.
- Preserve unexpected cards or missing fields as observations so later stages can respond to them.
- Recover from read errors where possible and continue with the usable queue details.
- Save the extracted queue details in their displayed order alongside the queue's HTML. Activity Selection uses that record to decide what to do.

Agreed scope: the activity queue only. The course summary, completed-activity list, and XP calculations move to the shared Post-Activity Processing stage.

Agreed card handling: default to expanding every activity shown in the queue, collecting its links, and recording any details. Jake noted that the cards previously left closed do not contain additional details and does not expect locked activities to appear in the queue. No separate locked-activity handling is planned.

Agreed evidence: save the queue's HTML alongside the extracted details so a bad read can be reviewed from the saved page.

Queue reading must be fault tolerant and continue. Routine retry and recovery details are implementation decisions; an unreadable card must not prevent processing the rest of the queue.

## 2. Activity Selection / Priorities

**Job:** choose an activity and explain why it serves our capture goals.

Agreed form: prioritize the five base activity types—Lesson, Review, Assessment, Multistep, and Diagnostic—in either started (begun but not completed) or unstarted form. Rank Lessons and Reviews together by priority score within each status group. This gives eight priority levels covering the same ten type/status combinations. Choose the first available level, then the highest-scoring Lesson or Review within that level.

Use the queue record, desired content, existing captured content, and the account's Math Academy progress. Pass the selected activity and its reason to Activity Capture, which applies the activity's answer and completion policy.

The agreed order is listed in `docs/2-activity-selection.md`: started Assessment, Diagnostic, Lesson/Review by score, Multistep; then unstarted Diagnostic, Lesson/Review by score, Multistep, Assessment. Started activities come before unstarted ones. Comparing scores happens when choosing or resuming an activity; changing scores must not interrupt the activity currently being captured. Use queue order for equal scores or when none are available. An assessment offered alone will still be selected even though unstarted assessments rank last.

Python calculates Lesson and Review scores from the downstream targets their topics support through the prerequisite graph. Record those targets with the selection reason.

Jake expects a required assessment to be the only displayed queue option. Treat that as an observation to verify when needed, rather than a separate priority category.

Diagnostic behavior follows its separately agreed course-membership and prerequisite-distance policy.

## 3. Activity Capture

**Job:** do the activity and then review its activity history page to capture its content and results.

Activity Capture covers both parts:

1. **Do the activity.** Carry it through to Math Academy's completion state, saving the original content and evidence from each interaction.
2. **Review the activity history page.** Collect the recorded questions, results, grades, and worked solutions, and connect them to the evidence saved while doing the activity.

Together, these form Activity Capture. Before handing off to Post-Activity Processing, Python checks source completeness and fetches missing evidence. It calls the activity's agent when the evidence needs interpretation, including ambiguous answer evidence, and checks the returned result. Lessons also receive the full topic-page review. Recovery does not change the fact that Math Academy already completed the activity.

Use [3-Activity-Capture.md](docs/3-Activity-Capture.md) as the single design document: shared activity/step and question processes, followed by Lesson, Review, Assessment, Diagnostic, and Multistep.

Assessment question counts and time limits belong to Queue Processing. Activity Capture uses those values and observes the current time remaining during a timed activity.

New and failed lessons are paths within Lesson capture. Resuming an interrupted activity continues that activity; it is not another activity type.

Python applies the answer and completion policies recorded for each type, including their fallback actions. During an activity it preserves uncertainty and continues; during final source review the agent closes every question judgment before handoff. A confirmed source error or genuinely unavailable answer has a recorded final finding, not a request for Jake or a future review. Preserve Math Academy's originals and the agent's separate conclusion.

## 4. Post-Activity Processing

**Job:** perform the account-level work that follows any completed activity, once, through shared Python code. See [4-post-activity-processing.md](docs/4-post-activity-processing.md).

This stage owns the course summary, completed-activity list, XP tracking, and updated topic progress. Compare progress with the previous observation and record activity completion. Keep these observations available for later use without automatically treating them as learner facts in EDB.

Read the dashboard and tracked courses' progress pages after capture, as specified in the stage document. Save retake instructions from available completion evidence. Retry missing nonessential observations without blocking capture or repeating the completed activity, recording their actual observation times. Startup reads and retry details are implementation choices.

Activity Capture hands off to this shared stage after collecting and checking the activity's content and history.

## 5. Database Preparation

**Job:** use Python to turn checked captures into prepared transactions. See [5-database-prep.md](docs/5-database-prep.md).

Reconcile questions, answer fields, solutions, tutorials, knowledge points, lesson steps, and multistep structure with the existing database. Python matches known identities and detects conflicting or ambiguous mappings. Only those cases go to an agent with the candidate entities and source evidence; Python checks the proposed resolution before building EDN. Preserve existing identities for confirmed source revisions. A newly discovered source-content gap returns directly to Activity Capture's agent for a final judgment now.

Python converts content, stores images using the existing SHA-256 layout under `/media/jake/SSD/EDB/math/images`, builds references and schema relationships, and calculates the topic workload multiplier from the checked lesson inputs. It produces reviewable EDN with separate source attribution for original and derived facts, and validates complete batches. An agent's final finding of insufficient evidence excludes only the affected content and dependent references, with an explicit reason. Complete supported content proceeds; no partial question or guessed authoritative answer is imported. An unavailable database leaves a durable completed capture for automatic preparation later, while new capture continues.

## 6. Database Transaction / Commit

**Job:** use Python to preview, commit, and verify prepared transactions against `/media/jake/SSD/EDB/math`. See [6-database-commit.md](docs/6-database-commit.md).

Content interpretation stays in Activity Capture; database identity decisions stay in Preparation. Python checks the prepared changes, submits them with the agreed source, records the receipt, and verifies the database result. It handles exact retries and classifies rejected or unknown outcomes. If a write times out, establish whether it committed before sending a different transaction.

Commit validated original content automatically. Preserve corrections already decided by the capture agent separately; later correction transactions follow the originals under their own source. Database work never waits for Jake to judge the content. Batch sizing is an implementation choice; follow the stage document's basis guards, exact retries, and read-back verification. A pending import retries automatically without blocking capture, and is marked complete only after verification.

## Design files and build sequence

- `docs/` holds the six stage documents, from `1-queue-processing.md` through `6-database-commit.md`.
- `scripts/` holds the replacement implementation as it is built.
- `principles.md` holds the rules shared by every phase.
- Keep one Activity Capture document with the shared process and activity-specific sections. Add charts as the design is settled, with separate Post-Activity Processing, preparation, and commit charts.
- Update this plan as decisions are made. Keep unanswered questions visible rather than filling them with assumptions.
- After the designs fit together, agree on the implementation sequence and checks using saved captures. Test completion and recovery before switching live accounts to the replacement.

The replacement is implemented in `scripts/`; see [its README](scripts/README.md) for modules, commands, storage, and recovery. Tests use saved captures and simulated failures; schema checks also use speculative EDB previews. Running workers are switched separately. Downstream target configuration will be added afterward.
