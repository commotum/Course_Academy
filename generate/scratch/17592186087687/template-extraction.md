# Four extraction stages

## 1. Specific observed records

q-13400 asks which line is parallel to `8x-y=2`; B=-1 means integer slope 8.
q-22574 asks the same question for `4x+2y=7`; B=2 means slope -2.
q-110094 uses `6x-4y=9`; slope 3/2 requires division and reduction.
Each stem is inline math in one interrogative sentence; each field is `selection`,
radio, with five complete slope-intercept equations. Intercepts include zero,
signed integers and exact fractions. Every original field lacks a correct reference;
every original question lacks difficulty and solution. Source.json retains raw
entity and UUID provenance. Local replay preserves learner attribute presence,
layout and exact bank strings while reassigning owned UUIDs and omitting EDB/MA
identity attributes. No TeX escape repair is required.

## 2. Shared mathematical purpose

Isolate y in `Ax+By=C`, recognize slope `-A/B`, and select the unique distinct line
with that slope. All candidate equations remain slope-intercept form. The canonical
example e-14367 gives the operative solution: state necessary equal slopes;
convert through original equation → isolated By → divided y; read x-coefficient;
select the one equal-slope option. The complete canonical shared prose and stage
order are retained in parameterized authored solutions, with spacing normalized.
Practice worked solutions are absent, so none can be claimed as source reproductions.

## 3. Every source component and choice

The source expression-pattern bank parameterization is `y=(r*m)x+s*C` with
`m=-A/B`. These rational factors are honest opaque observed patterns, not a claim
about the original authoring algorithm. Parameters and exact complete values:

| Bank | A,B,C | Original complete value | r,s | Inferred key |
|---|---|---|---|---|
| q-110094 | 6,-4,9 | y=-3/2 x+6 | -1,2/3 | no |
| q-110094 | 6,-4,9 | y=-9/4 x+6/5 | -3/2,2/15 | no |
| q-110094 | 6,-4,9 | y=6x+5 | 4,5/9 | no |
| q-110094 | 6,-4,9 | y=2/3 x-3 | 4/9,-1/3 | no |
| q-110094 | 6,-4,9 | y=3/2 x+1 | 1,1/9 | yes |
| q-13400 | 8,-1,2 | y=8x-3 | 1,-3/2 | yes |
| q-13400 | 8,-1,2 | y=-x-2 | -1/8,-1 | no |
| q-13400 | 8,-1,2 | y=2x+1 | 1/4,1/2 | no |
| q-13400 | 8,-1,2 | y=-2x+4 | -1/4,2 | no |
| q-13400 | 8,-1,2 | y=16x | 2,0 | no |
| q-22574 | 4,2,7 | y=-7x+1/2 | 7/2,1/14 | no |
| q-22574 | 4,2,7 | y=2x+2 | -1,2/7 | no |
| q-22574 | 4,2,7 | y=-2x | 1,0 | yes |
| q-22574 | 4,2,7 | y=-3x-1/2 | 3/2,-1/14 | no |
| q-22574 | 4,2,7 | y=4x+2/3 | -2,2/21 | no |

All 15 choices map, including their complete intercepts. Whole equations are
compared modulo nonzero scaling; independent side comparisons are insufficient.
The correct option follows independently from the printed slope and a distinct
intercept. Missing designation is reported as unavailable, never a fidelity match.

## 4. Reusable parameterized template

Prompt: `Which of the following lines is parallel to $Ax ± By = C$?`
Fixed field key/type/count and whole-equation answer shape. Complete source profiles
are public `profile=q-*`, preserving omitted difficulty/solution/correct attrs.
`profile=completed:q-*` renders exactly the same source-shaped bank plus inferred
key/solution, explicitly evidence-only. Parameter changes recompute all bank values;
there is no literal question-return branch or key lookup. Changed examples are in
review.md. The original snapshot itself remains in source.json.

Normal authored banks derive errors from slope extraction: failure to negate A,
reciprocal of the correct ratio, negative reciprocal, and copying A (profile
method-sign-reciprocal) or omitting division by B (method-sign-division). The chosen
correct line uses intercept b+1, where b=C/B, to ensure a distinct parallel line.
Other intercepts b-1,b+2,b-2,b+3 are presentation variations and do not purport to be
error diagnoses. Two incorrect lines may share a wrong slope while remaining
distinct complete equations, as slope recognition still identifies exactly one
correct line. A whole bank containing another correct slope or duplicate complete
line is rejected. No first-valid option pooling occurs. Bank profiles and recipe
metadata remain outside learner prose. There is one fixed worked solution independent
of the selected answer. Both complete normal banks are sampled by default where
eligible; coefficient signs vary at every level.

Source anomalies: only missing metadata/key/solution, independently confirmed by
local widget evidence. No original mathematical source error identified. All
completion is explicit authorship. Source fidelity is 3/3 prompts, 3/3 full banks,
15/15 exact strings and equivalent full lines, 12/12 inferred wrong values;
0 original designations and 0 original solutions exist to compare. Normal grading
is native ID radio grading; independent mathematics checks every displayed option
and every structurally distinct isolation stage. An equivalent-row mutation that
removes the By-isolation operation must fail validation.
