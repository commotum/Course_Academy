# Template extraction

Basis 1356, immutable snapshot provenance retained in source.json. The implementation uses complete mathematical-component slots: every full RHS in each aligned row is reconstructed from parameters. It never replaces short coefficients globally across prose or unrelated function arguments. Source scaffolding, supplied notation, prose, row counts, and the order of differentiating/substituting/evaluating/collecting are retained. TeX normalization changes insignificant spacing, braces around x/e, sum order in CAS-rendered answer values, signs moved outside derivative operators, explicit multiplication dots, and the final arithmetic arrangement; these are not claimed as byte-exact output. Full-equation answer values are compared mathematically, with actual function labels enforced independently.

## Stage 1: Specific source descriptions

- q-11728: `f=5e^x+2x^2-3`; five whole derivative equations. Unrated, no solution or correct designation. One quadratic coefficient multiplication, one exponent reduction, and constant removal. Authored easy assignment is supported by the labeled easy quadratic slope q-140431.
- q-11730: `f=9e^x-9x^2+11x-20`; signed quadratic, linear and constant terms; five whole derivative equations. Unrated, no solution/correct ref. Authored moderate assignment is supported by the nearly identical labeled moderate q-17255.
- q-167636: `k=g-f`, with `A=2,B=3` and definitions inferred explicitly from its combination row: `f=x^3+Ax`, `g=Be^x`. Easy blank derivative RHS. The prompt omits the earlier definitions; solution references steps 3 and 4. Three combination rows, then four derivative rows. The second derivative row misses a closing parenthesis and nests subsequent derivatives incorrectly.
- q-167694: on `x<1`, the preceding piece is `f=e^x+x^2+x`, stated in source solution but absent from prompt. Moderate blank derivative RHS. Three derivative rows, no evaluation or branch continuity test.
- q-140431: `f=2e^x+4x^2-3` at `x=1`; easy five-choice exact slope. Four derivative rows, three slope substitution/evaluation rows. Constant derivative is explicitly +0 after coefficient extraction.
- q-140432: `f=x^2+2x+6e^x` at zero; polynomial-first order; easy five-choice exact slope. Four derivative rows, four slope rows; explicit `2+6*1` before collection.
- q-17247: `f=2e^x-3x^2` at zero; easy five-choice exact slope. Five derivative rows include `-3(2x)`, then four slope rows include `2*1-0`.
- q-17255: `f=11e^x+8x^2-12x-20` at zero; moderate five-choice exact slope. Five derivative rows include all held constant/linear contributions; five slope rows include `11*1+0-12`, then `11-12`, then -1.
- q-304035: `f=6x^7+2e^x` at -1; easy exact scalar blank. Five polynomial-first derivative rows, four slope rows preserve `42(-1)^6+2e^-1`, then `42*1+2/e`. Its two-value blank bank contains both the correct scalar and an unevaluated derivative; the latter remains a legacy evidence value, never an alternate correct answer.

## Stage 2: Shared pattern and purpose

Differentiate each sum term independently. A constant multiple of e^x retains its coefficient and exponential; a polynomial monomial `cx^n` becomes `cnx^(n-1)`; a constant becomes zero. Slope families then substitute a familiar input (0, 1 or -1), preserving exact e values. A blank requesting a derivative expects only the RHS; a slope blank expects only the evaluated scalar. Whole-equation radio fields preserve the actual named function.

The three contextual/application forms are parallel uses of this same method. Piecewise branch selection does not expand to endpoints, continuity, or differentiability of a join. Difference assembly is only subtraction of the given explicit functions. There is no product rule for nonconstant factors, chain rule, logarithmic derivative, or non-e base.

## Stage 3: Components and complete banks

Let `a` be the exponential coefficient, `b` the leading polynomial coefficient, `c` the linear coefficient, `d` the constant, `F` the given function, `P` its polynomial, and `V` the true derivative/slope as appropriate. Every complete observed bank includes V; the remaining displayed values follow the formulas below. Their interpretations are hypotheses, not recovered source authoring code.

| Profile | Complete wrong-value formulas (alongside V) |
|---|---|
| observed_direct_quadratic | `ae^x+2bx^2+d`, `ae^x+2bx^2`, `V+d`, `e^x+2bx` |
| observed_direct_extended | `e^x+2bx+c`, `ae^x+2bx^2+cx`, `ae^x+2bx^2+c`, `ae^x+2bx^2+cx+d` |
| observed_slope_quad, input t=1 | `e^t+bt`, `e^t+2bt`, `ae^t`, `ae^t+bt` |
| observed_slope_polyfirst, input 0 | `(c+a)e`, `c+ae`, `b+ae`, `ae` |
| observed_slope_zero, input 0 | `ae+2b`, `1`, `(a+2b)e`, `0` |
| observed_slope_extended, input 0 | `0`, `a+c/2`, `c/4`, `-V` |
| observed_difference | blank V only |
| observed_branch | blank V only |
| observed_slope_seventh | blank V plus legacy `F'(x)` value |

