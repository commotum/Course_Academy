Generated variant / easy / line_power / method

Evaluate the line integral
${\int }_{C}10 y\,\text{d}s,$
where $C$ is the section of the curve $x=2 y + 2$ from $(6,2)$ to $(8,3).$

- $25 \sqrt{5}$ **CORRECT**
- $65 \sqrt{5}$
- $25$
- $45 \sqrt{5}$
- $\frac{190 \sqrt{5}}{3}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t + 2.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t + 2,\,t⟩,\,2\le t\le 3
$$

Note that the domain $2\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t + 2)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=10 y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =10 t \\  & =10 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}10 y\,\text{d}s & ={\int }_{2}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{2}^{3}\left(10 t\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{2}^{3}10 \sqrt{5} t\,\text{d}t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{2}^{3}10 \sqrt{5} t\,\text{d}t & =\left[5 \sqrt{5} t^{2}\right]_{2}^{3} \\  & =10 \sqrt{5}\left(\frac{3^2}{2}-\frac{2^2}{2}\right) \\  & =10 \sqrt{5}\left(\frac{9}{2}-2\right) \\  & =25 \sqrt{5}\end{aligned}
$$


---

Generated variant / easy / line_power / method

Evaluate the line integral
${\int }_{C}3 y\,\text{d}s,$
where $C$ is the section of the curve $x=2 y + 1$ from $(3,1)$ to $(7,3).$

- $12 \sqrt{5}$ **CORRECT**
- $15 \sqrt{5}$
- $12$
- $26 \sqrt{5}$
- $\frac{27 \sqrt{5}}{2}$

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

 

Now, if  $f(x,y)=3 y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =3 t \\  & =3 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}3 y\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}\left(3 t\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{3}3 \sqrt{5} t\,\text{d}t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{1}^{3}3 \sqrt{5} t\,\text{d}t & =\left[\frac{3 \sqrt{5} t^{2}}{2}\right]_{1}^{3} \\  & =3 \sqrt{5}\left(\frac{3^2}{2}-\frac{1^2}{2}\right) \\  & =3 \sqrt{5}\left(\frac{9}{2}-\frac{1}{2}\right) \\  & =12 \sqrt{5}\end{aligned}
$$


---

Generated variant / moderate / parabola / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/581fd6dc14e26e58149221a5.png)

Evaluate the line integral
${\int }_{C}\frac{10 x}{y}\,\text{d}s,$
where $C$ is the section of the curve $x=y^{2}$ from $(1,1)$ to $(12,2 \sqrt{3}),$ as shown above.

- $\frac{1715}{6} - \frac{25 \sqrt{5}}{6}$ **CORRECT**
- $\frac{25 \sqrt{5}}{6} + \frac{1715}{6}$
- $55$
- $\frac{1715}{6}$
- $1485$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=t^{2}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨t^{2},\,t⟩,\,1\le t\le 2 \sqrt{3}
$$

Note that the domain $1\le t\le 2 \sqrt{3}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2 t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2 t)^2+1^2} \\  & =\sqrt{4 t^{2}+1} \\  & =\sqrt{4 t^{2} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{10 x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{10 \left(t^{2}\right)}{t} \\  & =10 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{10 x}{y}\,\text{d}s & ={\int }_{1}^{2 \sqrt{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2 \sqrt{3}}\left(10 t\right)\cdot\left(\sqrt{4 t^{2} + 1}\right)\,\text{d}t \\  & ={\int }_{1}^{2 \sqrt{3}}10 t \sqrt{4 t^{2} + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 t^{2} + 1,$ $\text{d}u=8 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{2 \sqrt{3}}10 t \sqrt{4 t^{2} + 1}\,\text{d}t & =10{\int }_{5}^{49}\sqrt{u}\cdot\left(\frac{1}{8}\right)\,\text{d}u \\  & ={\int }_{5}^{49}\frac{5 \sqrt{u}}{4}\,\text{d}u \\  & =\left[\frac{5}{4}\cdot\frac{2}{3}u^{3/2}\right]_{5}^{49} \\  & =\left[\frac{5 u^{\frac{3}{2}}}{6}\right]_{5}^{49} \\  & =\left(\left(\frac{5 \left(49\right)^{\frac{3}{2}}}{6}\right)\right)-\left(\left(\frac{5 \left(5\right)^{\frac{3}{2}}}{6}\right)\right) \\  & =\left(\left(\frac{1715}{6}\right)\right)-\left(\left(\frac{25 \sqrt{5}}{6}\right)\right) \\  & =\frac{1715}{6} - \frac{25 \sqrt{5}}{6}\end{aligned}
$$


---

Generated variant / moderate / parabola / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/c3a72ade884754438d19a146.png)

Evaluate the line integral
${\int }_{C}\frac{3 x}{y}\,\text{d}s,$
where $C$ is the section of the curve $x=y^{2}$ from $(1,1)$ to $(2,\sqrt{2}),$ as shown above.

- $\frac{27}{4} - \frac{5 \sqrt{5}}{4}$ **CORRECT**
- $\frac{5 \sqrt{5}}{4} + \frac{27}{4}$
- $\frac{3}{2}$
- $\frac{21}{2}$
- $\frac{27}{4}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=t^{2}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨t^{2},\,t⟩,\,1\le t\le \sqrt{2}
$$

Note that the domain $1\le t\le \sqrt{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2 t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2 t)^2+1^2} \\  & =\sqrt{4 t^{2}+1} \\  & =\sqrt{4 t^{2} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{3 x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{3 \left(t^{2}\right)}{t} \\  & =3 t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{3 x}{y}\,\text{d}s & ={\int }_{1}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{2}}\left(3 t\right)\cdot\left(\sqrt{4 t^{2} + 1}\right)\,\text{d}t \\  & ={\int }_{1}^{\sqrt{2}}3 t \sqrt{4 t^{2} + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 t^{2} + 1,$ $\text{d}u=8 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{\sqrt{2}}3 t \sqrt{4 t^{2} + 1}\,\text{d}t & =3{\int }_{5}^{9}\sqrt{u}\cdot\left(\frac{1}{8}\right)\,\text{d}u \\  & ={\int }_{5}^{9}\frac{3 \sqrt{u}}{8}\,\text{d}u \\  & =\left[\frac{3}{8}\cdot\frac{2}{3}u^{3/2}\right]_{5}^{9} \\  & =\left[\frac{u^{\frac{3}{2}}}{4}\right]_{5}^{9} \\  & =\left(\left(\frac{\left(9\right)^{\frac{3}{2}}}{4}\right)\right)-\left(\left(\frac{\left(5\right)^{\frac{3}{2}}}{4}\right)\right) \\  & =\left(\left(\frac{27}{4}\right)\right)-\left(\left(\frac{5 \sqrt{5}}{4}\right)\right) \\  & =\frac{27}{4} - \frac{5 \sqrt{5}}{4}\end{aligned}
$$


---

Generated variant / moderate / reciprocal / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/6cc0eeb9bd08cd9e32ed01fa.png)

Evaluate the line integral
${\int }_{C}10 x y^{6}\,\text{d}s,$
where $C$ is the section of the curve $x=\frac{2}{y}$ from $(2,1)$ to $(\frac{2}{3},3),$ as shown above.

- $- \frac{50 \sqrt{5}}{3} + \frac{850 \sqrt{85}}{3}$ **CORRECT**
- $18000$
- $\frac{7280}{3}$
- $\frac{50 \sqrt{5}}{3} + \frac{850 \sqrt{85}}{3}$
- $\frac{850 \sqrt{85}}{3}$

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

 

Now, if  $f(x,y)=10 x y^{6},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =10 \left(\frac{2}{t}\right) t^{6} \\  & =20 t^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}10 x y^{6}\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}\left(20 t^{5}\right)\cdot\left(\sqrt{1 + \frac{4}{t^{4}}}\right)\,\text{d}t \\  & ={\int }_{1}^{3}20 t^{3} \sqrt{t^{4} + 4}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{4} + 4,$ $\text{d}u=4 t^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{3}20 t^{3} \sqrt{t^{4} + 4}\,\text{d}t & =20{\int }_{5}^{85}\sqrt{u}\cdot\left(\frac{1}{4}\right)\,\text{d}u \\  & ={\int }_{5}^{85}5 \sqrt{u}\,\text{d}u \\  & =\left[5\cdot\frac{2}{3}u^{3/2}\right]_{5}^{85} \\  & =\left[\frac{10 u^{\frac{3}{2}}}{3}\right]_{5}^{85} \\  & =\left(\left(\frac{10 \left(85\right)^{\frac{3}{2}}}{3}\right)\right)-\left(\left(\frac{10 \left(5\right)^{\frac{3}{2}}}{3}\right)\right) \\  & =\left(\left(\frac{850 \sqrt{85}}{3}\right)\right)-\left(\left(\frac{50 \sqrt{5}}{3}\right)\right) \\  & =- \frac{50 \sqrt{5}}{3} + \frac{850 \sqrt{85}}{3}\end{aligned}
$$


---

Generated variant / moderate / reciprocal / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/d5a6217a8602f558f59d8119.png)

