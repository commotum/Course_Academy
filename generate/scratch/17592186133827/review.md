## Original evidence q-76186

Evaluate the line integral of the function $f(x,y)=\frac{12x}{y-1}$ along the curve parametrized by $r(t)={t}^{2}\,i+(t+1)\,j\,$ for $t\in [\sqrt{2},\sqrt{6}].$

- $-64$
- $56$
- $-16$
- $98$
- $75$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i+(t+1)\,j$, then along the curve we have $x={t}^{2}$ and $y=t+1.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(t+1)\,j \\  & =2t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{12x}{y-1}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{12{t}^{2}}{(t+1)-1} \\  & =\frac{12{t}^{2}}{t} \\  & =12t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{\sqrt{2}}^{\sqrt{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=4{t}^{2}+1,$ $\text{d}u=8t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t & ={\int }_{9}^{25}\frac{3}{2}{u}^{1/2}\text{d}u \\  & ={u}^{3/2}{|}_{9}^{25} \\  & ={25}^{3/2}-{9}^{3/2} \\  & =125-27 \\  & =98\end{aligned}
$$

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral of the function $f(x,y)=2\left(\frac{12x}{y-1}\right)$ along the curve parametrized by $r(t)={t}^{2}\,i+(t+1)\,j\,$ for $t\in [\sqrt{2},\sqrt{6}].$

- $2\left(75\right)$
- $2\left(-64\right)$
- $2\left(56\right)$
- $2\left(98\right)$
- $2\left(-16\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i+(t+1)\,j$, then along the curve we have $x={t}^{2}$ and $y=t+1.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(t+1)\,j \\  & =2t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=2\left(\frac{12x}{y-1}\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left(\frac{12{t}^{2}}{(t+1)-1} \right)\\  & =2\left(\frac{12{t}^{2}}{t} \right)\\  & =2\left(12t\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{\sqrt{2}}^{\sqrt{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t\right).\end{aligned}
$$

We can solve this using the substitution $u=4{t}^{2}+1,$ $\text{d}u=8t\,\text{d}t$ as follows:

$$
\begin{aligned}2\left({\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t \right)& =2\left({\int }_{9}^{25}\frac{3}{2}{u}^{1/2}\text{d}u \right)\\  & =2\left({u}^{3/2}{|}_{9}^{25} \right)\\  & =2\left({25}^{3/2}-{9}^{3/2} \right)\\  & =2\left(125-27 \right)\\  & =2\left(98\right)\end{aligned}
$$

## Original evidence q-76187

Evaluate the line integral $\displaystyle \int_(C)4yz\cos xds$, where the curve $C$ is parametrized by $r(t) = ti + \sin tj + k$ for $0 < t < \frac{π}{2}$.

- $\frac{3\sqrt{2}}{4}$
- $\frac{3}{2}(\sqrt{2} - 1)$
- $\frac{3\sqrt{2}}{2}$
- $\frac{4}{3}(2\sqrt{2} - 1)$
- $\frac{1}{2}(2\sqrt{2} + 1)$

No original worked solution or correct ref; inferred correct is $\frac43(2\sqrt2-1)$.

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral $\displaystyle \int_(C)2\left(4yz\cos x\right)ds$, where the curve $C$ is parametrized by $r(t) = ti + \sin tj + k$ for $0 < t < \frac{π}{2}$.

- $2\left(\frac{1}{2}(2\sqrt{2} + 1)\right)$
- $2\left(\frac{3\sqrt{2}}{4}\right)$
- $2\left(\frac{3}{2}(\sqrt{2} - 1)\right)$
- $2\left(\frac{4}{3}(2\sqrt{2} - 1)\right)$
- $2\left(\frac{3\sqrt{2}}{2}\right)$

Original worked solution absent.

## Original evidence q-167612

Evaluate the line integral of the function $f(x,y)={x}^{3}+y$ along the curve parametrized by $r(t)=3t\,i+{t}^{3}\,j\,$ for $t\in [0,1].$

- $14(2\sqrt{2}-1)$
- $28\sqrt{2}$
- $7(\sqrt{2}-1)$
- $12\sqrt{2}-5$
- $7(2\sqrt{2}+1)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=3t\,i+{t}^{3}\,j$, then along the curve we have $x=3t$ and $y={t}^{3}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)\,i+\frac{\text{d}}{\text{d}t}({t}^{3})\,j \\  & =3\,i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{9+9{t}^{4}} \\  & =3\sqrt{1+{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}+y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3t)^{3}+{t}^{3} \\  & =27{t}^{3}+{t}^{3} \\  & =28{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}28{t}^{3}\cdot 3\sqrt{1+{t}^{4}}\,\text{d}t \\  & ={\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}.\end{aligned}
$$

We can solve this using the substitution $u=1+{t}^{4},$ $\text{d}u=4{t}^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t & ={\int }_{1}^{2}21\cdot {u}^{1/2}\,\text{d}u \\  & =21\cdot \frac{2}{3}{u}^{3/2}{|}_{1}^{2} \\  & =14({2}^{3/2}-{1}^{3/2}) \\  & =14(2\sqrt{2}-1)\end{aligned}
$$

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral of the function $f(x,y)=2\left({x}^{3}+y\right)$ along the curve parametrized by $r(t)=3t\,i+{t}^{3}\,j\,$ for $t\in [0,1].$

- $2\left(7(2\sqrt{2}+1)\right)$
- $2\left(14(2\sqrt{2}-1)\right)$
- $2\left(28\sqrt{2}\right)$
- $2\left(12\sqrt{2}-5\right)$
- $2\left(7(\sqrt{2}-1)\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=3t\,i+{t}^{3}\,j$, then along the curve we have $x=3t$ and $y={t}^{3}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)\,i+\frac{\text{d}}{\text{d}t}({t}^{3})\,j \\  & =3\,i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{9+9{t}^{4}} \\  & =3\sqrt{1+{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)=2\left({x}^{3}+y\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left((3t)^{3}+{t}^{3} \right)\\  & =2\left(27{t}^{3}+{t}^{3} \right)\\  & =2\left(28{t}^{3}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{1}28{t}^{3}\cdot 3\sqrt{1+{t}^{4}}\,\text{d}t \right)\\  & =2\left({\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}\right).\end{aligned}
$$

We can solve this using the substitution $u=1+{t}^{4},$ $\text{d}u=4{t}^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}2\left({\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t \right)& =2\left({\int }_{1}^{2}21\cdot {u}^{1/2}\,\text{d}u \right)\\  & =2\left(21\cdot \frac{2}{3}{u}^{3/2}{|}_{1}^{2} \right)\\  & =2\left(14({2}^{3/2}-{1}^{3/2}) \right)\\  & =2\left(14(2\sqrt{2}-1)\right)\end{aligned}
$$

## Original evidence q-76479

Evaluate the line integral of the function $f(x,y)=\operatorname{cos}⁡x$  along the curve $C$ parametrized by $r(t)={t}^{2}\,i-{t}^{2}\,j$ for $0<t<\sqrt{\pi /2}.$

- $\sqrt{2}-1$
- $2$
- $2\sqrt{2}$
- $\sqrt{2}$
- $2-\sqrt{2}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i-{t}^{2}\,j,$ then along the curve we have $x={t}^{2}$ and $y=-{t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(-{t}^{2})\,j \\  & =2t\,j-2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(-2t)^{2}} \\  & =\sqrt{8{t}^{2}} \\  & =2\sqrt{2}|t| \\  & =2\sqrt{2}t\end{aligned}
$$

Notice that $|t|=t$ because $t>0$ along the path of $C.$

Now, since $f(x,y)=\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\sqrt{\pi /2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u={t}^{2}$, $\text{d}u=2t\,\text{d}t$ as follows: 

$$
\begin{aligned}{\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t & =\sqrt{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\,\text{d}u \\  & =\sqrt{2}\,\operatorname{sin}⁡u\,{|}_{0}^{\pi /2} \\  & =\sqrt{2}(1-0) \\  & =\sqrt{2}\end{aligned}
$$

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral of the function $f(x,y)=2\left(\operatorname{cos}⁡x\right)$  along the curve $C$ parametrized by $r(t)={t}^{2}\,i-{t}^{2}\,j$ for $0<t<\sqrt{\pi /2}.$

- $2\left(2-\sqrt{2}\right)$
- $2\left(\sqrt{2}-1\right)$
- $2\left(2\right)$
- $2\left(\sqrt{2}\right)$
- $2\left(2\sqrt{2}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i-{t}^{2}\,j,$ then along the curve we have $x={t}^{2}$ and $y=-{t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(-{t}^{2})\,j \\  & =2t\,j-2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(-2t)^{2}} \\  & =\sqrt{8{t}^{2}} \\  & =2\sqrt{2}|t| \\  & =2\sqrt{2}t\end{aligned}
$$

Notice that $|t|=t$ because $t>0$ along the path of $C.$

Now, since $f(x,y)=2\left(\operatorname{cos}⁡x\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left(\operatorname{cos}⁡{t}^{2}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\sqrt{\pi /2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t\right).\end{aligned}
$$

We can solve this using the substitution $u={t}^{2}$, $\text{d}u=2t\,\text{d}t$ as follows: 

$$
\begin{aligned}2\left({\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t \right)& =2\left(\sqrt{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\,\text{d}u \right)\\  & =2\left(\sqrt{2}\,\operatorname{sin}⁡u\,{|}_{0}^{\pi /2} \right)\\  & =2\left(\sqrt{2}(1-0) \right)\\  & =2\left(\sqrt{2}\right)\end{aligned}
$$

## Original evidence q-76484

Evaluate the line integral of the function $f(x,y)=\frac{{x}^{2}+{y}^{2}}{5},$ along the curve parametrized by $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}].$

- $\frac{2}{5}$
- $\frac{5}{3}$
- $\frac{5}{2}$
- $\frac{20}{3}$
- $\frac{25}{3}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩,$ then along the curve we have $x=4\operatorname{sin}⁡t$ and $y=-3\operatorname{sin}⁡t.$   

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(-3\operatorname{sin}⁡t)j \\  & =4\operatorname{cos}⁡t\,i-3\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(4\operatorname{cos}⁡t)^{2}+(-3\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{cos}^{2}+9{cos}^{2}⁡t} \\  & =\sqrt{25{cos}^{2}⁡t} \\  & =5|\operatorname{cos}⁡t| \\  & =5\operatorname{cos}⁡t\end{aligned}
$$

Notice that $|\operatorname{cos}⁡t|=\operatorname{cos}⁡t$ because $\operatorname{cos}⁡t\ge 0$ when $t\in [0,\frac{\pi }{2}].$

Now, since $f(x,y)=\frac{{x}^{2}+{y}^{2}}{5}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{16{sin}^{2}⁡t+9{sin}^{2}⁡t}{5} \\  & =\frac{25{sin}^{2}⁡t}{5} \\  & =5{sin}^{2}⁡t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\pi /2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi /2}5{sin}^{2}⁡t\cdot 5\operatorname{cos}⁡t\,\text{d}t \\  & =25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t.\end{aligned}
$$

   

We can solve this using the substitution $u=\operatorname{sin}⁡t,$ $\text{d}u=\operatorname{cos}⁡t\,\text{d}t$ as follows: 

$$
\begin{aligned}25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t & =25{\int }_{0}^{1}{u}^{2}\,\text{d}u \\  & =25\cdot {\frac{{u}^{3}}{3}|}_{0}^{1} \\  & =25(\frac{1}{3}-0) \\  & =\frac{25}{3}\end{aligned}
$$

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral of the function $f(x,y)=2\left(\frac{{x}^{2}+{y}^{2}}{5}\right),$ along the curve parametrized by $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}].$

- $2\left(\frac{25}{3}\right)$
- $2\left(\frac{2}{5}\right)$
- $2\left(\frac{5}{3}\right)$
- $2\left(\frac{20}{3}\right)$
- $2\left(\frac{5}{2}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩,$ then along the curve we have $x=4\operatorname{sin}⁡t$ and $y=-3\operatorname{sin}⁡t.$   

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(-3\operatorname{sin}⁡t)j \\  & =4\operatorname{cos}⁡t\,i-3\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(4\operatorname{cos}⁡t)^{2}+(-3\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{cos}^{2}+9{cos}^{2}⁡t} \\  & =\sqrt{25{cos}^{2}⁡t} \\  & =5|\operatorname{cos}⁡t| \\  & =5\operatorname{cos}⁡t\end{aligned}
$$

Notice that $|\operatorname{cos}⁡t|=\operatorname{cos}⁡t$ because $\operatorname{cos}⁡t\ge 0$ when $t\in [0,\frac{\pi }{2}].$

Now, since $f(x,y)=2\left(\frac{{x}^{2}+{y}^{2}}{5}\right)$, we obtain

$$
\begin{aligned}f(r(t)) & =2\left(\frac{16{sin}^{2}⁡t+9{sin}^{2}⁡t}{5} \right)\\  & =2\left(\frac{25{sin}^{2}⁡t}{5} \right)\\  & =2\left(5{sin}^{2}⁡t\right).\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\pi /2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{0}^{\pi /2}5{sin}^{2}⁡t\cdot 5\operatorname{cos}⁡t\,\text{d}t \right)\\  & =2\left(25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t\right).\end{aligned}
$$

   

We can solve this using the substitution $u=\operatorname{sin}⁡t,$ $\text{d}u=\operatorname{cos}⁡t\,\text{d}t$ as follows: 

$$
\begin{aligned}2\left(25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \right)& =2\left(25{\int }_{0}^{1}{u}^{2}\,\text{d}u \right)\\  & =2\left(25\cdot {\frac{{u}^{3}}{3}|}_{0}^{1} \right)\\  & =2\left(25(\frac{1}{3}-0) \right)\\  & =2\left(\frac{25}{3}\right)\end{aligned}
$$

## Original evidence q-76496

Evaluate the line integral ${\int }_{C}\frac{y+z}{x}\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k$
for $1<t<\sqrt{2}.$

- $\frac{\sqrt{5}+3}{2}$
- $\frac{\sqrt{5}+\sqrt{3}}{3}$
- $\sqrt{5}+\sqrt{3}$
- $\frac{5\sqrt{5}-3\sqrt{3}}{6}$
- $5\sqrt{5}-3\sqrt{3}$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k,$ then along the curve we have $x=t,$ $y=\frac{{t}^{2}}{2},$ and $z=\frac{{t}^{2}}{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,k \\  & =i+t\,j+t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{t}^{2}+{t}^{2}} \\  & =\sqrt{1+2{t}^{2}}\end{aligned}
$$

Now, if $f(x,y)=\frac{y+z}{x}$, then we obtain

$$
\begin{aligned}f(r(t)) & =\frac{\frac{{t}^{2}}{2}+\frac{{t}^{2}}{2}}{t}=t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{y+z}{x}\,\text{d}s & ={\int }_{1}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+2{t}^{2}$, $\text{d}u=4t\,\text{d}t$ as follows: 

$$
\begin{aligned}{\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t & ={\int }_{3}^{5}\sqrt{u}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}{\int }_{3}^{5}{u}^{1/2}\,\text{d}u \\  & =\frac{1}{4}\cdot \frac{2}{3}{u}^{3/2}\,{|}_{3}^{5} \\  & =\frac{1}{6}({5}^{3/2}-{3}^{3/2}) \\  & =\frac{5\sqrt{5}-3\sqrt{3}}{6}\end{aligned}
$$

### Generated opaque bank scale variant (evidence only)

Evaluate the line integral ${\int }_{C}2\left(\frac{y+z}{x}\right)\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k$
for $1<t<\sqrt{2}.$

- $2\left(5\sqrt{5}-3\sqrt{3}\right)$
- $2\left(\frac{\sqrt{5}+3}{2}\right)$
- $2\left(\frac{\sqrt{5}+\sqrt{3}}{3}\right)$
- $2\left(\frac{5\sqrt{5}-3\sqrt{3}}{6}\right)$
- $2\left(\sqrt{5}+\sqrt{3}\right)$

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k,$ then along the curve we have $x=t,$ $y=\frac{{t}^{2}}{2},$ and $z=\frac{{t}^{2}}{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,k \\  & =i+t\,j+t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{t}^{2}+{t}^{2}} \\  & =\sqrt{1+2{t}^{2}}\end{aligned}
$$

Now, if $f(x,y)=2\left(\frac{y+z}{x}\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =2\left(\frac{\frac{{t}^{2}}{2}+\frac{{t}^{2}}{2}}{t}\right)=2\left(t\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{y+z}{x}\,\text{d}s & ={\int }_{1}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & =2\left({\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t\right).\end{aligned}
$$

We can solve this using the substitution $u=1+2{t}^{2}$, $\text{d}u=4t\,\text{d}t$ as follows: 

$$
\begin{aligned}2\left({\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t \right)& =2\left({\int }_{3}^{5}\sqrt{u}\cdot \frac{1}{4}\,\text{d}u \right)\\  & =2\left(\frac{1}{4}{\int }_{3}^{5}{u}^{1/2}\,\text{d}u \right)\\  & =2\left(\frac{1}{4}\cdot \frac{2}{3}{u}^{3/2}\,{|}_{3}^{5} \right)\\  & =2\left(\frac{1}{6}({5}^{3/2}-{3}^{3/2}) \right)\\  & =2\left(\frac{5\sqrt{5}-3\sqrt{3}}{6}\right)\end{aligned}
$$

## Generated easy / parabola_easy (authored bank)

Evaluate the line integral of the function $f(x,y)=9 y$ along the curve parametrized by $r(t)=\langle t^{2},t\rangle$ for $t\in [0,\sqrt{2}].$

- $9$
- $\frac{9}{2}$
- $156$
- $\frac{39}{2}$
- $21$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t^{2})\,i+(t)\,j$, then along the curve we have $x=t^{2}$, $y=t$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =(2 t)\,i+(1)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(2 t)^2+(1)^2} \\  & =\sqrt{4 t^{2} + 1}\end{aligned}
$$

Now, since $f(x,y)=9 y$, we obtain

$$
\begin{aligned}f(r(t)) & =(9)(t) \\  & =9 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\sqrt{2}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\sqrt{2}}(9 t)(\sqrt{4 t^{2} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 t^{2} + 1$, $\text{d}u=(8 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\sqrt{2}}9 t \sqrt{4 t^{2} + 1}\,\text{d}t & ={\int }_{1}^{9}\frac{9}{8}\cdot u^{1/2}\,\text{d}u \\  & =\frac{9}{8}\cdot\frac{2}{3}u^{3/2}\big|_{1}^{9} \\  & =\frac{3}{4}[(9)^{3/2}-(1)^{3/2}] \\  & =\frac{3}{4}[(27)-(1)] \\  & =(\frac{81}{4})-(\frac{3}{4}) \\  & =\frac{39}{2}\end{aligned}
$$

## Generated easy / parabola_easy (authored bank)

Evaluate the line integral of the function $f(x,y)=3 y$ along the curve parametrized by $r(t)=\langle t^{2},t\rangle$ for $t\in [0,2 \sqrt{3}].$

- $\frac{9}{2}$
- $86$
- $684$
- $\frac{171}{2}$
- $18$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t^{2})\,i+(t)\,j$, then along the curve we have $x=t^{2}$, $y=t$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =(2 t)\,i+(1)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(2 t)^2+(1)^2} \\  & =\sqrt{4 t^{2} + 1}\end{aligned}
$$

Now, since $f(x,y)=3 y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3)(t) \\  & =3 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{2 \sqrt{3}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{2 \sqrt{3}}(3 t)(\sqrt{4 t^{2} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 t^{2} + 1$, $\text{d}u=(8 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{2 \sqrt{3}}3 t \sqrt{4 t^{2} + 1}\,\text{d}t & ={\int }_{1}^{49}\frac{3}{8}\cdot u^{1/2}\,\text{d}u \\  & =\frac{3}{8}\cdot\frac{2}{3}u^{3/2}\big|_{1}^{49} \\  & =\frac{1}{4}[(49)^{3/2}-(1)^{3/2}] \\  & =\frac{1}{4}[(343)-(1)] \\  & =(\frac{343}{4})-(\frac{1}{4}) \\  & =\frac{171}{2}\end{aligned}
$$

## Generated moderate / ratio (authored bank)

Evaluate the line integral of the function $f(x,y)=\frac{12 x}{y + 2}$ along the curve parametrized by $r(t)=\langle 3 t^{2},t - 2\rangle$ for $t\in [\frac{\sqrt{2}}{3},\frac{2 \sqrt{3}}{3}].$

- $20$
- $4$
- $7584$
- $\frac{316}{3}$
- $\frac{370}{3}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(3 t^{2})\,i+(t - 2)\,j$, then along the curve we have $x=3 t^{2}$, $y=t - 2$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t^{2})\,i+\frac{\text{d}}{\text{d}t}(t - 2)\,j \\  & =(6 t)\,i+(1)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(6 t)^2+(1)^2} \\  & =\sqrt{36 t^{2} + 1}\end{aligned}
$$

Now, since $f(x,y)=\frac{12 x}{y + 2}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{12(3 t^{2})}{(t - 2)-(-2)} \\  & =\frac{36t^2}{t} \\  & =36 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{\frac{\sqrt{2}}{3}}^{\frac{2 \sqrt{3}}{3}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{\frac{\sqrt{2}}{3}}^{\frac{2 \sqrt{3}}{3}}(36 t)(\sqrt{36 t^{2} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=36 t^{2} + 1$, $\text{d}u=(72 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\frac{\sqrt{2}}{3}}^{\frac{2 \sqrt{3}}{3}}36 t \sqrt{36 t^{2} + 1}\,\text{d}t & ={\int }_{9}^{49}\frac{1}{2}\cdot u^{1/2}\,\text{d}u \\  & =\frac{1}{2}\cdot\frac{2}{3}u^{3/2}\big|_{9}^{49} \\  & =\frac{1}{3}[(49)^{3/2}-(9)^{3/2}] \\  & =\frac{1}{3}[(343)-(27)] \\  & =(\frac{343}{3})-(9) \\  & =\frac{316}{3}\end{aligned}
$$

## Generated moderate / ratio (authored bank)

Evaluate the line integral of the function $f(x,y)=\frac{10 x}{y - 1}$ along the curve parametrized by $r(t)=\langle t^{2},t + 1\rangle$ for $t\in [\sqrt{6},2 \sqrt{3}].$

- $5$
- $390$
- $\frac{4360}{3}$
- $\frac{545}{3}$
- $30$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t^{2})\,i+(t + 1)\,j$, then along the curve we have $x=t^{2}$, $y=t + 1$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(t + 1)\,j \\  & =(2 t)\,i+(1)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(2 t)^2+(1)^2} \\  & =\sqrt{4 t^{2} + 1}\end{aligned}
$$

Now, since $f(x,y)=\frac{10 x}{y - 1}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{10(t^{2})}{(t + 1)-(1)} \\  & =\frac{10t^2}{t} \\  & =10 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{\sqrt{6}}^{2 \sqrt{3}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{\sqrt{6}}^{2 \sqrt{3}}(10 t)(\sqrt{4 t^{2} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 t^{2} + 1$, $\text{d}u=(8 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\sqrt{6}}^{2 \sqrt{3}}10 t \sqrt{4 t^{2} + 1}\,\text{d}t & ={\int }_{25}^{49}\frac{5}{4}\cdot u^{1/2}\,\text{d}u \\  & =\frac{5}{4}\cdot\frac{2}{3}u^{3/2}\big|_{25}^{49} \\  & =\frac{5}{6}[(49)^{3/2}-(25)^{3/2}] \\  & =\frac{5}{6}[(343)-(125)] \\  & =(\frac{1715}{6})-(\frac{625}{6}) \\  & =\frac{545}{3}\end{aligned}
$$

## Generated moderate / cubic (authored bank)

Evaluate the line integral of the function $f(x,y)=x^{3} + 4 y$ along the curve parametrized by $r(t)=\langle 6 t,2 t^{3}\rangle$ for $t\in [0,1].$

- $56$
- $-672 + 672 \sqrt{2}$
- $-896 + 1792 \sqrt{2}$
- $-224 + 448 \sqrt{2}$
- $224 + 448 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(6 t)\,i+(2 t^{3})\,j$, then along the curve we have $x=6 t$, $y=2 t^{3}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(6 t)\,i+\frac{\text{d}}{\text{d}t}(2 t^{3})\,j \\  & =(6)\,i+(6 t^{2})\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(6)^2+(6 t^{2})^2} \\  & =\sqrt{36 t^{4} + 36}\end{aligned}
$$

Now, since $f(x,y)=x^{3} + 4 y$, we obtain

$$
\begin{aligned}f(r(t)) & =(6 t)^3+(4)(2 t^{3}) \\  & =216t^3+8t^3 \\  & =224 t^{3}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{1}(224 t^{3})(\sqrt{36 t^{4} + 36})\,\text{d}t \\  & ={\int }_{0}^{1}1344 t^{3} \sqrt{t^{4} + 1}\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{4} + 1$, $\text{d}u=(4 t^{3})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{1}1344 t^{3} \sqrt{t^{4} + 1}\,\text{d}t & ={\int }_{1}^{2}336\cdot u^{1/2}\,\text{d}u \\  & =336\cdot\frac{2}{3}u^{3/2}\big|_{1}^{2} \\  & =224[(2)^{3/2}-(1)^{3/2}] \\  & =224[(2 \sqrt{2})-(1)] \\  & =(448 \sqrt{2})-(224) \\  & =-224 + 448 \sqrt{2}\end{aligned}
$$

## Generated moderate / cubic (authored bank)

Evaluate the line integral of the function $f(x,y)=x^{3} + 3 y$ along the curve parametrized by $r(t)=\langle 3 t,t^{3}\rangle$ for $t\in [0,\sqrt[4]{3}].$

- $45$
- $135$
- $420$
- $105$
- $\frac{45}{2}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(3 t)\,i+(t^{3})\,j$, then along the curve we have $x=3 t$, $y=t^{3}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(t^{3})\,j \\  & =(3)\,i+(3 t^{2})\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(3)^2+(3 t^{2})^2} \\  & =\sqrt{9 t^{4} + 9}\end{aligned}
$$

Now, since $f(x,y)=x^{3} + 3 y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3 t)^3+(3)(t^{3}) \\  & =27t^3+3t^3 \\  & =30 t^{3}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\sqrt[4]{3}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\sqrt[4]{3}}(30 t^{3})(\sqrt{9 t^{4} + 9})\,\text{d}t \\  & ={\int }_{0}^{\sqrt[4]{3}}90 t^{3} \sqrt{t^{4} + 1}\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{4} + 1$, $\text{d}u=(4 t^{3})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\sqrt[4]{3}}90 t^{3} \sqrt{t^{4} + 1}\,\text{d}t & ={\int }_{1}^{4}\frac{45}{2}\cdot u^{1/2}\,\text{d}u \\  & =\frac{45}{2}\cdot\frac{2}{3}u^{3/2}\big|_{1}^{4} \\  & =15[(4)^{3/2}-(1)^{3/2}] \\  & =15[(8)-(1)] \\  & =(120)-(15) \\  & =105\end{aligned}
$$

## Generated moderate / cos_diagonal (authored bank)

Evaluate the line integral of the function $f(x,y)=6 \cos{\left(x \right)}$ along the curve parametrized by $r(t)=\langle 3 t^{2},- 2 t^{2}\rangle$ for $t\in [0,\frac{\sqrt{2} \sqrt{\pi}}{6}].$

- $1$
- $2 \sqrt{13} \left(-1 + \frac{\sqrt{3}}{2}\right)$
- $6 \sqrt{13}$
- $\sqrt{13}$
- $2 \sqrt{13} \sin{\left(\frac{\sqrt{2} \sqrt{\pi}}{6} \right)}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(3 t^{2})\,i+(- 2 t^{2})\,j$, then along the curve we have $x=3 t^{2}$, $y=- 2 t^{2}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t^{2})\,i+\frac{\text{d}}{\text{d}t}(- 2 t^{2})\,j \\  & =(6 t)\,i+(- 4 t)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(6 t)^2+(- 4 t)^2} \\  & =\sqrt{52 t^{2}} \\  & =2 \sqrt{13}|t| \\  & =2 \sqrt{13} t\end{aligned}
$$

Notice that $|t|=t$ because $t\geq0$ along the path of $C.$

Now, since $f(x,y)=6 \cos{\left(x \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =6 \cos{\left(3 t^{2} \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}}(6 \cos{\left(3 t^{2} \right)})(2 \sqrt{13} t)\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=3 t^{2}$, $\text{d}u=(6 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}}12 \sqrt{13} t \cos{\left(3 t^{2} \right)}\,\text{d}t & ={\int }_{0}^{\frac{\pi}{6}}2 \sqrt{13}\cdot \cos u\,\text{d}u \\  & =2 \sqrt{13}\sin u\big|_{0}^{\frac{\pi}{6}} \\  & =2 \sqrt{13}[\sin(\frac{\pi}{6})-\sin(0)] \\  & =2 \sqrt{13}[(\frac{1}{2})-(0)] \\  & =(\sqrt{13})-(0) \\  & =\sqrt{13}\end{aligned}
$$

## Generated moderate / cos_diagonal (authored bank)

Evaluate the line integral of the function $f(x,y)=5 \cos{\left(x \right)}$ along the curve parametrized by $r(t)=\langle t^{2},- t^{2}\rangle$ for $t\in [0,\frac{\sqrt{6} \sqrt{\pi}}{6}].$

- $5 \sqrt{2} \left(-1 + \frac{\sqrt{3}}{2}\right)$
- $5 \sqrt{2} \sin{\left(\frac{\sqrt{6} \sqrt{\pi}}{6} \right)}$
- $5 \sqrt{2}$
- $\frac{5 \sqrt{2}}{2}$
- $0$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t^{2})\,i+(- t^{2})\,j$, then along the curve we have $x=t^{2}$, $y=- t^{2}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(- t^{2})\,j \\  & =(2 t)\,i+(- 2 t)\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(2 t)^2+(- 2 t)^2} \\  & =\sqrt{8 t^{2}} \\  & =2 \sqrt{2}|t| \\  & =2 \sqrt{2} t\end{aligned}
$$

Notice that $|t|=t$ because $t\geq0$ along the path of $C.$

Now, since $f(x,y)=5 \cos{\left(x \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =5 \cos{\left(t^{2} \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}}(5 \cos{\left(t^{2} \right)})(2 \sqrt{2} t)\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=t^{2}$, $\text{d}u=(2 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}}10 \sqrt{2} t \cos{\left(t^{2} \right)}\,\text{d}t & ={\int }_{0}^{\frac{\pi}{6}}5 \sqrt{2}\cdot \cos u\,\text{d}u \\  & =5 \sqrt{2}\sin u\big|_{0}^{\frac{\pi}{6}} \\  & =5 \sqrt{2}[\sin(\frac{\pi}{6})-\sin(0)] \\  & =5 \sqrt{2}[(\frac{1}{2})-(0)] \\  & =(\frac{5 \sqrt{2}}{2})-(0) \\  & =\frac{5 \sqrt{2}}{2}\end{aligned}
$$

## Generated moderate / sine_line (authored bank)

Evaluate the line integral of the function $f(x,y)=\frac{x^{2}}{2} + \frac{y^{2}}{2}$ along the curve parametrized by $r(t)=\langle 15 \sin{\left(t \right)},- 8 \sin{\left(t \right)}\rangle$ for $t\in [0,\frac{\pi}{2}].$

- $\frac{4913}{4}$
- $\frac{83521 \pi}{32}$
- $\frac{289}{6}$
- $\frac{4913}{6}$
- $\frac{4913}{2}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(15 \sin{\left(t \right)})\,i+(- 8 \sin{\left(t \right)})\,j$, then along the curve we have $x=15 \sin{\left(t \right)}$, $y=- 8 \sin{\left(t \right)}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(15 \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(- 8 \sin{\left(t \right)})\,j \\  & =(15 \cos{\left(t \right)})\,i+(- 8 \cos{\left(t \right)})\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(15 \cos{\left(t \right)})^2+(- 8 \cos{\left(t \right)})^2} \\  & =\sqrt{225\cos^2 t+64\cos^2 t} \\  & =\sqrt{289 \cos^{2}{\left(t \right)}} \\  & =17|\cos t| \\  & =17 \cos{\left(t \right)}\end{aligned}
$$

Notice that $|\cos t|=\cos t$ because $\cos t\geq0$ along this interval.

Now, since $f(x,y)=\frac{x^{2}}{2} + \frac{y^{2}}{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(15 \sin{\left(t \right)})^2+(- 8 \sin{\left(t \right)})^2}{2} \\  & =\frac{225\sin^2 t+64\sin^2 t}{2} \\  & =\frac{289 \sin^{2}{\left(t \right)}}{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\pi}{2}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}(\frac{289 \sin^{2}{\left(t \right)}}{2})(17 \cos{\left(t \right)})\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}\frac{4913 \sin^{2}{\left(t \right)} \cos{\left(t \right)}}{2}\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=\sin{\left(t \right)}$, $\text{d}u=(\cos{\left(t \right)})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\pi}{2}}\frac{4913 \sin^{2}{\left(t \right)} \cos{\left(t \right)}}{2}\,\text{d}t & ={\int }_{0}^{1}\frac{4913}{2}\cdot u^2\,\text{d}u \\  & =\frac{4913}{2}\cdot\frac{u^3}{3}\big|_{0}^{1} \\  & =\frac{4913}{2}[\frac{(1)^3}{3}-\frac{(0)^3}{3}] \\  & =\frac{4913}{2}[(\frac{1}{3})-(0)] \\  & =(\frac{4913}{6})-(0) \\  & =\frac{4913}{6}\end{aligned}
$$

## Generated moderate / sine_line (authored bank)

Evaluate the line integral of the function $f(x,y)=\frac{x^{2}}{6} + \frac{y^{2}}{6}$ along the curve parametrized by $r(t)=\langle 3 \sin{\left(t \right)},- 4 \sin{\left(t \right)}\rangle$ for $t\in [0,\frac{\pi}{2}].$

- $\frac{625 \pi}{96}$
- $\frac{125}{6}$
- $\frac{25}{18}$
- $\frac{125}{18}$
- $\frac{125}{12}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(3 \sin{\left(t \right)})\,i+(- 4 \sin{\left(t \right)})\,j$, then along the curve we have $x=3 \sin{\left(t \right)}$, $y=- 4 \sin{\left(t \right)}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(- 4 \sin{\left(t \right)})\,j \\  & =(3 \cos{\left(t \right)})\,i+(- 4 \cos{\left(t \right)})\,j \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\  & =\sqrt{(3 \cos{\left(t \right)})^2+(- 4 \cos{\left(t \right)})^2} \\  & =\sqrt{9\cos^2 t+16\cos^2 t} \\  & =\sqrt{25 \cos^{2}{\left(t \right)}} \\  & =5|\cos t| \\  & =5 \cos{\left(t \right)}\end{aligned}
$$

Notice that $|\cos t|=\cos t$ because $\cos t\geq0$ along this interval.

Now, since $f(x,y)=\frac{x^{2}}{6} + \frac{y^{2}}{6}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(3 \sin{\left(t \right)})^2+(- 4 \sin{\left(t \right)})^2}{6} \\  & =\frac{9\sin^2 t+16\sin^2 t}{6} \\  & =\frac{25 \sin^{2}{\left(t \right)}}{6}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\pi}{2}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}(\frac{25 \sin^{2}{\left(t \right)}}{6})(5 \cos{\left(t \right)})\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}\frac{125 \sin^{2}{\left(t \right)} \cos{\left(t \right)}}{6}\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=\sin{\left(t \right)}$, $\text{d}u=(\cos{\left(t \right)})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\pi}{2}}\frac{125 \sin^{2}{\left(t \right)} \cos{\left(t \right)}}{6}\,\text{d}t & ={\int }_{0}^{1}\frac{125}{6}\cdot u^2\,\text{d}u \\  & =\frac{125}{6}\cdot\frac{u^3}{3}\big|_{0}^{1} \\  & =\frac{125}{6}[\frac{(1)^3}{3}-\frac{(0)^3}{3}] \\  & =\frac{125}{6}[(\frac{1}{3})-(0)] \\  & =(\frac{125}{18})-(0) \\  & =\frac{125}{18}\end{aligned}
$$

