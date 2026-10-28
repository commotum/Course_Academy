# 3. Activity Capture

Complete the selected activity, then review its history page to finish the capture. The shared process handles content; each activity type sets the answer policy, submission timing, and completion rules.

**Python controls the process:** page navigation, extraction, images, answer policies, timing, response entry, and completeness checks. It calls the math-solving sub-agent for answers and source interpretation. When checks find missing or conflicting evidence, Python requests a focused agent review, performs any additional page reads, and checks the returned result. The agent returns answers and evidence; Python records and acts on them.

## 3.1. Shared Process

Our schema separates the activity's structure from the content it presents:

| Record | What it contains |
|---|---|
| Activity | Title, type, scope, time limit, and steps. |
| Step | A content reference and its place in an activity or multistep. The owner's first-step and `step/next` define linear order. |
| Tutorial | A title and instructional content, including equations and images. |
| Knowledge Point | A canonical example and a pool of practice questions. A lesson step can present the knowledge point and expand into both. |
| Question | Problem, calculator requirement, answer fields, worked solution, and observed difficulty. Canonical examples are also questions. |
| Answer Field → Answer | The field's type and location, its answer choices, and a reference to its correct answer. |
| Multistep | Shared context and its own ordered steps. |

Capture complete formulas, preserving MathML table rows, column roles, grid rules, fences, zero-rule fraction stacks and operator limits. Never serialize a math table as pipe-and-semicolon text: `|=` is an alignment artifact, not an extra mathematical bar. The legacy JSON fallback must stop for structural conversion when it encounters a MathML table. Normalize and validate complete reconstructed formulas through `scripts/question_capture/math_format.py`, then compare actual renders against the source. Preserve intentional illustrations. Comparison-only aliases such as Unicode and ASCII derivative primes may help locate matching source grids; they must not silently change stored expressions.

Matrix-entry controls are semantic matrix cells, not a spreadsheet. Preserve source row/column spans and every live math-editor field when capturing HTML tables. For authored or repaired matrix-answer prompts, use `matrix_answer()` with the existing field keys in source row-major order; keep labels and bracket decoration outside the answer cells.

### Activity and steps

1. Open or resume the activity using its queue details. Save instructions, task ID, title, and topic/course references before starting when possible. Read instructions before starting a timed activity; use the queue's question count/time limit and monitor the live timer.
2. Follow Math Academy's steps. Record each step's title/type, content ID, verified placement ID when available, and position. Save its HTML, screenshot, and original images, including source URLs and where images appear.
3. Capture the content identified in the table above. Expand knowledge points into their example and practice, and multisteps into their shared context and parts. Use the question process below whenever a response is required.
4. Save responses and feedback before advancing. Continue until Math Academy ends the activity, recording success, failure, or timeout as the actual outcome.
5. Open its history page and expand every question. Match source IDs and positions to the live capture. Add difficulty, topic/knowledge-point/example references, final grades, revealed correct answers, and worked solutions, preserving the history HTML, screenshots, and images.
6. Before leaving Activity Capture, Python checks the live questions against history, including repeated presentations, and checks answer fields, correct-answer evidence, source identities, images, and activity structure. It fetches missing source material immediately. If the evidence needs interpretation, it gives the same sub-agent the specific gap or conflict and relevant captures, then checks the proposed resolution. Include the full lesson-page review described below when applicable.
7. Finish the source review and save a checked capture before handing it to Post-Activity Processing. Every question has an agent's final answer judgment and supporting evidence, including a reasoned finding of source error, genuine ambiguity, or unavailable evidence. Missing optional values are recorded as absent. No question waits for Jake or a later judgment queue. Learner responses, timing, and solver reasoning remain evidence for later.

Keep task, content, and placement IDs separate. Questions use `q-N`; canonical examples use `e-N`. Screen labels such as `step-qN` are not verified placement IDs. Keep observed attempt order distinct from reusable activity structure; preserve evidence of the route actually taken.

Retain an unfinished activity through errors or uncertain answers. Completing it lets Math Academy expose more work. Recover automatically, change strategy when retries fail, and expose persistent blockers while backing off with spaced probes. After an external interruption or manual stop, resume saved progress and check what Math Academy already accepted before repeating an action.

