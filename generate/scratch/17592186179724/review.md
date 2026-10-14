# Line segment construction review

Worker draft; parent QA remains required.

Observed originals below preserve source problem, every choice and the full fixed solution. Empirical evidence profiles are ineligible for ordinary learner generation.

## observed source replay — quadratic

### Immutable original q-123127

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(0,2)$ to $(3,1)?$

- $\sqrt{10}{\int }_{0}^{1}({t}^{2}-t+2)\text{d}t$

- $2{\int }_{0}^{1}({t}^{2}+t-2)\text{d}t$

- $\sqrt{10}{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t$

- $10{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t$

- $\sqrt{2}{\int }_{0}^{1}({t}^{2}-t+2)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,2)$ to $(3,1).$ 

The position vectors of the endpoints of our line segment are $a=2\,j$ and $b=3\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =2\,j+t[(3\,i+j)-2\,j] \\  & =2\,j+t(3\,i-j) \\  & =3t\,i+(2-t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3t$ and $y=2-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)i+\frac{\text{d}}{\text{d}t}(2-t)j \\  & =3\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+(-1)^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3t)^{2}-(2-t) \\  & =9{t}^{2}+t-2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(9{t}^{2}+t-2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t.\end{aligned}
$$

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(0,2)$ to $(3,1)?$

- $2{\int }_{0}^{1}({t}^{2}+t-2)\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}({t}^{2}-t+2)\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}({t}^{2}-t+2)\text{d}t$
- $10{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,2)$ to $(3,1).$ 

The position vectors of the endpoints of our line segment are $a=2\,j$ and $b=3\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =2\,j+t[(3\,i+j)-2\,j] \\  & =2\,j+t(3\,i-j) \\  & =3t\,i+(2-t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3t$ and $y=2-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)i+\frac{\text{d}}{\text{d}t}(2-t)j \\  & =3\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+(-1)^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3t)^{2}-(2-t) \\  & =9{t}^{2}+t-2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(9{t}^{2}+t-2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}(9{t}^{2}+t-2)\text{d}t.\end{aligned}
$$

## changed-parameter observed empirical evidence — quadratic

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(0,-4)$ to $(2,1)?$

- $\sqrt{29}{\int }_{0}^{1}(4{t}^{2}-5t+4)\text{d}t$
- $\sqrt{29}{\int }_{0}^{1}({t}^{2}+5t-4)\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}({t}^{2}+5t-4)\text{d}t$
- $29{\int }_{0}^{1}(4{t}^{2}-5t+4)\text{d}t$
- $4{\int }_{0}^{1}({t}^{2}-5t+4)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,-4)$ to $(2,1).$ 

The position vectors of the endpoints of our line segment are $a=-4\,j$ and $b=2\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-4\,j+t[(2\,i+j)--4\,j] \\  & =-4\,j+t(2\,i+5\,j) \\  & =2t\,i+(-4+5t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t$ and $y=-4+5t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2t)i+\frac{\text{d}}{\text{d}t}(-4+5t)j \\  & =2\,i+5\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{5}^{2}} \\  & =\sqrt{29}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(2t)^{2}-(-4+5t) \\  & =4{t}^{2}-5t+4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(4{t}^{2}-5t+4)\cdot \sqrt{29}\cdot \text{d}t \\  & =\sqrt{29}{\int }_{0}^{1}(4{t}^{2}-5t+4)\text{d}t.\end{aligned}
$$

## observed source replay — log

### Immutable original q-123269

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(1,3)$ to $(0,3)?$

- ${\int }_{0}^{1}\operatorname{ln}⁡(2-t)\,\text{d}t$

- ${\int }_{0}^{1}\operatorname{ln}⁡(3-2t)\,\text{d}t$

- $\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(3-2t)\,\text{d}t$

- ${\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t$

- $\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,3)$ to $(0,3).$ 

