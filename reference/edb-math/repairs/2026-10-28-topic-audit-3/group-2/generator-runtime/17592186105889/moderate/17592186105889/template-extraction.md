# Step 4 — template extraction

## Stage 1: specific source descriptions

Every source definition is reproduced below with its exact complete choices. The variable roles are independent real coordinates x,y, dependent graph coordinate z=g(x,y), and scalar surface weight f(x,y,z). Rectangle bounds are presentation/domain inputs; the assessment is the missing integrand, so they are excluded from mathematical task identity. Signs of the graph coefficients remain important to f(g) but are squared in the metric. All scalar operations are exact; there is no numerical approximation or evaluated surface integral.

### q-161106

Consider the surface integral of the function $f(x,y,z)=2xy,$ where the surface $S$ is defined by $z={x}^{2}+{y}^{2}$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 0be6bfb1-22ec-54d7-8d70-408044da5849 | `2xy\sqrt{1+4{x}^{2}+4{y}^{2}}` | yes | `(k/k₀) × (2xy\sqrt{1+4{x}^{2}+4{y}^{2}})`; complete structural expression, opaque intent |

| 11f496da-87e3-5a3b-81b0-ad4ccd99eec9 | `2xy\sqrt{1+{x}^{2}+{y}^{2}}` | no | `(k/k₀) × (2xy\sqrt{1+{x}^{2}+{y}^{2}})`; complete structural expression, opaque intent |

| 1ac43cfe-450e-5f00-a858-df79110cc719 | `xy\sqrt{1+4{x}^{2}+4{y}^{2}}` | no | `(k/k₀) × (xy\sqrt{1+4{x}^{2}+4{y}^{2}})`; complete structural expression, opaque intent |

| 855fc78b-5ccc-59f0-bca3-89185d1730e3 | `xy\sqrt{1+{x}^{2}+{y}^{2}}` | no | `(k/k₀) × (xy\sqrt{1+{x}^{2}+{y}^{2}})`; complete structural expression, opaque intent |

