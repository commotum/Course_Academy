# Template and complete-bank extraction

All original parameters and source IDs are in source-cases.json. source.json preserves the original Pull unchanged; source-questions.md spells out every source field and every original option. Served fidelity is independently demonstrated by source-bank-fidelity.json, rather than by those raw copies.

Write L=ln|x| and include +C in every expression below. Slot domains are the finite lists in extraction.json and in the generator's TEMPLATES. All choices in each row form one complete observed bank; they are never pooled or truncated. Recipes retain unusual compound patterns without attributing a pedagogical interpretation unsupported by the capture.

| Source and original slots | Complete ordered bank recipes (correct marked *) |
|---|---|
| q-103374: a=3,b=6,d=2 | a x²+ln|a x|; (a/d)x²−ln|a x|; *(a/(2d))x²−(b/d)L; (a/(2d))x²−ln|a x|; (a/d)x²+(b/d)L |
| q-103593: p=3/2,b=1/2 | (p+1)x^p+bL; (p+1)x^(p+1)+(1/b)L; *x^(p+1)/(p+1)+bL; p x^p+(1/b)L; p x^(p+1)+(1/b)L |
| q-29885: n=2,r=2; power n/3 | ((n+9)/(n+3))x^((n+9)/3)+sqrt(r+3)L; ((n+5)/(n+3))x^((n+2)/3)+rL; (3/(n+3))ln(x)x^((n+3)/3)+L; ((n+7)/(n+3))x^((n+5)/3)+sqrt(r+1)L; *(3/(n+3))x^((n+3)/3)+sqrt(r)L |
| q-29886: a=2,n=7,d=3; power n/3 | *(3a/(n+3))x^((n+3)/3)−L/d; ((n−2)/a)x^(n/3)−dL; (n/a)x^((n−5)/3)−L; x^((n−6)/3)/(n−2)−L/d; (n/(n−2))x^(n/3)−dL |
| q-29888: a=3,b=3 | *(a/2)x²+bL; ((a+1)/b)x²+(b+2)L; ((a−2)/2)x²+bL; ((a−1)/b)x²+(b−1)L; ((a+2)/2)x²+(b+1)L |
| q-49100: a=2,c=1 | ac x L; ln|a−c/x|; a x−cL; *a²x−2acL−c²/x; (a x−cL)² |
| q-29915: m=3,a=1,b=5; second root exponent m+2 | −bL; *(a−b)L; (b−a)L; −(a+b)x; b x |
| q-29836: a=3,d=5,b=3 | ln(x)+(b+4)x²/2; *(a/d)L+b x²/2; ((a+4)/d)L+d x²/2; (d/a)L+x²/2; (a/d)ln(x)+d x²/2 |
| q-29857: a=2,b=1 | aL−2b/x; bL−b x^(1/2); x−2b x^(1/2); *aL−2b x^(1/2); bL+2b x^(1/2) |

The q-103374 domain excludes b=d: then choice four would differ from the correct answer by a constant, because ln|a x|=L+ln(a). Such an option is another correct antiderivative family. Every accepted finite instance is tested for uniqueness by differentiation, including this constant-family issue. A foreign answer ID is an ownership error, separate from a rejected owned distractor.

Prompt and shared prose are fixed. Each source's exact ordered solution rows are retained with simultaneous token substitution in mathematical slot components, including unsimplified exponent additions, fraction simplification, binomial expansion and formal integral operands. No original-value bypass or raw source-bank return occurs; original and changed values use the same formulas and solution renderer. Presentation normalization repairs invisible function-application characters and bare `ln` into canonical TeX. Mathematical comparisons are kept separate from byte comparisons of normalized prose.

The source gives fractions, radicals, and negative powers. Positive-domain validation handles those real powers without complex branches; integer rational forms hold on connected intervals with x≠0. Log distractors with additional poles retain their own domain restrictions. ln(x) is preserved in source profiles where observed. No coefficient, power, or added operator enlarges the fixed method. Hard root exponent changes keep the gap exactly 2; semantic capacity excludes these cosmetic changes because the assessed integrand depends only on b.

The larger but bounded banks provide repeated practice: values change all dependent prompt, option, and solution rows. Sparse patterns support the conservative affine distractor generalizations above; their original values are observed, while their changed numerical coefficients are declared same-method extensions. Source-only coefficients need not imply those recipes are explanatory misconceptions.

The revised moderate slots are a=2..8,c=1..5 with gcd(a,c)=1, excluding uniformly scaled squared-binomial aliases. The reciprocal coefficient c is already the constant-factor role in the source; its sampled square is carried through the split, constant-factor and power-rule rows. The revised hard slots are a=1..8,b=2..25,b>a,m∈{1,3,5,7}; a is the coefficient of the quotient of roots. Its factor is carried through both formal reciprocal integrals and the collection row. Source a=1 is rendered without a redundant unit multiplier. Semantic hard capacity counts the canonical integrand (a−b)/x, excluding exponent aliases and repeated coefficient differences.

The unrated q-29836 domain additionally excludes a=b,d=a+4: its first and third observed-pattern options would coincide. This exclusion was discovered by exhaustive independent rendered-bank validation.