Evaluate the line integral
${\int }_{C}3 x y^{6}\,\text{d}s,$
where $C$ is the section of the curve $x=\frac{1}{y}$ from $(1,1)$ to $(\frac{1}{3},3),$ as shown above.

- $- \sqrt{2} + 41 \sqrt{82}$ **CORRECT**
- $364$
- $\sqrt{2} + 41 \sqrt{82}$
- $2520$
- $41 \sqrt{82}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\frac{1}{t}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\frac{1}{t},\,t⟩,\,1\le t\le 3
$$

Note that the domain $1\le t\le 3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{1}{t})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =- \frac{1}{t^{2}}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(- \frac{1}{t^{2}})^2+1^2} \\  & =\sqrt{\frac{1}{t^{4}}+1} \\  & =\sqrt{1 + \frac{1}{t^{4}}}\end{aligned}
$$

 

Now, if  $f(x,y)=3 x y^{6},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =3 \left(\frac{1}{t}\right) t^{6} \\  & =3 t^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}3 x y^{6}\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}\left(3 t^{5}\right)\cdot\left(\sqrt{1 + \frac{1}{t^{4}}}\right)\,\text{d}t \\  & ={\int }_{1}^{3}3 t^{3} \sqrt{t^{4} + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{4} + 1,$ $\text{d}u=4 t^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{3}3 t^{3} \sqrt{t^{4} + 1}\,\text{d}t & =3{\int }_{2}^{82}\sqrt{u}\cdot\left(\frac{1}{4}\right)\,\text{d}u \\  & ={\int }_{2}^{82}\frac{3 \sqrt{u}}{4}\,\text{d}u \\  & =\left[\frac{3}{4}\cdot\frac{2}{3}u^{3/2}\right]_{2}^{82} \\  & =\left[\frac{u^{\frac{3}{2}}}{2}\right]_{2}^{82} \\  & =\left(\left(\frac{\left(82\right)^{\frac{3}{2}}}{2}\right)\right)-\left(\left(\frac{\left(2\right)^{\frac{3}{2}}}{2}\right)\right) \\  & =\left(\left(41 \sqrt{82}\right)\right)-\left(\left(\sqrt{2}\right)\right) \\  & =- \sqrt{2} + 41 \sqrt{82}\end{aligned}
$$


---

Generated variant / moderate / line_log / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/3f308b9cc26cd4b1bc48d929.png)

Evaluate the line integral
${\int }_{C}\frac{10}{- x + y}\,\text{d}s,$
where $C$ is the section of the curve $x=2 y - 6$ from $(-4,1)$ to $(2,4),$ as shown above.

- $10 \sqrt{5} \ln{\left(\frac{5}{2} \right)}$ **CORRECT**
- $50 \ln{\left(\frac{5}{2} \right)}$
- $10 \ln{\left(\frac{5}{2} \right)}$
- $30 \sqrt{5}$
- $10 \sqrt{5} \ln{\left(5 \right)}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t - 6.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t - 6,\,t⟩,\,1\le t\le 4
$$

