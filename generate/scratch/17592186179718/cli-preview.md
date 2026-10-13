Generated variant / easy / line_power / method

Evaluate the line integral
${\int }_{C}6 y\,\text{d}s,$
where $C$ is the section of the curve $x=2 y + 2$ from $(4,1)$ to $(10,4).$

- $126 \sqrt{5}$
- $51 \sqrt{5}$
- $45 \sqrt{5}$ **CORRECT**
- $45$
- $48 \sqrt{5}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t + 2.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t + 2,\,t⟩,\,1\le t\le 4
$$

Note that the domain $1\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t + 2)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=6 y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =6 t \\  & =6 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}6 y\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}\left(6 t\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{4}6 \sqrt{5} t\,\text{d}t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{1}^{4}6 \sqrt{5} t\,\text{d}t & =\left[3 \sqrt{5} t^{2}\right]_{1}^{4} \\  & =6 \sqrt{5}\left(\frac{4^2}{2}-\frac{1^2}{2}\right) \\  & =6 \sqrt{5}\left(8-\frac{1}{2}\right) \\  & =45 \sqrt{5}\end{aligned}
$$


Generated variant / easy / line_power / method

Evaluate the line integral
${\int }_{C}8 y\,\text{d}s,$
where $C$ is the section of the curve $x=2 y + 1$ from $(3,1)$ to $(7,3).$

- $40 \sqrt{5}$
- $36 \sqrt{5}$
- $\frac{208 \sqrt{5}}{3}$
- $32$
- $32 \sqrt{5}$ **CORRECT**

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t + 1.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t + 1,\,t⟩,\,1\le t\le 3
$$

Note that the domain $1\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t + 1)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=8 y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =8 t \\  & =8 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}8 y\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}\left(8 t\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{3}8 \sqrt{5} t\,\text{d}t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{1}^{3}8 \sqrt{5} t\,\text{d}t & =\left[4 \sqrt{5} t^{2}\right]_{1}^{3} \\  & =8 \sqrt{5}\left(\frac{3^2}{2}-\frac{1^2}{2}\right) \\  & =8 \sqrt{5}\left(\frac{9}{2}-\frac{1}{2}\right) \\  & =32 \sqrt{5}\end{aligned}
$$


Generated variant / moderate / reciprocal / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/6cc0eeb9bd08cd9e32ed01fa.png)

Evaluate the line integral
${\int }_{C}6 x y^{6}\,\text{d}s,$
where $C$ is the section of the curve $x=\frac{2}{y}$ from $(2,1)$ to $(\frac{2}{3},3),$ as shown above.

- $10800$
- $10 \sqrt{5} + 170 \sqrt{85}$
- $170 \sqrt{85}$
- $- 10 \sqrt{5} + 170 \sqrt{85}$ **CORRECT**
- $1456$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\frac{2}{t}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\frac{2}{t},\,t⟩,\,1\le t\le 3
$$

Note that the domain $1\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{2}{t})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =- \frac{2}{t^{2}}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(- \frac{2}{t^{2}})^2+1^2} \\  & =\sqrt{\frac{4}{t^{4}}+1} \\  & =\sqrt{1 + \frac{4}{t^{4}}}\end{aligned}
$$

 

Now, if  $f(x,y)=6 x y^{6},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =6 \left(\frac{2}{t}\right) t^{6} \\  & =12 t^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}6 x y^{6}\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}\left(12 t^{5}\right)\cdot\left(\sqrt{1 + \frac{4}{t^{4}}}\right)\,\text{d}t \\  & ={\int }_{1}^{3}12 t^{3} \sqrt{t^{4} + 4}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{4} + 4,$ $\text{d}u=4 t^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{3}12 t^{3} \sqrt{t^{4} + 4}\,\text{d}t & =12{\int }_{5}^{85}\sqrt{u}\cdot\left(\frac{1}{4}\right)\,\text{d}u \\  & ={\int }_{5}^{85}3 \sqrt{u}\,\text{d}u \\  & =\left[3\cdot\frac{2}{3}u^{3/2}\right]_{5}^{85} \\  & =\left[2 u^{\frac{3}{2}}\right]_{5}^{85} \\  & =\left(\left(2 \left(85\right)^{\frac{3}{2}}\right)\right)-\left(\left(2 \left(5\right)^{\frac{3}{2}}\right)\right) \\  & =\left(\left(170 \sqrt{85}\right)\right)-\left(\left(10 \sqrt{5}\right)\right) \\  & =- 10 \sqrt{5} + 170 \sqrt{85}\end{aligned}
$$


