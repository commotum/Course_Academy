# Normal-line review

Raw originals, changed evidence profiles and authored normal variants are distinguished below.

## Observed evidence — quartic_axis

![](images/d4/d40bd1a54762b360dc590f014d1df9731168f8620df07ee8f0294bd078fc8da5.png)

The curve shown above is defined by the parametric equations
$x = t^{4} + t, y = t^{2}, - ∞ < t < ∞$.

Let $C$ be the point that corresponds to $t =-1$ on the curve. Determine the point at which the normal to the curve at $C$ crosses the $x$-axis.

selection:
- $(\frac{5}{8}, 0)$
- $(\frac{7}{12}, 0)$
- $(\frac{3}{5}, 0)$
- $(\frac{2}{3}, 0)$
- $(\frac{4}{7}, 0)$

---

## Observed evidence — log_sine

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡(\operatorname{sin}⁡t),\,y=\frac{1}{\operatorname{sin}⁡t}\,,\,t\in (0,\pi ).
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=x$
- $y=x+2$
- $y=x+1$
- $y=2x+3$
- $y=2x+1$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡[\operatorname{sin}⁡(\frac{\pi }{2})]=\operatorname{ln}⁡1=0, \\ y & =\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}=1\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(0,1).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t},\,{y}^{′}(t)=-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t} \\  & =-\frac{1}{\operatorname{sin}⁡t}.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =-\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}=-1.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(-1)\,}=1
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,1)$ and the slope ${m}_{n}=1.$ We get

$$
\begin{aligned}y-1 & =1\cdot (x-0) \\ y & =x+1.\end{aligned}
$$

---

## Observed evidence — log_power

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡({t}^{2}),\,y=2{t}^{3}-3t\,,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\frac{3}{2}x-1$
- $y=\frac{4}{3}x+2$
- $y=-\frac{2}{3}x+2$
- $y=-\frac{2}{3}x-1$
- $y=\frac{2}{3}x+1$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡({1}^{2})=\operatorname{ln}⁡1=0, \\ y & =2(1)^{3}-3(1)=-1\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(0,-1).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{2}{t},\,{y}^{′}(t)=6{t}^{2}-3
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-3}{\frac{2}{t}} \\  & =\frac{6{t}^{3}-3t}{2}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{3}-3(1)}{2}=\frac{3}{2}.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{3}{2})\,}=-\frac{2}{3}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,-1)$ and the slope ${m}_{n}=-\frac{2}{3}.$ We get

$$
\begin{aligned}y+1 & =-\frac{2}{3}\cdot (x-0) \\ y & =-\frac{2}{3}x-1.\end{aligned}
$$

---

## Observed evidence — cubic_axis

A curve is defined by the parametric equations

$$
x={t}^{2}+\frac{1}{2}t+\frac{1}{2},\,y={t}^{3}+7{t}^{2}+8t,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $x$-axis. Do not round the answers.

The normal to the curve at $C$ crosses the $x$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $-3$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}+\frac{1}{2}(-1)+\frac{1}{2}=1-\frac{1}{2}+\frac{1}{2}=1 \\ y & =(-1)^{3}+7(-1)^{2}+8(-1)=-1+7-8=-2\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(1,-2).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=2t+\frac{1}{2},\,{y}^{′}(t)=3{t}^{2}+14t+8
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{3{t}^{2}+14t+8}{2t+\frac{1}{2}}.\end{aligned}
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,-1} & =\frac{3(-1)^{2}+14(-1)+8}{2(-1)+\frac{1}{2}} \\  & =\frac{-3}{(-\frac{3}{2})} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(1,-2)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}y-(-2) & =-\frac{1}{2}(x-1) \\ y+2 & =-\frac{1}{2}(x-1).\end{aligned}
$$

The normal intersects the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0+2 & =-\frac{1}{2}(x-1) \\ -\frac{1}{2}(x-1) & =2 \\ x-1 & =-4 \\ x & =-3.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $x$-axis at $(-3,\,0).$

---

## Observed evidence — sixth_axis

A curve is defined by the parametric equations

$$
x=7{t}^{2}-9t,\,y={t}^{6}+2{t}^{2},\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $y$-axis. Do not round the answers.

The normal to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:
- $2$

field-1:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =7({1}^{2})-9(1)=-2 \\ y & ={1}^{6}+2({1}^{2})=3\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(-2,3).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=14t-9,\,{y}^{′}(t)=6{t}^{5}+4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{5}+4t}{14t-9}.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,1} & =\frac{6({1}^{5})+4(1)}{14(1)-9} \\  & =\frac{10}{5} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,3)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}y-3 & =-\frac{1}{2}(x-(-2)) \\ y-3 & =-\frac{1}{2}(x+2) \\ y-3 & =-\frac{1}{2}x-1 \\ y & =-\frac{1}{2}x-1+3 \\ y & =-\frac{1}{2}x+2.\end{aligned}
$$

The normal crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y & =-\frac{1}{2}(0)+2 \\ y & =2.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $y$-axis at $(0,\,2).$

---

## Observed evidence — cubic_linear

A curve is defined by the parametric equations

