## q-17540 — original

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx} + y = \cos x$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(yx) = x\cos x$
- $\frac{d}{dx}(y\ln x) = \ln x\cos x$
- $\frac{d}{dx^{2}}(yx^{2}) = x^{2}\cos x$
- $\frac{d}{dx}(\frac{y}{x}) = \frac{\cos x}{x}$
- $\frac{d}{dx}(ye^{x}) = e^{x}\cos x$

No captured worked solution or correct reference.

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+y=\cos{\left(x \right)}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx^{2}}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x}\right)\right)=\left(\frac{1}{x}\right)\cdot \left(\cos{\left(x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=\cos{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(1\right)\,dx} \\  & =e^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x}$ as follows:

$$
\begin{aligned}\left(e^{x}\right)\cdot \left(\frac{dy}{dx}+y\right) & =\left(e^{x}\right)\cdot \left(\cos{\left(x \right)}\right) \\ \left(e^{x}\right)\cdot \frac{dy}{dx}+\left(1\right)\cdot \left(e^{x}\right)\cdot y & =\left(e^{x}\right)\cdot \left(\cos{\left(x \right)}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right) & =\left(e^{x}\right)\cdot \left(\cos{\left(x \right)}\right)\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(2\right)\cdot y=\cos{\left(3 x \right)}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x}\right)\right)=\left(\frac{1}{x}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx^{2}}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(\cos{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(3 x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2$ and $Q(x)=\cos{\left(3 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2\right)\,dx} \\  & =e^{2 x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{2 x}$ as follows:

$$
\begin{aligned}\left(e^{2 x}\right)\cdot \left(\frac{dy}{dx}+\left(2\right)\cdot y\right) & =\left(e^{2 x}\right)\cdot \left(\cos{\left(3 x \right)}\right) \\ \left(e^{2 x}\right)\cdot \frac{dy}{dx}+\left(2\right)\cdot \left(e^{2 x}\right)\cdot y & =\left(e^{2 x}\right)\cdot \left(\cos{\left(3 x \right)}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right) & =\left(e^{2 x}\right)\cdot \left(\cos{\left(3 x \right)}\right)\end{aligned}
$$

## q-8546 — original

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx} + 2xy = 2xe^{-x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(ye^{x}) = e^{x} \cdot 2xe^{-x^{2}}$
- $\frac{d}{dx}(y \cdot 2x) = 2x \cdot 2xe^{-x^{2}}$
- $\frac{d}{dx}(yx^{2}) = x^{2} \cdot 2xe^{-x^{2}}$
- $\frac{d}{dx}(ye^{x^{2}}) = e^{x^{2}} \cdot 2xe^{-x^{2}}$
- $\frac{d}{dx}(yx) = x \cdot 2xe^{-x^{2}}$

No captured worked solution or correct reference.

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(2 x\right)\cdot y=2 x e^{- x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(2 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(2 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(2 x\right)\right)=\left(2 x\right)\cdot \left(2 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(2 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(2 x e^{- x^{2}}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2 x$ and $Q(x)=2 x e^{- x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2 x\right)\,dx} \\  & =e^{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(2 x\right)\cdot y\right) & =\left(e^{x^{2}}\right)\cdot \left(2 x e^{- x^{2}}\right) \\ \left(e^{x^{2}}\right)\cdot \frac{dy}{dx}+\left(2 x\right)\cdot \left(e^{x^{2}}\right)\cdot y & =\left(e^{x^{2}}\right)\cdot \left(2 x e^{- x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right) & =\left(e^{x^{2}}\right)\cdot \left(2 x e^{- x^{2}}\right)\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(4 x\right)\cdot y=6 x e^{- 2 x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right)=\left(e^{2 x^{2}}\right)\cdot \left(6 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(4 x\right)\right)=\left(4 x\right)\cdot \left(6 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(6 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(6 x e^{- 2 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(6 x e^{- 2 x^{2}}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=4 x$ and $Q(x)=6 x e^{- 2 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(4 x\right)\,dx} \\  & =e^{2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{2 x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(4 x\right)\cdot y\right) & =\left(e^{2 x^{2}}\right)\cdot \left(6 x e^{- 2 x^{2}}\right) \\ \left(e^{2 x^{2}}\right)\cdot \frac{dy}{dx}+\left(4 x\right)\cdot \left(e^{2 x^{2}}\right)\cdot y & =\left(e^{2 x^{2}}\right)\cdot \left(6 x e^{- 2 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right) & =\left(e^{2 x^{2}}\right)\cdot \left(6 x e^{- 2 x^{2}}\right)\end{aligned}
$$

## q-17533 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
x\frac{dy}{dx}+xy={x}^{2}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(y\cdot 2x)=2x\cdot x$
- $\frac{d}{dx}(y{e}^{x})={e}^{x}\cdot x$
- $\frac{d}{dx}(y\cdot 2)=2x$
- $\frac{d}{dx}(y{e}^{2x})={e}^{2x}\cdot x$
- $\frac{d}{dx}(yx)=x\cdot x$

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+y=x.
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int 1\,dx} \\  & ={e}^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{x}$ as follows:

$$
\begin{aligned}{e}^{x}\cdot (\frac{dy}{dx}+y) & ={e}^{x}\cdot x \\ {e}^{x}\frac{dy}{dx}+{e}^{x}y & ={e}^{x}\cdot x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}(y{e}^{x}) & ={e}^{x}\cdot x\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(x\right)\cdot y=x^{2}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(2\right)\right)=\left(2\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(2 x\right)\right)=\left(2 x\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(x\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+y=x.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(1\right)\,dx} \\  & =e^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x}$ as follows:

$$
\begin{aligned}\left(e^{x}\right)\cdot \left(\frac{dy}{dx}+y\right) & =\left(e^{x}\right)\cdot \left(x\right) \\ \left(e^{x}\right)\cdot \frac{dy}{dx}+\left(1\right)\cdot \left(e^{x}\right)\cdot y & =\left(e^{x}\right)\cdot \left(x\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right) & =\left(e^{x}\right)\cdot \left(x\right)\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}-\left(\frac{2 x}{3}\right)\cdot y=x^{3}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{4 x}{3}}\right)\right)=\left(e^{- \frac{4 x}{3}}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{2 x}{3}}\right)\right)=\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(- \frac{4}{3}\right)\right)=\left(- \frac{4}{3}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(- \frac{2 x}{3}\right)\right)=\left(- \frac{2 x}{3}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(- \frac{4 x}{3}\right)\right)=\left(- \frac{4 x}{3}\right)\cdot \left(x^{2}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot y=x^{2}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{2}{3}$ and $Q(x)=x^{2}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{2}{3}\right)\,dx} \\  & =e^{- \frac{2 x}{3}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- \frac{2 x}{3}}$ as follows:

$$
\begin{aligned}\left(e^{- \frac{2 x}{3}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot y\right) & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right) \\ \left(e^{- \frac{2 x}{3}}\right)\cdot \frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot \left(e^{- \frac{2 x}{3}}\right)\cdot y & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- \frac{2 x}{3}}\right)\right) & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

## q-17539 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
{x}^{2}\frac{dy}{dx}+xy={x}^{2}\operatorname{cos}⁡x,\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(y{e}^{x})={e}^{x}\operatorname{cos}⁡x$
- $\frac{d}{dx}(y{x}^{2})={x}^{2}\operatorname{cos}⁡x$
- $\frac{d}{dx}(yx)=x\operatorname{cos}⁡x$
- $\frac{d}{dx}(y{e}^{-x})={e}^{-x}\operatorname{cos}⁡x$
- $\frac{d}{dx}(y\operatorname{ln}⁡x)=\operatorname{ln}⁡x\operatorname{cos}⁡x$

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\frac{1}{x}\cdot y=\operatorname{cos}⁡x.
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\operatorname{cos}⁡x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)dx} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x$ as follows:

