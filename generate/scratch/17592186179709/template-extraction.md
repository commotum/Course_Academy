# Four-stage extraction

## 1. Specific observations

q-122139: y²=-16x, density 32xy, y interval [-8,4], supplied exterior factor -1/4, missing integrand radio. Prompt uses legacy `AAAAA` and `\int_(C)` notation. No label, solution, or correct ref.

q-122446: x=2y³, density xy², endpoints (0,0),(16,2), illustrated. Full integral radio; no label, solution, correct ref.

q-122530: easy line 3x=y, density 9x²y, [0,9], supplied √10/3; missing scalar polynomial. Solution isolates x, parameterizes, formal coordinate derivative, evaluated derivative, formal metric, square/fraction/common-denominator/radical metric stages, three scalar substitution rows, three integral rows.

q-122534: moderate x=ln y, density eˣy², positive interval [1,e²], illustrated. Already isolated opening; metric passes through absolute t and uses positive t. Three density rows; three integral rows.

q-149714: moderate x/2=ln y, density 4y e²ˣ, [1,e], illustrated. Initial isolation; shorter speed reduction than previous log family; four density rows, including a repeated original f(x,y) before substitution; three integral rows.

q-122542: moderate x=2/y, density 4xy², [1,6], illustrated. Negative derivative; speed denominator t²; two density rows; three integral rows.

q-122527: easy x/2=1-3y/2, density 2x-3y, [0,2], exterior √10; initial isolation, negative slope, four metric rows after formal metric, two density rows, three integral rows.

## 2. Shared pattern

Express the supplied curve as x=g(y), set y=t, use the endpoints' y coordinates as bounds, compute r′=(g′,1), speed √(g′²+1), substitute the density and combine. A missing-integrand response requests the actual scalar expression under the supplied factor; full integral responses request a definite integral. These criteria are checked separately. No numerical evaluation is requested.

## 3. Complete component and bank inventory

`source.json` preserves all original strings, UUIDs, attribute presence, and bank co-occurrence. `source-cases.json` maps every source to a public template and profile. `bank-inventory.json` lists each original choice with its exact symbolic expression, bounds, field, correct designation presence, and uniform-scaling operation. Every five-choice bank is kept together; no choice is silently substituted.

The recovered expression patterns do not establish distractor intent. In particular the easy banks' unrelated constants cannot be justified as generic mistakes. The observed profile scales the whole density by c and correspondingly scales every historical option and scalar-density solution stage. This is a genuinely parameterized linear operation on the same fixed curve and preserves the historical patterns, with c integer 1..5. It is evidence only, even when mathematically repaired/completed. No opaque bank is a normal default.

## 4. Reusable templates, masks, constraints

Historical prompts use complete density components; every density substitution row and final integral row is scaled as a complete grouped mathematical object. Curve, derivative, speed, endpoints, source plots, solution sentences and stage ordering remain fixed. At c=1 the operation is the identity and the complete source strings match exactly. There is no source-payload shortcut or answer-key lookup branch. Raw public profiles retain omitted difficulty/solution/correct refs. Completed profiles explicitly infer missing labels/keys and replace `AAAAA`/legacy integral notation; their teaching eligibility remains false.

Authored easy uses x=at+b and kxᵘyᵛ, a signed nonzero integer with |a|≤4, b∈[-4,4], k∈[1,5], u∈{1,2}, v∈[1,3], integer 0≤lo<hi≤5. Constant metric is supplied; requested fragment is density after substitution. Moderate uses x=atⁿ, n∈{2,3}, b=0, and requests the complete integral with variable metric. Hard is an explicitly authored missing-level extension: x=atⁿ+b, nonzero shift |b|≤4, n∈{2,3}, u=2. It requires retaining the shifted square during substitution plus nonlinear derivative/metric; it introduces no new calculus method. Hard cannot admit unshifted or first-degree easy/moderate instances. All explicit inputs use the same guards as samplers.

