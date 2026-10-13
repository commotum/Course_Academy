# Four-stage extraction

Each family has a separate captured prompt/solution template and one captured complete bank. `source.json` preserves all original attribute values/presence. Raw templates include known errors, while normal solutions apply the listed minimal corrections. No source record is omitted.

## quadratic

### 1. Specific source description

Source db-id 17592186124944, MA-id q-35995, level :question.difficulty/moderate. Exact object/features: a x²+b y²−c x, a,b,c positive integers; (3,1,1). Prompt:

Given that $f(x,y)=3{x}^{2}+{y}^{2}-x$, find the points $(x,y)$ where $∇f(x,y)=0.$

One selection radio, five choices, math answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Differentiate a sum with held-coordinate zeros; solve two independent linear equations.

### 3. Components and complete observed bank

r=c/(2a), s=c/(2b): observed [(r,s),(s,r/2),(0,0),(r,0),(0,s)]. The first, second and fifth have opaque/compound intent. Default [(r,0),(2r,0),(−r,0),(0,r),(r,s)]: omit factor 2, reverse sign, swap coordinates, mis-differentiate −cx with respect to y.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| a28c62d9-42c2-5bab-af79-c25e2c1af6db | `(\frac{1}{6},\frac{1}{2})` | False |
| bcdf801e-cc4b-53df-a3aa-d41d5909acc1 | `(\frac{1}{2},\frac{1}{12})` | False |
| ce509177-3d5a-5986-a13b-d30b4334afa7 | `(0,0)` | False |
| e8d388fe-66aa-582e-9f0b-761be7954f4c | `(\frac{1}{6},0)` | True |
| fe13f225-c620-5ad1-9d61-c77c2908a9da | `(0,\frac{1}{2})` | False |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 98. Parameters: {'a': 2, 'b': 1, 'c': 1} through {'a': 6, 'b': 4, 'c': 5}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## branch3

### 1. Specific source description

Source db-id 17592186125023, MA-id q-36970, level :question.difficulty/hard. Exact object/features: a xy+b xy²+c z³, (1,1,1). Prompt:

Given $h(x,y,z)=xy+x{y}^{2}+{z}^{3}.$ Find the points $(x,y,z)$ where $∇h(x,y,z)=0.$

One selection radio, five choices, text answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Compute three partials with zeros; factor y(a+by); substitute both y branches into the x equation; obtain z=0; return both points.

### 3. Components and complete observed bank

r=−a/b. Observed bank: origin plus (r,r,r); (1,r,1) only; (0,r,0) only; origin only; both true points. First two are opaque coordinate patterns. Default: both points, each single branch only, reversed y root only, all coordinates incorrectly equal r.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| 3a668d31-3cc8-5ea9-96ef-7e0fdcd58b8c | `$(0,0,0)$ and  $(-1,-1,-1)$` | False |
| 649040c7-206e-50ab-b58d-af585a9cdb7e | `$(1,-1,1)$ only` | False |
| b6c29216-4d6d-58d7-9dc1-49c48b3848a7 | `$(0,-1,0)$ only` | False |
| eff49e99-8930-5a35-aa82-5e696d691c29 | `$(0,0,0)$ only` | False |
| ff909540-c4d2-5403-9b36-0186dff131b9 | `$(0,0,0)$ and $(0,-1,0)$` | True |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 55. Parameters: {'a': 1, 'b': 1, 'c': 1} through {'a': 4, 'b': 4, 'c': 3}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## trig

### 1. Specific source description

Source db-id 17592186262919, MA-id q-128517, level :question.difficulty/moderate. Exact object/features: x²−2b x cos(ky), 0≤y<π/k; (b,k)=(1,1). Prompt:

Given that $f(x,y)={x}^{2}-2x\operatorname{cos}⁡y,$ find the points $(x,y),$ for $0\le y<\pi ,$ where $∇f(x,y)=0.$

