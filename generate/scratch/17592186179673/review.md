# Original and generated review

Database math; basis 1356; raw source exactness is separate from authored design.

Raw original q-124656 and its observed-profile variants are mathematically ambiguous: two complete integral choices equal zero. Native raw ID designation is fidelity evidence only. The repaired-profile variants below replace the wrong zero-valued choice by the omitted-dx integral of value 2pi.

## Original q-124597

Which of the following is equivalent to ${\int }_{C}{y}^{2}\,dx-{x}^{2}\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,1).$

- $-{\int }_{0}^{\pi /2}{sin}^{3}⁡t\,\text{d}t$
- ${\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t$
- ${\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t$
- $-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t$
- ${\int }_{0}^{\pi /2}\frac{1}{2}\operatorname{sin}⁡2t\,\text{d}t$

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}{y}^{2}\,dx-{x}^{2}\,dy & ={\int }_{0}^{\pi /2}{y}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t-{x}^{2}\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}({y}^{2}\,\frac{dx}{\text{d}t}-{x}^{2}\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi /2}(\operatorname{sin}⁡t)^{2}\cdot (-\operatorname{sin}⁡t)-(\operatorname{cos}⁡t)^{2}\cdot \operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi /2}-{sin}^{3}⁡t-{cos}^{3}⁡t\,\text{d}t \\  & =-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124597

Which of the following is equivalent to $-2\left({\int }_{C}{y}^{2}\,dx-{x}^{2}\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,1).$

- $-2\left(-{\int }_{0}^{\pi /2}{sin}^{3}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}{sin}^{2}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t\right)$
- $-2\left(-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}\frac{1}{2}\operatorname{sin}⁡2t\,\text{d}t\right)$

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}{y}^{2}\,dx-{x}^{2}\,dy\right) & =-2\left({\int }_{0}^{\pi /2}{y}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t-{x}^{2}\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}({y}^{2}\,\frac{dx}{\text{d}t}-{x}^{2}\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(\operatorname{sin}⁡t)^{2}\cdot (-\operatorname{sin}⁡t)-(\operatorname{cos}⁡t)^{2}\cdot \operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}-{sin}^{3}⁡t-{cos}^{3}⁡t\,\text{d}t \right)\\  & =-2\left(-{\int }_{0}^{\pi /2}{sin}^{3}⁡t+{cos}^{3}⁡t\,\text{d}t\right)\end{aligned}
$$

## Original q-81192

Evaluate ${\int }_{C}\frac{y\,dy-x\,dx}{{x}^{2}+{y}^{2}},$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $(1,0)$ to the point $(0,1).$

- $2$
- $\frac{1}{4}$
- $\frac{2}{3}$
- $\frac{1}{2}1$
- $1$

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}\frac{y\,dy-x\,dx}{{x}^{2}+{y}^{2}} & ={\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}\,\text{d}t-x\cdot {x}^{′}\,\text{d}t}{{x}^{2}+{y}^{2}} \\  & ={\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}-x\cdot {x}^{′}}{{x}^{2}+{y}^{2}}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\frac{\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t-\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t)}{{cos}^{2}⁡t+{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\operatorname{sin}⁡2t\,\text{d}t \\  & ={[-\frac{1}{2}\operatorname{cos}⁡2t]}_{0}^{\pi /2} \\  & =-\frac{1}{2}[\operatorname{cos}⁡(\pi )-\operatorname{cos}⁡(0)] \\  & =-\frac{1}{2}[-1-1] \\  & =1\end{aligned}
$$

## Generated replay-profile variant q-81192

Evaluate $-2\left({\int }_{C}\frac{y\,dy-x\,dx}{{x}^{2}+{y}^{2}}\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=1$ traversed in the counterclockwise direction from the point $(1,0)$ to the point $(0,1).$

- $-2\left(2\right)$
- $-2\left(\frac{1}{4}\right)$
- $-2\left(\frac{2}{3}\right)$
- $-2\left(\frac{1}{2}1\right)$
- $-2\left(1\right)$

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-2\left({\int }_{C}\frac{y\,dy-x\,dx}{{x}^{2}+{y}^{2}}\right) & =-2\left({\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}\,\text{d}t-x\cdot {x}^{′}\,\text{d}t}{{x}^{2}+{y}^{2}} \right)\\  & =-2\left({\int }_{0}^{\pi /2}\frac{y\cdot {y}^{′}-x\cdot {x}^{′}}{{x}^{2}+{y}^{2}}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}\frac{\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t-\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t)}{{cos}^{2}⁡t+{sin}^{2}⁡t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}\operatorname{sin}⁡2t\,\text{d}t \right)\\  & =-2\left({[-\frac{1}{2}\operatorname{cos}⁡2t]}_{0}^{\pi /2} \right)\\  & =-2\left(-\frac{1}{2}[\operatorname{cos}⁡(\pi )-\operatorname{cos}⁡(0)] \right)\\  & =-2\left(-\frac{1}{2}[-1-1] \right)\\  & =-2\left(1\right)\end{aligned}
$$

## Original q-124656

Which of the following is equivalent to ${\int }_{C}{x}^{2}y\,dx+x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(-2,0).$

