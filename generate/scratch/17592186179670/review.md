# Draft review

Basis 2275. Raw source profiles are evidence-only. Generated method banks are authored. Parent QA remains pending.


## Original q-39954

Profile: `source:q-39954`; evidence-only: True. Parameters: `{"a": 1, "b": 2, "c": 2, "dx": 1, "dy": -1}`.

Evaluate the integral of the function $f(x, y) = 2xy$ along the line segment from $(1, 2)$ to $(2, 1)$.

- $2\sqrt{2}$
- $\frac{3\sqrt{2}}{4}$
- $\frac{13\sqrt{2}}{3}$
- $\frac{2\sqrt{2}}{3}$
- $\frac{15}{3}$

[Source worked solution absent.]


## Original q-76565

Profile: `source:q-76565`; evidence-only: True. Parameters: `{"a": 1, "b": 0, "c": 2, "d": -3, "dx": -2, "dy": 0}`.

Evaluate the integral of the function $f(x, y) = 2x - 3y$ along the line segment from $(1, 0)$ to $(-1, 0)$.

- $\sqrt{5}$
- $2$
- $0$
- $4$
- $\sqrt{2}$

[Source worked solution absent.]


## Original q-123363

Profile: `source:q-123363`; evidence-only: True. Parameters: `{"a": 2, "b": 0, "dx": 0, "dy": 2, "k": 2}`.

Evaluate the integral of the function $f(x,y)=x+\sqrt{2y}$ along the line segment from $(2,0)$ to $(2,2).$

- $3$
- $6$
- $\frac{13}{6}$
- $\frac{17}{3}$
- $\frac{20}{3}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,0)$ to $(2,2).$ 

The position vectors of the endpoints of our line segment are $a=2\,i$ and $b=2\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =2\,i+t[(2\,i+2\,j)-2\,i] \\  & =2\,i+2t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2$ and $y=2t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2)i+\frac{\text{d}}{\text{d}t}(2t)j \\  & =2j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{0}^{2}+{2}^{2}} \\  & =2\end{aligned}
$$

Now, since $f(x,y)=x+\sqrt{2y}$, we obtain

$$
\begin{aligned}f(r(t)) & =2+\sqrt{2(2t)} \\  & =2+2\sqrt{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2+2\sqrt{t})\cdot 2\cdot \text{d}t \\  & =4{\int }_{0}^{1}(1+\sqrt{t})\text{d}t \\  & =4{[t+\frac{2{t}^{3/2}}{3}]}_{0}^{1} \\  & =4(1+\frac{2}{3})-0 \\  & =\frac{20}{3}.\end{aligned}
$$


## Original q-123366

Profile: `source:q-123366`; evidence-only: True. Parameters: `{"a": 0, "b": 0, "c": 3, "d": 1, "dx": -1, "dy": 4}`.

Evaluate the integral of the function $f(x,y)={e}^{3x+y}$ along the line segment from $(0,0)$ to $(-1,4).$

- $4e-1$
- $4(e-1)$
- $4({e}^{2}-1)$
- $\sqrt{17}(e-1)$
- $\sqrt{17}({e}^{2}-1)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(-1,4).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=-i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t\,(b) \\  & =t(-i+4\,j) \\  & =-t\,i+4t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=-t$ and $y=4t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(-t)i+\frac{\text{d}}{\text{d}t}(4t)j \\  & =-i+4\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-1)^{2}+{4}^{2}} \\  & =\sqrt{17}\end{aligned}
$$

Now, since $f(x,y)={e}^{3x+y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{3(-t)+4t} \\  & ={e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{e}^{t}\cdot \sqrt{17}\cdot \text{d}t \\  & =\sqrt{17}{\int }_{0}^{1}{e}^{t}\,\text{d}t \\  & =\sqrt{17}[{e}^{t}]_{0}^{1} \\  & =\sqrt{17}(e-1).\end{aligned}
$$


## Original q-76564

Profile: `source:q-76564`; evidence-only: True. Parameters: `{"a": 1, "b": 2, "c": 1, "dx": 3, "dy": 5}`.

Evaluate the integral of the function $f(x,y)=xy$ along the line segment from $(1,2)$ to $(4,7).$

- $25\sqrt{34}$
- $\frac{5\sqrt{34}}{2}$
- $\frac{25\sqrt{34}}{2}$
- $\frac{\sqrt{34}}{2}$
- $\frac{5\sqrt{3}}{2}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,2)$ to $(4,7).$

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=4\,i+7j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+2\,j)+t[4\,i+7j-(i+2\,j)] \\  & =(i+2\,j)+t(3i+5j) \\  & =(1+3t)\,i+(2+5t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1+3t$ and $y=2+5t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1+3t)i+\frac{\text{d}}{\text{d}t}(2+5t)j \\  & =3i+5j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+{5}^{2}} \\  & =\sqrt{34}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
\begin{aligned}f(r(t)) & =(1+3t)(2+5t) \\  & =15{t}^{2}+11t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(15{t}^{2}+11t+2)\cdot \sqrt{34}\cdot \text{d}t \\  & =\sqrt{34}{\int }_{0}^{1}(15{t}^{2}+11t+2)\,\text{d}t \\  & =\sqrt{34}{[5{t}^{3}+\frac{11}{2}{t}^{2}+2t]}_{0}^{1} \\  & =\sqrt{34}(5+\frac{11}{2}+2)-0 \\  & =\frac{25\sqrt{34}}{2}.\end{aligned}
$$


## Original q-76605

Profile: `source:q-76605`; evidence-only: True. Parameters: `{"a": 1, "b": 1, "dx": 1, "dy": 3, "n": 8}`.

Evaluate the integral ${\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{8})\,\text{d}s$ along the line segment from $(1,1)$ to $(2,4).$

- $\frac{4\sqrt{10}}{\pi }$
- $\frac{\pi \sqrt{10}}{4}$
- $\frac{4}{\pi }$
- $\frac{\pi }{4}$
- $\frac{\sqrt{10}}{\pi }$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,1)$ to $(2,4).$ 

The position vectors of the endpoints of our line segment are $a=i+j$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(i+j)+t[2\,i+4\,j-(i+j)] \\  & =(i+j)+t(i+3\,j) \\  & =(1+t)\,i+(1+3t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1+t$ and $y=1+3t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1+t)i+\frac{\text{d}}{\text{d}t}(1+3t)j \\  & =1\,i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={sec}^{2}⁡(\frac{\pi (y-x)}{8})$, we obtain

$$
\begin{aligned}f(r(t)) & ={sec}^{2}⁡(\frac{\pi ((1+3t)-(1+t))}{8}) \\  & ={sec}^{2}⁡(\frac{\pi t}{4}).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{8})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi t}{4})\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi t}{4})\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=\frac{\pi t}{4},$ $\text{d}u=\frac{\pi }{4}\,\text{d}t$ as follows: 

$$
\begin{aligned}\sqrt{10}{\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi t}{4})\,\text{d}t & =\frac{4\sqrt{10}}{\pi }{\int }_{0}^{\pi /4}{sec}^{2}⁡u\,\text{d}u \\  & =\frac{4\sqrt{10}}{\pi }\operatorname{tan}⁡u\,{|}_{0}^{\pi /4} \\  & =\frac{4\sqrt{10}}{\pi }(\operatorname{tan}⁡(\frac{\pi }{4})-\operatorname{tan}⁡(0)) \\  & =\frac{4\sqrt{10}}{\pi }(1-0) \\  & =\frac{4\sqrt{10}}{\pi }\end{aligned}
$$


## Original q-76650

Profile: `source:q-76650`; evidence-only: True. Parameters: `{"a": 0, "b": 1, "dx": 2, "dy": 2}`.

Evaluate the integral ${\int }_{C}(4x+2)\,{e}^{xy}\,\text{d}s$ along the line segment from $(0,1)$ to $(2,3).$

