# Template extraction

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unchanged wrapper/record is in `source.json`; canonical example is e-2480 and is not counted as practice.

The four stages below map every original bank before extension. The script is the executable recipe specification; formulas in the tables are symbolic parameter expressions, never lookup tables. Scalar mathematical equivalence and entire-vector equivalence are used. Choice order and equivalent TeX spelling are immaterial; every choice still matches exactly once.

## Source repairs and provenance

1. **q-32353 duplicate legacy field.** Basis 1356 contains a bmatrix five-option field with no `:answer-field/correct`, followed by an aligned-vector field with the correct designation; both have key `selection`. `/home/jake/Developer/MA/DATA/Lessons/1738/Source/1738.json`, lesson_index 14, question_id 32353, is one multiple-choice widget with `choice_count: 5`. `/home/jake/Developer/MA/DATA/Lessons/1738/1738.md` likewise has one choice list. Its two captured banks contain the same five entire vectors modulo notation/order. Supported repair: normal questions use the designated active field only. `cross_matrix_legacy` reproduces the old bmatrix bank as evidence, with the mathematically inferred correct ref. All 10 captured answer values are compared. The absent legacy designation is explicitly unmatchable, never counted passed.

2. **q-33446 intermediate typo.** The source second subtraction vector prints `2^(t+1)·2 ln 2 / 2^t` in its middle component although `v′=-ln 2/2^t`; hence this should be `2^(t+1) ln 2 / 2^t`. The preceding derivative and final zero component support the correction. Generated solutions calculate both product terms from the actual derivatives and remove the extra factor. The original worked solution remains in `source.json` and `review.md`.

3. **q-32347 wrong option `-362t²+12t`.** This is a valid but conspicuous incorrect option. There is insufficient evidence that the intended display was another number. It is preserved, with coefficient recipe `-(20 a e+b)`, i.e. appending the source second-coordinate coefficient to `2ae`. Its pedagogical interpretation is unresolved; its mathematical value and wrongness are resolved. No correct mathematics depends on this interpretation.

## Default bank policy

Every default learner question uses a complete authored bank derived from the product-rule calculation. Observed profiles are explicit replay banks: their uncertain wrong-operation interpretations limit their use as generalized learner distractors. All observed values and banks remain intact and testable. Scalar authored banks omit either product term, subtract the second term, or count the first term twice. Dot banks omit terms, reverse signs, or multiply derivatives; the symmetric logarithmic bank uses a sign-reversed omitted-term expression to avoid duplicate half-results. The evaluated self-dot bank uses the first-derivative square alone, a reversed second-derivative term, a repeated second-derivative term, or second derivatives missing their factor two. Cross banks omit either term, reverse the cross order, or use the wrong middle cofactor sign; self-cross substitutes the zero self-cross, reverses order/sign, or differentiates both inputs, avoiding the correct-answer omission collision.

## Parameter policies

Observed defaults are explicitly accepted. Sampling uses nonzero small integer coefficients/shift magnitudes 1–6, retaining negative signs where observed. Source coefficients 8 and 20 remain valid for explicit replay. Easy powers stay 1–4, with three distinct ascending powers in `scalar_power`; the scalar exponent is 1–3. `scalar_log` uses powers 1–3 with unequal last two powers so the complete bank remains distinct. Exponential rates remain 1–2 and 1–3; bases are integers 2–5 and their exponent shifts have magnitude 1–2, keeping the elementary cancellation bank readable. Hard monomial exponents are n=3 or 4, p=2, q=2 or 3. The evaluation template samples -1, 0, 1. These are authored parameter extensions, not new observed source templates. Each complete bank is selected first and the whole instance is rejected for equivalent options, ambiguity, or invalid mathematics. Explicit invalid inputs fail instead of being changed.

## Rendering contract

Prompt clauses, vector dimension and notation family, response type/count, shared solution sentences, rule order, derivative stage, componentwise product stage, and final answer are retained. TeX is normalized by SymPy, including expansion of an external tuple factor, ordering polynomial terms, and equivalent exponential/fraction simplification. Derivative calculation rows use direct componentwise differentiation; cross solutions retain both 3×3 determinants and their signed 2×2 minor expansions. Normal generated q-32353 instances apply the supported one-widget repair. The scalar-base worked row applies the supported typo repair. These are rendering/correction distinctions, not claims of literal character-for-character reproduction.

## scalar_log — easy, q-128586

### 1. Specific observed instance

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\operatorname{ln}⁡t,\,{t}^{2},\,t⟩$ and $v(t)=2t.$

