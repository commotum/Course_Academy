# KP 17592186124470 review

Original captured records are in source.json. Raw replay preserves original attribute absences; separately labeled records provide authored completions.

## Authored missing-attribute completion pair_products

If $f(x, y, z) = xy + yz + xz$ and $r(t) = ti + e^{t}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $e^{t + 1} + (1 + t)e^{t} + e$
- $e^{t + 1} + (1 + 2t)e^{t} + e$
- $e^{t + 1} + te^{t} + e$
- $e^{t + 1} + (t + 1)e^{t} + 2$
- $2e^{t} + 2e + t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(x y + x z + y z)\,i+\frac{∂}{∂y}(x y + x z + y z)\,j+\frac{∂}{∂z}(x y + x z + y z)\,k \\  & =(y + z)\,i+(x + z)\,j+(x + y)\,k\end{aligned}
$$

Next, we substitute $x=t,y=e^{t},$ and $z=e$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(e^{t} + e)\,i+(t + e)\,j+(t + e^{t})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(e^{t})\,j+\frac{\text{d}}{\text{d}t}(e)\,k \\  & =(1)\,i+(e^{t})\,j+(0)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{t} + e)\,i+(t + e)\,j+(t + e^{t})\,k)\cdot ((1)\,i+(e^{t})\,j+(0)\,k) \\  & =(e^{t} + e)\cdot (1)+(t + e)\cdot (e^{t})+(t + e^{t})\cdot (0) \\  & =(e^{t} + e)+(\left(t + e\right) e^{t})+(0) \\  & =t e^{t} + e^{t} + e e^{t} + e.\end{aligned}
$$

## Original replay pair_products

If $f(x, y, z) = xy + yz + xz$ and $r(t) = ti + e^{t}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $e^{t + 1} + (1 + t)e^{t} + e$
- $e^{t + 1} + (1 + 2t)e^{t} + e$
- $e^{t + 1} + te^{t} + e$
- $e^{t + 1} + (t + 1)e^{t} + 2$
- $2e^{t} + 2e + t$

[Original source has no worked-solution attribute.]

## Generated observed-pattern variant pair_products 0

If $f(x, y, z) = -2\left(xy + yz + xz\right)$ and $r(t) = (t + 1)i + e^{(t + 1)}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $-2\left(e^{(t + 1) + 1} + (1 + (t + 1))e^{(t + 1)} + e\right)$
- $-2\left(e^{(t + 1) + 1} + (1 + 2(t + 1))e^{(t + 1)} + e\right)$
- $-2\left(e^{(t + 1) + 1} + (t + 1)e^{(t + 1)} + e\right)$
- $-2\left(e^{(t + 1) + 1} + ((t + 1) + 1)e^{(t + 1)} + 2\right)$
- $-2\left(2e^{(t + 1)} + 2e + (t + 1)\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(- 2 x y - 2 x z - 2 y z)\,i+\frac{∂}{∂y}(- 2 x y - 2 x z - 2 y z)\,j+\frac{∂}{∂z}(- 2 x y - 2 x z - 2 y z)\,k \\  & =(- 2 y - 2 z)\,i+(- 2 x - 2 z)\,j+(- 2 x - 2 y)\,k\end{aligned}
$$

Next, we substitute $x=t + 1,y=e^{t + 1},$ and $z=e$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(- 2 e^{t + 1} - 2 e)\,i+(- 2 t - 2 e - 2)\,j+(- 2 t - 2 e^{t + 1} - 2)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t + 1)\,i+\frac{\text{d}}{\text{d}t}(e^{t + 1})\,j+\frac{\text{d}}{\text{d}t}(e)\,k \\  & =(1)\,i+(e^{t + 1})\,j+(0)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((- 2 e^{t + 1} - 2 e)\,i+(- 2 t - 2 e - 2)\,j+(- 2 t - 2 e^{t + 1} - 2)\,k)\cdot ((1)\,i+(e^{t + 1})\,j+(0)\,k) \\  & =(- 2 e^{t + 1} - 2 e)\cdot (1)+(- 2 t - 2 e - 2)\cdot (e^{t + 1})+(- 2 t - 2 e^{t + 1} - 2)\cdot (0) \\  & =(- 2 e^{t + 1} - 2 e)+(\left(- 2 t - 2 e - 2\right) e^{t + 1})+(0) \\  & =- 2 e \left(t e^{t} + 2 e^{t} + e e^{t} + 1\right).\end{aligned}
$$

## Generated observed-pattern variant pair_products 1

If $f(x, y, z) = 2\left(xy + yz + xz\right)$ and $r(t) = (t - 1)i + e^{(t - 1)}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $2\left(e^{(t - 1) + 1} + (1 + (t - 1))e^{(t - 1)} + e\right)$
- $2\left(e^{(t - 1) + 1} + (1 + 2(t - 1))e^{(t - 1)} + e\right)$
- $2\left(e^{(t - 1) + 1} + (t - 1)e^{(t - 1)} + e\right)$
- $2\left(e^{(t - 1) + 1} + ((t - 1) + 1)e^{(t - 1)} + 2\right)$
- $2\left(2e^{(t - 1)} + 2e + (t - 1)\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2 x y + 2 x z + 2 y z)\,i+\frac{∂}{∂y}(2 x y + 2 x z + 2 y z)\,j+\frac{∂}{∂z}(2 x y + 2 x z + 2 y z)\,k \\  & =(2 y + 2 z)\,i+(2 x + 2 z)\,j+(2 x + 2 y)\,k\end{aligned}
$$

Next, we substitute $x=t - 1,y=e^{t - 1},$ and $z=e$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2 e^{t - 1} + 2 e)\,i+(2 t - 2 + 2 e)\,j+(2 t + 2 e^{t - 1} - 2)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t - 1)\,i+\frac{\text{d}}{\text{d}t}(e^{t - 1})\,j+\frac{\text{d}}{\text{d}t}(e)\,k \\  & =(1)\,i+(e^{t - 1})\,j+(0)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2 e^{t - 1} + 2 e)\,i+(2 t - 2 + 2 e)\,j+(2 t + 2 e^{t - 1} - 2)\,k)\cdot ((1)\,i+(e^{t - 1})\,j+(0)\,k) \\  & =(2 e^{t - 1} + 2 e)\cdot (1)+(2 t - 2 + 2 e)\cdot (e^{t - 1})+(2 t + 2 e^{t - 1} - 2)\cdot (0) \\  & =(2 e^{t - 1} + 2 e)+(\left(2 t - 2 + 2 e\right) e^{t - 1})+(0) \\  & =2 \left(\frac{t e^{t}}{e} + e^{t} + e\right).\end{aligned}
$$

## Authored missing-attribute completion trig_product

If $f(x, y, z) = z(x + y)$ and $r(t) = \sin ti + \cos tj + e^{t}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $0$
- $2e^{t} + \sin t + \cos t$
- $2e^{t}\sin t$
- $2e^{t}\cos t$
- $2e^{t}(\sin t + \cos t)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(z \left(x + y\right))\,i+\frac{∂}{∂y}(z \left(x + y\right))\,j+\frac{∂}{∂z}(z \left(x + y\right))\,k \\  & =(z)\,i+(z)\,j+(x + y)\,k\end{aligned}
$$

Next, we substitute $x=\sin{\left(t \right)},y=\cos{\left(t \right)},$ and $z=e^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(e^{t})\,i+(e^{t})\,j+(\sin{\left(t \right)} + \cos{\left(t \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)})\,j+\frac{\text{d}}{\text{d}t}(e^{t})\,k \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j+(e^{t})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{t})\,i+(e^{t})\,j+(\sin{\left(t \right)} + \cos{\left(t \right)})\,k)\cdot ((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j+(e^{t})\,k) \\  & =(e^{t})\cdot (\cos{\left(t \right)})+(e^{t})\cdot (- \sin{\left(t \right)})+(\sin{\left(t \right)} + \cos{\left(t \right)})\cdot (e^{t}) \\  & =(e^{t} \cos{\left(t \right)})+(- e^{t} \sin{\left(t \right)})+(\left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}) \\  & =2 e^{t} \cos{\left(t \right)}.\end{aligned}
$$

## Original replay trig_product

If $f(x, y, z) = z(x + y)$ and $r(t) = \sin ti + \cos tj + e^{t}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $0$
- $2e^{t} + \sin t + \cos t$
- $2e^{t}\sin t$
- $2e^{t}\cos t$
- $2e^{t}(\sin t + \cos t)$

[Original source has no worked-solution attribute.]

## Generated observed-pattern variant trig_product 0

If $f(x, y, z) = -2\left(z(x + y)\right)$ and $r(t) = \sin (t + 1)i + \cos (t + 1)j + e^{(t + 1)}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $-2\left(0\right)$
- $-2\left(2e^{(t + 1)} + \sin (t + 1) + \cos (t + 1)\right)$
- $-2\left(2e^{(t + 1)}\sin (t + 1)\right)$
- $-2\left(2e^{(t + 1)}\cos (t + 1)\right)$
- $-2\left(2e^{(t + 1)}(\sin (t + 1) + \cos (t + 1))\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(- 2 z \left(x + y\right))\,i+\frac{∂}{∂y}(- 2 z \left(x + y\right))\,j+\frac{∂}{∂z}(- 2 z \left(x + y\right))\,k \\  & =(- 2 z)\,i+(- 2 z)\,j+(- 2 x - 2 y)\,k\end{aligned}
$$

Next, we substitute $x=\sin{\left(t + 1 \right)},y=\cos{\left(t + 1 \right)},$ and $z=e^{t + 1}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(- 2 e^{t + 1})\,i+(- 2 e^{t + 1})\,j+(- 2 \sin{\left(t + 1 \right)} - 2 \cos{\left(t + 1 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sin{\left(t + 1 \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t + 1 \right)})\,j+\frac{\text{d}}{\text{d}t}(e^{t + 1})\,k \\  & =(\cos{\left(t + 1 \right)})\,i+(- \sin{\left(t + 1 \right)})\,j+(e^{t + 1})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((- 2 e^{t + 1})\,i+(- 2 e^{t + 1})\,j+(- 2 \sin{\left(t + 1 \right)} - 2 \cos{\left(t + 1 \right)})\,k)\cdot ((\cos{\left(t + 1 \right)})\,i+(- \sin{\left(t + 1 \right)})\,j+(e^{t + 1})\,k) \\  & =(- 2 e^{t + 1})\cdot (\cos{\left(t + 1 \right)})+(- 2 e^{t + 1})\cdot (- \sin{\left(t + 1 \right)})+(- 2 \sin{\left(t + 1 \right)} - 2 \cos{\left(t + 1 \right)})\cdot (e^{t + 1}) \\  & =(- 2 e^{t + 1} \cos{\left(t + 1 \right)})+(2 e^{t + 1} \sin{\left(t + 1 \right)})+(\left(- 2 \sin{\left(t + 1 \right)} - 2 \cos{\left(t + 1 \right)}\right) e^{t + 1}) \\  & =- 4 e e^{t} \cos{\left(t + 1 \right)}.\end{aligned}
$$

## Generated observed-pattern variant trig_product 1

If $f(x, y, z) = 2\left(z(x + y)\right)$ and $r(t) = \sin (t - 1)i + \cos (t - 1)j + e^{(t - 1)}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $2\left(0\right)$
- $2\left(2e^{(t - 1)} + \sin (t - 1) + \cos (t - 1)\right)$
- $2\left(2e^{(t - 1)}\sin (t - 1)\right)$
- $2\left(2e^{(t - 1)}\cos (t - 1)\right)$
- $2\left(2e^{(t - 1)}(\sin (t - 1) + \cos (t - 1))\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2 z \left(x + y\right))\,i+\frac{∂}{∂y}(2 z \left(x + y\right))\,j+\frac{∂}{∂z}(2 z \left(x + y\right))\,k \\  & =(2 z)\,i+(2 z)\,j+(2 x + 2 y)\,k\end{aligned}
$$

Next, we substitute $x=\sin{\left(t - 1 \right)},y=\cos{\left(t - 1 \right)},$ and $z=e^{t - 1}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2 e^{t - 1})\,i+(2 e^{t - 1})\,j+(2 \sin{\left(t - 1 \right)} + 2 \cos{\left(t - 1 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sin{\left(t - 1 \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t - 1 \right)})\,j+\frac{\text{d}}{\text{d}t}(e^{t - 1})\,k \\  & =(\cos{\left(t - 1 \right)})\,i+(- \sin{\left(t - 1 \right)})\,j+(e^{t - 1})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2 e^{t - 1})\,i+(2 e^{t - 1})\,j+(2 \sin{\left(t - 1 \right)} + 2 \cos{\left(t - 1 \right)})\,k)\cdot ((\cos{\left(t - 1 \right)})\,i+(- \sin{\left(t - 1 \right)})\,j+(e^{t - 1})\,k) \\  & =(2 e^{t - 1})\cdot (\cos{\left(t - 1 \right)})+(2 e^{t - 1})\cdot (- \sin{\left(t - 1 \right)})+(2 \sin{\left(t - 1 \right)} + 2 \cos{\left(t - 1 \right)})\cdot (e^{t - 1}) \\  & =(2 e^{t - 1} \cos{\left(t - 1 \right)})+(- 2 e^{t - 1} \sin{\left(t - 1 \right)})+(\left(2 \sin{\left(t - 1 \right)} + 2 \cos{\left(t - 1 \right)}\right) e^{t - 1}) \\  & =\frac{4 e^{t} \cos{\left(t - 1 \right)}}{e}.\end{aligned}
$$

## Original replay constant_coordinate

If $f(x,y,z)=x{y}^{2}+y{z}^{3}$ and $r(t)={t}^{3}\,i+\,j+t\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $6{t}^{2}$
- ${t}^{2}+2t$
- $3{t}^{2}+3t$
- ${t}^{3}+3{t}^{2}$
- $3{t}^{2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(x{y}^{2}+y{z}^{3})\,i+\frac{∂}{∂y}(x{y}^{2}+y{z}^{3})\,j+\frac{∂}{∂z}(x{y}^{2}+y{z}^{3})\,k \\  & ={y}^{2}\,i+(2xy+{z}^{3})\,j+3y{z}^{2}\,k\end{aligned}
$$

Next, we substitute $x={t}^{3},y=1,$ and $z=t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\,i+3{t}^{3}\,j+3{t}^{2}\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3})\,i+\frac{\text{d}}{\text{d}t}(1)\,j+\frac{\text{d}}{\text{d}t}(t)\,k \\  & =3{t}^{2}i+(0)\,j+\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\,i+3{t}^{3}\,j+3{t}^{2}\,k)\cdot (3{t}^{2}i+(0)\,j+\,k) \\  & =1\cdot 3{t}^{2}+3{t}^{3}\cdot 0+3{t}^{2}\cdot 1 \\  & =3{t}^{2}+3{t}^{2} \\  & =6{t}^{2}.\end{aligned}
$$

