# Originals and generated variants

Original evidence is reproduced verbatim below, including the two documented solution defects. Generated records use minimal repaired notation. Native grading and independent displayed mathematics are reported separately in validation.json.

## cubic (easy)

### Original q-104616

Let $f(x,y)={x}^{3}+y.$ Given that $C$ is the path along the curve $r(t)=⟨3t,{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $8$
- $32$
- $28$ (correct)
- $10$
- $21$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨3,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(3,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(3,1)-f(0,0) \\  & =({3}^{3}+1)-({0}^{3}+0) \\  & =(27+1)-0 \\  & =28.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 4, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{3} + y.$ Given that $C$ is the path along the curve $r(t)=⟨4 t,t^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $5$
- $-65$
- $65$
- $0$
- $17$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨4,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(4,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(4,1)-f(0,0) \\  & =\left(\left(4\right)^{3} + \left(1\right)\right)-\left(\left(0\right)^{3} + \left(0\right)\right) \\  & =\left(64+1\right)-\left(0\right) \\  & =65.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 4, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{3} + y.$ Given that $C$ is the path along the curve $r(t)=⟨4 t,t^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $5$
- $17$
- $0$
- $65$
- $-65$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨4,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(4,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(4,1)-f(0,0) \\  & =\left(\left(4\right)^{3} + \left(1\right)\right)-\left(\left(0\right)^{3} + \left(0\right)\right) \\  & =\left(64+1\right)-\left(0\right) \\  & =65.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 3, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left({x}^{3}+y\right).$ Given that $C$ is the path along the curve $r(t)=⟨3t,{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $16$
- $56$
- $20$
- $42$
- $64$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨3,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(3,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0))  \\  & =f(3,1)-f(0,0)  \\  & =2\left(({3}^{3}+1)-({0}^{3}+0)\right) \\  & =2\left((27+1)-0\right) \\  & =2\left(28\right).\end{aligned}
$$

## cycloid (easy)

### Original q-104623

Let $f(x,y)={x}^{2}y-{y}^{2}x.$ Given that $C$ is the path along the curve $r(t)=⟨t-\operatorname{sin}⁡t,1-\operatorname{cos}⁡t⟩$ for $t\in [0,\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- ${\pi }^{2}+2\pi $
- ${\pi }^{2}-1$
- $\pi +2$
- $0$
- $2{\pi }^{2}-4\pi $ (correct)

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(\pi ) & =⟨\pi ,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi ,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi ))-f(r(0)) \\  & =f(\pi ,2)-f(0,0) \\  & =({\pi }^{2}\cdot 2-{2}^{2}\cdot \pi )-({0}^{2}\cdot 0-{0}^{2}\cdot 0) \\  & =(2{\pi }^{2}-4\pi )-0 \\  & =2{\pi }^{2}-4\pi .\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"d": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{2} y - x y^{2}.$ Given that $C$ is the path along the curve $r(t)=⟨t - \sin{\left(t \right)},2 - 2 \cos{\left(t \right)}⟩$ for $t\in [0,\pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $4 \pi^{2} + 16 \pi$
- $- 4 \pi^{2} + 16 \pi$
- $- 16 \pi + 4 \pi^{2}$
- $0$
- $4 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(\pi) & =⟨\pi,4⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,4).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi))-f(r(0)) \\  & =f(\pi,4)-f(0,0) \\  & =\left(\left(\pi\right)^{2} \left(4\right) - \left(\pi\right) \left(4\right)^{2}\right)-\left(\left(0\right)^{2} \left(0\right) - \left(0\right) \left(0\right)^{2}\right) \\  & =\left(- 16 \pi + 4 \pi^{2}\right)-\left(0\right) \\  & =- 16 \pi + 4 \pi^{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"d": 3, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y)=- 2 x^{2} y + 2 x y^{2}.$ Given that $C$ is the path along the curve $r(t)=⟨t - \sin{\left(t \right)},3 - 3 \cos{\left(t \right)}⟩$ for $t\in [0,\pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 72 \pi - 12 \pi^{2}$
- $- 12 \pi^{2}$
- $0$
- $- 12 \pi^{2} + 72 \pi$
- $- 72 \pi + 12 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(\pi) & =⟨\pi,6⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi,6).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi))-f(r(0)) \\  & =f(\pi,6)-f(0,0) \\  & =\left(- 2 \left(\pi\right)^{2} \left(6\right) + 2 \left(\pi\right) \left(6\right)^{2}\right)-\left(- 2 \left(0\right)^{2} \left(0\right) + 2 \left(0\right) \left(0\right)^{2}\right) \\  & =\left(- 12 \pi^{2} + 72 \pi\right)-\left(0\right) \\  & =- 12 \pi^{2} + 72 \pi.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"d": 1, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left({x}^{2}y-{y}^{2}x\right).$ Given that $C$ is the path along the curve $r(t)=⟨t-\operatorname{sin}⁡t,1-\operatorname{cos}⁡t⟩$ for $t\in [0,\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $4 \pi + 2 \pi^{2}$
- $4 + 2 \pi$
- $0$
- $- 8 \pi + 4 \pi^{2}$
- $-2 + 2 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(\pi ) & =⟨\pi ,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(\pi ,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi ))-f(r(0))  \\  & =f(\pi ,2)-f(0,0)  \\  & =2\left(({\pi }^{2}\cdot 2-{2}^{2}\cdot \pi )-({0}^{2}\cdot 0-{0}^{2}\cdot 0)\right) \\  & =2\left((2{\pi }^{2}-4\pi )-0\right) \\  & =2\left(2{\pi }^{2}-4\pi\right).\end{aligned}
$$

