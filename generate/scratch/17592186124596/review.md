# Originals and generated variants


All seven originals are captured at math basis 1356. Source-equivalent replays normalize notation; q-95172 has the documented first-chain-row correction. Generated examples are labeled, use a single fixed worked solution and complete five-option bank.


## z_mixed — easy


### Original 17592186125248


Given that $f(x,y,z)=xy+{y}^{2}z+x{z}^{2},$ find $\frac{∂f}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


${r}^{2}\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡\theta $
$r\operatorname{cos}⁡\theta +2rz\operatorname{sin}⁡\theta $
${r}^{2}{sin}^{2}⁡\theta +2rz\operatorname{cos}⁡\theta $
${r}^{2}\operatorname{sin}⁡(2\theta )+r{z}^{2}\operatorname{cos}⁡\theta $
$r\operatorname{sin}⁡\theta +{z}^{2}$


Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂f}{∂z} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂z}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂z}+\frac{∂f}{∂z}\cdot \frac{∂z}{∂z} \\  & =\frac{∂f}{∂z}.\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $z:$

$$
\begin{aligned}\frac{∂f}{∂z}={y}^{2}+2xz\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂f}{∂z} & ={r}^{2}{sin}^{2}⁡\theta +2rz\operatorname{cos}⁡\theta .\end{aligned}
$$


### Parameterized source replay


Given that $f(x,y,z)=x\cdot y+z\cdot y^{2}+x\cdot z^{2},$ find $\frac{∂f}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r^{2}\cdot \sin^{2}\theta+2\cdot r\cdot z\cdot \cos\theta$
2. $r\cdot \cos\theta+2\cdot r\cdot z\cdot \sin\theta$
3. $r^{2}\cdot \sin\theta+2\cdot r\cdot \cos\theta$
4. $z^{2}+r\cdot \sin\theta$
5. $r^{2}\cdot \sin(2\cdot \theta)+r\cdot z^{2}\cdot \cos\theta$

Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial f}{\partial z} & =\frac{\partial f}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial f}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial f}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial f}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $z:$

$$
\begin{aligned}\frac{\partial f}{\partial z}=y^{2}+2\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial f}{\partial z} & =r^{2}\cdot \sin^{2}\theta+2\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $u(x,y,z)=3\cdot x\cdot y-2\cdot z\cdot y^{2}-3\cdot x\cdot z^{2},$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-4\cdot r^{2}\cdot \sin^{2}\theta-12\cdot r\cdot z\cdot \cos\theta$
2. $-2\cdot r^{2}\cdot \sin^{2}\theta-6\cdot r\cdot z\cdot \cos\theta$
3. $-2\cdot \sin^{2}\theta-6\cdot z\cdot \cos\theta$
4. $-2\cdot r^{2}\cdot \cos^{2}\theta-6\cdot r\cdot z\cdot \sin\theta$
5. $2\cdot r^{2}\cdot \sin^{2}\theta+6\cdot r\cdot z\cdot \cos\theta$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-2\cdot y^{2}-6\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-2\cdot r^{2}\cdot \sin^{2}\theta-6\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $h(x,y,z)=2\cdot x\cdot y-5\cdot z\cdot y^{2}+4\cdot x\cdot z^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot \sin^{2}\theta+8\cdot z\cdot \cos\theta$
2. $-5\cdot r^{2}\cdot \sin^{2}\theta+8\cdot r\cdot z\cdot \cos\theta$
3. $-10\cdot r^{2}\cdot \sin^{2}\theta+16\cdot r\cdot z\cdot \cos\theta$
4. $-5\cdot r^{2}\cdot \cos^{2}\theta+8\cdot r\cdot z\cdot \sin\theta$
5. $5\cdot r^{2}\cdot \sin^{2}\theta-8\cdot r\cdot z\cdot \cos\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=-5\cdot y^{2}+8\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =-5\cdot r^{2}\cdot \sin^{2}\theta+8\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — observed


Given that $u(x,y,z)=3\cdot x\cdot y-2\cdot z\cdot y^{2}-3\cdot x\cdot z^{2},$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-3\cdot z^{2}+3\cdot r\cdot \sin\theta$
2. $-6\cdot r\cdot \cos\theta-2\cdot r^{2}\cdot \sin\theta$
3. $-2\cdot r^{2}\cdot \sin(2\cdot \theta)-3\cdot r\cdot z^{2}\cdot \cos\theta$
4. $-2\cdot r^{2}\cdot \sin^{2}\theta-6\cdot r\cdot z\cdot \cos\theta$
5. $3\cdot r\cdot \cos\theta-6\cdot r\cdot z\cdot \sin\theta$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-2\cdot y^{2}-6\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-2\cdot r^{2}\cdot \sin^{2}\theta-6\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — observed


Given that $h(x,y,z)=2\cdot x\cdot y-5\cdot z\cdot y^{2}+4\cdot x\cdot z^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot r^{2}\cdot \sin(2\cdot \theta)+4\cdot r\cdot z^{2}\cdot \cos\theta$
2. $-5\cdot r^{2}\cdot \sin\theta+8\cdot r\cdot \cos\theta$
3. $4\cdot z^{2}+2\cdot r\cdot \sin\theta$
4. $-5\cdot r^{2}\cdot \sin^{2}\theta+8\cdot r\cdot z\cdot \cos\theta$
5. $2\cdot r\cdot \cos\theta+8\cdot r\cdot z\cdot \sin\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=-5\cdot y^{2}+8\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =-5\cdot r^{2}\cdot \sin^{2}\theta+8\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


## z_square_cross — easy


### Original 17592186360581


Given that $u(x,y,z)={x}^{2}{z}^{2}+{x}^{2}{y}^{2}+xyz,$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


