# Directional-rate generator review

Raw originals are ineligible evidence. Changed raw witnesses prove recipe replay; normal anchors and variants use authored complete operation banks. Hard normal solutions retain the source norm chain and conclude with the negative signed rate.

## Original q-36297; raw public replay; ineligible evidence

Consider the function $g(x, y) = \frac{x^{2}}{y}$. What is the rate of change of $g(x, y)$ at the point $(2, 1)$ in the direction of the vector $v = ⟨ - 1, 3⟩$?

A. $17$

B. $1$

C. $-\frac{\sqrt{10}}{10}$

D. $\frac{2\sqrt{5}}{5}$

E. $-\frac{8\sqrt{10}}{5}$

[No observed worked solution.]

## Changed parameter raw-profile evidence q-36297

Consider the function $g(x, y) = \frac{2x^{2}}{y}$. What is the rate of change of $g(x, y)$ at the point $(2, 1)$ in the direction of the vector $v = ⟨ - 1, 3⟩$?

A. $65$

B. $1$

C. $-\frac{\sqrt{10}}{10}$

D. $\frac{2\sqrt{5}}{5}$

E. $-\frac{16\sqrt{10}}{5}$

[No observed worked solution.]

## Authored/mathematically repaired source-shaped anchor q-36297

Consider the function $g(x, y) = \frac{x^{2}}{y}$. What is the rate of change of $g(x, y)$ at the point $(2, 1)$ in the direction of the vector $v = ⟨ - 1, 3⟩$?

A. $-\sqrt{10}$

B. $-\frac{8\sqrt{10}}{5}$

C. $\frac{4\sqrt{10}}{5}$

D. $-\frac{4\sqrt{10}}{5}$

E. $-16$

The rate of change of $g(x,y)$ at the point $(2, 1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(2, 1).$

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-1)^{2}+{3}^{2}}=\sqrt{10} \\ u & =\frac{1}{\sqrt{10}}⟨-1,3⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(2, 1):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x^{2}}{y}),\,\frac{∂}{∂y}(\frac{x^{2}}{y})⟩ \\ & =⟨\frac{2x}{y},\,-\frac{x^{2}}{y^{2}}⟩ \\ ∇g(2, 1) & =⟨\frac{1\cdot 2\cdot 2}{1},\,-\frac{1\cdot {2}^{2}}{{1}^{2}}⟩ \\ & =⟨4,-4⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(2, 1)$ is

$$
\begin{aligned}{g}_{u}^{′}(2, 1) & =∇g(2, 1)\cdot u \\ & =⟨4,-4⟩\cdot ⟨-\frac{\sqrt{10}}{10},\frac{3\sqrt{10}}{10}⟩ \\ & =\frac{4\cdot (-1)+(-4)\cdot 3}{\sqrt{10}} \\ & =-\frac{8\sqrt{10}}{5}.\end{aligned}
$$

## Original q-37074; raw public replay; ineligible evidence

Consider the function $g(x, y) = \sin (y\ln x)$. What is the rate of change of $g(x, y)$ at the point $(e, π)$ in the direction in which the function increases most rapidly?

A. $\frac{\sqrt{π^{2} + e^{2}}}{e}$

B. $\sqrt{\frac{π + e}{e}}$

C. $\frac{\sqrt{π + e}}{e}$

D. $\frac{\sqrt{π^{2} + e^{2}}}{π}$

E. $\frac{\sqrt{π^{4} + e^{2}}}{π}$

[No observed worked solution.]

## Changed parameter raw-profile evidence q-37074

Consider the function $g(x, y) = \sin (y\ln x)$. What is the rate of change of $g(x, y)$ at the point $(e, 2 \pi)$ in the direction in which the function increases most rapidly?

A. $\frac{\sqrt{(2 \pi)^{2} + e^{2}}}{e}$

B. $\sqrt{\frac{2 \pi + e}{e}}$

C. $\frac{\sqrt{2 \pi + e}}{e}$

D. $\frac{\sqrt{(2 \pi)^{2} + e^{2}}}{2 \pi}$

E. $\frac{\sqrt{(2 \pi)^{4} + e^{2}}}{2 \pi}$

[No observed worked solution.]

## Authored/mathematically repaired source-shaped anchor q-37074

Consider the function $g(x, y) = \sin (y\ln x)$. What is the rate of change of $g(x, y)$ at the point $(e, π)$ in the direction in which the function increases most rapidly?

A. $\frac{\pi}{e}$

B. $\frac{\sqrt{e^{2} + \pi^{2}}}{e}$

C. $\frac{\sqrt{\pi^{2} + e^{4}}}{e}$

D. $\sqrt{1 + \pi^{2}}$

E. $1 + \frac{\pi}{e}$

At a given point, a function $g(x,y)$ increases most rapidly in the direction of its gradient at that point.

In our case, we compute $∇g(x,y)$ and evaluate it at the point $(e, π):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\sin (y\ln x)),\,\frac{∂}{∂y}(\sin (y\ln x))⟩ \\ & =⟨\cos(y\ln x)\cdot \frac{y}{x},\,\cos(y\ln x)\cdot \ln x⟩ \\ ∇g(e, π) & =⟨\cos(\pi\ln (e))\cdot \frac{\pi}{e},\,\cos(\pi\ln (e))\cdot \ln (e)⟩ \\ & =⟨-\frac{\pi}{e},-1⟩\end{aligned}
$$

Finally, the rate of change of $g(x,y)$ at the point $(e, π)$ in the direction of $∇g(e, π)$ is given by

$$
\begin{aligned}‖∇g(e, π)‖ & =‖⟨-\frac{\pi}{e},-1⟩‖ \\ & =\sqrt{(-\frac{\pi}{e})^{2}+(-1)^{2}} \\ & =\frac{\sqrt{e^{2} + \pi^{2}}}{e}.\end{aligned}
$$

## Original q-130801; raw public replay; ineligible evidence

Consider the function $g(x,y)=\frac{x}{y}+\frac{y}{x}.$ What is the rate of change of $g(x,y)$ at the point $(-1,1)$ in the direction of the vector $v=⟨1,-\sqrt{2}⟩?$

A. $2$

B. $\sqrt{3}$

C. $\sqrt{2}$

D. $0$

E. $3$

