# Four-stage extraction

## 1. Specific originals

The classification table identifies all twelve individual originals and distinguishes every prompt/notation/solution family. `source.json` retains every exact string, complete field, complete choice bank and available correct designation. `source-choice-map.json` records a one-to-one mathematical match of every original option to its parameterized recipe value; a missing original designation is never counted as matched. `review.md` shows the complete original prompts, banks and solutions alongside changed examples.

All functions have two additive terms. The differentiation variable is explicit in either a partial fraction or a subscript, while the other variable is held constant. Source coefficients are positive integers; subtraction is a stable operation sign in reciprocal, tangent/base-exponential, constant/sine, arctangent and arcsine families. Target and held powers are small nonnegative or reciprocal powers. Elementary primitives are sine, cosine, tangent, logarithm, natural or fixed-base exponential and inverse sine/tangent. No term requires a product rule in the target variable. Domains follow the function: positive log argument, inverse-sine interior, nonzero denominators and tangent poles excluded.

Every available original solution uses the same shared differentiation sentence and its original rule sentence. Moderate originals first explain subscript notation. The reciprocal original names the constant multiple rule, exp_sum names the sum rule, and the remaining originals name sum and constant multiple rules. The complete shared prose is compared against each original. q-132241 has no observed solution prose.

## 2. General pattern

Given `f(x,y)`, compute the specified first partial while treating the other variable as constant. Preserve the original one-field five-expression selection contract. The fixed five stages are: derivative of the full function; termwise splitting (with exponential factorization where observed); held-factor extraction; elementary derivatives inserted as ordered unevaluated products; collected final partial. Each generated instance has one concrete solution independent of the learner's selection.

## 3. Component and bank maps

In the implementation, `u` is the requested variable and `v` is the held variable. `exprs` returns ordered pairs `(held factor, target factor)` and the complete five-expression bank. Its twelve branches are the explicit parameterized operation recipes; no source payload branch, anchor lookup or option-subset pool exists. All original options, including compounds with unclear intent, are preserved as algebraic operation patterns. Those patterns are not presented as learner diagnoses. For example the source power_ratio bank retains both `nm*u^(n-1)/v^m+b` and `-nm*u^(n-1)/v^(m+1)+b`; these are evidence patterns, not claims about a learner's reasoning. The source atan product option retains multiplication of its two component derivative magnitudes. The q-35709 cross-variable option keeps the specified wrong-target power operation. Source anchors and bank membership are explicit in `source-cases.json`; complete original and regenerated values are in `source-choice-map.json`.

| Family | Ordered held × target components | Anchor parameters |
|---|---|---|
| cos_poly | `a*v × u^n`; `b*v^m × cos(u)` | a=b=1,n=m=2,target=y |
| sin_poly | `a*sin(v) × u^n`; `b*v × u` | a=b=1,n=2,target=x |
| log | `a*v × u`; `b*v^n × log(u)` | a=b=1,n=2,target=y |
| reciprocal | `a/v × u`; `-b*v × u^-n` | a=b=1,n=2,target=x |
| asin | `a*v × asin(u)`; `-b*v² × 1` | a=1,b=8,target=x |
| exp_sum | `exp(a*v) × exp(b*u)`; `v^m × u^n` | a=2,b=3,m=2,n=3,target=y |
| tan_power | `a*v^n × tan(u)`; `-b*B^v × B^u` | a=b=1,n=B=3,target=y |
| constant_sin | `a × v`; `-b × sin(u)` | a=5,b=2,target=x |
| power_ratio | `a/v^m × u^n`; `b*v × u` | a=1,b=6,n=3,m=4,target=x |
| inverse_power | `a*v^m × u`; `b*v^k × u^-n` | a=8,b=3,m=n=4,k=2,target=x |
| cross_exp | `a*v × exp(u)`; `b*exp(v) × u` | a=b=1,target=y |
| atan | `a × atan(u)`; `-b*v × u^n` | a=3,b=1,n=2,target=y |

## 4. Reusable slots and limits

All coefficient slots are integers 1–9; powers and bases are integers2–4. Both target roles x/y are eligible in every family, with every function, operator, solution reference and answer changed together. This role variation is tested with all other mathematical data held fixed. Positive coefficient bounds retain observed operation signs and arithmetic demand. Family term count and primitive types remain fixed. Complete source banks are selected by family before sampling; a whole instance is rejected if any pair of choices is equivalent, even two wrong choices. exp_sum has distinct affine slopes because equal slopes can collapse its observed bank. Explicit inputs enforce the identical domain and difficulty guards.

Hard has exactly three terms: `a*v^m log(u)+b*v exp(u)-c*v²/u^n`, or `a*v^m sin(u)+b*v atan(u)-c*v²/u^n`. Their complete method-derived banks retain a reciprocal sign error, one undifferentiated target primitive, one dropped held factor, and the partial with respect to the held variable. All three coefficients are nonzero. This is authored additive bookkeeping in the same introductory KP, not a recovered hard label. The canonical uses a log/exponential sum; source q-159612 supplies inverse-tangent/power handling and q-159616 supplies reciprocal-power handling. Topic prerequisites explicitly include exponential, logarithmic, trigonometric and inverse-trigonometric differentiation. The next topic teaches broader rules; sibling KPs teach limits and point evaluation. Those methods are excluded here.

`row_data` preserves the observed exponential split and fixed component order; it does not simplify operative products before the collection stage. Shared normalization precedes UUID creation. Content identity owns field and answer UUIDs and includes difficulty, prompt, fixed solution, complete bank and parameter data. Seed and option order do not affect identity. The mathematical fingerprint uses the canonical derivative in target/held role symbols and component count; variable-letter aliases and coefficients of wholly held additive terms do not inflate meaningful task counts.

No source feedback is invented. SymPy TeX normalizes glyph/function spelling, fraction grouping, term collection order and redundant product parentheses; mathematical stage equivalence and complete shared prose are validated separately. There are no graphic assets.
