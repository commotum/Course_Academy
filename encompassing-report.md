# Encompassing weights estimated from captured progress bands

## Selected method: original frequency weights at the requested fractions

**Use the original rising-activity frequencies as the initial encompassing weights, rounded to 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, or 1.** This is the current decision. It applies to the full original set of positive relationships, including those with only one observed activity. The magnitude, timing, content, and persistence investigations below remain background evidence; their alternative weight recommendations are superseded.

For an account $a$, source topic $s$, and target topic $t$, let $N_{a,s,t}$ be the number of original eligible activities, and let $b_i^-$ and $b_i^+$ be the target's before/after bands. Calculate:

$$
K_{a,s,t}=\sum_{i=1}^{N_{a,s,t}}\mathbf{1}[b_i^+>b_i^-],
\qquad \widehat w_{a,s\to t}=\frac{K_{a,s,t}}{N_{a,s,t}}.
$$

Then round the exact ratio directly to the nearest allowed fraction, choosing the higher fraction at an exact midpoint:

$$
\mathcal F=\left\{\frac15,\frac14,\frac13,\frac25,\frac12,\frac35,\frac23,\frac34,\frac45,1\right\},
\qquad
w_{a,s\to t}=\max\!\left(\arg\min_{f\in\mathcal F}\left|f-\frac{K_{a,s,t}}{N_{a,s,t}}\right|\right).
$$

Distances use exact rational arithmetic. The calculation does not first round to a decimal or to the old 0.05 increments. The transaction stores the resulting numerical value as a double; the exact fraction and original $K/N$ remain in its rationale and evidence.

Each rising activity contributes **one** to $K$: a 1→6 change and a 3→4 change each count as one rise. Flat and falling observations remain in $N$. Jump magnitudes and activity sequences remain available in the evidence, but do not change these weights. There is no minimum activity-count threshold, shrinkage, correctness multiplier, or additional spacing, diagnostic, content, or persistence adjustment.

### Original observation rules retained

The original sample consists of passed, fully graded lessons and reviews with a known source topic and usable before/after snapshots. Comparisons match account, course, and topic; duplicate course displays must agree. The observation interval must isolate one same-account activity, last at most 30 minutes, and use a timely baseline. Targets start in bands 1–5: starting band 6 cannot reveal another upward crossing, and starting band 0 belongs to placement or admission. An ending band of 6 remains eligible.

The candidate set contains prerequisite ancestors with at least one eligible rise, at any prerequisite distance. For each candidate, the denominator includes all its eligible exposures, including those before its first rise and after its last rise. Relationships with no rise are left unestimated. These are the original eligibility and discovery rules; the current rounding pass adds no exclusions. The [original methodology](reference/mathacademy/encompassing-analysis-2026-10-11/frequency-method-v1.md) preserves the detailed capture and activity-sequence definitions; its old 0.05 rounding and transaction status are historical.

### Coverage and examples

The result is **1,789 account-specific estimates**, covering **1,730 distinct source→target relationships across 533 source topics**. All **651 account-specific estimates with one eligible activity** remain included. The 533 source topics represent approximately **17.9% of the frozen 2,977-topic catalog**; this means each has at least one estimated outgoing relationship, not that all of its relationships have been estimated.

| Account | Relationship estimates | Estimates with one eligible activity |
|---|---:|---:|
| Foundations | 936 | 272 |
| Linear | 274 | 84 |
| Multivariable | 372 | 141 |
| Differential | 207 | 154 |
| Total | **1,789** | **651** |

Four examples from the full estimate set:

| Account | Source → target | Rising / eligible activities | Selected weight |
|---|---|---:|---:|
| Foundations | 4387 Visualizing Cartesian Products → 48 Cardinality of Finite Sets | 3 / 3 | **1** |
| Linear | 1961 Matrix Relative to a Basis → 2211 Standard Matrix from the Standard Basis | 3 / 4 | **3/4** |
| Multivariable | 2110 Fundamental Theorem for Line Integrals → 1951 Calculating Potential Functions | 2 / 5 | **2/5** |
| Differential | 3245 Euler's Method for Systems → 3668 Euler's Method: Multiple Steps | 3 / 4 | **3/4** |

### Account separation and committed transaction

Every frequency, denominator, and activity sequence stays within its original account. Where several accounts estimate the same shared relationship, the transaction selects **one complete account estimate**: most eligible observations first, then lower rounded weight, then account name. No counts, histories, or weights are pooled or averaged. All competing estimates remain in the evidence. The selected 1,730 relationships include **619 based on one eligible activity**.

The [fraction estimates](reference/mathacademy/encompassing-analysis-2026-10-11/frequency-fractions/README.md) retain the original evidence and its hashes. Following the user's authorization, the [transaction](reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/transaction.edn) **committed in `math` at basis 1308**, with **`:agent/gpt-6.1-sol-high` as its source**, as requested. It added the 1,730 relationships on 533 source topics. Every approved fraction, numerical weight, selected account, and observation count was retained. Earlier prepared requests remain preserved and unsubmitted.

The [native preview](reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/preview-verification.json) passed at basis 1307. The durable transaction advanced **1307 → 1308**, with 6,920 domain assertions, one transaction timestamp, and no retractions. [Commit verification](reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/commit-verification.json) confirms exact agreement with the preview, attribution of every assertion to the requested model source, and read-back of every domain fact at the committed basis. The earlier analysis and preparation suite passed 63 tests. The [bundle notes](reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/README.md) preserve the request, receipt, and verification.

