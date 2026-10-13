# Template extraction

## Stage 1: specific source descriptions

Every source has one five-option math radio field. Equations use Leibniz derivative notation and complete equality values. Correct values are not equation fragments. All original fields, UUIDs, values and sentences remain in source.json. The detailed table below accounts for every option in its actual observed bank; the normalized y′ flow is exact, not a hypothesis about a learner error.

### q-103560 — moderate

Which of the following is **NOT** a first order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}-(\operatorname{tan}⁡x)y=\operatorname{sec}⁡x$ | other choice | Linear after local normalization: y′ = `y*tan(x) + sec(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $x\frac{\text{d}y}{\text{d}x}-{x}^{2}y=x\operatorname{sin}⁡x$ | other choice | Linear after local normalization: y′ = `x*y + sin(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $2\frac{\text{d}y}{\text{d}x}-4xy=\sqrt{x}$ | other choice | Linear after local normalization: y′ = `sqrt(x)/2 + 2*x*y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-{x}^{2}=\frac{1}{1-y}$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-\frac{{e}^{x}}{x}y={x}^{3}$ | other choice | Linear after local normalization: y′ = `(x**4 + y*exp(x))/x`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Let's attempt to write $\frac{\text{d}y}{\text{d}x}-{u}^{2}=\frac{1}{1-y}$ in the standard form:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}-{u}^{2}=\frac{1}{1-y} \\ \frac{\text{d}y}{\text{d}x}+\frac{1}{y-1}={u}^{2}\end{aligned}
$$

This differential equation cannot be written in standard form since the power of $y$ in the term $\frac{1}{y-1}$ is not $1.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-8349 — easy

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+2xy=6x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $y\frac{\text{d}y}{\text{d}x}+2x=6x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+2xy=6{x}^{2}$ | correct selection | Linear after local normalization: y′ = `6*x**2 - 2*x*y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+2x{y}^{2}=6x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| ${(\frac{\text{d}y}{\text{d}x})}^{2}+2xy=6x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}+2uy=6{u}^{2}
$$

is already is written in standard form with  $P(x)=2u$ and $Q(x)=6{u}^{2}.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

### q-8352 — hard

Which of the following is **NOT** a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}+y=x$ | other choice | Linear after local normalization: y′ = `x - y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $y\frac{\text{d}y}{\text{d}x}+x=y$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+x=y$ | other choice | Linear after local normalization: y′ = `-x + y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+y=xy$ | other choice | Linear after local normalization: y′ = `x*y - y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+y=\operatorname{cos}⁡{e}^{\operatorname{arctan}⁡({x}^{2}+\operatorname{ln}⁡x)}$ | other choice | Linear after local normalization: y′ = `-y + cos(exp(atan(x**2 + log(x))))`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Let's attempt to write $y\frac{\text{d}y}{\text{d}x}+u=y$ in the standard form:

$$
\begin{aligned}y\frac{\text{d}y}{\text{d}x}+u=y \\ \frac{\text{d}y}{\text{d}x}+u{y}^{-1}=1\end{aligned}
$$

This differential equation cannot be written in standard form since the power of $y$ in the term $u{y}^{-1}$ is not $1.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-103551 — easy

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}-3(\operatorname{ln}⁡x)y=\frac{1}{x}$ | correct selection | Linear after local normalization: y′ = `(3*x*y*log(x) + 1)/x`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{1}{y}\frac{\text{d}y}{\text{d}x}-xy={x}^{3}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| ${(\frac{\text{d}y}{\text{d}x})}^{2}+{x}^{2}y=\operatorname{sin}⁡x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\operatorname{sin}⁡(xy)=x-1$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-{x}^{3}y=\frac{x}{1+y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}-3(\operatorname{ln}⁡u)y=\frac{1}{u}
$$

is already is written in standard form with  $P(x)=-3\operatorname{ln}⁡u$ and $Q(x)=\frac{1}{u}.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

### q-103554 — easy

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| ${(\frac{\text{d}y}{\text{d}x})}^{2}-{x}^{3}=\sqrt{1+y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-{e}^{xy}=x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-\frac{{e}^{x}}{x}y={x}^{2}\operatorname{sin}⁡x$ | correct selection | Linear after local normalization: y′ = `(x**3*sin(x) + y*exp(x))/x`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{1}{{y}^{2}}\frac{\text{d}y}{\text{d}x}-{x}^{2}=\operatorname{sin}⁡x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+x\operatorname{ln}⁡(xy)={x}^{2}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}-\frac{{e}^{u}}{u}y={u}^{2}\operatorname{sin}⁡u
$$

is already is written in standard form with  $P(x)=-\frac{{e}^{u}}{u}$ and $Q(x)={u}^{2}\operatorname{sin}⁡u.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

### q-103557 — moderate

Which of the following is **NOT** a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}-4y=x$ | other choice | Linear after local normalization: y′ = `x + 4*y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-\sqrt{xy}={x}^{2}$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $x\frac{\text{d}y}{\text{d}x}-({x}^{3}\operatorname{cos}⁡x)y=\operatorname{sin}⁡x$ | other choice | Linear after local normalization: y′ = `(x**3*y*cos(x) + sin(x))/x`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| ${x}^{2}\frac{\text{d}y}{\text{d}x}-(1+x)y=1$ | other choice | Linear after local normalization: y′ = `(x*y + y + 1)/x**2`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-\frac{1}{{x}^{2}}y={e}^{-x}$ | other choice | Linear after local normalization: y′ = `(x**2 + y*exp(x))*exp(-x)/x**2`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}-\sqrt{uy}={u}^{2}
$$