${r}^{2}(2z\operatorname{cos}⁡2\theta +\frac{1}{2}{sin}^{2}⁡\theta )$
$2{r}^{2}(z{cos}^{2}⁡\theta +\operatorname{sin}⁡2\theta )$
$2z{cos}^{2}⁡\theta +\frac{1}{2}\operatorname{sin}⁡2\theta $
$\operatorname{cos}⁡2\theta +{r}^{2}z\operatorname{sin}⁡2\theta $
${r}^{2}(2z{cos}^{2}⁡\theta +\frac{1}{2}\operatorname{sin}⁡2\theta )$


Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂u}{∂z} & =\frac{∂u}{∂x}\cdot \frac{∂x}{∂z}+\frac{∂u}{∂y}\cdot \frac{∂y}{∂z}+\frac{∂u}{∂z}\cdot \frac{∂z}{∂z} \\  & =\frac{∂u}{∂z}.\end{aligned}
$$

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{∂u}{∂z}=2{x}^{2}z+xy\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂u}{∂z} & =2{r}^{2}z{cos}^{2}⁡\theta +{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta  \\  & ={r}^{2}(2z{cos}^{2}⁡\theta +\frac{1}{2}\operatorname{sin}⁡2\theta ).\end{aligned}
$$


### Parameterized source replay


Given that $u(x,y,z)=x^{2}\cdot z^{2}+x^{2}\cdot y^{2}+x\cdot y\cdot z,$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $\frac{1}{2}\cdot \sin(2\cdot \theta)+2\cdot z\cdot \cos^{2}\theta$
2. $2\cdot r^{2}\cdot (z\cdot \cos^{2}\theta+\sin(2\cdot \theta))$
3. $r^{2}\cdot (\frac{1}{2}\cdot \sin^{2}\theta+2\cdot z\cdot \cos(2\cdot \theta))$
4. $r^{2}\cdot (2\cdot z\cdot \cos^{2}\theta+\frac{1}{2}\cdot \sin(2\cdot \theta))$
5. $z\cdot r^{2}\cdot \sin(2\cdot \theta)+\cos(2\cdot \theta)$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=x\cdot y+2\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =r^{2}\cdot \cos\theta\cdot \sin\theta+2\cdot z\cdot r^{2}\cdot \cos^{2}\theta \\  & =r^{2}\cdot (2\cdot z\cdot \cos^{2}\theta+\frac{1}{2}\cdot \sin(2\cdot \theta)).\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $u(x,y,z)=3\cdot x^{2}\cdot z^{2}-2\cdot x^{2}\cdot y^{2}-3\cdot x\cdot y\cdot z,$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $2\cdot r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta))$
2. $r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta))$
3. $-3\cdot \cos\theta\cdot \sin\theta+6\cdot z\cdot \cos^{2}\theta$
4. $-3\cdot r^{2}\cdot \cos\theta\cdot \sin\theta+6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $-r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta))$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-3\cdot x\cdot y+6\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-3\cdot r^{2}\cdot \cos\theta\cdot \sin\theta+6\cdot z\cdot r^{2}\cdot \cos^{2}\theta \\  & =r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta)).\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $h(x,y,z)=2\cdot x^{2}\cdot z^{2}-5\cdot x^{2}\cdot y^{2}+4\cdot x\cdot y\cdot z,$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $4\cdot z\cdot \cos^{2}\theta+4\cdot \cos\theta\cdot \sin\theta$
2. $r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta))$
3. $2\cdot r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta))$
4. $4\cdot z\cdot r^{2}\cdot \sin^{2}\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta$
5. $-r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta))$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=4\cdot x\cdot y+4\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =4\cdot z\cdot r^{2}\cdot \cos^{2}\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta)).\end{aligned}
$$


### Generated variant 1 — observed


Given that $u(x,y,z)=3\cdot x^{2}\cdot z^{2}-2\cdot x^{2}\cdot y^{2}-3\cdot x\cdot y\cdot z,$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta))$
2. $r^{2}\cdot (-\frac{3}{2}\cdot \sin^{2}\theta+6\cdot z\cdot \cos(2\cdot \theta))$
3. $3\cdot \cos(2\cdot \theta)-3\cdot z\cdot r^{2}\cdot \sin(2\cdot \theta)$
4. $-\frac{3}{2}\cdot \sin(2\cdot \theta)+6\cdot z\cdot \cos^{2}\theta$
5. $2\cdot r^{2}\cdot (-3\cdot \sin(2\cdot \theta)+3\cdot z\cdot \cos^{2}\theta)$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-3\cdot x\cdot y+6\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-3\cdot r^{2}\cdot \cos\theta\cdot \sin\theta+6\cdot z\cdot r^{2}\cdot \cos^{2}\theta \\  & =r^{2}\cdot (6\cdot z\cdot \cos^{2}\theta-\frac{3}{2}\cdot \sin(2\cdot \theta)).\end{aligned}
$$


### Generated variant 2 — observed


Given that $h(x,y,z)=2\cdot x^{2}\cdot z^{2}-5\cdot x^{2}\cdot y^{2}+4\cdot x\cdot y\cdot z,$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $2\cdot \cos(2\cdot \theta)+4\cdot z\cdot r^{2}\cdot \sin(2\cdot \theta)$
2. $r^{2}\cdot (2\cdot \sin^{2}\theta+4\cdot z\cdot \cos(2\cdot \theta))$
3. $r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta))$
4. $2\cdot \sin(2\cdot \theta)+4\cdot z\cdot \cos^{2}\theta$
5. $2\cdot r^{2}\cdot (4\cdot \sin(2\cdot \theta)+2\cdot z\cdot \cos^{2}\theta)$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=4\cdot x\cdot y+4\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =4\cdot z\cdot r^{2}\cdot \cos^{2}\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =r^{2}\cdot (4\cdot z\cdot \cos^{2}\theta+2\cdot \sin(2\cdot \theta)).\end{aligned}
$$


## z_single — easy


### Original 17592186360583


Given that $h(x,y,z)=2{x}^{2}+{y}^{2}+4{x}^{2}{z}^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


$8z$
$8z+{r}^{2}{cos}^{2}⁡\theta $
$8{r}^{2}z{cos}^{2}⁡\theta $
$8z+{r}^{2}{sin}^{2}⁡\theta $
$8{r}^{2}z{sin}^{2}⁡\theta $


Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂h}{∂z} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂z}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂z}+\frac{∂h}{∂z}\cdot \frac{∂z}{∂z} \\  & =\frac{∂h}{∂z}.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{∂h}{∂z}=8{x}^{2}z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂h}{∂z} & =8{r}^{2}z{cos}^{2}⁡\theta .\end{aligned}
$$


### Parameterized source replay


Given that $h(x,y,z)=2\cdot x^{2}+y^{2}+4\cdot x^{2}\cdot z^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $8\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
2. $8\cdot z+r^{2}\cdot \cos^{2}\theta$
3. $8\cdot z$
4. $8\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $8\cdot z+r^{2}\cdot \sin^{2}\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=8\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =8\cdot z\cdot r^{2}\cdot \cos^{2}\theta.\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $u(x,y,z)=3\cdot x^{2}-2\cdot y^{2}-3\cdot x^{2}\cdot z^{2},$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-12\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
2. $-6\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
3. $-6\cdot z\cdot \cos^{2}\theta$
4. $-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $6\cdot z\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-6\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-6\cdot z\cdot r^{2}\cdot \cos^{2}\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $h(x,y,z)=2\cdot x^{2}-5\cdot y^{2}+4\cdot x^{2}\cdot z^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $8\cdot z\cdot \cos^{2}\theta$
2. $8\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
3. $16\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
4. $8\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $-8\cdot z\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=8\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =8\cdot z\cdot r^{2}\cdot \cos^{2}\theta.\end{aligned}
$$


### Generated variant 1 — observed


