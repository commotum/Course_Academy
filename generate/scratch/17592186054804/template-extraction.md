# Four extraction stages

## 1. Specific source descriptions

| Source | Given roots in prompt; division order | Quartic; remaining quadratic | Response; complete bank |
|---|---|---|---|
| q-40091 | 1,−1; no recorded divisions | 12x⁴+17x³−6x²−17x−6; 12x²+17x+6 | Sum distinct; −1/3,−17/12,−1/6,−2/5,−11/9; designation absent |
| q-75795 | 2,−1; no recorded divisions | −4x⁴+15x²+5x−6; −4x²−4x+3 | Sum distinct; 0,−2,1,2,−1; designation absent |
| q-112638 | −3,1; first1 then−3 | x⁴+x³−35x²−57x+90; x²−x−30 | Sum distinct; 6,−2,5,−3,−1; correct−1 |
| q-270967 | 1,−1; first1 then−1 | x⁴−5x²+4; x²−4 | Four ascending blanks: −2,−1,1,2 |
| q-328522 | 3,−3; first3 then−3 | x⁴+x³−11x²−9x+18; x²+x−2 | Four ascending blanks: −3,−2,1,3 |
| q-337081 | −2,−3; first−2 then−3 | 9x⁴+42x³+37x²−28x−12; 9x²−3x−2 | Four ascending blanks: −3,−2,−1/3,2/3 |
| q-270970 | −3,−2; first−3 then−2 | −30x⁴−127x³−68x²+123x−18; −30x²+23x−3 | Four ascending blanks: −3,−2,1/6,3/5 |

Every original string/field/answer remains in source.json. Source-cases carries explicit known and remaining root slots, quartic leading scalar, template and raw bank profile. Blank field values are matched by key rather than arbitrary captured Pull order. q-270967 has an extra empty line before its second field; raw replay preserves it. q-328522's second-division lead ends in a period, unlike the other colon introductions. q-270970 reverses its two known factors in the second factorization. All retained.

## 2. Shared mathematical pattern

Infer two linear factors from given root identities; divide successively to obtain a cubic then quadratic; factor the quadratic into two real linear factors; equate factors to zero; return the sorted four root fragments or sum the distinct real roots. A Vieta-only sum solution would bypass the assessed factoring method and is not used. Every generated question has four distinct real rational roots. This conservative domain makes the observed four-blank contract sound and ensures the sum of distinct roots is not confused with multiplicity. Repeated-root canonical examples are method context, not permission to print four distinct-root blanks for only two distinct roots.

## 3. Components and complete banks

The quartic is built as `a(x−g0)(x−g1)(x−r0)(x−r1)`; every signed coefficient is expanded exactly. The first synthetic table records all five coefficients including zeros, multiply row and carry/add row. Its cubic quotient appears in the division fraction and first factorization. The second table records its four coefficients, multiply and carry/add rows; quadratic quotient appears in the second fraction and factorization. Primitive residual factors `(d0 x−n0)(d1 x−n1)` are multiplied by `a/(d0 d1)`. The final root row and sum row depend on the same root slots.

Observed q-112638 bank values can be replayed as `r0`, `g0+g1`, `−r1`, `g0`, and full sum. These descriptions reproduce every value but do not establish the original distractor author's intent. Its public profile `observed_sum_integer` is interpretation-limited and explicit. The normal `sum_method` uses one separately authored complete bank: full sum, known-root sum alone, remaining-root sum alone, sign reversal of both newly found roots, and omission of the second newly found root. Each wrong value is an operation on the actual factor-derived roots. Whole-instance rejection is required if any two values coincide; no per-option replacement pool.