| b4c85dc7-b6d4-5404-8564-0781f52fb42d | `(x+y+xy)\sqrt{1+{x}^{2}+{y}^{2}}` | no | `(k/k₀) × ((x+y+xy)\sqrt{1+{x}^{2}+{y}^{2}})`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}({x}^{2}+{y}^{2})=2x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}({x}^{2}+{y}^{2})=2y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(2x)}^{2}+{(2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2xy\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{2}\,2xy\sqrt{1+4{x}^{2}+4{y}^{2}}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161323

Consider the surface integral of the function $f(x, y, z) =-3xz$, where the surface $S$ is defined by $z = \sqrt{2}x + \sqrt{2}y$ for $0 \le x \le 1$ and $0 \le y \le 2$.
This surface integral can be written as a repeated integral, as shown below.
$∬_(S)f(x, y, z)dS = \displaystyle \int_{0}^{1}\displaystyle \int_{0}^{2}AAAAAAAdydx$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/id`, `:question/math-academy-id`, `:question/problem`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 8797f6aa-cf9f-5cdf-9e2e-81ed04cfb981 | `-3\sqrt{10}(x^{2} + xy)` | absent | `(k/k₀) × (-3\sqrt{10}(x^{2} + xy))`; complete structural expression, opaque intent |

| 9aa9edd5-3b13-5153-89a1-cbc230125392 | `-2\sqrt{10}(-x^{2}y + xy)` | absent | `(k/k₀) × (-2\sqrt{10}(-x^{2}y + xy))`; complete structural expression, opaque intent |

| 3c94fbac-ac12-5764-97bd-c8d97a316c61 | `-10\sqrt{3}(x^{2} - xy)` | absent | `(k/k₀) × (-10\sqrt{3}(x^{2} - xy))`; complete structural expression, opaque intent |

| 4ff3c3f4-ebf9-5068-a4a6-bd8e76178c58 | `-3\sqrt{5x}(x^{2} + x^{2}y^{2})` | absent | `(k/k₀) × (-3\sqrt{5x}(x^{2} + x^{2}y^{2}))`; complete structural expression, opaque intent |

| 710da267-89b8-50aa-a066-1c9994d5588d | `-3\sqrt{5}(x^{2} + 2xy)` | absent | `(k/k₀) × (-3\sqrt{5}(x^{2} + 2xy))`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

[Absent in capture; no solution is invented in raw replay.]

### q-161319

Consider the surface integral of the function $f(x,y,z)=xy{z}^{2},$ where the surface $S$ is defined by $z=y-2x$ for $-1\le x\le 1$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 2a533bb1-853f-5491-8c86-67f976471508 | `\sqrt{6}\,xy(y-2x)^{2}` | yes | `(k/k₀) × (\sqrt{6}\,xy(y-2x)^{2})`; complete structural expression, opaque intent |

| 51369986-90ae-5b8b-bd51-00e4a125fb18 | `\sqrt{6}\,x{y}^{2}(y+2x)^{2}` | no | `(k/k₀) × (\sqrt{6}\,x{y}^{2}(y+2x)^{2})`; complete structural expression, opaque intent |

| 62b5397b-e1ef-56af-b3c3-0127ce34e303 | `3{x}^{2}y(y-2x)^{2}` | no | `(k/k₀) × (3{x}^{2}y(y-2x)^{2})`; complete structural expression, opaque intent |

| 7ea26c5b-44a3-5c69-9b86-1ab9c4524f0c | `\sqrt{6}\,{x}^{2}y(y-2x)^{2}` | no | `(k/k₀) × (\sqrt{6}\,{x}^{2}y(y-2x)^{2})`; complete structural expression, opaque intent |

| e533f6b6-2b56-5f69-89d2-aa4aa20f904b | `\sqrt{3}\,xy(y-2x)^{2}` | no | `(k/k₀) × (\sqrt{3}\,xy(y-2x)^{2})`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(y-2x)=-2
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(y-2x)=1.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\sqrt{6}\,xy(y-2x)^{2}\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{-1}^{1}\,\sqrt{6}\,xy(y-2x)^{2}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161321

Consider the surface integral of the function $f(x,y,z)=\sqrt{2}xyz,$ where the surface $S$ is defined by $z=-\sqrt{2}x-\sqrt{2}y$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 086549fa-2a26-5001-86f1-5b98b5f931b5 | `\sqrt{5}({x}^{2}y+{x}^{2}{y}^{2})` | no | `(k/k₀) × (\sqrt{5}({x}^{2}y+{x}^{2}{y}^{2}))`; complete structural expression, opaque intent |

| 50ddfd56-d4fe-58e4-9068-9d6c2ddb54e5 | `\sqrt{5x}(2{x}^{2}-x{y}^{2})` | no | `(k/k₀) × (\sqrt{5x}(2{x}^{2}-x{y}^{2}))`; complete structural expression, opaque intent |

| 9dada5e0-74dc-5e81-a533-742d9452a01c | `-2\sqrt{5}({x}^{2}y+x{y}^{2})` | yes | `(k/k₀) × (-2\sqrt{5}({x}^{2}y+x{y}^{2}))`; complete structural expression, opaque intent |

| a82df97c-47b4-5649-adc4-f83468150b33 | `5\sqrt{2}({x}^{2}{y}^{2}+x{y}^{2})` | no | `(k/k₀) × (5\sqrt{2}({x}^{2}{y}^{2}+x{y}^{2}))`; complete structural expression, opaque intent |

| bca9a670-f13c-561a-a08a-381f1f64ba75 | `-2\sqrt{2}({x}^{2}y-x{y}^{2})` | no | `(k/k₀) × (-2\sqrt{2}({x}^{2}y-x{y}^{2}))`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-\sqrt{2}x-\sqrt{2}y)=-\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-\sqrt{2}x-\sqrt{2}y)=-\sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-\sqrt{2})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\sqrt{2}xy(-\sqrt{2}x-\sqrt{2}y)\sqrt{5}\,\text{d}A \\  & ={∬}_{D}\,(-2{x}^{2}y-2x{y}^{2})\sqrt{5}\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{2}\,-2\sqrt{5}({x}^{2}y+x{y}^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161325

Consider the surface integral of the function $f(x,y,z)={x}^{2}{z}^{2},$ where the surface $S$ is defined by $z=-{x}^{2}+2{y}^{2}$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 66ddc6b9-504b-58c8-bd2c-8ca80ec11d33 | `(6{x}^{4}+4{y}^{2}x+{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+4{y}^{2}}` | no | `(k/k₀) × ((6{x}^{4}+4{y}^{2}x+{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+4{y}^{2}})`; complete structural expression, opaque intent |

| 6ed6f32a-ed59-5647-bcd6-86e6da4ee2ec | `({x}^{4}-4{y}^{2}{x}^{3}+4{x}^{2})\sqrt{1+16{x}^{2}-4{y}^{2}}` | no | `(k/k₀) × (({x}^{4}-4{y}^{2}{x}^{3}+4{x}^{2})\sqrt{1+16{x}^{2}-4{y}^{2}})`; complete structural expression, opaque intent |

| 9b1689bf-d1a3-5784-9e6f-9117c0c02c2c | `(4{x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}x)\sqrt{1+16{x}^{2}+16{y}^{2}}` | no | `(k/k₀) × ((4{x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}x)\sqrt{1+16{x}^{2}+16{y}^{2}})`; complete structural expression, opaque intent |

| bd9b2183-af1c-5150-ab05-abef28325ca3 | `({x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+16{y}^{2}}` | yes | `(k/k₀) × (({x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+16{y}^{2}})`; complete structural expression, opaque intent |

| fb1e7756-7d83-53a3-b74f-dfc6cb5f4b38 | `({x}^{4}-{y}^{2}{x}^{3}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}-4{y}^{2}}` | no | `(k/k₀) × (({x}^{4}-{y}^{2}{x}^{3}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}-4{y}^{2}})`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-{x}^{2}+2{y}^{2})=-2x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-{x}^{2}+2{y}^{2})=4y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(4y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,{x}^{2}(-{x}^{2}+2{y}^{2})^{2}\sqrt{1+4{x}^{2}+16{y}^{2}}\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{2}\,({x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+16{y}^{2}}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161314

Consider the surface integral of the function $f(x,y,z)={x}^{2}yz,$ where the surface $S$ is defined by $z=-x+y$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| ed482a3a-a562-53c9-9952-b7f4ae64a9f4 | `\sqrt{3}(-{x}^{3}+{x}^{2}{y}^{3})` | no | `(k/k₀) × (\sqrt{3}(-{x}^{3}+{x}^{2}{y}^{3}))`; complete structural expression, opaque intent |

| 292ba469-4e9c-5812-b40c-813e27620124 | `\sqrt{3y}(-{x}^{2}y-{x}^{2}{y}^{2})` | no | `(k/k₀) × (\sqrt{3y}(-{x}^{2}y-{x}^{2}{y}^{2}))`; complete structural expression, opaque intent |

| 1139e147-84fe-5bb5-a30a-874f5c401de8 | `\sqrt{3}(-{x}^{2}y-{x}^{2}y)` | no | `(k/k₀) × (\sqrt{3}(-{x}^{2}y-{x}^{2}y))`; complete structural expression, opaque intent |

| 25a694b0-85e4-50a9-9c0d-fb4f6db18268 | `\sqrt{3}(-{x}^{3}y+{x}^{2}{y}^{2})` | yes | `(k/k₀) × (\sqrt{3}(-{x}^{3}y+{x}^{2}{y}^{2}))`; complete structural expression, opaque intent |

| 60287cb2-73a4-5d70-9afa-49321e3ddf3d | `\sqrt{3x}({x}^{3}y+{x}^{2}{y}^{2})` | no | `(k/k₀) × (\sqrt{3x}({x}^{3}y+{x}^{2}{y}^{2}))`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-x+y)=-1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-x+y)=1.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-1)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,{x}^{2}y(-x+y)\sqrt{3}\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{2}\,\sqrt{3}(-{x}^{3}y+{x}^{2}{y}^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161320

Consider the surface integral of the function $f(x,y,z)={x}^{2}{y}^{2}z,$ where the surface $S$ is defined by $z=-{x}^{2}-{y}^{2}$ for $0\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{0}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| fef4addc-f714-5c73-ba79-b8bbf017a6d0 | `({x}^{2}{y}^{2}-{x}^{4}{y}^{4})\sqrt{1+2{x}^{2}+2{y}^{2}}` | no | `(k/k₀) × (({x}^{2}{y}^{2}-{x}^{4}{y}^{4})\sqrt{1+2{x}^{2}+2{y}^{2}})`; complete structural expression, opaque intent |

| 32ada5ea-3508-5fad-8e67-d2275d868693 | `({x}^{4}{y}^{4}+{x}^{4}{y}^{4})\sqrt{1+4{y}^{2}}` | no | `(k/k₀) × (({x}^{4}{y}^{4}+{x}^{4}{y}^{4})\sqrt{1+4{y}^{2}})`; complete structural expression, opaque intent |

| 0adb517f-11c6-5796-89c8-e402d79f5011 | `(-{x}^{4}{y}^{2}-{x}^{2}{y}^{4})\sqrt{1+4{x}^{2}+4{y}^{2}}` | yes | `(k/k₀) × ((-{x}^{4}{y}^{2}-{x}^{2}{y}^{4})\sqrt{1+4{x}^{2}+4{y}^{2}})`; complete structural expression, opaque intent |

| d4c7988a-9786-511c-9fd8-d31cb890bb80 | `(-{x}^{4}{y}^{2}-4{x}^{4}{y}^{4})\sqrt{1+4x+4y}` | no | `(k/k₀) × ((-{x}^{4}{y}^{2}-4{x}^{4}{y}^{4})\sqrt{1+4x+4y})`; complete structural expression, opaque intent |

| cf5ced82-50c7-5506-b6d6-5d386e556ca9 | `({y}^{2}-{x}^{2}{y}^{4})\sqrt{4{x}^{2}+4{y}^{2}}` | no | `(k/k₀) × (({y}^{2}-{x}^{2}{y}^{4})\sqrt{4{x}^{2}+4{y}^{2}})`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-{x}^{2}-{y}^{2})=-2x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-{x}^{2}-{y}^{2})=-2y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(-2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,{x}^{2}{y}^{2}(-{x}^{2}-{y}^{2})\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}\,(-{x}^{4}{y}^{2}-{x}^{2}{y}^{4})\sqrt{1+4{x}^{2}+4{y}^{2}}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

### q-161326

Consider the surface integral of the function $f(x,y,z)=\sqrt{2}y,$ where the surface $S$ is defined by $z=-\sqrt{2}x-y$ for $-1\le x\le 0$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{0}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Fields present: `:db/id`, `:question/answer-fields`, `:question/difficulty`, `:question/id`, `:question/math-academy-id`, `:question/problem`, `:question/worked-solution`.

Original bank (field `selection`; each value remains a whole expression):

| UUID | Exact value | Original correct designation | Parameterized raw recipe |

|---|---|---|---|

| 246b6bfe-20aa-55cc-b239-3304de81494f | `-2\sqrt{2}y` | no | `(k/k₀) × (-2\sqrt{2}y)`; complete structural expression, opaque intent |

| 72fa2757-f8e2-52c7-97eb-f3ea64fd0de1 | `4\sqrt{2}y` | no | `(k/k₀) × (4\sqrt{2}y)`; complete structural expression, opaque intent |

| a9391385-1fbe-53da-993e-c0f38007e6e4 | `-4\sqrt{2}{y}^{2}` | no | `(k/k₀) × (-4\sqrt{2}{y}^{2})`; complete structural expression, opaque intent |

| abd564cc-a7f0-5f60-a224-edcb8733b99b | `2\sqrt{2}y` | yes | `(k/k₀) × (2\sqrt{2}y)`; complete structural expression, opaque intent |

| fa49e0e8-2a63-57cc-8df5-3f02f87ef7e4 | `\sqrt{2}y` | no | `(k/k₀) × (\sqrt{2}y)`; complete structural expression, opaque intent |

Original solution sequence and fixed prose:

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-\sqrt{2}x-y)=-\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-\sqrt{2}x-y)=-1.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\sqrt{2}y\cdot 2\,\text{d}A \\  & ={\int }_{-1}^{0}{\int }_{0}^{2}\,2\sqrt{2}y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

## Stage 2: generalized shared pattern

Given a Cartesian graph z=g(x,y) over an explicitly bounded rectangle and a polynomial scalar f, determine only the missing repeated-integral integrand f(x,y,g(x,y))√(1+g_x²+g_y²). Formal partial differentiation, substitution, metric construction and polynomial multiplication are the assessed operations. The differential order is dy dx. There is one fixed worked solution independent of the learner choice.

## Stage 3: components and complete bank mapping

The tables above map all 40 original options to their original owned UUID, correct designation where present, exact value and parameterized raw recipe. Each profile `raw:q-N` comprises the entire five-member original bank. A scalar multiplier k/k₀ scales f and every scalar solution/choice row without changing g or the derivative metric. This is a conservative parameterized structural generalization, not a recovered explanation of unusual exponent errors. Surface changes are rejected in these opaque raw profiles. The observed original expression trees are parsed, scaled and rendered through public generate; there is no source-payload return branch or final answer lookup. Original spelling is recovered per complete expression slot only when its symbolic value equals the original component.

No bank member is individually replaced or selected from a distractor pool. The normal complete `measure_conversion` bank is selected first and then evaluates precisely `[P M, P, P M², P/M, P√(g_x²+g_y²)]`, where P=f(x,y,g) and M=√(1+g_x²+g_y²). The mistakes are omission of surface measure, failure to take its square root, inversion of the measure conversion, and omission of the graph metric’s leading 1. Each is a real operation on the displayed formula. Native UUID tests independently check all five choices, while symbolic readback checks their displayed complete mathematical values. Any equivalence or invalid domain rejects the whole instance.

Historical bank domain anomalies remain explicit: q-161321 has √(5x) on x∈[-1,1]; q-161314 has √(3x) on x∈[-1,1]; q-161325 has 1+16x²−4y² and 1+4x²−4y² inside wrong radicals, becoming negative at x=0,y=2. q-161323’s √(5x) is real on its original x∈[0,1], but its missing grading metadata and arbitrary mixed exponents remain unresolved. These raw banks are all evidence-only; none enters default sampling. The correct inferred q-161323 expression is −3√10(x²+xy). Its first historical option equals this expression, but absent original correct designation is never counted as matched.

## Stage 4: reusable masks and bounded domains

Observed easy masks have g=ax^m+by^n and f=kx^u y^v z^w, with exponent patterns exactly as cataloged in classification. Default nonzero a,b,k∈{−2,−1,1,2,−√2,√2}; the original exact values are included. The original bounds all fit the domain: integer endpoints of magnitude ≤3, lower<upper on each coordinate. The raw masks permit k/k₀∈{−3,−2,−1,1,2,3} and hold a,b fixed; they preserve each original derivative block, whole row count, row order, punctuation and prose. Normal records retain formal operator rows plus generic formula, substituted derivative metric, unsimplified actual substitution, expanded product and repeated-integral setup. No diagnosis text is invented.

Authored moderate templates coupled_xz/coupled_yz use g=ax²+bxy+cy² and f=kxz or kyz. Both partials contain two nonzero algebraic terms and there is exactly one substantive z substitution with a three-term product. Authored hard templates coupled_two_x/coupled_two_y use f=kxz+lyz² or kyz+lxz² with the same graph. There are exactly two z substitutions, one square of a three-term graph and two outer polynomial products before collection. Their degrees differ, so the two assessed f terms cannot cancel each other. A cross coefficient in the expanded square can cancel; the required square/substitution workload remains unchanged. All nonzero authored coefficients have signed magnitude ≤2, enforced identically on samplers and explicit calls. All templates within either authored level are unordered coordinate placements.

Meaningful variety: easy provides 6×6×6=216 coefficient tuples per observed shape before mathematical deduplication; moderate 4⁴=256 tuples per coordinate placement; hard 4⁵=1024 tuples per placement. Bounds are excluded from task counts. Coefficient sign symmetries and proportional expressions can reduce equivalent assessed outputs; these raw tuple counts are not claimed as unique question counts. Mathematical fingerprints canonicalize actual f(g) and the squared derivative metric; complete banks, prose, profile labels, coefficient spellings and seed are excluded. Content identity separately includes actual difficulty, prompt, fixed solution and complete bank with correct designations, excluding option order and seed.

The raw source key-presence parity is checked independently for every record. q-161323 preserves its AAAAAAA placeholder and original strange integral spelling; a completed normal plane_xz question is separately authored and eligible. It has the normal displayed empty box, full solution and independent mathematical correct choice. No TeX escape repair is claimed on the basis of JSON serialization.

Exhaustive coefficient-domain enumeration in `variety.json` finds 738 easy, 256 moderate, 1024 hard distinct canonical assessed tasks after coefficient sign symmetries and duplicate substituted-scalar/metric pairs are removed. Bounds, permutations, seeds and profile spelling contribute zero tasks.
