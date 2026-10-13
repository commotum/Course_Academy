# Rate-of-change generator review

All records below are local author previews. Raw source notation errors are retained only in explicitly marked evidence profiles; consult validation.json.

## Original omission faithfully preserved q-36247

### mixed_product / q-36247_raw_omission (raw missing assessment)

Compute the rate of change of the function $f(x, y, z) = x^{2} + 3xyz$ with respect to $t$ along the curve $r(t) = ⟨t^{2}, t + 1,-t⟩$ at the point $t = 1$.

- $-17$
- $-15$
- $1$
- $9$
- $3$

Original difficulty, correct designation, and worked solution are absent.

## Original replay q-36247

### mixed_product / q-36247_raw

Compute the rate of change of the function $f(x, y, z) = x^{2} + 3xyz$ with respect to $t$ along the curve $r(t) = ⟨t^{2}, t + 1,-t⟩$ at the point $t = 1$.

- $-17$ **correct**
- $-15$
- $1$
- $9$
- $3$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(x^{2} + 3 x y z),\frac{∂}{∂y}(x^{2} + 3 x y z),\frac{∂}{∂z}(x^{2} + 3 x y z)⟩ \\  & =⟨2 x + 3 y z,3 x z,3 x y⟩\end{aligned}
$$

Next, we substitute $x=t^{2}$, $y=t + 1$, $z=- t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨3 \left(- t\right) \left(t + 1\right) + 2 t^{2},3 \left(- t\right) t^{2},3 t^{2} \left(t + 1\right)⟩ \\  & =⟨- t^{2} - 3 t,- 3 t^{3},3 t^{3} + 3 t^{2}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\frac{\text{d}}{\text{d}t}(t + 1),\frac{\text{d}}{\text{d}t}(- t)⟩ \\  & =⟨2 t,1,-1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- t^{2} - 3 t,- 3 t^{3},3 t^{3} + 3 t^{2}⟩\cdot ⟨2 t,1,-1⟩ \\  & =\left(- t^{2} - 3 t\right)\cdot \left(2 t\right)+\left(- 3 t^{3}\right)\cdot \left(1\right)+\left(3 t^{3} + 3 t^{2}\right)\cdot \left(-1\right) \\  & =t^{2} \left(- 8 t - 9\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =(1)^{2} \left(- 8 (1) - 9\right) \\  & =-17.\end{aligned}
$$

## Generated observed-bank equivariant variant q-36247; error intent unresolved

### mixed_product / q-36247_raw

Compute the rate of change of the function $f(x, y, z) = 2\left(x^{2} + 3xyz\right)$ with respect to $t$ along the curve $r(t) = ⟨t^{2}, t + 1,-t⟩$ at the point $t = 1$.

- $2\left(-15\right)$
- $2\left(1\right)$
- $2\left(3\right)$
- $2\left(9\right)$
- $2\left(-17\right)$ **correct**

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(2 x^{2} + 6 x y z),\frac{∂}{∂y}(2 x^{2} + 6 x y z),\frac{∂}{∂z}(2 x^{2} + 6 x y z)⟩ \\  & =⟨4 x + 6 y z,6 x z,6 x y⟩\end{aligned}
$$

Next, we substitute $x=t^{2}$, $y=t + 1$, $z=- t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨6 \left(- t\right) \left(t + 1\right) + 4 t^{2},6 \left(- t\right) t^{2},6 t^{2} \left(t + 1\right)⟩ \\  & =⟨- 2 t^{2} - 6 t,- 6 t^{3},6 t^{3} + 6 t^{2}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\frac{\text{d}}{\text{d}t}(t + 1),\frac{\text{d}}{\text{d}t}(- t)⟩ \\  & =⟨2 t,1,-1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 2 t^{2} - 6 t,- 6 t^{3},6 t^{3} + 6 t^{2}⟩\cdot ⟨2 t,1,-1⟩ \\  & =\left(- 2 t^{2} - 6 t\right)\cdot \left(2 t\right)+\left(- 6 t^{3}\right)\cdot \left(1\right)+\left(6 t^{3} + 6 t^{2}\right)\cdot \left(-1\right) \\  & =t^{2} \left(- 16 t - 18\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =(1)^{2} \left(- 16 (1) - 18\right) \\  & =-34.\end{aligned}
$$

## Generated observed-bank equivariant variant q-36247; error intent unresolved

### mixed_product / q-36247_raw

Compute the rate of change of the function $f(x, y, z) = 4\left(x^{2} + 3xyz\right)$ with respect to $t$ along the curve $r(t) = ⟨t^{2}, t + 1,-t⟩$ at the point $t = 1$.

- $4\left(-15\right)$
- $4\left(1\right)$
- $4\left(3\right)$
- $4\left(9\right)$
- $4\left(-17\right)$ **correct**

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(4 x^{2} + 12 x y z),\frac{∂}{∂y}(4 x^{2} + 12 x y z),\frac{∂}{∂z}(4 x^{2} + 12 x y z)⟩ \\  & =⟨8 x + 12 y z,12 x z,12 x y⟩\end{aligned}
$$

Next, we substitute $x=t^{2}$, $y=t + 1$, $z=- t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨12 \left(- t\right) \left(t + 1\right) + 8 t^{2},12 \left(- t\right) t^{2},12 t^{2} \left(t + 1\right)⟩ \\  & =⟨- 4 t^{2} - 12 t,- 12 t^{3},12 t^{3} + 12 t^{2}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\frac{\text{d}}{\text{d}t}(t + 1),\frac{\text{d}}{\text{d}t}(- t)⟩ \\  & =⟨2 t,1,-1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 4 t^{2} - 12 t,- 12 t^{3},12 t^{3} + 12 t^{2}⟩\cdot ⟨2 t,1,-1⟩ \\  & =\left(- 4 t^{2} - 12 t\right)\cdot \left(2 t\right)+\left(- 12 t^{3}\right)\cdot \left(1\right)+\left(12 t^{3} + 12 t^{2}\right)\cdot \left(-1\right) \\  & =t^{2} \left(- 32 t - 36\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =(1)^{2} \left(- 32 (1) - 36\right) \\  & =-68.\end{aligned}
$$

## Original omission faithfully preserved q-36253

### sine_difference / q-36253_raw_omission (raw missing assessment)

Compute the rate of change of the function $f(x, y) = \sin (x - y)$ with respect to $t$ along the curve $r(t) = ⟨2\sqrt{t}, 4t⟩$ at the point $t = 1$.

- $5\cos 2$
- $0$
- $-3\cos 8$
- $-3\cos 2$
- $\cos 2$

Original difficulty, correct designation, and worked solution are absent.

## Original replay q-36253

### sine_difference / q-36253_raw

Compute the rate of change of the function $f(x, y) = \sin (x - y)$ with respect to $t$ along the curve $r(t) = ⟨2\sqrt{t}, 4t⟩$ at the point $t = 1$.

- $5\cos 2$
- $0$
- $-3\cos 8$
- $-3\cos 2$ **correct**
- $\cos 2$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(\sin{\left(x - y \right)}),\frac{∂}{∂y}(\sin{\left(x - y \right)})⟩ \\  & =⟨\cos{\left(x - y \right)},- \cos{\left(x - y \right)}⟩\end{aligned}
$$

Next, we substitute $x=2 \sqrt{t}$, $y=4 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\cos{\left(2 \sqrt{t} - 4 t \right)},- \cos{\left(2 \sqrt{t} - 4 t \right)}⟩ \\  & =⟨\cos{\left(2 \sqrt{t} - 4 t \right)},- \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\frac{\text{d}}{\text{d}t}(4 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},4⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\cos{\left(2 \sqrt{t} - 4 t \right)},- \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\cdot ⟨\frac{1}{\sqrt{t}},4⟩ \\  & =\left(\cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(\frac{1}{\sqrt{t}}\right)+\left(- \cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(4\right) \\  & =\frac{\left(- 4 \sqrt{t} + 1\right) \cos{\left(2 \sqrt{t} - 4 t \right)}}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{\left(- 4 \sqrt{(1)} + 1\right) \cos{\left(2 \sqrt{(1)} - 4 (1) \right)}}{\sqrt{(1)}} \\  & =- 3 \cos{\left(2 \right)}.\end{aligned}
$$

## Generated observed-bank equivariant variant q-36253; error intent unresolved

### sine_difference / q-36253_raw

Compute the rate of change of the function $f(x, y) = 2\left(\sin (x - y)\right)$ with respect to $t$ along the curve $r(t) = ⟨2\sqrt{t}, 4t⟩$ at the point $t = 1$.

- $2\left(0\right)$
- $2\left(-3\cos 8\right)$
- $2\left(\cos 2\right)$
- $2\left(-3\cos 2\right)$ **correct**
- $2\left(5\cos 2\right)$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(2 \sin{\left(x - y \right)}),\frac{∂}{∂y}(2 \sin{\left(x - y \right)})⟩ \\  & =⟨2 \cos{\left(x - y \right)},- 2 \cos{\left(x - y \right)}⟩\end{aligned}
$$

Next, we substitute $x=2 \sqrt{t}$, $y=4 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨2 \cos{\left(2 \sqrt{t} - 4 t \right)},- 2 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩ \\  & =⟨2 \cos{\left(2 \sqrt{t} - 4 t \right)},- 2 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\frac{\text{d}}{\text{d}t}(4 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},4⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨2 \cos{\left(2 \sqrt{t} - 4 t \right)},- 2 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\cdot ⟨\frac{1}{\sqrt{t}},4⟩ \\  & =\left(2 \cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(\frac{1}{\sqrt{t}}\right)+\left(- 2 \cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(4\right) \\  & =\frac{2 \left(- 4 \sqrt{t} + 1\right) \cos{\left(2 \sqrt{t} - 4 t \right)}}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2 \left(- 4 \sqrt{(1)} + 1\right) \cos{\left(2 \sqrt{(1)} - 4 (1) \right)}}{\sqrt{(1)}} \\  & =- 6 \cos{\left(2 \right)}.\end{aligned}
$$

## Generated observed-bank equivariant variant q-36253; error intent unresolved

### sine_difference / q-36253_raw

Compute the rate of change of the function $f(x, y) = 4\left(\sin (x - y)\right)$ with respect to $t$ along the curve $r(t) = ⟨2\sqrt{t}, 4t⟩$ at the point $t = 1$.

- $4\left(0\right)$
- $4\left(-3\cos 8\right)$
- $4\left(\cos 2\right)$
- $4\left(-3\cos 2\right)$ **correct**
- $4\left(5\cos 2\right)$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(4 \sin{\left(x - y \right)}),\frac{∂}{∂y}(4 \sin{\left(x - y \right)})⟩ \\  & =⟨4 \cos{\left(x - y \right)},- 4 \cos{\left(x - y \right)}⟩\end{aligned}
$$

Next, we substitute $x=2 \sqrt{t}$, $y=4 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨4 \cos{\left(2 \sqrt{t} - 4 t \right)},- 4 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩ \\  & =⟨4 \cos{\left(2 \sqrt{t} - 4 t \right)},- 4 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\frac{\text{d}}{\text{d}t}(4 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},4⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨4 \cos{\left(2 \sqrt{t} - 4 t \right)},- 4 \cos{\left(2 \sqrt{t} - 4 t \right)}⟩\cdot ⟨\frac{1}{\sqrt{t}},4⟩ \\  & =\left(4 \cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(\frac{1}{\sqrt{t}}\right)+\left(- 4 \cos{\left(2 \sqrt{t} - 4 t \right)}\right)\cdot \left(4\right) \\  & =\frac{4 \left(- 4 \sqrt{t} + 1\right) \cos{\left(2 \sqrt{t} - 4 t \right)}}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{4 \left(- 4 \sqrt{(1)} + 1\right) \cos{\left(2 \sqrt{(1)} - 4 (1) \right)}}{\sqrt{(1)}} \\  & =- 12 \cos{\left(2 \right)}.\end{aligned}
$$

## Original replay q-167499

### quotient / q-167499_raw

Compute the rate of change of the function $f(x,y)=\frac{x}{y}$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t}⟩$ at the point $t=9.$

- $-\sqrt{3}$
- $\frac{1}{\sqrt{3}}$
- $-\frac{1}{9}$
- $\frac{1}{3}$ **correct**
- $1$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}),\frac{∂}{∂y}(\frac{x}{y})⟩ \\  & =⟨\frac{1}{y},-\frac{x}{{y}^{2}}⟩\end{aligned}
$$

Next, we substitute $x=2t$ and $y=\sqrt{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\frac{1}{\sqrt{t}},-2⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t})⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\frac{1}{\sqrt{t}},-2⟩\cdot ⟨2,\frac{1}{2\sqrt{t}}⟩ \\  & =\frac{1}{\sqrt{t}}\cdot 2-2\cdot \frac{1}{2\sqrt{t}} \\  & =\frac{2}{\sqrt{t}}-\frac{1}{\sqrt{t}} \\  & =\frac{1}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=9$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(9))] & =\frac{1}{\sqrt{9}} \\  & =\frac{1}{3}.\end{aligned}
$$

## Generated observed-bank equivariant variant q-167499; error intent unresolved

### quotient / q-167499_raw

Compute the rate of change of the function $f(x,y)=2\left(\frac{x}{y}\right)$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t}⟩$ at the point $t=9.$