The rate of change of $g(x,y)$ at the point $(-1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(-1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{1}^{2}+(-\sqrt{2})^{2}}=\sqrt{3} \\ u & =\frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(-1,1):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}+\frac{y}{x}),\,\frac{∂}{∂y}(\frac{x}{y}+\frac{y}{x})⟩ \\  & =⟨\frac{1}{y}-\frac{y}{{x}^{2}},\,\frac{1}{x}-\frac{x}{{y}^{2}}⟩ \\ ∇g(-1,1) & =⟨\frac{1}{1}-\frac{1}{(-1)^{2}},\frac{1}{(-1)}-\frac{(-1)}{{1}^{2}}⟩ \\  & =⟨0,0⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(-1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(-1,1) & =∇g(-1,1)\cdot u \\  & =⟨0,0⟩\cdot \frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩ \\  & =\frac{0(1)+0(-\sqrt{2})}{\sqrt{3}} \\  & =0.\end{aligned}
$$

## Changed parameter raw-profile evidence q-130801

Consider the function $g(x,y)=\frac{x}{y}+\frac{y}{x}.$ What is the rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of the vector $v=⟨1,-\sqrt{2}⟩?$

A. $2$

B. $\sqrt{3}$

C. $\sqrt{2}$

D. $0$

E. $3$

The rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{1}^{2}+(-\sqrt{2})^{2}}=\sqrt{3} \\ u & =\frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}+\frac{y}{x}),\,\frac{∂}{∂y}(\frac{x}{y}+\frac{y}{x})⟩ \\  & =⟨\frac{1}{y}-\frac{y}{{x}^{2}},\,\frac{1}{x}-\frac{x}{{y}^{2}}⟩ \\ ∇g(1,1) & =⟨\frac{1}{1}-\frac{1}{{1}^{2}},\frac{1}{1}-\frac{1}{{1}^{2}}⟩ \\  & =⟨0,0⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(1,1) & =∇g(1,1)\cdot u \\  & =⟨0,0⟩\cdot \frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩ \\  & =\frac{0(1)+0(-\sqrt{2})}{\sqrt{3}} \\  & =0.\end{aligned}
$$

## Authored/mathematically repaired source-shaped anchor q-130801

Consider the function $g(x,y)=\frac{x}{y}+\frac{y}{x}.$ What is the rate of change of $g(x,y)$ at the point $(-1,1)$ in the direction of the vector $v=⟨1,-\sqrt{2}⟩?$

A. $\sqrt{3}$

B. $0$

C. $\frac{2\sqrt{6}}{3}$

D. $\frac{2\sqrt{3}}{3}$

E. $\frac{2\sqrt{3} (1 +\sqrt{2})}{3}$

The rate of change of $g(x,y)$ at the point $(-1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(-1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{1}^{2}+(-\sqrt{2})^{2}}=\sqrt{3} \\ u & =\frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(-1,1):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}+\frac{y}{x}),\,\frac{∂}{∂y}(\frac{x}{y}+\frac{y}{x})⟩ \\  & =⟨\frac{1}{y}-\frac{y}{{x}^{2}},\,\frac{1}{x}-\frac{x}{{y}^{2}}⟩ \\ ∇g(-1,1) & =⟨\frac{1}{1}-\frac{1}{(-1)^{2}},\frac{1}{(-1)}-\frac{(-1)}{{1}^{2}}⟩ \\  & =⟨0,0⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(-1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(-1,1) & =∇g(-1,1)\cdot u \\  & =⟨0,0⟩\cdot \frac{1}{\sqrt{3}}⟨1,-\sqrt{2}⟩ \\  & =\frac{0(1)+0(-\sqrt{2})}{\sqrt{3}} \\  & =0.\end{aligned}
$$

## Original q-36300; raw public replay; ineligible evidence

Consider the function $f(x,y)=2xy+{e}^{3x-y}.$ What is the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly?

A. $\sqrt{80}$

B. $\sqrt{8}$

C. $\sqrt{10}$

D. $\sqrt{82}$

E. $9$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(1,3):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}(2xy+{e}^{3x-y})\text{ }i-\frac{∂}{∂y}(2xy+{e}^{3x-y})\text{ }j \\  & =-(2y+3{e}^{3x-y})\text{ }i-(2x-{e}^{3x-y})\text{ }j \\ -∇\,f(1,3) & =-(2\cdot 3+3\cdot {e}^{3\cdot 1-3})\text{ }i-(2\cdot 1-{e}^{3\cdot 1-3})\text{ }j \\  & =-9\text{ }i-\text{ }j\end{aligned}
$$

Finally, the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction of $-∇f(1,3)$ is given by

$$
\begin{aligned}‖-∇\,f(1,3)‖ & =‖-9\text{ }i-\text{ }j‖ \\  & =\sqrt{(-9)^{2}+(-1)^{2}} \\  & =\sqrt{82}.\end{aligned}
$$

## Changed parameter raw-profile evidence q-36300

Consider the function $f(x,y)=3xy+{e}^{3x-y}.$ What is the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly?

A. $\sqrt{140}$

B. $\sqrt{10}$

C. $\sqrt{14}$

D. $\sqrt{148}$

E. $12$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(1,3):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}(3xy+{e}^{3x-y})\text{ }i-\frac{∂}{∂y}(3xy+{e}^{3x-y})\text{ }j \\  & =-(3y+3{e}^{3x-y})\text{ }i-(3x-{e}^{3x-y})\text{ }j \\ -∇\,f(1,3) & =-(3\cdot 3+3\cdot {e}^{3\cdot 1-3})\text{ }i-(3\cdot 1-{e}^{3\cdot 1-3})\text{ }j \\  & =-12\text{ }i-2\text{ }j\end{aligned}
$$

Finally, the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction of $-∇f(1,3)$ is given by

$$
\begin{aligned}‖-∇\,f(1,3)‖ & =‖-12\text{ }i-2\text{ }j‖ \\  & =\sqrt{(-12)^{2}+(-2)^{2}} \\  & =2\sqrt{37}.\end{aligned}
$$

## Authored/mathematically repaired source-shaped anchor q-36300

Consider the function $f(x,y)=2xy+{e}^{3x-y}.$ What is the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly?

A. $-9$

B. $-\sqrt{82}$

C. $-5\sqrt{2}$

D. $\sqrt{82}$

E. $-\sqrt{10}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(1,3):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}(2xy+{e}^{3x-y})\text{ }i-\frac{∂}{∂y}(2xy+{e}^{3x-y})\text{ }j \\  & =-(2y+3{e}^{3x-y})\text{ }i-(2x-{e}^{3x-y})\text{ }j \\ -∇\,f(1,3) & =-(2\cdot 3+3\cdot {e}^{3\cdot 1-3})\text{ }i-(2\cdot 1-{e}^{3\cdot 1-3})\text{ }j \\  & =-9\text{ }i-\text{ }j\end{aligned}
$$

Finally, the norm of $-∇f(1,3)$ is

$$
\begin{aligned}‖-∇\,f(1,3)‖ & =‖-9\text{ }i-\text{ }j‖ \\  & =\sqrt{(-9)^{2}+(-1)^{2}} \\  & =\sqrt{82}.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly is $-\sqrt{82}.$