In lessons, Continue advances from the selected sidebar step. Scrolling to a short tutorial can select the preceding question instead. Settle the scroll, select the observed Continue button's matching sidebar step when necessary, and confirm that selection before clicking Continue. This uses the visible controls and preserves the saved action intent; it never resubmits an accepted question to recover navigation.

Custom dropdowns hide their menus on scroll. Position and settle the original frame below the observed visible fixed lesson header before opening, require the entire selected option inside the viewport, and never scroll an open menu. One reopen of the same original frame and option is allowed after the menu is already hidden; overlays, replaced controls, and changed readback remain entry failures.

Finish the activity and its question judgments as one unit of work. Math Academy completing an activity and us finishing its capture are separate events. Resolve source ambiguities during the final history/lesson-page review. Decide disagreements now and preserve both Math Academy's stated answer and the agent's conclusion with their evidence. A final finding that evidence is unavailable closes the judgment without inventing an answer or repeating the activity.

### Questions

1. Before answering, save the problem, calculator instructions, question ID when visible, HTML, screenshot, and images. Record each answer field's type, location, choices, and displayed order.
2. Launch one competent math-solving sub-agent for the first question and save its session ID. Resume that same conversation throughout the activity, including across knowledge points. Send each new question's fields, current choices, screenshot, and images, plus new examples, shared context, solutions, and grades. Earlier questions and reasoning remain in the conversation. Python restarts or replaces an unavailable or repeatedly inconclusive agent using the saved evidence.
3. When answering, request the correct answer for each field, reasoning, and confidence; save these separately from Math Academy's content. Apply the activity's answer policy to choose the actual response and preserve that decision on resume.
4. Enter and verify the field values or selected choices. Submit when the activity calls for it. Record actual responses, skips, retries, and timing. Check current choices again after a reload or shuffle.
5. Save each revealed grade, correct answer, worked solution, HTML, and image. Capture and answer any additional fields revealed within the same question before advancing.
6. Give feedback to the same sub-agent to check its answer. Resolve disagreements within the activity and record its conclusion separately from Math Academy's answer. A submission alone does not establish the correct answer.
7. During history review, Python records difficulty and checks the complete question record. It sends ambiguous answer evidence to the sub-agent for a final judgment before ending capture. If another competent agent is needed, Python requests that review now.

**C** means intended correct; **W** means intentionally incorrect. The sub-agent solves for the correct answer in both cases. Record intended responses separately from actual grades. The sequences and probabilities below are defaults: completion takes precedence when a disagreement, ambiguous question, timer, or unexpected behavior requires a different response. Save the planned response, actual response, and reason for deviation. Continue the sequence at its next position rather than restarting it.

For live response selection, confidence describes the mathematical answer separately from evidence of Math Academy's key. A missing source key alone must not override a planned W response, even when the source-evidence status is ambiguous or unavailable. Require mathematical confidence of at least 0.5, a supported answer for every active field, and no source disagreement before choosing an intentional error. Preserve the existing fallback when no demonstrably different valid response is available. On resume, restore a previously overridden W only if no response was submitted and the current answer meets these conditions; keep completed attempts and the original policy draw intact.

Failed entry and guarded `not_submitted` returns are browser recovery events, not learner submissions. They do not authorize a source-preferred all-correct retry. Record the guard's reason, back off, and reread before acting. After two focused recovery judgments on unchanged evidence, expose a persistent blocker and replace repeated reloads with spaced probes. Keep the activity pinned, resume normal recovery when source evidence changes, and preserve assessment submission deadlines throughout the wait.

Bind captured images to their source occurrences within the prompt or individual choices. Multiple source URLs can legitimately share one file by hash; that shared path must neither merge their source identities nor cause a false changed-question guard.

### Timing and browser readiness

Browser latency, answer pacing, and recovery waits serve different purposes. Their defaults are configured in [config.py](../scripts/config.py):

