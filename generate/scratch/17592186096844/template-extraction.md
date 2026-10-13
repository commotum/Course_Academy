# Template extraction

The full per-source components are preserved in source.json. source-components.json maps every original choice to its field, original parameters, exact mathematical value, complete bank profile, and the generated expression at those parameters. No banks are pooled. A recipe's psychological interpretation is unspecified where evidence is sparse; its observed expression is retained instead.

Common instruction: identify numerator and denominator, differentiate both with the chain rule where needed, substitute into the quotient rule, then simplify. Evaluation templates add substitution at the given point. One fixed solution is rendered per instance. Reference-parameter replays preserve source Markdown and worked solutions exactly, except q-132975's documented standalone prompt repair. Variants normalize TeX and redundant nested aligned environments, preserve instructional sentences, and show the formal rule, derivative substitution, and simplified result; evaluation variants add the source's evaluation stage. They do not invent distractor feedback. Blanks retain the original field-1 key and response fragment.

Let x be real; a,b,c,k are exact integer parameters. Proposed bounds are separate from observed values below. Scripts compute the derivative before the bank and reject complete-bank collisions. Every equation is a full derivative identity on the recorded function domain.

| Source/profile | Observed particulars | Generalized function/task | Response and constraints |
| --- | --- | --- | --- |
| q-11973 | 3x²/(3x+5)²; positive 3,3,5, common coefficient; square factors cancel | a*x²/(b*x+c)²; quotient then factor cancellation | Radio; a,b,c positive; x != -c/b |
| q-2396 | tan(7x-2)/(4x); negative inner shift; chain coefficient 7; squared 4 in distractors | tan(a*x+b)/(c*x) | Radio; signed/zero b, nonzero a,c; x != 0, cos(a*x+b) != 0 |
| q-11978 | (x+1)²/(x²+1); equal constants; chain rule in numerator | (x+a)²/(x²+a²) | Radio; positive a; real x; paired denominator constant a² is an extension |
| q-2403 | sqrt(ln x)/(2x); logarithm inside square root; derivative domain narrower than function | sqrt(ln x)/(a*x) | Radio; a positive, x > 1 |
| q-313362 | x³/(3x+5)²; table denominator (3x+5)³ | a*x³/(b*x+c)² | Numerator blank a*x²*(b*x+3c); positive a,b,c; x != -c/b |
| q-313365 | (x+1)²/(x+3); table denominator (x+3)² | (x+a)²/(x+b) | Numerator blank (x+a)(x+2b-a); signed/zero b; x != -b |
| q-344143 | e^(3x²)/(x-2); table supplies e^(3x²)/(x-2)², blank only coefficient | e^(a*x²)/(x+b) | Coefficient blank 2a*x²+2ab*x-1; signed/zero b; x != -b |
| q-343546 | cos(3x)/x at pi/2; exact sin=-1, cos=0; slope 6/pi | cos(a*x)/x at k*pi/2 | Full slope blank; a,k positive odd, k in 1,3,5 |
| q-343576 | e^(3x)/(x+2), derivative at 1 gives 8e³/9 | e^(a*x)/(x+b), at c | Full exact value blank; c+b != 0, a*c <= 12 |
| q-132975 | derivative-only prompt; solution supplies 2t/(2t²+3)²,t>0 | a*t/(b*t²+c)²,t>0; explicitly supplied function | Full derivative blank a*(c-3b*t²)/(b*t²+c)³; positive a,b,c |
| q-313371 | ln x/e^(2x); table denominator x*e^(2x) | ln(x)/e^(a*x) | Numerator blank 1-a*x*ln(x); x>0, a=1..9 |

All fields are one-field layouts. Every original answer/type is retained in generated records. Stable question UUIDs derive from the mathematical task, response shape, version and profile; field UUIDs belong to the question and answer UUIDs belong to the field. Task novelty ignores seed, identity and option order.

The full banks, with correct expression first, are:

- q-11973, L=b*x+c: [2*a*c*x/L³, 2*a*x/L³, x/L⁴, 2*x/L⁴, c*x/L⁴]. The literal coefficient 2 in the fourth expression is an observed pattern, not an inferred universal misconception. Reject c=1, c=2 and any other collision.
- q-2396, S=sec²(a*x+b), T=tan(a*x+b): [(a*x*S-T)/(c*x²), (a*S-T)/(c²*x²), (x*S+T)/(c*x²), (a*x*S-T)/(c²*x²), (S-T)/(c*x²)]. Select the entire profile; reject c=1 and any collisions.
- q-11978, D=(x²+a²)²: [2*a*(a²-x²)/D, (a-x)²/D, 2*(x+a)/D, 2*(a-x)/D, (a-2*x²)/D]. Literal 2 coefficients reproduce observed expressions; interpretation is unresolved. Varying a with denominator a² is documented as a parameter extension.
- q-2403, L=ln(x): [(1-2L)/(2*a*x²*sqrt(L)), (x-a*sqrt(L))/(a²*x²*L), (1-a*L)/sqrt(L), (1+a*sqrt(L))/(a*x²*sqrt(L)), (L-a)/sqrt(L)]. The source's scale expressions generalize directly; only the correct recipe is derived from differentiation. Their error interpretations are unresolved.

Each blank has exactly its canonical answer as a field-owned bank member, with no distractor or feedback. At the source parameters, complete mathematical banks (including correct designation) must match, ignoring order and equivalent formatting. Radio ID grading is reported separately from mathematical bank fidelity.

Bounds: a=1..9 validation, sampled a=1..7 except hard a=1..9 and odd-slope a=1,3,5,7,9; c=1..7; b in [-5,5] validation, sampled signed set {-5,-3,-2,-1,0,1,2,3,5}, or positive 1..5 for q-11973/q-313362/q-132975. Sparse source evidence motivates bounded integer sampling rather than arbitrary real coefficients. Observed negative b=-2, equal a=b=3, unit a=1, and all reference values are included; zero b is a labeled extension. Regenerate or reject collisions and singular evaluation points. The exponential evaluation family also restricts a*c <= 12: an exploratory e^63 sign-error probe was unresolved in the actual grader, so it lies outside the supported sampling policy. The bound is verified through canonical, equivalent and incorrect entries; no unresolved instance is counted as supported.

q-2400 and q-128660 remain preserved and explicitly excluded. The cubic q-313362 is mathematically consistent and supported. Missing fields and context are evidenced in classification.md, source.json and validation.json.
