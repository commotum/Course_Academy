# Template extraction

## 1. Specific observations

The complete records in source.json preserve all original IDs, attribute presence, banks and prose. source-cases.json maps all 16 practices to complete explicit parameters. q-1953 uses u=x² and four chain rows. q-107437 uses u=x⁵+1 and four rows. q-107445 differentiates x²−2x, with a parenthesized two-term inner derivative. q-312451 differentiates 4x⁵. q-48629 uses constant-first 8−2x³ and omits the separate e^u reduction row. q-71873 is rated moderate and differentiates 2x⁴ with four rows; its observed label remains unchanged.

Tangent q-340948 has −2x⁶+5x at 1 and four endpoint rows including a repeated final value. q-340955 has −3x at 1/3 with four endpoint rows including repetition. q-107449 uses 3x²−3 at −1 and explicitly evaluates −6·e⁰ before −6. q-107452 uses x³−4x at 2 and only three derivative chain rows before its four endpoint rows. q-340949 uses 4x³ at 1 and three endpoint rows. These row structures are retained at changed parameters.

The two trigonometric composition sources omit f,h definitions in the captured prompt. Their solutions establish f(h)=(1/2)e^h and h(x)=−4sin x. The product layout requires −2cos x; the supplied minus and reciprocal exponential layout requires **positive** 2cos x. Their fragment criteria differ even though their complete derivative is the same. Raw evidence is underdetermined, not a self-contained learner question. Normal prompts supply the actual definitions and display the supplied product or negative reciprocal fraction explicitly around the widget, retaining the same coefficient/numerator answer and source solution chains. No doubled-slash anomaly is asserted: the decoded source strings have ordinary single TeX command bytes.

q-48628 is independently solved as 4x³e^(x⁴+1); the authoritative MA1007 Markdown also labels its key missing. Raw replay remains keyless, solutionless and unrated. Normal generation completes the key and full composition/derivative/operator/substituted/reduction/restoration solution.

## 2. Generalized family description

Differentiate e raised to a polynomial or the observed scaled sine composition by identifying the outer exponential and inner derivative, multiplying the components and restoring the original exponent. Some sources then substitute a familiar exact evaluation point to obtain a tangent slope. Blanks expect only the supplied derivative, slope or fragment. No extra learner diagnosis is introduced.

## 3. Complete components and banks

Write g=a x^n+b x+c, d=a n x^(n−1)+b, E=e^g, A=dE. Trig uses g=a sin x, d=a cos x, outer scale k; fragment is kd (product) or −kd (supplied minus reciprocal). For slopes t, V=d(t), W=g(t), A=V e^W. Each ordered list below is a complete observed profile; order is immaterial. Recipe intention is only claimed where defensible; opaque lists are structural parameterizations for public evidence, not normal learner banks.

| Profile | Complete parameterized bank |
|---|---|
| q-1953 | a x^(n−1)E; e^(ng); anE; A; g |
| q-48628 | an x^(n+1)E; d+E; A; an x^n E; an x^(n+1)+E |
| q-107437 (opaque) | −A; A; a x^n E; x^(n−3)E/n; (n−1)a x^n E |
| q-107445 | an x^n E; anE; (an x^(n−1)−b)E; A; an x^(n−1)E |
| q-48629 | −A; (c+d)E; −an x^(n+1)E; A; an x^(n+1)E |
| q-71873 (opaque) | an x e^(x^(n−2)); an x^(n−1)e^(x^(n−1)); (an+1)x^(n−2)e^(an x^n); A; n x^(n−2)E |
| q-107449 (opaque) | A; −Ve; Ve^a; −Ve^(−a); e/a |
| q-107452 (partially opaque) | −A; an t^(n−1); an t; b; A |

All eight blank profiles compute their single fragment exactly. Correct refs are present for 15 originals and absent for q-48628. Exact bank matching uses mathematical equivalence of every entire value, one-to-one; reproducing a scalar alone does not recover historical intent.

Normal derivative radio banks are authored from the assessed method: [dE, E, d, d+E, −dE], representing omitted inner differentiation, lost exponential factor, adding instead of multiplying components, and incorrect sign. Normal slope radio banks are [Ve^W, e^W, V, Ve^(−W), −Ve^W]. Each complete bank is selected before parameters and wholly rejected on equivalent options; no pooled first-valid replacements. One fixed worked solution is independent of every error.

## 4. Reusable masks, constraints and extensions

Each source mask replaces whole exponent, inner derivative, product, endpoint substitution, evaluated scalar-exponential and prose evaluation-point components longest-first through protected tokens. It never replaces a digit globally. This preserves conditional skipped rows and all repeated source stages. Formula banks are computed, never looked up. Changed-parameter tests use the public generate API and read actual learner mathematics back.

Normal polynomial coefficients are integers and have |a|≤4, 2≤n≤6, |b|≤5, |c|≤8, nonzero a, and the source component support (a missing or present b,c cannot silently collapse). Slopes use t∈{−2,−1,1,2}, |g(t)|≤12, |g′(t)|≤100, nonzero slope, rejecting complete radio collisions. Trig uses a∈{−2,…,−6} and k∈{1/2,1/3,2/3}. Every explicit call receives the same guards as sampling.

