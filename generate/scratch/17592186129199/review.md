# Originals and generated variants

All nine original banks are preserved. Each original is followed by two parameterized generated examples of its family; two examples for each authored hard family appear afterwards. q-161044 has an inferred key/authored moderate difficulty/authored solution. Original source worked solutions are shown as raw Markdown to make the two literal-set brace anomalies visible; generated solutions show their presentation repair. Every displayed radio choice is independently verified as a complete setup object.

Validation: 9/9 raw banks; 45/45 exact values; 8/8 observed keys + 1 independent inference; 6 raw-exact and 2 brace-normalized solutions; 155 real engine checks; 95 displayed-math records. Hard is authored, not observed. Scalar coincidences are in bank-collisions.json and do not define validity for this setup task.

## Original q-161044 — xy2

Observed unrated; moderate assignment is authored. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/e2fe61de100b4a469e4d79dc67869dd68936a0bf396757c4d08fb4d6cade6bda.png)

The region $D$ is the circle shown above. What is $∬_(D)xy^{2}dA$ expressed in polar coordinates?

1. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{5}r^{3}\cos θ\sin θdrdθ$
2. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{5}}r^{3}\cos θ\sin θdrdθ$
3. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{5}r^{4}\cos θ\sin^{2} θdrdθ$
4. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{\sqrt{5}}r^{4}\cos θ\sin^{2} θdrdθ$
5. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{5}}r^{4}\cos θ\sin^{2} θdrdθ$

Original solution (raw evidence):

```markdown
[No source worked solution captured]
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/70d8823d4045d6e2a1868ef8662860f35b56adb6c9c3451f9ecaa1c75a308c0a.png)

The region $D$ is the circle shown above. What is $\iint_D xy^2\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}r^{4}\cos θ\sin^{2} θdrdθ$ **Correct setup**
2. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{9}r^{4}\cos θ\sin^{2} θdrdθ$
3. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}r^{3}\cos θ\sin θdrdθ$
4. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{9}r^{3}\cos θ\sin θdrdθ$
5. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{3}r^{4}\cos θ\sin^{2} θdrdθ$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}A&=\iint_\Delta (r\cos\theta) (r\sin\theta)^{2}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{3}r^{4} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/88c3ce92eb86852bcf5ac6496a2f20cf8f93a87634a2afb3a1f4921d2f8ed856.png)

The region $D$ is the circle shown above. What is $\iint_D xy^2\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{25}r^{4}\cos θ\sin^{2} θdrdθ$
2. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{5}r^{4}\cos θ\sin^{2} θdrdθ$
3. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{5}r^{3}\cos θ\sin θdrdθ$
4. $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{25}r^{3}\cos θ\sin θdrdθ$
5. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{5}r^{4}\cos θ\sin^{2} θdrdθ$ **Correct setup**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}A&=\iint_\Delta (r\cos\theta) (r\sin\theta)^{2}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{5}r^{4} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

## Original q-38076 — twoxy

Observed :question.difficulty/moderate. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/bccbe3973fa63908f5e264f4566e1207c5019dc1de9c36ef42481428527aef3b.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}2xy\,\text{d}A$
expressed in polar coordinates?

1. ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
2. ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{1}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
5. ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $2$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{Δ}2(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}2{r}^{3}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 1}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/65b0dcf5add17db75b7838a76025f4cc8e6bfe61e3fac921dbcc617d6318fb7f.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}2xy\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{\pi}{\int }_{0}^{3}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{\frac{3}{2}}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{3}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{3}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi}{\int }_{0}^{3}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $ **Correct setup**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq \pi\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{Δ}2(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi}{\int }_{0}^{3}2{r}^{3}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi}{\int }_{0}^{3}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 2}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/2b9eb6f049e80574165b9924ab1602e77d31930ce6dad65a03115036d6b92a90.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}2xy\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\frac{5}{2}}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $ **Correct setup**
5. ${\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \frac{\pi}{2}\leq\theta\leq \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{Δ}2(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}2{r}^{3}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-161038 — exp

Observed :question.difficulty/moderate. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/aa5b04b98d3796656fca912d8dc1732ea7e12bab9083f8ca543ad5fd4fdb10ff.png)

The region $D$ is the quarter-circle shown above. What is ${∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A$ expressed in polar coordinates?

1. ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{2}{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{r}\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{2}{r}^{2}{e}^{r}\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }dr\,d\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $4$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 4,\,\pi \le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 1}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/27059422eff3c99fd1beb82db1e656e141ac0188cc8f3f093ff8a3f523034b9c.png)

The region $D$ is the quarter-circle shown above. What is ${∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{2 \pi}{\int }_{0}^{\frac{3}{2}}{r}^{2}{e}^{r}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi}^{2 \pi}{\int }_{0}^{3}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $ **Correct setup**
4. ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3}r{e}^{r}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{\frac{3}{2}}{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }dr\,d\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ \frac{3 \pi}{2}\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3}r{e}^{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 2}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/8be4a8efd7413c6e398601126505e7646c11b416ea65f09c7fcf1abddb251c2a.png)

The region $D$ is the quarter-circle shown above. What is ${∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{2 \pi}^{\frac{5 \pi}{2}}{\int }_{0}^{5}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $ **Correct setup**
2. ${\int }_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}{\int }_{0}^{\frac{5}{2}}{r}^{2}{e}^{r}\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{3 \pi}{2}}^{\frac{5 \pi}{2}}{\int }_{0}^{5}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
4. ${\int }_{2 \pi}^{\frac{5 \pi}{2}}{\int }_{0}^{\frac{5}{2}}{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{2 \pi}^{\frac{5 \pi}{2}}{\int }_{0}^{5}r{e}^{r}\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }dr\,d\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ 2 \pi\leq\theta\leq \frac{5 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{2 \pi}^{\frac{5 \pi}{2}}{\int }_{0}^{5}r{e}^{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{2 \pi}^{\frac{5 \pi}{2}}{\int }_{0}^{5}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-161039 — diff

Observed :question.difficulty/easy. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/cdd5f0c58228b47a0bbba77daf2b426ce0247e71259e2b5af1a4a80fa833a036.png)

The region $D$ is the circle shown above. What is ${∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A$ expressed in polar coordinates?

1. ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi }{\int }_{0}^{4}{r}^{2}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{4}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $2$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi }.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — easy

Parameters: `{"radius_squared": 9, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/70d8823d4045d6e2a1868ef8662860f35b56adb6c9c3451f9ecaa1c75a308c0a.png)

