# Scalar ds evaluation review

Raw evidence replays preserve original omissions and teaching errors. Completed profiles infer missing keys and author solutions. Normal method profiles are learner-eligible.

## ORIGINAL PARAMETERIZED REPLAY sum / raw_sum

Evaluate the line integral of the function $f(x,y)=x+y$ along the curve $C$ parametrized by $r(t)=⟨t,\,1+t⟩$ for $t\in [0,1].$

1. $2$
2. $4$
3. $2\sqrt{2}$
4. $\frac{\sqrt{2}}{2}$
5. $\sqrt{2}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨t,\,1+t⟩,$ then along the curve we have $x=t$ and $y=1+t.$    

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(1+t)j \\  & =\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+(1+t)=2t+1.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}(2t+1)\cdot \sqrt{2}\cdot \text{d}t \\  & =\sqrt{2}{\int }_{0}^{1}2t+1\,\text{d}t \\  & =\sqrt{2}{[{t}^{2}+t]}_{0}^{1} \\  & =\sqrt{2}(1+1-0) \\  & =2\sqrt{2}.\end{aligned}
$$

## ORIGINAL PARAMETERIZED REPLAY reciprocal / raw_reciprocal

Evaluate the line integral of the function $f(x,y)=\frac{1}{y-x}$ along the curve $C$ parametrized by $r(t)=⟨t,\,t-4⟩$ for $t\in [0,4].$

1. $-\frac{\sqrt{2}}{2}$
2. $-\sqrt{2}$
3. $2\sqrt{2}$
4. $\frac{\sqrt{2}}{2}$
5. $\frac{\sqrt{2}}{4}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨t,\,t-4⟩,$ then along the curve we have $x=t$ and $y=t-4.$     

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{y-x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(4-t)}=-\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{4}-\frac{1}{4}\cdot \sqrt{2}\,\cdot \,\text{d}t \\  & =-\frac{\sqrt{2}}{4}{\int }_{0}^{4}\text{d}t \\  & =-\frac{\sqrt{2}}{4}t\,{|}_{0}^{4} \\  & =-\frac{\sqrt{2}}{4}\cdot (4-0) \\  & =-\sqrt{2}.\end{aligned}
$$

## ORIGINAL PARAMETERIZED REPLAY circle_cos / raw_circle_cos

Evaluate the integral ${\int }_{C}(2{x}^{2}-16)\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=4\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j$ for $0\le t\le \frac{\pi }{4}.$

1. $64$
2. $16$
3. $22\sqrt{2}$
4. $16\sqrt{2}$
5. $32$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=4\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j,$ then along the curve we have $x=4\operatorname{cos}⁡t$ and $y=4\operatorname{sin}⁡t.$  

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)j \\  & =-4\operatorname{sin}⁡t\,i+4\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-4\operatorname{sin}⁡t)^{2}+(4\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{sin}^{2}⁡t+16{cos}^{2}⁡t} \\  & =\sqrt{16({sin}^{2}⁡t+{cos}^{2}⁡t)} \\  & =\sqrt{16} \\  & =4\end{aligned}
$$

 

Now, if $f(x,y)=2{x}^{2}-16$, then we obtain

$$
\begin{aligned}f(r(t)) & =2(4\operatorname{cos}⁡t)^{2}-16 \\  & =16(2{cos}^{2}⁡t-1) \\  & =16\operatorname{cos}⁡2t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}(2{x}^{2}-16)\,\text{d}s & ={\int }_{0}^{\pi /4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi /4}16\operatorname{cos}⁡2t\cdot 4\,\text{d}t \\  & =64{\int }_{0}^{\pi /4}\operatorname{cos}⁡2t\,\text{d}t \\  & =64{[\frac{1}{2}\operatorname{sin}⁡2t]}_{0}^{\pi /4} \\  & =32[\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{sin}⁡0] \\  & =32(1-0) \\  & =32.\end{aligned}
$$

## ORIGINAL PARAMETERIZED REPLAY circle_sin / raw_circle_sin

Evaluate the integral ${\int }_{C}{y}^{2}\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $0\le t\le \frac{\pi }{4}.$

1. $\frac{2\pi -1}{4}$
2. $\pi -2$
3. $2\pi -1$
4. $\frac{\pi +1}{4}$
5. $\frac{\pi +2}{4}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,$ then along the curve we have $x=2\operatorname{cos}⁡t$ and $y=2\operatorname{sin}⁡t.$  

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)j \\  & =-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2\operatorname{sin}⁡t)^{2}+(2\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{4{sin}^{2}⁡t+4{cos}^{2}⁡t} \\  & =\sqrt{4({sin}^{2}⁡t+{cos}^{2}⁡t)} \\  & =\sqrt{4} \\  & =2\end{aligned}
$$

 

Now, if $f(x,y)={y}^{2}$, then we obtain

$$
\begin{aligned}f(r(t)) & ={(2\operatorname{sin}⁡t)}^{2}=4{sin}^{2}⁡t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}{y}^{2}\,\text{d}s & ={\int }_{0}^{\pi /4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi /4}4{sin}^{2}⁡t\cdot 2\cdot \text{d}t \\  & =8{\int }_{0}^{\pi /4}{sin}^{2}⁡t\,\text{d}t \\  & =8{\int }_{0}^{\pi /4}(\frac{1-\operatorname{cos}⁡2t}{2})\text{d}t \\  & =4{\int }_{0}^{\pi /4}(1-\operatorname{cos}⁡2t)\text{d}t \\  & =4{[t-\frac{\operatorname{sin}⁡2t}{2}]}_{0}^{\pi /4} \\  & =4[(\frac{\pi }{4}-\frac{1}{2})-0] \\  & =\pi -2.\end{aligned}
$$

## ORIGINAL PARAMETERIZED REPLAY cubic / raw_cubic

Evaluate the integral ${\int }_{C}({x}^{3}-2{y}^{3})\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=4{t}^{2}\,i+3{t}^{2}\,j$ for $0\le t\le 1.$

1. $8$
2. $7.5$
3. $12.5$
4. $15$
5. $10$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=4{t}^{2}\,i+3{t}^{2}\,j,$ then along the curve we have $x=4{t}^{2}$ and $y=3{t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4{t}^{2})i+\frac{\text{d}}{\text{d}t}(3{t}^{2})j \\  & =8t\,i+6t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(8t)^{2}+(6t)^{2}} \\  & =\sqrt{64{t}^{2}+36{t}^{2}} \\  & =\sqrt{100{t}^{2}} \\  & =10|t| \\  & =10t.\end{aligned}
$$

Notice that $|t|=t$ since $t>0$ along the path of $C.$ 

Now, if $f(x,y)={x}^{3}-2{y}^{3}$, then we obtain

$$
\begin{aligned}f(r(t)) & ={(4{t}^{2})}^{3}-2{(3{t}^{2})}^{3} \\  & ={4}^{3}{t}^{6}-2\cdot {3}^{3}{t}^{6} \\  & =64{t}^{6}-54{t}^{6} \\  & =10{t}^{6}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}({x}^{3}-{y}^{3})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}10{t}^{6}\cdot 10t\cdot \text{d}t \\  & =100{\int }_{0}^{1}{t}^{7}\,\text{d}t \\  & =100\cdot \frac{{t}^{8}}{8}\,{|}_{0}^{1} \\  & =100[\frac{{1}^{8}}{8}+\frac{{0}^{8}}{8}] \\  & =100\cdot \frac{1}{8} \\  & =12.5.\end{aligned}
$$

