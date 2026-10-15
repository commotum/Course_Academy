# Trigonometric integration by parts

Raw originals followed by labeled parameterized replays and generated variants. All source fields, correct refs, levels and solutions are present; raw missing keys: none. No within-level progression.

## Original q-12564 — moderate

Field type: radio

$\int (x+3)\operatorname{cos}⁡(3x)\,\text{d}x=$

- $\frac{x\operatorname{sin}⁡(3x)}{9}+\frac{\operatorname{cos}⁡(3x)}{3}+C$
- $-\frac{\operatorname{sin}⁡(3x)}{3}+\frac{x\operatorname{cos}⁡(3x)}{9}+C$
- $\frac{(x+3)\operatorname{sin}⁡(3x)}{3}+\frac{\operatorname{cos}⁡(3x)}{9}+C$ **original correct**
- $\frac{(x+3)\operatorname{sin}⁡(3x)}{9}+\frac{\operatorname{cos}⁡(3x)}{3}+C$
- $\frac{(x+3)\operatorname{sin}⁡(3x)}{3}-\frac{x\operatorname{cos}⁡(3x)}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x+3)\operatorname{cos}⁡(3x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x+3\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{cos}⁡(3x)\, & ⟹\,v=\frac{\operatorname{sin}⁡(3x)}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x+3)\cdot \operatorname{cos}⁡(3x)\,\text{d}x & =(x+3)\cdot \frac{\operatorname{sin}⁡(3x)}{3}-\int \frac{\operatorname{sin}⁡(3x)}{3}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x+3)\operatorname{cos}⁡(3x)\text{d}x & =\frac{(x+3)\operatorname{sin}⁡(3x)}{3}-\frac{1}{3}\int \operatorname{sin}⁡(3x)\,\text{d}x \\  & =\frac{(x+3)\operatorname{sin}⁡(3x)}{3}+\frac{\operatorname{cos}⁡(3x)}{9}+C\end{aligned}
$$

---

## Original q-14437 — easy

Field type: radio

Calculate $\int 2x\operatorname{sin}⁡(x)\,\text{d}x.$

- $-2x\operatorname{sin}⁡x+\operatorname{cos}⁡x+C$
- $2x\operatorname{cos}⁡x-x\operatorname{sin}⁡x+C$
- $\operatorname{cos}⁡2x+x\operatorname{sin}⁡2x+C$
- $-x\operatorname{cos}⁡x-\operatorname{cos}⁡2x+C$
- $-2x\operatorname{cos}⁡x+2\operatorname{sin}⁡x+C$ **original correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2x\operatorname{sin}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}⁡(x)\, & ⟹\,v=-\operatorname{cos}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 2x\cdot \operatorname{sin}⁡(x)\,\text{d}x & =2x\cdot (-\operatorname{cos}⁡(x))-\int (-\operatorname{cos}⁡(x))\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 2x\operatorname{sin}⁡(x)\,\text{d}x & =-2x\operatorname{cos}⁡(x)+2\int \operatorname{cos}⁡(x)\,\text{d}x \\  & =-2x\operatorname{cos}⁡(x)+2\operatorname{sin}⁡(x)+C\end{aligned}
$$

---

## Original q-114297 — easy

Field type: radio

$\int 3x\operatorname{cos}⁡(3x)\,\text{d}x=$

- $3\operatorname{sin}⁡(3x)+\frac{x\operatorname{cos}⁡(3x)}{6}+C$
- $\operatorname{sin}⁡(3x)-\frac{x\operatorname{cos}⁡(3x)}{3}+C$
- $2x\operatorname{sin}⁡(3x)+\frac{\operatorname{cos}⁡(3x)}{3}+C$
- $x\operatorname{sin}⁡(3x)+\frac{\operatorname{cos}⁡(3x)}{3}+C$ **original correct**
- $\frac{x\operatorname{sin}⁡(3x)}{3}-\frac{\operatorname{cos}⁡(3x)}{9}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3x\operatorname{cos}⁡(3x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}⁡(3x)\, & ⟹\,v=\frac{\operatorname{sin}⁡(3x)}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3x\cdot \operatorname{cos}⁡(3x)\,\text{d}x & =3x\cdot (\frac{\operatorname{sin}⁡(3x)}{3})-\int (\frac{\operatorname{sin}⁡(3x)}{3})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3x\operatorname{cos}⁡(3x)\,\text{d}x & =x\operatorname{sin}⁡(3x)-\int \operatorname{sin}⁡(3x)\,\text{d}x \\  & =x\operatorname{sin}⁡(3x)+\frac{\operatorname{cos}⁡(3x)}{3}+C\end{aligned}
$$

---

## Original q-114299 — easy

Field type: radio

Calculate $\int 2x\operatorname{cos}⁡4x\,\text{d}x.$

- $\frac{x\operatorname{sin}⁡4x}{2}+\frac{\operatorname{cos}⁡4x}{8}+C$ **original correct**
- $\frac{3x\operatorname{sin}⁡4x}{2}+\frac{\operatorname{cos}⁡4x}{4}+C$
- $\frac{x\operatorname{sin}⁡4x}{4}-\frac{\operatorname{cos}⁡4x}{2}+C$
- $-\frac{\operatorname{sin}⁡4x}{4}+\frac{x\operatorname{cos}⁡4x}{6}+C$
- $-\frac{\operatorname{sin}⁡4x}{8}+\frac{x\operatorname{cos}⁡4x}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2x\operatorname{cos}⁡4x\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{cos}⁡4x\, & ⟹\,v=\frac{1}{4}\operatorname{sin}⁡4x.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 2x\operatorname{cos}⁡4x\,\text{d}x & =2x\cdot \frac{1}{4}\operatorname{sin}⁡4x-\int \frac{1}{4}\operatorname{sin}⁡4x\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 2x\operatorname{cos}⁡4x\,\text{d}x & =\frac{1}{2}x\operatorname{sin}⁡4x-\frac{1}{2}\int \operatorname{sin}⁡4x\,\text{d}x \\  & =\frac{1}{2}x\operatorname{sin}⁡4x-\frac{1}{2}(-\frac{1}{4}\operatorname{cos}⁡4x)+C \\  & =\frac{1}{2}x\operatorname{sin}⁡4x+\frac{1}{8}\operatorname{cos}⁡4x+C\end{aligned}
$$

---

## Original q-114309 — moderate

Field type: radio

$\int (x+4)\operatorname{sin}⁡(2x)\,\text{d}x=$

- $-\frac{(x+4)\operatorname{cos}⁡(2x)}{2}+\frac{\operatorname{sin}⁡(2x)}{4}+C$ **original correct**
- $-\frac{3(x+4)\operatorname{cos}⁡(2x)}{2}+\frac{\operatorname{sin}⁡(2x)}{6}+C$
- $-\frac{(x+4)\operatorname{cos}⁡(2x)}{4}+\frac{\operatorname{sin}⁡(2x)}{8}+C$
- $-\frac{(x+4)\operatorname{cos}⁡(2x)}{6}-\frac{\operatorname{sin}⁡(2x)}{2}+C$
- $-\frac{(x+4)\operatorname{cos}⁡(2x)}{4}-\frac{\operatorname{sin}⁡(2x)}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x+4)\operatorname{sin}⁡(2x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x+4\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{sin}⁡(2x)\, & ⟹\,v=-\frac{\operatorname{cos}⁡(2x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x+4)\cdot \operatorname{sin}⁡(2x)\,\text{d}x & =(x+4)\cdot (-\frac{\operatorname{cos}⁡(2x)}{2})-\int (-\frac{\operatorname{cos}⁡(2x)}{2})\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x+4)\operatorname{sin}⁡(2x)\text{d}x & =-\frac{(x+4)\operatorname{cos}⁡(2x)}{2}+\frac{1}{2}\int \operatorname{cos}⁡(2x)\,\text{d}x \\  & =-\frac{(x+4)\operatorname{cos}⁡(2x)}{2}+\frac{\operatorname{sin}⁡(2x)}{4}+C\end{aligned}
$$

---

## Original q-114311 — moderate

Field type: radio

$\int (2x+3)\operatorname{sin}⁡(x)\,\text{d}x=$

- $-(2x+3)\operatorname{cos}⁡(x)+2\operatorname{sin}⁡(x)+C$ **original correct**
- $x\operatorname{cos}⁡(x)-6\operatorname{sin}⁡(x)+C$
- $(2x+3)\operatorname{cos}⁡(x)-\operatorname{sin}⁡(x)+C$
- $2x\operatorname{cos}⁡(x)+4\operatorname{sin}⁡(x)+C$
- $-(2x+3)\operatorname{cos}⁡(x)-4\operatorname{sin}⁡(x)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (2x+3)\operatorname{sin}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x+3\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}⁡(x)\, & ⟹\,v=-\operatorname{cos}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (2x+3)\cdot \operatorname{sin}⁡(x)\,\text{d}x & =(2x+3)\cdot (-\operatorname{cos}⁡(x))-\int (-\operatorname{cos}⁡(x))\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows

$$
\begin{aligned}\int (2x+3)\operatorname{sin}⁡(x)\text{d}x & =-(2x+3)\operatorname{cos}⁡(x)+2\int \operatorname{cos}⁡(x)\,\text{d}x \\  & =-(2x+3)\operatorname{cos}⁡(x)+2\operatorname{sin}⁡(x)+C\end{aligned}
$$

---

## Original q-114312 — easy

Field type: radio

$\int x\operatorname{cos}⁡(5x)\,\text{d}x=$

