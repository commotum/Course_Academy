![](images/09/09a38bb4306728f97b7fecbf9ab1bda7aa957607352c1ab27af09489c271c3ed.png)

Evaluate ${\int }_{C}9\left({y}^{2}-2x\right)\,\text{d}y,$ where $C$ is the path traversed along the line segment from the point $(0,1)$ to the point $(2,3),$ as shown above.

- $9\left(\frac{2}{3}\right)$
- $9\left(\frac{14}{3}\right)$ (correct)
- $9\left(\frac{7}{6}\right)$
- $9\left(\frac{11}{6}\right)$
- $9\left(\frac{5}{3}\right)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}y={\int }_{a}^{b}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t.
$$

The curve $C$ is a line segment with endpoints $(0,1)$ and $(2,3).$ It can be parametrized as 

$$
\begin{aligned}r(t) & =⟨(0+t(2-0)),\,(1+t(3-1))⟩ \\  & =⟨2t,\,1+2t⟩,\end{aligned}
$$

where $0\le t\le 1.$

Computing $\frac{\text{d}y}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1+2t)=2\end{aligned}
$$

Now, since $f(x,y)=9\left({y}^{2}-2x\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =9\left((1+2t)^{2}-2(2t)\right)\\  & =9\left(1+4t+4{t}^{2}-4t\right)\\  & =9\left(4{t}^{2}+1\right)\end{aligned}
$$

We can now evaluate the integral:

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}y & ={\int }_{0}^{1}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t \\  & =9\left({\int }_{0}^{1}(4{t}^{2}+1)\cdot 2\cdot \text{d}t\right)\\  & =9\left(2{\int }_{0}^{1}(4{t}^{2}+1)\,\text{d}t\right)\\  & =9\left(2{[\frac{4{t}^{3}}{3}+t]}_{0}^{1}\right)\\  & =9\left(2(\frac{4}{3}+1)-2(0)\right)\\  & =9\left(\frac{14}{3}\right)\end{aligned}
$$

---

![](images/4d/4d83f771aa650879909c33d7033e80ca044b7e6f8369e19667e6173aa8a40737.png)

Evaluate ${\int }_{C}7\left(x+\sqrt{3y}\right)\,\text{d}y,$ where $C$ is the path traversed along the line segment from the point $(2,0)$ to the point $(0,3),$ as shown above.

- $7\left(12\right)$
- $7\left(4\right)$
- $7\left(8\right)$
- $7\left(3\right)$
- $7\left(9\right)$ (correct)

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}y={\int }_{a}^{b}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t.
$$

The curve $C$ is a line segment with endpoints $(2,0)$ and $(0,3).$ It can be parametrized as 

$$
\begin{aligned}r(t) & =⟨(2+t(0-2)),\,(0+t(3-0))⟩ \\  & =⟨2-2t,\,3t⟩,\end{aligned}
$$

where $0\le t\le 1.$

Computing $\frac{\text{d}y}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3t)=3\end{aligned}
$$

Now, since $f(x,y)=7\left(x+\sqrt{3y}\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =7\left((2-2t)+\sqrt{3(3t)}\right)\\  & =7\left(2-2t+3\sqrt{t}\right)\end{aligned}
$$

We can now evaluate the integral:

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}y & ={\int }_{0}^{1}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t \\  & =7\left({\int }_{0}^{1}(2-2t+3\sqrt{t})\cdot 3\cdot \text{d}t\right)\\  & =7\left(3{\int }_{0}^{1}(2-2t+3{t}^{1/2})\,\text{d}t\right)\\  & =7\left(3{[2t-{t}^{2}+2{t}^{3/2}]}_{0}^{1}\right)\\  & =7\left(3[(2(1)-(1)^{2}+2(1)^{3/2})-(0)]\right)\\  & =7\left(3(3)\right)\\  & =7\left(9\right)\end{aligned}
$$

---