Authored missing hard retains e^g and tangent evaluation, with g=a x^n+b x²+c, n∈{3,4}, nonzero |a|,|b|≤3, nonzero |c|≤4, t=±2, the same evaluation bounds. This adds a second nonconstant power derivative and signed nonunit substitutions to the observed polynomial-sum/tangent workload, without another derivative rule or exponential base. It is a design claim, not an observed hard label. A full chain and separate arithmetic evaluation stages remain visible. Moderate derivative-only q-71873 retains its source label despite overlapping direct differentiation workload; labels are evidence, not retroactively corrected.

Task fingerprints canonicalize the assessed derivative and evaluation input, exclude bank profiles and seed/order, and do not count function-letter aliases. Additive exponent constants matter because they change e^g and hence the derivative. Content identities include actual prompt, fixed solution, actual difficulty, complete bank and canonical correct designation or explicit missing marker; observed omissions remain part of identity. Defaults select all eligible source-shaped families, with method-derived complete banks, before sampling.

The exact finite sampler catalogs contain 840 easy, 1,975 moderate and 264 hard meaningful tasks (3,039 across levels after removing overlapping derivative tasks), excluding syntax, profile and option-order aliases. These counts apply the complete method-bank eligibility and arithmetic bounds, not incidental seed shifts. The validator separately reports distinct tasks actually sampled.

The two trig fragment layouts require distinct correct fragments but assess the same complete derivative for fixed f,h; their mathematical fingerprints and catalog counts therefore merge that layout duplication while content identity and native fragment grading remain separate.

## Minimal normal presentation repair (revision 2)

Exact raw evidence is preserved in the wrappers. Served replay matches all16 normalized prompts and all15 captured solutions;15 prompts remain byte-exact, while q-167329 loses incidental indentation through shared normalization before IDs. In normal q-167329, incidental deep indentation is removed and the coefficient widget is followed by an explicit multiplication sign and e^g. In normal q-167783, the ambiguous legacy 2×2 table is replaced by dy/dx=−(numerator widget)/e^(−g). Ordinary parentheses span the math fragments around the widget. The supplied leading minus and reciprocal positive exponent are preserved. There is no new helper variable, bank, mathematical branch or worked-solution change. Validation reinserts the actual printed correct fragment into each complete displayed relation and independently checks equality with the derivative of the printed f,h, including changed parameters and sign/factor mutation regressions.


## Current-source additions

q-166076 supplies a full derivative blank, with correct value -2e^(-4 sin x) cos x; its four derivative rows also present the equivalent reciprocal-exponential form. Its reusable mathematical slots are a negative integer sine multiplier and a rational outer coefficient, with exactly the trig bounds already declared. The whole derivative, not either partial fragment, is the answer. All fixed prose and operative solution stages are retained. The prompt's missing definitions are completed in normal presentation; raw replay keeps the omission. There is no distractor bank.

q-340954 supplies y=e^(-2x^7), evaluates at x=1 and expects -14/e^2. Replay admits the observed seventh power and retains every derivative and evaluation row. Normal samples conservatively use the existing 2..6 exponent bound, integer coefficients and familiar nonzero integer evaluation points; this narrower sampling policy retains the same method and workload. Seventh-power replay is supported evidence, not a newly claimed difficulty level. There is no distractor bank.

Meaningful-task deduplication merges all three trigonometric layouts at identical f,h and merges derivative syntax aliases. All candidates are also compared against every current practice and canonical task, including seen and incomplete records; those records never become newly generated variants through identity or profile changes. The fixed sine input x is retained because general inner functions could add derivative operations absent from these source chains.


## Native-grader bound established during replenishment

Hard blanks now have exactly one field-owned canonical answer; no hidden distractor bank. All normal tangent samplers restrict the evaluated exponent to |g(t)| <= 12 while retaining |g'(t)| <= 100, nonzero slope and the previously declared structural bounds. This conservative policy follows a native grader failure for -72e^39 submitted as 0: the engine returned unresolved rather than rejected. Source replay remains unchanged and permits its observed parameters. This is a sampling capability bound, not evidence of a new difficulty or permission to alter the grader. The revised finite catalogs and current selected-instance native checks are recorded in validation.json and reference/replenishment.


## Private revalidation and native boundary

Primary basis1356 remains separate from supplemental basis2548; per-source replay metadata identifies the wrapper used. No independent inventory occurs. Shared prose is compared completely after replacing math spans; each normal source chain retains its differential-operator, substituted-product, intermediate inner-exponential, exponent-restoration and reciprocal-exponential stages as applicable. Evaluation chains retain unevaluated point substitution before numeric collection. Independent printed-math checks read both product operands, every row and all final expressions. The q-48628 authored completion has no observed solution to match. A C0 guard runs before IDs, with an independent corruption regression.

Actual native grading of changed q-166076 accepts its canonical derivative and independently unreduced chain form, and rejects0, but returns unresolved for wrong scalar1. The exact record, parameters, submission and result are retained in deep-native-input/report.json with current binary provenance. This incomplete wrong-entry comparison is not a mathematically valid alternative and does not erase the observed complete-derivative family. It remains an explicit native compatibility limit; no grader changes or database registration are authorized.
