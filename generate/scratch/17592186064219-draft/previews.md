Calculate $\int \frac{1}{1+11{x}^{2}}\,\text{d}x.$

- $\frac{\sqrt{11}}{11}\operatorname{arctan}⁡(x)+C$
- $\sqrt{11}\operatorname{arctan}⁡(\sqrt{11}x)+C$
- $11\operatorname{arctan}⁡(\sqrt{11}x)+C$
- $\operatorname{arctan}⁡(\frac{\sqrt{11}x}{11})+C$
- $\frac{\sqrt{11}}{11}\operatorname{arctan}⁡(\sqrt{11}x)+C$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $11{x}^{2}=(\sqrt{11}x)^{2}.$

So, let's substitute $u=\sqrt{11}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{11}\,⟹\,\text{d}x=\frac{1}{\sqrt{11}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{1+11{x}^{2}}\,\text{d}x & =\int \frac{1}{1+(\sqrt{11}x)^{2}}\text{d}x \\  & =\int \frac{1}{1+{u}^{2}}\cdot (\frac{1}{\sqrt{11}}\text{d}u) \\  & =\frac{1}{\sqrt{11}}\int \frac{1}{1+{u}^{2}}\text{d}u \\  & =\frac{\sqrt{11}}{11}\operatorname{arctan}⁡u+C \\  & =\frac{\sqrt{11}}{11}\operatorname{arctan}⁡(\sqrt{11}x)+C\end{aligned}\end{aligned}
$$

---

$\int \frac{1}{16+{x}^{2}}\,\text{d}x=$

- $\frac{1}{4}\operatorname{arctan}⁡(\frac{x}{4})+C$
- $\operatorname{arctan}⁡(\frac{x}{4})+C$
- $\frac{1}{4}\operatorname{arctan}⁡x+C$
- $\operatorname{arctan}⁡(4x)+C$
- $4\operatorname{arctan}⁡(4x)+C$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int \frac{1}{16+{x}^{2}}\,\text{d}x & =\int \frac{1}{16\cdot (1+{x}^{2}/16)}\,\text{d}x \\  & =\frac{1}{16}\int \frac{1}{1+{x}^{2}/16}\,\text{d}x \\  & =\frac{1}{16}\int \frac{1}{1+(x/4)^{2}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse tangent

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{4})}^{2}.$ 

So, let's substitute $u=\frac{x}{4}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4}\,⟹\,\text{d}x=4\,\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{16+{x}^{2}}\,\text{d}x & =\frac{1}{16}\int \frac{1}{1+(x/4)^{2}}\,\text{d}x \\  & =\frac{1}{16}\int \frac{1}{1+{u}^{2}}\cdot (4\,\text{d}u) \\  & =\frac{1}{4}\int \frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{1}{4}\operatorname{arctan}⁡u+C \\  & =\frac{1}{4}\operatorname{arctan}⁡(\frac{x}{4})+C\end{aligned}\end{aligned}
$$

---

Calculate $\int \frac{5}{8+72{x}^{2}}\,\text{d}x.$

- $\frac{5}{24}\operatorname{arctan}⁡(3x)+C$
- $\frac{5}{8}\operatorname{arctan}⁡(3x)+C$
- $\frac{5}{72}\operatorname{arctan}⁡(3x)+C$
- $\frac{5}{24}\operatorname{arctan}⁡(x)+C$
- $\frac{5}{24}\operatorname{arctan}⁡(\frac{x}{3})+C$

Note that we can rewrite this integral as

$$
\int \frac{5}{8+72{x}^{2}}\,\text{d}x=\frac{5}{8}\int\frac{1}{1+9{x}^{2}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse tangent,

$$
\int\frac{1}{1+u^2}\,\text{d}u=\operatorname{arctan}u+C.
$$

The only difference is that instead of $u^2$ as the variable, we have $9x^2=(3x)^2.$

So, let's substitute $u=3x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3\quad\Longrightarrow\quad\text{d}x=\frac{1}{3}\text{d}u.
$$

We can now write the integral in terms of $u,$ and evaluate:

$$
\begin{aligned}\int \frac{5}{8+72{x}^{2}}\,\text{d}x&=\frac{5}{8}\int\frac{1}{1+(3x)^2}\,\text{d}x\\&=\frac{5}{8}\int\frac{1}{1+u^2}\cdot\frac{1}{3}\,\text{d}u\\&=\frac{5}{24}\int\frac{1}{1+u^2}\,\text{d}u\\&=\frac{5}{24}\operatorname{arctan}u+C\\&=\frac{5}{24}\operatorname{arctan}⁡(3x)+C\end{aligned}
$$
