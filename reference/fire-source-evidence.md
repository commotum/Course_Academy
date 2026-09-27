# FIRe: source evidence and reconstruction boundaries

Research date: 2026-09-26. This records what the supplied Math Academy references and primary public sources actually establish. It supports an independently implemented FIRe-style engine, not a claim to have recovered Math Academy's proprietary implementation or calibrated parameters.

## Sources and provenance

The detailed rule inventory below is principally an analysis of the **local, supplied references**, not evidence extracted from a deployed Math Academy account. `Proprietary.md` is an index of excerpts from the supplied book; it is not an independent corroborating source, leaked implementation, or executable specification. `Proprietary-Notes.md` contains local interpretation and should not be promoted to primary evidence.

| ID | Source | Role |
|---|---|---|
| L1 | [Supplied FIRe article](<Optimized, Individualized Spaced Repetition in Hierarchical Knowledge Structures Introducing Spaced Repetition Compression and Fractional Implicit Repetition (FIRe)/Optimized, Individualized Spaced Repetition in Hierarchical Knowledge Structures Introducing Spaced Repetition Compression and Fractional Implicit Repetition (FIRe).md>) | Article, equation, diagrams, and follow-up clarifications. |
| L2 | [Supplied book chapter 29](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md>) | Formal variable definitions, ability/difficulty estimation, graph-weight construction. |
| L3 | [Supplied book chapter 18](<The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/18-Spaced-Repetition-Distributed-Practice/18-Spaced-Repetition-Distributed-Practice.md>) | Explicit-review gate for slow student-topic learning speeds; learning-speed diagram. |
| L4 | [Proprietary reference index](Proprietary.md) | FAQ extracts, especially source lines 146–161, 177–188, and 297–305 reproduced near the end of the file. |
| W1 | [Justin Skycak, FIRe article](https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/), dated 2023-10-05 | Current public page checked against L1. It explicitly describes the implementation as proprietary. The equations, speed gate, and surrounding explanation agree with the local copy. |
| W2 | [Math Academy, How Our AI Works](https://www.mathacademy.com/how-our-ai-works) | Public product explanation; sections “The Spaced Repetition Algorithm,” “How the Task Selection Algorithm Chooses Topics to Review,” and “How the Algorithms Adapt to Pace of Learning.” |
| W3 | [Skycak, Scraping Bits Podcast #107](https://www.justinmath.com/scraping-bits-podcast-107/) | Author-hosted transcript; paragraphs beginning “The review questions…” and “It's a kind of fuzzy space repetition…” give useful credit examples. Transcript is grammar-cleaned, not a formal specification. |
| W4 | [Skycak, Spaced Repetition 2.0: Accounting For and Discouraging Reference Reliance](https://www.justinmath.com/the-vision-for-version-2-of-math-academys-spaced-repetition-system/), dated 2025-10-22 | Version boundary: accuracy is described as the current signal; reference reliance and timing are described as future signals. This is a roadmap statement, not proof that those additions have shipped by the research date. |
| W5 | [Skycak, Cognitive Science of Learning: Spaced Repetition](https://www.justinmath.com/cognitive-science-of-learning-spaced-repetition/), dated 2024-02-18 | Confirms qualitative spacing principles and individual calibration; no missing implementation functions recovered. |
| W6 | [The Math Academy Way PDF](https://www.justinmath.com/files/the-math-academy-way.pdf) and [book index](https://www.justinmath.com/books/) | Search-indexed PDF passages confirm the speed gate and recurrence. Direct browser-text retrieval of the 20.8 MB PDF failed, so this research does not claim a complete read of its current revision. Local chapters were read directly. |
| W7 | [Math Academy Podcast #6, Part 3](https://www.justinmath.com/math-academy-podcast-6-part-3/), dated 2026-01-28, 21:33–23:42; [linked official video](https://www.youtube.com/watch?v=4iMh_KQkoZc&t=1293s) | Newer detail: separate assessment and non-assessment accuracy estimates are averaged; both global and per-topic accuracy estimates exist. Video URL was resolved from the author's page, but video retrieval failed; the transcript supplied the evidence. |
| W8 | [Math Academy Podcast #1](https://www.justinmath.com/math-academy-podcast-1/), dated 2025-10-30, 1:47:28 onward; [linked official video](https://www.youtube.com/watch?v=oUhToWZn6rI&t=6448s) | Discussion with founder Jason Roberts corroborates the planned status of reference-reliance integration in October 2025. |

## Published mechanics

**Confidence labels:** “explicit” means stated in a supplied primary reference; “illustrative” means an example/diagram, not a universal parameter; “inferred” means a reasonable engineering interpretation; “unknown” means no authoritative definition was found.

| Mechanic | Evidence and confidence | Implementation consequence |
|---|---|---|
| Prerequisites and encompassings are distinct | **Explicit.** L1 follow-up discussion; L2 “Setting Encompassing Weights.” A prerequisite may supply only conceptual familiarity and receive zero repetition credit. | Never assign review credit solely because a prerequisite path exists. Keep separate relations. |
| Positive propagation | **Explicit.** L2 “Concrete Example” and “Visualizing Repetition Flow.” Successful advanced work credits encompassed component skills through multiple graph layers. | Traverse advanced-to-component encompassings. An implementation may orient stored edges in this direction even though the book's diagrams draw prerequisite-style arrows upwards. |
| Negative propagation | **Explicit.** Same sections. Failed simple work penalizes advanced skills encompassing it; flow may cross multiple layers. | Traverse the reverse encompassing relation for negative evidence. Failing an advanced task does not, by itself, prove every component was failed. |
| Fractional edge weights | **Explicit.** L2 “Partial Encompassings.” A weight measures the fraction of the component topic exercised by the advanced topic; it can loosely be read as a problem-coverage probability. | Validate weights in `[0,1]`; preserve zero and partial weights; do not normalize outgoing weights to sum to one. Different components can all be fully exercised. |
| Sparse authored weights | **Explicit.** L2 “Direct and Key Prerequisites are Sufficient.” Experts author nontrivial nearby relationships that cannot be inferred; distant/default uninferred relationships are zero. | Author meaningful local edges, then compute closure. Record author/provenance and rationale. |
| Explicit correction of inferred weights | **Explicit in principle; algorithm unknown.** L2 says an explicitly set weight can correct the value inferred by repetition flow. | Support corrections, but label their precedence/closure semantics as an implementation policy. The source does not specify how a correction affects other paths. |
| Non-ancestor encompassings | **Explicit.** L2 corresponding subsection. An advanced equivalent topic can encompass a simpler equivalent topic that is not a prerequisite ancestor. | Do not require encompassing edges to be prerequisite edges. Validate the encompassing structure independently. |
| Incoming implicit-credit gate | **Explicit.** L3 “Calibrating to Individual Students and Topics,” especially lines 206–208; also L1. A target topic with student-topic speed `<1` receives no incoming implicit repetition credit and requires explicit reviews. | Gate positive implicit credit using the receiving topic's speed. Equality `1` is not below the threshold. Whether this blocks further traversal through the topic, versus only its own credit, is unspecified. |
| Student-topic speed | **Explicit.** L2 “Ratio of Student Ability and Topic Difficulty.” Speed is an ability-derived speedup divided by a difficulty-derived slowdown. | Keep speed positive and separate from raw event quality. Mapping accuracy to each factor is a policy, not recovered Math Academy code. |
| Per-topic ability evidence | **Explicit.** L2 “Measuring Student Ability at the Level of Individual Topics.” Accuracy weights recent answers more; correct answers propagate down and incorrect answers up. | Keep recency-weighted evidence per student/topic. Do not collapse it to a single global student ability. |
| Ability initialization | **Explicit inputs; unknown estimator.** L2 initializes a topic from neighboring direct/key prerequisites, encompassings, and same-module topics. | Store these relations; choose and disclose a shrinkage/neighbor estimator and fallback prior. |
| Topic difficulty | **Explicit inputs; unknown estimator.** L2 “Measuring Topic Difficulty.” Based on accuracy of serious students' assessment answers across students. | Do not estimate this from lesson attempts alone, or claim one learner's completion data identifies the population difficulty. “Serious student” selection and smoothing are unspecified. |
| Raw repetition quality | **Explicit.** L2 “High-Level Structure.” Positive for passed work, negative for failed work; magnitude grows with stronger success or worse failure. | Distinguish graded task performance from a bare completion flag. `rawDelta` can vary continuously. |
| Early discount | **Explicit direction; unknown function.** L2 says early work receives reduced magnitude when memory is high. | Discount at the receiving topic's state; preserve a configurable formula and parameters. A topic may be late while its encompassing source topic is early. |
| Overdue failure amplification | **Explicit direction; unknown function.** L2 defines `decay` as starting at 1 and increasing when the topic is severely overdue. | Use the multiplier only when `failed=1`; do not silently turn mere elapsed time into a repetition-count penalty. Memory decays even without a failure. |
| Reviews become due as memory falls | **Explicit principle; unknown number.** L2 “High-Level Structure.” | A due threshold is required but not published. Do not identify a plausible `0.5` threshold with Math Academy's actual threshold. |
| Calendar-time basis | **Explicit.** L2 defines both elapsed time and interval in days. The failure multiplier also addresses extended absence. | Use elapsed days for this reconstruction. XP is work-volume/reward metadata, not the published equation's time coordinate. Public sources do not exclude additional private scheduling heuristics. |
| Reviews require prior learning | **Explicit.** L1 clarifications; L4 baseline mastery discussion. New lessons require prerequisite mastery; review applies after baseline mastery. | Keep learned/mastered eligibility apart from transient memory. A topic with zero memory is not automatically an available new lesson or a mastered review topic. |
| Review compression | **Explicit objective, unknown optimizer.** L1 and L4. Prefer tasks that satisfy other due reviews implicitly, including new lessons; also postpone future reviews and maintain a broad frontier. | Separate state estimation from task ranking. A greedy gain/time rule is a reconstruction, not the recovered proprietary optimizer. |
| Early source review may cover due component review | **Explicit.** L4 FAQ source line 152. A newer topic can be offered before its own review is due to cover a due older topic. | Candidate selection cannot be restricted to currently due source topics. Apply the source's early discount independently from the component's. |
| Cross-course maintenance | **Explicit.** L4 FAQ source line 146. Spaced review applies across the student's learned profile. Mastery floors create an exception for assumed-mastered earlier material. | Avoid erasing review history at course boundaries; treat mastery floors as explicit policy/imported state. |
| Immediate quiz remediation | **Explicit.** L4 FAQ source line 103. W2 confirms missed quiz questions trigger immediate corresponding remedial review. | Remediation is a task-selection override; it need not wait for the ordinary memory threshold. The quiz's quantitative credit mapping remains unknown. |

## Exact published equations, and what they do not determine

L1 and L2 publish this high-level structure (variable spelling retained):

```text
repNum -> max(0, repNum + speed * decay^failed * rawDelta)
memory -> max(0, memory + rawDelta) * 0.5^(days / interval)
```

Here `repNum` is accumulated successful repetition progress, not an integer task counter; `interval` spans repetition `repNum` to `repNum+1`; `failed` is 0 or 1. The recurrence floors both values at zero. It does **not** show an upper cap on memory, so a clamp at one is an extra modeling decision. A memory value portrayed as a percentage in a diagram is insufficient evidence to alter the formula.

The displayed memory equation does not identify event-time phases. It can be read as a boost followed by future elapsed decay, but a programmer might instead apply its `days` term to elapsed time *before* the current event. Those readings produce different results. The supplied definition of `days` as time since the previous repetition does not resolve which timestamp the unprimed `memory` represents.

A coherent event-driven interpretation is to store post-event memory `M(t0)`, lazily calculate `M(t-)=M(t0)*2^(-(t-t0)/I)`, then apply the current event: `M(t+)=max(0,M(t-)+delta)`. It separates forgetting since the previous event from the boost occurring now. **This ordering is inferred, not an exact transcription of the displayed arrow.** A separate literal-equation helper and sensitivity mode make the distinction auditable.

Example of the difference: with previous memory `1`, elapsed time `10` days, interval `1` day, and current credit `1`, “elapsed decay then boost” gives `1.0009765625`; applying the displayed boost before that already elapsed decay gives `0.001953125`. The latter could leave a just-passed review immediately due. This demonstrates why a timestamp convention is necessary; it does not prove which internal convention Math Academy uses.

The equation does not supply `interval(repNum)`, a threshold, initial memory, the raw quality function, the early discount, the severe-overdue function, or the speed estimators. Any executable implementation must choose these. An exponential interval schedule is compatible with expanding intervals but not uniquely determined by them.

## Diagram checks

These local images were inspected directly, not inferred from filenames:

1. `math-academy-spaced-repetition-model-overview.png`: exactly reproduces the equations and variable descriptions. It adds no event-ordering convention, numerical due threshold, or hidden parameter table.
2. `integration-by-parts-partial-encompassing-weights.png`: integration by parts is linked to polynomial, exponential, and trigonometric integration with weights `1`, `0.5`, and `0.2`. Their sum is `1.7`, confirming that weights are independent coverage fractions rather than a normalized probability distribution over components. These are **illustrative domain weights**, not a Course Academy curriculum calibration.
3. `fractional-repetition-credit-through-partial-encompassings.png`: colored nodes fade off from a full-credit trunk. There are no numerical path values or merge annotations. It cannot establish max-product, sum-product, noisy-OR, or another aggregation rule.
4. `spaced-repetition-schedules-at-different-learning-speeds.png`: initial lessons at speeds `2` and `1` accrue `2` and `1` reps; later reviews accrue those increments. Curves visually restore to 100% and review around mid-height. That supports an illustrative initial-lesson seed and changing interval length, not an exact memory cap or threshold.

## Reconverging paths and explicit corrections

The sources establish multihop attenuation, preservation through full encompassings, and expert corrections. They do not give a path-composition or path-merge equation. Multiplying edge weights is a natural attenuation model, but even that remains an inference.

For a diamond with `A -> B -> D` and `A -> C -> D`, if each route has product `0.4`, plausible merges yield different credit: maximum `0.4`, capped sum `0.8`, independent noisy-OR `0.64`. The paths may represent overlapping practice, so independence or disjointness cannot be assumed from the graph alone. Plain path summation can also award multiple full repetitions for a single fully overlapping event.

A conservative reconstruction can use maximum path product, count each source event once at each destination, and let an explicitly authored source/destination weight replace inferred weight, including an explicit zero. **All three are declared engineering choices.** The local statement about correcting inferred values supports a correction mechanism, but it does not establish zero-override behavior or whether an intermediate correction must alter descendant inference. Store enough provenance to revise that choice.

Likewise, disabling credit at a slow target does not establish that the target is a graph barrier. Computing graph coverage first and applying each receiver's gate afterwards is a coherent choice. Applying the same attenuation in reverse for negative flow is plausible, but the public examples do not identify a separate penalty-weight function or prove exact symmetry.

## Additional primary findings beyond the local extracts

W3 supplies illustrative repetition magnitudes: a barely passed review may earn half a repetition or less, while a perfect review may earn around one and a half. It then describes multiplying performance credit by learning speed. These examples corroborate noninteger credit and make a universal upper bound of one inappropriate; they do not identify the actual accuracy-to-credit function. The same transcript describes replacing stored repetition records with a model that computes a student's knowledge profile dynamically, which supports retaining replayable evidence as an architectural approach.

W4 describes accuracy as the then-current input and reference reliance and timing as planned additions. Thus collecting hint/reference/timing telemetry is sensible, but a reconstruction using those signals must label their effects as its own extensions unless newer implementation evidence is obtained. Diagnostic timing is separately discussed in W2; that does not prove identical timing treatment inside FIRe.

W2 independently confirms task-quality-dependent credit, the distinction between prerequisites and actual practice coverage, explicit reviews for challenging topics, and task selection that uses new lessons or reviews to cover due component reviews. It supplies no exact merge rule, decay function, speed transform, or memory threshold.

W7 adds a relevant detail absent from the supplied chapter: maintain assessment and non-assessment accuracy separately, then average their estimates. Pooling all answers would let the more numerous lesson/review answers overwhelm quiz evidence. It also describes both aggregate and per-topic accuracy, with graph propagation. The exact recency kernel, missing-channel prior, averaging weights, and relationship between global and local estimates remain unspecified. A single pooled EMA should therefore be labeled a simplification; a channel-balanced estimator is better supported.

Follow-up searches specifically sought an SRS 2.0 launch through 2026-09-26, including the official product site, author posts/podcasts, and official social-account search results. No primary launch confirmation was found. W8 still speaks of future implementation; the June 2026 podcast concerns school onboarding and supplies no release confirmation. The correct status is **deployment unverified**, not “definitely unshipped” and not “already deployed.”

## Conflicts and cautions resolved

- **Gate omitted in chapter 29:** omission is not a contradiction. Chapter 18 explicitly contains the `<1` gate, and L1 agrees.
- **“Review phase” versus new lessons:** the follow-up says implicit knockouts occur after prerequisite mastery. It does not mean new lessons cannot review previously learned component topics; the compression examples explicitly use new lessons to do so.
- **“Review B itself” in the A-prerequisite-of-B safeguard:** L1 has a likely variable-name slip when describing which topic receives explicit fallback review. Its surrounding explanation says not to leave a due component unreviewed while waiting for an implicit opportunity. Do not encode the apparent slip as a new propagation rule.
- **One due review at a time versus dynamic menus:** L4 says tasks are recomputed dynamically and lessons can be interleaved with outstanding reviews. “Do not wait indefinitely for compression” does not specify a rigid all-due-reviews-first queue.
- **0.5 in the equation versus a 50% pass requirement:** `0.5` is the exponential decay base. It is not a stated review pass score, due threshold, or target quiz accuracy.
- **Time measurement versus forgetting clock:** response duration, earned XP, elapsed calendar days, and task-completion time are distinct quantities. The published memory equation uses days. W4 discusses response timing as another possible evidence signal.
- **Performance benefit:** the references describe Math Academy outcomes and theoretical efficiency; they do not validate this independently chosen parameterization on Course Academy learners.

## Search coverage and remaining unknowns

Primary searches covered JustinMath's FIRe article, spaced-repetition article, book index/current indexed PDF, author-hosted podcast transcripts, roadmap post, and Math Academy's own product/AI explanation. Targeted queries included `rawDelta`, memory ordering, implicit credit plus maximum/sum/paths, calendar/XP spacing, code/GitHub, inventor name, and Math Academy on Google Patents. No authoritative public FIRe model implementation or matching FIRe patent was found. Public graph-rendering code was subsequently recovered, as described below. Search absence is not proof that a model implementation or patent does not exist. Unaffiliated repositories and commercial implementations surfaced, but were excluded as evidence of Math Academy internals.

Outstanding numerical and structural unknowns:

- Interval family/parameters, interpolation at fractional `repNum`, interval floors/caps.
- Memory threshold, memory initialization, update timestamps/order, saturation behavior, timestamp handling for implicit events.
- Accuracy-to-quality map, task pass threshold, treatment of quiz questions versus multi-question tasks, lesson seed credit.
- Early-discount shape and whether every negative case is discounted identically.
- Overdue-failure multiplier and re-teaching trigger.
- Ability recency kernel, priors, neighborhood estimator, difficulty cohort selection/smoothing, transforms to speed, speed bounds, and whether an event uses old or updated speed.
- Path product, reconvergent aggregation, correction precedence, negative-flow attenuation, gate traversal, cycles, and multiple direct topics in one event.
- Compression optimizer, cost model, lookahead horizon, broad-frontier/interference tradeoffs, exact remediation overrides.

An honest engine should expose these choices in versioned configuration, log per-topic effects for each observation, preserve raw evidence for replay, and test invariant behavior separately from claims of empirical calibration. The defensible claim is: **the implementation instantiates the published FIRe structure with documented reconstruction policies.**

## Saved artifacts and public client investigation

A read-only inspection of `/home/jake/Developer/MA` and `/home/jake/Developer/study` looked for actual model outputs beyond the reference documents. No standalone `/home/jake/Developer/ECE` directory exists; the relevant ECE implementation is under `MA/PIPELINE/Electrical-and-Computer-Engineering`. Exact searches for `repNum`, `rawDelta`, `learningSpeed`, student-topic speed, fractional implicit repetition, or encompassing-weight declarations in source/data files found no FIRe implementation or exported numeric learner state. Ordinary occurrences of “encompass” in lesson prose were not algorithm evidence. The ECE prerequisite-generation script explicitly excludes encompassing edges from its output (for example, `3-Wire-Graph/1-Prerequisite-Identification/prerequisites.py`, around line 1374).

The saved graph captures do contain a weaker form of state evidence:

- `MA/COURSES/Math-Academy/**/SOURCE-*/Graph-*.html`: 31 SVG captures, 6,627 topic-node occurrences covering 2,590 distinct topic IDs. Node titles identify topics, and ellipses carry seven colors: gray `rgb(242,242,242)` and six blue shades. Example: `MA/COURSES/Math-Academy/University/Calculus-I/SOURCE-Calculus-I/Graph-Calculus-I.html`.
- Some `TOC-*.html` captures also contain per-topic color circles and module progress bars. Example: the corresponding `TOC-Calculus-I.html`, around lines 891–903.
- There are 217 topic IDs with different colors in different captures. For example, topic `526` is gray in the Mathematical Foundations II capture and dark blue in the Integrated Math I Honors capture. These differences cannot be assumed to represent answer-driven learning transitions.

Capture provenance was found in `MA/PIPELINE/Math-Academy/0-Ingest/1-Course-Source/course-source.py`, especially `capture_graph_element` and `capture_course_once` around lines 1135–1194. That code switches the active course, visits the learner's `/learn` page, opens the graph through the course-percent control, and saves `#graph.outerHTML`. Its adjacent `_course_progress_state.jsonl` has 32 completed capture records spanning 2026-04-09 02:06:37–18:53:36 UTC, including recaptures. It records course context, filenames, and completion timestamps, but no student identifier. A completion timestamp is an upper bound near capture time, not an answer timestamp. The source demonstrates a learner-page workflow; it does not establish that the graph belongs to the same learner as the later task-history dataset.

These should remain **rendering observations with source-file, course, and capture context**. A compatible color mapping was recovered subsequently, but it still does not identify the continuous FIRe `repNum`, memory, due time, accuracy, speed, or an encompassing weight. Combining conflicting contexts into one numeric learner state would fabricate information.

Public JavaScript linked directly from saved lesson/course HTML was downloaded without cookies and read, never executed. No authenticated application endpoint was invoked. The inspected assets were `api.js`, `api-new.js`, `core.js`, `core-ui.js`, `question-widget.js`, `student-reference.js`, `task-event.js`, `task-event-storage.js`, `course.js`, `course-progress.js`, `header.js`, `commonFunctions.js`, and `index.js`, all under `https://mathacademy.com/js/`. Two separately fetched public graph renderers, `knowledge-graph.js` and `student-knowledge-graph.js`, yielded the evidence below. The candidate `knowledge-graph-new.js` returned 404; no authentication challenge or access restriction was bypassed.

The [public API wrapper](https://mathacademy.com/js/api.js) exposes potentially relevant read contracts, without exposing their response schemas or proving account authorization:

| Client function | Declared route | What this proves |
|---|---|---|
| `getStudentKnowledgeGraph` | `GET /api/students/{studentId}/knowledge-graph`, optional `courseId` | A learner-graph resource exists in the client vocabulary. |
| `getStudentCourseKnowledgeGraph` | `GET /api/courses/{courseIds}/students/{studentId}/knowledge-graph` | A course-context learner graph is also declared. |
| `getTaskReviewState` | `GET /api/tasks/{taskId}/review/{topicId}/state` | A review-task state resource is declared; its state may be within-task progress rather than FIRe retention. |
| `getTaskLessonState` | `GET /api/tasks/{taskId}/lessons/{topicId}/state` | A lesson-task state resource is declared. |
| `getStudentCourseProgress` | `GET /api/courses/{courseId}/students/{studentId}/progress` | Course progress is independently addressable. |

The function `submitRequestProfile` is a false lead for learner modeling: its [question-widget caller](https://mathacademy.com/js/question-widget.js) passes `requestTime`, `renderTime`, and `processingTime`, so this is request-performance telemetry. The same widget consumes answer correctness, elapsed time, and XP speed-bonus fields. Those fields do not establish a time-dependent FIRe credit function or confirm SRS 2.0 deployment. The downloaded assets contain no `repNum`, `rawDelta`, encompassing-weight, learning-speed, or retention-memory calculation.

### Recovered display mappings

The older [knowledge-graph.js](https://mathacademy.com/js/knowledge-graph.js) renderer consumes `response.topics` from `getStudentCourseKnowledgeGraph`; `getTopicStyles` uses `topic.repetition` and `topic.isFrontier`. `getRepetitionColor`, at lines 522–534 of the fetched asset, has this exact case mapping:

| RGB fill | Numeric `topic.repetition` switch case | Saved node occurrences |
|---|---:|---:|
| `210,231,249` | 1 | 105 |
| `165,207,243` | 2 | 36 |
| `120,182,237` | 3 | 127 |
| `74,158,232` | 4 | 66 |
| `29,134,226` | 5 | 71 |
| `23,107,181` | default | 1,359 |
| `242,242,242` | fallback outside that switch | 4,863 |

The default is **not an exact count or a proved `>=6` bin**: any truthy value other than numeric 1–5 reaches it, including fractional values or strings. A zero/white case exists but the caller tests repetition truthiness first. Gray can mean falsy repetition without frontier, or a nonstudent unit view. No client rounding or calculation of `topic.repetition` was found; it arrives in the response. The relationship between this display field and published continuous `repNum` is unknown.

The captured `#graph` container, zero-width node strokes, and full RGB palette strongly match this renderer. The downloaded code is dated by retrieval on September 26, whereas captures date to April 9; a historical version match has not been proved.

The other [student-knowledge-graph.js](https://mathacademy.com/js/student-knowledge-graph.js) renderer instead consumes `response.topics` from `getStudentCourseProgress`. Its fields include `live`, `learningPath`, `failCount`, `stability`, and `frontier`. For positive stability after higher-priority status checks, blue lightness is `100*(1-0.7*stability)` with hue 208 and saturation 77. Other cases render unavailable gray, learning-path yellow, failures red, and frontier green. It uses container `#knowledgeGraph` and width-3 strokes. The meaning of stability and its relation to repetition/memory are not defined there. Its formula must not be retroactively applied to legacy RGB captures.

Fetched-asset SHA-256 identities for reproducibility:

- `knowledge-graph.js`: `9faf1eee0a0ee09c7e66c4da4db791088ab44ade2af23d317631d5bb71c90c79`.
- `student-knowledge-graph.js`: `094e279fd063cc926db7a583ab6a693fe519349bd5406a0cc2ac8cd1c2a351cb`.

The strongest remaining opportunity would be a legitimately authorized learner-graph response that exposes these fields, with known learner identity, timestamps, and before/after answers. This investigation did not obtain that response or call any account endpoint. The recovered colors add snapshot constraints but provide **zero verified FIRe state transitions**.

### Subsequent authorized account inspection

The user later approved read-only access. The [live-account follow-up](fire-live-account-analysis.md)
recovered 162 result occurrences, exact topic/example links, a 360-node graph
snapshot and five offered lessons through the ordinary UI. The learner identifier
was read from the learning page's declared `studentId`. A focused navigation to
the documented own-account course knowledge-graph GET resource was blocked by
the browser with `net::ERR_BLOCKED_BY_CLIENT`; no response or numeric FIRe state
was obtained, and no workaround was attempted. Earlier statements about not
invoking account resources describe the initial public/local research phase.