The region $D$ is the circle shown above. What is ${∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{2}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{9}{r}^{2}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — easy

Parameters: `{"radius_squared": 25, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/88c3ce92eb86852bcf5ac6496a2f20cf8f93a87634a2afb3a1f4921d2f8ed856.png)

The region $D$ is the circle shown above. What is ${∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{2\pi }{\int }_{0}^{25}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**
3. ${\int }_{0}^{\pi }{\int }_{0}^{25}{r}^{2}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{2}\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-161041 — log

Observed :question.difficulty/easy. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/6b077d20bcb79f293383a7810d1c46ad42ce78d17a8d631b01f66a9fd547f475.png)

The region $D$ is the circle shown above. What is ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A$ expressed in polar coordinates?

1. ${\int }_{0}^{2\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi }{\int }_{0}^{16}\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{16}{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{4}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $4$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 4,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — easy

Parameters: `{"radius_squared": 9, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/70d8823d4045d6e2a1868ef8662860f35b56adb6c9c3451f9ecaa1c75a308c0a.png)

The region $D$ is the circle shown above. What is ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{2\pi }{\int }_{0}^{3}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{9}\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{3}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $ **Correct setup**
5. ${\int }_{0}^{\pi }{\int }_{0}^{3}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — easy

Parameters: `{"radius_squared": 25, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/88c3ce92eb86852bcf5ac6496a2f20cf8f93a87634a2afb3a1f4921d2f8ed856.png)

The region $D$ is the circle shown above. What is ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{2\pi }{\int }_{0}^{25}{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi }{\int }_{0}^{5}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{25}\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{5}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $ **Correct setup**
5. ${\int }_{0}^{2\pi }{\int }_{0}^{5}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-83499 — sum

Observed :question.difficulty/moderate. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/8c3056de2634d5315aebcbc978bf279eeb95da736ab6796c9d86dc39d9feadc5.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A$
expressed in polar coordinates?

1. ${\int }_{3\pi /2}^{0}{\int }_{0}^{1}{r}^{2}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{-\pi /2}^{0}{\int }_{0}^{2}r\,\text{d}r\,\text{d}\theta $
3. ${\int }_{-\pi /2}^{0}{\int }_{0}^{1}{r}^{3}\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{-\pi /2}^{0}{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $2$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,-\frac{\pi }{2}\le \theta \le 0}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 1}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/48a472de5afdb1215e2990e737b3a1bdd52867a483c36a080d1f2c14c2a87cf2.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta $ **Correct setup**
2. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3}r\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{3}{r}^{2}\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\frac{3}{2}}{r}^{3}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{2 \pi}^{\frac{\pi}{2}}{\int }_{0}^{\frac{3}{2}}{r}^{2}\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 2}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/c629f589325c0447ba302c5f5e39ea3070fbc0146b4d1a89f65d74f46415293c.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{2}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}{r}^{3}\,\text{d}r\,\text{d}\theta $ **Correct setup**
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}r\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{5 \pi}{2}}^{\pi}{\int }_{0}^{\frac{5}{2}}{r}^{2}\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\frac{5}{2}}{r}^{3}\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \frac{\pi}{2}\leq\theta\leq \pi\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-83500 — linear

Observed :question.difficulty/moderate. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/55bbf6f55ce287321f2cc593ea48d65a78c655ca18d2a34df68b63c2bda92c8f.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}(x+y)\,\text{d}A$
expressed in polar coordinates?

1. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi }{\int }_{-\sqrt{2}}^{\sqrt{2}}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{-\sqrt{2}}^{\sqrt{2}}r\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{2}}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{2}}{r}^{2}\,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $\sqrt{2}$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le \sqrt{2},\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}(x+y)\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )+(r\operatorname{sin}⁡\theta ))\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{\sqrt{2}}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 1}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/fe7b50c9ba896a1deface85ccc1649b845144ef7aa40ef151cc41efffb05699f.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}(x+y)\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{-3}^{3}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $ **Correct setup**
4. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{-3}^{3}r\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\frac{5 \pi}{2}}{\int }_{0}^{3}r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ \frac{\pi}{2}\leq\theta\leq \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}(x+y)\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )+(r\operatorname{sin}⁡\theta ))\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 2}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/63d516c7eb6315bd93290ceef9ce0d4ab246828e7335949fff5a09001a6f0da1.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}(x+y)\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{2 \pi}{\int }_{0}^{5}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $ **Correct setup**
2. ${\int }_{\pi}^{2 \pi}{\int }_{0}^{5}{r}^{2}\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi}^{2 \pi}{\int }_{-5}^{5}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi}^{3 \pi}{\int }_{0}^{5}r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi}^{2 \pi}{\int }_{-5}^{5}r\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \pi\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}(x+y)\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )+(r\operatorname{sin}⁡\theta ))\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi}^{2 \pi}{\int }_{0}^{5}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-83954 — x

Observed :question.difficulty/moderate. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/a60d80425c240deb1ea372d7a21c3774247c4827536ce6f409f7e8736c7c94bc.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}x\,\text{d}A$
expressed in polar coordinates?

1. ${\int }_{-\pi }^{\pi }{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{\pi /2}{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi /2}^{\pi }{\int }_{-\sqrt{3}}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{-\sqrt{3}}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $\sqrt{3}$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le \sqrt{3},\,\frac{\pi }{2}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — moderate

Parameters: `{"radius_squared": 9, "rotation": 1}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/351d10dd598e7eb8e6f862476ef03303f0031e9e5fc829fd7a6f264cda903ff3.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}x\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**
2. ${\int }_{\pi}^{\pi}{\int }_{0}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{-3}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{-3}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{- \frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ \pi\leq\theta\leq \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi}^{\frac{3 \pi}{2}}{\int }_{0}^{3}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — moderate

