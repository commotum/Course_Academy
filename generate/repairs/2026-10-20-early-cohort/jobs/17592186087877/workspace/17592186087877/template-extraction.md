# Four extraction stages

## 1. Describe each source specifically

q17540: y′+y=cos x, no domain, no solution/key/rating, five complete equations. Factors x, ln x, x², 1/x, e^x; x² choice prints d/dx², an erroneous denominator. q8546: y′+2xy=2xe^(-x²); factors e^x,2x,x²,e^(x²),x; no solution/key/rating. q17533: xy′+xy=x², standardization y′+y=x, e^x factor; factors 2x,e^x,2,e^(2x),x. q335278: y′−(1/2)y=x³, factor e^(-x/2); factors e^(-x/2),e^(x/2),−x/2,−1/2,2. Its first distributed solution row wrongly has +1/2 instead of −1/2.

q17539: x²y′+xy=x²cos x, x>0; normalization gives P=1/x,Q=cos x; integrating-factor rows definition → reciprocal integrand → e^(ln x) → x. Factors e^x,x²,x,e^(-x),ln x. Its second multiplied row and final derivative collect x cos x. q79818: y′+(1/x)y=e^x,x>0; same four factor rows; factors x²,e^x,e^(-x),x,ln x; collect x e^x. q79819: xy′+2y=1, no domain stated; normalize P=2/x,Q=1/x; five integrating-factor rows definition → reciprocal integrand → e^(2 ln x) → e^(ln x²) → x². Factors ln x,x²,e^x,x,2. Retain the final product x²·(1/x), with no extra collection row.

All prompts request one complete equation in product-derivative form. No request asks for y(x). Five captured solutions share fixed instructional sentences and an ordered sequence: optional standardization; generic standard form; identify P/Q in prose; define and compute factor; multiply then distribute; identify product derivative. See unmodified `source.json` and originals in `review.md`.

## 2. Generalize the mathematical purpose

For a displayed A(x)y′+B(x)y=R(x), first obtain P=B/A and Q=R/A, compute I=exp(∫P dx), and choose d(y I)/dx=I Q. Constant, reciprocal and monomial P are the only families. Every displayed choice is a complete equation, compared after expanding its product derivative and allowing any nonzero scalar multiplier. Q is never integrated.

## 3. Component/choice mapping

`bank-mapping.json` enumerates every raw answer ID/value, complete field ownership, original correct designation (or explicit null), and the parameterized multiplier recipe. The full five-choice banks are selected together. For each factor F, the recipe is `(yF)′=FQ`, except the malformed q17540 denominator. The source replay uses the same normal generator with original explicit parameters and profile `observed_raw`; it contains no literal source-answer lookup or source-ID return branch.

Parameterized factors, in the original captured order:

| Source | Complete factor bank |
|---|---|
| q17540 | x, ln x, x² with denominator dx², 1/x, exp(a x) |
| q8546 | exp(a x), 2a x, x², exp(a x²), x |
| q17533 | 2a x, exp(a x), 2a, exp(2a x), a x |
| q335278 | exp(a x), exp(−a x), a x, a, −1/a |
| q17539 | exp(k x), x^(2k), x^k, exp(−k x), ln x |
| q79818 | x^(2k), exp(k x), exp(−k x), x^k, ln x |
| q79819 | ln x, x^k, exp(kx/2), x^(k/2), k |

These formulas preserve source components, but single observations do not identify original author intent. In particular constant factors and scale-equivalent wrong factors offer no defensible distinct misconception. They are replay evidence, never the default bank. Distinct parameter changes are exercised in review for each complete source bank. One-to-one source matching preserves duplicate observed values without calling the original bank unambiguous.

The independently derived missing correct keys are exp(x) for q17540 (I′=I), and exp(x²) for q8546 (I′=2xI). Their other factor choices do not satisfy I′=PI; the captured lesson radio widgets agree with the five choices but provide no designation. Count 35/35 displayed source shapes: 34 unambiguous complete mathematical values, plus one malformed denominator matched only under the explicitly documented chain-rule convention. Count 5/5 existing designations, plus 2 separately derived designations.

## 4. Extract reusable masks, domains and calculations

The script replaces only the complete supplied ODE math span and complete worked-solution math spans. Inline P,Q,I fragments are complete component slots. All source prose outside math is retained. Source TeX is normalized to conventional `dy/dx`, `ln`, grouped signed terms, and unambiguous multiplication. This changes typography but not stage order. Reciprocal factor rows preserve logarithm/exponentiation stages; k=±1 omit the redundant logarithm-power row, otherwise include it. Sources q17539/q79818 collect the RHS at their original stage; other templates do not. The negative source distribution sign is repaired before presentation.