## Original q-37083; raw public replay; ineligible evidence

Consider the function $f(x,y)=(x+y)\operatorname{ln}⁡(x+y).$ What is the rate of change of $f(x,y)$ at the point $(2,-1)$ in the direction in which the function decreases most rapidly?

A. $1$

B. $\sqrt{3}$

C. $2\sqrt{2}$

D. $2$

E. $\sqrt{2}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(2,-1):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}((x+y)\operatorname{ln}⁡(x+y))\text{ }i-\frac{∂}{∂y}((x+y)\operatorname{ln}⁡(x+y))\text{ }j \\  & =(\operatorname{ln}⁡(x+y)+1)\text{ }i+(\operatorname{ln}⁡(x+y)+1)\text{ }j \\ -∇\,f(2,-1) & =-(\operatorname{ln}⁡(2-1)+1)i-(\operatorname{ln}⁡(2-1)+1)j \\  & =-i-j\end{aligned}
$$

Finally, the rate of change of $f(x,y)$ at the point $(2,-1)$ in the direction of $-∇f(2,-1)$ is given by

$$
\begin{aligned}‖-∇\,f(2,-1)‖ & =‖-i-j‖ \\  & =\sqrt{(-1)^{2}+(-1)^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

## Changed parameter raw-profile evidence q-37083

Consider the function $f(x,y)=(3x+y)\operatorname{ln}⁡(3x+y).$ What is the rate of change of $f(x,y)$ at the point $(2,-5)$ in the direction in which the function decreases most rapidly?

A. $3$

B. $\sqrt{5}$

C. $2\sqrt{10}$

D. $4$

E. $\sqrt{10}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(2,-5):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}((3x+y)\operatorname{ln}⁡(3x+y))\text{ }i-\frac{∂}{∂y}((3x+y)\operatorname{ln}⁡(3x+y))\text{ }j \\  & =3(\operatorname{ln}⁡(3x+y)+1)\text{ }i+(\operatorname{ln}⁡(3x+y)+1)\text{ }j \\ -∇\,f(2,-5) & =-3(\operatorname{ln}⁡(3\cdot 2-5)+1)i-(\operatorname{ln}⁡(3\cdot 2-5)+1)j \\  & =-3i-j\end{aligned}
$$

Finally, the rate of change of $f(x,y)$ at the point $(2,-5)$ in the direction of $-∇f(2,-5)$ is given by

$$
\begin{aligned}‖-∇\,f(2,-5)‖ & =‖-3i-j‖ \\  & =\sqrt{(-3)^{2}+(-1)^{2}} \\  & =\sqrt{10}.\end{aligned}
$$

## Authored/mathematically repaired source-shaped anchor q-37083

Consider the function $f(x,y)=(x+y)\operatorname{ln}⁡(x+y).$ What is the rate of change of $f(x,y)$ at the point $(2,-1)$ in the direction in which the function decreases most rapidly?

A. $-2$

B. $-\sqrt{2}$

C. $0$

D. $\sqrt{2}$

E. $-1$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(2,-1):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}((x+y)\operatorname{ln}⁡(x+y))\text{ }i-\frac{∂}{∂y}((x+y)\operatorname{ln}⁡(x+y))\text{ }j \\  & =-(\operatorname{ln}⁡(x+y)+1)\text{ }i-(\operatorname{ln}⁡(x+y)+1)\text{ }j \\ -∇\,f(2,-1) & =-(\operatorname{ln}⁡(2-1)+1)i-(\operatorname{ln}⁡(2-1)+1)j \\  & =-i-j\end{aligned}
$$

Finally, the norm of $-∇f(2,-1)$ is

$$
\begin{aligned}‖-∇\,f(2,-1)‖ & =‖-i-j‖ \\  & =\sqrt{(-1)^{2}+(-1)^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(2,-1)$ in the direction in which the function decreases most rapidly is $-\sqrt{2}.$

## Original q-83608; raw public replay; ineligible evidence

Consider the function $g(x,y)=\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy.$ What is the rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of the vector $v=⟨-2,2⟩?$

A. $-2\pi $

B. $\frac{\pi }{\sqrt{2}}$

C. $\pi \sqrt{2}$

D. $\frac{\pi }{2}$

E. $-\frac{\pi }{\sqrt{2}}$

The rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-2)^{2}+{2}^{2}}=2\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy),\,\frac{∂}{∂y}(\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy)⟩ \\  & =⟨\frac{\pi \operatorname{cos}⁡(\pi x)}{y}+\pi y,\,-\frac{\operatorname{sin}⁡(\pi x)}{{y}^{2}}+\pi x⟩ \\ ∇\,g(1,1) & =⟨\frac{\pi \operatorname{cos}⁡(\pi \cdot 1)}{1}+\pi \cdot 1,\,-\frac{\operatorname{sin}⁡(\pi \cdot 1)}{{1}^{2}}+\pi \cdot 1⟩ \\  & =⟨-\pi +\pi ,0+\pi ⟩ \\  & =⟨0,\pi ⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(1,1) & =∇\,g(1,1)\cdot u \\  & =⟨0,\pi ⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{0\cdot (-1)+\pi \cdot 1}{\sqrt{2}} \\  & =\frac{\pi }{\sqrt{2}}.\end{aligned}
$$

## Changed parameter raw-profile evidence q-83608

Consider the function $g(x,y)=\frac{\operatorname{sin}⁡(\pi x)}{y}+2\pi xy.$ What is the rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of the vector $v=⟨-2,2⟩?$

A. $-4\pi $

B. $\frac{\sqrt{2} \pi}{2}$

C. $\pi \sqrt{2}$

D. $\frac{2 \pi }{2}$

E. $-\frac{\sqrt{2} \pi}{2}$

The rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-2)^{2}+{2}^{2}}=2\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(\frac{\operatorname{sin}⁡(\pi x)}{y}+2\pi xy),\,\frac{∂}{∂y}(\frac{\operatorname{sin}⁡(\pi x)}{y}+2\pi xy)⟩ \\  & =⟨\frac{\pi \operatorname{cos}⁡(\pi x)}{y}+2\pi y,\,-\frac{\operatorname{sin}⁡(\pi x)}{{y}^{2}}+2\pi x⟩ \\ ∇\,g(1,1) & =⟨\frac{\pi \operatorname{cos}⁡(\pi \cdot 1)}{1}+2\pi \cdot 1,\,-\frac{\operatorname{sin}⁡(\pi \cdot 1)}{{1}^{2}}+2\pi \cdot 1⟩ \\  & =⟨-\pi +2 \pi ,0+2 \pi ⟩ \\  & =⟨\pi,2 \pi ⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(1,1) & =∇\,g(1,1)\cdot u \\  & =⟨\pi,2 \pi ⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{\pi\cdot (-1)+2 \pi \cdot 1}{\sqrt{2}} \\  & =\frac{\pi }{\sqrt{2}}.\end{aligned}
$$

