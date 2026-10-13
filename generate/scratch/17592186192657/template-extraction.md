# Template extraction

## 1. Specific original descriptions

q-170145 displays `3x - 2y =-1; 4x + y =-5`, asks for `(x,y)` using elimination, and explicitly hints to eliminate y. Multiplying the second equation by 2 gives `8x+2y=-10`; addition gives `11x=-11`; x=-1; substitution into `4x+y=-5` gives y=-1. Five math tuples are captured, with no correct designation or worked solution. All original attribute absences are retained by `profile=source_radio`.

q-238087 displays `-5x+2y=11; 7x+4y=5`, requests eliminating y and supplies two coordinate-fragment blank widgets. Multiplying first equation by -2 gives `10x-4y=-22`; addition gives `17x=-17`; x=-1; substitution into `-5x+2y=11` gives y=3. Both fields lack captured choices/correct references. The raw prompt contains an unescaped literal system brace and malformed dollar placement between widgets. The original MA 4026 source JSON confirms exactly two math-editor coordinate widgets; normal output repairs presentation, while raw profile preserves exact bytes and omissions.

Canonical e-14002 uses `5u-6v=3; -3u+2v=-5`, multiplies the second row by 3, and presents the distributed two rows, grouped retained-variable addition, collected equation, solved first coordinate, original back-substitution equation, unevaluated substituted product, evaluated product, isolated second coordinate term, division, and conclusion `(3,2)`. Shared prose and this sequence drive normal solutions. Unit +1 back coefficients omit the redundant separate division row; nonunit signed coefficients retain it.

## 2. Shared pattern

For original equations ax+by=C and cx+dy=D, select the row with the smaller-magnitude y coefficient. Scale that row only by the exact nonunit integer k that makes its y coefficient opposite the other row. Preserve order of the two equations, add their retained x terms and RHS terms, collect hx=n, divide for x, substitute into the original scaled row and solve y. The response is either the whole tuple or two separately owned scalar fragments.

## 3. Component and complete-bank mapping

At q-170145 the independently derived solution is X=-1,Y=-1. The complete opaque historical bank is parameterized by the following explicit tuple translations; these are observed numerical patterns, not recovered mistake recipes:

| Original option | Parameterized value | Original correctness evidence |
|---|---|---|
| `(-3,-4)` | `(X-2,Y-3)` | fails both-row solution criterion |
| `(5, 3)` | `(X+6,Y+4)` | fails criterion |
| `(-3, 5)` | `(X-2,Y+6)` | fails criterion |
| `(-1,-1)` | `(X,Y)` | unique solution by independent substitution; source ref absent |
| `(-1, 2)` | `(X,Y+3)` | fails criterion |

The raw source radio profile renders every offset at changed system parameters through the public generator. It preserves all five options together and their original spaces at the original parameters. It is evidence-only and ineligible for learning. q-238087 has no observed bank values; its correctly inferred fragments are X=-1 and Y=3, explicitly authored completion.

The normal `signed_substitution` complete bank is the correct tuple plus: omit scaling the scaled-row RHS before finding x then substitute that incorrect x consistently; negate the scaled-row RHS contribution before finding x then substitute; add rather than subtract A*x during back-substitution; negate the correctly computed second coordinate (signed component mistake). The normal `distribution_division` bank is the correct tuple plus: omit scaling the scaled-row x coefficient when solving for x then substitute; omit RHS scaling then substitute; add rather than subtract A*x; omit dividing the isolated second coordinate by its nonunit coefficient. Complete tuples, not isolated side values, are checked for equivalence and uniqueness. A required zero denominator or any collision rejects the whole bank/instance. There is no first-valid option pool or unrelated perturbation in normal generation.

## 4. Reusable masks and constraints

Fixed learner prose is the original radio/blank opening, elimination hint/request, and canonical coefficient-noticing, one-scaling, addition, first-coordinate and back-substitution narrative plus final conclusion. Variable slots are complete coefficients, RHS terms, products, linear equations, grouped two-term sums, coordinate fragments and complete tuples. Both scaled-row choices are supported; prose chooses first/second accordingly. Original sign/space masks are retained for public raw prompts; normal prompts render a balanced braced aligned system. Negative terms use explicit signs; substituted integer factors are grouped to prevent numeric concatenation. The only conditional stage omission is the redundant division when the original back coefficient is +1.

Sampling and explicit-input guards use the classification bounds. Both normal layouts share the complete-bank eligible parameter domain; an explicit blank call also validates its chosen profile before constructing fields, so the finite census describes the full supported normal domain. All authored levels require gcd(a,b)=gcd(c,d)=1: neither original row can reduce its nonunit eliminated coefficient through a common factor. Integer solutions are constructed, but independent QA reads the actual printed equations and solves/reinserts each correct tuple into both original equations. All distributed rows, grouped addition components/order, collected equations, unevaluated and evaluated substitution products, division rows and conclusion are read from displayed strings and verified independently. Mutation checks remove grouping or corrupt a distributed row/conclusion and must fail.

Content identity uses version, actual prompt, fixed solution, complete bank and actual difficulty; option order/seed/profile alias cannot change it. Mathematical task fingerprints canonicalize whole-equation sign/GCF and equation order, exclude banks/layout/variable notation, and retain the actual absolute collected/back division operands because these affect arithmetic workload. Large finite parameter enumeration counts task fingerprints separately from profiles. Raw missing attributes are source evidence rather than invented empty values. No plots occur in any original or variant; steps 5/7 require no renderer.

Source fidelity, presentation normalization, inferred completion, mathematical correctness and native grading are separate denominators. The missing historical correct refs cannot be matched or directly graded. No opaque historical wrong-operation intention is claimed; default banks are authored.

The nonunit collected-x guard is this KP’s narrower authored sampling policy, grounded in original coefficients 11 and 17 and canonical -4; it is not asserted as a universal prerequisite or an identical sibling workload. The sibling distinction chiefly concerns the eliminated/back coefficient and multiplier bands.