Note that the domain $1\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t - 6)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{10}{- x + y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{10}{- \left(2 t - 6\right) + t} \\  & =- \frac{10}{t - 6}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{10}{- x + y}\,\text{d}s & ={\int }_{1}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{4}\left(- \frac{10}{t - 6}\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{4}- \frac{10 \sqrt{5}}{t - 6}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=6 - t,$ $\text{d}u=-1\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{4}- \frac{10 \sqrt{5}}{t - 6}\,\text{d}t & =10 \sqrt{5}{\int }_{5}^{2}\frac{1}{u}\cdot(-1)\,\text{d}u \\  & ={\int }_{5}^{2}- \frac{10 \sqrt{5}}{u}\,\text{d}u \\  & =\left[-(10 \sqrt{5})\cdot\ln{u}\right]_{5}^{2} \\  & =\left[- 10 \sqrt{5} \ln{\left(u \right)}\right]_{5}^{2} \\  & =\left(\left(- 10 \sqrt{5} \ln{\left(\left(2\right) \right)}\right)\right)-\left(\left(- 10 \sqrt{5} \ln{\left(\left(5\right) \right)}\right)\right) \\  & =\left(\left(- 10 \sqrt{5} \ln{\left(2 \right)}\right)\right)-\left(\left(- 10 \sqrt{5} \ln{\left(5 \right)}\right)\right) \\  & =10 \sqrt{5} \ln{\left(\frac{5}{2} \right)}\end{aligned}
$$


---

Generated variant / moderate / line_log / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/3d1e766b0586e45393a8ef5e.png)

Evaluate the line integral
${\int }_{C}\frac{3}{- x + y}\,\text{d}s,$
where $C$ is the section of the curve $x=2 y - 4$ from $(-2,1)$ to $(0,2),$ as shown above.

- $3 \sqrt{5} \ln{\left(\frac{3}{2} \right)}$ **CORRECT**
- $3 \ln{\left(\frac{3}{2} \right)}$
- $15 \ln{\left(\frac{3}{2} \right)}$
- $3 \sqrt{5}$
- $3 \sqrt{5} \ln{\left(3 \right)}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2 t - 4.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2 t - 4,\,t⟩,\,1\le t\le 2
$$

Note that the domain $1\le t\le 2$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t - 4)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2)^2+1^2} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{3}{- x + y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{3}{- \left(2 t - 4\right) + t} \\  & =- \frac{3}{t - 4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{3}{- x + y}\,\text{d}s & ={\int }_{1}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2}\left(- \frac{3}{t - 4}\right)\cdot\left(\sqrt{5}\right)\,\text{d}t \\  & ={\int }_{1}^{2}- \frac{3 \sqrt{5}}{t - 4}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 - t,$ $\text{d}u=-1\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{2}- \frac{3 \sqrt{5}}{t - 4}\,\text{d}t & =3 \sqrt{5}{\int }_{3}^{2}\frac{1}{u}\cdot(-1)\,\text{d}u \\  & ={\int }_{3}^{2}- \frac{3 \sqrt{5}}{u}\,\text{d}u \\  & =\left[-(3 \sqrt{5})\cdot\ln{u}\right]_{3}^{2} \\  & =\left[- 3 \sqrt{5} \ln{\left(u \right)}\right]_{3}^{2} \\  & =\left(\left(- 3 \sqrt{5} \ln{\left(\left(2\right) \right)}\right)\right)-\left(\left(- 3 \sqrt{5} \ln{\left(\left(3\right) \right)}\right)\right) \\  & =\left(\left(- 3 \sqrt{5} \ln{\left(2 \right)}\right)\right)-\left(\left(- 3 \sqrt{5} \ln{\left(3 \right)}\right)\right) \\  & =3 \sqrt{5} \ln{\left(\frac{3}{2} \right)}\end{aligned}
$$


---

Generated variant / moderate / log_curve / method

Evaluate the line integral
${\int }_{C}10 y^{3} e^{- x}\,\text{d}s,$
where $C$ is the section of the curve $x=\ln{\left(y \right)}$ from $(0,1)$ to $(\ln{\left(\sqrt{15} \right)},\sqrt{15}).$

- $\frac{640}{3} - \frac{20 \sqrt{2}}{3}$ **CORRECT**
- $\frac{20 \sqrt{2}}{3} + \frac{640}{3}$
- $- \frac{10}{3} + 50 \sqrt{15}$
- $\frac{640}{3}$
- $630$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\ln{\left(t \right)}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\ln{\left(t \right)},\,t⟩,\,1\le t\le \sqrt{15}
$$

Note that the domain $1\le t\le \sqrt{15}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{t}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{1}{t})^2+1^2} \\  & =\sqrt{\frac{1}{t^{2}}+1} \\  & =\sqrt{1 + \frac{1}{t^{2}}}\end{aligned}
$$

 

Now, if  $f(x,y)=10 y^{3} e^{- x},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =10 t^{3} e^{- \left(\ln{\left(t \right)}\right)} \\  & =10 t^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}10 y^{3} e^{- x}\,\text{d}s & ={\int }_{1}^{\sqrt{15}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{15}}\left(10 t^{2}\right)\cdot\left(\sqrt{1 + \frac{1}{t^{2}}}\right)\,\text{d}t \\  & ={\int }_{1}^{\sqrt{15}}10 t \sqrt{t^{2} + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{2} + 1,$ $\text{d}u=2 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{\sqrt{15}}10 t \sqrt{t^{2} + 1}\,\text{d}t & =10{\int }_{2}^{16}\sqrt{u}\cdot\left(\frac{1}{2}\right)\,\text{d}u \\  & ={\int }_{2}^{16}5 \sqrt{u}\,\text{d}u \\  & =\left[5\cdot\frac{2}{3}u^{3/2}\right]_{2}^{16} \\  & =\left[\frac{10 u^{\frac{3}{2}}}{3}\right]_{2}^{16} \\  & =\left(\left(\frac{10 \left(16\right)^{\frac{3}{2}}}{3}\right)\right)-\left(\left(\frac{10 \left(2\right)^{\frac{3}{2}}}{3}\right)\right) \\  & =\left(\left(\frac{640}{3}\right)\right)-\left(\left(\frac{20 \sqrt{2}}{3}\right)\right) \\  & =\frac{640}{3} - \frac{20 \sqrt{2}}{3}\end{aligned}
$$


---

Generated variant / moderate / log_curve / method

Evaluate the line integral
${\int }_{C}3 y^{3} e^{- x}\,\text{d}s,$
where $C$ is the section of the curve $x=\ln{\left(y \right)}$ from $(0,1)$ to $(\ln{\left(\sqrt{3} \right)},\sqrt{3}).$

- $8 - 2 \sqrt{2}$ **CORRECT**
- $2 \sqrt{2} + 8$
- $-1 + 3 \sqrt{3}$
- $9$
- $8$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\ln{\left(t \right)}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\ln{\left(t \right)},\,t⟩,\,1\le t\le \sqrt{3}
$$

Note that the domain $1\le t\le \sqrt{3}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{t}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{1}{t})^2+1^2} \\  & =\sqrt{\frac{1}{t^{2}}+1} \\  & =\sqrt{1 + \frac{1}{t^{2}}}\end{aligned}
$$

 

