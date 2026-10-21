# Course Academy workload and completion forecasting PRD

Status: implementation handoff  
Prepared for: Jake and Codex  
Date: October 21, 2026  
Primary application evidence: estimate-forecast.md, especially sections 3–13 and Appendices B–D

## 1 Product decision

Build a read-only forecasting feature that answers four questions for MTH 255, MTH 256, MTH 341, and their combined workload:

1. How much selected learning work remains?
2. How quickly is that work being completed, and how much additional work has actually entered the selected scope?
3. When would the selected work finish under the learner's recent study pattern and stated future-demand assumptions?
4. What learning pace and active study time would a chosen target date require?

The first release should use an auditable stock-and-flow model with empirical learning progress. It should reproduce the Targets graph exactly, measure actual active time, account for partial lessons consistently, and keep historical growth distinct from forecast assumptions about future demand.

Use an all-in effective learning-progress rate for the initial forecast. Reviews, quizzes, failed attempts, assignments, and other recorded study already consume time in that rate. Do not add a second generic overhead allowance.

Add an explicit engine-backed time simulation after the measurement foundation is verified. That later model is needed for materially changed review behavior, assessment eligibility, unusual repair backlogs, retention readiness, and validated probability estimates. A more elaborate simulation does not resolve missing syllabus or release information.

The attached handoff supplies implementation behavior and an inventory at a historical database basis. It does not supply measured recent base-XP pace, historical arrivals, remaining lesson XP, or a completion forecast. Application facts below are grounded in that handoff [H]. The architecture, defaults, formulas, and rollout decisions in this PRD specify the proposed feature.

### Release boundaries

| Capability | Initial release | Later engine simulation |
|---|---|---|
| Exact current graph scope and course allocation | Required | Reused |
| Remaining lesson inventory with partial and unknown states | Required | Refined residual durations |
| Seven-day and longer-window study metrics | Required | Reused |
| Historical filtered arrivals and reconciliation | Required when retained history supports them | Reused |
| Completion of the currently selected learning work | Conditional deterministic estimate | Model-based distribution |
| Catch-up with continuing additions | Explicit continuation or sensitivity scenario | Novel-root arrival simulation |
| Required pace and minutes by a selected date | Capacity estimate under stated assumptions | Schedule and eligibility aware estimate |
| Assignment preparation | Shared-work deadline capacity check | Full simulated readiness check |
| Retention readiness for an exam | Show current state separately | Supported only with an explicit readiness criterion |
| Probability of meeting a date | Unavailable in the initial release | Model-based, with validation evidence |

Do not implement a single unlabeled “completion date” that conflates these goals.

## 2 Completion events and units

### Completion events

**Current selected work complete** means that every first-acquisition obligation selected at the forecast origin is satisfied. Freeze that topic set for this forecast. A later target deletion is a withdrawal from a new forecast, not successful completion of an obligation in the saved forecast.

**Caught up under continuing additions** means the modeled unfinished acquisition backlog reaches zero under the specified arrival process. Report the horizon over which that process is assumed to apply. A first empty backlog does not mean no new work will arrive afterward.

**Prepared for assignments through a date** means all required preparation obligations supporting those assignments have been satisfied under the selected criterion. Current-scope exclusions and unmapped assignments can prevent a complete claim. Completing a homework activity and preparing its covered topics are separate events.

**Retention ready** requires a separately named criterion at the target time, such as the engine's operational readiness predicate plus no outstanding required repairs for the relevant topics. The engine's memory score is not a calibrated probability of recalling material or passing an exam [H, sections 6, 8].

### Units and metric names

Keep the following distinct in storage, API fields, calculations, and labels:

| Quantity | Meaning |
|---|---|
| Finished-attempt base XP | Sum of frozen bases of finalized attempts, with failed attempts separately identified |
| Earned XP | Actual awards, including bonuses and penalties |
| Successful acquisition XP | First-learning credit awarded once per qualifying acquired topic |
| Estimated lesson progress XP | Base-equivalent planning credit, including valid completed-stage credit on active lessons |
| Estimated remaining lesson XP | Full lesson base less that planning credit |
| Active seconds or minutes | Measured working intervals, excluding pauses and post-submission waits |
| Calendar-day exposure | Observed local civil days, with partial days explicitly handled |
| FIRe speed | Retention-update multiplier; never time productivity |

Base XP is an application workload scale. A catalog conversion of one base XP to approximately one estimated minute does not establish that the learner personally completes one XP per active minute [H, section 7].

Use explicit conversions between base XP and estimated progress XP. Do not allow earned XP into the acquisition demand equation. Monetary-style integer precision is unnecessary for derived partial credit; retain adequate numeric precision and round only for display.

## 3 Starting evidence and runtime inputs

At the handoff's basis 5382, captured on October 21, 2026, the reproducible scope was all three courses, Queue on, All weeks, upstream depth 2, and displayed L30 or higher [H, Appendix B].

| Course track | Visible topics | Unique target or queue roots | Prerequisite-only topics |
|---|---:|---:|---:|
| MTH 255 | 198 | 92 | 106 |
| MTH 256 | 156 | 57 | 99 |
| MTH 341 | 133 | 56 | 77 |
| Portfolio | 487 | 205 | 282 |

These are graph counts. Do not convert 487 into 487 unfinished lessons or subtract only the explicit learned and legacy-repetition counts to infer remaining work.

All mapped topics of the learner's linked assignments were already targets at that basis. The latest linked due dates were December 3 for MTH 255, October 20 for MTH 256, and October 21 for MTH 341. This shows uneven known schedule coverage. It does not establish that later demand is absent in the latter two courses [H, Appendix B].

At runtime:

- Read actual course identities and current titles from the captured database.
- Take the scope descriptor directly from the Targets graph controls.
- Capture one immutable database value and one forecast clock.
- Keep deadline, requested confidence, and future daily availability nullable.
- Do not infer a deadline from the last imported assignment.
- Do not treat the daily earned-XP goal or the FIRe ranking horizon as a future time commitment.

Use America/Los_Angeles for user-facing dates, calendar boundaries, and assignment weeks. Store instants in UTC.

## 4 Exact scope projection

Define a pure, versioned operation:

~~~text
project_scope(database_value, scope_descriptor)
  -> visible_topics
  -> selected_roots and root-source flags
  -> prerequisite distances and visible edges
  -> exactly one display track per topic
  -> all supported courses, roots, assignments, and deadlines
  -> inclusion and placement explanations
~~~

It must implement the existing graph behavior, including its unusual cases [H, section 5]:

1. Compute longest-path layers on the full prerequisite DAG. Displayed L30 means internal layer at least 29. Detect cycles as data errors.
2. Filter target roots using the actual course, week, and unassigned-target rules.
3. Queue roots bypass course and assignment-week filters when Queue is enabled.
4. Use all known curriculum and linked-assignment associations to decide whether a target is unassigned.
5. With all three course switches enabled, retain all valid saved targets subject to the layer cutoff, as the UI does.
6. Expand incoming prerequisite edges using shortest distance from any retained root, retaining distances 0, 1, and 2. Skip excluded low-layer prerequisites during expansion.
7. Do not apply the course filter again to supporting prerequisites.
8. Deduplicate roots, prerequisites, target/queue overlap, shared paths, and diamonds.
9. Apply the existing targetCourseBands algorithm exactly. Hidden saved roots still influence its balancing counts; full-graph distances and numeric entity-ID tie ordering matter.
10. Keep assignment support and deadlines in addition to the single display track.

Stable UUIDs identify physical topics across projections. Preserve database lineage and original numeric entity IDs as well, because the existing placement algorithm uses numeric IDs for tie ordering.

### Scope implementation strategy

First isolate the existing UI scope and placement functions as a pure reference with reproducible fixtures. Implement the native read-only projection used by forecasting and require differential parity against that reference. Prefer moving the graph to consume the same projection once parity is established. Do not introduce a browser process or a second database implementation into production forecasting.

If separate UI and server implementations temporarily remain, use a common scope version, a shared fixture corpus, and differential tests as a release gate. A change to filtering or placement must update both projections before shipping.

### Historical scope semantics

For historical growth, use:

~~~text
S_k = F_v(database_as_of_logical_T_k, fixed_scope_descriptor)
~~~

F_v is the selected current scope algorithm version. Label this “historical growth under the selected scope rules.” It is a backcast of current selection rules over historically available facts, not a claim about what an older UI displayed.

Use historical topology, memberships, curriculum associations, assignment mappings, prices, and progress when available. If current topology must substitute for missing historical topology, return a current_topology_backcast quality flag. Do not silently label it exact.

Resolve a relative week selection to absolute Los Angeles dates when the request is captured. Keep those dates fixed during the historical calculation. A moving “this week” filter creates calendar-window churn that is not target-arrival growth. The broad three-course forecast should visibly use All weeks.

## 5 Remaining work and partial lessons

### Work-state projection

Return separate fields for acquisition state, retention state, mandatory obligations, and blockers. These are independent axes; a learned topic can also be overdue or require repair.

Acquisition classifications should include:

- Satisfied by explicit learned state.
- Satisfied by qualifying historical completion evidence.
- Satisfied for preparation by legacy evidence or known-ancestor inference.
- Unstarted acquisition remaining.
- Active partial acquisition.
- Unresolved evidence.

Use the engine's known-topic and preparation semantics instead of creating a second mastery rule. Positive legacy repetitions with no learned flag are different from an explicit learned=false record. A known ancestor can need no new preparation lesson while lacking a complete retention record. Preserve that evidence source [H, section 6].

Satisfaction of an inventory obligation does not by itself establish newly performed work. Only actual qualifying dated learning or authored-stage events contribute to acquisition productivity. If learning one descendant makes several ancestors known for preparation, record the ancestors' removed residual work as preparation inference relief, separately from the direct lesson's progress. Initialization and recovered old evidence are corrections. These distinctions must be selected from provenance, not inferred from a change in the learned flag alone.

Track blockers independently: missing or ambiguous lesson, missing price, insufficient fresh question supply, deferred practice, retry gate, and missing mapping. An unknown or blocked obligation remains in the inventory.

### Lesson valuation

For topic i, choose one actual lesson route and a versioned base B_i:

- Active attempt: prefer its frozen learner-task/xp-base.
- Unstarted work: use the existing activity_base calculation, including the authoritative stored expected duration when present.
- Historical work: use the base actually available at that historical state.
- Alternate or missing lesson definitions: return a resolution problem; do not sum all alternatives.
- Unknown base: return null with a reason, plus counts and known subtotals.

Do not recover a missing base by reversing an earned-XP bonus. Treat changed content, changed base estimates, and changed formula versions as revaluation, not learning or arrival [H, section 7].

The fitted service rate and current backlog must use a compatible valuation scale. After a material formula-wide or calibration change, use a comparable historical suffix or explicitly re-express derived progress on a validated scale available at the forecast origin. Preserve original frozen attempt bases in historical factual displays. Merely separating revaluation in the ledger does not make a rate measured on an old scale comparable to a newly scaled backlog.

### Partial credit

Let P_i be valid planning credit in the same base-equivalent scale as B_i:

~~~text
0 <= P_i <= B_i
remaining_i = B_i - P_i
portfolio_remaining = sum(remaining_i for i in selected_scope)
~~~

Rules:

- Unstarted: P_i = 0.
- Acquisition satisfied: P_i = B_i.
- Active: credit completed authored stages that the engine's resume state confirms will not have to be repeated.
- Deferred KP practice remains outstanding. Visiting later stages does not complete it.
- An unfinished KP receives no speculative within-KP credit in the initial release.
- A failed or restarted attempt loses credit for stages that must actually be repeated.
- Required relearning after prior acquisition is a separate repair obligation, not a second first acquisition.

Weight completed stages using complete, credible step/expected-seconds, or additive stage contributions exposed by the existing content estimator. Normalize those weights once to the applicable B_i. The normalization must respect the lesson route and avoid counting a KP's expanded content twice.

If reliable stage weights or resume state cannot be reconstructed, use an explicitly conservative whole-unfinished-lesson point estimate and expose a partial-work range. Apply the same whole-completion accounting method to historical service. Never silently combine fractional backlog with an incompatible completion-only rate.

Partial credit is an effort estimate, not evidence of fractional mastery. Actual elapsed minutes and earned XP do not determine P_i.

### Matching the service estimator

Where valuation, scope, and preparation coverage are stable, net direct lesson progress in a window is:

~~~text
progress_W = successful_completion_credit_W
             + active_partial_credit_at_end
             - active_partial_credit_at_start
~~~

Scope entry/exit, inference relief, revaluation, retrospective corrections, and track changes require ledger adjustments; they are excluded from this service term. In particular, partial credit disappearing because an obligation becomes inference-covered must not become a negative work event. Use the cause-classified ledger as the authoritative service total; the boundary formula is a reconciliation shortcut after those adjustments.

Honor current known-ancestor coverage in the opening inventory. The initial projection does not extrapolate additional future inference relief as if it were performed XP. Record any relief when it actually occurs and reduce the next forecast's inventory. This is an explicit conservative modeling choice, not a guaranteed statistical bound. The later engine model can predict this state transition.

