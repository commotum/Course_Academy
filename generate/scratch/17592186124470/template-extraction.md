# Four-stage extraction

## 1. Describe each observed question

All prompts ask for the symbolic full derivative d/dt[f(r(t))], with exactly three coordinates in i,j,k notation. The supplied six solutions share the chain-rule statement, formal held-coordinate gradient operators, evaluated gradient, prose coordinate substitutions, composed gradient, three ordered d/dt(argument) operators, curve derivative, vector dot product, distribution and reduction. Templates preserve the full original sentences, row count and source-specific intermediate rows, including omitted redundant zero distribution terms. Source blanks, pictures and feedback do not occur.

- **pair_products**, q-36238: $f=x y + x z + y z$, $r=(t, e^{t}, e)$. Domain: all real t. A constant coordinate makes one curve derivative zero; the zero component is retained before source reduction.
- **trig_product**, q-95075: $f=z \left(x + y\right)$, $r=(\sin{\left(t \right)}, \cos{\left(t \right)}, e^{t})$. Domain: all real t. Three-coordinate symbolic vector chain rule with the displayed function forms.
- **constant_coordinate**, q-167453: $f=x y^{2} + y z^{3}$, $r=(t^{3}, 1, t)$. Domain: all real t. A constant coordinate makes one curve derivative zero; the zero component is retained before source reduction.
- **quartic_trig**, q-95070: $f=x^{4} - y^{4} - \cos{\left(z \right)}$, $r=(\sin{\left(t \right)}, \cos{\left(t \right)}, 2 t)$. Domain: all real t. Additional trig manipulation rows: quartic gradient, sine/cosine identity, double-angle reduction.
- **log_product**, q-95072: $f=\ln{\left(x y z \right)}$, $r=(t, e^{t - 1}, e^{t})$. Domain: t+h>0. Three-coordinate symbolic vector chain rule with the displayed function forms.
- **log_difference**, q-95142: $f=x \left(y^{2} - z^{2}\right)$, $r=(\ln{\left(t \right)}, t + 1, t - 1)$. Domain: t+h>0. Three-coordinate symbolic vector chain rule with the displayed function forms.
- **exponential_cosine**, q-95146: $f=y z \cos{\left(x \right)}$, $r=(t^{2}, e^{t}, e^{t})$. Domain: all real t. Three-coordinate symbolic vector chain rule with the displayed function forms.
- **log_exp**, q-95149: $f=e^{y} + \ln{\left(x z \right)}$, $r=(\sin{\left(t \right)}, t^{2}, \frac{1}{t})$. Domain: t+h != 0 and sin(t+h)/(t+h)>0. Three-coordinate symbolic vector chain rule with the displayed function forms.

## 2. Generalize the assessed pattern

Compute the three-coordinate gradient while holding the other coordinates fixed; substitute the complete curve components (including products such as xy), differentiate each curve coordinate with respect to the original independent variable t, form the dot product, distribute and reduce. The learner supplies one scalar expression via one five-choice radio field. A single fixed solution is independent of the chosen error. Authored missing solutions use the entire common formal sequence and all zero contributions.

## 3. Map every complete source bank

For each row below B(t) is the **complete displayed scalar expression pattern**, not a guessed misconception. The parameterized observed recipe is c·B(t+h), where the prompt is c·f(x,y,z) along r(t+h). This follows derivative linearity and time translation. All five expressions are selected together before parameters. There is insufficient evidence to infer the original distractor authoring algorithm for several options; these banks remain explicit observed profiles rather than normal defaults. They are not arbitrary fitted polynomials. The correct expression is derived from the prompt and uniquely located by exact mathematics; no answer table selects it.