- $2\left(\frac{1}{\sqrt{3}}\right)$
- $2\left(-\frac{1}{9}\right)$
- $2\left(1\right)$
- $2\left(\frac{1}{3}\right)$ **correct**
- $2\left(-\sqrt{3}\right)$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}(\frac{x}{y}),\frac{∂}{∂y}(\frac{x}{y})⟩\right) \\  & =2\left(⟨\frac{1}{y},-\frac{x}{{y}^{2}}⟩\right)\end{aligned}
$$

Next, we substitute $x=2t$ and $y=\sqrt{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨\frac{1}{\sqrt{t}},-2⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t})⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨\frac{1}{\sqrt{t}},-2⟩\cdot ⟨2,\frac{1}{2\sqrt{t}}⟩\right) \\  & =2\left(\frac{1}{\sqrt{t}}\cdot 2-2\cdot \frac{1}{2\sqrt{t}}\right) \\  & =2\left(\frac{2}{\sqrt{t}}-\frac{1}{\sqrt{t}}\right) \\  & =2\left(\frac{1}{\sqrt{t}}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=9$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(9))] & =2\left(\frac{1}{\sqrt{9}}\right) \\  & =2\left(\frac{1}{3}\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-167499; error intent unresolved

### quotient / q-167499_raw

Compute the rate of change of the function $f(x,y)=4\left(\frac{x}{y}\right)$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t}⟩$ at the point $t=9.$

- $4\left(\frac{1}{\sqrt{3}}\right)$
- $4\left(-\frac{1}{9}\right)$
- $4\left(1\right)$
- $4\left(\frac{1}{3}\right)$ **correct**
- $4\left(-\sqrt{3}\right)$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}(\frac{x}{y}),\frac{∂}{∂y}(\frac{x}{y})⟩\right) \\  & =4\left(⟨\frac{1}{y},-\frac{x}{{y}^{2}}⟩\right)\end{aligned}
$$

Next, we substitute $x=2t$ and $y=\sqrt{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨\frac{1}{\sqrt{t}},-2⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t})⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨\frac{1}{\sqrt{t}},-2⟩\cdot ⟨2,\frac{1}{2\sqrt{t}}⟩\right) \\  & =4\left(\frac{1}{\sqrt{t}}\cdot 2-2\cdot \frac{1}{2\sqrt{t}}\right) \\  & =4\left(\frac{2}{\sqrt{t}}-\frac{1}{\sqrt{t}}\right) \\  & =4\left(\frac{1}{\sqrt{t}}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=9$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(9))] & =4\left(\frac{1}{\sqrt{9}}\right) \\  & =4\left(\frac{1}{3}\right).\end{aligned}
$$

## Original replay q-36227

### trig_powers / q-36227_raw

Compute the rate of change of the function $f(x,y)={x}^{3}+{y}^{2}$ with respect to $t$ along the curve $r(t)=⟨\operatorname{sin}⁡t,\operatorname{cos}⁡t⟩$ at the point $t=\frac{\pi }{4}.$

- $\frac{\sqrt{3}-2}{2}$
- $\frac{3}{8}$
- $2\sqrt{3}-1$
- $\frac{3\sqrt{2}-4}{4}$ **correct**
- $0$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}({x}^{3}+{y}^{2}),\frac{∂}{∂y}({x}^{3}+{y}^{2})⟩ \\  & =⟨3{x}^{2},2y⟩\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡t$ and $y=\operatorname{cos}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t),\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)⟩ \\  & =⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\cdot ⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩ \\  & =3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t+2\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t) \\  & =3{sin}^{2}⁡t\operatorname{cos}⁡t-2\operatorname{sin}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=\frac{\pi }{4}$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{4}))] & =3{sin}^{2}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})-2\operatorname{sin}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4}) \\  & =3\cdot {(\frac{\sqrt{2}}{2})}^{2}\cdot \frac{\sqrt{2}}{2}-2\cdot \frac{\sqrt{2}}{2}\cdot \frac{\sqrt{2}}{2} \\  & =\frac{3\sqrt{2}}{4}-1 \\  & =\frac{3\sqrt{2}-4}{4}.\end{aligned}
$$

## Generated observed-bank equivariant variant q-36227; error intent unresolved

### trig_powers / q-36227_raw

Compute the rate of change of the function $f(x,y)=2\left({x}^{3}+{y}^{2}\right)$ with respect to $t$ along the curve $r(t)=⟨\operatorname{sin}⁡t,\operatorname{cos}⁡t⟩$ at the point $t=\frac{\pi }{4}.$

