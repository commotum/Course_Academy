# Template extraction (four stages)

## 1. Specific source descriptions

Each table row is a distinct mathematical/prompt/solution family; source ordering below is evidence order only. Raw records are preserved in `source.json`.

### q-33122

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨3t-1,\,6-t,\,7t⟩ \\ g(t) & =⟨{t}^{2},\,1-{t}^{2},\,t⟩\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3t-1),\,\frac{\text{d}}{\text{d}t}(6-t),\,\frac{\text{d}}{\text{d}t}(7t)⟩ \\  & =⟨3,\,-1,\,7⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}(1-{t}^{2}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨2t,\,-2t,\,1⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨3,\,-1,\,7⟩+⟨2t,\,-2t,\,1⟩ \\  & =⟨2t+3,\,-2t-1,\,8⟩\end{aligned}
$$

### q-33143

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)|= ⟨2t^{2}, t - 3, 8 + t^{3}⟩; g(t)|= ⟨t^{2} + 2t, 8, 2t^{3}⟩$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

Missing in snapshot; authored supported solution is separately labeled.

### q-128137

Find the value of $(f(t)-3g(t))^{′}$ at $t=0,$ if 

$$
\begin{aligned}f(t) & =⟨2\sqrt{t+1},\,{t}^{3},\,\operatorname{ln}⁡(t+1)⟩, \\ g(t) & =⟨\frac{1}{3(t+1)},\,\operatorname{sin}⁡t,\,\operatorname{tan}⁡t⟩.\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

First, notice that

$$
(f(t)-3g(t))^{′}={f}^{′}(t)-3{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2\sqrt{t+1}),\,\frac{\text{d}}{\text{d}t}({t}^{3}),\,\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(t+1))⟩ \\  & =⟨\frac{1}{\sqrt{t+1}},\,3{t}^{2},\,\frac{1}{t+1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\frac{1}{3(t+1)}),\,\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t),\,\frac{\text{d}}{\text{d}t}(\operatorname{tan}⁡t)⟩ \\  & =⟨-\frac{1}{3(t+1)^{2}},\,\operatorname{cos}⁡t,\,{sec}^{2}⁡t⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(0)-3g(0))^{′} & ={f}^{′}(0)-3{g}^{′}(0) \\  & =⟨\frac{1}{\sqrt{0+1}},\,3(0)^{2},\,\frac{1}{0+1}⟩-3⟨-\frac{1}{3(0+1)^{2}},\,\operatorname{cos}⁡0,\,{sec}^{2}⁡0⟩ \\  & =⟨1,0,1⟩-3⟨-\frac{1}{3},1,1⟩ \\  & =⟨1,0,1⟩-⟨-1,3,3⟩ \\  & =⟨2,-3,-2⟩.\end{aligned}
$$

### q-128452

Find the value of $(2f(t)-g(t))^{′}$ at $t=-1,$ if 

$$
\begin{aligned}f(t) & =⟨8\sqrt{3-t},\,\operatorname{sin}⁡(\pi t),\,\operatorname{ln}⁡(2t)⟩, \\ g(t) & =⟨{t}^{2}-t,\,\pi {t}^{2},\,1-{t}^{2}⟩.\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

First, notice that

$$
(2f(t)-g(t))^{′}=2{f}^{′}(t)-{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(8\sqrt{3-t}),\,\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t)),\,\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(2t))⟩ \\  & =⟨-\frac{4}{\sqrt{3-t}},\,\pi \operatorname{cos}⁡(\pi t),\,\frac{1}{t}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}-t),\,\frac{\text{d}}{\text{d}t}(\pi {t}^{2}),\,\frac{\text{d}}{\text{d}t}(1-{t}^{2})⟩ \\  & =⟨2t-1,\,2\pi t,\,-2t⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(2f(-1)-g(-1))^{′} & =2{f}^{′}(-1)-{g}^{′}(-1) \\  & =2⟨-\frac{4}{\sqrt{3-(-1)}},\,\pi \operatorname{cos}⁡(-\pi ),\,\frac{1}{(-1)}⟩-⟨2(-1)-1,\,2\pi (-1),\,-2(-1)⟩ \\  & =2⟨-2,-\pi ,-1⟩-⟨-3,-2\pi ,2⟩ \\  & =⟨-4,-2\pi ,-2⟩-⟨-3,-2\pi ,2⟩ \\  & =⟨-1,0,-4⟩.\end{aligned}
$$

