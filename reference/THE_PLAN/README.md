# Base XP and learner expected accuracy

Agreed direction: October 4, 2026. The schema and Rust engine changes below are implemented. The initial catalog transaction and its verification are recorded in the implementation results section. [Current formula documentation](../xp-docs/expected-distribution-base-xp.md) describes runtime behavior and calibration operations.

## Decisions

1. Repurpose `:topic/difficulty` as a positive workload multiplier used only in lesson base-XP estimation. Its default is **1.0**. Adjust it using authoritative Math Academy lesson base XP and captured content.
2. Add `:progress/expected-assessment-accuracy` and `:progress/expected-practice-accuracy`. These are learner-specific predictions initialized from performance on **direct prerequisite topics**, weighted separately by assessment and practice evidence mass.
3. Adopt the **expected-difficulty-distribution plus content formula** as the selected base-XP formula. Use the existing full-content coefficients with the configured 60% easy / 30% moderate / 10% hard distribution and workload weights **1/2/4**. Individual question difficulty labels are not required. The actual-difficulty and compact alternatives remain historical comparisons.
4. For calibration from a recorded lesson, measure the **first two practice questions per KP, across every KP in the lesson**. Retain all tutorial reading and canonical-example measurements.

“First two KPs” in the request is interpreted as **first two questions per KP**, consistent with the immediately preceding comparison. Restricting a whole lesson to its first two knowledge points would omit part of its content.

## What the XP estimate represents

Base XP is the lesson's allocated expected workload, using the displayed task denominator as the authoritative observation. Earned XP, correctness bonuses, penalties, actual elapsed time, and individual pace do not enter its calibration.

Our pricing assumption is a successful initial pass with two practice questions per KP, using the configured initial lesson difficulty distribution of 60% easy, 30% moderate, and 10% hard. A particular pair of captured questions need not match those percentages. Apply the expected distribution to its measured content instead of using individual difficulty labels.

The source describes XP as content-based expected time estimates subsequently calibrated with student data. It does **not** establish that Math Academy's base XP is computed exclusively from a learner getting exactly two questions correct per KP. Treat that successful-pass interpretation as our design assumption, rather than a recovered engine rule.

The selected expected-distribution formula averages **2.40 XP absolute error** with five captured questions per KP across the same 58 lessons, and **2.47 XP** using the first two questions per KP. These results retain the existing coefficients without refitting. The former actual-difficulty formula's **1.95 XP** result does not apply to this selection. Topic multipliers will correct observed lesson bases; that correction is calibration to known observations, not evidence of predictive accuracy on other content.

## Selected formula

For each KP, take the first two distinct captured practice questions in recorded presentation order. Do not sort by difficulty or question ID. Canonical examples do not occupy either practice slot. If fewer than two questions are available, produce a provisional estimate from available content and record the incomplete coverage; do not use it to tune the topic multiplier.

Initial estimates from the database use the available unordered practice pool per KP, since no recorded presentation order exists there. Missing practice worked solutions use that KP's canonical worked solution as a provisional measurement proxy; estimates record how many substitutions were used. Recorded-capture calibration still requires actual complete worked solutions and two questions per KP. No question content is changed by this estimate.

Let `mean_k` mean the average over that KP's selected questions. The expected difficulty-weight multiplier is `0.60 × 1 + 0.30 × 2 + 0.10 × 4 = 1.6`. Substitute `W = 1.6T`, `M = 0.30K`, and `H = 0.10K` into the full-content formula. This assumes the same content-length measurement represents the expected band mix; it does not estimate separate mean lengths for each band.

| Symbol | Measurement |
|---|---|
| T | Sum of per-KP mean unweighted solution math-token counts, divided by 100 |
| K | Number of KPs in the lesson |
| R | All tutorial and canonical-example prose words, divided by 100 |
| S | Sum of per-KP mean equals-sign counts in practice solutions |
| E | Total equals-sign count in canonical-example solutions |
| P | Sum of per-KP mean prompt math-token counts, divided by 100 |
| F | Sum of per-KP mean additional answer fields beyond the first |
| A | Sum of per-KP fractions with at least one blank answer field |

```text
L = 1.2364010385163302  T
  + 0.46544714915426905 K
  + 0.07513004637186382 R
  + 0.001586056170966394 S
  + 0.034422123109798704 E
  + 2.7349018409710975  P
  + 0.06047150091696244 F
  + 0.5742034148595132  A

c = topic/difficulty, default 1.0
estimated_base_xp = max(7, floor(c × L + 0.5))
```

Apply the multiplier to the **unrounded score L**, then round once and apply the seven-XP floor. Do not multiply an already rounded or floored prediction. `c` must be finite and strictly positive; it can be below or above 1 and is not an accuracy probability.