Illustration only: a 100-base-XP lesson that enters a window with 40 credited units and finishes in the window contributes 100 + 0 - 40 = 60 progress units. It does not contribute 100 newly performed units.

A discarded partial attempt can produce negative net progress. Preserve that setback. Its time also remains in measured study time. A completed failed attempt can contribute to finished-attempt base XP while contributing no successful acquisition.

## 6 Temporal ledger and reconciliation

Build a derived ledger from native EDB history or transaction logs. A since view is insufficient for complete addition/retraction history. Use logical transaction order; retain recorded time, original event time when known, source, and provenance. Repeated source assertions do not necessarily create a new membership transition [H, sections 3, 11].

### Ledger fields

~~~text
logical_T
recorded_at
original_event_at_if_known
evidence_available_at
source and import_batch_if_known
topic_uuid, original_eid, database_lineage
event_kind and cause
scope_before, scope_after
track_before, track_after
base_before, base_after
partial_credit_before, partial_credit_after
remaining_before, remaining_after
root_source_flags and supported_obligations
quality_flags
~~~

Event kinds include initial_inventory, scope_entry, scope_exit, acquisition_progress, progress_reset, preparation_inference_relief, estimate_revision, evidence_correction, category_transition, and track_transfer. Inference relief is signed so a reversal can restore an obligation without pretending a new target arrived. Keep mandatory repairs in a related obligation ledger.

Distinguish a first observed scope entry from reactivation of an earlier withdrawn unfinished obligation. Reactivation adds its residual work back to the active scope, without creating a second physical first-learning obligation.

### Accounting identity

For each interval, require:

~~~text
ending_remaining =
    opening_remaining
  + residual_work_entering_scope
  - residual_work_withdrawn
  - net_acquisition_progress
  - preparation_inference_relief
  + estimate_revaluation
  + evidence_corrections
~~~

Per-course reconciliation also includes transfer_in minus transfer_out. Portfolio transfer totals must be zero.

A prerequisite becoming a target is a category transition. A target already visible through another root contributes no new physical lesson. A learned topic entering the graph increases the graph count but adds zero acquisition work.

For additive category subtotals use selected target first, otherwise selected queue, otherwise supporting prerequisite. Preserve overlapping raw membership flags and the UI's overlapping category readouts separately.

### Atomic transactions

A transaction can change work state, membership, and prices together. Use this explicit accounting convention:

1. Apply qualifying progress, inference relief, and evidence corrections to previously scoped topics at their previous valuations and old tracks, preserving each cause separately.
2. Apply scope exits at the remaining value after those changes, withdrawing them from their old tracks.
3. Apply scope entries at their post-transaction residual value directly in their new tracks.
4. Revalue continuing obligations, initially attributing the adjustment to their old tracks.
5. Only for topics present both before and after the transaction, record a track transfer of their final residual value when placement changes.

This is an attribution convention, not an assertion of causal order inside a transaction. It makes simultaneous completion and target removal count as completion plus withdrawal of zero residual work. A topic imported as already completed enters with zero residual acquisition demand.

Classify recovered historical evidence as a correction when it becomes known. Do not present a backfill of an old completion as learning newly performed on the import date.

Compute reconciliation using unrounded values. Any unexplained difference is a data-quality failure rather than an invisible balancing adjustment.

## 7 Historical growth through the forecast cutoff

The requested historical measure is residual work entering the filtered scope per observed calendar day. Report graph-topic counts as a separate measure.

~~~text
historical_daily_added_XP = sum(residual_scope_entries) / observed_day_exposure
historical_weekly_added_XP = 7 * historical_daily_added_XP
historical_weekly_added_topics = 7 * sum(gross_scope_entry_count) / exposure
~~~

Also report gross withdrawals, acquisition progress, revaluation, transfers, and net backlog change. Net backlog change is not an arrival rate.

### Observation window decision

Use a comparable recent window anchored to local dates:

- Default start: midnight 28 local dates before the forecast date, shortened to the beginning of reliable comparable history when necessary.
- End: the forecast clock, including only the elapsed portion of today.
- Publish a comparison using the complete dates in that interval.
- Offer 7-day and 56-day historical views when available.
- Show the exact interval, exposure, observed dates, gaps, and history mode.

These are product defaults, not claims that four weeks guarantees a reliable growth model. A known migration, tracking interruption, or materially incompatible estimation regime can shorten the eligible contiguous window; surface the reason.

Define exposure as the sum of observed fractions of local civil dates. A fully observed DST date counts as one calendar day even if it has 23 or 25 hours. For a partial date, divide observed seconds by that date's actual duration. Unknown periods are not zero-growth exposure.

Use Sunday–Saturday bins for the weekly growth chart. Show the current week as a partial subtotal with elapsed exposure. Derive the combined rate from total additions divided by total exposure, not an unweighted mean of separately scaled partial-week rates. Never include future dates or future weeks in either the numerator or denominator.

### Imports and initial inventory

When retained history begins with a bulk population of an existing backlog, record that transaction as opening inventory. Do not assume all of that demand originated on the import day.

Later batch imports remain observed operational additions. Report their contribution separately and show sensitivity to their inclusion in a continuation scenario. Do not silently delete them to obtain a smoother rate.

Keep two clocks distinct:

- Operational growth: when scope membership became recorded and visible.
- Academic arrival: when new academic work was actually released, if independently known.

Assignment due dates are deadlines. They cannot substitute for release dates. A due-week proxy may be offered as a separately named exploratory view, restricted to elapsed evidence, but must not drive the default arrival forecast.

## 8 Measuring study pace and productivity

### Recent pace

Use the seven completed local dates before today for the headline recent pace. Show today separately as in progress. Also calculate a 28-complete-date comparison, shortened and labeled when coverage is incomplete.

For a common window with D observed calendar days and M observed active minutes:

~~~text
active_minutes_per_day = M / D
finished_base_XP_per_day = sum(valid_finalized_attempt_bases) / D
earned_XP_per_day = sum(valid_final_awards) / D
successful_acquisition_XP_per_day = unique_completion_credit / D

effective_progress_per_day = net_modeled_lesson_progress / D
effective_progress_per_active_minute = net_modeled_lesson_progress / M
~~~

The modeled-progress numerator contains direct qualifying work and valid partial-stage changes, not inferred ancestor coverage or initialization. Calendar-day progress requires complete dated progress and boundary-state coverage. Progress per minute additionally requires jointly reliable progress and timing coverage. Use a jointly observed comparable interval, or mark that ratio unavailable; never divide a full progress numerator by a known-time subtotal. A calendar-day completion estimate can remain available when missing time prevents a required-minutes estimate.