One selection radio, five choices, text answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Compute two partials, isolate x=b cos(ky), substitute into second, use sin(2ky), enumerate y=0 and π/(2k), evaluate both x coordinates.

### 3. Components and complete observed bank

P=(b,0), Q=(0,π/(2k)). Observed/default bank: {P,Q}, {P}, {Q}, {(b,π/(2k))}, {(−b,0),(b,π/(2k))}. Omit branch or fail to evaluate cosine/sign. Frequency extension adds the same familiar chain-factor arithmetic and narrows the interval proportionally.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| 23779567-a8ad-53b9-bba7-20eb9434d446 | `$(1,0)$ and $(0,\frac{\pi }{2})$` | True |
| 252ff177-ca33-56d5-90df-65c900fa8710 | `$(1,0)$ only` | False |
| 3c0fd5bb-e524-591c-95eb-dd9ac92e0ae7 | `$(0,\frac{\pi }{2})$ only` | False |
| 8a3682d9-c2f8-516c-9549-f226b96cd4e4 | `$(1,\frac{\pi }{2})$ only` | False |
| cfca039c-c8d9-5aa9-b3cf-495e5bcbfed8 | `$(-1,0)$ and $(1,\frac{\pi }{2})$` | False |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 24. Parameters: {'b': 1, 'k': 1} through {'b': 6, 'k': 4}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## coupled

### 1. Specific source description

Source db-id 17592186385536, MA-id q-71437, level :question.difficulty/moderate. Exact object/features: 2k xy+y²−x²; k=2. Prompt:

Given that $g(x,y)=4xy+{y}^{2}-{x}^{2}$, find the points $(x,y)$ where $∇g(x,y)=0.$

One selection radio, five choices, math answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Compute zero-term partials, factor out 2, equate components, x=ky, substitute into kx+y=0 giving (k²+1)y=0, back-substitute x=0.

### 3. Components and complete observed bank

Observed: [(0,0),(−k,−1),(2k,2),(2k,−2),(k,1)]. Coordinate patterns are parameterized evidence, error intent unresolved. Default: [(0,0),(k,1),(−k,1),(1,−k),(1,k)]: satisfy only one component with a free coordinate chosen as 1, or reverse its sign; none satisfies the complete system.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| 2f709b8d-e22d-555e-8f82-4b819b741a2d | `(0,0)` | True |
| 4f628e18-1e56-5031-998e-e94575d669fb | `(-2,-1)` | False |
| 8a817cfe-6e50-5534-9c89-401a91beed6d | `(4,2)` | False |
| 6f89f99e-c222-5f75-b88f-1f3ed3be632f | `(4,-2)` | False |
| 55d2d586-a13f-55b7-99b9-71d0fd4b3d5b | `(2,1)` | False |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 12. Parameters: {'k': 1} through {'k': 12}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## entropy

### 1. Specific source description

Source db-id 17592186385543, MA-id q-71475, level :question.difficulty/hard. Exact object/features: x ln x+y ln y+z ln z−d x−e y−f z, positive coordinates; (1,1,1). Prompt:

Given that $g(x,y,z)=x\operatorname{ln}⁡x+y\operatorname{ln}⁡y+z\operatorname{ln}⁡z-x-y-z$, find the points $(x,y,z)$ where $∇g(x,y,z)=0.$

One selection radio, five choices, math answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

For each of three variables, formal sum input, full product rule plus held-coordinate zeros, evaluate v(1/v)=1, collect constants, gradient/system, exponentiate each logarithmic equation and return one triple.

### 3. Components and complete observed bank

