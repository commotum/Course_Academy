# Original questions and parameterized variants

All originals below are explicit ineligible historical evidence profiles. Normal variants use complete method banks.


## Original sin_sin2 {'a': 3, 'b': 2}

![](images/df/df940d9ea08ed1b326d4904933bd41c318112836d2d657abcb3c158aabbe7bb4.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡t\,i+2\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$


Choices: 8, \frac{15}{2}, \frac{17}{2}, 10, 12, 12, 8, 10, \frac{17}{2}, \frac{15}{2}

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186134376.png)


## Original right_polynomial {'a': 2, 'b': 1}

![](images/01/01a5f06674cacca4764f438a8c06f020659f0177a0b74952f40bc9072627ec3f.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 2t^{2}i - t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 2i + tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: \frac{4}{3}, \frac{7}{3}, \frac{8}{5}, 2, 4

[Absent in source; retained as absent in raw replay.]

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186134386.png)


## Original sin2_minus_sin {'a': 2, 'b': 2}

![](images/2a/2a89a14bced6f6700614cfad216070154cae165785458f817ea06d266edfde4e.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=2\operatorname{sin}⁡2t\,i-2\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$


Choices: \frac{25}{3}, \frac{16}{3}, \frac{7}{2}, \frac{15}{2}, 10

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186369399.png)


## Original sin2_cos {'a': 1, 'b': 1}

![](images/41/41dc9af596ca43b1d0d61bb4273be46d3a3d1adc62f99a70fe53c72d69667093.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=\operatorname{sin}⁡2t\,i+\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: \frac{4}{3}, \frac{2}{3}, \frac{5}{2}, \frac{3}{2}, 7\pi 

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186369406.png)


## Original left_polynomial {'a': 2, 'b': 3}