The default forecast uses the comparable 28-day effective-progress estimate. The seven-day estimate is displayed and used as a recency sensitivity. If recent behavior has a documented change, use the comparable suffix and display its shorter coverage rather than silently blending incompatible periods.

Show failed-attempt and activity-type breakdowns for finished-base metrics. Use ratios of totals, not an average of daily productivity ratios.

For additive time shares, assign each physical activity occurrence one primary purpose. A remediation review is not charged once as repair and again as an ordinary review. Activity type and purpose can both be reported, but totals must reconcile to measured active time.

### Capacity domain

For the initial all-in forecast, the denominator is all observed Course Academy active time for this learner in the same window. The numerator is selected-scope learning progress under the historical scope rules.

This measures progress toward the selected work per minute of the learner's observed overall study pattern. It includes recorded homework that earns no XP, outside-scope study, quizzes, reviews, failed attempts, and pauses in acquisition caused by those activities. It is not a pure measure of mathematical ability or lesson-solving speed.

Label required time as “active study minutes under your current study mix.” Unrecorded off-platform work cannot be inferred. A future dedicated-focus scenario that changes this mix needs an explicit alternative model.

### Timing rules

Reuse the application's ownership and timing semantics [H, section 7]:

- Reconstruct active item intervals, split at local midnight, and truncate at working-ended-at when applicable.
- Sum item durations or the authoritative task aggregate, never both.
- Count real instructional reading even without an answer.
- Include time on unfinished attempts.
- Preserve imported duration checkpoints without adding them again to reconstructed intervals.
- Use recovered original finish time for dated outcomes.
- Exclude undated imported outcomes from dated rates; retain them in lifetime totals.
- Keep unknown durations and unknown dates missing.
- Include genuinely observed zero-study days.
- Exclude processing waits after submission from active work.

Keep a separate matched-task diagnostic:

~~~text
matched_finished_base_XP_per_hour =
    sum(bases of matched finalized tasks)
    / sum(full known active hours of those same tasks)
~~~

This is a completed-task cohort statistic, not daily acquisition capacity. Long-running unfinished attempts must remain visible so a fast-completer selection effect is apparent.

The existing study-stats endpoint reports earned XP, not daily base XP. Extend or reuse its timing projection; do not rename its earned-XP field [H, sections 7, 11].

## 9 Future arrivals and preloaded commitments

Store separate outputs for historical_recorded_growth and future_novel_demand. The first is measured; the second is a forecasting assumption or fitted model.

### Initial release scenarios

| Scenario | Future demand assumption | Result label |
|---|---|---|
| Current selected work | No additional unknown obligations enter this frozen goal | Current work completion |
| Comparable novel additions continue | A supported rate of genuinely new residual obligations continues over a stated horizon | Conditional catch-up estimate |
| Demand sensitivity | An explicit range of novel additions is supplied or explored | Scenario results |
| Content constrained | Blocked work becomes available only under a stated release assumption | Conditional or unresolved completion |

The absence of a future-demand estimate is not zero. The current-work scenario deliberately assumes no additional work for its defined goal; it does not claim the remaining semester has no new work.

A topic already in today's target/queue closure is already included in opening inventory. Its future assignment due date introduces no additional acquisition demand. A topic already acquired introduces no new first-learning demand, although review or repair can still be needed.

If ordinary recorded additions include preloading of distant assignments, do not automatically interpret their average as the rate of unseen future academic work. Display schedule-coverage gaps and an insufficient_evidence status for unseen academic demand where appropriate.

Do not set the continuation parameter g automatically equal to the gross historical scope-entry rate. That statistic can include reactivation, mapping churn, and preloading. Derive a comparable novel-obligation rate, or model reactivation together with withdrawal. If the data cannot support that separation, retain the historical statistic and offer an explicitly chosen rate-sensitivity scenario. The initial aggregate model must not recharge known physical topics by treating every past re-entry as a new future lesson.

### Later novel-root model

With sufficient evidence, sample new root events or assignment-release batches, apply the same scope projection, and calculate marginal residual workload against the already-known and already-acquired state.

Do not independently sample target XP, queue XP, and prerequisite XP and sum them. Overlap and prerequisite sharing make those components dependent. Scope re-entry, syllabus mapping changes, and genuinely new roots should remain separate event types.

Cap demand by a known finite curriculum only when curriculum completeness is actually established. Otherwise use an explicit modeling horizon and sensitivity cases. An indefinite constant rate is not a semester model.

## 10 Initial forecast equations

### Preconditions and interpretation

A finite whole-goal date requires an applicable estimate for every remaining acquisition obligation and a modeled resolution of each binding availability blocker. Otherwise return unknown_cost or blocked with a null whole-goal date. A known-and-available-subset date can be shown separately. A conditional whole-goal date must name an actual resolution assumption, such as immediate supply availability or a supplied release date.

First check whether the acquisition goal is actually satisfied, with no unknown remaining obligations. If so, report complete_at_forecast_origin and already_caught_up even when recent progress is zero. Future arrivals can still create a new backlog; repair and retention readiness remain separate. An estimated zero subtotal alone does not prove the goal is satisfied.

The closed forms below are capacity diagnostics under unconstrained, constant-rate assumptions. Displayed per-course and portfolio planning dates come from the joint projection in section 11 when order or availability matters. Do not let an aggregate ratio override a later feasible date or a blocker reported by that projection.

Let:

- R0 = estimated remaining selected lesson XP.
- s = net effective progress per calendar day.
- v = net effective progress per active minute.
- M(H) = future active minutes available through horizon H.
- G(H) = additional residual acquisition work under a specified future-arrival scenario.

The cumulative capacity condition is:

~~~text
v * M(H) >= R0 + G(H)
~~~

For constant daily pace and no additions:

~~~text
T_current = R0 / s
~~~

For constant daily additions g:

~~~text
T_catchup = R0 / (s - g), only when s > g
~~~

For a positive remaining backlog, if s is nonpositive, return insufficient_positive_progress. If s <= g, return no_finite_catchup_under_constant_rates. Do not clip the denominator.

That result describes the constant-rate approximation. It does not prove the learner can never finish a finite course or never temporarily clear a stochastic backlog.

### Required pace by a chosen date

For a horizon of H calendar days:

~~~text
required_progress_per_day = (R0 + G(H)) / H
required_active_minutes_per_day = (R0 + G(H)) / (H * v)
~~~

If there are K planned study days, also report required minutes per study day:

~~~text
required_minutes_per_study_day = (R0 + G(H)) / (K * v)
~~~

For a weekday schedule, use the actual cumulative availability instead of dividing equally across all days. Allocate only the remaining availability of today; do not count its already-observed study time twice.

