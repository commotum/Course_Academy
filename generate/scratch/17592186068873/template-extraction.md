# Four extraction stages

## 1. Specific sources

The exact source prompt, full worked prose/rows (or its absence), original field ordering/types, every option and original key/label presence are in source.json. source-cases.json gives all8 parameterized public API replays, including the three unrated sources. review.md renders raw originals alongside explicitly completed originals and changed-input variants; review.json contains their full local records.

| Source | Variable/base/outer | Form | Fields | Observed solution sequence |
|---|---|---|---|---|
| q140186 | x/3/-2 | numerical9 | radio5 | absent |
| q140271 | y/2/+1 | supplied2² | radio5 | absent |
| q250399 | x/3/-2 | supplied3² | blank field2,field1 | absent |
| q141513 | y/6/-3 | supplied6² | radio5 | identity; input; product2·6y; binomial square; full input; result |
| q250392 | x/7/+1 | numerical49 | blank field1,field2 | identity; input; product2·7x with7²; binomial square; full input; result |
| q250395 | x/6/+4 | supplied6² | blank field2,field1 | identity; input; product2·6x; binomial square; full input; spaced binomial result |
| q250396 | y/10/+7 | supplied10² | blank field1,field2 | identity; input; product2·10y; binomial square; full input; result |
| q250397 | x/2/-3 | numerical4 | blank field2,field1 | identity; input; rewrite4 as2²; product2·2x; binomial square; full input; result |

## 2. Shared pattern

Rewrite (v²+2av+a²)±k as (v+a)²±k, with a,k positive familiar integers. The isolated inner trinomial is already a perfect square. The source fixed prose recalls v²+2av+a²=(v+a)², identifies the square in parentheses, factors it through the displayed2·a product and concludes by retaining the outside constant. Each observed chain's row omissions/spacing remain fixed; a numerical constant does not automatically license inserting a redundant square-base row into a family that omits it.

## 3. Components and complete banks

For each radio profile, all options have the same outside ±k and squared form; below lists the ordered source binomial shifts, not just selected correct values. Formula a denotes the positive half-linear coefficient. The correct item is a.

| Original profile | Every original shift → recipe |
|---|---|
| q140186, a3 | +3→a; -3→-a; +6→2a; +9→a²; -6→-2a |
| q140271, a2 | +4→2a; +8→4a; +2→a; -4→-2a; -2→-a |
| q141513, a6 | +4→a-2; -3→-a/2; +3→a/2; -6→-a; +6→a |

The first two banks use the half coefficient, its sign, the full linear coefficient, doubled coefficient or square constant as binomial shift. These are expression-pattern reconstructions, not proof of historical author intent. In q141513 the +4 choice has no defensible single-source error operation: a-2 is an explicitly opaque affine pattern for public evidence replay only. Its complete historical bank, including otherwise interpretable half/sign choices, stays evidence-only in raw and completed source profiles. It is never a normal default.

Normal radio defaults use the separately authored complete bank [a,-a,2a,a/2,-2a], representing correct half coefficient, sign reversal, full linear coefficient, halving twice and full coefficient with reversed sign. Every recipe arises from the printed factoring method. All five choices are built together and rejected together on equality/collision; no first-valid replacement. Source profile q140186 collides at a1 and q141513 at a4; those whole-instance explicit calls reject rather than alter the historical profile. Original anchors remain valid.

Each blank has a single fragment v+a for field1 and k for field2. Its supplied sign is part of the printed response criterion. Raw q250399 has neither bank nor key; completed profiles explicitly author these exact fragments. q140186/q140271 missing keys are also explicitly inferred, not counted as matched original designations. There are23 captured options (15 radio and8 blank) and9 captured correct designations; the remaining keys were never present in this snapshot.

## 4. Reusable masks and constraints

The script compiles each source's complete math-region components into variable/half-coefficient/linear-coefficient/square/outside-constant slots. A literal exponent2 and the factor2 in the identity/product remain fixed. The outside constant slot is captured after the closing isolated-expression or binomial-square component, preventing equal scalar spellings from corrupting another operand. Math-only variable substitution handles implicit a·v and preserves prose and TeX commands. This is a parameterized source family, not a literal-payload branch or answer lookup.

At the original parameters, prompts/available solutions and option values replay byte-exactly. At changed parameters, each displayed row is independently parsed and checked against the actual input polynomial. Fixed factoring operands (2, half coefficient, its square, binomial), outside constant and fragment answers are checked individually. Structural assertions reject replacing the product stage by an algebraically equal collected polynomial, even when the final answer still works. Source prose and full row sequence are checked independently against family masks. Formatting rejects unintended C0 controls, unmatched math delimiters, braces and signed concatenations.

No source mathematical/TeX repair was necessary. Missing attributes are retained as raw evidence and authored only in completed/normal profiles. All normal fields have placeholders when blank; no plots/renderer/cache are needed. No database operation occurs.