## sqrt_product (easy)

### Original q-124002

Let $f(x,y)={x}^{2}{y}^{2}+x+y.$ Given that $C$ is the path along the curve $r(t)=⟨\sqrt{t},t+1⟩$ for $t\in [0,4],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $76$
- $98$
- $87$
- $109$
- $106$ (correct)

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩ \\ r(4) & =⟨2,5⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,5).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(4))-f(r(0)) \\  & =f(2,5)-f(0,1) \\  & =({2}^{2}\cdot {5}^{2}+2+5)-({0}^{2}\cdot {1}^{2}+0+1) \\  & =107-1 \\  & =106.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"h": -2, "n": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{2} y^{2} + x + y.$ Given that $C$ is the path along the curve $r(t)=⟨\sqrt{t},t - 2⟩$ for $t\in [0,4],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $20$
- $-22$
- $22$
- $0$
- $16$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-2⟩ \\ r(4) & =⟨2,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-2)$ and $(2,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(4))-f(r(0)) \\  & =f(2,2)-f(0,-2) \\  & =\left(\left(2\right)^{2} \left(2\right)^{2} + \left(2\right) + \left(2\right)\right)-\left(\left(0\right)^{2} \left(-2\right)^{2} + \left(0\right) + \left(-2\right)\right) \\  & =\left(20\right)-\left(-2\right) \\  & =22.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"h": -2, "n": 3, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y)=- 2 x^{2} y^{2} - 2 x - 2 y.$ Given that $C$ is the path along the curve $r(t)=⟨\sqrt{t},t - 2⟩$ for $t\in [0,9],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-902$
- $-882$
- $0$
- $-906$
- $906$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-2⟩ \\ r(9) & =⟨3,7⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-2)$ and $(3,7).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(9))-f(r(0)) \\  & =f(3,7)-f(0,-2) \\  & =\left(- 2 \left(3\right)^{2} \left(7\right)^{2} - 2 \left(3\right) - 2 \left(7\right)\right)-\left(- 2 \left(0\right)^{2} \left(-2\right)^{2} - 2 \left(0\right) - 2 \left(-2\right)\right) \\  & =\left(-902\right)-\left(4\right) \\  & =-906.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"h": 1, "n": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left({x}^{2}{y}^{2}+x+y\right).$ Given that $C$ is the path along the curve $r(t)=⟨\sqrt{t},t+1⟩$ for $t\in [0,4],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $152$
- $174$
- $218$
- $212$
- $196$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩ \\ r(4) & =⟨2,5⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(2,5).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(4))-f(r(0))  \\  & =f(2,5)-f(0,1)  \\  & =2\left(({2}^{2}\cdot {5}^{2}+2+5)-({0}^{2}\cdot {1}^{2}+0+1)\right) \\  & =2\left(107-1\right) \\  & =2\left(106\right).\end{aligned}
$$

## exponential (easy)

### Original q-124003

Let $f(x,y)=y{e}^{2x}.$ Given that $C$ is the path along the curve $r(t)=⟨t,3{t}^{2}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $3e+1$
- $3+e$
- $3e$
- $3{e}^{2}$ (correct)
- ${e}^{2}-1$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨1,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,3).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,3)-f(0,0) \\  & =(3{e}^{2\cdot 1})-(0\cdot {e}^{2(0)}) \\  & =3{e}^{2}-0 \\  & =3{e}^{2}.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 1, "k": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=y e^{2 x}.$ Given that $C$ is the path along the curve $r(t)=⟨t,t^{2}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $e$
- $- e^{2}$
- $e^{2}$
- $0$
- $-1 + e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨1,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,1)-f(0,0) \\  & =\left(\left(1\right) e^{2 \left(1\right)}\right)-\left(\left(0\right) e^{2 \left(0\right)}\right) \\  & =\left(e^{2}\right)-\left(0\right) \\  & =e^{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 1, "k": 3, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y)=- 2 y e^{3 x}.$ Given that $C$ is the path along the curve $r(t)=⟨t,t^{2}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 2 e$
- $2 - 2 e^{3}$
- $0$
- $- 2 e^{3}$
- $2 e^{3}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨1,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,1)-f(0,0) \\  & =\left(- 2 \left(1\right) e^{3 \left(1\right)}\right)-\left(- 2 \left(0\right) e^{3 \left(0\right)}\right) \\  & =\left(- 2 e^{3}\right)-\left(0\right) \\  & =- 2 e^{3}.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 3, "k": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left(y{e}^{2x}\right).$ Given that $C$ is the path along the curve $r(t)=⟨t,3{t}^{2}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $2 + 6 e$
- $6 e$
- $6 e^{2}$
- $-2 + 2 e^{2}$
- $2 e + 6$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0⟩ \\ r(1) & =⟨1,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0)$ and $(1,3).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0))  \\  & =f(1,3)-f(0,0)  \\  & =2\left((3{e}^{2\cdot 1})-(0\cdot {e}^{2(0)})\right) \\  & =2\left(3{e}^{2}-0\right) \\  & =2\left(3{e}^{2}\right).\end{aligned}
$$