Parameters: `{"radius_squared": 25, "rotation": 2}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/d1e7e1e6b0dfeb0a58214657e6577f8e9bb482b058fb78d2c6a4611d1b11db30.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}x\,\text{d}A$
expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{\pi}^{2 \pi}{\int }_{-5}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**
3. ${\int }_{\frac{3 \pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{-5}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \frac{3 \pi}{2}\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{5}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Original q-161043 — y2

Observed :question.difficulty/easy. Original raw bank follows; option order is captured order.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/2db1e29e5f911a45c4c48ab41c4ad6dc63eeb36a8112672ae66844e14342f4c0.png)

The region $D$ is the circle shown above. What is ${∬}_{D}{y}^{2}\,\text{d}A$ expressed in polar coordinates?

1. ${\int }_{0}^{2\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $

Original solution (raw evidence):

```markdown
We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{Δ}{(r\operatorname{sin}⁡\theta )}^{2}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$
```

### Generated variant 1 — easy

Parameters: `{"radius_squared": 9, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/70d8823d4045d6e2a1868ef8662860f35b56adb6c9c3451f9ecaa1c75a308c0a.png)

The region $D$ is the circle shown above. What is ${∬}_{D}{y}^{2}\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{\pi }{\int }_{0}^{9}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**
3. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{3}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ 0\leq\theta\leq 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{Δ}{(r\operatorname{sin}⁡\theta )}^{2}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Generated variant 2 — easy

Parameters: `{"radius_squared": 25, "rotation": 0}`; bank remains the complete observed profile.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/originals/2db1e29e5f911a45c4c48ab41c4ad6dc63eeb36a8112672ae66844e14342f4c0.png)

