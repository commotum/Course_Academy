# Originals and generated variants

Raw originals below retain all fields, refs, banks and source prose; every raw profile is evidence-only. Generated records are labeled and use authored complete banks.

## Original evidence — q-36343

Find a vector equation of the normal line to the surface $\frac{{x}^{2}}{4}-{y}^{2}={z}^{2}$ at the point $(2,0,1).$

Field 0 (:answer-field.type/radio)

- $r=⟨1,0,-2⟩+t\,⟨2,0,1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,0,1⟩+t\,⟨2,1,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,0,1⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨2,0,1⟩+t\,⟨2,0,1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨1,0,-2⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}\frac{{x}^{2}}{4}-{y}^{2} & ={z}^{2} \\ \frac{{x}^{2}}{4}-{y}^{2}-{z}^{2} & =0\end{aligned}
$$

If we set $f(x,y,z)=\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(2,0,1)$ can be found by computing $∇f(2,0,1).$ 

So, we find the gradient and evaluate it at $(2,0,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})i+\frac{∂}{∂y}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})j+\frac{∂}{∂z}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})k \\  & =\frac{x}{2}\text{ }i-2y\text{ }j-2z\text{ }k \\ ∇f(2,0,1) & =\frac{(2)}{2}\,i-2(0)\text{ }j-2(1)\,k \\  & =i-2\,k \\  & =⟨1,0,-2⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,0,1)$ and passes through the point $(2,0,1)$ can be written as

$$
\begin{aligned}r & =⟨2,0,1⟩+t\,∇f(2,0,1)=⟨2,0,1⟩+t\,⟨1,0,-2⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Original evidence — q-37515

Find the equation of the normal line to the surface $z=\operatorname{sin}⁡(xy)+{y}^{2}$ at the point $(0,-1,1).$

Field 0 (:answer-field.type/radio)

- $x =-\frac{y + 1}{2} = \frac{z - 1}{2}$
- $x = y + 1 = z - 1$
- $x = \frac{y + 1}{2} = z - 1$
- $-\frac{x}{2} = \frac{y + 1}{2} = z$
- $x =-y - 1 = \frac{z - 1}{2}$

Field 1 (:answer-field.type/radio)

- $x=-y-1=\frac{z-1}{2}$
- $x=\frac{y+1}{2}=z-1$ **keyed**
- $-\frac{x}{2}=\frac{y+1}{2}=z$
- $x=-\frac{y+1}{2}=\frac{z-1}{2}$
- $x=y+1=z-1$

First, we bring all variables to one side:

$$
\begin{aligned}z & =\operatorname{sin}⁡(xy)+{y}^{2} \\ 0 & =\operatorname{sin}⁡(xy)+{y}^{2}-z\end{aligned}
$$

If we set $f(x,y,z)=\operatorname{sin}⁡(xy)+{y}^{2}-z$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(0,-1,1)$ can be found by computing $∇f(0,-1,1).$ 

So, we find the gradient and evaluate it at $(0,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{sin}⁡(xy)+{y}^{2}-z)i+\frac{∂}{∂y}(\operatorname{sin}⁡(xy)+{y}^{2}-z)j+\frac{∂}{∂z}(\operatorname{sin}⁡(xy)+{y}^{2}-z)k \\  & =y\operatorname{cos}⁡(xy)\text{ }i+(x\operatorname{cos}⁡(xy)+2y)\text{ }j-\text{ }k \\ ∇f(0,-1,1) & =(-1)\operatorname{cos}⁡(0)\text{ }i+[(0)\operatorname{cos}⁡(0)+2(-1)]\text{ }j-\text{ }k \\  & =-i-2\,j-k \\  & =⟨-1,-2,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-0}{-1}=\frac{y-(-1)}{-2}=\frac{z-1}{-1} \\ \frac{x}{-1}=\frac{y+1}{-2}=\frac{z-1}{-1} \\ \frac{x}{1}=\frac{y+1}{2}=\frac{z-1}{1} \\ x=\frac{y+1}{2}=z-1\end{aligned}
$$

## Original evidence — q-131126

Find a vector equation of the normal line to the surface ${x}^{2}y+{y}^{2}z+{z}^{2}x=5$ at the point $(1,-1,2).$

Field 0 (:answer-field.type/radio)

- $⟨2,3,-5⟩+t\,⟨1,-1,2⟩,\,t\in (-\infty ,\infty )$
- $⟨1,-1,2⟩+t\,⟨-2,5,-3⟩,\,t\in (-\infty ,\infty )$
- $⟨-2,5,-3⟩+t\,⟨1,-1,2⟩,\,t\in (-\infty ,\infty )$
- $⟨1,-1,2⟩+t\,⟨2,-3,5⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨1,-1,2⟩+t\,⟨4,5,-5⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)={x}^{2}y+{y}^{2}z+{z}^{2}x.$ Then, our surface can be viewed as the level surface $f(x,y,z)=5.$ 

A normal vector to the level surface that passes through the point $(1,-1,2)$ can be found by computing $∇f(1,-1,2).$ 

So, we find the gradient and evaluate it at $(1,-1,2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}y+{y}^{2}z+{z}^{2}x)i+\frac{∂}{∂y}({x}^{2}y+{y}^{2}z+{z}^{2}x)j+\frac{∂}{∂z}({x}^{2}y+{y}^{2}z+{z}^{2}x)k \\  & =(2xy+{z}^{2})\,i+({x}^{2}+2yz)\,j+({y}^{2}+2zx)\,k \\ ∇f(1,-1,2) & =(2(1)(-1)+(2)^{2})\text{ }i+((1)^{2}+2(-1)(2))\text{ }j+((-1)^{2}+2(2)(1))\text{ }k \\  & =2\,i-3\,j+5\,k \\  & =⟨2,-3,5⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(1,-1,2)$ and passes through the point $(1,-1,2)$ can be written as

$$
\begin{aligned}r & =⟨1,-1,2⟩+t\,∇f(1,-1,2)=⟨1,-1,2⟩+t\,⟨2,-3,5⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Original evidence — q-131127

Find a vector equation of the normal line to the surface ${z}^{2}\operatorname{sin}⁡({x}^{2}y)={x}^{2}z+y-\frac{\pi }{2}$ at the point $(-1,\frac{\pi }{2},1).$

Field 0 (:answer-field.type/radio)

- $⟨2,-1,1⟩+t\,⟨-1,\frac{\pi }{2},1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi }{2},1⟩+t\,⟨2,-1,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨-1,\frac{\pi }{2},1⟩+t\,⟨2,1,-1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi }{2},1⟩+t\,⟨1,1,-1⟩,\,t\in (-\infty ,\infty )$
- $⟨2,1,-1⟩+t\,⟨-1,\frac{\pi }{2},1⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}{z}^{2}\operatorname{sin}⁡({x}^{2}y) & ={x}^{2}z+y-\frac{\pi }{2} \\ {z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y & =-\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y,z)={z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y,$ our surface can be viewed as the level surface $f(x,y,z)=-\frac{\pi }{2}.$ 

A normal vector to the level surface that passes through the point $(-1,\frac{\pi }{2},1)$ can be found by computing $∇f(-1,\frac{\pi }{2},1).$ 

So, we find the gradient and evaluate it at $(-1,\frac{\pi }{2},1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)i+\frac{∂}{∂y}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)j+\frac{∂}{∂z}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)k \\  & =(2xy{z}^{2}\operatorname{cos}⁡({x}^{2}y)-2xz)i+({x}^{2}{z}^{2}\operatorname{cos}⁡({x}^{2}y)-1)j+(2z\operatorname{sin}⁡({x}^{2}y)-{x}^{2})k \\ ∇f(-1,\frac{\pi }{2},1) & =(2(-1)(\frac{\pi }{2})(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-2(-1)(1))i+((-1)^{2}(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-1)j+(2(1)\operatorname{sin}⁡((-1)^{2}\frac{\pi }{2})-(-1)^{2})k \\  & =(-\pi \operatorname{cos}⁡(\frac{\pi }{2})+2)i+(\operatorname{cos}⁡(\frac{\pi }{2})-1)j+(2\operatorname{sin}⁡(\frac{\pi }{2})-1)k \\  & =2\,i-j+k \\  & =⟨2,-1,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-1,\frac{\pi }{2},1)$ and passes through the point $(-1,\frac{\pi }{2},1)$ can be written as

$$
\begin{aligned}r & =⟨-1,\frac{\pi }{2},1⟩+t\,∇f(-1,\frac{\pi }{2},1)=⟨-1,\frac{\pi }{2},1⟩+t\,⟨2,-1,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Original evidence — q-131128

Find the equation of the normal line to the surface ${x}^{2}yz=-4$ at the point $(2,-1,1).$

Field 0 (:answer-field.type/radio)

- $x-2=y+1=1-z$
- $2-x=y+1=1-z$ **keyed**
- $x-2=\frac{y+1}{2}=\frac{z-1}{3}$
- $\frac{x-2}{2}=\frac{y+1}{3}=\frac{z-1}{4}$
- $x-2=y+1=z-1$

Let's set $f(x,y,z)={x}^{2}yz.$ Then, our surface can be viewed as the level surface $f(x,y,z)=-4.$ 

A normal vector to the level surface that passes through the point $(2,-1,1)$ can be found by computing $∇f(2,-1,1).$ 

So, we find the gradient and evaluate it at $(2,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}yz)i+\frac{∂}{∂y}({x}^{2}yz)j+\frac{∂}{∂z}({x}^{2}yz)k \\  & =2xyz\text{ }i+{x}^{2}z\text{ }j+{x}^{2}y\,k \\ ∇f(2,-1,1) & =2(2)(-1)(1)\text{ }i+(2)^{2}(1)\text{ }j+(2)^{2}(-1)\text{ }k \\  & =-4\,i+4\,j-4\,k \\  & =⟨-4,4,-4⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{(-4)}=\frac{y-(-1)}{4}=\frac{z-1}{(-4)} \\ \frac{x-2}{(-1)}=\frac{y+1}{1}=\frac{z-1}{(-1)} \\ 2-x=y+1=1-z\end{aligned}
$$

## Original evidence — q-131130

Find the equation of the normal line to the surface $x={y}^{2}-{z}^{2}$ at the point $(3,2,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x-1}{4}=2-y=z-1$
- $x-1=y-2=z-1$
- $x-3=\frac{y-2}{2}=z-1$
- $\frac{x-3}{2}=\frac{y-2}{4}=z-1$
- $x-3=\frac{2-y}{4}=\frac{z-1}{2}$ **keyed**

First, we bring all variables to one side:

$$
\begin{aligned}x & ={y}^{2}-{z}^{2} \\ {y}^{2}-{z}^{2}-x & =0\end{aligned}
$$

If we set $f(x,y,z)={y}^{2}-{z}^{2}-x$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(3,2,1)$ can be found by computing $∇f(3,2,1).$ 

So, we find the gradient and evaluate it at $(3,2,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({y}^{2}-{z}^{2}-x)i+\frac{∂}{∂y}({y}^{2}-{z}^{2}-x)j+\frac{∂}{∂z}({y}^{2}-{z}^{2}-x)k \\  & =-i+2y\,j-2z\,k \\ ∇f(3,2,1) & =-i+2(2)\,j-2(1)\,k \\  & =-i+4\,j-2\,k \\  & =⟨-1,4,-2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-3}{(-1)}=\frac{y-2}{4}=\frac{z-1}{(-2)} \\ \frac{x-3}{1}=\frac{y-2}{-4}=\frac{z-1}{2} \\ x-3=\frac{2-y}{4}=\frac{z-1}{2}\end{aligned}
$$

## Original evidence — q-71411

Find the equation of the normal line to the surface $3{x}^{2}-xz=6-3xyz$ at the point $(1,0,-3).$

Field 0 (:answer-field.type/radio)

- $\frac{x-1}{9}=\frac{y}{-9}=\frac{z-3}{-1}$
- $\frac{x-1}{9}=\frac{y}{9}=\frac{z+3}{-1}$
- $\frac{x-1}{9}=\frac{y}{-9}=\frac{z+3}{-1}$ **keyed**
- $\frac{x-1}{9}=\frac{y}{-9}=z-3$
- $\frac{x-1}{9}=\frac{y}{9}=z+3$

First, we bring all variables to one side:

$$
\begin{aligned}3{x}^{2}-xz & =6-3xyz \\ 3{x}^{2}-xz+3xyz & =6\end{aligned}
$$

If we set $f(x,y,z)=3{x}^{2}-xz+3xyz$, our surface can be viewed as the level surface $f(x,y,z)=6.$ 

A normal vector to the level surface that passes through the point $(1,0,-3)$ can be found by computing $∇f(1,0,-3).$ 

So, we find the gradient and evaluate it at $(1,0,-3):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(3{x}^{2}-xz+3xyz)i+\frac{∂}{∂y}(3{x}^{2}-xz+3xyz)j+\frac{∂}{∂z}(3{x}^{2}-xz+3xyz)k \\  & =(6x-z+3yz)\text{ }i+3xz\text{ }j+(-x+3xy)\text{ }k \\ ∇f(1,0,-3) & =(6(1)-(-3)+3(0)(-3))\text{ }i+3(1)(-3)\text{ }j+(-1+3(1)(0))\text{ }k \\  & =9\,i-9\,j-k \\  & =⟨9,-9,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-1}{9}=\frac{y-0}{-9}=\frac{z-(-3)}{-1} \\ \frac{x-1}{9}=\frac{y}{-9}=\frac{z+3}{-1}\end{aligned}
$$

## Original evidence — q-36351

Find the equation of the normal line to the surface $z=\operatorname{ln}⁡(2x+y)$ at the point $(1,-1,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x-1}{2}=\frac{y+1}{2}=-z$
- $x-1=\frac{y}{2}=-z$
- $\frac{x-1}{2}=y+1=-z$ **keyed**
- $x-1=\frac{y+1}{2}=z$
- $\frac{x+1}{2}=\frac{y-1}{2}=z$

First, we bring all variables to one side:

$$
\begin{aligned}z & =\operatorname{ln}⁡(2x+y) \\ 0 & =\operatorname{ln}⁡(2x+y)-z\end{aligned}
$$

 

So, if we set $f(x,y,z)=\operatorname{ln}⁡(2x+y)-z$, then our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(1,-1,0)$ can be found by computing $∇f(1,-1,0).$

So, we find the gradient and evaluate it at $(1,-1,0):$ 

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(2x+y)-z)i+\frac{∂}{∂y}(\operatorname{ln}⁡(2x+y)-z)j+\frac{∂}{∂z}(\operatorname{ln}⁡(2x+y)-z)k \\  & =\frac{2}{2x+y}\text{ }i+\frac{1}{2x+y}\text{ }j-1\text{ }k \\ ∇f(1,-1,0) & =\frac{2}{2(1)+(-1)}\text{ }i+\frac{1}{2(1)+(-1)}\text{ }j-k \\  & =2\text{ }i+\,j-k \\  & =⟨2,\,1,\,-1⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-1}{2}=\frac{y-(-1)}{1}=\frac{z-0}{-1} \\ \frac{x-1}{2}=y+1=-z\end{aligned}
$$

## Original evidence — q-71408

Find the equation of the normal line to the surface ${x}^{2}+{y}^{2}+{z}^{2}=3$ at the point $(-1,-1,1).$

Field 0 (:answer-field.type/radio)

- $x-1=y+1=\frac{z-1}{-1}$
- $x+1=y+1=\frac{z+1}{-1}$
- $x+1=y-1=z-1$
- $x+1=y+1=z-1$
- $x+1=y+1=\frac{z-1}{-1}$ **keyed**

If we set $f(x,y,z)={x}^{2}+{y}^{2}+{z}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=3.$ 

A normal vector to the level surface that passes through the point $(-1,-1,1)$ can be found by computing $∇f(-1,-1,1).$ 

So, we find the gradient and evaluate it at $(-1,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}+{y}^{2}+{z}^{2})i+\frac{∂}{∂y}({x}^{2}+{y}^{2}+{z}^{2})j+\frac{∂}{∂z}({x}^{2}+{y}^{2}+{z}^{2})k \\  & =2x\text{ }i+2y\text{ }j+2z\text{ }k \\ ∇f(-1,-1,1) & =2(-1)\text{ }i+2(-1)\text{ }j+2(1)\text{ }k \\  & =-2\,i-2\,j+2\,k \\  & =⟨-2,-2,2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-(-1)}{-2}=\frac{y-(-1)}{-2}=\frac{z-1}{2} \\ \frac{x+1}{-2}=\frac{y+1}{-2}=\frac{z-1}{2} \\ \frac{x+1}{1}=\frac{y+1}{1}=\frac{z-1}{-1} \\ x+1=y+1=\frac{z-1}{-1}\end{aligned}
$$

## Original evidence — q-131124

Find a vector equation of the normal line to the surface $4{z}^{2}-4{y}^{2}={x}^{2}-6x+12$ at the point $(2,0,1).$

Field 0 (:answer-field.type/radio)

- $⟨2,0,1⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨2,0,1⟩+t\,⟨2,0,4⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,1⟩+t\,⟨4,-1,8⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,8⟩+t\,⟨-1,3,1⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,8⟩+t\,⟨2,0,1⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}4{z}^{2}-4{y}^{2} & ={x}^{2}-6x \\ 4{z}^{2}-4{y}^{2}-{x}^{2}+6x & =12\end{aligned}
$$

If we set $f(x,y,z)=4{z}^{2}-4{y}^{2}-{x}^{2}+6x$, our surface can be viewed as the level surface $f(x,y,z)=12.$ 

A normal vector to the level surface that passes through the point $(2,0,1)$ can be found by computing $∇f(2,0,1).$ 

So, we find the gradient and evaluate it at $(2,0,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)i+\frac{∂}{∂y}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)j+\frac{∂}{∂z}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)k \\  & =(6-2x)\,i-8y\,j+8z\,k \\ ∇f(2,0,1) & =(6-2(2))\,i-8(0)\text{ }j+8(1)\,k \\  & =2\,i+8\,k \\  & =⟨2,0,8⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,0,1)$ and passes through the point $(2,0,1)$ can be written as

$$
\begin{aligned}r & =⟨2,0,1⟩+t\,∇f(2,0,1)=⟨2,0,1⟩+t\,⟨2,0,8⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Original evidence — q-131129

Find the equation of the normal line to the surface ${e}^{x+y+z}-2xyz=-3$ at the point $(2,-1,-1).$

Field 0 (:answer-field.type/radio)

- $2-x=\frac{y+1}{5}=\frac{z+1}{5}$ **keyed**
- $x-2=y+1=\frac{z+1}{5}$
- $\frac{x-2}{2}=y+1=\frac{z+1}{5}$
- $\frac{2-x}{2}=\frac{y+1}{3}=z+1$
- $2-x=y+1=z+1$

Let's set $f(x,y,z)={e}^{x+y+z}-2xyz.$ Then, our surface can be viewed as the level surface $f(x,y,z)=-3.$ 

A normal vector to the level surface that passes through the point $(2,-1,-1)$ can be found by computing $∇f(2,-1,-1).$ 