Given that $u(x,y,z)=3\cdot x^{2}-2\cdot y^{2}-3\cdot x^{2}\cdot z^{2},$ find $\frac{∂u}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
2. $-6\cdot z$
3. $-6\cdot z-2\cdot r^{2}\cdot \sin^{2}\theta$
4. $-6\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
5. $-6\cdot z-2\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $u(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial u}{\partial z} & =\frac{\partial u}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial u}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial u}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial u}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $u$ with respect to $z:$

$$
\begin{aligned}\frac{\partial u}{\partial z}=-6\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial u}{\partial z} & =-6\cdot z\cdot r^{2}\cdot \cos^{2}\theta.\end{aligned}
$$


### Generated variant 2 — observed


Given that $h(x,y,z)=2\cdot x^{2}-5\cdot y^{2}+4\cdot x^{2}\cdot z^{2},$ find $\frac{∂h}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $8\cdot z-5\cdot r^{2}\cdot \sin^{2}\theta$
2. $8\cdot z$
3. $8\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
4. $8\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
5. $8\cdot z-5\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial z} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial h}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $z:$

$$
\begin{aligned}\frac{\partial h}{\partial z}=8\cdot z\cdot x^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial z} & =8\cdot z\cdot r^{2}\cdot \cos^{2}\theta.\end{aligned}
$$


## z_square_linear — easy


### Original 17592186367921


Given that $f(x,y,z)={y}^{2}{z}^{2}+xz,$ find $\frac{∂f}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


$r({sin}^{2}⁡\theta +\operatorname{cos}⁡\theta )$
$2{r}^{2}z{sin}^{2}⁡\theta +r\operatorname{cos}⁡\theta $
$2z+{r}^{2}{cos}^{2}⁡\theta $
$2{r}^{2}z{cos}^{2}⁡\theta +\operatorname{sin}⁡\theta $
${r}^{2}\operatorname{cos}⁡\theta +{sin}^{2}⁡\theta $


Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂f}{∂z} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂z}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂z}+\frac{∂f}{∂z}\cdot \frac{∂z}{∂z} \\  & =\frac{∂f}{∂z}.\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $z:$

$$
\begin{aligned}\frac{∂f}{∂z}=2{y}^{2}z+x\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂f}{∂z} & =2{r}^{2}z{sin}^{2}⁡\theta +r\operatorname{cos}⁡\theta .\end{aligned}
$$


### Parameterized source replay


Given that $f(x,y,z)=y^{2}\cdot z^{2}+x\cdot z,$ find $\frac{∂f}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $2\cdot z+r^{2}\cdot \cos^{2}\theta$
2. $r\cdot \cos\theta+2\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
3. $r\cdot (\sin^{2}\theta+\cos\theta)$
4. $\sin^{2}\theta+r^{2}\cdot \cos\theta$
5. $2\cdot z\cdot r^{2}\cdot \cos^{2}\theta+\sin\theta$

Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial f}{\partial z} & =\frac{\partial f}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial f}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial f}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial f}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $z:$

$$
\begin{aligned}\frac{\partial f}{\partial z}=x+2\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial f}{\partial z} & =r\cdot \cos\theta+2\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $g(x,y,z)=3\cdot y^{2}\cdot z^{2}-2\cdot x\cdot z,$ find $\frac{∂g}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-2\cdot r\cdot \cos\theta+6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
2. $-4\cdot r\cdot \cos\theta+12\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
3. $-2\cdot r\cdot \sin\theta+6\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
4. $2\cdot r\cdot \cos\theta-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $-2\cdot \cos\theta+6\cdot z\cdot \sin^{2}\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial z} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial g}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $g$ with respect to $z:$

$$
\begin{aligned}\frac{\partial g}{\partial z}=-2\cdot x+6\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial z} & =-2\cdot r\cdot \cos\theta+6\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $v(x,y,z)=2\cdot y^{2}\cdot z^{2}-5\cdot x\cdot z,$ find $\frac{∂v}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot r\cdot \cos\theta+4\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
2. $-10\cdot r\cdot \cos\theta+8\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
3. $-5\cdot \cos\theta+4\cdot z\cdot \sin^{2}\theta$
4. $5\cdot r\cdot \cos\theta-4\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $-5\cdot r\cdot \sin\theta+4\cdot z\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial z} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial v}{\partial z}.\end{aligned}
$$

The derivative requested holds $r$ and $\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\cos\theta$ and $y=r\sin\theta$.

First, we find the partial derivatives of $v$ with respect to $z:$

$$
\begin{aligned}\frac{\partial v}{\partial z}=-5\cdot x+4\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial z} & =-5\cdot r\cdot \cos\theta+4\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$


### Generated variant 1 — observed


Given that $g(x,y,z)=3\cdot y^{2}\cdot z^{2}-2\cdot x\cdot z,$ find $\frac{∂g}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r\cdot (-2\cdot \cos\theta+3\cdot \sin^{2}\theta)$
2. $3\cdot \sin^{2}\theta-2\cdot r^{2}\cdot \cos\theta$
3. $6\cdot z-2\cdot r^{2}\cdot \cos^{2}\theta$
4. $-2\cdot r\cdot \cos\theta+6\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $-2\cdot \sin\theta+6\cdot z\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial z} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial g}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $z:$

$$
\begin{aligned}\frac{\partial g}{\partial z}=-2\cdot x+6\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial z} & =-2\cdot r\cdot \cos\theta+6\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$


### Generated variant 2 — observed


Given that $v(x,y,z)=2\cdot y^{2}\cdot z^{2}-5\cdot x\cdot z,$ find $\frac{∂v}{∂z},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r\cdot (-5\cdot \cos\theta+2\cdot \sin^{2}\theta)$
2. $2\cdot \sin^{2}\theta-5\cdot r^{2}\cdot \cos\theta$
3. $-5\cdot \sin\theta+4\cdot z\cdot r^{2}\cdot \cos^{2}\theta$
4. $-5\cdot r\cdot \cos\theta+4\cdot z\cdot r^{2}\cdot \sin^{2}\theta$
5. $4\cdot z-5\cdot r^{2}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial z} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial z}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial z}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial z} \\  & =\frac{\partial v}{\partial z}.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $z:$

$$
\begin{aligned}\frac{\partial v}{\partial z}=-5\cdot x+4\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial z} & =-5\cdot r\cdot \cos\theta+4\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$


## theta_cancellation — moderate


### Original 17592186125243


Given that $f(x,y,z)={x}^{2}+{y}^{2}+2yz,$ find $\frac{∂f}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