The region $D$ is the circle shown above. What is ${∬}_{D}{y}^{2}\,\text{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $ **Correct setup**
2. ${\int }_{0}^{\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, notice that the region $D$ represents the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{Δ}{(r\operatorname{sin}⁡\theta )}^{2}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Authored hard extension — root_product

No observed hard source exists. Same-method origin-centered quarter-sector rewrite with radial-root and double-angle simplification.

### Generated hard variant 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/49ff6d212a558d8ee811db8c8851af852e4bb7e6676ddf9cfafcf0cc08abde03.png)

The region $D$ is the quarter-circle shown above. What is $\iint_D 2 x y \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{6}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
2. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{3} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
3. $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{4}}\int_{0}^{3}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
4. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{5} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
5. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$ **Correct setup**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ \frac{\pi}{2}\leq\theta\leq \pi\}.
$$

Since $r\geq0$, $\sqrt{r^2}=r$; also $\cos^2\theta+\sin^2\theta=1$.

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 2 x y \sqrt{x^{2} + y^{2}}\,\mathrm{d}A&=\iint_\Delta 2 (r\cos\theta) (r\sin\theta) \sqrt{(r\cos\theta)^{2} + (r\sin\theta)^{2}}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}2r^3\cos\theta\sin\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}2r^4\cos\theta\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^4\sin(2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

### Generated hard variant 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/f443f81d0500adb614064dd63bd148f71bdb8e3aa26f44f10674cf3541b0f0e1.png)

The region $D$ is the quarter-circle shown above. What is $\iint_D 2 x y \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\int_{\pi}^{\frac{5 \pi}{4}}\int_{0}^{5}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
2. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{10}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
3. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{3} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
4. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{4} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$ **Correct setup**
5. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{5} \sin{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \pi\leq\theta\leq \frac{3 \pi}{2}\}.
$$

Since $r\geq0$, $\sqrt{r^2}=r$; also $\cos^2\theta+\sin^2\theta=1$.

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 2 x y \sqrt{x^{2} + y^{2}}\,\mathrm{d}A&=\iint_\Delta 2 (r\cos\theta) (r\sin\theta) \sqrt{(r\cos\theta)^{2} + (r\sin\theta)^{2}}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}2r^3\cos\theta\sin\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}2r^4\cos\theta\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^4\sin(2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

## Authored hard extension — root_difference

No observed hard source exists. Same-method origin-centered quarter-sector rewrite with radial-root and double-angle simplification.

### Generated hard variant 1

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/49ff6d212a558d8ee811db8c8851af852e4bb7e6676ddf9cfafcf0cc08abde03.png)

The region $D$ is the quarter-circle shown above. What is $\iint_D \left(x^{2} - y^{2}\right) \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{6}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
2. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{3} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
3. $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{4}}\int_{0}^{3}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
4. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{5} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
5. $\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$ **Correct setup**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $3$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 3,\ \frac{\pi}{2}\leq\theta\leq \pi\}.
$$

Since $r\geq0$, $\sqrt{r^2}=r$; also $\cos^2\theta+\sin^2\theta=1$.

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D \left(x^{2} - y^{2}\right) \sqrt{x^{2} + y^{2}}\,\mathrm{d}A&=\iint_\Delta \left((r\cos\theta)^{2} - (r\sin\theta)^{2}\right) \sqrt{(r\cos\theta)^{2} + (r\sin\theta)^{2}}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^3(\cos^2\theta-\sin^2\theta)\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^4(\cos^2\theta-\sin^2\theta)\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}r^4\cos(2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

### Generated hard variant 2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129199/plots/f443f81d0500adb614064dd63bd148f71bdb8e3aa26f44f10674cf3541b0f0e1.png)

The region $D$ is the quarter-circle shown above. What is $\iint_D \left(x^{2} - y^{2}\right) \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$ expressed in polar coordinates?

Choose a change-of-variables setup with $r\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.

1. $\int_{\pi}^{\frac{5 \pi}{4}}\int_{0}^{5}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
2. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{10}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
3. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{3} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$
4. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{4} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$ **Correct setup**
5. $\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^{5} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $5$ centered at the origin. In polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta):0\leq r\leq 5,\ \pi\leq\theta\leq \frac{3 \pi}{2}\}.
$$

Since $r\geq0$, $\sqrt{r^2}=r$; also $\cos^2\theta+\sin^2\theta=1$.

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D \left(x^{2} - y^{2}\right) \sqrt{x^{2} + y^{2}}\,\mathrm{d}A&=\iint_\Delta \left((r\cos\theta)^{2} - (r\sin\theta)^{2}\right) \sqrt{(r\cos\theta)^{2} + (r\sin\theta)^{2}}\,r\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^3(\cos^2\theta-\sin^2\theta)\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^4(\cos^2\theta-\sin^2\theta)\,\mathrm{d}r\,\mathrm{d}\theta \\ &=\int_{\pi}^{\frac{3 \pi}{2}}\int_{0}^{5}r^4\cos(2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\end{aligned}
$$