All exact arithmetic uses SymPy. No numerical perturbations or answer offsets appear. Explicit input keys and difficulty bounds are validated identically to sampled inputs. Easy nonzero rational a has |a|≤4 and denominator≤3, n=1..4 or nonzero |b|≤4. Moderate reciprocal nonzero |k|≤4, familiar cos(bx)/exp(bx) b=1..4 sampled; the normalized forcing c/x has nonzero |c|≤4. Moderate monomial source P=2ax has nonzero |a|≤3, nonzero |b|,|c|≤4. Hard bounds are in classification.

Normal banks are authored complete profiles, based on wrong exponent sign/scale/power and wrong logarithmic vs exponential factor:
- Constant: I,1/I,exp(2ax),x,x².
- Reciprocal: x^k,x^(k+1),exp(kx),exp(−kx),ln x.
- Monomial: I,1/I,exp(P),exp(a x^(d−1)),x^d.

Before output, each full bank must contain exactly one correct equation and no equivalent pair; a failure rejects the whole instance. Changing seed only changes order when parameters are fixed. The mathematical fingerprint hashes normalized P,Q and the actual domain, excluding incidental supplied common scale and bank profile; content identity hashes actual prompt, fixed solution, complete sorted displayed bank and version/domain. Field-owned answer IDs remain stable under order changes.

# Anomaly accounting and minimal repairs

The unmodified capture is never overwritten. Separate `anomalies.json` records raw evidence and supported changes.

- q17540/q8546: missing keys, solutions and levels. Derive keys independently, author solutions matching the canonical stage pattern, assign contextual easy/moderate levels. No designation-fidelity credit.
- q17533: 2x and x factors give identical wrong complete equations; q8546: 2x and x likewise; q335278: −1/2 and 2 constant factors likewise. Preserve raw banks as explicitly labeled evidence, then replace entire default bank with a separately labeled complete authored profile.
- q17540: dx² differential denominator is malformed. Retain it in raw replay and original evidence; normal authored choices use d/dx throughout.
- q335278: wrong +1/2 coefficient in distributed row; normal/replay solutions use the mathematically required −1/2. Original remains visible alongside repair. Captured prose and row sequence survive.
- All raw answer strings contain doubled command backslashes; several include literal backslash-u2061, while solutions contain the invisible U+2061 character. These are presentation normalizations, not algebraic repairs.
- Division by x in q17533/q79819 requires a domain restriction absent in the source. A positive half-line assumption makes the standardization valid. The raw ln x/1/x options in q17540 likewise require a positive-domain interpretation. Do not claim raw-exact prompt reproduction.

Fidelity denominators are separate: complete displayed source banks 7/7 (including documented raw ambiguities and the malformed denominator convention), existing correct designations 5/5, missing keys derived 2; fixed prose and ordered captured sequences 5/5, uncorrected mathematical solutions 4/5, minimal sign repair 1/5. Raw-exact typography is not claimed.


## Current-source q-335274 extraction, basis 2009

Specific source: y′+2xy=sin x, with factor exp(x²), five complete transformed equations, one radio selection field, and four worked blocks. The factor bank is ln|2x|, x², exp(2x), 2x, exp(x²). Only exp(x²) solves I′=2xI. The standard-form display, P/Q identification, three integrating-factor rows, two multiplication/distribution rows, and final product derivative all match the existing transformation scope. RHS collection occurs at the distributed and final rows.

General template: y′+2ax y=sin(bx), nonzero integer |a|≤3, integer b=1..4 in normal sampling (explicit nonzero |b|≤4). Compute P=2ax, Q=sin(bx), H=ax² and I=exp(H). The entire observed bank is selected together: F=ln|2ax|, x², exp(2ax), 2ax, exp(ax²); each option is (yF)′=F sin(bx). On the declared x>0 half-line, ln|2ax| is rendered ln(2|a|x), with no new absolute-value branch. All five complete equations and the captured designation are replayed one-to-one. This added half-line restriction makes the logarithmic distractor real; originals remain unchanged. Wrong-option interpretations are observed expression patterns, with no asserted author intent.

The new source retains fixed prose and block/row order. Conventional TeX normalizes `operatorname{sin}` and the invisible function-application character. Parameter changes are checked under positive/negative a, original/changed b, complete bank distinctness, independently parsed printed equality stages, deterministic identity, and native radio selection. No plots are required. The immutable historical source.json remains unchanged; source-current.json records the added bank.
