# Template extraction

## 1. Describe each source

All original prompts, banks and complete worked solutions are retained in source.json and shown under Original labels in review.md. The following extraction inventories the actual three component argument slots and every bank member, rather than a scalar correct-answer lookup. Easy requests a scalar divergence field; moderate requests exact evaluation after coordinate differentiation. Basis-vector and tuple notation are kept source-specific. The two incomplete blanks retain their raw prompt as evidence.

The reusable evidence parameter is a nonzero integer scale c, |c|<=3. Each whole printed component is multiplied by c, each formal derivative argument is multiplied by c, and each subsequent complete scalar arithmetic row is multiplied by c. At c=1 the coefficient renderer has its ordinary multiplicative-identity behavior, restoring all source strings exactly. There is no branch returning a source question payload.

## 2. Generalized mathematical pattern

For F=(P,Q,R), compute Px+Qy+Rz, holding the other coordinates fixed. Where a point is requested, first produce the divergence field, then substitute all three coordinates into every factor. Source row counts and prose are captured as masks. Correct and incorrect complete mathematical objects are owned by their field. Scalar-versus-vector wrong options are preserved.

## 3. Components and complete bank mapping

The bank-preservation operation for member A_j is c*A_j. This is an explicit expression operation under uniformly scaled components, not evidence of a specific original student error. In particular, the numerical moderate choices do not determine unique omission/sign/arithmetic recipes. All observed profiles are conservatively classified observed_opaque, evidence only, and excluded from normal learner sampling. Authored defaults have independent method-derived error operations below.

### q-105555 — easy

Formal component arguments: $\operatorname{ln}⁡(xy)$, $-y\operatorname{cos}⁡x$, $y{z}^{3}$.

Bank profile: `observed_q-105555`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}$ | $c\left(\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}\right)$ | Correct |

| 2 | $\frac{1}{x}+\operatorname{sin}⁡x+3y{z}^{2}$ | $c\left(\frac{1}{x}+\operatorname{sin}⁡x+3y{z}^{2}\right)$ | Incorrect; intent unresolved |

| 3 | $\frac{1}{xy}-\operatorname{cos}⁡x+{z}^{3}$ | $c\left(\frac{1}{xy}-\operatorname{cos}⁡x+{z}^{3}\right)$ | Incorrect; intent unresolved |

| 4 | $\frac{1}{xy}\,i-\operatorname{cos}⁡x\,j+{z}^{3}\,k$ | $c\left(\frac{1}{xy}\,i-\operatorname{cos}⁡x\,j+{z}^{3}\,k\right)$ | Incorrect; intent unresolved |

| 5 | $\frac{1}{y}\,i-\operatorname{sin}⁡x\,j+3y{z}^{2}\,k$ | $c\left(\frac{1}{y}\,i-\operatorname{sin}⁡x\,j+3y{z}^{2}\,k\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}$ → $c\left(\frac{1}{x}-\operatorname{cos}⁡x+3y{z}^{2}\right)$

### q-41839 — moderate

Formal component arguments: $xyz$, ${e}^{-y}\operatorname{cos}⁡\pi x$, ${e}^{-y}\operatorname{sin}⁡\pi z+2xz$.

Bank profile: `observed_q-41839`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $1$ | $c\left(1\right)$ | Incorrect; intent unresolved |

| 2 | $1-\pi $ | $c\left(1-\pi \right)$ | Incorrect; intent unresolved |

| 3 | $3-\pi $ | $c\left(3-\pi \right)$ | Incorrect; intent unresolved |

| 4 | $\pi +1$ | $c\left(\pi +1\right)$ | Incorrect; intent unresolved |

