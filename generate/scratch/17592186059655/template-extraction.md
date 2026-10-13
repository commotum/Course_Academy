# Template extraction — four stages

## 1. Describe originals specifically

q-1578 asks “What is” a sum of two squared conjugate binomials in sin x,cos x, unit coefficients, no domain exclusions. Both squares must expand before the mixed terms cancel. The correct scalar2 is missing as a designation. No source solution/difficulty is stored.

q-65162 asks “What is” cos²θ times `(1+sin²θ/cos²θ)`, with Greek Unicode angle, positive unit coefficients and direct cancellation after distribution; domain cosθ≠0. Correct scalar1 has no source designation, solution or difficulty.

q-119361 displays `cosθ(cosθ+1/cosθ)+sin²θ=`. Its solution first writes both distributed products, then explicit crossed-out cos factors, then cos²+1+sin², regrouping, 1+1,2 and the conclusion. Domain cosθ≠0. Its bank mixes constants and cos expressions; their error intent cannot be recovered from single observations.

q-43288 displays `cosθ sinθ(cosθ/sinθ+sinθ/cosθ)=`. Its five RHS stages preserve distributed products, fractional numerators, both crossed-out denominator factors, sum of squares,1. Both sinθ and cosθ must be nonzero.

q-43293 displays `(1/sinθ)(sin³θ+cos²θ sinθ)=`. Its five RHS stages preserve distribution, fractions, canceled factors, sum of squares,1; sinθ≠0.

q-65222 asks to simplify cos t(1−cos t)−sin²t. Its three RHS rows are cos−cos²−sin², cos−(cos²+sin²),cos−1. q-65225 displays sin t(sin t−1)+cos²t=; its rows are sin²−sin+cos²,(sin²+cos²)−sin,1−sin. Both use real t, unit signs and no denominators.

## 2. Generalize the shared pattern

Expand existing parentheses, simplify any direct multiplicative cancellations already present, group equal-coefficient sin²/cos² terms, then replace the sum by1. Preserve any surviving linear or cross term. The response is one whole simplified expression in a single radio field, never an equation fragment. There are seven observed prompt/stage templates, each with one complete bank. Raw angle slots apply to the whole trig component throughout prompt, every solution row, conclusion and bank.

## 3. Components and complete bank recipes

The table below maps every original choice in source order. s=sin(angle),c=cos(angle). Source banks are observed **expression patterns**, not inferred diagnoses. Raw profiles replace the complete angle slot and support a common scalar1–6 multiplying the entire prompt expression, each displayed equation side/stage and each bank member. Unit scalar leaves the exact source bytes unchanged. Thus they are genuinely parameterized source masks, but angle aliases are excluded from variety claims. Coefficient extensions below are explicitly authored.

| Source | Exact original bank in stored order | Correct designation | Source expression patterns |
|---|---|---|---|
| q-1578 | −1,1,2,0,−2 | absent; inferred2 | −1,1,2,0,−2 |
| q-65162 | −1,2,0,1,−2 | absent; inferred1 | −1,2,0,1,−2 |
| q-119361 | 2c,2,−2c,2+c,c−2 |2| 2c,2,−2c,2+c,c−2 |
| q-43288 |1,0,−2,−1,2|1|1,0,−2,−1,2|
| q-43293 |−1,2,0,−2,1|1|−1,2,0,−2,1|
| q-65222 |c−1,c+1,−c,−c−1,c|c−1| c−1,c+1,−c,−c−1,c |
| q-65225 |−1−s,s,−s,1−s,1+s|1−s| −1−s,s,−s,1−s,1+s |

For scalar k, every table entry and complete displayed solution object is multiplied by k through a complete-component mask; k=1 gives the original table. No unrelated fit or answer lookup is used. All35 options are exact value-string replayed (including Unicode invisible application characters and spaces) and independently mathematically checked. All five stored correct designations are matched. There is no designation-match denominator for the two omissions. Complete exact source strings are in source.json, and the public generate interface regenerates these masks rather than copying the complete source question payload.

Authored default complete banks (correct first before deterministic shuffle):

