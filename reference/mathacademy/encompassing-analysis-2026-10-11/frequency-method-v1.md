> Superseded. This is the original frequency-only methodology and transaction documentation, retained for audit. See /encompassing-report.md for the corrected analysis.

# Encompassing weights estimated from captured progress bands

Date: 2026-10-11. Results below refer to the saved frequency reports generated at approximately `2026-10-11T23:38:35Z`.

The first-pass encompassing estimate is the fraction of eligible activities on a source topic that produced a visible upward band change on a component topic:

$$
\widehat w_{a,s\to t}=\frac{\text{activities with an upward target-band change}}{\text{eligible activities on the source topic}}.
$$

Flat activities remain in the denominator. **There is no minimum repeat-count cutoff: one-activity and two-activity estimates are included.** The account, sample size, activity sequence, and intervening target changes accompany each estimate.

This is a practical frequency-based starting weight. Its scale assumption is that a full-credit activity corresponds to one comparable visible upward transition. The measured quantity is crossing frequency; treating it as intrinsic skill coverage is an approximation.

## Results and coverage

| Account | Distinct source topics with estimates | Relationship estimates | Estimates with 1 activity | Estimates with 2 activities | Estimates with 3+ activities |
|---|---:|---:|---:|---:|---:|
| Foundations | 281 | 936 | 272 | 397 | 267 |
| Linear | 112 | 274 | 84 | 140 | 50 |
| Multivariable | 127 | 372 | 141 | 131 | 100 |
| Differential | 85 | 207 | 154 | 41 | 12 |
| Account-specific estimate totals | — | **1,789** | **651** | **709** | **429** |

A source topic is the topic whose activities potentially provide implicit practice to another topic. A relationship estimate is one directed source-to-component pair for one account. A topic can have several relationship estimates.

Let $P_a$ be the set of relationship estimates for account $a$, and let:

$$
S_a=\{s:\exists t\text{ such that }(s,t)\in P_a\}.
$$

The distinct source-topic coverage is:

$$
\left|\bigcup_a S_a\right|=533,
\qquad
\frac{533}{2,977}\times100\approx17.9\%.
$$

The denominator is the **full 2,977-topic catalog in the curriculum snapshots used by this analysis**, rather than the topic count of a single account's active course. The numerator means that each of those 533 topics has at least one estimated outgoing relationship; it does not mean that every outgoing encompassing relationship for that topic has been estimated.

Account source-topic counts overlap, so adding 281, 112, 127, and 85 would double-count some topic identities. The 1,789 relationship estimates remain account-specific and are summed without merging their weights. Counting either end of a relationship gives 797 distinct topics: 533 source topics, 427 component topics, with overlap between those sets.

## Data sources and account separation

The implementation is split between:

- [analyze_encompassing.py](capture/scripts/analyze_encompassing.py): discovers activities, matches complete before/after snapshots, checks timing, and prepares per-account source/target exposures.
- [estimate_encompassing_frequency.py](capture/scripts/estimate_encompassing_frequency.py): calculates the frequencies, activity numbers, waiting counts, proposed weights, and diagnostics documented here.
- [progress.py](capture/scripts/progress.py): maps captured colors to local ordinal bands.

The current capture pipeline saves each account's baseline in `.local/capture/<account>/progress.json` and activity evidence under `reference/mathacademy/capture/<account>/<task>/`. The analysis uses the activity's saved `progress-before.json`, `post-activity.json`, `activity.json`, and `content.json`, rather than substituting a later mutable baseline. The associated `progress-comparison.json` records the capture comparison; the analysis reconstructs observations from complete snapshots so unchanged topics also contribute to the denominator.

Older evidence is read from:

```text
reference/mathacademy/question-capture/<task>/knowledge-state/*-completed.json
reference/mathacademy/question-capture-workers/<account>/<task>/knowledge-state/*-completed.json
```

The first older location belongs to foundations. Legacy `state.json` supplies the source topic, task kind, observed question grades, completion outcome, and previous snapshot reference.

An activity is identified by **account and task ID**. If both capture pipelines saved the same account/task, the current pipeline takes precedence. Different accounts' task IDs are never used to merge observations.

Within an account, snapshots first match **course ID and topic ID**. If a topic appears in several courses and all its before/after band pairs agree, it contributes one topic observation. Conflicting course displays are excluded. Missing topics, unknown colors, and duplicate course/topic identities are not interpreted as progress losses.

