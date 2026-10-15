# Template extraction at math basis 2275

The immutable source.json contains every original complete record. Templates use the original instructional prose and exact ordered operative stages; raw TeX spelling is presentation-normalized. No anchor branch returns a copied question. The same layout and bank functions serve anchors and changed numeric parameters.
## natural_integer_radio: q-13751

1. Original: Evaluate the integral ${\int }_{0}^{\sqrt{\operatorname{ln}⁡3}}5x{e}^{{x}^{2}}\,\text{d}x.$

Observed parameters: `{'c': 5, 'b': 3}`. Field: :answer-field.type/radio. Full solution present.

2. Shared pattern and purpose: c*x*exp(x²), endpoint sqrt(ln b); substitute x², extract c/2, evaluate e^(ln b)-1.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `selection`: `$\frac{15}{2}$`
- `selection`: `$3$`
- `selection`: `$2\operatorname{ln}⁡3$`
- `selection`: `$5$` (original correct)
- `selection`: `$\operatorname{ln}⁡3$`

4. Stable backbone and variable slots: `{'c': 2, 'b': 2}` through `{'c': 9, 'b': 9}`, inclusive Cartesian ranges as implemented by parameters_for. 64 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## natural_fraction_radio: q-30953

1. Original: Evaluate the integral ${\int }_{0}^{\sqrt{\operatorname{ln}⁡5}}\frac{1}{5}x{e}^{2{x}^{2}}\,\text{d}x.$

Observed parameters: `{'d': 5, 'b': 5}`. Field: :answer-field.type/radio. Full solution present.

2. Shared pattern and purpose: x*exp(2x²)/d, endpoint sqrt(ln b); extract 1/d then 1/4, reduce the endpoint fraction.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `selection`: `$\frac{1}{20}$`
- `selection`: `$\frac{6}{5}$` (original correct)
- `selection`: `$\frac{1}{5}$`
- `selection`: `$6$`
- `selection`: `$\frac{3}{20}$`

4. Stable backbone and variable slots: `{'d': 2, 'b': 2}` through `{'d': 9, 'b': 9}`, inclusive Cartesian ranges as implemented by parameters_for. 64 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## shifted_natural_blank: q-350740

1. Original: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\sqrt{\operatorname{ln}⁡2}}x{e}^{3{x}^{2}+\operatorname{ln}⁡2}\,\text{d}x=$
{{field-1}}

Observed parameters: `{'b': 2, 'k': 3}`. Field: :answer-field.type/blank. Full solution present.

2. Shared pattern and purpose: x*exp(k*x²+ln b), endpoint sqrt(ln b); both transformed bounds contain ln b.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `field-1`: `$\frac{7}{3}$` (original correct)

4. Stable backbone and variable slots: `{'b': 2, 'k': 2}` through `{'b': 6, 'k': 4}`, inclusive Cartesian ranges as implemented by parameters_for. 15 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## quadratic_scaled_base_radio: q-30977

1. Original: Evaluate the integral $\displaystyle \int_{0}^{1}x2^{3x^{2}}dx$.

Observed parameters: `{'b': 2, 'k': 3}`. Field: :answer-field.type/radio. Original solution absent; separately authored substitution, differential, table, base primitive, endpoint-difference chain.

2. Shared pattern and purpose: x*b^(k*x²), unit interval; substitute k*x², account for 2k and ln b.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `selection`: `$\frac{7}{3\ln 2}$`
- `selection`: `$\frac{7}{6\ln 2}$`
- `selection`: `$\frac{1}{6\ln 2}$`
- `selection`: `$\frac{7}{2\ln 2}$`
- `selection`: `$\frac{1}{8\ln 2}$`

4. Stable backbone and variable slots: `{'b': 2, 'k': 2}` through `{'b': 6, 'k': 4}`, inclusive Cartesian ranges as implemented by parameters_for. 15 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## square_base_radio: q-30978

1. Original: Evaluate the integral ${\int }_{0}^{1}x{4}^{{x}^{2}}\,\text{d}x.$

Observed parameters: `{'b': 2}`. Field: :answer-field.type/radio. Full solution present.

2. Shared pattern and purpose: x*(b²)^(x²), unit interval; extract 1/2, evaluate the base primitive, reduce ln(b²) to 2ln b.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `selection`: `$\frac{4}{3\operatorname{ln}⁡2}$`
- `selection`: `$\frac{4\operatorname{ln}⁡2}{3}$`
- `selection`: `$\frac{3\operatorname{ln}⁡2}{4}$`
- `selection`: `$\frac{3}{4\operatorname{ln}⁡2}$` (original correct)
- `selection`: `$\frac{3}{\operatorname{ln}⁡2}$`

4. Stable backbone and variable slots: `{'b': 2}` through `{'b': 9}`, inclusive Cartesian ranges as implemented by parameters_for. 8 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## quadratic_base_blank: q-346400

1. Original: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1}2x\cdot {3}^{{x}^{2}}\,\text{d}x=$  
{{field-1}}

Observed parameters: `{'b': 3}`. Field: :answer-field.type/blank. Full solution present.

2. Shared pattern and purpose: 2x*b^(x²), unit interval; du=2x dx, direct base primitive and two endpoint arithmetic stages.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `field-1`: `$\frac{2}{\operatorname{ln}(3)}$` (original correct)

4. Stable backbone and variable slots: `{'b': 2}` through `{'b': 12}`, inclusive Cartesian ranges as implemented by parameters_for. 11 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## linear_base_blank: q-350743

1. Original: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1}2\cdot {3}^{2x+1}\,\text{d}x=$  
{{field-1}}

Observed parameters: `{'b': 3, 'k': 2, 'h': 1}`. Field: :answer-field.type/blank. Full solution present.

