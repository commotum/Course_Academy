# Arc-length setup extraction

Source basis 2568, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The immutable source.json contains all 12 practice questions and the canonical example, including complete prompts, banks, fields, solutions and asset references. classification.json assigns every source to a level, template and bank profile; source-choice-mapping.json retains every complete mathematical option and its original field and answer identity. No distractor recipes are pooled. Nine other complete profiles are exact replay only, not normal generation. The unrated q-15155 has no key or solution and remains excluded.

## Shared backbone

Given two explicit parametric coordinate functions and an ordered real interval, select the definite integral of the nonnegative derivative norm. One radio field `selection`, five math choices, no integration/evaluation or alternate response contract. Each solution states the general arc-length formula, differentiates x, differentiates y, substitutes both squared derivatives, and expands/collects the radicand. The hard source has an additional uncollected expansion row. The field key, answer ownership, option count and stage order remain fixed because they define the response and source instruction.

## Moderate normal family: q-15163

Original coordinates x=t+2 sin(t), y=1+cos(2t); bounds [2,5]. Original A=2, B=2. Generalization x=t+A sin(t), y=1+cos(Bt), A in {2,3}, B in {2,3,4,5}. Both are integer slots, separately sampled over their full Cartesian domain (8 tasks). A controls the amplitude in x; B is a frequency and chain-rule multiplier in y. These preserve the derivative types, quadratic expansion, and workload. Translations and endpoints stay at the source values: varying translations adds no derivative task, and varying bounds alone would add little instructional variety. Symbols, supplied/requested roles and derivative operations remain fixed. No target-position slot exists.

Let u=cos(t), v=sin(Bt). Complete bank radicands, in retained source profile order:

1. 1+4Au+4A²u²+4B²v² (source compound pattern; interpretation unresolved).
2. 1+Au+4A²u²+B²v² (source compound pattern; interpretation unresolved).
3. 1+2Au+A²u²+B²v² (correct).
4. 1+2Au+A²u²+4B²v² (source compound pattern; interpretation unresolved).
5. 1+Au+Au²+B²v² (source compound pattern; interpretation unresolved).

Each option is the integral of the square root on [2,5]. No inferred misconception language appears to the learner. Solution derivatives are 1+A cos(t) and -B sin(Bt). The displayed final expansion uses exactly their squares.

## Hard normal family: q-123027

Original x=3cos(t), y=8t+cos(t); bounds [-1,1]. Original A=3, B=8. Generalization x=Acos(t), y=Bt+cos(t), integer 2≤A≤6, 4≤B≤12, B>A+1 (35 tasks). Amplitude A and linear coefficient B are distinct slots. The bound keeps positive radicands for the complete authored bank and a comparable expansion workload. Conservative finite sampling policy, not a mathematical impossibility bound. Let u=sin(t). Complete bank integrands:

1. 2 sqrt((A²+1)u²/2 - Bu + B²/2).
2. sqrt(A²u²-Bu+B²).
3. sqrt(u²-2Bu+B²).
4. sqrt(Bu²-2u+B).
5. sqrt((A²+1)u²-2Bu+B²), correct.

These reproduce the whole original bank at (3,8), including the multiplier outside the first source integral. Unclear compound errors remain observed expression patterns. Derivatives -A sin(t), B-sin(t); substitution; uncollected A²sin²(t)+B²-2Bsin(t)+sin²(t); collected (A²+1)sin²(t)-2Bsin(t)+B².

## Plots and fidelity

The two normal families have no plots. Six complete evidence-only sources have a supplemental blue parametric-curve sketch, black axes, marked parameter endpoints, orientation arrows and dotted continuation; inspected individually. These require parameter-dependent plots if generalized and are rated moderate. plot-extraction.json retains original content hashes and roles. Existing assets are reused only for original evidence replay. Canonical e-7130 has its own log-cosine diagram and is never practice inventory. No new plot rendering/publishing is required for normal output.

Source replay compares all five complete mathematical integrals and correct designations, and normal source-parameter replay compares the same original banks separately from prose layout. Source prompts/solutions are normalized only through the existing math-format layer in evidence replay. Normal output preserves instructional sentences and operative stages, with consistent modern TeX rendering; it does not claim byte-exact source layout. review.md shows original, normal replay and changed-parameter output side by side.

Validation exhausts every declared finite A/B pair, re-reads the visible functions, derivatives, bounds, intermediate integral stages and full bank, rejects duplicate options and incorrect keys, verifies deterministic replay and stable identities across seed/choice shuffles, and calls the real application grader for all five options. Each slot's sampled values are reported in validation.json. There are no variable target locations, so changed A/B cases test that every reference and solution value changes together. Source-only families are not used to expand inventory.
