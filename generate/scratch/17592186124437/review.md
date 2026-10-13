# Originals and generated variants

Raw original replays preserve captured omissions and are evidence-only. Supported originals infer only q-36463 missing fields. Changed observed banks are opaque pattern continuations; normal examples use authored method-derived complete banks. Moderate and hard are explicitly authored missing-level workloads. Correct refs are author review data.

## 1. linear — observed_raw

Source q-36216; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "6", "x": "2", "y": "3", "z": "9"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P(2,3,9)$ lies on $C$, and that ${f}_{x}=6x-y$, find the slope of the tangent to $C$ at $P.$

- $9$
- $12$
- $-3$
- $-1$
- $1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(2,3,9)$ will be given by the partial derivative ${f}_{x}(2,3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(2,3):$

$$
\begin{aligned}{f}_{x}(2,3) & =6(2)-(3)=9\end{aligned}
$$

## 2. linear — observed_supported

Source q-36216; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "6", "x": "2", "y": "3", "z": "9"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P(2,3,9)$ lies on $C$, and that ${f}_{x}=6x-y$, find the slope of the tangent to $C$ at $P.$

- $9$
- $12$
- $-3$
- $-1$
- $1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(2,3,9)$ will be given by the partial derivative ${f}_{x}(2,3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(2,3):$

$$
\begin{aligned}{f}_{x}(2,3) & =6(2)-(3)=9\end{aligned}
$$

## 3. linear — observed_raw

Source q-36216; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "5", "x": "-3", "y": "3", "z": "-4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P(-3,3,-4)$ lies on $C$, and that ${f}_{x}=5x-y$, find the slope of the tangent to $C$ at $P.$

- $-18$
- $-3$
- $-4$
- $4$
- $-15$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-3,3,-4)$ will be given by the partial derivative ${f}_{x}(-3,3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-3,3):$

$$
\begin{aligned}{f}_{x}(-3,3) & =5(-3)-(3)=-18\end{aligned}
$$

## 4. linear — observed_raw

Source q-36216; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "5", "x": "-2", "y": "-2", "z": "-3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-2.$ Given that the point $P(-2,-2,-3)$ lies on $C$, and that ${f}_{x}=5x-y$, find the slope of the tangent to $C$ at $P.$

- $-8$
- $-3$
- $-10$
- $2$
- $3$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-2,-2,-3)$ will be given by the partial derivative ${f}_{x}(-2,-2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-2,-2):$

$$
\begin{aligned}{f}_{x}(-2,-2) & =5(-2)-(-2)=-8\end{aligned}
$$

## 5. cos_sum — observed_raw

