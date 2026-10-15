# Template extraction

The source-specific components and all 50 original answer mappings are retained
in `components.json` and `source-choice-mapping.json`; `source.json` retains the
complete original prompts, banks, solutions, field layouts and diagrams.

General pattern: use additivity of an oriented vector line integral over two
pieces. One piece's integral is supplied; parametrize the missing piece,
substitute into the vector field, differentiate the parametrization, form the
dot product, integrate it exactly and add the supplied value. The response is
one numerical exact value chosen from five mathematical options.

Fixed backbone: two oriented pieces, one supplied integral, total requested
integral, the source's field monomials and curve structure, one radio field,
source-specific complete bank, and the ordered solution stages above. The
reverse-parabola profile additionally reverses orientation explicitly. The
square-root profile retains x=t, y=-sqrt(t), its derivative and half powers;
the zero endpoint is handled by the integrable limiting expression.

Variable slot `scale`: one nonzero integer k in {-8,...,-1,2,...,8}. It multiplies
both components of F, the supplied integral, every substituted vector component,
the dot product, its antiderivative, both segment values, the total and every
source-bank value. Geometry, traversal and derivative of the path stay fixed.
This is a conservative same-method generalization of observed k=1. It changes
actual field coefficients and integral data, rather than seed, identity or option
order. Zero is excluded because it collapses the bank and removes the method.
The finite bounds keep coefficients manageable. k=1 is available only for source
replay and is excluded from normal sampling and fresh candidate inventory.

Each distractor recipe is k times its complete observed exact expression. The
underlying misconception is unresolved for several source options (including
e-2 and 2+ln(3)); the generator preserves their observed expressions without
inventing feedback or asserting a psychological explanation. This scaling is
an explicitly documented extension of the complete observed profiles. Every
original distractor and complete bank must replay; every scaled option must be
distinct and exactly one option must equal the independent integral sum.

Original parameters, equations, curves, bounds, known-piece roles and source
answers are enumerated in components.json. All values and solutions are derived
from the same instance. Replay retains original wording as evidence; normal
variants preserve shared instructional sentences and operative stages with
canonical mathematical notation. Fidelity of those stages, exact bank replay,
mathematical correctness and actual engine grading are separately checked.

The requested object is always the same total integral, so no target-position
slot is declared. A controlled scale change with all geometric data fixed is
checked for stale field coefficients, supplied values, solution values and key.
New geometry, independent coefficient sampling, new operations, and easier
workloads are outside this version's capability.
