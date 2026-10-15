## q-126814

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨3{x}^{5}+2y,\,3{y}^{2}-{e}^{x}⟩
$$

through the boundary of the triangle with vertices $(0,0),(1,1),$ and $(-1,1).$

Original complete bank: ['7', '5', '10', '12', '4']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 21 x^{5} + 14 y, \; 21 y^{2} - 7 e^{x} \right\rangle
$$

through the boundary of the triangle with vertices $(0,0),(1,1),$ and $(-1,1).$

Generated complete bank: ['49', '35', '70', '84', '28']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\,\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/26/269e3c7f92cee66c78f3226e7c967eb51153503c598d2e4d1e4b56a33e646ac4.png)

We have that $P(x,y)=21 x^{5} + 14 y$ and $Q(x,y)=21 y^{2} - 7 e^{x}.$ Therefore,

$$
\frac{\partial P}{\partial x}=105 x^{4},\qquad \frac{\partial Q}{\partial y}=42 y.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 1,\quad - y\leq x\leq y\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(105 x^{4} + 42 y\right)\,dA \\&=\int_{0}^{1}\int_{- y}^{y}\left(105 x^{4} + 42 y\right)\,dx\,dy \\&=\int_{0}^{1}\left[21 x^{5} + 42 x y\right]_{x=- y}^{x=y}\,dy \\&=\int_{0}^{1}\left(42 y^{2} \left(y^{3} + 2\right)\right)\,dy \\&=\left[7 y^{6} + 28 y^{3}\right]_{y=0}^{y=1} \\&=\left(35\right)-\left(0\right) \\&=35.\end{aligned}
$$

## q-126817

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{x}^{2}+2y,\,{x}^{2}+2xy⟩
$$

through the boundary of the region enclosed by the curve $y={x}^{2}$ and the lines $y=0$ and $x=1.$

Original complete bank: ['3', '2', '1', '0', '4']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 7 x^{2} + 14 y, \; 7 x^{2} + 14 x y \right\rangle
$$

through the boundary of the region enclosed by the curve $y={x}^{2}$ and the lines $y=0$ and $x=1.$

Generated complete bank: ['21', '14', '7', '0', '28']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\,\text{d}A
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/91/9168d2ed7eeaa5f1dd331a0a986ac7ecfd6b964217a2cb614deb0cdd54437d65.png)

We have that $P(x,y)=7 x^{2} + 14 y$ and $Q(x,y)=7 x^{2} + 14 x y.$ Therefore,

$$
\frac{\partial P}{\partial x}=14 x,\qquad \frac{\partial Q}{\partial y}=14 x.
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\leq x\leq 1,\quad 0\leq y\leq x^{2}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(28 x\right)\,dA \\&=\int_{0}^{1}\int_{0}^{x^{2}}\left(28 x\right)\,dy\,dx \\&=\int_{0}^{1}\left[28 x y\right]_{y=0}^{y=x^{2}}\,dx \\&=\int_{0}^{1}\left(28 x^{3}\right)\,dx \\&=\left[7 x^{4}\right]_{x=0}^{x=1} \\&=\left(7\right)-\left(0\right) \\&=7.\end{aligned}
$$

## q-127302

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨14xy,\,6{x}^{2}y+\operatorname{sin}⁡x⟩
$$

through the boundary of the region enclosed by the curve $y={x}^{3}$ and the lines $y=0$ and $x=1.$

Original complete bank: ['\\frac{5}{2}', '\\frac{7}{2}', '2', '\\frac{6}{5}', '5']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 98 x y, \; 42 x^{2} y + 7 \sin{\left(x \right)} \right\rangle
$$

through the boundary of the region enclosed by the curve $y={x}^{3}$ and the lines $y=0$ and $x=1.$

Generated complete bank: ['\\frac{35}{2}', '\\frac{49}{2}', '14', '\\frac{42}{5}', '35']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/e6/e6f6a5cf9b37fe16f17fe74face946d85b426badf8db710ca4a7ea308a1ff2ec.png)

We have that $P(x,y)=98 x y$ and $Q(x,y)=42 x^{2} y + 7 \sin{\left(x \right)}.$ Therefore,

