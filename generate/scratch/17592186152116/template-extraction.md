# Four-stage extraction

## 1. Specific source descriptions

| Source | Printed inputs | Response | Solution shape / anomalies |
|---|---|---|---|
| q-218482 | 6(w - 8),15(w - 8), spaces around subtraction | one blank, space before placeholder | no captured answer/key/rating/solution |
| q-76238 | 3(x - 1),5(x - 1), spaces around subtraction | five radio expressions | no captured correct designation/rating/solution |
| q-111582 | 2(z-4)²,7(z-4)² | five radio expressions | common source opening, numerical multiple lists (including omitted middle multiples and missing thin space before16), numeric LCM14, formal common-part LCM, product14·(z-4)² and final expression |
| q-221994 | 4(y-3),9(y-3) | blank without space before placeholder | same five prose components; list nine multiples of4 and six of9; LCM36; final period |
| q-221998 | 3(y+7)²,9(y+7)² | blank without space before placeholder | lists four multiples of3 and three of9; LCM9; no final display period |
| q-221999 | 4(z-1)²,10(z-1)² | blank without space before placeholder | lists six multiples of4 and five of10; LCM20; no final display period |
| q-76409 | 10(y+1),15(y+1), period inside second math span | five radio expressions | lists four multiples of10 and three of15; LCM30; final period |

All inputs are positive integer multiples of an identical primitive monic binomial or its identical square. Coefficients are content, not leading coefficients of an arbitrary nonprimitive factor. Variables x,y,z,w are independent single polynomial variables. Correct blanks require a complete expression rather than a coefficient fragment.

Decoded TeX bytes are checked directly. The captured strings have one backslash byte before `text` and `cdot`; no doubled-backslash or control-character repair is warranted. Missing spaces are faithfully reproduced in observed profiles, including q-111582's multiple-list masks. No source mathematical or presentation correction was needed in the five complete records.

## 2. Generalized pattern and boundary

Given P=aF and Q=bF, where F is the identical positive-leading primitive polynomial, compute l=lcm(|a|,|b|), retain F once and return lF. Canonical example4(x+1),6(x+1) gives12(x+1), fixing the integer-content convention. A rational-unit/monic answer such as x+1, an extra integer multiple24(x+1), or a negative associate is not the requested normalized answer. SymPy ZZ polynomial LCM and native blank equality both support this convention; divisibility alone is insufficient.

The linked lesson route follows activity first-step17592186152992 and successive step/next: introduction → this KP17592186152116 → single-variable independently differing powers KP17592186152117 → multivariable KP17592186152118 → three inputs KP17592186152119. The prerequisite is monomial LCM topic17592186048209. Those later branches establish exclusions, not licenses for authored hard. Hard keeps one common three-term primitive polynomial and requires only integer-content/GCF extraction, followed by the same operation sequence. Factoring that quadratic is unnecessary and is never included in solutions.

## 3. Complete component/bank maps

Let F=(v+h)^n, l=lcm(a,b), g=gcd(a,b). The following is the full field-owned source mapping; answer values are mathematically parameterized, not lookup tables.

| Profile | Original options → parameterized operations | Original correct designation |
|---|---|---|
| observed_q-76238 | 30(x-1)² → 2lF²; 30(x-1) → 2lF; 8(x-1) → (a+b)F; 15(x-1) → lF; 15(x-1)² → lF² | absent; independent derivation selects15(x-1) only in derived profile |
| observed_q-111582 | 9(z-4)² → (a+b)F; 14(z-4)² → lF; 28(z-4)⁴ → 2abF²; 28(z-4)² → 2abF; 14(z-4)⁴ → lF² | 14(z-4)² |
| observed_q-76409 | 30(y+1)² → lF²; 150(y+1)² → abF²; 150(y+1) → abF; 30(y+1) → lF; 25(y+1) → (a+b)F | 30(y+1) |
| observed_q-221994 | 36(y-3) → lF | captured |
| observed_q-221998 | 9(y+7)² → lF | captured |
| observed_q-221999 | 20(z-1)² → lF | captured |
| observed_q-218482 | no choices or key | independent derivation30(w-8) only in derived profile |