Source q-36463; origin observed-mask; difficulty absent in source; evidence only True. Parameters `{"x": "pi/2", "y": "0"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = 0$. Given that the point $P$ with $x$-coordinate $\frac{π}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $2$
- $π$
- $1$
- $0$
- $\frac{π}{2}$

[Raw source has no worked solution.]

## 6. cos_sum — observed_supported

Source q-36463; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "pi/2", "y": "0"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = 0$. Given that the point $P$ with $x$-coordinate $\frac{π}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $2$
- $π$
- $1$
- $0$
- $\frac{π}{2}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=0.$ Hence, the slope of the tangent to the curve $C$ at the point $P(\frac{π}{2},0,0)$ will be given by the partial derivative ${f}_{x}(\frac{π}{2},0).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(\frac{π}{2},0):$

$$
\begin{aligned}{f}_{x}(\frac{π}{2},0) & =(0)\cos (\frac{π}{2})+\cos (0) \\  & =1\end{aligned}
$$

## 7. cos_sum — observed_raw

Source q-36463; origin observed-mask; difficulty absent in source; evidence only True. Parameters `{"x": "pi/2", "y": "0"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = 0$. Given that the point $P$ with $x$-coordinate $\frac{π}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $\frac{π}{2}$
- $π$
- $2$
- $0$
- $1$

[Raw source has no worked solution.]

## 8. cos_sum — observed_raw

Source q-36463; origin observed-mask; difficulty absent in source; evidence only True. Parameters `{"x": "-pi/2", "y": "pi"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = \pi$. Given that the point $P$ with $x$-coordinate $- \frac{\pi}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $0$
- $-1$
- $2$
- $- π$
- $- \frac{π}{2}$

[Raw source has no worked solution.]

## 9. sin_product — observed_raw

Source q-132579; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-pi/2", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P$ with $x$-coordinate $-\frac{\pi }{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $-\pi $
- $1+2\pi $
- $-1-\pi $
- $\pi -1$
- $2-\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-\frac{\pi }{2}$ will be given by the partial derivative ${f}_{x}(-\frac{\pi }{2},2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-\frac{\pi }{2},2):$

$$
\begin{aligned}{f}_{x}(-\frac{\pi }{2},2) & =\operatorname{sin}⁡(-\frac{\pi }{2})+(-\frac{\pi }{2})\cdot 2 \\  & =-1-\pi \end{aligned}
$$

## 10. sin_product — observed_supported

Source q-132579; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-pi/2", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P$ with $x$-coordinate $-\frac{\pi }{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $-\pi $
- $1+2\pi $
- $-1-\pi $
- $\pi -1$
- $2-\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-\frac{\pi }{2}$ will be given by the partial derivative ${f}_{x}(-\frac{\pi }{2},2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-\frac{\pi }{2},2):$

$$
\begin{aligned}{f}_{x}(-\frac{\pi }{2},2) & =\operatorname{sin}⁡(-\frac{\pi }{2})+(-\frac{\pi }{2})\cdot 2 \\  & =-1-\pi \end{aligned}
$$

## 11. sin_product — observed_raw

Source q-132579; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "pi/2", "y": "-4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-4.$ Given that the point $P$ with $x$-coordinate $\frac{\pi}{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $-4-2\pi $
- $-1+4\pi $
- $-2\pi $
- $2\pi +1$
- $1-2\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-4.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=\frac{\pi}{2}$ will be given by the partial derivative ${f}_{x}(\frac{\pi}{2},-4).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(\frac{\pi}{2},-4):$

$$
\begin{aligned}{f}_{x}(\frac{\pi}{2},-4) & =\operatorname{sin}⁡(\frac{\pi }{2})+(\frac{\pi }{2})\cdot -4 \\  & =1-2 \pi\end{aligned}
$$

## 12. sin_product — observed_raw

Source q-132579; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-pi/2", "y": "-2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-2.$ Given that the point $P$ with $x$-coordinate $-\frac{\pi }{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $-\pi -1$
- $-1+\pi $
- $\pi $
- $1-2\pi $
- $-2+\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-\frac{\pi }{2}$ will be given by the partial derivative ${f}_{x}(-\frac{\pi }{2},-2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-\frac{\pi }{2},-2):$

$$
\begin{aligned}{f}_{x}(-\frac{\pi }{2},-2) & =\operatorname{sin}⁡(-\frac{\pi }{2})+(-\frac{\pi }{2})\cdot -2 \\  & =-1+\pi\end{aligned}
$$

## 13. rational_radical — observed_raw

Source q-132584; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "-3", "z": "8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-3.$ Given that the point $P(1,-3,8)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $\frac{2}{3}$
- $\frac{15}{6}$
- $-\frac{25}{9}$
- $-\frac{16}{9}$
- $-\frac{7}{3}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,-3,8)$ will be given by the partial derivative ${f}_{x}(1,-3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,-3):$

$$
\begin{aligned}{f}_{x}(1,-3) & =\frac{{1}^{2}+1}{{1}^{2}(-3)^{2}}+(-3)\sqrt{1} \\  & =\frac{2}{9}-3(1) \\  & =-\frac{25}{9}\end{aligned}
$$

## 14. rational_radical — observed_supported

Source q-132584; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "-3", "z": "8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-3.$ Given that the point $P(1,-3,8)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $\frac{2}{3}$
- $\frac{15}{6}$
- $-\frac{25}{9}$
- $-\frac{16}{9}$
- $-\frac{7}{3}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,-3,8)$ will be given by the partial derivative ${f}_{x}(1,-3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,-3):$

$$
\begin{aligned}{f}_{x}(1,-3) & =\frac{{1}^{2}+1}{{1}^{2}(-3)^{2}}+(-3)\sqrt{1} \\  & =\frac{2}{9}-3(1) \\  & =-\frac{25}{9}\end{aligned}
$$

## 15. rational_radical — observed_raw

Source q-132584; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "4", "y": "-4", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-4.$ Given that the point $P(4,-4,-8)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $\frac{20}{6}$
- $-\frac{77}{48}$
- $\frac{1}{2}$
- $-\frac{15}{4}$
- $-\frac{2031}{256}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-4.$ Hence, the slope of the tangent to the curve $C$ at the point $P(4,-4,-8)$ will be given by the partial derivative ${f}_{x}(4,-4).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(4,-4):$

$$
\begin{aligned}{f}_{x}(4,-4) & =\frac{{4}^{2}+1}{{4}^{2}(-4)^{2}}+(-4)\sqrt{4} \\  & =\frac{17}{256}-4(2) \\  & =-\frac{2031}{256}\end{aligned}
$$

## 16. rational_radical — observed_raw

Source q-132584; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "-2", "z": "6"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-2.$ Given that the point $P(1,-2,6)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $1$
- $-1$
- $-\frac{5}{6}$
- $-\frac{3}{2}$
- $\frac{10}{6}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,-2,6)$ will be given by the partial derivative ${f}_{x}(1,-2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,-2):$

$$
\begin{aligned}{f}_{x}(1,-2) & =\frac{{1}^{2}+1}{{1}^{2}(-2)^{2}}+(-2)\sqrt{1} \\  & =\frac{2}{4}-2(1) \\  & =-\frac{3}{2}\end{aligned}
$$

## 17. cos_shift — observed_raw

Source q-64968; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=1.$ Given that the point $P$ with $y$-coordinate $0$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $2$
- $1$
- $0$
- $-1$
- $-2$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=0$ will be given by the partial derivative ${f}_{y}(1,0).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(1,0):$ 

$$
\begin{aligned}{f}_{y}(1,0) & =\sqrt{2}(1)\operatorname{cos}⁡(1\cdot 0+\frac{\pi }{4}) \\  & =\sqrt{2}\operatorname{cos}⁡(\frac{\pi }{4}) \\  & =\sqrt{2}\cdot \frac{\sqrt{2}}{2} \\  & =1\end{aligned}
$$

## 18. cos_shift — observed_supported

Source q-64968; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=1.$ Given that the point $P$ with $y$-coordinate $0$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $2$
- $1$
- $0$
- $-1$
- $-2$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=0$ will be given by the partial derivative ${f}_{y}(1,0).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(1,0):$ 

$$
\begin{aligned}{f}_{y}(1,0) & =\sqrt{2}(1)\operatorname{cos}⁡(1\cdot 0+\frac{\pi }{4}) \\  & =\sqrt{2}\operatorname{cos}⁡(\frac{\pi }{4}) \\  & =\sqrt{2}\cdot \frac{\sqrt{2}}{2} \\  & =1\end{aligned}
$$

## 19. cos_shift — observed_raw

Source q-64968; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-1", "y": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=-1.$ Given that the point $P$ with $y$-coordinate $0$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $2$
- $-1$
- $-2$
- $1$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=0$ will be given by the partial derivative ${f}_{y}(-1,0).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(-1,0):$ 

$$
\begin{aligned}{f}_{y}(-1,0) & =\sqrt{2}(-1)\operatorname{cos}⁡(-1\cdot 0+\frac{\pi }{4}) \\  & =\sqrt{2}(-1)\operatorname{cos}⁡(\frac{\pi }{4}) \\  & =\sqrt{2}(-1)\cdot \frac{\sqrt{2}}{2} \\  & =-1\end{aligned}
$$

## 20. cos_shift — observed_raw

Source q-64968; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=1.$ Given that the point $P$ with $y$-coordinate $0$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $2$
- $-2$
- $1$
- $0$
- $-1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=0$ will be given by the partial derivative ${f}_{y}(1,0).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(1,0):$ 

$$
\begin{aligned}{f}_{y}(1,0) & =\sqrt{2}(1)\operatorname{cos}⁡(1\cdot 0+\frac{\pi }{4}) \\  & =\sqrt{2}\operatorname{cos}⁡(\frac{\pi }{4}) \\  & =\sqrt{2}\cdot \frac{\sqrt{2}}{2} \\  & =1\end{aligned}
$$

## 21. polynomial — observed_raw

Source q-71198; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "3", "b": "6", "x": "2", "y": "1"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=2.$ Given that the point $P$ with $y$-coordinate $1$ lies on $C$, and that ${f}_{y}=3{x}^{2}y-6x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $2$
- $-1$
- $1$
- $-3$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=1$ will be given by the partial derivative ${f}_{y}(2,1).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(2,1):$ 

$$
\begin{aligned}{f}_{y}(2,1) & =3(2)^{2}(1)-6(2)(1)^{2} \\  & =12-12 \\  & =0\end{aligned}
$$

## 22. polynomial — observed_supported

Source q-71198; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "3", "b": "6", "x": "2", "y": "1"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=2.$ Given that the point $P$ with $y$-coordinate $1$ lies on $C$, and that ${f}_{y}=3{x}^{2}y-6x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $2$
- $-1$
- $1$
- $-3$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=1$ will be given by the partial derivative ${f}_{y}(2,1).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(2,1):$ 

$$
\begin{aligned}{f}_{y}(2,1) & =3(2)^{2}(1)-6(2)(1)^{2} \\  & =12-12 \\  & =0\end{aligned}
$$

## 23. polynomial — observed_raw

Source q-71198; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "2", "b": "2", "x": "-1", "y": "4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=-1.$ Given that the point $P$ with $y$-coordinate $4$ lies on $C$, and that ${f}_{y}=2{x}^{2}y-2x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $-4$
- $-8$
- $-1$
- $40$
- $4$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=4$ will be given by the partial derivative ${f}_{y}(-1,4).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(-1,4):$ 

$$
\begin{aligned}{f}_{y}(-1,4) & =2(-1)^{2}(4)-2(-1)(4)^{2} \\  & =8+(32) \\  & =40\end{aligned}
$$

## 24. polynomial — observed_raw

Source q-71198; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "4", "b": "6", "x": "2", "y": "-4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=2.$ Given that the point $P$ with $y$-coordinate $-4$ lies on $C$, and that ${f}_{y}=4{x}^{2}y-6x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $-256$
- $4$
- $2$
- $-4$
- $16$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=-4$ will be given by the partial derivative ${f}_{y}(2,-4).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(2,-4):$ 

$$
\begin{aligned}{f}_{y}(2,-4) & =4(2)^{2}(-4)-6(2)(-4)^{2} \\  & =-64-192 \\  & =-256\end{aligned}
$$

## 25. monomial — observed_raw

Source q-132578; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "4", "x": "1", "y": "2", "z": "5"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(1,2,5)$ lies on $C$, and that ${f}_{x}=4{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $8$
- $20$
- $12$
- $4$
- $6$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,2,5)$ will be given by the partial derivative ${f}_{x}(1,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,2):$

$$
\begin{aligned}{f}_{x}(1,2) & =4(1)^{2}(2)=8\end{aligned}
$$

## 26. monomial — observed_supported

Source q-132578; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "4", "x": "1", "y": "2", "z": "5"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(1,2,5)$ lies on $C$, and that ${f}_{x}=4{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $8$
- $20$
- $12$
- $4$
- $6$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,2,5)$ will be given by the partial derivative ${f}_{x}(1,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,2):$

$$
\begin{aligned}{f}_{x}(1,2) & =4(1)^{2}(2)=8\end{aligned}
$$

## 27. monomial — observed_raw

Source q-132578; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "5", "x": "-3", "y": "3", "z": "-4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P(-3,3,-4)$ lies on $C$, and that ${f}_{x}=5{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $135$
- $0$
- $8$
- $5$
- $30$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-3,3,-4)$ will be given by the partial derivative ${f}_{x}(-3,3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-3,3):$

$$
\begin{aligned}{f}_{x}(-3,3) & =5(-3)^{2}(3)=135\end{aligned}
$$

## 28. monomial — observed_raw

Source q-132578; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "5", "x": "-2", "y": "-2", "z": "-3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-2.$ Given that the point $P(-2,-2,-3)$ lies on $C$, and that ${f}_{x}=5{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $-40$
- $3$
- $10$
- $-20$
- $5$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-2,-2,-3)$ will be given by the partial derivative ${f}_{x}(-2,-2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-2,-2):$

$$
\begin{aligned}{f}_{x}(-2,-2) & =5(-2)^{2}(-2)=-40\end{aligned}
$$

## 29. log_exp — observed_raw

Source q-132580; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "E", "y": "2", "z": "3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e.$ Given that the point $P(e,2,3)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $4-e$
- $3$
- $2-{e}^{2}$
- $3e$
- $4{e}^{2}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e,2,3)$ will be given by the partial derivative ${f}_{y}(e,2).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e,2):$

$$
\begin{aligned}{f}_{y}(e,2) & =2(2)\operatorname{ln}⁡e-\frac{{e}^{2}}{e}=4-e\end{aligned}
$$

## 30. log_exp — observed_supported

Source q-132580; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "E", "y": "2", "z": "3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e.$ Given that the point $P(e,2,3)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $4-e$
- $3$
- $2-{e}^{2}$
- $3e$
- $4{e}^{2}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e,2,3)$ will be given by the partial derivative ${f}_{y}(e,2).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e,2):$

$$
\begin{aligned}{f}_{y}(e,2) & =2(2)\operatorname{ln}⁡e-\frac{{e}^{2}}{e}=4-e\end{aligned}
$$

## 31. log_exp — observed_raw

Source q-132580; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "exp(2)", "y": "1", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e^{2}.$ Given that the point $P(e^{2},1,-8)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $2$
- $2 e^{2}$
- $4-e^{-1}$
- $2 e$
- $1 - e$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e^{2}.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e^{2},1,-8)$ will be given by the partial derivative ${f}_{y}(e^{2},1).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e^{2},1):$

$$
\begin{aligned}{f}_{y}(e^{2},1) & =2(1)\operatorname{ln}⁡e^{2}-\frac{{e}^{1}}{e^{2}}=4-e^{-1}\end{aligned}
$$

## 32. log_exp — observed_raw

Source q-132580; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "E", "y": "2", "z": "6"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e.$ Given that the point $P(e,2,6)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $4-e$
- $4{e}^{2}$
- $3e$
- $2-{e}^{2}$
- $3$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e,2,6)$ will be given by the partial derivative ${f}_{y}(e,2).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e,2):$

$$
\begin{aligned}{f}_{y}(e,2) & =2(2)\operatorname{ln}⁡e-\frac{{e}^{2}}{e}=4-e\end{aligned}
$$

## 33. exp_cos — observed_raw

Source q-132582; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=\pi .$ Given that the point $P$ with $x$-coordinate $1$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $2\pi e$
- $\frac{1+\pi }{e}$
- $\pi $
- $\frac{\pi }{{e}^{2}}$
- $e+\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=\pi .$ Hence, the slope of the tangent to the curve $C$ at the point where $x=1$ will be given by the partial derivative ${f}_{x}(1,\pi ).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,\pi ):$

$$
\begin{aligned}{f}_{x}(1,\pi ) & =(1+\pi ){e}^{\operatorname{cos}⁡(\pi \cdot 1)} \\  & =(1+\pi ){e}^{-1} \\  & =\frac{1+\pi }{e}\end{aligned}
$$

## 34. exp_cos — observed_supported

Source q-132582; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "1", "y": "pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=\pi .$ Given that the point $P$ with $x$-coordinate $1$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $2\pi e$
- $\frac{1+\pi }{e}$
- $\pi $
- $\frac{\pi }{{e}^{2}}$
- $e+\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=\pi .$ Hence, the slope of the tangent to the curve $C$ at the point where $x=1$ will be given by the partial derivative ${f}_{x}(1,\pi ).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,\pi ):$

$$
\begin{aligned}{f}_{x}(1,\pi ) & =(1+\pi ){e}^{\operatorname{cos}⁡(\pi \cdot 1)} \\  & =(1+\pi ){e}^{-1} \\  & =\frac{1+\pi }{e}\end{aligned}
$$

## 35. exp_cos — observed_raw

Source q-132582; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-1", "y": "pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=\pi .$ Given that the point $P$ with $x$-coordinate $-1$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $e+\pi $
- $\frac{-1 + \pi }{e}$
- $2\pi e$
- $\frac{\pi }{{e}^{2}}$
- $\pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=\pi .$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-1$ will be given by the partial derivative ${f}_{x}(-1,\pi ).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-1,\pi ):$

$$
\begin{aligned}{f}_{x}(-1,\pi ) & =(-1+\pi ){e}^{\operatorname{cos}⁡(\pi \cdot -1)} \\  & =(-1+\pi ){e}^{-1} \\  & =\frac{-1+\pi}{e}\end{aligned}
$$

## 36. exp_cos — observed_raw

Source q-132582; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "-2", "y": "-pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=- \pi.$ Given that the point $P$ with $x$-coordinate $-2$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $- \frac{\pi }{{e}^{2}}$
- $- \pi $
- $- 2\pi e$
- $- e \left(2 + \pi \right)$
- $e - \pi $

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=- \pi.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-2$ will be given by the partial derivative ${f}_{x}(-2,- \pi).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-2,- \pi):$

$$
\begin{aligned}{f}_{x}(-2,- \pi) & =(-2- \pi){e}^{\operatorname{cos}⁡(- \pi\cdot -2)} \\  & =(-2- \pi){e}^{1} \\  & =- e \left(2+\pi\right)\end{aligned}
$$

## 37. radical_ratio — observed_raw

Source q-71199; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "3", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P$ with $x$-coordinate $3$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $1$
- $\frac{1}{2}$
- $-\frac{1}{2}$
- $-1$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=3$ will be given by the partial derivative ${f}_{x}(3,2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(3,2):$

$$
\begin{aligned}{f}_{x}(3,2) & =\frac{\sqrt{(3)^{2}-2(2)^{2}}}{2-3} \\  & =\frac{\sqrt{9-8}}{-1} \\  & =-1\end{aligned}
$$

## 38. radical_ratio — observed_supported

Source q-71199; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "3", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P$ with $x$-coordinate $3$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $1$
- $\frac{1}{2}$
- $-\frac{1}{2}$
- $-1$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=3$ will be given by the partial derivative ${f}_{x}(3,2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(3,2):$

$$
\begin{aligned}{f}_{x}(3,2) & =\frac{\sqrt{(3)^{2}-2(2)^{2}}}{2-3} \\  & =\frac{\sqrt{9-8}}{-1} \\  & =-1\end{aligned}
$$

## 39. radical_ratio — observed_raw

Source q-71199; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "6", "y": "4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=4.$ Given that the point $P$ with $x$-coordinate $6$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $1$
- $\frac{1}{4}$
- $0$
- $-1$
- $-\frac{1}{4}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=4.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=6$ will be given by the partial derivative ${f}_{x}(6,4).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(6,4):$

$$
\begin{aligned}{f}_{x}(6,4) & =\frac{\sqrt{(6)^{2}-2(4)^{2}}}{4-6} \\  & =\frac{\sqrt{36-32}}{-2} \\  & =-1\end{aligned}
$$

## 40. radical_ratio — observed_raw

Source q-71199; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"x": "6", "y": "4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=4.$ Given that the point $P$ with $x$-coordinate $6$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $-1$
- $-\frac{1}{4}$
- $1$
- $\frac{1}{4}$
- $0$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=4.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=6$ will be given by the partial derivative ${f}_{x}(6,4).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(6,4):$

$$
\begin{aligned}{f}_{x}(6,4) & =\frac{\sqrt{(6)^{2}-2(4)^{2}}}{4-6} \\  & =\frac{\sqrt{36-32}}{-2} \\  & =-1\end{aligned}
$$

## 41. base_exp — observed_raw

Source q-64966; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "2", "x": "0", "y": "1", "z": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=1.$ Given that the point $P(0,1,0)$ lies on $C$, and that ${f}_{x}={2}^{x+y}y(x\operatorname{ln}⁡(2)+1)$, find the slope of the tangent to $C$ at $P.$

- $-1$
- $1$
- $2$
- $0$
- $-2$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,1,0)$ will be given by the partial derivative ${f}_{x}(0,1).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,1):$

$$
\begin{aligned}{f}_{x}(0,1) & ={2}^{0+1}(1)(0\cdot \operatorname{ln}⁡(2)+1)=2\end{aligned}
$$

## 42. base_exp — observed_supported

Source q-64966; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "2", "x": "0", "y": "1", "z": "0"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=1.$ Given that the point $P(0,1,0)$ lies on $C$, and that ${f}_{x}={2}^{x+y}y(x\operatorname{ln}⁡(2)+1)$, find the slope of the tangent to $C$ at $P.$

- $-1$
- $1$
- $2$
- $0$
- $-2$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,1,0)$ will be given by the partial derivative ${f}_{x}(0,1).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,1):$

$$
\begin{aligned}{f}_{x}(0,1) & ={2}^{0+1}(1)(0\cdot \operatorname{ln}⁡(2)+1)=2\end{aligned}
$$

## 43. base_exp — observed_raw

Source q-64966; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "2", "x": "0", "y": "2", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(0,2,-8)$ lies on $C$, and that ${f}_{x}={2}^{x+y}y(x\operatorname{ln}⁡(2)+1)$, find the slope of the tangent to $C$ at $P.$

- $2$
- $0$
- $-2$
- $-4$
- $8$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,2,-8)$ will be given by the partial derivative ${f}_{x}(0,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,2):$

$$
\begin{aligned}{f}_{x}(0,2) & ={2}^{0+2}(2)(0\cdot \operatorname{ln}⁡(2)+1)=8\end{aligned}
$$

## 44. base_exp — observed_raw

Source q-64966; origin observed-mask; difficulty :question.difficulty/easy; evidence only True. Parameters `{"a": "3", "x": "0", "y": "1", "z": "6"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=1.$ Given that the point $P(0,1,6)$ lies on $C$, and that ${f}_{x}={3}^{x+y}y(x\operatorname{ln}⁡(3)+1)$, find the slope of the tangent to $C$ at $P.$

- $-1$
- $-3$
- $0$
- $3$
- $1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,1,6)$ will be given by the partial derivative ${f}_{x}(0,1).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,1):$