All original positive candidates were retained as direct edges. Because explicit edges override inferred paths in the engine, preparation also records a [coverage audit](reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-gpt-6.1-sol-high/coverage-override-audit.json). Fourteen new direct edges override higher coverage that could otherwise be inferred through other new edges; no effective coverage decreases relative to the existing database graph were found at the read basis. This audit does not filter the selected estimates.

The engine's numerical defaults remain unchanged. These initial weights use frequency as the chosen practical estimate; the later observation models do not supply extra multipliers to this transaction.

Reproduce the fractional estimates from the repository root:

```bash
PYTHONPATH=capture python3 -m scripts.round_encompassing_frequency reference/mathacademy/encompassing-analysis-2026-10-11
```

The estimate generator performs no database writes. The committed bundle retains its exact saved request and receipt; do not create a new request to repeat the import.

## Historical analysis and superseded recommendations

The material below preserves the magnitude, spacing, content, and reassessment investigations. Their empirical findings remain available, but statements recommending pilot weights or rejecting frequency weights describe earlier decisions. **The selected method above governs the current estimates and committed transaction.**

<details>
<summary>Read the earlier analyses and recommendations</summary>

> Historical status before returning to frequency weights: the initial frequency-only transaction was superseded in favor of the calibration pilot. No database transaction was committed.

## Behavior audit: reviews, lessons, assessments, and reassessment

The [follow-up behavior analysis](reference/mathacademy/encompassing-analysis-2026-10-11/restoration-analysis/README.md) verifies the potential-functions critique and compares activity types using a common observation scope. **Large jumps remain after excluding diagnostics, including after passed reviews before an account's first captured diagnostic.** The original prerequisite-only panel contains multi-band jumps after 92 foundations, 23 linear, 21 multivariable, and 14 differential reviews.

The two potential-functions jumps have different persistence. The early review's 1→3 rise reverses after **32.6 minutes**. The later lesson's two component jumps from 1 to 6 persist through **40 original observations spanning 6.10 hours**, following 28 observations at 1. The earlier and later lessons have identical KP-level accuracy. The previous high bands of 5 and 6 were themselves assigned after an earlier diagnostic, and the later comparison uses a different course page. The best explanation is **post-diagnostic component revalidation**, not five newly earned repetition units or a larger encompassing weight.

The broader comparison finds no consistent lesson-over-review multiplier. Many multi-band changes reverse: for example, 617/786 foundations review-associated target jumps and 601/705 lesson-associated jumps return to their starting band within six hours. These common-scope counts include all comparable page topics, including unrelated ones; they must not be interpreted as encompassing credit. Directly assessed topics show a cleaner sign pattern: correct answers produce flat or rising bands, incorrect answers flat or falling bands; their largest observed increase is two bands.

Separate **ordinary signed practice credit**, **diagnostic/course reassessment**, and **transient displayed-state changes** before fitting a single magnitude response. Keep lesson initialization separate from blue-start practice and retain account/course identity throughout. The earlier pilot did not distinguish all these regimes; its scores remain reproducible, but do not validate treating every jump as an ordinary repetition increment. This behavior audit changes that interpretation without rewriting the historical fits or changing stored weights.

## Completed pilot and best-guess weights

Use **1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, or 1** for positive encompassing recommendations. The pilot fits keep their internal decimals for reproducibility; each final value is the allowed fraction nearest to the original unrounded estimate, with midpoint ties upward. Four example relationships from the nine-relationship pilot are:

| Account | Source → target | Best guess |
|---|---|---:|
| Foundations | 4387 Visualizing Cartesian Products → 48 Cardinality of Finite Sets | **3/5** |
| Linear | 1961 Matrix Relative to a Basis → 2211 Standard Matrix from the Standard Basis | **3/4** |
| Multivariable | 2110 Fundamental Theorem for Line Integrals → 1951 Calculating Potential Functions | **1/4** |
| Differential | 3245 Euler's Method for Systems → 3668 Euler's Method: Multiple Steps | **4/5** |

These are concrete working estimates. The foundations→cardinality score describes effective coverage through intermediate topics; it should not become a new direct cardinality edge. The [completed pilot](reference/mathacademy/encompassing-analysis-2026-10-11/calibration-pilot/README.md) contains nine estimates covering four source topics, six recommended procedural component relationships, equations, raw predictions and the engine-value recommendations. Whether to add a direct edge is a separate content decision: the two weak procedural relationships round to 1/5 but remain omitted as direct edges. Any explicit edge would override inferred coverage for its pair.

**Keep the numerical engine defaults**, including base half-life 1 day, interval growth 2, memory 1, review threshold 0.5 and early-practice discount power 1. The color-response fit is useful for calibration, but its parameters are not the engine's numerical memory state. The most useful addition is a separate display observation model; no new shared topic attribute or perfect-review bonus is required for this pilot.

The chronological check used the earliest 70% of each account's activities for training and later captures for testing. There was no cross-account pooling and no three-activity exclusion. Spacing improved direct-review crossing prediction in three of four accounts. **Magnitude-fitted encompassing weights did not consistently beat frequency weights passed through the same spacing model.** Our best recommendation is the fraction-rounded, content-backed pilot estimates, while retaining frequency as an initial signal rather than mass-replacing the old scores with the more complex estimator. The [decision artifact](reference/mathacademy/encompassing-analysis-2026-10-11/calibration-pilot/content-decisions.json) records the exact inputs and rounding.

## Revised findings: magnitude, spacing, and prior state

