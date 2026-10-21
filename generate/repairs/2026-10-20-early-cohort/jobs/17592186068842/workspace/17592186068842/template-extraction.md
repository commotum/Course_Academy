# Template extraction

## 1. Specific observed descriptions

The ten original prompts, complete choice banks, worked solutions, field types, and exact shapes appear in `source.json` and the Original replay sections of `review.md`. The source parameter map is in `source-cases.json`. Every displayed answer is a complete differential equation, never an isolated side.

| Template/source | Observed RHS and parameters | Source-specific workload/stages |
|---|---|---|
| rational_product / q-154678 | xy²/(x+1); n=2,a=1 | Explicit rational x factor times y²; final divide by y² |
| exp_product / q-158022 | ye^x; a=1 | Reorder product; divide by y |
| exp_quotient / q-158025 | 2^x/y³; base=2,a=1,n=3 | Write reciprocal y factor; multiply by y³ |
| sqrt_quotient / q-158026 | sqrt(1+y²)/x; a=1,n=2 | Write 1/x factor; divide by complete square root |
| trig_product / q-158027 | y² sin x; a=1,n=2 | Reorder product; divide by y² |
| simple_quotient / q-158030 | x/y; n=1 | Write reciprocal y factor; multiply by y |
| exp_sum / q-157692 | e^(x+y); a=b=1 | Split summed exponent, reciprocal exponential, equivalent negative-exponent final row |
| polynomial_factor / q-158023 | x+xy²; a=b=1,n=2 | Extract common x; divide by complete polynomial y factor |
| base_exp / q-158024 | 3^(x−2y); base=3,a=1,b=2 | Split subtracted exponent; transfer negative y exponent |
| rational_factor / q-158032 | 3x/(5xy+y); a=3,b=5,c=1 | Factor denominator, show two-row factorization, multiply by y |

All solutions begin with the same two separability/separation definitions, then “Notice that…” followed by factorization, and “Therefore…” followed by the separated equation. Source typography uses `\text{d}`, braces on powers, invisible function application in trig, and the typo “differentiable equation.” Observed profile preserves every character and punctuation. Standard profile changes that typo to “differential equation,” and adds the local domain instruction. No error-dependent feedback is added.

## 2. Shared generalized pattern

Identify h(x)g(y) from the displayed ODE, then produce (1/g(y))dy/dx=h(x). Easy has an already visible product/quotient. Moderate needs one common-factor extraction or exponent law first. The response must be separated as well as equivalent to the original ODE. No integration, constants of integration, initial conditions, or integrating factors are assessed.

## 3. Components and complete banks

The exact source option-to-expression map is `bank-mapping.json`: it contains every original source answer UUID/value, its indexed parameterized recipe, field key, and correct designation. `build` in the script renders those recipes from complete mathematical component masks. These formulas generalize the source expressions; labels describe algebraic operations, not a claim about author intent.

Writing D=dy/dx and O=hg, recurring source operations are: gD=h (failure to invert g); hD=g (exchange roles); (1/h)D=g (transfer x factor, equivalent but unseparated); (1/O)D=1 (divide by all of O, equivalent but unseparated); and the valid (1/g)D=h. Other banks keep their own compound expression operations: the rational-product bank clears x+a or divides by x; exponential banks negate either/both exponent components; polynomial-factor bank uses x/g instead of 1/g or multiplies by the whole O; trig bank uses csc x and puts reciprocal sin x on the RHS; rational-factor bank inverts h. Every complete observed five-option bank stays together; no pool/first-valid replacement is used.

Both profiles use these same banks. Equivalent UNSEPARATED ODEs are intentionally preserved, not source errors or numerical fits. The verifier reads the printed prompt, every printed answer, and each printed solution stage. It solves each full equation for D on its regular domain, detects nonzero-scale equivalence, and separately checks whether the coefficient of D depends only on y and the RHS only on x. Only one eligible equivalent response is permitted; all eligible responses must be distinct modulo full equation equivalence.

## 4. Reusable templates, constraints, and authored extension

Fixed prose, mathematical-component masks, optional exponential final row, and the two-row rational factorization are implemented in `build`. Coefficients a,b,c,d are positive integers 1–5, base is 2–5, and powers n are 1–4, with n restricted to {2,4} in positive-polynomial/square-root families. Every explicit input follows the same bounds. Powers and exponent scales vary the assessed transfer/factor recovery, not incidental presentation.

Hard is a design claim, not an observed label. The authored RHS ax/(bdx+bxy^n+cd+cy^n) has four substantive terms and factors into ax/((bx+c)(d+y^n)). It uses only the same independent-factor identification taught in the canonical radical example and moderate denominator factorization; it increases the number of factors to recognize, while still ending at (d+y^n)D=ax/(bx+c). Require b,c,d≥2, a≥1, n∈{2,4}; no coefficient can erase the four-term workload. This is one equal-level family with varied coefficients, not an instructional progression. Its bank is authored: multiply by g rather than its reciprocal; invert h; transfer the x factor; and divide by the x factor. These are explicit operations tied to the separation method.

Domains: divided y factors require y≠0; x denominators must be nonzero; exponential factors never vanish; positive constant plus an even y power is positive. Source trig csc choices and x-reciprocal choices have additional local exclusions. `generation.domain` records the original/separated equation restrictions; `domain-evidence.json` records every option's denominator. Normal instructions ask for a domain on which all displayed expressions are defined, without adding singular-solution assessment. The canonical example says x,y≥0 but its divided form requires y>0: the following tutorial explicitly supplies g(y)≠0, so the local-domain interpretation is supported. No source math correction or hidden branch is claimed.

Plots: none at steps 5 and 7; no rendering/assets required. Raw captures and observed replay remain unchanged. The only normal-presentation repairs are the typo and domain instruction. Distinct domain restrictions are not compared by evaluating only separate sides. Equation equivalence is evaluated on the common regular domain, with eligibility of the requested form as a separate necessary condition.