$$
x={t}^{3}-3t,\,y=2-t,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\,\frac{9}{4}x+2$
- $y=-3x+\frac{12}{5}$
- $y=-3x+2$
- $y=-\,\frac{9}{4}x+\frac{8}{3}$
- $y=-\,\frac{12}{5}x+2$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={0}^{3}-3\cdot 0=0-0=0, \\ y & =2-0=2\,.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(0,2).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-3,\,{y}^{′}(t)=-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =(-1)\cdot \frac{1}{3{t}^{2}-3} \\  & =-\,\frac{1}{3{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=0,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =-\,\frac{1}{3\cdot {0}^{2}-3} \\  & =-\,\frac{1}{0-3} \\  & =\frac{1}{3}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{1}{3})\,}=-3
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,2)$ and the slope ${m}_{n}=-3.$ We get

$$
\begin{aligned}y-2 & =-3(x-0) \\ y & =-3x+2\,.\end{aligned}
$$

---

## Observed evidence — exponential

A curve is defined by the parametric equations

$$
x={e}^{t},\,y=2t{e}^{t}-2{e}^{t},\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\frac{x}{4}+\frac{2e}{3}$
- $y=-\frac{x}{2}+\frac{e}{2}$
- $y=\frac{x}{3}+\frac{e}{4}$
- $y=\frac{x}{2}+\frac{2}{e}$
- $y=\frac{x}{2}-\frac{e}{4}$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =e, \\ y & =2(1){e}^{1}-2{e}^{1}=0\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(e,0).$  For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)={e}^{t},\,{y}^{′}(t)=2t{e}^{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t{e}^{t}}{{e}^{t}} \\  & =2t\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =2(1)=2\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,2\,}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(e,0)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}y-0 & =(-\frac{1}{2})(x-e) \\ y & =-\frac{x}{2}+\frac{e}{2}\,.\end{aligned}
$$

---

## Observed evidence — quartic_cubic

A curve is defined by the parametric equations

$$
x={t}^{4}-3{t}^{2},\,y=2{t}^{3}-t,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{2}{5}(x+2)+1$
- $y=\frac{5}{2}(x+2)+1$
- $y=\frac{2}{5}(x+2)-1$
- $y=\frac{5}{2}(x+2)-1$
- $y=\frac{2}{5}(x-2)+1$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =(1)^{4}-3(1)^{2}=-2, \\ y & =2(1)^{3}-1=1\,.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-2,1).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=4{t}^{3}-6t,\,{y}^{′}(t)=6{t}^{2}-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-1}{4{t}^{3}-6t}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{2}-1}{4(1)^{3}-6(1)} \\  & =\frac{5}{-2} \\  & =-\,\frac{5}{2}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{(\,-\frac{5}{2}\,)}=\frac{2}{5}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,1)$ and the slope ${m}_{n}=\frac{2}{5}.$ We get

$$
\begin{aligned}y-1 & =\frac{2}{5}(x+2) \\ y & =\frac{2}{5}(x+2)+1\,.\end{aligned}
$$

---

## Observed evidence — log_sine

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡(\operatorname{sin}⁡t)+2,\,y=\frac{1}{\operatorname{sin}⁡t}\,+4,\,t\in (0,\pi ).
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=(x-2)+4$
- $y=(x-2)+2+4$
- $y=(x-2)+1+4$
- $y=2(x-2)+3+4$
- $y=2(x-2)+1+4$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡[\operatorname{sin}⁡(\frac{\pi }{2})]+2=\operatorname{ln}⁡1+2=0+2, \\ y & =\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}+4=1+4\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(2,5).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t},\,{y}^{′}(t)=-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t} \\  & =-\frac{1}{\operatorname{sin}⁡t}.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =-\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}=-1.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(-1)\,}=1
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,5)$ and the slope ${m}_{n}=1.$ We get

$$
\begin{aligned}(y-4)-1 & =1\cdot ((x-2)-0) \\ (y-4) & =(x-2)+1.\end{aligned}
$$

---

## Observed evidence — log_power

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡({t}^{2})+2,\,y=2{t}^{3}-3t\,+4,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\frac{3}{2}(x-2)-1+4$
- $y=\frac{4}{3}(x-2)+2+4$
- $y=-\frac{2}{3}(x-2)+2+4$
- $y=-\frac{2}{3}(x-2)-1+4$
- $y=\frac{2}{3}(x-2)+1+4$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡({1}^{2})+2=\operatorname{ln}⁡1+2=0+2, \\ y & =2(1)^{3}-3(1)+4=-1+4\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(2,3).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{2}{t},\,{y}^{′}(t)=6{t}^{2}-3
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-3}{\frac{2}{t}} \\  & =\frac{6{t}^{3}-3t}{2}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{3}-3(1)}{2}=\frac{3}{2}.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{3}{2})\,}=-\frac{2}{3}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,3)$ and the slope ${m}_{n}=-\frac{2}{3}.$ We get

$$
\begin{aligned}(y-4)+1 & =-\frac{2}{3}\cdot ((x-2)-0) \\ (y-4) & =-\frac{2}{3}(x-2)-1.\end{aligned}
$$

---

## Observed evidence — cubic_axis

A curve is defined by the parametric equations