### q-128458

Find the value of $(2f(t)+5g(t))^{′}$ at $t=1,$ where

$$
\begin{aligned}f(t)=[\begin{aligned}2\sqrt{3+t} \\ \operatorname{cos}⁡(t-1) \\ 1\end{aligned}],\,g(t)=[\begin{aligned}2t-3 \\ {t}^{2} \\ (t+1)^{2}\end{aligned}]\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

By the sum rule, we have 
 

$$
(2f(t)+5g(t))^{′}=2{f}^{′}(t)+5{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}\,(2\sqrt{3+t}) \\ \frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t-1)) \\ \frac{\text{d}}{\text{d}t}(1)\end{aligned}]=[\begin{aligned}\frac{1}{\sqrt{3+t}} \\ -\operatorname{sin}⁡(t-1) \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2t-3) \\ \frac{\text{d}}{\text{d}t}({t}^{2}) \\ \frac{\text{d}}{\text{d}t}((t+1)^{2})\end{aligned}]=[\begin{aligned}2 \\ 2t \\ 2(t+1)\end{aligned}]\end{aligned}
$$

Hence , we get

$$
\begin{aligned}(2f(1)+5g(1))^{′} & =2{f}^{′}(1)+5{g}^{′}(1) \\  & =2[\begin{aligned}\frac{1}{\sqrt{3+1}} \\ -\operatorname{sin}⁡(1-1) \\ 0\end{aligned}]+5[\begin{aligned}2 \\ 2(1) \\ 2(1+1)\end{aligned}] \\  & =2[\begin{aligned}\frac{1}{2} \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}2 \\ 2 \\ 4\end{aligned}] \\  & =[\begin{aligned}1 \\ 0 \\ 0\end{aligned}]+[\begin{aligned}10 \\ 10 \\ 20\end{aligned}] \\  & =[\begin{aligned}11 \\ 10 \\ 20\end{aligned}].\end{aligned}
$$

### q-32499

Differentiate $2g(t)-h(t)$ with respect to $t$, where

$$
\begin{aligned}g(t) & =⟨\operatorname{cos}⁡t,\,3t-3,\,-{t}^{2}⟩ \\ h(t) & =⟨\operatorname{sin}⁡t,\,-t,\,4⟩\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

Using the constant multiple and the sum rules, we have

$$
(2g(t)-h(t))^{′}=2{g}^{′}(t)-{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}\operatorname{cos}⁡t,\,\frac{\text{d}}{\text{d}t}(3t-3),\,\frac{\text{d}}{\text{d}t}(-{t}^{2})⟩ \\  & =⟨-\operatorname{sin}⁡t,\,3,\,-2t⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}\operatorname{sin}⁡t,\,\frac{\text{d}}{\text{d}t}(-t),\,\frac{\text{d}}{\text{d}t}4⟩ \\  & =⟨\operatorname{cos}⁡t,\,-1,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2g(t)-h(t))^{′} & =2{g}^{′}(t)-{h}^{′}(t) \\  & =2⟨-\operatorname{sin}⁡t,\,3,\,-2t⟩-⟨\operatorname{cos}⁡t,\,-1,\,0⟩ \\  & =⟨-2\operatorname{sin}⁡t,\,6,\,-4t⟩-⟨\operatorname{cos}⁡t,\,-1,\,0⟩ \\  & =⟨-2\operatorname{sin}⁡t-\operatorname{cos}⁡t,\,6-(-1),\,-4t-0⟩ \\  & =⟨-2\operatorname{sin}⁡t-\operatorname{cos}⁡t,\,7,\,-4t⟩\end{aligned}
$$

