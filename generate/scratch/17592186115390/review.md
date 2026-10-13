# Originals and generated variants

Raw snapshot: `source.json`, math basis 1356. All generated items below are labeled.

## Original q-33122

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨3t-1,\,6-t,\,7t⟩ \\ g(t) & =⟨{t}^{2},\,1-{t}^{2},\,t⟩\end{aligned}
$$

- $⟨2t+3,\,-2t-1,\,0⟩$
- $⟨2t,\,-2t,\,0⟩$
- $⟨2t+3,\,-2t-1,\,8⟩$
- $⟨2t+3,\,2t+1,\,8t⟩$
- $⟨t+3,\,-t-1,\,8⟩$

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

## Replay (repairs explicitly recorded)

## q-33122 — easy
Profile: `q-33122`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨3t-1,\,6-t,\,7t⟩ \\ g(t) & =⟨{t}^{2},\,1-{t}^{2},\,t⟩\end{aligned}
$$

- $⟨2t+3,\,-2t-1,\,8⟩$ **correct**
- $⟨2t,\,-2t,\,0⟩$
- $⟨2t+3,\,-2t-1,\,0⟩$
- $⟨t+3,\,-t-1,\,8⟩$
- $⟨2t+3,\,2t+1,\,8t⟩$

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

## Original q-33143

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)|= ⟨2t^{2}, t - 3, 8 + t^{3}⟩; g(t)|= ⟨t^{2} + 2t, 8, 2t^{3}⟩$

- $⟨8, 1,-12⟩$
- $⟨12, 0, 48⟩$
- $⟨24, 3, 36⟩$
- $⟨6, 0, 24⟩$
- $⟨12, 3,-12⟩$

No captured worked solution.

## Replay (repairs explicitly recorded)