- $8{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{cos}^{2}⁡t)\,\text{d}t$
- $8{\int }_{0}^{\pi }{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t$
- $2{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{sin}^{2}⁡t)\,\text{d}t$
- $4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t$
- $4{\int }_{0}^{\pi }{sin}^{2}⁡t(1-4{cos}^{2}⁡t)\,\text{d}t$

Since $C$ is a circle of radius $2$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}{x}^{2}y\,dx+x\,dy & ={\int }_{0}^{\pi }{x}^{2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi }({x}^{2}y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi }(2\operatorname{cos}⁡t)^{2}\cdot (2\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot 2\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi }-16{sin}^{2}⁡t{cos}^{2}⁡t+4{cos}^{2}⁡t\,\text{d}t \\  & =4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124656

Which of the following is equivalent to $-2\left({\int }_{C}{x}^{2}y\,dx+x\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(-2,0).$

- $-2\left(8{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{cos}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(8{\int }_{0}^{\pi }{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t\right)$
- $-2\left(2{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{sin}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(4{\int }_{0}^{\pi }{sin}^{2}⁡t(1-4{cos}^{2}⁡t)\,\text{d}t\right)$

Since $C$ is a circle of radius $2$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}{x}^{2}y\,dx+x\,dy\right) & =-2\left({\int }_{0}^{\pi }{x}^{2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }({x}^{2}y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }(2\operatorname{cos}⁡t)^{2}\cdot (2\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot 2\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }-16{sin}^{2}⁡t{cos}^{2}⁡t+4{cos}^{2}⁡t\,\text{d}t \right)\\  & =-2\left(4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\right)\end{aligned}
$$

## Original q-124657

Which of the following is equivalent to ${\int }_{C}\frac{2}{y}\,dx+y{e}^{x}\,dy,$ where $C$ is part of the ellipse $4{x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,2).$

- ${\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}+1\,\text{d}t$
- ${\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t$
- ${\int }_{0}^{\pi /2}\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-\operatorname{sin}⁡t\,\text{d}t$
- ${\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-2\,\text{d}t$
- ${\int }_{0}^{3\pi /2}\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t}+2\operatorname{cos}⁡t\,\text{d}t$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $2,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}\frac{2}{y}\,dx+y{e}^{x}\,dy & ={\int }_{0}^{\pi /2}\frac{2}{y}\,\frac{dx}{\text{d}t}\,\text{d}t+y{e}^{x}\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}(\frac{2}{y}\,\frac{dx}{\text{d}t}+y{e}^{x}\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi /2}\frac{2}{2\operatorname{sin}⁡t}\cdot (-\operatorname{sin}⁡t)+(2\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t})\cdot 2\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124657

Which of the following is equivalent to $-2\left({\int }_{C}\frac{2}{y}\,dx+y{e}^{x}\,dy\right),$ where $C$ is part of the ellipse $4{x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(1,0)$ to the point $B(0,2).$

- $-2\left({\int }_{0}^{\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}+1\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-\operatorname{sin}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-2\,\text{d}t\right)$
- $-2\left({\int }_{0}^{3\pi /2}\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t}+2\operatorname{cos}⁡t\,\text{d}t\right)$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $2,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}\frac{2}{y}\,dx+y{e}^{x}\,dy\right) & =-2\left({\int }_{0}^{\pi /2}\frac{2}{y}\,\frac{dx}{\text{d}t}\,\text{d}t+y{e}^{x}\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(\frac{2}{y}\,\frac{dx}{\text{d}t}+y{e}^{x}\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}\frac{2}{2\operatorname{sin}⁡t}\cdot (-\operatorname{sin}⁡t)+(2\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t})\cdot 2\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}4\operatorname{sin}⁡t\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t}-1\,\text{d}t\right)\end{aligned}
$$

## Original q-124661

Evaluate ${\int }_{C}(x-y)\,dx+(x+y)\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+4{y}^{2}=36$ traversed in the counterclockwise direction from the point $(0,3)$ to the point $(-2,0).$

- $\frac{5\pi +1}{4}$
- $\frac{6\pi -5}{2}$
- $6\pi $
- $3\pi $
- $\frac{12\pi -5}{4}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & ={x}^{′}(t)\,i+{y}^{′}(t)\,j=-2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}(x-y)\,dx+(x+y)\,dy & ={\int }_{\pi /2}^{\pi }(x-y)\,\frac{dx}{\text{d}t}\,\text{d}t+(x+y)\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }((x-y)\,\frac{dx}{\text{d}t}+(x+y)\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }(2\operatorname{cos}⁡t-3\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t+3\operatorname{sin}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }(-4\operatorname{cos}⁡t\operatorname{sin}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t+9\operatorname{cos}⁡t\operatorname{sin}⁡t)\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }5\operatorname{sin}⁡t\operatorname{cos}⁡t+6\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }\frac{5}{2}\operatorname{sin}⁡2t+6\,\text{d}t \\  & ={[-\frac{5}{4}\operatorname{cos}⁡2t+6t]}_{\pi /2}^{\pi } \\  & =[(-\frac{5}{4}\operatorname{cos}⁡(2\pi )+6\pi )-(-\frac{5}{4}\operatorname{cos}⁡(\pi )+3\pi )] \\  & =(-\frac{5}{4}+6\pi )-(\frac{5}{4}+3\pi ) \\  & =3\pi -\frac{5}{2} \\  & =\frac{6\pi -5}{2}\end{aligned}
$$

## Generated replay-profile variant q-124661

Evaluate $-2\left({\int }_{C}(x-y)\,dx+(x+y)\,dy\right),$ where $C$ is part of the ellipse $9{x}^{2}+4{y}^{2}=36$ traversed in the counterclockwise direction from the point $(0,3)$ to the point $(-2,0).$

