# Original evidence and generated variants

All originals below are faithful evidence-only replays; generated examples are explicitly authored/default presentations.

## easy_quadratic

### Generated variant 1 (easy)

Consider the plane curve $3 x^{2} + 2 y^{2}=20.$  Find the equation of the normal line to the curve at the point $(2,-2).$

- $2 x + 3 y - 2=0$
- $2 x + 3 y=0$
- $2 x + 3 y + 2=0$
- $3 x - 2 y - 10=0$
- $x + 3 y + 4=0$

If we set $f(x,y)=3 x^{2} + 2 y^{2}$, our curve can be viewed as the level curve $f(x,y)=20.$  

A normal vector to the level curve that passes through the point $(2,-2)$ can be found by computing $∇f(2,-2).$ 

So, we find the gradient and evaluate it at $(2,-2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} + 2 y^{2})\,i+\frac{∂}{∂y}(3 x^{2} + 2 y^{2})\,j \\  & =(6 x)\,i+(4 y)\,j \\ ∇f(2,-2) & =(6 (2))\,i+(4 (-2))\,j \\  & =(12)\,i+(-8)\,j \\  & =⟨12,-8⟩\end{aligned}
$$

Hence, $∇f(2,-2)=⟨12,-8⟩$ is a normal vector to the curve at $(2,-2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(2)}{12} & =\frac{y-(-2)}{-8} \\ (-8)(x-(2)) & =(12)(y-(-2)) \\ (-2)(x-(2)) & =(3)(y-(-2)) \\ 4 - 2 x & =3 y + 6 \\ 2 x + 3 y + 2 & =0\end{aligned}
$$

### Generated variant 2 (easy)

Consider the plane curve $2 x^{2} + y^{2}=11.$  Find the equation of the normal line to the curve at the point $(-1,-3).$

- $3 x - 2 y - 3=0$
- $3 x - 4 y - 9=0$
- $2 x + 3 y + 11=0$
- $3 x - 2 y + 3=0$
- $3 x - 2 y=0$

If we set $f(x,y)=2 x^{2} + y^{2}$, our curve can be viewed as the level curve $f(x,y)=11.$  

A normal vector to the level curve that passes through the point $(-1,-3)$ can be found by computing $∇f(-1,-3).$ 

So, we find the gradient and evaluate it at $(-1,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x^{2} + y^{2})\,i+\frac{∂}{∂y}(2 x^{2} + y^{2})\,j \\  & =(4 x)\,i+(2 y)\,j \\ ∇f(-1,-3) & =(4 (-1))\,i+(2 (-3))\,j \\  & =(-4)\,i+(-6)\,j \\  & =⟨-4,-6⟩\end{aligned}
$$

Hence, $∇f(-1,-3)=⟨-4,-6⟩$ is a normal vector to the curve at $(-1,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-1)}{-4} & =\frac{y-(-3)}{-6} \\ (-6)(x-(-1)) & =(-4)(y-(-3)) \\ (-3)(x-(-1)) & =(-2)(y-(-3)) \\ - 3 x - 3 & =- 2 y - 6 \\ 3 x - 2 y - 3 & =0\end{aligned}
$$

## q-36339

### Original

Consider the plane curve $6xy=5{x}^{2}+{y}^{2}.$  Find the equation of the normal line to the curve at the point $(1,1).$

- $x+y=0$
- $x-y+2=0$
- $x+y-2=0$
- $x+y-1=0$
- $2x+y+2=0$

First, we bring all variables to one side:

$$
\begin{aligned}6xy & =5{x}^{2}+{y}^{2} \\ 0 & =5{x}^{2}+{y}^{2}-6xy\end{aligned}
$$

If we set $f(x,y)=5{x}^{2}+{y}^{2}-6xy$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(1,1)$ can be found by computing $∇f(1,1).$ 

So, we find the gradient and evaluate it at $(1,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5{x}^{2}+{y}^{2}-6xy)\,i+\frac{∂}{∂y}(5{x}^{2}+{y}^{2}-6xy)\,j \\  & =(10x-6y)\,i+(2y-6x)\,j \\ ∇f(1,1) & =(10-6(1))\,i+(2(1)-6)\,j \\  & =4\,i-4\,j \\  & =⟨4,-4⟩\end{aligned}
$$

Hence, $∇f(1,1)=⟨4,-4⟩$ is a normal vector to the curve at $(1,1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-1}{4} & =\frac{y-1}{-4} \\ x-1 & =-y+1 \\ x+y-2 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $6 x y + 44=5 x^{2} + y^{2}.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $3 x + 4 y + 27=0$
- $4 x - 3 y - 11=0$
- $3 x + 4 y=0$
- $3 x + 8 y - 39=0$
- $3 x + 4 y - 27=0$

First, we bring all variables to one side:

$$
\begin{aligned}6 x y + 44 & =5 x^{2} + y^{2} \\ 5 x^{2} - 6 x y + y^{2} & =44\end{aligned}
$$

If we set $f(x,y)=5 x^{2} - 6 x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=44.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 6 x y + y^{2})\,i+\frac{∂}{∂y}(5 x^{2} - 6 x y + y^{2})\,j \\  & =(10 x - 6 y)\,i+(- 6 x + 2 y)\,j \\ ∇f(5,3) & =(10 (5) - 6 (3))\,i+(- 6 (5) + 2 (3))\,j \\  & =(32)\,i+(-24)\,j \\  & =⟨32,-24⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨32,-24⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{32} & =\frac{y-(3)}{-24} \\ \frac{x}{4} - \frac{5}{4} & =1 - \frac{y}{3} \\ 3 x + 4 y - 27 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $6 x y + 17=5 x^{2} + y^{2}.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $9 x + 11 y=0$
- $9 x + 11 y - 69=0$
- $11 x - 9 y + 17=0$
- $9 x + 11 y + 69=0$
- $9 x + 22 y + 102=0$

First, we bring all variables to one side:

$$
\begin{aligned}6 x y + 17 & =5 x^{2} + y^{2} \\ 5 x^{2} - 6 x y + y^{2} & =17\end{aligned}
$$

If we set $f(x,y)=5 x^{2} - 6 x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=17.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(5 x^{2} - 6 x y + y^{2})\,i+\frac{∂}{∂y}(5 x^{2} - 6 x y + y^{2})\,j \\  & =(10 x - 6 y)\,i+(- 6 x + 2 y)\,j \\ ∇f(-4,-3) & =(10 (-4) - 6 (-3))\,i+(- 6 (-4) + 2 (-3))\,j \\  & =(-22)\,i+(18)\,j \\  & =⟨-22,18⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-22,18⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-22} & =\frac{y-(-3)}{18} \\ - \frac{x}{11} - \frac{4}{11} & =\frac{y}{9} + \frac{1}{3} \\ 9 x + 11 y + 69 & =0\end{aligned}
$$

## q-65173

### Original

Consider the plane curve $xy = x^{2} + y^{2} - 7$. Find the equation of the normal line to the curve at the point $(2,-1)$.

- $4x + 5y - 3 = 0$
- $-x - 3y + 5 = 0$
- $-5x - 4y + 1 = 0$
- $3x - 5y + 1 = 0$
- $-2x - 2y + 3 = 0$

[Original has no worked solution.]

### Generated variant 1 (moderate)

Consider the plane curve $x y + 12=x^{2} + y^{2} - 7.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $x - 7 y - 16=0$
- $7 x + y - 38=0$
- $x - 7 y=0$
- $x - 14 y + 37=0$
- $x - 7 y + 16=0$

First, we bring all variables to one side:

$$
\begin{aligned}x y + 12 & =x^{2} + y^{2} - 7 \\ x^{2} - x y + y^{2} & =19\end{aligned}
$$

If we set $f(x,y)=x^{2} - x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=19.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} - x y + y^{2})\,i+\frac{∂}{∂y}(x^{2} - x y + y^{2})\,j \\  & =(2 x - y)\,i+(- x + 2 y)\,j \\ ∇f(5,3) & =(2 (5) - (3))\,i+(- (5) + 2 (3))\,j \\  & =(7)\,i+(1)\,j \\  & =⟨7,1⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨7,1⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{7} & =\frac{y-(3)}{1} \\ (1)(x-(5)) & =(7)(y-(3)) \\ (1)(x-(5)) & =(7)(y-(3)) \\ x - 5 & =7 y - 21 \\ x - 7 y + 16 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $x y + 6=x^{2} + y^{2} - 7.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $2 x - 5 y=0$
- $2 x - 5 y + 7=0$
- $5 x + 2 y + 26=0$
- $2 x - 5 y - 7=0$
- $x - 5 y - 11=0$

First, we bring all variables to one side:

$$
\begin{aligned}x y + 6 & =x^{2} + y^{2} - 7 \\ x^{2} - x y + y^{2} & =13\end{aligned}
$$

If we set $f(x,y)=x^{2} - x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=13.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} - x y + y^{2})\,i+\frac{∂}{∂y}(x^{2} - x y + y^{2})\,j \\  & =(2 x - y)\,i+(- x + 2 y)\,j \\ ∇f(-4,-3) & =(2 (-4) - (-3))\,i+(- (-4) + 2 (-3))\,j \\  & =(-5)\,i+(-2)\,j \\  & =⟨-5,-2⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-5,-2⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-5} & =\frac{y-(-3)}{-2} \\ (-2)(x-(-4)) & =(-5)(y-(-3)) \\ (-2)(x-(-4)) & =(-5)(y-(-3)) \\ - 2 x - 8 & =- 5 y - 15 \\ 2 x - 5 y - 7 & =0\end{aligned}
$$

## q-130718

### Original

Consider the plane curve ${x}^{2}-3{y}^{2}=6.$  Find the equation of the normal line to the curve at the point $(3,1).$

- $x-3y=0$
- $x-y-2=0$
- $x+y-4=0$
- $x+3y-6=0$
- $2x+y-7=0$

If we set $f(x,y)={x}^{2}-3{y}^{2},$ our curve can be viewed as the level curve $f(x,y)=6.$  

A normal vector to the level curve that passes through the point $(3,1)$ can be found by computing $∇f(3,1).$ 

So, we find the gradient and evaluate it at $(3,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}-3{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}-3{y}^{2})\,j \\  & =2x\,i-6y\,j \\ ∇f(3,1) & =2(3)\,i-6(1)\,j \\  & =6\,i-6\,j \\  & =⟨6,-6⟩\end{aligned}
$$

Hence, $∇f(3,1)=⟨6,-6⟩$ is a normal vector to the curve at $(3,1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-3}{6} & =\frac{y-1}{(-6)} \\ -6(x-3) & =6(y-1) \\ -(x-3) & =y-1 \\ -x+3 & =y-1 \\ x+y-4 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $x^{2} - 3 y^{2}=-2.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $9 x + 5 y + 60=0$
- $5 x - 9 y + 2=0$
- $9 x + 5 y=0$
- $9 x + 10 y - 75=0$
- $9 x + 5 y - 60=0$

If we set $f(x,y)=x^{2} - 3 y^{2}$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} - 3 y^{2})\,i+\frac{∂}{∂y}(x^{2} - 3 y^{2})\,j \\  & =(2 x)\,i+(- 6 y)\,j \\ ∇f(5,3) & =(2 (5))\,i+(- 6 (3))\,j \\  & =(10)\,i+(-18)\,j \\  & =⟨10,-18⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨10,-18⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{10} & =\frac{y-(3)}{-18} \\ (-18)(x-(5)) & =(10)(y-(3)) \\ (-9)(x-(5)) & =(5)(y-(3)) \\ 45 - 9 x & =5 y - 15 \\ 9 x + 5 y - 60 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $x^{2} - 3 y^{2}=-11.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $9 x + 4 y=0$
- $9 x + 4 y - 48=0$
- $4 x - 9 y - 11=0$
- $9 x + 4 y + 48=0$
- $9 x + 8 y + 60=0$

If we set $f(x,y)=x^{2} - 3 y^{2}$, our curve can be viewed as the level curve $f(x,y)=-11.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} - 3 y^{2})\,i+\frac{∂}{∂y}(x^{2} - 3 y^{2})\,j \\  & =(2 x)\,i+(- 6 y)\,j \\ ∇f(-4,-3) & =(2 (-4))\,i+(- 6 (-3))\,j \\  & =(-8)\,i+(18)\,j \\  & =⟨-8,18⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-8,18⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-8} & =\frac{y-(-3)}{18} \\ (18)(x-(-4)) & =(-8)(y-(-3)) \\ (9)(x-(-4)) & =(-4)(y-(-3)) \\ 9 x + 36 & =- 4 y - 12 \\ 9 x + 4 y + 48 & =0\end{aligned}
$$

## q-130723

### Original

Consider the plane curve $4xy+2{x}^{2}=x+2y.$  Find the equation of the normal line to the curve at the point $(2,-1).$

- $2x-y-5=0$
- $x-3y-5=0$
- $x+y-1=0$
- $x-2y-4=0$
- $x+2y=0$

First, we bring all variables to one side: 

$$
\begin{aligned}4xy+2{x}^{2} & =x+2y \\ 4xy+2{x}^{2}-x-2y & =0\end{aligned}
$$

If we set $f(x,y)=4xy+2{x}^{2}-x-2y$, our curve can be viewed as the level curve $f(x,y)=0.$   

A normal vector to the level curve that passes through the point $(2,-1)$ can be found by computing $∇f(2,-1).$ 

So, we find the gradient and evaluate it at $(2,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(4xy+2{x}^{2}-x-2y)\,i+\frac{∂}{∂y}(4xy+2{x}^{2}-x-2y)\,j \\  & =(4y+4x-1)\,i+(4x-2)\,j \\ ∇f(2,-1) & =(4(-1)+4(2)-1)\,i+(4(2)-2)\,j \\  & =3\,i+6\,j \\  & =⟨3,6⟩\end{aligned}
$$

 Hence, $∇f(2,-1)=⟨3,6⟩$ is a normal vector to the curve at $(2,-1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-2}{3} & =\frac{y-(-1)}{6} \\ 6(x-2) & =3(y+1) \\ 2(x-2) & =y+1 \\ 2x-4 & =y+1 \\ 2x-y-5 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $2 x^{2} + 4 x y=x + 2 y + 99.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $18 x - 31 y - 3=0$
- $31 x + 18 y - 209=0$
- $18 x - 31 y=0$
- $9 x - 31 y + 48=0$
- $18 x - 31 y + 3=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x^{2} + 4 x y & =x + 2 y + 99 \\ 2 x^{2} + 4 x y - x - 2 y & =99\end{aligned}
$$

If we set $f(x,y)=2 x^{2} + 4 x y - x - 2 y$, our curve can be viewed as the level curve $f(x,y)=99.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x^{2} + 4 x y - x - 2 y)\,i+\frac{∂}{∂y}(2 x^{2} + 4 x y - x - 2 y)\,j \\  & =(4 x + 4 y - 1)\,i+(4 x - 2)\,j \\ ∇f(5,3) & =(4 (5) + 4 (3) - 1)\,i+(4 (5) - 2)\,j \\  & =(31)\,i+(18)\,j \\  & =⟨31,18⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨31,18⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{31} & =\frac{y-(3)}{18} \\ (18)(x-(5)) & =(31)(y-(3)) \\ (18)(x-(5)) & =(31)(y-(3)) \\ 18 x - 90 & =31 y - 93 \\ 18 x - 31 y + 3 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $2 x^{2} + 4 x y=x + 2 y + 90.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $18 x - 29 y=0$
- $18 x - 29 y + 15=0$
- $29 x + 18 y + 170=0$
- $18 x - 29 y - 15=0$
- $9 x - 29 y - 51=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x^{2} + 4 x y & =x + 2 y + 90 \\ 2 x^{2} + 4 x y - x - 2 y & =90\end{aligned}
$$

If we set $f(x,y)=2 x^{2} + 4 x y - x - 2 y$, our curve can be viewed as the level curve $f(x,y)=90.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x^{2} + 4 x y - x - 2 y)\,i+\frac{∂}{∂y}(2 x^{2} + 4 x y - x - 2 y)\,j \\  & =(4 x + 4 y - 1)\,i+(4 x - 2)\,j \\ ∇f(-4,-3) & =(4 (-4) + 4 (-3) - 1)\,i+(4 (-4) - 2)\,j \\  & =(-29)\,i+(-18)\,j \\  & =⟨-29,-18⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-29,-18⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-29} & =\frac{y-(-3)}{-18} \\ (-18)(x-(-4)) & =(-29)(y-(-3)) \\ (-18)(x-(-4)) & =(-29)(y-(-3)) \\ - 18 x - 72 & =- 29 y - 87 \\ 18 x - 29 y - 15 & =0\end{aligned}
$$

## q-130724

### Original

Consider the plane curve $\sqrt{{x}^{2}+{y}^{2}}=2y-x-2.$  Find the equation of the normal line to the curve at the point $(0,2).$

- $3x+2y=4$
- $x+y=2$
- $x-y=-2$
- $3x+y=2$
- $2x-y=-2$

First, we bring all variables to one side:

$$
\begin{aligned}\sqrt{{x}^{2}+{y}^{2}} & =2y-x-2 \\ \sqrt{{x}^{2}+{y}^{2}}-2y+x & =-2\end{aligned}
$$

