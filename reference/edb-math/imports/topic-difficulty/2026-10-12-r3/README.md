# Topic workload calibration from captured lessons

**Committed and verified at basis 1521.** The [transaction](transaction.edn) added **777 topic difficulty multipliers and 429 missing lesson durations** in database `math`, with **`:agent/gpt-6.1-sol-high`** as source. It committed against basis **1520**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The [receipt](receipt.edn) and [verification](commit-verification.json) confirm the exact values and provenance at the committed database basis.

The 777 topics cover **26.1% of the 2,981-topic database**. The remaining 2,204 have no eligible observed calibration and retain the engine's implicit multiplier of 1.0. The committed values range from **0.239987 to 2.877390**, with median **0.967408**. Full numerical precision is stored; the encompassing fraction choices do not apply to this XP calibration.

## Previous calculation

The previous database's implementation used the [agreed method](../../../../../reference/THE_PLAN/README.md) and [selected XP formula](../../../../../reference/xp-docs/expected-distribution-base-xp.md). Its initial catalog backfill priced lessons with multiplier 1.0; the saved topic-multiplier audit was empty. This preparation applies that existing calibration method to captured observations rather than copying old numeric entity IDs or assuming that the earlier database had calibrated topic values.

For each complete recorded lesson, use its displayed **base-XP denominator B**, the **first two distinct practice questions per KP in recorded order**, all tutorials, and one canonical example for every KP. Earned XP, correctness, elapsed time, and individual question difficulty labels are not inputs. A missing first question cannot be replaced by a later question; incomplete coverage is recorded in [excluded captures](excluded-captures.json).

The content measurements are:

| Symbol | Measurement |
|---|---|
| T | Sum of per-KP mean solution math-token counts, divided by 100 |
| K | Number of KPs |
| R | Tutorial and canonical-example prose words, divided by 100 |
| S | Sum of per-KP mean solution equals-sign counts |
| E | Equals-sign count in canonical-example solutions |
| P | Sum of per-KP mean prompt math-token counts, divided by 100 |
| F | Sum of per-KP mean additional answer fields beyond the first |
| A | Sum of per-KP fractions containing a blank answer field |

For normalized initial lesson probabilities pE, pM, pH:

```text
L = 0.7727506490727063 × (pE + 2pM + 4pH) × T
  + (0.8708735238642493 × pM + 2.041850919949942 × pH) × K
  + 0.07513004637186382 × R
  + 0.001586056170966394 × S
  + 0.034422123109798704 × E
  + 2.7349018409710975 × P
  + 0.06047150091696244 × F
  + 0.5742034148595132 × A

predicted_base = max(7, floor(c × L + 0.5))

B > 7: c = B / L
B = 7: c = 1 if max(7, floor(L + 0.5)) already equals 7;
       otherwise c = 7 / L
```

The old default was 60/30/10. The [live policy snapshot](lesson-weights.json) has **45/40/15**, so this transaction uses pE=0.45, pM=0.40, pH=0.15. Its expected question workload factor is **1.85**. The formula, extraction rules, and coefficients are unchanged; the calibration uses the probabilities actually stored in this database. No policy values were modified.

There are **232 floor-limited selected topics**; 116 retain the neutral multiplier 1.0. The seven-XP floor does not uniquely identify their latent workload, and the agreed rule above supplies their practical estimate.

## Evidence and selection

The combined archive supplies **931 eligible observations**: 378 from the current account folders and 553 from the older question-capture archive. They cover 777 distinct topics. Ten lesson captures lacked required content, complete coverage, or an authoritative denominator. Reviews, assessments, diagnostics, and multistep tasks are outside this lesson calibration.

Each observation is calculated independently. For repeated topics, select the eligible observation with the largest Math Academy task ID, using captured time and account/file name only to break ties. Task IDs order assignments; an archive read of an older task is not treated as a newer lesson. Select one whole observation, with no averaging or blending of account histories or lesson versions. The legacy archive lacks reliable account labels and is explicitly retained as `legacy-unlabelled`.

