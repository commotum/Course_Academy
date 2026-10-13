# Four-stage extraction

## 1. Specific source descriptions

All sources ask for `(f∘u)′(t)` or `(g∘u)′(t)` as a complete vector. No field expects a single scalar component. Source-specific descriptions and exact original options are in `bank-extraction.json`; raw text is in `source.json` and side-by-side `review.md`.

| Source | Outer vector (component order retained) | Inner scalar | Layout | Derivative rows / substitution rows |
|---|---|---|---|---|
| q-32498 | (2u,u²,3) | 2t+2 | column | 2 / 4 |
| q-32866 | (cos u,1−u²,12) | t³ | basis | 4 / 4 |
| q-128563 | (sin u,ln(2u),tan u) | t² | angle | 3 / 4 |
| q-128572 | (u,u²,6) | exp t | column | 2 / 4 |
| q-32502 | (u,2u,3u) | t² | basis | 4 / 3 |
| q-32860 | (ln u,5,u²) | ln t | column | 2 / 4 |
| q-32869 | (ln u,0,1/u) | exp(2t) | angle | 3 / 5 |
| q-33260 | (exp(u+1),exp(2u),1/e) | 2t² | basis | 4 / 3 |
| q-71222 | (sin u,cos u,exp u) | 4t−3 | column | 2 / 4 |
| q-128561 | (ln u,u²,√u) | exp(−t) | basis | 3 / 5 |
| q-128570 | (1/u,ln(u+1),1) | 1/t | angle | 3 / 4 |
| q-70695 | (cos u,u³,ln u) | exp t | column | 2 / 5 |

Numbers are exact integers, including negative scalar exponent and negative affine shift. Column vectors explicitly retain constant-zero derivative components. Basis vectors omit zero components after the source's explicit removal rows. Angle vectors retain zeros. Exp/log/root simplifications and optional rows stay source-specific. Every source has a five-option bank with exactly one designated correct vector; 60 values and 48 distractors are accounted for.

## 2. General pattern

Differentiate the vector's three scalar components with respect to its scalar input, differentiate the scalar input with respect to t, substitute the same input into each component, and multiply the entire vector by the scalar derivative. The assessed operation is one vector composition. The fixed solution is independent of selected answer. Observed component mixtures and scalar inner families already span affine, monomial, exponential, logarithmic, and reciprocal functions at easy; therefore different family labels alone do not establish authored missing-level difficulty.

## 3. Component and complete-bank mapping

Let F denote the outer vector, D=F′(u), H the inner scalar, P=H′(t), and C=D(H)P. All formulas below are complete three-component vectors; a suppressed basis component is still the mathematical zero. `observed_bank` in the script is the parameterized implementation. `bank-extraction.json` pairs each original answer UUID/value with a full reproduced vector and operation label. A single source often cannot uniquely identify intent; the label states operations/patterns, not a claim that the original author used that error algorithm.

- **q-32498:** C; D(H) (omit scalar factor); `(ca,2a²t,0)` (drop inner shift); D(t) (replace inner input by t and omit scalar factor); `(ca,2H,0)` (apply scalar factor only to first component). These generalize directly to affine coefficients/shift and outer linear coefficient.
- **q-32866:** `(-sin P,−2P,0)` (replace inner input by its derivative and omit scalar factor); C; `(-(n−1)at^(n−1)sin H,−(n−1)a²t^(2n−1),0)` (wrong power-rule coefficients separately in each component); D(u) (omit substitution and scalar factor); `(-sin H,−2nH,0)` (omit scalar factor in trig component, apply only constant n in polynomial component). The third bank member's unequal coefficients are a residual observed symbolic pattern; exponent-decrement interpretation is plausible but not recovered intent.
- **q-128563:** `(cos H,1/H,(P/n)sec²H)` (omit factors from first two components and lose n from third); `(cos H,1/t,P)` (omit first factor, replace logarithmic coefficient n by 1, omit tangent outer derivative); `(P sin H,1/t,P cos²H)` (wrong trig derivatives plus lost log coefficient); `(P sec H,1/t,P sin H)` (wrong trig derivative functions plus lost log coefficient); C. These preserve component-dependent and compound mistakes, rather than treating the entire vector as one scale error.
- **q-128572:** D(H); C; `(cP,2H,0)` (factor only in first component); `(ct,2H,0)` (use t instead of exponential inner derivative in first, omit factor in second); `(c,3H,0)` (omit factor and use 3 instead of 2 for quadratic derivative). The last coefficient is retained as an observed exponent-plus-one pattern, not a diagnosed learner intention.
- **q-32502:** C; `(2P,2P,2P)` (erase unequal component coefficients); 2C (apply an additional constant factor 2); F(H) (omit differentiation entirely); D (omit scalar derivative). Unequal outer coefficients are required for the complete bank; collisions reject the entire parameter instance.
- **q-32860:** D(H); D; `(1/H,0,C₃)` (omit factor only from first component); C; `(u,c,2u)` (leave the log component undifferentiated as u and constant component unchanged while differentiating only the quadratic component). The last is a full explicit symbolic pattern with incomplete error interpretation; it is retained for replay.
- **q-32869:** `(a,0,−aH)` (wrong reciprocal exponent after otherwise correct log component); D(H) (omit factor); C; `(a,0,aH)` (same wrong exponent and wrong sign); `(1/H,0,1/H²)` (omit scalar factor plus wrong reciprocal derivative sign). The positive-exponent mistakes are applied only to the reciprocal component, not the whole bank.
- **q-33260:** `(t exp(at+b),ct exp(cat),0)` (linearize scalar input and use t for inner factor); `(t exp(t+b),ct exp(ct),0)` (also omit scalar-input coefficient); C; `(P exp(t+b),(c+1)at exp(ct),0)` (wrong input in both exponentials and wrong scale only in second); `(an exp(H+b),−anc exp(cH),0)` (lose t^(n−1) from inner derivative and reverse second sign). The fourth unequal-scale pattern is explicit and replayable; coefficient-plus-one intent is unresolved.
- **q-71222:** `(a sin H,−a cos H,a exp H)` (retain original trig functions instead of their derivatives); `(-sin H,cos H,H exp t)` (wrong trig functions/signs, omit factor, use inner input as exponential coefficient and fail to substitute exponent); C; `(-2a sin H,2a cos H,H exp t)` (same compound pattern, plus double scalar coefficient in trig components); D(H) (omit factor). The exponential pattern is preserved as a component operation, not forced into a scalar normalization.
- **q-128561:** `(-a,4aH²,2aH^(3/2))` (wrong log sign, double polynomial coefficient, root derivative exponent/sign/coefficient errors); `(a,aH²,2a√H)` (halve polynomial derivative coefficient and multiply root rather than reciprocate it); `(-a,2aH,a√H/4)` (wrong log sign, lose one exponent in polynomial, halve root coefficient); C; `(a,2a/H²,a/(2H))` (reciprocal substitutions in polynomial/root components). These are full compound symbolic patterns; their isolated original coefficients underdetermine exact intent, and the replay profiles explicitly retain that limit.
- **q-128570:** `(-1/a,−at/(2b+t²),0)` (wrong first sign; square t substitution and doubled log shift in second); `(-a/t²,−t²/(b+t²),0)` (first becomes inner derivative alone; square t substitution/incorrect factor in second); C; `(a/t,C₂,0)` (first equals scalar input instead of derivative); `(1/a,−at/(b+t²),0)` (correct first, square-t substitution/wrong factor second). The denominator transformations are explicit component operations. The whole bank is not one scale pattern; original b=a=1 does not identify all underlying learner mistakes.
- **q-70695:** `(-P cos H,3H,1)` (wrong trig derivative and quadratic-power/inner-factor omissions); `(-sin(H²),3H²,1)` (square the trig input and omit factor from polynomial); `(P cos H,C₂,H²)` (wrong trig derivative/sign, log reciprocal changed to direct power); `(sin(H²),H³,1/H²)` (wrong trig sign/input, erase cubic derivative coefficient, use squared reciprocal with no factor); C. Several component exponents admit more than one error history; the exact patterns are preserved and not presented as recovered source code.