If we set $f(x,y)=\sqrt{{x}^{2}+{y}^{2}}-2y+x$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A normal vector to the level curve that passes through the point $(0,2)$ can be found by computing $∇f(0,2).$ 

So, we find the gradient and evaluate it at $(0,2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\sqrt{{x}^{2}+{y}^{2}}-2y+x)i+\frac{∂}{∂y}(\sqrt{{x}^{2}+{y}^{2}}-2y+x)j \\  & =(\frac{x}{\sqrt{{x}^{2}+{y}^{2}}}+1)i+(\frac{y}{\sqrt{{x}^{2}+{y}^{2}}}-2)j \\ ∇f(0,2) & =(\frac{0}{\sqrt{{0}^{2}+{2}^{2}}}+1)i+(\frac{2}{\sqrt{{0}^{2}+{2}^{2}}}-2)j \\  & =i-j \\  & =⟨1,-1⟩\end{aligned}
$$

Hence, $∇f(0,2)=⟨1,-1⟩$ is a normal vector to the curve at $(0,2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-0}{1} & =\frac{y-2}{-1} \\ x & =2-y \\ x+y & =2\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $\sqrt{x^{2} + y^{2}}=- x + 2 y - 4.$  Find the equation of the normal line to the curve at the point $(0,4).$

- $x + y + 4=0$
- $x + 2 y - 8=0$
- $x - y + 4=0$
- $x + y - 4=0$
- $x + y=0$

First, we bring all variables to one side:

$$
\begin{aligned}\sqrt{x^{2} + y^{2}} & =- x + 2 y - 4 \\ x - 2 y + \sqrt{x^{2} + y^{2}} & =-4\end{aligned}
$$

If we set $f(x,y)=x - 2 y + \sqrt{x^{2} + y^{2}}$, our curve can be viewed as the level curve $f(x,y)=-4.$  

A normal vector to the level curve that passes through the point $(0,4)$ can be found by computing $∇f(0,4).$ 

So, we find the gradient and evaluate it at $(0,4):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x - 2 y + \sqrt{x^{2} + y^{2}})\,i+\frac{∂}{∂y}(x - 2 y + \sqrt{x^{2} + y^{2}})\,j \\  & =(\frac{x}{\sqrt{x^{2} + y^{2}}} + 1)\,i+(\frac{y}{\sqrt{x^{2} + y^{2}}} - 2)\,j \\ ∇f(0,4) & =(\frac{(0)}{\sqrt{(0)^{2} + (4)^{2}}} + 1)\,i+(\frac{(4)}{\sqrt{(0)^{2} + (4)^{2}}} - 2)\,j \\  & =(1)\,i+(-1)\,j \\  & =⟨1,-1⟩\end{aligned}
$$

Hence, $∇f(0,4)=⟨1,-1⟩$ is a normal vector to the curve at $(0,4).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(0)}{1} & =\frac{y-(4)}{-1} \\ x & =4 - y \\ x + y - 4 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $\sqrt{x^{2} + y^{2}}=- x + 2 y - 2.$  Find the equation of the normal line to the curve at the point $(0,2).$

- $x + 2 y - 4=0$
- $x + y=0$
- $x - y + 2=0$
- $x + y - 2=0$
- $x + y + 2=0$

First, we bring all variables to one side:

$$
\begin{aligned}\sqrt{x^{2} + y^{2}} & =- x + 2 y - 2 \\ x - 2 y + \sqrt{x^{2} + y^{2}} & =-2\end{aligned}
$$

If we set $f(x,y)=x - 2 y + \sqrt{x^{2} + y^{2}}$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A normal vector to the level curve that passes through the point $(0,2)$ can be found by computing $∇f(0,2).$ 

So, we find the gradient and evaluate it at $(0,2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x - 2 y + \sqrt{x^{2} + y^{2}})\,i+\frac{∂}{∂y}(x - 2 y + \sqrt{x^{2} + y^{2}})\,j \\  & =(\frac{x}{\sqrt{x^{2} + y^{2}}} + 1)\,i+(\frac{y}{\sqrt{x^{2} + y^{2}}} - 2)\,j \\ ∇f(0,2) & =(\frac{(0)}{\sqrt{(0)^{2} + (2)^{2}}} + 1)\,i+(\frac{(2)}{\sqrt{(0)^{2} + (2)^{2}}} - 2)\,j \\  & =(1)\,i+(-1)\,j \\  & =⟨1,-1⟩\end{aligned}
$$

Hence, $∇f(0,2)=⟨1,-1⟩$ is a normal vector to the curve at $(0,2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(0)}{1} & =\frac{y-(2)}{-1} \\ x & =2 - y \\ x + y - 2 & =0\end{aligned}
$$

## q-36347

### Original

Consider the plane curve $2xy+6{y}^{2}=x-2.$  Find the equation of the normal line to the curve at the point $(8,-3).$

- $-20x-7y+181=0$
- $-20x+7y+181=0$
- $-20x+7y+28=0$
- $20x+7y-139=0$
- $20x+7y+181=0$

First, we bring all variables to one side: 

$$
\begin{aligned}2xy+6{y}^{2} & =x-2 \\ 2xy+6{y}^{2}-x & =-2\end{aligned}
$$

If we set $f(x,y)=2xy+6{y}^{2}-x$, our curve can be viewed as the level curve $f(x,y)=-2.$   

A normal vector to the level curve that passes through the point $(8,-3)$ can be found by computing $∇f(8,-3).$ 

So, we find the gradient and evaluate it at $(8,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2xy+6{y}^{2}-x)\,i+\frac{∂}{∂y}(2xy+6{y}^{2}-x)\,j \\  & =(2y-1)\,i+(2x+12y)\,j \\ ∇f(8,-3) & =(2(-3)-1)\,i+(2(8)+12(-3))\,j \\  & =-7\,i-20\,j \\  & =⟨-7,-20⟩\end{aligned}
$$

 Hence, $∇f(8,-3)=⟨-7,-20⟩$ is a normal vector to the curve at $(8,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-8}{-7} & =\frac{y-(-3)}{-20} \\ -20(x-8) & =-7(y+3) \\ -20x+7y+160+21 & =0 \\ -20x+7y+181 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $2 x y + 6 y^{2}=x + 79.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $46 x - 5 y + 215=0$
- $5 x + 46 y - 163=0$
- $46 x - 5 y=0$
- $23 x - 5 y - 100=0$
- $46 x - 5 y - 215=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x y + 6 y^{2} & =x + 79 \\ 2 x y - x + 6 y^{2} & =79\end{aligned}
$$

If we set $f(x,y)=2 x y - x + 6 y^{2}$, our curve can be viewed as the level curve $f(x,y)=79.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x y - x + 6 y^{2})\,i+\frac{∂}{∂y}(2 x y - x + 6 y^{2})\,j \\  & =(2 y - 1)\,i+(2 x + 12 y)\,j \\ ∇f(5,3) & =(2 (3) - 1)\,i+(2 (5) + 12 (3))\,j \\  & =(5)\,i+(46)\,j \\  & =⟨5,46⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨5,46⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{5} & =\frac{y-(3)}{46} \\ (46)(x-(5)) & =(5)(y-(3)) \\ 46 x - 5 y+(-230)+(15) & =0 \\ 46 x - 5 y - 215 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $2 x y + 6 y^{2}=x + 82.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $44 x - 7 y=0$
- $44 x - 7 y - 155=0$
- $7 x + 44 y + 160=0$
- $44 x - 7 y + 155=0$
- $22 x - 7 y + 67=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x y + 6 y^{2} & =x + 82 \\ 2 x y - x + 6 y^{2} & =82\end{aligned}
$$

If we set $f(x,y)=2 x y - x + 6 y^{2}$, our curve can be viewed as the level curve $f(x,y)=82.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(2 x y - x + 6 y^{2})\,i+\frac{∂}{∂y}(2 x y - x + 6 y^{2})\,j \\  & =(2 y - 1)\,i+(2 x + 12 y)\,j \\ ∇f(-4,-3) & =(2 (-3) - 1)\,i+(2 (-4) + 12 (-3))\,j \\  & =(-7)\,i+(-44)\,j \\  & =⟨-7,-44⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-7,-44⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-7} & =\frac{y-(-3)}{-44} \\ (-44)(x-(-4)) & =(-7)(y-(-3)) \\ - 44 x + 7 y+(-176)+(21) & =0 \\ 44 x - 7 y + 155 & =0\end{aligned}
$$

## q-71385

### Original

Consider the plane curve ${x}^{2}+{y}^{2}=4.$  Find the equation of the normal line to the curve at the point $(2,0).$

- $x+y=2$
- $x-y=2$
- $x=2$
- $x=0$
- $y=0$