| Timing | Default and scope |
|---|---|
| Browser interaction latency | At least **500 ms**, including connections to an existing browser. Configuration cannot lower this minimum. |
| Event waits | Random **0.8–2.5 seconds** around navigation, field selection, continuation, history expansion, and assessment confirmation. |
| Lesson, review, and multistep answer pacing | Random **5–12 seconds** from observing the question to submitting its response. Capture and solving time count toward this target. |
| Assessment pacing | A saved schedule targeting **70–85%** of the stated time limit, bounded by the remaining time as described below. |
| Diagnostic answer pacing | The separate course/prerequisite policy in §3.5. The ordinary 5–12 second answer wait does **not** apply. |
| Browser timeout | **45 seconds**, shortened when an active assessment has less time available. Expired assessments still allow bounded reads to recover their results. |
| Solver request budget | **300 seconds total**, including retries; assessment requests receive a smaller budget when needed. |

Save each sampled answer delay and submission due time before acting. Resume the remaining wait without drawing again. A newly revealed editable stage can have its own ordinary answer delay; rereading or retrying that same stage must not restart it. When solving takes longer than the target, add no further answer wait. All deliberate waits remain interruptible, and assessment deadlines shorten optional pacing. Between-activity rests belong to [Activity Selection](2-activity-selection.md).

Wait for question fields, rendered mathematics, canonical examples, tutorials, revealed explanations, and expanded history content before extracting them. Check images and diagrams for at least 500 ms of stable rendering; retry broken images with recovery backoff. MathEditor entry allows its initial 500 ms poll and a subsequent 200 ms poll before readback. Verify values again after saving evidence, and recheck the question identity, problem, and current fields before submission. Delayed rendering, a reused diagnostic container, or shuffled choices must not send an old answer to a new question. Readiness timeouts preserve readable content and explicit errors for recovery and agent judgment.

Keep original source bytes separate from browser compatibility repairs. Remove identical duplicate MathEditor script tags only after saving the original HTML response and a transformation record under the account's `reference/` capture directory. Preserve raw SVG sources and image hashes alongside any rendering support. Retry transient screenshot/font failures; retain an explicit error if evidence remains unavailable.

A failed history solution image alias can use a prior own original raster only when the permanent question identity, complete solution text, image count and position, original SHA-256, and full image decoding agree. Keep the alias fetch/render failures in provenance and extraction-error history; this restores original source evidence without claiming that the alias rendered in the browser. Canvas and SVG readiness failures still require their own source checks.

History alignment requires agreement on the problem, answer fields, and choices as well as source IDs or position. Position alone cannot attach a different question's ID or grade. Preserve conflicting originals and unresolved live presentations separately, and withhold a history grade when repeated presentations make its recipient ambiguous. Completeness checks include tutorials, canonical examples, images, extraction errors, and every declared lesson step. A final unavailable judgment preserves the gap; it does not silently remove the missing evidence.

For comparison only, normalize paragraph-wrapper whitespace at the boundaries of complete mathematical spans and answer placeholders. Preserve the mathematical tokens and internal whitespace: `$1 2$` must not match `$12$`, and field order must agree. Keep the original prompts intact; this comparison rule cannot reconcile changed mathematical content or missing controls.

Completed history questions can replace live blank inputs with static `.freeResponseTextbox` boxes while displaying the grade outside the question node. Capture those boxes as ordered, read-only blank fields and retain their original HTML and displayed text. Keep the field placeholders in the problem so live/history comparison checks the same prompt and field layout. Exclude learner `studentAnswer` blocks and solution controls. A displayed history value alone does not confirm a submitted response; answer attribution still requires the checked source evidence above.

Extract every authored problem section, including sibling `.questionBody` and `.questionWidget-body` sections containing proof steps, tables, or additional fields. Include nested sections once, preserve paragraph and table boundaries, and keep feedback and solutions separate from the prompt. Record the problem's field keys so a missing normalized placeholder is a completeness failure. Prose sentence-boundary repairs must not change mathematical tokens or relax mathematical whitespace checks.

Preserve ordered-list labels, nesting, and observed numbering resets from source list styles, `type`, `start`, and item `value` attributes; saved Math Academy `questionStatements` lists retain the upper-Roman labels verified in its public stylesheet.

Preserve every source HTML table as normalized HTML using the source-table contract in `scripts/question_capture/html_tables.py` and `scripts/question_capture/table_html.js`. Retain actual `td`/`th` roles, row and column spans, nested tables, captions, source alignment, rules, and shading through validated data attributes. Retain rendered mathematics, field placeholders, list boundaries, and captured assets. Never turn the first data row into an invented Markdown header, flatten a table inside a list, or discard cell shading. Unsupported spans or CSS layouts receive explicit extraction gaps instead of guessed cell positions. The shared player decorator makes source colors readable in both themes; arbitrary source styles remain forbidden.

