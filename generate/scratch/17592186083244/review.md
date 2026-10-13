# Tangent-line generator review

Original capture profiles are evidence only. Normal records explicitly use authored complete operation banks.

## polynomial_radio — original raw replay

Profile: `observed_17592186083912`; parameters: `{"a": 2, "b": 3, "c": 3, "d": -5, "u": 1}`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-3t,\,y=3{t}^{2}-5,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=1.$

selection:

- $y+2=2(x+1)$ **correct**
- $y+2=(x+1)$
- $y=\frac{24}{11}\,x+\frac{2}{11}$
- $y+2=(x+2)$
- $y+2=2(x+2)$

First, we find the coordinates of the point by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =2(1)^{3}-3(1)=2-3=-1, \\ y & =3(1)^{2}-5=3-5=-2\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(-1,-2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=6{t}^{2}-3,\,{y}^{′}(t)=6t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6t}{6{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6\cdot 1}{6\cdot (1)^{2}-3} \\  & =\frac{6}{6-3} \\  & =2\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(-1,-2)$ and the slope $m=2.$ We get

$$
\begin{aligned}y+2 & =2(x+1).\end{aligned}
$$


---

## quintic_radio — original raw replay

Profile: `observed_17592186083913`; parameters: `{"a": 1, "b": 2, "c": 1, "u": -1}`.

A curve is defined by the parametric equations
$x = t^{2} - 2t, y = t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

selection:

- $y+1 =-\frac{5}{4}(x-3)$
- $y+1 =-\frac{5}{4}(x+3)$
- $y-1 =-\frac{3}{4}(x-3)$
- $y+1 = \frac{5}{4}(x-3)$
- $y-1 =-\frac{5}{2}(x-3)$




---

## exponential_y_intercept — original raw replay

Profile: `observed_17592186256700`; parameters: `{"a": 3, "h": 1, "w": 1}`.

A curve is defined by the parametric equations

$$
x={e}^{3t}+1,\,y={e}^{t}\operatorname{sin}⁡(\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,-\pi)$
- $(0,\frac{\pi }{2})$
- $(0,\frac{\pi }{3})$
- $(0,-\frac{\pi }{6})$
- $(0,-\frac{2\pi }{3})$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{3\cdot 0}+1=1+1=2, \\ y & ={e}^{0}\operatorname{sin}⁡(\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(2,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{e}^{3t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t))}{3{e}^{3t}} \\  & =\frac{\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)}{3{e}^{2t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(\pi \cdot 0)+\pi \operatorname{cos}⁡(\pi \cdot 0)}{3{e}^{2\cdot 0}} \\  & =\frac{0+\pi }{3} \\  & =\frac{\pi }{3}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,0)$ and the slope $m=\frac{\pi }{3}.$ We get

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(x-2).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(0-2) \\ y & =-\frac{2\pi }{3}\,.\end{aligned}
$$

Consequently, $(0,-\frac{2\pi }{3})$ is the $y$-intercept.


---

## trig_x_intercept — original raw replay

Profile: `observed_17592186275337`; parameters: `{"a": 1, "b": 1, "c": 1, "h": "1/3", "k": 1}`.

A curve is defined by the parametric equations

