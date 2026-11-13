# 17592186051063 Describing Planar Regions Using Set-Builder Notation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186199551 — Introduction

We can use set-builder notation to represent sets that lie in the coordinate plane.

For example, let's describe the following shaded region using set-builder-notation.

![](images/2c/2c4545ab59c1bf6847ab38b09ddf8b86c3227bbc6006835aceb8637b45bff817.png)

  

First, notice that a point $P(x,y)$ lies *inside* the rectangle if the following conditions are satisfied:

$$
\begin{aligned}2<x<6,\hspace{2em}2<y<5.\end{aligned}
$$

However, notice that we also need to   

- *include* the left edge ($x=2$), and

- *include* the right edge ($x=6$).

Therefore, we change the corresponding inequality symbols to non-strict, as follows:

$$
\begin{aligned}2\bbox[Gainsboro, 2pt]{{\color{blue}\le }}x\bbox[Gainsboro, 2pt]{{\color{blue}\le }}6,\hspace{2em}2<y<5.\end{aligned}
$$

Moreover, since *every* real value in these intervals is included, $x\in \mathbb R, y\in\mathbb R,$ and therefore 

$$
(x,y)\in \mathbb R\times\mathbb R = \mathbb R^2.
$$

Thus, we can write our set as follows:

$$
\Big\{
(x,y) \in \mathbb R^2
\: : \:  

2 
\bbox[2pt,Gainsboro]{\color{blue}\leq} 
x 
\bbox[2pt,Gainsboro]{\color{blue}\leq}  
6, 
\: 
2 
\bbox[2pt,Gainsboro]{\color{blue}\lt} 
y
\bbox[2pt,Gainsboro]{\color{blue}\lt}   
5 
\Big\}.
$$



### example 17592186198151 — Describing Rectangular Sets Using Set-Builder Notation

![](images/89/89fa15ffb9a7f6b319cf3b9ff0de4ab821a15f632d7f93618fbe99b7979260f4.png)

Describe the set of points shown above using set-builder notation.

Since all points $P(x,y)$ in our set lie at integer values of $x$ and $y,$ we have $x\in \mathbb Z, y\in\mathbb Z,$ and therefore 

$$
(x,y)\in \mathbb Z\times\mathbb Z = \mathbb Z^2.
$$

The points $P(x,y)$ satisfy the condition

$$
x \in \{1,2,3\}, \quad y \in \{ -3,-2,-1,0,1,2 \}.
$$

In other words,

$$
1 \leq x \leq 3, \quad -3 \leq y \leq 2
$$

Therefore, we can write our set as follows:

$$
\Big\{ (x,y)  \in \bbox[2pt,Gainsboro]{\color{blue}\mathbb Z^2}
\: : \: 
\bbox[2pt,Gainsboro]{\color{blue}1}  
\leq  x \leq  
\bbox[2pt,Gainsboro]{\color{blue}3} , \: 
\bbox[2pt,Gainsboro]{\color{blue}-3}  
\leq  y \leq  
\bbox[2pt,Gainsboro]{\color{blue}2} 
\Big\}.
$$

### example 17592186198163 — Linear Boundaries, One Condition

![](images/78/787b62fbe367feae9e4c8ed10b983a256840e3a93727fea7c1ff67cacad0129d.png)

Describe the shaded region shown above using set-builder notation.

Since all points $P(x,y)$ in our set lie at integer values of $x$ and $y,$ we have $x\in \mathbb Z, y\in\mathbb Z,$ and therefore 

$$
(x,y)\in \mathbb Z\times\mathbb Z = \mathbb Z^2.
$$

The points in our set include all those that lie *below* the line $y=x+2.$ For those points, the following condition is satisfied:

$$
y \lt x+2
$$

Also, notice that some points in our set lie *on* the line. We include these points by changing the inequality symbol above as follows:

$$
y \bbox[2pt,Gainsboro]{\color{blue}\leq }x+2
$$

Therefore, we can write the set as follows:

$$
\Big\{(x,y) \in \bbox[2pt,Gainsboro]{\color{blue}\mathbb Z ^2} \: : \: y \bbox[2pt,Gainsboro]{\color{blue}\leq }x+2 \Big\}
$$

### example 17592186198152 — Linear Boundaries, Two Conditions

