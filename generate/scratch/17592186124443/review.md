# Originals and generated variants

Frozen math basis 1356. Raw captures remain in source.json. Each original below is a public parameterized replay; normalized choice notation is compared as complete vectors.


## Original parameterized raw replay q-35990

Evaluate $∇h(x,y)$ at $(2,3)$ if $h(x,y)=4{x}^{2}-3xy+2{y}^{2}+y.$

- $(7)\text{ }i+(7)\text{ }j$
- $(9)\text{ }i+(-6)\text{ }j$
- $(16)\text{ }i+(12)\text{ }j$
- $(16)\text{ }i+(6)\text{ }j$
- $(9)\text{ }i+(12)\text{ }j$
- $(16)\text{ }i+(12)\text{ }j$
- $(7)\text{ }i+(7)\text{ }j$
- $(9)\text{ }i+(-6)\text{ }j$
- $(9)\text{ }i+(12)\text{ }j$
- $(16)\text{ }i+(6)\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(4{x}^{2}-3xy+2{y}^{2}+y) \\  & =8x-3y+0+0 \\  & =8x-3y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(4{x}^{2}-3xy+2{y}^{2}+y) \\  & =0-3x+4y+1 \\  & =4y-3x+1\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\text{ }i+{h}_{y}(x,y)\text{ }j \\  & =(8x-3y)\text{ }i+(4y-3x+1)\text{ }j \\ ∇h(2,3) & =(8\cdot 2-3\cdot 3)\text{ }i+(4\cdot 3-3\cdot 2+1)\text{ }j \\  & =7\text{ }i+7\text{ }j\end{aligned}
$$


## Generated easy polynomial seed 0

Evaluate $∇h(x,y)$ at $(4,4)$ if $h(x,y)=4{x}^{2}-4xy+1{y}^{2}+y.$

- $(32)\text{ }i+(-8)\text{ }j$
- $(32)\text{ }i+(8)\text{ }j$
- $(16)\text{ }i+(-16)\text{ }j$
- $(16)\text{ }i+(8)\text{ }j$
- $(16)\text{ }i+(-7)\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(4{x}^{2}-4xy+1{y}^{2}+y) \\  & =8x-4y+0+0 \\  & =8x-4y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(4{x}^{2}-4xy+1{y}^{2}+y) \\  & =0-4x+2y+1 \\  & =2y-4x+1\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\text{ }i+{h}_{y}(x,y)\text{ }j \\  & =(8x-4y)\text{ }i+(2y-4x+1)\text{ }j \\ ∇h(4,4) & =(8\cdot 4-4\cdot 4)\text{ }i+(2\cdot 4-4\cdot 4+1)\text{ }j \\  & =16\text{ }i-7\text{ }j\end{aligned}
$$


## Generated easy polynomial seed 1

Evaluate $∇h(x,y)$ at $(1,4)$ if $h(x,y)=2{x}^{2}-5xy+1{y}^{2}+y.$

- $(4)\text{ }i+(8)\text{ }j$
- $(20)\text{ }i+(-5)\text{ }j$
- $(-16)\text{ }i+(4)\text{ }j$
- $(4)\text{ }i+(3)\text{ }j$
- $(20)\text{ }i+(8)\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(2{x}^{2}-5xy+1{y}^{2}+y) \\  & =4x-5y+0+0 \\  & =4x-5y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(2{x}^{2}-5xy+1{y}^{2}+y) \\  & =0-5x+2y+1 \\  & =2y-5x+1\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\text{ }i+{h}_{y}(x,y)\text{ }j \\  & =(4x-5y)\text{ }i+(2y-5x+1)\text{ }j \\ ∇h(1,4) & =(4\cdot 1-5\cdot 4)\text{ }i+(2\cdot 4-5\cdot 1+1)\text{ }j \\  & =-16\text{ }i+4\text{ }j\end{aligned}
$$


## Original parameterized raw replay q-36909

Evaluate $∇f(x,y)$ at $(2,1)$ if $f(x,y)={x}^{2}\sqrt{y+3}.$

- $⟨1,\,8⟩$
- $⟨2,\,0⟩$
- $⟨4,\,\frac{1}{2}⟩$
- $⟨8,\,1⟩$
- $⟨16,\,1⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({x}^{2}\sqrt{y+3}) \\  & =2x\sqrt{y+3} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}({x}^{2}\sqrt{y+3}) \\  & =\frac{{x}^{2}}{2\sqrt{y+3}}.\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & =⟨{f}_{x}(x,y),\,{f}_{y}(x,y)⟩ \\  & =⟨2x\sqrt{y+3},\,\frac{{x}^{2}}{2\sqrt{y+3}}⟩ \\ ∇f(2,1) & =⟨2\cdot 2\sqrt{1+3},\,\frac{{2}^{2}}{2\sqrt{1+3}}⟩ \\  & =⟨8,\,1⟩\end{aligned}
$$


## Generated easy root seed 0

Evaluate $∇f(x,y)$ at $(2,3)$ if $f(x,y)={x}^{2}\sqrt{y+6}.$

- $⟨12,\,- \frac{2}{3}⟩$
- $⟨6,\,\frac{2}{3}⟩$
- $⟨\frac{2}{3},\,12⟩$
- $⟨12,\,\frac{4}{3}⟩$
- $⟨12,\,\frac{2}{3}⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({x}^{2}\sqrt{y+6}) \\  & =2x\sqrt{y+6} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}({x}^{2}\sqrt{y+6}) \\  & =\frac{{x}^{2}}{2\sqrt{y+6}}.\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & =⟨{f}_{x}(x,y),\,{f}_{y}(x,y)⟩ \\  & =⟨2x\sqrt{y+6},\,\frac{{x}^{2}}{2\sqrt{y+6}}⟩ \\ ∇f(2,3) & =⟨2\cdot 2\sqrt{3+6},\,\frac{{2}^{2}}{2\sqrt{3+6}}⟩ \\  & =⟨12,\,\frac{2}{3}⟩\end{aligned}
$$


## Generated easy root seed 1

Evaluate $∇f(x,y)$ at $(-4,-2)$ if $f(x,y)={x}^{2}\sqrt{y+18}.$

- $⟨2,\,-32⟩$
- $⟨-32,\,-2⟩$
- $⟨-16,\,2⟩$
- $⟨-32,\,2⟩$
- $⟨-32,\,4⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({x}^{2}\sqrt{y+18}) \\  & =2x\sqrt{y+18} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}({x}^{2}\sqrt{y+18}) \\  & =\frac{{x}^{2}}{2\sqrt{y+18}}.\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & =⟨{f}_{x}(x,y),\,{f}_{y}(x,y)⟩ \\  & =⟨2x\sqrt{y+18},\,\frac{{x}^{2}}{2\sqrt{y+18}}⟩ \\ ∇f(-4,-2) & =⟨2\cdot (-4)\sqrt{(-2)+18},\,\frac{{(-4)}^{2}}{2\sqrt{(-2)+18}}⟩ \\  & =⟨-32,\,2⟩\end{aligned}
$$


## Original parameterized raw replay q-36910

Given  $g(x,y)=\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{2})$, find $∇g(x,y).$

- $(\frac{1}{x})\text{ }i+(2 y \sin{\left(y \right)} + \frac{1}{y})\text{ }j$
- $(\frac{1}{x})\text{ }i+(- 2 y \sin{\left(y^{2} \right)} + \frac{1}{y})\text{ }j$
- $(x)\text{ }i+(y - 2 \sin{\left(y^{2} \right)})\text{ }j$
- $(\frac{1}{x})\text{ }i+(2 y \left(- \sin{\left(y^{2} \right)} + \frac{1}{y}\right))\text{ }j$
- $(\frac{1}{x})\text{ }i+(\frac{1}{y})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{2})) \\  & =\frac{1}{xy}\cdot y+0 \\  & =\frac{1}{x} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{2})) \\  & =\frac{1}{xy}\cdot x-\operatorname{sin}⁡({y}^{2})\cdot 2y \\  & =\frac{1}{y}-2y\operatorname{sin}⁡({y}^{2})\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & ={g}_{x}(x,y)\text{ }i+{g}_{y}(x,y)\text{ }j \\  & =\frac{1}{x}\text{ }i+(\frac{1}{y}-2y\operatorname{sin}⁡({y}^{2}))\text{ }j\end{aligned}
$$


