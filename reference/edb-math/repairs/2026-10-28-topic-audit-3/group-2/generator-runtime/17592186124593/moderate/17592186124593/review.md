# Source and generated review

8 practice sources; 6 easy, 2 moderate. All 40 options and all source stages preserved; q-94878 has one supported basis-vector repair.

## Original q-36215

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that
$∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j$
and
$r(t)=t\,i+{t}^{2}\,j.$

- $\frac{1}{2}$
- $6$
- $1$
- $2$
- $4$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j.
$$

First, we substitute $x=t$ and $y={t}^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{2(t)}{(t)^{2}+3({t}^{2})}\,i+\frac{3}{(t)^{2}+3({t}^{2})}\,j \\  & =\frac{2t}{{t}^{2}+3{t}^{2}}\,i+\frac{3}{{t}^{2}+3{t}^{2}}\,j \\  & =\frac{2t}{4{t}^{2}}\,i+\frac{3}{4{t}^{2}}\,j \\  & =\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =i+2t\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j)\cdot (i+2t\,j) \\  & =(\frac{1}{2t})\cdot 1+(\frac{3}{4{t}^{2}})\cdot 2t \\  & =\frac{1}{2t}+\frac{3}{2t} \\  & =\frac{4}{2t} \\  & =\frac{2}{t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2}{1}=2.\end{aligned}
$$

## Parameterized source replay — evidence-only

### log_rational — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that
$∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j$
and
$r(t)=t\,i+{t}^{2}\,j.$

- $1$
- $6$
- $\frac{1}{2}$
- $4$
- $2$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j.
$$

First, we substitute $x=t$ and $y={t}^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{2(t)}{(t)^{2}+3({t}^{2})}\,i+\frac{3}{(t)^{2}+3({t}^{2})}\,j \\  & =\frac{2t}{{t}^{2}+3{t}^{2}}\,i+\frac{3}{{t}^{2}+3{t}^{2}}\,j \\  & =\frac{2t}{4{t}^{2}}\,i+\frac{3}{4{t}^{2}}\,j \\  & =\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =i+2t\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j)\cdot (i+2t\,j) \\  & =(\frac{1}{2t})\cdot 1+(\frac{3}{4{t}^{2}})\cdot 2t \\  & =\frac{1}{2t}+\frac{3}{2t} \\  & =\frac{4}{2t} \\  & =\frac{2}{t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2}{1}=2.\end{aligned}
$$

## Original q-94872

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{2}$ given that $∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j$ and $r(t)=\frac{t}{2}\,i+t\,j.$

- $2-\pi $
- $0$
- $\frac{\pi }{4}$
- $\frac{1}{2}$
- $-1$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j.
$$

First, we substitute $x=\frac{t}{2}$ and $y=t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =\frac{1}{2}\,i+j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j)\cdot (\frac{1}{2}\,i+j) \\  & =\operatorname{sin}⁡t\cdot \frac{1}{2}+\frac{t}{2}\operatorname{cos}⁡t\cdot 1 \\  & =\frac{1}{2}(\operatorname{sin}⁡t+t\operatorname{cos}⁡t).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{2}))] & =\frac{1}{2}(\operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\operatorname{cos}⁡(\frac{\pi }{2})) \\  & =\frac{1}{2}(1+\frac{\pi }{2}\cdot 0) \\  & =\frac{1}{2}.\end{aligned}
$$

## Parameterized source replay — evidence-only

### sin_y — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{2}$ given that $∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j$ and $r(t)=\frac{t}{2}\,i+t\,j.$

- $\frac{\pi }{4}$
- $0$
- $2-\pi $
- $-1$
- $\frac{1}{2}$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j.
$$

First, we substitute $x=\frac{t}{2}$ and $y=t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =\frac{1}{2}\,i+j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j)\cdot (\frac{1}{2}\,i+j) \\  & =\operatorname{sin}⁡t\cdot \frac{1}{2}+\frac{t}{2}\operatorname{cos}⁡t\cdot 1 \\  & =\frac{1}{2}(\operatorname{sin}⁡t+t\operatorname{cos}⁡t).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{2}))] & =\frac{1}{2}(\operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\operatorname{cos}⁡(\frac{\pi }{2})) \\  & =\frac{1}{2}(1+\frac{\pi }{2}\cdot 0) \\  & =\frac{1}{2}.\end{aligned}
$$

## Original q-167497

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\pi $ given that $∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j$ and $r(t)=\sqrt{t}\,i+\frac{t}{2}\,j.$

- $-2\pi $
- $\frac{1}{2}$
- $\pi $
- $-\frac{\pi }{2}$
- $-1$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j.
$$

First, we substitute $x=\sqrt{t}$ and $y=\frac{t}{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & ={t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,j \\  & =\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j)\cdot (\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j) \\  & ={t}^{3/2}\operatorname{cos}⁡(t)\cdot \frac{1}{2\sqrt{t}}+\operatorname{sin}⁡t\cdot \frac{1}{2} \\  & =\frac{t\operatorname{cos}⁡t+\operatorname{sin}⁡t}{2}.\end{aligned}
$$

Finally, evaluating the above at $t=\pi ,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\pi ))] & =\frac{\pi \operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi }{2} \\  & =\frac{\pi (-1)+0}{2} \\  & =-\frac{\pi }{2}.\end{aligned}
$$

## Parameterized source replay — evidence-only

### sqrt_sine — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\pi $ given that $∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j$ and $r(t)=\sqrt{t}\,i+\frac{t}{2}\,j.$

- $\pi $
- $\frac{1}{2}$
- $-2\pi $
- $-1$
- $-\frac{\pi }{2}$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j.
$$

First, we substitute $x=\sqrt{t}$ and $y=\frac{t}{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & ={t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,j \\  & =\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j)\cdot (\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j) \\  & ={t}^{3/2}\operatorname{cos}⁡(t)\cdot \frac{1}{2\sqrt{t}}+\operatorname{sin}⁡t\cdot \frac{1}{2} \\  & =\frac{t\operatorname{cos}⁡t+\operatorname{sin}⁡t}{2}.\end{aligned}
$$

Finally, evaluating the above at $t=\pi ,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\pi ))] & =\frac{\pi \operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi }{2} \\  & =\frac{\pi (-1)+0}{2} \\  & =-\frac{\pi }{2}.\end{aligned}
$$

## Original q-167498

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=-1$ given that $∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j$ and $r(t)=\operatorname{sin}⁡t\text{ }i+(t+{cos}^{2}⁡t)\text{ }j.$

- $1$
- $\frac{2}{e}$
- $2e$
- $e$
- $\frac{1}{2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j.
$$

First, we substitute $x=\operatorname{sin}⁡t$ and $y=t+{cos}^{2}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\operatorname{sin}⁡t\,{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,i+{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,j \\  & =2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(t+{cos}^{2}⁡t)\,j \\  & =\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j)\cdot (\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j) \\  & =2{e}^{t+1}\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t+{e}^{t+1}\cdot (1-2\operatorname{sin}⁡t\operatorname{cos}⁡t) \\  & =2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t+{e}^{t+1}-2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t \\  & ={e}^{t+1}.\end{aligned}
$$

Finally, evaluating the above at $t=-1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & ={e}^{-1+1}=1.\end{aligned}
$$

## Parameterized source replay — evidence-only

### exp_cancel — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=-1$ given that $∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j$ and $r(t)=\operatorname{sin}⁡t\text{ }i+(t+{cos}^{2}⁡t)\text{ }j.$

- $2e$
- $\frac{2}{e}$
- $1$ **correct**
- $\frac{1}{2}$
- $e$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j.
$$

First, we substitute $x=\operatorname{sin}⁡t$ and $y=t+{cos}^{2}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\operatorname{sin}⁡t\,{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,i+{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,j \\  & =2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(t+{cos}^{2}⁡t)\,j \\  & =\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j)\cdot (\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j) \\  & =2{e}^{t+1}\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t+{e}^{t+1}\cdot (1-2\operatorname{sin}⁡t\operatorname{cos}⁡t) \\  & =2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t+{e}^{t+1}-2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t \\  & ={e}^{t+1}.\end{aligned}
$$

Finally, evaluating the above at $t=-1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & ={e}^{-1+1}=1.\end{aligned}
$$

## Original q-37106

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j$ and $r(t)=(2{t}^{2}+2)\,i+\operatorname{arctan}⁡t\,j.$

- $1$
- $\frac{\pi +2}{\pi }$
- $\frac{\pi +1}{\pi }$
- $\frac{\pi }{\pi +2}$
- $\frac{\pi }{\pi +1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j.
$$

First, we substitute $x=2{t}^{2}+2$ and $y=\operatorname{arctan}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\frac{1}{2{t}^{2}+2}\text{ }i+\frac{1}{\operatorname{arctan}⁡t}\text{ }j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{2}+2)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{arctan}⁡t)\,j \\  & =4t\,i+\frac{1}{1+{t}^{2}}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2{t}^{2}+2}\,i+\frac{1}{\operatorname{arctan}⁡t}\,j)\cdot (4t\,i+\frac{1}{1+{t}^{2}}\,j) \\  & =\frac{1}{2{t}^{2}+2}\cdot 4t+\frac{1}{\operatorname{arctan}⁡t}\cdot \frac{1}{1+{t}^{2}} \\  & =\frac{2t}{{t}^{2}+1}+\frac{1}{({t}^{2}+1)\operatorname{arctan}⁡t} \\  & =\frac{2t\operatorname{arctan}⁡t+1}{({t}^{2}+1)\operatorname{arctan}⁡t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2(1)\operatorname{arctan}⁡1+1}{({1}^{2}+1)\operatorname{arctan}⁡1} \\  & =\frac{(2\cdot \frac{\pi }{4}+1)}{(2\cdot \frac{\pi }{4})} \\  & =\frac{\pi +2}{\pi }.\end{aligned}
$$

## Parameterized source replay — evidence-only

### atan_log — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j$ and $r(t)=(2{t}^{2}+2)\,i+\operatorname{arctan}⁡t\,j.$

- $\frac{\pi +1}{\pi }$
- $\frac{\pi +2}{\pi }$ **correct**
- $1$
- $\frac{\pi }{\pi +1}$
- $\frac{\pi }{\pi +2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j.
$$

First, we substitute $x=2{t}^{2}+2$ and $y=\operatorname{arctan}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\frac{1}{2{t}^{2}+2}\text{ }i+\frac{1}{\operatorname{arctan}⁡t}\text{ }j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{2}+2)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{arctan}⁡t)\,j \\  & =4t\,i+\frac{1}{1+{t}^{2}}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2{t}^{2}+2}\,i+\frac{1}{\operatorname{arctan}⁡t}\,j)\cdot (4t\,i+\frac{1}{1+{t}^{2}}\,j) \\  & =\frac{1}{2{t}^{2}+2}\cdot 4t+\frac{1}{\operatorname{arctan}⁡t}\cdot \frac{1}{1+{t}^{2}} \\  & =\frac{2t}{{t}^{2}+1}+\frac{1}{({t}^{2}+1)\operatorname{arctan}⁡t} \\  & =\frac{2t\operatorname{arctan}⁡t+1}{({t}^{2}+1)\operatorname{arctan}⁡t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =\frac{2(1)\operatorname{arctan}⁡1+1}{({1}^{2}+1)\operatorname{arctan}⁡1} \\  & =\frac{(2\cdot \frac{\pi }{4}+1)}{(2\cdot \frac{\pi }{4})} \\  & =\frac{\pi +2}{\pi }.\end{aligned}
$$

## Original q-37109

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=0$ given that $∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡(2t)\,j.$

- $3$
- $4$
- $2$
- $1$
- $0$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j.
$$

First, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡(2t)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\operatorname{sin}⁡(2t)(\operatorname{ln}⁡{e}^{2t}+1)\,i+{e}^{2t}\operatorname{ln}⁡{e}^{2t}\,j \\  & =\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2t))\,j \\  & =2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j)\cdot (2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j) \\  & =2{e}^{2t}(2t+1)\operatorname{sin}⁡(2t)+4t{e}^{2t}\operatorname{cos}⁡(2t) \\  & =2{e}^{2t}[(2t+1)\operatorname{sin}⁡(2t)+2t\operatorname{cos}⁡(2t)].\end{aligned}
$$

Finally, evaluating the above at $t=0,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2{e}^{2(0)}((2(0)+1)\operatorname{sin}⁡(2(0))+2(0)\operatorname{cos}⁡(2(0)))=0.\end{aligned}
$$

## Parameterized source replay — evidence-only

### log_sine — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=0$ given that $∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡(2t)\,j.$

- $2$
- $4$
- $3$
- $0$ **correct**
- $1$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j.
$$

First, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡(2t)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\operatorname{sin}⁡(2t)(\operatorname{ln}⁡{e}^{2t}+1)\,i+{e}^{2t}\operatorname{ln}⁡{e}^{2t}\,j \\  & =\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2t))\,j \\  & =2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j)\cdot (2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j) \\  & =2{e}^{2t}(2t+1)\operatorname{sin}⁡(2t)+4t{e}^{2t}\operatorname{cos}⁡(2t) \\  & =2{e}^{2t}[(2t+1)\operatorname{sin}⁡(2t)+2t\operatorname{cos}⁡(2t)].\end{aligned}
$$

Finally, evaluating the above at $t=0,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2{e}^{2(0)}((2(0)+1)\operatorname{sin}⁡(2(0))+2(0)\operatorname{cos}⁡(2(0)))=0.\end{aligned}
$$

## Original q-94873

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=2x\,i+2y\,j$ and $r(t)={e}^{-t}\,i+{e}^{t}\,j.$