## q-33143 — moderate
Profile: `q-33143`; parameters: `{"scales": [1, 1, 1]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨2t^{2}, t - 3, 8 + t^{3}⟩; g(t)= ⟨t^{2} + 2t, 8, 2t^{3}⟩$

- $⟨24, 3, 36⟩$
- $⟨12, 0, 48⟩$
- $⟨8, 1,-12⟩$
- $⟨12, 3,-12⟩$ **correct**
- $⟨6, 0, 24⟩$

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 3),\,\frac{\text{d}}{\text{d}t}(t^{3} + 8)⟩ \\ &=⟨4 t,\,1,\,3 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(8),\,\frac{\text{d}}{\text{d}t}(2 t^{3})⟩ \\ &=⟨2 t + 2,\,0,\,6 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨8,\,1,\,12⟩\right)-2\left(⟨6,\,0,\,24⟩\right) \\ &=\left(⟨24,\,3,\,36⟩\right)+\left(⟨-12,\,0,\,-48⟩\right) \\ &=⟨12,\,3,\,-12⟩.\end{aligned}
$$

## Original q-128137

Find the value of $(f(t)-3g(t))^{′}$ at $t=0,$ if 

$$
\begin{aligned}f(t) & =⟨2\sqrt{t+1},\,{t}^{3},\,\operatorname{ln}⁡(t+1)⟩, \\ g(t) & =⟨\frac{1}{3(t+1)},\,\operatorname{sin}⁡t,\,\operatorname{tan}⁡t⟩.\end{aligned}
$$

- $⟨2,-1,-2⟩$
- $⟨2,1,-2⟩$
- $⟨2,-3,-2⟩$
- $⟨1,-1,0⟩$
- $⟨0,-1,-2⟩$

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

## Replay (repairs explicitly recorded)

## q-128137 — moderate
Profile: `q-128137`; parameters: `{"scales": [1, 1, 1]}`.

Find the value of $(f(t)-3g(t))^{′}$ at $t=0,$ if 

$$
\begin{aligned}f(t) & =⟨2\sqrt{t+1},\,{t}^{3},\,\operatorname{ln}⁡(t+1)⟩, \\ g(t) & =⟨\frac{1}{3(t+1)},\,\operatorname{sin}⁡t,\,\operatorname{tan}⁡t⟩.\end{aligned}
$$

- $⟨2,-3,-2⟩$ **correct**
- $⟨2,1,-2⟩$
- $⟨2,-1,-2⟩$
- $⟨0,-1,-2⟩$
- $⟨1,-1,0⟩$

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
\begin{aligned}(f(t)-3g(t))^{′}\big|_{t=0} & ={f}^{′}(0)-3{g}^{′}(0) \\  & =⟨\frac{1}{\sqrt{0+1}},\,3(0)^{2},\,\frac{1}{0+1}⟩-3⟨-\frac{1}{3(0+1)^{2}},\,\operatorname{cos}⁡0,\,{sec}^{2}⁡0⟩ \\  & =⟨1,0,1⟩-3⟨-\frac{1}{3},1,1⟩ \\  & =⟨1,0,1⟩-⟨-1,3,3⟩ \\  & =⟨2,-3,-2⟩.\end{aligned}
$$

## Original q-128452

Find the value of $(2f(t)-g(t))^{′}$ at $t=-1,$ if 

$$
\begin{aligned}f(t) & =⟨8\sqrt{3-t},\,\operatorname{sin}⁡(\pi t),\,\operatorname{ln}⁡(2t)⟩, \\ g(t) & =⟨{t}^{2}-t,\,\pi {t}^{2},\,1-{t}^{2}⟩.\end{aligned}
$$

- $⟨-1,0,-2⟩$
- $⟨1,1,-4⟩$
- $⟨-1,0,-4⟩$
- $⟨-1,\pi ,-4⟩$
- $⟨-1,4\pi ,1⟩$

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

## Replay (repairs explicitly recorded)

## q-128452 — moderate
Profile: `q-128452`; parameters: `{"scales": [1, 1, 1]}`.

Find the value of $(2f(t)-g(t))^{′}$ at $t=-1,$ if 

$$
\begin{aligned}f(t) & =⟨8\sqrt{3-t},\,\operatorname{sin}⁡(\pi t),\,\operatorname{ln}⁡(-2t)⟩, \\ g(t) & =⟨{t}^{2}-t,\,\pi {t}^{2},\,1-{t}^{2}⟩.\end{aligned}
$$

- $⟨-1,0,-4⟩$ **correct**
- $⟨1,1,-4⟩$
- $⟨-1,0,-2⟩$
- $⟨-1,4\pi ,1⟩$
- $⟨-1,\pi ,-4⟩$

First, notice that

$$
(2f(t)-g(t))^{′}=2{f}^{′}(t)-{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(8\sqrt{3-t}),\,\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t)),\,\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡(-2t))⟩ \\  & =⟨-\frac{4}{\sqrt{3-t}},\,\pi \operatorname{cos}⁡(\pi t),\,\frac{1}{t}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}-t),\,\frac{\text{d}}{\text{d}t}(\pi {t}^{2}),\,\frac{\text{d}}{\text{d}t}(1-{t}^{2})⟩ \\  & =⟨2t-1,\,2\pi t,\,-2t⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(2f(t)-g(t))^{′}\big|_{t=-1} & =2{f}^{′}(-1)-{g}^{′}(-1) \\  & =2⟨-\frac{4}{\sqrt{3-(-1)}},\,\pi \operatorname{cos}⁡(-\pi ),\,\frac{1}{(-1)}⟩-⟨2(-1)-1,\,2\pi (-1),\,-2(-1)⟩ \\  & =2⟨-2,-\pi ,-1⟩-⟨-3,-2\pi ,2⟩ \\  & =⟨-4,-2\pi ,-2⟩-⟨-3,-2\pi ,2⟩ \\  & =⟨-1,0,-4⟩.\end{aligned}
$$

## Original q-128458

Find the value of $(2f(t)+5g(t))^{′}$ at $t=1,$ where

$$
\begin{aligned}f(t)=[\begin{aligned}2\sqrt{3+t} \\ \operatorname{cos}⁡(t-1) \\ 1\end{aligned}],\,g(t)=[\begin{aligned}2t-3 \\ {t}^{2} \\ (t+1)^{2}\end{aligned}]\end{aligned}
$$

- $[\begin{aligned}-5 \\ -15 \\ 20\end{aligned}]$
- $[\begin{aligned}10 \\ 5 \\ 10\end{aligned}]$
- $[\begin{aligned}1 \\ 5 \\ 10\end{aligned}]$
- $[\begin{aligned}11 \\ 10 \\ 20\end{aligned}]$
- $[\begin{aligned}5 \\ 10 \\ 20\end{aligned}]$

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

## Replay (repairs explicitly recorded)

## q-128458 — moderate
Profile: `q-128458`; parameters: `{"scales": [1, 1, 1]}`.

Find the value of $(2f(t)+5g(t))^{′}$ at $t=1,$ where

$$
\begin{aligned}f(t)=[\begin{aligned}2\sqrt{3+t} \\ \operatorname{cos}⁡(t-1) \\ 1\end{aligned}],\,g(t)=[\begin{aligned}2t-3 \\ {t}^{2} \\ (t+1)^{2}\end{aligned}]\end{aligned}
$$

- $[\begin{aligned}1 \\ 5 \\ 10\end{aligned}]$
- $[\begin{aligned}10 \\ 5 \\ 10\end{aligned}]$
- $[\begin{aligned}-5 \\ -15 \\ 20\end{aligned}]$
- $[\begin{aligned}5 \\ 10 \\ 20\end{aligned}]$
- $[\begin{aligned}11 \\ 10 \\ 20\end{aligned}]$ **correct**

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
\begin{aligned}(2f(t)+5g(t))^{′}\big|_{t=1} & =2{f}^{′}(1)+5{g}^{′}(1) \\  & =2[\begin{aligned}\frac{1}{\sqrt{3+1}} \\ -\operatorname{sin}⁡(1-1) \\ 0\end{aligned}]+5[\begin{aligned}2 \\ 2(1) \\ 2(1+1)\end{aligned}] \\  & =2[\begin{aligned}\frac{1}{2} \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}2 \\ 2 \\ 4\end{aligned}] \\  & =[\begin{aligned}1 \\ 0 \\ 0\end{aligned}]+[\begin{aligned}10 \\ 10 \\ 20\end{aligned}] \\  & =[\begin{aligned}11 \\ 10 \\ 20\end{aligned}].\end{aligned}
$$

## Original q-32499

Differentiate $2g(t)-h(t)$ with respect to $t$, where

$$
\begin{aligned}g(t) & =⟨\operatorname{cos}⁡t,\,3t-3,\,-{t}^{2}⟩ \\ h(t) & =⟨\operatorname{sin}⁡t,\,-t,\,4⟩\end{aligned}
$$

- $⟨-2\operatorname{sin}⁡t-\operatorname{cos}⁡t,\,7,\,-4t⟩$
- $⟨\operatorname{cos}⁡t,\,-1,\,0⟩$
- $⟨-2\operatorname{cos}⁡t,\,7,\,4t⟩$
- $⟨-\operatorname{sin}⁡t,\,3,\,-2t⟩$
- $⟨-2\operatorname{sin}⁡t,\,6,\,-4t⟩$

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

## Replay (repairs explicitly recorded)

## q-32499 — easy
Profile: `q-32499`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $2g(t)-h(t)$ with respect to $t$, where

$$
\begin{aligned}g(t) & =⟨\operatorname{cos}⁡t,\,3t-3,\,-{t}^{2}⟩ \\ h(t) & =⟨\operatorname{sin}⁡t,\,-t,\,4⟩\end{aligned}
$$

- $⟨-2\operatorname{cos}⁡t,\,7,\,4t⟩$
- $⟨\operatorname{cos}⁡t,\,-1,\,0⟩$
- $⟨-2\operatorname{sin}⁡t-\operatorname{cos}⁡t,\,7,\,-4t⟩$ **correct**
- $⟨-2\operatorname{sin}⁡t,\,6,\,-4t⟩$
- $⟨-\operatorname{sin}⁡t,\,3,\,-2t⟩$

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

## Original q-32503

Differentiate $f(t)+g(t)+h(t)$ with respect to $t$, where

$$
\begin{aligned}f(t) & =⟨-1,\,0,\,1⟩ \\ g(t) & =⟨-t,\,0,t⟩ \\ h(t) & =⟨-{t}^{2},0,{t}^{2}⟩\end{aligned}
$$

- $⟨-2t-1,0,2t+1⟩$
- $⟨-2t,0,2t⟩$
- $⟨-1,0,1⟩$
- $⟨t-1,0,t+1⟩$
- $⟨2t+1,2t+1,2t+1⟩$

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

## Replay (repairs explicitly recorded)

## q-32503 — easy
Profile: `q-32503`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $f(t)+g(t)+h(t)$ with respect to $t$, where

$$
\begin{aligned}f(t) & =⟨-1,\,0,\,1⟩ \\ g(t) & =⟨-t,\,0,t⟩ \\ h(t) & =⟨-{t}^{2},0,{t}^{2}⟩\end{aligned}
$$

- $⟨-1,0,1⟩$
- $⟨-2t,0,2t⟩$
- $⟨-2t-1,0,2t+1⟩$ **correct**
- $⟨2t+1,2t+1,2t+1⟩$
- $⟨t-1,0,t+1⟩$

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

## Original q-33123

Differentiate $2f(t)+3g(t)$ with respect to $t$, where

 

$$
\begin{aligned}f(t) & =2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,(j-\,k) \\ g(t) & =(5-\operatorname{sin}⁡t)\,i-\,j+2\operatorname{cos}⁡t\,k\end{aligned}
$$

- $2\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$
- $4\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$
- $2\operatorname{cos}⁡t\,i-3\operatorname{sin}⁡t\,j+3\operatorname{sin}⁡t\,k$
- $-\operatorname{cos}⁡ti-2\operatorname{sin}⁡t\,k$
- $\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j$

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

## Replay (repairs explicitly recorded)

## q-33123 — easy
Profile: `q-33123`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $2f(t)+3g(t)$ with respect to $t$, where

 

$$
\begin{aligned}f(t) & =2\operatorname{sin}⁡t\,i+3\operatorname{cos}⁡t\,(j-\,k) \\ g(t) & =(5-\operatorname{sin}⁡t)\,i-\,j+2\operatorname{cos}⁡t\,k\end{aligned}
$$

- $2\operatorname{cos}⁡t\,i-3\operatorname{sin}⁡t\,j+3\operatorname{sin}⁡t\,k$
- $4\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$
- $2\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j+6\operatorname{sin}⁡t\,k$
- $\operatorname{cos}⁡t\,i-6\operatorname{sin}⁡t\,j$ **correct**
- $-\operatorname{cos}⁡ti-2\operatorname{sin}⁡t\,k$

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

## Original q-70681

Differentiate $f(t)+4g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨\sqrt{t},\,\operatorname{ln}⁡t,\,2⟩ \\ g(t) & =⟨t,\,\frac{1}{t},\,{t}^{4}⟩\end{aligned}
$$

- $⟨\frac{1+\sqrt{t}}{\sqrt{t}},\,\frac{1}{t},\,16{t}^{4}⟩$
- $⟨2\sqrt{t},\,\frac{{t}^{2}+1}{t},\,2{t}^{4}⟩$
- $⟨4\sqrt{t},\,\frac{1}{{t}^{2}},\,8t⟩$
- $⟨\frac{4}{\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,4{t}^{3}⟩$
- $⟨\frac{1+8\sqrt{t}}{2\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,16{t}^{3}⟩$

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

## Replay (repairs explicitly recorded)

## q-70681 — easy
Profile: `q-70681`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $f(t)+4g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨\sqrt{t},\,\operatorname{ln}⁡t,\,2⟩ \\ g(t) & =⟨t,\,\frac{1}{t},\,{t}^{4}⟩\end{aligned}
$$

- $⟨4\sqrt{t},\,\frac{1}{{t}^{2}},\,8t⟩$
- $⟨2\sqrt{t},\,\frac{{t}^{2}+1}{t},\,2{t}^{4}⟩$
- $⟨\frac{1+\sqrt{t}}{\sqrt{t}},\,\frac{1}{t},\,16{t}^{4}⟩$
- $⟨\frac{1+8\sqrt{t}}{2\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,16{t}^{3}⟩$ **correct**
- $⟨\frac{4}{\sqrt{t}},\,\frac{t-4}{{t}^{2}},\,4{t}^{3}⟩$

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

## Original q-127998

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨1-2t,\,{t}^{2},\,(t-1)^{2}⟩, \\ g(t) & =⟨t+1,\,1-2t,\,{t}^{3}⟩\end{aligned}
$$

- $⟨-2,\,-2t,\,2t-2⟩$
- $⟨-1,\,2t,\,{t}^{2}⟩$
- $⟨-3,\,2t+1,\,3{t}^{2}+2t⟩$
- $⟨-1,\,2t-2,\,3{t}^{2}⟩$
- $⟨-1,\,2t-2,\,3{t}^{2}+2t-2⟩$

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

## Replay (repairs explicitly recorded)

## q-127998 — easy
Profile: `q-127998`; parameters: `{"scales": [1, 1, 1]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨1-2t,\,{t}^{2},\,(t-1)^{2}⟩, \\ g(t) & =⟨t+1,\,1-2t,\,{t}^{3}⟩\end{aligned}
$$

- $⟨-3,\,2t+1,\,3{t}^{2}+2t⟩$
- $⟨-1,\,2t,\,{t}^{2}⟩$
- $⟨-2,\,-2t,\,2t-2⟩$
- $⟨-1,\,2t-2,\,3{t}^{2}+2t-2⟩$ **correct**
- $⟨-1,\,2t-2,\,3{t}^{2}⟩$

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

## Original q-128144

Find the value of $(f(t)-2g(t))^{′}$ at $t=1,$ if 

$$
\begin{aligned}f(t) & =⟨{t}^{2},\,\operatorname{ln}⁡t,\,{e}^{t-1}⟩, \\ g(t) & =⟨2\sqrt{t},\,{t}^{3},\,3⟩.\end{aligned}
$$

- $⟨0,-7,0⟩$
- $⟨-2,-5,0⟩$
- $⟨2,7,0⟩$
- $⟨4,7,9⟩$
- $⟨0,-5,1⟩$

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

## Replay (repairs explicitly recorded)

## q-128144 — moderate
Profile: `q-128144`; parameters: `{"scales": [1, 1, 1]}`.

Find the value of $(f(t)-2g(t))^{′}$ at $t=1,$ if 

$$
\begin{aligned}f(t) & =⟨{t}^{2},\,\operatorname{ln}⁡t,\,{e}^{t-1}⟩, \\ g(t) & =⟨2\sqrt{t},\,{t}^{3},\,3⟩.\end{aligned}
$$

- $⟨2,7,0⟩$
- $⟨-2,-5,0⟩$
- $⟨0,-7,0⟩$
- $⟨0,-5,1⟩$ **correct**
- $⟨4,7,9⟩$

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
\begin{aligned}(f(t)-2g(t))^{′}\big|_{t=1} & ={f}^{′}(1)-2{g}^{′}(1) \\  & =⟨2(1),\,\frac{1}{1},\,{e}^{1-1}⟩-2⟨\frac{1}{\sqrt{1}},\,3(1)^{2},\,0⟩ \\  & =⟨2,1,1⟩-2⟨1,3,0⟩ \\  & =⟨2,1,1⟩-⟨2,6,0⟩ \\  & =⟨0,-5,1⟩.\end{aligned}
$$

# Generated variants (observed profiles and authored defaults)

## q-33122 — easy
Profile: `q-33122`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨2 - 6 t,\,6 - t,\,21 t⟩ \\ g(t) & =⟨- 2 t^{2},\,1 - t^{2},\,3 t⟩\end{aligned}
$$

- $⟨- 4 t - 6,\,- 2 t - 1,\,24⟩$ **correct**
- $⟨- 4 t - 6,\,2 t + 1,\,24 t⟩$
- $⟨- 2 t - 6,\,- t - 1,\,24⟩$
- $⟨- 4 t - 6,\,- 2 t - 1,\,0⟩$
- $⟨- 4 t,\,- 2 t,\,0⟩$

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 - 6 t),\,\frac{\text{d}}{\text{d}t}(6 - t),\,\frac{\text{d}}{\text{d}t}(21 t)⟩ \\  & =⟨-6,\,-1,\,21⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 t^{2}),\,\frac{\text{d}}{\text{d}t}(1 - t^{2}),\,\frac{\text{d}}{\text{d}t}(3 t)⟩ \\  & =⟨- 4 t,\,- 2 t,\,3⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨-6,\,-1,\,21⟩+⟨- 4 t,\,- 2 t,\,3⟩ \\  & =⟨- 4 t - 6,\,- 2 t - 1,\,24⟩\end{aligned}
$$

