# Original and generated review



Observed raw homogeneous profiles are evidence-only. Method profiles are authored complete banks. Easy/hard level labels are authored.



## Original — log / q-124694



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)={e}^{x}\,i+2y\,j$ and $C$ is the path $r(t)=\operatorname{ln}⁡t\,i+t\,j$ for $t\in [1,2].$



Bank: $4$ **correct**, $2$, $3$, $1$, $0$



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{ln}⁡t,\,y=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & ={e}^{x}\,i+2y\,j \\  & ={e}^{\operatorname{ln}⁡t}\,i+2t\,j \\  & =t\,i+2t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{t}\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\,i+2t\,j)\cdot (\frac{1}{t}\,i+j) \\  & =1+2t.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{1}^{2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{1}^{2}1+2t\,dt \\  & ={[t+{t}^{2}]}_{1}^{2} \\  & =[2+4-(1+1)] \\  & =4\end{aligned}
$$



## Original — polynomial / q-39340



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)={x}^{2}y\,i+(x+1)\,j$ and $C$ is the path $r(t)=3t\,i+(2+t)\,j$ for $t\in [0,1].$



Bank: $\frac{55}{4}$, $\frac{27}{4}$, $\frac{35}{4}$, $\frac{89}{4}$, $\frac{109}{4}$ **correct**



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=3t,\,y=2+t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & ={x}^{2}y\,i+(x+1)\,j \\  & =(3t)^{2}(2+t)\,i+(3t+1)\,j \\  & =9{t}^{2}(2+t)\,i+(3t+1)\,j \\  & =(18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)i+\frac{\text{d}}{\text{d}t}(2+t)j \\  & =3\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j)\cdot (3\,i+j) \\  & =54{t}^{2}+27{t}^{3}+3t+1.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}54{t}^{2}+27{t}^{3}+3t+1\,dt \\  & ={[18{t}^{3}+\frac{27}{4}{t}^{4}+\frac{3}{2}{t}^{2}+t]}_{0}^{1} \\  & =(18+\frac{27}{4}+\frac{3}{2}+1)-0 \\  & =\frac{109}{4}\end{aligned}
$$



## Original — offset_circle / q-124688



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)=x\,i+(y-1)\,j$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$



Bank: $-1$, $0$, $2$ **correct**, $-2$, $1$



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+(y-1)\,j \\  & =\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =\operatorname{sin}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t \\  & =\operatorname{sin}⁡t.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt \\  & =-\operatorname{cos}⁡t\,{|}_{0}^{\pi } \\  & =-(-1-1) \\  & =2\end{aligned}
$$



## Original — rotation / q-124689



Evaluate${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i-x\,j$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$



Bank: $\pi $ **correct**, $2\pi $, $0$, $1$, $2$



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =\operatorname{cos}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t(-\operatorname{sin}⁡t) \\  & ={cos}^{2}⁡t+{sin}^{2}⁡t \\  & =1.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }dt \\  & =t\,{|}_{0}^{\pi } \\  & =\pi -0 \\  & =\pi \end{aligned}
$$



## Original — spiral / q-124691



Evaluate  ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+y\,j$ and $C$ is the path $r(t)=t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j$ for $t\in [0,2\pi ].$



Bank: $2$, $2{\pi }^{2}$ **correct**, $\pi $, ${\pi }^{2}$, $2\pi $



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t\operatorname{sin}⁡t,\,y=t\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+y\,j \\  & =t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(t\operatorname{cos}⁡t)j \\  & =(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j)\cdot ((\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j) \\  & =t\operatorname{sin}⁡t(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)+t\operatorname{cos}⁡t(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t{sin}^{2}⁡t+{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t+t{cos}^{2}⁡t-{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t \\  & =t({sin}^{2}⁡t+{cos}^{2}⁡t) \\  & =t.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{2\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }t\,dt \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{2\pi } \\  & =\frac{(2\pi )^{2}}{2}-0 \\  & =2{\pi }^{2}\end{aligned}
$$



## Original — parabola / q-124693



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i+x\,j$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j$ for $t\in [0,1].$



Bank: $3$, $1$ **correct**, $4$, $0$, $2$



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y={t}^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,j \\  & ={t}^{2}\,i+t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({t}^{2}\,i+t\,j)\cdot (i+2t\,j) \\  & ={t}^{2}\cdot 1+t\cdot 2t \\  & =3{t}^{2}.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}3{t}^{2}\,dt \\  & ={[{t}^{3}]}_{0}^{1} \\  & =[1-0] \\  & =1\end{aligned}
$$



## Original — rational / q-124696



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j$ and $C$ is the path $r(t)={t}^{2}\,i+(t-1)\,j$ for $t\in [3,4].$



Bank: $-7$ **correct**, $-2$, $9$, $2$, $-11$



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={t}^{2},\,y=t-1.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j \\  & =\frac{(t-1)+1}{{t}^{2}}\,i-\frac{2({t}^{2}-1)}{t-1}\,j \\  & =\frac{1}{t}\,i-2(t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j \\  & =2t\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\frac{1}{t}\,i-2(t+1)\,j)\cdot (2t\,i+j) \\  & =\frac{1}{t}\cdot 2t-2(t+1)\cdot 1 \\  & =2-2(t+1)\cdot 1 \\  & =-2t.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{3}^{4}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{3}^{4}(-2t)\,dt \\  & ={[-{t}^{2}]}_{3}^{4} \\  & =[-16+9] \\  & =-7\end{aligned}
$$



## Original — arcsine / q-39422



Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(y\operatorname{sin}⁡x)\,i+(x+y)\,j$ and $C$ is the path  $r(t)=\operatorname{arcsin}⁡t\,i+2j$ for $t\in [0,\frac{1}{2}].$



Bank: $-4-\sqrt{2}$, $\sqrt{2}$, $1-\sqrt{3}$, $-2+\sqrt{3}$, $2-\sqrt{3}$ **correct**



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{arcsin}⁡t,\,y=2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =2\operatorname{sin}⁡(\operatorname{arcsin}⁡t)\,i+(\operatorname{arcsin}⁡t+2)\,j \\  & =2t\,i+(\operatorname{arcsin}⁡t+2)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{arcsin}⁡t)i+\frac{\text{d}}{\text{d}t}(2)j \\  & =\frac{1}{\sqrt{1-{t}^{2}}}\,i.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2t\,i+(\operatorname{arcsin}⁡t+2)\,j)\cdot (\frac{1}{\sqrt{1-{t}^{2}}}\,i) \\  & =\frac{2t}{\sqrt{1-{t}^{2}}}.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1/2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1/2}\frac{2t}{\sqrt{1-{t}^{2}}}\,dt \\  & =-2\sqrt{1-{t}^{2}}\,{|}_{0}^{1/2} \\  & =-2(\sqrt{1-{(\frac{1}{2})}^{2}}-1) \\  & =2-\sqrt{3}\end{aligned}
$$