## cos_linear (easy)

### Original q-124005

Let $f(x,y)=y\operatorname{cos}⁡x+x.$ Given that $C$ is the path along the curve $r(t)=⟨t,2t⟩$ for $t\in [\frac{\pi }{2},\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-\frac{3\pi }{4}$
- $\frac{\pi }{4}$
- $-2\pi $
- $\frac{\pi }{2}$
- $-\frac{3\pi }{2}$ (correct)

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(\frac{\pi }{2}) & =⟨\frac{\pi }{2},\pi ⟩ \\ r(\pi ) & =⟨\pi ,2\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(\frac{\pi }{2},\pi )$ and $(\pi ,2\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi ))-f(r(\frac{\pi }{2})) \\  & =f(\pi ,2\pi )-f(\frac{\pi }{2},\pi ) \\  & =(2\pi \operatorname{cos}⁡\pi +\pi )-(\pi \operatorname{cos}⁡(\frac{\pi }{2})+\frac{\pi }{2}) \\  & =-\pi -\frac{\pi }{2} \\  & =-\frac{3\pi }{2}.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 4, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x + y \cos{\left(x \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨t,4 t⟩$ for $t\in [\frac{\pi}{2},\pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 3 \pi$
- $\frac{7 \pi}{2}$
- $- \frac{7 \pi}{2}$
- $0$
- $\frac{\pi}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(\frac{\pi}{2}) & =⟨\frac{\pi}{2},2 \pi⟩ \\ r(\pi) & =⟨\pi,4 \pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(\frac{\pi}{2},2 \pi)$ and $(\pi,4 \pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi))-f(r(\frac{\pi}{2})) \\  & =f(\pi,4 \pi)-f(\frac{\pi}{2},2 \pi) \\  & =\left(\left(\pi\right) + \left(4 \pi\right) \cos{\left(\left(\pi\right) \right)}\right)-\left(\left(\frac{\pi}{2}\right) + \left(2 \pi\right) \cos{\left(\left(\frac{\pi}{2}\right) \right)}\right) \\  & =\left(- 3 \pi\right)-\left(\frac{\pi}{2}\right) \\  & =- \frac{7 \pi}{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 4, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x + y \cos{\left(x \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨t,4 t⟩$ for $t\in [\frac{\pi}{2},\pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 3 \pi$
- $\frac{\pi}{2}$
- $0$
- $- \frac{7 \pi}{2}$
- $\frac{7 \pi}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(\frac{\pi}{2}) & =⟨\frac{\pi}{2},2 \pi⟩ \\ r(\pi) & =⟨\pi,4 \pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(\frac{\pi}{2},2 \pi)$ and $(\pi,4 \pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi))-f(r(\frac{\pi}{2})) \\  & =f(\pi,4 \pi)-f(\frac{\pi}{2},2 \pi) \\  & =\left(\left(\pi\right) + \left(4 \pi\right) \cos{\left(\left(\pi\right) \right)}\right)-\left(\left(\frac{\pi}{2}\right) + \left(2 \pi\right) \cos{\left(\left(\frac{\pi}{2}\right) \right)}\right) \\  & =\left(- 3 \pi\right)-\left(\frac{\pi}{2}\right) \\  & =- \frac{7 \pi}{2}.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left(y\operatorname{cos}⁡x+x\right).$ Given that $C$ is the path along the curve $r(t)=⟨t,2t⟩$ for $t\in [\frac{\pi }{2},\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- \frac{3 \pi}{2}$
- $- 4 \pi$
- $\pi$
- $- 3 \pi$
- $\frac{\pi}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(\frac{\pi }{2}) & =⟨\frac{\pi }{2},\pi ⟩ \\ r(\pi ) & =⟨\pi ,2\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(\frac{\pi }{2},\pi )$ and $(\pi ,2\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi ))-f(r(\frac{\pi }{2}))  \\  & =f(\pi ,2\pi )-f(\frac{\pi }{2},\pi )  \\  & =2\left((2\pi \operatorname{cos}⁡\pi +\pi )-(\pi \operatorname{cos}⁡(\frac{\pi }{2})+\frac{\pi }{2})\right) \\  & =2\left(-\pi -\frac{\pi }{2}\right) \\  & =2\left(-\frac{3\pi }{2}\right).\end{aligned}
$$

## quadratic (easy)

### Original q-104624

Let $f(x,y)=y+{x}^{2}.$ Given that $C$ is the path along the curve $r(t)=⟨2t,{t}^{2}-1⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $15$
- $24$
- $12$
- $6$
- $20$ (correct)

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-1⟩ \\ r(2) & =⟨4,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(4,3)-f(0,-1) \\  & =(3+{4}^{2})-(-1+{0}^{2}) \\  & =(3+16)-(-1) \\  & =20.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"b": 3, "c": 2, "h": -1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{2} + y.$ Given that $C$ is the path along the curve $r(t)=⟨2 t,t^{2} + 1⟩$ for $t\in [0,3],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $46$
- $-45$
- $45$
- $0$
- $15$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,1⟩ \\ r(3) & =⟨6,10⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,1)$ and $(6,10).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(3))-f(r(0)) \\  & =f(6,10)-f(0,1) \\  & =\left(\left(6\right)^{2} + \left(10\right)\right)-\left(\left(0\right)^{2} + \left(1\right)\right) \\  & =\left(10+36\right)-\left(1\right) \\  & =45.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"b": 2, "c": 2, "h": 1, "scale": -3}`; profile `authored_endpoint_bank`.

Let $f(x,y)=- 3 x^{2} - 3 y.$ Given that $C$ is the path along the curve $r(t)=⟨2 t,t^{2} - 1⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-57$
- $-24$
- $0$
- $-60$
- $60$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-1⟩ \\ r(2) & =⟨4,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(4,3)-f(0,-1) \\  & =\left(- 3 \left(4\right)^{2} - 3 \left(3\right)\right)-\left(- 3 \left(0\right)^{2} - 3 \left(-1\right)\right) \\  & =-3\left(\left(3+16\right)-\left(-1\right)\right) \\  & =-60.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"b": 2, "c": 2, "h": 1, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left(y+{x}^{2}\right).$ Given that $C$ is the path along the curve $r(t)=⟨2t,{t}^{2}-1⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $30$
- $24$
- $12$
- $40$
- $48$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,-1⟩ \\ r(2) & =⟨4,3⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,-1)$ and $(4,3).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0))  \\  & =f(4,3)-f(0,-1)  \\  & =2\left((3+{4}^{2})-(-1+{0}^{2})\right) \\  & =2\left((3+16)-(-1)\right) \\  & =2\left(20\right).\end{aligned}
$$

## zero_ellipse (easy)

### Original q-104637

Let $f(x,y)=y{x}^{2}{e}^{xy}.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,2\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- ${\pi }^{2}-2$
- $0$ (correct)
- $\pi {e}^{2\pi }$
- ${\pi }^{2}{e}^{{\pi }^{2}}$
- $\frac{{\pi }^{2}}{4}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

  

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,0⟩, \\ r(\frac{\pi }{2}) & =⟨0,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(0,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f((r(\frac{\pi }{2}))-f(r(0)) \\  & =f(0,2)-f(1,0) \\  & =2\cdot (0)^{2}\cdot {e}^{0(2)}-0\cdot (1)^{2}\cdot {e}^{1(0)} \\  & =0.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 2, "d": 1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y)=x^{2} y e^{x y}.$ Given that $C$ is the path along the curve $r(t)=⟨2 \cos{\left(t \right)},\sin{\left(t \right)}⟩$ for $t\in [0,\frac{\pi}{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $4 e^{2}$
- $\frac{\pi^{2} e^{\frac{\pi}{2}}}{4}$
- $0$
- $\frac{\pi^{2} e^{\frac{\pi}{4}}}{16}$
- $2 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

  

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨2,0⟩ \\ r(\frac{\pi}{2}) & =⟨0,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0)$ and $(0,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi}{2}))-f(r(0)) \\  & =f(0,1)-f(2,0) \\  & =\left(\left(0\right)^{2} \left(1\right) e^{\left(0\right) \left(1\right)}\right)-\left(\left(2\right)^{2} \left(0\right) e^{\left(2\right) \left(0\right)}\right) \\  & =0.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 3, "d": 1, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y)=- 2 x^{2} y e^{x y}.$ Given that $C$ is the path along the curve $r(t)=⟨3 \cos{\left(t \right)},\sin{\left(t \right)}⟩$ for $t\in [0,\frac{\pi}{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 18 e^{3}$
- $- 6 e^{3}$
- $- \frac{\pi^{2} e^{\frac{\pi}{4}}}{8}$
- $0$
- $- \frac{\pi^{2} e^{\frac{\pi}{2}}}{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

  

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨3,0⟩ \\ r(\frac{\pi}{2}) & =⟨0,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(3,0)$ and $(0,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi}{2}))-f(r(0)) \\  & =f(0,1)-f(3,0) \\  & =\left(- 2 \left(0\right)^{2} \left(1\right) e^{\left(0\right) \left(1\right)}\right)-\left(- 2 \left(3\right)^{2} \left(0\right) e^{\left(3\right) \left(0\right)}\right) \\  & =0.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 1, "d": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y)=2\left(y{x}^{2}{e}^{xy}\right).$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,2\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-4 + 2 \pi^{2}$
- $2 \pi e^{2 \pi}$
- $2 \pi^{2} e^{\pi^{2}}$
- $\frac{\pi^{2}}{2}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

  

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,0⟩, \\ r(\frac{\pi }{2}) & =⟨0,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0)$ and $(0,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi }{2}))-f(r(0))  \\  & =f(0,2)-f(1,0)  \\  & =2\left(2\cdot (0)^{2}\cdot {e}^{0(2)}-0\cdot (1)^{2}\cdot {e}^{1(0)}\right) \\  & =2\left(0\right).\end{aligned}
$$

## trig3 (moderate)

### Original q-99008

Let $f(x,y,z)=x\operatorname{sin}⁡y+y\operatorname{cos}⁡z.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{sin}⁡t,t,2t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $\pi +1$
- $1-\frac{\pi }{2}$ (correct)
- $1-\pi $
- $\frac{\pi }{3}$
- ${\pi }^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(\frac{\pi }{2}) & =⟨1,\frac{\pi }{2},\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,\frac{\pi }{2},\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\pi ))-f(r(0)) \\  & =f(1,\frac{\pi }{2},\pi )-f(0,0,0) \\  & =(1\cdot \operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\cdot \operatorname{cos}⁡\pi )-(0\cdot \operatorname{sin}⁡0+0\cdot \operatorname{cos}⁡0) \\  & =(1+\frac{\pi }{2}\cdot (-1))-0 \\  & =1-\frac{\pi }{2}.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 2, "d": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=x \sin{\left(y \right)} + y \cos{\left(z \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨2 \sin{\left(t \right)},t,2 t⟩$ for $t\in [0,\frac{\pi}{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $-2 + \frac{\pi}{2}$
- $2 - \frac{\pi}{2}$
- $1 - \frac{\pi}{4}$
- $4 - \pi$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(\frac{\pi}{2}) & =⟨2,\frac{\pi}{2},\pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(2,\frac{\pi}{2},\pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi}{2}))-f(r(0)) \\  & =f(2,\frac{\pi}{2},\pi)-f(0,0,0) \\  & =\left(\left(2\right) \sin{\left(\left(\frac{\pi}{2}\right) \right)} + \left(\frac{\pi}{2}\right) \cos{\left(\left(\pi\right) \right)}\right)-\left(\left(0\right) \sin{\left(\left(0\right) \right)} + \left(0\right) \cos{\left(\left(0\right) \right)}\right) \\  & =\left(2+\frac{\pi}{2}\cdot\left(-1\right)\right)-\left(0\right) \\  & =2 - \frac{\pi}{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 3, "d": 2, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=- 2 x \sin{\left(y \right)} - 2 y \cos{\left(z \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨3 \sin{\left(t \right)},t,2 t⟩$ for $t\in [0,\frac{\pi}{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $-12 + 2 \pi$
- $-3 + \frac{\pi}{2}$
- $-6 + \pi$
- $6 - \pi$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(\frac{\pi}{2}) & =⟨3,\frac{\pi}{2},\pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(3,\frac{\pi}{2},\pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi}{2}))-f(r(0)) \\  & =f(3,\frac{\pi}{2},\pi)-f(0,0,0) \\  & =\left(- 2 \left(3\right) \sin{\left(\left(\frac{\pi}{2}\right) \right)} - 2 \left(\frac{\pi}{2}\right) \cos{\left(\left(\pi\right) \right)}\right)-\left(- 2 \left(0\right) \sin{\left(\left(0\right) \right)} - 2 \left(0\right) \cos{\left(\left(0\right) \right)}\right) \\  & =-2\left(\left(3+\frac{\pi}{2}\cdot\left(-1\right)\right)-\left(0\right)\right) \\  & =-6 + \pi.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 1, "d": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y,z)=2\left(x\operatorname{sin}⁡y+y\operatorname{cos}⁡z\right).$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{sin}⁡t,t,2t⟩$ for $t\in [0,\frac{\pi }{2}],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $2 + 2 \pi$
- $2 - 2 \pi$
- $\frac{2 \pi}{3}$
- $2 \pi^{2}$
- $2 - \pi$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(\frac{\pi }{2}) & =⟨1,\frac{\pi }{2},\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,\frac{\pi }{2},\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(\frac{\pi }{2}))-f(r(0))  \\  & =f(1,\frac{\pi }{2},\pi )-f(0,0,0)  \\  & =2\left((1\cdot \operatorname{sin}⁡(\frac{\pi }{2})+\frac{\pi }{2}\cdot \operatorname{cos}⁡\pi )-(0\cdot \operatorname{sin}⁡0+0\cdot \operatorname{cos}⁡0)\right) \\  & =2\left((1+\frac{\pi }{2}\cdot (-1))-0\right) \\  & =2\left(1-\frac{\pi }{2}\right).\end{aligned}
$$

## helix (moderate)

### Original q-104640

Let $f(x,y,z)={x}^{2}z+x\operatorname{sin}⁡y.$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,\operatorname{sin}⁡t,t⟩$ for $t\in [0,2\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- ${\pi }^{2}$
- $2$
- $2\pi $ (correct)
- $\pi +1$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,0,0⟩ \\ r(2\pi ) & =⟨1,0,2\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0,0)$ and $(1,0,2\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2\pi ))-f(r(0)) \\  & =f(1,0,2\pi )-f(1,0,0) \\  & =({1}^{2}\cdot 2\pi +1\cdot \operatorname{sin}⁡0)-({1}^{2}\cdot 0+1\cdot \operatorname{sin}⁡0) \\  & =(2\pi +0)-0 \\  & =2\pi .\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 2, "d": 1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=x^{2} z + x \sin{\left(y \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨2 \cos{\left(t \right)},\sin{\left(t \right)},t⟩$ for $t\in [0,2 \pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $- 8 \pi$
- $8 \pi$
- $4 \pi$
- $16 \pi$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨2,0,0⟩ \\ r(2 \pi) & =⟨2,0,2 \pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(2,0,0)$ and $(2,0,2 \pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2 \pi))-f(r(0)) \\  & =f(2,0,2 \pi)-f(2,0,0) \\  & =\left(\left(2\right)^{2} \left(2 \pi\right) + \left(2\right) \sin{\left(\left(0\right) \right)}\right)-\left(\left(2\right)^{2} \left(0\right) + \left(2\right) \sin{\left(\left(0\right) \right)}\right) \\  & =\left(8 \pi+0\right)-\left(0\right) \\  & =8 \pi.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 3, "d": 1, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=- 2 x^{2} z - 2 x \sin{\left(y \right)}.$ Given that $C$ is the path along the curve $r(t)=⟨3 \cos{\left(t \right)},\sin{\left(t \right)},t⟩$ for $t\in [0,2 \pi],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $- 72 \pi$
- $- 18 \pi$
- $- 36 \pi$
- $36 \pi$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨3,0,0⟩ \\ r(2 \pi) & =⟨3,0,2 \pi⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(3,0,0)$ and $(3,0,2 \pi).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2 \pi))-f(r(0)) \\  & =f(3,0,2 \pi)-f(3,0,0) \\  & =\left(- 2 \left(3\right)^{2} \left(2 \pi\right) - 2 \left(3\right) \sin{\left(\left(0\right) \right)}\right)-\left(- 2 \left(3\right)^{2} \left(0\right) - 2 \left(3\right) \sin{\left(\left(0\right) \right)}\right) \\  & =-2\left(\left(18 \pi+0\right)-\left(0\right)\right) \\  & =- 36 \pi.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 1, "d": 1, "scale": 2}`; profile `observed_scale`.

Let $f(x,y,z)=2\left({x}^{2}z+x\operatorname{sin}⁡y\right).$ Given that $C$ is the path along the curve $r(t)=⟨\operatorname{cos}⁡t,\operatorname{sin}⁡t,t⟩$ for $t\in [0,2\pi ],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $4$
- $4 \pi$
- $2 + 2 \pi$
- $2 \pi^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,0,0⟩ \\ r(2\pi ) & =⟨1,0,2\pi ⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,0,0)$ and $(1,0,2\pi ).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2\pi ))-f(r(0))  \\  & =f(1,0,2\pi )-f(1,0,0)  \\  & =2\left(({1}^{2}\cdot 2\pi +1\cdot \operatorname{sin}⁡0)-({1}^{2}\cdot 0+1\cdot \operatorname{sin}⁡0)\right) \\  & =2\left((2\pi +0)-0\right) \\  & =2\left(2\pi\right).\end{aligned}
$$