Historical q-40091 raw bank response patterns are full sum times `[4/17,1,2/17,24/85,44/51]`; q-75795 uses known-root sum times `[0,−2,1,2,−1]`. These are explicit underidentified numerical-pattern recipes: mathematical replay only, **not** recovered error operations, not served defaults. They vary with root parameters and reproduce the entire bank at anchors; no literal payload return, answer lookup, or arbitrary polynomial fit is used. They retain missing correct refs. Independently derived mathematical correct values are −17/12 and0, reported separately; missing source designation counts stay missing.

Normal completed historical sums use the separately authored method bank above and the established source synthetic-division solution mask; no nonexistent historical solution is claimed as recovered. All original blank banks have exactly one field-owned scalar value per corresponding ascending root fragment and no feedback/distractors.

## 4. Reusable templates, slots, constraints

Fixed backbone: quartic, two supplied distinct integer roots, two full synthetic divisions, zero remainders, rational quadratic factorization, four distinct real roots, and the source answer contract. Source conditional grammar, factor ordering and colon/period distinctions remain in the appropriate family. Variable slots are complete mathematical components: `given=[g0,g1]`, `remaining=[r0,r1]`, `scale=a`. The eligible known-root identities vary; their original numerical values are not frozen targets. Prompt identities, factor-theorem prose, divisor factors, every table cell, all quotient/factorization rows, root values and final sum update together.

Normal known roots are nonzero integers −6..6. Easy quartics are monic with four nonzero integer roots of magnitude ≤6 and absolute displayed coefficient ceiling150; opposite-pair family requires g0=−g1 and r0=−r1. Moderate has two reduced residual fractions whose sum is nonzero (retaining the observed quadratic middle term), with the same denominator2..4, numerator magnitude≤5, scale±d²; hard has two residual fractions with different reduced denominators2..6, numerator magnitude≤5, scale±d0d1. Both have absolute coefficient ceiling650. The bounds apply to reduced fractions and to explicit API inputs as well as samplers. Different denominators entail unlike factor coefficients and fraction comparisons; same denominator entails the observed moderate workload. These arithmetic extensions preserve exactly the two divisions/factoring stages and familiar small rational number forms.

Historical q-75795's normal family extends halves to the observed common-denominator moderate range; q-40091 extends its denominator3/4 pattern to the hard differing-denominator range. These authored level/design claims are not recovered labels. Raw source profiles are evidence-only, require explicit parameters and preserve original omissions/errors without normal learning eligibility.

Content identity includes difficulty, displayed prompt, fixed worked solution and complete bank/profile independently of seed and option order. Mathematical fingerprint excludes scalar multiples and both given/remaining root order, retaining the polynomial's root object and supplied known-root set because changing which two roots are provided changes instructional division work. Capacity.json enumerates admissible tasks without scalar/order/layout aliases; sum/blank response differences are reported separately rather than counted as new polynomials. Slot tests include changed known roots, remaining roots, scales and default family coverage.

The full-sum/remaining-only bank degenerates when the known-root sum is zero, as at q-40091. A second **complete** authored profile is therefore chosen before sampling: full sum, known-root sum0, negated full sum, first remaining root alone, second remaining root alone. It is eligible only for opposite known roots and requires all five values distinct. The first authored bank requires nonzero known-root sum. Random calls choose a complete profile first and resample the entire instance until its regime and distinctness hold; explicit parameters select their eligible regime deterministically unless a profile is supplied. This prevents per-option replacement and preserves normal generation of the historical opposite-root prompt. Capacity reports include separate sum-task counts after complete-bank eligibility, not only polynomial-domain counts.

Raw q-270970 retains its corrupt final-left polynomial as the observed coefficient-offset pattern `[38,153,69,−137,21]` relative to the correctly built quartic. This describes the source artifact only; it has no supported instructional interpretation and is never a learner/default error recipe. Its other stages and root values are parameterized normally. Changed raw evidence remains explicitly ineligible for learning.

Parent identity correction: presentation hashes use unordered whole banks and the designated mathematical value, excluding profile-name and internal choice-index aliases. Raw missing key/rating/solution presence remains part of the actual displayed contract.
