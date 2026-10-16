# Encompassing calibration pilot

> **Historical pilot; its weight recommendations are superseded.** The current decision uses the original account-specific rising-activity frequencies, rounded to the requested fractions, for the full original positive candidate set. See the [selected frequency method](../../../../encompassing-report.md) and [fraction estimates](../frequency-fractions/README.md). The experiment, fits, and empirical findings below are preserved; its content-based weights and direct-edge omissions do not control the new prepared transaction.

## Historical decisions

Use these positive weights: **1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, 1**. These are our best guesses from the mathematical content and the frozen, account-specific observations. Internal fitted decimals remain in the evidence files, but the recommendations use the values a human would choose.

| Account | Source → target | Observations | Best guess | Graph decision |
|---|---|---:|---:|---|
| Foundations | 4387 Visualizing Cartesian Products → 48 Cardinality of Finite Sets | 3 | **3/5** | Effective relationship through intermediate topics; retain the path, do not add a direct cardinality edge. |
| Foundations | 4387 → 49 The Cartesian Product | 3 | **2/3** | Direct procedural component. |
| Linear | 1961 Matrix Relative to a Basis → 1195 Matrix–Column-Vector Multiplication | 0 | **3/5** | Direct procedural component, estimated from content. |
| Linear | 1961 → 1864 Coordinates in a Given Basis | 4 | **2/3** | Direct procedural component. |
| Linear | 1961 → 2211 Standard Matrix from the Standard Basis | 4 | **3/4** | Direct procedural component. |
| Multivariable | 2110 Fundamental Theorem for Line Integrals → 1951 Calculating Potential Functions | 5 | **1/4** | Direct component exercised by the potential-not-given KP. |
| Multivariable | 2110 → 3149 Conservative Vector Fields in the Cartesian Plane | 5 | **1/5** | Omit a new direct edge; conceptual prerequisite practice is weak. |
| Differential | 3245 Euler's Method for Systems → 2086 Introduction to Systems of Linear ODEs | 4 | **1/5** | Omit a new direct edge; context is shared more than target procedures. |
| Differential | 3245 → 3668 Euler's Method: Multiple Steps | 4 | **4/5** | Direct procedural component. |

The nine estimates concern **four source topics**, not nine source topics. Six relationships support a direct procedural edge. Whether to add an edge is a separate content decision: the two weak procedural relationships have positive estimates of 1/5 but remain omitted as direct edges. In this engine an explicit edge replaces inferred coverage for its pair. The 3/5 cardinality estimate is an effective relationship score through intermediate topics, rather than a direct procedural edge.

These values come from the full-data spacing-model fit with content priors. Round the original unrounded estimate to the nearest allowed fraction by absolute distance, with ties going to the larger fraction:

\[
\mathcal F=\left\{\frac15,\frac14,\frac13,\frac25,\frac12,\frac35,\frac23,\frac34,\frac45,1\right\},\qquad
w_{\rm recommended}=\max\!\left(\arg\min_{f\in\mathcal F}|f-\hat w|\right).
\]

The content-only relationship retains its prior before rounding. Zero is not a rounding option; omitting a direct edge is recorded separately. [content-decisions.json](content-decisions.json) records the exact fitted values, fractional decisions and mathematical reasons. [content-priors.json](content-priors.json) preserves the original inputs. Rounding changes the recommendation, not the underlying captured evidence.

## What the pilot establishes

The best working explanation is **spacing plus target state**, with a separate display recalculation effect. Current correctness and selected KPs matter, but neither alone explains the matched flat/rising sequences. Keep encompassing as a topic relationship; use selected KP content to explain how much of that relationship a particular activity exercises. Do not replace the topic graph with KP-only weights on this evidence.

The direct-review anomaly audit verified six decreases and two perfect 1→6 changes in raw saved HTML. There was no account/course/topic matching or color parsing error. All six decreasing targets also fluctuate nearby; one decrease occurs alongside 72 falling targets. Our best explanation for these falls is recalculation of displayed mastery, likely influenced by ability/performance and sometimes shared across topics. A fixed penalty per incorrect answer is a worse explanation for the broad changes and rapid reversals. The perfect jumps most likely involve a large ability/quality-sensitive update to an already-known topic and the top display category. Their prior practice times are unknown, so they do not estimate a spacing multiplier. See the [eight-case audit](direct-anomalies.md).

