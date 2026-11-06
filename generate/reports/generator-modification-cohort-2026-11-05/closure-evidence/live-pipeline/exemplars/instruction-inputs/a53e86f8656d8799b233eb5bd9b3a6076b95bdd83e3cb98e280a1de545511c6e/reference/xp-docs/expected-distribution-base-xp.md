# Selected lesson base-XP formula

Implemented October 4, 2026 in [base_xp.rs](../../engine/rust/base_xp.rs). This is the selected production formula; the earlier actual-question-difficulty fit is a historical comparison.

The calculation requires content, not individual question difficulty labels, learner accuracy, or elapsed time. Default expected initial lesson distribution is 60% easy, 30% moderate, 10% hard. Workload weights 1/2/4 give an expected multiplier of 1.6. Runtime probabilities come from the active policy and are normalized before use.

At those default probabilities:

```text
L = 1.2364010385163302  T
  + 0.46544714915426905 K
  + 0.07513004637186382 R
  + 0.001586056170966394 S
  + 0.034422123109798704 E
  + 2.7349018409710975  P
  + 0.06047150091696244 F
  + 0.5742034148595132  A

base_xp = max(7, floor(topic_multiplier × L + 0.5))
expected_seconds = base_xp × 60
```

K is the number of KPs. T is the sum of per-KP mean solution math-token counts, divided by 100. R is tutorial plus canonical-example prose words, divided by 100. S is the sum of per-KP mean solution equals-sign counts; E is the total in canonical examples. P is the sum of per-KP mean prompt math-token counts, divided by 100. F is the sum of per-KP mean additional answer fields beyond the first. A is the sum of per-KP fractions containing a blank answer field. These lexical counts are workload proxies, not semantic operation counts. Images are excluded from text measurements.

The Rust implementation calculates the derived T and K coefficients from the original full-content coefficients and policy probabilities. It rounds once, using half-up rounding, after applying the positive finite topic multiplier. Missing `:topic/difficulty` means 1.0. The topic multiplier never enters retention speed or learner accuracy.

## Sampling and missing content

Recorded lesson calibration uses the **first two distinct practice questions per KP in presentation order**, with all tutorials and canonical examples. The database's question pools are unordered, so initial catalog estimates average the available practice pool for each KP rather than inventing presentation order.

Most imported practice questions have no stored worked solution. For the initial catalog estimate, the corresponding KP's canonical worked solution supplies the missing solution-length and equals-sign measurements. Prompt and answer-field measurements still come from the actual practice question. The estimate records `canonical_solution_proxy_count`; question content is not modified. These are provisional estimates, and the complete-capture fit error below does not measure the accuracy of this substitution. Missing canonical solutions or incomplete KP structure are reported rather than silently priced as complete content.

## Storage and calibration

- Shared workload correction: `:topic/difficulty`, default 1.0.
- Activity duration: `:activity/expected-seconds`, storing base XP × 60.
- Frozen attempt allocation: `:learner-task/xp-base`, set when starting an attempt if absent. Existing attempt bases are preserved.

An authoritative recorded lesson base B > 7 calibrates `topic_multiplier = B / L`, using the unrounded score. At B = 7 the floor makes the multiplier nonunique: preserve 1.0 if it already predicts seven; otherwise use 7/L. The engine checks that the calibrated score reproduces B. Keep the observed activity duration B × 60 authoritative. An estimate based on different sampled content can differ even with the same multiplier.

The `fire request` operations `estimate_lesson_xp` and `calibrate_lesson_xp` accept either explicit `features`, or saved capture `content` with `tutorial_words`. Content-based requests enforce two distinct questions and complete canonical-example coverage per KP. Calibration additionally accepts integer `base_xp`; estimates accept an optional positive `multiplier`. An optional `weights` array supplies policy weights. Results include formula version, normalized distribution, features, unscaled score, multiplier, base XP, and expected seconds. These operations calculate without database writes; save the result with its source observation, then update topic multiplier and activity duration together in a basis-guarded transaction.

## Fit evidence

The same frozen 58 lessons, with unchanged original coefficients and no refitting:

| Practice sample | Mean absolute error | Within 2 XP |
|---|---:|---:|
| All five questions per KP | 2.40 XP | 41/58 |
| First two questions per KP | 2.47 XP | 41/58 |

See [saved comparison](../mathacademy-base-xp/expected-distribution-comparison.json). The original 1.95-XP result required actual question difficulty labels and five questions per KP; it is not the error of this selected formula.

## Initial database backfill

```bash
python scripts/initialize_activity_xp.py --output .local/edb/initial-xp-preview
python scripts/initialize_activity_xp.py --output .local/edb/initial-xp-preview --apply
```

The wrapper invokes the Rust planner, saves estimates and proxies, previews the transaction, and uses a basis guard and stable retry key to commit only `activity/expected-seconds`. It verifies the stored values and unchanged learner/policy facts. Existing durations are preserved. Repeating the committed request replays its receipt; preparing a fresh plan after backfill produces no additional lesson writes.

The lesson formula does not price assignments, reviews, or assessments. Other activities can use existing complete step durations, or a timed assessment's explicit time limit. Unsupported activities are listed in the plan; no arbitrary lesson-floor estimate is assigned to them.

Changes to policy probabilities, content measurement, or source lesson version require explicitly regenerating affected duration estimates and workload calibrations. Existing estimates are not silently rewritten by a learner attempt.