Analysis date: October 11, 2026, local time. The frozen observation reports contain 1,247 foundations, 666 linear, 593 multivariable, and 527 differential activities. New runner activity is not included. Each account uses its own observations, history, graph snapshot, timing comparisons, and direct-review controls.

**The binary rising-activity frequency is useful as a descriptive statistic, but it should not be stored as intrinsic encompassing coverage.** It loses jump magnitude and treats early and well-spaced practice as equally informative. The prepared frequency transaction is superseded and remains uncommitted. Its exact original request and noncommitting preview have been preserved.

The stronger working explanation for inconsistent rises is **spacing plus target state**, including fractional position within a display band and intervening practice. Current task accuracy and KP selection can matter, but they do not explain the matched examples by themselves. Timing is an association in these captures, not a randomized causal result; it also does not explain every difference.

### First calibration check: unexplained direct-review changes

The direct-review audit came before fitting encompassing weights. It verified **six passed direct reviews whose reviewed topic decreases in color category**, and **two fully correct direct reviews with 1→6 changes**, against the saved raw HTML, same-account/course/topic identities and outcome records. No pairing or color-parsing bug was found. Direct coverage is already 1, so changing an encompassing weight cannot resolve these observations. The [audit](reference/mathacademy/encompassing-analysis-2026-10-11/calibration-pilot/direct-anomalies.md) retains all eight in the calibration evidence.

Positive retention credit at successful completion cannot lower repetitions under the local model. With default quality 1, prior accuracy 0.8 and speed exponent 2, its maximum successful increment is 1.5625 repetitions; a 1→6 jump is incompatible with that bound under unit-width repetition categories. These are model mismatches, not evidence that direct coverage should exceed 1. The large-jump objection depends on the proposed display scale; the decrease also contradicts any fixed monotone mapping from repetitions when repetitions only increase.

Our best explanation for the decreases is a displayed mastery value that is recalculated with ability/performance and sometimes changes across many topics. Every decreasing target also fluctuates nearby; one reviewed topic falls during a batch with 72 falling targets. A fixed per-question penalty explains this less well. For the perfect jumps, the best explanation is a large quality/ability-sensitive update to an already-known topic mapped into the top category. Neither perfect-jump target has a captured prior direct-practice time, so neither estimates a spacing multiplier. The pilot uses a separately calibrated signed residual to accommodate these changes and reports their prediction errors instead of allowing encompassing weights to absorb them.

### What was actually measured