![](images/45/45260087c5196cc239f21402d73169f60139bd7d2c10ee0aa1db4e1a2c56be4a.png)

Describe the shaded region shown above using set-builder notation.

The points in our set include all those that lie *above* the line $y=2x$ and *below* the line $y=3.$

A point $P(x,y)$ lies *inside* the shaded region if the following conditions are satisfied:

$$
y \gt 2x, \qquad y < 3.
$$

Combining this into a single condition, we have

$$
2x \lt y < 3.
$$

We must also include the line $y= 3$ since the boundary is included in the set (the curve is solid). So, we change the corresponding inequality symbol above as follows:

$$
2x \lt y  \bbox[2pt,Gainsboro]{\color{blue}\leq } 3
$$

Moreover, since we're considering *every* real value in this region, $x\in \mathbb R, y\in\mathbb R,$ and therefore 

$$
(x,y)\in \mathbb R\times\mathbb R = \mathbb R^2.
$$

Therefore, we can write the set as

$$
\Big\{(x,y)\in \bbox[2pt,Gainsboro]{\color{blue}\mathbb R^2 } \: : \:  2x \bbox[2pt,Gainsboro]{\color{blue}\lt } y \bbox[2pt,Gainsboro]{\color{blue}\leq } 3 \Big\}.
$$

### example 17592186198153 — Describing Non-Rectangular Sets Using Set-Builder Notation

Use set builder notation to describe the shaded region given in the diagram below:

![](images/e5/e5f5f2f2e67ba0ad566b2759ca5536d248f671bf0f082d567a7f7d993772601e.png)

The equation of an ellipse centered at the origin with a horizontal radius of length $a$ and a vertical radius of length $b$ is given by

$$
\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1.
$$

 

Here, the elliptical boundary of our region has horizontal radius $a=5$ and vertical radius $b=4.$ Therefore, the equation of the ellipse is

$$
\begin{aligned}\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16} & =1,\end{aligned}
$$

which we can write as

$$
16x^2 + 25y^2 = 400.
$$

We're interested in describing all points that lie *outside* the ellipse. So, let's pick any point outside the ellipse, say, $(10,0).$ Substituting its coordinates into the equation of the boundary, we obtain

$$
16(10)^2+25(0)^2 \: {\color{blue}>} \: 400.
$$

As a result, the points $P(x,y)$ in our region are any real numbers that satisfy the condition

$$
16x^2 + 25y^2  \gt 400.
$$

We must also include the curve $16x^2 + 25y^2 = 400$ since the boundary is included in the set (the curve is solid). So, we change the inequality symbol above as follows:

$$
16x^2 + 25y^2  \bbox[2pt,Gainsboro]{\color{blue}\geq } 400.
$$

Therefore, we can write the set as

$$
\Big\{(x,y) \in \mathbb{R}^2 \: : \: \bbox[2pt,Gainsboro]{\color{blue}16 }x^2 + \bbox[2pt,Gainsboro]{\color{blue}25 }y^2  \bbox[2pt,Gainsboro]{\color{blue}\geq } 400 \bigg\}.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Describing Rectangular Sets Using Set-Builder Notation (10 captured questions)

Question 17592186198772 — question.difficulty/easy

![](images/d5/d550ecec3b7103c9510b6e45e738ae1385e07fa63ff2e50c54da6c17606faaec.png)

Describe the set of points shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,{{field-2}}\le x\le {{field-3}},\,{{field-4}}\le y\le {{field-5}}\}
$$

Solution: Since all points $P(x,y)$ in our set lie at integer values of $x$ and $y,$ we have $x\in \mathbb{Z},y\in \mathbb{Z},$ and therefore 

$$
(x,y)\in \mathbb{Z}\times \mathbb{Z}={\mathbb{Z}}^{2}.
$$

The points $P(x,y)$ satisfy the condition

$$
x\in \{-3,-2,-1\},\hspace{1em}y\in \{-4,-3,-2,-1\}.
$$

In other words,

$$
-3\le x\le -1,\hspace{1em}-4\le y\le -1
$$

