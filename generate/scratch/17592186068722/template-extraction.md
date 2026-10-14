# Template extraction

## 1. Specific source descriptions

q-2189 (easy): Calculate prompt; inner x³+4, derivative 3x², outer power 5. Every value is an expression plus C. The source retains an incorrect extra x divisor, unchanged exponent/divisor, and two derivative/power variants with denominator 2.

q-2195 (easy): trailing equals prompt; inner x²+1, derivative 2x, outer power 12. Bank includes retained derivative, retained derivative with reversed sign, retained derivative with sign and missing successor, and missing successor alone.

q-113581 (moderate): Calculate prompt; inner 2x⁶−3, matched derivative 12x⁵, square root. Rewriting explicitly inserts a multiplication dot. Bank contains successor-power coefficients 1/2 and 3/2 and two negative reciprocal roots with coefficients 1/2 and 2.

q-2390 (moderate): Calculate prompt; inner 5x²−4, matched derivative 10x, square root. Rewriting uses juxtaposition. The bank has negative successor power coefficients −3/2 and −2/3 and reciprocal-successor exponent 2/3 with coefficients 3 and 3/2.

q-72382 (hard): Calculate prompt; inner 1+x⁵ (constant first), derivative 5x⁴, reciprocal square root. Incorrect answers include roots of the cube, inverted power-rule coefficient and retained x. Both primitive and conclusion are aligned blocks.

Every source has one selection radio field; no feedback, units, plots or answer diagnostics. Complete exact prompts, solutions and banks appear in review.md, not truncated extracts.

## 2. Shared mathematical pattern

Let F=ax^m+b and D=amx^(m−1). Integrate D F^q by u=F, du=D dx and the power rule F^(q+1)/(q+1)+C. Easy uses integer q=n; moderate q=1/2; hard q=−1/2. This exact derivative matching is essential: no learner must compensate a constant factor. Keep the root families at their observed square-root demand.

## 3. Components and complete bank mapping

The following per-source maps give every original value, field, designation, exact symbolic recipe, label and profile. Labels describe reproduction operations; they do not establish historical author intention. q-2189 and q-2390 contain opaque compound recipes, retained as public evidence-only profiles. No literal answer lookup or arbitrary numerical fitting is used. Other observed profiles also carry explicit inference limits. Normal output uses separately authored complete method-derived banks.

### q-2189 / historical_2189

Parameters: `{"a": 1, "m": 3, "b": 4, "n": 5}`; field `selection`, math radio.

- Incorrect `2452d0d5-3314-543c-8155-cd466478eb94`: $\frac{({x}^{3}+4)^{6}}{6x}+C$; operation `divide_primitive_by_x`; exact expression without C `(x**3 + 4)**6/(6*x)`.
- Incorrect `5181e9aa-208f-5201-b3ec-4362a8aec6e2`: $\frac{({x}^{3}+4)^{5}}{5}+C$; operation `omit_exponent_increment`; exact expression without C `(x**3 + 4)**5/5`.
- Incorrect `618b6980-5d49-54b2-98e1-6b2c17a106f2`: $\frac{3{x}^{2}({x}^{3}+4)^{6}}{2}+C$; operation `historical_derivative_retained_denominator_m_minus_one`; exact expression without C `3*x**2*(x**3 + 4)**6/2`.
- Correct `c874aedd-75e1-5980-8701-168e514e7383`: $\frac{({x}^{3}+4)^{6}}{6}+C$; operation `power_rule`; exact expression without C `(x**3 + 4)**6/6`.
- Incorrect `fa9cf091-1a90-540f-a2e6-02899e4f742d`: $\frac{3x({x}^{3}+4)^{6}}{2}+C$; operation `historical_lower_multiplier_power_denominator_m_minus_one`; exact expression without C `3*x*(x**3 + 4)**6/2`.

### q-2195 / observed_2195

Parameters: `{"a": 1, "m": 2, "b": 1, "n": 12}`; field `selection`, math radio.