The capture visits `/courses/<course>/progress`. Saved HTML contains server-rendered `.topicCircle` RGB colors, without numeric repetition, memory, interval, or due-state values. The fetched public [course-progress.js](https://mathacademy.com/js/course-progress.js) only toggles expanded units. The official description links darker shading with more successful practice and explains early-practice discounts, but does not supply the current server page's numeric color thresholds. See [How Our AI Works](https://www.mathacademy.com/how-our-ai-works).

An older **different** graph renderer maps numeric repetition values 1–5 to the same blue palette and uses dark blue as its default case. That default does not prove a `>=6` numerical threshold, and it cannot be transferred to the current server-rendered circles. The [earlier renderer investigation](reference/fire-source-evidence.md#recovered-display-mappings) records this distinction. Consequently, the captured local labels 0–6 are display categories. A 1→6 observation is retained as a much larger palette change, but is not asserted to be five repetitions. The darkest color has no higher visible category; this is a display ceiling, not proof of a specific latent repetition ceiling.

For each exposure, the new analysis saves the starting category, ending category, signed movement and positive movement:

$$
d_i=b_i^+-b_i^-,\qquad j_i=\max(0,d_i),\qquad
\overline j=\frac{1}{N}\sum_i j_i.
$$

The signed mean remains separate; decreases are not converted into positive credit or silently dropped. Flat observations remain included. These differences measure **ordinal palette steps**, whose distances are an explicit approximation, not known equal repetition increments.

| Account | Previously nominated pairs | Eligible exposures | Rising exposures | Positive palette-step total | Rises spanning several categories |
|---|---:|---:|---:|---:|---:|
| Foundations | 936 | 1,908 | 1,017 | 1,405 | 258 |
| Linear | 274 | 518 | 297 | 376 | 54 |
| Multivariable | 372 | 741 | 399 | 539 | 81 |
| Differential | 207 | 274 | 219 | 380 | 75 |

Thus the old binary statistic discarded appreciable movement in every account. The differential sample contains 380 positive steps across only 219 rising exposures. Neither number alone is a coverage fraction.

All **1,789** previously nominated account-specific relationships, including **651 with one exposure**, retain a magnitude/timing profile. There is no minimum activity-count exclusion. Their 533 distinct source topics remain observed candidates; after withdrawing the frequency weights, that number should not be presented as 533 topics with newly calibrated coverage weights.

### The timing comparison

The implementation is [analyze_encompassing_timing.py](capture/scripts/analyze_encompassing_timing.py). It reconstructs complete before/after snapshots using the original account/course/topic matching, duplicate handling, grade requirements and single-activity isolation checks. It includes unchanged prerequisite targets, rather than selecting only pairs that rose. That produces 21,755 foundations, 10,998 linear, 7,683 multivariable, and 3,984 differential eligible prerequisite-target observations. These targets are structural prerequisites; the analysis does **not** assume that every prerequisite is encompassed.

All clocks are computed from information captured **before** the activity:

- **Target-direct age:** hours since the target's last captured passed, fully graded lesson or review. This is the main descriptive comparison; it does not measure time since all implicit credit.
- **Source age:** hours since the last captured activity on the source, regardless of outcome.
- **Potential target-practice age:** hours since a passed, fully graded activity on the target or any prerequisite-graph descendant. This is an intentionally broad structural proxy. A descendant need not actually practice the target.
- **Visible-change age:** hours since any captured target-color change. This is a display-history marker, not a memory timestamp.

Unknown prior history stays unknown; it is never replaced with zero. Missing practice can make a recorded age longer than the true age. Assessment tasks without a single known topic cannot supply topic-specific clock updates. Absolute hours are not the same as lateness relative to the target's unknown review interval.

#### Direct reviews show a substantial spacing effect

The following table holds **starting category = 1** and **accuracy = 60%** fixed. Every activity is a passed direct review on its own source/target topic. Each cell is mean positive palette movement, followed by its activity count. It does not pool accounts.

| Account | <6 hours | 6–12 hours | 12–24 hours | 24–48 hours | 48+ hours |
|---|---:|---:|---:|---:|---:|
| Foundations | 0.027 (37) | 0.269 (156) | 0.553 (190) | 0.699 (83) | 0.800 (10) |
| Linear | 0.000 (37) | 0.406 (69) | 0.500 (74) | 0.714 (56) | 1.000 (1) |
| Multivariable | 0.036 (28) | 0.270 (63) | 0.523 (65) | 0.829 (35) | — (0) |
| Differential | 0.000 (16) | 0.280 (50) | 0.465 (43) | 0.442 (43) | 1.000 (2) |

**A flat early exposure is weak evidence for low encompassing coverage.** Even direct practice often leaves the display unchanged when done recently. The differential 24–48-hour group also illustrates why elapsed hours should not become a universal multiplier: the trend is not uniformly increasing, and later groups have sparse support.

To check whether the trend is just a change in topic mix, the analysis also compares repeated observations within a fixed context:

$$
g=(s,t,b^-,\text{activity kind},\text{exact accuracy},\text{capture pipeline}),
\qquad x_i=\log_2(1+h_i/(1\text{ hour})).
$$

For one clock, subtract each context's mean and fit:

$$
\widehat\beta=\frac{\sum_i(x_i-\overline x_g)(d_i-\overline d_g)}
{\sum_i(x_i-\overline x_g)^2}.
$$

For multiple clocks, use the corresponding demeaned least-squares system. Only repeated contexts identify this timing coefficient; singleton observations still remain in the overall results and relationship profiles. This is not an activity-count cutoff on relationships.

| Account | Direct-review observations identifying target-age association | Palette steps per doubling of `1 + hours` | Within-context variance explained |
|---|---:|---:|---:|
| Foundations | 237 | +0.308 | 32.5% |
| Linear | 104 | +0.203 | 35.5% |
| Multivariable | 76 | +0.196 | 31.4% |
| Differential | 76 | +0.274 | 54.4% |

These are descriptive associations, without independence-based confidence intervals. Multiple targets can share a task, topics repeat, and practice scheduling is not random. Subtracting same-activity mean movement among nonancestor targets barely changes these direct-review coefficients. Removing darkest-color endpoints also leaves them effectively unchanged. The spacing finding therefore does not depend on interpreting 1→6 as a precise numerical jump.

#### Suspected encompassing relationships show a weaker, more confounded effect

Within the previously nominated source/target pairs, using the same fixed contexts:

| Account | Target-direct-age coefficient | Identifying exposures | Source-age coefficient | Identifying exposures |
|---|---:|---:|---:|---:|
| Foundations | +0.153 | 174 | +0.213 | 279 |
| Linear | +0.136 | 42 | +0.182 | 44 |
| Multivariable | +0.214 | 76 | +0.351 | 80 |
| Differential | −0.378 | 6 | +0.555 | 14 |

The differential target-age estimate changes sign when darkest endpoints are omitted; six observations cannot support a stable adjustment. When target age and source age are fitted together, much of the target-age association moves to source age in foundations and linear. These clocks are correlated with repetition sequence, intervening activity and changing learner state. **The evidence supports including history and spacing, but does not identify a universal hours-based correction for implicit credit.**

Across *all* structural prerequisite observations, rather than only nominated pairs, timing associations are much smaller. Most such observations are flat because prerequisite status does not establish actual practice coverage. This is also why selecting only pairs that ever rose exaggerates average response.

### Matched activities: accuracy and KP outcomes do not explain everything

These saved comparisons hold source, target, starting category, activity kind, overall accuracy **and per-KP correct/incorrect counts** fixed. They are separate within-account comparisons, not pooled evidence. Question wording, difficulty, answer order and hidden state can still differ.

| Account and relationship | Earlier observation | Later observation | Hours since direct target practice |
|---|---|---|---|
| Foundations: 864→863, inverse matrices | `13991694`: 2→2 | `14033015`: 2→3 | 6.07 vs 34.98 |
| Multivariable: 2110→1951, line-integral theorem→potential functions, lessons | `14059357`: 1→1 | `14119320`: 1→6 | 5.77 vs 59.20 |
| Multivariable: same relationship, reviews | `14065132`: 1→1 | `14068004`: 1→3 | 10.49 vs 13.23 |
| Differential: 3674→1163, logistic-growth equation→models | `14063765`: 1→1 | `14071481`: 1→3 | 12.16 vs 22.46 |

For the multivariable lessons, all three KPs have 3/5 correct in **both** activities. The late activity is also 47.13 hours after the previous source activity and 25.29 hours after the last structurally possible target practice, versus 5.77 hours for the early lesson's target-practice age. The target was directly reviewed between those lessons, and there were 23 visible target changes between the previous eligible source exposure and the late lesson. Thus the late 1→6 must not be treated as uninterrupted accumulation across five source activities.

For the two multivariable reviews, both activities answer the explicitly linked “potential function not given” KP incorrectly on both of its questions. The later activity still produces a rise. This does not prove that the linked KP earned credit, but it defeats a simple explanation in which that KP's correct count alone determines the displayed effect.

A counterexample remains: multivariable 3360→3711 has matched lesson/KP counts and 1→1 versus 1→2 with direct-target ages only 0.27 versus 0.35 hours. Timing alone cannot explain every difference. Fractional starting position, performance ordering, target historical ability, other practice and display/model updates remain relevant.

The older KP comparison selected repeated mixed-response pairs to find useful examples. That selection is **not** used as a minimum-support gate in this revised analysis. Many captures deliberately target 60% correctness, leaving little accuracy variation from which to estimate performance coefficients. Missing imported key-prerequisite annotations are not proof that a KP omits a skill.

### Why substituting jump totals still does not produce a sound weight

For the four worked relationships:

| Account, source→target | Old rising frequency | Positive steps per eligible activity |
|---|---:|---:|
| Foundations, 4387→48 | 1.00 | 1.00 |
| Linear, 1961→2211 | 0.75 | 1.00 |
| Multivariable, 2110→1951 | 0.40 | 1.40 |
| Differential, 3245→3668 | 0.75 | 0.75 |

Magnitude materially changes the multivariable evidence. Simply clamping 1.40 into a maximum weight of 1.00 would erase the unresolved scale mismatch rather than explain it.

The revised script actually tests a direct-review normalization, rather than assuming it works. For each exposure, select same-account direct-review controls with the same starting category, exact accuracy and target-age bin. Prefer the same target when any such control exists; otherwise retain an explicitly labeled same-account control. Unknown ages are not matched. Let $C_i$ be the selected controls and:

$$
\mu_i=\frac{1}{|C_i|}\sum_{c\in C_i}\max(0,d_c),\qquad
R=\frac{\sum_{i:C_i\ne\varnothing}j_i}{\sum_{i:C_i\ne\varnothing}\mu_i}.
$$

| Account | No matching controls | Matched controls but zero total gain | Positive-anchor ratio >1 | Positive-anchor ratio ≤1 |
|---|---:|---:|---:|---:|
| Foundations | 394 | 277 | 228 | 37 |
| Linear | 110 | 97 | 54 | 13 |
| Multivariable | 177 | 25 | 97 | 73 |
| Differential | 172 | 13 | 13 | 9 |

A ratio is available for only the supported subset of exposures; it is not imputed for the missing ones. Starting categories 3–5 have particularly poor direct-review support in this short history. Lesson source exposures also lack a guaranteed comparable direct-review dose. Among the relationships with positive anchors, 392 of 524 ratios exceed one. Candidate selection on a rise, different target learning speeds, hidden memory and threshold phase all prevent this straightforward normalization from being an intrinsic coverage estimate. Even a ratio inside `[0,1]` is not automatically valid coverage. The ratios are retained **without clamping** as calibration diagnostics.

### The better estimation model

The useful distinction is between a **stable curriculum coverage weight** and the **state-dependent amount of repetition earned**. A practical model for a passed source activity is:

$$
\Delta r_{a,t,i}=w_{s\to t}\,Q_i\,v_{a,t,i}\,D(M^-_{a,t,i}),
$$

subject to target eligibility, the slow-implicit gate, and credit arriving through other encompassing paths. $Q$ is task-quality credit, $v$ is target learning speed, and $D$ is an early-practice discount. None of these is earned XP. The [XP reports](reference/xp-docs/earned-xp-formula-report.md) estimate task rewards/workload, not a repetition-credit conversion.

Memory immediately before activity depends on the last **actual** retention update, not just the last direct review:

$$
M^-_{a,t,i}=M^+_{a,t,j}\,2^{-\Delta t/H_{a,t,j}}.
$$

The current local engine's illustrative discount is:

$$
D(M)=\left[\operatorname{clip}\left(
\frac{M_{\mathrm{restored}}-M}{M_{\mathrm{restored}}-M_{\mathrm{due}}},0,1\right)\right]^\gamma.
$$

This is an explicit **local policy**, not a recovered Math Academy numerical rule. The published FIRe structure establishes early discounting and target-specific learning speed; see [chapter 29](reference/The%20Math%20Academy%20Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md). A longer gap can reduce memory, reduce the discount and increase the earned increment with the same coverage and correctness. It does not imply that unlimited lateness generates unlimited positive credit.

The observation model should use category intervals:

$$
b=F(r),\qquad r\in[\tau_b,\tau_{b+1}).
$$

The current thresholds are unknown. **If** uncensored bands were unit-width repetition intervals, a jump $d$ would constrain the increment to approximately $(d-1,d+1)$, rather than assigning exactly $d$ repetitions. A flat passed exposure could still contain nearly one interval's positive credit. A darkest endpoint would supply a lower constraint only **if** its actual lower threshold were known. That conditional model cannot be claimed as a recovered display mapping.

For a continuous run with no intervening retention-changing work, magnitude would constrain:

$$
J_{\mathrm{net}}-1
< w_{s\to t}\sum_i Q_i v_{a,t,i}D(M^-_{a,t,i})
< J_{\mathrm{net}}+1,
$$

under the same unit-width assumption. The effective denominator is the sum of state-adjusted practice doses, **not** the count of all activities. Intervening direct practice, other implicit practice, failed work, missing history, endpoint discontinuities and changes in the displayed model must be represented or split into separate runs. A run is not declared continuous merely because two captured endpoints agree.

The practical recommendation is to seed coverage from the actual mathematical component use in source KPs/questions, then refine it using a target-specific ordinal response model with these spacing and state factors. Keep one-activity relationships as estimates with broad uncertainty; sparse support calls for a content prior, not deletion. Compare plausible threshold/half-life/speed scenarios and retain a range where a point weight is sensitive. This does not require recovering private parameters perfectly, but does require declaring the scale assumptions. The present script computes all magnitude/spacing profiles and checks the proposed direct-review scale; it **does not yet fit that full latent-state model or issue replacement operational weights**.

### Engine and schema implications

Keep `:topic/encompasses` as the stable source-topic→component-topic relationship. Existing KP key prerequisites provide useful evidence about actual component use and remediation. These captures do not establish that encompassing belongs exclusively to a question or KP.

Keep target-specific memory/interval discounting. The evidence argues against using an equally weighted activity counter to infer coverage or using the source's clock for all receiving targets. Existing `:progress/memory`, `:progress/memory-at`, `:progress/interval-days`, `:progress/repetitions`, separate accuracy channels and `:progress/last-direct-at` cover the operational concepts needed. `memory-at` is an anchor, not necessarily the last successful practice time; `last-direct-at` deliberately does not track implicit practice.

Do not tune the exact half-life, interval-growth, discount exponent, speed exponent, failure multiplier or slow-implicit threshold from these colors alone. The observations establish a useful spacing trend, but not those numerical values. Likewise, XP workload and task awards should not become retention multipliers merely because they are observed.

For future evidence, preserve account/course/topic identity, raw color, before/after observation times, activity completion time, actual grades and KP identities, and each retention-credit update's timestamp and breakdown when our engine supplies it. If numeric upstream repetitions/memory/intervals are legitimately exposed, capture them as observations separate from our operational state. These are evidence/audit fields; no shared-topic attribute needs to store an account's current band or clock. No operational schema or engine values were changed in this investigation.

### Artifacts, transaction status, and reproduction

- [Foundations magnitude/timing results](reference/mathacademy/encompassing-analysis-2026-10-11/timing-magnitude/foundations.json)
- [Linear results](reference/mathacademy/encompassing-analysis-2026-10-11/timing-magnitude/linear.json)
- [Multivariable results](reference/mathacademy/encompassing-analysis-2026-10-11/timing-magnitude/multivariable.json)
- [Differential results](reference/mathacademy/encompassing-analysis-2026-10-11/timing-magnitude/differential.json)
- [Superseded transaction marker](reference/edb-math/imports/encompassing-weights/2026-10-11/superseded.json): exact request and speculative preview preserved; no submission occurred. The preparer refuses to regenerate that superseded bundle.
- [Original frequency methodology](reference/mathacademy/encompassing-analysis-2026-10-11/frequency-method-v1.md), retained for audit.

Each account JSON contains the frozen source-report hash, reconstructed observations, clocks, all 1,789 relationship profiles across the four files, direct controls, matched-context fits, darkest-end sensitivity and shared-movement diagnostics. No outcomes or calibration data are pooled between accounts.

```bash
PYTHONPATH=capture python3 -m scripts.analyze_encompassing_timing \
  reference/mathacademy/encompassing-analysis-2026-10-11
```

Validation: 23 targeted analysis/preparation tests pass, including jump magnitude, account isolation, unknown ages, fixed starting-category controls, single-exposure preservation, zero direct-review anchors and rejection of superseded preparation. The original report and prepared request remain intact as evidence of the superseded calculation.

## Separating crossing frequency, jump size, and FIRe policy

**The original crossing-frequency statistic remains useful as an initial score and an observation channel.** The mistake was identifying it directly with intrinsic encompassing coverage. The user's proposed separation—frequency for relationship strength, magnitude for spacing—is a useful starting structure, provided both channels share the timing/state model.

For positive palette movement $J=\max(0,b^+-b^-)$:

$$
E[J]=P(J>0)\,E[J\mid J>0].
$$

That identity separates occurrence and size statistically; it does not assign them independent causes. Spacing can turn a flat observation into a rise, as well as enlarge a rise. Coverage can increase jump size as well as crossing frequency. Linear-account direct reviews at 60% accuracy and starting band 1 rose in 0/37 observations within six hours, versus 40/56 at 24–48 hours. Direct coverage is 1 in both groups. Consequently, the unadjusted crossing frequencies cannot themselves be coverage weights.

Under an explicit approximation of unit-width bands, uniformly distributed fractional starting positions, no negative interference and effective increments $x_i<1$:

$$
x_i=w_{s\to t}d_i,\qquad d_i=Q_i v_{a,t,i}D(M^-_{a,t,i}),
\qquad P(\mathrm{rise}_i)\approx w_{s\to t}d_i.
$$

An initial method-of-moments estimate is then:

$$
\widehat w_{\mathrm{seed}}=\frac{K}{\sum_i d_i},
$$

rather than $K/N$. This is a starting approximation, not the general maximum-likelihood estimate. The exact Bernoulli likelihood for this approximation includes both $wd_i$ and $1-wd_i$; larger increments need a full category-transition model. For example, one rise across four exposures with estimated full-coverage doses $0.1,0.2,0.3,0.4$ gives a seed of 1.0, not 0.25. That example assumes the doses and scale; it is not an estimate for one of the captured pairs.

Use magnitude to constrain the same dose model. Once almost every exposure rises, crossing frequency stops distinguishing stronger effects, whereas larger transitions still carry information. Fit a joint likelihood of the observed transitions; alternatively factor it into the probability of a rise and the distribution of its size conditional on rising. Do not count the rise indicator twice by adding an independent binary likelihood to a full transition likelihood that already includes it. Retain declines and background movement in a residual/interference model rather than explaining every change with positive encompassing credit.

### How the actual policy parameters enter

The shared state-update formulas below were traced through [core.rs](engine/rust/core.rs) and [calibration.rs](engine/rust/calibration.rs). The task-quality behavior described later first refers specifically to [runtime.rs](engine/rust/runtime.rs); the progressive learning API in [learning.rs](engine/rust/learning.rs) and [retrieval.rs](engine/rust/retrieval.rs) constructs different credit events. A replay must identify its event path and initialization convention explicitly. Defaults refer to the checked-in [default policy](schema/engine/4-default-fire-policy.edn), not a new read of live database settings.

$$
H(r)=\min(H_{\max},H_0 g^r),\qquad
m(t)=M\,2^{-\Delta t/H},\qquad
s=\operatorname{clip}\left((a/a_0)^\beta,s_{\min},s_{\max}\right).
$$

For passed, admitted, ungated practice, with default decay-before-add ordering:

$$
u=QwD(m),\quad r'=r+s u,\quad M'=m+u,\quad
H'=H(r'),\quad t_{\mathrm{due}}=t+H'\log_2(M'/\theta).
$$

