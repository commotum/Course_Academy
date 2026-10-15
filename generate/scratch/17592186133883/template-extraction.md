# Template extraction

Source basis 2602, immutable lineage recorded in source.json. Specific descriptions,
original Markdown, field identities and every original option for all 12 families
are retained in source-components.json. The following sampler is restricted to
q-41475; no other observed banks are merged into it.

The source supplies `F=<6x²-xy+11,y²+1>` on the triangle with vertices (0,0),
(2,-1), (2,1). It asks for the complete scalar line integral. The inspected source
diagram specifies counterclockwise orientation, made explicit in generated text.
There is one radio field `selection`, with five math values. The solution states
Green's theorem, shows D, rewrites F·dr in differential form, identifies P and Q,
computes partials, states the type-I region, subtracts derivatives, evaluates the
inner integral using [y], multiplies by the vertical width x, integrates x² and
evaluates the cubic antiderivative at 0 and 2. These stages remain in this order.

The generalized pattern is to evaluate circulation of a polynomial vector field
over an oriented triangle using a linear scalar curl and two exact integrals.
The answer is the entire scalar value, with no equation fragment or new fields.

| Component | Template/role | Observed | Allowed in v1 | Dependencies |
|---|---|---|---|---|
| xy coefficient | P=6x²-a·xy+11 | a=1 | integers 1..12 | P, P_y=-ax, curl ax, inner ax², antiderivative ax³/3, answer and complete bank |
| Q | y²+1 | fixed | fixed | Q_x=0 |
| Other P terms | 6x²+11 | fixed | fixed | vanish in P_y; held fixed to keep variation focused on assessed curl |
| Triangle | (0,0),(2,-1),(2,1) | fixed | fixed | bounds 0<=x<=2, -x/2<=y<=x/2; unchanged solution asset |
| Requested object | full circulation | fixed | fixed | same solution and scalar response contract |
| Field | radio, key selection | fixed | fixed | five choices, one correct |

The coefficient range and fixed-region policy are conservative sampling choices,
not inferred limitations of Green's theorem. The source does not establish that
its coordinates are mathematically essential. V1 deliberately does not declare
region/target-position slots; varying them would require coordinated new plots
and additional validation. The coefficient slot changes the actual curl and
integral, and cannot be replaced by a seed, identity or option-order change.
There are 12 mathematical tasks in the declared domain, including the source
replay; at most 11 can be novel relative to the original source bank.

All polynomials are continuously differentiable on R². The triangle has simple
closed boundary and positive area; the traversal (0,0)->(2,-1)->(2,1)->(0,0) is
counterclockwise. a>0 prevents zero-answer bank collisions. A=8a/3 follows from
integrating ax over the triangle. No conditional branches or optional stages
are needed. All signed intermediate values and exact rational forms derive
from a single instance.

One complete source profile is used in its entirety:

| Source answer UUID | Exact source value | Parameterized recipe | Designation |
|---|---|---|---|
| 5bd1f5ef-c9ed-5994-83b0-1b7bfde99771 | -2/3 | -A/4 = -2a/3 | incorrect |
| 64f04a8e-60e7-5cb7-93ee-ee43e5f4bcee | 8/3 | A = 8a/3 | correct |
| 8b0a07cf-1f8b-5b69-8fec-824801c47fec | -8/3 | -A = -8a/3 | incorrect |
| f37da209-7b24-5d10-b640-c3d7580c8d8b | -4/3 | -A/2 = -4a/3 | incorrect |
| fd217b62-f697-5f47-89d1-aa9d6c12c868 | 4/3 | A/2 = 4a/3 | incorrect |

These formulas reproduce every complete source value at a=1, with no missing or
extra options. Their ratio-preserving extension to other a is an explicit
homogeneous generalization, not an observed multi-example inference. Cognitive
interpretations of the incorrect values are unresolved; no invented error
explanations appear to learners. The whole bank is selected before constructing
its five choices. Every domain case is checked for equivalence collisions.

The remaining 11 families have their original complete banks retained verbatim
in source-components.json and no declared generator recipes in v1. Their prompt
forms, numerical properties and ordered integral operations stay separate in
classification.md. q-41811 is invalid on its supplied domain and excluded without
changing the source. Eleven other source records independently pass exact
integration, bank uniqueness and native choice grading; freshness is checked
separately using the native question pool at the current database basis.

Plot extraction: the q-41475 solution asset is
`images/00/007634ca34871f05cde9d44a58fcf24b1e5fd3b8c337c68f2025fb8724eef819.png`.
It has white background, black x/y axes, light-blue triangular fill, orange
boundary, black counterclockwise arrows, dashed guides and labels x=2,
y=x/2, y=-x/2. Scale, topology, orientation and boundary equations carry the
mathematics. It appears once between the theorem and integral rewrite. The
coefficient a has no geometric role, so the plot is reused unchanged. Its
content-addressed bytes and availability are checked by validation; the package
plot rating is none. No new plot generator is required.

Validation separates fidelity (one complete bank, four distractors), mathematics
(exact Green integration and independent three-edge parametric integration),
rendered prompt/solution consistency, and actual application grading. All 12
coefficient values are exercised, including a=1,2,12 shown side by side in
review.md. The target and region stay fixed under all coefficient changes.