So, we find the gradient and evaluate it at $(2,-1,-1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({e}^{x+y+z}-2xyz)i+\frac{∂}{∂y}({e}^{x+y+z}-2xyz)j+\frac{∂}{∂z}({e}^{x+y+z}-2xyz)k \\  & =({e}^{x+y+z}-2yz)\text{ }i+({e}^{x+y+z}-2xz)\text{ }j+({e}^{x+y+z}-2xy)\text{ }k \\ ∇f(2,-1,-1) & =({e}^{2-1-1}-2(-1)(-1))\text{ }i+({e}^{2-1-1}-2(2)(-1))\text{ }j+({e}^{2-1-1}-2(2)(-1))\text{ }k \\  & =({e}^{0}-2)\text{ }i+({e}^{0}+4)\text{ }j+({e}^{0}+4)\text{ }k \\  & =-i+5\,j+5\,k \\  & =⟨-1,5,5⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{(-1)}=\frac{y-(-1)}{5}=\frac{z-(-1)}{5} \\ \frac{x-2}{(-1)}=\frac{y+1}{5}=\frac{z+1}{5} \\ 2-x=\frac{y+1}{5}=\frac{z+1}{5}\end{aligned}
$$

## Original evidence — q-37232

Find the equation of the normal line to the surface $\sqrt{2{x}^{2}+y-4z}=1$ at the point $(2,1,2).$

Field 0 (:answer-field.type/radio)

- $\frac{x-2}{4}=\frac{y-1}{3}=\frac{2-z}{2}$
- $\frac{x-2}{4}=2y-2=\frac{2-z}{2}$ **keyed**
- $\frac{x-2}{4}=2y-2=\frac{z-2}{2}$
- $\frac{x-2}{2}=2y-2=\frac{2-z}{2}$
- $\frac{x-2}{4}=y-1=\frac{2-z}{4}$

Let's set $f(x,y,z)=\sqrt{2{x}^{2}+y-4z}.$ Then, our surface can be viewed as the level surface $f(x,y,z)=1.$     

A normal vector to the level surface that passes through the point $(2,1,2)$ can be found by computing $∇f(2,1,2).$

So, we find the gradient and evaluate it at $(2,1,2):$    

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\sqrt{2{x}^{2}+y-4z})\text{ }i+\frac{∂}{∂y}(\sqrt{2{x}^{2}+y-4z})\text{ }j+\frac{∂}{∂z}(\sqrt{2{x}^{2}+y-4z})\text{ }k \\  & =\frac{2x}{\sqrt{2{x}^{2}+y-4z}}\text{ }i+\frac{1}{2\sqrt{2{x}^{2}+y-4z}}\text{ }j-\frac{2}{\sqrt{2{x}^{2}+y-4z}}\text{ }k \\ ∇f(2,1,2) & =\frac{2\cdot 2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }i+\frac{1}{2\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }j-\frac{2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }k \\  & =4\text{ }i+\frac{1}{2}\text{ }j-2\text{ }k \\  & =⟨4,\,\frac{1}{2},\,-2⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{4}=\frac{y-1}{\frac{1}{2}}=\frac{z-2}{-2} \\ \frac{x-2}{4}=2y-2=\frac{2-z}{2}\end{aligned}
$$

## Original evidence — q-71407

Find a vector equation of the normal line to the surface $z=2{x}^{2}+2{y}^{2}+x$ at the point $(\frac{1}{2},1,3).$

Field 0 (:answer-field.type/radio)

- $r=⟨-3,-4,1⟩+t\,⟨\frac{1}{2},1,3⟩$
- $r=⟨3,-4,1⟩+t\,⟨\frac{1}{2},1,3⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨3,4,1⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨3,-4,1⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨-3,-4,1⟩$ **keyed**

First, we bring all variables to one side:

$$
\begin{aligned}z & =2{x}^{2}+2{y}^{2}+x \\ z-2{x}^{2}-2{y}^{2}-x & =0\end{aligned}
$$

If we set $f(x,y,z)=z-2{x}^{2}-2{y}^{2}-x$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(\frac{1}{2},1,3)$ can be found by computing $∇f(\frac{1}{2},1,3).$ 

So, we find the gradient and evaluate it at $(\frac{1}{2},1,3):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(z-2{x}^{2}-2{y}^{2}-x)i+\frac{∂}{∂y}(z-2{x}^{2}-2{y}^{2}-x)j+\frac{∂}{∂z}(z-2{x}^{2}-2{y}^{2}-x)k \\  & =(-4x-1)\text{ }i-4y\text{ }j+k \\ ∇f(\frac{1}{2},1,3) & =(-4(\frac{1}{2})-1)\,i-4(1)\text{ }j+k \\  & =-3\,i-4\,j+k \\  & =⟨-3,-4,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(\frac{1}{2},1,3)$ and passes through the point $(\frac{1}{2},1,3)$ can be written as

$$
\begin{aligned}r & =⟨\frac{1}{2},1,3⟩+t\,∇f(\frac{1}{2},1,3)=⟨\frac{1}{2},1,3⟩+t\,⟨-3,-4,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Original evidence — q-36754

Find a vector equation of the normal line to the surface ${x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}=1$ at the point $(0,0,2),$ with parameter $t=0$ at this point.

Field 0 (:answer-field.type/radio)

- $⟨0,\,0,\,1⟩+t\,⟨0,\,0,\,1⟩,\,t\in (-\infty ,\infty )$
- $⟨0,\,0,\,2⟩+t\,⟨0,\,0,\,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨0,\,0,\,1⟩+t\,⟨0,\,0,\,2⟩,\,t\in (-\infty ,\infty )$
- $⟨0,\,0,\,2⟩+t\,⟨0,\,-1,\,1⟩,\,t\in (-\infty ,\infty )$
- $⟨0,\,0,\,-2⟩+t\,⟨1,\,0,\,1⟩,\,t\in (-\infty ,\infty )$

First, note that we can write the equation of our surface as

$$
\begin{aligned}{x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1=0\end{aligned}
$$

So, if we set $f(x,y,z)={x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1$, our surface can be viewed as the level surface $f(x,y,z)=0.$  

A normal vector to the level surface that passes through the point $(0,0,2)$ can be found by computing $∇f(0,0,2).$ 

So, we find the gradient and evaluate it at $(0,0,2):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)i+\frac{∂}{∂y}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)j+\frac{∂}{∂z}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)k \\  & =2x\text{ }i+\frac{2y}{9}\text{ }j+\frac{z}{2}\text{ }k \\ ∇f(0,0,2) & =2(0)\text{ }i+\frac{2(0)}{9}\text{ }j+\frac{(2)}{2}\text{ }k \\  & =k \\  & =⟨0,0,1⟩\end{aligned}
$$

 

Finally, the vector form of the equation of the line that is parallel to $∇f(0,0,2)$ and passes through the point $(0,0,2)$ can be written as

$$
\begin{aligned}r & =⟨0,\,0,\,2⟩+t\,∇f(0,0,2)=⟨0,\,0,\,2⟩+t\,⟨0,\,0,\,1⟩\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36343

Find a vector equation of the normal line to the surface $\frac{{x}^{2}}{4}-{y}^{2}={z}^{2}$ at the point $(2,0,1).$

Field 0 (:answer-field.type/radio)

- $r=⟨2,0,1⟩+t\,⟨1,0,0⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,0,1⟩+t\,⟨0,0,-2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,0,1⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨2,1,1⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,0,1⟩+t\,⟨1,1,-2⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}\frac{{x}^{2}}{4}-{y}^{2} & ={z}^{2} \\ \frac{{x}^{2}}{4}-{y}^{2}-{z}^{2} & =0\end{aligned}
$$

If we set $f(x,y,z)=\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(2,0,1)$ can be found by computing $∇f(2,0,1).$ 

So, we find the gradient and evaluate it at $(2,0,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})i+\frac{∂}{∂y}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})j+\frac{∂}{∂z}(\frac{{x}^{2}}{4}-{y}^{2}-{z}^{2})k \\  & =\frac{x}{2}\text{ }i-2y\text{ }j-2z\text{ }k \\ ∇f(2,0,1) & =\frac{(2)}{2}\,i-2(0)\text{ }j-2(1)\,k \\  & =i-2\,k \\  & =⟨1,0,-2⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,0,1)$ and passes through the point $(2,0,1)$ can be written as

$$
\begin{aligned}r & =⟨2,0,1⟩+t\,∇f(2,0,1)=⟨2,0,1⟩+t\,⟨1,0,-2⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36343

Find a vector equation of the normal line to the surface $\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}={\left(-\left(z - 1\right)\right)}^{2}$ at the point $(-5,2,0).$

Field 0 (:answer-field.type/radio)

- $r=⟨-5,2,0⟩+t\,⟨-1,0,2⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨-5,2,0⟩+t\,⟨0,0,2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨-5,2,0⟩+t\,⟨-1,-1,2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨-5,2,0⟩+t\,⟨-1,0,0⟩,\,t\in (-\infty ,\infty )$
- $r=⟨-5,3,0⟩+t\,⟨-1,0,2⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2} & ={\left(-\left(z - 1\right)\right)}^{2} \\ \frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2} & =0\end{aligned}
$$

If we set $f(x,y,z)=\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(-5,2,0)$ can be found by computing $∇f(-5,2,0).$ 

So, we find the gradient and evaluate it at $(-5,2,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2})i+\frac{∂}{∂y}(\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2})j+\frac{∂}{∂z}(\frac{{\left(-\left(x + 3\right)\right)}^{2}}{4}-{\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2})k \\  & =\left(-\left(\frac{\left(-\left(x + 3\right)\right)}{2}\right)\right)i+\left(-2\left(y - 2\right)\right)j+\left(-\left(-2\left(-\left(z - 1\right)\right)\right)\right)k\\∇f(-5,2,0)& =\left(-\left(\frac{\left(-\left(\left(-5\right) + 3\right)\right)}{2}\right)\right)i+\left(-2\left(\left(2\right) - 2\right)\right)j+\left(-\left(-2\left(-\left(\left(0\right) - 1\right)\right)\right)\right)k\\  & =\left(-\left(\frac{(2)}{2}\right)\right)i+\left(-2(0)\right)j+\left(-\left(-2(1)\right)\right)k\\  & =\left(-\left(1\right)\right)i+\left(0\right)j+\left(-\left(-2\right)\right)k\\  & =⟨-1,0,2⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-5,2,0)$ and passes through the point $(-5,2,0)$ can be written as

$$
\begin{aligned}r & =⟨-5,2,0⟩+t\,∇f(-5,2,0)=⟨-5,2,0⟩+t\,⟨-1,0,2⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36343

Find a vector equation of the normal line to the surface $\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}={\left(z + 3\right)}^{2}$ at the point $(5,-2,-2).$

Field 0 (:answer-field.type/radio)

- $r=⟨5,-2,-2⟩+t\,⟨1,1,-2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨5,-2,-2⟩+t\,⟨1,0,0⟩,\,t\in (-\infty ,\infty )$
- $r=⟨5,-2,-2⟩+t\,⟨0,0,-2⟩,\,t\in (-\infty ,\infty )$
- $r=⟨5,-2,-2⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨5,-1,-2⟩+t\,⟨1,0,-2⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2} & ={\left(z + 3\right)}^{2} \\ \frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2} & =0\end{aligned}
$$

If we set $f(x,y,z)=\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(5,-2,-2)$ can be found by computing $∇f(5,-2,-2).$ 

So, we find the gradient and evaluate it at $(5,-2,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2})i+\frac{∂}{∂y}(\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2})j+\frac{∂}{∂z}(\frac{{\left(x - 3\right)}^{2}}{4}-{\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2})k \\  & =\left(\frac{\left(x - 3\right)}{2}\right)i+\left(-\left(-2\left(-\left(y + 2\right)\right)\right)\right)j+\left(-2\left(z + 3\right)\right)k\\∇f(5,-2,-2)& =\left(\frac{\left(\left(5\right) - 3\right)}{2}\right)i+\left(-\left(-2\left(-\left(\left(-2\right) + 2\right)\right)\right)\right)j+\left(-2\left(\left(-2\right) + 3\right)\right)k\\  & =\left(\frac{(2)}{2}\right)i+\left(-\left(-2(0)\right)\right)j+\left(-2(1)\right)k\\  & =\left(1\right)i+\left(-\left(0\right)\right)j+\left(-2\right)k\\  & =⟨1,0,-2⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(5,-2,-2)$ and passes through the point $(5,-2,-2)$ can be written as

$$
\begin{aligned}r & =⟨5,-2,-2⟩+t\,∇f(5,-2,-2)=⟨5,-2,-2⟩+t\,⟨1,0,-2⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-37515

Find the equation of the normal line to the surface $z=\operatorname{sin}⁡(xy)+{y}^{2}$ at the point $(0,-1,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x}{-1}=\frac{y + 1}{-4}=\frac{z - 1}{-1}$
- $\frac{x}{-2}=\frac{y + 1}{-2}=\frac{z - 1}{-1}$
- $\frac{x}{-1}=\frac{y + 1}{-2}=\frac{z - 1}{-1}$ **keyed**
- $\frac{x - 1}{-1}=\frac{y + 1}{-2}=\frac{z - 1}{-1}$
- $\frac{x}{-1}=\frac{y + 1}{-2}=\frac{z - 1}{-2}$

First, we bring all variables to one side:

$$
\begin{aligned}z & =\operatorname{sin}⁡(xy)+{y}^{2} \\ 0 & =\operatorname{sin}⁡(xy)+{y}^{2}-z\end{aligned}
$$

If we set $f(x,y,z)=\operatorname{sin}⁡(xy)+{y}^{2}-z$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(0,-1,1)$ can be found by computing $∇f(0,-1,1).$ 

So, we find the gradient and evaluate it at $(0,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{sin}⁡(xy)+{y}^{2}-z)i+\frac{∂}{∂y}(\operatorname{sin}⁡(xy)+{y}^{2}-z)j+\frac{∂}{∂z}(\operatorname{sin}⁡(xy)+{y}^{2}-z)k \\  & =y\operatorname{cos}⁡(xy)\text{ }i+(x\operatorname{cos}⁡(xy)+2y)\text{ }j-\text{ }k \\ ∇f(0,-1,1) & =(-1)\operatorname{cos}⁡(0)\text{ }i+[(0)\operatorname{cos}⁡(0)+2(-1)]\text{ }j-\text{ }k \\  & =-i-2\,j-k \\  & =⟨-1,-2,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-0}{-1}=\frac{y-(-1)}{-2}=\frac{z-1}{-1} \\ \frac{x}{-1}=\frac{y+1}{-2}=\frac{z-1}{-1} \\ \frac{x}{1}=\frac{y+1}{2}=\frac{z-1}{1} \\ x=\frac{y+1}{2}=z-1\end{aligned}
$$

## Generated normal variants — q-37515

Find the equation of the normal line to the surface $\left(-\left(z - 1\right)\right)=\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}$ at the point $(-3,1,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 3}{1}=\frac{y - 1}{-2}=\frac{z}{1}$ **keyed**
- $\frac{x + 3}{2}=\frac{y - 1}{-2}=\frac{z}{1}$
- $\frac{x + 3}{1}=\frac{y - 1}{-2}=\frac{z}{2}$
- $\frac{x + 3}{1}=\frac{y - 1}{-4}=\frac{z}{1}$
- $\frac{x + 2}{1}=\frac{y - 1}{-2}=\frac{z}{1}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(-\left(z - 1\right)\right) & =\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2} \\ 0 & =\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}-\left(-\left(z - 1\right)\right)\end{aligned}
$$

If we set $f(x,y,z)=\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}-\left(-\left(z - 1\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(-3,1,0)$ can be found by computing $∇f(-3,1,0).$ 

So, we find the gradient and evaluate it at $(-3,1,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}-\left(-\left(z - 1\right)\right))i+\frac{∂}{∂y}(\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}-\left(-\left(z - 1\right)\right))j+\frac{∂}{∂z}(\operatorname{sin}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+{\left(y - 2\right)}^{2}-\left(-\left(z - 1\right)\right))k \\  & =\left(-\left(\left(y - 2\right)\operatorname{cos}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))\right)\right)i+\left(+(\left(-\left(x + 3\right)\right)\operatorname{cos}⁡(\left(-\left(x + 3\right)\right)\left(y - 2\right))+2\left(y - 2\right))\right)j+\left(-\left(-1\right)\right)k\\∇f(-3,1,0)& =\left(-\left(\left(\left(1\right) - 2\right)\operatorname{cos}⁡(\left(-\left(\left(-3\right) + 3\right)\right)\left(\left(1\right) - 2\right))\right)\right)i+\left(+(\left(-\left(\left(-3\right) + 3\right)\right)\operatorname{cos}⁡(\left(-\left(\left(-3\right) + 3\right)\right)\left(\left(1\right) - 2\right))+2\left(\left(1\right) - 2\right))\right)j+\left(-\left(-1\right)\right)k\\  & =\left(-\left((-1)\operatorname{cos}⁡(0)\right)\right)i+\left(+[(0)\operatorname{cos}⁡(0)+2(-1)]\right)j+\left(-\left(-1\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(-2\right)j+\left(-\left(-1\right)\right)k\\  & =⟨1,-2,1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-0}{-1}=\frac{\left(y - 2\right)-(-1)}{-2}=\frac{\left(-\left(z - 1\right)\right)-1}{-1} \\ \frac{\left(-\left(x + 3\right)\right)}{-1}=\frac{\left(y - 2\right)+1}{-2}=\frac{\left(-\left(z - 1\right)\right)-1}{-1} \\ \frac{\left(-\left(x + 3\right)\right)}{1}=\frac{\left(y - 2\right)+1}{2}=\frac{\left(-\left(z - 1\right)\right)-1}{1} \\ \left(-\left(x + 3\right)\right)=\frac{\left(y - 2\right)+1}{2}=\left(-\left(z - 1\right)\right)-1\end{aligned}
$$

## Generated normal variants — q-37515

Find the equation of the normal line to the surface $\left(z + 3\right)=\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}$ at the point $(3,-1,-2).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 3}{-1}=\frac{y + 1}{2}=\frac{z + 2}{-2}$
- $\frac{x - 3}{-1}=\frac{y + 1}{4}=\frac{z + 2}{-1}$
- $\frac{x - 3}{-2}=\frac{y + 1}{2}=\frac{z + 2}{-1}$
- $\frac{x - 3}{-1}=\frac{y + 1}{2}=\frac{z + 2}{-1}$ **keyed**
- $\frac{x - 4}{-1}=\frac{y + 1}{2}=\frac{z + 2}{-1}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(z + 3\right) & =\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2} \\ 0 & =\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}-\left(z + 3\right)\end{aligned}
$$