$$
x={t}^{2}+\frac{1}{2}t+\frac{1}{2}+2,\,y={t}^{3}+7{t}^{2}+8t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $x$-axis. Do not round the answers.

The normal to the curve at $C$ crosses the $x$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $7$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}+\frac{1}{2}(-1)+\frac{1}{2}+2=1-\frac{1}{2}+\frac{1}{2}+2=1+2 \\ y & =(-1)^{3}+7(-1)^{2}+8(-1)+4=-1+7-8+4=-2+4\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(3,2).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=2t+\frac{1}{2},\,{y}^{′}(t)=3{t}^{2}+14t+8
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{3{t}^{2}+14t+8}{2t+\frac{1}{2}}.\end{aligned}
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,-1} & =\frac{3(-1)^{2}+14(-1)+8}{2(-1)+\frac{1}{2}} \\  & =\frac{-3}{(-\frac{3}{2})} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(3,2)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-4)-(-2) & =-\frac{1}{2}((x-2)-1) \\ (y-4)+2 & =-\frac{1}{2}((x-2)-1).\end{aligned}
$$

The normal intersects the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-(2) & =- \frac{1}{2}(x-(3)) \\ - \frac{1}{2}(x-(3)) & =-2 \\ x-(3) & =4 \\ x & =7.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $x$-axis at $(7,\,0).$

---

## Observed evidence — sixth_axis

A curve is defined by the parametric equations

$$
x=7{t}^{2}-9t+2,\,y={t}^{6}+2{t}^{2}+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $y$-axis. Do not round the answers.

The normal to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-2:
- $7$

field-1:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =7({1}^{2})-9(1)+2=-2+2 \\ y & ={1}^{6}+2({1}^{2})+4=3+4\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(0,7).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=14t-9,\,{y}^{′}(t)=6{t}^{5}+4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{5}+4t}{14t-9}.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,1} & =\frac{6({1}^{5})+4(1)}{14(1)-9} \\  & =\frac{10}{5} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,7)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-4)-3 & =-\frac{1}{2}((x-2)-(-2)) \\ (y-4)-3 & =-\frac{1}{2}((x-2)+2) \\ (y-4)-3 & =-\frac{1}{2}(x-2)-1 \\ (y-4) & =-\frac{1}{2}(x-2)-1+3 \\ (y-4) & =-\frac{1}{2}(x-2)+2.\end{aligned}
$$

The normal crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y & =- \frac{1}{2}(0-(0))+7 \\ y & =7.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $y$-axis at $(0,\,7).$

---

## Observed evidence — cubic_linear

A curve is defined by the parametric equations

$$
x={t}^{3}-3t+2,\,y=2-t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\,\frac{9}{4}(x-2)+2+4$
- $y=-3(x-2)+\frac{12}{5}+4$
- $y=-3(x-2)+2+4$
- $y=-\,\frac{9}{4}(x-2)+\frac{8}{3}+4$
- $y=-\,\frac{12}{5}(x-2)+2+4$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={0}^{3}-3\cdot 0+2=0-0+2=0+2, \\ y & =2-0+4=2\,+4.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(2,6).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-3,\,{y}^{′}(t)=-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =(-1)\cdot \frac{1}{3{t}^{2}-3} \\  & =-\,\frac{1}{3{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=0,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =-\,\frac{1}{3\cdot {0}^{2}-3} \\  & =-\,\frac{1}{0-3} \\  & =\frac{1}{3}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{1}{3})\,}=-3
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(2,6)$ and the slope ${m}_{n}=-3.$ We get

$$
\begin{aligned}(y-4)-2 & =-3((x-2)-0) \\ (y-4) & =-3(x-2)+2\,.\end{aligned}
$$

---

## Observed evidence — exponential

A curve is defined by the parametric equations

$$
x={e}^{t}+2,\,y=2t{e}^{t}-2{e}^{t}+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=-\frac{(x-2)}{4}+\frac{2e}{3}+4$
- $y=-\frac{(x-2)}{2}+\frac{e}{2}+4$
- $y=\frac{(x-2)}{3}+\frac{e}{4}+4$
- $y=\frac{(x-2)}{2}+\frac{2}{e}+4$
- $y=\frac{(x-2)}{2}-\frac{e}{4}+4$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =e+2, \\ y & =2(1){e}^{1}-2{e}^{1}+4=0+4\end{aligned}
$$

So we're looking to find the equation of the tangent line to the curve at the point $(2 + e,4).$  For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)={e}^{t},\,{y}^{′}(t)=2t{e}^{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t{e}^{t}}{{e}^{t}} \\  & =2t\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =2(1)=2\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,2\,}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(2 + e,4)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-4)-0 & =(-\frac{1}{2})((x-2)-e) \\ (y-4) & =-\frac{(x-2)}{2}+\frac{e}{2}\,.\end{aligned}
$$

---

## Observed evidence — quartic_cubic

A curve is defined by the parametric equations

