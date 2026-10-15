## Generated — authored normal — Easy
Consider the line integral

$$
\int_C x - 2 y\,\mathrm{d}s=\sqrt{10}\int_{0}^{4}\boxed{}\,\mathrm{d}t
$$

where $C$ is the segment of the line $\frac{x}{4}=1 - \frac{3 y}{4}$ traversed between the points $(4,0)$ and $(-8,4)$. Which of the following is the missing expression under the integral on the right?

*Hint: Use the parameter $y=t.$*

- **A.** $- 5 t$
- **B.** $7 t - 8$
- **C (correct).** $4 - 5 t$
- **D.** $4 - t$
- **E.** $4 - 3 t$

**Worked solution**

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
\frac{x}{4}=1 - \frac{3 y}{4}\,\Longrightarrow\,x=4 - 3 y
$$

Therefore, by setting $y=t,$ we have 

$$
x=x(t)=4 - 3 t.
$$

 

This gives the following parametrization of the curve:

$$
r(t)=\langle 4 - 3 t,\,t\rangle,\quad 0\le t\le 4
$$

Note that the domain $0\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(4 - 3 t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(-3)i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(-3)^2+1^2} \\ &=\sqrt{9+1} \\ &=\sqrt{10}\end{aligned}
$$

 

Now, if  $f(x,y)=x - 2 y,$ then we obtain 

$$
\begin{aligned}f(r(t))&=1\left(4 - 3 t\right)-2t \\ &=4 - 5 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}\int_C x - 2 y\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{0}^{4}(4 - 5 t)\cdot \sqrt{10}\,\mathrm{d}t \\ &=\sqrt{10}\int_{0}^{4}(4 - 5 t)\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Easy
Consider the line integral

$$
\int_C 4 x^{2} y^{3}\,\mathrm{d}s=\sqrt{5}\int_{2}^{4}\boxed{}\,\mathrm{d}t
$$

where $C$ is the segment of the line $x=2 y + 2$ traversed between the points $(6,2)$ and $(10,4)$. Which of the following is the missing expression under the integral on the right?

*Hint: Use the parameter $y=t.$*

- **A (correct).** $4 t^{3} \left(2 t + 2\right)^{2}$
- **B.** $16 t^{5}$
- **C.** $4 t^{3} \left(2 - 2 t\right)^{2}$
- **D.** $4 t^{2} \left(2 t + 2\right)^{3}$
- **E.** $4 \left(2 t + 2\right)^{2}$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=2 t + 2.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle 2 t + 2,\,t\rangle,\quad 2\le t\le 4
$$

Note that the domain $2\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 2)i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(2)i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(2)^2+1^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, if $f(x,y)=4 x^{2} y^{3},$ then we obtain

$$
\begin{aligned}f(r(t))&=4\left(2 t + 2\right)^{2}t^{3} \\ &=4 t^{3} \left(2 t + 2\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 4 x^{2} y^{3}\,\mathrm{d}s&=\int_{2}^{4}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{2}^{4}(4 t^{3} \left(2 t + 2\right)^{2})\cdot \sqrt{5}\,\mathrm{d}t \\ &=\sqrt{5}\int_{2}^{4}4 t^{3} \left(2 t + 2\right)^{2}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Easy
Consider the line integral

$$
\int_C 48 x^{2} y^{3}\,\mathrm{d}s=\frac{\sqrt{17}}{4}\int_{1}^{2}\boxed{}\,\mathrm{d}t
$$

where $C$ is the segment of the line $4x=y$ traversed between the points $(\frac{1}{4},1)$ and $(\frac{1}{2},2)$. Which of the following is the missing expression under the integral on the right?

*Hint: Use the parameter $y=t.$*

- **A (correct).** $3 t^{5}$
- **B.** $768 t^{5}$
- **C.** $12 t^{5}$
- **D.** $\frac{3 t^{5}}{64}$
- **E.** $3 t^{2}$

**Worked solution**

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
4x=y\,\Longrightarrow\,x=\frac{y}{4}
$$

Therefore, by setting $y=t,$ we have 

$$
x=x(t)=\frac{t}{4}.
$$

 

This gives the following parametrization of the curve:

$$
r(t)=\langle\frac{t}{4},\,t\rangle,\quad 1\le t\le 2
$$

Note that the domain $1\le t\le 2$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t}{4})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(\frac{1}{4})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(\frac{1}{4})^2+1^2} \\ &=\sqrt{\frac{1}{16}+1} \\ &=\sqrt{\frac{17}{16}} \\ &=\frac{\sqrt{17}}{4}\end{aligned}
$$

 