If v is unavailable or nonpositive, return an unavailable required-time result rather than dividing by zero or a negative rate. If K is zero, the selected study schedule has no capacity. A completed acquisition goal needs zero additional acquisition time, while any separate readiness obligations retain their own status.

A date-only target means the end of that local civil date. A timestamp target retains its exact instant. H must be positive. The requested confidence remains null unless a supported probability model and a user-selected level exist.

These equations assume similar productivity and activity mix as time increases. A recommended study budget far outside the observed range must carry an extrapolation flag.

### Worked arithmetic illustration

These are hypothetical values, not Jake's measurements:

~~~text
R0 = 600 estimated lesson XP
s = 40 progress XP/day
g = 10 new residual XP/day

Current work: 600 / 40 = 15 days
Continuing additions: 600 / (40 - 10) = 20 days

For a 12-day horizon:
required progress = (600 + 10*12) / 12 = 60 XP/day

If v = 0.5 progress XP/active minute:
required time = 60 / 0.5 = 120 active minutes/day
~~~

The net margin s - g should be visible. Near zero, small rate changes create very large date changes.

## 11 Per-course forecasts and deadlines

Maintain three relationships:

1. One physical first-learning obligation per topic.
2. One graph display track per visible topic.
3. Any number of supported course and assignment obligations.

Display-track totals must sum to the portfolio. Deadline demand uses unions of physical obligations across all supported assignments, even when a prerequisite is drawn in a different track.

### One shared capacity budget

Use a single joint daily projection for all courses. Do not give every course the full portfolio pace.

First report each course's observed direct progress per calendar day, using the same complete interval and event-time tracks. These contributions sum to portfolio progress. Zero observed course progress can mean no recent allocation; it is not evidence of inability.

For the continuation of measured course progress, use those measured progress contributions to allocate the one service budget when they are usable and nonnegative. A course with no usable positive rate has an unavailable date under an unchanged-allocation claim. Do not turn a large share of failed lesson time into an equally large predicted share of successful progress.

Provide a separate pooled-productivity planning scenario for redistributing time:

1. Estimate allocation shares from direct first-learning attempt minutes on topics in the reconstructed selected scope at the time of that work, including failed attempts and using event-time tracks. Outside-scope study stays in the all-in productivity denominator but not in these within-scope shares.
2. Apply one pooled effective productivity v to the shared budget and allocate it using the stated time shares. This explicitly assumes similar effective productivity across courses; it is not a measurement of each course's speed.
3. Within a track, order physical work by earliest supported deadline and stable prerequisite/priority tie rules.
4. Reallocate unused capacity when a track has no available work to remaining available work, earliest supported deadline first.
5. Freeze existing topics' display allocation at the forecast origin for interpreting course dates. Record the allocation used for each genuinely new arrival.

Report the allocation evidence and reallocation rule. If no selected-scope allocation history exists, a demand-proportional allocation may be used only as a labeled planning assumption. If any course has negative net progress or inadequate comparable evidence, the pooled plan remains a scenario rather than a measured continuation for that course. Per-course matched productivity can replace pooling once it is supported, while retaining one total time budget.

Use known prerequisite and availability constraints where the projection can establish them. Do not infer full engine feasibility from the visible depth-2 graph. Unresolved required work outside the selected graph is a condition on the forecast.

Each course's date is the date its allocated obligations finish in this joint run. The portfolio date is the date all selected physical obligations finish. Shared obligations are performed once and can satisfy several deadlines.

### Deadline capacity checks

For every deadline checkpoint d, form the union U(d) of unfinished physical preparation work supporting assignments due by d.

~~~text
required_capacity_by_d >= sum(residual_work_i for i in U(d))
~~~

Compare it with cumulative modeled service by d. A failed inequality proves insufficient capacity under that scenario. Passing all inequalities is necessary but not sufficient when availability, prerequisites, session lengths, repairs, or assessment eligibility constrain the order.

Show overdue unsatisfied obligations separately. Do not erase them or invent a future due date.

If the selected graph excludes relevant prerequisites or the assignment has unmapped problems, return incomplete_preparation_scope. Offer a separate named expanded-scope scenario later; do not silently change the graph-matching headline inventory.

For required-time inversion, search a shared availability multiplier through the joint deterministic projection. The simple aggregate formula is the initial capacity estimate; earlier deadlines can require a larger or differently allocated budget.

## 12 Assessment, review, and repair modeling

### Initial release

Use the all-in rate. Report historical time shares for lessons, ordinary reviews, assessments, required repairs, assignments, and other recorded study. These explain why recorded activity does or does not reduce the acquisition backlog.

Also expose the current obligation inventory:

- Required repairs and relearning, with trigger provenance.
- Pending ordinary assessment, global cadence state, and eligibility blockers.
- Active/deferred lessons and fresh-question shortages.
- Retry or age gates and earliest known eligibility times.
- Mandatory outside-scope work.
- Optional review adherence reflected in the historical period.

A new exceptional repair backlog or unresolved blocking content makes the first-release date conditional. Do not add the entire repair bill on top of the all-in rate without separating the typical historical burden it replaces.

### Later explicit-time model

Predict active minutes by individual physical activity occurrences. Every occurrence is charged once. Assign one primary purpose for additive reporting; scope and course support are additional tags.

Possible primary purposes are acquisition attempt, required repair practice, ordinary review, ordinary assessment, retake, and assignment/other work. A task can satisfy several obligations without duplicating its duration. Outside-scope work is a tag, not another cost added to the same task.

Use empirical duration models by activity, authored stage, and difficulty features where evidence permits. Preserve incomplete attempts as censored observations or state-conditioned residuals. Do not estimate remaining time by subtracting elapsed time from a catalog mean.

Replay deterministic engine transitions on isolated state. Fit stochastic outcomes and durations to actual learner evidence; the engine's retention memory and FIRe speed do not supply those probabilities or time multipliers.

### Exact assessment behavior to preserve

The handoff establishes [H, section 8]:

- One learner-wide earned-practice-XP cadence.
- Ordinary assessment availability at 120 and required status at 150 when eligible.
- At least five eligible never-assessed topics, explicitly learned with successful learning at least 48 hours earlier, plus fresh usable questions.
- Ordinary assessment completion/expiry resets the relevant cadence; retakes follow different reset semantics.
- Assessment awards do not increment ordinary practice cadence.
- Negative awards, overshoot, and current counter position matter.
- Actual assembled duration determines base XP; the maximum 15-minute wall-clock limit is not an invariant 15-XP or 15-active-minute cost.
- Expiry can create repairs for unanswered assigned questions without fabricating incorrect-answer FIRe evidence.

