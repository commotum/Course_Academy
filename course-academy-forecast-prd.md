# Simple catch-up forecast

Show two estimated catch-up dates: **at the current seven-day average pace** and **at the daily earned-XP goal**. Catch-up means closing today's overdue/current backlog while average workload growth continues. It does not mean completing every preloaded future assignment.

Use **base XP** for work: 1 base XP is 1 estimated minute. Use actual active minutes to measure personal time efficiency. Reviews, quizzes, and failed attempts all count toward attempted base XP. No schema changes are required. The Study sidebar displays overall and per-course dates at both paces. [estimate-forecast.md](estimate-forecast.md) contains the schema and engine details.

## 1. Today's backlog

Match the Targets graph's final topic sets and course allocation: course/Queue/week filters, unassigned targets, prerequisite depth **2**, and displayed layers **L30+**. Each topic already appears once in one track. The forecast owns its projection; the graph page owns its filtering and placement code and does not import forecast modules.

Within those selections, an assignment target becomes current on its **local due date**, including everything due today even if its deadline time is later today. Queue and targets without an applicable dated assignment are standing work and remain current. Prerequisites inherit the earliest date of a root that needs them. There is no current-week approximation.

```text
L_c = unfinished lesson base XP needed through today in course track c
L   = sum_c L_c
```

Use existing engine preparation evidence to exclude satisfied lessons. Count unfinished lessons at full base initially; prefer an existing attempt's frozen base. Keep future-only lessons separate from `L`. Known future OHW is not today's backlog.

For each lesson's price, use a saved attempt's base first (prefer the active attempt, otherwise the latest finished attempt), then stored estimated duration, then the existing content estimator. If those cannot supply XP, use the median of directly priced lessons with the same knowledge-point count; if no such peers exist, use the overall lesson median. Record the fallback source, sample size and affected topic. Fallbacks never become samples for other fallback estimates. This is forecast-only: do not change lesson content, stored prices or XP awards. With no usable peer prices at all, retain an explicit unknown cost.

## 2. Average daily workload growth

Estimate growth from **assignment due dates from October 4, 2026 through today**, with an exponential **28-day half-life**. Future assignment dates never enter the historical numerator or denominator. The half-life is a weighting rule, not a trailing 28-day cutoff: retain every observation since October 4, with older dates receiving less weight.

Use all available assignment dates, including those before October 4, to find when each physical topic was first required. Apply the same graph selection, layer cutoff, prerequisite depth and course tracks. Count it once, excluding repeats across assignments, targets, Queue, prerequisite paths or tracks. Topics first required before October 4 stay out of the growth sample even if later assignments need them again. Exclude topics already known at or before their first due date, before pricing them; topics learned afterward still count as historical additions. Current mappings/graph supply the prerequisite and track projection.

```text
X_c(day) = new lesson base XP first required on that date in track c
age      = civil days from the observation date to today
weight   = 2^(-age / 28)
N        = elapsed civil days since October 4
W        = sum of 2^(-age / 28), for age = 0 through N-1

g_c = sum of weighted X_c(day) from October 4 through today / W

g = sum_c g_c
average weekly growth_c = 7 * g_c
```

Use one common window and weight denominator for additive course rates. Include zero-growth dates. Preserve the agreed elapsed-day convention: October 4 to October 21 is 17 daily intervals. Expose raw topic/XP totals, the unweighted daily XP rate, weighted rate, start/end and half-life. Report target, Queue and prerequisite-only categories, with target taking precedence over Queue.

Standing Queue and undated targets remain in today's backlog. Their manual membership changes are not assignment-driven future growth. Retained graph membership history is still used to recognize completed lessons that left the Queue, so they do not become unrelated recurring overhead. Work from weeks 0–1 remains in today's unfinished backlog even though those weeks are excluded from the growth-rate window.

**Project this average forward. Do not additionally insert individual future assignments on their due dates.** That would mix two demand models and could count the same growth twice. Moving a future OHW deadline farther into the future does not change the projection while it remains outside historical observations and today's backlog.

## 3. Recent pace and goal conversion

Use the last **seven completed local dates**, excluding today and including zero-study days. Use actual observed date coverage `d` if less history is available.

```text
X = base XP of all finished attempts, completed OR failed
M = recorded active working minutes over those dates

s = X / d                         current base XP/day
m = M / d                         current active minutes/day
v = X / M                         base XP per active minute

e = sum(earned XP) / sum(base XP)  same attempts with both values present
G = learner/daily-xp-goal          existing earned-XP goal
s_goal = G / e                     base XP/day at the goal
```