## ORIGINAL PARAMETERIZED REPLAY fractional / raw_fractional

Evaluate the line integral of the function $f(x, y) = 3x$ along the curve $C$ parametrized by $r(t) = ⟨\frac{4t^{3/2}}{3}, \frac{t^{2}}{2} - t⟩$ for $t ∈ [0, 1]$.

1. $\frac{104}{35}$
2. $\frac{24}{5}$
3. $\frac{96}{35}$
4. $\frac{54}{7}$
5. $\frac{62}{7}$

[No worked solution in raw source.]

## ORIGINAL PARAMETERIZED REPLAY involute / raw_involute

Evaluate the integral $\displaystyle \int_(C)(x^{2} + y^{2})ds$, where $C$ is the curve parametrized by $r(t) = 3(\cos t + t\sin t)i + 3(\sin t - t\cos t)j$ for $0 \le t \le 2π$.

1. $27(1 + 2π^{2})$
2. $54π^{2}(1 + 2π^{2})$
3. $54(1 + π^{4})$
4. $54(1 + π^{2})$
5. $18π^{2}(1 + 2π^{2})$

[No worked solution in raw source.]

## GENERATED / observed label/absence sum / raw_sum

Evaluate the line integral of the function $f(x,y)=2\left(x+y\right)$ along the curve $C$ parametrized by $r(t)=⟨t,\,1+t⟩$ for $t\in [0,1].$

