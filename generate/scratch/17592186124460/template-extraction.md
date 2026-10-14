# Template extraction

## Stage 1 — observed instances

The source-specific functions, inputs, number forms, field types and gaps are listed in classification. Exact full records remain in source.json; raw public profiles reproduce all present learner content and preserve every omission. Moderate q130801 uses a radical nonunit direction and evaluates two differences of reciprocal terms to zero. q83608 explicitly reduces (-2,2) to (-1,1), evaluates cos π=-1 and sin π=0 separately, and then dots (0,π). q83613 evaluates tan(π/4)=1 and sec²(π/4)=2 as separate multiplicative pieces, obtains (2−π,π−2), dots with (-1,1)/√2, combines (2π−4)/√2 and factors √2(π−2). Hard q36300 evaluates e⁰=1 inside both negative partials, then computes separate squared components (-9)²+(-1)². q37083 uses product rule, substitutes ln1=0, then squares (-1,-1).

## Stage 2 — generalized patterns

Each question asks for the scalar directional derivative, either ∇f(P)·v/||v|| for a supplied nonzero vector, or ±||∇f(P)|| for greatest increase/decrease. Formal partials, general components, substituted components, evaluated gradient, and the norm or dot-product chain are retained per family. Normal greatest-decrease questions require the negative signed rate.

## Stage 3 — all original components and banks

The five-value profiles below are in captured choice order; `source-cases.json` maps every source to its template/parameters/profile. Use `raw-<source-id>` through `generate(...)` for original fidelity. Let H,K be displayed coordinates, A,B evaluated gradient components, v=(r,s), N=||v|| and D=(Ar+Bs)/N. Historical scalar wrong-operation intentions are underdetermined. Their displayed expression recipes are parameterized evidence, not claims about original author intent and never normal default banks.

| Source/profile | Full original bank | Parameterized scalar recipe in same order | Original correct designation |
|---|---|---|---|
| q36297 | -√10/10; 1; 17; -8√10/5; 2√5/5 | r/N; K; A²+K²; D; H/√(H²+K²) | absent; D independently inferred |
| q37074 | √(π+e)/e; √((π+e)/e); √(π²+e²)/e; √(π⁴+e²)/π; √(π²+e²)/π | √(K+H)/H; √((K+H)/H); √(K²+H²)/H; √(K⁴+H²)/K; √(K²+H²)/K | absent; third independently inferred; historical profile requires c=n=1 |
| q130801 | √2; √3; 2; 3; 0 | |s|; N; s²; N²; D | 0 |
| q36300 | √10; √8; √80; 9; √82 | √(A+B); √(A−B); √(A²−B²); A; √(A²+B²) | positive norm; incorrect signed rate |
| q37083 | 2√2; √3; 1; √2; 2 | 2||gradient||; √(A+B+1); |A|; ||gradient||; A+B | positive norm; incorrect signed rate |
| q83608 | π√2; π/√2; -2π; -π/√2; π/2 | 2D; D; -2B; -D; B/2 | π/√2 |
| q83613 | √2(π−2); 2(π−2); π−√2; 2(π+2); √2(π+2) | D; Ar+Bs; a|2H|−a/√2; 2a(|2H|+1); √2a(|2H|+1) | first; historical profile H=K=π/4, v=(-s,s), s>0 |

Every recipe is checked against the actual rendered option math and against full source bank values, with key presence and designation counted separately. Historical profiles are exposed under changed parameters as public evidence witnesses. Where historical data omit a key, raw replay does not invent one. `completed-<id>` is a separately labeled ineligible historical profile with authored solution/key; hard completion replaces its positive correct value by the signed negative value. Normal sampling uses the following complete family-specific operation banks instead.

| Family | Authored complete five-option bank |
|---|---|
| quotient | D; reverse x-partial sign; reverse y-partial sign; omit vector normalization; omit the numerator square in quotient y-partial (-cH/K²) |
| ratio_sum | D; change minus to plus in x partial; same error in y partial; both errors; return vector norm |
| sine_quotient | D; omit normalization; reverse direction; omit differentiated sine contribution in x partial; divide the dot numerator by ||v||² instead of ||v|| |
| tangent | D; omit normalization; reverse direction; omit both sec² chain terms; omit both direct tan terms |
| exp_bilinear | negative norm; positive norm; omit inner exponential x-factor b; omit both bilinear contributions; keep only x-component magnitude with negative sign |
| sumlog | negative norm; positive norm; omit both direct product-rule terms (yielding zero at ln1=0); keep only x-component magnitude; add absolute component magnitudes instead of taking Euclidean norm |
| sinlog | norm; omit 1/H from x chain; replace ln H in y component by H; add component magnitudes; keep only x-component magnitude |

All banks are chosen whole before coordinates, and any collision/ambiguous/nonreal value rejects the whole instance. No first-valid pooling or unrelated random perturbation. Wrong-operation descriptions remain author metadata; learner choices contain only the source-style scalar answers.

## Stage 4 — masks, bounds and operations

The script slots complete function formulas, points, vector literals and complete solution rows; it never globally replaces a short numerical substring. Formal partial operands are slotted with the full displayed function. Shared source prose is retained for each observed family. q130801 preserves the reciprocal subtraction row; q83608 preserves the separate trig evaluation row; q83613 preserves tan/sec² substitution and term evaluation, the two-factor dot numerator, collection and final factoring; the hard families preserve negative partials and individual norm squares before final collection. The two absent source solutions are authored with complete formal/general/substitution/evaluation stages. Additional negative-rate conclusion is a mathematical correction, separately labeled.

Easy: c=1..4 and H,K=1..5; supplied vector components are nonzero signed integers ±1..3 in sampling. Moderate ratio coordinates are nonzero integers ±1..5; sine coefficients a,b=1..4, H,K=1..5; tangent a=1..6 with equal nonzero arguments ±π/4. Supplied direction components sample ±1..3 and explicit bounds allow signed integers or integer multiples of √2 with absolute magnitude up to 6 (supporting common-scale invariance tests). Hard exponential a=2..6,b=2..5,H=1..4,K=bH keeps e⁰ evaluation, with evaluated x/y gradient components bounded by 30/12 to avoid larger square arithmetic; log product uses a,b=1..8,H=1..4,K=(1−aH)/b to keep log argument 1; sine/log c,n,j=1..4, H=eⁿ,K=jπ/n keeps cos(jπ) familiar. The exponential domain has 39 valid parameter triples; the weighted log-product family has 64 meaningful coefficient pairs (changing its point along the same level line does not inflate task counts). These are equal-method bounded practice choices, not recovered sampling code. Guards apply equally to explicit inputs.

Content identity hashes actual rendered prompt, fixed solution, difficulty-presence/value, complete bank sorted independently of option order, and correct-key presence; seed/order changes cannot change it. The mathematical fingerprint uses the complete function, point, response criterion and normalized direction; it excludes profile/bank, positive common vector scaling, and displacement along a log-product level line (only its evaluated linear argument affects this assessment). Numerical coefficient variety is substantive because it changes gradient components and rate. No plots exist in these questions.
