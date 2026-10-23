# Template extraction — four stages, math basis 1356

## 1. Specific observations before generalization

Every source, exact matrix, complete prompt/solution, ordered field key, source answer ID, all exact choices and recipes are in source-components.json. This is the exhaustive mapping, including the two unrated originals.

| Source | Matrix / position | Number forms | Prompt/solution demand |
|---|---|---|---|
| q-13498 | A3×3, (1,2) | nonnegative integers0..20, repeated7 | inline bmatrix radio, unbraced a-subscript; no rating/correct ref/solution |
| q-13503 | B3×4, (3,3) | nonnegative integers0..17, repeated9,6 | inline bmatrix radio, unbraced b-subscript; same missing attributes |
| q-139426 | P3×3, (3,2) | -2,0,2 repeated | display aligned matrix; generic p_ij and two numeric placeholders; position sentence then i=3,j=2 |
| q-13489 | C2×2, (1,1) | 0,1,2,4 | display radio; position sentence then c11=1 |
| q-279553 | B2×3, (1,1) | -3..3, repeated2 | single symbolic blank, placeholder immediately before period; position sentence then -2=b11 |
| q-279556 | A2×3, (2,3) | 0 and5 repeated | same symbolic fragment layout; position sentence then5=a23 |
| q-125611 | Y4×2, (4,2) | -4..7, repeated0,1 | display radio; position sentence then y42=7 |
| q-13499 | A3×4, (3,4) | 0..17 repeated9,6 | display radio; position sentence then a34=0 |

Signs, zeros, repeated values do not create distinct methods: only cell position determines the answer. Bracketed aligned display and inline bmatrix are separate layout templates. Symbolic blanks differ from two numerical blanks. No source plot references.

## 2. Shared mathematical pattern

Count the highlighted cell's row from the top and column from the left using one-based indices. Return either the indexed symbol or its two index components. The first subscript is row, the second column. This reverses the sibling entry-finding task; it never asks for the number itself. A unique visible box distinguishes the cell even when values repeat.

## 3. Components and complete banks

Parameters are one rectangular matrix of integers, single uppercase letter, existing one-based i,j. Source bodies are replaced as whole mathematical components. Letter tokens, complete generic indexed symbols, the full positional clause, and full final equality are separate slots, avoiding accidental short-string replacement.

All five banks are complete observed coordinate-offset patterns, specified here in captured choice order. For each pair (di,dj) produce x_{i+di,j+dj} in the source's brace spelling. The target is exactly (0,0), and the source correct choice, where present, must independently agree with it. We do not claim to recover original authoring algorithms or psychological intent. Remote combined shifts are explicit observed patterns with underdetermined intent; source options are categorical coordinates, so no arbitrary fitted scalar formulas are needed.

| Profile | Complete ordered offsets relative to the actual highlighted cell | Explicit eligibility |
|---|---|---|
| q-13498 | (1,-1),(0,1),(0,0),(1,0),(0,-1) | j≥2, all resulting subscripts1..9 |
| q-13503 | (-2,0),(0,0),(-1,-2),(-1,0),(1,0) | i≥3,j≥3 |
| q-13489 | (0,0),(1,2),(1,1),(1,0),(0,1) | all resulting subscripts1..9 |
| q-125611 | (-1,-1),(0,-1),(-1,0),(0,0),(0,1) | i≥2,j≥2 |
| q-13499 | (-1,-3),(-2,-1),(1,-1),(-1,-2),(0,0) | i≥3,j≥4 |

Some observed wrong indexed symbols point outside the displayed matrix (c23 for2×2, y43 for4×2, a43 for3×4, b43 for3×4). This is faithfully preserved: these symbols cannot name its boxed entry. The valid target always exists. All options use positive single-digit subscripts; the complete set has no duplicate positions. Membership/equality of coordinates, not numerical equality of matrix cells, determines answer eligibility. Bank patterns are generalized coordinate operations and their learner-facing descriptions contain no invented distractor diagnosis.

For q-139426 the captured field order is field-2=column j, field-1=row i, each one math choice and correct ref; the prompt orders i then j. Preserve both keys and source field collection order. Symbolic blank expects the exact indexed fragment, retaining braced letter; its final equality puts the numerical entry first. Native incompatibility is recorded separately from fidelity and mathematics.

## 4. Reusable masks, constraints, calculations and identity

Raw replay uses source prose as a masked template, not literal answer payload branches. Matrix rows are rebuilt for every parameter set; all bank coordinates are recomputed from the actual i,j; the one fixed worked solution updates the ordered position sentence and full equality. Raw replay does not add a highlight, missing rating, missing solution or correct ref. Complete raw field-key presence and all29 source values replay exactly through generate(). Source-cases.json supplies parameters/profile for all8 public replay calls. Changed letters, signed entries and changed positions exercise every raw/completed recipe.

Normal/defaults box one actual cell and preserve source common sentences and stage sequence. Inline radio has authored source-style positional prose because its source solutions are absent. Numeric blanks retain the full original generic-symbol sentence and i/j conclusion, with only capture whitespace normalized. Symbolic blanks remain ineligible explicit drafts with their original fragment layout and equality direction. Complete bank/family is chosen before parameters; finite eligible positions are sampled for that chosen complete bank. There is no pooled first-valid distractor selection. Explicit invalid banks/positions fail without resampling or silently changing parameters.

Normal sampling chooses uniformly among the three supported layouts, then among the five complete radio profiles weighted by eligible meaningful position count when applicable; blank defaults use two numerical fields. All supported families and all profiles are exercised by default coverage and native grading at each level. Difficulty bounds are exactly those in classification.md; source raw/completed replay has its independently declared original workload envelope (existing positions, at most7×7, integers-34..34 including canonical34) and easy API calls never invent a captured easy attribute for unrated raw records.

Task identity hashes positional operation, dimensions and i,j only. Full identity hashes version, actual displayed prompt and complete fixed solution, actual difficulty/presence, every key/type and complete sorted bank, plus correct-presence and designation. Seeds, choice order, profile names and parameters that are not displayed cannot create identities. Changing entries or the letter alters full content identity while keeping the same assessed task. Source banks are tested one-to-one ignoring order; correct refs are counted only where captured. Raw exact8/8 prompts,6/6 solutions,9/9 field banks,29/29 values; captured refs7/7, two absences preserved.