## Generated easy log_cos seed 0

Given  $g(x,y)=3\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{5})$, find $∇g(x,y).$

- $(\frac{3}{x})\text{ }i+(5 y^{4} \left(- 5 \sin{\left(y^{5} \right)} + \frac{3}{y}\right))\text{ }j$
- $(\frac{3}{x})\text{ }i+(- 25 y^{4} \sin{\left(y^{5} \right)} + \frac{3}{y})\text{ }j$
- $(\frac{3}{x})\text{ }i+(\frac{3}{y})\text{ }j$
- $(\frac{3}{x})\text{ }i+(25 y^{4} \sin{\left(y \right)} + \frac{3}{y})\text{ }j$
- $(3 x)\text{ }i+(3 y - 25 \sin{\left(y^{5} \right)})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(3\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{5})) \\  & =\frac{3}{xy}\cdot y+0 \\  & =\frac{3}{x} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(3\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{5})) \\  & =\frac{3}{xy}\cdot x-5\operatorname{sin}⁡({y}^{5})\cdot 5{y}^{4} \\  & =\frac{3}{y}-25{y}^{4}\operatorname{sin}⁡({y}^{5})\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & ={g}_{x}(x,y)\text{ }i+{g}_{y}(x,y)\text{ }j \\  & =\frac{3}{x}\text{ }i+(\frac{3}{y}-25{y}^{4}\operatorname{sin}⁡({y}^{5}))\text{ }j\end{aligned}
$$


## Generated easy log_cos seed 1

Given  $g(x,y)=\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{6})$, find $∇g(x,y).$

- $(\frac{1}{x})\text{ }i+(\frac{1}{y})\text{ }j$
- $(\frac{1}{x})\text{ }i+(- 30 y^{5} \sin{\left(y^{6} \right)} + \frac{1}{y})\text{ }j$
- $(\frac{1}{x})\text{ }i+(6 y^{5} \left(- 5 \sin{\left(y^{6} \right)} + \frac{1}{y}\right))\text{ }j$
- $(\frac{1}{x})\text{ }i+(30 y^{5} \sin{\left(y \right)} + \frac{1}{y})\text{ }j$
- $(x)\text{ }i+(y - 30 \sin{\left(y^{6} \right)})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{6})) \\  & =\frac{1}{xy}\cdot y+0 \\  & =\frac{1}{x} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡(xy)+5\operatorname{cos}⁡({y}^{6})) \\  & =\frac{1}{xy}\cdot x-5\operatorname{sin}⁡({y}^{6})\cdot 6{y}^{5} \\  & =\frac{1}{y}-30{y}^{5}\operatorname{sin}⁡({y}^{6})\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & ={g}_{x}(x,y)\text{ }i+{g}_{y}(x,y)\text{ }j \\  & =\frac{1}{x}\text{ }i+(\frac{1}{y}-30{y}^{5}\operatorname{sin}⁡({y}^{6}))\text{ }j\end{aligned}
$$


## Original parameterized raw replay q-71350

Given  $f(x,y)=\operatorname{sin}⁡(xy)+{x}^{2}\operatorname{ln}⁡y$, find $∇f(x,y).$

- $(y \cos{\left(x y \right)})\text{ }i+(\frac{x^{2}}{y})\text{ }j$
- $(2 x \ln{\left(y \right)} + x \cos{\left(x y \right)})\text{ }i+(\frac{x^{2}}{y} + y \cos{\left(x y \right)})\text{ }j$
- $(2 x \ln{\left(y \right)} + y \sin{\left(x y \right)})\text{ }i+(\frac{x^{2}}{y} + x \sin{\left(x y \right)})\text{ }j$
- $(2 x \ln{\left(y \right)} + y \cos{\left(x y \right)})\text{ }i+(\frac{x^{2}}{y} + x \cos{\left(x y \right)})\text{ }j$
- $(2 x \ln{\left(y \right)} + x \sin{\left(x y \right)})\text{ }i+(\frac{x^{2}}{y} + y \sin{\left(x y \right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xy)+{x}^{2}\operatorname{ln}⁡y) \\  & =y\operatorname{cos}⁡(xy)+2x\operatorname{ln}⁡y \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xy)+{x}^{2}\operatorname{ln}⁡y) \\  & =x\operatorname{cos}⁡(xy)+{x}^{2}\cdot \frac{1}{y} \\  & =x\operatorname{cos}⁡(xy)+\frac{{x}^{2}}{y}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(y\operatorname{cos}⁡(xy)+2x\operatorname{ln}⁡y)\text{ }i+(x\operatorname{cos}⁡(xy)+\frac{{x}^{2}}{y})\text{ }j\end{aligned}
$$


## Generated easy sin_log seed 0

Given  $f(x,y)=3\operatorname{sin}⁡(xy)+5{x}^{5}\operatorname{ln}⁡y$, find $∇f(x,y).$

- $(25 x^{4} \ln{\left(y \right)} + 3 y \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{5}}{y} + 3 x \cos{\left(x y \right)})\text{ }j$
- $(25 x^{4} \ln{\left(y \right)} + 3 x \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{5}}{y} + 3 y \cos{\left(x y \right)})\text{ }j$
- $(25 x^{4} \ln{\left(y \right)} + 3 x \sin{\left(x y \right)})\text{ }i+(\frac{5 x^{5}}{y} + 3 y \sin{\left(x y \right)})\text{ }j$
- $(3 y \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{5}}{y})\text{ }j$
- $(25 x^{4} \ln{\left(y \right)} + 3 y \sin{\left(x y \right)})\text{ }i+(\frac{5 x^{5}}{y} + 3 x \sin{\left(x y \right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(3\operatorname{sin}⁡(xy)+5{x}^{5}\operatorname{ln}⁡y) \\  & =3y\operatorname{cos}⁡(xy)+25{x}^{4}\operatorname{ln}⁡y \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(3\operatorname{sin}⁡(xy)+5{x}^{5}\operatorname{ln}⁡y) \\  & =3x\operatorname{cos}⁡(xy)+5{x}^{5}\cdot \frac{1}{y} \\  & =3x\operatorname{cos}⁡(xy)+\frac{5{x}^{5}}{y}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(3y\operatorname{cos}⁡(xy)+25{x}^{4}\operatorname{ln}⁡y)\text{ }i+(3x\operatorname{cos}⁡(xy)+\frac{5{x}^{5}}{y})\text{ }j\end{aligned}
$$


## Generated easy sin_log seed 1

Given  $f(x,y)=\operatorname{sin}⁡(xy)+5{x}^{6}\operatorname{ln}⁡y$, find $∇f(x,y).$

- $(30 x^{5} \ln{\left(y \right)} + x \sin{\left(x y \right)})\text{ }i+(\frac{5 x^{6}}{y} + y \sin{\left(x y \right)})\text{ }j$
- $(30 x^{5} \ln{\left(y \right)} + x \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{6}}{y} + y \cos{\left(x y \right)})\text{ }j$
- $(30 x^{5} \ln{\left(y \right)} + y \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{6}}{y} + x \cos{\left(x y \right)})\text{ }j$
- $(y \cos{\left(x y \right)})\text{ }i+(\frac{5 x^{6}}{y})\text{ }j$
- $(30 x^{5} \ln{\left(y \right)} + y \sin{\left(x y \right)})\text{ }i+(\frac{5 x^{6}}{y} + x \sin{\left(x y \right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xy)+5{x}^{6}\operatorname{ln}⁡y) \\  & =y\operatorname{cos}⁡(xy)+30{x}^{5}\operatorname{ln}⁡y \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xy)+5{x}^{6}\operatorname{ln}⁡y) \\  & =x\operatorname{cos}⁡(xy)+5{x}^{6}\cdot \frac{1}{y} \\  & =x\operatorname{cos}⁡(xy)+\frac{5{x}^{6}}{y}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(y\operatorname{cos}⁡(xy)+30{x}^{5}\operatorname{ln}⁡y)\text{ }i+(x\operatorname{cos}⁡(xy)+\frac{5{x}^{6}}{y})\text{ }j\end{aligned}
$$


## Original parameterized raw replay q-36005

Evaluate $∇h(x,y)$ at $(1,1)$ if $h(x,y)=4x\operatorname{arctan}⁡y.$

