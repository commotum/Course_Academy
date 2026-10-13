# Review: potential reconstruction and endpoint subtraction

Original records and banks are retained in source-cases.json. Standard TeX is computed throughout; two documented endpoint typos are repaired in replay solutions.

## Original q-39349

Consider the vector field $F,$ defined as

$$
F(x,y)=\frac{x}{1+{x}^{2}+{y}^{2}}\,i+\frac{y}{1+{x}^{2}+{y}^{2}}\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}\operatorname{ln}⁡(x+1)$ for $x\in [0,1].$

Options: $\frac{1}{2}\operatorname{ln}⁡(2+\operatorname{ln}⁡2)$, $\frac{1}{2}\operatorname{ln}⁡(1+{ln}^{2}⁡2)$, $\frac{1}{2}\operatorname{ln}⁡(4)$, $\frac{1}{2}\operatorname{ln}⁡(2)$, $\frac{1}{2}\operatorname{ln}⁡(2+{ln}^{2}⁡2)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{\frac{x}{1+{x}^{2}+{y}^{2}}}_{⏟}}_{P(x,y)}\,i+{{\frac{y}{1+{x}^{2}+{y}^{2}}}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}=-\frac{2xy}{(1+{x}^{2}+{y}^{2})^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{x}{1+{x}^{2}+{y}^{2}}, \\ {f}_{y}(x,y) & =\frac{y}{1+{x}^{2}+{y}^{2}}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{1}{2}\operatorname{ln}⁡(1+{x}^{2}+{y}^{2}).
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,{t}^{2}\operatorname{ln}⁡(t+1)⟩,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩, \\ r(1) & =⟨1,\operatorname{ln}⁡2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\operatorname{ln}⁡2).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(1,\operatorname{ln}⁡2)-f(0,0) \\  & =\frac{1}{2}\operatorname{ln}⁡(1+{1}^{2}+{ln}^{2}⁡2)-\frac{1}{2}\operatorname{ln}⁡(1+{0}^{2}+{0}^{2}) \\  & =\frac{1}{2}\operatorname{ln}⁡(2+{ln}^{2}⁡2)-0 \\  & =\frac{1}{2}\operatorname{ln}⁡(2+{ln}^{2}⁡2).\end{aligned}
$$

## Original q-98995

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨t+\operatorname{sin}⁡(\frac{\pi t}{2}),t+\operatorname{cos}⁡(\frac{\pi t}{2})⟩,\,0\le t\le 1.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=x{y}^{2}\,i+{x}^{2}y\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: $4$, $6$, $\frac{1}{2}$, $1$, $2$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & =x{y}^{2}, \\ {f}_{y}(x,y) & ={x}^{2}y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{1}{2}{x}^{2}{y}^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩, \\ r(1) & =⟨2,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(2,1)-f(0,1) \\  & =\frac{1}{2}\cdot {2}^{2}\cdot {1}^{2}-\frac{1}{2}\cdot {0}^{2}\cdot {1}^{2} \\  & =2-0 \\  & =2.\end{aligned}
$$

## Original q-104725

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨t,{e}^{t}⟩,\,0\le t\le 1.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(3{x}^{2}{y}^{3}+2x)\,i+(3{x}^{3}{y}^{2}-4y)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: ${e}^{2}+{e}^{2}+1$, $0$, ${e}^{3}+{e}^{2}$, ${e}^{3}-2{e}^{2}+3$, $1+{e}^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & =3{x}^{2}{y}^{3}+2x, \\ {f}_{y}(x,y) & =3{x}^{3}{y}^{2}-4y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={x}^{3}{y}^{3}+{x}^{2}-2{y}^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩, \\ r(1) & =⟨1,e⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(1,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(1,e)-f(0,1) \\  & =({1}^{3}\cdot {e}^{3}+{1}^{2}-2\cdot {e}^{2})-({0}^{3}\cdot {1}^{3}+{0}^{2}-2\cdot {1}^{2}) \\  & ={e}^{3}+1-2{e}^{2}+2 \\  & ={e}^{3}-2{e}^{2}+3.\end{aligned}
$$

## Original q-104728

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨{t}^{2}+1,t⟩,\,0\le t\le 2\pi .
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F={e}^{x}\operatorname{cos}⁡y\,i-{e}^{x}\operatorname{sin}⁡y\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: ${e}^{{\pi }^{2}+1}$, $e({e}^{4{\pi }^{2}}-1)$, ${e}^{4\pi }$, $0$, $e({e}^{2\pi }-1)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & ={e}^{x}\operatorname{cos}⁡y, \\ {f}_{y}(x,y) & =-{e}^{x}\operatorname{sin}⁡y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={e}^{x}\operatorname{cos}⁡y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,0⟩, \\ r(2\pi ) & =⟨4{\pi }^{2}+1,2\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(4{\pi }^{2}+1,2\pi ).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(4{\pi }^{2}+1,2\pi )-f(1,0) \\  & ={e}^{4{\pi }^{2}+1}\cdot \operatorname{cos}⁡2\pi -{e}^{1}\cdot \operatorname{cos}⁡0 \\  & ={e}^{4{\pi }^{2}+1}-e \\  & =e({e}^{4{\pi }^{2}}-1).\end{aligned}
$$

## Original q-104731

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨2t,{t}^{2}-1⟩,\,0\le t\le 2.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(2xy-y)\,i+({x}^{2}-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: $12$, $48$, $0$, $36$, $24$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & =2xy-y, \\ {f}_{y}(x,y) & ={x}^{2}-x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={x}^{2}y-xy.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-1⟩, \\ r(2) & =⟨4,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(4,3)-f(0,-1) \\  & =({4}^{2}\cdot 3-4\cdot 3)-({0}^{2}\cdot (-1)-0\cdot (-1)) \\  & =48-12 \\  & =36.\end{aligned}
$$

## Original q-104733

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨3\operatorname{ln}⁡t,{t}^{2}⟩,\,1\le t\le 2.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=({x}^{2}-y)\,i+({y}^{2}-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: $9{ln}^{3}⁡2-12\operatorname{ln}⁡2+21$, ${ln}^{2}⁡2+9$, ${ln}^{3}⁡2-63$, ${ln}^{3}⁡2+\operatorname{ln}⁡2-9$, $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & ={x}^{2}-y, \\ {f}_{y}(x,y) & ={y}^{2}-x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{1}{3}{x}^{3}+\frac{1}{3}{y}^{3}-xy.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =⟨0,1⟩, \\ r(2) & =⟨3\operatorname{ln}⁡2,4⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(3\operatorname{ln}⁡2,4).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(3\operatorname{ln}⁡2,4)-f(0,1) \\  & =(\frac{1}{3}\cdot (3\operatorname{ln}⁡2)^{3}+\frac{1}{3}\cdot {4}^{3}-3\operatorname{ln}⁡2\cdot 4)-(\frac{1}{3}\cdot {0}^{3}+\frac{1}{3}\cdot {1}^{3}-0\cdot 1) \\  & =9{ln}^{3}⁡2+\frac{64}{3}-12\operatorname{ln}⁡2-\frac{1}{3} \\  & =9{ln}^{3}⁡2-12\operatorname{ln}⁡2+21.\end{aligned}
$$

## Original q-104739

Consider the vector field $F,$ defined as

$$
F(x,y)={y}^{2}\operatorname{cos}⁡x\,i+(2y\operatorname{sin}⁡x+{e}^{y})\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}+{sin}^{2}⁡x$ for $x\in [0,\pi ].$

Options: ${e}^{{\pi }^{2}}-1$, ${e}^{\pi -1}$, ${\pi }^{2}$, ${e}^{2}+\pi $, $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{{y}^{2}\operatorname{cos}⁡x}_{⏟}}_{P(x,y)}\,i+{{(2y\operatorname{sin}⁡x+{e}^{y})}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}=2y\operatorname{cos}⁡x
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & ={y}^{2}\operatorname{cos}⁡x, \\ {f}_{y}(x,y) & =2y\operatorname{sin}⁡x+{e}^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={y}^{2}\operatorname{sin}⁡x+{e}^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,{t}^{2}+{sin}^{2}⁡t⟩,\,t\in [0,\pi ].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩, \\ r(\pi ) & =⟨\pi ,{\pi }^{2}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi ,{\pi }^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(\pi ,{\pi }^{2})-f(0,0) \\  & =({\pi }^{4}\cdot \operatorname{sin}⁡\pi +{e}^{{\pi }^{2}})-({0}^{2}\cdot \operatorname{sin}⁡0+{e}^{0}) \\  & =(0+{e}^{{\pi }^{2}})-(0+1) \\  & ={e}^{{\pi }^{2}}-1.\end{aligned}
$$

## Original q-104745

Consider the vector field $F,$ defined as

$$
F(x,y)=({e}^{y}+y\operatorname{cos}⁡x)\,i+(x{e}^{y}+\operatorname{sin}⁡x)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x+\operatorname{cos}⁡x$ for $x\in [0,\pi ].$

Options: ${e}^{\pi }+1$, ${e}^{{\pi }^{2}-1}$, $\pi {e}^{\pi -1}$, $2\pi $, ${\pi }^{2}+1$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{({e}^{y}+y\operatorname{cos}⁡x)}_{⏟}}_{P(x,y)}\,i+{{(x{e}^{y}+\operatorname{sin}⁡x)}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}={e}^{y}+\operatorname{cos}⁡x.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & ={e}^{y}+y\operatorname{cos}⁡x, \\ {f}_{y}(x,y) & =x{e}^{y}+\operatorname{sin}⁡x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x{e}^{y}+y\operatorname{sin}⁡x.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,t+\operatorname{cos}⁡t⟩,\,t\in [0,\pi ].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩, \\ r(\pi ) & =⟨\pi ,\pi -1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi ,\pi -1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(\pi ,\pi -1)-f(0,1) \\  & =(\pi \cdot {e}^{\pi -1}+(\pi -1)\cdot \operatorname{sin}⁡\pi )-(0\cdot {e}^{1}+1\cdot \operatorname{sin}⁡0) \\  & =(\pi {e}^{\pi -1}+0)-0 \\  & =\pi {e}^{\pi -1}.\end{aligned}
$$

## Original q-104747

Consider the vector field $F,$ defined as

$$
F(x,y)=\operatorname{cos}⁡x\operatorname{sin}⁡y\,i+\operatorname{cos}⁡y\operatorname{sin}⁡x\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={e}^{\operatorname{sin}⁡x}+\operatorname{cos}⁡x$ for $x\in [0,\frac{\pi }{2}].$