## q-33122 — easy
Profile: `q-33122`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨3 t - 1,\,3 t - 18,\,14 t⟩ \\ g(t) & =⟨t^{2},\,3 t^{2} - 3,\,2 t⟩\end{aligned}
$$

- $⟨2 t + 3,\,6 t + 3,\,16⟩$ **correct**
- $⟨2 t,\,6 t,\,0⟩$
- $⟨2 t + 3,\,- 6 t - 3,\,16 t⟩$
- $⟨t + 3,\,3 t + 3,\,16⟩$
- $⟨2 t + 3,\,6 t + 3,\,0⟩$

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t - 1),\,\frac{\text{d}}{\text{d}t}(3 t - 18),\,\frac{\text{d}}{\text{d}t}(14 t)⟩ \\  & =⟨3,\,3,\,14⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\,\frac{\text{d}}{\text{d}t}(3 t^{2} - 3),\,\frac{\text{d}}{\text{d}t}(2 t)⟩ \\  & =⟨2 t,\,6 t,\,2⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨3,\,3,\,14⟩+⟨2 t,\,6 t,\,2⟩ \\  & =⟨2 t + 3,\,6 t + 3,\,16⟩\end{aligned}
$$

## q-33143 — moderate
Profile: `q-33143`; parameters: `{"scales": [-2, 1, 3]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨- 4 t^{2},\,t - 3,\,3 t^{3} + 24⟩; g(t)= ⟨2 t \left(- t - 2\right),\,8,\,6 t^{3}⟩$

- $⟨-48,\,3,\,108⟩$
- $⟨-12,\,0,\,72⟩$
- $⟨-24,\,3,\,-36⟩$ **correct**
- $⟨-16,\,1,\,-36⟩$
- $⟨-24,\,0,\,144⟩$

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(- 4 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 3),\,\frac{\text{d}}{\text{d}t}(3 t^{3} + 24)⟩ \\ &=⟨- 8 t,\,1,\,9 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(- 2 t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(8),\,\frac{\text{d}}{\text{d}t}(6 t^{3})⟩ \\ &=⟨- 4 t - 4,\,0,\,18 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨-16,\,1,\,36⟩\right)-2\left(⟨-12,\,0,\,72⟩\right) \\ &=\left(⟨-48,\,3,\,108⟩\right)+\left(⟨24,\,0,\,-144⟩\right) \\ &=⟨-24,\,3,\,-36⟩.\end{aligned}
$$

## q-33143 — moderate
Profile: `q-33143`; parameters: `{"scales": [1, -3, 2]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨2 t^{2},\,9 - 3 t,\,2 t^{3} + 16⟩; g(t)= ⟨t \left(t + 2\right),\,-24,\,4 t^{3}⟩$

- $⟨24,\,-9,\,72⟩$
- $⟨12,\,0,\,96⟩$
- $⟨6,\,0,\,48⟩$
- $⟨12,\,-9,\,-24⟩$ **correct**
- $⟨8,\,-3,\,-24⟩$

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(9 - 3 t),\,\frac{\text{d}}{\text{d}t}(2 t^{3} + 16)⟩ \\ &=⟨4 t,\,-3,\,6 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(-24),\,\frac{\text{d}}{\text{d}t}(4 t^{3})⟩ \\ &=⟨2 t + 2,\,0,\,12 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨8,\,-3,\,24⟩\right)-2\left(⟨6,\,0,\,48⟩\right) \\ &=\left(⟨24,\,-9,\,72⟩\right)+\left(⟨-12,\,0,\,-96⟩\right) \\ &=⟨12,\,-9,\,-24⟩.\end{aligned}
$$

## q-128137 — moderate
Profile: `q-128137`; parameters: `{"scales": [-2, 1, 3]}`.

Find the value of $(f(t)-3g(t))^{′}$ at $t=0,$ if 

$$
\begin{aligned}f(t) & =⟨- 4 \sqrt{t + 1},\,t^{3},\,3 \log{\left(t + 1 \right)}⟩, \\ g(t) & =⟨- \frac{2}{3 t + 3},\,\sin{\left(t \right)},\,3 \tan{\left(t \right)}⟩.\end{aligned}
$$

- $⟨-4,\,-3,\,-6⟩$ **correct**
- $⟨-2,\,-1,\,0⟩$
- $⟨0,\,-1,\,-6⟩$
- $⟨-4,\,-1,\,-6⟩$
- $⟨-4,\,1,\,-6⟩$

First, notice that

$$
(f(t)-3g(t))^{′}={f}^{′}(t)-3{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 4 \sqrt{t + 1}),\,\frac{\text{d}}{\text{d}t}(t^{3}),\,\frac{\text{d}}{\text{d}t}(3 \log{\left(t + 1 \right)})⟩ \\  & =⟨- \frac{2}{\sqrt{t + 1}},\,3 t^{2},\,\frac{3}{t + 1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- \frac{2}{3 t + 3}),\,\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(3 \tan{\left(t \right)})⟩ \\  & =⟨\frac{2}{3 \left(t + 1\right)^{2}},\,\cos{\left(t \right)},\,3 \sec^{2}{\left(t \right)}⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)-3g(t))^{′}\big|_{t=0} & ={f}^{′}(0)-3{g}^{′}(0) \\  & =⟨-2,\,0,\,3⟩-3⟨\frac{2}{3},\,1,\,3⟩ \\  & =⟨-2,\,0,\,3⟩-3⟨\frac{2}{3},\,1,\,3⟩ \\  & =⟨-2,\,0,\,3⟩-⟨2,\,3,\,9⟩ \\  & =⟨-4,\,-3,\,-6⟩.\end{aligned}
$$

## q-128137 — moderate
Profile: `q-128137`; parameters: `{"scales": [1, -3, 2]}`.

Find the value of $(f(t)-3g(t))^{′}$ at $t=0,$ if 

$$
\begin{aligned}f(t) & =⟨2 \sqrt{t + 1},\,- 3 t^{3},\,2 \log{\left(t + 1 \right)}⟩, \\ g(t) & =⟨\frac{1}{3 \left(t + 1\right)},\,- 3 \sin{\left(t \right)},\,2 \tan{\left(t \right)}⟩.\end{aligned}
$$

- $⟨2,\,9,\,-4⟩$ **correct**
- $⟨2,\,-3,\,-4⟩$
- $⟨1,\,3,\,0⟩$
- $⟨0,\,3,\,-4⟩$
- $⟨2,\,3,\,-4⟩$

First, notice that

$$
(f(t)-3g(t))^{′}={f}^{′}(t)-3{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t + 1}),\,\frac{\text{d}}{\text{d}t}(- 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(2 \log{\left(t + 1 \right)})⟩ \\  & =⟨\frac{1}{\sqrt{t + 1}},\,- 9 t^{2},\,\frac{2}{t + 1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\frac{1}{3 \left(t + 1\right)}),\,\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(2 \tan{\left(t \right)})⟩ \\  & =⟨- \frac{1}{3 \left(t + 1\right)^{2}},\,- 3 \cos{\left(t \right)},\,2 \sec^{2}{\left(t \right)}⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)-3g(t))^{′}\big|_{t=0} & ={f}^{′}(0)-3{g}^{′}(0) \\  & =⟨1,\,0,\,2⟩-3⟨- \frac{1}{3},\,-3,\,2⟩ \\  & =⟨1,\,0,\,2⟩-3⟨- \frac{1}{3},\,-3,\,2⟩ \\  & =⟨1,\,0,\,2⟩-⟨-1,\,-9,\,6⟩ \\  & =⟨2,\,9,\,-4⟩.\end{aligned}
$$

## q-128452 — moderate
Profile: `q-128452`; parameters: `{"scales": [-2, 1, 3]}`.

Find the value of $(2f(t)-g(t))^{′}$ at $t=-1,$ if 