If we set $f(x,y,z)=\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}-\left(z + 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(3,-1,-2)$ can be found by computing $∇f(3,-1,-2).$ 

So, we find the gradient and evaluate it at $(3,-1,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}-\left(z + 3\right))i+\frac{∂}{∂y}(\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}-\left(z + 3\right))j+\frac{∂}{∂z}(\operatorname{sin}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+{\left(-\left(y + 2\right)\right)}^{2}-\left(z + 3\right))k \\  & =\left(\left(-\left(y + 2\right)\right)\operatorname{cos}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))\right)i+\left(-\left(+(\left(x - 3\right)\operatorname{cos}⁡(\left(x - 3\right)\left(-\left(y + 2\right)\right))+2\left(-\left(y + 2\right)\right))\right)\right)j+\left(-1\right)k\\∇f(3,-1,-2)& =\left(\left(-\left(\left(-1\right) + 2\right)\right)\operatorname{cos}⁡(\left(\left(3\right) - 3\right)\left(-\left(\left(-1\right) + 2\right)\right))\right)i+\left(-\left(+(\left(\left(3\right) - 3\right)\operatorname{cos}⁡(\left(\left(3\right) - 3\right)\left(-\left(\left(-1\right) + 2\right)\right))+2\left(-\left(\left(-1\right) + 2\right)\right))\right)\right)j+\left(-1\right)k\\  & =\left((-1)\operatorname{cos}⁡(0)\right)i+\left(-\left(+[(0)\operatorname{cos}⁡(0)+2(-1)]\right)\right)j+\left(-1\right)k\\  & =\left(-1\right)i+\left(-\left(-2\right)\right)j+\left(-1\right)k\\  & =⟨-1,2,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-0}{-1}=\frac{\left(-\left(y + 2\right)\right)-(-1)}{-2}=\frac{\left(z + 3\right)-1}{-1} \\ \frac{\left(x - 3\right)}{-1}=\frac{\left(-\left(y + 2\right)\right)+1}{-2}=\frac{\left(z + 3\right)-1}{-1} \\ \frac{\left(x - 3\right)}{1}=\frac{\left(-\left(y + 2\right)\right)+1}{2}=\frac{\left(z + 3\right)-1}{1} \\ \left(x - 3\right)=\frac{\left(-\left(y + 2\right)\right)+1}{2}=\left(z + 3\right)-1\end{aligned}
$$

## Generated normal variants — q-131126

Find a vector equation of the normal line to the surface ${x}^{2}y+{y}^{2}z+{z}^{2}x=5$ at the point $(1,-1,2).$

Field 0 (:answer-field.type/radio)

- $⟨1,-1,2⟩+t\,⟨2,0,5⟩,\,t\in (-\infty ,\infty )$
- $⟨1,-1,2⟩+t\,⟨0,-3,5⟩,\,t\in (-\infty ,\infty )$
- $⟨1,-1,2⟩+t\,⟨2,-3,5⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨2,-1,2⟩+t\,⟨2,-3,5⟩,\,t\in (-\infty ,\infty )$
- $⟨1,-1,2⟩+t\,⟨2,-3,0⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)={x}^{2}y+{y}^{2}z+{z}^{2}x.$ Then, our surface can be viewed as the level surface $f(x,y,z)=5.$ 

A normal vector to the level surface that passes through the point $(1,-1,2)$ can be found by computing $∇f(1,-1,2).$ 

So, we find the gradient and evaluate it at $(1,-1,2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}y+{y}^{2}z+{z}^{2}x)i+\frac{∂}{∂y}({x}^{2}y+{y}^{2}z+{z}^{2}x)j+\frac{∂}{∂z}({x}^{2}y+{y}^{2}z+{z}^{2}x)k \\  & =(2xy+{z}^{2})\,i+({x}^{2}+2yz)\,j+({y}^{2}+2zx)\,k \\ ∇f(1,-1,2) & =(2(1)(-1)+(2)^{2})\text{ }i+((1)^{2}+2(-1)(2))\text{ }j+((-1)^{2}+2(2)(1))\text{ }k \\  & =2\,i-3\,j+5\,k \\  & =⟨2,-3,5⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(1,-1,2)$ and passes through the point $(1,-1,2)$ can be written as

$$
\begin{aligned}r & =⟨1,-1,2⟩+t\,∇f(1,-1,2)=⟨1,-1,2⟩+t\,⟨2,-3,5⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131126

Find a vector equation of the normal line to the surface ${\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)+{\left(y - 2\right)}^{2}\left(-\left(z - 1\right)\right)+{\left(-\left(z - 1\right)\right)}^{2}\left(-\left(x + 3\right)\right)=5$ at the point $(-4,1,-1).$

Field 0 (:answer-field.type/radio)

- $⟨-4,1,-1⟩+t\,⟨-2,-3,-5⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨-4,1,-1⟩+t\,⟨0,-3,-5⟩,\,t\in (-\infty ,\infty )$
- $⟨-4,1,-1⟩+t\,⟨-2,-3,0⟩,\,t\in (-\infty ,\infty )$
- $⟨-4,1,-1⟩+t\,⟨-2,0,-5⟩,\,t\in (-\infty ,\infty )$
- $⟨-3,1,-1⟩+t\,⟨-2,-3,-5⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)={\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)+{\left(y - 2\right)}^{2}\left(-\left(z - 1\right)\right)+{\left(-\left(z - 1\right)\right)}^{2}\left(-\left(x + 3\right)\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=5.$ 

A normal vector to the level surface that passes through the point $(-4,1,-1)$ can be found by computing $∇f(-4,1,-1).$ 

So, we find the gradient and evaluate it at $(-4,1,-1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)+{\left(y - 2\right)}^{2}\left(-\left(z - 1\right)\right)+{\left(-\left(z - 1\right)\right)}^{2}\left(-\left(x + 3\right)\right))i+\frac{∂}{∂y}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)+{\left(y - 2\right)}^{2}\left(-\left(z - 1\right)\right)+{\left(-\left(z - 1\right)\right)}^{2}\left(-\left(x + 3\right)\right))j+\frac{∂}{∂z}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)+{\left(y - 2\right)}^{2}\left(-\left(z - 1\right)\right)+{\left(-\left(z - 1\right)\right)}^{2}\left(-\left(x + 3\right)\right))k \\  & =\left(-\left((2\left(-\left(x + 3\right)\right)\left(y - 2\right)+{\left(-\left(z - 1\right)\right)}^{2})\right)\right)i+\left(+({\left(-\left(x + 3\right)\right)}^{2}+2\left(y - 2\right)\left(-\left(z - 1\right)\right))\right)j+\left(-\left(+({\left(y - 2\right)}^{2}+2\left(-\left(z - 1\right)\right)\left(-\left(x + 3\right)\right))\right)\right)k\\∇f(-4,1,-1)& =\left(-\left((2\left(-\left(\left(-4\right) + 3\right)\right)\left(\left(1\right) - 2\right)+{\left(-\left(\left(-1\right) - 1\right)\right)}^{2})\right)\right)i+\left(+({\left(-\left(\left(-4\right) + 3\right)\right)}^{2}+2\left(\left(1\right) - 2\right)\left(-\left(\left(-1\right) - 1\right)\right))\right)j+\left(-\left(+({\left(\left(1\right) - 2\right)}^{2}+2\left(-\left(\left(-1\right) - 1\right)\right)\left(-\left(\left(-4\right) + 3\right)\right))\right)\right)k\\  & =\left(-\left((2(1)(-1)+(2)^{2})\right)\right)i+\left(+((1)^{2}+2(-1)(2))\right)j+\left(-\left(+((-1)^{2}+2(2)(1))\right)\right)k\\  & =\left(-\left(2\right)\right)i+\left(-3\right)j+\left(-\left(+5\right)\right)k\\  & =⟨-2,-3,-5⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-4,1,-1)$ and passes through the point $(-4,1,-1)$ can be written as

$$
\begin{aligned}r & =⟨-4,1,-1⟩+t\,∇f(-4,1,-1)=⟨-4,1,-1⟩+t\,⟨-2,-3,-5⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131126

Find a vector equation of the normal line to the surface ${\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)+{\left(-\left(y + 2\right)\right)}^{2}\left(z + 3\right)+{\left(z + 3\right)}^{2}\left(x - 3\right)=5$ at the point $(4,-1,-1).$

Field 0 (:answer-field.type/radio)

- $⟨4,-1,-1⟩+t\,⟨2,3,0⟩,\,t\in (-\infty ,\infty )$
- $⟨4,-1,-1⟩+t\,⟨2,0,5⟩,\,t\in (-\infty ,\infty )$
- $⟨4,-1,-1⟩+t\,⟨0,3,5⟩,\,t\in (-\infty ,\infty )$
- $⟨4,-1,-1⟩+t\,⟨2,3,5⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨5,-1,-1⟩+t\,⟨2,3,5⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)={\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)+{\left(-\left(y + 2\right)\right)}^{2}\left(z + 3\right)+{\left(z + 3\right)}^{2}\left(x - 3\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=5.$ 

A normal vector to the level surface that passes through the point $(4,-1,-1)$ can be found by computing $∇f(4,-1,-1).$ 

So, we find the gradient and evaluate it at $(4,-1,-1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)+{\left(-\left(y + 2\right)\right)}^{2}\left(z + 3\right)+{\left(z + 3\right)}^{2}\left(x - 3\right))i+\frac{∂}{∂y}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)+{\left(-\left(y + 2\right)\right)}^{2}\left(z + 3\right)+{\left(z + 3\right)}^{2}\left(x - 3\right))j+\frac{∂}{∂z}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)+{\left(-\left(y + 2\right)\right)}^{2}\left(z + 3\right)+{\left(z + 3\right)}^{2}\left(x - 3\right))k \\  & =\left((2\left(x - 3\right)\left(-\left(y + 2\right)\right)+{\left(z + 3\right)}^{2})\right)i+\left(-\left(+({\left(x - 3\right)}^{2}+2\left(-\left(y + 2\right)\right)\left(z + 3\right))\right)\right)j+\left(+({\left(-\left(y + 2\right)\right)}^{2}+2\left(z + 3\right)\left(x - 3\right))\right)k\\∇f(4,-1,-1)& =\left((2\left(\left(4\right) - 3\right)\left(-\left(\left(-1\right) + 2\right)\right)+{\left(\left(-1\right) + 3\right)}^{2})\right)i+\left(-\left(+({\left(\left(4\right) - 3\right)}^{2}+2\left(-\left(\left(-1\right) + 2\right)\right)\left(\left(-1\right) + 3\right))\right)\right)j+\left(+({\left(-\left(\left(-1\right) + 2\right)\right)}^{2}+2\left(\left(-1\right) + 3\right)\left(\left(4\right) - 3\right))\right)k\\  & =\left((2(1)(-1)+(2)^{2})\right)i+\left(-\left(+((1)^{2}+2(-1)(2))\right)\right)j+\left(+((-1)^{2}+2(2)(1))\right)k\\  & =\left(2\right)i+\left(-\left(-3\right)\right)j+\left(+5\right)k\\  & =⟨2,3,5⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(4,-1,-1)$ and passes through the point $(4,-1,-1)$ can be written as

$$
\begin{aligned}r & =⟨4,-1,-1⟩+t\,∇f(4,-1,-1)=⟨4,-1,-1⟩+t\,⟨2,3,5⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131127

Find a vector equation of the normal line to the surface ${z}^{2}\operatorname{sin}⁡({x}^{2}y)={x}^{2}z+y-\frac{\pi }{2}$ at the point $(-1,\frac{\pi }{2},1).$

Field 0 (:answer-field.type/radio)

- $⟨-1,\frac{\pi}{2},1⟩+t\,⟨2,0,1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi}{2},1⟩+t\,⟨0,-1,1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi}{2},1⟩+t\,⟨2,-1,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨0,\frac{\pi}{2},1⟩+t\,⟨2,-1,1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi}{2},1⟩+t\,⟨2,-1,0⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}{z}^{2}\operatorname{sin}⁡({x}^{2}y) & ={x}^{2}z+y-\frac{\pi }{2} \\ {z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y & =-\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y,z)={z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y,$ our surface can be viewed as the level surface $f(x,y,z)=-\frac{\pi }{2}.$ 

A normal vector to the level surface that passes through the point $(-1,\frac{\pi }{2},1)$ can be found by computing $∇f(-1,\frac{\pi }{2},1).$ 

So, we find the gradient and evaluate it at $(-1,\frac{\pi }{2},1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)i+\frac{∂}{∂y}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)j+\frac{∂}{∂z}({z}^{2}\operatorname{sin}⁡({x}^{2}y)-{x}^{2}z-y)k \\  & =(2xy{z}^{2}\operatorname{cos}⁡({x}^{2}y)-2xz)i+({x}^{2}{z}^{2}\operatorname{cos}⁡({x}^{2}y)-1)j+(2z\operatorname{sin}⁡({x}^{2}y)-{x}^{2})k \\ ∇f(-1,\frac{\pi }{2},1) & =(2(-1)(\frac{\pi }{2})(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-2(-1)(1))i+((-1)^{2}(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-1)j+(2(1)\operatorname{sin}⁡((-1)^{2}\frac{\pi }{2})-(-1)^{2})k \\  & =(-\pi \operatorname{cos}⁡(\frac{\pi }{2})+2)i+(\operatorname{cos}⁡(\frac{\pi }{2})-1)j+(2\operatorname{sin}⁡(\frac{\pi }{2})-1)k \\  & =2\,i-j+k \\  & =⟨2,-1,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-1,\frac{\pi }{2},1)$ and passes through the point $(-1,\frac{\pi }{2},1)$ can be written as

$$
\begin{aligned}r & =⟨-1,\frac{\pi }{2},1⟩+t\,∇f(-1,\frac{\pi }{2},1)=⟨-1,\frac{\pi }{2},1⟩+t\,⟨2,-1,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131127

Find a vector equation of the normal line to the surface ${\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))={\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)+\left(y - 2\right)-\frac{\pi }{2}$ at the point $(-2,\frac{\pi}{2} + 2,0).$

Field 0 (:answer-field.type/radio)

- $⟨-2,\frac{\pi}{2} + 2,0⟩+t\,⟨-2,-1,-1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨-2,\frac{\pi}{2} + 2,0⟩+t\,⟨0,-1,-1⟩,\,t\in (-\infty ,\infty )$
- $⟨-2,\frac{\pi}{2} + 2,0⟩+t\,⟨-2,-1,0⟩,\,t\in (-\infty ,\infty )$
- $⟨-2,\frac{\pi}{2} + 2,0⟩+t\,⟨-2,0,-1⟩,\,t\in (-\infty ,\infty )$
- $⟨-1,\frac{\pi}{2} + 2,0⟩+t\,⟨-2,-1,-1⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}{\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)) & ={\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)+\left(y - 2\right)-\frac{\pi }{2} \\ {\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)-\left(y - 2\right) & =-\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y,z)={\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)-\left(y - 2\right),$ our surface can be viewed as the level surface $f(x,y,z)=-\frac{\pi }{2}.$ 

A normal vector to the level surface that passes through the point $(-2,\frac{\pi}{2} + 2,0)$ can be found by computing $∇f(-2,\frac{\pi}{2} + 2,0).$ 

So, we find the gradient and evaluate it at $(-2,\frac{\pi}{2} + 2,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)-\left(y - 2\right))i+\frac{∂}{∂y}({\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)-\left(y - 2\right))j+\frac{∂}{∂z}({\left(-\left(z - 1\right)\right)}^{2}\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)-\left(y - 2\right))k \\  & =\left(-\left((2\left(-\left(x + 3\right)\right)\left(y - 2\right){\left(-\left(z - 1\right)\right)}^{2}\operatorname{cos}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-2\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right))\right)\right)i+\left(+({\left(-\left(x + 3\right)\right)}^{2}{\left(-\left(z - 1\right)\right)}^{2}\operatorname{cos}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-1)\right)j+\left(-\left(+(2\left(-\left(z - 1\right)\right)\operatorname{sin}⁡({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right))-{\left(-\left(x + 3\right)\right)}^{2})\right)\right)k\\∇f(-2,\frac{\pi}{2} + 2,0)& =\left(-\left((2\left(-\left(\left(-2\right) + 3\right)\right)\left(\left(\frac{\pi}{2} + 2\right) - 2\right){\left(-\left(\left(0\right) - 1\right)\right)}^{2}\operatorname{cos}⁡({\left(-\left(\left(-2\right) + 3\right)\right)}^{2}\left(\left(\frac{\pi}{2} + 2\right) - 2\right))-2\left(-\left(\left(-2\right) + 3\right)\right)\left(-\left(\left(0\right) - 1\right)\right))\right)\right)i+\left(+({\left(-\left(\left(-2\right) + 3\right)\right)}^{2}{\left(-\left(\left(0\right) - 1\right)\right)}^{2}\operatorname{cos}⁡({\left(-\left(\left(-2\right) + 3\right)\right)}^{2}\left(\left(\frac{\pi}{2} + 2\right) - 2\right))-1)\right)j+\left(-\left(+(2\left(-\left(\left(0\right) - 1\right)\right)\operatorname{sin}⁡({\left(-\left(\left(-2\right) + 3\right)\right)}^{2}\left(\left(\frac{\pi}{2} + 2\right) - 2\right))-{\left(-\left(\left(-2\right) + 3\right)\right)}^{2})\right)\right)k\\  & =\left(-\left((2(-1)(\frac{\pi }{2})(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-2(-1)(1))\right)\right)i+\left(+((-1)^{2}(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-1)\right)j+\left(-\left(+(2(1)\operatorname{sin}⁡((-1)^{2}\frac{\pi }{2})-(-1)^{2})\right)\right)k\\  & =\left(-\left((-\pi \operatorname{cos}⁡(\frac{\pi }{2})+2)\right)\right)i+\left(+(\operatorname{cos}⁡(\frac{\pi }{2})-1)\right)j+\left(-\left(+(2\operatorname{sin}⁡(\frac{\pi }{2})-1)\right)\right)k\\  & =\left(-\left(2\right)\right)i+\left(-1\right)j+\left(-\left(1\right)\right)k\\  & =⟨-2,-1,-1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-2,\frac{\pi}{2} + 2,0)$ and passes through the point $(-2,\frac{\pi}{2} + 2,0)$ can be written as

$$
\begin{aligned}r & =⟨-2,\frac{\pi}{2} + 2,0⟩+t\,∇f(-2,\frac{\pi}{2} + 2,0)=⟨-2,\frac{\pi}{2} + 2,0⟩+t\,⟨-2,-1,-1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131127

Find a vector equation of the normal line to the surface ${\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))={\left(x - 3\right)}^{2}\left(z + 3\right)+\left(-\left(y + 2\right)\right)-\frac{\pi }{2}$ at the point $(2,-2 - \frac{\pi}{2},-2).$

Field 0 (:answer-field.type/radio)

- $⟨2,-2 - \frac{\pi}{2},-2⟩+t\,⟨2,1,0⟩,\,t\in (-\infty ,\infty )$
- $⟨2,-2 - \frac{\pi}{2},-2⟩+t\,⟨2,0,1⟩,\,t\in (-\infty ,\infty )$
- $⟨2,-2 - \frac{\pi}{2},-2⟩+t\,⟨0,1,1⟩,\,t\in (-\infty ,\infty )$
- $⟨2,-2 - \frac{\pi}{2},-2⟩+t\,⟨2,1,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨3,-2 - \frac{\pi}{2},-2⟩+t\,⟨2,1,1⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}{\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)) & ={\left(x - 3\right)}^{2}\left(z + 3\right)+\left(-\left(y + 2\right)\right)-\frac{\pi }{2} \\ {\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2}\left(z + 3\right)-\left(-\left(y + 2\right)\right) & =-\frac{\pi }{2}\end{aligned}
$$

If we set $f(x,y,z)={\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2}\left(z + 3\right)-\left(-\left(y + 2\right)\right),$ our surface can be viewed as the level surface $f(x,y,z)=-\frac{\pi }{2}.$ 

A normal vector to the level surface that passes through the point $(2,-2 - \frac{\pi}{2},-2)$ can be found by computing $∇f(2,-2 - \frac{\pi}{2},-2).$ 

