# Template extraction

The exact originals, all choices, field identities, solutions and domain restrictions are retained in `reference/source.json`. `template-extraction.json` describes every original separately, including every choice's owning field and correct status. No plots occur anywhere in these questions, banks, or solutions; no image publication is needed.

Write D = dy/dx below. The shared task is to express the same ODE as D + P(x)y = Q(x). An algebraically equivalent rearrangement can be an incorrect response when it is not in this requested form. Consequently the validator compares complete normalized equations and separately checks response shape; it never treats equation equivalence alone as correctness.

Each source ID names a complete bank profile. Banks below are ordered as the generator's bank; source order is irrelevant. C denotes the correct slot. All parameter values are integer; the original values and proposed bounds are separate.

| Source/template | Original parameters | Proposed bounds | Prompt | Correct P; Q | Complete bank recipes |
| --- | --- | --- | --- | --- | --- |
| q-16400 | a=2,b=3,c=1,h=4 | a=2..5,b,c=1..5,h=1..8 | aD-b cos x=c-hy sin x | h sin x/a; (c+b cos x)/a | D+h sin(x)y=c+b cos x; D+h cos(x)y=c+b sin x; **C** D+Py=Q; D+Q=Py; D+Py=c+(b/a)cos x |
| q-8359 | k=1 | k=1..8 | D=(2x-ky)/x | k/x; 2 | ky=2x-xD; D+(k/x)y-2=0; xD+ky=2x; D=-(k/x)y+2; **C** D+(k/x)y=2 |
| q-103349 | n=1 | n=1..6 | exp(2nx)D+2exp(nx)y-x=0 | 2exp(-nx); x exp(-2nx) | D+exp(-2nx)y-x exp(-nx)=0; **C** D+Py=Q; D+Py-Q=0; D-y=Q; D+2y=Q |
| q-103354 | n=1 | n=1..6 | cos(nx)D+sin(2nx)-sin(nx)y=0 | -tan(nx); -2sin(nx) | D+2sin(nx)=tan(nx)y; D-cot(nx)y=2cos(nx); D+sec(nx)y=-2sin(2nx); D+sin(2nx)=sec(nx)y; **C** D-tan(nx)y=-2sin(nx) |
| q-16396 | k=1 | k=1..8 | yD+x²y=ky²x, y != 0 | -kx; -x² | D+((k-x²)/(k+x²))y=k; D-ky=-2kx; **C** D-kxy=-x²; D=-x²; D+x²y=kx |
| q-79697 | k=1 | k=1..8 | D/x²=(x+ky)/x, x != 0 | -kx; x² | D-kxy=2x; D-(1+kx)y=0; **C** D-kxy=x²; D-ky=-x²; D+kxy=1/x |
| q-79699 | k=5 | k=2..8 | ky²-y exp(-x)D=y, y != 0 | -k exp(x); -exp(x) | **C** D-k exp(x)y=-exp(x); D+ky=-exp(x); D-k exp(x)y=x; D+k exp(-x)y=exp(-x); D-kxy=-exp(-x) |
| q-8360 | k=2 | k=1..8 | D+ky cot x+sin(2x)=0 | k cot x; -sin(2x) | D+sin(2x)=-ky cot x; D=-ky cot x-sin(2x); ky cot x=-D-sin(2x); y=-D/(k cot x)-sin(2x)/(k cot x); **C** D+k cot(x)y=-sin(2x) |
| q-16401 | a=b=n=1 | a=1..6,b=1..4,n=1..6 | D+b²y²cos²(nx)=(a-by cos(nx))² | 2ab cos(nx); a² | **C** D+2ab cos(nx)y=a²; D+b cos(nx)y=a²-ab cos(nx); D+b²cos²(nx)y=(a-b cos(nx))²; D=a²; D+4ab cos(nx)y=a² |

These recipes reproduce every complete source bank at its original parameters. The incomplete additional field of q-16400 has the same mathematical bank, so its five options are also mapped, but its absent correct reference cannot be certified. The complete field supplies the gradable representation for generated questions.

The intention of q-16396 and q-79697's arbitrary-looking wrong equations is unresolved. Their observed whole-expression patterns are retained, and the k generalizations are explicitly hypotheses rather than recovered psychological error recipes. No bank is pooled or mixed and no inferred feedback is displayed. All generalized banks must still pass exact correctness, response-form eligibility, distinct displayed choices and native grading.

Fixed components: instructional prompt sentence; standard-form definition; x and y roles; one five-choice radio field named selection; the original template's solution sequence; the source concluding P(x), Q(x) sentence. Variable components: the expressions and coefficient/frequency slots above. Conditional components: explicit nonzero domain conditions for x, y, cos(nx), or sin(x), and P/Q annotations. No optional fields or plots are introduced.

Worked steps are the ordered stages in `data()`, with the same rearrangement, division, factor cancellation, trig identity or square expansion sequence as each source. Source prose and math-block layout are reused as masks, empty math blocks are removed, and SymPy prints expressions with normalized grouping, derivative notation and underbraces. Exact source bytes and typography are not claimed as fidelity. `review.md` puts every original beside its parameter replay and a changed instance. `validate.py` independently reads all original and generated displayed equations, including the final prose values.

Domains are essential: division by x needs x != 0; cancellation of y needs y != 0; division by cos(nx) requires cos(nx) != 0; cot(x) requires sin(x) != 0. Exponential coefficients never vanish. The generators operate on intervals in these domains. Positive coefficients avoid degenerate banks, while full bank rejection protects explicit and sampled parameters equally.