In q-17255, values 0, 5, -3, 1 do not uniquely determine error mechanisms. The explicit coefficient patterns reproduce the complete captured bank (`a+c/2=5`, `c/4=-3`, `-V=1`) but their intentions remain unresolved. They are confined to a named **observed profile**; no arbitrary polynomial fit or default learner-error claim is made. Source q-17247's constants 0 and 1 correspond to dropping the exponential and dropping its coefficient; the remaining options combine wrong input/coefficient operations, rather than random numerical offsets.

Default radio banks are separately authored complete method banks. Direct questions use V, omitted exponential derivative, multiplied polynomial coefficients without lowering powers, reversed polynomial derivative signs, and original F. Slope questions use V, omitted exponential derivative, derivative evaluated at the wrong familiar input (1 for true 0, otherwise 0), original function value, and lost exponential scale. For slope_zero the function-value recipe is explicitly evaluated at 1 to avoid the necessarily correct original F(0)=a. The bank is selected before sampling; any correct/duplicate wrong member rejects the whole instance. No pooled fallback option substitutions occur. Blank defaults contain one correct fragment.

The following per-source table accounts one-to-one for **every** captured field value. Radio designation matches use the seven supplied refs; the two absent refs are independent mathematical inferences and are not included in that denominator.

### q-11728 / observed_direct_quadratic

Parameters: `{"a": 5, "b": 2, "d": -3, "name": "f"}`. Field `selection`, `radio`.

- `correct`: $4 x + 5 {e}^{x}$
- `retain_exponent_constant`: $4 x^{2} + 5 {e}^{x} - 3$
- `retain_exponent`: $4 x^{2} + 5 {e}^{x}$
- `retain_constant`: $4 x + 5 {e}^{x} - 3$
- `omit_exponential_coefficient`: $4 x + {e}^{x}$

### q-167636 / observed_difference

Parameters: `{"A": 2, "B": 3, "name": "k"}`. Field `field-1`, `blank`.

- `correct_fragment`: $- 3 x^{2} + 3 {e}^{x} - 2$

### q-140431 / observed_slope_quad

Parameters: `{"a": 2, "b": 4, "d": -3, "name": "f", "t": 1}`. Field `selection`, `radio`.

- `correct`: $2 e + 8$
- `omit_exp_scale_power_factor`: $e + 4$
- `omit_exp_scale`: $e + 8$
- `omit_polynomial_derivative`: $2 e$
- `omit_power_factor`: $4 + 2 e$

### q-140432 / observed_slope_polyfirst

Parameters: `{"a": 6, "b": 1, "c": 2, "name": "f", "t": 0}`. Field `selection`, `radio`.

- `correct`: $8$
- `multiply_linear_and_exp_by_e`: $8 e$
- `evaluate_exp_at_one`: $2 + 6 e$
- `treat_linear_as_quadratic_scale`: $1 + 6 e$
- `omit_linear_evaluate_at_one`: $6 e$

### q-17247 / observed_slope_zero

Parameters: `{"a": 2, "b": -3, "name": "f", "t": 0}`. Field `selection`, `radio`.

- `correct`: $2$
- `evaluate_at_one`: $-6 + 2 e$
- `unit_exp_omit_polynomial`: $1$
- `merge_coefficients_times_e`: $- 4 e$
- `omit_exp_evaluate_zero`: $0$

### q-304035 / observed_slope_seventh

Parameters: `{"a": 2, "b": 6, "n": 7, "name": "f", "t": -1}`. Field `field-1`, `blank`.

- `correct_fragment`: $\frac{2}{e} + 42$
- `legacy_unevaluated_derivative`: $42 x^{6} + 2 {e}^{x}$

### q-11730 / observed_direct_extended

Parameters: `{"a": 9, "b": -9, "c": 11, "d": -20, "name": "f"}`. Field `selection`, `radio`.

