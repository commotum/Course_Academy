# Green’s theorem area setup: original evidence and generated variants

Raw originals preserve the captured banks and missing attributes; they are evidence-only. Generated variants use a complete authored bank whose full integral values are pairwise unequal. Correctness, repair and fidelity are counted separately in validation.json.

### Original q-41466 — raw evidence

## ellipse_ccw (observed_raw; {'a': 3, 'b': 2})

![](images/1d/1de9544b8da50f6280920adf2292da517a844b8b4143f58f646da0a01ffad16c.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\operatorname{cos}⁡t,\,2\operatorname{sin}⁡t⟩$ for $t\in [0,2\pi ].$ The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

- $6({cos}^{2}⁡t-{sin}^{2}⁡t)$
- $6({sin}^{2}⁡t-{cos}^{2}⁡t)$
- $6\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $6{cos}^{2}⁡t$
- $6{sin}^{2}⁡t$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨-3\operatorname{sin}⁡t,\,2\operatorname{cos}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{0}^{2\pi }3\operatorname{cos}⁡t\cdot 2\operatorname{cos}⁡t\,dt \\  & ={\int }_{0}^{2\pi }6{cos}^{2}⁡t\,dt.\end{aligned}
$$

### Original q-42238 — raw evidence

## ellipse_cw (observed_raw; {'a': 2, 'b': 3})

![](images/6f/6f51a25843259881994e3dca0781b780878bec349930b76fbf449dc824e69ec2.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\operatorname{sin}⁡t,\,3\operatorname{cos}⁡t⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $6\cos^{2} t$
- $-6\sin^{2} t$
- $-6\cos^{2} t$
- $6\sin t\cos t$
- $-6\sin t\cos t$

- $-6{sin}^{2}⁡t$
- $-6{cos}^{2}⁡t$
- $6\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $-6\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $6{cos}^{2}⁡t$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\operatorname{cos}⁡t,\,-3\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }3\operatorname{cos}⁡t\cdot 2\operatorname{cos}⁡t\,dt \\  & ={\int }_{0}^{2\pi }6{cos}^{2}⁡t\,dt.\end{aligned}
$$

### Original q-42221 — raw evidence

## exp_ccw (observed_raw; {'a': 1, 'b': 1})

![](images/44/4408d1fcee1d168c6ab21ea53cf24845093bad9cc608299a36f0510c1636cc03.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t) = ⟨e^{\cos t}, e^{\sin t}⟩$ for $t ∈ [0, 2π]$. The area of $D$ can be written as

$Area(D) = ∬_(D)(\frac{∂Q}{∂x} - \frac{∂P}{∂y})dA = \displaystyle \int_{0}^{2π}AAAAAAAdt$,

where $P(x, y) = 0$ and $Q(x, y) = x$. Determine the missing part of the equation.

- $\sin te^{\cos t}$
- $\cos te^{\cos t}$
- $\cos te^{\cos t + \sin t}$
- $-\sin te^{\cos t + \sin t}$
- $-\sin te^{\sin t}$

Worked solution:

[Absent in raw evidence]

### Original q-126750 — raw evidence

## exp_cw (observed_raw; {'a': 1, 'b': 1})

![](images/0d/0d988bfd18a945ba96c3556775d4aebc706252e2baf02d5f76c108e5534baed1.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨{e}^{\operatorname{sin}⁡t},\,{e}^{\operatorname{cos}⁡t}⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $-\operatorname{sin}⁡t\,{e}^{2\operatorname{cos}⁡t}$
- $\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$
- $-\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$
- $-\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$
- $\operatorname{cos}⁡t\,{e}^{2\operatorname{sin}⁡t}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨\operatorname{cos}⁡t\,{e}^{\operatorname{sin}⁡t},\,-\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }{e}^{\operatorname{cos}⁡t}\cdot \operatorname{cos}⁡t\,{e}^{\operatorname{sin}⁡t}\,dt \\  & ={\int }_{0}^{2\pi }\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}\,dt.\end{aligned}
$$

### Original q-126751 — raw evidence

## double_sine (observed_raw; {'a': 2, 'b': 3})

