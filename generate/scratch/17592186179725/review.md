# Originals and generated variants

Basis2275. Historical profiles are evidence-only. All options are complete mathematical values. Source notation normalization is distinguished from prose/stage fidelity.

## q-123128 / sum

### Original captured record

Which of the following is equivalent to the line integral of the function $f(x, y, z) = x + y + z$, traversed along the line segment from $(1, 0, 1)$ to $(2, 3, 0)$?

- $\sqrt{11}\displaystyle \int_{0}^{1}(2 + 3t)dt$
- $\sqrt{5}\displaystyle \int_{0}^{1}(1 - 2t)dt$
- $\sqrt{5}\displaystyle \int_{0}^{1}(1 - t)dt$
- $\sqrt{13}\displaystyle \int_{0}^{1}(1 + 2t)dt$
- $\sqrt{11}\displaystyle \int_{0}^{1}(1 + 3t)dt$

[No observed solution, rating or correct key.]

### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x, y, z) = x + y + z$, traversed along the line segment from $(1, 0, 1)$ to $(2, 3, 0)$?

- $\sqrt{11}{\int }_{0}^{1}(3 t + 2)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(1 - t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(1 - 2 t)\,\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(2 t + 1)\,\text{d}t$
- $\sqrt{11}{\int }_{0}^{1}(3 t + 1)\,\text{d}t$

[Source worked solution absent.]


### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x, y, z) = x + y + z$, traversed along the line segment from $(-2, 2, -3)$ to $(1, 0, -2)$?

- $2 \sqrt{5}{\int }_{0}^{1}(- t - 2)\,\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}(t - 2)\,\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}(- 3 t - 2)\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(2 t - 2)\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(2 t - 3)\,\text{d}t$

[Source worked solution absent.]


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x, y, z) = x + y + z$, traversed along the line segment from $(-4, 2, 3)$ to $(-3, -1, 1)$?

- $14{\int }_{0}^{1}(1 - 4 t)\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(1 - 4 t)\,\text{d}t$
- $1{\int }_{0}^{1}(1 - 4 t)\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(1 - t)\,\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}(1 - 4 t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-4,2,3)$ to $(-3,-1,1).$

The position vectors of the endpoints of our line segment are $a=(-4)\,i+(2)\,j+(3)\,k$ and $b=(-3)\,i+(-1)\,j+(1)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-4)\,i+(2)\,j+(3)\,k)+t[((-3)\,i+(-1)\,j+(1)\,k)-((-4)\,i+(2)\,j+(3)\,k)] \\   & =((-4)\,i+(2)\,j+(3)\,k)+t((1)\,i+(-3)\,j+(-2)\,k) \\   & =(t - 4)\,i+(2 - 3 t)\,j+(3 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t - 4,$ $y=2 - 3 t,$ and $z=3 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t - 4)i+\frac{\text{d}}{\text{d}t}(2 - 3 t)j+\frac{\text{d}}{\text{d}t}(3 - 2 t)k \\   & =(1)\,i+(-3)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(-3)^{2}+(-2)^{2}} \\   & =\sqrt{14}\end{aligned}
$$

Now, since $f(x,y,z)=x + y + z$, we obtain

$$
\begin{aligned}f(r(t)) & =(t - 4)+(2 - 3 t)+(3 - 2 t) \\   & =1 - 4 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(1 - 4 t)\cdot \sqrt{14}\cdot \text{d}t \\   & =\sqrt{14}{\int }_{0}^{1}(1 - 4 t)\,\text{d}t\end{aligned}
$$


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x, y, z) = x + y + z$, traversed along the line segment from $(-1, -2, 2)$ to $(-3, 1, 0)$?

- $\sqrt{13}{\int }_{0}^{1}(- t - 1)\,\text{d}t$
- $17{\int }_{0}^{1}(- t - 1)\,\text{d}t$
- $\sqrt{17}{\int }_{0}^{1}(- t - 1)\,\text{d}t$
- $1{\int }_{0}^{1}(- t - 1)\,\text{d}t$
- $\sqrt{17}{\int }_{0}^{1}(- 4 t - 1)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,-2,2)$ to $(-3,1,0).$

The position vectors of the endpoints of our line segment are $a=(-1)\,i+(-2)\,j+(2)\,k$ and $b=(-3)\,i+(1)\,j+(0)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-1)\,i+(-2)\,j+(2)\,k)+t[((-3)\,i+(1)\,j+(0)\,k)-((-1)\,i+(-2)\,j+(2)\,k)] \\   & =((-1)\,i+(-2)\,j+(2)\,k)+t((-2)\,i+(3)\,j+(-2)\,k) \\   & =(- 2 t - 1)\,i+(3 t - 2)\,j+(2 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=- 2 t - 1,$ $y=3 t - 2,$ and $z=2 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(- 2 t - 1)i+\frac{\text{d}}{\text{d}t}(3 t - 2)j+\frac{\text{d}}{\text{d}t}(2 - 2 t)k \\   & =(-2)\,i+(3)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-2)^{2}+(3)^{2}+(-2)^{2}} \\   & =\sqrt{17}\end{aligned}
$$

Now, since $f(x,y,z)=x + y + z$, we obtain

$$
\begin{aligned}f(r(t)) & =(- 2 t - 1)+(3 t - 2)+(2 - 2 t) \\   & =- t - 1\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- t - 1)\cdot \sqrt{17}\cdot \text{d}t \\   & =\sqrt{17}{\int }_{0}^{1}(- t - 1)\,\text{d}t\end{aligned}
$$


## q-123431 / quotient

### Original captured record

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\frac{y+z}{x},$ traversed along the line segment from $(-4,1,5)$ to $(-2,3,3)?$

- $6\sqrt{3}{\int }_{0}^{1}\frac{1}{{t}^{2}+2}\,\text{d}t$
- $2\sqrt{3}{\int }_{0}^{1}\frac{1}{2t-1}\,\text{d}t$
- $2\sqrt{3}{\int }_{0}^{1}\frac{t}{t-2}\,\text{d}t$
- $6\sqrt{3}{\int }_{0}^{1}\frac{1}{t-2}\,\text{d}t$
- $6\sqrt{3}{\int }_{0}^{1}\frac{2t+1}{t-1}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-4,1,5)$ to $(-2,3,3).$

The position vectors of the endpoints of our line segment are $a=-4i+j+5\,k$ and $b=-2\,i+3\,j+3\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-4i+j+5\,k)+t[(-2\,i+3\,j+3\,k)-(-4i+j+5\,k)] \\  & =(-4i+j+5\,k)+t(2i+2\,j-2\,k) \\  & =(2t-4)\,i+(2t+1)\,j+(5-2t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t-4,y=2t+1,$ and $z=5-2t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2t-4)i+\frac{\text{d}}{\text{d}t}(2t+1)j+\frac{\text{d}}{\text{d}t}(5-2t)k \\  & =2\,i+2\,j-2\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{2}^{2}+(-2)^{2}} \\  & =\sqrt{12} \\  & =2\sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y+z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(2t+1)+(5-2t)}{2t-4} \\  & =\frac{6}{2t-4} \\  & =\frac{3}{t-2}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\frac{3}{t-2}\cdot 2\sqrt{3}\cdot \text{d}t \\  & =6\sqrt{3}{\int }_{0}^{1}\frac{1}{t-2}\,\text{d}t.\end{aligned}
$$

### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\frac{y+z}{x},$ traversed along the line segment from $(-4,1,5)$ to $(-2,3,3)?$

- $6 \sqrt{3}{\int }_{0}^{1}(\frac{1}{t^{2} + 2})\,\text{d}t$
- $2 \sqrt{3}{\int }_{0}^{1}(\frac{t}{t - 2})\,\text{d}t$
- $2 \sqrt{3}{\int }_{0}^{1}(\frac{1}{2 t - 1})\,\text{d}t$
- $6 \sqrt{3}{\int }_{0}^{1}(\frac{1}{t - 2})\,\text{d}t$
- $6 \sqrt{3}{\int }_{0}^{1}(\frac{2 t + 1}{t - 1})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-4,1,5)$ to $(-2,3,3).$

