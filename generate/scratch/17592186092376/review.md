Which of the following gives the length of the curve defined by the parametric equations
$x=5 \cos{\left(t \right)},\,y=7 t + \cos{\left(t \right)}$
from $t=-1$ to $t=1$?

- $\int_{-1}^{1}\sqrt{\sin^{2}{\left(t \right)} - 14 \sin{\left(t \right)} + 49}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{25 \sin^{2}{\left(t \right)} - 7 \sin{\left(t \right)} + 49}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{13 \sin^{2}{\left(t \right)} - 7 \sin{\left(t \right)} + \frac{49}{2}}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{26 \sin^{2}{\left(t \right)} - 14 \sin{\left(t \right)} + 49}\,\mathrm{d}t$ (correct)
- $\int_{-1}^{1}\sqrt{7 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} + 7}\,\mathrm{d}t$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\frac{\mathrm{d}x}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(5 \cos{\left(t \right)}\right)=- 5 \sin{\left(t \right)}
$$

and

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(7 t + \cos{\left(t \right)}\right)=7 - \sin{\left(t \right)}.
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L&=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{\left(- 5 \sin{\left(t \right)}\right)^2+\left(7 - \sin{\left(t \right)}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{25\sin^2(t)+49-14\sin(t)+\sin^2(t)}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{26 \sin^{2}{\left(t \right)} - 14 \sin{\left(t \right)} + 49}\,\mathrm{d}t.\end{aligned}
$$
