# Simple workload and completion forecast

Show two estimated catch-up dates: **at the current seven-day moving-average pace**, and **at the configured daily XP goal**. Both include continuing workload growth. Changing the goal updates the goal-pace date; no deadline input or backward calculation is needed. Keep workload and growth breakdowns per course. [estimate-forecast.md](estimate-forecast.md) contains the schema and engine details.

**Use base XP throughout: 1 base XP is 1 estimated minute of activity workload.** Actual minutes per base XP are measured separately. Reviews, quizzes, and failed lesson attempts all count toward completed base XP. Earned XP and its bonuses/penalties are not the workload unit.

## 1. Remaining lessons and historical growth

Let `S_c` be the final topic set assigned to course track `c` by the Targets graph. Reuse its exact course/Queue/week filters, unassigned-target handling, and track allocation, with prerequisite depth **2** and displayed layers **L30+**. Its final sets already contain each physical topic once in one reporting track; no separate deduplication step is needed.

```text
L_c = sum(lesson base XP for unfinished topics in S_c)
L   = sum_c L_c

g_c = newly required lesson base XP entering the filtered scope for course c
      / observed calendar days through now

g   = sum_c g_c
average weekly growth_c = 7 * g_c
```

Use the engine's existing preparation-completion evidence to exclude satisfied lessons. Initially count an unfinished lesson at its full base; no elaborate partial-credit calculation is required.

For growth, use all reliable comparable history through now, applying the same graph rules at each historical change. Count only genuinely additional unfinished topics: target/queue overlap, a prerequisite becoming a target, and a move between course tracks are not new physical work. Initial imported inventory is the starting backlog when its earlier arrival dates are unknown. Include observed zero-growth days; exclude future and unknown days.

Also report weekly added-topic counts and lesson XP for targets, queue, and prerequisite-only topics. For additive categories, use target first, then queue, then prerequisite-only. A category change adds no total workload. Withdrawals can be shown separately; do not assume they will continue reducing future demand.

Future assignments already represented in `L` are not added again. Continuing `g` is a rough assumption about additional, not-yet-represented work. Use the same growth estimate for both completion dates.

## 2. Current speed and simple overhead estimates

Use the last **7 completed local dates**, including zero-study days. Call the actual number of observed dates `d` if fewer than seven are available.

```text
X = sum(base XP of all finished activity attempts, completed OR failed)
M = total recorded active working minutes during the same dates

s = X / d                         base XP accomplished per calendar day
m = M / d                         active minutes per calendar day
v = X / M                         base XP per active minute
```

Include reviews, quizzes, and failed lessons in `X`. Include recorded work on unfinished activities and homework in `M`; exclude pauses. These are recent throughput estimates, not earned XP or successful-acquisition-only metrics.

The existing daily goal is **earned XP/day**, so convert it before comparing it with base-XP workload:

```text
G = learner/daily-xp-goal
e = sum(earned XP) / sum(base XP) for the same finished attempts over those dates
s_goal = G / e                     estimated base XP/day at the goal
```

Use attempts with both values for `e`, including failed attempts and their actual awards. This assumes the recent bonus/penalty mix continues; it does not change the workload unit. If no goal is set or no usable positive conversion is available, leave the goal date unavailable. The goal date assumes the goal is achieved every day.

Use three small estimates to put future lessons, retries, reviews, and quizzes on that same workload scale:

```text
a = base XP of all finished lesson attempts
    / base XP of successfully completed lesson attempts

q = finished quiz-attempt base XP
    / finished non-quiz-attempt base XP

r = (finished review base XP + other non-quiz base XP outside the modeled lessons)
    / d
```

- `a` is an observed retry allowance. Failed attempts contribute to its numerator. If there are no failures, `a = 1`. If no successful lessons are observed, use a longer available period or leave it unknown.
- `q` is the learner-wide quiz workload per non-quiz base XP. If history is insufficient, use the explicitly approximate fallback `q = 15 / 150 = 0.10`. Do not create independent quiz schedules for each course.
- `r` is recurring review/other workload in base XP/day. For reviews alone, expected review count over `T` days is `(finished review attempts / d) * T`. Use each attempt's base, including failed reviews. Include outside-scope reviews here without adding their topics to `L`.
- “Other” includes recurring priced activity not already in the modeled lessons, reviews, or quizzes. Each activity contributes once. Unknown homework XP is not fabricated; its recorded time still affects `v`.