$$
\begin{aligned}x\cdot (\frac{dy}{dx}+\frac{1}{x}\cdot y) & =x\cdot \operatorname{cos}⁡x \\ x\cdot \frac{dy}{dx}+y & =x\operatorname{cos}⁡x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}(yx) & =x\operatorname{cos}⁡x.\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x^{2}\right)\cdot \frac{dy}{dx}+\left(x\right)\cdot y=x^{2} \cos{\left(x \right)},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(\cos{\left(x \right)}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot y=\cos{\left(x \right)}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=\cos{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{1}{x}\right)\,dx} \\  & =e^{\ln{\left(x \right)}} \\  & =x\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x$ as follows:

$$
\begin{aligned}\left(x\right)\cdot \left(\frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot y\right) & =\left(x\right)\cdot \left(\cos{\left(x \right)}\right) \\ \left(x\right)\cdot \frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot \left(x\right)\cdot y & =x \cos{\left(x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x\right)\right) & =x \cos{\left(x \right)}.\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x^{2}\right)\cdot \frac{dy}{dx}+\left(3 x\right)\cdot y=x^{2} \cos{\left(2 x \right)},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(\cos{\left(2 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{6}\right)\right)=\left(x^{6}\right)\cdot \left(\cos{\left(2 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(\cos{\left(2 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(2 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(\cos{\left(2 x \right)}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=\cos{\left(2 x \right)}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\cos{\left(2 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(\cos{\left(2 x \right)}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =x^{3} \cos{\left(2 x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =x^{3} \cos{\left(2 x \right)}.\end{aligned}
$$

## q-335278 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\frac{1}{2}y={x}^{3}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(y{e}^{-x/2})={e}^{-x/2}\cdot {x}^{3}$
- $\frac{d}{dx}(y{e}^{x/2})={e}^{x/2}\cdot {x}^{3}$
- $\frac{d}{dx}(y\cdot (-\frac{x}{2}))=-\frac{x}{2}\cdot {x}^{3}$
- $\frac{d}{dx}(y\cdot (-\frac{1}{2}))=-\frac{1}{2}\cdot {x}^{3}$
- $\frac{d}{dx}(y\cdot 2)=2{x}^{3}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-\frac{1}{2}$ and $Q(x)={x}^{3}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (-1/2)\,dx} \\  & ={e}^{-x/2}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-x/2}$ as follows:

$$
\begin{aligned}{e}^{-x/2}\cdot (\frac{dy}{dx}-\frac{1}{2}y) & ={e}^{-x/2}\cdot {x}^{3} \\ {e}^{-x/2}\cdot \frac{dy}{dx}+\frac{1}{2}{e}^{-x/2}\cdot y & ={e}^{-x/2}\cdot {x}^{3}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}(y{e}^{-x/2}) & ={e}^{-x/2}\cdot {x}^{3}\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(\frac{1}{2}\right)\cdot y=x^{3}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(- \frac{x}{2}\right)\right)=\left(- \frac{x}{2}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{x}{2}}\right)\right)=\left(e^{- \frac{x}{2}}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{\frac{x}{2}}\right)\right)=\left(e^{\frac{x}{2}}\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(2\right)\right)=\left(2\right)\cdot \left(x^{3}\right)$
- $\frac{d}{dx}\left(y\cdot \left(- \frac{1}{2}\right)\right)=\left(- \frac{1}{2}\right)\cdot \left(x^{3}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{1}{2}$ and $Q(x)=x^{3}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{1}{2}\right)\,dx} \\  & =e^{- \frac{x}{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- \frac{x}{2}}$ as follows:

$$
\begin{aligned}\left(e^{- \frac{x}{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{1}{2}\right)\cdot y\right) & =\left(e^{- \frac{x}{2}}\right)\cdot \left(x^{3}\right) \\ \left(e^{- \frac{x}{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{1}{2}\right)\cdot \left(e^{- \frac{x}{2}}\right)\cdot y & =\left(e^{- \frac{x}{2}}\right)\cdot \left(x^{3}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- \frac{x}{2}}\right)\right) & =\left(e^{- \frac{x}{2}}\right)\cdot \left(x^{3}\right)\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot y=x^{2}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(- \frac{2}{3}\right)\right)=\left(- \frac{2}{3}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{\frac{2 x}{3}}\right)\right)=\left(e^{\frac{2 x}{3}}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(- \frac{2 x}{3}\right)\right)=\left(- \frac{2 x}{3}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{3}{2}\right)\right)=\left(\frac{3}{2}\right)\cdot \left(x^{2}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{2 x}{3}}\right)\right)=\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{2}{3}$ and $Q(x)=x^{2}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{2}{3}\right)\,dx} \\  & =e^{- \frac{2 x}{3}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- \frac{2 x}{3}}$ as follows:

$$
\begin{aligned}\left(e^{- \frac{2 x}{3}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot y\right) & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right) \\ \left(e^{- \frac{2 x}{3}}\right)\cdot \frac{dy}{dx}-\left(\frac{2}{3}\right)\cdot \left(e^{- \frac{2 x}{3}}\right)\cdot y & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- \frac{2 x}{3}}\right)\right) & =\left(e^{- \frac{2 x}{3}}\right)\cdot \left(x^{2}\right)\end{aligned}
$$

