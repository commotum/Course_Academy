# Instructional account

Source basis: 5277, KP 17592186184154, “Computing an Integral Using the Sum and Constant Factor Rules.” No diagrams occur; plot classification is none. The original candidate was retained for this repair. Review feedback identifies a denominator-conditioned exponent-rank shortcut; see the repair specification below.

## Learner operation and contract

Before selecting parameters, the learner must expand a two-term product or divide a two-term numerator, rewrite reciprocals/radicals as powers, separate the sum, extract constant factors, apply x^n → x^(n+1)/(n+1) to both terms, and combine with one integration constant. They must distinguish coefficient, exponent, and reciprocal-sign mistakes. Tutorial 703 (UUID 1b5ce4c9-ef44-52d9-a506-96aa15055e00) says to combine the constant factor and sum rules; tutorial 701 explains that the two arbitrary constants combine into C. Canonical example e-372 applies these stages to 2x^3−x. Prerequisites e-369/e-370 supply constant-factor and constant-function integration.

Supported/default band: moderate. Five complete moderate sources comprise two five-choice radio profiles and three one-field blanks. The blank is the antiderivative WITHOUT C, since the prompt supplies +C. Radio answers include +C. Preserve these response contracts, two nonzero terms, one variable x, and one constant. These are fixed to preserve the assessed operation, not because of repeated layout. Integer reciprocal powers and half powers never include exponent −1: logarithmic integration is outside these profiles. Half-power questions state x>0; rational questions state x≠0, and C applies on any interval in the domain. No diagrams or generated assets are needed.

Easy is not implemented in this package: q-2251 and q-29825 have no fields; q-132983, q-132779, q-133003 are orphaned multipart logarithm questions without y′ in the prompt; q-113787 is a complete easy radio but does not establish coverage of the other easy response families. Hard has no source evidence. q-211 and q-2166 have no difficulty, key, or solution; do not silently relabel them. Original labels remain in the captured source, not reassigned to generated questions.

## Source observations and exact banks

q-49059 (c3b5e67d-32a5-5a89-860d-1eeac5fbca6e): integrate (x^5+7)/x^2. With a=1,b=7,p=4 the entire bank, written as pairs (coefficient, exponent), is:

0. (a/p,p), (−b,−1): source key.
1. (a/(p−1),p−1), (−b,−2).
2. (a/(p−1),p−1), (−b,−1).
3. (a/p,p−1), (−b,−1).
4. (a/(p+2),p+2), (−b,−3).

All include +C. These reproduce all five source options, including the compound wrong-exponent cases. Error interpretations are exponent/denominator changes, not a claim about how an individual learner made them.

q-49063 (aa2d5333-814d-52c3-9ed1-e83660135b41): integrate sqrt(x)(2+x). With a=1,b=2 its complete bank is:

0. (2a/5,5/2), (2b/3,3/2): source key.
1. (2a/3,3/2), (−2b,−1/2).
2. (2a/3,3/2), (2b,−1/2).
3. (5a/2,5/2), (3b/2,3/2).
4. (a/5,5/2), (b/3,3/2).

These reproduce the two reciprocal-power errors, reciprocal power-rule multiplier error, and halved correct expression. Again all include +C.

q-167635 (221f7f46-e501-5c4b-9474-541896c7450d) and q-167587 (8913b80e-2bcb-5364-9080-3c746725b920) both ask for ∫f(x)/x^3 and key x−2/x, despite different A,B labels. Their solutions explicitly supply f(x)=x^3+2x. q-167617 (002408ea-9be6-53e5-9b20-0951e4cd4bad) supplies f(x)=2x^2−4 in its solution and keys 2x+4/x. No relation between A,B and f is available. Therefore a documented contextual repair replaces the unsupported A,B preamble with the explicit f from the worked solution. Replay preserves integral, complete answer bank, and solution mathematics; it cannot honestly claim literal prompt fidelity for these three records. Fix the omitted 1 in ∫1 dx in q-167587. Whitespace and redundant nested aligned environments are normalized.

Other source errors: q-132779 changes t²+1 to t²+3 between solution lines and omits absolute values without a positive-t assumption; q-133003 likewise needs positive t for its displayed real square roots. These excluded easy records are not used to infer a generator.

## Conservative extensions and answer-bearing roles

Numerical changes alone would preserve a median-coefficient shortcut in the radical source bank. Instead choose the eligible answer-bearing candidate first (index 0–4), then a,b and p, construct the complete source-shaped bank, and differentiate the chosen candidate to obtain the integrand. This reverse construction preserves the learner's forward method. No differentiation is requested from learners. It moves which exponent/coefficient/sign rule case is correct while keeping all original bank members available. Every candidate has two nonzero powers whose derivatives can be expressed as the same two-term quotient/product and integrated by the same power rule. This is an authored same-method extension, not an observed source parameter pattern.

