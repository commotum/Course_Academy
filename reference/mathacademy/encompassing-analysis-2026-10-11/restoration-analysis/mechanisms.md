# Diagnostic recalibration and relearning: mechanism evidence

This note separates the mechanisms Math Academy documents from the behavior implemented in Course Academy. It supplements the capture timeline; it does not independently establish the timeline's before/after counts.

## Best explanation to use

Treat a persistent large rebound after a diagnostic and relearning as **post-diagnostic revalidation of component knowledge**, separately from ordinary spaced-repetition increments. That is a better working explanation than raising the encompassing weight until a single activity produces five units of credit. “Revalidation” describes a change in the system's assessment of existing knowledge; it does not require a literal retrieval of an old stored repetition counter.

Math Academy explicitly supports two diagnostic modes: a diagnostic averaged into the existing knowledge profile, and a clean slate that wipes the profile and recalibrates it. Therefore the diagnostic boundary is a substantive state change. Course-page identity is also substantive because the published system includes course-based mastery floors. A stable topic relationship can produce very different visible effects across these states.

For short-lived rises followed by reversals, use a separate **transient displayed-state change** classification until the surrounding question outcomes and page sequence decide between reassessment and stale/asynchronous rendering. Monotone accumulation of successful completion credit is a poor explanation for repeated reversals.

## What the Math Academy sources establish

| Mechanism | Local source and lines | What it establishes |
|---|---|---|
| Diagnostic blending versus full reset | `reference/The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-XP-and-Practice-Schedules/FAQ-XP-and-Practice-Schedules.md:120` | A diagnostic can be averaged into an existing profile. A user-selected clean slate wipes the existing profile and recalibrates it. A new diagnostic alone does not tell us which mode was selected. |
| Conditional completion can be lost | Same FAQ, line 116; diagnostic chapter, lines 27–36 | Missing questions on a conditionally completed topic or its prerequisites can prune back that part of the knowledge profile. The status is deliberately sensitive to subsequent performance. |
| Diagnostic evidence directly initializes repetition credit | `reference/The Math Academy Way/V-TECHNICAL-DEEP-DIVES/30-Technical-Deep-Dive-on-Diagnostic-Exams/30-Technical-Deep-Dive-on-Diagnostic-Exams.md:54`–66 | Diagnostic answers update a signed balance; positive final balances become repetition credit. Correct but excessively slow answers receive less weight. This is a different route to repetition state from ordinary review credit. |
| Re-diagnostic can place a previously completed course lower | Same diagnostic chapter, lines 70–79 | Diagnostic placement uses a conservative edge of mastery, while lesson progression uses a more aggressive edge. Earlier completion and later lower placement are not contradictory. |
| Course-based mastery floors | `reference/The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md:77`–90 | Some lower-course topics are automatically considered mastered when taking a higher course. Course context can affect assigned mastery without a fresh full review of every topic. This does not establish which color a floor produces. |
| Ability and neighborhood initialization | Same spaced-repetition chapter, lines 111–129 | Ability is tracked per learner-topic, with correct answers propagating down and incorrect answers up. Initial accuracy uses direct prerequisites, key prerequisites, encompassings, and same-module topics. Ability can change without changing the mathematical encompassing relationship. |
| Ordinary spaced repetition | Same spaced-repetition chapter, lines 135–157 | Successful/failed raw credit changes repetition state; early practice discounts credit; quality and learning speed scale it. These equations describe ordinary retention updates, not a complete specification of diagnostic blending or display colors. |

The local `reference/xp-docs` reports independently keep diagnostics outside ordinary earned-XP formulas. `earned-xp-formula-report.md:201` states that diagnostic placement uses a separate policy. Those XP reports do not supply a restoration rule or numerical mapping from repetition state to the current progress colors.

## What our implementation actually does

