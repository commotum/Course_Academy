# Classification at basis 2677

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
KP 17592186133884, UUID 48652211-e469-55b9-96cb-2526a4135d34.
Live batched source read finds no generator. No existing scratch package or job
`.generated` file was present. All 13 practice questions, the canonical example,
complete fields, source banks, solutions and references are captured in source.edn
and source.json. source-components.json preserves every component and exact choice.

| Band | Field shapes | Distinct templates | Practice evidence |
|---|---|---:|---|
| Easy | unobserved | 0 | no source evidence |
| Moderate | 10 single radio fields (5 choices); 1 single blank | 11 | below |
| Hard | 2 single radio fields (5 choices) | 2 | below |

The 13 templates differ in geometry, field input (vector vs differential),
expression structures or response contract. One complete bank profile per radio
source; the blank has no distractor profile. Source questions are not merged into
a single pooled bank. Detailed prompt, original choice mapping, solution and image
references are in source-components.json.

| Source | Band | Template backbone | Plot requirements for package |
|---|---|---|---|
| q-108467 | moderate | triangular type I region; polynomial differential form | none: fixed diagram reused |
| q-42085 | moderate | square; polynomial vector field, vector rewrite | none: fixed diagram reusable |
| q-41702 | moderate | negative sine lobe; differential form, constant negative curl | none: fixed diagram reusable |
| q-42107 | moderate | triangular type II region; trigonometric vector field | none: fixed diagram reusable |
| q-168558 | moderate | supplied square limits; blank asks only curl fragment | none for fixed square, but prompt lacks F |
| q-109254 | moderate | first-quadrant circle; vector rewrite and trig cancellation | none: fixed diagram reusable |
| q-109291 | moderate | triangle with two nonconstant y limits; trig vector field | none: fixed diagram reusable |
| q-109288 | moderate | triangular type I region; differential trig cancellation | none: fixed diagram reusable |
| q-109248 | moderate | right semicircle; polynomial differential form | none: fixed diagram reusable |
| q-109245 | moderate | rectangle; differential trig cancellation | none: fixed diagram reusable |
| q-42074 | moderate | parabola cap; constant curl outside integral | none: fixed diagram reusable |
| q-109249 | hard | curved type II region; exponential/trig cancellation | none: fixed diagram reusable |
| q-109263 | hard | parabola/line type I region; log vector field | none: fixed diagram reused |

Plots inspected individually for the supported templates and as source-plots.png
for all source families. Orange boundaries, pale-blue fill, labeled curves,
axes/intercepts and counterclockwise arrows show the regions described by the
limits. They occur in worked solutions, not answer choices. Fixed geometry means
no new plots are needed; changing coefficients does not change those assets.
A future geometry-slot extension would require moderate recurring plot generation
and is outside this bounded version. Canonical example supports Green's theorem
analysis but is excluded from practice stock.

Capabilities: moderate triangle-polynomial and hard parabola-vector only. Other
source families remain preserved and may count as practice after independent math
and native grading checks; this generator does not synthesize them. Easy is
unsupported in this source-bounded version, not mathematically impossible. Reopen
classification if new source evidence arrives.

Source issues: q-168558 omits F from the learner prompt; q-109248 has both 2xy
and x²y integrals equal to zero over its right semicircle. q-109263 changes
ln(2+x) to ln(1+x) late in its solution and has two equal-valued distractors at
its original a=1. These originals are preserved and excluded from validated stock.
The hard generator corrects the repeated log and excludes a=1 from normal output.
Final audit also excludes q-42074: its correct cap integral and a distractor over
[-x²,x²] both evaluate to 4; two other distractors both evaluate to 2.

Final complete-value audit excludes two additional source banks under the same
policy: q-41702 has two options equal to -2, and q-109254 has duplicate incorrect
values by symmetry (1+cos(x) over the right and upper unit semidisks). Six moderate
and one hard source questions remain mathematically validated before generated
content. All their choices are checked as complete integrals, including values;
see source-value-audit.json. Neither source records nor historical answers change.