Therefore, we can write our set as follows:

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{Z}}^{2}}}\hspace{0.222em}:\hspace{0.222em}\bbox[Gainsboro, 2pt]{{\color{blue}-3}}\le x\le \bbox[Gainsboro, 2pt]{{\color{blue}-1}},\hspace{0.222em}\bbox[Gainsboro, 2pt]{{\color{blue}-4}}\le y\le \bbox[Gainsboro, 2pt]{{\color{blue}-1}}\}.
$$

Answer field-1: {Z}^{2}

Answer field-2: -3

Answer field-3: -1

Answer field-4: -4

Answer field-5: -1

Question 17592186198781 — None

![](images/25/250e250d7de7bb59cc394018b1f4645ea16b8ccab2cce3f2ddb3337dbb714c13.png)

Describe the shaded region shown above using set-builder notation.

$R=\{(x,y)\in {{field-1}}:{{field-2}}<x<{{field-3}},\ {{field-4}}<y<{{field-5}}\}$

Solution: The diagram shades a rectangle between $x=1$ and $x=5$, and between $y=2$ and $y=4$. Each boundary is dashed, so none of the four edges is included. The shaded region contains all real coordinate pairs satisfying these strict inequalities. Therefore,

$$
R=\{(x,y)\in\mathbb R^2:1<x<5,\ 2<y<4\}.
$$



Answer field-1: R^{2}

Answer field-2: 1

Answer field-3: 5

Answer field-4: 2

Answer field-5: 4

Question 17592186287677 — question.difficulty/easy

![](images/37/37294502ac1c3c15790f5b820b2499fd03c16edb53b2faa90080507f3065eb84.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,{{field-2}}\le x\le {{field-3}},\,{{field-4}}\le y\le {{field-5}}\}
$$

Solution: A point $P(x,y)$ lies inside or on the rectangle's edges if the following conditions are satisfied:

$$
\begin{aligned}-1\le x\le 5,\hspace{2em}1\le y\le 3.\end{aligned}
$$

Moreover, since *every* real value in these intervals is included, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write our set as follows:

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}\bbox[Gainsboro, 2pt]{{\color{blue}-1}}\le x\le \bbox[Gainsboro, 2pt]{{\color{blue}5}},\hspace{0.222em}\bbox[Gainsboro, 2pt]{{\color{blue}1}}\le y\le \bbox[Gainsboro, 2pt]{{\color{blue}3}}\}
$$

Answer field-1: {R}^{2}

Answer field-2: -1

Answer field-3: 5

Answer field-4: 1

Answer field-5: 3

### Linear Boundaries, One Condition (12 captured questions)

Question 17592186198777 — question.difficulty/easy

![](images/f0/f00499aad7b915267fe99bde8c13665a325cf6409e2e856466e9cdc90e4a8b8a.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,2x-3\}
$$

Solution: The points in our set include all those that lie *below* the line $y=2x-3.$

Therefore, a point $P(x,y)$ lies *inside* the shaded region if the following condition is satisfied:

$$
y<2x-3
$$

We must also include the line $y=2x-3$ since the boundary is included in the set (the curve is solid). So, we change the inequality symbol above as follows:

$$
y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}2x-3
$$

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}2x-3\}.
$$

Answer field-1: {R}^{2}

Answer field-2: \le 

Question 17592186198805 — question.difficulty/moderate

![](images/cc/cce16725dddcfc83098ee2323576b8e01bbc3f2625d17cb7e6030826ad9fbcd8.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,x-1\}
$$

Solution: Since all points $P(x,y)$ in our set lie at integer values of $x$ and $y,$ we have $x\in \mathbb{Z},y\in \mathbb{Z},$ and therefore 

$$
(x,y)\in \mathbb{Z}\times \mathbb{Z}={\mathbb{Z}}^{2}.
$$

The points in our set include all those that lie *below* the line $y=x-1.$ For those points, the following condition is satisfied:

$$
y<x-1
$$

Since the boundary is *not* included in the set (the curve is *not* solid),  no further action must be taken, so we have

$$
y\bbox[Gainsboro, 2pt]{{\color{blue}<}}x-1.
$$

Therefore, we can write the set as follows:

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{Z}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}<}}x-1\}
$$

Answer field-1: {Z}^{2}

Answer field-2: <

Question 17592186287779 — question.difficulty/moderate

