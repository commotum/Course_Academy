# Classification — Solving an Inhibited Growth Model

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw evidence is preserved unchanged in `source.json`; canonical e-6679 is context, not counted as practice.

| Difficulty | Observed questions | Distinct prompt/solution skeletons | Fields | Plot rating |
|---|---:|---:|---|---|
| easy | 3 | 3 | one text radio, `selection`, five choices | none |
| moderate | 3 | 3 | one text radio, `selection`, five choices | none |
| hard | 2 | 2 | one text radio, `selection`, five choices | none |
| unrated | 1 | 1 | one text radio, `selection`, five choices | none |

The moderate campus, culture and reserve questions have the same mathematical method, but distinct narrative sentences and worked-solution fraction layouts; all three are preserved as separate Markdown/value skeletons. Hard value questions share a mathematical family; the eggs source lacks a worked solution and is retained separately with an explicitly authored solution/rating. Thus there are nine concrete skeletons, six broader mathematical layouts (school value, soda calibrated target, volume known-rate target, moderate calibrated target, hard value, hard target), and nine complete empirical profiles. Each source bank is mapped individually before extension. No source question is discarded. No practice question contains a plot; the lesson's illustrative growth curve is not an assessment asset and is not included in generated questions.

## Curriculum and scope

The captured lesson route follows `activity/first-step` and `step/next`: Introduction → Identifying Inhibited Growth Equations and Initial Value Problems → Modeling Inhibited Growth tutorial → continuation tutorial → Modeling Inhibited Growth KP → Solving an Inhibited Growth Model KP. The two tutorials derive the equation and then fit two nonzero observations using an exponential ratio. The sole key prerequisite is **Solving First-Order IVPs Using Separation of Variables** (topic 1179). The preceding topic covers exponential growth/decay; the following topic is inhibited decay. Generated instances keep `k>0`, a solution strictly below capacity, nonnegative initial quantities and `t>=0`; no decay-from-above, logistic, nonlinear equation, or branch selection is added.

Easy retains the supplied equation and its observed known-rate/calibrated-temperature demands. Moderate retains deriving the equation from a contextual hint, fitting an initial observation and one later observation, and finding a target time. Hard retains fitting two nonzero observations, solving for both constants, and then evaluating a future quantity or target time. The source hard app solution explicitly simplifies a square root; sampling keeps a rational square-root ratio rather than adding harder radical algebra. The hard-value samples keep the observation times in a 1:2 relation; hard-time samples keep them in a 1:3 relation. These are peer variations within a level, not a progression.

All three levels have observed coverage. No missing-level extension is claimed. q-37389 is assigned hard by author judgment because its two nonzero observations, rate ratio, recovery of K, and future evaluation match q-335590 and the modeling continuation tutorial. That assignment is not a recovered source rating.

## Source anomaly

q-37389 has no captured difficulty, correct lookup or worked solution. `q-37389-widget.json` preserves the authoritative local captured widget from `/home/jake/Developer/MA/DATA/Lessons/1924/Source/1924.json`; it confirms one five-choice multiple-choice widget, the same prompt and complete bank, without supplying a correct designation. Independent calculation gives `k=log(11/10)/3`, `K=121`, and `E(42)=500-121(10/11)^14=468.136...`, rounding to 468 eggs. Its designation and solution are explicit repairs, not source matches. Eight supplied correct designations and eight supplied solutions can be matched; nine displayed banks can be matched.