$$
\begin{aligned}{f}_{x}(0,1) & ={3}^{0+1}(1)(0\cdot \operatorname{ln}⁡(3)+1)=3\end{aligned}
$$

## 45. linear — authored_method

Source q-36216; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "5", "x": "1", "y": "4", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=4.$ Given that the point $P(1,4,-8)$ lies on $C$, and that ${f}_{x}=5x-y$, find the slope of the tangent to $C$ at $P.$

- $1$
- $19$
- $9$
- $-4$
- $5$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=4.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,4,-8)$ will be given by the partial derivative ${f}_{x}(1,4).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,4):$

$$
\begin{aligned}{f}_{x}(1,4) & =5(1)-(4)=1\end{aligned}
$$

## 46. linear — authored_method

Source q-36216; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "5", "x": "-3", "y": "1", "z": "6"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=1.$ Given that the point $P(-3,1,6)$ lies on $C$, and that ${f}_{x}=5x-y$, find the slope of the tangent to $C$ at $P.$

- $-15$
- $8$
- $-16$
- $-14$
- $-1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-3,1,6)$ will be given by the partial derivative ${f}_{x}(-3,1).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-3,1):$

$$
\begin{aligned}{f}_{x}(-3,1) & =5(-3)-(1)=-16\end{aligned}
$$