Each account's graph is taken from one cached curriculum context, selected by highest saved EDB basis. The four analysis reports record bases 1092, 1177, 1067, and 1076 for foundations, linear, multivariable, and differential respectively. Graph paths, bases, and hashes are retained in those reports. All contain the 2,977-topic catalog used for the coverage denominator.

**Outcomes, denominators, background comparisons, and uncertainty calculations are separate for each account.** The union used for the 533-topic count combines topic identities only.

## Observation and relationship selection

The local palette assigns white to band 0 and the six progressively darker blue colors to bands 1 through 6. These integers are display categories. They are not known integer repetition values.

For a source activity to contribute a positive-practice exposure:

1. It must be a lesson or review with a known source topic and a saved baseline.
2. Completion must be observed as passed. All saved presentations must have an observed grade of `Correct`, `Incorrect`, or `Skipped Question`. All-correct performance is **not** required.
3. The target must have a known band in both snapshots, with agreeing course displays.
4. The before/after observation interval must be positive and at most 1,800 seconds. It must contain exactly one known same-account activity boundary, belonging to this activity.
5. A current-pipeline baseline must precede the first captured answer. Reads marked late or recovered after interruption are excluded from single-activity attribution.
6. The target's starting band must be between 1 and 5 inclusive.

For legacy captures, the start of post-activity snapshot collection is used as the activity boundary proxy. That is less precise than the current pipeline's capture-completion marker. Courses are read sequentially, and their actual observation timestamps are used.

Starting at band 6 is excluded from positive estimation because further credit cannot produce a higher display band. Starting at band 0 is treated as placement/admission rather than ordinary retention accumulation. **Flat observations beginning in bands 1–5 are included.** Downward observations beginning in those bands also remain in the denominator but do not count as upward crossings.

The initial analyzer nominates source/target pairs after an isolated visible rise. The frequency report then keeps nominated pairs whose target is an ancestor prerequisite of the source, with at least one upward crossing among eligible passed exposures. Ancestors at any prerequisite distance are permitted; there is no distance-two cutoff in this estimator.

For each retained pair, **all** eligible passed exposures are counted, including ones before the first crossing and ones after the last crossing. One observed exposure is enough to produce an estimate. Pairs with no eligible upward crossing are left unestimated by this positive-relationship method; they are not assigned a zero encompassing attribute. This discovery rule favors relationships that became visible in the captured sample.

## Weight equations

Fix an account $a$, source topic $s$, and component topic $t$. Sort the pair's eligible exposures chronologically and index them $i=1,\ldots,N$.

Let $b_i^-$ and $b_i^+$ be the target's band immediately before and after exposure $i$. Define:

$$
I_i=\mathbf{1}[b_i^+>b_i^-],
\qquad
K=\sum_{i=1}^{N}I_i.
$$

The unrounded frequency estimate and proposed starting coverage weight are:

$$
\widehat w_{a,s\to t}=\frac{K}{N},
\qquad
w^{\mathrm{proposal}}_{a,s\to t}
=\frac{\operatorname{round}(20\widehat w_{a,s\to t})}{20}.
$$

The implementation stores the unrounded value as `frequency_weight_estimate`, and the proposed value rounded to increments of 0.05 as `proposed_starting_coverage_weight`. It uses Python's `round`, including its ties-to-even behavior, and rounds the stored proposed value to two decimal places. There is no shrinkage or minimum-support gate in this calculation.

For example, one rise in one activity yields 1.00, one rise in two activities yields 0.50, and three rises in four activities yield 0.75. A one-activity 1.00 means that the observed activity crossed upward; the sample count remains visible alongside that estimate.

The unit is an **activity with a visible upward transition**, even when the transition spans several bands. A change from 1 to 3 contributes one to $K$, just as a change from 3 to 4 does. Jump sizes are preserved separately:

$$
J_+=\sum_{i=1}^{N}\max(0,b_i^+-b_i^-),
\qquad
J_-=\sum_{i=1}^{N}\max(0,b_i^--b_i^+).
$$

These are ordinal band-step totals, not repetition totals, and neither replaces $K$ in the weight equation.

### Why flat activities can still receive credit

A possible observation model is that a display band covers an interval of latent progress. If both the old and new progress lie inside that interval, positive credit can leave the band unchanged. Consequently, an individual flat observation does not establish an individual zero-credit event.

