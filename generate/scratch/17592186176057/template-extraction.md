# Template extraction

## 1. Specific source descriptions

### q-136545

If $cos⁡a=-\frac{1}{3},$ then $cos⁡(-a)=$

Parameters: {"c": "-1/3", "variable": "a"}. Field selection, radio, five scalar math options. Source label: :question.difficulty/easy.

Solution: graph recall; reflection/symmetry prose; generic evenness identity; aligned negative argument = positive argument = given exact value.

### q-136634

If $\cos x =-\frac{11}{24}$, then $\cos (-x + 16π) =$

Parameters: {"c": "-11/24", "variable": "x", "n": 8}. Field selection, radio, five scalar math options. Source label: unrated.

Solution: graph recall; period and symmetry bullets; generic evenness identity; two-row periodicity alignment; two-row evenness alignment; final sentence. q-136634 has no source solution, so its raw profile leaves it absent and its repair uses this common solution.

### q-136629

If $cos⁡x=-\frac{3}{10},$ then $cos⁡(-x)=$

Parameters: {"c": "-3/10", "variable": "x"}. Field selection, radio, five scalar math options. Source label: :question.difficulty/easy.

Solution: graph recall; reflection/symmetry prose; generic evenness identity; aligned negative argument = positive argument = given exact value.

### q-158047

If $cos⁡a=-\frac{\sqrt{2}}{3},$ then $cos⁡(-a)=$

Parameters: {"c": "-sqrt(2)/3", "variable": "a"}. Field selection, radio, five scalar math options. Source label: :question.difficulty/easy.

Solution: graph recall; reflection/symmetry prose; generic evenness identity; aligned negative argument = positive argument = given exact value.

### q-158052

If $cos⁡x=-1,$ then $cos⁡(-x+24\pi )=$

Parameters: {"c": "-1", "variable": "x", "n": 12}. Field selection, radio, five scalar math options. Source label: :question.difficulty/moderate.

Solution: graph recall; period and symmetry bullets; generic evenness identity; two-row periodicity alignment; two-row evenness alignment; final sentence. q-136634 has no source solution, so its raw profile leaves it absent and its repair uses this common solution.

### q-158059

If $cos⁡x=0,$ then $\pi cos⁡(-x+18\pi )-\frac{1}{2}=$

Parameters: {"c": "0", "variable": "x", "n": 9, "scale": "pi", "offset": "-1/2"}. Field selection, radio, five scalar math options. Source label: :question.difficulty/hard.

Solution: same graph, period and symmetry bullets (source says symmetric over); identity; periodicity alignment; evenness alignment; final three-row affine alignment: substituted product, evaluated product with offset retained, collected answer.

## 2. Generalized pattern

Given cos(v)=c, find cos(-v) at easy, cos(-v+2nπ) at moderate, or A cos(-v+2nπ)+b at hard. Required response is the exact scalar, not a structural simplification. The identity is always cos(-v)=cos(v), with the positive argument on the right. The source hard scale π and zero c do not require evaluating a familiar angle.

## 3. Complete component and bank mapping

A denotes scale, b offset, n integral full periods, c given cosine. Values are structural parameterized recipes rather than literal-source returns. The correct result is derived as Ac+b (A=1,b=0 outside hard). All banks are mapped one to one at original parameters. Recipe intent is not asserted from a lone scalar.

