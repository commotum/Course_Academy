## q-124121

Original

![](images/36/36b985c811eb28d8220017c6b7407b3a104554d785dafdb35f17553c262bdc35.png)

Which of the following is equivalent to ${\int }_{C}xy\,\text{d}y,$ where $C$ is the path along the line segment from the point $(-1,-2)$ to the point $(2,4),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨3t-1,\,6t-2⟩.$*

Replay

![](generate/scratch/17592186133892/assets/9e42edf11504da65509ea6c7.png)

Which of the following is equivalent to $\int_C\left(x y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-1,-2)$ to the point $(2,4)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 3 t - 1,\,6 t - 2\rangle$.*

- $12\int_{0}^{1}\left(t^{2} - 6 t + 9\right)\,\mathrm{d}t$
- $12\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t$
- $18\int_{0}^{1}\left(t^{2} - 6 t + 9\right)\,\mathrm{d}t$
- $18\int_{0}^{1}\left(t^{2} + 6 t + 9\right)\,\mathrm{d}t$
- $6\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-1,-2)$ and $(2,4)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -1+t(2-(-1)),\,-2+t(4-(-2))\rangle\\&=\langle 3 t - 1,\,6 t - 2\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(6 t - 2\right)=6.
$$

Now, since $f(x,y)=x y$, we obtain

$$
\begin{aligned}f(r(t))&=x y\big|_{x=3 t - 1,\,y=6 t - 2}\\&=18 t^{2} - 12 t + 2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(18 t^{2} - 12 t + 2\right)\left(6\right)\,\mathrm{d}t\\&=12\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124270

Original

![](images/58/58995f1bc5b45dbe0d30a9d0cbf704d792b955e7195c0e4dc3610ddf2e576579.png)

Which of the following is equivalent to ${\int }_{C}({x}^{2}-y)\,\text{d}y,$ where $C$ is the path along the line segment from the point $(-1,-1)$ to the point $(2,1),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨3t-1,\,2t-1⟩.$*

Replay

![](generate/scratch/17592186133892/assets/b6e0511e1c8872b049802465.png)

Which of the following is equivalent to $\int_C\left(x^{2} - y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-1,-1)$ to the point $(2,1)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 3 t - 1,\,2 t - 1\rangle$.*

- $9\int_{0}^{1}\left(2 t^{2} - t + 7\right)\,\mathrm{d}t$
- $\int_{0}^{1}\left(18 t^{2} + t\right)\,\mathrm{d}t$
- $2\int_{0}^{1}\left(9 t^{2} - 8 t + 2\right)\,\mathrm{d}t$
- $3\int_{0}^{1}\left(6 t^{2} + 5\right)\,\mathrm{d}t$
- $6\int_{0}^{1}\left(2 t^{2} + 7 t + 1\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-1,-1)$ and $(2,1)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -1+t(2-(-1)),\,-1+t(1-(-1))\rangle\\&=\langle 3 t - 1,\,2 t - 1\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(2 t - 1\right)=2.
$$

Now, since $f(x,y)=x^{2} - y$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} - y\big|_{x=3 t - 1,\,y=2 t - 1}\\&=9 t^{2} - 8 t + 2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(9 t^{2} - 8 t + 2\right)\left(2\right)\,\mathrm{d}t\\&=2\int_{0}^{1}\left(9 t^{2} - 8 t + 2\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124266

Original

![](images/b2/b21c9c11aa3320a729db0d8a71f5c89069d46527e78dfc76b47ae3925387c770.png)

Which of the following is equivalent to ${\int }_{C}(3x+2y)\,\text{d}y,$ where $C$ is the path along the line segment from the point $(-2,2)$ to the point $(-1,1),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨t-2,\,2-t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/bc768483e99d8272b877bdc5.png)

Which of the following is equivalent to $\int_C\left(3 x + 2 y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-2,2)$ to the point $(-1,1)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle t - 2,\,2 - t\rangle$.*