$$
x={t}^{4}-3{t}^{2}+2,\,y=2{t}^{3}-t+4,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{2}{5}((x-2)+2)+1+4$
- $y=\frac{5}{2}((x-2)+2)+1+4$
- $y=\frac{2}{5}((x-2)+2)-1+4$
- $y=\frac{5}{2}((x-2)+2)-1+4$
- $y=\frac{2}{5}((x-2)-2)+1+4$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =(1)^{4}-3(1)^{2}+2=-2+2, \\ y & =2(1)^{3}-1+4=1\,+4.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(0,5).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=4{t}^{3}-6t,\,{y}^{′}(t)=6{t}^{2}-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-1}{4{t}^{3}-6t}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{2}-1}{4(1)^{3}-6(1)} \\  & =\frac{5}{-2} \\  & =-\,\frac{5}{2}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{(\,-\frac{5}{2}\,)}=\frac{2}{5}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,5)$ and the slope ${m}_{n}=\frac{2}{5}.$ We get

$$
\begin{aligned}(y-4)-1 & =\frac{2}{5}((x-2)+2) \\ (y-4) & =\frac{2}{5}((x-2)+2)+1\,.\end{aligned}
$$

---

## Generated method-bank variant — linear_quadratic

A curve is defined by the parametric equations

$$
x=4 t + 2,\,y=4 t^{2} + 3,\,-\infty<t<\infty.
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=6 - \frac{x}{2}$
- $y=3 - 2 x$
- $y=\frac{x}{2} + 8$
- $y=\frac{x}{2} - 6$
- $y=\frac{x}{2} + 7$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =4(-1)+2=-2, \\ y & =4(-1)^2+3=7.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-2,7).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=4,\quad y\prime(t)=8 t.
$$

So, we have

$$
\frac{dy}{dx}=\frac{y\prime(t)}{x\prime(t)}=\frac{8 t}{4}.
$$

At the point where $t=-1$, the slope $m$ of the tangent line is given by

$$
m=\frac{8(-1)}{4}=-2.
$$

To find the slope $m_n$ of the normal line, we take the negative reciprocal of $m$:

$$
m_n=-\frac{1}{m}=-\frac{1}{(-2)}=\frac{1}{2}.
$$

To calculate the equation of the normal, we use point-slope form:

$$
\begin{aligned}y-(7) & =\frac{1}{2}(x-(-2)) \\ y & =\frac{x}{2} + 8.\end{aligned}
$$

---

## Generated method-bank variant — linear_quadratic

A curve is defined by the parametric equations

$$
x=t - 3,\,y=3 t^{2} + 1,\,-\infty<t<\infty.
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{10}{3} - \frac{x}{6}$
- $y=\frac{x}{6} + 4$
- $y=\frac{x}{6} - \frac{10}{3}$
- $y=\frac{x}{6} + \frac{14}{3}$
- $y=- 6 x - 20$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =1(-1)-3=-4, \\ y & =3(-1)^2+1=4.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-4,4).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
x'(t)=1,\quad y\prime(t)=6 t.
$$

So, we have

$$
\frac{dy}{dx}=\frac{y\prime(t)}{x\prime(t)}=\frac{6 t}{1}.
$$

At the point where $t=-1$, the slope $m$ of the tangent line is given by

$$
m=\frac{6(-1)}{1}=-6.
$$

To find the slope $m_n$ of the normal line, we take the negative reciprocal of $m$:

$$
m_n=-\frac{1}{m}=-\frac{1}{(-6)}=\frac{1}{6}.
$$

To calculate the equation of the normal, we use point-slope form:

$$
\begin{aligned}y-(4) & =\frac{1}{6}(x-(-4)) \\ y & =\frac{x}{6} + \frac{14}{3}.\end{aligned}
$$

---

## Generated method-bank variant — quartic_axis

A curve is defined by the parametric equations
$x = t^{4} + t, y = t^{2}+6, - ∞ < t < ∞$.

Let $C$ be the point that corresponds to $t =-1$ on the curve. Determine the point at which the normal to the curve at $C$ crosses the $x$-axis.

The normal crosses the $x$-axis at $(${{field-1}}, {{field-2}}$).$ Give exact answers.

field-1:
- $\frac{14}{3}$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^4+(-1)+0=0 \\ y & =(-1)^2+6=7.\end{aligned}
$$

For the normal at $(0,7)$, first find the derivatives:

$$
x\prime(t)=4t^3+1,\quad y\prime(t)=2t.
$$

So, we have

$$
\frac{dy}{dx}=\frac{y\prime(t)}{x\prime(t)}=\frac{2t}{4t^3+1}.
$$

At $t=-1$, the tangent slope is

$$
m=\frac{2(-1)}{4(-1)^3+1}=\frac{-2}{-3}=\frac{2}{3}.
$$

To find the normal slope, take the negative reciprocal:

$$
m_n=-\frac{1}{m}=-\frac{1}{(2/3)}=-\frac{3}{2}.
$$

Using point-slope form,

$$
y-(7)=-\frac{3}{2}(x-(0)).
$$

The normal intersects the $x$-axis when $y=0$. At this point,

$$
\begin{aligned}0-(7) & =- \frac{3}{2}(x-(0)) \\ x-(0) & =\frac{14}{3} \\ x & =\frac{14}{3}.\end{aligned}
$$

Consequently, the normal crosses the $x$-axis at $(\frac{14}{3},0).$

---

