# Template and value extraction

Raw per-source records are source.json; source-components.json retains every original choice and field. Each profile is selected as a whole before values are transported. In the formulas below x is real and all trigonometric arguments use radians. Variables u and v are the two intermediate composition variables.

| Source | Specific observed function and response | Varying parameter | Complete observed bank in original order |
|---|---|---|---|
| q-48569 | cos³(3x), full derivative radio, f-prime notation | a=3, frequency | -3a cos²(ax)sin(ax); -3a cos²(x)sin(x); -3 sin²(ax); 3a sin²(ax)cos(ax); 3 cos²(ax)sin(ax) |
| q-48570 | sin³(4x), full derivative radio, f-prime notation | a=4, frequency | 3a sin²(ax)cos(ax); 3 sin²(ax)cos(ax); 3a sin²(x)cos(x); 3a sin(ax)cos(ax); 3 sin(x)cos(x) |
| q-312907 | cos⁸(5x³), blank polynomial coefficient before supplied cos⁷(5x³)sin(5x³) | a=5, positive cubic coefficient | -24a x² |
| q-2397 | sin³(9x²-1), full derivative radio | a=9, positive quadratic coefficient | 6a x sin²(ax²-1)cos(ax²-1); 3x sin²(ax²-1)cos²(ax²-1); 2a x sin²(ax²-1)cos²(ax²-1); 2a x sin²(ax²-1)cos(ax²-1); 6a x sin³(ax²-1)cos³(ax²-1) |
| q-31352 | cot((x+6)²), full derivative radio, y-prime notation | a=6, positive shift | -2(x+a)csc²((x+a)²); -csc²((x+a)²); 2x csc²((x+a)²); -2(x+a)csc(x+a); 4(x+a) |
| q-342927 | sqrt(cos(2x-1)), numerator blank in a Markdown fraction table | a=1, negative shift magnitude | -sin(2x-a), over the supplied sqrt(cos(2x-a)) |
| q-31361 | cot⁴(5x-1), derivative at x=0, radio | a=5, positive frequency | 4a cot³(1)csc²(1); a cot³(1)sec²(1); -4 cot²(1)csc²(1); 4a cot(1)sec²(1); -4 cot³(1)csc²(1) |
| q-28655 | 5^(ln(cos x)), derivative at 0, radio | a=5, replay only | 0; -1; -a; a; 1 |
| q-16699 | cos³(5x²+2), derivative at 1, no captured field | none, excluded | absent; do not invent a source bank |

These recipes reproduce every complete mathematical object at original parameters. The scalar transported constants and compound changed powers/functions are observed expression patterns, not claims about the learner's misconception. No inferred error explanation appears in learner presentation. Banks cannot be mixed. The source field key, field type, choice count and exact response fragment remain fixed.

For the six sources with solutions and fields, the repeated prose, composite-function assignments, three component derivatives, two formal chain-rule rows, substitution/product rows, final simplified derivative and point-evaluation rows are transported together. The two missing solutions are explicitly authored with the same decomposition and chain-rule progression. q-16699's source solution is retained as evidence without creating an answer field or modifying its records.

Fixed values: outer powers 3 or 8, cubic degree 3, quadratic degree 2, cotangent outer power 4, and the -1 shift in the hard cotangent profile. Variable numeric locations are transported simultaneously, including derivative factors (15 to 3a, 120 to 24a; 18 to 2a, 54 to 6a; 20 to 4a). Frequency 3 in q-48569 is replaced only in 3x, retaining the outer power and fixed -3 distractor. q-342927 transports only the full 2x-1 phase so its 1/(2 sqrt(u)) derivative and field-1 key stay intact.

Observed feature coverage: positive frequencies/coefficient/shift, negative phase shift, zero evaluation point, exact trig values at -1/1, trig-function powers, a polynomial fragment, and a fractional numerator. Sampling restricts a to integers 1..12, with easy frequency a>=2. This is deliberately narrower than the unlimited mathematical family and includes every observed eligible parameter. No unsupported sign extension is claimed. Domains: all real x for sine/cosine powers; exclude sin((x+a)²)=0 or sin(ax-1)=0 for cotangent; require cos(2x-a)>0 for square-root differentiability; require cos(x)>0 for log-cosine. Point zero is in the hard cotangent domain because sin(-1) is nonzero.

Semantically distinct tasks use the parsed function and evaluation point, ignoring seed, identity and bank order. New candidates exclude each original parameter, the replay-only zero-at-origin profile, all existing source/canonical tasks, all generated pool tasks, and all previously shown/reserved questions when counting availability. Complete-bank checks reject accidental equivalences and bank collisions before commit.