Reuse lifecycle and sampling logic. Allocate the one global quiz across its actual sampled topics for reporting; never instantiate one quiz per course.

### Exact review and repair behavior to preserve

Use full persisted progress and policy state. Simulate repeated review arrivals, not only reviews due now or the first next-due date. Include newly acquired topics and implicit credit through encompassing relationships.

Use an explicit optional-review adherence policy. Required remediation remains distinct from optional ordinary reviews and optional retakes. Deduplicate physical repair practice that satisfies several originating obligations.

Known-ancestor preparation coverage does not establish operational retention state. Missing legacy state should produce unknown retention readiness rather than invented memory values.

### Event loop outline

~~~text
capture immutable database and clock
project scope, lesson obligations, deadlines, current engine state
fit parameters only from evidence available at the cutoff

for each modeled scenario or simulation path:
    clone state without a live writer
    initialize active tasks, cadence, repairs, supply, and known commitments

    advance to the next study session or relevant event:
        apply known releases and sampled novel root arrivals
        recompute marginal scoped demand and support relationships
        update engine time-dependent state
        select available work under the declared study policy
        sample remaining active duration and outcomes
        apply deterministic engine transitions to the clone
        charge each physical activity occurrence once
        update acquisition, repairs, reviews, cadence, and question supply
        record deadline satisfaction and completion events

    retain completed, blocked, and horizon-censored outcomes
~~~

Do not call mutating task preparation or submission paths against the live learner to explore hypothetical work. A copied state may use pure calculation or local simulated plans; it must not possess a live writer capability.

## 13 Uncertainty and validation

### Initial release uncertainty

Use scenario results, not claimed confidence intervals. Seven-day versus 28-day pace, alternative demand assumptions, partial-work bounds, and supply assumptions form sensitivity views. Their extrema are not automatically statistical lower and upper bounds.

Return an explicit uncertainty kind:

~~~text
unavailable
scenario_range
model_based_unvalidated
empirically_evaluated_predictive
~~~

Keep nominal probability level nullable. Identify the actual scenario behind each date. Do not invent an 80%, 90%, or 95% confidence preference.

Later, preserve dependence between availability, productivity, course allocation, and arrivals. Resampling consecutive daily or weekly vectors can preserve some observed dependence when there are enough comparable periods. It is not reliable merely because thousands of synthetic runs can be generated [S3].

Do not discard non-finishing paths before computing probabilities or quantiles. Distinguish no finite catch-up under a constant-rate scenario, not finished within the simulated horizon, and unresolved content blockers. Simulation sample size reduces Monte Carlo error, not missing-data or model error.

### Backtesting design

Use rolling historical forecast origins. At every origin reconstruct the information actually available then, fit only preceding observations, freeze the requested goal, and evaluate only after the target horizon has elapsed. Chronological and multi-step forecast evaluation are established approaches [S1].

Keep corrected-history analyses separate from genuine as-known-at-the-time backtests. A later import carrying an older original finish date was not available to an earlier forecast. Prospective saved forecast snapshots are especially useful when retrospective code or data reconstruction is incomplete.

Score residual work and learning progress in the forecast-origin valuation scale, or a fixed comparable scale available at that origin. Track later repricing and evidence corrections separately unless explicitly modeled. Do not count a changed price formula as acquisition or forecast error.

Evaluate frozen-scope completion separately from evolving-scope growth. Do not score a forecast as successful just because targets were later withdrawn.

| Prediction | Evaluation |
|---|---|
| Remaining work and progress | MAE and signed bias in estimated lesson XP |
| Active time | MAE and bias in minutes, with activity and course breakdowns |
| New marginal demand | Count/XP MAE, bias, and import-batch decomposition |
| Completion by a resolved deadline | Brier loss for probabilities |
| Quantiles and intervals | Quantile loss, empirical coverage, interval width/score |
| Product usefulness | Comparison with fixed-backlog and constant-rate baselines |

Proper probability and interval scoring evaluates truthful uncertainty and penalizes inappropriate precision [S2]. Avoid percentage errors for series containing zeros.

Publish the number of evaluated origins, fully elapsed horizons, distinct weeks, missing outcomes, and observed coverage. Overlapping forecast origins are dependent. A large number of overlapping windows does not create a large independent sample.

A complex model should become the default only if it improves relevant out-of-sample results or resolves a necessary feature the baseline cannot support. Preserve the baseline as an audit comparison.

## 14 Proposed input and output contract

The API is a read-only computation. A proposed POST /api/forecast accepts an explicit scope and scenario configuration; it must not prepare activities or write learner facts. Exact route naming can follow repository conventions.

### Request

~~~json
{
  "scope": {
    "courseCodes": ["MTH 255", "MTH 256", "MTH 341"],
    "includeQueue": true,
    "weekSelection": {"kind": "all"},
    "prerequisiteDepth": 2,
    "minimumDisplayedLayer": 30,
    "courseAssignmentPolicy": "current-targetCourseBands"
  },
  "goal": "current_selected_acquisition",
  "targetLocalDate": null,
  "requestedProbability": null,
  "futureAvailability": null,
  "history": {
    "preferredCompleteDays": 28,
    "includeElapsedTodayForGrowth": true,
    "recentPaceCompleteDays": 7
  },
  "scenario": {
    "arrivalMode": "known_commitments",
    "allocationMode": "measured_progress_continuation",
    "reviewBehavior": "continue_observed_mix"
  }
}
~~~

The server resolves learner ownership and course IDs, captures the basis and clock, normalizes relative dates, and returns them. Do not trust a client-supplied numeric entity ID without lineage and ownership validation.

For the changing-scope catch-up scenario, require a supported arrival model or explicit scenario parameter. For a date inversion, require a target date. Missing future availability is acceptable for an “at recent pace” forecast or a required-time calculation.

The alternative allocation mode pooled_productivity_plan enables the explicitly labeled redistribution scenario. Never silently substitute it when measured course continuation is unsupported.

### Response groups

~~~text
manifest:
  captured_basis, lineage, forecast_clock, timezone
  scope_descriptor, scope_version, scope_hash
  valuation_version, model_version, policy_fingerprints
  historical_window, exposure, completeness, assumptions

inventory:
  visible_topic_count, root_count, prerequisite_only_count
  acquisition_satisfied_by_evidence_type
  unstarted_count, active_partial_count
  known_remaining_XP, unknown_price_count, partial_estimate_bounds
  required_repairs, pending_assessment, content_and_supply_blockers
  per_course_track_totals
  per_assignment_support_and_deadline_coverage

pace:
  seven_complete_dates, longer_complete_window, today_partial
  active_minutes, finalized_base_XP, earned_XP
  successful_acquisition_XP, net_estimated_progress_XP
  per_day_rates, effective_progress_per_active_minute
  matched_task_productivity, activity_time_shares, quality_flags