### q-32503

Differentiate $f(t)+g(t)+h(t)$ with respect to $t$, where

$$
\begin{aligned}f(t) & =⟨-1,\,0,\,1⟩ \\ g(t) & =⟨-t,\,0,t⟩ \\ h(t) & =⟨-{t}^{2},0,{t}^{2}⟩\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

Using the sum rule, we can write

$$
(f(t)+g(t)+h(t))^{′}={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(-1),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(1)⟩ \\  & =⟨0,0,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(-t),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨-1,0,1⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(-{t}^{2}),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}({t}^{2})⟩ \\  & =⟨-2t,\,0,\,2t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t)+h(t))^{′} & ={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t) \\  & =⟨0,0,0⟩+⟨-1,0,1⟩+⟨-2t,\,0,\,2t⟩ \\  & =⟨-2t-1,\,0,\,2t+1⟩\end{aligned}
$$

### q-33123

Differentiate $2f(t)+3g(t)$ with respect to $t$, where

 

$$
\begin{aligned}f(t) & =2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,(j-\,k) \\ g(t) & =(5-\operatorname{sin}⁡t)\,i-\,j+2\operatorname{cos}⁡t\,k\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

Using the constant multiple and the sum rules, we have 

$$
(2f(t)+3g(t))^{′}=2{f}^{′}(t)+3{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t)\,j-\frac{\text{d}}{\text{d}t}(3\operatorname{cos}⁡t)\,k \\  & =2\operatorname{cos}⁡t\,i-3\operatorname{sin}⁡t\,j+3\operatorname{sin}⁡t\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5-\operatorname{sin}⁡t)\,i-\frac{\text{d}}{\text{d}t}1\,j+\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡t)\,k \\  & =-\operatorname{cos}⁡ti-2\operatorname{sin}⁡t\,k\end{aligned}
$$

Hence 

$$
\begin{aligned}(2f(t)+3g(t))^{′} & =2{f}^{′}(t)+3{g}^{′}(t) \\  & =2(2\operatorname{cos}⁡t\,i-3\operatorname{sin}⁡t\,j+3\operatorname{sin}⁡t\,k)+3(-\operatorname{cos}⁡ti-2\operatorname{sin}⁡t\,k) \\  & =4\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k-3\operatorname{cos}⁡ti-6\operatorname{sin}⁡t\,k \\  & =\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j\end{aligned}
$$

### q-70681

Differentiate $f(t)+4g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨\sqrt{t},\,\operatorname{ln}⁡t,\,2⟩ \\ g(t) & =⟨t,\,\frac{1}{t},\,{t}^{4}⟩\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

Using the constant multiple rule and the sum rule, we have