## Generated observed-pattern variant constant_coordinate 0

If $f(x,y,z)=-2\left(x{y}^{2}+y{z}^{3}\right)$ and $r(t)={(t + 1)}^{3}\,i+\,j+(t + 1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left(6{(t + 1)}^{2}\right)$
- $-2\left({(t + 1)}^{2}+2(t + 1)\right)$
- $-2\left(3{(t + 1)}^{2}+3(t + 1)\right)$
- $-2\left({(t + 1)}^{3}+3{(t + 1)}^{2}\right)$
- $-2\left(3{(t + 1)}^{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-2\left(x{y}^{2}+y{z}^{3}\right))\,i+\frac{∂}{∂y}(-2\left(x{y}^{2}+y{z}^{3}\right))\,j+\frac{∂}{∂z}(-2\left(x{y}^{2}+y{z}^{3}\right))\,k \\  & =(-2\left({y}^{2}\right))\,i+(-2\left(+(2xy+{z}^{3})\right))\,j+(-2\left(+3y{z}^{2}\right))\,k\end{aligned}
$$

Next, we substitute $x={(t + 1)}^{3},y=1,$ and $z=(t + 1)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left(1\right))\,i+(-2\left(+3{(t + 1)}^{3}\right))\,j+(-2\left(+3{(t + 1)}^{2}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t + 1)}^{3})\,i+\frac{\text{d}}{\text{d}t}(1)\,j+\frac{\text{d}}{\text{d}t}((t + 1))\,k \\  & =(3{(t + 1)}^{2})\,i+(+(0))\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(1\right))\,i+(-2\left(+3{(t + 1)}^{3}\right))\,j+(-2\left(+3{(t + 1)}^{2}\right))\,k)\cdot ((3{(t + 1)}^{2})\,i+(+(0))\,j+(1)\,k) \\  & =-2\left(1\cdot 3{(t + 1)}^{2}+3{(t + 1)}^{3}\cdot 0+3{(t + 1)}^{2}\cdot 1\right) \\  & =-2\left(3{(t + 1)}^{2}+3{(t + 1)}^{2}\right) \\  & =-2\left(6{(t + 1)}^{2}\right).\end{aligned}
$$

## Generated observed-pattern variant constant_coordinate 1

If $f(x,y,z)=2\left(x{y}^{2}+y{z}^{3}\right)$ and $r(t)={(t - 1)}^{3}\,i+\,j+(t - 1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left(6{(t - 1)}^{2}\right)$
- $2\left({(t - 1)}^{2}+2(t - 1)\right)$
- $2\left(3{(t - 1)}^{2}+3(t - 1)\right)$
- $2\left({(t - 1)}^{3}+3{(t - 1)}^{2}\right)$
- $2\left(3{(t - 1)}^{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2\left(x{y}^{2}+y{z}^{3}\right))\,i+\frac{∂}{∂y}(2\left(x{y}^{2}+y{z}^{3}\right))\,j+\frac{∂}{∂z}(2\left(x{y}^{2}+y{z}^{3}\right))\,k \\  & =(2\left({y}^{2}\right))\,i+(2\left(+(2xy+{z}^{3})\right))\,j+(2\left(+3y{z}^{2}\right))\,k\end{aligned}
$$

Next, we substitute $x={(t - 1)}^{3},y=1,$ and $z=(t - 1)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left(1\right))\,i+(2\left(+3{(t - 1)}^{3}\right))\,j+(2\left(+3{(t - 1)}^{2}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t - 1)}^{3})\,i+\frac{\text{d}}{\text{d}t}(1)\,j+\frac{\text{d}}{\text{d}t}((t - 1))\,k \\  & =(3{(t - 1)}^{2})\,i+(+(0))\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(1\right))\,i+(2\left(+3{(t - 1)}^{3}\right))\,j+(2\left(+3{(t - 1)}^{2}\right))\,k)\cdot ((3{(t - 1)}^{2})\,i+(+(0))\,j+(1)\,k) \\  & =2\left(1\cdot 3{(t - 1)}^{2}+3{(t - 1)}^{3}\cdot 0+3{(t - 1)}^{2}\cdot 1\right) \\  & =2\left(3{(t - 1)}^{2}+3{(t - 1)}^{2}\right) \\  & =2\left(6{(t - 1)}^{2}\right).\end{aligned}
$$

## Original replay quartic_trig

If $f(x,y,z)={x}^{4}-{y}^{4}-\operatorname{cos}⁡z$ and $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+2t\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\operatorname{cos}⁡t{sin}^{3}⁡t$
- $\operatorname{sin}⁡2t{cos}^{3}⁡2t$
- $4\operatorname{sin}⁡2t$
- ${cos}^{2}⁡t$
- $0$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,i+\frac{∂}{∂y}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,j+\frac{∂}{∂z}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,k \\  & =4{x}^{3}\,i-4{y}^{3}\,j+\operatorname{sin}⁡z\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡t,$ $y=\operatorname{cos}⁡t$ and $z=2t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4{sin}^{3}⁡t\,i-4{cos}^{3}⁡t\,j+\operatorname{sin}⁡2t\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(2t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(4{sin}^{3}⁡t\,i-4{cos}^{3}⁡t\,j+\operatorname{sin}⁡2t\,k)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\,k) \\  & =4{sin}^{3}⁡t\cdot \operatorname{cos}⁡t-4{cos}^{3}⁡t\cdot (-\operatorname{sin}⁡t)+\operatorname{sin}⁡2t\cdot 2 \\  & =4{sin}^{3}⁡t\operatorname{cos}⁡t+4{cos}^{3}⁡t\operatorname{sin}⁡t+2\operatorname{sin}⁡2t \\  & =4\operatorname{sin}⁡t\operatorname{cos}⁡t({sin}^{2}⁡t+{cos}^{2}⁡t)+2\operatorname{sin}⁡2t \\  & =4\operatorname{sin}⁡t\operatorname{cos}⁡t+2\operatorname{sin}⁡2t \\  & =2\operatorname{sin}⁡2t+2\operatorname{sin}⁡2t \\  & =4\operatorname{sin}⁡2t.\end{aligned}
$$

## Generated observed-pattern variant quartic_trig 0

If $f(x,y,z)=-2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right)$ and $r(t)=\operatorname{sin}⁡(t + 1)\,i+\operatorname{cos}⁡(t + 1)\,j+2(t + 1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left(\operatorname{cos}⁡(t + 1){sin}^{3}⁡(t + 1)\right)$
- $-2\left(\operatorname{sin}⁡2(t + 1){cos}^{3}⁡2(t + 1)\right)$
- $-2\left(4\operatorname{sin}⁡2(t + 1)\right)$
- $-2\left({cos}^{2}⁡(t + 1)\right)$
- $-2\left(0\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,i+\frac{∂}{∂y}(-2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,j+\frac{∂}{∂z}(-2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,k \\  & =(-2\left(4{x}^{3}\right))\,i+(-2\left(-4{y}^{3}\right))\,j+(-2\left(+\operatorname{sin}⁡z\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t + 1),$ $y=\operatorname{cos}⁡(t + 1)$ and $z=2(t + 1)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left(4{sin}^{3}⁡(t + 1)\right))\,i+(-2\left(-4{cos}^{3}⁡(t + 1)\right))\,j+(-2\left(+\operatorname{sin}⁡2(t + 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t + 1))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t + 1))\,j+\frac{\text{d}}{\text{d}t}(2(t + 1))\,k \\  & =(\operatorname{cos}⁡(t + 1))\,i+(-\operatorname{sin}⁡(t + 1))\,j+(+2)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(4{sin}^{3}⁡(t + 1)\right))\,i+(-2\left(-4{cos}^{3}⁡(t + 1)\right))\,j+(-2\left(+\operatorname{sin}⁡2(t + 1)\right))\,k)\cdot ((\operatorname{cos}⁡(t + 1))\,i+(-\operatorname{sin}⁡(t + 1))\,j+(+2)\,k) \\  & =-2\left(4{sin}^{3}⁡(t + 1)\cdot \operatorname{cos}⁡(t + 1)-4{cos}^{3}⁡(t + 1)\cdot (-\operatorname{sin}⁡(t + 1))+\operatorname{sin}⁡2(t + 1)\cdot 2\right) \\  & =-2\left(4{sin}^{3}⁡(t + 1)\operatorname{cos}⁡(t + 1)+4{cos}^{3}⁡(t + 1)\operatorname{sin}⁡(t + 1)+2\operatorname{sin}⁡2(t + 1)\right) \\  & =-2\left(4\operatorname{sin}⁡(t + 1)\operatorname{cos}⁡(t + 1)({sin}^{2}⁡(t + 1)+{cos}^{2}⁡(t + 1))+2\operatorname{sin}⁡2(t + 1)\right) \\  & =-2\left(4\operatorname{sin}⁡(t + 1)\operatorname{cos}⁡(t + 1)+2\operatorname{sin}⁡2(t + 1)\right) \\  & =-2\left(2\operatorname{sin}⁡2(t + 1)+2\operatorname{sin}⁡2(t + 1)\right) \\  & =-2\left(4\operatorname{sin}⁡2(t + 1)\right).\end{aligned}
$$

## Generated observed-pattern variant quartic_trig 1

If $f(x,y,z)=2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right)$ and $r(t)=\operatorname{sin}⁡(t - 1)\,i+\operatorname{cos}⁡(t - 1)\,j+2(t - 1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left(\operatorname{cos}⁡(t - 1){sin}^{3}⁡(t - 1)\right)$
- $2\left(\operatorname{sin}⁡2(t - 1){cos}^{3}⁡2(t - 1)\right)$
- $2\left(4\operatorname{sin}⁡2(t - 1)\right)$
- $2\left({cos}^{2}⁡(t - 1)\right)$
- $2\left(0\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,i+\frac{∂}{∂y}(2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,j+\frac{∂}{∂z}(2\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,k \\  & =(2\left(4{x}^{3}\right))\,i+(2\left(-4{y}^{3}\right))\,j+(2\left(+\operatorname{sin}⁡z\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t - 1),$ $y=\operatorname{cos}⁡(t - 1)$ and $z=2(t - 1)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left(4{sin}^{3}⁡(t - 1)\right))\,i+(2\left(-4{cos}^{3}⁡(t - 1)\right))\,j+(2\left(+\operatorname{sin}⁡2(t - 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t - 1))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t - 1))\,j+\frac{\text{d}}{\text{d}t}(2(t - 1))\,k \\  & =(\operatorname{cos}⁡(t - 1))\,i+(-\operatorname{sin}⁡(t - 1))\,j+(+2)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(4{sin}^{3}⁡(t - 1)\right))\,i+(2\left(-4{cos}^{3}⁡(t - 1)\right))\,j+(2\left(+\operatorname{sin}⁡2(t - 1)\right))\,k)\cdot ((\operatorname{cos}⁡(t - 1))\,i+(-\operatorname{sin}⁡(t - 1))\,j+(+2)\,k) \\  & =2\left(4{sin}^{3}⁡(t - 1)\cdot \operatorname{cos}⁡(t - 1)-4{cos}^{3}⁡(t - 1)\cdot (-\operatorname{sin}⁡(t - 1))+\operatorname{sin}⁡2(t - 1)\cdot 2\right) \\  & =2\left(4{sin}^{3}⁡(t - 1)\operatorname{cos}⁡(t - 1)+4{cos}^{3}⁡(t - 1)\operatorname{sin}⁡(t - 1)+2\operatorname{sin}⁡2(t - 1)\right) \\  & =2\left(4\operatorname{sin}⁡(t - 1)\operatorname{cos}⁡(t - 1)({sin}^{2}⁡(t - 1)+{cos}^{2}⁡(t - 1))+2\operatorname{sin}⁡2(t - 1)\right) \\  & =2\left(4\operatorname{sin}⁡(t - 1)\operatorname{cos}⁡(t - 1)+2\operatorname{sin}⁡2(t - 1)\right) \\  & =2\left(2\operatorname{sin}⁡2(t - 1)+2\operatorname{sin}⁡2(t - 1)\right) \\  & =2\left(4\operatorname{sin}⁡2(t - 1)\right).\end{aligned}
$$

## Original replay log_product

If $f(x,y,z)=\operatorname{ln}⁡(xyz)$ and $r(t)=t\,i+{e}^{t-1}\,j+{e}^{t}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2{e}^{t-1}(1-t)$
- $\frac{{e}^{t}+1}{t}$
- $\frac{2t{e}^{t}+1}{t}$
- $3$
- $\frac{2t+1}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xyz))\,i+\frac{∂}{∂y}(\operatorname{ln}⁡(xyz))\,j+\frac{∂}{∂z}(\operatorname{ln}⁡(xyz))\,k \\  & =\frac{yz}{xyz}\,i+\frac{xz}{xyz}\,j+\frac{xy}{xyz}\,k \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j+\frac{1}{z}\,k\end{aligned}
$$