### Generated — moderate / log / observed_log

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)={e}^{x}\,i+2y\,j$ and $C$ is the path $r(t)=\operatorname{ln}⁡t\,i+t\,j$ for $t\in [1,2].$

- $3$
- $2$
- $4$ **correct**
- $0$
- $1$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{ln}⁡t,\,y=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & ={e}^{x}\,i+2y\,j \\  & ={e}^{\operatorname{ln}⁡t}\,i+2t\,j \\  & =t\,i+2t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{t}\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\,i+2t\,j)\cdot (\frac{1}{t}\,i+j) \\  & =1+2t.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{1}^{2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{1}^{2}1+2t\,dt \\  & ={[t+{t}^{2}]}_{1}^{2} \\  & =[2+4-(1+1)] \\  & =4\end{aligned}
$$

### Generated — moderate / log / observed_log

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)=(2)\left({e}^{x}\,i+2y\,j\right)$ and $C$ is the path $r(t)=\operatorname{ln}⁡t\,i+t\,j$ for $t\in [1,2].$

- $2\left(4\right)$ **correct**
- $2\left(3\right)$
- $2\left(1\right)$
- $2\left(0\right)$
- $2\left(2\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{ln}⁡t,\,y=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left({e}^{x}\,i+2y\,j\right) \\  & =(2)\left({e}^{\operatorname{ln}⁡t}\,i+2t\,j\right) \\  & =(2)\left(t\,i+2t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =\frac{1}{t}\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((t\,i+2t\,j)\right)\cdot (\frac{1}{t}\,i+j) \\  & =(2)\left(1+2t\right).\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{1}^{2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{1}^{2}1+2t\,dt\right) \\  & =(2)\left({[t+{t}^{2}]}_{1}^{2}\right) \\  & =(2)\left([2+4-(1+1)]\right) \\  & =(2)\left(4\right)\end{aligned}
$$

### Generated — moderate / polynomial / observed_polynomial

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)={x}^{2}y\,i+(x+1)\,j$ and $C$ is the path $r(t)=3t\,i+(2+t)\,j$ for $t\in [0,1].$

- $\frac{35}{4}$
- $\frac{27}{4}$
- $\frac{55}{4}$
- $\frac{109}{4}$ **correct**
- $\frac{89}{4}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=3t,\,y=2+t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & ={x}^{2}y\,i+(x+1)\,j \\  & =(3t)^{2}(2+t)\,i+(3t+1)\,j \\  & =9{t}^{2}(2+t)\,i+(3t+1)\,j \\  & =(18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)i+\frac{\text{d}}{\text{d}t}(2+t)j \\  & =3\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j)\cdot (3\,i+j) \\  & =54{t}^{2}+27{t}^{3}+3t+1.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}54{t}^{2}+27{t}^{3}+3t+1\,dt \\  & ={[18{t}^{3}+\frac{27}{4}{t}^{4}+\frac{3}{2}{t}^{2}+t]}_{0}^{1} \\  & =(18+\frac{27}{4}+\frac{3}{2}+1)-0 \\  & =\frac{109}{4}\end{aligned}
$$

### Generated — moderate / polynomial / observed_polynomial

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left({x}^{2}y\,i+(x+1)\,j\right)$ and $C$ is the path $r(t)=3t\,i+(2+t)\,j$ for $t\in [0,1].$

- $2\left(\frac{55}{4}\right)$
- $2\left(\frac{35}{4}\right)$
- $2\left(\frac{89}{4}\right)$
- $2\left(\frac{109}{4}\right)$ **correct**
- $2\left(\frac{27}{4}\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=3t,\,y=2+t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left({x}^{2}y\,i+(x+1)\,j\right) \\  & =(2)\left((3t)^{2}(2+t)\,i+(3t+1)\,j\right) \\  & =(2)\left(9{t}^{2}(2+t)\,i+(3t+1)\,j\right) \\  & =(2)\left((18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)i+\frac{\text{d}}{\text{d}t}(2+t)j \\  & =3\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left(((18{t}^{2}+9{t}^{3})\,i+(3t+1)\,j)\right)\cdot (3\,i+j) \\  & =(2)\left(54{t}^{2}+27{t}^{3}+3t+1\right).\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{1}54{t}^{2}+27{t}^{3}+3t+1\,dt\right) \\  & =(2)\left({[18{t}^{3}+\frac{27}{4}{t}^{4}+\frac{3}{2}{t}^{2}+t]}_{0}^{1}\right) \\  & =(2)\left((18+\frac{27}{4}+\frac{3}{2}+1)-0\right) \\  & =(2)\left(\frac{109}{4}\right)\end{aligned}
$$

### Generated — moderate / offset_circle / observed_offset_circle

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)=x\,i+(y-1)\,j$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$

- $2$ **correct**
- $0$
- $-1$
- $1$
- $-2$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+(y-1)\,j \\  & =\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =\operatorname{sin}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t \\  & =\operatorname{sin}⁡t.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt \\  & =-\operatorname{cos}⁡t\,{|}_{0}^{\pi } \\  & =-(-1-1) \\  & =2\end{aligned}
$$

### Generated — moderate / offset_circle / observed_offset_circle

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that  $F(x,y)=(2)\left(x\,i+(y-1)\,j\right)$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$

- $2\left(-1\right)$
- $2\left(2\right)$ **correct**
- $2\left(-2\right)$
- $2\left(1\right)$
- $2\left(0\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(x\,i+(y-1)\,j\right) \\  & =(2)\left(\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((\operatorname{sin}⁡t\,i+(\operatorname{cos}⁡t-1)\,j)\right)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =(2)\left(\operatorname{sin}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{sin}⁡t\right) \\  & =(2)\left(\operatorname{sin}⁡t\right).\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt\right) \\  & =(2)\left(-\operatorname{cos}⁡t\,{|}_{0}^{\pi }\right) \\  & =(2)\left(-(-1-1)\right) \\  & =(2)\left(2\right)\end{aligned}
$$

### Generated — moderate / rotation / observed_rotation

Evaluate${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i-x\,j$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$

- $0$
- $2\pi $
- $\pi $ **correct**
- $2$
- $1$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =\operatorname{cos}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t(-\operatorname{sin}⁡t) \\  & ={cos}^{2}⁡t+{sin}^{2}⁡t \\  & =1.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }dt \\  & =t\,{|}_{0}^{\pi } \\  & =\pi -0 \\  & =\pi \end{aligned}
$$

### Generated — moderate / rotation / observed_rotation

Evaluate${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left(y\,i-x\,j\right)$ and $C$ is the path $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j$ for $t\in [0,\pi ].$

- $2\left(\pi \right)$ **correct**
- $2\left(0\right)$
- $2\left(1\right)$
- $2\left(2\right)$
- $2\left(2\pi \right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(y\,i-x\,j\right) \\  & =(2)\left(\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j)\right)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j) \\  & =(2)\left(\operatorname{cos}⁡t\operatorname{cos}⁡t-\operatorname{sin}⁡t(-\operatorname{sin}⁡t)\right) \\  & =(2)\left({cos}^{2}⁡t+{sin}^{2}⁡t\right) \\  & =(2)\left(1\right).\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{\pi }dt\right) \\  & =(2)\left(t\,{|}_{0}^{\pi }\right) \\  & =(2)\left(\pi -0\right) \\  & =(2)\left(\pi \right)\end{aligned}
$$

