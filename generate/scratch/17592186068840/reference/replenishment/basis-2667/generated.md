Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2(x+7)}{3{y}^{2}}.$ Assume $x+7>0.$

- $y=C + \left(x + 7\right)^{2}$
- $y=\sqrt[3]{C + 2 x + 14}$
- $y=C + \left|{x + 7}\right|^{\frac{2}{3}}$
- $y=\sqrt[3]{C - \left(x + 7\right)^{2}}$
- $y=\sqrt[3]{C + \left(x + 7\right)^{2}}$ (correct)

To find the general solution, we first separate the variables:

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2(x+7)}{3{y}^{2}} \\ 3{y}^{2}\,\frac{\text{d}y}{\text{d}x} & =2(x+7)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int 3{y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2(x+7)\,\text{d}x \\ \int 3{y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2(x+7)\,\text{d}x \\ \int 3{y}^{2}\,\text{d}y & =\int 2(x+7)\,\text{d}x \\ {y}^{3} & ={(x+7)}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={(x+7)}^{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\sqrt[3]{{(x+7)}^{2}+C}.
$$

Use the real cube root, on intervals where $y\ne 0.$

---

Find the general solution to the differential equation $y′=\frac{5 \left(x - 4\right)^{3}}{y}.$ Assume $x-4>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=C + \frac{\sqrt{10} \left(x - 4\right)^{2}}{2}$
- $y=\pm \sqrt{C + \frac{5 \left(x - 4\right)^{4}}{2}}$ (correct)
- $y=\pm \sqrt{C - \frac{5 \left(x - 4\right)^{4}}{2}}$
- $y=C + \frac{5 \left(x - 4\right)^{4}}{4}$
- $y=\pm \sqrt{C + 10 \left(x - 4\right)^{3}}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{5 \left(x - 4\right)^{3}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =5 \left(x - 4\right)^{3}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 5 \left(x - 4\right)^{3}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int 5 \left(x - 4\right)^{3}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{5 \left(x - 4\right)^{4}}{4}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{5 \left(x - 4\right)^{4}}{4}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\frac{5 \left(x - 4\right)^{4}}{2}+2C \\ y & =\pm\sqrt{\frac{5 \left(x - 4\right)^{4}}{2}+2C} \\ y & =\pm\sqrt{\frac{5 \left(x - 4\right)^{4}}{2}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

---

Find the general solution to the differential equation $y′=- e^{- 2 x - y}.$ Work on intervals where the logarithm argument is positive.

- $y=C + \frac{e^{- 2 x}}{2}$
- $y=\ln{\left(C + \frac{e^{- 2 x}}{2} \right)}$ (correct)
- $y=C + \ln{\left(\frac{e^{- 2 x}}{2} \right)}$
- $y=\ln{\left(C - e^{- 2 x} \right)}$
- $y=\ln{\left(C - \frac{e^{- 2 x}}{2} \right)}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =- e^{- 2 x - y} \\ e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x} & =- e^{- 2 x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int - e^{- 2 x}\,\mathrm{d}x \\ \int e^{y}\,\mathrm{d}y & =\int - e^{- 2 x}\,\mathrm{d}x \\ e^{y} & =\frac{e^{- 2 x}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
e^{y}=\frac{e^{- 2 x}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\ln{\left(C + \frac{e^{- 2 x}}{2} \right)}.
$$

The logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.

---

Find the general solution to the differential equation $y′=\frac{4 \left(x - 3\right)^{2}}{y}.$ Assume $x-3>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=\pm \sqrt{C + 8 \left(x - 3\right)^{2}}$
- $y=C + \frac{4 \left(x - 3\right)^{3}}{3}$
- $y=\pm \sqrt{C - \frac{8 \left(x - 3\right)^{3}}{3}}$
- $y=\pm \sqrt{C + \frac{8 \left(x - 3\right)^{3}}{3}}$ (correct)
- $y=C + \frac{2 \sqrt{6} \sqrt{\left(x - 3\right)^{3}}}{3}$

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{4 \left(x - 3\right)^{2}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =4 \left(x - 3\right)^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 4 \left(x - 3\right)^{2}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int 4 \left(x - 3\right)^{2}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{4 \left(x - 3\right)^{3}}{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{4 \left(x - 3\right)^{3}}{3}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\frac{8 \left(x - 3\right)^{3}}{3}+2C \\ y & =\pm\sqrt{\frac{8 \left(x - 3\right)^{3}}{3}+2C} \\ y & =\pm\sqrt{\frac{8 \left(x - 3\right)^{3}}{3}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

---

Find the general solution to the differential equation $y′=\frac{2 \left(x + 4\right)^{3}}{y}.$ Assume $x+4>0.$ Take both sign branches on intervals where the radicand is positive and $y\ne 0.$

- $y=C + \left(x + 4\right)^{2}$
- $y=\pm \sqrt{C + 4 \left(x + 4\right)^{3}}$
- $y=\pm \sqrt{C - \left(x + 4\right)^{4}}$
- $y=C + \frac{\left(x + 4\right)^{4}}{2}$
- $y=\pm \sqrt{C + \left(x + 4\right)^{4}}$ (correct)

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =\frac{2 \left(x + 4\right)^{3}}{y} \\ y\,\frac{\mathrm{d}y}{\mathrm{d}x} & =2 \left(x + 4\right)^{3}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int y\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int 2 \left(x + 4\right)^{3}\,\mathrm{d}x \\ \int y\,\mathrm{d}y & =\int 2 \left(x + 4\right)^{3}\,\mathrm{d}x \\ \frac{y^{2}}{2} & =\frac{\left(x + 4\right)^{4}}{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\frac{y^{2}}{2}=\frac{\left(x + 4\right)^{4}}{2}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
\begin{aligned}y^2 & =\left(x + 4\right)^{4}+2C \\ y & =\pm\sqrt{\left(x + 4\right)^{4}+2C} \\ y & =\pm\sqrt{\left(x + 4\right)^{4}+K}\end{aligned}
$$

where $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.

---

Find the general solution to the differential equation $y′=- 4 e^{- 2 x - y}.$ Work on intervals where the logarithm argument is positive.

- $y=C + 2 e^{- 2 x}$
- $y=\ln{\left(C - 2 e^{- 2 x} \right)}$
- $y=C + \ln{\left(2 e^{- 2 x} \right)}$
- $y=\ln{\left(C - 4 e^{- 2 x} \right)}$
- $y=\ln{\left(C + 2 e^{- 2 x} \right)}$ (correct)

To find the general solution, we first separate the variables:

$$
\begin{aligned}y′ & =- 4 e^{- 2 x - y} \\ e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x} & =- 4 e^{- 2 x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int e^{y}\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x & =\int - 4 e^{- 2 x}\,\mathrm{d}x \\ \int e^{y}\,\mathrm{d}y & =\int - 4 e^{- 2 x}\,\mathrm{d}x \\ e^{y} & =2 e^{- 2 x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
e^{y}=2 e^{- 2 x}+C.
$$

We're required to write the solution in the form $y=y(x).$ By doing this, we get

$$
y=\ln{\left(C + 2 e^{- 2 x} \right)}.
$$

The logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.