- $2e\sqrt{2}({e}^{5}-1)$
- $2\sqrt{2}({e}^{6}-1)$
- $({e}^{6}-1)$
- $\sqrt{2}({e}^{6}-1)$
- $2({e}^{6}-1)$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,1)$ to $(2,3).$ 

The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t[2\,i+3\,j-j] \\  & =j+t(2\,i+2\,j) \\  & =2t\,i+(1+2t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2t$ and $y=1+2t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2t)i+\frac{\text{d}}{\text{d}t}(1+2t)j \\  & =2\,i+2\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{2}^{2}} \\  & =2\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=(4x+2)\,{e}^{xy}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4(2t)+2){e}^{2t(1+2t)} \\  & =(8t+2)\,{e}^{2t+4{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{e}^{xy}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(8t+2)\,{e}^{2t+4{t}^{2}}\cdot 2\sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{1}(8t+2)\,{e}^{2t+4{t}^{2}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=2t+4{t}^{2},$ $\text{d}u=(2+8t)\,\text{d}t$ as follows:  

$$
\begin{aligned}2\sqrt{2}{\int }_{0}^{1}(8t+2)\,{e}^{2t+4{t}^{2}}\,\text{d}t & =2\sqrt{2}{\int }_{0}^{6}{e}^{u}\,\text{d}u \\  & =2\sqrt{2}\,{e}^{u}\,{|}_{0}^{6} \\  & =2\sqrt{2}({e}^{6}-{e}^{0}) \\  & =2\sqrt{2}({e}^{6}-1)\end{aligned}
$$


## Generated evidence variant q-39954

Profile: `source:q-39954`; evidence-only: True. Parameters: `{"a": 2, "b": 2, "c": 3, "dx": -2, "dy": 1}`.

Evaluate the integral of the function $f(x, y) = 3 \cdot x \cdot y$ along the line segment from $(2, 2)$ to $(0, 3)$.

- $3 \cdot \sqrt{5}$
- $\frac{9 \cdot \sqrt{5}}{8}$
- $7 \cdot \sqrt{5}$
- $\frac{15}{2}$
- $\sqrt{5}$

[Source worked solution absent.]


## Generated evidence variant q-39954

Profile: `source:q-39954`; evidence-only: True. Parameters: `{"a": 1, "b": 3, "c": 2, "dx": 3, "dy": -1}`.

Evaluate the integral of the function $f(x, y) = 2xy$ along the line segment from $(1, 3)$ to $(4, 2)$.

- $12 \cdot \sqrt{10}$
- $2 \cdot \sqrt{10}$
- $\frac{3 \cdot \sqrt{10}}{4}$
- $\frac{2 \cdot \sqrt{10}}{3}$
- $\frac{15}{3}$

[Source worked solution absent.]


## Generated evidence variant q-76565

Profile: `source:q-76565`; evidence-only: True. Parameters: `{"a": 4, "b": 0, "c": 4, "d": -3, "dx": -8, "dy": 0}`.

Evaluate the integral of the function $f(x, y) = (4 \cdot x - 3 \cdot y)$ along the line segment from $(4, 0)$ to $(-4, 0)$.

- $4$
- $0$
- $128$
- $16$
- $4 \cdot \sqrt{2}$

[Source worked solution absent.]


## Generated evidence variant q-76565

Profile: `source:q-76565`; evidence-only: True. Parameters: `{"a": 2, "b": 0, "c": 2, "d": -3, "dx": -4, "dy": 0}`.

Evaluate the integral of the function $f(x, y) = 2x - 3y$ along the line segment from $(2, 0)$ to $(-2, 0)$.

- $0$
- $2 \cdot \sqrt{2}$
- $2$
- $16$
- $4$

[Source worked solution absent.]


## Generated evidence variant q-123363

Profile: `source:q-123363`; evidence-only: True. Parameters: `{"a": 4, "b": 0, "dx": 0, "dy": 4, "k": 4}`.

Evaluate the integral of the function $f(x,y)=(x + 2 \cdot \sqrt{y})$ along the line segment from $(4,0)$ to $(4,4).$

- $\frac{80}{3}$
- $12$
- $\frac{11}{2}$
- $5$
- $\frac{77}{3}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(4,0)$ to $(4,4).$ 

The position vectors of the endpoints of our line segment are $a=((4)\,i+(0)\,j)$ and $b=((4)\,i+(4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =((4)\,i+(0)\,j)+t[(((4)\,i+(4)\,j))-((4)\,i+(0)\,j)] \\  & =((4)\,i+(0)\,j)+4 \cdot t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4$ and $y=4 \cdot t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4)i+\frac{\text{d}}{\text{d}t}(4 \cdot t)j \\  & =((0)\,i+(4)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =4 \\  & =4\end{aligned}
$$

Now, since $f(x,y)=(x + 2 \cdot \sqrt{y})$, we obtain

$$
\begin{aligned}f(r(t)) & =4+\sqrt{4(4 \cdot t)} \\  & =(4 \cdot \sqrt{t} + 4).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}((4 \cdot \sqrt{t} + 4))\cdot 4\cdot \text{d}t \\  & =16{\int }_{0}^{1}(1+\sqrt{t})\text{d}t \\  & =16{[t+\frac{2{t}^{3/2}}{3}]}_{0}^{1} \\  & =16(1+\frac{2}{3})-0 \\  & =\frac{80}{3}.\end{aligned}
$$


## Generated evidence variant q-123363

Profile: `source:q-123363`; evidence-only: True. Parameters: `{"a": 2, "b": 0, "dx": 0, "dy": 4, "k": 1}`.

Evaluate the integral of the function $f(x,y)=(x + \sqrt{y})$ along the line segment from $(2,0)$ to $(2,4).$

- $\frac{13}{6}$
- $3$
- $\frac{40}{3}$
- $\frac{37}{3}$
- $6$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,0)$ to $(2,4).$ 

The position vectors of the endpoints of our line segment are $a=2\,i$ and $b=((2)\,i+(4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =2\,i+t[(((2)\,i+(4)\,j))-2\,i] \\  & =2\,i+4 \cdot t\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2$ and $y=4 \cdot t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2)i+\frac{\text{d}}{\text{d}t}(4 \cdot t)j \\  & =((0)\,i+(4)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =4 \\  & =4\end{aligned}
$$

Now, since $f(x,y)=(x + \sqrt{y})$, we obtain

$$
\begin{aligned}f(r(t)) & =2+\sqrt{1(4 \cdot t)} \\  & =2+2\sqrt{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2+2\sqrt{t})\cdot 4\cdot \text{d}t \\  & =8{\int }_{0}^{1}(1+\sqrt{t})\text{d}t \\  & =8{[t+\frac{2{t}^{3/2}}{3}]}_{0}^{1} \\  & =8(1+\frac{2}{3})-0 \\  & =\frac{40}{3}.\end{aligned}
$$


## Generated evidence variant q-123366

Profile: `source:q-123366`; evidence-only: True. Parameters: `{"a": 0, "b": 0, "c": -3, "d": 1, "dx": 1, "dy": 2}`.

Evaluate the integral of the function $f(x,y)=e^{- 3 \cdot x + y}$ along the line segment from $(0,0)$ to $(1,2).$

- $-1 + \frac{2}{e}$
- $-2 + \frac{2}{e}$
- $-2 + \frac{2}{e^{2}}$
- $- \frac{\sqrt{5} \cdot \left(1 - e\right)}{e}$
- $- \frac{\sqrt{5} \cdot \left(1 - e^{2}\right)}{e^{2}}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(1,2).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=((1)\,i+(2)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t\,(b) \\  & =t(((1)\,i+(2)\,j)) \\  & =((t)\,i+(2 \cdot t)\,j)\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t$ and $y=2 \cdot t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2 \cdot t)j \\  & =((1)\,i+(2)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{5} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=e^{- 3 \cdot x + y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{-3(t)+2 \cdot t} \\  & =e^{- t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}e^{- t}\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}e^{- t}\,\text{d}t \\  & =\sqrt{5}[- e^{- t}]_{0}^{1} \\  & =\sqrt{5}((1 - e^{-1})).\end{aligned}
$$


## Generated evidence variant q-123366

Profile: `source:q-123366`; evidence-only: True. Parameters: `{"a": 0, "b": 0, "c": 1, "d": 1, "dx": 2, "dy": -4}`.

Evaluate the integral of the function $f(x,y)=e^{x + y}$ along the line segment from $(0,0)$ to $(2,-4).$

- $4 - \frac{4}{e^{2}}$
- $- \frac{\sqrt{5} \cdot \left(1 - e^{2}\right)}{e^{2}}$
- $-1 - \frac{4}{e^{2}}$
- $4 - \frac{4}{e^{4}}$
- $- \frac{\sqrt{5} \cdot \left(1 - e^{4}\right)}{e^{4}}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(0,0)$ to $(2,-4).$ 

The position vectors of the endpoints of our line segment are $a=0$ and $b=((2)\,i+(-4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t\,(b) \\  & =t(((2)\,i+(-4)\,j)) \\  & =((2 \cdot t)\,i+(- 4 \cdot t)\,j)\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t$ and $y=- 4 \cdot t$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 \cdot t)i+\frac{\text{d}}{\text{d}t}(- 4 \cdot t)j \\  & =((2)\,i+(-4)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =2 \cdot \sqrt{5} \\  & =2 \cdot \sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=e^{x + y}$, we obtain

$$
\begin{aligned}f(r(t)) & ={e}^{1(2 \cdot t)+- 4 \cdot t} \\  & =e^{- 2 \cdot t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}e^{- 2 \cdot t}\cdot 2 \cdot \sqrt{5}\cdot \text{d}t \\  & =2 \cdot \sqrt{5}{\int }_{0}^{1}e^{- 2 \cdot t}\,\text{d}t \\  & =2 \cdot \sqrt{5}[- \frac{e^{- 2 \cdot t}}{2}]_{0}^{1} \\  & =2 \cdot \sqrt{5}(- \frac{1 - e^{2}}{2 \cdot e^{2}}).\end{aligned}
$$


## Generated evidence variant q-76564

Profile: `source:q-76564`; evidence-only: True. Parameters: `{"a": 2, "b": 2, "c": 2, "dx": 1, "dy": 2}`.

Evaluate the integral of the function $f(x,y)=2 \cdot x \cdot y$ along the line segment from $(2,2)$ to $(3,4).$

- $\frac{\sqrt{5}}{2}$
- $\frac{92 \cdot \sqrt{5}}{3}$
- $\frac{23 \cdot \sqrt{5}}{3}$
- $\frac{46 \cdot \sqrt{5}}{3}$
- $1$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(2,2)$ to $(3,4).$

The position vectors of the endpoints of our line segment are $a=((2)\,i+(2)\,j)$ and $b=((3)\,i+(4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(((2)\,i+(2)\,j))+t[((3)\,i+(4)\,j)-(((2)\,i+(2)\,j))] \\  & =(((2)\,i+(2)\,j))+t(((1)\,i+(2)\,j)) \\  & =((t + 2))\,i+((2 \cdot t + 2))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=(t + 2)$ and $y=(2 \cdot t + 2)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}((t + 2))i+\frac{\text{d}}{\text{d}t}((2 \cdot t + 2))j \\  & =((1)\,i+(2)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{5} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=2 \cdot x \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =2((t + 2))((2 \cdot t + 2)) \\  & =(4 \cdot t^{2} + 12 \cdot t + 8).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}((4 \cdot t^{2} + 12 \cdot t + 8))\cdot \sqrt{5}\cdot \text{d}t \\  & =\sqrt{5}{\int }_{0}^{1}((4 \cdot t^{2} + 12 \cdot t + 8))\,\text{d}t \\  & =\sqrt{5}{[\frac{2 \cdot t \cdot \left(2 \cdot t^{2} + 9 \cdot t + 12\right)}{3}]}_{0}^{1} \\  & =\sqrt{5}(\frac{4}{3}+6+8)-0 \\  & =\frac{46 \cdot \sqrt{5}}{3}.\end{aligned}
$$


## Generated evidence variant q-76564

Profile: `source:q-76564`; evidence-only: True. Parameters: `{"a": 1, "b": 3, "c": 2, "dx": 3, "dy": -1}`.

Evaluate the integral of the function $f(x,y)=2 \cdot x \cdot y$ along the line segment from $(1,3)$ to $(4,2).$

- $12 \cdot \sqrt{10}$
- $24 \cdot \sqrt{10}$
- $- 12 \cdot \sqrt{10}$
- $\frac{\sqrt{10}}{2}$
- $- \frac{\sqrt{3}}{2}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,3)$ to $(4,2).$

The position vectors of the endpoints of our line segment are $a=((1)\,i+(3)\,j)$ and $b=((4)\,i+(2)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(((1)\,i+(3)\,j))+t[((4)\,i+(2)\,j)-(((1)\,i+(3)\,j))] \\  & =(((1)\,i+(3)\,j))+t(((3)\,i+(-1)\,j)) \\  & =(1+3t)\,i+((3 - t))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1+3t$ and $y=(3 - t)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(1+3t)i+\frac{\text{d}}{\text{d}t}((3 - t))j \\  & =((3)\,i+(-1)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{10} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)=2 \cdot x \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(1+3t)((3 - t)) \\  & =(- 6 \cdot t^{2} + 16 \cdot t + 6).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}((- 6 \cdot t^{2} + 16 \cdot t + 6))\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}((- 6 \cdot t^{2} + 16 \cdot t + 6))\,\text{d}t \\  & =\sqrt{10}{[2 \cdot t \cdot \left(- t^{2} + 4 \cdot t + 3\right)]}_{0}^{1} \\  & =\sqrt{10}(-2+8+6)-0 \\  & =12 \cdot \sqrt{10}.\end{aligned}
$$


## Generated evidence variant q-76605

Profile: `source:q-76605`; evidence-only: True. Parameters: `{"a": 3, "b": 3, "dx": 2, "dy": -2, "n": 16}`.

Evaluate the integral ${\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{16})\,\text{d}s$ along the line segment from $(3,3)$ to $(5,1).$

- $- \frac{2 \cdot \sqrt{2}}{\pi}$
- $\frac{\sqrt{2} \cdot \pi}{2}$
- $\frac{4}{\pi }$
- $\frac{8 \cdot \sqrt{2}}{\pi}$
- $\frac{\pi }{4}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(3,3)$ to $(5,1).$ 

The position vectors of the endpoints of our line segment are $a=((3)\,i+(3)\,j)$ and $b=((5)\,i+(1)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(((3)\,i+(3)\,j))+t[((5)\,i+(1)\,j)-(((3)\,i+(3)\,j))] \\  & =(((3)\,i+(3)\,j))+t(((2)\,i+(-2)\,j)) \\  & =((2 \cdot t + 3))\,i+((3 - 2 \cdot t))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=(2 \cdot t + 3)$ and $y=(3 - 2 \cdot t)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}((2 \cdot t + 3))i+\frac{\text{d}}{\text{d}t}((3 - 2 \cdot t))j \\  & =((2)\,i+(-2)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =2 \cdot \sqrt{2} \\  & =2 \cdot \sqrt{2}\end{aligned}
$$

Now, since $f(x,y)={sec}^{2}⁡(\frac{\pi (y-x)}{16})$, we obtain

$$
\begin{aligned}f(r(t)) & ={sec}^{2}⁡(\frac{\pi (((3 - 2 \cdot t))-((2 \cdot t + 3)))}{16}) \\  & ={sec}^{2}⁡(- \frac{\pi \cdot t}{4}).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{16})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{sec}^{2}⁡(- \frac{\pi \cdot t}{4})\cdot 2 \cdot \sqrt{2}\cdot \text{d}t \\  & =2 \cdot \sqrt{2}{\int }_{0}^{1}{sec}^{2}⁡(- \frac{\pi \cdot t}{4})\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=- \frac{\pi \cdot t}{4},$ $\text{d}u=- \frac{\pi}{4}\,\text{d}t$ as follows: 

$$
\begin{aligned}2 \cdot \sqrt{2}{\int }_{0}^{1}{sec}^{2}⁡(- \frac{\pi \cdot t}{4})\,\text{d}t & =- \frac{8 \cdot \sqrt{2}}{\pi}{\int }_{0}^{- \frac{\pi}{4}}{sec}^{2}⁡u\,\text{d}u \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}\operatorname{tan}⁡u\,{|}_{0}^{- \frac{\pi}{4}} \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}(\operatorname{tan}⁡(- \frac{\pi}{4})-\operatorname{tan}⁡(0)) \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}(-1-0) \\  & =\frac{8 \cdot \sqrt{2}}{\pi}\end{aligned}
$$


## Generated evidence variant q-76605

Profile: `source:q-76605`; evidence-only: True. Parameters: `{"a": -2, "b": -2, "dx": 3, "dy": 4, "n": 3}`.

Evaluate the integral ${\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{3})\,\text{d}s$ along the line segment from $(-2,-2)$ to $(1,2).$

- $\frac{15 \cdot \sqrt{3}}{\pi}$
- $\frac{5 \cdot \sqrt{3} \cdot \pi}{3}$
- $\frac{\sqrt{3} \cdot \pi}{3}$
- $\frac{3 \cdot \sqrt{3}}{\pi}$
- $\frac{5 \cdot \sqrt{3}}{\pi}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-2,-2)$ to $(1,2).$ 

The position vectors of the endpoints of our line segment are $a=((-2)\,i+(-2)\,j)$ and $b=((1)\,i+(2)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(((-2)\,i+(-2)\,j))+t[((1)\,i+(2)\,j)-(((-2)\,i+(-2)\,j))] \\  & =(((-2)\,i+(-2)\,j))+t(((3)\,i+(4)\,j)) \\  & =((3 \cdot t - 2))\,i+((4 \cdot t - 2))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=(3 \cdot t - 2)$ and $y=(4 \cdot t - 2)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}((3 \cdot t - 2))i+\frac{\text{d}}{\text{d}t}((4 \cdot t - 2))j \\  & =((3)\,i+(4)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =5 \\  & =5\end{aligned}
$$

Now, since $f(x,y)={sec}^{2}⁡(\frac{\pi (y-x)}{3})$, we obtain

$$
\begin{aligned}f(r(t)) & ={sec}^{2}⁡(\frac{\pi (((4 \cdot t - 2))-((3 \cdot t - 2)))}{3}) \\  & ={sec}^{2}⁡(\frac{\pi \cdot t}{3}).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{sec}^{2}⁡(\frac{\pi (y-x)}{3})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi \cdot t}{3})\cdot 5\cdot \text{d}t \\  & =5{\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi \cdot t}{3})\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=\frac{\pi \cdot t}{3},$ $\text{d}u=\frac{\pi}{3}\,\text{d}t$ as follows: 

$$
\begin{aligned}5{\int }_{0}^{1}{sec}^{2}⁡(\frac{\pi \cdot t}{3})\,\text{d}t & =\frac{15}{\pi}{\int }_{0}^{\frac{\pi}{3}}{sec}^{2}⁡u\,\text{d}u \\  & =\frac{15}{\pi}\operatorname{tan}⁡u\,{|}_{0}^{\frac{\pi}{3}} \\  & =\frac{15}{\pi}(\operatorname{tan}⁡(\frac{\pi}{3})-\operatorname{tan}⁡(0)) \\  & =\frac{15}{\pi}(\sqrt{3}-0) \\  & =\frac{15 \cdot \sqrt{3}}{\pi}\end{aligned}
$$


## Generated evidence variant q-76650

Profile: `source:q-76650`; evidence-only: True. Parameters: `{"a": 1, "b": 2, "dx": 2, "dy": 2}`.

Evaluate the integral ${\int }_{C}(4x+2)\,{e}^{xy}\,\text{d}s$ along the line segment from $(1,2)$ to $(3,4).$

- $- e^{2} + e^{12}$
- $- 2 \cdot \sqrt{2} \cdot \left(1 - e^{9}\right) \cdot e^{3}$
- $- 2 \cdot \left(1 - e^{10}\right) \cdot e^{2}$
- $- 2 \cdot \sqrt{2} \cdot \left(1 - e^{10}\right) \cdot e^{2}$
- $- \sqrt{2} \cdot \left(1 - e^{10}\right) \cdot e^{2}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(1,2)$ to $(3,4).$ 

The position vectors of the endpoints of our line segment are $a=((1)\,i+(2)\,j)$ and $b=((3)\,i+(4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =((1)\,i+(2)\,j)+t[((3)\,i+(4)\,j)-((1)\,i+(2)\,j)] \\  & =((1)\,i+(2)\,j)+t(2\,i+2\,j) \\  & =(2 \cdot t + 1)\,i+((2 \cdot t + 2))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=(2 \cdot t + 1)$ and $y=(2 \cdot t + 2)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}((2 \cdot t + 1))i+\frac{\text{d}}{\text{d}t}((2 \cdot t + 2))j \\  & =2\,i+2\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{2}^{2}+{2}^{2}} \\  & =2\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=(4x+2)\,{e}^{xy}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4((2 \cdot t + 1))+2){e}^{(2 \cdot t + 1)((2 \cdot t + 2))} \\  & =((8 \cdot t + 6))\,{e}^{(4 \cdot t^{2} + 6 \cdot t + 2)}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{e}^{xy}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}((8 \cdot t + 6))\,{e}^{(4 \cdot t^{2} + 6 \cdot t + 2)}\cdot 2\sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{1}((8 \cdot t + 6))\,{e}^{(4 \cdot t^{2} + 6 \cdot t + 2)}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=(4 \cdot t^{2} + 6 \cdot t + 2),$ $\text{d}u=((8 \cdot t + 6))\,\text{d}t$ as follows:  

