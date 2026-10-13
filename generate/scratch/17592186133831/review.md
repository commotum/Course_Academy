# Setup-only vector line integral review



Raw observed replays preserve anomalies and are ineligible for learning. Authored generated records use the stated parameterization and limits; the learner does not evaluate integrals.



## Original q-124638



Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)={y}^{2}\,i-{x}^{2}\,j$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j$ for $t\in [0,1]?$



Original worked solution



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
\begin{aligned}F(r(t)) & ={y}^{2}\,i-{x}^{2}\,j \\  & =({t}^{2})^{2}\,i-{t}^{2}\,j \\  & ={t}^{4}\,i-{t}^{2}\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({t}^{4}\,i-{t}^{2}\,j)\cdot (i+2t\,j) \\  & ={t}^{4}-2{t}^{3}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}{t}^{4}-2{t}^{3}\,dt\end{aligned}
$$



## observed-mask — easy
Template `polynomial`, profile `observed_polynomial`; eligible: False.

Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)={y}^{2}\,i-{x}^{2}\,j$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j$ for $t\in [0,1]?$

- ${\int }_{0}^{1}{t}^{4}-4{t}^{3}\,dt$
- ${\int }_{0}^{1}{t}^{4}-2{t}^{3}\,dt$ **Correct**
- ${\int }_{0}^{1}1-{t}^{2}\,dt$
- ${\int }_{0}^{1}4{t}^{3}-3{t}^{2}\,dt$
- ${\int }_{0}^{1}{t}^{2}-t\,dt$

Worked solution

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
\begin{aligned}F(r(t)) & ={y}^{2}\,i-{x}^{2}\,j \\  & =({t}^{2})^{2}\,i-{t}^{2}\,j \\  & ={t}^{4}\,i-{t}^{2}\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({t}^{4}\,i-{t}^{2}\,j)\cdot (i+2t\,j) \\  & ={t}^{4}-2{t}^{3}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}{t}^{4}-2{t}^{3}\,dt\end{aligned}
$$



## Original q-124687



Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i-x\,j$ and $C$ is the path $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$



Original worked solution



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j \\  & =\operatorname{sin}⁡t\,i-\operatorname{cos}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡t\,i-\operatorname{cos}⁡t\,j)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j) \\  & =-{sin}^{2}⁡t-{cos}^{2}⁡t \\  & =-1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-{\int }_{0}^{\pi }dt\end{aligned}
$$



## observed-mask — easy
Template `rotation`, profile `observed_rotation`; eligible: False.

Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=y\,i-x\,j$ and $C$ is the path $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$

- ${\int }_{0}^{\pi }dt$
- $-{\int }_{0}^{\pi }dt$ **Correct**
- ${\int }_{0}^{\pi }1-\operatorname{sin}⁡t\,dt$
- $0$
- ${\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt$

Worked solution

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j \\  & =\operatorname{sin}⁡t\,i-\operatorname{cos}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡t\,i-\operatorname{cos}⁡t\,j)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j) \\  & =-{sin}^{2}⁡t-{cos}^{2}⁡t \\  & =-1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-{\int }_{0}^{\pi }dt\end{aligned}
$$



## Original q-124679



Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+(y+1)\,j$ and $C$ is the path $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$



Original worked solution



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+(y+1)\,j \\  & =\operatorname{cos}⁡t\,i+(\operatorname{sin}⁡t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡t\,i+(\operatorname{sin}⁡t+1)\,j)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j) \\  & =-\operatorname{cos}⁡t\operatorname{sin}⁡t+(\operatorname{sin}⁡t+1)\operatorname{cos}⁡t \\  & =\operatorname{cos}⁡t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }\operatorname{cos}⁡t\,dt\end{aligned}
$$



## observed-mask — easy
Template `shifted_circle`, profile `observed_shifted_circle`; eligible: False.

Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+(y+1)\,j$ and $C$ is the path $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$