- $⟨2 \pi ,\,0⟩$
- $⟨1,\,1⟩$
- $⟨\pi ,\,\frac{1}{2}⟩$
- $⟨\frac{\pi }{4},\,\frac{1}{2}⟩$
- $⟨\pi ,\,2⟩$

First, we find the partial derivatives

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(4x\operatorname{arctan}⁡y) \\  & =4\operatorname{arctan}⁡y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(4x\operatorname{arctan}⁡y) \\  & =\frac{4x}{{y}^{2}+1}\end{aligned}
$$

Hence, the gradient is 

$$
\begin{aligned}∇h(x,y) & =⟨{h}_{x}(x,y),\,{h}_{y}(x,y)⟩ \\  & =⟨4\operatorname{arctan}⁡y,\,\frac{4x}{{y}^{2}+1}⟩ \\ ∇h(1,1) & =⟨4\operatorname{arctan}⁡1,\,\frac{4\cdot 1}{{1}^{2}+1}⟩ \\  & =⟨4\cdot \frac{\pi }{4},\,\frac{4}{2}⟩ \\  & =⟨\pi ,\,2⟩.\end{aligned}
$$


## Generated moderate atan_product seed 0

Evaluate $∇h(x,y)$ at $(1,1)$ if $h(x,y)=8x\operatorname{arctan}⁡y.$

- $⟨- 2 \pi ,\,4⟩$
- $⟨\frac{\pi }{4},\,4⟩$
- $⟨4,\,2 \pi ⟩$
- $⟨2 \pi ,\,\frac{1}{2}⟩$
- $⟨2 \pi ,\,4⟩$

First, we find the partial derivatives

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(8x\operatorname{arctan}⁡y) \\  & =8\operatorname{arctan}⁡y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(8x\operatorname{arctan}⁡y) \\  & =\frac{8x}{{y}^{2}+1}\end{aligned}
$$

Hence, the gradient is 

$$
\begin{aligned}∇h(x,y) & =⟨{h}_{x}(x,y),\,{h}_{y}(x,y)⟩ \\  & =⟨8\operatorname{arctan}⁡y,\,\frac{8x}{{y}^{2}+1}⟩ \\ ∇h(1,1) & =⟨8\operatorname{arctan}⁡1,\,\frac{8\cdot 1}{{1}^{2}+1}⟩ \\  & =⟨8\cdot \frac{\pi }{4},\,\frac{8}{2}⟩ \\  & =⟨2 \pi ,\,4⟩.\end{aligned}
$$


## Generated moderate atan_product seed 1

Evaluate $∇h(x,y)$ at $(2,-1)$ if $h(x,y)=3x\operatorname{arctan}⁡y.$

- $⟨3,\,- \frac{3 \pi }{4}⟩$
- $⟨\frac{3 \pi }{4},\,3⟩$
- $⟨- \frac{\pi }{4},\,3⟩$
- $⟨- \frac{3 \pi }{4},\,3⟩$
- $⟨- \frac{3 \pi }{4},\,1⟩$

First, we find the partial derivatives

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(3x\operatorname{arctan}⁡y) \\  & =3\operatorname{arctan}⁡y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(3x\operatorname{arctan}⁡y) \\  & =\frac{3x}{{y}^{2}+1}\end{aligned}
$$

Hence, the gradient is 

$$
\begin{aligned}∇h(x,y) & =⟨{h}_{x}(x,y),\,{h}_{y}(x,y)⟩ \\  & =⟨3\operatorname{arctan}⁡y,\,\frac{3x}{{y}^{2}+1}⟩ \\ ∇h(2,-1) & =⟨3\operatorname{arctan}⁡(-1),\,\frac{3\cdot 2}{{(-1)}^{2}+1}⟩ \\  & =⟨3\cdot (- \frac{\pi }{4}),\,\frac{6}{2}⟩ \\  & =⟨- \frac{3 \pi }{4},\,3⟩.\end{aligned}
$$


## Original parameterized raw replay q-36009

Evaluate the gradient of $g(x,y)$ at the point $(\frac{1}{2},0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

- $⟨8,\,0⟩$
- $⟨\frac{1}{2},\,\frac{1}{2}⟩$
- $⟨4,\,0⟩$
- $⟨8,\,\frac{1}{2}⟩$
- $⟨\frac{1}{2},\,0⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2x}{{x}^{2}+{y}^{2}} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & =⟨{g}_{x}(x,y),\,{g}_{y}(x,y)⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{2y}{{x}^{2}+{y}^{2}}⟩ \\  & =\frac{2}{{x}^{2}+{y}^{2}}⟨x,\,y⟩ \\ ∇g(\frac{1}{2},\,0) & =\frac{2}{{(\frac{1}{2})}^{2}+{0}^{2}}⟨\frac{1}{2},\,0⟩ \\  & =\frac{2}{\,\frac{1}{4}}⟨\frac{1}{2},\,0⟩ \\  & =8⟨\frac{1}{2},\,0⟩ \\  & =⟨4,\,0⟩\end{aligned}
$$


## Generated moderate radial_log seed 0

Evaluate the gradient of $g(x,y)$ at the point $(\frac{1}{7},0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

- $⟨-14,\,0⟩$
- $⟨7,\,0⟩$
- $⟨0,\,14⟩$
- $⟨28,\,0⟩$
- $⟨14,\,0⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2x}{{x}^{2}+{y}^{2}} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & =⟨{g}_{x}(x,y),\,{g}_{y}(x,y)⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{2y}{{x}^{2}+{y}^{2}}⟩ \\  & =\frac{2}{{x}^{2}+{y}^{2}}⟨x,\,y⟩ \\ ∇g(\frac{1}{7},\,0) & =\frac{2}{{(\frac{1}{7})}^{2}+{0}^{2}}⟨\frac{1}{7},\,0⟩ \\  & =\frac{2}{\,\frac{1}{49}}⟨\frac{1}{7},\,0⟩ \\  & =98⟨\frac{1}{7},\,0⟩ \\  & =⟨14,\,0⟩\end{aligned}
$$


## Generated moderate radial_log seed 1

Evaluate the gradient of $g(x,y)$ at the point $(- \frac{5}{2},0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

- $⟨0,\,- \frac{4}{5}⟩$
- $⟨\frac{4}{5},\,0⟩$
- $⟨- \frac{2}{5},\,0⟩$
- $⟨- \frac{4}{5},\,0⟩$
- $⟨- \frac{8}{5},\,0⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2x}{{x}^{2}+{y}^{2}} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & =⟨{g}_{x}(x,y),\,{g}_{y}(x,y)⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{2y}{{x}^{2}+{y}^{2}}⟩ \\  & =\frac{2}{{x}^{2}+{y}^{2}}⟨x,\,y⟩ \\ ∇g(- \frac{5}{2},\,0) & =\frac{2}{{(- \frac{5}{2})}^{2}+{0}^{2}}⟨- \frac{5}{2},\,0⟩ \\  & =\frac{2}{\,\frac{25}{4}}⟨- \frac{5}{2},\,0⟩ \\  & =\frac{8}{25}⟨- \frac{5}{2},\,0⟩ \\  & =⟨- \frac{4}{5},\,0⟩\end{aligned}
$$


## Original parameterized raw replay q-127650

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{x}),$ find $∇h(x,y).$