The coefficients of T and K above incorporate the fixed expected distribution. At implementation time, compute them from the original coefficients and versioned policy probabilities, rather than allowing the displayed derived decimals to drift from policy settings. A policy-distribution change changes the estimator version and requires recalibration of existing topic multipliers. Question difficulty labels can still be stored for other uses, but are not inputs to this formula or prerequisites for calibration.

Preserve the current lexical measurement rules and coefficients when first implementing this plan. Math stored in images is currently omitted by the text estimator. Record that limitation with the measurements. If extraction is improved later, version the measurement rules and recompute affected calibrations using the new unscaled L, rather than carrying forward incompatible multipliers.

## Calibrating topic difficulty from Math Academy

Use a complete lesson capture or recorded lesson with an authoritative base denominator `B` and content covering every KP. Individual question difficulty labels are unnecessary. Keep the observed activity base XP itself as authoritative; the multiplier provides a compatible estimate for that topic's lesson content.

For `B > 7` and `L > 0`, set:

```text
c = B / L
```

This makes the unrounded calibrated score equal to `B`, reproducing its integer base after rounding. For example, an observed base of 25 uses `25 / L`; dividing by the rounded prediction of 14 would introduce unnecessary error.

For `B = 7`, the floor means there is no uniquely identifiable multiplier. Keep `c = 1` if the unadjusted formula already predicts 7. Otherwise use `c = 7 / L` to reproduce the observed base. Mark this as a floor-limited calibration. A zero/nonfinite L, missing required content, or a base outside this lesson model's scope cannot produce a valid calibration.

Save the topic and activity IDs, source file, capture date, observed base, selected question IDs, configured expected distribution and workload weights, complete-KP coverage, feature values, unscaled L, formula/extraction version, and resulting multiplier. Retain question bands as optional provenance when available. Preserve previous observations. Use the most recent eligible observation for the current lesson version; do not blend different lesson versions silently.

Recompute each adjustment from the original unscaled formula, never from a score that already includes the previous multiplier. Reimporting the same observation must be a no-op. Reviews, quizzes, assessments, and multistep activities cannot calibrate this lesson multiplier.

The multiplier absorbs missing workload features and sampling variation as well as real content demands. It should not be interpreted as a universal measure of intrinsic topic difficulty. A scalar learned from one two-question sample reproduces that observation, but other sampled questions can produce a different estimate.

## Learner-specific expected accuracy

Add optional finite double attributes in `[0,1]` to the learner progress schema:

```text
:progress/expected-assessment-accuracy
:progress/expected-practice-accuracy
```

For the learner and target topic, find direct prerequisites through the reverse of `:topic/next`. For each channel, use prerequisite records with positive evidence mass:

```text
expected_assessment_accuracy =
    sum(prerequisite_assessment_accuracy × prerequisite_assessment_mass)
    / sum(prerequisite_assessment_mass)

expected_practice_accuracy =
    sum(prerequisite_practice_accuracy × prerequisite_practice_mass)
    / sum(prerequisite_practice_mass)
```

If no direct prerequisite has positive mass in a channel, fall back to that learner's mass-weighted accuracy across topics in the same channel; if no such evidence exists, use `policy/initial-accuracy` (currently 0.8). Calculate the two channels separately. Evidence mass is the existing cumulative effective mass, not a proven statistical confidence measure.

Store these values as the initial forecasts when a learner-topic state is first created, before applying its first outcome. Use them to initialize the corresponding evolving accuracy channels where no topic evidence exists. They create no evidence mass and do not by themselves mark a topic learned or admit it to retention tracking.

Existing observed assessment/practice accuracy and evidence mass must remain intact. A migration can fill missing forecast fields using available prerequisite evidence, but must label those as migration-time estimates rather than historical forecasts. Once recorded, preserve the initial forecasts; any future forecast-refresh policy should be a separate explicit change.

Mass weighting and limiting the neighborhood to direct prerequisites are **our chosen prediction rule**. The public source supports neighborhood-based initialization but does not specify this exact weighting rule. Current code uses a broader neighborhood and an unweighted mean, so this is an intentional behavior change.

## Remove the old topic-accuracy meaning

Currently `:topic/difficulty` is an expected assessment accuracy in `[0,1]` and enters the retention engine's speed calculation. Repurposing it requires a coordinated schema and runtime change, not only changing its documentation.

Update the topic predicate to accept positive finite multipliers, with default 1.0. Remove this attribute from accuracy, retention, and learning-speed calculations, and from any population-assessment difficulty calibration path. Keep it exclusively in base-XP calculation.