- $2\left(\frac{3}{8}\right)$
- $2\left(2\sqrt{3}-1\right)$
- $2\left(0\right)$
- $2\left(\frac{3\sqrt{2}-4}{4}\right)$ **correct**
- $2\left(\frac{\sqrt{3}-2}{2}\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}({x}^{3}+{y}^{2}),\frac{∂}{∂y}({x}^{3}+{y}^{2})⟩\right) \\  & =2\left(⟨3{x}^{2},2y⟩\right)\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡t$ and $y=\operatorname{cos}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t),\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)⟩ \\  & =⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\cdot ⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩\right) \\  & =2\left(3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t+2\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t)\right) \\  & =2\left(3{sin}^{2}⁡t\operatorname{cos}⁡t-2\operatorname{sin}⁡t\operatorname{cos}⁡t\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=\frac{\pi }{4}$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{4}))] & =2\left(3{sin}^{2}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})-2\operatorname{sin}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})\right) \\  & =2\left(3\cdot {(\frac{\sqrt{2}}{2})}^{2}\cdot \frac{\sqrt{2}}{2}-2\cdot \frac{\sqrt{2}}{2}\cdot \frac{\sqrt{2}}{2}\right) \\  & =2\left(\frac{3\sqrt{2}}{4}-1\right) \\  & =2\left(\frac{3\sqrt{2}-4}{4}\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-36227; error intent unresolved

### trig_powers / q-36227_raw

Compute the rate of change of the function $f(x,y)=4\left({x}^{3}+{y}^{2}\right)$ with respect to $t$ along the curve $r(t)=⟨\operatorname{sin}⁡t,\operatorname{cos}⁡t⟩$ at the point $t=\frac{\pi }{4}.$

- $4\left(\frac{3}{8}\right)$
- $4\left(2\sqrt{3}-1\right)$
- $4\left(0\right)$
- $4\left(\frac{3\sqrt{2}-4}{4}\right)$ **correct**
- $4\left(\frac{\sqrt{3}-2}{2}\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}({x}^{3}+{y}^{2}),\frac{∂}{∂y}({x}^{3}+{y}^{2})⟩\right) \\  & =4\left(⟨3{x}^{2},2y⟩\right)\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡t$ and $y=\operatorname{cos}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t),\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)⟩ \\  & =⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨3{sin}^{2}⁡t,2\operatorname{cos}⁡t⟩\cdot ⟨\operatorname{cos}⁡t,-\operatorname{sin}⁡t⟩\right) \\  & =4\left(3{sin}^{2}⁡t\cdot \operatorname{cos}⁡t+2\operatorname{cos}⁡t\cdot (-\operatorname{sin}⁡t)\right) \\  & =4\left(3{sin}^{2}⁡t\operatorname{cos}⁡t-2\operatorname{sin}⁡t\operatorname{cos}⁡t\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=\frac{\pi }{4}$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{4}))] & =4\left(3{sin}^{2}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})-2\operatorname{sin}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})\right) \\  & =4\left(3\cdot {(\frac{\sqrt{2}}{2})}^{2}\cdot \frac{\sqrt{2}}{2}-2\cdot \frac{\sqrt{2}}{2}\cdot \frac{\sqrt{2}}{2}\right) \\  & =4\left(\frac{3\sqrt{2}}{4}-1\right) \\  & =4\left(\frac{3\sqrt{2}-4}{4}\right).\end{aligned}
$$

## Original replay q-94884

### square_difference / q-94884_raw

Compute the rate of change of the function $f(x,y)={x}^{2}-{y}^{2}$ with respect to $t$ along the curve $r(t)=⟨{t}^{2},2t-1⟩$ at the point $t=0.$

- $-1$
- $-3$
- $4$ **correct**
- $5$
- $2$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}({x}^{2}-{y}^{2}),\frac{∂}{∂y}({x}^{2}-{y}^{2})⟩ \\  & =⟨2x,-2y⟩\end{aligned}
$$

Next, we substitute $x={t}^{2}$ and $y=2t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨2{t}^{2},-2(2t-1)⟩ \\  & =⟨2{t}^{2},2-4t⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\frac{\text{d}}{\text{d}t}(2t-1)⟩ \\  & =⟨2t,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨2{t}^{2},2-4t⟩\cdot ⟨2t,2⟩ \\  & =2{t}^{2}\cdot 2t+(2-4t)\cdot 2 \\  & =4{t}^{3}-8t+4.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =4(0)^{3}-8(0)+4 \\  & =4.\end{aligned}
$$

## Generated observed-bank equivariant variant q-94884; error intent unresolved

### square_difference / q-94884_raw

Compute the rate of change of the function $f(x,y)=2\left({x}^{2}-{y}^{2}\right)$ with respect to $t$ along the curve $r(t)=⟨{t}^{2},2t-1⟩$ at the point $t=0.$

- $2\left(-3\right)$
- $2\left(4\right)$ **correct**
- $2\left(2\right)$
- $2\left(5\right)$
- $2\left(-1\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}({x}^{2}-{y}^{2}),\frac{∂}{∂y}({x}^{2}-{y}^{2})⟩\right) \\  & =2\left(⟨2x,-2y⟩\right)\end{aligned}
$$

Next, we substitute $x={t}^{2}$ and $y=2t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨2{t}^{2},-2(2t-1)⟩\right) \\  & =2\left(⟨2{t}^{2},2-4t⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\frac{\text{d}}{\text{d}t}(2t-1)⟩ \\  & =⟨2t,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨2{t}^{2},2-4t⟩\cdot ⟨2t,2⟩\right) \\  & =2\left(2{t}^{2}\cdot 2t+(2-4t)\cdot 2\right) \\  & =2\left(4{t}^{3}-8t+4\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2\left(4(0)^{3}-8(0)+4\right) \\  & =2\left(4\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-94884; error intent unresolved

### square_difference / q-94884_raw

Compute the rate of change of the function $f(x,y)=4\left({x}^{2}-{y}^{2}\right)$ with respect to $t$ along the curve $r(t)=⟨{t}^{2},2t-1⟩$ at the point $t=0.$

- $4\left(-3\right)$
- $4\left(4\right)$ **correct**
- $4\left(2\right)$
- $4\left(5\right)$
- $4\left(-1\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}({x}^{2}-{y}^{2}),\frac{∂}{∂y}({x}^{2}-{y}^{2})⟩\right) \\  & =4\left(⟨2x,-2y⟩\right)\end{aligned}
$$

Next, we substitute $x={t}^{2}$ and $y=2t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨2{t}^{2},-2(2t-1)⟩\right) \\  & =4\left(⟨2{t}^{2},2-4t⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\frac{\text{d}}{\text{d}t}(2t-1)⟩ \\  & =⟨2t,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨2{t}^{2},2-4t⟩\cdot ⟨2t,2⟩\right) \\  & =4\left(2{t}^{2}\cdot 2t+(2-4t)\cdot 2\right) \\  & =4\left(4{t}^{3}-8t+4\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =4\left(4(0)^{3}-8(0)+4\right) \\  & =4\left(4\right).\end{aligned}
$$

## Original replay q-94887

### triple_product / q-94887_raw

Compute the rate of change of the function $f(x,y,z)=xyz$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t},3t-1⟩$ at the point $t=1.$

- $-8$
- $6$
- $15$
- $12$ **correct**
- $-10$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(xyz),\frac{∂}{∂y}(xyz),\frac{∂}{∂z}(xyz)⟩ \\  & =⟨yz,xz,xy⟩\end{aligned}
$$

Next, we substitute $x=2t,y=\sqrt{t}$ and $z=3t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\sqrt{t}(3t-1),2t(3t-1),2t\sqrt{t}⟩ \\  & =⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t}),\frac{\text{d}}{\text{d}t}(3t-1)⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}},3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\cdot ⟨2,\frac{1}{2\sqrt{t}},3⟩ \\  & =(3t-1)\sqrt{t}\cdot 2+(6{t}^{2}-2t)\cdot \frac{1}{2\sqrt{t}}+2t\sqrt{t}\cdot 3 \\  & =6t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}+6t\sqrt{t} \\  & =12t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =12(1)\sqrt{1}-2\sqrt{1}+\frac{3(1)^{2}-1}{\sqrt{1}} \\  & =12.\end{aligned}
$$

## Generated observed-bank equivariant variant q-94887; error intent unresolved

### triple_product / q-94887_raw

Compute the rate of change of the function $f(x,y,z)=2\left(xyz\right)$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t},3t-1⟩$ at the point $t=1.$

- $2\left(6\right)$
- $2\left(15\right)$
- $2\left(-10\right)$
- $2\left(12\right)$ **correct**
- $2\left(-8\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}(xyz),\frac{∂}{∂y}(xyz),\frac{∂}{∂z}(xyz)⟩\right) \\  & =2\left(⟨yz,xz,xy⟩\right)\end{aligned}
$$