- ${\int }_{0}^{\pi }\operatorname{cos}⁡t\,dt$ **Correct**
- ${\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\,dt$
- ${\int }_{0}^{\pi }-\operatorname{cos}⁡t\,dt$
- ${\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt$
- ${\int }_{0}^{\pi }-\operatorname{sin}⁡t\operatorname{cos}⁡t\,dt$

Worked solution

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=\operatorname{cos}⁡t,\,y=\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+(y+1)\,j \\  & =\operatorname{cos}⁡t\,i+(\operatorname{sin}⁡t+1)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡t\,i+(\operatorname{sin}⁡t+1)\,j)\cdot (-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j) \\  & =-\operatorname{cos}⁡t\operatorname{sin}⁡t+(\operatorname{sin}⁡t+1)\operatorname{cos}⁡t \\  & =\operatorname{cos}⁡t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }\operatorname{cos}⁡t\,dt\end{aligned}
$$



## Original q-124680



Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x{y}^{2}\,i+2y\,j$ and $C$ is the path $r(t)={e}^{t}\,i+\sqrt{t}\,j$ for $t\in [0,1]?$



Original worked solution



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x{y}^{2}\,i+2y\,j \\  & ={e}^{t}{(\sqrt{t})}^{2}\,i+2\sqrt{t}\,j \\  & =t{e}^{t}\,i+2\sqrt{t}\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({e}^{t})i+\frac{\text{d}}{\text{d}t}(\sqrt{t})j \\  & ={e}^{t}\,i+\frac{1}{2\sqrt{t}}j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t{e}^{t}\,i+2\sqrt{t}\,j)\cdot ({e}^{t}\,i+\frac{1}{2\sqrt{t}}) \\  & =t{e}^{t}\cdot {e}^{t}+2\sqrt{t}\cdot \frac{1}{2\sqrt{t}} \\  & =t{e}^{2t}+1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}t{e}^{2t}+1\,dt\end{aligned}
$$



## observed-mask — easy
Template `exponential_root`, profile `observed_exponential_root`; eligible: False.

Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x{y}^{2}\,i+2y\,j$ and $C$ is the path $r(t)={e}^{t}\,i+\sqrt{t}\,j$ for $t\in [0,1]?$

- ${\int }_{0}^{1}{e}^{t}\sqrt{t}\,dt$
- ${\int }_{0}^{1}t{e}^{2t}+1\,dt$ **Correct**
- ${\int }_{0}^{1}{e}^{2t}\,dt$
- ${\int }_{0}^{1}t{e}^{t}+2\sqrt{t}\,dt$
- ${\int }_{0}^{1}{e}^{t}+\sqrt{t}\,dt$

Worked solution

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x{y}^{2}\,i+2y\,j \\  & ={e}^{t}{(\sqrt{t})}^{2}\,i+2\sqrt{t}\,j \\  & =t{e}^{t}\,i+2\sqrt{t}\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({e}^{t})i+\frac{\text{d}}{\text{d}t}(\sqrt{t})j \\  & ={e}^{t}\,i+\frac{1}{2\sqrt{t}}j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t{e}^{t}\,i+2\sqrt{t}\,j)\cdot ({e}^{t}\,i+\frac{1}{2\sqrt{t}}) \\  & =t{e}^{t}\cdot {e}^{t}+2\sqrt{t}\cdot \frac{1}{2\sqrt{t}} \\  & =t{e}^{2t}+1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}t{e}^{2t}+1\,dt\end{aligned}
$$



## Original q-124685



Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+y\,j$ and $C$ is the path $r(t)=t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$



Original worked solution



We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t\operatorname{cos}⁡t,\,y=t\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+y\,j \\  & =t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t)j \\  & =(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,i+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j)\cdot ((\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,i+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,j) \\  & =t\operatorname{cos}⁡t(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)+t\operatorname{sin}⁡t(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =t{cos}^{2}⁡t-{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t+t{sin}^{2}⁡t+{t}^{2}\operatorname{sin}⁡\operatorname{cos}⁡t) \\  & =t({cos}^{2}⁡t+{sin}^{2}⁡t) \\  & =t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }t\,dt\end{aligned}
$$



## observed-mask — easy
Template `spiral`, profile `observed_spiral`; eligible: False.

Which of the following is equivalent to ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y)=x\,i+y\,j$ and $C$ is the path $r(t)=t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j$ for $t\in [0,\pi ]?$

- ${\int }_{0}^{\pi }t\,dt$ **Correct**
- ${\int }_{0}^{\pi }\operatorname{cos}⁡t\,dt$
- ${\int }_{0}^{\pi }\operatorname{sin}⁡t\,dt$
- ${\int }_{0}^{\pi }t\operatorname{sin}⁡t\,dt$
- ${\int }_{0}^{\pi }t\operatorname{cos}⁡t\,dt$

