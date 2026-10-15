## Generated variant — easy

authored easy

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - \cos{\left(t \right)}, - 2 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle - 3 y, 3 x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $6 \pi$

- $12 \pi$ **(correct)**

- $- 12 \pi$

- $0$

- $12$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- \cos{\left(t \right)},\quad y=- 2 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - 3 y, 3 x, 0\rangle \\ & =\langle - 3 \left(- 2 \sin{\left(t \right)}\right), 3 \left(- \cos{\left(t \right)}\right), 0\rangle \\ & =\langle 6 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 6 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\cdot \langle \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle \\ & =\left(6 \sin{\left(t \right)}\right)\cdot \left(\sin{\left(t \right)}\right)+\left(- 3 \cos{\left(t \right)}\right)\cdot \left(- 2 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(6 \sin^{2}{\left(t \right)}\right)+\left(6 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =6 \sin^{2}{\left(t \right)} + 6 \cos^{2}{\left(t \right)} \\ & =6\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(6\right)\,\mathrm dt \\ & =\left[\left(6 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(12 \pi\right)\right)-\left(\left(0\right)\right) \\ & =12 \pi\end{aligned}
$$

---

## Generated variant — easy

authored easy

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 2 \cos{\left(t \right)}, 3 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle y, - x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $-12$

- $- 6 \pi$

- $- 12 \pi$ **(correct)**

- $0$

- $12 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=2 \cos{\left(t \right)},\quad y=3 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle y, - x, 0\rangle \\ & =\langle \left(3 \sin{\left(t \right)}\right), - \left(2 \cos{\left(t \right)}\right), 0\rangle \\ & =\langle 3 \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle - 2 \sin{\left(t \right)}, 3 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 3 \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle\cdot \langle - 2 \sin{\left(t \right)}, 3 \cos{\left(t \right)}, 0\rangle \\ & =\left(3 \sin{\left(t \right)}\right)\cdot \left(- 2 \sin{\left(t \right)}\right)+\left(- 2 \cos{\left(t \right)}\right)\cdot \left(3 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(- 6 \sin^{2}{\left(t \right)}\right)+\left(- 6 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =- 6 \sin^{2}{\left(t \right)} - 6 \cos^{2}{\left(t \right)} \\ & =-6\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(-6\right)\,\mathrm dt \\ & =\left[\left(- 6 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(- 12 \pi\right)\right)-\left(\left(0\right)\right) \\ & =- 12 \pi\end{aligned}
$$

---

## Generated variant — easy

authored easy

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 3 \cos{\left(t \right)}, - 3 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle - 3 y, 3 x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 27 \pi$

- $- 54 \pi$ **(correct)**

- $0$

- $54 \pi$

- $-54$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=3 \cos{\left(t \right)},\quad y=- 3 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - 3 y, 3 x, 0\rangle \\ & =\langle - 3 \left(- 3 \sin{\left(t \right)}\right), 3 \left(3 \cos{\left(t \right)}\right), 0\rangle \\ & =\langle 9 \sin{\left(t \right)}, 9 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(3 \cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 3 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle - 3 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 9 \sin{\left(t \right)}, 9 \cos{\left(t \right)}, 0\rangle\cdot \langle - 3 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle \\ & =\left(9 \sin{\left(t \right)}\right)\cdot \left(- 3 \sin{\left(t \right)}\right)+\left(9 \cos{\left(t \right)}\right)\cdot \left(- 3 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(- 27 \sin^{2}{\left(t \right)}\right)+\left(- 27 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =- 27 \sin^{2}{\left(t \right)} - 27 \cos^{2}{\left(t \right)} \\ & =-27\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(-27\right)\,\mathrm dt \\ & =\left[\left(- 27 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(- 54 \pi\right)\right)-\left(\left(0\right)\right) \\ & =- 54 \pi\end{aligned}
$$

---

## Generated variant — easy

authored easy

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle \cos{\left(t \right)}, - 2 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle 3 y, - 3 x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- 12 \pi$

- $0$

- $12 \pi$ **(correct)**

- $12$

- $6 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\cos{\left(t \right)},\quad y=- 2 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle 3 y, - 3 x, 0\rangle \\ & =\langle 3 \left(- 2 \sin{\left(t \right)}\right), - 3 \left(\cos{\left(t \right)}\right), 0\rangle \\ & =\langle - 6 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(\cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle - \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 6 \sin{\left(t \right)}, - 3 \cos{\left(t \right)}, 0\rangle\cdot \langle - \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle \\ & =\left(- 6 \sin{\left(t \right)}\right)\cdot \left(- \sin{\left(t \right)}\right)+\left(- 3 \cos{\left(t \right)}\right)\cdot \left(- 2 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(6 \sin^{2}{\left(t \right)}\right)+\left(6 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =6 \sin^{2}{\left(t \right)} + 6 \cos^{2}{\left(t \right)} \\ & =6\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(6\right)\,\mathrm dt \\ & =\left[\left(6 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(12 \pi\right)\right)-\left(\left(0\right)\right) \\ & =12 \pi\end{aligned}
$$

---

## Generated variant — easy

authored easy

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle \cos{\left(t \right)}, - 2 \sin{\left(t \right)}, 1\rangle$ for $t\in [0,2 \pi).$
Given that $F(x,y,z)=\langle y, - x, 0\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $0$

- $4 \pi$ **(correct)**

- $2 \pi$

- $- 4 \pi$

- $4$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=\cos{\left(t \right)},\quad y=- 2 \sin{\left(t \right)},\quad z=1
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle y, - x, 0\rangle \\ & =\langle \left(- 2 \sin{\left(t \right)}\right), - \left(\cos{\left(t \right)}\right), 0\rangle \\ & =\langle - 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(\cos{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 \sin{\left(t \right)}\right), \frac{\mathrm d}{\mathrm dt}\left(1\right)\rangle \\ & =\langle - \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 2 \sin{\left(t \right)}, - \cos{\left(t \right)}, 0\rangle\cdot \langle - \sin{\left(t \right)}, - 2 \cos{\left(t \right)}, 0\rangle \\ & =\left(- 2 \sin{\left(t \right)}\right)\cdot \left(- \sin{\left(t \right)}\right)+\left(- \cos{\left(t \right)}\right)\cdot \left(- 2 \cos{\left(t \right)}\right)+\left(0\right)\cdot \left(0\right) \\ & =\left(2 \sin^{2}{\left(t \right)}\right)+\left(2 \cos^{2}{\left(t \right)}\right)+\left(0\right) \\ & =2 \sin^{2}{\left(t \right)} + 2 \cos^{2}{\left(t \right)} \\ & =2\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{2 \pi} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(2\right)\,\mathrm dt \\ & =\left[\left(2 t\right)\right]_{0}^{2 \pi} \\ & =\left(\left(4 \pi\right)\right)-\left(\left(0\right)\right) \\ & =4 \pi\end{aligned}
$$

---

## Generated variant — moderate

observed family, authored bank and coefficient variation

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle - t^{2} + t, t^{3} - t^{2}, - 2 t^{2} + 2 t\rangle$ for $t\in [0,1).$
Given that $F(x,y,z)=\langle - 2 z, 0, - 3 y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $- \frac{5}{12}$

- $- \frac{1}{10}$ **(correct)**

- $\frac{1}{10}$

- $- \frac{1}{30}$

- $- \frac{1}{3}$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=- t^{2} + t,\quad y=t^{3} - t^{2},\quad z=- 2 t^{2} + 2 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - 2 z, 0, - 3 y\rangle \\ & =\langle - 2 \left(- 2 t^{2} + 2 t\right), 0, - 3 \left(t^{3} - t^{2}\right)\rangle \\ & =\langle 4 t^{2} - 4 t, 0, - 3 t^{3} + 3 t^{2}\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(- t^{2} + t\right), \frac{\mathrm d}{\mathrm dt}\left(t^{3} - t^{2}\right), \frac{\mathrm d}{\mathrm dt}\left(- 2 t^{2} + 2 t\right)\rangle \\ & =\langle 1 - 2 t, 3 t^{2} - 2 t, 2 - 4 t\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle 4 t^{2} - 4 t, 0, - 3 t^{3} + 3 t^{2}\rangle\cdot \langle 1 - 2 t, 3 t^{2} - 2 t, 2 - 4 t\rangle \\ & =\left(4 t^{2} - 4 t\right)\cdot \left(1 - 2 t\right)+\left(0\right)\cdot \left(3 t^{2} - 2 t\right)+\left(- 3 t^{3} + 3 t^{2}\right)\cdot \left(2 - 4 t\right) \\ & =\left(- 8 t^{3} + 12 t^{2} - 4 t\right)+\left(0\right)+\left(12 t^{4} - 18 t^{3} + 6 t^{2}\right) \\ & =12 t^{4} - 26 t^{3} + 18 t^{2} - 4 t \\ & =12 t^{4} - 26 t^{3} + 18 t^{2} - 4 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{0}^{1} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(12 t^{4} - 26 t^{3} + 18 t^{2} - 4 t\right)\,\mathrm dt \\ & =\left[\left(- \frac{13 t^{4}}{2}\right) + \left(- 2 t^{2}\right) + \left(\frac{12 t^{5}}{5}\right) + \left(6 t^{3}\right)\right]_{0}^{1} \\ & =\left(\left(- \frac{13}{2}\right) + \left(-2\right) + \left(\frac{12}{5}\right) + \left(6\right)\right)-\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right) \\ & =- \frac{1}{10}\end{aligned}
$$

---

## Generated variant — moderate

observed family, authored bank and coefficient variation

Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)=\langle 4 t^{3} - 4 t, 9 t^{2} + 9 t, 3 t^{3} - 3 t\rangle$ for $t\in [-1,0).$
Given that $F(x,y,z)=\langle - z, 0, - y\rangle,$ evaluate the integral

$$
\iint_S\operatorname{curl}F\cdot\mathrm{d}S.
$$

- $\frac{39}{10}$

- $\frac{3}{4}$

- $- \frac{9}{20}$ **(correct)**

- $\frac{61}{140}$

- $\frac{9}{20}$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

Along the curve $C,$ we have

$$
x=4 t^{3} - 4 t,\quad y=9 t^{2} + 9 t,\quad z=3 t^{3} - 3 t
$$

So,

$$
\begin{aligned}F(r(t)) & =\langle - z, 0, - y\rangle \\ & =\langle - \left(3 t^{3} - 3 t\right), 0, - \left(9 t^{2} + 9 t\right)\rangle \\ & =\langle - 3 t^{3} + 3 t, 0, - 9 t^{2} - 9 t\rangle\end{aligned}
$$

Computing $r\prime(t),$ we get

$$
\begin{aligned}r\prime(t) & =\langle \frac{\mathrm d}{\mathrm dt}\left(4 t^{3} - 4 t\right), \frac{\mathrm d}{\mathrm dt}\left(9 t^{2} + 9 t\right), \frac{\mathrm d}{\mathrm dt}\left(3 t^{3} - 3 t\right)\rangle \\ & =\langle 12 t^{2} - 4, 18 t + 9, 9 t^{2} - 3\rangle\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r\prime(t) & =\langle - 3 t^{3} + 3 t, 0, - 9 t^{2} - 9 t\rangle\cdot \langle 12 t^{2} - 4, 18 t + 9, 9 t^{2} - 3\rangle \\ & =\left(- 3 t^{3} + 3 t\right)\cdot \left(12 t^{2} - 4\right)+\left(0\right)\cdot \left(18 t + 9\right)+\left(- 9 t^{2} - 9 t\right)\cdot \left(9 t^{2} - 3\right) \\ & =\left(- 36 t^{5} + 48 t^{3} - 12 t\right)+\left(0\right)+\left(- 81 t^{4} - 81 t^{3} + 27 t^{2} + 27 t\right) \\ & =- 36 t^{5} - 81 t^{4} - 33 t^{3} + 27 t^{2} + 15 t \\ & =- 36 t^{5} - 81 t^{4} - 33 t^{3} + 27 t^{2} + 15 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\iint_S\operatorname{curl}F\cdot\mathrm dS & =\oint_C F\cdot\mathrm dr \\ & =\int_{-1}^{0} F(r(t))\cdot r\prime(t)\,\mathrm dt \\ & =\int_{-1}^{0}\left(- 36 t^{5} - 81 t^{4} - 33 t^{3} + 27 t^{2} + 15 t\right)\,\mathrm dt \\ & =\left[\left(- \frac{81 t^{5}}{5}\right) + \left(- 6 t^{6}\right) + \left(- \frac{33 t^{4}}{4}\right) + \left(\frac{15 t^{2}}{2}\right) + \left(9 t^{3}\right)\right]_{-1}^{0} \\ & =\left(\left(0\right) + \left(0\right) + \left(0\right) + \left(0\right) + \left(0\right)\right)-\left(\left(\frac{81}{5}\right) + \left(-6\right) + \left(- \frac{33}{4}\right) + \left(\frac{15}{2}\right) + \left(-9\right)\right) \\ & =- \frac{9}{20}\end{aligned}
$$
