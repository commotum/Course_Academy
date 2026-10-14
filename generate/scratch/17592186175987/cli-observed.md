![](/home/jake/Developer/Course_Academy/generate/scratch/17592186175987/plots/4fb6580304b6f348e611.png)

Consider the path $C$ shown above. Given that $F(x,y)=⟨5\left(y(x+1)\right),\,5\left(x(y+1)\right)⟩,$ which of the following is equivalent to ${∮}_{C}F\cdot dr\,?$

Field selection

$5\left({\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{2}{r}^{2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta \right)$

$5\left({\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{2}{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta \right)$

$5\left({\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{2}r(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta \right)$

$5\left({\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{2}r(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta \right)$

$5\left({\int }_{0}^{\pi /2}\,{\int }_{0}^{2}{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta \right)$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr=5\left({∮}_{C}y(x+1)\,dx+x(y+1)\,dy.\right)
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186175987/plots/ab0480791a0e1f735bf3.png)

Since $P(x,y)=5\left(y(x+1)\right)$ and $Q(x,y)=5\left(x(y+1)\right),$ we obtain

$$
\begin{aligned}\frac{∂P}{∂y}=5\left(x+1\right),\,\frac{∂Q}{∂x}=5\left(y+1\right).\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}5\left({∮}_{C}y(x+1)\,dx+x(y+1)\,dy\right) & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =5\left({∬}_{D}(y+1-(x+1))\,\text{d}A\right) \\  & =5\left({∬}_{D}(y-x)\,\text{d}A.\right)\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,\frac{\pi }{2}\le \theta \le \frac{3\pi }{2}}.
$$

The change of variables formula for plane polar coordinates states that  

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, we can write our double integral as 

$$
\begin{aligned}5\left({∬}_{D}(y-x)\,\text{d}A\right) & =5\left({∬}_{Δ}(r\operatorname{sin}⁡\theta -r\operatorname{cos}⁡\theta )\,r\,\text{d}r\text{d}\theta \right) \\  & =5\left({\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{2}{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta .\right)\end{aligned}
$$