![](images/9e/9eb614f4f6e00c5fa03759a61d69734aa1c6eaf26d98d3c78b96052ca16162d0.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-2{t}^{2}\,i+3{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-2\,i-t\,j$ for $t\in [-3,3].$

Use Green's theorem to find the area of the region.


Choices: 6, \frac{14}{3}, \frac{4}{5}, \frac{24}{5}, 4

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186369427.png)


## Original upper_polynomial {'a': 1, 'b': 1}

![](images/52/52ec0dfc4590daf9306c2389bd321acbf80f263c799fa4ddd4e5b8f662e0a2b5.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)={t}^{5}\,i+{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-t\,i+1\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 4, \frac{8}{9}, \frac{2}{3}, 5, \frac{5}{4}

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186369448.png)


## Original minus_cos_sin2 {'a': 1, 'b': 2}

![](images/b5/b51e252935f7077f3285258845d8d1e4957b83894037f968ee306910aa88bad6.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: \frac{8}{3}, 2\pi , \frac{5}{2}, \frac{3}{4}, \frac{4}{3}

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186431051.png)


## Original lower_polynomial {'a': 1, 'b': 2}

![](images/9e/9ebabcf1e3c3c3d2f4850d425657e7314c0135c81a432bfbbc8ae31ee39cb85d.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)={t}^{5}\,i-2{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-t\,i-2\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 5\pi , \frac{15}{2}, 3\pi , \frac{12}{5}, \frac{16}{9}

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

Inspected source raster: ![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/source-plot-17592186431052.png)


## Generated eligible sin_sin2 {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/8c1a9bb940480d5c1dd2a5a5a8019f5b1cde1d9c8a29d7b7245ea27f8d84c323.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡t\,i+5\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$


Choices: 60, 10, 20, 0, -20

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =3\operatorname{cos}⁡t\,i+10\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}y\,dx & ={\int }_{0}^{\pi }5\operatorname{sin}⁡2t\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =30{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =10{{u}^{3}|}_{-1}^{1} \\  & =10({1}^{3}-(-1)^{3}) \\  & =10\cdot 1-10\cdot (-1) \\  & =10-(-10) \\  & =20\end{aligned}
$$


## Generated eligible sin_sin2 {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/1f4458127c574a761374c1c37cb0e078a16450d657e6ed355e0c8ce2e843b0bb.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡t\,i+4\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$


Choices: 112, \frac{56}{3}, \frac{112}{3}, 0, - \frac{112}{3}

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, piecewise-smooth, closed path $C$ is negatively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =7\operatorname{cos}⁡t\,i+8\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}y\,dx & ={\int }_{0}^{\pi }4\operatorname{sin}⁡2t\cdot 7\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =56{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{{u}^{3}|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{56}{3}\cdot 1-\frac{56}{3}\cdot (-1) \\  & =\frac{56}{3}-(- \frac{56}{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated eligible right_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/0e9c0ec9d74a47ef3227f7abc6da634a67f2265fc23a5a5bb186d98963fde6c5.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 3t^{2}i - 5t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 3i + 5tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: 30, 6, 12, 60, -12

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=6t\,i-15{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=5j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}(-5{t}^{3})\cdot 6t\,\text{d}t-{\int }_{-1}^{1}(5t)\cdot 0\,\text{d}t \\  & =30{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =30[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =30\left(\frac{1^{5}}{5}-\frac{(-1)^{5}}{5}\right) \\  & =30\left(\frac{1}{5}-\left(-\frac{1}{5}\right)\right) \\  & =30\cdot \frac{2}{5} \\  & =\frac{60}{5}.\end{aligned}
$$


## Generated eligible right_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e853bb110b4a18524dcc77df412ea0a0f2ce3ecbddf592553e63fa86ae78bd6b.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 7t^{2}i - 4t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 7i + 4tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: 56, \frac{56}{5}, \frac{112}{5}, 112, - \frac{112}{5}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=14t\,i-12{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=4j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}(-4{t}^{3})\cdot 14t\,\text{d}t-{\int }_{-1}^{1}(4t)\cdot 0\,\text{d}t \\  & =56{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =56[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =56\left(\frac{1^{5}}{5}-\frac{(-1)^{5}}{5}\right) \\  & =56\left(\frac{1}{5}-\left(-\frac{1}{5}\right)\right) \\  & =56\cdot \frac{2}{5} \\  & =\frac{112}{5}.\end{aligned}
$$


## Generated eligible sin2_minus_sin {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/30fb2d3f47372bd78750cbf689771cc7f2ea176d9ad3311ebdeb6f0ce756151a.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡2t\,i-5\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$


Choices: 60, 10, 20, 0, -20

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

 

The derivative of $r(t)$ is

$$
\begin{aligned}{r}^{′}(t) & =6\operatorname{cos}⁡2t\,i-5\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}x\,dy & =-{\int }_{0}^{\pi }3\operatorname{sin}⁡2t\cdot (-5\operatorname{cos}⁡t)\,\text{d}t \\  & =15{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =30{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =10\cdot 1-10\cdot (-1) \\  & =10-(-10) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated eligible sin2_minus_sin {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2e820016efddd732de442da09b5ebbb65543e5930dc52d3eb9e393ce8bfb4b26.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡2t\,i-4\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$


Choices: 112, \frac{56}{3}, \frac{112}{3}, 0, - \frac{112}{3}

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

 

The derivative of $r(t)$ is

$$
\begin{aligned}{r}^{′}(t) & =14\operatorname{cos}⁡2t\,i-4\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}x\,dy & =-{\int }_{0}^{\pi }7\operatorname{sin}⁡2t\cdot (-4\operatorname{cos}⁡t)\,\text{d}t \\  & =28{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =56{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{56}{3}\cdot 1-\frac{56}{3}\cdot (-1) \\  & =\frac{56}{3}-(- \frac{56}{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated eligible sin2_cos {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/5cd570cb430eaec856688b17f0b046c979534da255fd5a4f48e5e9444af2fbe8.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡2t\,i+5\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 60, 10, 20, 0, -20

First, let $P(x,y)=0$ and $Q(x,y)=x.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =6\operatorname{cos}⁡2t\,i-5\operatorname{sin}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{\pi /2}^{3\pi /2}3\operatorname{sin}⁡2t\cdot (-5\operatorname{sin}⁡t)\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-30{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =10\cdot 1-10\cdot (-1) \\  & =10-(-10) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated eligible sin2_cos {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/63267b7ad54dd7435ed6b6787c320d4c13734ee76f82414d3432db4403c54a79.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡2t\,i+4\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 112, \frac{56}{3}, \frac{112}{3}, 0, - \frac{112}{3}

First, let $P(x,y)=0$ and $Q(x,y)=x.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =14\operatorname{cos}⁡2t\,i-4\operatorname{sin}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{\pi /2}^{3\pi /2}7\operatorname{sin}⁡2t\cdot (-4\operatorname{sin}⁡t)\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-56{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{56}{3}\cdot 1-\frac{56}{3}\cdot (-1) \\  & =\frac{56}{3}-(- \frac{56}{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated eligible left_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e9211aa9722bfe620c7da6d877f4136efdf984f46df2b5a763dc11ebb05d6bca.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-3{t}^{2}\,i+5{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3\,i-t\,j$ for $t\in [-5,5].$

Use Green's theorem to find the area of the region.


Choices: 30, 6, 12, 60, -12

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=-6t\,i+15{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}5{t}^{3}\cdot (-6t)\,\text{d}t-{\int }_{-5}^{5}(-t)\cdot 0\,\text{d}t \\  & =30{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =30[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =30\left(\frac{1^{5}}{5}-\frac{(-1)^{5}}{5}\right) \\  & =30\left(\frac{1}{5}-\left(-\frac{1}{5}\right)\right) \\  & =30\cdot \frac{2}{5} \\  & =\frac{60}{5}.\end{aligned}
$$


## Generated eligible left_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/4e8cdfcadeac24945596824d763801e2ef44d2050a35e19390238bd47c3c951b.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-7{t}^{2}\,i+4{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7\,i-t\,j$ for $t\in [-4,4].$

Use Green's theorem to find the area of the region.


Choices: 56, \frac{56}{5}, \frac{112}{5}, 112, - \frac{112}{5}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=-14t\,i+12{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}4{t}^{3}\cdot (-14t)\,\text{d}t-{\int }_{-4}^{4}(-t)\cdot 0\,\text{d}t \\  & =56{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =56[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =56\left(\frac{1^{5}}{5}-\frac{(-1)^{5}}{5}\right) \\  & =56\left(\frac{1}{5}-\left(-\frac{1}{5}\right)\right) \\  & =56\cdot \frac{2}{5} \\  & =\frac{112}{5}.\end{aligned}
$$


## Generated eligible upper_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/887785c19d2bd96c9d0586f54ecc6d065b108e990b7226d5dffe021e63312df3.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=3{t}^{5}\,i+5{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3t\,i+5\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 60, \frac{10}{3}, \frac{40}{3}, 120, - \frac{40}{3}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=15{t}^{4}\,i+20{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-3i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,\text{d}y & ={∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & ={∮}_{{C}_{1}}x\,dy+{∮}_{{C}_{2}}x\,dy \\  & ={\int }_{-1}^{1}3{t}^{5}\cdot 20{t}^{3}\,\text{d}t+{\int }_{-1}^{1}(-3t)\cdot 0\,\text{d}t \\  & =60{\int }_{-1}^{1}{t}^{8}\,\text{d}t-0 \\  & =60[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =60\left(\frac{1^{9}}{9}-\frac{(-1)^{9}}{9}\right) \\  & =60\left(\frac{1}{9}-\left(-\frac{1}{9}\right)\right) \\  & =60\cdot \frac{2}{9} \\  & =\frac{120}{9}.\end{aligned}
$$


## Generated eligible upper_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/b4d4164695724c45b683ae27b2194ad5245837f8663d7f4d1369f2da7d49c23d.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=7{t}^{5}\,i+4{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7t\,i+4\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 112, \frac{56}{9}, \frac{224}{9}, 224, - \frac{224}{9}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=35{t}^{4}\,i+16{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-7i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,\text{d}y & ={∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & ={∮}_{{C}_{1}}x\,dy+{∮}_{{C}_{2}}x\,dy \\  & ={\int }_{-1}^{1}7{t}^{5}\cdot 16{t}^{3}\,\text{d}t+{\int }_{-1}^{1}(-7t)\cdot 0\,\text{d}t \\  & =112{\int }_{-1}^{1}{t}^{8}\,\text{d}t-0 \\  & =112[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =112\left(\frac{1^{9}}{9}-\frac{(-1)^{9}}{9}\right) \\  & =112\left(\frac{1}{9}-\left(-\frac{1}{9}\right)\right) \\  & =112\cdot \frac{2}{9} \\  & =\frac{224}{9}.\end{aligned}
$$


## Generated eligible minus_cos_sin2 {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/f7c5c2a0d5d37471f6db673ec9fc92d301deb745be1eb31d93ab0f46e1eb6b00.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-3\operatorname{cos}⁡t\,i+5\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 60, 10, 20, 0, -20

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =3\operatorname{sin}⁡t\,i+10\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}y\,dx & =-{\int }_{\pi /2}^{3\pi /2}5\operatorname{sin}⁡2t\cdot 3\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-30{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =10\cdot 1-10\cdot (-1) \\  & =10-(-10) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated eligible minus_cos_sin2 {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/131bbf32a3a090a42bcb695a46dcaeecbbd51df53ecff3733e0a8376a63759ba.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-7\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 112, \frac{56}{3}, \frac{112}{3}, 0, - \frac{112}{3}

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, piecewise-smooth, closed path $C$ is positively oriented, and  

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
\begin{aligned}{r}^{′}(t) & =7\operatorname{sin}⁡t\,i+8\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}y\,dx & =-{\int }_{\pi /2}^{3\pi /2}4\operatorname{sin}⁡2t\cdot 7\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-56{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{56}{3}\cdot 1-\frac{56}{3}\cdot (-1) \\  & =\frac{56}{3}-(- \frac{56}{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated eligible lower_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/bb87f082257bd436b7f89a6d5ea0500ac81da8c6d811ebbc37adddaf42504298.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=3{t}^{5}\,i-5{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3t\,i-5\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 60, \frac{10}{3}, \frac{40}{3}, 120, - \frac{40}{3}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=15{t}^{4}\,i-20{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-3i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}x\,\text{d}y & =-{∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & =-{∮}_{{C}_{1}}x\,dy-{∮}_{{C}_{2}}x\,dy \\  & =-{\int }_{-1}^{1}3{t}^{5}\cdot (-20{t}^{3})\,\text{d}t-{\int }_{-1}^{1}(-3t)\cdot 0\,\text{d}t \\  & =60{\int }_{-1}^{1}{t}^{8}\,\text{d}t+0 \\  & =60[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =60\left(\frac{1^{9}}{9}-\frac{(-1)^{9}}{9}\right) \\  & =60\left(\frac{1}{9}-\left(-\frac{1}{9}\right)\right) \\  & =60\cdot \frac{2}{9} \\  & =\frac{120}{9}.\end{aligned}
$$


## Generated eligible lower_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ce072d943595a89a093d12ffbb1c8232f3068f393c98cd5702d286ab301b502c.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=7{t}^{5}\,i-4{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7t\,i-4\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 112, \frac{56}{9}, \frac{224}{9}, 224, - \frac{224}{9}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=35{t}^{4}\,i-16{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-7i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}x\,\text{d}y & =-{∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & =-{∮}_{{C}_{1}}x\,dy-{∮}_{{C}_{2}}x\,dy \\  & =-{\int }_{-1}^{1}7{t}^{5}\cdot (-16{t}^{3})\,\text{d}t-{\int }_{-1}^{1}(-7t)\cdot 0\,\text{d}t \\  & =112{\int }_{-1}^{1}{t}^{8}\,\text{d}t+0 \\  & =112[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =112\left(\frac{1^{9}}{9}-\frac{(-1)^{9}}{9}\right) \\  & =112\left(\frac{1}{9}-\left(-\frac{1}{9}\right)\right) \\  & =112\cdot \frac{2}{9} \\  & =\frac{224}{9}.\end{aligned}
$$


## Generated eligible ellipse {'a': 2, 'b': 3}

Use Green's theorem to find the area of the region $D$ enclosed by the curve $C$ parametrized as $r(t)=2\cos t\,i+3\sin t\,j$ for $t\in[0,2\pi].$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/eaab9c42be1a72f7179d20b7073880217c67f2ce35dc9f6adbc17ef302424eba.png)


Choices: 3 \pi, 12 \pi, - 6 \pi, 6 \pi, 2 \pi

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, smooth, closed path $C$ is positively oriented, and

$$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=0-(-1)=1.$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$\begin{aligned}\text{Area}(D)&=\iint_D\text{d}A\\&=\iint_D(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y})\,\text{d}A\\&=\oint_C P\,\text{d}x+Q\,\text{d}y\end{aligned}$$

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$\oint_C P\,\text{d}x+Q\,\text{d}y=-\oint_C y\,\text{d}x.$$

The derivative of $r(t)$ is

$$r'(t)=\langle -2\sin t,3\cos t\rangle.$$

Therefore, we can write our line integral as

$$\begin{aligned}-\oint_C y\,\text{d}x&=-\int_0^{2\pi}3\sin t\cdot(-2\sin t)\,\text{d}t\\&=6\int_0^{2\pi}\sin^2 t\,\text{d}t\\&=6\int_0^{2\pi}\frac{1-\cos 2t}{2}\,\text{d}t\\&=\int_0^{2\pi}\left(3-3\cos 2t\right)\,\text{d}t\\&=\left[3t-\frac{3}{2}\sin 2t\right]_0^{2\pi}\\&=\left(6 \pi-0\right)-\left(0-0\right)\\&=6 \pi\end{aligned}$$

Therefore, we conclude that $\text{Area}(D)=6 \pi.$


## Generated eligible ellipse {'a': 5, 'b': 4}

Use Green's theorem to find the area of the region $D$ enclosed by the curve $C$ parametrized as $r(t)=5\cos t\,i+4\sin t\,j$ for $t\in[0,2\pi].$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/979b2c44553420f9dab7b4c59f40a9990ea5c3dfe1d90cd4bed29c283028db97.png)


Choices: 4 \pi, 40 \pi, - 20 \pi, 20 \pi, 5 \pi

First, let $P(x,y)=-y$ and $Q(x,y)=0.$

Our simple, smooth, closed path $C$ is positively oriented, and

$$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=0-(-1)=1.$$

So, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:

$$\begin{aligned}\text{Area}(D)&=\iint_D\text{d}A\\&=\iint_D(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y})\,\text{d}A\\&=\oint_C P\,\text{d}x+Q\,\text{d}y\end{aligned}$$

Substituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get

$$\oint_C P\,\text{d}x+Q\,\text{d}y=-\oint_C y\,\text{d}x.$$

The derivative of $r(t)$ is

$$r'(t)=\langle -5\sin t,4\cos t\rangle.$$

Therefore, we can write our line integral as

$$\begin{aligned}-\oint_C y\,\text{d}x&=-\int_0^{2\pi}4\sin t\cdot(-5\sin t)\,\text{d}t\\&=20\int_0^{2\pi}\sin^2 t\,\text{d}t\\&=20\int_0^{2\pi}\frac{1-\cos 2t}{2}\,\text{d}t\\&=\int_0^{2\pi}\left(10-10\cos 2t\right)\,\text{d}t\\&=\left[10t-5\sin 2t\right]_0^{2\pi}\\&=\left(20 \pi-0\right)-\left(0-0\right)\\&=20 \pi\end{aligned}$$

Therefore, we conclude that $\text{Area}(D)=20 \pi.$


## Generated opaque evidence only sin_sin2 {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/8c1a9bb940480d5c1dd2a5a5a8019f5b1cde1d9c8a29d7b7245ea27f8d84c323.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡t\,i+5\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$


Choices: 20, \frac{75}{4}, \frac{85}{4}, 25, 30, 30, 20, 25, \frac{85}{4}, \frac{75}{4}

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
\begin{aligned}{r}^{′}(t) & =3\operatorname{cos}⁡t\,i+10\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}y\,dx & ={\int }_{0}^{\pi }5\operatorname{sin}⁡2t\cdot 3\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =30{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =10{{u}^{3}|}_{-1}^{1} \\  & =10({1}^{3}-(-1)^{3}) \\  & =20\end{aligned}
$$


## Generated opaque evidence only sin_sin2 {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/1f4458127c574a761374c1c37cb0e078a16450d657e6ed355e0c8ce2e843b0bb.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡t\,i+4\operatorname{sin}⁡2t\,j$ 
for $t\in [0,\pi ].$


Choices: \frac{112}{3}, 35, \frac{119}{3}, \frac{140}{3}, 56, 56, \frac{112}{3}, \frac{140}{3}, \frac{119}{3}, 35

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
\begin{aligned}{r}^{′}(t) & =7\operatorname{cos}⁡t\,i+8\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}y\,dx & ={\int }_{0}^{\pi }4\operatorname{sin}⁡2t\cdot 7\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =56{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{{u}^{3}|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated opaque evidence only right_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/0e9c0ec9d74a47ef3227f7abc6da634a67f2265fc23a5a5bb186d98963fde6c5.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 3t^{2}i - 5t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 3i + 5tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: 10, \frac{35}{2}, 12, 15, 30

[Absent in source; retained as absent in raw replay.]


## Generated opaque evidence only right_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e853bb110b4a18524dcc77df412ea0a0f2ce3ecbddf592553e63fa86ae78bd6b.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 7t^{2}i - 4t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 7i + 4tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: \frac{56}{3}, \frac{98}{3}, \frac{112}{5}, 28, 56

[Absent in source; retained as absent in raw replay.]


## Generated opaque evidence only sin2_minus_sin {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/30fb2d3f47372bd78750cbf689771cc7f2ea176d9ad3311ebdeb6f0ce756151a.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡2t\,i-5\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$


Choices: \frac{125}{4}, 20, \frac{105}{8}, \frac{225}{8}, \frac{75}{2}

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
\begin{aligned}{r}^{′}(t) & =6\operatorname{cos}⁡2t\,i-5\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}x\,dy & =-{\int }_{0}^{\pi }3\operatorname{sin}⁡2t\cdot (-5\operatorname{cos}⁡t)\,\text{d}t \\  & =15{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =15{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =30{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated opaque evidence only sin2_minus_sin {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2e820016efddd732de442da09b5ebbb65543e5930dc52d3eb9e393ce8bfb4b26.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡2t\,i-4\operatorname{sin}⁡t\,j$ 
for $t\in [0,\pi ].$


Choices: \frac{175}{3}, \frac{112}{3}, \frac{49}{2}, \frac{105}{2}, 70

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
\begin{aligned}{r}^{′}(t) & =14\operatorname{cos}⁡2t\,i-4\operatorname{cos}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{cos}⁡t,\text{d}u=-\operatorname{sin}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}x\,dy & =-{\int }_{0}^{\pi }7\operatorname{sin}⁡2t\cdot (-4\operatorname{cos}⁡t)\,\text{d}t \\  & =28{\int }_{0}^{\pi }\operatorname{sin}⁡2t\operatorname{cos}⁡t\,\text{d}t \\  & =28{\int }_{0}^{\pi }2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t \\  & =56{\int }_{0}^{\pi }\operatorname{sin}⁡t{cos}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated opaque evidence only sin2_cos {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/5cd570cb430eaec856688b17f0b046c979534da255fd5a4f48e5e9444af2fbe8.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=3\operatorname{sin}⁡2t\,i+5\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 20, 10, \frac{75}{2}, \frac{45}{2}, 105\pi 

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
\begin{aligned}{r}^{′}(t) & =6\operatorname{cos}⁡2t\,i-5\operatorname{sin}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{\pi /2}^{3\pi /2}3\operatorname{sin}⁡2t\cdot (-5\operatorname{sin}⁡t)\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-30{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated opaque evidence only sin2_cos {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/63267b7ad54dd7435ed6b6787c320d4c13734ee76f82414d3432db4403c54a79.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=7\operatorname{sin}⁡2t\,i+4\operatorname{cos}⁡t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: \frac{112}{3}, \frac{56}{3}, 70, 42, 196\pi 

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
\begin{aligned}{r}^{′}(t) & =14\operatorname{cos}⁡2t\,i-4\operatorname{sin}⁡t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}{∮}_{C}x\,dy & ={\int }_{\pi /2}^{3\pi /2}7\operatorname{sin}⁡2t\cdot (-4\operatorname{sin}⁡t)\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-56{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated opaque evidence only left_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e9211aa9722bfe620c7da6d877f4136efdf984f46df2b5a763dc11ebb05d6bca.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-3{t}^{2}\,i+5{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3\,i-t\,j$ for $t\in [-5,5].$

Use Green's theorem to find the area of the region.


Choices: 15, \frac{35}{3}, 2, 12, 10

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=-6t\,i+15{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}5{t}^{3}\cdot (-6t)\,\text{d}t-{\int }_{-5}^{5}(-t)\cdot 0\,\text{d}t \\  & =30{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =30[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =30\cdot \frac{2}{5} \\  & =\frac{60}{5}.\end{aligned}
$$


## Generated opaque evidence only left_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/4e8cdfcadeac24945596824d763801e2ef44d2050a35e19390238bd47c3c951b.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=-7{t}^{2}\,i+4{t}^{3}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7\,i-t\,j$ for $t\in [-4,4].$

Use Green's theorem to find the area of the region.


Choices: 28, \frac{196}{9}, \frac{56}{15}, \frac{112}{5}, \frac{56}{3}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=-14t\,i+12{t}^{2}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-j\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}y\,\text{d}x & =-{∮}_{{C}_{1}\cup {C}_{2}}y\,dx \\  & =-{∮}_{{C}_{1}}y\,dx-{∮}_{{C}_{2}}y\,dx \\  & =-{\int }_{-1}^{1}4{t}^{3}\cdot (-14t)\,\text{d}t-{\int }_{-4}^{4}(-t)\cdot 0\,\text{d}t \\  & =56{\int }_{-1}^{1}{t}^{4}\,\text{d}t-0 \\  & =56[\frac{{t}^{5}}{5}]_{-1}^{1} \\  & =56\cdot \frac{2}{5} \\  & =\frac{112}{5}.\end{aligned}
$$


## Generated opaque evidence only upper_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/887785c19d2bd96c9d0586f54ecc6d065b108e990b7226d5dffe021e63312df3.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=3{t}^{5}\,i+5{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3t\,i+5\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 60, \frac{40}{3}, 10, 75, \frac{75}{4}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=15{t}^{4}\,i+20{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-3i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,\text{d}y & ={∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & ={∮}_{{C}_{1}}x\,dy+{∮}_{{C}_{2}}x\,dy \\  & ={\int }_{-1}^{1}3{t}^{5}\cdot 20{t}^{3}\,\text{d}t+{\int }_{-1}^{1}(-3t)\cdot 0\,\text{d}t \\  & =60{\int }_{-1}^{1}{t}^{8}\,\text{d}t-0 \\  & =60[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =60\cdot \frac{2}{9} \\  & =\frac{120}{9}.\end{aligned}
$$


## Generated opaque evidence only upper_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/b4d4164695724c45b683ae27b2194ad5245837f8663d7f4d1369f2da7d49c23d.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=7{t}^{5}\,i+4{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7t\,i+4\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 112, \frac{224}{9}, \frac{56}{3}, 140, 35

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=35{t}^{4}\,i+16{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-7i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}{∮}_{C}x\,\text{d}y & ={∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & ={∮}_{{C}_{1}}x\,dy+{∮}_{{C}_{2}}x\,dy \\  & ={\int }_{-1}^{1}7{t}^{5}\cdot 16{t}^{3}\,\text{d}t+{\int }_{-1}^{1}(-7t)\cdot 0\,\text{d}t \\  & =112{\int }_{-1}^{1}{t}^{8}\,\text{d}t-0 \\  & =112[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =112\cdot \frac{2}{9} \\  & =\frac{224}{9}.\end{aligned}
$$


## Generated opaque evidence only minus_cos_sin2 {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/f7c5c2a0d5d37471f6db673ec9fc92d301deb745be1eb31d93ab0f46e1eb6b00.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-3\operatorname{cos}⁡t\,i+5\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: 20, 15\pi , \frac{75}{4}, \frac{45}{8}, 10

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
\begin{aligned}{r}^{′}(t) & =3\operatorname{sin}⁡t\,i+10\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}y\,dx & =-{\int }_{\pi /2}^{3\pi /2}5\operatorname{sin}⁡2t\cdot 3\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-15{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-30{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-30{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =30{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{30}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{30}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{60}{3}\end{aligned}
$$


## Generated opaque evidence only minus_cos_sin2 {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/131bbf32a3a090a42bcb695a46dcaeecbbd51df53ecff3733e0a8376a63759ba.png)

Use Green's theorem to find the area of the region enclosed by the curve 
$C$ parametrized as $r(t)=-7\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡2t\,j$ 
for $t\in [\frac{\pi }{2},\frac{3\pi }{2}].$


Choices: \frac{112}{3}, 28\pi , 35, \frac{21}{2}, \frac{56}{3}

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
\begin{aligned}{r}^{′}(t) & =7\operatorname{sin}⁡t\,i+8\operatorname{cos}⁡2t\,j.\end{aligned}
$$

Finally, we can evaluate our line integral using the substitution $u=\operatorname{sin}⁡t,\text{d}u=\operatorname{cos}⁡t\,\text{d}t,$ as follows:

$$
\begin{aligned}-{∮}_{C}y\,dx & =-{\int }_{\pi /2}^{3\pi /2}4\operatorname{sin}⁡2t\cdot 7\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}\operatorname{sin}⁡2t\operatorname{sin}⁡t\,\text{d}t \\  & =-28{\int }_{\pi /2}^{3\pi /2}2\operatorname{sin}⁡t\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t\,\text{d}t \\  & =-56{\int }_{\pi /2}^{3\pi /2}\operatorname{cos}⁡t{sin}^{2}⁡t\,\text{d}t \\  & =-56{\int }_{1}^{-1}{u}^{2}\,\text{d}u \\  & =56{\int }_{-1}^{1}{u}^{2}\,\text{d}u \\  & =\frac{56}{3}{u}^{3}{|}_{-1}^{1} \\  & =\frac{56}{3}({1}^{3}-(-1)^{3}) \\  & =\frac{112}{3}\end{aligned}
$$


## Generated opaque evidence only lower_polynomial {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/bb87f082257bd436b7f89a6d5ea0500ac81da8c6d811ebbc37adddaf42504298.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=3{t}^{5}\,i-5{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-3t\,i-5\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: \frac{75}{2}\pi , \frac{225}{4}, \frac{45}{2}\pi , 18, \frac{40}{3}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=15{t}^{4}\,i-20{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-3i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}x\,\text{d}y & =-{∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & =-{∮}_{{C}_{1}}x\,dy-{∮}_{{C}_{2}}x\,dy \\  & =-{\int }_{-1}^{1}3{t}^{5}\cdot (-20{t}^{3})\,\text{d}t-{\int }_{-1}^{1}(-3t)\cdot 0\,\text{d}t \\  & =60{\int }_{-1}^{1}{t}^{8}\,\text{d}t+0 \\  & =60[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =60\cdot \frac{2}{9} \\  & =\frac{120}{9}.\end{aligned}
$$


## Generated opaque evidence only lower_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ce072d943595a89a093d12ffbb1c8232f3068f393c98cd5702d286ab301b502c.png)

Consider the region $D$ enclosed by the curve $C={C}_{1}\cup {C}_{2},$ where 

- ${C}_{1}$ is parametrized by ${r}_{1}(t)=7{t}^{5}\,i-4{t}^{4}\,j$ for $t\in [-1,1],$ and

- ${C}_{2}$ is parametrized by ${r}_{2}(t)=-7t\,i-4\,j$ for $t\in [-1,1].$

Use Green's theorem to find the area of the region.


Choices: 70\pi , 105, 42\pi , \frac{168}{5}, \frac{224}{9}

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
\begin{aligned}{C}_{1}:\, & {r}_{1}^{′}(t)=35{t}^{4}\,i-16{t}^{3}\,j \\ {C}_{2}:\, & {r}_{2}^{′}(t)=-7i\end{aligned}
$$

Therefore, we can write our line integral as

$$
\begin{aligned}-{∮}_{C}x\,\text{d}y & =-{∮}_{{C}_{1}\cup {C}_{2}}x\,dy \\  & =-{∮}_{{C}_{1}}x\,dy-{∮}_{{C}_{2}}x\,dy \\  & =-{\int }_{-1}^{1}7{t}^{5}\cdot (-16{t}^{3})\,\text{d}t-{\int }_{-1}^{1}(-7t)\cdot 0\,\text{d}t \\  & =112{\int }_{-1}^{1}{t}^{8}\,\text{d}t+0 \\  & =112[\frac{{t}^{9}}{9}]_{-1}^{1} \\  & =112\cdot \frac{2}{9} \\  & =\frac{224}{9}.\end{aligned}
$$