## Generated method-bank variant — quartic_axis

A curve is defined by the parametric equations
$x = t^{4} + t-4, y = t^{2}+3, - ∞ < t < ∞$.

Let $C$ be the point that corresponds to $t =-1$ on the curve. Determine the point at which the normal to the curve at $C$ crosses the $x$-axis.

The normal crosses the $x$-axis at $(${{field-1}}, {{field-2}}$).$ Give exact answers.

field-1:
- $- \frac{4}{3}$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^4+(-1)-4=-4 \\ y & =(-1)^2+3=4.\end{aligned}
$$

For the normal at $(-4,4)$, first find the derivatives:

$$
x\prime(t)=4t^3+1,\quad y\prime(t)=2t.
$$

So, we have

$$
\frac{dy}{dx}=\frac{y\prime(t)}{x\prime(t)}=\frac{2t}{4t^3+1}.
$$

At $t=-1$, the tangent slope is

$$
m=\frac{2(-1)}{4(-1)^3+1}=\frac{-2}{-3}=\frac{2}{3}.
$$

To find the normal slope, take the negative reciprocal:

$$
m_n=-\frac{1}{m}=-\frac{1}{(2/3)}=-\frac{3}{2}.
$$

Using point-slope form,

$$
y-(4)=-\frac{3}{2}(x-(-4)).
$$

The normal intersects the $x$-axis when $y=0$. At this point,

$$
\begin{aligned}0-(4) & =- \frac{3}{2}(x-(-4)) \\ x-(-4) & =\frac{8}{3} \\ x & =- \frac{4}{3}.\end{aligned}
$$

Consequently, the normal crosses the $x$-axis at $(- \frac{4}{3},0).$

---

## Generated method-bank variant — log_sine

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡(\operatorname{sin}⁡t),\,y=\frac{1}{\operatorname{sin}⁡t}\,+6,\,t\in (0,\pi ).
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=x$
- $y=7 - x$
- $y=x + 7$
- $y=- x$
- $y=x - 7$

Worked solution:
The parameter derivatives both vanish here. The curve lies on $(y-6)=e^{-x}$ with $x\leq 0$, so its endpoint tangent is obtained by the limiting derivative ratio.

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡[\operatorname{sin}⁡(\frac{\pi }{2})]=\operatorname{ln}⁡1=0, \\ y & =\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}+6=1+6\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(0,7).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t},\,{y}^{′}(t)=-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t} \\  & =-\frac{1}{\operatorname{sin}⁡t}.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =-\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}=-1.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(-1)\,}=1
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(0,7)$ and the slope ${m}_{n}=1.$ We get

$$
\begin{aligned}(y-6)-1 & =1\cdot (x-0) \\ (y-6) & =x+1.\end{aligned}
$$

---

## Generated method-bank variant — log_sine

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡(\operatorname{sin}⁡t)+6,\,y=\frac{1}{\operatorname{sin}⁡t}\,+6,\,t\in (0,\pi ).
$$

Let $C$ be the point that corresponds to $t=\frac{\pi }{2}$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=x$
- $y=x - 13$
- $y=- x$
- $y=x + 1$
- $y=13 - x$

Worked solution:
The parameter derivatives both vanish here. The curve lies on $(y-6)=e^{-(x-6)}$ with $x\leq 6$, so its endpoint tangent is obtained by the limiting derivative ratio.

First, we find the coordinates of the point $C$ by substituting $t=\frac{\pi }{2}$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡[\operatorname{sin}⁡(\frac{\pi }{2})]+6=\operatorname{ln}⁡1+6=0+6, \\ y & =\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}+6=1+6\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(6,7).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t},\,{y}^{′}(t)=-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =-\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t} \\  & =-\frac{1}{\operatorname{sin}⁡t}.\end{aligned}
$$

At the point where $t=\frac{\pi }{2},$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=\pi /2} & =-\frac{1}{\operatorname{sin}⁡(\frac{\pi }{2})}=-1.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(-1)\,}=1
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(6,7)$ and the slope ${m}_{n}=1.$ We get

$$
\begin{aligned}(y-6)-1 & =1\cdot ((x-6)-0) \\ (y-6) & =(x-6)+1.\end{aligned}
$$

---

## Generated method-bank variant — log_power

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡({t}^{2})-2,\,y=2{t}^{3}-3t\,+2,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{2 x}{3} + \frac{7}{3}$
- $y=\frac{3 x}{2} + 4$
- $y=- \frac{2 x}{3} - \frac{1}{3}$
- $y=- \frac{2 x}{3} - \frac{7}{3}$
- $y=1 - \frac{2 x}{3}$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡({1}^{2})-2=\operatorname{ln}⁡1-2=0-2, \\ y & =2(1)^{3}-3(1)+2=-1+2\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-2,1).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{2}{t},\,{y}^{′}(t)=6{t}^{2}-3
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-3}{\frac{2}{t}} \\  & =\frac{6{t}^{3}-3t}{2}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{3}-3(1)}{2}=\frac{3}{2}.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{3}{2})\,}=-\frac{2}{3}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,1)$ and the slope ${m}_{n}=-\frac{2}{3}.$ We get