## Authored/mathematically repaired source-shaped anchor q-83608

Consider the function $g(x,y)=\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy.$ What is the rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of the vector $v=⟨-2,2⟩?$

A. $\frac{\pi}{4}$

B. $\frac{\sqrt{2} \pi}{2}$

C. $-\frac{\sqrt{2} \pi}{2}$

D. $2 \pi$

E. $0$

The rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-2)^{2}+{2}^{2}}=2\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy),\,\frac{∂}{∂y}(\frac{\operatorname{sin}⁡(\pi x)}{y}+\pi xy)⟩ \\  & =⟨\frac{\pi \operatorname{cos}⁡(\pi x)}{y}+\pi y,\,-\frac{\operatorname{sin}⁡(\pi x)}{{y}^{2}}+\pi x⟩ \\ ∇\,g(1,1) & =⟨\frac{\pi \operatorname{cos}⁡(\pi \cdot 1)}{1}+\pi \cdot 1,\,-\frac{\operatorname{sin}⁡(\pi \cdot 1)}{{1}^{2}}+\pi \cdot 1⟩ \\  & =⟨-\pi +\pi ,0+\pi ⟩ \\  & =⟨0,\pi ⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(1,1) & =∇\,g(1,1)\cdot u \\  & =⟨0,\pi ⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{0\cdot (-1)+\pi \cdot 1}{\sqrt{2}} \\  & =\frac{\pi }{\sqrt{2}}.\end{aligned}
$$

## Original q-83613; raw public replay; ineligible evidence

Consider the function $g(x,y)=2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x.$ What is the rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of the vector $v=⟨-1,1⟩?$

A. $\pi -\sqrt{2}$

B. $2(\pi -2)$

C. $\sqrt{2}(\pi -2)$

D. $\sqrt{2}(\pi +2)$

E. $2(\pi +2)$

The rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-1)^{2}+{1}^{2}}=\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(\frac{\pi }{4},\frac{\pi }{4}):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x),\,\frac{∂}{∂y}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x)⟩ \\  & =⟨2\operatorname{tan}⁡y-2y{sec}^{2}⁡x,\,2x{sec}^{2}⁡y-2\operatorname{tan}⁡x⟩ \\ ∇\,g(\frac{\pi }{4},\frac{\pi }{4}) & =⟨2\operatorname{tan}⁡(\frac{\pi }{4})-2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4}),\,2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4})-2\operatorname{tan}⁡(\frac{\pi }{4})⟩ \\  & =⟨2\cdot 1-\frac{\pi }{2}\cdot 2,\frac{\pi }{2}\cdot 2-2\cdot 1⟩ \\  & =⟨2-\pi ,\,\pi -2⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4})$ is

$$
\begin{aligned}{g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}) & =∇\,g(\frac{\pi }{4},\frac{\pi }{4})\cdot u \\  & =⟨2-\pi ,\pi -2⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{(2-\pi )\cdot (-1)+(\pi -2)\cdot 1}{\sqrt{2}} \\  & =\frac{2\pi -4}{\sqrt{2}} \\  & =\sqrt{2}(\pi -2).\end{aligned}
$$

## Changed parameter raw-profile evidence q-83613

Consider the function $g(x,y)=3x\operatorname{tan}⁡y-3y\operatorname{tan}⁡x.$ What is the rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of the vector $v=⟨-1,1⟩?$

A. $\frac{3}{2}\pi -\frac{3\sqrt{2}}{2}$

B. $3(\pi -2)$

C. $\frac{3\sqrt{2}}{2}(\pi -2)$

D. $\frac{3\sqrt{2}}{2}(\pi +2)$

E. $3(\pi +2)$

The rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-1)^{2}+{1}^{2}}=\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(\frac{\pi }{4},\frac{\pi }{4}):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(3x\operatorname{tan}⁡y-3y\operatorname{tan}⁡x),\,\frac{∂}{∂y}(3x\operatorname{tan}⁡y-3y\operatorname{tan}⁡x)⟩ \\  & =⟨3\operatorname{tan}⁡y-3y{sec}^{2}⁡x,\,3x{sec}^{2}⁡y-3\operatorname{tan}⁡x⟩ \\ ∇\,g(\frac{\pi }{4},\frac{\pi }{4}) & =⟨3\operatorname{tan}⁡(\frac{\pi }{4})-3\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4}),\,3\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4})-3\operatorname{tan}⁡(\frac{\pi }{4})⟩ \\  & =⟨3\cdot 1-\frac{3 \pi }{4}\cdot 2,\frac{3 \pi }{4}\cdot 2-3\cdot 1⟩ \\  & =⟨3-\frac{3 \pi}{2} ,\,\frac{3 \pi}{2}-3⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4})$ is

$$
\begin{aligned}{g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}) & =∇\,g(\frac{\pi }{4},\frac{\pi }{4})\cdot u \\  & =⟨3-\frac{3 \pi}{2} ,\frac{3 \pi}{2}-3⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{(3-\frac{3 \pi}{2} )\cdot (-1)+(\frac{3 \pi}{2}-3)\cdot 1}{\sqrt{2}} \\  & =\frac{-6 + 3 \pi}{\sqrt{2}} \\  & =\frac{3\sqrt{2}(\pi -2)}{2}.\end{aligned}
$$

## Authored/mathematically repaired source-shaped anchor q-83613

Consider the function $g(x,y)=2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x.$ What is the rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of the vector $v=⟨-1,1⟩?$

A. $\sqrt{2} \pi$

B. $\sqrt{2} (-2 + \pi)$

C. $\sqrt{2} (2 -\pi)$

D. $-4 + 2 \pi$

E. $-2\sqrt{2}$

The rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-1)^{2}+{1}^{2}}=\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(\frac{\pi }{4},\frac{\pi }{4}):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x),\,\frac{∂}{∂y}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x)⟩ \\  & =⟨2\operatorname{tan}⁡y-2y{sec}^{2}⁡x,\,2x{sec}^{2}⁡y-2\operatorname{tan}⁡x⟩ \\ ∇\,g(\frac{\pi }{4},\frac{\pi }{4}) & =⟨2\operatorname{tan}⁡(\frac{\pi }{4})-2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4}),\,2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4})-2\operatorname{tan}⁡(\frac{\pi }{4})⟩ \\  & =⟨2\cdot 1-\frac{\pi }{2}\cdot 2,\frac{\pi }{2}\cdot 2-2\cdot 1⟩ \\  & =⟨2-\pi ,\,\pi -2⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4})$ is