$$
x=\operatorname{sin}⁡t+\operatorname{cos}⁡t+\frac{1}{3},\,y=\operatorname{cos}⁡t+1,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(\frac{2}{7},\,0)$
- $(\frac{1}{3},\,0)$ **correct**
- $(\frac{2}{9},\,0)$
- $(\frac{1}{4},\,0)$
- $(\frac{2}{5},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{sin}⁡(\frac{\pi }{2})+\operatorname{cos}⁡(\frac{\pi }{2})+\frac{1}{3}=1+0+\frac{1}{3}=\frac{4}{3}, \\ y & =\operatorname{cos}⁡(\frac{\pi }{2})+1=0+1=1\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(\frac{4}{3},1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{cos}⁡t-\operatorname{sin}⁡t,\,{y}^{′}(t)=-\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\operatorname{sin}⁡t(\frac{1}{\operatorname{cos}⁡t-\operatorname{sin}⁡t}) \\  & =\frac{\operatorname{sin}⁡t}{\operatorname{sin}⁡t-\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{\operatorname{sin}⁡(\frac{\pi }{2})}{\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{1}{1-0} \\  & =1\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(\frac{4}{3},1)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-1 & =1\cdot (x-\frac{4}{3}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-1 & =1\cdot (x-\frac{4}{3}) \\ -1 & =x-\frac{4}{3} \\ x & =\frac{1}{3}\end{aligned}
$$

Consequently, $(\frac{1}{3},\,0)$ is the $x$-intercept.


---

## polynomial_blank — original raw replay

Profile: `observed_17592186319229`; parameters: `{"a": 1, "b": 4, "c": 2, "d": 1, "u": 2}`.

A curve is defined by the parametric equations

$$
x={t}^{3}-4t,\,y=2{t}^{2}+1,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $x+9$ **correct**

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =(2)^{3}-4(2)=8-8=0 \\ y & =2(2)^{2}+1=2(4)+1=9\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(0,9).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-4,\,{y}^{′}(t)=4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{4t}{3{t}^{2}-4}.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,2} & =\frac{4(2)}{3(2)^{2}-4} \\  & =\frac{8}{3(4)-4} \\  & =\frac{8}{12-4} \\  & =\frac{8}{8} \\  & =1.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,9)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-9 & =1(x-0) \\ y-9 & =x \\ y & =x+9.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=x+9.$


---

## log_y_intercept — original raw replay

Profile: `observed_17592186319230`; parameters: `{"k": 2, "n": 1}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+2),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Do not round the answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{1}{4}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e$ into the parametric equations:

$$
\begin{aligned}x & =e(\operatorname{ln}⁡e+2)=3e \\ y & =\operatorname{ln}⁡e=1\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(3e,1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+3,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+3)}.\end{aligned}
$$

At the point where $t=e,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e} & =\frac{1}{e(\operatorname{ln}⁡e+3)} \\  & =\frac{1}{4e}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(3e,1)$ and the slope $m=\frac{1}{4e}.$ We get

$$
\begin{aligned}y-1=\frac{1}{4e}(x-3e).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-1 & =\frac{1}{4e}(0-3e) \\ y-1 & =-\frac{3}{4} \\ y & =\frac{1}{4}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{1}{4}).$


---

## polynomial_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 2, "b": 3, "c": 3, "d": -5, "u": 1}`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-3t,\,y=3{t}^{2}-5,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=1.$

selection:

- $y+2=-2(x+1)$
- $y+2=\frac{1}{2}(x+1)$
- $y+2=2(x+1)$ **correct**
- $y-2=2(x+1)$
- $y+2=2(x-1)$

First, we find the coordinates of the point by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =2(1)^{3}-3(1)=2-3=-1, \\ y & =3(1)^{2}-5=3-5=-2\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(-1,-2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=6{t}^{2}-3,\,{y}^{′}(t)=6t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6t}{6{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6\cdot 1}{6\cdot (1)^{2}-3} \\  & =\frac{6}{6-3} \\  & =2\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(-1,-2)$ and the slope $m=2.$ We get

$$
\begin{aligned}y+2 & =2(x+1).\end{aligned}
$$


---

## quintic_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 2, "c": 1, "u": -1}`.

A curve is defined by the parametric equations
$x = t^{2} - 2t, y = t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

selection:

- $y+1=\frac{5}{4}(x-3)$
- $y+1=-\frac{4}{5}(x-3)$
- $y+1=-\frac{5}{4}(x-3)$ **correct**
- $y-1=-\frac{5}{4}(x-3)$
- $y+1=-\frac{5}{4}(x+3)$

First, we find the coordinates of the point by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}-2 (-1)=1+2=3 \\ y & =(-1)^{5}=-1=-1\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(3,-1).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=2 t-2,\qquad y'(t)=5 t^{4}.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{5 t^{4}}{2 t-2}.
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{5 (-1)^{4}}{2 (-1)-2}=\frac{5}{-4}=-\frac{5}{4}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(3,-1)$ and the slope $m=-\frac{5}{4}.$ We get

$$
y+1=-\frac{5}{4}(x-3).
$$


---

## exponential_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "h": 1, "w": 1}`.

A curve is defined by the parametric equations

$$
x={e}^{3t}+1,\,y={e}^{t}\operatorname{sin}⁡(\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,\frac{2\pi }{3})$
- $(0,-2\pi)$
- $(0,-\frac{2\pi }{3})$ **correct**
- $(0,\frac{\pi }{3})$
- $(0,0)$

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{3\cdot 0}+1=1+1=2, \\ y & ={e}^{0}\operatorname{sin}⁡(\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(2,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{e}^{3t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t))}{3{e}^{3t}} \\  & =\frac{\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)}{3{e}^{2t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(\pi \cdot 0)+\pi \operatorname{cos}⁡(\pi \cdot 0)}{3{e}^{2\cdot 0}} \\  & =\frac{0+\pi }{3} \\  & =\frac{\pi }{3}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,0)$ and the slope $m=\frac{\pi }{3}.$ We get

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(x-2).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(0-2) \\ y & =-\frac{2\pi }{3}\,.\end{aligned}
$$

Consequently, $(0,-\frac{2\pi }{3})$ is the $y$-intercept.


---

## trig_x_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 1, "c": 1, "h": "1/3", "k": 1}`.

A curve is defined by the parametric equations

$$
x=\operatorname{sin}⁡t+\operatorname{cos}⁡t+\frac{1}{3},\,y=\operatorname{cos}⁡t+1,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(\frac{7}{3},\,0)$
- $(-\frac{2}{3},\,0)$
- $(\frac{1}{3},\,0)$ **correct**
- $(-1,\,0)$
- $(\frac{4}{3},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{sin}⁡(\frac{\pi }{2})+\operatorname{cos}⁡(\frac{\pi }{2})+\frac{1}{3}=1+0+\frac{1}{3}=\frac{4}{3}, \\ y & =\operatorname{cos}⁡(\frac{\pi }{2})+1=0+1=1\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(\frac{4}{3},1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{cos}⁡t-\operatorname{sin}⁡t,\,{y}^{′}(t)=-\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\operatorname{sin}⁡t(\frac{1}{\operatorname{cos}⁡t-\operatorname{sin}⁡t}) \\  & =\frac{\operatorname{sin}⁡t}{\operatorname{sin}⁡t-\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{\operatorname{sin}⁡(\frac{\pi }{2})}{\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{1}{1-0} \\  & =1\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(\frac{4}{3},1)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-1 & =1\cdot (x-\frac{4}{3}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-1 & =1\cdot (x-\frac{4}{3}) \\ -1 & =x-\frac{4}{3} \\ x & =\frac{1}{3}\end{aligned}
$$

Consequently, $(\frac{1}{3},\,0)$ is the $x$-intercept.


---

## polynomial_blank — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 4, "c": 2, "d": 1, "u": 2}`.

A curve is defined by the parametric equations

$$
x={t}^{3}-4t,\,y=2{t}^{2}+1,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $x+9$ **correct**

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =(2)^{3}-4(2)=8-8=0 \\ y & =2(2)^{2}+1=2(4)+1=9\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(0,9).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-4,\,{y}^{′}(t)=4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{4t}{3{t}^{2}-4}.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,2} & =\frac{4(2)}{3(2)^{2}-4} \\  & =\frac{8}{3(4)-4} \\  & =\frac{8}{12-4} \\  & =\frac{8}{8} \\  & =1.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,9)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-9 & =1(x-0) \\ y-9 & =x \\ y & =x+9.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=x+9.$


---

## log_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"k": 2, "n": 1}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+2),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Give exact answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{1}{4}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e$ into the parametric equations:

$$
\begin{aligned}x & =e(\operatorname{ln}⁡e+2)=3e \\ y & =\operatorname{ln}⁡e=1\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(3e,1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+3,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+3)}.\end{aligned}
$$

At the point where $t=e,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e} & =\frac{1}{e(\operatorname{ln}⁡e+3)} \\  & =\frac{1}{4e}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(3e,1)$ and the slope $m=\frac{1}{4e}.$ We get

$$
\begin{aligned}y-1=\frac{1}{4e}(x-3e).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-1 & =\frac{1}{4e}(0-3e) \\ y-1 & =-\frac{3}{4} \\ y & =\frac{1}{4}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{1}{4}).$


---

## linear_cubic — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "b": 1, "c": -3, "d": -1, "u": 2}`.

A curve is defined by the parametric equations

$$
x=3 t+1,\qquad y=-3 t^{3}-t,\qquad -\infty<t<\infty.
$$

Calculate the equation of the tangent to the curve at the point where $t=2.$

selection:

- $y+26=-\frac{37}{3}(x-7)$ **correct**
- $y-26=-\frac{37}{3}(x-7)$
- $y+26=-\frac{3}{37}(x-7)$
- $y+26=\frac{37}{3}(x-7)$
- $y+26=-\frac{37}{3}(x+7)$

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =3 (2)+1=6+1=7 \\ y & =-3 (2)^{3}-(2)=-24-2=-26\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(7,-26).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=3,\qquad y'(t)=-9 t^{2}-1.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{-9 t^{2}-1}{3}.
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{-9 (2)^{2}-1}{3}=\frac{-37}{3}=-\frac{37}{3}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(7,-26)$ and the slope $m=-\frac{37}{3}.$ We get

$$
y+26=-\frac{37}{3}(x-7).
$$


---

## linear_cubic — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": -2, "b": 4, "c": -3, "d": -1, "u": -2}`.

A curve is defined by the parametric equations

$$
x=-2 t+4,\qquad y=-3 t^{3}-t,\qquad -\infty<t<\infty.
$$

Calculate the equation of the tangent to the curve at the point where $t=-2.$

selection:

- $y-26=\frac{37}{2}(x-8)$ **correct**
- $y-26=-\frac{37}{2}(x-8)$
- $y-26=\frac{2}{37}(x-8)$
- $y+26=\frac{37}{2}(x-8)$
- $y-26=\frac{37}{2}(x+8)$

First, we find the coordinates of the point by substituting $t=-2$ into the parametric equations:

$$
\begin{aligned}x & =-2 (-2)+4=4+4=8 \\ y & =-3 (-2)^{3}-(-2)=24+2=26\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(8,26).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=-2,\qquad y'(t)=-9 t^{2}-1.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{-9 t^{2}-1}{-2}.
$$

At the point where $t=-2,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{-9 (-2)^{2}-1}{-2}=\frac{-37}{-2}=\frac{37}{2}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(8,26)$ and the slope $m=\frac{37}{2}.$ We get

$$
y-26=\frac{37}{2}(x-8).
$$


---

## polynomial_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 2, "b": 4, "c": 1, "d": -2, "u": 2}`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-4t,\,y={t}^{2}-2,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=2.$

selection:

- $y-2=\frac{1}{5}(x-8)$ **correct**
- $y+2=\frac{1}{5}(x-8)$
- $y-2=5(x-8)$
- $y-2=-\frac{1}{5}(x-8)$
- $y-2=\frac{1}{5}(x+8)$

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =2(2)^{3}-4(2)=16-8=8, \\ y & =(2)^{2}-2=4-2=2\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(8,2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=6{t}^{2}-4,\,{y}^{′}(t)=2t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t}{6{t}^{2}-4}\,.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=2} & =\frac{2\cdot 2}{6\cdot (2)^{2}-4} \\  & =\frac{4}{24-4} \\  & =\frac{1}{5}\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(8,2)$ and the slope $m=\frac{1}{5}.$ We get

$$
\begin{aligned}y-2 & =\frac{1}{5}(x-8).\end{aligned}
$$


---

## polynomial_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 5, "c": 1, "d": -2, "u": -2}`.

A curve is defined by the parametric equations

$$
x={t}^{3}-5t,\,y={t}^{2}-2,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=-2.$

selection:

- $y-2=-\frac{4}{7}(x-2)$ **correct**
- $y-2=\frac{4}{7}(x-2)$
- $y-2=-\frac{7}{4}(x-2)$
- $y+2=-\frac{4}{7}(x-2)$
- $y-2=-\frac{4}{7}(x+2)$

First, we find the coordinates of the point by substituting $t=-2$ into the parametric equations:

$$
\begin{aligned}x & =(-2)^{3}-5(-2)=-8-(-10)=2, \\ y & =(-2)^{2}-2=4-2=2\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(2,2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-5,\,{y}^{′}(t)=2t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t}{3{t}^{2}-5}\,.\end{aligned}
$$

At the point where $t=-2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=-2} & =\frac{2\cdot (-2)}{3\cdot (-2)^{2}-5} \\  & =\frac{-4}{12-5} \\  & =-\frac{4}{7}\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,2)$ and the slope $m=-\frac{4}{7}.$ We get