| 5 | $\pi +3$ | $c\left(\pi +3\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $yz-{e}^{-y}\operatorname{cos}⁡\pi x+\pi {e}^{-y}\operatorname{cos}⁡\pi z+2x$ → $c\left(yz-{e}^{-y}\operatorname{cos}⁡\pi x+\pi {e}^{-y}\operatorname{cos}⁡\pi z+2x\right)$

- `S1`: $(0)(0)-{e}^{0}\operatorname{cos}⁡\pi +\pi {e}^{0}\operatorname{cos}⁡0+2(1)$ → $c\left((0)(0)-{e}^{0}\operatorname{cos}⁡\pi +\pi {e}^{0}\operatorname{cos}⁡0+2(1)\right)$

- `S2`: $0-(-1)+\pi (1)+2$ → $c\left(0-(-1)+\pi (1)+2\right)$

- `S3`: $1+\pi +2$ → $c\left(1+\pi +2\right)$

- `S4`: $\pi +3$ → $c\left(\pi +3\right)$

### q-168615 — easy

Formal component arguments: ${z}^{2}$, $2xy$, $x{y}^{2}$.

Bank profile: `observed_q-168615`; 1 options; type `:answer-field.type/blank`; key `field-1`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $2x$ | $c\left(2x\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $0+2x+0$ → $c\left(0+2x+0\right)$

- `S1`: $2x$ → $c\left(2x\right)$

### q-123176 — easy

Formal component arguments: ${e}^{x}\operatorname{sin}⁡yz$, $xyz$, $2$.

Bank profile: `observed_q-123176`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | ${e}^{x}\operatorname{cos}⁡yz+xz$ | $c\left({e}^{x}\operatorname{cos}⁡yz+xz\right)$ | Incorrect; intent unresolved |

| 2 | ${e}^{x}\operatorname{cos}⁡yz$ | $c\left({e}^{x}\operatorname{cos}⁡yz\right)$ | Incorrect; intent unresolved |

| 3 | ${e}^{x}\operatorname{cos}⁡yz+xz+2$ | $c\left({e}^{x}\operatorname{cos}⁡yz+xz+2\right)$ | Incorrect; intent unresolved |

| 4 | ${e}^{x}\operatorname{sin}⁡yz+xyz+2$ | $c\left({e}^{x}\operatorname{sin}⁡yz+xyz+2\right)$ | Incorrect; intent unresolved |

| 5 | ${e}^{x}\operatorname{sin}⁡yz+xz$ | $c\left({e}^{x}\operatorname{sin}⁡yz+xz\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: ${e}^{x}\operatorname{sin}⁡yz+xz$ → $c\left({e}^{x}\operatorname{sin}⁡yz+xz\right)$

### q-123179 — easy

Formal component arguments: $(2x+3y-4z)^{2}$, $(2x+3y-4z)^{2}$, $(2x+3y-4z)^{2}$.

Bank profile: `observed_q-123179`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $6x+9y-12z$ | $c\left(6x+9y-12z\right)$ | Incorrect; intent unresolved |

| 2 | $4x+6y-8z$ | $c\left(4x+6y-8z\right)$ | Correct |

| 3 | $8x+12y-16z$ | $c\left(8x+12y-16z\right)$ | Incorrect; intent unresolved |

| 4 | $(2x+3y-4z)^{2}$ | $c\left((2x+3y-4z)^{2}\right)$ | Incorrect; intent unresolved |

| 5 | $x+2y-4z$ | $c\left(x+2y-4z\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $4(2x+3y-4z)+6(2x+3y-4z)-8(2x+3y-4z)$ → $c\left(4(2x+3y-4z)+6(2x+3y-4z)-8(2x+3y-4z)\right)$

- `S1`: $2(2x+3y-4z)$ → $c\left(2(2x+3y-4z)\right)$

- `S2`: $4x+6y-8z$ → $c\left(4x+6y-8z\right)$

### q-123200 — moderate

Formal component arguments: $(x-y)^{3}$, $(y+z)^{3}$, $(x+z)^{3}$.

Bank profile: `observed_q-123200`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $144$ | $c\left(144\right)$ | Incorrect; intent unresolved |

| 2 | $76$ | $c\left(76\right)$ | Incorrect; intent unresolved |

| 3 | $48$ | $c\left(48\right)$ | Incorrect; intent unresolved |

| 4 | $96$ | $c\left(96\right)$ | Correct |

| 5 | $84$ | $c\left(84\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $3(x-y)^{2}+3(y+z)^{2}+3(x+z)^{2}$ → $c\left(3(x-y)^{2}+3(y+z)^{2}+3(x+z)^{2}\right)$

- `S1`: $3((-2)-(2))^{2}+3((2)+(2))^{2}+3((-2)+(2))^{2}$ → $c\left(3((-2)-(2))^{2}+3((2)+(2))^{2}+3((-2)+(2))^{2}\right)$

- `S2`: $3(-4)^{2}+3(4)^{2}+3(0)^{2}$ → $c\left(3(-4)^{2}+3(4)^{2}+3(0)^{2}\right)$

- `S3`: $96$ → $c\left(96\right)$

### q-131176 — easy

Formal component arguments: $2xy{z}^{2}$, $x{e}^{y}$, $y{z}^{3}$.

Bank profile: `observed_q-131176`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $xy{z}^{2}+xz$ | $c\left(xy{z}^{2}+xz\right)$ | Incorrect; intent unresolved |

| 2 | $y{z}^{2}+xy{e}^{y}$ | $c\left(y{z}^{2}+xy{e}^{y}\right)$ | Incorrect; intent unresolved |

| 3 | $5y{z}^{2}+x{e}^{y}$ | $c\left(5y{z}^{2}+x{e}^{y}\right)$ | Correct |

| 4 | $y{z}^{2}+xy+y$ | $c\left(y{z}^{2}+xy+y\right)$ | Incorrect; intent unresolved |

| 5 | $x+{e}^{y}+{z}^{2}$ | $c\left(x+{e}^{y}+{z}^{2}\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $2y{z}^{2}+x{e}^{y}+3y{z}^{2}$ → $c\left(2y{z}^{2}+x{e}^{y}+3y{z}^{2}\right)$

- `S1`: $5y{z}^{2}+x{e}^{y}$ → $c\left(5y{z}^{2}+x{e}^{y}\right)$

### q-131178 — moderate

Formal component arguments: $xz\operatorname{cos}⁡y$, $y{x}^{2}$, $x{z}^{2}{e}^{y}$.

Bank profile: `observed_q-131178`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $-5$ | $c\left(-5\right)$ | Correct |

| 2 | $4$ | $c\left(4\right)$ | Incorrect; intent unresolved |

| 3 | $-2$ | $c\left(-2\right)$ | Incorrect; intent unresolved |

| 4 | $3$ | $c\left(3\right)$ | Incorrect; intent unresolved |

| 5 | $0$ | $c\left(0\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $z\operatorname{cos}⁡y+{x}^{2}+2xz{e}^{y}$ → $c\left(z\operatorname{cos}⁡y+{x}^{2}+2xz{e}^{y}\right)$

- `S1`: $(-2)\cdot \operatorname{cos}⁡0+{1}^{2}+2\cdot 1\cdot (-2)\cdot {e}^{0}$ → $c\left((-2)\cdot \operatorname{cos}⁡0+{1}^{2}+2\cdot 1\cdot (-2)\cdot {e}^{0}\right)$

- `S2`: $-2+1-4$ → $c\left(-2+1-4\right)$

- `S3`: $-5$ → $c\left(-5\right)$

### q-131179 — moderate

Formal component arguments: $x(y{e}^{z}+\operatorname{ln}⁡y)$, $xy{e}^{z}$, $z(x+1)$.

Bank profile: `observed_q-131179`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $0$ | $c\left(0\right)$ | Incorrect; intent unresolved |

| 2 | $2$ | $c\left(2\right)$ | Incorrect; intent unresolved |

| 3 | $3$ | $c\left(3\right)$ | Incorrect; intent unresolved |

| 4 | $6$ | $c\left(6\right)$ | Incorrect; intent unresolved |

| 5 | $4$ | $c\left(4\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $(y{e}^{z}+\operatorname{ln}⁡y)+x{e}^{z}+(x+1)$ → $c\left((y{e}^{z}+\operatorname{ln}⁡y)+x{e}^{z}+(x+1)\right)$

- `S1`: $y{e}^{z}+\operatorname{ln}⁡y+x{e}^{z}+x+1$ → $c\left(y{e}^{z}+\operatorname{ln}⁡y+x{e}^{z}+x+1\right)$

- `S2`: $1\cdot {e}^{0}+\operatorname{ln}⁡1+1\cdot {e}^{0}+1+1$ → $c\left(1\cdot {e}^{0}+\operatorname{ln}⁡1+1\cdot {e}^{0}+1+1\right)$

- `S3`: $1+0+1+1+1$ → $c\left(1+0+1+1+1\right)$

- `S4`: $4$ → $c\left(4\right)$

### q-168624 — easy

Formal component arguments: $0$, $0$, $-xy-2{z}^{2}$.

Bank profile: `observed_q-168624`; 1 options; type `:answer-field.type/blank`; key `field-1`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $-4z$ | $c\left(-4z\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $-4z$ → $c\left(-4z\right)$

### q-123192 — moderate

Formal component arguments: ${x}^{2}yz$, $x{y}^{2}z$, $xy{z}^{2}$.

Bank profile: `observed_q-123192`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $20$ | $c\left(20\right)$ | Incorrect; intent unresolved |

| 2 | $16$ | $c\left(16\right)$ | Incorrect; intent unresolved |

| 3 | $32$ | $c\left(32\right)$ | Incorrect; intent unresolved |

| 4 | $18$ | $c\left(18\right)$ | Incorrect; intent unresolved |

| 5 | $24$ | $c\left(24\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $2xyz+2xyz+2xyz$ → $c\left(2xyz+2xyz+2xyz\right)$

- `S1`: $6xyz$ → $c\left(6xyz\right)$

- `S2`: $6(1)(2)(2)$ → $c\left(6(1)(2)(2)\right)$

- `S3`: $6\cdot 4$ → $c\left(6\cdot 4\right)$

- `S4`: $24$ → $c\left(24\right)$

### q-41837 — easy

Formal component arguments: ${e}^{xz}\operatorname{cos}⁡y$, $0$, $\operatorname{ln}⁡yz$.

Bank profile: `observed_q-41837`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $z{e}^{xz}\operatorname{sin}⁡y-\frac{1}{z}$ | $c\left(z{e}^{xz}\operatorname{sin}⁡y-\frac{1}{z}\right)$ | Incorrect; intent unresolved |

| 2 | $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{{y}^{2}z}$ | $c\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{{y}^{2}z}\right)$ | Incorrect; intent unresolved |

| 3 | $z{e}^{xz}\operatorname{cos}⁡y-{e}^{xy}\operatorname{sin}⁡y+\frac{1}{z}$ | $c\left(z{e}^{xz}\operatorname{cos}⁡y-{e}^{xy}\operatorname{sin}⁡y+\frac{1}{z}\right)$ | Incorrect; intent unresolved |

| 4 | $xz{e}^{xz}\operatorname{cos}⁡y+\frac{1}{yz}$ | $c\left(xz{e}^{xz}\operatorname{cos}⁡y+\frac{1}{yz}\right)$ | Incorrect; intent unresolved |

| 5 | $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}$ | $c\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}\right)$ | Correct |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}$ → $c\left(z{e}^{xz}\operatorname{cos}⁡y+\frac{1}{z}\right)$

### q-105559 — moderate

Formal component arguments: $\operatorname{cos}⁡\pi x$, $y\operatorname{sin}⁡\pi y$, ${e}^{2z}$.

Bank profile: `observed_q-105559`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $2-\pi $ | $c\left(2-\pi \right)$ | Correct |

| 2 | $\pi $ | $c\left(\pi \right)$ | Incorrect; intent unresolved |

| 3 | $-\pi $ | $c\left(-\pi \right)$ | Incorrect; intent unresolved |

| 4 | $3-\pi $ | $c\left(3-\pi \right)$ | Incorrect; intent unresolved |

| 5 | $1+\pi $ | $c\left(1+\pi \right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $-\pi \operatorname{sin}⁡\pi x+\operatorname{sin}⁡\pi y+\pi y\operatorname{cos}⁡\pi y+2{e}^{2z}$ → $c\left(-\pi \operatorname{sin}⁡\pi x+\operatorname{sin}⁡\pi y+\pi y\operatorname{cos}⁡\pi y+2{e}^{2z}\right)$

- `S1`: $-\pi \operatorname{sin}⁡(0)+\operatorname{sin}⁡(\pi )+\pi \operatorname{cos}⁡(\pi )+2{e}^{0}$ → $c\left(-\pi \operatorname{sin}⁡(0)+\operatorname{sin}⁡(\pi )+\pi \operatorname{cos}⁡(\pi )+2{e}^{0}\right)$

- `S2`: $0+0-\pi +2$ → $c\left(0+0-\pi +2\right)$

- `S3`: $2-\pi $ → $c\left(2-\pi \right)$

### q-123196 — moderate

Formal component arguments: $(x+y)^{2}$, $(y+z)^{2}$, $(x+z)^{2}$.

Bank profile: `observed_q-123196`; 5 options; type `:answer-field.type/radio`; key `selection`.

| Member | Original complete expression A_j | Parameterized recipe | Original designation |

|---|---|---|---|

| 1 | $-6$ | $c\left(-6\right)$ | Incorrect; intent unresolved |

| 2 | $-8$ | $c\left(-8\right)$ | Correct |

| 3 | $-4$ | $c\left(-4\right)$ | Incorrect; intent unresolved |

| 4 | $10$ | $c\left(10\right)$ | Incorrect; intent unresolved |

| 5 | $4$ | $c\left(4\right)$ | Incorrect; intent unresolved |

Ordered scalar stage slots (each kept separately from formal operator rows):

- `S0`: $2(x+y)+2(y+z)+2(x+z)$ → $c\left(2(x+y)+2(y+z)+2(x+z)\right)$

- `S1`: $4(x+y+z)$ → $c\left(4(x+y+z)\right)$

- `S2`: $4((-2)+(1)+(-1))$ → $c\left(4((-2)+(1)+(-1))\right)$

- `S3`: $4\cdot (-2)$ → $c\left(4\cdot (-2)\right)$

- `S4`: $-8$ → $c\left(-8\right)$

## 4. Reusable templates, constraints and authored extension

Fixed: every original teaching sentence, ordered equality-row sequence, operators, coordinate identities, response shape, source point, and baseline complete observed bank. Variable: complete component scale c. Conditional: multiplication by unity is omitted; a negative coefficient is grouped; a negative displayed component whose original sign supplied the separator receives an explicit separator when scaled. Mask construction operates on complete component spans before replacement, so a basis label, function argument or coordinate tuple is never changed by a short global substring replacement.

Normal authored templates use a,b,c in {-3,-2,-1,1,2,3}, enforced on explicit calls and sampling. Symbolic components and derivative expressions are canonicalized, dropping additive terms constant in their differentiated coordinate. Bank/profile, answer layout, seed and option order do not enter the mathematical fingerprint. Moderate point aliases merge when actual canonical fields, derivative tasks and independently evaluated derivative contribution tuples agree. Different fields that merely share a final scalar remain distinct tasks. Full content identity contains version, displayed prompt, complete fixed solution, type, difficulty and complete bank values.

Authored easy exp_sine differentiates exp(ax) with a held yz trig factor, xyz, and a constant; monomial differentiates three simple monomial/exp components; shared_square applies three linear chain factors before collection and rejects a+b+c=0. These preserve the observed easy families and two/three substantive derivative contributions.

Authored moderate evaluated_monomial, evaluated_square and evaluated_exp_trig perform the same three coordinate derivatives then small exact substitution. Point coordinates are integers with magnitude <=2. Monomial coordinates and square arguments must be nonzero. Exponential/trig evaluation has y=0 and nonzero x,z, keeping e^0 and cos(0) familiar. No arbitrary transcendental numerical evaluation is added.

Authored hard product_exp and product_log each require six substantive derivative summands: a two-term product/chain derivative for each of P,Q,R. Powers are at most two; integer coefficient magnitudes <=3; hard is symbolic to avoid unrelated arithmetic difficulty. product_log restricts 2+xz>0. Both families demand equal workload and have no internal progression. Their use of product and chain rules is grounded in observed easy shared affine squares, observed moderate y sin(pi y) product/chain differentiation, the canonical 3D example, and prerequisite Partial Differentiability of Multivariable Functions. Hard is a supported design claim, not an observed source label.

Ordered lesson route (followed via activity/first-step and step/next, never collection order): Introduction → Some Important Notes About the Divergence of a Vector Field → Finding the Divergence of a Vector Field in Two Dimensions → Finding the Divergence of a Vector Field in Three Dimensions → Physical Interpretation of Divergence → Examples of Vector Field With Divergence and Solenoidal Vector Fields → Interpreting Divergence. The preceding Visualizing Vector Fields and Partial Differentiability topics establish the objects and held-coordinate derivatives. The later Properties of the Divergence Operator and Green’s Theorem are excluded: there are no flux integrals, curl, theorem applications or conceptual sink/source tasks in these generators.

Authored radio bank is selected before parameters. With three nonzero derivatives Dp,Dq,Dr, it contains D, D-Dp, D-Dq, D-Dr, -D. The two-derivative constant-component family contains D, Dp, Dq, -Dp+Dq, D+R. At a point, each complete expression is evaluated there. Any equality, correct distractor, zero-divergence negation collision or missing member rejects the whole parameter tuple; no first-valid pool is used. Authored blank has one verified expression and no distractor bank. Raw observed banks never silently replace these operations.

Plot extraction/specification: none. No source prompt, answer, or solution for this KP contains a plot or image. The neighboring interpretation KP’s diagrams do not belong to this KP and are not imported.