![](images/81/81da86ae54a837b954bf93f8a75d93e1e7a8b64c93ba6f6b06cf74b2d8fa7ecb.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\operatorname{sin}⁡t,\,3\operatorname{sin}⁡2t⟩$ for $t\in [0,\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $-4\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $-12\operatorname{sin}⁡t\operatorname{cos}⁡2t$
- $-18\operatorname{sin}⁡2t\operatorname{cos}⁡2t$
- $-6\operatorname{sin}⁡2t\operatorname{cos}⁡t$
- $6\operatorname{sin}⁡2t\operatorname{cos}⁡t$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\operatorname{cos}⁡t,\,6\operatorname{cos}⁡2t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{\pi }(-2\operatorname{sin}⁡t)\cdot 6\operatorname{cos}⁡2t\,dt \\  & ={\int }_{0}^{\pi }-12\operatorname{sin}⁡t\operatorname{cos}⁡2t\,dt.\end{aligned}
$$

### Original q-126748 — raw evidence

## double_cos (observed_raw; {'a': 2, 'b': 1})

![](images/65/6571fcdf94818485c2a39e90e018d46e9c95e1acbe0a8cf2f67c688d160a347c.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\operatorname{sin}⁡2t,\,\operatorname{cos}⁡t⟩$ for $t\in [-\frac{\pi }{2},\frac{\pi }{2}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{-\pi /2}^{\pi /2}\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $-\operatorname{cos}⁡t\operatorname{sin}⁡t$
- $2\operatorname{sin}⁡2t\operatorname{sin}⁡t$
- $4\operatorname{cos}⁡t\operatorname{cos}⁡2t$
- $-8\operatorname{sin}⁡2t\operatorname{cos}⁡2t$
- $-2\operatorname{sin}⁡2t\operatorname{sin}⁡t$

Worked solution:

Our simple, piecewise smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨4\operatorname{cos}⁡2t,\,-\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{-\pi /2}^{\pi /2}\operatorname{cos}⁡t\cdot 4\operatorname{cos}⁡2t\,dt \\  & ={\int }_{-\pi /2}^{\pi /2}4\operatorname{cos}⁡t\operatorname{cos}⁡2t\,dt.\end{aligned}
$$

### Original q-126760 — raw evidence

## mixed (observed_raw; {'a': 1, 'b': 1})

![](images/a9/a95b161dab89fe1245724921ef4ee36112d7a4062e7e171411e4ffe61253b91f.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨\operatorname{sin}⁡t-\operatorname{sin}⁡2t,\,\operatorname{cos}⁡t-\operatorname{cos}⁡2t⟩$ for $t\in [\frac{\pi }{3},\frac{5\pi }{3}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{\pi /3}^{5\pi /3}\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $(\operatorname{sin}⁡t-\operatorname{sin}⁡2t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $(\operatorname{cos}⁡2t-\operatorname{cos}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(\operatorname{cos}⁡t-2\operatorname{cos}⁡2t)$
- $(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $(\operatorname{cos}⁡2t-\operatorname{cos}⁡t)(\operatorname{cos}⁡t-2\operatorname{cos}⁡2t)$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨\operatorname{cos}⁡t-2\operatorname{cos}⁡2t,\,-\operatorname{sin}⁡t+2\operatorname{sin}⁡2t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{\pi /3}^{5\pi /3}(-\operatorname{sin}⁡t+\operatorname{sin}⁡2t)\cdot (-\operatorname{sin}⁡t+2\operatorname{sin}⁡2t)\,dt \\  & ={\int }_{\pi /3}^{5\pi /3}(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)\,dt.\end{aligned}
$$

### Original q-126761 — raw evidence

## power (observed_raw; {'a': 1, 'b': 1, 'm': 5})

![](images/10/10f4094edb09afc7908bd0cd3df089387c8f5b762ea5ef86da152d1c9d08b5e4.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨{sin}^{5}⁡t,\,{cos}^{5}⁡t⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $5{cos}^{5}⁡t\operatorname{sin}⁡t$
- $-5{cos}^{5}⁡t{sin}^{5}⁡t$
- $5{cos}^{6}⁡t{sin}^{4}⁡t$
- $5{sin}^{6}⁡t{cos}^{4}⁡t$
- $-5{sin}^{6}⁡t{cos}^{4}⁡t$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨5{sin}^{4}⁡t\operatorname{cos}⁡t,\,-5{cos}^{4}⁡t\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-{sin}^{5}⁡t)\cdot (-5{cos}^{4}⁡t\operatorname{sin}⁡t)\,dt \\  & ={\int }_{0}^{2\pi }5{sin}^{6}⁡t{cos}^{4}⁡t\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-41466 (learner-ineligible)

## ellipse_ccw (observed_raw; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/7649f93c85abfa55a8e490b55b41b8d0be48774691684df08dd5c87c83568fe8.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\operatorname{cos}⁡t,\,4\operatorname{sin}⁡t⟩$ for $t\in [0,2\pi ].$ The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

- $8({sin}^{2}⁡t-{cos}^{2}⁡t)$
- $8{sin}^{2}⁡t$
- $8({cos}^{2}⁡t-{sin}^{2}⁡t)$
- $8{cos}^{2}⁡t$
- $8\operatorname{sin}⁡t\operatorname{cos}⁡t$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨-2\operatorname{sin}⁡t,\,4\operatorname{cos}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{0}^{2\pi }2\operatorname{cos}⁡t\cdot 4\operatorname{cos}⁡t\,dt \\  & ={\int }_{0}^{2\pi }8{cos}^{2}⁡t\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-42238 (learner-ineligible)

## ellipse_cw (observed_raw; {'a': 3, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/4e40b2ebcb6c69328b34afbf17e72be606c5f8cd562c1e4a173aa2241decd727.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\operatorname{sin}⁡t,\,4\operatorname{cos}⁡t⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $-12\sin^{2} t$
- $-12\sin t\cos t$
- $12\cos^{2} t$
- $12\sin t\cos t$
- $-12\cos^{2} t$

- $-12{sin}^{2}⁡t$
- $12\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $12{cos}^{2}⁡t$
- $-12{cos}^{2}⁡t$
- $-12\operatorname{sin}⁡t\operatorname{cos}⁡t$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3\operatorname{cos}⁡t,\,-4\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }4\operatorname{cos}⁡t\cdot 3\operatorname{cos}⁡t\,dt \\  & ={\int }_{0}^{2\pi }12{cos}^{2}⁡t\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-42221 (learner-ineligible)

## exp_ccw (observed_raw; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/e76d58b53395442025b94ca72ffd891dd7f61c5de0137e6293b2f6cd160919f1.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t) = ⟨2e^{\cos t}, 4e^{\sin t}⟩$ for $t ∈ [0, 2π]$. The area of $D$ can be written as

$Area(D) = ∬_(D)(\frac{∂Q}{∂x} - \frac{∂P}{∂y})dA = \displaystyle \int_{0}^{2π}AAAAAAAdt$,

where $P(x, y) = 0$ and $Q(x, y) = x$. Determine the missing part of the equation.

- $4\cos te^{\cos t}$
- $-4\sin te^{\sin t}$
- $2\sin te^{\cos t}$
- $-8\sin te^{\cos t + \sin t}$
- $8\cos te^{\cos t + \sin t}$

Worked solution:

[Absent in raw evidence]

### Generated changed-parameter evidence — source bank q-126750 (learner-ineligible)

## exp_cw (observed_raw; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/044271d96422f79d0c3c2cba3707c03db3fc0bdf20805972a4563e6204d3e4f5.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2{e}^{\operatorname{sin}⁡t},\,4{e}^{\operatorname{cos}⁡t}⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $8\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$
- $4\operatorname{cos}⁡t\,{e}^{2\operatorname{sin}⁡t}$
- $-16\operatorname{sin}⁡t\,{e}^{2\operatorname{cos}⁡t}$
- $-8\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$
- $-8\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\operatorname{cos}⁡t\,{e}^{\operatorname{sin}⁡t},\,-4\operatorname{sin}⁡t\,{e}^{\operatorname{cos}⁡t}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }4{e}^{\operatorname{cos}⁡t}\cdot 2\operatorname{cos}⁡t\,{e}^{\operatorname{sin}⁡t}\,dt \\  & ={\int }_{0}^{2\pi }8\operatorname{cos}⁡t\,{e}^{\operatorname{cos}⁡t+\operatorname{sin}⁡t}\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-126751 (learner-ineligible)

## double_sine (observed_raw; {'a': 3, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/2fa9edcb3336356ecf6e7bdb66b366030e314a0767b5a8f9fc0895316d35a856.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\operatorname{sin}⁡t,\,4\operatorname{sin}⁡2t⟩$ for $t\in [0,\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $-24\operatorname{sin}⁡t\operatorname{cos}⁡2t$
- $12\operatorname{sin}⁡2t\operatorname{cos}⁡t$
- $-9\operatorname{sin}⁡t\operatorname{cos}⁡t$
- $-12\operatorname{sin}⁡2t\operatorname{cos}⁡t$
- $-32\operatorname{sin}⁡2t\operatorname{cos}⁡2t$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3\operatorname{cos}⁡t,\,8\operatorname{cos}⁡2t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{\pi }(-3\operatorname{sin}⁡t)\cdot 8\operatorname{cos}⁡2t\,dt \\  & ={\int }_{0}^{\pi }-24\operatorname{sin}⁡t\operatorname{cos}⁡2t\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-126748 (learner-ineligible)

## double_cos (observed_raw; {'a': 3, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/a3a123c3646694f118e7feff0aef78181b692688b28b286c29db6392edf076e6.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\operatorname{sin}⁡2t,\,4\operatorname{cos}⁡t⟩$ for $t\in [-\frac{\pi }{2},\frac{\pi }{2}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{-\pi /2}^{\pi /2}\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $12\operatorname{sin}⁡2t\operatorname{sin}⁡t$
- $-12\operatorname{sin}⁡2t\operatorname{sin}⁡t$
- $-16\operatorname{cos}⁡t\operatorname{sin}⁡t$
- $-18\operatorname{sin}⁡2t\operatorname{cos}⁡2t$
- $24\operatorname{cos}⁡t\operatorname{cos}⁡2t$

Worked solution:

Our simple, piecewise smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨6\operatorname{cos}⁡2t,\,-4\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{-\pi /2}^{\pi /2}4\operatorname{cos}⁡t\cdot 6\operatorname{cos}⁡2t\,dt \\  & ={\int }_{-\pi /2}^{\pi /2}24\operatorname{cos}⁡t\operatorname{cos}⁡2t\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-126760 (learner-ineligible)

## mixed (observed_raw; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/61e7aa83f01a8d68bf32d01fbbb79d6608aef9e6abeb2653f64b6af059aeca39.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2(\operatorname{sin}⁡t-\operatorname{sin}⁡2t),\,4(\operatorname{cos}⁡t-\operatorname{cos}⁡2t)⟩$ for $t\in [\frac{\pi }{3},\frac{5\pi }{3}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{\pi /3}^{5\pi /3}\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $8(\operatorname{cos}⁡2t-\operatorname{cos}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $8(\operatorname{cos}⁡2t-\operatorname{cos}⁡t)(\operatorname{cos}⁡t-2\operatorname{cos}⁡2t)$
- $8(\operatorname{sin}⁡t-\operatorname{sin}⁡2t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $8(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)$
- $8(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(\operatorname{cos}⁡t-2\operatorname{cos}⁡2t)$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2(\operatorname{cos}⁡t-2\operatorname{cos}⁡2t),\,4(-\operatorname{sin}⁡t+2\operatorname{sin}⁡2t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{\pi /3}^{5\pi /3}2(-\operatorname{sin}⁡t+\operatorname{sin}⁡2t)\cdot 4(-\operatorname{sin}⁡t+2\operatorname{sin}⁡2t)\,dt \\  & ={\int }_{\pi /3}^{5\pi /3}8(\operatorname{sin}⁡2t-\operatorname{sin}⁡t)(2\operatorname{sin}⁡2t-\operatorname{sin}⁡t)\,dt.\end{aligned}
$$

### Generated changed-parameter evidence — source bank q-126761 (learner-ineligible)

## power (observed_raw; {'a': 2, 'b': 4, 'm': 5})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/c929c814454bed4c15be142a9c9cea1515a08cdaf05e035bddcb2b495fbde79f.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2{sin}^{5}⁡t,\,4{cos}^{5}⁡t⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the missing part of the equation.

*Hint: Note that $C$ is negatively oriented.*

- $-40{cos}^{5}⁡t{sin}^{5}⁡t$
- $-40{sin}^{6}⁡t{cos}^{4}⁡t$
- $20{cos}^{5}⁡t\operatorname{sin}⁡t$
- $40{sin}^{6}⁡t{cos}^{4}⁡t$
- $40{cos}^{6}⁡t{sin}^{4}⁡t$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨10{sin}^{4}⁡t\operatorname{cos}⁡t,\,-20{cos}^{4}⁡t\operatorname{sin}⁡t⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-2{sin}^{5}⁡t)\cdot (-20{cos}^{4}⁡t\operatorname{sin}⁡t)\,dt \\  & ={\int }_{0}^{2\pi }40{sin}^{6}⁡t{cos}^{4}⁡t\,dt.\end{aligned}
$$

### Generated variant — easy

## circle_cw (authored; {'a': 2, 'b': 2})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/05beabbc375a6d6d6cd194fbb0a44d08953912c4767337ae6bdf44ebd072f045.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin(t),\,2\cos(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $4 \sin{\left(t \right)} \cos{\left(t \right)}$
- $4 \cos^{2}{\left(t \right)}$
- $2 \cos^{2}{\left(t \right)}$
- $- 4 \cos^{2}{\left(t \right)}$
- $8 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\&=-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}
$$

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_Cy\,\mathrm{d}x.
$$

The derivative of $r(t)$ is

$$
r'(t)=⟨2\cos(t),\,-2\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}\oint_Cy\,\mathrm{d}x&=\int_{0}^{2 \pi}2\cos(t)\cdot 2\cos(t)\,\mathrm{d}t\&=\int_{0}^{2 \pi}4\cos^{2}(t)\,\mathrm{d}t.\end{aligned}
$$

### Generated variant — easy

## circle_cw (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/6de000cc545ce6425596e0bf63b0b9574f455a7f42e94c84a801fd9e6b71d18d.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\sin(t),\,3\cos(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 9 \cos^{2}{\left(t \right)}$
- $9 \cos^{2}{\left(t \right)}$
- $9 \sin{\left(t \right)} \cos{\left(t \right)}$
- $3 \cos^{2}{\left(t \right)}$
- $18 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\&=-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}
$$

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_Cy\,\mathrm{d}x.
$$

The derivative of $r(t)$ is

$$
r'(t)=⟨3\cos(t),\,-3\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}\oint_Cy\,\mathrm{d}x&=\int_{0}^{2 \pi}3\cos(t)\cdot 3\cos(t)\,\mathrm{d}t\&=\int_{0}^{2 \pi}9\cos^{2}(t)\,\mathrm{d}t.\end{aligned}
$$

### Generated variant — moderate

## ellipse_ccw (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/7649f93c85abfa55a8e490b55b41b8d0be48774691684df08dd5c87c83568fe8.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\cos(t),\,4\sin(t)⟩$ for $t\in [0,2\pi ].$ The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

- $8 \sin{\left(t \right)} \cos{\left(t \right)}$
- $8 \cos^{2}{\left(t \right)}$
- $4 \cos^{2}{\left(t \right)}$
- $- 8 \cos^{2}{\left(t \right)}$
- $16 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨-2\sin(t),\,4\cos(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{0}^{2\pi }2\cos(t)\cdot 4\cos(t)\,dt \  & ={\int }_{0}^{2\pi }8\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — moderate

## ellipse_ccw (authored; {'a': 2, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/1f6830788feb68e5af2fa413c192be7c6a085f389a33bb42f169a48499918228.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\cos(t),\,3\sin(t)⟩$ for $t\in [0,2\pi ].$ The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

- $- 6 \cos^{2}{\left(t \right)}$
- $6 \cos^{2}{\left(t \right)}$
- $3 \cos^{2}{\left(t \right)}$
- $6 \sin{\left(t \right)} \cos{\left(t \right)}$
- $12 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨-2\sin(t),\,3\cos(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{0}^{2\pi }2\cos(t)\cdot 3\cos(t)\,dt \  & ={\int }_{0}^{2\pi }6\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## ellipse_cw (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/65d77d622631c67f83a8b016864287f527424241ba1a9aafa06ca3f67df31e4d.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin(t),\,4\cos(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $8 \sin{\left(t \right)} \cos{\left(t \right)}$
- $8 \cos^{2}{\left(t \right)}$
- $2 \cos^{2}{\left(t \right)}$
- $- 8 \cos^{2}{\left(t \right)}$
- $16 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\cos(t),\,-4\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }4\cos(t)\cdot 2\cos(t)\,dt \  & ={\int }_{0}^{2\pi }8\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## ellipse_cw (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/400ceed8a61ae7a57d62a0c73e431d2a5cbe6d6dd647feb4b6c012647be66ec9.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\sin(t),\,3\cos(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 9 \cos^{2}{\left(t \right)}$
- $9 \cos^{2}{\left(t \right)}$
- $9 \sin{\left(t \right)} \cos{\left(t \right)}$
- $3 \cos^{2}{\left(t \right)}$
- $18 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3\cos(t),\,-3\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }3\cos(t)\cdot 3\cos(t)\,dt \  & ={\int }_{0}^{2\pi }9\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## exp_ccw (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/e76d58b53395442025b94ca72ffd891dd7f61c5de0137e6293b2f6cd160919f1.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2e^{\cos(t)}, 4e^{\sin(t)}⟩$ for $t\in[0,2\pi].$ The area of $D$ can be written as

$$
\text{Area}(D)=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\mathrm{d}A=\int_0^{2\pi}\boxed{}\,\mathrm{d}t,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

- $8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}}$
- $8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $4 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $- 8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $16 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\&=\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}
$$

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_Cx\,\mathrm{d}y.
$$

The derivative of $r(t)$ is

$$
r'(t)=⟨-2\sin(t) e^{\cos(t)},\,4\cos(t) e^{\sin(t)}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}\oint_Cx\,\mathrm{d}y&=\int_{0}^{2 \pi}2e^{\cos(t)}\cdot 4\cos(t) e^{\sin(t)}\,\mathrm{d}t\&=\int_{0}^{2 \pi}8\cos(t)e^{\cos(t) + \sin(t)}\,\mathrm{d}t.\end{aligned}
$$

### Generated variant — hard

## exp_ccw (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/84a5c9a3879b60b6fb7236dbe9af3bf019159420fe106caf27d1046c8175344f.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3e^{\cos(t)}, 3e^{\sin(t)}⟩$ for $t\in[0,2\pi].$ The area of $D$ can be written as

$$
\text{Area}(D)=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\mathrm{d}A=\int_0^{2\pi}\boxed{}\,\mathrm{d}t,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

- $- 9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}}$
- $3 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $18 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\&=\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}
$$

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_Cx\,\mathrm{d}y.
$$

The derivative of $r(t)$ is

$$
r'(t)=⟨-3\sin(t) e^{\cos(t)},\,3\cos(t) e^{\sin(t)}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}\oint_Cx\,\mathrm{d}y&=\int_{0}^{2 \pi}3e^{\cos(t)}\cdot 3\cos(t) e^{\sin(t)}\,\mathrm{d}t\&=\int_{0}^{2 \pi}9\cos(t)e^{\cos(t) + \sin(t)}\,\mathrm{d}t.\end{aligned}
$$

### Generated variant — hard

## exp_cw (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/044271d96422f79d0c3c2cba3707c03db3fc0bdf20805972a4563e6204d3e4f5.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2{e}^{\sin(t)},\,4{e}^{\cos(t)}⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}}$
- $8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $2 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $- 8 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $16 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\cos(t)\,{e}^{\sin(t)},\,-4\sin(t)\,{e}^{\cos(t)}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }4{e}^{\cos(t)}\cdot 2\cos(t)\,{e}^{\sin(t)}\,dt \  & ={\int }_{0}^{2\pi }8\cos(t)\,{e}^{\cos(t)+\sin(t)}\,dt.\end{aligned}
$$