Now, if  $f(x,y)=3 y^{3} e^{- x},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =3 t^{3} e^{- \left(\ln{\left(t \right)}\right)} \\  & =3 t^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}3 y^{3} e^{- x}\,\text{d}s & ={\int }_{1}^{\sqrt{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{3}}\left(3 t^{2}\right)\cdot\left(\sqrt{1 + \frac{1}{t^{2}}}\right)\,\text{d}t \\  & ={\int }_{1}^{\sqrt{3}}3 t \sqrt{t^{2} + 1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{2} + 1,$ $\text{d}u=2 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{\sqrt{3}}3 t \sqrt{t^{2} + 1}\,\text{d}t & =3{\int }_{2}^{4}\sqrt{u}\cdot\left(\frac{1}{2}\right)\,\text{d}u \\  & ={\int }_{2}^{4}\frac{3 \sqrt{u}}{2}\,\text{d}u \\  & =\left[\frac{3}{2}\cdot\frac{2}{3}u^{3/2}\right]_{2}^{4} \\  & =\left[u^{\frac{3}{2}}\right]_{2}^{4} \\  & =\left(\left(\left(4\right)^{\frac{3}{2}}\right)\right)-\left(\left(\left(2\right)^{\frac{3}{2}}\right)\right) \\  & =\left(\left(8\right)\right)-\left(\left(2 \sqrt{2}\right)\right) \\  & =8 - 2 \sqrt{2}\end{aligned}
$$


---

Generated variant / hard / implicit_parabola / method

Evaluate the line integral
${\int }_{C}\frac{10 x}{y}\,\text{d}s,$
where $C$ is the section of the curve $y^2=6x$ from $(\frac{8}{3},4)$ to $(\frac{20}{3},2 \sqrt{10}).$

- $\frac{740}{3}$
- $\frac{1090}{27}$ **CORRECT**
- $20$
- $\frac{1715}{27}$
- $\frac{260}{3}$

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
r(t)=⟨\frac{t^{2}}{6},\,t⟩,\,4\le t\le 2 \sqrt{10}
$$

Note that the domain $4\le t\le 2 \sqrt{10}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{t^{2}}{6})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{t}{3}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{t}{3})^2+1^2} \\  & =\sqrt{\frac{t^{2}}{9}+1} \\  & =\sqrt{\frac{t^{2}}{9} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{10 x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{10 \left(\frac{t^{2}}{6}\right)}{t} \\  & =\frac{5 t}{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{10 x}{y}\,\text{d}s & ={\int }_{4}^{2 \sqrt{10}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{4}^{2 \sqrt{10}}\left(\frac{5 t}{3}\right)\cdot\left(\sqrt{\frac{t^{2}}{9} + 1}\right)\,\text{d}t \\  & ={\int }_{4}^{2 \sqrt{10}}\frac{5 t \sqrt{t^{2} + 9}}{9}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{2} + 9,$ $\text{d}u=2 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{4}^{2 \sqrt{10}}\frac{5 t \sqrt{t^{2} + 9}}{9}\,\text{d}t & =\frac{5}{9}{\int }_{25}^{49}\sqrt{u}\cdot\left(\frac{1}{2}\right)\,\text{d}u \\  & ={\int }_{25}^{49}\frac{5 \sqrt{u}}{18}\,\text{d}u \\  & =\left[\frac{5}{18}\cdot\frac{2}{3}u^{3/2}\right]_{25}^{49} \\  & =\left[\frac{5 u^{\frac{3}{2}}}{27}\right]_{25}^{49} \\  & =\left(\left(\frac{5 \left(49\right)^{\frac{3}{2}}}{27}\right)\right)-\left(\left(\frac{5 \left(25\right)^{\frac{3}{2}}}{27}\right)\right) \\  & =\left(\left(\frac{1715}{27}\right)\right)-\left(\left(\frac{625}{27}\right)\right) \\  & =\frac{1090}{27}\end{aligned}
$$


---

Generated variant / hard / implicit_parabola / method

Evaluate the line integral
${\int }_{C}\frac{3 x}{y}\,\text{d}s,$
where $C$ is the section of the curve $y^2=4x$ from $(3,2 \sqrt{3})$ to $(8,4 \sqrt{2}).$

- $\frac{15}{2}$
- $35$
- $19$ **CORRECT**
- $\frac{195}{2}$
- $27$

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
y^2=4x\,⟹\,x=\frac{y^{2}}{4}.
$$

Therefore, by setting $y=t,$ we have

$$
x=x(t)=\frac{t^{2}}{4}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\frac{t^{2}}{4},\,t⟩,\,2 \sqrt{3}\le t\le 4 \sqrt{2}
$$

Note that the domain $2 \sqrt{3}\le t\le 4 \sqrt{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{t^{2}}{4})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{t}{2}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{t}{2})^2+1^2} \\  & =\sqrt{\frac{t^{2}}{4}+1} \\  & =\sqrt{\frac{t^{2}}{4} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{3 x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{3 \left(\frac{t^{2}}{4}\right)}{t} \\  & =\frac{3 t}{4}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{3 x}{y}\,\text{d}s & ={\int }_{2 \sqrt{3}}^{4 \sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{2 \sqrt{3}}^{4 \sqrt{2}}\left(\frac{3 t}{4}\right)\cdot\left(\sqrt{\frac{t^{2}}{4} + 1}\right)\,\text{d}t \\  & ={\int }_{2 \sqrt{3}}^{4 \sqrt{2}}\frac{3 t \sqrt{t^{2} + 4}}{8}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=t^{2} + 4,$ $\text{d}u=2 t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{2 \sqrt{3}}^{4 \sqrt{2}}\frac{3 t \sqrt{t^{2} + 4}}{8}\,\text{d}t & =\frac{3}{8}{\int }_{16}^{36}\sqrt{u}\cdot\left(\frac{1}{2}\right)\,\text{d}u \\  & ={\int }_{16}^{36}\frac{3 \sqrt{u}}{16}\,\text{d}u \\  & =\left[\frac{3}{16}\cdot\frac{2}{3}u^{3/2}\right]_{16}^{36} \\  & =\left[\frac{u^{\frac{3}{2}}}{8}\right]_{16}^{36} \\  & =\left(\left(\frac{\left(36\right)^{\frac{3}{2}}}{8}\right)\right)-\left(\left(\frac{\left(16\right)^{\frac{3}{2}}}{8}\right)\right) \\  & =\left(\left(27\right)\right)-\left(\left(8\right)\right) \\  & =19\end{aligned}
$$


---

Generated variant / hard / exponential / method

Evaluate the line integral
${\int }_{C}10 x^{6} e^{- 2 y}\,\text{d}s,$
where $C$ is the section of the curve $x=e^{\frac{y}{2}}$ from $(1,0)$ to $(2,\ln{\left(4 \right)}).$

- $- \frac{50 \sqrt{5}}{3} + \frac{160 \sqrt{2}}{3}$ **CORRECT**
- $\frac{50 \sqrt{5}}{3} + \frac{160 \sqrt{2}}{3}$
- $30$
- $\frac{160 \sqrt{2}}{3}$
- $\frac{195}{2}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=e^{\frac{t}{2}}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨e^{\frac{t}{2}},\,t⟩,\,0\le t\le \ln{\left(4 \right)}
$$

Note that the domain $0\le t\le \ln{\left(4 \right)}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(e^{\frac{t}{2}})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{e^{\frac{t}{2}}}{2}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{e^{\frac{t}{2}}}{2})^2+1^2} \\  & =\sqrt{\frac{e^{t}}{4}+1} \\  & =\sqrt{\frac{e^{t}}{4} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=10 x^{6} e^{- 2 y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =10 \left(e^{\frac{t}{2}}\right)^{6} e^{- 2 t} \\  & =10 e^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}10 x^{6} e^{- 2 y}\,\text{d}s & ={\int }_{0}^{\ln{\left(4 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(4 \right)}}\left(10 e^{t}\right)\cdot\left(\sqrt{\frac{e^{t}}{4} + 1}\right)\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(4 \right)}}5 \sqrt{e^{t} + 4} e^{t}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=e^{t} + 4,$ $\text{d}u=e^{t}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\ln{\left(4 \right)}}5 \sqrt{e^{t} + 4} e^{t}\,\text{d}t & =5{\int }_{5}^{8}\sqrt{u}\cdot\left(1\right)\,\text{d}u \\  & ={\int }_{5}^{8}5 \sqrt{u}\,\text{d}u \\  & =\left[5\cdot\frac{2}{3}u^{3/2}\right]_{5}^{8} \\  & =\left[\frac{10 u^{\frac{3}{2}}}{3}\right]_{5}^{8} \\  & =\left(\left(\frac{10 \left(8\right)^{\frac{3}{2}}}{3}\right)\right)-\left(\left(\frac{10 \left(5\right)^{\frac{3}{2}}}{3}\right)\right) \\  & =\left(\left(\frac{160 \sqrt{2}}{3}\right)\right)-\left(\left(\frac{50 \sqrt{5}}{3}\right)\right) \\  & =- \frac{50 \sqrt{5}}{3} + \frac{160 \sqrt{2}}{3}\end{aligned}
$$


---

Generated variant / hard / exponential / method

Evaluate the line integral
${\int }_{C}3 x^{6} e^{- 2 y}\,\text{d}s,$
where $C$ is the section of the curve $x=e^{\frac{y}{2}}$ from $(1,0)$ to $(\sqrt{2},\ln{\left(2 \right)}).$

- $- 5 \sqrt{5} + 6 \sqrt{6}$ **CORRECT**
- $5 \sqrt{5} + 6 \sqrt{6}$
- $3$
- $\frac{33}{4}$
- $6 \sqrt{6}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=e^{\frac{t}{2}}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨e^{\frac{t}{2}},\,t⟩,\,0\le t\le \ln{\left(2 \right)}
$$

Note that the domain $0\le t\le \ln{\left(2 \right)}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(e^{\frac{t}{2}})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{e^{\frac{t}{2}}}{2}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{e^{\frac{t}{2}}}{2})^2+1^2} \\  & =\sqrt{\frac{e^{t}}{4}+1} \\  & =\sqrt{\frac{e^{t}}{4} + 1}\end{aligned}
$$

 