$$
(f(t)+4g(t))^{′}={f}^{′}(t)+4{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\sqrt{t}),\,\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t),\,\frac{\text{d}}{\text{d}t}(2)⟩ \\  & =⟨\frac{1}{2\sqrt{t}},\,\frac{1}{t},\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(\frac{1}{t}),\,\frac{\text{d}}{\text{d}t}({t}^{4})⟩ \\  & =⟨1,\,-\frac{1}{{t}^{2}},\,4{t}^{3}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+4g(t))^{′} & ={f}^{′}(t)+4{g}^{′}(t) \\  & =⟨\frac{1}{2\sqrt{t}},\,\frac{1}{t},\,0⟩+4⟨1,\,-\frac{1}{{t}^{2}},\,4{t}^{3}⟩ \\  & =⟨\frac{1}{2\sqrt{t}},\,\frac{1}{t},\,0⟩+⟨4,\,-\frac{4}{{t}^{2}},\,16{t}^{3}⟩ \\  & =⟨\frac{1}{2\sqrt{t}}+4,\,\frac{1}{t}-\frac{4}{{t}^{2}},\,0+16{t}^{3}⟩ \\  & =⟨\frac{1+8\sqrt{t}}{2\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,16{t}^{3}⟩\end{aligned}
$$

### q-127998

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨1-2t,\,{t}^{2},\,(t-1)^{2}⟩, \\ g(t) & =⟨t+1,\,1-2t,\,{t}^{3}⟩\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(1-2t),\,\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}((t-1)^{2})⟩ \\  & =⟨-2,\,2t,\,2(t-1)⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t+1),\,\frac{\text{d}}{\text{d}t}(1-2t),\,\frac{\text{d}}{\text{d}t}({t}^{3})⟩ \\  & =⟨1,\,-2,\,3{t}^{2}⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨-2,\,2t,\,2t-2⟩+⟨1,\,-2,\,3{t}^{2}⟩ \\  & =⟨-1,\,2t-2,\,3{t}^{2}+2t-2⟩.\end{aligned}
$$

### q-128144

Find the value of $(f(t)-2g(t))^{′}$ at $t=1,$ if 

$$
\begin{aligned}f(t) & =⟨{t}^{2},\,\operatorname{ln}⁡t,\,{e}^{t-1}⟩, \\ g(t) & =⟨2\sqrt{t},\,{t}^{3},\,3⟩.\end{aligned}
$$

Observed field: one `selection` radio with five delimiter-free math answer values.

Observed worked solution:

First, notice that

$$
(f(t)-2g(t))^{′}={f}^{′}(t)-2{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t),\,\frac{\text{d}}{\text{d}t}({e}^{t-1})⟩ \\  & =⟨2t,\,\frac{1}{t},\,{e}^{t-1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2\sqrt{t}),\,\frac{\text{d}}{\text{d}t}({t}^{3}),\,\frac{\text{d}}{\text{d}t}(3)⟩ \\  & =⟨\frac{1}{\sqrt{t}},\,3{t}^{2},\,0⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(1)-2g(1))^{′} & ={f}^{′}(1)-2{g}^{′}(1) \\  & =⟨2(1),\,\frac{1}{1},\,{e}^{1-1}⟩-2⟨\frac{1}{\sqrt{1}},\,3(1)^{2},\,0⟩ \\  & =⟨2,1,1⟩-2⟨1,3,0⟩ \\  & =⟨2,1,1⟩-⟨2,6,0⟩ \\  & =⟨0,-5,1⟩.\end{aligned}
$$

## 2. Shared mathematical pattern

Differentiate a constant linear combination of vector-valued functions componentwise, then distribute constant multipliers and add/subtract corresponding components. Easy requests the derivative function; moderate requests its value at a fixed familiar input. The tuple/basis/column layouts and the original prose/solution row sequences are retained as distinct templates. No distractor-specific explanations are inserted in learner content.

## 3. Component and complete-bank map

Let U and V denote the componentwise derivatives of the first and second source functions (at the stated input for evaluated questions), C their required constant combination, and D=diag(s_x,s_y,s_z). In each observed profile the exact generalized recipe for **every full option** is D applied componentwise to the expression printed below. Inputs, formal derivative operands, derivative rows and every distributed/simplified vector receive the same D. This is a natural linear transformation commuting with differentiation. It is not a polynomial fit to isolated scalar answers. The interpretations below record supported operations; compound intent is only asserted when supported. Residual patterns remain explicit replay profiles. Normal defaults use a separately authored complete operation bank, not these residual patterns.

### Bank q-33122

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨2t+3,\,-2t-1,\,0⟩$ | C with both z contributions omitted | $D$ times this complete vector |

| $⟨2t,\,-2t,\,0⟩$ | G prime with z set to 0: omit F prime and the linear z derivative | $D$ times this complete vector |

