# Template extraction

## 1. Describe each original before generalizing

All originals solve `y′−hy=f e^(kx)` with `y(0)=v` and a supplied complementary solution `Ae^(hx)`. Signs are significant: positive h prints a subtraction, negative h an addition. Rates ±1 omit the numeric coefficient in exponent bodies. The six easy records have k≠h; the seven moderate records have k=h. Both unrated records use the same prompt and one blank, but lack difficulty, solution, choices and correct designation.

Original source parameters and every bank member are listed below. The complete capture retains original UUIDs and all raw fields; the public generator gives generated, field-owned UUIDs with the same correct-bank position. `source-cases.json` replays each original via the normal public API using `raw:<source-id>`.

| Source | h | k | f | v | Original level | All bank members (correct is bold) |
|---|---:|---:|---:|---:|---|---|
| q-332426 | 6 | 2 | 8 | 1 | unrated | missing |
| q-332797 | 3 | 3 | 9 | 2 | unrated | missing |
| q-332903 | 5 | 2 | 6 | 4 | easy | **$6{e}^{5x}-2{e}^{2x}$** |
| q-332905 | 4 | -1 | 5 | -1 | easy | **$-{e}^{-x}$** |
| q-332906 | 3 | -2 | 7 | 0 | easy | **$\frac{7}{5}{e}^{3x}-\frac{7}{5}{e}^{-2x}$** |
| q-332908 | 1 | 4 | 2 | 10 | easy | **$\frac{2}{3}{e}^{4x}+\frac{28}{3}{e}^{x}$** |
| q-332909 | -2 | -3 | -5 | 8 | easy | **$3{e}^{-2x}+5{e}^{-3x}$** |
| q-332936 | -2 | -2 | 8 | -1 | moderate | $-{e}^{-2x}+8x{e}^{-2x}$; **$(8x-1)e^{-2x}$** |
| q-332937 | 4 | 4 | -2 | 1 | moderate | **${e}^{4x}-2x{e}^{4x}$** |
| q-332938 | 5 | 5 | 15 | 1 | moderate | ${e}^{5x}+15x{e}^{5x}$; **$e^{5x}+15xe^{5x}$** |
| q-332940 | 2 | 2 | -10 | 0 | moderate | **$-10x{e}^{2x}$** |
| q-333160 | -3 | -3 | 12 | 1 | moderate | **${e}^{-3x}+12x{e}^{-3x}$** |
| q-333171 | 3 | 1 | 8 | 1 | easy | **$5{e}^{3x}-4{e}^{x}$** |
| q-332942 | 1 | 1 | 7 | 4 | moderate | **$4{e}^{x}+7x{e}^{x}$** |
| q-333174 | 5 | 5 | 4 | -1 | moderate | **$-{e}^{5x}+4x{e}^{5x}$** |


q-332903/q-332905/q-333171 substitute grouped `yp` and `yp′`, collect `(k−h)αe^(kx)`, evaluate that coefficient, and solve α: four rows. q-332906/q-332908/q-332909 print the already-distributed initial substitution and omit the redundant `(k−h)` row: three rows. q-333171 ends the α row with a period; the other grouped cases do not. These distinctions survive changed parameters.

All seven resonant solutions retain four derivative rows: the formal derivative of the full trial, extraction of α from the formal derivative, the explicit product-rule component sum, and collection into `α(1+kx)e^(kx)`. All retain four substitution rows, including the unreduced `1+kx−hx` before cancellation. Every complete solution then presents the particular solution, symbolic sum `yc+yp`, actual general solution, two initial-constant rows, and final solution. The exact shared sentences and full sequence are replayed byte for byte.

## 2. Generalize the shared assessed move

Choose the correct exponential trial, differentiate it, substitute into the given first-order ODE, determine its coefficient, add the complementary solution, and determine the remaining constant from the supplied initial condition. The blank asks for the full explicit RHS with no arbitrary constant. Source alternatives that differ by factoring or exponential brace spelling describe the same unique solution.