Now, if  $f(x,y)=3 x^{6} e^{- 2 y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =3 \left(e^{\frac{t}{2}}\right)^{6} e^{- 2 t} \\  & =3 e^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}3 x^{6} e^{- 2 y}\,\text{d}s & ={\int }_{0}^{\ln{\left(2 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(2 \right)}}\left(3 e^{t}\right)\cdot\left(\sqrt{\frac{e^{t}}{4} + 1}\right)\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(2 \right)}}\frac{3 \sqrt{e^{t} + 4} e^{t}}{2}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=e^{t} + 4,$ $\text{d}u=e^{t}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\ln{\left(2 \right)}}\frac{3 \sqrt{e^{t} + 4} e^{t}}{2}\,\text{d}t & =\frac{3}{2}{\int }_{5}^{6}\sqrt{u}\cdot\left(1\right)\,\text{d}u \\  & ={\int }_{5}^{6}\frac{3 \sqrt{u}}{2}\,\text{d}u \\  & =\left[\frac{3}{2}\cdot\frac{2}{3}u^{3/2}\right]_{5}^{6} \\  & =\left[u^{\frac{3}{2}}\right]_{5}^{6} \\  & =\left(\left(\left(6\right)^{\frac{3}{2}}\right)\right)-\left(\left(\left(5\right)^{\frac{3}{2}}\right)\right) \\  & =\left(\left(6 \sqrt{6}\right)\right)-\left(\left(5 \sqrt{5}\right)\right) \\  & =- 5 \sqrt{5} + 6 \sqrt{6}\end{aligned}
$$


---

Generated variant / hard / sqrt / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/c563dc03bb6b1ec42895b7e3.png)