## 47. cos_sum — authored_method

Source q-36463; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "3*pi/2", "y": "pi"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = \pi$. Given that the point $P$ with $x$-coordinate $\frac{3 \pi}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $1 - \pi$
- $- \pi - 1$
- $\pi$
- $1$
- $-1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=\pi.$ Hence, the slope of the tangent to the curve $C$ at the point $P(\frac{3 \pi}{2},\pi,0)$ will be given by the partial derivative ${f}_{x}(\frac{3 \pi}{2},\pi).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(\frac{3 \pi}{2},\pi):$

$$
\begin{aligned}{f}_{x}(\frac{3 \pi}{2},\pi) & =(\pi)\cos (\frac{3 \pi}{2})+\cos (\pi) \\  & =-1\end{aligned}
$$

## 48. cos_sum — authored_method

Source q-36463; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "-pi/2", "y": "2*pi"}`.

A surface $S$ is defined by $z = f(x, y)$. The curve $C$ is the intersection of $S$ with the plane $y = 2 \pi$. Given that the point $P$ with $x$-coordinate $- \frac{\pi}{2}$ lies on $C$, and that $f_{x} = y\cos x + \cos y$, find the slope of the tangent to $C$ at $P$.

- $2 \pi$
- $1 - 2 \pi$
- $- 2 \pi - 1$
- $-1$
- $1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2 \pi.$ Hence, the slope of the tangent to the curve $C$ at the point $P(- \frac{\pi}{2},2 \pi,0)$ will be given by the partial derivative ${f}_{x}(- \frac{\pi}{2},2 \pi).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(- \frac{\pi}{2},2 \pi):$

$$
\begin{aligned}{f}_{x}(- \frac{\pi}{2},2 \pi) & =(2 \pi)\cos (- \frac{\pi}{2})+\cos (2 \pi) \\  & =1\end{aligned}
$$

## 49. sin_product — authored_method

Source q-132579; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "3*pi/2", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P$ with $x$-coordinate $\frac{3 \pi}{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $-1 + \frac{3 \pi}{2}$
- $1 + 3 \pi$
- $3 \pi$
- $-1$
- $-1 + 3 \pi$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=\frac{3 \pi}{2}$ will be given by the partial derivative ${f}_{x}(\frac{3 \pi}{2},2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(\frac{3 \pi}{2},2):$

$$
\begin{aligned}{f}_{x}(\frac{3 \pi}{2},2) & =\operatorname{sin}⁡(\frac{3 \pi}{2})+(\frac{3 \pi}{2})\cdot 2 \\  & =-1+3 \pi\end{aligned}
$$

## 50. sin_product — authored_method

Source q-132579; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "-pi/2", "y": "3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P$ with $x$-coordinate $-\frac{\pi }{2}$ lies on $C$, and that ${f}_{x}=\operatorname{sin}⁡x+xy$, find the slope of the tangent to $C$ at $P.$

- $- \frac{3 \pi}{2}$
- $1 - \frac{3 \pi}{2}$
- $- \frac{\pi}{2} - 1$
- $-1$
- $- \frac{3 \pi}{2} - 1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-\frac{\pi }{2}$ will be given by the partial derivative ${f}_{x}(-\frac{\pi }{2},3).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-\frac{\pi }{2},3):$

$$
\begin{aligned}{f}_{x}(-\frac{\pi }{2},3) & =\operatorname{sin}⁡(-\frac{\pi }{2})+(-\frac{\pi }{2})\cdot 3 \\  & =-\frac{3 \pi}{2}-1\end{aligned}
$$

## 51. rational_radical — authored_method

Source q-132584; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "4", "y": "2", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(4,2,-8)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $\frac{273}{64}$
- $- \frac{239}{64}$
- $\frac{145}{32}$
- $4$
- $\frac{17}{64}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(4,2,-8)$ will be given by the partial derivative ${f}_{x}(4,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(4,2):$

$$
\begin{aligned}{f}_{x}(4,2) & =\frac{{4}^{2}+1}{{4}^{2}(2)^{2}}+(2)\sqrt{4} \\  & =\frac{17}{64}+2(2) \\  & =\frac{273}{64}\end{aligned}
$$

## 52. rational_radical — authored_method

Source q-132584; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "1", "y": "3", "z": "-7"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=3.$ Given that the point $P(1,3,-7)$ lies on $C$, and that ${f}_{x}=\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}$, find the slope of the tangent to $C$ at $P.$

- $3$
- $- \frac{25}{9}$
- $\frac{11}{3}$
- $\frac{29}{9}$
- $\frac{2}{9}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(1,3,-7)$ will be given by the partial derivative ${f}_{x}(1,3).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,3):$

$$
\begin{aligned}{f}_{x}(1,3) & =\frac{{1}^{2}+1}{{1}^{2}(3)^{2}}+(3)\sqrt{1} \\  & =\frac{2}{9}+3(1) \\  & =\frac{29}{9}\end{aligned}
$$

## 53. cos_shift — authored_method

Source q-64968; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "1", "y": "pi/2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=1.$ Given that the point $P$ with $y$-coordinate $\frac{\pi}{2}$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $1$
- $0$
- $\sqrt{2}$
- $- \frac{\sqrt{2}}{2}$
- $-1$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=\frac{\pi}{2}$ will be given by the partial derivative ${f}_{y}(1,\frac{\pi}{2}).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(1,\frac{\pi}{2}):$ 

$$
\begin{aligned}{f}_{y}(1,\frac{\pi}{2}) & =\sqrt{2}(1)\operatorname{cos}⁡(1\cdot \frac{\pi }{2}+\frac{\pi }{4}) \\  & =\sqrt{2}\operatorname{cos}⁡(\frac{3 \pi}{4}) \\  & =\sqrt{2}\cdot-\frac{\sqrt{2}}{2} \\  & =-1\end{aligned}
$$

## 54. cos_shift — authored_method

Source q-64968; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "-2", "y": "-pi/2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=-2.$ Given that the point $P$ with $y$-coordinate $- \frac{\pi}{2}$ lies on $C$, and that ${f}_{y}=\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})$, find the slope of the tangent to $C$ at $P.$

- $- 2 \sqrt{2}$
- $2 \sqrt{2}$
- $-2$
- $\sqrt{2}$
- $2$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-2.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=- \frac{\pi}{2}$ will be given by the partial derivative ${f}_{y}(-2,- \frac{\pi}{2}).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(-2,- \frac{\pi}{2}):$ 

$$
\begin{aligned}{f}_{y}(-2,- \frac{\pi}{2}) & =\sqrt{2}(-2)\operatorname{cos}⁡(-2\cdot-\frac{\pi }{2}+\frac{\pi }{4}) \\  & =\sqrt{2}(-2)\operatorname{cos}⁡(\frac{5 \pi}{4}) \\  & =\sqrt{2}(-2)\cdot-\frac{\sqrt{2}}{2} \\  & =2\end{aligned}
$$

## 55. polynomial — authored_method

Source q-71198; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "5", "b": "2", "x": "1", "y": "4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=1.$ Given that the point $P$ with $y$-coordinate $4$ lies on $C$, and that ${f}_{y}=5{x}^{2}y-2x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $-12$
- $72$
- $52$
- $-32$
- $20$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=1.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=4$ will be given by the partial derivative ${f}_{y}(1,4).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(1,4):$ 

$$
\begin{aligned}{f}_{y}(1,4) & =5(1)^{2}(4)-2(1)(4)^{2} \\  & =20-32 \\  & =-12\end{aligned}
$$

## 56. polynomial — authored_method

Source q-71198; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "2", "b": "4", "x": "-2", "y": "2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=-2.$ Given that the point $P$ with $y$-coordinate $2$ lies on $C$, and that ${f}_{y}=2{x}^{2}y-4x{y}^{2}$, find the slope of the tangent to $C$ at $P.$

- $-48$
- $16$
- $-16$
- $32$
- $48$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=-2.$ Hence, the slope of the tangent to the curve $C$ at the point where $y=2$ will be given by the partial derivative ${f}_{y}(-2,2).$ 

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(-2,2):$ 

$$
\begin{aligned}{f}_{y}(-2,2) & =2(-2)^{2}(2)-4(-2)(2)^{2} \\  & =16+(32) \\  & =48\end{aligned}
$$

## 57. monomial — authored_method

Source q-132578; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "5", "x": "-1", "y": "2", "z": "3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(-1,2,3)$ lies on $C$, and that ${f}_{x}=5{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $15$
- $10$
- $-10$
- $5$
- $-20$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-1,2,3)$ will be given by the partial derivative ${f}_{x}(-1,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-1,2):$

$$
\begin{aligned}{f}_{x}(-1,2) & =5(-1)^{2}(2)=10\end{aligned}
$$

## 58. monomial — authored_method

Source q-132578; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "2", "x": "-2", "y": "2", "z": "-1"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(-2,2,-1)$ lies on $C$, and that ${f}_{x}=2{x}^{2}y$, find the slope of the tangent to $C$ at $P.$

- $12$
- $-16$
- $-8$
- $8$
- $16$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(-2,2,-1)$ will be given by the partial derivative ${f}_{x}(-2,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-2,2):$

$$
\begin{aligned}{f}_{x}(-2,2) & =2(-2)^{2}(2)=16\end{aligned}
$$

## 59. log_exp — authored_method

Source q-132580; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "exp(2)", "y": "2", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e^{2}.$ Given that the point $P(e^{2},2,-8)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $7$
- $9$
- $4 - e^{2}$
- $-1$
- $8$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e^{2}.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e^{2},2,-8)$ will be given by the partial derivative ${f}_{y}(e^{2},2).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e^{2},2):$

$$
\begin{aligned}{f}_{y}(e^{2},2) & =2(2)\operatorname{ln}⁡e^{2}-\frac{{e}^{2}}{e^{2}}=7\end{aligned}
$$

## 60. log_exp — authored_method

Source q-132580; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "E", "y": "3", "z": "-7"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=e.$ Given that the point $P(e,3,-7)$ lies on $C$, and that ${f}_{y}=2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}$, find the slope of the tangent to $C$ at $P.$

- $- e^{2}$
- $6 + e^{2}$
- $3 - e^{3}$
- $6 - e^{2}$
- $6$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=e.$ Hence, the slope of the tangent to the curve $C$ at the point $P(e,3,-7)$ will be given by the partial derivative ${f}_{y}(e,3).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(e,3):$

$$
\begin{aligned}{f}_{y}(e,3) & =2(3)\operatorname{ln}⁡e-\frac{{e}^{3}}{e}=6-e^{2}\end{aligned}
$$

## 61. exp_cos — authored_method

Source q-132582; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "1", "y": "-pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=- \pi.$ Given that the point $P$ with $x$-coordinate $1$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $-1 + \pi$
- $- \pi$
- $- \frac{\pi}{e} + 1$
- $e \left(1 - \pi\right)$
- $\frac{1 - \pi}{e}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=- \pi.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=1$ will be given by the partial derivative ${f}_{x}(1,- \pi).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(1,- \pi):$

$$
\begin{aligned}{f}_{x}(1,- \pi) & =(1- \pi){e}^{\operatorname{cos}⁡(- \pi\cdot 1)} \\  & =(1- \pi){e}^{-1} \\  & =\frac{1-\pi}{e}\end{aligned}
$$

## 62. exp_cos — authored_method

Source q-132582; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "-2", "y": "2*pi"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2 \pi.$ Given that the point $P$ with $x$-coordinate $-2$ lies on $C$, and that ${f}_{x}=(x+y){e}^{\operatorname{cos}⁡(xy)}$, find the slope of the tangent to $C$ at $P.$

- $-2 + 2 e \pi$
- $2 \pi$
- $-2 + 2 \pi$
- $\frac{2 \left(-1 + \pi\right)}{e}$
- $2 e \left(-1 + \pi\right)$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2 \pi.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=-2$ will be given by the partial derivative ${f}_{x}(-2,2 \pi).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(-2,2 \pi):$

$$
\begin{aligned}{f}_{x}(-2,2 \pi) & =(-2+2 \pi){e}^{\operatorname{cos}⁡(2 \pi\cdot -2)} \\  & =(-2+2 \pi){e}^{1} \\  & =2 e \left(-1+\pi\right)\end{aligned}
$$

## 63. radical_ratio — authored_method

Source q-71199; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "6", "y": "-4"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-4.$ Given that the point $P$ with $x$-coordinate $6$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $- \frac{\sqrt{5}}{5}$
- $- \frac{1}{2}$
- $\frac{1}{5}$
- $- \frac{1}{5}$
- $\frac{1}{2}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-4.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=6$ will be given by the partial derivative ${f}_{x}(6,-4).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(6,-4):$

$$
\begin{aligned}{f}_{x}(6,-4) & =\frac{\sqrt{(6)^{2}-2(-4)^{2}}}{-4-6} \\  & =\frac{\sqrt{36-32}}{-10} \\  & =-\frac{1}{5}\end{aligned}
$$

## 64. radical_ratio — authored_method

Source q-71199; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"x": "3", "y": "-2"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=-2.$ Given that the point $P$ with $x$-coordinate $3$ lies on $C$, and that ${f}_{x}=\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}$, find the slope of the tangent to $C$ at $P.$

- $- \frac{1}{2}$
- $\frac{1}{2}$
- $\frac{1}{5}$
- $- \frac{1}{5}$
- $- \frac{\sqrt{5}}{5}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=-2.$ Hence, the slope of the tangent to the curve $C$ at the point where $x=3$ will be given by the partial derivative ${f}_{x}(3,-2).$ 

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(3,-2):$

$$
\begin{aligned}{f}_{x}(3,-2) & =\frac{\sqrt{(3)^{2}-2(-2)^{2}}}{-2-3} \\  & =\frac{\sqrt{9-8}}{-5} \\  & =-\frac{1}{5}\end{aligned}
$$

## 65. base_exp — authored_method

Source q-64966; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "3", "x": "0", "y": "2", "z": "-8"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=2.$ Given that the point $P(0,2,-8)$ lies on $C$, and that ${f}_{x}={3}^{x+y}y(x\operatorname{ln}⁡(3)+1)$, find the slope of the tangent to $C$ at $P.$

- $18$
- $27$
- $2$
- $0$
- $-18$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=2.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,2,-8)$ will be given by the partial derivative ${f}_{x}(0,2).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,2):$

$$
\begin{aligned}{f}_{x}(0,2) & ={3}^{0+2}(2)(0\cdot \operatorname{ln}⁡(3)+1)=18\end{aligned}
$$

## 66. base_exp — authored_method

Source q-64966; origin authored-bank/source-mask; difficulty :question.difficulty/easy; evidence only False. Parameters `{"a": "4", "x": "0", "y": "1", "z": "-7"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $y=1.$ Given that the point $P(0,1,-7)$ lies on $C$, and that ${f}_{x}={4}^{x+y}y(x\operatorname{ln}⁡(4)+1)$, find the slope of the tangent to $C$ at $P.$

- $0$
- $8$
- $1$
- $4$
- $-4$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $y=1.$ Hence, the slope of the tangent to the curve $C$ at the point $P(0,1,-7)$ will be given by the partial derivative ${f}_{x}(0,1).$

To get the slope, we evaluate the partial derivative ${f}_{x}(x,y)$ at $(0,1):$

$$
\begin{aligned}{f}_{x}(0,1) & ={4}^{0+1}(1)(0\cdot \operatorname{ln}⁡(4)+1)=4\end{aligned}
$$

## 67. canonical_rational — authored_method

Source None; origin authored-missing-level; difficulty :question.difficulty/moderate; evidence only False. Parameters `{"a": "2", "x": "3", "y": "4", "z": "-1"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=3.$ Given that the point $P(3,4,-1)$ lies on $C,$ and that $f_y = \dfrac{2x}y - 2x^2y$, find the slope of the tangent to $C$ at $P.$

- $- \frac{141}{2}$
- $-72$
- $\frac{147}{2}$
- $\frac{3}{2}$
- $-66$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(3,4,-1)$ will be given by the partial derivative ${f}_{y}(3,4).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(3,4):$

$$
\begin{aligned}{f}_{y}(3,4) & =\frac{2(3)}{(4)}-2(3)^2(4) \\  & =(\frac{3}{2})+(-72) \\  & =- \frac{141}{2}\end{aligned}
$$

## 68. canonical_rational — authored_method

Source None; origin authored-missing-level; difficulty :question.difficulty/moderate; evidence only False. Parameters `{"a": "5", "x": "3", "y": "4", "z": "3"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=3.$ Given that the point $P(3,4,3)$ lies on $C,$ and that $f_y = \dfrac{5x}y - 5x^2y$, find the slope of the tangent to $C$ at $P.$

- $-180$
- $\frac{15}{4}$
- $-165$
- $- \frac{705}{4}$
- $\frac{735}{4}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(3,4,3)$ will be given by the partial derivative ${f}_{y}(3,4).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(3,4):$

$$
\begin{aligned}{f}_{y}(3,4) & =\frac{5(3)}{(4)}-5(3)^2(4) \\  & =(\frac{15}{4})+(-180) \\  & =- \frac{705}{4}\end{aligned}
$$

## 69. canonical_trig — authored_method

Source None; origin authored-missing-level; difficulty :question.difficulty/hard; evidence only False. Parameters `{"a": "2", "b": "3", "x": "3", "y": "4", "z": "7"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=3.$ Given that the point $P(3,4,7)$ lies on $C,$ and that $f_y = \dfrac{2x}y - 2x^2y+3\cos(\pi y)$, find the slope of the tangent to $C$ at $P.$

- $- \frac{135}{2}$
- $-69$
- $\frac{153}{2}$
- $-63$
- $\frac{9}{2}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(3,4,7)$ will be given by the partial derivative ${f}_{y}(3,4).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(3,4):$

$$
\begin{aligned}{f}_{y}(3,4) & =\frac{2(3)}{(4)}-2(3)^2(4)+3\cos(\pi (4)) \\  & =(\frac{3}{2})+(-72)+(3) \\  & =- \frac{135}{2}\end{aligned}
$$

## 70. canonical_trig — authored_method

Source None; origin authored-missing-level; difficulty :question.difficulty/hard; evidence only False. Parameters `{"a": "5", "b": "2", "x": "3", "y": "4", "z": "-6"}`.

A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane $x=3.$ Given that the point $P(3,4,-6)$ lies on $C,$ and that $f_y = \dfrac{5x}y - 5x^2y+2\cos(\pi y)$, find the slope of the tangent to $C$ at $P.$

- $-163$
- $-178$
- $\frac{743}{4}$
- $- \frac{697}{4}$
- $\frac{23}{4}$

The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $x=3.$ Hence, the slope of the tangent to the curve $C$ at the point $P(3,4,-6)$ will be given by the partial derivative ${f}_{y}(3,4).$

To get the slope, we evaluate the partial derivative ${f}_{y}(x,y)$ at $(3,4):$

$$
\begin{aligned}{f}_{y}(3,4) & =\frac{5(3)}{(4)}-5(3)^2(4)+2\cos(\pi (4)) \\  & =(\frac{15}{4})+(-180)+(2) \\  & =- \frac{697}{4}\end{aligned}
$$

