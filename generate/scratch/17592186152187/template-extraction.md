# Four extraction stages

## 1. Specific observations

The source values, complete original prompts, solutions, fields, choices, correct values and attribute presence are retained in `source.json`. The following table maps every original to its actual oriented semiaxes, assessment and field bank. All radii are positive unequal integers; no ellipse is translated. The independent variable is θ and the domain is the half-open interval [0,2π). The requested pair is ordered x then y.

| Source | a,b | Family | Bank specifics |
|---|---|---|---|
| q-15803 | 3,5 | graph, unrated | b²/a²; a/b; √b/√a with both cos; a²/b²; b/a. Correct absent, solution absent. |
| q-15856 | 7,2 | traversal radio | swapped squared; swapped sin/cos; direct sin/cos; direct cos/sin; swapped cos/sin. Two captured fields with legacy order/notation; only second designated. |
| q-106392 | 8,3 | graph | a²/b²; b/a; a/b; b²/a²; √a/√b. |
| q-106393 | 5,3 | traversal radio | swapped squared; direct; direct sin/cos; swapped sin/cos; swapped cos/sin. |
| q-106394 | 2,6 | traversal radio | direct sin/cos; squared sin/cos; swapped cos/sin; swapped sin/cos; direct cos/sin. |
| q-106701 | 7,4 | graph, opaque bank | direct; squared; square roots; swapped squared; b/(a+1). Last operation's intention unresolved. |
| q-274855 | 6,4 | traversal blanks | field-1 is x-component only, field-2 y-component only; point A. |
| q-326267 | 2,9 | traversal blanks | same ordered component values; point J; captured whitespace retained. |
| q-6889 | 3,4 | graph | b/a; 2b/2a; a/b; 2a/2b; b²/a² with both cos. |
| q-79284 | 8,5 | traversal radio | swapped sin/cos; direct sin/cos; direct cos/sin; swapped cos/sin; swapped-squared sin/cos. |
| q-106391 | 3,6 | graph | squared; swapped sin/cos; direct; swapped-squared sin/cos; square roots. |
| q-6880 | 4,2 | graph | swapped squared; b/√b with both cos; squared; swapped; direct. |
| q-79281 | 2,4 | traversal radio | squared; swapped sin/cos; direct sin/cos; direct cos/sin; swapped cos/sin. |

In this table an unqualified pair uses cos for x and sin for y. `recipes.json` records each individual choice's complete mask, coefficient operations and actual component functions; this is the executable one-to-one map rather than a bank pooled from several originals.

## 2. Shared mathematical description

Determine horizontal radius a and vertical radius b, then construct/select x=a cos θ, y=b sin θ. Graph-only questions ask for the geometric locus; traversal questions additionally require the rightmost start, counterclockwise orientation and one traversal on the supplied full-period interval. Both sine/cosine swapped with the same oriented coefficients have the same ellipse locus but the wrong start and clockwise direction; their eligibility is checked against the actual request. The two components using cos describe a line segment, not a nondegenerate ellipse.

## 3. Components and operations

The common fixed solution introduces a,b and the general pair plus interval. Traversal versions then state the counterclockwise/rightmost-start rule. The variable prose identifies actual a,b, followed by the substituted final pair. This two-display stage sequence and all common sentences are retained. q-15803 raw replay retains absence of the entire solution; normal completion uses the graph-family common mask and is explicitly authored.

Prompt slots are the complete plot reference, horizontal radius, vertical radius and complete start-point coordinate. Solution slots are complete actual radius values in prose and final x/y coefficients. Answer slots are complete coefficient expressions only. Generic symbolic a,b and the fixed period 2π never undergo blind numeric replacement. Choices belong to their own field; blanks expect component functions without `x=` or `y=` because those symbols are supplied in the prompt. No extra distractor explanations are inserted into learner content.

All observed choice operations are normal mathematically meaningful errors (squared radii, exchanged axes, exchanged component functions, doubled radii, radii square roots or both functions equal) except q-106701's final `a+1`. That bank remains publicly replayable as opaque evidence. Normal graph banks use the other complete observed banks with defensible method operations; hard uses a separately authored complete bank: direct correct pair, exchanged axes, exchanged sine/cosine, squared radii, clockwise y sign. A normal hard blank uses the original two-component field pattern.

## 4. Reusable masks and constraints

`recipes.json` stores each observed prompt/solution/answer mask and complete profile. `generate` fills masks with exact SymPy values through the same path at source and changed parameters; there is no literal payload return or answer lookup. Original image assets are reused only for an exact raw source parameter tuple, whose geometry was individually inspected; all other tuples invoke the parameter-dependent Matplotlib renderer. Scalar coefficient normalization may render √8 as 2√2; that is reported separately from raw-string fidelity and preserves the full mathematical bank.

Normal integer semiaxes lie in 2..9; hard semiaxes lie in 2..9 in steps of 1/2 with at least one noninteger. All are positive and unequal. The complete chosen bank must contain distinct ordered component pairs with exactly one response eligible for the actual request. Explicit invalid inputs fail rather than silently change. Content identity includes the actual prompt, fixed solution, level and complete displayed bank; it is independent of seed and option order. The separate assessed-task fingerprint retains oriented axes, graph scale and actual locus/traversal/information demands, excluding notation aliases, bank/profile and layout.