- Incorrect `7d5927e7-3d1a-5589-9ab4-b01b479f66f5`: $\frac{2x({x}^{2}+1)^{13}}{13}+C$; operation `retain_derivative`; exact expression without C `2*x*(x**2 + 1)**13/13`.
- Correct `a65798db-1640-5ac0-9550-f0316b86d818`: $\frac{({x}^{2}+1)^{13}}{13}+C$; operation `power_rule`; exact expression without C `(x**2 + 1)**13/13`.
- Incorrect `a71c627c-e9b2-5a11-b21d-b190f3a77006`: $-\frac{2x({x}^{2}+1)^{13}}{13}+C$; operation `retain_derivative_and_reverse_sign`; exact expression without C `-2*x*(x**2 + 1)**13/13`.
- Incorrect `d436ea16-40f5-50d5-8944-8947c0a63c89`: $-\frac{2x({x}^{2}+1)^{12}}{12}+C$; operation `retain_derivative_reverse_sign_omit_increment`; exact expression without C `-x*(x**2 + 1)**12/6`.
- Incorrect `eb4463e3-17c4-52b2-809c-06d7c4b4e286`: $\frac{({x}^{2}+1)^{12}}{12}+C$; operation `omit_exponent_increment`; exact expression without C `(x**2 + 1)**12/12`.

### q-113581 / observed_113581

Parameters: `{"a": 2, "m": 6, "b": -3, "n": 0}`; field `selection`, math radio.

- Incorrect `25e9f2b0-37e6-50e9-81f9-f4870eb89a96`: $\frac{(2{x}^{6}-3)^{3/2}}{2}+C$; operation `divide_by_reciprocal_of_original_exponent`; exact expression without C `(2*x**6 - 3)**(3/2)/2`.
- Correct `5c181d1d-bf18-55ce-a822-d1dd57423b61`: $\frac{2(2{x}^{6}-3)^{3/2}}{3}+C$; operation `power_rule`; exact expression without C `2*(2*x**6 - 3)**(3/2)/3`.
- Incorrect `96815189-eaa4-553f-a459-50b35808ed3d`: $-\frac{1}{2\sqrt{2{x}^{6}-3}}+C$; operation `differentiate_power_and_reverse_sign`; exact expression without C `-1/(2*sqrt(2*x**6 - 3))`.
- Incorrect `9f1a82cf-c0af-5ed8-82c6-891e0d588025`: $-\frac{2}{\sqrt{2{x}^{6}-3}}+C$; operation `derivative_exponent_reciprocal_coefficient_reverse_sign`; exact expression without C `-2/sqrt(2*x**6 - 3)`.
- Incorrect `cdcc076d-df76-5525-b8c1-56042f929b6e`: $\frac{3(2{x}^{6}-3)^{3/2}}{2}+C$; operation `multiply_by_successor`; exact expression without C `3*(2*x**6 - 3)**(3/2)/2`.

### q-2390 / historical_2390

Parameters: `{"a": 5, "m": 2, "b": -4, "n": 0}`; field `selection`, math radio.

- Incorrect `2029e990-e06c-5de3-bbb1-b0f88ba76514`: $-\frac{3(5{x}^{2}-4)^{3/2}}{2}+C$; operation `reverse_sign_multiply_by_successor`; exact expression without C `-3*(5*x**2 - 4)**(3/2)/2`.
- Correct `26e955b2-8d3d-529c-aa79-f141fc091ae9`: $\frac{2(5{x}^{2}-4)^{3/2}}{3}+C$; operation `power_rule`; exact expression without C `2*(5*x**2 - 4)**(3/2)/3`.
- Incorrect `2df24f84-49a3-5635-8292-77d1429d86ae`: $-\frac{2(5{x}^{2}-4)^{3/2}}{3}+C$; operation `reverse_sign`; exact expression without C `-2*(5*x**2 - 4)**(3/2)/3`.
- Incorrect `836b0c8d-6627-5e01-a339-6971dc4ede71`: $3(5{x}^{2}-4)^{2/3}+C$; operation `historical_reciprocal_successor_coefficient_reciprocal_exponent_plus_one`; exact expression without C `3*(5*x**2 - 4)**(2/3)`.
- Incorrect `b431a516-679a-55de-bc9a-2dca5dba0032`: $\frac{3(5{x}^{2}-4)^{2/3}}{2}+C$; operation `reciprocal_successor_multiply_by_successor`; exact expression without C `3*(5*x**2 - 4)**(2/3)/2`.

### q-72382 / observed_72382

Parameters: `{"a": 1, "m": 5, "b": 1, "n": 0}`; field `selection`, math radio.