1. $2\left(2\right)$
2. $2\left(4\right)$
3. $2\left(\frac{\sqrt{2}}{2}\right)$
4. $2\left(\sqrt{2}\right)$
5. $2\left(2\sqrt{2}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨t,\,1+t⟩,$ then along the curve we have $x=t$ and $y=1+t.$    

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(1+t)j \\  & =\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=2\left(x+y\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left(t+(1+t)\right)=2\left(2t+1.\right)\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{1}(2t+1)\cdot \sqrt{2}\cdot \text{d}t\right) \\  & =2\left(\sqrt{2}{\int }_{0}^{1}2t+1\,\text{d}t\right) \\  & =2\left(\sqrt{2}{[{t}^{2}+t]}_{0}^{1}\right) \\  & =2\left(\sqrt{2}(1+1-0)\right) \\  & =2\left(2\sqrt{2}.\right)\end{aligned}
$$

## GENERATED / observed label/absence reciprocal / raw_reciprocal

Evaluate the line integral of the function $f(x,y)=2\left(\frac{1}{y-x}\right)$ along the curve $C$ parametrized by $r(t)=⟨t,\,t-4⟩$ for $t\in [0,4].$

1. $2\left(-\frac{\sqrt{2}}{2}\right)$
2. $2\left(-\sqrt{2}\right)$
3. $2\left(\frac{\sqrt{2}}{2}\right)$
4. $2\left(\frac{\sqrt{2}}{4}\right)$
5. $2\left(2\sqrt{2}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨t,\,t-4⟩,$ then along the curve we have $x=t$ and $y=t-4.$     

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=2\left(\frac{1}{y-x}\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left(\frac{1}{t-(4-t)}\right)=2\left(-\frac{1}{4}.\right)\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{4}-\frac{1}{4}\cdot \sqrt{2}\,\cdot \,\text{d}t\right) \\  & =2\left(-\frac{\sqrt{2}}{4}{\int }_{0}^{4}\text{d}t\right) \\  & =2\left(-\frac{\sqrt{2}}{4}t\,{|}_{0}^{4}\right) \\  & =2\left(-\frac{\sqrt{2}}{4}\cdot (4-0)\right) \\  & =2\left(-\sqrt{2}.\right)\end{aligned}
$$

## GENERATED / observed label/absence circle_cos / raw_circle_cos

Evaluate the integral ${\int }_{C}(2\left(2{x}^{2}-16\right))\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=4\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j$ for $0\le t\le \frac{\pi }{4}.$

1. $2\left(64\right)$
2. $2\left(16\right)$
3. $2\left(16\sqrt{2}\right)$
4. $2\left(32\right)$
5. $2\left(22\sqrt{2}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=4\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j,$ then along the curve we have $x=4\operatorname{cos}⁡t$ and $y=4\operatorname{sin}⁡t.$  

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)j \\  & =-4\operatorname{sin}⁡t\,i+4\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-4\operatorname{sin}⁡t)^{2}+(4\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{sin}^{2}⁡t+16{cos}^{2}⁡t} \\  & =\sqrt{16({sin}^{2}⁡t+{cos}^{2}⁡t)} \\  & =\sqrt{16} \\  & =4\end{aligned}
$$

 

Now, if $f(x,y)=2\left(2{x}^{2}-16\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =2\left(2(4\operatorname{cos}⁡t)^{2}-16\right) \\  & =2\left(16(2{cos}^{2}⁡t-1)\right) \\  & =2\left(16\operatorname{cos}⁡2t.\right)\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}(2\left(2{x}^{2}-16\right))\,\text{d}s & ={\int }_{0}^{\pi /4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{\pi /4}16\operatorname{cos}⁡2t\cdot 4\,\text{d}t\right) \\  & =2\left(64{\int }_{0}^{\pi /4}\operatorname{cos}⁡2t\,\text{d}t\right) \\  & =2\left(64{[\frac{1}{2}\operatorname{sin}⁡2t]}_{0}^{\pi /4}\right) \\  & =2\left(32[\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{sin}⁡0]\right) \\  & =2\left(32(1-0)\right) \\  & =2\left(32.\right)\end{aligned}
$$

## GENERATED / observed label/absence circle_sin / raw_circle_sin

Evaluate the integral ${\int }_{C}2\left({y}^{2}\right)\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $0\le t\le \frac{\pi }{4}.$

1. $2\left(\frac{2\pi -1}{4}\right)$
2. $2\left(\pi -2\right)$
3. $2\left(\frac{\pi +1}{4}\right)$
4. $2\left(\frac{\pi +2}{4}\right)$
5. $2\left(2\pi -1\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j,$ then along the curve we have $x=2\operatorname{cos}⁡t$ and $y=2\operatorname{sin}⁡t.$  

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)j \\  & =-2\operatorname{sin}⁡t\,i+2\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(-2\operatorname{sin}⁡t)^{2}+(2\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{4{sin}^{2}⁡t+4{cos}^{2}⁡t} \\  & =\sqrt{4({sin}^{2}⁡t+{cos}^{2}⁡t)} \\  & =\sqrt{4} \\  & =2\end{aligned}
$$

 

Now, if $f(x,y)=2\left({y}^{2}\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =2\left({(2\operatorname{sin}⁡t)}^{2}\right)=2\left(4{sin}^{2}⁡t.\right)\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}2\left({y}^{2}\right)\,\text{d}s & ={\int }_{0}^{\pi /4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{\pi /4}4{sin}^{2}⁡t\cdot 2\cdot \text{d}t\right) \\  & =2\left(8{\int }_{0}^{\pi /4}{sin}^{2}⁡t\,\text{d}t\right) \\  & =2\left(8{\int }_{0}^{\pi /4}(\frac{1-\operatorname{cos}⁡2t}{2})\text{d}t\right) \\  & =2\left(4{\int }_{0}^{\pi /4}(1-\operatorname{cos}⁡2t)\text{d}t\right) \\  & =2\left(4{[t-\frac{\operatorname{sin}⁡2t}{2}]}_{0}^{\pi /4}\right) \\  & =2\left(4[(\frac{\pi }{4}-\frac{1}{2})-0]\right) \\  & =2\left(\pi -2.\right)\end{aligned}
$$

## GENERATED / observed label/absence cubic / raw_cubic

Evaluate the integral ${\int }_{C}(2\left({x}^{3}-2{y}^{3}\right))\,\text{d}s,$ where $C$ is the curve parametrized by $r(t)=4{t}^{2}\,i+3{t}^{2}\,j$ for $0\le t\le 1.$

1. $2\left(8\right)$
2. $2\left(7.5\right)$
3. $2\left(15\right)$
4. $2\left(10\right)$
5. $2\left(12.5\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=4{t}^{2}\,i+3{t}^{2}\,j,$ then along the curve we have $x=4{t}^{2}$ and $y=3{t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4{t}^{2})i+\frac{\text{d}}{\text{d}t}(3{t}^{2})j \\  & =8t\,i+6t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(8t)^{2}+(6t)^{2}} \\  & =\sqrt{64{t}^{2}+36{t}^{2}} \\  & =\sqrt{100{t}^{2}} \\  & =10|t| \\  & =10t.\end{aligned}
$$

Notice that $|t|=t$ since $t>0$ along the path of $C.$ 

Now, if $f(x,y)=2\left({x}^{3}-2{y}^{3}\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =2\left({(4{t}^{2})}^{3}-2{(3{t}^{2})}^{3}\right) \\  & =2\left({4}^{3}{t}^{6}-2\cdot {3}^{3}{t}^{6}\right) \\  & =2\left(64{t}^{6}-54{t}^{6}\right) \\  & =2\left(10{t}^{6}.\right)\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}({x}^{3}-{y}^{3})\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{1}10{t}^{6}\cdot 10t\cdot \text{d}t\right) \\  & =2\left(100{\int }_{0}^{1}{t}^{7}\,\text{d}t\right) \\  & =2\left(100\cdot \frac{{t}^{8}}{8}\,{|}_{0}^{1}\right) \\  & =2\left(100[\frac{{1}^{8}}{8}+\frac{{0}^{8}}{8}]\right) \\  & =2\left(100\cdot \frac{1}{8}\right) \\  & =2\left(12.5.\right)\end{aligned}
$$

## GENERATED / observed label/absence fractional / raw_fractional

Evaluate the line integral of the function $f(x, y) = 2\left(3x\right)$ along the curve $C$ parametrized by $r(t) = ⟨\frac{4t^{3/2}}{3}, \frac{t^{2}}{2} - t⟩$ for $t ∈ [0, 1]$.

1. $2\left(\frac{104}{35}\right)$
2. $2\left(\frac{24}{5}\right)$
3. $2\left(\frac{54}{7}\right)$
4. $2\left(\frac{62}{7}\right)$
5. $2\left(\frac{96}{35}\right)$

[No worked solution in raw source.]

## GENERATED / inferred key; authored level; authored worked solution; opaque historical bank fractional / completed_fractional

Evaluate the line integral of the function $f(x, y) = 3x$ along the curve $C$ parametrized by $r(t) = ⟨\frac{4t^{3/2}}{3}, \frac{t^{2}}{2} - t⟩$ for $t ∈ [0, 1]$.

1. $\frac{104}{35}$
2. $\frac{24}{5}$
3. $\frac{96}{35}$
4. $\frac{54}{7}$
5. $\frac{62}{7}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{4 t^{\frac{3}{2}}}{3},\,\frac{t^{2}}{2} - t⟩,$ then along the curve we have $x=\frac{4 t^{\frac{3}{2}}}{3}$ and $y=\frac{t^{2}}{2} - t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{4 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(\frac{t^{2}}{2} - t)j \\ &=(2 \sqrt{t})i+(t - 1)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(2 \sqrt{t})^2+(t - 1)^2} \\ &=\sqrt{4t+1(t-1)^2} \\ &=\sqrt{1(t^2+2t+1)} \\ &=1|t+1| \\ &=t + 1\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=3 x$, then we obtain

$$
\begin{aligned}f(r(t))&=(3)(\frac{4 t^{\frac{3}{2}}}{3}) \\ &=4 t^{\frac{3}{2}}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 3 x\,\text{d}s&=\int_{0}^{1}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{1}(4 t^{\frac{3}{2}})\cdot (t + 1)\,\text{d}t \\ &=\int_{0}^{1}4t^{3/2}(t+1)\,\text{d}t \\ &=\int_{0}^{1}4 t^{\frac{5}{2}} + 4 t^{\frac{3}{2}}\,\text{d}t \\ &=\left[(\frac{8 t^{\frac{7}{2}}}{7})+(\frac{8 t^{\frac{5}{2}}}{5})\right]_{0}^{1} \\ &=\left((\frac{8 (1)^{\frac{7}{2}}}{7})+(\frac{8 (1)^{\frac{5}{2}}}{5})\right)-\left((\frac{8 (0)^{\frac{7}{2}}}{7})+(\frac{8 (0)^{\frac{5}{2}}}{5})\right) \\ &=\left((\frac{8}{7})+(\frac{8}{5})\right)-\left((0)+(0)\right) \\ &=\frac{96}{35}.\end{aligned}
$$

## GENERATED / observed label/absence involute / raw_involute

Evaluate the integral $\displaystyle \int_(C)(2\left(x^{2} + y^{2}\right))ds$, where $C$ is the curve parametrized by $r(t) = 3(\cos t + t\sin t)i + 3(\sin t - t\cos t)j$ for $0 \le t \le 2π$.

1. $2\left(27(1 + 2π^{2})\right)$
2. $2\left(54π^{2}(1 + 2π^{2})\right)$
3. $2\left(54(1 + π^{2})\right)$
4. $2\left(18π^{2}(1 + 2π^{2})\right)$
5. $2\left(54(1 + π^{4})\right)$

[No worked solution in raw source.]

## GENERATED / inferred key; authored level; authored worked solution; opaque historical bank involute / completed_involute

Evaluate the integral $\displaystyle \int_(C)(x^{2} + y^{2})ds$, where $C$ is the curve parametrized by $r(t) = 3(\cos t + t\sin t)i + 3(\sin t - t\cos t)j$ for $0 \le t \le 2π$.

1. $27(1 + 2π^{2})$
2. $54π^{2}(1 + 2π^{2})$
3. $54(1 + π^{4})$
4. $54(1 + π^{2})$
5. $18π^{2}(1 + 2π^{2})$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 t \sin{\left(t \right)} + 3 \cos{\left(t \right)},\,- 3 t \cos{\left(t \right)} + 3 \sin{\left(t \right)}⟩,$ then along the curve we have $x=3 t \sin{\left(t \right)} + 3 \cos{\left(t \right)}$ and $y=- 3 t \cos{\left(t \right)} + 3 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 t \sin{\left(t \right)} + 3 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 3 t \cos{\left(t \right)} + 3 \sin{\left(t \right)})j \\ &=(3)(-\sin t+\sin t+t\cos t)i+(3)(\cos t-\cos t+t\sin t)j \\ &=(3 t \cos{\left(t \right)})i+(3 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(3 t \cos{\left(t \right)})^2+(3 t \sin{\left(t \right)})^2} \\ &=\sqrt{9t^2(\cos^2t+\sin^2t)} \\ &=3|t| \\ &=3 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=x^{2} + y^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(1)\left((3 t \sin{\left(t \right)} + 3 \cos{\left(t \right)})^2+(- 3 t \cos{\left(t \right)} + 3 \sin{\left(t \right)})^2\right)+(0) \\ &=(9)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(0) \\ &=(9)(1+t^2)+(0) \\ &=9 t^{2} + 9\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x^{2} + y^{2}\,\text{d}s&=\int_{0}^{2 \pi}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{2 \pi}(9 t^{2} + 9)\cdot (3 t)\,\text{d}t \\ &=\int_{0}^{2 \pi}27 t^{3} + 27 t\,\text{d}t \\ &=\left[(\frac{27 t^{2}}{2})+(\frac{27 t^{4}}{4})\right]_{0}^{2 \pi} \\ &=\left((\frac{27 (2 \pi)^{2}}{2})+(\frac{27 (2 \pi)^{4}}{4})\right)-\left((\frac{27 (0)^{2}}{2})+(\frac{27 (0)^{4}}{4})\right) \\ &=\left((54 \pi^{2})+(108 \pi^{4})\right)-\left((0)+(0)\right) \\ &=\pi^{2} \left(54 + 108 \pi^{2}\right).\end{aligned}
$$