Preserve Markdown paragraph and list boundaries around complex HTML tables. Preserve zero-rule MathML fractions as unfenced TeX stacks while keeping any source parentheses; unknown fraction-rule attributes receive explicit gaps rather than inferred division or binomial semantics.

When a source SVG title mixes literal TeX with nested MathML, the nested root may represent only an inner fragment. Preserve or reconstruct the complete outer expression, including operators, equalities, labels, fences and explanatory color. If full reconstruction is unsupported, retain the whole graphic or report an explicit extraction gap. Never substitute the first descendant MathML root for the complete formula. Compare source replay against the original complete expression, because truncated math can render with zero MathJax errors.

Normalize the complete formula after recovering its fences: a generic MathML table inside brackets or determinant bars needs a matrix environment, including when it is nested inside an aligned derivation. Preserve every ordered cell and genuine equation alignment. Check matrix column spacing and fence height visually; malformed fenced `aligned` tables can typeset without any MathJax error.

An unfenced source data table with explicit column alignment also needs its own array layout; do not apply equation-pair spacing to it merely because it has no grid rules. Preserve `lim` as an operator with its complete tendency condition, and preserve piecewise value/condition rows with their visible brace. When matching old source evidence, equivalent derivative primes (`′`, `'`, `\prime`) are comparison aliases only; retain current cell bytes when repairing table structure. Source reconstruction must normalize the complete formula after walking MathML, then pass both structural and matrix-layout validation.

Preserve literal MathML brace operators and curly `mfenced` delimiters as visible TeX braces (`\{`, `\}`). Keep serializer grouping braces unchanged, and bind an observed select marker before rendering its MathML delimiters. Only `{{field-N}}` tokens identify normalized answer controls; nested authored sets such as `{{2}}` do not declare fields.

Preserve explicit MathML `mathcolor`, `mathbackground`, and `mathvariant` on visible entries with local TeX scope. Row/column focus, pivot emphasis, bold vectors, script basis names and blackboard number domains carry instructional meaning. Do not silently remove unsupported variants or colors; emit an extraction gap. Check both source and rendered output, including unchanged neighboring entries, so styling does not leak across cells. Original source arithmetic still needs independent checks.

Preserve explicitly shaded or bordered phantom containers with their original hidden mathematics and exact symmetric integer padding. The local MathJax 3.2.2 bbox extension renders those source attributes; unsupported colors, CSS, padding or hidden geometry receive explicit gaps. Preserve hidden width inside original long-division enclosures, while leaving bare phantom samples unchanged. Source repairs bind the extractor generation and retain original HTML; refresh only questions whose source output actually changes.

The local renderer also loads the matching enclose and cancel extensions so original polynomial-division enclosures and cancellation marks remain visible. These vendored files come from the same integrity-checked MathJax 3.2.2 archive as the existing renderer. Verify source notation through the actual UI configuration and typesetting functions.

For completed history proofs, use the grade parsed from that question's enclosing history entry when the grade is outside its node. A single correct field does not establish that the whole proof is complete: require a terminal overall grade, visible proof stages, and terminal grades for its select fields. A `No Credit` history proof may lack individual field grades; its controls are complete only when all stages are visible and every select has its original disabled frame and multiple captured choices. This establishes the control layout, not the correct answers. Bind that context to the matching history question only.

Before handing off the capture, run the same authoritative answer-evidence validation used by Database Preparation. If validation fails, request one focused final review with the specific gap and captured source. Check returned quotations against the question's own worked solution and choices. Save the judgment with its source-evidence hash; reuse an unchanged finding on resume. A still-unsupported answer receives an explicit unavailable finding, while the activity continues. A confirmed-looking solver status alone does not establish Math Academy's answer.

Revalidate saved answer evidence against the current question and exact typed choices during finalization. A new checked interpretation of the worked solution may replace an older interpreted answer, even if the older quotation remains present in a premise. Preserve explicit Math Academy answer keys, correctly bound successful grades, and original graphic filename facts ahead of prose interpretation. Keep original evidence and disagreements in the archive.