If we set $f(x,y)={x}^{2}+{y}^{2}$, our curve can be viewed as the level curve $f(x,y)=4.$  

A normal vector to the level curve that passes through the point $(2,0)$ can be found by computing $∇f(2,0).$ 

So, we find the gradient and evaluate it at $(2,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({x}^{2}+{y}^{2})\,i+\frac{∂}{∂y}({x}^{2}+{y}^{2})\,j \\  & =2x\,i+2y\,j \\ ∇f(2,0) & =2(2)\,i+2(0)\,j \\  & =4\,i \\  & =⟨4,0⟩\end{aligned}
$$

Hence, $∇f(2,0)=⟨4,0⟩$ is a normal vector to the curve at $(2,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-2)0-(y-0)4 & =0 \\ -4y & =0 \\ y & =0\end{aligned}
$$

### Generated variant 1 (hard)

Consider the plane curve $x^{2} + y^{2}=1.$  Find the equation of the normal line to the curve at the point $(-1,0).$

- $x + y + 1=0$
- $x=0$
- $x + 1=0$
- $y + 1=0$
- $y=0$

If we set $f(x,y)=x^{2} + y^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$  

A normal vector to the level curve that passes through the point $(-1,0)$ can be found by computing $∇f(-1,0).$ 

So, we find the gradient and evaluate it at $(-1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} + y^{2})\,i+\frac{∂}{∂y}(x^{2} + y^{2})\,j \\  & =(2 x)\,i+(2 y)\,j \\ ∇f(-1,0) & =(2 (-1))\,i+(2 (0))\,j \\  & =(-2)\,i+(0)\,j \\  & =⟨-2,0⟩\end{aligned}
$$

Hence, $∇f(-1,0)=⟨-2,0⟩$ is a normal vector to the curve at $(-1,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(-1))(0)-(y-(0))(-2) & =0 \\ 2 y & =0 \\ y & =0\end{aligned}
$$

### Generated variant 2 (hard)

Consider the plane curve $x^{2} + y^{2}=9.$  Find the equation of the normal line to the curve at the point $(3,0).$

- $x=0$
- $y=0$
- $x - 3=0$
- $y - 3=0$
- $x + y - 3=0$

If we set $f(x,y)=x^{2} + y^{2}$, our curve can be viewed as the level curve $f(x,y)=9.$  

A normal vector to the level curve that passes through the point $(3,0)$ can be found by computing $∇f(3,0).$ 

So, we find the gradient and evaluate it at $(3,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{2} + y^{2})\,i+\frac{∂}{∂y}(x^{2} + y^{2})\,j \\  & =(2 x)\,i+(2 y)\,j \\ ∇f(3,0) & =(2 (3))\,i+(2 (0))\,j \\  & =(6)\,i+(0)\,j \\  & =⟨6,0⟩\end{aligned}
$$

Hence, $∇f(3,0)=⟨6,0⟩$ is a normal vector to the curve at $(3,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(3))(0)-(y-(0))(6) & =0 \\ - 6 y & =0 \\ y & =0\end{aligned}
$$

## q-71388

### Original

Consider the plane curve $2x+y-1=\sqrt{{x}^{2}-{y}^{2}}.$  Find the equation of the normal line to the curve at the point $(1,0).$

- $x+y=1$
- $x-2y=1$
- $x-y=1$
- $x+2y=1$
- $y-x=1$

First, we bring all variables to one side:

$$
\begin{aligned}2x+y-1 & =\sqrt{{x}^{2}-{y}^{2}} \\ -1 & =\sqrt{{x}^{2}-{y}^{2}}-2x-y\end{aligned}
$$

If we set $f(x,y)=\sqrt{{x}^{2}-{y}^{2}}-2x-y$, our curve can be viewed as the level curve $f(x,y)=-1.$  

A normal vector to the level curve that passes through the point $(1,0)$ can be found by computing $∇f(1,0).$ 

So, we find the gradient and evaluate it at $(1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\sqrt{{x}^{2}-{y}^{2}}-2x-y)\,i+\frac{∂}{∂y}(\sqrt{{x}^{2}-{y}^{2}}-2x-y)\,j \\  & =(\frac{x}{\sqrt{{x}^{2}-{y}^{2}}}-2)\,i+(-\frac{y}{\sqrt{{x}^{2}-{y}^{2}}}-1)\,j \\ ∇f(1,0) & =(\frac{1}{\sqrt{{1}^{2}-{0}^{2}}}-2)\,i+(-\frac{0}{\sqrt{{1}^{2}-{0}^{2}}}-1)\,j \\  & =-i-j \\  & =⟨-1,-1⟩\end{aligned}
$$

Hence, $∇f(1,0)=⟨-1,-1⟩$ is a normal vector to the curve at $(1,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-1}{-1} & =\frac{y-0}{-1} \\ 1-x & =-y \\ x-y & =1\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $2 x + y - 4=\sqrt{x^{2} - y^{2}}.$  Find the equation of the normal line to the curve at the point $(4,0).$

- $x - y + 4=0$
- $x - 2 y - 4=0$
- $x + y - 4=0$
- $x - y - 4=0$
- $x - y=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x + y - 4 & =\sqrt{x^{2} - y^{2}} \\ - 2 x - y + \sqrt{x^{2} - y^{2}} & =-4\end{aligned}
$$

If we set $f(x,y)=- 2 x - y + \sqrt{x^{2} - y^{2}}$, our curve can be viewed as the level curve $f(x,y)=-4.$  

A normal vector to the level curve that passes through the point $(4,0)$ can be found by computing $∇f(4,0).$ 

So, we find the gradient and evaluate it at $(4,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 2 x - y + \sqrt{x^{2} - y^{2}})\,i+\frac{∂}{∂y}(- 2 x - y + \sqrt{x^{2} - y^{2}})\,j \\  & =(\frac{x}{\sqrt{x^{2} - y^{2}}} - 2)\,i+(- \frac{y}{\sqrt{x^{2} - y^{2}}} - 1)\,j \\ ∇f(4,0) & =(\frac{(4)}{\sqrt{(4)^{2} - (0)^{2}}} - 2)\,i+(- \frac{(0)}{\sqrt{(4)^{2} - (0)^{2}}} - 1)\,j \\  & =(-1)\,i+(-1)\,j \\  & =⟨-1,-1⟩\end{aligned}
$$

Hence, $∇f(4,0)=⟨-1,-1⟩$ is a normal vector to the curve at $(4,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(4)}{-1} & =\frac{y-(0)}{-1} \\ 4 - x & =- y \\ x - y - 4 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $2 x + y - 2=\sqrt{x^{2} - y^{2}}.$  Find the equation of the normal line to the curve at the point $(2,0).$

- $x - 2 y - 2=0$
- $x - y=0$
- $x + y - 2=0$
- $x - y - 2=0$
- $x - y + 2=0$

First, we bring all variables to one side:

$$
\begin{aligned}2 x + y - 2 & =\sqrt{x^{2} - y^{2}} \\ - 2 x - y + \sqrt{x^{2} - y^{2}} & =-2\end{aligned}
$$

If we set $f(x,y)=- 2 x - y + \sqrt{x^{2} - y^{2}}$, our curve can be viewed as the level curve $f(x,y)=-2.$  

A normal vector to the level curve that passes through the point $(2,0)$ can be found by computing $∇f(2,0).$ 

So, we find the gradient and evaluate it at $(2,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 2 x - y + \sqrt{x^{2} - y^{2}})\,i+\frac{∂}{∂y}(- 2 x - y + \sqrt{x^{2} - y^{2}})\,j \\  & =(\frac{x}{\sqrt{x^{2} - y^{2}}} - 2)\,i+(- \frac{y}{\sqrt{x^{2} - y^{2}}} - 1)\,j \\ ∇f(2,0) & =(\frac{(2)}{\sqrt{(2)^{2} - (0)^{2}}} - 2)\,i+(- \frac{(0)}{\sqrt{(2)^{2} - (0)^{2}}} - 1)\,j \\  & =(-1)\,i+(-1)\,j \\  & =⟨-1,-1⟩\end{aligned}
$$

Hence, $∇f(2,0)=⟨-1,-1⟩$ is a normal vector to the curve at $(2,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(2)}{-1} & =\frac{y-(0)}{-1} \\ 2 - x & =- y \\ x - y - 2 & =0\end{aligned}
$$

## q-71390

### Original

Consider the plane curve ${y}^{2}+3{x}^{2}=4xy.$  Find the equation of the normal line to the curve at the point $(-1,-3).$

- $3y+x+10=0$
- $y+3x+4=0$
- $3y-x+8=0$
- $3y+2x+11=0$
- $y+3x+20=0$

