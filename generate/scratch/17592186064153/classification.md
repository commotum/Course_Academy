# Classification

Capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged wrapper. Six practice questions are present; the canonical school-budget example is curriculum evidence, not a seventh practice question.

| Difficulty | Source | Template | Field/layout | Complete bank | Plot rating |
|---|---|---|---|---|---|
| easy | q-48571 | app | one text radio, selection | 5 options | none |
| unrated; authored easy assignment | q-48615 | walking | one text radio, selection; missing key | 5 options | none |
| moderate | q-48688 | car | one text radio, selection | 5 options | none |
| moderate | q-48691 | price | tangent-slope statement; text radio | 5 options | none |
| moderate | q-48709 | visitors | tangent-slope statement; text radio | 5 options | none |
| hard | q-112091 | ice | one text radio, selection | 5 options | none |

Six distinct contextual prompt/solution templates are retained because the unit conversion, response context, bank operations, and solution stages differ. There are six complete observed banks, not one merged distractor pool. Five have captured keys and worked solutions. All six banks and all 30 options remain available through `generate(..., profile="observed")`.

The lesson route follows links, not collection order: introduction (64979), units (65155), generic derivative interpretation (64980), this KP (64981), determining a rate (64982), relating derivative/entry/exit (65156). Prerequisite topics are derivative notation (812) and units of rates (2231). Here the learner interprets **a supplied numerical derivative at a supplied input**; calculation of derivatives, finite differences, velocities, entry-minus-exit, or identifying only units would belong elsewhere.

Every source level exists. Sparse coverage motivates three explicitly authored templates: easy `budget` anchored to e-271, hard `temperature` preserving ice's sign/locality demands in another physical unit, and hard `signed_visitors` combining the observed negative-rate and thousand-unit interpretations. Signed visitors explicitly means visitors currently on the website, a changing stock rather than cumulative lifetime visits; its negative derivative is physically meaningful. The observed positive visitors prompt remains exact. These do not create a progression. Moderate retains its observed direct-car classification even though its algebra is no harder than easy; its other two templates require tangent-slope interpretation and unit scaling. Hard always has a negative derivative, and `signed_visitors` also has the source's scaling demand. No harder algebra is introduced.

Inputs are positive integers, normally 2, 4, 5, 8, 10, 16, or 20, to keep quotient distractors terminating and legible. Rates are positive for easy/moderate and negative for hard; scaled rate magnitudes normally 0.1–2.5 and bounded explicitly at 0.1–5 with hundredth precision. Integer rate magnitudes are explicitly 2–5000, normally 2–25 for hard, 10–200 for car/walking, and 100–2050 for app/budget. No level is made harder through arithmetic. Explicit source input 30 and walking input 3 remain valid. Physical input values and rate magnitudes in options remain nonnegative; decreasing-rate options encode sign in prose rather than negative counts, area, or elapsed times.

Normal generation selects a complete authored profile before construction, computes every member, and rejects the whole bank on duplicate text. The ice swapped-value member collides with its ordinary-value member when input equals rate magnitude; explicit calls fail, random generation resamples the entire instance.

This categorical skill has nine context/layout structures, not hundreds of new skills. Numerical task sample counts report distinct supplied input/rate/context instances, excluding profiles, banks, ordering, seeds, and aliases; `signed_visitors` shares the visitors fingerprint family. Function/variable names are fixed and cannot inflate counts. Different physical units and scales are part of the interpretation. No plot assets are referenced by this KP; mentioning a tangent line does not require displaying a graph.

## Raw evidence and repairs

* q-48615 has no difficulty, correct reference, or worked solution in EDB. The source screenshot at `/home/jake/Developer/MA/DATA/Lessons/296/Source/Sections/09-question-48615.png` was inspected; it confirms the five source options, without a revealed key. The positive derivative supports the increasing local meters-per-day option. That key and an easy assignment are authored, never counted as matched source metadata. Normal walking output says `On day` and explicitly describes a continuous model; this resolves the source's ordinal-day/elapsed-day mismatch. Raw wording remains in observed replay.
* q-48688's scalar constant-rate `3` does not identify its authoring intent. The observed profile explicitly uses the reciprocal quotient `input/rate`, which reproduces 30/10=3. This is an evidence-preserving numerical pattern with uncertain intent, not a recovered error recipe. The default authored bank uses the defensible mistaken average `rate/input`; it never claims the source bank was that recipe. It also replaces the physically impossible decrease in cumulative distance with a positive input-as-rate error; input=rate rejects the whole bank.
* q-112091's source opening claims S′(t) represents the rate at which area `is decreasing`, before evaluating at the known negative point. A derivative at one point does not establish a global sign. Raw replay preserves this source sentence. Normal output minimally substitutes `changing`, keeping the negative-at-the-point conclusion. This is a mathematical teaching-prose repair, separate from exact bank and raw solution fidelity.

No source is dropped, no missing key is fabricated as observed, and no source-format issue is silently normalized. There are no unbalanced source math delimiters or missing blank placeholders here.