Observed: zero triple; (exp(d),exp(e),exp(f)); (exp(−d),exp(−e),exp(−f)); negative-one triple; true exp(d−1), exp(e−1), exp(f−1). Literal negative/zero source choices preserved, not promoted to normal defaults. Default true triple, exp(−1) triple (omit linear term), exp(d,e,f) (omit product-rule +1), exp(−d−1,−e−1,−f−1) (reverse linear sign), exp(1−d,1−e,1−f) (reverse logarithm sign). Reject all-2 collision.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| 00852e0a-f6f6-5c5a-ac0e-5aab7917034a | `(0,0,0)` | False |
| 0a138de7-1cdb-5fca-ab9b-192f03014909 | `(e,e,e)` | False |
| 4db23065-4328-5f87-98fa-c2f53e71285d | `(\frac{1}{e},\frac{1}{e},\frac{1}{e})` | False |
| c45fae02-a3c6-5e5b-83c3-515185ddf33b | `(-1,-1,-1)` | False |
| 965bb97e-ab1f-5bcd-b8b9-68650da44bfa | `(1,1,1)` | True |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 27. Parameters: {'d': 2, 'e': 2, 'f': 2} through {'d': 4, 'e': 4, 'f': 4}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## logquad

### 1. Specific source description

Source db-id 17592186395845, MA-id q-36911, level :question.difficulty/moderate. Exact object/features: ln(x²+c)+a(y−b)²; (a,b,c)=(2,3,1), c>0. Prompt:

Given that $f(x,y)=\operatorname{ln}⁡({x}^{2}+1)+2(y-3)^{2}$, find the points $(x,y)$ where $∇f(x,y)=0.$

One selection radio, five choices, math answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Formal partials; logarithmic chain product plus zero; y square chain product plus zero; reduction; two independent zero equations; x=0,y=b.

### 3. Components and complete observed bank

Observed: [(0,0),(1/a,b/(2a)),(c,a),(b,0),(0,b)]. Full coordinate patterns, opaque intent. Default true, omitted shift, reversed shift, exchanged coordinates, divide shift by derivative scale: [(0,b),(0,0),(0,−b),(b,0),(0,b/(2a))].

| Source answer UUID | Exact value | Correct |
|---|---|---|
| c3c6467b-917f-5aae-9cc9-3d8de87bf705 | `(0,0)` | False |
| 95acc209-e214-5661-af27-7731166005f9 | `(\frac{1}{2},\frac{3}{4})` | False |
| 8a0c76fb-2820-5cf1-9645-b9dbc230a965 | `(1,2)` | False |
| bef1175c-5920-532e-b7b5-9da5b087ef6f | `(3,0)` | False |
| 4b5d5b3b-9e1f-57a7-8376-c15ae99d31d4 | `(0,3)` | True |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 200. Parameters: {'a': 1, 'b': 1, 'c': 1} through {'a': 5, 'b': 8, 'c': 5}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## reciprocal2

### 1. Specific source description

Source db-id 17592186400373, MA-id q-128519, level :question.difficulty/moderate. Exact object/features: A/y−m y/x+x with A=n³/m, m divides n²; source n=m=3. Prompt:

Given that $g(x,y)=\frac{9}{y}-\frac{3y}{x}+x,$ find the points $(x,y)$ where $∇g(x,y)=0.$

One selection radio, five choices, text answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Compute reciprocal partials; isolate y=−x²/m; substitute, reciprocal square, expanded numerator, common denominator, nonzero numerator equation, cubic root, back-substitute y; return the single negative point.

### 3. Components and complete observed bank

P=(−n,−n²/m), Q=(n,n²/m). Observed/default: {Q,P}, {P}, {(n,−n²/m),(−n,n²/m)}, {(−n,n²/m)}, {Q}. Sign and extra/omitted-real-root errors follow the cubic/substitution operations.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| 7a10163a-dceb-5ab4-b904-ba9a054ac615 | `$(3,3)$ and $(-3,-3)$` | False |
| 83d361ab-691b-507d-aa60-ee6cbedb4a3b | `$(-3,-3)$ only` | True |
| 6ad8d842-3217-5d0b-a3d1-f6c4802c29c7 | `$(3,-3)$ and $(-3,3)$` | False |
| e58ac478-7209-5f45-a6c1-f164d3f25552 | `$(-3,3)$ only` | False |
| bf97e181-9c44-5eb6-9ba0-39838ff1806e | `$(3,3)$ only` | False |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 19. Parameters: {'n': 2, 'm': 1} through {'n': 8, 'm': 8}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## reciprocal3