$$
\begin{aligned}2\sqrt{2}{\int }_{0}^{1}((8 \cdot t + 6))\,{e}^{(4 \cdot t^{2} + 6 \cdot t + 2)}\,\text{d}t & =2\sqrt{2}{\int }_{2}^{12}{e}^{u}\,\text{d}u \\  & =2\sqrt{2}\,{e}^{u}\,{|}_{2}^{12} \\  & =2\sqrt{2}({e}^{12}-{e}^{2}) \\  & =2\sqrt{2}((- e^{2} + e^{12}))\end{aligned}
$$


## Generated evidence variant q-76650

Profile: `source:q-76650`; evidence-only: True. Parameters: `{"a": -1, "b": 3, "dx": 3, "dy": 1}`.

Evaluate the integral ${\int }_{C}2 \cdot \left(x + 5\right) \cdot e^{x \cdot y}\,\text{d}s$ along the line segment from $(-1,3)$ to $(2,4).$

- $- \frac{1 - e^{11}}{e^{3}}$
- $- \frac{\sqrt{10} \cdot \left(1 - e^{10}\right)}{e^{2}}$
- $- \frac{3 - 3 \cdot e^{11}}{e^{3}}$
- $- \frac{\sqrt{10} \cdot \left(1 - e^{11}\right)}{2 \cdot e^{3}}$
- $- \frac{\sqrt{10} \cdot \left(1 - e^{11}\right)}{e^{3}}$