These approximate the recent study mix continuing. Review demand may increase as more topics are learned; this first estimate does not simulate FIRe. Show the observed review rate so the assumption is visible.

## 3. Workload and the two completion dates

For a horizon of `T` calendar days:

```text
estimated lesson-attempt work = a * (L + g*T)
estimated review/other work   = r*T
estimated quiz work          = q * (a*(L + g*T) + r*T)

W(T) = (1 + q) * (a*(L + g*T) + r*T)
```

Define two convenient totals:

```text
B = (1 + q) * a * L                 initial work, including retry/quiz allowance
k = (1 + q) * (a*g + r)             additional base XP/day, including overhead

T_current = B / (s - k)
T_goal    = B / (s_goal - k)

current-pace completion date = now + T_current days
goal-pace completion date    = now + T_goal days
```

If `L = 0`, today's lesson backlog is already complete. For positive backlog, a pace at or below `k` does not catch up under the assumed growth/overhead: report that separately for each pace instead of manufacturing a date. Recompute the goal date when the daily XP goal changes. Keep `a`, `q`, `r`, and `g` the same in both scenarios so the goal controls only assumed daily capacity.

## 4. Per-course results share one budget

Use `L_c` and `g_c` above. Allocate review/other overhead to courses using the graph's topic tracks where available. Split global/unattributable overhead by observed non-quiz base-XP shares. This produces `r_c` with `sum_c r_c = r`.

```text
B_c = (1 + q) * a * L_c
k_c = (1 + q) * (a*g_c + r_c)

B = sum_c B_c
k = sum_c k_c
```

These course workloads sum to the overall workload. The two overall dates assume study effort can move between courses as needed. They use one shared current pace or goal pace; never give each course the full daily capacity. Separate course completion dates or a course-allocation planner are not required.

## 5. Values to read from the database

| Values | Database source / existing calculation |
|---|---|
| `S_c`, topic categories, historical entries | `learner/targets`, `learner/queue`, `topic/next`, curriculum membership, linked assignments and topic coverage; reuse Targets graph selection and placement. Membership/graph history supplies past states and recorded entry dates. |
| Unfinished lessons and `L_c` | Topic progress (`progress/learned`, legacy repetitions) plus historical lesson/review evidence, using existing engine preparation semantics. Lesson definitions use `activity/type` and `activity/scope`. |
| Lesson bases | Frozen `learner-task/xp-base` for an existing attempt; otherwise existing `base_xp::activity_base`, using `activity/expected-seconds` or the existing content estimator. |
| `X`, lesson/review/quiz subtotals, `a`, `q`, course shares | Learner-owned tasks: activity reference/type/topic, `learner-task/xp-base`, terminal `learner-task/status`, original `learner-task/finished-at` or terminal status history. Count both completed and failed attempts once. |
| `G`, `e`, `s_goal` | `learner/daily-xp-goal` is the existing earned-XP goal. Use paired `learner-task/xp-earned` and `learner-task/xp-base` over the same recent dates to estimate its base-XP equivalent. |
| `M` | Existing timing calculation over task-item status intervals and `task-item/working-ended-at`; saved elapsed durations where dated reliably. Do not add item durations to their parent task aggregate. |
| `g_c`, observation duration | Historical filtered scope entries and topic completion state when they entered. Value genuinely additional lesson work using existing lesson bases. Track transfers and completions are not arrivals. |
| `r`, `r_c`, expected review count | Dated review and other finished attempts, their bases, topics/tracks, and observation days. This is an empirical estimate of work likely to surface, not an exact future due-date simulation. |

Use original activity dates rather than import dates. Unknown costs or time remain unknown, with known subtotals shown. Do not present incomplete timing as a complete productivity measurement.

The main output is the two completion dates: **at the current seven-day average** and **at the daily XP goal**. Supporting values are remaining lesson XP, recent base XP and active minutes/day, average weekly topic/XP additions and observation dates, and estimated quiz/review work, with course workload breakdowns. These are approximate planning estimates, not exam-readiness guarantees. No deadline planner, ledger subsystem, exact partial-stage accounting, engine simulation, or probability model is required.

Implemented calculation entry points are in [ui/forecast.js](ui/forecast.js): `readForecast()` reads the existing Targets filter preferences and returns the calculated values; `withForecastGoal(forecast, earnedXpGoal)` previews another goal immediately. The read-only `/api/forecast-inputs?dayStarts=...` endpoint supplies database evidence. Selection and placement are shared with the viewer through [ui/target-scope.js](ui/target-scope.js). No display layout or schema changes are included.