The position vectors of the endpoints of our line segment are $a=i+3\,j$ and $b=3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+3\,j)+t[3\,j-(i+3\,j)] \\  & =(i+3\,j)-t\,i \\  & =(1-t)\,i+3\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1-t$ and $y=3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1-t)i+\frac{\text{d}}{\text{d}t}(3)j \\  & =-i \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-1)^{2}+{0}^{2}} \\  & =1\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((1-t)+3) \\  & =\operatorname{ln}⁡(4-t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(4-t)\cdot 1\cdot \text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t.\end{aligned}
$$

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(1,3)$ to $(0,3)?$

- ${\int }_{0}^{1}\operatorname{ln}⁡(3-2t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(2-t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(3-2t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,3)$ to $(0,3).$ 

The position vectors of the endpoints of our line segment are $a=i+3\,j$ and $b=3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+3\,j)+t[3\,j-(i+3\,j)] \\  & =(i+3\,j)-t\,i \\  & =(1-t)\,i+3\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1-t$ and $y=3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1-t)i+\frac{\text{d}}{\text{d}t}(3)j \\  & =-i \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-1)^{2}+{0}^{2}} \\  & =1\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((1-t)+3) \\  & =\operatorname{ln}⁡(4-t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(4-t)\cdot 1\cdot \text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(4-t)\,\text{d}t.\end{aligned}
$$

## changed-parameter observed empirical evidence — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(1,2)$ to $(2,3)?$

- ${\int }_{0}^{1}\operatorname{ln}⁡(1+t)\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(3+2t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(2+3t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(2+3t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(3+2t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,2)$ to $(2,3).$ 

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+2\,j)+t[(2\,i+3\,j)-(i+2\,j)] \\  & =(i+2\,j)+t(i+j) \\  & =(1+t)\,i+(2+t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1+t$ and $y=2+t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1+t)i+\frac{\text{d}}{\text{d}t}(2+t)j \\  & =i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((1+t)+2+t) \\  & =\operatorname{ln}⁡(3+2t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(3+2t)\cdot \sqrt{2}\cdot \text{d}t \\  & =\sqrt{2}{\int }_{0}^{1}\operatorname{ln}⁡(3+2t)\,\text{d}t.\end{aligned}
$$

## observed source replay — cos

### Immutable original q-123268

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(-1,1)$ to $(1,2)?$

- $\sqrt{5}{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t$

- $5{\int }_{0}^{1}(t-1-\operatorname{cos}⁡2t)\text{d}t$

- $\sqrt{5}{\int }_{0}^{1}(4t-\operatorname{cos}⁡t)\text{d}t$

- $5{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t$

- $\sqrt{5}{\int }_{0}^{1}(t-1-\operatorname{cos}⁡2t)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,1)$ to $(1,2).$ 

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-i+j)+t[(i+2\,j)-(-i+j)] \\  & =(-i+j)+t(2\,i+j) \\  & =(2t-1)\,i+(t+1)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t-1$ and $y=t+1$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2t-1)i+\frac{\text{d}}{\text{d}t}(t+1)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{1}^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(2t-1)-\operatorname{cos}⁡(t+1) \\  & =2t-\operatorname{cos}⁡(t+1).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t.\end{aligned}
$$

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(-1,1)$ to $(1,2)?$

- $\sqrt{5}{\int }_{0}^{1}(4t-\operatorname{cos}⁡t)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(t-1-\operatorname{cos}⁡2t)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t$
- $5{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t$
- $5{\int }_{0}^{1}(t-1-\operatorname{cos}⁡2t)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,1)$ to $(1,2).$ 

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-i+j)+t[(i+2\,j)-(-i+j)] \\  & =(-i+j)+t(2\,i+j) \\  & =(2t-1)\,i+(t+1)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t-1$ and $y=t+1$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2t-1)i+\frac{\text{d}}{\text{d}t}(t+1)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{1}^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(2t-1)-\operatorname{cos}⁡(t+1) \\  & =2t-\operatorname{cos}⁡(t+1).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}(2t-\operatorname{cos}⁡(t+1))\text{d}t.\end{aligned}
$$

## changed-parameter observed empirical evidence — cos

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(3,0)$ to $(1,-1)?$

- $5{\int }_{0}^{1}(-t+3-\operatorname{cos}⁡2t)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(-t+3-\operatorname{cos}⁡2t)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(4t-\operatorname{cos}⁡t)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(-2t+4-\operatorname{cos}⁡t)\text{d}t$
- $5{\int }_{0}^{1}(-2t+4-\operatorname{cos}⁡t)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,0)$ to $(1,-1).$ 

The position vectors of the endpoints of our line segment are $a=3\,i$ and $b=i-j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =3\,i+t[(i-j)-3\,i] \\  & =3\,i+t(-2\,i-j) \\  & =(-2t+3)\,i-t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+3$ and $y=-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+3)i+\frac{\text{d}}{\text{d}t}(-t)j \\  & =-2\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-1)^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(-2t+3)-\operatorname{cos}⁡(-t) \\  & =-2t+4-\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-2t+4-\operatorname{cos}⁡t)\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}(-2t+4-\operatorname{cos}⁡t)\text{d}t.\end{aligned}
$$

## observed source replay — linear

### Immutable original q-123279

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(-3,1)$ to $(2,3)?$

- $3\sqrt{3}{\int }_{0}^{1}(12t-5)\text{d}t$

- $29{\int }_{0}^{1}(10t-3)\text{d}t$

- $\sqrt{29}{\int }_{0}^{1}(8t+7)\text{d}t$

- $\sqrt{29}{\int }_{0}^{1}(12t-5)\text{d}t$

- $3\sqrt{3}{\int }_{0}^{1}(8t+7)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-3,1)$ to $(2,3).$ 

The position vectors of the endpoints of our line segment are $a=-3\,i+j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-3\,i+j)+t[(2\,i+3\,j)-(-3\,i+j)] \\  & =(-3\,i+j)+t(5\,i+2\,j) \\  & =(5t-3)\,i+(1+2t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=5t-3$ and $y=1+2t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(5t-3)i+\frac{\text{d}}{\text{d}t}(1+2t)j \\  & =5\,i+2\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{5}^{2}+{2}^{2}} \\  & =\sqrt{29}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(5t-3)+(1+2t) \\  & =12t-5.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(12t-5)\cdot \sqrt{29}\cdot \text{d}t \\  & =\sqrt{29}{\int }_{0}^{1}(12t-5)\text{d}t.\end{aligned}
$$

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(-3,1)$ to $(2,3)?$