Generated variant / moderate / line_log / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/0eabca4a191e201a9c26a2a0.png)

Evaluate the line integral
${\int }_{C}\frac{8}{- x + y}\,\text{d}s,$
where $C$ is the section of the curve $x=2 y - 5$ from $(-3,1)$ to $(-1,2),$ as shown above.

- $8 \sqrt{5} \ln{\left(4 \right)}$
- $40 \ln{\left(\frac{4}{3} \right)}$
- $8 \sqrt{5}$
- $8 \sqrt{5} \ln{\left(\frac{4}{3} \right)}$ **CORRECT**
- $8 \ln{\left(\frac{4}{3} \right)}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t - 5.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t - 5,\,t⟩,\,1\le t\le 2
$$

Note that the domain $1\le t\le 2$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t - 5)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{8}{- x + y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{8}{- \left(2 t - 5\right) + t} \\  & =- \frac{8}{t - 5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{8}{- x + y}\,\text{d}s & ={\int }_{1}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2}\left(- \frac{8}{t - 5}\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{2}- \frac{8 \sqrt{5}}{t - 5}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=5 - t,$ $\text{d}u=-1\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{2}- \frac{8 \sqrt{5}}{t - 5}\,\text{d}t & =8 \sqrt{5}{\int }_{4}^{3}\frac{1}{u}\cdot(-1)\,\text{d}u \\  & ={\int }_{4}^{3}- \frac{8 \sqrt{5}}{u}\,\text{d}u \\  & =\left[-(8 \sqrt{5})\cdot\ln{u}\right]_{4}^{3} \\  & =\left[- 8 \sqrt{5} \ln{\left(u \right)}\right]_{4}^{3} \\  & =\left(\left(- 8 \sqrt{5} \ln{\left(\left(3\right) \right)}\right)\right)-\left(\left(- 8 \sqrt{5} \ln{\left(\left(4\right) \right)}\right)\right) \\  & =\left(\left(- 8 \sqrt{5} \ln{\left(3 \right)}\right)\right)-\left(\left(- 16 \sqrt{5} \ln{\left(2 \right)}\right)\right) \\  & =8 \sqrt{5} \ln{\left(\frac{4}{3} \right)}\end{aligned}
$$


Generated variant / hard / implicit_parabola / method

Evaluate the line integral
${\int }_{C}\frac{6 x}{y}\,\text{d}s,$
where $C$ is the section of the curve $y^2=6x$ from $(\frac{8}{3},4)$ to $(\frac{9}{2},3 \sqrt{3}).$

- $\frac{341}{9}$
- $\frac{11}{2}$
- $24$
- $\frac{671}{12}$
- $\frac{91}{9}$ **CORRECT**

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
y^2=6x\,⟹\,x=\frac{y^{2}}{6}.
$$

Therefore, by setting $y=t,$ we have

$$
x=x(t)=\frac{t^{2}}{6}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\frac{t^{2}}{6},\,t⟩,\,4\le t\le 3 \sqrt{3}
$$

Note that the domain $4\le t\le 3 \sqrt{3}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{t^{2}}{6})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{t}{3}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{t}{3})^2+1^2} \\  & =\sqrt{\frac{t^{2}}{9}+1} \\  & =\sqrt{\frac{t^{2}}{9} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{6 x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{6 \left(\frac{t^{2}}{6}\right)}{t} \\  & =t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{6 x}{y}\,\text{d}s & ={\int }_{4}^{3 \sqrt{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{4}^{3 \sqrt{3}}\left(t\right)\cdot\left(\sqrt{\frac{t^{2}}{9} + 1}\right)\,\text{d}t \\  & ={\int }_{4}^{3 \sqrt{3}}\frac{t \sqrt{t^{2} + 9}}{3}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{2} + 9,$ $\text{d}u=2 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{4}^{3 \sqrt{3}}\frac{t \sqrt{t^{2} + 9}}{3}\,\text{d}t & =\frac{1}{3}{\int }_{25}^{36}\sqrt{u}\cdot\left(\frac{1}{2}\right)\,\text{d}u \\  & ={\int }_{25}^{36}\frac{\sqrt{u}}{6}\,\text{d}u \\  & =\left[\frac{1}{6}\cdot\frac{2}{3}u^{3/2}\right]_{25}^{36} \\  & =\left[\frac{u^{\frac{3}{2}}}{9}\right]_{25}^{36} \\  & =\left(\left(\frac{\left(36\right)^{\frac{3}{2}}}{9}\right)\right)-\left(\left(\frac{\left(25\right)^{\frac{3}{2}}}{9}\right)\right) \\  & =\left(\left(24\right)\right)-\left(\left(\frac{125}{9}\right)\right) \\  & =\frac{91}{9}\end{aligned}
$$


Generated variant / hard / sqrt / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/9897043e0fa84d0f7b41a5e4.png)

Evaluate the line integral
${\int }_{C}6 x y\,\text{d}s,$
where $C$ is the section of the curve $x=\sqrt{y}$ from $(1,1)$ to $(\sqrt{5},5),$ as shown above.

- $532$
- $\frac{5 \sqrt{5}}{4} + \frac{609 \sqrt{21}}{20}$
- $\frac{609 \sqrt{21}}{20}$
- $- \frac{5 \sqrt{5}}{4} + \frac{609 \sqrt{21}}{20}$ **CORRECT**
- $- \frac{12}{5} + 60 \sqrt{5}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\sqrt{t}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\sqrt{t},\,t⟩,\,1\le t\le 5
$$

Note that the domain $1\le t\le 5$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sqrt{t})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{2 \sqrt{t}}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{1}{2 \sqrt{t}})^2+1^2} \\  & =\sqrt{\frac{1}{4 t}+1} \\  & =\sqrt{1 + \frac{1}{4 t}}\end{aligned}
$$

 

