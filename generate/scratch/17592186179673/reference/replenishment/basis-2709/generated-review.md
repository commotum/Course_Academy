## easy 73913116-384d-502d-a4e5-8830e55db474

Which of the following is equivalent to $\int_C\left(- 3 x^{2}\right)\,\mathrm{d}x+\left(- x y\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,1)$.

- $\int_{0}^{\frac{\pi}{2}}\left(- 84 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\frac{\pi}{2}}\left(78 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$ (correct)
- $\int_{0}^{\frac{\pi}{2}}\left(81 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\frac{\pi}{2}}\left(- 3 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 81 \cos^{3}{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\frac{\pi}{2}}\left(- 3 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

Therefore, we can write our line integral as follows:

$$
\begin{aligned}\int_C\left(- 3 x^{2}\right)\,\mathrm{d}x+\left(- x y\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 3 x^{2}\right)x\prime(t)\,\mathrm{d}t+\left(- x y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 3 x^{2}\right)x\prime(t)+\left(- x y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 27 \cos^{2}{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(- 3 \sin{\left(t \right)} \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(81 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 3 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(78 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm{d}t\end{aligned}
$$

## moderate b8886af2-15c3-5d9c-8be1-602af41bdf96

Evaluate $\int_C\left(- 4 x + y\right)\,\mathrm{d}x+\left(- x + 3 y\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,1)$.

- $- \frac{33}{2}$
- $\frac{39}{2} - \frac{3 \pi}{2}$ (correct)
- $18 - \frac{3 \pi}{4}$
- $- \frac{33 \pi}{4}$
- $\frac{3}{2} - \frac{3 \pi}{4}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- 4 x + y\right)\,\mathrm{d}x+\left(- x + 3 y\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 4 x + y\right)x\prime(t)\,\mathrm{d}t+\left(- x + 3 y\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 4 x + y\right)x\prime(t)+\left(- x + 3 y\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(\sin{\left(t \right)} - 12 \cos{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} - 3 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(36 \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(- 3 \sin^{2}{\left(t \right)}\right)+\left(- 3 \cos^{2}{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(39 \sin{\left(t \right)} \cos{\left(t \right)} - 3\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\frac{39 \sin{\left(2 t \right)}}{2} - 3\right)\,\mathrm{d}t\\ & =\left[- 3 t + \frac{39 \sin^{2}{\left(t \right)}}{2}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(- 3 \left(\frac{\pi}{2}\right) + \frac{39 \sin^{2}{\left(\left(\frac{\pi}{2}\right) \right)}}{2}\right)-\left(- 3 \left(0\right) + \frac{39 \sin^{2}{\left(\left(0\right) \right)}}{2}\right)\\ & =\left(\left(- \frac{3 \pi}{2}\right)+\left(\frac{39}{2}\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =\frac{39}{2} - \frac{3 \pi}{2}\end{aligned}
$$

## hard 0faff4ca-cb6c-5f59-80aa-48ecec1fa2a8

Evaluate $\int_C\left(- 4 x^{2} y + y\right)\,\mathrm{d}x+\left(3 x y^{2} - x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,1)$.

- $- \frac{99 \pi}{16}$
- $\frac{93 \pi}{16}$ (correct)
- $6 \pi$
- $- \frac{99}{4}$
- $- \frac{3 \pi}{16}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- 4 x^{2} y + y\right)\,\mathrm{d}x+\left(3 x y^{2} - x\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 4 x^{2} y + y\right)x\prime(t)\,\mathrm{d}t+\left(3 x y^{2} - x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 4 x^{2} y + y\right)x\prime(t)+\left(3 x y^{2} - x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 36 \sin{\left(t \right)} \cos^{2}{\left(t \right)} + \sin{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(9 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 3 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(108 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 3 \sin^{2}{\left(t \right)}\right)+\left(- 3 \cos^{2}{\left(t \right)}\right)+\left(9 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(117 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} - 3\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\frac{93}{8} - \frac{117 \cos{\left(4 t \right)}}{8}\right)\,\mathrm{d}t\\ & =\left[\frac{93 t}{8} - \frac{117 \sin{\left(4 t \right)}}{32}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(\frac{93 \left(\frac{\pi}{2}\right)}{8} - \frac{117 \sin{\left(4 \left(\frac{\pi}{2}\right) \right)}}{32}\right)-\left(\frac{93 \left(0\right)}{8} - \frac{117 \sin{\left(4 \left(0\right) \right)}}{32}\right)\\ & =\left(\left(0\right)+\left(\frac{93 \pi}{16}\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =\frac{93 \pi}{16}\end{aligned}
$$

## hard 03ef4d10-8b30-5c10-920c-534b995f0855

Evaluate $\int_C\left(4 x^{2} y - 2 y\right)\,\mathrm{d}x+\left(3 x y^{2} + 2 x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $9 x^{2} + 16 y^{2}=144$ traversed in the counterclockwise direction from the point $(4,0)$ to the point $(-4,0)$.

- $\frac{105 \pi}{2}$
- $- \frac{63 \pi}{2}$ (correct)
- $0$
- $- 84 \pi$
- $\frac{273 \pi}{2}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $4$ and $3,$ respectively, it can be parametrized as follows:

$$r(t)=4 \cos{\left(t \right)}\,i+3 \sin{\left(t \right)}\,j,\quad t\in[0,\pi].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 4 \sin{\left(t \right)}\,i+3 \cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(4 x^{2} y - 2 y\right)\,\mathrm{d}x+\left(3 x y^{2} + 2 x\right)\,\mathrm{d}y & =\int_{0}^{\pi}\left(4 x^{2} y - 2 y\right)x\prime(t)\,\mathrm{d}t+\left(3 x y^{2} + 2 x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(4 x^{2} y - 2 y\right)x\prime(t)+\left(3 x y^{2} + 2 x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(192 \sin{\left(t \right)} \cos^{2}{\left(t \right)} - 6 \sin{\left(t \right)}\right)\left(- 4 \sin{\left(t \right)}\right)+\left(108 \sin^{2}{\left(t \right)} \cos{\left(t \right)} + 8 \cos{\left(t \right)}\right)\left(3 \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\left(- 768 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(24 \sin^{2}{\left(t \right)}\right)+\left(24 \cos^{2}{\left(t \right)}\right)+\left(324 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(- 444 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} + 24\right)\,\mathrm{d}t\\ & =\int_{0}^{\pi}\left(\frac{111 \cos{\left(4 t \right)}}{2} - \frac{63}{2}\right)\,\mathrm{d}t\\ & =\left[- \frac{63 t}{2} + \frac{111 \sin{\left(4 t \right)}}{8}\right]_{0}^{\pi}\\ & =\left(- \frac{63 \left(\pi\right)}{2} + \frac{111 \sin{\left(4 \left(\pi\right) \right)}}{8}\right)-\left(- \frac{63 \left(0\right)}{2} + \frac{111 \sin{\left(4 \left(0\right) \right)}}{8}\right)\\ & =\left(\left(- \frac{63 \pi}{2}\right)+\left(0\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =- \frac{63 \pi}{2}\end{aligned}
$$

## hard b760d270-0b52-5110-b068-ec2545a8607e

Evaluate $\int_C\left(- 2 x^{2} y + y\right)\,\mathrm{d}x+\left(- x y^{2} - x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $x^{2} + 9 y^{2}=9$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,1)$.

- $- \frac{57 \pi}{16}$
- $\frac{21 \pi}{8}$
- $- \frac{57}{4}$
- $- \frac{15 \pi}{16}$
- $\frac{27 \pi}{16}$ (correct)

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $1,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+\sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+\cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- 2 x^{2} y + y\right)\,\mathrm{d}x+\left(- x y^{2} - x\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 2 x^{2} y + y\right)x\prime(t)\,\mathrm{d}t+\left(- x y^{2} - x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 2 x^{2} y + y\right)x\prime(t)+\left(- x y^{2} - x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 18 \sin{\left(t \right)} \cos^{2}{\left(t \right)} + \sin{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(- 3 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 3 \cos{\left(t \right)}\right)\left(\cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(54 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 3 \sin^{2}{\left(t \right)}\right)+\left(- 3 \cos^{2}{\left(t \right)}\right)+\left(- 3 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(51 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} - 3\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\frac{27}{8} - \frac{51 \cos{\left(4 t \right)}}{8}\right)\,\mathrm{d}t\\ & =\left[\frac{27 t}{8} - \frac{51 \sin{\left(4 t \right)}}{32}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(\frac{27 \left(\frac{\pi}{2}\right)}{8} - \frac{51 \sin{\left(4 \left(\frac{\pi}{2}\right) \right)}}{32}\right)-\left(\frac{27 \left(0\right)}{8} - \frac{51 \sin{\left(4 \left(0\right) \right)}}{32}\right)\\ & =\left(\left(0\right)+\left(\frac{27 \pi}{16}\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =\frac{27 \pi}{16}\end{aligned}
$$

## hard 9be25acc-1ec0-58da-aef8-6711e4d01192

Evaluate $\int_C\left(- 2 x^{2} y + 4 y\right)\,\mathrm{d}x+\left(- 2 x y^{2} - 4 x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $9 x^{2} + 4 y^{2}=36$ traversed in the counterclockwise direction from the point $(2,0)$ to the point $(0,3)$.

- $-39$
- $- \frac{39 \pi}{4}$
- $- \frac{63 \pi}{4}$ (correct)
- $- 3 \pi$
- $- \frac{51 \pi}{4}$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $2$ and $3,$ respectively, it can be parametrized as follows:

$$r(t)=2 \cos{\left(t \right)}\,i+3 \sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 2 \sin{\left(t \right)}\,i+3 \cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- 2 x^{2} y + 4 y\right)\,\mathrm{d}x+\left(- 2 x y^{2} - 4 x\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 2 x^{2} y + 4 y\right)x\prime(t)\,\mathrm{d}t+\left(- 2 x y^{2} - 4 x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 2 x^{2} y + 4 y\right)x\prime(t)+\left(- 2 x y^{2} - 4 x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 24 \sin{\left(t \right)} \cos^{2}{\left(t \right)} + 12 \sin{\left(t \right)}\right)\left(- 2 \sin{\left(t \right)}\right)+\left(- 36 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 8 \cos{\left(t \right)}\right)\left(3 \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(48 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 24 \sin^{2}{\left(t \right)}\right)+\left(- 24 \cos^{2}{\left(t \right)}\right)+\left(- 108 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(- 60 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} - 24\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\frac{15 \cos{\left(4 t \right)}}{2} - \frac{63}{2}\right)\,\mathrm{d}t\\ & =\left[- \frac{63 t}{2} + \frac{15 \sin{\left(4 t \right)}}{8}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(- \frac{63 \left(\frac{\pi}{2}\right)}{2} + \frac{15 \sin{\left(4 \left(\frac{\pi}{2}\right) \right)}}{8}\right)-\left(- \frac{63 \left(0\right)}{2} + \frac{15 \sin{\left(4 \left(0\right) \right)}}{8}\right)\\ & =\left(\left(- \frac{63 \pi}{4}\right)+\left(0\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =- \frac{63 \pi}{4}\end{aligned}
$$

## hard 8739eb28-3666-500d-b030-f6ce2af45845

Evaluate $\int_C\left(- 4 x^{2} y + y\right)\,\mathrm{d}x+\left(- 3 x y^{2} - x\right)\,\mathrm{d}y,$ where $C$ is part of the ellipse $16 x^{2} + 9 y^{2}=144$ traversed in the counterclockwise direction from the point $(3,0)$ to the point $(0,4)$.

- $-252$
- $- 39 \pi$
- $- 15 \pi$ (correct)
- $- 63 \pi$
- $24 \pi$

Since $C$ is an ellipse centered at $O$ with horizontal and vertical semiaxes of $3$ and $4,$ respectively, it can be parametrized as follows:

$$r(t)=3 \cos{\left(t \right)}\,i+4 \sin{\left(t \right)}\,j,\quad t\in[0,\frac{\pi}{2}].$$

The derivative of $r(t)$ is given by

$$r\prime(t)=- 3 \sin{\left(t \right)}\,i+4 \cos{\left(t \right)}\,j.$$

We can now evaluate the line integral:

$$
\begin{aligned}\int_C\left(- 4 x^{2} y + y\right)\,\mathrm{d}x+\left(- 3 x y^{2} - x\right)\,\mathrm{d}y & =\int_{0}^{\frac{\pi}{2}}\left(- 4 x^{2} y + y\right)x\prime(t)\,\mathrm{d}t+\left(- 3 x y^{2} - x\right)y\prime(t)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 4 x^{2} y + y\right)x\prime(t)+\left(- 3 x y^{2} - x\right)y\prime(t)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(- 144 \sin{\left(t \right)} \cos^{2}{\left(t \right)} + 4 \sin{\left(t \right)}\right)\left(- 3 \sin{\left(t \right)}\right)+\left(- 144 \sin^{2}{\left(t \right)} \cos{\left(t \right)} - 3 \cos{\left(t \right)}\right)\left(4 \cos{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(\left(432 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)+\left(- 12 \sin^{2}{\left(t \right)}\right)+\left(- 12 \cos^{2}{\left(t \right)}\right)+\left(- 576 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)}\right)\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(- 144 \sin^{2}{\left(t \right)} \cos^{2}{\left(t \right)} - 12\right)\,\mathrm{d}t\\ & =\int_{0}^{\frac{\pi}{2}}\left(18 \cos{\left(4 t \right)} - 30\right)\,\mathrm{d}t\\ & =\left[- 30 t + \frac{9 \sin{\left(4 t \right)}}{2}\right]_{0}^{\frac{\pi}{2}}\\ & =\left(- 30 \left(\frac{\pi}{2}\right) + \frac{9 \sin{\left(4 \left(\frac{\pi}{2}\right) \right)}}{2}\right)-\left(- 30 \left(0\right) + \frac{9 \sin{\left(4 \left(0\right) \right)}}{2}\right)\\ & =\left(\left(- 15 \pi\right)+\left(0\right)\right)-\left(\left(0\right)+\left(0\right)\right)\\ & =- 15 \pi\end{aligned}
$$