We will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,
$$

 

where $C$ is the line segment from $(-1,3)$ to $(2,4).$ 

The position vectors of the endpoints of our line segment are $a=((-1)\,i+(3)\,j)$ and $b=((2)\,i+(4)\,j).$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =((-1)\,i+(3)\,j)+t[((2)\,i+(4)\,j)-((-1)\,i+(3)\,j)] \\  & =((-1)\,i+(3)\,j)+t(((3)\,i+(1)\,j)) \\  & =(3 \cdot t - 1)\,i+((t + 3))\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=(3 \cdot t - 1)$ and $y=(t + 3)$ along the segment.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}((3 \cdot t - 1))i+\frac{\text{d}}{\text{d}t}((t + 3))j \\  & =((3)\,i+(1)\,j) \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{10} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)=2 \cdot \left(x + 5\right) \cdot e^{x \cdot y}$, we obtain

$$
\begin{aligned}f(r(t)) & =(2((3 \cdot t - 1))+10){e}^{(3 \cdot t - 1)((t + 3))} \\  & =((6 \cdot t + 8))\,{e}^{(3 \cdot t^{2} + 8 \cdot t - 3)}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}{e}^{xy}\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}((6 \cdot t + 8))\,{e}^{(3 \cdot t^{2} + 8 \cdot t - 3)}\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}((6 \cdot t + 8))\,{e}^{(3 \cdot t^{2} + 8 \cdot t - 3)}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=(3 \cdot t^{2} + 8 \cdot t - 3),$ $\text{d}u=((6 \cdot t + 8))\,\text{d}t$ as follows:  