- $\int_{0}^{1}\left(5 - 2 t\right)\,\mathrm{d}t$
- $\int_{0}^{1}\left(2 - t\right)\,\mathrm{d}t$
- $\int_{0}^{1}\left(3 t + 1\right)\,\mathrm{d}t$
- $\int_{0}^{1}\left(t^{2} + 3 t - 1\right)\,\mathrm{d}t$
- $\int_{0}^{1}\left(1 - t^{2}\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-2,2)$ and $(-1,1)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -2+t(-1-(-2)),\,2+t(1-(2))\rangle\\&=\langle t - 2,\,2 - t\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(2 - t\right)=-1.
$$

Now, since $f(x,y)=3 x + 2 y$, we obtain

$$
\begin{aligned}f(r(t))&=3 x + 2 y\big|_{x=t - 2,\,y=2 - t}\\&=t - 2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(t - 2\right)\left(-1\right)\,\mathrm{d}t\\&=\int_{0}^{1}\left(2 - t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124272

Original

![](images/f5/f5f5b235b54d2acd20297ab365d9b93907111b3fec9a86776c28e93fdfe105ee.png)

Which of the following is equivalent to ${\int }_{C}({x}^{2}+{y}^{2})\,\text{d}y,$ where $C$ is the path along the line segment from the point $(0,0)$ to the point $(2,3),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨2t,\,3t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/1752cf569194577b45d683a9.png)

Which of the following is equivalent to $\int_C\left(x^{2} + y^{2}\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(0,0)$ to the point $(2,3)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 t,\,3 t\rangle$.*

- $13\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t$
- $13\int_{0}^{1}\left(3 t^{2} + 1\right)\,\mathrm{d}t$
- $9\int_{0}^{1}\left(3 - t^{2}\right)\,\mathrm{d}t$
- $26\int_{0}^{1}\left(3 t^{2} - 1\right)\,\mathrm{d}t$
- $39\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(0,0)$ and $(2,3)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle 0+t(2-(0)),\,0+t(3-(0))\rangle\\&=\langle 2 t,\,3 t\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(3 t\right)=3.
$$

Now, since $f(x,y)=x^{2} + y^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} + y^{2}\big|_{x=2 t,\,y=3 t}\\&=13 t^{2}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(13 t^{2}\right)\left(3\right)\,\mathrm{d}t\\&=39\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124283

Original

![](images/f8/f83043b44a8ad9181e66de57357397deb49c4b0e79b5e6e16330305a58391148.png)

Which of the following is equivalent to ${\int }_{C}xy\,\text{d}y,$ where $C$ is the path along a circle of radius $4,$ traversed from the point $(4,0)$ to the point $(-4,0),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨4\operatorname{cos}⁡t,\,4\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/66c5e66d4a0f0577864c95d2.png)

Which of the following is equivalent to $\int_C\left(x y\right)\,\mathrm{d}y$, where $C$ is the path along a circle of radius $4$, traversed counterclockwise from the point $(4,0)$ to the point $(-4,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 4 \cos t,\,4 \sin t\rangle$.*

- $32\int_{0}^{\pi}\left(\sin t \cos t\right)\,\mathrm{d}t$
- $64\int_{0}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t$
- $64\int_{0}^{\pi}\left(\sin t + \cos t\right)\,\mathrm{d}t$
- $16\int_{0}^{\pi}\left(\sin t + \cos^{2} t\right)\,\mathrm{d}t$
- $4\int_{0}^{\pi}\left(\sin^{2} t \cos t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a part-circle of radius $4$ centered at $O$.

$$
r(t)=\langle 4 \cos t,\,4 \sin t\rangle,\qquad 0\le t\le \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(4 \sin t\right)=4 \cos t.
$$

Now, since $f(x,y)=x y$, we obtain

$$
\begin{aligned}f(r(t))&=x y\big|_{x=4 \cos t,\,y=4 \sin t}\\&=16 \sin t \cos t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{\pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{\pi}\left(16 \sin t \cos t\right)\left(4 \cos t\right)\,\mathrm{d}t\\&=64\int_{0}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124279

Original

![](images/8d/8d55ece1948f9ecb7da7d489b86a297651a34f409f83ba2470f6dd06678a375e.png)

Which of the following is equivalent to ${\int }_{C}(x-y)\,\text{d}y,$ where $C$ is the path along a circle of radius $3,$ traversed from the point $(0,-3)$ to the point $(0,3),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨3\operatorname{cos}⁡t,\,3\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/c9c8b41466647bb060fbe1e4.png)

Which of the following is equivalent to $\int_C\left(x - y\right)\,\mathrm{d}y$, where $C$ is the path along a circle of radius $3$, traversed counterclockwise from the point $(0,-3)$ to the point $(0,3)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 3 \cos t,\,3 \sin t\rangle$.*

- $3\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos^{2} t\right)\,\mathrm{d}t$
- $9\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t$
- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t$
- $3\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \sin t\right)\,\mathrm{d}t$
- $9\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \sin^{2} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a part-circle of radius $3$ centered at $O$.

