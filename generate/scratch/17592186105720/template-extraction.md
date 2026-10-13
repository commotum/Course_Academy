# Templates and exact banks

Every source's original prompt, solution, field identity and each choice appear in `extraction-data.json`. Each supported choice is mapped to its field, source answer identity, exact original value, complete source bank and parameterized expression. `templates.json` freezes the corresponding prompt and solution slots; no pooled or inferred distractor bank is used.

The shared move is to integrate a reciprocal term, then express the arbitrary additive constant as a nonzero coefficient times ln(K), K>0, and combine it with ln|x|. The domain is x>0 or x<0; K is a positive arbitrary constant on each connected interval. Every supported prompt asks for one complete antiderivative and has exactly one five-choice radio field named `selection`.

| Source/profile | Original integrand | Parameter/domain | Correct family | Sequence |
|---|---|---|---|---|
| q-15717 | 8/(3x) | n/3, n>3, gcd(n,3)=1, n<=31 | (n/3)ln(K|x|) | Factor, reciprocal integral, C=(n/3)ln K, log sum, combine |
| q-15710 | 5/(2x) | n/2, n>2, odd n<=31 | (n/2)ln(K|x|) | Same operations, source spacing and commands retained after log normalization |
| q-29834 | -5/(2x) | -n/2, n>2, odd n<=31 | -(n/2)ln(K|x|) | Negative factor, reciprocal integral, C=-(n/2)ln K, combine |
| q-103605 | (2x-1)/x | n=2..16 | nx-ln(K|x|) | Split numerator, cancel x, sum and factor rules, log constant |
| q-103375 | (1+3/(2x))^2 | odd n=3..31; a=n/2 | x-a^2/x+2a ln(K|x|) | Expand square, integrate three terms, simplify inverse power, log constant |

Original features are retained: positive fractional coefficients, a negative fractional coefficient, a negative reciprocal term beside a positive constant, and a binomial square with a positive fractional reciprocal coefficient. Sampling bounds are narrower authored policies, separately recorded from observed values. Numerator bounds and integer/rational restrictions preserve the original workload. No unsupported easy assignment is inferred. The n=2 square case is excluded because a=a^2 causes this bank's distractors to collide.

The exact complete bank recipes are in `templates.json`, including altered logarithm arguments, reciprocal coefficient scales, wrong signs, a misplaced integration constant, failure to integrate the constant, failure to square the reciprocal coefficient, and coefficient moved into the logarithm. Their original mathematical values are fully reproduced. Uncertain pedagogical interpretations are labeled as observed expressions rather than guessed mistakes. Source replay maps all 25 supported choices (20 distractors) one to one and verifies correct designations; none are unmapped.

Fixed parts include instructional sentences, equation sequence, variable x, field layout and five-choice count. Variable parts are the numerator/coefficient and its derived square; no plot or optional component occurs. Exact SymPy answers are computed before bank rendering. Logs are normalized to `\ln`, with a space before a letter to keep commands valid; this changes notation only. Each question has one fixed worked solution, with no additional learner-facing feedback.

Distinct tasks are normalized exact integrands, across source profiles and display forms. Record UUIDs include exact bank identity, but inventory never treats a different profile, seed or order as new mathematics. Every generated question, field and owned answer uses deterministic UUIDs unrelated to Math Academy IDs. Validation independently parses every printed prompt, all answer values and every solution equation on both branches, checks real-valued domains and arbitrary constants, and exercises actual application radio grading. There are 64 moderate and 15 hard tasks in the frozen domain; future shortages beyond that domain remain explicit.