$2rz{sin}^{2}⁡\theta $
${r}^{2}\operatorname{sin}⁡2\theta -r\operatorname{cos}⁡\theta $
$2rz\operatorname{cos}⁡\theta +{r}^{2}\operatorname{sin}⁡\theta $
${r}^{2}\operatorname{sin}⁡\theta $
$2rz\operatorname{cos}⁡\theta $


Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta } & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta }+\frac{∂f}{∂z}\cdot \frac{∂z}{∂\theta } \\  & =-\frac{∂f}{∂x}r\operatorname{sin}⁡\theta +\frac{∂f}{∂y}r\operatorname{cos}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=2x,\,\frac{∂f}{∂y}=2y+2z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2r\operatorname{cos}⁡\theta , \\ \frac{∂f}{∂y} & =2r\operatorname{sin}⁡\theta +2z.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta } & =-(2r\operatorname{cos}⁡\theta )r\operatorname{sin}⁡\theta +(2r\operatorname{sin}⁡\theta +2z)r\operatorname{cos}⁡\theta  \\  & =-2{r}^{2}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta +2{r}^{2}\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta +2rz\operatorname{cos}⁡\theta  \\  & =2rz\operatorname{cos}⁡\theta .\end{aligned}
$$


### Parameterized source replay


Given that $f(x,y,z)=x^{2}+y^{2}+2\cdot y\cdot z,$ find $\frac{∂f}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r^{2}\cdot \sin\theta+2\cdot r\cdot z\cdot \cos\theta$
2. $r^{2}\cdot \sin(2\cdot \theta)-r\cdot \cos\theta$
3. $2\cdot r\cdot z\cdot \sin^{2}\theta$
4. $2\cdot r\cdot z\cdot \cos\theta$
5. $r^{2}\cdot \sin\theta$

Applying the multivariable chain rule for the function $f(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial f}{\partial \theta} & =\frac{\partial f}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial f}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial f}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial f}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial f}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial f}{\partial x}=2\cdot x,\,\frac{\partial f}{\partial y}=2\cdot y+2\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial f}{\partial x} & =2\cdot r\cdot \cos\theta, \\ \frac{\partial f}{\partial y} & =2\cdot z+2\cdot r\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial f}{\partial \theta} & =-(2\cdot r\cdot \cos\theta)\cdot r\cdot \sin\theta+(2\cdot z+2\cdot r\cdot \sin\theta)\cdot r\cdot \cos\theta \\  & =-2\cdot r^{2}\cdot \cos\theta\cdot \sin\theta+2\cdot r\cdot z\cdot \cos\theta+2\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =2\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $g(x,y,z)=3\cdot x^{2}+3\cdot y^{2}-2\cdot y\cdot z,$ find $\frac{∂g}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-2\cdot r\cdot z\cdot \cos\theta$
2. $-2\cdot z+6\cdot r\cdot \cos\theta+6\cdot r\cdot \sin\theta$
3. $-6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta$
4. $r\cdot (-2\cdot z+6\cdot r\cdot \sin\theta)\cdot \cos\theta+6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta$
5. $r\cdot (-2\cdot z+6\cdot r\cdot \sin\theta)\cdot \cos\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial g}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial g}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=6\cdot x,\,\frac{\partial g}{\partial y}=-2\cdot z+6\cdot y\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =6\cdot r\cdot \cos\theta, \\ \frac{\partial g}{\partial y} & =-2\cdot z+6\cdot r\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =-(6\cdot r\cdot \cos\theta)\cdot r\cdot \sin\theta+(-2\cdot z+6\cdot r\cdot \sin\theta)\cdot r\cdot \cos\theta \\  & =-6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta+6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =-2\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $v(x,y,z)=2\cdot x^{2}+2\cdot y^{2}-5\cdot y\cdot z,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot r\cdot z\cdot \cos\theta$
2. $-5\cdot z+4\cdot r\cdot \cos\theta+4\cdot r\cdot \sin\theta$
3. $r\cdot (-5\cdot z+4\cdot r\cdot \sin\theta)\cdot \cos\theta$
4. $r\cdot (-5\cdot z+4\cdot r\cdot \sin\theta)\cdot \cos\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta$
5. $-4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial v}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial v}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial v}{\partial x}=4\cdot x,\,\frac{\partial v}{\partial y}=-5\cdot z+4\cdot y\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial x} & =4\cdot r\cdot \cos\theta, \\ \frac{\partial v}{\partial y} & =-5\cdot z+4\cdot r\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =-(4\cdot r\cdot \cos\theta)\cdot r\cdot \sin\theta+(-5\cdot z+4\cdot r\cdot \sin\theta)\cdot r\cdot \cos\theta \\  & =-4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta-5\cdot r\cdot z\cdot \cos\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =-5\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — observed


Given that $g(x,y,z)=3\cdot x^{2}+3\cdot y^{2}-2\cdot y\cdot z,$ find $\frac{∂g}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-2\cdot r\cdot z\cdot \sin^{2}\theta$
2. $-2\cdot r\cdot z\cdot \cos\theta$
3. $3\cdot r^{2}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta$
4. $-3\cdot r\cdot \cos\theta+3\cdot r^{2}\cdot \sin(2\cdot \theta)$
5. $3\cdot r^{2}\cdot \sin\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial g}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial g}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=6\cdot x,\,\frac{\partial g}{\partial y}=-2\cdot z+6\cdot y\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =6\cdot r\cdot \cos\theta, \\ \frac{\partial g}{\partial y} & =-2\cdot z+6\cdot r\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =-(6\cdot r\cdot \cos\theta)\cdot r\cdot \sin\theta+(-2\cdot z+6\cdot r\cdot \sin\theta)\cdot r\cdot \cos\theta \\  & =-6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta+6\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =-2\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — observed


Given that $v(x,y,z)=2\cdot x^{2}+2\cdot y^{2}-5\cdot y\cdot z,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot r\cdot z\cdot \sin^{2}\theta$
2. $-5\cdot r\cdot z\cdot \cos\theta$
3. $2\cdot r^{2}\cdot \sin\theta$
4. $-2\cdot r\cdot \cos\theta+2\cdot r^{2}\cdot \sin(2\cdot \theta)$
5. $2\cdot r^{2}\cdot \sin\theta-5\cdot r\cdot z\cdot \cos\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial v}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial v}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial v}{\partial x}=4\cdot x,\,\frac{\partial v}{\partial y}=-5\cdot z+4\cdot y\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial x} & =4\cdot r\cdot \cos\theta, \\ \frac{\partial v}{\partial y} & =-5\cdot z+4\cdot r\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =-(4\cdot r\cdot \cos\theta)\cdot r\cdot \sin\theta+(-5\cdot z+4\cdot r\cdot \sin\theta)\cdot r\cdot \cos\theta \\  & =-4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta-5\cdot r\cdot z\cdot \cos\theta+4\cdot r^{2}\cdot \cos\theta\cdot \sin\theta \\  & =-5\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$


## theta_linear — moderate


### Original 17592186360582


Given that $v(x,y,z)=2y-xz,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