### Generated variant — hard

## exp_cw (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/1321d60033e7f01a615857a905d202c2efbcae7fc008fe673b25309177d21bde.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3{e}^{\sin(t)},\,3{e}^{\cos(t)}⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $9 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}}$
- $3 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $18 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3\cos(t)\,{e}^{\sin(t)},\,-3\sin(t)\,{e}^{\cos(t)}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }3{e}^{\cos(t)}\cdot 3\cos(t)\,{e}^{\sin(t)}\,dt \  & ={\int }_{0}^{2\pi }9\cos(t)\,{e}^{\cos(t)+\sin(t)}\,dt.\end{aligned}
$$

### Generated variant — hard

## double_sine (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/00ff8c690dcf508c8ba25a8763735747108ac111665ab0a24ff9588ec0384b1e.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin(t),\,4\sin(2t)⟩$ for $t\in [0,\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 8 \sin{\left(t \right)} \sin{\left(2 t \right)}$
- $- 16 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 8 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $16 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 32 \sin{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\cos(t),\,8\cos(2t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{\pi }(-2\sin(t))\cdot 8\cos(2t)\,dt \  & ={\int }_{0}^{\pi }-16\sin(t)\cos(2t)\,dt.\end{aligned}
$$

### Generated variant — hard

## double_sine (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/904d193d6dfd879899ff4c94e00528b39a97a1e4b78c0d42066ad91fc32fed1a.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\sin(t),\,3\sin(2t)⟩$ for $t\in [0,\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $18 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 18 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 9 \sin{\left(t \right)} \sin{\left(2 t \right)}$
- $- 6 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 36 \sin{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3\cos(t),\,6\cos(2t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{\pi }(-3\sin(t))\cdot 6\cos(2t)\,dt \  & ={\int }_{0}^{\pi }-18\sin(t)\cos(2t)\,dt.\end{aligned}
$$

### Generated variant — hard

## double_cos (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/abe66a5dec284b1a5789731441e5aef1f62c94c733f76c675c41b3de339207af.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin(2t),\,4\cos(t)⟩$ for $t\in [-\frac{\pi }{2},\frac{\pi }{2}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{-\pi /2}^{\pi /2}\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $8 \sin{\left(2 t \right)} \cos{\left(t \right)}$
- $16 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $4 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $- 16 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $32 \cos{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, piecewise smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨4\cos(2t),\,-4\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{-\pi /2}^{\pi /2}4\cos(t)\cdot 4\cos(2t)\,dt \  & ={\int }_{-\pi /2}^{\pi /2}16\cos(t)\cos(2t)\,dt.\end{aligned}
$$

### Generated variant — hard

## double_cos (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/68e54b306594a63d0e63cb7dbbaafd3986603f2e5c2f15262514d081c9a8cf03.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\sin(2t),\,3\cos(t)⟩$ for $t\in [-\frac{\pi }{2},\frac{\pi }{2}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{-\pi /2}^{\pi /2}\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 18 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $18 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $9 \sin{\left(2 t \right)} \cos{\left(t \right)}$
- $6 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $36 \cos{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, piecewise smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨6\cos(2t),\,-3\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{-\pi /2}^{\pi /2}3\cos(t)\cdot 6\cos(2t)\,dt \  & ={\int }_{-\pi /2}^{\pi /2}18\cos(t)\cos(2t)\,dt.\end{aligned}
$$

### Generated variant — hard

## mixed (authored; {'a': 2, 'b': 4})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/61e7aa83f01a8d68bf32d01fbbb79d6608aef9e6abeb2653f64b6af059aeca39.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2(\sin(t)-\sin(2t)),\,4(\cos(t)-\cos(2t))⟩$ for $t\in [\frac{\pi }{3},\frac{5\pi }{3}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{\pi /3}^{5\pi /3}\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 8 \sin{\left(t \right)} \cos{\left(t \right)} + 8 \sin{\left(t \right)} \cos{\left(2 t \right)} + 8 \sin{\left(2 t \right)} \cos{\left(t \right)} - 8 \sin{\left(2 t \right)} \cos{\left(2 t \right)}$
- $8 \sin^{2}{\left(t \right)} - 24 \sin{\left(t \right)} \sin{\left(2 t \right)} + 16 \sin^{2}{\left(2 t \right)}$
- $4 \sin^{2}{\left(t \right)} - 12 \sin{\left(t \right)} \sin{\left(2 t \right)} + 8 \sin^{2}{\left(2 t \right)}$
- $- 8 \sin^{2}{\left(t \right)} + 24 \sin{\left(t \right)} \sin{\left(2 t \right)} - 16 \sin^{2}{\left(2 t \right)}$
- $16 \sin^{2}{\left(t \right)} - 48 \sin{\left(t \right)} \sin{\left(2 t \right)} + 32 \sin^{2}{\left(2 t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2(\cos(t)-2\cos(2t)),\,4(-\sin(t)+2\sin(2t))⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{\pi /3}^{5\pi /3}2(-\sin(t)+\sin(2t))\cdot 4(-\sin(t)+2\sin(2t))\,dt \  & ={\int }_{\pi /3}^{5\pi /3}8(\sin(2t)-\sin(t))(2\sin(2t)-\sin(t))\,dt.\end{aligned}
$$

### Generated variant — hard

## mixed (authored; {'a': 3, 'b': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/4dcb310975f05ddfa772c408a22bcb52adaaf60b1bec57e38213f8b244e157ee.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3(\sin(t)-\sin(2t)),\,3(\cos(t)-\cos(2t))⟩$ for $t\in [\frac{\pi }{3},\frac{5\pi }{3}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{\pi /3}^{5\pi /3}\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 9 \sin^{2}{\left(t \right)} + 27 \sin{\left(t \right)} \sin{\left(2 t \right)} - 18 \sin^{2}{\left(2 t \right)}$
- $9 \sin^{2}{\left(t \right)} - 27 \sin{\left(t \right)} \sin{\left(2 t \right)} + 18 \sin^{2}{\left(2 t \right)}$
- $- 9 \sin{\left(t \right)} \cos{\left(t \right)} + 9 \sin{\left(t \right)} \cos{\left(2 t \right)} + 9 \sin{\left(2 t \right)} \cos{\left(t \right)} - 9 \sin{\left(2 t \right)} \cos{\left(2 t \right)}$
- $3 \sin^{2}{\left(t \right)} - 9 \sin{\left(t \right)} \sin{\left(2 t \right)} + 6 \sin^{2}{\left(2 t \right)}$
- $18 \sin^{2}{\left(t \right)} - 54 \sin{\left(t \right)} \sin{\left(2 t \right)} + 36 \sin^{2}{\left(2 t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨3(\cos(t)-2\cos(2t)),\,3(-\sin(t)+2\sin(2t))⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{\pi /3}^{5\pi /3}3(-\sin(t)+\sin(2t))\cdot 3(-\sin(t)+2\sin(2t))\,dt \  & ={\int }_{\pi /3}^{5\pi /3}9(\sin(2t)-\sin(t))(2\sin(2t)-\sin(t))\,dt.\end{aligned}
$$

### Generated variant — hard

## power (authored; {'a': 2, 'b': 4, 'm': 5})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/c929c814454bed4c15be142a9c9cea1515a08cdaf05e035bddcb2b495fbde79f.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin^{5}(t),\,4\cos^{5}(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 8 \sin^{5}{\left(t \right)} \cos^{5}{\left(t \right)}$
- $20 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $80 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $40 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $- 40 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨10\sin^{4}(t)\cos(t),\,-20\cos^{4}(t)\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-2\sin^{5}(t))\cdot (-20\cos^{4}(t)\sin(t))\,dt \  & ={\int }_{0}^{2\pi }40\sin^{6}(t)\cos^{4}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## power (authored; {'a': 3, 'b': 3, 'm': 5})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/d835150daa25bde31ae27632aeb21b39a367b21bf932d8c2298c3571e478fd30.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨3\sin^{5}(t),\,3\cos^{5}(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $90 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $- 9 \sin^{5}{\left(t \right)} \cos^{5}{\left(t \right)}$
- $- 45 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $45 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$
- $15 \sin^{6}{\left(t \right)} \cos^{4}{\left(t \right)}$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨15\sin^{4}(t)\cos(t),\,-15\cos^{4}(t)\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-3\sin^{5}(t))\cdot (-15\cos^{4}(t)\sin(t))\,dt \  & ={\int }_{0}^{2\pi }45\sin^{6}(t)\cos^{4}(t)\,dt.\end{aligned}
$$

### Generated variant — easy

## circle_cw (authored; {'a': 6, 'b': 6})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/edd908bb73392cd5c245c74188fae09711575e0084b671f989304fa5f21135e7.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨6\sin(t),\,6\cos(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $6 \cos^{2}{\left(t \right)}$
- $72 \cos^{2}{\left(t \right)}$
- $36 \sin{\left(t \right)} \cos{\left(t \right)}$
- $- 36 \cos^{2}{\left(t \right)}$
- $36 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D)&=\iint_D\mathrm{d}A\&=\iint_D(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\mathrm{d}A\&=-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)\end{aligned}
$$

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-\oint_C(P\,\mathrm{d}x+Q\,\mathrm{d}y)=\oint_Cy\,\mathrm{d}x.
$$

The derivative of $r(t)$ is

$$
r'(t)=⟨6\cos(t),\,-6\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}\oint_Cy\,\mathrm{d}x&=\int_{0}^{2 \pi}6\cos(t)\cdot 6\cos(t)\,\mathrm{d}t\&=\int_{0}^{2 \pi}36\cos^{2}(t)\,\mathrm{d}t.\end{aligned}
$$

### Generated variant — moderate

## ellipse_ccw (authored; {'a': 6, 'b': 1})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/23d12beade53afe2ce7dce7d0fc199476e4be1076200e7c8d105e3249851f844.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨6\cos(t),\,\sin(t)⟩$ for $t\in [0,2\pi ].$ The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

- $\cos^{2}{\left(t \right)}$
- $12 \cos^{2}{\left(t \right)}$
- $6 \sin{\left(t \right)} \cos{\left(t \right)}$
- $- 6 \cos^{2}{\left(t \right)}$
- $6 \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨-6\sin(t),\,\cos(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{0}^{2\pi }6\cos(t)\cdot \cos(t)\,dt \  & ={\int }_{0}^{2\pi }6\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## power (authored; {'a': 6, 'b': 1, 'm': 3})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/20acb6cb05bad75b13a383975c8f00d44e5768cef78e090d765d5001a3a9abf3.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨6\sin^{3}(t),\,\cos^{3}(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $3 \sin^{4}{\left(t \right)} \cos^{2}{\left(t \right)}$
- $36 \sin^{4}{\left(t \right)} \cos^{2}{\left(t \right)}$
- $- 6 \sin^{3}{\left(t \right)} \cos^{3}{\left(t \right)}$
- $- 18 \sin^{4}{\left(t \right)} \cos^{2}{\left(t \right)}$
- $18 \sin^{4}{\left(t \right)} \cos^{2}{\left(t \right)}$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨18\sin^{2}(t)\cos(t),\,-3\cos^{2}(t)\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-6\sin^{3}(t))\cdot (-3\cos^{2}(t)\sin(t))\,dt \  & ={\int }_{0}^{2\pi }18\sin^{4}(t)\cos^{2}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## power (authored; {'a': 2, 'b': 6, 'm': 7})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/ede29395907d4850efb6bd8d87889b5c40906f74daf5ff9933381894317730a5.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨2\sin^{7}(t),\,6\cos^{7}(t)⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $42 \sin^{8}{\left(t \right)} \cos^{6}{\left(t \right)}$
- $168 \sin^{8}{\left(t \right)} \cos^{6}{\left(t \right)}$
- $- 12 \sin^{7}{\left(t \right)} \cos^{7}{\left(t \right)}$
- $- 84 \sin^{8}{\left(t \right)} \cos^{6}{\left(t \right)}$
- $84 \sin^{8}{\left(t \right)} \cos^{6}{\left(t \right)}$

Worked solution:

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨14\sin^{6}(t)\cos(t),\,-42\cos^{6}(t)\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{2\pi }(-2\sin^{7}(t))\cdot (-42\cos^{6}(t)\sin(t))\,dt \  & ={\int }_{0}^{2\pi }84\sin^{8}(t)\cos^{6}(t)\,dt.\end{aligned}
$$

### Generated variant — hard

## exp_cw (authored; {'a': 1, 'b': 6})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/a4b4d5357612a620fb5c878cf372812ca4e2446f58e099bea6b303676afa8e15.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨{e}^{\sin(t)},\,6{e}^{\cos(t)}⟩$ for $t\in [0,2\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{2\pi }\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $12 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $6 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}}$
- $- 6 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$
- $6 e^{\sin{\left(t \right)}} e^{\cos{\left(t \right)}} \cos{\left(t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨\cos(t)\,{e}^{\sin(t)},\,-6\sin(t)\,{e}^{\cos(t)}⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{0}^{2\pi }6{e}^{\cos(t)}\cdot \cos(t)\,{e}^{\sin(t)}\,dt \  & ={\int }_{0}^{2\pi }6\cos(t)\,{e}^{\cos(t)+\sin(t)}\,dt.\end{aligned}
$$

### Generated variant — hard

## double_sine (authored; {'a': 6, 'b': 1})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/f4758bb0bfe1033cb04c93711f6e6f0fd136e36ee288413154f1035dce0dfa4f.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨6\sin(t),\,\sin(2t)⟩$ for $t\in [0,\pi ].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{0}^{\pi }\boxed{}\,dt,
$$

where $P(x,y)=0$ and $Q(x,y)=x.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $- 2 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 24 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 6 \sin{\left(t \right)} \sin{\left(2 t \right)}$
- $12 \sin{\left(t \right)} \cos{\left(2 t \right)}$
- $- 12 \sin{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}-x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨6\cos(t),\,2\cos(2t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}-x\,\text{d}y & ={\int }_{0}^{\pi }(-6\sin(t))\cdot 2\cos(2t)\,dt \  & ={\int }_{0}^{\pi }-12\sin(t)\cos(2t)\,dt.\end{aligned}
$$

### Generated variant — hard

## double_cos (authored; {'a': 1, 'b': 6})

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133896/plots/d4b080242af32a1cdbe4cf88eed5563b9b77de07da68cb8fbbd3c75dc8a9f7af.png)

Let $D$ be the region enclosed by the curve $C$ parametrized as
$r(t)=⟨\sin(2t),\,6\cos(t)⟩$ for $t\in [-\frac{\pi }{2},\frac{\pi }{2}].$ 
The area of $D$ can be written as

$$
\text{Area}(D)={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})dA={\int }_{-\pi /2}^{\pi /2}\boxed{}\,dt,
$$

where $P(x,y)=-y$ and $Q(x,y)=0.$ Determine the pointwise integrand obtained from the given $P$, $Q$, and parametrization using Green's theorem, with the sign adjusted for the orientation of $C$.

*Hint: Note that $C$ is negatively oriented.*

- $2 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $24 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $6 \sin{\left(2 t \right)} \cos{\left(t \right)}$
- $- 12 \cos{\left(t \right)} \cos{\left(2 t \right)}$
- $12 \cos{\left(t \right)} \cos{\left(2 t \right)}$

Worked solution:

Our simple, piecewise smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since the path is negatively oriented.

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
{r}^{′}(t)=⟨2\cos(2t),\,-6\sin(t)⟩.
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}y\,\text{d}x & ={\int }_{-\pi /2}^{\pi /2}6\cos(t)\cdot 2\cos(2t)\,dt \  & ={\int }_{-\pi /2}^{\pi /2}12\cos(t)\cos(2t)\,dt.\end{aligned}
$$

