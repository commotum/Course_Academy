# Template extraction

Current inventory classification and durable preparation/commit are documented in [reference/current-classification.md](reference/current-classification.md). The basis-1356 analysis below remains historical source evidence.

## 1. Specific source descriptions

The raw descriptions, prompts, every original choice, and complete available worked solutions are preserved in `source.json`, and shown beside parameterized replays in `review.md`. The classification table names all six sources without merging their field layouts or mathematical stage sequences. Every bank has five delimiter-free scalar expressions in t. Source exponent typography (`{e}^{t}`, `{sin}^{2}⁡t`), Unicode gradient/prime/function-application characters, spacing and original shared prose are retained in observed profiles.

q-36211 uses two squared exponential coordinates and a negative exponential derivative, with one gradient substitution row and two final scalar rows. q-37099 has a mixed product xy², one logarithmic coordinate and a scaled quadratic coordinate; its last scalar row contains three additive contributions. q-95052 has a trig function of x, linear πt coordinate and exponential y coordinate; its last block distributes the dot product and factors eᵗ. q-95054 retains two unreduced logarithmic partial fractions before gradient reduction, two gradient substitution rows, a multiplication row, a collected constant/rational row and a factored rational row. q-95059 retains separate rational dot-product contributions before combining the shared denominator. q-95056 is an unrated source with no worked solution/designation; ln xy is interpreted as ln(xy), as required by the independently derived matching bank expression.

## 2. Shared pattern

Given an explicit scalar f(x,y) and an explicit two-component r(t), compute the complete symbolic derivative by ∇f(r(t))·r′(t). The gradient must be evaluated at the actual composed coordinates before taking the dot product. The source asks for one final scalar, with one fixed complete worked solution independent of chosen error. Five radio options are retained; there are no blanks, so blank-fragment native grading is inapplicable.

## 3. Components and complete choice-bank mapping

Each observed profile is a whole five-expression pattern, never a pool or arbitrary numerical perturbation. Parameters below use the same names as the script. Original parameters are in `source-cases.json`. `bank-extraction.json` maps each original owned answer ID/value one-to-one to its computed symbolic expression, original index and correctness status. Source exact-value pattern reproduction is distinct from inferred error intent.

- **square_exp**, f=a x²+b y², r=(e^(kt),e^(−kt)): bank, in original order, is 2ak e^(2kt)+2bk e^(−2kt); 2k(a+b)e^(2kt); 2ak e^(2kt)−2bk e^(−2kt); 2ak e^(kt)−2bk e^(−kt); a e^(2kt)+b e^(−2kt). The third is correct. The sign-loss and exponent-loss interpretations are supported expression patterns; the second and fifth intent remains underdetermined.
- **log_cos**, f=ln(x y^a), r=(cos kt,t^n): (an t+1)/t²; (an−kt tan kt)/t; (k t² tan kt+an)/t²; (an−kt sec kt)/t; (k t² sec kt+1)/t². The second is independently correct. The +1 constants are part of the observed pattern and their underlying intent is unresolved; no original designation exists.
- **polylog**, f=a x−b x y², r=(ln t,c t^n): a+bc²t^(2n−1)+2bc t^(2n−1)ln t; a/t−bc t^(n−1)−bc t^(n−1)ln t; a/t−bc t^n+2bc²n t^(2n−1); a/t−bc²t^n−2bcn t^n ln t; a/t−bc²t^(2n−1)−2bc²n t^(2n−1)ln t. The fifth is correct. Compound coefficient/power alterations are explicit observed expression patterns with unresolved cognitive intent.
- **cos_exp**, f=a y cos x, r=(kt,e^(lt)): al e^(lt)cos kt−a sin kt; a e^(lt)(l cos kt−k sin kt); al cos kt−a e^(lt)sin kt; kt+a e^(lt)cos kt; kt−a e^(lt)sin kt. The second is correct. Missing multiplier/product patterns are explicit; linear-coordinate replacement intent is unresolved.
- **log_power**, f=ln(x y^a), r=(t^(−n),e^(kt)): (a+n−1)(t²+1)/t; (t^n e^(kt)+a)/e^(kt); ak−n/t; t(t−n); a(t e^(kt)−1)/e^(kt). The third is correct. All four wrong patterns reproduce exactly, but the original scalar values do not uniquely determine error operations. They are retained as explicit observed profiles rather than used as authored defaults.
- **atan_product**, f=arctan(a xy), r=(e^(kt),sin lt); D=1+a²e^(2kt)sin²lt: a e^(kt)(l cos lt+k)/D; a(sin lt+e^(kt))/D; a e^(kt)(k sin lt+l cos lt)/D; a e^(kt)(k sin lt+l)/D; a(e^(kt)−cos lt)/D. The third is correct. Omitted factors and replaced coordinate derivatives are hypotheses, not recovered authoring code.

Normal authored banks are five fixed operations chosen together before parameters: correct g·r′; omit the second product; negate the second product; omit both coordinate derivatives (g_x+g_y); swap coordinate derivatives. If any complete-bank members are equivalent or an incorrect member equals the answer, the whole instance is rejected. Explicit inputs fail rather than silently resampling. This bank is labeled authored and never counted as the original bank.

## 4. Reusable template

The script's `build` creates formal partial-operator rows, unreduced/reduced gradient components, actual coordinate substitutions, both formal coordinate derivative operators, evaluated derivatives, formal vector chain rule, evaluated vector dot product, and the source-specific ordered scalar rows. `render` uses complete mathematical components; substitution prose is filled from the same coordinates. For the five observed solutions, the captured prose is a reusable skeleton whose five full display blocks are slots: no raw-payload-return branch or answer lookup exists. Source replay runs through the same `generate` API, exact calculations and validity checks as new parameters. Conditional coefficient-one omission, exponent-one omission, pi command spacing, and log/atan argument grouping preserve unambiguous display.

Content identity hashes version, displayed prompt, fixed worked solution, owned bank, correct value and field layout; it excludes option order/seed/profile aliases. Mathematical fingerprints canonicalize f and the two parameterized coordinates and exclude the bank/profile. Variable names are fixed by this source. Radio options are shuffled deterministically after correct identity is fixed. All explicit inputs pass normal level/profile guards.

No plot extraction or renderer is required: no relevant asset exists in any source or authored template. Work stops after step 7, with no EDB transaction or registration.

The public `raw_observed` anomaly profile replays the complete q-95056 bank and prompt without adding the absent source difficulty/solution/designation. `source-cases.json` uses that profile for the anomalous source. The separately completed `observed` profile is mathematically validated and native graded but its authored attributes never count as original designation/solution fidelity. Both use the same parameterized formulas.