The position vectors of the endpoints of our line segment are $a=(-4)\,i+(1)\,j+(5)\,k$ and $b=(-2)\,i+(3)\,j+(3)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-4)\,i+(1)\,j+(5)\,k)+t[((-2)\,i+(3)\,j+(3)\,k)-((-4)\,i+(1)\,j+(5)\,k)] \\   & =((-4)\,i+(1)\,j+(5)\,k)+t((2)\,i+(2)\,j+(-2)\,k) \\   & =(2 t - 4)\,i+(2 t + 1)\,j+(5 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t - 4,$ $y=2 t + 1,$ and $z=5 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t - 4)i+\frac{\text{d}}{\text{d}t}(2 t + 1)j+\frac{\text{d}}{\text{d}t}(5 - 2 t)k \\   & =(2)\,i+(2)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(2)^{2}+(-2)^{2}} \\   & =\sqrt{12} \\   & =2 \sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y+z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(2 t + 1)+(5 - 2 t)}{2 t - 4} \\   & =\frac{6}{2 t - 4} \\   & =\frac{3}{t - 2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\frac{3}{t - 2})\cdot 2 \sqrt{3}\cdot \text{d}t \\   & =6 \sqrt{3}{\int }_{0}^{1}(\frac{1}{t - 2})\,\text{d}t\end{aligned}
$$


### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\frac{y+z}{x},$ traversed along the line segment from $(2,-2,3)$ to $(3,-4,5)?$

- $3{\int }_{0}^{1}(\frac{t}{t + 2})\,\text{d}t$
- $3{\int }_{0}^{1}(\frac{1}{t^{2} - 2})\,\text{d}t$
- $3{\int }_{0}^{1}(\frac{1}{t + 2})\,\text{d}t$
- $3{\int }_{0}^{1}(\frac{t - 2}{t + 3})\,\text{d}t$
- $3{\int }_{0}^{1}(\frac{1}{t - 1})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-2,3)$ to $(3,-4,5).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(-2)\,j+(3)\,k$ and $b=(3)\,i+(-4)\,j+(5)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((2)\,i+(-2)\,j+(3)\,k)+t[((3)\,i+(-4)\,j+(5)\,k)-((2)\,i+(-2)\,j+(3)\,k)] \\   & =((2)\,i+(-2)\,j+(3)\,k)+t((1)\,i+(-2)\,j+(2)\,k) \\   & =(t + 2)\,i+(- 2 t - 2)\,j+(2 t + 3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t + 2,$ $y=- 2 t - 2,$ and $z=2 t + 3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t + 2)i+\frac{\text{d}}{\text{d}t}(- 2 t - 2)j+\frac{\text{d}}{\text{d}t}(2 t + 3)k \\   & =(1)\,i+(-2)\,j+(2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(-2)^{2}+(2)^{2}} \\   & =\sqrt{9} \\   & =3\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y+z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(- 2 t - 2)+(2 t + 3)}{t + 2} \\   & =\frac{1}{t + 2} \\   & =\frac{1}{t + 2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\frac{1}{t + 2})\cdot 3\cdot \text{d}t \\   & =3{\int }_{0}^{1}(\frac{1}{t + 2})\,\text{d}t\end{aligned}
$$


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\frac{y+z}{x},$ traversed along the line segment from $(3,4,5)$ to $(1,6,3)?$

- $2 \sqrt{3}{\int }_{0}^{1}(\frac{9 - 2 t}{3 - 2 t})\,\text{d}t$
- $12{\int }_{0}^{1}(- \frac{9}{2 t - 3})\,\text{d}t$
- $2 \sqrt{2}{\int }_{0}^{1}(- \frac{9}{2 t - 3})\,\text{d}t$
- $1{\int }_{0}^{1}(- \frac{9}{2 t - 3})\,\text{d}t$
- $2 \sqrt{3}{\int }_{0}^{1}(- \frac{9}{2 t - 3})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,4,5)$ to $(1,6,3).$

The position vectors of the endpoints of our line segment are $a=(3)\,i+(4)\,j+(5)\,k$ and $b=(1)\,i+(6)\,j+(3)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((3)\,i+(4)\,j+(5)\,k)+t[((1)\,i+(6)\,j+(3)\,k)-((3)\,i+(4)\,j+(5)\,k)] \\   & =((3)\,i+(4)\,j+(5)\,k)+t((-2)\,i+(2)\,j+(-2)\,k) \\   & =(3 - 2 t)\,i+(2 t + 4)\,j+(5 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3 - 2 t,$ $y=2 t + 4,$ and $z=5 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(3 - 2 t)i+\frac{\text{d}}{\text{d}t}(2 t + 4)j+\frac{\text{d}}{\text{d}t}(5 - 2 t)k \\   & =(-2)\,i+(2)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-2)^{2}+(2)^{2}+(-2)^{2}} \\   & =\sqrt{12} \\   & =2 \sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y+z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(2 t + 4)+(5 - 2 t)}{3 - 2 t} \\   & =\frac{9}{3 - 2 t} \\   & =- \frac{9}{2 t - 3}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- \frac{9}{2 t - 3})\cdot 2 \sqrt{3}\cdot \text{d}t \\   & =- 9 \sqrt{3}{\int }_{0}^{1}(\frac{1}{t - \frac{3}{2}})\,\text{d}t\end{aligned}
$$


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\frac{y+z}{x},$ traversed along the line segment from $(-6,0,2)$ to $(-7,-1,3)?$

- $1{\int }_{0}^{1}(- \frac{2}{t + 6})\,\text{d}t$
- $3{\int }_{0}^{1}(- \frac{2}{t + 6})\,\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(- \frac{2}{t + 6})\,\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(\frac{t + 2}{- t - 6})\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}(- \frac{2}{t + 6})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-6,0,2)$ to $(-7,-1,3).$

The position vectors of the endpoints of our line segment are $a=(-6)\,i+(0)\,j+(2)\,k$ and $b=(-7)\,i+(-1)\,j+(3)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-6)\,i+(0)\,j+(2)\,k)+t[((-7)\,i+(-1)\,j+(3)\,k)-((-6)\,i+(0)\,j+(2)\,k)] \\   & =((-6)\,i+(0)\,j+(2)\,k)+t((-1)\,i+(-1)\,j+(1)\,k) \\   & =(- t - 6)\,i+(- t)\,j+(t + 2)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=- t - 6,$ $y=- t,$ and $z=t + 2$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(- t - 6)i+\frac{\text{d}}{\text{d}t}(- t)j+\frac{\text{d}}{\text{d}t}(t + 2)k \\   & =(-1)\,i+(-1)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-1)^{2}+(-1)^{2}+(1)^{2}} \\   & =\sqrt{3} \\   & =\sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y+z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(- t)+(t + 2)}{- t - 6} \\   & =\frac{2}{- t - 6} \\   & =- \frac{2}{t + 6}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- \frac{2}{t + 6})\cdot \sqrt{3}\cdot \text{d}t \\   & =- 2 \sqrt{3}{\int }_{0}^{1}(\frac{1}{t + 6})\,\text{d}t\end{aligned}
$$


## q-123387 / radical

### Original captured record

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\sqrt{2x+y-z},$ traversed along the line segment from $(3,-2,3)$ to $(5,-1,7)?$

- $\sqrt{21}{\int }_{0}^{1}\sqrt{2t+1}\,\text{d}t$
- $\sqrt{21}{\int }_{0}^{1}\sqrt{{t}^{2}+2t+1}\,\text{d}t$
- $2\sqrt{5}{\int }_{0}^{1}t\sqrt{t-1}\,\text{d}t$
- $2\sqrt{5}{\int }_{0}^{1}\sqrt{5t-3}\,\text{d}t$
- $\sqrt{21}{\int }_{0}^{1}\sqrt{t+1}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,-2,3)$ to $(5,-1,7).$

The position vectors of the endpoints of our line segment are $a=3i-2\,j+3k$ and $b=5\,i-j+7\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(3i-2\,j+3k)+t[(5\,i-j+7\,k)-(3i-2\,j+3k)] \\  & =(3i-2\,j+3k)+t(2i+\,j+4k) \\  & =(2t+3)\,i+(t-2)\,j+(4t+3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t+3,y=t-2,$ and $z=4t+3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2t+3)i+\frac{\text{d}}{\text{d}t}(t-2)j+\frac{\text{d}}{\text{d}t}(4t+3)k \\  & =2i+j+4\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{1}^{2}+{4}^{2}} \\  & =\sqrt{21}\end{aligned}
$$

Now, since $f(x,y,z)=\sqrt{2x+y-z}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sqrt{2(2t+3)+(t-2)-(4t+3)} \\  & =\sqrt{t+1}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\sqrt{t+1}\cdot \sqrt{21}\cdot \text{d}t \\  & =\sqrt{21}{\int }_{0}^{1}\sqrt{t+1}\,\text{d}t.\end{aligned}
$$

### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\sqrt{2x+y-z},$ traversed along the line segment from $(3,-2,3)$ to $(5,-1,7)?$

