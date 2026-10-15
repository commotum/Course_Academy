Given that

$$
{∮}_{C}F\cdot dr={\int }_{0}^{2\pi }\,{\int }_{0}^{1}\boxed{}\,\text{d}r\,\text{d}\theta ,
$$

where $F(x,y)=⟨6y(x-1),\,6x(y-1)⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=1$ oriented counterclockwise, what is the missing part of the equation? Use $x=r\cos\theta$, $y=r\sin\theta$, and simplify the integrand pointwise before integration.

- $6 r^{2}$
- $6 r^{2} (\sin{(\theta )} - \cos{(\theta )})$
- $6 r \cos{(2 \theta )}$
- $6 r (\sin{(\theta )} - \cos{(\theta )})$
- $6 r^{2} \cos{(2 \theta )}$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}y(x-1)\,dx+x(y-1)\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/fb/fbf107e5d55e2dd51307b821d9d2f5134810317c69706a57f8d9aac528f78e93.png)

Since $P(x,y)=6y(x-1)$ and $Q(x,y)=6x(y-1),$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=6(x-1),\,\frac{∂Q}{∂x}=6(y-1).\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}y(x-1)\,dx+x(y-1)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}((6(y-1))-(6(x-1)))\,\text{d}A \\  & ={∬}_{D}(6(y-x))\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that 

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, we can write our double integral as 