**The magnitude-fitted weights do not consistently beat frequency weights passed through the same spacing model.** This is an actual result of the pilot. The useful improvement is separating the probability of a visible crossing from intrinsic coverage and calibrating the practice response. We recommend the concrete content-backed weights above, while keeping frequency as a useful initial signal. We do not claim that this particular magnitude-fitting algorithm is a demonstrated improvement for mass-producing weights.

## Frozen experiment and account separation

[calibrate_encompassing_pilot.py](../../../../capture/scripts/calibrate_encompassing_pilot.py) reads the existing frozen timing reports. It does not import newly arriving captures. Every fit, age distribution, relationship nomination and prediction belongs to one account. No parameters or histories are averaged across accounts.

Within each account, the earliest 70% of **all audited activities** train the model; the remaining tasks test it. All targets from a task stay on the same side. The broad relationship panel is selected by at least one rise **in training**, without a minimum activity-count filter. The nine content relationships were chosen after earlier descriptive inspection and are a retrospective diagnostic panel, rather than a blinded sample.

| Account | Train / test activities | Train / test direct reviews | Training-nominated pairs | Pairs with one training observation | Later pair observations / distinct tasks |
|---|---:|---:|---:|---:|---:|
| Foundations | 872 / 375 | 429 / 146 | 793 | 241 | 46 / 16 |
| Linear | 466 / 200 | 163 / 110 | 251 | 76 | 7 / 5 |
| Multivariable | 415 / 178 | 135 / 72 | 192 | 77 | 59 / 29 |
| Differential | 368 / 159 | 110 / 70 | 52 | 20 | 7 / 6 |

Single-observation relationships stay in the analysis. Several later target observations share a source activity, so they are not independent experimental replicates. Many training pairs have no eligible later observation: the topic may not recur, or it may already be at the display ceiling. This test measures predictions for recurring, observable pairs.

The primary analysis includes unchanged targets and signed decreases. Starting bands must be 1–5, because a starting top category cannot reveal further upward movement. **Ending** band 6 remains included and is treated as a censored display endpoint. All original account/course matching and isolated-activity checks come from the frozen timing report.

## Direct-review observation model

This is a statistical observation model inspired by the local policy, not an execution replay of either Rust API. It uses display categories and observed age proxies. It does not fabricate initial repetitions, memory, assessment accuracy or a history outside capture.

For starting category \(b\), elapsed hours \(h\), and coverage \(w\), use

\[
H_b=H_1g^{b-1},\qquad
D(h,b)=\operatorname{clip}\left(2[1-2^{-h/H_b}],0,1\right),\qquad
\mu=wAD(h,b).
\]

Direct review fixes \(w=1\). Memory normalization 1, threshold 0.5, discount power 1, and the primary display-growth assumption \(g=2\) stay fixed. \(H_1\) and \(A\) are **effective display-response parameters**, not recovered engine half-life and speed. In particular, \(b\) has not been established as numerical repetitions. The amplitude absorbs typical quality, learner speed and display scale; the model does not equate current-task accuracy with quality.

The primary clock is hours since captured direct target practice. Intervening implicit refreshes make it an imperfect memory clock. A separately fitted sensitivity variant uses hours since any potential prerequisite-based refresh. Unknown ages use eleven training-only quantiles of known direct-review gaps, within starting band when at least eight such controls exist, otherwise within the account. This is an explicit imputation of missing state; missing history is not treated as zero age. Known-age and unknown-age test scores are reported separately.

Assume a uniform fractional starting position within a display interval. With \(k=\lfloor\mu\rfloor\) and \(f=\mu-k\), the ordinary model gives probability \(1-f\) to ending category \(\min(6,b+k)\) and \(f\) to \(\min(6,b+k+1)\). Average these probabilities over imputed ages when necessary. Add a signed residual:

\[
P(B^+=j)=(1-\epsilon)P_{\rm ordinary}(B^+=j)+\frac{\epsilon}{7},\qquad j=0,\ldots,6.
\]

This gives decreases and unusually large jumps nonzero probability without inventing negative encompassing weights. The uniform residual is a simple error model, not an assertion that all exceptional changes are equally common. A jump that the ordinary model cannot produce for **any** coverage receives residual probability and therefore does not force coverage upward. For example, the late multivariable 1→6 events remain poorly predicted; fitting a larger encompassing weight does not fix that failure.