First, we bring all variables to one side:

$$
\begin{aligned}{y}^{2}+3{x}^{2} & =4xy \\ {y}^{2}+3{x}^{2}-4xy & =0\end{aligned}
$$

If we set $f(x,y)={y}^{2}+3{x}^{2}-4xy$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(-1,-3)$ can be found by computing $∇f(-1,-3).$ 

So, we find the gradient and evaluate it at $(-1,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({y}^{2}+3{x}^{2}-4xy)\,i+\frac{∂}{∂y}({y}^{2}+3{x}^{2}-4xy)\,j \\  & =(6x-4y)\,i+(2y-4x)\,j \\ ∇f(-1,-3) & =(6(-1)-4(-3))\,i+(2(-3)-4(-1))\,j \\  & =6\,i-2\,j \\  & =⟨6,-2⟩\end{aligned}
$$

Hence, $∇f(-1,-3)=⟨6,-2⟩$ is a normal vector to the curve at $(-1,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-1)}{6} & =\frac{y-(-3)}{-2} \\ (-2)(x+1) & =6(y+3) \\ -2x-2 & =6y+18 \\ 6y+2x+20 & =0 \\ 3y+x+10 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $3 x^{2} + y^{2}=4 x y + 24.$  Find the equation of the normal line to the curve at the point $(5,3).$

- $7 x + 9 y + 62=0$
- $9 x - 7 y - 24=0$
- $7 x + 9 y=0$
- $7 x + 18 y - 89=0$
- $7 x + 9 y - 62=0$

First, we bring all variables to one side:

$$
\begin{aligned}3 x^{2} + y^{2} & =4 x y + 24 \\ 3 x^{2} - 4 x y + y^{2} & =24\end{aligned}
$$

If we set $f(x,y)=3 x^{2} - 4 x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=24.$  

A normal vector to the level curve that passes through the point $(5,3)$ can be found by computing $∇f(5,3).$ 

So, we find the gradient and evaluate it at $(5,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} - 4 x y + y^{2})\,i+\frac{∂}{∂y}(3 x^{2} - 4 x y + y^{2})\,j \\  & =(6 x - 4 y)\,i+(- 4 x + 2 y)\,j \\ ∇f(5,3) & =(6 (5) - 4 (3))\,i+(- 4 (5) + 2 (3))\,j \\  & =(18)\,i+(-14)\,j \\  & =⟨18,-14⟩\end{aligned}
$$

Hence, $∇f(5,3)=⟨18,-14⟩$ is a normal vector to the curve at $(5,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(5)}{18} & =\frac{y-(3)}{-14} \\ (-14)(x-(5)) & =(18)(y-(3)) \\ 70 - 14 x & =18 y - 54 \\ - 14 x - 18 y + 124 & =0 \\ 7 x + 9 y - 62 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $3 x^{2} + y^{2}=4 x y + 9.$  Find the equation of the normal line to the curve at the point $(-4,-3).$

- $5 x + 6 y=0$
- $5 x + 6 y - 38=0$
- $6 x - 5 y + 9=0$
- $5 x + 6 y + 38=0$
- $5 x + 12 y + 56=0$

First, we bring all variables to one side:

$$
\begin{aligned}3 x^{2} + y^{2} & =4 x y + 9 \\ 3 x^{2} - 4 x y + y^{2} & =9\end{aligned}
$$

If we set $f(x,y)=3 x^{2} - 4 x y + y^{2}$, our curve can be viewed as the level curve $f(x,y)=9.$  

A normal vector to the level curve that passes through the point $(-4,-3)$ can be found by computing $∇f(-4,-3).$ 

So, we find the gradient and evaluate it at $(-4,-3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(3 x^{2} - 4 x y + y^{2})\,i+\frac{∂}{∂y}(3 x^{2} - 4 x y + y^{2})\,j \\  & =(6 x - 4 y)\,i+(- 4 x + 2 y)\,j \\ ∇f(-4,-3) & =(6 (-4) - 4 (-3))\,i+(- 4 (-4) + 2 (-3))\,j \\  & =(-12)\,i+(10)\,j \\  & =⟨-12,10⟩\end{aligned}
$$

Hence, $∇f(-4,-3)=⟨-12,10⟩$ is a normal vector to the curve at $(-4,-3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{-12} & =\frac{y-(-3)}{10} \\ (10)(x-(-4)) & =(-12)(y-(-3)) \\ 10 x + 40 & =- 12 y - 36 \\ 10 x + 12 y + 76 & =0 \\ 5 x + 6 y + 38 & =0\end{aligned}
$$

## q-71393

### Original

Consider the plane curve $\operatorname{ln}⁡(x+y)=2xy.$  Find the equation of the normal line to the curve at the point $(0,1).$

- $x+2y-2=0$
- $-x+y-1=0$
- $x+y-1=0$
- $x+y+1=0$
- $x-y+1=0$

First, we bring all variables to one side:

$$
\begin{aligned}\operatorname{ln}⁡(x+y) & =2xy \\ \operatorname{ln}⁡(x+y)-2xy & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{ln}⁡(x+y)-2xy$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(0,1)$ can be found by computing $∇f(0,1).$ 

So, we find the gradient and evaluate it at $(0,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(x+y)-2xy)\,i+\frac{∂}{∂y}(\operatorname{ln}⁡(x+y)-2xy)\,j \\  & =(\frac{1}{x+y}-2y)\,i+(\frac{1}{x+y}-2x)\,j \\ ∇f(0,1) & =(\frac{1}{0+1}-2(1))\,i+(\frac{1}{0+1}-2(0))\,j \\  & =-i+j \\  & =⟨-1,1⟩\end{aligned}
$$

Hence, $∇f(0,1)=⟨-1,1⟩$ is a normal vector to the curve at $(0,1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-0}{-1} & =\frac{y-1}{1} \\ -x & =y-1 \\ x+y-1 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $\ln{\left(x + y \right)}=2 x y + 12.$  Find the equation of the normal line to the curve at the point $(3,-2).$

- $x + y + 1=0$
- $x + 2 y + 1=0$
- $x - y - 5=0$
- $x + y - 1=0$
- $x + y=0$

First, we bring all variables to one side:

$$
\begin{aligned}\ln{\left(x + y \right)} & =2 x y + 12 \\ - 2 x y + \ln{\left(x + y \right)} & =12\end{aligned}
$$

If we set $f(x,y)=- 2 x y + \ln{\left(x + y \right)}$, our curve can be viewed as the level curve $f(x,y)=12.$  

A normal vector to the level curve that passes through the point $(3,-2)$ can be found by computing $∇f(3,-2).$ 

So, we find the gradient and evaluate it at $(3,-2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 2 x y + \ln{\left(x + y \right)})\,i+\frac{∂}{∂y}(- 2 x y + \ln{\left(x + y \right)})\,j \\  & =(- 2 y + \frac{1}{x + y})\,i+(- 2 x + \frac{1}{x + y})\,j \\ ∇f(3,-2) & =(- 2 (-2) + \frac{1}{(3) + (-2)})\,i+(- 2 (3) + \frac{1}{(3) + (-2)})\,j \\  & =(5)\,i+(-5)\,j \\  & =⟨5,-5⟩\end{aligned}
$$

Hence, $∇f(3,-2)=⟨5,-5⟩$ is a normal vector to the curve at $(3,-2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(3)}{5} & =\frac{y-(-2)}{-5} \\ \frac{x}{5} - \frac{3}{5} & =- \frac{y}{5} - \frac{2}{5} \\ x + y - 1 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $\ln{\left(x + y \right)}=2 x y + 4.$  Find the equation of the normal line to the curve at the point $(-1,2).$

- $x + 2 y - 3=0$
- $x + y=0$
- $x - y + 3=0$
- $x + y - 1=0$
- $x + y + 1=0$

First, we bring all variables to one side:

$$
\begin{aligned}\ln{\left(x + y \right)} & =2 x y + 4 \\ - 2 x y + \ln{\left(x + y \right)} & =4\end{aligned}
$$

If we set $f(x,y)=- 2 x y + \ln{\left(x + y \right)}$, our curve can be viewed as the level curve $f(x,y)=4.$  

A normal vector to the level curve that passes through the point $(-1,2)$ can be found by computing $∇f(-1,2).$ 

So, we find the gradient and evaluate it at $(-1,2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- 2 x y + \ln{\left(x + y \right)})\,i+\frac{∂}{∂y}(- 2 x y + \ln{\left(x + y \right)})\,j \\  & =(- 2 y + \frac{1}{x + y})\,i+(- 2 x + \frac{1}{x + y})\,j \\ ∇f(-1,2) & =(- 2 (2) + \frac{1}{(-1) + (2)})\,i+(- 2 (-1) + \frac{1}{(-1) + (2)})\,j \\  & =(-3)\,i+(3)\,j \\  & =⟨-3,3⟩\end{aligned}
$$

Hence, $∇f(-1,2)=⟨-3,3⟩$ is a normal vector to the curve at $(-1,2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-1)}{-3} & =\frac{y-(2)}{3} \\ - \frac{x}{3} - \frac{1}{3} & =\frac{y}{3} - \frac{2}{3} \\ x + y - 1 & =0\end{aligned}
$$

## q-71394

### Original

Consider the plane curve $\frac{{y}^{2}}{16}-\frac{{x}^{2}}{9}=1.$  Find the equation of the normal line to the curve at the point $(0,4).$

- $y=4$
- $x=4$
- $x=0$
- $y=0$
- $x-y=-4$

If we set $f(x,y)=\frac{{y}^{2}}{16}-\frac{{x}^{2}}{9}$, our curve can be viewed as the level curve $f(x,y)=1.$  

A normal vector to the level curve that passes through the point $(0,4)$ can be found by computing $∇f(0,4).$ 

So, we find the gradient and evaluate it at $(0,4):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\frac{{y}^{2}}{16}-\frac{{x}^{2}}{9})\,i+\frac{∂}{∂y}(\frac{{y}^{2}}{16}-\frac{{x}^{2}}{9})\,j \\  & =-\frac{2}{9}x\,i+\frac{1}{8}y\,j \\ ∇f(0,4) & =-\frac{2}{9}(0)\,i+\frac{1}{8}(4)\,j \\  & =\frac{1}{2}\,j \\  & =⟨0,\frac{1}{2}⟩\end{aligned}
$$