Worked solution

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t\operatorname{cos}⁡t,\,y=t\operatorname{sin}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+y\,j \\  & =t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t)j \\  & =(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,i+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t\operatorname{cos}⁡t\,i+t\operatorname{sin}⁡t\,j)\cdot ((\operatorname{cos}⁡t-t\operatorname{sin}⁡t)\,i+(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,j) \\  & =t\operatorname{cos}⁡t(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)+t\operatorname{sin}⁡t(\operatorname{sin}⁡t+t\operatorname{cos}⁡t) \\  & =t{cos}^{2}⁡t-{t}^{2}\operatorname{sin}⁡t\operatorname{cos}⁡t+t{sin}^{2}⁡t+{t}^{2}\operatorname{sin}⁡\operatorname{cos}⁡t) \\  & =t({cos}^{2}⁡t+{sin}^{2}⁡t) \\  & =t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi }t\,dt\end{aligned}
$$



## authored-extension — easy
Template `polynomial`, profile `authored_polynomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 y^{2})\,i+(4 x^{2})\,j$ and $C$ is the path $r(t)=(t)\,i+(t^{2})\,j$ for $t\in [0,2]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{2}(3 t^{4} + 8 t^{3})\,dt$ **Correct**
- $\int_{0}^{2}(3 t^{4} + 4 t^{2})\,dt$
- $\int_{0}^{2}(- 3 t^{4} - 8 t^{3})\,dt$
- $\int_{0}^{2}(8 t^{3})\,dt$
- $\int_{0}^{2}(3 t^{4})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 y^{2})\,i+(4 x^{2})\,j \\  & =(3 (t^{2})^{2})\,i+(4 (t)^{2})\,j \\  & =(3 t^{4})\,i+(4 t^{2})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})j \\  & =(1)\,i+(2 t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t^{4})\,i+(4 t^{2})\,j)\cdot ((1)\,i+(2 t)\,j) \\  & =(3 t^{4})\cdot (1)+(4 t^{2})\cdot (2 t) \\  & =3 t^{4} + 8 t^{3}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{2}(3 t^{4} + 8 t^{3})\,dt.\end{aligned}
$$

## authored-extension — easy
Template `polynomial`, profile `authored_polynomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 y^{2})\,i+(3 x^{2})\,j$ and $C$ is the path $r(t)=(t)\,i+(t^{2})\,j$ for $t\in [0,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{3}(6 t^{3})\,dt$
- $\int_{0}^{3}(- 2 t^{4} + 3 t^{2})\,dt$
- $\int_{0}^{3}(2 t^{4} - 6 t^{3})\,dt$
- $\int_{0}^{3}(- 2 t^{4} + 6 t^{3})\,dt$ **Correct**
- $\int_{0}^{3}(- 2 t^{4})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y^{2})\,i+(3 x^{2})\,j \\  & =(- 2 (t^{2})^{2})\,i+(3 (t)^{2})\,j \\  & =(- 2 t^{4})\,i+(3 t^{2})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t)i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})j \\  & =(1)\,i+(2 t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t^{4})\,i+(3 t^{2})\,j)\cdot ((1)\,i+(2 t)\,j) \\  & =(- 2 t^{4})\cdot (1)+(3 t^{2})\cdot (2 t) \\  & =- 2 t^{4} + 6 t^{3}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{3}(- 2 t^{4} + 6 t^{3})\,dt.\end{aligned}
$$