$$
\begin{aligned}{g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}) & =∇\,g(\frac{\pi }{4},\frac{\pi }{4})\cdot u \\  & =⟨2-\pi ,\pi -2⟩\cdot ⟨-\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{(2-\pi )\cdot (-1)+(\pi -2)\cdot 1}{\sqrt{2}} \\  & =\frac{2\pi -4}{\sqrt{2}} \\  & =\sqrt{2}(\pi -2).\end{aligned}
$$

## Generated easy / quotient / 0

Consider the function $g(x, y) = \frac{2x^{2}}{y}$. What is the rate of change of $g(x, y)$ at the point $(2, 4)$ in the direction of the vector $v = ⟨ 3, -2⟩$?

A. $-\frac{5\sqrt{13}}{13}$

B. $7$

C. $\frac{7\sqrt{13}}{13}$

D. $\frac{5\sqrt{13}}{13}$

E. $\frac{\sqrt{13}}{2}$

The rate of change of $g(x,y)$ at the point $(2, 4)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(2, 4).$

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{3}^{2}+(-2)^{2}}=\sqrt{13} \\ u & =\frac{1}{\sqrt{13}}⟨3,-2⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(2, 4):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{2x^{2}}{y}),\,\frac{∂}{∂y}(\frac{2x^{2}}{y})⟩ \\ & =⟨\frac{4x}{y},\,-\frac{2x^{2}}{y^{2}}⟩ \\ ∇g(2, 4) & =⟨\frac{2\cdot 2\cdot 2}{4},\,-\frac{2\cdot {2}^{2}}{{4}^{2}}⟩ \\ & =⟨2,-\frac{1}{2}⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(2, 4)$ is

$$
\begin{aligned}{g}_{u}^{′}(2, 4) & =∇g(2, 4)\cdot u \\ & =⟨2,-\frac{1}{2}⟩\cdot ⟨\frac{3\sqrt{13}}{13},-\frac{2\sqrt{13}}{13}⟩ \\ & =\frac{2\cdot 3+(-\frac{1}{2})\cdot (-2)}{\sqrt{13}} \\ & =\frac{7\sqrt{13}}{13}.\end{aligned}
$$

## Generated easy / quotient / 1

Consider the function $g(x, y) = \frac{3x^{2}}{y}$. What is the rate of change of $g(x, y)$ at the point $(4, 1)$ in the direction of the vector $v = ⟨ -3, 2⟩$?

A. $-168$

B. $-\frac{168\sqrt{13}}{13}$

C. $\frac{24\sqrt{13}}{13}$

D. $-\frac{24\sqrt{13}}{13}$

E. $-\frac{96\sqrt{13}}{13}$

The rate of change of $g(x,y)$ at the point $(4, 1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(4, 1).$

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-3)^{2}+{2}^{2}}=\sqrt{13} \\ u & =\frac{1}{\sqrt{13}}⟨-3,2⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(4, 1):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{3x^{2}}{y}),\,\frac{∂}{∂y}(\frac{3x^{2}}{y})⟩ \\ & =⟨\frac{6x}{y},\,-\frac{3x^{2}}{y^{2}}⟩ \\ ∇g(4, 1) & =⟨\frac{3\cdot 2\cdot 4}{1},\,-\frac{3\cdot {4}^{2}}{{1}^{2}}⟩ \\ & =⟨24,-48⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(4, 1)$ is

$$
\begin{aligned}{g}_{u}^{′}(4, 1) & =∇g(4, 1)\cdot u \\ & =⟨24,-48⟩\cdot ⟨-\frac{3\sqrt{13}}{13},\frac{2\sqrt{13}}{13}⟩ \\ & =\frac{24\cdot (-3)+(-48)\cdot 2}{\sqrt{13}} \\ & =-\frac{168\sqrt{13}}{13}.\end{aligned}
$$

## Generated moderate / ratio_sum / 0

Consider the function $g(x,y)=\frac{x}{y}+\frac{y}{x}.$ What is the rate of change of $g(x,y)$ at the point $(-3,-2)$ in the direction of the vector $v=⟨1,3⟩?$

A. $\sqrt{10}$

B. $-\frac{143\sqrt{10}}{360}$

C. $\frac{7\sqrt{10}}{72}$

D. $-\frac{127\sqrt{10}}{360}$

E. $\frac{19\sqrt{10}}{360}$

The rate of change of $g(x,y)$ at the point $(-3,-2)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(-3,-2).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{1}^{2}+{3}^{2}}=\sqrt{10} \\ u & =\frac{1}{\sqrt{10}}⟨1,3⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(-3,-2):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}+\frac{y}{x}),\,\frac{∂}{∂y}(\frac{x}{y}+\frac{y}{x})⟩ \\  & =⟨\frac{1}{y}-\frac{y}{{x}^{2}},\,\frac{1}{x}-\frac{x}{{y}^{2}}⟩ \\ ∇g(-3,-2) & =⟨\frac{1}{(-2)}-\frac{(-2)}{(-3)^{2}},\frac{1}{(-3)}-\frac{(-3)}{(-2)^{2}}⟩ \\  & =⟨-\frac{5}{18},\frac{5}{12}⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(-3,-2)$ is

$$
\begin{aligned}{g}_{u}^{′}(-3,-2) & =∇g(-3,-2)\cdot u \\  & =⟨-\frac{5}{18},\frac{5}{12}⟩\cdot \frac{1}{\sqrt{10}}⟨1,3⟩ \\  & =\frac{(-\frac{5}{18})(1)+\frac{5}{12}(3)}{\sqrt{10}} \\  & =\frac{7\sqrt{10}}{72}.\end{aligned}
$$

## Generated moderate / ratio_sum / 1

Consider the function $g(x,y)=\frac{x}{y}+\frac{y}{x}.$ What is the rate of change of $g(x,y)$ at the point $(-1,3)$ in the direction of the vector $v=⟨-3,-3⟩?$

A. $-\frac{10\sqrt{2}}{9}$

B. $\frac{16\sqrt{2}}{9}$

C. $\frac{17\sqrt{2}}{9}$

D. $-\frac{11\sqrt{2}}{9}$

E. $3\sqrt{2}$

The rate of change of $g(x,y)$ at the point $(-1,3)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(-1,3).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-3)^{2}+(-3)^{2}}=3\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨-1,-1⟩\end{aligned}
$$