$$
\begin{aligned}{∬}_{D}(6(y-x))\,\text{d}A & ={∬}_{Δ}(6(r\operatorname{sin}⁡\theta -r\operatorname{cos}⁡\theta ))\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,{\int }_{0}^{1}6{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

Given that ${∮}_C F\cdot dr=\int_0^{2\pi}\int_0^{1}\boxed{}\,dr\,d\theta$, where $F(x,y)=⟨6{y}^{3}+{e}^{x},\,\sqrt[3]{{y}^{2}+10}-3{x}^{3}⟩$ and $C$ is the circle $x^2+y^2=1$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?

- $9 r^{2} (\cos^{2}{(\theta )} - 2)$
- $- 9 r^{3} \cos^{2}{(\theta )}$
- $9 r^{3} (3 \sin^{2}{(\theta )} - 1)$
- $9 r^{3} (\cos^{2}{(\theta )} - 2)$
- $- 18 r^{3} \sin^{2}{(\theta )}$

First, notice that we can rewrite our integral as

$$
{∮}_{C}F\cdot dr={∮}_{C}(6{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-3{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/fb/fbf107e5d55e2dd51307b821d9d2f5134810317c69706a57f8d9aac528f78e93.png)

Since $P(x,y)=6{y}^{3}+{e}^{x}$ and $Q(x,y)=\sqrt[3]{{y}^{2}+10}-3{x}^{3},$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=18{y}^{2},\,\frac{∂Q}{∂x}=-9{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(6{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-3{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\ & ={∬}_{D}(-9{x}^{2}-18{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{aligned}{∬}_{D}(-9{x}^{2}-18{y}^{2})\,\text{d}A & ={∬}_{Δ}(-9\cdot (r\operatorname{cos}⁡\theta )^{2}-18\cdot (r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-9{r}^{2}{cos}^{2}⁡\theta -18{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-9{r}^{3}{cos}^{2}⁡\theta -18{r}^{3}{sin}^{2}⁡\theta )\,\text{d}r\text{d}\theta \\ & ={\int }_{0}^{2\pi }\,{\int }_{0}^{1}-9{r}^{3}{cos}^{2}⁡\theta -18{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

Given that ${∮}_C F\cdot dr=\int_0^{2\pi}\int_0^{5}\boxed{}\,dr\,d\theta$, where $F(x,y)=⟨3{y}^{3}+{e}^{x},\,\sqrt[3]{{y}^{2}+10}-2{x}^{3}⟩$ and $C$ is the circle $x^2+y^2=25$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?

- $3 r^{2} (\cos^{2}{(\theta )} - 3)$
- $3 r^{3} (5 \sin^{2}{(\theta )} - 2)$
- $3 r^{3} (\cos^{2}{(\theta )} - 3)$
- $- 9 r^{3} \sin^{2}{(\theta )}$
- $- 6 r^{3} \cos^{2}{(\theta )}$

First, notice that we can rewrite our integral as

$$
{∮}_{C}F\cdot dr={∮}_{C}(3{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-2{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/ee/ee7096a5ce1f420ac962f93b0efb47a00cdc2c9d9ec69f66b6340d02dd106b77.png)

Since $P(x,y)=3{y}^{3}+{e}^{x}$ and $Q(x,y)=\sqrt[3]{{y}^{2}+10}-2{x}^{3},$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=9{y}^{2},\,\frac{∂Q}{∂x}=-6{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(3{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-2{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\ & ={∬}_{D}(-6{x}^{2}-9{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{aligned}{∬}_{D}(-6{x}^{2}-9{y}^{2})\,\text{d}A & ={∬}_{Δ}(-6\cdot (r\operatorname{cos}⁡\theta )^{2}-9\cdot (r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-6{r}^{2}{cos}^{2}⁡\theta -9{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-6{r}^{3}{cos}^{2}⁡\theta -9{r}^{3}{sin}^{2}⁡\theta )\,\text{d}r\text{d}\theta \\ & ={\int }_{0}^{2\pi }\,{\int }_{0}^{5}-6{r}^{3}{cos}^{2}⁡\theta -9{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

Given that ${∮}_C F\cdot dr=\int_0^{2\pi}\int_0^{5}\boxed{}\,dr\,d\theta$, where $F(x,y)=⟨6{y}^{3}+{e}^{x},\,\sqrt[3]{{y}^{2}+10}-{x}^{3}⟩$ and $C$ is the circle $x^2+y^2=25$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?

- $3 r^{3} (5 \cos^{2}{(\theta )} - 6)$
- $- 18 r^{3} \sin^{2}{(\theta )}$
- $3 r^{3} (7 \sin^{2}{(\theta )} - 1)$
- $3 r^{2} (5 \cos^{2}{(\theta )} - 6)$
- $- 3 r^{3} \cos^{2}{(\theta )}$

First, notice that we can rewrite our integral as

$$
{∮}_{C}F\cdot dr={∮}_{C}(6{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/ee/ee7096a5ce1f420ac962f93b0efb47a00cdc2c9d9ec69f66b6340d02dd106b77.png)

Since $P(x,y)=6{y}^{3}+{e}^{x}$ and $Q(x,y)=\sqrt[3]{{y}^{2}+10}-{x}^{3},$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=18{y}^{2},\,\frac{∂Q}{∂x}=-3{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(6{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\ & ={∬}_{D}(-3{x}^{2}-18{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{aligned}{∬}_{D}(-3{x}^{2}-18{y}^{2})\,\text{d}A & ={∬}_{Δ}(-3\cdot (r\operatorname{cos}⁡\theta )^{2}-18\cdot (r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-3{r}^{2}{cos}^{2}⁡\theta -18{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-3{r}^{3}{cos}^{2}⁡\theta -18{r}^{3}{sin}^{2}⁡\theta )\,\text{d}r\text{d}\theta \\ & ={\int }_{0}^{2\pi }\,{\int }_{0}^{5}-3{r}^{3}{cos}^{2}⁡\theta -18{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

Given that ${∮}_C F\cdot dr=\int_0^{2\pi}\int_0^{6}\boxed{}\,dr\,d\theta$, where $F(x,y)=⟨3{y}^{3}+{e}^{x},\,\sqrt[3]{{y}^{2}+10}-6{x}^{3}⟩$ and $C$ is the circle $x^2+y^2=36$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?

- $- 18 r^{3} \cos^{2}{(\theta )}$
- $9 r^{3} (\sin^{2}{(\theta )} - 2)$
- $9 r^{3} (3 \sin^{2}{(\theta )} - 2)$
- $9 r^{2} (\sin^{2}{(\theta )} - 2)$
- $- 9 r^{3} \sin^{2}{(\theta )}$

First, notice that we can rewrite our integral as

$$
{∮}_{C}F\cdot dr={∮}_{C}(3{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-6{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/47/47ee81cb3603c75c8a83dca2df1153733902576892fa6eed3df4bccd329655ee.png)

Since $P(x,y)=3{y}^{3}+{e}^{x}$ and $Q(x,y)=\sqrt[3]{{y}^{2}+10}-6{x}^{3},$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=9{y}^{2},\,\frac{∂Q}{∂x}=-18{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(3{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-6{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\ & ={∬}_{D}(-18{x}^{2}-9{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 6,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{aligned}{∬}_{D}(-18{x}^{2}-9{y}^{2})\,\text{d}A & ={∬}_{Δ}(-18\cdot (r\operatorname{cos}⁡\theta )^{2}-9\cdot (r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-18{r}^{2}{cos}^{2}⁡\theta -9{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-18{r}^{3}{cos}^{2}⁡\theta -9{r}^{3}{sin}^{2}⁡\theta )\,\text{d}r\text{d}\theta \\ & ={\int }_{0}^{2\pi }\,{\int }_{0}^{6}-18{r}^{3}{cos}^{2}⁡\theta -9{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

Given that ${∮}_C F\cdot dr=\int_0^{2\pi}\int_0^{2}\boxed{}\,dr\,d\theta$, where $F(x,y)=⟨4{y}^{3}+{e}^{x},\,\sqrt[3]{{y}^{2}+10}-3{x}^{3}⟩$ and $C$ is the circle $x^2+y^2=4$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?

- $3 r^{3} (\cos^{2}{(\theta )} - 4)$
- $3 r^{2} (\cos^{2}{(\theta )} - 4)$
- $- 9 r^{3} \cos^{2}{(\theta )}$
- $3 r^{3} (7 \sin^{2}{(\theta )} - 3)$
- $- 12 r^{3} \sin^{2}{(\theta )}$

First, notice that we can rewrite our integral as

$$
{∮}_{C}F\cdot dr={∮}_{C}(4{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-3{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/06/06ecd3e3f2b2538556ffb2ffece12564b621f997ef8bf6de0e3297c7b86b393b.png)

Since $P(x,y)=4{y}^{3}+{e}^{x}$ and $Q(x,y)=\sqrt[3]{{y}^{2}+10}-3{x}^{3},$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=12{y}^{2},\,\frac{∂Q}{∂x}=-9{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(4{y}^{3}+{e}^{x})\,dx+(\sqrt[3]{{y}^{2}+10}-3{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\ & ={∬}_{D}(-9{x}^{2}-12{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{aligned}{∬}_{D}(-9{x}^{2}-12{y}^{2})\,\text{d}A & ={∬}_{Δ}(-9\cdot (r\operatorname{cos}⁡\theta )^{2}-12\cdot (r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-9{r}^{2}{cos}^{2}⁡\theta -12{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta \\ & ={∬}_{Δ}(-9{r}^{3}{cos}^{2}⁡\theta -12{r}^{3}{sin}^{2}⁡\theta )\,\text{d}r\text{d}\theta \\ & ={\int }_{0}^{2\pi }\,{\int }_{0}^{2}-9{r}^{3}{cos}^{2}⁡\theta -12{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$