- $\sqrt{21}{\int }_{0}^{1}(\sqrt{2 t + 1})\,\text{d}t$
- $2 \sqrt{5}{\int }_{0}^{1}(t \sqrt{t - 1})\,\text{d}t$
- $\sqrt{21}{\int }_{0}^{1}(\sqrt{t^{2} + 2 t + 1})\,\text{d}t$
- $2 \sqrt{5}{\int }_{0}^{1}(\sqrt{5 t - 3})\,\text{d}t$
- $\sqrt{21}{\int }_{0}^{1}(\sqrt{t + 1})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,-2,3)$ to $(5,-1,7).$

The position vectors of the endpoints of our line segment are $a=(3)\,i+(-2)\,j+(3)\,k$ and $b=(5)\,i+(-1)\,j+(7)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((3)\,i+(-2)\,j+(3)\,k)+t[((5)\,i+(-1)\,j+(7)\,k)-((3)\,i+(-2)\,j+(3)\,k)] \\   & =((3)\,i+(-2)\,j+(3)\,k)+t((2)\,i+(1)\,j+(4)\,k) \\   & =(2 t + 3)\,i+(t - 2)\,j+(4 t + 3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t + 3,$ $y=t - 2,$ and $z=4 t + 3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t + 3)i+\frac{\text{d}}{\text{d}t}(t - 2)j+\frac{\text{d}}{\text{d}t}(4 t + 3)k \\   & =(2)\,i+(1)\,j+(4)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(1)^{2}+(4)^{2}} \\   & =\sqrt{21}\end{aligned}
$$

Now, since $f(x,y,z)=\sqrt{2x+y-z}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sqrt{2(2 t + 3)+(t - 2)-(4 t + 3)} \\   & =\sqrt{t + 1}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\sqrt{t + 1})\cdot \sqrt{21}\cdot \text{d}t \\   & =\sqrt{21}{\int }_{0}^{1}(\sqrt{t + 1})\,\text{d}t\end{aligned}
$$


### Parameterized historical evidence

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\sqrt{2x+y-z},$ traversed along the line segment from $(-2,2,-3)$ to $(1,0,-2)?$

- $\sqrt{13}{\int }_{0}^{1}(\sqrt{7 t - 3})\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(\sqrt{9 t^{2} + 6 t + 1})\,\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(t \sqrt{3 t - 1})\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(\sqrt{3 t + 1})\,\text{d}t$
- $\sqrt{14}{\int }_{0}^{1}(\sqrt{6 t + 1})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-2,2,-3)$ to $(1,0,-2).$

The position vectors of the endpoints of our line segment are $a=(-2)\,i+(2)\,j+(-3)\,k$ and $b=(1)\,i+(0)\,j+(-2)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-2)\,i+(2)\,j+(-3)\,k)+t[((1)\,i+(0)\,j+(-2)\,k)-((-2)\,i+(2)\,j+(-3)\,k)] \\   & =((-2)\,i+(2)\,j+(-3)\,k)+t((3)\,i+(-2)\,j+(1)\,k) \\   & =(3 t - 2)\,i+(2 - 2 t)\,j+(t - 3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3 t - 2,$ $y=2 - 2 t,$ and $z=t - 3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(3 t - 2)i+\frac{\text{d}}{\text{d}t}(2 - 2 t)j+\frac{\text{d}}{\text{d}t}(t - 3)k \\   & =(3)\,i+(-2)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(3)^{2}+(-2)^{2}+(1)^{2}} \\   & =\sqrt{14}\end{aligned}
$$

Now, since $f(x,y,z)=\sqrt{2x+y-z}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sqrt{2(3 t - 2)+(2 - 2 t)-(t - 3)} \\   & =\sqrt{3 t + 1}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\sqrt{3 t + 1})\cdot \sqrt{14}\cdot \text{d}t \\   & =\sqrt{14}{\int }_{0}^{1}(\sqrt{3 t + 1})\,\text{d}t\end{aligned}
$$


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\sqrt{2x+y-z},$ traversed along the line segment from $(0,3,-2)$ to $(2,2,0)?$

- $3{\int }_{0}^{1}(\sqrt{2 t + 5})\,\text{d}t$
- $3{\int }_{0}^{1}(\sqrt{t + 5})\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(\sqrt{t + 5})\,\text{d}t$
- $1{\int }_{0}^{1}(\sqrt{t + 5})\,\text{d}t$
- $9{\int }_{0}^{1}(\sqrt{t + 5})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,3,-2)$ to $(2,2,0).$

The position vectors of the endpoints of our line segment are $a=(0)\,i+(3)\,j+(-2)\,k$ and $b=(2)\,i+(2)\,j+(0)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((0)\,i+(3)\,j+(-2)\,k)+t[((2)\,i+(2)\,j+(0)\,k)-((0)\,i+(3)\,j+(-2)\,k)] \\   & =((0)\,i+(3)\,j+(-2)\,k)+t((2)\,i+(-1)\,j+(2)\,k) \\   & =(2 t)\,i+(3 - t)\,j+(2 t - 2)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t,$ $y=3 - t,$ and $z=2 t - 2$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t)i+\frac{\text{d}}{\text{d}t}(3 - t)j+\frac{\text{d}}{\text{d}t}(2 t - 2)k \\   & =(2)\,i+(-1)\,j+(2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(-1)^{2}+(2)^{2}} \\   & =3\end{aligned}
$$

Now, since $f(x,y,z)=\sqrt{2x+y-z}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sqrt{2(2 t)+(3 - t)-(2 t - 2)} \\   & =\sqrt{t + 5}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\sqrt{t + 5})\cdot 3\cdot \text{d}t \\   & =3{\int }_{0}^{1}(\sqrt{t + 5})\,\text{d}t\end{aligned}
$$


### Generated method-bank learner variant

Which of the following is equivalent to the line integral of the function $f(x,y,z)=\sqrt{2x+y-z},$ traversed along the line segment from $(0,0,-3)$ to $(1,1,-4)?$

- $1{\int }_{0}^{1}(\sqrt{4 t + 3})\,\text{d}t$
- $3{\int }_{0}^{1}(\sqrt{4 t + 3})\,\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(\sqrt{3 t + 3})\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}(\sqrt{4 t + 3})\,\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(\sqrt{4 t + 3})\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0,-3)$ to $(1,1,-4).$

The position vectors of the endpoints of our line segment are $a=(0)\,i+(0)\,j+(-3)\,k$ and $b=(1)\,i+(1)\,j+(-4)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((0)\,i+(0)\,j+(-3)\,k)+t[((1)\,i+(1)\,j+(-4)\,k)-((0)\,i+(0)\,j+(-3)\,k)] \\   & =((0)\,i+(0)\,j+(-3)\,k)+t((1)\,i+(1)\,j+(-1)\,k) \\   & =(t)\,i+(t)\,j+(- t - 3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t,$ $y=t,$ and $z=- t - 3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j+\frac{\text{d}}{\text{d}t}(- t - 3)k \\   & =(1)\,i+(1)\,j+(-1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(1)^{2}+(-1)^{2}} \\   & =\sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=\sqrt{2x+y-z}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sqrt{2(t)+(t)-(- t - 3)} \\   & =\sqrt{4 t + 3}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\sqrt{4 t + 3})\cdot \sqrt{3}\cdot \text{d}t \\   & =\sqrt{3}{\int }_{0}^{1}(\sqrt{4 t + 3})\,\text{d}t\end{aligned}
$$


## q-76569 / polynomial

### Original captured record

Evaluate the integral ${\int }_{C}x{y}^{2}\,\text{d}s$ along the line segment from $(1,2,0)$ to $(2,1,3).$

- $13\sqrt{11}$
- $\frac{13\sqrt{11}}{4}$
- $\frac{\sqrt{13}}{4}$
- $\frac{\sqrt{11}}{4}$
- $\frac{13}{4}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from$(1,2,0)$ to $(2,1,3).$

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=2\,i+j+3\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+2\,j)+t[(2\,i+j+3\,k)-(i+2\,j)] \\  & =(i+2\,j)+t(i-j+3\,k) \\  & =(1+t)\,i+(2-t)\,j+3t\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1+t,$ $y=2-t,$ and $z=3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(1+t)i+\frac{\text{d}}{\text{d}t}(2-t)j+\frac{\text{d}}{\text{d}t}(3t)k \\  & =i-j+3\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(-1)^{2}+{3}^{2}} \\  & =\sqrt{11}\end{aligned}
$$

Now, since $f(x,y,z)=x{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =(1+t)(2-t)^{2} \\  & ={t}^{3}-3{t}^{2}+4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{y}^{2}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}({t}^{3}-3{t}^{2}+4)\cdot \sqrt{11}\,\text{d}t \\  & =\sqrt{11}{\int }_{0}^{1}({t}^{3}-3{t}^{2}+4)\,\text{d}t \\  & =\sqrt{11}{[\frac{{t}^{4}}{4}-{t}^{3}+4t]}_{0}^{1} \\  & =\sqrt{11}(\frac{1}{4}-1+4)-0 \\  & =\frac{13\sqrt{11}}{4}.\end{aligned}
$$