Options: $\operatorname{sin}⁡2\operatorname{sin}⁡(e-1)$, $\operatorname{sin}⁡e-\operatorname{sin}⁡2$, $\operatorname{sin}⁡e$, $2\operatorname{sin}⁡e-1$, $\operatorname{sin}⁡2e-\operatorname{sin}⁡{e}^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{\operatorname{cos}⁡x\operatorname{sin}⁡y}_{⏟}}_{P(x,y)}\,i+{{\operatorname{cos}⁡y\operatorname{sin}⁡x}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}=\operatorname{cos}⁡x\operatorname{cos}⁡y.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & =\operatorname{cos}⁡x\operatorname{sin}⁡y, \\ {f}_{y}(x,y) & =\operatorname{cos}⁡y\operatorname{sin}⁡x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\operatorname{sin}⁡x\operatorname{sin}⁡y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,{e}^{\operatorname{sin}⁡t}+\operatorname{cos}⁡t⟩,\,t\in [0,\frac{\pi }{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,2⟩, \\ r(\frac{\pi }{2}) & =⟨\frac{\pi }{2},e⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\frac{\pi }{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(\frac{\pi }{2},e)-f(0,2) \\  & =(\operatorname{sin}⁡(\frac{\pi }{2})\cdot \operatorname{sin}⁡e)-(\operatorname{sin}⁡0\cdot \operatorname{sin}⁡2) \\  & =1\cdot \operatorname{sin}⁡e-0\cdot \operatorname{sin}⁡2 \\  & =\operatorname{sin}⁡e.\end{aligned}
$$

## Original q-104761

Consider the vector field $F,$ defined as

$$
F(x,y)=2x{e}^{-y}\,i+(2y-{x}^{2}{e}^{-y})\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\operatorname{ln}⁡(x-1)$ for $x\in [2,3].$

Options: $1-\operatorname{ln}⁡2$, $\frac{1}{2}+{ln}^{2}⁡2$, $1+{ln}^{2}⁡3$, $\frac{{ln}^{2}⁡2}{3}$, $\frac{1}{2}+\operatorname{ln}⁡3$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{2x{e}^{-y}}_{⏟}}_{P(x,y)}\,i+{{(2y-{x}^{2}{e}^{-y})}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}=-2x{e}^{-y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & =2x{e}^{-y}, \\ {f}_{y}(x,y) & =2y-{x}^{2}{e}^{-y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={x}^{2}{e}^{-y}+{y}^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,\operatorname{ln}⁡(t-1)⟩,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =⟨2,0⟩, \\ r(3) & =⟨3,\operatorname{ln}⁡2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\operatorname{ln}⁡2).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(3,\operatorname{ln}⁡2)-f(2,0) \\  & =({3}^{2}\cdot {e}^{-\operatorname{ln}⁡2}+(\operatorname{ln}⁡2)^{2})-({2}^{2}\cdot {e}^{-0}+{0}^{2}) \\  & =\frac{9}{2}+{ln}^{2}⁡2-4 \\  & =\frac{1}{2}+{ln}^{2}⁡2.\end{aligned}
$$

## Original q-104764

Consider the vector field $F,$ defined as

$$
F(x,y)=(6{x}^{2}-y)\,i-x\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y={x}^{2}-{e}^{\sqrt{x+1}}$ for $x\in [0,3].$

Options: $3{e}^{2}-1$, $3(e+3)$, ${e}^{2}+27$, $9(3e-1)$, $3({e}^{2}+9)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)={{(6{x}^{2}-y)}_{⏟}}_{P(x,y)}\,i+{{(-x)}_{⏟}}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{∂P}{∂y}=\frac{∂Q}{∂x}=-1.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}{f}_{x}(x,y) & =6{x}^{2}-y, \\ {f}_{y}(x,y) & =-x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2{x}^{3}-xy.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=⟨t,{t}^{2}-{e}^{\sqrt{t+1}}⟩,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-e⟩, \\ r(3) & =⟨3,9-{e}^{2}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-e)$ and $(3,9-{e}^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(3,9-{e}^{2})-f(0,e) \\  & =(2\cdot {3}^{3}-3\cdot (9-{e}^{2}))-(2\cdot {0}^{3}-0\cdot (-e)) \\  & =(54-27+3{e}^{2})-0 \\  & =(27+3{e}^{2})-0 \\  & =3({e}^{2}+9).\end{aligned}
$$

## Original q-104732

Consider the curve $C,$ defined parametrically as

$$
r(t)=⟨\operatorname{sin}⁡\pi t,\frac{\pi t}{2}⟩,\,0\le t\le \frac{1}{2}.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F=(2x\operatorname{cos}⁡y+y)\,i-({x}^{2}\operatorname{sin}⁡y-x)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

Options: $\frac{2\sqrt{2}+\pi }{4}$, $\frac{2\sqrt{2}-\pi }{2}$, $\frac{\sqrt{2}}{2}$, $0$, $\frac{\sqrt{2}}{2}+1$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}{f}_{x}(x,y) & =2x\operatorname{cos}⁡y+y, \\ {f}_{y}(x,y) & =-{x}^{2}\operatorname{sin}⁡y+x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)={x}^{2}\operatorname{cos}⁡y+xy.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩, \\ r(\frac{1}{2}) & =⟨1,\frac{\pi }{4}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\frac{\pi }{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{C}∇f\cdot \text{d}r \\  & =f(1,\frac{\pi }{4})-f(0,0) \\  & =({1}^{2}\cdot \operatorname{cos}⁡(\frac{\pi }{4})+1\cdot (\frac{\pi }{4}))-({0}^{2}\cdot \operatorname{cos}⁡0+0\cdot 0) \\  & =\frac{\sqrt{2}}{2}+\frac{\pi }{4} \\  & =\frac{2\sqrt{2}+\pi }{4}.\end{aligned}
$$

## Original replay q-39349

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\frac{x}{x^{2} + y^{2} + 1}\right)\,i+\left(\frac{y}{x^{2} + y^{2} + 1}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} \ln{\left(x + 1 \right)}$ for $x\in [0,1].$