- Incorrect `181818f9-ee5d-570b-8805-3453bec6da26`: $2\sqrt{(1+{x}^{5})^{3}}+C$; operation `use_positive_integrand_power_successor`; exact expression without C `2*(x**5 + 1)**(3/2)`.
- Correct `324b72d3-41e0-5026-af58-5b34dc0551ad`: $2\sqrt{1+{x}^{5}}+C$; operation `power_rule`; exact expression without C `2*sqrt(x**5 + 1)`.
- Incorrect `601c5f25-3385-59f3-b9ec-6f4783410687`: $\frac{\sqrt{1+{x}^{5}}}{2}+C$; operation `multiply_by_successor`; exact expression without C `sqrt(x**5 + 1)/2`.
- Incorrect `d13e9d9a-a682-5a93-b274-9657dd12c702`: $2x\sqrt{1+{x}^{5}}+C$; operation `retain_x`; exact expression without C `2*x*sqrt(x**5 + 1)`.
- Incorrect `e2d6ab9a-d942-55d2-8674-766bbfa15318`: $\frac{\sqrt{(1+{x}^{5})^{3}}}{2}+C$; operation `positive_integrand_power_and_multiply_by_half`; exact expression without C `(x**5 + 1)**(3/2)/2`.

## 4. Reusable templates, slots and constraints

Source prose is fixed and reused verbatim: note the derivative, make the substitution, show derivative/differential, rewrite integral, use power rule, lastly substitute and conclude. Every concrete solution is independent of any selected answer. Easy has two rewrite rows and one primitive row; moderate three rewrite rows and two primitive rows; hard four rewrite rows and three primitive rows. Source replay preserves each complete sentence, row, notation and aligned/display distinction byte for byte.

Slots (normal extensions, not claims about source authoring): a integer 1..5; m integer 2..6; b integer −6..6 including zero; easy n integer 2..12. Root levels use sentinel n=0 and fixed q=±1/2. Positive a preserves derivative recognition and familiar monomial coefficient am≤30. Signed b is already observed at moderate and requires no new step. Inner m variations require the same monomial derivative and substitution; the largest observed m is six. Easy exponent upper bound twelve is observed; lower bound two retains nontrivial successor/divisor arithmetic. Explicit parameters enforce exactly the same bounds as samplers. Zero shifts omit the inactive term while retaining the same nonlinear monomial and derivative; no constant-factor adjustment is introduced.

Dependent components: prompt inner and multiplier, all prose substitutions, both sides of differential row, all integrands, fractional exponent conversion, power successor/divisor, back substitution, final conclusion and every answer. Root and reciprocal-root domain is F>0 on any connected open real interval. This resolves root-of-cube equivalence without allowing complex branches. Easy domain is all real x. No n=−1/logarithm exception, nested functions, parts, definite endpoints or derivative mismatch.

Default family is selected before its complete authored profile and parameters. Easy defaults serve both prompt layouts; moderate defaults serve both source multiplication layouts. For easy the authored bank contains power-rule primitive, omitted successor, multiply by successor, retain derivative, reverse sign. Moderate contains primitive, multiply by successor, omit successor, retain derivative, reverse sign. Hard contains primitive, multiply by successor, drop negative-power sign, retain derivative, reverse sign. These are complete banks, not a pool. Any derivative-equivalent pair rejects the whole instance; no option is replaced independently. Incorrect retained-derivative factors use a visible dot when two numeric factors would otherwise concatenate.

Historical banks remain public through generate(..., profile=...). Their evidence-only flags are explicit. The opaque q-2189 denominator m−1 and lowered-multiplier-power operations reproduce its original entire bank but are not treated as discovered pedagogy. q-2390's coefficient 1/q+1 and reciprocal successor have the same explicit restriction. No malformed raw values or ambiguous antiderivatives were found, so no repaired-source mode is necessary.

Meaningful parameter domains: 5×5×13×11 = 3575 easy parameter tasks; each square-root level 5×5×13 = 325. Prompt-layout/profile aliases and option order do not count as tasks. Actual sampled slot coverage and distinct mathematical fingerprints are reported in validation.json. Presentation identities include level, rendered prompt, fixed solution and complete bank. Mathematical fingerprints omit bank and source profile.