### Parameterized historical evidence

Evaluate the integral ${\int }_{C}x{y}^{2}\,\text{d}s$ along the line segment from $(1,2,0)$ to $(2,1,3).$

- $13 \sqrt{11}$
- $\frac{\sqrt{13}}{4}$
- $\frac{13 \sqrt{11}}{4}$
- $\frac{\sqrt{11}}{4}$
- $\frac{13}{4}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,2,0)$ to $(2,1,3).$

The position vectors of the endpoints of our line segment are $a=(1)\,i+(2)\,j+(0)\,k$ and $b=(2)\,i+(1)\,j+(3)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((1)\,i+(2)\,j+(0)\,k)+t[((2)\,i+(1)\,j+(3)\,k)-((1)\,i+(2)\,j+(0)\,k)] \\   & =((1)\,i+(2)\,j+(0)\,k)+t((1)\,i+(-1)\,j+(3)\,k) \\   & =(t + 1)\,i+(2 - t)\,j+(3 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t + 1,$ $y=2 - t,$ and $z=3 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t + 1)i+\frac{\text{d}}{\text{d}t}(2 - t)j+\frac{\text{d}}{\text{d}t}(3 t)k \\   & =(1)\,i+(-1)\,j+(3)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(-1)^{2}+(3)^{2}} \\   & =\sqrt{11}\end{aligned}
$$

Now, since $f(x,y,z)=x{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =(t + 1)(2 - t)^{2} \\   & =t^{3} - 3 t^{2} + 4\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{y}^{2}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(t^{3} - 3 t^{2} + 4)\cdot \sqrt{11}\cdot \text{d}t \\   & =\sqrt{11}{\int }_{0}^{1}(t^{3} - 3 t^{2} + 4)\,\text{d}t \\   & =\sqrt{11}\left[(\frac{t^{4}}{4})+(- t^{3})+(4 t)\right]_{0}^{1} \\   & =\sqrt{11}((\frac{1}{4})+(-1)+(4))-\sqrt{11}((0)+(0)+(0)) \\   & =\frac{13 \sqrt{11}}{4}.\end{aligned}
$$


### Parameterized historical evidence

Evaluate the integral ${\int }_{C}x{y}^{2}\,\text{d}s$ along the line segment from $(3,3,-1)$ to $(2,4,-4).$

- $\frac{121 \sqrt{11}}{4}$
- $\frac{\sqrt{13}}{4}$
- $\frac{\sqrt{11}}{4}$
- $\frac{121}{4}$
- $121 \sqrt{11}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,3,-1)$ to $(2,4,-4).$

The position vectors of the endpoints of our line segment are $a=(3)\,i+(3)\,j+(-1)\,k$ and $b=(2)\,i+(4)\,j+(-4)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((3)\,i+(3)\,j+(-1)\,k)+t[((2)\,i+(4)\,j+(-4)\,k)-((3)\,i+(3)\,j+(-1)\,k)] \\   & =((3)\,i+(3)\,j+(-1)\,k)+t((-1)\,i+(1)\,j+(-3)\,k) \\   & =(3 - t)\,i+(t + 3)\,j+(- 3 t - 1)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3 - t,$ $y=t + 3,$ and $z=- 3 t - 1$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(3 - t)i+\frac{\text{d}}{\text{d}t}(t + 3)j+\frac{\text{d}}{\text{d}t}(- 3 t - 1)k \\   & =(-1)\,i+(1)\,j+(-3)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-1)^{2}+(1)^{2}+(-3)^{2}} \\   & =\sqrt{11}\end{aligned}
$$

Now, since $f(x,y,z)=x{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =(3 - t)(t + 3)^{2} \\   & =- t^{3} - 3 t^{2} + 9 t + 27\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{y}^{2}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- t^{3} - 3 t^{2} + 9 t + 27)\cdot \sqrt{11}\cdot \text{d}t \\   & =\sqrt{11}{\int }_{0}^{1}(- t^{3} - 3 t^{2} + 9 t + 27)\,\text{d}t \\   & =\sqrt{11}\left[(- \frac{t^{4}}{4})+(- t^{3})+(\frac{9 t^{2}}{2})+(27 t)\right]_{0}^{1} \\   & =\sqrt{11}((- \frac{1}{4})+(-1)+(\frac{9}{2})+(27))-\sqrt{11}((0)+(0)+(0)+(0)) \\   & =\frac{121 \sqrt{11}}{4}.\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}x{y}^{2}\,\text{d}s$ along the line segment from $(4,3,2)$ to $(2,1,4).$

- $\frac{43}{3}$
- $\frac{104 \sqrt{3}}{3}$
- $\frac{86 \sqrt{3}}{3}$
- $172$
- $\frac{38 \sqrt{3}}{3}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(4,3,2)$ to $(2,1,4).$

The position vectors of the endpoints of our line segment are $a=(4)\,i+(3)\,j+(2)\,k$ and $b=(2)\,i+(1)\,j+(4)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((4)\,i+(3)\,j+(2)\,k)+t[((2)\,i+(1)\,j+(4)\,k)-((4)\,i+(3)\,j+(2)\,k)] \\   & =((4)\,i+(3)\,j+(2)\,k)+t((-2)\,i+(-2)\,j+(2)\,k) \\   & =(4 - 2 t)\,i+(3 - 2 t)\,j+(2 t + 2)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4 - 2 t,$ $y=3 - 2 t,$ and $z=2 t + 2$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(4 - 2 t)i+\frac{\text{d}}{\text{d}t}(3 - 2 t)j+\frac{\text{d}}{\text{d}t}(2 t + 2)k \\   & =(-2)\,i+(-2)\,j+(2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-2)^{2}+(-2)^{2}+(2)^{2}} \\   & =2 \sqrt{3}\end{aligned}
$$

Now, since $f(x,y,z)=x{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4 - 2 t)(3 - 2 t)^{2} \\   & =(4 - 2 t)((4 t^{2})+(- 12 t)+(9)) \\   & =(4 - 2 t)(4 t^{2})+(4 - 2 t)(- 12 t)+(4 - 2 t)(9) \\   & =- 8 t^{3} + 40 t^{2} - 66 t + 36\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{y}^{2}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- 8 t^{3} + 40 t^{2} - 66 t + 36)\cdot 2 \sqrt{3}\cdot \text{d}t \\   & =2 \sqrt{3}{\int }_{0}^{1}(- 8 t^{3} + 40 t^{2} - 66 t + 36)\,\text{d}t \\   & =2 \sqrt{3}\left[(- 2 t^{4})+(\frac{40 t^{3}}{3})+(- 33 t^{2})+(36 t)\right]_{0}^{1} \\   & =2 \sqrt{3}((-2)+(\frac{40}{3})+(-33)+(36))-2 \sqrt{3}((0)+(0)+(0)+(0)) \\   & =\frac{86 \sqrt{3}}{3}.\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}x{y}^{2}\,\text{d}s$ along the line segment from $(4,4,-2)$ to $(2,2,-1).$

- $28$
- $90$
- $270$
- $112$
- $30$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(4,4,-2)$ to $(2,2,-1).$

The position vectors of the endpoints of our line segment are $a=(4)\,i+(4)\,j+(-2)\,k$ and $b=(2)\,i+(2)\,j+(-1)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((4)\,i+(4)\,j+(-2)\,k)+t[((2)\,i+(2)\,j+(-1)\,k)-((4)\,i+(4)\,j+(-2)\,k)] \\   & =((4)\,i+(4)\,j+(-2)\,k)+t((-2)\,i+(-2)\,j+(1)\,k) \\   & =(4 - 2 t)\,i+(4 - 2 t)\,j+(t - 2)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4 - 2 t,$ $y=4 - 2 t,$ and $z=t - 2$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(4 - 2 t)i+\frac{\text{d}}{\text{d}t}(4 - 2 t)j+\frac{\text{d}}{\text{d}t}(t - 2)k \\   & =(-2)\,i+(-2)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-2)^{2}+(-2)^{2}+(1)^{2}} \\   & =3\end{aligned}
$$

Now, since $f(x,y,z)=x{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4 - 2 t)(4 - 2 t)^{2} \\   & =(4 - 2 t)((4 t^{2})+(- 16 t)+(16)) \\   & =(4 - 2 t)(4 t^{2})+(4 - 2 t)(- 16 t)+(4 - 2 t)(16) \\   & =- 8 t^{3} + 48 t^{2} - 96 t + 64\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{y}^{2}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(- 8 t^{3} + 48 t^{2} - 96 t + 64)\cdot 3\cdot \text{d}t \\   & =3{\int }_{0}^{1}(- 8 t^{3} + 48 t^{2} - 96 t + 64)\,\text{d}t \\   & =3\left[(- 2 t^{4})+(16 t^{3})+(- 48 t^{2})+(64 t)\right]_{0}^{1} \\   & =3((-2)+(16)+(-48)+(64))-3((0)+(0)+(0)+(0)) \\   & =90.\end{aligned}
$$