- $-2\left(\frac{5\pi +1}{4}\right)$
- $-2\left(\frac{6\pi -5}{2}\right)$
- $-2\left(6\pi \right)$
- $-2\left(3\pi \right)$
- $-2\left(\frac{12\pi -5}{4}\right)$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & ={x}^{′}(t)\,i+{y}^{′}(t)\,j=-2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-2\left({\int }_{C}(x-y)\,dx+(x+y)\,dy\right) & =-2\left({\int }_{\pi /2}^{\pi }(x-y)\,\frac{dx}{\text{d}t}\,\text{d}t+(x+y)\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }((x-y)\,\frac{dx}{\text{d}t}+(x+y)\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }(2\operatorname{cos}⁡t-3\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t+3\operatorname{sin}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }(-4\operatorname{cos}⁡t\operatorname{sin}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t+9\operatorname{cos}⁡t\operatorname{sin}⁡t)\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }5\operatorname{sin}⁡t\operatorname{cos}⁡t+6\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }\frac{5}{2}\operatorname{sin}⁡2t+6\,\text{d}t \right)\\  & =-2\left({[-\frac{5}{4}\operatorname{cos}⁡2t+6t]}_{\pi /2}^{\pi } \right)\\  & =-2\left([(-\frac{5}{4}\operatorname{cos}⁡(2\pi )+6\pi )-(-\frac{5}{4}\operatorname{cos}⁡(\pi )+3\pi )] \right)\\  & =-2\left((-\frac{5}{4}+6\pi )-(\frac{5}{4}+3\pi ) \right)\\  & =-2\left(3\pi -\frac{5}{2} \right)\\  & =-2\left(\frac{6\pi -5}{2}\right)\end{aligned}
$$

## Original q-124665

Evaluate ${\int }_{C}dx+\frac{2}{x}\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $(-1,0)$ to the point $(0,-3).$

- $4\pi $
- $3\pi -4$
- $2\pi -1$
- $\frac{3\pi +1}{2}$
- $3\pi +1$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\pi ,\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}dx+\frac{2}{x}\,dy & ={\int }_{\pi }^{3\pi /2}\frac{dx}{\text{d}t}\,\text{d}t+\frac{2}{x}\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}(\frac{dx}{\text{d}t}+\frac{2}{x}\,\frac{dy}{\text{d}t})\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}(-\operatorname{sin}⁡t)+\frac{2}{\operatorname{cos}⁡t}\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}-\operatorname{sin}⁡t+6\,\text{d}t \\  & =[\operatorname{cos}⁡t+6t]_{\pi }^{3\pi /2} \\  & =(\operatorname{cos}⁡(\frac{3\pi }{2})+9\pi )-(\operatorname{cos}⁡\pi +6\pi ) \\  & =(0+9\pi )-(-1+6\pi ) \\  & =3\pi +1\end{aligned}
$$

## Generated replay-profile variant q-124665

Evaluate $-2\left({\int }_{C}dx+\frac{2}{x}\,dy\right),$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $(-1,0)$ to the point $(0,-3).$

- $-2\left(4\pi \right)$
- $-2\left(3\pi -4\right)$
- $-2\left(2\pi -1\right)$
- $-2\left(\frac{3\pi +1}{2}\right)$
- $-2\left(3\pi +1\right)$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\pi ,\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-2\left({\int }_{C}dx+\frac{2}{x}\,dy\right) & =-2\left({\int }_{\pi }^{3\pi /2}\frac{dx}{\text{d}t}\,\text{d}t+\frac{2}{x}\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}(\frac{dx}{\text{d}t}+\frac{2}{x}\,\frac{dy}{\text{d}t})\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}(-\operatorname{sin}⁡t)+\frac{2}{\operatorname{cos}⁡t}\cdot 3\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}-\operatorname{sin}⁡t+6\,\text{d}t \right)\\  & =-2\left([\operatorname{cos}⁡t+6t]_{\pi }^{3\pi /2} \right)\\  & =-2\left((\operatorname{cos}⁡(\frac{3\pi }{2})+9\pi )-(\operatorname{cos}⁡\pi +6\pi ) \right)\\  & =-2\left((0+9\pi )-(-1+6\pi ) \right)\\  & =-2\left(3\pi +1\right)\end{aligned}
$$

## Original q-124651

