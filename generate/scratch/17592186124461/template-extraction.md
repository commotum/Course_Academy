# Template extraction

## 1. Describe each observed question

The following descriptions account for every practice item, including unrated items. Full original fields/refs/options, exact number forms, formal partials and evaluated values are mapped in bank-mapping.json. Source solutions stay in source.json; original widgets for the unrated banks are in legacy-widget-evidence.json.

### q-36311 — axisquad

Find a unit normal vector to the level curve of the function $f(x, y) = 2x^{2} + 2y^{2} - y$ that passes through the point where $(x, y) = (0, 1)$.

Printed function: $2x^{2}+2y^{2}-y$. Exact point parameters: {'p': '0', 'q': '1'}. Ordered partials: ['4*x', '4*y - 1']. Evaluated gradient: ['0', '3'].

One selection radio, five math values. Original correct designation: absent; the computed normal does not retroactively create source evidence. Source prose/stages: absent.

### q-36378 — mixed

Find a unit normal vector to the level curve of the function $f(x, y) = 2x + 4y + 5xy$ that passes through the point where $(x, y) = (2, 1)$.

Printed function: $2x+4y+5xy$. Exact point parameters: {'p': '2', 'q': '1'}. Ordered partials: ['5*y + 2', '5*x + 4']. Evaluated gradient: ['7', '14'].

One selection radio, five math values. Original correct designation: absent; the computed normal does not retroactively create source evidence. Source prose/stages: absent.

### q-130271 — roots

Find a unit normal vector to the level curve of the function $f(x,y)=\sqrt{x}+2\sqrt{y}$ that passes through the point where $(x,y)=(1,4).$

