If $f(x,y)=x e^{x y},$ $x=3 t^{4}$ and $y=t^{3},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- 27 t^{10} e^{3 t^{7}} + 12 t^{3} (3 t^{7} e^{3 t^{7}} + e^{3 t^{7}})$
- $27 t^{10} e^{3 t^{7}}$
- $12 t^{3} (3 t^{7} e^{3 t^{7}} + e^{3 t^{7}})$
- $3 t^{3} (21 t^{7} + 4) e^{3 t^{7}}$
- $- 3 t^{3} (21 t^{7} + 4) e^{3 t^{7}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =3 t^{7} e^{3 t^{7}} + e^{3 t^{7}} \\ \frac{∂f}{∂y} & =9 t^{8} e^{3 t^{7}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=12 t^{3},\,\frac{\text{d}y}{\text{d}t}=3 t^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =(3 t^{7} e^{3 t^{7}} + e^{3 t^{7}})\cdot (12 t^{3})+(9 t^{8} e^{3 t^{7}})\cdot (3 t^{2}) \\  & =12 t^{3} e^{3 t^{7}} + (36 t^{10} e^{3 t^{7}}) + (27 t^{10} e^{3 t^{7}}) \\  & =3 t^{3} (21 t^{7} + 4) e^{3 t^{7}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=t^{3}$ and $y=t^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- 2 t^{7} e^{t^{5}} + 3 t^{2} (t^{5} e^{t^{5}} + e^{t^{5}})$
- $- t^{2} (5 t^{5} + 3) e^{t^{5}}$
- $t^{2} (5 t^{5} + 3) e^{t^{5}}$
- $3 t^{2} (t^{5} e^{t^{5}} + e^{t^{5}})$
- $2 t^{7} e^{t^{5}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =t^{5} e^{t^{5}} + e^{t^{5}} \\ \frac{∂f}{∂y} & =t^{6} e^{t^{5}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=3 t^{2},\,\frac{\text{d}y}{\text{d}t}=2 t.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =(t^{5} e^{t^{5}} + e^{t^{5}})\cdot (3 t^{2})+(t^{6} e^{t^{5}})\cdot (2 t) \\  & =3 t^{2} e^{t^{5}} + (3 t^{7} e^{t^{5}}) + (2 t^{7} e^{t^{5}}) \\  & =t^{2} (5 t^{5} + 3) e^{t^{5}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=2 t^{2}$ and $y=t^{3},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $4 t (2 t^{5} e^{2 t^{5}} + e^{2 t^{5}})$
- $4 t (5 t^{5} + 1) e^{2 t^{5}}$
- $- 12 t^{6} e^{2 t^{5}} + 4 t (2 t^{5} e^{2 t^{5}} + e^{2 t^{5}})$
- $12 t^{6} e^{2 t^{5}}$
- $- 4 t (5 t^{5} + 1) e^{2 t^{5}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2 t^{5} e^{2 t^{5}} + e^{2 t^{5}} \\ \frac{∂f}{∂y} & =4 t^{4} e^{2 t^{5}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=4 t,\,\frac{\text{d}y}{\text{d}t}=3 t^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =(2 t^{5} e^{2 t^{5}} + e^{2 t^{5}})\cdot (4 t)+(4 t^{4} e^{2 t^{5}})\cdot (3 t^{2}) \\  & =4 t e^{2 t^{5}} + (8 t^{6} e^{2 t^{5}}) + (12 t^{6} e^{2 t^{5}}) \\  & =4 t (5 t^{5} + 1) e^{2 t^{5}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=4 t^{2}$ and $y=t^{4},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- 8 t (12 t^{6} + 1) e^{4 t^{6}}$
- $8 t (4 t^{6} e^{4 t^{6}} + e^{4 t^{6}})$
- $64 t^{7} e^{4 t^{6}}$
- $8 t (12 t^{6} + 1) e^{4 t^{6}}$
- $- 64 t^{7} e^{4 t^{6}} + 8 t (4 t^{6} e^{4 t^{6}} + e^{4 t^{6}})$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =4 t^{6} e^{4 t^{6}} + e^{4 t^{6}} \\ \frac{∂f}{∂y} & =16 t^{4} e^{4 t^{6}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=8 t,\,\frac{\text{d}y}{\text{d}t}=4 t^{3}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =(4 t^{6} e^{4 t^{6}} + e^{4 t^{6}})\cdot (8 t)+(16 t^{4} e^{4 t^{6}})\cdot (4 t^{3}) \\  & =8 t e^{4 t^{6}} + (32 t^{7} e^{4 t^{6}}) + (64 t^{7} e^{4 t^{6}}) \\  & =8 t (12 t^{6} + 1) e^{4 t^{6}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=t^{2}$ and $y=t^{3},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $2 t (t^{5} e^{t^{5}} + e^{t^{5}})$
- $- 3 t^{6} e^{t^{5}} + 2 t (t^{5} e^{t^{5}} + e^{t^{5}})$
- $- t (5 t^{5} + 2) e^{t^{5}}$
- $t (5 t^{5} + 2) e^{t^{5}}$
- $3 t^{6} e^{t^{5}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =t^{5} e^{t^{5}} + e^{t^{5}} \\ \frac{∂f}{∂y} & =t^{4} e^{t^{5}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=2 t,\,\frac{\text{d}y}{\text{d}t}=3 t^{2}.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =(t^{5} e^{t^{5}} + e^{t^{5}})\cdot (2 t)+(t^{4} e^{t^{5}})\cdot (3 t^{2}) \\  & =2 t e^{t^{5}} + (2 t^{6} e^{t^{5}}) + (3 t^{6} e^{t^{5}}) \\  & =t (5 t^{5} + 2) e^{t^{5}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=(2 t - 1)^{3}$ and $y=(2 t - 2)^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- (2 t - 1)^{6} (8 t - 8) e^{(2 t - 2)^{2} (2 t - 1)^{3}} + 6 (2 t - 1)^{2} ((2 t - 2)^{2} (2 t - 1)^{3} e^{(2 t - 2)^{2} (2 t - 1)^{3}} + e^{(2 t - 2)^{2} (2 t - 1)^{3}})$
- $(2 t - 1)^{6} (8 t - 8) e^{(2 t - 2)^{2} (2 t - 1)^{3}}$
- $6 (2 t - 1)^{2} ((2 t - 2)^{2} (2 t - 1)^{3} e^{(2 t - 2)^{2} (2 t - 1)^{3}} + e^{(2 t - 2)^{2} (2 t - 1)^{3}})$
- $2 (2 t - 1)^{2} (12 (t - 1)^{2} (2 t - 1)^{3} + 4 (t - 1) (2 t - 1)^{4} + 3) e^{(2 t - 2)^{2} (2 t - 1)^{3}}$
- $- 2 (2 t - 1)^{2} (12 (t - 1)^{2} (2 t - 1)^{3} + 4 (t - 1) (2 t - 1)^{4} + 3) e^{(2 t - 2)^{2} (2 t - 1)^{3}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =(2 t - 2)^{2} (2 t - 1)^{3} e^{(2 t - 2)^{2} (2 t - 1)^{3}} + e^{(2 t - 2)^{2} (2 t - 1)^{3}} \\ \frac{∂f}{∂y} & =(2 t - 1)^{6} e^{(2 t - 2)^{2} (2 t - 1)^{3}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=6 (2 t - 1)^{2},\,\frac{\text{d}y}{\text{d}t}=8 t - 8.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =((2 t - 2)^{2} (2 t - 1)^{3} e^{(2 t - 2)^{2} (2 t - 1)^{3}} + e^{(2 t - 2)^{2} (2 t - 1)^{3}})\cdot (6 (2 t - 1)^{2})+((2 t - 1)^{6} e^{(2 t - 2)^{2} (2 t - 1)^{3}})\cdot (8 t - 8) \\  & =6 (2 t - 1)^{2} e^{(2 t - 2)^{2} (2 t - 1)^{3}} + (6 (2 t - 2)^{2} (2 t - 1)^{5} e^{(2 t - 2)^{2} (2 t - 1)^{3}}) + ((2 t - 1)^{6} (8 t - 8) e^{(2 t - 2)^{2} (2 t - 1)^{3}}) \\  & =2 (2 t - 1)^{2} (12 (t - 1)^{2} (2 t - 1)^{3} + 4 (t - 1) (2 t - 1)^{4} + 3) e^{(2 t - 2)^{2} (2 t - 1)^{3}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=(t - 3)^{2}$ and $y=(t - 1)^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- (t - 3)^{4} (2 t - 2) e^{(t - 3)^{2} (t - 1)^{2}} + (2 t - 6) ((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})$
- $- 2 (t - 3) ((t - 3)^{3} (t - 1) + (t - 3)^{2} (t - 1)^{2} + 1) e^{(t - 3)^{2} (t - 1)^{2}}$
- $2 (t - 3) ((t - 3)^{3} (t - 1) + (t - 3)^{2} (t - 1)^{2} + 1) e^{(t - 3)^{2} (t - 1)^{2}}$
- $(2 t - 6) ((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})$
- $(t - 3)^{4} (2 t - 2) e^{(t - 3)^{2} (t - 1)^{2}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =(t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}} \\ \frac{∂f}{∂y} & =(t - 3)^{4} e^{(t - 3)^{2} (t - 1)^{2}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=2 t - 6,\,\frac{\text{d}y}{\text{d}t}=2 t - 2.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})\cdot (2 t - 6)+((t - 3)^{4} e^{(t - 3)^{2} (t - 1)^{2}})\cdot (2 t - 2) \\  & =(2 t - 6) e^{(t - 3)^{2} (t - 1)^{2}} + ((t - 3)^{2} (t - 1)^{2} (2 t - 6) e^{(t - 3)^{2} (t - 1)^{2}}) + ((t - 3)^{4} (2 t - 2) e^{(t - 3)^{2} (t - 1)^{2}}) \\  & =2 (t - 3) ((t - 3)^{3} (t - 1) + (t - 3)^{2} (t - 1)^{2} + 1) e^{(t - 3)^{2} (t - 1)^{2}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=(t - 1)^{2}$ and $y=(t - 3)^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $(2 t - 2) ((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})$
- $2 (t - 1) ((t - 3)^{2} (t - 1)^{2} + (t - 3) (t - 1)^{3} + 1) e^{(t - 3)^{2} (t - 1)^{2}}$
- $- (t - 1)^{4} (2 t - 6) e^{(t - 3)^{2} (t - 1)^{2}} + (2 t - 2) ((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})$
- $(t - 1)^{4} (2 t - 6) e^{(t - 3)^{2} (t - 1)^{2}}$
- $- 2 (t - 1) ((t - 3)^{2} (t - 1)^{2} + (t - 3) (t - 1)^{3} + 1) e^{(t - 3)^{2} (t - 1)^{2}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =(t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}} \\ \frac{∂f}{∂y} & =(t - 1)^{4} e^{(t - 3)^{2} (t - 1)^{2}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=2 t - 2,\,\frac{\text{d}y}{\text{d}t}=2 t - 6.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =((t - 3)^{2} (t - 1)^{2} e^{(t - 3)^{2} (t - 1)^{2}} + e^{(t - 3)^{2} (t - 1)^{2}})\cdot (2 t - 2)+((t - 1)^{4} e^{(t - 3)^{2} (t - 1)^{2}})\cdot (2 t - 6) \\  & =(2 t - 2) e^{(t - 3)^{2} (t - 1)^{2}} + ((t - 3)^{2} (t - 1)^{2} (2 t - 2) e^{(t - 3)^{2} (t - 1)^{2}}) + ((t - 1)^{4} (2 t - 6) e^{(t - 3)^{2} (t - 1)^{2}}) \\  & =2 (t - 1) ((t - 3)^{2} (t - 1)^{2} + (t - 3) (t - 1)^{3} + 1) e^{(t - 3)^{2} (t - 1)^{2}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=(3 t + 2)^{2}$ and $y=(3 t + 2)^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $- 6 (3 t + 2) (2 (3 t + 2)^{4} + 1) e^{(3 t + 2)^{4}}$
- $(18 t + 12) ((3 t + 2)^{4} e^{(3 t + 2)^{4}} + e^{(3 t + 2)^{4}})$
- $(3 t + 2)^{4} (18 t + 12) e^{(3 t + 2)^{4}}$
- $6 (3 t + 2) (2 (3 t + 2)^{4} + 1) e^{(3 t + 2)^{4}}$
- $- (3 t + 2)^{4} (18 t + 12) e^{(3 t + 2)^{4}} + (18 t + 12) ((3 t + 2)^{4} e^{(3 t + 2)^{4}} + e^{(3 t + 2)^{4}})$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =(3 t + 2)^{4} e^{(3 t + 2)^{4}} + e^{(3 t + 2)^{4}} \\ \frac{∂f}{∂y} & =(3 t + 2)^{4} e^{(3 t + 2)^{4}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=18 t + 12,\,\frac{\text{d}y}{\text{d}t}=18 t + 12.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =((3 t + 2)^{4} e^{(3 t + 2)^{4}} + e^{(3 t + 2)^{4}})\cdot (18 t + 12)+((3 t + 2)^{4} e^{(3 t + 2)^{4}})\cdot (18 t + 12) \\  & =(18 t + 12) e^{(3 t + 2)^{4}} + ((3 t + 2)^{4} (18 t + 12) e^{(3 t + 2)^{4}}) + ((3 t + 2)^{4} (18 t + 12) e^{(3 t + 2)^{4}}) \\  & =6 (3 t + 2) (2 (3 t + 2)^{4} + 1) e^{(3 t + 2)^{4}}.\end{aligned}
$$

---

If $f(x,y)=x e^{x y},$ $x=(3 t + 2)^{2}$ and $y=(3 t - 2)^{2},$ compute $\frac{\text{d}f}{\text{d}t}$.

- $(18 t + 12) ((3 t - 2)^{2} (3 t + 2)^{2} e^{(3 t - 2)^{2} (3 t + 2)^{2}} + e^{(3 t - 2)^{2} (3 t + 2)^{2}})$
- $- (3 t + 2)^{4} (18 t - 12) e^{(3 t - 2)^{2} (3 t + 2)^{2}} + (18 t + 12) ((3 t - 2)^{2} (3 t + 2)^{2} e^{(3 t - 2)^{2} (3 t + 2)^{2}} + e^{(3 t - 2)^{2} (3 t + 2)^{2}})$
- $- 6 (3 t + 2) ((3 t - 2)^{2} (3 t + 2)^{2} + (3 t - 2) (3 t + 2)^{3} + 1) e^{(3 t - 2)^{2} (3 t + 2)^{2}}$
- $6 (3 t + 2) ((3 t - 2)^{2} (3 t + 2)^{2} + (3 t - 2) (3 t + 2)^{3} + 1) e^{(3 t - 2)^{2} (3 t + 2)^{2}}$
- $(3 t + 2)^{4} (18 t - 12) e^{(3 t - 2)^{2} (3 t + 2)^{2}}$

![](images/f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3.png)

The chain rule for a multivariable function $f(x,y)$ with one independent variable $t,$ where $x=x(t)$ and $y=y(t),$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x} &=x y e^{x y} + e^{x y},\,\frac{∂f}{∂y}=x^{2} e^{x y}\end{aligned}
$$

Writing the above results in terms of $t,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =(3 t - 2)^{2} (3 t + 2)^{2} e^{(3 t - 2)^{2} (3 t + 2)^{2}} + e^{(3 t - 2)^{2} (3 t + 2)^{2}} \\ \frac{∂f}{∂y} & =(3 t + 2)^{4} e^{(3 t - 2)^{2} (3 t + 2)^{2}}\end{aligned}
$$

Next, we take the derivatives of $x$ and $y$ with respect to $t,$ and we get

$$
\begin{aligned}\frac{\text{d}x}{\text{d}t} &=18 t + 12,\,\frac{\text{d}y}{\text{d}t}=18 t - 12.\end{aligned}
$$

Finally, substituting all of our derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =((3 t - 2)^{2} (3 t + 2)^{2} e^{(3 t - 2)^{2} (3 t + 2)^{2}} + e^{(3 t - 2)^{2} (3 t + 2)^{2}})\cdot (18 t + 12)+((3 t + 2)^{4} e^{(3 t - 2)^{2} (3 t + 2)^{2}})\cdot (18 t - 12) \\  & =(18 t + 12) e^{(3 t - 2)^{2} (3 t + 2)^{2}} + ((3 t - 2)^{2} (3 t + 2)^{2} (18 t + 12) e^{(3 t - 2)^{2} (3 t + 2)^{2}}) + ((3 t + 2)^{4} (18 t - 12) e^{(3 t - 2)^{2} (3 t + 2)^{2}}) \\  & =6 (3 t + 2) ((3 t - 2)^{2} (3 t + 2)^{2} + (3 t - 2) (3 t + 2)^{3} + 1) e^{(3 t - 2)^{2} (3 t + 2)^{2}}.\end{aligned}
$$