$2r\operatorname{sin}⁡\theta +z\operatorname{cos}⁡\theta $
$z\operatorname{cos}⁡2\theta +2r{sin}^{2}⁡\theta $
$rz\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡\theta $
$z{cos}^{2}⁡\theta +2r\operatorname{sin}⁡2\theta $
$z{sin}^{2}⁡\theta +2r{cos}^{2}⁡\theta $


Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂v}{∂\theta } & =\frac{∂v}{∂x}\cdot \frac{∂x}{∂\theta }+\frac{∂v}{∂y}\cdot \frac{∂v}{∂\theta }+\frac{∂v}{∂z}\cdot \frac{∂z}{∂\theta } \\  & =-\frac{∂v}{∂x}r\operatorname{sin}⁡\theta +\frac{∂v}{∂y}r\operatorname{cos}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂v}{∂x}=-z,\,\frac{∂v}{∂y}=2\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂v}{∂x} & =-z, \\ \frac{∂v}{∂y} & =2.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂v}{∂\theta } & =-(-z)r\operatorname{sin}⁡\theta +(2)r\operatorname{cos}⁡\theta  \\  & =rz\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡\theta .\end{aligned}
$$


### Parameterized source replay


Given that $v(x,y,z)=2\cdot y-x\cdot z,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta$
2. $z\cdot \cos(2\cdot \theta)+2\cdot r\cdot \sin^{2}\theta$
3. $z\cdot \cos\theta+2\cdot r\cdot \sin\theta$
4. $z\cdot \sin^{2}\theta+2\cdot r\cdot \cos^{2}\theta$
5. $z\cdot \cos^{2}\theta+2\cdot r\cdot \sin(2\cdot \theta)$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial v}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial v}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial v}{\partial x}=-z,\,\frac{\partial v}{\partial y}=2\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial x} & =-z, \\ \frac{\partial v}{\partial y} & =2.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =-(-z)\cdot r\cdot \sin\theta+(2)\cdot r\cdot \cos\theta \\  & =r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $g(x,y,z)=3\cdot y+2\cdot x\cdot z,$ find $\frac{∂g}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-2\cdot r\cdot z\cdot \sin\theta+3\cdot r\cdot \cos\theta$
2. $3+2\cdot z$
3. $-2\cdot r\cdot z\cdot \sin\theta$
4. $3\cdot r\cdot \cos\theta+2\cdot r\cdot z\cdot \sin\theta$
5. $3\cdot r\cdot \cos\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial g}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial g}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=2\cdot z,\,\frac{\partial g}{\partial y}=3\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =2\cdot z, \\ \frac{\partial g}{\partial y} & =3.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =-(2\cdot z)\cdot r\cdot \sin\theta+(3)\cdot r\cdot \cos\theta \\  & =-2\cdot r\cdot z\cdot \sin\theta+3\cdot r\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $v(x,y,z)=2\cdot y+5\cdot x\cdot z,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta$
2. $2+5\cdot z$
3. $2\cdot r\cdot \cos\theta$
4. $2\cdot r\cdot \cos\theta+5\cdot r\cdot z\cdot \sin\theta$
5. $-5\cdot r\cdot z\cdot \sin\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial v}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial v}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial v}{\partial x}=5\cdot z,\,\frac{\partial v}{\partial y}=2\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial x} & =5\cdot z, \\ \frac{\partial v}{\partial y} & =2.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =-(5\cdot z)\cdot r\cdot \sin\theta+(2)\cdot r\cdot \cos\theta \\  & =-5\cdot r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta.\end{aligned}
$$


### Generated variant 1 — observed


Given that $g(x,y,z)=3\cdot y+2\cdot x\cdot z,$ find $\frac{∂g}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-2\cdot z\cdot \cos\theta+3\cdot r\cdot \sin\theta$
2. $-2\cdot z\cdot \sin^{2}\theta+3\cdot r\cdot \cos^{2}\theta$
3. $-2\cdot r\cdot z\cdot \sin\theta+3\cdot r\cdot \cos\theta$
4. $-2\cdot z\cdot \cos(2\cdot \theta)+3\cdot r\cdot \sin^{2}\theta$
5. $-2\cdot z\cdot \cos^{2}\theta+3\cdot r\cdot \sin(2\cdot \theta)$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial g}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial g}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=2\cdot z,\,\frac{\partial g}{\partial y}=3\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =2\cdot z, \\ \frac{\partial g}{\partial y} & =3.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =-(2\cdot z)\cdot r\cdot \sin\theta+(3)\cdot r\cdot \cos\theta \\  & =-2\cdot r\cdot z\cdot \sin\theta+3\cdot r\cdot \cos\theta.\end{aligned}
$$


### Generated variant 2 — observed


Given that $v(x,y,z)=2\cdot y+5\cdot x\cdot z,$ find $\frac{∂v}{∂\theta },$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-5\cdot z\cdot \cos\theta+2\cdot r\cdot \sin\theta$
2. $-5\cdot z\cdot \sin^{2}\theta+2\cdot r\cdot \cos^{2}\theta$
3. $-5\cdot z\cdot \cos^{2}\theta+2\cdot r\cdot \sin(2\cdot \theta)$
4. $-5\cdot z\cdot \cos(2\cdot \theta)+2\cdot r\cdot \sin^{2}\theta$
5. $-5\cdot r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta$

Applying the multivariable chain rule for the function $v(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =\frac{\partial v}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial v}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial v}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial v}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial v}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $v$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial v}{\partial x}=5\cdot z,\,\frac{\partial v}{\partial y}=2\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial v}{\partial x} & =5\cdot z, \\ \frac{\partial v}{\partial y} & =2.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial v}{\partial \theta} & =-(5\cdot z)\cdot r\cdot \sin\theta+(2)\cdot r\cdot \cos\theta \\  & =-5\cdot r\cdot z\cdot \sin\theta+2\cdot r\cdot \cos\theta.\end{aligned}
$$


## r_cubic — moderate


### Original 17592186368892


Given that $g(x,y,z)={x}^{3}{z}^{4}+{y}^{3}{z}^{2},$ find $\frac{∂g}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.


$3{r}^{2}({z}^{2}{cos}^{2}⁡\theta +{sin}^{2}⁡\theta )$
$3{r}^{2}{z}^{2}(\operatorname{cos}⁡3\theta +\operatorname{sin}⁡3\theta )$
${z}^{2}{cos}^{3}⁡\theta +{sin}^{3}⁡\theta $
${r}^{2}z({z}^{3}{cos}^{3}⁡\theta +z{sin}^{3}⁡\theta )$
$3{r}^{2}{z}^{2}({z}^{2}{cos}^{3}⁡\theta +{sin}^{3}⁡\theta )$


Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{∂g}{∂r} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂r}+\frac{∂g}{∂z}\cdot \frac{∂z}{∂r} \\  & =\frac{∂g}{∂x}\operatorname{cos}⁡\theta +\frac{∂g}{∂y}\operatorname{sin}⁡\theta .\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=3{x}^{2}{z}^{4},\,\frac{∂g}{∂y}=3{y}^{2}{z}^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =3{r}^{2}{z}^{4}{cos}^{2}⁡\theta , \\ \frac{∂g}{∂y} & =3{r}^{2}{z}^{2}{sin}^{2}⁡\theta .\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂r} & =(3{r}^{2}{z}^{4}{cos}^{2}⁡\theta )\operatorname{cos}⁡\theta +(3{r}^{2}{z}^{2}{sin}^{2}⁡\theta )\operatorname{sin}⁡\theta  \\  & =3{r}^{2}{z}^{2}({z}^{2}{cos}^{3}⁡\theta +{sin}^{3}⁡\theta ).\end{aligned}
$$