### Generated — moderate / spiral / observed_spiral

Evaluate  ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+y\,j$ and $C$ is the path $r(t)=t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j$ for $t\in [0,2\pi ].$

- $\pi $
- $2{\pi }^{2}$ **correct**
- $2$
- $2\pi $
- ${\pi }^{2}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t\operatorname{sin}⁡t,\,y=t\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+y\,j \\  & =t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(t\operatorname{cos}⁡t)j \\  & =(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j)\cdot ((\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j) \\  & =t\operatorname{sin}⁡t(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)+t\operatorname{cos}⁡t(\operatorname{cos}⁡t-t\operatorname{sin}⁡t) \\  & =t{sin}^{2}⁡t+{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t+t{cos}^{2}⁡t-{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t \\  & =t({sin}^{2}⁡t+{cos}^{2}⁡t) \\  & =t.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{2\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }t\,dt \\  & =\frac{{t}^{2}}{2}\,{|}_{0}^{2\pi } \\  & =\frac{(2\pi )^{2}}{2}-0 \\  & =2{\pi }^{2}\end{aligned}
$$

### Generated — moderate / spiral / observed_spiral

Evaluate  ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left(x\,i+y\,j\right)$ and $C$ is the path $r(t)=t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j$ for $t\in [0,2\pi ].$

- $2\left(2\right)$
- $2\left(\pi \right)$
- $2\left({\pi }^{2}\right)$
- $2\left(2\pi \right)$
- $2\left(2{\pi }^{2}\right)$ **correct**

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t\operatorname{sin}⁡t,\,y=t\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(x\,i+y\,j\right) \\  & =(2)\left(t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(t\operatorname{cos}⁡t)j \\  & =(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((t\operatorname{sin}⁡t\,i+t\operatorname{cos}⁡t\,j)\right)\cdot ((\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,i+(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,j) \\  & =(2)\left(t\operatorname{sin}⁡t(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)+t\operatorname{cos}⁡t(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\right) \\  & =(2)\left(t{sin}^{2}⁡t+{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t+t{cos}^{2}⁡t-{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t\right) \\  & =(2)\left(t({sin}^{2}⁡t+{cos}^{2}⁡t)\right) \\  & =(2)\left(t\right).\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{2\pi }f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{2\pi }t\,dt\right) \\  & =(2)\left(\frac{{t}^{2}}{2}\,{|}_{0}^{2\pi }\right) \\  & =(2)\left(\frac{(2\pi )^{2}}{2}-0\right) \\  & =(2)\left(2{\pi }^{2}\right)\end{aligned}
$$

### Generated — moderate / parabola / observed_parabola

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i+x\,j$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j$ for $t\in [0,1].$

- $4$
- $1$ **correct**
- $3$
- $2$
- $0$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y={t}^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,j \\  & ={t}^{2}\,i+t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({t}^{2}\,i+t\,j)\cdot (i+2t\,j) \\  & ={t}^{2}\cdot 1+t\cdot 2t \\  & =3{t}^{2}.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}3{t}^{2}\,dt \\  & ={[{t}^{3}]}_{0}^{1} \\  & =[1-0] \\  & =1\end{aligned}
$$

### Generated — moderate / parabola / observed_parabola

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left(y\,i+x\,j\right)$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j$ for $t\in [0,1].$

- $2\left(3\right)$
- $2\left(4\right)$
- $2\left(0\right)$
- $2\left(2\right)$
- $2\left(1\right)$ **correct**

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y={t}^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(y\,i+x\,j\right) \\  & =(2)\left({t}^{2}\,i+t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left(({t}^{2}\,i+t\,j)\right)\cdot (i+2t\,j) \\  & =(2)\left({t}^{2}\cdot 1+t\cdot 2t\right) \\  & =(2)\left(3{t}^{2}\right).\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{1}3{t}^{2}\,dt\right) \\  & =(2)\left({[{t}^{3}]}_{0}^{1}\right) \\  & =(2)\left([1-0]\right) \\  & =(2)\left(1\right)\end{aligned}
$$

### Generated — moderate / rational / observed_rational

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j$ and $C$ is the path $r(t)={t}^{2}\,i+(t-1)\,j$ for $t\in [3,4].$

- $9$
- $-2$
- $-7$ **correct**
- $-11$
- $2$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={t}^{2},\,y=t-1.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j \\  & =\frac{(t-1)+1}{{t}^{2}}\,i-\frac{2({t}^{2}-1)}{t-1}\,j \\  & =\frac{1}{t}\,i-2(t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j \\  & =2t\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\frac{1}{t}\,i-2(t+1)\,j)\cdot (2t\,i+j) \\  & =\frac{1}{t}\cdot 2t-2(t+1)\cdot 1 \\  & =2-2(t+1)\cdot 1 \\  & =-2t.\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{3}^{4}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{3}^{4}(-2t)\,dt \\  & ={[-{t}^{2}]}_{3}^{4} \\  & =[-16+9] \\  & =-7\end{aligned}
$$

### Generated — moderate / rational / observed_rational

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left(\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j\right)$ and $C$ is the path $r(t)={t}^{2}\,i+(t-1)\,j$ for $t\in [3,4].$

- $2\left(-7\right)$ **correct**
- $2\left(9\right)$
- $2\left(2\right)$
- $2\left(-11\right)$
- $2\left(-2\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={t}^{2},\,y=t-1.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(\frac{y+1}{x}\,i-\frac{2(x-1)}{y}\,j\right) \\  & =(2)\left(\frac{(t-1)+1}{{t}^{2}}\,i-\frac{2({t}^{2}-1)}{t-1}\,j\right) \\  & =(2)\left(\frac{1}{t}\,i-2(t+1)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(t-1)j \\  & =2t\,i+j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((\frac{1}{t}\,i-2(t+1)\,j)\right)\cdot (2t\,i+j) \\  & =(2)\left(\frac{1}{t}\cdot 2t-2(t+1)\cdot 1\right) \\  & =(2)\left(2-2(t+1)\cdot 1\right) \\  & =(2)\left(-2t\right).\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{3}^{4}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{3}^{4}(-2t)\,dt\right) \\  & =(2)\left({[-{t}^{2}]}_{3}^{4}\right) \\  & =(2)\left([-16+9]\right) \\  & =(2)\left(-7\right)\end{aligned}
$$

### Generated — moderate / arcsine / observed_arcsine

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(y\operatorname{sin}⁡x)\,i+(x+y)\,j$ and $C$ is the path  $r(t)=\operatorname{arcsin}⁡t\,i+2j$ for $t\in [0,\frac{1}{2}].$

- $1-\sqrt{3}$
- $\sqrt{2}$
- $-4-\sqrt{2}$
- $2-\sqrt{3}$ **correct**
- $-2+\sqrt{3}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{arcsin}⁡t,\,y=2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =2\operatorname{sin}⁡(\operatorname{arcsin}⁡t)\,i+(\operatorname{arcsin}⁡t+2)\,j \\  & =2t\,i+(\operatorname{arcsin}⁡t+2)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{arcsin}⁡t)i+\frac{\text{d}}{\text{d}t}(2)j \\  & =\frac{1}{\sqrt{1-{t}^{2}}}\,i.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2t\,i+(\operatorname{arcsin}⁡t+2)\,j)\cdot (\frac{1}{\sqrt{1-{t}^{2}}}\,i) \\  & =\frac{2t}{\sqrt{1-{t}^{2}}}.\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1/2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1/2}\frac{2t}{\sqrt{1-{t}^{2}}}\,dt \\  & =-2\sqrt{1-{t}^{2}}\,{|}_{0}^{1/2} \\  & =-2(\sqrt{1-{(\frac{1}{2})}^{2}}-1) \\  & =2-\sqrt{3}\end{aligned}
$$

### Generated — moderate / arcsine / observed_arcsine

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=(2)\left((y\operatorname{sin}⁡x)\,i+(x+y)\,j\right)$ and $C$ is the path  $r(t)=\operatorname{arcsin}⁡t\,i+2j$ for $t\in [0,\frac{1}{2}].$

- $2\left(-4-\sqrt{2}\right)$
- $2\left(1-\sqrt{3}\right)$
- $2\left(-2+\sqrt{3}\right)$
- $2\left(2-\sqrt{3}\right)$ **correct**
- $2\left(\sqrt{2}\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{arcsin}⁡t,\,y=2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2)\left(2\operatorname{sin}⁡(\operatorname{arcsin}⁡t)\,i+(\operatorname{arcsin}⁡t+2)\,j\right) \\  & =(2)\left(2t\,i+(\operatorname{arcsin}⁡t+2)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{arcsin}⁡t)i+\frac{\text{d}}{\text{d}t}(2)j \\  & =\frac{1}{\sqrt{1-{t}^{2}}}\,i.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2)\left((2t\,i+(\operatorname{arcsin}⁡t+2)\,j)\right)\cdot (\frac{1}{\sqrt{1-{t}^{2}}}\,i) \\  & =(2)\left(\frac{2t}{\sqrt{1-{t}^{2}}}\right).\end{aligned}
$$

Finally, we evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1/2}f(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =(2)\left({\int }_{0}^{1/2}\frac{2t}{\sqrt{1-{t}^{2}}}\,dt\right) \\  & =(2)\left(-2\sqrt{1-{t}^{2}}\,{|}_{0}^{1/2}\right) \\  & =(2)\left(-2(\sqrt{1-{(\frac{1}{2})}^{2}}-1)\right) \\  & =(2)\left(2-\sqrt{3}\right)\end{aligned}
$$

### Generated — easy / affine / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 2 y)\,i+(2 x - 2 y)\,j$ and $C$ is the path $r(t)=(3 t + 3)\,i+(- 3 t - 3)\,j$ for $t\in[0,1].$

- $81$
- $-54$
- $-27$ **correct**
- $-45$
- $45$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=3 t + 3,\quad y=- 3 t - 3.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y)\,i+(2 x - 2 y)\,j \\  & =(6 t + 6)\,i+(12 t + 12)\,j \\  & =(6 t + 6)\,i+(12 t + 12)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t + 3)\,i+\frac{\text{d}}{\text{d}t}(- 3 t - 3)\,j \\  & =(3)\,i+(-3)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((6 t + 6)\,i+(12 t + 12)\,j)\cdot((3)\,i+(-3)\,j) \\  & =(6 t + 6)\cdot(3)+(12 t + 12)\cdot(-3) \\  & =(18 t + 18)+(- 36 t - 36) \\  & =- 18 t - 18\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{1}(- 18 t - 18)\,\text{d}t \\  & =\left[- 9 t^{2} - 18 t\right]_{0}^{1} \\  & =((-18)+(-9))-((0)+(0)) \\  & =(-27)-(0) \\  & =-27\end{aligned}
$$

### Generated — easy / affine / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(2 y)\,i+(4 x + 2 y)\,j$ and $C$ is the path $r(t)=(2 t - 3)\,i+(- 4 t - 4)\,j$ for $t\in[0,1].$

- $68$
- $56$ **correct**
- $-44$
- $-104$
- $80$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=2 t - 3,\quad y=- 4 t - 4.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2 y)\,i+(4 x + 2 y)\,j \\  & =(- 8 t - 8)\,i+(-20)\,j \\  & =(- 8 t - 8)\,i+(-20)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(2 t - 3)\,i+\frac{\text{d}}{\text{d}t}(- 4 t - 4)\,j \\  & =(2)\,i+(-4)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 8 t - 8)\,i+(-20)\,j)\cdot((2)\,i+(-4)\,j) \\  & =(- 8 t - 8)\cdot(2)+(-20)\cdot(-4) \\  & =(- 16 t - 16)+(80) \\  & =- 16 t + 64\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{1}(- 16 t + 64)\,\text{d}t \\  & =\left[- 8 t^{2} + 64 t\right]_{0}^{1} \\  & =((-8)+(64))-((0)+(0)) \\  & =(56)-(0) \\  & =56\end{aligned}
$$

