Given that $f(x,y)=- 2 x^{2} + 3 x y + 4 y^{2},$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- 8 r \sin^{2}{\left(\theta \right)} - 6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}$

B. $\frac{8 r \sin^{2}{\left(\theta \right)} + 6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}}{r}$

C. $8 r \sin^{2}{\left(\theta \right)} + 3 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

D. $8 r \sin^{2}{\left(\theta \right)} + 6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}$

E. $3 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂f}{∂r} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂r} \\  & =(\frac{∂f}{∂x})(\cos{\left(\theta \right)})+(\frac{∂f}{∂y})(\sin{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=- 4 x + 3 y,\,\frac{∂f}{∂y}=3 x + 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =3 r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)}, \\ \frac{∂f}{∂y} & =8 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂r} & =(3 r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)})(\cos{\left(\theta \right)})+(8 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)})(\sin{\left(\theta \right)}) \\  & =(3 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)})+(8 r \sin^{2}{\left(\theta \right)} + 3 r \sin{\left(\theta \right)} \cos{\left(\theta \right)}) \\  & =8 r \sin^{2}{\left(\theta \right)} + 6 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}\end{aligned}
$$

---

Given that $g(x,y)=- x^{2} - x y + 2 y^{2},$ find $\frac{∂g}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r \cos^{2}{\left(\theta \right)}$

B. $\frac{4 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r \cos^{2}{\left(\theta \right)}}{r}$

C. $4 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r \cos^{2}{\left(\theta \right)}$

D. $4 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $- 4 r \sin^{2}{\left(\theta \right)} + 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂r} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂r} \\  & =(\frac{∂g}{∂x})(\cos{\left(\theta \right)})+(\frac{∂g}{∂y})(\sin{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=- 2 x - y,\,\frac{∂g}{∂y}=- x + 4 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =- r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =4 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂r} & =(- r \sin{\left(\theta \right)} - 2 r \cos{\left(\theta \right)})(\cos{\left(\theta \right)})+(4 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)})(\sin{\left(\theta \right)}) \\  & =(- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r \cos^{2}{\left(\theta \right)})+(4 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}) \\  & =4 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r \cos^{2}{\left(\theta \right)}\end{aligned}
$$

---

Given that $w(x,y)=4 x^{2} - x y - 3 y^{2},$ find $\frac{∂w}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $r^{2} \sin^{2}{\left(\theta \right)} - 8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

B. $- 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}$

C. $r^{2} \sin^{2}{\left(\theta \right)} - 14 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}$

D. $- r^{2} \sin^{2}{\left(\theta \right)} + 14 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)}$

E. $\frac{r^{2} \sin^{2}{\left(\theta \right)} - 14 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}}{r}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂w}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂w}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=8 x - y,\,\frac{∂w}{∂y}=- x - 6 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =- r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}, \\ \frac{∂w}{∂y} & =- 6 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =(- r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(- 6 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(r^{2} \sin^{2}{\left(\theta \right)} - 8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})+(- 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}) \\  & =r^{2} \sin^{2}{\left(\theta \right)} - 14 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}\end{aligned}
$$

---

Given that $w(x,y)=- 2 x^{2} - x y - 4 y^{2},$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- 8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}$

B. $- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}$

C. $\frac{- 8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}}{r}$

D. $- 8 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

E. $8 r \sin^{2}{\left(\theta \right)} + 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂w}{∂r} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂r}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂r} \\  & =(\frac{∂w}{∂x})(\cos{\left(\theta \right)})+(\frac{∂w}{∂y})(\sin{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=- 4 x - y,\,\frac{∂w}{∂y}=- x - 8 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =- r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)}, \\ \frac{∂w}{∂y} & =- 8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂r} & =(- r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)})(\cos{\left(\theta \right)})+(- 8 r \sin{\left(\theta \right)} - r \cos{\left(\theta \right)})(\sin{\left(\theta \right)}) \\  & =(- r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)})+(- 8 r \sin^{2}{\left(\theta \right)} - r \sin{\left(\theta \right)} \cos{\left(\theta \right)}) \\  & =- 8 r \sin^{2}{\left(\theta \right)} - 2 r \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 r \cos^{2}{\left(\theta \right)}\end{aligned}
$$

---

Given that $g(x,y)=4 x^{2} + 3 x y + y^{2},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- 3 r^{2} \sin^{2}{\left(\theta \right)} - 8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}$