Now, if  $f(x,y)=6 x y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =6 \left(\sqrt{t}\right) t \\  & =6 t^{\frac{3}{2}}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}6 x y\,\text{d}s & ={\int }_{1}^{5}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{5}\left(6 t^{\frac{3}{2}}\right)\cdot\left(\sqrt{1 + \frac{1}{4 t}}\right)\,\text{d}t \\  & ={\int }_{1}^{5}3 t \sqrt{4 t + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 t + 1,$ $\text{d}u=4\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{5}3 t \sqrt{4 t + 1}\,\text{d}t & =3{\int }_{5}^{21}\frac{u-1}{4}\cdot\sqrt{u}\cdot\frac{1}{4}\,\text{d}u \\  & ={\int }_{5}^{21}\frac{3 u^{\frac{3}{2}}}{16} - \frac{3 \sqrt{u}}{16}\,\text{d}u \\  & =\left[\frac{3}{16}\cdot\left(\frac{2}{5}u^{5/2}-(1)\cdot\frac{2}{3}u^{3/2}\right)\right]_{5}^{21} \\  & =\left[\frac{3 u^{\frac{5}{2}}}{40} - \frac{u^{\frac{3}{2}}}{8}\right]_{5}^{21} \\  & =\left(\left(\frac{3 \left(21\right)^{\frac{5}{2}}}{40}\right)+\left(- \frac{\left(21\right)^{\frac{3}{2}}}{8}\right)\right)-\left(\left(\frac{3 \left(5\right)^{\frac{5}{2}}}{40}\right)+\left(- \frac{\left(5\right)^{\frac{3}{2}}}{8}\right)\right) \\  & =\left(\left(\frac{1323 \sqrt{21}}{40}\right)+\left(- \frac{21 \sqrt{21}}{8}\right)\right)-\left(\left(\frac{15 \sqrt{5}}{8}\right)+\left(- \frac{5 \sqrt{5}}{8}\right)\right) \\  & =- \frac{5 \sqrt{5}}{4} + \frac{609 \sqrt{21}}{20}\end{aligned}
$$