$$
\begin{aligned}f(t) & =⟨- 16 \sqrt{3 - t},\,\sin{\left(\pi t \right)},\,3 \log{\left(- 2 t \right)}⟩, \\ g(t) & =⟨2 t \left(1 - t\right),\,\pi t^{2},\,3 - 3 t^{2}⟩.\end{aligned}
$$

- $⟨2,\,0,\,-12⟩$ **correct**
- $⟨2,\,\pi,\,-12⟩$
- $⟨2,\,4 \pi,\,3⟩$
- $⟨2,\,0,\,-6⟩$
- $⟨-2,\,1,\,-12⟩$

First, notice that

$$
(2f(t)-g(t))^{′}=2{f}^{′}(t)-{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 16 \sqrt{3 - t}),\,\frac{\text{d}}{\text{d}t}(\sin{\left(\pi t \right)}),\,\frac{\text{d}}{\text{d}t}(3 \log{\left(- 2 t \right)})⟩ \\  & =⟨\frac{8}{\sqrt{3 - t}},\,\pi \cos{\left(\pi t \right)},\,\frac{3}{t}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t \left(1 - t\right)),\,\frac{\text{d}}{\text{d}t}(\pi t^{2}),\,\frac{\text{d}}{\text{d}t}(3 - 3 t^{2})⟩ \\  & =⟨2 - 4 t,\,2 \pi t,\,- 6 t⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(2f(t)-g(t))^{′}\big|_{t=-1} & =2{f}^{′}(-1)-{g}^{′}(-1) \\  & =2⟨4,\,- \pi,\,-3⟩-⟨6,\,- 2 \pi,\,6⟩ \\  & =2⟨4,\,- \pi,\,-3⟩-⟨6,\,- 2 \pi,\,6⟩ \\  & =⟨8,\,- 2 \pi,\,-6⟩-⟨6,\,- 2 \pi,\,6⟩ \\  & =⟨2,\,0,\,-12⟩.\end{aligned}
$$

## q-128452 — moderate
Profile: `q-128452`; parameters: `{"scales": [1, -3, 2]}`.

Find the value of $(2f(t)-g(t))^{′}$ at $t=-1,$ if 

$$
\begin{aligned}f(t) & =⟨8 \sqrt{3 - t},\,- 3 \sin{\left(\pi t \right)},\,2 \log{\left(- 2 t \right)}⟩, \\ g(t) & =⟨t \left(t - 1\right),\,- 3 \pi t^{2},\,2 - 2 t^{2}⟩.\end{aligned}
$$

- $⟨-1,\,0,\,-8⟩$ **correct**
- $⟨1,\,-3,\,-8⟩$
- $⟨-1,\,- 3 \pi,\,-8⟩$
- $⟨-1,\,- 12 \pi,\,2⟩$
- $⟨-1,\,0,\,-4⟩$

First, notice that

$$
(2f(t)-g(t))^{′}=2{f}^{′}(t)-{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(8 \sqrt{3 - t}),\,\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(\pi t \right)}),\,\frac{\text{d}}{\text{d}t}(2 \log{\left(- 2 t \right)})⟩ \\  & =⟨- \frac{4}{\sqrt{3 - t}},\,- 3 \pi \cos{\left(\pi t \right)},\,\frac{2}{t}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t \left(t - 1\right)),\,\frac{\text{d}}{\text{d}t}(- 3 \pi t^{2}),\,\frac{\text{d}}{\text{d}t}(2 - 2 t^{2})⟩ \\  & =⟨2 t - 1,\,- 6 \pi t,\,- 4 t⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(2f(t)-g(t))^{′}\big|_{t=-1} & =2{f}^{′}(-1)-{g}^{′}(-1) \\  & =2⟨-2,\,3 \pi,\,-2⟩-⟨-3,\,6 \pi,\,4⟩ \\  & =2⟨-2,\,3 \pi,\,-2⟩-⟨-3,\,6 \pi,\,4⟩ \\  & =⟨-4,\,6 \pi,\,-4⟩-⟨-3,\,6 \pi,\,4⟩ \\  & =⟨-1,\,0,\,-8⟩.\end{aligned}
$$

## q-128458 — moderate
Profile: `q-128458`; parameters: `{"scales": [-2, 1, 3]}`.

Find the value of $(2f(t)+5g(t))^{′}$ at $t=1,$ where

$$
\begin{aligned}f(t)=[\begin{aligned}- 4 \sqrt{t + 3} \\ \cos{\left(t - 1 \right)} \\ 3\end{aligned}],\,g(t)=[\begin{aligned}6 - 4 t \\ t^{2} \\ 3 \left(t + 1\right)^{2}\end{aligned}]\end{aligned}
$$

- $[\begin{aligned}-2 \\ 5 \\ 30\end{aligned}]$
- $[\begin{aligned}-22 \\ 10 \\ 60\end{aligned}]$ **correct**
- $[\begin{aligned}-10 \\ 10 \\ 60\end{aligned}]$
- $[\begin{aligned}10 \\ -15 \\ 60\end{aligned}]$
- $[\begin{aligned}-20 \\ 5 \\ 30\end{aligned}]$

By the sum rule, we have 
 

$$
(2f(t)+5g(t))^{′}=2{f}^{′}(t)+5{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 4 \sqrt{t + 3}) \\ \frac{\text{d}}{\text{d}t}(\cos{\left(t - 1 \right)}) \\ \frac{\text{d}}{\text{d}t}(3)\end{aligned}]=[\begin{aligned}- \frac{2}{\sqrt{t + 3}} \\ - \sin{\left(t - 1 \right)} \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(6 - 4 t) \\ \frac{\text{d}}{\text{d}t}(t^{2}) \\ \frac{\text{d}}{\text{d}t}(3 \left(t + 1\right)^{2})\end{aligned}]=[\begin{aligned}-4 \\ 2 t \\ 6 t + 6\end{aligned}]\end{aligned}
$$

Hence , we get

$$
\begin{aligned}(2f(t)+5g(t))^{′}\big|_{t=1} & =2{f}^{′}(1)+5{g}^{′}(1) \\  & =2[\begin{aligned}-1 \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}-4 \\ 2 \\ 12\end{aligned}] \\  & =2[\begin{aligned}-1 \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}-4 \\ 2 \\ 12\end{aligned}] \\  & =[\begin{aligned}-2 \\ 0 \\ 0\end{aligned}]+[\begin{aligned}-20 \\ 10 \\ 60\end{aligned}] \\  & =[\begin{aligned}-22 \\ 10 \\ 60\end{aligned}].\end{aligned}
$$

## q-128458 — moderate
Profile: `q-128458`; parameters: `{"scales": [1, -3, 2]}`.

Find the value of $(2f(t)+5g(t))^{′}$ at $t=1,$ where

$$
\begin{aligned}f(t)=[\begin{aligned}2 \sqrt{t + 3} \\ - 3 \cos{\left(t - 1 \right)} \\ 2\end{aligned}],\,g(t)=[\begin{aligned}2 t - 3 \\ - 3 t^{2} \\ 2 \left(t + 1\right)^{2}\end{aligned}]\end{aligned}
$$

- $[\begin{aligned}1 \\ -15 \\ 20\end{aligned}]$
- $[\begin{aligned}10 \\ -15 \\ 20\end{aligned}]$
- $[\begin{aligned}11 \\ -30 \\ 40\end{aligned}]$ **correct**
- $[\begin{aligned}5 \\ -30 \\ 40\end{aligned}]$
- $[\begin{aligned}-5 \\ 45 \\ 40\end{aligned}]$

By the sum rule, we have 
 

$$
(2f(t)+5g(t))^{′}=2{f}^{′}(t)+5{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \sqrt{t + 3}) \\ \frac{\text{d}}{\text{d}t}(- 3 \cos{\left(t - 1 \right)}) \\ \frac{\text{d}}{\text{d}t}(2)\end{aligned}]=[\begin{aligned}\frac{1}{\sqrt{t + 3}} \\ 3 \sin{\left(t - 1 \right)} \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t - 3) \\ \frac{\text{d}}{\text{d}t}(- 3 t^{2}) \\ \frac{\text{d}}{\text{d}t}(2 \left(t + 1\right)^{2})\end{aligned}]=[\begin{aligned}2 \\ - 6 t \\ 4 t + 4\end{aligned}]\end{aligned}
$$

Hence , we get

$$
\begin{aligned}(2f(t)+5g(t))^{′}\big|_{t=1} & =2{f}^{′}(1)+5{g}^{′}(1) \\  & =2[\begin{aligned}\frac{1}{2} \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}2 \\ -6 \\ 8\end{aligned}] \\  & =2[\begin{aligned}\frac{1}{2} \\ 0 \\ 0\end{aligned}]+5[\begin{aligned}2 \\ -6 \\ 8\end{aligned}] \\  & =[\begin{aligned}1 \\ 0 \\ 0\end{aligned}]+[\begin{aligned}10 \\ -30 \\ 40\end{aligned}] \\  & =[\begin{aligned}11 \\ -30 \\ 40\end{aligned}].\end{aligned}
$$

## q-32499 — easy
Profile: `q-32499`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $2g(t)-h(t)$ with respect to $t$, where

$$
\begin{aligned}g(t) & =⟨- 2 \cos{\left(t \right)},\,3 t - 3,\,- 3 t^{2}⟩ \\ h(t) & =⟨- 2 \sin{\left(t \right)},\,- t,\,12⟩\end{aligned}
$$