![](images/01/010d4befaa2bd2142cf63010f79f071df331bb6394eb65e4f883752cb04a2cb4.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,-x+1\}
$$

Solution: Since all points $P(x,y)$ in our set lie at integer values of $x$ and $y,$ we have $x\in \mathbb{Z},y\in \mathbb{Z},$ and therefore 

$$
(x,y)\in \mathbb{Z}\times \mathbb{Z}={\mathbb{Z}}^{2}.
$$

The points in our set include all those that lie *above* the line $y=-x+1.$ For those points, the following condition is satisfied:

$$
y>-x+1
$$

Also, notice that some points in our set lie *on* the line. We include these points by changing the inequality symbol above as follows:

$$
y\bbox[Gainsboro, 2pt]{{\color{blue}\ge }}-x+1
$$

Therefore, we can write the set as follows:

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{Z}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}\ge }}-x+1\}
$$

Answer field-1: {Z}^{2}

Answer field-2: \ge 

### Linear Boundaries, Two Conditions (12 captured questions)

Question 17592186198788 — question.difficulty/moderate

![](images/83/83ebd6f5d742a869b267a0cead4a9a94ae17fa534ca3e1cfddbb495c67390ecf.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,-x\,{{field-2}}\,y\,{{field-3}}\,2\}
$$

Solution: The points in our set include all those that lie *above* the line $y=-x$ and *below* the line $y=2.$

A point $P(x,y)$ lies *inside* the shaded region if the following conditions are satisfied:

$$
y>-x,\hspace{2em}y<2.
$$

Combining this into a single condition, we have

$$
-x<y<2.
$$

We must also include the line $y=-x$ since the boundary is included in the set (the curve is solid). So, we change the corresponding inequality symbol above as follows:

$$
-x\bbox[Gainsboro, 2pt]{{\color{blue}\le }}y<2
$$

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}-x\bbox[Gainsboro, 2pt]{{\color{blue}\le }}y\bbox[Gainsboro, 2pt]{{\color{blue}<}}2\}.
$$

Answer field-1: {R}^{2}

Answer field-2: \le 

Answer field-3: <

Question 17592186198793 — question.difficulty/easy

![](images/0f/0f95f6b259237816a5a3da041452cfd9458f0852b1ae717a044738b6f310ab5d.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,3\,{{field-2}}\,y\,{{field-3}}\,2x+3\}
$$

Solution: The points in our set include all those that lie *above* the line $y=3$ and *below* the line $y=2x+3.$

A point $P(x,y)$ lies *inside* the shaded region if the following conditions are satisfied:

$$
y>3,\hspace{2em}y<2x+3.
$$

Combining this into a single condition, we have

$$
3<y<2x+3.
$$

We must also include the lines $y=3$ and $y=2x+3$ since the boundaries are included in the set (the lines are solid). So, we change the corresponding inequality symbols above as follows:

$$
3\bbox[Gainsboro, 2pt]{{\color{blue}\le }}y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}2x+3
$$

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}3\bbox[Gainsboro, 2pt]{{\color{blue}\le }}y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}2x+3\}.
$$

Answer field-1: {R}^{2}

Answer field-2: \le 

Answer field-3: \le 

Question 17592186287718 — question.difficulty/easy

![](images/71/718ee39f4a0b2e9cca18ed4de77271a90139b13e8b71990611c1e13357245713.png)

Describe the shaded region shown above using set-builder notation.

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,-x+5,\,y\,{{field-3}}\,x+3\}
$$

Solution: The points in our set include all those that lie *below* the line $y=-x+5$ and *below* the line $y=x+3.$

A point $P(x,y)$ lies *inside* the shaded region if the following conditions are satisfied:

$$
y<-x+5,\hspace{2em}y<x+3.
$$

Since the boundary is not included in the set (the lines are dashed), the inequalities are strict.

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}<}}-x+5,\hspace{1em}y\bbox[Gainsboro, 2pt]{{\color{blue}<}}x+3\}.
$$

Answer field-1: {R}^{2}

Answer field-2: <

Answer field-3: <

### Describing Non-Rectangular Sets Using Set-Builder Notation (12 captured questions)

Question 17592186198774 — question.difficulty/easy

![](images/5c/5c4ffbb64a754df9a6100fda3fd6eaf4a68f28ac59de4dfb716c2c8b1f2847ab.png)

