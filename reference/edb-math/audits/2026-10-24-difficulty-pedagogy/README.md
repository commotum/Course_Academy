# Difficulty should measure the target skill

Read-only review at database basis **T6441**. No question, generator registration, difficulty label, or learner record was changed. Further generator publication remains on hold following the user's difficulty concerns.

The review started with a catalog of 211 integration, substitution, and chain-rule KPs, then compared their imported-question counts. Selected references were checked for retirement and structural multistep exclusion. The primary benchmark below has two complete, active, standalone imported examples in every band. [Verification](benchmark-verification.json) records exact identities and counts.

## The flagged easy question

Question **17592186482724** asks for

\[
\int_0^{\pi/48}9\sin(24x)\,dx.
\]

It is generated, labeled easy, and already retired from fresh practice. Its mathematics is correct: \(u=24x\) gives bounds \(0,\pi/2\), with factor \(9/24=3/8\), so the answer is \(3/8\). Its record remains available for historical/saved work.

The numbers 24 and 48 do not automatically make it conceptually moderate: they cancel to a familiar angle. Nevertheless, this easy variant adds visual clutter, multiplication of fractions, and reduction of 9/24 without adding a useful substitution decision. A small-number variant can exercise the same skill more cleanly. The generator should control the work produced by its parameters, rather than treating every mathematically valid coordinate dilation as equally easy.

The earlier generated hard question **17592186676292** has a different problem. It combines fractional amplitude, fractional inner slope, a phase shift, awkward original bounds, quadrant signs, and unlike radical endpoint values. Those demands accumulate around a single linear substitution. That band was authored without imported hard anchors for the linear-trig KP; correctness and rendering checks did not establish appropriate difficulty calibration.

## Primary benchmark: a small, clear progression

KP **17592186064172**, **Integrating an Exponential Function With a General Base**.

It has **2 easy, 3 moderate, and 2 hard imported practice questions**. One moderate entry, q-31248 / 17592186064732, lacks its answer link and worked solution; it is excluded from the benchmark. The remaining **six complete questions provide two examples per band**. No selected source was retired or structurally excluded as a multistep part.

| Band | Imported questions | Entity IDs | Intended increase in work |
| --- | --- | --- | --- |
| Easy | \(\int3^x\,dx\); \(\int5^x\,dx\) | 17592186064932; 17592186250130 | Apply the general-base antiderivative rule directly. |
| Moderate | \(\int2\cdot9^x\,dx\); \(\int3\cdot2^x\,dx\) | 17592186250131; 17592186297341 | Carry an outside constant through the same rule. |
| Hard | \(\int(1/8)^x\,dx\); \(\int(1/3)^x\,dx\) | 17592186250132; 17592186573944 | Handle a reciprocal base and the sign of its logarithm. |

Source IDs are q-66139, q-113887, q-113890, q-31249, q-113893, and q-71910. Their complete questions, banks, and solutions are retained in [the imported snapshot](17592186064172/imported.json).

### What is effective

1. **A stable backbone.** Every question applies \(\int a^x\,dx=a^x/\ln a+C\). The exponent remains x. The hard examples do not simultaneously introduce a composite exponent, bounds, fractional outside coefficients, and another integration technique.
2. **A small, identifiable change between bands.** Moderate adds an outside constant. Hard changes the role of the base from a number above one to its reciprocal. This is a difficulty distinction within this narrow KP, rather than an attempt to make the entire problem formidable.
3. **Little incidental computation.** The answers retain \(\ln9\) and \(\ln8\); the learner need not approximate logarithms, evaluate large powers, or rewrite every expression into a CAS-preferred form. A numeral's role matters more than its size: 9 as an unevaluated base is different from a large denominator that must be combined with several other fractions.
4. **The extra conversion is actually explained.** Both hard solutions first give \((1/a)^x/\ln(1/a)+C\), then explicitly show \(\ln(1/a)=\ln1-\ln a=0-\ln a=-\ln a\). They finish at the same form used in the correct choice. This directly addresses the missing-conversion failure in the trig generators.
5. **The response demand stays stable.** All six are five-option radio questions. Their progression is not confounded by switching from recognition to unrestricted exact entry while retaining the same difficulty label.

These examples are useful design evidence, not proof that every imported question or every distractor is optimal. The extra incomplete moderate entry is a concrete reason not to equate imported provenance with readiness or quality.

## More direct evidence from substitution KPs

### Scaffolding can change the requested task

KP **17592186064209**, Calculating Definite Integrals of Algebraic Functions Using Substitution, has 3 easy, 5 moderate, and 6 hard active imported examples before content-quality review. Its full [snapshot](17592186064209/imported.json) also demonstrates why source labels require judgment.

Two useful easy examples are:

- q-49529 / **17592186332733**: given \(u=2x-1\), choose an equivalent integral for \(\int_1^3x\sqrt{2x-1}\,dx\). The question stops after transforming the integral; it does not require completing the power-rule integration.
- q-49532 / **17592186392689**: given \(u=3-2x^2\), choose the corresponding transformed integral. It likewise isolates rewriting the factors, differential, and bounds.

Moderate q-13191 / **17592186064497** asks for the complete evaluation of \(\int_{-2}^{0}x(x+2)^3\,dx\), with transformed bounds 0 and 2. Hard q-346393 / **17592186319096** requires rewriting the numerator of \(\int_1^6(3x+1)/\sqrt{x+3}\,dx\); the new bounds are deliberately 4 and 9, making their square roots integers. The hard question adds substitution/algebra work while choosing bounds that simplify the root evaluation. Its final answer is 22.