As the initial removal rule, neutralize the old topic-accuracy factor in speed: retain the existing learner accuracy term, prior, exponent, and clamps. Algebraically, this gives `clamp((learner_accuracy / policy_initial_accuracy)^speed_exponent, minimum_speed, maximum_speed)`. The new expected-accuracy fields influence initialization; they are not silently substituted as a second factor in the old product. This is a local model change and must be documented as such.

Do not reinterpret any historical `[0,1]` topic accuracy values as workload multipliers. The previous database audit at basis 500 found no stored `:topic/difficulty` values; recheck at implementation time. If values exist then, preserve their provenance and explicitly migrate or retire their old meaning before installing the new validation.

## Implementation order and completion checks

1. Update topic/progress schema documentation, predicates, and migration handling together. Preserve captured content and learner outcomes.
2. Implement separate-channel prerequisite forecasts and their fallbacks. Keep existing observed learner performance intact.
3. Remove the old topic-difficulty accuracy input from retention speed and update dependency documentation.
4. Port the selected expected-distribution content formula into the production engine, retaining the original coefficient precision, token rules, half-up rounding, and floor. The existing estimator supplies the original full-content coefficients and lexical measurement rules, but its current difficulty-label requirement must be removed for this selected path.
5. Add two-question-per-KP feature extraction, authoritative base-XP calibration, and provenance records. Base-XP transactions must not manufacture learner performance from automated capture runs.
6. Document the final behavior and commit the implementation as the selected formula. Update the engine dependency diagram and existing XP report to distinguish the original actual-difficulty fit from the selected expected-distribution formula and its adopted two-question measurement rule.

Verify agreement with the expected-distribution comparison, operation with all individual difficulty labels absent, repeat-import stability, multiplier round trips to authoritative bases, default 1.0 behavior, floor-limited cases, separate-channel forecast weighting/fallbacks, and preservation of observed learner state. Check that a multiplier above 1 passes validation and cannot reach the former accuracy input. Verify that changes in capture question order cannot silently change an existing calibration's recorded sample.

## Implementation results

- Added and installed the two optional progress forecast attributes; updated topic documentation and validation to a positive workload multiplier. No old topic accuracy values were present. Schema transaction advanced basis 504 to 505.
- Rust forecasts use separate assessment/practice mass weighting over direct prerequisites. Their values remain frozen after initialization; existing observed channels are preserved.
- Retention speed now uses learner accuracy alone. Topic workload multipliers are read only by the base-XP module.
- The study app computes missing lesson bases from the selected formula and freezes them on attempts. Existing attempt allocations are preserved.
- Initial duration transaction advanced basis 505 to 506 and populated all **2,964 lesson activities**. Base estimates range from 7 to 52 XP, with median 9. **2,924 lessons** used at least one canonical worked-solution proxy. Nine assignments lacked a duration model or complete step estimates and were reported without assigning fabricated lesson estimates.
- Both schema and duration transactions verified unchanged learner and policy facts. The duration transaction's protected-fact comparison covered **4,587 facts**. The updated local writer and study app were activated.
- Verification passed: 78 Rust engine tests, 17 in-memory app tests, native schema/progress predicate checks, and the durable 13-presentation lesson lifecycle using a temporary learner. Both forecast attributes persisted; the attempt base stayed fixed. Cleanup restored the exact protected-fact fingerprint. A fresh backfill plan produced zero writes.
- Calibration calculation is available through `fire request` without individual difficulty labels. Automatic capture-import recalibration is a separate integration step; this initial backfill uses default workload multiplier 1.0.

Transaction evidence is retained in `.local/edb/xp-schema-2026-10-04/` and `.local/edb/initial-activity-xp-complete-2026-10-04/`, including plans, proxies, source features, previews, receipts, and verification. The reusable backfill command is `scripts/initialize_activity_xp.py`; it preserves existing durations and supports exact retries.

## Evidence and references

- [Full base-XP formula and original fit](../xp-docs/base-xp-formula-report.md).
- [Reference estimator](../mathacademy-base-xp/estimator.py).
- [First-two-question comparison](../mathacademy-base-xp/first-two-questions-comparison.json): 58 lessons, 190 KPs, 380 selected practice questions; unchanged coefficients.
- [Expected-distribution comparison](../mathacademy-base-xp/expected-distribution-comparison.json): selected formula with all five versus first two questions per KP, retaining the original coefficients.
- [Current topic schema](../../schema/data/5-1-topic.edn).
- [Current learner progress schema](../../schema/learner/1-3-learner-progress.edn).
- [Public model description, saved locally](<../The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md>): neighborhood initialization and the distinct population-based meaning of topic difficulty.

This plan applies to lesson base XP and learner accuracy initialization. The already selected earned-XP rules remain separate.