Fit \(H_1,A,\epsilon\) on training direct-review categorical likelihood over these declared grids:

- \(H_1\): 6, 12, 24, 48, 96 hours.
- \(A\): 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5 display units.
- \(\epsilon\): 0.01, 0.05, 0.1, 0.2, 0.4, 0.6.

The predeclared alternatives are no timing effect, display growth 1, and the potential-practice clock. A smoothed empirical transition table conditional on starting band supplies a flexible no-clock comparator. Accuracy and capture pipeline scores are reported as strata; they are not silently treated as the same event mechanism. The primary model is not switched to whichever alternative wins the test set.

## Fitting encompassing weights

Hold the account's direct calibration fixed. Fit each relationship against its complete training sequence, including flats and decreases:

\[
\hat w=\arg\max_{w\in\mathcal G}\left[\sum_i\log P(B_i^+\mid b_i,h_i,w)
+\lambda\{m\log w+(1-m)\log(1-w)\}\right].
\]

The internal grid contains 101 evenly spaced values from 0.001 to 0.999. For a content-reviewed pair, \(m\) is the mathematical coverage prior and \(\lambda=2\). Other training-nominated pairs use \(m=0.5,\lambda=1\). This is a Beta prior with parameters \(1+\lambda m,1+\lambda(1-m)\). A relationship with no observations retains its content prior. There is no three-activity exclusion.

Lessons and reviews share the fitted ordinary activity amplitude in this first pilot. We do not model a lesson's extra KP count or imported-state initialization as established multipliers. This is one reason to use the fitted scores as informed estimates rather than treat their decimals as recovered physical constants.

For the old method, recompute \(K/N\) from **training only**, never from the original all-period proposals. Compare it directly as a crossing probability using Brier score. Also use \(K/N\) as a weight in the same spacing observation model, to isolate the effect of fitting weights from the effect of adding timing. A third comparator uses the same prior:

\[
w_{\rm smoothed\ frequency}=\frac{K+\lambda m}{N+\lambda}.
\]

Evaluate full-category log loss, crossing Brier score and positive-step prediction errors. Raw frequency has no original magnitude prediction, so it is not given an invented one-step prediction. The full-category comparisons use the declared probability models and their residuals. Fraction-rounded training weights get a separate prediction comparison. Do not multiply another binary-rise likelihood into the transition likelihood: that would count the same observation twice.

After fixing all test predictions, refit the direct models and the nine content relationships using all frozen observations to obtain the best current estimates. These final refits are separate output fields and are never scored as held-out predictions.

## Results

Lower scores are better. Direct-review crossing Brier scores:

| Account | Later reviews | No timing | Primary spacing | Empirical starting-band comparator |
|---|---:|---:|---:|---:|
| Foundations | 146 | 0.307 | **0.237** | 0.239 |
| Linear | 110 | 0.315 | **0.228** | 0.260 |
| Multivariable | 72 | 0.337 | **0.275** | 0.285 |
| Differential | 70 | 0.275 | 0.317 | **0.257** |

Spacing improves crossing prediction in three accounts and loses in differential. Full-transition log loss is more demanding: the primary spacing model beats its constant-dose counterpart in foundations and linear, and loses in multivariable and differential. The residual permits the anomalous changes, but does not predict their magnitudes well. This is a useful working model of ordinary changes, not a complete explanation of the display.

The primary direct model trained on early captures selected \((H_1,A,\epsilon)\) of (24 h, 0.5, 0.01), (12 h, 0.5, 0.01), (48 h, 1.5, 0.01), and (96 h, 2, 0.01), respectively. The all-data refits select (24 h, 0.5, 0.05), (48 h, 1, 0.01), (96 h, 2, 0.05), and (96 h, 1.5, 0.05). Those account differences and changing fits are another reason not to copy the observation parameters into the engine policy.

Later relationship crossing scores for pairs selected entirely from training:

| Account | Observations | Original frequency | Frequency + spacing | Smoothed frequency + spacing | Fitted weights + spacing |
|---|---:|---:|---:|---:|---:|
| Foundations | 46 | 0.421 | 0.101 | **0.099** | 0.116 |
| Linear | 7 | **0.187** | 0.368 | 0.397 | 0.384 |
| Multivariable | 59 | 0.590 | 0.272 | **0.247** | 0.278 |
| Differential | 7 | **0.302** | 0.625 | 0.626 | 0.609 |

