# Template extraction: four stages

## 1. Specific observations

Every easy source supplies a specified x-coordinate and asks for the continuous function among5 complete graphs. q-48039 asks -2 and its correct graph has an unrelated point discontinuity at1; q-48081 asks2 and correct graph is a closed sharp peak; q-69782 asks5 and correct graph is a connected parabola around5 with an unrelated jump at2; q-48082 asks0 and correct graph has an unrelated point discontinuity at2. q-48039/48082 prose explicitly distinguishes local continuity from continuity elsewhere. q-69782 has different opening prose, then correct highlighted graph, then shared elimination. q-48081 has no worked-solution plot despite its “shown below” sentence; exact observed replay preserves that omission; normal output adds the correct graph at that stated solution position as a presentation repair.

Moderate: q-102106 targets(-1,2,4), connected/connected/pole; q-78133 targets(-7,-4,-1), jump/connected/displaced singleton; q-102115 targets(-1,1,3), jump/displaced singleton/connected; q-78131 targets(-2,0,2), pole/closed cusp/connected; q-78132 targets(-2,1,3), connected/jump/connected. Their solution stage sequence is opening → three separate local-point bullets → final named subset → optional highlighted graph. All source sentences and image positions remain parameterized masks rather than being replaced with a generic limit calculation.

q-102115 uses unlabeled point bullets against Roman-subset answers: normal output explicitly labels I/II/III. q-78132 has omitted “at” in one final local-point sentence: raw wording retained and normal minimal grammatical correction. q-48082 solution image90c2fbe9 reverses its open/filled positions at the unrelated point2 compared to answer imagec6f0914f: the lower filled point now sits on the curve and the upper open marker is isolated. Its local0 answer is still correct, but prose assertion of discontinuity at2 is unsupported by that solution drawing. Raw asset/prose remain exact; normal solution render uses the same function as the correct answer option. This is a mathematical image repair, separately reported from raw fidelity.

## 2. General pattern

Decide continuity locally at supplied positions by reading connected branches, finite holes with separately specified values, jumps and vertical asymptotes. The assessed answer is **actual continuity**, not existence of a finite limit alone or existence of the function value alone. Each question has one fixed worked solution independent of selected response. Complete graph objects are different answers even when several share the same false continuity predicate.

## 3. Component and full-bank mapping

`source-cases.json` maps every source to its public template, parameters and observed profile. `source.json` retains all source fields/options, original UUIDs, literal values and original presence. Per-option graph recipes and expected independent source topology are explicitly listed in plot-extraction.md and validate.py; nothing is discarded. Easy banks contain all5 observed images, not a pool of plausible distractors. Moderate observed banks are:

|Source|Complete bank|Correct|
|---|---|---|
|q-102115|I+III; II; III; II+III; I|III|
|q-78131|I+III; II+III; all3; II; III|II+III|
|q-78132|III; I+II; II+III; I; I+III|I+III|

The exact “only”, comma and “and” fragments are retained in API bank values. Text option recipes are categorical subsets of candidate-position roles; numerical equality is irrelevant here. q-102106/78133 have no original bank. Authored q-102106 bank: I, II, I+II, I+III, all3. Authored q-78133 bank: I, II, III, I+II, II+III. These full sets are selected before graph parameters; no first-valid option substitution or option-wise perturbation occurs. All original fields8/options40 are included in fidelity, including the5 legacy options without a known correct designation. Seven available correct designations and their28 designated distractors are compared individually.

## 4. Backbone, slots and guards

Fixed: question instruction, field shape/image versus text response, number of candidate points, complete per-family graph bank, local branch/inclusion topology, shared solution wording and sequence. Variable: a complete affine horizontal coordinate transform x' = scale*x+shift; vertical offset applies to all branch/point ordinates. Every queried and contextual prose coordinate, plot interval, branch formula, hole, closed point and asymptote derives from those slots. All slots are exact rationals. Easy/moderate horizontal scale1 or2, integer shift[-4,4], integer vertical[-2,2]. Hard scale1/2 only, same bounded integer offsets and at least2 half-integer targets (q-78133:2 midpoint positions+1 integer; q-102115:3 midpoint positions); source observed anchors scale1,shift0,vertical0. Invalid explicit inputs fail instead of being silently resampled.

Source graph equations and unlabelled y-scales are unavailable. Changed graphs are authored exact piecewise-linear/rational **realizations of the inspected topology**, with source unassessed corners/peaks/jumps kept in context. They are not claimed to recover unknown original algebraic formulas. Original image anchors are reused only for exact explicit observed replay. The raw q-48082 solution drawing has its own independently transcribed graph/annotation recipe; normal drawings repair it. Source paths are not used to prove continuity; exact graph limits, domain membership and singleton values independently prove each local decision.

Sampling selects the complete family/bank first and then coordinates. The declared semantic catalog has11 tasks:4 easy banks,5 moderate graph/target topologies,2 hard coordinate-reading variants. Numeric translation, vertical offset, option order and cosmetic profile aliases do not inflate semantic variety. Different graph realizations create new full content but retain the same assessed categorical structure. This narrow KP has a finite conceptual catalog; we do not invent another skill to claim infinite structural diversity. All9 source-shaped families participate in normal defaults.

Content IDs include generator version, actual rendered prompt, fixed solution, complete displayed bank, difficulty, field/key layout and attribute presence; ignore option order and profile aliases. Mathematical IDs exclude numeric/cosmetic aliases and incidental unqueried point coordinates, retaining candidate roles/topology and hard scale-reading demand. Raw omitted fields/designations are ineligible evidence. UUID correct refs are field-owned and identify exactly one bank option. Metadata is never inserted into learner prose.