- $⟨4 \cos{\left(t \right)},\,7,\,12 t⟩$
- $⟨2 \sin{\left(t \right)},\,3,\,- 6 t⟩$
- $⟨4 \sin{\left(t \right)},\,6,\,- 12 t⟩$
- $⟨4 \sin{\left(t \right)} + 2 \cos{\left(t \right)},\,7,\,- 12 t⟩$ **correct**
- $⟨- 2 \cos{\left(t \right)},\,-1,\,0⟩$

Using the constant multiple and the sum rules, we have

$$
(2g(t)-h(t))^{′}=2{g}^{′}(t)-{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 \cos{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(3 t - 3),\,\frac{\text{d}}{\text{d}t}(- 3 t^{2})⟩ \\  & =⟨2 \sin{\left(t \right)},\,3,\,- 6 t⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 \sin{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(- t),\,\frac{\text{d}}{\text{d}t}(12)⟩ \\  & =⟨- 2 \cos{\left(t \right)},\,-1,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2g(t)-h(t))^{′} & =2{g}^{′}(t)-{h}^{′}(t) \\  & =2⟨2 \sin{\left(t \right)},\,3,\,- 6 t⟩-⟨- 2 \cos{\left(t \right)},\,-1,\,0⟩ \\  & =⟨4 \sin{\left(t \right)},\,6,\,- 12 t⟩-⟨- 2 \cos{\left(t \right)},\,-1,\,0⟩ \\  & =⟨4 \sin{\left(t \right)} + 2 \cos{\left(t \right)},\,7,\,- 12 t⟩ \\  & =⟨4 \sin{\left(t \right)} + 2 \cos{\left(t \right)},\,7,\,- 12 t⟩\end{aligned}
$$

## q-32499 — easy
Profile: `q-32499`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $2g(t)-h(t)$ with respect to $t$, where

$$
\begin{aligned}g(t) & =⟨\cos{\left(t \right)},\,9 - 9 t,\,- 2 t^{2}⟩ \\ h(t) & =⟨\sin{\left(t \right)},\,3 t,\,8⟩\end{aligned}
$$

- $⟨- 2 \cos{\left(t \right)},\,-21,\,8 t⟩$
- $⟨\cos{\left(t \right)},\,3,\,0⟩$
- $⟨- \sin{\left(t \right)},\,-9,\,- 4 t⟩$
- $⟨- 2 \sin{\left(t \right)},\,-18,\,- 8 t⟩$
- $⟨- 2 \sin{\left(t \right)} - \cos{\left(t \right)},\,-21,\,- 8 t⟩$ **correct**

Using the constant multiple and the sum rules, we have

$$
(2g(t)-h(t))^{′}=2{g}^{′}(t)-{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\cos{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(9 - 9 t),\,\frac{\text{d}}{\text{d}t}(- 2 t^{2})⟩ \\  & =⟨- \sin{\left(t \right)},\,-9,\,- 4 t⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\sin{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(3 t),\,\frac{\text{d}}{\text{d}t}(8)⟩ \\  & =⟨\cos{\left(t \right)},\,3,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2g(t)-h(t))^{′} & =2{g}^{′}(t)-{h}^{′}(t) \\  & =2⟨- \sin{\left(t \right)},\,-9,\,- 4 t⟩-⟨\cos{\left(t \right)},\,3,\,0⟩ \\  & =⟨- 2 \sin{\left(t \right)},\,-18,\,- 8 t⟩-⟨\cos{\left(t \right)},\,3,\,0⟩ \\  & =⟨- 2 \sin{\left(t \right)} - \cos{\left(t \right)},\,-21,\,- 8 t⟩ \\  & =⟨- 2 \sin{\left(t \right)} - \cos{\left(t \right)},\,-21,\,- 8 t⟩\end{aligned}
$$

## q-32503 — easy
Profile: `q-32503`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $f(t)+g(t)+h(t)$ with respect to $t$, where

$$
\begin{aligned}f(t) & =⟨2,\,0,\,3⟩ \\ g(t) & =⟨2 t,\,0,\,3 t⟩ \\ h(t) & =⟨2 t^{2},\,0,\,3 t^{2}⟩\end{aligned}
$$

- $⟨2,\,0,\,3⟩$
- $⟨2 - 2 t,\,0,\,3 t + 3⟩$
- $⟨- 4 t - 2,\,2 t + 1,\,6 t + 3⟩$
- $⟨4 t + 2,\,0,\,6 t + 3⟩$ **correct**
- $⟨4 t,\,0,\,6 t⟩$

Using the sum rule, we can write

$$
(f(t)+g(t)+h(t))^{′}={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(3)⟩ \\  & =⟨0,\,0,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(3 t)⟩ \\  & =⟨2,\,0,\,3⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(3 t^{2})⟩ \\  & =⟨4 t,\,0,\,6 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t)+h(t))^{′} & ={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t) \\  & =⟨0,\,0,\,0⟩+⟨2,\,0,\,3⟩+⟨4 t,\,0,\,6 t⟩ \\  & =⟨4 t + 2,\,0,\,6 t + 3⟩\end{aligned}
$$

## q-32503 — easy
Profile: `q-32503`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $f(t)+g(t)+h(t)$ with respect to $t$, where

$$
\begin{aligned}f(t) & =⟨-1,\,0,\,2⟩ \\ g(t) & =⟨- t,\,0,\,2 t⟩ \\ h(t) & =⟨- t^{2},\,0,\,2 t^{2}⟩\end{aligned}
$$

- $⟨-1,\,0,\,2⟩$
- $⟨- 2 t,\,0,\,4 t⟩$
- $⟨t - 1,\,0,\,2 t + 2⟩$
- $⟨2 t + 1,\,- 6 t - 3,\,4 t + 2⟩$
- $⟨- 2 t - 1,\,0,\,4 t + 2⟩$ **correct**

Using the sum rule, we can write

$$
(f(t)+g(t)+h(t))^{′}={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(-1),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(2)⟩ \\  & =⟨0,\,0,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(2 t)⟩ \\  & =⟨-1,\,0,\,2⟩ \\ {h}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t^{2}),\,\frac{\text{d}}{\text{d}t}(0),\,\frac{\text{d}}{\text{d}t}(2 t^{2})⟩ \\  & =⟨- 2 t,\,0,\,4 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t)+h(t))^{′} & ={f}^{′}(t)+{g}^{′}(t)+{h}^{′}(t) \\  & =⟨0,\,0,\,0⟩+⟨-1,\,0,\,2⟩+⟨- 2 t,\,0,\,4 t⟩ \\  & =⟨- 2 t - 1,\,0,\,4 t + 2⟩\end{aligned}
$$

## q-33123 — easy
Profile: `q-33123`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $2f(t)+3g(t)$ with respect to $t$, where

 

$$
\begin{aligned}f(t) & =\left(- 4 \sin{\left(t \right)}\,i\right)+\left(3 \cos{\left(t \right)}\,j- 9 \cos{\left(t \right)}\,k\right) \\ g(t) & =\left((2 \sin{\left(t \right)} - 10)\,i\right)+\left(-1\,j\right)+\left(6 \cos{\left(t \right)}\,k\right)\end{aligned}
$$

- $\left(- 4 \cos{\left(t \right)}\,i\right)+\left(- 3 \sin{\left(t \right)}\,j\right)+\left(9 \sin{\left(t \right)}\,k\right)$
- $\left(2 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,k\right)$
- $\left(- 2 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,j\right)$ **correct**
- $\left(- 4 \cos{\left(t \right)}\,i\right)+\left(6 \sin{\left(t \right)}\,j\right)+\left(18 \sin{\left(t \right)}\,k\right)$
- $\left(- 8 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,j\right)+\left(18 \sin{\left(t \right)}\,k\right)$

Using the constant multiple and the sum rules, we have 

$$
(2f(t)+3g(t))^{′}=2{f}^{′}(t)+3{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(- 4 \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(3 \cos{\left(t \right)})\,j+\frac{\text{d}}{\text{d}t}(- 9 \cos{\left(t \right)})\,k \\  & =\left(- 4 \cos{\left(t \right)}\,i\right)+\left(- 3 \sin{\left(t \right)}\,j\right)+\left(9 \sin{\left(t \right)}\,k\right) \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)} - 10)\,i+\frac{\text{d}}{\text{d}t}(-1)\,j+\frac{\text{d}}{\text{d}t}(6 \cos{\left(t \right)})\,k \\  & =\left(2 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,k\right)\end{aligned}
$$

Hence 

$$
\begin{aligned}(2f(t)+3g(t))^{′} & =2{f}^{′}(t)+3{g}^{′}(t) \\  & =2\left(\left(- 4 \cos{\left(t \right)}\,i\right)+\left(- 3 \sin{\left(t \right)}\,j\right)+\left(9 \sin{\left(t \right)}\,k\right)\right)+3\left(\left(2 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,k\right)\right) \\  & =\left(- 8 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,j\right)+\left(18 \sin{\left(t \right)}\,k\right)+\left(6 \cos{\left(t \right)}\,i\right)+\left(- 18 \sin{\left(t \right)}\,k\right) \\  & =\left(- 2 \cos{\left(t \right)}\,i\right)+\left(- 6 \sin{\left(t \right)}\,j\right)\end{aligned}
$$

## q-33123 — easy
Profile: `q-33123`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $2f(t)+3g(t)$ with respect to $t$, where

 

$$
\begin{aligned}f(t) & =\left(2 \sin{\left(t \right)}\,i\right)+\left(- 9 \cos{\left(t \right)}\,j- 6 \cos{\left(t \right)}\,k\right) \\ g(t) & =\left((5 - \sin{\left(t \right)})\,i\right)+\left(3\,j\right)+\left(4 \cos{\left(t \right)}\,k\right)\end{aligned}
$$