On the same full-category comparison, fitted weights versus frequency-through-spacing have log losses 1.189 vs 1.169, 1.872 vs 1.930, 1.617 vs 1.739, and 2.136 vs 2.143. Some category scores improve while crossing scores worsen; there is no consistent victory. Linear and differential each have only seven later relationship observations. The account-specific result should remain visible rather than be hidden by a pooled score.

Rounding the training weights to the allowed fractions gives later crossing scores **0.116, 0.383, 0.278, 0.608**, respectively. The residual also remains imperfectly calibrated: in foundations it predicts a 0.17% direct-review fall rate on later captures versus the observed 2.05%. The other three accounts have no later direct-review falls, with predicted rates around 0.15–0.17%. Allowing anomalies is not equivalent to having explained or accurately forecast them.

Our decision is to use the fraction-rounded, content-backed pilot weights, retain timing in the engine, and keep the frequency score as an initialization signal. The evidence does **not** support replacing every old frequency score with the output of this display model. In particular, the two-component intuition—coverage affects whether practice reaches a component, timing changes its effective dose—is useful, but crossing probability also changes with timing. Frequency is not an independent measurement of coverage.

## Engine values and attributes

Our best current policy choice is to **keep the checked-in numerical defaults**:

| Setting | Working value |
|---|---:|
| Base half-life | 1 day |
| Interval growth | 2 |
| Initial memory / review threshold | 1 / 0.5 |
| Early-practice discount power | 1 |
| Initial accuracy / accuracy update rate | 0.8 / 0.2 |
| Speed exponent | 2 |
| Minimum / maximum speed | 0.25 / 4 |
| Slow implicit-credit gate | Enabled |
| Overdue failure slope / maximum multiplier | 1 / 4 |
| Retention update order | Decay before adding credit |
| Future planning horizon | 7 days |

Keep ordinary review quality at 1. Do not add a fivefold perfect-review bonus or a new incorrect-answer repetition penalty to reproduce color anomalies. Model display recalculation separately. Repetitions remain fractional operational state, memory remains anchored at its own timestamp, and elapsed time applies to that stored memory interval. Waiting removes an early discount; the current positive spacing multiplier caps at 1.

No new shared topic attribute is necessary for this pilot. Keep provenance, account, task, starting/ending band, quality/accuracy, chosen KPs, clock availability, and model version with the calibration evidence. The best implementation improvement is a distinct observation/readout layer so an ability-sensitive or noisy color change does not get treated as a literal repetition update. A later KP-level adjustment should refine the amount of a topic relationship practiced in an activity, not erase the topic-level relationship.

The two engine entry paths must remain explicit in an eventual operational replay: native `runtime.rs` uses mean graded performance for lesson/review completion and normalizes assessment question credit by per-topic question count; progressive `retrieval.rs` uses quality 1 events and `learning.rs` preserves banked imported repetitions at first local learning. Current progressive assessments require one question per topic. This pilot fits observations rather than replaying either path, so it cannot establish a policy difference between them.

## Artifacts and verification

- [experiment.json](experiment.json): declared grids, rounding, selection and script/prior hashes.
- `foundations.json`, `linear.json`, `multivariable.json`, `differential.json`: source hashes, exact task splits, fitted models, every held-out prediction, metrics by accuracy/pipeline/age, single-observation results, and separate full-data refits.
- [content-decisions.json](content-decisions.json): nine human-scale recommendations attributed to Codex, with direct-edge decisions.
- [direct-anomalies.json](direct-anomalies.json): exact saved HTML evidence and neighboring changes.
- [test_encompassing_pilot.py](../../../../capture/scripts/tests/test_encompassing_pilot.py): checks account isolation, task/time boundaries, future-data leakage, singleton retention, saturation and signed residuals.

Reproduce from the repository root with a Python environment containing NumPy:

```sh
/home/jake/Developer/MA/.venv/bin/python capture/scripts/calibrate_encompassing_pilot.py
PYTHONPATH=capture /home/jake/Developer/MA/.venv/bin/python -m unittest scripts.tests.test_encompassing_pilot
```

No engine parameter or database entity was changed. The earlier frequency-only transaction remains superseded. These are explicit recommendations and reproducible evidence; any replacement transaction should use the rounded component weights and check existing effective paths before inserting overriding edges.