The doubled-content2l and2ab choices are explicit parameterized replay patterns with unresolved author intent. Reproduction is not evidence of the intended mistake. They never enter default sampling; the entire five-member original bank is chosen only by explicit observed_/derived_ profile. Source choices and correct designation are compared separately, exactly and mathematically; missing designations have no fidelity denominator. The three source radio banks have15 values and the three captured blanks have3 values:18/18. Every captured complete bank matches6/6; captured correct refs match5/5.

The normal authored factored radio bank is lF, (a+b)F, lF², l, gF: correct content/shared-part combination, add contents, multiply duplicate common parts, omit the common part, use GCF. The normal hard radio bank is lF, gF, |ab|F, F, lF². Wrong values are full assessed-method operations derived after the correct answer. No random coefficient perturbations are used. A collision rejects the WHOLE sampled instance; explicit invalid instances raise. Source radio options have no invented diagnosis or feedback.

## 4. Reusable masks and constraints

Fixed: complete source opening, numerical LCM paragraph, the sentence retaining the same variable part, formal LCM(F,F)=F, final multiplication paragraph and formal LCM(P,Q)=l·F=lF. Variable: entire polynomial components, coefficients, variable letter, shift, exponent, numerical multiple values, complete bank expressions. Conditional: radio/blank layout, source whitespace/punctuation, source-specific list-index masks, captured omission of rating/solution/choice/correct keys. Source masks preserve all solution sentences and arithmetic stages byte-exact at original parameters. The authored difficulty completions assign q-76238 to easy (coprime3/5), and q-218482 to moderate (shared GCF3 in6/15, neither dividing), consistent with the five rated records. Raw omissions are exposed through the public `generate(...,profile='observed_q-...')`; derived profiles add only independently justified keys and authored rating/solution, retaining exact observed banks.

Normal bounds, also enforced on explicit inputs:

- Easy: distinct positive COPRIME contents2..9, LCM<=72, nonzero shift magnitude<=9, identical monic binomial exponent1 or2.
- Moderate: positive contents2..18, gcd>1, LCM<=120, same shifts/exponents. Linear instances require neither content to divide the other; squared instances permit the observed dividing-content workload. The observed/derived profiles enforce these same level bounds while preserving the original source values, and reject level/template mismatch, changed source exponent shape and erased moderate content workload. Source list masks additionally require the computed numerical LCM to appear in both displayed lists; otherwise the whole instance is rejected.
- Hard (authored): P=aF,Q=bF with F=A v²+h v+k; A2..4, 1<=|h|,|k|<=9, gcd(A,h,k)=1, exactly three nonzero terms. Integer contents have magnitude2..18, at least one negative sign, gcd>1, neither divides the other, numerical LCM<=120. The leading coefficient is nonmonic after reduction, so a hidden GCF cannot erase the advertised workload. The solution displays actual expanded P,Q, content extraction with grouped negative scalar products, numerical LCM multiple lists, formal common-part LCM, and final signed-input LCM. It never factors F further.

Normal question text makes the positive integer-content normalization explicit. Source profiles retain exact prompts. Identical mathematical parameters/layout/bank keep identity when seed/choice order changes; actual displayed prompt, fixed solution and whole bank determine content identity. Mathematical fingerprints normalize variable aliases and input order and exclude profiles/answer banks. All missing-source labels, solutions and keys have their own counts. Normal easy and moderate are disjoint by the coprime/shared-content condition, including explicit source-profile parameters. Validation rejects3/9 squared and its swapped/variable-alias shared-content variants at easy; the moderate boundary control verifies native expanded and unreduced equivalent answers and rejects incorrect content. No plots: extraction and generation stages5/7 are inapplicable.