## Generated moderate / sin_cos (authored bank)

Evaluate the line integral of the function $f(x,y,z)=y z \cos{\left(x \right)}$ along the curve parametrized by $r(t)=\langle t,2 \sin{\left(t \right)},2\rangle$ for $t\in [0,\frac{\pi}{2}].$

- $-1 + \sqrt{5}$
- $6$
- $2$
- $- \frac{1}{3} + \frac{5 \sqrt{5}}{3}$
- $\frac{8}{3} - \frac{40 \sqrt{5}}{3}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t)\,i+(2 \sin{\left(t \right)})\,j+(2)\,k$, then along the curve we have $x=t$, $y=2 \sin{\left(t \right)}$, $z=2$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\,j+\frac{\text{d}}{\text{d}t}(2)\,k \\  & =(1)\,i+(2 \cos{\left(t \right)})\,j+(0)\,k \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2+(\frac{\text{d}z}{\text{d}t})^2} \\  & =\sqrt{(1)^2+(2 \cos{\left(t \right)})^2+(0)^2} \\  & =\sqrt{4 \cos^{2}{\left(t \right)} + 1}\end{aligned}
$$

The substitution decreases from $5$ to $1$; its differential includes the negative sign.

Now, since $f(x,y,z)=y z \cos{\left(x \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =(1)(2 \sin{\left(t \right)})(2)\cos(t) \\  & =2 \sin{\left(2 t \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\pi}{2}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}(2 \sin{\left(2 t \right)})(\sqrt{4 \cos^{2}{\left(t \right)} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=4 \cos^{2}{\left(t \right)} + 1$, $\text{d}u=(- 8 \sin{\left(t \right)} \cos{\left(t \right)})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\pi}{2}}2 \sqrt{4 \cos^{2}{\left(t \right)} + 1} \sin{\left(2 t \right)}\,\text{d}t & ={\int }_{5}^{1}- \frac{1}{2}\cdot u^{1/2}\,\text{d}u \\  & =- \frac{1}{2}\cdot\frac{2}{3}u^{3/2}\big|_{5}^{1} \\  & =- \frac{1}{3}[(1)^{3/2}-(5)^{3/2}] \\  & =- \frac{1}{3}[(1)-(5 \sqrt{5})] \\  & =(- \frac{1}{3})-(- \frac{5 \sqrt{5}}{3}) \\  & =- \frac{1}{3} + \frac{5 \sqrt{5}}{3}\end{aligned}
$$

## Generated moderate / sin_cos (authored bank)

Evaluate the line integral of the function $f(x,y,z)=3 y z \cos{\left(x \right)}$ along the curve parametrized by $r(t)=\langle t,\sin{\left(t \right)},2\rangle$ for $t\in [0,\frac{\pi}{2}].$

- $\frac{9}{2}$
- $4 - 8 \sqrt{2}$
- $3$
- $-2 + 4 \sqrt{2}$
- $-6 + 6 \sqrt{2}$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t)\,i+(\sin{\left(t \right)})\,j+(2)\,k$, then along the curve we have $x=t$, $y=\sin{\left(t \right)}$, $z=2$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,j+\frac{\text{d}}{\text{d}t}(2)\,k \\  & =(1)\,i+(\cos{\left(t \right)})\,j+(0)\,k \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2+(\frac{\text{d}z}{\text{d}t})^2} \\  & =\sqrt{(1)^2+(\cos{\left(t \right)})^2+(0)^2} \\  & =\sqrt{\cos^{2}{\left(t \right)} + 1}\end{aligned}
$$