**Default generation:** all normal source-workload instances use a separately labeled authored complete bank: C, D(H), D(u), D(H)P², and `(C₁,D₂(H),D₃(H))`. These operations are omission of scalar derivative, omission of substitution, applying the inner derivative twice, and applying it only to the first component. Constant D needs a separate complete bank because D(u)=D(H): C, D, F(H), 2C, and `(D₁P,D₁P,D₁P)`. There is no first-valid distractor pool. Complete bank selection precedes solving; C is computed first, all four wrong vectors follow, and any complete-vector equivalence rejects the entire instance. Explicit invalid/colliding parameters raise an error. Observed banks remain opt-in replay profiles; there are no literal source payload branches.

## 4. Reusable templates, constraints, and repairs

The script rebuilds the three complete inline prompt formulas as slots. It replaces entire math display blocks in the source's fixed prose skeleton; no short scalar string or variable-name replacements across arbitrary prose occur. Exact shared prose and display/outer-align row counts are compared separately from mathematical equivalence and notation. Twelve distinct source row sequences are retained, including omission of substitution row for q-32502/q-33260, zero removal for q-32866/q-33260, distributed-ratio row for q-32869, and simplification row for q-128561/q-70695. Notation normalization is deliberate: Unicode application markers, scalar/braced commands and sec² versus tan²+1 are converted to standard SymPy TeX. Exact mathematical stages, not exact bytes, are compared. No answer fragment changes layout or component order.

Easy samplers retain each observed monomial exponent and component function structure, with inner coefficient |a|=1..4, affine shifts |b|≤4, positive reciprocal-log shift 1..4, outer constants/coefficients 1..12 (sampled 1..4). Positive a is enforced where the natural logarithm/radical domain needs it; signed exponential exponents and affine coefficients are allowed. Source values 12, −3, and −1 remain valid explicit inputs. Source bank collisions are rejected as whole instances; coefficients are not swapped to salvage a bank. Every profile is exercised at source parameters and non-source parameters.

Missing-level templates and fixed workload bounds are documented in classification.md and enforced in explicit calls as well as samplers. Hard constant cannot be zero, ensuring all five expanded polynomial terms are present. Function names are fixed source f/g names; unsupported renaming is not exposed.

Four source teaching errors require small corrections, preserved in raw `source.json` and identified in output metadata:

1. q-32866's prompt writes f(t) for a vector expressed in u; use f(u).
2. q-32502 differentiates outer 3u using d/dt; use d/du. The printed resulting component 3 was already mathematically correct.
3. q-32860's opening chain formula uses f although the function is g; use g.
4. q-33260's intermediate outer derivative writes 2exp(2t); use 2exp(2u). Subsequent substitution and final source answer were correct.

All 12 complete banks and 60 option values match. Source solution prose/row sequences: 12/12. Original mathematical sequences requiring no repair: 8/12; minimally repaired sequences: 4/12. Exact notation/solution-byte matches: 0/12 because TeX is normalized. These denominators are kept separate; no wrong source stage is silently counted as an exact pass. Every generated derivative and substitution/distributed stage is independently read from displayed math and checked against the derivative of the actual printed functions.