Next, we substitute $x=t,y={e}^{t-1},$ and $z={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{t}\,i+\frac{1}{{e}^{t-1}}\,j+\frac{1}{{e}^{t}}\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t-1})\,j+\frac{\text{d}}{\text{d}t}({e}^{t})\,k \\  & =i+{e}^{t-1}\,j+{e}^{t}\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{t}\,i+\frac{1}{{e}^{t-1}}\,j+\frac{1}{{e}^{t}}\,k)\cdot (i+{e}^{t-1}\,j+{e}^{t}\,k) \\  & =\frac{1}{t}+\frac{{e}^{t-1}}{{e}^{t-1}}+\frac{{e}^{t}}{{e}^{t}} \\  & =\frac{1}{t}+2 \\  & =\frac{2t+1}{t}.\end{aligned}
$$

## Generated observed-pattern variant log_product 0

If $f(x,y,z)=-2\left(\operatorname{ln}⁡(xyz)\right)$ and $r(t)=(t + 1)\,i+{e}^{(t + 1)-1}\,j+{e}^{(t + 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left(2{e}^{(t + 1)-1}(1-(t + 1))\right)$
- $-2\left(\frac{{e}^{(t + 1)}+1}{(t + 1)}\right)$
- $-2\left(\frac{2(t + 1){e}^{(t + 1)}+1}{(t + 1)}\right)$
- $-2\left(3\right)$
- $-2\left(\frac{2(t + 1)+1}{(t + 1)}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-2\left(\operatorname{ln}⁡(xyz)\right))\,i+\frac{∂}{∂y}(-2\left(\operatorname{ln}⁡(xyz)\right))\,j+\frac{∂}{∂z}(-2\left(\operatorname{ln}⁡(xyz)\right))\,k \\  & =(-2\left(\frac{yz}{xyz}\right))\,i+(-2\left(+\frac{xz}{xyz}\right))\,j+(-2\left(+\frac{xy}{xyz}\right))\,k \\  & =(-2\left(\frac{1}{x}\right))\,i+(-2\left(+\frac{1}{y}\right))\,j+(-2\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=(t + 1),y={e}^{(t + 1)-1},$ and $z={e}^{(t + 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left(\frac{1}{(t + 1)}\right))\,i+(-2\left(+\frac{1}{{e}^{(t + 1)-1}}\right))\,j+(-2\left(+\frac{1}{{e}^{(t + 1)}}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}((t + 1))\,i+\frac{\text{d}}{\text{d}t}({e}^{(t + 1)-1})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t + 1)})\,k \\  & =(1)\,i+(+{e}^{(t + 1)-1})\,j+(+{e}^{(t + 1)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(\frac{1}{(t + 1)}\right))\,i+(-2\left(+\frac{1}{{e}^{(t + 1)-1}}\right))\,j+(-2\left(+\frac{1}{{e}^{(t + 1)}}\right))\,k)\cdot ((1)\,i+(+{e}^{(t + 1)-1})\,j+(+{e}^{(t + 1)})\,k) \\  & =-2\left(\frac{1}{(t + 1)}+\frac{{e}^{(t + 1)-1}}{{e}^{(t + 1)-1}}+\frac{{e}^{(t + 1)}}{{e}^{(t + 1)}}\right) \\  & =-2\left(\frac{1}{(t + 1)}+2\right) \\  & =-2\left(\frac{2(t + 1)+1}{(t + 1)}\right).\end{aligned}
$$

## Generated observed-pattern variant log_product 1

If $f(x,y,z)=2\left(\operatorname{ln}⁡(xyz)\right)$ and $r(t)=(t - 1)\,i+{e}^{(t - 1)-1}\,j+{e}^{(t - 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left(2{e}^{(t - 1)-1}(1-(t - 1))\right)$
- $2\left(\frac{{e}^{(t - 1)}+1}{(t - 1)}\right)$
- $2\left(\frac{2(t - 1){e}^{(t - 1)}+1}{(t - 1)}\right)$
- $2\left(3\right)$
- $2\left(\frac{2(t - 1)+1}{(t - 1)}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2\left(\operatorname{ln}⁡(xyz)\right))\,i+\frac{∂}{∂y}(2\left(\operatorname{ln}⁡(xyz)\right))\,j+\frac{∂}{∂z}(2\left(\operatorname{ln}⁡(xyz)\right))\,k \\  & =(2\left(\frac{yz}{xyz}\right))\,i+(2\left(+\frac{xz}{xyz}\right))\,j+(2\left(+\frac{xy}{xyz}\right))\,k \\  & =(2\left(\frac{1}{x}\right))\,i+(2\left(+\frac{1}{y}\right))\,j+(2\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=(t - 1),y={e}^{(t - 1)-1},$ and $z={e}^{(t - 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left(\frac{1}{(t - 1)}\right))\,i+(2\left(+\frac{1}{{e}^{(t - 1)-1}}\right))\,j+(2\left(+\frac{1}{{e}^{(t - 1)}}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}((t - 1))\,i+\frac{\text{d}}{\text{d}t}({e}^{(t - 1)-1})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t - 1)})\,k \\  & =(1)\,i+(+{e}^{(t - 1)-1})\,j+(+{e}^{(t - 1)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(\frac{1}{(t - 1)}\right))\,i+(2\left(+\frac{1}{{e}^{(t - 1)-1}}\right))\,j+(2\left(+\frac{1}{{e}^{(t - 1)}}\right))\,k)\cdot ((1)\,i+(+{e}^{(t - 1)-1})\,j+(+{e}^{(t - 1)})\,k) \\  & =2\left(\frac{1}{(t - 1)}+\frac{{e}^{(t - 1)-1}}{{e}^{(t - 1)-1}}+\frac{{e}^{(t - 1)}}{{e}^{(t - 1)}}\right) \\  & =2\left(\frac{1}{(t - 1)}+2\right) \\  & =2\left(\frac{2(t - 1)+1}{(t - 1)}\right).\end{aligned}
$$

## Original replay log_difference

If $f(x,y,z)=x({y}^{2}-{z}^{2})$ and $r(t)=\operatorname{ln}⁡t\,i+(t+1)\,j+(t-1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $4(t-\operatorname{ln}⁡t)$
- $4+4t+{t}^{2}\operatorname{ln}⁡t$
- $4t(t-\operatorname{ln}⁡t)$
- $4(\operatorname{ln}⁡t+1)$
- $4t(t-1)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}[x({y}^{2}-{z}^{2})]\,i+\frac{∂}{∂y}[x({y}^{2}-{z}^{2})]\,j+\frac{∂}{∂z}[x({y}^{2}-{z}^{2})]\,k \\  & =({y}^{2}-{z}^{2})\,i+2xy\,j-2xz\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t,$ $y=t+1$ and $z=t-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =[(t+1)^{2}-(t-1)^{2}]i+2\operatorname{ln}⁡t\cdot (t+1)\,j-2\operatorname{ln}⁡t\cdot (t-1)\,k \\  & =4t\,i+2(t+1)\operatorname{ln}⁡t\,j-2(t-1)\operatorname{ln}⁡t\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}(t+1)\,j+\frac{\text{d}}{\text{d}t}(t-1)\,k \\  & =\frac{1}{t}\,i+\,j+\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(4t\,i+2(t+1)\operatorname{ln}⁡t\,j-2(t-1)\operatorname{ln}⁡t\,k)\cdot (\frac{1}{t}\,i+\,j+\,k) \\  & =4t\cdot \frac{1}{t}+2(t+1)\operatorname{ln}⁡t\cdot 1-2(t-1)\operatorname{ln}⁡t\cdot 1 \\  & =4+2(t+1)\operatorname{ln}⁡t-2(t-1)\operatorname{ln}⁡t \\  & =4+4\operatorname{ln}⁡t \\  & =4(\operatorname{ln}⁡t+1).\end{aligned}
$$

## Generated observed-pattern variant log_difference 0

If $f(x,y,z)=-2\left(x({y}^{2}-{z}^{2})\right)$ and $r(t)=\operatorname{ln}⁡(t + 1)\,i+((t + 1)+1)\,j+((t + 1)-1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left(4((t + 1)-\operatorname{ln}⁡(t + 1))\right)$
- $-2\left(4+4(t + 1)+{(t + 1)}^{2}\operatorname{ln}⁡(t + 1)\right)$
- $-2\left(4(t + 1)((t + 1)-\operatorname{ln}⁡(t + 1))\right)$
- $-2\left(4(\operatorname{ln}⁡(t + 1)+1)\right)$
- $-2\left(4(t + 1)((t + 1)-1)\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}[-2\left(x({y}^{2}-{z}^{2})\right)]\,i+\frac{∂}{∂y}[-2\left(x({y}^{2}-{z}^{2})\right)]\,j+\frac{∂}{∂z}[-2\left(x({y}^{2}-{z}^{2})\right)]\,k \\  & =(-2\left(({y}^{2}-{z}^{2})\right))\,i+(-2\left(+2xy\right))\,j+(-2\left(-2xz\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡(t + 1),$ $y=(t + 1)+1$ and $z=(t + 1)-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left([((t + 1)+1)^{2}-((t + 1)-1)^{2}]\right))\,i+(-2\left(+2\operatorname{ln}⁡(t + 1)\cdot ((t + 1)+1)\right))\,j+(-2\left(-2\operatorname{ln}⁡(t + 1)\cdot ((t + 1)-1)\right))\,k \\  & =(-2\left(4(t + 1)\right))\,i+(-2\left(+2((t + 1)+1)\operatorname{ln}⁡(t + 1)\right))\,j+(-2\left(-2((t + 1)-1)\operatorname{ln}⁡(t + 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t + 1))\,i+\frac{\text{d}}{\text{d}t}((t + 1)+1)\,j+\frac{\text{d}}{\text{d}t}((t + 1)-1)\,k \\  & =(\frac{1}{(t + 1)})\,i+(1)\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(4(t + 1)\right))\,i+(-2\left(+2((t + 1)+1)\operatorname{ln}⁡(t + 1)\right))\,j+(-2\left(-2((t + 1)-1)\operatorname{ln}⁡(t + 1)\right))\,k)\cdot ((\frac{1}{(t + 1)})\,i+(1)\,j+(1)\,k) \\  & =-2\left(4(t + 1)\cdot \frac{1}{(t + 1)}+2((t + 1)+1)\operatorname{ln}⁡(t + 1)\cdot 1-2((t + 1)-1)\operatorname{ln}⁡(t + 1)\cdot 1\right) \\  & =-2\left(4+2((t + 1)+1)\operatorname{ln}⁡(t + 1)-2((t + 1)-1)\operatorname{ln}⁡(t + 1)\right) \\  & =-2\left(4+4\operatorname{ln}⁡(t + 1)\right) \\  & =-2\left(4(\operatorname{ln}⁡(t + 1)+1)\right).\end{aligned}
$$

## Generated observed-pattern variant log_difference 1

If $f(x,y,z)=2\left(x({y}^{2}-{z}^{2})\right)$ and $r(t)=\operatorname{ln}⁡(t - 1)\,i+((t - 1)+1)\,j+((t - 1)-1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left(4((t - 1)-\operatorname{ln}⁡(t - 1))\right)$
- $2\left(4+4(t - 1)+{(t - 1)}^{2}\operatorname{ln}⁡(t - 1)\right)$
- $2\left(4(t - 1)((t - 1)-\operatorname{ln}⁡(t - 1))\right)$
- $2\left(4(\operatorname{ln}⁡(t - 1)+1)\right)$
- $2\left(4(t - 1)((t - 1)-1)\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}[2\left(x({y}^{2}-{z}^{2})\right)]\,i+\frac{∂}{∂y}[2\left(x({y}^{2}-{z}^{2})\right)]\,j+\frac{∂}{∂z}[2\left(x({y}^{2}-{z}^{2})\right)]\,k \\  & =(2\left(({y}^{2}-{z}^{2})\right))\,i+(2\left(+2xy\right))\,j+(2\left(-2xz\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡(t - 1),$ $y=(t - 1)+1$ and $z=(t - 1)-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left([((t - 1)+1)^{2}-((t - 1)-1)^{2}]\right))\,i+(2\left(+2\operatorname{ln}⁡(t - 1)\cdot ((t - 1)+1)\right))\,j+(2\left(-2\operatorname{ln}⁡(t - 1)\cdot ((t - 1)-1)\right))\,k \\  & =(2\left(4(t - 1)\right))\,i+(2\left(+2((t - 1)+1)\operatorname{ln}⁡(t - 1)\right))\,j+(2\left(-2((t - 1)-1)\operatorname{ln}⁡(t - 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t - 1))\,i+\frac{\text{d}}{\text{d}t}((t - 1)+1)\,j+\frac{\text{d}}{\text{d}t}((t - 1)-1)\,k \\  & =(\frac{1}{(t - 1)})\,i+(1)\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(4(t - 1)\right))\,i+(2\left(+2((t - 1)+1)\operatorname{ln}⁡(t - 1)\right))\,j+(2\left(-2((t - 1)-1)\operatorname{ln}⁡(t - 1)\right))\,k)\cdot ((\frac{1}{(t - 1)})\,i+(1)\,j+(1)\,k) \\  & =2\left(4(t - 1)\cdot \frac{1}{(t - 1)}+2((t - 1)+1)\operatorname{ln}⁡(t - 1)\cdot 1-2((t - 1)-1)\operatorname{ln}⁡(t - 1)\cdot 1\right) \\  & =2\left(4+2((t - 1)+1)\operatorname{ln}⁡(t - 1)-2((t - 1)-1)\operatorname{ln}⁡(t - 1)\right) \\  & =2\left(4+4\operatorname{ln}⁡(t - 1)\right) \\  & =2\left(4(\operatorname{ln}⁡(t - 1)+1)\right).\end{aligned}
$$

## Original replay exponential_cosine

If $f(x,y,z)=yz\operatorname{cos}⁡x$ and $r(t)={t}^{2}\,i+{e}^{t}\,j+{e}^{t}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- ${e}^{2t}(\operatorname{sin}⁡t-\operatorname{cos}⁡t)$
- $2{e}^{2t}$
- ${e}^{2t}\operatorname{cos}⁡t$
- $2{e}^{2t}(\operatorname{cos}⁡{t}^{2}-t\operatorname{sin}⁡{t}^{2})$
- ${e}^{2t}(2\operatorname{cos}⁡{t}^{2}-\operatorname{sin}⁡{t}^{2})$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(yz\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(yz\operatorname{cos}⁡x)\,j+\frac{∂}{∂z}(yz\operatorname{cos}⁡x)\,k \\  & =-yz\operatorname{sin}⁡x\,i+z\operatorname{cos}⁡x\,j+y\operatorname{cos}⁡x\,k\end{aligned}
$$

Next, we substitute $x={t}^{2},y={e}^{t},$ and $z={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{2t}\operatorname{sin}⁡{t}^{2}\,i+{e}^{t}\operatorname{cos}⁡{t}^{2}\,j+{e}^{t}\operatorname{cos}⁡{t}^{2}\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j+\frac{\text{d}}{\text{d}t}({e}^{t})\,k \\  & =2t\,i+{e}^{t}\,j+{e}^{t}\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{2t}\operatorname{sin}⁡{t}^{2}\,i+{e}^{t}\operatorname{cos}⁡{t}^{2}\,j+{e}^{t}\operatorname{cos}⁡{t}^{2}\,k)\cdot (2t\,i+{e}^{t}\,j+{e}^{t}\,k) \\  & =-2t{e}^{2t}\operatorname{sin}⁡{t}^{2}+{e}^{t}\operatorname{cos}⁡{t}^{2}\cdot {e}^{t}+{e}^{t}\operatorname{cos}⁡{t}^{2}\cdot {e}^{t} \\  & =-2t{e}^{2t}\operatorname{sin}⁡{t}^{2}+2{e}^{2t}\operatorname{cos}⁡{t}^{2} \\  & =2{e}^{2t}(\operatorname{cos}⁡{t}^{2}-t\operatorname{sin}⁡{t}^{2}).\end{aligned}
$$

## Generated observed-pattern variant exponential_cosine 0

If $f(x,y,z)=-2\left(yz\operatorname{cos}⁡x\right)$ and $r(t)={(t + 1)}^{2}\,i+{e}^{(t + 1)}\,j+{e}^{(t + 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left({e}^{2(t + 1)}(\operatorname{sin}⁡(t + 1)-\operatorname{cos}⁡(t + 1))\right)$
- $-2\left(2{e}^{2(t + 1)}\right)$
- $-2\left({e}^{2(t + 1)}\operatorname{cos}⁡(t + 1)\right)$
- $-2\left(2{e}^{2(t + 1)}(\operatorname{cos}⁡({(t + 1)}^{2})-(t + 1)\operatorname{sin}⁡({(t + 1)}^{2}))\right)$
- $-2\left({e}^{2(t + 1)}(2\operatorname{cos}⁡({(t + 1)}^{2})-\operatorname{sin}⁡({(t + 1)}^{2}))\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-2\left(yz\operatorname{cos}⁡x\right))\,i+\frac{∂}{∂y}(-2\left(yz\operatorname{cos}⁡x\right))\,j+\frac{∂}{∂z}(-2\left(yz\operatorname{cos}⁡x\right))\,k \\  & =(-2\left(-yz\operatorname{sin}⁡x\right))\,i+(-2\left(+z\operatorname{cos}⁡x\right))\,j+(-2\left(+y\operatorname{cos}⁡x\right))\,k\end{aligned}
$$

Next, we substitute $x={(t + 1)}^{2},y={e}^{(t + 1)},$ and $z={e}^{(t + 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left(-{e}^{2(t + 1)}\operatorname{sin}⁡({(t + 1)}^{2})\right))\,i+(-2\left(+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\right))\,j+(-2\left(+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t + 1)}^{2})\,i+\frac{\text{d}}{\text{d}t}({e}^{(t + 1)})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t + 1)})\,k \\  & =(2(t + 1))\,i+(+{e}^{(t + 1)})\,j+(+{e}^{(t + 1)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(-{e}^{2(t + 1)}\operatorname{sin}⁡({(t + 1)}^{2})\right))\,i+(-2\left(+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\right))\,j+(-2\left(+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\right))\,k)\cdot ((2(t + 1))\,i+(+{e}^{(t + 1)})\,j+(+{e}^{(t + 1)})\,k) \\  & =-2\left(-2(t + 1){e}^{2(t + 1)}\operatorname{sin}⁡({(t + 1)}^{2})+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\cdot {e}^{(t + 1)}+{e}^{(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\cdot {e}^{(t + 1)}\right) \\  & =-2\left(-2(t + 1){e}^{2(t + 1)}\operatorname{sin}⁡({(t + 1)}^{2})+2{e}^{2(t + 1)}\operatorname{cos}⁡({(t + 1)}^{2})\right) \\  & =-2\left(2{e}^{2(t + 1)}(\operatorname{cos}⁡({(t + 1)}^{2})-(t + 1)\operatorname{sin}⁡({(t + 1)}^{2}))\right).\end{aligned}
$$

## Generated observed-pattern variant exponential_cosine 1

If $f(x,y,z)=2\left(yz\operatorname{cos}⁡x\right)$ and $r(t)={(t - 1)}^{2}\,i+{e}^{(t - 1)}\,j+{e}^{(t - 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left({e}^{2(t - 1)}(\operatorname{sin}⁡(t - 1)-\operatorname{cos}⁡(t - 1))\right)$
- $2\left(2{e}^{2(t - 1)}\right)$
- $2\left({e}^{2(t - 1)}\operatorname{cos}⁡(t - 1)\right)$
- $2\left(2{e}^{2(t - 1)}(\operatorname{cos}⁡({(t - 1)}^{2})-(t - 1)\operatorname{sin}⁡({(t - 1)}^{2}))\right)$
- $2\left({e}^{2(t - 1)}(2\operatorname{cos}⁡({(t - 1)}^{2})-\operatorname{sin}⁡({(t - 1)}^{2}))\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2\left(yz\operatorname{cos}⁡x\right))\,i+\frac{∂}{∂y}(2\left(yz\operatorname{cos}⁡x\right))\,j+\frac{∂}{∂z}(2\left(yz\operatorname{cos}⁡x\right))\,k \\  & =(2\left(-yz\operatorname{sin}⁡x\right))\,i+(2\left(+z\operatorname{cos}⁡x\right))\,j+(2\left(+y\operatorname{cos}⁡x\right))\,k\end{aligned}
$$

Next, we substitute $x={(t - 1)}^{2},y={e}^{(t - 1)},$ and $z={e}^{(t - 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left(-{e}^{2(t - 1)}\operatorname{sin}⁡({(t - 1)}^{2})\right))\,i+(2\left(+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\right))\,j+(2\left(+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t - 1)}^{2})\,i+\frac{\text{d}}{\text{d}t}({e}^{(t - 1)})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t - 1)})\,k \\  & =(2(t - 1))\,i+(+{e}^{(t - 1)})\,j+(+{e}^{(t - 1)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(-{e}^{2(t - 1)}\operatorname{sin}⁡({(t - 1)}^{2})\right))\,i+(2\left(+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\right))\,j+(2\left(+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\right))\,k)\cdot ((2(t - 1))\,i+(+{e}^{(t - 1)})\,j+(+{e}^{(t - 1)})\,k) \\  & =2\left(-2(t - 1){e}^{2(t - 1)}\operatorname{sin}⁡({(t - 1)}^{2})+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\cdot {e}^{(t - 1)}+{e}^{(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\cdot {e}^{(t - 1)}\right) \\  & =2\left(-2(t - 1){e}^{2(t - 1)}\operatorname{sin}⁡({(t - 1)}^{2})+2{e}^{2(t - 1)}\operatorname{cos}⁡({(t - 1)}^{2})\right) \\  & =2\left(2{e}^{2(t - 1)}(\operatorname{cos}⁡({(t - 1)}^{2})-(t - 1)\operatorname{sin}⁡({(t - 1)}^{2}))\right).\end{aligned}
$$

## Original replay log_exp

If $f(x,y,z)=\operatorname{ln}⁡(xz)+{e}^{y}$ and $r(t)=\operatorname{sin}⁡t\,i+{t}^{2}\,j+\frac{1}{t}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\operatorname{cot}⁡t+2t{e}^{{t}^{2}}-\frac{1}{t}$
- $\operatorname{csc}⁡t+2t{e}^{{t}^{2}}$
- $\operatorname{csc}⁡t+{e}^{{t}^{2}}+t$
- $\operatorname{tan}⁡t+\frac{{e}^{{t}^{2}}}{{t}^{2}}$
- $\operatorname{cot}⁡t+{e}^{{t}^{2}}-1$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xz)+{e}^{y})\,i+\frac{∂}{∂y}(\operatorname{ln}⁡(xz)+{e}^{y})\,j+\frac{∂}{∂z}(\operatorname{ln}⁡(xz)+{e}^{y})\,k \\  & =\frac{1}{x}\,i+{e}^{y}\,j+\frac{1}{z}\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡t,y={t}^{2},$ and $z=\frac{1}{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\operatorname{sin}⁡t}\,i+{e}^{{t}^{2}}\,j+t\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{1}{t})k \\  & =\operatorname{cos}⁡t\,i+2t\,j-\frac{1}{{t}^{2}}\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\operatorname{sin}⁡t}\,i+{e}^{{t}^{2}}\,j+t\,k)\cdot (\operatorname{cos}⁡t\,i+2t\,j-\frac{1}{{t}^{2}}\,k) \\  & =\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}+2t{e}^{{t}^{2}}-\frac{t}{{t}^{2}} \\  & =\operatorname{cot}⁡t+2t{e}^{{t}^{2}}-\frac{1}{t}.\end{aligned}
$$

## Generated observed-pattern variant log_exp 0

If $f(x,y,z)=-2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right)$ and $r(t)=\operatorname{sin}⁡(t + 1)\,i+{(t + 1)}^{2}\,j+\frac{1}{(t + 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $-2\left(\operatorname{cot}⁡(t + 1)+2(t + 1){e}^{{(t + 1)}^{2}}-\frac{1}{(t + 1)}\right)$
- $-2\left(\operatorname{csc}⁡(t + 1)+2(t + 1){e}^{{(t + 1)}^{2}}\right)$
- $-2\left(\operatorname{csc}⁡(t + 1)+{e}^{{(t + 1)}^{2}}+(t + 1)\right)$
- $-2\left(\operatorname{tan}⁡(t + 1)+\frac{{e}^{{(t + 1)}^{2}}}{{(t + 1)}^{2}}\right)$
- $-2\left(\operatorname{cot}⁡(t + 1)+{e}^{{(t + 1)}^{2}}-1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,i+\frac{∂}{∂y}(-2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,j+\frac{∂}{∂z}(-2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,k \\  & =(-2\left(\frac{1}{x}\right))\,i+(-2\left(+{e}^{y}\right))\,j+(-2\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t + 1),y={(t + 1)}^{2},$ and $z=\frac{1}{(t + 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-2\left(\frac{1}{\operatorname{sin}⁡(t + 1)}\right))\,i+(-2\left(+{e}^{{(t + 1)}^{2}}\right))\,j+(-2\left(+(t + 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t + 1))\,i+\frac{\text{d}}{\text{d}t}({(t + 1)}^{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{1}{(t + 1)})k \\  & =(\operatorname{cos}⁡(t + 1))\,i+(+2(t + 1))\,j+(-\frac{1}{{(t + 1)}^{2}})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-2\left(\frac{1}{\operatorname{sin}⁡(t + 1)}\right))\,i+(-2\left(+{e}^{{(t + 1)}^{2}}\right))\,j+(-2\left(+(t + 1)\right))\,k)\cdot ((\operatorname{cos}⁡(t + 1))\,i+(+2(t + 1))\,j+(-\frac{1}{{(t + 1)}^{2}})\,k) \\  & =-2\left(\frac{\operatorname{cos}⁡(t + 1)}{\operatorname{sin}⁡(t + 1)}+2(t + 1){e}^{{(t + 1)}^{2}}-\frac{(t + 1)}{{(t + 1)}^{2}}\right) \\  & =-2\left(\operatorname{cot}⁡(t + 1)+2(t + 1){e}^{{(t + 1)}^{2}}-\frac{1}{(t + 1)}\right).\end{aligned}
$$

## Generated observed-pattern variant log_exp 1

If $f(x,y,z)=2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right)$ and $r(t)=\operatorname{sin}⁡(t - 1)\,i+{(t - 1)}^{2}\,j+\frac{1}{(t - 1)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2\left(\operatorname{cot}⁡(t - 1)+2(t - 1){e}^{{(t - 1)}^{2}}-\frac{1}{(t - 1)}\right)$
- $2\left(\operatorname{csc}⁡(t - 1)+2(t - 1){e}^{{(t - 1)}^{2}}\right)$
- $2\left(\operatorname{csc}⁡(t - 1)+{e}^{{(t - 1)}^{2}}+(t - 1)\right)$
- $2\left(\operatorname{tan}⁡(t - 1)+\frac{{e}^{{(t - 1)}^{2}}}{{(t - 1)}^{2}}\right)$
- $2\left(\operatorname{cot}⁡(t - 1)+{e}^{{(t - 1)}^{2}}-1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,i+\frac{∂}{∂y}(2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,j+\frac{∂}{∂z}(2\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,k \\  & =(2\left(\frac{1}{x}\right))\,i+(2\left(+{e}^{y}\right))\,j+(2\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t - 1),y={(t - 1)}^{2},$ and $z=\frac{1}{(t - 1)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2\left(\frac{1}{\operatorname{sin}⁡(t - 1)}\right))\,i+(2\left(+{e}^{{(t - 1)}^{2}}\right))\,j+(2\left(+(t - 1)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t - 1))\,i+\frac{\text{d}}{\text{d}t}({(t - 1)}^{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{1}{(t - 1)})k \\  & =(\operatorname{cos}⁡(t - 1))\,i+(+2(t - 1))\,j+(-\frac{1}{{(t - 1)}^{2}})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2\left(\frac{1}{\operatorname{sin}⁡(t - 1)}\right))\,i+(2\left(+{e}^{{(t - 1)}^{2}}\right))\,j+(2\left(+(t - 1)\right))\,k)\cdot ((\operatorname{cos}⁡(t - 1))\,i+(+2(t - 1))\,j+(-\frac{1}{{(t - 1)}^{2}})\,k) \\  & =2\left(\frac{\operatorname{cos}⁡(t - 1)}{\operatorname{sin}⁡(t - 1)}+2(t - 1){e}^{{(t - 1)}^{2}}-\frac{(t - 1)}{{(t - 1)}^{2}}\right) \\  & =2\left(\operatorname{cot}⁡(t - 1)+2(t - 1){e}^{{(t - 1)}^{2}}-\frac{1}{(t - 1)}\right).\end{aligned}
$$

## Generated default easy affine_polynomial 19

If $f(x,y,z)=3 x - 3 y + 2 z$ and $r(t)=(t)\,i+(t^{2})\,j+(t)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $5 - 6 t$
- $5$
- $3 \left(1 - 2 t\right)$
- $2 \left(1 - 3 t\right)$
- $t \left(5 - 3 t\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3 x - 3 y + 2 z)\,i+\frac{∂}{∂y}(3 x - 3 y + 2 z)\,j+\frac{∂}{∂z}(3 x - 3 y + 2 z)\,k \\  & =(3)\,i+(-3)\,j+(2)\,k\end{aligned}
$$

Next, we substitute $x=t,y=t^{2},$ and $z=t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3)\,i+(-3)\,j+(2)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j+\frac{\text{d}}{\text{d}t}(t)\,k \\  & =(1)\,i+(2 t)\,j+(1)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3)\,i+(-3)\,j+(2)\,k)\cdot ((1)\,i+(2 t)\,j+(1)\,k) \\  & =(3)\cdot (1)+(-3)\cdot (2 t)+(2)\cdot (1) \\  & =(3)+(- 6 t)+(2) \\  & =5 - 6 t.\end{aligned}
$$

## Generated default easy affine_polynomial 44

If $f(x,y,z)=x + 2 y + 2 z$ and $r(t)=(t)\,i+(t^{2})\,j+(t)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $3$
- $t \left(2 t + 3\right)$
- $4 t + 3$
- $4 t + 1$
- $2 \left(2 t + 1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(x + 2 y + 2 z)\,i+\frac{∂}{∂y}(x + 2 y + 2 z)\,j+\frac{∂}{∂z}(x + 2 y + 2 z)\,k \\  & =(1)\,i+(2)\,j+(2)\,k\end{aligned}
$$

Next, we substitute $x=t,y=t^{2},$ and $z=t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(1)\,i+(2)\,j+(2)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j+\frac{\text{d}}{\text{d}t}(t)\,k \\  & =(1)\,i+(2 t)\,j+(1)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((1)\,i+(2)\,j+(2)\,k)\cdot ((1)\,i+(2 t)\,j+(1)\,k) \\  & =(1)\cdot (1)+(2)\cdot (2 t)+(2)\cdot (1) \\  & =(1)+(4 t)+(2) \\  & =4 t + 3.\end{aligned}
$$

## Generated default moderate pair_products 19

If $f(x, y, z) = 3\left(xy + yz + xz\right)$ and $r(t) = (t - 2)i + e^{(t - 2)}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{3 \left(\frac{t}{e} - \frac{2}{e} + 1\right) e^{t}}{e}$
- $6 \left(\frac{t e^{t}}{e^{2}} + e t - \frac{2 e^{t}}{e^{2}} + \frac{e^{t}}{e} - 2 e\right)$
- $3 \left(\frac{e^{t}}{e^{2}} + e\right)$
- $3 \left(\frac{t e^{t}}{e^{2}} - \frac{e^{t}}{e^{2}} + \frac{e^{t}}{e} + e\right)$
- $6 \left(t + \frac{e^{t}}{e^{2}} - 2 + e\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3 x y + 3 x z + 3 y z)\,i+\frac{∂}{∂y}(3 x y + 3 x z + 3 y z)\,j+\frac{∂}{∂z}(3 x y + 3 x z + 3 y z)\,k \\  & =(3 y + 3 z)\,i+(3 x + 3 z)\,j+(3 x + 3 y)\,k\end{aligned}
$$

Next, we substitute $x=t - 2,y=e^{t - 2},$ and $z=e$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3 e^{t - 2} + 3 e)\,i+(3 t - 6 + 3 e)\,j+(3 t + 3 e^{t - 2} - 6)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t - 2)\,i+\frac{\text{d}}{\text{d}t}(e^{t - 2})\,j+\frac{\text{d}}{\text{d}t}(e)\,k \\  & =(1)\,i+(e^{t - 2})\,j+(0)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3 e^{t - 2} + 3 e)\,i+(3 t - 6 + 3 e)\,j+(3 t + 3 e^{t - 2} - 6)\,k)\cdot ((1)\,i+(e^{t - 2})\,j+(0)\,k) \\  & =(3 e^{t - 2} + 3 e)\cdot (1)+(3 t - 6 + 3 e)\cdot (e^{t - 2})+(3 t + 3 e^{t - 2} - 6)\cdot (0) \\  & =(3 e^{t - 2} + 3 e)+(\left(3 t - 6 + 3 e\right) e^{t - 2})+(0) \\  & =3 \left(\frac{t e^{t}}{e^{2}} - \frac{e^{t}}{e^{2}} + \frac{e^{t}}{e} + e\right).\end{aligned}
$$

## Generated default moderate pair_products 44

If $f(x, y, z) = xy + yz + xz$ and $r(t) = (t + 2)i + e^{(t + 2)}j + ek$, compute $\frac{d}{dt}[f(r(t))]$.

- $e \left(e e^{t} + 1\right)$
- $\left(t + 2 + e\right) e^{2} e^{t}$
- $2 e \left(e t e^{t} + t + 2 e e^{t} + e^{2} e^{t} + 2\right)$
- $e \left(e t e^{t} + e^{2} e^{t} + 3 e e^{t} + 1\right)$
- $2 \left(t + e^{2} e^{t} + 2 + e\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(x y + x z + y z)\,i+\frac{∂}{∂y}(x y + x z + y z)\,j+\frac{∂}{∂z}(x y + x z + y z)\,k \\  & =(y + z)\,i+(x + z)\,j+(x + y)\,k\end{aligned}
$$

Next, we substitute $x=t + 2,y=e^{t + 2},$ and $z=e$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(e^{t + 2} + e)\,i+(t + 2 + e)\,j+(t + e^{t + 2} + 2)\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t + 2)\,i+\frac{\text{d}}{\text{d}t}(e^{t + 2})\,j+\frac{\text{d}}{\text{d}t}(e)\,k \\  & =(1)\,i+(e^{t + 2})\,j+(0)\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{t + 2} + e)\,i+(t + 2 + e)\,j+(t + e^{t + 2} + 2)\,k)\cdot ((1)\,i+(e^{t + 2})\,j+(0)\,k) \\  & =(e^{t + 2} + e)\cdot (1)+(t + 2 + e)\cdot (e^{t + 2})+(t + e^{t + 2} + 2)\cdot (0) \\  & =(e^{t + 2} + e)+(\left(t + 2 + e\right) e^{t + 2})+(0) \\  & =e \left(e t e^{t} + e^{2} e^{t} + 3 e e^{t} + 1\right).\end{aligned}
$$

## Generated default moderate trig_product 19

If $f(x, y, z) = 3\left(z(x + y)\right)$ and $r(t) = \sin (t - 2)i + \cos (t - 2)j + e^{(t - 2)}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{3 e^{t} \cos{\left(t - 2 \right)}}{e^{2}}$
- $\frac{3 \left(- \sin{\left(t - 2 \right)} + \cos{\left(t - 2 \right)}\right) e^{t}}{e^{2}}$
- $\frac{3 \left(\sin{\left(t - 2 \right)} + 2 \cos{\left(t - 2 \right)}\right) e^{t}}{e^{2}}$
- $\frac{6 e^{t} \cos{\left(t - 2 \right)}}{e^{2}}$
- $\frac{6 \left(\sin{\left(t - 2 \right)} + \cos{\left(t - 2 \right)}\right) e^{t}}{e^{2}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3 z \left(x + y\right))\,i+\frac{∂}{∂y}(3 z \left(x + y\right))\,j+\frac{∂}{∂z}(3 z \left(x + y\right))\,k \\  & =(3 z)\,i+(3 z)\,j+(3 x + 3 y)\,k\end{aligned}
$$

Next, we substitute $x=\sin{\left(t - 2 \right)},y=\cos{\left(t - 2 \right)},$ and $z=e^{t - 2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3 e^{t - 2})\,i+(3 e^{t - 2})\,j+(3 \sin{\left(t - 2 \right)} + 3 \cos{\left(t - 2 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sin{\left(t - 2 \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t - 2 \right)})\,j+\frac{\text{d}}{\text{d}t}(e^{t - 2})\,k \\  & =(\cos{\left(t - 2 \right)})\,i+(- \sin{\left(t - 2 \right)})\,j+(e^{t - 2})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3 e^{t - 2})\,i+(3 e^{t - 2})\,j+(3 \sin{\left(t - 2 \right)} + 3 \cos{\left(t - 2 \right)})\,k)\cdot ((\cos{\left(t - 2 \right)})\,i+(- \sin{\left(t - 2 \right)})\,j+(e^{t - 2})\,k) \\  & =(3 e^{t - 2})\cdot (\cos{\left(t - 2 \right)})+(3 e^{t - 2})\cdot (- \sin{\left(t - 2 \right)})+(3 \sin{\left(t - 2 \right)} + 3 \cos{\left(t - 2 \right)})\cdot (e^{t - 2}) \\  & =(3 e^{t - 2} \cos{\left(t - 2 \right)})+(- 3 e^{t - 2} \sin{\left(t - 2 \right)})+(\left(3 \sin{\left(t - 2 \right)} + 3 \cos{\left(t - 2 \right)}\right) e^{t - 2}) \\  & =\frac{6 e^{t} \cos{\left(t - 2 \right)}}{e^{2}}.\end{aligned}
$$

## Generated default moderate trig_product 44

If $f(x, y, z) = z(x + y)$ and $r(t) = \sin (t + 2)i + \cos (t + 2)j + e^{(t + 2)}k$, compute $\frac{d}{dt}[f(r(t))]$.

- $\left(\sin{\left(t + 2 \right)} + 2 \cos{\left(t + 2 \right)}\right) e^{2} e^{t}$
- $e^{2} e^{t} \cos{\left(t + 2 \right)}$
- $\left(- \sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)}\right) e^{2} e^{t}$
- $2 e^{2} e^{t} \cos{\left(t + 2 \right)}$
- $2 \left(\sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)}\right) e^{2} e^{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(z \left(x + y\right))\,i+\frac{∂}{∂y}(z \left(x + y\right))\,j+\frac{∂}{∂z}(z \left(x + y\right))\,k \\  & =(z)\,i+(z)\,j+(x + y)\,k\end{aligned}
$$

Next, we substitute $x=\sin{\left(t + 2 \right)},y=\cos{\left(t + 2 \right)},$ and $z=e^{t + 2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(e^{t + 2})\,i+(e^{t + 2})\,j+(\sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sin{\left(t + 2 \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t + 2 \right)})\,j+\frac{\text{d}}{\text{d}t}(e^{t + 2})\,k \\  & =(\cos{\left(t + 2 \right)})\,i+(- \sin{\left(t + 2 \right)})\,j+(e^{t + 2})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{t + 2})\,i+(e^{t + 2})\,j+(\sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)})\,k)\cdot ((\cos{\left(t + 2 \right)})\,i+(- \sin{\left(t + 2 \right)})\,j+(e^{t + 2})\,k) \\  & =(e^{t + 2})\cdot (\cos{\left(t + 2 \right)})+(e^{t + 2})\cdot (- \sin{\left(t + 2 \right)})+(\sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)})\cdot (e^{t + 2}) \\  & =(e^{t + 2} \cos{\left(t + 2 \right)})+(- e^{t + 2} \sin{\left(t + 2 \right)})+(\left(\sin{\left(t + 2 \right)} + \cos{\left(t + 2 \right)}\right) e^{t + 2}) \\  & =2 e^{2} e^{t} \cos{\left(t + 2 \right)}.\end{aligned}
$$