$$
\begin{aligned}y-2 & =-\frac{4}{7}(x-2).\end{aligned}
$$


---

## polynomial_blank — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 2, "b": 4, "c": 1, "d": -2, "u": 2}`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-4t,\,y={t}^{2}-2,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $\frac{x}{5}+\frac{2}{5}$ **correct**

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =2(2)^{3}-4(2)=16-8=8 \\ y & =(2)^{2}-2=1(4)-2=2\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(8,2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=6{t}^{2}-4,\,{y}^{′}(t)=2t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t}{6{t}^{2}-4}.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,2} & =\frac{2(2)}{6(2)^{2}-4} \\  & =\frac{4}{6(4)-4} \\  & =\frac{4}{24-4} \\  & =\frac{4}{20} \\  & =\frac{1}{5}.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(8,2)$ and the slope $m=\frac{1}{5}.$ We get

$$
\begin{aligned}y-2 & =\frac{1}{5}(x-8) \\ y-2 & =\frac{x}{5}-\frac{8}{5} \\ y & =\frac{x}{5}+\frac{2}{5}.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=\frac{x}{5}+\frac{2}{5}.$


---

## polynomial_blank — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 5, "c": 1, "d": -2, "u": -2}`.

A curve is defined by the parametric equations

$$
x={t}^{3}-5t,\,y={t}^{2}-2,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=-2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $-\frac{4 x}{7}+\frac{22}{7}$ **correct**