- `correct`: $- 18 x + 9 {e}^{x} + 11$
- `omit_exponential_coefficient`: $- 18 x + {e}^{x} + 11$
- `retain_both_powers`: $- 18 x^{2} + 11 x + 9 {e}^{x}$
- `retain_quadratic_power`: $- 18 x^{2} + 9 {e}^{x} + 11$
- `retain_powers_constant`: $- 18 x^{2} + 11 x + 9 {e}^{x} - 20$

### q-167694 / observed_branch

Parameters: `{"a": 1, "b": 1, "c": 1, "h": 1, "name": "f"}`. Field `field-1`, `blank`.

- `correct_fragment`: $2 x + {e}^{x} + 1$

### q-17255 / observed_slope_extended

Parameters: `{"a": 11, "b": 8, "c": -12, "d": -20, "name": "f", "t": 0}`. Field `selection`, `radio`.

- `correct`: $-1$
- `observed_zero`: $0$
- `observed_half_linear`: $5$
- `observed_quarter_linear`: $-3$
- `observed_negated_result`: $1$

## Stage 4: Reusable templates, domains, and repairs

Easy templates keep their source structures. Coefficients a/b/c are nonzero signed integers with absolute value at most 9; samplers use magnitudes at most 7 and a nonunit exponential coefficient for authored radio eligibility. Constants d have magnitude at most 20. Difference uses A,B in 1..9 and fixed name k. Slope inputs are fixed to original 0 or 1. The polynomial-first reciprocal-e slope uses positive a,b (a 2..7 in sampling, positive up to 9 accepted), degree n in {3,5,7}, fixed input -1: the derivative exponent is even, so evaluating the power stays trivial. This reproduces the observed seventh-degree example without negative powers or fractional coefficient arithmetic.

Moderate direct/slope templates have a quadratic, a nonzero linear term, and a nonzero constant. Branch templates have an exponential, a quadratic, and a nonzero linear term with threshold h in -3..3; h is incidental to mathematical task identity. Moderate coefficient bounds have absolute value at most 12 (source includes 11/-12); sampling uses at most 7. All explicit parameters receive the same workload/domain guards as samples.

Authored hard: `ae^x+bx^n+cx^m`, three nonzero coefficients with magnitude at most 7; `3<=n<=7`, `2<=m<=3`, `n>m`. Sampling uses n=4..7 and m=2 or 3. Both polynomial components require actual coefficient multiplication and exponent reduction, before any cancellation; distinct powers prevent collapse. The template retains the common addition/power-rule prose and complete formal derivative, term separation, constant extraction, rule substitution, and reduction stages. Function names f/g/h vary consistently. This is an authored missing-level design, not recovered hard difficulty evidence.

Original source profiles retain the actual original function name, original type/choice count/response shape, whole bank, and fixed worked solution structure. Invalid bank instances fail rather than silently changing coefficients/options. Component signs are rendered through a signed-term join; no bare -- or +- occurs. Expressions e^x keep course exponential notation; no hyperbolic rewrite is possible.

Repairs and fidelity denominators:

1. q-11728 and q-11730: their missing correct refs are inferred by differentiating the actual displayed functions; independent local MA1114 JSON/Markdown also have no marked correct choice. Authored solution scaffolding follows the common canonical addition/power stages. Source difficulty assignments easy/moderate are documented above, not labeled observed.
2. q-167636: preserve raw malformed text in source.json/review. Repair the second derivative row to `D(Be^x)-D(x^3)-D(Ax)`, retaining the same three terms and row position. The preamble's source y label stays in observed replay; standalone default changes it to k(x). Its missing definitions are supplied in normal prompts, and the unsupported reference to earlier steps is replaced with “Using the given definitions, we have”. Exact malformed-row fidelity is not claimed.
3. q-167694: normal prompts state the branch expression; observed prompts retain the short contextual form. No endpoint or second-branch claims are authored.
4. q-304035: preserve both captured bank values in the public observed profile; native grading rejects the derivative-expression submission and accepts the correct scalar and unreduced equivalent. Default uses one scalar bank entry.
5. q-17255: observed scalar formulas are limited-evidence patterns, not inferred intentions. Default uses the method bank above.

Validation separates 9/9 complete original banks (34/34 values), 7/7 supplied correct designations plus two inferences, source prose/ordered-stage checks (six mathematically well-formed sequences and one supported repaired sequence), and exact-string notation fidelity. The validation report gives exact prompt/solution string counts honestly. Source originals are preserved in full in review rather than silently excluded or declared mathematically valid when malformed.

No plots exist in any source prompt, bank, or solution, so plot extraction/specification is not applicable. No renderer is required. Freeze follows review and native validation; work stops after step 7.