$$
\begin{aligned}\sqrt{10}{\int }_{0}^{1}((6 \cdot t + 8))\,{e}^{(3 \cdot t^{2} + 8 \cdot t - 3)}\,\text{d}t & =\sqrt{10}{\int }_{-3}^{8}{e}^{u}\,\text{d}u \\  & =\sqrt{10}\,{e}^{u}\,{|}_{-3}^{8} \\  & =\sqrt{10}({e}^{8}-{e}^{-3}) \\  & =\sqrt{10}(- \frac{1 - e^{11}}{e^{3}})\end{aligned}
$$


## Generated easy / linear

Profile: `method`; evidence-only: False. Parameters: `{"a": 0, "b": 0, "c": 1, "d": 3, "dx": 2, "dy": 3}`.

Evaluate the integral of the function $f(x,y)=x + 3 \cdot y$ along the line segment from $(0,0)$ to $(2,3).$

- $0$
- $\frac{11 \cdot \sqrt{13}}{2}$
- $11 \cdot \sqrt{13}$
- $\frac{11 \cdot \sqrt{13}}{8}$
- $\frac{11}{2}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(0,0)$ to $(2,3).$

The position vectors of the endpoints of our line segment are $a=(0)\,i+(0)\,j$ and $b=(2)\,i+(3)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(0)\,i+(0)\,j+t[((2)\,i+(3)\,j)-((0)\,i+(0)\,j)] \\  & =(0)\,i+(0)\,j+t((2)\,i+(3)\,j) \\  & =(2 \cdot t)\,i+(3 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t$ and $y=3 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t)i+\frac{\mathrm{d}}{\mathrm{d}t}(3 \cdot t)j \\  & =(2)\,i+(3)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(2)^2+(3)^2} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=x + 3 \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =1(2 \cdot t)+3(3 \cdot t) \\  & =11 \cdot t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x + 3 \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (11 \cdot t)\cdot \sqrt{13}\,\mathrm{d}t \\  & =\sqrt{13}\int_0^1 (11 \cdot t)\,\mathrm{d}t \\  & =\sqrt{13}[\frac{11 \cdot t^{2}}{2}]_0^1 \\  & =\sqrt{13}((\frac{11}{2})+(0))-\sqrt{13}(0) \\  & =\frac{11 \cdot \sqrt{13}}{2}\end{aligned}
$$


## Generated easy / linear

Profile: `method`; evidence-only: False. Parameters: `{"a": -2, "b": 1, "c": -3, "d": 2, "dx": -3, "dy": 2}`.

Evaluate the integral of the function $f(x,y)=- 3 \cdot x + 2 \cdot y$ along the line segment from $(-2,1)$ to $(-5,3).$

- $\frac{29 \cdot \sqrt{13}}{2}$
- $\frac{29}{2}$
- $8 \cdot \sqrt{13}$
- $\frac{45 \cdot \sqrt{13}}{8}$
- $21 \cdot \sqrt{13}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(-2,1)$ to $(-5,3).$

The position vectors of the endpoints of our line segment are $a=(-2)\,i+(1)\,j$ and $b=(-5)\,i+(3)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-2)\,i+(1)\,j+t[((-5)\,i+(3)\,j)-((-2)\,i+(1)\,j)] \\  & =(-2)\,i+(1)\,j+t((-3)\,i+(2)\,j) \\  & =(- 3 \cdot t - 2)\,i+(2 \cdot t + 1)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=- 3 \cdot t - 2$ and $y=2 \cdot t + 1$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(- 3 \cdot t - 2)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 1)j \\  & =(-3)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(-3)^2+(2)^2} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=- 3 \cdot x + 2 \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =-3(- 3 \cdot t - 2)+2(2 \cdot t + 1) \\  & =13 \cdot t + 8.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 \cdot x + 2 \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (13 \cdot t + 8)\cdot \sqrt{13}\,\mathrm{d}t \\  & =\sqrt{13}\int_0^1 (13 \cdot t + 8)\,\mathrm{d}t \\  & =\sqrt{13}[\frac{13 \cdot t^{2}}{2} + 8 \cdot t]_0^1 \\  & =\sqrt{13}((\frac{13}{2})+(8))-\sqrt{13}(0) \\  & =\frac{29 \cdot \sqrt{13}}{2}\end{aligned}
$$


## Generated easy / odd_linear

Profile: `method`; evidence-only: False. Parameters: `{"a": 4, "b": 0, "c": 4, "d": -3, "dx": -8, "dy": 0}`.

Evaluate the integral of the function $f(x,y)=4 \cdot x - 3 \cdot y$ along the line segment from $(4,0)$ to $(-4,0).$

- $16$
- $-128$
- $64$
- $128$
- $0$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(4,0)$ to $(-4,0).$

The position vectors of the endpoints of our line segment are $a=(4)\,i+(0)\,j$ and $b=(-4)\,i+(0)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(4)\,i+(0)\,j+t[((-4)\,i+(0)\,j)-((4)\,i+(0)\,j)] \\  & =(4)\,i+(0)\,j+t((-8)\,i+(0)\,j) \\  & =(4 - 8 \cdot t)\,i+(0)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4 - 8 \cdot t$ and $y=0$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(4 - 8 \cdot t)i+\frac{\mathrm{d}}{\mathrm{d}t}(0)j \\  & =(-8)\,i+(0)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(-8)^2+(0)^2} \\  & =8\end{aligned}
$$

Now, since $f(x,y)=4 \cdot x - 3 \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =4(4 - 8 \cdot t)+-3(0) \\  & =16 - 32 \cdot t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 4 \cdot x - 3 \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (16 - 32 \cdot t)\cdot 8\,\mathrm{d}t \\  & =8\int_0^1 (16 - 32 \cdot t)\,\mathrm{d}t \\  & =8[- 16 \cdot t^{2} + 16 \cdot t]_0^1 \\  & =8((-16)+(16))-8(0) \\  & =0\end{aligned}
$$


## Generated easy / odd_linear

Profile: `method`; evidence-only: False. Parameters: `{"a": 2, "b": 0, "c": 1, "d": -3, "dx": -4, "dy": 0}`.

Evaluate the integral of the function $f(x,y)=x - 3 \cdot y$ along the line segment from $(2,0)$ to $(-2,0).$

- $4$
- $2$
- $-8$
- $0$
- $8$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(2,0)$ to $(-2,0).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(0)\,j$ and $b=(-2)\,i+(0)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2)\,i+(0)\,j+t[((-2)\,i+(0)\,j)-((2)\,i+(0)\,j)] \\  & =(2)\,i+(0)\,j+t((-4)\,i+(0)\,j) \\  & =(2 - 4 \cdot t)\,i+(0)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 - 4 \cdot t$ and $y=0$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 - 4 \cdot t)i+\frac{\mathrm{d}}{\mathrm{d}t}(0)j \\  & =(-4)\,i+(0)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(-4)^2+(0)^2} \\  & =4\end{aligned}
$$

