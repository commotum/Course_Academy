# Template extraction

## 1. Specific originals

All plots are 360×304 and were inspected individually at full original resolution after compositing alpha on white.

### q-42215 / db17592186134376

Anchor a=3, b=2; exact segments [(3*sin(t), 2*sin(2*t), 0, pi)]; orientation -1; selected area form -y dx with orientation correction; final area 8.

![](images/df/df940d9ea08ed1b326d4904933bd41c318112836d2d657abcb3c158aabbe7bb4.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡t\,i+2\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since our path is negatively oriented. 

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y={∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
\begin{aligned}{r}^{′}(t) & =3\operatorname{cos}⁡t\,i+4\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}y\,dx & ={\int }_{0}^{\pi }2\operatorname{sin}⁡2t\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & =6{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =6{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =12{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-12{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =12{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =4{{u}^{3}|}_{-1}^{1} \\  & =4({1}^{3}-(-1)^{3}) \\  & =8\end{aligned}
$$

### q-42298 / db17592186134386

Anchor a=2, b=1; exact segments [(2*t**2, -t**3, -1, 1), (2, t, -1, 1)]; orientation 1; selected area form -y dx with orientation correction; final area 8/5.

![](images/01/01a5f06674cacca4764f438a8c06f020659f0177a0b74952f40bc9072627ec3f.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 2t^{2}i - t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 2i + tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.

Worked solution absent; correct designation absent. Infer area by independent integration only in normal authored completion.

### q-126722 / db17592186369399

Anchor a=2, b=2; exact segments [(2*sin(2*t), -2*sin(t), 0, pi)]; orientation -1; selected area form x dy with orientation correction; final area 16/3.

![](images/2a/2a89a14bced6f6700614cfad216070154cae165785458f817ea06d266edfde4e.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=2\operatorname{sin}⁡2t\,i-2\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$

First, let $P(x,y)=0$ and $Q(x,y)=x.$

Our simple, smooth, closed path $C$ is negatively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since our path is negatively oriented. 

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y=-{∮}_{C}x\,\text{d}y.
$$

 

The derivative of $r(t)$ is

$$
\begin{aligned}{r}^{′}(t) & =4\operatorname{cos}⁡2t\,i-2\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}x\,dy & =-{\int }_{0}^{\pi }2\operatorname{sin}⁡2t\cdot (-2\operatorname{cos}⁡t)\,\text{d}t \\  & =4{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =4{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =8{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-8{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =8{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{8}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{8}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{16}{3}\end{aligned}
$$

### q-126725 / db17592186369406

Anchor a=1, b=1; exact segments [(sin(2*t), cos(t), pi/2, 3*pi/2)]; orientation 1; selected area form x dy with orientation correction; final area 4/3.

![](images/41/41dc9af596ca43b1d0d61bb4273be46d3a3d1adc62f99a70fe53c72d69667093.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=\operatorname{sin}⁡2t\,i+\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$

First, let $P(x,y)=0$ and $Q(x,y)=x.$

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
\begin{aligned}{r}^{′}(t) & =2\operatorname{cos}⁡2t\,i-\operatorname{sin}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\cdot (-\operatorname{sin}⁡t)\,\text{d}t \\  & =-{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-2{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-2{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =2{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{2}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{4}{3}\end{aligned}
$$

### q-126818 / db17592186369427

Anchor a=2, b=3; exact segments [(-2*t**2, 3*t**3, -1, 1), (-2, -t, -3, 3)]; orientation 1; selected area form -y dx with orientation correction; final area 24/5.

![](images/9e/9eb614f4f6e00c5fa03759a61d69734aa1c6eaf26d98d3c78b96052ca16162d0.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-2{t}^{2}\,i+3{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-2\,i-t\,j$ for $t\in [-3,3].$

Use Green's theorem to find the area of the region.

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y=-{∮}_{C}y\,\text{d}x.
$$

 

The derivatives of ${r}_{1}(t)$ and ${r}_{2}(t)$ are as follows:

$$
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=-4t\,i+9{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}3{t}^{3}\cdot (-4t)\,\text{d}t-{\int }_{-3}^{3}(-t)\cdot 0\,\text{d}t \\  & =12{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =12[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =12\cdot \frac{2}{5} \\  & =\frac{24}{5}.\end{aligned}
$$

### q-126858 / db17592186369448

Anchor a=1, b=1; exact segments [(t**5, t**4, -1, 1), (-t, 1, -1, 1)]; orientation 1; selected area form x dy with orientation correction; final area 8/9.

![](images/52/52ec0dfc4590daf9306c2389bd321acbf80f263c799fa4ddd4e5b8f662e0a2b5.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)={t}^{5}\,i+{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-t\,i+1\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.

First, let $P(x,y)=0$ and $Q(x,y)=x.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented and  

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

 

The derivatives of ${r}_{1}(t)$ and ${r}_{2}(t)$ are as follows:

$$
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=5{t}^{4}\,i+4{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,\text{d}y & ={∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & ={∮}_{{C}_{1}}x\,dy+{∮}_{{C}_{2}}x\,dy \\  & ={\int }_{-1}^{1}{t}^{5}\cdot 4{t}^{3}\,\text{d}t+{\int }_{-1}^{1}(-t)\cdot 0\,\text{d}t \\  & =4{\int }_{-1}^{1}{t}^{8}\,\text{d}t-0 \\  & =4[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =4\cdot \frac{2}{9} \\  & =\frac{8}{9}.\end{aligned}
$$

### q-126727 / db17592186431051

Anchor a=1, b=2; exact segments [(-cos(t), 2*sin(2*t), pi/2, 3*pi/2)]; orientation 1; selected area form -y dx with orientation correction; final area 8/3.

![](images/b5/b51e252935f7077f3285258845d8d1e4957b83894037f968ee306910aa88bad6.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, smooth, closed path $C$ is positively oriented, and  

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=0-(-1)=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$
{∮}_{C}P\,\text{d}x+Q\,\text{d}y=-{∮}_{C}y\,\text{d}x.
$$

 

The derivative of $r(t)$ is

$$
\begin{aligned}{r}^{′}(t) & =\operatorname{sin}⁡t\,i+4\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}y\,dx & =-{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡2t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-2{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-2{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-4{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-4{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =4{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{4}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{4}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{8}{3}\end{aligned}
$$

### q-126859 / db17592186431052

Anchor a=1, b=2; exact segments [(t**5, -2*t**4, -1, 1), (-t, -2, -1, 1)]; orientation -1; selected area form x dy with orientation correction; final area 16/9.

![](images/9e/9ebabcf1e3c3c3d2f4850d425657e7314c0135c81a432bfbbc8ae31ee39cb85d.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)={t}^{5}\,i-2{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-t\,i-2\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.

First, let $P(x,y)=0$ and $Q(x,y)=x.$ 

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and   

$$
\frac{∂Q}{∂x}-\frac{∂P}{∂y}=1-0=1.
$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$
\begin{aligned}\text{Area}(D) & ={∬}_{D}\text{d}A \\  & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & =-{∮}_{C}P\,\text{d}x+Q\,\text{d}y\end{aligned}
$$

  

Notice that we have to take the line integral with a minus sign since our path is negatively oriented.

Substituting $P(x,y)=0$ and $Q(x,y)=x,$ we get

$$
-{∮}_{C}P\,\text{d}x+Q\,\text{d}y=-{∮}_{C}x\,\text{d}y.
$$

 

The derivatives of ${r}_{1}(t)$ and ${r}_{2}(t)$ are as follows:

$$
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=5{t}^{4}\,i-8{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}x\,\text{d}y & =-{∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & =-{∮}_{{C}_{1}}x\,dy-{∮}_{{C}_{2}}x\,dy \\  & =-{\int }_{-1}^{1}{t}^{5}\cdot (-8{t}^{3})\,\text{d}t-{\int }_{-1}^{1}(-t)\cdot 0\,\text{d}t \\  & =8{\int }_{-1}^{1}{t}^{8}\,\text{d}t+0 \\  & =8[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =8\cdot \frac{2}{9} \\  & =\frac{16}{9}.\end{aligned}
$$

## 2. Shared purpose

Evaluate the region’s area, choosing a unit-curl field, correcting the circulation sign for traversal orientation, substituting complete coordinate functions and derivatives, and evaluating the resulting definite integral. The response is a scalar exact area. The source banks contain scalar expressions, so equivalence is equality of full scalar values, including wrong-wrong pairs.

## 3. Components and every original bank

Each opaque original bank scales every complete answer by ab/(a₀b₀). This is a homogeneous parameterized expression recipe reproducing all values, not an inferred error operation. Scalar examples underdetermine the historical distractor intent. Raw opaque profiles remain publicly replayable and explicitly evidence_only=true / eligible_for_learning=false, including complete repaired metadata. They are never defaults.

### original:17592186134376, field 0 (q-42215)

Key selection; type radio; correct presence False.

- `\frac{17}{2}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `\frac{15}{2}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `8` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `12` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `10` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

### original:17592186134376, field 1 (q-42215)

Key selection; type radio; correct presence True.

- `12` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `10` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `8` → that complete scalar × ab/6; observed correct; interpretation unresolved.

- `\frac{17}{2}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `\frac{15}{2}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

### original:17592186134386, field 0 (q-42298)

Key selection; type radio; correct presence False.

- `\frac{8}{5}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{7}{3}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{4}{3}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `4` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `2` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

### original:17592186369399, field 0 (q-126722)

Key selection; type radio; correct presence True.

- `\frac{7}{2}` → that complete scalar × ab/4; wrong or designation absent; interpretation unresolved.

- `\frac{16}{3}` → that complete scalar × ab/4; observed correct; interpretation unresolved.

- `\frac{25}{3}` → that complete scalar × ab/4; wrong or designation absent; interpretation unresolved.

- `10` → that complete scalar × ab/4; wrong or designation absent; interpretation unresolved.

- `\frac{15}{2}` → that complete scalar × ab/4; wrong or designation absent; interpretation unresolved.

### original:17592186369406, field 0 (q-126725)

Key selection; type radio; correct presence True.

- `\frac{5}{2}` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `\frac{2}{3}` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `\frac{4}{3}` → that complete scalar × ab/1; observed correct; interpretation unresolved.

- `7\pi ` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `\frac{3}{2}` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

### original:17592186369427, field 0 (q-126818)

Key selection; type radio; correct presence True.

- `\frac{4}{5}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `\frac{14}{3}` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `6` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `4` → that complete scalar × ab/6; wrong or designation absent; interpretation unresolved.

- `\frac{24}{5}` → that complete scalar × ab/6; observed correct; interpretation unresolved.

### original:17592186369448, field 0 (q-126858)

Key selection; type radio; correct presence True.

- `\frac{2}{3}` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `\frac{8}{9}` → that complete scalar × ab/1; observed correct; interpretation unresolved.

- `4` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `\frac{5}{4}` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

- `5` → that complete scalar × ab/1; wrong or designation absent; interpretation unresolved.

### original:17592186431051, field 0 (q-126727)

Key selection; type radio; correct presence True.

- `\frac{5}{2}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `2\pi ` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{8}{3}` → that complete scalar × ab/2; observed correct; interpretation unresolved.

- `\frac{4}{3}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{3}{4}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

### original:17592186431052, field 0 (q-126859)

Key selection; type radio; correct presence True.

- `3\pi ` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{15}{2}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `5\pi ` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

- `\frac{16}{9}` → that complete scalar × ab/2; observed correct; interpretation unresolved.

- `\frac{12}{5}` → that complete scalar × ab/2; wrong or designation absent; interpretation unresolved.

## 4. Reusable masks and constraints

SPECS contains the complete coefficient maps for every prompt and solution; INSERTIONS supplies omitted unit-coefficient slots. Numeric slots refer only to complete scalar coefficients; derivative/function exponents, function arguments, segment indices and unit-curl blocks remain fixed. Separate masks distinguish derivative coefficients, substituted coordinate components, factored products, double-angle factor2, transformed bounds, primitive coefficients and endpoint arithmetic. All source-specific prose and aligned row order remain present at changed parameters. Normal solutions add separate evaluated endpoint component rows without replacing original primitives or endpoint-substitution stages.

Normal method banks are selected before coefficients. Moderate: [4ab/3, 2ab/3, 4ab, −4ab/3, 0], representing correct area, omitted double-angle factor, omitted primitive divisor, orientation error, and dropping the single-angle factor (sin2t integrates to zero). Hard with derivative n=2 or4 and primitive degree d=5 or9: [2nab/d, 2ab/d, nab, −2nab/d, 2nab], representing area, omitted derivative factor, upper endpoint alone plus omitted primitive divisor, orientation error, omitted primitive divisor. Easy: [abπ, −abπ, 2abπ, aπ, bπ], representing area, orientation error, omitted half-angle divisor and individually omitted coordinate coefficients. Every whole bank rejects collisions; no option is filled from a pool.

All explicit inputs and random samplers enforce positive integer coefficients1..8. Easy requires both>=2 and unequal for complete omitted-coefficient banks. These bounded domains supply 64 tasks per moderate family and 64 per hard family,42 ellipse presentations /21 mathematical tasks after equal-role a,b interchange; no cosmetic variable or bank aliases inflate counts. Source number forms are exact integers/rationals and the interval angles remain familiar.

## Missing-level design and route

Activity first-step17592186134864 → concrete ellipse tutorial17592186134868 → negative-orientation tutorial17592186134876 → unit-curl KP17592186134865 → express-area-setup KP17592186134866 → this evaluation KP17592186134867. This follows step/next, not Pull collection order. Prerequisite: Introduction to Green’s Theorem (topic17592186051070, MA2116). Sibling17592186133896 asks for a missing area-integrand/setup expression; authored easy here must evaluate the definite integral to an exact area. The concrete ellipse tutorial supplies that complete evaluation method and half-angle identity. No setup-only easy questions, new technique, within-level progression or off-topic branch is added.

Easy always has one smooth ellipse, two derivatives, one half-angle reduction and familiar endpoint evaluations; moderate always has one trig loop with sin2t expansion and one u-substitution; hard always has two segments with separate derivatives, zero closing-segment contribution and one polynomial primitive. Fixed workloads differ by assessed bookkeeping/method, not large coefficient difficulty.

## Source repair ledger

q-42215/db17592186134376: one extra legacy EDB field without a correct ref; authoritative captured widget confirms one field. Preserve both raw; normal uses one. q-42298/db17592186134386: missing difficulty/solution/correct ref retained absent raw. Authored hard assignment, common two-segment solution and independently derived correct area8/5 in normal. Four trig sources: source smoothness description minimally repaired normal because their closing tangent directions differ. Historical scalar bank intents unresolved; no wrong value is claimed recovered. All eight raw profiles ineligible solely because banks are opaque and/or fields incomplete; no source omitted.