Which of the following is equivalent to ${\int }_{C}{x}^{2}\,dx+xy\,dy,$ where $C$ is part of the ellipse ${x}^{2}+4{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(0,1).$

- $-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t$
- $-2{\int }_{0}^{\pi /2}{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t$
- $6{\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,\text{d}t$
- $3{\int }_{0}^{\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t$
- ${\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\,\text{d}t$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $1,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}{x}^{2}\,dx+xy\,dy & ={\int }_{0}^{\pi /2}{x}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t+xy\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}({x}^{2}\,\frac{dx}{\text{d}t}+xy\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi /2}(2\operatorname{cos}⁡t)^{2}\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot \operatorname{sin}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi /2}-8{cos}^{2}⁡t\operatorname{sin}⁡t+2{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t \\  & =-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124651

Which of the following is equivalent to $-2\left({\int }_{C}{x}^{2}\,dx+xy\,dy\right),$ where $C$ is part of the ellipse ${x}^{2}+4{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(0,1).$

- $-2\left(-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t\right)$
- $-2\left(-2{\int }_{0}^{\pi /2}{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t\right)$
- $-2\left(6{\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,\text{d}t\right)$
- $-2\left(3{\int }_{0}^{\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡t\operatorname{sin}⁡t(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\,\text{d}t\right)$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $1,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j,\,t\in [0,\frac{\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}{x}^{2}\,dx+xy\,dy\right) & =-2\left({\int }_{0}^{\pi /2}{x}^{2}\,\frac{dx}{\text{d}t}\,\text{d}t+xy\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}({x}^{2}\,\frac{dx}{\text{d}t}+xy\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(2\operatorname{cos}⁡t)^{2}\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot \operatorname{sin}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}-8{cos}^{2}⁡t\operatorname{sin}⁡t+2{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t \right)\\  & =-2\left(-6{\int }_{0}^{\pi /2}{cos}^{2}⁡t\operatorname{sin}⁡t\,\text{d}t\right)\end{aligned}
$$

## Original q-124653

Which of the following is equivalent to ${\int }_{C}({e}^{x}+y)\,dx-x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=3$ traversed in the counterclockwise direction from the point $A(0,\sqrt{3})$ to the point $B(-\sqrt{3},0).$

- $-3{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}\,\text{d}t$
- $-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{cos}⁡t\,\text{d}t$
- $-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+3\,\text{d}t$
- $-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t$
- ${\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+1\,\text{d}t$

Since $C$ is a circle of radius $\sqrt{3}$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{3}\operatorname{cos}⁡t\,i+\sqrt{3}\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{3}\operatorname{sin}⁡t\,i+\sqrt{3}\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}({e}^{x}+y)\,dx-x\,dy & ={\int }_{\pi /2}^{\pi }({e}^{x}+y)\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }(({e}^{x}+y)\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }({e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{sin}⁡t)\cdot (-\sqrt{3}\operatorname{sin}⁡t)-(\sqrt{3}\operatorname{cos}⁡t)\cdot (\sqrt{3}\operatorname{cos}⁡t)\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3{sin}^{2}⁡t-3{cos}^{2}⁡t\,\text{d}t \\  & ={\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3\,\text{d}t \\  & =-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124653

Which of the following is equivalent to $-2\left({\int }_{C}({e}^{x}+y)\,dx-x\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=3$ traversed in the counterclockwise direction from the point $A(0,\sqrt{3})$ to the point $B(-\sqrt{3},0).$

- $-2\left(-3{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}\,\text{d}t\right)$
- $-2\left(-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{cos}⁡t\,\text{d}t\right)$
- $-2\left(-{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+3\,\text{d}t\right)$
- $-2\left(-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t\right)$
- $-2\left({\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{3\operatorname{cos}⁡t}+1\,\text{d}t\right)$

Since $C$ is a circle of radius $\sqrt{3}$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{3}\operatorname{cos}⁡t\,i+\sqrt{3}\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{3}\operatorname{sin}⁡t\,i+\sqrt{3}\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}({e}^{x}+y)\,dx-x\,dy\right) & =-2\left({\int }_{\pi /2}^{\pi }({e}^{x}+y)\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }(({e}^{x}+y)\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }({e}^{\sqrt{3}\operatorname{cos}⁡t}+\sqrt{3}\operatorname{sin}⁡t)\cdot (-\sqrt{3}\operatorname{sin}⁡t)-(\sqrt{3}\operatorname{cos}⁡t)\cdot (\sqrt{3}\operatorname{cos}⁡t)\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3{sin}^{2}⁡t-3{cos}^{2}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{\pi }-\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}-3\,\text{d}t \right)\\  & =-2\left(-{\int }_{\pi /2}^{\pi }\sqrt{3}\operatorname{sin}⁡t\,{e}^{\sqrt{3}\operatorname{cos}⁡t}+3\,\text{d}t\right)\end{aligned}
$$

## Original q-124655

Which of the following is equivalent to ${\int }_{C}(x-2y)\,dx+2x\,dy,$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $A(0,3)$ to the point $B(0,-3).$

- ${\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t$
- $2{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t$
- ${\int }_{\pi /2}^{3\pi /2}6{sin}^{2}⁡t-\operatorname{cos}⁡t\,\text{d}t$
- ${\int }_{\pi /2}^{3\pi /2}3-{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t$
- ${\int }_{\pi /2}^{3\pi /2}3\operatorname{sin}⁡t+\operatorname{cos}⁡t\,\text{d}t$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}(x-2y)\,dx+2x\,dy & ={\int }_{\pi /2}^{3\pi /2}(x-2y)\,\frac{dx}{\text{d}t}\,\text{d}t+2x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{\pi /2}^{3\pi /2}((x-2y)\,\frac{dx}{\text{d}t}+2x\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡t-2(3\operatorname{sin}⁡t))\cdot (-\operatorname{sin}⁡t)+2(\operatorname{cos}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{\pi /2}^{3\pi /2}-\operatorname{sin}⁡t\operatorname{cos}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t\,\text{d}t \\  & ={\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t\end{aligned}
$$

## Generated replay-profile variant q-124655

Which of the following is equivalent to $-2\left({\int }_{C}(x-2y)\,dx+2x\,dy\right),$ where $C$ is part of the ellipse $9{x}^{2}+{y}^{2}=9$ traversed in the counterclockwise direction from the point $A(0,3)$ to the point $B(0,-3).$

- $-2\left({\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t\right)$
- $-2\left(2{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{\pi /2}^{3\pi /2}6{sin}^{2}⁡t-\operatorname{cos}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{\pi /2}^{3\pi /2}3-{sin}^{2}⁡t\operatorname{cos}⁡t\,\text{d}t\right)$
- $-2\left({\int }_{\pi /2}^{3\pi /2}3\operatorname{sin}⁡t+\operatorname{cos}⁡t\,\text{d}t\right)$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $3,$ respectively, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j,\,t\in [\frac{\pi }{2},\frac{3\pi }{2}]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}(x-2y)\,dx+2x\,dy\right) & =-2\left({\int }_{\pi /2}^{3\pi /2}(x-2y)\,\frac{dx}{\text{d}t}\,\text{d}t+2x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{3\pi /2}((x-2y)\,\frac{dx}{\text{d}t}+2x\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡t-2(3\operatorname{sin}⁡t))\cdot (-\operatorname{sin}⁡t)+2(\operatorname{cos}⁡t)\cdot 3\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{3\pi /2}-\operatorname{sin}⁡t\operatorname{cos}⁡t+6{sin}^{2}⁡t+6{cos}^{2}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{\pi /2}^{3\pi /2}6-\operatorname{sin}⁡t\operatorname{cos}⁡t\,\text{d}t\right)\end{aligned}
$$

## Original q-81186

Evaluate ${\int }_{C}y\,dx+x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(-2,0)$ to the point $B(0,-2).$

- $-1$
- $4$
- $0$
- $-2$
- $2$

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $2$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡(t)\,i+2\operatorname{sin}⁡(t)\,j,\,t\in [\pi ,\frac{3\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=2\operatorname{cos}⁡t$ and $y(t)=2\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡(t)\,i+2\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
\begin{aligned}{\int }_{C}y\,dx+x\,dy & ={\int }_{\pi }^{3\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}(y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}(2\operatorname{sin}⁡t\cdot (-2\operatorname{sin}⁡t)+2\operatorname{cos}⁡t\cdot 2\operatorname{cos}⁡t)\text{d}t \\  & ={\int }_{\pi }^{3\pi /2}(-4{sin}^{2}⁡t+4{cos}^{2}⁡t)\text{d}t \\  & =4{\int }_{\pi }^{3\pi /2}({cos}^{2}⁡t-{sin}^{2}⁡t)\text{d}t \\  & =4{\int }_{\pi }^{3\pi /2}\operatorname{cos}⁡(2t)\,\text{d}t \\  & =2\operatorname{sin}⁡2t{|}_{\pi }^{3\pi /2} \\  & =2[\operatorname{sin}⁡(3\pi )-\operatorname{sin}⁡(2\pi )] \\  & =2(0-0) \\  & =0\end{aligned}
$$

## Generated replay-profile variant q-81186

Evaluate $-2\left({\int }_{C}y\,dx+x\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(-2,0)$ to the point $B(0,-2).$

- $-2\left(-1\right)$
- $-2\left(4\right)$
- $-2\left(0\right)$
- $-2\left(-2\right)$
- $-2\left(2\right)$

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $2$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡(t)\,i+2\operatorname{sin}⁡(t)\,j,\,t\in [\pi ,\frac{3\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=2\operatorname{cos}⁡t$ and $y(t)=2\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡(t)\,i+2\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}y\,dx+x\,dy\right) & =-2\left({\int }_{\pi }^{3\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}(y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}(2\operatorname{sin}⁡t\cdot (-2\operatorname{sin}⁡t)+2\operatorname{cos}⁡t\cdot 2\operatorname{cos}⁡t)\text{d}t \right)\\  & =-2\left({\int }_{\pi }^{3\pi /2}(-4{sin}^{2}⁡t+4{cos}^{2}⁡t)\text{d}t \right)\\  & =-2\left(4{\int }_{\pi }^{3\pi /2}({cos}^{2}⁡t-{sin}^{2}⁡t)\text{d}t \right)\\  & =-2\left(4{\int }_{\pi }^{3\pi /2}\operatorname{cos}⁡(2t)\,\text{d}t \right)\\  & =-2\left(2\operatorname{sin}⁡2t{|}_{\pi }^{3\pi /2} \right)\\  & =-2\left(2[\operatorname{sin}⁡(3\pi )-\operatorname{sin}⁡(2\pi )] \right)\\  & =-2\left(2(0-0) \right)\\  & =-2\left(0\right)\end{aligned}
$$

## Original q-90895

Evaluate ${\int }_{C}y\,dx-x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=2$ traversed in the counterclockwise direction from the point $A(\sqrt{2},0)$ to the point $B(0,\sqrt{2}).$

- $-\frac{\pi }{3}$
- $\frac{\pi }{3}$
- $0$
- $\pi $
- $-\pi $

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $\sqrt{2}$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{2}\operatorname{cos}⁡(t)\,i+\sqrt{2}\operatorname{sin}⁡(t)\,j,\,t\in [0,\frac{\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=\sqrt{2}\operatorname{cos}⁡t$ and $y(t)=\sqrt{2}\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{2}\operatorname{sin}⁡(t)\,i+\sqrt{2}\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
\begin{aligned}{\int }_{C}y\,dx-x\,dy & ={\int }_{0}^{\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi /2}(y\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi /2}(\sqrt{2}\operatorname{sin}⁡t\cdot (-\sqrt{2}\operatorname{sin}⁡t)-\sqrt{2}\operatorname{cos}⁡t\cdot \sqrt{2}\operatorname{cos}⁡t)\text{d}t \\  & ={\int }_{0}^{\pi /2}(-2{sin}^{2}⁡t-2{cos}^{2}⁡t)\text{d}t \\  & =-2{\int }_{0}^{\pi /2}\text{d}t \\  & =-2t{|}_{0}^{\pi /2} \\  & =-2[\frac{\pi }{2}-0] \\  & =-\pi \end{aligned}
$$

## Generated replay-profile variant q-90895

Evaluate $-2\left({\int }_{C}y\,dx-x\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=2$ traversed in the counterclockwise direction from the point $A(\sqrt{2},0)$ to the point $B(0,\sqrt{2}).$

- $-2\left(-\frac{\pi }{3}\right)$
- $-2\left(\frac{\pi }{3}\right)$
- $-2\left(0\right)$
- $-2\left(\pi \right)$
- $-2\left(-\pi \right)$

First, we need to find the parametrization of the curve $C.$ Since it's a circle if radius $\sqrt{2}$ centered at the origin, the curve $C$ can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=\sqrt{2}\operatorname{cos}⁡(t)\,i+\sqrt{2}\operatorname{sin}⁡(t)\,j,\,t\in [0,\frac{\pi }{2}].\end{aligned}
$$

So, along the curve we have that $x(t)=\sqrt{2}\operatorname{cos}⁡t$ and $y(t)=\sqrt{2}\operatorname{sin}⁡t.$ 

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-\sqrt{2}\operatorname{sin}⁡(t)\,i+\sqrt{2}\operatorname{cos}⁡(t)\,j.\end{aligned}
$$

Therefore, we can calculate the line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}y\,dx-x\,dy\right) & =-2\left({\int }_{0}^{\pi /2}y\,\frac{dx}{\text{d}t}\,\text{d}t-x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(y\,\frac{dx}{\text{d}t}-x\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(\sqrt{2}\operatorname{sin}⁡t\cdot (-\sqrt{2}\operatorname{sin}⁡t)-\sqrt{2}\operatorname{cos}⁡t\cdot \sqrt{2}\operatorname{cos}⁡t)\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi /2}(-2{sin}^{2}⁡t-2{cos}^{2}⁡t)\text{d}t \right)\\  & =-2\left(-2{\int }_{0}^{\pi /2}\text{d}t \right)\\  & =-2\left(-2t{|}_{0}^{\pi /2} \right)\\  & =-2\left(-2[\frac{\pi }{2}-0] \right)\\  & =-2\left(-\pi \right)\end{aligned}
$$

## Repaired source-bank variant q-124656 c=1

Which of the following is equivalent to ${\int }_{C}{x}^{2}y\,dx+x\,dy,$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(-2,0).$

- $8{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{cos}^{2}⁡t)\,\text{d}t$
- $8{\int }_{0}^{\pi }{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t$
- $2{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{sin}^{2}⁡t)\,\text{d}t$
- $4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t$
- $4{\int }_{0}^{\pi }{cos}^{2}⁡t\,\text{d}t$

Since $C$ is a circle of radius $2$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}{\int }_{C}{x}^{2}y\,dx+x\,dy & ={\int }_{0}^{\pi }{x}^{2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \\  & ={\int }_{0}^{\pi }({x}^{2}y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\,\text{d}t \\  & ={\int }_{0}^{\pi }(2\operatorname{cos}⁡t)^{2}\cdot (2\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot 2\operatorname{cos}⁡t\,\text{d}t \\  & ={\int }_{0}^{\pi }-16{sin}^{2}⁡t{cos}^{2}⁡t+4{cos}^{2}⁡t\,\text{d}t \\  & =4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\end{aligned}
$$

## Repaired source-bank variant q-124656 c=-2

Which of the following is equivalent to $-2\left({\int }_{C}{x}^{2}y\,dx+x\,dy\right),$ where $C$ is part of the circle ${x}^{2}+{y}^{2}=4$ traversed in the counterclockwise direction from the point $A(2,0)$ to the point $B(-2,0).$

- $-2\left(8{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{cos}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(8{\int }_{0}^{\pi }{cos}^{2}⁡t{sin}^{2}⁡t\,\text{d}t\right)$
- $-2\left(2{\int }_{0}^{\pi }{cos}^{2}⁡t(1-2{sin}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\right)$
- $-2\left(4{\int }_{0}^{\pi }{cos}^{2}⁡t\,\text{d}t\right)$

Since $C$ is a circle of radius $2$ centered at the origin, it can be parametrized as follows:

$$
\begin{aligned}r(t) & =x(t)\,i+y(t)\,j=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,\,t\in [0,\pi ]\end{aligned}
$$

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}-2\left({\int }_{C}{x}^{2}y\,dx+x\,dy\right) & =-2\left({\int }_{0}^{\pi }{x}^{2}y\,\frac{dx}{\text{d}t}\,\text{d}t+x\,\frac{dy}{\text{d}t}\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }({x}^{2}y\,\frac{dx}{\text{d}t}+x\,\frac{dy}{\text{d}t})\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }(2\operatorname{cos}⁡t)^{2}\cdot (2\operatorname{sin}⁡t)\cdot (-2\operatorname{sin}⁡t)+(2\operatorname{cos}⁡t)\cdot 2\operatorname{cos}⁡t\,\text{d}t \right)\\  & =-2\left({\int }_{0}^{\pi }-16{sin}^{2}⁡t{cos}^{2}⁡t+4{cos}^{2}⁡t\,\text{d}t \right)\\  & =-2\left(4{\int }_{0}^{\pi }{cos}^{2}⁡t(1-4{sin}^{2}⁡t)\,\text{d}t\right)\end{aligned}
$$

## Authored easy seed 0

Which of the following is equivalent to $\int_C\left(3 x^{2}\right)\,\mathrm{d}x+\left(- x y\right)\,\mathrm{d}y,$ where $C$ is part of the circle $x^{2} + y^{2}=1$ traversed in the counterclockwise direction from the point $(1,0)$ to the point $(-1,0)$.

- $\int_{0}^{\pi}\left(- 3 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(- \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(- 4 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(- \sin^{2}{\left(t \right)} \cos{\left(t \right)} + 3 \cos^{3}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(2 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$

Since $C$ is a circle of radius $1$ centered at the origin, it can be parametrized as follows:

$$r(t)=\cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\pi].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}\int_C\left(3 x^{2}\right)\,\mathrm{d}x+\left(- x y\right)\,\mathrm{d}y & =\int_{0}^{\pi}\left(3 x^{2}\right)x\prime(t)\,\mathrm{d}t+\left(- x y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(3 x^{2}\right)x\prime(t)+\left(- x y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(3 \cos^{2}{\left(t \right)}\right)\left(- \sin{\left(t \right)}\right)+\left(- \sin{\left(t \right)} \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(- 3 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(- 4 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t\end{aligned}
$$

## Authored easy seed 1

Which of the following is equivalent to $\int_C\left(- x^{2}\right)\,\mathrm{d}x+\left(3 x y\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $16 x^{2} + y^{2}=16$ traversed in the counterclockwise direction from the point $(1,0)$ to the point $(-1,0)$.

- $\int_{0}^{\pi}\left(\sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(47 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(48 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - \cos^{3}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(49 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\left(48 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $4,$ respectively, it can be parametrized as follows:

$$r(t)=\cos{\left(t \right)}\,i+4 \sin{\left(t \right)}\,j,\quad t\in[0,\pi].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- \sin{\left(t \right)}\,i+4 \cos{\left(t \right)}\,j.$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}\int_C\left(- x^{2}\right)\,\mathrm{d}x+\left(3 x y\right)\,\mathrm{d}y & =\int_{0}^{\pi}\left(- x^{2}\right)x\prime(t)\,\mathrm{d}t+\left(3 x y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(- x^{2}\right)x\prime(t)+\left(3 x y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(- \cos^{2}{\left(t \right)}\right)\left(- \sin{\left(t \right)}\right)+\left(12 \sin{\left(t \right)} \cos{\left(t \right)}\right)\left(4 \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(\sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(48 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(49 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t\end{aligned}
$$

## Authored moderate seed 0

Evaluate $\int_C\left(2 x + 4 y\right)\,\mathrm{d}x+\left(- 4 x - 3 y\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(0,-1)$ to the point $(3,0)$.

- $9 - 3 \pi$
- $\frac{3}{2} - 3 \pi$
- $\frac{21}{2} - 6 \pi$
- $\frac{15 \pi}{4}$
- $- \frac{15}{2}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[\frac{3 \pi}{2},2 \pi].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(2 x + 4 y\right)\,\mathrm{d}x+\left(- 4 x - 3 y\right)\,\mathrm{d}y & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(2 x + 4 y\right)x\prime(t)\,\mathrm{d}t+\left(- 4 x - 3 y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(\left(2 x + 4 y\right)x\prime(t)+\left(- 4 x - 3 y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(\left(4 \sin{\left(t \right)} + 6 \cos{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(- 3 \sin{\left(t \right)} - 12 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(\left(- 18 \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(- 12 \sin^{2}{\left(t \right)}\right)+\left(- 12 \cos^{2}{\left(t \right)}\right)+\left(- 3 \sin{\left(t \right)} \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(- 21 \sin{\left(t \right)} \cos{\left(t \right)} - 12\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{2 \pi}\left(- \frac{21 \sin{\left(2 t \right)}}{2} - 12\right)\,\mathrm{d}t\\ & =\left[- 12 t - \frac{21 \sin^{2}{\left(t \right)}}{2}\right]_{\frac{3 \pi}{2}}^{2 \pi}\\ & =\left(- 12 \left(2 \pi\right) - \frac{21 \sin^{2}{\left(\left(2 \pi\right) \right)}}{2}\right)-\left(- 12 \left(\frac{3 \pi}{2}\right) - \frac{21 \sin^{2}{\left(\left(\frac{3 \pi}{2}\right) \right)}}{2}\right)\\ & =\left(\left(- 24 \pi\right)+\left(0\right)\right)-\left(\left(- 18 \pi\right)+\left(- \frac{21}{2}\right)\right)\\ & =\frac{21}{2} - 6 \pi\end{aligned}
$$

## Authored moderate seed 1

Evaluate $\int_C\left(x - 2 y\right)\,\mathrm{d}x+\left(2 x + 3 y\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,1)$.

- $- \frac{9}{2} + \frac{3 \pi}{2}$
- $6$
- $3 \pi$
- $-3 + 3 \pi$
- $\frac{3}{2} + \frac{3 \pi}{2}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(x - 2 y\right)\,\mathrm{d}x+\left(2 x + 3 y\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(x - 2 y\right)x\prime(t)\,\mathrm{d}t+\left(2 x + 3 y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(x - 2 y\right)x\prime(t)+\left(2 x + 3 y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 2 \sin{\left(t \right)} + 3 \cos{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} + 6 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 9 \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(6 \sin^{2}{\left(t \right)}\right)+\left(6 \cos^{2}{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(- 6 \sin{\left(t \right)} \cos{\left(t \right)} + 6\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(6 - 3 \sin{\left(2 t \right)}\right)\,\mathrm{d}t\\ & =\left[6 t - 3 \sin^{2}{\left(t \right)}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(6 \left(\frac{\pi}{2}\right) - 3 \sin^{2}{\left(\left(\frac{\pi}{2}\right) \right)}\right)-\left(6 \left(0\right) - 3 \sin^{2}{\left(\left(0\right) \right)}\right)\\ & =\left(\left(-3\right)+\left(3 \pi\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =-3 + 3 \pi\end{aligned}
$$

## Authored hard seed 0

Evaluate $\int_C\left(- x^{2} y - 2 y\right)\,\mathrm{d}x+\left(- 2 x y^{2} + 2 x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $16 x^{2} + 9 y^{2}=144$ traversed in the counterclockwise direction from the point $(0,4)$ to the point $(0,-4)$.

- $\frac{51 \pi}{2}$
- $- 36 \pi$
- $- \frac{21 \pi}{2}$
- $0$
- $- \frac{123 \pi}{2}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $4,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+4 \sin{\left(t \right)}\,j,\quad t\in[\frac{\pi}{2},\frac{3 \pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+4 \cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- x^{2} y - 2 y\right)\,\mathrm{d}x+\left(- 2 x y^{2} + 2 x\right)\,\mathrm{d}y & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(- x^{2} y - 2 y\right)x\prime(t)\,\mathrm{d}t+\left(- 2 x y^{2} + 2 x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(\left(- x^{2} y - 2 y\right)x\prime(t)+\left(- 2 x y^{2} + 2 x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(\left(- 36 \sin{\left(t \right)} \cos^{2}{\left(t \right)} - 8 \sin{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(- 96 \sin^{2}{\left(t \right)} \cos{\left(t \right)} + 6 \cos{\left(t \right)}\right)\left(4 \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(\left(108 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(24 \sin^{2}{\left(t \right)}\right)+\left(24 \cos^{2}{\left(t \right)}\right)+\left(- 384 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(- 276 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} + 24\right)\,\mathrm{d}t\\ & =\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\left(\frac{69 \cos{\left(4 t \right)}}{2} - \frac{21}{2}\right)\,\mathrm{d}t\\ & =\left[- \frac{21 t}{2} + \frac{69 \sin{\left(4 t \right)}}{8}\right]_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\\ & =\left(- \frac{21 \left(\frac{3 \pi}{2}\right)}{2} + \frac{69 \sin{\left(4 \left(\frac{3 \pi}{2}\right) \right)}}{8}\right)-\left(- \frac{21 \left(\frac{\pi}{2}\right)}{2} + \frac{69 \sin{\left(4 \left(\frac{\pi}{2}\right) \right)}}{8}\right)\\ & =\left(\left(- \frac{63 \pi}{4}\right)+\left(0\right)\right)-\left(\left(- \frac{21 \pi}{4}\right)+\left(0\right)\right)\\ & =- \frac{21 \pi}{2}\end{aligned}
$$

## Authored hard seed 1

Evaluate $\int_C\left(- x^{2} y + 4 y\right)\,\mathrm{d}x+\left(x y^{2} - 4 x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 4 y^{2}=4$ traversed in the counterclockwise direction from the point $(0,-1)$ to the point $(0,1)$.

- $- 3 \pi$
- $- \frac{3 \pi}{4}$
- $0$
- $- \frac{27 \pi}{4}$
- $- \frac{15 \pi}{4}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=2 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[\frac{3 \pi}{2},\frac{5 \pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 2 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- x^{2} y + 4 y\right)\,\mathrm{d}x+\left(x y^{2} - 4 x\right)\,\mathrm{d}y & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(- x^{2} y + 4 y\right)x\prime(t)\,\mathrm{d}t+\left(x y^{2} - 4 x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(\left(- x^{2} y + 4 y\right)x\prime(t)+\left(x y^{2} - 4 x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(\left(- 4 \sin{\left(t \right)} \cos^{2}{\left(t \right)} + 4 \sin{\left(t \right)}\right)\left(- 2 \sin{\left(t \right)}\right)+\left(2 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 8 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(\left(8 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 8 \sin^{2}{\left(t \right)}\right)+\left(- 8 \cos^{2}{\left(t \right)}\right)+\left(2 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(10 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} - 8\right)\,\mathrm{d}t\\ & =\int_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\left(- \frac{5 \cos{\left(4 t \right)}}{4} - \frac{27}{4}\right)\,\mathrm{d}t\\ & =\left[- \frac{27 t}{4} - \frac{5 \sin{\left(4 t \right)}}{16}\right]_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}\\ & =\left(- \frac{27 \left(\frac{5 \pi}{2}\right)}{4} - \frac{5 \sin{\left(4 \left(\frac{5 \pi}{2}\right) \right)}}{16}\right)-\left(- \frac{27 \left(\frac{3 \pi}{2}\right)}{4} - \frac{5 \sin{\left(4 \left(\frac{3 \pi}{2}\right) \right)}}{16}\right)\\ & =\left(\left(- \frac{135 \pi}{8}\right)+\left(0\right)\right)-\left(\left(- \frac{81 \pi}{8}\right)+\left(0\right)\right)\\ & =- \frac{27 \pi}{4}\end{aligned}
$$