The approximation behind using crossing frequency as a weight can be illustrated with equally spaced display thresholds. Suppose a full-credit activity advances one display unit, an activity's effective increment is $w\in[0,1]$, and its initial fractional position $\phi$ within the current band is uniformly distributed over $[0,1)$. Then:

$$
\Pr(\text{upward crossing})
=\Pr(\phi+w\ge1)=w.
$$

Under those assumptions, $K/N$ estimates the increment scale. This illustration motivates the heuristic; equal spacing, uniform starting positions, and the one-unit full-credit anchor have not been established for the captured system.

## Activity numbers and waiting counts

Let the eligible activity numbers that crossed upward be:

$$
c_1<c_2<\cdots<c_K.
$$

Set $c_0=0$. The counts of eligible source activities to successive visible rises are:

$$
d_j=c_j-c_{j-1}\quad(j=1,\ldots,K).
$$

Unfinished waiting time after the last crossing is:

$$
L=N-c_K,
$$

or $L=N$ when there are no crossings. The reported mean activities per visible rise includes this unfinished waiting time:

$$
A=\frac{N}{K}\quad(K>0),
\qquad
\widehat w=\frac{1}{A}.
$$

The sequence also saves the ordinal among **all captured activities on that source topic**. This can differ from the eligible ordinal when a captured activity is unsuitable for this comparison. Both ordinals start with the saved capture history, rather than the learner's first-ever activity.

Intervening visible target changes, direct target activities, elapsed hours, and a mismatch between one exposure's ending band and the next exposure's starting band are recorded. Such intervening events do not remove a pair from the report. They mean the waiting counts cannot be read as an uninterrupted accumulation experiment solely driven by the source.

## Worked relationships

| Account | Source → component | Target transitions on successive eligible activities | Crossing activity numbers | Waiting counts | Estimate |
|---|---|---|---|---|---:|
| Foundations | Visualizing Cartesian Products (4387) → Cardinality of Finite Sets (48) | 3→4; 4→5; 5→6 | 1, 2, 3 | 1, 1, 1 | 3/3 = **1.00** |
| Linear | Matrix of a Linear Transformation Relative to a Basis (1961) → Standard Matrix in Terms of the Standard Basis (2211) | 1→1; 1→3; 3→4; 4→5 | 2, 3, 4 | 2, 1, 1 | 3/4 = **0.75** |
| Multivariable | Fundamental Theorem for Line Integrals (2110) → Calculating Potential Functions (1951) | 1→1; 1→1; 1→3; 2→2; 1→6 | 3, 5 | 3, 2 | 2/5 = **0.40** |
| Differential | Euler's Method for Systems of ODEs (3245) → Euler's Method: Calculating Multiple Steps (3668) | 1→1; 2→3; 4→5; 5→6 | 2, 3, 4 | 2, 1, 1 | 3/4 = **0.75** |

For linear, the first flat activity contributes to the initial two-activity wait. For multivariable, the first visible rise follows three eligible activities, and the second follows two more. Its upward band-step sum is seven, but the estimator uses two rising activities out of five, giving 0.40. The changes between 3 and the next starting band 2, and between 2 and the next starting band 1, are intervening target-state changes rather than source-activity transitions.

All activities in these four examples have 60% observed overall correctness. Counts use the actual observed grades, rather than intended answers. The matched KP analysis found that two multivariable reviews both had 0/2 correct on the explicitly linked potential-function KP, while one stayed at band 1 and the other rose from 1 to 3. This supports keeping current-task correctness, coverage, and target state/history distinct.

## Performance and background diagnostics

Raw activity accuracy is recorded as:

$$
\alpha_i=\frac{\text{observed Correct presentations}}{\text{all graded presentations}}.
$$

The current estimator does **not** divide $K/N$ by $\alpha_i$, multiply it by earned/base XP, or weight correctness by question difficulty. The background comparison groups accuracy into a rounded fifths class:

$$
q_i=\operatorname{round}(5\alpha_i).
$$

For each exposure, the original analysis counts other-source passed exposures for the **same account, target, starting band, and quality class**. This source's exposures are removed from that background. If there are $n_i^{\mathrm{bg}}>0$ such observations and $k_i^{\mathrm{bg}}$ rises, the smoothed background rate is:

$$
p_i^{\mathrm{bg}}=\frac{k_i^{\mathrm{bg}}+0.5}{n_i^{\mathrm{bg}}+1}.
$$

When no background observations exist, the implementation records a rate of zero. Its expected background rise count and adjusted frequency diagnostic are:

$$
E^{\mathrm{bg}}=\sum_{i=1}^{N}p_i^{\mathrm{bg}},
\qquad
f^{\mathrm{adjusted}}=\max\left(0,\frac{K-E^{\mathrm{bg}}}{N}\right).
$$

This diagnostic is saved separately and does not change the proposed weight. Other-source activities can genuinely encompass the target too, so background subtraction is a sensitivity comparison rather than a known correction for noise. The older analysis also calculated direct-review-normalized, shrunken response proxies. Those proxies and the earlier content-only priors are not used in the frequency equation documented here.

The JSON includes a descriptive Wilson interval for crossing frequency. With $p=K/N$ and $z=1.96$:

$$
D=1+\frac{z^2}{N},\qquad
C=\frac{p+z^2/(2N)}{D},\qquad
H=\frac{z\sqrt{p(1-p)/N+z^2/(4N^2)}}{D}.
$$

The stored interval is $[\max(0,C-H),\min(1,C+H)]$. It describes uncertainty in observed crossing frequency under a binomial approximation. Candidate selection, repeated learner history, and shared activities between targets mean it is not a formal confidence interval for intrinsic encompassing coverage. The interval never acts as an inclusion cutoff.

## Interpretation and engine use

The schema's [`:encompassing/weight`](schema/data/5-2-encompassing.edn) is a coverage fraction, distinct from final repetition credit. Applying the frequency estimate to that attribute is a proposed initial calibration choice. Target memory, historical accuracy, learned eligibility, timing discounts, and latent position within a display band can change whether the same coverage produces a visible rise.

In the current engine, successful implicit repetition credit is approximately coverage × event quality × target speed × early-practice discount, subject to learned eligibility and the slow-implicit gate. Those multipliers were not separately fitted or inverted here. A source-to-target effect can also be explained by a transitive encompassing path; observing it does not establish that the curriculum needs an additional direct edge.

KP key prerequisites identify directly used component topics and can help refine coverage estimates when the sampled subskills differ. The present frequency estimate remains a topic-pair estimate; it does not infer that encompassing belongs exclusively to individual questions or KPs.

The calculations produced analysis proposals and evidence files. They did not update shared encompassing attributes, learner progress, engine policies, or capture baselines.

## Prepared initial EDB transaction

At the user's request, a transaction was prepared under [`reference/edb-math/imports/encompassing-weights/2026-10-11/`](reference/edb-math/imports/encompassing-weights/2026-10-11/). It has been verified with a noncommitting EDB preview and has **not been submitted**.

| Item | Prepared value |
|---|---|
| Database | `math` |
| Database lineage | `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1` |
| Read basis and intended submission basis guard | `1179` |
| Contributor | `:agent/codex`, bootstrapped in the proposed transaction |
| New encompassing records | **1,730** |
| Existing source topics receiving records | **533** |
| Existing encompassing records at the read basis | **0** |
| Retractions | **0** |

The 1,789 independent account estimates contain 1,730 distinct source/component pairs. There are 56 pairs represented in multiple accounts, including 34 with differing proposed weights. A shared `:topic/encompasses` relationship can store one weight, so preparation selects one complete account estimate per pair using this ordered rule:

1. Most eligible activity observations.
2. Lower proposed weight when observation counts tie.
3. Alphabetical account name if both count and weight tie.

This selects an account estimate without averaging account outcomes or adding their denominators. All alternatives, their separate activity sequences, and the selected account are retained in [selected-relationships.json](reference/edb-math/imports/encompassing-weights/2026-10-11/selected-relationships.json); the 34 differing-weight cases are listed in [account-conflicts.json](reference/edb-math/imports/encompassing-weights/2026-10-11/account-conflicts.json). The chosen estimates include 619 single-activity, 683 two-activity, and 428 estimates with three or more activities.

The source identity names the Codex assistant without asserting an unverified model/version. Its bootstrap map establishes tempid `"codex-encompassing-contributor"` as `:agent/codex`; the saved request uses that tempid as its source so every proposed fact, including the contributor's own facts, has the same attribution. Future requests can use the resulting ident. This identity is not asserted under Math Academy's contributor.

Existing source and component topics are addressed through unique lookup refs `[:topic/math-academy-id id]`. New relationship records use transaction-local tempids, and every record requests `:db/ensure :encompassing/validate`. Each source's cardinality-many `:topic/encompasses` map adds the new children without replacing existing memberships. The preparer preserves any already-existing source/component relationship; there were none at the captured basis.