| $⟨2t+3,\,-2t-1,\,8⟩$ | C (correct) | $D$ times this complete vector |

| $⟨2t+3,\,2t+1,\,8t⟩$ | C_x, -C_y, t C_z: y sign reversed and linear z power retained | $D$ times this complete vector |

| $⟨t+3,\,-t-1,\,8⟩$ | Half the quadratic derivative terms in x,y; preserve linear terms and correct z | $D$ times this complete vector |

### Bank q-33143

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨8, 1,-12⟩$ | U_x,U_y,C_z: omit outer factors/other-vector contribution in first two components | $D$ times this complete vector |

| $⟨12, 0, 48⟩$ | 2V: omit U, reverse subtraction sign | $D$ times this complete vector |

| $⟨24, 3, 36⟩$ | 3U: omit V | $D$ times this complete vector |

| $⟨6, 0, 24⟩$ | V: omit U and outer factor | $D$ times this complete vector |

| $⟨12, 3,-12⟩$ | C (independently inferred correct; missing designation) | $D$ times this complete vector |

### Bank q-128137

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨2,-1,-2⟩$ | C with y=-V_y rather than -3V_y | $D$ times this complete vector |

| $⟨2,1,-2⟩$ | C with y=V_y: omit multiplier and reverse sign | $D$ times this complete vector |

| $⟨2,-3,-2⟩$ | C (correct) | $D$ times this complete vector |

| $⟨1,-1,0⟩$ | (U_x,-V_y,U_z-V_z): x omit V, y omit multiplier, z omit multiplier | $D$ times this complete vector |

| $⟨0,-1,-2⟩$ | (U_x+3V_x,-V_y,C_z): x reverse sign, y omit multiplier | $D$ times this complete vector |

### Bank q-128452

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨-1,0,-2⟩$ | C_x,C_y,2U_z: omit V_z | $D$ times this complete vector |

| $⟨1,1,-4⟩$ | (-C_x,1,C_z): first sign flip; literal middle 1 has residual uncertain intent | $D$ times this complete vector |

| $⟨-1,0,-4⟩$ | C (correct) | $D$ times this complete vector |

| $⟨-1,\pi ,-4⟩$ | C_x,-U_y,C_z: middle omit outer factor and other vector, reverse sign | $D$ times this complete vector |

| $⟨-1,4\pi ,1⟩$ | C_x,-2U_y-V_y,-U_z: component-specific sign/multiplier/omission compound | $D$ times this complete vector |

### Bank q-128458

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $[\begin{aligned}-5 \\ -15 \\ 20\end{aligned}]$ | (-5,-15,5V_z): exact first two scalar patterns have residual uncertain intent | $D$ times this complete vector |

| $[\begin{aligned}10 \\ 5 \\ 10\end{aligned}]$ | (5V_x,(5/2)V_y,(5/2)V_z): omit U, half last two scales | $D$ times this complete vector |

| $[\begin{aligned}1 \\ 5 \\ 10\end{aligned}]$ | (2U_x,(5/2)V_y,(5/2)V_z): omit V_x, half last two scales | $D$ times this complete vector |

| $[\begin{aligned}11 \\ 10 \\ 20\end{aligned}]$ | C (correct) | $D$ times this complete vector |

| $[\begin{aligned}5 \\ 10 \\ 20\end{aligned}]$ | (5,5V_y,5V_z): first derivative of linear component treated as 1 and U_x omitted | $D$ times this complete vector |

### Bank q-32499

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨-2\operatorname{sin}⁡t-\operatorname{cos}⁡t,\,7,\,-4t⟩$ | C (correct) | $D$ times this complete vector |

| $⟨\operatorname{cos}⁡t,\,-1,\,0⟩$ | H prime only: omit G and outer/sign factors | $D$ times this complete vector |