Now, since $f(x,y)=x - 3 \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =1(2 - 4 \cdot t)+-3(0) \\  & =2 - 4 \cdot t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x - 3 \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (2 - 4 \cdot t)\cdot 4\,\mathrm{d}t \\  & =4\int_0^1 (2 - 4 \cdot t)\,\mathrm{d}t \\  & =4[- 2 \cdot t^{2} + 2 \cdot t]_0^1 \\  & =4((-2)+(2))-4(0) \\  & =0\end{aligned}
$$


## Generated moderate / product

Profile: `method`; evidence-only: False. Parameters: `{"a": 2, "b": 2, "c": 3, "dx": -2, "dy": 1}`.

Evaluate the integral of the function $f(x,y)=3 \cdot x \cdot y$ along the line segment from $(2,2)$ to $(0,3).$

- $7 \cdot \sqrt{5}$
- $10 \cdot \sqrt{5}$
- $7$
- $6 \cdot \sqrt{5}$
- $9 \cdot \sqrt{5}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(2,2)$ to $(0,3).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(2)\,j$ and $b=(0)\,i+(3)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2)\,i+(2)\,j+t[((0)\,i+(3)\,j)-((2)\,i+(2)\,j)] \\  & =(2)\,i+(2)\,j+t((-2)\,i+(1)\,j) \\  & =(2 - 2 \cdot t)\,i+(t + 2)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 - 2 \cdot t$ and $y=t + 2$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 - 2 \cdot t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t + 2)j \\  & =(-2)\,i+(1)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(-2)^2+(1)^2} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=3 \cdot x \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =3(2 - 2 \cdot t)(t + 2) \\  & =- 6 \cdot t^{2} - 6 \cdot t + 12.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 3 \cdot x \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (- 6 \cdot t^{2} - 6 \cdot t + 12)\cdot \sqrt{5}\,\mathrm{d}t \\  & =\sqrt{5}\int_0^1 (- 6 \cdot t^{2} - 6 \cdot t + 12)\,\mathrm{d}t \\  & =\sqrt{5}[- 2 \cdot t^{3} - 3 \cdot t^{2} + 12 \cdot t]_0^1 \\  & =\sqrt{5}((-2)+(-3)+(12))-\sqrt{5}(0) \\  & =7 \cdot \sqrt{5}\end{aligned}
$$


## Generated moderate / product

Profile: `method`; evidence-only: False. Parameters: `{"a": 2, "b": 2, "c": 2, "dx": 2, "dy": 4}`.

Evaluate the integral of the function $f(x,y)=2 \cdot x \cdot y$ along the line segment from $(2,2)$ to $(4,6).$

- $\frac{80 \cdot \sqrt{5}}{3}$
- $40 \cdot \sqrt{5}$
- $56 \cdot \sqrt{5}$
- $\frac{152 \cdot \sqrt{5}}{3}$
- $\frac{76}{3}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(2,2)$ to $(4,6).$

The position vectors of the endpoints of our line segment are $a=(2)\,i+(2)\,j$ and $b=(4)\,i+(6)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(2)\,i+(2)\,j+t[((4)\,i+(6)\,j)-((2)\,i+(2)\,j)] \\  & =(2)\,i+(2)\,j+t((2)\,i+(4)\,j) \\  & =(2 \cdot t + 2)\,i+(4 \cdot t + 2)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t + 2$ and $y=4 \cdot t + 2$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 2)i+\frac{\mathrm{d}}{\mathrm{d}t}(4 \cdot t + 2)j \\  & =(2)\,i+(4)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(2)^2+(4)^2} \\  & =2 \cdot \sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=2 \cdot x \cdot y$, we obtain

$$
\begin{aligned}f(r(t)) & =2(2 \cdot t + 2)(4 \cdot t + 2) \\  & =16 \cdot t^{2} + 24 \cdot t + 8.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 \cdot x \cdot y\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (16 \cdot t^{2} + 24 \cdot t + 8)\cdot 2 \cdot \sqrt{5}\,\mathrm{d}t \\  & =2 \cdot \sqrt{5}\int_0^1 (16 \cdot t^{2} + 24 \cdot t + 8)\,\mathrm{d}t \\  & =2 \cdot \sqrt{5}[\frac{16 \cdot t^{3}}{3} + 12 \cdot t^{2} + 8 \cdot t]_0^1 \\  & =2 \cdot \sqrt{5}((\frac{16}{3})+(12)+(8))-2 \cdot \sqrt{5}(0) \\  & =\frac{152 \cdot \sqrt{5}}{3}\end{aligned}
$$


## Generated moderate / radical

Profile: `method`; evidence-only: False. Parameters: `{"a": 4, "b": 0, "dx": 0, "dy": 4, "k": 4}`.

Evaluate the integral of the function $f(x,y)=x + 2 \cdot \sqrt{y}$ along the line segment from $(4,0)$ to $(4,4).$

- $40$
- $32$
- $\frac{20}{3}$
- $\frac{80}{3}$
- $24$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(4,0)$ to $(4,4).$

The position vectors of the endpoints of our line segment are $a=(4)\,i+(0)\,j$ and $b=(4)\,i+(4)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(4)\,i+(0)\,j+t[((4)\,i+(4)\,j)-((4)\,i+(0)\,j)] \\  & =(4)\,i+(4 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=4$ and $y=4 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(4)i+\frac{\mathrm{d}}{\mathrm{d}t}(4 \cdot t)j \\  & =(0)\,i+(4)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(0)^2+(4)^2} \\  & =4\end{aligned}
$$

