# Review — scalar graph line-integral setup

Originals retain raw snapshot strings in source.json. Observed evidence replays preserve complete banks; two banks contain equal complete wrong answers. Normal authored banks reject every complete-value collision.


## Raw original q-76188

Which of the following is equivalent to the integral $\displaystyle \int_(C)\frac{y}{x}ds$, where $C$ is the section of the curve $y = \frac{x^{2}}{2}$ between the points $(0, 0)$ and $(2, 2)$?

1. $\frac{1}{2}\displaystyle \int_{0}^{2}tdt$
2. $\displaystyle \int_{0}^{2}\sqrt{1 + t^{2}}dt$
3. $\displaystyle \int_{0}^{2}t\sqrt{1 + \frac{t^{4}}{4}}dt$
4. $\frac{1}{2}\displaystyle \int_{0}^{2}t\sqrt{1 + t^{2}}dt$
5. $\frac{1}{2}\displaystyle \int_{0}^{2}t\sqrt{1 + \frac{t^{2}}{2}}dt$

Original correct designation: **missing**

**No source worked solution.**


## Raw original q-76189

Which of the following is equivalent to the integral ${\int }_{C}5y{e}^{-x}\text{d}s,$ where $C$ is the section of the curve $y={e}^{x}$ for $\,0\le x\le e?$

1. $5{\int }_{0}^{e}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
2. $5{\int }_{0}^{e}\sqrt{1+{e}^{2t}}\,\text{d}t$
3. ${\int }_{0}^{e}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
4. $5{\int }_{0}^{e}{e}^{t}\sqrt{t+{e}^{t}}\,\text{d}t$
5. ${\int }_{0}^{e}t{e}^{2t}\,\text{d}t$

Original correct designation: 5{\int }_{0}^{e}\sqrt{1+{e}^{2t}}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{e}^{t}⟩,\,0\le t\le e
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+({e}^{t})^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=5y{e}^{-x}$, we obtain

$$
\begin{aligned}f(r(t)) & =5{e}^{t}\cdot {e}^{-t}=5.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{e}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{e}5\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & =5{\int }_{0}^{e}\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## Raw original q-148206

Which of the following is equivalent to the integral ${\int }_{C}xy\,\text{d}s,$ where $C$ is the section of the curve $y={x}^{3}$ between the points $(0,0)$ and $(2,8)?$

1. $4{\int }_{0}^{2}{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t$
2. ${\int }_{0}^{2}{t}^{2}\sqrt{1+{t}^{4}}\,\text{d}t$
3. ${\int }_{0}^{2}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t$
4. ${\int }_{0}^{2}t\sqrt{9+{t}^{4}}\,\text{d}t$
5. $2{\int }_{0}^{2}{t}^{3}\sqrt{1+9{t}^{4}}\,\text{d}t$

Original correct designation: {\int }_{0}^{2}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={t}^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{t}^{3}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{1+9{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
\begin{aligned}f(r(t)) & =t\cdot {t}^{3}={t}^{4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t.\end{aligned}
$$


## Raw original q-148208

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{3}y\,\text{d}s,$ where $C$ is the section of the curve $y=\frac{1}{x}$ between the points $(1,1)$ and $(2,\frac{1}{2})?$

1. ${\int }_{1}^{2}t\sqrt{{t}^{2}+2}\,\text{d}t$
2. $2{\int }_{1}^{2}{t}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$
3. ${\int }_{1}^{2}{t}^{4}\sqrt{{t}^{2}+1}\,\text{d}t$
4. $2{\int }_{1}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$
5. $2{\int }_{1}^{2}t\sqrt{{t}^{2}+1}\,\text{d}t$

Original correct designation: 2{\int }_{1}^{2}\sqrt{{t}^{4}+1}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\frac{1}{t}⟩,\,1\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}} \\  & =\frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{3}y$, we obtain

$$
\begin{aligned}f(r(t)) & =2\cdot {t}^{3}\cdot \frac{1}{t}=2{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2}2{t}^{2}\cdot \frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{2}\sqrt{{t}^{4}+1}\,\text{d}t.\end{aligned}
$$


## Raw original q-76414

Which of the following is equivalent to the integral ${\int }_{C}y{e}^{x}\,\text{d}s,$ where $C$ is the section of the curve $y=5x+2$ for $\,0\le x\le 1?$

1. $\sqrt{26}{\int }_{0}^{1}(t+2){e}^{5t}\,\text{d}t$
2. $\sqrt{26}{\int }_{0}^{1}{e}^{t}\sqrt{5t+2}\,\text{d}t$
3. $\sqrt{26}{\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t$
4. ${\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t$
5. ${\int }_{0}^{1}(5t+2){e}^{t}\sqrt{26t}\,\text{d}t$

Original correct designation: \sqrt{26}{\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,5t+2⟩,\,0\le t\le 1
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(5t+2)j \\  & =i+5\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{5}^{2}} \\  & =\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=y{e}^{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =(5t+2){e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(5t+2){e}^{t}\cdot \sqrt{26}\cdot \text{d}t \\  & =\sqrt{26}{\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t.\end{aligned}
$$


## Raw original q-148199

Which of the following is equivalent to the integral ${\int }_{C}({x}^{3}-2y)\text{d}s,$ where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $\,0\le x\le 2?$

1. $\frac{1}{2}{\int }_{0}^{2}({t}^{3}-t-4)\,\text{d}t$
2. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}(t-4)\,\text{d}t$
3. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}(2{t}^{3}+t-8)\,\text{d}t$
4. $\frac{1}{2}{\int }_{0}^{2}({t}^{3}+2t-8)\,\text{d}t$
5. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}({t}^{3}+t-4)\,\text{d}t$

Original correct designation: \frac{\sqrt{5}}{2}{\int }_{0}^{2}({t}^{3}+t-4)\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2-\frac{t}{2}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2-\frac{t}{2})j \\  & =i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{2})}^{2}} \\  & =\sqrt{1+\frac{1}{4}} \\  & =\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}-2y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{3}-2(2-\frac{t}{2})={t}^{3}+t-4.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}({t}^{3}+t-4)\cdot \frac{\sqrt{5}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{5}}{2}{\int }_{0}^{2}({t}^{3}+t-4)\,\text{d}t.\end{aligned}
$$


## Raw original q-148205

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{cos}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{e}^{x}$ for $\,0\le x\le 2?$

1. ${\int }_{0}^{2}{e}^{t}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
2. $2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
3. $2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+{e}^{t}}\,\text{d}t$
4. ${\int }_{0}^{2}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
5. $4{\int }_{0}^{2}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$

