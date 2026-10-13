# Frozen step-7 review

Raw evidence is explicitly ineligible. Normal examples use authored complete method banks. No plots occur.


## original raw evidence — q-161928

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=({t}^{2}-t)\,i+(t-{t}^{3})\,j+(2{t}^{2}-2t)\,k$ for $t\in [0,1).$
Given that $F(x,y,z)=y\,i+x\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\frac{1}{60}$

- $-1$

- $0$

- $\frac{2}{25}$

- $\frac{3}{32}$

- $\frac{1}{60}$

- $0$

- $\frac{2}{25}$

- $\frac{3}{32}$

- $-1$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x={t}^{2}-t,\,y=t-{t}^{3},\,z=2{t}^{2}-2t.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,k \\  & =(t-{t}^{3})\,i+({t}^{2}-t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,i+\frac{\text{d}}{\text{d}t}(t-{t}^{3})\,j-\frac{\text{d}}{\text{d}t}(2{t}^{2}-2t)\,k \\  & =(2t-1)\,i+(1-3{t}^{2})\,j+(4t-2)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((t-{t}^{3})\,i+({t}^{2}-t)\,k)\cdot ((2t-1)\,i+(1-3{t}^{2})\,j+(4t-2)\,k) \\  & =(t-{t}^{3})\cdot (2t-1)+0\cdot (1-3{t}^{2})+({t}^{2}-t)\cdot (4t-2) \\  & =t-4{t}^{2}+5{t}^{3}-2{t}^{4}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}(t-4{t}^{2}+5{t}^{3}-2{t}^{4})\,\text{d}t \\  & ={[\frac{{t}^{2}}{2}-\frac{4{t}^{3}}{3}+\frac{5{t}^{3}}{4}-\frac{2{t}^{5}}{5}]}_{0}^{1} \\  & =\frac{1}{2}-\frac{4}{3}+\frac{5}{4}-\frac{2}{5} \\  & =\frac{1}{60}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-161928

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 t^{2} + 2 t, t^{3} - t, - 6 t^{2} + 6 t\rangle$ for $t\in [0,1).$
Given that $F(x,y,z)=\langle 3 y, 0, 3 x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{1}{4}$

- $9$

- $\frac{1}{10}$

- $\frac{9}{10}$

- $- \frac{1}{10}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 t^{2} + 2 t,\quad y=t^{3} - t,\quad z=- 6 t^{2} + 6 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 0, 3 x\rangle \\ & =\langle 3 \left(t^{3} - t\right), 0, 3 \left(- 2 t^{2} + 2 t\right)\rangle \\ & =\langle 3 t^{3} - 3 t, 0, - 6 t^{2} + 6 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} + 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(t^{3} - t\right), \frac{\mathrm d}{\mathrm dt}\left(- 6 t^{2} + 6 t\right)\rangle \\ & =\langle 2 - 4 t, 3 t^{2} - 1, 6 - 12 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 3 t^{3} - 3 t, 0, - 6 t^{2} + 6 t\rangle\cdot \langle 2 - 4 t, 3 t^{2} - 1, 6 - 12 t\rangle \\ & =\left(3 t^{3} - 3 t\right)\cdot \left(2 - 4 t\right)+\left(0\right)\cdot \left(3 t^{2} - 1\right)+\left(- 6 t^{2} + 6 t\right)\cdot \left(6 - 12 t\right) \\ & =\left(- 12 t^{4} + 6 t^{3} + 12 t^{2} - 6 t\right)+\left(0\right)+\left(72 t^{3} - 108 t^{2} + 36 t\right) \\ & =- 12 t^{4} + 78 t^{3} - 96 t^{2} + 30 t \\ & =- 12 t^{4} + 78 t^{3} - 96 t^{2} + 30 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(- 12 t^{4} + 78 t^{3} - 96 t^{2} + 30 t\right)\,\mathrm dt \\ & =\left[\left(- 32 t^{3}\right) + \left(- \frac{12 t^{5}}{5}\right) + \left(15 t^{2}\right) + \left(\frac{39 t^{4}}{2}\right)\right]_{0}^{1} \\ & =\left(\left(-32\right) + \left(- \frac{12}{5}\right) + \left(15\right) + \left(\frac{39}{2}\right)\right)-\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right) \\ & =\frac{1}{10}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-161928

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 t^{2} - 2 t, - t^{3} + t, - 2 t^{2} + 2 t\rangle$ for $t\in [0,1).$
Given that $F(x,y,z)=\langle - y, 0, - x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{1}{30}$

- $\frac{7}{30}$

- $\frac{1}{30}$

- $\frac{1}{12}$

- $\frac{7}{3}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 t^{2} - 2 t,\quad y=- t^{3} + t,\quad z=- 2 t^{2} + 2 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - y, 0, - x\rangle \\ & =\langle - \left(- t^{3} + t\right), 0, - \left(2 t^{2} - 2 t\right)\rangle \\ & =\langle t^{3} - t, 0, - 2 t^{2} + 2 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 t^{2} - 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{3} + t\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} + 2 t\right)\rangle \\ & =\langle 4 t - 2, 1 - 3 t^{2}, 2 - 4 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle t^{3} - t, 0, - 2 t^{2} + 2 t\rangle\cdot \langle 4 t - 2, 1 - 3 t^{2}, 2 - 4 t\rangle \\ & =\left(t^{3} - t\right)\cdot \left(4 t - 2\right)+\left(0\right)\cdot \left(1 - 3 t^{2}\right)+\left(- 2 t^{2} + 2 t\right)\cdot \left(2 - 4 t\right) \\ & =\left(4 t^{4} - 2 t^{3} - 4 t^{2} + 2 t\right)+\left(0\right)+\left(8 t^{3} - 12 t^{2} + 4 t\right) \\ & =4 t^{4} + 6 t^{3} - 16 t^{2} + 6 t \\ & =4 t^{4} + 6 t^{3} - 16 t^{2} + 6 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(4 t^{4} + 6 t^{3} - 16 t^{2} + 6 t\right)\,\mathrm dt \\ & =\left[\left(- \frac{16 t^{3}}{3}\right) + \left(\frac{4 t^{5}}{5}\right) + \left(3 t^{2}\right) + \left(\frac{3 t^{4}}{2}\right)\right]_{0}^{1} \\ & =\left(\left(- \frac{16}{3}\right) + \left(\frac{4}{5}\right) + \left(3\right) + \left(\frac{3}{2}\right)\right)-\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right) \\ & =- \frac{1}{30}\end{aligned}
$$


## original raw evidence — q-162377

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t) = \sin (πt)i + \cos (πt)j + \sin (πt)k$ for $t ∈ [- 1, 1)$.
Given that $F(x, y, z) = xi + yk$, evaluate the integral
$∬_(S)curlF \cdot dS$.

- $2π$

- $-2π$

- $0$

- $1$

- $π$