## 3. Components and complete banks

Parameters: h is the complementary exponential rate, k the forcing rate, f its nonzero signed coefficient, and v the initial value. For k≠h, α=f/(k−h), yp=αe^(kx), A=v−α. For k=h, α=f, yp=fxe^(hx), A=v. Every answer and every intermediate block is calculated from these operations; no source answer or final solution is looked up.

All banks contain correct blank-entry alternatives only; none requires a wrong-answer recipe. Each expanded member is `Ae^(hx)+yp` with A computed from the initial condition. q-332908 places the forcing term first in the answer bank while retaining complementary-first order in its worked solution. q-332936's second member is `(fx+v)e^(hx)`; q-332938's second member uses unbraced `e` and otherwise the same calculated terms. All 15 displayed expressions and all 13 available correct designations are compared independently. A missing designation is never counted as matched.

Decoded source bytes were checked directly: each `frac`, `alpha` and `begin` command starts with **one** byte 92; doubled serialized tool escaping is not evidence of doubled command slashes. There are no command-slash repairs. There are no mathematical source errors in these practice records. The two absent answer/solution sets are preserved exactly by raw public replay. Normal source profiles fill these sets using independently checked mathematics and explicitly authored easy/moderate labels; these completions have their own denominator (2), separate from the 13 available original solutions/designations.

## 4. Reusable masks, guards and authored extensions

The generator assembles complete mathematical components and fixed shared prose. It never replaces digits globally. Conditional masks control grouped/compact substitution rows, period placement, inline/display prompt style, negative/unit coefficients, a zero complementary term, forcing-first bank order, and the two equivalent source alternatives. Blank answer values omit math delimiters. Source metadata stays outside learner text.

Easy and moderate explicit domains: h,k are nonzero integers with absolute magnitude ≤6; f is nonzero with |f|≤15; |v|≤10. Easy enforces k≠h and moderate k=h. Default samplers use |f|≤12 and |v|≤8 and cover signed rates and signed forcing. Source values f=15 and v=10 remain valid explicit replays. The easy default domain contains 53,856 mathematical tasks; moderate contains 4,896.

Authored hard uses two distinct nonzero exponential rates, nonzero signed forcing coefficients of magnitude ≤12, the same |h|,|k|,|k2|≤6 bounds, and |v|≤8. `two_nonresonant` excludes both rates from h. `mixed` requires its first component to be resonant and its second nonresonant. The two families have equal-level reasoning: choose two supported trials, calculate one first derivative, equate two coefficients, and solve one initial constant. There is no progression within hard. Both guards apply to explicit calls as well as random samples. The default domains contain 6,462,720 unordered two-nonresonant tasks and 1,292,544 mixed tasks. Exponent order, variable spelling, presentation profile and bank alternatives do not inflate the mathematical fingerprint.

Curriculum evidence: the lesson route is reconstructed through `activity/first-step` and `step/next`: 17592186230044 → 30045 → 30046 (KP29162: two nonresonant exponentials) → 30047 (resonance discussion) → 30048 → 30049 (KP29163: one resonant plus one nonresonant exponential) → 30050 (KP29164: general solution) → 30051 (this IVP KP). Thus both hard families use methods that precede the initial-value assessment. Canonical IVP e-21617 supplies the initial-constant stage. Required background is homogeneous complementary solutions, exponential derivatives, the product rule, signed rational coefficient arithmetic and initial-condition substitution. No later general first-order/integrating-factor topic is used.

Hard solutions keep the full formal derivative, the product-rule component stages when applicable, substituted sums, distributed coefficients, reduced exponential coefficients, unsolved coefficient equations, solved coefficients, particular/general solutions, initial substitution and constant solve. The validator reads these actual displayed expressions independently and verifies the ODE and initial value again at the end. No plots are needed at steps 5/7.