- $2-3{e}^{-1}$
- $3e+{e}^{-1}$
- $2{e}^{2}-2{e}^{-2}$
- $4{e}^{2}$
- $-4{e}^{-1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x\,i+2y\,j.
$$

First, we substitute $x={e}^{-t}$ and $y={e}^{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{-t}\,i+2{e}^{t}\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =(-{e}^{-t})\,i+{e}^{t}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{-t}\,i+2{e}^{t}\,j)\cdot ((-{e}^{-t})\,i+{e}^{t}\,j) \\  & =2{e}^{-t}\cdot (-{e}^{-t})+2{e}^{t}\cdot {e}^{t} \\  & =2{e}^{2t}-2{e}^{-2t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2{e}^{2(1)}-2{e}^{-2(1)} \\  & =2{e}^{2}-2{e}^{-2}.\end{aligned}
$$

## Parameterized source replay — evidence-only

### exp_quadratic — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=2x\,i+2y\,j$ and $r(t)={e}^{-t}\,i+{e}^{t}\,j.$

- $2{e}^{2}-2{e}^{-2}$ **correct**
- $3e+{e}^{-1}$
- $2-3{e}^{-1}$
- $-4{e}^{-1}$
- $4{e}^{2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x\,i+2y\,j.
$$

First, we substitute $x={e}^{-t}$ and $y={e}^{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{-t}\,i+2{e}^{t}\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =(-{e}^{-t})\,i+{e}^{t}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{-t}\,i+2{e}^{t}\,j)\cdot ((-{e}^{-t})\,i+{e}^{t}\,j) \\  & =2{e}^{-t}\cdot (-{e}^{-t})+2{e}^{t}\cdot {e}^{t} \\  & =2{e}^{2t}-2{e}^{-2t}.\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2{e}^{2(1)}-2{e}^{-2(1)} \\  & =2{e}^{2}-2{e}^{-2}.\end{aligned}
$$

## Original q-94878

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{8}$ given that $∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j$ and $r(t)=2\sqrt{t}\,i-2\sqrt{t}\,j.$

- $-4$
- $0$
- $2$
- $-\frac{\sqrt{\pi }}{2}$
- $\frac{\sqrt{\pi }}{4}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.
$$

First, we substitute $x=2\sqrt{t}$ and $y=-2\sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-(-2\sqrt{t})\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,i-2\sqrt{t}\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,j \\  & =-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{t})\,j \\  & =\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j)\cdot (\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})i) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t))\cdot \frac{1}{\sqrt{t}}+2\sqrt{t}\operatorname{sin}⁡(4t)\cdot (-\frac{1}{\sqrt{t}}) \\  & =-2\operatorname{sin}⁡(4t)-2\operatorname{sin}⁡(4t) \\  & =-4\operatorname{sin}⁡(4t).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{8}))] & =-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8}) \\  & =-4\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =-4.\end{aligned}
$$

## Public raw erroneous source replay — evidence-only

### sqrt_product — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{8}$ given that $∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j$ and $r(t)=2\sqrt{t}\,i-2\sqrt{t}\,j.$

- $2$
- $0$
- $-4$ **correct**
- $\frac{\sqrt{\pi }}{4}$
- $-\frac{\sqrt{\pi }}{2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.
$$

First, we substitute $x=2\sqrt{t}$ and $y=-2\sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-(-2\sqrt{t})\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,i-2\sqrt{t}\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,j \\  & =-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{t})\,j \\  & =\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j)\cdot (\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})i) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t))\cdot \frac{1}{\sqrt{t}}+2\sqrt{t}\operatorname{sin}⁡(4t)\cdot (-\frac{1}{\sqrt{t}}) \\  & =-2\operatorname{sin}⁡(4t)-2\operatorname{sin}⁡(4t) \\  & =-4\operatorname{sin}⁡(4t).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{8}))] & =-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8}) \\  & =-4\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =-4.\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_rational — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that
$∇f(x,y)=2\cdot \left(\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j\right)$
and
$r(t)=t\,i+{t}^{2}\,j.$