$$
\frac{\partial P}{\partial x}=98 y,\qquad \frac{\partial Q}{\partial y}=42 x^{2}.
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\leq x\leq 1,\quad 0\leq y\leq x^{3}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(42 x^{2} + 98 y\right)\,dA \\&=\int_{0}^{1}\int_{0}^{x^{3}}\left(42 x^{2} + 98 y\right)\,dy\,dx \\&=\int_{0}^{1}\left[42 x^{2} y + 49 y^{2}\right]_{y=0}^{y=x^{3}}\,dx \\&=\int_{0}^{1}\left(x^{5} \left(49 x + 42\right)\right)\,dx \\&=\left[7 x^{7} + 7 x^{6}\right]_{x=0}^{x=1} \\&=\left(14\right)-\left(0\right) \\&=14.\end{aligned}
$$

## q-127309

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨6y{x}^{2}+{e}^{y},\,3{y}^{2}⟩
$$

through the boundary of the region enclosed by the curve $y=\sqrt{x}$ and the lines $y=0$ and $x=2.$

Original complete bank: ['\\frac{45}{2}', '17', '22', '25', '\\frac{50}{3}']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 42 x^{2} y + 7 e^{y}, \; 21 y^{2} \right\rangle
$$

through the boundary of the region enclosed by the curve $y=\sqrt{x}$ and the lines $y=0$ and $x=2.$

Generated complete bank: ['\\frac{315}{2}', '119', '154', '175', '\\frac{350}{3}']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/f6/f6e80e3010ec7c40d3f59dbb1da4e77c985c889a720b6f954177d8ad83a01351.png)

We have that $P(x,y)=42 x^{2} y + 7 e^{y}$ and $Q(x,y)=21 y^{2}.$ Therefore,

$$
\frac{\partial P}{\partial x}=84 x y,\qquad \frac{\partial Q}{\partial y}=42 y.
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\leq x\leq 2,\quad 0\leq y\leq \sqrt{x}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(84 x y + 42 y\right)\,dA \\&=\int_{0}^{2}\int_{0}^{\sqrt{x}}\left(84 x y + 42 y\right)\,dy\,dx \\&=\int_{0}^{2}\left[y^{2} \left(42 x + 21\right)\right]_{y=0}^{y=\sqrt{x}}\,dx \\&=\int_{0}^{2}\left(21 x \left(2 x + 1\right)\right)\,dx \\&=\left[14 x^{3} + \frac{21 x^{2}}{2}\right]_{x=0}^{x=2} \\&=\left(154\right)-\left(0\right) \\&=154.\end{aligned}
$$

## q-127323

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨6{x}^{2}+2y,\,-10y-\operatorname{arctan}⁡x⟩
$$

through the boundary of the triangle with vertices $(0,0),(2,1),$ and $(-2,1).$

Original complete bank: ['10', '-25', '15', '-20', '-\\frac{15}{2}']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 42 x^{2} + 14 y, \; - 70 y - 7 \operatorname{atan}{\left(x \right)} \right\rangle
$$

through the boundary of the triangle with vertices $(0,0),(2,1),$ and $(-2,1).$

Generated complete bank: ['70', '-175', '105', '-140', '- \\frac{105}{2}']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/3a/3ad0a876fe801980a2c3724a639fc6c379db750635c0278a10a5094e2d64c34a.png)

We have that $P(x,y)=42 x^{2} + 14 y$ and $Q(x,y)=- 70 y - 7 \operatorname{atan}{\left(x \right)}.$ Therefore,

$$
\frac{\partial P}{\partial x}=84 x,\qquad \frac{\partial Q}{\partial y}=-70.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 1,\quad - 2 y\leq x\leq 2 y\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(84 x - 70\right)\,dA \\&=\int_{0}^{1}\int_{- 2 y}^{2 y}\left(84 x - 70\right)\,dx\,dy \\&=\int_{0}^{1}\left[42 x^{2} - 70 x\right]_{x=- 2 y}^{x=2 y}\,dy \\&=\int_{0}^{1}\left(- 280 y\right)\,dy \\&=\left[- 140 y^{2}\right]_{y=0}^{y=1} \\&=\left(-140\right)-\left(0\right) \\&=-140.\end{aligned}
$$