- $29{\int }_{0}^{1}(10t-3)\text{d}t$
- $3\sqrt{3}{\int }_{0}^{1}(12t-5)\text{d}t$
- $\sqrt{29}{\int }_{0}^{1}(12t-5)\text{d}t$
- $3\sqrt{3}{\int }_{0}^{1}(8t+7)\text{d}t$
- $\sqrt{29}{\int }_{0}^{1}(8t+7)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-3,1)$ to $(2,3).$ 

The position vectors of the endpoints of our line segment are $a=-3\,i+j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-3\,i+j)+t[(2\,i+3\,j)-(-3\,i+j)] \\  & =(-3\,i+j)+t(5\,i+2\,j) \\  & =(5t-3)\,i+(1+2t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=5t-3$ and $y=1+2t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(5t-3)i+\frac{\text{d}}{\text{d}t}(1+2t)j \\  & =5\,i+2\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{5}^{2}+{2}^{2}} \\  & =\sqrt{29}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(5t-3)+(1+2t) \\  & =12t-5.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(12t-5)\cdot \sqrt{29}\cdot \text{d}t \\  & =\sqrt{29}{\int }_{0}^{1}(12t-5)\text{d}t.\end{aligned}
$$

## changed-parameter observed empirical evidence — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(3,0)$ to $(1,-1)?$

- $\sqrt{5}{\int }_{0}^{1}(-3t+1)\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(-5t+6)\text{d}t$
- $5{\int }_{0}^{1}(-4t+3)\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}(-5t+6)\text{d}t$
- $\sqrt{3}{\int }_{0}^{1}(-3t+1)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,0)$ to $(1,-1).$ 

The position vectors of the endpoints of our line segment are $a=3\,i$ and $b=i-j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =3\,i+t[(i-j)-3\,i] \\  & =3\,i+t(-2\,i-j) \\  & =(-2t+3)\,i-t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+3$ and $y=-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+3)i+\frac{\text{d}}{\text{d}t}(-t)j \\  & =-2\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-1)^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-2t+3)+(-t) \\  & =-5t+6.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-5t+6)\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}(-5t+6)\text{d}t.\end{aligned}
$$

## observed source replay — exp

### Immutable original q-123283

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(-3,4)?$

- $2\sqrt{5}{\int }_{0}^{1}{e}^{7t}\,\text{d}t$

- $10{\int }_{0}^{1}{e}^{3t}\,\text{d}t$

- $2\sqrt{5}{\int }_{0}^{1}{e}^{t}\,\text{d}t$

- $5{\int }_{0}^{1}{e}^{t}\,\text{d}t$

- $5{\int }_{0}^{1}{e}^{7t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(-3,4).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=-3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(-3\,i+4\,j) \\  & =-3t\,i+4t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-3t$ and $y=4t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-3t)i+\frac{\text{d}}{\text{d}t}(4t)j \\  & =-3\,i+4\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-3)^{2}+{4}^{2}} \\  & =\sqrt{25} \\  & =5\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{-3t+4t} \\  & ={e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{t}\cdot 5\cdot \text{d}t \\  & =5{\int }_{0}^{1}{e}^{t}\,\text{d}t.\end{aligned}
$$

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(-3,4)?$

- $10{\int }_{0}^{1}{e}^{3t}\,\text{d}t$
- $2\sqrt{5}{\int }_{0}^{1}{e}^{7t}\,\text{d}t$
- $5{\int }_{0}^{1}{e}^{t}\,\text{d}t$
- $5{\int }_{0}^{1}{e}^{7t}\,\text{d}t$
- $2\sqrt{5}{\int }_{0}^{1}{e}^{t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(-3,4).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=-3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(-3\,i+4\,j) \\  & =-3t\,i+4t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-3t$ and $y=4t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-3t)i+\frac{\text{d}}{\text{d}t}(4t)j \\  & =-3\,i+4\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-3)^{2}+{4}^{2}} \\  & =\sqrt{25} \\  & =5\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{-3t+4t} \\  & ={e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{t}\cdot 5\cdot \text{d}t \\  & =5{\int }_{0}^{1}{e}^{t}\,\text{d}t.\end{aligned}
$$

## changed-parameter observed empirical evidence — exp

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(1,3)?$

- $\sqrt{13}{\int }_{0}^{1}{e}^{4t}\,\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}{e}^{2t}\,\text{d}t$
- $5{\int }_{0}^{1}{e}^{-t}\,\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}{e}^{4t}\,\text{d}t$
- $\sqrt{10}{\int }_{0}^{1}{e}^{2t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(1,3).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(i+3\,j) \\  & =t\,i+3t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t$ and $y=3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{t+3t} \\  & ={e}^{4t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{4t}\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}{e}^{4t}\,\text{d}t.\end{aligned}
$$

## authored easy variant — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,-1)$ to $(-2,0)?$

- $\sqrt{17}{\int }_{0}^{1}(-7t+3)\text{d}t$
- $\sqrt{17}{\int }_{0}^{1}(-8t+3)\text{d}t$
- ${\int }_{0}^{1}(-7t+3)\text{d}t$
- $17{\int }_{0}^{1}(-7t+3)\text{d}t$
- $\sqrt{17}{\int }_{0}^{1}(t+3)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-1)$ to $(-2,0).$ 