![](images/ab/ab95b870025708090e40cbd7645072e8f4453cf50047b2a00036a30171c81994.png)

Evaluate ${\int }_{C}3\left(\sqrt{x-1}+y\right)\,\text{d}x,$ where $C$ is the path traversed along the line segment from the point $(1,2)$ to the point $(2,1),$ as shown above.

- $3\left(\frac{10}{3}\right)$
- $3\left(\frac{1}{3}\right)$
- $3\left(\frac{13}{6}\right)$ (correct)
- $3\left(\frac{15}{4}\right)$
- $3\left(\frac{3}{5}\right)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}x={\int }_{a}^{b}f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t.
$$

The curve $C$ is a line segment with endpoints $(1,2)$ and $(2,1).$ It can be parametrized as 

$$
\begin{aligned}r(t) & =⟨(1+t(2-1)),\,(2+t(1-2))⟩ \\  & =⟨1+t,\,2-t⟩,\end{aligned}
$$

where $0\le t\le 1.$

Computing $\frac{\text{d}x}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1+t)=1\end{aligned}
$$

Now, since $f(x,y)=3\left(\sqrt{x-1}+y\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =3\left(\sqrt{(1+t)-1}+2-t\right)\\  & =3\left(\sqrt{t}-t+2\right)\end{aligned}
$$

We can now evaluate the integral:

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}x & ={\int }_{0}^{1}f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t \\  & =3\left({\int }_{0}^{1}(\sqrt{t}-t+2)\cdot 1\cdot \text{d}t\right)\\  & =3\left({\int }_{0}^{1}({t}^{1/2}-t+2)\,\text{d}t\right)\\  & =3\left({[\frac{2{t}^{3/2}}{3}-\frac{{t}^{2}}{2}+2t]}_{0}^{1}\right)\\  & =3\left((\frac{2}{3}-\frac{1}{2}+2)-(0)\right)\\  & =3\left(\frac{13}{6}\right)\end{aligned}
$$

---

![](images/be/be3ad044a611d99e67c89d053d4878a2835be65828a4dc9300697bfd61822994.png)

Evaluate ${\int }_{C}7\left({x}^{2}y\right)\,\text{d}y,$ where $C$ is the path along the below-left quarter of the ellipse $4{x}^{2}+{y}^{2}=4,$ traversed from the point $(-1,0)$ to the point $(0,-2),$ as shown above.

- $7\left(9\right)$
- $7\left(1\right)$ (correct)
- $7\left(5\right)$
- $7\left(-2\right)$
- $7\left(-6\right)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}y={\int }_{a}^{b}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t.
$$

Note that we can write the equation of our ellipse in the form

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1.
$$

So, the curve $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $1$ and $2,$ respectively. Therefore, it can be parametrized as 

$$
r(t)=⟨\operatorname{cos}t,\,2\operatorname{sin}t⟩,\,\pi \le t\le \frac{3\pi }{2}.
$$

Computing $\frac{\text{d}y}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(2\operatorname{sin}t)=2\operatorname{cos}t\end{aligned}
$$

Now, since $f(x,y)=7\left({x}^{2}y\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =7\left((\operatorname{cos}t)^{2}(2\operatorname{sin}t)\right)\\  & =7\left(2\operatorname{sin}t{cos}^{2}t\right)\end{aligned}
$$

We can now evaluate the integral:

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}y & ={\int }_{\pi }^{3\pi /2}f(r(t))\,\frac{\text{d}y}{\text{d}t}\,\text{d}t \\  & =7\left({\int }_{\pi }^{3\pi /2}(2\operatorname{sin}t{cos}^{2}t)\cdot (2\operatorname{cos}t)\cdot \text{d}t\right)\\  & =7\left(4{\int }_{\pi }^{3\pi /2}\operatorname{sin}t{cos}^{3}t\,\text{d}t\right)\end{aligned}
$$

We can solve this using the substitution $u=\operatorname{cos}t,$ $\text{d}u=-\operatorname{sin}t\,\text{d}t$ as follows:

$$
\begin{aligned}7\left(4{\int }_{\pi }^{3\pi /2}\operatorname{sin}t{cos}^{3}t\,\text{d}t\right)& =7\left(4{\int }_{-1}^{0}{u}^{3}\,(-\text{d}u)\right)\\  & =7\left(-4{\int }_{-1}^{0}{u}^{3}\,\text{d}u\right)\\  & =7\left(-{u}^{4}{|}_{-1}^{0}\right)\\  & =7\left(-[(0)^{4}-(-1)^{4}]\right)\\  & =7\left(-(-1)\right)\\  & =7\left(1\right)\end{aligned}
$$

---

![](images/0e/0e5257867dae67451500793687a2da24ee31a73a17c691d8d8a6dcded46e8993.png)

Evaluate ${\int }_{C}7\left(x{e}^{1-{y}^{2}}\right)\,\text{d}x,$ where $C$ is the path along the three-quarters of the ellipse ${x}^{2}+9{y}^{2}=9,$ traversed from the point $(0,1)$ to the point $(3,0),$ as shown above.

- $7\left(\frac{1}{2}(e-1)\right)$
- $7\left(\frac{9}{2}(e-1)\right)$ (correct)
- $7\left(\frac{3}{2}(e+1)\right)$
- $7\left(\frac{e}{2}-1\right)$
- $7\left({e}^{2}+1\right)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}x={\int }_{a}^{b}f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t.
$$

Note that we can write the equation of our ellipse in the form

$$
\frac{{x}^{2}}{{3}^{2}}+\frac{{y}^{2}}{{1}^{2}}=1.
$$

So, the curve $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively. Therefore, it can be parametrized as 

$$
r(t)=⟨3\operatorname{cos}t,\,\operatorname{sin}t⟩,\,\frac{\pi }{2}\le t\le 2\pi .
$$

Computing $\frac{\text{d}x}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}t)=-3\operatorname{sin}t\end{aligned}
$$

Now, since $f(x,y)=7\left(x{e}^{1-{y}^{2}}\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =7\left((3\operatorname{cos}t){e}^{1-\operatorname{sin}^{2}t}\right)\\  & =7\left(3\operatorname{cos}t{e}^{\operatorname{cos}^{2}t}\right)\end{aligned}
$$

We can now evaluate the integral:

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}x & ={\int }_{\pi /2}^{2\pi }f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t \\  & =7\left({\int }_{\pi /2}^{2\pi }(3\operatorname{cos}t{e}^{\operatorname{cos}^{2}t})\cdot (-3\operatorname{sin}t)\cdot \text{d}t\right)\\  & =7\left(-9{\int }_{\pi /2}^{2\pi }\operatorname{sin}t\operatorname{cos}t{e}^{\operatorname{cos}^{2}t}\,\text{d}t\right)\end{aligned}
$$

We can solve this using the substitution $u=\operatorname{cos}^{2}t,$ $\text{d}u=-2\operatorname{sin}t\operatorname{cos}t\,\text{d}t$ as follows:

$$
\begin{aligned}7\left(-9{\int }_{\pi /2}^{2\pi }\operatorname{sin}t\operatorname{cos}t{e}^{\operatorname{cos}^{2}t}\,\text{d}t\right)& =7\left(-9{\int }_{0}^{1}{e}^{u}\,(-\frac{1}{2}\text{d}u)\right)\\  & =7\left(\frac{9}{2}{\int }_{0}^{1}{e}^{u}\,\text{d}u\right)\\  & =7\left(\frac{9}{2}{e}^{u}{|}_{0}^{1}\right)\\  & =7\left(\frac{9}{2}[{e}^{1}-{e}^{0}]\right)\\  & =7\left(\frac{9}{2}\cdot (e-1)\right)\\  & =7\left(\frac{9}{2}(e-1)\right)\end{aligned}
$$