$$
\begin{aligned}(y-2)+1 & =-\frac{2}{3}\cdot ((x+2)-0) \\ (y-2) & =-\frac{2}{3}(x+2)-1.\end{aligned}
$$

---

## Generated method-bank variant — log_power

A curve is defined by the parametric equations

$$
x=\operatorname{ln}⁡({t}^{2})-4,\,y=2{t}^{3}-3t\,+3,\,t\in (0,\infty ).
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{2 x}{3} + \frac{14}{3}$
- $y=2 - \frac{2 x}{3}$
- $y=- \frac{2 x}{3} - \frac{14}{3}$
- $y=- \frac{2 x}{3} - \frac{2}{3}$
- $y=\frac{3 x}{2} + 8$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =\operatorname{ln}⁡({1}^{2})-4=\operatorname{ln}⁡1-4=0-4, \\ y & =2(1)^{3}-3(1)+3=-1+3\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-4,2).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=\frac{2}{t},\,{y}^{′}(t)=6{t}^{2}-3
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-3}{\frac{2}{t}} \\  & =\frac{6{t}^{3}-3t}{2}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{3}-3(1)}{2}=\frac{3}{2}.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{3}{2})\,}=-\frac{2}{3}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-4,2)$ and the slope ${m}_{n}=-\frac{2}{3}.$ We get

$$
\begin{aligned}(y-3)+1 & =-\frac{2}{3}\cdot ((x+4)-0) \\ (y-3) & =-\frac{2}{3}(x+4)-1.\end{aligned}
$$

---

## Generated method-bank variant — cubic_axis

A curve is defined by the parametric equations

$$
x={t}^{2}+\frac{1}{2}t+\frac{1}{2},\,y={t}^{3}+7{t}^{2}+8t+6,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $x$-axis. Give exact answers.

The normal to the curve at $C$ crosses the $x$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $9$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}+\frac{1}{2}(-1)+\frac{1}{2}=1-\frac{1}{2}+\frac{1}{2}=1 \\ y & =(-1)^{3}+7(-1)^{2}+8(-1)+6=-1+7-8+6=-2+6\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(1,4).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=2t+\frac{1}{2},\,{y}^{′}(t)=3{t}^{2}+14t+8
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{3{t}^{2}+14t+8}{2t+\frac{1}{2}}.\end{aligned}
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,-1} & =\frac{3(-1)^{2}+14(-1)+8}{2(-1)+\frac{1}{2}} \\  & =\frac{-3}{(-\frac{3}{2})} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(1,4)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-6)-(-2) & =-\frac{1}{2}(x-1) \\ (y-6)+2 & =-\frac{1}{2}(x-1).\end{aligned}
$$

The normal intersects the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-(4) & =- \frac{1}{2}(x-(1)) \\ - \frac{1}{2}(x-(1)) & =-4 \\ x-(1) & =8 \\ x & =9.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $x$-axis at $(9,\,0).$

---

## Generated method-bank variant — cubic_axis

A curve is defined by the parametric equations

$$
x={t}^{2}+\frac{1}{2}t+\frac{1}{2}-4,\,y={t}^{3}+7{t}^{2}+8t+3,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=-1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $x$-axis. Give exact answers.

The normal to the curve at $C$ crosses the $x$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $-1$

field-2:
- $0$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:

$$
\begin{aligned}x & =(-1)^{2}+\frac{1}{2}(-1)+\frac{1}{2}-4=1-\frac{1}{2}+\frac{1}{2}-4=1-4 \\ y & =(-1)^{3}+7(-1)^{2}+8(-1)+3=-1+7-8+3=-2+3\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(-3,1).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=2t+\frac{1}{2},\,{y}^{′}(t)=3{t}^{2}+14t+8
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{3{t}^{2}+14t+8}{2t+\frac{1}{2}}.\end{aligned}
$$

At the point where $t=-1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,-1} & =\frac{3(-1)^{2}+14(-1)+8}{2(-1)+\frac{1}{2}} \\  & =\frac{-3}{(-\frac{3}{2})} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-3,1)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-3)-(-2) & =-\frac{1}{2}((x+4)-1) \\ (y-3)+2 & =-\frac{1}{2}((x+4)-1).\end{aligned}
$$

The normal intersects the $x$-axis when $y=0.$ At this point, we have

$$
\begin{aligned}0-(1) & =- \frac{1}{2}(x-(-3)) \\ - \frac{1}{2}(x-(-3)) & =-1 \\ x-(-3) & =2 \\ x & =-1.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $x$-axis at $(-1,\,0).$

---

## Generated method-bank variant — sixth_axis

A curve is defined by the parametric equations

$$
x=7{t}^{2}-9t,\,y={t}^{6}+2{t}^{2}+6,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $y$-axis. Give exact answers.

The normal to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $0$

field-2:
- $8$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =7({1}^{2})-9(1)=-2 \\ y & ={1}^{6}+2({1}^{2})+6=3+6\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(-2,9).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=14t-9,\,{y}^{′}(t)=6{t}^{5}+4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{5}+4t}{14t-9}.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,1} & =\frac{6({1}^{5})+4(1)}{14(1)-9} \\  & =\frac{10}{5} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,9)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-6)-3 & =-\frac{1}{2}(x-(-2)) \\ (y-6)-3 & =-\frac{1}{2}(x+2) \\ (y-6)-3 & =-\frac{1}{2}x-1 \\ (y-6) & =-\frac{1}{2}x-1+3 \\ (y-6) & =-\frac{1}{2}x+2.\end{aligned}
$$