So, we find the gradient and evaluate it at $(2,-2 - \frac{\pi}{2},-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2}\left(z + 3\right)-\left(-\left(y + 2\right)\right))i+\frac{∂}{∂y}({\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2}\left(z + 3\right)-\left(-\left(y + 2\right)\right))j+\frac{∂}{∂z}({\left(z + 3\right)}^{2}\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2}\left(z + 3\right)-\left(-\left(y + 2\right)\right))k \\  & =\left((2\left(x - 3\right)\left(-\left(y + 2\right)\right){\left(z + 3\right)}^{2}\operatorname{cos}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-2\left(x - 3\right)\left(z + 3\right))\right)i+\left(-\left(+({\left(x - 3\right)}^{2}{\left(z + 3\right)}^{2}\operatorname{cos}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-1)\right)\right)j+\left(+(2\left(z + 3\right)\operatorname{sin}⁡({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right))-{\left(x - 3\right)}^{2})\right)k\\∇f(2,-2 - \frac{\pi}{2},-2)& =\left((2\left(\left(2\right) - 3\right)\left(-\left(\left(-2 - \frac{\pi}{2}\right) + 2\right)\right){\left(\left(-2\right) + 3\right)}^{2}\operatorname{cos}⁡({\left(\left(2\right) - 3\right)}^{2}\left(-\left(\left(-2 - \frac{\pi}{2}\right) + 2\right)\right))-2\left(\left(2\right) - 3\right)\left(\left(-2\right) + 3\right))\right)i+\left(-\left(+({\left(\left(2\right) - 3\right)}^{2}{\left(\left(-2\right) + 3\right)}^{2}\operatorname{cos}⁡({\left(\left(2\right) - 3\right)}^{2}\left(-\left(\left(-2 - \frac{\pi}{2}\right) + 2\right)\right))-1)\right)\right)j+\left(+(2\left(\left(-2\right) + 3\right)\operatorname{sin}⁡({\left(\left(2\right) - 3\right)}^{2}\left(-\left(\left(-2 - \frac{\pi}{2}\right) + 2\right)\right))-{\left(\left(2\right) - 3\right)}^{2})\right)k\\  & =\left((2(-1)(\frac{\pi }{2})(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-2(-1)(1))\right)i+\left(-\left(+((-1)^{2}(1)^{2}\operatorname{cos}⁡((-1)^{2}\frac{\pi }{2})-1)\right)\right)j+\left(+(2(1)\operatorname{sin}⁡((-1)^{2}\frac{\pi }{2})-(-1)^{2})\right)k\\  & =\left((-\pi \operatorname{cos}⁡(\frac{\pi }{2})+2)\right)i+\left(-\left(+(\operatorname{cos}⁡(\frac{\pi }{2})-1)\right)\right)j+\left(+(2\operatorname{sin}⁡(\frac{\pi }{2})-1)\right)k\\  & =\left(2\right)i+\left(-\left(-1\right)\right)j+\left(1\right)k\\  & =⟨2,1,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,-2 - \frac{\pi}{2},-2)$ and passes through the point $(2,-2 - \frac{\pi}{2},-2)$ can be written as

$$
\begin{aligned}r & =⟨2,-2 - \frac{\pi}{2},-2⟩+t\,∇f(2,-2 - \frac{\pi}{2},-2)=⟨2,-2 - \frac{\pi}{2},-2⟩+t\,⟨2,1,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131128

Find the equation of the normal line to the surface ${x}^{2}yz=-4$ at the point $(2,-1,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 2}{-4}=\frac{y + 1}{8}=\frac{z - 1}{-4}$
- $\frac{x - 2}{-8}=\frac{y + 1}{4}=\frac{z - 1}{-4}$
- $\frac{x - 2}{-4}=\frac{y + 1}{4}=\frac{z - 1}{-4}$ **keyed**
- $\frac{x - 3}{-4}=\frac{y + 1}{4}=\frac{z - 1}{-4}$
- $\frac{x - 2}{-4}=\frac{y + 1}{4}=\frac{z - 1}{-8}$

Let's set $f(x,y,z)={x}^{2}yz.$ Then, our surface can be viewed as the level surface $f(x,y,z)=-4.$ 

A normal vector to the level surface that passes through the point $(2,-1,1)$ can be found by computing $∇f(2,-1,1).$ 

So, we find the gradient and evaluate it at $(2,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}yz)i+\frac{∂}{∂y}({x}^{2}yz)j+\frac{∂}{∂z}({x}^{2}yz)k \\  & =2xyz\text{ }i+{x}^{2}z\text{ }j+{x}^{2}y\,k \\ ∇f(2,-1,1) & =2(2)(-1)(1)\text{ }i+(2)^{2}(1)\text{ }j+(2)^{2}(-1)\text{ }k \\  & =-4\,i+4\,j-4\,k \\  & =⟨-4,4,-4⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{(-4)}=\frac{y-(-1)}{4}=\frac{z-1}{(-4)} \\ \frac{x-2}{(-1)}=\frac{y+1}{1}=\frac{z-1}{(-1)} \\ 2-x=y+1=1-z\end{aligned}
$$

## Generated normal variants — q-131128

Find the equation of the normal line to the surface ${\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\left(-\left(z - 1\right)\right)=-4$ at the point $(-5,1,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 5}{4}=\frac{y - 1}{4}=\frac{z}{4}$ **keyed**
- $\frac{x + 5}{8}=\frac{y - 1}{4}=\frac{z}{4}$
- $\frac{x + 5}{4}=\frac{y - 1}{4}=\frac{z}{8}$
- $\frac{x + 5}{4}=\frac{y - 1}{8}=\frac{z}{4}$
- $\frac{x + 4}{4}=\frac{y - 1}{4}=\frac{z}{4}$

Let's set $f(x,y,z)={\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\left(-\left(z - 1\right)\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=-4.$ 

A normal vector to the level surface that passes through the point $(-5,1,0)$ can be found by computing $∇f(-5,1,0).$ 

So, we find the gradient and evaluate it at $(-5,1,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\left(-\left(z - 1\right)\right))i+\frac{∂}{∂y}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\left(-\left(z - 1\right)\right))j+\frac{∂}{∂z}({\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\left(-\left(z - 1\right)\right))k \\  & =\left(-\left(2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right)\right)\right)i+\left(+{\left(-\left(x + 3\right)\right)}^{2}\left(-\left(z - 1\right)\right)\right)j+\left(-\left(+{\left(-\left(x + 3\right)\right)}^{2}\left(y - 2\right)\right)\right)k\\∇f(-5,1,0)& =\left(-\left(2\left(-\left(\left(-5\right) + 3\right)\right)\left(\left(1\right) - 2\right)\left(-\left(\left(0\right) - 1\right)\right)\right)\right)i+\left(+{\left(-\left(\left(-5\right) + 3\right)\right)}^{2}\left(-\left(\left(0\right) - 1\right)\right)\right)j+\left(-\left(+{\left(-\left(\left(-5\right) + 3\right)\right)}^{2}\left(\left(1\right) - 2\right)\right)\right)k\\  & =\left(-\left(2(2)(-1)(1)\right)\right)i+\left(+(2)^{2}(1)\right)j+\left(-\left(+(2)^{2}(-1)\right)\right)k\\  & =\left(-\left(-4\right)\right)i+\left(+4\right)j+\left(-\left(-4\right)\right)k\\  & =⟨4,4,4⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-2}{(-4)}=\frac{\left(y - 2\right)-(-1)}{4}=\frac{\left(-\left(z - 1\right)\right)-1}{(-4)} \\ \frac{\left(-\left(x + 3\right)\right)-2}{(-1)}=\frac{\left(y - 2\right)+1}{1}=\frac{\left(-\left(z - 1\right)\right)-1}{(-1)} \\ 2-\left(-\left(x + 3\right)\right)=\left(y - 2\right)+1=1-\left(-\left(z - 1\right)\right)\end{aligned}
$$

## Generated normal variants — q-131128

Find the equation of the normal line to the surface ${\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\left(z + 3\right)=-4$ at the point $(5,-1,-2).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 5}{-4}=\frac{y + 1}{-4}=\frac{z + 2}{-8}$
- $\frac{x - 5}{-4}=\frac{y + 1}{-8}=\frac{z + 2}{-4}$
- $\frac{x - 5}{-8}=\frac{y + 1}{-4}=\frac{z + 2}{-4}$
- $\frac{x - 5}{-4}=\frac{y + 1}{-4}=\frac{z + 2}{-4}$ **keyed**
- $\frac{x - 6}{-4}=\frac{y + 1}{-4}=\frac{z + 2}{-4}$

Let's set $f(x,y,z)={\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\left(z + 3\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=-4.$ 

A normal vector to the level surface that passes through the point $(5,-1,-2)$ can be found by computing $∇f(5,-1,-2).$ 

So, we find the gradient and evaluate it at $(5,-1,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\left(z + 3\right))i+\frac{∂}{∂y}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\left(z + 3\right))j+\frac{∂}{∂z}({\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\left(z + 3\right))k \\  & =\left(2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right)\right)i+\left(-\left(+{\left(x - 3\right)}^{2}\left(z + 3\right)\right)\right)j+\left(+{\left(x - 3\right)}^{2}\left(-\left(y + 2\right)\right)\right)k\\∇f(5,-1,-2)& =\left(2\left(\left(5\right) - 3\right)\left(-\left(\left(-1\right) + 2\right)\right)\left(\left(-2\right) + 3\right)\right)i+\left(-\left(+{\left(\left(5\right) - 3\right)}^{2}\left(\left(-2\right) + 3\right)\right)\right)j+\left(+{\left(\left(5\right) - 3\right)}^{2}\left(-\left(\left(-1\right) + 2\right)\right)\right)k\\  & =\left(2(2)(-1)(1)\right)i+\left(-\left(+(2)^{2}(1)\right)\right)j+\left(+(2)^{2}(-1)\right)k\\  & =\left(-4\right)i+\left(-\left(+4\right)\right)j+\left(-4\right)k\\  & =⟨-4,-4,-4⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-2}{(-4)}=\frac{\left(-\left(y + 2\right)\right)-(-1)}{4}=\frac{\left(z + 3\right)-1}{(-4)} \\ \frac{\left(x - 3\right)-2}{(-1)}=\frac{\left(-\left(y + 2\right)\right)+1}{1}=\frac{\left(z + 3\right)-1}{(-1)} \\ 2-\left(x - 3\right)=\left(-\left(y + 2\right)\right)+1=1-\left(z + 3\right)\end{aligned}
$$

## Generated normal variants — q-131130

Find the equation of the normal line to the surface $x={y}^{2}-{z}^{2}$ at the point $(3,2,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 3}{-1}=\frac{y - 2}{8}=\frac{z - 1}{-2}$
- $\frac{x - 3}{-2}=\frac{y - 2}{4}=\frac{z - 1}{-2}$
- $\frac{x - 3}{-1}=\frac{y - 2}{4}=\frac{z - 1}{-2}$ **keyed**
- $\frac{x - 4}{-1}=\frac{y - 2}{4}=\frac{z - 1}{-2}$
- $\frac{x - 3}{-1}=\frac{y - 2}{4}=\frac{z - 1}{-4}$

First, we bring all variables to one side:

$$
\begin{aligned}x & ={y}^{2}-{z}^{2} \\ {y}^{2}-{z}^{2}-x & =0\end{aligned}
$$

If we set $f(x,y,z)={y}^{2}-{z}^{2}-x$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(3,2,1)$ can be found by computing $∇f(3,2,1).$ 

So, we find the gradient and evaluate it at $(3,2,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({y}^{2}-{z}^{2}-x)i+\frac{∂}{∂y}({y}^{2}-{z}^{2}-x)j+\frac{∂}{∂z}({y}^{2}-{z}^{2}-x)k \\  & =-i+2y\,j-2z\,k \\ ∇f(3,2,1) & =-i+2(2)\,j-2(1)\,k \\  & =-i+4\,j-2\,k \\  & =⟨-1,4,-2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-3}{(-1)}=\frac{y-2}{4}=\frac{z-1}{(-2)} \\ \frac{x-3}{1}=\frac{y-2}{-4}=\frac{z-1}{2} \\ x-3=\frac{2-y}{4}=\frac{z-1}{2}\end{aligned}
$$

## Generated normal variants — q-131130

Find the equation of the normal line to the surface $\left(-\left(x + 3\right)\right)={\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}$ at the point $(-6,4,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 6}{1}=\frac{y - 4}{4}=\frac{z}{2}$ **keyed**
- $\frac{x + 6}{2}=\frac{y - 4}{4}=\frac{z}{2}$
- $\frac{x + 6}{1}=\frac{y - 4}{4}=\frac{z}{4}$
- $\frac{x + 6}{1}=\frac{y - 4}{8}=\frac{z}{2}$
- $\frac{x + 5}{1}=\frac{y - 4}{4}=\frac{z}{2}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(-\left(x + 3\right)\right) & ={\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2} \\ {\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}-\left(-\left(x + 3\right)\right) & =0\end{aligned}
$$

If we set $f(x,y,z)={\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}-\left(-\left(x + 3\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(-6,4,0)$ can be found by computing $∇f(-6,4,0).$ 

So, we find the gradient and evaluate it at $(-6,4,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}-\left(-\left(x + 3\right)\right))i+\frac{∂}{∂y}({\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}-\left(-\left(x + 3\right)\right))j+\frac{∂}{∂z}({\left(y - 2\right)}^{2}-{\left(-\left(z - 1\right)\right)}^{2}-\left(-\left(x + 3\right)\right))k \\  & =\left(-\left(-1\right)\right)i+\left(+2\left(y - 2\right)\right)j+\left(-\left(-2\left(-\left(z - 1\right)\right)\right)\right)k\\∇f(-6,4,0)& =\left(-\left(-1\right)\right)i+\left(+2\left(\left(4\right) - 2\right)\right)j+\left(-\left(-2\left(-\left(\left(0\right) - 1\right)\right)\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(+2(2)\right)j+\left(-\left(-2(1)\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(+4\right)j+\left(-\left(-2\right)\right)k\\  & =⟨1,4,2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-3}{(-1)}=\frac{\left(y - 2\right)-2}{4}=\frac{\left(-\left(z - 1\right)\right)-1}{(-2)} \\ \frac{\left(-\left(x + 3\right)\right)-3}{1}=\frac{\left(y - 2\right)-2}{-4}=\frac{\left(-\left(z - 1\right)\right)-1}{2} \\ \left(-\left(x + 3\right)\right)-3=\frac{2-\left(y - 2\right)}{4}=\frac{\left(-\left(z - 1\right)\right)-1}{2}\end{aligned}
$$

## Generated normal variants — q-131130

Find the equation of the normal line to the surface $\left(x - 3\right)={\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}$ at the point $(6,-4,-2).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 6}{-1}=\frac{y + 4}{-4}=\frac{z + 2}{-4}$
- $\frac{x - 6}{-1}=\frac{y + 4}{-8}=\frac{z + 2}{-2}$
- $\frac{x - 6}{-2}=\frac{y + 4}{-4}=\frac{z + 2}{-2}$
- $\frac{x - 6}{-1}=\frac{y + 4}{-4}=\frac{z + 2}{-2}$ **keyed**
- $\frac{x - 7}{-1}=\frac{y + 4}{-4}=\frac{z + 2}{-2}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(x - 3\right) & ={\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2} \\ {\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}-\left(x - 3\right) & =0\end{aligned}
$$

If we set $f(x,y,z)={\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}-\left(x - 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(6,-4,-2)$ can be found by computing $∇f(6,-4,-2).$ 

So, we find the gradient and evaluate it at $(6,-4,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}-\left(x - 3\right))i+\frac{∂}{∂y}({\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}-\left(x - 3\right))j+\frac{∂}{∂z}({\left(-\left(y + 2\right)\right)}^{2}-{\left(z + 3\right)}^{2}-\left(x - 3\right))k \\  & =\left(-1\right)i+\left(-\left(+2\left(-\left(y + 2\right)\right)\right)\right)j+\left(-2\left(z + 3\right)\right)k\\∇f(6,-4,-2)& =\left(-1\right)i+\left(-\left(+2\left(-\left(\left(-4\right) + 2\right)\right)\right)\right)j+\left(-2\left(\left(-2\right) + 3\right)\right)k\\  & =\left(-1\right)i+\left(-\left(+2(2)\right)\right)j+\left(-2(1)\right)k\\  & =\left(-1\right)i+\left(-\left(+4\right)\right)j+\left(-2\right)k\\  & =⟨-1,-4,-2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-3}{(-1)}=\frac{\left(-\left(y + 2\right)\right)-2}{4}=\frac{\left(z + 3\right)-1}{(-2)} \\ \frac{\left(x - 3\right)-3}{1}=\frac{\left(-\left(y + 2\right)\right)-2}{-4}=\frac{\left(z + 3\right)-1}{2} \\ \left(x - 3\right)-3=\frac{2-\left(-\left(y + 2\right)\right)}{4}=\frac{\left(z + 3\right)-1}{2}\end{aligned}
$$

## Generated normal variants — q-71411

Find the equation of the normal line to the surface $3{x}^{2}-xz=6-3xyz$ at the point $(1,0,-3).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 1}{9}=\frac{y}{-18}=\frac{z + 3}{-1}$
- $\frac{x - 1}{18}=\frac{y}{-9}=\frac{z + 3}{-1}$
- $\frac{x - 1}{9}=\frac{y}{-9}=\frac{z + 3}{-1}$ **keyed**
- $\frac{x - 2}{9}=\frac{y}{-9}=\frac{z + 3}{-1}$
- $\frac{x - 1}{9}=\frac{y}{-9}=\frac{z + 3}{-2}$

First, we bring all variables to one side:

$$
\begin{aligned}3{x}^{2}-xz & =6-3xyz \\ 3{x}^{2}-xz+3xyz & =6\end{aligned}
$$

If we set $f(x,y,z)=3{x}^{2}-xz+3xyz$, our surface can be viewed as the level surface $f(x,y,z)=6.$ 

A normal vector to the level surface that passes through the point $(1,0,-3)$ can be found by computing $∇f(1,0,-3).$ 

So, we find the gradient and evaluate it at $(1,0,-3):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(3{x}^{2}-xz+3xyz)i+\frac{∂}{∂y}(3{x}^{2}-xz+3xyz)j+\frac{∂}{∂z}(3{x}^{2}-xz+3xyz)k \\  & =(6x-z+3yz)\text{ }i+3xz\text{ }j+(-x+3xy)\text{ }k \\ ∇f(1,0,-3) & =(6(1)-(-3)+3(0)(-3))\text{ }i+3(1)(-3)\text{ }j+(-1+3(1)(0))\text{ }k \\  & =9\,i-9\,j-k \\  & =⟨9,-9,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-1}{9}=\frac{y-0}{-9}=\frac{z-(-3)}{-1} \\ \frac{x-1}{9}=\frac{y}{-9}=\frac{z+3}{-1}\end{aligned}
$$

## Generated normal variants — q-71411