First, we find the coordinates of the point by substituting $t=-2$ into the parametric equations:

$$
\begin{aligned}x & =(-2)^{3}-5(-2)=-8-(-10)=2 \\ y & =(-2)^{2}-2=1(4)-2=2\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(2,2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-5,\,{y}^{′}(t)=2t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t}{3{t}^{2}-5}.\end{aligned}
$$

At the point where $t=-2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,-2} & =\frac{2(-2)}{3(-2)^{2}-5} \\  & =\frac{-4}{3(4)-5} \\  & =\frac{-4}{12-5} \\  & =\frac{-4}{7} \\  & =-\frac{4}{7}.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,2)$ and the slope $m=-\frac{4}{7}.$ We get

$$
\begin{aligned}y-2 & =-\frac{4}{7}(x-2) \\ y-2 & =-\frac{4 x}{7}+\frac{8}{7} \\ y & =-\frac{4 x}{7}+\frac{22}{7}.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=-\frac{4 x}{7}+\frac{22}{7}.$


---

## quintic_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "b": 4, "c": 2, "u": 1}`.

A curve is defined by the parametric equations
$x = 3t^{2} - 4t, y = 2t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =1$.

> A scientific calculator is required to answer this question.

selection:

- $y-2=\frac{1}{5}(x+1)$
- $y-2=5(x+1)$ **correct**
- $y+2=5(x+1)$
- $y-2=-5(x+1)$
- $y-2=5(x-1)$

First, we find the coordinates of the point by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =3 (1)^{2}-4 (1)=3-4=-1 \\ y & =2 (1)^{5}=2=2\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(-1,2).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=6 t-4,\qquad y'(t)=10 t^{4}.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{10 t^{4}}{6 t-4}.
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{10 (1)^{4}}{6 (1)-4}=\frac{10}{2}=5.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(-1,2)$ and the slope $m=5.$ We get

$$
y-2=5(x+1).
$$


---

## quintic_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 1, "c": 2, "u": -1}`.

A curve is defined by the parametric equations
$x = t^{2} - 1t, y = 2t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

selection:

- $y+2=-\frac{10}{3}(x-2)$ **correct**
- $y+2=\frac{10}{3}(x-2)$
- $y+2=-\frac{3}{10}(x-2)$
- $y-2=-\frac{10}{3}(x-2)$
- $y+2=-\frac{10}{3}(x+2)$

First, we find the coordinates of the point by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}-(-1)=1+1=2 \\ y & =2 (-1)^{5}=-2=-2\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(2,-2).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=2 t-1,\qquad y'(t)=10 t^{4}.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{10 t^{4}}{2 t-1}.
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{10 (-1)^{4}}{2 (-1)-1}=\frac{10}{-3}=-\frac{10}{3}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(2,-2)$ and the slope $m=-\frac{10}{3}.$ We get

$$
y+2=-\frac{10}{3}(x-2).
$$


---

## exponential_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 5, "h": 4, "w": 1}`.

A curve is defined by the parametric equations