Now, we find the gradient $∇g(x,y)$ and evaluate it at the point $(-1,3):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}+\frac{y}{x}),\,\frac{∂}{∂y}(\frac{x}{y}+\frac{y}{x})⟩ \\  & =⟨\frac{1}{y}-\frac{y}{{x}^{2}},\,\frac{1}{x}-\frac{x}{{y}^{2}}⟩ \\ ∇g(-1,3) & =⟨\frac{1}{3}-\frac{3}{(-1)^{2}},\frac{1}{(-1)}-\frac{(-1)}{{3}^{2}}⟩ \\  & =⟨-\frac{8}{3},-\frac{8}{9}⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(-1,3)$ is

$$
\begin{aligned}{g}_{u}^{′}(-1,3) & =∇g(-1,3)\cdot u \\  & =⟨-\frac{8}{3},-\frac{8}{9}⟩\cdot \frac{1}{\sqrt{2}}⟨-1,-1⟩ \\  & =\frac{(-\frac{8}{3})(-1)+(-\frac{8}{9})(-1)}{\sqrt{2}} \\  & =\frac{16\sqrt{2}}{9}.\end{aligned}
$$

## Generated moderate / sine_quotient / 0

Consider the function $g(x,y)=\frac{2\operatorname{sin}⁡(\pi x)}{y}+2\pi xy.$ What is the rate of change of $g(x,y)$ at the point $(4,2)$ in the direction of the vector $v=⟨2,2⟩?$

A. $26 \pi$

B. $6\sqrt{2} \pi$

C. $\frac{13 \pi}{4}$

D. $\frac{13\sqrt{2} \pi}{2}$

E. $-\frac{13\sqrt{2} \pi}{2}$

The rate of change of $g(x,y)$ at the point $(4,2)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(4,2).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{2}^{2}+{2}^{2}}=2\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(4,2):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(\frac{2\operatorname{sin}⁡(\pi x)}{y}+2\pi xy),\,\frac{∂}{∂y}(\frac{2\operatorname{sin}⁡(\pi x)}{y}+2\pi xy)⟩ \\  & =⟨\frac{2\pi \operatorname{cos}⁡(\pi x)}{y}+2\pi y,\,-\frac{2\operatorname{sin}⁡(\pi x)}{{y}^{2}}+2\pi x⟩ \\ ∇\,g(4,2) & =⟨\frac{2\pi \operatorname{cos}⁡(\pi \cdot 4)}{2}+2\pi \cdot 2,\,-\frac{2\operatorname{sin}⁡(\pi \cdot 4)}{{2}^{2}}+2\pi \cdot 4⟩ \\  & =⟨\pi +4 \pi ,0+8 \pi ⟩ \\  & =⟨5 \pi,8 \pi ⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(4,2)$ is

$$
\begin{aligned}{g}_{u}^{′}(4,2) & =∇\,g(4,2)\cdot u \\  & =⟨5 \pi,8 \pi ⟩\cdot ⟨\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{5 \pi\cdot 1+8 \pi \cdot 1}{\sqrt{2}} \\  & =\frac{13 \pi }{\sqrt{2}}.\end{aligned}
$$

## Generated moderate / sine_quotient / 1

Consider the function $g(x,y)=\frac{3\operatorname{sin}⁡(\pi x)}{y}+4\pi xy.$ What is the rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of the vector $v=⟨2,2⟩?$

A. $-\frac{5\sqrt{2} \pi}{2}$

B. $\frac{5\sqrt{2} \pi}{2}$

C. $4\sqrt{2} \pi$

D. $\frac{5 \pi}{4}$

E. $10 \pi$

The rate of change of $g(x,y)$ at the point $(1,1)$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(1,1).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{2}^{2}+{2}^{2}}=2\sqrt{2} \\ u & =\frac{1}{\sqrt{2}}⟨1,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(\frac{3\operatorname{sin}⁡(\pi x)}{y}+4\pi xy),\,\frac{∂}{∂y}(\frac{3\operatorname{sin}⁡(\pi x)}{y}+4\pi xy)⟩ \\  & =⟨\frac{3\pi \operatorname{cos}⁡(\pi x)}{y}+4\pi y,\,-\frac{3\operatorname{sin}⁡(\pi x)}{{y}^{2}}+4\pi x⟩ \\ ∇\,g(1,1) & =⟨\frac{3\pi \operatorname{cos}⁡(\pi \cdot 1)}{1}+4\pi \cdot 1,\,-\frac{3\operatorname{sin}⁡(\pi \cdot 1)}{{1}^{2}}+4\pi \cdot 1⟩ \\  & =⟨-3 \pi +4 \pi ,0+4 \pi ⟩ \\  & =⟨\pi,4 \pi ⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(1,1)$ is

$$
\begin{aligned}{g}_{u}^{′}(1,1) & =∇\,g(1,1)\cdot u \\  & =⟨\pi,4 \pi ⟩\cdot ⟨\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}⟩ \\  & =\frac{\pi\cdot 1+4 \pi \cdot 1}{\sqrt{2}} \\  & =\frac{5 \pi }{\sqrt{2}}.\end{aligned}
$$

## Generated moderate / tangent / 0

Consider the function $g(x,y)=2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x.$ What is the rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of the vector $v=⟨1,3⟩?$

A. $\frac{\sqrt{10} \pi}{5}$

B. $-\frac{2\sqrt{10}}{5}$

C. $\frac{\sqrt{10} (-2 + \pi)}{5}$

D. $\frac{\sqrt{10} (2 -\pi)}{5}$

E. $-4 + 2 \pi$

The rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{{1}^{2}+{3}^{2}}=\sqrt{10} \\ u & =\frac{1}{\sqrt{10}}⟨1,3⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(\frac{\pi }{4},\frac{\pi }{4}):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x),\,\frac{∂}{∂y}(2x\operatorname{tan}⁡y-2y\operatorname{tan}⁡x)⟩ \\  & =⟨2\operatorname{tan}⁡y-2y{sec}^{2}⁡x,\,2x{sec}^{2}⁡y-2\operatorname{tan}⁡x⟩ \\ ∇\,g(\frac{\pi }{4},\frac{\pi }{4}) & =⟨2\operatorname{tan}⁡(\frac{\pi }{4})-2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4}),\,2\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4})-2\operatorname{tan}⁡(\frac{\pi }{4})⟩ \\  & =⟨2\cdot 1-\frac{\pi }{2}\cdot 2,\frac{\pi }{2}\cdot 2-2\cdot 1⟩ \\  & =⟨2-\pi ,\,\pi -2⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4})$ is

$$
\begin{aligned}{g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}) & =∇\,g(\frac{\pi }{4},\frac{\pi }{4})\cdot u \\  & =⟨2-\pi ,\pi -2⟩\cdot ⟨\frac{1}{\sqrt{10}},\frac{3}{\sqrt{10}}⟩ \\  & =\frac{(2-\pi )\cdot 1+(\pi -2)\cdot 3}{\sqrt{10}} \\  & =\frac{2\pi -4}{\sqrt{10}} \\  & =\frac{\sqrt{10} (-2 + \pi)}{5}.\end{aligned}
$$

