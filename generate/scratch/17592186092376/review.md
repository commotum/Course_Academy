# Original and variant review

## q-15163

### Source

Which of the following gives the length of the curve defined by the parametric equations
$x=t+2\operatorname{sin}⁡(t),\,y=1+\operatorname{cos}⁡(2t)$
from $t=2$ to $t=5$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(t+2\operatorname{sin}⁡(t))=1+2\operatorname{cos}⁡(t)\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(1+\operatorname{cos}⁡(2t))=-2\operatorname{sin}⁡(2t).\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{2}^{5}\sqrt{(1+2\operatorname{cos}⁡(t))^{2}+(-2\operatorname{sin}⁡(2t))^{2}}\,\text{d}t \\  & ={\int }_{2}^{5}\sqrt{1+4\operatorname{cos}⁡(t)+4{cos}^{2}⁡(t)+4{sin}^{2}⁡(2t)}\,\text{d}t\,.\end{aligned}
$$

### Normal replay at original parameters

Which of the following gives the length of the curve defined by the parametric equations
$x=t + 2 \sin{\left(t \right)},\,y=\cos{\left(2 t \right)} + 1$
from $t=2$ to $t=5$?

- $\int_{2}^{5}\sqrt{4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(t \right)} + 4 \cos{\left(t \right)} + 1}\,\mathrm{d}t$ (correct)
- $\int_{2}^{5}\sqrt{4 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(t \right)} + 2 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(t \right)} + 8 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{4 \sin^{2}{\left(2 t \right)} + 2 \cos^{2}{\left(t \right)} + 2 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{16 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(t \right)} + 4 \cos{\left(t \right)} + 1}\,\mathrm{d}t$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\frac{\mathrm{d}x}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(t + 2 \sin{\left(t \right)}\right)=2 \cos{\left(t \right)} + 1
$$

and

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(\cos{\left(2 t \right)} + 1\right)=- 2 \sin{\left(2 t \right)}.
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L&=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t \\ &=\int_{2}^{5}\sqrt{\left(2 \cos{\left(t \right)} + 1\right)^2+\left(- 2 \sin{\left(2 t \right)}\right)^2}\,\mathrm{d}t \\ &=\int_{2}^{5}\sqrt{4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(t \right)} + 4 \cos{\left(t \right)} + 1}\,\mathrm{d}t.\end{aligned}
$$

### Changed coefficients

Which of the following gives the length of the curve defined by the parametric equations
$x=t + 3 \sin{\left(t \right)},\,y=\cos{\left(4 t \right)} + 1$
from $t=2$ to $t=5$?