### Generated — moderate / log / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(e^{x})\,i+(2 y)\,j$ and $C$ is the path $r(t)=(\ln{\left(t \right)})\,i+(t)\,j$ for $t\in[1,4].$

- $18$ **correct**
- $\frac{21}{2}$
- $\frac{45}{2}$
- $12$
- $15$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\ln{\left(t \right)},\quad y=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(e^{x})\,i+(2 y)\,j \\  & =(t)\,i+(2 t)\,j \\  & =(t)\,i+(2 t)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =(\frac{1}{t})\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t)\,i+(2 t)\,j)\cdot((\frac{1}{t})\,i+(1)\,j) \\  & =(t)\cdot(\frac{1}{t})+(2 t)\cdot(1) \\  & =(1)+(2 t) \\  & =2 t + 1\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{1}^{4}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{1}^{4}(2 t + 1)\,\text{d}t \\  & =\left[t^{2} + t\right]_{1}^{4} \\  & =((4)+(16))-((1)+(1)) \\  & =(20)-(2) \\  & =18\end{aligned}
$$

### Generated — moderate / log / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 e^{x})\,i+(- 8 y)\,j$ and $C$ is the path $r(t)=(\ln{\left(t \right)})\,i+(t)\,j$ for $t\in[1,2].$

- $-10$
- $-12$
- $-18$
- $-8$
- $-16$ **correct**

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\ln{\left(t \right)},\quad y=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 e^{x})\,i+(- 8 y)\,j \\  & =(- 4 t)\,i+(- 8 t)\,j \\  & =(- 4 t)\,i+(- 8 t)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =(\frac{1}{t})\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 4 t)\,i+(- 8 t)\,j)\cdot((\frac{1}{t})\,i+(1)\,j) \\  & =(- 4 t)\cdot(\frac{1}{t})+(- 8 t)\cdot(1) \\  & =(-4)+(- 8 t) \\  & =- 8 t - 4\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{1}^{2}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{1}^{2}(- 8 t - 4)\,\text{d}t \\  & =\left[- 4 t^{2} - 4 t\right]_{1}^{2} \\  & =((-8)+(-16))-((-4)+(-4)) \\  & =(-24)-(-8) \\  & =-16\end{aligned}
$$