2. Shared pattern and purpose: k*b^(kx+h), unit interval; matched derivative, shifted integer u bounds, direct base primitive and endpoint powers.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `field-1`: `$\frac{24}{\operatorname{ln}(3)}$` (original correct)

4. Stable backbone and variable slots: `{'b': 2, 'k': 2, 'h': 1}` through `{'b': 6, 'k': 4, 'h': 3}`, inclusive Cartesian ranges as implemented by parameters_for. 45 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## exponential_ratio_blank: q-350751

1. Original: Evaluate the following integral. Do not round the answer.

${\int }_{\operatorname{ln}⁡2}^{\operatorname{ln}⁡5}\frac{12{e}^{x}}{3{e}^{x}+1}\,\text{d}x=$  
{{field-1}}

Observed parameters: `{'a': 3, 'c': 4, 'h': 1, 'l': 2, 'r': 5}`. Field: :answer-field.type/blank. Full solution present.

2. Shared pattern and purpose: a*c*exp(x)/(a*exp(x)+h), ln(l) to ln(r); denominator substitution, factor c, logarithmic primitive, positive endpoint log ratio.

3. Components: original integral, substitution u, formal derivative and differential relation, two-row limits table, source-specific aligned integration stages, exact final scalar. Every bound, exponent, factor, endpoint power, and bank operand derives from the same supplied slots. Complete original bank values:

- `field-1`: `$4\operatorname{ln}(\frac{16}{7})$` (original correct)

4. Stable backbone and variable slots: `{'a': 2, 'c': 2, 'h': 1, 'l': 2, 'r': 5}` through `{'a': 5, 'c': 6, 'h': 3, 'l': 4, 'r': 8}`, inclusive Cartesian ranges as implemented by parameters_for. 720 bounded parameter sets before whole-bank exclusions. No optional operators/branches, new fields, or extra reasoning stages. Positive integer bases, positive rational coefficients, and finite ascending real bounds keep all logarithms and ratio denominators valid. Fixed powers x², derivative proportionality, field contract, limits layout, and ordered stages retain this family’s assessed skill. Linear degree and quadratic degree remain fixed because changing them would alter the source mask. Numeric base/scale/shift/endpoint values are not essential to the method.

## Complete banks and interpretation limits

Source-bank profiles preserve the observed values together, never a pooled set. In the expressions below A is the independently computed correct integral. These are empirical expression transports, not claims about the original author's intended error.

| Family | Complete source-bank recipe, in captured order |
| --- | --- |
| q-13751 | c*b/2; b; 2ln b; A=c(b−1)/2; ln b |
| q-30953 | 1/(4d); A=(b²−1)/(4d); 1/d; b+1; (b−2)/(4d) |
| q-30977 | (b^k−1)/(k ln b); A=(b^k−1)/(2k ln b); 1/(2k ln b); (b^k−1)/(2ln b); 1/(b^k ln b) |
| q-30978 | B/((B−1)ln b); B ln b/(B−1); (B−1)ln b/B; A=(B−1)/(4ln b), B=b²; (B−1)/ln b |

All 20 original radio values and all 4 blank values match mathematically at original parameters; every choice and designation is checked. q-30977's mathematically correct result is (2³−1)/(6ln2)=7/(6ln2). The original lesson widget independently confirms its complete five choices but supplies neither rating nor a solution/correct designation. We infer the result with a displayed derivative and primitive calculation and record the missing designation separately.

The opaque empirical profiles are publicly replayable through source_bank, with whole-instance rejection on every equivalence collision. They are not normal default banks. Default radios use one separately authored complete method bank: correct A; upper endpoint alone; omitted differential factor; reversed limits −A; half the proper scale A/2. The missing-differential factor is 2 for q-13751 and q-30978, 4 for q-30953, and 2k for q-30977. This is a bank extension only; it preserves each source's prompt and full worked-solution backbone. Reject the whole candidate if any pair collides. No individual option is replaced. Blanks retain one exact scalar and no distractors.

Source exact wording “Do not round the answer.” is preserved in source_presentation, restricted to its original anchor. The frozen native grader interprets “round” as a form restriction. Normal source_blank uses the semantically equivalent “Give an exact answer.” The public field shape and assessed response are unchanged. Exact raw strings stay in source.json; raw-copy-only replay is not used as served fidelity evidence.

## Curriculum calibration

The frozen lesson route follows Introduction → natural exponential products → other bases → More Complex Cases → Definite Integrals tutorial → this KP. It explicitly teaches three steps: substitution, changing bounds, and evaluation in u. The key prerequisite is topic1159, Calculating Definite Integrals Using Substitution. Its captured lesson teaches the same three steps for powers and rational denominators. Context copies are frozen under reference/. The hard source adds recognition of a logarithmic derivative plus nonzero log endpoints; only its existing positive denominator and integer endpoint workload varies. No integration by parts, improper integrals, sign-domain split, or new transcendental functions are introduced. There are no missing-level templates to author.

## Variation and identity

Each family is chosen before its bounded numeric parameters. All family/field masks appear in normal seeded generation. Source_bank selection remains separate from normal authored_method_bank. capacity.json reports eligible sets, complete-bank exclusions, unique prompt task fingerprints, and per-slot attained values. Content identity hashes the actual normalized prompt, full concrete solution, complete bank, field shape, and version. Seed and option order are excluded. The same mathematical given across bank profiles has the same task fingerprint. Template/profile aliases are not used to create extra identities. No plots or render assets require generation.

Native grading limitation: a valid general log difference such as `2(ln(11)-ln(5))` is unresolved against `2ln(11/5)` by the frozen engine. Supported unreduced endpoint ratios pass throughout the full hard domain. This is recorded separately from malformed input and ownership diagnostics and requires parent review; native grading is not claimed unrestricted.