The normal crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y & =- \frac{1}{2}(0-(-2))+9 \\ y & =8.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $y$-axis at $(0,\,8).$

---

## Generated method-bank variant — sixth_axis

A curve is defined by the parametric equations

$$
x=7{t}^{2}-9t-4,\,y={t}^{6}+2{t}^{2}+3,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Determine the coordinates of the point at which the normal to the curve at $C$ crosses the $y$-axis. Give exact answers.

The normal to the curve at $C$ crosses the $y$-axis at $(${{field-1}},
{{field-2}}$).$

field-1:
- $0$

field-2:
- $3$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =7({1}^{2})-9(1)-4=-2-4 \\ y & ={1}^{6}+2({1}^{2})+3=3+3\end{aligned}
$$

So, we're looking to determine the equation of the normal at the point $(-6,6).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=14t-9,\,{y}^{′}(t)=6{t}^{5}+4t
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{5}+4t}{14t-9}.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t\,=\,1} & =\frac{6({1}^{5})+4(1)}{14(1)-9} \\  & =\frac{10}{5} \\  & =2.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m:$

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{2}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-6,6)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-3)-3 & =-\frac{1}{2}((x+4)-(-2)) \\ (y-3)-3 & =-\frac{1}{2}((x+4)+2) \\ (y-3)-3 & =-\frac{1}{2}(x+4)-1 \\ (y-3) & =-\frac{1}{2}(x+4)-1+3 \\ (y-3) & =-\frac{1}{2}(x+4)+2.\end{aligned}
$$

The normal crosses the $y$-axis when $x=0.$ At this point, we have

$$
\begin{aligned}y & =- \frac{1}{2}(0-(-6))+6 \\ y & =3.\end{aligned}
$$

Consequently, the normal to the curve at $C$ crosses the $y$-axis at $(0,\,3).$

---

## Generated method-bank variant — cubic_linear

A curve is defined by the parametric equations

$$
x={t}^{3}-3t-2,\,y=2-t+2,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=3 x + 10$
- $y=\frac{x}{3} + \frac{14}{3}$
- $y=- 3 x - 2$
- $y=- 3 x - 10$
- $y=4 - 3 x$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={0}^{3}-3\cdot 0-2=0-0-2=0-2, \\ y & =2-0+2=2\,+2.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-2,4).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-3,\,{y}^{′}(t)=-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =(-1)\cdot \frac{1}{3{t}^{2}-3} \\  & =-\,\frac{1}{3{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=0,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =-\,\frac{1}{3\cdot {0}^{2}-3} \\  & =-\,\frac{1}{0-3} \\  & =\frac{1}{3}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{1}{3})\,}=-3
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,4)$ and the slope ${m}_{n}=-3.$ We get

$$
\begin{aligned}(y-2)-2 & =-3((x+2)-0) \\ (y-2) & =-3(x+2)+2\,.\end{aligned}
$$

---

## Generated method-bank variant — cubic_linear

A curve is defined by the parametric equations

$$
x={t}^{3}-3t-4,\,y=2-t+3,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=0$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=3 x + 17$
- $y=5 - 3 x$
- $y=- 3 x - 17$
- $y=- 3 x - 7$
- $y=\frac{x}{3} + \frac{19}{3}$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=0$ into the parametric equations:

$$
\begin{aligned}x & ={0}^{3}-3\cdot 0-4=0-0-4=0-4, \\ y & =2-0+3=2\,+3.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-4,5).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=3{t}^{2}-3,\,{y}^{′}(t)=-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =(-1)\cdot \frac{1}{3{t}^{2}-3} \\  & =-\,\frac{1}{3{t}^{2}-3}\,.\end{aligned}
$$

At the point where $t=0,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=0} & =-\,\frac{1}{3\cdot {0}^{2}-3} \\  & =-\,\frac{1}{0-3} \\  & =\frac{1}{3}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,(\frac{1}{3})\,}=-3
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-4,5)$ and the slope ${m}_{n}=-3.$ We get

$$
\begin{aligned}(y-3)-2 & =-3((x+4)-0) \\ (y-3) & =-3(x+4)+2\,.\end{aligned}
$$

---

## Generated method-bank variant — exponential

A curve is defined by the parametric equations

$$
x={e}^{t},\,y=2t{e}^{t}-2{e}^{t}+6,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{x}{2} - \frac{e}{2} + 6$
- $y=2 x - 2 e + 6$
- $y=- \frac{x}{2} + \frac{e}{2} + 6$
- $y=- \frac{x}{2} - 6 + \frac{e}{2}$
- $y=6 - \frac{x}{2}$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =e, \\ y & =2(1){e}^{1}-2{e}^{1}+6=0+6\end{aligned}
$$