| Source | Original value | Parameterized operation | Designation |
|---|---|---|---|
| q-136545 | $\frac{2}{3}$ | -2c | wrong |
| q-136545 | $0$ | 0 | wrong |
| q-136545 | $-\frac{2}{3}$ | 2c | wrong |
| q-136545 | $\frac{1}{3}$ | -c | wrong |
| q-136545 | $-\frac{1}{3}$ | c | correct |
| q-136634 | $\frac{11}{24} + 8π$ | -c+nπ | missing source key |
| q-136634 | $-\frac{11}{24}$ | c | missing source key |
| q-136634 | $-\frac{13}{24}$ | -(1+c) | missing source key |
| q-136634 | $-\frac{11}{24} + 8π$ | c+nπ | missing source key |
| q-136634 | $\frac{11}{24}$ | -c | missing source key |
| q-136629 | $\frac{7}{10}$ | 1+c | wrong |
| q-136629 | $-\frac{7}{10}$ | -1-c | wrong |
| q-136629 | $\frac{3}{10}$ | -c | wrong |
| q-136629 | $-\frac{3}{10}$ | c | correct |
| q-136629 | $\frac{\sqrt{91}}{10}$ | sqrt(1-c²) | wrong |
| q-158047 | $-\frac{\sqrt{2}}{3}$ | c | correct |
| q-158047 | $-\frac{\sqrt{7}}{3}$ | -sqrt(1-c²) | wrong |
| q-158047 | $-\frac{1}{6}$ | -1/(2d), d=denominator(c) | wrong |
| q-158047 | $\frac{\sqrt{7}}{3}$ | sqrt(1-c²) | wrong |
| q-158047 | $\frac{\sqrt{2}}{3}$ | -c | wrong |
| q-158052 | $-1+12\pi $ | c+nπ | wrong |
| q-158052 | $0$ | 0 | wrong |
| q-158052 | $-\frac{1}{12}$ | c/n | wrong |
| q-158052 | $-1$ | c | correct |
| q-158052 | $1$ | -c | wrong |
| q-158059 | $1$ | 1 | wrong |
| q-158059 | $\pi -\frac{1}{2}$ | A+b | wrong |
| q-158059 | $0$ | c | wrong |
| q-158059 | $2\pi $ | 2A | wrong |
| q-158059 | $-\frac{1}{2}$ | Ac+b | correct |

Interpretation limits: the zero, doubled-given, complement and complementary-root recipes are structurally simple but source error intent is unproved. In q-158047, -1/(2d) is an explicit denominator-pattern replay recipe, with unresolved pedagogical interpretation. In q-158052, c/n is an explicit full-period-count division pattern, not recovered author code. In q-158059, constants 1 and 2A are structural preserved fragments, not invented diagnoses. These entire profiles remain selectable for replay and changed-parameter tests; they are never the default authored banks.

Authored default profiles (each complete five-operation bank): easy [c,-c,1-c²,sqrt(1-c²),2c]; moderate [c,-c,c+2nπ,c/(2n),1-c²]; hard [Ac+b,-Ac+b,Ac-b,c+b,A+b]. These are same-method confusion operations (oddness, substituted complementary square/root, output shift/division, dropped or sign-changed affine components). Each complete bank is validated for exactly one correct scalar and pairwise inequality. No first-valid distractor pooling or random numeric perturbation is used. Learners receive no new diagnosis prose.

## 4. Reusable templates and constraints

Fixed: graph asset, all shared sentences, the identity and its right-side cosine, radio selection field and five values. Variable: complete given scalar c, variable v, integral count n, hard scale A and offset b. Separate prompt mask preserves q-136634 spaced \cos and Unicode π. Moderate/hard masks preserve the unreduced negative argument, expansion ±2π·|n|, cos(-v), cos(v), c, and affine substitution/product/reduction rows. Rows are constructed unevaluated until their particular evaluation stage. The graph remains y=cos(x), not y=cos(v) transformed by n/A/b.

Correct answer computed before the wrong values; exactly one correct designation per normal record. Source raw q-136634 has no key, difficulty or worked solution. Public generate(... profile="q-136634_raw") reproduces those absences through the same parameterized prompt/bank API; profile="q-136634_repaired" retains all choices and inserts the independently derived key c and shared moderate solution. There is no mathematical source error requiring changed values. Five available designations and five complete available solutions are exact; one missing designation/solution is reported separately, never counted matched.

Displayed choices normalize spacing and Unicode π to TeX with full exact equivalence. Source prompt strings and all available solution strings remain byte-exact at original parameters. Canonical mathematical fingerprint includes c,n,A,b and level, excluding variable aliases, bank profiles, choice order and notation spelling. Content identity uses version, actual prompt, fixed solution, entire displayed bank and key status. The same content under seed/profile aliases retains an ID; changed content cannot share one.