Now, if  $f(x,y)=48 x^{2} y^{3},$ then we obtain 

$$
\begin{aligned}f(r(t))&=48\left(\frac{t}{4}\right)^2t^{3} \\ &=48\left(\frac{t^2}{16}\right)t^{3} \\ &=3 t^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}\int_C 48 x^{2} y^{3}\,\mathrm{d}s&=\int_{1}^{2}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{1}^{2}(3 t^{5})\cdot \frac{\sqrt{17}}{4}\,\mathrm{d}t \\ &=\frac{\sqrt{17}}{4}\int_{1}^{2}3 t^{5}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Moderate
Which of the following is equivalent to the integral $\int_C y^{2} e^{x}\,\mathrm{d}s$

where $C$ is the section of the curve $x=3 \ln{\left(y \right)}$ traversed between the points $(0,1)$ and $(6,e^{2})$.

*Hint: Use the parameter $y=t.$*

- **A (correct).** $\int_{1}^{e^{2}}t^{4} \sqrt{t^{2} + 9}\,\mathrm{d}t$
- **B.** $\int_{1}^{e^{2}}\sqrt{10} t^{5}\,\mathrm{d}t$
- **C.** $\int_{1}^{e^{2}}t \sqrt{t^{2} + 9}\,\mathrm{d}t$
- **D.** $\int_{1}^{e^{2}}t^{5} \sqrt{t^{2} + 9}\,\mathrm{d}t$
- **E.** $\int_{0}^{6}t^{4} \sqrt{t^{2} + 9}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=3 \ln{\left(t \right)}.
$$

 

This gives the following parametrization of the curve:

$$
r(t)=\langle 3 \ln{\left(t \right)},\,t\rangle,\quad 1\le t\le e^{2}
$$