## Generated default moderate constant_coordinate 19

If $f(x,y,z)=3\left(x{y}^{2}+y{z}^{3}\right)$ and $r(t)={(t - 2)}^{3}\,i+\,j+(t - 2)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $9 \left(t^{2} - 4 t + 4\right)$
- $21 \left(t^{3} - 6 t^{2} + 12 t - 8\right)$
- $12 \left(t^{2} - 4 t + 4\right)$
- $18 \left(t^{2} - 4 t + 4\right)$
- $3 \left(3 t^{3} - 15 t^{2} + 24 t - 11\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3\left(x{y}^{2}+y{z}^{3}\right))\,i+\frac{∂}{∂y}(3\left(x{y}^{2}+y{z}^{3}\right))\,j+\frac{∂}{∂z}(3\left(x{y}^{2}+y{z}^{3}\right))\,k \\  & =(3\left({y}^{2}\right))\,i+(3\left(+(2xy+{z}^{3})\right))\,j+(3\left(+3y{z}^{2}\right))\,k\end{aligned}
$$

Next, we substitute $x={(t - 2)}^{3},y=1,$ and $z=(t - 2)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left(1\right))\,i+(3\left(+3{(t - 2)}^{3}\right))\,j+(3\left(+3{(t - 2)}^{2}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t - 2)}^{3})\,i+\frac{\text{d}}{\text{d}t}(1)\,j+\frac{\text{d}}{\text{d}t}((t - 2))\,k \\  & =(3{(t - 2)}^{2})\,i+(+(0))\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(1\right))\,i+(3\left(+3{(t - 2)}^{3}\right))\,j+(3\left(+3{(t - 2)}^{2}\right))\,k)\cdot ((3{(t - 2)}^{2})\,i+(+(0))\,j+(1)\,k) \\  & =3\left(1\cdot 3{(t - 2)}^{2}+3{(t - 2)}^{3}\cdot 0+3{(t - 2)}^{2}\cdot 1\right) \\  & =3\left(3{(t - 2)}^{2}+3{(t - 2)}^{2}\right) \\  & =3\left(6{(t - 2)}^{2}\right).\end{aligned}
$$