| Implementation path | Behavior | Consequence for this analysis |
|---|---|---|
| `engine/rust/runtime.rs:682`–743, `place_diagnostic` | Forms signed diagnostic balances and initializes positive balances only for previously unlearned topics. Lines 732–734 skip topics already marked learned. | Our diagnostic implementation does **not** reproduce clean-slate resets or blending into already-learned state. Do not replay an MA reset through this path and then fit weights to absorb the discrepancy. |
| `engine/rust/learning.rs:1906`–1926 | Partial imported progress preserves observed repetition position but starts with zero current retention, no fabricated past answer evidence, and a new observation anchor. | Banked repetition state and established current memory are already separate concepts in our progressive API. |
| `engine/rust/learning.rs:1932`–2007 | Successful first local learning keeps the direct topic's imported repetition credit and adds the new local credit. | This is a useful architectural precedent for retaining history through revalidation. It applies to the **direct lesson topic**, not every encompassed component; it is not evidence of MA's mechanism. |
| `engine/rust/core.rs:814`–879 | Initial learning marks only the direct topic learned; a component that is not learned receives no retention update. | Our engine has no automatic “revalidate all old components and restore their prior counters” operation. |
| `engine/rust/core.rs:881`–937 | Ordinary retention applies positive or negative discounted credit and can gate positive implicit credit when target speed is below one. | Opening the gate changes whether ordinary credit arrives; by itself it does not restore five prior units. |
| `engine/rust/retrieval.rs:291`–301 | A failed review adds the topic to relearning; a later completed lesson/review clears that obligation. | Relearning scheduling is distinct from diagnostic placement and from repetition restoration. |
| `schema/learner/1-3-learner-progress.edn:1`–21 | One learner-topic state, with topics shared across course contexts. | Course-page-dependent observations must remain identified in the analysis. Our single shared learner-topic state does not implement a separate course mastery-floor display layer. |

## Ranking the explanations

For the late event, assuming the capture audit confirms both components remain low before the lesson and high for hours afterward:

1. **Post-diagnostic revalidation or recomputation of previously strong component knowledge.** It explains the diagnostic boundary, the remembered high state, the coordinated component jump, and persistence. This is the working explanation to use.
2. **Ordinary implicit practice amplified by a different learner-state or display mapping.** The lesson practices the components and could supply ordinary credit at the same time. It is a weaker explanation of a coordinated return to earlier high bands unless the target state or mapping itself changed.
3. **A delayed/stale update.** Plausible for transient reversals; less persuasive for a clean stable before/after block lasting hours. It moves up the ranking if the jump occurs broadly on unrelated topics or aligns with alternating capture surfaces.

The exact historical repetition values need not be restored for explanation 1 to be correct. A newly recomputed knowledge confidence, a course mastery rule, or blending with older evidence could yield the same visible rebound. The useful model distinction is **ordinary practice versus state reassessment**, rather than choosing one unobserved private implementation prematurely.

## Consequences for fitting weights

Keep the content-based encompassing estimate stable. Classify each observation using account, topic, course page, diagnostic epoch, ordinary practice/relearning status, earlier observed high state, and persistence. Do not join a target state across course pages merely because the topic ID matches.

Fit ordinary credit from ordinary-practice observations. Preserve reassessment events in a separate state-transition component. They establish that the advanced topic provides evidence about the component, but their full color jump is not ordinary credit magnitude. Preserve transient changes in the observation model rather than treating the disappearance of a gain as new negative encompassing evidence.

For a lightweight implementation, the classification can remain an analysis field; no schema or engine change is needed to produce the revised estimates. Useful fields are `diagnostic_epoch`, `course_id`, `event_regime`, `prior_peak_same_course`, `prior_peak_other_course`, `hours_persisted`, `snapshots_persisted`, and `cojump_topics`. The prior peaks are descriptive evidence, not an instruction to reset repetition state to the historical maximum.

There is no minimum-activity exclusion. A one-observation relationship still gets a best content-based estimate. What changes is which mechanism is allowed to explain that observation's magnitude.