Original correct designation: 2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{e}^{t}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{e}^{t})j \\  & =i+2{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2{e}^{t})^{2}} \\  & =\sqrt{1+4{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{e}^{t}\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}2{e}^{t}\operatorname{cos}⁡t\cdot \sqrt{1+4{e}^{2t}}\,\text{d}t \\  & =2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## Raw original q-76415

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{sin}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{x}^{2}$ between the points $(1,2)$ and $(3,18)?$

1. $2{\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
2. $2{\int }_{1}^{3}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
3. ${\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+4{t}^{2}}\,\text{d}t$
4. $2{\int }_{1}^{3}{t}^{2}\,\sqrt{1+16{t}^{2}}\,\text{d}t$
5. $8{\int }_{1}^{3}t\operatorname{sin}⁡{t}^{2}\,\sqrt{\frac{1}{16}+{t}^{2}}\,\text{d}t$

Original correct designation: 2{\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{t}^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{t}^{2}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{t}^{2})j \\  & =i+4t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(4t)^{2}} \\  & =\sqrt{1+16{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{sin}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\operatorname{sin}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{t}^{2}\operatorname{sin}⁡t\cdot \sqrt{1+16{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t.\end{aligned}
$$


## Raw original q-76416

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{2}{e}^{y}\,\text{d}s,$ where $C$ is the section of the curve $y=\operatorname{ln}⁡(x)$ for $\,1\le x\le 2e?$

1. $2{\int }_{1}^{2e}{t}^{2}\sqrt{1+\frac{1}{{t}^{3}}}\,\text{d}t$
2. $2{\int }_{1}^{2e}{t}^{2}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
3. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
4. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+{t}^{2}}\,\text{d}t$
5. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{t}}\,\text{d}t$

Original correct designation: 2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\operatorname{ln}⁡(t).$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\operatorname{ln}⁡(t)⟩,\,1\le t\le 2e
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t))j \\  & =i+\frac{1}{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{1}{t})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{2}{e}^{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\cdot {e}^{\operatorname{ln}⁡t}=2{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{2e}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2e}2{t}^{3}\cdot \sqrt{1+\frac{1}{{t}^{2}}}\cdot \text{d}t \\  & =2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-76188

Which of the following is equivalent to the integral $\displaystyle \int_{C}\frac{y}{x}ds$, where $C$ is the section of the curve $y = \frac{x^{2}}{2}$ between the points $(0, 0)$ and $(2, 2)$?

1. $\displaystyle \int_{0}^{2}t\sqrt{1 + \frac{t^{4}}{4}}dt$
2. $\displaystyle \int_{0}^{2}\sqrt{1 + t^{2}}dt$
3. $\frac{1}{2}\displaystyle \int_{0}^{2}tdt$
4. $\frac{1}{2}\displaystyle \int_{0}^{2}t\sqrt{1 + \frac{t^{2}}{2}}dt$
5. $\frac{1}{2}\displaystyle \int_{0}^{2}t\sqrt{1 + t^{2}}dt$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{t^{2}}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{t^{2}}{2}\rangle,\quad 0\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t^{2}}{2})j\\&=i+(t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(t)^2}\\&=\sqrt{t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
f(r(t))=\frac{(\frac{t^{2}}{2})}{t}=\frac{t}{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{2}(\frac{t}{2})\cdot (\sqrt{t^{2}+1})\,\mathrm{d}t\\&=\int_{0}^{2}\frac{t\sqrt{t^{2}+1}}{2}\,\mathrm{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76188 0

Which of the following is equivalent to the integral $\displaystyle \int_{C}\frac{y}{x}ds$, where $C$ is the section of the curve $y = \frac{x^{2}}{2}$ between the points $(1, \frac{1}{2})$ and $(3, \frac{9}{2})$?

1. $\displaystyle \int_{1}^{3}\sqrt{1 + t^{2}}dt$
2. $\frac{1}{2}\displaystyle \int_{1}^{3}t\sqrt{1 + \frac{t^{2}}{2}}dt$
3. $\frac{1}{2}\displaystyle \int_{1}^{3}t\sqrt{1 + t^{2}}dt$
4. $\displaystyle \int_{1}^{3}t\sqrt{1 + \frac{t^{4}}{4}}dt$
5. $\frac{1}{2}\displaystyle \int_{1}^{3}tdt$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{t^{2}}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{t^{2}}{2}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t^{2}}{2})j\\&=i+(t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(t)^2}\\&=\sqrt{t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
f(r(t))=\frac{(\frac{t^{2}}{2})}{t}=\frac{t}{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(\frac{t}{2})\cdot (\sqrt{t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}\frac{t\sqrt{t^{2}+1}}{2}\,\mathrm{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76188 1

Which of the following is equivalent to the integral $\displaystyle \int_{C}\frac{y}{x}ds$, where $C$ is the section of the curve $y = \frac{x^{2}}{2}$ between the points $(1, \frac{1}{2})$ and $(4, 8)$?

1. $\displaystyle \int_{1}^{4}t\sqrt{1 + \frac{t^{4}}{4}}dt$
2. $\displaystyle \int_{1}^{4}\sqrt{1 + t^{2}}dt$
3. $\frac{1}{2}\displaystyle \int_{1}^{4}t\sqrt{1 + \frac{t^{2}}{2}}dt$
4. $\frac{1}{2}\displaystyle \int_{1}^{4}tdt$
5. $\frac{1}{2}\displaystyle \int_{1}^{4}t\sqrt{1 + t^{2}}dt$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{t^{2}}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{t^{2}}{2}\rangle,\quad 1\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t^{2}}{2})j\\&=i+(t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(t)^2}\\&=\sqrt{t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
f(r(t))=\frac{(\frac{t^{2}}{2})}{t}=\frac{t}{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{4}(\frac{t}{2})\cdot (\sqrt{t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{4}\frac{t\sqrt{t^{2}+1}}{2}\,\mathrm{d}t.\end{aligned}
$$


## original-parameter evidence replay q-76189

Which of the following is equivalent to the integral ${\int }_{C}5y{e}^{-x}\text{d}s,$ where $C$ is the section of the curve $y={e}^{x}$ for $\,0\le x\le e?$

1. ${\int }_{0}^{e}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
2. $5{\int }_{0}^{e}\sqrt{1+{e}^{2t}}\,\text{d}t$
3. $5{\int }_{0}^{e}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
4. ${\int }_{0}^{e}t{e}^{2t}\,\text{d}t$
5. $5{\int }_{0}^{e}{e}^{t}\sqrt{t+{e}^{t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{e}^{t}⟩,\,0\le t\le e
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+({e}^{t})^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=5y{e}^{-x}$, we obtain

$$
\begin{aligned}f(r(t)) & =5{e}^{t}\cdot {e}^{-t}=5.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{e}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{e}5\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & =5{\int }_{0}^{e}\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76189 0

Which of the following is equivalent to the integral ${\int }_{C}5y{e}^{-x}\text{d}s,$ where $C$ is the section of the curve $y={e}^{x}$ for $\,1\le x\le 3?$

1. $5{\int }_{1}^{3}\sqrt{1+{e}^{2t}}\,\text{d}t$
2. ${\int }_{1}^{3}t{e}^{2t}\,\text{d}t$
3. $5{\int }_{1}^{3}{e}^{t}\sqrt{t+{e}^{t}}\,\text{d}t$
4. ${\int }_{1}^{3}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
5. $5{\int }_{1}^{3}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{e}^{t}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+({e}^{t})^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=5y{e}^{-x}$, we obtain

$$
\begin{aligned}f(r(t)) & =5{e}^{t}\cdot {e}^{-t}=5.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}5\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & =5{\int }_{1}^{3}\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76189 1

Which of the following is equivalent to the integral ${\int }_{C}5y{e}^{-x}\text{d}s,$ where $C$ is the section of the curve $y={e}^{x}$ for $\,1\le x\le 4?$

1. ${\int }_{1}^{4}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
2. $5{\int }_{1}^{4}\sqrt{1+{e}^{2t}}\,\text{d}t$
3. ${\int }_{1}^{4}t{e}^{2t}\,\text{d}t$
4. $5{\int }_{1}^{4}{e}^{t}\sqrt{1+{e}^{2t}}\,\text{d}t$
5. $5{\int }_{1}^{4}{e}^{t}\sqrt{t+{e}^{t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{e}^{t}⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+({e}^{t})^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=5y{e}^{-x}$, we obtain

$$
\begin{aligned}f(r(t)) & =5{e}^{t}\cdot {e}^{-t}=5.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}5\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & =5{\int }_{1}^{4}\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-148206

Which of the following is equivalent to the integral ${\int }_{C}xy\,\text{d}s,$ where $C$ is the section of the curve $y={x}^{3}$ between the points $(0,0)$ and $(2,8)?$

1. ${\int }_{0}^{2}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t$
2. ${\int }_{0}^{2}{t}^{2}\sqrt{1+{t}^{4}}\,\text{d}t$
3. $4{\int }_{0}^{2}{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t$
4. $2{\int }_{0}^{2}{t}^{3}\sqrt{1+9{t}^{4}}\,\text{d}t$
5. ${\int }_{0}^{2}t\sqrt{9+{t}^{4}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={t}^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{t}^{3}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{1+9{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
\begin{aligned}f(r(t)) & =t\cdot {t}^{3}={t}^{4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148206 0

Which of the following is equivalent to the integral ${\int }_{C}xy\,\text{d}s,$ where $C$ is the section of the curve $y={x}^{3}$ between the points $(1,1)$ and $(3,27)?$

1. ${\int }_{1}^{3}{t}^{2}\sqrt{1+{t}^{4}}\,\text{d}t$
2. $2{\int }_{1}^{3}{t}^{3}\sqrt{1+9{t}^{4}}\,\text{d}t$
3. ${\int }_{1}^{3}t\sqrt{9+{t}^{4}}\,\text{d}t$
4. ${\int }_{1}^{3}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t$
5. $4{\int }_{1}^{3}{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={t}^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{t}^{3}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{1+9{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
\begin{aligned}f(r(t)) & =t\cdot {t}^{3}={t}^{4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148206 1

Which of the following is equivalent to the integral ${\int }_{C}xy\,\text{d}s,$ where $C$ is the section of the curve $y={x}^{3}$ between the points $(1,1)$ and $(4,64)?$

1. ${\int }_{1}^{4}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t$
2. ${\int }_{1}^{4}{t}^{2}\sqrt{1+{t}^{4}}\,\text{d}t$
3. $2{\int }_{1}^{4}{t}^{3}\sqrt{1+9{t}^{4}}\,\text{d}t$
4. $4{\int }_{1}^{4}{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t$
5. ${\int }_{1}^{4}t\sqrt{9+{t}^{4}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={t}^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,{t}^{3}⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{1+9{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
\begin{aligned}f(r(t)) & =t\cdot {t}^{3}={t}^{4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}{t}^{4}\sqrt{1+9{t}^{4}}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-148208

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{3}y\,\text{d}s,$ where $C$ is the section of the curve $y=\frac{1}{x}$ between the points $(1,1)$ and $(2,\frac{1}{2})?$

1. ${\int }_{1}^{2}{t}^{4}\sqrt{{t}^{2}+1}\,\text{d}t$
2. $2{\int }_{1}^{2}{t}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$
3. ${\int }_{1}^{2}t\sqrt{{t}^{2}+2}\,\text{d}t$
4. $2{\int }_{1}^{2}t\sqrt{{t}^{2}+1}\,\text{d}t$
5. $2{\int }_{1}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\frac{1}{t}⟩,\,1\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}} \\  & =\frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{3}y$, we obtain

$$
\begin{aligned}f(r(t)) & =2\cdot {t}^{3}\cdot \frac{1}{t}=2{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2}2{t}^{2}\cdot \frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{2}\sqrt{{t}^{4}+1}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148208 0

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{3}y\,\text{d}s,$ where $C$ is the section of the curve $y=\frac{1}{x}$ between the points $(1,1)$ and $(3,\frac{1}{3})?$

1. $2{\int }_{1}^{3}{t}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$
2. $2{\int }_{1}^{3}t\sqrt{{t}^{2}+1}\,\text{d}t$
3. $2{\int }_{1}^{3}\sqrt{{t}^{4}+1}\,\text{d}t$
4. ${\int }_{1}^{3}{t}^{4}\sqrt{{t}^{2}+1}\,\text{d}t$
5. ${\int }_{1}^{3}t\sqrt{{t}^{2}+2}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\frac{1}{t}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}} \\  & =\frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{3}y$, we obtain

$$
\begin{aligned}f(r(t)) & =2\cdot {t}^{3}\cdot \frac{1}{t}=2{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{t}^{2}\cdot \frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{3}\sqrt{{t}^{4}+1}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148208 1

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{3}y\,\text{d}s,$ where $C$ is the section of the curve $y=\frac{1}{x}$ between the points $(1,1)$ and $(4,\frac{1}{4})?$

1. ${\int }_{1}^{4}{t}^{4}\sqrt{{t}^{2}+1}\,\text{d}t$
2. $2{\int }_{1}^{4}{t}^{2}\sqrt{{t}^{4}+1}\,\text{d}t$
3. $2{\int }_{1}^{4}t\sqrt{{t}^{2}+1}\,\text{d}t$
4. ${\int }_{1}^{4}t\sqrt{{t}^{2}+2}\,\text{d}t$
5. $2{\int }_{1}^{4}\sqrt{{t}^{4}+1}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\frac{1}{t}⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}} \\  & =\frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{3}y$, we obtain

$$
\begin{aligned}f(r(t)) & =2\cdot {t}^{3}\cdot \frac{1}{t}=2{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}2{t}^{2}\cdot \frac{\sqrt{{t}^{4}+1}}{{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{4}\sqrt{{t}^{4}+1}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-76414

Which of the following is equivalent to the integral ${\int }_{C}y{e}^{x}\,\text{d}s,$ where $C$ is the section of the curve $y=5x+2$ for $\,0\le x\le 1?$

1. $\sqrt{26}{\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t$
2. $\sqrt{26}{\int }_{0}^{1}{e}^{t}\sqrt{5t+2}\,\text{d}t$
3. $\sqrt{26}{\int }_{0}^{1}(t+2){e}^{5t}\,\text{d}t$
4. ${\int }_{0}^{1}(5t+2){e}^{t}\sqrt{26t}\,\text{d}t$
5. ${\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,5t+2⟩,\,0\le t\le 1
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(5t+2)j \\  & =i+5\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{5}^{2}} \\  & =\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=y{e}^{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =(5t+2){e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(5t+2){e}^{t}\cdot \sqrt{26}\cdot \text{d}t \\  & =\sqrt{26}{\int }_{0}^{1}(5t+2){e}^{t}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76414 0

Which of the following is equivalent to the integral ${\int }_{C}y{e}^{x}\,\text{d}s,$ where $C$ is the section of the curve $y=5x+2$ for $\,1\le x\le 3?$

1. $\sqrt{26}{\int }_{1}^{3}{e}^{t}\sqrt{5t+2}\,\text{d}t$
2. ${\int }_{1}^{3}(5t+2){e}^{t}\sqrt{26t}\,\text{d}t$
3. ${\int }_{1}^{3}(5t+2){e}^{t}\,\text{d}t$
4. $\sqrt{26}{\int }_{1}^{3}(5t+2){e}^{t}\,\text{d}t$
5. $\sqrt{26}{\int }_{1}^{3}(t+2){e}^{5t}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,5t+2⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(5t+2)j \\  & =i+5\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{5}^{2}} \\  & =\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=y{e}^{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =(5t+2){e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}(5t+2){e}^{t}\cdot \sqrt{26}\cdot \text{d}t \\  & =\sqrt{26}{\int }_{1}^{3}(5t+2){e}^{t}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76414 1

Which of the following is equivalent to the integral ${\int }_{C}y{e}^{x}\,\text{d}s,$ where $C$ is the section of the curve $y=5x+2$ for $\,1\le x\le 4?$

1. $\sqrt{26}{\int }_{1}^{4}(5t+2){e}^{t}\,\text{d}t$
2. $\sqrt{26}{\int }_{1}^{4}{e}^{t}\sqrt{5t+2}\,\text{d}t$
3. ${\int }_{1}^{4}(5t+2){e}^{t}\sqrt{26t}\,\text{d}t$
4. $\sqrt{26}{\int }_{1}^{4}(t+2){e}^{5t}\,\text{d}t$
5. ${\int }_{1}^{4}(5t+2){e}^{t}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,5t+2⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(5t+2)j \\  & =i+5\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{5}^{2}} \\  & =\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=y{e}^{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =(5t+2){e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}(5t+2){e}^{t}\cdot \sqrt{26}\cdot \text{d}t \\  & =\sqrt{26}{\int }_{1}^{4}(5t+2){e}^{t}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-148199

Which of the following is equivalent to the integral ${\int }_{C}({x}^{3}-2y)\text{d}s,$ where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $\,0\le x\le 2?$

1. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}(2{t}^{3}+t-8)\,\text{d}t$
2. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}(t-4)\,\text{d}t$
3. $\frac{1}{2}{\int }_{0}^{2}({t}^{3}-t-4)\,\text{d}t$
4. $\frac{\sqrt{5}}{2}{\int }_{0}^{2}({t}^{3}+t-4)\,\text{d}t$
5. $\frac{1}{2}{\int }_{0}^{2}({t}^{3}+2t-8)\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2-\frac{t}{2}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2-\frac{t}{2})j \\  & =i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{2})}^{2}} \\  & =\sqrt{1+\frac{1}{4}} \\  & =\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}-2y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{3}-2(2-\frac{t}{2})={t}^{3}+t-4.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}({t}^{3}+t-4)\cdot \frac{\sqrt{5}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{5}}{2}{\int }_{0}^{2}({t}^{3}+t-4)\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148199 0

Which of the following is equivalent to the integral ${\int }_{C}({x}^{3}-2y)\text{d}s,$ where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $\,1\le x\le 3?$

1. $\frac{\sqrt{5}}{2}{\int }_{1}^{3}(t-4)\,\text{d}t$
2. $\frac{\sqrt{5}}{2}{\int }_{1}^{3}({t}^{3}+t-4)\,\text{d}t$
3. $\frac{1}{2}{\int }_{1}^{3}({t}^{3}+2t-8)\,\text{d}t$
4. $\frac{\sqrt{5}}{2}{\int }_{1}^{3}(2{t}^{3}+t-8)\,\text{d}t$
5. $\frac{1}{2}{\int }_{1}^{3}({t}^{3}-t-4)\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2-\frac{t}{2}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2-\frac{t}{2})j \\  & =i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{2})}^{2}} \\  & =\sqrt{1+\frac{1}{4}} \\  & =\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}-2y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{3}-2(2-\frac{t}{2})={t}^{3}+t-4.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}({t}^{3}+t-4)\cdot \frac{\sqrt{5}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{5}}{2}{\int }_{1}^{3}({t}^{3}+t-4)\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148199 1

Which of the following is equivalent to the integral ${\int }_{C}({x}^{3}-2y)\text{d}s,$ where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $\,1\le x\le 4?$

1. $\frac{\sqrt{5}}{2}{\int }_{1}^{4}(2{t}^{3}+t-8)\,\text{d}t$
2. $\frac{\sqrt{5}}{2}{\int }_{1}^{4}(t-4)\,\text{d}t$
3. $\frac{\sqrt{5}}{2}{\int }_{1}^{4}({t}^{3}+t-4)\,\text{d}t$
4. $\frac{1}{2}{\int }_{1}^{4}({t}^{3}-t-4)\,\text{d}t$
5. $\frac{1}{2}{\int }_{1}^{4}({t}^{3}+2t-8)\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2-\frac{t}{2}⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2-\frac{t}{2})j \\  & =i-\frac{1}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{2})}^{2}} \\  & =\sqrt{1+\frac{1}{4}} \\  & =\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}-2y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{3}-2(2-\frac{t}{2})={t}^{3}+t-4.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}({t}^{3}+t-4)\cdot \frac{\sqrt{5}}{2}\cdot \text{d}t \\  & =\frac{\sqrt{5}}{2}{\int }_{1}^{4}({t}^{3}+t-4)\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-148205

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{cos}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{e}^{x}$ for $\,0\le x\le 2?$

1. $2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+{e}^{t}}\,\text{d}t$
2. $2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
3. ${\int }_{0}^{2}{e}^{t}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
4. $4{\int }_{0}^{2}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
5. ${\int }_{0}^{2}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{e}^{t}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{e}^{t})j \\  & =i+2{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2{e}^{t})^{2}} \\  & =\sqrt{1+4{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{e}^{t}\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}2{e}^{t}\operatorname{cos}⁡t\cdot \sqrt{1+4{e}^{2t}}\,\text{d}t \\  & =2{\int }_{0}^{2}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148205 0

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{cos}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{e}^{x}$ for $\,1\le x\le 3?$

1. $2{\int }_{1}^{3}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
2. $4{\int }_{1}^{3}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
3. ${\int }_{1}^{3}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
4. $2{\int }_{1}^{3}{e}^{t}\operatorname{cos}⁡t\sqrt{1+{e}^{t}}\,\text{d}t$
5. ${\int }_{1}^{3}{e}^{t}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{e}^{t}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{e}^{t})j \\  & =i+2{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2{e}^{t})^{2}} \\  & =\sqrt{1+4{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{e}^{t}\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{e}^{t}\operatorname{cos}⁡t\cdot \sqrt{1+4{e}^{2t}}\,\text{d}t \\  & =2{\int }_{1}^{3}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-148205 1

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{cos}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{e}^{x}$ for $\,1\le x\le 4?$

1. $2{\int }_{1}^{4}{e}^{t}\operatorname{cos}⁡t\sqrt{1+{e}^{t}}\,\text{d}t$
2. $2{\int }_{1}^{4}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
3. $4{\int }_{1}^{4}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
4. ${\int }_{1}^{4}{e}^{t}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$
5. ${\int }_{1}^{4}\operatorname{sin}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{e}^{t}⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{e}^{t})j \\  & =i+2{e}^{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2{e}^{t})^{2}} \\  & =\sqrt{1+4{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{e}^{t}\operatorname{cos}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}2{e}^{t}\operatorname{cos}⁡t\cdot \sqrt{1+4{e}^{2t}}\,\text{d}t \\  & =2{\int }_{1}^{4}{e}^{t}\operatorname{cos}⁡t\sqrt{1+4{e}^{2t}}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-76415

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{sin}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{x}^{2}$ between the points $(1,2)$ and $(3,18)?$

1. ${\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+4{t}^{2}}\,\text{d}t$
2. $2{\int }_{1}^{3}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
3. $2{\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
4. $8{\int }_{1}^{3}t\operatorname{sin}⁡{t}^{2}\,\sqrt{\frac{1}{16}+{t}^{2}}\,\text{d}t$
5. $2{\int }_{1}^{3}{t}^{2}\,\sqrt{1+16{t}^{2}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{t}^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{t}^{2}⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{t}^{2})j \\  & =i+4t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(4t)^{2}} \\  & =\sqrt{1+16{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{sin}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\operatorname{sin}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{t}^{2}\operatorname{sin}⁡t\cdot \sqrt{1+16{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{1}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76415 0

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{sin}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{x}^{2}$ between the points $(0,0)$ and $(2,8)?$

1. $2{\int }_{0}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
2. $8{\int }_{0}^{2}t\operatorname{sin}⁡{t}^{2}\,\sqrt{\frac{1}{16}+{t}^{2}}\,\text{d}t$
3. $2{\int }_{0}^{2}{t}^{2}\,\sqrt{1+16{t}^{2}}\,\text{d}t$
4. ${\int }_{0}^{2}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+4{t}^{2}}\,\text{d}t$
5. $2{\int }_{0}^{2}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{t}^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{t}^{2}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{t}^{2})j \\  & =i+4t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(4t)^{2}} \\  & =\sqrt{1+16{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{sin}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\operatorname{sin}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}2{t}^{2}\operatorname{sin}⁡t\cdot \sqrt{1+16{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{0}^{2}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76415 1

Which of the following is equivalent to the integral ${\int }_{C}y\operatorname{sin}⁡x\,\text{d}s,$ where $C$ is the section of the curve $y=2{x}^{2}$ between the points $(0,0)$ and $(3,18)?$

1. ${\int }_{0}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+4{t}^{2}}\,\text{d}t$
2. $2{\int }_{0}^{3}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
3. $8{\int }_{0}^{3}t\operatorname{sin}⁡{t}^{2}\,\sqrt{\frac{1}{16}+{t}^{2}}\,\text{d}t$
4. $2{\int }_{0}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t$
5. $2{\int }_{0}^{3}{t}^{2}\,\sqrt{1+16{t}^{2}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2{t}^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,2{t}^{2}⟩,\,0\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(2{t}^{2})j \\  & =i+4t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(4t)^{2}} \\  & =\sqrt{1+16{t}^{2}}\end{aligned}
$$

Now, since $f(x,y)=y\operatorname{sin}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\operatorname{sin}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{3}2{t}^{2}\operatorname{sin}⁡t\cdot \sqrt{1+16{t}^{2}}\cdot \text{d}t \\  & =2{\int }_{0}^{3}{t}^{2}\operatorname{sin}⁡t\,\sqrt{1+16{t}^{2}}\,\text{d}t.\end{aligned}
$$


## original-parameter evidence replay q-76416

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{2}{e}^{y}\,\text{d}s,$ where $C$ is the section of the curve $y=\operatorname{ln}⁡(x)$ for $\,1\le x\le 2e?$

1. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
2. $2{\int }_{1}^{2e}{t}^{2}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
3. $2{\int }_{1}^{2e}{t}^{2}\sqrt{1+\frac{1}{{t}^{3}}}\,\text{d}t$
4. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{t}}\,\text{d}t$
5. $2{\int }_{1}^{2e}{t}^{3}\sqrt{1+{t}^{2}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\operatorname{ln}⁡(t).$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\operatorname{ln}⁡(t)⟩,\,1\le t\le 2e
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t))j \\  & =i+\frac{1}{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{1}{t})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{2}{e}^{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\cdot {e}^{\operatorname{ln}⁡t}=2{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{2e}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2e}2{t}^{3}\cdot \sqrt{1+\frac{1}{{t}^{2}}}\cdot \text{d}t \\  & =2{\int }_{1}^{2e}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76416 0

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{2}{e}^{y}\,\text{d}s,$ where $C$ is the section of the curve $y=\operatorname{ln}⁡(x)$ for $\,1\le x\le 3?$

1. $2{\int }_{1}^{3}{t}^{2}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
2. $2{\int }_{1}^{3}{t}^{3}\sqrt{1+\frac{1}{t}}\,\text{d}t$
3. $2{\int }_{1}^{3}{t}^{3}\sqrt{1+{t}^{2}}\,\text{d}t$
4. $2{\int }_{1}^{3}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
5. $2{\int }_{1}^{3}{t}^{2}\sqrt{1+\frac{1}{{t}^{3}}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\operatorname{ln}⁡(t).$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\operatorname{ln}⁡(t)⟩,\,1\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t))j \\  & =i+\frac{1}{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{1}{t})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{2}{e}^{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\cdot {e}^{\operatorname{ln}⁡t}=2{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{t}^{3}\cdot \sqrt{1+\frac{1}{{t}^{2}}}\cdot \text{d}t \\  & =2{\int }_{1}^{3}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t.\end{aligned}
$$


## generated observed-pattern variant q-76416 1

Which of the following is equivalent to the integral ${\int }_{C}2{x}^{2}{e}^{y}\,\text{d}s,$ where $C$ is the section of the curve $y=\operatorname{ln}⁡(x)$ for $\,1\le x\le 4?$

1. $2{\int }_{1}^{4}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
2. $2{\int }_{1}^{4}{t}^{2}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t$
3. $2{\int }_{1}^{4}{t}^{3}\sqrt{1+\frac{1}{t}}\,\text{d}t$
4. $2{\int }_{1}^{4}{t}^{2}\sqrt{1+\frac{1}{{t}^{3}}}\,\text{d}t$
5. $2{\int }_{1}^{4}{t}^{3}\sqrt{1+{t}^{2}}\,\text{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\operatorname{ln}⁡(t).$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\operatorname{ln}⁡(t)⟩,\,1\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t))j \\  & =i+\frac{1}{t}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{1}{t})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2{x}^{2}{e}^{y}$, we obtain

$$
\begin{aligned}f(r(t)) & =2{t}^{2}\cdot {e}^{\operatorname{ln}⁡t}=2{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}2{t}^{3}\cdot \sqrt{1+\frac{1}{{t}^{2}}}\cdot \text{d}t \\  & =2{\int }_{1}^{4}{t}^{3}\sqrt{1+\frac{1}{{t}^{2}}}\,\text{d}t.\end{aligned}
$$


## generated normal authored bank easy quadratic_ratio 0

Which of the following is equivalent to the integral $\int_C \frac{2y}{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=\frac{x^{2}}{2}$ for $1\le x\le 3$?

1. $\int_{1}^{3}t\sqrt{t^{2}+1}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{t^{2}+1}\,\mathrm{d}t$
3. $\int_{1}^{3}t\,\mathrm{d}t$
4. $\int_{1}^{3}t\left|{t}\right|\,\mathrm{d}t$
5. $\int_{1}^{3}t\left(t^{2}+1\right)\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{t^{2}}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{t^{2}}{2}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t^{2}}{2})j\\&=i+(t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(t)^2}\\&=\sqrt{t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{2y}{x}$, we obtain

$$
f(r(t))=\frac{2(\frac{t^{2}}{2})}{t}=t.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(t)\cdot (\sqrt{t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}t\sqrt{t^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy quadratic_ratio 1

Which of the following is equivalent to the integral $\int_C \frac{2y}{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=\frac{x^{2}}{2}$ for $0\le x\le 4$?

1. $\int_{0}^{4}t\left(t^{2}+1\right)\,\mathrm{d}t$
2. $\int_{0}^{4}\sqrt{t^{2}+1}\,\mathrm{d}t$
3. $\int_{0}^{4}t\,\mathrm{d}t$
4. $\int_{0}^{4}t\left|{t}\right|\,\mathrm{d}t$
5. $\int_{0}^{4}t\sqrt{t^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{t^{2}}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{t^{2}}{2}\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{t^{2}}{2})j\\&=i+(t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(t)^2}\\&=\sqrt{t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{2y}{x}$, we obtain

$$
f(r(t))=\frac{2(\frac{t^{2}}{2})}{t}=t.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(t)\cdot (\sqrt{t^{2}+1})\,\mathrm{d}t\\&=\int_{0}^{4}t\sqrt{t^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy exponential_cancel 0

Which of the following is equivalent to the integral $\int_C 10ye^{-x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=e^{x}$ for $1\le x\le 3$?

1. $\int_{1}^{3}10\sqrt{e^{2t}+1}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{e^{2t}+1}\,\mathrm{d}t$
3. $\int_{1}^{3}10\,\mathrm{d}t$
4. $\int_{1}^{3}10e^{t}\,\mathrm{d}t$
5. $\int_{1}^{3}10e^{2t}+10\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=e^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,e^{t}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})j\\&=i+(e^{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(e^{t})^2}\\&=\sqrt{e^{2t}+1}\end{aligned}
$$

Now, since $f(x,y)=10ye^{-x}$, we obtain

$$
f(r(t))=10(e^{t})e^{-t}=10.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(10)\cdot (\sqrt{e^{2t}+1})\,\mathrm{d}t\\&=\int_{1}^{3}10\sqrt{e^{2t}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy exponential_cancel 1

Which of the following is equivalent to the integral $\int_C 10ye^{-x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=e^{x}$ for $0\le x\le 4$?

1. $\int_{0}^{4}10e^{2t}+10\,\mathrm{d}t$
2. $\int_{0}^{4}\sqrt{e^{2t}+1}\,\mathrm{d}t$
3. $\int_{0}^{4}10\,\mathrm{d}t$
4. $\int_{0}^{4}10e^{t}\,\mathrm{d}t$
5. $\int_{0}^{4}10\sqrt{e^{2t}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=e^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,e^{t}\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})j\\&=i+(e^{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(e^{t})^2}\\&=\sqrt{e^{2t}+1}\end{aligned}
$$

Now, since $f(x,y)=10ye^{-x}$, we obtain

$$
f(r(t))=10(e^{t})e^{-t}=10.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(10)\cdot (\sqrt{e^{2t}+1})\,\mathrm{d}t\\&=\int_{0}^{4}10\sqrt{e^{2t}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy cubic_product 0

Which of the following is equivalent to the integral $\int_C 2xy\,\mathrm{d}s$, where $C$ is the section of the curve $y=x^{3}$ for $1\le x\le 3$?

1. $\int_{1}^{3}2t^{4}\sqrt{9t^{4}+1}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{9t^{4}+1}\,\mathrm{d}t$
3. $\int_{1}^{3}2t^{4}\,\mathrm{d}t$
4. $\int_{1}^{3}6t^{6}\,\mathrm{d}t$
5. $\int_{1}^{3}2t^{4}\left(9t^{4}+1\right)\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,t^{3}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})j\\&=i+(3t^{2})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(3t^{2})^2}\\&=\sqrt{9t^{4}+1}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
f(r(t))=2t(t^{3})=2t^{4}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(2t^{4})\cdot (\sqrt{9t^{4}+1})\,\mathrm{d}t\\&=\int_{1}^{3}2t^{4}\sqrt{9t^{4}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy cubic_product 1

Which of the following is equivalent to the integral $\int_C 2xy\,\mathrm{d}s$, where $C$ is the section of the curve $y=x^{3}$ for $0\le x\le 4$?

1. $\int_{0}^{4}2t^{4}\left(9t^{4}+1\right)\,\mathrm{d}t$
2. $\int_{0}^{4}\sqrt{9t^{4}+1}\,\mathrm{d}t$
3. $\int_{0}^{4}2t^{4}\,\mathrm{d}t$
4. $\int_{0}^{4}6t^{6}\,\mathrm{d}t$
5. $\int_{0}^{4}2t^{4}\sqrt{9t^{4}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t^{3}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,t^{3}\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})j\\&=i+(3t^{2})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(3t^{2})^2}\\&=\sqrt{9t^{4}+1}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
f(r(t))=2t(t^{3})=2t^{4}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(2t^{4})\cdot (\sqrt{9t^{4}+1})\,\mathrm{d}t\\&=\int_{0}^{4}2t^{4}\sqrt{9t^{4}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy reciprocal_product 0

Which of the following is equivalent to the integral $\int_C 4x^{3}y\,\mathrm{d}s$, where $C$ is the section of the curve $y=\frac{1}{x}$ for $2\le x\le 4$?

1. $\int_{2}^{4}4t^{2}\sqrt{1+\frac{1}{t^{4}}}\,\mathrm{d}t$
2. $\int_{2}^{4}\sqrt{1+\frac{1}{t^{4}}}\,\mathrm{d}t$
3. $\int_{2}^{4}4t^{2}\,\mathrm{d}t$
4. $\int_{2}^{4}4\,\mathrm{d}t$
5. $\int_{2}^{4}4t^{2}\left(1+\frac{1}{t^{4}}\right)\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{1}{t}\rangle,\quad 2\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{1}{t})j\\&=i+(-\frac{1}{t^{2}})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(-\frac{1}{t^{2}})^2}\\&=\sqrt{1+\frac{1}{t^{4}}}\end{aligned}
$$

Now, since $f(x,y)=4x^{3}y$, we obtain

$$
f(r(t))=4t^{3}(\frac{1}{t})=4t^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{2}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{2}^{4}(4t^{2})\cdot (\sqrt{1+\frac{1}{t^{4}}})\,\mathrm{d}t\\&=\int_{2}^{4}4\sqrt{t^{4}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy reciprocal_product 1

Which of the following is equivalent to the integral $\int_C 4x^{3}y\,\mathrm{d}s$, where $C$ is the section of the curve $y=\frac{1}{x}$ for $1\le x\le 5$?

1. $\int_{1}^{5}4t^{2}\left(1+\frac{1}{t^{4}}\right)\,\mathrm{d}t$
2. $\int_{1}^{5}\sqrt{1+\frac{1}{t^{4}}}\,\mathrm{d}t$
3. $\int_{1}^{5}4t^{2}\,\mathrm{d}t$
4. $\int_{1}^{5}4\,\mathrm{d}t$
5. $\int_{1}^{5}4t^{2}\sqrt{1+\frac{1}{t^{4}}}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\frac{1}{t}\rangle,\quad 1\le t\le 5
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\frac{1}{t})j\\&=i+(-\frac{1}{t^{2}})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(-\frac{1}{t^{2}})^2}\\&=\sqrt{1+\frac{1}{t^{4}}}\end{aligned}
$$

Now, since $f(x,y)=4x^{3}y$, we obtain

$$
f(r(t))=4t^{3}(\frac{1}{t})=4t^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{5}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{5}(4t^{2})\cdot (\sqrt{1+\frac{1}{t^{4}}})\,\mathrm{d}t\\&=\int_{1}^{5}4\sqrt{t^{4}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy linear_exponential 0

Which of the following is equivalent to the integral $\int_C 2ye^{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=5x+2$ for $1\le x\le 3$?

1. $\int_{1}^{3}\sqrt{26}\left(10t+4\right)e^{t}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{26}\,\mathrm{d}t$
3. $\int_{1}^{3}\left(10t+4\right)e^{t}\,\mathrm{d}t$
4. $\int_{1}^{3}5\left(10t+4\right)e^{t}\,\mathrm{d}t$
5. $\int_{1}^{3}26\left(10t+4\right)e^{t}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,5t+2\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(5t+2)j\\&=i+(5)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(5)^2}\\&=\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=2ye^{x}$, we obtain

$$
f(r(t))=2(5t+2)e^{t}=\left(10t+4\right)e^{t}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(\left(10t+4\right)e^{t})\cdot (\sqrt{26})\,\mathrm{d}t\\&=\int_{1}^{3}\sqrt{26}\left(10t+4\right)e^{t}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy linear_exponential 1

Which of the following is equivalent to the integral $\int_C 2ye^{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=5x+2$ for $0\le x\le 4$?

1. $\int_{0}^{4}26\left(10t+4\right)e^{t}\,\mathrm{d}t$
2. $\int_{0}^{4}\sqrt{26}\,\mathrm{d}t$
3. $\int_{0}^{4}\left(10t+4\right)e^{t}\,\mathrm{d}t$
4. $\int_{0}^{4}5\left(10t+4\right)e^{t}\,\mathrm{d}t$
5. $\int_{0}^{4}\sqrt{26}\left(10t+4\right)e^{t}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=5t+2.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,5t+2\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(5t+2)j\\&=i+(5)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(5)^2}\\&=\sqrt{26}\end{aligned}
$$

Now, since $f(x,y)=2ye^{x}$, we obtain

$$
f(r(t))=2(5t+2)e^{t}=\left(10t+4\right)e^{t}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(\left(10t+4\right)e^{t})\cdot (\sqrt{26})\,\mathrm{d}t\\&=\int_{0}^{4}\sqrt{26}\left(10t+4\right)e^{t}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy linear_difference 0

Which of the following is equivalent to the integral $\int_C 2x^{3}-4y\,\mathrm{d}s$, where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $1\le x\le 3$?

1. $\int_{1}^{3}\frac{\sqrt{5}\left(2t^{3}+2t-8\right)}{2}\,\mathrm{d}t$
2. $\int_{1}^{3}\frac{\sqrt{5}}{2}\,\mathrm{d}t$
3. $\int_{1}^{3}2t^{3}+2t-8\,\mathrm{d}t$
4. $\int_{1}^{3}t^{3}+t-4\,\mathrm{d}t$
5. $\int_{1}^{3}\frac{5t^{3}}{2}+\frac{5t}{2}-10\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2-\frac{t}{2}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2-\frac{t}{2})j\\&=i+(-\frac{1}{2})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(-\frac{1}{2})^2}\\&=\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)=2x^{3}-4y$, we obtain

$$
f(r(t))=2t^{3}-4(2-\frac{t}{2})=2t^{3}+2t-8.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(2t^{3}+2t-8)\cdot (\frac{\sqrt{5}}{2})\,\mathrm{d}t\\&=\int_{1}^{3}\sqrt{5}\left(t^{3}+t-4\right)\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy linear_difference 1

Which of the following is equivalent to the integral $\int_C 2x^{3}-4y\,\mathrm{d}s$, where $C$ is the section of the curve $y=2-\frac{x}{2}$ for $0\le x\le 4$?

1. $\int_{0}^{4}\frac{5t^{3}}{2}+\frac{5t}{2}-10\,\mathrm{d}t$
2. $\int_{0}^{4}\frac{\sqrt{5}}{2}\,\mathrm{d}t$
3. $\int_{0}^{4}2t^{3}+2t-8\,\mathrm{d}t$
4. $\int_{0}^{4}t^{3}+t-4\,\mathrm{d}t$
5. $\int_{0}^{4}\frac{\sqrt{5}\left(2t^{3}+2t-8\right)}{2}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2-\frac{t}{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2-\frac{t}{2}\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2-\frac{t}{2})j\\&=i+(-\frac{1}{2})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(-\frac{1}{2})^2}\\&=\frac{\sqrt{5}}{2}\end{aligned}
$$

Now, since $f(x,y)=2x^{3}-4y$, we obtain

$$
f(r(t))=2t^{3}-4(2-\frac{t}{2})=2t^{3}+2t-8.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(2t^{3}+2t-8)\cdot (\frac{\sqrt{5}}{2})\,\mathrm{d}t\\&=\int_{0}^{4}\sqrt{5}\left(t^{3}+t-4\right)\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy exponential_cosine 0

Which of the following is equivalent to the integral $\int_C 2y\cos{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2e^{x}$ for $1\le x\le 3$?

1. $\int_{1}^{3}4\sqrt{4e^{2t}+1}e^{t}\cos{\left(t\right)}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{4e^{2t}+1}\,\mathrm{d}t$
3. $\int_{1}^{3}4e^{t}\cos{\left(t\right)}\,\mathrm{d}t$
4. $\int_{1}^{3}8e^{2t}\cos{\left(t\right)}\,\mathrm{d}t$
5. $\int_{1}^{3}4\left(4e^{2t}+1\right)e^{t}\cos{\left(t\right)}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2e^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2e^{t}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2e^{t})j\\&=i+(2e^{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(2e^{t})^2}\\&=\sqrt{4e^{2t}+1}\end{aligned}
$$

Now, since $f(x,y)=2y\cos{\left(x\right)}$, we obtain

$$
f(r(t))=2(2e^{t})\cos{\left(t\right)}=4e^{t}\cos{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(4e^{t}\cos{\left(t\right)})\cdot (\sqrt{4e^{2t}+1})\,\mathrm{d}t\\&=\int_{1}^{3}4\sqrt{4e^{2t}+1}e^{t}\cos{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy exponential_cosine 1

Which of the following is equivalent to the integral $\int_C 2y\cos{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2e^{x}$ for $0\le x\le 4$?

1. $\int_{0}^{4}4\left(4e^{2t}+1\right)e^{t}\cos{\left(t\right)}\,\mathrm{d}t$
2. $\int_{0}^{4}\sqrt{4e^{2t}+1}\,\mathrm{d}t$
3. $\int_{0}^{4}4e^{t}\cos{\left(t\right)}\,\mathrm{d}t$
4. $\int_{0}^{4}8e^{2t}\cos{\left(t\right)}\,\mathrm{d}t$
5. $\int_{0}^{4}4\sqrt{4e^{2t}+1}e^{t}\cos{\left(t\right)}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2e^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2e^{t}\rangle,\quad 0\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2e^{t})j\\&=i+(2e^{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(2e^{t})^2}\\&=\sqrt{4e^{2t}+1}\end{aligned}
$$

Now, since $f(x,y)=2y\cos{\left(x\right)}$, we obtain

$$
f(r(t))=2(2e^{t})\cos{\left(t\right)}=4e^{t}\cos{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{4}(4e^{t}\cos{\left(t\right)})\cdot (\sqrt{4e^{2t}+1})\,\mathrm{d}t\\&=\int_{0}^{4}4\sqrt{4e^{2t}+1}e^{t}\cos{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy quadratic_sine 0

Which of the following is equivalent to the integral $\int_C 2y\sin{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2x^{2}$ for $1\le x\le 3$?

1. $\int_{1}^{3}4t^{2}\sqrt{16t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t$
2. $\int_{1}^{3}\sqrt{16t^{2}+1}\,\mathrm{d}t$
3. $\int_{1}^{3}4t^{2}\sin{\left(t\right)}\,\mathrm{d}t$
4. $\int_{1}^{3}16t^{2}\sin{\left(t\right)}\left|{t}\right|\,\mathrm{d}t$
5. $\int_{1}^{3}4t^{2}\left(16t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2t^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2t^{2}\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2t^{2})j\\&=i+(4t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(4t)^2}\\&=\sqrt{16t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=2y\sin{\left(x\right)}$, we obtain

$$
f(r(t))=2(2t^{2})\sin{\left(t\right)}=4t^{2}\sin{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(4t^{2}\sin{\left(t\right)})\cdot (\sqrt{16t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}4t^{2}\sqrt{16t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy quadratic_sine 1

Which of the following is equivalent to the integral $\int_C y\sin{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=4x^{2}$ for $0\le x\le 2$?

1. $\int_{0}^{2}4t^{2}\sqrt{64t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t$
2. $\int_{0}^{2}\sqrt{64t^{2}+1}\,\mathrm{d}t$
3. $\int_{0}^{2}4t^{2}\sin{\left(t\right)}\,\mathrm{d}t$
4. $\int_{0}^{2}4t^{2}\left(64t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$
5. $\int_{0}^{2}32t^{2}\sin{\left(t\right)}\left|{t}\right|\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=4t^{2}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,4t^{2}\rangle,\quad 0\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(4t^{2})j\\&=i+(8t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(8t)^2}\\&=\sqrt{64t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=y\sin{\left(x\right)}$, we obtain

$$
f(r(t))=(4t^{2})\sin{\left(t\right)}=4t^{2}\sin{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{0}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{0}^{2}(4t^{2}\sin{\left(t\right)})\cdot (\sqrt{64t^{2}+1})\,\mathrm{d}t\\&=\int_{0}^{2}4t^{2}\sqrt{64t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy log_exponential 0

Which of the following is equivalent to the integral $\int_C 4x^{2}e^{y}\,\mathrm{d}s$, where $C$ is the section of the curve $y=\ln{\left(x\right)}$ for $2\le x\le 4$?

1. $\int_{2}^{4}4t^{3}\sqrt{1+\frac{1}{t^{2}}}\,\mathrm{d}t$
2. $\int_{2}^{4}\sqrt{1+\frac{1}{t^{2}}}\,\mathrm{d}t$
3. $\int_{2}^{4}4t^{3}\,\mathrm{d}t$
4. $\int_{2}^{4}\frac{4t^{3}}{\left|{t}\right|}\,\mathrm{d}t$
5. $\int_{2}^{4}4t^{3}\left(1+\frac{1}{t^{2}}\right)\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\ln{\left(t\right)}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\ln{\left(t\right)}\rangle,\quad 2\le t\le 4
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\ln{\left(t\right)})j\\&=i+(\frac{1}{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(\frac{1}{t})^2}\\&=\sqrt{1+\frac{1}{t^{2}}}\end{aligned}
$$

Now, since $f(x,y)=4x^{2}e^{y}$, we obtain

$$
f(r(t))=4t^{2}e^{(\ln{\left(t\right)})}=4t^{3}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{2}^{4}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{2}^{4}(4t^{3})\cdot (\sqrt{1+\frac{1}{t^{2}}})\,\mathrm{d}t\\&=\int_{2}^{4}\frac{4t^{3}\sqrt{t^{2}+1}}{\left|{t}\right|}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank easy log_exponential 1

Which of the following is equivalent to the integral $\int_C 4x^{2}e^{y}\,\mathrm{d}s$, where $C$ is the section of the curve $y=\ln{\left(x\right)}$ for $1\le x\le 5$?

1. $\int_{1}^{5}4t^{3}\left(1+\frac{1}{t^{2}}\right)\,\mathrm{d}t$
2. $\int_{1}^{5}\sqrt{1+\frac{1}{t^{2}}}\,\mathrm{d}t$
3. $\int_{1}^{5}4t^{3}\,\mathrm{d}t$
4. $\int_{1}^{5}\frac{4t^{3}}{\left|{t}\right|}\,\mathrm{d}t$
5. $\int_{1}^{5}4t^{3}\sqrt{1+\frac{1}{t^{2}}}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\ln{\left(t\right)}.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,\ln{\left(t\right)}\rangle,\quad 1\le t\le 5
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(\ln{\left(t\right)})j\\&=i+(\frac{1}{t})j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(\frac{1}{t})^2}\\&=\sqrt{1+\frac{1}{t^{2}}}\end{aligned}
$$

Now, since $f(x,y)=4x^{2}e^{y}$, we obtain

$$
f(r(t))=4t^{2}e^{(\ln{\left(t\right)})}=4t^{3}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{5}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{5}(4t^{3})\cdot (\sqrt{1+\frac{1}{t^{2}}})\,\mathrm{d}t\\&=\int_{1}^{5}\frac{4t^{3}\sqrt{t^{2}+1}}{\left|{t}\right|}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank moderate shifted_quadratic 0

Which of the following is equivalent to the integral $\int_C xy\,\mathrm{d}s$, where $C$ is the section of the curve $y=2x^{2}+1$ for $1\le x\le 3$?

1. $\int_{1}^{3}\sqrt{16t^{2}+1}\left(2t^{3}+t\right)\,\mathrm{d}t$
2. $\int_{1}^{3}\left(16t^{2}+1\right)\left(2t^{3}+t\right)\,\mathrm{d}t$
3. $\int_{1}^{3}2t^{3}+t\,\mathrm{d}t$
4. $\int_{1}^{3}4\left(2t^{3}+t\right)\left|{t}\right|\,\mathrm{d}t$
5. $\int_{1}^{3}\sqrt{16t^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2t^{2}+1.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2t^{2}+1\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2t^{2}+1)j\\&=i+(4t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(4t)^2}\\&=\sqrt{16t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
f(r(t))=t(2t^{2}+1)=2t^{3}+t.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(2t^{3}+t)\cdot (\sqrt{16t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}t\left(2t^{2}+1\right)\sqrt{16t^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank moderate shifted_quadratic 1

Which of the following is equivalent to the integral $\int_C xy\,\mathrm{d}s$, where $C$ is the section of the curve $y=3x^{2}+1$ for $1\le x\le 2$?

1. $\int_{1}^{2}6\left(3t^{3}+t\right)\left|{t}\right|\,\mathrm{d}t$
2. $\int_{1}^{2}\left(36t^{2}+1\right)\left(3t^{3}+t\right)\,\mathrm{d}t$
3. $\int_{1}^{2}3t^{3}+t\,\mathrm{d}t$
4. $\int_{1}^{2}\sqrt{36t^{2}+1}\left(3t^{3}+t\right)\,\mathrm{d}t$
5. $\int_{1}^{2}\sqrt{36t^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t^{2}+1.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,3t^{2}+1\rangle,\quad 1\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(3t^{2}+1)j\\&=i+(6t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(6t)^2}\\&=\sqrt{36t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=xy$, we obtain

$$
f(r(t))=t(3t^{2}+1)=3t^{3}+t.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{2}(3t^{3}+t)\cdot (\sqrt{36t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{2}t\left(3t^{2}+1\right)\sqrt{36t^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank moderate shifted_quadratic_sine 0

Which of the following is equivalent to the integral $\int_C y\sin{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2x^{2}+1$ for $1\le x\le 3$?

1. $\int_{1}^{3}\left(2t^{2}+1\right)\sqrt{16t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t$
2. $\int_{1}^{3}\left(2t^{2}+1\right)\left(16t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$
3. $\int_{1}^{3}\left(2t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$
4. $\int_{1}^{3}4\left(2t^{2}+1\right)\sin{\left(t\right)}\left|{t}\right|\,\mathrm{d}t$
5. $\int_{1}^{3}\sqrt{16t^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2t^{2}+1.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2t^{2}+1\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2t^{2}+1)j\\&=i+(4t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(4t)^2}\\&=\sqrt{16t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=y\sin{\left(x\right)}$, we obtain

$$
f(r(t))=(2t^{2}+1)\sin{\left(t\right)}=\left(2t^{2}+1\right)\sin{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(\left(2t^{2}+1\right)\sin{\left(t\right)})\cdot (\sqrt{16t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}\left(2t^{2}+1\right)\sqrt{16t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank moderate shifted_quadratic_sine 1

Which of the following is equivalent to the integral $\int_C y\sin{\left(x\right)}\,\mathrm{d}s$, where $C$ is the section of the curve $y=3x^{2}+1$ for $1\le x\le 2$?

1. $\int_{1}^{2}6\left(3t^{2}+1\right)\sin{\left(t\right)}\left|{t}\right|\,\mathrm{d}t$
2. $\int_{1}^{2}\left(3t^{2}+1\right)\left(36t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$
3. $\int_{1}^{2}\left(3t^{2}+1\right)\sin{\left(t\right)}\,\mathrm{d}t$
4. $\int_{1}^{2}\left(3t^{2}+1\right)\sqrt{36t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t$
5. $\int_{1}^{2}\sqrt{36t^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t^{2}+1.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,3t^{2}+1\rangle,\quad 1\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(3t^{2}+1)j\\&=i+(6t)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(6t)^2}\\&=\sqrt{36t^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=y\sin{\left(x\right)}$, we obtain

$$
f(r(t))=(3t^{2}+1)\sin{\left(t\right)}=\left(3t^{2}+1\right)\sin{\left(t\right)}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{2}(\left(3t^{2}+1\right)\sin{\left(t\right)})\cdot (\sqrt{36t^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{2}\left(3t^{2}+1\right)\sqrt{36t^{2}+1}\sin{\left(t\right)}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank hard cubic_squared_quotient 0

Which of the following is equivalent to the integral $\int_C \frac{y^{2}}{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2x^{3}+x$ for $1\le x\le 3$?

1. $\int_{1}^{3}t\left(2t^{2}+1\right)^{2}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t$
2. $\int_{1}^{3}t\left(2t^{2}+1\right)^{2}\left(\left(6t^{2}+1\right)^{2}+1\right)\,\mathrm{d}t$
3. $\int_{1}^{3}t\left(2t^{2}+1\right)^{2}\,\mathrm{d}t$
4. $\int_{1}^{3}t\left(2t^{2}+1\right)^{2}\left(6t^{2}+1\right)\,\mathrm{d}t$
5. $\int_{1}^{3}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2t^{3}+t.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2t^{3}+t\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2t^{3}+t)j\\&=i+(6t^{2}+1)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(6t^{2}+1)^2}\\&=\sqrt{\left(6t^{2}+1\right)^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{y^{2}}{x}$, we obtain

$$
f(r(t))=\frac{(2t^{3}+t)^{2}}{t}=t\left(2t^{2}+1\right)^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(t\left(2t^{2}+1\right)^{2})\cdot (\sqrt{\left(6t^{2}+1\right)^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}t\left(2t^{2}+1\right)^{2}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank hard cubic_squared_quotient 1

Which of the following is equivalent to the integral $\int_C \frac{y^{2}}{x}\,\mathrm{d}s$, where $C$ is the section of the curve $y=3x^{3}+x$ for $1\le x\le 2$?

1. $\int_{1}^{2}t\left(3t^{2}+1\right)^{2}\left(9t^{2}+1\right)\,\mathrm{d}t$
2. $\int_{1}^{2}t\left(3t^{2}+1\right)^{2}\left(\left(9t^{2}+1\right)^{2}+1\right)\,\mathrm{d}t$
3. $\int_{1}^{2}t\left(3t^{2}+1\right)^{2}\,\mathrm{d}t$
4. $\int_{1}^{2}t\left(3t^{2}+1\right)^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t$
5. $\int_{1}^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t^{3}+t.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,3t^{3}+t\rangle,\quad 1\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(3t^{3}+t)j\\&=i+(9t^{2}+1)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(9t^{2}+1)^2}\\&=\sqrt{\left(9t^{2}+1\right)^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{y^{2}}{x}$, we obtain

$$
f(r(t))=\frac{(3t^{3}+t)^{2}}{t}=t\left(3t^{2}+1\right)^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{2}(t\left(3t^{2}+1\right)^{2})\cdot (\sqrt{\left(9t^{2}+1\right)^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{2}t\left(3t^{2}+1\right)^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank hard cubic_squared_product 0

Which of the following is equivalent to the integral $\int_C xy^{2}\,\mathrm{d}s$, where $C$ is the section of the curve $y=2x^{3}+x$ for $1\le x\le 3$?

1. $\int_{1}^{3}t^{3}\left(2t^{2}+1\right)^{2}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t$
2. $\int_{1}^{3}t^{3}\left(2t^{2}+1\right)^{2}\left(\left(6t^{2}+1\right)^{2}+1\right)\,\mathrm{d}t$
3. $\int_{1}^{3}t^{3}\left(2t^{2}+1\right)^{2}\,\mathrm{d}t$
4. $\int_{1}^{3}t^{3}\left(2t^{2}+1\right)^{2}\left(6t^{2}+1\right)\,\mathrm{d}t$
5. $\int_{1}^{3}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2t^{3}+t.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,2t^{3}+t\rangle,\quad 1\le t\le 3
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2t^{3}+t)j\\&=i+(6t^{2}+1)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(6t^{2}+1)^2}\\&=\sqrt{\left(6t^{2}+1\right)^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=xy^{2}$, we obtain

$$
f(r(t))=t(2t^{3}+t)^{2}=t^{3}\left(2t^{2}+1\right)^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{3}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{3}(t^{3}\left(2t^{2}+1\right)^{2})\cdot (\sqrt{\left(6t^{2}+1\right)^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{3}t^{3}\left(2t^{2}+1\right)^{2}\sqrt{\left(6t^{2}+1\right)^{2}+1}\,\mathrm{d}t.\end{aligned}
$$


## generated normal authored bank hard cubic_squared_product 1

Which of the following is equivalent to the integral $\int_C xy^{2}\,\mathrm{d}s$, where $C$ is the section of the curve $y=3x^{3}+x$ for $1\le x\le 2$?

1. $\int_{1}^{2}t^{3}\left(3t^{2}+1\right)^{2}\left(9t^{2}+1\right)\,\mathrm{d}t$
2. $\int_{1}^{2}t^{3}\left(3t^{2}+1\right)^{2}\left(\left(9t^{2}+1\right)^{2}+1\right)\,\mathrm{d}t$
3. $\int_{1}^{2}t^{3}\left(3t^{2}+1\right)^{2}\,\mathrm{d}t$
4. $\int_{1}^{2}t^{3}\left(3t^{2}+1\right)^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t$
5. $\int_{1}^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t^{3}+t.$ This gives the following parametrization of the curve:

$$
r(t)=\langle t,3t^{3}+t\rangle,\quad 1\le t\le 2
$$

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}i+\frac{\mathrm{d}y}{\mathrm{d}t}j\\&=\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(3t^{3}+t)j\\&=i+(9t^{2}+1)j\\\|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2}\\&=\sqrt{1^2+(9t^{2}+1)^2}\\&=\sqrt{\left(9t^{2}+1\right)^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=xy^{2}$, we obtain

$$
f(r(t))=t(3t^{3}+t)^{2}=t^{3}\left(3t^{2}+1\right)^{2}.
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{1}^{2}f(r(t))\,\|r'(t)\|\,\mathrm{d}t\\&=\int_{1}^{2}(t^{3}\left(3t^{2}+1\right)^{2})\cdot (\sqrt{\left(9t^{2}+1\right)^{2}+1})\,\mathrm{d}t\\&=\int_{1}^{2}t^{3}\left(3t^{2}+1\right)^{2}\sqrt{\left(9t^{2}+1\right)^{2}+1}\,\mathrm{d}t.\end{aligned}
$$