If $M'\le\theta$, the topic is already due. Notice that repetition gain uses speed, while the memory increment uses raw credit $u$. Repetitions are **learner state**, not another independent policy weight; they determine subsequent half-life. Implicit updates change the target's memory anchor too.

| Policy attributes | Checked-in defaults | Role and practical estimation treatment |
|---|---|---|
| `base-half-life-days`, `interval-growth` | 1 day, 2 | Set the half-life curve. Start by fitting one timing scale from direct practice; hold growth near its prior until higher-repetition observations support a separate estimate. At one repetition level, only their combination is well constrained. |
| `initial-retention`, `review-threshold` | 1, 0.5 | Define memory scale and when reviews become due. Keep these anchors fixed in the first fit; varying them together with half-life and dose creates unnecessary ambiguity. |
| `early-practice-discount-power` | 1 | Shapes the early-practice credit curve. Fit or compare a small set of values jointly with timing scale and starting-memory uncertainty. More memory and a steeper exponent can both explain early flats. |
| `initial-accuracy`, `accuracy-update-rate`, `speed-exponent` | 0.8, 0.2, 2 | Set fallback ability, response to answer history, and its effect on repetition speed. Replay ordered answers; initially keep these near their defaults because most captured reviews have exactly 60% correctness. |
| `minimum-speed`, `maximum-speed` | 0.25, 4 | Bound speed. Hold fixed initially. With prior 0.8 and exponent 2, the maximum reachable speed is actually $(1/0.8)^2=1.5625$, so the configured upper bound 4 cannot explain a large jump under these defaults. |
| `gate-slow-implicit` | true | Suppresses positive implicit retention credit while target speed is below 1. Compare gated and ungated replay after reconstructing target ability; source accuracy alone does not determine the gate. |
| `overdue-failure-slope`, `maximum-failure-multiplier` | 1, 4 | Increase negative credit for overdue failures. Calibrate from failed work and subsequent behavior, not successful large jumps. Frozen full audits have only 4/1/2/7 failed activities in foundations/linear/multivariable/differential. |
| `maximum-half-life-days` | 36,500 | Long-term numerical cap. Keep fixed; the short capture histories do not identify it. |
| `retention-update-order` | decay-before-add | Model convention, not a freely compensating multiplier. Keep fixed while fitting; compare the other convention as a separate model if needed. |
| `future-horizon-days` | 7 | Affects ranking by how much activities postpone future reviews. It does not multiply credit or decay. Fit against offered task choices and scheduling behavior, after retention calibration. |
| `question-selection-weights` | Activity-specific distributions | Affect which difficulty bands are sampled and thus the practice content. Fit from question draws/continuation rules, not color jumps. |