Hence, $∇f(0,4)=⟨0,\frac{1}{2}⟩$ is a normal vector to the curve at $(0,4).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-0)\frac{1}{2}-(y-4)0 & =0 \\ \frac{1}{2}x & =0 \\ x & =0\end{aligned}
$$

### Generated variant 1 (hard)

Consider the plane curve $- \frac{x^{2}}{9} + \frac{y^{2}}{16}=\frac{1}{16}.$  Find the equation of the normal line to the curve at the point $(0,-1).$

- $x - y - 1=0$
- $x=0$
- $x + 1=0$
- $y + 1=0$
- $y=0$

If we set $f(x,y)=- \frac{x^{2}}{9} + \frac{y^{2}}{16}$, our curve can be viewed as the level curve $f(x,y)=\frac{1}{16}.$  

A normal vector to the level curve that passes through the point $(0,-1)$ can be found by computing $∇f(0,-1).$ 

So, we find the gradient and evaluate it at $(0,-1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- \frac{x^{2}}{9} + \frac{y^{2}}{16})\,i+\frac{∂}{∂y}(- \frac{x^{2}}{9} + \frac{y^{2}}{16})\,j \\  & =(- \frac{2 x}{9})\,i+(\frac{y}{8})\,j \\ ∇f(0,-1) & =(- \frac{2 (0)}{9})\,i+(\frac{(-1)}{8})\,j \\  & =(0)\,i+(- \frac{1}{8})\,j \\  & =⟨0,- \frac{1}{8}⟩\end{aligned}
$$

Hence, $∇f(0,-1)=⟨0,- \frac{1}{8}⟩$ is a normal vector to the curve at $(0,-1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(0))(- \frac{1}{8})-(y-(-1))(0) & =0 \\ - \frac{x}{8} & =0 \\ x & =0\end{aligned}
$$

### Generated variant 2 (hard)

Consider the plane curve $- \frac{x^{2}}{9} + \frac{y^{2}}{16}=\frac{9}{16}.$  Find the equation of the normal line to the curve at the point $(0,3).$

- $x=0$
- $y=0$
- $x - 3=0$
- $y - 3=0$
- $x - y + 3=0$

If we set $f(x,y)=- \frac{x^{2}}{9} + \frac{y^{2}}{16}$, our curve can be viewed as the level curve $f(x,y)=\frac{9}{16}.$  

A normal vector to the level curve that passes through the point $(0,3)$ can be found by computing $∇f(0,3).$ 

So, we find the gradient and evaluate it at $(0,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- \frac{x^{2}}{9} + \frac{y^{2}}{16})\,i+\frac{∂}{∂y}(- \frac{x^{2}}{9} + \frac{y^{2}}{16})\,j \\  & =(- \frac{2 x}{9})\,i+(\frac{y}{8})\,j \\ ∇f(0,3) & =(- \frac{2 (0)}{9})\,i+(\frac{(3)}{8})\,j \\  & =(0)\,i+(\frac{3}{8})\,j \\  & =⟨0,\frac{3}{8}⟩\end{aligned}
$$

Hence, $∇f(0,3)=⟨0,\frac{3}{8}⟩$ is a normal vector to the curve at $(0,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(0))(\frac{3}{8})-(y-(3))(0) & =0 \\ \frac{3 x}{8} & =0 \\ x & =0\end{aligned}
$$

## q-71386

### Original

Consider the plane curve $\frac{{x}^{2}}{9}+{y}^{2}=1.$  Find the equation of the normal line to the curve at the point $(3,0).$

- $y=3$
- $x=3$
- $x=0$
- $y=0$
- $x+y=3$

If we set $f(x,y)=\frac{{x}^{2}}{9}+{y}^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$  

A normal vector to the level curve that passes through the point $(3,0)$ can be found by computing $∇f(3,0).$ 

So, we find the gradient and evaluate it at $(3,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\frac{{x}^{2}}{9}+{y}^{2})\,i+\frac{∂}{∂y}(\frac{{x}^{2}}{9}+{y}^{2})\,j \\  & =\frac{2}{9}x\,i+2y\,j \\ ∇f(3,0) & =\frac{2}{9}(3)\,i+2(0)\,j \\  & =\frac{2}{3}\,i \\  & =⟨\frac{2}{3},0⟩\end{aligned}
$$

Hence, $∇f(3,0)=⟨\frac{2}{3},0⟩$ is a normal vector to the curve at $(3,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-3)0-(y-0)\frac{2}{3} & =0 \\ -\frac{2}{3}y & =0 \\ y & =0\end{aligned}
$$

### Generated variant 1 (hard)

Consider the plane curve $\frac{x^{2}}{9} + y^{2}=\frac{1}{9}.$  Find the equation of the normal line to the curve at the point $(-1,0).$

- $x + y + 1=0$
- $x=0$
- $x + 1=0$
- $y + 1=0$
- $y=0$

If we set $f(x,y)=\frac{x^{2}}{9} + y^{2}$, our curve can be viewed as the level curve $f(x,y)=\frac{1}{9}.$  

A normal vector to the level curve that passes through the point $(-1,0)$ can be found by computing $∇f(-1,0).$ 

So, we find the gradient and evaluate it at $(-1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\frac{x^{2}}{9} + y^{2})\,i+\frac{∂}{∂y}(\frac{x^{2}}{9} + y^{2})\,j \\  & =(\frac{2 x}{9})\,i+(2 y)\,j \\ ∇f(-1,0) & =(\frac{2 (-1)}{9})\,i+(2 (0))\,j \\  & =(- \frac{2}{9})\,i+(0)\,j \\  & =⟨- \frac{2}{9},0⟩\end{aligned}
$$

Hence, $∇f(-1,0)=⟨- \frac{2}{9},0⟩$ is a normal vector to the curve at $(-1,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(-1))(0)-(y-(0))(- \frac{2}{9}) & =0 \\ \frac{2 y}{9} & =0 \\ y & =0\end{aligned}
$$

### Generated variant 2 (hard)

Consider the plane curve $\frac{x^{2}}{9} + y^{2}=1.$  Find the equation of the normal line to the curve at the point $(3,0).$

- $x=0$
- $y=0$
- $x - 3=0$
- $y - 3=0$
- $x + y - 3=0$

If we set $f(x,y)=\frac{x^{2}}{9} + y^{2}$, our curve can be viewed as the level curve $f(x,y)=1.$  

A normal vector to the level curve that passes through the point $(3,0)$ can be found by computing $∇f(3,0).$ 

So, we find the gradient and evaluate it at $(3,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\frac{x^{2}}{9} + y^{2})\,i+\frac{∂}{∂y}(\frac{x^{2}}{9} + y^{2})\,j \\  & =(\frac{2 x}{9})\,i+(2 y)\,j \\ ∇f(3,0) & =(\frac{2 (3)}{9})\,i+(2 (0))\,j \\  & =(\frac{2}{3})\,i+(0)\,j \\  & =⟨\frac{2}{3},0⟩\end{aligned}
$$

