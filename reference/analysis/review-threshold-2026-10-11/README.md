# Review threshold and implicit practice

**Keep `:policy/review-threshold` at 0.5 provisionally, but reconsider the current one-day base half-life.** The new review-offer evidence points toward substantially earlier initial reviews. It does not recover a unique numerical threshold. This revises the earlier encompassing report's recommendation to retain the complete timing defaults unchanged.

Implicit repetitions are central to this conclusion. Studying a topic that exercises another skill gives that receiving skill fractional practice credit. That credit changes its memory and interval and can postpone its next review. Time since its last explicit lesson or review is therefore an incomplete measure of forgetting. A flat color can still contain fractional credit that has not crossed the next display boundary.

## Evidence examined

The analysis uses the encompassing report's frozen **3,033 activities across four separate accounts**, preserving account, course, topic and observation times. It re-read the saved progress observations and reconstructed **1,559 distinct first-observed review offers** from original queue journals and Learn HTML. Activities captured after those manifests are excluded.

The independent raw-progress check reproduced every previously analyzed direct-review before/after pair and included the darkest starting band. It retained **1,245 passed reviews with isolated progress pairs**, including unchanged and decreasing observations; 1,192 had a captured preceding passed lesson or review. See [raw reconstruction](raw_review_state.py) and [results](raw-review-state.json).

## Intervening credit changes the observed gaps

The following comparison requires an isolated upward change on an already-learned prerequisite target during another topic's activity. It uses the frozen encompassing analysis's structural qualification; a prerequisite path alone does not establish the exact practiced content or fractional dose.

| Account | Reviews with an intervening visible implicit rise | Median direct-practice gap, with a rise | Without an observed rise |
|---|---:|---:|---:|
| Foundations | 25 | 26.2 h | 14.5 h |
| Linear | 10 | 31.1 h | 14.7 h |
| Multivariable | 8 | 24.3 h | 12.6 h |
| Differential | 2 | 34.8 h | 14.7 h |

This is consistent with postponement through implicit practice. It does not measure the causal delay: longer gaps also allow more intervening activities, starting states differ, and flat-band credit is hidden. The last column means no *observed crossing*, not no implicit practice. Correct assessment answers are also not reconstructed as numerical memory updates in this comparison.

## Initial review offers are earlier than our default example

To reduce those confounds, the queue audit separates lessons from reviews and excludes captured remediation triggers, intervening assessments, visible upward crossings, stale color reads and late-recovered practice timestamps. For topics still in band 1:

| Account | First offer after first captured passed lesson | First offer after a passed review |
|---|---:|---:|
| Foundations | 10.17 h (25 observations) | 18.49 h (2) |
| Linear | 7.04 h (83) | 12.77 h (18) |
| Multivariable | 8.77 h (101) | 11.45 h (22) |
| Differential | 8.66 h (73) | 11.56 h (15) |

These are medians of **observed offers**, not known backend due times. Typical preceding-absence/first-presence brackets are 3–6 minutes, but a missing card need not mean a topic was ineligible. First captured learning need not be first-ever learning; flat colors still allow fractional implicit practice. Excluding intervening assessments also favors shorter windows. Nevertheless, the consistent early offers challenge our illustrative 48-hour initial review interval. See [queue audit](offers/README.md) for classifications and source verification.

## Why changing only the threshold is insufficient

The current engine computes `due age = half-life × log2(stored memory / threshold)`. Successful qualifying implicit practice increases memory and repetitions and recalculates the half-life. Its amount depends on coverage, performance, learning speed and the target's existing state. The threshold also affects the early-practice discount.

For illustration, with the current defaults, speed and quality 1, first learning gives memory 1 and one repetition: the first review is due in 48 hours. Half-coverage implicit practice 24 hours later gives about 0.293 fractional repetition credit and moves the due time to **82.8 hours after learning**. That postponement requires no threshold change. This is a calculation from our engine's equations, not a recovered Math Academy trajectory.

Raising the threshold to 0.9 would make that initial review due in 7.3 hours. But a full-credit success at that due point would then yield memory 1.9 and a 96-hour half-life, putting the next review **103.5 hours later**. Matching the first observed interval by changing the threshold alone can therefore produce unsuitable later intervals.

A separate color-response experiment profiled thresholds 0.2–0.9 while refitting its time scale and response amplitude. The training-selected threshold failed to improve later direct-review predictions in three accounts, and implicit-credit checks showed no consistent benefit. These are **observation-model sensitivity checks, not a chronological replay of the engine or validation of 0.5**. Details, source hashes and predictions are in [model audit](model-audit/README.md).

## Recommended calibration direction

Retain 0.5 as a provisional working threshold. Use the new evidence to evaluate a shorter base half-life together with chronological direct and implicit updates. A six-hour base half-life is a reasonable rounded candidate to test: with an illustrative assumed initial repetition credit of 0.5625–1, it produces initial intervals of about 8.9–12 hours. That credit range is not estimated from these captures. The candidate is not a fitted or validated replacement, and subsequent reviews must also be checked.

The decisive comparison should replay each receiving topic's memory, repetitions and interval through actual activities, including correct assessment practice and inferred fractional credit within unchanged bands, then predict later first offers separately for each account. Color histories constrain the credit; queue histories constrain the resulting timing. Neither raw direct-review gaps nor resetting a clock at every prerequisite-descendant activity supplies that replay.

**No database settings, engine code, capture records or existing reports were changed.** The artifacts here establish the timing discrepancy and the importance of implicit credit; they do not claim that a complete numerical memory history has been recovered.
