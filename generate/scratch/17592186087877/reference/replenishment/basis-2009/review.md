# Replenishment question review

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(3 x\right)\cdot y=x^{4}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{6 x}\right)\right)=\left(e^{6 x}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(x^{3}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(3\right)\cdot y=x^{3}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=3$ and $Q(x)=x^{3}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(3\right)\,dx} \\  & =e^{3 x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{3 x}$ as follows:

$$
\begin{aligned}\left(e^{3 x}\right)\cdot \left(\frac{dy}{dx}+\left(3\right)\cdot y\right) & =\left(e^{3 x}\right)\cdot \left(x^{3}\right) \\ \left(e^{3 x}\right)\cdot \frac{dy}{dx}+\left(3\right)\cdot \left(e^{3 x}\right)\cdot y & =\left(e^{3 x}\right)\cdot \left(x^{3}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right) & =\left(e^{3 x}\right)\cdot \left(x^{3}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+y=x^{2}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x^{2}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=x^{2}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(1\right)\,dx} \\  & =e^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x}$ as follows:

$$
\begin{aligned}\left(e^{x}\right)\cdot \left(\frac{dy}{dx}+y\right) & =\left(e^{x}\right)\cdot \left(x^{2}\right) \\ \left(e^{x}\right)\cdot \frac{dy}{dx}+\left(1\right)\cdot \left(e^{x}\right)\cdot y & =\left(e^{x}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right) & =\left(e^{x}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}-y=\cos{\left(3 x \right)}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(\cos{\left(3 x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=-1$ and $Q(x)=\cos{\left(3 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(-1\right)\,dx} \\  & =e^{- x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- x}$ as follows:

$$
\begin{aligned}\left(e^{- x}\right)\cdot \left(\frac{dy}{dx}-y\right) & =\left(e^{- x}\right)\cdot \left(\cos{\left(3 x \right)}\right) \\ \left(e^{- x}\right)\cdot \frac{dy}{dx}-\left(1\right)\cdot \left(e^{- x}\right)\cdot y & =\left(e^{- x}\right)\cdot \left(\cos{\left(3 x \right)}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right) & =\left(e^{- x}\right)\cdot \left(\cos{\left(3 x \right)}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(6 x\right)\cdot y=2 x e^{3 x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(2 x e^{3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right)=\left(e^{3 x^{2}}\right)\cdot \left(2 x e^{3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x^{2}}\right)\right)=\left(e^{- 3 x^{2}}\right)\cdot \left(2 x e^{3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{6 x}\right)\right)=\left(e^{6 x}\right)\cdot \left(2 x e^{3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(2 x e^{3 x^{2}}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=6 x$ and $Q(x)=2 x e^{3 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(6 x\right)\,dx} \\  & =e^{3 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{3 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{3 x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(6 x\right)\cdot y\right) & =\left(e^{3 x^{2}}\right)\cdot \left(2 x e^{3 x^{2}}\right) \\ \left(e^{3 x^{2}}\right)\cdot \frac{dy}{dx}+\left(6 x\right)\cdot \left(e^{3 x^{2}}\right)\cdot y & =\left(e^{3 x^{2}}\right)\cdot \left(2 x e^{3 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right) & =\left(e^{3 x^{2}}\right)\cdot \left(2 x e^{3 x^{2}}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(3\right)\cdot \frac{dy}{dx}+\left(18 x\right)\cdot y=3 x e^{- 3 x^{2}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(x e^{- 3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right)=\left(e^{3 x^{2}}\right)\cdot \left(x e^{- 3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x^{2}}\right)\right)=\left(e^{- 3 x^{2}}\right)\cdot \left(x e^{- 3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{6 x}\right)\right)=\left(e^{6 x}\right)\cdot \left(x e^{- 3 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x e^{- 3 x^{2}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(6 x\right)\cdot y=x e^{- 3 x^{2}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=6 x$ and $Q(x)=x e^{- 3 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(6 x\right)\,dx} \\  & =e^{3 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{3 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{3 x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(6 x\right)\cdot y\right) & =\left(e^{3 x^{2}}\right)\cdot \left(x e^{- 3 x^{2}}\right) \\ \left(e^{3 x^{2}}\right)\cdot \frac{dy}{dx}+\left(6 x\right)\cdot \left(e^{3 x^{2}}\right)\cdot y & =\left(e^{3 x^{2}}\right)\cdot \left(x e^{- 3 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right) & =\left(e^{3 x^{2}}\right)\cdot \left(x e^{- 3 x^{2}}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(3\right)\cdot \frac{dy}{dx}+\left(12 x\right)\cdot y=6 x e^{- 2 x^{2}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{4 x}\right)\right)=\left(e^{4 x}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right)=\left(e^{2 x^{2}}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(4 x\right)\cdot y=2 x e^{- 2 x^{2}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=4 x$ and $Q(x)=2 x e^{- 2 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(4 x\right)\,dx} \\  & =e^{2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{2 x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(4 x\right)\cdot y\right) & =\left(e^{2 x^{2}}\right)\cdot \left(2 x e^{- 2 x^{2}}\right) \\ \left(e^{2 x^{2}}\right)\cdot \frac{dy}{dx}+\left(4 x\right)\cdot \left(e^{2 x^{2}}\right)\cdot y & =\left(e^{2 x^{2}}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right) & =\left(e^{2 x^{2}}\right)\cdot \left(2 x e^{- 2 x^{2}}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(4\right)\cdot \frac{dy}{dx}+\left(12 x^{2}\right)\cdot y=- 8 x^{2} e^{- x^{3}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{x^{3}}\right)\right)=\left(e^{x^{3}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right)=\left(e^{3 x^{2}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x^{3}}\right)\right)=\left(e^{- x^{3}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(3 x^{2}\right)\cdot y=- 2 x^{2} e^{- x^{3}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=3 x^{2}$ and $Q(x)=- 2 x^{2} e^{- x^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(3 x^{2}\right)\,dx} \\  & =e^{x^{3}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{3}}$ as follows:

$$
\begin{aligned}\left(e^{x^{3}}\right)\cdot \left(\frac{dy}{dx}+\left(3 x^{2}\right)\cdot y\right) & =\left(e^{x^{3}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right) \\ \left(e^{x^{3}}\right)\cdot \frac{dy}{dx}+\left(3 x^{2}\right)\cdot \left(e^{x^{3}}\right)\cdot y & =\left(e^{x^{3}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{3}}\right)\right) & =\left(e^{x^{3}}\right)\cdot \left(- 2 x^{2} e^{- x^{3}}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(3\right)\cdot \frac{dy}{dx}-\left(12 x\right)\cdot y=3 x e^{2 x^{2}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right)=\left(e^{2 x^{2}}\right)\cdot \left(x e^{2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(x e^{2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 4 x}\right)\right)=\left(e^{- 4 x}\right)\cdot \left(x e^{2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x e^{2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(x e^{2 x^{2}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(4 x\right)\cdot y=x e^{2 x^{2}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- 4 x$ and $Q(x)=x e^{2 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- 4 x\right)\,dx} \\  & =e^{- 2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(4 x\right)\cdot y\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(x e^{2 x^{2}}\right) \\ \left(e^{- 2 x^{2}}\right)\cdot \frac{dy}{dx}-\left(4 x\right)\cdot \left(e^{- 2 x^{2}}\right)\cdot y & =\left(e^{- 2 x^{2}}\right)\cdot \left(x e^{2 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(x e^{2 x^{2}}\right)\end{aligned}
$$

---

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(4\right)\cdot \frac{dy}{dx}+\left(36 x^{2}\right)\cdot y=4 x^{2} e^{- 3 x^{3}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x^{3}}\right)\right)=\left(e^{- 3 x^{3}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{9 x^{2}}\right)\right)=\left(e^{9 x^{2}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x^{2}}\right)\right)=\left(e^{3 x^{2}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x^{3}}\right)\right)=\left(e^{3 x^{3}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(9 x^{2}\right)\cdot y=x^{2} e^{- 3 x^{3}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=9 x^{2}$ and $Q(x)=x^{2} e^{- 3 x^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(9 x^{2}\right)\,dx} \\  & =e^{3 x^{3}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{3 x^{3}}$ as follows:

$$
\begin{aligned}\left(e^{3 x^{3}}\right)\cdot \left(\frac{dy}{dx}+\left(9 x^{2}\right)\cdot y\right) & =\left(e^{3 x^{3}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right) \\ \left(e^{3 x^{3}}\right)\cdot \frac{dy}{dx}+\left(9 x^{2}\right)\cdot \left(e^{3 x^{3}}\right)\cdot y & =\left(e^{3 x^{3}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{3 x^{3}}\right)\right) & =\left(e^{3 x^{3}}\right)\cdot \left(x^{2} e^{- 3 x^{3}}\right)\end{aligned}
$$
