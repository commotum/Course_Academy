# Four-stage template extraction

## 1. Describe the individual sources

Every original has a signed integer monomial, variables x,y, three strict positive/negative claims about every point in named open quadrants, and a five-option radio subset-selection bank. `source.json` preserves exact strings and UUIDs; `source-cases.json` supplies replay parameters. Source c, powers (a,b), quadrant order, claimed signs, correct mask and ordered observed bank are listed below. Mask bits 1/2/4 correspond to statements I/II/III. A zero mask is “None of those listed”; 7 is all three.

| Source | c | (a,b) | Quadrants | Claimed signs | Correct mask | Complete source bank masks |
|---|---:|---|---|---|---:|---|
| q96767 | 2 | (1,1) | I,II,III | +,+,+ | 5 | 7,5,3,1,6 |
| q97483 | 1 | (1,2) | I,II,III | −,−,− | 6 (derived) | 4,1,6,3,5 |
| q119766 | 6 | (1,1) | II,III,IV | −,+,− | 7 | 3,6,1,7,2 |
| q119769 | −5 | (1,1) | I,II,IV | +,−,+ | 4 | 0,2,1,4,3 |
| q119774 | 8 | (2,2) | I,III,IV | −,+,− | 2 | 1,5,0,4,2 |
| q97477 | −1 | (1,1) | I,II,IV | +,+,− | 2 | 0,4,2,1,6 |
| q97482 | 9 | (1,1) | I,II,IV | −,−,+ | 2 | 4,1,2,6,5 |
| q97487 | −4 | (1,2) | I,II,IV | −,+,− | 7 | 4,6,7,1,3 |

The first equation uses `\frac{\text{d}y}{\text{d}x}` except q97483's plain dy/dx. Source power notation contains braces around variables in hard records; q97483 uses `xy^{2}`. The template retains those differences. q96767 additionally appends thin spaces after inequality punctuation. Some sources end after statement III; others include the final subset answer sentence. These are distinct sequence templates, not silently normalized.

## 2. Generalized mathematical pattern

For y′ = cxᵃyᵇ, infer the strict sign throughout each usual open quadrant from the coefficient and coordinate powers. Compare the three stated sign assertions with those global signs and select the complete true-statement subset. The purpose is recognizing regions of positive/negative slope, without sketching short slope segments, solving the ODE, identifying symmetry/type, or moving the quadrant boundaries.

## 3. Components and every choice recipe

All answers use the same categorical, fully parameterized subset operation: select the statement positions whose bits are set. Their text is fixed by cardinality/order of that subset, independent of the equation coefficients. This is appropriate for a narrow categorical skill; there is no unsupported claim that each scalar answer encodes a recovered algebraic error operation.

| Mask / operation | Exact text |
|---:|---|
| 0 / empty subset | None of those listed |
| 1 / select statement 1 | I only |
| 2 / select statement 2 | II only |
| 3 / select statements 1 and 2 | I and II only |
| 4 / select statement 3 | III only |
| 5 / select statements 1 and 3 | I and III only |
| 6 / select statements 2 and 3 | II and III only |
| 7 / select statements 1,2,3 | I, II, and III |

Together with the complete per-source profile row above, this maps every one of the **40** observed options one-to-one, including all **28** observed distractors and all four independently classified wrong choices in the missing-ref source. Every profile preserves its five masks, complete source field, text fragments and proper correct designation where supplied. Distractor cognitive intent is unresolved; categorical subset selection itself is fully specified and exact. No learner-facing distractor diagnosis is introduced.

The prompt contains one variable monomial and three parameterized statement sentences. The fixed solution sequence is: define f and rewrite the equation → locate zero axes → sign diagram introduction and image → check I, II, III each with truth value, same quadrant condition, displayed inequality and corresponding sign prose → optional final answer sentence. There are no answer-dependent branches of the worked solution.

## 4. Reusable templates and constraints

Fixed components are the shared source sentences, three statement layout, radio field key/type, text labels, and ordered worked-solution stages. Variable components are c, exponent pair, three distinct quadrants and three strict sign claims. Conditional components are closed/open final sentence, thin-space row punctuation, numbered/bullet prompt, and source-specific fraction/power notation. The final sentence omission is preserved, not counted as missing source prose.

A whole observed profile is selected before constructing the instance. Its categorical masks remain unchanged; if the mathematically correct mask is absent, the **entire instance** is rejected. Explicit invalid parameters/profile combinations raise an error and are never silently resampled. Seeded random sampling resamples the whole instance. Five distinct categorical values cannot collide mathematically; independently interpreted subsets enforce exactly one correct option.

The normal authored bank is separately labeled `authored_sign_errors`: after determining truth mask m its complete five operations are correct subset m, complement all three classifications (`m^7`), toggle only statement I (`m^1`), toggle only II (`m^2`), and toggle only III (`m^4`). The four wrong masks directly encode full or individual statement sign misclassification; their interpretations are authored, not recovered source intent. All five are always distinct. This complete prescribed bank supports all eight truth subsets and retains the observed count/type. `authored_cycle` remains only a compatibility alias for these same five operations, never the earlier adjacent-integer recipe. None-of-those-listed is interpreted as no listed statement being true; correct subset is always explicitly available.

Moderate requires (a,b)=(1,1), hard requires one of (1,2),(2,1),(2,2), easy requires (1,0). Easy's zero set is **only x=0**, and its authored zero-axis sentence and diagrams are distinct. Hard authored defaults include a brief parity justification; observed replays retain exact source prose, without this additional sentence. These authored prose additions and banks do not count as recovered source templates.

### Honest anomaly accounting

q97483 has no correct ref, solution or difficulty in the snapshot. The owning widget confirms numbered prompt and all five choices, but does not recover those absent properties. Since y²>0 in every open quadrant, xy² has sign x: I false, II true, III true. The added ref is II and III only. Its solution is authored through the common sequence and its hard assignment is anchored to q97487, not labeled observed. Match reporting therefore has 8/8 exact prompts, 8/8 complete banks, 40/40 answer values, **7/7 available correct designations**, 7/7 available exact worked solutions, and one documented independent designation/solution/level addition. There are no other mathematical source errors or presentation repairs.