Note that the domain $1\le t\le e^{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(3 \ln{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(\frac{3}{t})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(\frac{3}{t})^2+1^2} \\ &=\sqrt{\frac{9}{t^2}+1} \\ &=\sqrt{\frac{t^{2} + 9}{t^2}} \\ &=\frac{\sqrt{t^{2} + 9}}{|t|} \\ &=\frac{\sqrt{t^{2} + 9}}{t}\end{aligned}
$$

 

Now, if  $f(x,y)=y^{2} e^{x},$ then we obtain 

$$
\begin{aligned}f(r(t))&=1\left(e^{3\ln t}\right)t^{2} \\ &=1\left(t^{3}\right)t^{2} \\ &=t^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}\int_C y^{2} e^{x}\,\mathrm{d}s&=\int_{1}^{e^{2}}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{1}^{e^{2}}(t^{5})\cdot \sqrt{1 + \frac{9}{t^{2}}}\,\mathrm{d}t \\ &=\int_{1}^{e^{2}}t^{4} \sqrt{t^{2} + 9}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Moderate
Which of the following is equivalent to the integral $\int_C 4 y e^{x}\,\mathrm{d}s$

where $C$ is the section of the curve $\frac{x}{2}=\ln y$ traversed between the points $(0,1)$ and $(4,e^{2})$.

*Hint: Use the parameter $y=t.$*

- **A.** $\int_{1}^{e^{2}}4 t^{3} \sqrt{t^{2} + 4}\,\mathrm{d}t$
- **B.** $\int_{0}^{4}4 t^{2} \sqrt{t^{2} + 4}\,\mathrm{d}t$
- **C (correct).** $\int_{1}^{e^{2}}4 t^{2} \sqrt{t^{2} + 4}\,\mathrm{d}t$
- **D.** $\int_{1}^{e^{2}}4 \sqrt{5} t^{3}\,\mathrm{d}t$
- **E.** $\int_{1}^{e^{2}}4 \sqrt{t^{2} + 4}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
\frac{x}{2}=\ln y\,\Longrightarrow\,x=2 \ln{\left(y \right)}
$$

Therefore, by setting $y=t,$ we have 

$$
x=x(t)=2 \ln{\left(t \right)}.
$$

 

This gives the following parametrization of the curve:

$$
r(t)=\langle 2 \ln{\left(t \right)},\,t\rangle,\quad 1\le t\le e^{2}
$$

Note that the domain $1\le t\le e^{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(2 \ln{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(\frac{2}{t})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(\frac{2}{t})^2+1^2} \\ &=\sqrt{\frac{4}{t^2}+1} \\ &=\frac{1}{t}\sqrt{t^{2} + 4}\end{aligned}
$$

 

Now, if  $f(x,y)=4 y e^{x}$, then we obtain 

$$
\begin{aligned}f(r(t))&=4 y e^{x} \\ &=4\cdot t^{1}e^{2\ln t} \\ &=4\cdot t^{1}\left(t^{2}\right) \\ &=4 t^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}\int_C 4 y e^{x}\,\mathrm{d}s&=\int_{1}^{e^{2}}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{1}^{e^{2}}(4 t^{3})\cdot \sqrt{1 + \frac{4}{t^{2}}}\,\mathrm{d}t \\ &=\int_{1}^{e^{2}}4 t^{2} \sqrt{t^{2} + 4}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Hard
Which of the following is equivalent to the integral $\int_C 2 x^{2} y^{2}\,\mathrm{d}s$

where $C$ is the section of the curve $x=y^{3} - 4$ traversed between the points $(-4,0)$ and $(23,3)$.

*Hint: Use the parameter $y=t.$*

- **A (correct).** $\int_{0}^{3}2 t^{2} \left(t^{3} - 4\right)^{2} \sqrt{9 t^{4} + 1}\,\mathrm{d}t$
- **B.** $\int_{0}^{3}2 t^{2} \left(t^{3} - 4\right)^{2} \sqrt{t^{4} + 1}\,\mathrm{d}t$
- **C.** $\int_{0}^{3}2 \left(t^{3} - 4\right)^{2} \sqrt{9 t^{4} + 1}\,\mathrm{d}t$
- **D.** $\int_{0}^{3}t^{2} \left(2 t^{3} - 8\right) \sqrt{9 t^{4} + 1}\,\mathrm{d}t$
- **E.** $\int_{0}^{3}2 t^{2} \left(t^{3} - 4\right)^{2}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=t^{3} - 4.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle t^{3} - 4,\,t\rangle,\quad 0\le t\le 3
$$

Note that the domain $0\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(t^{3} - 4)i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(3 t^{2})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(3 t^{2})^2+1^2} \\ &=\sqrt{9 t^{4} + 1}\end{aligned}
$$

Now, if $f(x,y)=2 x^{2} y^{2},$ then we obtain

$$
\begin{aligned}f(r(t))&=2\left(t^{3} - 4\right)^{2}t^{2} \\ &=2 t^{2} \left(t^{3} - 4\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x^{2} y^{2}\,\mathrm{d}s&=\int_{0}^{3}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{0}^{3}(2 t^{2} \left(t^{3} - 4\right)^{2})\cdot \sqrt{9 t^{4} + 1}\,\mathrm{d}t \\ &=\int_{0}^{3}2 t^{2} \left(t^{3} - 4\right)^{2} \sqrt{9 t^{4} + 1}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Hard
Which of the following is equivalent to the integral $\int_C 5 x^{2} y\,\mathrm{d}s$

where $C$ is the section of the curve $x=3 - 3 y^{3}$ traversed between the points $(3,0)$ and $(-78,3)$.

*Hint: Use the parameter $y=t.$*

- **A.** $\int_{0}^{3}t \left(15 - 15 t^{3}\right) \sqrt{81 t^{4} + 1}\,\mathrm{d}t$
- **B.** $\int_{0}^{3}5 t \left(3 - 3 t^{3}\right)^{2} \sqrt{9 t^{4} + 1}\,\mathrm{d}t$
- **C (correct).** $\int_{0}^{3}5 t \left(3 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t$
- **D.** $\int_{0}^{3}5 t \left(3 - 3 t^{3}\right)^{2}\,\mathrm{d}t$
- **E.** $\int_{0}^{3}5 \left(3 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=3 - 3 t^{3}.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle 3 - 3 t^{3},\,t\rangle,\quad 0\le t\le 3
$$

Note that the domain $0\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(3 - 3 t^{3})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(- 9 t^{2})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(- 9 t^{2})^2+1^2} \\ &=\sqrt{81 t^{4} + 1}\end{aligned}
$$

Now, if $f(x,y)=5 x^{2} y,$ then we obtain

$$
\begin{aligned}f(r(t))&=5\left(3 - 3 t^{3}\right)^{2}t^{1} \\ &=5 t \left(3 - 3 t^{3}\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 5 x^{2} y\,\mathrm{d}s&=\int_{0}^{3}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{0}^{3}(5 t \left(3 - 3 t^{3}\right)^{2})\cdot \sqrt{81 t^{4} + 1}\,\mathrm{d}t \\ &=\int_{0}^{3}5 t \left(3 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Hard
Which of the following is equivalent to the integral $\int_C 2 x^{2} y^{2}\,\mathrm{d}s$

where $C$ is the section of the curve $x=2 y^{2} + 3$ traversed between the points $(5,1)$ and $(21,3)$.

*Hint: Use the parameter $y=t.$*

- **A.** $\int_{1}^{3}2 t^{2} \left(2 t^{2} + 3\right)^{2}\,\mathrm{d}t$
- **B.** $\int_{1}^{3}2 t^{2} \left(2 t^{2} + 3\right)^{2} \sqrt{4 t^{2} + 1}\,\mathrm{d}t$
- **C.** $\int_{1}^{3}2 \left(2 t^{2} + 3\right)^{2} \sqrt{16 t^{2} + 1}\,\mathrm{d}t$
- **D (correct).** $\int_{1}^{3}2 t^{2} \left(2 t^{2} + 3\right)^{2} \sqrt{16 t^{2} + 1}\,\mathrm{d}t$
- **E.** $\int_{1}^{3}t^{2} \left(4 t^{2} + 6\right) \sqrt{16 t^{2} + 1}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=2 t^{2} + 3.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle 2 t^{2} + 3,\,t\rangle,\quad 1\le t\le 3
$$

Note that the domain $1\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2} + 3)i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(4 t)i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(4 t)^2+1^2} \\ &=\sqrt{16 t^{2} + 1}\end{aligned}
$$

Now, if $f(x,y)=2 x^{2} y^{2},$ then we obtain

$$
\begin{aligned}f(r(t))&=2\left(2 t^{2} + 3\right)^{2}t^{2} \\ &=2 t^{2} \left(2 t^{2} + 3\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x^{2} y^{2}\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{1}^{3}(2 t^{2} \left(2 t^{2} + 3\right)^{2})\cdot \sqrt{16 t^{2} + 1}\,\mathrm{d}t \\ &=\int_{1}^{3}2 t^{2} \left(2 t^{2} + 3\right)^{2} \sqrt{16 t^{2} + 1}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Hard
Which of the following is equivalent to the integral $\int_C 4 x^{2} y\,\mathrm{d}s$

where $C$ is the section of the curve $x=2 y^{3} + 2$ traversed between the points $(4,1)$ and $(130,4)$.

*Hint: Use the parameter $y=t.$*

- **A (correct).** $\int_{1}^{4}4 t \left(2 t^{3} + 2\right)^{2} \sqrt{36 t^{4} + 1}\,\mathrm{d}t$
- **B.** $\int_{1}^{4}4 t \left(2 t^{3} + 2\right)^{2}\,\mathrm{d}t$
- **C.** $\int_{1}^{4}4 \left(2 t^{3} + 2\right)^{2} \sqrt{36 t^{4} + 1}\,\mathrm{d}t$
- **D.** $\int_{1}^{4}t \left(8 t^{3} + 8\right) \sqrt{36 t^{4} + 1}\,\mathrm{d}t$
- **E.** $\int_{1}^{4}4 t \left(2 t^{3} + 2\right)^{2} \sqrt{4 t^{4} + 1}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=2 t^{3} + 2.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle 2 t^{3} + 2,\,t\rangle,\quad 1\le t\le 4
$$

Note that the domain $1\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(2 t^{3} + 2)i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(6 t^{2})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(6 t^{2})^2+1^2} \\ &=\sqrt{36 t^{4} + 1}\end{aligned}
$$

Now, if $f(x,y)=4 x^{2} y,$ then we obtain

$$
\begin{aligned}f(r(t))&=4\left(2 t^{3} + 2\right)^{2}t^{1} \\ &=4 t \left(2 t^{3} + 2\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 4 x^{2} y\,\mathrm{d}s&=\int_{1}^{4}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{1}^{4}(4 t \left(2 t^{3} + 2\right)^{2})\cdot \sqrt{36 t^{4} + 1}\,\mathrm{d}t \\ &=\int_{1}^{4}4 t \left(2 t^{3} + 2\right)^{2} \sqrt{36 t^{4} + 1}\,\mathrm{d}t.\end{aligned}
$$

---

## Generated — authored normal — Hard
Which of the following is equivalent to the integral $\int_C 2 x^{2} y\,\mathrm{d}s$

where $C$ is the section of the curve $x=2 - 3 y^{3}$ traversed between the points $(2,0)$ and $(-79,3)$.

*Hint: Use the parameter $y=t.$*

- **A.** $\int_{0}^{3}2 t \left(2 - 3 t^{3}\right)^{2}\,\mathrm{d}t$
- **B.** $\int_{0}^{3}t \left(4 - 6 t^{3}\right) \sqrt{81 t^{4} + 1}\,\mathrm{d}t$
- **C.** $\int_{0}^{3}2 \left(2 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t$
- **D.** $\int_{0}^{3}2 t \left(2 - 3 t^{3}\right)^{2} \sqrt{9 t^{4} + 1}\,\mathrm{d}t$
- **E (correct).** $\int_{0}^{3}2 t \left(2 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t$

**Worked solution**

Notice that the given curve is of the form $x=x(y).$ Therefore, by setting $y=t,$ we have 

$$
x=x(t)=2 - 3 t^{3}.
$$

This gives the following parametrization of the curve:

$$
r(t)=\langle 2 - 3 t^{3},\,t\rangle,\quad 0\le t\le 3
$$

Note that the domain $0\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}r^{\prime}(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j \\ &=\frac{\mathrm{d}}{\mathrm{d}t}(2 - 3 t^{3})i+\frac{\mathrm{d}}{\mathrm{d}t}(t)j \\ &=(- 9 t^{2})i+j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &=\sqrt{(- 9 t^{2})^2+1^2} \\ &=\sqrt{81 t^{4} + 1}\end{aligned}
$$

Now, if $f(x,y)=2 x^{2} y,$ then we obtain

$$
\begin{aligned}f(r(t))&=2\left(2 - 3 t^{3}\right)^{2}t^{1} \\ &=2 t \left(2 - 3 t^{3}\right)^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x^{2} y\,\mathrm{d}s&=\int_{0}^{3}f(r(t))\|r^{\prime}(t)\|\,\mathrm{d}t \\ &=\int_{0}^{3}(2 t \left(2 - 3 t^{3}\right)^{2})\cdot \sqrt{81 t^{4} + 1}\,\mathrm{d}t \\ &=\int_{0}^{3}2 t \left(2 - 3 t^{3}\right)^{2} \sqrt{81 t^{4} + 1}\,\mathrm{d}t.\end{aligned}
$$