### Parameterized source replay


Given that $g(x,y,z)=x^{3}\cdot z^{4}+y^{3}\cdot z^{2},$ find $\frac{∂g}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $\sin^{3}\theta+z^{2}\cdot \cos^{3}\theta$
2. $3\cdot r^{2}\cdot z^{2}\cdot (\cos(3\cdot \theta)+\sin(3\cdot \theta))$
3. $3\cdot r^{2}\cdot (\sin^{2}\theta+z^{2}\cdot \cos^{2}\theta)$
4. $3\cdot r^{2}\cdot z^{2}\cdot (z^{2}\cdot \cos^{3}\theta+\sin^{3}\theta)$
5. $z\cdot r^{2}\cdot (z\cdot \sin^{3}\theta+z^{3}\cdot \cos^{3}\theta)$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial r} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial g}{\partial x}\cdot \cos\theta+\frac{\partial g}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=3\cdot x^{2}\cdot z^{4},\,\frac{\partial g}{\partial y}=3\cdot y^{2}\cdot z^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =3\cdot r^{2}\cdot z^{4}\cdot \cos^{2}\theta, \\ \frac{\partial g}{\partial y} & =3\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial r} & =(3\cdot r^{2}\cdot z^{4}\cdot \cos^{2}\theta)\cdot \cos\theta+(3\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta)\cdot \sin\theta \\  & =3\cdot r^{2}\cdot z^{2}\cdot (z^{2}\cdot \cos^{3}\theta+\sin^{3}\theta).\end{aligned}
$$


### Generated variant 1 — authored_operations


Given that $w(x,y,z)=3\cdot x^{3}\cdot z^{3}-2\cdot z\cdot y^{3},$ find $\frac{∂w}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-9\cdot r^{2}\cdot z^{3}\cdot \cos^{3}\theta-6\cdot z\cdot r^{2}\cdot \sin^{3}\theta$
2. $3\cdot z\cdot r^{2}\cdot (3\cdot z^{2}\cdot \cos^{3}\theta-2\cdot \sin^{3}\theta)$
3. $-6\cdot z\cdot r^{2}\cdot \sin^{3}\theta$
4. $9\cdot r^{2}\cdot z^{3}\cdot \cos^{3}\theta$
5. $-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta+9\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta$

Applying the multivariable chain rule for the function $w(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial w}{\partial r} & =\frac{\partial w}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial w}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial w}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial w}{\partial x}\cdot \cos\theta+\frac{\partial w}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial w}{\partial x}=9\cdot x^{2}\cdot z^{3},\,\frac{\partial w}{\partial y}=-6\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial w}{\partial x} & =9\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta, \\ \frac{\partial w}{\partial y} & =-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial w}{\partial r} & =(9\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta)\cdot \cos\theta+(-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta)\cdot \sin\theta \\  & =3\cdot z\cdot r^{2}\cdot (3\cdot z^{2}\cdot \cos^{3}\theta-2\cdot \sin^{3}\theta).\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $g(x,y,z)=2\cdot x^{3}\cdot z^{3}-5\cdot y^{3}\cdot z^{2},$ find $\frac{∂g}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $-15\cdot r^{2}\cdot z^{2}\cdot \sin^{3}\theta$
2. $3\cdot r^{2}\cdot z^{2}\cdot (2\cdot z\cdot \cos^{3}\theta-5\cdot \sin^{3}\theta)$
3. $-15\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta+6\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta$
4. $-15\cdot r^{2}\cdot z^{2}\cdot \sin^{3}\theta-6\cdot r^{2}\cdot z^{3}\cdot \cos^{3}\theta$
5. $6\cdot r^{2}\cdot z^{3}\cdot \cos^{3}\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial r} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial g}{\partial x}\cdot \cos\theta+\frac{\partial g}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=6\cdot x^{2}\cdot z^{3},\,\frac{\partial g}{\partial y}=-15\cdot y^{2}\cdot z^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =6\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta, \\ \frac{\partial g}{\partial y} & =-15\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial r} & =(6\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta)\cdot \cos\theta+(-15\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta)\cdot \sin\theta \\  & =3\cdot r^{2}\cdot z^{2}\cdot (2\cdot z\cdot \cos^{3}\theta-5\cdot \sin^{3}\theta).\end{aligned}
$$


### Generated variant 1 — observed


Given that $w(x,y,z)=3\cdot x^{3}\cdot z^{3}-2\cdot z\cdot y^{3},$ find $\frac{∂w}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $3\cdot z\cdot r^{2}\cdot (-2\cdot \sin(3\cdot \theta)+3\cdot \cos(3\cdot \theta))$
2. $3\cdot r^{2}\cdot (-2\cdot \sin^{2}\theta+3\cdot z^{2}\cdot \cos^{2}\theta)$
3. $z\cdot r^{2}\cdot (-2\cdot \sin^{3}\theta+3\cdot z^{2}\cdot \cos^{3}\theta)$
4. $-2\cdot \sin^{3}\theta+3\cdot z^{2}\cdot \cos^{3}\theta$
5. $3\cdot z\cdot r^{2}\cdot (3\cdot z^{2}\cdot \cos^{3}\theta-2\cdot \sin^{3}\theta)$

Applying the multivariable chain rule for the function $w(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial w}{\partial r} & =\frac{\partial w}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial w}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial w}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial w}{\partial x}\cdot \cos\theta+\frac{\partial w}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial w}{\partial x}=9\cdot x^{2}\cdot z^{3},\,\frac{\partial w}{\partial y}=-6\cdot z\cdot y^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial w}{\partial x} & =9\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta, \\ \frac{\partial w}{\partial y} & =-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial w}{\partial r} & =(9\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta)\cdot \cos\theta+(-6\cdot z\cdot r^{2}\cdot \sin^{2}\theta)\cdot \sin\theta \\  & =3\cdot z\cdot r^{2}\cdot (3\cdot z^{2}\cdot \cos^{3}\theta-2\cdot \sin^{3}\theta).\end{aligned}
$$


### Generated variant 2 — observed


Given that $g(x,y,z)=2\cdot x^{3}\cdot z^{3}-5\cdot y^{3}\cdot z^{2},$ find $\frac{∂g}{∂r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta ,z)$ are the corresponding cylindrical polar coordinates.

