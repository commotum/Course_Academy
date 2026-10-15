# Complete template extraction

Each original prompt, complete solution, exact fields, every answer value, original parameters, and finite slot domain appears in source-components.json. Raw API profile observed_raw returns the entire unmodified source Pull object, retaining IDs, nested enums, absence of fields, omissions, whitespace, full banks and source errors. It is ineligible for learning and requires the exact source parameters. All normal questions use simultaneous masks of whole components; source anchors have no literal replay branch. Original common sentences and ordered solution stages are present for every public parameter.

Fixed workload and variable slots:

| Family | Fixed mathematical backbone | Variable slot and dependencies |
|---|---|---|
| q-11973 | 3x²/(3x+c)², full five-choice derivative | c=3..9; affine component, cancellation constant, 6c numerator, c-scaled distractor, excluded zero -c/3 |
| q-2396 | tan(7x+b)/(4x), full five-choice derivative | b=-5..5; every tan/sec operand and trig domain; slope7 and denominator4 fixed |
| q-313362 | x³/(3x+c)², numerator fragment over supplied cube | c=1..9; all affine factors, reduced x+c factor and supplied denominator |
| q-132975 | 2t/(2t²+c)² on t>0, full derivative | c=1..9; all denominator components and 2c constant; original prompt lacked givens, restored exactly from its solution; 'from part 1' sentence repaired to explicit chain differentiation |
| q-11978 | (x+a)²/(x²+a²), full five-choice derivative | a=1..7; numerator inner shift, dependent a² denominator, every factor/expanded term/cancellation and full bank |
| q-2403 | sqrt(ln x)/(ax), full five-choice derivative | a=2..8; denominator and derivative a, intermediate a/2 divided by sqrt(ln x), square a² and every bank recipe; x>1 for derivative |
| q-313365 | (x+1)²/(x+b), numerator fragment | b=2..9; denominator shift, 2b intermediate, 2b-1 simplification, supplied square and excluded x=-b |
| q-313371 | ln x/e^(ax), numerator fragment over xe^(ax) | a=1..9; exponential inner slope, derivative factor, every intermediate product and numerator1-ax ln x; x>0 |
| q-343546 | cos(ax)/x, tangent slope at pi/2 | odd a=1,3,5,7,9; inner slope/angle, exact sine ±1, cosine0, evaluated derivative and key; evaluation point fixed because changing it changes trig workload |
| q-343576 | e^(ax)/(x+2), derivative at1 | a=1..9; inner slope, 2a-1 expansion, (3a-1)e^a/9 answer; evaluation1 fixed to preserve arithmetic workload |
| q-344143 | e^(ax²)/(x-2), polynomial fragment | a=1..9; inner a x², inner derivative2ax, expansion2ax²-4ax-1; supplied exponential factor and square remain coherent |
| authored-affine-square | (ax+b)²/x, numerator fragment over x² | a=2..5,b=1..7; inner slope a, outer slope2(ax+b), full quotient subtraction, factoring, final a²x²-b²; 28 distinct tasks |

q-2400 has no captured answer fields; q-128660 relies on undefined f and earlier parts. Their exact raw records remain available but normal generation explicitly rejects them. No source error is silently copied or repaired by broad generic rewriting.

Whole banks are selected before constructing recipes. Each radio bank retains five options as observed together; there is no pooled first-valid selection. Complete-bank collision rejects the whole instance. All originally unclear distractors remain explicitly expression-pattern recipes, without claiming a psychological interpretation. With D=(x²+a²)², q-11978 uses (a-x)²/D,2(x+a)/D,correct,2(a-x)/D,(a-2x²)/D. q-11973 uses6x/(3x+c)³,x/(3x+c)^4,correct,2x/(3x+c)^4,cx/(3x+c)^4. q-2396 uses correct,(7S-T)/(16x²),(xS+T)/(4x²),(7xS-T)/(16x²),(S-T)/(4x²), T=tan(7x+b),S=sec²(7x+b). q-2403 uses(x-a sqrt(L))/(a²x²L),(a/2-aL)/sqrt(L),(1+a sqrt(L))/(ax²sqrt(L)),correct,(L-a)/sqrt(L),L=ln x. The a/2 term is inferred from the actual intermediate quotient simplification, recovers the original1 at a2, and is varied coherently in both original matching patterns.

Correct answers are derived first by exact differentiation, then the complete bank and all components are derived from that instance. Blanks contain the fragment required by the actually displayed denominator and multiplier. Radio prompts retain no extra placeholder. Source math is separately retained from normalized course-academy-tex-v1 presentation. Fingerprints use the mathematical function, requested evaluation point, fragment/full contract and assessed expression. Seed, option order, aliases and raw/normal profiles are excluded from semantic counts.

No within-level progression, new operators, additional rules, variable powers, changed response types, new evaluation branches or new solution stages are introduced. Missing easy coverage is authored conservatively and labeled; hard retains the observed log/exponential family rather than relabeling moderate problems.