Evaluate the line integral
${\int }_{C}10 x y\,\text{d}s,$
where $C$ is the section of the curve $x=\sqrt{3} \sqrt{y}$ from $(\sqrt{3},1)$ to $(\sqrt{15},5),$ as shown above.

- $- \frac{7 \sqrt{21}}{4} + \frac{207 \sqrt{69}}{4}$ **CORRECT**
- $\frac{3020 \sqrt{3}}{3}$
- $- 4 \sqrt{3} + 100 \sqrt{15}$
- $\frac{7 \sqrt{21}}{4} + \frac{207 \sqrt{69}}{4}$
- $\frac{207 \sqrt{69}}{4}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=\sqrt{3} \sqrt{t}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\sqrt{3} \sqrt{t},\,t⟩,\,1\le t\le 5
$$

Note that the domain $1\le t\le 5$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sqrt{3} \sqrt{t})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{\sqrt{3}}{2 \sqrt{t}}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(\frac{\sqrt{3}}{2 \sqrt{t}})^2+1^2} \\  & =\sqrt{\frac{3}{4 t}+1} \\  & =\sqrt{1 + \frac{3}{4 t}}\end{aligned}
$$

 

Now, if  $f(x,y)=10 x y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =10 \left(\sqrt{3} \sqrt{t}\right) t \\  & =10 \sqrt{3} t^{\frac{3}{2}}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}10 x y\,\text{d}s & ={\int }_{1}^{5}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{5}\left(10 \sqrt{3} t^{\frac{3}{2}}\right)\cdot\left(\sqrt{1 + \frac{3}{4 t}}\right)\,\text{d}t \\  & ={\int }_{1}^{5}5 t \sqrt{12 t + 9}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 t + 3,$ $\text{d}u=4\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{5}5 t \sqrt{12 t + 9}\,\text{d}t & =5 \sqrt{3}{\int }_{7}^{23}\frac{u-3}{4}\cdot\sqrt{u}\cdot\frac{1}{4}\,\text{d}u \\  & ={\int }_{7}^{23}\frac{5 \sqrt{3} u^{\frac{3}{2}}}{16} - \frac{15 \sqrt{3} \sqrt{u}}{16}\,\text{d}u \\  & =\left[\frac{5 \sqrt{3}}{16}\cdot\left(\frac{2}{5}u^{5/2}-(3)\cdot\frac{2}{3}u^{3/2}\right)\right]_{7}^{23} \\  & =\left[\frac{5 \sqrt{3} \left(\frac{2 u^{\frac{5}{2}}}{5} - 2 u^{\frac{3}{2}}\right)}{16}\right]_{7}^{23} \\  & =\left(\left(\frac{\sqrt{3} \left(23\right)^{\frac{5}{2}}}{8}\right)+\left(- \frac{5 \sqrt{3} \left(23\right)^{\frac{3}{2}}}{8}\right)\right)-\left(\left(\frac{\sqrt{3} \left(7\right)^{\frac{5}{2}}}{8}\right)+\left(- \frac{5 \sqrt{3} \left(7\right)^{\frac{3}{2}}}{8}\right)\right) \\  & =\left(\left(\frac{529 \sqrt{69}}{8}\right)+\left(- \frac{115 \sqrt{69}}{8}\right)\right)-\left(\left(\frac{49 \sqrt{21}}{8}\right)+\left(- \frac{35 \sqrt{21}}{8}\right)\right) \\  & =- \frac{7 \sqrt{21}}{4} + \frac{207 \sqrt{69}}{4}\end{aligned}
$$


---

Generated variant / hard / sqrt / method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/9897043e0fa84d0f7b41a5e4.png)

Evaluate the line integral
${\int }_{C}3 x y\,\text{d}s,$
where $C$ is the section of the curve $x=\sqrt{y}$ from $(1,1)$ to $(\sqrt{5},5),$ as shown above.

- $- \frac{5 \sqrt{5}}{8} + \frac{609 \sqrt{21}}{40}$ **CORRECT**
- $- \frac{6}{5} + 30 \sqrt{5}$
- $\frac{5 \sqrt{5}}{8} + \frac{609 \sqrt{21}}{40}$
- $266$
- $\frac{609 \sqrt{21}}{40}$

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

 

Now, if  $f(x,y)=3 x y,$ then we obtain 

$$
\begin{aligned}f(r(t)) & =3 \left(\sqrt{t}\right) t \\  & =3 t^{\frac{3}{2}}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}3 x y\,\text{d}s & ={\int }_{1}^{5}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{5}\left(3 t^{\frac{3}{2}}\right)\cdot\left(\sqrt{1 + \frac{1}{4 t}}\right)\,\text{d}t \\  & ={\int }_{1}^{5}\frac{3 t \sqrt{4 t + 1}}{2}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4 t + 1,$ $\text{d}u=4\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{5}\frac{3 t \sqrt{4 t + 1}}{2}\,\text{d}t & =\frac{3}{2}{\int }_{5}^{21}\frac{u-1}{4}\cdot\sqrt{u}\cdot\frac{1}{4}\,\text{d}u \\  & ={\int }_{5}^{21}\frac{3 u^{\frac{3}{2}}}{32} - \frac{3 \sqrt{u}}{32}\,\text{d}u \\  & =\left[\frac{3}{32}\cdot\left(\frac{2}{5}u^{5/2}-(1)\cdot\frac{2}{3}u^{3/2}\right)\right]_{5}^{21} \\  & =\left[\frac{3 u^{\frac{5}{2}}}{80} - \frac{u^{\frac{3}{2}}}{16}\right]_{5}^{21} \\  & =\left(\left(\frac{3 \left(21\right)^{\frac{5}{2}}}{80}\right)+\left(- \frac{\left(21\right)^{\frac{3}{2}}}{16}\right)\right)-\left(\left(\frac{3 \left(5\right)^{\frac{5}{2}}}{80}\right)+\left(- \frac{\left(5\right)^{\frac{3}{2}}}{16}\right)\right) \\  & =\left(\left(\frac{1323 \sqrt{21}}{80}\right)+\left(- \frac{21 \sqrt{21}}{16}\right)\right)-\left(\left(\frac{15 \sqrt{5}}{16}\right)+\left(- \frac{5 \sqrt{5}}{16}\right)\right) \\  & =- \frac{5 \sqrt{5}}{8} + \frac{609 \sqrt{21}}{40}\end{aligned}
$$


---