- $2\cdot \left(1\right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(6\right)$
- $2\cdot \left(4\right)$
- $2\cdot \left(2\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j.\right)
$$

First, we substitute $x=t$ and $y={t}^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left(\frac{2(t)}{(t)^{2}+3({t}^{2})}\,i+\frac{3}{(t)^{2}+3({t}^{2})}\,j\right) \\  & =2\cdot \left(\frac{2t}{{t}^{2}+3{t}^{2}}\,i+\frac{3}{{t}^{2}+3{t}^{2}}\,j\right) \\  & =2\cdot \left(\frac{2t}{4{t}^{2}}\,i+\frac{3}{4{t}^{2}}\,j\right) \\  & =2\cdot \left(\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =i+2t\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((\frac{1}{2t}\,i+\frac{3}{4{t}^{2}}\,j)\right)\cdot (i+2t\,j) \\  & =2\cdot \left((\frac{1}{2t})\cdot 1+(\frac{3}{4{t}^{2}})\cdot 2t\right) \\  & =2\cdot \left(\frac{1}{2t}+\frac{3}{2t}\right) \\  & =2\cdot \left(\frac{4}{2t}\right) \\  & =2\cdot \left(\frac{2}{t}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2\cdot \left(\frac{2}{1}\right)=2\cdot \left(2.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_rational — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{2}$ given that
$∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j$
and
$r(t)=\left(2t\right)\,i+{\left(2t\right)}^{2}\,j.$

- $2\cdot \left(1\right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(6\right)$
- $2\cdot \left(4\right)$
- $2\cdot \left(2\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j.
$$

First, we substitute $x=\left(2t\right)$ and $y={\left(2t\right)}^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{2(\left(2t\right))}{(\left(2t\right))^{2}+3({\left(2t\right)}^{2})}\,i+\frac{3}{(\left(2t\right))^{2}+3({\left(2t\right)}^{2})}\,j \\  & =\frac{2\left(2t\right)}{{\left(2t\right)}^{2}+3{\left(2t\right)}^{2}}\,i+\frac{3}{{\left(2t\right)}^{2}+3{\left(2t\right)}^{2}}\,j \\  & =\frac{2\left(2t\right)}{4{\left(2t\right)}^{2}}\,i+\frac{3}{4{\left(2t\right)}^{2}}\,j \\  & =\frac{1}{2\left(2t\right)}\,i+\frac{3}{4{\left(2t\right)}^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\left(2t\right))\,i+\frac{\text{d}}{\text{d}t}({\left(2t\right)}^{2})\,j \\  & =2\cdot \left(i+2\left(2t\right)\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2\left(2t\right)}\,i+\frac{3}{4{\left(2t\right)}^{2}}\,j)\cdot2\cdot \left( (i+2\left(2t\right)\,j)\right) \\  & =2\cdot \left((\frac{1}{2\left(2t\right)})\cdot 1+(\frac{3}{4{\left(2t\right)}^{2}})\cdot 2\left(2t\right)\right) \\  & =2\cdot \left(\frac{1}{2\left(2t\right)}+\frac{3}{2\left(2t\right)}\right) \\  & =2\cdot \left(\frac{4}{2\left(2t\right)}\right) \\  & =2\cdot \left(\frac{2}{\left(2t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{2}))] & =2\cdot \left(\frac{2}{1}\right)=2\cdot \left(2.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_rational — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{3}$ given that
$∇f(x,y)=3\cdot \left(\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j\right)$
and
$r(t)=\left(3t\right)\,i+{\left(3t\right)}^{2}\,j.$

- $9\cdot \left(1\right)$
- $9\cdot \left(\frac{1}{2}\right)$
- $9\cdot \left(6\right)$
- $9\cdot \left(4\right)$
- $9\cdot \left(2\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(\frac{2x}{{x}^{2}+3y}\,i+\frac{3}{{x}^{2}+3y}\,j.\right)
$$

First, we substitute $x=\left(3t\right)$ and $y={\left(3t\right)}^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left(\frac{2(\left(3t\right))}{(\left(3t\right))^{2}+3({\left(3t\right)}^{2})}\,i+\frac{3}{(\left(3t\right))^{2}+3({\left(3t\right)}^{2})}\,j\right) \\  & =3\cdot \left(\frac{2\left(3t\right)}{{\left(3t\right)}^{2}+3{\left(3t\right)}^{2}}\,i+\frac{3}{{\left(3t\right)}^{2}+3{\left(3t\right)}^{2}}\,j\right) \\  & =3\cdot \left(\frac{2\left(3t\right)}{4{\left(3t\right)}^{2}}\,i+\frac{3}{4{\left(3t\right)}^{2}}\,j\right) \\  & =3\cdot \left(\frac{1}{2\left(3t\right)}\,i+\frac{3}{4{\left(3t\right)}^{2}}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\left(3t\right))\,i+\frac{\text{d}}{\text{d}t}({\left(3t\right)}^{2})\,j \\  & =3\cdot \left(i+2\left(3t\right)\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((\frac{1}{2\left(3t\right)}\,i+\frac{3}{4{\left(3t\right)}^{2}}\,j)\right)\cdot3\cdot \left( (i+2\left(3t\right)\,j)\right) \\  & =9\cdot \left((\frac{1}{2\left(3t\right)})\cdot 1+(\frac{3}{4{\left(3t\right)}^{2}})\cdot 2\left(3t\right)\right) \\  & =9\cdot \left(\frac{1}{2\left(3t\right)}+\frac{3}{2\left(3t\right)}\right) \\  & =9\cdot \left(\frac{4}{2\left(3t\right)}\right) \\  & =9\cdot \left(\frac{2}{\left(3t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{3},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{3}))] & =9\cdot \left(\frac{2}{1}\right)=9\cdot \left(2.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sin_y — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{2}$ given that $∇f(x,y)=2\cdot \left(\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j\right)$ and $r(t)=\frac{t}{2}\,i+t\,j.$

- $2\cdot \left(\frac{\pi }{4}\right)$
- $2\cdot \left(2-\pi \right)$
- $2\cdot \left(0\right)$
- $2\cdot \left(-1\right)$
- $2\cdot \left(\frac{1}{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j.\right)
$$

First, we substitute $x=\frac{t}{2}$ and $y=t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left(\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =\frac{1}{2}\,i+j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((\operatorname{sin}⁡t\,i+\frac{t}{2}\operatorname{cos}⁡t\,j)\right)\cdot (\frac{1}{2}\,i+j) \\  & =2\cdot \left(\operatorname{sin}⁡t\cdot \frac{1}{2}+\frac{t}{2}\operatorname{cos}⁡t\cdot 1\right) \\  & =2\cdot \left(\frac{1}{2}(\operatorname{sin}⁡t+t\operatorname{cos}⁡t).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{2}))] & =2\cdot \left(\frac{1}{2}(\operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\operatorname{cos}⁡(\frac{\pi }{2}))\right) \\  & =2\cdot \left(\frac{1}{2}(1+\frac{\pi }{2}\cdot 0)\right) \\  & =2\cdot \left(\frac{1}{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sin_y — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{4}$ given that $∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j$ and $r(t)=\frac{\left(2t\right)}{2}\,i+\left(2t\right)\,j.$

- $2\cdot \left(\frac{\pi }{4}\right)$
- $2\cdot \left(2-\pi \right)$
- $2\cdot \left(0\right)$
- $2\cdot \left(-1\right)$
- $2\cdot \left(\frac{1}{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j.
$$

First, we substitute $x=\frac{\left(2t\right)}{2}$ and $y=\left(2t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\operatorname{sin}⁡\left(2t\right)\,i+\frac{\left(2t\right)}{2}\operatorname{cos}⁡\left(2t\right)\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{\left(2t\right)}{2})\,i+\frac{\text{d}}{\text{d}t}(\left(2t\right))\,j \\  & =2\cdot \left(\frac{1}{2}\,i+j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡\left(2t\right)\,i+\frac{\left(2t\right)}{2}\operatorname{cos}⁡\left(2t\right)\,j)\cdot2\cdot \left( (\frac{1}{2}\,i+j)\right) \\  & =2\cdot \left(\operatorname{sin}⁡\left(2t\right)\cdot \frac{1}{2}+\frac{\left(2t\right)}{2}\operatorname{cos}⁡\left(2t\right)\cdot 1\right) \\  & =2\cdot \left(\frac{1}{2}(\operatorname{sin}⁡\left(2t\right)+\left(2t\right)\operatorname{cos}⁡\left(2t\right)).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{4},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{4}))] & =2\cdot \left(\frac{1}{2}(\operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\operatorname{cos}⁡(\frac{\pi }{2}))\right) \\  & =2\cdot \left(\frac{1}{2}(1+\frac{\pi }{2}\cdot 0)\right) \\  & =2\cdot \left(\frac{1}{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sin_y — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{6}$ given that $∇f(x,y)=3\cdot \left(\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j\right)$ and $r(t)=\frac{\left(3t\right)}{2}\,i+\left(3t\right)\,j.$

- $9\cdot \left(\frac{\pi }{4}\right)$
- $9\cdot \left(2-\pi \right)$
- $9\cdot \left(0\right)$
- $9\cdot \left(-1\right)$
- $9\cdot \left(\frac{1}{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(\operatorname{sin}⁡y\,i+x\operatorname{cos}⁡y\,j.\right)
$$

First, we substitute $x=\frac{\left(3t\right)}{2}$ and $y=\left(3t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left(\operatorname{sin}⁡\left(3t\right)\,i+\frac{\left(3t\right)}{2}\operatorname{cos}⁡\left(3t\right)\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{\left(3t\right)}{2})\,i+\frac{\text{d}}{\text{d}t}(\left(3t\right))\,j \\  & =3\cdot \left(\frac{1}{2}\,i+j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((\operatorname{sin}⁡\left(3t\right)\,i+\frac{\left(3t\right)}{2}\operatorname{cos}⁡\left(3t\right)\,j)\right)\cdot3\cdot \left( (\frac{1}{2}\,i+j)\right) \\  & =9\cdot \left(\operatorname{sin}⁡\left(3t\right)\cdot \frac{1}{2}+\frac{\left(3t\right)}{2}\operatorname{cos}⁡\left(3t\right)\cdot 1\right) \\  & =9\cdot \left(\frac{1}{2}(\operatorname{sin}⁡\left(3t\right)+\left(3t\right)\operatorname{cos}⁡\left(3t\right)).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{6},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{6}))] & =9\cdot \left(\frac{1}{2}(\operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\operatorname{cos}⁡(\frac{\pi }{2}))\right) \\  & =9\cdot \left(\frac{1}{2}(1+\frac{\pi }{2}\cdot 0)\right) \\  & =9\cdot \left(\frac{1}{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_sine — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\pi $ given that $∇f(x,y)=2\cdot \left(2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j\right)$ and $r(t)=\sqrt{t}\,i+\frac{t}{2}\,j.$

- $2\cdot \left(\pi \right)$
- $2\cdot \left(-2\pi \right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(-1\right)$
- $2\cdot \left(-\frac{\pi }{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j.\right)
$$

First, we substitute $x=\sqrt{t}$ and $y=\frac{t}{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left({t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(\frac{t}{2})\,j \\  & =\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left(({t}^{3/2}\operatorname{cos}⁡(t)\,i+\operatorname{sin}⁡(t)\,j)\right)\cdot (\frac{1}{2\sqrt{t}}\,i+\frac{1}{2}j) \\  & =2\cdot \left({t}^{3/2}\operatorname{cos}⁡(t)\cdot \frac{1}{2\sqrt{t}}+\operatorname{sin}⁡t\cdot \frac{1}{2}\right) \\  & =2\cdot \left(\frac{t\operatorname{cos}⁡t+\operatorname{sin}⁡t}{2}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\pi ,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\pi ))] & =2\cdot \left(\frac{\pi \operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi }{2}\right) \\  & =2\cdot \left(\frac{\pi (-1)+0}{2}\right) \\  & =2\cdot \left(-\frac{\pi }{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_sine — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{2}$ given that $∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j$ and $r(t)=\sqrt{\left(2t\right)}\,i+\frac{\left(2t\right)}{2}\,j.$

- $2\cdot \left(\pi \right)$
- $2\cdot \left(-2\pi \right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(-1\right)$
- $2\cdot \left(-\frac{\pi }{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j.
$$

First, we substitute $x=\sqrt{\left(2t\right)}$ and $y=\frac{\left(2t\right)}{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & ={\left(2t\right)}^{3/2}\operatorname{cos}⁡(\left(2t\right))\,i+\operatorname{sin}⁡(\left(2t\right))\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sqrt{\left(2t\right)})\,i+\frac{\text{d}}{\text{d}t}(\frac{\left(2t\right)}{2})\,j \\  & =2\cdot \left(\frac{1}{2\sqrt{\left(2t\right)}}\,i+\frac{1}{2}j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({\left(2t\right)}^{3/2}\operatorname{cos}⁡(\left(2t\right))\,i+\operatorname{sin}⁡(\left(2t\right))\,j)\cdot2\cdot \left( (\frac{1}{2\sqrt{\left(2t\right)}}\,i+\frac{1}{2}j)\right) \\  & =2\cdot \left({\left(2t\right)}^{3/2}\operatorname{cos}⁡(\left(2t\right))\cdot \frac{1}{2\sqrt{\left(2t\right)}}+\operatorname{sin}⁡\left(2t\right)\cdot \frac{1}{2}\right) \\  & =2\cdot \left(\frac{\left(2t\right)\operatorname{cos}⁡\left(2t\right)+\operatorname{sin}⁡\left(2t\right)}{2}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{2}))] & =2\cdot \left(\frac{\pi \operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi }{2}\right) \\  & =2\cdot \left(\frac{\pi (-1)+0}{2}\right) \\  & =2\cdot \left(-\frac{\pi }{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_sine — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{3}$ given that $∇f(x,y)=3\cdot \left(2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j\right)$ and $r(t)=\sqrt{\left(3t\right)}\,i+\frac{\left(3t\right)}{2}\,j.$

- $9\cdot \left(\pi \right)$
- $9\cdot \left(-2\pi \right)$
- $9\cdot \left(\frac{1}{2}\right)$
- $9\cdot \left(-1\right)$
- $9\cdot \left(-\frac{\pi }{2}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(2xy\operatorname{cos}⁡({x}^{2})\,i+\operatorname{sin}⁡({x}^{2})\,j.\right)
$$

First, we substitute $x=\sqrt{\left(3t\right)}$ and $y=\frac{\left(3t\right)}{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left({\left(3t\right)}^{3/2}\operatorname{cos}⁡(\left(3t\right))\,i+\operatorname{sin}⁡(\left(3t\right))\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\sqrt{\left(3t\right)})\,i+\frac{\text{d}}{\text{d}t}(\frac{\left(3t\right)}{2})\,j \\  & =3\cdot \left(\frac{1}{2\sqrt{\left(3t\right)}}\,i+\frac{1}{2}j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left(({\left(3t\right)}^{3/2}\operatorname{cos}⁡(\left(3t\right))\,i+\operatorname{sin}⁡(\left(3t\right))\,j)\right)\cdot3\cdot \left( (\frac{1}{2\sqrt{\left(3t\right)}}\,i+\frac{1}{2}j)\right) \\  & =9\cdot \left({\left(3t\right)}^{3/2}\operatorname{cos}⁡(\left(3t\right))\cdot \frac{1}{2\sqrt{\left(3t\right)}}+\operatorname{sin}⁡\left(3t\right)\cdot \frac{1}{2}\right) \\  & =9\cdot \left(\frac{\left(3t\right)\operatorname{cos}⁡\left(3t\right)+\operatorname{sin}⁡\left(3t\right)}{2}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{3},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{3}))] & =9\cdot \left(\frac{\pi \operatorname{cos}⁡\pi +\operatorname{sin}⁡\pi }{2}\right) \\  & =9\cdot \left(\frac{\pi (-1)+0}{2}\right) \\  & =9\cdot \left(-\frac{\pi }{2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_cancel — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=-1$ given that $∇f(x,y)=2\cdot \left(2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j\right)$ and $r(t)=\operatorname{sin}⁡t\text{ }i+(t+{cos}^{2}⁡t)\text{ }j.$

- $2\cdot \left(2e\right)$
- $2\cdot \left(1\right)$ **correct**
- $2\cdot \left(\frac{2}{e}\right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(e\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j.\right)
$$

First, we substitute $x=\operatorname{sin}⁡t$ and $y=t+{cos}^{2}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left(2\operatorname{sin}⁡t\,{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,i+{e}^{{sin}^{2}⁡t+t+{cos}^{2}⁡t}\,j\right) \\  & =2\cdot \left(2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(t+{cos}^{2}⁡t)\,j \\  & =\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((2{e}^{t+1}\operatorname{sin}⁡t\,i+{e}^{t+1}\,j)\right)\cdot (\operatorname{cos}⁡t\,i+(1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\,j) \\  & =2\cdot \left(2{e}^{t+1}\operatorname{sin}⁡t\cdot \operatorname{cos}⁡t+{e}^{t+1}\cdot (1-2\operatorname{sin}⁡t\operatorname{cos}⁡t)\right) \\  & =2\cdot \left(2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t+{e}^{t+1}-2{e}^{t+1}\operatorname{sin}⁡t\operatorname{cos}⁡t\right) \\  & =2\cdot \left({e}^{t+1}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=-1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & =2\cdot \left({e}^{-1+1}\right)=2\cdot \left(1.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_cancel — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=- \frac{1}{2}$ given that $∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j$ and $r(t)=\operatorname{sin}⁡\left(2t\right)\text{ }i+(\left(2t\right)+{cos}^{2}⁡\left(2t\right))\text{ }j.$

- $2\cdot \left(2e\right)$
- $2\cdot \left(1\right)$ **correct**
- $2\cdot \left(\frac{2}{e}\right)$
- $2\cdot \left(\frac{1}{2}\right)$
- $2\cdot \left(e\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j.
$$

First, we substitute $x=\operatorname{sin}⁡\left(2t\right)$ and $y=\left(2t\right)+{cos}^{2}⁡\left(2t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\operatorname{sin}⁡\left(2t\right)\,{e}^{{sin}^{2}⁡\left(2t\right)+\left(2t\right)+{cos}^{2}⁡\left(2t\right)}\,i+{e}^{{sin}^{2}⁡\left(2t\right)+\left(2t\right)+{cos}^{2}⁡\left(2t\right)}\,j \\  & =2{e}^{\left(2t\right)+1}\operatorname{sin}⁡\left(2t\right)\,i+{e}^{\left(2t\right)+1}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡\left(2t\right))\,i+\frac{\text{d}}{\text{d}t}(\left(2t\right)+{cos}^{2}⁡\left(2t\right))\,j \\  & =2\cdot \left(\operatorname{cos}⁡\left(2t\right)\,i+(1-2\operatorname{sin}⁡\left(2t\right)\operatorname{cos}⁡\left(2t\right))\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{\left(2t\right)+1}\operatorname{sin}⁡\left(2t\right)\,i+{e}^{\left(2t\right)+1}\,j)\cdot2\cdot \left( (\operatorname{cos}⁡\left(2t\right)\,i+(1-2\operatorname{sin}⁡\left(2t\right)\operatorname{cos}⁡\left(2t\right))\,j)\right) \\  & =2\cdot \left(2{e}^{\left(2t\right)+1}\operatorname{sin}⁡\left(2t\right)\cdot \operatorname{cos}⁡\left(2t\right)+{e}^{\left(2t\right)+1}\cdot (1-2\operatorname{sin}⁡\left(2t\right)\operatorname{cos}⁡\left(2t\right))\right) \\  & =2\cdot \left(2{e}^{\left(2t\right)+1}\operatorname{sin}⁡\left(2t\right)\operatorname{cos}⁡\left(2t\right)+{e}^{\left(2t\right)+1}-2{e}^{\left(2t\right)+1}\operatorname{sin}⁡\left(2t\right)\operatorname{cos}⁡\left(2t\right)\right) \\  & =2\cdot \left({e}^{\left(2t\right)+1}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=- \frac{1}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(- \frac{1}{2}))] & =2\cdot \left({e}^{-1+1}\right)=2\cdot \left(1.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_cancel — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=- \frac{1}{3}$ given that $∇f(x,y)=3\cdot \left(2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j\right)$ and $r(t)=\operatorname{sin}⁡\left(3t\right)\text{ }i+(\left(3t\right)+{cos}^{2}⁡\left(3t\right))\text{ }j.$

- $9\cdot \left(2e\right)$
- $9\cdot \left(1\right)$ **correct**
- $9\cdot \left(\frac{2}{e}\right)$
- $9\cdot \left(\frac{1}{2}\right)$
- $9\cdot \left(e\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(2x{e}^{{x}^{2}+y}\,i+{e}^{{x}^{2}+y}\,j.\right)
$$

First, we substitute $x=\operatorname{sin}⁡\left(3t\right)$ and $y=\left(3t\right)+{cos}^{2}⁡\left(3t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left(2\operatorname{sin}⁡\left(3t\right)\,{e}^{{sin}^{2}⁡\left(3t\right)+\left(3t\right)+{cos}^{2}⁡\left(3t\right)}\,i+{e}^{{sin}^{2}⁡\left(3t\right)+\left(3t\right)+{cos}^{2}⁡\left(3t\right)}\,j\right) \\  & =3\cdot \left(2{e}^{\left(3t\right)+1}\operatorname{sin}⁡\left(3t\right)\,i+{e}^{\left(3t\right)+1}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡\left(3t\right))\,i+\frac{\text{d}}{\text{d}t}(\left(3t\right)+{cos}^{2}⁡\left(3t\right))\,j \\  & =3\cdot \left(\operatorname{cos}⁡\left(3t\right)\,i+(1-2\operatorname{sin}⁡\left(3t\right)\operatorname{cos}⁡\left(3t\right))\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((2{e}^{\left(3t\right)+1}\operatorname{sin}⁡\left(3t\right)\,i+{e}^{\left(3t\right)+1}\,j)\right)\cdot3\cdot \left( (\operatorname{cos}⁡\left(3t\right)\,i+(1-2\operatorname{sin}⁡\left(3t\right)\operatorname{cos}⁡\left(3t\right))\,j)\right) \\  & =9\cdot \left(2{e}^{\left(3t\right)+1}\operatorname{sin}⁡\left(3t\right)\cdot \operatorname{cos}⁡\left(3t\right)+{e}^{\left(3t\right)+1}\cdot (1-2\operatorname{sin}⁡\left(3t\right)\operatorname{cos}⁡\left(3t\right))\right) \\  & =9\cdot \left(2{e}^{\left(3t\right)+1}\operatorname{sin}⁡\left(3t\right)\operatorname{cos}⁡\left(3t\right)+{e}^{\left(3t\right)+1}-2{e}^{\left(3t\right)+1}\operatorname{sin}⁡\left(3t\right)\operatorname{cos}⁡\left(3t\right)\right) \\  & =9\cdot \left({e}^{\left(3t\right)+1}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=- \frac{1}{3},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(- \frac{1}{3}))] & =9\cdot \left({e}^{-1+1}\right)=9\cdot \left(1.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### atan_log — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=2\cdot \left(\frac{1}{x}\,i+\frac{1}{y}\,j\right)$ and $r(t)=(2{t}^{2}+2)\,i+\operatorname{arctan}⁡t\,j.$

- $2\cdot \left(\frac{\pi +1}{\pi }\right)$
- $2\cdot \left(1\right)$
- $2\cdot \left(\frac{\pi +2}{\pi }\right)$ **correct**
- $2\cdot \left(\frac{\pi }{\pi +1}\right)$
- $2\cdot \left(\frac{\pi }{\pi +2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(\frac{1}{x}\,i+\frac{1}{y}\,j.\right)
$$

First, we substitute $x=2{t}^{2}+2$ and $y=\operatorname{arctan}⁡t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =2\cdot \left(\frac{1}{2{t}^{2}+2}\text{ }i+\frac{1}{\operatorname{arctan}⁡t}\text{ }j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{2}+2)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{arctan}⁡t)\,j \\  & =4t\,i+\frac{1}{1+{t}^{2}}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((\frac{1}{2{t}^{2}+2}\,i+\frac{1}{\operatorname{arctan}⁡t}\,j)\right)\cdot (4t\,i+\frac{1}{1+{t}^{2}}\,j) \\  & =2\cdot \left(\frac{1}{2{t}^{2}+2}\cdot 4t+\frac{1}{\operatorname{arctan}⁡t}\cdot \frac{1}{1+{t}^{2}}\right) \\  & =2\cdot \left(\frac{2t}{{t}^{2}+1}+\frac{1}{({t}^{2}+1)\operatorname{arctan}⁡t}\right) \\  & =2\cdot \left(\frac{2t\operatorname{arctan}⁡t+1}{({t}^{2}+1)\operatorname{arctan}⁡t}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2\cdot \left(\frac{2(1)\operatorname{arctan}⁡1+1}{({1}^{2}+1)\operatorname{arctan}⁡1}\right) \\  & =2\cdot \left(\frac{(2\cdot \frac{\pi }{4}+1)}{(2\cdot \frac{\pi }{4})}\right) \\  & =2\cdot \left(\frac{\pi +2}{\pi }.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### atan_log — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{2}$ given that $∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j$ and $r(t)=(2{\left(2t\right)}^{2}+2)\,i+\operatorname{arctan}⁡\left(2t\right)\,j.$

- $2\cdot \left(\frac{\pi +1}{\pi }\right)$
- $2\cdot \left(1\right)$
- $2\cdot \left(\frac{\pi +2}{\pi }\right)$ **correct**
- $2\cdot \left(\frac{\pi }{\pi +1}\right)$
- $2\cdot \left(\frac{\pi }{\pi +2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\frac{1}{x}\,i+\frac{1}{y}\,j.
$$

First, we substitute $x=2{\left(2t\right)}^{2}+2$ and $y=\operatorname{arctan}⁡\left(2t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\frac{1}{2{\left(2t\right)}^{2}+2}\text{ }i+\frac{1}{\operatorname{arctan}⁡\left(2t\right)}\text{ }j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{\left(2t\right)}^{2}+2)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{arctan}⁡\left(2t\right))\,j \\  & =2\cdot \left(4\left(2t\right)\,i+\frac{1}{1+{\left(2t\right)}^{2}}\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{2{\left(2t\right)}^{2}+2}\,i+\frac{1}{\operatorname{arctan}⁡\left(2t\right)}\,j)\cdot2\cdot \left( (4\left(2t\right)\,i+\frac{1}{1+{\left(2t\right)}^{2}}\,j)\right) \\  & =2\cdot \left(\frac{1}{2{\left(2t\right)}^{2}+2}\cdot 4\left(2t\right)+\frac{1}{\operatorname{arctan}⁡\left(2t\right)}\cdot \frac{1}{1+{\left(2t\right)}^{2}}\right) \\  & =2\cdot \left(\frac{2\left(2t\right)}{{\left(2t\right)}^{2}+1}+\frac{1}{({\left(2t\right)}^{2}+1)\operatorname{arctan}⁡\left(2t\right)}\right) \\  & =2\cdot \left(\frac{2\left(2t\right)\operatorname{arctan}⁡\left(2t\right)+1}{({\left(2t\right)}^{2}+1)\operatorname{arctan}⁡\left(2t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{2}))] & =2\cdot \left(\frac{2(1)\operatorname{arctan}⁡1+1}{({1}^{2}+1)\operatorname{arctan}⁡1}\right) \\  & =2\cdot \left(\frac{(2\cdot \frac{\pi }{4}+1)}{(2\cdot \frac{\pi }{4})}\right) \\  & =2\cdot \left(\frac{\pi +2}{\pi }.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### atan_log — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{3}$ given that $∇f(x,y)=3\cdot \left(\frac{1}{x}\,i+\frac{1}{y}\,j\right)$ and $r(t)=(2{\left(3t\right)}^{2}+2)\,i+\operatorname{arctan}⁡\left(3t\right)\,j.$

- $9\cdot \left(\frac{\pi +1}{\pi }\right)$
- $9\cdot \left(1\right)$
- $9\cdot \left(\frac{\pi +2}{\pi }\right)$ **correct**
- $9\cdot \left(\frac{\pi }{\pi +1}\right)$
- $9\cdot \left(\frac{\pi }{\pi +2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(\frac{1}{x}\,i+\frac{1}{y}\,j.\right)
$$

First, we substitute $x=2{\left(3t\right)}^{2}+2$ and $y=\operatorname{arctan}⁡\left(3t\right)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =3\cdot \left(\frac{1}{2{\left(3t\right)}^{2}+2}\text{ }i+\frac{1}{\operatorname{arctan}⁡\left(3t\right)}\text{ }j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{\left(3t\right)}^{2}+2)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{arctan}⁡\left(3t\right))\,j \\  & =3\cdot \left(4\left(3t\right)\,i+\frac{1}{1+{\left(3t\right)}^{2}}\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((\frac{1}{2{\left(3t\right)}^{2}+2}\,i+\frac{1}{\operatorname{arctan}⁡\left(3t\right)}\,j)\right)\cdot3\cdot \left( (4\left(3t\right)\,i+\frac{1}{1+{\left(3t\right)}^{2}}\,j)\right) \\  & =9\cdot \left(\frac{1}{2{\left(3t\right)}^{2}+2}\cdot 4\left(3t\right)+\frac{1}{\operatorname{arctan}⁡\left(3t\right)}\cdot \frac{1}{1+{\left(3t\right)}^{2}}\right) \\  & =9\cdot \left(\frac{2\left(3t\right)}{{\left(3t\right)}^{2}+1}+\frac{1}{({\left(3t\right)}^{2}+1)\operatorname{arctan}⁡\left(3t\right)}\right) \\  & =9\cdot \left(\frac{2\left(3t\right)\operatorname{arctan}⁡\left(3t\right)+1}{({\left(3t\right)}^{2}+1)\operatorname{arctan}⁡\left(3t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{3},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{3}))] & =9\cdot \left(\frac{2(1)\operatorname{arctan}⁡1+1}{({1}^{2}+1)\operatorname{arctan}⁡1}\right) \\  & =9\cdot \left(\frac{(2\cdot \frac{\pi }{4}+1)}{(2\cdot \frac{\pi }{4})}\right) \\  & =9\cdot \left(\frac{\pi +2}{\pi }.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_sine — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=0$ given that $∇f(x,y)=2\cdot \left(y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j\right)$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡(2t)\,j.$

- $2\cdot \left(2\right)$
- $2\cdot \left(3\right)$
- $2\cdot \left(4\right)$
- $2\cdot \left(0\right)$ **correct**
- $2\cdot \left(1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j.\right)
$$

First, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡(2t)$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =2\cdot \left(\operatorname{sin}⁡(2t)(\operatorname{ln}⁡{e}^{2t}+1)\,i+{e}^{2t}\operatorname{ln}⁡{e}^{2t}\,j\right) \\  & =2\cdot \left(\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2t))\,j \\  & =2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((\operatorname{sin}⁡(2t)(2t+1)\,i+2t{e}^{2t}\,j)\right)\cdot (2{e}^{2t}\,i+2\operatorname{cos}⁡(2t)\,j) \\  & =2\cdot \left(2{e}^{2t}(2t+1)\operatorname{sin}⁡(2t)+4t{e}^{2t}\operatorname{cos}⁡(2t)\right) \\  & =2\cdot \left(2{e}^{2t}[(2t+1)\operatorname{sin}⁡(2t)+2t\operatorname{cos}⁡(2t)].\right)\end{aligned}
$$

Finally, evaluating the above at $t=0,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2\cdot \left(2{e}^{2(0)}((2(0)+1)\operatorname{sin}⁡(2(0))+2(0)\operatorname{cos}⁡(2(0)))\right)=2\cdot \left(0.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_sine — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=0$ given that $∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j$ and $r(t)={e}^{2\left(2t\right)}\,i+\operatorname{sin}⁡(2\left(2t\right))\,j.$

- $2\cdot \left(2\right)$
- $2\cdot \left(3\right)$
- $2\cdot \left(4\right)$
- $2\cdot \left(0\right)$ **correct**
- $2\cdot \left(1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j.
$$

First, we substitute $x={e}^{2\left(2t\right)}$ and $y=\operatorname{sin}⁡(2\left(2t\right))$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =\operatorname{sin}⁡(2\left(2t\right))(\operatorname{ln}⁡{e}^{2\left(2t\right)}+1)\,i+{e}^{2\left(2t\right)}\operatorname{ln}⁡{e}^{2\left(2t\right)}\,j \\  & =\operatorname{sin}⁡(2\left(2t\right))(2\left(2t\right)+1)\,i+2\left(2t\right){e}^{2\left(2t\right)}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2\left(2t\right)})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2\left(2t\right)))\,j \\  & =2\cdot \left(2{e}^{2\left(2t\right)}\,i+2\operatorname{cos}⁡(2\left(2t\right))\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\operatorname{sin}⁡(2\left(2t\right))(2\left(2t\right)+1)\,i+2\left(2t\right){e}^{2\left(2t\right)}\,j)\cdot2\cdot \left( (2{e}^{2\left(2t\right)}\,i+2\operatorname{cos}⁡(2\left(2t\right))\,j)\right) \\  & =2\cdot \left(2{e}^{2\left(2t\right)}(2\left(2t\right)+1)\operatorname{sin}⁡(2\left(2t\right))+4\left(2t\right){e}^{2\left(2t\right)}\operatorname{cos}⁡(2\left(2t\right))\right) \\  & =2\cdot \left(2{e}^{2\left(2t\right)}[(2\left(2t\right)+1)\operatorname{sin}⁡(2\left(2t\right))+2\left(2t\right)\operatorname{cos}⁡(2\left(2t\right))].\right)\end{aligned}
$$

Finally, evaluating the above at $t=0,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =2\cdot \left(2{e}^{2(0)}((2(0)+1)\operatorname{sin}⁡(2(0))+2(0)\operatorname{cos}⁡(2(0)))\right)=2\cdot \left(0.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### log_sine — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=0$ given that $∇f(x,y)=3\cdot \left(y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j\right)$ and $r(t)={e}^{2\left(3t\right)}\,i+\operatorname{sin}⁡(2\left(3t\right))\,j.$

- $9\cdot \left(2\right)$
- $9\cdot \left(3\right)$
- $9\cdot \left(4\right)$
- $9\cdot \left(0\right)$ **correct**
- $9\cdot \left(1\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(y(\operatorname{ln}⁡x+1)\,i+x\operatorname{ln}⁡x\,j.\right)
$$

First, we substitute $x={e}^{2\left(3t\right)}$ and $y=\operatorname{sin}⁡(2\left(3t\right))$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇\,f(r(t)) & =3\cdot \left(\operatorname{sin}⁡(2\left(3t\right))(\operatorname{ln}⁡{e}^{2\left(3t\right)}+1)\,i+{e}^{2\left(3t\right)}\operatorname{ln}⁡{e}^{2\left(3t\right)}\,j\right) \\  & =3\cdot \left(\operatorname{sin}⁡(2\left(3t\right))(2\left(3t\right)+1)\,i+2\left(3t\right){e}^{2\left(3t\right)}\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2\left(3t\right)})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2\left(3t\right)))\,j \\  & =3\cdot \left(2{e}^{2\left(3t\right)}\,i+2\operatorname{cos}⁡(2\left(3t\right))\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((\operatorname{sin}⁡(2\left(3t\right))(2\left(3t\right)+1)\,i+2\left(3t\right){e}^{2\left(3t\right)}\,j)\right)\cdot3\cdot \left( (2{e}^{2\left(3t\right)}\,i+2\operatorname{cos}⁡(2\left(3t\right))\,j)\right) \\  & =9\cdot \left(2{e}^{2\left(3t\right)}(2\left(3t\right)+1)\operatorname{sin}⁡(2\left(3t\right))+4\left(3t\right){e}^{2\left(3t\right)}\operatorname{cos}⁡(2\left(3t\right))\right) \\  & =9\cdot \left(2{e}^{2\left(3t\right)}[(2\left(3t\right)+1)\operatorname{sin}⁡(2\left(3t\right))+2\left(3t\right)\operatorname{cos}⁡(2\left(3t\right))].\right)\end{aligned}
$$

Finally, evaluating the above at $t=0,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =9\cdot \left(2{e}^{2(0)}((2(0)+1)\operatorname{sin}⁡(2(0))+2(0)\operatorname{cos}⁡(2(0)))\right)=9\cdot \left(0.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_quadratic — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=2\cdot \left(2x\,i+2y\,j\right)$ and $r(t)={e}^{-t}\,i+{e}^{t}\,j.$

- $2\cdot \left(2{e}^{2}-2{e}^{-2}\right)$ **correct**
- $2\cdot \left(2-3{e}^{-1}\right)$
- $2\cdot \left(3e+{e}^{-1}\right)$
- $2\cdot \left(-4{e}^{-1}\right)$
- $2\cdot \left(4{e}^{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(2x\,i+2y\,j.\right)
$$

First, we substitute $x={e}^{-t}$ and $y={e}^{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left(2{e}^{-t}\,i+2{e}^{t}\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =(-{e}^{-t})\,i+{e}^{t}\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((2{e}^{-t}\,i+2{e}^{t}\,j)\right)\cdot ((-{e}^{-t})\,i+{e}^{t}\,j) \\  & =2\cdot \left(2{e}^{-t}\cdot (-{e}^{-t})+2{e}^{t}\cdot {e}^{t}\right) \\  & =2\cdot \left(2{e}^{2t}-2{e}^{-2t}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =2\cdot \left(2{e}^{2(1)}-2{e}^{-2(1)}\right) \\  & =2\cdot \left(2{e}^{2}-2{e}^{-2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_quadratic — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{2}$ given that $∇f(x,y)=2x\,i+2y\,j$ and $r(t)={e}^{-\left(2t\right)}\,i+{e}^{\left(2t\right)}\,j.$

- $2\cdot \left(2{e}^{2}-2{e}^{-2}\right)$ **correct**
- $2\cdot \left(2-3{e}^{-1}\right)$
- $2\cdot \left(3e+{e}^{-1}\right)$
- $2\cdot \left(-4{e}^{-1}\right)$
- $2\cdot \left(4{e}^{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2x\,i+2y\,j.
$$

First, we substitute $x={e}^{-\left(2t\right)}$ and $y={e}^{\left(2t\right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{-\left(2t\right)}\,i+2{e}^{\left(2t\right)}\,j.\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-\left(2t\right)})\,i+\frac{\text{d}}{\text{d}t}({e}^{\left(2t\right)})\,j \\  & =2\cdot \left((-{e}^{-\left(2t\right)})\,i+{e}^{\left(2t\right)}\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{-\left(2t\right)}\,i+2{e}^{\left(2t\right)}\,j)\cdot2\cdot \left( ((-{e}^{-\left(2t\right)})\,i+{e}^{\left(2t\right)}\,j)\right) \\  & =2\cdot \left(2{e}^{-\left(2t\right)}\cdot (-{e}^{-\left(2t\right)})+2{e}^{\left(2t\right)}\cdot {e}^{\left(2t\right)}\right) \\  & =2\cdot \left(2{e}^{2\left(2t\right)}-2{e}^{-2\left(2t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{2}))] & =2\cdot \left(2{e}^{2(1)}-2{e}^{-2(1)}\right) \\  & =2\cdot \left(2{e}^{2}-2{e}^{-2}.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### exp_quadratic — easy (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{3}$ given that $∇f(x,y)=3\cdot \left(2x\,i+2y\,j\right)$ and $r(t)={e}^{-\left(3t\right)}\,i+{e}^{\left(3t\right)}\,j.$

- $9\cdot \left(2{e}^{2}-2{e}^{-2}\right)$ **correct**
- $9\cdot \left(2-3{e}^{-1}\right)$
- $9\cdot \left(3e+{e}^{-1}\right)$
- $9\cdot \left(-4{e}^{-1}\right)$
- $9\cdot \left(4{e}^{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(2x\,i+2y\,j.\right)
$$

First, we substitute $x={e}^{-\left(3t\right)}$ and $y={e}^{\left(3t\right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left(2{e}^{-\left(3t\right)}\,i+2{e}^{\left(3t\right)}\,j.\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-\left(3t\right)})\,i+\frac{\text{d}}{\text{d}t}({e}^{\left(3t\right)})\,j \\  & =3\cdot \left((-{e}^{-\left(3t\right)})\,i+{e}^{\left(3t\right)}\,j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((2{e}^{-\left(3t\right)}\,i+2{e}^{\left(3t\right)}\,j)\right)\cdot3\cdot \left( ((-{e}^{-\left(3t\right)})\,i+{e}^{\left(3t\right)}\,j)\right) \\  & =9\cdot \left(2{e}^{-\left(3t\right)}\cdot (-{e}^{-\left(3t\right)})+2{e}^{\left(3t\right)}\cdot {e}^{\left(3t\right)}\right) \\  & =9\cdot \left(2{e}^{2\left(3t\right)}-2{e}^{-2\left(3t\right)}.\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{3},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{1}{3}))] & =9\cdot \left(2{e}^{2(1)}-2{e}^{-2(1)}\right) \\  & =9\cdot \left(2{e}^{2}-2{e}^{-2}.\right)\end{aligned}
$$

## Supported normal solution repair; observed bank remains evidence-only

### sqrt_product — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{8}$ given that $∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j$ and $r(t)=2\sqrt{t}\,i-2\sqrt{t}\,j.$

- $2$
- $0$
- $-4$ **correct**
- $\frac{\sqrt{\pi }}{4}$
- $-\frac{\sqrt{\pi }}{2}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.
$$

First, we substitute $x=2\sqrt{t}$ and $y=-2\sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-(-2\sqrt{t})\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,i-2\sqrt{t}\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,j \\  & =-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{t})\,j \\  & =\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j)\cdot (\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})j) \\  & =(-2\sqrt{t}\operatorname{sin}⁡(4t))\cdot \frac{1}{\sqrt{t}}+2\sqrt{t}\operatorname{sin}⁡(4t)\cdot (-\frac{1}{\sqrt{t}}) \\  & =-2\operatorname{sin}⁡(4t)-2\operatorname{sin}⁡(4t) \\  & =-4\operatorname{sin}⁡(4t).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{8}))] & =-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8}) \\  & =-4\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =-4.\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_product — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi }{8}$ given that $∇f(x,y)=2\cdot \left(-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j\right)$ and $r(t)=2\sqrt{t}\,i-2\sqrt{t}\,j.$

- $2\cdot \left(2\right)$
- $2\cdot \left(-4\right)$ **correct**
- $2\cdot \left(0\right)$
- $2\cdot \left(\frac{\sqrt{\pi }}{4}\right)$
- $2\cdot \left(-\frac{\sqrt{\pi }}{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=2\cdot \left(-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.\right)
$$

First, we substitute $x=2\sqrt{t}$ and $y=-2\sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2\cdot \left(-(-2\sqrt{t})\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,i-2\sqrt{t}\operatorname{sin}⁡[(2\sqrt{t})(-2\sqrt{t})]\,j\right) \\  & =2\cdot \left(-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{t})\,j \\  & =\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =2\cdot \left((-2\sqrt{t}\operatorname{sin}⁡(4t)\,i+2\sqrt{t}\operatorname{sin}⁡(4t)\,j)\right)\cdot (\frac{1}{\sqrt{t}}\,i+(-\frac{1}{\sqrt{t}})i) \\  & =2\cdot \left((-2\sqrt{t}\operatorname{sin}⁡(4t))\cdot \frac{1}{\sqrt{t}}+2\sqrt{t}\operatorname{sin}⁡(4t)\cdot (-\frac{1}{\sqrt{t}})\right) \\  & =2\cdot \left(-2\operatorname{sin}⁡(4t)-2\operatorname{sin}⁡(4t)\right) \\  & =2\cdot \left(-4\operatorname{sin}⁡(4t).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi }{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi }{8}))] & =2\cdot \left(-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8})\right) \\  & =2\cdot \left(-4\operatorname{sin}⁡(\frac{\pi }{2})\right) \\  & =2\cdot \left(-4.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_product — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{16}$ given that $∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j$ and $r(t)=2\sqrt{\left(2t\right)}\,i-2\sqrt{\left(2t\right)}\,j.$

- $2\cdot \left(2\right)$
- $2\cdot \left(-4\right)$ **correct**
- $2\cdot \left(0\right)$
- $2\cdot \left(\frac{\sqrt{\pi }}{4}\right)$
- $2\cdot \left(-\frac{\sqrt{\pi }}{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.
$$

First, we substitute $x=2\sqrt{\left(2t\right)}$ and $y=-2\sqrt{\left(2t\right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-(-2\sqrt{\left(2t\right)})\operatorname{sin}⁡[(2\sqrt{\left(2t\right)})(-2\sqrt{\left(2t\right)})]\,i-2\sqrt{\left(2t\right)}\operatorname{sin}⁡[(2\sqrt{\left(2t\right)})(-2\sqrt{\left(2t\right)})]\,j \\  & =-2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right))\,i+2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right))\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{\left(2t\right)})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{\left(2t\right)})\,j \\  & =2\cdot \left(\frac{1}{\sqrt{\left(2t\right)}}\,i+(-\frac{1}{\sqrt{\left(2t\right)}})j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right))\,i+2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right))\,j)\cdot2\cdot \left( (\frac{1}{\sqrt{\left(2t\right)}}\,i+(-\frac{1}{\sqrt{\left(2t\right)}})i)\right) \\  & =2\cdot \left((-2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right)))\cdot \frac{1}{\sqrt{\left(2t\right)}}+2\sqrt{\left(2t\right)}\operatorname{sin}⁡(4\left(2t\right))\cdot (-\frac{1}{\sqrt{\left(2t\right)}})\right) \\  & =2\cdot \left(-2\operatorname{sin}⁡(4\left(2t\right))-2\operatorname{sin}⁡(4\left(2t\right))\right) \\  & =2\cdot \left(-4\operatorname{sin}⁡(4\left(2t\right)).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{16},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{16}))] & =2\cdot \left(-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8})\right) \\  & =2\cdot \left(-4\operatorname{sin}⁡(\frac{\pi }{2})\right) \\  & =2\cdot \left(-4.\right)\end{aligned}
$$

## Generated observed bank scaling/dilation; unresolved error interpretations

### sqrt_product — moderate (observed_bank_replay_underdetermined)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{24}$ given that $∇f(x,y)=3\cdot \left(-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j\right)$ and $r(t)=2\sqrt{\left(3t\right)}\,i-2\sqrt{\left(3t\right)}\,j.$

- $9\cdot \left(2\right)$
- $9\cdot \left(-4\right)$ **correct**
- $9\cdot \left(0\right)$
- $9\cdot \left(\frac{\sqrt{\pi }}{4}\right)$
- $9\cdot \left(-\frac{\sqrt{\pi }}{2}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=3\cdot \left(-y\operatorname{sin}⁡(xy)\,i-x\operatorname{sin}⁡(xy)\,j.\right)
$$

First, we substitute $x=2\sqrt{\left(3t\right)}$ and $y=-2\sqrt{\left(3t\right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =3\cdot \left(-(-2\sqrt{\left(3t\right)})\operatorname{sin}⁡[(2\sqrt{\left(3t\right)})(-2\sqrt{\left(3t\right)})]\,i-2\sqrt{\left(3t\right)}\operatorname{sin}⁡[(2\sqrt{\left(3t\right)})(-2\sqrt{\left(3t\right)})]\,j\right) \\  & =3\cdot \left(-2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right))\,i+2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right))\,j\right)\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{\left(3t\right)})\,i+\frac{\text{d}}{\text{d}t}(-2\sqrt{\left(3t\right)})\,j \\  & =3\cdot \left(\frac{1}{\sqrt{\left(3t\right)}}\,i+(-\frac{1}{\sqrt{\left(3t\right)}})j.\right)\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =3\cdot \left((-2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right))\,i+2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right))\,j)\right)\cdot3\cdot \left( (\frac{1}{\sqrt{\left(3t\right)}}\,i+(-\frac{1}{\sqrt{\left(3t\right)}})i)\right) \\  & =9\cdot \left((-2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right)))\cdot \frac{1}{\sqrt{\left(3t\right)}}+2\sqrt{\left(3t\right)}\operatorname{sin}⁡(4\left(3t\right))\cdot (-\frac{1}{\sqrt{\left(3t\right)}})\right) \\  & =9\cdot \left(-2\operatorname{sin}⁡(4\left(3t\right))-2\operatorname{sin}⁡(4\left(3t\right))\right) \\  & =9\cdot \left(-4\operatorname{sin}⁡(4\left(3t\right)).\right)\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{24},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(\frac{\pi}{24}))] & =9\cdot \left(-4\operatorname{sin}⁡(4\cdot \frac{\pi }{8})\right) \\  & =9\cdot \left(-4\operatorname{sin}⁡(\frac{\pi }{2})\right) \\  & =9\cdot \left(-4.\right)\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### log_rational — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(\frac{8 x}{4 x^{2} + 4 y}\right)\,i+\left(\frac{4}{4 x^{2} + 4 y}\right)\,j$ and $r(t)=\left(t\right)\,i+\left(3 t^{2}\right)\,j.$

- $- \frac{1}{2}$
- $1$ **correct**
- $\frac{5}{16}$
- $-1$
- $\frac{3}{16}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(\frac{8 x}{4 x^{2} + 4 y}\right)\,i+\left(\frac{4}{4 x^{2} + 4 y}\right)\,j.
$$

First, we substitute $x=t$ and $y=3 t^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(\frac{8 x}{4 x^{2} + 4 y}\right)\,i+\left(\frac{4}{4 x^{2} + 4 y}\right)\,j\Big|_{x=t,\,y=3 t^{2}} \\  & =\left(\frac{1}{2 t}\right)\,i+\left(\frac{1}{4 t^{2}}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t\right)\,i+\frac{\text{d}}{\text{d}t}\left(3 t^{2}\right)\,j \\  & =\left(1\right)\,i+\left(6 t\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(\frac{1}{2 t}\right)\,i+\left(\frac{1}{4 t^{2}}\right)\,j\right)\cdot \left(\left(1\right)\,i+\left(6 t\right)\,j\right) \\  & =\left(\frac{1}{2 t}\right)\cdot \left(1\right)+\left(\frac{1}{4 t^{2}}\right)\cdot \left(6 t\right) \\  & =\left(\frac{1}{2 t}\right)+\left(\frac{3}{2 t}\right) \\  & =\frac{2}{t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =\frac{2}{t}\Big|_{t=2} \\  & =\left(\frac{1}{4}\right)+\left(\frac{3}{4}\right) \\  & =1.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### log_rational — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(\frac{4 x}{2 x^{2} + y}\right)\,i+\left(\frac{1}{2 x^{2} + y}\right)\,j$ and $r(t)=\left(3 t\right)\,i+\left(t^{2}\right)\,j.$

- $\frac{1}{38}$
- $\frac{577}{5776}$
- $1$ **correct**
- $\frac{37}{19}$
- $\frac{99}{76}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(\frac{4 x}{2 x^{2} + y}\right)\,i+\left(\frac{1}{2 x^{2} + y}\right)\,j.
$$

First, we substitute $x=3 t$ and $y=t^{2}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(\frac{4 x}{2 x^{2} + y}\right)\,i+\left(\frac{1}{2 x^{2} + y}\right)\,j\Big|_{x=3 t,\,y=t^{2}} \\  & =\left(\frac{12}{19 t}\right)\,i+\left(\frac{1}{19 t^{2}}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t\right)\,i+\frac{\text{d}}{\text{d}t}\left(t^{2}\right)\,j \\  & =\left(3\right)\,i+\left(2 t\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(\frac{12}{19 t}\right)\,i+\left(\frac{1}{19 t^{2}}\right)\,j\right)\cdot \left(\left(3\right)\,i+\left(2 t\right)\,j\right) \\  & =\left(\frac{12}{19 t}\right)\cdot \left(3\right)+\left(\frac{1}{19 t^{2}}\right)\cdot \left(2 t\right) \\  & =\left(\frac{36}{19 t}\right)+\left(\frac{2}{19 t}\right) \\  & =\frac{2}{t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =\frac{2}{t}\Big|_{t=2} \\  & =\left(\frac{18}{19}\right)+\left(\frac{1}{19}\right) \\  & =1.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sin_y — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=3 \pi$ given that $∇f(x,y)=\left(3 \sin{\left(y \right)}\right)\,i+\left(3 x \cos{\left(y \right)}\right)\,j$ and $r(t)=\left(2 t\right)\,i+\left(\frac{t}{3}\right)\,j.$

- $324 \pi^{2}$
- $- 6 \pi$ **correct**
- $- 36 \pi$
- $- 18 \pi^{2}$
- $0$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(3 \sin{\left(y \right)}\right)\,i+\left(3 x \cos{\left(y \right)}\right)\,j.
$$

First, we substitute $x=2 t$ and $y=\frac{t}{3}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(3 \sin{\left(y \right)}\right)\,i+\left(3 x \cos{\left(y \right)}\right)\,j\Big|_{x=2 t,\,y=\frac{t}{3}} \\  & =\left(3 \sin{\left(\frac{t}{3} \right)}\right)\,i+\left(6 t \cos{\left(\frac{t}{3} \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t\right)\,i+\frac{\text{d}}{\text{d}t}\left(\frac{t}{3}\right)\,j \\  & =\left(2\right)\,i+\left(\frac{1}{3}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(3 \sin{\left(\frac{t}{3} \right)}\right)\,i+\left(6 t \cos{\left(\frac{t}{3} \right)}\right)\,j\right)\cdot \left(\left(2\right)\,i+\left(\frac{1}{3}\right)\,j\right) \\  & =\left(3 \sin{\left(\frac{t}{3} \right)}\right)\cdot \left(2\right)+\left(6 t \cos{\left(\frac{t}{3} \right)}\right)\cdot \left(\frac{1}{3}\right) \\  & =\left(6 \sin{\left(\frac{t}{3} \right)}\right)+\left(2 t \cos{\left(\frac{t}{3} \right)}\right) \\  & =2 \left(t \cos{\left(\frac{t}{3} \right)} + 3 \sin{\left(\frac{t}{3} \right)}\right).\end{aligned}
$$

Finally, evaluating the above at $t=3 \pi,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=3 \pi} & =2 \left(t \cos{\left(\frac{t}{3} \right)} + 3 \sin{\left(\frac{t}{3} \right)}\right)\Big|_{t=3 \pi} \\  & =\left(0\right)+\left(- 6 \pi\right) \\  & =- 6 \pi.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sin_y — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{3 \pi}{2}$ given that $∇f(x,y)=\left(2 \sin{\left(y \right)}\right)\,i+\left(2 x \cos{\left(y \right)}\right)\,j$ and $r(t)=\left(t\right)\,i+\left(\frac{t}{3}\right)\,j.$

- $0$
- $4$
- $2$ **correct**
- $3 \pi$
- $\frac{2}{3}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(2 \sin{\left(y \right)}\right)\,i+\left(2 x \cos{\left(y \right)}\right)\,j.
$$

First, we substitute $x=t$ and $y=\frac{t}{3}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(2 \sin{\left(y \right)}\right)\,i+\left(2 x \cos{\left(y \right)}\right)\,j\Big|_{x=t,\,y=\frac{t}{3}} \\  & =\left(2 \sin{\left(\frac{t}{3} \right)}\right)\,i+\left(2 t \cos{\left(\frac{t}{3} \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t\right)\,i+\frac{\text{d}}{\text{d}t}\left(\frac{t}{3}\right)\,j \\  & =\left(1\right)\,i+\left(\frac{1}{3}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(2 \sin{\left(\frac{t}{3} \right)}\right)\,i+\left(2 t \cos{\left(\frac{t}{3} \right)}\right)\,j\right)\cdot \left(\left(1\right)\,i+\left(\frac{1}{3}\right)\,j\right) \\  & =\left(2 \sin{\left(\frac{t}{3} \right)}\right)\cdot \left(1\right)+\left(2 t \cos{\left(\frac{t}{3} \right)}\right)\cdot \left(\frac{1}{3}\right) \\  & =\left(2 \sin{\left(\frac{t}{3} \right)}\right)+\left(\frac{2 t \cos{\left(\frac{t}{3} \right)}}{3}\right) \\  & =\frac{2 \left(t \cos{\left(\frac{t}{3} \right)} + 3 \sin{\left(\frac{t}{3} \right)}\right)}{3}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{3 \pi}{2},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{3 \pi}{2}} & =\frac{2 \left(t \cos{\left(\frac{t}{3} \right)} + 3 \sin{\left(\frac{t}{3} \right)}\right)}{3}\Big|_{t=\frac{3 \pi}{2}} \\  & =\left(2\right)+\left(0\right) \\  & =2.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sqrt_sine — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{4}$ given that $∇f(x,y)=\left(8 x y \cos{\left(x^{2} \right)}\right)\,i+\left(4 \sin{\left(x^{2} \right)}\right)\,j$ and $r(t)=\left(2 \sqrt{t}\right)\,i+\left(3 t\right)\,j.$

- $24$
- $36 \pi^{3}$
- $- 6 \pi^{2}$
- $- 18 \pi^{\frac{3}{2}}$
- $- 12 \pi$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(8 x y \cos{\left(x^{2} \right)}\right)\,i+\left(4 \sin{\left(x^{2} \right)}\right)\,j.
$$

First, we substitute $x=2 \sqrt{t}$ and $y=3 t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(8 x y \cos{\left(x^{2} \right)}\right)\,i+\left(4 \sin{\left(x^{2} \right)}\right)\,j\Big|_{x=2 \sqrt{t},\,y=3 t} \\  & =\left(48 t^{\frac{3}{2}} \cos{\left(4 t \right)}\right)\,i+\left(4 \sin{\left(4 t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 \sqrt{t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(3 t\right)\,j \\  & =\left(\frac{1}{\sqrt{t}}\right)\,i+\left(3\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(48 t^{\frac{3}{2}} \cos{\left(4 t \right)}\right)\,i+\left(4 \sin{\left(4 t \right)}\right)\,j\right)\cdot \left(\left(\frac{1}{\sqrt{t}}\right)\,i+\left(3\right)\,j\right) \\  & =\left(48 t^{\frac{3}{2}} \cos{\left(4 t \right)}\right)\cdot \left(\frac{1}{\sqrt{t}}\right)+\left(4 \sin{\left(4 t \right)}\right)\cdot \left(3\right) \\  & =\left(48 t \cos{\left(4 t \right)}\right)+\left(12 \sin{\left(4 t \right)}\right) \\  & =12 \left(4 t \cos{\left(4 t \right)} + \sin{\left(4 t \right)}\right).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{4},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{4}} & =12 \left(4 t \cos{\left(4 t \right)} + \sin{\left(4 t \right)}\right)\Big|_{t=\frac{\pi}{4}} \\  & =\left(- 12 \pi\right)+\left(0\right) \\  & =- 12 \pi.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sqrt_sine — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2 \pi$ given that $∇f(x,y)=\left(4 x y \cos{\left(x^{2} \right)}\right)\,i+\left(2 \sin{\left(x^{2} \right)}\right)\,j$ and $r(t)=\left(\sqrt{t}\right)\,i+\left(3 t\right)\,j.$

- $-3$
- $1152 \pi^{3}$
- $12 \pi$ **correct**
- $48 \pi^{2}$
- $72 \sqrt{2} \pi^{\frac{3}{2}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(4 x y \cos{\left(x^{2} \right)}\right)\,i+\left(2 \sin{\left(x^{2} \right)}\right)\,j.
$$

First, we substitute $x=\sqrt{t}$ and $y=3 t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(4 x y \cos{\left(x^{2} \right)}\right)\,i+\left(2 \sin{\left(x^{2} \right)}\right)\,j\Big|_{x=\sqrt{t},\,y=3 t} \\  & =\left(12 t^{\frac{3}{2}} \cos{\left(t \right)}\right)\,i+\left(2 \sin{\left(t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\sqrt{t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(3 t\right)\,j \\  & =\left(\frac{1}{2 \sqrt{t}}\right)\,i+\left(3\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(12 t^{\frac{3}{2}} \cos{\left(t \right)}\right)\,i+\left(2 \sin{\left(t \right)}\right)\,j\right)\cdot \left(\left(\frac{1}{2 \sqrt{t}}\right)\,i+\left(3\right)\,j\right) \\  & =\left(12 t^{\frac{3}{2}} \cos{\left(t \right)}\right)\cdot \left(\frac{1}{2 \sqrt{t}}\right)+\left(2 \sin{\left(t \right)}\right)\cdot \left(3\right) \\  & =\left(6 t \cos{\left(t \right)}\right)+\left(6 \sin{\left(t \right)}\right) \\  & =6 \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right).\end{aligned}
$$

Finally, evaluating the above at $t=2 \pi,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2 \pi} & =6 \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right)\Big|_{t=2 \pi} \\  & =\left(12 \pi\right)+\left(0\right) \\  & =12 \pi.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### exp_cancel — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(8 x e^{x^{2} + y}\right)\,i+\left(4 e^{x^{2} + y}\right)\,j$ and $r(t)=\left(\sin{\left(4 t \right)}\right)\,i+\left(t + \cos^{2}{\left(4 t \right)}\right)\,j.$

- $4 \left(8 \sin{\left(16 \right)} - 1\right) e^{3}$
- $4 e^{3}$ **correct**
- $4 \left(1 + 2 \sin{\left(8 \right)}\right) e^{3}$
- $- 4 e^{3}$
- $64 \left(-2 + \sin{\left(16 \right)} + 2 \cos{\left(32 \right)}\right) e^{6}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(8 x e^{x^{2} + y}\right)\,i+\left(4 e^{x^{2} + y}\right)\,j.
$$

First, we substitute $x=\sin{\left(4 t \right)}$ and $y=t + \cos^{2}{\left(4 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(8 x e^{x^{2} + y}\right)\,i+\left(4 e^{x^{2} + y}\right)\,j\Big|_{x=\sin{\left(4 t \right)},\,y=t + \cos^{2}{\left(4 t \right)}} \\  & =\left(8 e e^{t} \sin{\left(4 t \right)}\right)\,i+\left(4 e e^{t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\sin{\left(4 t \right)}\right)\,i+\frac{\text{d}}{\text{d}t}\left(t + \cos^{2}{\left(4 t \right)}\right)\,j \\  & =\left(4 \cos{\left(4 t \right)}\right)\,i+\left(- 8 \sin{\left(4 t \right)} \cos{\left(4 t \right)} + 1\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(8 e e^{t} \sin{\left(4 t \right)}\right)\,i+\left(4 e e^{t}\right)\,j\right)\cdot \left(\left(4 \cos{\left(4 t \right)}\right)\,i+\left(- 8 \sin{\left(4 t \right)} \cos{\left(4 t \right)} + 1\right)\,j\right) \\  & =\left(8 e e^{t} \sin{\left(4 t \right)}\right)\cdot \left(4 \cos{\left(4 t \right)}\right)+\left(4 e e^{t}\right)\cdot \left(- 8 \sin{\left(4 t \right)} \cos{\left(4 t \right)} + 1\right) \\  & =\left(32 e e^{t} \sin{\left(4 t \right)} \cos{\left(4 t \right)}\right)+\left(- 32 e e^{t} \sin{\left(4 t \right)} \cos{\left(4 t \right)} + 4 e e^{t}\right) \\  & =4 e e^{t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =4 e e^{t}\Big|_{t=2} \\  & =\left(16 e^{3} \sin{\left(16 \right)}\right)+\left(- 4 \left(4 \sin{\left(16 \right)} - 1\right) e^{3}\right) \\  & =4 e^{3}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### exp_cancel — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(4 x e^{x^{2} + y}\right)\,i+\left(2 e^{x^{2} + y}\right)\,j$ and $r(t)=\left(\sin{\left(t \right)}\right)\,i+\left(3 t + \cos^{2}{\left(t \right)}\right)\,j.$

- $- 4 e^{7} \cos^{2}{\left(2 \right)}$
- $- 4 \left(-3 + 2 \cos{\left(4 \right)}\right) e^{14}$
- $6 e^{7}$ **correct**
- $2 \left(\sin^{2}{\left(2 \right)} + 7\right) e^{7}$
- $2 \left(\cos{\left(6 \right)} + 6 \sin{\left(2 \right)}\right) e^{7}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(4 x e^{x^{2} + y}\right)\,i+\left(2 e^{x^{2} + y}\right)\,j.
$$

First, we substitute $x=\sin{\left(t \right)}$ and $y=3 t + \cos^{2}{\left(t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(4 x e^{x^{2} + y}\right)\,i+\left(2 e^{x^{2} + y}\right)\,j\Big|_{x=\sin{\left(t \right)},\,y=3 t + \cos^{2}{\left(t \right)}} \\  & =\left(4 e e^{3 t} \sin{\left(t \right)}\right)\,i+\left(2 e e^{3 t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\sin{\left(t \right)}\right)\,i+\frac{\text{d}}{\text{d}t}\left(3 t + \cos^{2}{\left(t \right)}\right)\,j \\  & =\left(\cos{\left(t \right)}\right)\,i+\left(- 2 \sin{\left(t \right)} \cos{\left(t \right)} + 3\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(4 e e^{3 t} \sin{\left(t \right)}\right)\,i+\left(2 e e^{3 t}\right)\,j\right)\cdot \left(\left(\cos{\left(t \right)}\right)\,i+\left(- 2 \sin{\left(t \right)} \cos{\left(t \right)} + 3\right)\,j\right) \\  & =\left(4 e e^{3 t} \sin{\left(t \right)}\right)\cdot \left(\cos{\left(t \right)}\right)+\left(2 e e^{3 t}\right)\cdot \left(- 2 \sin{\left(t \right)} \cos{\left(t \right)} + 3\right) \\  & =\left(4 e e^{3 t} \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(- 4 e e^{3 t} \sin{\left(t \right)} \cos{\left(t \right)} + 6 e e^{3 t}\right) \\  & =6 e e^{3 t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =6 e e^{3 t}\Big|_{t=2} \\  & =\left(2 e^{7} \sin{\left(4 \right)}\right)+\left(- 2 \left(-3 + \sin{\left(4 \right)}\right) e^{7}\right) \\  & =6 e^{7}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### atan_log — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{4}$ given that $∇f(x,y)=\left(\frac{4}{x}\right)\,i+\left(\frac{4}{y}\right)\,j$ and $r(t)=\left(t^{2} + 3\right)\,i+\left(\operatorname{atan}{\left(4 t \right)}\right)\,j.$

- $\frac{32 \left(-49 + \pi\right)}{49 \pi}$
- $\frac{32 \left(\pi + 49\right)}{49 \pi}$ **correct**
- $\frac{16 \left(4 \pi + 49\right)}{49 \pi}$
- $- \frac{32 \left(\pi + 49\right)}{49 \pi}$
- $\frac{1024}{49 \pi}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(\frac{4}{x}\right)\,i+\left(\frac{4}{y}\right)\,j.
$$

First, we substitute $x=t^{2} + 3$ and $y=\operatorname{atan}{\left(4 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(\frac{4}{x}\right)\,i+\left(\frac{4}{y}\right)\,j\Big|_{x=t^{2} + 3,\,y=\operatorname{atan}{\left(4 t \right)}} \\  & =\left(\frac{4}{t^{2} + 3}\right)\,i+\left(\frac{4}{\operatorname{atan}{\left(4 t \right)}}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2} + 3\right)\,i+\frac{\text{d}}{\text{d}t}\left(\operatorname{atan}{\left(4 t \right)}\right)\,j \\  & =\left(2 t\right)\,i+\left(\frac{4}{16 t^{2} + 1}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(\frac{4}{t^{2} + 3}\right)\,i+\left(\frac{4}{\operatorname{atan}{\left(4 t \right)}}\right)\,j\right)\cdot \left(\left(2 t\right)\,i+\left(\frac{4}{16 t^{2} + 1}\right)\,j\right) \\  & =\left(\frac{4}{t^{2} + 3}\right)\cdot \left(2 t\right)+\left(\frac{4}{\operatorname{atan}{\left(4 t \right)}}\right)\cdot \left(\frac{4}{16 t^{2} + 1}\right) \\  & =\left(\frac{8 t}{t^{2} + 3}\right)+\left(\frac{16}{16 t^{2} \operatorname{atan}{\left(4 t \right)} + \operatorname{atan}{\left(4 t \right)}}\right) \\  & =\frac{8 \left(16 t^{3} \operatorname{atan}{\left(4 t \right)} + 2 t^{2} + t \operatorname{atan}{\left(4 t \right)} + 6\right)}{\left(t^{2} + 3\right) \left(16 t^{2} + 1\right) \operatorname{atan}{\left(4 t \right)}}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{4},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{1}{4}} & =\frac{8 \left(16 t^{3} \operatorname{atan}{\left(4 t \right)} + 2 t^{2} + t \operatorname{atan}{\left(4 t \right)} + 6\right)}{\left(t^{2} + 3\right) \left(16 t^{2} + 1\right) \operatorname{atan}{\left(4 t \right)}}\Big|_{t=\frac{1}{4}} \\  & =\left(\frac{32}{49}\right)+\left(\frac{32}{\pi}\right) \\  & =\frac{32 \left(\pi + 49\right)}{49 \pi}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### atan_log — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{1}{4}$ given that $∇f(x,y)=\left(\frac{2}{x}\right)\,i+\left(\frac{1}{y}\right)\,j$ and $r(t)=\left(3 t^{2} + 1\right)\,i+\left(\operatorname{atan}{\left(4 t \right)}\right)\,j.$

- $\frac{32 \left(-19 + 6 \pi\right)}{19 \pi}$
- $\frac{16 \left(361 + 64 \pi^{2}\right)}{361 \pi^{2}}$
- $\frac{8 \left(6 \pi + 19\right)}{19 \pi}$ **correct**
- $3$
- $\frac{2 \left(57 + 32 \pi\right)}{19 \pi}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(\frac{2}{x}\right)\,i+\left(\frac{1}{y}\right)\,j.
$$

First, we substitute $x=3 t^{2} + 1$ and $y=\operatorname{atan}{\left(4 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(\frac{2}{x}\right)\,i+\left(\frac{1}{y}\right)\,j\Big|_{x=3 t^{2} + 1,\,y=\operatorname{atan}{\left(4 t \right)}} \\  & =\left(\frac{2}{3 t^{2} + 1}\right)\,i+\left(\frac{1}{\operatorname{atan}{\left(4 t \right)}}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t^{2} + 1\right)\,i+\frac{\text{d}}{\text{d}t}\left(\operatorname{atan}{\left(4 t \right)}\right)\,j \\  & =\left(6 t\right)\,i+\left(\frac{4}{16 t^{2} + 1}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(\frac{2}{3 t^{2} + 1}\right)\,i+\left(\frac{1}{\operatorname{atan}{\left(4 t \right)}}\right)\,j\right)\cdot \left(\left(6 t\right)\,i+\left(\frac{4}{16 t^{2} + 1}\right)\,j\right) \\  & =\left(\frac{2}{3 t^{2} + 1}\right)\cdot \left(6 t\right)+\left(\frac{1}{\operatorname{atan}{\left(4 t \right)}}\right)\cdot \left(\frac{4}{16 t^{2} + 1}\right) \\  & =\left(\frac{12 t}{3 t^{2} + 1}\right)+\left(\frac{4}{16 t^{2} \operatorname{atan}{\left(4 t \right)} + \operatorname{atan}{\left(4 t \right)}}\right) \\  & =\frac{4 \left(48 t^{3} \operatorname{atan}{\left(4 t \right)} + 3 t^{2} + 3 t \operatorname{atan}{\left(4 t \right)} + 1\right)}{\left(3 t^{2} + 1\right) \left(16 t^{2} + 1\right) \operatorname{atan}{\left(4 t \right)}}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{1}{4},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{1}{4}} & =\frac{4 \left(48 t^{3} \operatorname{atan}{\left(4 t \right)} + 3 t^{2} + 3 t \operatorname{atan}{\left(4 t \right)} + 1\right)}{\left(3 t^{2} + 1\right) \left(16 t^{2} + 1\right) \operatorname{atan}{\left(4 t \right)}}\Big|_{t=\frac{1}{4}} \\  & =\left(\frac{48}{19}\right)+\left(\frac{8}{\pi}\right) \\  & =\frac{8 \left(6 \pi + 19\right)}{19 \pi}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### exp_quadratic — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(8 x\right)\,i+\left(8 y\right)\,j$ and $r(t)=\left(e^{- t}\right)\,i+\left(e^{3 t}\right)\,j.$

- $- \frac{8 \left(1 + 3 e^{16}\right)}{e^{4}}$
- $\frac{8 \left(-1 + 3 e^{16}\right)}{e^{4}}$ **correct**
- $\frac{8 \left(1 + e^{8}\right)}{e^{2}}$
- $- \frac{8 \left(-1 + 3 e^{16}\right)}{e^{4}}$
- $- 192 e^{8}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(8 x\right)\,i+\left(8 y\right)\,j.
$$

First, we substitute $x=e^{- t}$ and $y=e^{3 t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(8 x\right)\,i+\left(8 y\right)\,j\Big|_{x=e^{- t},\,y=e^{3 t}} \\  & =\left(8 e^{- t}\right)\,i+\left(8 e^{3 t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{- t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(e^{3 t}\right)\,j \\  & =\left(- e^{- t}\right)\,i+\left(3 e^{3 t}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(8 e^{- t}\right)\,i+\left(8 e^{3 t}\right)\,j\right)\cdot \left(\left(- e^{- t}\right)\,i+\left(3 e^{3 t}\right)\,j\right) \\  & =\left(8 e^{- t}\right)\cdot \left(- e^{- t}\right)+\left(8 e^{3 t}\right)\cdot \left(3 e^{3 t}\right) \\  & =\left(- 8 e^{- 2 t}\right)+\left(24 e^{6 t}\right) \\  & =8 \left(3 e^{8 t} - 1\right) e^{- 2 t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =8 \left(3 e^{8 t} - 1\right) e^{- 2 t}\Big|_{t=2} \\  & =\left(- \frac{8}{e^{4}}\right)+\left(24 e^{12}\right) \\  & =\frac{8 \left(-1 + 3 e^{16}\right)}{e^{4}}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### exp_quadratic — easy (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=2$ given that $∇f(x,y)=\left(4 x\right)\,i+\left(2 y\right)\,j$ and $r(t)=\left(e^{- 3 t}\right)\,i+\left(e^{t}\right)\,j.$

- $\frac{2 \left(18 + e^{16}\right)}{e^{12}}$
- $\frac{4 \left(2 + 2 e^{4} + e^{8}\right) \left(- 2 e^{4} + 2 + e^{8}\right)}{e^{12}}$
- $\frac{2 \left(-6 + e^{16}\right)}{e^{12}}$ **correct**
- $\frac{2 \left(2 + e^{16}\right)}{e^{12}}$
- $- \frac{2}{e^{4}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(4 x\right)\,i+\left(2 y\right)\,j.
$$

First, we substitute $x=e^{- 3 t}$ and $y=e^{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(4 x\right)\,i+\left(2 y\right)\,j\Big|_{x=e^{- 3 t},\,y=e^{t}} \\  & =\left(4 e^{- 3 t}\right)\,i+\left(2 e^{t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{- 3 t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(e^{t}\right)\,j \\  & =\left(- 3 e^{- 3 t}\right)\,i+\left(e^{t}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(4 e^{- 3 t}\right)\,i+\left(2 e^{t}\right)\,j\right)\cdot \left(\left(- 3 e^{- 3 t}\right)\,i+\left(e^{t}\right)\,j\right) \\  & =\left(4 e^{- 3 t}\right)\cdot \left(- 3 e^{- 3 t}\right)+\left(2 e^{t}\right)\cdot \left(e^{t}\right) \\  & =\left(- 12 e^{- 6 t}\right)+\left(2 e^{2 t}\right) \\  & =2 \left(e^{8 t} - 6\right) e^{- 6 t}.\end{aligned}
$$

Finally, evaluating the above at $t=2,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=2} & =2 \left(e^{8 t} - 6\right) e^{- 6 t}\Big|_{t=2} \\  & =\left(- \frac{12}{e^{12}}\right)+\left(2 e^{4}\right) \\  & =\frac{2 \left(-6 + e^{16}\right)}{e^{12}}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### log_sine — moderate (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{6}$ given that $∇f(x,y)=\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j$ and $r(t)=\left(e^{4 t}\right)\,i+\left(\sin{\left(3 t \right)}\right)\,j.$

- $\frac{2 \left(3 + 2 \pi\right)}{3}$
- $\frac{2 \left(3 + 2 \pi + 2 \pi e^{\frac{2 \pi}{3}}\right)}{3}$
- $4 e^{\frac{2 \pi}{3}}$
- $\frac{8 \left(3 + 2 \pi\right) e^{\frac{2 \pi}{3}}}{3}$ **correct**
- $\frac{4 \left(6 + 5 \pi\right) e^{\frac{2 \pi}{3}}}{3}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j.
$$

First, we substitute $x=e^{4 t}$ and $y=\sin{\left(3 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j\Big|_{x=e^{4 t},\,y=\sin{\left(3 t \right)}} \\  & =\left(2 \left(4 t + 1\right) \sin{\left(3 t \right)}\right)\,i+\left(8 t e^{4 t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{4 t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(\sin{\left(3 t \right)}\right)\,j \\  & =\left(4 e^{4 t}\right)\,i+\left(3 \cos{\left(3 t \right)}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(2 \left(4 t + 1\right) \sin{\left(3 t \right)}\right)\,i+\left(8 t e^{4 t}\right)\,j\right)\cdot \left(\left(4 e^{4 t}\right)\,i+\left(3 \cos{\left(3 t \right)}\right)\,j\right) \\  & =\left(2 \left(4 t + 1\right) \sin{\left(3 t \right)}\right)\cdot \left(4 e^{4 t}\right)+\left(8 t e^{4 t}\right)\cdot \left(3 \cos{\left(3 t \right)}\right) \\  & =\left(32 t e^{4 t} \sin{\left(3 t \right)} + 8 e^{4 t} \sin{\left(3 t \right)}\right)+\left(24 t e^{4 t} \cos{\left(3 t \right)}\right) \\  & =8 \left(4 t \sin{\left(3 t \right)} + 3 t \cos{\left(3 t \right)} + \sin{\left(3 t \right)}\right) e^{4 t}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{6},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{6}} & =8 \left(4 t \sin{\left(3 t \right)} + 3 t \cos{\left(3 t \right)} + \sin{\left(3 t \right)}\right) e^{4 t}\Big|_{t=\frac{\pi}{6}} \\  & =\left(\frac{8 \left(3 + 2 \pi\right) e^{\frac{2 \pi}{3}}}{3}\right)+\left(0\right) \\  & =\frac{8 \left(3 + 2 \pi\right) e^{\frac{2 \pi}{3}}}{3}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### log_sine — moderate (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{6}$ given that $∇f(x,y)=\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j$ and $r(t)=\left(e^{3 t}\right)\,i+\left(\sin{\left(3 t \right)}\right)\,j.$

- $18 e^{\frac{\pi}{2}}$
- $3 \pi e^{\pi}$
- $4 + \pi^{2} + 4 \pi + \pi^{2} e^{\pi}$
- $3 \left(2 + \pi\right) e^{\frac{\pi}{2}}$ **correct**
- $2 \left(1 + \pi\right) e^{\frac{\pi}{2}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j.
$$

First, we substitute $x=e^{3 t}$ and $y=\sin{\left(3 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(2 y \left(\ln{\left(x \right)} + 1\right)\right)\,i+\left(2 x \ln{\left(x \right)}\right)\,j\Big|_{x=e^{3 t},\,y=\sin{\left(3 t \right)}} \\  & =\left(2 \left(3 t + 1\right) \sin{\left(3 t \right)}\right)\,i+\left(6 t e^{3 t}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{3 t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(\sin{\left(3 t \right)}\right)\,j \\  & =\left(3 e^{3 t}\right)\,i+\left(3 \cos{\left(3 t \right)}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(2 \left(3 t + 1\right) \sin{\left(3 t \right)}\right)\,i+\left(6 t e^{3 t}\right)\,j\right)\cdot \left(\left(3 e^{3 t}\right)\,i+\left(3 \cos{\left(3 t \right)}\right)\,j\right) \\  & =\left(2 \left(3 t + 1\right) \sin{\left(3 t \right)}\right)\cdot \left(3 e^{3 t}\right)+\left(6 t e^{3 t}\right)\cdot \left(3 \cos{\left(3 t \right)}\right) \\  & =\left(18 t e^{3 t} \sin{\left(3 t \right)} + 6 e^{3 t} \sin{\left(3 t \right)}\right)+\left(18 t e^{3 t} \cos{\left(3 t \right)}\right) \\  & =6 \left(3 \sqrt{2} t \sin{\left(3 t + \frac{\pi}{4} \right)} + \sin{\left(3 t \right)}\right) e^{3 t}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{6},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{6}} & =6 \left(3 \sqrt{2} t \sin{\left(3 t + \frac{\pi}{4} \right)} + \sin{\left(3 t \right)}\right) e^{3 t}\Big|_{t=\frac{\pi}{6}} \\  & =\left(3 \left(2 + \pi\right) e^{\frac{\pi}{2}}\right)+\left(0\right) \\  & =3 \left(2 + \pi\right) e^{\frac{\pi}{2}}.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sqrt_product — moderate (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{8}$ given that $∇f(x,y)=\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j$ and $r(t)=\left(4 \sqrt{t}\right)\,i+\left(- 3 \sqrt{t}\right)\,j.$

- $\frac{3 \left(\sqrt{2} \sqrt{\pi} + 8\right)}{2}$
- $- \frac{\sqrt{2} \sqrt{\pi}}{2}$
- $\frac{\sqrt{2}}{\sqrt{\pi}}$
- $24$ **correct**
- $- 2 \left(-6 + \sqrt{2} \sqrt{\pi}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j.
$$

First, we substitute $x=4 \sqrt{t}$ and $y=- 3 \sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j\Big|_{x=4 \sqrt{t},\,y=- 3 \sqrt{t}} \\  & =\left(- 6 \sqrt{t} \sin{\left(12 t \right)}\right)\,i+\left(8 \sqrt{t} \sin{\left(12 t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 \sqrt{t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(- 3 \sqrt{t}\right)\,j \\  & =\left(\frac{2}{\sqrt{t}}\right)\,i+\left(- \frac{3}{2 \sqrt{t}}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(- 6 \sqrt{t} \sin{\left(12 t \right)}\right)\,i+\left(8 \sqrt{t} \sin{\left(12 t \right)}\right)\,j\right)\cdot \left(\left(\frac{2}{\sqrt{t}}\right)\,i+\left(- \frac{3}{2 \sqrt{t}}\right)\,j\right) \\  & =\left(- 6 \sqrt{t} \sin{\left(12 t \right)}\right)\cdot \left(\frac{2}{\sqrt{t}}\right)+\left(8 \sqrt{t} \sin{\left(12 t \right)}\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right) \\  & =\left(- 12 \sin{\left(12 t \right)}\right)+\left(- 12 \sin{\left(12 t \right)}\right) \\  & =- 24 \sin{\left(12 t \right)}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{8}} & =- 24 \sin{\left(12 t \right)}\Big|_{t=\frac{\pi}{8}} \\  & =\left(12\right)+\left(12\right) \\  & =24.\end{aligned}
$$

## Generated parameter and complete operation-bank extension

### sqrt_product — moderate (authored_parameter_and_bank_extension)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{6}$ given that $∇f(x,y)=\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j$ and $r(t)=\left(3 \sqrt{t}\right)\,i+\left(- 3 \sqrt{t}\right)\,j.$

- $- \frac{54}{\pi}$
- $-18$
- $12 \pi$
- $18$ **correct**
- $6 \pi$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j.
$$

First, we substitute $x=3 \sqrt{t}$ and $y=- 3 \sqrt{t}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(- 2 y \sin{\left(x y \right)}\right)\,i+\left(- 2 x \sin{\left(x y \right)}\right)\,j\Big|_{x=3 \sqrt{t},\,y=- 3 \sqrt{t}} \\  & =\left(- 6 \sqrt{t} \sin{\left(9 t \right)}\right)\,i+\left(6 \sqrt{t} \sin{\left(9 t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 \sqrt{t}\right)\,i+\frac{\text{d}}{\text{d}t}\left(- 3 \sqrt{t}\right)\,j \\  & =\left(\frac{3}{2 \sqrt{t}}\right)\,i+\left(- \frac{3}{2 \sqrt{t}}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(- 6 \sqrt{t} \sin{\left(9 t \right)}\right)\,i+\left(6 \sqrt{t} \sin{\left(9 t \right)}\right)\,j\right)\cdot \left(\left(\frac{3}{2 \sqrt{t}}\right)\,i+\left(- \frac{3}{2 \sqrt{t}}\right)\,j\right) \\  & =\left(- 6 \sqrt{t} \sin{\left(9 t \right)}\right)\cdot \left(\frac{3}{2 \sqrt{t}}\right)+\left(6 \sqrt{t} \sin{\left(9 t \right)}\right)\cdot \left(- \frac{3}{2 \sqrt{t}}\right) \\  & =\left(- 9 \sin{\left(9 t \right)}\right)+\left(- 9 \sin{\left(9 t \right)}\right) \\  & =- 18 \sin{\left(9 t \right)}.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{6},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{6}} & =- 18 \sin{\left(9 t \right)}\Big|_{t=\frac{\pi}{6}} \\  & =\left(9\right)+\left(9\right) \\  & =18.\end{aligned}
$$

## Generated authored default; missing hard scope is an authored claim

### coupled_trig — hard (authored_missing_level)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{\pi}{8}$ given that $∇f(x,y)=\left(3 x + 3 y\right)\,i+\left(3 x + 2 y\right)\,j$ and $r(t)=\left(\sin{\left(2 t \right)}\right)\,i+\left(\cos{\left(2 t \right)}\right)\,j.$

- $11$
- $-5$
- $6$
- $1$ **correct**
- $-11$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(3 x + 3 y\right)\,i+\left(3 x + 2 y\right)\,j.
$$

First, we substitute $x=\sin{\left(2 t \right)}$ and $y=\cos{\left(2 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(3 x + 3 y\right)\,i+\left(3 x + 2 y\right)\,j\Big|_{x=\sin{\left(2 t \right)},\,y=\cos{\left(2 t \right)}} \\  & =\left(3 \sqrt{2} \sin{\left(2 t + \frac{\pi}{4} \right)}\right)\,i+\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\sin{\left(2 t \right)}\right)\,i+\frac{\text{d}}{\text{d}t}\left(\cos{\left(2 t \right)}\right)\,j \\  & =\left(2 \cos{\left(2 t \right)}\right)\,i+\left(- 2 \sin{\left(2 t \right)}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(3 \sqrt{2} \sin{\left(2 t + \frac{\pi}{4} \right)}\right)\,i+\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\,j\right)\cdot \left(\left(2 \cos{\left(2 t \right)}\right)\,i+\left(- 2 \sin{\left(2 t \right)}\right)\,j\right) \\  & =\left(3 \sqrt{2} \sin{\left(2 t + \frac{\pi}{4} \right)}\right)\cdot \left(2 \cos{\left(2 t \right)}\right)+\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\cdot \left(- 2 \sin{\left(2 t \right)}\right) \\  & =\left(6 \sqrt{2} \sin{\left(2 t + \frac{\pi}{4} \right)} \cos{\left(2 t \right)}\right)+\left(- 6 \sin^{2}{\left(2 t \right)} - 4 \sin{\left(2 t \right)} \cos{\left(2 t \right)}\right) \\  & =\sin{\left(4 t \right)} + 12 \cos^{2}{\left(2 t \right)} - 6.\end{aligned}
$$

Finally, evaluating the above at $t=\frac{\pi}{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{\pi}{8}} & =\sin{\left(4 t \right)} + 12 \cos^{2}{\left(2 t \right)} - 6\Big|_{t=\frac{\pi}{8}} \\  & =\left(6\right)+\left(-5\right) \\  & =1.\end{aligned}
$$

## Generated authored default; missing hard scope is an authored claim

### coupled_trig — hard (authored_missing_level)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=\frac{3 \pi}{8}$ given that $∇f(x,y)=\left(3 x + 2 y\right)\,i+\left(2 x + 3 y\right)\,j$ and $r(t)=\left(\sin{\left(2 t \right)}\right)\,i+\left(\cos{\left(2 t \right)}\right)\,j.$

- $1$
- $-2$
- $2$
- $0$ **correct**
- $-1$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(3 x + 2 y\right)\,i+\left(2 x + 3 y\right)\,j.
$$

First, we substitute $x=\sin{\left(2 t \right)}$ and $y=\cos{\left(2 t \right)}$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(3 x + 2 y\right)\,i+\left(2 x + 3 y\right)\,j\Big|_{x=\sin{\left(2 t \right)},\,y=\cos{\left(2 t \right)}} \\  & =\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\,i+\left(2 \sin{\left(2 t \right)} + 3 \cos{\left(2 t \right)}\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\sin{\left(2 t \right)}\right)\,i+\frac{\text{d}}{\text{d}t}\left(\cos{\left(2 t \right)}\right)\,j \\  & =\left(2 \cos{\left(2 t \right)}\right)\,i+\left(- 2 \sin{\left(2 t \right)}\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\,i+\left(2 \sin{\left(2 t \right)} + 3 \cos{\left(2 t \right)}\right)\,j\right)\cdot \left(\left(2 \cos{\left(2 t \right)}\right)\,i+\left(- 2 \sin{\left(2 t \right)}\right)\,j\right) \\  & =\left(3 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)\cdot \left(2 \cos{\left(2 t \right)}\right)+\left(2 \sin{\left(2 t \right)} + 3 \cos{\left(2 t \right)}\right)\cdot \left(- 2 \sin{\left(2 t \right)}\right) \\  & =\left(6 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}\right)+\left(- 4 \sin^{2}{\left(2 t \right)} - 6 \sin{\left(2 t \right)} \cos{\left(2 t \right)}\right) \\  & =4 \left(- \sin{\left(2 t \right)} + \cos{\left(2 t \right)}\right) \left(\sin{\left(2 t \right)} + \cos{\left(2 t \right)}\right).\end{aligned}
$$

Finally, evaluating the above at $t=\frac{3 \pi}{8},$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=\frac{3 \pi}{8}} & =4 \left(- \sin{\left(2 t \right)} + \cos{\left(2 t \right)}\right) \left(\sin{\left(2 t \right)} + \cos{\left(2 t \right)}\right)\Big|_{t=\frac{3 \pi}{8}} \\  & =\left(-1\right)+\left(1\right) \\  & =0.\end{aligned}
$$

## Generated authored default; missing hard scope is an authored claim

### product_exp — hard (authored_missing_level)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j$ and $r(t)=\left(3 t^{2}\right)\,i+\left(2 t\right)\,j.$

- $108 \left(2 + 3 e^{6}\right) \left(3 + 2 e^{6}\right)$
- $6 \left(11 + 9 e^{6}\right)$ **correct**
- $- 6 \left(11 + 9 e^{6}\right)$
- $6 \left(7 + 3 e^{6}\right)$
- $15 \left(1 + e^{2}\right) \left(- e^{2} + 1 + e^{4}\right)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j.
$$

First, we substitute $x=3 t^{2}$ and $y=2 t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j\Big|_{x=3 t^{2},\,y=2 t} \\  & =\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\,i+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t^{2}\right)\,i+\frac{\text{d}}{\text{d}t}\left(2 t\right)\,j \\  & =\left(6 t\right)\,i+\left(2\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\,i+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\,j\right)\cdot \left(\left(6 t\right)\,i+\left(2\right)\,j\right) \\  & =\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\cdot \left(6 t\right)+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\cdot \left(2\right) \\  & =\left(54 t^{3} + 36 t^{2} e^{6 t^{3}}\right)+\left(18 t^{2} e^{6 t^{3}} + 12 t\right) \\  & =6 t \left(9 t^{2} + 9 t e^{6 t^{3}} + 2\right).\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=1} & =6 t \left(9 t^{2} + 9 t e^{6 t^{3}} + 2\right)\Big|_{t=1} \\  & =\left(18 \left(3 + 2 e^{6}\right)\right)+\left(6 \left(2 + 3 e^{6}\right)\right) \\  & =6 \left(11 + 9 e^{6}\right).\end{aligned}
$$

## Generated authored default; missing hard scope is an authored claim

### product_exp — hard (authored_missing_level)

Evaluate $\frac{\text{d}}{\text{d}t}[f(r(t))]$ at $t=1$ given that $∇f(x,y)=\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j$ and $r(t)=\left(3 t^{2}\right)\,i+\left(2 t\right)\,j.$

- $15 \left(4 + 3 e^{6}\right)$
- $3 \left(7 + 8 e^{6}\right)$
- $8$
- $15 \left(1 + e^{2}\right) \left(- e^{2} + 1 + e^{4}\right)$
- $6 \left(11 + 9 e^{6}\right)$ **correct**

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

In addition, we've been given that

$$
∇f(x,y)=\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j.
$$

First, we substitute $x=3 t^{2}$ and $y=2 t$ into $∇f(x,y)$ to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\left(3 x + 3 y e^{x y}\right)\,i+\left(3 x e^{x y} + 3 y\right)\,j\Big|_{x=3 t^{2},\,y=2 t} \\  & =\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\,i+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t^{2}\right)\,i+\frac{\text{d}}{\text{d}t}\left(2 t\right)\,j \\  & =\left(6 t\right)\,i+\left(2\right)\,j.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =\left(\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\,i+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\,j\right)\cdot \left(\left(6 t\right)\,i+\left(2\right)\,j\right) \\  & =\left(3 t \left(3 t + 2 e^{6 t^{3}}\right)\right)\cdot \left(6 t\right)+\left(3 t \left(3 t e^{6 t^{3}} + 2\right)\right)\cdot \left(2\right) \\  & =\left(54 t^{3} + 36 t^{2} e^{6 t^{3}}\right)+\left(18 t^{2} e^{6 t^{3}} + 12 t\right) \\  & =6 t \left(9 t^{2} + 9 t e^{6 t^{3}} + 2\right).\end{aligned}
$$

Finally, evaluating the above at $t=1,$ we obtain

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))]\Big|_{t=1} & =6 t \left(9 t^{2} + 9 t e^{6 t^{3}} + 2\right)\Big|_{t=1} \\  & =\left(18 \left(3 + 2 e^{6}\right)\right)+\left(6 \left(2 + 3 e^{6}\right)\right) \\  & =6 \left(11 + 9 e^{6}\right).\end{aligned}
$$
