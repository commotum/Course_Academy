# Scalar line-integral setup review

Raw source banks are evidence only. Generated records are explicitly labeled; no integral evaluation is requested.

## Raw original q-167608

Which of the following is equivalent to the integral ${\int }_{C}\frac{x}{4y+1}\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $0\le t\le 1?$

1. ${\int }_{0}^{1}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t$
2. ${\int }_{0}^{1}\frac{{t}^{2}}{\sqrt{2t+1}}\text{d}t$
3. ${\int }_{0}^{1}t(2t+1)\text{d}t$
4. ${\int }_{0}^{1}t\sqrt{4{t}^{2}+1}\text{d}t$
5. ${\int }_{0}^{1}(4{t}^{2}+1)\text{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{x}{4y+1}$, then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{t}{4{t}^{2}+1}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{x}{4y+1}\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t \\  & ={\int }_{0}^{1}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t.\end{aligned}
$$

---

## Raw original q-40253

Which of the following is equivalent to ${\int }_{C}f(x,y)\,\text{d}s,$ where $f(x,y)=\sqrt{2}(x-y)$ and the curve $C$ is parametrized 
 by $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩$ for $t\in [0,\sqrt{2}]?$

1. $\sqrt{2}{\int }_{0}^{\sqrt{2}}t\sqrt{2{t}^{2}-1}\,\text{d}t.$
2. ${\int }_{0}^{\sqrt{2}}t\sqrt{2{t}^{2}+1}\,\text{d}t.$
3. $4{\int }_{0}^{\sqrt{2}}t\sqrt{8{t}^{2}+1}\,\text{d}t.$
4. $2{\int }_{0}^{\sqrt{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.$
5. $4{\int }_{0}^{\sqrt{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.$

Since $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩,$ then along the curve we have $x={t}^{2}+t,$ and $y={t}^{2}-t.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+t)i+\frac{\text{d}}{\text{d}t}({t}^{2}-t)j \\  & =(2t+1)\,i+(2t-1)\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t+1)^{2}+(2t-1)^{2}} \\  & =\sqrt{4{t}^{2}+4t+1+4{t}^{2}-4t+1} \\  & =\sqrt{8{t}^{2}+2} \\  & =\sqrt{2}\sqrt{4{t}^{2}+1}\end{aligned}
$$

 

Now, since $f(x,y)=\sqrt{2}(x-y)$, we obtain 

$$
\begin{aligned}f(r(t)) & =\sqrt{2}[({t}^{2}+t)-({t}^{2}-t)] \\  & =2\sqrt{2}t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\sqrt{2}}2\sqrt{2}t\cdot \sqrt{2}\sqrt{4{t}^{2}+1}\cdot \text{d}t \\  & =4{\int }_{0}^{\sqrt{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

---

## Raw original q-76377

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=2x-{y}^{2}-{z}^{2}$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩$ for $t\in [0,3]?$

1. $-2{\int }_{0}^{3}t\sqrt{{t}^{2}+1}\,\text{d}t$
2. $-2\sqrt{2}{\int }_{0}^{3}\sqrt{2{t}^{2}+1}\,\text{d}t$
3. $\sqrt{2}{\int }_{0}^{3}({t}^{2}-2t)\sqrt{2{t}^{2}+1}\,\text{d}t$
4. ${\int }_{0}^{3}({t}^{2}+2t)\sqrt{2{t}^{2}+1}\,\text{d}t$
5. $-2{\int }_{0}^{3}({t}^{2}+2t-1)\sqrt{{t}^{2}+1}\,\text{d}t$

Since $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩,$ then along the curve we have $x={t}^{2},$ $y=t-1,$ and $z=t+1.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j+\frac{\text{d}}{\text{d}t}(t+1)k \\  & =2t\,i+j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+2}\end{aligned}
$$

  

Now, since $f(x,y,z)=2x-{y}^{2}-{z}^{2}$, we obtain 

$$
\begin{aligned}f(r(t)) & =2({t}^{2})-(t-1)^{2}-(t+1)^{2} \\  & =2{t}^{2}-({t}^{2}-2t+1)-({t}^{2}+2t+1) \\  & =2{t}^{2}-{t}^{2}+2t-1-{t}^{2}-2t-1 \\  & =-2.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{3}(-2)\cdot \sqrt{4{t}^{2}+2}\cdot \text{d}t \\  & ={\int }_{0}^{3}(-2)\cdot \sqrt{2(2{t}^{2}+1)}\cdot \text{d}t \\  & ={\int }_{0}^{3}(-2)\cdot \sqrt{2}\cdot \sqrt{2{t}^{2}+1}\,\text{d}t \\  & =-2\sqrt{2}{\int }_{0}^{3}\sqrt{2{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

---

## Raw original q-76356

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=x+y-z$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩$ for $t\in [0,2]?$

1. $\sqrt{2}{\int }_{0}^{2}({t}^{2}-t)\sqrt{t+1}\,\text{d}t$
2. $2\sqrt{3}{\int }_{0}^{2}{t}^{3}\,\text{d}t$
3. $2{\int }_{0}^{2}{t}^{2}\sqrt{{t}^{2}-t}\,\text{d}t$
4. $\sqrt{3}{\int }_{0}^{2}{t}^{2}\sqrt{{t}^{2}+1}\,\text{d}t$
5. $2{\int }_{0}^{2}{t}^{2}\sqrt{t+1}\,\text{d}t$

Since $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩,$ then along the curve we have $x={t}^{2}+1,$ $y={t}^{2}-1,$ and $z={t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+1)i+\frac{\text{d}}{\text{d}t}({t}^{2}-1)j+\frac{\text{d}}{\text{d}t}({t}^{2})k \\  & =2t\,i+2t\,j+2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(2t)^{2}+(2t)^{2}} \\  & =\sqrt{4{t}^{2}+4{t}^{2}+4{t}^{2}} \\  & =\sqrt{12{t}^{2}} \\  & =2\sqrt{3}|t| \\  & =2\sqrt{3}t\end{aligned}
$$

Notice that $|t|=t$ since $t>0$ along the path of $C.$

Now, since $f(x,y,z)=x+y-z$, we obtain 

$$
\begin{aligned}f(r(t)) & =({t}^{2}+1)+({t}^{2}-1)-{t}^{2} \\  & =2{t}^{2}-{t}^{2} \\  & ={t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}{t}^{2}\cdot 2\sqrt{3}t\cdot \text{d}t \\  & =2\sqrt{3}{\int }_{0}^{2}{t}^{3}\,\text{d}t.\end{aligned}
$$

---

## Raw original q-76379

Which of the following is equivalent to the integral ${\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,0\le t\le \frac{\pi }{2}?$

1. $2\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{sin}⁡t\sqrt{2{cos}^{2}⁡t+3}\,\text{d}t$
2. $\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{cos}⁡2t\,\text{d}t$
3. $2{\int }_{0}^{\pi /2}t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,\text{d}t$
4. $2{\int }_{0}^{\pi /2}t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)^{2}\,\text{d}t$
5. $\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{cos}⁡t\sqrt{2{cos}^{2}⁡t+1}\,\text{d}t$

Since $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k,$ then along the curve we have $x=\operatorname{cos}⁡t,$ $y=\operatorname{sin}⁡t,$ and $z=t.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j+\frac{\text{d}}{\text{d}t}(t)k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+{1}^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

  

Now, if $f(x,y,z)=z({x}^{2}-{y}^{2})$, then we obtain

$$
\begin{aligned}f(r(t)) & =t((\operatorname{cos}⁡t)^{2}-(\operatorname{sin}⁡t)^{2}) \\  & =t({cos}^{2}⁡t-{sin}^{2}⁡t) \\  & =t\operatorname{cos}⁡2t.\end{aligned}
$$

Therefore, we can write the integral as  

$$
\begin{aligned}{\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s & ={\int }_{0}^{\pi /2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi /2}t\operatorname{cos}⁡2t\cdot \sqrt{2}\cdot \text{d}t \\  & =\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{cos}⁡2t\,\text{d}t.\end{aligned}
$$

---

## Raw original q-76368

Which of the following is equivalent to the integral $\displaystyle \int_(C)(x^{3} - y)ds$, where the curve $C$ is parametrized by $r(t) = 2ti + (2 - t)j$ for $-1 \le t \le 2$?

1. $2\displaystyle \int_{-1}^{2}(t^{3} - t^{2} + 4t)dt$
2. $\sqrt{2}\displaystyle \int_{-1}^{2}(4t^{3} - 3)dt$
3. $3\displaystyle \int_{-1}^{2}(8t^{3} - t^{2} + 4t - 4)dt$
4. $\displaystyle \int_{-1}^{2}(8t^{3} + t^{2} - 4)dt$
5. $\sqrt{5}\displaystyle \int_{-1}^{2}(8t^{3} + t - 2)dt$.

[Raw source has no worked solution.]

---

## Generated parabola seed 0

Which of the following is equivalent to the integral ${\int }_{C}\frac{x}{4y+1}\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $\frac{5}{2}\le t\le \frac{11}{2}?$

1. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
2. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{t}{4 t^{2} + 1}\,\mathrm{d}t$
3. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$
4. $\int_{\frac{5}{2}}^{\frac{11}{2}}t\,\mathrm{d}t$
5. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{x}{4y+1}$, then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{t}{4{t}^{2}+1}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{x}{4y+1}\text{d}s & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t.\end{aligned}
$$

---

## Generated parabola seed 1

Which of the following is equivalent to the integral ${\int }_{C}-5\left(\frac{x}{4y+1}\right)\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $1\le t\le 4?$

1. $\int_{1}^{4}- \frac{5 t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$
2. $\int_{1}^{4}- \frac{5 t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
3. $\int_{1}^{4}- \frac{5 t}{4 t^{2} + 1}\,\mathrm{d}t$
4. $\int_{1}^{4}- \frac{5 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
5. $\int_{1}^{4}- 5 t\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=-5\left(\frac{x}{4y+1}\right)$, then we obtain 

$$
\begin{aligned}f(r(t)) & =-5\left(\frac{t}{4{t}^{2}+1}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}-5\left(\frac{x}{4y+1}\right)\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =-5\left({\int }_{1}^{4}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t\right) \\    & =-5\left({\int }_{1}^{4}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t\right).\end{aligned}
$$

---

## Generated difference seed 0

Which of the following is equivalent to ${\int }_{C}f(x,y)\,\text{d}s,$ where $f(x,y)=\sqrt{2}(x-y)$ and the curve $C$ is parametrized 
 by $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩$ for $t\in [\frac{5}{2},\frac{11}{2}]?$

1. $\int_{\frac{5}{2}}^{\frac{11}{2}}4 t^{2} \sqrt{4 t^{2} + 1}\,\mathrm{d}t$
2. $\int_{\frac{5}{2}}^{\frac{11}{2}}2 \sqrt{2} t\,\mathrm{d}t$
3. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{2 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
4. $\int_{\frac{5}{2}}^{\frac{11}{2}}4 \sqrt{2} t \left(4 t^{2} + 1\right)\,\mathrm{d}t$
5. $\int_{\frac{5}{2}}^{\frac{11}{2}}4 t \sqrt{4 t^{2} + 1}\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩,$ then along the curve we have $x={t}^{2}+t,$ and $y={t}^{2}-t.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+t)i+\frac{\text{d}}{\text{d}t}({t}^{2}-t)j \\  & =(2t+1)\,i+(2t-1)\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t+1)^{2}+(2t-1)^{2}} \\  & =\sqrt{4{t}^{2}+4t+1+4{t}^{2}-4t+1} \\  & =\sqrt{8{t}^{2}+2} \\  & =\sqrt{2}\sqrt{4{t}^{2}+1}\end{aligned}
$$

 

Now, since $f(x,y)=\sqrt{2}(x-y)$, we obtain 

$$
\begin{aligned}f(r(t)) & =\sqrt{2}[({t}^{2}+t)-({t}^{2}-t)] \\  & =2\sqrt{2}t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}2\sqrt{2}t\cdot \sqrt{2}\sqrt{4{t}^{2}+1}\cdot \text{d}t \\  & =4{\int }_{\frac{5}{2}}^{\frac{11}{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

---

## Generated difference seed 1

Which of the following is equivalent to ${\int }_{C}f(x,y)\,\text{d}s,$ where $f(x,y)=-5\left(\sqrt{2}(x-y)\right)$ and the curve $C$ is parametrized 
 by $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩$ for $t\in [1,4]?$

1. $\int_{1}^{4}- \frac{10 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
2. $\int_{1}^{4}- 20 t^{2} \sqrt{4 t^{2} + 1}\,\mathrm{d}t$
3. $\int_{1}^{4}- 10 \sqrt{2} t\,\mathrm{d}t$
4. $\int_{1}^{4}- 20 t \sqrt{4 t^{2} + 1}\,\mathrm{d}t$
5. $\int_{1}^{4}- 20 \sqrt{2} t \left(4 t^{2} + 1\right)\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩,$ then along the curve we have $x={t}^{2}+t,$ and $y={t}^{2}-t.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+t)i+\frac{\text{d}}{\text{d}t}({t}^{2}-t)j \\  & =(2t+1)\,i+(2t-1)\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t+1)^{2}+(2t-1)^{2}} \\  & =\sqrt{4{t}^{2}+4t+1+4{t}^{2}-4t+1} \\  & =\sqrt{8{t}^{2}+2} \\  & =\sqrt{2}\sqrt{4{t}^{2}+1}\end{aligned}
$$

 

Now, since $f(x,y)=-5\left(\sqrt{2}(x-y)\right)$, we obtain 

$$
\begin{aligned}f(r(t)) & =-5\left(\sqrt{2}[({t}^{2}+t)-({t}^{2}-t)]\right) \\    & =-5\left(2\sqrt{2}t\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =-5\left({\int }_{1}^{4}2\sqrt{2}t\cdot \sqrt{2}\sqrt{4{t}^{2}+1}\cdot \text{d}t\right) \\    & =-5\left(4{\int }_{1}^{4}t\sqrt{4{t}^{2}+1}\,\text{d}t\right).\end{aligned}
$$

---

## Generated squares seed 0

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=2x-{y}^{2}-{z}^{2}$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩$ for $t\in [\frac{5}{2},\frac{11}{2}]?$

1. $\int_{\frac{5}{2}}^{\frac{11}{2}}2 \sqrt{2} \left(2 t^{2} + 1\right)^{\frac{3}{2}}\,\mathrm{d}t$
2. $\int_{\frac{5}{2}}^{\frac{11}{2}}-2\,\mathrm{d}t$
3. $\int_{\frac{5}{2}}^{\frac{11}{2}}- \frac{\sqrt{2}}{\sqrt{2 t^{2} + 1}}\,\mathrm{d}t$
4. $\int_{\frac{5}{2}}^{\frac{11}{2}}- 8 t^{2} - 4\,\mathrm{d}t$
5. $\int_{\frac{5}{2}}^{\frac{11}{2}}- 2 \sqrt{4 t^{2} + 2}\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩,$ then along the curve we have $x={t}^{2},$ $y=t-1,$ and $z=t+1.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j+\frac{\text{d}}{\text{d}t}(t+1)k \\  & =2t\,i+j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+2}\end{aligned}
$$

  

Now, since $f(x,y,z)=2x-{y}^{2}-{z}^{2}$, we obtain 

$$
\begin{aligned}f(r(t)) & =2({t}^{2})-(t-1)^{2}-(t+1)^{2} \\  & =2{t}^{2}-({t}^{2}-2t+1)-({t}^{2}+2t+1) \\  & =2{t}^{2}-{t}^{2}+2t-1-{t}^{2}-2t-1 \\  & =-2.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}(-2)\cdot \sqrt{4{t}^{2}+2}\cdot \text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}(-2)\cdot \sqrt{2(2{t}^{2}+1)}\cdot \text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}(-2)\cdot \sqrt{2}\cdot \sqrt{2{t}^{2}+1}\,\text{d}t \\  & =-2\sqrt{2}{\int }_{\frac{5}{2}}^{\frac{11}{2}}\sqrt{2{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

---

## Generated squares seed 1

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=-5\left(2x-{y}^{2}-{z}^{2}\right)$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩$ for $t\in [1,4]?$

1. $\int_{1}^{4}\frac{5 \sqrt{2}}{\sqrt{2 t^{2} + 1}}\,\mathrm{d}t$
2. $\int_{1}^{4}- 10 \sqrt{2} \left(2 t^{2} + 1\right)^{\frac{3}{2}}\,\mathrm{d}t$
3. $\int_{1}^{4}10\,\mathrm{d}t$
4. $\int_{1}^{4}10 \sqrt{4 t^{2} + 2}\,\mathrm{d}t$
5. $\int_{1}^{4}40 t^{2} + 20\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩,$ then along the curve we have $x={t}^{2},$ $y=t-1,$ and $z=t+1.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j+\frac{\text{d}}{\text{d}t}(t+1)k \\  & =2t\,i+j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+2}\end{aligned}
$$

  

Now, since $f(x,y,z)=-5\left(2x-{y}^{2}-{z}^{2}\right)$, we obtain 

$$
\begin{aligned}f(r(t)) & =-5\left(2({t}^{2})-(t-1)^{2}-(t+1)^{2}\right) \\    & =-5\left(2{t}^{2}-({t}^{2}-2t+1)-({t}^{2}+2t+1)\right) \\    & =-5\left(2{t}^{2}-{t}^{2}+2t-1-{t}^{2}-2t-1\right) \\    & =-5\left(-2\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =-5\left({\int }_{1}^{4}(-2)\cdot \sqrt{4{t}^{2}+2}\cdot \text{d}t\right) \\    & =-5\left({\int }_{1}^{4}(-2)\cdot \sqrt{2(2{t}^{2}+1)}\cdot \text{d}t\right) \\    & =-5\left({\int }_{1}^{4}(-2)\cdot \sqrt{2}\cdot \sqrt{2{t}^{2}+1}\,\text{d}t\right) \\    & =-5\left(-2\sqrt{2}{\int }_{1}^{4}\sqrt{2{t}^{2}+1}\,\text{d}t\right).\end{aligned}
$$

---

## Generated quadratic3 seed 0

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=x+y-z$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩$ for $t\in [\frac{5}{2},\frac{11}{2}]?$

1. $\int_{\frac{5}{2}}^{\frac{11}{2}}6 \sqrt{3} t^{3}\,\mathrm{d}t$
2. $\int_{\frac{5}{2}}^{\frac{11}{2}}t^{2}\,\mathrm{d}t$
3. $\int_{\frac{5}{2}}^{\frac{11}{2}}\frac{\sqrt{3} t}{6}\,\mathrm{d}t$
4. $\int_{\frac{5}{2}}^{\frac{11}{2}}12 t^{4}\,\mathrm{d}t$
5. $\int_{\frac{5}{2}}^{\frac{11}{2}}2 \sqrt{3} t^{3}\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩,$ then along the curve we have $x={t}^{2}+1,$ $y={t}^{2}-1,$ and $z={t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+1)i+\frac{\text{d}}{\text{d}t}({t}^{2}-1)j+\frac{\text{d}}{\text{d}t}({t}^{2})k \\  & =2t\,i+2t\,j+2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(2t)^{2}+(2t)^{2}} \\  & =\sqrt{4{t}^{2}+4{t}^{2}+4{t}^{2}} \\  & =\sqrt{12{t}^{2}} \\  & =2\sqrt{3}|t| \\  & =2\sqrt{3}t\end{aligned}
$$

Notice that $|t|=t$ since $t\ge 0$ along the path of $C.$

Now, since $f(x,y,z)=x+y-z$, we obtain 

$$
\begin{aligned}f(r(t)) & =({t}^{2}+1)+({t}^{2}-1)-{t}^{2} \\  & =2{t}^{2}-{t}^{2} \\  & ={t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{5}{2}}^{\frac{11}{2}}{t}^{2}\cdot 2\sqrt{3}t\cdot \text{d}t \\  & =2\sqrt{3}{\int }_{\frac{5}{2}}^{\frac{11}{2}}{t}^{3}\,\text{d}t.\end{aligned}
$$

---

## Generated quadratic3 seed 1

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=-5\left(x+y-z\right)$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩$ for $t\in [1,4]?$

1. $\int_{1}^{4}- \frac{5 \sqrt{3} t}{6}\,\mathrm{d}t$
2. $\int_{1}^{4}- 30 \sqrt{3} t^{3}\,\mathrm{d}t$
3. $\int_{1}^{4}- 5 t^{2}\,\mathrm{d}t$
4. $\int_{1}^{4}- 10 \sqrt{3} t^{3}\,\mathrm{d}t$
5. $\int_{1}^{4}- 60 t^{4}\,\mathrm{d}t$

Since $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩,$ then along the curve we have $x={t}^{2}+1,$ $y={t}^{2}-1,$ and $z={t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2}+1)i+\frac{\text{d}}{\text{d}t}({t}^{2}-1)j+\frac{\text{d}}{\text{d}t}({t}^{2})k \\  & =2t\,i+2t\,j+2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(2t)^{2}+(2t)^{2}} \\  & =\sqrt{4{t}^{2}+4{t}^{2}+4{t}^{2}} \\  & =\sqrt{12{t}^{2}} \\  & =2\sqrt{3}|t| \\  & =2\sqrt{3}t\end{aligned}
$$