## q-79818 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{x}\cdot y={e}^{x},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{\text{d}}{\text{d}x}(y{x}^{2})={x}^{2}{e}^{x}$
- $\frac{\text{d}}{\text{d}x}(y{e}^{x})={e}^{x}{e}^{x}$
- $\frac{\text{d}}{\text{d}x}(y{e}^{-x})={e}^{-x}{e}^{x}$
- $\frac{\text{d}}{\text{d}x}(yx)=x{e}^{x}$
- $\frac{\text{d}}{\text{d}x}(y\operatorname{ln}⁡x)=\operatorname{ln}⁡x\cdot {e}^{x}$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)={e}^{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (1/x)\,\text{d}x} \\  & ={e}^{\operatorname{ln}⁡x} \\  & =x\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x$ as follows:

$$
\begin{aligned}x\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{x}\cdot y) & =x\cdot {e}^{x} \\ x\cdot \frac{\text{d}y}{\text{d}x}+y & =x{e}^{x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(yx) & =x{e}^{x}\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot y=e^{x},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(e^{x}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{x}$ and $Q(x)=e^{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{1}{x}\right)\,dx} \\  & =e^{\ln{\left(x \right)}} \\  & =x\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x$ as follows:

$$
\begin{aligned}\left(x\right)\cdot \left(\frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot y\right) & =\left(x\right)\cdot \left(e^{x}\right) \\ \left(x\right)\cdot \frac{dy}{dx}+\left(\frac{1}{x}\right)\cdot \left(x\right)\cdot y & =x e^{x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x\right)\right) & =x e^{x}\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=e^{2 x},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(e^{2 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(e^{2 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(e^{2 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(e^{2 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{6}\right)\right)=\left(x^{6}\right)\cdot \left(e^{2 x}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=e^{2 x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(e^{2 x}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =x^{3} e^{2 x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =x^{3} e^{2 x}\end{aligned}
$$

## q-79819 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
x\cdot \frac{\text{d}y}{\text{d}x}+2y=1
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{\text{d}}{\text{d}x}(y\operatorname{ln}⁡x)=\operatorname{ln}⁡x\cdot \frac{1}{x}$
- $\frac{\text{d}}{\text{d}x}(y{x}^{2})={x}^{2}\cdot \frac{1}{x}$
- $\frac{\text{d}}{\text{d}x}(y{e}^{x})={e}^{x}\cdot \frac{1}{x}$
- $\frac{\text{d}}{\text{d}x}(yx)=x\cdot \frac{1}{x}$
- $\frac{\text{d}}{\text{d}x}(y\cdot 2)=2\cdot \frac{1}{x}$

First, we write the equation in standard form. This gives

$$
\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y=\frac{1}{x}.
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{1}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{2})} \\  & ={x}^{2}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{2}$ as follows:

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}\cdot y) & ={x}^{2}\cdot \frac{1}{x} \\ {x}^{2}\cdot \frac{\text{d}y}{\text{d}x}+2xy & ={x}^{2}\cdot \frac{1}{x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{2}) & ={x}^{2}\cdot \frac{1}{x}\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(2\right)\cdot y=1
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(\frac{1}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\frac{1}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\frac{1}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(2\right)\right)=\left(2\right)\cdot \left(\frac{1}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\frac{1}{x}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{2}{x}\right)\cdot y=\frac{1}{x}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{1}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{2}{x}\right)\,dx} \\  & =e^{2 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{2}\right)} \\  & =x^{2}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{2}$ as follows:

$$
\begin{aligned}\left(x^{2}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{2}{x}\right)\cdot y\right) & =\left(x^{2}\right)\cdot \left(\frac{1}{x}\right) \\ \left(x^{2}\right)\cdot \frac{dy}{dx}+\left(\frac{2}{x}\right)\cdot \left(x^{2}\right)\cdot y & =\left(x^{2}\right)\cdot \left(\frac{1}{x}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right) & =\left(x^{2}\right)\cdot \left(\frac{1}{x}\right)\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(3\right)\cdot y=2
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(x^{\frac{3}{2}}\right)\right)=\left(x^{\frac{3}{2}}\right)\cdot \left(\frac{2}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(\frac{2}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{\frac{3 x}{2}}\right)\right)=\left(e^{\frac{3 x}{2}}\right)\cdot \left(\frac{2}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(3\right)\right)=\left(3\right)\cdot \left(\frac{2}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\frac{2}{x}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=\frac{2}{x}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{2}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(\frac{2}{x}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =\left(x^{3}\right)\cdot \left(\frac{2}{x}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =\left(x^{3}\right)\cdot \left(\frac{2}{x}\right)\end{aligned}
$$

## q-335274 — original

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+2xy=\operatorname{sin}⁡x
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}(y\operatorname{ln}⁡|2x|)=\operatorname{ln}⁡|2x|\operatorname{sin}⁡x$
- $\frac{d}{dx}(y{x}^{2})={x}^{2}\operatorname{sin}⁡x$
- $\frac{d}{dx}(y{e}^{2x})={e}^{2x}\operatorname{sin}⁡x$
- $\frac{d}{dx}(y\cdot 2x)=2x\operatorname{sin}⁡x$
- $\frac{d}{dx}(y{e}^{{x}^{2}})={e}^{{x}^{2}}\operatorname{sin}⁡x$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=2x$ and $Q(x)=\operatorname{sin}⁡x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int 2x\,dx} \\  & ={e}^{{x}^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{{x}^{2}}$ as follows:

$$
\begin{aligned}{e}^{{x}^{2}}\cdot (\frac{dy}{dx}+2xy) & ={e}^{{x}^{2}}\cdot \operatorname{sin}⁡x \\ {e}^{{x}^{2}}\cdot \frac{dy}{dx}+2x{e}^{{x}^{2}}\cdot y & ={e}^{{x}^{2}}\operatorname{sin}⁡x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}(y{e}^{{x}^{2}}) & ={e}^{{x}^{2}}\operatorname{sin}⁡x\end{aligned}
$$

### Parameterized raw-bank replay (normal API)

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+\left(2 x\right)\cdot y=\sin{\left(x \right)}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(2 x \right)}\right)\right)=\left(\ln{\left(2 x \right)}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(2 x\right)\right)=\left(2 x\right)\cdot \left(\sin{\left(x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2 x$ and $Q(x)=\sin{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2 x\right)\,dx} \\  & =e^{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(2 x\right)\cdot y\right) & =\left(e^{x^{2}}\right)\cdot \left(\sin{\left(x \right)}\right) \\ \left(e^{x^{2}}\right)\cdot \frac{dy}{dx}+\left(2 x\right)\cdot \left(e^{x^{2}}\right)\cdot y & =e^{x^{2}} \sin{\left(x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right) & =e^{x^{2}} \sin{\left(x \right)}\end{aligned}
$$

### Generated variant of this complete observed bank

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(4 x\right)\cdot y=\sin{\left(3 x \right)}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(- 4 x\right)\right)=\left(- 4 x\right)\cdot \left(\sin{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\sin{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 4 x}\right)\right)=\left(e^{- 4 x}\right)\cdot \left(\sin{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(\sin{\left(3 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(4 x \right)}\right)\right)=\left(\ln{\left(4 x \right)}\right)\cdot \left(\sin{\left(3 x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- 4 x$ and $Q(x)=\sin{\left(3 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- 4 x\right)\,dx} \\  & =e^{- 2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(4 x\right)\cdot y\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(\sin{\left(3 x \right)}\right) \\ \left(e^{- 2 x^{2}}\right)\cdot \frac{dy}{dx}-\left(4 x\right)\cdot \left(e^{- 2 x^{2}}\right)\cdot y & =e^{- 2 x^{2}} \sin{\left(3 x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right) & =e^{- 2 x^{2}} \sin{\left(3 x \right)}\end{aligned}
$$

## easy generated authored-bank constant_cos seed 0

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(3\right)\cdot y=\cos{\left(4 x \right)}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{6 x}\right)\right)=\left(e^{6 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=3$ and $Q(x)=\cos{\left(4 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(3\right)\,dx} \\  & =e^{3 x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{3 x}$ as follows:

$$
\begin{aligned}\left(e^{3 x}\right)\cdot \left(\frac{dy}{dx}+\left(3\right)\cdot y\right) & =\left(e^{3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right) \\ \left(e^{3 x}\right)\cdot \frac{dy}{dx}+\left(3\right)\cdot \left(e^{3 x}\right)\cdot y & =\left(e^{3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right) & =\left(e^{3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)\end{aligned}
$$

## easy generated authored-bank constant_cos seed 1

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}-\left(2\right)\cdot y=\cos{\left(x \right)}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 4 x}\right)\right)=\left(e^{- 4 x}\right)\cdot \left(\cos{\left(x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=-2$ and $Q(x)=\cos{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(-2\right)\,dx} \\  & =e^{- 2 x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x}\right)\cdot \left(\frac{dy}{dx}-\left(2\right)\cdot y\right) & =\left(e^{- 2 x}\right)\cdot \left(\cos{\left(x \right)}\right) \\ \left(e^{- 2 x}\right)\cdot \frac{dy}{dx}-\left(2\right)\cdot \left(e^{- 2 x}\right)\cdot y & =\left(e^{- 2 x}\right)\cdot \left(\cos{\left(x \right)}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right) & =\left(e^{- 2 x}\right)\cdot \left(\cos{\left(x \right)}\right)\end{aligned}
$$

## easy generated authored-bank scaled_constant_power seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(x\right)\cdot y=x^{5}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(x^{4}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+y=x^{4}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=x^{4}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(1\right)\,dx} \\  & =e^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x}$ as follows:

$$
\begin{aligned}\left(e^{x}\right)\cdot \left(\frac{dy}{dx}+y\right) & =\left(e^{x}\right)\cdot \left(x^{4}\right) \\ \left(e^{x}\right)\cdot \frac{dy}{dx}+\left(1\right)\cdot \left(e^{x}\right)\cdot y & =\left(e^{x}\right)\cdot \left(x^{4}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right) & =\left(e^{x}\right)\cdot \left(x^{4}\right)\end{aligned}
$$

## easy generated authored-bank scaled_constant_power seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}-\left(\frac{3 x}{2}\right)\cdot y=x^{2}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{\frac{3 x}{2}}\right)\right)=\left(e^{\frac{3 x}{2}}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{3 x}{2}}\right)\right)=\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(x\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot y=x.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{3}{2}$ and $Q(x)=x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{3}{2}\right)\,dx} \\  & =e^{- \frac{3 x}{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- \frac{3 x}{2}}$ as follows:

$$
\begin{aligned}\left(e^{- \frac{3 x}{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot y\right) & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right) \\ \left(e^{- \frac{3 x}{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot \left(e^{- \frac{3 x}{2}}\right)\cdot y & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- \frac{3 x}{2}}\right)\right) & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)\end{aligned}
$$

## easy generated authored-bank signed_constant_power seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+y=x^{4}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x}\right)\right)=\left(e^{- x}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(x^{4}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(x^{4}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=1$ and $Q(x)=x^{4}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(1\right)\,dx} \\  & =e^{x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x}$ as follows:

$$
\begin{aligned}\left(e^{x}\right)\cdot \left(\frac{dy}{dx}+y\right) & =\left(e^{x}\right)\cdot \left(x^{4}\right) \\ \left(e^{x}\right)\cdot \frac{dy}{dx}+\left(1\right)\cdot \left(e^{x}\right)\cdot y & =\left(e^{x}\right)\cdot \left(x^{4}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right) & =\left(e^{x}\right)\cdot \left(x^{4}\right)\end{aligned}
$$

## easy generated authored-bank signed_constant_power seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot y=x
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x\right)\right)=\left(x\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{\frac{3 x}{2}}\right)\right)=\left(e^{\frac{3 x}{2}}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- \frac{3 x}{2}}\right)\right)=\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(x\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{3}{2}$ and $Q(x)=x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{3}{2}\right)\,dx} \\  & =e^{- \frac{3 x}{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- \frac{3 x}{2}}$ as follows:

$$
\begin{aligned}\left(e^{- \frac{3 x}{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot y\right) & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right) \\ \left(e^{- \frac{3 x}{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{3}{2}\right)\cdot \left(e^{- \frac{3 x}{2}}\right)\cdot y & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- \frac{3 x}{2}}\right)\right) & =\left(e^{- \frac{3 x}{2}}\right)\cdot \left(x\right)\end{aligned}
$$

## moderate generated authored-bank linear_exp seed 0

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}+\left(2 x\right)\cdot y=6 x e^{4 x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(6 x e^{4 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(6 x e^{4 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x^{2}}\right)\right)=\left(e^{- x^{2}}\right)\cdot \left(6 x e^{4 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(6 x e^{4 x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(6 x e^{4 x^{2}}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2 x$ and $Q(x)=6 x e^{4 x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2 x\right)\,dx} \\  & =e^{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(2 x\right)\cdot y\right) & =\left(e^{x^{2}}\right)\cdot \left(6 x e^{4 x^{2}}\right) \\ \left(e^{x^{2}}\right)\cdot \frac{dy}{dx}+\left(2 x\right)\cdot \left(e^{x^{2}}\right)\cdot y & =\left(e^{x^{2}}\right)\cdot \left(6 x e^{4 x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right) & =\left(e^{x^{2}}\right)\cdot \left(6 x e^{4 x^{2}}\right)\end{aligned}
$$

## moderate generated authored-bank linear_exp seed 1

Consider the following first-order linear ODE for the function $y = y(x)$:
$\frac{dy}{dx}-\left(4 x\right)\cdot y=- 6 x e^{- x^{2}}$
Write the equation in the form $\frac{d}{dx}(yI(x)) = I(x)Q(x)$, where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(- 6 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 4 x}\right)\right)=\left(e^{- 4 x}\right)\cdot \left(- 6 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x^{2}}\right)\right)=\left(e^{2 x^{2}}\right)\cdot \left(- 6 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(- 6 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(- 6 x e^{- x^{2}}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- 4 x$ and $Q(x)=- 6 x e^{- x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- 4 x\right)\,dx} \\  & =e^{- 2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(4 x\right)\cdot y\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(- 6 x e^{- x^{2}}\right) \\ \left(e^{- 2 x^{2}}\right)\cdot \frac{dy}{dx}-\left(4 x\right)\cdot \left(e^{- 2 x^{2}}\right)\cdot y & =\left(e^{- 2 x^{2}}\right)\cdot \left(- 6 x e^{- x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(- 6 x e^{- x^{2}}\right)\end{aligned}
$$

## moderate generated authored-bank scaled_reciprocal_cos seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x^{2}\right)\cdot \frac{dy}{dx}+\left(3 x\right)\cdot y=x^{2} \cos{\left(4 x \right)},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{4}\right)\right)=\left(x^{4}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(\cos{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(\cos{\left(4 x \right)}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=\cos{\left(4 x \right)}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\cos{\left(4 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(\cos{\left(4 x \right)}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =x^{3} \cos{\left(4 x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =x^{3} \cos{\left(4 x \right)}.\end{aligned}
$$

## moderate generated authored-bank scaled_reciprocal_cos seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x^{2}\right)\cdot \frac{dy}{dx}-\left(2 x\right)\cdot y=x^{2} \cos{\left(x \right)},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x}\right)\right)=\left(\frac{1}{x}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right)=\left(\frac{1}{x^{2}}\right)\cdot \left(\cos{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(\cos{\left(x \right)}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y=\cos{\left(x \right)}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{2}{x}$ and $Q(x)=\cos{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{2}{x}\right)\,dx} \\  & =e^{- 2 \ln{\left(x \right)}} \\  & =e^{\ln \left(\frac{1}{x^{2}}\right)} \\  & =\frac{1}{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=\frac{1}{x^{2}}$ as follows:

$$
\begin{aligned}\left(\frac{1}{x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y\right) & =\left(\frac{1}{x^{2}}\right)\cdot \left(\cos{\left(x \right)}\right) \\ \left(\frac{1}{x^{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot \left(\frac{1}{x^{2}}\right)\cdot y & =\frac{\cos{\left(x \right)}}{x^{2}}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right) & =\frac{\cos{\left(x \right)}}{x^{2}}.\end{aligned}
$$

## moderate generated authored-bank reciprocal_exp seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=e^{4 x},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(e^{4 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{4}\right)\right)=\left(x^{4}\right)\cdot \left(e^{4 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(e^{4 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(e^{4 x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(e^{4 x}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=e^{4 x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(e^{4 x}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =x^{3} e^{4 x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =x^{3} e^{4 x}\end{aligned}
$$

## moderate generated authored-bank reciprocal_exp seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y=e^{x},\,x>0
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x}\right)\right)=\left(\frac{1}{x}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right)=\left(\frac{1}{x^{2}}\right)\cdot \left(e^{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(e^{x}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{2}{x}$ and $Q(x)=e^{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{2}{x}\right)\,dx} \\  & =e^{- 2 \ln{\left(x \right)}} \\  & =e^{\ln \left(\frac{1}{x^{2}}\right)} \\  & =\frac{1}{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=\frac{1}{x^{2}}$ as follows:

$$
\begin{aligned}\left(\frac{1}{x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y\right) & =\left(\frac{1}{x^{2}}\right)\cdot \left(e^{x}\right) \\ \left(\frac{1}{x^{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot \left(\frac{1}{x^{2}}\right)\cdot y & =\frac{e^{x}}{x^{2}}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right) & =\frac{e^{x}}{x^{2}}\end{aligned}
$$

## moderate generated authored-bank scaled_reciprocal_rhs seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}+\left(3\right)\cdot y=3
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(\frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{4}\right)\right)=\left(x^{4}\right)\cdot \left(\frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 3 x}\right)\right)=\left(e^{- 3 x}\right)\cdot \left(\frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{3 x}\right)\right)=\left(e^{3 x}\right)\cdot \left(\frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(\frac{3}{x}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y=\frac{3}{x}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{3}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(\frac{3}{x}\right)\,dx} \\  & =e^{3 \ln{\left(x \right)}} \\  & =e^{\ln \left(x^{3}\right)} \\  & =x^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=x^{3}$ as follows:

$$
\begin{aligned}\left(x^{3}\right)\cdot \left(\frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot y\right) & =\left(x^{3}\right)\cdot \left(\frac{3}{x}\right) \\ \left(x^{3}\right)\cdot \frac{dy}{dx}+\left(\frac{3}{x}\right)\cdot \left(x^{3}\right)\cdot y & =\left(x^{3}\right)\cdot \left(\frac{3}{x}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right) & =\left(x^{3}\right)\cdot \left(\frac{3}{x}\right)\end{aligned}
$$

## moderate generated authored-bank scaled_reciprocal_rhs seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(x\right)\cdot \frac{dy}{dx}-\left(2\right)\cdot y=-3
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(- \frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(x \right)}\right)\right)=\left(\ln{\left(x \right)}\right)\cdot \left(- \frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x}\right)\right)=\left(\frac{1}{x}\right)\cdot \left(- \frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right)=\left(\frac{1}{x^{2}}\right)\cdot \left(- \frac{3}{x}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x}\right)\right)=\left(e^{- 2 x}\right)\cdot \left(- \frac{3}{x}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y=- \frac{3}{x}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- \frac{2}{x}$ and $Q(x)=- \frac{3}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- \frac{2}{x}\right)\,dx} \\  & =e^{- 2 \ln{\left(x \right)}} \\  & =e^{\ln \left(\frac{1}{x^{2}}\right)} \\  & =\frac{1}{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=\frac{1}{x^{2}}$ as follows:

$$
\begin{aligned}\left(\frac{1}{x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot y\right) & =\left(\frac{1}{x^{2}}\right)\cdot \left(- \frac{3}{x}\right) \\ \left(\frac{1}{x^{2}}\right)\cdot \frac{dy}{dx}-\left(\frac{2}{x}\right)\cdot \left(\frac{1}{x^{2}}\right)\cdot y & =\left(\frac{1}{x^{2}}\right)\cdot \left(- \frac{3}{x}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(\frac{1}{x^{2}}\right)\right) & =\left(\frac{1}{x^{2}}\right)\cdot \left(- \frac{3}{x}\right)\end{aligned}
$$

## moderate generated authored-bank linear_sin seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}+\left(2 x\right)\cdot y=\sin{\left(4 x \right)}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(\sin{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\sin{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(2 x\right)\right)=\left(2 x\right)\cdot \left(\sin{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(\sin{\left(4 x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(2 x \right)}\right)\right)=\left(\ln{\left(2 x \right)}\right)\cdot \left(\sin{\left(4 x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2 x$ and $Q(x)=\sin{\left(4 x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2 x\right)\,dx} \\  & =e^{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(2 x\right)\cdot y\right) & =\left(e^{x^{2}}\right)\cdot \left(\sin{\left(4 x \right)}\right) \\ \left(e^{x^{2}}\right)\cdot \frac{dy}{dx}+\left(2 x\right)\cdot \left(e^{x^{2}}\right)\cdot y & =e^{x^{2}} \sin{\left(4 x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right) & =e^{x^{2}} \sin{\left(4 x \right)}\end{aligned}
$$

## moderate generated authored-bank linear_sin seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\frac{dy}{dx}-\left(4 x\right)\cdot y=\sin{\left(x \right)}
$$

Write the equation in the form $\frac{\text{d}}{\text{d}x}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

Assume $x>0$.

- $\frac{d}{dx}\left(y\cdot \left(- 4 x\right)\right)=\left(- 4 x\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(\ln{\left(4 x \right)}\right)\right)=\left(\ln{\left(4 x \right)}\right)\cdot \left(\sin{\left(x \right)}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 4 x}\right)\right)=\left(e^{- 4 x}\right)\cdot \left(\sin{\left(x \right)}\right)$

Worked solution:

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- 4 x$ and $Q(x)=\sin{\left(x \right)}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- 4 x\right)\,dx} \\  & =e^{- 2 x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x^{2}}\right)\cdot \left(\frac{dy}{dx}-\left(4 x\right)\cdot y\right) & =\left(e^{- 2 x^{2}}\right)\cdot \left(\sin{\left(x \right)}\right) \\ \left(e^{- 2 x^{2}}\right)\cdot \frac{dy}{dx}-\left(4 x\right)\cdot \left(e^{- 2 x^{2}}\right)\cdot y & =e^{- 2 x^{2}} \sin{\left(x \right)}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$ 

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right) & =e^{- 2 x^{2}} \sin{\left(x \right)}\end{aligned}
$$

## hard generated authored-bank polynomial_transform seed 0

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(3\right)\cdot \frac{dy}{dx}+\left(6 x\right)\cdot y=9 x e^{- x^{2}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right)=\left(e^{x^{2}}\right)\cdot \left(3 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x}\right)\right)=\left(e^{2 x}\right)\cdot \left(3 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- x^{2}}\right)\right)=\left(e^{- x^{2}}\right)\cdot \left(3 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{x}\right)\right)=\left(e^{x}\right)\cdot \left(3 x e^{- x^{2}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{2}\right)\right)=\left(x^{2}\right)\cdot \left(3 x e^{- x^{2}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}+\left(2 x\right)\cdot y=3 x e^{- x^{2}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=2 x$ and $Q(x)=3 x e^{- x^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(2 x\right)\,dx} \\  & =e^{x^{2}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{x^{2}}$ as follows:

$$
\begin{aligned}\left(e^{x^{2}}\right)\cdot \left(\frac{dy}{dx}+\left(2 x\right)\cdot y\right) & =\left(e^{x^{2}}\right)\cdot \left(3 x e^{- x^{2}}\right) \\ \left(e^{x^{2}}\right)\cdot \frac{dy}{dx}+\left(2 x\right)\cdot \left(e^{x^{2}}\right)\cdot y & =\left(e^{x^{2}}\right)\cdot \left(3 x e^{- x^{2}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{x^{2}}\right)\right) & =\left(e^{x^{2}}\right)\cdot \left(3 x e^{- x^{2}}\right)\end{aligned}
$$

## hard generated authored-bank polynomial_transform seed 1

Consider the following first-order linear ODE for the function $y=y(x):$

$$
\left(2\right)\cdot \frac{dy}{dx}-\left(12 x^{2}\right)\cdot y=- 6 x^{2} e^{2 x^{3}}
$$

Write the equation in the form $\frac{d}{dx}(yI(x))=I(x)Q(x),$ where $I(x)$ is an integrating factor.

- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{3}}\right)\right)=\left(e^{- 2 x^{3}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 6 x^{2}}\right)\right)=\left(e^{- 6 x^{2}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{2 x^{3}}\right)\right)=\left(e^{2 x^{3}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(x^{3}\right)\right)=\left(x^{3}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)$
- $\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{2}}\right)\right)=\left(e^{- 2 x^{2}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)$

Worked solution:

First, we write the equation in standard form. This gives

$$
\frac{dy}{dx}-\left(6 x^{2}\right)\cdot y=- 3 x^{2} e^{2 x^{3}}.
$$

This equation is in the standard form

$$
\frac{dy}{dx}+P(x)y=Q(x)
$$

with $P(x)=- 6 x^{2}$ and $Q(x)=- 3 x^{2} e^{2 x^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & =e^{\int P(x)\,dx} \\  & =e^{\int \left(- 6 x^{2}\right)\,dx} \\  & =e^{- 2 x^{3}}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)=e^{- 2 x^{3}}$ as follows:

$$
\begin{aligned}\left(e^{- 2 x^{3}}\right)\cdot \left(\frac{dy}{dx}-\left(6 x^{2}\right)\cdot y\right) & =\left(e^{- 2 x^{3}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right) \\ \left(e^{- 2 x^{3}}\right)\cdot \frac{dy}{dx}-\left(6 x^{2}\right)\cdot \left(e^{- 2 x^{3}}\right)\cdot y & =\left(e^{- 2 x^{3}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x)):$

$$
\begin{aligned}\frac{d}{dx}\left(y\cdot \left(e^{- 2 x^{3}}\right)\right) & =\left(e^{- 2 x^{3}}\right)\cdot \left(- 3 x^{2} e^{2 x^{3}}\right)\end{aligned}
$$