- $\left(2 \cos{\left(t \right)}\,i\right)+\left(9 \sin{\left(t \right)}\,j\right)+\left(6 \sin{\left(t \right)}\,k\right)$
- $\left(4 \cos{\left(t \right)}\,i\right)+\left(18 \sin{\left(t \right)}\,j\right)+\left(12 \sin{\left(t \right)}\,k\right)$
- $\left(- \cos{\left(t \right)}\,i\right)+\left(- 4 \sin{\left(t \right)}\,k\right)$
- $\left(\cos{\left(t \right)}\,i\right)+\left(18 \sin{\left(t \right)}\,j\right)$ **correct**
- $\left(2 \cos{\left(t \right)}\,i\right)+\left(- 18 \sin{\left(t \right)}\,j\right)+\left(12 \sin{\left(t \right)}\,k\right)$

Using the constant multiple and the sum rules, we have 

$$
(2f(t)+3g(t))^{′}=2{f}^{′}(t)+3{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(- 9 \cos{\left(t \right)})\,j+\frac{\text{d}}{\text{d}t}(- 6 \cos{\left(t \right)})\,k \\  & =\left(2 \cos{\left(t \right)}\,i\right)+\left(9 \sin{\left(t \right)}\,j\right)+\left(6 \sin{\left(t \right)}\,k\right) \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 - \sin{\left(t \right)})\,i+\frac{\text{d}}{\text{d}t}(3)\,j+\frac{\text{d}}{\text{d}t}(4 \cos{\left(t \right)})\,k \\  & =\left(- \cos{\left(t \right)}\,i\right)+\left(- 4 \sin{\left(t \right)}\,k\right)\end{aligned}
$$

Hence 

$$
\begin{aligned}(2f(t)+3g(t))^{′} & =2{f}^{′}(t)+3{g}^{′}(t) \\  & =2\left(\left(2 \cos{\left(t \right)}\,i\right)+\left(9 \sin{\left(t \right)}\,j\right)+\left(6 \sin{\left(t \right)}\,k\right)\right)+3\left(\left(- \cos{\left(t \right)}\,i\right)+\left(- 4 \sin{\left(t \right)}\,k\right)\right) \\  & =\left(4 \cos{\left(t \right)}\,i\right)+\left(18 \sin{\left(t \right)}\,j\right)+\left(12 \sin{\left(t \right)}\,k\right)+\left(- 3 \cos{\left(t \right)}\,i\right)+\left(- 12 \sin{\left(t \right)}\,k\right) \\  & =\left(\cos{\left(t \right)}\,i\right)+\left(18 \sin{\left(t \right)}\,j\right)\end{aligned}
$$

## q-70681 — easy
Profile: `q-70681`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $f(t)+4g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨- 2 \sqrt{t},\,\log{\left(t \right)},\,6⟩ \\ g(t) & =⟨- 2 t,\,\frac{1}{t},\,3 t^{4}⟩\end{aligned}
$$

- $⟨- 8 \sqrt{t},\,\frac{1}{t^{2}},\,24 t⟩$
- $⟨- \frac{8}{\sqrt{t}},\,\frac{t - 4}{t^{2}},\,12 t^{3}⟩$
- $⟨-8 - \frac{1}{\sqrt{t}},\,\frac{t - 4}{t^{2}},\,48 t^{3}⟩$ **correct**
- $⟨-2 - \frac{2}{\sqrt{t}},\,\frac{1}{t},\,48 t^{4}⟩$
- $⟨- 4 \sqrt{t},\,t + \frac{1}{t},\,6 t^{4}⟩$

Using the constant multiple rule and the sum rule, we have

