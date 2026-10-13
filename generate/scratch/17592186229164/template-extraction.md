# Template extraction

## 1. Individual observed descriptions

The source equation is y' - a*y = b*e^(k*x), with complementary solution A*e^(a*x). All variables are x and y; A is arbitrary. All five easy questions have a != k; all four rated moderate and the unrated question have a = k. Integers are exact, with no initial condition or plot.

| Source | a | k | b | Particular coefficient | Layout / complete accepted bank |
|---|---:|---:|---:|---:|---|
| q-332531 | 1 | 2 | 2 | 2 | aligned single derivative; Ae^x+2e^(2x) |
| q-332532 | 4 | 4 | 3 | 3 | compact inline prompt; blank has no bank/correct/solution/rating |
| q-332801 | 1 | 5 | 20 | 5 | unaligned derivative; Ae^x+5e^(5x) |
| q-332895 | 2 | 2 | 5 | 5 | resonant four derivative rows; Ae^(2x)+5xe^(2x) |
| q-332898 | 3 | 3 | 4 | 4 | resonant four derivative rows; Ae^(3x)+4xe^(3x) |
| q-332899 | -2 | -2 | 6 | 6 | positive ODE y coefficient, negative exponent; Ae^(-2x)+6xe^(-2x) |
| q-333168 | 7 | 7 | 5 | 5 | punctuation variant; Ae^(7x)+5xe^(7x), (5x+A)e^(7x); second designated correct |
| q-333176 | 5 | 3 | 2 | -1 | aligned single derivative; Ae^(5x)-e^(3x) |
| q-333178 | 4 | 1 | 6 | -2 | unit exponential derivative; Ae^(4x)-2e^x |
| q-333179 | 3 | 5 | 8 | 4 | derivative first prints alpha*e^(5x)*5, then 5alpha*e^(5x); Ae^(3x)+4e^(5x) |

Exact complete source strings and field ownership are in source.json; all corresponding explicit parameter/profile cases are in source-cases.json. No choice has an inferred error mechanism: all source values are accepted blank expressions. There are no incorrect choices to map.

## 2. Generalized patterns

Nonresonant: trial yp=alpha e^(kx); derivative k alpha e^(kx); substituted difference (k-a)alpha e^(kx)=b e^(kx); alpha=b/(k-a); sum with A e^(ax). Resonant: trial yp=alpha x e^(ax); differentiate using product rule; the two ax terms cancel; alpha=b; sum with A e^(ax). Return the complete RHS, because y(x)= is supplied beside the blank.

Hard, authored: y'-a*y=b*e^(ax)+c*e^(kx), a != k and both b,c nonzero. Trial alpha*x*e^(ax)+beta*e^(kx) incorporates exactly one resonance. Four ordered derivative rows preserve the formal derivative operator, separately differentiated components, product-rule terms and collected derivative. Three substituted/distributed/collected equation rows precede two coefficient-comparison stages; alpha=b, beta=c/(k-a). Finish yp, then y=yc+yp, then the complete family. This is the immediately preceding lesson's actual two-term ansatz, followed by the general-family task of the assigned KP. No progression among hard instances is introduced.

## 3. Component maps

Each source profile owns a complete prose mask with slots for ODE, supplied complement, homogeneous equation, solved complement, inline forcing, forcing exponential, trial, derivative block, substitution block, particular and final general family. Slot creation replaces entire math components; prose and parameter-free equations remain exact. layouts.json retains optional aligned derivative, extra chain-rule equality, commas/periods, and omitted period in q-332531's final row. Source profiles are raw:<source_id> and observed:<source_id>; raw preserves the incomplete source exactly, while observed adds the normal response-form clarification and the single documented missing-data repair. All values are derived; no source answer lookup is used.

For q-333168 the two bank recipes are A e^(ax)+b*x*e^(ax) and (b*x+A)e^(ax), preserving the second designation. The two are checked as complete families, allowing nonzero arbitrary-constant rescaling and shifting for mathematical QA. They remain two accepted aliases in normal output; no deletion is needed.

## 4. Reusable templates and domains

Fixed prose follows the sources, including the full opening rule, corresponding homogeneous equation, complementary solution, particular ansatz, derivative, coefficient determination, particular result and sum. Variable complete components use exact rational arithmetic. Signed coefficients are rendered as explicit + or - operations, never bare -- or +- tokens. Control strings are raw Python strings, and hidden control characters fail validation. Every blank retains {{field-1}}. x ranges over real numbers and A is arbitrary real.

Easy explicit bounds: nonzero integer a,k, |a|,|k|<=8; a!=k; nonzero |b|<=48; |b/(k-a)|<=8. Default samplers take |a|,|k|<=6 and choose b=(k-a)*q for nonzero small integer q, preserving observed integer coefficient-division workload. Explicit source replays include the observed coefficients.

Moderate explicit bounds: a=k, nonzero integers |a|<=8 and |b|<=12. Default sampler |a|<=6 and 1<=|b|<=6. Every question requires the same x-resonance product-rule workload.

Hard explicit bounds: nonzero integer |a|,|k|<=6 with a!=k, 1<=|b|,|c|<=18, |c/(k-a)|<=8, reduced denominator<=6. Default samples small signed b and c, with the entire instance rejected when bounds fail. Both components remain nonzero, so the two-coefficient comparison cannot collapse to moderate. These guards apply equally to explicit parameters. For all levels, no independent/dependent-variable renaming is offered.

Content identity is computed from generator version, actual prompt, fixed worked solution, complete bank values with designation, and field type. Seed/order and profile aliases cannot alter identity. Mathematical fingerprints use the normalized ODE and complete-family response criterion, excluding profile aliases and accepted-value multiplicity. All parameters affect the assessed ODE; arbitrary variable aliases are absent. A two-exponential forcing fingerprint sorts its exponent/coefficient pairs.

No plot extraction or renderer is needed: no image or geometric information occurs. Guide steps 5 and 7 have plot rating none.

The native engine checks canonical responses, meaningful factored forms with the prescribed A term, and wrong entries for all complete sources and all reviewed variants. Complete family equivalence is independently verified, including rescaling and shifting A. Native rescaling rejection is recorded honestly as a comparator form restriction, not mathematical non-equivalence. The source missing answer is inferred from differentiation, not counted as a matched original designation. Validation fails on unknown printed tokens, equation/derivative errors, missing math stages, incomplete families, changed source banks/prose, formatting, scope or native grading mismatches.