Find the equation of the normal line to the surface $3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)=6-3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right)$ at the point $(-4,2,4).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 4}{-9}=\frac{y - 2}{-9}=\frac{z - 4}{1}$ **keyed**
- $\frac{x + 4}{-18}=\frac{y - 2}{-9}=\frac{z - 4}{1}$
- $\frac{x + 4}{-9}=\frac{y - 2}{-9}=\frac{z - 4}{2}$
- $\frac{x + 4}{-9}=\frac{y - 2}{-18}=\frac{z - 4}{1}$
- $\frac{x + 3}{-9}=\frac{y - 2}{-9}=\frac{z - 4}{1}$

First, we bring all variables to one side:

$$
\begin{aligned}3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right) & =6-3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right) \\ 3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right) & =6\end{aligned}
$$

If we set $f(x,y,z)=3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=6.$ 

A normal vector to the level surface that passes through the point $(-4,2,4)$ can be found by computing $∇f(-4,2,4).$ 

So, we find the gradient and evaluate it at $(-4,2,4):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))i+\frac{∂}{∂y}(3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))j+\frac{∂}{∂z}(3{\left(-\left(x + 3\right)\right)}^{2}-\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))k \\  & =\left(-\left((6\left(-\left(x + 3\right)\right)-\left(-\left(z - 1\right)\right)+3\left(y - 2\right)\left(-\left(z - 1\right)\right))\right)\right)i+\left(+3\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right)\right)j+\left(-\left(+(-\left(-\left(x + 3\right)\right)+3\left(-\left(x + 3\right)\right)\left(y - 2\right))\right)\right)k\\∇f(-4,2,4)& =\left(-\left((6\left(-\left(\left(-4\right) + 3\right)\right)-\left(-\left(\left(4\right) - 1\right)\right)+3\left(\left(2\right) - 2\right)\left(-\left(\left(4\right) - 1\right)\right))\right)\right)i+\left(+3\left(-\left(\left(-4\right) + 3\right)\right)\left(-\left(\left(4\right) - 1\right)\right)\right)j+\left(-\left(+(-\left(-\left(\left(-4\right) + 3\right)\right)+3\left(-\left(\left(-4\right) + 3\right)\right)\left(\left(2\right) - 2\right))\right)\right)k\\  & =\left(-\left((6(1)-(-3)+3(0)(-3))\right)\right)i+\left(+3(1)(-3)\right)j+\left(-\left(+(-1+3(1)(0))\right)\right)k\\  & =\left(-\left(9\right)\right)i+\left(-9\right)j+\left(-\left(-1\right)\right)k\\  & =⟨-9,-9,1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-1}{9}=\frac{\left(y - 2\right)-0}{-9}=\frac{\left(-\left(z - 1\right)\right)-(-3)}{-1} \\ \frac{\left(-\left(x + 3\right)\right)-1}{9}=\frac{\left(y - 2\right)}{-9}=\frac{\left(-\left(z - 1\right)\right)+3}{-1}\end{aligned}
$$

## Generated normal variants — q-71411

Find the equation of the normal line to the surface $3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)=6-3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right)$ at the point $(4,-2,-6).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 4}{9}=\frac{y + 2}{9}=\frac{z + 6}{-2}$
- $\frac{x - 4}{9}=\frac{y + 2}{18}=\frac{z + 6}{-1}$
- $\frac{x - 4}{18}=\frac{y + 2}{9}=\frac{z + 6}{-1}$
- $\frac{x - 4}{9}=\frac{y + 2}{9}=\frac{z + 6}{-1}$ **keyed**
- $\frac{x - 5}{9}=\frac{y + 2}{9}=\frac{z + 6}{-1}$

First, we bring all variables to one side:

$$
\begin{aligned}3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right) & =6-3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right) \\ 3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right) & =6\end{aligned}
$$

If we set $f(x,y,z)=3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=6.$ 

A normal vector to the level surface that passes through the point $(4,-2,-6)$ can be found by computing $∇f(4,-2,-6).$ 

So, we find the gradient and evaluate it at $(4,-2,-6):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))i+\frac{∂}{∂y}(3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))j+\frac{∂}{∂z}(3{\left(x - 3\right)}^{2}-\left(x - 3\right)\left(z + 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))k \\  & =\left((6\left(x - 3\right)-\left(z + 3\right)+3\left(-\left(y + 2\right)\right)\left(z + 3\right))\right)i+\left(-\left(+3\left(x - 3\right)\left(z + 3\right)\right)\right)j+\left(+(-\left(x - 3\right)+3\left(x - 3\right)\left(-\left(y + 2\right)\right))\right)k\\∇f(4,-2,-6)& =\left((6\left(\left(4\right) - 3\right)-\left(\left(-6\right) + 3\right)+3\left(-\left(\left(-2\right) + 2\right)\right)\left(\left(-6\right) + 3\right))\right)i+\left(-\left(+3\left(\left(4\right) - 3\right)\left(\left(-6\right) + 3\right)\right)\right)j+\left(+(-\left(\left(4\right) - 3\right)+3\left(\left(4\right) - 3\right)\left(-\left(\left(-2\right) + 2\right)\right))\right)k\\  & =\left((6(1)-(-3)+3(0)(-3))\right)i+\left(-\left(+3(1)(-3)\right)\right)j+\left(+(-1+3(1)(0))\right)k\\  & =\left(9\right)i+\left(-\left(-9\right)\right)j+\left(-1\right)k\\  & =⟨9,9,-1⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-1}{9}=\frac{\left(-\left(y + 2\right)\right)-0}{-9}=\frac{\left(z + 3\right)-(-3)}{-1} \\ \frac{\left(x - 3\right)-1}{9}=\frac{\left(-\left(y + 2\right)\right)}{-9}=\frac{\left(z + 3\right)+3}{-1}\end{aligned}
$$

## Generated normal variants — q-36351

Find the equation of the normal line to the surface $z=\operatorname{ln}⁡(2x+y)$ at the point $(1,-1,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 1}{2}=\frac{y + 1}{2}=\frac{z}{-1}$
- $\frac{x - 1}{4}=\frac{y + 1}{1}=\frac{z}{-1}$
- $\frac{x - 1}{2}=\frac{y + 1}{1}=\frac{z}{-1}$ **keyed**
- $\frac{x - 2}{2}=\frac{y + 1}{1}=\frac{z}{-1}$
- $\frac{x - 1}{2}=\frac{y + 1}{1}=\frac{z}{-2}$

First, we bring all variables to one side:

$$
\begin{aligned}z & =\operatorname{ln}⁡(2x+y) \\ 0 & =\operatorname{ln}⁡(2x+y)-z\end{aligned}
$$

 

So, if we set $f(x,y,z)=\operatorname{ln}⁡(2x+y)-z$, then our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(1,-1,0)$ can be found by computing $∇f(1,-1,0).$

So, we find the gradient and evaluate it at $(1,-1,0):$ 

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(2x+y)-z)i+\frac{∂}{∂y}(\operatorname{ln}⁡(2x+y)-z)j+\frac{∂}{∂z}(\operatorname{ln}⁡(2x+y)-z)k \\  & =\frac{2}{2x+y}\text{ }i+\frac{1}{2x+y}\text{ }j-1\text{ }k \\ ∇f(1,-1,0) & =\frac{2}{2(1)+(-1)}\text{ }i+\frac{1}{2(1)+(-1)}\text{ }j-k \\  & =2\text{ }i+\,j-k \\  & =⟨2,\,1,\,-1⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-1}{2}=\frac{y-(-1)}{1}=\frac{z-0}{-1} \\ \frac{x-1}{2}=y+1=-z\end{aligned}
$$

## Generated normal variants — q-36351

Find the equation of the normal line to the surface $\left(-\left(z - 1\right)\right)=\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))$ at the point $(-4,1,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 4}{-2}=\frac{y - 1}{1}=\frac{z - 1}{1}$ **keyed**
- $\frac{x + 4}{-4}=\frac{y - 1}{1}=\frac{z - 1}{1}$
- $\frac{x + 4}{-2}=\frac{y - 1}{1}=\frac{z - 1}{2}$
- $\frac{x + 4}{-2}=\frac{y - 1}{2}=\frac{z - 1}{1}$
- $\frac{x + 3}{-2}=\frac{y - 1}{1}=\frac{z - 1}{1}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(-\left(z - 1\right)\right) & =\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right)) \\ 0 & =\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))-\left(-\left(z - 1\right)\right)\end{aligned}
$$

 

So, if we set $f(x,y,z)=\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))-\left(-\left(z - 1\right)\right)$, then our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(-4,1,1)$ can be found by computing $∇f(-4,1,1).$

So, we find the gradient and evaluate it at $(-4,1,1):$ 

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))-\left(-\left(z - 1\right)\right))i+\frac{∂}{∂y}(\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))-\left(-\left(z - 1\right)\right))j+\frac{∂}{∂z}(\operatorname{ln}⁡(2\left(-\left(x + 3\right)\right)+\left(y - 2\right))-\left(-\left(z - 1\right)\right))k \\  & =\left(-\left(\frac{2}{2\left(-\left(x + 3\right)\right)+\left(y - 2\right)}\right)\right)i+\left(+\frac{1}{2\left(-\left(x + 3\right)\right)+\left(y - 2\right)}\right)j+\left(-\left(-1\right)\right)k\\∇f(-4,1,1)& =\left(-\left(\frac{2}{2\left(-\left(\left(-4\right) + 3\right)\right)+\left(\left(1\right) - 2\right)}\right)\right)i+\left(+\frac{1}{2\left(-\left(\left(-4\right) + 3\right)\right)+\left(\left(1\right) - 2\right)}\right)j+\left(-\left(-1\right)\right)k\\  & =\left(-\left(\frac{2}{2(1)+(-1)}\right)\right)i+\left(+\frac{1}{2(1)+(-1)}\right)j+\left(-\left(-1\right)\right)k\\  & =\left(-\left(2\right)\right)i+\left(1\right)j+\left(-\left(-1\right)\right)k\\  & =⟨-2,\,1,1⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-1}{2}=\frac{\left(y - 2\right)-(-1)}{1}=\frac{\left(-\left(z - 1\right)\right)-0}{-1} \\ \frac{\left(-\left(x + 3\right)\right)-1}{2}=\left(y - 2\right)+1=-\left(-\left(z - 1\right)\right)\end{aligned}
$$

## Generated normal variants — q-36351

Find the equation of the normal line to the surface $\left(z + 3\right)=\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))$ at the point $(4,-1,-3).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 4}{2}=\frac{y + 1}{-1}=\frac{z + 3}{-2}$
- $\frac{x - 4}{2}=\frac{y + 1}{-2}=\frac{z + 3}{-1}$
- $\frac{x - 4}{4}=\frac{y + 1}{-1}=\frac{z + 3}{-1}$
- $\frac{x - 4}{2}=\frac{y + 1}{-1}=\frac{z + 3}{-1}$ **keyed**
- $\frac{x - 5}{2}=\frac{y + 1}{-1}=\frac{z + 3}{-1}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(z + 3\right) & =\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right)) \\ 0 & =\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))-\left(z + 3\right)\end{aligned}
$$

 

So, if we set $f(x,y,z)=\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))-\left(z + 3\right)$, then our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(4,-1,-3)$ can be found by computing $∇f(4,-1,-3).$

So, we find the gradient and evaluate it at $(4,-1,-3):$ 

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))-\left(z + 3\right))i+\frac{∂}{∂y}(\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))-\left(z + 3\right))j+\frac{∂}{∂z}(\operatorname{ln}⁡(2\left(x - 3\right)+\left(-\left(y + 2\right)\right))-\left(z + 3\right))k \\  & =\left(\frac{2}{2\left(x - 3\right)+\left(-\left(y + 2\right)\right)}\right)i+\left(-\left(+\frac{1}{2\left(x - 3\right)+\left(-\left(y + 2\right)\right)}\right)\right)j+\left(-1\right)k\\∇f(4,-1,-3)& =\left(\frac{2}{2\left(\left(4\right) - 3\right)+\left(-\left(\left(-1\right) + 2\right)\right)}\right)i+\left(-\left(+\frac{1}{2\left(\left(4\right) - 3\right)+\left(-\left(\left(-1\right) + 2\right)\right)}\right)\right)j+\left(-1\right)k\\  & =\left(\frac{2}{2(1)+(-1)}\right)i+\left(-\left(+\frac{1}{2(1)+(-1)}\right)\right)j+\left(-1\right)k\\  & =\left(2\right)i+\left(-\left(1\right)\right)j+\left(-1\right)k\\  & =⟨2,-1,\,-1⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get: 

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-1}{2}=\frac{\left(-\left(y + 2\right)\right)-(-1)}{1}=\frac{\left(z + 3\right)-0}{-1} \\ \frac{\left(x - 3\right)-1}{2}=\left(-\left(y + 2\right)\right)+1=-\left(z + 3\right)\end{aligned}
$$

## Generated normal variants — q-71408

Find the equation of the normal line to the surface ${x}^{2}+{y}^{2}+{z}^{2}=3$ at the point $(-1,-1,1).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 1}{-2}=\frac{y + 1}{-4}=\frac{z - 1}{2}$
- $\frac{x + 1}{-4}=\frac{y + 1}{-2}=\frac{z - 1}{2}$
- $\frac{x + 1}{-2}=\frac{y + 1}{-2}=\frac{z - 1}{2}$ **keyed**
- $\frac{x}{-2}=\frac{y + 1}{-2}=\frac{z - 1}{2}$
- $\frac{x + 1}{-2}=\frac{y + 1}{-2}=\frac{z - 1}{4}$

If we set $f(x,y,z)={x}^{2}+{y}^{2}+{z}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=3.$ 

A normal vector to the level surface that passes through the point $(-1,-1,1)$ can be found by computing $∇f(-1,-1,1).$ 

So, we find the gradient and evaluate it at $(-1,-1,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({x}^{2}+{y}^{2}+{z}^{2})i+\frac{∂}{∂y}({x}^{2}+{y}^{2}+{z}^{2})j+\frac{∂}{∂z}({x}^{2}+{y}^{2}+{z}^{2})k \\  & =2x\text{ }i+2y\text{ }j+2z\text{ }k \\ ∇f(-1,-1,1) & =2(-1)\text{ }i+2(-1)\text{ }j+2(1)\text{ }k \\  & =-2\,i-2\,j+2\,k \\  & =⟨-2,-2,2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-(-1)}{-2}=\frac{y-(-1)}{-2}=\frac{z-1}{2} \\ \frac{x+1}{-2}=\frac{y+1}{-2}=\frac{z-1}{2} \\ \frac{x+1}{1}=\frac{y+1}{1}=\frac{z-1}{-1} \\ x+1=y+1=\frac{z-1}{-1}\end{aligned}
$$

## Generated normal variants — q-71408

Find the equation of the normal line to the surface ${\left(-\left(x + 3\right)\right)}^{2}+{\left(y - 2\right)}^{2}+{\left(-\left(z - 1\right)\right)}^{2}=3$ at the point $(-2,1,0).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 2}{2}=\frac{y - 1}{-2}=\frac{z}{-2}$ **keyed**
- $\frac{x + 2}{4}=\frac{y - 1}{-2}=\frac{z}{-2}$
- $\frac{x + 2}{2}=\frac{y - 1}{-2}=\frac{z}{-4}$
- $\frac{x + 2}{2}=\frac{y - 1}{-4}=\frac{z}{-2}$
- $\frac{x + 1}{2}=\frac{y - 1}{-2}=\frac{z}{-2}$

If we set $f(x,y,z)={\left(-\left(x + 3\right)\right)}^{2}+{\left(y - 2\right)}^{2}+{\left(-\left(z - 1\right)\right)}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=3.$ 

A normal vector to the level surface that passes through the point $(-2,1,0)$ can be found by computing $∇f(-2,1,0).$ 

So, we find the gradient and evaluate it at $(-2,1,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(x + 3\right)\right)}^{2}+{\left(y - 2\right)}^{2}+{\left(-\left(z - 1\right)\right)}^{2})i+\frac{∂}{∂y}({\left(-\left(x + 3\right)\right)}^{2}+{\left(y - 2\right)}^{2}+{\left(-\left(z - 1\right)\right)}^{2})j+\frac{∂}{∂z}({\left(-\left(x + 3\right)\right)}^{2}+{\left(y - 2\right)}^{2}+{\left(-\left(z - 1\right)\right)}^{2})k \\  & =\left(-\left(2\left(-\left(x + 3\right)\right)\right)\right)i+\left(+2\left(y - 2\right)\right)j+\left(-\left(+2\left(-\left(z - 1\right)\right)\right)\right)k\\∇f(-2,1,0)& =\left(-\left(2\left(-\left(\left(-2\right) + 3\right)\right)\right)\right)i+\left(+2\left(\left(1\right) - 2\right)\right)j+\left(-\left(+2\left(-\left(\left(0\right) - 1\right)\right)\right)\right)k\\  & =\left(-\left(2(-1)\right)\right)i+\left(+2(-1)\right)j+\left(-\left(+2(1)\right)\right)k\\  & =\left(-\left(-2\right)\right)i+\left(-2\right)j+\left(-\left(+2\right)\right)k\\  & =⟨2,-2,-2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-(-1)}{-2}=\frac{\left(y - 2\right)-(-1)}{-2}=\frac{\left(-\left(z - 1\right)\right)-1}{2} \\ \frac{\left(-\left(x + 3\right)\right)+1}{-2}=\frac{\left(y - 2\right)+1}{-2}=\frac{\left(-\left(z - 1\right)\right)-1}{2} \\ \frac{\left(-\left(x + 3\right)\right)+1}{1}=\frac{\left(y - 2\right)+1}{1}=\frac{\left(-\left(z - 1\right)\right)-1}{-1} \\ \left(-\left(x + 3\right)\right)+1=\left(y - 2\right)+1=\frac{\left(-\left(z - 1\right)\right)-1}{-1}\end{aligned}
$$

## Generated normal variants — q-71408

Find the equation of the normal line to the surface ${\left(x - 3\right)}^{2}+{\left(-\left(y + 2\right)\right)}^{2}+{\left(z + 3\right)}^{2}=3$ at the point $(2,-1,-2).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 2}{-2}=\frac{y + 1}{2}=\frac{z + 2}{4}$
- $\frac{x - 2}{-2}=\frac{y + 1}{4}=\frac{z + 2}{2}$
- $\frac{x - 2}{-4}=\frac{y + 1}{2}=\frac{z + 2}{2}$
- $\frac{x - 2}{-2}=\frac{y + 1}{2}=\frac{z + 2}{2}$ **keyed**
- $\frac{x - 3}{-2}=\frac{y + 1}{2}=\frac{z + 2}{2}$

If we set $f(x,y,z)={\left(x - 3\right)}^{2}+{\left(-\left(y + 2\right)\right)}^{2}+{\left(z + 3\right)}^{2}$, our surface can be viewed as the level surface $f(x,y,z)=3.$ 

A normal vector to the level surface that passes through the point $(2,-1,-2)$ can be found by computing $∇f(2,-1,-2).$ 