### Generated — moderate / polynomial / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(x^{2} y)\,i+(x + 1)\,j$ and $C$ is the path $r(t)=(3 t)\,i+(t + 2)\,j$ for $t\in[0,1].$

- $\frac{109}{4}$ **correct**
- $\frac{89}{4}$
- $\frac{43}{4}$
- $\frac{5}{2}$
- $\frac{99}{4}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=3 t,\quad y=t + 2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x^{2} y)\,i+(x + 1)\,j \\  & =(9 t^{2} \left(t + 2\right))\,i+(3 t + 1)\,j \\  & =(9 t^{2} \left(t + 2\right))\,i+(3 t + 1)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(t + 2)\,j \\  & =(3)\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((9 t^{2} \left(t + 2\right))\,i+(3 t + 1)\,j)\cdot((3)\,i+(1)\,j) \\  & =(9 t^{2} \left(t + 2\right))\cdot(3)+(3 t + 1)\cdot(1) \\  & =(27 t^{3} + 54 t^{2})+(3 t + 1) \\  & =27 t^{3} + 54 t^{2} + 3 t + 1\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{1}(27 t^{3} + 54 t^{2} + 3 t + 1)\,\text{d}t \\  & =\left[\frac{27 t^{4}}{4} + 18 t^{3} + \frac{3 t^{2}}{2} + t\right]_{0}^{1} \\  & =((1)+(18)+(\frac{3}{2})+(\frac{27}{4}))-((0)+(0)+(0)+(0)) \\  & =(\frac{109}{4})-(0) \\  & =\frac{109}{4}\end{aligned}
$$

### Generated — moderate / polynomial / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 x^{2} y)\,i+(- 4 x - 4)\,j$ and $C$ is the path $r(t)=(3 t)\,i+(t + 2)\,j$ for $t\in[0,2].$

- $-32$
- $-976$
- $-368$
- $-1040$ **correct**
- $-1008$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=3 t,\quad y=t + 2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 x^{2} y)\,i+(- 4 x - 4)\,j \\  & =(- 36 t^{2} \left(t + 2\right))\,i+(- 12 t - 4)\,j \\  & =(36 t^{2} \left(- t - 2\right))\,i+(- 12 t - 4)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(t + 2)\,j \\  & =(3)\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((36 t^{2} \left(- t - 2\right))\,i+(- 12 t - 4)\,j)\cdot((3)\,i+(1)\,j) \\  & =(36 t^{2} \left(- t - 2\right))\cdot(3)+(- 12 t - 4)\cdot(1) \\  & =(- 108 t^{3} - 216 t^{2})+(- 12 t - 4) \\  & =- 108 t^{3} - 216 t^{2} - 12 t - 4\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{2}(- 108 t^{3} - 216 t^{2} - 12 t - 4)\,\text{d}t \\  & =\left[- 27 t^{4} - 72 t^{3} - 6 t^{2} - 4 t\right]_{0}^{2} \\  & =((-576)+(-432)+(-24)+(-8))-((0)+(0)+(0)+(0)) \\  & =(-1040)-(0) \\  & =-1040\end{aligned}
$$

### Generated — moderate / offset_circle / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(x)\,i+(y - 1)\,j$ and $C$ is the path $r(t)=(\sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j$ for $t\in[\pi,\frac{3 \pi}{2}].$

- $2$
- $-1$ **correct**
- $-2 - \frac{\pi}{2}$
- $- \frac{3}{2}$
- $0$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\sin{\left(t \right)},\quad y=\cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x)\,i+(y - 1)\,j \\  & =(\sin{\left(t \right)})\,i+(\cos{\left(t \right)} - 1)\,j \\  & =(\sin{\left(t \right)})\,i+(\cos{\left(t \right)} - 1)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)})\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((\sin{\left(t \right)})\,i+(\cos{\left(t \right)} - 1)\,j)\cdot((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j) \\  & =(\sin{\left(t \right)})\cdot(\cos{\left(t \right)})+(\cos{\left(t \right)} - 1)\cdot(- \sin{\left(t \right)}) \\  & =(\sin{\left(t \right)} \cos{\left(t \right)})+(- \sin{\left(t \right)} \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =\sin{\left(t \right)}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{\pi}^{\frac{3 \pi}{2}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{\pi}^{\frac{3 \pi}{2}}(\sin{\left(t \right)})\,\text{d}t \\  & =\left[- \cos{\left(t \right)}\right]_{\pi}^{\frac{3 \pi}{2}} \\  & =((0))-((1)) \\  & =(0)-(1) \\  & =-1\end{aligned}
$$

### Generated — moderate / offset_circle / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(6 x)\,i+(6 y - 6)\,j$ and $C$ is the path $r(t)=(\sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j$ for $t\in[\pi,\frac{3 \pi}{2}].$

- $-6$ **correct**
- $0$
- $12$
- $-9$
- $-12 - 3 \pi$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\sin{\left(t \right)},\quad y=\cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(6 x)\,i+(6 y - 6)\,j \\  & =(6 \sin{\left(t \right)})\,i+(6 \cos{\left(t \right)} - 6)\,j \\  & =(6 \sin{\left(t \right)})\,i+(6 \cos{\left(t \right)} - 6)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)})\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((6 \sin{\left(t \right)})\,i+(6 \cos{\left(t \right)} - 6)\,j)\cdot((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j) \\  & =(6 \sin{\left(t \right)})\cdot(\cos{\left(t \right)})+(6 \cos{\left(t \right)} - 6)\cdot(- \sin{\left(t \right)}) \\  & =(6 \sin{\left(t \right)} \cos{\left(t \right)})+(- 6 \sin{\left(t \right)} \cos{\left(t \right)} + 6 \sin{\left(t \right)}) \\  & =6 \sin{\left(t \right)}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{\pi}^{\frac{3 \pi}{2}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{\pi}^{\frac{3 \pi}{2}}(6 \sin{\left(t \right)})\,\text{d}t \\  & =\left[- 6 \cos{\left(t \right)}\right]_{\pi}^{\frac{3 \pi}{2}} \\  & =((0))-((6)) \\  & =(0)-(6) \\  & =-6\end{aligned}
$$

### Generated — moderate / rotation / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(y)\,i+(- x)\,j$ and $C$ is the path $r(t)=(\sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j$ for $t\in[0,\frac{3 \pi}{2}].$

- $\frac{3 \pi}{2}$ **correct**
- $3 \pi$
- $\frac{3 \pi}{4}$
- $\frac{9 \pi}{4}$
- $0$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\sin{\left(t \right)},\quad y=\cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(y)\,i+(- x)\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)})\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j)\cdot((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j) \\  & =(\cos{\left(t \right)})\cdot(\cos{\left(t \right)})+(- \sin{\left(t \right)})\cdot(- \sin{\left(t \right)}) \\  & =(\cos^{2}{\left(t \right)})+(\sin^{2}{\left(t \right)}) \\  & =1\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{\frac{3 \pi}{2}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{\frac{3 \pi}{2}}(1)\,\text{d}t \\  & =\left[t\right]_{0}^{\frac{3 \pi}{2}} \\  & =((\frac{3 \pi}{2}))-((0)) \\  & =(\frac{3 \pi}{2})-(0) \\  & =\frac{3 \pi}{2}\end{aligned}
$$

### Generated — moderate / rotation / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 y)\,i+(4 x)\,j$ and $C$ is the path $r(t)=(\sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j$ for $t\in[0,2 \pi].$

- $- 12 \pi$
- $- 16 \pi$
- $- 4 \pi$
- $- 8 \pi$ **correct**
- $0$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\sin{\left(t \right)},\quad y=\cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 y)\,i+(4 x)\,j \\  & =(- 4 \cos{\left(t \right)})\,i+(4 \sin{\left(t \right)})\,j \\  & =(- 4 \cos{\left(t \right)})\,i+(4 \sin{\left(t \right)})\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)})\,j \\  & =(\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 4 \cos{\left(t \right)})\,i+(4 \sin{\left(t \right)})\,j)\cdot((\cos{\left(t \right)})\,i+(- \sin{\left(t \right)})\,j) \\  & =(- 4 \cos{\left(t \right)})\cdot(\cos{\left(t \right)})+(4 \sin{\left(t \right)})\cdot(- \sin{\left(t \right)}) \\  & =(- 4 \cos^{2}{\left(t \right)})+(- 4 \sin^{2}{\left(t \right)}) \\  & =-4\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{2 \pi}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{2 \pi}(-4)\,\text{d}t \\  & =\left[- 4 t\right]_{0}^{2 \pi} \\  & =((- 8 \pi))-((0)) \\  & =(- 8 \pi)-(0) \\  & =- 8 \pi\end{aligned}
$$