### 1. Specific source description

Source db-id 17592186403475, MA-id q-71474, level :question.difficulty/hard. Exact object/features: pq/(xy)+q/y+p/(zx)−z; p=q=1. Prompt:

Given that $f(x,y,z)=\frac{1}{xy}+\frac{1}{y}+\frac{1}{zx}-z$, find the points $(x,y,z)$ where $∇f(x,y,z)=0.$

One selection radio, five choices, text answer type; no plot. The complete solution sequence is quoted in review.md.

### 2. Shared pattern

Three full partial rows including zeros; collect fractions; gradient/system; second equation x=−p; substitute into third, normalize to 1−z²=0, take both ±1 roots; substitute into first, y=−qz; evaluate each y branch; return both triples.

### 3. Components and complete observed bank

P=(−p,−q,1), Q=(−p,q,−1). Observed/default: {P}, {(−p,−q,−1),(−p,q,1)}, {P,Q}, {Q}, {(p,−q,−1),(p,q,1)}. Single branch omissions and sign errors in solved x or relation y=−qz.

| Source answer UUID | Exact value | Correct |
|---|---|---|
| c9ec4597-899c-5f21-a16c-2695e9541e21 | `$(-1,-1,1)$ only` | False |
| 4c24ba4d-0c93-5d33-a565-f106f0e3b765 | `$(-1,-1,-1)$ and $(-1,1,1)$` | False |
| a1afdd74-60dd-5f9b-bad5-2d5610ad3377 | `$(-1,-1,1)$ and $(-1,1,-1)$` | True |
| e68b95bf-0642-5f05-aa57-9a8fabde2338 | `$(-1,1,-1)$ only` | False |
| 15edafbf-4f96-51e2-9aa0-c33dbac930ad | `$(1,-1,-1)$ and $(1,1,1)$` | False |

### 4. Reusable template

The fixed source prose, formal operators, zero-term rows, block order, branch introductions and conclusion become the template. Complete expression/coordinate/prose-equation slots are replaced in one longest-first pass; substitutions never recurse into generated TeX. The `build` function maps every initial derivative input, reduced derivative, intermediate coefficient, substitution, branch coordinate and concluding tuple to calculations from the same parameters. Raw profile preserves source spelling/spacing; normal profile repairs only documented anomalies. Explicit inputs obey the same finite bounds as sampling.

Catalog size before whole-bank rejection: 64. Parameters: {'p': 1, 'q': 1} through {'p': 8, 'q': 8}. Enumerated domains in the script are authoritative (not the lexicographic endpoints alone). Common polynomial scaling is primitive/reduced; seed, bank profile, notation and option order never increase task counts. Full meaningful counts after rejection are in validation.json.

## Authored missing easy — shifted_log

1. Canonical evidence: e-3133 uses `(y−4) ln(x−2)` with point `(3,4)`. There are no rated easy practice records.

2. Pattern: two independent components vanish, giving y=b and ln(x−a)=0 => x=a+1. This is precisely the canonical gradient-vanishes skill, with no additional topic.

3. Components: signed shifts a,b∈[−4,4], x>a; correct `(a+1,b)`, distractors `(a,b)`, `(a−1,b)`, `(a+1,0)`, `(a+1,−b)`. These respectively mistake ln argument for 0 or −1, omit y shift or reverse its sign. Reject b=0 because the bank collides.

4. Template: canonical shared formal partials, gradient and coefficient equating sentences, two independent zero equations, each solution and final tuple; normal visible system brace; single math radio with five choices. Equal workload for every valid signed-shift instance; no progression.