- $(- \frac{y^{2}}{x^{2} + y^{2}})\text{ }i+(\frac{x^{2}}{x^{2} + y^{2}})\text{ }j$
- $(\frac{x}{x^{2} + y^{2}})\text{ }i+(- \frac{y}{x^{2} + y^{2}})\text{ }j$
- $(- \frac{x}{x^{2} + y^{2}})\text{ }i+(\frac{y}{x^{2} + y^{2}})\text{ }j$
- $(\frac{y}{x^{2} \left(1 + \frac{y^{2}}{x^{2}}\right)})\text{ }i+(- \frac{1}{x \left(1 + \frac{y^{2}}{x^{2}}\right)})\text{ }j$
- $(- \frac{y}{x^{2} \left(1 + \frac{y^{2}}{x^{2}}\right)})\text{ }i+(\frac{1}{x \left(1 + \frac{y^{2}}{x^{2}}\right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(\frac{y}{x})) \\  & =\frac{1}{1+{(\frac{y}{x})}^{2}}\cdot (-\frac{y}{{x}^{2}}) \\  & =\frac{{x}^{2}}{{x}^{2}+{y}^{2}}\cdot (-\frac{y}{{x}^{2}}) \\  & =-\frac{y}{{x}^{2}+{y}^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{arctan}⁡(\frac{y}{x})) \\  & =\frac{1}{1+{(\frac{y}{x})}^{2}}\cdot (\frac{1}{x}) \\  & =\frac{{x}^{2}}{{x}^{2}+{y}^{2}}\cdot \frac{1}{x} \\  & =\frac{x}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =-\frac{y}{{x}^{2}+{y}^{2}}\,i+\frac{x}{{x}^{2}+{y}^{2}}\,j.\end{aligned}
$$


## Generated moderate atan_ratio seed 0

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{\frac{6}{5}x}),$ find $∇h(x,y).$

- $(\frac{5 y}{6 x^{2} \left(1 + \frac{25 y^{2}}{36 x^{2}}\right)})\text{ }i+(- \frac{5}{6 x \left(1 + \frac{25 y^{2}}{36 x^{2}}\right)})\text{ }j$
- $(- \frac{6 y^{2}}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }i+(\frac{6 x^{2}}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(\frac{6 x}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }i+(- \frac{6 y}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(- \frac{6 x}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }i+(\frac{6 y}{5 \left(\frac{36 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(- \frac{5 y}{6 x^{2} \left(1 + \frac{25 y^{2}}{36 x^{2}}\right)})\text{ }i+(\frac{5}{6 x \left(1 + \frac{25 y^{2}}{36 x^{2}}\right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(\frac{y}{\frac{6}{5}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{6}{5}x})}^{2}}\cdot (-\frac{y}{\frac{6}{5}{x}^{2}}) \\  & =\frac{\frac{36}{25}{x}^{2}}{{\frac{6}{5}x}^{2}+{y}^{2}}\cdot (-\frac{y}{\frac{6}{5}{x}^{2}}) \\  & =-\frac{\frac{6}{5}y}{{\frac{6}{5}x}^{2}+{y}^{2}} \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{arctan}⁡(\frac{y}{\frac{6}{5}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{6}{5}x})}^{2}}\cdot (\frac{1}{\frac{6}{5}x}) \\  & =\frac{\frac{36}{25}{x}^{2}}{{\frac{6}{5}x}^{2}+{y}^{2}}\cdot \frac{1}{\frac{6}{5}x} \\  & =\frac{\frac{6}{5}x}{{\frac{6}{5}x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\,i+{h}_{y}(x,y)\,j \\  & =-\frac{\frac{6}{5}y}{{\frac{6}{5}x}^{2}+{y}^{2}}\,i+\frac{\frac{6}{5}x}{{\frac{6}{5}x}^{2}+{y}^{2}}\,j.\end{aligned}
$$


## Generated moderate atan_ratio seed 1

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{\frac{2}{5}x}),$ find $∇h(x,y).$

- $(- \frac{2 y^{2}}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }i+(\frac{2 x^{2}}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(- \frac{5 y}{2 x^{2} \left(1 + \frac{25 y^{2}}{4 x^{2}}\right)})\text{ }i+(\frac{5}{2 x \left(1 + \frac{25 y^{2}}{4 x^{2}}\right)})\text{ }j$
- $(\frac{2 x}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }i+(- \frac{2 y}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(- \frac{2 x}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }i+(\frac{2 y}{5 \left(\frac{4 x^{2}}{25} + y^{2}\right)})\text{ }j$
- $(\frac{5 y}{2 x^{2} \left(1 + \frac{25 y^{2}}{4 x^{2}}\right)})\text{ }i+(- \frac{5}{2 x \left(1 + \frac{25 y^{2}}{4 x^{2}}\right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(\frac{y}{\frac{2}{5}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{2}{5}x})}^{2}}\cdot (-\frac{y}{\frac{2}{5}{x}^{2}}) \\  & =\frac{\frac{4}{25}{x}^{2}}{{\frac{2}{5}x}^{2}+{y}^{2}}\cdot (-\frac{y}{\frac{2}{5}{x}^{2}}) \\  & =-\frac{\frac{2}{5}y}{{\frac{2}{5}x}^{2}+{y}^{2}} \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{arctan}⁡(\frac{y}{\frac{2}{5}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{2}{5}x})}^{2}}\cdot (\frac{1}{\frac{2}{5}x}) \\  & =\frac{\frac{4}{25}{x}^{2}}{{\frac{2}{5}x}^{2}+{y}^{2}}\cdot \frac{1}{\frac{2}{5}x} \\  & =\frac{\frac{2}{5}x}{{\frac{2}{5}x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\,i+{h}_{y}(x,y)\,j \\  & =-\frac{\frac{2}{5}y}{{\frac{2}{5}x}^{2}+{y}^{2}}\,i+\frac{\frac{2}{5}x}{{\frac{2}{5}x}^{2}+{y}^{2}}\,j.\end{aligned}
$$


## Original parameterized raw replay q-35988

Given $f(x, y) = \frac{3x + 2y}{x - y}$, find $∇f(x, y)$.

- $(\frac{5 y}{\left(x - y\right)^{2}})\text{ }i+(\frac{5 x}{\left(x - y\right)^{2}})\text{ }j$
- $(- \frac{5 x}{\left(x - y\right)^{2}})\text{ }i+(\frac{5 y}{\left(x - y\right)^{2}})\text{ }j$
- $(\frac{3}{x - y} - \frac{3 x + 2 y}{\left(x - y\right)^{2}})\text{ }i+(\frac{2}{x - y} + \frac{3 x + 2 y}{\left(x - y\right)^{2}})\text{ }j$
- $(- 5 y)\text{ }i+(5 x)\text{ }j$
- $(- 5 x)\text{ }i+(5 y)\text{ }j$

[Worked solution absent in raw source.]


## Generated moderate quotient seed 0

Given $f(x, y) = \frac{7x + 7y}{x - \frac{1}{6}y}$, find $∇f(x, y)$.

- $(\frac{7}{x - \frac{y}{6}} - \frac{7 x + 7 y}{\left(x - \frac{y}{6}\right)^{2}})\text{ }i+(\frac{7}{x - \frac{y}{6}} + \frac{7 x + 7 y}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }j$
- $(- \frac{49 y}{6})\text{ }i+(\frac{49 x}{6})\text{ }j$
- $(- \frac{49 x}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }i+(\frac{49 y}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }j$
- $(- \frac{49 x}{6})\text{ }i+(\frac{49 y}{6})\text{ }j$
- $(\frac{49 y}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }i+(\frac{49 x}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{7 x + 7 y}{x - \frac{y}{6}}) \\  & =\frac{(7)(x - \frac{y}{6})-(7 x + 7 y)(1)}{(x - \frac{y}{6})^{2}} \\  & =- \frac{294 y}{\left(6 x - y\right)^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\frac{7 x + 7 y}{x - \frac{y}{6}}) \\  & =\frac{(7)(x - \frac{y}{6})-(7 x + 7 y)(- \frac{1}{6})}{(x - \frac{y}{6})^{2}} \\  & =\frac{294 x}{\left(6 x - y\right)^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(\frac{7}{x - \frac{y}{6}} - \frac{7 x + 7 y}{\left(x - \frac{y}{6}\right)^{2}})\text{ }i+(\frac{7}{x - \frac{y}{6}} + \frac{7 x + 7 y}{6 \left(x - \frac{y}{6}\right)^{2}})\text{ }j\end{aligned}
$$


## Generated moderate quotient seed 1

Given $f(x, y) = \frac{3x + 2y}{x - \frac{3}{4}y}$, find $∇f(x, y)$.

- $(- \frac{17 y}{4})\text{ }i+(\frac{17 x}{4})\text{ }j$
- $(\frac{17 y}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }i+(\frac{17 x}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }j$
- $(- \frac{17 x}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }i+(\frac{17 y}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }j$
- $(- \frac{17 x}{4})\text{ }i+(\frac{17 y}{4})\text{ }j$
- $(\frac{3}{x - \frac{3 y}{4}} - \frac{3 x + 2 y}{\left(x - \frac{3 y}{4}\right)^{2}})\text{ }i+(\frac{2}{x - \frac{3 y}{4}} + \frac{3 \left(3 x + 2 y\right)}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{3 x + 2 y}{x - \frac{3 y}{4}}) \\  & =\frac{(3)(x - \frac{3 y}{4})-(3 x + 2 y)(1)}{(x - \frac{3 y}{4})^{2}} \\  & =- \frac{68 y}{\left(4 x - 3 y\right)^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\frac{3 x + 2 y}{x - \frac{3 y}{4}}) \\  & =\frac{(2)(x - \frac{3 y}{4})-(3 x + 2 y)(- \frac{3}{4})}{(x - \frac{3 y}{4})^{2}} \\  & =\frac{68 x}{\left(4 x - 3 y\right)^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(\frac{3}{x - \frac{3 y}{4}} - \frac{3 x + 2 y}{\left(x - \frac{3 y}{4}\right)^{2}})\text{ }i+(\frac{2}{x - \frac{3 y}{4}} + \frac{3 \left(3 x + 2 y\right)}{4 \left(x - \frac{3 y}{4}\right)^{2}})\text{ }j\end{aligned}
$$


## Original parameterized raw replay q-168115

Find the direction of the greatest rate of expansion of the fluid at the point $(1,1).$ Do not normalize the answer.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The required direction is $∇(\text{div}\,V)\,{|}_{(1,\,1)}=⟨$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$⟩.$

- $4$
- $2$

In part 2, we found that

$$
\begin{aligned}\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(1,\,1)} & =4 \\ \frac{∂}{∂y}(\text{div}\,V)\,{|}_{(1,\,1)} & =2\end{aligned}
$$

Therefore, the gradient at $(1,1)$ is the following:

$$
\begin{aligned}∇(\text{div}\,V)\,{|}_{(1,\,1)} & =\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(1,\,1)}\,i+\frac{∂}{∂y}(\text{div}\,V)\,{|}_{(1,\,1)}\,j \\  & =4\,i+2\,j \\  & =⟨4,\,2⟩\end{aligned}
$$


## Generated moderate components seed 0

At $(-4,0)$, the scalar expansion rate $E(x,y)$ has partial derivatives $E_x=3$ and $E_y=5$. Find its gradient. Do not normalize the answer.

$∇E=⟨$ {{field-1}} $,$ {{field-2}} $⟩.$

- $3$
- $5$

The gradient is the vector of the supplied partial derivatives:

$$
\begin{aligned}∇E & =E_x\,i+E_y\,j \\  & =3\,i+5\,j \\  & =⟨3,\,5⟩\end{aligned}
$$


## Generated moderate components seed 1

At $(0,-3)$, the scalar expansion rate $E(x,y)$ has partial derivatives $E_x=-4$ and $E_y=-5$. Find its gradient. Do not normalize the answer.

$∇E=⟨$ {{field-1}} $,$ {{field-2}} $⟩.$

- $-4$
- $-5$

The gradient is the vector of the supplied partial derivatives:

$$
\begin{aligned}∇E & =E_x\,i+E_y\,j \\  & =-4\,i-5\,j \\  & =⟨-4,\,-5⟩\end{aligned}
$$


## Generated hard hard_quotient seed 0

Evaluate $∇f(x,y)$ at $(1,3)$ if $f(x,y)=\frac{x^{2} y + 4 y^{2}}{x + 4 y}.$

- $(\frac{3}{13})\text{ }i+(1)\text{ }j$
- $(\frac{9}{13})\text{ }i+(1)\text{ }j$
- $(\frac{6}{13})\text{ }i+(\frac{25}{13})\text{ }j$
- $(\frac{3}{13})\text{ }i+(\frac{37}{13})\text{ }j$
- $(1)\text{ }i+(\frac{3}{13})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{x^{2} y + 4 y^{2}}{x + 4 y}) \\  & =\frac{(2 x y)(x + 4 y)-(x^{2} y + 4 y^{2})(1)}{(x + 4 y)^{2}} \\  & =\frac{y \left(x^{2} + 8 x y - 4 y\right)}{\left(x + 4 y\right)^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\frac{x^{2} y + 4 y^{2}}{x + 4 y}) \\  & =\frac{(x^{2} + 8 y)(x + 4 y)-(x^{2} y + 4 y^{2})(4)}{(x + 4 y)^{2}} \\  & =\frac{x^{3} + 8 x y + 16 y^{2}}{\left(x + 4 y\right)^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(\frac{2 x y}{x + 4 y} - \frac{x^{2} y + 4 y^{2}}{\left(x + 4 y\right)^{2}})\text{ }i+(\frac{x^{2} + 8 y}{x + 4 y} - \frac{4 \left(x^{2} y + 4 y^{2}\right)}{\left(x + 4 y\right)^{2}})\text{ }j \\ ∇f(1,3) & =(\frac{2 (1) (3)}{(1) + 4 (3)} - \frac{(1)^{2} (3) + 4 (3)^{2}}{\left((1) + 4 (3)\right)^{2}})\text{ }i+(\frac{(1)^{2} + 8 (3)}{(1) + 4 (3)} - \frac{4 \left((1)^{2} (3) + 4 (3)^{2}\right)}{\left((1) + 4 (3)\right)^{2}})\text{ }j \\  & =(\frac{3}{13})\text{ }i+(1)\text{ }j\end{aligned}
$$


## Generated hard hard_quotient seed 1

Evaluate $∇f(x,y)$ at $(3,1)$ if $f(x,y)=\frac{x^{2} y + 2 y^{2}}{x + y}.$

- $(\frac{13}{16})\text{ }i+(\frac{41}{16})\text{ }j$
- $(\frac{35}{16})\text{ }i+(\frac{41}{16})\text{ }j$
- $(\frac{3}{2})\text{ }i+(\frac{13}{4})\text{ }j$
- $(\frac{41}{16})\text{ }i+(\frac{13}{16})\text{ }j$
- $(\frac{13}{16})\text{ }i+(\frac{63}{16})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{x^{2} y + 2 y^{2}}{x + y}) \\  & =\frac{(2 x y)(x + y)-(x^{2} y + 2 y^{2})(1)}{(x + y)^{2}} \\  & =\frac{y \left(x^{2} + 2 x y - 2 y\right)}{\left(x + y\right)^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\frac{x^{2} y + 2 y^{2}}{x + y}) \\  & =\frac{(x^{2} + 4 y)(x + y)-(x^{2} y + 2 y^{2})(1)}{(x + y)^{2}} \\  & =\frac{x^{3} + 4 x y + 2 y^{2}}{\left(x + y\right)^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(\frac{2 x y}{x + y} - \frac{x^{2} y + 2 y^{2}}{\left(x + y\right)^{2}})\text{ }i+(\frac{x^{2} + 4 y}{x + y} - \frac{x^{2} y + 2 y^{2}}{\left(x + y\right)^{2}})\text{ }j \\ ∇f(3,1) & =(\frac{2 (3) (1)}{(3) + (1)} - \frac{(3)^{2} (1) + 2 (1)^{2}}{\left((3) + (1)\right)^{2}})\text{ }i+(\frac{(3)^{2} + 4 (1)}{(3) + (1)} - \frac{(3)^{2} (1) + 2 (1)^{2}}{\left((3) + (1)\right)^{2}})\text{ }j \\  & =(\frac{13}{16})\text{ }i+(\frac{41}{16})\text{ }j\end{aligned}
$$


## Generated raw evidence easy polynomial seed 30

Evaluate $∇h(x,y)$ at $(2,3)$ if $h(x,y)=5{x}^{2}-3xy+5{y}^{2}-2y.$

- $(11)\text{ }i+(22)\text{ }j$
- $(20)\text{ }i+(24)\text{ }j$
- $(9)\text{ }i+(-6)\text{ }j$
- $(9)\text{ }i+(30)\text{ }j$
- $(20)\text{ }i+(30)\text{ }j$
- $(9)\text{ }i+(-6)\text{ }j$
- $(11)\text{ }i+(22)\text{ }j$
- $(20)\text{ }i+(24)\text{ }j$
- $(9)\text{ }i+(30)\text{ }j$
- $(20)\text{ }i+(30)\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(5{x}^{2}-3xy+5{y}^{2}-2y) \\  & =10x-3y+0+0 \\  & =10x-3y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(5{x}^{2}-3xy+5{y}^{2}-2y) \\  & =0-3x+10y-2 \\  & =10y-3x-2\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\text{ }i+{h}_{y}(x,y)\text{ }j \\  & =(10x-3y)\text{ }i+(10y-3x-2)\text{ }j \\ ∇h(2,3) & =(10\cdot 2-3\cdot 3)\text{ }i+(10\cdot 3-3\cdot 2-2)\text{ }j \\  & =11\text{ }i+22\text{ }j\end{aligned}
$$


## Generated raw evidence easy polynomial seed 31

Evaluate $∇h(x,y)$ at $(2,2)$ if $h(x,y)=2{x}^{2}-1xy+5{y}^{2}-1y.$

- $(2)\text{ }i+(-2)\text{ }j$
- $(6)\text{ }i+(17)\text{ }j$
- $(2)\text{ }i+(20)\text{ }j$
- $(8)\text{ }i+(18)\text{ }j$
- $(8)\text{ }i+(20)\text{ }j$
- $(8)\text{ }i+(20)\text{ }j$
- $(2)\text{ }i+(-2)\text{ }j$
- $(6)\text{ }i+(17)\text{ }j$
- $(2)\text{ }i+(20)\text{ }j$
- $(8)\text{ }i+(18)\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(2{x}^{2}-1xy+5{y}^{2}-1y) \\  & =4x-1y+0+0 \\  & =4x-1y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(2{x}^{2}-1xy+5{y}^{2}-1y) \\  & =0-1x+10y-1 \\  & =10y-1x-1\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y) & ={h}_{x}(x,y)\text{ }i+{h}_{y}(x,y)\text{ }j \\  & =(4x-1y)\text{ }i+(10y-1x-1)\text{ }j \\ ∇h(2,2) & =(4\cdot 2-1\cdot 2)\text{ }i+(10\cdot 2-1\cdot 2-1)\text{ }j \\  & =6\text{ }i+17\text{ }j\end{aligned}
$$


## Generated raw evidence easy root seed 30

Evaluate $∇f(x,y)$ at $(3,1)$ if $f(x,y)={x}^{2}\sqrt{y+8}.$

- $⟨\frac{3}{2},\,18⟩$
- $⟨18,\,\frac{3}{2}⟩$
- $⟨36,\,\frac{3}{2}⟩$
- $⟨3,\,0⟩$
- $⟨9,\,\frac{3}{4}⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({x}^{2}\sqrt{y+8}) \\  & =2x\sqrt{y+8} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}({x}^{2}\sqrt{y+8}) \\  & =\frac{{x}^{2}}{2\sqrt{y+8}}.\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & =⟨{f}_{x}(x,y),\,{f}_{y}(x,y)⟩ \\  & =⟨2x\sqrt{y+8},\,\frac{{x}^{2}}{2\sqrt{y+8}}⟩ \\ ∇f(3,1) & =⟨2\cdot 3\sqrt{1+8},\,\frac{{3}^{2}}{2\sqrt{1+8}}⟩ \\  & =⟨18,\,\frac{3}{2}⟩\end{aligned}
$$


## Generated raw evidence easy root seed 31

Evaluate $∇f(x,y)$ at $(-4,-3)$ if $f(x,y)={x}^{2}\sqrt{y+12}.$

- $⟨-24,\,\frac{8}{3}⟩$
- $⟨-12,\,\frac{4}{3}⟩$
- $⟨\frac{8}{3},\,-24⟩$
- $⟨-4,\,0⟩$
- $⟨-48,\,\frac{8}{3}⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({x}^{2}\sqrt{y+12}) \\  & =2x\sqrt{y+12} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}({x}^{2}\sqrt{y+12}) \\  & =\frac{{x}^{2}}{2\sqrt{y+12}}.\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & =⟨{f}_{x}(x,y),\,{f}_{y}(x,y)⟩ \\  & =⟨2x\sqrt{y+12},\,\frac{{x}^{2}}{2\sqrt{y+12}}⟩ \\ ∇f(-4,-3) & =⟨2\cdot (-4)\sqrt{(-3)+12},\,\frac{{(-4)}^{2}}{2\sqrt{(-3)+12}}⟩ \\  & =⟨-24,\,\frac{8}{3}⟩\end{aligned}
$$


## Generated raw evidence easy log_cos seed 30

Given  $g(x,y)=5\operatorname{ln}⁡(xy)+2\operatorname{cos}⁡({y}^{4})$, find $∇g(x,y).$

- $(\frac{5}{x})\text{ }i+(- 8 y^{3} \sin{\left(y^{4} \right)} + \frac{5}{y})\text{ }j$
- $(\frac{5}{x})\text{ }i+(\frac{5}{y})\text{ }j$
- $(\frac{5}{x})\text{ }i+(8 y^{3} \sin{\left(y \right)} + \frac{5}{y})\text{ }j$
- $(5 x)\text{ }i+(5 y - 8 \sin{\left(y^{4} \right)})\text{ }j$
- $(\frac{5}{x})\text{ }i+(4 y^{3} \left(- 2 \sin{\left(y^{4} \right)} + \frac{5}{y}\right))\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(5\operatorname{ln}⁡(xy)+2\operatorname{cos}⁡({y}^{4})) \\  & =\frac{5}{xy}\cdot y+0 \\  & =\frac{5}{x} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(5\operatorname{ln}⁡(xy)+2\operatorname{cos}⁡({y}^{4})) \\  & =\frac{5}{xy}\cdot x-2\operatorname{sin}⁡({y}^{4})\cdot 4{y}^{3} \\  & =\frac{5}{y}-8{y}^{3}\operatorname{sin}⁡({y}^{4})\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & ={g}_{x}(x,y)\text{ }i+{g}_{y}(x,y)\text{ }j \\  & =\frac{5}{x}\text{ }i+(\frac{5}{y}-8{y}^{3}\operatorname{sin}⁡({y}^{4}))\text{ }j\end{aligned}
$$


## Generated raw evidence easy log_cos seed 31

Given  $g(x,y)=\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{5})$, find $∇g(x,y).$

- $(\frac{1}{x})\text{ }i+(- 5 y^{4} \sin{\left(y^{5} \right)} + \frac{1}{y})\text{ }j$
- $(\frac{1}{x})\text{ }i+(5 y^{4} \sin{\left(y \right)} + \frac{1}{y})\text{ }j$
- $(\frac{1}{x})\text{ }i+(5 y^{4} \left(- \sin{\left(y^{5} \right)} + \frac{1}{y}\right))\text{ }j$
- $(\frac{1}{x})\text{ }i+(\frac{1}{y})\text{ }j$
- $(x)\text{ }i+(y - 5 \sin{\left(y^{5} \right)})\text{ }j$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{5})) \\  & =\frac{1}{xy}\cdot y+0 \\  & =\frac{1}{x} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{5})) \\  & =\frac{1}{xy}\cdot x-\operatorname{sin}⁡({y}^{5})\cdot 5{y}^{4} \\  & =\frac{1}{y}-5{y}^{4}\operatorname{sin}⁡({y}^{5})\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & ={g}_{x}(x,y)\text{ }i+{g}_{y}(x,y)\text{ }j \\  & =\frac{1}{x}\text{ }i+(\frac{1}{y}-5{y}^{4}\operatorname{sin}⁡({y}^{5}))\text{ }j\end{aligned}
$$


## Generated raw evidence easy sin_log seed 30

Given  $f(x,y)=5\operatorname{sin}⁡(xy)+2{x}^{4}\operatorname{ln}⁡y$, find $∇f(x,y).$

- $(8 x^{3} \ln{\left(y \right)} + 5 x \cos{\left(x y \right)})\text{ }i+(\frac{2 x^{4}}{y} + 5 y \cos{\left(x y \right)})\text{ }j$
- $(8 x^{3} \ln{\left(y \right)} + 5 x \sin{\left(x y \right)})\text{ }i+(\frac{2 x^{4}}{y} + 5 y \sin{\left(x y \right)})\text{ }j$
- $(5 y \cos{\left(x y \right)})\text{ }i+(\frac{2 x^{4}}{y})\text{ }j$
- $(8 x^{3} \ln{\left(y \right)} + 5 y \sin{\left(x y \right)})\text{ }i+(\frac{2 x^{4}}{y} + 5 x \sin{\left(x y \right)})\text{ }j$
- $(8 x^{3} \ln{\left(y \right)} + 5 y \cos{\left(x y \right)})\text{ }i+(\frac{2 x^{4}}{y} + 5 x \cos{\left(x y \right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(5\operatorname{sin}⁡(xy)+2{x}^{4}\operatorname{ln}⁡y) \\  & =5y\operatorname{cos}⁡(xy)+8{x}^{3}\operatorname{ln}⁡y \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(5\operatorname{sin}⁡(xy)+2{x}^{4}\operatorname{ln}⁡y) \\  & =5x\operatorname{cos}⁡(xy)+2{x}^{4}\cdot \frac{1}{y} \\  & =5x\operatorname{cos}⁡(xy)+\frac{2{x}^{4}}{y}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(5y\operatorname{cos}⁡(xy)+8{x}^{3}\operatorname{ln}⁡y)\text{ }i+(5x\operatorname{cos}⁡(xy)+\frac{2{x}^{4}}{y})\text{ }j\end{aligned}
$$


## Generated raw evidence easy sin_log seed 31

Given  $f(x,y)=\operatorname{sin}⁡(xy)+{x}^{5}\operatorname{ln}⁡y$, find $∇f(x,y).$

- $(5 x^{4} \ln{\left(y \right)} + x \cos{\left(x y \right)})\text{ }i+(\frac{x^{5}}{y} + y \cos{\left(x y \right)})\text{ }j$
- $(y \cos{\left(x y \right)})\text{ }i+(\frac{x^{5}}{y})\text{ }j$
- $(5 x^{4} \ln{\left(y \right)} + y \cos{\left(x y \right)})\text{ }i+(\frac{x^{5}}{y} + x \cos{\left(x y \right)})\text{ }j$
- $(5 x^{4} \ln{\left(y \right)} + x \sin{\left(x y \right)})\text{ }i+(\frac{x^{5}}{y} + y \sin{\left(x y \right)})\text{ }j$
- $(5 x^{4} \ln{\left(y \right)} + y \sin{\left(x y \right)})\text{ }i+(\frac{x^{5}}{y} + x \sin{\left(x y \right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xy)+{x}^{5}\operatorname{ln}⁡y) \\  & =y\operatorname{cos}⁡(xy)+5{x}^{4}\operatorname{ln}⁡y \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xy)+{x}^{5}\operatorname{ln}⁡y) \\  & =x\operatorname{cos}⁡(xy)+{x}^{5}\cdot \frac{1}{y} \\  & =x\operatorname{cos}⁡(xy)+\frac{{x}^{5}}{y}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j \\  & =(y\operatorname{cos}⁡(xy)+5{x}^{4}\operatorname{ln}⁡y)\text{ }i+(x\operatorname{cos}⁡(xy)+\frac{{x}^{5}}{y})\text{ }j\end{aligned}
$$


## Generated raw evidence moderate atan_product seed 30

Evaluate $∇h(x,y)$ at $(4,1)$ if $h(x,y)=6x\operatorname{arctan}⁡y.$

- $⟨4,\,1⟩$
- $⟨\frac{3 \pi }{2},\,12⟩$
- $⟨3 \pi ,\,0⟩$
- $⟨\frac{3 \pi }{2},\,2⟩$
- $⟨\frac{\pi }{4},\,2⟩$

First, we find the partial derivatives

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(6x\operatorname{arctan}⁡y) \\  & =6\operatorname{arctan}⁡y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(6x\operatorname{arctan}⁡y) \\  & =\frac{6x}{{y}^{2}+1}\end{aligned}
$$

Hence, the gradient is 

$$
\begin{aligned}∇h(x,y) & =⟨{h}_{x}(x,y),\,{h}_{y}(x,y)⟩ \\  & =⟨6\operatorname{arctan}⁡y,\,\frac{6x}{{y}^{2}+1}⟩ \\ ∇h(4,1) & =⟨6\operatorname{arctan}⁡1,\,\frac{6\cdot 4}{{1}^{2}+1}⟩ \\  & =⟨6\cdot \frac{\pi }{4},\,\frac{24}{2}⟩ \\  & =⟨\frac{3 \pi }{2},\,12⟩.\end{aligned}
$$


## Generated raw evidence moderate atan_product seed 31

Evaluate $∇h(x,y)$ at $(1,-1)$ if $h(x,y)=2x\operatorname{arctan}⁡y.$

- $⟨- \frac{\pi }{4},\,\frac{1}{2}⟩$
- $⟨- \frac{\pi }{2},\,\frac{1}{2}⟩$
- $⟨- \pi ,\,0⟩$
- $⟨1,\,-1⟩$
- $⟨- \frac{\pi }{2},\,1⟩$

First, we find the partial derivatives

$$
\begin{aligned}{h}_{x}(x,y) & =\frac{∂}{∂x}(2x\operatorname{arctan}⁡y) \\  & =2\operatorname{arctan}⁡y \\ {h}_{y}(x,y) & =\frac{∂}{∂y}(2x\operatorname{arctan}⁡y) \\  & =\frac{2x}{{y}^{2}+1}\end{aligned}
$$

Hence, the gradient is 

$$
\begin{aligned}∇h(x,y) & =⟨{h}_{x}(x,y),\,{h}_{y}(x,y)⟩ \\  & =⟨2\operatorname{arctan}⁡y,\,\frac{2x}{{y}^{2}+1}⟩ \\ ∇h(1,-1) & =⟨2\operatorname{arctan}⁡(-1),\,\frac{2\cdot 1}{{(-1)}^{2}+1}⟩ \\  & =⟨2\cdot (- \frac{\pi }{4}),\,\frac{2}{2}⟩ \\  & =⟨- \frac{\pi }{2},\,1⟩.\end{aligned}
$$


## Generated raw evidence moderate radial_log seed 30

Evaluate the gradient of $g(x,y)$ at the point $(\frac{3}{5},0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

- $⟨\frac{3}{5},\,\frac{3}{5}⟩$
- $⟨\frac{3}{5},\,0⟩$
- $⟨\frac{50}{9},\,0⟩$
- $⟨\frac{10}{3},\,0⟩$
- $⟨\frac{50}{9},\,\frac{3}{5}⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2x}{{x}^{2}+{y}^{2}} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & =⟨{g}_{x}(x,y),\,{g}_{y}(x,y)⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{2y}{{x}^{2}+{y}^{2}}⟩ \\  & =\frac{2}{{x}^{2}+{y}^{2}}⟨x,\,y⟩ \\ ∇g(\frac{3}{5},\,0) & =\frac{2}{{(\frac{3}{5})}^{2}+{0}^{2}}⟨\frac{3}{5},\,0⟩ \\  & =\frac{2}{\,\frac{9}{25}}⟨\frac{3}{5},\,0⟩ \\  & =\frac{50}{9}⟨\frac{3}{5},\,0⟩ \\  & =⟨\frac{10}{3},\,0⟩\end{aligned}
$$


## Generated raw evidence moderate radial_log seed 31

Evaluate the gradient of $g(x,y)$ at the point $(-1,0)$ if $g(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}).$

- $⟨-1,\,-1⟩$
- $⟨2,\,0⟩$
- $⟨2,\,-1⟩$
- $⟨-1,\,0⟩$
- $⟨-2,\,0⟩$

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2x}{{x}^{2}+{y}^{2}} \\ {g}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{ln}⁡({x}^{2}+{y}^{2})) \\  & =\frac{2y}{{x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇g(x,y) & =⟨{g}_{x}(x,y),\,{g}_{y}(x,y)⟩ \\  & =⟨\frac{2x}{{x}^{2}+{y}^{2}},\,\frac{2y}{{x}^{2}+{y}^{2}}⟩ \\  & =\frac{2}{{x}^{2}+{y}^{2}}⟨x,\,y⟩ \\ ∇g(-1,\,0) & =\frac{2}{{(-1)}^{2}+{0}^{2}}⟨-1,\,0⟩ \\  & =\frac{2}{\,1}⟨-1,\,0⟩ \\  & =2⟨-1,\,0⟩ \\  & =⟨-2,\,0⟩\end{aligned}
$$


## Generated raw evidence moderate atan_ratio seed 30

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{\frac{5}{2}x}),$ find $∇h(x,y).$

- $(\frac{5 x}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }i+(- \frac{5 y}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }j$
- $(- \frac{2 y}{5 x^{2} \left(1 + \frac{4 y^{2}}{25 x^{2}}\right)})\text{ }i+(\frac{2}{5 x \left(1 + \frac{4 y^{2}}{25 x^{2}}\right)})\text{ }j$
- $(\frac{2 y}{5 x^{2} \left(1 + \frac{4 y^{2}}{25 x^{2}}\right)})\text{ }i+(- \frac{2}{5 x \left(1 + \frac{4 y^{2}}{25 x^{2}}\right)})\text{ }j$
- $(- \frac{5 x}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }i+(\frac{5 y}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }j$
- $(- \frac{5 y^{2}}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }i+(\frac{5 x^{2}}{2 \left(\frac{25 x^{2}}{4} + y^{2}\right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(\frac{y}{\frac{5}{2}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{5}{2}x})}^{2}}\cdot (-\frac{y}{\frac{5}{2}{x}^{2}}) \\  & =\frac{\frac{25}{4}{x}^{2}}{{\frac{5}{2}x}^{2}+{y}^{2}}\cdot (-\frac{y}{\frac{5}{2}{x}^{2}}) \\  & =-\frac{\frac{5}{2}y}{{\frac{5}{2}x}^{2}+{y}^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{arctan}⁡(\frac{y}{\frac{5}{2}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{5}{2}x})}^{2}}\cdot (\frac{1}{\frac{5}{2}x}) \\  & =\frac{\frac{25}{4}{x}^{2}}{{\frac{5}{2}x}^{2}+{y}^{2}}\cdot \frac{1}{\frac{5}{2}x} \\  & =\frac{\frac{5}{2}x}{{\frac{5}{2}x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =-\frac{\frac{5}{2}y}{{\frac{5}{2}x}^{2}+{y}^{2}}\,i+\frac{\frac{5}{2}x}{{\frac{5}{2}x}^{2}+{y}^{2}}\,j.\end{aligned}
$$


## Generated raw evidence moderate atan_ratio seed 31

If $h(x,y)=\operatorname{arctan}⁡(\frac{y}{\frac{1}{8}x}),$ find $∇h(x,y).$

- $(- \frac{y^{2}}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }i+(\frac{x^{2}}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }j$
- $(\frac{8 y}{x^{2} \left(1 + \frac{64 y^{2}}{x^{2}}\right)})\text{ }i+(- \frac{8}{x \left(1 + \frac{64 y^{2}}{x^{2}}\right)})\text{ }j$
- $(\frac{x}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }i+(- \frac{y}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }j$
- $(- \frac{x}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }i+(\frac{y}{8 \left(\frac{x^{2}}{64} + y^{2}\right)})\text{ }j$
- $(- \frac{8 y}{x^{2} \left(1 + \frac{64 y^{2}}{x^{2}}\right)})\text{ }i+(\frac{8}{x \left(1 + \frac{64 y^{2}}{x^{2}}\right)})\text{ }j$

First, we find the partial derivatives: 

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{arctan}⁡(\frac{y}{\frac{1}{8}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{1}{8}x})}^{2}}\cdot (-\frac{y}{\frac{1}{8}{x}^{2}}) \\  & =\frac{\frac{1}{64}{x}^{2}}{{\frac{1}{8}x}^{2}+{y}^{2}}\cdot (-\frac{y}{\frac{1}{8}{x}^{2}}) \\  & =-\frac{\frac{1}{8}y}{{\frac{1}{8}x}^{2}+{y}^{2}} \\ {f}_{y}(x,y) & =\frac{∂}{∂y}(\operatorname{arctan}⁡(\frac{y}{\frac{1}{8}x})) \\  & =\frac{1}{1+{(\frac{y}{\frac{1}{8}x})}^{2}}\cdot (\frac{1}{\frac{1}{8}x}) \\  & =\frac{\frac{1}{64}{x}^{2}}{{\frac{1}{8}x}^{2}+{y}^{2}}\cdot \frac{1}{\frac{1}{8}x} \\  & =\frac{\frac{1}{8}x}{{\frac{1}{8}x}^{2}+{y}^{2}}\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =-\frac{\frac{1}{8}y}{{\frac{1}{8}x}^{2}+{y}^{2}}\,i+\frac{\frac{1}{8}x}{{\frac{1}{8}x}^{2}+{y}^{2}}\,j.\end{aligned}
$$


## Generated raw evidence moderate quotient seed 30

Given $f(x, y) = \frac{5x + 1y}{x - 5y}$, find $∇f(x, y)$.

- $(- 26 x)\text{ }i+(26 y)\text{ }j$
- $(- 26 y)\text{ }i+(26 x)\text{ }j$
- $(\frac{5}{x - 5 y} - \frac{5 x + y}{\left(x - 5 y\right)^{2}})\text{ }i+(\frac{1}{x - 5 y} + \frac{5 \left(5 x + y\right)}{\left(x - 5 y\right)^{2}})\text{ }j$
- $(\frac{26 y}{\left(x - 5 y\right)^{2}})\text{ }i+(\frac{26 x}{\left(x - 5 y\right)^{2}})\text{ }j$
- $(- \frac{26 x}{\left(x - 5 y\right)^{2}})\text{ }i+(\frac{26 y}{\left(x - 5 y\right)^{2}})\text{ }j$

[Worked solution absent in raw source.]


## Generated raw evidence moderate quotient seed 31

Given $f(x, y) = \frac{1x + 8y}{x - \frac{3}{8}y}$, find $∇f(x, y)$.

- $(- \frac{67 y}{8})\text{ }i+(\frac{67 x}{8})\text{ }j$
- $(\frac{1}{x - \frac{3 y}{8}} - \frac{x + 8 y}{\left(x - \frac{3 y}{8}\right)^{2}})\text{ }i+(\frac{8}{x - \frac{3 y}{8}} + \frac{3 \left(x + 8 y\right)}{8 \left(x - \frac{3 y}{8}\right)^{2}})\text{ }j$
- $(\frac{67 y}{8 \left(x - \frac{3 y}{8}\right)^{2}})\text{ }i+(\frac{67 x}{8 \left(x - \frac{3 y}{8}\right)^{2}})\text{ }j$
- $(- \frac{67 x}{8 \left(x - \frac{3 y}{8}\right)^{2}})\text{ }i+(\frac{67 y}{8 \left(x - \frac{3 y}{8}\right)^{2}})\text{ }j$
- $(- \frac{67 x}{8})\text{ }i+(\frac{67 y}{8})\text{ }j$

[Worked solution absent in raw source.]


## Generated raw evidence moderate components seed 30

Find the direction of the greatest rate of expansion of the fluid at the point $(-4,-1).$ Do not normalize the answer.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The required direction is $∇(\text{div}\,V)\,{|}_{(-4,\,-1)}=⟨$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$⟩.$

- $6$
- $2$

In part 2, we found that

$$
\begin{aligned}\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(-4,\,-1)} & =6 \\ \frac{∂}{∂y}(\text{div}\,V)\,{|}_{(-4,\,-1)} & =2\end{aligned}
$$

Therefore, the gradient at $(-4,-1)$ is the following:

$$
\begin{aligned}∇(\text{div}\,V)\,{|}_{(-4,\,-1)} & =\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(-4,\,-1)}\,i+\frac{∂}{∂y}(\text{div}\,V)\,{|}_{(-4,\,-1)}\,j \\  & =6\,i+2\,j \\  & =⟨6,\,2⟩\end{aligned}
$$


## Generated raw evidence moderate components seed 31

Find the direction of the greatest rate of expansion of the fluid at the point $(-3,2).$ Do not normalize the answer.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The required direction is $∇(\text{div}\,V)\,{|}_{(-3,\,2)}=⟨$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$,$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$⟩.$

- $-8$
- $8$

In part 2, we found that

$$
\begin{aligned}\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(-3,\,2)} & =-8 \\ \frac{∂}{∂y}(\text{div}\,V)\,{|}_{(-3,\,2)} & =8\end{aligned}
$$

Therefore, the gradient at $(-3,2)$ is the following:

$$
\begin{aligned}∇(\text{div}\,V)\,{|}_{(-3,\,2)} & =\frac{∂}{∂x}(\text{div}\,V)\,{|}_{(-3,\,2)}\,i+\frac{∂}{∂y}(\text{div}\,V)\,{|}_{(-3,\,2)}\,j \\  & =-8\,i+8\,j \\  & =⟨-8,\,8⟩\end{aligned}
$$