There are very few direct review controls starting in bands 3–5: foundations 17, linear 1, multivariable 0, differential 2. This particularly limits separate estimation of interval growth. Offered or completed review times are also not exact due timestamps: remediation, candidate filtering, fresh-question availability and learner selection intervene. They provide additional scheduling evidence without becoming literal half-life measurements.

### Implementation paths and coverage semantics

**In the `runtime.rs` path, task quality is not automatically task accuracy.** Every graded native question first updates ability. Lesson/review retention is applied at completion with the task's pass/fail sign and mean graded `task-item/performance`, whose input default is 1.0. Incorrect graded answers are included in that mean. There is no current policy translating a 60% review into a particular fractional dose or a perfect review into a bonus dose. Assessment/multistep retention is applied per question with performance divided by the activity's question count for that topic. First successful learning also has a special initialization: $r=sQ$, $M=M_0$, without the ordinary spacing discount. See [runtime.rs](engine/rust/runtime.rs#L989).

**The progressive learning API uses another event path.** [retrieval.rs](engine/rust/retrieval.rs#L169) uses `Event::default()` quality 1: an assessment question receives one unnormalized signed retention event, while a review receives retention at completion. It does not calculate the `runtime.rs` mean performance or per-topic assessment denominator. Current progressive assessment validation requires one question per topic, so the normalization difference does not change the dose for a valid unit-performance assessment under that constraint, but the event construction remains distinct. Progressive lesson completion in [learning.rs](engine/rust/learning.rs#L1937) also uses quality 1. Its loader admits partial imported repetition records with zero memory, no invented answer history and `learned=false`; successful first local learning then preserves those banked imported repetitions by adding them back after initialization. That preservation is additional to the shared core's $r=sQ$ initialization. A replay that mixes these paths can manufacture a credit or initial-state discrepancy and incorrectly attribute it to half-life or encompassing coverage.

Thus a configurable task-quality mapping is a candidate addition if we want current-task accuracy to affect credit beyond its existing effect on ability. It should be estimated against direct practice first. Treating accuracy as $Q$ silently would change the model and let encompassing weights compensate for that change. No such policy was added here.

**Coverage affects future speed as well as current credit.** For an encompassing weight $w$, each propagated accuracy observation uses step size $\alpha_w=1-(1-\alpha)^w$. Correct answers propagate toward components; incorrect answers propagate toward encompassing dependents. Both assessment and practice channels contribute equally to target effective accuracy. Therefore a source at 60% can improve a component's ability estimate, and the incoming-credit gate can open later.

For example, start a target at assessment accuracy 0.8 and practice accuracy 0.6, with $\alpha=0.2$ and $w=0.5$. Suppose each source review supplies three correct fractional target updates and no other intervening target evidence. After one, two and three reviews, target speed is 0.895, 0.994 and 1.068. The first two completion updates are gated and the third is eligible. This produces a possible flat–flat–rise pattern with fixed coverage, even before considering spacing or display thresholds. It is a calculation from our current engine, not evidence that Math Academy uses this exact gate.

**An explicit edge overrides inferred coverage for the same source and target.** [Graph::coverage](engine/rust/core.rs#L188) uses the largest path product for inferred pairs, but replaces that result when an explicit source→target edge exists. For example, A→B at 0.8 and B→C at 0.8 imply A→C coverage 0.64; adding an explicit A→C edge at 0.2 reduces A→C coverage to 0.2. The override can also affect further propagation through C. Thus inserting a low estimated direct edge is not merely adding evidence to the strongest-path calculation. Fit a coherent graph, compare effective coverage before and after proposed insertions, and reserve direct edges for component relationships supported by the mathematical content. Every observed indirect effect need not become another direct edge.

### A concrete spacing example

Start independent scenarios at $r=1$, $M=1$, speed 1, quality 1 and encompassing weight **0.5**, using the checked-in policy. The starting half-life is $1\times2^1=2$ days.

| Time since the last memory anchor | Early discount | Repetition credit | New half-life | Next review due after this activity |
|---|---:|---:|---:|---:|
| 6 hours | 0.166 | 0.083 | 2.118 days | 2.118 days |
| 24 hours | 0.586 | 0.293 | 2.450 days | 2.450 days |
| 48 hours | 1.000 | 0.500 | 2.828 days | 2.828 days |

The coverage weight is the same in all rows. These are separate starts from the same state, not a three-activity sequence. They show how spacing changes both credit and the next review interval. Whether any increment crosses a visible band still depends on the initial fractional position and display thresholds. Longer spacing here removes an early discount; once it reaches 1, waiting still longer does not create an unlimited positive multiplier.

### Recommended fitting procedure with the existing evidence

1. **Audit the unexplained direct reviews first.** Verify the six reported decreases and two perfect 1→6 reviews. With direct coverage fixed at 1, test whether a provisional observation model can accommodate them, including an explicit residual component if needed. State which behavior remains unexplained before fitting coverage.
2. **Anchor and fit a small direct-practice model.** Keep memory normalization, most policy parameters and update order fixed; distinguish new learning, imported-state initialization and later practice. Declare the credit-event path. Fit one timing scale and, if supported, discount shape within each account, with sensitivity checks for display thresholds and darkest endpoints. Reconstruct ability in answer order and preserve unknown initial memory and band position.
3. **Fit a representative set of relationships.** Use crossing frequency as a starting value, adjust for estimated practice dose where supported, and use mathematical component coverage as a prior. Keep single-exposure pairs as provisional estimates with broad uncertainty. A flat early observation supplies little evidence for low coverage.
4. **Replay and refine the limited pilot.** Replay relevant captured practice, including implicit memory and accuracy updates, assessments, failures and relearning under the declared event semantics. Fit against both crossings and jump sizes, then refine only the small selected policy subset. Apply maximum-product inference **with explicit-pair overrides**, and inspect effective coverage changes before proposing direct edges.
5. **Compare later predictions with the original scores.** Hold later captures out of fitting. Compare the pilot and original frequency scores on the same observations within each account, using crossing predictions and, where the model supplies them, full transition predictions. Report direct-review residuals as well as relationship predictions. Check whether errors track spacing, accuracy or KP mix before adding KP-specific weights. If several settings perform similarly, retain a practical prior-backed estimate and a sensitivity range. Do not describe the fitted weights as operationally improved until this comparison supports that claim.

This is a feasible approximation strategy, not a requirement for perfect evidence. All four accounts remain independent during fitting; they can yield separate candidate settings and coverage estimates. Selecting one shared curriculum estimate later is a separate decision from pooling learner histories. The old prepared transaction remains superseded because its unadjusted values have not undergone this calibration.

Two stale descriptions in `1-fire-policy.edn` were corrected: initial accuracy is no longer described as topic difficulty, and speed sensitivity now refers to learner-topic accuracy. These are documentation corrections; no policy values or database records changed.

</details>