During response entry, a worked-solution answer may describe a mathematical value differently from the literal dropdown choice. If source-preferred entry cannot match that value, use the solver's exact current typed choice only when it explicitly reports no disagreement, the value/type match uniquely, and its supplied option agrees. Preserve the original judgment and evidence; this selects a live response without establishing a database answer fact. Explicit source keys, correct grades, disagreements, and ambiguous or stale choices retain their existing handling.

Record which source sections each extraction read and which section produced each failure. A successful reread can clear a resolved extraction error for the same question while keeping the original error, source paths, and recovery evidence in `extraction_error_history`. A prompt or solution failure must not label otherwise complete answer controls as incomplete. Preserve authored source errors and failures in sections the reread did not recover. A history page with the same verified question ID and matching problem can supplement the source text while retaining previously captured controls; missing history controls do not establish a grade for a live submission.

### Default actions when something goes wrong

| Situation | Default action |
|---|---|
| The solver is uncertain, fails, or stops responding | Python requests focused reconsideration or replaces it using saved evidence. During a timed activity, submit the best available valid response before the deadline; finish the agent's judgment during history review. |
| A question is genuinely ambiguous or unanswerable | The agent chooses the best supported valid response, or an offered Don't Know/skip when no answer is defensible. If skipping is unavailable, submit its best attempt. Record the uncertainty and continue. |
| The agent disagrees with Math Academy | Check the mathematics and source evidence now. Use the response needed to advance, including Math Academy's expected response when required. Preserve both conclusions and override the planned C/W response when necessary. |
| A field, page, or submission behaves unexpectedly | Save the current evidence, reread the page, and check what was accepted. Python requests a focused agent interpretation when needed, then retries the appropriate action on the same activity. |
| Source content or images cannot be recovered | Try the saved evidence and available source pages. The agent makes a final finding of what is supported and what is unavailable; preserve that finding and continue without inventing content. |
| The site or connection is unavailable | Save progress and retry automatically with backoff. Resume the same activity when access returns; do not abandon it or ask Jake to resolve its questions. |

Each recovery attempt must obtain new evidence, change the attempted action, or wait for an unavailable dependency. Repeating the same unsuccessful reasoning indefinitely is not progress. A final finding of ambiguity or missing evidence is recorded for this capture; new evidence in a future capture can revise it.

For completed historical captures, [source recovery](../scripts/recovery.py) can re-extract saved HTML and rerun final review without replaying the activity. Archive the original package and hashes first, resolve any outstanding database request before preparing a replacement, and leave account checkpoints, XP accounting, retake policies, and original observation times intact. Apply only to completed, inactive captures. Requeue only the affected import through Database Commit, and preserve capture-only status. Saved or freshly read history without answer controls cannot justify restoring field types or choices inferred by an old manual import.

Bind a recovered record to its checked stable source DOM root before retiring matching extraction failures; conflicting saved/source IDs refuse recovery, and generic diagnostic containers remain unbound. Recovery cache versions include the recovery and Markdown-normalization code; a changed version only invalidates memoization for explicitly reprocessed captures and never enqueues other captures.

Repeated browser failures start with a 30-second recovery wait, increase by 30 seconds per failure to a 180-second cap, and add up to 5 seconds of jitter. Save failure counts across re-observation and restart; seeing the same accepted question does not prove that a failed Continue succeeded. Repeated entry or continuation failures receive focused reconsideration or a reload, followed by a fresh observation before another action.

After completion, three HTTP 5xx failures of the supplemental lesson topic page preserve an incomplete lesson definition with the failed source evidence and allow question review to finish. Save the failure count across restarts. The final source-recovery pass can reread that page, but does not restart the retry budget. Authentication failures, rate limits, and uncertain learner submissions retain their normal recovery rules.

HTTP 429 responses, including asynchronous requests, save an account-wide cooldown using `Retry-After` seconds or its HTTP date. Resume that cooldown after a restart and reconcile uncertain submissions with the server before retrying. Temporary solver capacity failures allow up to two retries with 30–60 second waits within the request budget, preserving the session where possible. These waits do not abandon the pinned activity or turn a timed-out action into permission to submit twice.

## 3.2. Lesson

