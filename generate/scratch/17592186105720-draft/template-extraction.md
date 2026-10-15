# Four extraction stages

## 1. Specific source descriptions

Each source's complete original prompt, field/layout, bank, key, difficulty presence, worked prose and rows is retained in `templates.json` under `raw_source`. `source-cases.json` records every original anchor. This includes the unrated original rather than silently omitting it. All independent inventory appears separately.

- q-15717: 8/(3x), positive irreducible fraction, moderate; constant-factor integration in two rows followed by four constant/log rows.
- q-15710: 5/(2x), positive irreducible fraction, moderate; two integral rows followed by three log rows, omitting the redundant +C row.
- q-29834: -5/(2x), signed irreducible fraction, moderate; same two/three row structure, negative log coefficient and C=-5/2 ln K.
- q-103603: 2x^-1, moderate, two/three rows; five options include two equivalent unit-slope log families.
- q-103605: (2x-1)/x, moderate; four separation/integration rows, four constant/log rows.
- q-49096: (6+7x)/x, unrated; five options, no correct ref, no solution. Normal completion uses the canonical example's four plus three ordered stages, not a claimed observed solution.
- q-103375: (1+3/(2x))^2, hard; expansion, sum/factor decomposition, unsimplified power rule, reduced primitive; then three constant/log rows.
- q-49067: (1+1/x)^2, hard; same arithmetic stages, with unit coefficients and omitted redundant factors. Two wrong options use ln(|K|x), whose domain excludes x<0.

## 2. Generalized backbone

Recognize the reciprocal term, perform only the source's sum/constant-factor/binomial expansion operations, integrate termwise, identify the nonzero log coefficient a, use C=a ln K for K>0, and combine ln|x|+ln K. The bank asks for the entire antiderivative family; additive constants and positive scaling of a log argument cannot create wrong answers. Domains are the separate connected intervals x>0 and x<0; a different arbitrary constant can be chosen on each. No identity is forced through zero or across a nonpositive logarithm argument.

## 3. Components and complete bank mapping

`extraction.json` lists every source value, exact parameterized recipe mask, index, key status, fixed prose and ordered mathematical masks. Recipes are algebraic errors in coefficient placement, sign, integrating a constant, reciprocal power, inserting K additively, or integrating before squaring. Their recovery is expression-level, not a claim about an individual learner's intention. Every bank is constructed whole before eligibility checks. No first-valid option pool exists.

The opaque/malformed elements remain raw ineligible evidence. q-103603's ln(K|x|/n) and ln(nK|x|) are equivalent modulo an arbitrary additive constant; normal output replaces the latter with -ln(K|x|), a sign error. q-49067 changes the two wrong |K|x arguments to K|x| for domain validity. q-49096's key is inferred by differentiation (a ln(K|x|)+bx); its normal worked solution is explicitly authored from the canonical example. Raw replay preserves all omissions. Source fidelity counts 40 values and seven existing keys; the eighth key was never captured and is not counted as matched.

## 4. Reusable templates and slots

The complete component masks in `templates.json` parameterize all occurrences in prompt, prose, arithmetic, primitives and banks. Shared prose and source row order are retained. Optional unit coefficients in q-49067 are omitted at n=1 exactly as in the original. Normalization changes bare ln/Unicode function markers to canonical TeX; original replay preserves bytes. Samplers and explicit API share the exact finite `domain(template)` lists:

- integer easy n in -24..-2 or 2..24;
- positive/negative half and positive third numerators d<n<=31, coprime with fixed observed denominator d;
- negative-power and linear-minus numerator n in 2..31;
- canonical-style positive linear numerator a,b in 2..12;
- half-integer binomial n odd in 3..31;
- integer binomial n in 1..15.

These keep observed number forms, the original number of terms, and the largest observed original numerator (8) within a bounded same-operation extension, with hard source coefficient3 and current inventory up to31 retained as contextual arithmetic ceilings rather than new difficulty evidence. Integer binomial n<=15 keeps log coefficient<=30, comparable to the half-integer form n<=31. The positive-numerator extension bounds keep both terms substantive. Domain capacities are enumerated, not claimed unlimited. Mathematical fingerprints omit banks, aliases and seed; content identities use difficulty, actual prompt, full solution, complete bank and key. Choices shuffle deterministically; order alone does not affect identity.