## Generated default moderate constant_coordinate 44

If $f(x,y,z)=x{y}^{2}+y{z}^{3}$ and $r(t)={(t + 2)}^{3}\,i+\,j+(t + 2)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $4 \left(t^{2} + 4 t + 4\right)$
- $3 \left(t^{2} + 4 t + 4\right)$
- $7 \left(t^{3} + 6 t^{2} + 12 t + 8\right)$
- $6 \left(t^{2} + 4 t + 4\right)$
- $3 t^{3} + 21 t^{2} + 48 t + 37$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(x{y}^{2}+y{z}^{3})\,i+\frac{∂}{∂y}(x{y}^{2}+y{z}^{3})\,j+\frac{∂}{∂z}(x{y}^{2}+y{z}^{3})\,k \\  & ={y}^{2}\,i+(2xy+{z}^{3})\,j+3y{z}^{2}\,k\end{aligned}
$$

Next, we substitute $x={(t + 2)}^{3},y=1,$ and $z=(t + 2)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(1)\,i+(+3{(t + 2)}^{3})\,j+(+3{(t + 2)}^{2})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t + 2)}^{3})\,i+\frac{\text{d}}{\text{d}t}(1)\,j+\frac{\text{d}}{\text{d}t}((t + 2))\,k \\  & =(3{(t + 2)}^{2})\,i+(+(0))\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((1)\,i+(+3{(t + 2)}^{3})\,j+(+3{(t + 2)}^{2})\,k)\cdot ((3{(t + 2)}^{2})\,i+(+(0))\,j+(1)\,k) \\  & =1\cdot 3{(t + 2)}^{2}+3{(t + 2)}^{3}\cdot 0+3{(t + 2)}^{2}\cdot 1 \\  & =3{(t + 2)}^{2}+3{(t + 2)}^{2} \\  & =6{(t + 2)}^{2}.\end{aligned}
$$

