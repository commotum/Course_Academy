# Direction generator review

Frozen source: math basis 1356. Raw originals retain omissions and known label error. Changed variants use authored complete banks.

## cosxy — original

In what direction does the function $f(x, y) = \cos x + x^{2}y$ increase most rapidly at the point $(1, 1)$?

- $-\sin (1)i + 2j$
- $-2i - j$
- $(2 - \sin (1))i + j$
- $(\sin (1) - 2)i - j$
- $2i + j$

[Source omits difficulty, solution and correct ref.]

## cosxy — generated raw source bank variant (evidence only)

In what direction does the function $f(x, y) = 2\cos x + x^{2}y$ increase most rapidly at the point $(1, 1)$?

- $2i + j$
- $(2\sin (1) - 2)i - j$
- $-2\sin (1)i + 2j$
- $-2i - j$
- $(2 - 2\sin (1))i + j$

[Raw source omits worked solution.]

## cosxy — generated easy seed 170

In what direction does the function $f(x, y) = \cos x + 2x^{2}y$ decrease most rapidly at the point $(2, -1)$?

- $(-8 -\sin{(2 )})\,i+8\,j$
- $(\sin{(2 )} + 8)\,i+8\,j$
- $\sin{(2 )}\,i-8\,j$
- $8\,i-8\,j$
- $(\sin{(2 )} + 8)\,i-8\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(2,-1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(\cos x + 2x^{2}y)\,i+\frac{∂}{∂y}(\cos x + 2x^{2}y)\,j \\ & =(-\sin x+4xy)\,i+(2x^{2})\,j \\ ∇f(2,-1) & =(-\sin (2)+4\cdot (2)\cdot (-1))\,i+(2\cdot (2)^{2})\,j \\ & =(-8 -\sin{(2 )})\,i+8\,j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $(\sin{(2 )} + 8)\,i-8\,j.$

## cosxy — generated easy seed 171

In what direction does the function $f(x, y) = 4\cos x + 4x^{2}y$ decrease most rapidly at the point $(3, -2)$?

- $(-48 -4 \sin{(3 )})\,i+36\,j$
- $4 \sin{(3 )}\,i-36\,j$
- $(4 \sin{(3 )} + 48)\,i-36\,j$
- $(4 \sin{(3 )} + 48)\,i+48\,j$
- $48\,i-36\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(3,-2):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(4\cos x + 4x^{2}y)\,i+\frac{∂}{∂y}(4\cos x + 4x^{2}y)\,j \\ & =(-4\sin x+8xy)\,i+(4x^{2})\,j \\ ∇f(3,-2) & =(-4\sin (3)+8\cdot (3)\cdot (-2))\,i+(4\cdot (3)^{2})\,j \\ & =(-48 -4 \sin{(3 )})\,i+36\,j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $(4 \sin{(3 )} + 48)\,i-36\,j.$

## linear_sin — original

In what direction does the function $g(x,y,z)={y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)$ increase most rapidly at the point $(1,1,2)?$

- $⟨-2\pi ,-2,-\pi ⟩$
- $⟨2,2,1⟩$
- $⟨-\pi ,-1,\pi ⟩$
- $⟨\pi ,2,\pi ⟩$
- $⟨2\pi ,2,\pi ⟩$

At a given point, a function $g(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇g(x,y,z)$ and evaluate it at the point $(1,1,2):$

$$
\begin{aligned}∇g(x,y,z) & =⟨\frac{∂}{∂x}({y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)),\,\frac{∂}{∂y}({y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)),\,\frac{∂}{∂z}({y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z))⟩ \\  & =⟨2\pi \operatorname{cos}⁡(2\pi x+\pi z),\,2y,\,\pi \operatorname{cos}⁡(2\pi x+\pi z)⟩ \\ ∇g(1,1,2) & =⟨2\pi \operatorname{cos}⁡(2\pi \cdot 1+\pi \cdot 2),\,2\cdot 1,\,\pi \operatorname{cos}⁡(2\pi \cdot 1+\pi \cdot 2)⟩ \\  & =⟨2\pi \operatorname{cos}⁡(4\pi ),\,2,\,\pi \operatorname{cos}⁡(4\pi )⟩ \\  & =⟨2\pi ,\,2,\,\pi ⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨2\pi ,\,2,\,\pi ⟩.$

## linear_sin — generated raw source bank variant (evidence only)

In what direction does the function $g(x,y,z)=2{y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)$ increase most rapidly at the point $(1,1,2)?$

- $⟨2\pi ,4,\pi ⟩$
- $⟨\pi ,4,\pi ⟩$
- $⟨-2\pi ,-4,-\pi ⟩$
- $⟨2,4,1⟩$
- $⟨-\pi ,-2,\pi ⟩$

At a given point, a function $g(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇g(x,y,z)$ and evaluate it at the point $(1,1,2):$

$$
\begin{aligned}∇g(x,y,z) & =⟨\frac{∂}{∂x}(2{y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)),\,\frac{∂}{∂y}(2{y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z)),\,\frac{∂}{∂z}(2{y}^{2}+\operatorname{sin}⁡(2\pi x+\pi z))⟩ \\  & =⟨2\pi \operatorname{cos}⁡(2\pi x+\pi z),\,4y,\,\pi \operatorname{cos}⁡(2\pi x+\pi z)⟩ \\ ∇g(1,1,2) & =⟨2\pi \operatorname{cos}⁡(2\pi \cdot 1+\pi \cdot 2),\,4\cdot 1,\,\pi \operatorname{cos}⁡(2\pi \cdot 1+\pi \cdot 2)⟩ \\  & =⟨2\pi \operatorname{cos}⁡(4\pi ),\,4,\,\pi \operatorname{cos}⁡(4\pi )⟩ \\  & =⟨2\pi ,\,4,\,\pi ⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨2\pi ,\,4,\,\pi ⟩.$

## linear_sin — generated moderate seed 170

In what direction does the function $g(x,y,z)=4{y}^{2}+\operatorname{sin}⁡(3\pi x+4\pi z)$ decrease most rapidly at the point $(-2,-1,2)?$

- $⟨-3\pi ,\,8,\,-1⟩$
- $⟨-3\pi ,\,8,\,-4\pi ⟩$
- $⟨-\pi ,\,8,\,-4\pi ⟩$
- $⟨-3\pi ,\,4,\,-4\pi ⟩$
- $⟨3\pi ,\,-8,\,4\pi ⟩$

At a given point, a function $g(x,y,z)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇g(x,y,z)$ and evaluate it at the point $(-2,-1,2):$

$$
\begin{aligned}∇g(x,y,z) & =⟨\frac{∂}{∂x}(4{y}^{2}+\operatorname{sin}⁡(3\pi x+4\pi z)),\,\frac{∂}{∂y}(4{y}^{2}+\operatorname{sin}⁡(3\pi x+4\pi z)),\,\frac{∂}{∂z}(4{y}^{2}+\operatorname{sin}⁡(3\pi x+4\pi z))⟩ \\  & =⟨3\pi \operatorname{cos}⁡(3\pi x+4\pi z),\,8y,\,4\pi \operatorname{cos}⁡(3\pi x+4\pi z)⟩ \\ ∇g(-2,-1,2) & =⟨3\pi \operatorname{cos}⁡(3\pi \cdot -2+4\pi \cdot 2),\,8\cdot -1,\,4\pi \operatorname{cos}⁡(3\pi \cdot -2+4\pi \cdot 2)⟩ \\  & =⟨3\pi \operatorname{cos}⁡(2\pi ),\,-8,\,4\pi \operatorname{cos}⁡(2\pi )⟩ \\  & =⟨3\pi ,\,-8,\,4\pi ⟩\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $⟨-3\pi ,\,8,\,-4\pi ⟩.$

## linear_sin — generated moderate seed 171

In what direction does the function $g(x,y,z)=4{y}^{2}+\operatorname{sin}⁡(4\pi x+\pi z)$ increase most rapidly at the point $(1,1,-1)?$

- $⟨-4\pi ,\,4,\,-\pi ⟩$
- $⟨-\pi ,\,8,\,-\pi ⟩$
- $⟨-4\pi ,\,8,\,-\pi ⟩$
- $⟨-4\pi ,\,8,\,-1⟩$
- $⟨4\pi ,\,-8,\,\pi ⟩$

At a given point, a function $g(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇g(x,y,z)$ and evaluate it at the point $(1,1,-1):$

$$
\begin{aligned}∇g(x,y,z) & =⟨\frac{∂}{∂x}(4{y}^{2}+\operatorname{sin}⁡(4\pi x+\pi z)),\,\frac{∂}{∂y}(4{y}^{2}+\operatorname{sin}⁡(4\pi x+\pi z)),\,\frac{∂}{∂z}(4{y}^{2}+\operatorname{sin}⁡(4\pi x+\pi z))⟩ \\  & =⟨4\pi \operatorname{cos}⁡(4\pi x+\pi z),\,8y,\,\pi \operatorname{cos}⁡(4\pi x+\pi z)⟩ \\ ∇g(1,1,-1) & =⟨4\pi \operatorname{cos}⁡(4\pi \cdot 1+\pi \cdot -1),\,8\cdot 1,\,\pi \operatorname{cos}⁡(4\pi \cdot 1+\pi \cdot -1)⟩ \\  & =⟨4\pi \operatorname{cos}⁡(3\pi ),\,8,\,\pi \operatorname{cos}⁡(3\pi )⟩ \\  & =⟨-4\pi ,\,8,\,-\pi ⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨-4\pi ,\,8,\,-\pi ⟩.$

## quadratic — original

In what direction does the function $f(x,y)={x}^{2}+3xy+2{y}^{2}$ increase most rapidly at the point $(2,1)?$

- $i-2\,j$
- $2\,i+j$
- $7\,i+10\,j$
- $4\,i+j$
- $3\,i-5\,j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(2,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+3xy+2{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+3xy+2{y}^{2})\,j \\  & =(2x+3y)\,i+(3x+4y)\,j \\ ∇f(2,1) & =(2(2)+3(1))\,i+(3(2)+4(1))\,j \\  & =7\,i+10\,j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $7\,i+10\,j.$

## quadratic — generated raw source bank variant (evidence only)

In what direction does the function $f(x,y)={x}^{2}+4xy+2{y}^{2}$ increase most rapidly at the point $(2,1)?$

- $4\,i-5\,j$
- $4\,i+j$
- $i-2\,j$
- $2\,i+j$
- $8\,i+12\,j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(2,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}({x}^{2}+4xy+2{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+4xy+2{y}^{2})\,j \\  & =(2x+4y)\,i+(4x+4y)\,j \\ ∇f(2,1) & =(2(2)+4(1))\,i+(4(2)+4(1))\,j \\  & =8\,i+12\,j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $8\,i+12\,j.$

## quadratic — generated easy seed 170

In what direction does the function $f(x,y)=2{x}^{2}+xy+4{y}^{2}$ decrease most rapidly at the point $(-3,2)?$

- $10\,i-16\,j$
- $12\,i-13\,j$
- $10\,i-13\,j$
- $-10\,i+13\,j$
- $4\,i-5\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(-3,2):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2{x}^{2}+xy+4{y}^{2})\,i+\frac{∂}{∂y}(2{x}^{2}+xy+4{y}^{2})\,j \\  & =(4x+y)\,i+(x+8y)\,j \\ ∇f(-3,2) & =(4(-3)+1(2))\,i+(1(-3)+8(2))\,j \\  & =-10\,i+13\,j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $10\,i-13\,j.$

## quadratic — generated easy seed 171

In what direction does the function $f(x,y)=4{x}^{2}+4xy+{y}^{2}$ decrease most rapidly at the point $(1,-1)?$

- $-4\,i+2\,j$
- $-8\,i-2\,j$
- $-4\,i-2\,j$
- $-3\,j$
- $4\,i+2\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(1,-1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(4{x}^{2}+4xy+{y}^{2})\,i+\frac{∂}{∂y}(4{x}^{2}+4xy+{y}^{2})\,j \\  & =(8x+4y)\,i+(4x+2y)\,j \\ ∇f(1,-1) & =(8(1)+4(-1))\,i+(4(1)+2(-1))\,j \\  & =4\,i+2\,j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $-4\,i-2\,j.$

## mixed_sin — original

Given the function $f(x,y,z)=\operatorname{sin}⁡(\pi x+y)+3{z}^{2}x$, in what direction does the function increase most rapidly at the point $(1,0,1)?$

- $⟨3,\,-\pi ,\,3⟩$
- $⟨-\pi +3,\,\pi ,\,3⟩$
- $⟨3,\,0,\,6⟩$
- $⟨-\pi +3,\,-1,\,6⟩$
- $⟨2,\,-1,\,6⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(1,0,1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\operatorname{sin}⁡(\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂y}(\operatorname{sin}⁡(\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂z}(\operatorname{sin}⁡(\pi x+y)+3{z}^{2}x)⟩ \\  & =⟨\pi \operatorname{cos}⁡(\pi x+y)+3{z}^{2},\,\operatorname{cos}⁡(\pi x+y),\,6xz⟩ \\ ∇f(1,0,1) & =⟨\pi \operatorname{cos}⁡(\pi \cdot 1+0)+3\cdot {1}^{2},\,\operatorname{cos}⁡(\pi \cdot 1+0),\,6\cdot 1\cdot 1⟩ \\  & =⟨\pi \operatorname{cos}⁡(\pi )+3,\,\operatorname{cos}⁡(\pi ),\,6⟩ \\  & =⟨-\pi +3,\,-1,\,6⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨-\pi +3,\,-1,\,6⟩.$

## mixed_sin — generated raw source bank variant (evidence only)

Given the function $f(x,y,z)=\operatorname{sin}⁡(2\pi x+y)+3{z}^{2}x$, in what direction does the function increase most rapidly at the point $(1,0,1)?$

- $⟨5,\,1,\,6⟩$
- $⟨2\pi +3,\,1,\,6⟩$
- $⟨3,\,-2\pi ,\,3⟩$
- $⟨2\pi +3,\,2\pi ,\,3⟩$
- $⟨3,\,0,\,6⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(1,0,1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\operatorname{sin}⁡(2\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂y}(\operatorname{sin}⁡(2\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂z}(\operatorname{sin}⁡(2\pi x+y)+3{z}^{2}x)⟩ \\  & =⟨2\pi \operatorname{cos}⁡(2\pi x+y)+3{z}^{2},\,\operatorname{cos}⁡(2\pi x+y),\,6xz⟩ \\ ∇f(1,0,1) & =⟨2\pi \operatorname{cos}⁡(2\pi \cdot 1+0)+3\cdot {1}^{2},\,\operatorname{cos}⁡(2\pi \cdot 1+0),\,6\cdot 1\cdot 1⟩ \\  & =⟨2\pi \operatorname{cos}⁡(2\pi )+3,\,\operatorname{cos}⁡(2\pi ),\,6⟩ \\  & =⟨2\pi +3,\,1,\,6⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨2\pi +3,\,1,\,6⟩.$

## mixed_sin — generated moderate seed 170

Given the function $f(x,y,z)=\operatorname{sin}⁡(3\pi x+y)+3{z}^{2}x$, in what direction does the function increase most rapidly at the point $(1,0,1)?$

- $⟨3 -3\pi ,\,-1,\,3⟩$
- $⟨3,\,-1,\,6⟩$
- $⟨2,\,-1,\,6⟩$
- $⟨3 -3\pi ,\,-1,\,6⟩$
- $⟨-3 + 3\pi ,\,1,\,-6⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(1,0,1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\operatorname{sin}⁡(3\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂y}(\operatorname{sin}⁡(3\pi x+y)+3{z}^{2}x),\,\frac{∂}{∂z}(\operatorname{sin}⁡(3\pi x+y)+3{z}^{2}x)⟩ \\  & =⟨3\pi \operatorname{cos}⁡(3\pi x+y)+3{z}^{2},\,\operatorname{cos}⁡(3\pi x+y),\,6xz⟩ \\ ∇f(1,0,1) & =⟨3\pi \operatorname{cos}⁡(3\pi \cdot 1+0)+3\cdot {1}^{2},\,\operatorname{cos}⁡(3\pi \cdot 1+0),\,6\cdot 1\cdot 1⟩ \\  & =⟨3\pi \operatorname{cos}⁡(3\pi )+3,\,\operatorname{cos}⁡(3\pi ),\,6⟩ \\  & =⟨-3\pi +3,\,-1,\,6⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨-3\pi +3,\,-1,\,6⟩.$

## mixed_sin — generated moderate seed 171

Given the function $f(x,y,z)=\operatorname{sin}⁡(2\pi x+y)+2{z}^{2}x$, in what direction does the function increase most rapidly at the point $(-1,0,-1)?$

- $⟨2,\,1,\,4⟩$
- $⟨2 + 2\pi ,\,1,\,2⟩$
- $⟨3,\,1,\,4⟩$
- $⟨-2\pi -2,\,-1,\,-4⟩$
- $⟨2 + 2\pi ,\,1,\,4⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(-1,0,-1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\operatorname{sin}⁡(2\pi x+y)+2{z}^{2}x),\,\frac{∂}{∂y}(\operatorname{sin}⁡(2\pi x+y)+2{z}^{2}x),\,\frac{∂}{∂z}(\operatorname{sin}⁡(2\pi x+y)+2{z}^{2}x)⟩ \\  & =⟨2\pi \operatorname{cos}⁡(2\pi x+y)+2{z}^{2},\,\operatorname{cos}⁡(2\pi x+y),\,4xz⟩ \\ ∇f(-1,0,-1) & =⟨2\pi \operatorname{cos}⁡(2\pi \cdot -1+0)+2\cdot {-1}^{2},\,\operatorname{cos}⁡(2\pi \cdot -1+0),\,4\cdot -1\cdot -1⟩ \\  & =⟨2\pi \operatorname{cos}⁡(-2\pi )+2,\,\operatorname{cos}⁡(-2\pi ),\,4⟩ \\  & =⟨2\pi +2,\,1,\,4⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $⟨2\pi +2,\,1,\,4⟩.$

## exp — original

In what direction does the function $f(x,y)=x\operatorname{ln}⁡y+y{e}^{x}-xy$ increase most rapidly at the point $(-1,1)?$

- $({e}^{-1}+1)\text{ }i+({e}^{-1}-1)j$
- $(e-1)\text{ }i+ej$
- $({e}^{-1}+1)\text{ }i+{e}^{-1}j$
- $({e}^{-1}-1)\text{ }i+{e}^{-1}j$
- $(e+1)\text{ }i+(e-1)j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(-1,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x\operatorname{ln}⁡y+y{e}^{x}-xy)\text{ }i+\frac{∂}{∂y}(x\operatorname{ln}⁡y+y{e}^{x}-xy)\text{ }j \\  & =(\operatorname{ln}⁡y+y{e}^{x}-y)\text{ }i+(\frac{x}{y}+{e}^{x}-x)\text{ }j \\ ∇f(1,1) & =(\operatorname{ln}⁡1+1\cdot {e}^{-1}-1)\text{ }i+(\frac{-1}{1}+{e}^{-1}-(-1))\text{ }j \\  & =({e}^{-1}-1)\text{ }i+{e}^{-1}j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $({e}^{-1}-1)\text{ }i+{e}^{-1}j.$

## exp — generated raw source bank variant (evidence only)

In what direction does the function $f(x,y)=x\operatorname{ln}⁡y+y{e}^{x}-2xy$ increase most rapidly at the point $(-1,1)?$

- $(e+2)\text{ }i+(e-2)j$
- $({e}^{-1}-2)\text{ }i+({e}^{-1}+1)j$
- $({e}^{-1}+2)\text{ }i+({e}^{-1}-2)j$
- $(e-2)\text{ }i+(e+1)j$
- $({e}^{-1}+2)\text{ }i+({e}^{-1}+1)j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(-1,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(x\operatorname{ln}⁡y+y{e}^{x}-2xy)\text{ }i+\frac{∂}{∂y}(x\operatorname{ln}⁡y+y{e}^{x}-2xy)\text{ }j \\  & =(\operatorname{ln}⁡y+y{e}^{x}-2y)\text{ }i+(\frac{x}{y}+{e}^{x}-2x)\text{ }j \\ ∇f(1,1) & =(\operatorname{ln}⁡1+1\cdot {e}^{-1}-2\cdot (1))\text{ }i+(\frac{-1}{1}+{e}^{-1}-2(-1))\text{ }j \\  & =({e}^{-1}-2)\text{ }i+({e}^{-1}+1)j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $({e}^{-1}-2)\text{ }i+({e}^{-1}+1)j.$

## exp — generated easy seed 170

In what direction does the function $f(x,y)=3x\operatorname{ln}⁡y+3y{e}^{x}-3xy$ decrease most rapidly at the point $(1,1)?$

- $(-3 + 3 e)\,i+3 e\,j$
- $(-3 e -3)\,i-3 e\,j$
- $(3 -3 e)\,i+(3 -3 e)\,j$
- $(3 -3 e)\,i-3 e\,j$
- $(3 -\frac{3}{e})\,i-\frac{3}{e}\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(3x\operatorname{ln}⁡y+3y{e}^{x}-3xy)\text{ }i+\frac{∂}{∂y}(3x\operatorname{ln}⁡y+3y{e}^{x}-3xy)\text{ }j \\  & =(3\operatorname{ln}⁡y+3y{e}^{x}-3y)\text{ }i+(3\frac{x}{y}+3{e}^{x}-3x)\text{ }j \\ ∇f(1,1) & =(3\operatorname{ln}⁡1+3\cdot (1\cdot {e}^{1})-3\cdot (1))\text{ }i+(3\frac{1}{1}+3{e}^{1}-3(1))\text{ }j \\  & =(3{e}^{1}-3)\text{ }i+3{e}^{1}j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $(3 -3 e)\,i-3 e\,j.$

## exp — generated easy seed 171

In what direction does the function $f(x,y)=4x\operatorname{ln}⁡y+4y{e}^{x}-xy$ decrease most rapidly at the point $(2,1)?$

- $(1 -4 {e}^{2})\,i+(2 -4 {e}^{2})\,j$
- $(1 -\frac{4}{{e}^{2}})\,i+(-6 -\frac{4}{{e}^{2}})\,j$
- $(1 -4 {e}^{2})\,i+(-4 {e}^{2} -6)\,j$
- $(-1 + 4 {e}^{2})\,i+(6 + 4 {e}^{2})\,j$
- $(-4 {e}^{2} -1)\,i+(-4 {e}^{2} -6)\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(2,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(4x\operatorname{ln}⁡y+4y{e}^{x}-xy)\text{ }i+\frac{∂}{∂y}(4x\operatorname{ln}⁡y+4y{e}^{x}-xy)\text{ }j \\  & =(4\operatorname{ln}⁡y+4y{e}^{x}-y)\text{ }i+(4\frac{x}{y}+4{e}^{x}-x)\text{ }j \\ ∇f(2,1) & =(4\operatorname{ln}⁡1+4\cdot (1\cdot {e}^{2})-1)\text{ }i+(4\frac{2}{1}+4{e}^{2}-(2))\text{ }j \\  & =(4{e}^{2}-1)\text{ }i+(4{e}^{2}+6)j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $(1 -4 {e}^{2})\,i+(-4 {e}^{2} -6)\,j.$

## trig_product — original

In what direction does the function $f(x,y)=3{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x$ increase most rapidly at the point $(0,1)?$

- $-j$
- $j$
- $i+j$
- $2i-j$
- $i-j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(0,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(3{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }i+\frac{∂}{∂y}(3{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }j \\  & =(y\operatorname{sin}⁡x+6x\operatorname{sin}⁡y)\text{ }i+(3{x}^{2}\operatorname{cos}⁡y-\operatorname{cos}⁡x)\text{ }j \\ ∇f(0,1) & =(1\cdot \operatorname{sin}⁡(0)+6\cdot 0\cdot \operatorname{sin}⁡(1))\text{ }i+(3(0)^{2}\operatorname{cos}⁡(1)-\operatorname{cos}⁡(0))\text{ }j \\  & =-j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $-j.$

## trig_product — generated raw source bank variant (evidence only)

In what direction does the function $f(x,y)=4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x$ increase most rapidly at the point $(0,1)?$

- $i-j$
- $2i-j$
- $-j$
- $j$
- $i+j$

At a given point, a function $f(x,y)$ increases most rapidly in the direction of its gradient at that point.

So, we compute $∇f(x,y)$ and evaluate it at the point $(0,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }i+\frac{∂}{∂y}(4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }j \\  & =(y\operatorname{sin}⁡x+8x\operatorname{sin}⁡y)\text{ }i+(4{x}^{2}\operatorname{cos}⁡y-\operatorname{cos}⁡x)\text{ }j \\ ∇f(0,1) & =(1\cdot \operatorname{sin}⁡(0)+8\cdot 0\cdot \operatorname{sin}⁡(1))\text{ }i+(4(0)^{2}\operatorname{cos}⁡(1)-\operatorname{cos}⁡(0))\text{ }j \\  & =-j\end{aligned}
$$

Therefore, the function increases most rapidly in the direction of $-j.$

## trig_product — generated easy seed 170

In what direction does the function $f(x,y)=2{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x$ decrease most rapidly at the point $(1,-1)?$

- $5 \sin{(1 )}\,i-3 \cos{(1 )}\,j$
- $4 \sin{(1 )}\,i-\cos{(1 )}\,j$
- $5 \sin{(1 )}\,i-\cos{(1 )}\,j$
- $-5 \sin{(1 )}\,i+\cos{(1 )}\,j$
- $-\cos{(1 )}\,i+5 \sin{(1 )}\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(1,-1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(2{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }i+\frac{∂}{∂y}(2{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }j \\  & =(y\operatorname{sin}⁡x+4x\operatorname{sin}⁡y)\text{ }i+(2{x}^{2}\operatorname{cos}⁡y-\operatorname{cos}⁡x)\text{ }j \\ ∇f(1,-1) & =(-1\cdot \operatorname{sin}⁡(1)+4\cdot 1\cdot \operatorname{sin}⁡(-1))\text{ }i+(2(1)^{2}\operatorname{cos}⁡(-1)-\operatorname{cos}⁡(1))\text{ }j \\  & =-5 \sin{(1 )}\text{ }i+\cos{(1 )}\text{ }j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $5 \sin{(1 )}\,i-\cos{(1 )}\,j.$

## trig_product — generated easy seed 171

In what direction does the function $f(x,y)=4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x$ decrease most rapidly at the point $(1,1)?$

- $-9 \sin{(1 )}\,i-5 \cos{(1 )}\,j$
- $-8 \sin{(1 )}\,i-3 \cos{(1 )}\,j$
- $-9 \sin{(1 )}\,i-3 \cos{(1 )}\,j$
- $-3 \cos{(1 )}\,i-9 \sin{(1 )}\,j$
- $9 \sin{(1 )}\,i+3 \cos{(1 )}\,j$

At a given point, a function $f(x,y)$ decreases most rapidly in the direction opposite to that of its gradient.

So, we compute $∇f(x,y)$ and evaluate it at the point $(1,1):$

$$
\begin{aligned}∇f(x,y) & =\frac{∂}{∂x}(4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }i+\frac{∂}{∂y}(4{x}^{2}\operatorname{sin}⁡y-y\operatorname{cos}⁡x)\text{ }j \\  & =(y\operatorname{sin}⁡x+8x\operatorname{sin}⁡y)\text{ }i+(4{x}^{2}\operatorname{cos}⁡y-\operatorname{cos}⁡x)\text{ }j \\ ∇f(1,1) & =(1\cdot \operatorname{sin}⁡(1)+8\cdot 1\cdot \operatorname{sin}⁡(1))\text{ }i+(4(1)^{2}\operatorname{cos}⁡(1)-\operatorname{cos}⁡(1))\text{ }j \\  & =9 \sin{(1 )}\text{ }i+3 \cos{(1 )}\text{ }j\end{aligned}
$$

Therefore, the function decreases most rapidly in the direction of $-9 \sin{(1 )}\,i-3 \cos{(1 )}\,j.$

## log_unit — generated hard seed 170

In what unit direction does the function $f(x,y,z)=\ln (x^{4}y^{3}z^{2})$ increase most rapidly at the point $(2,3,1)$?

- $⟨\frac{\sqrt{21}}{21},\,\frac{2 \sqrt{21}}{21},\,\frac{4 \sqrt{21}}{21}⟩$
- $⟨\frac{2}{9},\,\frac{1}{9},\,\frac{2}{9}⟩$
- $⟨-\frac{2}{3},\,-\frac{1}{3},\,-\frac{2}{3}⟩$
- $⟨\frac{2}{3},\,\frac{1}{3},\,\frac{2}{3}⟩$
- $⟨2,\,1,\,2⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(2,3,1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\ln (x^{4}y^{3}z^{2})),\,\frac{∂}{∂y}(\ln (x^{4}y^{3}z^{2})),\,\frac{∂}{∂z}(\ln (x^{4}y^{3}z^{2}))⟩ \\ & =⟨\frac{1}{x^{4}y^{3}z^{2}}\cdot 4x^{3}y^{3}z^{2},\,\frac{1}{x^{4}y^{3}z^{2}}\cdot 3x^{4}y^{2}z^{2},\,\frac{1}{x^{4}y^{3}z^{2}}\cdot 2x^{4}y^{3}z^{1}⟩ \\ & =⟨\frac{4}{x},\,\frac{3}{y},\,\frac{2}{z}⟩ \\ ∇f(2,3,1) & =⟨\frac{4}{2},\,\frac{3}{3},\,\frac{2}{1}⟩ \\ & =⟨2,\,1,\,2⟩\end{aligned}
$$

The corresponding unit direction is

$$
\begin{aligned}u & =\frac{∇f(2,3,1)}{‖∇f(2,3,1)‖} \\ & =\frac{1}{\sqrt{(2)^{2}+(1)^{2}+(2)^{2}}}⟨2,\,1,\,2⟩ \\ & =⟨\frac{2}{3},\,\frac{1}{3},\,\frac{2}{3}⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the unit direction of $⟨\frac{2}{3},\,\frac{1}{3},\,\frac{2}{3}⟩.$

## log_unit — generated hard seed 171

In what unit direction does the function $f(x,y,z)=\ln (x^{3}y^{3}z^{2})$ increase most rapidly at the point $(1,1,1)$?

- $⟨\frac{3}{22},\,\frac{3}{22},\,\frac{1}{11}⟩$
- $⟨3,\,3,\,2⟩$
- $⟨\frac{3 \sqrt{22}}{22},\,\frac{3 \sqrt{22}}{22},\,\frac{\sqrt{22}}{11}⟩$
- $⟨\frac{\sqrt{14}}{14},\,\frac{3 \sqrt{14}}{14},\,\frac{\sqrt{14}}{7}⟩$
- $⟨-\frac{3 \sqrt{22}}{22},\,-\frac{3 \sqrt{22}}{22},\,-\frac{\sqrt{22}}{11}⟩$

At a given point, a function $f(x,y,z)$ increases most rapidly in the direction of its gradient.

So, we compute $∇f(x,y,z)$ and evaluate it at the point $(1,1,1):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(\ln (x^{3}y^{3}z^{2})),\,\frac{∂}{∂y}(\ln (x^{3}y^{3}z^{2})),\,\frac{∂}{∂z}(\ln (x^{3}y^{3}z^{2}))⟩ \\ & =⟨\frac{1}{x^{3}y^{3}z^{2}}\cdot 3x^{2}y^{3}z^{2},\,\frac{1}{x^{3}y^{3}z^{2}}\cdot 3x^{3}y^{2}z^{2},\,\frac{1}{x^{3}y^{3}z^{2}}\cdot 2x^{3}y^{3}z^{1}⟩ \\ & =⟨\frac{3}{x},\,\frac{3}{y},\,\frac{2}{z}⟩ \\ ∇f(1,1,1) & =⟨\frac{3}{1},\,\frac{3}{1},\,\frac{2}{1}⟩ \\ & =⟨3,\,3,\,2⟩\end{aligned}
$$

The corresponding unit direction is

$$
\begin{aligned}u & =\frac{∇f(1,1,1)}{‖∇f(1,1,1)‖} \\ & =\frac{1}{\sqrt{(3)^{2}+(3)^{2}+(2)^{2}}}⟨3,\,3,\,2⟩ \\ & =⟨\frac{3 \sqrt{22}}{22},\,\frac{3 \sqrt{22}}{22},\,\frac{\sqrt{22}}{11}⟩\end{aligned}
$$

Therefore, the function increases most rapidly in the unit direction of $⟨\frac{3 \sqrt{22}}{22},\,\frac{3 \sqrt{22}}{22},\,\frac{\sqrt{22}}{11}⟩.$