The position vectors of the endpoints of our line segment are $a=2\,i-j$ and $b=-2\,i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i-j)+t[-2\,i-(2\,i-j)] \\  & =(2\,i-j)+t(-4\,i+j) \\  & =(-4t+2)\,i+(-1+t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-4t+2$ and $y=-1+t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-4t+2)i+\frac{\text{d}}{\text{d}t}(-1+t)j \\  & =-4\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-4)^{2}+{1}^{2}} \\  & =\sqrt{17}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-4t+2)+(-1+t) \\  & =-7t+3.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-7t+3)\cdot \sqrt{17}\cdot \text{d}t \\  & =\sqrt{17}{\int }_{0}^{1}(-7t+3)\text{d}t.\end{aligned}
$$

## authored easy variant — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(4,2)$ to $(2,1)?$

- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(6-2t)\,\text{d}t$
- $5{\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(6-t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(4,2)$ to $(2,1).$ 

The position vectors of the endpoints of our line segment are $a=4\,i+2\,j$ and $b=2\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(4\,i+2\,j)+t[(2\,i+j)-(4\,i+2\,j)] \\  & =(4\,i+2\,j)+t(-2\,i-j) \\  & =(4-2t)\,i+(2-t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4-2t$ and $y=2-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4-2t)i+\frac{\text{d}}{\text{d}t}(2-t)j \\  & =-2\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-1)^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((4-2t)+2-t) \\  & =\operatorname{ln}⁡(6-3t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\,\text{d}t.\end{aligned}
$$

## authored easy family demonstration — quadratic

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(2,3)$ to $(0,0)?$

- $\sqrt{13}{\int }_{0}^{1}(4{t}^{2}-5t+1)\text{d}t$
- ${\int }_{0}^{1}(4{t}^{2}-5t+1)\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(4{t}^{2}-8t+1)\text{d}t$
- $13{\int }_{0}^{1}(4{t}^{2}-5t+1)\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(3t+1)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,0).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=0.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[0-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-3\,j) \\  & =(-2t+2)\,i+(3-3t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=3-3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(3-3t)j \\  & =-2\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-3)^{2}} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(-2t+2)^{2}-(3-3t) \\  & =4{t}^{2}-5t+1.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(4{t}^{2}-5t+1)\cdot \sqrt{13}\cdot \text{d}t \\  & =\sqrt{13}{\int }_{0}^{1}(4{t}^{2}-5t+1)\text{d}t.\end{aligned}
$$

## authored easy family demonstration — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(2,3)$ to $(4,2)?$

- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(5+2t)\,\text{d}t$
- $5{\int }_{0}^{1}\operatorname{ln}⁡(5+t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(5+t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(5-t)\,\text{d}t$
- $\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(5+t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(4,2).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[(4\,i+2\,j)-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(2\,i-j) \\  & =(2+2t)\,i+(3-t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2+2t$ and $y=3-t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2+2t)i+\frac{\text{d}}{\text{d}t}(3-t)j \\  & =2\,i-j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+(-1)^{2}} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((2+2t)+3-t) \\  & =\operatorname{ln}⁡(5+t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(5+t)\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}\operatorname{ln}⁡(5+t)\,\text{d}t.\end{aligned}
$$

## authored easy family demonstration — cos

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(2,3)$ to $(0,0)?$

- $\sqrt{13}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(3t-3))\text{d}t$
- ${\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(3t-3))\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡3)\text{d}t$
- $13{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(3t-3))\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(3-\operatorname{cos}⁡(3t-3))\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,0).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=0.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[0-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-3\,j) \\  & =(-2t+2)\,i+(-3t+3)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=-3t+3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(-3t+3)j \\  & =-2\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-3)^{2}} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(-2t+2)-\operatorname{cos}⁡(-3t+3) \\  & =-2t+3-\operatorname{cos}⁡(3t-3).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(3t-3))\cdot \sqrt{13}\cdot \text{d}t \\  & =\sqrt{13}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(3t-3))\text{d}t.\end{aligned}
$$

## authored easy family demonstration — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,3)$ to $(0,0)?$

- $\sqrt{13}{\int }_{0}^{1}(-7t+7)\text{d}t$
- ${\int }_{0}^{1}(-7t+7)\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(-4t+7)\text{d}t$
- $13{\int }_{0}^{1}(-7t+7)\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}(-3t+7)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,0).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=0.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[0-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-3\,j) \\  & =(-2t+2)\,i+(3-3t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=3-3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(3-3t)j \\  & =-2\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-3)^{2}} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-2t+2)+(3-3t) \\  & =-7t+7.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-7t+7)\cdot \sqrt{13}\cdot \text{d}t \\  & =\sqrt{13}{\int }_{0}^{1}(-7t+7)\text{d}t.\end{aligned}
$$

## authored easy family demonstration — exp

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(-2,-3)?$

