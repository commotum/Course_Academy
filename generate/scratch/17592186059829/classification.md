# Classification

Snapshot: math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` preserves the captured wrapper unchanged.

| Source | Observed difficulty | Template | Field | Complete profile | Plot rating |
|---|---|---|---|---|---|
| q-102200 | absent | inequality_to_interval | radio / selection, five math choices | raw_interval | none |
| q-59295 | absent | interval_to_inequality | radio / selection, four math plus one text choice | raw_inequality | none |

Both sources lack a correct designation, worked solution and rating. Their displayed banks have exactly one mathematically correct closed set. The original MA topic-239 widgets confirm both complete banks and multiple-choice layouts; neither supplies a recovered worked solution. No fields are fabricated in raw replay. Normal profiles add independently derived keys, explicit authored ratings and canonical-style solutions. There is no source mathematical error or decoded doubled-backslash anomaly.

The actual route traced from first-step/next is Introduction → Closed Intervals tutorial → Open Intervals KP → Closed Intervals KP → Half-Open Intervals tutorial → Half-Open Intervals/Inequalities KP → Half-Open Intervals/Number Lines KP. Open and half-open sets are distractor errors; they never become correct assessed objects. Unbounded Intervals is a later topic, so the observed half-line stays a distractor only.

Canonical closed example e-10816 converts 1 ≤ x ≤ 4 to [1,4], includes both endpoints, uses blue brackets and a final membership line. The preceding open canonical example supplies the reverse-direction sentence/stage structure, adapted explicitly to closed endpoints. Topic prerequisites include Compound Inequalities, Surds, and Simplifying Expressions With Surds. The half-open sibling uses −4 and sqrt(2), and its original practice uses −5 and 2sqrt(2): exact surd reading is already supported.

All easy/moderate/hard labels are authored, including assigning the two integer originals to easy normal replay. Easy reads ordered signed integers; moderate reads at least one reduced noninteger rational endpoint; hard reads two noninteger endpoints with at least one surd and a negative left endpoint. These are endpoint-reading workloads within the same direct conversion. Hard does not require solving inequalities, simplifying radicals, determining ordering, or translating a nonclosed correct set. Both directions are equal-level variants within each level; no progression is implied.

## Current source addendum (basis 2088)

The current database has three practice questions. q-102200 now has an easy rating, independently correct key, and complete worked solution; its five-choice bank is mathematically equivalent to the historical bank, with normalized notation. q-59295 remains unrated, unkeyed, and solutionless and is excluded from available inventory. New q-154728 is rated moderate, asks for the inequality for [-7,0], and has five choices: four combinations of endpoint inclusion plus the inclusive outside union x ≤ -7 or x ≥ 0. It is distinct from the historical strict outside profile, and both remain explicit complete profiles. No plots are needed.

`captured_interval` preserves the current q-102200 prompt/bank/solution layout and easy rating. `captured_inequality` preserves the current q-154728 bank and fixed solution layout and moderate rating. Each uses ordered integer endpoints -12..12, matching the current observed workload; this authored extension has 300 endpoint pairs per direction, overlaps older integer tasks, and cannot inflate distinct task counts. Original q-154728 has `?` inside the math delimiter; generated variants move punctuation outside, with the source preserved. Every choice and solution endpoint is substituted from the same exact parameters; outside-union distractors retain their inclusive boundary relations. Fresh source-bank replay, correct designations, solution stages, and native grading are recorded in current-validation.json. Existing rational/surd catalogs and historical raw profiles retain their earlier evidence.