## GENERATED / observed family workload sum / method_sum

Evaluate the line integral of the function $f(x,y)=- x - y$ along the curve $C$ parametrized by $r(t)=⟨3 t,\,3 t - 6⟩$ for $t\in [1,5].$

1. $-864$
2. $-48$
3. $- 144 \sqrt{2}$
4. $- 36 \sqrt{2}$
5. $- 216 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 t,\,3 t - 6⟩,$ then along the curve we have $x=3 t$ and $y=3 t - 6.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 t)i+\frac{\text{d}}{\text{d}t}(3 t - 6)j \\ &=(3)i+(3)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(3)^2+(3)^2} \\ &=\sqrt{18} \\ &=3 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- x - y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-1)\left(3 t+(3 t - 6)\right) \\ &=6 - 6 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - x - y\,\text{d}s&=\int_{1}^{5}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{5}(6 - 6 t)\cdot (3 \sqrt{2})\,\text{d}t \\ &=(3 \sqrt{2})\int_{1}^{5}6 - 6 t\,\text{d}t \\ &=\int_{1}^{5}- 18 \sqrt{2} t + 18 \sqrt{2}\,\text{d}t \\ &=(- 3 \sqrt{2})\left[3 t^{2}+(- 6 t)\right]_{1}^{5} \\ &=\left[(- 9 \sqrt{2} t^{2})+(18 \sqrt{2} t)\right]_{1}^{5} \\ &=\left((- 9 \sqrt{2} (5)^{2})+(18 \sqrt{2} (5))\right)-\left((- 9 \sqrt{2} (1)^{2})+(18 \sqrt{2} (1))\right) \\ &=\left((- 225 \sqrt{2})+(90 \sqrt{2})\right)-\left((- 9 \sqrt{2})+(18 \sqrt{2})\right) \\ &=- 144 \sqrt{2}.\end{aligned}
$$

## GENERATED / observed family workload sum / method_sum

Evaluate the line integral of the function $f(x,y)=- 3 x - 3 y$ along the curve $C$ parametrized by $r(t)=⟨- 3 t,\,- 3 t - 2⟩$ for $t\in [-1,3].$

1. $1728$
2. $216 \sqrt{2}$
3. $180 \sqrt{2}$
4. $288 \sqrt{2}$
5. $96$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨- 3 t,\,- 3 t - 2⟩,$ then along the curve we have $x=- 3 t$ and $y=- 3 t - 2.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(- 3 t)i+\frac{\text{d}}{\text{d}t}(- 3 t - 2)j \\ &=(-3)i+(-3)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(-3)^2+(-3)^2} \\ &=\sqrt{18} \\ &=3 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- 3 x - 3 y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)\left(- 3 t+(- 3 t - 2)\right) \\ &=18 t + 6\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x - 3 y\,\text{d}s&=\int_{-1}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{-1}^{3}(18 t + 6)\cdot (3 \sqrt{2})\,\text{d}t \\ &=(3 \sqrt{2})\int_{-1}^{3}18 t + 6\,\text{d}t \\ &=\int_{-1}^{3}54 \sqrt{2} t + 18 \sqrt{2}\,\text{d}t \\ &=(- 9 \sqrt{2})\left[- 3 t^{2}+(- 2 t)\right]_{-1}^{3} \\ &=\left[(27 \sqrt{2} t^{2})+(18 \sqrt{2} t)\right]_{-1}^{3} \\ &=\left((27 \sqrt{2} (3)^{2})+(18 \sqrt{2} (3))\right)-\left((27 \sqrt{2} (-1)^{2})+(18 \sqrt{2} (-1))\right) \\ &=\left((243 \sqrt{2})+(54 \sqrt{2})\right)-\left((27 \sqrt{2})+(- 18 \sqrt{2})\right) \\ &=288 \sqrt{2}.\end{aligned}
$$

## GENERATED / observed family workload reciprocal / method_reciprocal

Evaluate the line integral of the function $f(x,y)=- \frac{1}{- x + y}$ along the curve $C$ parametrized by $r(t)=⟨3 t,\,3 t - 6⟩$ for $t\in [1,5].$

1. $12$
2. $\frac{2}{3}$
3. $2 \sqrt{2}$
4. $72 \sqrt{2}$
5. $- 2 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 t,\,3 t - 6⟩,$ then along the curve we have $x=3 t$ and $y=3 t - 6.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 t)i+\frac{\text{d}}{\text{d}t}(3 t - 6)j \\ &=(3)i+(3)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(3)^2+(3)^2} \\ &=\sqrt{18} \\ &=3 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- \frac{1}{- x + y}$, then we obtain

$$
\begin{aligned}f(r(t))&=\frac{-1}{(3 t - 6)-(3 t)} \\ &=\frac{-1}{-6} \\ &=\frac{1}{6}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - \frac{1}{- x + y}\,\text{d}s&=\int_{1}^{5}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{5}(\frac{1}{6})\cdot (3 \sqrt{2})\,\text{d}t \\ &=(3 \sqrt{2})\int_{1}^{5}\frac{1}{6}\,\text{d}t \\ &=\int_{1}^{5}\frac{\sqrt{2}}{2}\,\text{d}t \\ &=(\frac{\sqrt{2}}{2})\left[t\right]_{1}^{5} \\ &=\left[(\frac{\sqrt{2} t}{2})\right]_{1}^{5} \\ &=\left((\frac{\sqrt{2} (5)}{2})\right)-\left((\frac{\sqrt{2} (1)}{2})\right) \\ &=\left((\frac{5 \sqrt{2}}{2})\right)-\left((\frac{\sqrt{2}}{2})\right) \\ &=2 \sqrt{2}.\end{aligned}
$$

## GENERATED / observed family workload reciprocal / method_reciprocal

Evaluate the line integral of the function $f(x,y)=- \frac{3}{- x + y}$ along the curve $C$ parametrized by $r(t)=⟨- 3 t,\,- 3 t - 2⟩$ for $t\in [-1,3].$