## q-123434 / exponential

### Original captured record

Evaluate the integral ${\int }_{C}x{e}^{yz}\,\text{d}s$ along the line segment from $(2,-2,4)$ to $(4,-1,5).$

- $\frac{\sqrt{3}({e}^{3}+2)}{{e}^{8}}$
- $\frac{\sqrt{6}({e}^{2}-1)}{{e}^{3}}$
- $\frac{\sqrt{6}({e}^{3}-1)}{{e}^{8}}$
- $\frac{{e}^{3}-1}{{e}^{8}}$
- $\frac{{e}^{3}+1}{{e}^{5}}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-2,4)$ to $(4,-1,5).$ 

The position vectors of the endpoints of our line segment are $a=2\,i-2\,j+4\,k$ and $b=4\,i-\,j+5\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i-2\,j+4\,k)+t[(4\,i-\,j+5\,k)-(2\,i-2\,j+4\,k)] \\  & =(2\,i-2\,j+4\,k)+t(2\,i+j+k) \\  & =(2t+2)\,i+(t-2)\,j+(t+4)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t+2,$ $y=t-2,$ and $z=t+4$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2t+2)i+\frac{\text{d}}{\text{d}t}(t-2)j+\frac{\text{d}}{\text{d}t}(t+4)k \\  & =2\,i+j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{6}\end{aligned}
$$

Now, since $f(x,y,z)=x{e}^{yz}$, we obtain

$$
\begin{aligned}f(r(t)) & =(2t+2){e}^{(t-2)(t+4)} \\  & =(2t+2){e}^{{t}^{2}+2t-8}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{e}^{yz}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2t+2){e}^{{t}^{2}+2t-8}\cdot \sqrt{6}\cdot \text{d}t \\  & =\sqrt{6}{\int }_{0}^{1}(2t+2){e}^{{t}^{2}+2t-8}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u={t}^{2}+2t-8$, $\text{d}u=(2t+2)\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{6}{\int }_{0}^{1}(2t+2){e}^{{t}^{2}+2t-8}\,\text{d}t & =\sqrt{6}\,{\int }_{-8}^{-5}{e}^{u}\,\text{d}u \\  & =\sqrt{6}\,{e}^{u}\,{|}_{-8}^{-5} \\  & =\sqrt{6}({e}^{-5}-{e}^{-8}) \\  & =\sqrt{6}(\frac{1}{{e}^{5}}-\frac{1}{{e}^{8}}) \\  & =\frac{\sqrt{6}({e}^{3}-1)}{{e}^{8}}\end{aligned}
$$

### Parameterized historical evidence

Evaluate the integral ${\int }_{C}x{e}^{yz}\,\text{d}s$ along the line segment from $(2,-2,4)$ to $(4,-1,5).$

- $\frac{\sqrt{3} \left(2 + e^{3}\right)}{e^{8}}$
- $- \frac{\sqrt{6} \left(1 - e^{3}\right)}{e^{8}}$
- $- \frac{\sqrt{6} \left(1 - e^{2}\right)}{e^{3}}$
- $- \frac{1 - e^{3}}{e^{8}}$
- $\frac{1 + e^{3}}{e^{5}}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-2,4)$ to $(4,-1,5).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(-2)\,j+(4)\,k$ and $b=(4)\,i+(-1)\,j+(5)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((2)\,i+(-2)\,j+(4)\,k)+t[((4)\,i+(-1)\,j+(5)\,k)-((2)\,i+(-2)\,j+(4)\,k)] \\   & =((2)\,i+(-2)\,j+(4)\,k)+t((2)\,i+(1)\,j+(1)\,k) \\   & =(2 t + 2)\,i+(t - 2)\,j+(t + 4)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t + 2,$ $y=t - 2,$ and $z=t + 4$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t + 2)i+\frac{\text{d}}{\text{d}t}(t - 2)j+\frac{\text{d}}{\text{d}t}(t + 4)k \\   & =(2)\,i+(1)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(1)^{2}+(1)^{2}} \\   & =\sqrt{6}\end{aligned}
$$

Now, since $f(x,y,z)=x{e}^{yz}$, we obtain

$$
\begin{aligned}f(r(t)) & =(2 t + 2){e}^{(t - 2)(t + 4)} \\   & =\left(2 t + 2\right) e^{t^{2} + 2 t - 8}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{e}^{yz}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\left(2 t + 2\right) e^{t^{2} + 2 t - 8})\cdot \sqrt{6}\cdot \text{d}t \\   & =\sqrt{6}{\int }_{0}^{1}(\left(2 t + 2\right) e^{t^{2} + 2 t - 8})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{2} + 2 t - 8$, $\text{d}u=(2 t + 2)\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{6}{\int }_{0}^{1}(\left(2 t + 2\right) e^{t^{2} + 2 t - 8})\,\text{d}t & =\sqrt{6}\,{\int }_{-8}^{-5}{e}^{u}\,\text{d}u \\   & =\sqrt{6}\,{e}^{u}\,{|}_{-8}^{-5} \\   & =\sqrt{6}({e}^{-5}-{e}^{-8}) \\   & =\sqrt{6}(\frac{1}{{e}^{5}}-\frac{1}{{e}^{8}}) \\   & =\sqrt{6}\frac{{e}^{3}-1}{{e}^{8}}\end{aligned}
$$


### Parameterized historical evidence

Evaluate the integral ${\int }_{C}x{e}^{yz}\,\text{d}s$ along the line segment from $(2,-2,6)$ to $(6,-1,8).$

- $- \frac{\sqrt{21} \left(1 - e^{3}\right)}{e^{4}}$
- $\frac{1 + e^{4}}{e^{8}}$
- $- \frac{\sqrt{21} \left(1 - e^{4}\right)}{e^{12}}$
- $\frac{\sqrt{42} \left(2 + e^{4}\right)}{2 e^{12}}$
- $- \frac{1 - e^{4}}{e^{12}}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-2,6)$ to $(6,-1,8).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(-2)\,j+(6)\,k$ and $b=(6)\,i+(-1)\,j+(8)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((2)\,i+(-2)\,j+(6)\,k)+t[((6)\,i+(-1)\,j+(8)\,k)-((2)\,i+(-2)\,j+(6)\,k)] \\   & =((2)\,i+(-2)\,j+(6)\,k)+t((4)\,i+(1)\,j+(2)\,k) \\   & =(4 t + 2)\,i+(t - 2)\,j+(2 t + 6)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4 t + 2,$ $y=t - 2,$ and $z=2 t + 6$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(4 t + 2)i+\frac{\text{d}}{\text{d}t}(t - 2)j+\frac{\text{d}}{\text{d}t}(2 t + 6)k \\   & =(4)\,i+(1)\,j+(2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(4)^{2}+(1)^{2}+(2)^{2}} \\   & =\sqrt{21}\end{aligned}
$$

Now, since $f(x,y,z)=x{e}^{yz}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4 t + 2){e}^{(t - 2)(2 t + 6)} \\   & =\left(4 t + 2\right) e^{2 t^{2} + 2 t - 12}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{e}^{yz}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\left(4 t + 2\right) e^{2 t^{2} + 2 t - 12})\cdot \sqrt{21}\cdot \text{d}t \\   & =\sqrt{21}{\int }_{0}^{1}(\left(4 t + 2\right) e^{2 t^{2} + 2 t - 12})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=2 t^{2} + 2 t - 12$, $\text{d}u=(4 t + 2)\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{21}{\int }_{0}^{1}(\left(4 t + 2\right) e^{2 t^{2} + 2 t - 12})\,\text{d}t & =\sqrt{21}\,{\int }_{-12}^{-8}{e}^{u}\,\text{d}u \\   & =\sqrt{21}\,{e}^{u}\,{|}_{-12}^{-8} \\   & =\sqrt{21}({e}^{-8}-{e}^{-12}) \\   & =\sqrt{21}(\frac{1}{{e}^{8}}-\frac{1}{{e}^{12}}) \\   & =\sqrt{21}\frac{{e}^{4}-1}{{e}^{12}}\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}x{e}^{yz}\,\text{d}s$ along the line segment from $(1,-3,4)$ to $(3,-2,5).$

