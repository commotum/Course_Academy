## q-127055 / signed-half

Source:

Calculate the flux of the vector field $F(x,y)=(x+y)\,i+(y-x)\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(x + y)\,i+(- x + y)\,j$ across the closed curve $C$ given by $r(t)=3 \cos{\left(t \right)}\,i+3 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=3 \cos{\left(t \right)}$, $y=3 \sin{\left(t \right)}$.

Therefore, $P=3 \sin{\left(t \right)} + 3 \cos{\left(t \right)}$ and $Q=3 \sin{\left(t \right)} - 3 \cos{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 3 \sin{\left(t \right)}$ and $y\prime(t)=3 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(3 \sin{\left(t \right)} + 3 \cos{\left(t \right)})(3 \cos{\left(t \right)})-(3 \sin{\left(t \right)} - 3 \cos{\left(t \right)})(- 3 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(9 \sin^{2}{\left(t \right)} + 9 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $9$. Thus the flux is $[9t]_0^{2\pi}=18 \pi$.

Changed radius:

Calculate the flux of the vector field $F(x,y)=(x + y)\,i+(- x + y)\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+10 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=10 \sin{\left(t \right)}$.

Therefore, $P=10 \sin{\left(t \right)} + 10 \cos{\left(t \right)}$ and $Q=10 \sin{\left(t \right)} - 10 \cos{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=10 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(10 \sin{\left(t \right)} + 10 \cos{\left(t \right)})(10 \cos{\left(t \right)})-(10 \sin{\left(t \right)} - 10 \cos{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(100 \sin^{2}{\left(t \right)} + 100 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $100$. Thus the flux is $[100t]_0^{2\pi}=200 \pi$.

## q-127060 / cubic-scale

Source:

Calculate the flux of the vector field $F(x,y)=xy\,i+{x}^{2}\,j$ across the closed curve $C$ given by $r(t)=2\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(x y)\,i+(x^{2})\,j$ across the closed curve $C$ given by $r(t)=2 \cos{\left(t \right)}\,i+2 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=2 \cos{\left(t \right)}$, $y=2 \sin{\left(t \right)}$.

Therefore, $P=4 \sin{\left(t \right)} \cos{\left(t \right)}$ and $Q=4 \cos^{2}{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 2 \sin{\left(t \right)}$ and $y\prime(t)=2 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(4 \sin{\left(t \right)} \cos{\left(t \right)})(2 \cos{\left(t \right)})-(4 \cos^{2}{\left(t \right)})(- 2 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(16 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: $$-16\int_1^1u^2\,\mathrm du=0.$$

Changed radius:

Calculate the flux of the vector field $F(x,y)=(x y)\,i+(x^{2})\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+10 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=10 \sin{\left(t \right)}$.

Therefore, $P=100 \sin{\left(t \right)} \cos{\left(t \right)}$ and $Q=100 \cos^{2}{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=10 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(100 \sin{\left(t \right)} \cos{\left(t \right)})(10 \cos{\left(t \right)})-(100 \cos^{2}{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(2000 \sin{\left(t \right)} \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: $$-2000\int_1^1u^2\,\mathrm du=0.$$

## q-127077 / signed-half

Source:

Calculate the flux of the vector field $F(x,y)=x\,i+y\,j$ across the closed curve $C$ given by $r(t)=5\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(x)\,i+(y)\,j$ across the closed curve $C$ given by $r(t)=5 \cos{\left(t \right)}\,i+6 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=5 \cos{\left(t \right)}$, $y=6 \sin{\left(t \right)}$.

Therefore, $P=5 \cos{\left(t \right)}$ and $Q=6 \sin{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 5 \sin{\left(t \right)}$ and $y\prime(t)=6 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(5 \cos{\left(t \right)})(6 \cos{\left(t \right)})-(6 \sin{\left(t \right)})(- 5 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(30 \sin^{2}{\left(t \right)} + 30 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $30$. Thus the flux is $[30t]_0^{2\pi}=60 \pi$.

Changed radius:

Calculate the flux of the vector field $F(x,y)=(x)\,i+(y)\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+6 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=6 \sin{\left(t \right)}$.

Therefore, $P=10 \cos{\left(t \right)}$ and $Q=6 \sin{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=6 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(10 \cos{\left(t \right)})(6 \cos{\left(t \right)})-(6 \sin{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(60 \sin^{2}{\left(t \right)} + 60 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $60$. Thus the flux is $[60t]_0^{2\pi}=120 \pi$.

## q-127081 / coefficient-scale

Source:

Calculate the flux of the vector field $F(x,y)=y\,i+9{x}^{3}\,j$ across the closed curve $C$ given by $r(t)=\operatorname{cos}⁡t\,i+3\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(y)\,i+(9 x^{3})\,j$ across the closed curve $C$ given by $r(t)=\cos{\left(t \right)}\,i+3 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=\cos{\left(t \right)}$, $y=3 \sin{\left(t \right)}$.

Therefore, $P=3 \sin{\left(t \right)}$ and $Q=9 \cos^{3}{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- \sin{\left(t \right)}$ and $y\prime(t)=3 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(3 \sin{\left(t \right)})(3 \cos{\left(t \right)})-(9 \cos^{3}{\left(t \right)})(- \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(9 \sin{\left(t \right)} \cos^{3}{\left(t \right)} + 9 \sin{\left(t \right)} \cos{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: $$-\int_1^1\left(9u+9u^3\right)\,\mathrm du=0.$$

Changed radius:

Calculate the flux of the vector field $F(x,y)=(y)\,i+(9 x^{3})\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+3 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=3 \sin{\left(t \right)}$.

Therefore, $P=3 \sin{\left(t \right)}$ and $Q=9000 \cos^{3}{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=3 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(3 \sin{\left(t \right)})(3 \cos{\left(t \right)})-(9000 \cos^{3}{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(90000 \sin{\left(t \right)} \cos^{3}{\left(t \right)} + 9 \sin{\left(t \right)} \cos{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=\cos t$, $\mathrm du=-\sin t\,\mathrm dt$: $$-\int_1^1\left(9u+90000u^3\right)\,\mathrm du=0.$$

## q-127139 / area-scale

Source:

Calculate the flux of the vector field $F(x,y)={x}^{2}\,i+j$ across the closed curve $C$ given by $r(t)=7\operatorname{cos}⁡t\,i+2\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(x^{2})\,i+(1)\,j$ across the closed curve $C$ given by $r(t)=7 \cos{\left(t \right)}\,i+2 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=7 \cos{\left(t \right)}$, $y=2 \sin{\left(t \right)}$.

Therefore, $P=49 \cos^{2}{\left(t \right)}$ and $Q=1$.

Computing the derivatives gives $x\prime(t)=- 7 \sin{\left(t \right)}$ and $y\prime(t)=2 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(49 \cos^{2}{\left(t \right)})(2 \cos{\left(t \right)})-(1)(- 7 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(7 \sin{\left(t \right)} + 98 \cos^{3}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Write $\cos^3t=(1-\sin^2t)\cos t$ and use $u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$: $$[98\sin t-7\cos t]_0^{2\pi}-98\int_0^0u^2\,\mathrm du=0.$$

Changed radius:

Calculate the flux of the vector field $F(x,y)=(x^{2})\,i+(1)\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+2 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=2 \sin{\left(t \right)}$.

Therefore, $P=100 \cos^{2}{\left(t \right)}$ and $Q=1$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=2 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(100 \cos^{2}{\left(t \right)})(2 \cos{\left(t \right)})-(1)(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(10 \sin{\left(t \right)} + 200 \cos^{3}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Write $\cos^3t=(1-\sin^2t)\cos t$ and use $u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$: $$[200\sin t-10\cos t]_0^{2\pi}-200\int_0^0u^2\,\mathrm du=0.$$

## q-127140 / component-scale

Source:

Calculate the flux of the vector field $F(x,y)=4x\,i+4y\,j$ across the closed curve $C$ given by $r(t)=8\operatorname{cos}⁡t\,i+6\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(4 x)\,i+(4 y)\,j$ across the closed curve $C$ given by $r(t)=8 \cos{\left(t \right)}\,i+6 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=8 \cos{\left(t \right)}$, $y=6 \sin{\left(t \right)}$.

Therefore, $P=32 \cos{\left(t \right)}$ and $Q=24 \sin{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 8 \sin{\left(t \right)}$ and $y\prime(t)=6 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(32 \cos{\left(t \right)})(6 \cos{\left(t \right)})-(24 \sin{\left(t \right)})(- 8 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(192 \sin^{2}{\left(t \right)} + 192 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $192$. Thus the flux is $[192t]_0^{2\pi}=384 \pi$.

Changed radius:

Calculate the flux of the vector field $F(x,y)=(4 x)\,i+(4 y)\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+6 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=6 \sin{\left(t \right)}$.

Therefore, $P=40 \cos{\left(t \right)}$ and $Q=24 \sin{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=6 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(40 \cos{\left(t \right)})(6 \cos{\left(t \right)})-(24 \sin{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(240 \sin^{2}{\left(t \right)} + 240 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Using $\cos^2t+\sin^2t=1$, the integrand is $240$. Thus the flux is $[240t]_0^{2\pi}=480 \pi$.

## q-127062 / axis-square-scale

Source:

Calculate the flux of the vector field $F(x,y)={e}^{y}\,i+{e}^{x}\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+4\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(e^{y})\,i+(e^{x})\,j$ across the closed curve $C$ given by $r(t)=3 \cos{\left(t \right)}\,i+4 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=3 \cos{\left(t \right)}$, $y=4 \sin{\left(t \right)}$.

Therefore, $P=e^{4 \sin{\left(t \right)}}$ and $Q=e^{3 \cos{\left(t \right)}}$.

Computing the derivatives gives $x\prime(t)=- 3 \sin{\left(t \right)}$ and $y\prime(t)=4 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(e^{4 \sin{\left(t \right)}})(4 \cos{\left(t \right)})-(e^{3 \cos{\left(t \right)}})(- 3 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(4 e^{4 \sin{\left(t \right)}} \cos{\left(t \right)} + 3 e^{3 \cos{\left(t \right)}} \sin{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=4\sin t$, $\mathrm du=4\cos t\,\mathrm dt$ and $v=3\cos t$, $\mathrm dv=-3\sin t\,\mathrm dt$: $$\int_0^0e^u\,\mathrm du-\int_{3}^{3}e^v\,\mathrm dv=0.$$

Changed radius:

Calculate the flux of the vector field $F(x,y)=(e^{y})\,i+(e^{x})\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+4 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=4 \sin{\left(t \right)}$.

Therefore, $P=e^{4 \sin{\left(t \right)}}$ and $Q=e^{10 \cos{\left(t \right)}}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=4 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(e^{4 \sin{\left(t \right)}})(4 \cos{\left(t \right)})-(e^{10 \cos{\left(t \right)}})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(4 e^{4 \sin{\left(t \right)}} \cos{\left(t \right)} + 10 e^{10 \cos{\left(t \right)}} \sin{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

Use $u=4\sin t$, $\mathrm du=4\cos t\,\mathrm dt$ and $v=10\cos t$, $\mathrm dv=-10\sin t\,\mathrm dt$: $$\int_0^0e^u\,\mathrm du-\int_{10}^{10}e^v\,\mathrm dv=0.$$

## q-127082 / signed-half

Source:

Calculate the flux of the vector field $F(x,y)=x\,i+(x+y)\,j$ across the closed curve $C$ given by $r(t)=3\operatorname{cos}⁡t\,i+5\operatorname{sin}⁡t\,j$ for $t\in [0,2\pi ).$

Replay:

Calculate the flux of the vector field $F(x,y)=(x)\,i+(x + y)\,j$ across the closed curve $C$ given by $r(t)=3 \cos{\left(t \right)}\,i+5 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=3 \cos{\left(t \right)}$, $y=5 \sin{\left(t \right)}$.

Therefore, $P=3 \cos{\left(t \right)}$ and $Q=5 \sin{\left(t \right)} + 3 \cos{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 3 \sin{\left(t \right)}$ and $y\prime(t)=5 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(3 \cos{\left(t \right)})(5 \cos{\left(t \right)})-(5 \sin{\left(t \right)} + 3 \cos{\left(t \right)})(- 3 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(15 \sin^{2}{\left(t \right)} + 9 \sin{\left(t \right)} \cos{\left(t \right)} + 15 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

The integrand is $15+9\sin t\cos t$. Use $u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$ in the second term: $$[15t]_0^{2\pi}+9\int_0^0u\,\mathrm du=30 \pi.$$

Changed radius:

Calculate the flux of the vector field $F(x,y)=(x)\,i+(x + y)\,j$ across the closed curve $C$ given by $r(t)=10 \cos{\left(t \right)}\,i+5 \sin{\left(t \right)}\,j$ for $t\in[0,2\pi)$.

If $F=P\,i+Q\,j$ is a vector field and $C$ is a piecewise-smooth, simple, closed curve, then the outward flux is

$$\oint_C F\cdot n\,\mathrm ds=\oint_C P\,\mathrm dy-Q\,\mathrm dx,$$

where $n$ denotes the outward-pointing unit normal vector to $C$.

Along the curve $C$, we have $x=10 \cos{\left(t \right)}$, $y=5 \sin{\left(t \right)}$.

Therefore, $P=10 \cos{\left(t \right)}$ and $Q=5 \sin{\left(t \right)} + 10 \cos{\left(t \right)}$.

Computing the derivatives gives $x\prime(t)=- 10 \sin{\left(t \right)}$ and $y\prime(t)=5 \cos{\left(t \right)}$.

Finally, evaluate the integral:

$$\begin{aligned}\oint_C F\cdot n\,\mathrm ds&=\int_0^{2\pi}(P y\prime-Q x\prime)\,\mathrm dt\\&=\int_0^{2\pi}\left[(10 \cos{\left(t \right)})(5 \cos{\left(t \right)})-(5 \sin{\left(t \right)} + 10 \cos{\left(t \right)})(- 10 \sin{\left(t \right)})\right]\,\mathrm dt\\&=\int_0^{2\pi}\left(50 \sin^{2}{\left(t \right)} + 100 \sin{\left(t \right)} \cos{\left(t \right)} + 50 \cos^{2}{\left(t \right)}\right)\,\mathrm dt.\end{aligned}$$

The integrand is $50+100\sin t\cos t$. Use $u=\sin t$, $\mathrm du=\cos t\,\mathrm dt$ in the second term: $$[50t]_0^{2\pi}+100\int_0^0u\,\mathrm du=100 \pi.$$