1. $108$
2. $- 18 \sqrt{2}$
3. $72 \sqrt{2}$
4. $18 \sqrt{2}$
5. $6$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨- 3 t,\,- 3 t - 2⟩,$ then along the curve we have $x=- 3 t$ and $y=- 3 t - 2.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(- 3 t)i+\frac{\text{d}}{\text{d}t}(- 3 t - 2)j \\ &=(-3)i+(-3)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(-3)^2+(-3)^2} \\ &=\sqrt{18} \\ &=3 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- \frac{3}{- x + y}$, then we obtain

$$
\begin{aligned}f(r(t))&=\frac{-3}{(- 3 t - 2)-(- 3 t)} \\ &=\frac{-3}{-2} \\ &=\frac{3}{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - \frac{3}{- x + y}\,\text{d}s&=\int_{-1}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{-1}^{3}(\frac{3}{2})\cdot (3 \sqrt{2})\,\text{d}t \\ &=(3 \sqrt{2})\int_{-1}^{3}\frac{3}{2}\,\text{d}t \\ &=\int_{-1}^{3}\frac{9 \sqrt{2}}{2}\,\text{d}t \\ &=(\frac{9 \sqrt{2}}{2})\left[t\right]_{-1}^{3} \\ &=\left[(\frac{9 \sqrt{2} t}{2})\right]_{-1}^{3} \\ &=\left((\frac{9 \sqrt{2} (3)}{2})\right)-\left((\frac{9 \sqrt{2} (-1)}{2})\right) \\ &=\left((\frac{27 \sqrt{2}}{2})\right)-\left((- \frac{9 \sqrt{2}}{2})\right) \\ &=18 \sqrt{2}.\end{aligned}
$$

## GENERATED / observed family workload circle_cos / method_circle_cos

Evaluate the line integral of the function $f(x,y)=2 x^{2} - 16$ along the curve $C$ parametrized by $r(t)=⟨4 \cos{\left(t \right)},\,4 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{2},- \frac{\pi}{4}].$

1. $-128$
2. $-8$
3. $-32$
4. $-32 + 16 \pi$
5. $-64$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨4 \cos{\left(t \right)},\,4 \sin{\left(t \right)}⟩,$ then along the curve we have $x=4 \cos{\left(t \right)}$ and $y=4 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(4 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(4 \sin{\left(t \right)})j \\ &=(- 4 \sin{\left(t \right)})i+(4 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 4 \sin{\left(t \right)})^2+(4 \cos{\left(t \right)})^2} \\ &=\sqrt{16\sin^2t+16\cos^2t} \\ &=\sqrt{16(\sin^2t+\cos^2t)} \\ &=\sqrt{16} \\ &=4\end{aligned}
$$

Now, if $f(x,y)=2 x^{2} - 16$, then we obtain

$$
\begin{aligned}f(r(t))&=(1)\left(2(4 \cos{\left(t \right)})^2-16\right) \\ &=(16)(2\cos^2t-1) \\ &=16 \cos{\left(2 t \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x^{2} - 16\,\text{d}s&=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}(16 \cos{\left(2 t \right)})\cdot (4)\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}64 \cos{\left(2 t \right)}\,\text{d}t \\ &=64\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}\cos 2t\,\text{d}t \\ &=(64)\left[\frac{1}{2}\sin 2t\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left[(32 \sin{\left(2 t \right)})\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left((32 \sin{\left(2 (- \frac{\pi}{4}) \right)})\right)-\left((32 \sin{\left(2 (- \frac{\pi}{2}) \right)})\right) \\ &=\left((-32)\right)-\left((0)\right) \\ &=-32.\end{aligned}
$$

## GENERATED / observed family workload circle_cos / method_circle_cos

Evaluate the line integral of the function $f(x,y)=75 - 6 x^{2}$ along the curve $C$ parametrized by $r(t)=⟨5 \cos{\left(t \right)},\,5 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{4},0].$

1. $- \frac{1875}{2}$
2. $-375$
3. $- \frac{375 \pi}{4} - \frac{375}{2}$
4. $- \frac{375}{2}$
5. $- \frac{75}{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨5 \cos{\left(t \right)},\,5 \sin{\left(t \right)}⟩,$ then along the curve we have $x=5 \cos{\left(t \right)}$ and $y=5 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(5 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(5 \sin{\left(t \right)})j \\ &=(- 5 \sin{\left(t \right)})i+(5 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 5 \sin{\left(t \right)})^2+(5 \cos{\left(t \right)})^2} \\ &=\sqrt{25\sin^2t+25\cos^2t} \\ &=\sqrt{25(\sin^2t+\cos^2t)} \\ &=\sqrt{25} \\ &=5\end{aligned}
$$

Now, if $f(x,y)=75 - 6 x^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)\left(2(5 \cos{\left(t \right)})^2-25\right) \\ &=(-75)(2\cos^2t-1) \\ &=- 75 \cos{\left(2 t \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 75 - 6 x^{2}\,\text{d}s&=\int_{- \frac{\pi}{4}}^{0}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}(- 75 \cos{\left(2 t \right)})\cdot (5)\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}- 375 \cos{\left(2 t \right)}\,\text{d}t \\ &=-375\int_{- \frac{\pi}{4}}^{0}\cos 2t\,\text{d}t \\ &=(-375)\left[\frac{1}{2}\sin 2t\right]_{- \frac{\pi}{4}}^{0} \\ &=\left[(- \frac{375 \sin{\left(2 t \right)}}{2})\right]_{- \frac{\pi}{4}}^{0} \\ &=\left((- \frac{375 \sin{\left(2 (0) \right)}}{2})\right)-\left((- \frac{375 \sin{\left(2 (- \frac{\pi}{4}) \right)}}{2})\right) \\ &=\left((0)\right)-\left((\frac{375}{2})\right) \\ &=- \frac{375}{2}.\end{aligned}
$$

## GENERATED / observed family workload circle_sin / method_circle_sin

Evaluate the line integral of the function $f(x,y)=y^{2}$ along the curve $C$ parametrized by $r(t)=⟨4 \cos{\left(t \right)},\,4 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{2},- \frac{\pi}{4}].$

1. $64 + 32 \pi$
2. $4 + 2 \pi$
3. $16 + 8 \pi$
4. $8 \pi + 32$
5. $-16 + 8 \pi$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨4 \cos{\left(t \right)},\,4 \sin{\left(t \right)}⟩,$ then along the curve we have $x=4 \cos{\left(t \right)}$ and $y=4 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(4 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(4 \sin{\left(t \right)})j \\ &=(- 4 \sin{\left(t \right)})i+(4 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 4 \sin{\left(t \right)})^2+(4 \cos{\left(t \right)})^2} \\ &=\sqrt{16\sin^2t+16\cos^2t} \\ &=\sqrt{16(\sin^2t+\cos^2t)} \\ &=\sqrt{16} \\ &=4\end{aligned}
$$