## q-127325

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨xy-\sqrt{{y}^{2}+1},\,{x}^{3}+y⟩
$$

through the boundary of the triangle with vertices $(0,0),(1,2),$ and $(-1,2).$

Original complete bank: ['-\\frac{11}{2}', '\\frac{14}{3}', '2', '-4', '\\frac{5}{3}']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 7 x y - 7 \sqrt{y^{2} + 1}, \; 7 x^{3} + 7 y \right\rangle
$$

through the boundary of the triangle with vertices $(0,0),(1,2),$ and $(-1,2).$

Generated complete bank: ['- \\frac{77}{2}', '\\frac{98}{3}', '14', '-28', '\\frac{35}{3}']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/00/006d80a7dbe4d03b78cc5fb1a642405e3fdfdd69ec9d80014ee8e0355ad1ae73.png)

We have that $P(x,y)=7 x y - 7 \sqrt{y^{2} + 1}$ and $Q(x,y)=7 x^{3} + 7 y.$ Therefore,

$$
\frac{\partial P}{\partial x}=7 y,\qquad \frac{\partial Q}{\partial y}=7.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 2,\quad - \frac{y}{2}\leq x\leq \frac{y}{2}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(7 y + 7\right)\,dA \\&=\int_{0}^{2}\int_{- \frac{y}{2}}^{\frac{y}{2}}\left(7 y + 7\right)\,dx\,dy \\&=\int_{0}^{2}\left[x \left(7 y + 7\right)\right]_{x=- \frac{y}{2}}^{x=\frac{y}{2}}\,dy \\&=\int_{0}^{2}\left(7 y \left(y + 1\right)\right)\,dy \\&=\left[\frac{7 y^{3}}{3} + \frac{7 y^{2}}{2}\right]_{y=0}^{y=2} \\&=\left(\frac{98}{3}\right)-\left(0\right) \\&=\frac{98}{3}.\end{aligned}
$$

## q-127328

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨{x}^{2}+y,\,xy+1⟩
$$

through the boundary of the region enclosed by the curves $x=-y,$ $\,x=\sqrt{y},$ and the line $y=1.$

Original complete bank: ['-4', '6', '8', '-\\frac{7}{3}', '\\frac{1}{4}']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 7 x^{2} + 7 y, \; 7 x y + 7 \right\rangle
$$

through the boundary of the region enclosed by the curves $x=-y,$ $\,x=\sqrt{y},$ and the line $y=1.$

Generated complete bank: ['-28', '42', '56', '- \\frac{49}{3}', '\\frac{7}{4}']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/2e/2ecabe22395006f0c7ef0a3f914087fa324f4d59c7d7886c18907f824744643e.png)

We have that $P(x,y)=7 x^{2} + 7 y$ and $Q(x,y)=7 x y + 7.$ Therefore,

$$
\frac{\partial P}{\partial x}=14 x,\qquad \frac{\partial Q}{\partial y}=7 x.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 1,\quad - y\leq x\leq \sqrt{y}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(21 x\right)\,dA \\&=\int_{0}^{1}\int_{- y}^{\sqrt{y}}\left(21 x\right)\,dx\,dy \\&=\int_{0}^{1}\left[\frac{21 x^{2}}{2}\right]_{x=- y}^{x=\sqrt{y}}\,dy \\&=\int_{0}^{1}\left(\frac{21 y \left(1 - y\right)}{2}\right)\,dy \\&=\left[- \frac{7 y^{3}}{2} + \frac{21 y^{2}}{4}\right]_{y=0}^{y=1} \\&=\left(\frac{7}{4}\right)-\left(0\right) \\&=\frac{7}{4}.\end{aligned}
$$

## q-127365

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨30xy,\,15{y}^{2}-\operatorname{sin}⁡x⟩
$$

through the boundary of the region enclosed by the curves $x=y,$ $\,x=-\sqrt{y},$ and the line $y=1.$

Original complete bank: ['-50', '44', '37', '-\\frac{55}{4}', '\\frac{35}{2}']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle 210 x y, \; 105 y^{2} - 7 \sin{\left(x \right)} \right\rangle
$$