- $\frac{\sqrt{6} \left(1 + e^{2}\right)}{e^{12}}$
- $- \frac{\sqrt{6} \left(1 - e^{2}\right)}{e^{12}}$
- $- \frac{1 - e^{2}}{e^{12}}$
- $\frac{\sqrt{6}}{e^{10}}$
- $- \frac{\sqrt{6} \left(1 - e^{2}\right)}{2 e^{12}}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,-3,4)$ to $(3,-2,5).$

The position vectors of the endpoints of our line segment are $a=(1)\,i+(-3)\,j+(4)\,k$ and $b=(3)\,i+(-2)\,j+(5)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((1)\,i+(-3)\,j+(4)\,k)+t[((3)\,i+(-2)\,j+(5)\,k)-((1)\,i+(-3)\,j+(4)\,k)] \\   & =((1)\,i+(-3)\,j+(4)\,k)+t((2)\,i+(1)\,j+(1)\,k) \\   & =(2 t + 1)\,i+(t - 3)\,j+(t + 4)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t + 1,$ $y=t - 3,$ and $z=t + 4$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t + 1)i+\frac{\text{d}}{\text{d}t}(t - 3)j+\frac{\text{d}}{\text{d}t}(t + 4)k \\   & =(2)\,i+(1)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(1)^{2}+(1)^{2}} \\   & =\sqrt{6}\end{aligned}
$$

Now, since $f(x,y,z)=x{e}^{yz}$, we obtain

$$
\begin{aligned}f(r(t)) & =(2 t + 1){e}^{(t - 3)(t + 4)} \\   & =\left(2 t + 1\right) e^{t^{2} + t - 12}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{e}^{yz}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 12})\cdot \sqrt{6}\cdot \text{d}t \\   & =\sqrt{6}{\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 12})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{2} + t - 12$, $\text{d}u=(2 t + 1)\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{6}{\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 12})\,\text{d}t & =\sqrt{6}\,{\int }_{-12}^{-10}{e}^{u}\,\text{d}u \\   & =\sqrt{6}\,{e}^{u}\,{|}_{-12}^{-10} \\   & =\sqrt{6}({e}^{-10}-{e}^{-12}) \\   & =\sqrt{6}(\frac{1}{{e}^{10}}-\frac{1}{{e}^{12}}) \\   & =\sqrt{6}\frac{{e}^{2}-1}{{e}^{12}}\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}x{e}^{yz}\,\text{d}s$ along the line segment from $(1,-4,5)$ to $(3,-3,6).$

- $\frac{\sqrt{6} \left(1 + e^{2}\right)}{e^{20}}$
- $- \frac{\sqrt{6} \left(1 - e^{2}\right)}{2 e^{20}}$
- $- \frac{1 - e^{2}}{e^{20}}$
- $\frac{\sqrt{6}}{e^{18}}$
- $- \frac{\sqrt{6} \left(1 - e^{2}\right)}{e^{20}}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,-4,5)$ to $(3,-3,6).$

The position vectors of the endpoints of our line segment are $a=(1)\,i+(-4)\,j+(5)\,k$ and $b=(3)\,i+(-3)\,j+(6)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((1)\,i+(-4)\,j+(5)\,k)+t[((3)\,i+(-3)\,j+(6)\,k)-((1)\,i+(-4)\,j+(5)\,k)] \\   & =((1)\,i+(-4)\,j+(5)\,k)+t((2)\,i+(1)\,j+(1)\,k) \\   & =(2 t + 1)\,i+(t - 4)\,j+(t + 5)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t + 1,$ $y=t - 4,$ and $z=t + 5$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t + 1)i+\frac{\text{d}}{\text{d}t}(t - 4)j+\frac{\text{d}}{\text{d}t}(t + 5)k \\   & =(2)\,i+(1)\,j+(1)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(1)^{2}+(1)^{2}} \\   & =\sqrt{6}\end{aligned}
$$

Now, since $f(x,y,z)=x{e}^{yz}$, we obtain

$$
\begin{aligned}f(r(t)) & =(2 t + 1){e}^{(t - 4)(t + 5)} \\   & =\left(2 t + 1\right) e^{t^{2} + t - 20}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}x{e}^{yz}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 20})\cdot \sqrt{6}\cdot \text{d}t \\   & =\sqrt{6}{\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 20})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{2} + t - 20$, $\text{d}u=(2 t + 1)\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{6}{\int }_{0}^{1}(\left(2 t + 1\right) e^{t^{2} + t - 20})\,\text{d}t & =\sqrt{6}\,{\int }_{-20}^{-18}{e}^{u}\,\text{d}u \\   & =\sqrt{6}\,{e}^{u}\,{|}_{-20}^{-18} \\   & =\sqrt{6}({e}^{-18}-{e}^{-20}) \\   & =\sqrt{6}(\frac{1}{{e}^{18}}-\frac{1}{{e}^{20}}) \\   & =\sqrt{6}\frac{{e}^{2}-1}{{e}^{20}}\end{aligned}
$$


## q-76577 / cosine

### Original captured record

Evaluate the integral ${\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s$ along the line segment from $(-1,2,1)$ to $(1,2,5).$

- $-\frac{4\sqrt{5}}{3\pi }$
- $-\frac{2\sqrt{5}}{3\pi }$
- $-\frac{4\sqrt{3}}{5\pi }$
- $\frac{4\sqrt{5}}{\pi }$
- $\frac{\sqrt{5}}{3\pi }$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,2,1)$ to $(1,2,5).$ 

The position vectors of the endpoints of our line segment are $a=-i+2\,j+k$ and $b=i+2\,j+5\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-i+2\,j+k)+t[(i+2\,j+5\,k)-(-i+2\,j+k)] \\  & =(-i+2\,j+k)+t(2\,i+4\,k) \\  & =(-1+2t)\,i+2\,j+(1+4t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-1+2t,$ $y=2,$ and $z=1+4t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(-1+2t)i+\frac{\text{d}}{\text{d}t}(2)j+\frac{\text{d}}{\text{d}t}(1+4t)k \\  & =2\,i+0+4\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{0}^{2}+{4}^{2}} \\  & =\sqrt{20} \\  & =2\sqrt{5}\end{aligned}
$$

Now, since $f(x,y,z)=\operatorname{cos}⁡(\frac{\pi }{4}(x+z))$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡(\frac{\pi }{4}((-1+2t)+(1+4t))) \\  & =\operatorname{cos}⁡(\frac{3\pi t}{2}).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{cos}⁡(\frac{3\pi t}{2})\cdot 2\sqrt{5}\cdot \text{d}t \\  & =2\sqrt{5}{\int }_{0}^{1}\operatorname{cos}⁡(\frac{3\pi t}{2})\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=\frac{3\pi t}{2}$, $\text{d}u=\frac{3\pi }{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}2\sqrt{5}{\int }_{0}^{1}\operatorname{cos}⁡(\frac{3\pi t}{2})\,\text{d}t & =\frac{4\sqrt{5}}{3\pi }{\int }_{0}^{3\pi /2}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{4\sqrt{5}}{3\pi }\operatorname{sin}⁡u\,{|}_{0}^{3\pi /2} \\  & =\frac{4\sqrt{5}}{3\pi }(\operatorname{sin}⁡(\frac{3\pi }{2})-\operatorname{sin}⁡(0)) \\  & =\frac{4\sqrt{5}}{3\pi }(-1-0) \\  & =-\frac{4\sqrt{5}}{3\pi }\end{aligned}
$$

### Parameterized historical evidence

Evaluate the integral ${\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s$ along the line segment from $(-1,2,1)$ to $(1,2,5).$

- $- \frac{4 \sqrt{5}}{3 \pi}$
- $- \frac{4 \sqrt{3}}{5 \pi}$
- $- \frac{2 \sqrt{5}}{3 \pi}$
- $\frac{4 \sqrt{5}}{\pi}$
- $\frac{\sqrt{5}}{3 \pi}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,2,1)$ to $(1,2,5).$

The position vectors of the endpoints of our line segment are $a=(-1)\,i+(2)\,j+(1)\,k$ and $b=(1)\,i+(2)\,j+(5)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-1)\,i+(2)\,j+(1)\,k)+t[((1)\,i+(2)\,j+(5)\,k)-((-1)\,i+(2)\,j+(1)\,k)] \\   & =((-1)\,i+(2)\,j+(1)\,k)+t((2)\,i+(0)\,j+(4)\,k) \\   & =(2 t - 1)\,i+(2)\,j+(4 t + 1)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 t - 1,$ $y=2,$ and $z=4 t + 1$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(2 t - 1)i+\frac{\text{d}}{\text{d}t}(2)j+\frac{\text{d}}{\text{d}t}(4 t + 1)k \\   & =(2)\,i+(0)\,j+(4)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(2)^{2}+(0)^{2}+(4)^{2}} \\   & =\sqrt{20} \\   & =2 \sqrt{5}\end{aligned}
$$