## Generated default moderate quartic_trig 19

If $f(x,y,z)=3\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right)$ and $r(t)=\operatorname{sin}⁡(t - 2)\,i+\operatorname{cos}⁡(t - 2)\,j+2(t - 2)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $6 \left(2 \sin{\left(t - 2 \right)} \cos^{3}{\left(t - 2 \right)} + \sin{\left(2 \left(t - 2\right) \right)}\right)$
- $12 \left(\sin^{2}{\left(t - 2 \right)} + \cos^{2}{\left(t - 2 \right)}\right) \sin{\left(t - 2 \right)} \cos{\left(t - 2 \right)}$
- $6 \left(2 \sin^{3}{\left(t - 2 \right)} \cos{\left(t - 2 \right)} + \sin{\left(2 \left(t - 2\right) \right)}\right)$
- $12 \sin{\left(2 t - 4 \right)}$
- $6 \left(t \sin{\left(2 \left(t - 2\right) \right)} + 2 \sin^{4}{\left(t - 2 \right)} - 2 \sin{\left(2 \left(t - 2\right) \right)} - 2 \cos^{4}{\left(t - 2 \right)}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,i+\frac{∂}{∂y}(3\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,j+\frac{∂}{∂z}(3\left({x}^{4}-{y}^{4}-\operatorname{cos}⁡z\right))\,k \\  & =(3\left(4{x}^{3}\right))\,i+(3\left(-4{y}^{3}\right))\,j+(3\left(+\operatorname{sin}⁡z\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t - 2),$ $y=\operatorname{cos}⁡(t - 2)$ and $z=2(t - 2)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left(4{sin}^{3}⁡(t - 2)\right))\,i+(3\left(-4{cos}^{3}⁡(t - 2)\right))\,j+(3\left(+\operatorname{sin}⁡2(t - 2)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t - 2))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t - 2))\,j+\frac{\text{d}}{\text{d}t}(2(t - 2))\,k \\  & =(\operatorname{cos}⁡(t - 2))\,i+(-\operatorname{sin}⁡(t - 2))\,j+(+2)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(4{sin}^{3}⁡(t - 2)\right))\,i+(3\left(-4{cos}^{3}⁡(t - 2)\right))\,j+(3\left(+\operatorname{sin}⁡2(t - 2)\right))\,k)\cdot ((\operatorname{cos}⁡(t - 2))\,i+(-\operatorname{sin}⁡(t - 2))\,j+(+2)\,k) \\  & =3\left(4{sin}^{3}⁡(t - 2)\cdot \operatorname{cos}⁡(t - 2)-4{cos}^{3}⁡(t - 2)\cdot (-\operatorname{sin}⁡(t - 2))+\operatorname{sin}⁡2(t - 2)\cdot 2\right) \\  & =3\left(4{sin}^{3}⁡(t - 2)\operatorname{cos}⁡(t - 2)+4{cos}^{3}⁡(t - 2)\operatorname{sin}⁡(t - 2)+2\operatorname{sin}⁡2(t - 2)\right) \\  & =3\left(4\operatorname{sin}⁡(t - 2)\operatorname{cos}⁡(t - 2)({sin}^{2}⁡(t - 2)+{cos}^{2}⁡(t - 2))+2\operatorname{sin}⁡2(t - 2)\right) \\  & =3\left(4\operatorname{sin}⁡(t - 2)\operatorname{cos}⁡(t - 2)+2\operatorname{sin}⁡2(t - 2)\right) \\  & =3\left(2\operatorname{sin}⁡2(t - 2)+2\operatorname{sin}⁡2(t - 2)\right) \\  & =3\left(4\operatorname{sin}⁡2(t - 2)\right).\end{aligned}
$$

## Generated default moderate quartic_trig 44

If $f(x,y,z)={x}^{4}-{y}^{4}-\operatorname{cos}⁡z$ and $r(t)=\operatorname{sin}⁡(t + 2)\,i+\operatorname{cos}⁡(t + 2)\,j+2(t + 2)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2 \left(2 \sin^{3}{\left(t + 2 \right)} \cos{\left(t + 2 \right)} + \sin{\left(2 \left(t + 2\right) \right)}\right)$
- $2 \left(2 \sin{\left(t + 2 \right)} \cos^{3}{\left(t + 2 \right)} + \sin{\left(2 \left(t + 2\right) \right)}\right)$
- $4 \left(\sin^{2}{\left(t + 2 \right)} + \cos^{2}{\left(t + 2 \right)}\right) \sin{\left(t + 2 \right)} \cos{\left(t + 2 \right)}$
- $4 \sin{\left(2 t + 4 \right)}$
- $2 \left(t \sin{\left(2 \left(t + 2\right) \right)} + 2 \sin^{4}{\left(t + 2 \right)} + 2 \sin{\left(2 \left(t + 2\right) \right)} - 2 \cos^{4}{\left(t + 2 \right)}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,i+\frac{∂}{∂y}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,j+\frac{∂}{∂z}({x}^{4}-{y}^{4}-\operatorname{cos}⁡z)\,k \\  & =4{x}^{3}\,i-4{y}^{3}\,j+\operatorname{sin}⁡z\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t + 2),$ $y=\operatorname{cos}⁡(t + 2)$ and $z=2(t + 2)$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(4{sin}^{3}⁡(t + 2))\,i+(-4{cos}^{3}⁡(t + 2))\,j+(+\operatorname{sin}⁡2(t + 2))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t + 2))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t + 2))\,j+\frac{\text{d}}{\text{d}t}(2(t + 2))\,k \\  & =(\operatorname{cos}⁡(t + 2))\,i+(-\operatorname{sin}⁡(t + 2))\,j+(+2)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((4{sin}^{3}⁡(t + 2))\,i+(-4{cos}^{3}⁡(t + 2))\,j+(+\operatorname{sin}⁡2(t + 2))\,k)\cdot ((\operatorname{cos}⁡(t + 2))\,i+(-\operatorname{sin}⁡(t + 2))\,j+(+2)\,k) \\  & =4{sin}^{3}⁡(t + 2)\cdot \operatorname{cos}⁡(t + 2)-4{cos}^{3}⁡(t + 2)\cdot (-\operatorname{sin}⁡(t + 2))+\operatorname{sin}⁡2(t + 2)\cdot 2 \\  & =4{sin}^{3}⁡(t + 2)\operatorname{cos}⁡(t + 2)+4{cos}^{3}⁡(t + 2)\operatorname{sin}⁡(t + 2)+2\operatorname{sin}⁡2(t + 2) \\  & =4\operatorname{sin}⁡(t + 2)\operatorname{cos}⁡(t + 2)({sin}^{2}⁡(t + 2)+{cos}^{2}⁡(t + 2))+2\operatorname{sin}⁡2(t + 2) \\  & =4\operatorname{sin}⁡(t + 2)\operatorname{cos}⁡(t + 2)+2\operatorname{sin}⁡2(t + 2) \\  & =2\operatorname{sin}⁡2(t + 2)+2\operatorname{sin}⁡2(t + 2) \\  & =4\operatorname{sin}⁡2(t + 2).\end{aligned}
$$

## Generated default moderate log_product 19

