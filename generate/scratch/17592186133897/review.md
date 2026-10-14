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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/3a5126082a3f6b1f30fa645564f6c3a85d9c5702f40f087410138f6c587eb0b0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2db8cd7a471113439b23b21c41c854a84f999ab65c8b098fe00cfcb3e0d9e2a4.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/0cab9524ed5c7f4023193a3efad2588fbce2ce544cb0a86491b524fb21c7466a.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ccb98396c7e1760c6efb13b36f24d388a6d1f8a4cd03c54ce88d618bdca961ef.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/f58a47e08eabf2de82fda04ec87aad2988491b2bd6e680d4eaa8dfea9309d109.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/81ab8e10a0380e0ed4456f6b6f02da216a2dc73517b991444523ff6412f0c5fd.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2a7ed035e38384165fdfbdd64543c88cf3f0e635d10e2a678d51ca9f9e6830b0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/45035580a57ce8f599b621f05a35f8200939b31005e793ca166ed55304189b0f.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e2e31ee75e23064551a238fa20e0347a0f8411d7cef6532197edce296ed78e40.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/c4c276f93d8955366ecc4c454e29f75c7bef590fc477145193cd5e9594520c5d.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ccb7a568cc16e9bc1fb335687b5b6dcd8165fe15204c90481224a531a863d1cc.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/37a6d96c6019e307e5f473444f9dc6e34e813f7916f731fa7827c2ee5e913f8b.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/a1a5a6e41db84d94f5fd3771e679cd0e586dd00cea7bf5bd94f1b465a272cb8f.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/17064959715aa61f33310535b823bedadd7af0a316513d3e011755d303821141.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/aaecef4b8ef2ac4f9d6f8213db72f781227fe20fa53c58b4917e96667228e091.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/fc2a08384c1b6153e62c2083be5cdbaaaeffc323f2567e93371dfe08e2e6bbdd.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/0f9dda57b5eb537104fde7ea4914e3f8d69dd510e3674806af488ab8690db5a2.png)


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/aeed97266f8b5d287dfdde21ab6a3b16205c2ae5e461fba25398e3a743520485.png)


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/3a5126082a3f6b1f30fa645564f6c3a85d9c5702f40f087410138f6c587eb0b0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2db8cd7a471113439b23b21c41c854a84f999ab65c8b098fe00cfcb3e0d9e2a4.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/0cab9524ed5c7f4023193a3efad2588fbce2ce544cb0a86491b524fb21c7466a.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 3t^{2}i - 5t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 3i + 5tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: 10, \frac{35}{2}, 12, 15, 30

[Absent in source; retained as absent in raw replay.]


## Generated opaque evidence only right_polynomial {'a': 7, 'b': 4}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ccb98396c7e1760c6efb13b36f24d388a6d1f8a4cd03c54ce88d618bdca961ef.png)

Consider the region $D$ enclosed by the curve $C = C_{1}∪C_{2}$, where

- $C_{1}$ is parametrized by $r_{1}(t) = 7t^{2}i - 4t^{3}j$ for $t ∈ [- 1, 1]$, and
- $C_{2}$ is parametrized by $r_{2}(t) = 7i + 4tj$ for $t ∈ [- 1, 1]$.

Use Green's theorem to find the area of the region.


Choices: \frac{56}{3}, \frac{98}{3}, \frac{112}{5}, 28, 56

[Absent in source; retained as absent in raw replay.]


## Generated opaque evidence only sin2_minus_sin {'a': 3, 'b': 5}

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/f58a47e08eabf2de82fda04ec87aad2988491b2bd6e680d4eaa8dfea9309d109.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/81ab8e10a0380e0ed4456f6b6f02da216a2dc73517b991444523ff6412f0c5fd.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/2a7ed035e38384165fdfbdd64543c88cf3f0e635d10e2a678d51ca9f9e6830b0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/45035580a57ce8f599b621f05a35f8200939b31005e793ca166ed55304189b0f.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/e2e31ee75e23064551a238fa20e0347a0f8411d7cef6532197edce296ed78e40.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/c4c276f93d8955366ecc4c454e29f75c7bef590fc477145193cd5e9594520c5d.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/ccb7a568cc16e9bc1fb335687b5b6dcd8165fe15204c90481224a531a863d1cc.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/37a6d96c6019e307e5f473444f9dc6e34e813f7916f731fa7827c2ee5e913f8b.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/a1a5a6e41db84d94f5fd3771e679cd0e586dd00cea7bf5bd94f1b465a272cb8f.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/17064959715aa61f33310535b823bedadd7af0a316513d3e011755d303821141.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/aaecef4b8ef2ac4f9d6f8213db72f781227fe20fa53c58b4917e96667228e091.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133897/plots/fc2a08384c1b6153e62c2083be5cdbaaaeffc323f2567e93371dfe08e2e6bbdd.png)

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