$$
(f(t)+4g(t))^{′}={f}^{′}(t)+4{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(\log{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(6)⟩ \\  & =⟨- \frac{1}{\sqrt{t}},\,\frac{1}{t},\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 t),\,\frac{\text{d}}{\text{d}t}(\frac{1}{t}),\,\frac{\text{d}}{\text{d}t}(3 t^{4})⟩ \\  & =⟨-2,\,- \frac{1}{t^{2}},\,12 t^{3}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+4g(t))^{′} & ={f}^{′}(t)+4{g}^{′}(t) \\  & =⟨- \frac{1}{\sqrt{t}},\,\frac{1}{t},\,0⟩+4⟨-2,\,- \frac{1}{t^{2}},\,12 t^{3}⟩ \\  & =⟨- \frac{1}{\sqrt{t}},\,\frac{1}{t},\,0⟩+⟨-8,\,- \frac{4}{t^{2}},\,48 t^{3}⟩ \\  & =⟨-8 - \frac{1}{\sqrt{t}},\,\frac{t - 4}{t^{2}},\,48 t^{3}⟩ \\  & =⟨-8 - \frac{1}{\sqrt{t}},\,\frac{t - 4}{t^{2}},\,48 t^{3}⟩\end{aligned}
$$

## q-70681 — easy
Profile: `q-70681`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $f(t)+4g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨\sqrt{t},\,- 3 \log{\left(t \right)},\,4⟩ \\ g(t) & =⟨t,\,- \frac{3}{t},\,2 t^{4}⟩\end{aligned}
$$

- $⟨4 \sqrt{t},\,- \frac{3}{t^{2}},\,16 t⟩$
- $⟨2 \sqrt{t},\,- 3 t - \frac{3}{t},\,4 t^{4}⟩$
- $⟨\frac{4}{\sqrt{t}},\,\frac{3 \left(4 - t\right)}{t^{2}},\,8 t^{3}⟩$
- $⟨4 + \frac{1}{2 \sqrt{t}},\,\frac{3 \left(4 - t\right)}{t^{2}},\,32 t^{3}⟩$ **correct**
- $⟨1 + \frac{1}{\sqrt{t}},\,- \frac{3}{t},\,32 t^{4}⟩$

Using the constant multiple rule and the sum rule, we have

$$
(f(t)+4g(t))^{′}={f}^{′}(t)+4{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- 3 \log{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(4)⟩ \\  & =⟨\frac{1}{2 \sqrt{t}},\,- \frac{3}{t},\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(- \frac{3}{t}),\,\frac{\text{d}}{\text{d}t}(2 t^{4})⟩ \\  & =⟨1,\,\frac{3}{t^{2}},\,8 t^{3}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+4g(t))^{′} & ={f}^{′}(t)+4{g}^{′}(t) \\  & =⟨\frac{1}{2 \sqrt{t}},\,- \frac{3}{t},\,0⟩+4⟨1,\,\frac{3}{t^{2}},\,8 t^{3}⟩ \\  & =⟨\frac{1}{2 \sqrt{t}},\,- \frac{3}{t},\,0⟩+⟨4,\,\frac{12}{t^{2}},\,32 t^{3}⟩ \\  & =⟨4 + \frac{1}{2 \sqrt{t}},\,\frac{3 \left(4 - t\right)}{t^{2}},\,32 t^{3}⟩ \\  & =⟨4 + \frac{1}{2 \sqrt{t}},\,\frac{3 \left(4 - t\right)}{t^{2}},\,32 t^{3}⟩\end{aligned}
$$

## q-127998 — easy
Profile: `q-127998`; parameters: `{"scales": [-2, 1, 3]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨4 t - 2,\,t^{2},\,3 \left(t - 1\right)^{2}⟩, \\ g(t) & =⟨- 2 t - 2,\,1 - 2 t,\,3 t^{3}⟩\end{aligned}
$$

- $⟨6,\,2 t + 1,\,3 t \left(3 t + 2\right)⟩$
- $⟨2,\,2 t - 2,\,9 t^{2}⟩$
- $⟨2,\,2 t - 2,\,9 t^{2} + 6 t - 6⟩$ **correct**
- $⟨4,\,- 2 t,\,6 t - 6⟩$
- $⟨2,\,2 t,\,3 t^{2}⟩$

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(4 t - 2),\,\frac{\text{d}}{\text{d}t}(t^{2}),\,\frac{\text{d}}{\text{d}t}(3 \left(t - 1\right)^{2})⟩ \\  & =⟨4,\,2 t,\,6 t - 6⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 t - 2),\,\frac{\text{d}}{\text{d}t}(1 - 2 t),\,\frac{\text{d}}{\text{d}t}(3 t^{3})⟩ \\  & =⟨-2,\,-2,\,9 t^{2}⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨4,\,2 t,\,6 t - 6⟩+⟨-2,\,-2,\,9 t^{2}⟩ \\  & =⟨2,\,2 t - 2,\,9 t^{2} + 6 t - 6⟩.\end{aligned}
$$

## q-127998 — easy
Profile: `q-127998`; parameters: `{"scales": [1, -3, 2]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨1 - 2 t,\,- 3 t^{2},\,2 \left(t - 1\right)^{2}⟩, \\ g(t) & =⟨t + 1,\,6 t - 3,\,2 t^{3}⟩\end{aligned}
$$

- $⟨-3,\,- 6 t - 3,\,2 t \left(3 t + 2\right)⟩$
- $⟨-1,\,- 6 t,\,2 t^{2}⟩$
- $⟨-1,\,6 - 6 t,\,6 t^{2}⟩$
- $⟨-1,\,6 - 6 t,\,6 t^{2} + 4 t - 4⟩$ **correct**
- $⟨-2,\,6 t,\,4 t - 4⟩$

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(1 - 2 t),\,\frac{\text{d}}{\text{d}t}(- 3 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 \left(t - 1\right)^{2})⟩ \\  & =⟨-2,\,- 6 t,\,4 t - 4⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t + 1),\,\frac{\text{d}}{\text{d}t}(6 t - 3),\,\frac{\text{d}}{\text{d}t}(2 t^{3})⟩ \\  & =⟨1,\,6,\,6 t^{2}⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨-2,\,- 6 t,\,4 t - 4⟩+⟨1,\,6,\,6 t^{2}⟩ \\  & =⟨-1,\,6 - 6 t,\,6 t^{2} + 4 t - 4⟩.\end{aligned}
$$

## q-128144 — moderate
Profile: `q-128144`; parameters: `{"scales": [-2, 1, 3]}`.

Find the value of $(f(t)-2g(t))^{′}$ at $t=1,$ if 

$$
\begin{aligned}f(t) & =⟨- 2 t^{2},\,\log{\left(t \right)},\,3 e^{t - 1}⟩, \\ g(t) & =⟨- 4 \sqrt{t},\,t^{3},\,9⟩.\end{aligned}
$$

- $⟨-4,\,7,\,0⟩$
- $⟨-8,\,7,\,27⟩$
- $⟨0,\,-5,\,3⟩$ **correct**
- $⟨0,\,-7,\,0⟩$
- $⟨4,\,-5,\,0⟩$

First, notice that

$$
(f(t)-2g(t))^{′}={f}^{′}(t)-2{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 t^{2}),\,\frac{\text{d}}{\text{d}t}(\log{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(3 e^{t - 1})⟩ \\  & =⟨- 4 t,\,\frac{1}{t},\,3 e^{t - 1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 4 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(t^{3}),\,\frac{\text{d}}{\text{d}t}(9)⟩ \\  & =⟨- \frac{2}{\sqrt{t}},\,3 t^{2},\,0⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)-2g(t))^{′}\big|_{t=1} & ={f}^{′}(1)-2{g}^{′}(1) \\  & =⟨-4,\,1,\,3⟩-2⟨-2,\,3,\,0⟩ \\  & =⟨-4,\,1,\,3⟩-2⟨-2,\,3,\,0⟩ \\  & =⟨-4,\,1,\,3⟩-⟨-4,\,6,\,0⟩ \\  & =⟨0,\,-5,\,3⟩.\end{aligned}
$$

## q-128144 — moderate
Profile: `q-128144`; parameters: `{"scales": [1, -3, 2]}`.

Find the value of $(f(t)-2g(t))^{′}$ at $t=1,$ if 

$$
\begin{aligned}f(t) & =⟨t^{2},\,- 3 \log{\left(t \right)},\,2 e^{t - 1}⟩, \\ g(t) & =⟨2 \sqrt{t},\,- 3 t^{3},\,6⟩.\end{aligned}
$$

- $⟨2,\,-21,\,0⟩$
- $⟨-2,\,15,\,0⟩$
- $⟨4,\,-21,\,18⟩$
- $⟨0,\,15,\,2⟩$ **correct**
- $⟨0,\,21,\,0⟩$

First, notice that

$$
(f(t)-2g(t))^{′}={f}^{′}(t)-2{g}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\,\frac{\text{d}}{\text{d}t}(- 3 \log{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(2 e^{t - 1})⟩ \\  & =⟨2 t,\,- \frac{3}{t},\,2 e^{t - 1}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(6)⟩ \\  & =⟨\frac{1}{\sqrt{t}},\,- 9 t^{2},\,0⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f(t)-2g(t))^{′}\big|_{t=1} & ={f}^{′}(1)-2{g}^{′}(1) \\  & =⟨2,\,-3,\,2⟩-2⟨1,\,-9,\,0⟩ \\  & =⟨2,\,-3,\,2⟩-2⟨1,\,-9,\,0⟩ \\  & =⟨2,\,-3,\,2⟩-⟨2,\,-18,\,0⟩ \\  & =⟨0,\,15,\,2⟩.\end{aligned}
$$

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 2, "b": 1, "A": 2, "B": -3, "n": 3, "h": 1, "u": 3, "v": 4}`.

Find the derivative of $2f(t)-3g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(2 t^{3} + 1)\,i- \frac{2}{t - 1}\,j+\cos{\left(3 t \right)}\,k \\ g(t)&=(t - 2)\,i+e^{4 t}\,j+\cos{\left(3 t \right)}\,k\end{aligned}
$$

- $12 t^{2}\,i+\frac{4}{\left(t - 1\right)^{2}}\,j- 6 \sin{\left(3 t \right)}\,k$
- $(- 12 t^{2} - 3)\,i+(- 12 e^{4 t} - \frac{4}{\left(t - 1\right)^{2}})\,j+15 \sin{\left(3 t \right)}\,k$
- $(4 t^{3} - 3 t + 8)\,i+\frac{3 \left(1 - t\right) e^{4 t} - 4}{t - 1}\,j- \cos{\left(3 t \right)}\,k$
- $(12 t^{2} - 3)\,i+(- 12 e^{4 t} + \frac{4}{\left(t - 1\right)^{2}})\,j+3 \sin{\left(3 t \right)}\,k$ **correct**
- $-3\,i- 12 e^{4 t}\,j+9 \sin{\left(3 t \right)}\,k$

Using the constant multiple rule and the sum rule, we have

$$
(2f(t)-3g(t))'=2f'(\!t)-3g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{3} + 1),\,\frac{\text{d}}{\text{d}t}(- \frac{2}{t - 1}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=6 t^{2}\,i+\frac{2}{\left(t - 1\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t - 2),\,\frac{\text{d}}{\text{d}t}(e^{4 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=1\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2f(t)-3g(t))'&=2f'(\!t)-3g'(\!t) \\ &=2\left(6 t^{2}\,i+\frac{2}{\left(t - 1\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k\right)-3\left(1\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\right) \\ &=\left(12 t^{2}\,i+\frac{4}{\left(t - 1\right)^{2}}\,j- 6 \sin{\left(3 t \right)}\,k\right)+\left(-3\,i- 12 e^{4 t}\,j+9 \sin{\left(3 t \right)}\,k\right) \\ &=(12 t^{2} - 3)\,i+(- 12 e^{4 t} + \frac{4}{\left(t - 1\right)^{2}})\,j+3 \sin{\left(3 t \right)}\,k.\end{aligned}
$$

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 1, "b": 1, "A": -3, "B": 2, "n": 2, "h": 3, "u": 4, "v": 3}`.

Find the derivative of $-3f(t)+2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(t^{2} + 1)\,i- \frac{1}{t - 3}\,j+\cos{\left(4 t \right)}\,k \\ g(t)&=(t - 1)\,i+e^{3 t}\,j+\cos{\left(4 t \right)}\,k\end{aligned}
$$

- $- 6 t\,i- \frac{3}{\left(t - 3\right)^{2}}\,j+12 \sin{\left(4 t \right)}\,k$
- $2\,i+6 e^{3 t}\,j- 8 \sin{\left(4 t \right)}\,k$
- $(6 t + 2)\,i+(6 e^{3 t} + \frac{3}{\left(t - 3\right)^{2}})\,j- 20 \sin{\left(4 t \right)}\,k$
- $(- 3 t^{2} + 2 t - 5)\,i+\frac{2 \left(t - 3\right) e^{3 t} + 3}{t - 3}\,j- \cos{\left(4 t \right)}\,k$
- $(2 - 6 t)\,i+(6 e^{3 t} - \frac{3}{\left(t - 3\right)^{2}})\,j+4 \sin{\left(4 t \right)}\,k$ **correct**

Using the constant multiple rule and the sum rule, we have

$$
(-3f(t)+2g(t))'=-3f'(\!t)+2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(t^{2} + 1),\,\frac{\text{d}}{\text{d}t}(- \frac{1}{t - 3}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=2 t\,i+\frac{1}{\left(t - 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t - 1),\,\frac{\text{d}}{\text{d}t}(e^{3 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=1\,i+3 e^{3 t}\,j- 4 \sin{\left(4 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(-3f(t)+2g(t))'&=-3f'(\!t)+2g'(\!t) \\ &=-3\left(2 t\,i+\frac{1}{\left(t - 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k\right)+2\left(1\,i+3 e^{3 t}\,j- 4 \sin{\left(4 t \right)}\,k\right) \\ &=\left(- 6 t\,i- \frac{3}{\left(t - 3\right)^{2}}\,j+12 \sin{\left(4 t \right)}\,k\right)+\left(2\,i+6 e^{3 t}\,j- 8 \sin{\left(4 t \right)}\,k\right) \\ &=(2 - 6 t)\,i+(6 e^{3 t} - \frac{3}{\left(t - 3\right)^{2}})\,j+4 \sin{\left(4 t \right)}\,k.\end{aligned}
$$

## q-33122 — easy
Profile: `authored-operations`; parameters: `{"scales": [1, -3, 1]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨3 t - 1,\,3 t - 18,\,7 t⟩ \\ g(t) & =⟨t^{2},\,3 t^{2} - 3,\,t⟩\end{aligned}
$$

- $⟨3,\,3,\,7⟩$
- $⟨2 t,\,6 t,\,1⟩$
- $⟨t^{2} + 3 t - 1,\,3 t^{2} + 3 t - 21,\,8 t⟩$
- $⟨2 t - 3,\,6 t - 3,\,-6⟩$
- $⟨2 t + 3,\,6 t + 3,\,8⟩$ **correct**

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t - 1),\,\frac{\text{d}}{\text{d}t}(3 t - 18),\,\frac{\text{d}}{\text{d}t}(7 t)⟩ \\  & =⟨3,\,3,\,7⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t^{2}),\,\frac{\text{d}}{\text{d}t}(3 t^{2} - 3),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨2 t,\,6 t,\,1⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨3,\,3,\,7⟩+⟨2 t,\,6 t,\,1⟩ \\  & =⟨2 t + 3,\,6 t + 3,\,8⟩\end{aligned}
$$

## q-33122 — easy
Profile: `authored-operations`; parameters: `{"scales": [-2, -2, -1]}`.

Differentiate $f(t)+g(t)$ with respect to $t$, given that 

$$
\begin{aligned}f(t) & =⟨2 - 6 t,\,2 t - 12,\,- 7 t⟩ \\ g(t) & =⟨- 2 t^{2},\,2 t^{2} - 2,\,- t⟩\end{aligned}
$$

- $⟨-6,\,2,\,-7⟩$
- $⟨6 - 4 t,\,4 t - 2,\,6⟩$
- $⟨- 2 t^{2} - 6 t + 2,\,2 t^{2} + 2 t - 14,\,- 8 t⟩$
- $⟨- 4 t,\,4 t,\,-1⟩$
- $⟨- 4 t - 6,\,4 t + 2,\,-8⟩$ **correct**

By the sum rule, we have

$$
(f(t)+g(t))^{′}={f}^{′}(t)+{g}^{′}(t)
$$

Let's find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 - 6 t),\,\frac{\text{d}}{\text{d}t}(2 t - 12),\,\frac{\text{d}}{\text{d}t}(- 7 t)⟩ \\  & =⟨-6,\,2,\,-7⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 2 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t^{2} - 2),\,\frac{\text{d}}{\text{d}t}(- t)⟩ \\  & =⟨- 4 t,\,4 t,\,-1⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f(t)+g(t))^{′} & ={f}^{′}(t)+{g}^{′}(t) \\  & =⟨-6,\,2,\,-7⟩+⟨- 4 t,\,4 t,\,-1⟩ \\  & =⟨- 4 t - 6,\,4 t + 2,\,-8⟩\end{aligned}
$$

## q-33143 — moderate
Profile: `authored-operations`; parameters: `{"scales": [1, -3, 1]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨2 t^{2},\,9 - 3 t,\,t^{3} + 8⟩; g(t)= ⟨t \left(t + 2\right),\,-24,\,2 t^{3}⟩$

- $⟨24,\,-9,\,36⟩$
- $⟨-12,\,0,\,-48⟩$
- $⟨8,\,57,\,16⟩$
- $⟨-36,\,9,\,-84⟩$
- $⟨12,\,-9,\,-12⟩$ **correct**

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(9 - 3 t),\,\frac{\text{d}}{\text{d}t}(t^{3} + 8)⟩ \\ &=⟨4 t,\,-3,\,3 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(-24),\,\frac{\text{d}}{\text{d}t}(2 t^{3})⟩ \\ &=⟨2 t + 2,\,0,\,6 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨8,\,-3,\,12⟩\right)-2\left(⟨6,\,0,\,24⟩\right) \\ &=\left(⟨24,\,-9,\,36⟩\right)+\left(⟨-12,\,0,\,-48⟩\right) \\ &=⟨12,\,-9,\,-12⟩.\end{aligned}
$$

## q-33143 — moderate
Profile: `authored-operations`; parameters: `{"scales": [-2, -2, -1]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨- 4 t^{2},\,6 - 2 t,\,- t^{3} - 8⟩; g(t)= ⟨2 t \left(- t - 2\right),\,-16,\,- 2 t^{3}⟩$

- $⟨-48,\,-6,\,-36⟩$
- $⟨72,\,6,\,84⟩$
- $⟨-16,\,38,\,-16⟩$
- $⟨24,\,0,\,48⟩$
- $⟨-24,\,-6,\,12⟩$ **correct**

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(- 4 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 - 2 t),\,\frac{\text{d}}{\text{d}t}(- t^{3} - 8)⟩ \\ &=⟨- 8 t,\,-2,\,- 3 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(- 2 t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(-16),\,\frac{\text{d}}{\text{d}t}(- 2 t^{3})⟩ \\ &=⟨- 4 t - 4,\,0,\,- 6 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨-16,\,-2,\,-12⟩\right)-2\left(⟨-12,\,0,\,-24⟩\right) \\ &=\left(⟨-48,\,-6,\,-36⟩\right)+\left(⟨24,\,0,\,48⟩\right) \\ &=⟨-24,\,-6,\,12⟩.\end{aligned}
$$

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 4, "b": 1, "A": 3, "B": -2, "n": 2, "h": -2, "u": 2, "v": 4}`.

Find the derivative of $3f(t)-2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(4 t^{2} + 1)\,i- \frac{4}{t + 2}\,j+\cos{\left(2 t \right)}\,k \\ g(t)&=(t - 4)\,i+e^{4 t}\,j+\cos{\left(2 t \right)}\,k\end{aligned}
$$

- $24 t\,i+\frac{12}{\left(t + 2\right)^{2}}\,j- 6 \sin{\left(2 t \right)}\,k$
- $-2\,i- 8 e^{4 t}\,j+4 \sin{\left(2 t \right)}\,k$
- $(12 t^{2} - 2 t + 11)\,i+\frac{2 \left(\left(- t - 2\right) e^{4 t} - 6\right)}{t + 2}\,j+\cos{\left(2 t \right)}\,k$
- $(- 24 t - 2)\,i+(- 8 e^{4 t} - \frac{12}{\left(t + 2\right)^{2}})\,j+10 \sin{\left(2 t \right)}\,k$
- $(24 t - 2)\,i+(- 8 e^{4 t} + \frac{12}{\left(t + 2\right)^{2}})\,j- 2 \sin{\left(2 t \right)}\,k$ **correct**

Using the constant multiple rule and the sum rule, we have

$$
(3f(t)-2g(t))'=3f'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(4 t^{2} + 1),\,\frac{\text{d}}{\text{d}t}(- \frac{4}{t + 2}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(2 t \right)})⟩ \\ &=8 t\,i+\frac{4}{\left(t + 2\right)^{2}}\,j- 2 \sin{\left(2 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t - 4),\,\frac{\text{d}}{\text{d}t}(e^{4 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(2 t \right)})⟩ \\ &=1\,i+4 e^{4 t}\,j- 2 \sin{\left(2 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3f(t)-2g(t))'&=3f'(\!t)-2g'(\!t) \\ &=3\left(8 t\,i+\frac{4}{\left(t + 2\right)^{2}}\,j- 2 \sin{\left(2 t \right)}\,k\right)-2\left(1\,i+4 e^{4 t}\,j- 2 \sin{\left(2 t \right)}\,k\right) \\ &=\left(24 t\,i+\frac{12}{\left(t + 2\right)^{2}}\,j- 6 \sin{\left(2 t \right)}\,k\right)+\left(-2\,i- 8 e^{4 t}\,j+4 \sin{\left(2 t \right)}\,k\right) \\ &=(24 t - 2)\,i+(- 8 e^{4 t} + \frac{12}{\left(t + 2\right)^{2}})\,j- 2 \sin{\left(2 t \right)}\,k.\end{aligned}
$$

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 2, "b": 2, "A": 2, "B": -2, "n": 3, "h": -3, "u": 4, "v": 2}`.

Find the derivative of $2f(t)-2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(2 t^{3} + 2)\,i- \frac{2}{t + 3}\,j+\cos{\left(4 t \right)}\,k \\ g(t)&=(2 t - 2)\,i+e^{2 t}\,j+\cos{\left(4 t \right)}\,k\end{aligned}
$$

- $12 t^{2}\,i+\frac{4}{\left(t + 3\right)^{2}}\,j- 8 \sin{\left(4 t \right)}\,k$
- $(- 12 t^{2} - 4)\,i+(- 4 e^{2 t} - \frac{4}{\left(t + 3\right)^{2}})\,j+16 \sin{\left(4 t \right)}\,k$
- $(4 t^{3} - 4 t + 8)\,i+\frac{2 \left(\left(- t - 3\right) e^{2 t} - 2\right)}{t + 3}\,j$
- $-4\,i- 4 e^{2 t}\,j+8 \sin{\left(4 t \right)}\,k$
- $(12 t^{2} - 4)\,i+(- 4 e^{2 t} + \frac{4}{\left(t + 3\right)^{2}})\,j$ **correct**

Using the constant multiple rule and the sum rule, we have

$$
(2f(t)-2g(t))'=2f'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{3} + 2),\,\frac{\text{d}}{\text{d}t}(- \frac{2}{t + 3}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=6 t^{2}\,i+\frac{2}{\left(t + 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t - 2),\,\frac{\text{d}}{\text{d}t}(e^{2 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=2\,i+2 e^{2 t}\,j- 4 \sin{\left(4 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2f(t)-2g(t))'&=2f'(\!t)-2g'(\!t) \\ &=2\left(6 t^{2}\,i+\frac{2}{\left(t + 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k\right)-2\left(2\,i+2 e^{2 t}\,j- 4 \sin{\left(4 t \right)}\,k\right) \\ &=\left(12 t^{2}\,i+\frac{4}{\left(t + 3\right)^{2}}\,j- 8 \sin{\left(4 t \right)}\,k\right)+\left(-4\,i- 4 e^{2 t}\,j+8 \sin{\left(4 t \right)}\,k\right) \\ &=(12 t^{2} - 4)\,i+(- 4 e^{2 t} + \frac{4}{\left(t + 3\right)^{2}})\,j.\end{aligned}
$$