Now, if $f(x,y)=y^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(1)(4 \sin{\left(t \right)})^2 \\ &=16\sin^2t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C y^{2}\,\text{d}s&=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}(16 \sin^{2}{\left(t \right)})\cdot (4)\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}64 \sin^{2}{\left(t \right)}\,\text{d}t \\ &=64\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}\sin^2t\,\text{d}t \\ &=64\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}\frac{1-\cos 2t}{2}\,\text{d}t \\ &=32\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}1-\cos 2t\,\text{d}t \\ &=(32)\left[t-\frac{\sin 2t}{2}\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left[(32 t)+(- 16 \sin{\left(2 t \right)})\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left((32 (- \frac{\pi}{4}))+(- 16 \sin{\left(2 (- \frac{\pi}{4}) \right)})\right)-\left((32 (- \frac{\pi}{2}))+(- 16 \sin{\left(2 (- \frac{\pi}{2}) \right)})\right) \\ &=\left((- 8 \pi)+(16)\right)-\left((- 16 \pi)+(0)\right) \\ &=16 + 8 \pi.\end{aligned}
$$

## GENERATED / observed family workload circle_sin / method_circle_sin

Evaluate the line integral of the function $f(x,y)=- 3 y^{2}$ along the curve $C$ parametrized by $r(t)=⟨5 \cos{\left(t \right)},\,5 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{4},0].$

1. $\frac{1875}{4} - \frac{1875 \pi}{8}$
2. $- \frac{375 \pi}{8} - \frac{375}{4}$
3. $\frac{375}{2} - \frac{375 \pi}{8}$
4. $\frac{375}{4} - \frac{375 \pi}{8}$
5. $\frac{75}{4} - \frac{75 \pi}{8}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨5 \cos{\left(t \right)},\,5 \sin{\left(t \right)}⟩,$ then along the curve we have $x=5 \cos{\left(t \right)}$ and $y=5 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(5 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(5 \sin{\left(t \right)})j \\ &=(- 5 \sin{\left(t \right)})i+(5 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 5 \sin{\left(t \right)})^2+(5 \cos{\left(t \right)})^2} \\ &=\sqrt{25\sin^2t+25\cos^2t} \\ &=\sqrt{25(\sin^2t+\cos^2t)} \\ &=\sqrt{25} \\ &=5\end{aligned}
$$

Now, if $f(x,y)=- 3 y^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)(5 \sin{\left(t \right)})^2 \\ &=-75\sin^2t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 y^{2}\,\text{d}s&=\int_{- \frac{\pi}{4}}^{0}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}(- 75 \sin^{2}{\left(t \right)})\cdot (5)\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}- 375 \sin^{2}{\left(t \right)}\,\text{d}t \\ &=-375\int_{- \frac{\pi}{4}}^{0}\sin^2t\,\text{d}t \\ &=-375\int_{- \frac{\pi}{4}}^{0}\frac{1-\cos 2t}{2}\,\text{d}t \\ &=- \frac{375}{2}\int_{- \frac{\pi}{4}}^{0}1-\cos 2t\,\text{d}t \\ &=(- \frac{375}{2})\left[t-\frac{\sin 2t}{2}\right]_{- \frac{\pi}{4}}^{0} \\ &=\left[(- \frac{375 t}{2})+(\frac{375 \sin{\left(2 t \right)}}{4})\right]_{- \frac{\pi}{4}}^{0} \\ &=\left((- \frac{375 (0)}{2})+(\frac{375 \sin{\left(2 (0) \right)}}{4})\right)-\left((- \frac{375 (- \frac{\pi}{4})}{2})+(\frac{375 \sin{\left(2 (- \frac{\pi}{4}) \right)}}{4})\right) \\ &=\left((0)+(0)\right)-\left((\frac{375 \pi}{8})+(- \frac{375}{4})\right) \\ &=\frac{375}{4} - \frac{375 \pi}{8}.\end{aligned}
$$

## GENERATED / observed family workload cubic / method_cubic

Evaluate the line integral of the function $f(x,y)=- x^{3} + 3 y^{3}$ along the curve $C$ parametrized by $r(t)=⟨3 t^{2},\,- 4 t^{2}⟩$ for $t\in [0,1].$

1. $- \frac{7300}{3}$
2. $- \frac{219}{7}$
3. $- \frac{1095}{4}$
4. $\frac{825}{4}$
5. $- \frac{455}{4}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 t^{2},\,- 4 t^{2}⟩,$ then along the curve we have $x=3 t^{2}$ and $y=- 4 t^{2}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 t^{2})i+\frac{\text{d}}{\text{d}t}(- 4 t^{2})j \\ &=(6 t)i+(- 8 t)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(6 t)^2+(- 8 t)^2} \\ &=\sqrt{36t^2+64t^2} \\ &=\sqrt{100t^2} \\ &=10|t| \\ &=10 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- x^{3} + 3 y^{3}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-1)\left((3 t^{2})^3-(3)(- 4 t^{2})^3\right) \\ &=(-1)\left((3)^3t^6-(3)(-4)^3t^6\right) \\ &=(-1)\left(27t^6-(-192)t^6\right) \\ &=- 219 t^{6}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - x^{3} + 3 y^{3}\,\text{d}s&=\int_{0}^{1}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{1}(- 219 t^{6})\cdot (10 t)\,\text{d}t \\ &=\int_{0}^{1}- 2190 t^{7}\,\text{d}t \\ &=-2190\int_{0}^{1}t^7\,\text{d}t \\ &=(-2190)\left[\frac{t^8}{8}\right]_{0}^{1} \\ &=\left[(- \frac{1095 t^{8}}{4})\right]_{0}^{1} \\ &=\left((- \frac{1095 (1)^{8}}{4})\right)-\left((- \frac{1095 (0)^{8}}{4})\right) \\ &=\left((- \frac{1095}{4})\right)-\left((0)\right) \\ &=- \frac{1095}{4}.\end{aligned}
$$

## GENERATED / observed family workload cubic / method_cubic

Evaluate the line integral of the function $f(x,y)=- 3 x^{3} + 6 y^{3}$ along the curve $C$ parametrized by $r(t)=⟨- 4 t^{2},\,3 t^{2}⟩$ for $t\in [0,1].$

1. $\frac{11800}{3}$
2. $\frac{1365}{4}$
3. $\frac{75}{2}$
4. $\frac{885}{2}$
5. $\frac{354}{7}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨- 4 t^{2},\,3 t^{2}⟩,$ then along the curve we have $x=- 4 t^{2}$ and $y=3 t^{2}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(- 4 t^{2})i+\frac{\text{d}}{\text{d}t}(3 t^{2})j \\ &=(- 8 t)i+(6 t)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 8 t)^2+(6 t)^2} \\ &=\sqrt{64t^2+36t^2} \\ &=\sqrt{100t^2} \\ &=10|t| \\ &=10 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x^{3} + 6 y^{3}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)\left((- 4 t^{2})^3-(2)(3 t^{2})^3\right) \\ &=(-3)\left((-4)^3t^6-(2)(3)^3t^6\right) \\ &=(-3)\left(-64t^6-(54)t^6\right) \\ &=354 t^{6}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x^{3} + 6 y^{3}\,\text{d}s&=\int_{0}^{1}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{1}(354 t^{6})\cdot (10 t)\,\text{d}t \\ &=\int_{0}^{1}3540 t^{7}\,\text{d}t \\ &=3540\int_{0}^{1}t^7\,\text{d}t \\ &=(3540)\left[\frac{t^8}{8}\right]_{0}^{1} \\ &=\left[(\frac{885 t^{8}}{2})\right]_{0}^{1} \\ &=\left((\frac{885 (1)^{8}}{2})\right)-\left((\frac{885 (0)^{8}}{2})\right) \\ &=\left((\frac{885}{2})\right)-\left((0)\right) \\ &=\frac{885}{2}.\end{aligned}
$$

## GENERATED / authored level policy fractional / method_fractional

Evaluate the line integral of the function $f(x,y)=- 3 x$ along the curve $C$ parametrized by $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩$ for $t\in [1,3].$

