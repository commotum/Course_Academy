# Review: originals and explicitly generated variants

Source math basis 1356; six full radio banks, five rated easy and one unrated.

## Original q-36211

If $f(x,y)={x}^{2}+{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2{e}^{2t}+2{e}^{-2t}$
- $4{e}^{2t}$
- $2{e}^{2t}-2{e}^{-2t}$
- $2{e}^{t}-2{e}^{-t}$
- ${e}^{2t}+{e}^{-2t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+{y}^{2})\,j \\  & =2x\,i+2y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{t}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t}\,i+2{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =2{e}^{t}\cdot {e}^{t}-2{e}^{-t}\cdot {e}^{-t} \\  & =2{e}^{2t}-2{e}^{-2t}.\end{aligned}
$$

### Parameterized exact replay

If $f(x,y)={x}^{2}+{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2{e}^{2t}-2{e}^{-2t}$ [correct]
- $4{e}^{2t}$
- $2{e}^{2t}+2{e}^{-2t}$
- ${e}^{2t}+{e}^{-2t}$
- $2{e}^{t}-2{e}^{-t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+{y}^{2})\,j \\  & =2x\,i+2y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{t}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t}\,i+2{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =2{e}^{t}\cdot {e}^{t}-2{e}^{-t}\cdot {e}^{-t} \\  & =2{e}^{2t}-2{e}^{-2t}.\end{aligned}
$$

## Original q-95056

If $f(x, y) = \ln xy$ and $r(t) = \cos ti + t^{2}j$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{2t + 1}{t^{2}}$
- $\frac{2 - t\tan t}{t}$
- $\frac{t^{2}\tan t + 2}{t^{2}}$
- $\frac{2 - t\sec t}{t}$
- $\frac{t^{2}\sec t + 1}{t^{2}}$

[No captured solution or correct designation.]

### Parameterized completed replay — authored solution/level/designation

If $f(x, y) = \ln xy$ and $r(t) = \cos ti + t^{2}j$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{t^{2}\tan t + 2}{t^{2}}$
- $\frac{2 - t\tan t}{t}$ [correct]
- $\frac{2t + 1}{t^{2}}$
- $\frac{t^{2}\sec t + 1}{t^{2}}$
- $\frac{2 - t\sec t}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\ln xy)\,i+\frac{∂}{∂y}(\ln xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x=\cos t$ and $y=t^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\cos t}\,i+\frac{1}{t^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\cos t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j \\  & =-\sin t\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\cos t}\,i+\frac{1}{t^{2}}\,j)\cdot (-\sin t\,i+2t\,j) \\  & =(\frac{1}{\cos t})(-\sin t)+(\frac{1}{t^{2}})(2t) \\  & =\frac{2}{t}-\tan t.\end{aligned}
$$

## Original q-37099

If $f(x,y)=2x-x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+3{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2+9{t}^{3}+6{t}^{3}\operatorname{ln}⁡t$
- $\frac{2}{t}-3t-3t\operatorname{ln}⁡t$
- $\frac{2}{t}-3{t}^{2}+36{t}^{3}$
- $\frac{2}{t}-9{t}^{2}-12{t}^{2}\operatorname{ln}⁡t$
- $\frac{2}{t}-9{t}^{3}-36{t}^{3}\operatorname{ln}⁡t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2x-x{y}^{2})\,i+\frac{∂}{∂y}(2x-x{y}^{2})\,j \\  & =(2-{y}^{2})\,i-2xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y=3{t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2-9{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}(3{t}^{2})\,j \\  & =\frac{1}{t}\,i+6t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2-9{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+6t\,j) \\  & =(2-9{t}^{4})\cdot \frac{1}{t}+(-6{t}^{2}\operatorname{ln}⁡t)\cdot 6t \\  & =\frac{2}{t}-9{t}^{3}-36{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

### Parameterized exact replay

If $f(x,y)=2x-x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+3{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{2}{t}-3{t}^{2}+36{t}^{3}$
- $\frac{2}{t}-3t-3t\operatorname{ln}⁡t$
- $2+9{t}^{3}+6{t}^{3}\operatorname{ln}⁡t$
- $\frac{2}{t}-9{t}^{3}-36{t}^{3}\operatorname{ln}⁡t$ [correct]
- $\frac{2}{t}-9{t}^{2}-12{t}^{2}\operatorname{ln}⁡t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2x-x{y}^{2})\,i+\frac{∂}{∂y}(2x-x{y}^{2})\,j \\  & =(2-{y}^{2})\,i-2xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y=3{t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2-9{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}(3{t}^{2})\,j \\  & =\frac{1}{t}\,i+6t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2-9{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+6t\,j) \\  & =(2-9{t}^{4})\cdot \frac{1}{t}+(-6{t}^{2}\operatorname{ln}⁡t)\cdot 6t \\  & =\frac{2}{t}-9{t}^{3}-36{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

## Original q-95052

If $f(x,y)=y\operatorname{cos}⁡x$ and $r(t)=\pi t\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- ${e}^{t}\operatorname{cos}⁡\pi t-\operatorname{sin}⁡\pi t$
- ${e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t)$
- $\operatorname{cos}⁡\pi t-{e}^{t}\operatorname{sin}⁡\pi t$
- $\pi t+{e}^{t}\operatorname{cos}⁡\pi t$
- $\pi t-{e}^{t}\operatorname{sin}⁡\pi t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(y\operatorname{cos}⁡x)\,j \\  & =-y\operatorname{sin}⁡x\,i+\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=\pi t$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\pi t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =\pi \,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j)\cdot (\pi \,i+{e}^{t}\,j) \\  & =-\pi {e}^{t}\operatorname{sin}⁡\pi t+{e}^{t}\operatorname{cos}⁡\pi t \\  & ={e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t).\end{aligned}
$$

### Parameterized exact replay

If $f(x,y)=y\operatorname{cos}⁡x$ and $r(t)=\pi t\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\operatorname{cos}⁡\pi t-{e}^{t}\operatorname{sin}⁡\pi t$
- ${e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t)$ [correct]
- ${e}^{t}\operatorname{cos}⁡\pi t-\operatorname{sin}⁡\pi t$
- $\pi t-{e}^{t}\operatorname{sin}⁡\pi t$
- $\pi t+{e}^{t}\operatorname{cos}⁡\pi t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(y\operatorname{cos}⁡x)\,j \\  & =-y\operatorname{sin}⁡x\,i+\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=\pi t$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\pi t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =\pi \,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j)\cdot (\pi \,i+{e}^{t}\,j) \\  & =-\pi {e}^{t}\operatorname{sin}⁡\pi t+{e}^{t}\operatorname{cos}⁡\pi t \\  & ={e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t).\end{aligned}
$$

## Original q-95054

If $f(x,y)=\operatorname{ln}⁡(x{y}^{2})$ and $r(t)={t}^{-2}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{3({t}^{2}+1)}{t}$
- $\frac{{t}^{2}{e}^{t}+2}{{e}^{t}}$
- $\frac{2(t-1)}{t}$
- $t(t-2)$
- $\frac{2(t{e}^{t}-1)}{{e}^{t}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(x{y}^{2})\,i+\frac{∂}{∂y}\operatorname{ln}⁡(x{y}^{2})\,j \\  & =\frac{{y}^{2}}{x{y}^{2}}\,i+\frac{2xy}{x{y}^{2}}\,j \\  & =\frac{1}{x}\,i+\frac{2}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-2}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-2}}\,i+\frac{2}{{e}^{t}}\,j \\  & ={t}^{2}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-2})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-2{t}^{-3}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{2}\,i+2{e}^{-t}\,j)\cdot (-2{t}^{-3}\,i+{e}^{t}\,j) \\  & =-2({t}^{2})({t}^{-3})+2{e}^{-t}({e}^{t}) \\  & =2-\frac{2}{t} \\  & =\frac{2(t-1)}{t}.\end{aligned}
$$