$$
r(t)=\langle 3 \cos t,\,3 \sin t\rangle,\qquad - \frac{\pi}{2}\le t\le \frac{\pi}{2}.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(3 \sin t\right)=3 \cos t.
$$

Now, since $f(x,y)=x - y$, we obtain

$$
\begin{aligned}f(r(t))&=x - y\big|_{x=3 \cos t,\,y=3 \sin t}\\&=- 3 \sin t + 3 \cos t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(- 3 \sin t + 3 \cos t\right)\left(3 \cos t\right)\,\mathrm{d}t\\&=9\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124287

Original

![](images/69/69a10b5524670d31cfc9f2982e37d58a5ee9ca39fe49f35b9dace011275a635a.png)

Which of the following is equivalent to ${\int }_{C}(9-{y}^{2})\,\text{d}y,$ where $C$ is the path along three-quarters of the ellipse $9{x}^{2}+{y}^{2}=9,$ traversed from the point $(0,3)$ to the point $(1,0),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨\operatorname{cos}⁡t,\,3\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/ee6eb206748068fb97870a54.png)

Which of the following is equivalent to $\int_C\left(9 - y^{2}\right)\,\mathrm{d}y$, where $C$ is the path along three-quarters of the ellipse $9x^2+1y^2=9$, traversed counterclockwise from the point $(0,3)$ to the point $(1,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle \cos t,\,3 \sin t\rangle$.*

- $9\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin^{2} t \cos t\right)\,\mathrm{d}t$
- $27\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t$
- $27\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{3} t\right)\,\mathrm{d}t$
- $18\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin^{3} t\right)\,\mathrm{d}t$
- $18\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{2} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ can be parameterized as

$$
r(t)=\langle \cos t,\,3 \sin t\rangle,\qquad \frac{\pi}{2}\le t\le 2 \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(3 \sin t\right)=3 \cos t.
$$

Now, since $f(x,y)=9 - y^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=9 - y^{2}\big|_{x=\cos t,\,y=3 \sin t}\\&=9 - 9 \sin^{2} t\\&=9(1-\sin^2 t)\\&=9\cos^2 t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\frac{\pi}{2}}^{2 \pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\frac{\pi}{2}}^{2 \pi}\left(9 - 9 \sin^{2} t\right)\left(3 \cos t\right)\,\mathrm{d}t\\&=27\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{3} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124277

Original

![](images/f5/f532544febd248846eede65941f4617d325d0f91fec291d2679ba28abb2fb8fc.png)

Which of the following is equivalent to ${\int }_{C}{x}^{2}y\,\text{d}y,$ where $C$ is the path along a circle of radius $2,$ traversed from the point $(-2,0)$ to the point $(0,-2),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨2\operatorname{cos}⁡t,\,2\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/3b66229b419f89715a278391.png)

Which of the following is equivalent to $\int_C\left(x^{2} y\right)\,\mathrm{d}y$, where $C$ is the path along a circle of radius $2$, traversed counterclockwise from the point $(-2,0)$ to the point $(0,-2)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 \cos t,\,2 \sin t\rangle$.*

- $16\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t$
- $4\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t + \cos^{2} t\right)\,\mathrm{d}t$
- $4\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin^{2} t \cos^{2} t\right)\,\mathrm{d}t$
- $8\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin^{2} t \cos^{2} t\right)\,\mathrm{d}t$
- $8\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a part-circle of radius $2$ centered at $O$.

$$
r(t)=\langle 2 \cos t,\,2 \sin t\rangle,\qquad \pi\le t\le \frac{3 \pi}{2}.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sin t\right)=2 \cos t.
$$