## exp_sum (moderate)

### Original q-124008

Let $f(x,y,z)={e}^{x}+{e}^{y}+{e}^{z}.$ Given that $C$ is the path along the curve $r(t)=⟨t,{t}^{2},2{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- ${e}^{2}+3e$
- $3{e}^{2}-2$
- ${e}^{2}+2e-3$ (correct)
- ${e}^{2}-2$
- $3e-3$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,1,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,1,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,1,2)-f(0,0,0) \\  & =({e}^{1}+{e}^{1}+{e}^{2})-({e}^{0}+{e}^{0}+{e}^{0}) \\  & =(2e+{e}^{2})-3 \\  & ={e}^{2}+2e-3.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 2, "d": 1, "k": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=e^{x} + e^{y} + e^{z}.$ Given that $C$ is the path along the curve $r(t)=⟨2 t,t^{2},2 t^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $e + 2 e^{2}$
- $- 2 e^{2} - e + 3$
- $-3 + e + 2 e^{2}$
- $-3 + 3 e^{2}$
- $-1 + e + 2 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨2,1,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(2,1,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(2,1,2)-f(0,0,0) \\  & =\left(e^{\left(2\right)} + e^{\left(1\right)} + e^{\left(2\right)}\right)-\left(e^{\left(0\right)} + e^{\left(0\right)} + e^{\left(0\right)}\right) \\  & =\left(e + 2 e^{2}\right)-\left(3\right) \\  & =-3 + e + 2 e^{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 1, "d": 2, "k": 1, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=- 2 e^{x} - 2 e^{y} - 2 e^{z}.$ Given that $C$ is the path along the curve $r(t)=⟨t,2 t^{2},t^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- 2 e^{2} - 4 e$
- $- 2 e^{2} - 4 e + 2$
- $6 - 6 e$
- $- 2 e^{2} - 4 e + 6$
- $-6 + 4 e + 2 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,2,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,2,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,2,1)-f(0,0,0) \\  & =\left(- 2 e^{\left(1\right)} - 2 e^{\left(2\right)} - 2 e^{\left(1\right)}\right)-\left(- 2 e^{\left(0\right)} - 2 e^{\left(0\right)} - 2 e^{\left(0\right)}\right) \\  & =\left(- 2 e^{2} - 4 e\right)-\left(-6\right) \\  & =- 2 e^{2} - 4 e + 6.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 1, "d": 1, "k": 2, "scale": 2}`; profile `observed_scale`.

Let $f(x,y,z)=2\left({e}^{x}+{e}^{y}+{e}^{z}\right).$ Given that $C$ is the path along the curve $r(t)=⟨t,{t}^{2},2{t}^{3}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $2 e^{2} + 6 e$
- $-6 + 4 e + 2 e^{2}$
- $-4 + 2 e^{2}$
- $-6 + 6 e$
- $-4 + 6 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,1,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,1,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0))  \\  & =f(1,1,2)-f(0,0,0)  \\  & =2\left(({e}^{1}+{e}^{1}+{e}^{2})-({e}^{0}+{e}^{0}+{e}^{0})\right) \\  & =2\left((2e+{e}^{2})-3\right) \\  & =2\left({e}^{2}+2e-3\right).\end{aligned}
$$

## exp_product (moderate)

### Original q-104638

Let $f(x,y,z)=y{e}^{xz}.$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2}+1,{t}^{2}-1,{t}^{2}-2t⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $e$
- $0$
- $4$ (correct)
- $3{e}^{2}$
- $5{e}^{6}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,-1,0⟩ \\ r(2) & =⟨5,3,0⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,-1,0)$ and $(5,3,0).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(5,3,0)-f(1,-1,0) \\  & =3\cdot {e}^{5(0)}-(-1)\cdot {e}^{1(0)} \\  & =3+1 \\  & =4.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"b": 2, "h": 3, "k": 1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=y e^{x z}.$ Given that $C$ is the path along the curve $r(t)=⟨t^{2} + 3,t^{2} - 1,t \left(t - 2\right)⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $2$
- $-4$
- $4$
- $0$
- $3$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨3,-1,0⟩ \\ r(2) & =⟨7,3,0⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(3,-1,0)$ and $(7,3,0).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(7,3,0)-f(3,-1,0) \\  & =\left(\left(3\right) e^{\left(7\right) \left(0\right)}\right)-\left(\left(-1\right) e^{\left(3\right) \left(0\right)}\right) \\  & =3+1 \\  & =4.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"b": 3, "h": 1, "k": 2, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=- 2 y e^{x z}.$ Given that $C$ is the path along the curve $r(t)=⟨t^{2} + 1,t^{2} - 2,t \left(t - 3\right)⟩$ for $t\in [0,3],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-10$
- $-14$
- $0$
- $-18$
- $18$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,-2,0⟩ \\ r(3) & =⟨10,7,0⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,-2,0)$ and $(10,7,0).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(3))-f(r(0)) \\  & =f(10,7,0)-f(1,-2,0) \\  & =\left(- 2 \left(7\right) e^{\left(10\right) \left(0\right)}\right)-\left(- 2 \left(-2\right) e^{\left(1\right) \left(0\right)}\right) \\  & =-2\left(7+2\right) \\  & =-18.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"b": 2, "h": 1, "k": 1, "scale": 2}`; profile `observed_scale`.