The substitution decreases from $2$ to $1$; its differential includes the negative sign.

Now, since $f(x,y,z)=3 y z \cos{\left(x \right)}$, we obtain

$$
\begin{aligned}f(r(t)) & =(3)(\sin{\left(t \right)})(2)\cos(t) \\  & =3 \sin{\left(2 t \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{0}^{\frac{\pi}{2}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{0}^{\frac{\pi}{2}}(3 \sin{\left(2 t \right)})(\sqrt{\cos^{2}{\left(t \right)} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=\cos^{2}{\left(t \right)} + 1$, $\text{d}u=(- 2 \sin{\left(t \right)} \cos{\left(t \right)})\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\frac{\pi}{2}}3 \sqrt{\cos^{2}{\left(t \right)} + 1} \sin{\left(2 t \right)}\,\text{d}t & ={\int }_{2}^{1}-3\cdot u^{1/2}\,\text{d}u \\  & =-3\cdot\frac{2}{3}u^{3/2}\big|_{2}^{1} \\  & =-2[(1)^{3/2}-(2)^{3/2}] \\  & =-2[(1)-(2 \sqrt{2})] \\  & =(-2)-(- 4 \sqrt{2}) \\  & =-2 + 4 \sqrt{2}\end{aligned}
$$

## Generated hard / space_ratio (authored bank)

Evaluate the line integral of the function $f(x,y,z)=\frac{y + z}{x}$ along the curve parametrized by $r(t)=\langle 2 t,t^{2},t^{2}\rangle$ for $t\in [\sqrt{3},2].$

- $\frac{1}{2}$
- $\frac{3}{4} - \frac{\sqrt{7}}{4}$
- $144 - \frac{112 \sqrt{7}}{3}$
- $9 - \frac{7 \sqrt{7}}{3}$
- $\frac{7 \sqrt{7}}{3} + 9$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(2 t)\,i+(t^{2})\,j+(t^{2})\,k$, then along the curve we have $x=2 t$, $y=t^{2}$, $z=t^{2}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2 t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j+\frac{\text{d}}{\text{d}t}(t^{2})\,k \\  & =(2)\,i+(2 t)\,j+(2 t)\,k \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2+(\frac{\text{d}z}{\text{d}t})^2} \\  & =\sqrt{(2)^2+(2 t)^2+(2 t)^2} \\  & =\sqrt{8 t^{2} + 4}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{y + z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(1)[(t^{2})+(t^{2})]}{2 t} \\  & =\frac{(2)t^2}{(2)t} \\  & =t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{\sqrt{3}}^{2}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{\sqrt{3}}^{2}(t)(\sqrt{8 t^{2} + 4})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=8 t^{2} + 4$, $\text{d}u=(16 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\sqrt{3}}^{2}2 t \sqrt{2 t^{2} + 1}\,\text{d}t & ={\int }_{28}^{36}\sqrt{u}\cdot \frac{1}{16}\,\text{d}u \\  & =\frac{1}{16}{\int }_{28}^{36}u^{1/2}\,\text{d}u \\  & =\frac{1}{16}\cdot\frac{2}{3}u^{3/2}\big|_{28}^{36} \\  & =\frac{1}{24}[(36)^{3/2}-(28)^{3/2}] \\  & =\frac{1}{24}[(216)-(56 \sqrt{7})] \\  & =(9)-(\frac{7 \sqrt{7}}{3}) \\  & =9 - \frac{7 \sqrt{7}}{3}\end{aligned}
$$

## Generated hard / space_ratio (authored bank)

Evaluate the line integral of the function $f(x,y,z)=\frac{4 y + 4 z}{x}$ along the curve parametrized by $r(t)=\langle t,t^{2},t^{2}\rangle$ for $t\in [\sqrt{2},\sqrt{3}].$

- $5 - \sqrt{17}$
- $\frac{17 \sqrt{17}}{3} + \frac{125}{3}$
- $\frac{2000}{3} - \frac{272 \sqrt{17}}{3}$
- $\frac{125}{3} - \frac{17 \sqrt{17}}{3}$
- $4$

To calculate the line integral, we will use the formula

$$
\begin{aligned}\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t.\end{aligned}
$$

Since $r(t)=(t)\,i+(t^{2})\,j+(t^{2})\,k$, then along the curve we have $x=t$, $y=t^{2}$, $z=t^{2}$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j+\frac{\text{d}}{\text{d}t}(t^{2})\,k \\  & =(1)\,i+(2 t)\,j+(2 t)\,k \\ \|r'(t)\| & =\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2+(\frac{\text{d}z}{\text{d}t})^2} \\  & =\sqrt{(1)^2+(2 t)^2+(2 t)^2} \\  & =\sqrt{8 t^{2} + 1}\end{aligned}
$$

Now, since $f(x,y,z)=\frac{4 y + 4 z}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(4)[(t^{2})+(t^{2})]}{t} \\  & =\frac{(8)t^2}{(1)t} \\  & =8 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f\,\text{d}s & ={\int }_{\sqrt{2}}^{\sqrt{3}}f(r(t))\,\|r'(t)\|\,\text{d}t \\  & ={\int }_{\sqrt{2}}^{\sqrt{3}}(8 t)(\sqrt{8 t^{2} + 1})\,\text{d}t\end{aligned}
$$

We can solve this using the substitution $u=8 t^{2} + 1$, $\text{d}u=(16 t)\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\sqrt{2}}^{\sqrt{3}}8 t \sqrt{8 t^{2} + 1}\,\text{d}t & ={\int }_{17}^{25}\sqrt{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}{\int }_{17}^{25}u^{1/2}\,\text{d}u \\  & =\frac{1}{2}\cdot\frac{2}{3}u^{3/2}\big|_{17}^{25} \\  & =\frac{1}{3}[(25)^{3/2}-(17)^{3/2}] \\  & =\frac{1}{3}[(125)-(17 \sqrt{17})] \\  & =(\frac{125}{3})-(\frac{17 \sqrt{17}}{3}) \\  & =\frac{125}{3} - \frac{17 \sqrt{17}}{3}\end{aligned}
$$