Now, since $f(x,y,z)=\operatorname{cos}⁡(\frac{\pi }{4}(x+z))$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡(\frac{\pi }{4}((2 t - 1)+(4 t + 1))) \\   & =\cos{\left(\frac{3 \pi t}{2} \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{2} \right)})\cdot 2 \sqrt{5}\cdot \text{d}t \\   & =2 \sqrt{5}{\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{2} \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=\frac{3 \pi t}{2}$, $\text{d}u=(\frac{3 \pi}{2})\,\text{d}t$ as follows: 

$$
\begin{aligned}2 \sqrt{5}{\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{2} \right)})\,\text{d}t & =\frac{4 \sqrt{5}}{3 \pi}{\int }_{0}^{\frac{3 \pi}{2}}\operatorname{cos}⁡u\,\text{d}u \\   & =\frac{4 \sqrt{5}}{3 \pi}(\operatorname{sin}⁡u)\,{|}_{0}^{\frac{3 \pi}{2}} \\   & =\frac{4 \sqrt{5}}{3 \pi}(\operatorname{sin}⁡(\frac{3 \pi}{2})-\operatorname{sin}⁡(0)) \\   & =\frac{4 \sqrt{5}}{3 \pi}((-1)-(0)) \\   & =- \frac{4 \sqrt{5}}{3 \pi}\end{aligned}
$$


### Parameterized historical evidence

Evaluate the integral ${\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s$ along the line segment from $(3,1,-3)$ to $(0,0,-5).$

- $\frac{\sqrt{7}}{5 \pi}$
- $\frac{\sqrt{6}}{3 \pi}$
- $- \frac{4 \sqrt{7}}{5 \pi}$
- $\frac{2 \sqrt{14}}{\pi}$
- $- \frac{2 \sqrt{7}}{5 \pi}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,1,-3)$ to $(0,0,-5).$

The position vectors of the endpoints of our line segment are $a=(3)\,i+(1)\,j+(-3)\,k$ and $b=(0)\,i+(0)\,j+(-5)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((3)\,i+(1)\,j+(-3)\,k)+t[((0)\,i+(0)\,j+(-5)\,k)-((3)\,i+(1)\,j+(-3)\,k)] \\   & =((3)\,i+(1)\,j+(-3)\,k)+t((-3)\,i+(-1)\,j+(-2)\,k) \\   & =(3 - 3 t)\,i+(1 - t)\,j+(- 2 t - 3)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3 - 3 t,$ $y=1 - t,$ and $z=- 2 t - 3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(3 - 3 t)i+\frac{\text{d}}{\text{d}t}(1 - t)j+\frac{\text{d}}{\text{d}t}(- 2 t - 3)k \\   & =(-3)\,i+(-1)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(-3)^{2}+(-1)^{2}+(-2)^{2}} \\   & =\sqrt{14} \\   & =\sqrt{14}\end{aligned}
$$

Now, since $f(x,y,z)=\operatorname{cos}⁡(\frac{\pi }{4}(x+z))$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡(\frac{\pi }{4}((3 - 3 t)+(- 2 t - 3))) \\   & =\cos{\left(\frac{5 \pi t}{4} \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\cos{\left(\frac{5 \pi t}{4} \right)})\cdot \sqrt{14}\cdot \text{d}t \\   & =\sqrt{14}{\int }_{0}^{1}(\cos{\left(\frac{5 \pi t}{4} \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{5 \pi t}{4}$, $\text{d}u=(- \frac{5 \pi}{4})\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{14}{\int }_{0}^{1}(\cos{\left(\frac{5 \pi t}{4} \right)})\,\text{d}t & =- \frac{4 \sqrt{14}}{5 \pi}{\int }_{0}^{- \frac{5 \pi}{4}}\operatorname{cos}⁡u\,\text{d}u \\   & =- \frac{4 \sqrt{14}}{5 \pi}(\operatorname{sin}⁡u)\,{|}_{0}^{- \frac{5 \pi}{4}} \\   & =- \frac{4 \sqrt{14}}{5 \pi}(\operatorname{sin}⁡(- \frac{5 \pi}{4})-\operatorname{sin}⁡(0)) \\   & =- \frac{4 \sqrt{14}}{5 \pi}((\frac{\sqrt{2}}{2})-(0)) \\   & =- \frac{4 \sqrt{7}}{5 \pi}\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s$ along the line segment from $(-4,2,3)$ to $(-3,-1,1).$

- $\frac{2 \sqrt{14} \left(-2 + \sqrt{2}\right)}{\pi}$
- $\frac{2 \sqrt{14} \left(2 - \sqrt{2}\right)}{\pi}$
- $\frac{2 \left(2 - \sqrt{2}\right)}{\pi}$
- $\frac{\sqrt{14} \left(2 - \sqrt{2}\right)}{\pi}$
- $- \sqrt{14} + \sqrt{7}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-4,2,3)$ to $(-3,-1,1).$

The position vectors of the endpoints of our line segment are $a=(-4)\,i+(2)\,j+(3)\,k$ and $b=(-3)\,i+(-1)\,j+(1)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-4)\,i+(2)\,j+(3)\,k)+t[((-3)\,i+(-1)\,j+(1)\,k)-((-4)\,i+(2)\,j+(3)\,k)] \\   & =((-4)\,i+(2)\,j+(3)\,k)+t((1)\,i+(-3)\,j+(-2)\,k) \\   & =(t - 4)\,i+(2 - 3 t)\,j+(3 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t - 4,$ $y=2 - 3 t,$ and $z=3 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t - 4)i+\frac{\text{d}}{\text{d}t}(2 - 3 t)j+\frac{\text{d}}{\text{d}t}(3 - 2 t)k \\   & =(1)\,i+(-3)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(-3)^{2}+(-2)^{2}} \\   & =\sqrt{14} \\   & =\sqrt{14}\end{aligned}
$$

Now, since $f(x,y,z)=\operatorname{cos}⁡(\frac{\pi }{4}(x+z))$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡(\frac{\pi }{4}((t - 4)+(3 - 2 t))) \\   & =\cos{\left(\pi \left(\frac{t}{4} + \frac{1}{4}\right) \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} + \frac{1}{4}\right) \right)})\cdot \sqrt{14}\cdot \text{d}t \\   & =\sqrt{14}{\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} + \frac{1}{4}\right) \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{\pi t}{4} - \frac{\pi}{4}$, $\text{d}u=(- \frac{\pi}{4})\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{14}{\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} + \frac{1}{4}\right) \right)})\,\text{d}t & =- \frac{4 \sqrt{14}}{\pi}{\int }_{- \frac{\pi}{4}}^{- \frac{\pi}{2}}\operatorname{cos}⁡u\,\text{d}u \\   & =- \frac{4 \sqrt{14}}{\pi}(\operatorname{sin}⁡u)\,{|}_{- \frac{\pi}{4}}^{- \frac{\pi}{2}} \\   & =- \frac{4 \sqrt{14}}{\pi}(\operatorname{sin}⁡(- \frac{\pi}{2})-\operatorname{sin}⁡(- \frac{\pi}{4})) \\   & =- \frac{4 \sqrt{14}}{\pi}((-1)-(- \frac{\sqrt{2}}{2})) \\   & =\frac{2 \sqrt{14} \left(2 - \sqrt{2}\right)}{\pi}\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s$ along the line segment from $(-3,-2,4)$ to $(-2,0,2).$

- $\frac{6 \sqrt{2}}{\pi}$
- $- \frac{3 \sqrt{2}}{2}$
- $- \frac{6 \sqrt{2}}{\pi}$
- $\frac{3 \sqrt{2}}{\pi}$
- $\frac{2 \sqrt{2}}{\pi}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-3,-2,4)$ to $(-2,0,2).$

The position vectors of the endpoints of our line segment are $a=(-3)\,i+(-2)\,j+(4)\,k$ and $b=(-2)\,i+(0)\,j+(2)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-3)\,i+(-2)\,j+(4)\,k)+t[((-2)\,i+(0)\,j+(2)\,k)-((-3)\,i+(-2)\,j+(4)\,k)] \\   & =((-3)\,i+(-2)\,j+(4)\,k)+t((1)\,i+(2)\,j+(-2)\,k) \\   & =(t - 3)\,i+(2 t - 2)\,j+(4 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t - 3,$ $y=2 t - 2,$ and $z=4 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t - 3)i+\frac{\text{d}}{\text{d}t}(2 t - 2)j+\frac{\text{d}}{\text{d}t}(4 - 2 t)k \\   & =(1)\,i+(2)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(2)^{2}+(-2)^{2}} \\   & =\sqrt{9} \\   & =3\end{aligned}
$$