So, we find the gradient and evaluate it at $(2,-1,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(x - 3\right)}^{2}+{\left(-\left(y + 2\right)\right)}^{2}+{\left(z + 3\right)}^{2})i+\frac{∂}{∂y}({\left(x - 3\right)}^{2}+{\left(-\left(y + 2\right)\right)}^{2}+{\left(z + 3\right)}^{2})j+\frac{∂}{∂z}({\left(x - 3\right)}^{2}+{\left(-\left(y + 2\right)\right)}^{2}+{\left(z + 3\right)}^{2})k \\  & =\left(2\left(x - 3\right)\right)i+\left(-\left(+2\left(-\left(y + 2\right)\right)\right)\right)j+\left(+2\left(z + 3\right)\right)k\\∇f(2,-1,-2)& =\left(2\left(\left(2\right) - 3\right)\right)i+\left(-\left(+2\left(-\left(\left(-1\right) + 2\right)\right)\right)\right)j+\left(+2\left(\left(-2\right) + 3\right)\right)k\\  & =\left(2(-1)\right)i+\left(-\left(+2(-1)\right)\right)j+\left(+2(1)\right)k\\  & =\left(-2\right)i+\left(-\left(-2\right)\right)j+\left(+2\right)k\\  & =⟨-2,2,2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-(-1)}{-2}=\frac{\left(-\left(y + 2\right)\right)-(-1)}{-2}=\frac{\left(z + 3\right)-1}{2} \\ \frac{\left(x - 3\right)+1}{-2}=\frac{\left(-\left(y + 2\right)\right)+1}{-2}=\frac{\left(z + 3\right)-1}{2} \\ \frac{\left(x - 3\right)+1}{1}=\frac{\left(-\left(y + 2\right)\right)+1}{1}=\frac{\left(z + 3\right)-1}{-1} \\ \left(x - 3\right)+1=\left(-\left(y + 2\right)\right)+1=\frac{\left(z + 3\right)-1}{-1}\end{aligned}
$$

## Generated normal variants — q-131124

Find a vector equation of the normal line to the surface $4{z}^{2}-4{y}^{2}={x}^{2}-6x+12$ at the point $(2,0,1).$

Field 0 (:answer-field.type/radio)

- $⟨2,0,1⟩+t\,⟨2,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,1⟩+t\,⟨0,0,8⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,1⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨2,1,1⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$
- $⟨2,0,1⟩+t\,⟨2,2,8⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}4{z}^{2}-4{y}^{2} & ={x}^{2}-6x +12\\ 4{z}^{2}-4{y}^{2}-{x}^{2}+6x & =12\end{aligned}
$$

If we set $f(x,y,z)=4{z}^{2}-4{y}^{2}-{x}^{2}+6x$, our surface can be viewed as the level surface $f(x,y,z)=12.$ 

A normal vector to the level surface that passes through the point $(2,0,1)$ can be found by computing $∇f(2,0,1).$ 

So, we find the gradient and evaluate it at $(2,0,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)i+\frac{∂}{∂y}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)j+\frac{∂}{∂z}(4{z}^{2}-4{y}^{2}-{x}^{2}+6x)k \\  & =(6-2x)\,i-8y\,j+8z\,k \\ ∇f(2,0,1) & =(6-2(2))\,i-8(0)\text{ }j+8(1)\,k \\  & =2\,i+8\,k \\  & =⟨2,0,8⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,0,1)$ and passes through the point $(2,0,1)$ can be written as

$$
\begin{aligned}r & =⟨2,0,1⟩+t\,∇f(2,0,1)=⟨2,0,1⟩+t\,⟨2,0,8⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131124

Find a vector equation of the normal line to the surface $4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}={\left(-\left(x + 3\right)\right)}^{2}-6\left(-\left(x + 3\right)\right)+12$ at the point $(-5,2,0).$

Field 0 (:answer-field.type/radio)

- $⟨-5,2,0⟩+t\,⟨-2,0,-8⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨-5,2,0⟩+t\,⟨0,0,-8⟩,\,t\in (-\infty ,\infty )$
- $⟨-5,2,0⟩+t\,⟨-2,-2,-8⟩,\,t\in (-\infty ,\infty )$
- $⟨-5,2,0⟩+t\,⟨-2,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨-5,3,0⟩+t\,⟨-2,0,-8⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2} & ={\left(-\left(x + 3\right)\right)}^{2}-6\left(-\left(x + 3\right)\right) +12\\ 4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}-{\left(-\left(x + 3\right)\right)}^{2}+6\left(-\left(x + 3\right)\right) & =12\end{aligned}
$$

If we set $f(x,y,z)=4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}-{\left(-\left(x + 3\right)\right)}^{2}+6\left(-\left(x + 3\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=12.$ 

A normal vector to the level surface that passes through the point $(-5,2,0)$ can be found by computing $∇f(-5,2,0).$ 

So, we find the gradient and evaluate it at $(-5,2,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}-{\left(-\left(x + 3\right)\right)}^{2}+6\left(-\left(x + 3\right)\right))i+\frac{∂}{∂y}(4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}-{\left(-\left(x + 3\right)\right)}^{2}+6\left(-\left(x + 3\right)\right))j+\frac{∂}{∂z}(4{\left(-\left(z - 1\right)\right)}^{2}-4{\left(y - 2\right)}^{2}-{\left(-\left(x + 3\right)\right)}^{2}+6\left(-\left(x + 3\right)\right))k \\  & =\left(-\left((6-2\left(-\left(x + 3\right)\right))\right)\right)i+\left(-8\left(y - 2\right)\right)j+\left(-\left(+8\left(-\left(z - 1\right)\right)\right)\right)k\\∇f(-5,2,0)& =\left(-\left((6-2\left(-\left(\left(-5\right) + 3\right)\right))\right)\right)i+\left(-8\left(\left(2\right) - 2\right)\right)j+\left(-\left(+8\left(-\left(\left(0\right) - 1\right)\right)\right)\right)k\\  & =\left(-\left((6-2(2))\right)\right)i+\left(-8(0)\right)j+\left(-\left(+8(1)\right)\right)k\\  & =\left(-\left(2\right)\right)i+\left(0\right)j+\left(-\left(+8\right)\right)k\\  & =⟨-2,0,-8⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(-5,2,0)$ and passes through the point $(-5,2,0)$ can be written as

$$
\begin{aligned}r & =⟨-5,2,0⟩+t\,∇f(-5,2,0)=⟨-5,2,0⟩+t\,⟨-2,0,-8⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131124

Find a vector equation of the normal line to the surface $4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}={\left(x - 3\right)}^{2}-6\left(x - 3\right)+12$ at the point $(5,-2,-2).$

Field 0 (:answer-field.type/radio)

- $⟨5,-2,-2⟩+t\,⟨2,2,8⟩,\,t\in (-\infty ,\infty )$
- $⟨5,-2,-2⟩+t\,⟨2,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨5,-2,-2⟩+t\,⟨0,0,8⟩,\,t\in (-\infty ,\infty )$
- $⟨5,-2,-2⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨5,-1,-2⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2} & ={\left(x - 3\right)}^{2}-6\left(x - 3\right) +12\\ 4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right) & =12\end{aligned}
$$

If we set $f(x,y,z)=4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=12.$ 

A normal vector to the level surface that passes through the point $(5,-2,-2)$ can be found by computing $∇f(5,-2,-2).$ 

So, we find the gradient and evaluate it at $(5,-2,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))i+\frac{∂}{∂y}(4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))j+\frac{∂}{∂z}(4{\left(z + 3\right)}^{2}-4{\left(-\left(y + 2\right)\right)}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))k \\  & =\left((6-2\left(x - 3\right))\right)i+\left(-\left(-8\left(-\left(y + 2\right)\right)\right)\right)j+\left(+8\left(z + 3\right)\right)k\\∇f(5,-2,-2)& =\left((6-2\left(\left(5\right) - 3\right))\right)i+\left(-\left(-8\left(-\left(\left(-2\right) + 2\right)\right)\right)\right)j+\left(+8\left(\left(-2\right) + 3\right)\right)k\\  & =\left((6-2(2))\right)i+\left(-\left(-8(0)\right)\right)j+\left(+8(1)\right)k\\  & =\left(2\right)i+\left(-\left(0\right)\right)j+\left(+8\right)k\\  & =⟨2,0,8⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(5,-2,-2)$ and passes through the point $(5,-2,-2)$ can be written as

$$
\begin{aligned}r & =⟨5,-2,-2⟩+t\,∇f(5,-2,-2)=⟨5,-2,-2⟩+t\,⟨2,0,8⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131129

Find the equation of the normal line to the surface ${e}^{x+y+z}-2xyz=-3$ at the point $(2,-1,-1).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 2}{-1}=\frac{y + 1}{10}=\frac{z + 1}{5}$
- $\frac{x - 2}{-2}=\frac{y + 1}{5}=\frac{z + 1}{5}$
- $\frac{x - 2}{-1}=\frac{y + 1}{5}=\frac{z + 1}{5}$ **keyed**
- $\frac{x - 3}{-1}=\frac{y + 1}{5}=\frac{z + 1}{5}$
- $\frac{x - 2}{-1}=\frac{y + 1}{5}=\frac{z + 1}{10}$

Let's set $f(x,y,z)={e}^{x+y+z}-2xyz.$ Then, our surface can be viewed as the level surface $f(x,y,z)=-3.$ 

A normal vector to the level surface that passes through the point $(2,-1,-1)$ can be found by computing $∇f(2,-1,-1).$ 

So, we find the gradient and evaluate it at $(2,-1,-1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({e}^{x+y+z}-2xyz)i+\frac{∂}{∂y}({e}^{x+y+z}-2xyz)j+\frac{∂}{∂z}({e}^{x+y+z}-2xyz)k \\  & =({e}^{x+y+z}-2yz)\text{ }i+({e}^{x+y+z}-2xz)\text{ }j+({e}^{x+y+z}-2xy)\text{ }k \\ ∇f(2,-1,-1) & =({e}^{2-1-1}-2(-1)(-1))\text{ }i+({e}^{2-1-1}-2(2)(-1))\text{ }j+({e}^{2-1-1}-2(2)(-1))\text{ }k \\  & =({e}^{0}-2)\text{ }i+({e}^{0}+4)\text{ }j+({e}^{0}+4)\text{ }k \\  & =-i+5\,j+5\,k \\  & =⟨-1,5,5⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{(-1)}=\frac{y-(-1)}{5}=\frac{z-(-1)}{5} \\ \frac{x-2}{(-1)}=\frac{y+1}{5}=\frac{z+1}{5} \\ 2-x=\frac{y+1}{5}=\frac{z+1}{5}\end{aligned}
$$

## Generated normal variants — q-131129

Find the equation of the normal line to the surface ${e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right)=-3$ at the point $(-5,1,2).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 5}{1}=\frac{y - 1}{5}=\frac{z - 2}{-5}$ **keyed**
- $\frac{x + 5}{2}=\frac{y - 1}{5}=\frac{z - 2}{-5}$
- $\frac{x + 5}{1}=\frac{y - 1}{5}=\frac{z - 2}{-10}$
- $\frac{x + 5}{1}=\frac{y - 1}{10}=\frac{z - 2}{-5}$
- $\frac{x + 4}{1}=\frac{y - 1}{5}=\frac{z - 2}{-5}$

Let's set $f(x,y,z)={e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=-3.$ 

A normal vector to the level surface that passes through the point $(-5,1,2)$ can be found by computing $∇f(-5,1,2).$ 

So, we find the gradient and evaluate it at $(-5,1,2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))i+\frac{∂}{∂y}({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))j+\frac{∂}{∂z}({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right)\left(-\left(z - 1\right)\right))k \\  & =\left(-\left(({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(y - 2\right)\left(-\left(z - 1\right)\right))\right)\right)i+\left(+({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(-\left(z - 1\right)\right))\right)j+\left(-\left(+({e}^{\left(-\left(x + 3\right)\right)+\left(y - 2\right)+\left(-\left(z - 1\right)\right)}-2\left(-\left(x + 3\right)\right)\left(y - 2\right))\right)\right)k\\∇f(-5,1,2)& =\left(-\left(({e}^{\left(-\left(\left(-5\right) + 3\right)\right)+\left(\left(1\right) - 2\right)+\left(-\left(\left(2\right) - 1\right)\right)}-2\left(\left(1\right) - 2\right)\left(-\left(\left(2\right) - 1\right)\right))\right)\right)i+\left(+({e}^{\left(-\left(\left(-5\right) + 3\right)\right)+\left(\left(1\right) - 2\right)+\left(-\left(\left(2\right) - 1\right)\right)}-2\left(-\left(\left(-5\right) + 3\right)\right)\left(-\left(\left(2\right) - 1\right)\right))\right)j+\left(-\left(+({e}^{\left(-\left(\left(-5\right) + 3\right)\right)+\left(\left(1\right) - 2\right)+\left(-\left(\left(2\right) - 1\right)\right)}-2\left(-\left(\left(-5\right) + 3\right)\right)\left(\left(1\right) - 2\right))\right)\right)k\\  & =\left(-\left(({e}^{2-1-1}-2(-1)(-1))\right)\right)i+\left(+({e}^{2-1-1}-2(2)(-1))\right)j+\left(-\left(+({e}^{2-1-1}-2(2)(-1))\right)\right)k\\  & =\left(-\left(({e}^{0}-2)\right)\right)i+\left(+({e}^{0}+4)\right)j+\left(-\left(+({e}^{0}+4)\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(+5\right)j+\left(-\left(+5\right)\right)k\\  & =⟨1,5,-5⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-2}{(-1)}=\frac{\left(y - 2\right)-(-1)}{5}=\frac{\left(-\left(z - 1\right)\right)-(-1)}{5} \\ \frac{\left(-\left(x + 3\right)\right)-2}{(-1)}=\frac{\left(y - 2\right)+1}{5}=\frac{\left(-\left(z - 1\right)\right)+1}{5} \\ 2-\left(-\left(x + 3\right)\right)=\frac{\left(y - 2\right)+1}{5}=\frac{\left(-\left(z - 1\right)\right)+1}{5}\end{aligned}
$$

## Generated normal variants — q-131129

Find the equation of the normal line to the surface ${e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right)=-3$ at the point $(5,-1,-4).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 5}{-1}=\frac{y + 1}{-5}=\frac{z + 4}{10}$
- $\frac{x - 5}{-1}=\frac{y + 1}{-10}=\frac{z + 4}{5}$
- $\frac{x - 5}{-2}=\frac{y + 1}{-5}=\frac{z + 4}{5}$
- $\frac{x - 5}{-1}=\frac{y + 1}{-5}=\frac{z + 4}{5}$ **keyed**
- $\frac{x - 6}{-1}=\frac{y + 1}{-5}=\frac{z + 4}{5}$

Let's set $f(x,y,z)={e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=-3.$ 

A normal vector to the level surface that passes through the point $(5,-1,-4)$ can be found by computing $∇f(5,-1,-4).$ 

So, we find the gradient and evaluate it at $(5,-1,-4):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))i+\frac{∂}{∂y}({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))j+\frac{∂}{∂z}({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right)\left(z + 3\right))k \\  & =\left(({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(-\left(y + 2\right)\right)\left(z + 3\right))\right)i+\left(-\left(+({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(z + 3\right))\right)\right)j+\left(+({e}^{\left(x - 3\right)+\left(-\left(y + 2\right)\right)+\left(z + 3\right)}-2\left(x - 3\right)\left(-\left(y + 2\right)\right))\right)k\\∇f(5,-1,-4)& =\left(({e}^{\left(\left(5\right) - 3\right)+\left(-\left(\left(-1\right) + 2\right)\right)+\left(\left(-4\right) + 3\right)}-2\left(-\left(\left(-1\right) + 2\right)\right)\left(\left(-4\right) + 3\right))\right)i+\left(-\left(+({e}^{\left(\left(5\right) - 3\right)+\left(-\left(\left(-1\right) + 2\right)\right)+\left(\left(-4\right) + 3\right)}-2\left(\left(5\right) - 3\right)\left(\left(-4\right) + 3\right))\right)\right)j+\left(+({e}^{\left(\left(5\right) - 3\right)+\left(-\left(\left(-1\right) + 2\right)\right)+\left(\left(-4\right) + 3\right)}-2\left(\left(5\right) - 3\right)\left(-\left(\left(-1\right) + 2\right)\right))\right)k\\  & =\left(({e}^{2-1-1}-2(-1)(-1))\right)i+\left(-\left(+({e}^{2-1-1}-2(2)(-1))\right)\right)j+\left(+({e}^{2-1-1}-2(2)(-1))\right)k\\  & =\left(({e}^{0}-2)\right)i+\left(-\left(+({e}^{0}+4)\right)\right)j+\left(+({e}^{0}+4)\right)k\\  & =\left(-1\right)i+\left(-\left(+5\right)\right)j+\left(+5\right)k\\  & =⟨-1,-5,5⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-2}{(-1)}=\frac{\left(-\left(y + 2\right)\right)-(-1)}{5}=\frac{\left(z + 3\right)-(-1)}{5} \\ \frac{\left(x - 3\right)-2}{(-1)}=\frac{\left(-\left(y + 2\right)\right)+1}{5}=\frac{\left(z + 3\right)+1}{5} \\ 2-\left(x - 3\right)=\frac{\left(-\left(y + 2\right)\right)+1}{5}=\frac{\left(z + 3\right)+1}{5}\end{aligned}
$$

## Generated normal variants — q-37232

Find the equation of the normal line to the surface $\sqrt{2{x}^{2}+y-4z}=1$ at the point $(2,1,2).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 2}{4}=\frac{y - 1}{1}=\frac{z - 2}{-2}$
- $\frac{x - 2}{8}=\frac{y - 1}{\frac{1}{2}}=\frac{z - 2}{-2}$
- $\frac{x - 2}{4}=\frac{y - 1}{\frac{1}{2}}=\frac{z - 2}{-2}$ **keyed**
- $\frac{x - 3}{4}=\frac{y - 1}{\frac{1}{2}}=\frac{z - 2}{-2}$
- $\frac{x - 2}{4}=\frac{y - 1}{\frac{1}{2}}=\frac{z - 2}{-4}$

Let's set $f(x,y,z)=\sqrt{2{x}^{2}+y-4z}.$ Then, our surface can be viewed as the level surface $f(x,y,z)=1.$     

A normal vector to the level surface that passes through the point $(2,1,2)$ can be found by computing $∇f(2,1,2).$

So, we find the gradient and evaluate it at $(2,1,2):$    

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\sqrt{2{x}^{2}+y-4z})\text{ }i+\frac{∂}{∂y}(\sqrt{2{x}^{2}+y-4z})\text{ }j+\frac{∂}{∂z}(\sqrt{2{x}^{2}+y-4z})\text{ }k \\  & =\frac{2x}{\sqrt{2{x}^{2}+y-4z}}\text{ }i+\frac{1}{2\sqrt{2{x}^{2}+y-4z}}\text{ }j-\frac{2}{\sqrt{2{x}^{2}+y-4z}}\text{ }k \\ ∇f(2,1,2) & =\frac{2\cdot 2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }i+\frac{1}{2\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }j-\frac{2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\text{ }k \\  & =4\text{ }i+\frac{1}{2}\text{ }j-2\text{ }k \\  & =⟨4,\,\frac{1}{2},\,-2⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{x-2}{4}=\frac{y-1}{\frac{1}{2}}=\frac{z-2}{-2} \\ \frac{x-2}{4}=2y-2=\frac{2-z}{2}\end{aligned}
$$

## Generated normal variants — q-37232

Find the equation of the normal line to the surface $\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)}=1$ at the point $(-5,3,-1).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 5}{-4}=\frac{y - 3}{\frac{1}{2}}=\frac{z + 1}{2}$ **keyed**
- $\frac{x + 5}{-8}=\frac{y - 3}{\frac{1}{2}}=\frac{z + 1}{2}$
- $\frac{x + 5}{-4}=\frac{y - 3}{\frac{1}{2}}=\frac{z + 1}{4}$
- $\frac{x + 5}{-4}=\frac{y - 3}{1}=\frac{z + 1}{2}$
- $\frac{x + 4}{-4}=\frac{y - 3}{\frac{1}{2}}=\frac{z + 1}{2}$