1. $\frac{96256}{315} - \frac{331776 \sqrt{3}}{35}$
2. $\frac{32}{5} - \frac{288 \sqrt{3}}{5}$
3. $\frac{1536}{35} - \frac{25344 \sqrt{3}}{35}$
4. $\frac{1024}{15} - \frac{5376 \sqrt{3}}{5}$
5. $\frac{128}{7} - \frac{3456 \sqrt{3}}{7}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩,$ then along the curve we have $x=\frac{16 t^{\frac{3}{2}}}{3}$ and $y=2 t^{2} - 4 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{16 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(2 t^{2} - 4 t)j \\ &=(8 \sqrt{t})i+(4 t - 4)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(8 \sqrt{t})^2+(4 t - 4)^2} \\ &=\sqrt{64t+16(t-1)^2} \\ &=\sqrt{16(t^2+2t+1)} \\ &=4|t+1| \\ &=4 t + 4\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)(\frac{16 t^{\frac{3}{2}}}{3}) \\ &=- 16 t^{\frac{3}{2}}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x\,\text{d}s&=\int_{1}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{3}(- 16 t^{\frac{3}{2}})\cdot (4 t + 4)\,\text{d}t \\ &=\int_{1}^{3}-64t^{3/2}(t+1)\,\text{d}t \\ &=\int_{1}^{3}- 64 t^{\frac{5}{2}} - 64 t^{\frac{3}{2}}\,\text{d}t \\ &=\left[(- \frac{128 t^{\frac{7}{2}}}{7})+(- \frac{128 t^{\frac{5}{2}}}{5})\right]_{1}^{3} \\ &=\left((- \frac{128 (3)^{\frac{7}{2}}}{7})+(- \frac{128 (3)^{\frac{5}{2}}}{5})\right)-\left((- \frac{128 (1)^{\frac{7}{2}}}{7})+(- \frac{128 (1)^{\frac{5}{2}}}{5})\right) \\ &=\left((- \frac{3456 \sqrt{3}}{7})+(- \frac{1152 \sqrt{3}}{5})\right)-\left((- \frac{128}{7})+(- \frac{128}{5})\right) \\ &=\frac{1536}{35} - \frac{25344 \sqrt{3}}{35}.\end{aligned}
$$

## GENERATED / authored level policy fractional / method_fractional

Evaluate the line integral of the function $f(x,y)=- 3 x$ along the curve $C$ parametrized by $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩$ for $t\in [0,2].$

1. $- \frac{306400 \sqrt{2}}{63}$
2. $- \frac{1600 \sqrt{2}}{7}$
3. $- \frac{1760 \sqrt{2}}{3}$
4. $- \frac{2720 \sqrt{2}}{7}$
5. $- 32 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩,$ then along the curve we have $x=\frac{20 t^{\frac{3}{2}}}{3}$ and $y=\frac{5 t^{2}}{2} - 5 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{20 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(\frac{5 t^{2}}{2} - 5 t)j \\ &=(10 \sqrt{t})i+(5 t - 5)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(10 \sqrt{t})^2+(5 t - 5)^2} \\ &=\sqrt{100t+25(t-1)^2} \\ &=\sqrt{25(t^2+2t+1)} \\ &=5|t+1| \\ &=5 t + 5\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)(\frac{20 t^{\frac{3}{2}}}{3}) \\ &=- 20 t^{\frac{3}{2}}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x\,\text{d}s&=\int_{0}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{2}(- 20 t^{\frac{3}{2}})\cdot (5 t + 5)\,\text{d}t \\ &=\int_{0}^{2}-100t^{3/2}(t+1)\,\text{d}t \\ &=\int_{0}^{2}- 100 t^{\frac{5}{2}} - 100 t^{\frac{3}{2}}\,\text{d}t \\ &=\left[(- \frac{200 t^{\frac{7}{2}}}{7})+(- 40 t^{\frac{5}{2}})\right]_{0}^{2} \\ &=\left((- \frac{200 (2)^{\frac{7}{2}}}{7})+(- 40 (2)^{\frac{5}{2}})\right)-\left((- \frac{200 (0)^{\frac{7}{2}}}{7})+(- 40 (0)^{\frac{5}{2}})\right) \\ &=\left((- \frac{1600 \sqrt{2}}{7})+(- 160 \sqrt{2})\right)-\left((0)+(0)\right) \\ &=- \frac{2720 \sqrt{2}}{7}.\end{aligned}
$$

## GENERATED / authored level policy involute / method_involute

Evaluate the line integral of the function $f(x,y)=- 3 x^{2} - 3 y^{2} - 1$ along the curve $C$ parametrized by $r(t)=⟨4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)},\,- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}⟩$ for $t\in [\frac{\pi}{2},\pi].$

1. $\frac{2 \pi^{3} \left(- 1116 \pi^{2} - 1715\right)}{15}$
2. $- 14 \pi^{3} - \frac{49 \pi}{2}$
3. $\pi^{2} \left(- 45 \pi^{2} - \frac{147}{2}\right)$
4. $- \frac{147 \pi^{2}}{2}$
5. $\pi^{2} \left(- 45 \pi^{2} - 72\right)$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)},\,- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}⟩,$ then along the curve we have $x=4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)}$ and $y=- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)})j \\ &=(4)(-\sin t+\sin t+t\cos t)i+(4)(\cos t-\cos t+t\sin t)j \\ &=(4 t \cos{\left(t \right)})i+(4 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(4 t \cos{\left(t \right)})^2+(4 t \sin{\left(t \right)})^2} \\ &=\sqrt{16t^2(\cos^2t+\sin^2t)} \\ &=4|t| \\ &=4 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x^{2} - 3 y^{2} - 1$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)\left((4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)})^2+(- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)})^2\right)+(-1) \\ &=(-48)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(-1) \\ &=(-48)(1+t^2)+(-1) \\ &=- 48 t^{2} - 49\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x^{2} - 3 y^{2} - 1\,\text{d}s&=\int_{\frac{\pi}{2}}^{\pi}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{\frac{\pi}{2}}^{\pi}(- 48 t^{2} - 49)\cdot (4 t)\,\text{d}t \\ &=\int_{\frac{\pi}{2}}^{\pi}- 192 t^{3} - 196 t\,\text{d}t \\ &=\left[(- 98 t^{2})+(- 48 t^{4})\right]_{\frac{\pi}{2}}^{\pi} \\ &=\left((- 98 (\pi)^{2})+(- 48 (\pi)^{4})\right)-\left((- 98 (\frac{\pi}{2})^{2})+(- 48 (\frac{\pi}{2})^{4})\right) \\ &=\left((- 98 \pi^{2})+(- 48 \pi^{4})\right)-\left((- \frac{49 \pi^{2}}{2})+(- 3 \pi^{4})\right) \\ &=\pi^{2} \left(- 45 \pi^{2} - \frac{147}{2}\right).\end{aligned}
$$

## GENERATED / authored level policy involute / method_involute

Evaluate the line integral of the function $f(x,y)=- 3 x^{2} - 3 y^{2} - 1$ along the curve $C$ parametrized by $r(t)=⟨5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)},\,- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}⟩$ for $t\in [1,2].$

