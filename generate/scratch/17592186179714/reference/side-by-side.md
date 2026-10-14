### separate_roots

Original:

Find the gradient vector field of the function $f(x,y)=\sqrt{2x-1}-\sqrt{4y+1}.$

Variant:

Find the gradient vector field of the function $f(x,y)=\sqrt{6 x - 3} - \sqrt{3 y - 2}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y)&=\frac{\partial}{\partial x}\left(\sqrt{6 x - 3} - \sqrt{3 y - 2}\right) \\ &=\frac{3}{\sqrt{6 x - 3}} \\ f_{y}(x,y)&=\frac{\partial}{\partial y}\left(\sqrt{6 x - 3} - \sqrt{3 y - 2}\right) \\ &=- \frac{3}{2 \sqrt{3 y - 2}}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y)$ is

$$
\begin{aligned}\nabla f(x,y)&=f_{x}(x,y)\,i+f_{y}(x,y)\,j \\ &= \frac{3}{\sqrt{6 x - 3}}\,i- \frac{3}{2 \sqrt{3 y - 2}}\,j.\end{aligned}
$$

---

### linear_log

Original:

Find the gradient vector field of the function $f(x,y)=\operatorname{ln}⁡(2x+4y).$

Variant:

Find the gradient vector field of the function $f(x,y)=\ln{\left(6 x + 2 y \right)}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y)&=\frac{\partial}{\partial x}\left(\ln{\left(6 x + 2 y \right)}\right) \\ &=\frac{6}{6 x + 2 y} \\ f_{y}(x,y)&=\frac{\partial}{\partial y}\left(\ln{\left(6 x + 2 y \right)}\right) \\ &=\frac{2}{6 x + 2 y}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y)$ is

$$
\begin{aligned}\nabla f(x,y)&=f_{x}(x,y)\,i+f_{y}(x,y)\,j \\ &= \frac{6}{6 x + 2 y}\,i+\frac{2}{6 x + 2 y}\,j.\end{aligned}
$$

---

### linear_tan

Original:

Find the gradient vector field of the function $f(x,y)=\operatorname{tan}⁡(x-2y).$

Variant:

Find the gradient vector field of the function $f(x,y)=\tan{\left(4 x - 3 y \right)}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y)&=\frac{\partial}{\partial x}\left(\tan{\left(4 x - 3 y \right)}\right) \\ &=4 \sec^{2}{\left(4 x - 3 y \right)} \\ f_{y}(x,y)&=\frac{\partial}{\partial y}\left(\tan{\left(4 x - 3 y \right)}\right) \\ &=- 3 \sec^{2}{\left(4 x - 3 y \right)}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y)$ is

$$
\begin{aligned}\nabla f(x,y)&=f_{x}(x,y)\,i+f_{y}(x,y)\,j \\ &= 4 \sec^{2}{\left(4 x - 3 y \right)}\,i- 3 \sec^{2}{\left(4 x - 3 y \right)}\,j.\end{aligned}
$$

---

### product_log

Original:

Find the gradient vector field of the function $f(x,y,z)=x\operatorname{ln}⁡(z-2y).$

Variant:

Find the gradient vector field of the function $f(x,y,z)=x \ln{\left(- 5 y + z \right)}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y,z)&=\frac{\partial}{\partial x}\left(x \ln{\left(- 5 y + z \right)}\right) \\ &=\ln{\left(- 5 y + z \right)} \\ f_{y}(x,y,z)&=\frac{\partial}{\partial y}\left(x \ln{\left(- 5 y + z \right)}\right) \\ &=- \frac{5 x}{- 5 y + z} \\ f_{z}(x,y,z)&=\frac{\partial}{\partial z}\left(x \ln{\left(- 5 y + z \right)}\right) \\ &=\frac{x}{- 5 y + z}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y,z)$ is

$$
\begin{aligned}\nabla f(x,y,z)&=f_{x}(x,y,z)\,i+f_{y}(x,y,z)\,j+f_{z}(x,y,z)\,k \\ &= \ln{\left(- 5 y + z \right)}\,i- \frac{5 x}{- 5 y + z}\,j+\frac{x}{- 5 y + z}\,k.\end{aligned}
$$

---

### radial_root

Original:

Find the gradient vector field of the function $f(x,y,z)=\sqrt{{x}^{2}+{y}^{2}+{z}^{2}}.$

Variant:

Find the gradient vector field of the function $f(x,y,z)=\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y,z)&=\frac{\partial}{\partial x}\left(\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}\right) \\ &=\frac{4 x}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}} \\ f_{y}(x,y,z)&=\frac{\partial}{\partial y}\left(\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}\right) \\ &=\frac{4 y}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}} \\ f_{z}(x,y,z)&=\frac{\partial}{\partial z}\left(\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}\right) \\ &=\frac{4 z}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y,z)$ is