cannot be written in standard form since the power of $y$ in the term $\sqrt{uy}$ is not $1.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-103559 — moderate

Which of the following is **NOT** a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{1}{x}\frac{\text{d}y}{\text{d}x}-{x}^{2}y=\operatorname{sin}⁡x$ | other choice | Linear after local normalization: y′ = `x**3*y + x*sin(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+4y={e}^{x}$ | other choice | Linear after local normalization: y′ = `-4*y + exp(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-xy=\operatorname{sin}⁡x$ | other choice | Linear after local normalization: y′ = `x*y + sin(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+(\operatorname{ln}⁡x)y={x}^{2}$ | other choice | Linear after local normalization: y′ = `x**2 - y*log(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\operatorname{ln}⁡(xy)={x}^{2}$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}+\operatorname{ln}⁡(uy)={u}^{2}
$$

cannot be written in standard form since the power of $y$ in the term $\operatorname{ln}⁡(uy)$ is not $1.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-79750 — moderate

Which of the following is **NOT** a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $y\frac{\text{d}y}{\text{d}x}+x{y}^{2}=2y$ | other choice | Linear after local normalization: y′ = `-x*y + 2`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\frac{y}{2}=x$ | other choice | Linear after local normalization: y′ = `x - y/2`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+y=1+\operatorname{sin}⁡x$ | other choice | Linear after local normalization: y′ = `-y + sin(x) + 1`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+xy={y}^{2}$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+{x}^{2}y=\operatorname{sec}⁡x$ | other choice | Linear after local normalization: y′ = `-x**2*y + sec(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}+uy={y}^{2}
$$

cannot be written in standard form since the right-hand side depends on $y.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-79752 — moderate

Which of the following is **NOT** a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}+y=0$ | other choice | Linear after local normalization: y′ = `-y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\frac{y}{{x}^{2}}={e}^{2x}$ | other choice | Linear after local normalization: y′ = `(x**2*exp(2*x) - y)/x**2`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\frac{y}{\sqrt{{x}^{2}+1}}=0$ | other choice | Linear after local normalization: y′ = `-y/sqrt(x**2 + 1)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\sqrt{y}=x\operatorname{cos}⁡x$ | correct selection | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\frac{y}{\operatorname{arctan}⁡x}=\frac{1}{{x}^{2}}$ | other choice | Linear after local normalization: y′ = `(-x**2*y + atan(x))/(x**2*atan(x))`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}+\sqrt{y}=u\operatorname{cos}⁡u
$$

cannot be written in standard form since the power of $y$ in the term $\sqrt{y}$ is not $1.$ Since the equation cannot be written in standard form, we conclude that it is not a first-order linear ODE.

All of the other equations can be written in the standard form, and therefore they are first-order linear ODEs.

### q-79753 — easy

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{\text{d}y}{\text{d}x}+y=\operatorname{sin}⁡y$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+(\sqrt{x})y=x\operatorname{tan}⁡x$ | correct selection | Linear after local normalization: y′ = `-sqrt(x)*y + x*tan(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-xy=\frac{1}{y-1}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-y={y}^{2}\operatorname{cos}⁡x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}+\sqrt{(xy)}=x+1$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Note that the option

$$
\frac{\text{d}y}{\text{d}x}+(\sqrt{u})y=u\operatorname{tan}⁡u
$$

is already is written in standard form with  $P(x)=\sqrt{u}$ and $Q(x)=u\operatorname{tan}⁡u.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

### q-79754 — hard

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $(\frac{1}{y})\frac{\text{d}y}{\text{d}x}=\frac{2y+{x}^{2}}{y}$ | correct selection | Linear after local normalization: y′ = `x**2 + 2*y`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $(\frac{1}{y})\frac{\text{d}y}{\text{d}x}=\frac{1}{y\operatorname{cos}⁡x}-y$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}+3x}{y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $y\frac{\text{d}y}{\text{d}x}={y}^{2}-2x$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $(\frac{1}{y})\frac{\text{d}y}{\text{d}x}=\frac{y-x}{{y}^{2}}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Let's attempt to write $(\frac{1}{y})\frac{\text{d}y}{\text{d}x}=\frac{2y+{u}^{2}}{y}$ in the standard form:

$$
\begin{aligned}(\frac{1}{y})\frac{\text{d}y}{\text{d}x} & =\frac{2y+{u}^{2}}{y} \\ \frac{\text{d}y}{\text{d}x} & =y(\frac{2y+{u}^{2}}{y}) \\ \frac{\text{d}y}{\text{d}x} & =2y+{u}^{2} \\ \frac{\text{d}y}{\text{d}x}-2y & ={u}^{2}.\end{aligned}
$$

This differential equation is in standard form with  $P(x)=-2$ and $Q(x)={u}^{2}.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

### q-103567 — hard

Which of the following is a first-order linear ordinary differential equation?

| Choice value | Designation | Parameterized recipe/object |
|---|---|---|
| $\frac{1}{y}\frac{\text{d}y}{\text{d}x}-x{e}^{2x}=\frac{\operatorname{cos}⁡x}{y}$ | correct selection | Linear after local normalization: y′ = `x*y*exp(2*x) + cos(x)`; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{1}{y}\frac{\text{d}y}{\text{d}x}+x{e}^{2x}y=\frac{\operatorname{cos}⁡x}{y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-x{e}^{y}={x}^{3}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $y\frac{\text{d}y}{\text{d}x}-x{e}^{x}=\frac{\operatorname{sin}⁡x}{y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |
| $\frac{\text{d}y}{\text{d}x}-y{e}^{2x}=\frac{\operatorname{cos}⁡x}{y}$ | other choice | Higher-order or nonlinear: does not normalize to affine y′ flow; replace each independent-variable function input x by u=a*x+h, leaving y′/y″ untouched |

Worked-sentence and stage template:

To determine which of the following differential equations is a first-order linear ordinary differential equation, we attempt to write each option in the standard form.

A first-order linear ODE is in standard form if it is written as

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x).
$$

Let's attempt to write $\frac{1}{y}\frac{\text{d}y}{\text{d}x}-u{e}^{2u}=\frac{\operatorname{cos}⁡u}{y}$ in the standard form:

$$
\begin{aligned}\frac{1}{y}\frac{\text{d}y}{\text{d}x}-u{e}^{2u} & =\frac{\operatorname{cos}⁡u}{y} \\ \frac{\text{d}y}{\text{d}x}-u{e}^{2u}y & =y\cdot \frac{\operatorname{cos}⁡u}{y} \\ \frac{\text{d}y}{\text{d}x}-u{e}^{2u}y & =\operatorname{cos}⁡u.\end{aligned}
$$

This differential equation is in standard form with  $P(x)=-u{e}^{2u}$ and $Q(x)=\operatorname{cos}⁡u.$ Since the equation is written in standard form, we conclude that it is a first-order linear ODE.

All of the other equations cannot be written in the standard form, and therefore they are not first-order linear ODEs.

## Stage 2: shared mathematical pattern

Identify which complete equation can (easy and two hard banks) or cannot (moderate and one hard bank) be written as y′+P(x)y=Q(x). Local cancellation of nonzero factors is allowed exactly as in the observed lesson. Each source bank mixes the same intended categorical distinctions across all parameters. Neither complicated x-only functions nor y on the RHS by itself proves nonlinearity.

## Stage 3: component and bank accounting

The tables map all 60 original values and 12 correct designations to their complete profiles. Every option is a parameterized mathematical object, produced by the same substitution into its explicit equation recipe. Higher derivative, derivative square, nonlinear y powers/functions, reciprocal y coefficients, and cancelable factors are the observed operations. These are categorical alternatives rather than wrong numerical outputs derived from a single numeric correct value. No empirical distractor fit, interpretation of an unknown scalar intent, partial-bank pool, or literal replay branch is used.

The fixed components are question wording, field layout, five-option count, derivative notation, sentence sequence, and local normalization steps. Variable components are all independent-variable function inputs. P(x) and Q(x) arguments remain x; their displayed values receive the same function substitution. All aligned stages and explanatory expression references receive the substitution. Source parameter a=1,h=0 is an ordinary valid input, not a special source-return mode.

## Stage 4: reusable templates, constraints and authored variation

The 12 implementation templates own their full observed banks. Select the complete eligible bank before sampling a,h. Render each equation from its reusable text recipe; independently parse it as an exact symbolic equation and normalize its derivative coefficient. Compute the unique desired linearity category rather than looking up the correct answer index. Any invalid/ambiguous/equivalent option rejects the whole bank. The worked solution is a single fixed text/stage template, independent of chosen answer.

Observed parameters are a=1,h=0. Authored default bounds: a in {−3,−2,−1,1,2,3}, h from −4 through 4. Supported explicit boundary bounds: 0<|a|≤6 and |h|≤8. This varies signed, scaled, translated polynomial/rational/trigonometric/logarithmic/exponential coefficient functions without introducing an integration step, new nonlinear classification branch or difficulty progression. Every source profile remains default eligible. Source intent and sampling algorithms are not claimed recovered.

Domains: use local real intervals where every displayed function is finite; a*x+h>0 is available for logarithms and roots. Exclude zeros of displayed denominator functions. Require y≠0 wherever reciprocal factors are cleared; additional positive-domain restrictions for y roots/logarithms belong to author metadata. The lesson interprets cancelable y-dependent factors locally, not as equality of global solution sets at excluded singular points.

## Source wording findings

No mathematical bank or correct-designation error was found. q-79750 says its nonlinear equation cannot be in standard form “since the right-hand side depends on y.” This rationale is incomplete in isolation: linear RHS y terms can be collected. The actual RHS is y², so the designation and equation are correct. The exact observed sentence is retained for fidelity and this limitation is explicit here. The other root/log explanations use “power” informally to describe nonlinearity. No source was excluded or silently repaired.

## Parent solution correction

q-79750’s original rationale says dependence on y prevents linearity, which is incomplete: a linear y term on the right can be collected. The generated sentence now specifies the nonlinear y² term. All12 source prompts,60 options and12 designations remain exact;11 supplied worked solutions remain byte-exact and one has this documented correction. Original evidence remains unchanged.