Next, we substitute $x=2t,y=\sqrt{t}$ and $z=3t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨\sqrt{t}(3t-1),2t(3t-1),2t\sqrt{t}⟩\right) \\  & =2\left(⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t}),\frac{\text{d}}{\text{d}t}(3t-1)⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}},3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\cdot ⟨2,\frac{1}{2\sqrt{t}},3⟩\right) \\  & =2\left((3t-1)\sqrt{t}\cdot 2+(6{t}^{2}-2t)\cdot \frac{1}{2\sqrt{t}}+2t\sqrt{t}\cdot 3\right) \\  & =2\left(6t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}+6t\sqrt{t}\right) \\  & =2\left(12t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2\left(12(1)\sqrt{1}-2\sqrt{1}+\frac{3(1)^{2}-1}{\sqrt{1}}\right) \\  & =2\left(12\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-94887; error intent unresolved

### triple_product / q-94887_raw

Compute the rate of change of the function $f(x,y,z)=4\left(xyz\right)$ with respect to $t$ along the curve $r(t)=⟨2t,\sqrt{t},3t-1⟩$ at the point $t=1.$

- $4\left(6\right)$
- $4\left(15\right)$
- $4\left(-10\right)$
- $4\left(12\right)$ **correct**
- $4\left(-8\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}(xyz),\frac{∂}{∂y}(xyz),\frac{∂}{∂z}(xyz)⟩\right) \\  & =4\left(⟨yz,xz,xy⟩\right)\end{aligned}
$$

Next, we substitute $x=2t,y=\sqrt{t}$ and $z=3t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨\sqrt{t}(3t-1),2t(3t-1),2t\sqrt{t}⟩\right) \\  & =4\left(⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t),\frac{\text{d}}{\text{d}t}(\sqrt{t}),\frac{\text{d}}{\text{d}t}(3t-1)⟩ \\  & =⟨2,\frac{1}{2\sqrt{t}},3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨(3t-1)\sqrt{t},6{t}^{2}-2t,2t\sqrt{t}⟩\cdot ⟨2,\frac{1}{2\sqrt{t}},3⟩\right) \\  & =4\left((3t-1)\sqrt{t}\cdot 2+(6{t}^{2}-2t)\cdot \frac{1}{2\sqrt{t}}+2t\sqrt{t}\cdot 3\right) \\  & =4\left(6t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}+6t\sqrt{t}\right) \\  & =4\left(12t\sqrt{t}-2\sqrt{t}+\frac{3{t}^{2}-t}{\sqrt{t}}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =4\left(12(1)\sqrt{1}-2\sqrt{1}+\frac{3(1)^{2}-1}{\sqrt{1}}\right) \\  & =4\left(12\right).\end{aligned}
$$

## Original replay q-94888

### radical_square / q-94888_raw

Compute the rate of change of the function $f(x,y,z)=x{z}^{2}+{y}^{3}$ with respect to $t$ along the curve $r(t)=⟨t,4,\sqrt{{t}^{2}-3}⟩$ at the point $t=2.$

- $-12$
- $6$
- $10$
- $9$ **correct**
- $-7$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(x{z}^{2}+{y}^{3}),\frac{∂}{∂y}(x{z}^{2}+{y}^{3}),\frac{∂}{∂z}(x{z}^{2}+{y}^{3})⟩ \\  & =⟨{z}^{2},3{y}^{2},2xz⟩\end{aligned}
$$

Next, we substitute $x=t,$ $y=4$ and $z=\sqrt{{t}^{2}-3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨(\sqrt{{t}^{2}-3})^{2},3(4)^{2},2t\sqrt{{t}^{2}-3}⟩ \\  & =⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(4),\sqrt{{t}^{2}-3}⟩ \\  & =⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\cdot ⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩ \\  & =({t}^{2}-3)\cdot 1+48\cdot 0+2t\sqrt{{t}^{2}-3}\cdot \frac{t}{\sqrt{{t}^{2}-3}} \\  & ={t}^{2}-3+0+2{t}^{2} \\  & =3{t}^{2}-3.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =3(2)^{2}-3 \\  & =12-3 \\  & =9.\end{aligned}
$$

## Generated observed-bank equivariant variant q-94888; error intent unresolved

### radical_square / q-94888_raw

Compute the rate of change of the function $f(x,y,z)=2\left(x{z}^{2}+{y}^{3}\right)$ with respect to $t$ along the curve $r(t)=⟨t,4,\sqrt{{t}^{2}-3}⟩$ at the point $t=2.$

- $2\left(6\right)$
- $2\left(10\right)$
- $2\left(-7\right)$
- $2\left(9\right)$ **correct**
- $2\left(-12\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}(x{z}^{2}+{y}^{3}),\frac{∂}{∂y}(x{z}^{2}+{y}^{3}),\frac{∂}{∂z}(x{z}^{2}+{y}^{3})⟩\right) \\  & =2\left(⟨{z}^{2},3{y}^{2},2xz⟩\right)\end{aligned}
$$

Next, we substitute $x=t,$ $y=4$ and $z=\sqrt{{t}^{2}-3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨(\sqrt{{t}^{2}-3})^{2},3(4)^{2},2t\sqrt{{t}^{2}-3}⟩\right) \\  & =2\left(⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(4),\sqrt{{t}^{2}-3}⟩ \\  & =⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\cdot ⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩\right) \\  & =2\left(({t}^{2}-3)\cdot 1+48\cdot 0+2t\sqrt{{t}^{2}-3}\cdot \frac{t}{\sqrt{{t}^{2}-3}}\right) \\  & =2\left({t}^{2}-3+0+2{t}^{2}\right) \\  & =2\left(3{t}^{2}-3\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =2\left(3(2)^{2}-3\right) \\  & =2\left(12-3\right) \\  & =2\left(9\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-94888; error intent unresolved

### radical_square / q-94888_raw

Compute the rate of change of the function $f(x,y,z)=4\left(x{z}^{2}+{y}^{3}\right)$ with respect to $t$ along the curve $r(t)=⟨t,4,\sqrt{{t}^{2}-3}⟩$ at the point $t=2.$

- $4\left(6\right)$
- $4\left(10\right)$
- $4\left(-7\right)$
- $4\left(9\right)$ **correct**
- $4\left(-12\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}(x{z}^{2}+{y}^{3}),\frac{∂}{∂y}(x{z}^{2}+{y}^{3}),\frac{∂}{∂z}(x{z}^{2}+{y}^{3})⟩\right) \\  & =4\left(⟨{z}^{2},3{y}^{2},2xz⟩\right)\end{aligned}
$$

Next, we substitute $x=t,$ $y=4$ and $z=\sqrt{{t}^{2}-3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨(\sqrt{{t}^{2}-3})^{2},3(4)^{2},2t\sqrt{{t}^{2}-3}⟩\right) \\  & =4\left(⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(4),\sqrt{{t}^{2}-3}⟩ \\  & =⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨{t}^{2}-3,48,2t\sqrt{{t}^{2}-3}⟩\cdot ⟨1,0,\frac{t}{\sqrt{{t}^{2}-3}}⟩\right) \\  & =4\left(({t}^{2}-3)\cdot 1+48\cdot 0+2t\sqrt{{t}^{2}-3}\cdot \frac{t}{\sqrt{{t}^{2}-3}}\right) \\  & =4\left({t}^{2}-3+0+2{t}^{2}\right) \\  & =4\left(3{t}^{2}-3\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =4\left(3(2)^{2}-3\right) \\  & =4\left(12-3\right) \\  & =4\left(9\right).\end{aligned}
$$

## Original replay q-94891

### log_norm / q-94891_raw

Compute the rate of change of the function $f(x,y,z)=\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})$ with respect to $t$ along the curve $r(t)=⟨t-1,3,2t⟩$ at the point $t=0.$

- $\frac{3}{10}$
- $-\frac{12}{17}$
- $\frac{8}{13}$
- $-\frac{1}{5}$ **correct**
- $\frac{2}{3}$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂z}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2}))⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2y}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2z}{{x}^{2}+{y}^{2}+{z}^{2}}⟩\end{aligned}
$$

Next, we substitute $x=t-1,$ $y=3$ and $z=2t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\frac{2(t-1)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(3)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(2t)}{(t-1)^{2}+(3)^{2}+(2t)^{2}}⟩ \\  & =⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t-1),\frac{\text{d}}{\text{d}t}(3),2t⟩ \\  & =⟨1,0,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\cdot ⟨1,0,2⟩ \\  & =\frac{2t-2}{5{t}^{2}-2t+10}\cdot 1+\frac{6}{5{t}^{2}-2t+10}\cdot 0+\frac{4t}{5{t}^{2}-2t+10}\cdot 2 \\  & =\frac{2t-2+8t}{5{t}^{2}-2t+10} \\  & =\frac{10t-2}{5{t}^{2}-2t+10}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =\frac{10(0)-2}{5(0)^{2}-2(0)+10} \\  & =\frac{-2}{10} \\  & =-\frac{1}{5}.\end{aligned}
$$

## Generated observed-bank equivariant variant q-94891; error intent unresolved

### log_norm / q-94891_raw

Compute the rate of change of the function $f(x,y,z)=2\left(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})\right)$ with respect to $t$ along the curve $r(t)=⟨t-1,3,2t⟩$ at the point $t=0.$

- $2\left(-\frac{12}{17}\right)$
- $2\left(\frac{8}{13}\right)$
- $2\left(\frac{2}{3}\right)$
- $2\left(-\frac{1}{5}\right)$ **correct**
- $2\left(\frac{3}{10}\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =2\left(⟨\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂z}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2}))⟩\right) \\  & =2\left(⟨\frac{2x}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2y}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2z}{{x}^{2}+{y}^{2}+{z}^{2}}⟩\right)\end{aligned}
$$

Next, we substitute $x=t-1,$ $y=3$ and $z=2t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\left(⟨\frac{2(t-1)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(3)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(2t)}{(t-1)^{2}+(3)^{2}+(2t)^{2}}⟩\right) \\  & =2\left(⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t-1),\frac{\text{d}}{\text{d}t}(3),2t⟩ \\  & =⟨1,0,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\left(⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\cdot ⟨1,0,2⟩\right) \\  & =2\left(\frac{2t-2}{5{t}^{2}-2t+10}\cdot 1+\frac{6}{5{t}^{2}-2t+10}\cdot 0+\frac{4t}{5{t}^{2}-2t+10}\cdot 2\right) \\  & =2\left(\frac{2t-2+8t}{5{t}^{2}-2t+10}\right) \\  & =2\left(\frac{10t-2}{5{t}^{2}-2t+10}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2\left(\frac{10(0)-2}{5(0)^{2}-2(0)+10}\right) \\  & =2\left(\frac{-2}{10}\right) \\  & =2\left(-\frac{1}{5}\right).\end{aligned}
$$

## Generated observed-bank equivariant variant q-94891; error intent unresolved

### log_norm / q-94891_raw

Compute the rate of change of the function $f(x,y,z)=4\left(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})\right)$ with respect to $t$ along the curve $r(t)=⟨t-1,3,2t⟩$ at the point $t=0.$