Now, since $f(x,y)=x^{2} y$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} y\big|_{x=2 \cos t,\,y=2 \sin t}\\&=8 \sin t \cos^{2} t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\pi}^{\frac{3 \pi}{2}} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\pi}^{\frac{3 \pi}{2}}\left(8 \sin t \cos^{2} t\right)\left(2 \cos t\right)\,\mathrm{d}t\\&=16\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124293

Original

![](images/4d/4d02a56e1f927ccf8bd76a6fcc46dec61259649176695912865dd050657ce7f0.png)

Which of the following is equivalent to ${\int }_{C}xy\,\text{d}y,$ where $C$ is the path along a quarter of the ellipse ${x}^{2}+4{y}^{2}=4,$ traversed from the point $(0,1)$ to the point $(-2,0),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨2\operatorname{cos}⁡t,\,\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/9f0cbf0d9bd13a108104d80a.png)

Which of the following is equivalent to $\int_C\left(x y\right)\,\mathrm{d}y$, where $C$ is the path along a quarter of the ellipse $1x^2+4y^2=4$, traversed counterclockwise from the point $(0,1)$ to the point $(-2,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 \cos t,\,\sin t\rangle$.*

- $\int_{\frac{\pi}{2}}^{\pi}\left(2 \sin t + \cos t\right)\,\mathrm{d}t$
- $4\int_{\frac{\pi}{2}}^{\pi}\left(\sin^{2} t \cos t\right)\,\mathrm{d}t$
- $2\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t$
- $2\int_{\frac{\pi}{2}}^{\pi}\left(\sin t + \cos^{2} t\right)\,\mathrm{d}t$
- $2\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ can be parameterized as

$$
r(t)=\langle 2 \cos t,\,\sin t\rangle,\qquad \frac{\pi}{2}\le t\le \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(\sin t\right)=\cos t.
$$

Now, since $f(x,y)=x y$, we obtain

$$
\begin{aligned}f(r(t))&=x y\big|_{x=2 \cos t,\,y=\sin t}\\&=2 \sin t \cos t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\frac{\pi}{2}}^{\pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\frac{\pi}{2}}^{\pi}\left(2 \sin t \cos t\right)\left(\cos t\right)\,\mathrm{d}t\\&=2\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## q-124298

Original

![](images/fd/fd1956c8291f1bcecd7d37082110861ed7265fa40f7f85cbc69221cfdc5bea2d.png)

Which of the following is equivalent to ${\int }_{C}(3{x}^{2}+{y}^{2})\,\text{d}y,$ where $C$ is the path along the ellipse $16{x}^{2}+4{y}^{2}=64,$ traversed from the point $(-2,0)$ to the point $(2,0),$ as shown above?

*Hint: Use the parametrization $r(t)=⟨2\operatorname{cos}⁡t,\,4\operatorname{sin}⁡t⟩.$*

Replay

![](generate/scratch/17592186133892/assets/223c85e2ae5e58615b247567.png)