Let's set $f(x,y,z)=\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)}.$ Then, our surface can be viewed as the level surface $f(x,y,z)=1.$     

A normal vector to the level surface that passes through the point $(-5,3,-1)$ can be found by computing $∇f(-5,3,-1).$

So, we find the gradient and evaluate it at $(-5,3,-1):$    

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)})\text{ }i+\frac{∂}{∂y}(\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)})\text{ }j+\frac{∂}{∂z}(\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)})\text{ }k \\  & =\left(-\left(\frac{2\left(-\left(x + 3\right)\right)}{\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)}}\right)\right)i+\left(+\frac{1}{2\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)}}\right)j+\left(-\left(-\frac{2}{\sqrt{2{\left(-\left(x + 3\right)\right)}^{2}+\left(y - 2\right)-4\left(-\left(z - 1\right)\right)}}\right)\right)k\\∇f(-5,3,-1)& =\left(-\left(\frac{2\left(-\left(\left(-5\right) + 3\right)\right)}{\sqrt{2{\left(-\left(\left(-5\right) + 3\right)\right)}^{2}+\left(\left(3\right) - 2\right)-4\left(-\left(\left(-1\right) - 1\right)\right)}}\right)\right)i+\left(+\frac{1}{2\sqrt{2{\left(-\left(\left(-5\right) + 3\right)\right)}^{2}+\left(\left(3\right) - 2\right)-4\left(-\left(\left(-1\right) - 1\right)\right)}}\right)j+\left(-\left(-\frac{2}{\sqrt{2{\left(-\left(\left(-5\right) + 3\right)\right)}^{2}+\left(\left(3\right) - 2\right)-4\left(-\left(\left(-1\right) - 1\right)\right)}}\right)\right)k\\  & =\left(-\left(\frac{2\cdot 2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)\right)i+\left(+\frac{1}{2\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)j+\left(-\left(-\frac{2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)\right)k\\  & =\left(-\left(4\right)\right)i+\left(+\frac{1}{2}\right)j+\left(-\left(-2\right)\right)k\\  & =⟨-4,\,\frac{1}{2},2⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x + 3\right)\right)-2}{4}=\frac{\left(y - 2\right)-1}{\frac{1}{2}}=\frac{\left(-\left(z - 1\right)\right)-2}{-2} \\ \frac{\left(-\left(x + 3\right)\right)-2}{4}=2\left(y - 2\right)-2=\frac{2-\left(-\left(z - 1\right)\right)}{2}\end{aligned}
$$

## Generated normal variants — q-37232

Find the equation of the normal line to the surface $\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)}=1$ at the point $(5,-3,-1).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 5}{4}=\frac{y + 3}{- \frac{1}{2}}=\frac{z + 1}{-4}$
- $\frac{x - 5}{4}=\frac{y + 3}{-1}=\frac{z + 1}{-2}$
- $\frac{x - 5}{8}=\frac{y + 3}{- \frac{1}{2}}=\frac{z + 1}{-2}$
- $\frac{x - 5}{4}=\frac{y + 3}{- \frac{1}{2}}=\frac{z + 1}{-2}$ **keyed**
- $\frac{x - 6}{4}=\frac{y + 3}{- \frac{1}{2}}=\frac{z + 1}{-2}$

Let's set $f(x,y,z)=\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)}.$ Then, our surface can be viewed as the level surface $f(x,y,z)=1.$     

A normal vector to the level surface that passes through the point $(5,-3,-1)$ can be found by computing $∇f(5,-3,-1).$

So, we find the gradient and evaluate it at $(5,-3,-1):$    

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}(\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)})\text{ }i+\frac{∂}{∂y}(\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)})\text{ }j+\frac{∂}{∂z}(\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)})\text{ }k \\  & =\left(\frac{2\left(x - 3\right)}{\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)}}\right)i+\left(-\left(+\frac{1}{2\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)}}\right)\right)j+\left(-\frac{2}{\sqrt{2{\left(x - 3\right)}^{2}+\left(-\left(y + 2\right)\right)-4\left(z + 3\right)}}\right)k\\∇f(5,-3,-1)& =\left(\frac{2\left(\left(5\right) - 3\right)}{\sqrt{2{\left(\left(5\right) - 3\right)}^{2}+\left(-\left(\left(-3\right) + 2\right)\right)-4\left(\left(-1\right) + 3\right)}}\right)i+\left(-\left(+\frac{1}{2\sqrt{2{\left(\left(5\right) - 3\right)}^{2}+\left(-\left(\left(-3\right) + 2\right)\right)-4\left(\left(-1\right) + 3\right)}}\right)\right)j+\left(-\frac{2}{\sqrt{2{\left(\left(5\right) - 3\right)}^{2}+\left(-\left(\left(-3\right) + 2\right)\right)-4\left(\left(-1\right) + 3\right)}}\right)k\\  & =\left(\frac{2\cdot 2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)i+\left(-\left(+\frac{1}{2\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)\right)j+\left(-\frac{2}{\sqrt{2\cdot {2}^{2}+1-4\cdot 2}}\right)k\\  & =\left(4\right)i+\left(-\left(+\frac{1}{2}\right)\right)j+\left(-2\right)k\\  & =⟨4,- \frac{1}{2},\,-2⟩\end{aligned}
$$

Finally, by using the symmetric form of the equation of the line that is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$,  we get:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-2}{4}=\frac{\left(-\left(y + 2\right)\right)-1}{\frac{1}{2}}=\frac{\left(z + 3\right)-2}{-2} \\ \frac{\left(x - 3\right)-2}{4}=2\left(-\left(y + 2\right)\right)-2=\frac{2-\left(z + 3\right)}{2}\end{aligned}
$$

## Generated normal variants — q-71407

Find a vector equation of the normal line to the surface $z=2{x}^{2}+2{y}^{2}+x$ at the point $(\frac{1}{2},1,3).$

Field 0 (:answer-field.type/radio)

- $r=⟨\frac{1}{2},1,3⟩+t\,⟨-3,0,1⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨0,-4,1⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨-3,-4,1⟩$ **keyed**
- $r=⟨\frac{3}{2},1,3⟩+t\,⟨-3,-4,1⟩$
- $r=⟨\frac{1}{2},1,3⟩+t\,⟨-3,-4,0⟩$

First, we bring all variables to one side:

$$
\begin{aligned}z & =2{x}^{2}+2{y}^{2}+x \\ z-2{x}^{2}-2{y}^{2}-x & =0\end{aligned}
$$

If we set $f(x,y,z)=z-2{x}^{2}-2{y}^{2}-x$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(\frac{1}{2},1,3)$ can be found by computing $∇f(\frac{1}{2},1,3).$ 

So, we find the gradient and evaluate it at $(\frac{1}{2},1,3):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(z-2{x}^{2}-2{y}^{2}-x)i+\frac{∂}{∂y}(z-2{x}^{2}-2{y}^{2}-x)j+\frac{∂}{∂z}(z-2{x}^{2}-2{y}^{2}-x)k \\  & =(-4x-1)\text{ }i-4y\text{ }j+k \\ ∇f(\frac{1}{2},1,3) & =(-4(\frac{1}{2})-1)\,i-4(1)\text{ }j+k \\  & =-3\,i-4\,j+k \\  & =⟨-3,-4,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(\frac{1}{2},1,3)$ and passes through the point $(\frac{1}{2},1,3)$ can be written as

$$
\begin{aligned}r & =⟨\frac{1}{2},1,3⟩+t\,∇f(\frac{1}{2},1,3)=⟨\frac{1}{2},1,3⟩+t\,⟨-3,-4,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-71407

Find a vector equation of the normal line to the surface $\left(-\left(z - 1\right)\right)=2{\left(-\left(x + 3\right)\right)}^{2}+2{\left(y - 2\right)}^{2}+\left(-\left(x + 3\right)\right)$ at the point $(- \frac{7}{2},3,-2).$

Field 0 (:answer-field.type/radio)

- $r=⟨- \frac{7}{2},3,-2⟩+t\,⟨3,-4,-1⟩$ **keyed**
- $r=⟨- \frac{7}{2},3,-2⟩+t\,⟨0,-4,-1⟩$
- $r=⟨- \frac{7}{2},3,-2⟩+t\,⟨3,-4,0⟩$
- $r=⟨- \frac{7}{2},3,-2⟩+t\,⟨3,0,-1⟩$
- $r=⟨- \frac{5}{2},3,-2⟩+t\,⟨3,-4,-1⟩$

First, we bring all variables to one side:

$$
\begin{aligned}\left(-\left(z - 1\right)\right) & =2{\left(-\left(x + 3\right)\right)}^{2}+2{\left(y - 2\right)}^{2}+\left(-\left(x + 3\right)\right) \\ \left(-\left(z - 1\right)\right)-2{\left(-\left(x + 3\right)\right)}^{2}-2{\left(y - 2\right)}^{2}-\left(-\left(x + 3\right)\right) & =0\end{aligned}
$$

If we set $f(x,y,z)=\left(-\left(z - 1\right)\right)-2{\left(-\left(x + 3\right)\right)}^{2}-2{\left(y - 2\right)}^{2}-\left(-\left(x + 3\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(- \frac{7}{2},3,-2)$ can be found by computing $∇f(- \frac{7}{2},3,-2).$ 

So, we find the gradient and evaluate it at $(- \frac{7}{2},3,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\left(-\left(z - 1\right)\right)-2{\left(-\left(x + 3\right)\right)}^{2}-2{\left(y - 2\right)}^{2}-\left(-\left(x + 3\right)\right))i+\frac{∂}{∂y}(\left(-\left(z - 1\right)\right)-2{\left(-\left(x + 3\right)\right)}^{2}-2{\left(y - 2\right)}^{2}-\left(-\left(x + 3\right)\right))j+\frac{∂}{∂z}(\left(-\left(z - 1\right)\right)-2{\left(-\left(x + 3\right)\right)}^{2}-2{\left(y - 2\right)}^{2}-\left(-\left(x + 3\right)\right))k \\  & =\left(-\left((-4\left(-\left(x + 3\right)\right)-1)\right)\right)i+\left(-4\left(y - 2\right)\right)j+\left(-\left(1\right)\right)k\\∇f(- \frac{7}{2},3,-2)& =\left(-\left((-4\left(-\left(\left(- \frac{7}{2}\right) + 3\right)\right)-1)\right)\right)i+\left(-4\left(\left(3\right) - 2\right)\right)j+\left(-\left(1\right)\right)k\\  & =\left(-\left((-4(\frac{1}{2})-1)\right)\right)i+\left(-4(1)\right)j+\left(-\left(1\right)\right)k\\  & =\left(-\left(-3\right)\right)i+\left(-4\right)j+\left(-\left(1\right)\right)k\\  & =⟨3,-4,-1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(- \frac{7}{2},3,-2)$ and passes through the point $(- \frac{7}{2},3,-2)$ can be written as

$$
\begin{aligned}r & =⟨- \frac{7}{2},3,-2⟩+t\,∇f(- \frac{7}{2},3,-2)=⟨- \frac{7}{2},3,-2⟩+t\,⟨3,-4,-1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-71407

Find a vector equation of the normal line to the surface $\left(z + 3\right)=2{\left(x - 3\right)}^{2}+2{\left(-\left(y + 2\right)\right)}^{2}+\left(x - 3\right)$ at the point $(\frac{7}{2},-3,0).$

Field 0 (:answer-field.type/radio)

- $r=⟨\frac{7}{2},-3,0⟩+t\,⟨-3,4,0⟩$
- $r=⟨\frac{7}{2},-3,0⟩+t\,⟨-3,0,1⟩$
- $r=⟨\frac{7}{2},-3,0⟩+t\,⟨0,4,1⟩$
- $r=⟨\frac{7}{2},-3,0⟩+t\,⟨-3,4,1⟩$ **keyed**
- $r=⟨\frac{9}{2},-3,0⟩+t\,⟨-3,4,1⟩$

First, we bring all variables to one side:

$$
\begin{aligned}\left(z + 3\right) & =2{\left(x - 3\right)}^{2}+2{\left(-\left(y + 2\right)\right)}^{2}+\left(x - 3\right) \\ \left(z + 3\right)-2{\left(x - 3\right)}^{2}-2{\left(-\left(y + 2\right)\right)}^{2}-\left(x - 3\right) & =0\end{aligned}
$$

If we set $f(x,y,z)=\left(z + 3\right)-2{\left(x - 3\right)}^{2}-2{\left(-\left(y + 2\right)\right)}^{2}-\left(x - 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(\frac{7}{2},-3,0)$ can be found by computing $∇f(\frac{7}{2},-3,0).$ 

So, we find the gradient and evaluate it at $(\frac{7}{2},-3,0):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(\left(z + 3\right)-2{\left(x - 3\right)}^{2}-2{\left(-\left(y + 2\right)\right)}^{2}-\left(x - 3\right))i+\frac{∂}{∂y}(\left(z + 3\right)-2{\left(x - 3\right)}^{2}-2{\left(-\left(y + 2\right)\right)}^{2}-\left(x - 3\right))j+\frac{∂}{∂z}(\left(z + 3\right)-2{\left(x - 3\right)}^{2}-2{\left(-\left(y + 2\right)\right)}^{2}-\left(x - 3\right))k \\  & =\left((-4\left(x - 3\right)-1)\right)i+\left(-\left(-4\left(-\left(y + 2\right)\right)\right)\right)j+\left(1\right)k\\∇f(\frac{7}{2},-3,0)& =\left((-4\left(\left(\frac{7}{2}\right) - 3\right)-1)\right)i+\left(-\left(-4\left(-\left(\left(-3\right) + 2\right)\right)\right)\right)j+\left(1\right)k\\  & =\left((-4(\frac{1}{2})-1)\right)i+\left(-\left(-4(1)\right)\right)j+\left(1\right)k\\  & =\left(-3\right)i+\left(-\left(-4\right)\right)j+\left(1\right)k\\  & =⟨-3,4,1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(\frac{7}{2},-3,0)$ and passes through the point $(\frac{7}{2},-3,0)$ can be written as

$$
\begin{aligned}r & =⟨\frac{7}{2},-3,0⟩+t\,∇f(\frac{7}{2},-3,0)=⟨\frac{7}{2},-3,0⟩+t\,⟨-3,4,1⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36754

Find a vector equation of the normal line to the surface ${x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}=1$ at the point $(0,0,2),$ with parameter $t=0$ at this point.

Field 0 (:answer-field.type/radio)

- $⟨0,0,2⟩+t\,⟨0,1,0⟩,\,t\in (-\infty ,\infty )$
- $⟨0,0,2⟩+t\,⟨1,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨0,0,2⟩+t\,⟨0,0,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨0,0,2⟩+t\,⟨0,1,1⟩,\,t\in (-\infty ,\infty )$
- $⟨0,0,2⟩+t\,⟨1,0,1⟩,\,t\in (-\infty ,\infty )$

First, note that we can write the equation of our surface as

$$
\begin{aligned}{x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1=0\end{aligned}
$$

So, if we set $f(x,y,z)={x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1$, our surface can be viewed as the level surface $f(x,y,z)=0.$  

A normal vector to the level surface that passes through the point $(0,0,2)$ can be found by computing $∇f(0,0,2).$ 

So, we find the gradient and evaluate it at $(0,0,2):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)i+\frac{∂}{∂y}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)j+\frac{∂}{∂z}({x}^{2}+\frac{{y}^{2}}{9}+\frac{{z}^{2}}{4}-1)k \\  & =2x\text{ }i+\frac{2y}{9}\text{ }j+\frac{z}{2}\text{ }k \\ ∇f(0,0,2) & =2(0)\text{ }i+\frac{2(0)}{9}\text{ }j+\frac{(2)}{2}\text{ }k \\  & =k \\  & =⟨0,0,1⟩\end{aligned}
$$

 

Finally, the vector form of the equation of the line that is parallel to $∇f(0,0,2)$ and passes through the point $(0,0,2)$ can be written as

$$
\begin{aligned}r & =⟨0,\,0,\,2⟩+t\,∇f(0,0,2)=⟨0,\,0,\,2⟩+t\,⟨0,\,0,\,1⟩\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36754

Find a vector equation of the normal line to the surface ${\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}=1$ at the point $(-3,2,-1),$ with parameter $t=0$ at this point.

Field 0 (:answer-field.type/radio)

- $⟨-3,2,-1⟩+t\,⟨0,0,-1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨-3,2,-1⟩+t\,⟨-1,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨-3,2,-1⟩+t\,⟨-1,0,-1⟩,\,t\in (-\infty ,\infty )$
- $⟨-3,2,-1⟩+t\,⟨0,-1,0⟩,\,t\in (-\infty ,\infty )$
- $⟨-3,2,-1⟩+t\,⟨0,-1,-1⟩,\,t\in (-\infty ,\infty )$

First, note that we can write the equation of our surface as

$$
\begin{aligned}{\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}-1=0\end{aligned}
$$

So, if we set $f(x,y,z)={\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}-1$, our surface can be viewed as the level surface $f(x,y,z)=0.$  

A normal vector to the level surface that passes through the point $(-3,2,-1)$ can be found by computing $∇f(-3,2,-1).$ 

So, we find the gradient and evaluate it at $(-3,2,-1):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}-1)i+\frac{∂}{∂y}({\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}-1)j+\frac{∂}{∂z}({\left(-\left(x + 3\right)\right)}^{2}+\frac{{\left(y - 2\right)}^{2}}{9}+\frac{{\left(-\left(z - 1\right)\right)}^{2}}{4}-1)k \\  & =\left(-\left(2\left(-\left(x + 3\right)\right)\right)\right)i+\left(+\frac{2\left(y - 2\right)}{9}\right)j+\left(-\left(+\frac{\left(-\left(z - 1\right)\right)}{2}\right)\right)k\\∇f(-3,2,-1)& =\left(-\left(2\left(-\left(\left(-3\right) + 3\right)\right)\right)\right)i+\left(+\frac{2\left(\left(2\right) - 2\right)}{9}\right)j+\left(-\left(+\frac{\left(-\left(\left(-1\right) - 1\right)\right)}{2}\right)\right)k\\  & =\left(-\left(2(0)\right)\right)i+\left(+\frac{2(0)}{9}\right)j+\left(-\left(+\frac{(2)}{2}\right)\right)k\\  & =\left(-\left(0\right)\right)i+\left(0\right)j+\left(-\left(1\right)\right)k\\  & =⟨0,0,-1⟩\end{aligned}
$$

 

Finally, the vector form of the equation of the line that is parallel to $∇f(-3,2,-1)$ and passes through the point $(-3,2,-1)$ can be written as

$$
\begin{aligned}r & =⟨-3,2,-1⟩+t\,∇f(-3,2,-1)=⟨-3,2,-1⟩+t\,⟨0,\,0,-1⟩\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-36754

Find a vector equation of the normal line to the surface ${\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}=1$ at the point $(3,-2,-1),$ with parameter $t=0$ at this point.

Field 0 (:answer-field.type/radio)

- $⟨3,-2,-1⟩+t\,⟨1,0,1⟩,\,t\in (-\infty ,\infty )$
- $⟨3,-2,-1⟩+t\,⟨0,1,0⟩,\,t\in (-\infty ,\infty )$
- $⟨3,-2,-1⟩+t\,⟨1,0,0⟩,\,t\in (-\infty ,\infty )$
- $⟨3,-2,-1⟩+t\,⟨0,0,1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨3,-2,-1⟩+t\,⟨0,1,1⟩,\,t\in (-\infty ,\infty )$

First, note that we can write the equation of our surface as

$$
\begin{aligned}{\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}-1=0\end{aligned}
$$

So, if we set $f(x,y,z)={\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}-1$, our surface can be viewed as the level surface $f(x,y,z)=0.$  

A normal vector to the level surface that passes through the point $(3,-2,-1)$ can be found by computing $∇f(3,-2,-1).$ 

So, we find the gradient and evaluate it at $(3,-2,-1):$

$$
\begin{aligned}∇f(x,y,z) & =\frac{∂}{∂x}({\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}-1)i+\frac{∂}{∂y}({\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}-1)j+\frac{∂}{∂z}({\left(x - 3\right)}^{2}+\frac{{\left(-\left(y + 2\right)\right)}^{2}}{9}+\frac{{\left(z + 3\right)}^{2}}{4}-1)k \\  & =\left(2\left(x - 3\right)\right)i+\left(-\left(+\frac{2\left(-\left(y + 2\right)\right)}{9}\right)\right)j+\left(+\frac{\left(z + 3\right)}{2}\right)k\\∇f(3,-2,-1)& =\left(2\left(\left(3\right) - 3\right)\right)i+\left(-\left(+\frac{2\left(-\left(\left(-2\right) + 2\right)\right)}{9}\right)\right)j+\left(+\frac{\left(\left(-1\right) + 3\right)}{2}\right)k\\  & =\left(2(0)\right)i+\left(-\left(+\frac{2(0)}{9}\right)\right)j+\left(+\frac{(2)}{2}\right)k\\  & =\left(0\right)i+\left(-\left(0\right)\right)j+\left(1\right)k\\  & =⟨0,0,1⟩\end{aligned}
$$

 

Finally, the vector form of the equation of the line that is parallel to $∇f(3,-2,-1)$ and passes through the point $(3,-2,-1)$ can be written as

$$
\begin{aligned}r & =⟨3,-2,-1⟩+t\,∇f(3,-2,-1)=⟨3,-2,-1⟩+t\,⟨0,0,\,1⟩\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — easy_quadratic

Find a vector equation of the normal line to the level surface $\left(x - 1\right)^{2}+2\left(y + 2\right)^{2}-z=0$ at the point $(2,-1,3).$

Field 0 (:answer-field.type/radio)

- $r=⟨2,-1,3⟩+t\,⟨0,4,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,-1,3⟩+t\,⟨2,4,-1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨3,-1,3⟩+t\,⟨2,4,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,-1,3⟩+t\,⟨2,0,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨2,-1,3⟩+t\,⟨2,4,0⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)=\left(x - 1\right)^{2}+2\left(y + 2\right)^{2}-z.$ Then, our surface can be viewed as the level surface $f(x,y,z)=0.$

A normal vector to the level surface that passes through the point $(2,-1,3)$ can be found by computing $∇f(2,-1,3).$

So, we find the gradient and evaluate it at $(2,-1,3):$

$$
\begin{aligned}∇f(x,y,z)&={f}_{x}(x,y,z)i+{f}_{y}(x,y,z)j+{f}_{z}(x,y,z)k\\&=\frac{∂}{∂x}(\left(x - 1\right)^{2}+2\left(y + 2\right)^{2}-z)i+\frac{∂}{∂y}(\left(x - 1\right)^{2}+2\left(y + 2\right)^{2}-z)j+\frac{∂}{∂z}(\left(x - 1\right)^{2}+2\left(y + 2\right)^{2}-z)k\\&=\left(2 x - 2\right)i+\left(4 y + 8\right)j+\left(-1\right)k\\∇f(2,-1,3)&=\left(2\right)i+\left(4\right)j+\left(-1\right)k\\&=⟨2,4,-1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(2,-1,3)$ and passes through the point $(2,-1,3)$ can be written as

$$r=⟨2,-1,3⟩+t\,∇f(2,-1,3)=⟨2,-1,3⟩+t\,⟨2,4,-1⟩.$$

where $t\in (-\infty,\infty).$

## Generated normal variants — easy_quadratic

Find a vector equation of the normal line to the level surface $\left(-\left(x - 2\right)\right)^{2}+2\left(y + 2\right)^{2}-z=0$ at the point $(1,-1,3).$

Field 0 (:answer-field.type/radio)

- $r=⟨1,-1,3⟩+t\,⟨0,4,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨1,-1,3⟩+t\,⟨-2,0,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨1,-1,3⟩+t\,⟨-2,4,-1⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $r=⟨2,-1,3⟩+t\,⟨-2,4,-1⟩,\,t\in (-\infty ,\infty )$
- $r=⟨1,-1,3⟩+t\,⟨-2,4,0⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)=\left(-\left(x - 2\right)\right)^{2}+2\left(y + 2\right)^{2}-z.$ Then, our surface can be viewed as the level surface $f(x,y,z)=0.$