Notice that $|t|=t$ since $t\ge 0$ along the path of $C.$

Now, since $f(x,y,z)=-5\left(x+y-z\right)$, we obtain 

$$
\begin{aligned}f(r(t)) & =-5\left(({t}^{2}+1)+({t}^{2}-1)-{t}^{2}\right) \\    & =-5\left(2{t}^{2}-{t}^{2}\right) \\    & =-5\left({t}^{2}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y,z)\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =-5\left({\int }_{1}^{4}{t}^{2}\cdot 2\sqrt{3}t\cdot \text{d}t\right) \\    & =-5\left(2\sqrt{3}{\int }_{1}^{4}{t}^{3}\,\text{d}t\right).\end{aligned}
$$

---

## Generated helix seed 0

Which of the following is equivalent to the integral ${\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,\frac{\pi}{4}\le t\le \frac{\pi}{2}?$

1. $\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}\sqrt{2} t\,\mathrm{d}t$
2. $\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}t \cos{\left(2 t \right)}\,\mathrm{d}t$
3. $\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}\frac{\sqrt{2} t \cos{\left(2 t \right)}}{2}\,\mathrm{d}t$
4. $\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}2 t \cos{\left(2 t \right)}\,\mathrm{d}t$
5. $\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}\sqrt{2} t \cos{\left(2 t \right)}\,\mathrm{d}t$