Which of the following is equivalent to $\int_C\left(3 x^{2} + y^{2}\right)\,\mathrm{d}y$, where $C$ is the path along the ellipse $16x^2+4y^2=64$, traversed counterclockwise from the point $(-2,0)$ to the point $(2,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 \cos t,\,4 \sin t\rangle$.*

- $16\int_{\pi}^{2 \pi}\left(\left(3 \sin^{2} t + 1\right) \cos t\right)\,\mathrm{d}t$
- $8\int_{\pi}^{2 \pi}\left(\left(3 \sin^{2} t + 1\right) \sin t\right)\,\mathrm{d}t$
- $16\int_{\pi}^{2 \pi}\left(\left(\sin^{2} t + 3\right) \sin^{2} t\right)\,\mathrm{d}t$
- $16\int_{\pi}^{2 \pi}\left(\left(\sin^{2} t + 3\right) \cos t\right)\,\mathrm{d}t$
- $4\int_{\pi}^{2 \pi}\left(\left(\sin^{2} t + 3\right) \cos^{2} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ can be parameterized as

$$
r(t)=\langle 2 \cos t,\,4 \sin t\rangle,\qquad \pi\le t\le 2 \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(4 \sin t\right)=4 \cos t.
$$

Now, since $f(x,y)=3 x^{2} + y^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=3 x^{2} + y^{2}\big|_{x=2 \cos t,\,y=4 \sin t}\\&=16 \sin^{2} t + 12 \cos^{2} t\\&=4\sin^2 t+12(\sin^2 t+\cos^2 t)\\&=4(\sin^2 t+3).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\pi}^{2 \pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\pi}^{2 \pi}\left(16 \sin^{2} t + 12 \cos^{2} t\right)\left(4 \cos t\right)\,\mathrm{d}t\\&=16\int_{\pi}^{2 \pi}\left(\left(\sin^{2} t + 3\right) \cos t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124121 (k=2)

![](generate/scratch/17592186133892/assets/0c0f232d8965a8111933fdd9.png)

Which of the following is equivalent to $\int_C\left(x y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-2,-4)$ to the point $(4,8)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 6 t - 2,\,12 t - 4\rangle$.*

- $96\int_{0}^{1}\left(t^{2} - 6 t + 9\right)\,\mathrm{d}t$
- $96\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t$
- $144\int_{0}^{1}\left(t^{2} - 6 t + 9\right)\,\mathrm{d}t$
- $144\int_{0}^{1}\left(t^{2} + 6 t + 9\right)\,\mathrm{d}t$
- $48\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-2,-4)$ and $(4,8)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -2+t(4-(-2)),\,-4+t(8-(-4))\rangle\\&=\langle 6 t - 2,\,12 t - 4\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(12 t - 4\right)=12.
$$

Now, since $f(x,y)=x y$, we obtain

$$
\begin{aligned}f(r(t))&=x y\big|_{x=6 t - 2,\,y=12 t - 4}\\&=72 t^{2} - 48 t + 8.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(72 t^{2} - 48 t + 8\right)\left(12\right)\,\mathrm{d}t\\&=96\int_{0}^{1}\left(9 t^{2} - 6 t + 1\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124270 (k=2)

![](generate/scratch/17592186133892/assets/4287ba2e732444c068801ac9.png)

Which of the following is equivalent to $\int_C\left(x^{2} - y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-2,-4)$ to the point $(4,4)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 6 t - 2,\,8 t - 4\rangle$.*

- $144\int_{0}^{1}\left(2 t^{2} - t + 7\right)\,\mathrm{d}t$
- $16\int_{0}^{1}\left(18 t^{2} + t\right)\,\mathrm{d}t$
- $32\int_{0}^{1}\left(9 t^{2} - 8 t + 2\right)\,\mathrm{d}t$
- $48\int_{0}^{1}\left(6 t^{2} + 5\right)\,\mathrm{d}t$
- $96\int_{0}^{1}\left(2 t^{2} + 7 t + 1\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-2,-4)$ and $(4,4)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -2+t(4-(-2)),\,-4+t(4-(-4))\rangle\\&=\langle 6 t - 2,\,8 t - 4\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(8 t - 4\right)=8.
$$

Now, since $f(x,y)=x^{2} - y$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} - y\big|_{x=6 t - 2,\,y=8 t - 4}\\&=36 t^{2} - 32 t + 8.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(36 t^{2} - 32 t + 8\right)\left(8\right)\,\mathrm{d}t\\&=32\int_{0}^{1}\left(9 t^{2} - 8 t + 2\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124266 (k=2)

![](generate/scratch/17592186133892/assets/7c5278fd0f21cfb7dedc10d7.png)

Which of the following is equivalent to $\int_C\left(3 x + 2 y\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(-4,4)$ to the point $(-2,2)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 t - 4,\,4 - 2 t\rangle$.*

- $4\int_{0}^{1}\left(5 - 2 t\right)\,\mathrm{d}t$
- $4\int_{0}^{1}\left(2 - t\right)\,\mathrm{d}t$
- $4\int_{0}^{1}\left(3 t + 1\right)\,\mathrm{d}t$
- $4\int_{0}^{1}\left(t^{2} + 3 t - 1\right)\,\mathrm{d}t$
- $4\int_{0}^{1}\left(1 - t^{2}\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(-4,4)$ and $(-2,2)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle -4+t(-2-(-4)),\,4+t(2-(4))\rangle\\&=\langle 2 t - 4,\,4 - 2 t\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(4 - 2 t\right)=-2.
$$

Now, since $f(x,y)=3 x + 2 y$, we obtain

$$
\begin{aligned}f(r(t))&=3 x + 2 y\big|_{x=2 t - 4,\,y=4 - 2 t}\\&=2 t - 4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(2 t - 4\right)\left(-2\right)\,\mathrm{d}t\\&=4\int_{0}^{1}\left(2 - t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124272 (k=2)

![](generate/scratch/17592186133892/assets/edace9a2ccbacbf20cdf2e79.png)

Which of the following is equivalent to $\int_C\left(x^{2} + y^{2}\right)\,\mathrm{d}y$, where $C$ is the path along the line segment from the point $(0,0)$ to the point $(4,6)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 4 t,\,6 t\rangle$.*

- $104\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t$
- $104\int_{0}^{1}\left(3 t^{2} + 1\right)\,\mathrm{d}t$
- $72\int_{0}^{1}\left(3 - t^{2}\right)\,\mathrm{d}t$
- $208\int_{0}^{1}\left(3 t^{2} - 1\right)\,\mathrm{d}t$
- $312\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a line segment with endpoints $(0,0)$ and $(4,6)$. It can be parametrized as

$$
\begin{aligned}r(t)&=\langle 0+t(4-(0)),\,0+t(6-(0))\rangle\\&=\langle 4 t,\,6 t\rangle,\end{aligned}
$$

where $0\le t\le 1$.

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(6 t\right)=6.
$$

Now, since $f(x,y)=x^{2} + y^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} + y^{2}\big|_{x=4 t,\,y=6 t}\\&=52 t^{2}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{0}^{1} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{0}^{1}\left(52 t^{2}\right)\left(6\right)\,\mathrm{d}t\\&=312\int_{0}^{1}\left(t^{2}\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124279 (k=2)

![](generate/scratch/17592186133892/assets/eb42aa7d2ab09384dca6c197.png)

Which of the following is equivalent to $\int_C\left(x - y\right)\,\mathrm{d}y$, where $C$ is the path along a circle of radius $6$, traversed counterclockwise from the point $(0,-6)$ to the point $(0,6)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 6 \cos t,\,6 \sin t\rangle$.*

- $12\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos^{2} t\right)\,\mathrm{d}t$
- $36\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t$
- $4\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t$
- $12\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \sin t\right)\,\mathrm{d}t$
- $36\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \sin^{2} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a part-circle of radius $6$ centered at $O$.

$$
r(t)=\langle 6 \cos t,\,6 \sin t\rangle,\qquad - \frac{\pi}{2}\le t\le \frac{\pi}{2}.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(6 \sin t\right)=6 \cos t.
$$

Now, since $f(x,y)=x - y$, we obtain

$$
\begin{aligned}f(r(t))&=x - y\big|_{x=6 \cos t,\,y=6 \sin t}\\&=- 6 \sin t + 6 \cos t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(- 6 \sin t + 6 \cos t\right)\left(6 \cos t\right)\,\mathrm{d}t\\&=36\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\left(\left(- \sin t + \cos t\right) \cos t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124287 (k=2)

![](generate/scratch/17592186133892/assets/f604169d7971618d20f0a0bf.png)

Which of the following is equivalent to $\int_C\left(36 - y^{2}\right)\,\mathrm{d}y$, where $C$ is the path along three-quarters of the ellipse $36x^2+4y^2=144$, traversed counterclockwise from the point $(0,6)$ to the point $(2,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 2 \cos t,\,6 \sin t\rangle$.*

- $72\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin^{2} t \cos t\right)\,\mathrm{d}t$
- $216\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t$
- $216\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{3} t\right)\,\mathrm{d}t$
- $144\int_{\frac{\pi}{2}}^{2 \pi}\left(\sin^{3} t\right)\,\mathrm{d}t$
- $144\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{2} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ can be parameterized as

$$
r(t)=\langle 2 \cos t,\,6 \sin t\rangle,\qquad \frac{\pi}{2}\le t\le 2 \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(6 \sin t\right)=6 \cos t.
$$

Now, since $f(x,y)=36 - y^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=36 - y^{2}\big|_{x=2 \cos t,\,y=6 \sin t}\\&=36 - 36 \sin^{2} t\\&=36(1-\sin^2 t)\\&=36\cos^2 t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\frac{\pi}{2}}^{2 \pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\frac{\pi}{2}}^{2 \pi}\left(36 - 36 \sin^{2} t\right)\left(6 \cos t\right)\,\mathrm{d}t\\&=216\int_{\frac{\pi}{2}}^{2 \pi}\left(\cos^{3} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124277 (k=2)

![](generate/scratch/17592186133892/assets/c25676cfe5ec8add29aff816.png)

Which of the following is equivalent to $\int_C\left(x^{2} y\right)\,\mathrm{d}y$, where $C$ is the path along a circle of radius $4$, traversed counterclockwise from the point $(-4,0)$ to the point $(0,-4)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 4 \cos t,\,4 \sin t\rangle$.*

- $256\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t$
- $64\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t + \cos^{2} t\right)\,\mathrm{d}t$
- $64\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin^{2} t \cos^{2} t\right)\,\mathrm{d}t$
- $128\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin^{2} t \cos^{2} t\right)\,\mathrm{d}t$
- $128\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ is a part-circle of radius $4$ centered at $O$.