This is useful pedagogical scaffolding: a supplied substitution and a limited requested stage reduce the amount the learner must coordinate. Merely providing a long worked solution after an unsuccessful attempt does not provide the same support during the question.

Do not reproduce the whole KP indiscriminately. For example, easy q-49533 starts at x=0 with \(\sqrt{5x-3}\), so part of its stated interval is outside the real domain. Moderate q-12910 has swapped bounds in its first displayed equality. These were observed and recorded, not repaired in this review.

### A hard substitution question can have easy resulting arithmetic

The trig topic explicitly lists **17592186100874**, Calculating a Definite Integral of Function Using Substitution, in its prerequisite context. It has **7 easy, 3 moderate, and 6 hard imported questions**, with no structural exclusions in this review. Its [snapshot](17592186100874/imported.json) includes this particularly useful hard example:

\[
\int_0^1 8x^3(x^4+1)^2\,dx.
\]

This is q-336612 / **17592186311725**. Recognizing \(u=x^4+1\) is the main challenge. Then \(du=4x^3dx\), the outside factor is 2, and the bounds become 1 and 2:

\[
2\int_1^2u^2\,du=\frac{14}{3}.
\]

The harder recognition step is not accompanied by a difficult change of bounds or mixed-radical subtraction. The label reflects the form of the substitution, not a requirement that every component be harder. This KP also contains incomplete and arithmetically heavier examples; it is evidence to analyze, not a blanket gold standard.

## Proposed pedagogy for our trig generators

These are design proposals, not newly published questions or externally calibrated ratings.

### A conservative linear-trig progression

| Band | Example task | Target work | Support and arithmetic |
| --- | --- | --- | --- |
| Easy | Given \(u=2x\), choose the transformed form of \(\int_0^{\pi/4}2\sin(2x)\,dx\). | Match the differential and bounds. | Supply u; ask for the transformed integral only. It becomes \(\int_0^{\pi/2}\sin u\,du\). |
| Moderate | Evaluate \(\int_0^{\pi/4}3\sin(2x)\,dx\). | Choose u, carry one small reciprocal factor, and evaluate. | One factor, 3/2; familiar endpoint values. Answer 3/2. |
| Provisional hard | Evaluate \(\int_0^{\pi/2}2\sin(\pi-2x)\,dx\). | Coordinate a negative inner derivative and decreasing transformed bounds. | Keep coefficients small and use bounds \(\pi\) and 0. The phase keeps the transformed interval familiar. Answer 2. |

The hard example adds one target-specific condition, the orientation change. It does not add fractional amplitude, fractional slope, unfamiliar angle recall, or mixed-radical arithmetic. Its suitability still needs review against the exact lesson and prerequisite treatment of decreasing transformed bounds. The word “hard” here is relative to this narrow KP.

Sine/cosine, small coefficients, compatible intervals, and response formats can vary within a band. Those variations should preserve its target workload. Their combinations must be designed for the resulting work, rather than sampled independently and labeled afterward.

### Apply the same principle to the other three KPs

- **Reciprocal trig with linear arguments:** vary the four known derivative/primitive families. Choose endpoints with simple primitive values or supply the values when their recall is not being assessed. A negative derivative can be the added condition without simultaneously adding fractional slopes and unlike radicals.
- **Products:** use provided substitutions or clear derivative matches for introductory practice; require independent recognition next. Use the imported reciprocal-inner case for a harder recognition task with small coefficients. For definite questions, choose bounds for a simple transformed problem. Root bounds should remain grouped and legible.
- **Quotients:** start with a supplied denominator substitution and an obvious derivative match. Moderate can add one small derivative-factor adjustment. The source-supported rearrangement \((u-1)/u=1-1/u\) can be a harder case, while retaining simple arguments and unit coefficients. Show that rearrangement and any integration-constant change explicitly.

### Requirements before another publication

1. State the exact learner operation and what the prompt supplies for each family. Count work required before feedback, not just steps present in the worked solution.
2. Choose a target decision case before coefficients, functions, shifts, and bounds. Add one controlled target-specific difficulty at a time.
3. Keep incidental arithmetic small. Allow a simple reciprocal factor; avoid stacking independent fractions, awkward bound calculations, and unlike radicals. Validate the rendered parameters and the actual resulting calculation, not just raw sampling ranges.
4. Use the existing prerequisite scope. Preserve trig arguments. Give identities or evaluation values that would otherwise turn the exercise into a test of another skill; avoid introducing a new method just to fill a band.
5. Treat response format as part of difficulty. Exact entry removes answer-choice support. A radio-to-blank change needs its own pedagogical review.
6. Separate within-band variety from increased difficulty. Different valid functions and small coefficients provide useful practice without requiring a harder problem.
7. Review matched easy/moderate/hard examples and explain the single intended increase. Repeat that review on the actual batch surviving preparation and deduplication.
8. Keep mathematical correctness, grading compatibility, explanation completeness, and pedagogical calibration as separate checks. Passing the first three does not establish the fourth.
9. Record imported anchors and authored extensions separately. A missing hard band does not license manufacturing difficulty with arithmetic. If no appropriate hard form is established, leave it unsupported until one is justified.

The earlier replacement improved variety and mathematical consistency, but its authored hard bands and universal exact-entry response policy need this additional pedagogical review. No further pool changes were made while drawing these conclusions.