- $\sqrt{13}{\int }_{0}^{1}{e}^{-3t}\,\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}{e}^{-2t}\,\text{d}t$
- ${\int }_{0}^{1}{e}^{-5t}\,\text{d}t$
- $\sqrt{13}{\int }_{0}^{1}{e}^{-5t}\,\text{d}t$
- $13{\int }_{0}^{1}{e}^{-5t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(-2,-3).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=-2\,i-3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(-2\,i-3\,j) \\  & =-2t\,i-3t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t$ and $y=-3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t)i+\frac{\text{d}}{\text{d}t}(-3t)j \\  & =-2\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(-3)^{2}} \\  & =\sqrt{13} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{-2t-3t} \\  & ={e}^{-5t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{-5t}\cdot \sqrt{13}\cdot \text{d}t \\  & =\sqrt{13}{\int }_{0}^{1}{e}^{-5t}\,\text{d}t.\end{aligned}
$$

## authored moderate variant — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,-1)$ to $(-2,\frac{1}{2})?$

- $\frac{\sqrt{73}}{2}{\int }_{0}^{1}(-8t+3)\text{d}t$
- $\frac{\sqrt{73}}{2}{\int }_{0}^{1}(-\frac{13}{2}t+3)\text{d}t$
- ${\int }_{0}^{1}(-\frac{13}{2}t+3)\text{d}t$
- $\frac{\sqrt{73}}{2}{\int }_{0}^{1}(\frac{3}{2}t+3)\text{d}t$
- $\frac{73}{4}{\int }_{0}^{1}(-\frac{13}{2}t+3)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,-1)$ to $(-2,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i-j$ and $b=-2\,i+\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i-j)+t[(-2\,i+\frac{1}{2}\,j)-(2\,i-j)] \\  & =(2\,i-j)+t(-4\,i+\frac{3}{2}\,j) \\  & =(-4t+2)\,i+(-1+\frac{3}{2}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-4t+2$ and $y=-1+\frac{3}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-4t+2)i+\frac{\text{d}}{\text{d}t}(-1+\frac{3}{2}t)j \\  & =-4\,i+\frac{3}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-4)^{2}+{\frac{3}{2}}^{2}} \\  & =\frac{\sqrt{73}}{2}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-4t+2)+(-1+\frac{3}{2}t) \\  & =-\frac{13}{2}t+3.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-\frac{13}{2}t+3)\cdot \frac{\sqrt{73}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{73}}{2}{\int }_{0}^{1}(-\frac{13}{2}t+3)\text{d}t.\end{aligned}
$$

## authored moderate variant — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(4,2)$ to $(2,\frac{3}{2})?$

- $\frac{17}{4}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$
- $\frac{\sqrt{17}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-2t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$
- $\frac{\sqrt{17}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{1}{2}t)\,\text{d}t$
- $\frac{\sqrt{17}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(4,2)$ to $(2,\frac{3}{2}).$ 

The position vectors of the endpoints of our line segment are $a=4\,i+2\,j$ and $b=2\,i+\frac{3}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(4\,i+2\,j)+t[(2\,i+\frac{3}{2}\,j)-(4\,i+2\,j)] \\  & =(4\,i+2\,j)+t(-2\,i-\frac{1}{2}\,j) \\  & =(4-2t)\,i+(2-\frac{1}{2}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4-2t$ and $y=2-\frac{1}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4-2t)i+\frac{\text{d}}{\text{d}t}(2-\frac{1}{2}t)j \\  & =-2\,i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{1}{2})^{2}} \\  & =\frac{\sqrt{17}}{2}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((4-2t)+2-\frac{1}{2}t) \\  & =\operatorname{ln}⁡(6-\frac{5}{2}t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\cdot \frac{\sqrt{17}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{17}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t.\end{aligned}
$$

## authored moderate family demonstration — quadratic

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(2,3)$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(4{t}^{2}-\frac{11}{2}t+1)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(4{t}^{2}-\frac{11}{2}t+1)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(\frac{5}{2}t+1)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(4{t}^{2}-8t+1)\text{d}t$
- $\frac{41}{4}{\int }_{0}^{1}(4{t}^{2}-\frac{11}{2}t+1)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[\frac{1}{2}\,j-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-\frac{5}{2}\,j) \\  & =(-2t+2)\,i+(3-\frac{5}{2}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=3-\frac{5}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(3-\frac{5}{2}t)j \\  & =-2\,i-\frac{5}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{5}{2})^{2}} \\  & =\frac{\sqrt{41}}{2}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(-2t+2)^{2}-(3-\frac{5}{2}t) \\  & =4{t}^{2}-\frac{11}{2}t+1.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(4{t}^{2}-\frac{11}{2}t+1)\cdot \frac{\sqrt{41}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{41}}{2}{\int }_{0}^{1}(4{t}^{2}-\frac{11}{2}t+1)\text{d}t.\end{aligned}
$$

## authored moderate family demonstration — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(2,4)$ to $(\frac{5}{2},1)?$

- $\frac{\sqrt{37}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6+\frac{1}{2}t)\,\text{d}t$
- $\frac{\sqrt{37}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-3t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$
- $\frac{37}{4}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$
- $\frac{\sqrt{37}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,4)$ to $(\frac{5}{2},1).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+4\,j$ and $b=\frac{5}{2}\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+4\,j)+t[(\frac{5}{2}\,i+j)-(2\,i+4\,j)] \\  & =(2\,i+4\,j)+t(\frac{1}{2}\,i-3\,j) \\  & =(2+\frac{1}{2}t)\,i+(4-3t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2+\frac{1}{2}t$ and $y=4-3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2+\frac{1}{2}t)i+\frac{\text{d}}{\text{d}t}(4-3t)j \\  & =\frac{1}{2}\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{\frac{1}{2}}^{2}+(-3)^{2}} \\  & =\frac{\sqrt{37}}{2}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((2+\frac{1}{2}t)+4-3t) \\  & =\operatorname{ln}⁡(6-\frac{5}{2}t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\cdot \frac{\sqrt{37}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{37}}{2}{\int }_{0}^{1}\operatorname{ln}⁡(6-\frac{5}{2}t)\,\text{d}t.\end{aligned}
$$

## authored moderate family demonstration — cos

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(2,3)$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3))\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3))\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(3-\operatorname{cos}⁡(\frac{5}{2}t-3))\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡3)\text{d}t$
- $\frac{41}{4}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3))\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[\frac{1}{2}\,j-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-\frac{5}{2}\,j) \\  & =(-2t+2)\,i+(-\frac{5}{2}t+3)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=-\frac{5}{2}t+3$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(-\frac{5}{2}t+3)j \\  & =-2\,i-\frac{5}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{5}{2})^{2}} \\  & =\frac{\sqrt{41}}{2}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(-2t+2)-\operatorname{cos}⁡(-\frac{5}{2}t+3) \\  & =-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3))\cdot \frac{\sqrt{41}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{5}{2}t-3))\text{d}t.\end{aligned}
$$