| $⟨-2\operatorname{cos}⁡t,\,7,\,4t⟩$ | (-2 cos t,C_y,-C_z): altered trig derivative, omit H_x, reverse quadratic derivative sign | $D$ times this complete vector |

| $⟨-\operatorname{sin}⁡t,\,3,\,-2t⟩$ | G prime only: omit H and outer factor | $D$ times this complete vector |

| $⟨-2\operatorname{sin}⁡t,\,6,\,-4t⟩$ | 2G prime: omit H | $D$ times this complete vector |

### Bank q-32503

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨-2t-1,0,2t+1⟩$ | C (correct) | $D$ times this complete vector |

| $⟨-2t,0,2t⟩$ | H prime: omit linear derivative | $D$ times this complete vector |

| $⟨-1,0,1⟩$ | G prime: omit quadratic derivative | $D$ times this complete vector |

| $⟨t-1,0,t+1⟩$ | (t-1,0,t+1): quadratic derivatives lose factor 2 and x sign | $D$ times this complete vector |

| $⟨2t+1,2t+1,2t+1⟩$ | Broadcast C_z to all three components (including zero coordinate) | $D$ times this complete vector |

### Bank q-33123

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $2\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$ | 2F prime with first coefficient halved and j sign reversed (compound) | $D$ times this complete vector |

| $4\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$ | 2F prime: omit G | $D$ times this complete vector |

| $2\operatorname{cos}⁡t\,i-3\operatorname{sin}⁡t\,j+3\operatorname{sin}⁡t\,k$ | F prime: omit G and outer factor | $D$ times this complete vector |

| $-\operatorname{cos}⁡ti-2\operatorname{sin}⁡t\,k$ | G prime: omit F and outer factor | $D$ times this complete vector |

| $\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j$ | C (correct) | $D$ times this complete vector |

### Bank q-70681

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨\frac{1+\sqrt{t}}{\sqrt{t}},\,\frac{1}{t},\,16{t}^{4}⟩$ | (1/sqrt(t)+1,1/t,16t^4): first component derivative/factor compound, omit reciprocal contribution, retain power; exact compound intent uncertain | $D$ times this complete vector |

| $⟨2\sqrt{t},\,\frac{{t}^{2}+1}{t},\,2{t}^{4}⟩$ | (2sqrt(t),t+1/t,2t^4): component expression pattern; no coherent single derivative operation recovered | $D$ times this complete vector |

| $⟨4\sqrt{t},\,\frac{1}{{t}^{2}},\,8t⟩$ | (4sqrt(t),1/t^2,8t): component expression pattern; exact compound intent uncertain | $D$ times this complete vector |

