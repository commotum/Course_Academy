# Authored complete banks grounded in the supplied equation

All formulas below are author metadata. The learner still sees the source-style prompt, a scalar choice bank and one shared fixed solution; no distractor feedback or diagnostic claim is added. Let u be the printed initial input and b the printed initial output. Each bank is selected from the function family and fixed unary/nonunit source layout **before** sampling. Each has the correct constant plus four specified wrong operations. Every member is constructed together. Any undefined/nonreal member or equivalence collision rejects the **whole instance**; no member is replaced, no other profile is tried after seeing the parameters, and explicit invalid instances raise `ValueError`.

| Selected bank | Actual substitution | Correct A | Four wrong operations and their complete scalar results |
|---|---|---|---|
| Power, n≥2 | b=A uⁿ | b/uⁿ | multiply rather than divide: b uⁿ; omit exponent: b/u; read uⁿ as n u: b/(n u); read uⁿ as u+n: b/(u+n) |
| Unary power | b=A u | b/u | multiply rather than divide: b u; omit input factor: b; invert the isolation quotient: u/b; invert b before dividing: 1/(b u) |
| Reciprocal power, n≥2 | b=A/uⁿ | b uⁿ | divide rather than multiply: b/uⁿ; omit exponent: b u; read uⁿ as n u: b n u; read uⁿ as u+n: b(u+n) |
| Unary reciprocal power | b=A/u | b u | divide rather than multiply: b/u; omit input factor: b; invert b before multiplying: u/b; invert the whole isolated product: 1/(b u) |
| Exponential, F=exp(k u) | b=A F | b/F | multiply rather than divide: b F; omit F: b; invert the isolation quotient: F/b; invert b before dividing: 1/(b F) |
| Cosine, F=cos(k u), G=sin(k u) | b=A F | b/F | multiply rather than divide: b F; omit F: b; evaluate sine rather than cosine: b/G; invert the isolation quotient: F/b |
| Sine, F=sin(k u), G=cos(k u) | b=A F | b/F | multiply rather than divide: b F; omit F: b; evaluate cosine rather than sine: b/G; invert the isolation quotient: F/b |
| Reciprocal affine, c=k u | b=1/(A+c) | 1/b−c | wrong shift sign: 1/b+c; omit inversion of b: b−c; subtract shift before inversion: 1/(b−c); negate reciprocal before subtracting: −1/b−c |
| Logarithmic affine | b=ln(A+u) | exp(b)−u | wrong shift sign: exp(b)+u; omit exponentiation: b−u; subtract input before exponentiating: exp(b−u); negate exponent before subtracting input: exp(−b)−u |

Sine source layouts are blanks, so the sine recipe is documented alongside cosine but no radio layout is newly introduced. Blank generation keeps the single exact scalar answer and unchanged solution stages.

The unary power bank is fixed to q-141114's linear source layout; the unary reciprocal-power bank is fixed to q-141112. Other normal radio power profiles require n≥2. Their coefficient is never silently changed: an incompatible explicit input rejects, and an incompatible sampled instance rejects before the next draw. Observed/completed source profiles preserve their original numerical banks and coefficient domains, including opaque proportional profiles. They remain evidence only.

Examples of whole-bank rejection include exponential u=0 (F=1 makes omission/multiplication correct), unary power u=±1 (multiplication equals division), equal sine/cosine values at π/4, reciprocal-affine u=0 (the wrong shift sign vanishes), logarithmic u=0 (moving the shift before/after exponentiation coincides), and selected nonunit-power evaluations where n u happens to equal uⁿ. There is no fallback bank. Random samplers reject these entire draws; explicit calls reject them with a clear error.

`validate.py` reconstructs each normal radio bank independently from the actual displayed supplied function and initial condition, not from the generator's saved parameter values or selected IDs. It then compares all five actual displayed choices one-to-one, verifies the correct designation, checks the ODE and ordered worked stages, and uses the native grader on every option. `number-domains.json` records finite eligible radio counts separately from the union of all normal layouts. The easy union changes from 3,814 to 3,808 because log has only a radio layout and loses its six u=0 cases. Other easy families retain blank layouts that cover their original finite support; individual radio banks have smaller valid supports. Moderate and hard are blank layouts, so their 384 and 216 task counts are unchanged.

The finite-domain audit finds 176 eligible nonunit-power radio tasks, 76 unary-power, 220 nonunit reciprocal-power, 76 unary reciprocal-power, 1,008 exponential, 168 cosine, 320 reciprocal-affine and 24 logarithmic tasks. It constructs each selected bank in full and checks all mathematical members; finite support is not inflated by layout/profile aliases or shuffling.