1. $z\cdot r^{2}\cdot (-5\cdot z\cdot \sin^{3}\theta+2\cdot z^{2}\cdot \cos^{3}\theta)$
2. $3\cdot r^{2}\cdot (-5\cdot \sin^{2}\theta+2\cdot z\cdot \cos^{2}\theta)$
3. $3\cdot r^{2}\cdot z^{2}\cdot (2\cdot z\cdot \cos^{3}\theta-5\cdot \sin^{3}\theta)$
4. $3\cdot r^{2}\cdot z^{2}\cdot (-5\cdot \sin(3\cdot \theta)+2\cdot \cos(3\cdot \theta))$
5. $-5\cdot \sin^{3}\theta+2\cdot z\cdot \cos^{3}\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta ,$ and $z,$ where $x=r\operatorname{cos}⁡\theta ,y=r\operatorname{sin}⁡\theta ,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial r} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial g}{\partial x}\cdot \cos\theta+\frac{\partial g}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=6\cdot x^{2}\cdot z^{3},\,\frac{\partial g}{\partial y}=-15\cdot y^{2}\cdot z^{2}\end{aligned}
$$

Writing the above results in terms of $r,\theta ,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =6\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta, \\ \frac{\partial g}{\partial y} & =-15\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial r} & =(6\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta)\cdot \cos\theta+(-15\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta)\cdot \sin\theta \\  & =3\cdot r^{2}\cdot z^{2}\cdot (2\cdot z\cdot \cos^{3}\theta-5\cdot \sin^{3}\theta).\end{aligned}
$$


## theta_coupled — authored hard


### Generated variant 1 — authored_operations


Given that $w(x,y,z)=z^{2}\cdot (3\cdot x^{2}-2\cdot x\cdot y-3\cdot y^{2}),$ find $\frac{\partial w}{\partial \theta},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta,z)$ are the corresponding cylindrical polar coordinates.

1. $r\cdot z^{2}\cdot (-6\cdot r\cdot \sin\theta-2\cdot r\cdot \cos\theta)\cdot \cos\theta+r\cdot z^{2}\cdot (-2\cdot r\cdot \sin\theta+6\cdot r\cdot \cos\theta)\cdot \sin\theta$
2. $r^{2}\cdot z^{2}\cdot (-6\cdot \sin(2\cdot \theta)-2\cdot \cos(2\cdot \theta))$
3. $r\cdot z^{2}\cdot (-6\cdot r\cdot \sin\theta-2\cdot r\cdot \cos\theta)\cdot \cos\theta$
4. $-r\cdot z^{2}\cdot (-2\cdot r\cdot \sin\theta+6\cdot r\cdot \cos\theta)\cdot \sin\theta$
5. $z^{2}\cdot (-6\cdot r\cdot \sin\theta-2\cdot r\cdot \cos\theta)+z^{2}\cdot (-2\cdot r\cdot \sin\theta+6\cdot r\cdot \cos\theta)$

Applying the multivariable chain rule for the function $w(x,y,z)$ with three independent variables $r,\theta,$ and $z,$ where $x=r\cos\theta,y=r\sin\theta,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial w}{\partial \theta} & =\frac{\partial w}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial w}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial w}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial w}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial w}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial w}{\partial x}=z^{2}\cdot (-2\cdot y+6\cdot x),\,\frac{\partial w}{\partial y}=z^{2}\cdot (-6\cdot y-2\cdot x)\end{aligned}
$$

Writing the above results in terms of $r,\theta,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial w}{\partial x} & =z^{2}\cdot (-2\cdot r\cdot \sin\theta+6\cdot r\cdot \cos\theta), \\ \frac{\partial w}{\partial y} & =z^{2}\cdot (-6\cdot r\cdot \sin\theta-2\cdot r\cdot \cos\theta).\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial w}{\partial \theta} & =-(z^{2}\cdot (-2\cdot r\cdot \sin\theta+6\cdot r\cdot \cos\theta))\cdot r\cdot \sin\theta+(z^{2}\cdot (-6\cdot r\cdot \sin\theta-2\cdot r\cdot \cos\theta))\cdot r\cdot \cos\theta \\  & =2\cdot r^{2}\cdot z^{2}\cdot \sin^{2}\theta-6\cdot r^{2}\cdot z^{2}\cdot \cos\theta\cdot \sin\theta-6\cdot r^{2}\cdot z^{2}\cdot \cos\theta\cdot \sin\theta-2\cdot r^{2}\cdot z^{2}\cdot \cos^{2}\theta \\  & =r^{2}\cdot z^{2}\cdot (-6\cdot \sin(2\cdot \theta)-2\cdot \cos(2\cdot \theta)).\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $g(x,y,z)=z^{3}\cdot (2\cdot x^{2}-5\cdot x\cdot y+4\cdot y^{2}),$ find $\frac{\partial g}{\partial \theta},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta,z)$ are the corresponding cylindrical polar coordinates.

1. $r\cdot z^{3}\cdot (-5\cdot r\cdot \cos\theta+8\cdot r\cdot \sin\theta)\cdot \cos\theta$
2. $r^{2}\cdot z^{3}\cdot (2\cdot \sin(2\cdot \theta)-5\cdot \cos(2\cdot \theta))$
3. $z^{3}\cdot (-5\cdot r\cdot \cos\theta+8\cdot r\cdot \sin\theta)+z^{3}\cdot (-5\cdot r\cdot \sin\theta+4\cdot r\cdot \cos\theta)$
4. $r\cdot z^{3}\cdot (-5\cdot r\cdot \cos\theta+8\cdot r\cdot \sin\theta)\cdot \cos\theta+r\cdot z^{3}\cdot (-5\cdot r\cdot \sin\theta+4\cdot r\cdot \cos\theta)\cdot \sin\theta$
5. $-r\cdot z^{3}\cdot (-5\cdot r\cdot \sin\theta+4\cdot r\cdot \cos\theta)\cdot \sin\theta$

Applying the multivariable chain rule for the function $g(x,y,z)$ with three independent variables $r,\theta,$ and $z,$ where $x=r\cos\theta,y=r\sin\theta,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =\frac{\partial g}{\partial x}\cdot \frac{\partial x}{\partial \theta}+\frac{\partial g}{\partial y}\cdot \frac{\partial y}{\partial \theta}+\frac{\partial g}{\partial z}\cdot \frac{\partial z}{\partial \theta} \\  & =-\frac{\partial g}{\partial x}\cdot r\cdot \sin\theta+\frac{\partial g}{\partial y}\cdot r\cdot \cos\theta.\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial g}{\partial x}=z^{3}\cdot (-5\cdot y+4\cdot x),\,\frac{\partial g}{\partial y}=z^{3}\cdot (-5\cdot x+8\cdot y)\end{aligned}
$$

