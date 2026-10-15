![](images/1b/1b693165c8f6201e96f0a972746324c65a308d1f143f229c465b6aa22b7aeb16.png)

Which of the following is equivalent to ${\int }_{C}5\left((x-y)\right)\,\text{d}x,$ where $C$ is the path along the ellipse $16{x}^{2}+25{y}^{2}=400,$ traversed from the point $(0,-4)$ to the point $(5,0),$ as shown above?
*Hint: Use the parametrization $r(t)=⟨5\operatorname{cos}⁡t,\,4\operatorname{sin}⁡t⟩.$*

- $5\left(4{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{cos}⁡t\,\text{d}t\right)$
- $5\left(-10{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{sin}⁡t\,\text{d}t\right)$
- $5\left(-10{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{cos}⁡t\,\text{d}t\right)$
- $5\left(4{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{sin}⁡t\,\text{d}t\right)$
- $5\left(-5{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{sin}⁡t\,\text{d}t\right)$ (correct)

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}x={\int }_{a}^{b}f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t.
$$

 

The curve $C$ can be parameterized as 

$$
r(t)=⟨5\operatorname{cos}⁡t,\,4\operatorname{sin}⁡t⟩,\,\frac{3\pi }{2}\le t\le 2\pi .
$$

Computing $\frac{\text{d}x}{\text{d}t},$ we get the following:

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(5\operatorname{cos}⁡t)=-5\operatorname{sin}⁡t\end{aligned}
$$

Now, since $f(x,y)=5\left(x-y\right)$ we obtain

$$
\begin{aligned}f(r(t)) & =5\left(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t\right)\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}x & ={\int }_{3\pi /2}^{2\pi }f(r(t))\,\frac{\text{d}x}{\text{d}t}\,\text{d}t \\  & =5\left({\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)(-5\operatorname{sin}⁡t)\,\text{d}t\right)\\  & =5\left(-5{\int }_{3\pi /2}^{2\pi }(5\operatorname{cos}⁡t-4\operatorname{sin}⁡t)\operatorname{sin}⁡t\,\text{d}t\right)\end{aligned}
$$