Hence, $∇f(3,0)=⟨\frac{2}{3},0⟩$ is a normal vector to the curve at $(3,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0 \\ (x-(3))(0)-(y-(0))(\frac{2}{3}) & =0 \\ - \frac{2 y}{3} & =0 \\ y & =0\end{aligned}
$$

## q-71389

### Original

Consider the plane curve $\operatorname{cos}⁡(xy)={x}^{2}+y.$  Find the equation of the normal line to the curve at the point $(-1,0).$

- $x+2y+1=0$
- $2x+y+2=0$
- $x+y+1=0$
- $x-2y+1=0$
- $2x-y+2=0$

First, we bring all variables to one side:

$$
\begin{aligned}\operatorname{cos}⁡(xy) & ={x}^{2}+y \\ \operatorname{cos}⁡(xy)-{x}^{2}-y & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{cos}⁡(xy)-{x}^{2}-y$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(-1,0)$ can be found by computing $∇f(-1,0).$ 

So, we find the gradient and evaluate it at $(-1,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{cos}⁡(xy)-{x}^{2}-y)\,i+\frac{∂}{∂y}(\operatorname{cos}⁡(xy)-{x}^{2}-y)\,j \\  & =(-y\operatorname{sin}⁡(xy)-2x)\,i+(-x\operatorname{sin}⁡(xy)-1)\,j \\ ∇f(-1,0) & =(-0\cdot \operatorname{sin}⁡((-1)\cdot 0)-2\cdot (-1))\,i+(-(-1)\cdot \operatorname{sin}⁡((-1)\cdot 0)-1)\,j \\  & =2\,i-j \\  & =⟨2,-1⟩\end{aligned}
$$

Hence, $∇f(-1,0)=⟨2,-1⟩$ is a normal vector to the curve at $(-1,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-1)}{2} & =\frac{y-0}{-1} \\ \frac{x+1}{2} & =-y \\ x+1 & =-2y \\ x+2y+1 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $\cos{\left(x y \right)}=x^{2} + y - 8.$  Find the equation of the normal line to the curve at the point $(3,0).$

- $x - 6 y + 3=0$
- $x - 12 y - 3=0$
- $6 x + y - 18=0$
- $x - 6 y - 3=0$
- $x - 6 y=0$

First, we bring all variables to one side:

$$
\begin{aligned}\cos{\left(x y \right)} & =x^{2} + y - 8 \\ - x^{2} - y + \cos{\left(x y \right)} & =-8\end{aligned}
$$

If we set $f(x,y)=- x^{2} - y + \cos{\left(x y \right)}$, our curve can be viewed as the level curve $f(x,y)=-8.$  

A normal vector to the level curve that passes through the point $(3,0)$ can be found by computing $∇f(3,0).$ 

So, we find the gradient and evaluate it at $(3,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- x^{2} - y + \cos{\left(x y \right)})\,i+\frac{∂}{∂y}(- x^{2} - y + \cos{\left(x y \right)})\,j \\  & =(- 2 x - y \sin{\left(x y \right)})\,i+(- x \sin{\left(x y \right)} - 1)\,j \\ ∇f(3,0) & =(- 2 (3) - (0) \sin{\left((3) (0) \right)})\,i+(- (3) \sin{\left((3) (0) \right)} - 1)\,j \\  & =(-6)\,i+(-1)\,j \\  & =⟨-6,-1⟩\end{aligned}
$$

Hence, $∇f(3,0)=⟨-6,-1⟩$ is a normal vector to the curve at $(3,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(3)}{-6} & =\frac{y-(0)}{-1} \\ \frac{1}{2} - \frac{x}{6} & =- y \\ x - 3 & =6 y \\ x - 6 y - 3 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $\cos{\left(x y \right)}=x^{2} + y - 3.$  Find the equation of the normal line to the curve at the point $(-2,0).$

- $x + 8 y + 2=0$
- $x + 4 y=0$
- $4 x - y + 8=0$
- $x + 4 y + 2=0$
- $x + 4 y - 2=0$

First, we bring all variables to one side:

$$
\begin{aligned}\cos{\left(x y \right)} & =x^{2} + y - 3 \\ - x^{2} - y + \cos{\left(x y \right)} & =-3\end{aligned}
$$

If we set $f(x,y)=- x^{2} - y + \cos{\left(x y \right)}$, our curve can be viewed as the level curve $f(x,y)=-3.$  

A normal vector to the level curve that passes through the point $(-2,0)$ can be found by computing $∇f(-2,0).$ 

So, we find the gradient and evaluate it at $(-2,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(- x^{2} - y + \cos{\left(x y \right)})\,i+\frac{∂}{∂y}(- x^{2} - y + \cos{\left(x y \right)})\,j \\  & =(- 2 x - y \sin{\left(x y \right)})\,i+(- x \sin{\left(x y \right)} - 1)\,j \\ ∇f(-2,0) & =(- 2 (-2) - (0) \sin{\left((-2) (0) \right)})\,i+(- (-2) \sin{\left((-2) (0) \right)} - 1)\,j \\  & =(4)\,i+(-1)\,j \\  & =⟨4,-1⟩\end{aligned}
$$

Hence, $∇f(-2,0)=⟨4,-1⟩$ is a normal vector to the curve at $(-2,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-2)}{4} & =\frac{y-(0)}{-1} \\ \frac{x}{4} + \frac{1}{2} & =- y \\ x + 2 & =- 4 y \\ x + 4 y + 2 & =0\end{aligned}
$$

## q-130719

### Original

Consider the plane curve $2y-x=\operatorname{ln}⁡(\frac{x}{2y}).$  Find the equation of the normal line to the curve at the point $(2,1).$

- $x+y-3=0$
- $2x-y-3=0$
- $2x+y-5=0$
- $x+2y-4=0$
- $x-y-1=0$

First, we bring all variables to one side:

$$
\begin{aligned}2y-x & =\operatorname{ln}⁡(\frac{x}{2y}) \\ \operatorname{ln}⁡(\frac{x}{2y})-2y+x & =0\end{aligned}
$$

If we set $f(x,y)=\operatorname{ln}⁡(\frac{x}{2y})-2y+x,$ our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(2,1)$ can be found by computing $∇f(2,1).$ 

So, we find the gradient and evaluate it at $(2,1):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(\frac{x}{2y})-2y+x)i+\frac{∂}{∂y}(\operatorname{ln}⁡(\frac{x}{2y})-2y+x)j \\  & =(\frac{2y}{x}\cdot \frac{1}{2y}+1)i+(\frac{2y}{x}\cdot (-\frac{x}{2{y}^{2}})-2)j \\  & =(\frac{1}{x}+1)i+(-\frac{1}{y}-2)j \\ ∇f(2,1) & =(\frac{1}{2}+1)i+(-\frac{1}{1}-2)j \\  & =\frac{3}{2}\,i-3\,j \\  & =⟨\frac{3}{2},-3⟩\end{aligned}
$$

Hence, $∇f(3,1)=⟨\frac{3}{2},-3⟩$ is a normal vector to the curve at $(2,1).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-2}{(\frac{3}{2})} & =\frac{y-1}{(-3)} \\ -3(x-2) & =\frac{3}{2}(y-1) \\ -6(x-2) & =3(y-1) \\ -2(x-2) & =y-1 \\ -2x+4 & =y-1 \\ 2x+y-5 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $- x + 2 y=\ln{\left(\frac{x}{2 y} \right)}.$  Find the equation of the normal line to the curve at the point $(6,3).$

- $2 x + y + 15=0$
- $x + y - 9=0$
- $x - 2 y=0$
- $2 x + y - 15=0$
- $2 x + y=0$

First, we bring all variables to one side:

$$
\begin{aligned}- x + 2 y & =\ln{\left(\frac{x}{2 y} \right)} \\ x - 2 y + \ln{\left(\frac{x}{2 y} \right)} & =0\end{aligned}
$$

If we set $f(x,y)=x - 2 y + \ln{\left(\frac{x}{2 y} \right)}$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(6,3)$ can be found by computing $∇f(6,3).$ 

So, we find the gradient and evaluate it at $(6,3):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x - 2 y + \ln{\left(\frac{x}{2 y} \right)})\,i+\frac{∂}{∂y}(x - 2 y + \ln{\left(\frac{x}{2 y} \right)})\,j \\  & =(\frac{2y}{x}\cdot\frac{1}{2y}+1)i+(\frac{2y}{x}\cdot(-\frac{x}{2y^2})-2)j \\  & =(1 + \frac{1}{x})\,i+(-2 - \frac{1}{y})\,j \\ ∇f(6,3) & =(1 + \frac{1}{(6)})\,i+(-2 - \frac{1}{(3)})\,j \\  & =(\frac{7}{6})\,i+(- \frac{7}{3})\,j \\  & =⟨\frac{7}{6},- \frac{7}{3}⟩\end{aligned}
$$