B. $3 r^{2} \sin^{2}{\left(\theta \right)} + 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 3 r^{2} \cos^{2}{\left(\theta \right)}$

C. $2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}$

D. $\frac{- 3 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}}{r}$

E. $- 3 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=8 x + 3 y,\,\frac{∂g}{∂y}=3 x + 2 y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =3 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =2 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(3 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(2 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(- 3 r^{2} \sin^{2}{\left(\theta \right)} - 8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})+(2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}) \\  & =- 3 r^{2} \sin^{2}{\left(\theta \right)} - 6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 r^{2} \cos^{2}{\left(\theta \right)}\end{aligned}
$$

---

Given that $f(x,y)=- 2 x^{2} y + 3 x y^{2},$ find $\frac{∂f}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $3 r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}$

B. $\frac{- 3 r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}}{r}$

C. $- 3 r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}$

D. $6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}$

E. $- 3 r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $f(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂f}{∂\theta} & =\frac{∂f}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂f}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂f}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂f}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂f}{∂x}=- 4 x y + 3 y^{2},\,\frac{∂f}{∂y}=- 2 x^{2} + 6 x y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}, \\ \frac{∂f}{∂y} & =6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂f}{∂\theta} & =(3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(- 3 r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)})+(6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}) \\  & =- 3 r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 6 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}\end{aligned}
$$

---

Given that $g(x,y)=- x^{2} y - x y^{2},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $r^{3} \sin^{3}{\left(\theta \right)} + 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}$

B. $- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - r^{3} \cos^{3}{\left(\theta \right)}$

C. $r^{3} \sin^{3}{\left(\theta \right)} + 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - r^{3} \cos^{3}{\left(\theta \right)}$

D. $- r^{3} \sin^{3}{\left(\theta \right)} - 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + r^{3} \cos^{3}{\left(\theta \right)}$

E. $\frac{r^{3} \sin^{3}{\left(\theta \right)} + 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - r^{3} \cos^{3}{\left(\theta \right)}}{r}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=- 2 x y - y^{2},\,\frac{∂g}{∂y}=- x^{2} - 2 x y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =- r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}, \\ \frac{∂g}{∂y} & =- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(- r^{2} \sin^{2}{\left(\theta \right)} - 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - r^{2} \cos^{2}{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(r^{3} \sin^{3}{\left(\theta \right)} + 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)})+(- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - r^{3} \cos^{3}{\left(\theta \right)}) \\  & =r^{3} \sin^{3}{\left(\theta \right)} + 2 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - r^{3} \cos^{3}{\left(\theta \right)}\end{aligned}
$$

---

Given that $h(x,y)=\ln{\left(4 x^{2} - 4 x y + 3 y^{2} \right)},$ find $\frac{∂h}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $\frac{4 r^{2} \sin^{2}{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}$

B. $\frac{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 \cos^{2}{\left(\theta \right)}}{r \left(3 \sin^{2}{\left(\theta \right)} - 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}\right)}$

C. $\frac{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 \cos^{2}{\left(\theta \right)}}{3 \sin^{2}{\left(\theta \right)} - 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}$

D. $\frac{6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{4 r^{2} \cos^{2}{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}$

E. $- \frac{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 \cos^{2}{\left(\theta \right)}}{3 \sin^{2}{\left(\theta \right)} - 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}$

Worked solution:

Applying the multivariable chain rule for the function $h(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂h}{∂\theta} & =\frac{∂h}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂h}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂h}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂h}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $h$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂h}{∂x}=\frac{8 x - 4 y}{4 x^{2} - 4 x y + 3 y^{2}},\,\frac{∂h}{∂y}=\frac{- 4 x + 6 y}{4 x^{2} - 4 x y + 3 y^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂h}{∂x} & =\frac{- 4 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}, \\ \frac{∂h}{∂y} & =\frac{6 r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂h}{∂\theta} & =(\frac{- 4 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})(- r \sin{\left(\theta \right)})+(\frac{6 r \sin{\left(\theta \right)} - 4 r \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})(r \cos{\left(\theta \right)}) \\  & =(\frac{4 r^{2} \sin^{2}{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})+(\frac{6 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{4 r^{2} \cos^{2}{\left(\theta \right)}}{3 r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}) \\  & =\frac{4 \sin^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 4 \cos^{2}{\left(\theta \right)}}{3 \sin^{2}{\left(\theta \right)} - 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}\end{aligned}
$$

---

Given that $w(x,y)=- 2 x^{2} y - x y^{2},$ find $\frac{∂w}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $\frac{r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}}{r}$

B. $r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}$