Now, since $f(x,y,z)=\operatorname{cos}⁡(\frac{\pi }{4}(x+z))$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡(\frac{\pi }{4}((t - 3)+(4 - 2 t))) \\   & =\cos{\left(\pi \left(\frac{t}{4} - \frac{1}{4}\right) \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\operatorname{cos}⁡(\frac{\pi }{4}(x+z))\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} - \frac{1}{4}\right) \right)})\cdot 3\cdot \text{d}t \\   & =3{\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} - \frac{1}{4}\right) \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{\pi t}{4} + \frac{\pi}{4}$, $\text{d}u=(- \frac{\pi}{4})\,\text{d}t$ as follows: 

$$
\begin{aligned}3{\int }_{0}^{1}(\cos{\left(\pi \left(\frac{t}{4} - \frac{1}{4}\right) \right)})\,\text{d}t & =- \frac{12}{\pi}{\int }_{\frac{\pi}{4}}^{0}\operatorname{cos}⁡u\,\text{d}u \\   & =- \frac{12}{\pi}(\operatorname{sin}⁡u)\,{|}_{\frac{\pi}{4}}^{0} \\   & =- \frac{12}{\pi}(\operatorname{sin}⁡(0)-\operatorname{sin}⁡(\frac{\pi}{4})) \\   & =- \frac{12}{\pi}((0)-(\frac{\sqrt{2}}{2})) \\   & =\frac{6 \sqrt{2}}{\pi}\end{aligned}
$$


## q-76200 / sine

### Original captured record

Evaluate the integral $\displaystyle \int_(C)\sin (\frac{πy}{4})ds$ along the line segment from $(1, 0, 1)$ to $(2, 2, 3)$.

- $2π$
- $\frac{6}{π}$
- $\frac{π}{2}$
- $\frac{1}{2}$
- $\frac{3}{2π}$

[No observed solution, rating or correct key.]

### Parameterized historical evidence

Evaluate the integral $\displaystyle \int_(C)\sin (\frac{πy}{4})ds$ along the line segment from $(1, 0, 1)$ to $(2, 2, 3)$.

- $2 \pi$
- $\frac{\pi}{2}$
- $\frac{6}{\pi}$
- $\frac{1}{2}$
- $\frac{3}{2 \pi}$

[Source worked solution absent.]


### Parameterized historical evidence

Evaluate the integral $\displaystyle \int_(C)\sin (\frac{πy}{4})ds$ along the line segment from $(3, 1, -3)$ to $(0, 0, -5)$.

- $\frac{- \sqrt{7} + \sqrt{14}}{\pi}$
- $- \frac{\pi}{4}$
- $- \pi$
- $-1$
- $\frac{2 \sqrt{14} \left(2 - \sqrt{2}\right)}{\pi}$

[Source worked solution absent.]


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}\sin (\frac{πy}{4})ds$ along the line segment from $(-4, 2, 3)$ to $(-3, -1, 1)$.

- $- \frac{4 \sqrt{7}}{3 \pi}$
- $\frac{4 \sqrt{7}}{3 \pi}$
- $\frac{2 \sqrt{2}}{3 \pi}$
- $\frac{2 \sqrt{7}}{3 \pi}$
- $- \sqrt{7}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-4,2,3)$ to $(-3,-1,1).$

The position vectors of the endpoints of our line segment are $a=(-4)\,i+(2)\,j+(3)\,k$ and $b=(-3)\,i+(-1)\,j+(1)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-4)\,i+(2)\,j+(3)\,k)+t[((-3)\,i+(-1)\,j+(1)\,k)-((-4)\,i+(2)\,j+(3)\,k)] \\   & =((-4)\,i+(2)\,j+(3)\,k)+t((1)\,i+(-3)\,j+(-2)\,k) \\   & =(t - 4)\,i+(2 - 3 t)\,j+(3 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t - 4,$ $y=2 - 3 t,$ and $z=3 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t - 4)i+\frac{\text{d}}{\text{d}t}(2 - 3 t)j+\frac{\text{d}}{\text{d}t}(3 - 2 t)k \\   & =(1)\,i+(-3)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(-3)^{2}+(-2)^{2}} \\   & =\sqrt{14}\end{aligned}
$$

Now, since $f(x,y,z)=\sin (\frac{πy}{4})$, we obtain

$$
\begin{aligned}f(r(t)) & =\sin(\frac{\pi}{4}(2 - 3 t)) \\   & =\cos{\left(\frac{3 \pi t}{4} \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\sin (\frac{πy}{4})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{4} \right)})\cdot \sqrt{14}\cdot \text{d}t \\   & =\sqrt{14}{\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{4} \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{3 \pi t}{4} + \frac{\pi}{2}$, $\text{d}u=(- \frac{3 \pi}{4})\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{14}{\int }_{0}^{1}(\cos{\left(\frac{3 \pi t}{4} \right)})\,\text{d}t & =- \frac{4 \sqrt{14}}{3 \pi}{\int }_{\frac{\pi}{2}}^{- \frac{\pi}{4}}\sin u\,\text{d}u \\   & =- \frac{4 \sqrt{14}}{3 \pi}(-\cos u)\,{|}_{\frac{\pi}{2}}^{- \frac{\pi}{4}} \\   & =- \frac{4 \sqrt{14}}{3 \pi}(-\cos(- \frac{\pi}{4})-(-\cos(\frac{\pi}{2}))) \\   & =- \frac{4 \sqrt{14}}{3 \pi}((- \frac{\sqrt{2}}{2})-(0)) \\   & =\frac{4 \sqrt{7}}{3 \pi}\end{aligned}
$$


### Generated method-bank learner variant

Evaluate the integral ${\int }_{C}\sin (\frac{πy}{4})ds$ along the line segment from $(-3, -2, 4)$ to $(-2, 0, 2)$.

- $- \frac{6}{\pi}$
- $-3$
- $\frac{6}{\pi}$
- $- \frac{3}{\pi}$
- $- \frac{2}{\pi}$

We will use the formula

$$
{\int }_{C}f(x,y,z)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-3,-2,4)$ to $(-2,0,2).$

The position vectors of the endpoints of our line segment are $a=(-3)\,i+(-2)\,j+(4)\,k$ and $b=(-2)\,i+(0)\,j+(2)\,k.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =((-3)\,i+(-2)\,j+(4)\,k)+t[((-2)\,i+(0)\,j+(2)\,k)-((-3)\,i+(-2)\,j+(4)\,k)] \\   & =((-3)\,i+(-2)\,j+(4)\,k)+t((1)\,i+(2)\,j+(-2)\,k) \\   & =(t - 3)\,i+(2 t - 2)\,j+(4 - 2 t)\,k\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t - 3,$ $y=2 t - 2,$ and $z=4 - 2 t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\   & =\frac{\text{d}}{\text{d}t}(t - 3)i+\frac{\text{d}}{\text{d}t}(2 t - 2)j+\frac{\text{d}}{\text{d}t}(4 - 2 t)k \\   & =(1)\,i+(2)\,j+(-2)\,k \\  ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\   & =\sqrt{(1)^{2}+(2)^{2}+(-2)^{2}} \\   & =3\end{aligned}
$$

Now, since $f(x,y,z)=\sin (\frac{πy}{4})$, we obtain

$$
\begin{aligned}f(r(t)) & =\sin(\frac{\pi}{4}(2 t - 2)) \\   & =\sin{\left(\pi \left(\frac{t}{2} - \frac{1}{2}\right) \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\sin (\frac{πy}{4})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\   & ={\int }_{0}^{1}(\sin{\left(\pi \left(\frac{t}{2} - \frac{1}{2}\right) \right)})\cdot 3\cdot \text{d}t \\   & =3{\int }_{0}^{1}(\sin{\left(\pi \left(\frac{t}{2} - \frac{1}{2}\right) \right)})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=\frac{\pi t}{2} - \frac{\pi}{2}$, $\text{d}u=(\frac{\pi}{2})\,\text{d}t$ as follows: 

$$
\begin{aligned}3{\int }_{0}^{1}(\sin{\left(\pi \left(\frac{t}{2} - \frac{1}{2}\right) \right)})\,\text{d}t & =\frac{6}{\pi}{\int }_{- \frac{\pi}{2}}^{0}\sin u\,\text{d}u \\   & =\frac{6}{\pi}(-\cos u)\,{|}_{- \frac{\pi}{2}}^{0} \\   & =\frac{6}{\pi}(-\cos(0)-(-\cos(- \frac{\pi}{2}))) \\   & =\frac{6}{\pi}((-1)-(0)) \\   & =- \frac{6}{\pi}\end{aligned}
$$