### Parameterized exact replay

If $f(x,y)=\operatorname{ln}⁡(x{y}^{2})$ and $r(t)={t}^{-2}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{2(t-1)}{t}$ [correct]
- $\frac{{t}^{2}{e}^{t}+2}{{e}^{t}}$
- $\frac{3({t}^{2}+1)}{t}$
- $\frac{2(t{e}^{t}-1)}{{e}^{t}}$
- $t(t-2)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(x{y}^{2})\,i+\frac{∂}{∂y}\operatorname{ln}⁡(x{y}^{2})\,j \\  & =\frac{{y}^{2}}{x{y}^{2}}\,i+\frac{2xy}{x{y}^{2}}\,j \\  & =\frac{1}{x}\,i+\frac{2}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-2}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-2}}\,i+\frac{2}{{e}^{t}}\,j \\  & ={t}^{2}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-2})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-2{t}^{-3}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{2}\,i+2{e}^{-t}\,j)\cdot (-2{t}^{-3}\,i+{e}^{t}\,j) \\  & =-2({t}^{2})({t}^{-3})+2{e}^{-t}({e}^{t}) \\  & =2-\frac{2}{t} \\  & =\frac{2(t-1)}{t}.\end{aligned}
$$

## Original q-95059

If $f(x,y)=\operatorname{arctan}⁡xy$ and $r(t)={e}^{t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{{e}^{t}(\operatorname{cos}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{\operatorname{sin}⁡t+{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{sin}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}-\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡xy)\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡xy)\,j \\  & =\frac{y}{1+{x}^{2}{y}^{2}}\,i+\frac{x}{1+{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & ={e}^{t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j)\cdot ({e}^{t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{{e}^{t}\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}+\frac{{e}^{t}\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}.\end{aligned}
$$

### Parameterized exact replay

If $f(x,y)=\operatorname{arctan}⁡xy$ and $r(t)={e}^{t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}$ [correct]
- $\frac{\operatorname{sin}⁡t+{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{cos}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}-\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{sin}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡xy)\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡xy)\,j \\  & =\frac{y}{1+{x}^{2}{y}^{2}}\,i+\frac{x}{1+{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & ={e}^{t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j)\cdot ({e}^{t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{{e}^{t}\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}+\frac{{e}^{t}\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}.\end{aligned}
$$

## generated observed-profile variant — square_exp

If $f(x,y)={x}^{2}+2{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- ${e}^{2t}+2{e}^{-2t}$
- $2{e}^{2t}+4{e}^{-2t}$
- $2{e}^{2t}-4{e}^{-2t}$ [correct]
- $6{e}^{2t}$
- $2{e}^{t}-4{e}^{-t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+2{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+2{y}^{2})\,j \\  & =2x\,i+4y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{t}\,i+4{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t}\,i+4{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =2{e}^{t}\cdot {e}^{t}-4{e}^{-t}\cdot {e}^{-t} \\  & =2{e}^{2t}-4{e}^{-2t}.\end{aligned}
$$

## generated observed-profile variant — square_exp

If $f(x,y)={x}^{2}+{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- ${e}^{2t}+{e}^{-2t}$
- $2{e}^{2t}+2{e}^{-2t}$
- $2{e}^{t}-2{e}^{-t}$
- $4{e}^{2t}$
- $2{e}^{2t}-2{e}^{-2t}$ [correct]

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+{y}^{2})\,j \\  & =2x\,i+2y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{t}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t}\,i+2{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =2{e}^{t}\cdot {e}^{t}-2{e}^{-t}\cdot {e}^{-t} \\  & =2{e}^{2t}-2{e}^{-2t}.\end{aligned}
$$

## generated observed-profile variant — log_cos

If $f(x, y) = \ln xy$ and $r(t) = \cos ti + t^{2}j$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{t^{2}\sec t + 1}{t^{2}}$
- $\frac{2t + 1}{t^{2}}$
- $\frac{t^{2}\tan t + 2}{t^{2}}$
- $\frac{2 - t\tan t}{t}$ [correct]
- $\frac{2 - t\sec t}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\ln xy)\,i+\frac{∂}{∂y}(\ln xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x=\cos t$ and $y=t^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\cos t}\,i+\frac{1}{t^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\cos t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j \\  & =-\sin t\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\cos t}\,i+\frac{1}{t^{2}}\,j)\cdot (-\sin t\,i+2t\,j) \\  & =(\frac{1}{\cos t})(-\sin t)+(\frac{1}{t^{2}})(2t) \\  & =\frac{2}{t}-\tan t.\end{aligned}
$$

## generated observed-profile variant — log_cos

If $f(x, y) = \ln xy$ and $r(t) = \cos ti + tj$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{t^{2}\sec t + 1}{t^{2}}$
- $\frac{t + 1}{t^{2}}$
- $\frac{1 - t\sec t}{t}$
- $\frac{1 - t\tan t}{t}$ [correct]
- $\frac{t^{2}\tan t + 1}{t^{2}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\ln xy)\,i+\frac{∂}{∂y}(\ln xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x=\cos t$ and $y=t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\cos t}\,i+\frac{1}{t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\cos t)\,i+\frac{\text{d}}{\text{d}t}(t)\,j \\  & =-\sin t\,i+{t}^{0}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\cos t}\,i+\frac{1}{t}\,j)\cdot (-\sin t\,i+{t}^{0}\,j) \\  & =(\frac{1}{\cos t})(-\sin t)+(\frac{1}{t})({t}^{0}) \\  & =\frac{1}{t}-\tan t.\end{aligned}
$$

## generated observed-profile variant — polylog

If $f(x,y)=x-2x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{1}{t}-2{t}^{3}-8{t}^{3}\operatorname{ln}⁡t$ [correct]
- $1+2{t}^{3}+4{t}^{3}\operatorname{ln}⁡t$
- $\frac{1}{t}-2{t}^{2}+8{t}^{3}$
- $\frac{1}{t}-2t-2t\operatorname{ln}⁡t$
- $\frac{1}{t}-2{t}^{2}-8{t}^{2}\operatorname{ln}⁡t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x-2x{y}^{2})\,i+\frac{∂}{∂y}(x-2x{y}^{2})\,j \\  & =(1-2{y}^{2})\,i-4xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y={t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(1-2{t}^{4})\,i-4{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =\frac{1}{t}\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((1-2{t}^{4})\,i-4{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+2t\,j) \\  & =(1-2{t}^{4})\cdot \frac{1}{t}+(-4{t}^{2}\operatorname{ln}⁡t)\cdot 2t \\  & =\frac{1}{t}-2{t}^{3}-8{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

## generated observed-profile variant — polylog

If $f(x,y)=x-x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{1}{t}-{t}^{3}-4{t}^{3}\operatorname{ln}⁡t$ [correct]
- $1+{t}^{3}+2{t}^{3}\operatorname{ln}⁡t$
- $\frac{1}{t}-{t}^{2}-4{t}^{2}\operatorname{ln}⁡t$
- $\frac{1}{t}-t-t\operatorname{ln}⁡t$
- $\frac{1}{t}-{t}^{2}+4{t}^{3}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x-x{y}^{2})\,i+\frac{∂}{∂y}(x-x{y}^{2})\,j \\  & =(1-{y}^{2})\,i-2xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y={t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(1-{t}^{4})\,i-2{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =\frac{1}{t}\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((1-{t}^{4})\,i-2{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+2t\,j) \\  & =(1-{t}^{4})\cdot \frac{1}{t}+(-2{t}^{2}\operatorname{ln}⁡t)\cdot 2t \\  & =\frac{1}{t}-{t}^{3}-4{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

## generated observed-profile variant — cos_exp

If $f(x,y)=y\operatorname{cos}⁡x$ and $r(t)=\pi t\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\pi t-{e}^{t}\operatorname{sin}⁡\pi t$
- ${e}^{t}\operatorname{cos}⁡\pi t-\operatorname{sin}⁡\pi t$
- $\operatorname{cos}⁡\pi t-{e}^{t}\operatorname{sin}⁡\pi t$
- ${e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t)$ [correct]
- $\pi t+{e}^{t}\operatorname{cos}⁡\pi t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(y\operatorname{cos}⁡x)\,j \\  & =-y\operatorname{sin}⁡x\,i+\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=\pi t$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\pi t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =\pi \,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{t}\operatorname{sin}⁡\pi t\,i+\operatorname{cos}⁡\pi t\,j)\cdot (\pi \,i+{e}^{t}\,j) \\  & =-\pi {e}^{t}\operatorname{sin}⁡\pi t+{e}^{t}\operatorname{cos}⁡\pi t \\  & ={e}^{t}(\operatorname{cos}⁡\pi t-\pi \operatorname{sin}⁡\pi t).\end{aligned}
$$

## generated observed-profile variant — cos_exp

If $f(x,y)=y\operatorname{cos}⁡x$ and $r(t)=2t\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2t-{e}^{t}\operatorname{sin}⁡2t$
- ${e}^{t}\operatorname{cos}⁡2t-\operatorname{sin}⁡2t$
- $2t+{e}^{t}\operatorname{cos}⁡2t$
- ${e}^{t}(\operatorname{cos}⁡2t-2\operatorname{sin}⁡2t)$ [correct]
- $\operatorname{cos}⁡2t-{e}^{t}\operatorname{sin}⁡2t$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(y\operatorname{cos}⁡x)\,j \\  & =-y\operatorname{sin}⁡x\,i+\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=2t$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{t}\operatorname{sin}⁡2t\,i+\operatorname{cos}⁡2t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =2\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{t}\operatorname{sin}⁡2t\,i+\operatorname{cos}⁡2t\,j)\cdot (2\,i+{e}^{t}\,j) \\  & =-2{e}^{t}\operatorname{sin}⁡2t+{e}^{t}\operatorname{cos}⁡2t \\  & ={e}^{t}(\operatorname{cos}⁡2t-2\operatorname{sin}⁡2t).\end{aligned}
$$

## generated observed-profile variant — log_power

If $f(x,y)=\operatorname{ln}⁡(xy)$ and $r(t)={t}^{-2}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{(t{e}^{t}-1)}{{e}^{t}}$
- $\frac{2({t}^{2}+1)}{t}$
- $\frac{t-2}{t}$ [correct]
- $\frac{{t}^{2}{e}^{t}+1}{{e}^{t}}$
- $t(t-2)$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(xy)\,i+\frac{∂}{∂y}\operatorname{ln}⁡(xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-2}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-2}}\,i+\frac{1}{{e}^{t}}\,j \\  & ={t}^{2}\,i+{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-2})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-2{t}^{-3}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{2}\,i+{e}^{-t}\,j)\cdot (-2{t}^{-3}\,i+{e}^{t}\,j) \\  & =-2({t}^{2})({t}^{-3})+{e}^{-t}({e}^{t}) \\  & =1-\frac{2}{t} \\  & =\frac{t-2}{t}.\end{aligned}
$$

## generated observed-profile variant — log_power

If $f(x,y)=\operatorname{ln}⁡(xy)$ and $r(t)={t}^{-1}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{(t{e}^{t}-1)}{{e}^{t}}$
- $\frac{({t}^{2}+1)}{t}$
- $t(t-1)$
- $\frac{t{e}^{t}+1}{{e}^{t}}$
- $\frac{(t-1)}{t}$ [correct]

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(xy)\,i+\frac{∂}{∂y}\operatorname{ln}⁡(xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-1}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-1}}\,i+\frac{1}{{e}^{t}}\,j \\  & =t\,i+{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-1})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-{t}^{-2}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(t\,i+{e}^{-t}\,j)\cdot (-{t}^{-2}\,i+{e}^{t}\,j) \\  & =-(t)({t}^{-2})+{e}^{-t}({e}^{t}) \\  & =1-\frac{1}{t} \\  & =\frac{(t-1)}{t}.\end{aligned}
$$

## generated observed-profile variant — atan_product

If $f(x,y)=\operatorname{arctan}⁡xy$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{{e}^{2t}-\operatorname{cos}⁡t}{1+{e}^{4t}{sin}^{2}⁡t}$
- $\frac{{e}^{2t}(\operatorname{cos}⁡t+2)}{1+{e}^{4t}{sin}^{2}⁡t}$
- $\frac{{e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{4t}{sin}^{2}⁡t}$ [correct]
- $\frac{\operatorname{sin}⁡t+{e}^{2t}}{1+{e}^{4t}{sin}^{2}⁡t}$
- $\frac{{e}^{2t}(2\operatorname{sin}⁡t+1)}{1+{e}^{4t}{sin}^{2}⁡t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡xy)\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡xy)\,j \\  & =\frac{y}{1+{x}^{2}{y}^{2}}\,i+\frac{x}{1+{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{\operatorname{sin}⁡t}{1+{e}^{4t}{sin}^{2}⁡t}\,i+\frac{{e}^{2t}}{1+{e}^{4t}{sin}^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & =2{e}^{2t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\operatorname{sin}⁡t}{1+{e}^{4t}{sin}^{2}⁡t}\,i+\frac{{e}^{2t}}{1+{e}^{4t}{sin}^{2}⁡t}\,j)\cdot (2{e}^{2t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{2{e}^{2t}\operatorname{sin}⁡t}{1+{e}^{4t}{sin}^{2}⁡t}+\frac{{e}^{2t}\operatorname{cos}⁡t}{1+{e}^{4t}{sin}^{2}⁡t} \\  & =\frac{{e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{4t}{sin}^{2}⁡t}.\end{aligned}
$$

## generated observed-profile variant — atan_product

If $f(x,y)=\operatorname{arctan}⁡xy$ and $r(t)={e}^{t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{{e}^{t}-\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{cos}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{sin}⁡t+1)}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{\operatorname{sin}⁡t+{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}$
- $\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}$ [correct]

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡xy)\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡xy)\,j \\  & =\frac{y}{1+{x}^{2}{y}^{2}}\,i+\frac{x}{1+{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & ={e}^{t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}\,i+\frac{{e}^{t}}{1+{e}^{2t}{sin}^{2}⁡t}\,j)\cdot ({e}^{t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{{e}^{t}\operatorname{sin}⁡t}{1+{e}^{2t}{sin}^{2}⁡t}+\frac{{e}^{t}\operatorname{cos}⁡t}{1+{e}^{2t}{sin}^{2}⁡t} \\  & =\frac{{e}^{t}(\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{2t}{sin}^{2}⁡t}.\end{aligned}
$$

## generated authored-default variant — square_exp

If $f(x,y)=2{x}^{2}+2{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $4 \left(e^{t} - 1\right) \left(e^{t} + 1\right) \left(e^{2 t} + 1\right) e^{- 2 t}$ [correct]
- $0$
- $4 e^{2 t}$
- $4 \left(e^{2 t} + 1\right) e^{- t}$
- $4 \left(e^{4 t} + 1\right) e^{- 2 t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2{x}^{2}+2{y}^{2})\,i+\frac{∂}{∂y}(2{x}^{2}+2{y}^{2})\,j \\  & =4x\,i+4y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =4{e}^{t}\,i+4{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(4{e}^{t}\,i+4{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =4{e}^{t}\cdot {e}^{t}-4{e}^{-t}\cdot {e}^{-t} \\  & =4{e}^{2t}-4{e}^{-2t}.\end{aligned}
$$

## generated authored-default variant — square_exp

If $f(x,y)={x}^{2}+3{y}^{2}$ and $r(t)={e}^{t}\,i+{e}^{-t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2 \left(e^{2 t} + 3\right) e^{- t}$
- $4$
- $2 e^{2 t}$
- $2 \left(e^{4 t} - 3\right) e^{- 2 t}$ [correct]
- $2 \left(e^{4 t} + 3\right) e^{- 2 t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+3{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+3{y}^{2})\,j \\  & =2x\,i+6y\,j\end{aligned}
$$

Next, we substitute $x={e}^{t}$ and $y={e}^{-t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =2{e}^{t}\,i+6{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}({e}^{-t})\,j \\  & ={e}^{t}\,i-{e}^{-t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(2{e}^{t}\,i+6{e}^{-t}\,j)\cdot ({e}^{t}\,i-{e}^{-t}\,j) \\  & =2{e}^{t}\cdot {e}^{t}-6{e}^{-t}\cdot {e}^{-t} \\  & =2{e}^{2t}-6{e}^{-2t}.\end{aligned}
$$

## generated authored-default variant — log_cos

If $f(x, y) = \ln (x{y}^{2})$ and $r(t) = \cos ti + t^{2}j$, compute $\frac{d}{dt}[f(r(t))]$.

- $- \frac{t \sin{\left(t \right)} - 4 \cos{\left(t \right)}}{t \cos{\left(t \right)}}$ [correct]
- $\frac{2 \left(t^{3} - \sin{\left(t \right)} \cos{\left(t \right)}\right)}{t^{2} \cos{\left(t \right)}}$
- $- \frac{\sin{\left(t \right)}}{\cos{\left(t \right)}}$
- $\frac{t^{2} + 2 \cos{\left(t \right)}}{t^{2} \cos{\left(t \right)}}$
- $- \frac{t \sin{\left(t \right)} + 4 \cos{\left(t \right)}}{t \cos{\left(t \right)}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\ln (x{y}^{2}))\,i+\frac{∂}{∂y}(\ln (x{y}^{2}))\,j \\  & =\frac{{y}^{2}}{x{y}^{2}}\,i+\frac{2xy}{x{y}^{2}}\,j \\  & =\frac{1}{x}\,i+\frac{2}{y}\,j\end{aligned}
$$

Next, we substitute $x=\cos t$ and $y=t^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\cos t}\,i+\frac{2}{t^{2}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\cos t)\,i+\frac{\text{d}}{\text{d}t}(t^{2})\,j \\  & =-\sin t\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\cos t}\,i+\frac{2}{t^{2}}\,j)\cdot (-\sin t\,i+2t\,j) \\  & =(\frac{1}{\cos t})(-\sin t)+(\frac{2}{t^{2}})(2t) \\  & =\frac{4}{t}-\tan t.\end{aligned}
$$

## generated authored-default variant — log_cos

If $f(x, y) = \ln xy$ and $r(t) = \cos ti + t^{3}j$, compute $\frac{d}{dt}[f(r(t))]$.

- $\frac{t^{3} + \cos{\left(t \right)}}{t^{3} \cos{\left(t \right)}}$
- $\frac{3 t^{5} - \sin{\left(t \right)} \cos{\left(t \right)}}{t^{3} \cos{\left(t \right)}}$
- $- \frac{\sin{\left(t \right)}}{\cos{\left(t \right)}}$
- $- \frac{t \sin{\left(t \right)} - 3 \cos{\left(t \right)}}{t \cos{\left(t \right)}}$ [correct]
- $- \frac{t \sin{\left(t \right)} + 3 \cos{\left(t \right)}}{t \cos{\left(t \right)}}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\ln xy)\,i+\frac{∂}{∂y}(\ln xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x=\cos t$ and $y=t^{3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{\cos t}\,i+\frac{1}{t^{3}}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\cos t)\,i+\frac{\text{d}}{\text{d}t}(t^{3})\,j \\  & =-\sin t\,i+3{t}^{2}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{1}{\cos t}\,i+\frac{1}{t^{3}}\,j)\cdot (-\sin t\,i+3{t}^{2}\,j) \\  & =(\frac{1}{\cos t})(-\sin t)+(\frac{1}{t^{3}})(3{t}^{2}) \\  & =\frac{3}{t}-\tan t.\end{aligned}
$$

## generated authored-default variant — polylog

If $f(x,y)=2x-2x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- \frac{2 \left(4 t^{4} \ln{\left(t \right)} + t^{4} - 1\right)}{t}$ [correct]
- $- 4 t \left(t^{4} + \ln{\left(t \right)} - 1\right)$
- $- \frac{2 \left(t - 1\right) \left(t + 1\right) \left(t^{2} + 1\right)}{t}$
- $- 2 \left(t^{4} + 2 t^{2} \ln{\left(t \right)} - 1\right)$
- $\frac{2 \left(4 t^{4} \ln{\left(t \right)} - t^{4} + 1\right)}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2x-2x{y}^{2})\,i+\frac{∂}{∂y}(2x-2x{y}^{2})\,j \\  & =(2-2{y}^{2})\,i-4xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y={t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2-2{t}^{4})\,i-4{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =\frac{1}{t}\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((2-2{t}^{4})\,i-4{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+2t\,j) \\  & =(2-2{t}^{4})\cdot \frac{1}{t}+(-4{t}^{2}\operatorname{ln}⁡t)\cdot 2t \\  & =\frac{2}{t}-2{t}^{3}-8{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

## generated authored-default variant — polylog

If $f(x,y)=x-3x{y}^{2}$ and $r(t)=\operatorname{ln}⁡t\,i+{t}^{2}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- 3 t^{4} - 6 t^{2} \ln{\left(t \right)} + 1$
- $- 2 t \left(3 t^{4} + 3 \ln{\left(t \right)} - 1\right)$
- $- \frac{3 t^{4} - 1}{t}$
- $- \frac{12 t^{4} \ln{\left(t \right)} + 3 t^{4} - 1}{t}$ [correct]
- $\frac{12 t^{4} \ln{\left(t \right)} - 3 t^{4} + 1}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x-3x{y}^{2})\,i+\frac{∂}{∂y}(x-3x{y}^{2})\,j \\  & =(1-3{y}^{2})\,i-6xy\,j\end{aligned}
$$

Next, we substitute $x=\operatorname{ln}⁡t$ and $y={t}^{2}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(1-3{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j \\  & =\frac{1}{t}\,i+2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((1-3{t}^{4})\,i-6{t}^{2}\operatorname{ln}⁡t\,j)\cdot (\frac{1}{t}\,i+2t\,j) \\  & =(1-3{t}^{4})\cdot \frac{1}{t}+(-6{t}^{2}\operatorname{ln}⁡t)\cdot 2t \\  & =\frac{1}{t}-3{t}^{3}-12{t}^{3}\operatorname{ln}⁡t.\end{aligned}
$$

## generated authored-default variant — cos_exp

If $f(x,y)=2y\operatorname{cos}⁡x$ and $r(t)=\pi t\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $2 \left(- \pi \sin{\left(\pi t \right)} + \cos{\left(\pi t \right)}\right) e^{t}$ [correct]
- $2 \left(- e^{2 t} \sin{\left(\pi t \right)} + \pi \cos{\left(\pi t \right)}\right)$
- $- 2 \pi e^{t} \sin{\left(\pi t \right)}$
- $2 \left(- e^{t} \sin{\left(\pi t \right)} + \cos{\left(\pi t \right)}\right)$
- $- 2 \left(\pi \sin{\left(\pi t \right)} + \cos{\left(\pi t \right)}\right) e^{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(2y\operatorname{cos}⁡x)\,j \\  & =-2y\operatorname{sin}⁡x\,i+2\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=\pi t$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-2{e}^{t}\operatorname{sin}⁡\pi t\,i+2\operatorname{cos}⁡\pi t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\pi t)\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =\pi \,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-2{e}^{t}\operatorname{sin}⁡\pi t\,i+2\operatorname{cos}⁡\pi t\,j)\cdot (\pi \,i+{e}^{t}\,j) \\  & =-2 \pi {e}^{t}\operatorname{sin}⁡\pi t+2{e}^{t}\operatorname{cos}⁡\pi t \\  & ={e}^{t}(2\operatorname{cos}⁡\pi t-2 \pi \operatorname{sin}⁡\pi t).\end{aligned}
$$

## generated authored-default variant — cos_exp

If $f(x,y)=y\operatorname{cos}⁡x$ and $r(t)=t\,i+{e}^{2t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- 2 e^{4 t} \sin{\left(t \right)} + \cos{\left(t \right)}$
- $- \left(\sin{\left(t \right)} + 2 \cos{\left(t \right)}\right) e^{2 t}$
- $- e^{2 t} \sin{\left(t \right)}$
- $- e^{2 t} \sin{\left(t \right)} + \cos{\left(t \right)}$
- $\left(- \sin{\left(t \right)} + 2 \cos{\left(t \right)}\right) e^{2 t}$ [correct]

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(y\operatorname{cos}⁡x)\,i+\frac{∂}{∂y}(y\operatorname{cos}⁡x)\,j \\  & =-y\operatorname{sin}⁡x\,i+\operatorname{cos}⁡x\,j\end{aligned}
$$

Next, we substitute $x=t$ and $y={e}^{2t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =-{e}^{2t}\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}({e}^{2t})\,j \\  & =1\,i+2{e}^{2t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(-{e}^{2t}\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j)\cdot (1\,i+2{e}^{2t}\,j) \\  & =-{e}^{2t}\operatorname{sin}⁡t+2{e}^{2t}\operatorname{cos}⁡t \\  & ={e}^{2t}(2\operatorname{cos}⁡t-\operatorname{sin}⁡t).\end{aligned}
$$

## generated authored-default variant — log_power

If $f(x,y)=\operatorname{ln}⁡(x{y}^{2})$ and $r(t)={t}^{-2}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{2 \left(t - 1\right)}{t}$ [correct]
- $\frac{\left(t^{5} e^{2 t} - 4\right) e^{- t}}{t^{3}}$
- $- \frac{2}{t}$
- $\left(t^{2} e^{t} + 2\right) e^{- t}$
- $- \frac{2 \left(t + 1\right)}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(x{y}^{2})\,i+\frac{∂}{∂y}\operatorname{ln}⁡(x{y}^{2})\,j \\  & =\frac{{y}^{2}}{x{y}^{2}}\,i+\frac{2xy}{x{y}^{2}}\,j \\  & =\frac{1}{x}\,i+\frac{2}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-2}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-2}}\,i+\frac{2}{{e}^{t}}\,j \\  & ={t}^{2}\,i+2{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-2})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-2{t}^{-3}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{2}\,i+2{e}^{-t}\,j)\cdot (-2{t}^{-3}\,i+{e}^{t}\,j) \\  & =-2({t}^{2})({t}^{-3})+2{e}^{-t}({e}^{t}) \\  & =2-\frac{2}{t} \\  & =\frac{2(t-1)}{t}.\end{aligned}
$$

## generated authored-default variant — log_power

If $f(x,y)=\operatorname{ln}⁡(xy)$ and $r(t)={t}^{-3}\,i+{e}^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\left(t^{3} e^{t} + 1\right) e^{- t}$
- $\frac{\left(t^{7} e^{2 t} - 3\right) e^{- t}}{t^{4}}$
- $- \frac{3}{t}$
- $\frac{t - 3}{t}$ [correct]
- $- \frac{t + 3}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}\operatorname{ln}⁡(xy)\,i+\frac{∂}{∂y}\operatorname{ln}⁡(xy)\,j \\  & =\frac{y}{xy}\,i+\frac{x}{xy}\,j \\  & =\frac{1}{x}\,i+\frac{1}{y}\,j\end{aligned}
$$

Next, we substitute $x={t}^{-3}$ and $y={e}^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{1}{{t}^{-3}}\,i+\frac{1}{{e}^{t}}\,j \\  & ={t}^{3}\,i+{e}^{-t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{-3})\,i+\frac{\text{d}}{\text{d}t}({e}^{t})\,j \\  & =-3{t}^{-4}\,i+{e}^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =({t}^{3}\,i+{e}^{-t}\,j)\cdot (-3{t}^{-4}\,i+{e}^{t}\,j) \\  & =-3({t}^{3})({t}^{-4})+{e}^{-t}({e}^{t}) \\  & =1-\frac{3}{t} \\  & =\frac{t-3}{t}.\end{aligned}
$$

## generated authored-default variant — atan_product

If $f(x,y)=\operatorname{arctan}⁡(2xy)$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{2 \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}}{4 e^{4 t} \sin^{2}{\left(t \right)} + 1}$ [correct]
- $\frac{2 \left(2 e^{4 t} + \sin{\left(t \right)} \cos{\left(t \right)}\right)}{4 e^{4 t} \sin^{2}{\left(t \right)} + 1}$
- $\frac{4 e^{2 t} \sin{\left(t \right)}}{4 e^{4 t} \sin^{2}{\left(t \right)} + 1}$
- $\frac{2 \left(e^{2 t} + \sin{\left(t \right)}\right)}{4 e^{4 t} \sin^{2}{\left(t \right)} + 1}$
- $- \frac{2 \left(- 2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}}{4 e^{4 t} \sin^{2}{\left(t \right)} + 1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(2xy))\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡(2xy))\,j \\  & =\frac{2y}{1+4{x}^{2}{y}^{2}}\,i+\frac{2x}{1+4{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{2\operatorname{sin}⁡t}{1+4{e}^{4t}\sin^{2}⁡t}\,i+\frac{2{e}^{2t}}{1+4{e}^{4t}\sin^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & =2{e}^{2t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{2\operatorname{sin}⁡t}{1+4{e}^{4t}\sin^{2}⁡t}\,i+\frac{2{e}^{2t}}{1+4{e}^{4t}\sin^{2}⁡t}\,j)\cdot (2{e}^{2t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{4{e}^{2t}\operatorname{sin}⁡t}{1+4{e}^{4t}\sin^{2}⁡t}+\frac{2{e}^{2t}\operatorname{cos}⁡t}{1+4{e}^{4t}\sin^{2}⁡t} \\  & =\frac{2{e}^{2t}(2\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+4{e}^{4t}\sin^{2}⁡t}.\end{aligned}
$$

## generated authored-default variant — atan_product

If $f(x,y)=\operatorname{arctan}⁡xy$ and $r(t)={e}^{3t}\,i+\operatorname{sin}⁡t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $\frac{e^{3 t} + \sin{\left(t \right)}}{e^{6 t} \sin^{2}{\left(t \right)} + 1}$
- $\frac{3 e^{6 t} + \sin{\left(t \right)} \cos{\left(t \right)}}{e^{6 t} \sin^{2}{\left(t \right)} + 1}$
- $\frac{3 e^{3 t} \sin{\left(t \right)}}{e^{6 t} \sin^{2}{\left(t \right)} + 1}$
- $\frac{\left(3 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{3 t}}{e^{6 t} \sin^{2}{\left(t \right)} + 1}$ [correct]
- $- \frac{\left(- 3 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{3 t}}{e^{6 t} \sin^{2}{\left(t \right)} + 1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡xy)\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡xy)\,j \\  & =\frac{y}{1+{x}^{2}{y}^{2}}\,i+\frac{x}{1+{x}^{2}{y}^{2}}\,j\text{ }\end{aligned}
$$

Next, we substitute $x={e}^{3t}$ and $y=\operatorname{sin}⁡t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{\operatorname{sin}⁡t}{1+{e}^{6t}\sin^{2}⁡t}\,i+\frac{{e}^{3t}}{1+{e}^{6t}\sin^{2}⁡t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{3t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j \\  & =3{e}^{3t}\,i+\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\operatorname{sin}⁡t}{1+{e}^{6t}\sin^{2}⁡t}\,i+\frac{{e}^{3t}}{1+{e}^{6t}\sin^{2}⁡t}\,j)\cdot (3{e}^{3t}\,i+\operatorname{cos}⁡t\,j) \\  & =\frac{3{e}^{3t}\operatorname{sin}⁡t}{1+{e}^{6t}\sin^{2}⁡t}+\frac{{e}^{3t}\operatorname{cos}⁡t}{1+{e}^{6t}\sin^{2}⁡t} \\  & =\frac{{e}^{3t}(3\operatorname{sin}⁡t+\operatorname{cos}⁡t)}{1+{e}^{6t}\sin^{2}⁡t}.\end{aligned}
$$

## generated authored-default variant — mixed_polynomial

If $f(x,y)=x^{2} + x y^{2}$ and $r(t)=\ln{\left(t \right)}\,i+e^{t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- \frac{2 t e^{2 t} \ln{\left(t \right)} - e^{2 t} - 2 \ln{\left(t \right)}}{t}$
- $\frac{e^{2 t} + 2 \ln{\left(t \right)}}{t}$
- $\frac{2 t e^{2 t} \ln{\left(t \right)} + e^{2 t} + 2 \ln{\left(t \right)}}{t}$ [correct]
- $\frac{\left(t e^{2 t} + 2 t \ln{\left(t \right)} + 2 \ln{\left(t \right)}\right) e^{t}}{t}$
- $e^{2 t} + 2 e^{t} \ln{\left(t \right)} + 2 \ln{\left(t \right)}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x^{2} + x y^{2})\,i+\frac{∂}{∂y}(x^{2} + x y^{2})\,j \\  & =(2 x + y^{2})\,i+2 x y\,j\end{aligned}
$$

Next, we substitute $x=\ln{\left(t \right)}$ and $y=e^{t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2(\ln{\left(t \right)})+(e^{t})^{2})\,i+2(\ln{\left(t \right)})(e^{t})\,j \\  & =(e^{2 t} + 2 \ln{\left(t \right)})\,i+2 e^{t} \ln{\left(t \right)}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(e^{t})\,j \\  & =\frac{1}{t}\,i+e^{t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{2 t} + 2 \ln{\left(t \right)})\,i+2 e^{t} \ln{\left(t \right)}\,j)\cdot (\frac{1}{t}\,i+e^{t}\,j) \\  & =((e^{2 t} + 2 \ln{\left(t \right)}))(\frac{1}{t})+(2 e^{t} \ln{\left(t \right)})(e^{t}) \\  & =\frac{2 \ln{\left(t \right)}}{t}+\frac{e^{2 t}}{t}+2 e^{2 t} \ln{\left(t \right)} \\  & =2 e^{2 t} \ln{\left(t \right)} + \frac{e^{2 t}}{t} + \frac{2 \ln{\left(t \right)}}{t}.\end{aligned}
$$

## generated authored-default variant — mixed_polynomial

If $f(x,y)=x^{2} + x y^{2}$ and $r(t)=\ln{\left(t \right)}\,i+e^{2 t}\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- \frac{4 t e^{4 t} \ln{\left(t \right)} - e^{4 t} - 2 \ln{\left(t \right)}}{t}$
- $e^{4 t} + 2 e^{2 t} \ln{\left(t \right)} + 2 \ln{\left(t \right)}$
- $\frac{2 \left(t e^{4 t} + 2 t \ln{\left(t \right)} + \ln{\left(t \right)}\right) e^{2 t}}{t}$
- $\frac{4 t e^{4 t} \ln{\left(t \right)} + e^{4 t} + 2 \ln{\left(t \right)}}{t}$ [correct]
- $\frac{e^{4 t} + 2 \ln{\left(t \right)}}{t}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x^{2} + x y^{2})\,i+\frac{∂}{∂y}(x^{2} + x y^{2})\,j \\  & =(2 x + y^{2})\,i+2 x y\,j\end{aligned}
$$

Next, we substitute $x=\ln{\left(t \right)}$ and $y=e^{2 t}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =(2(\ln{\left(t \right)})+(e^{2 t})^{2})\,i+2(\ln{\left(t \right)})(e^{2 t})\,j \\  & =(e^{4 t} + 2 \ln{\left(t \right)})\,i+2 e^{2 t} \ln{\left(t \right)}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(e^{2 t})\,j \\  & =\frac{1}{t}\,i+2 e^{2 t}\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =((e^{4 t} + 2 \ln{\left(t \right)})\,i+2 e^{2 t} \ln{\left(t \right)}\,j)\cdot (\frac{1}{t}\,i+2 e^{2 t}\,j) \\  & =((e^{4 t} + 2 \ln{\left(t \right)}))(\frac{1}{t})+(2 e^{2 t} \ln{\left(t \right)})(2 e^{2 t}) \\  & =\frac{2 \ln{\left(t \right)}}{t}+\frac{e^{4 t}}{t}+4 e^{4 t} \ln{\left(t \right)} \\  & =4 e^{4 t} \ln{\left(t \right)} + \frac{e^{4 t}}{t} + \frac{2 \ln{\left(t \right)}}{t}.\end{aligned}
$$

## generated authored-default variant — atan_squared

If $f(x,y)=\operatorname{arctan}⁡(x{y}^{2})$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡2t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- \frac{2 \left(- \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right) e^{2 t} \sin{\left(2 t \right)}}{e^{4 t} \sin^{4}{\left(2 t \right)} + 1}$
- $\frac{2 e^{2 t} \sin^{2}{\left(2 t \right)}}{e^{4 t} \sin^{4}{\left(2 t \right)} + 1}$
- $\frac{2 \left(\sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right) e^{2 t} \sin{\left(2 t \right)}}{e^{4 t} \sin^{4}{\left(2 t \right)} + 1}$ [correct]
- $\frac{2 \left(2 e^{4 t} + \sin{\left(2 t \right)} \cos{\left(2 t \right)}\right) \sin{\left(2 t \right)}}{e^{4 t} \sin^{4}{\left(2 t \right)} + 1}$
- $\frac{\left(2 e^{2 t} + \sin{\left(2 t \right)}\right) \sin{\left(2 t \right)}}{e^{4 t} \sin^{4}{\left(2 t \right)} + 1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(x{y}^{2}))\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡(x{y}^{2}))\,j \\  & =\frac{(1{y}^{2}+x2y\cdot 0)}{1+{x}^{2}{y}^{4}}\,i+\frac{(0{y}^{2}+x2y\cdot 1)}{1+{x}^{2}{y}^{4}}\,j \\  & =\frac{{y}^{2}}{1+{x}^{2}{y}^{4}}\,i+\frac{2xy}{1+{x}^{2}{y}^{4}}\,j\end{aligned}
$$

Next, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡2t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{(\operatorname{sin}⁡2t)^{2}}{1+({e}^{2t})^{2}(\operatorname{sin}⁡2t)^{4}}\,i+\frac{2({e}^{2t})(\operatorname{sin}⁡2t)}{1+({e}^{2t})^{2}(\operatorname{sin}⁡2t)^{4}}\,j \\  & =\frac{\sin^{2}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t}\,i+\frac{2{e}^{2t}\operatorname{sin}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡2t)\,j \\  & =2{e}^{2t}\,i+2\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\sin^{2}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t}\,i+\frac{2{e}^{2t}\operatorname{sin}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t}\,j)\cdot (2{e}^{2t}\,i+2\operatorname{cos}⁡2t\,j) \\  & =\frac{2{e}^{2t}\sin^{2}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t}+\frac{4{e}^{2t}\operatorname{sin}⁡2t\operatorname{cos}⁡2t}{1+{e}^{4t}\sin^{4}⁡2t} \\  & =\frac{{e}^{2t}(2\sin^{2}⁡2t+4\operatorname{sin}⁡2t\operatorname{cos}⁡2t)}{1+{e}^{4t}\sin^{4}⁡2t}.\end{aligned}
$$

## generated authored-default variant — atan_squared

If $f(x,y)=\operatorname{arctan}⁡(x{y}^{2})$ and $r(t)={e}^{2t}\,i+\operatorname{sin}⁡3t\,j,$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$

- $- \frac{2 \left(- \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{2 t} \sin{\left(3 t \right)}}{e^{4 t} \sin^{4}{\left(3 t \right)} + 1}$
- $\frac{\left(2 e^{2 t} + \sin{\left(3 t \right)}\right) \sin{\left(3 t \right)}}{e^{4 t} \sin^{4}{\left(3 t \right)} + 1}$
- $\frac{\left(4 e^{4 t} + 3 \sin{\left(3 t \right)} \cos{\left(3 t \right)}\right) \sin{\left(3 t \right)}}{e^{4 t} \sin^{4}{\left(3 t \right)} + 1}$
- $\frac{2 \left(\sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{2 t} \sin{\left(3 t \right)}}{e^{4 t} \sin^{4}{\left(3 t \right)} + 1}$ [correct]
- $\frac{2 e^{2 t} \sin^{2}{\left(3 t \right)}}{e^{4 t} \sin^{4}{\left(3 t \right)} + 1}$

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(x{y}^{2}))\,i+\frac{∂}{∂y}(\operatorname{arctan}⁡(x{y}^{2}))\,j \\  & =\frac{(1{y}^{2}+x2y\cdot 0)}{1+{x}^{2}{y}^{4}}\,i+\frac{(0{y}^{2}+x2y\cdot 1)}{1+{x}^{2}{y}^{4}}\,j \\  & =\frac{{y}^{2}}{1+{x}^{2}{y}^{4}}\,i+\frac{2xy}{1+{x}^{2}{y}^{4}}\,j\end{aligned}
$$

Next, we substitute $x={e}^{2t}$ and $y=\operatorname{sin}⁡3t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =\frac{(\operatorname{sin}⁡3t)^{2}}{1+({e}^{2t})^{2}(\operatorname{sin}⁡3t)^{4}}\,i+\frac{2({e}^{2t})(\operatorname{sin}⁡3t)}{1+({e}^{2t})^{2}(\operatorname{sin}⁡3t)^{4}}\,j \\  & =\frac{\sin^{2}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t}\,i+\frac{2{e}^{2t}\operatorname{sin}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t}\,j\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡3t)\,j \\  & =2{e}^{2t}\,i+3\operatorname{cos}⁡3t\,j.\end{aligned}
$$

Finally, applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =(\frac{\sin^{2}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t}\,i+\frac{2{e}^{2t}\operatorname{sin}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t}\,j)\cdot (2{e}^{2t}\,i+3\operatorname{cos}⁡3t\,j) \\  & =\frac{2{e}^{2t}\sin^{2}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t}+\frac{6{e}^{2t}\operatorname{sin}⁡3t\operatorname{cos}⁡3t}{1+{e}^{4t}\sin^{4}⁡3t} \\  & =\frac{{e}^{2t}(2\sin^{2}⁡3t+6\operatorname{sin}⁡3t\operatorname{cos}⁡3t)}{1+{e}^{4t}\sin^{4}⁡3t}.\end{aligned}
$$