through the boundary of the region enclosed by the curves $x=y,$ $\,x=-\sqrt{y},$ and the line $y=1.$

Generated complete bank: ['-350', '308', '259', '- \\frac{385}{4}', '\\frac{245}{2}']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/24/24369439bc62cf06084a43d97dff0cee4e4089fd103511ef73d9dd5af1256ebb.png)

We have that $P(x,y)=210 x y$ and $Q(x,y)=105 y^{2} - 7 \sin{\left(x \right)}.$ Therefore,

$$
\frac{\partial P}{\partial x}=210 y,\qquad \frac{\partial Q}{\partial y}=210 y.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 1,\quad - \sqrt{y}\leq x\leq y\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(420 y\right)\,dA \\&=\int_{0}^{1}\int_{- \sqrt{y}}^{y}\left(420 y\right)\,dx\,dy \\&=\int_{0}^{1}\left[420 x y\right]_{x=- \sqrt{y}}^{x=y}\,dy \\&=\int_{0}^{1}\left(420 y^{\frac{3}{2}} + 420 y^{2}\right)\,dy \\&=\left[168 y^{\frac{5}{2}} + 140 y^{3}\right]_{y=0}^{y=1} \\&=\left(308\right)-\left(0\right) \\&=308.\end{aligned}
$$

## q-127370

Original prompt:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=⟨-x,\,\operatorname{sin}⁡2{x}^{2}⟩
$$

through the boundary of the region enclosed by the curves $x=-y+1,$ $\,x={e}^{y},$ and the line $y=1.$

Original complete bank: ['5{e}^{2}', '5', '7', '\\frac{5}{2}+2e', '\\frac{3}{2}-e']

Scale 7 variant:

Use the flux form of Green's theorem to calculate the flux of the vector field

$$
F(x,y)=\left\langle - 7 x, \; 7 \sin{\left(2 x^{2} \right)} \right\rangle
$$

through the boundary of the region enclosed by the curves $x=-y+1,$ $\,x={e}^{y},$ and the line $y=1.$

Generated complete bank: ['35 e^{2}', '35', '49', '\\frac{35}{2} + 14 e', '\\frac{21}{2} - 7 e']

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $F=P\,i+Q\,j,$ and $P$ and $Q$ have continuous first derivatives on an open region containing $D,$ then the flux form of Green's theorem states that

$$
{∮}_{C}F\cdot n\,\text{d}s={∬}_{D}\text{div}\,F\,\text{d}A,
$$

which is equivalent to

$$
{∮}_{C}P\,dy-Q\,dx={∬}_{D}(\frac{∂P}{∂x}+\frac{∂Q}{∂y})\text{d}A.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/72/728036ffc90e2476017b3102b6279f9c5900f0e7fc58536e76c9aa038eb04f02.png)

We have that $P(x,y)=- 7 x$ and $Q(x,y)=7 \sin{\left(2 x^{2} \right)}.$ Therefore,

$$
\frac{\partial P}{\partial x}=-7,\qquad \frac{\partial Q}{\partial y}=0.
$$

We can express the region $D$ as a type II region as follows:

$$
D=\{(x,y):0\leq y\leq 1,\quad 1 - y\leq x\leq e^{y}\}.
$$

Therefore, applying Green's theorem in flux form, we get

$$
\begin{aligned}\oint_C \mathbf F\cdot\mathbf n\,ds&=\oint_C P\,dy-Q\,dx \\&=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,dA \\&=\iint_D\left(-7\right)\,dA \\&=\int_{0}^{1}\int_{1 - y}^{e^{y}}\left(-7\right)\,dx\,dy \\&=\int_{0}^{1}\left[- 7 x\right]_{x=1 - y}^{x=e^{y}}\,dy \\&=\int_{0}^{1}\left(- 7 y - 7 e^{y} + 7\right)\,dy \\&=\left[- \frac{7 y^{2}}{2} + 7 y - 7 e^{y}\right]_{y=0}^{y=1} \\&=\left(\frac{7}{2} - 7 e\right)-\left(-7\right) \\&=\frac{21}{2} - 7 e.\end{aligned}
$$
