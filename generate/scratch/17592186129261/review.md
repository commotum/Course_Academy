# Original and generated review

All original previews below are exact public raw replays. Missing ratings/solutions/keys remain missing. Historical profiles are evidence-only. The source easy quadrant error is retained here and repaired in normal examples.

Source coverage: 4/4 complete banks, 20/20 values, 2/2 observed refs; 2 missing refs not counted matched.

## Original raw replay — linear_legacy

Difficulty: easy (authored assignment); profile: observed-linear-legacy; parameters: `{"a": 2, "b": 1, "h": 1, "j": 1, "k": 2, "l": -1}`.

Using the change of variables

$u = y - 2x, v = y + x$,
calculate the area of the finite region $D$ in the first quadrant bounded by the lines
$y = 2x - 1, y = 2x + 1, y = 1 - x, y = 2 - x$.

- $\frac{1}{3}$
- $\frac{2}{3}$
- $2$
- $4$
- $6$

[Worked solution absent in raw capture.]

## Changed-parameter historical bank (evidence-only) — linear_legacy

Difficulty: easy (authored assignment); profile: observed-linear-legacy; parameters: `{"a": 2, "b": 1, "h": 1, "j": 1, "k": 3, "l": -1}`.

Using the change of variables

$u = y - 2x, v = y + x$,
calculate the area of the finite region $D$ in the first quadrant bounded by the lines
$y = 2x - 1, y = 2x + 1, y = 1 - x, y = 3 - x$.

- $\frac{2}{3}$
- $\frac{4}{3}$
- $4$
- $8$
- $12$

[Worked solution absent in raw capture.]

## Original raw replay — quotient

Difficulty: moderate (authored assignment); profile: observed-quotient; parameters: `{"h": 2, "j": 1, "k": 4, "l": 1, "n": 2}`.

Using the change of variables

$u = \frac{y}{x^{2}}, v = xy$,

calculate the area of the finite region $D$ in the first quadrant bounded by the curves
$y = x^{2}, y = 2x^{2}, y = \frac{1}{x}, y = \frac{4}{x}$.

- $\ln 4$
- $4\ln 2$
- $3\ln 2$
- $\frac{1}{2}\ln 2$
- $\ln 2$

[Worked solution absent in raw capture.]

## Changed-parameter historical bank (evidence-only) — quotient

Difficulty: moderate (authored assignment); profile: observed-quotient; parameters: `{"h": 2, "j": 1, "k": 5, "l": 1, "n": 2}`.

Using the change of variables

$u = \frac{y}{x^{2}}, v = xy$,

calculate the area of the finite region $D$ in the first quadrant bounded by the curves
$y = x^{2}, y = 2x^{2}, y = \frac{1}{x}, y = \frac{5}{x}$.

- $\ln 5$
- $5\ln 2$
- $4\ln 2$
- $\frac{2}{3}\ln 2$
- $\frac{4}{3}\ln 2$

[Worked solution absent in raw capture.]

## Original raw replay — linear

Difficulty: easy (observed level); profile: observed-linear; parameters: `{"a": 3, "b": 2, "h": 2, "j": 1, "k": 3, "l": -2}`.

Using the change of variables 

$$
u=y-3x,\,v=y+2x,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the lines

$$
y=3x-2,\,y=3x+2,\,y=1-2x,\,y=3-2x.
$$

- $\frac{8}{3}$
- $\frac{4}{5}$
- $\frac{5}{6}$
- $\frac{8}{5}$
- $\frac{4}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=y-3x,\,v=y+2x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=y-3x$ into the equations of the first and second lines:

$$
\begin{aligned} & y=3x-2 & ⟹\, & y-3x=-2 & ⟹\, & u=-2 \\  & y=3x+2 & ⟹\, & y-3x=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=y+2x$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=1-2x & ⟹\, & y+2x=1 & ⟹\, & v=1 \\  & y=3-2x & ⟹\, & y+2x=3 & ⟹\, & v=3\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ={(u,v)\,:\,-2\le u\le 2,\,1\le v\le 3}
$$