- $\frac{\ln{\left(\ln{\left(2 \right)} + 2 \right)}}{2}$
- $\frac{\ln{\left(\ln{\left(2 \right)}^{2} + 1 \right)}}{2}$
- $\ln{\left(2 \right)}$
- $\frac{\ln{\left(2 \right)}}{2}$
- $\frac{\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\frac{x}{x^{2} + y^{2} + 1}\right)}_{P(x,y)}\,i+\underbrace{\left(\frac{y}{x^{2} + y^{2} + 1}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- \frac{2 x y}{\left(x^{2} + y^{2} + 1\right)^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\frac{x}{x^{2} + y^{2} + 1}, \\ f_y(x,y) & =\frac{y}{x^{2} + y^{2} + 1}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{\ln{\left(x^{2} + y^{2} + 1 \right)}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} \ln{\left(t + 1 \right)}\rangle,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(1) & =\langle 1,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\ln{\left(2 \right)})-f(0,0) \\  & =\frac{\ln{\left(\left(1\right)^{2} + \left(\ln{\left(2 \right)}\right)^{2} + 1 \right)}}{2}-\frac{\ln{\left(\left(0\right)^{2} + \left(0\right)^{2} + 1 \right)}}{2} \\  & =\frac{\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}-\left(0\right) \\  & =\frac{\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}.\end{aligned}
$$

## Generated observed-profile variant q-39349 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\frac{2 x}{x^{2} + y^{2} + 1}\right)\,i+\left(\frac{2 y}{x^{2} + y^{2} + 1}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} \ln{\left(x + 1 \right)}$ for $x\in [0,1].$

- $\ln{\left(\ln{\left(2 \right)} + 2 \right)}$
- $\ln{\left(\ln{\left(2 \right)}^{2} + 1 \right)}$
- $2 \ln{\left(2 \right)}$
- $\ln{\left(2 \right)}$
- $\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\frac{2 x}{x^{2} + y^{2} + 1}\right)}_{P(x,y)}\,i+\underbrace{\left(\frac{2 y}{x^{2} + y^{2} + 1}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- \frac{4 x y}{\left(x^{2} + y^{2} + 1\right)^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\frac{2 x}{x^{2} + y^{2} + 1}, \\ f_y(x,y) & =\frac{2 y}{x^{2} + y^{2} + 1}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\ln{\left(x^{2} + y^{2} + 1 \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} \ln{\left(t + 1 \right)}\rangle,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(1) & =\langle 1,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\ln{\left(2 \right)})-f(0,0) \\  & =\ln{\left(\left(1\right)^{2} + \left(\ln{\left(2 \right)}\right)^{2} + 1 \right)}-\ln{\left(\left(0\right)^{2} + \left(0\right)^{2} + 1 \right)} \\  & =\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}-\left(0\right) \\  & =\ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}.\end{aligned}
$$

## Generated observed-profile variant q-39349 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\frac{3 x}{x^{2} + y^{2} + 1}\right)\,i+\left(\frac{3 y}{x^{2} + y^{2} + 1}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} \ln{\left(x + 1 \right)}$ for $x\in [0,1].$

- $\frac{3 \ln{\left(\ln{\left(2 \right)} + 2 \right)}}{2}$
- $\frac{3 \ln{\left(\ln{\left(2 \right)}^{2} + 1 \right)}}{2}$
- $3 \ln{\left(2 \right)}$
- $\frac{3 \ln{\left(2 \right)}}{2}$
- $\frac{3 \ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\frac{3 x}{x^{2} + y^{2} + 1}\right)}_{P(x,y)}\,i+\underbrace{\left(\frac{3 y}{x^{2} + y^{2} + 1}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- \frac{6 x y}{\left(x^{2} + y^{2} + 1\right)^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\frac{3 x}{x^{2} + y^{2} + 1}, \\ f_y(x,y) & =\frac{3 y}{x^{2} + y^{2} + 1}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{3 \ln{\left(x^{2} + y^{2} + 1 \right)}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} \ln{\left(t + 1 \right)}\rangle,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(1) & =\langle 1,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\ln{\left(2 \right)})-f(0,0) \\  & =\frac{3 \ln{\left(\left(1\right)^{2} + \left(\ln{\left(2 \right)}\right)^{2} + 1 \right)}}{2}-\frac{3 \ln{\left(\left(0\right)^{2} + \left(0\right)^{2} + 1 \right)}}{2} \\  & =\frac{3 \ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}-\left(0\right) \\  & =\frac{3 \ln{\left(\ln{\left(2 \right)}^{2} + 2 \right)}}{2}.\end{aligned}
$$

## Original replay q-98995

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t + \sin{\left(\frac{\pi t}{2} \right)},t + \cos{\left(\frac{\pi t}{2} \right)}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(x y^{2}\right)\,i+\left(x^{2} y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $4$
- $6$
- $\frac{1}{2}$
- $1$
- $2$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =x y^{2}, \\ f_y(x,y) & =x^{2} y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{x^{2} y^{2}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 2,1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,1)-f(0,1) \\  & =\frac{\left(2\right)^{2} \left(1\right)^{2}}{2}-\frac{\left(0\right)^{2} \left(1\right)^{2}}{2} \\  & =2-\left(0\right) \\  & =2.\end{aligned}
$$

## Generated observed-profile variant q-98995 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t + \sin{\left(\frac{\pi t}{2} \right)},t + \cos{\left(\frac{\pi t}{2} \right)}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x y^{2}\right)\,i+\left(2 x^{2} y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $8$
- $12$
- $1$
- $2$
- $4$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x y^{2}, \\ f_y(x,y) & =2 x^{2} y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 2,1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,1)-f(0,1) \\  & =\left(2\right)^{2} \left(1\right)^{2}-\left(0\right)^{2} \left(1\right)^{2} \\  & =4-\left(0\right) \\  & =4.\end{aligned}
$$

## Generated observed-profile variant q-98995 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t + \sin{\left(\frac{\pi t}{2} \right)},t + \cos{\left(\frac{\pi t}{2} \right)}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(3 x y^{2}\right)\,i+\left(3 x^{2} y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $12$
- $18$
- $\frac{3}{2}$
- $3$
- $6$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =3 x y^{2}, \\ f_y(x,y) & =3 x^{2} y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{3 x^{2} y^{2}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 2,1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,1)-f(0,1) \\  & =\frac{3 \left(2\right)^{2} \left(1\right)^{2}}{2}-\frac{3 \left(0\right)^{2} \left(1\right)^{2}}{2} \\  & =6-\left(0\right) \\  & =6.\end{aligned}
$$

## Original replay q-104725

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t,e^{t}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(3 x^{2} y^{3} + 2 x\right)\,i+\left(3 x^{3} y^{2} - 4 y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $1 + 2 e^{2}$
- $0$
- $e^{2} + e^{3}$
- $- 2 e^{2} + 3 + e^{3}$
- $1 + e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =3 x^{2} y^{3} + 2 x, \\ f_y(x,y) & =3 x^{3} y^{2} - 4 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{3} y^{3} + x^{2} - 2 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 1,e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(1,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,e)-f(0,1) \\  & =\left(\left(1\right)^{3} \left(e\right)^{3}+\left(1\right)^{2}- 2 \left(e\right)^{2}\right)-\left(\left(0\right)^{3} \left(1\right)^{3}+\left(0\right)^{2}- 2 \left(1\right)^{2}\right) \\  & =e^{3}+1- 2 e^{2}+2 \\  & =- 2 e^{2} + 3 + e^{3}.\end{aligned}
$$

## Generated observed-profile variant q-104725 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t,e^{t}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(6 x^{2} y^{3} + 4 x\right)\,i+\left(6 x^{3} y^{2} - 8 y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $2 + 4 e^{2}$
- $0$
- $2 \left(1 + e\right) e^{2}$
- $- 4 e^{2} + 6 + 2 e^{3}$
- $2 + 2 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =6 x^{2} y^{3} + 4 x, \\ f_y(x,y) & =6 x^{3} y^{2} - 8 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x^{3} y^{3} + 2 x^{2} - 4 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 1,e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(1,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,e)-f(0,1) \\  & =\left(2 \left(1\right)^{3} \left(e\right)^{3}+2 \left(1\right)^{2}- 4 \left(e\right)^{2}\right)-\left(2 \left(0\right)^{3} \left(1\right)^{3}+2 \left(0\right)^{2}- 4 \left(1\right)^{2}\right) \\  & =2 e^{3}+2- 4 e^{2}+4 \\  & =- 4 e^{2} + 6 + 2 e^{3}.\end{aligned}
$$

## Generated observed-profile variant q-104725 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t,e^{t}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(9 x^{2} y^{3} + 6 x\right)\,i+\left(9 x^{3} y^{2} - 12 y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $3 + 6 e^{2}$
- $0$
- $3 \left(1 + e\right) e^{2}$
- $- 6 e^{2} + 9 + 3 e^{3}$
- $3 + 3 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =9 x^{2} y^{3} + 6 x, \\ f_y(x,y) & =9 x^{3} y^{2} - 12 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x^{3} y^{3} + 3 x^{2} - 6 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 1,e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(1,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,e)-f(0,1) \\  & =\left(3 \left(1\right)^{3} \left(e\right)^{3}+3 \left(1\right)^{2}- 6 \left(e\right)^{2}\right)-\left(3 \left(0\right)^{3} \left(1\right)^{3}+3 \left(0\right)^{2}- 6 \left(1\right)^{2}\right) \\  & =3 e^{3}+3- 6 e^{2}+6 \\  & =- 6 e^{2} + 9 + 3 e^{3}.\end{aligned}
$$

## Original replay q-104728

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t^{2} + 1,t\rangle,\,t\in [0,2 \pi].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(e^{x} \cos{\left(y \right)}\right)\,i+\left(- e^{x} \sin{\left(y \right)}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $e^{1 + \pi^{2}}$
- $- e + e^{1 + 4 \pi^{2}}$
- $e^{4 \pi}$
- $0$
- $- e \left(1 - e^{2 \pi}\right)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =e^{x} \cos{\left(y \right)}, \\ f_y(x,y) & =- e^{x} \sin{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=e^{x} \cos{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 1,0\rangle, \\ r(2 \pi) & =\langle 1 + 4 \pi^{2},2 \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(1 + 4 \pi^{2},2 \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1 + 4 \pi^{2},2 \pi)-f(1,0) \\  & =e^{\left(1 + 4 \pi^{2}\right)} \cos{\left(\left(2 \pi\right) \right)}-e^{\left(1\right)} \cos{\left(\left(0\right) \right)} \\  & =e^{1 + 4 \pi^{2}}-\left(e\right) \\  & =e \left(-1 + e^{4 \pi^{2}}\right).\end{aligned}
$$

## Generated observed-profile variant q-104728 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t^{2} + 1,t\rangle,\,t\in [0,2 \pi].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 e^{x} \cos{\left(y \right)}\right)\,i+\left(- 2 e^{x} \sin{\left(y \right)}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $2 e^{1 + \pi^{2}}$
- $- 2 e + 2 e^{1 + 4 \pi^{2}}$
- $2 e^{4 \pi}$
- $0$
- $- 2 e \left(1 - e^{2 \pi}\right)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 e^{x} \cos{\left(y \right)}, \\ f_y(x,y) & =- 2 e^{x} \sin{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 e^{x} \cos{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 1,0\rangle, \\ r(2 \pi) & =\langle 1 + 4 \pi^{2},2 \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(1 + 4 \pi^{2},2 \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1 + 4 \pi^{2},2 \pi)-f(1,0) \\  & =2 e^{\left(1 + 4 \pi^{2}\right)} \cos{\left(\left(2 \pi\right) \right)}-2 e^{\left(1\right)} \cos{\left(\left(0\right) \right)} \\  & =2 e^{1 + 4 \pi^{2}}-\left(2 e\right) \\  & =2 e \left(-1 + e^{4 \pi^{2}}\right).\end{aligned}
$$

## Generated observed-profile variant q-104728 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t^{2} + 1,t\rangle,\,t\in [0,2 \pi].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(3 e^{x} \cos{\left(y \right)}\right)\,i+\left(- 3 e^{x} \sin{\left(y \right)}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $3 e^{1 + \pi^{2}}$
- $- 3 e + 3 e^{1 + 4 \pi^{2}}$
- $3 e^{4 \pi}$
- $0$
- $- 3 e \left(1 - e^{2 \pi}\right)$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =3 e^{x} \cos{\left(y \right)}, \\ f_y(x,y) & =- 3 e^{x} \sin{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 e^{x} \cos{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 1,0\rangle, \\ r(2 \pi) & =\langle 1 + 4 \pi^{2},2 \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(1 + 4 \pi^{2},2 \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1 + 4 \pi^{2},2 \pi)-f(1,0) \\  & =3 e^{\left(1 + 4 \pi^{2}\right)} \cos{\left(\left(2 \pi\right) \right)}-3 e^{\left(1\right)} \cos{\left(\left(0\right) \right)} \\  & =3 e^{1 + 4 \pi^{2}}-\left(3 e\right) \\  & =3 e \left(-1 + e^{4 \pi^{2}}\right).\end{aligned}
$$

## Original replay q-104731

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t,t^{2} - 1\rangle,\,t\in [0,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x y - y\right)\,i+\left(x^{2} - x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $12$
- $48$
- $0$
- $36$
- $24$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x y - y, \\ f_y(x,y) & =x^{2} - x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} y - x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,-1\rangle, \\ r(2) & =\langle 4,3\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(4,3)-f(0,-1) \\  & =\left(\left(4\right)^{2} \left(3\right)- \left(4\right) \left(3\right)\right)-\left(\left(0\right)^{2} \left(-1\right)- \left(0\right) \left(-1\right)\right) \\  & =48-12 \\  & =36.\end{aligned}
$$

## Generated observed-profile variant q-104731 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t,t^{2} - 1\rangle,\,t\in [0,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(4 x y - 2 y\right)\,i+\left(2 x^{2} - 2 x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $24$
- $96$
- $0$
- $72$
- $48$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =4 x y - 2 y, \\ f_y(x,y) & =2 x^{2} - 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x^{2} y - 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,-1\rangle, \\ r(2) & =\langle 4,3\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(4,3)-f(0,-1) \\  & =\left(2 \left(4\right)^{2} \left(3\right)- 2 \left(4\right) \left(3\right)\right)-\left(2 \left(0\right)^{2} \left(-1\right)- 2 \left(0\right) \left(-1\right)\right) \\  & =96-24 \\  & =72.\end{aligned}
$$

## Generated observed-profile variant q-104731 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t,t^{2} - 1\rangle,\,t\in [0,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(6 x y - 3 y\right)\,i+\left(3 x^{2} - 3 x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $36$
- $144$
- $0$
- $108$
- $72$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =6 x y - 3 y, \\ f_y(x,y) & =3 x^{2} - 3 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x^{2} y - 3 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,-1\rangle, \\ r(2) & =\langle 4,3\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(4,3)-f(0,-1) \\  & =\left(3 \left(4\right)^{2} \left(3\right)- 3 \left(4\right) \left(3\right)\right)-\left(3 \left(0\right)^{2} \left(-1\right)- 3 \left(0\right) \left(-1\right)\right) \\  & =144-36 \\  & =108.\end{aligned}
$$

## Original replay q-104733

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 3 \ln{\left(t \right)},t^{2}\rangle,\,t\in [1,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(x^{2} - y\right)\,i+\left(- x + y^{2}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 12 \ln{\left(2 \right)} + 9 \ln{\left(2 \right)}^{3} + 21$
- $\ln{\left(2 \right)}^{2} + 9$
- $-63 + \ln{\left(2 \right)}^{3}$
- $-9 + \ln{\left(2 \right)}^{3} + \ln{\left(2 \right)}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =x^{2} - y, \\ f_y(x,y) & =- x + y^{2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{x^{3}}{3} - x y + \frac{y^{3}}{3}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =\langle 0,1\rangle, \\ r(2) & =\langle 3 \ln{\left(2 \right)},4\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(3 \ln{\left(2 \right)},4).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3 \ln{\left(2 \right)},4)-f(0,1) \\  & =\left(\frac{\left(3 \ln{\left(2 \right)}\right)^{3}}{3}+\frac{\left(4\right)^{3}}{3}- \left(3 \ln{\left(2 \right)}\right) \left(4\right)\right)-\left(\frac{\left(0\right)^{3}}{3}+\frac{\left(1\right)^{3}}{3}- \left(0\right) \left(1\right)\right) \\  & =9 \ln{\left(2 \right)}^{3}+\frac{64}{3}- 12 \ln{\left(2 \right)}- \frac{1}{3} \\  & =- 12 \ln{\left(2 \right)} + 9 \ln{\left(2 \right)}^{3} + 21.\end{aligned}
$$

## Generated observed-profile variant q-104733 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 3 \ln{\left(t \right)},t^{2}\rangle,\,t\in [1,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x^{2} - 2 y\right)\,i+\left(- 2 x + 2 y^{2}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 24 \ln{\left(2 \right)} + 18 \ln{\left(2 \right)}^{3} + 42$
- $2 \ln{\left(2 \right)}^{2} + 18$
- $-126 + 2 \ln{\left(2 \right)}^{3}$
- $-18 + 2 \ln{\left(2 \right)}^{3} + 2 \ln{\left(2 \right)}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x^{2} - 2 y, \\ f_y(x,y) & =- 2 x + 2 y^{2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{2 x^{3}}{3} - 2 x y + \frac{2 y^{3}}{3}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =\langle 0,1\rangle, \\ r(2) & =\langle 3 \ln{\left(2 \right)},4\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(3 \ln{\left(2 \right)},4).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3 \ln{\left(2 \right)},4)-f(0,1) \\  & =\left(\frac{2 \left(3 \ln{\left(2 \right)}\right)^{3}}{3}+\frac{2 \left(4\right)^{3}}{3}- 2 \left(3 \ln{\left(2 \right)}\right) \left(4\right)\right)-\left(\frac{2 \left(0\right)^{3}}{3}+\frac{2 \left(1\right)^{3}}{3}- 2 \left(0\right) \left(1\right)\right) \\  & =18 \ln{\left(2 \right)}^{3}+\frac{128}{3}- 24 \ln{\left(2 \right)}- \frac{2}{3} \\  & =- 24 \ln{\left(2 \right)} + 18 \ln{\left(2 \right)}^{3} + 42.\end{aligned}
$$

## Generated observed-profile variant q-104733 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 3 \ln{\left(t \right)},t^{2}\rangle,\,t\in [1,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(3 x^{2} - 3 y\right)\,i+\left(- 3 x + 3 y^{2}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 36 \ln{\left(2 \right)} + 27 \ln{\left(2 \right)}^{3} + 63$
- $3 \ln{\left(2 \right)}^{2} + 27$
- $-189 + 3 \ln{\left(2 \right)}^{3}$
- $-27 + 3 \ln{\left(2 \right)}^{3} + 3 \ln{\left(2 \right)}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =3 x^{2} - 3 y, \\ f_y(x,y) & =- 3 x + 3 y^{2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{3} - 3 x y + y^{3}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =\langle 0,1\rangle, \\ r(2) & =\langle 3 \ln{\left(2 \right)},4\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(3 \ln{\left(2 \right)},4).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3 \ln{\left(2 \right)},4)-f(0,1) \\  & =\left(\left(3 \ln{\left(2 \right)}\right)^{3}+\left(4\right)^{3}- 3 \left(3 \ln{\left(2 \right)}\right) \left(4\right)\right)-\left(\left(0\right)^{3}+\left(1\right)^{3}- 3 \left(0\right) \left(1\right)\right) \\  & =27 \ln{\left(2 \right)}^{3}+64- 36 \ln{\left(2 \right)}-1 \\  & =- 36 \ln{\left(2 \right)} + 27 \ln{\left(2 \right)}^{3} + 63.\end{aligned}
$$

## Original replay q-104739

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(y^{2} \cos{\left(x \right)}\right)\,i+\left(2 y \sin{\left(x \right)} + e^{y}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} + \sin^{2}{\left(x \right)}$ for $x\in [0,\pi].$

- $-1 + e^{\pi^{2}}$
- $e^{-1 + \pi}$
- $\pi^{2}$
- $\pi + e^{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(y^{2} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(2 y \sin{\left(x \right)} + e^{y}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=2 y \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =y^{2} \cos{\left(x \right)}, \\ f_y(x,y) & =2 y \sin{\left(x \right)} + e^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=y^{2} \sin{\left(x \right)} + e^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} + \sin^{2}{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\pi) & =\langle \pi,\pi^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,\pi^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,\pi^{2})-f(0,0) \\  & =\left(\left(\left(\pi^{2}\right)\right)^{2} \sin{\left(\left(\pi\right) \right)}+e^{\left(\pi^{2}\right)}\right)-\left(\left(0\right)^{2} \sin{\left(\left(0\right) \right)}+e^{\left(0\right)}\right) \\  & =\left(0+e^{\pi^{2}}\right)-\left(0+1\right) \\  & =-1 + e^{\pi^{2}}.\end{aligned}
$$

## Generated observed-profile variant q-104739 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 y^{2} \cos{\left(x \right)}\right)\,i+\left(4 y \sin{\left(x \right)} + 2 e^{y}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} + \sin^{2}{\left(x \right)}$ for $x\in [0,\pi].$

- $-2 + 2 e^{\pi^{2}}$
- $2 e^{-1 + \pi}$
- $2 \pi^{2}$
- $2 \pi + 2 e^{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 y^{2} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(4 y \sin{\left(x \right)} + 2 e^{y}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=4 y \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 y^{2} \cos{\left(x \right)}, \\ f_y(x,y) & =4 y \sin{\left(x \right)} + 2 e^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 y^{2} \sin{\left(x \right)} + 2 e^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} + \sin^{2}{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\pi) & =\langle \pi,\pi^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,\pi^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,\pi^{2})-f(0,0) \\  & =\left(2 \left(\left(\pi^{2}\right)\right)^{2} \sin{\left(\left(\pi\right) \right)}+2 e^{\left(\pi^{2}\right)}\right)-\left(2 \left(0\right)^{2} \sin{\left(\left(0\right) \right)}+2 e^{\left(0\right)}\right) \\  & =\left(0+2 e^{\pi^{2}}\right)-\left(0+2\right) \\  & =-2 + 2 e^{\pi^{2}}.\end{aligned}
$$

## Generated observed-profile variant q-104739 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(3 y^{2} \cos{\left(x \right)}\right)\,i+\left(6 y \sin{\left(x \right)} + 3 e^{y}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} + \sin^{2}{\left(x \right)}$ for $x\in [0,\pi].$

- $-3 + 3 e^{\pi^{2}}$
- $3 e^{-1 + \pi}$
- $3 \pi^{2}$
- $3 \pi + 3 e^{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(3 y^{2} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(6 y \sin{\left(x \right)} + 3 e^{y}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=6 y \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =3 y^{2} \cos{\left(x \right)}, \\ f_y(x,y) & =6 y \sin{\left(x \right)} + 3 e^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 y^{2} \sin{\left(x \right)} + 3 e^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} + \sin^{2}{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\pi) & =\langle \pi,\pi^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,\pi^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,\pi^{2})-f(0,0) \\  & =\left(3 \left(\left(\pi^{2}\right)\right)^{2} \sin{\left(\left(\pi\right) \right)}+3 e^{\left(\pi^{2}\right)}\right)-\left(3 \left(0\right)^{2} \sin{\left(\left(0\right) \right)}+3 e^{\left(0\right)}\right) \\  & =\left(0+3 e^{\pi^{2}}\right)-\left(0+3\right) \\  & =-3 + 3 e^{\pi^{2}}.\end{aligned}
$$

## Original replay q-104745

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(y \cos{\left(x \right)} + e^{y}\right)\,i+\left(x e^{y} + \sin{\left(x \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x + \cos{\left(x \right)}$ for $x\in [0,\pi].$

- $1 + e^{\pi}$
- $e^{-1 + \pi^{2}}$
- $\pi e^{-1 + \pi}$
- $2 \pi$
- $1 + \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(y \cos{\left(x \right)} + e^{y}\right)}_{P(x,y)}\,i+\underbrace{\left(x e^{y} + \sin{\left(x \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=e^{y} + \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =y \cos{\left(x \right)} + e^{y}, \\ f_y(x,y) & =x e^{y} + \sin{\left(x \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x e^{y} + y \sin{\left(x \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t + \cos{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(\pi) & =\langle \pi,-1 + \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi,-1 + \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,-1 + \pi)-f(0,1) \\  & =\left(\left(\pi\right) e^{\left(-1 + \pi\right)}+\left(-1 + \pi\right) \sin{\left(\left(\pi\right) \right)}\right)-\left(\left(0\right) e^{\left(1\right)}+\left(1\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(\pi e^{-1 + \pi}+0\right)-\left(0\right) \\  & =\pi e^{-1 + \pi}.\end{aligned}
$$

## Generated observed-profile variant q-104745 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 y \cos{\left(x \right)} + 2 e^{y}\right)\,i+\left(2 x e^{y} + 2 \sin{\left(x \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x + \cos{\left(x \right)}$ for $x\in [0,\pi].$

- $2 + 2 e^{\pi}$
- $2 e^{-1 + \pi^{2}}$
- $2 \pi e^{-1 + \pi}$
- $4 \pi$
- $2 + 2 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 y \cos{\left(x \right)} + 2 e^{y}\right)}_{P(x,y)}\,i+\underbrace{\left(2 x e^{y} + 2 \sin{\left(x \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=2 e^{y} + 2 \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 y \cos{\left(x \right)} + 2 e^{y}, \\ f_y(x,y) & =2 x e^{y} + 2 \sin{\left(x \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x e^{y} + 2 y \sin{\left(x \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t + \cos{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(\pi) & =\langle \pi,-1 + \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi,-1 + \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,-1 + \pi)-f(0,1) \\  & =\left(2 \left(\pi\right) e^{\left(-1 + \pi\right)}+2 \left(-1 + \pi\right) \sin{\left(\left(\pi\right) \right)}\right)-\left(2 \left(0\right) e^{\left(1\right)}+2 \left(1\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(2 \pi e^{-1 + \pi}+0\right)-\left(0\right) \\  & =2 \pi e^{-1 + \pi}.\end{aligned}
$$

## Generated observed-profile variant q-104745 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(3 y \cos{\left(x \right)} + 3 e^{y}\right)\,i+\left(3 x e^{y} + 3 \sin{\left(x \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x + \cos{\left(x \right)}$ for $x\in [0,\pi].$

- $3 + 3 e^{\pi}$
- $3 e^{-1 + \pi^{2}}$
- $3 \pi e^{-1 + \pi}$
- $6 \pi$
- $3 + 3 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(3 y \cos{\left(x \right)} + 3 e^{y}\right)}_{P(x,y)}\,i+\underbrace{\left(3 x e^{y} + 3 \sin{\left(x \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=3 e^{y} + 3 \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =3 y \cos{\left(x \right)} + 3 e^{y}, \\ f_y(x,y) & =3 x e^{y} + 3 \sin{\left(x \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x e^{y} + 3 y \sin{\left(x \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t + \cos{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(\pi) & =\langle \pi,-1 + \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi,-1 + \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,-1 + \pi)-f(0,1) \\  & =\left(3 \left(\pi\right) e^{\left(-1 + \pi\right)}+3 \left(-1 + \pi\right) \sin{\left(\left(\pi\right) \right)}\right)-\left(3 \left(0\right) e^{\left(1\right)}+3 \left(1\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(3 \pi e^{-1 + \pi}+0\right)-\left(0\right) \\  & =3 \pi e^{-1 + \pi}.\end{aligned}
$$

## Original replay q-104747

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\sin{\left(y \right)} \cos{\left(x \right)}\right)\,i+\left(\sin{\left(x \right)} \cos{\left(y \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=e^{\sin{\left(x \right)}} + \cos{\left(x \right)}$ for $x\in [0,\frac{\pi}{2}].$

- $- \sin{\left(2 \right)} \sin{\left(1 - e \right)}$
- $- \sin{\left(2 \right)} + \sin{\left(e \right)}$
- $\sin{\left(e \right)}$
- $-1 + 2 \sin{\left(e \right)}$
- $- \sin{\left(e^{2} \right)} + \sin{\left(2 e \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\sin{\left(y \right)} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(\sin{\left(x \right)} \cos{\left(y \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=\cos{\left(x \right)} \cos{\left(y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\sin{\left(y \right)} \cos{\left(x \right)}, \\ f_y(x,y) & =\sin{\left(x \right)} \cos{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\sin{\left(x \right)} \sin{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,e^{\sin{\left(t \right)}} + \cos{\left(t \right)}\rangle,\,t\in [0,\frac{\pi}{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,2\rangle, \\ r(\frac{\pi}{2}) & =\langle \frac{\pi}{2},e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,2)$ and $(\frac{\pi}{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\frac{\pi}{2},e)-f(0,2) \\  & =\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)} \sin{\left(\left(e\right) \right)}\right)-\left(\sin{\left(\left(0\right) \right)} \sin{\left(\left(2\right) \right)}\right) \\  & =1\cdot \sin{\left(e \right)}-0\cdot \sin{\left(2 \right)} \\  & =\sin{\left(e \right)}.\end{aligned}
$$

## Generated observed-profile variant q-104747 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 \sin{\left(y \right)} \cos{\left(x \right)}\right)\,i+\left(2 \sin{\left(x \right)} \cos{\left(y \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=e^{\sin{\left(x \right)}} + \cos{\left(x \right)}$ for $x\in [0,\frac{\pi}{2}].$

- $- 2 \sin{\left(2 \right)} \sin{\left(1 - e \right)}$
- $- 2 \sin{\left(2 \right)} + 2 \sin{\left(e \right)}$
- $2 \sin{\left(e \right)}$
- $-2 + 4 \sin{\left(e \right)}$
- $- 2 \sin{\left(e^{2} \right)} + 2 \sin{\left(2 e \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 \sin{\left(y \right)} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(2 \sin{\left(x \right)} \cos{\left(y \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=2 \cos{\left(x \right)} \cos{\left(y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 \sin{\left(y \right)} \cos{\left(x \right)}, \\ f_y(x,y) & =2 \sin{\left(x \right)} \cos{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 \sin{\left(x \right)} \sin{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,e^{\sin{\left(t \right)}} + \cos{\left(t \right)}\rangle,\,t\in [0,\frac{\pi}{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,2\rangle, \\ r(\frac{\pi}{2}) & =\langle \frac{\pi}{2},e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,2)$ and $(\frac{\pi}{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\frac{\pi}{2},e)-f(0,2) \\  & =\left(2 \sin{\left(\left(\frac{\pi}{2}\right) \right)} \sin{\left(\left(e\right) \right)}\right)-\left(2 \sin{\left(\left(0\right) \right)} \sin{\left(\left(2\right) \right)}\right) \\  & =2\cdot 1\cdot \sin{\left(e \right)}-2\cdot 0\cdot \sin{\left(2 \right)} \\  & =2 \sin{\left(e \right)}.\end{aligned}
$$

## Generated observed-profile variant q-104747 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(3 \sin{\left(y \right)} \cos{\left(x \right)}\right)\,i+\left(3 \sin{\left(x \right)} \cos{\left(y \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=e^{\sin{\left(x \right)}} + \cos{\left(x \right)}$ for $x\in [0,\frac{\pi}{2}].$

- $- 3 \sin{\left(2 \right)} \sin{\left(1 - e \right)}$
- $- 3 \sin{\left(2 \right)} + 3 \sin{\left(e \right)}$
- $3 \sin{\left(e \right)}$
- $-3 + 6 \sin{\left(e \right)}$
- $- 3 \sin{\left(e^{2} \right)} + 3 \sin{\left(2 e \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(3 \sin{\left(y \right)} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(3 \sin{\left(x \right)} \cos{\left(y \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=3 \cos{\left(x \right)} \cos{\left(y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =3 \sin{\left(y \right)} \cos{\left(x \right)}, \\ f_y(x,y) & =3 \sin{\left(x \right)} \cos{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 \sin{\left(x \right)} \sin{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,e^{\sin{\left(t \right)}} + \cos{\left(t \right)}\rangle,\,t\in [0,\frac{\pi}{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,2\rangle, \\ r(\frac{\pi}{2}) & =\langle \frac{\pi}{2},e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,2)$ and $(\frac{\pi}{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\frac{\pi}{2},e)-f(0,2) \\  & =\left(3 \sin{\left(\left(\frac{\pi}{2}\right) \right)} \sin{\left(\left(e\right) \right)}\right)-\left(3 \sin{\left(\left(0\right) \right)} \sin{\left(\left(2\right) \right)}\right) \\  & =3\cdot 1\cdot \sin{\left(e \right)}-3\cdot 0\cdot \sin{\left(2 \right)} \\  & =3 \sin{\left(e \right)}.\end{aligned}
$$

## Original replay q-104761

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 x e^{- y}\right)\,i+\left(- x^{2} e^{- y} + 2 y\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\ln{\left(x - 1 \right)}$ for $x\in [2,3].$

- $1 - \ln{\left(2 \right)}$
- $\ln{\left(2 \right)}^{2} + \frac{1}{2}$
- $1 + \ln{\left(3 \right)}^{2}$
- $\frac{\ln{\left(2 \right)}^{2}}{3}$
- $\frac{1}{2} + \ln{\left(3 \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 x e^{- y}\right)}_{P(x,y)}\,i+\underbrace{\left(- x^{2} e^{- y} + 2 y\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 2 x e^{- y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 x e^{- y}, \\ f_y(x,y) & =- x^{2} e^{- y} + 2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} e^{- y} + y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,\ln{\left(t - 1 \right)}\rangle,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =\langle 2,0\rangle, \\ r(3) & =\langle 3,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\ln{\left(2 \right)})-f(2,0) \\  & =\left(\left(3\right)^{2} e^{- \left(\ln{\left(2 \right)}\right)}+\left(\ln{\left(2 \right)}\right)^{2}\right)-\left(\left(2\right)^{2} e^{- \left(0\right)}+\left(0\right)^{2}\right) \\  & =\frac{9}{2}+\ln{\left(2 \right)}^{2}-4 \\  & =\ln{\left(2 \right)}^{2} + \frac{1}{2}.\end{aligned}
$$

## Generated observed-profile variant q-104761 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(4 x e^{- y}\right)\,i+\left(- 2 x^{2} e^{- y} + 4 y\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\ln{\left(x - 1 \right)}$ for $x\in [2,3].$

- $2 - 2 \ln{\left(2 \right)}$
- $2 \ln{\left(2 \right)}^{2} + 1$
- $2 + 2 \ln{\left(3 \right)}^{2}$
- $\frac{2 \ln{\left(2 \right)}^{2}}{3}$
- $1 + 2 \ln{\left(3 \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(4 x e^{- y}\right)}_{P(x,y)}\,i+\underbrace{\left(- 2 x^{2} e^{- y} + 4 y\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 4 x e^{- y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =4 x e^{- y}, \\ f_y(x,y) & =- 2 x^{2} e^{- y} + 4 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x^{2} e^{- y} + 2 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,\ln{\left(t - 1 \right)}\rangle,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =\langle 2,0\rangle, \\ r(3) & =\langle 3,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\ln{\left(2 \right)})-f(2,0) \\  & =\left(2 \left(3\right)^{2} e^{- \left(\ln{\left(2 \right)}\right)}+2 \left(\ln{\left(2 \right)}\right)^{2}\right)-\left(2 \left(2\right)^{2} e^{- \left(0\right)}+2 \left(0\right)^{2}\right) \\  & =9+2 \ln{\left(2 \right)}^{2}-8 \\  & =2 \ln{\left(2 \right)}^{2} + 1.\end{aligned}
$$

## Generated observed-profile variant q-104761 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(6 x e^{- y}\right)\,i+\left(- 3 x^{2} e^{- y} + 6 y\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\ln{\left(x - 1 \right)}$ for $x\in [2,3].$

- $3 - 3 \ln{\left(2 \right)}$
- $3 \ln{\left(2 \right)}^{2} + \frac{3}{2}$
- $3 + 3 \ln{\left(3 \right)}^{2}$
- $\ln{\left(2 \right)}^{2}$
- $\frac{3}{2} + 3 \ln{\left(3 \right)}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(6 x e^{- y}\right)}_{P(x,y)}\,i+\underbrace{\left(- 3 x^{2} e^{- y} + 6 y\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 6 x e^{- y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =6 x e^{- y}, \\ f_y(x,y) & =- 3 x^{2} e^{- y} + 6 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x^{2} e^{- y} + 3 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,\ln{\left(t - 1 \right)}\rangle,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =\langle 2,0\rangle, \\ r(3) & =\langle 3,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\ln{\left(2 \right)})-f(2,0) \\  & =\left(3 \left(3\right)^{2} e^{- \left(\ln{\left(2 \right)}\right)}+3 \left(\ln{\left(2 \right)}\right)^{2}\right)-\left(3 \left(2\right)^{2} e^{- \left(0\right)}+3 \left(0\right)^{2}\right) \\  & =\frac{27}{2}+3 \ln{\left(2 \right)}^{2}-12 \\  & =3 \ln{\left(2 \right)}^{2} + \frac{3}{2}.\end{aligned}
$$

## Original replay q-104764

observed replay

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(6 x^{2} - y\right)\,i+\left(- x\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} - e^{\sqrt{x + 1}}$ for $x\in [0,3].$

- $-1 + 3 e^{2}$
- $3 e + 9$
- $e^{2} + 27$
- $-9 + 27 e$
- $3 e^{2} + 27$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(6 x^{2} - y\right)}_{P(x,y)}\,i+\underbrace{\left(- x\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=-1.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =6 x^{2} - y, \\ f_y(x,y) & =- x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x^{3} - x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} - e^{\sqrt{t + 1}}\rangle,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,- e\rangle, \\ r(3) & =\langle 3,9 - e^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,- e)$ and $(3,9 - e^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,9 - e^{2})-f(0,- e) \\  & =\left(2 \left(3\right)^{3}- \left(3\right) \left(9 - e^{2}\right)\right)-\left(2 \left(0\right)^{3}- \left(0\right) \left(- e\right)\right) \\  & =\left(54-27+3 e^{2}\right)-\left(0\right) \\  & =\left(27+3 e^{2}\right)-\left(0\right) \\  & =3 \left(e^{2} + 9\right).\end{aligned}
$$

## Generated observed-profile variant q-104764 scale 2

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(12 x^{2} - 2 y\right)\,i+\left(- 2 x\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} - e^{\sqrt{x + 1}}$ for $x\in [0,3].$

- $-2 + 6 e^{2}$
- $6 e + 18$
- $2 e^{2} + 54$
- $-18 + 54 e$
- $6 e^{2} + 54$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(12 x^{2} - 2 y\right)}_{P(x,y)}\,i+\underbrace{\left(- 2 x\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=-2.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =12 x^{2} - 2 y, \\ f_y(x,y) & =- 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=4 x^{3} - 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} - e^{\sqrt{t + 1}}\rangle,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,- e\rangle, \\ r(3) & =\langle 3,9 - e^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,- e)$ and $(3,9 - e^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,9 - e^{2})-f(0,- e) \\  & =\left(4 \left(3\right)^{3}- 2 \left(3\right) \left(9 - e^{2}\right)\right)-\left(4 \left(0\right)^{3}- 2 \left(0\right) \left(- e\right)\right) \\  & =\left(108-54+6 e^{2}\right)-\left(0\right) \\  & =\left(54+6 e^{2}\right)-\left(0\right) \\  & =6 \left(e^{2} + 9\right).\end{aligned}
$$

## Generated observed-profile variant q-104764 scale 3

homogeneous observed-bank extension

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(18 x^{2} - 3 y\right)\,i+\left(- 3 x\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} - e^{\sqrt{x + 1}}$ for $x\in [0,3].$

- $-3 + 9 e^{2}$
- $9 e + 27$
- $3 e^{2} + 81$
- $-27 + 81 e$
- $9 e^{2} + 81$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(18 x^{2} - 3 y\right)}_{P(x,y)}\,i+\underbrace{\left(- 3 x\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=-3.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =18 x^{2} - 3 y, \\ f_y(x,y) & =- 3 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=6 x^{3} - 3 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} - e^{\sqrt{t + 1}}\rangle,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,- e\rangle, \\ r(3) & =\langle 3,9 - e^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,- e)$ and $(3,9 - e^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,9 - e^{2})-f(0,- e) \\  & =\left(6 \left(3\right)^{3}- 3 \left(3\right) \left(9 - e^{2}\right)\right)-\left(6 \left(0\right)^{3}- 3 \left(0\right) \left(- e\right)\right) \\  & =\left(162-81+9 e^{2}\right)-\left(0\right) \\  & =\left(81+9 e^{2}\right)-\left(0\right) \\  & =9 \left(e^{2} + 9\right).\end{aligned}
$$

## Original replay q-104732

observed replay

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle \sin{\left(\pi t \right)},\frac{\pi t}{2}\rangle,\,t\in [0,\frac{1}{2}].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x \cos{\left(y \right)} + y\right)\,i+\left(- x^{2} \sin{\left(y \right)} + x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $\frac{\sqrt{2}}{2} + \frac{\pi}{4}$
- $- \frac{\pi}{2} + \sqrt{2}$
- $\frac{\sqrt{2}}{2}$
- $0$
- $\frac{\sqrt{2}}{2} + 1$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x \cos{\left(y \right)} + y, \\ f_y(x,y) & =- x^{2} \sin{\left(y \right)} + x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} \cos{\left(y \right)} + x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\frac{1}{2}) & =\langle 1,\frac{\pi}{4}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\frac{\pi}{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\frac{\pi}{4})-f(0,0) \\  & =\left(\left(1\right)^{2} \cos{\left(\left(\frac{\pi}{4}\right) \right)}+\left(1\right) \left(\frac{\pi}{4}\right)\right)-\left(\left(0\right)^{2} \cos{\left(\left(0\right) \right)}+\left(0\right) \left(0\right)\right) \\  & =\frac{\sqrt{2}}{2}+\frac{\pi}{4} \\  & =\frac{2 \sqrt{2} + \pi}{4}.\end{aligned}
$$

## Generated observed-profile variant q-104732 scale 2

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle \sin{\left(\pi t \right)},\frac{\pi t}{2}\rangle,\,t\in [0,\frac{1}{2}].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(4 x \cos{\left(y \right)} + 2 y\right)\,i+\left(- 2 x^{2} \sin{\left(y \right)} + 2 x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $\sqrt{2} + \frac{\pi}{2}$
- $- \pi + 2 \sqrt{2}$
- $\sqrt{2}$
- $0$
- $\sqrt{2} + 2$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =4 x \cos{\left(y \right)} + 2 y, \\ f_y(x,y) & =- 2 x^{2} \sin{\left(y \right)} + 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=2 x^{2} \cos{\left(y \right)} + 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\frac{1}{2}) & =\langle 1,\frac{\pi}{4}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\frac{\pi}{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\frac{\pi}{4})-f(0,0) \\  & =\left(2 \left(1\right)^{2} \cos{\left(\left(\frac{\pi}{4}\right) \right)}+2 \left(1\right) \left(\frac{\pi}{4}\right)\right)-\left(2 \left(0\right)^{2} \cos{\left(\left(0\right) \right)}+2 \left(0\right) \left(0\right)\right) \\  & =\sqrt{2}+\frac{\pi}{2} \\  & =\frac{2 \sqrt{2} + \pi}{2}.\end{aligned}
$$

## Generated observed-profile variant q-104732 scale 3

homogeneous observed-bank extension

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle \sin{\left(\pi t \right)},\frac{\pi t}{2}\rangle,\,t\in [0,\frac{1}{2}].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(6 x \cos{\left(y \right)} + 3 y\right)\,i+\left(- 3 x^{2} \sin{\left(y \right)} + 3 x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $\frac{3 \sqrt{2}}{2} + \frac{3 \pi}{4}$
- $- \frac{3 \pi}{2} + 3 \sqrt{2}$
- $\frac{3 \sqrt{2}}{2}$
- $0$
- $\frac{3 \sqrt{2}}{2} + 3$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =6 x \cos{\left(y \right)} + 3 y, \\ f_y(x,y) & =- 3 x^{2} \sin{\left(y \right)} + 3 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x^{2} \cos{\left(y \right)} + 3 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\frac{1}{2}) & =\langle 1,\frac{\pi}{4}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\frac{\pi}{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\frac{\pi}{4})-f(0,0) \\  & =\left(3 \left(1\right)^{2} \cos{\left(\left(\frac{\pi}{4}\right) \right)}+3 \left(1\right) \left(\frac{\pi}{4}\right)\right)-\left(3 \left(0\right)^{2} \cos{\left(\left(0\right) \right)}+3 \left(0\right) \left(0\right)\right) \\  & =\frac{3 \sqrt{2}}{2}+\frac{3 \pi}{4} \\  & =\frac{3 \left(2 \sqrt{2} + \pi\right)}{4}.\end{aligned}
$$

## Authored variant easy_product 0

authored missing easy level

Consider the curve $C$, defined parametrically as

$$
r(t)=\langle t + 1,2 t - 2\rangle,\,t\in [0,1].
$$

Evaluate $\int_C F\cdot\mathrm{d}r$ for $F(x,y)=\left(y\right)\,i+\left(x\right)\,j.$

*Hint: You may wish to use the fact that $F$ is conservative.*

- $2$
- $-2$
- $4$
- $1$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=\nabla f.$ Since $F$ is conservative, we must have

$$
\begin{aligned}f_x(x,y) & =y, \\ f_y(x,y) & =x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $\nabla f=F.$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 1,-2\rangle, \\ r(1) & =\langle 2,0\rangle.\end{aligned}
$$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,0)-f(1,-2) \\  & =\left(\left(2\right) \left(0\right)\right)-\left(\left(1\right) \left(-2\right)\right) \\  & =2 \\  & =2.\end{aligned}
$$

## Authored variant easy_product 1

authored missing easy level

Consider the curve $C$, defined parametrically as

$$
r(t)=\langle t + 2,2 t - 2\rangle,\,t\in [0,1].
$$

Evaluate $\int_C F\cdot\mathrm{d}r$ for $F(x,y)=\left(- 2 y\right)\,i+\left(- 2 x\right)\,j.$

*Hint: You may wish to use the fact that $F$ is conservative.*

- $-8$
- $8$
- $-16$
- $-4$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=\nabla f.$ Since $F$ is conservative, we must have

$$
\begin{aligned}f_x(x,y) & =- 2 y, \\ f_y(x,y) & =- 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $\nabla f=F.$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 2,-2\rangle, \\ r(1) & =\langle 3,0\rangle.\end{aligned}
$$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,0)-f(2,-2) \\  & =\left(- 2 \left(3\right) \left(0\right)\right)-\left(- 2 \left(2\right) \left(-2\right)\right) \\  & =-8 \\  & =-8.\end{aligned}
$$

## Authored variant easy_separable 0

authored missing easy level

Consider the curve $C$, defined parametrically as

$$
r(t)=\langle t - 2,2 t\rangle,\,t\in [0,1].
$$

Evaluate $\int_C F\cdot\mathrm{d}r$ for $F(x,y)=\left(2 x\right)\,i+\left(2 y\right)\,j.$

*Hint: You may wish to use the fact that $F$ is conservative.*

- $1$
- $-1$
- $2$
- $\frac{1}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=\nabla f.$ Since $F$ is conservative, we must have

$$
\begin{aligned}f_x(x,y) & =2 x, \\ f_y(x,y) & =2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} + y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $\nabla f=F.$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle -2,0\rangle, \\ r(1) & =\langle -1,2\rangle.\end{aligned}
$$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(-1,2)-f(-2,0) \\  & =\left(\left(-1\right)^{2}+\left(2\right)^{2}\right)-\left(\left(-2\right)^{2}+\left(0\right)^{2}\right) \\  & =1+4-4 \\  & =1.\end{aligned}
$$

## Authored variant easy_separable 1

authored missing easy level

Consider the curve $C$, defined parametrically as

$$
r(t)=\langle t + 1,t + 1\rangle,\,t\in [0,1].
$$

Evaluate $\int_C F\cdot\mathrm{d}r$ for $F(x,y)=\left(2 x\right)\,i+\left(2 y\right)\,j.$

*Hint: You may wish to use the fact that $F$ is conservative.*

- $6$
- $-6$
- $12$
- $3$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=\nabla f.$ Since $F$ is conservative, we must have

$$
\begin{aligned}f_x(x,y) & =2 x, \\ f_y(x,y) & =2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} + y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $\nabla f=F.$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 1,1\rangle, \\ r(1) & =\langle 2,2\rangle.\end{aligned}
$$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,2)-f(1,1) \\  & =\left(\left(2\right)^{2}+\left(2\right)^{2}\right)-\left(\left(1\right)^{2}+\left(1\right)^{2}\right) \\  & =4+4-1-1 \\  & =6.\end{aligned}
$$

## Authored variant quartic_trig 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t + \sin{\left(\frac{\pi t}{2} \right)},t + \cos{\left(\frac{\pi t}{2} \right)}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(x y^{2}\right)\,i+\left(x^{2} y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $\frac{9}{2}$
- $- \frac{9}{2}$
- $9$
- $\frac{9}{4}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =x y^{2}, \\ f_y(x,y) & =x^{2} y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{x^{2} y^{2}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 3,1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(3,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,1)-f(0,1) \\  & =\frac{\left(3\right)^{2} \left(1\right)^{2}}{2}-\frac{\left(0\right)^{2} \left(1\right)^{2}}{2} \\  & =\frac{9}{2}-\left(0\right) \\  & =\frac{9}{2}.\end{aligned}
$$

## Authored variant quartic_trig 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 3 t + \sin{\left(\frac{\pi t}{2} \right)},t + \cos{\left(\frac{\pi t}{2} \right)}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(- 2 x y^{2}\right)\,i+\left(- 2 x^{2} y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $-16$
- $16$
- $-32$
- $-8$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =- 2 x y^{2}, \\ f_y(x,y) & =- 2 x^{2} y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- x^{2} y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 4,1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(4,1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(4,1)-f(0,1) \\  & =- \left(4\right)^{2} \left(1\right)^{2}-\left(- \left(0\right)^{2} \left(1\right)^{2}\right) \\  & =-16-\left(0\right) \\  & =-16.\end{aligned}
$$

## Authored variant cubic_exponential 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t,e^{t}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(3 x^{2} y^{3} + 2 x\right)\,i+\left(3 x^{3} y^{2} - 2 y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- e^{2} + 5 + 8 e^{3}$
- $- 8 e^{3} - 5 + e^{2}$
- $- 2 e^{2} + 10 + 16 e^{3}$
- $- \frac{e^{2}}{2} + \frac{5}{2} + 4 e^{3}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =3 x^{2} y^{3} + 2 x, \\ f_y(x,y) & =3 x^{3} y^{2} - 2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{3} y^{3} + x^{2} - y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 2,e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,e)-f(0,1) \\  & =\left(\left(2\right)^{3} \left(e\right)^{3}+\left(2\right)^{2}- \left(e\right)^{2}\right)-\left(\left(0\right)^{3} \left(1\right)^{3}+\left(0\right)^{2}- \left(1\right)^{2}\right) \\  & =8 e^{3}+4- e^{2}+1 \\  & =- e^{2} + 5 + 8 e^{3}.\end{aligned}
$$

## Authored variant cubic_exponential 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 t,e^{t}\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(- 6 x^{2} y^{3} + 4 x\right)\,i+\left(- 6 x^{3} y^{2} - 2 y\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 16 e^{3} - e^{2} + 9$
- $-9 + e^{2} + 16 e^{3}$
- $- 32 e^{3} - 2 e^{2} + 18$
- $- 8 e^{3} - \frac{e^{2}}{2} + \frac{9}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =- 6 x^{2} y^{3} + 4 x, \\ f_y(x,y) & =- 6 x^{3} y^{2} - 2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x^{3} y^{3} + 2 x^{2} - y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(1) & =\langle 2,e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,e)-f(0,1) \\  & =\left(- 2 \left(2\right)^{3} \left(e\right)^{3}+2 \left(2\right)^{2}- \left(e\right)^{2}\right)-\left(- 2 \left(0\right)^{3} \left(1\right)^{3}+2 \left(0\right)^{2}- \left(1\right)^{2}\right) \\  & =- 16 e^{3}+8- e^{2}+1 \\  & =- 16 e^{3} - e^{2} + 9.\end{aligned}
$$

## Authored variant exponential_cosine 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t^{2} + 2,t\rangle,\,t\in [0,\pi].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(e^{x} \cos{\left(y \right)}\right)\,i+\left(- e^{x} \sin{\left(y \right)}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- e^{2 + \pi^{2}} - e^{2}$
- $e^{2} + e^{2 + \pi^{2}}$
- $- 2 e^{2 + \pi^{2}} - 2 e^{2}$
- $- \frac{e^{2 + \pi^{2}}}{2} - \frac{e^{2}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =e^{x} \cos{\left(y \right)}, \\ f_y(x,y) & =- e^{x} \sin{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=e^{x} \cos{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 2,0\rangle, \\ r(\pi) & =\langle 2 + \pi^{2},\pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(2 + \pi^{2},\pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2 + \pi^{2},\pi)-f(2,0) \\  & =e^{\left(2 + \pi^{2}\right)} \cos{\left(\left(\pi\right) \right)}-e^{\left(2\right)} \cos{\left(\left(0\right) \right)} \\  & =- e^{2 + \pi^{2}}-\left(e^{2}\right) \\  & =\left(- e^{\pi^{2}} - 1\right) e^{2}.\end{aligned}
$$

## Authored variant exponential_cosine 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t^{2} + 3,t\rangle,\,t\in [0,\pi].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(- 2 e^{x} \cos{\left(y \right)}\right)\,i+\left(2 e^{x} \sin{\left(y \right)}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $2 e^{3} + 2 e^{3 + \pi^{2}}$
- $- 2 e^{3 + \pi^{2}} - 2 e^{3}$
- $4 e^{3} + 4 e^{3 + \pi^{2}}$
- $e^{3} + e^{3 + \pi^{2}}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =- 2 e^{x} \cos{\left(y \right)}, \\ f_y(x,y) & =2 e^{x} \sin{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 e^{x} \cos{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 3,0\rangle, \\ r(\pi) & =\langle 3 + \pi^{2},\pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(3,0)$ and $(3 + \pi^{2},\pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3 + \pi^{2},\pi)-f(3,0) \\  & =- 2 e^{\left(3 + \pi^{2}\right)} \cos{\left(\left(\pi\right) \right)}-\left(- 2 e^{\left(3\right)} \cos{\left(\left(0\right) \right)}\right) \\  & =2 e^{3 + \pi^{2}}-\left(- 2 e^{3}\right) \\  & =- 2 \left(- e^{\pi^{2}} - 1\right) e^{3}.\end{aligned}
$$

## Authored variant cubic_product 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t,t^{2} - 2\rangle,\,t\in [0,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x y - y\right)\,i+\left(x^{2} - x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $4$
- $-4$
- $8$
- $2$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x y - y, \\ f_y(x,y) & =x^{2} - x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} y - x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,-2\rangle, \\ r(2) & =\langle 2,2\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-2)$ and $(2,2).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2,2)-f(0,-2) \\  & =\left(\left(2\right)^{2} \left(2\right)- \left(2\right) \left(2\right)\right)-\left(\left(0\right)^{2} \left(-2\right)- \left(0\right) \left(-2\right)\right) \\  & =8-4 \\  & =4.\end{aligned}
$$

## Authored variant cubic_product 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle t,t^{2} - 2\rangle,\,t\in [0,1].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(- 4 x y - 2 y\right)\,i+\left(- 2 x^{2} - 2 x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $4$
- $-4$
- $8$
- $2$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =- 4 x y - 2 y, \\ f_y(x,y) & =- 2 x^{2} - 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x^{2} y - 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,-2\rangle, \\ r(1) & =\langle 1,-1\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-2)$ and $(1,-1).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,-1)-f(0,-2) \\  & =\left(- 2 \left(1\right)^{2} \left(-1\right)- 2 \left(1\right) \left(-1\right)\right)-\left(- 2 \left(0\right)^{2} \left(-2\right)- 2 \left(0\right) \left(-2\right)\right) \\  & =2+2 \\  & =4.\end{aligned}
$$

## Authored variant separable_cubic 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 \ln{\left(t \right)},t^{2}\rangle,\,t\in [1,3].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(x^{2} - y\right)\,i+\left(- x + y^{2}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 18 \ln{\left(3 \right)} + \frac{8 \ln{\left(3 \right)}^{3}}{3} + \frac{728}{3}$
- $- \frac{728}{3} - \frac{8 \ln{\left(3 \right)}^{3}}{3} + 18 \ln{\left(3 \right)}$
- $- 36 \ln{\left(3 \right)} + \frac{16 \ln{\left(3 \right)}^{3}}{3} + \frac{1456}{3}$
- $- 9 \ln{\left(3 \right)} + \frac{4 \ln{\left(3 \right)}^{3}}{3} + \frac{364}{3}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =x^{2} - y, \\ f_y(x,y) & =- x + y^{2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{x^{3}}{3} - x y + \frac{y^{3}}{3}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =\langle 0,1\rangle, \\ r(3) & =\langle 2 \ln{\left(3 \right)},9\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2 \ln{\left(3 \right)},9).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2 \ln{\left(3 \right)},9)-f(0,1) \\  & =\left(\frac{\left(2 \ln{\left(3 \right)}\right)^{3}}{3}+\frac{\left(9\right)^{3}}{3}- \left(2 \ln{\left(3 \right)}\right) \left(9\right)\right)-\left(\frac{\left(0\right)^{3}}{3}+\frac{\left(1\right)^{3}}{3}- \left(0\right) \left(1\right)\right) \\  & =\frac{8 \ln{\left(3 \right)}^{3}}{3}+243- 18 \ln{\left(3 \right)}- \frac{1}{3} \\  & =- 18 \ln{\left(3 \right)} + \frac{8 \ln{\left(3 \right)}^{3}}{3} + \frac{728}{3}.\end{aligned}
$$

## Authored variant separable_cubic 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 2 \ln{\left(t \right)},t^{2}\rangle,\,t\in [1,2].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(- 2 x^{2} - y\right)\,i+\left(- x + 2 y^{2}\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- 8 \ln{\left(2 \right)} - \frac{16 \ln{\left(2 \right)}^{3}}{3} + 42$
- $-42 + \frac{16 \ln{\left(2 \right)}^{3}}{3} + 8 \ln{\left(2 \right)}$
- $- 16 \ln{\left(2 \right)} - \frac{32 \ln{\left(2 \right)}^{3}}{3} + 84$
- $- 4 \ln{\left(2 \right)} - \frac{8 \ln{\left(2 \right)}^{3}}{3} + 21$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =- 2 x^{2} - y, \\ f_y(x,y) & =- x + 2 y^{2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- \frac{2 x^{3}}{3} - x y + \frac{2 y^{3}}{3}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(1) & =\langle 0,1\rangle, \\ r(2) & =\langle 2 \ln{\left(2 \right)},4\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2 \ln{\left(2 \right)},4).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(2 \ln{\left(2 \right)},4)-f(0,1) \\  & =\left(- \frac{2 \left(2 \ln{\left(2 \right)}\right)^{3}}{3}+\frac{2 \left(4\right)^{3}}{3}- \left(2 \ln{\left(2 \right)}\right) \left(4\right)\right)-\left(- \frac{2 \left(0\right)^{3}}{3}+\frac{2 \left(1\right)^{3}}{3}- \left(0\right) \left(1\right)\right) \\  & =- \frac{16 \ln{\left(2 \right)}^{3}}{3}+\frac{128}{3}- 8 \ln{\left(2 \right)}- \frac{2}{3} \\  & =- 8 \ln{\left(2 \right)} - \frac{16 \ln{\left(2 \right)}^{3}}{3} + 42.\end{aligned}
$$

## Authored variant cosine_product 0

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle 3 \sin{\left(\pi t \right)},\frac{\pi t}{2}\rangle,\,t\in [0,\frac{1}{2}].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(2 x \cos{\left(y \right)} - y\right)\,i+\left(- x^{2} \sin{\left(y \right)} - x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $- \frac{3 \pi}{4} + \frac{9 \sqrt{2}}{2}$
- $- \frac{9 \sqrt{2}}{2} + \frac{3 \pi}{4}$
- $- \frac{3 \pi}{2} + 9 \sqrt{2}$
- $- \frac{3 \pi}{8} + \frac{9 \sqrt{2}}{4}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =2 x \cos{\left(y \right)} - y, \\ f_y(x,y) & =- x^{2} \sin{\left(y \right)} - x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} \cos{\left(y \right)} - x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\frac{1}{2}) & =\langle 3,\frac{\pi}{4}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(3,\frac{\pi}{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\frac{\pi}{4})-f(0,0) \\  & =\left(\left(3\right)^{2} \cos{\left(\left(\frac{\pi}{4}\right) \right)}- \left(3\right) \left(\frac{\pi}{4}\right)\right)-\left(\left(0\right)^{2} \cos{\left(\left(0\right) \right)}- \left(0\right) \left(0\right)\right) \\  & =\frac{9 \sqrt{2}}{2}- \frac{3 \pi}{4} \\  & =\frac{3 \left(- \pi + 6 \sqrt{2}\right)}{4}.\end{aligned}
$$

## Authored variant cosine_product 1

authored bank/parameter variation

Consider the curve $C,$ defined parametrically as

$$
r(t)=\langle \sin{\left(\pi t \right)},\frac{\pi t}{2}\rangle,\,t\in [0,\frac{1}{2}].
$$

Evaluate ${\int }_{C}F\cdot \text{d}r$ for $F(x,y)=\left(6 x \cos{\left(y \right)} + y\right)\,i+\left(- 3 x^{2} \sin{\left(y \right)} + x\right)\,j.$ 

*Hint: You may wish to use the fact that $F$ is conservative.*

- $\frac{\pi}{4} + \frac{3 \sqrt{2}}{2}$
- $- \frac{3 \sqrt{2}}{2} - \frac{\pi}{4}$
- $\frac{\pi}{2} + 3 \sqrt{2}$
- $\frac{\pi}{8} + \frac{3 \sqrt{2}}{4}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=∇f.$ Since we're given that $F$ is conservative, we know that such a function exists. Therefore, we must have

$$
\begin{aligned}f_x(x,y) & =6 x \cos{\left(y \right)} + y, \\ f_y(x,y) & =- 3 x^{2} \sin{\left(y \right)} + x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=3 x^{2} \cos{\left(y \right)} + x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\frac{1}{2}) & =\langle 1,\frac{\pi}{4}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\frac{\pi}{4}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\frac{\pi}{4})-f(0,0) \\  & =\left(3 \left(1\right)^{2} \cos{\left(\left(\frac{\pi}{4}\right) \right)}+\left(1\right) \left(\frac{\pi}{4}\right)\right)-\left(3 \left(0\right)^{2} \cos{\left(\left(0\right) \right)}+\left(0\right) \left(0\right)\right) \\  & =\frac{3 \sqrt{2}}{2}+\frac{\pi}{4} \\  & =\frac{\pi + 6 \sqrt{2}}{4}.\end{aligned}
$$

## Authored variant radial_log 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\frac{x}{x^{2} + y^{2} + 2}\right)\,i+\left(\frac{y}{x^{2} + y^{2} + 2}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} \ln{\left(x + 1 \right)}$ for $x\in [0,1].$

- $- \frac{\ln{\left(2 \right)}}{2} + \frac{\ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}}{2}$
- $- \frac{\ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}}{2} + \frac{\ln{\left(2 \right)}}{2}$
- $- \ln{\left(2 \right)} + \ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}$
- $- \frac{\ln{\left(2 \right)}}{4} + \frac{\ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}}{4}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\frac{x}{x^{2} + y^{2} + 2}\right)}_{P(x,y)}\,i+\underbrace{\left(\frac{y}{x^{2} + y^{2} + 2}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- \frac{2 x y}{\left(x^{2} + y^{2} + 2\right)^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\frac{x}{x^{2} + y^{2} + 2}, \\ f_y(x,y) & =\frac{y}{x^{2} + y^{2} + 2}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\frac{\ln{\left(x^{2} + y^{2} + 2 \right)}}{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} \ln{\left(t + 1 \right)}\rangle,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(1) & =\langle 1,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\ln{\left(2 \right)})-f(0,0) \\  & =\frac{\ln{\left(\left(1\right)^{2} + \left(\ln{\left(2 \right)}\right)^{2} + 2 \right)}}{2}-\frac{\ln{\left(\left(0\right)^{2} + \left(0\right)^{2} + 2 \right)}}{2} \\  & =\frac{\ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}}{2}-\left(\frac{\ln{\left(2 \right)}}{2}\right) \\  & =- \frac{\ln{\left(2 \right)}}{2} + \frac{\ln{\left(\ln{\left(2 \right)}^{2} + 3 \right)}}{2}.\end{aligned}
$$

## Authored variant radial_log 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(- \frac{2 x}{x^{2} + y^{2} + 3}\right)\,i+\left(- \frac{2 y}{x^{2} + y^{2} + 3}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} \ln{\left(x + 1 \right)}$ for $x\in [0,1].$

- $- \ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)} + \ln{\left(3 \right)}$
- $- \ln{\left(3 \right)} + \ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)}$
- $- 2 \ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)} + 2 \ln{\left(3 \right)}$
- $- \frac{\ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)}}{2} + \frac{\ln{\left(3 \right)}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(- \frac{2 x}{x^{2} + y^{2} + 3}\right)}_{P(x,y)}\,i+\underbrace{\left(- \frac{2 y}{x^{2} + y^{2} + 3}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=\frac{4 x y}{\left(x^{2} + y^{2} + 3\right)^{2}}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =- \frac{2 x}{x^{2} + y^{2} + 3}, \\ f_y(x,y) & =- \frac{2 y}{x^{2} + y^{2} + 3}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- \ln{\left(x^{2} + y^{2} + 3 \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} \ln{\left(t + 1 \right)}\rangle,\,t\in [0,1].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(1) & =\langle 1,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(1,\ln{\left(2 \right)})-f(0,0) \\  & =- \ln{\left(\left(1\right)^{2} + \left(\ln{\left(2 \right)}\right)^{2} + 3 \right)}-\left(- \ln{\left(\left(0\right)^{2} + \left(0\right)^{2} + 3 \right)}\right) \\  & =- \ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)}-\left(- \ln{\left(3 \right)}\right) \\  & =- \ln{\left(\ln{\left(2 \right)}^{2} + 4 \right)} + \ln{\left(3 \right)}.\end{aligned}
$$

## Authored variant sine_exponential 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(y^{2} \cos{\left(x \right)}\right)\,i+\left(2 y \sin{\left(x \right)} + e^{y}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} + \sin^{2}{\left(x \right)}$ for $x\in [0,\pi].$

- $-1 + e^{\pi^{2}}$
- $1 - e^{\pi^{2}}$
- $-2 + 2 e^{\pi^{2}}$
- $- \frac{1}{2} + \frac{e^{\pi^{2}}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(y^{2} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(2 y \sin{\left(x \right)} + e^{y}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=2 y \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =y^{2} \cos{\left(x \right)}, \\ f_y(x,y) & =2 y \sin{\left(x \right)} + e^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=y^{2} \sin{\left(x \right)} + e^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} + \sin^{2}{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\pi) & =\langle \pi,\pi^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,\pi^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,\pi^{2})-f(0,0) \\  & =\left(\left(\left(\pi^{2}\right)\right)^{2} \sin{\left(\left(\pi\right) \right)}+e^{\left(\pi^{2}\right)}\right)-\left(\left(0\right)^{2} \sin{\left(\left(0\right) \right)}+e^{\left(0\right)}\right) \\  & =\left(0+e^{\pi^{2}}\right)-\left(0+1\right) \\  & =-1 + e^{\pi^{2}}.\end{aligned}
$$

## Authored variant sine_exponential 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(- 2 y^{2} \cos{\left(x \right)}\right)\,i+\left(- 4 y \sin{\left(x \right)} + 2 e^{y}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} + \sin^{2}{\left(x \right)}$ for $x\in [0,\pi].$

- $-2 + 2 e^{\pi^{2}}$
- $2 - 2 e^{\pi^{2}}$
- $-4 + 4 e^{\pi^{2}}$
- $-1 + e^{\pi^{2}}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(- 2 y^{2} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(- 4 y \sin{\left(x \right)} + 2 e^{y}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 4 y \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =- 2 y^{2} \cos{\left(x \right)}, \\ f_y(x,y) & =- 4 y \sin{\left(x \right)} + 2 e^{y}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 y^{2} \sin{\left(x \right)} + 2 e^{y}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} + \sin^{2}{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,0\rangle, \\ r(\pi) & =\langle \pi,\pi^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,\pi^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,\pi^{2})-f(0,0) \\  & =\left(- 2 \left(\left(\pi^{2}\right)\right)^{2} \sin{\left(\left(\pi\right) \right)}+2 e^{\left(\pi^{2}\right)}\right)-\left(- 2 \left(0\right)^{2} \sin{\left(\left(0\right) \right)}+2 e^{\left(0\right)}\right) \\  & =\left(0+2 e^{\pi^{2}}\right)-\left(0+2\right) \\  & =-2 + 2 e^{\pi^{2}}.\end{aligned}
$$

## Authored variant mixed_exponential 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(y \cos{\left(x \right)} + e^{y}\right)\,i+\left(x e^{y} + \sin{\left(x \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x + \cos{\left(x \right)}$ for $x\in [0,\pi].$

- $\pi e^{-1 + \pi}$
- $- \pi e^{-1 + \pi}$
- $2 \pi e^{-1 + \pi}$
- $\frac{\pi e^{-1 + \pi}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(y \cos{\left(x \right)} + e^{y}\right)}_{P(x,y)}\,i+\underbrace{\left(x e^{y} + \sin{\left(x \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=e^{y} + \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =y \cos{\left(x \right)} + e^{y}, \\ f_y(x,y) & =x e^{y} + \sin{\left(x \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x e^{y} + y \sin{\left(x \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t + \cos{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(\pi) & =\langle \pi,-1 + \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi,-1 + \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,-1 + \pi)-f(0,1) \\  & =\left(\left(\pi\right) e^{\left(-1 + \pi\right)}+\left(-1 + \pi\right) \sin{\left(\left(\pi\right) \right)}\right)-\left(\left(0\right) e^{\left(1\right)}+\left(1\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(\pi e^{-1 + \pi}+0\right)-\left(0\right) \\  & =\pi e^{-1 + \pi}.\end{aligned}
$$

## Authored variant mixed_exponential 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 y \cos{\left(x \right)} - 2 e^{y}\right)\,i+\left(- 2 x e^{y} + 2 \sin{\left(x \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x + \cos{\left(x \right)}$ for $x\in [0,\pi].$

- $- 2 \pi e^{-1 + \pi}$
- $2 \pi e^{-1 + \pi}$
- $- 4 \pi e^{-1 + \pi}$
- $- \pi e^{-1 + \pi}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 y \cos{\left(x \right)} - 2 e^{y}\right)}_{P(x,y)}\,i+\underbrace{\left(- 2 x e^{y} + 2 \sin{\left(x \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 2 e^{y} + 2 \cos{\left(x \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 y \cos{\left(x \right)} - 2 e^{y}, \\ f_y(x,y) & =- 2 x e^{y} + 2 \sin{\left(x \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x e^{y} + 2 y \sin{\left(x \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t + \cos{\left(t \right)}\rangle,\,t\in [0,\pi].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,1\rangle, \\ r(\pi) & =\langle \pi,-1 + \pi\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(\pi,-1 + \pi).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\pi,-1 + \pi)-f(0,1) \\  & =\left(- 2 \left(\pi\right) e^{\left(-1 + \pi\right)}+2 \left(-1 + \pi\right) \sin{\left(\left(\pi\right) \right)}\right)-\left(- 2 \left(0\right) e^{\left(1\right)}+2 \left(1\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(- 2 \pi e^{-1 + \pi}+0\right)-\left(0\right) \\  & =- 2 \pi e^{-1 + \pi}.\end{aligned}
$$

## Authored variant sine_product 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(\sin{\left(y \right)} \cos{\left(x \right)}\right)\,i+\left(\sin{\left(x \right)} \cos{\left(y \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=e^{\sin{\left(x \right)}} + 2 \cos{\left(x \right)}$ for $x\in [0,\frac{\pi}{2}].$

- $\sin{\left(e \right)}$
- $- \sin{\left(e \right)}$
- $2 \sin{\left(e \right)}$
- $\frac{\sin{\left(e \right)}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(\sin{\left(y \right)} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(\sin{\left(x \right)} \cos{\left(y \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=\cos{\left(x \right)} \cos{\left(y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =\sin{\left(y \right)} \cos{\left(x \right)}, \\ f_y(x,y) & =\sin{\left(x \right)} \cos{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=\sin{\left(x \right)} \sin{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,e^{\sin{\left(t \right)}} + 2 \cos{\left(t \right)}\rangle,\,t\in [0,\frac{\pi}{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,3\rangle, \\ r(\frac{\pi}{2}) & =\langle \frac{\pi}{2},e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,3)$ and $(\frac{\pi}{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\frac{\pi}{2},e)-f(0,3) \\  & =\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)} \sin{\left(\left(e\right) \right)}\right)-\left(\sin{\left(\left(0\right) \right)} \sin{\left(\left(3\right) \right)}\right) \\  & =1\cdot \sin{\left(e \right)}-0\cdot \sin{\left(3 \right)} \\  & =\sin{\left(e \right)}.\end{aligned}
$$

## Authored variant sine_product 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(- 2 \sin{\left(y \right)} \cos{\left(x \right)}\right)\,i+\left(- 2 \sin{\left(x \right)} \cos{\left(y \right)}\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=e^{\sin{\left(x \right)}} + 3 \cos{\left(x \right)}$ for $x\in [0,\frac{\pi}{2}].$

- $- 2 \sin{\left(e \right)}$
- $2 \sin{\left(e \right)}$
- $- 4 \sin{\left(e \right)}$
- $- \sin{\left(e \right)}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(- 2 \sin{\left(y \right)} \cos{\left(x \right)}\right)}_{P(x,y)}\,i+\underbrace{\left(- 2 \sin{\left(x \right)} \cos{\left(y \right)}\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 2 \cos{\left(x \right)} \cos{\left(y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =- 2 \sin{\left(y \right)} \cos{\left(x \right)}, \\ f_y(x,y) & =- 2 \sin{\left(x \right)} \cos{\left(y \right)}.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 \sin{\left(x \right)} \sin{\left(y \right)}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,e^{\sin{\left(t \right)}} + 3 \cos{\left(t \right)}\rangle,\,t\in [0,\frac{\pi}{2}].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,4\rangle, \\ r(\frac{\pi}{2}) & =\langle \frac{\pi}{2},e\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,4)$ and $(\frac{\pi}{2},e).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(\frac{\pi}{2},e)-f(0,4) \\  & =\left(- 2 \sin{\left(\left(\frac{\pi}{2}\right) \right)} \sin{\left(\left(e\right) \right)}\right)-\left(- 2 \sin{\left(\left(0\right) \right)} \sin{\left(\left(4\right) \right)}\right) \\  & =-2\cdot 1\cdot \sin{\left(e \right)}--2\cdot 0\cdot \sin{\left(4 \right)} \\  & =- 2 \sin{\left(e \right)}.\end{aligned}
$$

## Authored variant negative_exponential 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(2 x e^{- y}\right)\,i+\left(- x^{2} e^{- y} + 2 y\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\ln{\left(x - 1 \right)}$ for $x\in [2,3].$

- $\ln{\left(2 \right)}^{2} + \frac{1}{2}$
- $- \frac{1}{2} - \ln{\left(2 \right)}^{2}$
- $2 \ln{\left(2 \right)}^{2} + 1$
- $\frac{\ln{\left(2 \right)}^{2}}{2} + \frac{1}{4}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(2 x e^{- y}\right)}_{P(x,y)}\,i+\underbrace{\left(- x^{2} e^{- y} + 2 y\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=- 2 x e^{- y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =2 x e^{- y}, \\ f_y(x,y) & =- x^{2} e^{- y} + 2 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{2} e^{- y} + y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,\ln{\left(t - 1 \right)}\rangle,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =\langle 2,0\rangle, \\ r(3) & =\langle 3,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\ln{\left(2 \right)})-f(2,0) \\  & =\left(\left(3\right)^{2} e^{- \left(\ln{\left(2 \right)}\right)}+\left(\ln{\left(2 \right)}\right)^{2}\right)-\left(\left(2\right)^{2} e^{- \left(0\right)}+\left(0\right)^{2}\right) \\  & =\frac{9}{2}+\ln{\left(2 \right)}^{2}-4 \\  & =\ln{\left(2 \right)}^{2} + \frac{1}{2}.\end{aligned}
$$

## Authored variant negative_exponential 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(- 4 x e^{- y}\right)\,i+\left(2 x^{2} e^{- y} + 4 y\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=\ln{\left(x - 1 \right)}$ for $x\in [2,3].$

- $-1 + 2 \ln{\left(2 \right)}^{2}$
- $1 - 2 \ln{\left(2 \right)}^{2}$
- $-2 + 4 \ln{\left(2 \right)}^{2}$
- $- \frac{1}{2} + \ln{\left(2 \right)}^{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(- 4 x e^{- y}\right)}_{P(x,y)}\,i+\underbrace{\left(2 x^{2} e^{- y} + 4 y\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=4 x e^{- y}.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =- 4 x e^{- y}, \\ f_y(x,y) & =2 x^{2} e^{- y} + 4 y.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x^{2} e^{- y} + 2 y^{2}.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,\ln{\left(t - 1 \right)}\rangle,\,t\in [2,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(2) & =\langle 2,0\rangle, \\ r(3) & =\langle 3,\ln{\left(2 \right)}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(3,\ln{\left(2 \right)}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,\ln{\left(2 \right)})-f(2,0) \\  & =\left(- 2 \left(3\right)^{2} e^{- \left(\ln{\left(2 \right)}\right)}+2 \left(\ln{\left(2 \right)}\right)^{2}\right)-\left(- 2 \left(2\right)^{2} e^{- \left(0\right)}+2 \left(0\right)^{2}\right) \\  & =-9+2 \ln{\left(2 \right)}^{2}+8 \\  & =-1 + 2 \ln{\left(2 \right)}^{2}.\end{aligned}
$$

## Authored variant cubic_radical_path 0

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(3 x^{2} - y\right)\,i+\left(- x\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} - e^{\sqrt{x + 1}}$ for $x\in [0,3].$

- $3 e^{2}$
- $- 3 e^{2}$
- $6 e^{2}$
- $\frac{3 e^{2}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(3 x^{2} - y\right)}_{P(x,y)}\,i+\underbrace{\left(- x\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=-1.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =3 x^{2} - y, \\ f_y(x,y) & =- x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=x^{3} - x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} - e^{\sqrt{t + 1}}\rangle,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,- e\rangle, \\ r(3) & =\langle 3,9 - e^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,- e)$ and $(3,9 - e^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,9 - e^{2})-f(0,- e) \\  & =\left(\left(3\right)^{3}- \left(3\right) \left(9 - e^{2}\right)\right)-\left(\left(0\right)^{3}- \left(0\right) \left(- e\right)\right) \\  & =\left(27-27+3 e^{2}\right)-\left(0\right) \\  & =\left(3 e^{2}\right)-\left(0\right) \\  & =3 e^{2}.\end{aligned}
$$

## Authored variant cubic_radical_path 1

authored bank/parameter variation

Consider the vector field $F,$ defined as

$$
F(x,y)=\left(- 6 x^{2} - 2 y\right)\,i+\left(- 2 x\right)\,j.
$$

Evaluate ${\int }_{C}F\cdot \text{d}r,$ where $C$ is the curve $y=x^{2} - e^{\sqrt{x + 1}}$ for $x\in [0,3].$

- $-108 + 6 e^{2}$
- $108 - 6 e^{2}$
- $-216 + 12 e^{2}$
- $-54 + 3 e^{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).
$$

 

First, we define $P(x,y)$ and $Q(x,y)$ as follows:

$$
F(x,y)=\underbrace{\left(- 6 x^{2} - 2 y\right)}_{P(x,y)}\,i+\underbrace{\left(- 2 x\right)}_{Q(x,y)}\,j.
$$

To apply the fundamental theorem for line integrals, we must first find a potential function $f$ (if it exists) such that $F=∇f.$ Notice that the domain of $F$ is ${R}^{2},$ and

$$
\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}=-2.
$$

Since the partial derivatives are continuous and equal everywhere on ${R}^{2},$ there exists a potential function $f$ such that $F=∇f,$ and we must have

$$
\begin{aligned}f_x(x,y) & =- 6 x^{2} - 2 y, \\ f_y(x,y) & =- 2 x.\end{aligned}
$$

Reconstructing the function $f$ from its gradient in the usual way, we get

$$
f(x,y)=- 2 x^{3} - 2 x y.
$$

Note that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $∇f=F.$

We're now ready to apply the fundamental theorem for line integrals. A suitable parametrization of the curve $C$ is given by

$$
r(t)=\langle t,t^{2} - e^{\sqrt{t + 1}}\rangle,\,t\in [0,3].
$$

The position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =\langle 0,- e\rangle, \\ r(3) & =\langle 3,9 - e^{2}\rangle.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,- e)$ and $(3,9 - e^{2}).$

Finally, applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r \\  & =f(3,9 - e^{2})-f(0,- e) \\  & =\left(- 2 \left(3\right)^{3}- 2 \left(3\right) \left(9 - e^{2}\right)\right)-\left(- 2 \left(0\right)^{3}- 2 \left(0\right) \left(- e\right)\right) \\  & =\left(-54-54+6 e^{2}\right)-\left(0\right) \\  & =\left(-108+6 e^{2}\right)-\left(0\right) \\  & =6 \left(-18 + e^{2}\right).\end{aligned}
$$