| Template | Parameters/expression | Bank operations |
|---|---|---|
| paired_squares |(as−ac)²+(as+ac)²|2a²,a²,−a²,0,−2a²: both squares, one square, sign reversal, omit squared terms, reverse both squares |
| cos_ratio |c²(a+as²/c²)|a,−a,2a,0,−2a: identity, sign reversal, identity sum treated2, zero, signed double |
| cos_reciprocal |c(c+a/c)+s²|named cos_reciprocal_nonunit (a2–6):a+1,a,1,0,−a−1; named cos_reciprocal_unit (a1):2,1,0,−1,−2| identity plus cancellation; omit identity/canceled term, zero, sign reversal; unit case uses signed identity constants |
| cross_ratio |acs(c/s+s/c)|a,0,−2a,−a,2a| identity, zero, signed double, sign reversal, identity sum treated2 |
| cubic |(a/s)(s³+c²s)|a,−a,2a,0,−2a| identity, reversed sum, double sum, zero, reversed double |
| linear_cos |c(a−bc)−bs²|ac−b,ac+b,−ac,−ac−b,ac| correct; identity sign reversal; dropped identity with reversed linear sign; both reversed; dropped identity |
| linear_sin |s(bs−a)+bc²|b−as,−b−as,as,−as,b+as| correct; identity sign reversal; dropped identity and linear sign reversal; dropped identity; linear sign reversal |
| cross_single |s(ac−bs)−bc²|asc−b,asc+b,−asc−b,asc,asc−bs²| correct; identity sign reversal; cross sign reversal; omitted identity terms; omitted cosine-square term |
| cross_double |s(ac−bs)+c(ds−bc)|(a+d)sc−b,(a+d)sc+b,(a−d)sc−b,(a+d)sc,(a+d)sc−bs²| correct; identity sign reversal; second cross-product sign reversal; omitted identity terms; omitted cosine-square term |

The scalar-only observed choices underdetermine misconception intent. Normal constant banks are conservative authored omission/sign/identity operations; their finite shape is not represented as recovered source error code. No diagnosis appears in learner content. Every bank is selected whole and rejected whole on duplicate/correct-equivalent wrong options. No unrelated numerical perturbation or first-valid distractor pooling occurs.

## 4. Reusable masks, constraints and fidelity

Fixed prose in observed masks is retained byte-for-byte at original angle. Variable components are a common scalar1–6 applied to complete mathematical objects and complete trig angle tokens (x,t,θ,\\theta), substituted in prompt, solution and choices. Optional attributes depend on **original presence**, not inferred values: raw missing difficulty, correct ref and solution remain absent. Normal source completions use supported independently derived values2/1 and authored solutions/levels, explicitly labeled. The captured MA207 widget evidence confirms field layout and full banks, not missing correct refs. The raw decoded byte audit reports backslash runs; all single slashes are commands and double slashes are legitimate aligned row separators. No invented serialization-based TeX anomaly is claimed.

Normal coefficients use separately authored exact masks retaining the same expression families and source canonical instructional sentences. Their solution structure is expansion → group → identity → conclusion. Easy a,b1–6; unused d1. Moderate |a|2–8,b1–6,d1. Hard same-sign |a|,|d|2–6,b1–6. Signed terms are formatted with visible signs; two numeric factors are never concatenated. Domain exclusions derive from actual displayed denominator factors and remain author metadata. Angle aliases do not increase task counts; hard a,d decompositions with equal a+d do not increase counts. SHA256 identity includes generator version, displayed prompt, solution and sorted complete bank/correct designation. Seed/order alone cannot change identity. The mathematical fingerprint excludes bank/profile/unused components.

Plot extraction/specification: none. There are no source assets or parameter-dependent diagrams to recreate. Steps5 and7 are satisfied without a renderer; work stops before database preparation.

All observed raw/completed profiles are explicitly evidence-only and ineligible for learning. Raw missing difficulty previews are labeled Unrated; supported completions are labeled Inferred Easy. Authored defaults remain eligible. The cos-reciprocal generator chooses its named complete unit/nonunit bank before sampling the constrained coefficient domain, records its eligibility/recipes, and rejects an explicit mismatched bank/domain instead of switching profiles. Unit and nonunit banks are alternative whole eligible banks, not a first-valid recipe fallback.
