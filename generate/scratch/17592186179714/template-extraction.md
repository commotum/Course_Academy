# Gradient template extraction

The source-specific details, complete source choices, correct designations and
worked solutions are preserved verbatim in `source.json`. The exact original
parameters and one-to-one option mappings are in `source-bank-replay.json`.
The following names refer to the explicit algebraic formulas in `model()` of
`../17592186179714.py`; each branch constructs exactly one whole source bank.

The common backbone is: supply a scalar function, request its gradient field,
compute each partial derivative in x,y[,z] order, then assemble those components
against i,j[,k]. All questions have one selection radio containing five vectors.
No new derivative stages, target types, feedback or plots are introduced.
The solution retains the source's three instructional sentences, a partial
calculation block and the final vector assembly block. SymPy normalizes TeX;
source fidelity is mathematical and structural, not byte-for-byte typography.

| Template | Source function and original slots | Generalization and constraints |
|---|---|---|
| separate_roots | sqrt(2x-1)-sqrt(4y+1); a=2,b=-1,c=4,d=1 | sqrt(ax+b)-sqrt(cy+d); distinct a,c in 2..6; b,d in -3..3 |
| linear_log | ln(2x+4y); a=2,b=4 | ln(ax+by); distinct a,b in 2..6 |
| linear_tan | tan(x-2y); a=1,b=-2 | tan(ax+by); a in 1..4, b in -6..-2, b != -a |
| product_log | x ln(z-2y); a=2 | x ln(z-ay); a in 2..6 |
| radial_root | sqrt(x²+y²+z²); a=b=c=1 | sqrt(ax²+by²+cz²); a,b,c in 1..4 |
| product_sine | sin(xz+2y); a=2 | sin(xz+ay); a in 2..6 |
| product_arctan | arctan(xyz); a=1 | arctan(a xyz); a in 1..6 |
| mixed_polynomial | zx²+xy³-yz⁴; a=b=c=1 | a zx²+b xy³-c yz⁴; a,b,c in 1..4 |

These coefficient domains are conservative same-method generalizations, not
claims that all coefficients were observed. Signed shifts from the root source
are retained. Exponents, multiplication structure and variable roles stay fixed
because changing them alters the expression backbone or derivative workload.
The radial weights are positive to retain the real radial domain. Logarithms
are differentiated only on positive arguments; roots on positive radicands;
tangent where cosine is nonzero. Other functions use all of R³. Domain contracts
are recorded in each generated record. Roots exclude derivative singularities.

Each source bank contains the correct vector plus four exact distractor recipes.
All formulas, including source's compound swaps and changed denominators, are
preserved in `model()`. Their mathematical patterns are parameterized directly;
we do not claim a known cognitive interpretation for opaque compound mistakes.
For example, the log bank retains b/(x+y),a/(x+y) and a/(ax+y),1/(ax+y), rather
than replacing them with generic wrong signs. The arctan bank retains the z²
numerator in its wrong first option. The polynomial bank retains 8*y³ and
8*y*z² in its last two wrong z-components. Every recipe must remain incorrect
and every vector pair distinct at every sampled instance, or sampling fails.

All slot values are independently swept with the remaining coefficients held
at source values, excluding explicit collision constraints. Joint seeded samples
also exercise each template. Targets are fixed x,y[,z], not variable positions.
Every printed function, partial derivative row and final vector is parsed and
validated independently; changed-coefficient cases catch stale keys or prose.
Source replay compares full vectors, ignoring option order and preserving the
correct designation. No source recipe or bank is omitted.

Mathematical deduplication uses the normalized printed function, domain and
rated band; positive common scales inside logarithms are removed because those
functions differ only by a constant and have identical gradients and domains.
Seed and option order are excluded. Stable identities also include the complete
authored bank so distinct banks cannot collide under one question UUID.
No source question or learner history is modified.