Writing the above results in terms of $r,\theta,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial g}{\partial x} & =z^{3}\cdot (-5\cdot r\cdot \sin\theta+4\cdot r\cdot \cos\theta), \\ \frac{\partial g}{\partial y} & =z^{3}\cdot (-5\cdot r\cdot \cos\theta+8\cdot r\cdot \sin\theta).\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial g}{\partial \theta} & =-(z^{3}\cdot (-5\cdot r\cdot \sin\theta+4\cdot r\cdot \cos\theta))\cdot r\cdot \sin\theta+(z^{3}\cdot (-5\cdot r\cdot \cos\theta+8\cdot r\cdot \sin\theta))\cdot r\cdot \cos\theta \\  & =5\cdot r^{2}\cdot z^{3}\cdot \sin^{2}\theta-4\cdot r^{2}\cdot z^{3}\cdot \cos\theta\cdot \sin\theta-5\cdot r^{2}\cdot z^{3}\cdot \cos^{2}\theta+8\cdot r^{2}\cdot z^{3}\cdot \cos\theta\cdot \sin\theta \\  & =r^{2}\cdot z^{3}\cdot (2\cdot \sin(2\cdot \theta)-5\cdot \cos(2\cdot \theta)).\end{aligned}
$$


## r_coupled — authored hard


### Generated variant 1 — authored_operations


Given that $w(x,y,z)=3\cdot x^{2}\cdot z^{4}-2\cdot x\cdot y\cdot z-3\cdot y^{2}\cdot z^{4},$ find $\frac{\partial w}{\partial r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta,z)$ are the corresponding cylindrical polar coordinates.

1. $(-6\cdot r\cdot z^{4}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta)\cdot \sin\theta$
2. $(-6\cdot r\cdot z^{4}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta)\cdot \sin\theta-(-2\cdot r\cdot z\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos\theta)\cdot \cos\theta$
3. $-6\cdot r\cdot z^{4}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta-2\cdot r\cdot z\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos\theta$
4. $-6\cdot r\cdot z^{4}\cdot \sin^{2}\theta+6\cdot r\cdot z^{4}\cdot \cos^{2}\theta-4\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta$
5. $(-2\cdot r\cdot z\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos\theta)\cdot \cos\theta$

Applying the multivariable chain rule for the function $w(x,y,z)$ with three independent variables $r,\theta,$ and $z,$ where $x=r\cos\theta,y=r\sin\theta,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial w}{\partial r} & =\frac{\partial w}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial w}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial w}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial w}{\partial x}\cdot \cos\theta+\frac{\partial w}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial w}{\partial x}=-2\cdot y\cdot z+6\cdot x\cdot z^{4},\,\frac{\partial w}{\partial y}=-6\cdot y\cdot z^{4}-2\cdot x\cdot z\end{aligned}
$$

Writing the above results in terms of $r,\theta,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial w}{\partial x} & =-2\cdot r\cdot z\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos\theta, \\ \frac{\partial w}{\partial y} & =-6\cdot r\cdot z^{4}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial w}{\partial r} & =(-2\cdot r\cdot z\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos\theta)\cdot \cos\theta+(-6\cdot r\cdot z^{4}\cdot \sin\theta-2\cdot r\cdot z\cdot \cos\theta)\cdot \sin\theta \\  & =-2\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta+6\cdot r\cdot z^{4}\cdot \cos^{2}\theta-6\cdot r\cdot z^{4}\cdot \sin^{2}\theta-2\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta \\  & =-6\cdot r\cdot z^{4}\cdot \sin^{2}\theta+6\cdot r\cdot z^{4}\cdot \cos^{2}\theta-4\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta.\end{aligned}
$$


### Generated variant 2 — authored_operations


Given that $h(x,y,z)=2\cdot x^{2}\cdot z^{3}-5\cdot x\cdot y\cdot z+4\cdot y^{2}\cdot z^{3},$ find $\frac{\partial h}{\partial r},$ where $(x,y,z)$ are Cartesian coordinates and $(r,\theta,z)$ are the corresponding cylindrical polar coordinates.

1. $(-5\cdot r\cdot z\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos\theta)\cdot \cos\theta$
2. $4\cdot r\cdot z^{3}\cdot \cos^{2}\theta+8\cdot r\cdot z^{3}\cdot \sin^{2}\theta-10\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta$
3. $(-5\cdot r\cdot z\cdot \cos\theta+8\cdot r\cdot z^{3}\cdot \sin\theta)\cdot \sin\theta$
4. $-5\cdot r\cdot z\cdot \cos\theta-5\cdot r\cdot z\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos\theta+8\cdot r\cdot z^{3}\cdot \sin\theta$
5. $(-5\cdot r\cdot z\cdot \cos\theta+8\cdot r\cdot z^{3}\cdot \sin\theta)\cdot \sin\theta-(-5\cdot r\cdot z\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos\theta)\cdot \cos\theta$

Applying the multivariable chain rule for the function $h(x,y,z)$ with three independent variables $r,\theta,$ and $z,$ where $x=r\cos\theta,y=r\sin\theta,$ and $z=z,$ we have

$$
\begin{aligned}\frac{\partial h}{\partial r} & =\frac{\partial h}{\partial x}\cdot \frac{\partial x}{\partial r}+\frac{\partial h}{\partial y}\cdot \frac{\partial y}{\partial r}+\frac{\partial h}{\partial z}\cdot \frac{\partial z}{\partial r} \\  & =\frac{\partial h}{\partial x}\cdot \cos\theta+\frac{\partial h}{\partial y}\cdot \sin\theta.\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{\partial h}{\partial x}=-5\cdot y\cdot z+4\cdot x\cdot z^{3},\,\frac{\partial h}{\partial y}=-5\cdot x\cdot z+8\cdot y\cdot z^{3}\end{aligned}
$$

Writing the above results in terms of $r,\theta,$ and $z,$ we get

$$
\begin{aligned}\frac{\partial h}{\partial x} & =-5\cdot r\cdot z\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos\theta, \\ \frac{\partial h}{\partial y} & =-5\cdot r\cdot z\cdot \cos\theta+8\cdot r\cdot z^{3}\cdot \sin\theta.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{\partial h}{\partial r} & =(-5\cdot r\cdot z\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos\theta)\cdot \cos\theta+(-5\cdot r\cdot z\cdot \cos\theta+8\cdot r\cdot z^{3}\cdot \sin\theta)\cdot \sin\theta \\  & =-5\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta+4\cdot r\cdot z^{3}\cdot \cos^{2}\theta-5\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta+8\cdot r\cdot z^{3}\cdot \sin^{2}\theta \\  & =4\cdot r\cdot z^{3}\cdot \cos^{2}\theta+8\cdot r\cdot z^{3}\cdot \sin^{2}\theta-10\cdot r\cdot z\cdot \cos\theta\cdot \sin\theta.\end{aligned}
$$