### Generated — moderate / spiral / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(x)\,i+(y)\,j$ and $C$ is the path $r(t)=(t \sin{\left(t \right)})\,i+(t \cos{\left(t \right)})\,j$ for $t\in[0,\frac{3 \pi}{2}].$

- $\frac{9 \pi^{2}}{8}$ **correct**
- $- \frac{1}{4} + \frac{9 \pi^{2}}{16}$
- $0$
- $\frac{3 \pi}{2}$
- $\frac{9 \pi^{2}}{4}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t \sin{\left(t \right)},\quad y=t \cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x)\,i+(y)\,j \\  & =(t \sin{\left(t \right)})\,i+(t \cos{\left(t \right)})\,j \\  & =(t \sin{\left(t \right)})\,i+(t \cos{\left(t \right)})\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(t \cos{\left(t \right)})\,j \\  & =(t \cos{\left(t \right)} + \sin{\left(t \right)})\,i+(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t \sin{\left(t \right)})\,i+(t \cos{\left(t \right)})\,j)\cdot((t \cos{\left(t \right)} + \sin{\left(t \right)})\,i+(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,j) \\  & =(t \sin{\left(t \right)})\cdot(t \cos{\left(t \right)} + \sin{\left(t \right)})+(t \cos{\left(t \right)})\cdot(- t \sin{\left(t \right)} + \cos{\left(t \right)}) \\  & =(t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t \sin^{2}{\left(t \right)})+(- t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)}) \\  & =t\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{\frac{3 \pi}{2}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{\frac{3 \pi}{2}}(t)\,\text{d}t \\  & =\left[\frac{t^{2}}{2}\right]_{0}^{\frac{3 \pi}{2}} \\  & =((\frac{9 \pi^{2}}{8}))-((0)) \\  & =(\frac{9 \pi^{2}}{8})-(0) \\  & =\frac{9 \pi^{2}}{8}\end{aligned}
$$

### Generated — moderate / spiral / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 x)\,i+(- 4 y)\,j$ and $C$ is the path $r(t)=(t \sin{\left(t \right)})\,i+(t \cos{\left(t \right)})\,j$ for $t\in[0,2 \pi].$

- $- 8 \pi$
- $- 4 \pi^{2}$
- $0$
- $- 8 \pi^{2}$ **correct**
- $- 16 \pi^{2}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t \sin{\left(t \right)},\quad y=t \cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 x)\,i+(- 4 y)\,j \\  & =(- 4 t \sin{\left(t \right)})\,i+(- 4 t \cos{\left(t \right)})\,j \\  & =(- 4 t \sin{\left(t \right)})\,i+(- 4 t \cos{\left(t \right)})\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(t \cos{\left(t \right)})\,j \\  & =(t \cos{\left(t \right)} + \sin{\left(t \right)})\,i+(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 4 t \sin{\left(t \right)})\,i+(- 4 t \cos{\left(t \right)})\,j)\cdot((t \cos{\left(t \right)} + \sin{\left(t \right)})\,i+(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,j) \\  & =(- 4 t \sin{\left(t \right)})\cdot(t \cos{\left(t \right)} + \sin{\left(t \right)})+(- 4 t \cos{\left(t \right)})\cdot(- t \sin{\left(t \right)} + \cos{\left(t \right)}) \\  & =(- 4 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t \sin^{2}{\left(t \right)})+(4 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t \cos^{2}{\left(t \right)}) \\  & =- 4 t\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{2 \pi}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{2 \pi}(- 4 t)\,\text{d}t \\  & =\left[- 2 t^{2}\right]_{0}^{2 \pi} \\  & =((- 8 \pi^{2}))-((0)) \\  & =(- 8 \pi^{2})-(0) \\  & =- 8 \pi^{2}\end{aligned}
$$

### Generated — moderate / parabola / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 2 y)\,i+(- 2 x)\,j$ and $C$ is the path $r(t)=(t)\,i+(t^{2})\,j$ for $t\in[3,4].$

- $-74$ **correct**
- $- \frac{74}{3}$
- $-182$
- $- \frac{116}{3}$
- $- \frac{148}{3}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t,\quad y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y)\,i+(- 2 x)\,j \\  & =(- 2 t^{2})\,i+(- 2 t)\,j \\  & =(- 2 t^{2})\,i+(- 2 t)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j \\  & =(1)\,i+(2 t)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t^{2})\,i+(- 2 t)\,j)\cdot((1)\,i+(2 t)\,j) \\  & =(- 2 t^{2})\cdot(1)+(- 2 t)\cdot(2 t) \\  & =(- 2 t^{2})+(- 4 t^{2}) \\  & =- 6 t^{2}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{3}^{4}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{3}^{4}(- 6 t^{2})\,\text{d}t \\  & =\left[- 2 t^{3}\right]_{3}^{4} \\  & =((-128))-((-54)) \\  & =(-128)-(-54) \\  & =-74\end{aligned}
$$