1. $- \frac{48175}{3}$
2. $- \frac{7875}{4}$
3. $-570$
4. $- \frac{7905}{4}$
5. $-251$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)},\,- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}⟩,$ then along the curve we have $x=5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)}$ and $y=- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)})j \\ &=(5)(-\sin t+\sin t+t\cos t)i+(5)(\cos t-\cos t+t\sin t)j \\ &=(5 t \cos{\left(t \right)})i+(5 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(5 t \cos{\left(t \right)})^2+(5 t \sin{\left(t \right)})^2} \\ &=\sqrt{25t^2(\cos^2t+\sin^2t)} \\ &=5|t| \\ &=5 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x^{2} - 3 y^{2} - 1$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)\left((5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)})^2+(- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)})^2\right)+(-1) \\ &=(-75)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(-1) \\ &=(-75)(1+t^2)+(-1) \\ &=- 75 t^{2} - 76\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x^{2} - 3 y^{2} - 1\,\text{d}s&=\int_{1}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{2}(- 75 t^{2} - 76)\cdot (5 t)\,\text{d}t \\ &=\int_{1}^{2}- 375 t^{3} - 380 t\,\text{d}t \\ &=\left[(- 190 t^{2})+(- \frac{375 t^{4}}{4})\right]_{1}^{2} \\ &=\left((- 190 (2)^{2})+(- \frac{375 (2)^{4}}{4})\right)-\left((- 190 (1)^{2})+(- \frac{375 (1)^{4}}{4})\right) \\ &=\left((-760)+(-1500)\right)-\left((-190)+(- \frac{375}{4})\right) \\ &=- \frac{7905}{4}.\end{aligned}
$$

## GENERATED / authored level policy mixed_fractional / method_mixed_fractional

Evaluate the line integral of the function $f(x,y)=- 3 x - y$ along the curve $C$ parametrized by $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩$ for $t\in [1,3].$

1. $- \frac{331776 \sqrt{3}}{35} - \frac{48896}{315}$
2. $\frac{76}{15} - \frac{288 \sqrt{3}}{5}$
3. $\frac{1808}{105} - \frac{25344 \sqrt{3}}{35}$
4. $- \frac{80}{3}$
5. $\frac{1536}{35} - \frac{25344 \sqrt{3}}{35}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩,$ then along the curve we have $x=\frac{16 t^{\frac{3}{2}}}{3}$ and $y=2 t^{2} - 4 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{16 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(2 t^{2} - 4 t)j \\ &=(8 \sqrt{t})i+(4 t - 4)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(8 \sqrt{t})^2+(4 t - 4)^2} \\ &=\sqrt{64t+16(t-1)^2} \\ &=\sqrt{16(t^2+2t+1)} \\ &=4|t+1| \\ &=4 t + 4\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x - y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)(\frac{16 t^{\frac{3}{2}}}{3})+(-1)(2 t^{2} - 4 t) \\ &=- 16 t^{\frac{3}{2}} - 2 t^{2} + 4 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x - y\,\text{d}s&=\int_{1}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{3}(- 16 t^{\frac{3}{2}} - 2 t^{2} + 4 t)\cdot (4 t + 4)\,\text{d}t \\ &=\int_{1}^{3}-64t^{3/2}(t+1)+(-16)(t^2/2-t)(t+1)\,\text{d}t \\ &=\int_{1}^{3}- 64 t^{\frac{5}{2}} - 64 t^{\frac{3}{2}} - 8 t^{3} + 8 t^{2} + 16 t\,\text{d}t \\ &=\left[(- \frac{128 t^{\frac{7}{2}}}{7})+(- \frac{128 t^{\frac{5}{2}}}{5})+(- 2 t^{4})+(\frac{8 t^{3}}{3})+(8 t^{2})\right]_{1}^{3} \\ &=\left((- \frac{128 (3)^{\frac{7}{2}}}{7})+(- \frac{128 (3)^{\frac{5}{2}}}{5})+(- 2 (3)^{4})+(\frac{8 (3)^{3}}{3})+(8 (3)^{2})\right)-\left((- \frac{128 (1)^{\frac{7}{2}}}{7})+(- \frac{128 (1)^{\frac{5}{2}}}{5})+(- 2 (1)^{4})+(\frac{8 (1)^{3}}{3})+(8 (1)^{2})\right) \\ &=\left((- \frac{3456 \sqrt{3}}{7})+(- \frac{1152 \sqrt{3}}{5})+(-162)+(72)+(72)\right)-\left((- \frac{128}{7})+(- \frac{128}{5})+(-2)+(\frac{8}{3})+(8)\right) \\ &=\frac{1808}{105} - \frac{25344 \sqrt{3}}{35}.\end{aligned}
$$

## GENERATED / authored level policy mixed_fractional / method_mixed_fractional

Evaluate the line integral of the function $f(x,y)=- 3 x - y$ along the curve $C$ parametrized by $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩$ for $t\in [0,2].$

1. $350 - \frac{306400 \sqrt{2}}{63}$
2. $- \frac{2720 \sqrt{2}}{7}$
3. $\frac{100}{3}$
4. $\frac{100}{3} - \frac{2720 \sqrt{2}}{7}$
5. $\frac{10}{3} - 32 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩,$ then along the curve we have $x=\frac{20 t^{\frac{3}{2}}}{3}$ and $y=\frac{5 t^{2}}{2} - 5 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{20 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(\frac{5 t^{2}}{2} - 5 t)j \\ &=(10 \sqrt{t})i+(5 t - 5)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(10 \sqrt{t})^2+(5 t - 5)^2} \\ &=\sqrt{100t+25(t-1)^2} \\ &=\sqrt{25(t^2+2t+1)} \\ &=5|t+1| \\ &=5 t + 5\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 3 x - y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-3)(\frac{20 t^{\frac{3}{2}}}{3})+(-1)(\frac{5 t^{2}}{2} - 5 t) \\ &=- 20 t^{\frac{3}{2}} - \frac{5 t^{2}}{2} + 5 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 3 x - y\,\text{d}s&=\int_{0}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{2}(- 20 t^{\frac{3}{2}} - \frac{5 t^{2}}{2} + 5 t)\cdot (5 t + 5)\,\text{d}t \\ &=\int_{0}^{2}-100t^{3/2}(t+1)+(-25)(t^2/2-t)(t+1)\,\text{d}t \\ &=\int_{0}^{2}- 100 t^{\frac{5}{2}} - 100 t^{\frac{3}{2}} - \frac{25 t^{3}}{2} + \frac{25 t^{2}}{2} + 25 t\,\text{d}t \\ &=\left[(- \frac{200 t^{\frac{7}{2}}}{7})+(- 40 t^{\frac{5}{2}})+(- \frac{25 t^{4}}{8})+(\frac{25 t^{3}}{6})+(\frac{25 t^{2}}{2})\right]_{0}^{2} \\ &=\left((- \frac{200 (2)^{\frac{7}{2}}}{7})+(- 40 (2)^{\frac{5}{2}})+(- \frac{25 (2)^{4}}{8})+(\frac{25 (2)^{3}}{6})+(\frac{25 (2)^{2}}{2})\right)-\left((- \frac{200 (0)^{\frac{7}{2}}}{7})+(- 40 (0)^{\frac{5}{2}})+(- \frac{25 (0)^{4}}{8})+(\frac{25 (0)^{3}}{6})+(\frac{25 (0)^{2}}{2})\right) \\ &=\left((- \frac{1600 \sqrt{2}}{7})+(- 160 \sqrt{2})+(-50)+(\frac{100}{3})+(50)\right)-\left((0)+(0)+(0)+(0)+(0)\right) \\ &=\frac{100}{3} - \frac{2720 \sqrt{2}}{7}.\end{aligned}
$$