So we're looking to find the equation of the normal to the curve at the point $(e,6).$  For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)={e}^{t},\,{y}^{′}(t)=2t{e}^{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t{e}^{t}}{{e}^{t}} \\  & =2t\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =2(1)=2\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,2\,}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(e,6)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-6)-0 & =(-\frac{1}{2})(x-e) \\ (y-6) & =-\frac{x}{2}+\frac{e}{2}\,.\end{aligned}
$$

---

## Generated method-bank variant — exponential

A curve is defined by the parametric equations

$$
x={e}^{t}-4,\,y=2t{e}^{t}-2{e}^{t}+3,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{x}{2} - \frac{e}{2} + 5$
- $y=3 - \frac{x}{2}$
- $y=- \frac{x}{2} - 5 + \frac{e}{2}$
- $y=- \frac{x}{2} + 1 + \frac{e}{2}$
- $y=2 x - 2 e + 11$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =e-4, \\ y & =2(1){e}^{1}-2{e}^{1}+3=0+3\end{aligned}
$$

So we're looking to find the equation of the normal to the curve at the point $(-4 + e,3).$  For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)={e}^{t},\,{y}^{′}(t)=2t{e}^{t}
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{2t{e}^{t}}{{e}^{t}} \\  & =2t\,.\end{aligned}
$$

At the point where $t=1,$ the slope of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =2(1)=2\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{\,2\,}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-4 + e,3)$ and the slope ${m}_{n}=-\frac{1}{2}.$ We get

$$
\begin{aligned}(y-3)-0 & =(-\frac{1}{2})((x+4)-e) \\ (y-3) & =-\frac{(x+4)}{2}+\frac{e}{2}\,.\end{aligned}
$$

---

## Generated method-bank variant — quartic_cubic

A curve is defined by the parametric equations

$$
x={t}^{4}-3{t}^{2},\,y=2{t}^{3}-t+6,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{31}{5} - \frac{2 x}{5}$
- $y=2 - \frac{5 x}{2}$
- $y=\frac{2 x}{5} + \frac{39}{5}$
- $y=\frac{2 x}{5} - \frac{31}{5}$
- $y=\frac{2 x}{5} + 7$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =(1)^{4}-3(1)^{2}=-2, \\ y & =2(1)^{3}-1+6=1\,+6.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-2,7).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=4{t}^{3}-6t,\,{y}^{′}(t)=6{t}^{2}-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-1}{4{t}^{3}-6t}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{2}-1}{4(1)^{3}-6(1)} \\  & =\frac{5}{-2} \\  & =-\,\frac{5}{2}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{(\,-\frac{5}{2}\,)}=\frac{2}{5}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-2,7)$ and the slope ${m}_{n}=\frac{2}{5}.$ We get

$$
\begin{aligned}(y-6)-1 & =\frac{2}{5}(x+2) \\ (y-6) & =\frac{2}{5}(x+2)+1\,.\end{aligned}
$$

---

## Generated method-bank variant — quartic_cubic

A curve is defined by the parametric equations

$$
x={t}^{4}-3{t}^{2}-4,\,y=2{t}^{3}-t+3,\,-\infty <t<\infty .
$$

Let $C$ be the point that corresponds to $t=1$ on the curve. Find the equation of the normal to the curve at $C.$

selection:
- $y=\frac{8}{5} - \frac{2 x}{5}$
- $y=\frac{2 x}{5} + 4$
- $y=\frac{2 x}{5} - \frac{8}{5}$
- $y=\frac{2 x}{5} + \frac{32}{5}$
- $y=- \frac{5 x}{2} - 11$

Worked solution:
First, we find the coordinates of the point $C$ by substituting $t=1$ into the parametric equations:

$$
\begin{aligned}x & =(1)^{4}-3(1)^{2}-4=-2-4, \\ y & =2(1)^{3}-1+3=1\,+3.\end{aligned}
$$

So we're looking to find the equation of the normal at the point $(-6,4).$ For this, we need to find $\frac{\text{d}y}{\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:

$$
{x}^{′}(t)=4{t}^{3}-6t,\,{y}^{′}(t)=6{t}^{2}-1.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{y}^{′}(t)}{{x}^{′}(t)} \\  & =\frac{6{t}^{2}-1}{4{t}^{3}-6t}.\end{aligned}
$$

At the point where $t=1,$  the slope $m$ of the tangent line is given by

$$
\begin{aligned}m={\frac{dy}{dx}|}_{t=1} & =\frac{6(1)^{2}-1}{4(1)^{3}-6(1)} \\  & =\frac{5}{-2} \\  & =-\,\frac{5}{2}\,.\end{aligned}
$$

To find the slope ${m}_{n}$ of the normal line, we take the negative reciprocal of $m$:

$$
{m}_{n}=-\frac{1}{m}=-\frac{1}{(\,-\frac{5}{2}\,)}=\frac{2}{5}
$$

To calculate the equation of the normal, we use point-slope form with the point $({x}_{1},{y}_{1})=(-6,4)$ and the slope ${m}_{n}=\frac{2}{5}.$ We get

$$
\begin{aligned}(y-3)-1 & =\frac{2}{5}((x+4)+2) \\ (y-3) & =\frac{2}{5}((x+4)+2)+1\,.\end{aligned}
$$