### Generated — moderate / parabola / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 y)\,i+(- 4 x)\,j$ and $C$ is the path $r(t)=(t)\,i+(t^{2})\,j$ for $t\in[0,4].$

- $- \frac{512}{3}$
- $- \frac{256}{3}$
- $-544$
- $-256$ **correct**
- $- \frac{448}{3}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t,\quad y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 y)\,i+(- 4 x)\,j \\  & =(- 4 t^{2})\,i+(- 4 t)\,j \\  & =(- 4 t^{2})\,i+(- 4 t)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j \\  & =(1)\,i+(2 t)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 4 t^{2})\,i+(- 4 t)\,j)\cdot((1)\,i+(2 t)\,j) \\  & =(- 4 t^{2})\cdot(1)+(- 4 t)\cdot(2 t) \\  & =(- 4 t^{2})+(- 8 t^{2}) \\  & =- 12 t^{2}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{4}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{4}(- 12 t^{2})\,\text{d}t \\  & =\left[- 4 t^{3}\right]_{0}^{4} \\  & =((-256))-((0)) \\  & =(-256)-(0) \\  & =-256\end{aligned}
$$

### Generated — moderate / rational / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(\frac{y + 1}{x})\,i+(\frac{- 2 x + 2}{y})\,j$ and $C$ is the path $r(t)=(t^{2})\,i+(t - 1)\,j$ for $t\in[2,5].$

- $-21$ **correct**
- $33$
- $-27 + \ln{\left(\frac{5}{2} \right)}$
- $-27$
- $6$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t^{2},\quad y=t - 1.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(\frac{y + 1}{x})\,i+(\frac{- 2 x + 2}{y})\,j \\  & =(\frac{1}{t})\,i+(\frac{- 2 t^{2} + 2}{t - 1})\,j \\  & =(\frac{1}{t})\,i+(- 2 t - 2)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(t - 1)\,j \\  & =(2 t)\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((\frac{1}{t})\,i+(- 2 t - 2)\,j)\cdot((2 t)\,i+(1)\,j) \\  & =(\frac{1}{t})\cdot(2 t)+(- 2 t - 2)\cdot(1) \\  & =(2)+(- 2 t - 2) \\  & =- 2 t\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{2}^{5}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{2}^{5}(- 2 t)\,\text{d}t \\  & =\left[- t^{2}\right]_{2}^{5} \\  & =((-25))-((-4)) \\  & =(-25)-(-4) \\  & =-21\end{aligned}
$$

### Generated — moderate / rational / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(\frac{- 4 y - 4}{x})\,i+(\frac{8 x - 8}{y})\,j$ and $C$ is the path $r(t)=(t^{2})\,i+(t - 1)\,j$ for $t\in[2,3].$

- $-36$
- $-8$
- $\ln{\left(\frac{16}{81} \right)} + 28$
- $28$
- $20$ **correct**

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=t^{2},\quad y=t - 1.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(\frac{- 4 y - 4}{x})\,i+(\frac{8 x - 8}{y})\,j \\  & =(- \frac{4}{t})\,i+(\frac{8 t^{2} - 8}{t - 1})\,j \\  & =(- \frac{4}{t})\,i+(8 t + 8)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t^{2})\,i+\frac{\text{d}}{\text{d}t}(t - 1)\,j \\  & =(2 t)\,i+(1)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- \frac{4}{t})\,i+(8 t + 8)\,j)\cdot((2 t)\,i+(1)\,j) \\  & =(- \frac{4}{t})\cdot(2 t)+(8 t + 8)\cdot(1) \\  & =(-8)+(8 t + 8) \\  & =8 t\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{2}^{3}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{2}^{3}(8 t)\,\text{d}t \\  & =\left[4 t^{2}\right]_{2}^{3} \\  & =((36))-((16)) \\  & =(36)-(16) \\  & =20\end{aligned}
$$

### Generated — moderate / arcsine / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(y \sin{\left(x \right)})\,i+(x + y)\,j$ and $C$ is the path $r(t)=(\operatorname{asin}{\left(t \right)})\,i+(2)\,j$ for $t\in[\frac{1}{4},\frac{3}{4}].$

- $- \frac{7 \sqrt{7}}{96} + \frac{5 \sqrt{15}}{32}$
- $\frac{1}{2}$
- $- \frac{\sqrt{15}}{2} + \frac{\sqrt{7}}{2}$
- $\ln{\left(\frac{15}{7} \right)}$
- $- \frac{\sqrt{7}}{2} + \frac{\sqrt{15}}{2}$ **correct**

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{asin}{\left(t \right)},\quad y=2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(y \sin{\left(x \right)})\,i+(x + y)\,j \\  & =(2 t)\,i+(\operatorname{asin}{\left(t \right)} + 2)\,j \\  & =(2 t)\,i+(\operatorname{asin}{\left(t \right)} + 2)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{asin}{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(2)\,j \\  & =(\frac{1}{\sqrt{- t^{2} + 1}})\,i+(0)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((2 t)\,i+(\operatorname{asin}{\left(t \right)} + 2)\,j)\cdot((\frac{1}{\sqrt{- t^{2} + 1}})\,i+(0)\,j) \\  & =(2 t)\cdot(\frac{1}{\sqrt{- t^{2} + 1}})+(\operatorname{asin}{\left(t \right)} + 2)\cdot(0) \\  & =(\frac{2 t}{\sqrt{- t^{2} + 1}})+(0) \\  & =\frac{2 t}{\sqrt{- t^{2} + 1}}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{\frac{1}{4}}^{\frac{3}{4}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{\frac{1}{4}}^{\frac{3}{4}}(\frac{2 t}{\sqrt{- t^{2} + 1}})\,\text{d}t \\  & =\left[- 2 \sqrt{- t^{2} + 1}\right]_{\frac{1}{4}}^{\frac{3}{4}} \\  & =((- \frac{\sqrt{7}}{2}))-((- \frac{\sqrt{15}}{2})) \\  & =(- \frac{\sqrt{7}}{2})-(- \frac{\sqrt{15}}{2}) \\  & =- \frac{\sqrt{7}}{2} + \frac{\sqrt{15}}{2}\end{aligned}
$$

### Generated — moderate / arcsine / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 4 y \sin{\left(x \right)})\,i+(- 4 x - 4 y)\,j$ and $C$ is the path $r(t)=(\operatorname{asin}{\left(t \right)})\,i+(2)\,j$ for $t\in[\frac{1}{2},\frac{3}{4}].$

- $- 2 \sqrt{7} + 4 \sqrt{3}$
- $- \frac{5}{4}$
- $- \sqrt{3} + \frac{7 \sqrt{7}}{24}$
- $\ln{\left(\frac{2401}{20736} \right)}$
- $- 4 \sqrt{3} + 2 \sqrt{7}$ **correct**

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{asin}{\left(t \right)},\quad y=2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 y \sin{\left(x \right)})\,i+(- 4 x - 4 y)\,j \\  & =(- 8 t)\,i+(- 4 \operatorname{asin}{\left(t \right)} - 8)\,j \\  & =(- 8 t)\,i+(- 4 \operatorname{asin}{\left(t \right)} - 8)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{asin}{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(2)\,j \\  & =(\frac{1}{\sqrt{- t^{2} + 1}})\,i+(0)\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 8 t)\,i+(- 4 \operatorname{asin}{\left(t \right)} - 8)\,j)\cdot((\frac{1}{\sqrt{- t^{2} + 1}})\,i+(0)\,j) \\  & =(- 8 t)\cdot(\frac{1}{\sqrt{- t^{2} + 1}})+(- 4 \operatorname{asin}{\left(t \right)} - 8)\cdot(0) \\  & =(- \frac{8 t}{\sqrt{- t^{2} + 1}})+(0) \\  & =- \frac{8 t}{\sqrt{- t^{2} + 1}}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{\frac{1}{2}}^{\frac{3}{4}}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{\frac{1}{2}}^{\frac{3}{4}}(- \frac{8 t}{\sqrt{- t^{2} + 1}})\,\text{d}t \\  & =\left[8 \sqrt{- t^{2} + 1}\right]_{\frac{1}{2}}^{\frac{3}{4}} \\  & =((2 \sqrt{7}))-((4 \sqrt{3})) \\  & =(2 \sqrt{7})-(4 \sqrt{3}) \\  & =- 4 \sqrt{3} + 2 \sqrt{7}\end{aligned}
$$