## authored moderate family demonstration — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,3)$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(-\frac{13}{2}t+7)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-\frac{13}{2}t+7)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-\frac{5}{2}t+7)\text{d}t$
- $\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-4t+7)\text{d}t$
- $\frac{41}{4}{\int }_{0}^{1}(-\frac{13}{2}t+7)\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,3)$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+3\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+3\,j)+t[\frac{1}{2}\,j-(2\,i+3\,j)] \\  & =(2\,i+3\,j)+t(-2\,i-\frac{5}{2}\,j) \\  & =(-2t+2)\,i+(3-\frac{5}{2}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=3-\frac{5}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(3-\frac{5}{2}t)j \\  & =-2\,i-\frac{5}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{5}{2})^{2}} \\  & =\frac{\sqrt{41}}{2}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-2t+2)+(3-\frac{5}{2}t) \\  & =-\frac{13}{2}t+7.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-\frac{13}{2}t+7)\cdot \frac{\sqrt{41}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{41}}{2}{\int }_{0}^{1}(-\frac{13}{2}t+7)\text{d}t.\end{aligned}
$$

## authored moderate family demonstration — exp

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(\frac{3}{2},1)?$

- $\frac{\sqrt{13}}{2}{\int }_{0}^{1}{e}^{\frac{5}{2}t}\,\text{d}t$
- $\frac{\sqrt{13}}{2}{\int }_{0}^{1}{e}^{\frac{3}{2}t}\,\text{d}t$
- ${\int }_{0}^{1}{e}^{\frac{5}{2}t}\,\text{d}t$
- $\frac{\sqrt{13}}{2}{\int }_{0}^{1}{e}^{t}\,\text{d}t$
- $\frac{13}{4}{\int }_{0}^{1}{e}^{\frac{5}{2}t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(\frac{3}{2},1).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=\frac{3}{2}\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(\frac{3}{2}\,i+j) \\  & =\frac{3}{2}t\,i+t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=\frac{3}{2}t$ and $y=t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{3}{2}t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{3}{2}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{\frac{3}{2}}^{2}+{1}^{2}} \\  & =\sqrt{\frac{13}{4}} \\  & =\frac{\sqrt{13}}{2}\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{\frac{3}{2}t+t} \\  & ={e}^{\frac{5}{2}t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{\frac{5}{2}t}\cdot \frac{\sqrt{13}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{13}}{2}{\int }_{0}^{1}{e}^{\frac{5}{2}t}\,\text{d}t.\end{aligned}
$$

## authored hard variant — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,- \frac{2}{3})$ to $(-2,\frac{1}{2})?$

- ${\int }_{0}^{1}(-\frac{41}{6}t+\frac{10}{3})\text{d}t$
- $\frac{25}{6}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{10}{3})\text{d}t$
- $\frac{25}{6}{\int }_{0}^{1}(-8t+\frac{10}{3})\text{d}t$
- $\frac{625}{36}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{10}{3})\text{d}t$
- $\frac{25}{6}{\int }_{0}^{1}(\frac{7}{6}t+\frac{10}{3})\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,- \frac{2}{3})$ to $(-2,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i-\frac{2}{3}\,j$ and $b=-2\,i+\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i-\frac{2}{3}\,j)+t[(-2\,i+\frac{1}{2}\,j)-(2\,i-\frac{2}{3}\,j)] \\  & =(2\,i-\frac{2}{3}\,j)+t(-4\,i+\frac{7}{6}\,j) \\  & =(-4t+2)\,i+(-\frac{2}{3}+\frac{7}{6}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-4t+2$ and $y=-\frac{2}{3}+\frac{7}{6}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-4t+2)i+\frac{\text{d}}{\text{d}t}(-\frac{2}{3}+\frac{7}{6}t)j \\  & =-4\,i+\frac{7}{6}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-4)^{2}+{\frac{7}{6}}^{2}} \\  & =\frac{25}{6}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-4t+2)+(-\frac{2}{3}+\frac{7}{6}t) \\  & =-\frac{41}{6}t+\frac{10}{3}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-\frac{41}{6}t+\frac{10}{3})\cdot \frac{25}{6}\cdot \text{d}t \\  & =\frac{25}{6}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{10}{3})\text{d}t.\end{aligned}
$$