$$
r(t)=\langle 4 \cos t,\,4 \sin t\rangle,\qquad \pi\le t\le \frac{3 \pi}{2}.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(4 \sin t\right)=4 \cos t.
$$

Now, since $f(x,y)=x^{2} y$, we obtain

$$
\begin{aligned}f(r(t))&=x^{2} y\big|_{x=4 \cos t,\,y=4 \sin t}\\&=64 \sin t \cos^{2} t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\pi}^{\frac{3 \pi}{2}} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\pi}^{\frac{3 \pi}{2}}\left(64 \sin t \cos^{2} t\right)\left(4 \cos t\right)\,\mathrm{d}t\\&=256\int_{\pi}^{\frac{3 \pi}{2}}\left(\sin t \cos^{3} t\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Changed geometry q-124293 (k=2)

![](generate/scratch/17592186133892/assets/8a42e5649a142e3b712a5635.png)

Which of the following is equivalent to $\int_C\left(x y\right)\,\mathrm{d}y$, where $C$ is the path along a quarter of the ellipse $4x^2+16y^2=64$, traversed counterclockwise from the point $(0,2)$ to the point $(-4,0)$, as shown above?

*Hint: Use the parametrization $r(t)=\langle 4 \cos t,\,2 \sin t\rangle$.*

- $8\int_{\frac{\pi}{2}}^{\pi}\left(2 \sin t + \cos t\right)\,\mathrm{d}t$
- $32\int_{\frac{\pi}{2}}^{\pi}\left(\sin^{2} t \cos t\right)\,\mathrm{d}t$
- $16\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t$
- $16\int_{\frac{\pi}{2}}^{\pi}\left(\sin t + \cos^{2} t\right)\,\mathrm{d}t$
- $16\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos t\right)\,\mathrm{d}t$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}y=\int_a^b f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t.
$$

The curve $C$ can be parameterized as

$$
r(t)=\langle 4 \cos t,\,2 \sin t\rangle,\qquad \frac{\pi}{2}\le t\le \pi.
$$

Computing $\frac{\mathrm{d}y}{\mathrm{d}t}$, we get the following:

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sin t\right)=2 \cos t.
$$

Now, since $f(x,y)=x y$, we obtain

$$
\begin{aligned}f(r(t))&=x y\big|_{x=4 \cos t,\,y=2 \sin t}\\&=8 \sin t \cos t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}y&=\int_{\frac{\pi}{2}}^{\pi} f(r(t))\,\frac{\mathrm{d}y}{\mathrm{d}t}\,\mathrm{d}t\\&=\int_{\frac{\pi}{2}}^{\pi}\left(8 \sin t \cos t\right)\left(2 \cos t\right)\,\mathrm{d}t\\&=16\int_{\frac{\pi}{2}}^{\pi}\left(\sin t \cos^{2} t\right)\,\mathrm{d}t.\end{aligned}
$$