Include lessons, reviews, quizzes and failed attempts in `X` and paired goal-conversion totals. Include recorded unfinished work and homework in `M`; exclude pauses. Missing assignment XP is not invented. Missing timing must not inflate `v`. A usable positive `e` and a configured goal are needed for the goal forecast. The goal scenario assumes the goal is achieved every day.

## 4. Simple overhead estimates

```text
a = finished lesson-attempt base XP / successful lesson-attempt base XP
q = finished quiz base XP / finished non-quiz base XP
r = (finished review base XP + other non-quiz work outside modeled lessons) / d
```

`a` allows for retries. Use a longer available lesson history if the recent window has no successful lessons; otherwise leave an unsupported factor unknown. `q` is learner-wide; use the labeled rough fallback `15/150` only when the ratio cannot be measured. `r` uses the recent study mix, including outside-scope reviews without adding their topics to the lesson inventory. Completed lessons that left the Queue still count as modeled learning, not recurring unrelated overhead.

Expected review count over `t` days is `(recent review attempts / d) * t`. Review and quiz bases give expected XP costs. These are empirical approximations; no FIRe simulation is required.

## 5. Intersection of cumulative capacity and workload

```text
capacity_current(t) = s * t
capacity_goal(t)    = s_goal * t

work_required(t) = (1 + q) * [a * (L + g*t) + r*t]

B = (1 + q) * a * L
k = (1 + q) * (a*g + r)

T_current = B / (s - k)
T_goal    = B / (s_goal - k)

catch-up date = now + T days
```

These are the first intersections of the average cumulative curves. If today's backlog is already satisfied, return caught up now even if more assignments are due tomorrow. For positive backlog, a pace at or below `k` does not catch up under the assumed averages. Include fallback lesson prices in both inventory and growth, with a simple label such as “3 lessons use fallback XP estimates.” Only costs still unknown after the fallback prevent a full-backlog date; unresolved historical costs give a labeled lower-bound growth rate and an optimistic date. Both scenarios use the same workload, growth and overhead assumptions.

Allocate review/other overhead to course tracks where attributable and split global overhead by observed non-quiz shares. Course `B_c` and `k_c` use the same formulas with `L_c`, `g_c`, and `r_c`; they sum to the overall values. Use one shared study budget, not the full daily pace independently for each course.

For the sidebar's course catch-up estimates, split each pace evenly across the three courses: `T_current,c = B_c / (s/3 - k_c)` and `T_goal,c = B_c / (s_goal/3 - k_c)`. Apply the same complete/unavailable/not-catching-up rules per course. Keep each share fixed rather than redistributing it when another course finishes. Display rates in earned XP/day; retain base XP for all calculations. Changing the saved daily goal updates both goal-date displays.

## 6. Database inputs and code

| Values | Existing source |
|---|---|
| Topic scope, tracks and prerequisite closure | `learner/targets`, `learner/queue`, `topic/next`, curriculum membership, linked assignments and mapped topic coverage; independent forecast projection matching the Targets rules. |
| Current versus future work and full course dates | `learner/assignments`, `activity/due`, `activity/course`, nested assignment topic coverage. Use the assignment's local calendar date, not its import date. |
| Remaining lesson state and historical known-before evidence | Progress learned/legacy repetitions, completed lesson/review evidence and original completion dates, using engine preparation semantics and prerequisite ancestry. |
| Lesson bases | `learner-task/xp-base` for an existing attempt; otherwise existing `base_xp::activity_base` and `activity/expected-seconds`/content estimator. Forecast-only fallback uses `topic/knowledge-points` counts and directly priced peer lessons. |
| Pace, retries, quizzes, reviews and goal conversion | Owned tasks, activity type/topic, `learner-task/status`, `learner-task/xp-base`, `learner-task/xp-earned`, original `learner-task/finished-at` or dated terminal history. |
| Actual active minutes | Existing task-item timing/status intervals, working-ended cutoff and reliably dated saved durations; never add item time to the parent aggregate. |
| Historical scope of completed lessons | Retained target/queue membership and graph-association history; used for activity overhead attribution, not as a second arrival stream. |
| Goal | Existing `learner/daily-xp-goal`; no new stored counters or forecast attributes. |

[ui/forecast.js](ui/forecast.js) exports `readForecast()` and `withForecastGoal(forecast, earnedXpGoal)` for immediate goal previews. The read-only `/api/forecast-inputs?dayStarts=...` endpoint supplies evidence. [ui/target-scope.js](ui/target-scope.js) belongs to the forecast; the graph page keeps its own code. The output includes both dates, today's remaining XP, future-only inventory separately, measured pace, historical growth/coverage and overhead estimates. These are average-based planning estimates, not exact future schedules or exam-readiness guarantees.
