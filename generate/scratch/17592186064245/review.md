# Exponential integration by parts: originals and variants

Author preview. All generated variants explicitly labeled; same-level variants have no progression.

## Original q-14434 — easy

$\int 6x{e}^{4x}\,\text{d}x=$

- $\frac{x{e}^{4x}}{3}+\frac{x{e}^{4x}}{9}+C$
- $\frac{3x{e}^{4x}}{2}-\frac{3{e}^{4x}}{8}+C$ **original correct**
- $\frac{3x{e}^{4x}}{2}-\frac{3{e}^{4x}}{9}+C$
- $\frac{x{e}^{4x}}{2}-\frac{3{e}^{4x}}{8}+C$
- $\frac{{e}^{4x}}{3}+\frac{{e}^{4x}}{9}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6x{e}^{4x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6x\, & ⟹\,{u}^{′}=6 \\ {v}^{′}={e}^{4x}\, & ⟹\,v=\frac{1}{4}{e}^{4x}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 6x\cdot {e}^{4x}\,\text{d}x & =6x\cdot \frac{1}{4}{e}^{4x}-\int \frac{1}{4}{e}^{4x}\cdot 6\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 6x{e}^{4x}\,\text{d}x & =\frac{3}{2}x{e}^{4x}-\frac{3}{2}\int {e}^{4x}\,\text{d}x \\  & =\frac{3x{e}^{4x}}{2}-\frac{3{e}^{4x}}{8}+C\end{aligned}
$$

---

## Original q-2425 — unrated

Calculate $\intx2^{x}dx$.

- $\frac{2^{x}}{\ln 2}(\frac{1}{x} - \frac{x}{\ln 2}) + C$
- $\frac{2^{x}}{\ln 2}(x - 1) + C$
- $\frac{2^{x}}{\ln 2}(1 - \frac{x}{\ln 2}) + C$
- $\frac{2^{x}}{\ln 2}(x + \frac{1}{\ln 2}) + C$
- $\frac{2^{x}}{\ln 2}(x - \frac{1}{\ln 2}) + C$

*No original correct designation, solution, or difficulty captured.*

---

## Original q-114287 — moderate

Calculate $\int 6x{e}^{-3x}\,\text{d}x.$

- $\frac{x{e}^{-3x}}{2}-\frac{2{e}^{-3x}}{3}+C$
- $-2x{e}^{-3x}-\frac{2{e}^{-3x}}{3}+C$ **original correct**
- $4x{e}^{-3x}-\frac{3{e}^{-3x}}{2}+C$
- $-x{e}^{-3x}+\frac{2{e}^{-3x}}{3}+C$
- $-3x{e}^{-3x}-\frac{{e}^{-3x}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6x{e}^{-3x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=6x\, & ⟹\,{u}^{′}=6 \\ {v}^{′}={e}^{-3x}\, & ⟹\,v=-\frac{{e}^{-3x}}{3}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 6x\cdot {e}^{-3x}\,\text{d}x & =6x\cdot (-\frac{{e}^{-3x}}{3})-\int (-\frac{{e}^{-3x}}{3})\cdot 6\,\text{d}x \\  & =-2x{e}^{-3x}+2\int {e}^{-3x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 6x{e}^{-3x}\,\text{d}x & =-2x{e}^{-3x}+2\int {e}^{-3x}\,\text{d}x \\  & =-2x{e}^{-3x}-\frac{2{e}^{-3x}}{3}+C\end{aligned}
$$

---

## Original q-114288 — easy

$\int 4x{e}^{8x}\,\text{d}x=$

- $\frac{x{e}^{8x}}{2}-\frac{{e}^{8x}}{4}+C$
- $\frac{x{e}^{8x}}{4}+\frac{5{e}^{8x}}{16}+C$
- $\frac{x{e}^{8x}}{8}-\frac{{e}^{8x}}{16}+C$
- $\frac{x{e}^{8x}}{2}-\frac{{e}^{8x}}{16}+C$ **original correct**
- $\frac{3x{e}^{8x}}{8}+\frac{{e}^{8x}}{12}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 4x{e}^{8x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=4x\, & ⟹\,{u}^{′}=4 \\ {v}^{′}={e}^{8x}\, & ⟹\,v=\frac{1}{8}{e}^{8x}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 4x\cdot {e}^{8x}\,\text{d}x & =4x\cdot \frac{1}{8}{e}^{8x}-\int \frac{1}{8}{e}^{8x}\cdot 4\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 4x{e}^{8x}\,\text{d}x & =\frac{1}{2}x{e}^{8x}-\frac{1}{2}\int {e}^{8x}\,\text{d}x \\  & =\frac{x{e}^{8x}}{2}-\frac{{e}^{8x}}{16}+C\end{aligned}
$$

---

## Original q-114289 — moderate

Calculate $\int x{3}^{x}\,\text{d}x.$

- $\frac{{3}^{x}}{\operatorname{ln}⁡3}(2x+\frac{1}{\operatorname{ln}⁡3})+C$
- $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-\frac{1}{\operatorname{ln}⁡3})+C$ **original correct**
- $\frac{{3}^{x}}{\operatorname{ln}⁡3}(\frac{1}{\operatorname{ln}⁡3}-\frac{x}{2})+C$
- $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-\frac{1}{3})+C$
- $\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-1)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x{3}^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & ={3}^{x}\, & ⟹\,v=\frac{{3}^{x}}{\operatorname{ln}⁡3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot {3}^{x}\,\text{d}x & =x\cdot \frac{{3}^{x}}{\operatorname{ln}⁡3}-\int \frac{{3}^{x}}{\operatorname{ln}⁡3}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x{3}^{x}\,\text{d}x & =\frac{x{3}^{x}}{\operatorname{ln}⁡3}-\int \frac{{3}^{x}}{\operatorname{ln}⁡3}\,\text{d}x \\  & =\frac{x{3}^{x}}{\operatorname{ln}⁡3}-\frac{{3}^{x}}{(\operatorname{ln}⁡3)^{2}}+C \\  & =\frac{{3}^{x}}{\operatorname{ln}⁡3}(x-\frac{1}{\operatorname{ln}⁡3})+C\end{aligned}
$$

---

## Original q-114290 — hard

Calculate the integral $\int (x-2){e}^{x+3}\,\text{d}x.$

- $(x-3){e}^{x+3}+C$ **original correct**
- $(\frac{x}{3}-6){e}^{x+3}+C$
- $(2x-1){e}^{x+3}+C$
- $(\frac{x}{\operatorname{ln}⁡3}+3){e}^{x+3}+C$
- $(\frac{x}{2}-3){e}^{x+3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x-2){e}^{x+3}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x-2\, & ⟹\,{u}^{′}=1 \\ {v}^{′}={e}^{x+3}\, & ⟹\,v={e}^{x+3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x-2)\cdot {e}^{x+3}\,\text{d}x & =(x-2)\cdot {e}^{x+3}-\int {e}^{x+3}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x-2){e}^{x+3}\,\text{d}x & =(x-2){e}^{x+3}-\int {e}^{x+3}\,\text{d}x \\  & =(x-2){e}^{x+3}-{e}^{x+3}+C \\  & =(x-3){e}^{x+3}+C\end{aligned}
$$

---

## Original q-114293 — hard

Calculate $\int (3x-4){e}^{-3x}\,\text{d}x.$

- $\frac{(2x-1){e}^{-3x}}{3}+C$
- $(1-x){e}^{-3x}+C$ **original correct**
- $(2-3x){e}^{-3x}+C$
- $(2x-1){e}^{-3x}+C$
- $\frac{(2-x){e}^{-3x}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3x-4){e}^{-3x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3x-4\, & ⟹\,{u}^{′}=3 \\ {v}^{′}={e}^{-3x}\, & ⟹\,v=-\frac{{e}^{-3x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3x-4)\cdot {e}^{-3x}\,\text{d}x & =(3x-4)\cdot (-\frac{{e}^{-3x}}{3})-\int (-\frac{{e}^{-3x}}{3})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3x-4){e}^{-3x}\,\text{d}x & =-\frac{(3x-4){e}^{-3x}}{3}+\int {e}^{-3x}\,\text{d}x \\  & =-\frac{(3x-4){e}^{-3x}}{3}-\frac{{e}^{-3x}}{3}+C \\  & =-\frac{(3x-3){e}^{-3x}}{3}+C \\  & =(1-x){e}^{-3x}+C\end{aligned}
$$

---

## Original q-12462 — moderate

Calculate the integral $\int 3x{e}^{-x}\,\text{d}x.$

- $-3x{e}^{-x}-2{e}^{-x}+C$
- $-3x{e}^{-x}+{e}^{-x}+C$
- $-3x{e}^{-x}-3{e}^{-x}+C$ **original correct**
- $2{e}^{-x}-3x{e}^{-x}+C$
- $3{e}^{-x}-x{e}^{-x}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3x{e}^{-x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}={e}^{-x}\, & ⟹\,v=-{e}^{-x}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3x\cdot {e}^{-x}\,\text{d}x & =3x\cdot (-{e}^{-x})-\int (-{e}^{-x})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3x{e}^{-x}\,\text{d}x & =-3x{e}^{-x}+3\int {e}^{-x}\,\text{d}x \\  & =-3x{e}^{-x}-3{e}^{-x}+C\end{aligned}
$$

---

## Original q-12556 — moderate

Calculate the integral $\int x{e}^{-3x}\,\text{d}x.$

- $-\frac{x{e}^{-3x}}{3}-\frac{{e}^{-3x}}{9}+C$ **original correct**
- $\frac{x{e}^{-3x}}{9}+\frac{{e}^{-3x}}{9}+C$
- $\frac{{e}^{-3x}}{3}-\frac{x{e}^{-3x}}{9}+C$
- $-\frac{x{e}^{3x}}{3}+\frac{{e}^{3x}}{9}+C$
- $\frac{x{e}^{-3x}}{9}-\frac{{e}^{-3x}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x{e}^{-3x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}={e}^{-3x}\, & ⟹\,v=-\frac{{e}^{-3x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot {e}^{-3x}\,\text{d}x & =x\cdot (-\frac{{e}^{-3x}}{3})-\int (-\frac{{e}^{-3x}}{3})\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x{e}^{-3x}\,\text{d}x & =-\frac{x{e}^{-3x}}{3}+\frac{1}{3}\int {e}^{-3x}\,\text{d}x \\  & =-\frac{x{e}^{-3x}}{3}-\frac{{e}^{-3x}}{9}+C\end{aligned}
$$

---

## Original q-12559 — hard

Calculate $\int (3x+5){e}^{-5x}\,\text{d}x.$

- $-\frac{(3x+5){e}^{5x}}{5}+\frac{3x{e}^{5x}}{25}+C$
- $\frac{(3x+5){e}^{-5x}}{5}+\frac{3x{e}^{-5x}}{25}+C$
- $\frac{(3x+5){e}^{-5x}}{25}-\frac{{e}^{-5x}}{5}+C$
- $-\frac{(3x+5){e}^{-5x}}{5}-\frac{3{e}^{-5x}}{25}+C$ **original correct**
- $-\frac{3x{e}^{-5x}}{25}-\frac{3{e}^{-5x}}{25}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3x+5){e}^{-5x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3x+5\, & ⟹\,{u}^{′}=3 \\ {v}^{′}={e}^{-5x}\, & ⟹\,v=-\frac{{e}^{-5x}}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3x+5)\cdot {e}^{-5x}\,\text{d}x & =(3x+5)\cdot (-\frac{{e}^{-5x}}{5})-\int (-\frac{{e}^{-5x}}{5})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3x+5){e}^{-5x}\,\text{d}x & =-\frac{(3x+5){e}^{-5x}}{5}+\frac{3}{5}\int {e}^{-5x}\,\text{d}x \\  & =-\frac{(3x+5){e}^{-5x}}{5}-\frac{3{e}^{-5x}}{25}+C\end{aligned}
$$

---

## Original q-12560 — hard

Calculate the integral $\int (x+7){e}^{2x+5}\,\text{d}x.$

- $-\frac{x{e}^{2x+5}}{4}+\frac{{e}^{2x+5}}{2}+C$
- $\frac{x{e}^{2x+5}}{4}-\frac{{e}^{2x+5}}{4}+C$
- $\frac{(x+7){e}^{2x+5}}{4}-\frac{x{e}^{2x+5}}{4}+C$
- $\frac{(x+7){e}^{2x+5}}{2}-\frac{{e}^{2x+5}}{4}+C$ **original correct**
- $-\frac{(x+7){e}^{2x+5}}{4}+\frac{{e}^{2x+5}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x+7){e}^{2x+5}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x+7\, & ⟹\,{u}^{′}=1 \\ {v}^{′}={e}^{2x+5}\, & ⟹\,v=\frac{{e}^{2x+5}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x+7)\cdot {e}^{2x+5}\,\text{d}x & =(x+7)\cdot \frac{{e}^{2x+5}}{2}-\int \frac{{e}^{2x+5}}{2}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x+7){e}^{2x+5}\,\text{d}x & =\frac{(x+7){e}^{2x+5}}{2}-\frac{1}{2}\int {e}^{2x+5}\,\text{d}x \\  & =\frac{(x+7){e}^{2x+5}}{2}-\frac{{e}^{2x+5}}{4}+C\end{aligned}
$$

---

## Original q-2420 — moderate

$\int x{5}^{x}\,\text{d}x=$

- $\frac{{5}^{x}}{\operatorname{ln}⁡5}(\frac{1}{x}-\frac{x}{\operatorname{ln}⁡5})+C$
- $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x-1)+C$
- $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x-\frac{1}{\operatorname{ln}⁡5})+C$ **original correct**
- $\frac{{5}^{x}}{\operatorname{ln}⁡5}(1-\frac{x}{\operatorname{ln}⁡5})+C$
- $\frac{{5}^{x}}{\operatorname{ln}⁡5}(x+\frac{1}{\operatorname{ln}⁡5})+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x{5}^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=x\, & ⟹\,{u}^{′}=1 \\ {v}^{′}={5}^{x}\, & ⟹\,v=\frac{{5}^{x}}{\operatorname{ln}⁡(5)}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot {5}^{x}\,\text{d}x & =x\cdot \frac{{5}^{x}}{\operatorname{ln}⁡(5)}-\int \frac{{5}^{x}}{\operatorname{ln}⁡(5)}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x{5}^{x}\,\text{d}x & =\frac{x{5}^{x}}{\operatorname{ln}⁡(5)}-\int \frac{{5}^{x}}{\operatorname{ln}⁡(5)}\,\text{d}x \\  & =\frac{x{5}^{x}}{\operatorname{ln}⁡(5)}-\frac{{5}^{x}}{(\operatorname{ln}⁡(5))^{2}}+C \\  & =\frac{{5}^{x}}{\operatorname{ln}⁡5}(x-\frac{1}{\operatorname{ln}⁡5})+C\end{aligned}
$$

---

## Original q-114291 — hard

Calculate the integral $\int (2x+1){e}^{3x}\,\text{d}x.$

- $\frac{(3x+2){e}^{3x}}{9}+C$
- $\frac{(6x+1){e}^{3x}}{9}+C$ **original correct**
- $\frac{(6x+4){e}^{3x}}{3}+C$
- $\frac{(4x-3){e}^{3x}}{9}+C$
- $\frac{(4x-1){e}^{3x}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (2x+1){e}^{3x}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=2x+1\, & ⟹\,{u}^{′}=2 \\ {v}^{′}={e}^{3x}\, & ⟹\,v=\frac{{e}^{3x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (2x+1)\cdot {e}^{3x}\,\text{d}x & =(2x+1)\cdot \frac{{e}^{3x}}{3}-\int \frac{{e}^{3x}}{3}\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (2x+1){e}^{3x}\,\text{d}x & =\frac{(2x+1){e}^{3x}}{3}-\frac{2}{3}\int {e}^{3x}\,\text{d}x \\  & =\frac{(2x+1){e}^{3x}}{3}-\frac{2{e}^{3x}}{9}+C \\  & =\frac{(6x+1){e}^{3x}}{9}+C\end{aligned}
$$

---

## Original q-12558 — moderate

$\int 3x{e}^{2x+5}\,\text{d}x=$

- $\frac{x{e}^{2x+5}}{4}+\frac{3{e}^{2x+5}}{4}+C$
- $\frac{3{e}^{2x}}{2}-\frac{3x{e}^{2x}}{4}+C$
- $\frac{3{e}^{2x+5}}{2}-\frac{3x{e}^{2x+5}}{4}+C$
- $\frac{3x{e}^{2x+5}}{2}-\frac{3{e}^{2x+5}}{4}+C$ **original correct**
- $\frac{{e}^{2x+5}}{2}+\frac{3{e}^{2x+5}}{4}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3x{e}^{2x+5}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u=3x\, & ⟹\,{u}^{′}=3 \\ {v}^{′}={e}^{2x+5}\, & ⟹\,v=\frac{{e}^{2x+5}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3x\cdot {e}^{2x+5}\,\text{d}x & =3x\cdot \frac{{e}^{2x+5}}{2}-\int \frac{{e}^{2x+5}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3x{e}^{2x+5}\,\text{d}x & =\frac{3x{e}^{2x+5}}{2}-\frac{3}{2}\int {e}^{2x+5}\,\text{d}x \\  & =\frac{3x{e}^{2x+5}}{2}-\frac{3{e}^{2x+5}}{4}+C\end{aligned}
$$

---

## Source replay q-14434

### easy — e_positive

$\int 6 xe^{4 x}\,\text{d}x=$

- $\frac{3 x e^{4 x}}{2}- \frac{e^{4 x}}{3}+C$
- $\frac{3 x e^{4 x}}{2}- \frac{3 e^{4 x}}{8}+C$ **correct**
- $\frac{x e^{4 x}}{3}+\frac{x e^{4 x}}{9}+C$
- $\frac{e^{4 x}}{3}+\frac{e^{4 x}}{9}+C$
- $\frac{x e^{4 x}}{2}- \frac{3 e^{4 x}}{8}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6 xe^{4 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =6 x\, & ⟹\,{u}^{′}=6 \\ {v}^{′} & =e^{4 x}\, & ⟹\,v=\frac{e^{4 x}}{4}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 6 x\cdot e^{4 x}\,\text{d}x & =6 x\cdot \frac{e^{4 x}}{4}-\int \frac{e^{4 x}}{4}\cdot 6\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 6 xe^{4 x}\,\text{d}x & =\frac{1}{4}6 xe^{4 x}-\frac{3}{2}\int e^{4 x}\,\text{d}x \\  & =\frac{1}{4}6 xe^{4 x}-\frac{3}{8}e^{4 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-14434

### easy — e_positive

$\int 3 xe^{8 x}\,\text{d}x=$

- $\frac{2 x e^{8 x}}{3}+\frac{4 x e^{8 x}}{9}+C$
- $\frac{2 e^{8 x}}{3}+\frac{4 e^{8 x}}{9}+C$
- $\frac{3 x e^{8 x}}{8}- \frac{3 e^{8 x}}{98}+C$
- $\frac{3 x e^{8 x}}{8}- \frac{3 e^{8 x}}{64}+C$ **correct**
- $\frac{x e^{8 x}}{2}- \frac{3 e^{8 x}}{64}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{8 x}\, & ⟹\,v=\frac{e^{8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{8 x}\,\text{d}x & =3 x\cdot \frac{e^{8 x}}{8}-\int \frac{e^{8 x}}{8}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{8 x}\,\text{d}x & =\frac{1}{8}3 xe^{8 x}-\frac{3}{8}\int e^{8 x}\,\text{d}x \\  & =\frac{1}{8}3 xe^{8 x}-\frac{3}{64}e^{8 x}+C\end{aligned}
$$

---

## Source replay q-114288

### easy — e_positive

$\int 4 xe^{8 x}\,\text{d}x=$

- $\frac{x e^{8 x}}{8}- \frac{e^{8 x}}{16}+C$
- $\frac{x e^{8 x}}{4}+\frac{5 e^{8 x}}{16}+C$
- $\frac{x e^{8 x}}{2}- \frac{e^{8 x}}{4}+C$
- $\frac{3 x e^{8 x}}{8}+\frac{e^{8 x}}{12}+C$
- $\frac{x e^{8 x}}{2}- \frac{e^{8 x}}{16}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 4 xe^{8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =4 x\, & ⟹\,{u}^{′}=4 \\ {v}^{′} & =e^{8 x}\, & ⟹\,v=\frac{e^{8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 4 x\cdot e^{8 x}\,\text{d}x & =4 x\cdot \frac{e^{8 x}}{8}-\int \frac{e^{8 x}}{8}\cdot 4\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 4 xe^{8 x}\,\text{d}x & =\frac{1}{8}4 xe^{8 x}-\frac{1}{2}\int e^{8 x}\,\text{d}x \\  & =\frac{1}{8}4 xe^{8 x}-\frac{1}{16}e^{8 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114288

### easy — e_positive

$\int 3 xe^{8 x}\,\text{d}x=$

- $\frac{3 x e^{8 x}}{8}- \frac{e^{8 x}}{3}+C$
- $\frac{x e^{8 x}}{4}+\frac{e^{8 x}}{11}+C$
- $\frac{x e^{8 x}}{8}- \frac{e^{8 x}}{16}+C$
- $\frac{x e^{8 x}}{3}+\frac{e^{8 x}}{4}+C$
- $\frac{3 x e^{8 x}}{8}- \frac{3 e^{8 x}}{64}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{8 x}\, & ⟹\,v=\frac{e^{8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{8 x}\,\text{d}x & =3 x\cdot \frac{e^{8 x}}{8}-\int \frac{e^{8 x}}{8}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{8 x}\,\text{d}x & =\frac{1}{8}3 xe^{8 x}-\frac{3}{8}\int e^{8 x}\,\text{d}x \\  & =\frac{1}{8}3 xe^{8 x}-\frac{3}{64}e^{8 x}+C\end{aligned}
$$

---

## Source replay q-2425

### moderate — base_legacy

Calculate $\int x2^{x}dx$.

- $\frac{2^{x}}{\ln{(2 )}}(- \frac{x}{\ln{(2 )}} + 1)+C$
- $\frac{2^{x}}{\ln{(2 )}}(x - 1)+C$
- $\frac{2^{x}}{\ln{(2 )}}(- \frac{x}{\ln{(2 )}} + \frac{1}{x})+C$
- $\frac{2^{x}}{\ln{(2 )}}(x - \frac{1}{\ln{(2 )}})+C$ **correct**
- $\frac{2^{x}}{\ln{(2 )}}(x + \frac{1}{\ln{(2 )}})+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x2^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =2^{x}\, & ⟹\,v=\frac{2^{x}}{\ln{(2 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 2^{x}\,\text{d}x & =x\cdot \frac{2^{x}}{\ln{(2 )}}-\int \frac{2^{x}}{\ln{(2 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x2^{x}\,\text{d}x & =\frac{2^{x} x}{\ln{(2 )}}-\int \frac{2^{x}}{\ln{(2 )}}\,\text{d}x \\  & =\frac{1}{\ln{(2 )}}x2^{x}-\frac{1}{\ln{(2 )}^{2}}2^{x}+C \\  & =\frac{2^{x}}{\ln{(2 )}}(x - \frac{1}{\ln{(2 )}})+C\end{aligned}
$$

---

## Generated empirical-profile variant q-2425

### moderate — base_legacy

Calculate $\int x4^{x}dx$.

- $\frac{4^{x}}{\ln{(4 )}}(- \frac{x}{\ln{(4 )}} + 1)+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - 1)+C$
- $\frac{4^{x}}{\ln{(4 )}}(- \frac{x}{\ln{(4 )}} + \frac{1}{x})+C$
- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(4^{x} )} - 1}{\ln{(4 )}})+C$ **correct**
- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(4^{x} )} + 1}{\ln{(4 )}})+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Source replay q-114287

### moderate — e_negative_distributed

Calculate $\int 6 xe^{- 3 x}\,\text{d}x.$

- $4 x e^{- 3 x}- \frac{3 e^{- 3 x}}{2}+C$
- $- 2 x e^{- 3 x}- \frac{2 e^{- 3 x}}{3}+C$ **correct**
- $\frac{x e^{- 3 x}}{2}- \frac{2 e^{- 3 x}}{3}+C$
- $- 3 x e^{- 3 x}- \frac{e^{- 3 x}}{3}+C$
- $- x e^{- 3 x}+\frac{2 e^{- 3 x}}{3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 6 xe^{- 3 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =6 x\, & ⟹\,{u}^{′}=6 \\ {v}^{′} & =e^{- 3 x}\, & ⟹\,v=- \frac{e^{- 3 x}}{3}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 6 x\cdot e^{- 3 x}\,\text{d}x & =6 x\cdot (- \frac{e^{- 3 x}}{3})-\int (- \frac{e^{- 3 x}}{3})\cdot 6\,\text{d}x \\  & =- \frac{1}{3}6 xe^{- 3 x}+2\int e^{- 3 x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 6 xe^{- 3 x}\,\text{d}x & =- \frac{1}{3}6 xe^{- 3 x}+2\int e^{- 3 x}\,\text{d}x \\  & =- \frac{1}{3}6 xe^{- 3 x}-\frac{2}{3}e^{- 3 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114287

### moderate — e_negative_distributed

Calculate $\int 3 xe^{- 8 x}\,\text{d}x.$

- $\frac{x e^{- 8 x}}{2}- \frac{e^{- 8 x}}{8}+C$
- $- 8 x e^{- 8 x}- \frac{e^{- 8 x}}{8}+C$
- $x e^{- 8 x}- 4 e^{- 8 x}+C$
- $- \frac{3 x e^{- 8 x}}{8}- \frac{3 e^{- 8 x}}{64}+C$ **correct**
- $- x e^{- 8 x}+\frac{e^{- 8 x}}{8}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- 8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 8 x}\, & ⟹\,v=- \frac{e^{- 8 x}}{8}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- 8 x}\,\text{d}x & =3 x\cdot (- \frac{e^{- 8 x}}{8})-\int (- \frac{e^{- 8 x}}{8})\cdot 3\,\text{d}x \\  & =- \frac{1}{8}3 xe^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- 8 x}\,\text{d}x & =- \frac{1}{8}3 xe^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x \\  & =- \frac{1}{8}3 xe^{- 8 x}-\frac{3}{64}e^{- 8 x}+C\end{aligned}
$$

---

## Source replay q-114289

### moderate — base_calculate

Calculate $\int x3^{x}\,\text{d}x.$

- $\frac{3^{x}}{\ln{(3 )}}(- \frac{x}{2} + \frac{1}{\ln{(3 )}})+C$
- $\frac{3^{x}}{\ln{(3 )}}(x - \frac{1}{\ln{(3 )}})+C$ **correct**
- $\frac{3^{x}}{\ln{(3 )}}(2 x + \frac{1}{\ln{(3 )}})+C$
- $\frac{3^{x}}{\ln{(3 )}}(x - 1)+C$
- $\frac{3^{x}}{\ln{(3 )}}(x - \frac{1}{3})+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x3^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =3^{x}\, & ⟹\,v=\frac{3^{x}}{\ln{(3 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 3^{x}\,\text{d}x & =x\cdot \frac{3^{x}}{\ln{(3 )}}-\int \frac{3^{x}}{\ln{(3 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x3^{x}\,\text{d}x & =\frac{3^{x} x}{\ln{(3 )}}-\int \frac{3^{x}}{\ln{(3 )}}\,\text{d}x \\  & =\frac{1}{\ln{(3 )}}x3^{x}-\frac{1}{\ln{(3 )}^{2}}3^{x}+C \\  & =\frac{3^{x}}{\ln{(3 )}}(x - \frac{1}{\ln{(3 )}})+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114289

### moderate — base_calculate

Calculate $\int x4^{x}\,\text{d}x.$

- $\frac{4^{x}}{\ln{(4 )}}(\frac{1 - \frac{\ln{(4^{x} )}}{2}}{\ln{(4 )}})+C$
- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(4^{x} )} - 1}{\ln{(4 )}})+C$ **correct**
- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(2^{4 x} )} + 1}{\ln{(4 )}})+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - 1)+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{4})+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Source replay q-114290

### hard — hard_shift_unit

Calculate the integral $\int (x - 2)e^{x + 3}\,\text{d}x.$

- $(2 x - 1) e^{x + 3}+C$
- $(\frac{x}{3} - 6) e^{x + 3}+C$
- $(x - 3) e^{x + 3}+C$ **correct**
- $(\frac{x}{2} - 3) e^{x + 3}+C$
- $(\frac{x}{\ln{(3 )}} + 3) e^{x + 3}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x - 2)e^{x + 3}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x - 2\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{x + 3}\, & ⟹\,v=e^{x + 3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x - 2)\cdot e^{x + 3}\,\text{d}x & =(x - 2)\cdot e^{x + 3}-\int e^{x + 3}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x - 2)e^{x + 3}\,\text{d}x & =(x - 2)e^{x + 3}-\int e^{x + 3}\,\text{d}x \\  & =(x - 2)e^{x + 3}-e^{x + 3}+C \\  & =(x - 3)e^{x + 3}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114290

### hard — hard_shift_unit

Calculate the integral $\int (x + 4)e^{x + 6}\,\text{d}x.$

- $(x + 3) e^{x + 6}+C$ **correct**
- $(- 4 x - 1) e^{x + 6}+C$
- $(3 - \frac{x}{4}) e^{x + 6}+C$
- $(\frac{x}{\ln{(6 )}} + 6) e^{x + 6}+C$
- $(\frac{x}{6} + 12) e^{x + 6}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x + 4)e^{x + 6}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x + 4\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{x + 6}\, & ⟹\,v=e^{x + 6}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x + 4)\cdot e^{x + 6}\,\text{d}x & =(x + 4)\cdot e^{x + 6}-\int e^{x + 6}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x + 4)e^{x + 6}\,\text{d}x & =(x + 4)e^{x + 6}-\int e^{x + 6}\,\text{d}x \\  & =(x + 4)e^{x + 6}-e^{x + 6}+C \\  & =(x + 3)e^{x + 6}+C\end{aligned}
$$

---

## Source replay q-114293

### hard — hard_negative_factor

Calculate $\int (3 x - 4)e^{- 3 x}\,\text{d}x.$

- $(2 - 3 x) e^{- 3 x}+C$
- $(1 - x) e^{- 3 x}+C$ **correct**
- $\frac{(2 x - 1) e^{- 3 x}}{3}+C$
- $\frac{(2 - x) e^{- 3 x}}{3}+C$
- $(2 x - 1) e^{- 3 x}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x - 4)e^{- 3 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x - 4\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 3 x}\, & ⟹\,v=- \frac{e^{- 3 x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x - 4)\cdot e^{- 3 x}\,\text{d}x & =(3 x - 4)\cdot (- \frac{e^{- 3 x}}{3})-\int (- \frac{e^{- 3 x}}{3})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x - 4)e^{- 3 x}\,\text{d}x & =- \frac{1}{3}(3 x - 4)e^{- 3 x}+\int e^{- 3 x}\,\text{d}x \\  & =- \frac{1}{3}(3 x - 4)e^{- 3 x}-\frac{1}{3}e^{- 3 x}+C \\  & =-\frac{(3 x - 3)e^{- 3 x}}{3}+C \\  & =(1 - x)e^{- 3 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114293

### hard — hard_negative_factor

Calculate $\int (3 x + 7)e^{- 8 x}\,\text{d}x.$

- $\frac{(2 x - 1) e^{- 8 x}}{8}+C$
- $\frac{(2 - x) e^{- 8 x}}{8}+C$
- $(2 - 3 x) e^{- 8 x}+C$
- $(2 x - 1) e^{- 8 x}+C$
- $(- \frac{3 x}{8} - \frac{59}{64}) e^{- 8 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)e^{- 8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 8 x}\, & ⟹\,v=- \frac{e^{- 8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot e^{- 8 x}\,\text{d}x & =(3 x + 7)\cdot (- \frac{e^{- 8 x}}{8})-\int (- \frac{e^{- 8 x}}{8})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 7)e^{- 8 x}\,\text{d}x & =- \frac{1}{8}(3 x + 7)e^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x \\  & =- \frac{1}{8}(3 x + 7)e^{- 8 x}-\frac{3}{64}e^{- 8 x}+C \\  & =-\frac{(3 x + \frac{59}{8})e^{- 8 x}}{8}+C \\  & =(- \frac{24 x + 59}{64})e^{- 8 x}+C\end{aligned}
$$

---

## Source replay q-12462

### moderate — e_negative_integral

Calculate the integral $\int 3 xe^{- x}\,\text{d}x.$

- $- 3 x e^{- x}- 3 e^{- x}+C$ **correct**
- $- 3 x e^{- x}+e^{- x}+C$
- $- 3 x e^{- x}- 2 e^{- x}+C$
- $3 e^{- x}- x e^{- x}+C$
- $2 e^{- x}- 3 x e^{- x}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- x}\, & ⟹\,v=- e^{- x}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- x}\,\text{d}x & =3 x\cdot (- e^{- x})-\int (- e^{- x})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- x}\,\text{d}x & =-3 xe^{- x}+3\int e^{- x}\,\text{d}x \\  & =-3 xe^{- x}-3e^{- x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-12462

### moderate — e_negative_integral

Calculate the integral $\int 3 xe^{- 8 x}\,\text{d}x.$

- $- 3 x e^{- 8 x}- 2 e^{- 8 x}+C$
- $3 e^{- 8 x}- x e^{- 8 x}+C$
- $- \frac{3 x e^{- 8 x}}{8}- \frac{3 e^{- 8 x}}{64}+C$ **correct**
- $- 3 x e^{- 8 x}+e^{- 8 x}+C$
- $2 e^{- 8 x}- 3 x e^{- 8 x}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- 8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 8 x}\, & ⟹\,v=- \frac{e^{- 8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- 8 x}\,\text{d}x & =3 x\cdot (- \frac{e^{- 8 x}}{8})-\int (- \frac{e^{- 8 x}}{8})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- 8 x}\,\text{d}x & =- \frac{1}{8}3 xe^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x \\  & =- \frac{1}{8}3 xe^{- 8 x}-\frac{3}{64}e^{- 8 x}+C\end{aligned}
$$

---

## Source replay q-12556

### moderate — e_negative_integral

Calculate the integral $\int xe^{- 3 x}\,\text{d}x.$

- $\frac{e^{- 3 x}}{3}- \frac{x e^{- 3 x}}{9}+C$
- $\frac{x e^{- 3 x}}{9}+\frac{e^{- 3 x}}{9}+C$
- $- \frac{x e^{- 3 x}}{3}- \frac{e^{- 3 x}}{9}+C$ **correct**
- $\frac{x e^{- 3 x}}{9}- \frac{e^{- 3 x}}{3}+C$
- $- \frac{x e^{3 x}}{3}+\frac{e^{3 x}}{9}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int xe^{- 3 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{- 3 x}\, & ⟹\,v=- \frac{e^{- 3 x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot e^{- 3 x}\,\text{d}x & =x\cdot (- \frac{e^{- 3 x}}{3})-\int (- \frac{e^{- 3 x}}{3})\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int xe^{- 3 x}\,\text{d}x & =- \frac{1}{3}xe^{- 3 x}+\frac{1}{3}\int e^{- 3 x}\,\text{d}x \\  & =- \frac{1}{3}xe^{- 3 x}-\frac{1}{9}e^{- 3 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-12556

### moderate — e_negative_integral

Calculate the integral $\int 3 xe^{- 8 x}\,\text{d}x.$

- $- \frac{3 x e^{- 8 x}}{8}- \frac{3 e^{- 8 x}}{64}+C$ **correct**
- $\frac{x e^{- 8 x}}{64}- \frac{e^{- 8 x}}{8}+C$
- $\frac{e^{- 8 x}}{8}- \frac{x e^{- 8 x}}{64}+C$
- $\frac{x e^{- 8 x}}{64}+\frac{e^{- 8 x}}{64}+C$
- $- \frac{x e^{8 x}}{8}+\frac{e^{8 x}}{64}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- 8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 8 x}\, & ⟹\,v=- \frac{e^{- 8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- 8 x}\,\text{d}x & =3 x\cdot (- \frac{e^{- 8 x}}{8})-\int (- \frac{e^{- 8 x}}{8})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- 8 x}\,\text{d}x & =- \frac{1}{8}3 xe^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x \\  & =- \frac{1}{8}3 xe^{- 8 x}-\frac{3}{64}e^{- 8 x}+C\end{aligned}
$$

---

## Source replay q-12559

### hard — hard_negative_split

Calculate $\int (3 x + 5)e^{- 5 x}\,\text{d}x.$

- $\frac{(3 x + 5) e^{- 5 x}}{25}- \frac{e^{- 5 x}}{5}+C$
- $\frac{(3 x + 5) e^{- 5 x}}{5}+\frac{3 x e^{- 5 x}}{25}+C$
- $\frac{(- 3 x - 5) e^{5 x}}{5}+\frac{3 x e^{5 x}}{25}+C$
- $- \frac{3 x e^{- 5 x}}{25}- \frac{3 e^{- 5 x}}{25}+C$
- $- \frac{(3 x + 5) e^{- 5 x}}{5}- \frac{3 e^{- 5 x}}{25}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 5)e^{- 5 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 5\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 5 x}\, & ⟹\,v=- \frac{e^{- 5 x}}{5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 5)\cdot e^{- 5 x}\,\text{d}x & =(3 x + 5)\cdot (- \frac{e^{- 5 x}}{5})-\int (- \frac{e^{- 5 x}}{5})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 5)e^{- 5 x}\,\text{d}x & =- \frac{1}{5}(3 x + 5)e^{- 5 x}+\frac{3}{5}\int e^{- 5 x}\,\text{d}x \\  & =- \frac{1}{5}(3 x + 5)e^{- 5 x}-\frac{3}{25}e^{- 5 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-12559

### hard — hard_negative_split

Calculate $\int (3 x + 7)e^{- 8 x}\,\text{d}x.$

- $\frac{(- 3 x - 7) e^{8 x}}{8}+\frac{3 x e^{8 x}}{64}+C$
- $- \frac{3 x e^{- 8 x}}{64}- \frac{3 e^{- 8 x}}{64}+C$
- $\frac{(3 x + 7) e^{- 8 x}}{64}- \frac{e^{- 8 x}}{8}+C$
- $- \frac{(3 x + 7) e^{- 8 x}}{8}- \frac{3 e^{- 8 x}}{64}+C$ **correct**
- $\frac{(3 x + 7) e^{- 8 x}}{8}+\frac{3 x e^{- 8 x}}{64}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)e^{- 8 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 8 x}\, & ⟹\,v=- \frac{e^{- 8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot e^{- 8 x}\,\text{d}x & =(3 x + 7)\cdot (- \frac{e^{- 8 x}}{8})-\int (- \frac{e^{- 8 x}}{8})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 7)e^{- 8 x}\,\text{d}x & =- \frac{1}{8}(3 x + 7)e^{- 8 x}+\frac{3}{8}\int e^{- 8 x}\,\text{d}x \\  & =- \frac{1}{8}(3 x + 7)e^{- 8 x}-\frac{3}{64}e^{- 8 x}+C\end{aligned}
$$

---

## Source replay q-12560

### hard — hard_shift_split

Calculate the integral $\int (x + 7)e^{2 x + 5}\,\text{d}x.$

- $\frac{(x + 7) e^{2 x + 5}}{4}- \frac{x e^{2 x + 5}}{4}+C$
- $\frac{x e^{2 x + 5}}{4}- \frac{e^{2 x + 5}}{4}+C$
- $- \frac{x e^{2 x + 5}}{4}+\frac{e^{2 x + 5}}{2}+C$
- $\frac{(- x - 7) e^{2 x + 5}}{4}+\frac{e^{2 x + 5}}{2}+C$
- $\frac{(x + 7) e^{2 x + 5}}{2}- \frac{e^{2 x + 5}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x + 7)e^{2 x + 5}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x + 7\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{2 x + 5}\, & ⟹\,v=\frac{e^{2 x + 5}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x + 7)\cdot e^{2 x + 5}\,\text{d}x & =(x + 7)\cdot \frac{e^{2 x + 5}}{2}-\int \frac{e^{2 x + 5}}{2}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x + 7)e^{2 x + 5}\,\text{d}x & =\frac{1}{2}(x + 7)e^{2 x + 5}-\frac{1}{2}\int e^{2 x + 5}\,\text{d}x \\  & =\frac{1}{2}(x + 7)e^{2 x + 5}-\frac{1}{4}e^{2 x + 5}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-12560

### hard — hard_shift_split

Calculate the integral $\int (3 x + 7)e^{8 x - 3}\,\text{d}x.$

- $\frac{(- 3 x - 7) e^{8 x - 3}}{64}+\frac{e^{8 x - 3}}{8}+C$
- $- \frac{x e^{8 x - 3}}{64}+\frac{e^{8 x - 3}}{8}+C$
- $\frac{x e^{8 x - 3}}{64}- \frac{e^{8 x - 3}}{64}+C$
- $\frac{(3 x + 7) e^{8 x - 3}}{64}- \frac{x e^{8 x - 3}}{64}+C$
- $\frac{(3 x + 7) e^{8 x - 3}}{8}- \frac{3 e^{8 x - 3}}{64}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)e^{8 x - 3}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{8 x - 3}\, & ⟹\,v=\frac{e^{8 x - 3}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot e^{8 x - 3}\,\text{d}x & =(3 x + 7)\cdot \frac{e^{8 x - 3}}{8}-\int \frac{e^{8 x - 3}}{8}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 7)e^{8 x - 3}\,\text{d}x & =\frac{1}{8}(3 x + 7)e^{8 x - 3}-\frac{3}{8}\int e^{8 x - 3}\,\text{d}x \\  & =\frac{1}{8}(3 x + 7)e^{8 x - 3}-\frac{3}{64}e^{8 x - 3}+C\end{aligned}
$$

---

## Source replay q-2420

### moderate — base_equals

$\int x5^{x}\,\text{d}x=$

- $\frac{5^{x}}{\ln{(5 )}}(x - \frac{1}{\ln{(5 )}})+C$ **correct**
- $\frac{5^{x}}{\ln{(5 )}}(x - 1)+C$
- $\frac{5^{x}}{\ln{(5 )}}(- \frac{x}{\ln{(5 )}} + \frac{1}{x})+C$
- $\frac{5^{x}}{\ln{(5 )}}(x + \frac{1}{\ln{(5 )}})+C$
- $\frac{5^{x}}{\ln{(5 )}}(- \frac{x}{\ln{(5 )}} + 1)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x5^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =5^{x}\, & ⟹\,v=\frac{5^{x}}{\ln{(5 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 5^{x}\,\text{d}x & =x\cdot \frac{5^{x}}{\ln{(5 )}}-\int \frac{5^{x}}{\ln{(5 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x5^{x}\,\text{d}x & =\frac{5^{x} x}{\ln{(5 )}}-\int \frac{5^{x}}{\ln{(5 )}}\,\text{d}x \\  & =\frac{1}{\ln{(5 )}}x5^{x}-\frac{1}{\ln{(5 )}^{2}}5^{x}+C \\  & =\frac{5^{x}}{\ln{(5 )}}(x - \frac{1}{\ln{(5 )}})+C\end{aligned}
$$

---

## Generated empirical-profile variant q-2420

### moderate — base_equals

$\int x4^{x}\,\text{d}x=$

- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(4^{x} )} - 1}{\ln{(4 )}})+C$ **correct**
- $\frac{4^{x}}{\ln{(4 )}}(x - 1)+C$
- $\frac{4^{x}}{\ln{(4 )}}(- \frac{x}{\ln{(4 )}} + \frac{1}{x})+C$
- $\frac{4^{x}}{\ln{(4 )}}(\frac{\ln{(4^{x} )} + 1}{\ln{(4 )}})+C$
- $\frac{4^{x}}{\ln{(4 )}}(- \frac{x}{\ln{(4 )}} + 1)+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Source replay q-114291

### hard — hard_positive_factor

Calculate the integral $\int (2 x + 1)e^{3 x}\,\text{d}x.$

- $\frac{(6 x + 4) e^{3 x}}{3}+C$
- $\frac{(6 x + 1) e^{3 x}}{9}+C$ **correct**
- $\frac{(3 x + 2) e^{3 x}}{9}+C$
- $\frac{(4 x - 1) e^{3 x}}{3}+C$
- $\frac{(4 x - 3) e^{3 x}}{9}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (2 x + 1)e^{3 x}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =2 x + 1\, & ⟹\,{u}^{′}=2 \\ {v}^{′} & =e^{3 x}\, & ⟹\,v=\frac{e^{3 x}}{3}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (2 x + 1)\cdot e^{3 x}\,\text{d}x & =(2 x + 1)\cdot \frac{e^{3 x}}{3}-\int \frac{e^{3 x}}{3}\cdot 2\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (2 x + 1)e^{3 x}\,\text{d}x & =\frac{1}{3}(2 x + 1)e^{3 x}-\frac{2}{3}\int e^{3 x}\,\text{d}x \\  & =\frac{1}{3}(2 x + 1)e^{3 x}-\frac{2}{9}e^{3 x}+C \\  & =(\frac{6 x + 1}{9})e^{3 x}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-114291

### hard — hard_positive_factor

Calculate the integral $\int (3 x + 7)e^{8 x}\,\text{d}x.$

- $\frac{(4 x + 3) e^{8 x}}{64}+C$
- $\frac{(5 x - 7) e^{8 x}}{8}+C$
- $\frac{(24 x + 6) e^{8 x}}{8}+C$
- $\frac{(5 x - 8) e^{8 x}}{64}+C$
- $\frac{(24 x + 53) e^{8 x}}{64}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 7)e^{8 x}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 7\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{8 x}\, & ⟹\,v=\frac{e^{8 x}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 7)\cdot e^{8 x}\,\text{d}x & =(3 x + 7)\cdot \frac{e^{8 x}}{8}-\int \frac{e^{8 x}}{8}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 7)e^{8 x}\,\text{d}x & =\frac{1}{8}(3 x + 7)e^{8 x}-\frac{3}{8}\int e^{8 x}\,\text{d}x \\  & =\frac{1}{8}(3 x + 7)e^{8 x}-\frac{3}{64}e^{8 x}+C \\  & =(\frac{24 x + 53}{64})e^{8 x}+C\end{aligned}
$$

---

## Source replay q-12558

### moderate — e_shift

$\int 3 xe^{2 x + 5}\,\text{d}x=$

- $\frac{3 e^{2 x + 5}}{2}- \frac{3 x e^{2 x + 5}}{4}+C$
- $\frac{3 e^{2 x}}{2}- \frac{3 x e^{2 x}}{4}+C$
- $\frac{x e^{2 x + 5}}{4}+\frac{3 e^{2 x + 5}}{4}+C$
- $\frac{e^{2 x + 5}}{2}+\frac{3 e^{2 x + 5}}{4}+C$
- $\frac{3 x e^{2 x + 5}}{2}- \frac{3 e^{2 x + 5}}{4}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{2 x + 5}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{2 x + 5}\, & ⟹\,v=\frac{e^{2 x + 5}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{2 x + 5}\,\text{d}x & =3 x\cdot \frac{e^{2 x + 5}}{2}-\int \frac{e^{2 x + 5}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{2 x + 5}\,\text{d}x & =\frac{1}{2}3 xe^{2 x + 5}-\frac{3}{2}\int e^{2 x + 5}\,\text{d}x \\  & =\frac{1}{2}3 xe^{2 x + 5}-\frac{3}{4}e^{2 x + 5}+C\end{aligned}
$$

---

## Generated empirical-profile variant q-12558

### moderate — e_shift

$\int 3 xe^{8 x + 7}\,\text{d}x=$

- $\frac{x e^{8 x + 7}}{64}+\frac{3 e^{8 x + 7}}{64}+C$
- $\frac{e^{8 x + 7}}{8}+\frac{3 e^{8 x + 7}}{64}+C$
- $\frac{3 e^{8 x + 7}}{8}- \frac{3 x e^{8 x + 7}}{64}+C$
- $\frac{3 x e^{8 x + 7}}{8}- \frac{3 e^{8 x + 7}}{64}+C$ **correct**
- $\frac{3 e^{8 x}}{8}- \frac{3 x e^{8 x}}{64}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{8 x + 7}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{8 x + 7}\, & ⟹\,v=\frac{e^{8 x + 7}}{8}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{8 x + 7}\,\text{d}x & =3 x\cdot \frac{e^{8 x + 7}}{8}-\int \frac{e^{8 x + 7}}{8}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{8 x + 7}\,\text{d}x & =\frac{1}{8}3 xe^{8 x + 7}-\frac{3}{8}\int e^{8 x + 7}\,\text{d}x \\  & =\frac{1}{8}3 xe^{8 x + 7}-\frac{3}{64}e^{8 x + 7}+C\end{aligned}
$$

---

## Generated authored default e_positive/0

### easy — e_positive

$\int 7 xe^{7 x}\,\text{d}x=$

- $\frac{6 x e^{7 x}}{7}+C$
- $x e^{7 x} + \frac{e^{7 x}}{7}+C$
- $- x e^{7 x} - \frac{e^{7 x}}{7}+C$
- $x e^{7 x}+C$
- $\frac{1}{7}7 xe^{7 x}-\frac{1}{7}e^{7 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 xe^{7 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{7 x}\, & ⟹\,v=\frac{e^{7 x}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot e^{7 x}\,\text{d}x & =7 x\cdot \frac{e^{7 x}}{7}-\int \frac{e^{7 x}}{7}\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 7 xe^{7 x}\,\text{d}x & =\frac{1}{7}7 xe^{7 x}-\int e^{7 x}\,\text{d}x \\  & =\frac{1}{7}7 xe^{7 x}-\frac{1}{7}e^{7 x}+C\end{aligned}
$$

---

## Generated authored default e_positive/1

### easy — e_positive

$\int 3 xe^{2 x}\,\text{d}x=$

- $- \frac{3 x e^{2 x}}{2} - \frac{3 e^{2 x}}{4}+C$
- $\frac{3 x e^{2 x}}{4}+C$
- $\frac{3 x e^{2 x}}{2} + \frac{3 e^{2 x}}{4}+C$
- $\frac{1}{2}3 xe^{2 x}-\frac{3}{4}e^{2 x}+C$ **correct**
- $\frac{3 x e^{2 x}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{2 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{2 x}\, & ⟹\,v=\frac{e^{2 x}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{2 x}\,\text{d}x & =3 x\cdot \frac{e^{2 x}}{2}-\int \frac{e^{2 x}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{2 x}\,\text{d}x & =\frac{1}{2}3 xe^{2 x}-\frac{3}{2}\int e^{2 x}\,\text{d}x \\  & =\frac{1}{2}3 xe^{2 x}-\frac{3}{4}e^{2 x}+C\end{aligned}
$$

---

## Generated authored default e_negative_distributed/0

### moderate — e_negative_distributed

Calculate $\int 7 xe^{- 7 x}\,\text{d}x.$

- $- \frac{8 x e^{- 7 x}}{7}+C$
- $- x e^{- 7 x} + \frac{e^{- 7 x}}{7}+C$
- $x e^{- 7 x} - \frac{e^{- 7 x}}{7}+C$
- $- x e^{- 7 x}+C$
- $- \frac{1}{7}7 xe^{- 7 x}-\frac{1}{7}e^{- 7 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 xe^{- 7 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{- 7 x}\, & ⟹\,v=- \frac{e^{- 7 x}}{7}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot e^{- 7 x}\,\text{d}x & =7 x\cdot (- \frac{e^{- 7 x}}{7})-\int (- \frac{e^{- 7 x}}{7})\cdot 7\,\text{d}x \\  & =- \frac{1}{7}7 xe^{- 7 x}+\int e^{- 7 x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 7 xe^{- 7 x}\,\text{d}x & =- \frac{1}{7}7 xe^{- 7 x}+\int e^{- 7 x}\,\text{d}x \\  & =- \frac{1}{7}7 xe^{- 7 x}-\frac{1}{7}e^{- 7 x}+C\end{aligned}
$$

---

## Generated authored default e_negative_distributed/1

### moderate — e_negative_distributed

Calculate $\int 3 xe^{- 2 x}\,\text{d}x.$

- $\frac{3 x e^{- 2 x}}{2} - \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{9 x e^{- 2 x}}{4}+C$
- $- \frac{3 x e^{- 2 x}}{2} + \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{1}{2}3 xe^{- 2 x}-\frac{3}{4}e^{- 2 x}+C$ **correct**
- $- \frac{3 x e^{- 2 x}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- 2 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 2 x}\, & ⟹\,v=- \frac{e^{- 2 x}}{2}.\end{aligned}
$$

We, substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- 2 x}\,\text{d}x & =3 x\cdot (- \frac{e^{- 2 x}}{2})-\int (- \frac{e^{- 2 x}}{2})\cdot 3\,\text{d}x \\  & =- \frac{1}{2}3 xe^{- 2 x}+\frac{3}{2}\int e^{- 2 x}\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- 2 x}\,\text{d}x & =- \frac{1}{2}3 xe^{- 2 x}+\frac{3}{2}\int e^{- 2 x}\,\text{d}x \\  & =- \frac{1}{2}3 xe^{- 2 x}-\frac{3}{4}e^{- 2 x}+C\end{aligned}
$$

---

## Generated authored default e_negative_integral/0

### moderate — e_negative_integral

Calculate the integral $\int 7 xe^{- 7 x}\,\text{d}x.$

- $- \frac{8 x e^{- 7 x}}{7}+C$
- $- x e^{- 7 x} + \frac{e^{- 7 x}}{7}+C$
- $x e^{- 7 x} - \frac{e^{- 7 x}}{7}+C$
- $- x e^{- 7 x}+C$
- $- \frac{1}{7}7 xe^{- 7 x}-\frac{1}{7}e^{- 7 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 xe^{- 7 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{- 7 x}\, & ⟹\,v=- \frac{e^{- 7 x}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot e^{- 7 x}\,\text{d}x & =7 x\cdot (- \frac{e^{- 7 x}}{7})-\int (- \frac{e^{- 7 x}}{7})\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 7 xe^{- 7 x}\,\text{d}x & =- \frac{1}{7}7 xe^{- 7 x}+\int e^{- 7 x}\,\text{d}x \\  & =- \frac{1}{7}7 xe^{- 7 x}-\frac{1}{7}e^{- 7 x}+C\end{aligned}
$$

---

## Generated authored default e_negative_integral/1

### moderate — e_negative_integral

Calculate the integral $\int 3 xe^{- 2 x}\,\text{d}x.$

- $\frac{3 x e^{- 2 x}}{2} - \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{9 x e^{- 2 x}}{4}+C$
- $- \frac{3 x e^{- 2 x}}{2} + \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{1}{2}3 xe^{- 2 x}-\frac{3}{4}e^{- 2 x}+C$ **correct**
- $- \frac{3 x e^{- 2 x}}{2}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{- 2 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 2 x}\, & ⟹\,v=- \frac{e^{- 2 x}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{- 2 x}\,\text{d}x & =3 x\cdot (- \frac{e^{- 2 x}}{2})-\int (- \frac{e^{- 2 x}}{2})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{- 2 x}\,\text{d}x & =- \frac{1}{2}3 xe^{- 2 x}+\frac{3}{2}\int e^{- 2 x}\,\text{d}x \\  & =- \frac{1}{2}3 xe^{- 2 x}-\frac{3}{4}e^{- 2 x}+C\end{aligned}
$$

---

## Generated authored default e_shift/0

### moderate — e_shift

$\int 7 xe^{7 x - 7}\,\text{d}x=$

- $\frac{1}{7}7 xe^{7 x - 7}-\frac{1}{7}e^{7 x - 7}+C$ **correct**
- $\frac{6 x e^{7 x - 7}}{7}+C$
- $x e^{7 x - 7} + \frac{e^{7 x - 7}}{7}+C$
- $- x e^{7 x - 7} - \frac{e^{7 x - 7}}{7}+C$
- $x e^{7 x - 7}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 7 xe^{7 x - 7}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{7 x - 7}\, & ⟹\,v=\frac{e^{7 x - 7}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 7 x\cdot e^{7 x - 7}\,\text{d}x & =7 x\cdot \frac{e^{7 x - 7}}{7}-\int \frac{e^{7 x - 7}}{7}\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 7 xe^{7 x - 7}\,\text{d}x & =\frac{1}{7}7 xe^{7 x - 7}-\int e^{7 x - 7}\,\text{d}x \\  & =\frac{1}{7}7 xe^{7 x - 7}-\frac{1}{7}e^{7 x - 7}+C\end{aligned}
$$

---

## Generated authored default e_shift/1

### moderate — e_shift

$\int 3 xe^{2 x + 1}\,\text{d}x=$

- $\frac{3 x e^{2 x + 1}}{4}+C$
- $\frac{3 x e^{2 x + 1}}{2}+C$
- $\frac{3 x e^{2 x + 1}}{2} + \frac{3 e^{2 x + 1}}{4}+C$
- $- \frac{3 x e^{2 x + 1}}{2} - \frac{3 e^{2 x + 1}}{4}+C$
- $\frac{1}{2}3 xe^{2 x + 1}-\frac{3}{4}e^{2 x + 1}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int 3 xe^{2 x + 1}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{2 x + 1}\, & ⟹\,v=\frac{e^{2 x + 1}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int 3 x\cdot e^{2 x + 1}\,\text{d}x & =3 x\cdot \frac{e^{2 x + 1}}{2}-\int \frac{e^{2 x + 1}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int 3 xe^{2 x + 1}\,\text{d}x & =\frac{1}{2}3 xe^{2 x + 1}-\frac{3}{2}\int e^{2 x + 1}\,\text{d}x \\  & =\frac{1}{2}3 xe^{2 x + 1}-\frac{3}{4}e^{2 x + 1}+C\end{aligned}
$$

---

## Generated authored default base_calculate/0

### moderate — base_calculate

Calculate $\int x8^{x}\,\text{d}x.$

- $- \frac{8^{x} x}{\ln{(8 )}^{2}} + \frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}} + \frac{8^{x}}{\ln{(8 )}^{2}}+C$
- $\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C$ **correct**
- $- \frac{8^{x} x}{\ln{(8 )}} - \frac{8^{x}}{\ln{(8 )}^{2}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x8^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =8^{x}\, & ⟹\,v=\frac{8^{x}}{\ln{(8 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 8^{x}\,\text{d}x & =x\cdot \frac{8^{x}}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x8^{x}\,\text{d}x & =\frac{8^{x} x}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\,\text{d}x \\  & =\frac{1}{\ln{(8 )}}x8^{x}-\frac{1}{\ln{(8 )}^{2}}8^{x}+C \\  & =\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C\end{aligned}
$$

---

## Generated authored default base_calculate/1

### moderate — base_calculate

Calculate $\int x4^{x}\,\text{d}x.$

- $\frac{4^{x} x}{\ln{(4 )}}+C$
- $- \frac{4^{x} x}{\ln{(4 )}} - \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x} x}{\ln{(4 )}} + \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C$ **correct**
- $- \frac{4^{x} x}{\ln{(4 )}^{2}} + \frac{4^{x} x}{\ln{(4 )}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Generated authored default base_equals/0

### moderate — base_equals

$\int x8^{x}\,\text{d}x=$

- $- \frac{8^{x} x}{\ln{(8 )}^{2}} + \frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}} + \frac{8^{x}}{\ln{(8 )}^{2}}+C$
- $\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C$ **correct**
- $- \frac{8^{x} x}{\ln{(8 )}} - \frac{8^{x}}{\ln{(8 )}^{2}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x8^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =8^{x}\, & ⟹\,v=\frac{8^{x}}{\ln{(8 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 8^{x}\,\text{d}x & =x\cdot \frac{8^{x}}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x8^{x}\,\text{d}x & =\frac{8^{x} x}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\,\text{d}x \\  & =\frac{1}{\ln{(8 )}}x8^{x}-\frac{1}{\ln{(8 )}^{2}}8^{x}+C \\  & =\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C\end{aligned}
$$

---

## Generated authored default base_equals/1

### moderate — base_equals

$\int x4^{x}\,\text{d}x=$

- $\frac{4^{x} x}{\ln{(4 )}}+C$
- $- \frac{4^{x} x}{\ln{(4 )}} - \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x} x}{\ln{(4 )}} + \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C$ **correct**
- $- \frac{4^{x} x}{\ln{(4 )}^{2}} + \frac{4^{x} x}{\ln{(4 )}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Generated authored default base_legacy/0

### moderate — base_legacy

Calculate $\int x8^{x}dx$.

- $- \frac{8^{x} x}{\ln{(8 )}^{2}} + \frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}}+C$
- $\frac{8^{x} x}{\ln{(8 )}} + \frac{8^{x}}{\ln{(8 )}^{2}}+C$
- $\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C$ **correct**
- $- \frac{8^{x} x}{\ln{(8 )}} - \frac{8^{x}}{\ln{(8 )}^{2}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x8^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =8^{x}\, & ⟹\,v=\frac{8^{x}}{\ln{(8 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 8^{x}\,\text{d}x & =x\cdot \frac{8^{x}}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x8^{x}\,\text{d}x & =\frac{8^{x} x}{\ln{(8 )}}-\int \frac{8^{x}}{\ln{(8 )}}\,\text{d}x \\  & =\frac{1}{\ln{(8 )}}x8^{x}-\frac{1}{\ln{(8 )}^{2}}8^{x}+C \\  & =\frac{8^{x}}{\ln{(8 )}}(x - \frac{1}{\ln{(8 )}})+C\end{aligned}
$$

---

## Generated authored default base_legacy/1

### moderate — base_legacy

Calculate $\int x4^{x}dx$.

- $\frac{4^{x} x}{\ln{(4 )}}+C$
- $- \frac{4^{x} x}{\ln{(4 )}} - \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x} x}{\ln{(4 )}} + \frac{4^{x}}{\ln{(4 )}^{2}}+C$
- $\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C$ **correct**
- $- \frac{4^{x} x}{\ln{(4 )}^{2}} + \frac{4^{x} x}{\ln{(4 )}}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int x4^{x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =4^{x}\, & ⟹\,v=\frac{4^{x}}{\ln{(4 )}}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int x\cdot 4^{x}\,\text{d}x & =x\cdot \frac{4^{x}}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int x4^{x}\,\text{d}x & =\frac{4^{x} x}{\ln{(4 )}}-\int \frac{4^{x}}{\ln{(4 )}}\,\text{d}x \\  & =\frac{1}{\ln{(4 )}}x4^{x}-\frac{1}{\ln{(4 )}^{2}}4^{x}+C \\  & =\frac{4^{x}}{\ln{(4 )}}(x - \frac{1}{\ln{(4 )}})+C\end{aligned}
$$

---

## Generated authored default hard_shift_unit/0

### hard — hard_shift_unit

Calculate the integral $\int (x - 7)e^{x + 1}\,\text{d}x.$

- $(x - 8)e^{x + 1}+C$ **correct**
- $(x - 7) e^{x + 1}+C$
- $(x - 7) e^{x + 1} + e^{x + 1}+C$
- $(7 - x) e^{x + 1} - e^{x + 1}+C$
- $0+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x - 7)e^{x + 1}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x - 7\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{x + 1}\, & ⟹\,v=e^{x + 1}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x - 7)\cdot e^{x + 1}\,\text{d}x & =(x - 7)\cdot e^{x + 1}-\int e^{x + 1}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x - 7)e^{x + 1}\,\text{d}x & =(x - 7)e^{x + 1}-\int e^{x + 1}\,\text{d}x \\  & =(x - 7)e^{x + 1}-e^{x + 1}+C \\  & =(x - 8)e^{x + 1}+C\end{aligned}
$$

---

## Generated authored default hard_shift_unit/1

### hard — hard_shift_unit

Calculate the integral $\int (x + 1)e^{x - 5}\,\text{d}x.$

- $(x)e^{x - 5}+C$ **correct**
- $(x + 1) e^{x - 5}+C$
- $(x + 1) e^{x - 5} + e^{x - 5}+C$
- $0+C$
- $(- x - 1) e^{x - 5} - e^{x - 5}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (x + 1)e^{x - 5}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =x + 1\, & ⟹\,{u}^{′}=1 \\ {v}^{′} & =e^{x - 5}\, & ⟹\,v=e^{x - 5}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (x + 1)\cdot e^{x - 5}\,\text{d}x & =(x + 1)\cdot e^{x - 5}-\int e^{x - 5}\cdot 1\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (x + 1)e^{x - 5}\,\text{d}x & =(x + 1)e^{x - 5}-\int e^{x - 5}\,\text{d}x \\  & =(x + 1)e^{x - 5}-e^{x - 5}+C \\  & =(x)e^{x - 5}+C\end{aligned}
$$

---

## Generated authored default hard_negative_factor/0

### hard — hard_negative_factor

Calculate $\int (7 x - 7)e^{- 7 x}\,\text{d}x.$

- $(- \frac{7 x - 6}{7})e^{- 7 x}+C$ **correct**
- $- \frac{8 (7 x - 7) e^{- 7 x}}{49}+C$
- $- \frac{(7 x - 7) e^{- 7 x}}{7} + \frac{e^{- 7 x}}{7}+C$
- $- \frac{(7 - 7 x) e^{- 7 x}}{7} - \frac{e^{- 7 x}}{7}+C$
- $- \frac{(7 x - 7) e^{- 7 x}}{7}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)e^{- 7 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{- 7 x}\, & ⟹\,v=- \frac{e^{- 7 x}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot e^{- 7 x}\,\text{d}x & =(7 x - 7)\cdot (- \frac{e^{- 7 x}}{7})-\int (- \frac{e^{- 7 x}}{7})\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (7 x - 7)e^{- 7 x}\,\text{d}x & =- \frac{1}{7}(7 x - 7)e^{- 7 x}+\int e^{- 7 x}\,\text{d}x \\  & =- \frac{1}{7}(7 x - 7)e^{- 7 x}-\frac{1}{7}e^{- 7 x}+C \\  & =-\frac{(7 x - 6)e^{- 7 x}}{7}+C \\  & =(- \frac{7 x - 6}{7})e^{- 7 x}+C\end{aligned}
$$

---

## Generated authored default hard_negative_factor/1

### hard — hard_negative_factor

Calculate $\int (3 x + 1)e^{- 2 x}\,\text{d}x.$

- $- \frac{3 (3 x + 1) e^{- 2 x}}{4}+C$
- $- \frac{(3 x + 1) e^{- 2 x}}{2}+C$
- $- \frac{(3 x + 1) e^{- 2 x}}{2} + \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{(- 3 x - 1) e^{- 2 x}}{2} - \frac{3 e^{- 2 x}}{4}+C$
- $(- \frac{6 x + 5}{4})e^{- 2 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)e^{- 2 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 2 x}\, & ⟹\,v=- \frac{e^{- 2 x}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot e^{- 2 x}\,\text{d}x & =(3 x + 1)\cdot (- \frac{e^{- 2 x}}{2})-\int (- \frac{e^{- 2 x}}{2})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 1)e^{- 2 x}\,\text{d}x & =- \frac{1}{2}(3 x + 1)e^{- 2 x}+\frac{3}{2}\int e^{- 2 x}\,\text{d}x \\  & =- \frac{1}{2}(3 x + 1)e^{- 2 x}-\frac{3}{4}e^{- 2 x}+C \\  & =-\frac{(3 x + \frac{5}{2})e^{- 2 x}}{2}+C \\  & =(- \frac{6 x + 5}{4})e^{- 2 x}+C\end{aligned}
$$

---

## Generated authored default hard_negative_split/0

### hard — hard_negative_split

Calculate $\int (7 x - 7)e^{- 7 x}\,\text{d}x.$

- $- \frac{1}{7}(7 x - 7)e^{- 7 x}-\frac{1}{7}e^{- 7 x}+C$ **correct**
- $- \frac{8 (7 x - 7) e^{- 7 x}}{49}+C$
- $- \frac{(7 x - 7) e^{- 7 x}}{7} + \frac{e^{- 7 x}}{7}+C$
- $- \frac{(7 - 7 x) e^{- 7 x}}{7} - \frac{e^{- 7 x}}{7}+C$
- $- \frac{(7 x - 7) e^{- 7 x}}{7}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)e^{- 7 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{- 7 x}\, & ⟹\,v=- \frac{e^{- 7 x}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot e^{- 7 x}\,\text{d}x & =(7 x - 7)\cdot (- \frac{e^{- 7 x}}{7})-\int (- \frac{e^{- 7 x}}{7})\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (7 x - 7)e^{- 7 x}\,\text{d}x & =- \frac{1}{7}(7 x - 7)e^{- 7 x}+\int e^{- 7 x}\,\text{d}x \\  & =- \frac{1}{7}(7 x - 7)e^{- 7 x}-\frac{1}{7}e^{- 7 x}+C\end{aligned}
$$

---

## Generated authored default hard_negative_split/1

### hard — hard_negative_split

Calculate $\int (3 x + 1)e^{- 2 x}\,\text{d}x.$

- $- \frac{3 (3 x + 1) e^{- 2 x}}{4}+C$
- $- \frac{(3 x + 1) e^{- 2 x}}{2}+C$
- $- \frac{(3 x + 1) e^{- 2 x}}{2} + \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{(- 3 x - 1) e^{- 2 x}}{2} - \frac{3 e^{- 2 x}}{4}+C$
- $- \frac{1}{2}(3 x + 1)e^{- 2 x}-\frac{3}{4}e^{- 2 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)e^{- 2 x}\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{- 2 x}\, & ⟹\,v=- \frac{e^{- 2 x}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot e^{- 2 x}\,\text{d}x & =(3 x + 1)\cdot (- \frac{e^{- 2 x}}{2})-\int (- \frac{e^{- 2 x}}{2})\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 1)e^{- 2 x}\,\text{d}x & =- \frac{1}{2}(3 x + 1)e^{- 2 x}+\frac{3}{2}\int e^{- 2 x}\,\text{d}x \\  & =- \frac{1}{2}(3 x + 1)e^{- 2 x}-\frac{3}{4}e^{- 2 x}+C\end{aligned}
$$

---

## Generated authored default hard_shift_split/0

### hard — hard_shift_split

Calculate the integral $\int (7 x - 7)e^{7 x + 1}\,\text{d}x.$

- $\frac{1}{7}(7 x - 7)e^{7 x + 1}-\frac{1}{7}e^{7 x + 1}+C$ **correct**
- $\frac{(7 x - 7) e^{7 x + 1}}{7}+C$
- $\frac{(7 x - 7) e^{7 x + 1}}{7} + \frac{e^{7 x + 1}}{7}+C$
- $\frac{(7 - 7 x) e^{7 x + 1}}{7} - \frac{e^{7 x + 1}}{7}+C$
- $\frac{6 (7 x - 7) e^{7 x + 1}}{49}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)e^{7 x + 1}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{7 x + 1}\, & ⟹\,v=\frac{e^{7 x + 1}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot e^{7 x + 1}\,\text{d}x & =(7 x - 7)\cdot \frac{e^{7 x + 1}}{7}-\int \frac{e^{7 x + 1}}{7}\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (7 x - 7)e^{7 x + 1}\,\text{d}x & =\frac{1}{7}(7 x - 7)e^{7 x + 1}-\int e^{7 x + 1}\,\text{d}x \\  & =\frac{1}{7}(7 x - 7)e^{7 x + 1}-\frac{1}{7}e^{7 x + 1}+C\end{aligned}
$$

---

## Generated authored default hard_shift_split/1

### hard — hard_shift_split

Calculate the integral $\int (3 x + 1)e^{2 x - 5}\,\text{d}x.$

- $\frac{1}{2}(3 x + 1)e^{2 x - 5}-\frac{3}{4}e^{2 x - 5}+C$ **correct**
- $\frac{(3 x + 1) e^{2 x - 5}}{2}+C$
- $\frac{(3 x + 1) e^{2 x - 5}}{2} + \frac{3 e^{2 x - 5}}{4}+C$
- $\frac{(3 x + 1) e^{2 x - 5}}{4}+C$
- $\frac{(- 3 x - 1) e^{2 x - 5}}{2} - \frac{3 e^{2 x - 5}}{4}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)e^{2 x - 5}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{2 x - 5}\, & ⟹\,v=\frac{e^{2 x - 5}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot e^{2 x - 5}\,\text{d}x & =(3 x + 1)\cdot \frac{e^{2 x - 5}}{2}-\int \frac{e^{2 x - 5}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 1)e^{2 x - 5}\,\text{d}x & =\frac{1}{2}(3 x + 1)e^{2 x - 5}-\frac{3}{2}\int e^{2 x - 5}\,\text{d}x \\  & =\frac{1}{2}(3 x + 1)e^{2 x - 5}-\frac{3}{4}e^{2 x - 5}+C\end{aligned}
$$

---

## Generated authored default hard_positive_factor/0

### hard — hard_positive_factor

Calculate the integral $\int (7 x - 7)e^{7 x}\,\text{d}x.$

- $(\frac{7 x - 8}{7})e^{7 x}+C$ **correct**
- $\frac{6 (7 x - 7) e^{7 x}}{49}+C$
- $\frac{(7 x - 7) e^{7 x}}{7} + \frac{e^{7 x}}{7}+C$
- $\frac{(7 - 7 x) e^{7 x}}{7} - \frac{e^{7 x}}{7}+C$
- $\frac{(7 x - 7) e^{7 x}}{7}+C$

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (7 x - 7)e^{7 x}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =7 x - 7\, & ⟹\,{u}^{′}=7 \\ {v}^{′} & =e^{7 x}\, & ⟹\,v=\frac{e^{7 x}}{7}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (7 x - 7)\cdot e^{7 x}\,\text{d}x & =(7 x - 7)\cdot \frac{e^{7 x}}{7}-\int \frac{e^{7 x}}{7}\cdot 7\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (7 x - 7)e^{7 x}\,\text{d}x & =\frac{1}{7}(7 x - 7)e^{7 x}-\int e^{7 x}\,\text{d}x \\  & =\frac{1}{7}(7 x - 7)e^{7 x}-\frac{1}{7}e^{7 x}+C \\  & =(\frac{7 x - 8}{7})e^{7 x}+C\end{aligned}
$$

---

## Generated authored default hard_positive_factor/1

### hard — hard_positive_factor

Calculate the integral $\int (3 x + 1)e^{2 x}\,\text{d}x.$

- $\frac{(3 x + 1) e^{2 x}}{4}+C$
- $\frac{(3 x + 1) e^{2 x}}{2}+C$
- $\frac{(3 x + 1) e^{2 x}}{2} + \frac{3 e^{2 x}}{4}+C$
- $\frac{(- 3 x - 1) e^{2 x}}{2} - \frac{3 e^{2 x}}{4}+C$
- $(\frac{6 x - 1}{4})e^{2 x}+C$ **correct**

To solve this integral, we use the by-parts formula, given by

$$
\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.
$$

We need to express $\int (3 x + 1)e^{2 x}\,\text{d}x$ as $\int u{v}^{′}\,\text{d}x.$ Therefore, we set

$$
\begin{aligned}u & =3 x + 1\, & ⟹\,{u}^{′}=3 \\ {v}^{′} & =e^{2 x}\, & ⟹\,v=\frac{e^{2 x}}{2}.\end{aligned}
$$

We substitute the above into the integration by parts formula, and we get

$$
\begin{aligned}\int u{v}^{′}\,\text{d}x & =uv-\int v{u}^{′}\,\text{d}x \\ \int (3 x + 1)\cdot e^{2 x}\,\text{d}x & =(3 x + 1)\cdot \frac{e^{2 x}}{2}-\int \frac{e^{2 x}}{2}\cdot 3\,\text{d}x.\end{aligned}
$$

Finally, we calculate the integral, as follows:

$$
\begin{aligned}\int (3 x + 1)e^{2 x}\,\text{d}x & =\frac{1}{2}(3 x + 1)e^{2 x}-\frac{3}{2}\int e^{2 x}\,\text{d}x \\  & =\frac{1}{2}(3 x + 1)e^{2 x}-\frac{3}{4}e^{2 x}+C \\  & =(\frac{6 x - 1}{4})e^{2 x}+C\end{aligned}
$$