$$
x={e}^{5t}+4,\,y={e}^{t}\operatorname{sin}⁡(\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,-\pi)$ **correct**
- $(0,\frac{\pi }{5})$
- $(0,-5\pi)$
- $(0,0)$
- $(0,\pi)$

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{5\cdot 0}+4=1+4=5, \\ y & ={e}^{0}\operatorname{sin}⁡(\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(5,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=5{e}^{5t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t))}{5{e}^{5t}} \\  & =\frac{\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)}{5{e}^{4t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(\pi \cdot 0)+\pi \operatorname{cos}⁡(\pi \cdot 0)}{5{e}^{4\cdot 0}} \\  & =\frac{0+\pi }{5} \\  & =\frac{\pi }{5}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(5,0)$ and the slope $m=\frac{\pi }{5}.$ We get

$$
\begin{aligned}y-0 & =\frac{\pi }{5}(x-5).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{\pi }{5}(0-5) \\ y & =-\pi\,.\end{aligned}
$$

Consequently, $(0,-\pi)$ is the $y$-intercept.


---

## exponential_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "h": 1, "w": 2}`.

A curve is defined by the parametric equations

$$
x={e}^{3t}+1,\,y={e}^{t}\operatorname{sin}⁡(2\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,\frac{2\pi }{3})$
- $(0,\frac{4\pi }{3})$
- $(0,-4\pi)$
- $(0,0)$
- $(0,-\frac{4\pi }{3})$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{3\cdot 0}+1=1+1=2, \\ y & ={e}^{0}\operatorname{sin}⁡(2\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(2,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{e}^{3t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(2\pi t)+2\pi \operatorname{cos}⁡(2\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(2\pi t)+2\pi \operatorname{cos}⁡(2\pi t))}{3{e}^{3t}} \\  & =\frac{\operatorname{sin}⁡(2\pi t)+2\pi \operatorname{cos}⁡(2\pi t)}{3{e}^{2t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(2\pi \cdot 0)+2\pi \operatorname{cos}⁡(2\pi \cdot 0)}{3{e}^{2\cdot 0}} \\  & =\frac{0+2\pi }{3} \\  & =\frac{2\pi }{3}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,0)$ and the slope $m=\frac{2\pi }{3}.$ We get

$$
\begin{aligned}y-0 & =\frac{2\pi }{3}(x-2).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{2\pi }{3}(0-2) \\ y & =-\frac{4\pi }{3}\,.\end{aligned}
$$

Consequently, $(0,-\frac{4\pi }{3})$ is the $y$-intercept.


---

## trig_x_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 4, "b": 4, "c": 1, "h": "-1/3", "k": 4}`.

A curve is defined by the parametric equations

$$
x=4\operatorname{sin}⁡t+4\operatorname{cos}⁡t-\frac{1}{3},\,y=\operatorname{cos}⁡t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(-\frac{37}{3},\,0)$ **correct**
- $(-16,\,0)$
- $(-\frac{85}{3},\,0)$
- $(\frac{59}{3},\,0)$
- $(\frac{11}{3},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =4\operatorname{sin}⁡(\frac{\pi }{2})+4\operatorname{cos}⁡(\frac{\pi }{2})-\frac{1}{3}=4+0-\frac{1}{3}=\frac{11}{3}, \\ y & =\operatorname{cos}⁡(\frac{\pi }{2})+4=0+4=4\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(\frac{11}{3},4).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=4\operatorname{cos}⁡t-4\operatorname{sin}⁡t,\,{y}^{′}(t)=-\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\operatorname{sin}⁡t(\frac{1}{4\operatorname{cos}⁡t-4\operatorname{sin}⁡t}) \\  & =\frac{\operatorname{sin}⁡t}{4\operatorname{sin}⁡t-4\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{\operatorname{sin}⁡(\frac{\pi }{2})}{4\operatorname{sin}⁡(\frac{\pi }{2})-4\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{1}{4-0} \\  & =\frac{1}{4}\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(\frac{11}{3},4)$ and the slope $m=\frac{1}{4}.$ We get

$$
\begin{aligned}y-4 & =\frac{1}{4}\cdot (x-\frac{11}{3}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-4 & =\frac{1}{4}\cdot (x-\frac{11}{3}) \\ -4 & =\frac{x}{4}-\frac{11}{12} \\ x & =-\frac{37}{3}\end{aligned}
$$

Consequently, $(-\frac{37}{3},\,0)$ is the $x$-intercept.


---

## trig_x_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 2, "b": 1, "c": 3, "h": "-4/5", "k": 4}`.

A curve is defined by the parametric equations

$$
x=2\operatorname{sin}⁡t+\operatorname{cos}⁡t-\frac{4}{5},\,y=3\operatorname{cos}⁡t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(-\frac{2}{15},\,0)$ **correct**
- $(-\frac{14}{5},\,0)$
- $(\frac{38}{15},\,0)$
- $(-\frac{4}{3},\,0)$
- $(\frac{6}{5},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =2\operatorname{sin}⁡(\frac{\pi }{2})+\operatorname{cos}⁡(\frac{\pi }{2})-\frac{4}{5}=2+0-\frac{4}{5}=\frac{6}{5}, \\ y & =3\operatorname{cos}⁡(\frac{\pi }{2})+4=0+4=4\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(\frac{6}{5},4).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=2\operatorname{cos}⁡t-\operatorname{sin}⁡t,\,{y}^{′}(t)=-3\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-3\operatorname{sin}⁡t(\frac{1}{2\operatorname{cos}⁡t-\operatorname{sin}⁡t}) \\  & =\frac{3\operatorname{sin}⁡t}{\operatorname{sin}⁡t-2\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{3\operatorname{sin}⁡(\frac{\pi }{2})}{\operatorname{sin}⁡(\frac{\pi }{2})-2\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{3}{1-0} \\  & =3\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(\frac{6}{5},4)$ and the slope $m=3.$ We get

$$
\begin{aligned}y-4 & =3\cdot (x-\frac{6}{5}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-4 & =3\cdot (x-\frac{6}{5}) \\ -4 & =3 x-\frac{18}{5} \\ x & =-\frac{2}{15}\end{aligned}
$$

Consequently, $(-\frac{2}{15},\,0)$ is the $x$-intercept.


---

## log_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"k": 4, "n": 2}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+4),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e^{2}$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Give exact answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{8}{7}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e^{2}$ into the parametric equations:

$$
\begin{aligned}x & =e^{2}(\operatorname{ln}⁡e^{2}+4)=6e^{2} \\ y & =\operatorname{ln}⁡e^{2}=2\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(6e^{2},2).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+5,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+5)}.\end{aligned}
$$

At the point where $t=e^{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e^{2}} & =\frac{1}{e^{2}(\operatorname{ln}⁡e^{2}+5)} \\  & =\frac{1}{7e^{2}}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(6e^{2},2)$ and the slope $m=\frac{1}{7e^{2}}.$ We get

$$
\begin{aligned}y-2=\frac{1}{7e^{2}}(x-6e^{2}).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-2 & =\frac{1}{7e^{2}}(0-6e^{2}) \\ y-2 & =-\frac{6}{7} \\ y & =\frac{8}{7}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{8}{7}).$


---

## log_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"k": 1, "n": 1}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+1),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Give exact answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{1}{3}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e$ into the parametric equations:

$$
\begin{aligned}x & =e(\operatorname{ln}⁡e+1)=2e \\ y & =\operatorname{ln}⁡e=1\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(2e,1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+2,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+2)}.\end{aligned}
$$

At the point where $t=e,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e} & =\frac{1}{e(\operatorname{ln}⁡e+2)} \\  & =\frac{1}{3e}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(2e,1)$ and the slope $m=\frac{1}{3e}.$ We get

$$
\begin{aligned}y-1=\frac{1}{3e}(x-2e).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-1 & =\frac{1}{3e}(0-2e) \\ y-1 & =-\frac{2}{3} \\ y & =\frac{1}{3}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{1}{3}).$


---

## linear_cubic — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": -4, "b": -5, "c": -3, "d": -5, "u": -2}`.

A curve is defined by the parametric equations

$$
x=-4 t-5,\qquad y=-3 t^{3}-5 t,\qquad -\infty<t<\infty.
$$

Calculate the equation of the tangent to the curve at the point where $t=-2.$

selection:

- $y-34=-\frac{41}{4}(x-3)$
- $y-34=\frac{4}{41}(x-3)$
- $y-34=\frac{41}{4}(x-3)$ **correct**
- $y+34=\frac{41}{4}(x-3)$
- $y-34=\frac{41}{4}(x+3)$

First, we find the coordinates of the point by substituting $t=-2$ into the parametric equations:

$$
\begin{aligned}x & =-4 (-2)-5=8-5=3 \\ y & =-3 (-2)^{3}-5 (-2)=24+10=34\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(3,34).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=-4,\qquad y'(t)=-9 t^{2}-5.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{-9 t^{2}-5}{-4}.
$$

At the point where $t=-2,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{-9 (-2)^{2}-5}{-4}=\frac{-41}{-4}=\frac{41}{4}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(3,34)$ and the slope $m=\frac{41}{4}.$ We get

$$
y-34=\frac{41}{4}(x-3).
$$


---

## polynomial_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "b": 6, "c": 4, "d": -6, "u": -2}`.

A curve is defined by the parametric equations

$$
x=3{t}^{3}-6t,\,y=4{t}^{2}-6,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=-2.$

selection:

- $y-10=\frac{8}{15}(x+12)$
- $y-10=-\frac{15}{8}(x+12)$
- $y-10=-\frac{8}{15}(x+12)$ **correct**
- $y+10=-\frac{8}{15}(x+12)$
- $y-10=-\frac{8}{15}(x-12)$

First, we find the coordinates of the point by substituting $t=-2$ into the parametric equations:

$$
\begin{aligned}x & =3(-2)^{3}-6(-2)=-24-(-12)=-12, \\ y & =4(-2)^{2}-6=16-6=10\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(-12,10).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=9{t}^{2}-6,\,{y}^{′}(t)=8t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{8t}{9{t}^{2}-6}\,.\end{aligned}
$$

At the point where $t=-2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=-2} & =\frac{8\cdot (-2)}{9\cdot (-2)^{2}-6} \\  & =\frac{-16}{36-6} \\  & =-\frac{8}{15}\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(-12,10)$ and the slope $m=-\frac{8}{15}.$ We get

$$
\begin{aligned}y-10 & =-\frac{8}{15}(x+12).\end{aligned}
$$


---

## polynomial_blank — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "b": 6, "c": 4, "d": 6, "u": 2}`.

A curve is defined by the parametric equations

$$
x=3{t}^{3}-6t,\,y=4{t}^{2}+6,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $\frac{8 x}{15}+\frac{78}{5}$ **correct**

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =3(2)^{3}-6(2)=24-12=12 \\ y & =4(2)^{2}+6=4(4)+6=22\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(12,22).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=9{t}^{2}-6,\,{y}^{′}(t)=8t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{8t}{9{t}^{2}-6}.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,2} & =\frac{8(2)}{9(2)^{2}-6} \\  & =\frac{16}{9(4)-6} \\  & =\frac{16}{36-6} \\  & =\frac{16}{30} \\  & =\frac{8}{15}.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(12,22)$ and the slope $m=\frac{8}{15}.$ We get

$$
\begin{aligned}y-22 & =\frac{8}{15}(x-12) \\ y-22 & =\frac{8 x}{15}-\frac{32}{5} \\ y & =\frac{8 x}{15}+\frac{78}{5}.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=\frac{8 x}{15}+\frac{78}{5}.$


---

## quintic_radio — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 3, "b": 4, "c": 3, "u": -1}`.

A curve is defined by the parametric equations
$x = 3t^{2} - 4t, y = 3t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

selection:

- $y+3=\frac{3}{2}(x-7)$
- $y+3=-\frac{2}{3}(x-7)$
- $y+3=-\frac{3}{2}(x-7)$ **correct**
- $y-3=-\frac{3}{2}(x-7)$
- $y+3=-\frac{3}{2}(x+7)$

First, we find the coordinates of the point by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =3 (-1)^{2}-4 (-1)=3+4=7 \\ y & =3 (-1)^{5}=-3=-3\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(7,-3).$

To find the slope of the tangent line, we need to find $\dfrac{\mathrm{d}y}{\mathrm{d}x}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=6 t-4,\qquad y'(t)=15 t^{4}.
$$

So, we have

$$
\frac{\mathrm{d}y}{\mathrm{d}x}=\frac{y'(t)}{x'(t)}=\frac{15 t^{4}}{6 t-4}.
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m & =\frac{15 (-1)^{4}}{6 (-1)-4}=\frac{15}{-10}=-\frac{3}{2}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $(x_1,y_1)=(7,-3)$ and the slope $m=-\frac{3}{2}.$ We get

$$
y+3=-\frac{3}{2}(x-7).
$$


---

## exponential_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 5, "h": 4, "w": 3}`.

A curve is defined by the parametric equations

$$
x={e}^{5t}+4,\,y={e}^{t}\operatorname{sin}⁡(3\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,3\pi)$
- $(0,-15\pi)$
- $(0,-3\pi)$ **correct**
- $(0,\frac{3\pi }{5})$
- $(0,0)$

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{5\cdot 0}+4=1+4=5, \\ y & ={e}^{0}\operatorname{sin}⁡(3\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(5,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=5{e}^{5t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(3\pi t)+3\pi \operatorname{cos}⁡(3\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(3\pi t)+3\pi \operatorname{cos}⁡(3\pi t))}{5{e}^{5t}} \\  & =\frac{\operatorname{sin}⁡(3\pi t)+3\pi \operatorname{cos}⁡(3\pi t)}{5{e}^{4t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(3\pi \cdot 0)+3\pi \operatorname{cos}⁡(3\pi \cdot 0)}{5{e}^{4\cdot 0}} \\  & =\frac{0+3\pi }{5} \\  & =\frac{3\pi }{5}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(5,0)$ and the slope $m=\frac{3\pi }{5}.$ We get

$$
\begin{aligned}y-0 & =\frac{3\pi }{5}(x-5).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{3\pi }{5}(0-5) \\ y & =-3\pi\,.\end{aligned}
$$

Consequently, $(0,-3\pi)$ is the $y$-intercept.


---

## trig_x_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"a": 1, "b": 4, "c": 3, "h": "-6/5", "k": 4}`.

A curve is defined by the parametric equations

$$
x=\operatorname{sin}⁡t+4\operatorname{cos}⁡t-\frac{6}{5},\,y=3\operatorname{cos}⁡t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(\frac{77}{15},\,0)$
- $(-\frac{103}{15},\,0)$
- $(-\frac{83}{15},\,0)$ **correct**
- $(-\frac{16}{3},\,0)$
- $(-\frac{1}{5},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{sin}⁡(\frac{\pi }{2})+4\operatorname{cos}⁡(\frac{\pi }{2})-\frac{6}{5}=1+0-\frac{6}{5}=-\frac{1}{5}, \\ y & =3\operatorname{cos}⁡(\frac{\pi }{2})+4=0+4=4\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(-\frac{1}{5},4).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{cos}⁡t-4\operatorname{sin}⁡t,\,{y}^{′}(t)=-3\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-3\operatorname{sin}⁡t(\frac{1}{\operatorname{cos}⁡t-4\operatorname{sin}⁡t}) \\  & =\frac{3\operatorname{sin}⁡t}{4\operatorname{sin}⁡t-\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{3\operatorname{sin}⁡(\frac{\pi }{2})}{4\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{3}{4-0} \\  & =\frac{3}{4}\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(-\frac{1}{5},4)$ and the slope $m=\frac{3}{4}.$ We get

$$
\begin{aligned}y-4 & =\frac{3}{4}\cdot (x+\frac{1}{5}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-4 & =\frac{3}{4}\cdot (x+\frac{1}{5}) \\ -4 & =\frac{3 x}{4}+\frac{3}{20} \\ x & =-\frac{83}{15}\end{aligned}
$$

Consequently, $(-\frac{83}{15},\,0)$ is the $x$-intercept.


---

## log_y_intercept — generated variant (authored bank)

Profile: `authored_operations`; parameters: `{"k": 4, "n": 3}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+4),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e^{3}$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Give exact answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{17}{8}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e^{3}$ into the parametric equations:

$$
\begin{aligned}x & =e^{3}(\operatorname{ln}⁡e^{3}+4)=7e^{3} \\ y & =\operatorname{ln}⁡e^{3}=3\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(7e^{3},3).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+5,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+5)}.\end{aligned}
$$

At the point where $t=e^{3},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e^{3}} & =\frac{1}{e^{3}(\operatorname{ln}⁡e^{3}+5)} \\  & =\frac{1}{8e^{3}}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(7e^{3},3)$ and the slope $m=\frac{1}{8e^{3}}.$ We get

$$
\begin{aligned}y-3=\frac{1}{8e^{3}}(x-7e^{3}).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-3 & =\frac{1}{8e^{3}}(0-7e^{3}) \\ y-3 & =-\frac{7}{8} \\ y & =\frac{17}{8}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{17}{8}).$


---

## polynomial_radio — changed-parameter raw evidence variant

Profile: `observed_17592186083912`; parameters: `{"a": 2, "b": 3, "c": 3, "d": -6, "u": 1}`.

A curve is defined by the parametric equations

$$
x=2{t}^{3}-3t,\,y=3{t}^{2}-6,\,-\infty <t<\infty .
$$

Calculate the equation of the tangent to the curve at the point where $t=1.$

selection:

- $y+3=2(x+1)$ **correct**
- $y+3=(x+1)$
- $y=\frac{24}{11}\,x+\frac{2}{11}$
- $y+3=(x+3)$
- $y+3=2(x+3)$

First, we find the coordinates of the point by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =2(1)^{3}-3(1)=2-3=-1, \\ y & =3(1)^{2}-6=3-6=-3\,.\end{aligned}
$$

So we're looking to find the equation of the tangent at the point $(-1,-3).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=6{t}^{2}-3,\,{y}^{′}(t)=6t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6t}{6{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6\cdot 1}{6\cdot (1)^{2}-3} \\  & =\frac{6}{6-3} \\  & =2\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(-1,-3)$ and the slope $m=2.$ We get

$$
\begin{aligned}y+3 & =2(x+1).\end{aligned}
$$


---

## quintic_radio — changed-parameter raw evidence variant

Profile: `observed_17592186083913`; parameters: `{"a": 1, "b": 3, "c": 1, "u": -1}`.

A curve is defined by the parametric equations
$x = t^{2} - 3t, y = t^{5}, - ∞ < t < ∞$.

Calculate the equation of the tangent to the curve at the point where $t =-1$.

> A scientific calculator is required to answer this question.

selection:

- $y+1 =-1(x-4)$
- $y+1 =-1(x+4)$
- $y-1 =-\frac{3}{5}(x-4)$
- $y+1 = 1(x-4)$
- $y-1 =-2(x-4)$




---

## exponential_y_intercept — changed-parameter raw evidence variant

Profile: `observed_17592186256700`; parameters: `{"a": 3, "h": 3, "w": 1}`.

A curve is defined by the parametric equations

$$
x={e}^{3t}+3,\,y={e}^{t}\operatorname{sin}⁡(\pi t),\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $y$-axis.

selection:

- $(0,-\pi)$
- $(0,\frac{\pi }{4})$
- $(0,\frac{\pi }{3})$
- $(0,-\frac{\pi }{12})$
- $(0,-\frac{4\pi }{3})$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={e}^{3\cdot 0}+3=1+3=4, \\ y & ={e}^{0}\operatorname{sin}⁡(\pi \cdot 0)=0\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(4,0).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{e}^{3t},\,{y}^{′}(t)={e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)),
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t))}{3{e}^{3t}} \\  & =\frac{\operatorname{sin}⁡(\pi t)+\pi \operatorname{cos}⁡(\pi t)}{3{e}^{2t}}.\end{aligned}
$$

At the point where $t=0,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =\frac{\operatorname{sin}⁡(\pi \cdot 0)+\pi \operatorname{cos}⁡(\pi \cdot 0)}{3{e}^{2\cdot 0}} \\  & =\frac{0+\pi }{3} \\  & =\frac{\pi }{3}\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(4,0)$ and the slope $m=\frac{\pi }{3}.$ We get

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(x-4).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-0 & =\frac{\pi }{3}(0-4) \\ y & =-\frac{4\pi }{3}\,.\end{aligned}
$$

Consequently, $(0,-\frac{4\pi }{3})$ is the $y$-intercept.


---

## trig_x_intercept — changed-parameter raw evidence variant

Profile: `observed_17592186275337`; parameters: `{"a": 1, "b": 1, "c": 1, "h": "2/3", "k": 1}`.

A curve is defined by the parametric equations

$$
x=\operatorname{sin}⁡t+\operatorname{cos}⁡t+\frac{2}{3},\,y=\operatorname{cos}⁡t+1,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Determine the point at which the tangent to the curve at $C$ crosses the $x$-axis.

selection:

- $(\frac{4}{7},\,0)$
- $(\frac{2}{3},\,0)$ **correct**
- $(\frac{4}{9},\,0)$
- $(\frac{1}{2},\,0)$
- $(\frac{4}{5},\,0)$

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{sin}⁡(\frac{\pi }{2})+\operatorname{cos}⁡(\frac{\pi }{2})+\frac{2}{3}=1+0+\frac{2}{3}=\frac{5}{3}, \\ y & =\operatorname{cos}⁡(\frac{\pi }{2})+1=0+1=1\,.\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(\frac{5}{3},1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{cos}⁡t-\operatorname{sin}⁡t,\,{y}^{′}(t)=-\operatorname{sin}⁡t.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\operatorname{sin}⁡t(\frac{1}{\operatorname{cos}⁡t-\operatorname{sin}⁡t}) \\  & =\frac{\operatorname{sin}⁡t}{\operatorname{sin}⁡t-\operatorname{cos}⁡t}\,.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =\frac{\operatorname{sin}⁡(\frac{\pi }{2})}{\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{1}{1-0} \\  & =1\,.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(\frac{5}{3},1)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-1 & =1\cdot (x-\frac{5}{3}).\end{aligned}
$$

The tangent crosses the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-1 & =1\cdot (x-\frac{5}{3}) \\ -1 & =x-\frac{5}{3} \\ x & =\frac{2}{3}\end{aligned}
$$

Consequently, $(\frac{2}{3},\,0)$ is the $x$-intercept.


---

## polynomial_blank — changed-parameter raw evidence variant

Profile: `observed_17592186319229`; parameters: `{"a": 1, "b": 4, "c": 2, "d": 2, "u": 2}`.

A curve is defined by the parametric equations

$$
x={t}^{3}-4t,\,y=2{t}^{2}+2,\,-\infty <t<\infty .
$$

Find the Cartesian equation of the tangent to the curve at the point where $t=2.$

The Cartesian equation of the tangent line is $y=$
{{field-1}}.

field-1:

- $x+10$ **correct**

First, we find the coordinates of the point by substituting $t=2$ into the parametric equations:

$$
\begin{aligned}x & =(2)^{3}-4(2)=8-8=0 \\ y & =2(2)^{2}+2=2(4)+2=10\end{aligned}
$$

So, we're looking to find the equation of the tangent at the point $(0,10).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-4,\,{y}^{′}(t)=4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{4t}{3{t}^{2}-4}.\end{aligned}
$$

At the point where $t=2,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,2} & =\frac{4(2)}{3(2)^{2}-4} \\  & =\frac{8}{3(4)-4} \\  & =\frac{8}{12-4} \\  & =\frac{8}{8} \\  & =1.\end{aligned}
$$

Finally, to calculate the Cartesian equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,10)$ and the slope $m=1.$ We get

$$
\begin{aligned}y-10 & =1(x-0) \\ y-10 & =x \\ y & =x+10.\end{aligned}
$$

Therefore the equation of the tangent line  in slope-intercept form is $y=x+10.$


---

## log_y_intercept — changed-parameter raw evidence variant

Profile: `observed_17592186319230`; parameters: `{"k": 3, "n": 1}`.

A curve is defined by the parametric equations

$$
x=t(\operatorname{ln}⁡t+3),\,y=\operatorname{ln}⁡t,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=e$ on the curve. Determine the coordinates of the point at which the tangent to the curve at $C$ crosses the $y$-axis. Do not round the answers.

The tangent to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:

- $\frac{1}{5}$ **correct**
field-1:

- $0$ **correct**

First, we find the coordinates of the point $C$ by substituting $t=e$ into the parametric equations:

$$
\begin{aligned}x & =e(\operatorname{ln}⁡e+3)=4e \\ y & =\operatorname{ln}⁡e=1\end{aligned}
$$

So, we're looking to find the equation of the tangent line to the curve at the point $(4e,1).$ 

To find the equation of the tangent line, we need to find $\frac{dy}{dx}.$ To compute it, we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\operatorname{ln}⁡t+4,\,{y}^{′}(t)=\frac{1}{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{1}{t(\operatorname{ln}⁡t+4)}.\end{aligned}
$$

At the point where $t=e,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,e} & =\frac{1}{e(\operatorname{ln}⁡e+4)} \\  & =\frac{1}{5e}.\end{aligned}
$$

Finally, to calculate the equation of the tangent line, we use point-slope form with the point $({x}_{1},{y}_{1})=(4e,1)$ and the slope $m=\frac{1}{5e}.$ We get

$$
\begin{aligned}y-1=\frac{1}{5e}(x-4e).\end{aligned}
$$

The tangent crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y-1 & =\frac{1}{5e}(0-4e) \\ y-1 & =-\frac{4}{5} \\ y & =\frac{1}{5}.\end{aligned}
$$

Consequently, the tangent to the curve at $C$ crosses the $y$-axis at $(0,\,\frac{1}{5}).$