## authored hard variant — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(\frac{13}{3},2)$ to $(2,\frac{3}{2})?$

- ${\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$
- $\frac{\sqrt{205}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$
- $\frac{205}{36}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$
- $\frac{\sqrt{205}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{7}{3}t)\,\text{d}t$
- $\frac{\sqrt{205}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{1}{2}t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(\frac{13}{3},2)$ to $(2,\frac{3}{2}).$ 

The position vectors of the endpoints of our line segment are $a=\frac{13}{3}\,i+2\,j$ and $b=2\,i+\frac{3}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(\frac{13}{3}\,i+2\,j)+t[(2\,i+\frac{3}{2}\,j)-(\frac{13}{3}\,i+2\,j)] \\  & =(\frac{13}{3}\,i+2\,j)+t(-\frac{7}{3}\,i-\frac{1}{2}\,j) \\  & =(\frac{13}{3}-\frac{7}{3}t)\,i+(2-\frac{1}{2}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=\frac{13}{3}-\frac{7}{3}t$ and $y=2-\frac{1}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{13}{3}-\frac{7}{3}t)i+\frac{\text{d}}{\text{d}t}(2-\frac{1}{2}t)j \\  & =-\frac{7}{3}\,i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(- \frac{7}{3})^{2}+(- \frac{1}{2})^{2}} \\  & =\frac{\sqrt{205}}{6}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((\frac{13}{3}-\frac{7}{3}t)+2-\frac{1}{2}t) \\  & =\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\cdot \frac{\sqrt{205}}{6}\cdot \text{d}t \\  & =\frac{\sqrt{205}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t.\end{aligned}
$$

## authored hard family demonstration — quadratic

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={x}^{2}-y,$ traversed along the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(4{t}^{2}-\frac{31}{6}t+\frac{2}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(4{t}^{2}-\frac{31}{6}t+\frac{2}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(\frac{17}{6}t+\frac{2}{3})\text{d}t$
- $\frac{433}{36}{\int }_{0}^{1}(4{t}^{2}-\frac{31}{6}t+\frac{2}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(4{t}^{2}-8t+\frac{2}{3})\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+\frac{10}{3}\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+\frac{10}{3}\,j)+t[\frac{1}{2}\,j-(2\,i+\frac{10}{3}\,j)] \\  & =(2\,i+\frac{10}{3}\,j)+t(-2\,i-\frac{17}{6}\,j) \\  & =(-2t+2)\,i+(\frac{10}{3}-\frac{17}{6}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=\frac{10}{3}-\frac{17}{6}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(\frac{10}{3}-\frac{17}{6}t)j \\  & =-2\,i-\frac{17}{6}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{17}{6})^{2}} \\  & =\frac{\sqrt{433}}{6}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}-y$, we obtain

$$
\begin{aligned}f(r(t)) & =(-2t+2)^{2}-(\frac{10}{3}-\frac{17}{6}t) \\  & =4{t}^{2}-\frac{31}{6}t+\frac{2}{3}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(4{t}^{2}-\frac{31}{6}t+\frac{2}{3})\cdot \frac{\sqrt{433}}{6}\cdot \text{d}t \\  & =\frac{\sqrt{433}}{6}{\int }_{0}^{1}(4{t}^{2}-\frac{31}{6}t+\frac{2}{3})\text{d}t.\end{aligned}
$$

## authored hard family demonstration — log

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=\operatorname{ln}⁡(x+y),$ traversed along the line segment from $(\frac{7}{3},4)$ to $(\frac{5}{2},1)?$

- $\frac{5\sqrt{13}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$
- $\frac{5\sqrt{13}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}+\frac{1}{6}t)\,\text{d}t$
- ${\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$
- $\frac{5\sqrt{13}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-3t)\,\text{d}t$
- $\frac{325}{36}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(\frac{7}{3},4)$ to $(\frac{5}{2},1).$ 

The position vectors of the endpoints of our line segment are $a=\frac{7}{3}\,i+4\,j$ and $b=\frac{5}{2}\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(\frac{7}{3}\,i+4\,j)+t[(\frac{5}{2}\,i+j)-(\frac{7}{3}\,i+4\,j)] \\  & =(\frac{7}{3}\,i+4\,j)+t(\frac{1}{6}\,i-3\,j) \\  & =(\frac{7}{3}+\frac{1}{6}t)\,i+(4-3t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=\frac{7}{3}+\frac{1}{6}t$ and $y=4-3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{7}{3}+\frac{1}{6}t)i+\frac{\text{d}}{\text{d}t}(4-3t)j \\  & =\frac{1}{6}\,i-3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{\frac{1}{6}}^{2}+(-3)^{2}} \\  & =\frac{5\sqrt{13}}{6}\end{aligned}
$$

Now, since $f(x,y)=\operatorname{ln}⁡(x+y)$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{ln}⁡((\frac{7}{3}+\frac{1}{6}t)+4-3t) \\  & =\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\cdot \frac{5\sqrt{13}}{6}\cdot \text{d}t \\  & =\frac{5\sqrt{13}}{6}{\int }_{0}^{1}\operatorname{ln}⁡(\frac{19}{3}-\frac{17}{6}t)\,\text{d}t.\end{aligned}
$$

## authored hard family demonstration — cos

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=1+x-\operatorname{cos}⁡y,$ traversed along the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\text{d}t$
- $\frac{433}{36}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{10}{3}))\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+\frac{10}{3}\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+\frac{10}{3}\,j)+t[\frac{1}{2}\,j-(2\,i+\frac{10}{3}\,j)] \\  & =(2\,i+\frac{10}{3}\,j)+t(-2\,i-\frac{17}{6}\,j) \\  & =(-2t+2)\,i+(-\frac{17}{6}t+\frac{10}{3})\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=-\frac{17}{6}t+\frac{10}{3}$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(-\frac{17}{6}t+\frac{10}{3})j \\  & =-2\,i-\frac{17}{6}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{17}{6})^{2}} \\  & =\frac{\sqrt{433}}{6}\end{aligned}
$$