A normal vector to the level surface that passes through the point $(1,-1,3)$ can be found by computing $∇f(1,-1,3).$

So, we find the gradient and evaluate it at $(1,-1,3):$

$$
\begin{aligned}∇f(x,y,z)&={f}_{x}(x,y,z)i+{f}_{y}(x,y,z)j+{f}_{z}(x,y,z)k\\&=\frac{∂}{∂x}(\left(-\left(x - 2\right)\right)^{2}+2\left(y + 2\right)^{2}-z)i+\frac{∂}{∂y}(\left(-\left(x - 2\right)\right)^{2}+2\left(y + 2\right)^{2}-z)j+\frac{∂}{∂z}(\left(-\left(x - 2\right)\right)^{2}+2\left(y + 2\right)^{2}-z)k\\&=\left(2 x - 4\right)i+\left(4 y + 8\right)j+\left(-1\right)k\\∇f(1,-1,3)&=\left(-2\right)i+\left(4\right)j+\left(-1\right)k\\&=⟨-2,4,-1⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(1,-1,3)$ and passes through the point $(1,-1,3)$ can be written as

$$r=⟨1,-1,3⟩+t\,∇f(1,-1,3)=⟨1,-1,3⟩+t\,⟨-2,4,-1⟩.$$

where $t\in (-\infty,\infty).$

## Generated normal variants — q-131124

Find a vector equation of the normal line to the surface $4{\left(z + 3\right)}^{2}-4{y}^{2}={\left(x - 3\right)}^{2}-6\left(x - 3\right)+12$ at the point $(5,0,-2).$

Field 0 (:answer-field.type/radio)

- $⟨5,1,-2⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$
- $⟨5,0,-2⟩+t\,⟨2,0,8⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨5,0,-2⟩+t\,⟨0,0,8⟩,\,t\in (-\infty ,\infty )$
- $⟨5,0,-2⟩+t\,⟨2,2,8⟩,\,t\in (-\infty ,\infty )$
- $⟨5,0,-2⟩+t\,⟨2,0,0⟩,\,t\in (-\infty ,\infty )$

First, we bring all variables to one side:

$$
\begin{aligned}4{\left(z + 3\right)}^{2}-4{y}^{2} & ={\left(x - 3\right)}^{2}-6\left(x - 3\right) +12\\ 4{\left(z + 3\right)}^{2}-4{y}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right) & =12\end{aligned}
$$

If we set $f(x,y,z)=4{\left(z + 3\right)}^{2}-4{y}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right)$, our surface can be viewed as the level surface $f(x,y,z)=12.$ 

A normal vector to the level surface that passes through the point $(5,0,-2)$ can be found by computing $∇f(5,0,-2).$ 

So, we find the gradient and evaluate it at $(5,0,-2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}(4{\left(z + 3\right)}^{2}-4{y}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))i+\frac{∂}{∂y}(4{\left(z + 3\right)}^{2}-4{y}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))j+\frac{∂}{∂z}(4{\left(z + 3\right)}^{2}-4{y}^{2}-{\left(x - 3\right)}^{2}+6\left(x - 3\right))k \\  & =\left((6-2\left(x - 3\right))\right)i+\left(-8y\right)j+\left(+8\left(z + 3\right)\right)k\\∇f(5,0,-2)& =\left((6-2\left(\left(5\right) - 3\right))\right)i+\left(-8\left(0\right)\right)j+\left(+8\left(\left(-2\right) + 3\right)\right)k\\  & =(6-2(2))\,i-8(0)\text{ }j+8(1)\,k \\  & =2\,i+8\,k \\  & =⟨2,0,8⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(5,0,-2)$ and passes through the point $(5,0,-2)$ can be written as

$$
\begin{aligned}r & =⟨5,0,-2⟩+t\,∇f(5,0,-2)=⟨5,0,-2⟩+t\,⟨2,0,8⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131126

Find a vector equation of the normal line to the surface ${\left(-\left(x - 1\right)\right)}^{2}\left(y - 3\right)+{\left(y - 3\right)}^{2}\left(-\left(z - 3\right)\right)+{\left(-\left(z - 3\right)\right)}^{2}\left(-\left(x - 1\right)\right)=5$ at the point $(0,2,1).$

Field 0 (:answer-field.type/radio)

- $⟨0,2,1⟩+t\,⟨-2,-3,-5⟩,\,t\in (-\infty ,\infty )$ **keyed**
- $⟨0,2,1⟩+t\,⟨-2,0,-5⟩,\,t\in (-\infty ,\infty )$
- $⟨0,2,1⟩+t\,⟨0,-3,-5⟩,\,t\in (-\infty ,\infty )$
- $⟨1,2,1⟩+t\,⟨-2,-3,-5⟩,\,t\in (-\infty ,\infty )$
- $⟨0,2,1⟩+t\,⟨-2,-3,0⟩,\,t\in (-\infty ,\infty )$

Let's set $f(x,y,z)={\left(-\left(x - 1\right)\right)}^{2}\left(y - 3\right)+{\left(y - 3\right)}^{2}\left(-\left(z - 3\right)\right)+{\left(-\left(z - 3\right)\right)}^{2}\left(-\left(x - 1\right)\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=5.$ 

A normal vector to the level surface that passes through the point $(0,2,1)$ can be found by computing $∇f(0,2,1).$ 

So, we find the gradient and evaluate it at $(0,2,1):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(-\left(x - 1\right)\right)}^{2}\left(y - 3\right)+{\left(y - 3\right)}^{2}\left(-\left(z - 3\right)\right)+{\left(-\left(z - 3\right)\right)}^{2}\left(-\left(x - 1\right)\right))i+\frac{∂}{∂y}({\left(-\left(x - 1\right)\right)}^{2}\left(y - 3\right)+{\left(y - 3\right)}^{2}\left(-\left(z - 3\right)\right)+{\left(-\left(z - 3\right)\right)}^{2}\left(-\left(x - 1\right)\right))j+\frac{∂}{∂z}({\left(-\left(x - 1\right)\right)}^{2}\left(y - 3\right)+{\left(y - 3\right)}^{2}\left(-\left(z - 3\right)\right)+{\left(-\left(z - 3\right)\right)}^{2}\left(-\left(x - 1\right)\right))k \\  & =\left(-\left((2\left(-\left(x - 1\right)\right)\left(y - 3\right)+{\left(-\left(z - 3\right)\right)}^{2})\right)\right)i+\left(+({\left(-\left(x - 1\right)\right)}^{2}+2\left(y - 3\right)\left(-\left(z - 3\right)\right))\right)j+\left(-\left(+({\left(y - 3\right)}^{2}+2\left(-\left(z - 3\right)\right)\left(-\left(x - 1\right)\right))\right)\right)k\\∇f(0,2,1)& =\left(-\left((2\left(-\left(\left(0\right) - 1\right)\right)\left(\left(2\right) - 3\right)+{\left(-\left(\left(1\right) - 3\right)\right)}^{2})\right)\right)i+\left(+({\left(-\left(\left(0\right) - 1\right)\right)}^{2}+2\left(\left(2\right) - 3\right)\left(-\left(\left(1\right) - 3\right)\right))\right)j+\left(-\left(+({\left(\left(2\right) - 3\right)}^{2}+2\left(-\left(\left(1\right) - 3\right)\right)\left(-\left(\left(0\right) - 1\right)\right))\right)\right)k\\  & =\left(-\left((2(1)(-1)+(2)^{2})\right)\right)i+\left(+((1)^{2}+2(-1)(2))\right)j+\left(-\left(+((-1)^{2}+2(2)(1))\right)\right)k\\  & =\left(-\left(2\right)\right)i+\left(-3\right)j+\left(-\left(+5\right)\right)k\\  & =⟨-2,-3,-5⟩\end{aligned}
$$

Finally, the vector equation of the line that is parallel to $∇f(0,2,1)$ and passes through the point $(0,2,1)$ can be written as

$$
\begin{aligned}r & =⟨0,2,1⟩+t\,∇f(0,2,1)=⟨0,2,1⟩+t\,⟨-2,-3,-5⟩,\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

## Generated normal variants — q-131129

Find the equation of the normal line to the surface ${e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y\left(z + 3\right)=-3$ at the point $(5,-1,-4).$

Field 0 (:answer-field.type/radio)

- $\frac{x - 6}{-1}=\frac{y + 1}{5}=\frac{z + 4}{5}$
- $\frac{x - 5}{-1}=\frac{y + 1}{5}=\frac{z + 4}{5}$ **keyed**
- $\frac{x - 5}{-2}=\frac{y + 1}{5}=\frac{z + 4}{5}$
- $\frac{x - 5}{-1}=\frac{y + 1}{5}=\frac{z + 4}{10}$
- $\frac{x - 5}{-1}=\frac{y + 1}{10}=\frac{z + 4}{5}$

Let's set $f(x,y,z)={e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y\left(z + 3\right).$ Then, our surface can be viewed as the level surface $f(x,y,z)=-3.$ 

A normal vector to the level surface that passes through the point $(5,-1,-4)$ can be found by computing $∇f(5,-1,-4).$ 

So, we find the gradient and evaluate it at $(5,-1,-4):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y\left(z + 3\right))i+\frac{∂}{∂y}({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y\left(z + 3\right))j+\frac{∂}{∂z}({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y\left(z + 3\right))k \\  & =\left(({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2y\left(z + 3\right))\right)i+\left(+({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)\left(z + 3\right))\right)j+\left(+({e}^{\left(x - 3\right)+y+\left(z + 3\right)}-2\left(x - 3\right)y)\right)k\\∇f(5,-1,-4)& =\left(({e}^{\left(\left(5\right) - 3\right)+\left(-1\right)+\left(\left(-4\right) + 3\right)}-2\left(-1\right)\left(\left(-4\right) + 3\right))\right)i+\left(+({e}^{\left(\left(5\right) - 3\right)+\left(-1\right)+\left(\left(-4\right) + 3\right)}-2\left(\left(5\right) - 3\right)\left(\left(-4\right) + 3\right))\right)j+\left(+({e}^{\left(\left(5\right) - 3\right)+\left(-1\right)+\left(\left(-4\right) + 3\right)}-2\left(\left(5\right) - 3\right)\left(-1\right))\right)k\\  & =({e}^{2-1-1}-2(-1)(-1))\text{ }i+({e}^{2-1-1}-2(2)(-1))\text{ }j+({e}^{2-1-1}-2(2)(-1))\text{ }k \\  & =({e}^{0}-2)\text{ }i+({e}^{0}+4)\text{ }j+({e}^{0}+4)\text{ }k \\  & =-i+5\,j+5\,k \\  & =⟨-1,5,5⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(x - 3\right)-2}{(-1)}=\frac{y-(-1)}{5}=\frac{\left(z + 3\right)-(-1)}{5} \\ \frac{\left(x - 3\right)-2}{(-1)}=\frac{y+1}{5}=\frac{\left(z + 3\right)+1}{5} \\ 2-\left(x - 3\right)=\frac{y+1}{5}=\frac{\left(z + 3\right)+1}{5}\end{aligned}
$$

## Generated normal variants — q-131130

Find the equation of the normal line to the surface $\left(-\left(x - 1\right)\right)={\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}$ at the point $(-2,5,2).$

Field 0 (:answer-field.type/radio)

- $\frac{x + 2}{1}=\frac{y - 5}{4}=\frac{z - 2}{2}$ **keyed**
- $\frac{x + 2}{1}=\frac{y - 5}{8}=\frac{z - 2}{2}$
- $\frac{x + 2}{2}=\frac{y - 5}{4}=\frac{z - 2}{2}$
- $\frac{x + 1}{1}=\frac{y - 5}{4}=\frac{z - 2}{2}$
- $\frac{x + 2}{1}=\frac{y - 5}{4}=\frac{z - 2}{4}$

First, we bring all variables to one side:

$$
\begin{aligned}\left(-\left(x - 1\right)\right) & ={\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2} \\ {\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}-\left(-\left(x - 1\right)\right) & =0\end{aligned}
$$

If we set $f(x,y,z)={\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}-\left(-\left(x - 1\right)\right)$, our surface can be viewed as the level surface $f(x,y,z)=0.$ 

A normal vector to the level surface that passes through the point $(-2,5,2)$ can be found by computing $∇f(-2,5,2).$ 

So, we find the gradient and evaluate it at $(-2,5,2):$

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{∂}{∂x}({\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}-\left(-\left(x - 1\right)\right))i+\frac{∂}{∂y}({\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}-\left(-\left(x - 1\right)\right))j+\frac{∂}{∂z}({\left(y - 3\right)}^{2}-{\left(-\left(z - 3\right)\right)}^{2}-\left(-\left(x - 1\right)\right))k \\  & =\left(-\left(-1\right)\right)i+\left(+2\left(y - 3\right)\right)j+\left(-\left(-2\left(-\left(z - 3\right)\right)\right)\right)k\\∇f(-2,5,2)& =\left(-\left(-1\right)\right)i+\left(+2\left(\left(5\right) - 3\right)\right)j+\left(-\left(-2\left(-\left(\left(2\right) - 3\right)\right)\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(+2(2)\right)j+\left(-\left(-2(1)\right)\right)k\\  & =\left(-\left(-1\right)\right)i+\left(+4\right)j+\left(-\left(-2\right)\right)k\\  & =⟨1,4,2⟩\end{aligned}
$$

Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$ and passes through the point $({x}_{0},{y}_{0},{z}_{0})$ can be written as:

$$
\begin{aligned}\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}} \\ \frac{\left(-\left(x - 1\right)\right)-3}{(-1)}=\frac{\left(y - 3\right)-2}{4}=\frac{\left(-\left(z - 3\right)\right)-1}{(-2)} \\ \frac{\left(-\left(x - 1\right)\right)-3}{1}=\frac{\left(y - 3\right)-2}{-4}=\frac{\left(-\left(z - 3\right)\right)-1}{2} \\ \left(-\left(x - 1\right)\right)-3=\frac{2-\left(y - 3\right)}{4}=\frac{\left(-\left(z - 3\right)\right)-1}{2}\end{aligned}
$$