![](/media/jake/SSD/EDB/math/images/9c/9c17c81b4abc0d4ebd1eadfe951b0eb0c2674d9eb07b785e7fd972fd00e513ae.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-3 & 1 \\ 2 & \text{ }\text{ }1\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{5}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|-\frac{1}{5}|\,\text{d}u\text{d}v \\  & =\frac{1}{5}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{5}\cdot \text{Area}(Δ) \\  & =\frac{1}{5}\cdot 4\cdot 2 \\  & =\frac{8}{5}\end{aligned}
$$

## Changed-parameter historical bank (evidence-only) — linear

Difficulty: easy (observed level); profile: observed-linear; parameters: `{"a": 3, "b": 2, "h": 2, "j": 1, "k": 4, "l": -2}`.

Using the change of variables 

$$
u=y-3x,\,v=y+2x,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the lines

$$
y=3x-2,\,y=3x+2,\,y=1-2x,\,y=4-2x.
$$

- $4$
- $\frac{4}{5}$
- $\frac{5}{7}$
- $\frac{12}{5}$
- $\frac{4}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=y-3x,\,v=y+2x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=y-3x$ into the equations of the first and second lines:

$$
\begin{aligned} & y=3x-2 & ⟹\, & y-3x=-2 & ⟹\, & u=-2 \\  & y=3x+2 & ⟹\, & y-3x=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=y+2x$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=1-2x & ⟹\, & y+2x=1 & ⟹\, & v=1 \\  & y=4-2x & ⟹\, & y+2x=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ={(u,v)\,:\,-2\le u\le 2,\,1\le v\le 4}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/77ac43741ae1f19d53f1cc76b6139d701f7087a61f39703a1250a33db4471123.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-3 & 1 \\ 2 & \text{ }\text{ }1\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{5}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|-\frac{1}{5}|\,\text{d}u\text{d}v \\  & =\frac{1}{5}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{5}\cdot \text{Area}(Δ) \\  & =\frac{1}{5}\cdot 4\cdot 3 \\  & =\frac{12}{5}\end{aligned}
$$

## Original raw replay — reciprocal

Difficulty: moderate (observed level); profile: observed-reciprocal; parameters: `{"c": 1, "d": 1, "h": 3, "j": 1, "k": 3, "l": 2, "n": 2}`.

Using the change of variables

$$
u=\frac{1}{xy},\,v={x}^{2}y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{2x},\,y=\frac{1}{3x},\,y=\frac{1}{{x}^{2}},\,y=\frac{3}{{x}^{2}}.
$$

- $\frac{1}{3}\operatorname{ln}⁡2$
- $\frac{1}{6}\operatorname{ln}⁡3$
- $\frac{1}{3}\operatorname{ln}⁡3$
- $\frac{1}{2}\operatorname{ln}⁡3$
- $\frac{1}{6}\operatorname{ln}⁡2$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{1}{xy},\,v={x}^{2}y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{1}{xy}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{2x} & ⟹\, & \frac{1}{xy}=2 & ⟹\, & u=2 \\  & y=\frac{1}{3x} & ⟹\, & \frac{1}{xy}=3 & ⟹\, & u=3\end{aligned}
$$

And we substitute $v={x}^{2}y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{{x}^{2}} & ⟹\, & {x}^{2}y=1 & ⟹\, & v=1 \\  & y=\frac{3}{{x}^{2}} & ⟹\, & {x}^{2}y=3 & ⟹\, & v=3\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ={(u,v)\,:\,2\le u\le 3,\,1\le v\le 3}
$$

![](/media/jake/SSD/EDB/math/images/05/05d2ca47db245b147cb52f95a474a60ece144931c8b6e1e40c6628a99b53d690.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{1}{{x}^{2}y} & -\frac{1}{x{y}^{2}} \\ 2xy & \text{ }\text{ }{x}^{2}\end{aligned}| \\  & =\frac{1}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=y=\frac{{x}^{2}{y}^{2}}{{x}^{2}y}=\frac{1}{{u}^{2}v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|-\frac{1}{{u}^{2}v}|\,\text{d}u\text{d}v \\  & ={\int }_{2}^{3}{\int }_{1}^{3}\frac{1}{{u}^{2}v}\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{3}\frac{1}{{u}^{2}}\,\text{d}u{\int }_{1}^{3}\frac{1}{v}\,\text{d}v \\  & =(-\frac{1}{3}+\frac{1}{2})\cdot (\operatorname{ln}⁡3-\operatorname{ln}⁡1) \\  & =\frac{1}{6}\operatorname{ln}⁡3.\end{aligned}
$$

## Changed-parameter historical bank (evidence-only) — reciprocal

Difficulty: moderate (observed level); profile: observed-reciprocal; parameters: `{"c": 1, "d": 1, "h": 3, "j": 1, "k": 4, "l": 2, "n": 2}`.

Using the change of variables

$$
u=\frac{1}{xy},\,v={x}^{2}y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{2x},\,y=\frac{1}{3x},\,y=\frac{1}{{x}^{2}},\,y=\frac{4}{{x}^{2}}.
$$

- $\frac{1}{3}\operatorname{ln}⁡3$
- $\frac{1}{6}\operatorname{ln}⁡4$
- $\frac{1}{3}\operatorname{ln}⁡4$
- $\frac{1}{2}\operatorname{ln}⁡4$
- $\frac{1}{6}\operatorname{ln}⁡3$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{1}{xy},\,v={x}^{2}y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{1}{xy}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{2x} & ⟹\, & \frac{1}{xy}=2 & ⟹\, & u=2 \\  & y=\frac{1}{3x} & ⟹\, & \frac{1}{xy}=3 & ⟹\, & u=3\end{aligned}
$$

And we substitute $v={x}^{2}y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{{x}^{2}} & ⟹\, & {x}^{2}y=1 & ⟹\, & v=1 \\  & y=\frac{4}{{x}^{2}} & ⟹\, & {x}^{2}y=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ={(u,v)\,:\,2\le u\le 3,\,1\le v\le 4}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/4b0b01a0c31c1d198dcea098ff7b6fc93d20ee2634084750ebe8ffcd531b84ca.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{1}{{x}^{2}y} & -\frac{1}{x{y}^{2}} \\ 2xy & \text{ }\text{ }{x}^{2}\end{aligned}| \\  & =\frac{1}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=y=\frac{{x}^{2}{y}^{2}}{{x}^{2}y}=\frac{1}{{u}^{2}v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|-\frac{1}{{u}^{2}v}|\,\text{d}u\text{d}v \\  & ={\int }_{2}^{3}{\int }_{1}^{4}\frac{1}{{u}^{2}v}\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{3}\frac{1}{{u}^{2}}\,\text{d}u{\int }_{1}^{4}\frac{1}{v}\,\text{d}v \\  & =(-\frac{1}{3}+\frac{1}{2})\cdot (\operatorname{ln}⁡4-\operatorname{ln}⁡1) \\  & =\frac{\ln{\left(2 \right)}}{3}.\end{aligned}
$$

## Generated method-bank variant — linear_legacy

Difficulty: easy (authored assignment); profile: linear-legacy-unit-method; parameters: `{"a": 1, "b": 4, "h": 3, "j": 2, "k": 8, "l": -2}`.

Using the change of variables

$$
u=- x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=x - 2,\qquad y=x + 3,\qquad y=2 - 4 x,\qquad y=8 - 4 x.
$$

- $\frac{6}{5}$
- $6$
- $150$
- $30$
- $\frac{11}{5}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=x - 2 & ⟹\, & - x + y=-2 & ⟹\, & u=-2 \\  & y=x + 3 & ⟹\, & - x + y=3 & ⟹\, & u=3\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=2 - 4 x & ⟹\, & 4 x + y=2 & ⟹\, & v=2 \\  & y=8 - 4 x & ⟹\, & 4 x + y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,-2\le u\le 3,\,2\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/5bee89ecf88460cad4e3b27d21c6c101a43601d1c6e61d12242ee77e4c3e6192.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 4 & 1\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{5}=- \frac{1}{5}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{5}|\,\text{d}u\text{d}v \\  & =\frac{1}{5}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{5}\cdot \text{Area}(Δ) \\  & =\frac{1}{5}\cdot 5\cdot 6 \\  & =6\end{aligned}
$$

## Generated method-bank variant — linear_legacy

Difficulty: easy (authored assignment); profile: linear-legacy-method; parameters: `{"a": 2, "b": 4, "h": 2, "j": 1, "k": 7, "l": 1}`.

Using the change of variables

$$
u=- 2 x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x + 1,\qquad y=2 x + 2,\qquad y=1 - 4 x,\qquad y=7 - 4 x.
$$

- $1$
- $36$
- $3$
- $6$
- $\frac{3}{2}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x + 1 & ⟹\, & - 2 x + y=1 & ⟹\, & u=1 \\  & y=2 x + 2 & ⟹\, & - 2 x + y=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=1 - 4 x & ⟹\, & 4 x + y=1 & ⟹\, & v=1 \\  & y=7 - 4 x & ⟹\, & 4 x + y=7 & ⟹\, & v=7\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,1\le u\le 2,\,1\le v\le 7\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/976c0c5197a843567fe75b39fbc78143fe26e5279a6f5566538dd0680fd1e1f0.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 4 & 1\end{aligned}| \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{6}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{6}|\,\text{d}u\text{d}v \\  & =\frac{1}{6}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{6}\cdot \text{Area}(Δ) \\  & =\frac{1}{6}\cdot 1\cdot 6 \\  & =1\end{aligned}
$$

## Generated method-bank variant — linear

Difficulty: easy (observed level); profile: linear-unit-method; parameters: `{"a": 1, "b": 4, "h": 3, "j": 2, "k": 8, "l": -2}`.

Using the change of variables

$$
u=- x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=x - 2,\qquad y=x + 3,\qquad y=2 - 4 x,\qquad y=8 - 4 x.
$$

- $\frac{6}{5}$
- $6$
- $150$
- $30$
- $\frac{11}{5}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=x - 2 & ⟹\, & - x + y=-2 & ⟹\, & u=-2 \\  & y=x + 3 & ⟹\, & - x + y=3 & ⟹\, & u=3\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=2 - 4 x & ⟹\, & 4 x + y=2 & ⟹\, & v=2 \\  & y=8 - 4 x & ⟹\, & 4 x + y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,-2\le u\le 3,\,2\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/5bee89ecf88460cad4e3b27d21c6c101a43601d1c6e61d12242ee77e4c3e6192.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 4 & 1\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{5}=- \frac{1}{5}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{5}|\,\text{d}u\text{d}v \\  & =\frac{1}{5}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{5}\cdot \text{Area}(Δ) \\  & =\frac{1}{5}\cdot 5\cdot 6 \\  & =6\end{aligned}
$$

## Generated method-bank variant — linear

Difficulty: easy (observed level); profile: linear-method; parameters: `{"a": 2, "b": 4, "h": 2, "j": 1, "k": 7, "l": 1}`.

Using the change of variables

$$
u=- 2 x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x + 1,\qquad y=2 x + 2,\qquad y=1 - 4 x,\qquad y=7 - 4 x.
$$

- $1$
- $36$
- $3$
- $6$
- $\frac{3}{2}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x + 1 & ⟹\, & - 2 x + y=1 & ⟹\, & u=1 \\  & y=2 x + 2 & ⟹\, & - 2 x + y=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=1 - 4 x & ⟹\, & 4 x + y=1 & ⟹\, & v=1 \\  & y=7 - 4 x & ⟹\, & 4 x + y=7 & ⟹\, & v=7\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,1\le u\le 2,\,1\le v\le 7\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/976c0c5197a843567fe75b39fbc78143fe26e5279a6f5566538dd0680fd1e1f0.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 4 & 1\end{aligned}| \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{6}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{6}|\,\text{d}u\text{d}v \\  & =\frac{1}{6}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{6}\cdot \text{Area}(Δ) \\  & =\frac{1}{6}\cdot 1\cdot 6 \\  & =1\end{aligned}
$$

## Generated method-bank variant — quotient

Difficulty: moderate (authored assignment); profile: quotient-lower-unit-method; parameters: `{"h": 5, "j": 2, "k": 8, "l": 1, "n": 2}`.

Using the change of variables

$$
u=\frac{y}{x^{2}},\qquad v=x y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=x^{2},\qquad y=5 x^{2},\qquad y=\frac{2}{x},\qquad y=\frac{8}{x}.
$$

- $2 \ln{\left(5 \right)}$
- $3 \ln{\left(5 \right)}$
- $6 \ln{\left(5 \right)}$
- $8$
- $4 \ln{\left(2 \right)}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{y}{x^{2}},\,v=x y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{y}{x^{2}}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=x^{2} & ⟹\, & \frac{y}{x^{2}}=1 & ⟹\, & u=1 \\  & y=5 x^{2} & ⟹\, & \frac{y}{x^{2}}=5 & ⟹\, & u=5\end{aligned}
$$

And we substitute $v=x y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{2}{x} & ⟹\, & x y=2 & ⟹\, & v=2 \\  & y=\frac{8}{x} & ⟹\, & x y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,1\le u\le 5,\,2\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/6a27c2e3ef133aca96c6f5871173ad7b022980f1bc327b211f9ac5a6685478d4.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2 y}{x^{3}} & \frac{1}{x^{2}} \\ y & x\end{aligned}| \\  & =- \frac{3 y}{x^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{x^{2}}{3 y}=- \frac{1}{3 u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{3 u}|\,\text{d}u\text{d}v \\  & =\int_{1}^{5}\int_{2}^{8}\frac{1}{3 u}\,\mathrm d v\,\mathrm d u \\  & =\frac{1}{3}\int_{1}^{5}\frac{1}{u}\,\mathrm d u\int_{2}^{8}1\,\mathrm d v \\  & =\frac{1}{3}\cdot (\ln 5-\ln 1)\cdot (8-2) \\  & =2 \ln{\left(5 \right)}.\end{aligned}
$$

## Generated method-bank variant — quotient

Difficulty: moderate (authored assignment); profile: quotient-method; parameters: `{"h": 8, "j": 3, "k": 7, "l": 4, "n": 2}`.

Using the change of variables

$$
u=\frac{y}{x^{2}},\qquad v=x y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=4 x^{2},\qquad y=8 x^{2},\qquad y=\frac{3}{x},\qquad y=\frac{7}{x}.
$$

- $2 \ln{\left(2 \right)}$
- $12 \ln{\left(2 \right)}$
- $\frac{8 \ln{\left(2 \right)}}{3}$
- $\frac{4 \ln{\left(2 \right)}}{3}$
- $4 \ln{\left(2 \right)}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{y}{x^{2}},\,v=x y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{y}{x^{2}}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=4 x^{2} & ⟹\, & \frac{y}{x^{2}}=4 & ⟹\, & u=4 \\  & y=8 x^{2} & ⟹\, & \frac{y}{x^{2}}=8 & ⟹\, & u=8\end{aligned}
$$

And we substitute $v=x y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{3}{x} & ⟹\, & x y=3 & ⟹\, & v=3 \\  & y=\frac{7}{x} & ⟹\, & x y=7 & ⟹\, & v=7\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 8,\,3\le v\le 7\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/72e0fa5e93644faf78a3f2c8560031e90b2d67603a4392406775a71c52992d66.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2 y}{x^{3}} & \frac{1}{x^{2}} \\ y & x\end{aligned}| \\  & =- \frac{3 y}{x^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{x^{2}}{3 y}=- \frac{1}{3 u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{3 u}|\,\text{d}u\text{d}v \\  & =\int_{4}^{8}\int_{3}^{7}\frac{1}{3 u}\,\mathrm d v\,\mathrm d u \\  & =\frac{1}{3}\int_{4}^{8}\frac{1}{u}\,\mathrm d u\int_{3}^{7}1\,\mathrm d v \\  & =\frac{1}{3}\cdot (\ln 8-\ln 4)\cdot (7-3) \\  & =\frac{4 \ln{\left(2 \right)}}{3}.\end{aligned}
$$

## Generated method-bank variant — reciprocal

Difficulty: moderate (observed level); profile: reciprocal-lower-unit-method; parameters: `{"c": 1, "d": 1, "h": 5, "j": 1, "k": 8, "l": 4, "n": 2}`.

Using the change of variables

$$
u=\frac{1}{x y},\qquad v=x^{2} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{4 x},\qquad y=\frac{1}{5 x},\qquad y=\frac{1}{x^{2}},\qquad y=\frac{8}{x^{2}}.
$$

- $\frac{3 \ln{\left(2 \right)}}{20}$
- $\frac{3 \ln{\left(2 \right)}}{5}$
- $\frac{3 \ln{\left(2 \right)}}{4}$
- $\frac{7}{20}$
- $3 \ln{\left(2 \right)}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{1}{x y},\,v=x^{2} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{1}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{4 x} & ⟹\, & \frac{1}{x y}=4 & ⟹\, & u=4 \\  & y=\frac{1}{5 x} & ⟹\, & \frac{1}{x y}=5 & ⟹\, & u=5\end{aligned}
$$

And we substitute $v=x^{2} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{2}} & ⟹\, & x^{2} y=1 & ⟹\, & v=1 \\  & y=\frac{8}{x^{2}} & ⟹\, & x^{2} y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 5,\,1\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/7349f4e4bfcc768ceb9ca04feedb98639243779845851139b3bac39c0b12635e.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{1}{x^{2} y} & - \frac{1}{x y^{2}} \\ 2 x y & x^{2}\end{aligned}| \\  & =\frac{1}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=y=\frac{x^{2} y^{2}}{x^{2} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{4}^{5}\int_{1}^{8}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{4}^{5}\frac{1}{u^{2}}\,\mathrm d u\int_{1}^{8}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{5}+\frac{1}{4})\cdot (\ln 8-\ln 1) \\  & =\frac{3 \ln{\left(2 \right)}}{20}.\end{aligned}
$$

## Generated method-bank variant — reciprocal

Difficulty: moderate (observed level); profile: reciprocal-method; parameters: `{"c": 1, "d": 1, "h": 7, "j": 3, "k": 5, "l": 4, "n": 2}`.

Using the change of variables

$$
u=\frac{1}{x y},\qquad v=x^{2} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{4 x},\qquad y=\frac{1}{7 x},\qquad y=\frac{3}{x^{2}},\qquad y=\frac{5}{x^{2}}.
$$

- $- \frac{\ln{\left(3 \right)}}{7} + \frac{\ln{\left(5 \right)}}{7}$
- $\frac{3 \ln{\left(5 \right)}}{28}$
- $- \frac{\ln{\left(3 \right)}}{4} + \frac{\ln{\left(5 \right)}}{4}$
- $- \frac{3 \ln{\left(3 \right)}}{28} + \frac{3 \ln{\left(5 \right)}}{28}$
- $\frac{3 \ln{\left(3 \right)}}{28}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{1}{x y},\,v=x^{2} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{1}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{4 x} & ⟹\, & \frac{1}{x y}=4 & ⟹\, & u=4 \\  & y=\frac{1}{7 x} & ⟹\, & \frac{1}{x y}=7 & ⟹\, & u=7\end{aligned}
$$

And we substitute $v=x^{2} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{3}{x^{2}} & ⟹\, & x^{2} y=3 & ⟹\, & v=3 \\  & y=\frac{5}{x^{2}} & ⟹\, & x^{2} y=5 & ⟹\, & v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 7,\,3\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/bfceb4b61860c37a408f61947c04bf6d0a623e0f05cd587a4c8bb9e2731fca36.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{1}{x^{2} y} & - \frac{1}{x y^{2}} \\ 2 x y & x^{2}\end{aligned}| \\  & =\frac{1}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=y=\frac{x^{2} y^{2}}{x^{2} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{4}^{7}\int_{3}^{5}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{4}^{7}\frac{1}{u^{2}}\,\mathrm d u\int_{3}^{5}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{7}+\frac{1}{4})\cdot (\ln 5-\ln 3) \\  & =- \frac{3 \ln{\left(3 \right)}}{28} + \frac{3 \ln{\left(5 \right)}}{28}.\end{aligned}
$$

## Generated method-bank variant — reciprocal_scaled

Difficulty: hard (authored assignment); profile: scaled-lower-unit-method; parameters: `{"c": 3, "d": 3, "h": 5, "j": 1, "k": 8, "l": 4, "n": 3}`.

Using the change of variables

$$
u=\frac{3}{x y},\qquad v=3 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{3}{4 x},\qquad y=\frac{3}{5 x},\qquad y=\frac{1}{3 x^{3}},\qquad y=\frac{8}{3 x^{3}}.
$$

- $\frac{21}{40}$
- $\frac{9 \ln{\left(2 \right)}}{40}$
- $\frac{9 \ln{\left(2 \right)}}{8}$
- $\frac{9 \ln{\left(2 \right)}}{2}$
- $\frac{9 \ln{\left(2 \right)}}{10}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{3}{x y},\,v=3 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{3}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{3}{4 x} & ⟹\, & \frac{3}{x y}=4 & ⟹\, & u=4 \\  & y=\frac{3}{5 x} & ⟹\, & \frac{3}{x y}=5 & ⟹\, & u=5\end{aligned}
$$

And we substitute $v=3 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{3 x^{3}} & ⟹\, & 3 x^{3} y=1 & ⟹\, & v=1 \\  & y=\frac{8}{3 x^{3}} & ⟹\, & 3 x^{3} y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 5,\,1\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/7349f4e4bfcc768ceb9ca04feedb98639243779845851139b3bac39c0b12635e.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{3}{x^{2} y} & - \frac{3}{x y^{2}} \\ 9 x^{2} y & 3 x^{3}\end{aligned}| \\  & =\frac{18 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{18 x}=\frac{x^{2} y^{2}}{18 x^{3} y}=\frac{3}{2 u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{3}{2 u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{4}^{5}\int_{1}^{8}\frac{3}{2 u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\frac{3}{2}\int_{4}^{5}\frac{1}{u^{2}}\,\mathrm d u\int_{1}^{8}\frac{1}{v}\,\mathrm d v \\  & =\frac{3}{2}\cdot (- \frac{1}{5}+\frac{1}{4})\cdot (\ln 8-\ln 1) \\  & =\frac{9 \ln{\left(2 \right)}}{40}.\end{aligned}
$$

## Generated method-bank variant — reciprocal_scaled

Difficulty: hard (authored assignment); profile: scaled-method; parameters: `{"c": 3, "d": 3, "h": 5, "j": 3, "k": 5, "l": 4, "n": 3}`.

Using the change of variables

$$
u=\frac{3}{x y},\qquad v=3 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{3}{4 x},\qquad y=\frac{3}{5 x},\qquad y=\frac{1}{x^{3}},\qquad y=\frac{5}{3 x^{3}}.
$$

- $- \frac{3 \ln{\left(3 \right)}}{10} + \frac{3 \ln{\left(5 \right)}}{10}$
- $- \frac{3 \ln{\left(3 \right)}}{40} + \frac{3 \ln{\left(5 \right)}}{40}$
- $\frac{3 \ln{\left(5 \right)}}{40}$
- $- \frac{3 \ln{\left(3 \right)}}{8} + \frac{3 \ln{\left(5 \right)}}{8}$
- $\frac{3 \ln{\left(3 \right)}}{40}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{3}{x y},\,v=3 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{3}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{3}{4 x} & ⟹\, & \frac{3}{x y}=4 & ⟹\, & u=4 \\  & y=\frac{3}{5 x} & ⟹\, & \frac{3}{x y}=5 & ⟹\, & u=5\end{aligned}
$$

And we substitute $v=3 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{3}} & ⟹\, & 3 x^{3} y=3 & ⟹\, & v=3 \\  & y=\frac{5}{3 x^{3}} & ⟹\, & 3 x^{3} y=5 & ⟹\, & v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 5,\,3\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/c116d6a35d094e32018a0fe61a96bdef3d6180d4a3c4f7d51db7f7008dfac281.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{3}{x^{2} y} & - \frac{3}{x y^{2}} \\ 9 x^{2} y & 3 x^{3}\end{aligned}| \\  & =\frac{18 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{18 x}=\frac{x^{2} y^{2}}{18 x^{3} y}=\frac{3}{2 u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{3}{2 u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{4}^{5}\int_{3}^{5}\frac{3}{2 u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\frac{3}{2}\int_{4}^{5}\frac{1}{u^{2}}\,\mathrm d u\int_{3}^{5}\frac{1}{v}\,\mathrm d v \\  & =\frac{3}{2}\cdot (- \frac{1}{5}+\frac{1}{4})\cdot (\ln 5-\ln 3) \\  & =- \frac{3 \ln{\left(3 \right)}}{40} + \frac{3 \ln{\left(5 \right)}}{40}.\end{aligned}
$$