Let $f(x,y,z)=2\left(y{e}^{xz}\right).$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2}+1,{t}^{2}-1,{t}^{2}-2t⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $2 e$
- $8$
- $6 e^{2}$
- $10 e^{6}$
- $0$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,-1,0⟩ \\ r(2) & =⟨5,3,0⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,-1,0)$ and $(5,3,0).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0))  \\  & =f(5,3,0)-f(1,-1,0)  \\  & =2\left(3\cdot {e}^{5(0)}-(-1)\cdot {e}^{1(0)}\right) \\  & =2\left(3+1\right) \\  & =2\left(4\right).\end{aligned}
$$

## monomial3 (moderate)

### Original q-104639

Let $f(x,y,z)=x{y}^{2}{z}^{3}.$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2},{t}^{4},{t}^{6}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $1$ (correct)
- $36$
- $8$
- $64$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,1,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,1,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,1,1)-f(0,0,0) \\  & =(1\cdot {1}^{2}\cdot {1}^{3})-(0\cdot {0}^{2}\cdot {0}^{3}) \\  & =1-0 \\  & =1.\end{aligned}
$$

### Authored generated variant 1

Parameters: `{"c": 2, "d": 1, "k": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=x y^{2} z^{3}.$ Given that $C$ is the path along the curve $r(t)=⟨2 t^{2},t^{4},2 t^{6}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $24$
- $-16$
- $16$
- $0$
- $4$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨2,1,2⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(2,1,2).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(2,1,2)-f(0,0,0) \\  & =\left(\left(2\right) \left(1\right)^{2} \left(2\right)^{3}\right)-\left(\left(0\right) \left(0\right)^{2} \left(0\right)^{3}\right) \\  & =\left(16\right)-\left(0\right) \\  & =16.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"c": 1, "d": 2, "k": 1, "scale": -2}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=- 2 x y^{2} z^{3}.$ Given that $C$ is the path along the curve $r(t)=⟨t^{2},2 t^{4},t^{6}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-16$
- $-4$
- $0$
- $-8$
- $8$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,2,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,2,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(1,2,1)-f(0,0,0) \\  & =\left(- 2 \left(1\right) \left(2\right)^{2} \left(1\right)^{3}\right)-\left(- 2 \left(0\right) \left(0\right)^{2} \left(0\right)^{3}\right) \\  & =\left(-8\right)-\left(0\right) \\  & =-8.\end{aligned}
$$

### Observed-bank homogeneous variant 3

Parameters: `{"c": 1, "d": 1, "k": 1, "scale": 2}`; profile `observed_scale`.

Let $f(x,y,z)=2\left(x{y}^{2}{z}^{3}\right).$ Given that $C$ is the path along the curve $r(t)=⟨{t}^{2},{t}^{4},{t}^{6}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $0$
- $72$
- $16$
- $128$
- $2$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨0,0,0⟩ \\ r(1) & =⟨1,1,1⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(0,0,0)$ and $(1,1,1).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0))  \\  & =f(1,1,1)-f(0,0,0)  \\  & =2\left((1\cdot {1}^{2}\cdot {1}^{3})-(0\cdot {0}^{2}\cdot {0}^{3})\right) \\  & =2\left(1-0\right) \\  & =2\left(1\right).\end{aligned}
$$

## reciprocal_exp (hard)

Authored missing-hard template; method reference e-8759. There is no observed hard original.

### Authored generated variant 1

Parameters: `{"a": 1, "b": 1, "end": 2, "h": 1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=x y^{2} + y z.$ Given that $C$ is the path along the curve $r(t)=⟨e^{t},t + 1,e^{- t}⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $\frac{3}{e^{2}} + 2 + 9 e^{2}$
- $- 9 e^{2} - \frac{3}{e^{2}} + 2$
- $-2 + \frac{3}{e^{2}} + 9 e^{2}$
- $2$
- $\frac{3}{e^{2}} + 9 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,1,1⟩ \\ r(2) & =⟨e^{2},3,e^{-2}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,1,1)$ and $(e^{2},3,e^{-2}).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(e^{2},3,e^{-2})-f(1,1,1) \\  & =\left(\left(e^{2}\right) \left(3\right)^{2} + \left(3\right) \left(e^{-2}\right)\right)-\left(\left(1\right) \left(1\right)^{2} + \left(1\right) \left(1\right)\right) \\  & =\left(\frac{3}{e^{2}} + 9 e^{2}\right)-\left(2\right) \\  & =-2 + \frac{3}{e^{2}} + 9 e^{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"a": 2, "b": -3, "end": 1, "h": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=2 x y^{2} - 3 y z.$ Given that $C$ is the path along the curve $r(t)=⟨e^{t},t + 2,e^{- t}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $- \frac{9}{e} + 2 + 18 e$
- $- \frac{9}{e} + 18 e$
- $2$
- $- \frac{9}{e} - 2 + 18 e$
- $- 18 e + 2 + \frac{9}{e}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,2,1⟩ \\ r(1) & =⟨e,3,e^{-1}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,2,1)$ and $(e,3,e^{-1}).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(e,3,e^{-1})-f(1,2,1) \\  & =\left(2 \left(e\right) \left(3\right)^{2} - 3 \left(3\right) \left(e^{-1}\right)\right)-\left(2 \left(1\right) \left(2\right)^{2} - 3 \left(2\right) \left(1\right)\right) \\  & =\left(- \frac{9}{e} + 18 e\right)-\left(2\right) \\  & =- \frac{9}{e} - 2 + 18 e.\end{aligned}
$$