## authored bank/coefficient variant of observed family — q-162377

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 \sin{\left(\pi t \right)}, - \cos{\left(\pi t \right)}, - 3 \sin{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle 3 x, 0, 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{9 \pi}{2}$

- $9$

- $9 \pi$

- $0$

- $- 9 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 \sin{\left(\pi t \right)},\quad y=- \cos{\left(\pi t \right)},\quad z=- 3 \sin{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 x, 0, 3 y\rangle \\ & =\langle 3 \left(- 2 \sin{\left(\pi t \right)}\right), 0, 3 \left(- \cos{\left(\pi t \right)}\right)\rangle \\ & =\langle - 6 \sin{\left(\pi t \right)}, 0, - 3 \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 \sin{\left(\pi t \right)}\right)\rangle \\ & =\langle - 2 \pi \cos{\left(\pi t \right)}, \pi \sin{\left(\pi t \right)}, - 3 \pi \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 6 \sin{\left(\pi t \right)}, 0, - 3 \cos{\left(\pi t \right)}\rangle\cdot \langle - 2 \pi \cos{\left(\pi t \right)}, \pi \sin{\left(\pi t \right)}, - 3 \pi \cos{\left(\pi t \right)}\rangle \\ & =\left(- 6 \sin{\left(\pi t \right)}\right)\cdot \left(- 2 \pi \cos{\left(\pi t \right)}\right)+\left(0\right)\cdot \left(\pi \sin{\left(\pi t \right)}\right)+\left(- 3 \cos{\left(\pi t \right)}\right)\cdot \left(- 3 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(12 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right)+\left(0\right)+\left(9 \pi \cos^{2}{\left(\pi t \right)}\right) \\ & =12 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + 9 \pi \cos^{2}{\left(\pi t \right)} \\ & =12 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + \frac{9 \pi \cos{\left(2 \pi t \right)}}{2} + \frac{9 \pi}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(12 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + \frac{9 \pi \cos{\left(2 \pi t \right)}}{2} + \frac{9 \pi}{2}\right)\,\mathrm dt \\ & =\left[\left(\frac{9 \pi t}{2}\right) + \left(\frac{9 \sin{\left(2 \pi t \right)}}{4}\right) + \left(6 \sin^{2}{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(\frac{9 \pi}{2}\right) + \left(0\right) + \left(0\right)\right)-\left(\left(- \frac{9 \pi}{2}\right) + \left(0\right) + \left(0\right)\right) \\ & =9 \pi\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162377

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 \sin{\left(\pi t \right)}, \cos{\left(\pi t \right)}, - \sin{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle - x, 0, - y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\pi$

- $0$

- $- \pi$

- $\frac{\pi}{2}$

- $1$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 \sin{\left(\pi t \right)},\quad y=\cos{\left(\pi t \right)},\quad z=- \sin{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - x, 0, - y\rangle \\ & =\langle - \left(2 \sin{\left(\pi t \right)}\right), 0, - \left(\cos{\left(\pi t \right)}\right)\rangle \\ & =\langle - 2 \sin{\left(\pi t \right)}, 0, - \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(\cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(\pi t \right)}\right)\rangle \\ & =\langle 2 \pi \cos{\left(\pi t \right)}, - \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 2 \sin{\left(\pi t \right)}, 0, - \cos{\left(\pi t \right)}\rangle\cdot \langle 2 \pi \cos{\left(\pi t \right)}, - \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}\rangle \\ & =\left(- 2 \sin{\left(\pi t \right)}\right)\cdot \left(2 \pi \cos{\left(\pi t \right)}\right)+\left(0\right)\cdot \left(- \pi \sin{\left(\pi t \right)}\right)+\left(- \cos{\left(\pi t \right)}\right)\cdot \left(- \pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 4 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right)+\left(0\right)+\left(\pi \cos^{2}{\left(\pi t \right)}\right) \\ & =- 4 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + \pi \cos^{2}{\left(\pi t \right)} \\ & =- 4 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + \frac{\pi \cos{\left(2 \pi t \right)}}{2} + \frac{\pi}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 4 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + \frac{\pi \cos{\left(2 \pi t \right)}}{2} + \frac{\pi}{2}\right)\,\mathrm dt \\ & =\left[\left(\frac{\pi t}{2}\right) + \left(\frac{\sin{\left(2 \pi t \right)}}{4}\right) + \left(- 2 \sin^{2}{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(\frac{\pi}{2}\right) + \left(0\right) + \left(0\right)\right)-\left(\left(- \frac{\pi}{2}\right) + \left(0\right) + \left(0\right)\right) \\ & =\pi\end{aligned}
$$


## original raw evidence — q-162316

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=(2{t}^{3}-2t)\,i+(3{t}^{2}+3t)\,j+({t}^{3}-t)\,k$ for $t\in [-1,0).$
Given that $F(x,y,z)=z\,i+y\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\frac{1}{20}$

- $\frac{1}{5}$

- $\frac{7}{5}$

- $\frac{-5}{103}$

- $7$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2{t}^{3}-2t,\,y=3{t}^{2}+3t,\,z={t}^{3}-t.
$$

So,

$$
\begin{aligned}F(r(t)) & =z\,i+x\,k \\  & =({t}^{3}-t)\,i+(3{t}^{2}+3t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{3}-2t)\,i+\frac{\text{d}}{\text{d}t}(3{t}^{2}+3t)\,j-\frac{\text{d}}{\text{d}t}({t}^{3}-t)\,k \\  & =(6{t}^{2}-2)\,i+(6t+3)\,j+(3{t}^{2}-1)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(({t}^{3}-t)\,i+(3{t}^{2}+3t)\,k)\cdot ((6{t}^{2}-2)\,i+(6t+3)\,j+(3{t}^{2}-1)\,k) \\  & =({t}^{3}-t)\cdot (6{t}^{2}-2)+0\cdot (6t+3)+(3{t}^{2}+3t)\cdot (3{t}^{2}-1) \\  & =6{t}^{5}+9{t}^{4}+{t}^{3}-3{t}^{2}-t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{0}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{0}(6{t}^{5}+9{t}^{4}+{t}^{3}-3{t}^{2}-t)\,\text{d}t \\  & ={[{t}^{6}+\frac{9{t}^{5}}{5}+\frac{{t}^{4}}{4}-{t}^{3}-\frac{{t}^{2}}{2}]}_{-1}^{0} \\  & =0-(1-\frac{9}{5}+\frac{1}{4}+1-\frac{1}{2}) \\  & =\frac{1}{20}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162316

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 4 t^{3} + 4 t, - 3 t^{2} - 3 t, - 3 t^{3} + 3 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle 3 z, 0, 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{3}{4}$

- $\frac{153}{10}$

- $\frac{9}{20}$

- $\frac{39}{28}$

- $- \frac{9}{20}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 4 t^{3} + 4 t,\quad y=- 3 t^{2} - 3 t,\quad z=- 3 t^{3} + 3 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 z, 0, 3 y\rangle \\ & =\langle 3 \left(- 3 t^{3} + 3 t\right), 0, 3 \left(- 3 t^{2} - 3 t\right)\rangle \\ & =\langle - 9 t^{3} + 9 t, 0, - 9 t^{2} - 9 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 4 t^{3} + 4 t\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 t^{2} - 3 t\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 t^{3} + 3 t\right)\rangle \\ & =\langle 4 - 12 t^{2}, - 6 t - 3, 3 - 9 t^{2}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 9 t^{3} + 9 t, 0, - 9 t^{2} - 9 t\rangle\cdot \langle 4 - 12 t^{2}, - 6 t - 3, 3 - 9 t^{2}\rangle \\ & =\left(- 9 t^{3} + 9 t\right)\cdot \left(4 - 12 t^{2}\right)+\left(0\right)\cdot \left(- 6 t - 3\right)+\left(- 9 t^{2} - 9 t\right)\cdot \left(3 - 9 t^{2}\right) \\ & =\left(108 t^{5} - 144 t^{3} + 36 t\right)+\left(0\right)+\left(81 t^{4} + 81 t^{3} - 27 t^{2} - 27 t\right) \\ & =108 t^{5} + 81 t^{4} - 63 t^{3} - 27 t^{2} + 9 t \\ & =108 t^{5} + 81 t^{4} - 63 t^{3} - 27 t^{2} + 9 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(108 t^{5} + 81 t^{4} - 63 t^{3} - 27 t^{2} + 9 t\right)\,\mathrm dt \\ & =\left[\left(- \frac{63 t^{4}}{4}\right) + \left(- 9 t^{3}\right) + \left(\frac{9 t^{2}}{2}\right) + \left(\frac{81 t^{5}}{5}\right) + \left(18 t^{6}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(- \frac{63}{4}\right) + \left(9\right) + \left(\frac{9}{2}\right) + \left(- \frac{81}{5}\right) + \left(18\right)\right) \\ & =\frac{9}{20}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162316

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 4 t^{3} - 4 t, 3 t^{2} + 3 t, - t^{3} + t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle - z, 0, - y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{1}{20}$

- $\frac{13}{84}$

- $- \frac{1}{20}$

- $\frac{3}{4}$

- $\frac{17}{10}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=4 t^{3} - 4 t,\quad y=3 t^{2} + 3 t,\quad z=- t^{3} + t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - z, 0, - y\rangle \\ & =\langle - \left(- t^{3} + t\right), 0, - \left(3 t^{2} + 3 t\right)\rangle \\ & =\langle t^{3} - t, 0, - 3 t^{2} - 3 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(4 t^{3} - 4 t\right), \frac{\mathrm d}{\mathrm dt}\left(3 t^{2} + 3 t\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{3} + t\right)\rangle \\ & =\langle 12 t^{2} - 4, 6 t + 3, 1 - 3 t^{2}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle t^{3} - t, 0, - 3 t^{2} - 3 t\rangle\cdot \langle 12 t^{2} - 4, 6 t + 3, 1 - 3 t^{2}\rangle \\ & =\left(t^{3} - t\right)\cdot \left(12 t^{2} - 4\right)+\left(0\right)\cdot \left(6 t + 3\right)+\left(- 3 t^{2} - 3 t\right)\cdot \left(1 - 3 t^{2}\right) \\ & =\left(12 t^{5} - 16 t^{3} + 4 t\right)+\left(0\right)+\left(9 t^{4} + 9 t^{3} - 3 t^{2} - 3 t\right) \\ & =12 t^{5} + 9 t^{4} - 7 t^{3} - 3 t^{2} + t \\ & =12 t^{5} + 9 t^{4} - 7 t^{3} - 3 t^{2} + t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(12 t^{5} + 9 t^{4} - 7 t^{3} - 3 t^{2} + t\right)\,\mathrm dt \\ & =\left[\left(\frac{t^{2}}{2}\right) + \left(- \frac{7 t^{4}}{4}\right) + \left(- t^{3}\right) + \left(\frac{9 t^{5}}{5}\right) + \left(2 t^{6}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(\frac{1}{2}\right) + \left(- \frac{7}{4}\right) + \left(1\right) + \left(- \frac{9}{5}\right) + \left(2\right)\right) \\ & =\frac{1}{20}\end{aligned}
$$


## original raw evidence — q-162324

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+\operatorname{cos}⁡(\pi t)\,k$ for $t\in [-1,1).$
Given that $F(x,y,z)=y\,i+x\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $-\frac{2}{\pi }$

- $2$

- $2\pi $

- $-1$

- $-\pi $

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=\operatorname{cos}⁡(\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,k \\  & =\operatorname{sin}⁡(\pi t)\,i+\operatorname{cos}⁡(\pi t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,k \\  & =-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-\pi \operatorname{sin}⁡(\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡(\pi t)\,i+\operatorname{cos}⁡(\pi t)\,k)\cdot (-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-\pi \operatorname{sin}⁡(\pi t)\,k) \\  & =\operatorname{sin}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t))+0\cdot \pi \operatorname{cos}⁡(\pi t)+\operatorname{cos}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t)) \\  & =-\pi \operatorname{sin}⁡(\pi t)\operatorname{cos}⁡(\pi t)-\pi {sin}^{2}⁡(\pi t).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{1}(-\pi \operatorname{sin}⁡(\pi t)\operatorname{cos}⁡(\pi t)-\pi {sin}^{2}⁡(\pi t))\,\text{d}t \\  & =-{\int }_{-1}^{1}(\pi \operatorname{sin}⁡(\pi t)\operatorname{cos}⁡(\pi t)+\frac{\pi }{2}(1-\operatorname{cos}⁡(2\pi t)))\,\text{d}t \\  & =-{[\frac{{sin}^{2}⁡(\pi t)}{2}+\frac{\pi t}{2}-\frac{\operatorname{sin}⁡(2\pi t)}{4}]}_{-1}^{1} \\  & =-[0+\frac{\pi }{2}+0-(0-\frac{\pi }{2}+0)] \\  & =-\pi \end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162324

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 \cos{\left(\pi t \right)}, - \sin{\left(\pi t \right)}, - 3 \cos{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle 3 y, 0, 3 x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 3 \pi$

- $-6$

- $- 6 \pi$

- $0$

- $6 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 \cos{\left(\pi t \right)},\quad y=- \sin{\left(\pi t \right)},\quad z=- 3 \cos{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 0, 3 x\rangle \\ & =\langle 3 \left(- \sin{\left(\pi t \right)}\right), 0, 3 \left(- 2 \cos{\left(\pi t \right)}\right)\rangle \\ & =\langle - 3 \sin{\left(\pi t \right)}, 0, - 6 \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 \cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 \cos{\left(\pi t \right)}\right)\rangle \\ & =\langle 2 \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}, 3 \pi \sin{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 3 \sin{\left(\pi t \right)}, 0, - 6 \cos{\left(\pi t \right)}\rangle\cdot \langle 2 \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}, 3 \pi \sin{\left(\pi t \right)}\rangle \\ & =\left(- 3 \sin{\left(\pi t \right)}\right)\cdot \left(2 \pi \sin{\left(\pi t \right)}\right)+\left(0\right)\cdot \left(- \pi \cos{\left(\pi t \right)}\right)+\left(- 6 \cos{\left(\pi t \right)}\right)\cdot \left(3 \pi \sin{\left(\pi t \right)}\right) \\ & =\left(- 6 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(0\right)+\left(- 18 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 6 \pi \sin^{2}{\left(\pi t \right)} - 18 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} \\ & =- 18 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + 3 \pi \cos{\left(2 \pi t \right)} - 3 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 18 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} + 3 \pi \cos{\left(2 \pi t \right)} - 3 \pi\right)\,\mathrm dt \\ & =\left[\left(- 3 \pi t\right) + \left(\frac{3 \sin{\left(2 \pi t \right)}}{2}\right) + \left(- 9 \sin^{2}{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(- 3 \pi\right) + \left(0\right) + \left(0\right)\right)-\left(\left(3 \pi\right) + \left(0\right) + \left(0\right)\right) \\ & =- 6 \pi\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162324

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 \cos{\left(\pi t \right)}, \sin{\left(\pi t \right)}, - \cos{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle - y, 0, - x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $2 \pi$

- $0$

- $- 2 \pi$

- $\pi$

- $2$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 \cos{\left(\pi t \right)},\quad y=\sin{\left(\pi t \right)},\quad z=- \cos{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - y, 0, - x\rangle \\ & =\langle - \left(\sin{\left(\pi t \right)}\right), 0, - \left(2 \cos{\left(\pi t \right)}\right)\rangle \\ & =\langle - \sin{\left(\pi t \right)}, 0, - 2 \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(\sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(\pi t \right)}\right)\rangle \\ & =\langle - 2 \pi \sin{\left(\pi t \right)}, \pi \cos{\left(\pi t \right)}, \pi \sin{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - \sin{\left(\pi t \right)}, 0, - 2 \cos{\left(\pi t \right)}\rangle\cdot \langle - 2 \pi \sin{\left(\pi t \right)}, \pi \cos{\left(\pi t \right)}, \pi \sin{\left(\pi t \right)}\rangle \\ & =\left(- \sin{\left(\pi t \right)}\right)\cdot \left(- 2 \pi \sin{\left(\pi t \right)}\right)+\left(0\right)\cdot \left(\pi \cos{\left(\pi t \right)}\right)+\left(- 2 \cos{\left(\pi t \right)}\right)\cdot \left(\pi \sin{\left(\pi t \right)}\right) \\ & =\left(2 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(0\right)+\left(- 2 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =2 \pi \sin^{2}{\left(\pi t \right)} - 2 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} \\ & =- 2 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} - \pi \cos{\left(2 \pi t \right)} + \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 2 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)} - \pi \cos{\left(2 \pi t \right)} + \pi\right)\,\mathrm dt \\ & =\left[\left(\pi t\right) + \left(- \frac{\sin{\left(2 \pi t \right)}}{2}\right) + \left(- \sin^{2}{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(\pi\right) + \left(0\right) + \left(0\right)\right)-\left(\left(- \pi\right) + \left(0\right) + \left(0\right)\right) \\ & =2 \pi\end{aligned}
$$


## original raw evidence — q-162886

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=({t}^{2}+t)\,i+({t}^{3}+{t}^{2})\,j+(2{t}^{2}+2t)\,k$ for $t\in [-1,0).$
Given that $F(x,y,z)=y\,i+z\,j+x\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\frac{3}{20}$

- $\frac{7}{45}$

- $\frac{2}{15}$

- $\frac{1}{60}$

- $\frac{1}{15}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x={t}^{2}+t,\,y={t}^{3}+{t}^{2},\,z=2{t}^{2}+2t.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+z\,j+x\,k \\  & =({t}^{3}+{t}^{2})\,i+(2{t}^{2}+2t)\,j+({t}^{2}+t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}+t)\,i+\frac{\text{d}}{\text{d}t}({t}^{3}+{t}^{2})\,j+\frac{\text{d}}{\text{d}t}(2{t}^{2}+2t)\,k \\  & =(2t+1)\,i+(3{t}^{2}+2t)\,j+(4t+2)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(({t}^{3}+{t}^{2})\,i+(2{t}^{2}+2t)\,j+({t}^{2}+t)\,k)\cdot ((2t+1)\,i+(3{t}^{2}+2t)\,j+(4t+2)\,k) \\  & =({t}^{3}+{t}^{2})(2t+1)+(2{t}^{2}+2t)(3{t}^{2}+2t)+({t}^{2}+t)(4t+2) \\  & =2t+11{t}^{2}+17{t}^{3}+8{t}^{4}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{0}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{0}(2t+11{t}^{2}+17{t}^{3}+8{t}^{4})\,\text{d}t \\  & ={[{t}^{2}+\frac{11}{3}{t}^{3}+\frac{17}{4}{t}^{4}+\frac{8}{5}{t}^{5}]}_{-1}^{0} \\  & =0-(1-\frac{11}{3}+\frac{17}{4}-\frac{8}{5}) \\  & =\frac{1}{60}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162886

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 t^{2} - 2 t, - t^{3} - t^{2}, - 6 t^{2} - 6 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle 3 y, 3 z, 3 x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{15}{4}$

- $8$

- $\frac{1}{5}$

- $\frac{4}{5}$

- $- \frac{1}{5}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 t^{2} - 2 t,\quad y=- t^{3} - t^{2},\quad z=- 6 t^{2} - 6 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 3 z, 3 x\rangle \\ & =\langle 3 \left(- t^{3} - t^{2}\right), 3 \left(- 6 t^{2} - 6 t\right), 3 \left(- 2 t^{2} - 2 t\right)\rangle \\ & =\langle - 3 t^{3} - 3 t^{2}, - 18 t^{2} - 18 t, - 6 t^{2} - 6 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} - 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{3} - t^{2}\right), \frac{\mathrm d}{\mathrm dt}\left(- 6 t^{2} - 6 t\right)\rangle \\ & =\langle - 4 t - 2, - 3 t^{2} - 2 t, - 12 t - 6\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 3 t^{3} - 3 t^{2}, - 18 t^{2} - 18 t, - 6 t^{2} - 6 t\rangle\cdot \langle - 4 t - 2, - 3 t^{2} - 2 t, - 12 t - 6\rangle \\ & =\left(- 3 t^{3} - 3 t^{2}\right)\cdot \left(- 4 t - 2\right)+\left(- 18 t^{2} - 18 t\right)\cdot \left(- 3 t^{2} - 2 t\right)+\left(- 6 t^{2} - 6 t\right)\cdot \left(- 12 t - 6\right) \\ & =\left(12 t^{4} + 18 t^{3} + 6 t^{2}\right)+\left(54 t^{4} + 90 t^{3} + 36 t^{2}\right)+\left(72 t^{3} + 108 t^{2} + 36 t\right) \\ & =66 t^{4} + 180 t^{3} + 150 t^{2} + 36 t \\ & =66 t^{4} + 180 t^{3} + 150 t^{2} + 36 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(66 t^{4} + 180 t^{3} + 150 t^{2} + 36 t\right)\,\mathrm dt \\ & =\left[\left(18 t^{2}\right) + \left(\frac{66 t^{5}}{5}\right) + \left(50 t^{3}\right) + \left(45 t^{4}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(18\right) + \left(- \frac{66}{5}\right) + \left(-50\right) + \left(45\right)\right) \\ & =\frac{1}{5}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162886

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 t^{2} + 2 t, t^{3} + t^{2}, - 2 t^{2} - 2 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle - y, - z, - x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{1}{15}$

- $\frac{2}{15}$

- $- \frac{1}{15}$

- $- \frac{1}{12}$

- $\frac{4}{3}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 t^{2} + 2 t,\quad y=t^{3} + t^{2},\quad z=- 2 t^{2} - 2 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - y, - z, - x\rangle \\ & =\langle - \left(t^{3} + t^{2}\right), - \left(- 2 t^{2} - 2 t\right), - \left(2 t^{2} + 2 t\right)\rangle \\ & =\langle - t^{3} - t^{2}, 2 t^{2} + 2 t, - 2 t^{2} - 2 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 t^{2} + 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(t^{3} + t^{2}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} - 2 t\right)\rangle \\ & =\langle 4 t + 2, 3 t^{2} + 2 t, - 4 t - 2\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - t^{3} - t^{2}, 2 t^{2} + 2 t, - 2 t^{2} - 2 t\rangle\cdot \langle 4 t + 2, 3 t^{2} + 2 t, - 4 t - 2\rangle \\ & =\left(- t^{3} - t^{2}\right)\cdot \left(4 t + 2\right)+\left(2 t^{2} + 2 t\right)\cdot \left(3 t^{2} + 2 t\right)+\left(- 2 t^{2} - 2 t\right)\cdot \left(- 4 t - 2\right) \\ & =\left(- 4 t^{4} - 6 t^{3} - 2 t^{2}\right)+\left(6 t^{4} + 10 t^{3} + 4 t^{2}\right)+\left(8 t^{3} + 12 t^{2} + 4 t\right) \\ & =2 t^{4} + 12 t^{3} + 14 t^{2} + 4 t \\ & =2 t^{4} + 12 t^{3} + 14 t^{2} + 4 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(2 t^{4} + 12 t^{3} + 14 t^{2} + 4 t\right)\,\mathrm dt \\ & =\left[\left(\frac{2 t^{5}}{5}\right) + \left(2 t^{2}\right) + \left(3 t^{4}\right) + \left(\frac{14 t^{3}}{3}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(- \frac{2}{5}\right) + \left(2\right) + \left(3\right) + \left(- \frac{14}{3}\right)\right) \\ & =\frac{1}{15}\end{aligned}
$$


## original raw evidence — q-162887

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=({t}^{3}-t)\,i+(2{t}^{2}+1)\,j+({t}^{2}-1)\,k$ for $t\in [-1,1).$
Given that $F(x,y,z)=y\,i+3\,j+yz\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\frac{7}{12}$

- $\frac{11}{10}$

- $\frac{5}{6}$

- $\frac{9}{8}$

- $\frac{16}{15}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x={t}^{3}-t,\,y=2{t}^{2}+1,\,z={t}^{2}-1.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+3\,j+yz\,k \\  & =(2{t}^{2}+1)\,i+3\,j+(2{t}^{2}+1)({t}^{2}-1)\,k \\  & =(2{t}^{2}+1)\,i+3\,j+(2{t}^{4}-{t}^{2}-1)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3}-t)\,i+\frac{\text{d}}{\text{d}t}(2{t}^{2}+1)\,j+\frac{\text{d}}{\text{d}t}({t}^{2}-1)\,k \\  & =(3{t}^{2}-1)\,i+4t\,j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((2{t}^{2}+1)\,i+3\,j+(2{t}^{4}-{t}^{2}-1)\,k)\cdot ((3{t}^{2}-1)\,i+4t\,j+2t\,k) \\  & =(2{t}^{2}+1)(3{t}^{2}-1)+3(4t)+(2{t}^{4}-{t}^{2}-1)(2t) \\  & =-1+10t+{t}^{2}-2{t}^{3}+6{t}^{4}+4{t}^{5}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{1}(-1+10t+{t}^{2}-2{t}^{3}+6{t}^{4}+4{t}^{5})\,\text{d}t \\  & ={[-t+5{t}^{2}+\frac{1}{3}{t}^{3}-\frac{1}{2}{t}^{4}+\frac{6}{5}{t}^{5}+\frac{2}{3}{t}^{6}]}_{-1}^{1} \\  & =(-1+5+\frac{1}{3}-\frac{1}{2}+\frac{6}{5}+\frac{2}{3})-(1+5-\frac{1}{3}-\frac{1}{2}-\frac{6}{5}+\frac{2}{3}) \\  & =-2+\frac{2}{3}+\frac{12}{5} \\  & =\frac{16}{15}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162887

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 t^{3} + 2 t, 4 t^{2} + 2, 2 t^{2} - 2\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle 3 y, 9, 3 y z\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{78}{5}$

- $0$

- $- \frac{64}{5}$

- $\frac{3252}{35}$

- $\frac{64}{5}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 t^{3} + 2 t,\quad y=4 t^{2} + 2,\quad z=2 t^{2} - 2
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 9, 3 y z\rangle \\ & =\langle 3 \left(4 t^{2} + 2\right), 9, 3 \left(4 t^{2} + 2\right) \left(2 t^{2} - 2\right)\rangle \\ & =\langle 12 t^{2} + 6, 9, 24 t^{4} - 12 t^{2} - 12\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{3} + 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(4 t^{2} + 2\right), \frac{\mathrm d}{\mathrm dt}\left(2 t^{2} - 2\right)\rangle \\ & =\langle 2 - 6 t^{2}, 8 t, 4 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 12 t^{2} + 6, 9, 24 t^{4} - 12 t^{2} - 12\rangle\cdot \langle 2 - 6 t^{2}, 8 t, 4 t\rangle \\ & =\left(12 t^{2} + 6\right)\cdot \left(2 - 6 t^{2}\right)+\left(9\right)\cdot \left(8 t\right)+\left(24 t^{4} - 12 t^{2} - 12\right)\cdot \left(4 t\right) \\ & =\left(- 72 t^{4} - 12 t^{2} + 12\right)+\left(72 t\right)+\left(96 t^{5} - 48 t^{3} - 48 t\right) \\ & =96 t^{5} - 72 t^{4} - 48 t^{3} - 12 t^{2} + 24 t + 12 \\ & =96 t^{5} - 72 t^{4} - 48 t^{3} - 12 t^{2} + 24 t + 12\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(96 t^{5} - 72 t^{4} - 48 t^{3} - 12 t^{2} + 24 t + 12\right)\,\mathrm dt \\ & =\left[\left(12 t\right) + \left(- \frac{72 t^{5}}{5}\right) + \left(- 12 t^{4}\right) + \left(- 4 t^{3}\right) + \left(12 t^{2}\right) + \left(16 t^{6}\right)\right]_{-1}^{1} \\ & =\left(\left(12\right) + \left(- \frac{72}{5}\right) + \left(-12\right) + \left(-4\right) + \left(12\right) + \left(16\right)\right)-\left(\left(-12\right) + \left(\frac{72}{5}\right) + \left(-12\right) + \left(4\right) + \left(12\right) + \left(16\right)\right) \\ & =- \frac{64}{5}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162887

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 t^{3} - 2 t, 2 t^{2} + 1, 1 - t^{2}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle - y, -3, - y z\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{32}{15}$

- $- \frac{398}{35}$

- $\frac{32}{15}$

- $- \frac{56}{5}$

- $0$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 t^{3} - 2 t,\quad y=2 t^{2} + 1,\quad z=1 - t^{2}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - y, -3, - y z\rangle \\ & =\langle - \left(2 t^{2} + 1\right), -3, - \left(2 t^{2} + 1\right) \left(1 - t^{2}\right)\rangle \\ & =\langle - 2 t^{2} - 1, -3, 2 t^{4} - t^{2} - 1\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 t^{3} - 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(2 t^{2} + 1\right), \frac{\mathrm d}{\mathrm dt}\left(1 - t^{2}\right)\rangle \\ & =\langle 6 t^{2} - 2, 4 t, - 2 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 2 t^{2} - 1, -3, 2 t^{4} - t^{2} - 1\rangle\cdot \langle 6 t^{2} - 2, 4 t, - 2 t\rangle \\ & =\left(- 2 t^{2} - 1\right)\cdot \left(6 t^{2} - 2\right)+\left(-3\right)\cdot \left(4 t\right)+\left(2 t^{4} - t^{2} - 1\right)\cdot \left(- 2 t\right) \\ & =\left(- 12 t^{4} - 2 t^{2} + 2\right)+\left(- 12 t\right)+\left(- 4 t^{5} + 2 t^{3} + 2 t\right) \\ & =- 4 t^{5} - 12 t^{4} + 2 t^{3} - 2 t^{2} - 10 t + 2 \\ & =- 4 t^{5} - 12 t^{4} + 2 t^{3} - 2 t^{2} - 10 t + 2\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 4 t^{5} - 12 t^{4} + 2 t^{3} - 2 t^{2} - 10 t + 2\right)\,\mathrm dt \\ & =\left[\left(2 t\right) + \left(- \frac{12 t^{5}}{5}\right) + \left(- 5 t^{2}\right) + \left(- \frac{2 t^{6}}{3}\right) + \left(- \frac{2 t^{3}}{3}\right) + \left(\frac{t^{4}}{2}\right)\right]_{-1}^{1} \\ & =\left(\left(2\right) + \left(- \frac{12}{5}\right) + \left(-5\right) + \left(- \frac{2}{3}\right) + \left(- \frac{2}{3}\right) + \left(\frac{1}{2}\right)\right)-\left(\left(-2\right) + \left(\frac{12}{5}\right) + \left(-5\right) + \left(- \frac{2}{3}\right) + \left(\frac{2}{3}\right) + \left(\frac{1}{2}\right)\right) \\ & =- \frac{32}{15}\end{aligned}
$$


## original raw evidence — q-162892

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+2\operatorname{sin}⁡(\pi t)\,k$ for $t\in [-1,1).$
Given that $F(x,y,z)=2y\,i-2x\,j+{e}^{z-2y}\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $3\pi $

- $-\pi $

- $2\pi $

- $0$

- $-4\pi $

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=2\operatorname{sin}⁡(\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =2y\,i-2x\,j+{e}^{z-2y}\,k \\  & =2\operatorname{sin}⁡(\pi t)\,i-2\operatorname{cos}⁡(\pi t)\,j+{e}^{2\operatorname{sin}⁡(\pi t)-2\operatorname{sin}⁡(\pi t)}\,k \\  & =2\operatorname{sin}⁡(\pi t)\,i-2\operatorname{cos}⁡(\pi t)\,j+k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡(\pi t))\,k \\  & =-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+2\pi \operatorname{cos}⁡(\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2\operatorname{sin}⁡(\pi t)\,i-2\operatorname{cos}⁡(\pi t)\,j+k)\cdot (-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+2\pi \operatorname{cos}⁡(\pi t)\,k) \\  & =2\operatorname{sin}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t))-2\operatorname{cos}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)+1\cdot 2\pi \operatorname{cos}⁡(\pi t) \\  & =-2\pi {sin}^{2}⁡(\pi t)-2\pi {cos}^{2}⁡(\pi t)+2\pi \operatorname{cos}⁡(\pi t) \\  & =-2\pi +2\pi \operatorname{cos}⁡(\pi t).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{1}(-2\pi +2\pi \operatorname{cos}⁡(\pi t))\,\text{d}t \\  & =[-2\pi t+2\operatorname{sin}⁡(\pi t)]_{-1}^{1} \\  & =(-2\pi (1)+0)-(-2\pi (-1)+0) \\  & =-4\pi \end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162892

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 \cos{\left(\pi t \right)}, - \sin{\left(\pi t \right)}, - 2 \sin{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle 6 y, - 6 x, 3 e^{- 2 y + z}\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 12 \pi$

- $-24$

- $- 24 \pi$

- $0$

- $24 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 \cos{\left(\pi t \right)},\quad y=- \sin{\left(\pi t \right)},\quad z=- 2 \sin{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 6 y, - 6 x, 3 e^{- 2 y + z}\rangle \\ & =\langle 6 \left(- \sin{\left(\pi t \right)}\right), - 6 \left(- 2 \cos{\left(\pi t \right)}\right), 3 e^{- 2 \left(- \sin{\left(\pi t \right)}\right) + \left(- 2 \sin{\left(\pi t \right)}\right)}\rangle \\ & =\langle - 6 \sin{\left(\pi t \right)}, 12 \cos{\left(\pi t \right)}, 3\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 \cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(\pi t \right)}\right)\rangle \\ & =\langle 2 \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}, - 2 \pi \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 6 \sin{\left(\pi t \right)}, 12 \cos{\left(\pi t \right)}, 3\rangle\cdot \langle 2 \pi \sin{\left(\pi t \right)}, - \pi \cos{\left(\pi t \right)}, - 2 \pi \cos{\left(\pi t \right)}\rangle \\ & =\left(- 6 \sin{\left(\pi t \right)}\right)\cdot \left(2 \pi \sin{\left(\pi t \right)}\right)+\left(12 \cos{\left(\pi t \right)}\right)\cdot \left(- \pi \cos{\left(\pi t \right)}\right)+\left(3\right)\cdot \left(- 2 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 12 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(- 12 \pi \cos^{2}{\left(\pi t \right)}\right)+\left(- 6 \pi \cos{\left(\pi t \right)}\right) \\ & =- 12 \pi \sin^{2}{\left(\pi t \right)} - 12 \pi \cos^{2}{\left(\pi t \right)} - 6 \pi \cos{\left(\pi t \right)} \\ & =- 6 \pi \cos{\left(\pi t \right)} - 12 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 6 \pi \cos{\left(\pi t \right)} - 12 \pi\right)\,\mathrm dt \\ & =\left[\left(- 12 \pi t\right) + \left(- 6 \sin{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(- 12 \pi\right) + \left(0\right)\right)-\left(\left(12 \pi\right) + \left(0\right)\right) \\ & =- 24 \pi\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162892

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 \cos{\left(\pi t \right)}, \sin{\left(\pi t \right)}, 2 \sin{\left(\pi t \right)}\rangle$ for $t\in [-1,1).$
Given that $F(x,y,z)=\langle - 2 y, 2 x, - e^{- 2 y + z}\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $8 \pi$

- $0$

- $- 8 \pi$

- $4 \pi$

- $8$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 \cos{\left(\pi t \right)},\quad y=\sin{\left(\pi t \right)},\quad z=2 \sin{\left(\pi t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - 2 y, 2 x, - e^{- 2 y + z}\rangle \\ & =\langle - 2 \left(\sin{\left(\pi t \right)}\right), 2 \left(2 \cos{\left(\pi t \right)}\right), - e^{- 2 \left(\sin{\left(\pi t \right)}\right) + \left(2 \sin{\left(\pi t \right)}\right)}\rangle \\ & =\langle - 2 \sin{\left(\pi t \right)}, 4 \cos{\left(\pi t \right)}, -1\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(\sin{\left(\pi t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(\pi t \right)}\right)\rangle \\ & =\langle - 2 \pi \sin{\left(\pi t \right)}, \pi \cos{\left(\pi t \right)}, 2 \pi \cos{\left(\pi t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 2 \sin{\left(\pi t \right)}, 4 \cos{\left(\pi t \right)}, -1\rangle\cdot \langle - 2 \pi \sin{\left(\pi t \right)}, \pi \cos{\left(\pi t \right)}, 2 \pi \cos{\left(\pi t \right)}\rangle \\ & =\left(- 2 \sin{\left(\pi t \right)}\right)\cdot \left(- 2 \pi \sin{\left(\pi t \right)}\right)+\left(4 \cos{\left(\pi t \right)}\right)\cdot \left(\pi \cos{\left(\pi t \right)}\right)+\left(-1\right)\cdot \left(2 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(4 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(4 \pi \cos^{2}{\left(\pi t \right)}\right)+\left(- 2 \pi \cos{\left(\pi t \right)}\right) \\ & =4 \pi \sin^{2}{\left(\pi t \right)} + 4 \pi \cos^{2}{\left(\pi t \right)} - 2 \pi \cos{\left(\pi t \right)} \\ & =- 2 \pi \cos{\left(\pi t \right)} + 4 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 2 \pi \cos{\left(\pi t \right)} + 4 \pi\right)\,\mathrm dt \\ & =\left[\left(4 \pi t\right) + \left(- 2 \sin{\left(\pi t \right)}\right)\right]_{-1}^{1} \\ & =\left(\left(4 \pi\right) + \left(0\right)\right)-\left(\left(- 4 \pi\right) + \left(0\right)\right) \\ & =8 \pi\end{aligned}
$$


## original raw evidence — q-162889

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j+k$ for $t\in [0,2\pi ).$
Given that $F(x,y,z)=z\,i+3x\,j+2{y}^{2}\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\pi +1$

- $\pi $

- $4\pi $

- $2\pi -1$

- $3\pi $

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t,\,z=1.
$$

So,

$$
\begin{aligned}F(r(t)) & =z\,i+3x\,j+2{y}^{2}\,k \\  & =\,i+3\operatorname{cos}⁡t\,j+2{sin}^{2}⁡t\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j+\frac{\text{d}}{\text{d}t}(1)\,k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+0\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\,i+3\operatorname{cos}⁡t\,j+2{sin}^{2}⁡t\,k)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+0\,k) \\  & =1\cdot (-\operatorname{sin}⁡t)+3\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t+2{sin}^{2}⁡t\cdot 0 \\  & =-\operatorname{sin}⁡t+3{cos}^{2}⁡t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }(-\operatorname{sin}⁡t+3{cos}^{2}⁡t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }(-\operatorname{sin}⁡t+\frac{3}{2}(1+\operatorname{cos}⁡2t))\,\text{d}t \\  & ={\int }_{0}^{2\pi }(-\operatorname{sin}⁡t+\frac{3}{2}+\frac{3}{2}\operatorname{cos}⁡2t)\,\text{d}t \\  & ={[\operatorname{cos}⁡t+\frac{3}{2}t+\frac{3}{4}\operatorname{sin}⁡2t]}_{0}^{2\pi } \\  & =(1+\frac{3}{2}(2\pi )+0)-(1+\frac{3}{2}(0)+0) \\  & =3\pi \end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162889

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 \cos{\left(t \right)}, - \sin{\left(t \right)}, -3\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle 3 z, 9 x, 6 y^{2}\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $-36 + 9 \pi$

- $36 \pi$

- $18 \pi$

- $0$

- $- 18 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 \cos{\left(t \right)},\quad y=- \sin{\left(t \right)},\quad z=-3
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 z, 9 x, 6 y^{2}\rangle \\ & =\langle 3 \left(-3\right), 9 \left(- 2 \cos{\left(t \right)}\right), 6 \left(- \sin{\left(t \right)}\right)^{2}\rangle \\ & =\langle -9, - 18 \cos{\left(t \right)}, 6 \sin^{2}{\left(t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(-3\right)\rangle \\ & =\langle 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle -9, - 18 \cos{\left(t \right)}, 6 \sin^{2}{\left(t \right)}\rangle\cdot \langle 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle \\ & =\left(-9\right)\cdot \left(2 \sin{\left(t \right)}\right)+\left(- 18 \cos{\left(t \right)}\right)\cdot \left(- \cos{\left(t \right)}\right)+\left(6 \sin^{2}{\left(t \right)}\right)\cdot \left(0\right) \\ & =\left(- 18 \sin{\left(t \right)}\right)+\left(18 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =- 18 \sin{\left(t \right)} + 18 \cos^{2}{\left(t \right)} \\ & =- 18 \sin{\left(t \right)} + 9 \cos{\left(2 t \right)} + 9\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(- 18 \sin{\left(t \right)} + 9 \cos{\left(2 t \right)} + 9\right)\,\mathrm dt \\ & =\left[\left(9 t\right) + \left(18 \cos{\left(t \right)}\right) + \left(\frac{9 \sin{\left(2 t \right)}}{2}\right)\right]_{0}^{2 \pi} \\ & =\left(\left(18 \pi\right) + \left(18\right) + \left(0\right)\right)-\left(\left(0\right) + \left(18\right) + \left(0\right)\right) \\ & =18 \pi\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162889

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 \cos{\left(t \right)}, \sin{\left(t \right)}, -1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle - z, - 3 x, - 2 y^{2}\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 6 \pi$

- $0$

- $6 \pi$

- $- 3 \pi - 4$

- $- 12 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 \cos{\left(t \right)},\quad y=\sin{\left(t \right)},\quad z=-1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - z, - 3 x, - 2 y^{2}\rangle \\ & =\langle - \left(-1\right), - 3 \left(2 \cos{\left(t \right)}\right), - 2 \left(\sin{\left(t \right)}\right)^{2}\rangle \\ & =\langle 1, - 6 \cos{\left(t \right)}, - 2 \sin^{2}{\left(t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(\sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(-1\right)\rangle \\ & =\langle - 2 \sin{\left(t \right)}, \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 1, - 6 \cos{\left(t \right)}, - 2 \sin^{2}{\left(t \right)}\rangle\cdot \langle - 2 \sin{\left(t \right)}, \cos{\left(t \right)}, 0\rangle \\ & =\left(1\right)\cdot \left(- 2 \sin{\left(t \right)}\right)+\left(- 6 \cos{\left(t \right)}\right)\cdot \left(\cos{\left(t \right)}\right)+\left(- 2 \sin^{2}{\left(t \right)}\right)\cdot \left(0\right) \\ & =\left(- 2 \sin{\left(t \right)}\right)+\left(- 6 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =- 2 \sin{\left(t \right)} - 6 \cos^{2}{\left(t \right)} \\ & =- 2 \sin{\left(t \right)} - 3 \cos{\left(2 t \right)} - 3\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(- 2 \sin{\left(t \right)} - 3 \cos{\left(2 t \right)} - 3\right)\,\mathrm dt \\ & =\left[\left(- 3 t\right) + \left(- \frac{3 \sin{\left(2 t \right)}}{2}\right) + \left(2 \cos{\left(t \right)}\right)\right]_{0}^{2 \pi} \\ & =\left(\left(- 6 \pi\right) + \left(0\right) + \left(2\right)\right)-\left(\left(0\right) + \left(0\right) + \left(2\right)\right) \\ & =- 6 \pi\end{aligned}
$$


## original raw evidence — q-162891

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j+(1-\operatorname{sin}⁡t)\,k$ for $t\in [0,2\pi ).$
Given that $F(x,y,z)=(y-z)\,i+(z-x)\,j+(x-y)\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $-4\pi $

- $-2\pi $

- $-8\pi $

- $3\pi $

- $\pi $

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t,\,z=1-\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =(y-z)\,i+(z-x)\,j+(x-y)\,k \\  & =(\operatorname{sin}⁡t-(1-\operatorname{sin}⁡t))\,i+(1-\operatorname{sin}⁡t-\operatorname{cos}⁡t)\,j+(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,k \\  & =(2\operatorname{sin}⁡t-1)\,i+(1-\operatorname{sin}⁡t-\operatorname{cos}⁡t)\,j+(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j+\frac{\text{d}}{\text{d}t}(1-\operatorname{sin}⁡t)\,k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j-\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((2\operatorname{sin}⁡t-1)\,i+(1-\operatorname{sin}⁡t-\operatorname{cos}⁡t)\,j+(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,k)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j-\operatorname{cos}⁡t\,k) \\  & =(2\operatorname{sin}⁡t-1)\cdot (-\operatorname{sin}⁡t)+(1-\operatorname{sin}⁡t-\operatorname{cos}⁡t)\cdot \operatorname{cos}⁡t+(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\cdot (-\operatorname{cos}⁡t) \\  & =-2{sin}^{2}⁡t+\operatorname{sin}⁡t+\operatorname{cos}⁡t-\operatorname{sin}⁡t\operatorname{cos}⁡t-{cos}^{2}⁡t-{cos}^{2}⁡t+\operatorname{sin}⁡t\operatorname{cos}⁡t \\  & =\operatorname{sin}⁡t+\operatorname{cos}⁡t-2{sin}^{2}⁡t-2{cos}^{2}⁡t \\  & =\operatorname{sin}⁡t+\operatorname{cos}⁡t-2.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }(\operatorname{sin}⁡t+\operatorname{cos}⁡t-2)\,\text{d}t \\  & =[-\operatorname{cos}⁡t+\operatorname{sin}⁡t-2t]_{0}^{2\pi } \\  & =(-1+0-2(2\pi ))-(-1+0-2(0)) \\  & =-4\pi \end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162891

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 \cos{\left(t \right)}, - \sin{\left(t \right)}, 3 \sin{\left(t \right)} - 3\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle 3 y - 3 z, - 3 x + 3 z, 3 x - 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $36 - 24 \pi$

- $- 96 \pi$

- $- 48 \pi$

- $0$

- $48 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 \cos{\left(t \right)},\quad y=- \sin{\left(t \right)},\quad z=3 \sin{\left(t \right)} - 3
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y - 3 z, - 3 x + 3 z, 3 x - 3 y\rangle \\ & =\langle 3 \left(- \sin{\left(t \right)}\right) - 3 \left(3 \sin{\left(t \right)} - 3\right), - 3 \left(- 2 \cos{\left(t \right)}\right) + 3 \left(3 \sin{\left(t \right)} - 3\right), 3 \left(- 2 \cos{\left(t \right)}\right) - 3 \left(- \sin{\left(t \right)}\right)\rangle \\ & =\langle 9 - 12 \sin{\left(t \right)}, 9 \sin{\left(t \right)} + 6 \cos{\left(t \right)} - 9, 3 \sin{\left(t \right)} - 6 \cos{\left(t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(t \right)} - 3\right)\rangle \\ & =\langle 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 3 \cos{\left(t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 9 - 12 \sin{\left(t \right)}, 9 \sin{\left(t \right)} + 6 \cos{\left(t \right)} - 9, 3 \sin{\left(t \right)} - 6 \cos{\left(t \right)}\rangle\cdot \langle 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 3 \cos{\left(t \right)}\rangle \\ & =\left(9 - 12 \sin{\left(t \right)}\right)\cdot \left(2 \sin{\left(t \right)}\right)+\left(9 \sin{\left(t \right)} + 6 \cos{\left(t \right)} - 9\right)\cdot \left(- \cos{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} - 6 \cos{\left(t \right)}\right)\cdot \left(3 \cos{\left(t \right)}\right) \\ & =\left(- 24 \sin^{2}{\left(t \right)} + 18 \sin{\left(t \right)}\right)+\left(- 9 \sin{\left(t \right)} \cos{\left(t \right)} - 6 \cos^{2}{\left(t \right)} + 9 \cos{\left(t \right)}\right)+\left(9 \sin{\left(t \right)} \cos{\left(t \right)} - 18 \cos^{2}{\left(t \right)}\right) \\ & =- 24 \sin^{2}{\left(t \right)} + 18 \sin{\left(t \right)} - 24 \cos^{2}{\left(t \right)} + 9 \cos{\left(t \right)} \\ & =18 \sin{\left(t \right)} + 9 \cos{\left(t \right)} - 24\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(18 \sin{\left(t \right)} + 9 \cos{\left(t \right)} - 24\right)\,\mathrm dt \\ & =\left[\left(- 24 t\right) + \left(9 \sin{\left(t \right)}\right) + \left(- 18 \cos{\left(t \right)}\right)\right]_{0}^{2 \pi} \\ & =\left(\left(- 48 \pi\right) + \left(0\right) + \left(-18\right)\right)-\left(\left(0\right) + \left(0\right) + \left(-18\right)\right) \\ & =- 48 \pi\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162891

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - \cos{\left(t \right)}, - 2 \sin{\left(t \right)}, 3 - 3 \sin{\left(t \right)}\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle 3 y - 3 z, - 3 x + 3 z, 3 x - 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $6 \pi$

- $0$

- $- 6 \pi$

- $-18 + 3 \pi$

- $12 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- \cos{\left(t \right)},\quad y=- 2 \sin{\left(t \right)},\quad z=3 - 3 \sin{\left(t \right)}
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y - 3 z, - 3 x + 3 z, 3 x - 3 y\rangle \\ & =\langle 3 \left(- 2 \sin{\left(t \right)}\right) - 3 \left(3 - 3 \sin{\left(t \right)}\right), - 3 \left(- \cos{\left(t \right)}\right) + 3 \left(3 - 3 \sin{\left(t \right)}\right), 3 \left(- \cos{\left(t \right)}\right) - 3 \left(- 2 \sin{\left(t \right)}\right)\rangle \\ & =\langle 3 \sin{\left(t \right)} - 9, - 9 \sin{\left(t \right)} + 3 \cos{\left(t \right)} + 9, 6 \sin{\left(t \right)} - 3 \cos{\left(t \right)}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(3 - 3 \sin{\left(t \right)}\right)\rangle \\ & =\langle \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, - 3 \cos{\left(t \right)}\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 3 \sin{\left(t \right)} - 9, - 9 \sin{\left(t \right)} + 3 \cos{\left(t \right)} + 9, 6 \sin{\left(t \right)} - 3 \cos{\left(t \right)}\rangle\cdot \langle \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, - 3 \cos{\left(t \right)}\rangle \\ & =\left(3 \sin{\left(t \right)} - 9\right)\cdot \left(\sin{\left(t \right)}\right)+\left(- 9 \sin{\left(t \right)} + 3 \cos{\left(t \right)} + 9\right)\cdot \left(- 2 \cos{\left(t \right)}\right)+\left(6 \sin{\left(t \right)} - 3 \cos{\left(t \right)}\right)\cdot \left(- 3 \cos{\left(t \right)}\right) \\ & =\left(3 \sin^{2}{\left(t \right)} - 9 \sin{\left(t \right)}\right)+\left(18 \sin{\left(t \right)} \cos{\left(t \right)} - 6 \cos^{2}{\left(t \right)} - 18 \cos{\left(t \right)}\right)+\left(- 18 \sin{\left(t \right)} \cos{\left(t \right)} + 9 \cos^{2}{\left(t \right)}\right) \\ & =3 \sin^{2}{\left(t \right)} - 9 \sin{\left(t \right)} + 3 \cos^{2}{\left(t \right)} - 18 \cos{\left(t \right)} \\ & =- 9 \sin{\left(t \right)} - 18 \cos{\left(t \right)} + 3\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(- 9 \sin{\left(t \right)} - 18 \cos{\left(t \right)} + 3\right)\,\mathrm dt \\ & =\left[\left(3 t\right) + \left(- 18 \sin{\left(t \right)}\right) + \left(9 \cos{\left(t \right)}\right)\right]_{0}^{2 \pi} \\ & =\left(\left(6 \pi\right) + \left(0\right) + \left(9\right)\right)-\left(\left(0\right) + \left(0\right) + \left(9\right)\right) \\ & =6 \pi\end{aligned}
$$


## original raw evidence — q-162999

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=({t}^{2}-t)\,i+({t}^{2}-{t}^{3})\,j+({t}^{2}-t)\,k$ for $t\in [0,1).$
Given that $F(x,y,z)=2z\,i+3y\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $\frac{3}{25}$

- $\frac{2}{5}$

- $\frac{4}{15}$

- $\frac{1}{15}$

- $\frac{1}{20}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x={t}^{2}-t,\,y={t}^{2}-{t}^{3},\,z={t}^{2}-t.
$$

So,

$$
\begin{aligned}F(r(t)) & =2z\,i+3y\,k \\  & =(2{t}^{2}-2t)\,i+(3{t}^{2}-3{t}^{3})\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2}-{t}^{3})\,j+\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,k \\  & =(2t-1)\,i+(2t-3{t}^{2})\,j+(2t-1)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((2{t}^{2}-2t)\,i+(3{t}^{2}-3{t}^{3})\,k)\cdot ((2t-1)\,i+(2t-3{t}^{2})\,j+(2t-1)\,k) \\  & =(2{t}^{2}-2t)\cdot (2t-1)+0\cdot (2t-3{t}^{2})+(3{t}^{2}-3{t}^{3})\cdot (2t-1) \\  & =(-3{t}^{3}+5{t}^{2}-2t)\cdot (2t-1) \\  & =2t-9{t}^{2}+13{t}^{3}-6{t}^{4}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}(2t-9{t}^{2}+13{t}^{3}-6{t}^{4})\,\text{d}t \\  & ={[{t}^{2}-3{t}^{3}+\frac{13}{4}{t}^{4}-\frac{6}{5}{t}^{5}]}_{0}^{1} \\  & =1-3+\frac{13}{4}-\frac{6}{5} \\  & =\frac{1}{20}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162999

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 t^{2} + 2 t, t^{3} - t^{2}, - 3 t^{2} + 3 t\rangle$ for $t\in [0,1).$
Given that $F(x,y,z)=\langle 6 z, 0, 9 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{9}{4}$

- $\frac{15}{2}$

- $\frac{9}{20}$

- $\frac{3}{4}$

- $- \frac{9}{20}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 t^{2} + 2 t,\quad y=t^{3} - t^{2},\quad z=- 3 t^{2} + 3 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 6 z, 0, 9 y\rangle \\ & =\langle 6 \left(- 3 t^{2} + 3 t\right), 0, 9 \left(t^{3} - t^{2}\right)\rangle \\ & =\langle - 18 t^{2} + 18 t, 0, 9 t^{3} - 9 t^{2}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} + 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(t^{3} - t^{2}\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 t^{2} + 3 t\right)\rangle \\ & =\langle 2 - 4 t, 3 t^{2} - 2 t, 3 - 6 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 18 t^{2} + 18 t, 0, 9 t^{3} - 9 t^{2}\rangle\cdot \langle 2 - 4 t, 3 t^{2} - 2 t, 3 - 6 t\rangle \\ & =\left(- 18 t^{2} + 18 t\right)\cdot \left(2 - 4 t\right)+\left(0\right)\cdot \left(3 t^{2} - 2 t\right)+\left(9 t^{3} - 9 t^{2}\right)\cdot \left(3 - 6 t\right) \\ & =\left(72 t^{3} - 108 t^{2} + 36 t\right)+\left(0\right)+\left(- 54 t^{4} + 81 t^{3} - 27 t^{2}\right) \\ & =- 54 t^{4} + 153 t^{3} - 135 t^{2} + 36 t \\ & =- 54 t^{4} + 153 t^{3} - 135 t^{2} + 36 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(- 54 t^{4} + 153 t^{3} - 135 t^{2} + 36 t\right)\,\mathrm dt \\ & =\left[\left(- 45 t^{3}\right) + \left(- \frac{54 t^{5}}{5}\right) + \left(18 t^{2}\right) + \left(\frac{153 t^{4}}{4}\right)\right]_{0}^{1} \\ & =\left(\left(-45\right) + \left(- \frac{54}{5}\right) + \left(18\right) + \left(\frac{153}{4}\right)\right)-\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right) \\ & =\frac{9}{20}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162999

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 t^{2} - 2 t, - t^{3} + t^{2}, - t^{2} + t\rangle$ for $t\in [0,1).$
Given that $F(x,y,z)=\langle - 2 z, 0, - 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{1}{20}$

- $\frac{1}{12}$

- $- \frac{1}{20}$

- $- \frac{7}{12}$

- $\frac{5}{6}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 t^{2} - 2 t,\quad y=- t^{3} + t^{2},\quad z=- t^{2} + t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - 2 z, 0, - 3 y\rangle \\ & =\langle - 2 \left(- t^{2} + t\right), 0, - 3 \left(- t^{3} + t^{2}\right)\rangle \\ & =\langle 2 t^{2} - 2 t, 0, 3 t^{3} - 3 t^{2}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 t^{2} - 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{3} + t^{2}\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{2} + t\right)\rangle \\ & =\langle 4 t - 2, - 3 t^{2} + 2 t, 1 - 2 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 2 t^{2} - 2 t, 0, 3 t^{3} - 3 t^{2}\rangle\cdot \langle 4 t - 2, - 3 t^{2} + 2 t, 1 - 2 t\rangle \\ & =\left(2 t^{2} - 2 t\right)\cdot \left(4 t - 2\right)+\left(0\right)\cdot \left(- 3 t^{2} + 2 t\right)+\left(3 t^{3} - 3 t^{2}\right)\cdot \left(1 - 2 t\right) \\ & =\left(8 t^{3} - 12 t^{2} + 4 t\right)+\left(0\right)+\left(- 6 t^{4} + 9 t^{3} - 3 t^{2}\right) \\ & =- 6 t^{4} + 17 t^{3} - 15 t^{2} + 4 t \\ & =- 6 t^{4} + 17 t^{3} - 15 t^{2} + 4 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(- 6 t^{4} + 17 t^{3} - 15 t^{2} + 4 t\right)\,\mathrm dt \\ & =\left[\left(- 5 t^{3}\right) + \left(- \frac{6 t^{5}}{5}\right) + \left(2 t^{2}\right) + \left(\frac{17 t^{4}}{4}\right)\right]_{0}^{1} \\ & =\left(\left(-5\right) + \left(- \frac{6}{5}\right) + \left(2\right) + \left(\frac{17}{4}\right)\right)-\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right) \\ & =\frac{1}{20}\end{aligned}
$$


## original raw evidence — q-162314

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=(2{t}^{3}-2t)\,i+(t+{t}^{2})\,j+(-t-{t}^{2})\,k$ for $t\in [-1,0).$
Given that $F(x,y,z)=y\,i+x\,k,$ evaluate the integral

$$
{∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

- $-2$

- $\frac{9}{5}$

- $-\frac{2}{3}$

- $0$

- $\frac{1}{15}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2{t}^{3}-2t,\,y=t+{t}^{2},\,z=-t-{t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,k \\  & =(t+{t}^{2})\,i+(2{t}^{3}-2t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{3}-2t)\,i+\frac{\text{d}}{\text{d}t}(t+{t}^{2})\,j-\frac{\text{d}}{\text{d}t}(-t-{t}^{2})\,k \\  & =(6{t}^{2}-2)\,i+(1+2t)\,j+(-1-2t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((t+{t}^{2})\,i+(2{t}^{3}-2t)\,k)\cdot ((6{t}^{2}-2)\,i+(1+2t)\,j+(-1-2t)\,k) \\  & =(t+{t}^{2})\cdot (6{t}^{2}-2)+0\cdot (1+2t)+(2{t}^{3}-2t)\cdot (-1-2t) \\  & =2{t}^{4}+4{t}^{3}+2{t}^{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{∬}_{S}\text{curl}\,F\cdot \text{d}S & ={∮}_{C}F\cdot dr \\  & ={\int }_{-1}^{0}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{0}(2{t}^{4}+4{t}^{3}+2{t}^{2})\,\text{d}t \\  & ={[\frac{2{t}^{5}}{5}+{t}^{4}+\frac{2{t}^{3}}{3}]}_{-1}^{0} \\  & =0-(-\frac{2}{5}+1-\frac{2}{3}) \\  & =\frac{1}{15}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162314

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 4 t^{3} + 4 t, - t^{2} - t, 3 t^{2} + 3 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle 3 y, 0, 3 x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{5}{2}$

- $12$

- $\frac{4}{5}$

- $\frac{6}{5}$

- $- \frac{4}{5}$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 4 t^{3} + 4 t,\quad y=- t^{2} - t,\quad z=3 t^{2} + 3 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 0, 3 x\rangle \\ & =\langle 3 \left(- t^{2} - t\right), 0, 3 \left(- 4 t^{3} + 4 t\right)\rangle \\ & =\langle - 3 t^{2} - 3 t, 0, - 12 t^{3} + 12 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 4 t^{3} + 4 t\right), \frac{\mathrm d}{\mathrm dt}\left(- t^{2} - t\right), \frac{\mathrm d}{\mathrm dt}\left(3 t^{2} + 3 t\right)\rangle \\ & =\langle 4 - 12 t^{2}, - 2 t - 1, 6 t + 3\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 3 t^{2} - 3 t, 0, - 12 t^{3} + 12 t\rangle\cdot \langle 4 - 12 t^{2}, - 2 t - 1, 6 t + 3\rangle \\ & =\left(- 3 t^{2} - 3 t\right)\cdot \left(4 - 12 t^{2}\right)+\left(0\right)\cdot \left(- 2 t - 1\right)+\left(- 12 t^{3} + 12 t\right)\cdot \left(6 t + 3\right) \\ & =\left(36 t^{4} + 36 t^{3} - 12 t^{2} - 12 t\right)+\left(0\right)+\left(- 72 t^{4} - 36 t^{3} + 72 t^{2} + 36 t\right) \\ & =- 36 t^{4} + 60 t^{2} + 24 t \\ & =- 36 t^{4} + 60 t^{2} + 24 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(- 36 t^{4} + 60 t^{2} + 24 t\right)\,\mathrm dt \\ & =\left[\left(- \frac{36 t^{5}}{5}\right) + \left(12 t^{2}\right) + \left(20 t^{3}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(\frac{36}{5}\right) + \left(12\right) + \left(-20\right)\right) \\ & =\frac{4}{5}\end{aligned}
$$


## authored bank/coefficient variant of observed family — q-162314

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - 2 t^{3} + 2 t, - 2 t^{2} - 2 t, - 3 t^{2} - 3 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle 3 y, 0, 3 x\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{1}{10}$

- $- \frac{3}{2}$

- $\frac{1}{10}$

- $- \frac{1}{2}$

- $-15$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- 2 t^{3} + 2 t,\quad y=- 2 t^{2} - 2 t,\quad z=- 3 t^{2} - 3 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, 0, 3 x\rangle \\ & =\langle 3 \left(- 2 t^{2} - 2 t\right), 0, 3 \left(- 2 t^{3} + 2 t\right)\rangle \\ & =\langle - 6 t^{2} - 6 t, 0, - 6 t^{3} + 6 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{3} + 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} - 2 t\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 t^{2} - 3 t\right)\rangle \\ & =\langle 2 - 6 t^{2}, - 4 t - 2, - 6 t - 3\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 6 t^{2} - 6 t, 0, - 6 t^{3} + 6 t\rangle\cdot \langle 2 - 6 t^{2}, - 4 t - 2, - 6 t - 3\rangle \\ & =\left(- 6 t^{2} - 6 t\right)\cdot \left(2 - 6 t^{2}\right)+\left(0\right)\cdot \left(- 4 t - 2\right)+\left(- 6 t^{3} + 6 t\right)\cdot \left(- 6 t - 3\right) \\ & =\left(36 t^{4} + 36 t^{3} - 12 t^{2} - 12 t\right)+\left(0\right)+\left(36 t^{4} + 18 t^{3} - 36 t^{2} - 18 t\right) \\ & =72 t^{4} + 54 t^{3} - 48 t^{2} - 30 t \\ & =72 t^{4} + 54 t^{3} - 48 t^{2} - 30 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(72 t^{4} + 54 t^{3} - 48 t^{2} - 30 t\right)\,\mathrm dt \\ & =\left[\left(- 16 t^{3}\right) + \left(- 15 t^{2}\right) + \left(\frac{27 t^{4}}{2}\right) + \left(\frac{72 t^{5}}{5}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(16\right) + \left(-15\right) + \left(\frac{27}{2}\right) + \left(- \frac{72}{5}\right)\right) \\ & =- \frac{1}{10}\end{aligned}
$$


## authored missing easy — easy-circle

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - \cos{\left(t \right)}, - 3 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle - y, x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $3 \pi$

- $6$

- $6 \pi$

- $0$

- $- 6 \pi$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- \cos{\left(t \right)},\quad y=- 3 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - y, x, 0\rangle \\ & =\langle - \left(- 3 \sin{\left(t \right)}\right), \left(- \cos{\left(t \right)}\right), 0\rangle \\ & =\langle 3 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 3 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\cdot \langle \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle \\ & =\left(3 \sin{\left(t \right)}\right)\cdot \left(\sin{\left(t \right)}\right)+\left(- \cos{\left(t \right)}\right)\cdot \left(- 3 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(3 \sin^{2}{\left(t \right)}\right)+\left(3 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =3 \sin^{2}{\left(t \right)} + 3 \cos^{2}{\left(t \right)} \\ & =3\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(3\right)\,\mathrm dt \\ & =\left[\left(3 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(6 \pi\right)\right)-\left(\left(0\right)\right) \\ & =6 \pi\end{aligned}
$$


## authored missing easy — easy-circle

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - \cos{\left(t \right)}, - \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle 2 y, - 2 x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 4 \pi$

- $0$

- $4 \pi$

- $- 2 \pi$

- $-4$

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- \cos{\left(t \right)},\quad y=- \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 2 y, - 2 x, 0\rangle \\ & =\langle 2 \left(- \sin{\left(t \right)}\right), - 2 \left(- \cos{\left(t \right)}\right), 0\rangle \\ & =\langle - 2 \sin{\left(t \right)}, 2 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 2 \sin{\left(t \right)}, 2 \cos{\left(t \right)}, 0\rangle\cdot \langle \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle \\ & =\left(- 2 \sin{\left(t \right)}\right)\cdot \left(\sin{\left(t \right)}\right)+\left(2 \cos{\left(t \right)}\right)\cdot \left(- \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(- 2 \sin^{2}{\left(t \right)}\right)+\left(- 2 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =- 2 \sin^{2}{\left(t \right)} - 2 \cos^{2}{\left(t \right)} \\ & =-2\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(-2\right)\,\mathrm dt \\ & =\left[\left(- 2 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(- 4 \pi\right)\right)-\left(\left(0\right)\right) \\ & =- 4 \pi\end{aligned}
$$