Use set builder notation to describe the shaded region given in the diagram above:

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,{x}^{2}\}
$$

Solution: The points in our set include all those that lie *below* the curve $y={x}^{2}.$

Therefore, a point $P(x,y)$ lies *inside* the shaded region if the following condition is satisfied:

$$
y<{x}^{2}
$$

We must also include the curve $y={x}^{2}$ since the boundary is included in the set (the curve is solid). So, we change the inequality symbol above as follows:

$$
y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}{x}^{2}
$$

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}\le }}{x}^{2}\}.
$$

Answer field-1: {R}^{2}

Answer field-2: \le 

Question 17592186198790 — question.difficulty/moderate

![](images/fb/fbd778f48199acd5b731e739cb527a990ba28a8d88981d50554d135e853f8815.png)

Use set builder notation to describe the shaded region given in the diagram above:

$\{(x,y)\in {\mathbb{R}}^{2}\hspace{0.222em}:\hspace{0.222em\}$
{{field-1}}
${x}^{2}\hspace{0.222em}+\hspace{0.222em}$
{{field-2}}
${y}^{2}$
{{field-3}}

$36$

$\}$

Solution: The equation of an ellipse centered at the origin with a horizontal radius of length $a$ and a vertical radius of length $b$ is given by

$$
\frac{{x}^{2}}{{a}^{2}}+\frac{{y}^{2}}{{b}^{2}}=1.
$$

 

Here, the elliptical boundary of our region has horizontal radius $a=3$ and vertical radius $b=2.$ Therefore, the equation of the ellipse is

$$
\begin{aligned}\frac{{x}^{2}}{9}+\frac{{y}^{2}}{4} & =1,\end{aligned}
$$

which we can write as

$$
4{x}^{2}+9{y}^{2}=36.
$$

We're interested in describing all points that lie *inside* the ellipse. So, let's pick any point inside the region, say, $(0,0).$ Substituting its coordinates into the equation of the boundary, we obtain

$$
4(0)^{2}+9(0)^{2}\hspace{0.222em}{\color{blue}<}\hspace{0.222em}36.
$$

As a result, the points $P(x,y)$ in our region are any real numbers that satisfy the condition

$$
4{x}^{2}+9{y}^{2}<36.
$$

Notice that we use $<$ since the boundary is excluded from the set (the boundary curve is dashed).

Therefore, we can write the set as

$$
\{(x,y)\in {\mathbb{R}}^{2}\hspace{0.222em}:\hspace{0.222em}\bbox[Gainsboro, 2pt]{{\color{blue}4}}{x}^{2}+\bbox[Gainsboro, 2pt]{{\color{blue}9}}{y}^{2}\bbox[Gainsboro, 2pt]{{\color{blue}<}}36\}.
$$

Answer field-1: 4

Answer field-2: 9

Answer field-3: <

Question 17592186287727 — question.difficulty/easy

![](images/6a/6affe267a93d1dab16de3dc153fddbdb165bab831790f7387dcbd29354ebb63a.png)

Use set builder notation to describe the shaded region given in the diagram above:

$$
\{(x,y)\in {{field-1}}\,:\,y\,{{field-2}}\,-\frac{1}{2}{x}^{2}\}
$$

Solution: The points in our set include all those that lie *below* the curve $y=-\frac{1}{2}{x}^{2}.$

Therefore, a point $P(x,y)$ lies *inside* the shaded region if the following condition is satisfied:

$$
y<-\frac{1}{2}{x}^{2}
$$

Since the boundary is not included in the set (the curve is dashed), the inequality is strict.

Moreover, since we're considering *every* real value in this region, $x\in \mathbb{R},y\in \mathbb{R},$ and therefore 

$$
(x,y)\in \mathbb{R}\times \mathbb{R}={\mathbb{R}}^{2}.
$$

Therefore, we can write the set as

$$
\{(x,y)\in \bbox[Gainsboro, 2pt]{{\color{blue}{\mathbb{R}}^{2}}}\hspace{0.222em}:\hspace{0.222em}y\bbox[Gainsboro, 2pt]{{\color{blue}<}}-\frac{1}{2}{x}^{2}\}.
$$

Answer field-1: {R}^{2}

Answer field-2: <