## reciprocal_product (hard)

Authored missing-hard template; method reference e-8759. There is no observed hard original.

### Authored generated variant 1

Parameters: `{"a": 1, "b": 1, "end": 2, "h": 1, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=x y^{2} + x y z.$ Given that $C$ is the path along the curve $r(t)=⟨e^{t},t + 1,e^{- t}⟩$ for $t\in [0,2],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $5 + 9 e^{2}$
- $- 9 e^{2} - 1$
- $1 + 9 e^{2}$
- $2$
- $3 + 9 e^{2}$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,1,1⟩ \\ r(2) & =⟨e^{2},3,e^{-2}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,1,1)$ and $(e^{2},3,e^{-2}).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(2))-f(r(0)) \\  & =f(e^{2},3,e^{-2})-f(1,1,1) \\  & =\left(\left(e^{2}\right) \left(3\right)^{2} + \left(e^{2}\right) \left(3\right) \left(e^{-2}\right)\right)-\left(\left(1\right) \left(1\right)^{2} + \left(1\right) \left(1\right) \left(1\right)\right) \\  & =\left(3 + 9 e^{2}\right)-\left(2\right) \\  & =1 + 9 e^{2}.\end{aligned}
$$

### Authored generated variant 2

Parameters: `{"a": 2, "b": -3, "end": 1, "h": 2, "scale": 1}`; profile `authored_endpoint_bank`.

Let $f(x,y,z)=2 x y^{2} - 3 x y z.$ Given that $C$ is the path along the curve $r(t)=⟨e^{t},t + 2,e^{- t}⟩$ for $t\in [0,1],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$

- $-7 + 18 e$
- $-9 + 18 e$
- $2$
- $-11 + 18 e$
- $11 - 18 e$

Let $C$ be a piecewise-smooth curve given by the vector function $r(t)$ for $t\in [a,b].$ Let $f$ be a differentiable function of two or three variables such that $∇f$ is continuous on $C.$ The fundamental theorem for line integrals states that 

$$
{\int }_{C}∇f\cdot \text{d}r=f(r(b))-f(r(a)).
$$

 

In our case, the position vectors of the endpoints of the curve are given by

$$
\begin{aligned}r(0) & =⟨1,2,1⟩ \\ r(1) & =⟨e,3,e^{-1}⟩.\end{aligned}
$$

Therefore, the coordinates of the endpoints of the path defined by $C$ are $(1,2,1)$ and $(e,3,e^{-1}).$

Applying the fundamental theorem for line integrals, we have

$$
\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & =f(r(1))-f(r(0)) \\  & =f(e,3,e^{-1})-f(1,2,1) \\  & =\left(2 \left(e\right) \left(3\right)^{2} - 3 \left(e\right) \left(3\right) \left(e^{-1}\right)\right)-\left(2 \left(1\right) \left(2\right)^{2} - 3 \left(1\right) \left(2\right) \left(1\right)\right) \\  & =\left(-9 + 18 e\right)-\left(2\right) \\  & =-11 + 18 e.\end{aligned}
$$
