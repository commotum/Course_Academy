Find $y'$ for $y=\log(12 - x).$

First, we express $y$ as the composite function

$$
y=\log(u)=\log_{10}(u),\quad u=12 - x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-1.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (-1)\\ &=\frac{1}{(12 - x)\ln(10)}\cdot (-1)\\ &=- \frac{1}{12 - x}\frac{1}{\ln(10)}.\end{aligned}
$$

---

Given that $y=\log(x^{5}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$.

First, we express $y$ as the composite function

$$
y=\log(u),\quad u=x^{5}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5 x^{4}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (5 x^{4})\\ &=\frac{5 x^{4}}{(x^{5})\ln(10)}\\ &=\frac{\cancel{x^{4}}\cdot 5}{\cancel{x^{4}}\cdot x\ln(10)}\\ &=\frac{5}{x \ln{(10 )}}.\end{aligned}
$$

---

Given that $y=\log(\sqrt{6 x}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log(u),\quad u=\sqrt{6 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{6}{2\sqrt{6 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (\frac{6}{2\sqrt{6 x}})\\ &=\frac{1}{(\sqrt{6 x})\ln(10)}\cdot (\frac{6}{2\sqrt{6 x}})\\ &=\frac{6}{2(6 x)\ln(10)}\\ &=\frac{\cancel{6}}{2\cdot \cancel{6}x\ln(10)}\\ &=\frac{1}{2 x \ln{(10 )}}.\end{aligned}
$$
