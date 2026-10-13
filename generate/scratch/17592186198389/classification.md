# Classification

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Raw source.json is an unchanged copy of the captured wrapper.

12/12 practice questions are labeled easy; 0 observed moderate and hard. All are radio selection fields with five complete mathematical options. There is one shared prompt structure, 12 field/value families and 12 observed bank patterns; the extra q-161360 field retains an equivalent bank as a separate evidence profile. Layout differences include omission of the simplified substitution row or distributed dot row and brace spelling. We retain each field family as a template so these source row omissions remain fixed.

| Source | Printed field | Graph | Rectangle | Raw fields |
|---|---|---|---|---|
| q-160887 | $⟨- y + z,\,2 y - z,\,xy⟩$ | $z=x + y$ | [0, 4, -2, 3] | 1 |
| q-161360 | $⟨x^{2},\,y^{2},\,z^{2}⟩$ | $z=x + y$ | [0, 2, 0, 2] | 2 |
| q-161358 | $⟨z,\,- y,\,2 x⟩$ | $z=3 x - 2 y$ | [0, 5, -3, 3] | 1 |
| q-161441 | $⟨x,\,y - z,\,x + y⟩$ | $z=x - 2 y$ | [0, 1, -1, 1] | 1 |
| q-161462 | $⟨z,\,y + 2 z,\,2 x - y⟩$ | $z=- x + y$ | [0, 2, -1, 2] | 1 |
| q-161381 | $⟨x + z,\,y + 2 z,\,x - 4 y⟩$ | $z=2 x - 4 y$ | [-2, 0, -1, 5] | 1 |
| q-161467 | $⟨2 x - z,\,y - z,\,y + z⟩$ | $z=4 x - y$ | [0, 2, -1, 2] | 1 |
| q-161357 | $⟨x + y,\,2 x - y,\,x + z⟩$ | $z=2 x - 2 y$ | [0, 2, -1, 2] | 1 |
| q-161359 | $⟨y z,\,x z,\,xy⟩$ | $z=x - y$ | [-1, 1, 0, 1] | 1 |
| q-161377 | $⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩$ | $z=- x - y$ | [-2, 2, -2, 2] | 1 |
| q-161379 | $⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩$ | $z=- x + y$ | [-1, 1, -3, 0] | 1 |
| q-161471 | $⟨x + z,\,2 z,\,y + z⟩$ | $z=x - 3 y$ | [-1, 2, -1, 3] | 1 |

## Plot requirement

None at every level. All practice prompts, banks and solutions contain textual mathematics, not graphs. The canonical SVG is a rendered repeated integral with a missing integrand; the original rendered section 02-step-44435.png was inspected. No geometry is present or needed in generated instances. Step 5 documents this asset, and step 7 requires no renderer.

## Curriculum and authored levels

The activity first-step is 17592186199306 (Introduction), whose next is 17592186199295 (this concrete setup KP), then 17592186199300 (formula tutorial), 17592186199299 (formula KP 17592186198392), and 17592186199282 (evaluation KP 17592186198379). This is obtained from first-step/next, not collection order. The key prerequisite is topic 4145 Calculating Flux Through Parametric Surfaces. The introductory example already takes a constant fundamental vector product and a quadratic vector field; this KP canonical example substitutes a plane into all three affine components and cancels the dot product. The next KP abstracts formulas, and the evaluation KP actually integrates. Here every question stops at the full repeated-integral integrand; no antiderivative, new theorem, coordinate-plane branch, reversed orientation, or curvilinear domain is authored.

Easy peers retain a plane, both nonzero integer slopes of magnitude 1–4, one of the 12 observed field structures of degree at most two, a whole-field integer coefficient of magnitude 1–3, and integer rectangle endpoints -3..5. The observed field structure and cancellation workload, rather than a new topic, govern variation.

Moderate is an authored assignment, with no source labels to recover: g=a x²+b y², 1<=|a|,|b|<=2; P=px x+py y and Q=qx x+qy y with px,qy in 1..3 and 1<=|py|,|qx|<=2; R=rz z+r0 with 1<=|rz|<=2 and 1<=|r0|<=2. Every peer differentiates two quadratic terms, obtains two variable tangent components, substitutes one quadratic graph into one field component, and distributes three dot terms with an integrand of degree at most two. This introduces the variable fundamental vector product already available from the parametric-surface prerequisite, while retaining the same concrete r, tangent, cross, substitution, dot, bounds sequence. It never asks the subsequent symbolic-formula KP skill.

Hard is also authored: g=a xy+b x+c y with 1<=|a|<=2 and |b|=|c|=1; F=<p z,q xy,r(x+y)> with p,q,r in 1..2. Every peer differentiates a mixed graph whose two gradient components depend on different coordinates, substitutes that graph into P, substitutes the coordinate product into Q, and multiplies it by a variable gradient. The three dot terms give degree at most three; coefficients and term counts are bounded, and no integral is evaluated. This combines the observed coordinate-product fields and concrete graph substitution with the prerequisite's variable tangent method. It adds one product contribution relative to the moderate workload, not a sequence of escalating cases within hard. Both affine graph terms are nonzero: all peers have three graph terms and two terms in each gradient. Major algebraic components never vanish.

All levels use the same rectangular endpoints -3..5, canonical ordered parametrization x=u,y=v, and upward ru cross rv. The explicit API enforces these bounds as well as the sampler. These are supported authored workload claims, not observed difficulty evidence.

## Fixed authored term workload

Moderate requires nonzero py, qx and r0 in both sampler and explicit calls. Both P/Q have two affine terms; each gradient is one variable term; R has two graph terms plus a nonzero constant after substitution. The scalar products have 2+2+3 displayed contributions before collection (seven), with possible same-degree cancellation only at final collection. Hard requires b,c=±1; its graph has three terms, each gradient has two, P substitution has three, Q is bilinear and R has two. The unsimplified three dot products distribute 6+2+2 contributions (ten) before collection. Bounds remain incidental to this setup response and are excluded from assessed-task variety counts.
