# Four extraction stages

## 1. Specific source descriptions

Every practice source asks which plot shows some solution curves. Each bank contains five images; each image has three curves. All correctly designated images show vertical translates of a single primitive. Every solution begins with integrating (or rearranging and integrating), displays the indefinite-integral stages, then selects three constants and shows a labeled solution plot.

| Source | Actual ODE | Primitive | Selected constants | Solution structure |
|---|---|---|---|---|
| q50195 | y′=2(x−1) | (x−1)²+C | −1,0,1 | two equal integral rows, primitive row |
| q50196 | y′=−3(x+1)² | −(x+1)³+C | −1,0,1 | integral, repeated factored integral, primitive |
| q119132 | y′=e^(−x/4)/2 | −2e^(−x/4)+C | 0,3,6 | integral, coefficient extraction, primitive scaling, collection |
| q49947 | xy′=1, x>0 | ln x+C | −1,0,2 | rearrange, integral, repeated integral, absolute-log primitive, positive-domain form |
| q50197 | x²y′+1=0, x>0 | 1/x+C | −1,0,1 | rearrange, integral, repeated integral, primitive |
| q50198 | y′=−2 | −2x+C | −3,0,3 | integral, primitive |
| q79565 | y′=2x | x²+C | −1,0,1 | integral, primitive (source omits y on final aligned LHS) |
| q79566 | y′=3(x+2)²/2 | (x+2)³/2+C | −1,0,1 | integral, factored integral, primitive |
| q119139 | y′=−4e^(2x) | −2e^(2x)+C | −2,0,2 | integral, coefficient extraction, primitive scaling, collection |
| q119142 | y′=−3(x−1)²/4 | −(x−1)³/4+C | −2,0,2 | integral, coefficient extraction, primitive scaling, collection |
| q79563 | y′=3 | 3x+C | −2,0,2 | integral, primitive |

The canonical example y′=2x explicitly explains varying C after integrating to x²+C. It is evidence for instructional purpose, not a practice replay denominator.

## 2. Shared pattern

Integrate y′=g(x) once to obtain F(x)+C, then identify a whole plotted family. Correctness requires every displayed curve to satisfy the actual ODE on the stated domain. Adding a constant to F produces the same general family, so families are compared by derivatives. Distinct C values, curve colors or vertical positioning cannot make a wrong family. Horizontal translates of logarithm, reciprocal or cubic curves can be a distractor family even when the silhouettes look similar.

## 3. Component mapping

`recipes.json` records each source's exact prompt, fields, all answer fragments/image values and full solution, alongside actual parameter values, five complete plotted recipes, their color assignments, and correct index. `raster-evidence.json` maps every source asset to its own origin, pixels-per-coordinate-unit and fitted colored curves. `asset-index.json` maps source assets to full-resolution local copies. `plot-extraction.md` lists the complete banks in source field order. The legacy q50195 field is preserved independently, including absent correct designation. All observed answer types are image.

Raw bank recipes are affine transports of explicit extracted curve formulas: x_old=h_old+(x−h_new) k_new/k_old for exponential templates, x_old=h_old+(x−h_new) otherwise, and vertical scale a_new/a_old. This is a mathematical plot recipe, not a presumed diagnosis of the original author's mistakes. Four source metric coefficients remain inferential; their exact source PNGs are preserved, and their profiles are evidence-only. These raw profiles are public through `generate(..., profile='raw-q-…')`; they are not selected by normal generation.

## 4. Reusable components and constraints

Parameters are complete mathematical components: family, primitive coefficient a, horizontal shift h, exponential rate k, and three chosen constants. Primitive and derivative are calculated exactly with SymPy. Source math masks remove complete components before inserting replacements; exponent digits and prose are never blind numeric substitutions. Original component spelling is retained at original mathematics, preserving every source stage and prose sentence. Changes are generated through the same masks. There is no branch that returns a stored source payload or answer lookup table.

Normal profiles deliberately use an authored complete bank of five families. Correct primitive first; then sign reversal, derivative/degree confusion, wrong scale or horizontal shift, chosen together by family before parameter sampling. A whole instance is rejected if two families have equal derivatives or a required wrong family satisfies the printed ODE. Linear banks use five unequal slopes, because horizontally shifting a line would merely change C and create an ambiguous correct answer. Full banks have five image choices; all choices share plotting style and domain conventions.

The worked solution is fixed independently of submitted choice. Normal output has integration, coefficient/primitive stages and final y=F+C, plus one labeled translated-family plot. Parameter/recipe/snapshot metadata stays outside learner prose.

### Source anomaly and fidelity denominators

q50195 has two radio fields with key `selection`; the older field has no correct ref, while the newer field designates the correct parabola. The authoritative `/home/jake/Developer/MA/DATA/Lessons/1061/Source/1061.json` captured widget has one multiple-choice question, five images, one choice bank. Raw replay preserves both field attributes and absent designation. Normal output uses one supported field. The missing designation is not counted as a matched or native-tested correct ref.

No incorrect ODE primitive or incorrect source designation was found. The source omission of y in q79565's final aligned LHS and intermediate convention omitting C on some primitive-scaling rows are kept in raw replay. Normal solutions state y and retain C. This is an authored presentation, not an exact-source claim.