For rational radios: p∈{3,4,5}, signed a∈{±1,±2,±3}, signed b∈{±1,…,±8}. The selected polynomial component and reciprocal assignment determine the numerator exponent and reciprocal denominator (2,3,4); the repair below varies these assignments independently. For radical radios: signed a,b∈{±1,…,±4}; selected indices 0,3,4 lead to sqrt(x)(A x+B), while 1,2 lead to (A x²+B)/(x sqrt(x)). The latter adds no term or integration operation; its two half powers are 1/2 and −3/2. Coefficients may be rational but remain small. Changing which factor is a reciprocal power is a conservative extension; rendering and coverage must include both forms. Polynomial components and radical answer pairs retain their source ordering internally, with shuffled choices for display. Quotient reciprocal components additionally vary by the mixed-component profile defined below.

Blank family: choose signs of two independent nonzero coefficients first, then degree d∈{2,3}, a∈{±1,…,±4}, b∈{±1,…,±8}. Supply f(x)=a x^d+b x^(d−2), divide by x^d, integrate a+b/x² to a x−b/x. Degree is irrelevant to the response after cancellation; signs and coefficients are relevant. Both numerator terms and the denominator update together. Degree 2/3 is justified by the source examples, and fixed reduced exponent −2 preserves their exact workload.

## Validation obligations

Replay all five moderate sources including 10/10 radio choices and 3/3 blank banks. Independently differentiate each answer and check one unique radio key. Cover every candidate role, coefficient sign pair, p, denominator, radical form, and blank degree; count semantic prompts rather than seeds or shuffles. Hold banks/parameters fixed while changing the selected candidate: prompt, answer and solution must change together, and the old selection must be rejected by the actual grader. For blanks, change b with a,d fixed, then change d with a,b fixed to test relevant response change and irrelevant response preservation. Choice order is another irrelevant change.

Probe first/last position, source candidate identity, coefficient median, answer length, and exponent-pattern rules separately within each family and radical form. Exponent matching to the actual integrand is legitimate power-rule reasoning; static exponent preference is incidental and must not be perfect. Run the same probes after the shared delivery filter. Generator rejection is only semantic duplicate resampling, with no decision-case exclusions. Inspect selection's same-band behavior read-only: all supported records are moderate, so positive moderate weight samples within that band; learner history and live policy are unavailable and cannot be certified. Save scripts, source replay, native grader cases/reports, counterfactual records, filtered records, and actual UI screenshots. These support separate fidelity, correctness, grading and variation claims, not a claim of exhaustive shortcut absence.

## Review repair specification (before implementation)

Review 1 correctly rejects the correlation “denominator x^4 → largest visible polynomial exponent.” Tutorial 703 requires integration of constant multiples, and q-49059 requires termwise division; neither requires that cross-term rank correlation. The old account incorrectly defended the denominator branches without checking the polynomial rank inside them.

Retain both radio families, all blank repairs, all original parameters, and exact source banks. Extend only the quotient bank: independently assign the multiset of reciprocal exponents (−1,−1,−1,−2,−3) to its five polynomial components. Choose the answer-bearing candidate and eligible component assignment before coefficient magnitudes. Keep every polynomial component and reciprocal coefficient −b. There are fourteen distinct internal assignments (seven unordered mathematical banks, since polynomial components 1 and 2 coincide) after excluding assignments that make the identical polynomial components at indices 1 and 2 share the same reciprocal exponent. That exclusion prevents duplicate choices; it is not a target-dependent filter. Swapping the two identical polynomial components is not counted as semantic variety; coverage reports count mathematical integrands separately from internal slot assignments. The source assignment remains directly replayable. Normal generation selects all fourteen assignments without target-dependent restrictions.

This is an explicit authored mixed-component bank extension: every option remains a sum of one polynomial power and one reciprocal power; derivative-based construction and forward worked solutions still require exactly two power integrations. The denominator can now be 2, 3 or 4 for each polynomial role, so its exponent no longer predicts polynomial rank. p in {3,4,5} keeps polynomial powers positive and arithmetic small; nonzero signed a,b keep both integration terms present. Fixed five-choice shape and +C contract preserve the source response workload. Reciprocal exponent matching to the integrand remains legitimate mathematical evidence, but does not impose a polynomial-rank preference. No claim is made that every radio requires both terms to eliminate all distractors.

Affected obligations: replay all original banks unchanged; test all fourteen assignments and all five targets at every p, including denominator-4 low/middle/high polynomial ranks; reject duplicate mathematical options; independently parse/differentiate served choices and solutions; test native grading when a changed target keeps the bank and denominator fixed. Hold a,b,p and the reciprocal assignment fixed for these counterfactuals, changing the target among equal reciprocal exponents; numerator, key, solution and native accepted response must change together. Recheck first/last, min/max visible exponent, polynomial rank, coefficient rank, length and fixed source role within denominator and p subgroups, before and after actual delivery filtering. Keep the existing radical and blank counterfactual regression. Test the actual sampler separately from controlled records and inspect same-band selection without writing any database state.