$$
\begin{aligned}\nabla f(x,y,z)&=f_{x}(x,y,z)\,i+f_{y}(x,y,z)\,j+f_{z}(x,y,z)\,k \\ &= \frac{4 x}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}}\,i+\frac{4 y}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}}\,j+\frac{4 z}{\sqrt{4 x^{2} + 4 y^{2} + 4 z^{2}}}\,k.\end{aligned}
$$

---

### product_sine

Original:

Find the gradient vector field of the function $f(x,y,z)=\operatorname{sin}⁡(xz+2y).$

Variant:

Find the gradient vector field of the function $f(x,y,z)=\sin{\left(x z + 5 y \right)}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y,z)&=\frac{\partial}{\partial x}\left(\sin{\left(x z + 5 y \right)}\right) \\ &=z \cos{\left(x z + 5 y \right)} \\ f_{y}(x,y,z)&=\frac{\partial}{\partial y}\left(\sin{\left(x z + 5 y \right)}\right) \\ &=5 \cos{\left(x z + 5 y \right)} \\ f_{z}(x,y,z)&=\frac{\partial}{\partial z}\left(\sin{\left(x z + 5 y \right)}\right) \\ &=x \cos{\left(x z + 5 y \right)}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y,z)$ is

$$
\begin{aligned}\nabla f(x,y,z)&=f_{x}(x,y,z)\,i+f_{y}(x,y,z)\,j+f_{z}(x,y,z)\,k \\ &= z \cos{\left(x z + 5 y \right)}\,i+5 \cos{\left(x z + 5 y \right)}\,j+x \cos{\left(x z + 5 y \right)}\,k.\end{aligned}
$$

---

### product_arctan

Original:

Find the gradient vector field of the function $f(x,y,z)=\operatorname{arctan}⁡(xyz).$

Variant:

Find the gradient vector field of the function $f(x,y,z)=\arctan{\left(4 x y z \right)}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y,z)&=\frac{\partial}{\partial x}\left(\arctan{\left(4 x y z \right)}\right) \\ &=\frac{4 y z}{16 x^{2} y^{2} z^{2} + 1} \\ f_{y}(x,y,z)&=\frac{\partial}{\partial y}\left(\arctan{\left(4 x y z \right)}\right) \\ &=\frac{4 x z}{16 x^{2} y^{2} z^{2} + 1} \\ f_{z}(x,y,z)&=\frac{\partial}{\partial z}\left(\arctan{\left(4 x y z \right)}\right) \\ &=\frac{4 x y}{16 x^{2} y^{2} z^{2} + 1}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y,z)$ is

$$
\begin{aligned}\nabla f(x,y,z)&=f_{x}(x,y,z)\,i+f_{y}(x,y,z)\,j+f_{z}(x,y,z)\,k \\ &= \frac{4 y z}{16 x^{2} y^{2} z^{2} + 1}\,i+\frac{4 x z}{16 x^{2} y^{2} z^{2} + 1}\,j+\frac{4 x y}{16 x^{2} y^{2} z^{2} + 1}\,k.\end{aligned}
$$

---

### mixed_polynomial

Original:

Find the gradient vector field of the function $f(x,y,z)=z{x}^{2}+x{y}^{3}-y{z}^{4}.$

Variant:

Find the gradient vector field of the function $f(x,y,z)=4 x^{2} z + 4 x y^{3} - 4 y z^{4}.$

The gradient vector field of a function $f$ is given by $\nabla f.$

First, we find the partial derivatives:

$$
\begin{aligned}f_{x}(x,y,z)&=\frac{\partial}{\partial x}\left(4 x^{2} z + 4 x y^{3} - 4 y z^{4}\right) \\ &=8 x z + 4 y^{3} \\ f_{y}(x,y,z)&=\frac{\partial}{\partial y}\left(4 x^{2} z + 4 x y^{3} - 4 y z^{4}\right) \\ &=12 x y^{2} - 4 z^{4} \\ f_{z}(x,y,z)&=\frac{\partial}{\partial z}\left(4 x^{2} z + 4 x y^{3} - 4 y z^{4}\right) \\ &=4 x^{2} - 16 y z^{3}\end{aligned}
$$

Therefore, the gradient vector field of $f(x,y,z)$ is

$$
\begin{aligned}\nabla f(x,y,z)&=f_{x}(x,y,z)\,i+f_{y}(x,y,z)\,j+f_{z}(x,y,z)\,k \\ &= \left(8 x z + 4 y^{3}\right)\,i+\left(12 x y^{2} - 4 z^{4}\right)\,j+\left(4 x^{2} - 16 y z^{3}\right)\,k.\end{aligned}
$$