Now, since $f(x,y)=x + 2 \cdot \sqrt{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =4+\sqrt{4(4 \cdot t)} \\  & =4 \cdot \sqrt{t} + 4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x + 2 \cdot \sqrt{y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (4 \cdot \sqrt{t} + 4)\cdot 4\,\mathrm{d}t \\  & =16\int_0^1 (\sqrt{t} + 1)\,\mathrm{d}t \\  & =16[\frac{2 \cdot t^{\frac{3}{2}}}{3} + t]_0^1 \\  & =16(1+\frac{2}{3})-0 \\  & =\frac{80}{3}\end{aligned}
$$


## Generated moderate / radical

Profile: `method`; evidence-only: False. Parameters: `{"a": 1, "b": 0, "dx": 0, "dy": 4, "k": 1}`.

Evaluate the integral of the function $f(x,y)=x + \sqrt{y}$ along the line segment from $(1,0)$ to $(1,4).$

- $8$
- $16$
- $\frac{7}{3}$
- $\frac{28}{3}$
- $12$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(1,0)$ to $(1,4).$

The position vectors of the endpoints of our line segment are $a=(1)\,i+(0)\,j$ and $b=(1)\,i+(4)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(1)\,i+(0)\,j+t[((1)\,i+(4)\,j)-((1)\,i+(0)\,j)] \\  & =(1)\,i+(4 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=1$ and $y=4 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(1)i+\frac{\mathrm{d}}{\mathrm{d}t}(4 \cdot t)j \\  & =(0)\,i+(4)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(0)^2+(4)^2} \\  & =4\end{aligned}
$$

Now, since $f(x,y)=x + \sqrt{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =1+\sqrt{1(4 \cdot t)} \\  & =2 \cdot \sqrt{t} + 1.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x + \sqrt{y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (2 \cdot \sqrt{t} + 1)\cdot 4\,\mathrm{d}t \\  & =4\int_0^1 (2 \cdot \sqrt{t} + 1)\,\mathrm{d}t \\  & =4[\frac{4 \cdot t^{\frac{3}{2}}}{3} + t]_0^1 \\  & =4(1+\frac{4}{3})-0 \\  & =\frac{28}{3}\end{aligned}
$$


## Generated moderate / exponential

Profile: `method`; evidence-only: False. Parameters: `{"a": 0, "b": 0, "c": -3, "d": 1, "dx": 1, "dy": 2}`.

Evaluate the integral of the function $f(x,y)=e^{- 3 \cdot x + y}$ along the line segment from $(0,0)$ to $(1,2).$

- $- \frac{\sqrt{5} \cdot \left(1 - e\right)}{e}$
- $- \frac{\sqrt{5}}{e}$
- $1 - e^{-1}$
- $- \frac{\sqrt{5} \cdot \left(1 - e^{2}\right)}{e^{2}}$
- $- \frac{\sqrt{5} \cdot \left(1 + e\right)}{e}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(0,0)$ to $(1,2).$

The position vectors of the endpoints of our line segment are $a=(0)\,i+(0)\,j$ and $b=(1)\,i+(2)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t\,(b) \\  & =t((1)\,i+(2)\,j) \\  & =(t)\,i+(2 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=t$ and $y=2 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t)j \\  & =(1)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(1)^2+(2)^2} \\  & =\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=e^{- 3 \cdot x + y}$, we obtain

$$
\begin{aligned}f(r(t)) & =e^{-3(t)+1(2 \cdot t)} \\  & =e^{- t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C e^{- 3 \cdot x + y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (e^{- t})\cdot \sqrt{5}\,\mathrm{d}t \\  & =\sqrt{5}\int_0^1 (e^{- t})\,\mathrm{d}t \\  & =\sqrt{5}[- e^{- t}]_0^1 \\  & =\sqrt{5}(- \frac{1}{e})-\sqrt{5}(-1) \\  & =- \frac{\sqrt{5} \cdot \left(1 - e\right)}{e}\end{aligned}
$$


## Generated moderate / exponential

Profile: `method`; evidence-only: False. Parameters: `{"a": 0, "b": 0, "c": 1, "d": 2, "dx": -3, "dy": 2}`.

Evaluate the integral of the function $f(x,y)=e^{x + 2 \cdot y}$ along the line segment from $(0,0)$ to $(-3,2).$

- $\sqrt{13} \cdot e$
- $\sqrt{13} \cdot \left(1 + e\right)$
- $\sqrt{13} \cdot \left(-1 + e\right)$
- $-1 + e$
- $- \sqrt{13} \cdot \left(1 - e^{2}\right)$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(0,0)$ to $(-3,2).$

The position vectors of the endpoints of our line segment are $a=(0)\,i+(0)\,j$ and $b=(-3)\,i+(2)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0+t\,(b-0) \\  & =t\,(b) \\  & =t((-3)\,i+(2)\,j) \\  & =(- 3 \cdot t)\,i+(2 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=- 3 \cdot t$ and $y=2 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(- 3 \cdot t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t)j \\  & =(-3)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(-3)^2+(2)^2} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=e^{x + 2 \cdot y}$, we obtain

$$
\begin{aligned}f(r(t)) & =e^{1(- 3 \cdot t)+2(2 \cdot t)} \\  & =e^{t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C e^{x + 2 \cdot y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (e^{t})\cdot \sqrt{13}\,\mathrm{d}t \\  & =\sqrt{13}\int_0^1 (e^{t})\,\mathrm{d}t \\  & =\sqrt{13}[e^{t}]_0^1 \\  & =\sqrt{13}(e)-\sqrt{13}(1) \\  & =\sqrt{13} \cdot \left(-1 + e\right)\end{aligned}
$$


## Generated hard / secant

Profile: `method`; evidence-only: False. Parameters: `{"a": 3, "b": 3, "dx": 2, "dy": -2, "n": 16}`.

Evaluate the integral $\int_C \sec^{2}{\left(\pi \cdot \left(- \frac{x}{16} + \frac{y}{16}\right) \right)}\,\mathrm{d}s$ along the line segment from $(3,3)$ to $(5,1).$

- $- 2 \cdot \sqrt{2}$
- $\frac{\sqrt{2} \cdot \pi}{2}$
- $\frac{4}{\pi}$
- $\frac{8 \cdot \sqrt{2}}{\pi}$
- $\frac{\pi}{4}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(3,3)$ to $(5,1).$

The position vectors of the endpoints of our line segment are $a=(3)\,i+(3)\,j$ and $b=(5)\,i+(1)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(3)\,i+(3)\,j+t[((5)\,i+(1)\,j)-((3)\,i+(3)\,j)] \\  & =(3)\,i+(3)\,j+t((2)\,i+(-2)\,j) \\  & =(2 \cdot t + 3)\,i+(3 - 2 \cdot t)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t + 3$ and $y=3 - 2 \cdot t$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 3)i+\frac{\mathrm{d}}{\mathrm{d}t}(3 - 2 \cdot t)j \\  & =(2)\,i+(-2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(2)^2+(-2)^2} \\  & =2 \cdot \sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\sec^{2}{\left(\pi \cdot \left(- \frac{x}{16} + \frac{y}{16}\right) \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sec^2\left(\frac{\pi((3 - 2 \cdot t)-(2 \cdot t + 3))}{16}\right) \\  & =\sec^2\left(- \frac{\pi \cdot t}{4}\right).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C \sec^{2}{\left(\pi \cdot \left(- \frac{x}{16} + \frac{y}{16}\right) \right)}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (\sec^2\left(- \frac{\pi \cdot t}{4}\right))\cdot 2 \cdot \sqrt{2}\,\mathrm{d}t \\  & =2 \cdot \sqrt{2}\int_0^1 (\sec^2\left(- \frac{\pi \cdot t}{4}\right))\,\mathrm{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{\pi \cdot t}{4},$ $\mathrm{d}u=(- \frac{\pi}{4})\,\mathrm{d}t$ as follows: 

$$
\begin{aligned}2 \cdot \sqrt{2}\int_0^1 \sec^{2}{\left(\frac{\pi \cdot t}{4} \right)}\,\mathrm{d}t & =- \frac{8 \cdot \sqrt{2}}{\pi}\int_{0}^{- \frac{\pi}{4}}\sec^2 u\,\mathrm{d}u \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}[\tan u]_{0}^{- \frac{\pi}{4}} \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}(\tan(- \frac{\pi}{4})-\tan(0)) \\  & =- \frac{8 \cdot \sqrt{2}}{\pi}(-1-0) \\  & =\frac{8 \cdot \sqrt{2}}{\pi}\end{aligned}
$$


## Generated hard / secant

Profile: `method`; evidence-only: False. Parameters: `{"a": -2, "b": -2, "dx": 3, "dy": 2, "n": 3}`.

Evaluate the integral $\int_C \sec^{2}{\left(\pi \cdot \left(- \frac{x}{3} + \frac{y}{3}\right) \right)}\,\mathrm{d}s$ along the line segment from $(-2,-2)$ to $(1,0).$

- $\frac{\sqrt{3} \cdot \pi}{3}$
- $\frac{3 \cdot \sqrt{3}}{\pi}$
- $- \sqrt{39}$
- $\frac{\sqrt{39} \cdot \pi}{3}$
- $\frac{3 \cdot \sqrt{39}}{\pi}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(-2,-2)$ to $(1,0).$

The position vectors of the endpoints of our line segment are $a=(-2)\,i+(-2)\,j$ and $b=(1)\,i+(0)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-2)\,i+(-2)\,j+t[((1)\,i+(0)\,j)-((-2)\,i+(-2)\,j)] \\  & =(-2)\,i+(-2)\,j+t((3)\,i+(2)\,j) \\  & =(3 \cdot t - 2)\,i+(2 \cdot t - 2)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=3 \cdot t - 2$ and $y=2 \cdot t - 2$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(3 \cdot t - 2)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t - 2)j \\  & =(3)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(3)^2+(2)^2} \\  & =\sqrt{13}\end{aligned}
$$

Now, since $f(x,y)=\sec^{2}{\left(\pi \cdot \left(- \frac{x}{3} + \frac{y}{3}\right) \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =\sec^2\left(\frac{\pi((2 \cdot t - 2)-(3 \cdot t - 2))}{3}\right) \\  & =\sec^2\left(- \frac{\pi \cdot t}{3}\right).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C \sec^{2}{\left(\pi \cdot \left(- \frac{x}{3} + \frac{y}{3}\right) \right)}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 (\sec^2\left(- \frac{\pi \cdot t}{3}\right))\cdot \sqrt{13}\,\mathrm{d}t \\  & =\sqrt{13}\int_0^1 (\sec^2\left(- \frac{\pi \cdot t}{3}\right))\,\mathrm{d}t\end{aligned}
$$

We can solve this using the substitution $u=- \frac{\pi \cdot t}{3},$ $\mathrm{d}u=(- \frac{\pi}{3})\,\mathrm{d}t$ as follows: 

$$
\begin{aligned}\sqrt{13}\int_0^1 \sec^{2}{\left(\frac{\pi \cdot t}{3} \right)}\,\mathrm{d}t & =- \frac{3 \cdot \sqrt{13}}{\pi}\int_{0}^{- \frac{\pi}{3}}\sec^2 u\,\mathrm{d}u \\  & =- \frac{3 \cdot \sqrt{13}}{\pi}[\tan u]_{0}^{- \frac{\pi}{3}} \\  & =- \frac{3 \cdot \sqrt{13}}{\pi}(\tan(- \frac{\pi}{3})-\tan(0)) \\  & =- \frac{3 \cdot \sqrt{13}}{\pi}(- \sqrt{3}-0) \\  & =\frac{3 \cdot \sqrt{39}}{\pi}\end{aligned}
$$


## Generated hard / matched_exponential

Profile: `method`; evidence-only: False. Parameters: `{"a": 1, "b": 2, "dx": 2, "dy": 2}`.

Evaluate the integral $\int_C \left(4 \cdot x + 2\right) \cdot e^{x \cdot y}\,\mathrm{d}s$ along the line segment from $(1,2)$ to $(3,4).$

- $- e^{2} + e^{12}$
- $- 2 \cdot \sqrt{2} \cdot \left(1 - e^{10}\right) \cdot e^{2}$
- $- 2 \cdot \left(1 - e^{10}\right) \cdot e^{2}$
- $2 \cdot \sqrt{2} \cdot \left(1 + e^{10}\right) \cdot e^{2}$
- $- 2 \cdot \sqrt{2} \cdot \left(1 - e^{9}\right) \cdot e^{3}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(1,2)$ to $(3,4).$

The position vectors of the endpoints of our line segment are $a=(1)\,i+(2)\,j$ and $b=(3)\,i+(4)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(1)\,i+(2)\,j+t[((3)\,i+(4)\,j)-((1)\,i+(2)\,j)] \\  & =(1)\,i+(2)\,j+t((2)\,i+(2)\,j) \\  & =(2 \cdot t + 1)\,i+(2 \cdot t + 2)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t + 1$ and $y=2 \cdot t + 2$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 1)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 2)j \\  & =(2)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(2)^2+(2)^2} \\  & =2 \cdot \sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\left(4 \cdot x + 2\right) \cdot e^{x \cdot y}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4(2 \cdot t + 1)+2)e^{(2 \cdot t + 1)(2 \cdot t + 2)} \\  & =(8 \cdot t + 6)e^{4 \cdot t^{2} + 6 \cdot t + 2}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C \left(4 \cdot x + 2\right) \cdot e^{x \cdot y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 ((8 \cdot t + 6)e^{4 \cdot t^{2} + 6 \cdot t + 2})\cdot 2 \cdot \sqrt{2}\,\mathrm{d}t \\  & =2 \cdot \sqrt{2}\int_0^1 ((8 \cdot t + 6)e^{4 \cdot t^{2} + 6 \cdot t + 2})\,\mathrm{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 \cdot t^{2} + 6 \cdot t + 2,$ $\mathrm{d}u=(8 \cdot t + 6)\,\mathrm{d}t$ as follows: 

$$
\begin{aligned}2 \cdot \sqrt{2}\int_0^1 \left(8 \cdot t + 6\right) \cdot e^{4 \cdot t^{2} + 6 \cdot t + 2}\,\mathrm{d}t & =2 \cdot \sqrt{2}\int_{2}^{12}e^u\,\mathrm{d}u \\  & =2 \cdot \sqrt{2}[e^u]_{2}^{12} \\  & =2 \cdot \sqrt{2}(e^{12}-e^{2}) \\  & =- 2 \cdot \sqrt{2} \cdot \left(1 - e^{10}\right) \cdot e^{2}\end{aligned}
$$


## Generated hard / matched_exponential

Profile: `method`; evidence-only: False. Parameters: `{"a": -1, "b": 2, "dx": 2, "dy": 2}`.

Evaluate the integral $\int_C \left(4 \cdot x + 6\right) \cdot e^{x \cdot y}\,\mathrm{d}s$ along the line segment from $(-1,2)$ to $(1,4).$

- $\frac{2 \cdot \sqrt{2} \cdot \left(1 + e^{6}\right)}{e^{2}}$
- $- \frac{2 - 2 \cdot e^{6}}{e^{2}}$
- $- \frac{2 \cdot \sqrt{2} \cdot \left(1 - e^{6}\right)}{e^{2}}$
- $- \frac{1 - e^{6}}{e^{2}}$
- $- \frac{2 \cdot \sqrt{2} \cdot \left(1 - e^{5}\right)}{e}$

We will use the formula

$$
\int_C f(x,y)\,\mathrm{d}s=\int_{t_a}^{t_b} f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t,
$$

where $C$ is the line segment from $(-1,2)$ to $(1,4).$

The position vectors of the endpoints of our line segment are $a=(-1)\,i+(2)\,j$ and $b=(1)\,i+(4)\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =(-1)\,i+(2)\,j+t[((1)\,i+(4)\,j)-((-1)\,i+(2)\,j)] \\  & =(-1)\,i+(2)\,j+t((2)\,i+(2)\,j) \\  & =(2 \cdot t - 1)\,i+(2 \cdot t + 2)\,j\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x=2 \cdot t - 1$ and $y=2 \cdot t + 2$ along the segment.

Computing $r\prime(t)$ and $\|r\prime(t)\|,$ we get the following:

$$
\begin{aligned}r\prime(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t - 1)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 \cdot t + 2)j \\  & =(2)\,i+(2)\,j \\ \|r\prime(t)\| & =\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\  & =\sqrt{(2)^2+(2)^2} \\  & =2 \cdot \sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\left(4 \cdot x + 6\right) \cdot e^{x \cdot y}$, we obtain

$$
\begin{aligned}f(r(t)) & =(4(2 \cdot t - 1)+6)e^{(2 \cdot t - 1)(2 \cdot t + 2)} \\  & =(8 \cdot t + 2)e^{4 \cdot t^{2} + 2 \cdot t - 2}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C \left(4 \cdot x + 6\right) \cdot e^{x \cdot y}\,\mathrm{d}s & =\int_0^1 f(r(t))\,\|r\prime(t)\|\,\mathrm{d}t \\  & =\int_0^1 ((8 \cdot t + 2)e^{4 \cdot t^{2} + 2 \cdot t - 2})\cdot 2 \cdot \sqrt{2}\,\mathrm{d}t \\  & =2 \cdot \sqrt{2}\int_0^1 ((8 \cdot t + 2)e^{4 \cdot t^{2} + 2 \cdot t - 2})\,\mathrm{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 \cdot t^{2} + 2 \cdot t - 2,$ $\mathrm{d}u=(8 \cdot t + 2)\,\mathrm{d}t$ as follows: 

$$
\begin{aligned}2 \cdot \sqrt{2}\int_0^1 \left(8 \cdot t + 2\right) \cdot e^{4 \cdot t^{2} + 2 \cdot t - 2}\,\mathrm{d}t & =2 \cdot \sqrt{2}\int_{-2}^{4}e^u\,\mathrm{d}u \\  & =2 \cdot \sqrt{2}[e^u]_{-2}^{4} \\  & =2 \cdot \sqrt{2}(e^{4}-e^{-2}) \\  & =- \frac{2 \cdot \sqrt{2} \cdot \left(1 - e^{6}\right)}{e^{2}}\end{aligned}
$$