## authored-extension — easy
Template `rotation`, profile `authored_rotation`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 y)\,i+(- 3 x)\,j$ and $C$ is the path $r(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(-3)\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(3 \sin{\left(t \right)} - 3 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(3)\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 3 \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 3 \sin^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\,y=\sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 y)\,i+(- 3 x)\,j \\  & =(3 (\sin{\left(t \right)}))\,i+(- 3 (\cos{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})j \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 \sin{\left(t \right)})\,i+(- 3 \cos{\left(t \right)})\,j)\cdot ((- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j) \\  & =(3 \sin{\left(t \right)})\cdot (- \sin{\left(t \right)})+(- 3 \cos{\left(t \right)})\cdot (\cos{\left(t \right)}) \\  & =-3.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(-3)\,dt.\end{aligned}
$$

## authored-extension — easy
Template `rotation`, profile `authored_rotation`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 y)\,i+(2 x)\,j$ and $C$ is the path $r(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(2 \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 2 \sin{\left(t \right)} + 2 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(-2)\,dt$
- $\int_{0}^{\frac{\pi}{3}}(2)\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(2 \sin^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\,y=\sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y)\,i+(2 x)\,j \\  & =(- 2 (\sin{\left(t \right)}))\,i+(2 (\cos{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})j \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 \sin{\left(t \right)})\,i+(2 \cos{\left(t \right)})\,j)\cdot ((- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j) \\  & =(- 2 \sin{\left(t \right)})\cdot (- \sin{\left(t \right)})+(2 \cos{\left(t \right)})\cdot (\cos{\left(t \right)}) \\  & =2.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(2)\,dt.\end{aligned}
$$

## authored-extension — easy
Template `shifted_circle`, profile `authored_shifted_circle`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 x)\,i+(3 y - 4)\,j$ and $C$ is the path $r(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j$ for $t\in [0,\frac{2 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{2 \pi}{3}}(- 4 \cos{\left(t \right)})\,dt$ **Correct**
- $\int_{0}^{\frac{2 \pi}{3}}(- 3 \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(4 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(3 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(3 \sin{\left(t \right)} + 3 \cos{\left(t \right)} - 4)\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\,y=\sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 x)\,i+(3 y - 4)\,j \\  & =(3 (\cos{\left(t \right)}))\,i+(3 (\sin{\left(t \right)}) - 4)\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})j \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 \cos{\left(t \right)})\,i+(3 \sin{\left(t \right)} - 4)\,j)\cdot ((- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j) \\  & =(3 \cos{\left(t \right)})\cdot (- \sin{\left(t \right)})+(3 \sin{\left(t \right)} - 4)\cdot (\cos{\left(t \right)}) \\  & =- 4 \cos{\left(t \right)}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{2 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{2 \pi}{3}}(- 4 \cos{\left(t \right)})\,dt.\end{aligned}
$$

## authored-extension — easy
Template `shifted_circle`, profile `authored_shifted_circle`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 x)\,i+(- 2 y - 3)\,j$ and $C$ is the path $r(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j$ for $t\in [0,\frac{2 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{2 \pi}{3}}(- 2 \sin{\left(t \right)} - 2 \cos{\left(t \right)} - 3)\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(2 \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(3 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(- 2 \sin{\left(t \right)} \cos{\left(t \right)} - 3 \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(- 3 \cos{\left(t \right)})\,dt$ **Correct**

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\,y=\sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 x)\,i+(- 2 y - 3)\,j \\  & =(- 2 (\cos{\left(t \right)}))\,i+(- 2 (\sin{\left(t \right)}) - 3)\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})j \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 \cos{\left(t \right)})\,i+(- 2 \sin{\left(t \right)} - 3)\,j)\cdot ((- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j) \\  & =(- 2 \cos{\left(t \right)})\cdot (- \sin{\left(t \right)})+(- 2 \sin{\left(t \right)} - 3)\cdot (\cos{\left(t \right)}) \\  & =- 3 \cos{\left(t \right)}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{2 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{2 \pi}{3}}(- 3 \cos{\left(t \right)})\,dt.\end{aligned}
$$

## authored-extension — easy
Template `exponential_root`, profile `authored_exponential_root`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 x y^{2})\,i+(- 8 y)\,j$ and $C$ is the path $r(t)=(e^{t})\,i+(\sqrt{t})\,j$ for $t\in [1,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{1}^{3}(3 t e^{2 t} - 4)\,dt$ **Correct**
- $\int_{1}^{3}(3 t e^{2 t})\,dt$
- $\int_{1}^{3}(- 3 t e^{2 t} + 4)\,dt$
- $\int_{1}^{3}(-4)\,dt$
- $\int_{1}^{3}(- 8 \sqrt{t} + 3 t e^{t})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=e^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 x y^{2})\,i+(- 8 y)\,j \\  & =(3 (e^{t}) (\sqrt{t})^{2})\,i+(- 8 (\sqrt{t}))\,j \\  & =(3 t e^{t})\,i+(- 8 \sqrt{t})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sqrt{t})j \\  & =(e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t e^{t})\,i+(- 8 \sqrt{t})\,j)\cdot ((e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j) \\  & =(3 t e^{t})\cdot (e^{t})+(- 8 \sqrt{t})\cdot (\frac{1}{2 \sqrt{t}}) \\  & =3 t e^{2 t} - 4.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{1}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{1}^{3}(3 t e^{2 t} - 4)\,dt.\end{aligned}
$$

## authored-extension — easy
Template `exponential_root`, profile `authored_exponential_root`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 x y^{2})\,i+(- 6 y)\,j$ and $C$ is the path $r(t)=(e^{t})\,i+(\sqrt{t})\,j$ for $t\in [1,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{1}^{3}(- 6 \sqrt{t} - 2 t e^{t})\,dt$
- $\int_{1}^{3}(- 2 t e^{2 t})\,dt$
- $\int_{1}^{3}(2 t e^{2 t} + 3)\,dt$
- $\int_{1}^{3}(-3)\,dt$
- $\int_{1}^{3}(- 2 t e^{2 t} - 3)\,dt$ **Correct**

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=e^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 x y^{2})\,i+(- 6 y)\,j \\  & =(- 2 (e^{t}) (\sqrt{t})^{2})\,i+(- 6 (\sqrt{t}))\,j \\  & =(- 2 t e^{t})\,i+(- 6 \sqrt{t})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sqrt{t})j \\  & =(e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t e^{t})\,i+(- 6 \sqrt{t})\,j)\cdot ((e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j) \\  & =(- 2 t e^{t})\cdot (e^{t})+(- 6 \sqrt{t})\cdot (\frac{1}{2 \sqrt{t}}) \\  & =- 2 t e^{2 t} - 3.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{1}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{1}^{3}(- 2 t e^{2 t} - 3)\,dt.\end{aligned}
$$

## authored-extension — easy
Template `spiral`, profile `authored_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 x)\,i+(3 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(3 t)\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(3 t \sin{\left(t \right)} + 3 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 3 t)\,dt$
- $\int_{0}^{\frac{\pi}{3}}(3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 3 t \sin^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 3 t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 x)\,i+(3 y)\,j \\  & =(3 (t \cos{\left(t \right)}))\,i+(3 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t \cos{\left(t \right)})\,i+(3 t \sin{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(3 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =3 t \sin^{2}{\left(t \right)} + 3 t \cos^{2}{\left(t \right)} \\  & =3 t(\cos^2 t+\sin^2 t) \\  & =3 t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(3 t)\,dt.\end{aligned}
$$

## authored-extension — easy
Template `spiral`, profile `authored_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 x)\,i+(- 2 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(- 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 2 t \sin^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 2 t \sin{\left(t \right)} - 2 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(2 t)\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 2 t)\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 2 t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 x)\,i+(- 2 y)\,j \\  & =(- 2 (t \cos{\left(t \right)}))\,i+(- 2 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t \cos{\left(t \right)})\,i+(- 2 t \sin{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(- 2 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 2 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 2 t \sin^{2}{\left(t \right)} - 2 t \cos^{2}{\left(t \right)} \\  & =- 2 t(\cos^2 t+\sin^2 t) \\  & =- 2 t.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(- 2 t)\,dt.\end{aligned}
$$

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(3 y^{2})\,i+(4 x^{2})\,j$ and $C$ is the path $r(t)=(t^{3})\,i+(t^{4})\,j$ for $t\in [0,2]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{2}(9 t^{10} + 16 t^{9})\,dt$ **Correct**
- $\int_{0}^{2}(3 t^{8} + 4 t^{6})\,dt$
- $\int_{0}^{2}(- 9 t^{10} - 16 t^{9})\,dt$
- $\int_{0}^{2}(9 t^{10})\,dt$
- $\int_{0}^{2}(16 t^{9})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{3},\,y=t^{4}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(3 y^{2})\,i+(4 x^{2})\,j \\  & =(3 (t^{4})^{2})\,i+(4 (t^{3})^{2})\,j \\  & =(3 t^{8})\,i+(4 t^{6})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{4})j \\  & =(3 t^{2})\,i+(4 t^{3})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t^{8})\,i+(4 t^{6})\,j)\cdot ((3 t^{2})\,i+(4 t^{3})\,j) \\  & =(3 t^{8})\cdot (3 t^{2})+(4 t^{6})\cdot (4 t^{3}) \\  & =9 t^{10} + 16 t^{9}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{2}(9 t^{10} + 16 t^{9})\,dt.\end{aligned}
$$

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 y^{2})\,i+(3 x^{2})\,j$ and $C$ is the path $r(t)=(t^{3})\,i+(t^{2})\,j$ for $t\in [0,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{3}(6 t^{7} - 6 t^{6})\,dt$ **Correct**
- $\int_{0}^{3}(- 6 t^{6})\,dt$
- $\int_{0}^{3}(- 6 t^{7} + 6 t^{6})\,dt$
- $\int_{0}^{3}(3 t^{6} - 2 t^{4})\,dt$
- $\int_{0}^{3}(6 t^{7})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{3},\,y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y^{2})\,i+(3 x^{2})\,j \\  & =(- 2 (t^{2})^{2})\,i+(3 (t^{3})^{2})\,j \\  & =(- 2 t^{4})\,i+(3 t^{6})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})j \\  & =(3 t^{2})\,i+(2 t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t^{4})\,i+(3 t^{6})\,j)\cdot ((3 t^{2})\,i+(2 t)\,j) \\  & =(- 2 t^{4})\cdot (3 t^{2})+(3 t^{6})\cdot (2 t) \\  & =6 t^{7} - 6 t^{6}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{3}(6 t^{7} - 6 t^{6})\,dt.\end{aligned}
$$

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(x + 2 y)\,i+(- x - 2 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{4 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{4 \pi}{3}}(0)\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(- 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - t^{2} \cos^{2}{\left(t \right)} - 2 t \sin^{2}{\left(t \right)} - t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 2 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 2 \sin^{2}{\left(t \right)} + \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{4 \pi}{3}}(- t^{2} \left(- 2 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) - t \left(- 2 \sin^{2}{\left(t \right)} + \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(- 2 t^{2} \sin^{2}{\left(t \right)} - t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x + 2 y)\,i+(- x - 2 y)\,j \\  & =((t \cos{\left(t \right)}) + 2 (t \sin{\left(t \right)}))\,i+(- (t \cos{\left(t \right)}) - 2 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((2 t \sin{\left(t \right)} + t \cos{\left(t \right)})\,i+(- 2 t \sin{\left(t \right)} - t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(2 t \sin{\left(t \right)} + t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 2 t \sin{\left(t \right)} - t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(2 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(- 2 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 2 t^{2} \sin^{2}{\left(t \right)} - 3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - t^{2} \cos^{2}{\left(t \right)} - 2 t \sin^{2}{\left(t \right)} + t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- 2 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 2 \sin^{2}{\left(t \right)} + \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{4 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 2 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 2 \sin^{2}{\left(t \right)} + \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 4 x + 3 y)\,i+(- 4 x + 4 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{4 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{4 \pi}{3}}(4 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t^{2} \cos^{2}{\left(t \right)} + 4 t \sin^{2}{\left(t \right)} - 4 t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 3 \sin^{2}{\left(t \right)} + 8 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(4 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{4 \pi}{3}}(7 t \sin{\left(t \right)} - 8 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(- t^{2} \left(- 3 \sin^{2}{\left(t \right)} + 8 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) - t \left(4 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right))\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(- 3 t^{2} \sin^{2}{\left(t \right)} + 4 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 3 t \sin{\left(t \right)} \cos{\left(t \right)} - 4 t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 4 x + 3 y)\,i+(- 4 x + 4 y)\,j \\  & =(- 4 (t \cos{\left(t \right)}) + 3 (t \sin{\left(t \right)}))\,i+(- 4 (t \cos{\left(t \right)}) + 4 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\,i+(4 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(3 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(4 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(- 4 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 4 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(4 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 3 t^{2} \sin^{2}{\left(t \right)} + 8 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t^{2} \cos^{2}{\left(t \right)} + 4 t \sin^{2}{\left(t \right)} - t \sin{\left(t \right)} \cos{\left(t \right)} - 4 t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- 3 \sin^{2}{\left(t \right)} + 8 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(4 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{4 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 3 \sin^{2}{\left(t \right)} + 8 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(4 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$