| Selected observation source | Topics |
|---|---:|
| Legacy archive, account unlabelled | 429 |
| Differential | 121 |
| Multivariable | 96 |
| Linear | 74 |
| Foundations | 57 |

[Selected calibrations](selected-calibrations.json) include topic titles, database identities, source hashes, denominator evidence, selected question IDs, complete-KP coverage, features, unscaled scores, policy weights, previous values, and competing eligible task IDs. [All observations](observations.json) retain the original default-distribution calculation; [current-policy calibrations](current-policy-calibrations.json) retain the recalculation for 45/40/15. Legacy tutorial prose is measured from the original HTML using the same exclusion rules as the old analysis. No canonical-solution substitutions are used.

The [historical method check](historical-method-check.json) covers all 58 lessons in the original comparison. Fifty-three reproduce every frozen feature exactly. Five current capture texts differ from their frozen measurements by one to three math tokens; the current captured text is used and its hashes are retained.

## Matching lesson caches

The engine reads `:activity/expected-seconds` before calculating a content-based lesson base. The [duration audit](activity-duration-audit.json) found **348 matching current values and 429 missing values**. The transaction fills those 429 shared lesson definitions with **B × 60 seconds**, preserving the authoritative captured denominator alongside the multiplier. No existing durations differ from their selected observations or require replacement. Existing learner-task XP allocations and historical XP awards are not modified. Each duration addition ensures `:activity/validate`; each multiplier addition ensures `:topic/difficulty-validate`.

## Verification and request

All **931 current-policy calibrations passed the Rust engine's denominator round trip**. The relevant Python suite passed **46 tests**. The [native preview verification](preview-verification.json) confirms exactly **1,206 domain assertions**, **zero retractions**, and one generated timestamp, all attributed to the requested source. Only `:topic/difficulty` and `:activity/expected-seconds` gain facts; no learner or policy facts change. The preview is speculative and performs zero durable writes.

[request.json](request.json) preserves the exact forms, transaction digest, stable request key, source, database lineage, connection identity, basis guard, policy identities, and evidence hashes. Preserve this immutable request for recovery. The earlier [difficulty-only request](../2026-10-12/README.md) remains unsubmitted. The [basis-1519 combined request](../2026-10-12-r2/README.md) received a confirmed `postgres/stale-basis` rejection. Only after reconciling its original key was this replacement request prepared against basis 1520. Its [scope check](approved-scope-check.json) confirms the exact transaction text, evidence, values, and source are unchanged.

The reusable [preparation script](../../../../../capture/scripts/prepare_topic_difficulty.py) supports `collect` and `prepare` only. To create a refreshed proposal, use a new output folder:

```bash
cargo build --bin fire
PYTHONPATH=capture /home/jake/Developer/MA/.venv/bin/python -m scripts.prepare_topic_difficulty collect --folder NEW_FOLDER
PYTHONPATH=capture /home/jake/Developer/MA/.venv/bin/python -m scripts.prepare_topic_difficulty prepare --folder NEW_FOLDER
```

Neither action submits a transaction.

## Commit and recovery

The durable request key is `topic-workload-2026-10-12-04578d9e-4da5-4945-ab02-f73adbf43e39`. Transaction entity `13194139534833` advances basis **1520 → 1521**. The committed receipt contains exactly **1,206 domain additions and one timestamp**, with **zero retractions** and no new entities. All 1,206 values and their source were independently read back at basis 1521. The receipt contains no learner or policy changes.

The [commit script](commit.py) validates the saved request and preview hashes, reuses a confirmed saved receipt, and verifies the exact receipt facts and stored values at its committed basis. If a reply is lost, recover the same complete request under the same key; never create a new key to recover an unknown outcome. Running it again here reuses the saved receipt and repeats read-only verification:

```bash
python3 reference/edb-math/imports/topic-difficulty/2026-10-12-r3/commit.py
```