- $\frac{x\operatorname{sin}⁡(5x)}{15}+\frac{\operatorname{cos}⁡(5x)}{5}+C$
- $\frac{\operatorname{sin}⁡(5x)}{25}+\frac{x\operatorname{cos}⁡(5x)}{5}+C$
- $\frac{x\operatorname{sin}⁡(5x)}{5}-\frac{2\operatorname{cos}⁡(5x)}{25}+C$
- $\frac{x\operatorname{sin}⁡(5x)}{5}+\frac{\operatorname{cos}⁡(5x)}{25}+C$ **original correct**
- $\frac{2\operatorname{sin}⁡(5x)}{5}-\frac{x\operatorname{cos}⁡(5x)}{15}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x\operatorname{cos}⁡(5x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{cos}⁡(5x)\, & ⟹\,v=\frac{\operatorname{sin}⁡(5x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot \operatorname{cos}⁡(5x)\,\text{d}x & =x\cdot (\frac{\operatorname{sin}⁡(5x)}{5})-\int (\frac{\operatorname{sin}⁡(5x)}{5})\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x\operatorname{cos}⁡(5x)\,\text{d}x & =\frac{x\operatorname{sin}⁡(5x)}{5}-\frac{1}{5}\int \operatorname{sin}⁡(5x)\,\text{d}x \\  & =\frac{x\operatorname{sin}⁡(5x)}{5}+\frac{\operatorname{cos}⁡(5x)}{25}+C\end{aligned}
$$

---

## Original q-114314 — hard

Field type: radio

Calculate $\int x{csc}^{2}⁡x\,\text{d}x.$

- $x\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{cos}⁡x|+C$
- $-x\operatorname{cot}⁡x+\operatorname{ln}⁡|\operatorname{sin}⁡x|+C$ **original correct**
- $-x\operatorname{cot}⁡x-2\operatorname{ln}⁡|\operatorname{cos}⁡x|+C$
- $x\operatorname{tan}⁡x-2\operatorname{ln}⁡|\operatorname{sin}⁡x|+C$
- $-2x\operatorname{cot}⁡x-\operatorname{ln}⁡|\operatorname{sin}⁡x|+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x{csc}^{2}⁡x\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}={csc}^{2}⁡x\, & ⟹\,v=-\operatorname{cot}⁡x.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot {csc}^{2}⁡x\,\text{d}x & =x\cdot (-\operatorname{cot}⁡x)-\int (-\operatorname{cot}⁡x)\cdot 1\,\text{d}x \\  & =-x\operatorname{cot}⁡x+\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral using the substitution $u=\operatorname{sin}⁡x,$ where $\text{d}u=\operatorname{cos}⁡x\,\text{d}x,$ as follows:

$$
\begin{aligned}\int x{csc}^{2}⁡(x)\,\text{d}x & =-x\operatorname{cot}⁡x+\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x \\  & =-x\operatorname{cot}⁡x+\int \frac{1}{u}\,\text{d}u \\  & =-x\operatorname{cot}⁡x+\operatorname{ln}⁡|u|+C \\  & =-x\operatorname{cot}⁡x+\operatorname{ln}⁡|\operatorname{sin}⁡x|+C\end{aligned}
$$

---

## Original q-14449 — easy

Field type: radio

Calculate $\int 5x\operatorname{sin}⁡(x)\,\text{d}x.$

- $\operatorname{cos}⁡5x+x\operatorname{sin}⁡5x+C$
- $-5x\operatorname{sin}⁡x+\operatorname{cos}⁡x+C$
- $-x\operatorname{cos}⁡x-\operatorname{cos}⁡5x+C$
- $-5x\operatorname{cos}⁡x+5\operatorname{sin}⁡x+C$ **original correct**
- $5x\operatorname{cos}⁡x-x\operatorname{sin}⁡x+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 5x\operatorname{sin}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=5x\, & ⟹\,{u}^{′}=5 \\ {v}^{′}=\operatorname{sin}⁡(x)\, & ⟹\,v=-\operatorname{cos}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 5x\cdot \operatorname{sin}⁡(x)\,\text{d}x & =5x\cdot (-\operatorname{cos}⁡(x))-\int (-\operatorname{cos}⁡(x))\cdot 5\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 5x\operatorname{sin}⁡(x)\,\text{d}x & =-5x\operatorname{cos}⁡(x)+5\int \operatorname{cos}⁡(x)\,\text{d}x \\  & =-5x\operatorname{cos}⁡(x)+5\operatorname{sin}⁡(x)+C\end{aligned}
$$

---

## Original q-14453 — easy

Field type: radio

$\int 6x\operatorname{cos}⁡(x)\,\text{d}x=$

- $-6x\operatorname{sin}⁡x+6\operatorname{cos}⁡x+C$
- $x\operatorname{cos}⁡6x+x\operatorname{sin}⁡6x+C$
- $x\operatorname{cos}⁡6x-x\operatorname{sin}⁡6x+C$
- $-6x\operatorname{cos}⁡x-\operatorname{cos}⁡x+C$
- $6x\operatorname{sin}⁡x+6\operatorname{cos}⁡x+C$ **original correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6x\operatorname{cos}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6x\, & ⟹\,{u}^{′}=6 \\ {v}^{′}=\operatorname{cos}⁡(x)\, & ⟹\,v=\operatorname{sin}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 6x\cdot \operatorname{cos}⁡(x)\,\text{d}x & =6x\cdot \operatorname{sin}⁡(x)-\int \operatorname{sin}⁡(x)\cdot 6\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 6x\operatorname{cos}⁡(x)\,\text{d}x & =6x\operatorname{sin}⁡(x)-6\int \operatorname{sin}⁡(x)\,\text{d}x \\  & =6x\operatorname{sin}⁡(x)-6(-\operatorname{cos}⁡(x))+C \\  & =6x\operatorname{sin}⁡(x)+6\operatorname{cos}⁡(x)+C\end{aligned}
$$

---

## Original q-74087 — moderate

Field type: radio

Calculate  $\int 2x\operatorname{cos}⁡(2x+8)\text{d}x.$

- $2x\operatorname{sin}⁡(2x+8)+\operatorname{cos}⁡(2x+8)+C$
- $x\operatorname{sin}⁡(2x+8)+\frac{\operatorname{cos}⁡(2x+8)}{2}+C$ **original correct**
- $2x\operatorname{sin}⁡(2x+8)-\frac{\operatorname{cos}⁡(2x+8)}{4}+C$
- $2x\operatorname{sin}⁡(2x+8)+\frac{\operatorname{cos}⁡(2x+8)}{2}+C$
- $x\operatorname{sin}⁡(2x+8)-\operatorname{cos}⁡(2x+8)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2x\operatorname{cos}⁡(2x+8)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{cos}⁡(2x+8)\, & ⟹\,v=\frac{\operatorname{sin}⁡(2x+8)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 2x\cdot \operatorname{cos}⁡(2x+8)\,\text{d}x & =2x\cdot \frac{\operatorname{sin}⁡(2x+8)}{2}-\int \frac{\operatorname{sin}⁡(2x+8)}{2}\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 2x\operatorname{cos}⁡(2x+8)\text{d}x & =x\operatorname{sin}⁡(2x+8)-\int \operatorname{sin}⁡(2x+8)\text{d}x \\  & =x\operatorname{sin}⁡(2x+8)+\frac{\operatorname{cos}⁡(2x+8)}{2}+C\end{aligned}
$$

---

## Original q-74088 — moderate

Field type: radio

$\int (6x+1)\operatorname{cos}⁡(x)\,\text{d}x=$

- $\operatorname{sin}⁡(x)+\operatorname{cos}⁡(x)+C$
- $(6x+1)\operatorname{sin}⁡(x)+\frac{\operatorname{cos}⁡(x)}{6}+C$
- $6\operatorname{sin}⁡(x)+6\operatorname{cos}⁡(x)+C$
- $(6x+1)\operatorname{sin}⁡(x)+6\operatorname{cos}⁡(x)+C$ **original correct**
- $\frac{(6x+1)\operatorname{sin}⁡(x)}{6}+\operatorname{cos}⁡(x)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (6x+1)\operatorname{cos}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6x+1\, & ⟹\,{u}^{′}=6 \\ {v}^{′}=\operatorname{cos}⁡(x)\, & ⟹\,v=\operatorname{sin}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (6x+1)\cdot \operatorname{cos}⁡(x)\,\text{d}x & =(6x+1)\cdot \operatorname{sin}⁡(x)-\int \operatorname{sin}⁡(x)\cdot 6\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows

$$
\begin{aligned}\int (6x+1)\operatorname{cos}⁡(x)\text{d}x & =(6x+1)\operatorname{sin}⁡(x)-6\int \operatorname{sin}⁡(x)\,\text{d}x \\  & =(6x+1)\operatorname{sin}⁡(x)+6\operatorname{cos}⁡(x)+C\end{aligned}
$$

---

## Original q-74090 — easy

Field type: radio

Calculate $\int 10x\operatorname{cos}⁡(x)\,\text{d}x.$

- $\frac{x\operatorname{sin}⁡(x)}{10}-\operatorname{cos}⁡(x)+C$
- $10x\operatorname{sin}⁡(x)+\frac{\operatorname{cos}⁡(x)}{10}+C$
- $10x\operatorname{sin}⁡(x)+10\operatorname{cos}⁡(x)+C$ **original correct**
- $10\operatorname{sin}⁡(x)-10x\operatorname{cos}⁡(x)+C$
- $10\operatorname{sin}⁡(x)-\operatorname{cos}⁡(x)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 10x\operatorname{cos}⁡(x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=10x\, & ⟹\,{u}^{′}=10 \\ {v}^{′}=\operatorname{cos}⁡(x)\, & ⟹\,v=\operatorname{sin}⁡(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 10x\cdot \operatorname{cos}⁡(x)\,\text{d}x & =10x\cdot (\operatorname{sin}⁡(x))-\int (\operatorname{sin}⁡(x))\cdot 10\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 10x\operatorname{cos}⁡(x)\,\text{d}x & =10x\operatorname{sin}⁡(x)-10\int \operatorname{sin}⁡(x)\,\text{d}x \\  & =10x\operatorname{sin}⁡(x)+10\operatorname{cos}⁡(x)+C\end{aligned}
$$

---

## Original q-12565 — moderate

Field type: radio

Calculate  $\int x\operatorname{sin}⁡(3x+5)\text{d}x.$

- $-\frac{3x\operatorname{cos}⁡(x+5)}{3}+\frac{3\operatorname{sin}⁡(x+5)}{9}+C$
- $\frac{\operatorname{cos}⁡(3x+5)}{3}+\frac{x\operatorname{sin}⁡(3x+5)}{9}+C$
- $-\frac{x\operatorname{cos}⁡(3x+5)}{3}+\frac{\operatorname{sin}⁡(3x+5)}{9}+C$ **original correct**
- $\frac{x\operatorname{cos}⁡(3x+5)}{9}-\frac{\operatorname{sin}⁡(3x+5)}{3}+C$
- $\frac{x\operatorname{cos}⁡(3x+5)}{9}+\frac{2\operatorname{sin}⁡(3x+5)}{9}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x\operatorname{sin}⁡(3x+5)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{sin}⁡(3x+5)\, & ⟹\,v=-\frac{\operatorname{cos}⁡(3x+5)}{3}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot \operatorname{sin}⁡(3x+5)\,\text{d}x & =x\cdot (-\frac{\operatorname{cos}⁡(3x+5)}{3})-\int (-\frac{\operatorname{cos}⁡(3x+5)}{3})\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x\operatorname{sin}⁡(3x+5)\text{d}x & =-\frac{x\operatorname{cos}⁡(3x+5)}{3}+\frac{1}{3}\int \operatorname{cos}⁡(3x+5)\text{d}x \\  & =-\frac{x\operatorname{cos}⁡(3x+5)}{3}+\frac{\operatorname{sin}⁡(3x+5)}{9}+C\end{aligned}
$$

---

## Original q-14451 — easy

Field type: radio

$\int 2x\operatorname{sin}⁡(2x)\,\text{d}x=$

- $\frac{x\operatorname{cos}⁡(2x)}{4}-\frac{\operatorname{sin}⁡(2x)}{4}+C$
- $-x\operatorname{cos}⁡(2x)+\frac{\operatorname{sin}⁡(2x)}{2}+C$ **original correct**
- $\frac{\operatorname{cos}⁡(4x)}{4}+\frac{x\operatorname{sin}⁡(4x)}{4}+C$
- $-\frac{x\operatorname{cos}⁡(2x)}{2}+\frac{\operatorname{sin}⁡(2x)}{4}+C$
- $\frac{x\operatorname{cos}⁡(2x)}{4}+\frac{\operatorname{sin}⁡(2x)}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2x\operatorname{sin}⁡(2x)\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}⁡(2x)\, & ⟹\,v=-\frac{\operatorname{cos}⁡(2x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 2x\cdot \operatorname{sin}⁡(2x)\,\text{d}x & =2x\cdot (-\frac{\operatorname{cos}⁡(2x)}{2})-\int (-\frac{\operatorname{cos}⁡(2x)}{2})\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 2x\operatorname{sin}⁡(2x)\,\text{d}x & =-x\operatorname{cos}⁡(2x)+\int \operatorname{cos}⁡(2x)\,\text{d}x \\  & =-x\operatorname{cos}⁡(2x)+\frac{\operatorname{sin}⁡(2x)}{2}+C\end{aligned}
$$

---

## Original-profile parameterized replay q-12564

Level: moderate; template: affine_cos; profile: observed:q-12564; field type: radio

$\int (x + 3)\operatorname{cos}(3 x)\,\text{d}x=$

- $\frac{(x + 3) \operatorname{sin}{(3 x )}}{3}+\frac{\operatorname{cos}{(3 x )}}{9}+C$ **correct**
- $- \frac{\operatorname{sin}{(3 x )}}{3}+\frac{x \operatorname{cos}{(3 x )}}{9}+C$
- $\frac{x \operatorname{sin}{(3 x )}}{9}+\frac{\operatorname{cos}{(3 x )}}{3}+C$
- $\frac{(x + 3) \operatorname{sin}{(3 x )}}{3}- \frac{x \operatorname{cos}{(3 x )}}{3}+C$
- $\frac{(x + 3) \operatorname{sin}{(3 x )}}{9}+\frac{\operatorname{cos}{(3 x )}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x + 3)\operatorname{cos}(3 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x + 3\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{cos}(3 x)\, & ⟹\,v=\frac{\operatorname{sin}(3 x)}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (x + 3)\cdot \operatorname{cos}(3 x)\,\text{d}x= \\ (x + 3)\cdot \frac{\operatorname{sin}(3 x)}{3}-\int \frac{\operatorname{sin}(3 x)}{3}\cdot 1\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (x + 3)\operatorname{cos}(3 x)\,\text{d}x= \\ \frac{(x + 3)\operatorname{sin}(3 x)}{3}-\frac{\int \operatorname{sin}(3 x)\,\text{d}x}{3} \\ =\frac{(x + 3)\operatorname{sin}(3 x)}{3}+\frac{\operatorname{cos}(3 x)}{9}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-12564

Level: moderate; template: affine_cos; profile: observed:q-12564; field type: radio

$\int (3 x + 7)\operatorname{cos}(5 x)\,\text{d}x=$

- $\frac{x \operatorname{sin}{(5 x )}}{25}+\frac{\operatorname{cos}{(5 x )}}{5}+C$
- $\frac{(3 x + 7) \operatorname{sin}{(5 x )}}{5}- \frac{x \operatorname{cos}{(5 x )}}{5}+C$
- $\frac{(3 x + 7) \operatorname{sin}{(5 x )}}{5}+\frac{3 \operatorname{cos}{(5 x )}}{25}+C$ **correct**
- $\frac{(3 x + 7) \operatorname{sin}{(5 x )}}{25}+\frac{\operatorname{cos}{(5 x )}}{5}+C$
- $- \frac{\operatorname{sin}{(5 x )}}{5}+\frac{x \operatorname{cos}{(5 x )}}{25}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ (3 x + 7)\cdot \frac{\operatorname{sin}(5 x)}{5}-\int \frac{\operatorname{sin}(5 x)}{5}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (3 x + 7)\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{(3 x + 7)\operatorname{sin}(5 x)}{5}-\frac{3\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{(3 x + 7)\operatorname{sin}(5 x)}{5}+\frac{3\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-14437

Level: easy; template: sin_unit; profile: observed:q-14437; field type: radio

Calculate $\int 2 x\operatorname{sin}(x)\,\text{d}x.$

- $\operatorname{cos}{(2 x )}+x \operatorname{sin}{(2 x )}+C$
- $2 x \operatorname{cos}{(x )}- x \operatorname{sin}{(x )}+C$
- $- 2 x \operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $- 2 x \operatorname{cos}{(x )}+2 \operatorname{sin}{(x )}+C$ **correct**
- $- x \operatorname{cos}{(x )}- \operatorname{cos}{(2 x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2 x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 2 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 2 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 2\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 2 x\operatorname{sin}(x)\,\text{d}x= \\ -2 x\operatorname{cos}(x)+2\int \operatorname{cos}(x)\,\text{d}x \\ =-2 x\operatorname{cos}(x)+2\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-14437

Level: easy; template: sin_unit; profile: observed:q-14437; field type: radio

Calculate $\int 3 x\operatorname{sin}(x)\,\text{d}x.$

- $\operatorname{cos}{(3 x )}+x \operatorname{sin}{(3 x )}+C$
- $3 x \operatorname{cos}{(x )}- x \operatorname{sin}{(x )}+C$
- $- 3 x \operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $- 3 x \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$ **correct**
- $- x \operatorname{cos}{(x )}- \operatorname{cos}{(3 x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 3 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(x)\,\text{d}x= \\ -3 x\operatorname{cos}(x)+3\int \operatorname{cos}(x)\,\text{d}x \\ =-3 x\operatorname{cos}(x)+3\operatorname{sin}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114297

Level: easy; template: cos_frequency; profile: observed:q-114297; field type: radio

$\int 3 x\operatorname{cos}(3 x)\,\text{d}x=$

- $2 x \operatorname{sin}{(3 x )}+\frac{\operatorname{cos}{(3 x )}}{3}+C$
- $\operatorname{sin}{(3 x )}- \frac{x \operatorname{cos}{(3 x )}}{3}+C$
- $3 \operatorname{sin}{(3 x )}+\frac{x \operatorname{cos}{(3 x )}}{6}+C$
- $\frac{x \operatorname{sin}{(3 x )}}{3}- \frac{\operatorname{cos}{(3 x )}}{9}+C$
- $x \operatorname{sin}{(3 x )}+\frac{\operatorname{cos}{(3 x )}}{3}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(3 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(3 x)\, & ⟹\,v=\frac{\operatorname{sin}(3 x)}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(3 x)\,\text{d}x= \\ 3 x\cdot (\frac{\operatorname{sin}(3 x)}{3})-\int (\frac{\operatorname{sin}(3 x)}{3})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(3 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(3 x)}{3}-\int \operatorname{sin}(3 x)\,\text{d}x \\ =\frac{3 x\operatorname{sin}(3 x)}{3}+\frac{\operatorname{cos}(3 x)}{3}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114297

Level: easy; template: cos_frequency; profile: observed:q-114297; field type: radio

$\int 3 x\operatorname{cos}(5 x)\,\text{d}x=$

- $5 \operatorname{sin}{(5 x )}+\frac{x \operatorname{cos}{(5 x )}}{10}+C$
- $\frac{x \operatorname{sin}{(5 x )}}{5}- \frac{\operatorname{cos}{(5 x )}}{25}+C$
- $\frac{6 x \operatorname{sin}{(5 x )}}{5}+\frac{3 \operatorname{cos}{(5 x )}}{25}+C$
- $\operatorname{sin}{(5 x )}- \frac{x \operatorname{cos}{(5 x )}}{5}+C$
- $\frac{3 x \operatorname{sin}{(5 x )}}{5}+\frac{3 \operatorname{cos}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ 3 x\cdot (\frac{\operatorname{sin}(5 x)}{5})-\int (\frac{\operatorname{sin}(5 x)}{5})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(5 x)}{5}-\frac{3\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{3 x\operatorname{sin}(5 x)}{5}+\frac{3\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114299

Level: easy; template: cos_frequency_expanded; profile: observed:q-114299; field type: radio

Calculate $\int 2 x\operatorname{cos}(4 x)\,\text{d}x.$

- $\frac{x \operatorname{sin}{(4 x )}}{4}- \frac{\operatorname{cos}{(4 x )}}{2}+C$
- $\frac{3 x \operatorname{sin}{(4 x )}}{2}+\frac{\operatorname{cos}{(4 x )}}{4}+C$
- $\frac{x \operatorname{sin}{(4 x )}}{2}+\frac{\operatorname{cos}{(4 x )}}{8}+C$ **correct**
- $- \frac{\operatorname{sin}{(4 x )}}{8}+\frac{x \operatorname{cos}{(4 x )}}{2}+C$
- $- \frac{\operatorname{sin}{(4 x )}}{4}+\frac{x \operatorname{cos}{(4 x )}}{6}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2 x\operatorname{cos}(4 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2 x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{cos}(4 x)\, & ⟹\,v=\frac{\operatorname{sin}(4 x)}{4}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 2 x\cdot \operatorname{cos}(4 x)\,\text{d}x= \\ 2 x\cdot \frac{\operatorname{sin}(4 x)}{4}-\int \frac{\operatorname{sin}(4 x)}{4}\cdot 2\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 2 x\operatorname{cos}(4 x)\,\text{d}x= \\ \frac{2 x\operatorname{sin}(4 x)}{4}-\frac{\int \operatorname{sin}(4 x)\,\text{d}x}{2} \\ =\frac{2 x\operatorname{sin}(4 x)}{4}-\frac{(-\frac{\operatorname{cos}(4 x)}{4})}{2}+C \\ =\frac{2 x\operatorname{sin}(4 x)}{4}+\frac{\operatorname{cos}(4 x)}{8}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114299

Level: easy; template: cos_frequency_expanded; profile: observed:q-114299; field type: radio

Calculate $\int 3 x\operatorname{cos}(5 x)\,\text{d}x.$

- $\frac{3 x \operatorname{sin}{(5 x )}}{5}+\frac{3 \operatorname{cos}{(5 x )}}{25}+C$ **correct**
- $- \frac{\operatorname{sin}{(5 x )}}{10}+\frac{x \operatorname{cos}{(5 x )}}{2}+C$
- $\frac{x \operatorname{sin}{(5 x )}}{5}- \frac{\operatorname{cos}{(5 x )}}{2}+C$
- $2 x \operatorname{sin}{(5 x )}+\frac{\operatorname{cos}{(5 x )}}{5}+C$
- $- \frac{\operatorname{sin}{(5 x )}}{5}+\frac{x \operatorname{cos}{(5 x )}}{8}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ 3 x\cdot \frac{\operatorname{sin}(5 x)}{5}-\int \frac{\operatorname{sin}(5 x)}{5}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(5 x)}{5}-\frac{3\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{3 x\operatorname{sin}(5 x)}{5}-\frac{3(-\frac{\operatorname{cos}(5 x)}{5})}{5}+C \\ =\frac{3 x\operatorname{sin}(5 x)}{5}+\frac{3\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114309

Level: moderate; template: affine_sin; profile: observed:q-114309; field type: radio

$\int (x + 4)\operatorname{sin}(2 x)\,\text{d}x=$

- $\frac{(- x - 4) \operatorname{cos}{(2 x )}}{4}+\frac{\operatorname{sin}{(2 x )}}{8}+C$
- $\frac{(- 3 x - 12) \operatorname{cos}{(2 x )}}{2}+\frac{\operatorname{sin}{(2 x )}}{6}+C$
- $\frac{(- x - 4) \operatorname{cos}{(2 x )}}{2}+\frac{\operatorname{sin}{(2 x )}}{4}+C$ **correct**
- $\frac{(- x - 4) \operatorname{cos}{(2 x )}}{4}- \frac{\operatorname{sin}{(2 x )}}{2}+C$
- $\frac{(- x - 4) \operatorname{cos}{(2 x )}}{6}- \frac{\operatorname{sin}{(2 x )}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x + 4)\operatorname{sin}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x + 4\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{sin}(2 x)\, & ⟹\,v=-\frac{\operatorname{cos}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (x + 4)\cdot \operatorname{sin}(2 x)\,\text{d}x= \\ (x + 4)\cdot (-\frac{\operatorname{cos}(2 x)}{2})-\int (-\frac{\operatorname{cos}(2 x)}{2})\cdot 1\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (x + 4)\operatorname{sin}(2 x)\,\text{d}x= \\ -\frac{(x + 4)\operatorname{cos}(2 x)}{2}+\frac{\int \operatorname{cos}(2 x)\,\text{d}x}{2} \\ =-\frac{(x + 4)\operatorname{cos}(2 x)}{2}+\frac{\operatorname{sin}(2 x)}{4}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114309

Level: moderate; template: affine_sin; profile: observed:q-114309; field type: radio

$\int (3 x + 7)\operatorname{sin}(5 x)\,\text{d}x=$

- $\frac{(- 3 x - 7) \operatorname{cos}{(5 x )}}{5}+\frac{3 \operatorname{sin}{(5 x )}}{25}+C$ **correct**
- $\frac{(- 3 x - 7) \operatorname{cos}{(5 x )}}{10}- \frac{\operatorname{sin}{(5 x )}}{5}+C$
- $\frac{(- 3 x - 7) \operatorname{cos}{(5 x )}}{10}+\frac{\operatorname{sin}{(5 x )}}{50}+C$
- $\frac{(- 3 x - 7) \operatorname{cos}{(5 x )}}{15}- \frac{\operatorname{sin}{(5 x )}}{5}+C$
- $\frac{(- 9 x - 21) \operatorname{cos}{(5 x )}}{5}+\frac{\operatorname{sin}{(5 x )}}{15}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)\operatorname{sin}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(5 x)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot \operatorname{sin}(5 x)\,\text{d}x= \\ (3 x + 7)\cdot (-\frac{\operatorname{cos}(5 x)}{5})-\int (-\frac{\operatorname{cos}(5 x)}{5})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (3 x + 7)\operatorname{sin}(5 x)\,\text{d}x= \\ -\frac{(3 x + 7)\operatorname{cos}(5 x)}{5}+\frac{3\int \operatorname{cos}(5 x)\,\text{d}x}{5} \\ =-\frac{(3 x + 7)\operatorname{cos}(5 x)}{5}+\frac{3\operatorname{sin}(5 x)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114311

Level: moderate; template: affine_sin_unit; profile: observed:q-114311; field type: radio

$\int (2 x + 3)\operatorname{sin}(x)\,\text{d}x=$

- $(2 x + 3) \operatorname{cos}{(x )}- \operatorname{sin}{(x )}+C$
- $x \operatorname{cos}{(x )}- 6 \operatorname{sin}{(x )}+C$
- $(- 2 x - 3) \operatorname{cos}{(x )}+2 \operatorname{sin}{(x )}+C$ **correct**
- $(- 2 x - 3) \operatorname{cos}{(x )}- 4 \operatorname{sin}{(x )}+C$
- $2 x \operatorname{cos}{(x )}+4 \operatorname{sin}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (2 x + 3)\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2 x + 3\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (2 x + 3)\cdot \operatorname{sin}(x)\,\text{d}x= \\ (2 x + 3)\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 2\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (2 x + 3)\operatorname{sin}(x)\,\text{d}x= \\ -(2 x + 3)\operatorname{cos}(x)+2\int \operatorname{cos}(x)\,\text{d}x \\ =-(2 x + 3)\operatorname{cos}(x)+2\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114311

Level: moderate; template: affine_sin_unit; profile: observed:q-114311; field type: radio

$\int (3 x + 7)\operatorname{sin}(x)\,\text{d}x=$

- $(- 3 x - 7) \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$ **correct**
- $(- 3 x - 7) \operatorname{cos}{(x )}- 9 \operatorname{sin}{(x )}+C$
- $(3 x + 7) \operatorname{cos}{(x )}- \operatorname{sin}{(x )}+C$
- $x \operatorname{cos}{(x )}- 21 \operatorname{sin}{(x )}+C$
- $3 x \operatorname{cos}{(x )}+9 \operatorname{sin}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot \operatorname{sin}(x)\,\text{d}x= \\ (3 x + 7)\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (3 x + 7)\operatorname{sin}(x)\,\text{d}x= \\ -(3 x + 7)\operatorname{cos}(x)+3\int \operatorname{cos}(x)\,\text{d}x \\ =-(3 x + 7)\operatorname{cos}(x)+3\operatorname{sin}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114312

Level: easy; template: cos_frequency; profile: observed:q-114312; field type: radio

$\int x\operatorname{cos}(5 x)\,\text{d}x=$

- $\frac{x \operatorname{sin}{(5 x )}}{5}- \frac{2 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{\operatorname{sin}{(5 x )}}{25}+\frac{x \operatorname{cos}{(5 x )}}{5}+C$
- $\frac{x \operatorname{sin}{(5 x )}}{15}+\frac{\operatorname{cos}{(5 x )}}{5}+C$
- $\frac{2 \operatorname{sin}{(5 x )}}{5}- \frac{x \operatorname{cos}{(5 x )}}{15}+C$
- $\frac{x \operatorname{sin}{(5 x )}}{5}+\frac{\operatorname{cos}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ x\cdot (\frac{\operatorname{sin}(5 x)}{5})-\int (\frac{\operatorname{sin}(5 x)}{5})\cdot 1\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{x\operatorname{sin}(5 x)}{5}-\frac{\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{x\operatorname{sin}(5 x)}{5}+\frac{\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114312

Level: easy; template: cos_frequency; profile: observed:q-114312; field type: radio

$\int 3 x\operatorname{cos}(5 x)\,\text{d}x=$

- $\frac{x \operatorname{sin}{(5 x )}}{15}+\frac{\operatorname{cos}{(5 x )}}{5}+C$
- $\frac{2 \operatorname{sin}{(5 x )}}{5}- \frac{x \operatorname{cos}{(5 x )}}{15}+C$
- $\frac{x \operatorname{sin}{(5 x )}}{5}- \frac{2 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{\operatorname{sin}{(5 x )}}{25}+\frac{x \operatorname{cos}{(5 x )}}{5}+C$
- $\frac{3 x \operatorname{sin}{(5 x )}}{5}+\frac{3 \operatorname{cos}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ 3 x\cdot (\frac{\operatorname{sin}(5 x)}{5})-\int (\frac{\operatorname{sin}(5 x)}{5})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(5 x)}{5}-\frac{3\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{3 x\operatorname{sin}(5 x)}{5}+\frac{3\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-114314

Level: hard; template: csc_log; profile: observed:q-114314; field type: radio

Calculate $\int x\operatorname{csc}^{2}(x)\,\text{d}x.$

- $- x \operatorname{cot}{(x )}- 2 \ln{(|{\operatorname{cos}{(x )}}| )}+C$
- $- x \operatorname{cot}{(x )}+\ln{(|{\operatorname{sin}{(x )}}| )}+C$ **correct**
- $x \operatorname{tan}{(x )}- \ln{(|{\operatorname{cos}{(x )}}| )}+C$
- $- 2 x \operatorname{cot}{(x )}- \ln{(|{\operatorname{sin}{(x )}}| )}+C$
- $x \operatorname{tan}{(x )}- 2 \ln{(|{\operatorname{sin}{(x )}}| )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x\operatorname{csc}^{2}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{csc}^{2}(x)\, & ⟹\,v=-\operatorname{cot}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot \operatorname{csc}^{2}(x)\,\text{d}x= \\ x\cdot (-\operatorname{cot}(x))-\int (-\operatorname{cot}(x))\cdot 1\,\text{d}x \\ =-x\operatorname{cot}(x)+\int \frac{\operatorname{cos}(x)}{\operatorname{sin}(x)}\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral using the substitution $u=\operatorname{sin}(x),$ where $\text{d}u=\operatorname{cos}(x)\,\text{d}x,$ as follows:

$$
\begin{gathered}\int x\operatorname{csc}^{2}(x)\,\text{d}x= \\ -x\operatorname{cot}(x)+\int \frac{\operatorname{cos}(x)}{\operatorname{sin}(x)}\,\text{d}x \\ =-x\operatorname{cot}(x)+\int \frac{1}{u}\,\text{d}u \\ =-x\operatorname{cot}(x)+\ln|u|+C \\ =-x\operatorname{cot}(x)+\ln|\operatorname{sin}(x)|+C\end{gathered}
$$

---

## Generated empirical evidence variant q-114314

Level: hard; template: csc_log; profile: observed:q-114314; field type: radio

Calculate $\int 3 x\operatorname{csc}^{2}(x + 6)\,\text{d}x.$

- $3 x \operatorname{tan}{(x + 6 )}- 3 \ln{(|{\operatorname{cos}{(x + 6 )}}| )}+C$
- $- 6 x \operatorname{cot}{(x + 6 )}- 3 \ln{(|{\operatorname{sin}{(x + 6 )}}| )}+C$
- $- 3 x \operatorname{cot}{(x + 6 )}- 6 \ln{(|{\operatorname{cos}{(x + 6 )}}| )}+C$
- $- 3 x \operatorname{cot}{(x + 6 )}+3 \ln{(|{\operatorname{sin}{(x + 6 )}}| )}+C$ **correct**
- $3 x \operatorname{tan}{(x + 6 )}- 6 \ln{(|{\operatorname{sin}{(x + 6 )}}| )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{csc}^{2}(x + 6)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{csc}^{2}(x + 6)\, & ⟹\,v=-\operatorname{cot}(x + 6).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{csc}^{2}(x + 6)\,\text{d}x= \\ 3 x\cdot (-\operatorname{cot}(x + 6))-\int (-\operatorname{cot}(x + 6))\cdot 3\,\text{d}x \\ =-3 x\operatorname{cot}(x + 6)+3\int \frac{\operatorname{cos}(x + 6)}{\operatorname{sin}(x + 6)}\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral using the substitution $u=\operatorname{sin}(x + 6),$ where $\text{d}u=\operatorname{cos}(x + 6)\,\text{d}x,$ as follows:

$$
\begin{gathered}\int 3 x\operatorname{csc}^{2}(x + 6)\,\text{d}x= \\ -3 x\operatorname{cot}(x + 6)+3\int \frac{\operatorname{cos}(x + 6)}{\operatorname{sin}(x + 6)}\,\text{d}x \\ =-3 x\operatorname{cot}(x + 6)+3\int \frac{1}{u}\,\text{d}u \\ =-3 x\operatorname{cot}(x + 6)+3\ln|u|+C \\ =-3 x\operatorname{cot}(x + 6)+3\ln|\operatorname{sin}(x + 6)|+C\end{gathered}
$$

---

## Original-profile parameterized replay q-14449

Level: easy; template: sin_unit; profile: observed:q-14449; field type: radio

Calculate $\int 5 x\operatorname{sin}(x)\,\text{d}x.$

- $- x \operatorname{cos}{(x )}- \operatorname{cos}{(5 x )}+C$
- $- 5 x \operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $\operatorname{cos}{(5 x )}+x \operatorname{sin}{(5 x )}+C$
- $5 x \operatorname{cos}{(x )}- x \operatorname{sin}{(x )}+C$
- $- 5 x \operatorname{cos}{(x )}+5 \operatorname{sin}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 5 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=5 x\, & ⟹\,{u}^{′}=5 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 5 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 5 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 5\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 5 x\operatorname{sin}(x)\,\text{d}x= \\ -5 x\operatorname{cos}(x)+5\int \operatorname{cos}(x)\,\text{d}x \\ =-5 x\operatorname{cos}(x)+5\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-14449

Level: easy; template: sin_unit; profile: observed:q-14449; field type: radio

Calculate $\int 3 x\operatorname{sin}(x)\,\text{d}x.$

- $- x \operatorname{cos}{(x )}- \operatorname{cos}{(3 x )}+C$
- $- 3 x \operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $\operatorname{cos}{(3 x )}+x \operatorname{sin}{(3 x )}+C$
- $3 x \operatorname{cos}{(x )}- x \operatorname{sin}{(x )}+C$
- $- 3 x \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 3 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(x)\,\text{d}x= \\ -3 x\operatorname{cos}(x)+3\int \operatorname{cos}(x)\,\text{d}x \\ =-3 x\operatorname{cos}(x)+3\operatorname{sin}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-14453

Level: easy; template: cos_unit_expanded; profile: observed:q-14453; field type: radio

$\int 6 x\operatorname{cos}(x)\,\text{d}x=$

- $x \operatorname{cos}{(6 x )}- x \operatorname{sin}{(6 x )}+C$
- $x \operatorname{cos}{(6 x )}+x \operatorname{sin}{(6 x )}+C$
- $- 6 x \operatorname{sin}{(x )}+6 \operatorname{cos}{(x )}+C$
- $6 x \operatorname{sin}{(x )}+6 \operatorname{cos}{(x )}+C$ **correct**
- $- 6 x \operatorname{cos}{(x )}- \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6 x\, & ⟹\,{u}^{′}=6 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 6 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 6 x\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 6\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 6 x\operatorname{cos}(x)\,\text{d}x= \\ 6 x\operatorname{sin}(x)-6\int \operatorname{sin}(x)\,\text{d}x \\ =6 x\operatorname{sin}(x)-6(-\operatorname{cos}(x))+C \\ =6 x\operatorname{sin}(x)+6\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-14453

Level: easy; template: cos_unit_expanded; profile: observed:q-14453; field type: radio

$\int 3 x\operatorname{cos}(x)\,\text{d}x=$

- $x \operatorname{cos}{(3 x )}- x \operatorname{sin}{(3 x )}+C$
- $x \operatorname{cos}{(3 x )}+x \operatorname{sin}{(3 x )}+C$
- $- 3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$
- $3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**
- $- 3 x \operatorname{cos}{(x )}- \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 3 x\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(x)\,\text{d}x= \\ 3 x\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =3 x\operatorname{sin}(x)-3(-\operatorname{cos}(x))+C \\ =3 x\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-74087

Level: moderate; template: phase_cos; profile: observed:q-74087; field type: radio

Calculate  $\int 2 x\operatorname{cos}(2 x + 8)\,\text{d}x.$

- $2 x \operatorname{sin}{(2 x + 8 )}- \frac{\operatorname{cos}{(2 x + 8 )}}{4}+C$
- $x \operatorname{sin}{(2 x + 8 )}+\frac{\operatorname{cos}{(2 x + 8 )}}{2}+C$ **correct**
- $2 x \operatorname{sin}{(2 x + 8 )}+\operatorname{cos}{(2 x + 8 )}+C$
- $x \operatorname{sin}{(2 x + 8 )}- \operatorname{cos}{(2 x + 8 )}+C$
- $2 x \operatorname{sin}{(2 x + 8 )}+\frac{\operatorname{cos}{(2 x + 8 )}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2 x\operatorname{cos}(2 x + 8)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2 x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{cos}(2 x + 8)\, & ⟹\,v=\frac{\operatorname{sin}(2 x + 8)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 2 x\cdot \operatorname{cos}(2 x + 8)\,\text{d}x= \\ 2 x\cdot \frac{\operatorname{sin}(2 x + 8)}{2}-\int \frac{\operatorname{sin}(2 x + 8)}{2}\cdot 2\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 2 x\operatorname{cos}(2 x + 8)\,\text{d}x= \\ \frac{2 x\operatorname{sin}(2 x + 8)}{2}-\int \operatorname{sin}(2 x + 8)\,\text{d}x \\ =\frac{2 x\operatorname{sin}(2 x + 8)}{2}+\frac{\operatorname{cos}(2 x + 8)}{2}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-74087

Level: moderate; template: phase_cos; profile: observed:q-74087; field type: radio

Calculate  $\int 3 x\operatorname{cos}(5 x + 7)\,\text{d}x.$

- $3 x \operatorname{sin}{(5 x + 7 )}+\operatorname{cos}{(5 x + 7 )}+C$
- $\frac{3 x \operatorname{sin}{(5 x + 7 )}}{5}- \operatorname{cos}{(5 x + 7 )}+C$
- $3 x \operatorname{sin}{(5 x + 7 )}- \frac{\operatorname{cos}{(5 x + 7 )}}{25}+C$
- $3 x \operatorname{sin}{(5 x + 7 )}+\frac{\operatorname{cos}{(5 x + 7 )}}{5}+C$
- $\frac{3 x \operatorname{sin}{(5 x + 7 )}}{5}+\frac{3 \operatorname{cos}{(5 x + 7 )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(5 x + 7)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(5 x + 7)\, & ⟹\,v=\frac{\operatorname{sin}(5 x + 7)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(5 x + 7)\,\text{d}x= \\ 3 x\cdot \frac{\operatorname{sin}(5 x + 7)}{5}-\int \frac{\operatorname{sin}(5 x + 7)}{5}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(5 x + 7)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(5 x + 7)}{5}-\frac{3\int \operatorname{sin}(5 x + 7)\,\text{d}x}{5} \\ =\frac{3 x\operatorname{sin}(5 x + 7)}{5}+\frac{3\operatorname{cos}(5 x + 7)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-74088

Level: moderate; template: affine_cos_unit; profile: observed:q-74088; field type: radio

$\int (6 x + 1)\operatorname{cos}(x)\,\text{d}x=$

- $6 \operatorname{sin}{(x )}+6 \operatorname{cos}{(x )}+C$
- $(6 x + 1) \operatorname{sin}{(x )}+\frac{\operatorname{cos}{(x )}}{6}+C$
- $\operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $\frac{(6 x + 1) \operatorname{sin}{(x )}}{6}+\operatorname{cos}{(x )}+C$
- $(6 x + 1) \operatorname{sin}{(x )}+6 \operatorname{cos}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (6 x + 1)\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6 x + 1\, & ⟹\,{u}^{′}=6 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (6 x + 1)\cdot \operatorname{cos}(x)\,\text{d}x= \\ (6 x + 1)\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 6\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (6 x + 1)\operatorname{cos}(x)\,\text{d}x= \\ (6 x + 1)\operatorname{sin}(x)-6\int \operatorname{sin}(x)\,\text{d}x \\ =(6 x + 1)\operatorname{sin}(x)+6\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-74088

Level: moderate; template: affine_cos_unit; profile: observed:q-74088; field type: radio

$\int (3 x + 7)\operatorname{cos}(x)\,\text{d}x=$

- $\operatorname{sin}{(x )}+\operatorname{cos}{(x )}+C$
- $\frac{(3 x + 7) \operatorname{sin}{(x )}}{3}+\operatorname{cos}{(x )}+C$
- $3 \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$
- $(3 x + 7) \operatorname{sin}{(x )}+\frac{\operatorname{cos}{(x )}}{3}+C$
- $(3 x + 7) \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot \operatorname{cos}(x)\,\text{d}x= \\ (3 x + 7)\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (3 x + 7)\operatorname{cos}(x)\,\text{d}x= \\ (3 x + 7)\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =(3 x + 7)\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-74090

Level: easy; template: cos_unit; profile: observed:q-74090; field type: radio

Calculate $\int 10 x\operatorname{cos}(x)\,\text{d}x.$

- $10 x \operatorname{sin}{(x )}+10 \operatorname{cos}{(x )}+C$ **correct**
- $10 x \operatorname{sin}{(x )}+\frac{\operatorname{cos}{(x )}}{10}+C$
- $\frac{x \operatorname{sin}{(x )}}{10}- \operatorname{cos}{(x )}+C$
- $10 \operatorname{sin}{(x )}- \operatorname{cos}{(x )}+C$
- $10 \operatorname{sin}{(x )}- 10 x \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 10 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=10 x\, & ⟹\,{u}^{′}=10 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 10 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 10 x\cdot (\operatorname{sin}(x))-\int (\operatorname{sin}(x))\cdot 10\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 10 x\operatorname{cos}(x)\,\text{d}x= \\ 10 x\operatorname{sin}(x)-10\int \operatorname{sin}(x)\,\text{d}x \\ =10 x\operatorname{sin}(x)+10\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated empirical evidence variant q-74090

Level: easy; template: cos_unit; profile: observed:q-74090; field type: radio

Calculate $\int 3 x\operatorname{cos}(x)\,\text{d}x.$

- $3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**
- $3 x \operatorname{sin}{(x )}+\frac{\operatorname{cos}{(x )}}{3}+C$
- $\frac{x \operatorname{sin}{(x )}}{3}- \operatorname{cos}{(x )}+C$
- $3 \operatorname{sin}{(x )}- \operatorname{cos}{(x )}+C$
- $3 \operatorname{sin}{(x )}- 3 x \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 3 x\cdot (\operatorname{sin}(x))-\int (\operatorname{sin}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(x)\,\text{d}x= \\ 3 x\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =3 x\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Original-profile parameterized replay q-12565

Level: moderate; template: phase_sin; profile: observed:q-12565; field type: radio

Calculate  $\int x\operatorname{sin}(3 x + 5)\,\text{d}x.$

- $- \frac{x \operatorname{cos}{(3 x + 5 )}}{3}+\frac{\operatorname{sin}{(3 x + 5 )}}{9}+C$ **correct**
- $\frac{\operatorname{cos}{(3 x + 5 )}}{3}+\frac{x \operatorname{sin}{(3 x + 5 )}}{9}+C$
- $- x \operatorname{cos}{(x + 5 )}+\frac{\operatorname{sin}{(x + 5 )}}{3}+C$
- $\frac{x \operatorname{cos}{(3 x + 5 )}}{9}+\frac{2 \operatorname{sin}{(3 x + 5 )}}{9}+C$
- $\frac{x \operatorname{cos}{(3 x + 5 )}}{9}- \frac{\operatorname{sin}{(3 x + 5 )}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x\operatorname{sin}(3 x + 5)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}=\operatorname{sin}(3 x + 5)\, & ⟹\,v=-\frac{\operatorname{cos}(3 x + 5)}{3}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot \operatorname{sin}(3 x + 5)\,\text{d}x= \\ x\cdot (-\frac{\operatorname{cos}(3 x + 5)}{3})-\int (-\frac{\operatorname{cos}(3 x + 5)}{3})\cdot 1\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int x\operatorname{sin}(3 x + 5)\,\text{d}x= \\ -\frac{x\operatorname{cos}(3 x + 5)}{3}+\frac{\int \operatorname{cos}(3 x + 5)\,\text{d}x}{3} \\ =-\frac{x\operatorname{cos}(3 x + 5)}{3}+\frac{\operatorname{sin}(3 x + 5)}{9}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-12565

Level: moderate; template: phase_sin; profile: observed:q-12565; field type: radio

Calculate  $\int 3 x\operatorname{sin}(5 x + 7)\,\text{d}x.$

- $- x \operatorname{cos}{(x + 7 )}+\frac{\operatorname{sin}{(x + 7 )}}{5}+C$
- $\frac{x \operatorname{cos}{(5 x + 7 )}}{25}+\frac{2 \operatorname{sin}{(5 x + 7 )}}{25}+C$
- $- \frac{3 x \operatorname{cos}{(5 x + 7 )}}{5}+\frac{3 \operatorname{sin}{(5 x + 7 )}}{25}+C$ **correct**
- $\frac{x \operatorname{cos}{(5 x + 7 )}}{25}- \frac{\operatorname{sin}{(5 x + 7 )}}{5}+C$
- $\frac{\operatorname{cos}{(5 x + 7 )}}{5}+\frac{x \operatorname{sin}{(5 x + 7 )}}{25}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(5 x + 7)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(5 x + 7)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x + 7)}{5}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(5 x + 7)\,\text{d}x= \\ 3 x\cdot (-\frac{\operatorname{cos}(5 x + 7)}{5})-\int (-\frac{\operatorname{cos}(5 x + 7)}{5})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(5 x + 7)\,\text{d}x= \\ -\frac{3 x\operatorname{cos}(5 x + 7)}{5}+\frac{3\int \operatorname{cos}(5 x + 7)\,\text{d}x}{5} \\ =-\frac{3 x\operatorname{cos}(5 x + 7)}{5}+\frac{3\operatorname{sin}(5 x + 7)}{25}+C\end{gathered}
$$

---

## Original-profile parameterized replay q-14451

Level: easy; template: sin_frequency; profile: observed:q-14451; field type: radio

$\int 2 x\operatorname{sin}(2 x)\,\text{d}x=$

- $\frac{\operatorname{cos}{(4 x )}}{4}+\frac{x \operatorname{sin}{(4 x )}}{4}+C$
- $- x \operatorname{cos}{(2 x )}+\frac{\operatorname{sin}{(2 x )}}{2}+C$ **correct**
- $\frac{x \operatorname{cos}{(2 x )}}{4}- \frac{\operatorname{sin}{(2 x )}}{4}+C$
- $\frac{x \operatorname{cos}{(2 x )}}{4}+\frac{\operatorname{sin}{(2 x )}}{2}+C$
- $- \frac{x \operatorname{cos}{(2 x )}}{2}+\frac{\operatorname{sin}{(2 x )}}{4}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 2 x\operatorname{sin}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2 x\, & ⟹\,{u}^{′}=2 \\ {v}^{′}=\operatorname{sin}(2 x)\, & ⟹\,v=-\frac{\operatorname{cos}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 2 x\cdot \operatorname{sin}(2 x)\,\text{d}x= \\ 2 x\cdot (-\frac{\operatorname{cos}(2 x)}{2})-\int (-\frac{\operatorname{cos}(2 x)}{2})\cdot 2\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 2 x\operatorname{sin}(2 x)\,\text{d}x= \\ -\frac{2 x\operatorname{cos}(2 x)}{2}+\int \operatorname{cos}(2 x)\,\text{d}x \\ =-\frac{2 x\operatorname{cos}(2 x)}{2}+\frac{\operatorname{sin}(2 x)}{2}+C\end{gathered}
$$

---

## Generated empirical evidence variant q-14451

Level: easy; template: sin_frequency; profile: observed:q-14451; field type: radio

$\int 3 x\operatorname{sin}(5 x)\,\text{d}x=$

- $\frac{x \operatorname{cos}{(5 x )}}{25}- \frac{\operatorname{sin}{(5 x )}}{25}+C$
- $\frac{x \operatorname{cos}{(5 x )}}{25}+\frac{\operatorname{sin}{(5 x )}}{5}+C$
- $\frac{\operatorname{cos}{(15 x )}}{25}+\frac{x \operatorname{sin}{(15 x )}}{25}+C$
- $- \frac{3 x \operatorname{cos}{(5 x )}}{5}+\frac{3 \operatorname{sin}{(5 x )}}{25}+C$ **correct**
- $- \frac{x \operatorname{cos}{(5 x )}}{5}+\frac{\operatorname{sin}{(5 x )}}{25}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(5 x)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(5 x)\,\text{d}x= \\ 3 x\cdot (-\frac{\operatorname{cos}(5 x)}{5})-\int (-\frac{\operatorname{cos}(5 x)}{5})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(5 x)\,\text{d}x= \\ -\frac{3 x\operatorname{cos}(5 x)}{5}+\frac{3\int \operatorname{cos}(5 x)\,\text{d}x}{5} \\ =-\frac{3 x\operatorname{cos}(5 x)}{5}+\frac{3\operatorname{sin}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal sin_unit/0

Level: easy; template: sin_unit; profile: authored:parts-errors; field type: radio

Calculate $\int 7 x\operatorname{sin}(x)\,\text{d}x.$

- $- 7 x \operatorname{cos}{(x )}+7 x \operatorname{sin}{(x )}+C$
- $- 7 x \operatorname{cos}{(x )}+0+C$
- $- 7 x \operatorname{cos}{(x )}- 7 \operatorname{sin}{(x )}+C$
- $- 7 x \operatorname{cos}{(x )}+7 \operatorname{sin}{(x )}+C$ **correct**
- $7 x \operatorname{cos}{(x )}+7 \operatorname{sin}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 7 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{sin}(x)\,\text{d}x= \\ -7 x\operatorname{cos}(x)+7\int \operatorname{cos}(x)\,\text{d}x \\ =-7 x\operatorname{cos}(x)+7\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated normal sin_unit/1

Level: easy; template: sin_unit; profile: authored:parts-errors; field type: radio

Calculate $\int 3 x\operatorname{sin}(x)\,\text{d}x.$

- $- 3 x \operatorname{cos}{(x )}+0+C$
- $3 x \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$
- $- 3 x \operatorname{cos}{(x )}- 3 \operatorname{sin}{(x )}+C$
- $- 3 x \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$ **correct**
- $- 3 x \operatorname{cos}{(x )}+3 x \operatorname{sin}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(x)\,\text{d}x= \\ 3 x\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(x)\,\text{d}x= \\ -3 x\operatorname{cos}(x)+3\int \operatorname{cos}(x)\,\text{d}x \\ =-3 x\operatorname{cos}(x)+3\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated normal cos_frequency/0

Level: easy; template: cos_frequency; profile: authored:parts-errors; field type: radio

$\int 7 x\operatorname{cos}(5 x)\,\text{d}x=$

- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 x \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}- \frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $- \frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+0+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ 7 x\cdot (\frac{\operatorname{sin}(5 x)}{5})-\int (\frac{\operatorname{sin}(5 x)}{5})\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{7 x\operatorname{sin}(5 x)}{5}-\frac{7\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{7 x\operatorname{sin}(5 x)}{5}+\frac{7\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal cos_frequency/1

Level: easy; template: cos_frequency; profile: authored:parts-errors; field type: radio

$\int 3 x\operatorname{cos}(2 x)\,\text{d}x=$

- $- \frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 x \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}- \frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$ **correct**
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(2 x)\, & ⟹\,v=\frac{\operatorname{sin}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(2 x)\,\text{d}x= \\ 3 x\cdot (\frac{\operatorname{sin}(2 x)}{2})-\int (\frac{\operatorname{sin}(2 x)}{2})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(2 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(2 x)}{2}-\frac{3\int \operatorname{sin}(2 x)\,\text{d}x}{2} \\ =\frac{3 x\operatorname{sin}(2 x)}{2}+\frac{3\operatorname{cos}(2 x)}{4}+C\end{gathered}
$$

---

## Generated normal cos_frequency_expanded/0

Level: easy; template: cos_frequency_expanded; profile: authored:parts-errors; field type: radio

Calculate $\int 7 x\operatorname{cos}(5 x)\,\text{d}x.$

- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 x \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}- \frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $- \frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+0+C$
- $\frac{7 x \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ 7 x\cdot \frac{\operatorname{sin}(5 x)}{5}-\int \frac{\operatorname{sin}(5 x)}{5}\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{7 x\operatorname{sin}(5 x)}{5}-\frac{7\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{7 x\operatorname{sin}(5 x)}{5}-\frac{7(-\frac{\operatorname{cos}(5 x)}{5})}{5}+C \\ =\frac{7 x\operatorname{sin}(5 x)}{5}+\frac{7\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal cos_frequency_expanded/1

Level: easy; template: cos_frequency_expanded; profile: authored:parts-errors; field type: radio

Calculate $\int 3 x\operatorname{cos}(2 x)\,\text{d}x.$

- $- \frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 x \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}- \frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$ **correct**
- $\frac{3 x \operatorname{sin}{(2 x )}}{2}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(2 x)\, & ⟹\,v=\frac{\operatorname{sin}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(2 x)\,\text{d}x= \\ 3 x\cdot \frac{\operatorname{sin}(2 x)}{2}-\int \frac{\operatorname{sin}(2 x)}{2}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(2 x)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(2 x)}{2}-\frac{3\int \operatorname{sin}(2 x)\,\text{d}x}{2} \\ =\frac{3 x\operatorname{sin}(2 x)}{2}-\frac{3(-\frac{\operatorname{cos}(2 x)}{2})}{2}+C \\ =\frac{3 x\operatorname{sin}(2 x)}{2}+\frac{3\operatorname{cos}(2 x)}{4}+C\end{gathered}
$$

---

## Generated normal cos_unit_expanded/0

Level: easy; template: cos_unit_expanded; profile: authored:parts-errors; field type: radio

$\int 7 x\operatorname{cos}(x)\,\text{d}x=$

- $7 x \operatorname{sin}{(x )}+7 x \operatorname{cos}{(x )}+C$
- $7 x \operatorname{sin}{(x )}+0+C$
- $7 x \operatorname{sin}{(x )}- 7 \operatorname{cos}{(x )}+C$
- $7 x \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$ **correct**
- $- 7 x \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 7 x\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{cos}(x)\,\text{d}x= \\ 7 x\operatorname{sin}(x)-7\int \operatorname{sin}(x)\,\text{d}x \\ =7 x\operatorname{sin}(x)-7(-\operatorname{cos}(x))+C \\ =7 x\operatorname{sin}(x)+7\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal cos_unit_expanded/1

Level: easy; template: cos_unit_expanded; profile: authored:parts-errors; field type: radio

$\int 3 x\operatorname{cos}(x)\,\text{d}x=$

- $3 x \operatorname{sin}{(x )}+0+C$
- $- 3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$
- $3 x \operatorname{sin}{(x )}- 3 \operatorname{cos}{(x )}+C$
- $3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**
- $3 x \operatorname{sin}{(x )}+3 x \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 3 x\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(x)\,\text{d}x= \\ 3 x\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =3 x\operatorname{sin}(x)-3(-\operatorname{cos}(x))+C \\ =3 x\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal cos_unit/0

Level: easy; template: cos_unit; profile: authored:parts-errors; field type: radio

Calculate $\int 7 x\operatorname{cos}(x)\,\text{d}x.$

- $7 x \operatorname{sin}{(x )}+7 x \operatorname{cos}{(x )}+C$
- $7 x \operatorname{sin}{(x )}+0+C$
- $7 x \operatorname{sin}{(x )}- 7 \operatorname{cos}{(x )}+C$
- $7 x \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$ **correct**
- $- 7 x \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 7 x\cdot (\operatorname{sin}(x))-\int (\operatorname{sin}(x))\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{cos}(x)\,\text{d}x= \\ 7 x\operatorname{sin}(x)-7\int \operatorname{sin}(x)\,\text{d}x \\ =7 x\operatorname{sin}(x)+7\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal cos_unit/1

Level: easy; template: cos_unit; profile: authored:parts-errors; field type: radio

Calculate $\int 3 x\operatorname{cos}(x)\,\text{d}x.$

- $3 x \operatorname{sin}{(x )}+0+C$
- $- 3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$
- $3 x \operatorname{sin}{(x )}- 3 \operatorname{cos}{(x )}+C$
- $3 x \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**
- $3 x \operatorname{sin}{(x )}+3 x \operatorname{cos}{(x )}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(x)\,\text{d}x= \\ 3 x\cdot (\operatorname{sin}(x))-\int (\operatorname{sin}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(x)\,\text{d}x= \\ 3 x\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =3 x\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal sin_frequency/0

Level: easy; template: sin_frequency; profile: authored:parts-errors; field type: radio

$\int 7 x\operatorname{sin}(5 x)\,\text{d}x=$

- $- \frac{7 x \operatorname{cos}{(5 x )}}{5}+\frac{7 x \operatorname{sin}{(5 x )}}{25}+C$
- $- \frac{7 x \operatorname{cos}{(5 x )}}{5}- \frac{7 \operatorname{sin}{(5 x )}}{25}+C$
- $\frac{7 x \operatorname{cos}{(5 x )}}{5}+\frac{7 \operatorname{sin}{(5 x )}}{25}+C$
- $- \frac{7 x \operatorname{cos}{(5 x )}}{5}+0+C$
- $- \frac{7 x \operatorname{cos}{(5 x )}}{5}+\frac{7 \operatorname{sin}{(5 x )}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{sin}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{sin}(5 x)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{sin}(5 x)\,\text{d}x= \\ 7 x\cdot (-\frac{\operatorname{cos}(5 x)}{5})-\int (-\frac{\operatorname{cos}(5 x)}{5})\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{sin}(5 x)\,\text{d}x= \\ -\frac{7 x\operatorname{cos}(5 x)}{5}+\frac{7\int \operatorname{cos}(5 x)\,\text{d}x}{5} \\ =-\frac{7 x\operatorname{cos}(5 x)}{5}+\frac{7\operatorname{sin}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal sin_frequency/1

Level: easy; template: sin_frequency; profile: authored:parts-errors; field type: radio

$\int 3 x\operatorname{sin}(2 x)\,\text{d}x=$

- $\frac{3 x \operatorname{cos}{(2 x )}}{2}+\frac{3 \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{3 x \operatorname{cos}{(2 x )}}{2}+\frac{3 x \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{3 x \operatorname{cos}{(2 x )}}{2}- \frac{3 \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{3 x \operatorname{cos}{(2 x )}}{2}+\frac{3 \operatorname{sin}{(2 x )}}{4}+C$ **correct**
- $- \frac{3 x \operatorname{cos}{(2 x )}}{2}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(2 x)\, & ⟹\,v=-\frac{\operatorname{cos}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(2 x)\,\text{d}x= \\ 3 x\cdot (-\frac{\operatorname{cos}(2 x)}{2})-\int (-\frac{\operatorname{cos}(2 x)}{2})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(2 x)\,\text{d}x= \\ -\frac{3 x\operatorname{cos}(2 x)}{2}+\frac{3\int \operatorname{cos}(2 x)\,\text{d}x}{2} \\ =-\frac{3 x\operatorname{cos}(2 x)}{2}+\frac{3\operatorname{sin}(2 x)}{4}+C\end{gathered}
$$

---

## Generated normal affine_cos/0

Level: moderate; template: affine_cos; profile: authored:parts-errors; field type: radio

$\int (7 x - 7)\operatorname{cos}(5 x)\,\text{d}x=$

- $\frac{(7 x - 7) \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$ **correct**
- $\frac{(7 x - 7) \operatorname{sin}{(5 x )}}{5}+\frac{(7 x - 7) \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{(7 x - 7) \operatorname{sin}{(5 x )}}{5}- \frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{(7 - 7 x) \operatorname{sin}{(5 x )}}{5}+\frac{7 \operatorname{cos}{(5 x )}}{25}+C$
- $\frac{(7 x - 7) \operatorname{sin}{(5 x )}}{5}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)\operatorname{cos}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(5 x)\, & ⟹\,v=\frac{\operatorname{sin}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot \operatorname{cos}(5 x)\,\text{d}x= \\ (7 x - 7)\cdot \frac{\operatorname{sin}(5 x)}{5}-\int \frac{\operatorname{sin}(5 x)}{5}\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (7 x - 7)\operatorname{cos}(5 x)\,\text{d}x= \\ \frac{(7 x - 7)\operatorname{sin}(5 x)}{5}-\frac{7\int \operatorname{sin}(5 x)\,\text{d}x}{5} \\ =\frac{(7 x - 7)\operatorname{sin}(5 x)}{5}+\frac{7\operatorname{cos}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal affine_cos/1

Level: moderate; template: affine_cos; profile: authored:parts-errors; field type: radio

$\int (3 x + 1)\operatorname{cos}(2 x)\,\text{d}x=$

- $\frac{(3 x + 1) \operatorname{sin}{(2 x )}}{2}+\frac{(3 x + 1) \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{(3 x + 1) \operatorname{sin}{(2 x )}}{2}+0+C$
- $\frac{(3 x + 1) \operatorname{sin}{(2 x )}}{2}- \frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{(- 3 x - 1) \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$
- $\frac{(3 x + 1) \operatorname{sin}{(2 x )}}{2}+\frac{3 \operatorname{cos}{(2 x )}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)\operatorname{cos}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(2 x)\, & ⟹\,v=\frac{\operatorname{sin}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot \operatorname{cos}(2 x)\,\text{d}x= \\ (3 x + 1)\cdot \frac{\operatorname{sin}(2 x)}{2}-\int \frac{\operatorname{sin}(2 x)}{2}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (3 x + 1)\operatorname{cos}(2 x)\,\text{d}x= \\ \frac{(3 x + 1)\operatorname{sin}(2 x)}{2}-\frac{3\int \operatorname{sin}(2 x)\,\text{d}x}{2} \\ =\frac{(3 x + 1)\operatorname{sin}(2 x)}{2}+\frac{3\operatorname{cos}(2 x)}{4}+C\end{gathered}
$$

---

## Generated normal affine_sin/0

Level: moderate; template: affine_sin; profile: authored:parts-errors; field type: radio

$\int (7 x - 7)\operatorname{sin}(5 x)\,\text{d}x=$

- $- \frac{(7 x - 7) \operatorname{cos}{(5 x )}}{5}+\frac{7 \operatorname{sin}{(5 x )}}{25}+C$ **correct**
- $- \frac{(7 x - 7) \operatorname{cos}{(5 x )}}{5}+\frac{(7 x - 7) \operatorname{sin}{(5 x )}}{25}+C$
- $- \frac{(7 x - 7) \operatorname{cos}{(5 x )}}{5}- \frac{7 \operatorname{sin}{(5 x )}}{25}+C$
- $- \frac{(7 - 7 x) \operatorname{cos}{(5 x )}}{5}+\frac{7 \operatorname{sin}{(5 x )}}{25}+C$
- $- \frac{(7 x - 7) \operatorname{cos}{(5 x )}}{5}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)\operatorname{sin}(5 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{sin}(5 x)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot \operatorname{sin}(5 x)\,\text{d}x= \\ (7 x - 7)\cdot (-\frac{\operatorname{cos}(5 x)}{5})-\int (-\frac{\operatorname{cos}(5 x)}{5})\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (7 x - 7)\operatorname{sin}(5 x)\,\text{d}x= \\ -\frac{(7 x - 7)\operatorname{cos}(5 x)}{5}+\frac{7\int \operatorname{cos}(5 x)\,\text{d}x}{5} \\ =-\frac{(7 x - 7)\operatorname{cos}(5 x)}{5}+\frac{7\operatorname{sin}(5 x)}{25}+C\end{gathered}
$$

---

## Generated normal affine_sin/1

Level: moderate; template: affine_sin; profile: authored:parts-errors; field type: radio

$\int (3 x + 1)\operatorname{sin}(2 x)\,\text{d}x=$

- $- \frac{(3 x + 1) \operatorname{cos}{(2 x )}}{2}+\frac{(3 x + 1) \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{(3 x + 1) \operatorname{cos}{(2 x )}}{2}+0+C$
- $- \frac{(3 x + 1) \operatorname{cos}{(2 x )}}{2}- \frac{3 \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{(- 3 x - 1) \operatorname{cos}{(2 x )}}{2}+\frac{3 \operatorname{sin}{(2 x )}}{4}+C$
- $- \frac{(3 x + 1) \operatorname{cos}{(2 x )}}{2}+\frac{3 \operatorname{sin}{(2 x )}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)\operatorname{sin}(2 x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(2 x)\, & ⟹\,v=-\frac{\operatorname{cos}(2 x)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot \operatorname{sin}(2 x)\,\text{d}x= \\ (3 x + 1)\cdot (-\frac{\operatorname{cos}(2 x)}{2})-\int (-\frac{\operatorname{cos}(2 x)}{2})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int (3 x + 1)\operatorname{sin}(2 x)\,\text{d}x= \\ -\frac{(3 x + 1)\operatorname{cos}(2 x)}{2}+\frac{3\int \operatorname{cos}(2 x)\,\text{d}x}{2} \\ =-\frac{(3 x + 1)\operatorname{cos}(2 x)}{2}+\frac{3\operatorname{sin}(2 x)}{4}+C\end{gathered}
$$

---

## Generated normal affine_sin_unit/0

Level: moderate; template: affine_sin_unit; profile: authored:parts-errors; field type: radio

$\int (7 x + 6)\operatorname{sin}(x)\,\text{d}x=$

- $- (7 x + 6) \operatorname{cos}{(x )}+(7 x + 6) \operatorname{sin}{(x )}+C$
- $- (7 x + 6) \operatorname{cos}{(x )}- 7 \operatorname{sin}{(x )}+C$
- $- (- 7 x - 6) \operatorname{cos}{(x )}+7 \operatorname{sin}{(x )}+C$
- $- (7 x + 6) \operatorname{cos}{(x )}+0+C$
- $- (7 x + 6) \operatorname{cos}{(x )}+7 \operatorname{sin}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x + 6)\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x + 6\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x + 6)\cdot \operatorname{sin}(x)\,\text{d}x= \\ (7 x + 6)\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (7 x + 6)\operatorname{sin}(x)\,\text{d}x= \\ -(7 x + 6)\operatorname{cos}(x)+7\int \operatorname{cos}(x)\,\text{d}x \\ =-(7 x + 6)\operatorname{cos}(x)+7\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated normal affine_sin_unit/1

Level: moderate; template: affine_sin_unit; profile: authored:parts-errors; field type: radio

$\int (3 x - 6)\operatorname{sin}(x)\,\text{d}x=$

- $- (6 - 3 x) \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$
- $- (3 x - 6) \operatorname{cos}{(x )}+(3 x - 6) \operatorname{sin}{(x )}+C$
- $- (3 x - 6) \operatorname{cos}{(x )}- 3 \operatorname{sin}{(x )}+C$
- $- (3 x - 6) \operatorname{cos}{(x )}+3 \operatorname{sin}{(x )}+C$ **correct**
- $- (3 x - 6) \operatorname{cos}{(x )}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x - 6)\operatorname{sin}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x - 6\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(x)\, & ⟹\,v=-\operatorname{cos}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x - 6)\cdot \operatorname{sin}(x)\,\text{d}x= \\ (3 x - 6)\cdot (-\operatorname{cos}(x))-\int (-\operatorname{cos}(x))\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (3 x - 6)\operatorname{sin}(x)\,\text{d}x= \\ -(3 x - 6)\operatorname{cos}(x)+3\int \operatorname{cos}(x)\,\text{d}x \\ =-(3 x - 6)\operatorname{cos}(x)+3\operatorname{sin}(x)+C\end{gathered}
$$

---

## Generated normal phase_cos/0

Level: moderate; template: phase_cos; profile: authored:parts-errors; field type: radio

Calculate  $\int 7 x\operatorname{cos}(5 x - 7)\,\text{d}x.$

- $\frac{7 x \operatorname{sin}{(5 x - 7 )}}{5}+\frac{7 \operatorname{cos}{(5 x - 7 )}}{25}+C$ **correct**
- $\frac{7 x \operatorname{sin}{(5 x - 7 )}}{5}+\frac{7 x \operatorname{cos}{(5 x - 7 )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x - 7 )}}{5}- \frac{7 \operatorname{cos}{(5 x - 7 )}}{25}+C$
- $- \frac{7 x \operatorname{sin}{(5 x - 7 )}}{5}+\frac{7 \operatorname{cos}{(5 x - 7 )}}{25}+C$
- $\frac{7 x \operatorname{sin}{(5 x - 7 )}}{5}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{cos}(5 x - 7)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(5 x - 7)\, & ⟹\,v=\frac{\operatorname{sin}(5 x - 7)}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{cos}(5 x - 7)\,\text{d}x= \\ 7 x\cdot \frac{\operatorname{sin}(5 x - 7)}{5}-\int \frac{\operatorname{sin}(5 x - 7)}{5}\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{cos}(5 x - 7)\,\text{d}x= \\ \frac{7 x\operatorname{sin}(5 x - 7)}{5}-\frac{7\int \operatorname{sin}(5 x - 7)\,\text{d}x}{5} \\ =\frac{7 x\operatorname{sin}(5 x - 7)}{5}+\frac{7\operatorname{cos}(5 x - 7)}{25}+C\end{gathered}
$$

---

## Generated normal phase_cos/1

Level: moderate; template: phase_cos; profile: authored:parts-errors; field type: radio

Calculate  $\int 3 x\operatorname{cos}(2 x + 1)\,\text{d}x.$

- $\frac{3 x \operatorname{sin}{(2 x + 1 )}}{2}+\frac{3 x \operatorname{cos}{(2 x + 1 )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x + 1 )}}{2}+0+C$
- $\frac{3 x \operatorname{sin}{(2 x + 1 )}}{2}- \frac{3 \operatorname{cos}{(2 x + 1 )}}{4}+C$
- $- \frac{3 x \operatorname{sin}{(2 x + 1 )}}{2}+\frac{3 \operatorname{cos}{(2 x + 1 )}}{4}+C$
- $\frac{3 x \operatorname{sin}{(2 x + 1 )}}{2}+\frac{3 \operatorname{cos}{(2 x + 1 )}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{cos}(2 x + 1)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(2 x + 1)\, & ⟹\,v=\frac{\operatorname{sin}(2 x + 1)}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{cos}(2 x + 1)\,\text{d}x= \\ 3 x\cdot \frac{\operatorname{sin}(2 x + 1)}{2}-\int \frac{\operatorname{sin}(2 x + 1)}{2}\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{cos}(2 x + 1)\,\text{d}x= \\ \frac{3 x\operatorname{sin}(2 x + 1)}{2}-\frac{3\int \operatorname{sin}(2 x + 1)\,\text{d}x}{2} \\ =\frac{3 x\operatorname{sin}(2 x + 1)}{2}+\frac{3\operatorname{cos}(2 x + 1)}{4}+C\end{gathered}
$$

---

## Generated normal affine_cos_unit/0

Level: moderate; template: affine_cos_unit; profile: authored:parts-errors; field type: radio

$\int (7 x + 6)\operatorname{cos}(x)\,\text{d}x=$

- $(7 x + 6) \operatorname{sin}{(x )}+(7 x + 6) \operatorname{cos}{(x )}+C$
- $(7 x + 6) \operatorname{sin}{(x )}- 7 \operatorname{cos}{(x )}+C$
- $(- 7 x - 6) \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$
- $(7 x + 6) \operatorname{sin}{(x )}+0+C$
- $(7 x + 6) \operatorname{sin}{(x )}+7 \operatorname{cos}{(x )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x + 6)\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x + 6\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x + 6)\cdot \operatorname{cos}(x)\,\text{d}x= \\ (7 x + 6)\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (7 x + 6)\operatorname{cos}(x)\,\text{d}x= \\ (7 x + 6)\operatorname{sin}(x)-7\int \operatorname{sin}(x)\,\text{d}x \\ =(7 x + 6)\operatorname{sin}(x)+7\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal affine_cos_unit/1

Level: moderate; template: affine_cos_unit; profile: authored:parts-errors; field type: radio

$\int (3 x - 6)\operatorname{cos}(x)\,\text{d}x=$

- $(6 - 3 x) \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$
- $(3 x - 6) \operatorname{sin}{(x )}+(3 x - 6) \operatorname{cos}{(x )}+C$
- $(3 x - 6) \operatorname{sin}{(x )}- 3 \operatorname{cos}{(x )}+C$
- $(3 x - 6) \operatorname{sin}{(x )}+3 \operatorname{cos}{(x )}+C$ **correct**
- $(3 x - 6) \operatorname{sin}{(x )}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x - 6)\operatorname{cos}(x)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x - 6\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{cos}(x)\, & ⟹\,v=\operatorname{sin}(x).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x - 6)\cdot \operatorname{cos}(x)\,\text{d}x= \\ (3 x - 6)\cdot \operatorname{sin}(x)-\int \operatorname{sin}(x)\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows

$$
\begin{gathered}\int (3 x - 6)\operatorname{cos}(x)\,\text{d}x= \\ (3 x - 6)\operatorname{sin}(x)-3\int \operatorname{sin}(x)\,\text{d}x \\ =(3 x - 6)\operatorname{sin}(x)+3\operatorname{cos}(x)+C\end{gathered}
$$

---

## Generated normal phase_sin/0

Level: moderate; template: phase_sin; profile: authored:parts-errors; field type: radio

Calculate  $\int 7 x\operatorname{sin}(5 x - 7)\,\text{d}x.$

- $- \frac{7 x \operatorname{cos}{(5 x - 7 )}}{5}+\frac{7 \operatorname{sin}{(5 x - 7 )}}{25}+C$ **correct**
- $- \frac{7 x \operatorname{cos}{(5 x - 7 )}}{5}+\frac{7 x \operatorname{sin}{(5 x - 7 )}}{25}+C$
- $- \frac{7 x \operatorname{cos}{(5 x - 7 )}}{5}- \frac{7 \operatorname{sin}{(5 x - 7 )}}{25}+C$
- $\frac{7 x \operatorname{cos}{(5 x - 7 )}}{5}+\frac{7 \operatorname{sin}{(5 x - 7 )}}{25}+C$
- $- \frac{7 x \operatorname{cos}{(5 x - 7 )}}{5}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{sin}(5 x - 7)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{sin}(5 x - 7)\, & ⟹\,v=-\frac{\operatorname{cos}(5 x - 7)}{5}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{sin}(5 x - 7)\,\text{d}x= \\ 7 x\cdot (-\frac{\operatorname{cos}(5 x - 7)}{5})-\int (-\frac{\operatorname{cos}(5 x - 7)}{5})\cdot 7\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 7 x\operatorname{sin}(5 x - 7)\,\text{d}x= \\ -\frac{7 x\operatorname{cos}(5 x - 7)}{5}+\frac{7\int \operatorname{cos}(5 x - 7)\,\text{d}x}{5} \\ =-\frac{7 x\operatorname{cos}(5 x - 7)}{5}+\frac{7\operatorname{sin}(5 x - 7)}{25}+C\end{gathered}
$$

---

## Generated normal phase_sin/1

Level: moderate; template: phase_sin; profile: authored:parts-errors; field type: radio

Calculate  $\int 3 x\operatorname{sin}(2 x + 1)\,\text{d}x.$

- $- \frac{3 x \operatorname{cos}{(2 x + 1 )}}{2}+\frac{3 x \operatorname{sin}{(2 x + 1 )}}{4}+C$
- $- \frac{3 x \operatorname{cos}{(2 x + 1 )}}{2}+0+C$
- $- \frac{3 x \operatorname{cos}{(2 x + 1 )}}{2}- \frac{3 \operatorname{sin}{(2 x + 1 )}}{4}+C$
- $\frac{3 x \operatorname{cos}{(2 x + 1 )}}{2}+\frac{3 \operatorname{sin}{(2 x + 1 )}}{4}+C$
- $- \frac{3 x \operatorname{cos}{(2 x + 1 )}}{2}+\frac{3 \operatorname{sin}{(2 x + 1 )}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{sin}(2 x + 1)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{sin}(2 x + 1)\, & ⟹\,v=-\frac{\operatorname{cos}(2 x + 1)}{2}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{sin}(2 x + 1)\,\text{d}x= \\ 3 x\cdot (-\frac{\operatorname{cos}(2 x + 1)}{2})-\int (-\frac{\operatorname{cos}(2 x + 1)}{2})\cdot 3\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral, as follows:

$$
\begin{gathered}\int 3 x\operatorname{sin}(2 x + 1)\,\text{d}x= \\ -\frac{3 x\operatorname{cos}(2 x + 1)}{2}+\frac{3\int \operatorname{cos}(2 x + 1)\,\text{d}x}{2} \\ =-\frac{3 x\operatorname{cos}(2 x + 1)}{2}+\frac{3\operatorname{sin}(2 x + 1)}{4}+C\end{gathered}
$$

---

## Generated normal csc_log/0

Level: hard; template: csc_log; profile: authored:parts-errors; field type: radio

Calculate $\int 7 x\operatorname{csc}^{2}(x + 5)\,\text{d}x.$

- $- 7 x \operatorname{cot}{(x + 5 )}+7 x \ln{(|{\operatorname{sin}{(x + 5 )}}| )}+C$
- $- 7 x \operatorname{cot}{(x + 5 )}- 7 \ln{(|{\operatorname{sin}{(x + 5 )}}| )}+C$
- $7 x \operatorname{cot}{(x + 5 )}+7 \ln{(|{\operatorname{sin}{(x + 5 )}}| )}+C$
- $- 7 x \operatorname{cot}{(x + 5 )}+0+C$
- $- 7 x \operatorname{cot}{(x + 5 )}+7 \ln{(|{\operatorname{sin}{(x + 5 )}}| )}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 x\operatorname{csc}^{2}(x + 5)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore we set

$$
\begin{aligned}u=7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′}=\operatorname{csc}^{2}(x + 5)\, & ⟹\,v=-\operatorname{cot}(x + 5).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot \operatorname{csc}^{2}(x + 5)\,\text{d}x= \\ 7 x\cdot (-\operatorname{cot}(x + 5))-\int (-\operatorname{cot}(x + 5))\cdot 7\,\text{d}x \\ =-7 x\operatorname{cot}(x + 5)+7\int \frac{\operatorname{cos}(x + 5)}{\operatorname{sin}(x + 5)}\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral using the substitution $u=\operatorname{sin}(x + 5),$ where $\text{d}u=\operatorname{cos}(x + 5)\,\text{d}x,$ as follows:

$$
\begin{gathered}\int 7 x\operatorname{csc}^{2}(x + 5)\,\text{d}x= \\ -7 x\operatorname{cot}(x + 5)+7\int \frac{\operatorname{cos}(x + 5)}{\operatorname{sin}(x + 5)}\,\text{d}x \\ =-7 x\operatorname{cot}(x + 5)+7\int \frac{1}{u}\,\text{d}u \\ =-7 x\operatorname{cot}(x + 5)+7\ln|u|+C \\ =-7 x\operatorname{cot}(x + 5)+7\ln|\operatorname{sin}(x + 5)|+C\end{gathered}
$$

---

## Generated normal csc_log/1

Level: hard; template: csc_log; profile: authored:parts-errors; field type: radio

Calculate $\int 3 x\operatorname{csc}^{2}(x - 6)\,\text{d}x.$

- $3 x \operatorname{cot}{(x - 6 )}+3 \ln{(|{\operatorname{sin}{(x - 6 )}}| )}+C$
- $- 3 x \operatorname{cot}{(x - 6 )}+3 x \ln{(|{\operatorname{sin}{(x - 6 )}}| )}+C$
- $- 3 x \operatorname{cot}{(x - 6 )}- 3 \ln{(|{\operatorname{sin}{(x - 6 )}}| )}+C$
- $- 3 x \operatorname{cot}{(x - 6 )}+3 \ln{(|{\operatorname{sin}{(x - 6 )}}| )}+C$ **correct**
- $- 3 x \operatorname{cot}{(x - 6 )}+0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 x\operatorname{csc}^{2}(x - 6)\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore we set

$$
\begin{aligned}u=3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}=\operatorname{csc}^{2}(x - 6)\, & ⟹\,v=-\operatorname{cot}(x - 6).\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{gathered}\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot \operatorname{csc}^{2}(x - 6)\,\text{d}x= \\ 3 x\cdot (-\operatorname{cot}(x - 6))-\int (-\operatorname{cot}(x - 6))\cdot 3\,\text{d}x \\ =-3 x\operatorname{cot}(x - 6)+3\int \frac{\operatorname{cos}(x - 6)}{\operatorname{sin}(x - 6)}\,\text{d}x.\end{gathered}
$$

Finally, we calculate the integral using the substitution $u=\operatorname{sin}(x - 6),$ where $\text{d}u=\operatorname{cos}(x - 6)\,\text{d}x,$ as follows:

$$
\begin{gathered}\int 3 x\operatorname{csc}^{2}(x - 6)\,\text{d}x= \\ -3 x\operatorname{cot}(x - 6)+3\int \frac{\operatorname{cos}(x - 6)}{\operatorname{sin}(x - 6)}\,\text{d}x \\ =-3 x\operatorname{cot}(x - 6)+3\int \frac{1}{u}\,\text{d}u \\ =-3 x\operatorname{cot}(x - 6)+3\ln|u|+C \\ =-3 x\operatorname{cot}(x - 6)+3\ln|\operatorname{sin}(x - 6)|+C\end{gathered}
$$