- $4\left(-\frac{12}{17}\right)$
- $4\left(\frac{8}{13}\right)$
- $4\left(\frac{2}{3}\right)$
- $4\left(-\frac{1}{5}\right)$ **correct**
- $4\left(\frac{3}{10}\right)$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =4\left(⟨\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2})),\frac{∂}{∂z}(\operatorname{ln}⁡({x}^{2}+{y}^{2}+{z}^{2}))⟩\right) \\  & =4\left(⟨\frac{2x}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2y}{{x}^{2}+{y}^{2}+{z}^{2}},\frac{2z}{{x}^{2}+{y}^{2}+{z}^{2}}⟩\right)\end{aligned}
$$

Next, we substitute $x=t-1,$ $y=3$ and $z=2t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4\left(⟨\frac{2(t-1)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(3)}{(t-1)^{2}+(3)^{2}+(2t)^{2}},\frac{2(2t)}{(t-1)^{2}+(3)^{2}+(2t)^{2}}⟩\right) \\  & =4\left(⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t-1),\frac{\text{d}}{\text{d}t}(3),2t⟩ \\  & =⟨1,0,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =4\left(⟨\frac{2t-2}{5{t}^{2}-2t+10},\frac{6}{5{t}^{2}-2t+10},\frac{4t}{5{t}^{2}-2t+10}⟩\cdot ⟨1,0,2⟩\right) \\  & =4\left(\frac{2t-2}{5{t}^{2}-2t+10}\cdot 1+\frac{6}{5{t}^{2}-2t+10}\cdot 0+\frac{4t}{5{t}^{2}-2t+10}\cdot 2\right) \\  & =4\left(\frac{2t-2+8t}{5{t}^{2}-2t+10}\right) \\  & =4\left(\frac{10t-2}{5{t}^{2}-2t+10}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =4\left(\frac{10(0)-2}{5(0)^{2}-2(0)+10}\right) \\  & =4\left(\frac{-2}{10}\right) \\  & =4\left(-\frac{1}{5}\right).\end{aligned}
$$

## Authored hard method-operation variant; mixed_product

### mixed_product / mixed_product_operations

Compute the rate of change of the function $f(x,y,z)=2 x^{2} - 2 x y z$ with respect to $t$ along the curve $r(t)=⟨- t^{2},- 3 t + 1,2 t⟩$ at the point $t=-1.$

- $36$
- $28$
- $52$ **correct**
- $20$
- $16$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(2 x^{2} - 2 x y z),\frac{∂}{∂y}(2 x^{2} - 2 x y z),\frac{∂}{∂z}(2 x^{2} - 2 x y z)⟩ \\  & =⟨4 x - 2 y z,- 2 x z,- 2 x y⟩\end{aligned}
$$

Next, we substitute $x=- t^{2}$, $y=- 3 t + 1$, $z=2 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨4 \left(- t^{2}\right) - 2 \cdot 2 t \left(- 3 t + 1\right),- 2 \cdot 2 t \left(- t^{2}\right),- 2 \left(- t^{2}\right) \left(- 3 t + 1\right)⟩ \\  & =⟨8 t^{2} - 4 t,4 t^{3},- 6 t^{3} + 2 t^{2}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t^{2}),\frac{\text{d}}{\text{d}t}(- 3 t + 1),\frac{\text{d}}{\text{d}t}(2 t)⟩ \\  & =⟨- 2 t,-3,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨8 t^{2} - 4 t,4 t^{3},- 6 t^{3} + 2 t^{2}⟩\cdot ⟨- 2 t,-3,2⟩ \\  & =\left(8 t^{2} - 4 t\right)\cdot \left(- 2 t\right)+\left(4 t^{3}\right)\cdot \left(-3\right)+\left(- 6 t^{3} + 2 t^{2}\right)\cdot \left(2\right) \\  & =t^{2} \left(- 40 t + 12\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=-1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & =(-1)^{2} \left(- 40 (-1) + 12\right) \\  & =52.\end{aligned}
$$

## Authored hard method-operation variant; mixed_product

### mixed_product / mixed_product_operations

Compute the rate of change of the function $f(x,y,z)=x^{2} + x y z$ with respect to $t$ along the curve $r(t)=⟨3 t^{2},- 2 t + 1,- 3 t⟩$ at the point $t=1.$

- $72$
- $-3$
- $63$
- $81$ **correct**
- $27$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(x^{2} + x y z),\frac{∂}{∂y}(x^{2} + x y z),\frac{∂}{∂z}(x^{2} + x y z)⟩ \\  & =⟨2 x + y z,x z,x y⟩\end{aligned}
$$

Next, we substitute $x=3 t^{2}$, $y=- 2 t + 1$, $z=- 3 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 3 t \left(- 2 t + 1\right) + 2 \cdot 3 t^{2},- 3 t 3 t^{2},3 t^{2} \left(- 2 t + 1\right)⟩ \\  & =⟨12 t^{2} - 3 t,- 9 t^{3},- 6 t^{3} + 3 t^{2}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t^{2}),\frac{\text{d}}{\text{d}t}(- 2 t + 1),\frac{\text{d}}{\text{d}t}(- 3 t)⟩ \\  & =⟨6 t,-2,-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨12 t^{2} - 3 t,- 9 t^{3},- 6 t^{3} + 3 t^{2}⟩\cdot ⟨6 t,-2,-3⟩ \\  & =\left(12 t^{2} - 3 t\right)\cdot \left(6 t\right)+\left(- 9 t^{3}\right)\cdot \left(-2\right)+\left(- 6 t^{3} + 3 t^{2}\right)\cdot \left(-3\right) \\  & =t^{2} \left(108 t - 27\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =(1)^{2} \left(108 (1) - 27\right) \\  & =81.\end{aligned}
$$

## Authored moderate method-operation variant; sine_difference

### sine_difference / sine_difference_operations

Compute the rate of change of the function $f(x,y)=\sin{\left(x - y \right)}$ with respect to $t$ along the curve $r(t)=⟨\sqrt{t},- 3 t⟩$ at the point $t=9.$

- $3 \cos{\left(30 \right)}$
- $\frac{\cos{\left(30 \right)}}{6}$
- $\frac{19 \cos{\left(30 \right)}}{6}$ **correct**
- $- \frac{17 \cos{\left(30 \right)}}{6}$
- $0$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(\sin{\left(x - y \right)}),\frac{∂}{∂y}(\sin{\left(x - y \right)})⟩ \\  & =⟨\cos{\left(x - y \right)},- \cos{\left(x - y \right)}⟩\end{aligned}
$$

Next, we substitute $x=\sqrt{t}$, $y=- 3 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\cos{\left(\sqrt{t} - - 3 t \right)},- \cos{\left(\sqrt{t} - - 3 t \right)}⟩ \\  & =⟨\cos{\left(\sqrt{t} + 3 t \right)},- \cos{\left(\sqrt{t} + 3 t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\sqrt{t}),\frac{\text{d}}{\text{d}t}(- 3 t)⟩ \\  & =⟨\frac{1}{2 \sqrt{t}},-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\cos{\left(\sqrt{t} + 3 t \right)},- \cos{\left(\sqrt{t} + 3 t \right)}⟩\cdot ⟨\frac{1}{2 \sqrt{t}},-3⟩ \\  & =\left(\cos{\left(\sqrt{t} + 3 t \right)}\right)\cdot \left(\frac{1}{2 \sqrt{t}}\right)+\left(- \cos{\left(\sqrt{t} + 3 t \right)}\right)\cdot \left(-3\right) \\  & =\frac{\left(6 \sqrt{t} + 1\right) \cos{\left(\sqrt{t} + 3 t \right)}}{2 \sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=9$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(9))] & =\frac{\left(6 \sqrt{(9)} + 1\right) \cos{\left(\sqrt{(9)} + 3 (9) \right)}}{2 \sqrt{(9)}} \\  & =\frac{19 \cos{\left(30 \right)}}{6}.\end{aligned}
$$

## Authored moderate method-operation variant; sine_difference

### sine_difference / sine_difference_operations

Compute the rate of change of the function $f(x,y)=- 2 \sin{\left(x - y \right)}$ with respect to $t$ along the curve $r(t)=⟨2 \sqrt{t},- 3 t⟩$ at the point $t=1.$

- $- 6 \cos{\left(5 \right)}$
- $0$
- $4 \cos{\left(5 \right)}$
- $- 8 \cos{\left(5 \right)}$ **correct**
- $- 2 \cos{\left(5 \right)}$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- 2 \sin{\left(x - y \right)}),\frac{∂}{∂y}(- 2 \sin{\left(x - y \right)})⟩ \\  & =⟨- 2 \cos{\left(x - y \right)},2 \cos{\left(x - y \right)}⟩\end{aligned}
$$