Generated variant / hard / implicit_parabola / source:q-122271

Evaluate the line integral
${\int }_{C}\frac{24x}{y}\,\text{d}s,$
where $C$ is the arc of the parabola ${y}^{2}=8x$ from $(0,0)$ to $(2,4).$

- $-18+32\sqrt{2}$
- $-\frac{29}{2}+32\sqrt{2}$
- $-\frac{39}{2}+32\sqrt{2}$
- $-\frac{37}{2}+32\sqrt{2}$
- $-16+32\sqrt{2}$ **CORRECT**

Notice that the given curve can be expressed in the form $x=x(y),$ as follows:

$$
{y}^{2}=8x\,⟹\,x=\frac{{y}^{2}}{8}.
$$

Therefore, by setting $y=t,$ we have

$$
x=x(t)=\frac{{t}^{2}}{8}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨\frac{{t}^{2}}{8},\,t⟩,\,0\le t\le 4
$$

Note that the domain $0\le t\le 4$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{8})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{t}{4}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{(\frac{t}{4})}^{2}+{1}^{2}} \\  & =\sqrt{\frac{{t}^{2}}{16}+1} \\  & =\frac{1}{4}\sqrt{{t}^{2}+16}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{24x}{y}$, then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{24x}{y} \\  & =\frac{24\cdot (\frac{{t}^{2}}{8})}{t} \\  & =3t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{24x}{y}\,\text{d}s & ={\int }_{0}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{4}3t\cdot \frac{1}{4}\sqrt{{t}^{2}+16}\cdot \text{d}t \\  & =\frac{3}{4}{\int }_{0}^{4}t\sqrt{{t}^{2}+16}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u={t}^{2}+16,$ $\text{d}u=2t\,\text{d}t$ as follows:

$$
\begin{aligned}\frac{3}{4}{\int }_{0}^{4}t\sqrt{{t}^{2}+16}\,\text{d}t & =\frac{3}{8}{\int }_{16}^{32}\sqrt{u}\,\text{d}u \\  & =\frac{1}{4}\cdot {u}^{3/2}\,{|}_{16}^{32} \\  & =\frac{1}{4}({32}^{3/2}-{16}^{3/2}) \\  & =\frac{1}{4}(128\sqrt{2}-64) \\  & =-16+32\sqrt{2}\end{aligned}
$$


---

Generated variant / not rated / sqrt / source:q-122579

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/c5c80c6bc60735c626450e0b.png)

Evaluate the line integral
$\displaystyle \int_(C)4xyds$,
where $C$ is the section of the curve $x = \sqrt{y}$ from $(0, 0)$ to $(\sqrt{3}, 3)$, as shown above.

- $\frac{72}{745}+\frac{15912\sqrt{13}}{745}$
- $\frac{125}{894}+\frac{27625\sqrt{13}}{894}$
- $\frac{121}{4470}+\frac{26741\sqrt{13}}{4470}$
- $\frac{213}{1490}+\frac{47073\sqrt{13}}{1490}$
- $\frac{1}{30}+\frac{221\sqrt{13}}{30}$
[Original correct designation absent; independently derived value 1/30 + 221*sqrt(13)/30.]

(Source worked solution absent.)


---

Generated variant / moderate / parabola / source:q-122574

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/b95597c11f49e0e7ff31389d.png)

Evaluate the line integral
${\int }_{C}\frac{12x}{y}\,\text{d}s,$
where $C$ is the arc of the parabola $x={y}^{2}$ from $(1,1)$ to $(\frac{99}{4},\frac{3\sqrt{11}}{2}),$ as shown above.

- $100-\sqrt{5}$
- $36-\sqrt{6}$
- $\frac{99}{4}-\sqrt{5}$
- $6(36-\sqrt{6})$
- $5(200-\sqrt{5})$ **CORRECT**

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)={t}^{2}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨{t}^{2},\,t⟩,\,1\le t\le \frac{3\sqrt{11}}{2}
$$

Note that the domain $1\le t\le \frac{3\sqrt{11}}{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{(2t)}^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+1}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{12x}{y},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{12{t}^{2}}{t} \\  & =12t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{12x}{y}\,\text{d}s & ={\int }_{1}^{\frac{3\sqrt{11}}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\frac{3\sqrt{11}}{2}}12t\sqrt{4{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4{t}^{2}+1,$ $\text{d}u=8t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{1}^{\frac{3\sqrt{11}}{2}}12t\sqrt{4{t}^{2}+1}\,\text{d}t & =12{\int }_{5}^{100}\sqrt{u}\cdot \frac{1}{8}\,\text{d}u \\  & =\frac{3}{2}{\int }_{5}^{100}\sqrt{u}\,\text{d}u \\  & =\frac{3}{2}\cdot \frac{2}{3}\sqrt{{u}^{3}}\,{|}_{5}^{100} \\  & =\sqrt{{100}^{3}}-\sqrt{{5}^{3}} \\  & =1000-5\sqrt{5} \\  & =5(200-\sqrt{5})\end{aligned}
$$


---

Generated variant / moderate / reciprocal / source:q-122593

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/6cc0eeb9bd08cd9e32ed01fa.png)

Evaluate the line integral
${\int }_{C}x{y}^{6}\,\text{d}s,$
where $C$ is the section of the curve $x=\frac{2}{y}$ from $(2,1)$ to $(\frac{2}{3},3),$ as shown above.

- $\frac{86\sqrt{3}}{5}$
- $\frac{100}{77}$
- $11\sqrt{5}$
- $\frac{49}{15}$
- $-\frac{5\sqrt{5}}{3}+\frac{85\sqrt{85}}{3}$ **CORRECT**

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
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\frac{2}{t})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =-\frac{2}{{t}^{2}}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{(-\frac{2}{{t}^{2}})}^{2}+{1}^{2}} \\  & =\sqrt{\frac{4}{{t}^{4}}+1} \\  & =\sqrt{\frac{{t}^{4}+4}{{t}^{4}}} \\  & =\frac{\sqrt{{t}^{4}+4}}{{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=x{y}^{6},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{2}{t}\cdot {t}^{6} \\  & =2{t}^{5}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}x{y}^{6}\,\text{d}s & ={\int }_{1}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{3}2{t}^{5}\cdot \frac{\sqrt{{t}^{4}+4}}{{t}^{2}}\,\text{d}t \\  & =2{\int }_{1}^{3}{t}^{3}\sqrt{{t}^{4}+4}\,\text{d}t\end{aligned}
$$

Finally, we solve this using the substitution $u={t}^{4}+4,$ $\text{d}u=4{t}^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}2{\int }_{1}^{3}{t}^{3}\sqrt{{t}^{4}+4}\,\text{d}t & =2{\int }_{5}^{85}\sqrt{u}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{2}{\int }_{5}^{85}\sqrt{u}\,\text{d}u \\  & =\frac{1}{2}\cdot \frac{2}{3}\sqrt{{u}^{3}}\,{|}_{5}^{85} \\  & =\frac{1}{3}[\sqrt{{85}^{3}}-\sqrt{{5}^{3}}] \\  & =\frac{85\sqrt{85}-5\sqrt{5}}{3} \\  & =-\frac{5\sqrt{5}}{3}+\frac{85\sqrt{85}}{3}\end{aligned}
$$