The answer policies below describe the default `capture` profile. The nine
learning profiles instead use the per-KP probability curve for lessons, reviews,
multisteps, and assessments, including retakes. Diagnostics keep the policy in
section 3.5 for every profile. Profile rates, exposure accounting, and account
configuration are documented in [Answer profiles](../scripts/README.md#answer-profiles).

A lesson teaches one topic through tutorials and knowledge points. Each knowledge point has a canonical example followed by adaptive practice questions.

**Answer policy:** Independently choose `CWCWC` with 70% probability or `WCWCC` with 30% probability for each knowledge point. Keep that choice on resume. After those five questions, answer any additional questions correctly until Math Academy advances. A retake following a negative-XP completion uses all-correct answers throughout.

1. Capture each tutorial's title, body, images, and source ID. Capture each canonical example's title, problem, worked solution, images, and `e-N` ID, and pass it to the sub-agent before the associated practice.
2. Capture and answer the practice questions, retaining their knowledge-point association and every revealed result. Follow Math Academy's completion state even when it serves fewer questions or ends the lesson unsuccessfully.
3. At completion, save Math Academy's displayed base-XP denominator and its source evidence: for “8 of 13 XP,” save 13 as the base. Preserve the first two distinct practice questions per knowledge point in presentation order, with their problems, answer fields, and worked solutions completed from history.
4. After history review, capture `/topics/<topic-id>` for the complete lesson: tutorial and example content, verified placement/content IDs, titles, and order, including sections this attempt did not visit. Database Preparation compares that definition with the existing lesson and preserves existing identities when updating it.

Lesson steps point to tutorials and knowledge points. Served practice questions join the knowledge point's pool, rather than becoming permanent lesson steps. Failed lessons and retakes share the definition but retain separate attempt evidence.

**Topic difficulty:** Python checks these inputs during the final lesson review and recovers missing source content here. Database Preparation then applies the [existing workload formula](../../reference/xp-docs/expected-distribution-base-xp.md): expected 1.6 difficulty weighting on per-KP solution measurements, followed by `topic/difficulty = observed base XP / unrounded workload score`, including the seven-XP minimum handling. Save the inputs and formula version with this derived value. An incomplete lesson does not produce a calibrated multiplier.

## 3.3. Review

A review serves practice questions from a topic's knowledge points, usually without presenting their canonical examples first.

**Answer policy:** Choose `CWCWC` with 70% probability or `WCWCC` with 30% probability once for the whole review. Continue the sequence across knowledge points and repeat it if Math Academy serves more than five questions. A retake following a negative-XP completion uses all-correct answers.

1. Capture each question before answering, then save its grade and worked solution before continuing. Preserve any instructional content Math Academy does show.
2. Continue until Math Academy completes the review. Save the actual question order and outcome.
3. Use history to confirm each question's topic, knowledge point, difficulty, and answer evidence. Keep the served order as attempt evidence; it does not define a fixed question sequence for every review.

## 3.4. Assessment

An assessment presents a fixed set of questions under a time limit. It may span several topics. The whole assessment is submitted together, so question grades and worked solutions arrive afterward.

**Answer policy:** Independently choose C with **87.17%** probability or W with **12.83%** probability per question, including retakes. Save the draw and response before entry. For W, use a different choice or an incorrect entered value; make only one field wrong. The probabilities do not guarantee a final score.

1. Save the instructions before starting. Use the question count and time limit already recorded by Queue Processing, and track the remaining time during the activity.
2. Capture and fill every question using the shared process. Save the entered answers before submitting the whole assessment. As time runs short, use the best available responses and submit before the timer expires.
3. Confirm completion, then expand every history question to collect grades, worked solutions, correct-answer evidence, difficulty, and topic/knowledge-point references. Preserve timeout or unanswered questions if they occur.

For an assessment started by capture, save the start time before clicking Start; when the time limit and question count are known, also save the absolute deadline and question schedule. Spread the sampled 70–85% target across the question count; preserve that schedule on resume. Use observed remaining time when initial timing details are missing. An already running assessment uses its observed remaining time without inventing a new full-duration schedule. Wait for the question navigator and initial question rendering, and save the full initial question DOM before entering answers; record any readiness failures.

Use the earliest saved or observed deadline. Minute-only countdown labels use their conservative lower bound. Recheck the visible timer during longer pacing waits and check the deadline again after solving and before entry or submission. Optional pacing leaves 15 seconds per remaining question and a final submission reserve of 5% of the time limit, bounded to 15–60 seconds. Divide the remaining solver budget among unanswered questions. When the reserve is reached, submit the whole assessment with the responses already entered and finish unanswered questions' judgments from history. Record the timing deviation and actual outcome. A restart never grants extra assessment time.

## 3.5. Diagnostic

A diagnostic adapts to answers and skips to determine placement. It has an observed path rather than a fixed question list known in advance.

### Before starting

1. Read and save the course's complete topic list, with IDs and titles, through `course/units → unit/modules → module/topics`.
2. Read the prerequisite graph. For each prerequisite topic, find the shortest directed path to any topic in the course. `topic/next` points from a prerequisite to the topic that requires it: one edge means a direct prerequisite.
3. Save the course topic list, prerequisite distances, instructions, and policy with the activity. Reuse them when resuming.

If the database is unavailable, use the latest saved course-topic and prerequisite snapshot and record which snapshot was used. Missing topic or graph information uses the unknown-topic response below; it must not stop the diagnostic.

### Answer policy and timing

| Question's topic | Intended response | Time from question appearing to submission |
|---|---|---|
| In the course | Independently choose 50% correct or 50% Don't Know | Correct: random 4½–6 minutes. Don't Know: immediate. |
| Direct prerequisite of a course topic: 1 edge | Correct | Random 1½–2 minutes |
| Prerequisite 2 edges from the closest course topic | Correct | Random 1–1½ minutes |
| Prerequisite 3 or more edges from the closest course topic | Correct | Random 30–60 seconds |

Check course membership first: a topic in the course keeps the 50/50 policy even if it is also a prerequisite of another course topic. An unknown topic or one with no path to the course is not a distant prerequisite; capture it, record the uncertainty, and choose Don't Know.

Draw each correct-answer delay uniformly within its range. Capture and solving time count toward that delay; wait only for the remaining time. If solving takes longer, submit when ready. **Don't Know has no deliberate wait** after capturing and classifying the question. Save the response decision, sampled delay, and question start time so resuming does not redraw or restart the wait.

The shared 500 ms browser latency and readiness checks still apply to diagnostics, including Don't Know. The ordinary 5–12 second answer pacing adds no extra delay here. For an offered retry after an intended correct prerequisite response, accept at most one consecutive retry; otherwise decline it. Save the choice for that offer so repeated observations or restarts cannot toggle it. Wait for a new numbered question or completion after the retry screen closes before continuing.

### Capture sequence

1. Capture every question, including all answer fields, choices, and images, before answering or choosing Don't Know. Save its numbered position when a source question ID is unavailable.
2. Identify its topic from an existing source-question association when available. Otherwise, have the same sub-agent match it against the saved course and prerequisite topics. Use the graph's recorded distance for timing.
3. Apply the policy above. Record the matched topic, distance, chosen action, timing, any offered retry, feedback, and next question presented. Continue until Math Academy ends the diagnostic.
4. Capture the results and history. Match numbered positions to the revealed `q-N` IDs and collect topic/knowledge-point references, difficulty, and worked solutions, including for skipped questions where provided.

Record the branches observed without inventing unvisited routes. A diagnostic worked solution remains part of its question; it does not become a canonical example.

## 3.6. Multistep

A multistep is one problem with shared setup and ordered parts. In the current schema mapping, an assignment activity contains a step referencing an assigned problem, which references the reusable multistep. The multistep owns its part steps, which reference reusable questions.

**Answer policy:** Aim for every part correct. Use the same sub-agent conversation for the whole problem, including shared context, earlier parts, and their confirmed answers.

1. Capture the source problem ID, title, instructions, shared setup, diagrams, and part order. Keep shared context available as each part is presented, including any additions revealed later.
2. Capture and answer each part in order, including all answer fields. Save its grade and explanation before continuing. Keep the original part statement separate from the shared context and earlier answers supplied to the sub-agent.
3. After the final part and history review, confirm the complete part sequence and collect each question's difficulty, topic/knowledge-point references, and answer evidence. Database Preparation stores shared setup in `multistep/context` and part order through `multistep/first-step` and `step/next`.