Parameters: `{"c": 2, "m": 1, "n": 2}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: t>0.

### 2. Generalized mathematical pattern

Differentiate a scalar function times a three-component vector: u f′ + u′ f. The fixed component structures assess the same observed derivative/cancellation workload.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[c*(log(t) + 1)], [c*t**n*(n + 1)], [c*t**m*(m + 1)]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `2⟨\operatorname{ln}⁡t,\,3{t}^{2},\,\sqrt{t}⟩` | `omit_log_constant_and_halve_last_exponent` | `Matrix([[c*log(t)], [c*t**n*(n + 1)], [c*t**(m/2)]])` |
| 0 | `2⟨\operatorname{ln}⁡t+1,\,3{t}^{2},\,2t⟩` | `correct` | `Matrix([[c*(log(t) + 1)], [c*t**n*(n + 1)], [c*t**m*(m + 1)]])` |
| 0 | `⟨\operatorname{ln}⁡t+1,\,t,\,3t⟩` | `omit_scalar_and_use_last_power_in_both_slots` | `Matrix([[log(t) + 1], [t**m], [t**m*(n + 1)]])` |
| 0 | `2⟨\operatorname{ln}⁡t+1,\,3t,\,{t}^{2}⟩` | `exchange_last_two_power_structures` | `Matrix([[c*(log(t) + 1)], [c*t**m*(n + 1)], [c*t**n]])` |
| 0 | `⟨\operatorname{ln}⁡t,\,3{t}^{2},\,{t}^{2}⟩` | `omit_scalar_and_log_constant_use_second_power_last` | `Matrix([[log(t)], [t**n*(n + 1)], [t**n]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_scalar_derivative_term` | `Matrix([[c], [c*n*t**n], [c*m*t**m]])` |
| `omit_vector_derivative_term` | `Matrix([[c*log(t)], [c*t**n], [c*t**m]])` |
| `subtract_second_product_term` | `Matrix([[c*(1 - log(t))], [c*t**n*(n - 1)], [c*t**m*(m - 1)]])` |
| `count_first_product_term_twice` | `Matrix([[c*(log(t) + 2)], [c*t**n*(2*n + 1)], [c*t**m*(2*m + 1)]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## scalar_power — easy, q-128587

### 1. Specific observed instance

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨t,\,{t}^{2},\,2{t}^{3}⟩$ and $u(t)={t}^{3}.$

Parameters: `{"a": 1, "b": 1, "c": 2, "n": 3, "p": 1, "q": 2, "r": 3}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate a scalar function times a three-component vector: u f′ + u′ f. The fixed component structures assess the same observed derivative/cancellation workload.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[a*t**(n + p - 1)*(n + p)], [b*t**(n + q - 1)*(n + q)], [c*t**(n + r - 1)*(n + r)]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨2t,\,5{t}^{3},\,9{t}^{4}⟩` | `source_mixed_power_and_coefficient_A` | `Matrix([[c*t**p], [b*t**n*(n + q)], [n*r*t**(n + r - 2)]])` |
| 0 | `⟨{t}^{4},\,{t}^{3},\,{t}^{2}⟩` | `source_descending_power_bank` | `Matrix([[t**(n + p)], [t**n], [t**q]])` |
| 0 | `⟨2t,\,5{t}^{4},\,3{t}^{5}⟩` | `source_mixed_power_and_coefficient_B` | `Matrix([[c*t**p], [b*t**(n + q - 1)*(n + q)], [n*t**(n + r - 1)]])` |
| 0 | `⟨4{t}^{3},\,5{t}^{2},\,9{t}^{4}⟩` | `retain_first_alter_second_and_third` | `Matrix([[a*t**(n + p - 1)*(n + p)], [b*t**q*(n + q)], [n*r*t**(n + r - 2)]])` |
| 0 | `⟨4{t}^{3},\,5{t}^{4},\,12{t}^{5}⟩` | `correct` | `Matrix([[a*t**(n + p - 1)*(n + p)], [b*t**(n + q - 1)*(n + q)], [c*t**(n + r - 1)*(n + r)]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_scalar_derivative_term` | `Matrix([[a*p*t**(n + p - 1)], [b*q*t**(n + q - 1)], [c*r*t**(n + r - 1)]])` |
| `omit_vector_derivative_term` | `Matrix([[a*n*t**(n + p - 1)], [b*n*t**(n + q - 1)], [c*n*t**(n + r - 1)]])` |
| `subtract_second_product_term` | `Matrix([[a*t**(n + p - 1)*(-n + p)], [b*t**(n + q - 1)*(-n + q)], [c*t**(n + r - 1)*(-n + r)]])` |
| `count_first_product_term_twice` | `Matrix([[a*t**(n + p - 1)*(n + 2*p)], [b*t**(n + q - 1)*(n + 2*q)], [c*t**(n + r - 1)*(n + 2*r)]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## scalar_exp — easy, q-128894

### 1. Specific observed instance

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨{e}^{t+1},\,{e}^{-t},\,{e}^{2t}⟩$ and $v(t)={e}^{t}.$

Parameters: `{"a": 1, "b": 2, "s": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate a scalar function times a three-component vector: u f′ + u′ f. The fixed component structures assess the same observed derivative/cancellation workload.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[2*a*exp(2*a*t + s)], [0], [(a + b)*exp(t*(a + b))]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨2{e}^{t+1},\,2,\,4{e}^{3t}⟩` | `leave_first_exponent_uncombined_and_double_second_rate` | `Matrix([[2*a*exp(a*t + s)], [2*a], [2*b*exp(t*(a + b))]])` |
| 0 | `⟨{e}^{2t+1},\,0,\,-3{e}^{3t}⟩` | `omit_first_product_term_reverse_last` | `Matrix([[a*exp(2*a*t + s)], [0], [(-a - b)*exp(t*(a + b))]])` |
| 0 | `⟨{e}^{2t+1},\,-2,\,2{e}^{3t}⟩` | `omit_scalar_derivative_and_miscancel_middle` | `Matrix([[a*exp(2*a*t + s)], [-2*a], [b*exp(t*(a + b))]])` |
| 0 | `⟨{e}^{2t+1},\,1,\,2{e}^{3t}⟩` | `omit_first_product_term_and_leave_middle_constant` | `Matrix([[a*exp(2*a*t + s)], [a], [b*exp(t*(a + b))]])` |
| 0 | `⟨2{e}^{2t+1},\,0,\,3{e}^{3t}⟩` | `correct` | `Matrix([[2*a*exp(2*a*t + s)], [0], [(a + b)*exp(t*(a + b))]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_scalar_derivative_term` | `Matrix([[a*exp(2*a*t + s)], [-a], [b*exp(t*(a + b))]])` |
| `omit_vector_derivative_term` | `Matrix([[a*exp(2*a*t + s)], [a], [a*exp(t*(a + b))]])` |
| `subtract_second_product_term` | `Matrix([[0], [-2*a], [(-a + b)*exp(t*(a + b))]])` |
| `count_first_product_term_twice` | `Matrix([[3*a*exp(2*a*t + s)], [-a], [(a + 2*b)*exp(t*(a + b))]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## scalar_base — easy, q-33446

### 1. Specific observed instance

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨{2}^{t},\,{2}^{t+1},\,{2}^{2t}+1⟩$ and $v(t)=\frac{1}{{2}^{t}}.$

Parameters: `{"base": 2, "c": 1, "s": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate a scalar function times a three-component vector: u f′ + u′ f. The fixed component structures assess the same observed derivative/cancellation workload.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[0], [0], [(base**(2*t) - c)*log(base)/base**t]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨0,\,0,\,\frac{({2}^{2t}-1)\operatorname{ln}⁡2}{{2}^{t}}⟩` | `correct` | `Matrix([[0], [0], [(base**(2*t) - c)*log(base)/base**t]])` |
| 0 | `⟨\operatorname{ln}⁡2,\,\operatorname{ln}⁡2,\,({2}^{2t}-1)\operatorname{ln}⁡2⟩` | `drop_scalar_denominator_and_fail_first_cancellations` | `Matrix([[log(base)], [log(base)], [(base**(2*t) - c)*log(base)]])` |
| 0 | `⟨0,\,-\frac{\operatorname{ln}⁡2}{{2}^{t}},\,0⟩` | `residual_middle_only` | `Matrix([[0], [-log(base)/base**t], [0]])` |
| 0 | `⟨{2}^{t},\,0,\,\frac{({2}^{2t}-1)\operatorname{ln}⁡2}{{2}^{t}}⟩` | `retain_first_exponential` | `Matrix([[base**t], [0], [(base**(2*t) - c)*log(base)/base**t]])` |
| 0 | `⟨0,\,\operatorname{ln}⁡2,\,-\frac{\operatorname{ln}⁡2}{{2}^{t}}⟩` | `middle_log_and_constant_only_last` | `Matrix([[0], [log(base)], [-c*log(base)/base**t]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_scalar_derivative_term` | `Matrix([[log(base)], [base**s*log(base)], [2*base**t*log(base)]])` |
| `omit_vector_derivative_term` | `Matrix([[-log(base)], [-base**s*log(base)], [(-base**(2*t) - c)*log(base)/base**t]])` |
| `subtract_second_product_term` | `Matrix([[2*log(base)], [2*base**s*log(base)], [(3*base**(2*t) + c)*log(base)/base**t]])` |
| `count_first_product_term_twice` | `Matrix([[log(base)], [base**s*log(base)], [(3*base**(2*t) - c)*log(base)/base**t]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## dot_polynomial — moderate, q-32298

### 1. Specific observed instance

Find $(f\cdot g)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =20t\,i-2t\,j+(2+5t)\,k \\ g(t) & ={t}^{3}\,i+t\,j+({t}^{2}+t)\,k\end{aligned}
$$

Parameters: `{"a": 20, "b": -2, "c": 2, "d": 5}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed dot product by differentiating both inputs and adding the two component dot products. Self-product templates supply the observed first and second derivatives; evaluation retains the source point-evaluation task.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `4*a*t**3 + 2*b*t + 2*c*t + c + 3*d*t**2 + 2*d*t`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `80{t}^{3}+11{t}^{2}+12t+2` | `source_wrong_1` | `4*a*t**3 + c*t + c + 2*d*t**2 + 2*d*t + t**2` |
| 0 | `80{t}^{3}+6{t}^{2}+10t+2` | `source_wrong_2` | `4*a*t**3 + 2*b*t + 3*c*t**2 + 2*c*t + c + 2*d*t` |
| 0 | `60{t}^{3}+15{t}^{2}+14t+2` | `source_wrong_3` | `3*a*t**3 + 2*c*t + c + 3*d*t**2 + 2*d*t` |
| 0 | `60{t}^{3}+7{t}^{2}+10t+2` | `source_wrong_4` | `3*a*t**3 + 2*b*t + c*t**2 + 2*c*t + c + d*t**2 + 2*d*t` |
| 0 | `80{t}^{3}+15{t}^{2}+10t+2` | `correct` | `4*a*t**3 + 2*b*t + 2*c*t + c + 3*d*t**2 + 2*d*t` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_product_term` | `t*(a*t**2 + b + d*t + d)` |
| `omit_first_product_term` | `3*a*t**3 + b*t + 2*c*t + c + 2*d*t**2 + d*t` |
| `reverse_sign_of_entire_result` | `-4*a*t**3 - 2*b*t - 2*c*t - c - 3*d*t**2 - 2*d*t` |
| `multiply_derivatives_instead_of_product_rule` | `3*a*t**2 + b + 2*d*t + d` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## dot_self_cubic — moderate, q-32804

### 1. Specific observed instance

Given $f(t)=2{t}^{3}\,i-2t\,j+(1+5{t}^{2})\,k$, find $({f}^{′}\cdot f)^{′}(t).$

Parameters: `{"a": 2, "b": -2, "c": 1, "d": 5}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed dot product by differentiating both inputs and adding the two component dot products. Self-product templates supply the observed first and second derivatives; evaluation retains the source point-evaluation task.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `15*a**2*t**4 + b**2 + 2*c*d + 6*d**2*t**2`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `12{t}^{4}+150{t}^{2}+14` | `source_wrong_1` | `3*a**2*t**4 + b**2 + 2*c*d + 6*d**2*t**2` |
| 0 | `60{t}^{4}+50{t}^{2}+6` | `source_wrong_2` | `15*a**2*t**4 + b**2 + 2*c + 2*d**2*t**2` |
| 0 | `60{t}^{4}+150{t}^{2}+14` | `correct` | `15*a**2*t**4 + b**2 + 2*c*d + 6*d**2*t**2` |
| 0 | `12{t}^{4}+50{t}^{2}+14` | `source_wrong_3` | `3*a**2*t**4 + b**2 + 2*c*d + 2*d**2*t**2` |
| 0 | `60{t}^{4}+150{t}^{2}-10` | `source_wrong_4` | `15*a**2*t**4 - 2*c*d + 6*d**2*t**2` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_product_term` | `6*a**2*t**4 + 2*c*d + 2*d**2*t**2` |
| `omit_first_product_term` | `9*a**2*t**4 + b**2 + 4*d**2*t**2` |
| `reverse_sign_of_entire_result` | `-15*a**2*t**4 - b**2 - 2*c*d - 6*d**2*t**2` |
| `multiply_derivatives_instead_of_product_rule` | `18*a**2*t**3 + 4*d**2*t` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## dot_self_shifted — moderate, q-32835

### 1. Specific observed instance

Given $f(t)=⟨{t}^{2}-1\,,\,2t\,,\,{t}^{3}-1⟩$, find $({f}^{′}\cdot f)^{′}(t).$

Parameters: `{"a": 1, "b": 2, "c": 1, "h": 1, "k": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed dot product by differentiating both inputs and adding the two component dot products. Self-product templates supply the observed first and second derivatives; evaluation retains the source point-evaluation task.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `6*a**2*t**2 - 2*a*h + b**2 + 15*c**2*t**4 - 6*c*k*t`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `3{t}^{4}-2{t}^{2}+6t+2` | `source_wrong_1` | `-2*a**2*t**2 - 2*a*h + b**2 + 3*c**2*t**4 + 6*c*k*t` |
| 0 | `15{t}^{4}+6{t}^{2}+2` | `source_wrong_2` | `6*a**2*t**2 - 2*a*h + b**2 + 15*c**2*t**4` |
| 0 | `15{t}^{4}-6t+2` | `source_wrong_3` | `-2*a*h + b**2 + 15*c**2*t**4 - 6*c*k*t` |
| 0 | `3{t}^{4}+2{t}^{2}-6t+2` | `source_wrong_4` | `2*a**2*t**2 - 2*a*h + b**2 + 3*c**2*t**4 - 6*c*k*t` |
| 0 | `15{t}^{4}+6{t}^{2}-6t+2` | `correct` | `6*a**2*t**2 - 2*a*h + b**2 + 15*c**2*t**4 - 6*c*k*t` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_product_term` | `2*a**2*t**2 - 2*a*h + 6*c**2*t**4 - 6*c*k*t` |
| `omit_first_product_term` | `4*a**2*t**2 + b**2 + 9*c**2*t**4` |
| `reverse_sign_of_entire_result` | `-6*a**2*t**2 + 2*a*h - b**2 - 15*c**2*t**4 + 6*c*k*t` |
| `multiply_derivatives_instead_of_product_rule` | `4*a**2*t + 18*c**2*t**3` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## dot_self_evaluate — moderate, q-32837

### 1. Specific observed instance

Given $f(t)=({t}^{3}-1)\,i+({t}^{2}-2)\,j+4{t}^{2}\,k$, evaluate $({f}^{′}\cdot f)^{′}(0).$

Parameters: `{"a": 1, "b": 1, "c": 4, "h": 1, "k": 2, "x": 0}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed dot product by differentiating both inputs and adding the two component dot products. Self-product templates supply the observed first and second derivatives; evaluation retains the source point-evaluation task.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `15*a**2*x**4 - 6*a*h*x + 6*b**2*x**2 - 2*b*k + 6*c**2*x**2`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `4` | `source_wrong_1` | `-15*a**2*x**4 + 6*a*h*x - 6*b**2*x**2 + 2*b*k - 6*c**2*x**2` |
| 0 | `-8` | `source_wrong_2` | `30*a**2*x**4 - 12*a*h*x + 12*b**2*x**2 - 4*b*k + 12*c**2*x**2` |
| 0 | `-4` | `correct` | `15*a**2*x**4 - 6*a*h*x + 6*b**2*x**2 - 2*b*k + 6*c**2*x**2` |
| 0 | `0` | `source_wrong_3` | `0` |
| 0 | `8` | `source_wrong_4` | `-30*a**2*x**4 + 12*a*h*x - 12*b**2*x**2 + 4*b*k - 12*c**2*x**2` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_derivative_product` | `x**2*(9*a**2*x**2 + 4*b**2 + 4*c**2)` |
| `reverse_sign_of_second_derivative_product` | `3*a**2*x**4 + 6*a*h*x + 2*b**2*x**2 + 2*b*k + 2*c**2*x**2` |
| `count_second_derivative_product_twice` | `21*a**2*x**4 - 12*a*h*x + 8*b**2*x**2 - 4*b*k + 8*c**2*x**2` |
| `omit_factor_two_from_second_derivatives` | `12*a**2*x**4 - 3*a*h*x + 5*b**2*x**2 - b*k + 5*c**2*x**2` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## dot_log_reciprocal — moderate, q-33336

### 1. Specific observed instance

Find $(f\cdot g)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =\operatorname{ln}⁡t\,i+\frac{1}{t}\,j+t\,k \\ g(t) & =t\,i+\frac{1}{t}\,j+\operatorname{ln}⁡t\,k\end{aligned}
$$

Parameters: `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "h": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: t>0.

### 2. Generalized mathematical pattern

Differentiate the displayed dot product by differentiating both inputs and adding the two component dot products. Self-product templates supply the observed first and second derivatives; evaluation retains the source point-evaluation task.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `a*d*log(t) + a*d - 2*b*e/t**3 + c*h*log(t) + c*h`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `2\operatorname{ln}⁡t+\frac{2}{{t}^{3}}` | `source_wrong_1` | `a*d*log(t) + 2*b*e/t**3 + c*h*log(t)` |
| 0 | `\operatorname{ln}⁡t+1-\frac{1}{{t}^{3}}` | `source_wrong_2` | `(-b*e + t**3*(a*d*log(t) + a*d + c*h*log(t) + c*h)/2)/t**3` |
| 0 | `\operatorname{ln}⁡t+1+\frac{1}{{t}^{3}}` | `source_wrong_3` | `(b*e + t**3*(a*d*log(t) + a*d + c*h*log(t) + c*h)/2)/t**3` |
| 0 | `2\operatorname{ln}⁡t+2-\frac{2}{{t}^{3}}` | `correct` | `a*d*log(t) + a*d - 2*b*e/t**3 + c*h*log(t) + c*h` |
| 0 | `0` | `source_wrong_4` | `0` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_product_term` | `a*d - b*e/t**3 + c*h*log(t)` |
| `omit_second_product_term_and_reverse_sign` | `-a*d + b*e/t**3 - c*h*log(t)` |
| `reverse_sign_of_entire_result` | `-a*d*log(t) - a*d + 2*b*e/t**3 - c*h*log(t) - c*h` |
| `multiply_derivatives_instead_of_product_rule` | `(b*e + t**3*(a*d + c*h))/t**4` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## cross_matrix — hard, q-32353

### 1. Specific observed instance

Find $(f\times g)^{′}(t)$ where

$$
f(t)=[\begin{aligned}3{t}^{2} \\ t+4 \\ 8\end{aligned}],\,g(t)=[\begin{aligned}t+2 \\ -2{t}^{2} \\ 5t\end{aligned}]
$$

Parameters: `{"a": 3, "b": 4, "c": 8, "d": 2, "e": -2, "h": 5}`. Field type radio, five math choices; legacy duplicate and designated active bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed ordered cross product; expand each term through signed minors and add entire vectors. The self template uses f″×f plus f′×f′=0.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[b*h - 2*c*e*t + 2*h*t], [-3*a*h*t**2 + c], [4*a*e*t**3 - b - d - 2*t]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `\begin{bmatrix}-24t^{3} - 2t - 6 \\ 8 - 45t^{2} \\ 42t + 20\end{bmatrix}` | `source_wrong_1` | `Matrix([[4*a*e*t**3 - b - d - 2*t], [-3*a*h*t**2 + c], [b*h - 2*c*e*t + 2*h*t]])` |
| 0 | `\begin{bmatrix}-42t - 20 \\ 8 - 45t^{2} \\ 24t^{3} + 2t + 6\end{bmatrix}` | `source_wrong_2` | `Matrix([[-b*h + 2*c*e*t - 2*h*t], [-3*a*h*t**2 + c], [-4*a*e*t**3 + b + d + 2*t]])` |
| 0 | `\begin{bmatrix}42t + 20 \\ 8 - 45t^{2} \\ -24t^{3} - 2t - 6\end{bmatrix}` | `correct` | `Matrix([[b*h - 2*c*e*t + 2*h*t], [-3*a*h*t**2 + c], [4*a*e*t**3 - b - d - 2*t]])` |
| 0 | `\begin{bmatrix}8 - 45t^{2} \\ 42t + 20 \\ -24t^{3} - 2t - 6\end{bmatrix}` | `source_wrong_3` | `Matrix([[-3*a*h*t**2 + c], [b*h - 2*c*e*t + 2*h*t], [4*a*e*t**3 - b - d - 2*t]])` |
| 0 | `\begin{bmatrix}21t + 10 \\ 45t^{2} \\ -24t^{3} - 2t - 6\end{bmatrix}` | `source_wrong_4` | `Matrix([[b*h/2 - c*e*t + h*t], [3*a*h*t**2], [4*a*e*t**3 - b - d - 2*t]])` |
| 1 | `[\begin{aligned}21t+10 \\ 45{t}^{2} \\ -24{t}^{3}-2t-6\end{aligned}]` | `source_wrong_4` | `Matrix([[b*h/2 - c*e*t + h*t], [3*a*h*t**2], [4*a*e*t**3 - b - d - 2*t]])` |
| 1 | `[\begin{aligned}8-45{t}^{2} \\ 42t+20 \\ -24{t}^{3}-2t-6\end{aligned}]` | `source_wrong_3` | `Matrix([[-3*a*h*t**2 + c], [b*h - 2*c*e*t + 2*h*t], [4*a*e*t**3 - b - d - 2*t]])` |
| 1 | `[\begin{aligned}-42t-20 \\ 8-45{t}^{2} \\ 24{t}^{3}+2t+6\end{aligned}]` | `source_wrong_2` | `Matrix([[-b*h + 2*c*e*t - 2*h*t], [-3*a*h*t**2 + c], [-4*a*e*t**3 + b + d + 2*t]])` |
| 1 | `[\begin{aligned}-24{t}^{3}-2t-6 \\ 8-45{t}^{2} \\ 42t+20\end{aligned}]` | `source_wrong_1` | `Matrix([[4*a*e*t**3 - b - d - 2*t], [-3*a*h*t**2 + c], [b*h - 2*c*e*t + 2*h*t]])` |
| 1 | `[\begin{aligned}42t+20 \\ 8-45{t}^{2} \\ -24{t}^{3}-2t-6\end{aligned}]` | `correct` | `Matrix([[b*h - 2*c*e*t + 2*h*t], [-3*a*h*t**2 + c], [4*a*e*t**3 - b - d - 2*t]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_cross_product_term` | `Matrix([[h*t], [-2*a*h*t**2], [2*a*e*t**3 - d - t]])` |
| `omit_first_cross_product_term` | `Matrix([[b*h - 2*c*e*t + h*t], [-a*h*t**2 + c], [2*a*e*t**3 - b - t]])` |
| `reverse_cross_order_in_both_terms` | `Matrix([[-b*h + 2*c*e*t - 2*h*t], [3*a*h*t**2 - c], [-4*a*e*t**3 + b + d + 2*t]])` |
| `use_positive_middle_cofactor` | `Matrix([[b*h - 2*c*e*t + 2*h*t], [3*a*h*t**2 - c], [4*a*e*t**3 - b - d - 2*t]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## cross_monomials — hard, q-128896

### 1. Specific observed instance

Find $(f\times g)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨t,\,5,\,{t}^{4}⟩, \\ g(t) & =⟨{t}^{2},\,{t}^{3},\,t⟩.\end{aligned}
$$

Parameters: `{"a": 1, "b": 5, "c": 1, "d": 1, "e": 1, "h": 1, "n": 4, "p": 2, "q": 3}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed ordered cross product; expand each term through signed minors and add entire vectors. The self template uses f″×f plus f′×f′=0.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[b*h - c*e*n*t**(n + q - 1) - c*e*q*t**(n + q - 1)], [-2*a*h*t + c*d*n*t**(n + p - 1) + c*d*p*t**(n + p - 1)], [a*e*q*t**q + a*e*t**q - b*d*p*t**(p - 1)]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨5{t}^{6},\,{t}^{5}+4{t}^{2},\,4{t}^{3}⟩` | `source_wrong_1` | `Matrix([[b*c*e*t**(n + q - 1)], [a*h*n*t**2 + c*d*t**(n + p - 1)], [a*e*t**q*(q + 1)]])` |
| 0 | `⟨{t}^{6}-5,\,4{t}^{5}+2t,\,4{t}^{3}-10t⟩` | `source_wrong_2` | `Matrix([[-b*h + c*e*t**(n + q - 1)], [2*a*h*t + c*d*n*t**(n + p - 1)], [a*e*q*t**q + a*e*t**q - b*d*p*t**(p - 1)]])` |
| 0 | `⟨2{t}^{6}+1,\,4{t}^{5},\,{t}^{3}-5t⟩` | `source_wrong_3` | `Matrix([[a*h + c*e*p*t**(n + q - 1)], [c*d*n*t**(n + p - 1)], [a*e*t**q - b*d*t**(p - 1)]])` |
| 0 | `⟨-7{t}^{6}+5,\,6{t}^{5}-2t,\,4{t}^{3}-10t⟩` | `correct` | `Matrix([[b*h - c*e*n*t**(n + q - 1) - c*e*q*t**(n + q - 1)], [-2*a*h*t + c*d*n*t**(n + p - 1) + c*d*p*t**(n + p - 1)], [a*e*q*t**q + a*e*t**q - b*d*p*t**(p - 1)]])` |
| 0 | `⟨7{t}^{6},\,6{t}^{5}-5,\,4{t}^{3}+2t⟩` | `source_wrong_4` | `Matrix([[c*e*t**(n + q - 1)*(n + q)], [-b + c*d*n*t**(n + p - 1) + c*d*p*t**(n + p - 1)], [a*(e*q*t**q + e*t**q + 2*h*t)]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_cross_product_term` | `Matrix([[-c*e*n*t**(n + q - 1)], [(-a*h*t**2 + c*d*n*t**(n + p))/t], [a*e*t**q]])` |
| `omit_first_cross_product_term` | `Matrix([[(b*h*t - c*e*q*t**(n + q))/t], [(-a*h*t**2 + c*d*p*t**(n + p))/t], [a*e*q*t**q - b*d*p*t**p/t]])` |
| `reverse_cross_order_in_both_terms` | `Matrix([[-b*h + c*e*n*t**(n + q - 1) + c*e*q*t**(n + q - 1)], [2*a*h*t - c*d*n*t**(n + p - 1) - c*d*p*t**(n + p - 1)], [-a*e*q*t**q - a*e*t**q + b*d*p*t**(p - 1)]])` |
| `use_positive_middle_cofactor` | `Matrix([[b*h - c*e*n*t**(n + q - 1) - c*e*q*t**(n + q - 1)], [2*a*h*t - c*d*n*t**(n + p - 1) - c*d*p*t**(n + p - 1)], [a*e*q*t**q + a*e*t**q - b*d*p*t**(p - 1)]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## cross_shifted — hard, q-32347

### 1. Specific observed instance

Find $(f\times g)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨6{t}^{2},\,2t,\,6⟩ \\ g(t) & =⟨3,\,3{t}^{2},\,4t-1⟩\end{aligned}
$$

Parameters: `{"a": 6, "b": 2, "c": 6, "d": 3, "e": 3, "h": 4, "k": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed ordered cross product; expand each term through signed minors and add entire vectors. The self template uses f″×f plus f′×f′=0.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[2*b*h*t - b*k - 2*c*e*t], [a*t*(-3*h*t + 2*k)], [4*a*e*t**3 - b*d]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨20t-2,\,36{t}^{2}+12t,\,72{t}^{3}⟩` | `source_wrong_1` | `Matrix([[2*b*h*t - b*k + h*t], [2*a*t*(e*t + k)], [4*a*e*t**3]])` |
| 0 | `⟨8t-2,\,-48{t}^{2}+12t,\,36{t}^{3}-6⟩` | `source_wrong_2` | `Matrix([[b*(h*t - k)], [2*a*t*(-h*t + k)], [2*a*e*t**3 - b*d]])` |
| 0 | `⟨48t-2,\,-362{t}^{2}+12t,\,6⟩` | `source_wrong_3` | `Matrix([[2*a*h*t - b*k], [t*(-20*a*e*t + 2*a*k - b*t)], [b*d]])` |
| 0 | `⟨-28t,\,-24{t}^{2},\,36{t}^{3}⟩` | `source_wrong_4` | `Matrix([[t*(b*h - 2*c*e)], [-a*h*t**2], [2*a*e*t**3]])` |
| 0 | `⟨-20t-2,\,-72{t}^{2}+12t,\,72{t}^{3}-6⟩` | `correct` | `Matrix([[2*b*h*t - b*k - 2*c*e*t], [a*t*(-3*h*t + 2*k)], [4*a*e*t**3 - b*d]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `omit_second_cross_product_term` | `Matrix([[b*(h*t - k)], [2*a*t*(-h*t + k)], [2*a*e*t**3 - b*d]])` |
| `omit_first_cross_product_term` | `Matrix([[t*(b*h - 2*c*e)], [-a*h*t**2], [2*a*e*t**3]])` |
| `reverse_cross_order_in_both_terms` | `Matrix([[-2*b*h*t + b*k + 2*c*e*t], [a*t*(3*h*t - 2*k)], [-4*a*e*t**3 + b*d]])` |
| `use_positive_middle_cofactor` | `Matrix([[2*b*h*t - b*k - 2*c*e*t], [a*t*(3*h*t - 2*k)], [4*a*e*t**3 - b*d]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

## cross_self — hard, q-32836

### 1. Specific observed instance

Given $f(t)=⟨1-{t}^{2}\,,\,1-{t}^{3}\,,\,1-t⟩$, find $({f}^{′}\times f)^{′}(t).$

Parameters: `{"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "h": 1}`. Field type radio, five math choices; one designated bank. Components are exact. Domains: all real t.

### 2. Generalized mathematical pattern

Differentiate the displayed ordered cross product; expand each term through signed minors and add entire vectors. The self template uses f″×f plus f′×f′=0.

### 3. Components and complete bank mapping

Prompt vector(s), scalar (easy), derivatives, product terms, and answer are calculated from the same parameters. Correct formula: `Matrix([[6*d*t*(-e + h*t)], [2*b*(e - h*t)], [6*a*d*t - 2*b*c - 4*b*d*t**3]])`.

| Captured field | Original choice (entire value) | Recipe | Symbolic complete value |
|---|---|---|---|
| 0 | `⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+8{t}^{3}⟩` | `source_wrong_1` | `Matrix([[6*d*t*(-e + h*t)], [2*b*(e - h*t)], [2*b*(-c + 4*d*t**3)]])` |
| 0 | `⟨0\,,\,0\,,\,-2+6t-4{t}^{3}⟩` | `source_wrong_2` | `Matrix([[0], [0], [6*a*d*t - 2*b*c - 4*b*d*t**3]])` |
| 0 | `⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+6t-4{t}^{3}⟩` | `correct` | `Matrix([[6*d*t*(-e + h*t)], [2*b*(e - h*t)], [6*a*d*t - 2*b*c - 4*b*d*t**3]])` |
| 0 | `⟨-6t+6{t}^{2}\,,\,-2+2t\,,\,-6t+8{t}^{3}⟩` | `source_wrong_3` | `Matrix([[6*d*t*(-e + h*t)], [2*b*(-e + h*t)], [2*d*t*(-3*a + 4*b*t**2)]])` |
| 0 | `⟨-6+6{t}^{2}\,,\,-2t\,,\,-2+6t-4{t}^{3}⟩` | `source_wrong_4` | `Matrix([[6*d*(-e + h*t**2)], [-2*b*h*t], [6*a*d*t - 2*b*c - 4*b*d*t**3]])` |

Authored default whole bank (correct value above plus these four operation-derived wrong values):

| Wrong operation | Complete symbolic value |
|---|---|
| `retain_only_self_cross_zero_term` | `Matrix([[0], [0], [0]])` |
| `reverse_cross_order_in_both_terms` | `Matrix([[6*d*t*(e - h*t)], [2*b*(-e + h*t)], [-6*a*d*t + 2*b*c + 4*b*d*t**3]])` |
| `use_positive_middle_cofactor` | `Matrix([[6*d*t*(-e + h*t)], [2*b*(-e + h*t)], [6*a*d*t - 2*b*c - 4*b*d*t**3]])` |
| `differentiate_both_inputs_instead_of_product_rule` | `Matrix([[6*d*h*t], [-2*b*h], [-6*b*d*t**2]])` |

Wrong-value interpretations are hypotheses unless the algebra clearly identifies an omitted term/permutation. Every expression above reproduces its source option; the full bank is kept together. The formulas generalize the observed pattern using prompt coefficients, powers, and intermediate results. They do not derive wrong options from arbitrary unrelated random offsets.

### 4. Reusable Markdown/value template

Fixed: the source prompt clause, product operator, vector notation family, field layout, rule sentences, and derivative → products → sum sequence. Variable: the displayed component/scalar expressions and every resulting derivative, product-term, option, and final expression. Conditional: one evaluation substitution for `dot_self_evaluate`; one legacy notation profile for `cross_matrix`; domains positive for logarithmic templates. No plot components. See `build_easy`, `build_moderate`, `build_hard`, and `render` in the script for the derived values and sequence.