C. $- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}$

D. $- r^{3} \sin^{3}{\left(\theta \right)} - 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} + 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} + 2 r^{3} \cos^{3}{\left(\theta \right)}$

E. $r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}$

Worked solution:

Applying the multivariable chain rule for the function $w(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂w}{∂\theta} & =\frac{∂w}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂w}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂w}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂w}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $w$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂w}{∂x}=- 4 x y - y^{2},\,\frac{∂w}{∂y}=- 2 x^{2} - 2 x y\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂w}{∂x} & =- r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}, \\ \frac{∂w}{∂y} & =- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂w}{∂\theta} & =(- r^{2} \sin^{2}{\left(\theta \right)} - 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)})(- r \sin{\left(\theta \right)})+(- 2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{2} \cos^{2}{\left(\theta \right)})(r \cos{\left(\theta \right)}) \\  & =(r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)})+(- 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}) \\  & =r^{3} \sin^{3}{\left(\theta \right)} + 4 r^{3} \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)} - 2 r^{3} \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 r^{3} \cos^{3}{\left(\theta \right)}\end{aligned}
$$

---

Given that $g(x,y)=\ln{\left(4 x^{2} + 3 x y + y^{2} \right)},$ find $\frac{∂g}{∂\theta},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta)$ are the corresponding plane polar coordinates.

A. $- \frac{3 r^{2} \sin^{2}{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}$

B. $- \frac{- 3 \sin^{2}{\left(\theta \right)} - 6 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}{\sin^{2}{\left(\theta \right)} + 3 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}$

C. $\frac{2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} + \frac{3 r^{2} \cos^{2}{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}$

D. $\frac{- 3 \sin^{2}{\left(\theta \right)} - 6 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}{r \left(\sin^{2}{\left(\theta \right)} + 3 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}\right)}$

E. $\frac{- 3 \sin^{2}{\left(\theta \right)} - 6 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}{\sin^{2}{\left(\theta \right)} + 3 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}$

Worked solution:

Applying the multivariable chain rule for the function $g(x,y)$ with two independent variables $r$ and $\theta,$ where $x=r\cos\theta$ and $y=r\sin\theta,$ we have

$$
\begin{aligned}\frac{∂g}{∂\theta} & =\frac{∂g}{∂x}\cdot \frac{∂x}{∂\theta}+\frac{∂g}{∂y}\cdot \frac{∂y}{∂\theta} \\  & =(\frac{∂g}{∂x})(- r \sin{\left(\theta \right)})+(\frac{∂g}{∂y})(r \cos{\left(\theta \right)})\end{aligned}
$$

First, we find the partial derivatives of $g$ with respect to $x$ and $y:$

$$
\begin{aligned}\frac{∂g}{∂x}=\frac{8 x + 3 y}{4 x^{2} + 3 x y + y^{2}},\,\frac{∂g}{∂y}=\frac{3 x + 2 y}{4 x^{2} + 3 x y + y^{2}}\end{aligned}
$$

Writing the above results in terms of $r$ and $\theta,$ we get

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{3 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}, \\ \frac{∂g}{∂y} & =\frac{2 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}.\end{aligned}
$$

Finally, substituting these into our chain rule formula, we get

$$
\begin{aligned}\frac{∂g}{∂\theta} & =(\frac{3 r \sin{\left(\theta \right)} + 8 r \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})(- r \sin{\left(\theta \right)})+(\frac{2 r \sin{\left(\theta \right)} + 3 r \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})(r \cos{\left(\theta \right)}) \\  & =(- \frac{3 r^{2} \sin^{2}{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} - \frac{8 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}})+(\frac{2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}} + \frac{3 r^{2} \cos^{2}{\left(\theta \right)}}{r^{2} \sin^{2}{\left(\theta \right)} + 3 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 r^{2} \cos^{2}{\left(\theta \right)}}) \\  & =\frac{- 3 \sin^{2}{\left(\theta \right)} - 6 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 3 \cos^{2}{\left(\theta \right)}}{\sin^{2}{\left(\theta \right)} + 3 \sin{\left(\theta \right)} \cos{\left(\theta \right)} + 4 \cos^{2}{\left(\theta \right)}}\end{aligned}
$$