Since $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k,$ then along the curve we have $x=\operatorname{cos}⁡t,$ $y=\operatorname{sin}⁡t,$ and $z=t.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j+\frac{\text{d}}{\text{d}t}(t)k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+{1}^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

  

Now, if $f(x,y,z)=z({x}^{2}-{y}^{2})$, then we obtain

$$
\begin{aligned}f(r(t)) & =t((\operatorname{cos}⁡t)^{2}-(\operatorname{sin}⁡t)^{2}) \\  & =t({cos}^{2}⁡t-{sin}^{2}⁡t) \\  & =t\operatorname{cos}⁡2t.\end{aligned}
$$

Therefore, we can write the integral as  

$$
\begin{aligned}{\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s & ={\int }_{\frac{\pi}{4}}^{\frac{\pi}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{\pi}{4}}^{\frac{\pi}{2}}t\operatorname{cos}⁡2t\cdot \sqrt{2}\cdot \text{d}t \\  & =\sqrt{2}{\int }_{\frac{\pi}{4}}^{\frac{\pi}{2}}t\operatorname{cos}⁡2t\,\text{d}t.\end{aligned}
$$

---

## Generated helix seed 1

Which of the following is equivalent to the integral ${\int }_{C}-5\left(z({x}^{2}-{y}^{2})\right)\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,\frac{\pi}{12}\le t\le \frac{\pi}{3}?$

1. $\int_{\frac{\pi}{12}}^{\frac{\pi}{3}}- \frac{5 \sqrt{2} t \cos{\left(2 t \right)}}{2}\,\mathrm{d}t$
2. $\int_{\frac{\pi}{12}}^{\frac{\pi}{3}}- 5 \sqrt{2} t\,\mathrm{d}t$
3. $\int_{\frac{\pi}{12}}^{\frac{\pi}{3}}- 5 t \cos{\left(2 t \right)}\,\mathrm{d}t$
4. $\int_{\frac{\pi}{12}}^{\frac{\pi}{3}}- 5 \sqrt{2} t \cos{\left(2 t \right)}\,\mathrm{d}t$
5. $\int_{\frac{\pi}{12}}^{\frac{\pi}{3}}- 10 t \cos{\left(2 t \right)}\,\mathrm{d}t$

Since $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k,$ then along the curve we have $x=\operatorname{cos}⁡t,$ $y=\operatorname{sin}⁡t,$ and $z=t.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j+\frac{\text{d}}{\text{d}t}(t)k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+{1}^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

  

Now, if $f(x,y,z)=-5\left(z({x}^{2}-{y}^{2})\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =-5\left(t((\operatorname{cos}⁡t)^{2}-(\operatorname{sin}⁡t)^{2})\right) \\    & =-5\left(t({cos}^{2}⁡t-{sin}^{2}⁡t)\right) \\    & =-5\left(t\operatorname{cos}⁡2t\right).\end{aligned}
$$

Therefore, we can write the integral as  

$$
\begin{aligned}{\int }_{C}-5\left(z({x}^{2}-{y}^{2})\right)\,\text{d}s & ={\int }_{\frac{\pi}{12}}^{\frac{\pi}{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =-5\left({\int }_{\frac{\pi}{12}}^{\frac{\pi}{3}}t\operatorname{cos}⁡2t\cdot \sqrt{2}\cdot \text{d}t\right) \\    & =-5\left(\sqrt{2}{\int }_{\frac{\pi}{12}}^{\frac{\pi}{3}}t\operatorname{cos}⁡2t\,\text{d}t\right).\end{aligned}
$$

---

## Generated linear_cubic seed 0

Which of the following is equivalent to the integral $\displaystyle \int_C-6\left((x^{3} - y)\right)ds$, where the curve $C$ is parametrized by $r(t) = 2ti + (2 - t)j$ for $- \frac{1}{2}\le t\le \frac{5}{2}$?

1. $\int_{- \frac{1}{2}}^{\frac{5}{2}}6 \sqrt{5} \left(- 8 t^{3} - t + 2\right)\,\mathrm{d}t$.
2. $\int_{- \frac{1}{2}}^{\frac{5}{2}}6 \sqrt{5} \left(- 8 t^{3} + t - 2\right)\,\mathrm{d}t$
3. $\int_{- \frac{1}{2}}^{\frac{5}{2}}- 48 t^{3} - 6 t + 12\,\mathrm{d}t$
4. $\int_{- \frac{1}{2}}^{\frac{5}{2}}\frac{6 \sqrt{5} \left(- 8 t^{3} - t + 2\right)}{5}\,\mathrm{d}t$
5. $\int_{- \frac{1}{2}}^{\frac{5}{2}}- 240 t^{3} - 30 t + 60\,\mathrm{d}t$

Since $r(t)=\langle 2 t, 2 - t\rangle,$ then along the curve we have $x=2 t$, $y=2 - t$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 - t)j \\ &= (2)\,i+(-1)\,j \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &= \sqrt{(2)^2+(-1)^2} \\ &= \sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=- 6 x^{3} + 6 y$, we obtain

$$
\begin{aligned}f(r(t))&=-6\left((2 t)^3-(2 - t)\right) \\ &= -6\left(8t^3-2+t\right) \\ &= - 48 t^{3} - 6 t + 12.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{- \frac{1}{2}}^{\frac{5}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{- \frac{1}{2}}^{\frac{5}{2}}(- 48 t^{3} - 6 t + 12)(\sqrt{5})\,\mathrm{d}t \\ &= \int_{- \frac{1}{2}}^{\frac{5}{2}}6 \sqrt{5} \left(- 8 t^{3} - t + 2\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Generated linear_cubic seed 1

Which of the following is equivalent to the integral $\displaystyle \int_C-5\left((x^{3} - y)\right)ds$, where the curve $C$ is parametrized by $r(t) = 2ti + (2 - t)j$ for $- \frac{3}{2}\le t\le 3$?

1. $\int_{- \frac{3}{2}}^{3}\sqrt{5} \left(- 8 t^{3} - t + 2\right)\,\mathrm{d}t$
2. $\int_{- \frac{3}{2}}^{3}5 \sqrt{5} \left(- 8 t^{3} + t - 2\right)\,\mathrm{d}t$
3. $\int_{- \frac{3}{2}}^{3}- 40 t^{3} - 5 t + 10\,\mathrm{d}t$
4. $\int_{- \frac{3}{2}}^{3}5 \sqrt{5} \left(- 8 t^{3} - t + 2\right)\,\mathrm{d}t$.
5. $\int_{- \frac{3}{2}}^{3}- 200 t^{3} - 25 t + 50\,\mathrm{d}t$

Since $r(t)=\langle 2 t, 2 - t\rangle,$ then along the curve we have $x=2 t$, $y=2 - t$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 - t)j \\ &= (2)\,i+(-1)\,j \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &= \sqrt{(2)^2+(-1)^2} \\ &= \sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=- 5 x^{3} + 5 y$, we obtain

$$
\begin{aligned}f(r(t))&=-5\left((2 t)^3-(2 - t)\right) \\ &= -5\left(8t^3-2+t\right) \\ &= - 40 t^{3} - 5 t + 10.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{- \frac{3}{2}}^{3} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{- \frac{3}{2}}^{3}(- 40 t^{3} - 5 t + 10)(\sqrt{5})\,\mathrm{d}t \\ &= \int_{- \frac{3}{2}}^{3}5 \sqrt{5} \left(- 8 t^{3} - t + 2\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Generated hard_product_square seed 0

Which of the following is equivalent to $\int_C x y - z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle 2 t^{2}, 2 t - 1, t + 2\rangle$ for $\frac{1}{2}\le t\le \frac{5}{2}$?

1. $\int_{\frac{1}{2}}^{\frac{5}{2}}4 t^{3} - 3 t^{2} - 4 t - 4\,\mathrm{d}t$
2. $\int_{\frac{1}{2}}^{\frac{5}{2}}\sqrt{16 t^{2} + 5} \left(4 t^{3} - 3 t^{2} - 4 t - 4\right)\,\mathrm{d}t$
3. $\int_{\frac{1}{2}}^{\frac{5}{2}}\sqrt{16 t^{2} + 5} \left(4 t^{3} - t^{2} + 4 t + 4\right)\,\mathrm{d}t$
4. $\int_{\frac{1}{2}}^{\frac{5}{2}}- \left(16 t^{2} + 5\right) \left(- 4 t^{3} + 3 t^{2} + 4 t + 4\right)\,\mathrm{d}t$
5. $\int_{\frac{1}{2}}^{\frac{5}{2}}\frac{4 t^{3} - 3 t^{2} - 4 t - 4}{\sqrt{16 t^{2} + 5}}\,\mathrm{d}t$

Since $r(t)=\langle 2 t^{2}, 2 t - 1, t + 2\rangle,$ then along the curve we have $x=2 t^{2}$, $y=2 t - 1$, $z=t + 2$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(2 t - 1)j+\frac{\mathrm{d}}{\mathrm{d}t}(t + 2)k \\ &= (4 t)\,i+(2)\,j+(1)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(4 t)^2+(2)^2+(1)^2} \\ &= \sqrt{16 t^{2} + 5}\end{aligned}
$$

Now, since $f(x,y,z)=x y - z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=(2 t^{2})(2 t - 1)-(t + 2)^2 \\ &= 4t^3+(-2)t^2-\left(1t^2+(4)t+4\right) \\ &= 4 t^{3} - 3 t^{2} - 4 t - 4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{\frac{1}{2}}^{\frac{5}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{\frac{5}{2}}(4 t^{3} - 3 t^{2} - 4 t - 4)(\sqrt{16 t^{2} + 5})\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{\frac{5}{2}}\sqrt{16 t^{2} + 5} \left(4 t^{3} - 3 t^{2} - 4 t - 4\right)\,\mathrm{d}t.\end{aligned}
$$

---

## Generated hard_product_square seed 1

Which of the following is equivalent to $\int_C x y - z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle t^{2}, 3 t - 1, t - 3\rangle$ for $\frac{1}{2}\le t\le 3$?

1. $\int_{\frac{1}{2}}^{3}2 \left(2 t^{2} + 5\right) \left(3 t^{3} - 2 t^{2} + 6 t - 9\right)\,\mathrm{d}t$
2. $\int_{\frac{1}{2}}^{3}\sqrt{4 t^{2} + 10} \left(3 t^{3} - 6 t + 9\right)\,\mathrm{d}t$
3. $\int_{\frac{1}{2}}^{3}\sqrt{4 t^{2} + 10} \left(3 t^{3} - 2 t^{2} + 6 t - 9\right)\,\mathrm{d}t$
4. $\int_{\frac{1}{2}}^{3}3 t^{3} - 2 t^{2} + 6 t - 9\,\mathrm{d}t$
5. $\int_{\frac{1}{2}}^{3}\frac{\sqrt{2} \left(3 t^{3} - 2 t^{2} + 6 t - 9\right)}{2 \sqrt{2 t^{2} + 5}}\,\mathrm{d}t$

Since $r(t)=\langle t^{2}, 3 t - 1, t - 3\rangle,$ then along the curve we have $x=t^{2}$, $y=3 t - 1$, $z=t - 3$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(3 t - 1)j+\frac{\mathrm{d}}{\mathrm{d}t}(t - 3)k \\ &= (2 t)\,i+(3)\,j+(1)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(2 t)^2+(3)^2+(1)^2} \\ &= \sqrt{4 t^{2} + 10}\end{aligned}
$$

Now, since $f(x,y,z)=x y - z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=(t^{2})(3 t - 1)-(t - 3)^2 \\ &= 3t^3+(-1)t^2-\left(1t^2+(-6)t+9\right) \\ &= 3 t^{3} - 2 t^{2} + 6 t - 9.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{\frac{1}{2}}^{3} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{3}(3 t^{3} - 2 t^{2} + 6 t - 9)(\sqrt{4 t^{2} + 10})\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{3}\sqrt{4 t^{2} + 10} \left(3 t^{3} - 2 t^{2} + 6 t - 9\right)\,\mathrm{d}t.\end{aligned}
$$