Preparation resolves every topic against the pinned database read, verifies finite weights in `(0,1]`, checks unique targets and ownership of the proposed new records, verifies that each component is still an ancestor prerequisite in the current topic graph, and checks the combined encompassing graph for cycles. This application validation complements the installed entity spec's required-attribute checks.

The [transaction.edn](reference/edb-math/imports/encompassing-weights/2026-10-11/transaction.edn) contains the original logical forms. The [request.json](reference/edb-math/imports/encompassing-weights/2026-10-11/request.json) retains those exact forms, their SHA-256 hash, source representation, stable request key, configured endpoint, database lineage, basis guard, and hashes of the four account evidence reports. It is a prepared request rather than a commit receipt.

The [preview-verification.json](reference/edb-math/imports/encompassing-weights/2026-10-11/preview-verification.json) confirms that the speculative result contains exactly 6,922 expected source/domain assertions plus one transaction timestamp, no retractions, and Codex attribution on every fact. No learner or policy attributes appear in the proposed changes. The speculative entity IDs and after-basis are not reserved for a later commit. The compact [summary.json](reference/edb-math/imports/encompassing-weights/2026-10-11/summary.json) records the selected account counts, sample sizes, weight distribution, and preview result.

If submitted later, the saved `--basis 1179` guard must remain part of that exact request. A changed database basis requires a freshly reviewed preparation; it must not be silently submitted without its guard. After an unknown submission outcome, recover the exact original request under its saved request key rather than allocating new relationship tempids in a new request.

The deterministic preparation logic is in [prepare_encompassing_weights.py](capture/scripts/prepare_encompassing_weights.py). It consumes the saved database read exports and frequency reports; it has no durable database submission operation.

## Saved results and reproduction

All supporting results are in [`reference/mathacademy/encompassing-analysis-2026-10-11/`](reference/mathacademy/encompassing-analysis-2026-10-11/):

| Account | Frequency results | Source observation report |
|---|---|---|
| Foundations | [JSON](reference/mathacademy/encompassing-analysis-2026-10-11/foundations-frequency-estimates.json), [text](reference/mathacademy/encompassing-analysis-2026-10-11/foundations-frequency-estimates.txt) | [foundations.json](reference/mathacademy/encompassing-analysis-2026-10-11/foundations.json) |
| Linear | [JSON](reference/mathacademy/encompassing-analysis-2026-10-11/linear-frequency-estimates.json), [text](reference/mathacademy/encompassing-analysis-2026-10-11/linear-frequency-estimates.txt) | [linear.json](reference/mathacademy/encompassing-analysis-2026-10-11/linear.json) |
| Multivariable | [JSON](reference/mathacademy/encompassing-analysis-2026-10-11/multivariable-frequency-estimates.json), [text](reference/mathacademy/encompassing-analysis-2026-10-11/multivariable-frequency-estimates.txt) | [multivariable.json](reference/mathacademy/encompassing-analysis-2026-10-11/multivariable.json) |
| Differential | [JSON](reference/mathacademy/encompassing-analysis-2026-10-11/differential-frequency-estimates.json), [text](reference/mathacademy/encompassing-analysis-2026-10-11/differential-frequency-estimates.txt) | [differential.json](reference/mathacademy/encompassing-analysis-2026-10-11/differential.json) |

Each frequency JSON saves its account, generation timestamp, source-report path and SHA-256 hash, assumptions, and full activity sequences. The source-report hashes were verified while documenting these results.

To regenerate the frequency estimates from the saved observation reports, run from the repository root:

```bash
PYTHONPATH=capture python3 -m scripts.estimate_encompassing_frequency \
  reference/mathacademy/encompassing-analysis-2026-10-11
```

To rebuild the observation reports from the capture corpus first:

```bash
PYTHONPATH=capture python3 -m scripts.analyze_encompassing \
  --output reference/mathacademy/encompassing-analysis-2026-10-11
```

Rebuilding reads the capture files and cached graph contexts available at that time, so new runner evidence can change totals. Re-run the frequency estimator afterward. The documentation's counts refer to the saved results identified above.

The existing analysis checks can be run with:

```bash
PYTHONPATH=capture python3 -m unittest scripts.tests.test_encompassing_analysis
```

These checks cover account isolation, cross-course deduplication, observed-grade precedence, single-activity inclusion, flat and trailing waiting counts, declines, and multi-band jump accounting.