### pair_products: one complete observed bank (q-36238)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `e^{t + 1} + te^{t} + e` | c·B(t+h) | absent; independently derived in replay |
| 2 | `e^{t + 1} + (1 + 2t)e^{t} + e` | c·B(t+h) | absent; independently derived in replay |
| 3 | `e^{t + 1} + (1 + t)e^{t} + e` | c·B(t+h) | absent; independently derived in replay |
| 4 | `2e^{t} + 2e + t` | c·B(t+h) | absent; independently derived in replay |
| 5 | `e^{t + 1} + (t + 1)e^{t} + 2` | c·B(t+h) | absent; independently derived in replay |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### trig_product: one complete observed bank (q-95075)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `2e^{t}\sin t` | c·B(t+h) | absent; independently derived in replay |
| 2 | `2e^{t} + \sin t + \cos t` | c·B(t+h) | absent; independently derived in replay |
| 3 | `0` | c·B(t+h) | absent; independently derived in replay |
| 4 | `2e^{t}(\sin t + \cos t)` | c·B(t+h) | absent; independently derived in replay |
| 5 | `2e^{t}\cos t` | c·B(t+h) | absent; independently derived in replay |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### constant_coordinate: one complete observed bank (q-167453)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `3{t}^{2}+3t` | c·B(t+h) | wrong |
| 2 | `{t}^{2}+2t` | c·B(t+h) | wrong |
| 3 | `6{t}^{2}` | c·B(t+h) | correct |
| 4 | `3{t}^{2}` | c·B(t+h) | wrong |
| 5 | `{t}^{3}+3{t}^{2}` | c·B(t+h) | wrong |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### quartic_trig: one complete observed bank (q-95070)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `4\operatorname{sin}⁡2t` | c·B(t+h) | correct |
| 2 | `\operatorname{sin}⁡2t{cos}^{3}⁡2t` | c·B(t+h) | wrong |
| 3 | `\operatorname{cos}⁡t{sin}^{3}⁡t` | c·B(t+h) | wrong |
| 4 | `0` | c·B(t+h) | wrong |
| 5 | `{cos}^{2}⁡t` | c·B(t+h) | wrong |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### log_product: one complete observed bank (q-95072)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `\frac{2t{e}^{t}+1}{t}` | c·B(t+h) | wrong |
| 2 | `\frac{{e}^{t}+1}{t}` | c·B(t+h) | wrong |
| 3 | `2{e}^{t-1}(1-t)` | c·B(t+h) | wrong |
| 4 | `\frac{2t+1}{t}` | c·B(t+h) | correct |
| 5 | `3` | c·B(t+h) | wrong |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### log_difference: one complete observed bank (q-95142)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `4t(t-\operatorname{ln}⁡t)` | c·B(t+h) | wrong |
| 2 | `4+4t+{t}^{2}\operatorname{ln}⁡t` | c·B(t+h) | wrong |
| 3 | `4(t-\operatorname{ln}⁡t)` | c·B(t+h) | wrong |
| 4 | `4t(t-1)` | c·B(t+h) | wrong |
| 5 | `4(\operatorname{ln}⁡t+1)` | c·B(t+h) | correct |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### exponential_cosine: one complete observed bank (q-95146)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `{e}^{2t}\operatorname{cos}⁡t` | c·B(t+h) | wrong |
| 2 | `2{e}^{2t}` | c·B(t+h) | wrong |
| 3 | `{e}^{2t}(\operatorname{sin}⁡t-\operatorname{cos}⁡t)` | c·B(t+h) | wrong |
| 4 | `{e}^{2t}(2\operatorname{cos}⁡{t}^{2}-\operatorname{sin}⁡{t}^{2})` | c·B(t+h) | wrong |
| 5 | `2{e}^{2t}(\operatorname{cos}⁡{t}^{2}-t\operatorname{sin}⁡{t}^{2})` | c·B(t+h) | correct |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.

### log_exp: one complete observed bank (q-95149)

| Source option | Exact raw expression B(t) | Formula for varying c,h | Source designation |
|---|---|---|---|
| 1 | `\operatorname{csc}⁡t+{e}^{{t}^{2}}+t` | c·B(t+h) | wrong |
| 2 | `\operatorname{csc}⁡t+2t{e}^{{t}^{2}}` | c·B(t+h) | wrong |
| 3 | `\operatorname{cot}⁡t+2t{e}^{{t}^{2}}-\frac{1}{t}` | c·B(t+h) | correct |
| 4 | `\operatorname{cot}⁡t+{e}^{{t}^{2}}-1` | c·B(t+h) | wrong |
| 5 | `\operatorname{tan}⁡t+\frac{{e}^{{t}^{2}}}{{t}^{2}}` | c·B(t+h) | wrong |

Every source value remains byte-exact at c=1,h=0. Original choice order is incidental; each source option matches one unique generated value.