## Generated moderate / tangent / 1

Consider the function $g(x,y)=5x\operatorname{tan}⁡y-5y\operatorname{tan}⁡x.$ What is the rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of the vector $v=⟨-2,1⟩?$

A. $\frac{3\sqrt{5} (2 -\pi)}{2}$

B. $-3\sqrt{5}$

C. $-15 + \frac{15 \pi}{2}$

D. $\frac{3\sqrt{5} (-2 + \pi)}{2}$

E. $\frac{3\sqrt{5} \pi}{2}$

The rate of change of $g(x,y)$ at the point $(\frac{\pi }{4},\frac{\pi }{4})$ in the direction of $v$ is equal to the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}).$ 

First, we find the unit vector $u$ in the direction of $v:$

$$
\begin{aligned}‖v‖ & =\sqrt{(-2)^{2}+{1}^{2}}=\sqrt{5} \\ u & =\frac{1}{\sqrt{5}}⟨-2,1⟩\end{aligned}
$$

Now, we find the gradient $∇\,g(x,y)$ and evaluate it at the point $(\frac{\pi }{4},\frac{\pi }{4}):$

$$
\begin{aligned}∇\,g(x,y) & =⟨\frac{∂}{∂x}(5x\operatorname{tan}⁡y-5y\operatorname{tan}⁡x),\,\frac{∂}{∂y}(5x\operatorname{tan}⁡y-5y\operatorname{tan}⁡x)⟩ \\  & =⟨5\operatorname{tan}⁡y-5y{sec}^{2}⁡x,\,5x{sec}^{2}⁡y-5\operatorname{tan}⁡x⟩ \\ ∇\,g(\frac{\pi }{4},\frac{\pi }{4}) & =⟨5\operatorname{tan}⁡(\frac{\pi }{4})-5\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4}),\,5\cdot \frac{\pi }{4}\cdot {sec}^{2}⁡(\frac{\pi }{4})-5\operatorname{tan}⁡(\frac{\pi }{4})⟩ \\  & =⟨5\cdot 1-\frac{5 \pi }{4}\cdot 2,\frac{5 \pi }{4}\cdot 2-5\cdot 1⟩ \\  & =⟨5-\frac{5 \pi}{2} ,\,\frac{5 \pi}{2}-5⟩\end{aligned}
$$

Finally, the directional derivative ${g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4})$ is

$$
\begin{aligned}{g}_{u}^{′}(\frac{\pi }{4},\frac{\pi }{4}) & =∇\,g(\frac{\pi }{4},\frac{\pi }{4})\cdot u \\  & =⟨5-\frac{5 \pi}{2} ,\frac{5 \pi}{2}-5⟩\cdot ⟨-\frac{2}{\sqrt{5}},\frac{1}{\sqrt{5}}⟩ \\  & =\frac{(5-\frac{5 \pi}{2} )\cdot (-2)+(\frac{5 \pi}{2}-5)\cdot 1}{\sqrt{5}} \\  & =\frac{-15 + \frac{15 \pi}{2}}{\sqrt{5}} \\  & =\frac{3\sqrt{5} (-2 + \pi)}{2}.\end{aligned}
$$

## Generated hard / exp_bilinear / 0

Consider the function $f(x,y)=2xy+{e}^{4x-y}.$ What is the rate of change of $f(x,y)$ at the point $(3,12)$ in the direction in which the function decreases most rapidly?

A. $-28$

B. $-\sqrt{809}$

C. $-5\sqrt{26}$

D. $-\sqrt{17}$

E. $\sqrt{809}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(3,12):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}(2xy+{e}^{4x-y})\text{ }i-\frac{∂}{∂y}(2xy+{e}^{4x-y})\text{ }j \\  & =-(2y+4{e}^{4x-y})\text{ }i-(2x-{e}^{4x-y})\text{ }j \\ -∇\,f(3,12) & =-(2\cdot 12+4\cdot {e}^{4\cdot 3-12})\text{ }i-(2\cdot 3-{e}^{4\cdot 3-12})\text{ }j \\  & =-28\text{ }i-5\text{ }j\end{aligned}
$$

Finally, the norm of $-∇f(3,12)$ is

$$
\begin{aligned}‖-∇\,f(3,12)‖ & =‖-28\text{ }i-5\text{ }j‖ \\  & =\sqrt{(-28)^{2}+(-5)^{2}} \\  & =\sqrt{809}.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(3,12)$ in the direction in which the function decreases most rapidly is $-\sqrt{809}.$

## Generated hard / exp_bilinear / 1

Consider the function $f(x,y)=3xy+{e}^{3x-y}.$ What is the rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly?

A. $2\sqrt{37}$

B. $-2\sqrt{26}$

C. $-12$

D. $-2\sqrt{37}$

E. $-\sqrt{10}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(1,3):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}(3xy+{e}^{3x-y})\text{ }i-\frac{∂}{∂y}(3xy+{e}^{3x-y})\text{ }j \\  & =-(3y+3{e}^{3x-y})\text{ }i-(3x-{e}^{3x-y})\text{ }j \\ -∇\,f(1,3) & =-(3\cdot 3+3\cdot {e}^{3\cdot 1-3})\text{ }i-(3\cdot 1-{e}^{3\cdot 1-3})\text{ }j \\  & =-12\text{ }i-2\text{ }j\end{aligned}
$$

Finally, the norm of $-∇f(1,3)$ is

$$
\begin{aligned}‖-∇\,f(1,3)‖ & =‖-12\text{ }i-2\text{ }j‖ \\  & =\sqrt{(-12)^{2}+(-2)^{2}} \\  & =2\sqrt{37}.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(1,3)$ in the direction in which the function decreases most rapidly is $-2\sqrt{37}.$

## Generated hard / sumlog / 0

Consider the function $f(x,y)=(3x+4y)\operatorname{ln}⁡(3x+4y).$ What is the rate of change of $f(x,y)$ at the point $(4,-\frac{11}{4})$ in the direction in which the function decreases most rapidly?

A. $-7$

B. $-3$

C. $-5$

D. $0$

E. $5$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(4,-\frac{11}{4}):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}((3x+4y)\operatorname{ln}⁡(3x+4y))\text{ }i-\frac{∂}{∂y}((3x+4y)\operatorname{ln}⁡(3x+4y))\text{ }j \\  & =-3(\operatorname{ln}⁡(3x+4y)+1)\text{ }i-4(\operatorname{ln}⁡(3x+4y)+1)\text{ }j \\ -∇\,f(4,-\frac{11}{4}) & =-3(\operatorname{ln}⁡(3\cdot 4-4\cdot \frac{11}{4})+1)i-4(\operatorname{ln}⁡(3\cdot 4-4\cdot \frac{11}{4})+1)j \\  & =-3i-4j\end{aligned}
$$