- $\int_{2}^{5}\sqrt{16 \sin^{2}{\left(4 t \right)} + 9 \cos^{2}{\left(t \right)} + 6 \cos{\left(t \right)} + 1}\,\mathrm{d}t$ (correct)
- $\int_{2}^{5}\sqrt{16 \sin^{2}{\left(4 t \right)} + 36 \cos^{2}{\left(t \right)} + 3 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{64 \sin^{2}{\left(4 t \right)} + 36 \cos^{2}{\left(t \right)} + 12 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{16 \sin^{2}{\left(4 t \right)} + 3 \cos^{2}{\left(t \right)} + 3 \cos{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{64 \sin^{2}{\left(4 t \right)} + 9 \cos^{2}{\left(t \right)} + 6 \cos{\left(t \right)} + 1}\,\mathrm{d}t$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\frac{\mathrm{d}x}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(t + 3 \sin{\left(t \right)}\right)=3 \cos{\left(t \right)} + 1
$$

and

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(\cos{\left(4 t \right)} + 1\right)=- 4 \sin{\left(4 t \right)}.
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L&=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t \\ &=\int_{2}^{5}\sqrt{\left(3 \cos{\left(t \right)} + 1\right)^2+\left(- 4 \sin{\left(4 t \right)}\right)^2}\,\mathrm{d}t \\ &=\int_{2}^{5}\sqrt{16 \sin^{2}{\left(4 t \right)} + 9 \cos^{2}{\left(t \right)} + 6 \cos{\left(t \right)} + 1}\,\mathrm{d}t.\end{aligned}
$$

## q-123027

### Source

Which of the following gives the length of the curve defined by the parametric equations
$x=3\operatorname{cos}⁡t,\,y=8t+\operatorname{cos}⁡t$
from $t=-1$ to $t=1$ ?

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t)=-3\operatorname{sin}⁡t\end{aligned}
$$

and

$$
\begin{aligned}\frac{\text{d}y}{\text{d}t} & =\frac{\text{d}}{\text{d}t}(8t+\operatorname{cos}⁡t)=8-\operatorname{sin}⁡t.\end{aligned}
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L & ={\int }_{{t}_{1}}^{{t}_{2}}\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}\,\text{d}t \\  & ={\int }_{-1}^{1}\sqrt{{(-3\operatorname{sin}⁡t)}^{2}+{(8-\operatorname{sin}⁡t)}^{2}}\,\text{d}t \\  & ={\int }_{-1}^{1}\sqrt{9{sin}^{2}⁡t+64-16\operatorname{sin}⁡t+{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{-1}^{1}\sqrt{10{sin}^{2}⁡t-16\operatorname{sin}⁡t+64}\,\text{d}t\,.\end{aligned}
$$

### Normal replay at original parameters

Which of the following gives the length of the curve defined by the parametric equations
$x=3 \cos{\left(t \right)},\,y=8 t + \cos{\left(t \right)}$
from $t=-1$ to $t=1$?

- $\int_{-1}^{1}\sqrt{\sin^{2}{\left(t \right)} - 16 \sin{\left(t \right)} + 64}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{9 \sin^{2}{\left(t \right)} - 8 \sin{\left(t \right)} + 64}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{5 \sin^{2}{\left(t \right)} - 8 \sin{\left(t \right)} + 32}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{10 \sin^{2}{\left(t \right)} - 16 \sin{\left(t \right)} + 64}\,\mathrm{d}t$ (correct)
- $\int_{-1}^{1}\sqrt{8 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} + 8}\,\mathrm{d}t$

To compute the arc length $L$ of a parametrically defined curve, we use the formula

$$
L=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t.
$$

Computing the derivatives of $x$ and $y,$ we have

$$
\frac{\mathrm{d}x}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(3 \cos{\left(t \right)}\right)=- 3 \sin{\left(t \right)}
$$

and

$$
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(8 t + \cos{\left(t \right)}\right)=8 - \sin{\left(t \right)}.
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L&=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{\left(- 3 \sin{\left(t \right)}\right)^2+\left(8 - \sin{\left(t \right)}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{9\sin^2(t)+64-16\sin(t)+\sin^2(t)}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{10 \sin^{2}{\left(t \right)} - 16 \sin{\left(t \right)} + 64}\,\mathrm{d}t.\end{aligned}
$$

### Changed coefficients

Which of the following gives the length of the curve defined by the parametric equations
$x=5 \cos{\left(t \right)},\,y=9 t + \cos{\left(t \right)}$
from $t=-1$ to $t=1$?

- $\int_{-1}^{1}\sqrt{\sin^{2}{\left(t \right)} - 18 \sin{\left(t \right)} + 81}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{25 \sin^{2}{\left(t \right)} - 9 \sin{\left(t \right)} + 81}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{13 \sin^{2}{\left(t \right)} - 9 \sin{\left(t \right)} + \frac{81}{2}}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{26 \sin^{2}{\left(t \right)} - 18 \sin{\left(t \right)} + 81}\,\mathrm{d}t$ (correct)
- $\int_{-1}^{1}\sqrt{9 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} + 9}\,\mathrm{d}t$

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
\frac{\mathrm{d}y}{\mathrm{d}t}=\frac{\mathrm{d}}{\mathrm{d}t}\left(9 t + \cos{\left(t \right)}\right)=9 - \sin{\left(t \right)}.
$$

We substitute these derivatives in the formula for arc length, and we get

$$
\begin{aligned}L&=\int_{t_1}^{t_2}\sqrt{\left(\frac{\mathrm{d}x}{\mathrm{d}t}\right)^2+\left(\frac{\mathrm{d}y}{\mathrm{d}t}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{\left(- 5 \sin{\left(t \right)}\right)^2+\left(9 - \sin{\left(t \right)}\right)^2}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{25\sin^2(t)+81-18\sin(t)+\sin^2(t)}\,\mathrm{d}t \\ &=\int_{-1}^{1}\sqrt{26 \sin^{2}{\left(t \right)} - 18 \sin{\left(t \right)} + 81}\,\mathrm{d}t.\end{aligned}
$$