Authored complete operation banks compute the correct derivative first and then the full required wrong-operation set. `omit_chain`: omit each of the x/y/z products, plus use r rather than r′. `sign_chain`: negate one product at a time, plus sum gradient components without the dot weights. `constant_active` omits x, omits the factor 3 in d/dt[(t+h)^3], uses the undifferentiated curve, and sums the gradient. A bank omitting x and z separately is excluded because those omissions coincide. `xy_active` does the analogous x/y omissions for constant z. `log_rates` omits one exponential contribution, both exponential contributions, reverses the x contribution, and uses the undifferentiated curve. `paired_exp` omits the x contribution, omits both exponential contributions, uses gradient-x without its inner derivative, and sums the gradient. Exact formulas appear in OP_BANKS/bank_values; each complete bank is checked for pairwise equivalence. ELIGIBLE restricts special operations to the applicable source family; impossible profiles fail before sampling. No member is replaced from a candidate pool, and an explicit collision rejects the whole instance.

## 4. Extract reusable complete-component masks

The source's entire f RHS, each gradient vector component, each composed gradient component, each ordered derivative argument, each curve-derivative component, both complete dot vectors and each scalar distribution/reduction row are complete slots. Fixed prose, labels, i/j/k basis symbols, independent-variable derivative operators and original row separators remain fixed. The c slot multiplies f and all gradient/dot-scalar contributions; the h slot translates only mathematical curve-coordinate expressions and prose substitutions. Command names, including operatorname{cot}, remain protected; their mathematical arguments remain substitutable. Compact source ti/tj/te are handled as known implicit products within these slots.

Source parameter values: c=1,h=0. Authored bounds in **both** random samplers and explicit inputs: moderate c∈{-3,-2,-1,1,2,3}, hard c∈{-4,-3,-2,-1,1,2,3,4}, h∈{-2,-1,0,1,2}. Easy a,b,d∈{-3,-2,-1,1,2,3}, n∈{1,2}; coefficients are nonzero. Time translation preserves every original degree/function workload and domains become conditions on t+h. The domain is mathematically derived per family, never an evaluation point. Samplers reject entire ambiguous banks; bounds cannot be bypassed by observed profiles.

At most 30 coefficient/shift instances per moderate family, 40 per hard family, and 432 easy candidate parameter combinations before ambiguity rejection. These are finite catalogs, not claims of unlimited variety; mathematical fingerprints canonicalize equivalent f expressions and curve coordinates and exclude seed, option order, profile and bank. The actual printed prompt, fixed solution, complete bank, correct value, domain and version determine separate content identity.

No plots require extraction or generation (steps 5 and 7 rating none). Work stops before database preparation.

## Raw absence versus authored completion

`observed_raw` preserves the two originals' missing difficulty, worked-solution and correct-ref attributes. Its content identity includes those absences; it does not identify the raw record with its completion. `observed_pattern` supplies independently derived correct refs, full common solutions and explicitly authored moderate labels. Both observed expression-pattern profiles carry evidence_only=true and eligible_for_learning=false. Authored default operation banks carry the opposite flags. Native grading excludes raw fixtures without a key and grades their separate completed fixtures.

For q-36238, ∇f=(y+z,x+z,x+y) and r′=(1,eᵗ,0), yielding eᵗ+e+(t+e)eᵗ=e^(t+1)+(1+t)eᵗ+e (source option 3). For q-95075, ∇f=(z,z,x+y) and r′=(cos t,−sin t,eᵗ), yielding eᵗ cos t−eᵗ sin t+eᵗ(sin t+cos t)=2eᵗ cos t (source option 5). These derivations establish mathematical keys, not missing original designations. The authoritative captured lesson widget (MA/DATA/Lessons/1936/Source/1936.json) confirms both original five-choice layouts but supplies no captured correct key or worked solution.

## Conditional trigonometric argument-power mask

In the exponential_cosine source, `sin⁡{t}^{2}` and `cos⁡{t}^{2}` have the inner argument t², while the quartic source's `{sin}^{3}⁡t` has function power 3. When h changes, the inner-power mask becomes explicitly `sin⁡({(t+h)}^{2})`/`cos⁡({(t+h)}^{2})` before translation; the outer visible parentheses contain the entire powered argument. It must never become `sin⁡{(t+h)}^{2}`, which displays a power of the function value. This conditional mask applies uniformly to composed gradients, both dot vectors, scalar rows and observed choices. All h=0 source bytes remain unchanged. The parser and independent display tests distinguish inner powers, pre-argument function powers and powers following visibly parenthesized arguments; a mutation restoring the former ambiguous shifted spelling fails the composed-gradient mathematics check.
