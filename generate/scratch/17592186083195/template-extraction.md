# Template extraction

The common task is to evaluate a convergent upper-limit improper integral of C x^(-p), with C>0, p>1 and lower endpoint L>0. First replace infinity by a, rewrite a radical as a rational power where needed, integrate using the power rule, evaluate the endpoints, then let a tend to infinity. The exact answer is C L^(1-p)/(p-1). For real radicals the positive integration domain avoids branch ambiguity. No new or reused plot assets are required; stage 5 and 7 plot work is inapplicable.

Every source question's original Markdown, answer shape, complete field-owned bank, correct reference and exact fixed solution are retained in source.json. templates.json lists every source answer ID, value, type, correct designation, coefficient-scaled expression, and profile. No pooled/mixed banks are used. The proportional observed recipes reproduce complete source mathematical values; their error interpretations remain unresolved. They are recorded as observed patterns rather than asserted misconception theories. There is no unresolved algebraic source-bank comparison.

The extracted templates hold exponent, endpoint, variable, root degree, expression layout, and solution sequence fixed in each subtemplate. @INTEGRAND@, @C@, @K@ and @V@ vary together. K=C/(p-1) and V=K L^(1-p). Each complete radio bank scales each original math value by C/C0; its text divergence option is unchanged when present. Blank answers are just the exact scalar, with no added distractors or feedback. The source instructional sentences and source notation are unchanged. Parenthesized versus unparenthesized primitives and the shortened inverse-square sequence remain separate layouts.

The proposed sampling policy is deliberately narrower than unrestricted power-law integrals: C is an integer from 1 to 2000, except q-152754 uses C=1/D with 2<=D<=2000. Every observed coefficient lies in its corresponding policy. Across the set of fixed source subtemplates, every observed exponent, endpoint and variable is covered. Negative or zero coefficients, new endpoint values, new exponents, and divergence tasks are excluded. Changed positive coefficients produce different integrands and different exact answers, not seed-only or formatting-only variants.

## Source-specific components

|Source|Level|C|p|L|Variable|Response/layout|Profile|
|---|---|---:|---:|---:|---|---|---|
|q-152777|moderate|2|9/2|1|x|radio/pulled|q-152777|
|q-5962|easy|3|3|1|\theta |radio/inline|q-5962|
|q-152755|easy|2|6|1|\theta |radio/inline|q-152755|
|q-152758|easy|5|2|3|x|radio/inline|q-152758|
|q-152762|moderate|2|4/3|8|z|radio/pulled|q-152762|
|q-350322|easy|18|4|3|x|blank/pulled|none|
|q-350331|moderate|5|8/3|1|y|blank/pulled|none|
|q-350333|moderate|12|7/3|1|s|blank/pulled|none|
|q-350337|moderate|8|13/5|1|t|blank/pulled|none|
|q-100310|easy|4|2|2|z|radio/short|q-100310|
|q-152754|moderate|1/4|3/2|2|t|radio/pulled|q-152754|
|q-350324|easy|16|3|2|x|blank/pulled|none|

The 13th source, q-128340, uses partial fractions of 7/((x-3)(2x+1)) on x>=4, with log-difference primitive and logarithmic limit. It requires a separate rational-function template. Its missing prompt definition is retained as evidence, and this frozen package excludes the family explicitly. The canonical e-511 uses C=8,p=5,L=2 and yields 1/8; it supports the common method but does not count as practice.
