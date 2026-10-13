# Template extraction

## 1. Specific observations

Each source is retained with its complete exact strings in source.json; source-cases.json assigns all seven to a normal generator replay, and masks.json records the extracted components. All independent variables are x, all exponential exponents are x, every coefficient/base/constant is an exact integer. Learner-facing radio answers in the two unrated sources include `f′(x)=`; q-11735 radio answers are derivative RHS fragments. Blanks retain their original field key and supplied f′ notation. No added distractor diagnosis is presented.

| Source | Original expression; task | Shape and ordered solution |
|---|---|---|
| q-11732 | 5·2^x; derivative | radio, 4 equations; solution absent |
| q-1917 | 4^x+3e^x; derivative | radio, 5 equations; solution absent |
| q-11735 | 6^x−5x²+6x−19; derivative | radio, 5 RHS fragments; formal derivative → sum operators → coefficient extraction → formula/power substitution → collection |
| q-17388 | 3^x+5e^x; rate at zero | radio, 5 scalars; 4 derivative rows then 4 evaluation rows |
| q-304038 | 3·8^x+12x+10; derivative | blank field-1, 1 RHS; 5 derivative rows |
| q-340272 | 7−2·8^x; derivative | blank field-1, 2 equivalent RHS aliases; 5 derivative rows with constant first |
| q-340280 | 5^x−6x³+4x−1; slope at zero | blank field-1, scalar correct + stale derivative alias; 5 derivative rows then 4 evaluation rows |

## 2. Generalized pattern

Differentiate constant-scaled positive-base exponentials using (b^x)′ = b^x ln(b), alongside existing sum, constant and power rules. For moderate questions evaluate the derivative at zero. Keep the exact source layout and stage sequence for each observed family. Hard adds a second distinct non-e base and nonzero small-integer evaluation using the same rules.

## 3. Complete component and bank mapping

Use a for an exponential coefficient, b for its base, c for an e^x coefficient, q for the magnitude of a negative polynomial coefficient, l for a linear coefficient and k for a constant magnitude. Signs, source degrees and source evaluation zero are fixed. Exact original-to-mask mapping is in masks.json; choice-mapping.json includes each original value and its parameterized full recipe, field, profile and designation. Radio recipes include whole equations where the source does. Source replay always chooses the complete observed profile, never an option pool.

- **q-11732** f=a·b^x: a·b^x (omit log), a·b^x/ln(b) (divide by log), a·ln(b)/b^x (invert exponential), a·ln(b)·b^x (correct).
- **q-1917** f=b^x+c e^x: b^x ln(b)+c e^x (correct), ln(b)+c e^x (omit exponential), b^x−ln(b)+c e^x (subtract log instead of multiply), b^x ln(x)+c e^x (wrong log input), b^x+c e^x (omit log).
- **q-11735** f=b^x−q x²+l x−k: b^x ln(b)−2q x²+l x (keep polynomial powers), b^x−2q x²+l x−k (also omit log/keep constant), b^x ln(b)−2q x+l (correct), b^x−2q x+l (omit log), b^x ln(b)−2q x²+l x−k (keep polynomial powers/constant). Exact observed expression patterns define reproducible operations; intent behind the mixed partial differentiations is a hypothesis, not recovered author code.
- **q-17388** f=b^x+c e^x at zero: c+1 (omit log), ln(b)+c (correct), ln(b)+c e (evaluate natural exponential at one), ln(b) (omit natural term), c (omit other-base term).
- **q-304038** f=a·b^x+l x+k: a ln(b)b^x+l, only correct RHS.
- **q-340272** f=k−a·b^x: −a ln(b)b^x and −a·b^x ln(b), equivalent aliases, not separate radio choices.
- **q-340280** f=b^x−q x³+l x−k at zero: ln(b)+l (correct scalar) and b^x ln(b)−3q x²+l (stale full derivative, incorrect response criterion). The latter is preserved only in explicit observed/raw_source profiles and removed from normal banks.

No interpolated perturbation recipes, number-offset guesses, unrelated random wrong values, or source-answer lookups are used. Every number in every original option has a specified mathematical role. Equal b and l in q-11735 are separate slots; powers 2/3 are fixed, not coefficient slots.

## 4. Reusable templates and constraints

masks.json contains fixed prose/TeX plus explicit complete-constant slots. Its small build script masks source numerals once, separating identical base/linear roles before mask construction. Runtime performs slot replacement only, never search-and-replace of small expressions across arbitrary prose. Derived q2=2q, q3=3q and c1=c+1 maintain all intermediate rows and bank formulas. Baseline source masks replay exact Unicode/TeX strings; normal output normalizes ln typography and repairs dy/dx. Missing solutions use the shared “Applying the formula, we get” and canonical coefficient/formula stages, with the natural-sum source using preceding sibling sum-rule scaffolding. Their authored origin is explicit.

All samplers and explicit inputs enforce identical level bounds. An eligible complete bank is chosen by template before parameter sampling; an equivalent pair rejects the whole instance. All radio banks are checked symbolically before deterministic shuffle. Blank equivalent aliases are retained where legitimate. Normal and source profile content identities reflect the complete actual prompt, solution, bank, fragment shape and correct designation; seed/order/profile labels do not affect IDs. Mathematical fingerprints use the canonical printed derivative and evaluation input, exclude banks, profile aliases and additive constants with zero derivative, and deduplicate the same task across layouts.

Hard rows retain formal differentiation, coefficient extraction, separate rule substitution, collection, evaluation substitution, component evaluation, and final sum. Powers and derivative coefficient products are shown before collection. Natural logs use ln; no chain, product, quotient or logarithmic differentiation is assessed.

## Anomalies and repairs

1. **q-11732/q-1917:** original correct ref and worked solution missing. The captured owning widget also lacks solutions/designations. Independently differentiating the printed functions identifies a ln(b)b^x and b^x ln(b)+c e^x. The two new designations are recovered, not matched original refs. New solutions are authored, not source-exact.
2. **q-11732 owning widget:** five choices, two identical wrong a·b^x expressions. The EDB capture deduplicates them to four unique values. source.json is unchanged; authoritative-widget-evidence.json preserves the additional UI evidence. Normal/source replay targets all four unique EDB values and does not introduce a duplicate answer.
3. **q-17388:** the original says d y/dx applied to 5e^x and e^x in two formal operator rows. This is malformed operator notation, because y is not defined. Normal output minimally repairs to d/dx, retaining stage order and mathematics. Explicit observed replay retains raw notation. Printed mathematics checks interpret that raw notation using the documented intended operator. Raw exact solution count and repaired-normal solution count are reported separately.
4. **q-340280:** second blank alias is an unevaluated derivative, while the task asks for a slope at zero. Native grading uses the designated correct scalar and rejects that alias. Retain both values under observed/raw_source API for fidelity, and retain only scalar in normal output. This is a response-fragment repair, not a recovered source designation.

All original prompts and all observed worked-solution sentences/rows replay exactly (5 available solutions). Every original value is reproduced including the invalid alias, with correctness explicitly separated from fidelity. Normal generated output never treats the stale alias as a valid fragment. No raw-exact claim is made for absent fields/solutions, normalized notation or historical UI duplicate-count mismatch.
