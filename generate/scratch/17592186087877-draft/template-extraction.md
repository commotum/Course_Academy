# Four-stage extraction

## 1. Describe the original questions

The eight exact original records are preserved in source.json and exercised by public `generate(..., profile="raw:q-...")`. q17540 supplies y′+y=cos x; q8546 y′+2xy=2xe^(-x²); both lack difficulty, worked solution and correct reference. q17533 supplies xy′+xy=x². q335278 supplies y′−y/2=x³, with one erroneous positive sign in its distributed row. q17539 supplies x²y′+xy=x²cos x,x>0. q79818 supplies y′+y/x=e^x,x>0. q79819 supplies xy′+2y=1 without a domain. q335274 supplies y′+2xy=sin x.

All expect the entire equation d(yI)/dx=IQ through one five-choice radio field, preserving complete original banks. Six captured solutions contain the shared standard-form/identify-PQ/factor-definition/multiply/distribute/product-derivative stages. Sources needing normalization put that step first; already-standard equations retain their already-standard opening. Reciprocal k1 examples have four integrating-factor rows; k2 has five, including e^(ln(x²)). q17539/q79818 collect the RHS at distribution and final rewrite. q79819 retains the uncollected RHS product. q335274 retains its exponential-times-sine product. Raw replay preserves every complete string and every missing attribute at the original parameters.

## 2. Generalize the backbone

From A y′+B y=R, obtain P=B/A,Q=R/A, compute I=exp(∫P dx), multiply the complete standard equation, distribute its LHS, simplify IP where the source does, and rewrite the LHS as a product derivative. Do not integrate IQ or solve for y. I′/I=P provides the independent correctness test. Integrating factors are compared modulo nonzero constant multipliers on a connected valid interval. Full equation equivalence is checked after expanding the derivative and normalizing the y′ coefficient; it must not compare equation sides independently.

## 3. Map every complete choice bank

`bank-mapping.json` gives all40 original values/IDs/field ownership, complete multiplier recipes, correct-presence flags, and interpretations. Multipliers in original order:

| Source | Whole factor bank |
|---|---|
| q17540 | x, ln x, x² with malformed d/dx²,1/x,e^x |
| q8546 | e^x,2x,x²,e^(x²),x |
| q17533 |2x,e^x,2,e^(2x),x |
| q335278 |e^(-x/2),e^(x/2),−x/2,−1/2,2 |
| q17539 |e^x,x²,x,e^(-x),ln x |
| q79818 |x²,e^x,e^(-x),x,ln x |
| q79819 |ln x,x²,e^x,x,2 |
| q335274 |ln|2x|,x²,e^(2x),2x,e^(x²) |

Every option is `(yF)′=FQ`, except the explicitly malformed operator. Source q17533 factors2x/x, q8546 factors2x/x, and q335278 constant factors−1/2/2 each give equivalent wrong complete equations. Preserve these original ambiguities as ineligible raw evidence. The malformed q17540 denominator receives exact-byte fidelity only, with no asserted recovered semantic meaning. For missing keys, independently derive exp(x) and exp(x²) from the displayed P; these normal completion keys receive no original-key match credit.

Normal complete banks are method-derived operations, selected before sampling and rejected as a whole on any equivalent pair:
- Constant: correct exp(∫P), reverse the integrated exponent sign, double its coefficient (observed exp2x pattern), retain the primitive without exponentiating, exponentiate P without integrating.
- Reciprocal: correct x^k; double the logarithmic coefficient x^(2k); omit the reciprocal denominator before integrating exp(kx); reverse sign while omitting that denominator exp(−kx); retain the unexponentiated log.
- Monomial: correct exp(a x^d); reverse sign; exponentiate P without integrating; fail to increment the integrated exponent degree; retain x^d rather than exponentiate.
- q335274: its source-shaped complete log-absolute/power/exponential/linear-factor bank, with every multiplier tied to the actual P=2ax.

These are documented conservative operations, not a claim that single observations recover the original author's distractor code. No option-specific diagnosis is added to learner content.

## 4. Parameterized masks, slots and constraints

Exact raw profiles use source-masks.json, with complete forcing slots Q and, where necessary, supplied R. Historical P and all five factor components stay fixed; changing a/k in a raw profile is rejected rather than silently ignored. Every source has a meaningful forcing slot: n1..4 for power templates; b for cos/sin/exp; b,c for2bx exp(−cx²); c for c/x. Raw source formatting is rendered from these slots even at anchors; there is no source-ID branch returning a copied source question. The fixed prose and complete operative strings outside the Q/R slots remain exact. Existing source rating is retained, unrated originals omit difficulty, missing solution/key stays absent. All raw profiles explicitly set evidence_only=true, eligible_for_learning=false.

Normal profiles retain source prose and stage recipes, vary all declared P/Q slots, normalize through shared math_format before computing IDs, and undergo checked_math_content. Easy rational a is sampled from the entire finite reduced domain denominator≤3,magnitude≤4,nonzero. n1..4; familiar cosine frequency1..4. Moderate reciprocal k∈±1..±4, familiar frequencies and signed exponential/forcing coefficients |b|,|c|≤4; linear a∈±1..±3. Hard a∈±1..±3,b∈±1..±4,d2/3,scale2..4. Cosmetic negative cosine frequencies are accepted aliases, not extra task counts. Boolean/extra/missing/nonintegral inappropriate slots and out-of-bound values fail explicitly.

Positive-half-line assumptions are printed in normal reciprocal/division/log banks. Thus ∫k/x=k ln x and I=x^k are valid; no hidden |x| or sign branch is discarded. On a negative interval, k ln|x| and |x|^k differ from x^k by a nonzero constant sign for integer k, preserving factor convention; validator checks this independently. The q335274 raw ln|2x| option remains exact; normal log(|2a|x) is its positive-interval expression even when a<0. Exponential-factor families with no division/log use all real x.

The task fingerprint uses reduced P,Q, actual domain and normalization role, excluding seed, option order, bank aliases and incidental common scale. Content identity uses actual difficulty, prompt, fixed worked solution, complete displayed bank, version and domain. Fixed explicit parameters infer a compatible family deterministically when template is omitted. Each declared slot is swept while others stay fixed; scale changes presentation and retains the same task fingerprint. Structural regression controls must reject deletion of multiplication/distribution even when equal rows preserve the answer.

# Legacy normalized-profile eligibility

`observed_raw` was an older normalized replay profile. It is now rejected in both generate and _generate_normal, before any question record is constructed. Its factor recipe helper remains available for analysis/mapping, but it cannot create serving output. Public raw:q-... remains the exact source evidence contract and is always ineligible. The regression calls both record entrypoints for every template and requires a ValueError; normal validation also rejects malformed differential denominators and any equivalent pair.