Hence, $∇f(6,3)=⟨\frac{7}{6},- \frac{7}{3}⟩$ is a normal vector to the curve at $(6,3).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(6)}{\frac{7}{6}} & =\frac{y-(3)}{- \frac{7}{3}} \\ (- \frac{7}{3})(x-(6)) & =(\frac{7}{6})(y-(3)) \\ (- \frac{14}{3})(x-(6)) & =(\frac{7}{3})(y-(3)) \\ (-2)(x-(6)) & =(1)(y-(3)) \\ 12 - 2 x & =y - 3 \\ 2 x + y - 15 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $- x + 2 y=\ln{\left(\frac{x}{2 y} \right)}.$  Find the equation of the normal line to the curve at the point $(-4,-2).$

- $x + y + 6=0$
- $2 x + y=0$
- $x - 2 y=0$
- $2 x + y + 10=0$
- $2 x + y - 10=0$

First, we bring all variables to one side:

$$
\begin{aligned}- x + 2 y & =\ln{\left(\frac{x}{2 y} \right)} \\ x - 2 y + \ln{\left(\frac{x}{2 y} \right)} & =0\end{aligned}
$$

If we set $f(x,y)=x - 2 y + \ln{\left(\frac{x}{2 y} \right)}$, our curve can be viewed as the level curve $f(x,y)=0.$  

A normal vector to the level curve that passes through the point $(-4,-2)$ can be found by computing $∇f(-4,-2).$ 

So, we find the gradient and evaluate it at $(-4,-2):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x - 2 y + \ln{\left(\frac{x}{2 y} \right)})\,i+\frac{∂}{∂y}(x - 2 y + \ln{\left(\frac{x}{2 y} \right)})\,j \\  & =(\frac{2y}{x}\cdot\frac{1}{2y}+1)i+(\frac{2y}{x}\cdot(-\frac{x}{2y^2})-2)j \\  & =(1 + \frac{1}{x})\,i+(-2 - \frac{1}{y})\,j \\ ∇f(-4,-2) & =(1 + \frac{1}{(-4)})\,i+(-2 - \frac{1}{(-2)})\,j \\  & =(\frac{3}{4})\,i+(- \frac{3}{2})\,j \\  & =⟨\frac{3}{4},- \frac{3}{2}⟩\end{aligned}
$$

Hence, $∇f(-4,-2)=⟨\frac{3}{4},- \frac{3}{2}⟩$ is a normal vector to the curve at $(-4,-2).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-4)}{\frac{3}{4}} & =\frac{y-(-2)}{- \frac{3}{2}} \\ (- \frac{3}{2})(x-(-4)) & =(\frac{3}{4})(y-(-2)) \\ (-3)(x-(-4)) & =(\frac{3}{2})(y-(-2)) \\ (-2)(x-(-4)) & =(1)(y-(-2)) \\ - 2 x - 8 & =y + 2 \\ 2 x + y + 10 & =0\end{aligned}
$$

## q-130721

### Original

Consider the plane curve ${e}^{{x}^{2}y}={y}^{2}-{x}^{3}+9.$  Find the equation of the normal line to the curve at the point $(2,0).$

- $2x+3y-4=0$
- $2x-y-4=0$
- $x+2y-2=0$
- $x-3y-2=0$
- $x+3y-2=0$

First, we bring all variables to one side:

$$
\begin{aligned}{e}^{{x}^{2}y} & ={y}^{2}-{x}^{3}+9 \\ {e}^{{x}^{2}y}-{y}^{2}+{x}^{3} & =9\end{aligned}
$$

If we set $f(x,y)={e}^{{x}^{2}y}-{y}^{2}+{x}^{3}$, our curve can be viewed as the level curve $f(x,y)=9.$  

A normal vector to the level curve that passes through the point $(2,0)$ can be found by computing $∇f(2,0).$ 

So, we find the gradient and evaluate it at $(2,0):$ 

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}({e}^{{x}^{2}y}-{y}^{2}+{x}^{3})i+\frac{∂}{∂y}({e}^{{x}^{2}y}-{y}^{2}+{x}^{3})j \\  & =(2xy{e}^{{x}^{2}y}+3{x}^{2})i+({x}^{2}{e}^{{x}^{2}y}-2y)j \\ ∇f(2,0) & =(2(2)(0){e}^{({2}^{2})(0)}+3({2}^{2}))i+(({2}^{2}){e}^{({2}^{2})(0)}-2(0))j \\  & =12\,i+4\,j \\  & =⟨12,4⟩\end{aligned}
$$

Hence, $∇f(2,0)=⟨12,4⟩$ is a normal vector to the curve at $(2,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-2}{12} & =\frac{y-0}{4} \\ 4(x-2) & =12y \\ x-2 & =3y \\ x-3y-2 & =0\end{aligned}
$$

### Generated variant 1 (moderate)

Consider the plane curve $e^{x^{2} y}=- x^{3} + y^{2} + 28.$  Find the equation of the normal line to the curve at the point $(3,0).$

- $x - 3 y + 3=0$
- $x - 6 y - 3=0$
- $3 x + y - 9=0$
- $x - 3 y - 3=0$
- $x - 3 y=0$

First, we bring all variables to one side:

$$
\begin{aligned}e^{x^{2} y} & =- x^{3} + y^{2} + 28 \\ x^{3} - y^{2} + e^{x^{2} y} & =28\end{aligned}
$$

If we set $f(x,y)=x^{3} - y^{2} + e^{x^{2} y}$, our curve can be viewed as the level curve $f(x,y)=28.$  

A normal vector to the level curve that passes through the point $(3,0)$ can be found by computing $∇f(3,0).$ 

So, we find the gradient and evaluate it at $(3,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{3} - y^{2} + e^{x^{2} y})\,i+\frac{∂}{∂y}(x^{3} - y^{2} + e^{x^{2} y})\,j \\  & =(3 x^{2} + 2 x y e^{x^{2} y})\,i+(x^{2} e^{x^{2} y} - 2 y)\,j \\ ∇f(3,0) & =(3 (3)^{2} + 2 (3) (0) e^{(3)^{2} (0)})\,i+((3)^{2} e^{(3)^{2} (0)} - 2 (0))\,j \\  & =(27)\,i+(9)\,j \\  & =⟨27,9⟩\end{aligned}
$$

Hence, $∇f(3,0)=⟨27,9⟩$ is a normal vector to the curve at $(3,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(3)}{27} & =\frac{y-(0)}{9} \\ (9)(x-(3)) & =(27)(y-(0)) \\ (1)(x-(3)) & =(3)(y-(0)) \\ x - 3 y - 3 & =0\end{aligned}
$$

### Generated variant 2 (moderate)

Consider the plane curve $e^{x^{2} y}=- x^{3} + y^{2} - 7.$  Find the equation of the normal line to the curve at the point $(-2,0).$

- $x - 6 y + 2=0$
- $x - 3 y=0$
- $3 x + y + 6=0$
- $x - 3 y + 2=0$
- $x - 3 y - 2=0$

First, we bring all variables to one side:

$$
\begin{aligned}e^{x^{2} y} & =- x^{3} + y^{2} - 7 \\ x^{3} - y^{2} + e^{x^{2} y} & =-7\end{aligned}
$$

If we set $f(x,y)=x^{3} - y^{2} + e^{x^{2} y}$, our curve can be viewed as the level curve $f(x,y)=-7.$  

A normal vector to the level curve that passes through the point $(-2,0)$ can be found by computing $∇f(-2,0).$ 

So, we find the gradient and evaluate it at $(-2,0):$

$$
\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & =\frac{∂}{∂x}(x^{3} - y^{2} + e^{x^{2} y})\,i+\frac{∂}{∂y}(x^{3} - y^{2} + e^{x^{2} y})\,j \\  & =(3 x^{2} + 2 x y e^{x^{2} y})\,i+(x^{2} e^{x^{2} y} - 2 y)\,j \\ ∇f(-2,0) & =(3 (-2)^{2} + 2 (-2) (0) e^{(-2)^{2} (0)})\,i+((-2)^{2} e^{(-2)^{2} (0)} - 2 (0))\,j \\  & =(12)\,i+(4)\,j \\  & =⟨12,4⟩\end{aligned}
$$

Hence, $∇f(-2,0)=⟨12,4⟩$ is a normal vector to the curve at $(-2,0).$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}} \\ \frac{x-(-2)}{12} & =\frac{y-(0)}{4} \\ (4)(x-(-2)) & =(12)(y-(0)) \\ (1)(x-(-2)) & =(3)(y-(0)) \\ x - 3 y + 2 & =0\end{aligned}
$$