### Generated — hard / mixed_power / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(2 x y + 2 y)\,i+(- 4 x^{2} - 2 y)\,j$ and $C$ is the path $r(t)=(3 t^{2})\,i+(2 t^{3} + 2)\,j$ for $t\in[0,1].$

- $\frac{3078}{35}$
- $\frac{78}{35}$ **correct**
- $- \frac{223}{7}$
- $- \frac{300}{7}$
- $\frac{1151}{35}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=3 t^{2},\quad y=2 t^{3} + 2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2 x y + 2 y)\,i+(- 4 x^{2} - 2 y)\,j \\  & =(4 t^{3} + 6 t^{2} \left(2 t^{3} + 2\right) + 4)\,i+(- 36 t^{4} - 4 t^{3} - 4)\,j \\  & =(4 t^{3} + 12 t^{2} \left(t^{3} + 1\right) + 4)\,i+(- 36 t^{4} - 4 t^{3} - 4)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3 t^{2})\,i+\frac{\text{d}}{\text{d}t}(2 t^{3} + 2)\,j \\  & =(6 t)\,i+(6 t^{2})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((4 t^{3} + 12 t^{2} \left(t^{3} + 1\right) + 4)\,i+(- 36 t^{4} - 4 t^{3} - 4)\,j)\cdot((6 t)\,i+(6 t^{2})\,j) \\  & =(4 t^{3} + 12 t^{2} \left(t^{3} + 1\right) + 4)\cdot(6 t)+(- 36 t^{4} - 4 t^{3} - 4)\cdot(6 t^{2}) \\  & =(72 t^{6} + 24 t^{4} + 72 t^{3} + 24 t)+(- 216 t^{6} - 24 t^{5} - 24 t^{2}) \\  & =24 t \left(- 6 t^{5} - t^{4} + t^{3} + 3 t^{2} - t + 1\right)\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{1}(24 t \left(- 6 t^{5} - t^{4} + t^{3} + 3 t^{2} - t + 1\right))\,\text{d}t \\  & =\left[- \frac{144 t^{7}}{7} - 4 t^{6} + \frac{24 t^{5}}{5} + 18 t^{4} - 8 t^{3} + 12 t^{2}\right]_{0}^{1} \\  & =((-8)+(-4)+(12)+(18)+(- \frac{144}{7})+(\frac{24}{5}))-((0)+(0)+(0)+(0)+(0)+(0)) \\  & =(\frac{78}{35})-(0) \\  & =\frac{78}{35}\end{aligned}
$$

### Generated — hard / mixed_power / method

Evaluate ${\int}_{C}F\cdot\text{d}r$ given that $F(x,y)=(- 3 x y + 3 y)\,i+(- 4 x^{2} - 2 y)\,j$ and $C$ is the path $r(t)=(- 4 t^{2})\,i+(2 t^{3} + 2)\,j$ for $t\in[0,1].$

- $- \frac{663}{14}$
- $- \frac{4439}{35}$
- $- \frac{6156}{35}$ **correct**
- $- \frac{1476}{35}$
- $- \frac{468}{7}$

We will use the formula

$$
\int_C F\cdot\text{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=- 4 t^{2},\quad y=2 t^{3} + 2.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 3 x y + 3 y)\,i+(- 4 x^{2} - 2 y)\,j \\  & =(6 t^{3} + 12 t^{2} \left(2 t^{3} + 2\right) + 6)\,i+(- 64 t^{4} - 4 t^{3} - 4)\,j \\  & =(6 t^{3} + 24 t^{2} \left(t^{3} + 1\right) + 6)\,i+(- 64 t^{4} - 4 t^{3} - 4)\,j\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(- 4 t^{2})\,i+\frac{\text{d}}{\text{d}t}(2 t^{3} + 2)\,j \\  & =(- 8 t)\,i+(6 t^{2})\,j\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((6 t^{3} + 24 t^{2} \left(t^{3} + 1\right) + 6)\,i+(- 64 t^{4} - 4 t^{3} - 4)\,j)\cdot((- 8 t)\,i+(6 t^{2})\,j) \\  & =(6 t^{3} + 24 t^{2} \left(t^{3} + 1\right) + 6)\cdot(- 8 t)+(- 64 t^{4} - 4 t^{3} - 4)\cdot(6 t^{2}) \\  & =(- 192 t^{6} - 48 t^{4} - 192 t^{3} - 48 t)+(- 384 t^{6} - 24 t^{5} - 24 t^{2}) \\  & =24 t \left(- 24 t^{5} - t^{4} - 2 t^{3} - 8 t^{2} - t - 2\right)\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}\int_C F\cdot\text{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\text{d}t \\  & =\int_{0}^{1}(24 t \left(- 24 t^{5} - t^{4} - 2 t^{3} - 8 t^{2} - t - 2\right))\,\text{d}t \\  & =\left[- \frac{576 t^{7}}{7} - 4 t^{6} - \frac{48 t^{5}}{5} - 48 t^{4} - 8 t^{3} - 24 t^{2}\right]_{0}^{1} \\  & =((-48)+(-24)+(-8)+(-4)+(- \frac{576}{7})+(- \frac{48}{5}))-((0)+(0)+(0)+(0)+(0)+(0)) \\  & =(- \frac{6156}{35})-(0) \\  & =- \frac{6156}{35}\end{aligned}
$$