Next, we substitute $x=2 \sqrt{t}$, $y=- 3 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 2 \cos{\left(2 \sqrt{t} - - 3 t \right)},2 \cos{\left(2 \sqrt{t} - - 3 t \right)}⟩ \\  & =⟨- 2 \cos{\left(2 \sqrt{t} + 3 t \right)},2 \cos{\left(2 \sqrt{t} + 3 t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\frac{\text{d}}{\text{d}t}(- 3 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 2 \cos{\left(2 \sqrt{t} + 3 t \right)},2 \cos{\left(2 \sqrt{t} + 3 t \right)}⟩\cdot ⟨\frac{1}{\sqrt{t}},-3⟩ \\  & =\left(- 2 \cos{\left(2 \sqrt{t} + 3 t \right)}\right)\cdot \left(\frac{1}{\sqrt{t}}\right)+\left(2 \cos{\left(2 \sqrt{t} + 3 t \right)}\right)\cdot \left(-3\right) \\  & =\frac{2 \left(- 3 \sqrt{t} - 1\right) \cos{\left(2 \sqrt{t} + 3 t \right)}}{\sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2 \left(- 3 \sqrt{(1)} - 1\right) \cos{\left(2 \sqrt{(1)} + 3 (1) \right)}}{\sqrt{(1)}} \\  & =- 8 \cos{\left(5 \right)}.\end{aligned}
$$

## Authored moderate method-operation variant; quotient

### quotient / quotient_operations

Compute the rate of change of the function $f(x,y)=\frac{x}{y}$ with respect to $t$ along the curve $r(t)=⟨t,- 3 \sqrt{t}⟩$ at the point $t=9.$

- $\frac{1}{18}$
- $- \frac{1}{9}$
- $- \frac{1}{18}$ **correct**
- $- \frac{1}{6}$
- $- \frac{2}{9}$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(\frac{x}{y}),\frac{∂}{∂y}(\frac{x}{y})⟩ \\  & =⟨\frac{1}{y},- \frac{x}{y^{2}}⟩\end{aligned}
$$

Next, we substitute $x=t$, $y=- 3 \sqrt{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- \frac{1}{3 \sqrt{t}},- \frac{1}{9}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(- 3 \sqrt{t})⟩ \\  & =⟨1,- \frac{3}{2 \sqrt{t}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- \frac{1}{3 \sqrt{t}},- \frac{1}{9}⟩\cdot ⟨1,- \frac{3}{2 \sqrt{t}}⟩ \\  & =\left(- \frac{1}{3 \sqrt{t}}\right)\cdot \left(1\right)+\left(- \frac{1}{9}\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right) \\  & =- \frac{1}{3 \sqrt{t}}+\frac{1}{6 \sqrt{t}} \\  & =- \frac{1}{6 \sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=9$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(9))] & =- \frac{1}{6 \sqrt{(9)}} \\  & =- \frac{1}{18}.\end{aligned}
$$

## Authored moderate method-operation variant; quotient

### quotient / quotient_operations

Compute the rate of change of the function $f(x,y)=- \frac{2 x}{y}$ with respect to $t$ along the curve $r(t)=⟨2 t,- 3 \sqrt{t}⟩$ at the point $t=1.$

- $- \frac{2}{3}$
- $\frac{10}{9}$
- $2$
- $\frac{2}{3}$ **correct**
- $\frac{4}{3}$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- \frac{2 x}{y}),\frac{∂}{∂y}(- \frac{2 x}{y})⟩ \\  & =⟨- \frac{2}{y},\frac{2 x}{y^{2}}⟩\end{aligned}
$$

Next, we substitute $x=2 t$, $y=- 3 \sqrt{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\frac{2}{3 \sqrt{t}},\frac{4}{9}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\frac{\text{d}}{\text{d}t}(- 3 \sqrt{t})⟩ \\  & =⟨2,- \frac{3}{2 \sqrt{t}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\frac{2}{3 \sqrt{t}},\frac{4}{9}⟩\cdot ⟨2,- \frac{3}{2 \sqrt{t}}⟩ \\  & =\left(\frac{2}{3 \sqrt{t}}\right)\cdot \left(2\right)+\left(\frac{4}{9}\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right) \\  & =\frac{4}{3 \sqrt{t}}- \frac{2}{3 \sqrt{t}} \\  & =\frac{2}{3 \sqrt{t}}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2}{3 \sqrt{(1)}} \\  & =\frac{2}{3}.\end{aligned}
$$

## Authored moderate method-operation variant; trig_powers

### trig_powers / trig_powers_operations

Compute the rate of change of the function $f(x,y)=x^{3} + y^{2}$ with respect to $t$ along the curve $r(t)=⟨- 3 \sin{\left(t \right)},2 \cos{\left(t \right)}⟩$ at the point $t=\frac{2 \pi}{3}.$

- $2 \sqrt{3}$
- $\frac{243}{8}$
- $2 \sqrt{3} + \frac{243}{8}$ **correct**
- $- 2 \sqrt{3} + \frac{243}{8}$
- $\frac{73}{4}$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(x^{3} + y^{2}),\frac{∂}{∂y}(x^{3} + y^{2})⟩ \\  & =⟨3 x^{2},2 y⟩\end{aligned}
$$

Next, we substitute $x=- 3 \sin{\left(t \right)}$, $y=2 \cos{\left(t \right)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨27 \sin^{2}{\left(t \right)},4 \cos{\left(t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)}),\frac{\text{d}}{\text{d}t}(2 \cos{\left(t \right)})⟩ \\  & =⟨- 3 \cos{\left(t \right)},- 2 \sin{\left(t \right)}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨27 \sin^{2}{\left(t \right)},4 \cos{\left(t \right)}⟩\cdot ⟨- 3 \cos{\left(t \right)},- 2 \sin{\left(t \right)}⟩ \\  & =\left(27 \sin^{2}{\left(t \right)}\right)\cdot \left(- 3 \cos{\left(t \right)}\right)+\left(4 \cos{\left(t \right)}\right)\cdot \left(- 2 \sin{\left(t \right)}\right) \\  & =- \left(81 \sin{\left(t \right)} + 8\right) \sin{\left(t \right)} \cos{\left(t \right)}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=\frac{2 \pi}{3}$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{2 \pi}{3}))] & =- \left(81 \sin{\left((\frac{2 \pi}{3}) \right)} + 8\right) \sin{\left((\frac{2 \pi}{3}) \right)} \cos{\left((\frac{2 \pi}{3}) \right)} \\  & =\left(\frac{81}{4}\right)\cdot \left(\frac{3}{2}\right)+\left(-2\right)\cdot \left(- \sqrt{3}\right) \\  & =\frac{243}{8}+2 \sqrt{3} \\  & =2 \sqrt{3} + \frac{243}{8}.\end{aligned}
$$

## Authored moderate method-operation variant; trig_powers

### trig_powers / trig_powers_operations

Compute the rate of change of the function $f(x,y)=- 2 x^{3} + 2 y^{2}$ with respect to $t$ along the curve $r(t)=⟨- 3 \sin{\left(t \right)},- 3 \cos{\left(t \right)}⟩$ at the point $t=\frac{2 \pi}{3}.$

- $9 \sqrt{3}$
- $- \frac{69}{2}$
- $- \frac{243}{4} - 9 \sqrt{3}$
- $- \frac{243}{4} + 9 \sqrt{3}$ **correct**
- $- \frac{243}{4}$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- 2 x^{3} + 2 y^{2}),\frac{∂}{∂y}(- 2 x^{3} + 2 y^{2})⟩ \\  & =⟨- 6 x^{2},4 y⟩\end{aligned}
$$

Next, we substitute $x=- 3 \sin{\left(t \right)}$, $y=- 3 \cos{\left(t \right)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 54 \sin^{2}{\left(t \right)},- 12 \cos{\left(t \right)}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)}),\frac{\text{d}}{\text{d}t}(- 3 \cos{\left(t \right)})⟩ \\  & =⟨- 3 \cos{\left(t \right)},3 \sin{\left(t \right)}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 54 \sin^{2}{\left(t \right)},- 12 \cos{\left(t \right)}⟩\cdot ⟨- 3 \cos{\left(t \right)},3 \sin{\left(t \right)}⟩ \\  & =\left(- 54 \sin^{2}{\left(t \right)}\right)\cdot \left(- 3 \cos{\left(t \right)}\right)+\left(- 12 \cos{\left(t \right)}\right)\cdot \left(3 \sin{\left(t \right)}\right) \\  & =18 \left(9 \sin{\left(t \right)} - 2\right) \sin{\left(t \right)} \cos{\left(t \right)}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=\frac{2 \pi}{3}$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{2 \pi}{3}))] & =18 \left(9 \sin{\left((\frac{2 \pi}{3}) \right)} - 2\right) \sin{\left((\frac{2 \pi}{3}) \right)} \cos{\left((\frac{2 \pi}{3}) \right)} \\  & =\left(- \frac{81}{2}\right)\cdot \left(\frac{3}{2}\right)+\left(6\right)\cdot \left(\frac{3 \sqrt{3}}{2}\right) \\  & =- \frac{243}{4}+9 \sqrt{3} \\  & =- \frac{243}{4} + 9 \sqrt{3}.\end{aligned}
$$

## Authored moderate method-operation variant; square_difference

### square_difference / square_difference_operations

Compute the rate of change of the function $f(x,y)=2 x^{2} + 2 y^{2}$ with respect to $t$ along the curve $r(t)=⟨- t^{2},- 3 t + 2⟩$ at the point $t=-1.$

- $-60$
- $-8$
- $-68$ **correct**
- $52$
- $16$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(2 x^{2} + 2 y^{2}),\frac{∂}{∂y}(2 x^{2} + 2 y^{2})⟩ \\  & =⟨4 x,4 y⟩\end{aligned}
$$