Now, since $f(x,y)=1+x-\operatorname{cos}⁡y$, we obtain

$$
\begin{aligned}f(r(t)) & =1+(-2t+2)-\operatorname{cos}⁡(-\frac{17}{6}t+\frac{10}{3}) \\  & =-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\cdot \frac{\sqrt{433}}{6}\cdot \text{d}t \\  & =\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-2t+3-\operatorname{cos}⁡(\frac{17}{6}t-\frac{10}{3}))\text{d}t.\end{aligned}
$$

## authored hard family demonstration — linear

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)=2x+y,$ traversed along the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2})?$

- ${\int }_{0}^{1}(-\frac{41}{6}t+\frac{22}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{22}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-\frac{17}{6}t+\frac{22}{3})\text{d}t$
- $\frac{433}{36}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{22}{3})\text{d}t$
- $\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-4t+\frac{22}{3})\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,\frac{10}{3})$ to $(0,\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=2\,i+\frac{10}{3}\,j$ and $b=\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2\,i+\frac{10}{3}\,j)+t[\frac{1}{2}\,j-(2\,i+\frac{10}{3}\,j)] \\  & =(2\,i+\frac{10}{3}\,j)+t(-2\,i-\frac{17}{6}\,j) \\  & =(-2t+2)\,i+(\frac{10}{3}-\frac{17}{6}t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-2t+2$ and $y=\frac{10}{3}-\frac{17}{6}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-2t+2)i+\frac{\text{d}}{\text{d}t}(\frac{10}{3}-\frac{17}{6}t)j \\  & =-2\,i-\frac{17}{6}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2)^{2}+(- \frac{17}{6})^{2}} \\  & =\frac{\sqrt{433}}{6}\end{aligned}
$$

Now, since $f(x,y)=2x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(-2t+2)+(\frac{10}{3}-\frac{17}{6}t) \\  & =-\frac{41}{6}t+\frac{22}{3}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(-\frac{41}{6}t+\frac{22}{3})\cdot \frac{\sqrt{433}}{6}\cdot \text{d}t \\  & =\frac{\sqrt{433}}{6}{\int }_{0}^{1}(-\frac{41}{6}t+\frac{22}{3})\text{d}t.\end{aligned}
$$

## authored hard family demonstration — exp

### Parameterized generator

Which of the following is equivalent to the line integral of the function $f(x,y)={e}^{x+y},$ traversed along the line segment from $(0,0)$ to $(\frac{1}{3},\frac{1}{2})?$

- ${\int }_{0}^{1}{e}^{\frac{5}{6}t}\,\text{d}t$
- $\frac{\sqrt{13}}{6}{\int }_{0}^{1}{e}^{\frac{5}{6}t}\,\text{d}t$
- $\frac{\sqrt{13}}{6}{\int }_{0}^{1}{e}^{\frac{1}{2}t}\,\text{d}t$
- $\frac{13}{36}{\int }_{0}^{1}{e}^{\frac{5}{6}t}\,\text{d}t$
- $\frac{\sqrt{13}}{6}{\int }_{0}^{1}{e}^{\frac{1}{3}t}\,\text{d}t$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(\frac{1}{3},\frac{1}{2}).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=\frac{1}{3}\,i+\frac{1}{2}\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t(b) \\  & =t(\frac{1}{3}\,i+\frac{1}{2}\,j) \\  & =\frac{1}{3}t\,i+\frac{1}{2}t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=\frac{1}{3}t$ and $y=\frac{1}{2}t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{1}{3}t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{2}t)j \\  & =\frac{1}{3}\,i+\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{\frac{1}{3}}^{2}+{\frac{1}{2}}^{2}} \\  & =\sqrt{\frac{13}{36}} \\  & =\frac{\sqrt{13}}{6}\end{aligned}
$$

Now, since $f(x,y)={e}^{x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{\frac{1}{3}t+\frac{1}{2}t} \\  & ={e}^{\frac{5}{6}t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{\frac{5}{6}t}\cdot \frac{\sqrt{13}}{6}\cdot \text{d}t \\  & =\frac{\sqrt{13}}{6}{\int }_{0}^{1}{e}^{\frac{5}{6}t}\,\text{d}t.\end{aligned}
$$