If $f(x,y,z)=3\left(\operatorname{ln}⁡(xyz)\right)$ and $r(t)=(t - 2)\,i+{e}^{(t - 2)-1}\,j+{e}^{(t - 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $3 \left(1 + \frac{1}{t - 2}\right)$
- $3 \left(2 - \frac{1}{t - 2}\right)$
- $\frac{3}{t - 2}$
- $3 \left(2 + \frac{1}{t - 2}\right)$
- $9$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3\left(\operatorname{ln}⁡(xyz)\right))\,i+\frac{∂}{∂y}(3\left(\operatorname{ln}⁡(xyz)\right))\,j+\frac{∂}{∂z}(3\left(\operatorname{ln}⁡(xyz)\right))\,k \\  & =(3\left(\frac{yz}{xyz}\right))\,i+(3\left(+\frac{xz}{xyz}\right))\,j+(3\left(+\frac{xy}{xyz}\right))\,k \\  & =(3\left(\frac{1}{x}\right))\,i+(3\left(+\frac{1}{y}\right))\,j+(3\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=(t - 2),y={e}^{(t - 2)-1},$ and $z={e}^{(t - 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left(\frac{1}{(t - 2)}\right))\,i+(3\left(+\frac{1}{{e}^{(t - 2)-1}}\right))\,j+(3\left(+\frac{1}{{e}^{(t - 2)}}\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}((t - 2))\,i+\frac{\text{d}}{\text{d}t}({e}^{(t - 2)-1})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t - 2)})\,k \\  & =(1)\,i+(+{e}^{(t - 2)-1})\,j+(+{e}^{(t - 2)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(\frac{1}{(t - 2)}\right))\,i+(3\left(+\frac{1}{{e}^{(t - 2)-1}}\right))\,j+(3\left(+\frac{1}{{e}^{(t - 2)}}\right))\,k)\cdot ((1)\,i+(+{e}^{(t - 2)-1})\,j+(+{e}^{(t - 2)})\,k) \\  & =3\left(\frac{1}{(t - 2)}+\frac{{e}^{(t - 2)-1}}{{e}^{(t - 2)-1}}+\frac{{e}^{(t - 2)}}{{e}^{(t - 2)}}\right) \\  & =3\left(\frac{1}{(t - 2)}+2\right) \\  & =3\left(\frac{2(t - 2)+1}{(t - 2)}\right).\end{aligned}
$$

## Generated default moderate log_product 44

If $f(x,y,z)=\operatorname{ln}⁡(xyz)$ and $r(t)=(t + 2)\,i+{e}^{(t + 2)-1}\,j+{e}^{(t + 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{1}{t + 2}$
- $1 + \frac{1}{t + 2}$
- $2 - \frac{1}{t + 2}$
- $2 + \frac{1}{t + 2}$
- $3$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xyz))\,i+\frac{∂}{∂y}(\operatorname{ln}⁡(xyz))\,j+\frac{∂}{∂z}(\operatorname{ln}⁡(xyz))\,k \\  & =\frac{yz}{xyz}\,i+\frac{xz}{xyz}\,j+\frac{xy}{xyz}\,k \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j+\frac{1}{z}\,k\end{aligned}
$$

Next, we substitute $x=(t + 2),y={e}^{(t + 2)-1},$ and $z={e}^{(t + 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(\frac{1}{(t + 2)})\,i+(+\frac{1}{{e}^{(t + 2)-1}})\,j+(+\frac{1}{{e}^{(t + 2)}})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}((t + 2))\,i+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)-1})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)})\,k \\  & =(1)\,i+(+{e}^{(t + 2)-1})\,j+(+{e}^{(t + 2)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((\frac{1}{(t + 2)})\,i+(+\frac{1}{{e}^{(t + 2)-1}})\,j+(+\frac{1}{{e}^{(t + 2)}})\,k)\cdot ((1)\,i+(+{e}^{(t + 2)-1})\,j+(+{e}^{(t + 2)})\,k) \\  & =\frac{1}{(t + 2)}+\frac{{e}^{(t + 2)-1}}{{e}^{(t + 2)-1}}+\frac{{e}^{(t + 2)}}{{e}^{(t + 2)}} \\  & =\frac{1}{(t + 2)}+2 \\  & =\frac{2(t + 2)+1}{(t + 2)}.\end{aligned}
$$

## Generated default moderate log_difference 19

If $f(x,y,z)=3\left(x({y}^{2}-{z}^{2})\right)$ and $r(t)=\operatorname{ln}⁡(t - 2)\,i+((t - 2)+1)\,j+((t - 2)-1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $12 \ln{\left(t - 2 \right)}$
- $6 \left(t \ln{\left(t - 2 \right)} + \frac{2 t}{t - 2} - \ln{\left(t - 2 \right)} - \frac{4}{t - 2}\right)$
- $6 \left(- t \ln{\left(t - 2 \right)} + \frac{2 t}{t - 2} + 3 \ln{\left(t - 2 \right)} - \frac{4}{t - 2}\right)$
- $12 \left(\frac{t}{t - 2} + \ln{\left(t - 2 \right)} - \frac{2}{t - 2}\right)$
- $36 \left(t - 2\right) \ln{\left(t - 2 \right)}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}[3\left(x({y}^{2}-{z}^{2})\right)]\,i+\frac{∂}{∂y}[3\left(x({y}^{2}-{z}^{2})\right)]\,j+\frac{∂}{∂z}[3\left(x({y}^{2}-{z}^{2})\right)]\,k \\  & =(3\left(({y}^{2}-{z}^{2})\right))\,i+(3\left(+2xy\right))\,j+(3\left(-2xz\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡(t - 2),$ $y=(t - 2)+1$ and $z=(t - 2)-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left([((t - 2)+1)^{2}-((t - 2)-1)^{2}]\right))\,i+(3\left(+2\operatorname{ln}⁡(t - 2)\cdot ((t - 2)+1)\right))\,j+(3\left(-2\operatorname{ln}⁡(t - 2)\cdot ((t - 2)-1)\right))\,k \\  & =(3\left(4(t - 2)\right))\,i+(3\left(+2((t - 2)+1)\operatorname{ln}⁡(t - 2)\right))\,j+(3\left(-2((t - 2)-1)\operatorname{ln}⁡(t - 2)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t - 2))\,i+\frac{\text{d}}{\text{d}t}((t - 2)+1)\,j+\frac{\text{d}}{\text{d}t}((t - 2)-1)\,k \\  & =(\frac{1}{(t - 2)})\,i+(1)\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(4(t - 2)\right))\,i+(3\left(+2((t - 2)+1)\operatorname{ln}⁡(t - 2)\right))\,j+(3\left(-2((t - 2)-1)\operatorname{ln}⁡(t - 2)\right))\,k)\cdot ((\frac{1}{(t - 2)})\,i+(1)\,j+(1)\,k) \\  & =3\left(4(t - 2)\cdot \frac{1}{(t - 2)}+2((t - 2)+1)\operatorname{ln}⁡(t - 2)\cdot 1-2((t - 2)-1)\operatorname{ln}⁡(t - 2)\cdot 1\right) \\  & =3\left(4+2((t - 2)+1)\operatorname{ln}⁡(t - 2)-2((t - 2)-1)\operatorname{ln}⁡(t - 2)\right) \\  & =3\left(4+4\operatorname{ln}⁡(t - 2)\right) \\  & =3\left(4(\operatorname{ln}⁡(t - 2)+1)\right).\end{aligned}
$$

## Generated default moderate log_difference 44

If $f(x,y,z)=x({y}^{2}-{z}^{2})$ and $r(t)=\operatorname{ln}⁡(t + 2)\,i+((t + 2)+1)\,j+((t + 2)-1)\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2 \left(- t \ln{\left(t + 2 \right)} + \frac{2 t}{t + 2} - \ln{\left(t + 2 \right)} + \frac{4}{t + 2}\right)$
- $4 \ln{\left(t + 2 \right)}$
- $2 \left(t \ln{\left(t + 2 \right)} + \frac{2 t}{t + 2} + 3 \ln{\left(t + 2 \right)} + \frac{4}{t + 2}\right)$
- $4 \left(\frac{t}{t + 2} + \ln{\left(t + 2 \right)} + \frac{2}{t + 2}\right)$
- $12 \left(t + 2\right) \ln{\left(t + 2 \right)}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}[x({y}^{2}-{z}^{2})]\,i+\frac{∂}{∂y}[x({y}^{2}-{z}^{2})]\,j+\frac{∂}{∂z}[x({y}^{2}-{z}^{2})]\,k \\  & =({y}^{2}-{z}^{2})\,i+2xy\,j-2xz\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡(t + 2),$ $y=(t + 2)+1$ and $z=(t + 2)-1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =([((t + 2)+1)^{2}-((t + 2)-1)^{2}])\,i+(+2\operatorname{ln}⁡(t + 2)\cdot ((t + 2)+1))\,j+(-2\operatorname{ln}⁡(t + 2)\cdot ((t + 2)-1))\,k \\  & =(4(t + 2))\,i+(+2((t + 2)+1)\operatorname{ln}⁡(t + 2))\,j+(-2((t + 2)-1)\operatorname{ln}⁡(t + 2))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t + 2))\,i+\frac{\text{d}}{\text{d}t}((t + 2)+1)\,j+\frac{\text{d}}{\text{d}t}((t + 2)-1)\,k \\  & =(\frac{1}{(t + 2)})\,i+(1)\,j+(1)\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((4(t + 2))\,i+(+2((t + 2)+1)\operatorname{ln}⁡(t + 2))\,j+(-2((t + 2)-1)\operatorname{ln}⁡(t + 2))\,k)\cdot ((\frac{1}{(t + 2)})\,i+(1)\,j+(1)\,k) \\  & =4(t + 2)\cdot \frac{1}{(t + 2)}+2((t + 2)+1)\operatorname{ln}⁡(t + 2)\cdot 1-2((t + 2)-1)\operatorname{ln}⁡(t + 2)\cdot 1 \\  & =4+2((t + 2)+1)\operatorname{ln}⁡(t + 2)-2((t + 2)-1)\operatorname{ln}⁡(t + 2) \\  & =4+4\operatorname{ln}⁡(t + 2) \\  & =4(\operatorname{ln}⁡(t + 2)+1).\end{aligned}
$$

## Generated default moderate log_exp 19