Finally, the norm of $-∇f(4,-\frac{11}{4})$ is

$$
\begin{aligned}‖-∇\,f(4,-\frac{11}{4})‖ & =‖-3i-4j‖ \\  & =\sqrt{(-3)^{2}+(-4)^{2}} \\  & =5.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(4,-\frac{11}{4})$ in the direction in which the function decreases most rapidly is $-5.$

## Generated hard / sumlog / 1

Consider the function $f(x,y)=(5x+8y)\operatorname{ln}⁡(5x+8y).$ What is the rate of change of $f(x,y)$ at the point $(1,-\frac{1}{2})$ in the direction in which the function decreases most rapidly?

A. $-5$

B. $-13$

C. $0$

D. $\sqrt{89}$

E. $-\sqrt{89}$

At a given point, a function $f(x,y)$ decreases most rapidly in the opposite direction of its gradient at that point.

In our case, we compute $-∇f(x,y)$ and evaluate it at the point $(1,-\frac{1}{2}):$

$$
\begin{aligned}-∇\,f(x,y) & =-\frac{∂}{∂x}((5x+8y)\operatorname{ln}⁡(5x+8y))\text{ }i-\frac{∂}{∂y}((5x+8y)\operatorname{ln}⁡(5x+8y))\text{ }j \\  & =-5(\operatorname{ln}⁡(5x+8y)+1)\text{ }i-8(\operatorname{ln}⁡(5x+8y)+1)\text{ }j \\ -∇\,f(1,-\frac{1}{2}) & =-5(\operatorname{ln}⁡(5\cdot 1-8\cdot \frac{1}{2})+1)i-8(\operatorname{ln}⁡(5\cdot 1-8\cdot \frac{1}{2})+1)j \\  & =-5i-8j\end{aligned}
$$

Finally, the norm of $-∇f(1,-\frac{1}{2})$ is

$$
\begin{aligned}‖-∇\,f(1,-\frac{1}{2})‖ & =‖-5i-8j‖ \\  & =\sqrt{(-5)^{2}+(-8)^{2}} \\  & =\sqrt{89}.\end{aligned}
$$

Therefore, the signed rate of change of $f(x,y)$ at the point $(1,-\frac{1}{2})$ in the direction in which the function decreases most rapidly is $-\sqrt{89}.$

## Generated hard / sinlog / 0

Consider the function $g(x, y) = 2\sin (y\ln x)$. What is the rate of change of $g(x, y)$ at the point $(e^{2}, 2 \pi)$ in the direction in which the function increases most rapidly?

A. $\frac{4 \pi}{e^{2}}$

B. $\frac{4 \pi}{e^{2}} + 4$

C. $\frac{4\sqrt{\pi^{2} + e^{4}}}{e^{2}}$

D. $\frac{2\sqrt{4 \pi^{2} + e^{8}}}{e^{2}}$

E. $4\sqrt{1 + \pi^{2}}$

At a given point, a function $g(x,y)$ increases most rapidly in the direction of its gradient at that point.

In our case, we compute $∇g(x,y)$ and evaluate it at the point $(e^{2}, 2 \pi):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(2\sin (y\ln x)),\,\frac{∂}{∂y}(2\sin (y\ln x))⟩ \\ & =⟨2\cos(y\ln x)\cdot \frac{y}{x},\,2\cos(y\ln x)\cdot \ln x⟩ \\ ∇g(e^{2}, 2 \pi) & =⟨2\cos(2 \pi\ln (e^{2}))\cdot \frac{2 \pi}{e^{2}},\,2\cos(2 \pi\ln (e^{2}))\cdot \ln (e^{2})⟩ \\ & =⟨\frac{4 \pi}{e^{2}},4⟩\end{aligned}
$$

Finally, the rate of change of $g(x,y)$ at the point $(e^{2}, 2 \pi)$ in the direction of $∇g(e^{2}, 2 \pi)$ is given by

$$
\begin{aligned}‖∇g(e^{2}, 2 \pi)‖ & =‖⟨\frac{4 \pi}{e^{2}},4⟩‖ \\ & =\sqrt{{\frac{4 \pi}{e^{2}}}^{2}+{4}^{2}} \\ & =\frac{4\sqrt{\pi^{2} + e^{4}}}{e^{2}}.\end{aligned}
$$

## Generated hard / sinlog / 1

Consider the function $g(x, y) = 3\sin (y\ln x)$. What is the rate of change of $g(x, y)$ at the point $(e^{4}, \frac{\pi}{4})$ in the direction in which the function increases most rapidly?

A. $\frac{3 \pi}{4 e^{4}} + 12$

B. $\frac{3 \pi}{4 e^{4}}$

C. $\frac{3\sqrt{\pi^{2} + 16 e^{16}}}{4 e^{4}}$

D. $\frac{3\sqrt{\pi^{2} + 256}}{4}$

E. $\frac{3\sqrt{\pi^{2} + 256 e^{8}}}{4 e^{4}}$

At a given point, a function $g(x,y)$ increases most rapidly in the direction of its gradient at that point.

In our case, we compute $∇g(x,y)$ and evaluate it at the point $(e^{4}, \frac{\pi}{4}):$

$$
\begin{aligned}∇g(x,y) & =⟨\frac{∂}{∂x}(3\sin (y\ln x)),\,\frac{∂}{∂y}(3\sin (y\ln x))⟩ \\ & =⟨3\cos(y\ln x)\cdot \frac{y}{x},\,3\cos(y\ln x)\cdot \ln x⟩ \\ ∇g(e^{4}, \frac{\pi}{4}) & =⟨3\cos(\frac{\pi}{4}\ln (e^{4}))\cdot \frac{\frac{\pi}{4}}{e^{4}},\,3\cos(\frac{\pi}{4}\ln (e^{4}))\cdot \ln (e^{4})⟩ \\ & =⟨-\frac{3 \pi}{4 e^{4}},-12⟩\end{aligned}
$$

Finally, the rate of change of $g(x,y)$ at the point $(e^{4}, \frac{\pi}{4})$ in the direction of $∇g(e^{4}, \frac{\pi}{4})$ is given by

$$
\begin{aligned}‖∇g(e^{4}, \frac{\pi}{4})‖ & =‖⟨-\frac{3 \pi}{4 e^{4}},-12⟩‖ \\ & =\sqrt{(-\frac{3 \pi}{4 e^{4}})^{2}+(-12)^{2}} \\ & =\frac{3\sqrt{\pi^{2} + 256 e^{8}}}{4 e^{4}}.\end{aligned}
$$