growth:
  gross_scope_entries_and_exits
  required_residual_XP_entering_and_withdrawn
  direct_progress, preparation_inference_relief, revaluation, evidence_corrections, transfers
  exposure_normalized_weekly_rates
  weekly_bins_with_partial_flags
  ordinary_edits_vs_batch_imports_vs_initial_inventory
  unseen_demand_status

forecast:
  goal, model_kind, scenario, status
  portfolio_completion_date_or_null
  per_course_dates_from_joint_projection
  net_progress_margin
  deadline_capacity_checks
  required_progress_and_active_minutes_or_null
  observed_allocation_shares_and_reallocation_policy
  uncertainty_kind, probability_or_null, validation_summary
  binding_blockers_and_main_drivers
~~~

Every metric should carry unit, status, method, window or basis, and coverage. Useful statuses include estimated, measured, partial, missing_history, unknown_cost, blocked, conditional, insufficient_positive_progress, no_finite_catchup_under_constant_rates, and unsupported_goal.

Return unknown counts alongside known subtotals. Do not represent unavailable totals as zero. Do not represent infinity as an ordinary JSON number or convert it into a remote date.

## 15 Read-only extraction and implementation map

The graph endpoint alone is insufficient. Fetch complete relevant history and retain pagination and completeness evidence [H, section 11].

| Projection | Required evidence | Existing implementation anchors |
|---|---|---|
| Scope and associations | Full DAG, memberships, full course associations, linked coverage, deadlines | Math-Academy-Graph-Explorer.html; target-weeks.js; graph_explorer_reader.rs |
| Learning obligations | Lesson identity/base, known ancestry, current resume state, blockers | learning.rs; activities.rs; base_xp.rs; inventory.rs |
| Timing and dated outcomes | Owned tasks/items, original finish times, status intervals, submission cutoffs, checkpoints | timing.rs; study_stats.rs; activity_history.rs |
| Historical additions | As-of snapshots and additions/retractions of every scope input | Native EDB read helpers and history/log access |
| Current required overhead | Repairs, retry/retake links, global cadence and eligibility | scheduling.rs; retrieval.rs; assessment_sampling.rs |
| Later retention simulation | Full progress, persisted policies, encompassing graph, supply and reservations | core.rs; calibration.rs; schema.rs; inventory.rs |

Repository paths and behavior are described in the attached handoff. Codex must inspect the current checkout before changing code; the handoff's fingerprints identify the earlier inspected sources.

Use native EDB reads through the configured reader. Do not invent a PostgreSQL relational schema. Capture one immutable value for a forecast and explicit as-of values for history. Ensure complete many-valued Pull results and all activity-history pages; existing defaults can truncate collections or return only one page [H, section 11].

Do not fetch question prose or generator source merely to compute measured pace. Read content only when uncached workload estimates or supply checks actually need it.

### Smallest useful persistence

Prefer derived projections and caches over new learner attributes.

Add only what cannot be recovered or is needed to reproduce results:

- Versioned derived work/time ledger.
- Forecast manifest and saved prediction snapshots.
- Estimate-source and quality flags.
- Import-batch classification when provenance cannot otherwise express it.
- Optional verified original release dates and schedule-completeness metadata.
- Measured generator/supply wait only if the later model requires it.

Do not add a target-added-at attribute merely to duplicate reliable retained transaction history. If history is incomplete, start prospective observations and mark the earlier interval unknown.

Cache by basis, learner, scope, valuation/model versions, and observation window. Time-dependent retention and open active intervals also depend on the forecast clock; invalidate or explicitly parameterize them. Avoid replaying the entire database on every UI filter change.

## 16 User interface requirements

Add a Forecast panel adjacent to or reachable from the Targets graph. Its scope summary should show enabled courses, Queue, week filter, depth, and layer cutoff. Changing those controls changes the forecast and its historical projection consistently.

The main view should contain:

1. Remaining selected learning work, including known XP, partial lessons, unknown costs, and blockers.
2. Recent seven-day study time and learning progress, plus the longer-window comparison.
3. Historical weekly additions, with observed coverage and partial-week labeling.
4. Current-work completion and the separately named continuing-additions scenario.
5. A target-date control that computes required progress and active minutes.
6. Per-course rows derived from the shared projection and capacity budget.
7. Assignment deadline capacity checks and schedule-coverage gaps.

Use an expandable explanation showing the opening workload, measured pace, arrival assumption, and binding constraints. Keep internal schema fields and implementation details out of the main user flow.

Suggested labels:

- “487 topics in this graph” for the audited fixture, not “487 lessons left.”
- “Estimated remaining lesson XP.”
- “Learning progress per calendar day.”
- “New work added per observed week.”
- “Current work completion.”
- “Catch-up if additions continue.”
- “Conditional on resolving 2 content blockers” when such a runtime count exists.
- “Future demand is not yet known” when coverage is insufficient.

The count examples are fixture or illustrative labels, not values to hard-code into the live interface.

Show what a selected date means. Do not label acquisition completion as exam readiness. Show unavailable results with the specific missing evidence that would make them calculable.

## 17 Delivery sequence for Codex

### Stage 1 Scope and inventory

Deliver the pure scope contract, UI-reference fixtures, native projection, current acquisition inventory, evidence classifications, partial-state projection, and unknown/blocker reporting.

Exit gate: exact scope and course-allocation parity, plus one physical obligation per topic. The historical census is a fixture only when its original captured data and matching source version are available.

### Stage 2 Measurement and historical accounting

Deliver complete read-only extraction, time and outcome provenance, recent metrics, historical state projection, residual-arrival ledger, and reconciliation.

Exit gate: stock changes reconcile; durations and study dates match application semantics; no future observations enter a historical rate. Missing history produces an explicit partial capability rather than fabricated metrics.

### Stage 3 Initial forecast and interface

Deliver current-work and continuing-additions scenarios, one shared course-capacity projection, target-date inversion, deadline capacity checks, explanation UI, and exportable manifests.

Exit gate: compatible units; no overhead double count; unresolved inputs produce correct states; all-in conditional acquisition claims remain distinct from operational/retention readiness.

Stages 1–3 constitute the initial useful release.

### Stage 4 Engine-backed readiness

Add isolated engine state replay, explicit activity durations, assessment cadence, repeated reviews, repairs, supply/eligibility constraints, and selectable behavior scenarios.

Exit gate: deterministic transitions match the actual engine, physical time is charged once, no live writes occur, and the model addresses a demonstrated weakness of the baseline.

### Stage 5 Probabilistic forecasting