If $f(x,y,z)=3\left(\operatorname{ln}⁡(xz)+{e}^{y}\right)$ and $r(t)=\operatorname{sin}⁡(t - 2)\,i+{(t - 2)}^{2}\,j+\frac{1}{(t - 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $3 \left(2 t e^{4} e^{- 4 t} e^{t^{2}} - \frac{t}{t^{2} - 4 t + 4} - 4 e^{4} e^{- 4 t} e^{t^{2}} + \frac{2}{t^{2} - 4 t + 4}\right)$
- $3 \left(2 t e^{4} e^{- 4 t} e^{t^{2}} + \frac{\cos{\left(t - 2 \right)}}{\sin{\left(t - 2 \right)}} - 4 e^{4} e^{- 4 t} e^{t^{2}}\right)$
- $3 \left(- \frac{t}{t^{2} - 4 t + 4} + \frac{\cos{\left(t - 2 \right)}}{\sin{\left(t - 2 \right)}} + \frac{2}{t^{2} - 4 t + 4}\right)$
- $3 \left(2 t e^{4} e^{- 4 t} e^{t^{2}} - \frac{t}{t^{2} - 4 t + 4} + \frac{\cos{\left(t - 2 \right)}}{\sin{\left(t - 2 \right)}} - 4 e^{4} e^{- 4 t} e^{t^{2}} + \frac{2}{t^{2} - 4 t + 4}\right)$
- $3 \left(t^{2} e^{4} e^{- 4 t} e^{t^{2}} - 4 t e^{4} e^{- 4 t} e^{t^{2}} + \frac{t}{t - 2} + 1 + 4 e^{4} e^{- 4 t} e^{t^{2}} - \frac{2}{t - 2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,i+\frac{∂}{∂y}(3\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,j+\frac{∂}{∂z}(3\left(\operatorname{ln}⁡(xz)+{e}^{y}\right))\,k \\  & =(3\left(\frac{1}{x}\right))\,i+(3\left(+{e}^{y}\right))\,j+(3\left(+\frac{1}{z}\right))\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t - 2),y={(t - 2)}^{2},$ and $z=\frac{1}{(t - 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left(\frac{1}{\operatorname{sin}⁡(t - 2)}\right))\,i+(3\left(+{e}^{{(t - 2)}^{2}}\right))\,j+(3\left(+(t - 2)\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t - 2))\,i+\frac{\text{d}}{\text{d}t}({(t - 2)}^{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{1}{(t - 2)})k \\  & =(\operatorname{cos}⁡(t - 2))\,i+(+2(t - 2))\,j+(-\frac{1}{{(t - 2)}^{2}})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(\frac{1}{\operatorname{sin}⁡(t - 2)}\right))\,i+(3\left(+{e}^{{(t - 2)}^{2}}\right))\,j+(3\left(+(t - 2)\right))\,k)\cdot ((\operatorname{cos}⁡(t - 2))\,i+(+2(t - 2))\,j+(-\frac{1}{{(t - 2)}^{2}})\,k) \\  & =3\left(\frac{\operatorname{cos}⁡(t - 2)}{\operatorname{sin}⁡(t - 2)}+2(t - 2){e}^{{(t - 2)}^{2}}-\frac{(t - 2)}{{(t - 2)}^{2}}\right) \\  & =3\left(\operatorname{cot}⁡(t - 2)+2(t - 2){e}^{{(t - 2)}^{2}}-\frac{1}{(t - 2)}\right).\end{aligned}
$$

## Generated default moderate log_exp 44

If $f(x,y,z)=\operatorname{ln}⁡(xz)+{e}^{y}$ and $r(t)=\operatorname{sin}⁡(t + 2)\,i+{(t + 2)}^{2}\,j+\frac{1}{(t + 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{\cos{\left(t + 2 \right)}}{\sin{\left(t + 2 \right)}} - \frac{1}{t + 2}$
- $2 t e^{4} e^{4 t} e^{t^{2}} + 4 e^{4} e^{4 t} e^{t^{2}} - \frac{1}{t + 2}$
- $2 t e^{4} e^{4 t} e^{t^{2}} + 4 e^{4} e^{4 t} e^{t^{2}} + \frac{\cos{\left(t + 2 \right)}}{\sin{\left(t + 2 \right)}}$
- $2 t e^{4} e^{4 t} e^{t^{2}} + 4 e^{4} e^{4 t} e^{t^{2}} + \frac{\cos{\left(t + 2 \right)}}{\sin{\left(t + 2 \right)}} - \frac{1}{t + 2}$
- $t^{2} e^{4} e^{4 t} e^{t^{2}} + 4 t e^{4} e^{4 t} e^{t^{2}} + 4 e^{4} e^{4 t} e^{t^{2}} + 2$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xz)+{e}^{y})\,i+\frac{∂}{∂y}(\operatorname{ln}⁡(xz)+{e}^{y})\,j+\frac{∂}{∂z}(\operatorname{ln}⁡(xz)+{e}^{y})\,k \\  & =\frac{1}{x}\,i+{e}^{y}\,j+\frac{1}{z}\,k\end{aligned}
$$

Next, we substitute $x=\operatorname{sin}⁡(t + 2),y={(t + 2)}^{2},$ and $z=\frac{1}{(t + 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(\frac{1}{\operatorname{sin}⁡(t + 2)})\,i+(+{e}^{{(t + 2)}^{2}})\,j+(+(t + 2))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t + 2))\,i+\frac{\text{d}}{\text{d}t}({(t + 2)}^{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{1}{(t + 2)})k \\  & =(\operatorname{cos}⁡(t + 2))\,i+(+2(t + 2))\,j+(-\frac{1}{{(t + 2)}^{2}})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((\frac{1}{\operatorname{sin}⁡(t + 2)})\,i+(+{e}^{{(t + 2)}^{2}})\,j+(+(t + 2))\,k)\cdot ((\operatorname{cos}⁡(t + 2))\,i+(+2(t + 2))\,j+(-\frac{1}{{(t + 2)}^{2}})\,k) \\  & =\frac{\operatorname{cos}⁡(t + 2)}{\operatorname{sin}⁡(t + 2)}+2(t + 2){e}^{{(t + 2)}^{2}}-\frac{(t + 2)}{{(t + 2)}^{2}} \\  & =\operatorname{cot}⁡(t + 2)+2(t + 2){e}^{{(t + 2)}^{2}}-\frac{1}{(t + 2)}.\end{aligned}
$$

## Generated default hard exponential_cosine 19

If $f(x,y,z)=-4\left(yz\operatorname{cos}⁡x\right)$ and $r(t)={(t + 2)}^{2}\,i+{e}^{(t + 2)}\,j+{e}^{(t + 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $4 \left(e^{2} e^{t} \sin{\left(t^{2} + 4 t + 4 \right)} - 2 \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{2} e^{t}$
- $8 \left(t + 2\right) e^{4} e^{2 t} \sin{\left(t^{2} + 4 t + 4 \right)}$
- $4 \left(\sin{\left(t^{2} + 4 t + 4 \right)} - 2 \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{4} e^{2 t}$
- $- 8 e^{4} e^{2 t} \cos{\left(t^{2} + 4 t + 4 \right)}$
- $8 \left(t \sin{\left(t^{2} + 4 t + 4 \right)} + 2 \sin{\left(t^{2} + 4 t + 4 \right)} - \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{4} e^{2 t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(-4\left(yz\operatorname{cos}⁡x\right))\,i+\frac{∂}{∂y}(-4\left(yz\operatorname{cos}⁡x\right))\,j+\frac{∂}{∂z}(-4\left(yz\operatorname{cos}⁡x\right))\,k \\  & =(-4\left(-yz\operatorname{sin}⁡x\right))\,i+(-4\left(+z\operatorname{cos}⁡x\right))\,j+(-4\left(+y\operatorname{cos}⁡x\right))\,k\end{aligned}
$$

Next, we substitute $x={(t + 2)}^{2},y={e}^{(t + 2)},$ and $z={e}^{(t + 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(-4\left(-{e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})\right))\,i+(-4\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,j+(-4\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t + 2)}^{2})\,i+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)})\,k \\  & =(2(t + 2))\,i+(+{e}^{(t + 2)})\,j+(+{e}^{(t + 2)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((-4\left(-{e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})\right))\,i+(-4\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,j+(-4\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,k)\cdot ((2(t + 2))\,i+(+{e}^{(t + 2)})\,j+(+{e}^{(t + 2)})\,k) \\  & =-4\left(-2(t + 2){e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\cdot {e}^{(t + 2)}+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\cdot {e}^{(t + 2)}\right) \\  & =-4\left(-2(t + 2){e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})+2{e}^{2(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right) \\  & =-4\left(2{e}^{2(t + 2)}(\operatorname{cos}⁡({(t + 2)}^{2})-(t + 2)\operatorname{sin}⁡({(t + 2)}^{2}))\right).\end{aligned}
$$

## Generated default hard exponential_cosine 44

If $f(x,y,z)=3\left(yz\operatorname{cos}⁡x\right)$ and $r(t)={(t + 2)}^{2}\,i+{e}^{(t + 2)}\,j+{e}^{(t + 2)}\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- 6 \left(t + 2\right) e^{4} e^{2 t} \sin{\left(t^{2} + 4 t + 4 \right)}$
- $6 e^{4} e^{2 t} \cos{\left(t^{2} + 4 t + 4 \right)}$
- $3 \left(- \sin{\left(t^{2} + 4 t + 4 \right)} + 2 \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{4} e^{2 t}$
- $6 \left(- t \sin{\left(t^{2} + 4 t + 4 \right)} - 2 \sin{\left(t^{2} + 4 t + 4 \right)} + \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{4} e^{2 t}$
- $3 \left(- e^{2} e^{t} \sin{\left(t^{2} + 4 t + 4 \right)} + 2 \cos{\left(t^{2} + 4 t + 4 \right)}\right) e^{2} e^{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3\left(yz\operatorname{cos}⁡x\right))\,i+\frac{∂}{∂y}(3\left(yz\operatorname{cos}⁡x\right))\,j+\frac{∂}{∂z}(3\left(yz\operatorname{cos}⁡x\right))\,k \\  & =(3\left(-yz\operatorname{sin}⁡x\right))\,i+(3\left(+z\operatorname{cos}⁡x\right))\,j+(3\left(+y\operatorname{cos}⁡x\right))\,k\end{aligned}
$$

Next, we substitute $x={(t + 2)}^{2},y={e}^{(t + 2)},$ and $z={e}^{(t + 2)}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3\left(-{e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})\right))\,i+(3\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,j+(3\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({(t + 2)}^{2})\,i+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)})\,j+\frac{\text{d}}{\text{d}t}({e}^{(t + 2)})\,k \\  & =(2(t + 2))\,i+(+{e}^{(t + 2)})\,j+(+{e}^{(t + 2)})\,k.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3\left(-{e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})\right))\,i+(3\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,j+(3\left(+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right))\,k)\cdot ((2(t + 2))\,i+(+{e}^{(t + 2)})\,j+(+{e}^{(t + 2)})\,k) \\  & =3\left(-2(t + 2){e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\cdot {e}^{(t + 2)}+{e}^{(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\cdot {e}^{(t + 2)}\right) \\  & =3\left(-2(t + 2){e}^{2(t + 2)}\operatorname{sin}⁡({(t + 2)}^{2})+2{e}^{2(t + 2)}\operatorname{cos}⁡({(t + 2)}^{2})\right) \\  & =3\left(2{e}^{2(t + 2)}(\operatorname{cos}⁡({(t + 2)}^{2})-(t + 2)\operatorname{sin}⁡({(t + 2)}^{2}))\right).\end{aligned}
$$

## Generated default hard canonical_log 19

If $f(x,y,z)=- 4 x z \ln{\left(y \right)}$ and $r(t)=(\left(t + 2\right)^{2})\,i+(t + 2)\,j+(\left(t + 2\right)^{3})\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- 4 \left(2 t^{5} \ln{\left(t + 2 \right)} + t^{5} + 20 t^{4} \ln{\left(t + 2 \right)} + 10 t^{4} + 80 t^{3} \ln{\left(t + 2 \right)} + 40 t^{3} + 160 t^{2} \ln{\left(t + 2 \right)} + 80 t^{2} + 160 t \ln{\left(t + 2 \right)} + 80 t + 64 \ln{\left(t + 2 \right)} + 32\right)$
- $- 20 \left(t^{4} + 8 t^{3} + 24 t^{2} + 32 t + 16\right) \ln{\left(t + 2 \right)}$
- $- 4 \left(2 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 16 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 48 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 64 t \ln{\left(t + 2 \right)} + 32 t + 32 \ln{\left(t + 2 \right)} + 16\right)$
- $- 4 \left(3 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 24 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 72 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 96 t \ln{\left(t + 2 \right)} + 32 t + 48 \ln{\left(t + 2 \right)} + 16\right)$
- $- 4 \left(5 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 40 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 120 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 160 t \ln{\left(t + 2 \right)} + 32 t + 80 \ln{\left(t + 2 \right)} + 16\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(- 4 x z \ln{\left(y \right)})\,i+\frac{∂}{∂y}(- 4 x z \ln{\left(y \right)})\,j+\frac{∂}{∂z}(- 4 x z \ln{\left(y \right)})\,k \\  & =(- 4 z \ln{\left(y \right)})\,i+(- \frac{4 x z}{y})\,j+(- 4 x \ln{\left(y \right)})\,k\end{aligned}
$$

Next, we substitute $x=\left(t + 2\right)^{2},y=t + 2,$ and $z=\left(t + 2\right)^{3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(- 4 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\,i+(- 4 \left(t + 2\right)^{4})\,j+(- 4 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\left(t + 2\right)^{2})\,i+\frac{\text{d}}{\text{d}t}(t + 2)\,j+\frac{\text{d}}{\text{d}t}(\left(t + 2\right)^{3})\,k \\  & =(2 t + 4)\,i+(1)\,j+(3 \left(t + 2\right)^{2})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((- 4 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\,i+(- 4 \left(t + 2\right)^{4})\,j+(- 4 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\,k)\cdot ((2 t + 4)\,i+(1)\,j+(3 \left(t + 2\right)^{2})\,k) \\  & =(- 4 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\cdot (2 t + 4)+(- 4 \left(t + 2\right)^{4})\cdot (1)+(- 4 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\cdot (3 \left(t + 2\right)^{2}) \\  & =(- 4 \left(t + 2\right)^{3} \left(2 t + 4\right) \ln{\left(t + 2 \right)})+(- 4 \left(t + 2\right)^{4})+(- 12 \left(t + 2\right)^{4} \ln{\left(t + 2 \right)}) \\  & =- 4 \left(5 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 40 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 120 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 160 t \ln{\left(t + 2 \right)} + 32 t + 80 \ln{\left(t + 2 \right)} + 16\right).\end{aligned}
$$

## Generated default hard canonical_log 44

If $f(x,y,z)=3 x z \ln{\left(y \right)}$ and $r(t)=(\left(t + 2\right)^{2})\,i+(t + 2)\,j+(\left(t + 2\right)^{3})\,k,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $15 \left(t^{4} + 8 t^{3} + 24 t^{2} + 32 t + 16\right) \ln{\left(t + 2 \right)}$
- $3 \left(3 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 24 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 72 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 96 t \ln{\left(t + 2 \right)} + 32 t + 48 \ln{\left(t + 2 \right)} + 16\right)$
- $3 \left(2 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 16 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 48 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 64 t \ln{\left(t + 2 \right)} + 32 t + 32 \ln{\left(t + 2 \right)} + 16\right)$
- $3 \left(5 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 40 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 120 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 160 t \ln{\left(t + 2 \right)} + 32 t + 80 \ln{\left(t + 2 \right)} + 16\right)$
- $3 \left(2 t^{5} \ln{\left(t + 2 \right)} + t^{5} + 20 t^{4} \ln{\left(t + 2 \right)} + 10 t^{4} + 80 t^{3} \ln{\left(t + 2 \right)} + 40 t^{3} + 160 t^{2} \ln{\left(t + 2 \right)} + 80 t^{2} + 160 t \ln{\left(t + 2 \right)} + 80 t + 64 \ln{\left(t + 2 \right)} + 32\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(3 x z \ln{\left(y \right)})\,i+\frac{∂}{∂y}(3 x z \ln{\left(y \right)})\,j+\frac{∂}{∂z}(3 x z \ln{\left(y \right)})\,k \\  & =(3 z \ln{\left(y \right)})\,i+(\frac{3 x z}{y})\,j+(3 x \ln{\left(y \right)})\,k\end{aligned}
$$

Next, we substitute $x=\left(t + 2\right)^{2},y=t + 2,$ and $z=\left(t + 2\right)^{3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(3 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\,i+(3 \left(t + 2\right)^{4})\,j+(3 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\,k\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\left(t + 2\right)^{2})\,i+\frac{\text{d}}{\text{d}t}(t + 2)\,j+\frac{\text{d}}{\text{d}t}(\left(t + 2\right)^{3})\,k \\  & =(2 t + 4)\,i+(1)\,j+(3 \left(t + 2\right)^{2})\,k\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((3 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\,i+(3 \left(t + 2\right)^{4})\,j+(3 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\,k)\cdot ((2 t + 4)\,i+(1)\,j+(3 \left(t + 2\right)^{2})\,k) \\  & =(3 \left(t + 2\right)^{3} \ln{\left(t + 2 \right)})\cdot (2 t + 4)+(3 \left(t + 2\right)^{4})\cdot (1)+(3 \left(t + 2\right)^{2} \ln{\left(t + 2 \right)})\cdot (3 \left(t + 2\right)^{2}) \\  & =(3 \left(t + 2\right)^{3} \left(2 t + 4\right) \ln{\left(t + 2 \right)})+(3 \left(t + 2\right)^{4})+(9 \left(t + 2\right)^{4} \ln{\left(t + 2 \right)}) \\  & =3 \left(5 t^{4} \ln{\left(t + 2 \right)} + t^{4} + 40 t^{3} \ln{\left(t + 2 \right)} + 8 t^{3} + 120 t^{2} \ln{\left(t + 2 \right)} + 24 t^{2} + 160 t \ln{\left(t + 2 \right)} + 32 t + 80 \ln{\left(t + 2 \right)} + 16\right).\end{aligned}
$$