Complete authored banks are method operations chosen before sampling. Easy: correct substitution; omitted y factor; omitted curve shift; interchanged density powers; reversed slope sign. Moderate/hard: correct; omitted y factor; omitted x power; omitted metric; omitted exponent multiplier in derivative. A collision rejects the entire instance. Full integral choices must also have unequal scalar values, checked by independent high-precision quadrature; same bounds/unequal integrands alone are insufficient. Arithmetic ceilings match familiar polynomial substitution already in sources and prerequisites. Negative coefficients are allowed without bare double signs; u=2 prevents the hard shifted substitution demand from vanishing.

Normal solution retains common formal operator, substituted derivative, metric, literal density substitution, reduced density, and three integral stages. Source-specific historical solution stages are preserved exactly only in historical replay, including the five different row sequences. No learner distractor diagnosis is added.

Identity includes version, level, actual prompt, fixed solution, field shape, complete displayed bank and correct-ref presence, excluding option order/seed. Mathematical fingerprint excludes banks/profile and incidental source layout but includes supplied factor/fragment versus whole-integral assessment. Numerical bounds belong to the mathematical task. Runtime metadata records actual Python and SymPy versions.

## Normal source-shaped families added after independent scope review

These five families preserve the rated originals' prompt demand and solution prose/stage sequence while replacing opaque banks with complete method-derived banks. All are normal eligible learning output, unlike historical replay. Their optional curve illustrations are omitted; the equation and both endpoints remain explicit. The source-specific rearrangement opening is used for the fractional line, affine line and scaled-log curve; the already-isolated opening is used for log and reciprocal curves. Complete math blocks are slots, and the introductory domain and density equations are separately substituted. No short token replacement crosses prose or coordinate components.

| Normal template | Parameters and bounds | Complete authored bank operations |
|---|---|---|
| `authored_line_monomial` | mx=y; m=2..5, density k m²x²yᵛ; k=1..4, v=1..3; y start 0..1 and end 2..9 | correct; first-power rather than squared denominator for x²; omit y factor; use x=mt; use x(t) for the y factor |
| `authored_affine` | x/b=1+ay/b; signed 1≤abs(a)≤4, b=1..4, density Px+Qy; P=1..4, signed 1≤abs(Q)≤4; y start 0..1 and end 2..5 | correct; omit Qy; omit x intercept; reverse Q sign; interchange x/y coordinates in density |
| `authored_log` | x=a ln y; a=1..4; k eᶜˣyᵛ; k=1..5,c=1..2,v=1..3, ac+v≤7; y bounds eˡᵒ to eʰⁱ, lo=0..1, hi=2..3 | correct; omit exponential substitution; omit metric's denominator t; use (ln t)′=1; use endpoint x coordinates as t bounds |
| `authored_scaled_log` | x/a=ln y; a=2..4; same density rules, v=1..2 and ac+v≤7; lo=0..1, hi=1..3, lo<hi | same complete method bank, with initial isolation and the original four density stages |
| `authored_reciprocal` | x=a/y; a=2..4; kxyᵛ, k=2..5,v=2..3; positive y start 1..2, end 3..6 | correct; omit x numerator scale a; omit density coefficient k; omit metric denominator t²; use endpoint x coordinates as t bounds |

The monomial fractional line retains all eight derivative/metric rows and three density rows of q-122530. Affine retains seven derivative/metric rows and two density rows; isolated log retains nine and three; scaled log retains seven and four; reciprocal retains eight and two. Every family retains three final integral rows. Independent QA parses each actual displayed row, verifies all endpoint coordinates against the printed curve, checks original row counts, and tests native grading separately. Bounds are enforced on explicit calls, and all complete integral banks reject equal scalar values even when their setup expressions differ. Every normal template receives two review examples and twelve explicit per-template QA instances in addition to forty-eight random instances per level.

CLI Markdown now labels author review as Original or Generated, includes the actual difficulty or source Unrated omission, and marks each owned correct option. The missing original correct designations remain labeled absent.

Reciprocal v=1 is excluded from the authored complete bank: f=kxy is constant on xy=a, and the x-bound distractor describes the reflected segment with exactly equal arc length. This is a real whole-integral equivalence, not merely a structural difference. The source v=2 remains supported. Generator and independent QA convert exact rational bounds to 40+ digit mpmath values rather than binary floats, so this symmetry cannot pass as numerical noise.