---

Generated variant / moderate / line_log / source:q-149727

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186179718/plots/4fcd449024da0ee43752b54d.png)

Evaluate the line integral
${\int }_{C}\frac{1}{y-x}\,\text{d}s,$
where $C$ is the segment of the line $x=2y-4$ from $(0,2)$ to $(1,\frac{5}{2}),$ as shown above.

- $\sqrt{2}\operatorname{ln}⁡5$
- $\sqrt{5}\operatorname{ln}⁡\frac{4}{3}$ **CORRECT**
- $\frac{7}{2}\sqrt{2}$
- $2\sqrt{5}$
- $2\operatorname{ln}⁡2$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)=2t-4.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨2t-4,\,t⟩,\,2\le t\le \frac{5}{2}
$$

Note that the domain $2\le t\le \frac{5}{2}$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2t-4)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =2\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{(2)}^{2}+{1}^{2}} \\  & =\sqrt{4+1} \\  & =\sqrt{5}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{1}{y-x},$ then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(2t-4)} \\  & =\frac{1}{4-t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{1}{y-x}\,\text{d}s & ={\int }_{2}^{\frac{5}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{2}^{\frac{5}{2}}\frac{1}{4-t}\cdot \sqrt{5}\,\text{d}t \\  & =\sqrt{5}{\int }_{2}^{\frac{5}{2}}\frac{1}{4-t}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u=4-t,$ $\text{d}u=-\,\text{d}t$ as follows:

$$
\begin{aligned}\sqrt{5}{\int }_{2}^{\frac{5}{2}}\frac{1}{4-t}\,\text{d}t & =\sqrt{5}{\int }_{2}^{\frac{3}{2}}\frac{1}{u}\cdot (-\text{d}u) \\  & =-\sqrt{5}{\int }_{2}^{\frac{3}{2}}\frac{1}{u}\,\text{d}u \\  & =\sqrt{5}{\int }_{\frac{3}{2}}^{2}\frac{1}{u}\,\text{d}u \\  & =\sqrt{5}[\operatorname{ln}⁡u]_{\frac{3}{2}}^{2} \\  & =\sqrt{5}[\operatorname{ln}⁡2-\operatorname{ln}⁡\frac{3}{2}] \\  & =\sqrt{5}[\operatorname{ln}⁡2-\operatorname{ln}⁡\frac{3}{2}] \\  & =\sqrt{5}\operatorname{ln}⁡\frac{4}{3}\end{aligned}
$$


---

Generated variant / hard / exponential / source:q-149745

Evaluate the line integral
${\int }_{C}6{x}^{6}{e}^{-2y}\,\text{d}s,$
where $C$ is the section of the curve $x={e}^{y/2}$ from $(1,0)$ to $(\sqrt{3},\operatorname{ln}⁡3).$

- $5\sqrt{7}-7\sqrt{5}$
- $14\sqrt{7}-10\sqrt{5}$ **CORRECT**
- $\sqrt{7}-\sqrt{5}$
- $\frac{7\sqrt{14}}{2}-2\sqrt{5}$
- $2\sqrt{7}-5\sqrt{5}$

Notice that the given curve is of the form $x=x(y),$ Therefore, by setting $y=t,$ we have

$$
x=x(t)={e}^{t/2}.
$$

This gives the following parametrization of the curve:

$$
r(t)=⟨{e}^{t/2},\,t⟩,\,0\le t\le \operatorname{ln}⁡3
$$

Note that the domain $0\le t\le \operatorname{ln}⁡3$ is defined by the $y$-coordinates of the end-points on the path.

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following: 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({e}^{t/2})i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{{e}^{t/2}}{2}\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{(\frac{{e}^{t/2}}{2})}^{2}+{1}^{2}} \\  & =\sqrt{\frac{{e}^{t}}{4}+1} \\  & =\frac{1}{2}\sqrt{{e}^{t}+4}\end{aligned}
$$

 

Now, if  $f(x,y)=6{x}^{6}{e}^{-2y}$, then we obtain 

$$
\begin{aligned}f(r(t)) & =6{x}^{6}{e}^{-2y} \\  & =6{({e}^{t/2})}^{6}{e}^{-2t} \\  & =6{e}^{t}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}6{x}^{6}{e}^{-2y}\,\text{d}s & ={\int }_{0}^{\operatorname{ln}⁡3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\operatorname{ln}⁡3}6{e}^{t}\cdot \frac{1}{2}\sqrt{{e}^{t}+4}\cdot \text{d}t \\  & =3{\int }_{0}^{\operatorname{ln}⁡3}{e}^{t}\sqrt{{e}^{t}+4}\,\text{d}t.\end{aligned}
$$

Finally, we solve this using the substitution $u={e}^{t}+4,$ $\text{d}u={e}^{t}\,\text{d}t$ as follows:

$$
\begin{aligned}3{\int }_{0}^{\operatorname{ln}⁡3}{e}^{t}\sqrt{{e}^{t}+4}\,\text{d}t & =3{\int }_{5}^{7}\sqrt{u}\,\text{d}u \\  & =3\cdot \frac{2}{3}{u}^{3/2}\,{|}_{5}^{7} \\  & =2({7}^{3/2}-{5}^{3/2}) \\  & =2(7\sqrt{7}-5\sqrt{5}) \\  & =14\sqrt{7}-10\sqrt{5}\end{aligned}
$$