Printed function: $\sqrt{x}+2\sqrt{y}$. Exact point parameters: {'p': '1', 'q': '4'}. Ordered partials: ['1/(2*sqrt(x))', '1/sqrt(y)']. Evaluated gradient: ['1/2', '1/2'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-36346 — log

Find a unit normal vector to the level curve of the function $g(x,y)=\operatorname{ln}⁡(xy)$ that passes through the point where $(x,y)=(1,1).$

Printed function: $\operatorname{ln}⁡(xy)$. Exact point parameters: {'p': '1', 'q': '1'}. Ordered partials: ['1/x', '1/y']. Evaluated gradient: ['1', '1'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-71370 — circle

Find a unit normal vector to the level curve of the function $f(x,y)={x}^{2}+{y}^{2}$ that passes through the point where $(x,y)=(-\frac{1}{2},\frac{1}{2}).$

Printed function: ${x}^{2}+{y}^{2}$. Exact point parameters: {'p': '-1/2', 'q': '1/2'}. Ordered partials: ['2*x', '2*y']. Evaluated gradient: ['-1', '1'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-71374 — bilinear

Find a unit normal vector to the level curve of the function $f(x,y)=x+3y-2xy$ that passes through the point where $(x,y)=(\frac{3}{2},1).$

Printed function: $x+3y-2xy$. Exact point parameters: {'p': '3/2', 'q': '1'}. Ordered partials: ['1 - 2*y', '3 - 2*x']. Evaluated gradient: ['-1', '0'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-71381 — exp

Find a unit normal vector to the level curve of the function $f(x,y)={e}^{x+y}+x+y$ that passes through the point where $(x,y)=(0,0).$

Printed function: ${e}^{x+y}+x+y$. Exact point parameters: {'p': '0', 'q': '0'}. Ordered partials: ['exp(x + y) + 1', 'exp(x + y) + 1']. Evaluated gradient: ['2', '2'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-129892 — quotient

Find a unit normal vector to the level curve of the function $f(x,y)=\frac{x+y}{x-y}$ that passes through the point where $(x,y)=(-2,-1).$

Printed function: $\frac{x+y}{x-y}$. Exact point parameters: {'p': '-2', 'q': '-1'}. Ordered partials: ['-2*y/(x - y)**2', '2*x/(x - y)**2']. Evaluated gradient: ['2', '-4'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-130274 — angle

Find a unit normal vector to the level curve of the function $f(x,y)=\operatorname{arctan}⁡(\frac{y}{x})$ that passes through the point where $(x,y)=(2,-2).$

Printed function: $\operatorname{arctan}⁡(\frac{y}{x})$. Exact point parameters: {'p': '2', 'q': '-2'}. Ordered partials: ['-y/(x**2 + y**2)', 'x/(x**2 + y**2)']. Evaluated gradient: ['1/4', '1/4'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

### q-71383 — radical

Find a unit normal vector to the level curve of the function $f(x,y)=\sqrt{{x}^{2}-{y}^{2}}$ that passes through the point where $(x,y)=(5,4).$

Printed function: $\sqrt{{x}^{2}-{y}^{2}}$. Exact point parameters: {'p': '5', 'q': '4'}. Ordered partials: ['x/sqrt(x**2 - y**2)', '-y/sqrt(x**2 - y**2)']. Evaluated gradient: ['5/3', '-4/3'].

One selection radio, five math values. Original correct designation: present. Source prose/stages: present, ordered partial/evaluation/normalization chains.

## 2. Generalized family pattern

For a fixed differentiable function of x and y at an admissible point, compute the ordered partial derivatives while holding the other coordinate fixed, substitute both coordinates, obtain the nonzero gradient, then divide by its Cartesian magnitude. The answer is a two-dimensional unit normal to f(x,y)=f(P). Neither slope nor a line equation nor a third coordinate is introduced.

Each source function is kept separate. All number changes preserve the formal derivative family. The exponential normal template adds authored affine coefficients c,d from 1–4: e^(x+y)+cx+dy, evaluated with x+y=0. Its four gradient rows and three normalization rows stay intact, but the partials become e^(x+y)+c and e^(x+y)+d. Unit source coefficients remain available for raw replay and normal original-parameter comparison. This yields 16 operative coefficient tasks; coordinate aliases within a coefficient pair are deduplicated. The four source formal-chain templates with quotient/chain stages (log, quotient, angle, radical) retain those stages instead of replacing them with one CAS derivative row. Equal-component factorizations in roots/angle and primitive-direction cancellation in quotient remain explicit.

## 3. Components and complete bank mappings

Every original answer is mapped one-to-one to an operation in observed_bank and its independently evaluated vector in bank-mapping.json. The source field UUID, original answer UUID/value/type, original correct ref presence and complete source profile are retained there. The bank consists of all five operations together, not a first-valid pool.

The source-bank equations below state the actual parameterized operations. a=f_x(P), b=f_y(P), U=unit(a,b), and unit(u,v)=(u,v)/sqrt(u²+v²). Constant legacy vectors are unresolved observed shapes, not evidence of the original error mechanism. Raw evidence can display these constants but normal defaults use method-derived complete banks.

- **axisquad**: 1: (0,0,-1); 2: unit(1,1); 3: U; 4: (1,0); 5: (-1,-1)

- **mixed**: 1: (a,-(b-2)) [opaque]; 2: (a,a); 3: U; 4: (1,-4) [opaque]; 5: unit(b,a)

- **roots**: 1: U; 2: unit(a,2b); 3: unit(a,-b); 4: (0,-1); 5: unit(a,b/2)

- **log**: 1: unit(a,-b); 2: (a,b); 3: sqrt(3)(a,b) [opaque]; 4: sqrt(3)/2(a,-b) [opaque]; 5: U

- **circle**: 1: unit(a,-b); 2: (1,0); 3: U; 4: (a,b)/(|a|+|b|); 5: (0,-1)

- **bilinear**: 1: (0,-1); 2: (2,0) [repeated basis]; 3: (0,0) [cancel basis]; 4: U; 5: (-1/sqrt(5),0) [opaque repeated basis]

- **exp**: 1: (a,-b)/(|a|+|b|); 2: (1,0); 3: (0,1); 4: unit(a,-b); 5: U

- **quotient**: 1: unit(-b,a); 2: U; 3: (0,1/sqrt(5)) [opaque repeated j]; 4: unit(1,-1); 5: unit(a,-b)

- **angle**: 1: (1,-1) [fixed primitive]; 2: unit(-a,b); 3: U; 4: (1,1) [fixed primitive]; 5: unit(a,-b)

- **radical**: 1: unit(a,-b); 2: (1,0); 3: unit(1,1); 4: (0,1); 5: U

The earlier suspicion of ambiguity in q-130274 was disproved by parsing the whole vector: (-i+j)/sqrt(2) is tangent to its level curve, while the correct unit normal is (i+j)/sqrt(2). Only one source option is admissible. No mathematical repair is needed for this bank.

## 4. Reusable templates, slots and constraints

Fixed components are the printed source function (except authored affine coefficients in exp), function name (g only for log), shared introductory and normalization prose, formal derivative stages and source field shape. Complete point tuples, complete substituted operands, intermediate vectors, primitive-direction factor, magnitude and final normalized vector are variable slots. Numeric factors are grouped to prevent implicit multiplication from concatenating digits or bare signed operations. Source prose is masked only outside display blocks, and every changed point/normalization introduction is checked against the printed prompt.

solution_blocks contains separate ordered per-family formal and evaluated masks. The source-specific row counts are maintained at original parameters. A bilinear axis question has the source one-row normalization; a changed nonaxis bilinear instance adds explicit magnitude and final rows, a documented necessary extension rather than an unreported source-stage replacement.

The source banks are public observed-q-N profiles, marked evidence_only=true and eligible_for_learning=false. Their values are computed by operation recipes; no literal source-question or correct-answer lookup is used. Source typography is normalized in rendered vectors and math blocks; fidelity reports distinguish byte-exact prompt/prose from algebraic bank matches and source stage sequence.

### Authored normal banks

method-generic selects all five: U; one partial sign flipped then normalized; swapped ordered partials (only when unequal magnitudes); unnormalized gradient; gradient divided by its L1 magnitude. Balanced components use U, flipped partial, L1 normalization, division by squared magnitude, and a held-y-zero partial. method-balanced substitutes the actual unnormalized gradient for squared-magnitude normalization where equal components would collide.

method-axis selects U, swapped normal components, unnormalized gradient, division by squared magnitude, and swapped unnormalized gradient. It requires component magnitude greater than one. method-bilinear-axis selects U, x partial with its constant omitted (-2q,0), swapped normal, mixed-term partials omitted unit(1,3), and exchanged substitution coordinates unit(1-2p,3-2q). This serves the original (-1,0) gradient without introducing duplicated normalized/unnormalized choices. Each is a complete operation bank chosen before parameters; any collision, second valid unit normal, undefined member or out-of-plane member rejects the whole normal instance.

### Equal-level workload bounds

**Easy**: ten observed families; integer-substitution families (axisquad, mixed, log, quotient, angle, exp) use integers bounded by four; circle and bilinear use halves bounded by four. Roots and radical are bounded by sixteen. Roots use familiar positive integer squares 1,4,9,16; radical points use perfect-square differences. log requires xy>0; quotient requires x≠y; angle requires x≠0; radical requires x²>y². exp evaluates x+y=0, retaining its source normalization sequence and using authored affine coefficients 1–4. Its coordinate aliases count as one assessed task per coefficient pair (16 coefficient pairs), rather than nine different numerical tasks. The integer-coordinate easy families and at-most-one-fractional-coordinate bilinear family cannot accept the authored moderate/hard workload inputs.

**Moderate, authored absent level**: canonical weighted quadratic, mixed linear/product and bilinear functions. Both coordinates are opposite-sign nonintegral halves with absolute value at most four; both affine partials are substituted, with two nonzero unequal components. This raises substitution bookkeeping within the canonical method, without claiming a recovered source label.

**Hard, authored absent level**: roots, quotient, angle and radical source methods; two nonintegral rational coordinates. Quotient, angle and radical use denominators 2–4 and absolute values at most eight; roots use squared halves/thirds with reduced coordinate denominators 4 or 9 and absolute values at most sixteen. Both families use familiar rational square roots where applicable; nonzero unequal rational gradient components and at least one nonunit gradient denominator before clearing the common scalar. This imposes two rational substitutions and denominator clearing while using only already-observed derivative methods. It adds neither level surfaces nor normal lines.

The moderate and hard eligibility guards are shared by explicit calls and sampling. Hard roots are squares of familiar halves and thirds (root numerators 1–11, roots bounded by four); hard radical pairs come from the declared small Pythagorean triple catalog divided by 2–4; explicit inputs must belong to that same catalog. The easy radical sampler enumerates every integral perfect-square-difference pair within its stated bounds. No arbitrary new differentiation branch is added.

### Evidence limits and minimal repairs

q-36311 retains an out-of-plane -k wrong option only in raw evidence. q-71374 retains its zero and repeated-basis wrong vectors only as evidence. Opaque source shapes are not promoted to learner defaults. The two unrated items omit missing keys in public raw replay; normal records supply independently verified correct designation, easy design assignment and canonical-method solution, explicitly authored. No source correct-ref match is claimed for these two items. No TeX escape repair is made: decoded source values contain no adjacent doubled backslashes.