Next, we substitute $x=- t^{2}$, $y=- 3 t + 2$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨4 \left(- t^{2}\right),4 \left(- 3 t + 2\right)⟩ \\  & =⟨- 4 t^{2},- 12 t + 8⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t^{2}),\frac{\text{d}}{\text{d}t}(- 3 t + 2)⟩ \\  & =⟨- 2 t,-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 4 t^{2},- 12 t + 8⟩\cdot ⟨- 2 t,-3⟩ \\  & =\left(- 4 t^{2}\right)\cdot \left(- 2 t\right)+\left(- 12 t + 8\right)\cdot \left(-3\right) \\  & =8 t^{3} + 36 t - 24.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=-1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & =8 (-1)^{3} + 36 (-1) - 24 \\  & =-68.\end{aligned}
$$

## Authored moderate method-operation variant; square_difference

### square_difference / square_difference_operations

Compute the rate of change of the function $f(x,y)=x^{2} + 3 y^{2}$ with respect to $t$ along the curve $r(t)=⟨t^{2},2 t - 3⟩$ at the point $t=1.$

- $-12$
- $-4$
- $16$
- $-8$ **correct**
- $4$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(x^{2} + 3 y^{2}),\frac{∂}{∂y}(x^{2} + 3 y^{2})⟩ \\  & =⟨2 x,6 y⟩\end{aligned}
$$

Next, we substitute $x=t^{2}$, $y=2 t - 3$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨2 t^{2},6 \left(2 t - 3\right)⟩ \\  & =⟨2 t^{2},12 t - 18⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\frac{\text{d}}{\text{d}t}(2 t - 3)⟩ \\  & =⟨2 t,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨2 t^{2},12 t - 18⟩\cdot ⟨2 t,2⟩ \\  & =\left(2 t^{2}\right)\cdot \left(2 t\right)+\left(12 t - 18\right)\cdot \left(2\right) \\  & =4 t^{3} + 24 t - 36.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =4 (1)^{3} + 24 (1) - 36 \\  & =-8.\end{aligned}
$$

## Authored hard method-operation variant; triple_product

### triple_product / triple_product_operations

Compute the rate of change of the function $f(x,y,z)=x y z$ with respect to $t$ along the curve $r(t)=⟨t,- 3 \sqrt{t},2 t + 1⟩$ at the point $t=4.$

- $-81$
- $-75$
- $-129$ **correct**
- $-33$
- $-42$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(x y z),\frac{∂}{∂y}(x y z),\frac{∂}{∂z}(x y z)⟩ \\  & =⟨y z,x z,x y⟩\end{aligned}
$$

Next, we substitute $x=t$, $y=- 3 \sqrt{t}$, $z=2 t + 1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 3 \sqrt{t} \left(2 t + 1\right),t \left(2 t + 1\right),- 3 \sqrt{t} t⟩ \\  & =⟨- 6 t^{\frac{3}{2}} - 3 \sqrt{t},2 t^{2} + t,- 3 t^{\frac{3}{2}}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(- 3 \sqrt{t}),\frac{\text{d}}{\text{d}t}(2 t + 1)⟩ \\  & =⟨1,- \frac{3}{2 \sqrt{t}},2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 6 t^{\frac{3}{2}} - 3 \sqrt{t},2 t^{2} + t,- 3 t^{\frac{3}{2}}⟩\cdot ⟨1,- \frac{3}{2 \sqrt{t}},2⟩ \\  & =\left(- 6 t^{\frac{3}{2}} - 3 \sqrt{t}\right)\cdot \left(1\right)+\left(2 t^{2} + t\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right)+\left(- 3 t^{\frac{3}{2}}\right)\cdot \left(2\right) \\  & =\sqrt{t} \left(- 6 t - 3\right)+\sqrt{t} \left(- 3 t - \frac{3}{2}\right)- 6 t^{\frac{3}{2}} \\  & =\sqrt{t} \left(- 15 t - \frac{9}{2}\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=4$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(4))] & =\sqrt{(4)} \left(- 15 (4) - \frac{9}{2}\right) \\  & =-129.\end{aligned}
$$

## Authored hard method-operation variant; triple_product

### triple_product / triple_product_operations

Compute the rate of change of the function $f(x,y,z)=- 2 x y z$ with respect to $t$ along the curve $r(t)=⟨2 t,- 3 \sqrt{t},- 3 t + 1⟩$ at the point $t=4.$

- $-396$
- $140$
- $-108$
- $-684$ **correct**
- $-420$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(- 2 x y z),\frac{∂}{∂y}(- 2 x y z),\frac{∂}{∂z}(- 2 x y z)⟩ \\  & =⟨- 2 y z,- 2 x z,- 2 x y⟩\end{aligned}
$$

Next, we substitute $x=2 t$, $y=- 3 \sqrt{t}$, $z=- 3 t + 1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 2 \left(- 3 \sqrt{t}\right) \left(- 3 t + 1\right),- 2 \cdot 2 t \left(- 3 t + 1\right),- 2 \left(- 3 \sqrt{t}\right) 2 t⟩ \\  & =⟨- 18 t^{\frac{3}{2}} + 6 \sqrt{t},12 t^{2} - 4 t,12 t^{\frac{3}{2}}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\frac{\text{d}}{\text{d}t}(- 3 \sqrt{t}),\frac{\text{d}}{\text{d}t}(- 3 t + 1)⟩ \\  & =⟨2,- \frac{3}{2 \sqrt{t}},-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 18 t^{\frac{3}{2}} + 6 \sqrt{t},12 t^{2} - 4 t,12 t^{\frac{3}{2}}⟩\cdot ⟨2,- \frac{3}{2 \sqrt{t}},-3⟩ \\  & =\left(- 18 t^{\frac{3}{2}} + 6 \sqrt{t}\right)\cdot \left(2\right)+\left(12 t^{2} - 4 t\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right)+\left(12 t^{\frac{3}{2}}\right)\cdot \left(-3\right) \\  & =\sqrt{t} \left(- 36 t + 12\right)+\sqrt{t} \left(- 18 t + 6\right)- 36 t^{\frac{3}{2}} \\  & =\sqrt{t} \left(- 90 t + 18\right).\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=4$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(4))] & =\sqrt{(4)} \left(- 90 (4) + 18\right) \\  & =-684.\end{aligned}
$$

## Authored hard method-operation variant; radical_square

### radical_square / radical_square_operations

Compute the rate of change of the function $f(x,y,z)=x z^{2} + y^{3}$ with respect to $t$ along the curve $r(t)=⟨- 3 t,2,\sqrt{t^{2} - 3}⟩$ at the point $t=2.$

- $-24$
- $-3$
- $-27$ **correct**
- $-39$
- $1$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(x z^{2} + y^{3}),\frac{∂}{∂y}(x z^{2} + y^{3}),\frac{∂}{∂z}(x z^{2} + y^{3})⟩ \\  & =⟨z^{2},3 y^{2},2 x z⟩\end{aligned}
$$

Next, we substitute $x=- 3 t$, $y=2$, $z=\sqrt{t^{2} - 3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\left(\sqrt{t^{2} - 3}\right)^{2},3 \cdot 2^{2},2 \left(- 3 t\right) \sqrt{t^{2} - 3}⟩ \\  & =⟨t^{2} - 3,12,- 6 t \sqrt{t^{2} - 3}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t),\frac{\text{d}}{\text{d}t}(2),\frac{\text{d}}{\text{d}t}(\sqrt{t^{2} - 3})⟩ \\  & =⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨t^{2} - 3,12,- 6 t \sqrt{t^{2} - 3}⟩\cdot ⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩ \\  & =\left(t^{2} - 3\right)\cdot \left(-3\right)+\left(12\right)\cdot \left(0\right)+\left(- 6 t \sqrt{t^{2} - 3}\right)\cdot \left(\frac{t}{\sqrt{t^{2} - 3}}\right) \\  & =- 3 t^{2} + 9+0- 6 t^{2} \\  & =- 9 t^{2} + 9.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =- 9 (2)^{2} + 9 \\  & =-3+0-24 \\  & =-27.\end{aligned}
$$

## Authored hard method-operation variant; radical_square

### radical_square / radical_square_operations

Compute the rate of change of the function $f(x,y,z)=- 2 x z^{2} + 2 y^{3}$ with respect to $t$ along the curve $r(t)=⟨- 3 t,-3,\sqrt{t^{2} - 3}⟩$ at the point $t=2.$

- $48$
- $76$
- $78$
- $54$ **correct**
- $6$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(- 2 x z^{2} + 2 y^{3}),\frac{∂}{∂y}(- 2 x z^{2} + 2 y^{3}),\frac{∂}{∂z}(- 2 x z^{2} + 2 y^{3})⟩ \\  & =⟨- 2 z^{2},6 y^{2},- 4 x z⟩\end{aligned}
$$