Add empirically supported joint duration/outcome/arrival uncertainty, saved prospective forecasts, resolved-horizon validation, and probability-based target-time inversion.

Exit gate: uncertainty labels match their evidence; non-finishing paths remain in the results; validation is reported against the simple baseline. A large simulation count is not a substitute for observed history.

## 18 Acceptance criteria

### Scope and identity

- L29 is excluded and L30 retained using full-DAG layers.
- Depth 2 uses shortest upstream distance.
- Diamonds, shared prerequisites, and target/queue overlap produce one physical topic.
- Queue, unassigned-target, All-courses, week, and hidden-root placement rules match the UI.
- Every selected topic has exactly one display track.
- Pure track reassignment changes no portfolio workload.
- Historical identities use stable UUIDs while placement retains original EID ordering and lineage.
- The basis-5382 fixture gives 487 visible topics and 205 roots only when the matching input is supplied.

### Work and timing

- A learned topic entering scope contributes zero new first-acquisition work.
- Known-ancestor and legacy evidence are distinguished from complete retention readiness.
- Completing one descendant can retire inferred ancestor obligations, while measured successful-acquisition XP credits only qualifying work actually performed.
- A completed failed attempt consumes time without becoming a successful acquisition.
- A 100-XP lesson with 40 pre-window partial units contributes 60 units when completed.
- Deferred KP practice remains unfinished after later stages have been visited.
- Failed partial-credit loss is a progress reset, not target growth.
- Content repricing and evidence backfills are not learning.
- Item and task time cannot be counted together.
- Imported durations and reconstructed intervals cannot be counted twice.
- Unknown import dates do not become original study dates.
- Homework without XP remains real recorded time.
- Unknown or blocked cost is never silently zero.
- A full-goal date is null when required costs or binding blocker resolutions are unmodeled; a subset date is labeled separately.
- Complete progress with incomplete time can support a per-day rate but never an inflated progress-per-minute ratio.
- Current backlog and fitted service use compatible valuation scales.

### Growth and forecasting

- New targets already in the closure add no duplicate physical lesson.
- A prerequisite-to-target transition is not new work.
- Reactivating withdrawn unfinished work restores residual scope demand without duplicating the obligation.
- A future due date of an already-loaded topic contributes zero new acquisition demand.
- Initial population, later imports, ordinary additions, withdrawals, and corrections are separable.
- Future weeks never enter the historical average or denominator.
- Observed zero-growth/zero-study dates count; unknown dates do not become zeros.
- DST and partial civil dates have explicit exposure semantics.
- Frozen date-range filters do not move during historical reconstruction.
- Reconciliation holds for simultaneous progress, removal, and revaluation.
- A simultaneous entry, completion, repricing, and placement change reconciles per course; only continuing topics generate track transfers.
- Earned XP is rejected as acquisition workload.
- All-in capacity and explicit overhead cannot be active simultaneously in one calculation.
- An already-satisfied goal returns completion at the forecast origin before any positive-rate check.
- A positive backlog with service at or below demand never produces a clipped finite catch-up date.
- Each course shares the one portfolio budget.
- Course time shares cannot masquerade as measured course progress shares; a pooled-productivity plan is labeled as an assumption.
- Shared deadline obligations consume physical work once.
- Target deletion does not count as completion in a saved frozen-scope forecast.
- A passing aggregate deadline inequality is not presented as proof of schedule feasibility.
- Missing future-demand evidence is distinct from the deliberate current-work scenario.
- Scenario ranges are not labeled confidence intervals.
- Blocked and horizon-censored simulation paths are not discarded.
- Retrospective corrections are unavailable to earlier as-known-at-the-time backtests.
- Backtest scoring preserves the origin valuation scale instead of treating repricing as forecast error.

These tests protect substantive accounting and forecasting behavior. Avoid tests that merely mirror implementation details.

## 19 Missing evidence in priority order

| Priority | Evidence | What it enables |
|---|---|---|
| 1 | Current lessons, known-acquisition evidence, partial state, bases, and blockers | A defensible remaining-work total |
| 2 | Complete timed attempt history with original dates and frozen bases | Seven-day pace, longer-window capacity, and time conversion |
| 3 | Retained history of all scope inputs and valuations | Actual filtered historical additions |
| 4 | Current mandatory obligations, cadence, retry and supply state | Conditions on the initial estimate and inputs for readiness |
| 5 | Release dates and syllabus/mapping completeness | Better forecasts of unseen academic demand |
| 6 | Full historical retention/policy state and matched outcome/duration evidence | Engine simulation and probabilistic refinement |

Deadline, future availability, and requested confidence are runtime inputs. Their absence does not block implementing the measurement layer or an at-recent-pace current-work forecast.

## 20 Codex handoff instructions

Implement Stages 1–3 first, using this PRD together with estimate-forecast.md.

Before coding, verify current source behavior and extract a read-only data-completeness report. Resolve technical mismatches in favor of the actual application behavior and update the scope/version manifest. Preserve the graph's existing semantics.

Keep measurements, assumptions, and conditional results distinct. Build the accounting ledger before the forecast formulas. Use the simple baseline as a permanent regression and explanation tool.

Do not fill missing evidence with zero, infer workload from topic counts, infer historical arrivals from future due dates, or add overhead twice. If a requested metric is not supported by the available evidence, return its explicit reason and complete the supported parts.

The initial release is successful when Jake can see what selected work remains, what measured progress and additions mean, what assumptions produce a completion date, and what active study time a chosen date would require.

## Sources

**[H]** estimate-forecast.md, “Pace, workload growth, and completion forecasting: technical handoff,” prepared October 21, 2026. Application evidence: sections 3–13; census and schedule coverage: Appendix B; policy defaults: Appendix C; reproduction fingerprints: Appendix D. The document is the application-specific source for this PRD and should accompany it in the Codex handoff.

**[S1]** Hyndman, R. J., and Athanasopoulos, G. Forecasting: Principles and Practice, time-series cross-validation section. Supports chronological rolling-origin and multi-step evaluation, not the particular observation-window defaults chosen here. [Author textbook](https://otexts.com/fpp3/toolbox.html).

**[S2]** Gneiting, T., and Raftery, A. E. (2007). Strictly Proper Scoring Rules, Prediction, and Estimation. Journal of the American Statistical Association, 102(477), 359–378. Supports probability, quantile, and interval evaluation. [Author-hosted paper](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf).

**[S3]** Politis, D. N. (2003). The Impact of Bootstrap Methods on Time Series Analysis. Statistical Science, 18(2), 219–230. Supports dependence-aware block resampling under appropriate assumptions. [Author-hosted paper](https://mathweb.ucsd.edu/~politis/StatSci03.pdf).