| $⟨\frac{4}{\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,4{t}^{3}⟩$ | (4/sqrt(t),C_y,4t^3): altered square-root coefficient and omit constant derivative contribution; omit outer power-component factor | $D$ times this complete vector |

| $⟨\frac{1+8\sqrt{t}}{2\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,16{t}^{3}⟩$ | C (correct) | $D$ times this complete vector |

### Bank q-127998

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨-2,\,-2t,\,2t-2⟩$ | (F prime_x,-F prime_y,F prime_z): omit G and reverse y sign | $D$ times this complete vector |

| $⟨-1,\,2t,\,{t}^{2}⟩$ | (C_x,F prime_y,t^2): omit G_y, omit F_z, lose cubic derivative coefficient | $D$ times this complete vector |

| $⟨-3,\,2t+1,\,3{t}^{2}+2t⟩$ | (F prime_x-G prime_x,2t+1,3t^2+2t): first subtraction, middle altered linear derivative, shifted quadratic derivative loses constant | $D$ times this complete vector |

| $⟨-1,\,2t-2,\,3{t}^{2}⟩$ | (C_x,C_y,G prime_z): omit F_z | $D$ times this complete vector |

| $⟨-1,\,2t-2,\,3{t}^{2}+2t-2⟩$ | C (correct) | $D$ times this complete vector |

### Bank q-128144

| Source option (full value) | Supported structural interpretation / residual uncertainty | Generalized recipe |

|---|---|---|

| $⟨0,-7,0⟩$ | (C_x,-U_y-2V_y,0): y sign error, exponential derivative omitted | $D$ times this complete vector |

| $⟨-2,-5,0⟩$ | (-2V_x,C_y,0): omit first-vector x and exponential derivative | $D$ times this complete vector |

| $⟨2,7,0⟩$ | (U_x,U_y+2V_y,0): omit V_x, reverse subtraction y, exponential omitted | $D$ times this complete vector |

| $⟨4,7,9⟩$ | (U_x+2V_x,U_y+2V_y,9): reverse subtraction; literal z=9 intent residual uncertain | $D$ times this complete vector |

| $⟨0,-5,1⟩$ | C (correct) | $D$ times this complete vector |

## 4. Reusable slots, bounds and calculations

`templates.json` stores fixed prose and whole-vector/basis-expression slots. `extract.py` compiles the captured source into these masks; `render_slots` renders each complete component with the signed scale. Identity scales preserve the original component notation. Every non-identity instance evaluates exactly the same operations with altered signed coefficients. No short-expression/global number replacement is used. `BASES` supplies independently transcribed mathematical functions; differentiation computes the correct value, and the correct choice is identified by complete mathematical equivalence, not a stored answer index.

The source profiles are selected explicitly before construction. They preserve all five original values, layout, answer count, original sentences and all distributed solution stages. Whole-instance rejection applies if any complete options collide. Normal complete authored banks are [correct, omit first derivative, omit last derivative, reverse first multiplier, combine without differentiating]. The constant/linear/quadratic triple-sum source instead uses the fixed complete bank [correct, omit middle derivative, omit last derivative, reverse middle multiplier, combine without differentiating], because its first vector is constant. The bank is never assembled from first-valid pooled errors.

Scales are signed integers ±1..3, except the explicitly authored narrow triple-sum default permits x,z ±1..6 and fixes y=1. Both are constrained by the API as well as the sampler. General source families have 216 meaningful diagonal variants, the expanded triple-sum default has 144, and hard has 27,648 bounded parameter tuples before whole-bank rejection. Moderate evaluation points stay fixed to preserve perfect-square roots and familiar angles. Hard bounds and scope rationale are in `classification.md`; hard follows one fixed worked sequence across all samples.

### Source anomalies and supported repairs

- q-33143: inspected `/home/jake/Developer/MA/DATA/Lessons/1738/Source/1738.json` and its `03-question-33143.png`. Copied authoritative widget to `original-widget-33143.json`. Widget confirms tuple functions, five choices, no observed correct designation or solution. Derivation: h prime(2)=(8,1,12), g prime(2)=(6,0,24), hence 3h prime(2)-2g prime(2)=(12,3,-12). Repair capture `|=` into `=`. Assign moderate and add worked solution as authored; do not count missing designation as matched.

- q-128452: ln(2t) at t=-1 is not real. Raw EDB remains unchanged. Generated source replay and normal variants use ln(-2t), retaining derivative 1/t, every answer value, and all subsequent solution stages. Exact prompt fidelity excludes this repaired record; its worked solution also receives the evaluated-derivative notation repair below. Mathematical bank fidelity includes it. This is a minimal real-domain correction, not a claim that the original was mathematically valid.

- All four rated evaluated solutions: repair the source shorthand derivative of an already-evaluated constant combination to the derivative function evaluated at the input, e.g. (f(t)-3g(t)) prime evaluated at t=0. Preserve every RHS row, prose sentence and row count. This overlaps the q-128452 domain repair: four repaired solutions out of ten available; six remain exact. The missing q-33143 solution is authored separately.

- Some legacy choice strings double-escape thin-space backslashes. Identity replay preserves their full original strings; the independent mathematical reader treats them as spacing only.