Next, we substitute $x=- 3 t$, $y=-3$, $z=\sqrt{t^{2} - 3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 2 \left(\sqrt{t^{2} - 3}\right)^{2},6 \left(-3\right)^{2},- 4 \left(- 3 t\right) \sqrt{t^{2} - 3}⟩ \\  & =⟨- 2 t^{2} + 6,54,12 t \sqrt{t^{2} - 3}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t),\frac{\text{d}}{\text{d}t}(-3),\frac{\text{d}}{\text{d}t}(\sqrt{t^{2} - 3})⟩ \\  & =⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 2 t^{2} + 6,54,12 t \sqrt{t^{2} - 3}⟩\cdot ⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩ \\  & =\left(- 2 t^{2} + 6\right)\cdot \left(-3\right)+\left(54\right)\cdot \left(0\right)+\left(12 t \sqrt{t^{2} - 3}\right)\cdot \left(\frac{t}{\sqrt{t^{2} - 3}}\right) \\  & =6 t^{2} - 18+0+12 t^{2} \\  & =18 t^{2} - 18.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =18 (2)^{2} - 18 \\  & =6+0+48 \\  & =54.\end{aligned}
$$

## Authored hard method-operation variant; log_norm

### log_norm / log_norm_operations

Compute the rate of change of the function $f(x,y,z)=- \ln{\left(x^{2} + y^{2} + z^{2} \right)}$ with respect to $t$ along the curve $r(t)=⟨2 t + 3,-2,- t⟩$ at the point $t=2.$

- $- \frac{4}{57}$
- $- \frac{28}{57}$
- $- \frac{32}{57}$ **correct**
- $- \frac{52}{57}$
- $- \frac{2}{19}$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(- \ln{\left(x^{2} + y^{2} + z^{2} \right)}),\frac{∂}{∂y}(- \ln{\left(x^{2} + y^{2} + z^{2} \right)}),\frac{∂}{∂z}(- \ln{\left(x^{2} + y^{2} + z^{2} \right)})⟩ \\  & =⟨- \frac{2 x}{x^{2} + y^{2} + z^{2}},- \frac{2 y}{x^{2} + y^{2} + z^{2}},- \frac{2 z}{x^{2} + y^{2} + z^{2}}⟩\end{aligned}
$$

Next, we substitute $x=2 t + 3$, $y=-2$, $z=- t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- \frac{2 \left(2 t + 3\right)}{\left(- t\right)^{2} + \left(2 t + 3\right)^{2} + \left(-2\right)^{2}},\left(-2\right) \left(-2\right) \frac{1}{\left(- t\right)^{2} + \left(2 t + 3\right)^{2} + \left(-2\right)^{2}},- \frac{2 \left(- t\right)}{\left(- t\right)^{2} + \left(2 t + 3\right)^{2} + \left(-2\right)^{2}}⟩ \\  & =⟨- \frac{4 t}{5 t^{2} + 12 t + 13} - \frac{6}{5 t^{2} + 12 t + 13},\frac{4}{5 t^{2} + 12 t + 13},\frac{2 t}{5 t^{2} + 12 t + 13}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t + 3),\frac{\text{d}}{\text{d}t}(-2),\frac{\text{d}}{\text{d}t}(- t)⟩ \\  & =⟨2,0,-1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- \frac{4 t}{5 t^{2} + 12 t + 13} - \frac{6}{5 t^{2} + 12 t + 13},\frac{4}{5 t^{2} + 12 t + 13},\frac{2 t}{5 t^{2} + 12 t + 13}⟩\cdot ⟨2,0,-1⟩ \\  & =\left(- \frac{4 t}{5 t^{2} + 12 t + 13} - \frac{6}{5 t^{2} + 12 t + 13}\right)\cdot \left(2\right)+\left(\frac{4}{5 t^{2} + 12 t + 13}\right)\cdot \left(0\right)+\left(\frac{2 t}{5 t^{2} + 12 t + 13}\right)\cdot \left(-1\right) \\  & =\frac{4 \left(- 2 t - 3\right)}{5 t^{2} + 12 t + 13}+0- \frac{2 t}{5 t^{2} + 12 t + 13} \\  & =\frac{2 \left(- 5 t - 6\right)}{5 t^{2} + 12 t + 13}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =\frac{2 \left(- 5 (2) - 6\right)}{5 (2)^{2} + 12 (2) + 13} \\  & =- \frac{28}{57}+0- \frac{4}{57} \\  & =- \frac{32}{57}.\end{aligned}
$$

## Authored hard method-operation variant; log_norm

### log_norm / log_norm_operations

Compute the rate of change of the function $f(x,y,z)=\ln{\left(x^{2} + y^{2} + z^{2} \right)}$ with respect to $t$ along the curve $r(t)=⟨t + 3,-2,- 3 t⟩$ at the point $t=1.$

- $\frac{18}{29}$
- $- \frac{2}{29}$
- $- \frac{46}{29}$
- $\frac{26}{29}$ **correct**
- $\frac{8}{29}$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\ln{\left(x^{2} + y^{2} + z^{2} \right)}),\frac{∂}{∂y}(\ln{\left(x^{2} + y^{2} + z^{2} \right)}),\frac{∂}{∂z}(\ln{\left(x^{2} + y^{2} + z^{2} \right)})⟩ \\  & =⟨\frac{2 x}{x^{2} + y^{2} + z^{2}},\frac{2 y}{x^{2} + y^{2} + z^{2}},\frac{2 z}{x^{2} + y^{2} + z^{2}}⟩\end{aligned}
$$

Next, we substitute $x=t + 3$, $y=-2$, $z=- 3 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨\frac{2 \left(t + 3\right)}{\left(- 3 t\right)^{2} + \left(t + 3\right)^{2} + \left(-2\right)^{2}},2 \left(-2\right) \frac{1}{\left(- 3 t\right)^{2} + \left(t + 3\right)^{2} + \left(-2\right)^{2}},\frac{2 \left(- 3 t\right)}{\left(- 3 t\right)^{2} + \left(t + 3\right)^{2} + \left(-2\right)^{2}}⟩ \\  & =⟨\frac{2 t}{10 t^{2} + 6 t + 13} + \frac{6}{10 t^{2} + 6 t + 13},- \frac{4}{10 t^{2} + 6 t + 13},- \frac{6 t}{10 t^{2} + 6 t + 13}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t + 3),\frac{\text{d}}{\text{d}t}(-2),\frac{\text{d}}{\text{d}t}(- 3 t)⟩ \\  & =⟨1,0,-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨\frac{2 t}{10 t^{2} + 6 t + 13} + \frac{6}{10 t^{2} + 6 t + 13},- \frac{4}{10 t^{2} + 6 t + 13},- \frac{6 t}{10 t^{2} + 6 t + 13}⟩\cdot ⟨1,0,-3⟩ \\  & =\left(\frac{2 t}{10 t^{2} + 6 t + 13} + \frac{6}{10 t^{2} + 6 t + 13}\right)\cdot \left(1\right)+\left(- \frac{4}{10 t^{2} + 6 t + 13}\right)\cdot \left(0\right)+\left(- \frac{6 t}{10 t^{2} + 6 t + 13}\right)\cdot \left(-3\right) \\  & =\frac{2 \left(t + 3\right)}{10 t^{2} + 6 t + 13}+0+\frac{18 t}{10 t^{2} + 6 t + 13} \\  & =\frac{2 \left(10 t + 3\right)}{10 t^{2} + 6 t + 13}.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2 \left(10 (1) + 3\right)}{10 (1)^{2} + 6 (1) + 13} \\  & =\frac{8}{29}+0+\frac{18}{29} \\  & =\frac{26}{29}.\end{aligned}
$$

## Authored easy method-operation variant; quadratic_affine

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=- x^{2} + y^{2}$ with respect to $t$ along the curve $r(t)=⟨- t - 2,2 t - 2⟩$ at the point $t=2.$

- $8$
- $-8$
- $0$ **correct**
- $-16$
- $12$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- x^{2} + y^{2}),\frac{∂}{∂y}(- x^{2} + y^{2})⟩ \\  & =⟨- 2 x,2 y⟩\end{aligned}
$$

Next, we substitute $x=- t - 2$, $y=2 t - 2$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 2 \left(- t - 2\right),2 \left(2 t - 2\right)⟩ \\  & =⟨2 t + 4,4 t - 4⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t - 2),\frac{\text{d}}{\text{d}t}(2 t - 2)⟩ \\  & =⟨-1,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨2 t + 4,4 t - 4⟩\cdot ⟨-1,2⟩ \\  & =\left(2 t + 4\right)\cdot \left(-1\right)+\left(4 t - 4\right)\cdot \left(2\right) \\  & =6 t - 12.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =6 (2) - 12 \\  & =0.\end{aligned}
$$

## Authored easy method-operation variant; quadratic_affine

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=- 2 x^{2} + 2 y^{2}$ with respect to $t$ along the curve $r(t)=⟨- 3 t - 3,t + 3⟩$ at the point $t=0.$

- $12$
- $24$
- $-48$
- $-24$ **correct**
- $-36$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- 2 x^{2} + 2 y^{2}),\frac{∂}{∂y}(- 2 x^{2} + 2 y^{2})⟩ \\  & =⟨- 4 x,4 y⟩\end{aligned}
$$

Next, we substitute $x=- 3 t - 3$, $y=t + 3$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 4 \left(- 3 t - 3\right),4 \left(t + 3\right)⟩ \\  & =⟨12 t + 12,4 t + 12⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t - 3),\frac{\text{d}}{\text{d}t}(t + 3)⟩ \\  & =⟨-3,1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨12 t + 12,4 t + 12⟩\cdot ⟨-3,1⟩ \\  & =\left(12 t + 12\right)\cdot \left(-3\right)+\left(4 t + 12\right)\cdot \left(1\right) \\  & =- 32 t - 24.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =- 32 (0) - 24 \\  & =-24.\end{aligned}
$$
