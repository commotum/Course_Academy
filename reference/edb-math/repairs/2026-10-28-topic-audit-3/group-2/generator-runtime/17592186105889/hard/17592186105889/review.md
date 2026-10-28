# Source originals and generated setup variants

Raw historical profiles are evidence-only; authored normal variants are eligible.

## ORIGINAL q-161106

Consider the surface integral of the function $f(x,y,z)=2xy,$ where the surface $S$ is defined by $z={x}^{2}+{y}^{2}$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $xy\sqrt{1+4{x}^{2}+4{y}^{2}}$
- $2xy\sqrt{1+{x}^{2}+{y}^{2}}$
- $2xy\sqrt{1+4{x}^{2}+4{y}^{2}}$
- $(x+y+xy)\sqrt{1+{x}^{2}+{y}^{2}}$
- $xy\sqrt{1+{x}^{2}+{y}^{2}}$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_xy", "profile": "raw:q-161106", "parameters": {"a": "1", "b": "1", "k": "2", "bounds": [-1, 1, 0, 2]}, "seed": 0, "content_id": "7747f82b-3037-5ace-86c5-1861d4f2ccd6", "mathematical_fingerprint": "60f1b32f3a0b2dd5be3cf87983571d2bea90db35c82c38b5faa3b9d9544b449c", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161106"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161106 scale -2

Consider the surface integral of the function $f(x,y,z)=- 4 x y,$ where the surface $S$ is defined by $z={x}^{2}+{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 x y \sqrt{4 x^{2} + 4 y^{2} + 1}$
- $- 4 x y \sqrt{x^{2} + y^{2} + 1}$
- $- 2 x y \sqrt{x^{2} + y^{2} + 1}$
- $- 2 \sqrt{x^{2} + y^{2} + 1} (x y + x + y)$
- $- 4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(2x)}^{2}+{(2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_xy", "profile": "raw:q-161106", "parameters": {"a": "1", "b": "1", "k": "-4", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "61492fc6-17c3-5ed2-a19d-19552f5c4d2b", "mathematical_fingerprint": "2ea00aca9aa56c995dc1e804ae28685a24d07ee51dd3a96d973612eea908c780", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161106"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161106 scale 2

Consider the surface integral of the function $f(x,y,z)=4 x y,$ where the surface $S$ is defined by $z={x}^{2}+{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $2 x y \sqrt{4 x^{2} + 4 y^{2} + 1}$
- $4 x y \sqrt{x^{2} + y^{2} + 1}$
- $2 x y \sqrt{x^{2} + y^{2} + 1}$
- $2 \sqrt{x^{2} + y^{2} + 1} (x y + x + y)$
- $4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(2x)}^{2}+{(2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,4 x y \sqrt{4 x^{2} + 4 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_xy", "profile": "raw:q-161106", "parameters": {"a": "1", "b": "1", "k": "4", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "5c3fa8be-34eb-5027-9847-999a123f78fe", "mathematical_fingerprint": "1581768b725faeb6ccb438e45dcdf0523c679b422ea80e082f390df268fa8670", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161106"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161323

Consider the surface integral of the function $f(x, y, z) =-3xz$, where the surface $S$ is defined by $z = \sqrt{2}x + \sqrt{2}y$ for $0 \le x \le 1$ and $0 \le y \le 2$.
This surface integral can be written as a repeated integral, as shown below.
$∬_(S)f(x, y, z)dS = \displaystyle \int_{0}^{1}\displaystyle \int_{0}^{2}AAAAAAAdydx$

What is the missing expression?

Choices:
- $-10\sqrt{3}(x^{2} - xy)$
- $-2\sqrt{10}(-x^{2}y + xy)$
- $-3\sqrt{10}(x^{2} + xy)$
- $-3\sqrt{5}(x^{2} + 2xy)$
- $-3\sqrt{5x}(x^{2} + x^{2}y^{2})$

Worked solution:
[Absent in raw source]

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xz", "profile": "raw:q-161323", "parameters": {"a": "sqrt(2)", "b": "sqrt(2)", "k": "-3", "bounds": [0, 1, 0, 2]}, "seed": 0, "content_id": "59895a71-3032-5ce1-9f66-d3f4101f8a0c", "mathematical_fingerprint": "1c7961879ecccd137ba8c7ab757d857b669140f12e2f9f2bc8693d755e251af9", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161323"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161323 scale -2

Consider the surface integral of the function $f(x, y, z) =6 x z$, where the surface $S$ is defined by $z = \sqrt{2}x + \sqrt{2}y$ for $0 \le x \le 2$ and $-1 \le y \le 1$.
This surface integral can be written as a repeated integral, as shown below.
$∬_(S)f(x, y, z)dS = \displaystyle \int_{0}^{2}\displaystyle \int_{-1}^{1}AAAAAAAdydx$

What is the missing expression?

Choices:
- $20 \sqrt{3} (x^{2} - x y)$
- $4 \sqrt{10} (- x^{2} y + x y)$
- $6 \sqrt{5} \sqrt{x} (x^{2} y^{2} + x^{2})$
- $6 \sqrt{5} (x^{2} + 2 x y)$
- $6 \sqrt{10} (x^{2} + x y)$

Worked solution:
[Absent in raw source]

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xz", "profile": "raw:q-161323", "parameters": {"a": "sqrt(2)", "b": "sqrt(2)", "k": "6", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "614ea009-2b49-5f15-8820-78a024e3ef8e", "mathematical_fingerprint": "da23833df778c834d9a06e0e52dc01e90c36049a693720629824367ced00fda0", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161323"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161323 scale 2

Consider the surface integral of the function $f(x, y, z) =- 6 x z$, where the surface $S$ is defined by $z = \sqrt{2}x + \sqrt{2}y$ for $0 \le x \le 2$ and $-1 \le y \le 1$.
This surface integral can be written as a repeated integral, as shown below.
$∬_(S)f(x, y, z)dS = \displaystyle \int_{0}^{2}\displaystyle \int_{-1}^{1}AAAAAAAdydx$

What is the missing expression?

Choices:
- $- 20 \sqrt{3} (x^{2} - x y)$
- $- 4 \sqrt{10} (- x^{2} y + x y)$
- $- 6 \sqrt{5} \sqrt{x} (x^{2} y^{2} + x^{2})$
- $- 6 \sqrt{5} (x^{2} + 2 x y)$
- $- 6 \sqrt{10} (x^{2} + x y)$

Worked solution:
[Absent in raw source]

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xz", "profile": "raw:q-161323", "parameters": {"a": "sqrt(2)", "b": "sqrt(2)", "k": "-6", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "992f1ca7-4c87-5326-be10-a8f67fef51fe", "mathematical_fingerprint": "f492a9d2ddad0a13267d390fbbc5b5c2624d353e22b8de3d15d603f0e786332e", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161323"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161319

Consider the surface integral of the function $f(x,y,z)=xy{z}^{2},$ where the surface $S$ is defined by $z=y-2x$ for $-1\le x\le 1$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $3{x}^{2}y(y-2x)^{2}$
- $\sqrt{6}\,x{y}^{2}(y+2x)^{2}$
- $\sqrt{6}\,xy(y-2x)^{2}$
- $\sqrt{3}\,xy(y-2x)^{2}$
- $\sqrt{6}\,{x}^{2}y(y-2x)^{2}$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xy_z2", "profile": "raw:q-161319", "parameters": {"a": "-2", "b": "1", "k": "1", "bounds": [-1, 1, -1, 1]}, "seed": 0, "content_id": "fb04a65f-2d1b-5a4f-8d58-7db614be0c1a", "mathematical_fingerprint": "a6d8da89fc37d7f57ef4fbe2eee1e97aa784c9ad356ebd799283729977108b9c", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161319"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161319 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 x y z^{2},$ where the surface $S$ is defined by $z=y-2x$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 6 x^{2} y (- 2 x + y)^{2}$
- $- 2 \sqrt{6} x y^{2} (2 x + y)^{2}$
- $- 2 \sqrt{6} x^{2} y (- 2 x + y)^{2}$
- $- 2 \sqrt{3} x y (- 2 x + y)^{2}$
- $- 2 \sqrt{6} x y (- 2 x + y)^{2}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 2 \sqrt{6} x y (- 2 x + y)^{2}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 2 \sqrt{6} x y (- 2 x + y)^{2}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xy_z2", "profile": "raw:q-161319", "parameters": {"a": "-2", "b": "1", "k": "-2", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "4e190f86-2482-5dca-9a16-986edfdaad82", "mathematical_fingerprint": "8a4990ddfff92473aa4f3b5fdb80be9511c0909cd40f933968055aff93f7f158", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161319"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161319 scale 2

Consider the surface integral of the function $f(x,y,z)=2 x y z^{2},$ where the surface $S$ is defined by $z=y-2x$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $6 x^{2} y (- 2 x + y)^{2}$
- $2 \sqrt{6} x y^{2} (2 x + y)^{2}$
- $2 \sqrt{6} x^{2} y (- 2 x + y)^{2}$
- $2 \sqrt{3} x y (- 2 x + y)^{2}$
- $2 \sqrt{6} x y (- 2 x + y)^{2}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2 \sqrt{6} x y (- 2 x + y)^{2}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,2 \sqrt{6} x y (- 2 x + y)^{2}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xy_z2", "profile": "raw:q-161319", "parameters": {"a": "-2", "b": "1", "k": "2", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "3d28a55e-88f5-5af4-aa62-31596e4e4bd0", "mathematical_fingerprint": "592d264175f803e2a44bf74b52fe86399e193384feb729129b424e8802473ec5", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161319"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161321

Consider the surface integral of the function $f(x,y,z)=\sqrt{2}xyz,$ where the surface $S$ is defined by $z=-\sqrt{2}x-\sqrt{2}y$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $-2\sqrt{5}({x}^{2}y+x{y}^{2})$
- $\sqrt{5x}(2{x}^{2}-x{y}^{2})$
- $\sqrt{5}({x}^{2}y+{x}^{2}{y}^{2})$
- $-2\sqrt{2}({x}^{2}y-x{y}^{2})$
- $5\sqrt{2}({x}^{2}{y}^{2}+x{y}^{2})$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xyz", "profile": "raw:q-161321", "parameters": {"a": "-sqrt(2)", "b": "-sqrt(2)", "k": "sqrt(2)", "bounds": [-1, 1, 0, 2]}, "seed": 0, "content_id": "13086d74-2ebf-56e0-ba96-52080092657d", "mathematical_fingerprint": "f0c969a18f78c87e8150599cecf05004d9f7085eb8549c60b8b74ab94739919b", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161321"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161321 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 \sqrt{2} x y z,$ where the surface $S$ is defined by $z=-\sqrt{2}x-\sqrt{2}y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $4 \sqrt{5} (x^{2} y + x y^{2})$
- $- 2 \sqrt{5} \sqrt{x} (2 x^{2} - x y^{2})$
- $- 10 \sqrt{2} (x^{2} y^{2} + x y^{2})$
- $4 \sqrt{2} (x^{2} y - x y^{2})$
- $- 2 \sqrt{5} (x^{2} y^{2} + x^{2} y)$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-\sqrt{2})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 2 \sqrt{10} x y (- \sqrt{2} x - \sqrt{2} y)\,\text{d}A \\  & ={∬}_{D}\,- 2 \sqrt{5} (- 2 x^{2} y - 2 x y^{2})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,4 \sqrt{5} (x^{2} y + x y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xyz", "profile": "raw:q-161321", "parameters": {"a": "-sqrt(2)", "b": "-sqrt(2)", "k": "-2*sqrt(2)", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "f62c5dd0-c725-54d9-971f-7cafa0a16543", "mathematical_fingerprint": "c87027cc6a4555a9a9a4c95e2c6eadd86b2117c7641588c314244dc9de455927", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161321"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161321 scale 2

Consider the surface integral of the function $f(x,y,z)=2 \sqrt{2} x y z,$ where the surface $S$ is defined by $z=-\sqrt{2}x-\sqrt{2}y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 4 \sqrt{5} (x^{2} y + x y^{2})$
- $2 \sqrt{5} \sqrt{x} (2 x^{2} - x y^{2})$
- $10 \sqrt{2} (x^{2} y^{2} + x y^{2})$
- $- 4 \sqrt{2} (x^{2} y - x y^{2})$
- $2 \sqrt{5} (x^{2} y^{2} + x^{2} y)$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-\sqrt{2})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2 \sqrt{10} x y (- \sqrt{2} x - \sqrt{2} y)\,\text{d}A \\  & ={∬}_{D}\,2 \sqrt{5} (- 2 x^{2} y - 2 x y^{2})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 4 \sqrt{5} (x^{2} y + x y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xyz", "profile": "raw:q-161321", "parameters": {"a": "-sqrt(2)", "b": "-sqrt(2)", "k": "2*sqrt(2)", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "1a0f133c-b09b-5dd3-a39e-2b9936a0166f", "mathematical_fingerprint": "5a915210b195ffb5258757deb01287216443b02d933a995322d2a8268a8dc186", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161321"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161325

Consider the surface integral of the function $f(x,y,z)={x}^{2}{z}^{2},$ where the surface $S$ is defined by $z=-{x}^{2}+2{y}^{2}$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $(4{x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}x)\sqrt{1+16{x}^{2}+16{y}^{2}}$
- $({x}^{4}-4{y}^{2}{x}^{3}+4{x}^{2})\sqrt{1+16{x}^{2}-4{y}^{2}}$
- $(6{x}^{4}+4{y}^{2}x+{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+4{y}^{2}}$
- $({x}^{4}-{y}^{2}{x}^{3}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}-4{y}^{2}}$
- $({x}^{6}-4{y}^{2}{x}^{4}+4{y}^{4}{x}^{2})\sqrt{1+4{x}^{2}+16{y}^{2}}$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2_z2", "profile": "raw:q-161325", "parameters": {"a": "-1", "b": "2", "k": "1", "bounds": [-1, 1, 0, 2]}, "seed": 0, "content_id": "fb691132-f2cc-56c3-8d3b-13fc91af0a31", "mathematical_fingerprint": "c71d368f63ed08de5ec0dc9830deb0cda7ce86ee0be9dc4e5c06fd718489e0d6", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161325"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161325 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 x^{2} z^{2},$ where the surface $S$ is defined by $z=-{x}^{2}+2{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 \sqrt{16 x^{2} + 16 y^{2} + 1} (4 x^{6} - 4 x^{4} y^{2} + 4 x y^{4})$
- $- 2 \sqrt{16 x^{2} - 4 y^{2} + 1} (x^{4} - 4 x^{3} y^{2} + 4 x^{2})$
- $- 2 \sqrt{4 x^{2} + 16 y^{2} + 1} (x^{6} - 4 x^{4} y^{2} + 4 x^{2} y^{4})$
- $- 2 \sqrt{4 x^{2} - 4 y^{2} + 1} (x^{4} - x^{3} y^{2} + 4 x^{2} y^{4})$
- $- 2 \sqrt{4 x^{2} + 4 y^{2} + 1} (6 x^{4} + x^{2} y^{4} + 4 x y^{2})$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(4y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 2 x^{2} (- x^{2} + 2 y^{2})^{2} \sqrt{4 x^{2} + 16 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 2 \sqrt{4 x^{2} + 16 y^{2} + 1} (x^{6} - 4 x^{4} y^{2} + 4 x^{2} y^{4})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2_z2", "profile": "raw:q-161325", "parameters": {"a": "-1", "b": "2", "k": "-2", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "839d23a0-652b-58d9-9971-a09028f65ab3", "mathematical_fingerprint": "f797dd51537e7badef5aad55ffe76218afe74622898ce514c4f0b9523346d821", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161325"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161325 scale 2

Consider the surface integral of the function $f(x,y,z)=2 x^{2} z^{2},$ where the surface $S$ is defined by $z=-{x}^{2}+2{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $2 \sqrt{16 x^{2} + 16 y^{2} + 1} (4 x^{6} - 4 x^{4} y^{2} + 4 x y^{4})$
- $2 \sqrt{16 x^{2} - 4 y^{2} + 1} (x^{4} - 4 x^{3} y^{2} + 4 x^{2})$
- $2 \sqrt{4 x^{2} + 16 y^{2} + 1} (x^{6} - 4 x^{4} y^{2} + 4 x^{2} y^{4})$
- $2 \sqrt{4 x^{2} - 4 y^{2} + 1} (x^{4} - x^{3} y^{2} + 4 x^{2} y^{4})$
- $2 \sqrt{4 x^{2} + 4 y^{2} + 1} (6 x^{4} + x^{2} y^{4} + 4 x y^{2})$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(4y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2 x^{2} (- x^{2} + 2 y^{2})^{2} \sqrt{4 x^{2} + 16 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,2 \sqrt{4 x^{2} + 16 y^{2} + 1} (x^{6} - 4 x^{4} y^{2} + 4 x^{2} y^{4})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2_z2", "profile": "raw:q-161325", "parameters": {"a": "-1", "b": "2", "k": "2", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "534cd0e4-29c1-575b-953c-4844429c2da6", "mathematical_fingerprint": "05aa69d6d08539ae816c31522663b6bfe48023c147e26333563385f66e92d73c", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161325"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161314

Consider the surface integral of the function $f(x,y,z)={x}^{2}yz,$ where the surface $S$ is defined by $z=-x+y$ for $-1\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{3}(-{x}^{2}y-{x}^{2}y)$
- $\sqrt{3y}(-{x}^{2}y-{x}^{2}{y}^{2})$
- $\sqrt{3}(-{x}^{3}+{x}^{2}{y}^{3})$
- $\sqrt{3x}({x}^{3}y+{x}^{2}{y}^{2})$
- $\sqrt{3}(-{x}^{3}y+{x}^{2}{y}^{2})$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_x2yz", "profile": "raw:q-161314", "parameters": {"a": "-1", "b": "1", "k": "1", "bounds": [-1, 1, 0, 2]}, "seed": 0, "content_id": "74c2bb86-d0bf-51da-80ea-f1722036da56", "mathematical_fingerprint": "692ba1132f01ab418e8380f2caffb5f42cbe49e10a981f589fd4022386c21e29", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161314"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161314 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 x^{2} y z,$ where the surface $S$ is defined by $z=-x+y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $4 \sqrt{3} x^{2} y$
- $- 2 \sqrt{3} \sqrt{y} (- x^{2} y^{2} - x^{2} y)$
- $- 2 \sqrt{3} (- x^{3} y + x^{2} y^{2})$
- $- 2 \sqrt{3} \sqrt{x} (x^{3} y + x^{2} y^{2})$
- $- 2 \sqrt{3} (- x^{3} + x^{2} y^{3})$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-1)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 2 \sqrt{3} x^{2} y (- x + y)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 2 \sqrt{3} (- x^{3} y + x^{2} y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_x2yz", "profile": "raw:q-161314", "parameters": {"a": "-1", "b": "1", "k": "-2", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "aaa8d40b-6915-5d7a-8e30-f1124ed01248", "mathematical_fingerprint": "368d7e7690728ec72ef2b240507caf1eff36fb1eb21a284596ef362409f47db4", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161314"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161314 scale 2

Consider the surface integral of the function $f(x,y,z)=2 x^{2} y z,$ where the surface $S$ is defined by $z=-x+y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 4 \sqrt{3} x^{2} y$
- $2 \sqrt{3} \sqrt{y} (- x^{2} y^{2} - x^{2} y)$
- $2 \sqrt{3} (- x^{3} y + x^{2} y^{2})$
- $2 \sqrt{3} \sqrt{x} (x^{3} y + x^{2} y^{2})$
- $2 \sqrt{3} (- x^{3} + x^{2} y^{3})$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-1)}^{2}+{(1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2 \sqrt{3} x^{2} y (- x + y)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,2 \sqrt{3} (- x^{3} y + x^{2} y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_x2yz", "profile": "raw:q-161314", "parameters": {"a": "-1", "b": "1", "k": "2", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "63f714dd-18d4-50d5-9e05-670aef3961ae", "mathematical_fingerprint": "b9d094ded332c571ef559054a8f4b5e28ef9386b42100f116ed2df071018843e", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161314"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161320

Consider the surface integral of the function $f(x,y,z)={x}^{2}{y}^{2}z,$ where the surface $S$ is defined by $z=-{x}^{2}-{y}^{2}$ for $0\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{0}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $(-{x}^{4}{y}^{2}-{x}^{2}{y}^{4})\sqrt{1+4{x}^{2}+4{y}^{2}}$
- $({x}^{4}{y}^{4}+{x}^{4}{y}^{4})\sqrt{1+4{y}^{2}}$
- $({x}^{2}{y}^{2}-{x}^{4}{y}^{4})\sqrt{1+2{x}^{2}+2{y}^{2}}$
- $({y}^{2}-{x}^{2}{y}^{4})\sqrt{4{x}^{2}+4{y}^{2}}$
- $(-{x}^{4}{y}^{2}-4{x}^{4}{y}^{4})\sqrt{1+4x+4y}$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2y2z", "profile": "raw:q-161320", "parameters": {"a": "-1", "b": "-1", "k": "1", "bounds": [0, 1, 0, 1]}, "seed": 0, "content_id": "be9fb803-e741-5d3c-86ce-080d558d5188", "mathematical_fingerprint": "fb621a0db7384ed022fcd7e8846b2f70f8edfc63885891cb57e525f2d3290319", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161320"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161320 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 x^{2} y^{2} z,$ where the surface $S$ is defined by $z=-{x}^{2}-{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 (- x^{4} y^{2} - x^{2} y^{4}) \sqrt{4 x^{2} + 4 y^{2} + 1}$
- $- 4 x^{4} y^{4} \sqrt{4 y^{2} + 1}$
- $- 2 (- 4 x^{4} y^{4} - x^{4} y^{2}) \sqrt{4 x + 4 y + 1}$
- $- 2 \sqrt{4 x^{2} + 4 y^{2}} (- x^{2} y^{4} + y^{2})$
- $- 2 (- x^{4} y^{4} + x^{2} y^{2}) \sqrt{2 x^{2} + 2 y^{2} + 1}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(-2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 2 x^{2} y^{2} (- x^{2} - y^{2}) \sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 2 (- x^{4} y^{2} - x^{2} y^{4}) \sqrt{4 x^{2} + 4 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2y2z", "profile": "raw:q-161320", "parameters": {"a": "-1", "b": "-1", "k": "-2", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "8bc264f6-2429-5601-a4ca-ccf26a473bee", "mathematical_fingerprint": "e53fbc63c73da1a33f33bb9682c65c83915e196d9f1fd90670b2bcaebf913e5a", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161320"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161320 scale 2

Consider the surface integral of the function $f(x,y,z)=2 x^{2} y^{2} z,$ where the surface $S$ is defined by $z=-{x}^{2}-{y}^{2}$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $2 (- x^{4} y^{2} - x^{2} y^{4}) \sqrt{4 x^{2} + 4 y^{2} + 1}$
- $4 x^{4} y^{4} \sqrt{4 y^{2} + 1}$
- $2 (- 4 x^{4} y^{4} - x^{4} y^{2}) \sqrt{4 x + 4 y + 1}$
- $2 \sqrt{4 x^{2} + 4 y^{2}} (- x^{2} y^{4} + y^{2})$
- $2 (- x^{4} y^{4} + x^{2} y^{2}) \sqrt{2 x^{2} + 2 y^{2} + 1}$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-2x)}^{2}+{(-2y)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2 x^{2} y^{2} (- x^{2} - y^{2}) \sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,2 (- x^{4} y^{2} - x^{2} y^{4}) \sqrt{4 x^{2} + 4 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2y2z", "profile": "raw:q-161320", "parameters": {"a": "-1", "b": "-1", "k": "2", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "d9b831c3-6c41-5934-ba03-ed5391cfa68b", "mathematical_fingerprint": "66a2242af9d8cd237229bcdca66cbc5a5e5585b87f372f34dcb96160a4b8614d", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161320"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## ORIGINAL q-161326

Consider the surface integral of the function $f(x,y,z)=\sqrt{2}y,$ where the surface $S$ is defined by $z=-\sqrt{2}x-y$ for $-1\le x\le 0$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{0}{\int }_{0}^{2}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $-4\sqrt{2}{y}^{2}$
- $4\sqrt{2}y$
- $-2\sqrt{2}y$
- $\sqrt{2}y$
- $2\sqrt{2}y$

Worked solution:
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

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_y", "profile": "raw:q-161326", "parameters": {"a": "-sqrt(2)", "b": "-1", "k": "sqrt(2)", "bounds": [-1, 0, 0, 2]}, "seed": 0, "content_id": "8910be8b-01a1-50e4-82a9-5981f95782a4", "mathematical_fingerprint": "767b3d4b23a89680b43d25283eeae47dd12c54ea8fddfb3d2201d1de31d30fb4", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161326"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161326 scale -2

Consider the surface integral of the function $f(x,y,z)=- 2 \sqrt{2} y,$ where the surface $S$ is defined by $z=-\sqrt{2}x-y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $8 \sqrt{2} y^{2}$
- $- 8 \sqrt{2} y$
- $- 4 \sqrt{2} y$
- $- 2 \sqrt{2} y$
- $4 \sqrt{2} y$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,- 4 \sqrt{2} y\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,- 4 \sqrt{2} y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_y", "profile": "raw:q-161326", "parameters": {"a": "-sqrt(2)", "b": "-1", "k": "-2*sqrt(2)", "bounds": [0, 2, -1, 1]}, "seed": -2, "content_id": "8066d79c-6947-5c7f-8ff8-ba65c29d0cae", "mathematical_fingerprint": "b6f271c2844d55bba2a6aae5622d3a85179484afd0ad709ef5924b69246dfc66", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161326"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## RAW PROFILE VARIANT q-161326 scale 2

Consider the surface integral of the function $f(x,y,z)=2 \sqrt{2} y,$ where the surface $S$ is defined by $z=-\sqrt{2}x-y$ for $0\le x\le 2$ and $-1\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{1}\boxed{}\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 8 \sqrt{2} y^{2}$
- $8 \sqrt{2} y$
- $4 \sqrt{2} y$
- $2 \sqrt{2} y$
- $- 4 \sqrt{2} y$

Worked solution:
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
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(-\sqrt{2})}^{2}+{(-1)}^{2}}\,\text{d}A \\  & ={∬}_{D}\,4 \sqrt{2} y\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}\,4 \sqrt{2} y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_y", "profile": "raw:q-161326", "parameters": {"a": "-sqrt(2)", "b": "-1", "k": "2*sqrt(2)", "bounds": [0, 2, -1, 1]}, "seed": 2, "content_id": "d6644c9c-bec4-5863-921c-d9cb171ff65e", "mathematical_fingerprint": "9d101159fc747dacf02ebfe64cb0d8e9a142a5b7e80c4202fe2b1ce4c33248fe", "eligible_for_learning": false, "evidence_only": true, "bank_interpretation": "coefficient-scaled opaque historical expressions", "source_ids": ["q-161326"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_xy seed 31

Consider the surface integral of the function $f(x,y,z)=2 x y,$ where the surface $S$ is defined by $z=2 x^{2} - 2 y^{2}$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{2 x y}{\sqrt{16 x^{2} + 16 y^{2} + 1}}$
- $2 x y \sqrt{16 x^{2} + 16 y^{2} + 1}$
- $2 x y (16 x^{2} + 16 y^{2} + 1)$
- $2 x y$
- $2 x y \sqrt{16 x^{2} + 16 y^{2}}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 y^{2})=4 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 y^{2})=- 4 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x)^2+(- 4 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x y)\cdot (\sqrt{16 x^{2} + 16 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,2 x y \sqrt{16 x^{2} + 16 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_xy", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "a76b9364-0c55-5aa7-aacb-db074cfb6fee", "mathematical_fingerprint": "33b90452879d528562ac72c5192b164cc0bb96a8a366c316bb86c6822402decc", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161106"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_xy seed 72

Consider the surface integral of the function $f(x,y,z)=- x y,$ where the surface $S$ is defined by $z=\sqrt{2} x^{2} - \sqrt{2} y^{2}$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- x y \sqrt{8 x^{2} + 8 y^{2}}$
- $- x y \sqrt{8 x^{2} + 8 y^{2} + 1}$
- $- \frac{x y}{\sqrt{8 x^{2} + 8 y^{2} + 1}}$
- $- x y$
- $- x y (8 x^{2} + 8 y^{2} + 1)$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=2 \sqrt{2} x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=- 2 \sqrt{2} y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2 \sqrt{2} x)^2+(- 2 \sqrt{2} y)^2}\,\text{d}A \\  & ={∬}_{D}\,(- x y)\cdot (\sqrt{8 x^{2} + 8 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,- x y \sqrt{8 x^{2} + 8 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_xy", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "61d2b0cf-71e2-55a9-9578-44a4cccb432e", "mathematical_fingerprint": "6bc093a5dd7028598ba8eb69cfd49d7e211ed3867b83b378324c96dede2e3768", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161106"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xz seed 31

Consider the surface integral of the function $f(x,y,z)=2 x z,$ where the surface $S$ is defined by $z=2 x - 2 y$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{2}}{3} - \frac{4 x y}{3}$
- $12 x^{2} - 12 x y$
- $36 x^{2} - 36 x y$
- $4 x^{2} - 4 x y$
- $2 \sqrt{2} (4 x^{2} - 4 x y)$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2)^2+(-2)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x (2 x - 2 y))\cdot (3)\,\text{d}A \\  & ={∬}_{D}\,(4 x^{2} - 4 x y)\cdot (3)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,12 x^{2} - 12 x y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xz", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "784f8600-adf8-52bf-9e5e-83229e589f10", "mathematical_fingerprint": "abfcc1cf5a7b266f310178429a9a5329a417daa39d3bbb95724d882bedcb46a1", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161323"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xz seed 72

Consider the surface integral of the function $f(x,y,z)=- x z,$ where the surface $S$ is defined by $z=\sqrt{2} x - \sqrt{2} y$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 \sqrt{2} x^{2} + 2 \sqrt{2} x y$
- $\sqrt{5} (- \sqrt{2} x^{2} + \sqrt{2} x y)$
- $\frac{\sqrt{5} (- \sqrt{2} x^{2} + \sqrt{2} x y)}{5}$
- $- \sqrt{2} x^{2} + \sqrt{2} x y$
- $- 5 \sqrt{2} x^{2} + 5 \sqrt{2} x y$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x - \sqrt{2} y)=\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x - \sqrt{2} y)=- \sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(\sqrt{2})^2+(- \sqrt{2})^2}\,\text{d}A \\  & ={∬}_{D}\,(- x (\sqrt{2} x - \sqrt{2} y))\cdot (\sqrt{5})\,\text{d}A \\  & ={∬}_{D}\,(- \sqrt{2} x^{2} + \sqrt{2} x y)\cdot (\sqrt{5})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,\sqrt{5} (- \sqrt{2} x^{2} + \sqrt{2} x y)\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xz", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "0e011b49-814f-5f81-918c-0f4602cf609b", "mathematical_fingerprint": "f6788f4d0cffc8bc3e2da69d9364eef3c30935eb07b09e0d4f981cf62712db33", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161323"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xy_z2 seed 31

Consider the surface integral of the function $f(x,y,z)=2 x y z^{2},$ where the surface $S$ is defined by $z=2 x - 2 y$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{8 x^{3} y}{3} - \frac{16 x^{2} y^{2}}{3} + \frac{8 x y^{3}}{3}$
- $24 x^{3} y - 48 x^{2} y^{2} + 24 x y^{3}$
- $72 x^{3} y - 144 x^{2} y^{2} + 72 x y^{3}$
- $8 x^{3} y - 16 x^{2} y^{2} + 8 x y^{3}$
- $2 \sqrt{2} (8 x^{3} y - 16 x^{2} y^{2} + 8 x y^{3})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2)^2+(-2)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x y (2 x - 2 y)^{2})\cdot (3)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,24 x^{3} y - 48 x^{2} y^{2} + 24 x y^{3}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xy_z2", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "e46c0ad1-0c14-50fb-b4e2-eee62f4906ce", "mathematical_fingerprint": "53dd342b2ae5ba50554b8fd8b4fff60cea851d24f82b326875f5fa4964ae08e1", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161319"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xy_z2 seed 72

Consider the surface integral of the function $f(x,y,z)=- x y z^{2},$ where the surface $S$ is defined by $z=\sqrt{2} x - \sqrt{2} y$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 4 x^{3} y + 8 x^{2} y^{2} - 4 x y^{3}$
- $\sqrt{5} (- 2 x^{3} y + 4 x^{2} y^{2} - 2 x y^{3})$
- $\frac{\sqrt{5} (- 2 x^{3} y + 4 x^{2} y^{2} - 2 x y^{3})}{5}$
- $- 2 x^{3} y + 4 x^{2} y^{2} - 2 x y^{3}$
- $- 10 x^{3} y + 20 x^{2} y^{2} - 10 x y^{3}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x - \sqrt{2} y)=\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x - \sqrt{2} y)=- \sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(\sqrt{2})^2+(- \sqrt{2})^2}\,\text{d}A \\  & ={∬}_{D}\,(- x y (\sqrt{2} x - \sqrt{2} y)^{2})\cdot (\sqrt{5})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,\sqrt{5} (- 2 x^{3} y + 4 x^{2} y^{2} - 2 x y^{3})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xy_z2", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "4605bb01-c32f-5271-be68-4c1d579542bb", "mathematical_fingerprint": "fd3a4213bba3c08b808d37e9d86cee1ed17100c3e2a8d15c8a56a5b1f0f4f783", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161319"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xyz seed 31

Consider the surface integral of the function $f(x,y,z)=2 x y z,$ where the surface $S$ is defined by $z=2 x - 2 y$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{2} y}{3} - \frac{4 x y^{2}}{3}$
- $12 x^{2} y - 12 x y^{2}$
- $36 x^{2} y - 36 x y^{2}$
- $4 x^{2} y - 4 x y^{2}$
- $2 \sqrt{2} (4 x^{2} y - 4 x y^{2})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2)^2+(-2)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x y (2 x - 2 y))\cdot (3)\,\text{d}A \\  & ={∬}_{D}\,(4 x^{2} y - 4 x y^{2})\cdot (3)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,12 x^{2} y - 12 x y^{2}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xyz", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "0faf9d42-46fc-554c-a761-26e052bf638b", "mathematical_fingerprint": "09d0fd3312e39a77c00a6027b1aaa03e54b7b9c9bb881161f0937e0844455eb3", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161321"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_xyz seed 72

Consider the surface integral of the function $f(x,y,z)=- x y z,$ where the surface $S$ is defined by $z=\sqrt{2} x - \sqrt{2} y$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 \sqrt{2} x^{2} y + 2 \sqrt{2} x y^{2}$
- $\sqrt{5} (- \sqrt{2} x^{2} y + \sqrt{2} x y^{2})$
- $\frac{\sqrt{5} (- \sqrt{2} x^{2} y + \sqrt{2} x y^{2})}{5}$
- $- \sqrt{2} x^{2} y + \sqrt{2} x y^{2}$
- $- 5 \sqrt{2} x^{2} y + 5 \sqrt{2} x y^{2}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x - \sqrt{2} y)=\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x - \sqrt{2} y)=- \sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(\sqrt{2})^2+(- \sqrt{2})^2}\,\text{d}A \\  & ={∬}_{D}\,(- x y (\sqrt{2} x - \sqrt{2} y))\cdot (\sqrt{5})\,\text{d}A \\  & ={∬}_{D}\,(- \sqrt{2} x^{2} y + \sqrt{2} x y^{2})\cdot (\sqrt{5})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,\sqrt{5} (- \sqrt{2} x^{2} y + \sqrt{2} x y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_xyz", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "3b85b573-98f4-5905-9e4c-9e5df13865fc", "mathematical_fingerprint": "15a48db515a8e97a169911b8ad562916cea988bd928b0a8e540c0d9ecfe54840", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161321"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_x2_z2 seed 31

Consider the surface integral of the function $f(x,y,z)=2 x^{2} z^{2},$ where the surface $S$ is defined by $z=2 x^{2} - 2 y^{2}$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4}}{\sqrt{16 x^{2} + 16 y^{2} + 1}}$
- $\sqrt{16 x^{2} + 16 y^{2} + 1} (8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4})$
- $(16 x^{2} + 16 y^{2} + 1) (8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4})$
- $8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4}$
- $\sqrt{16 x^{2} + 16 y^{2}} (8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 y^{2})=4 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 y^{2})=- 4 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x)^2+(- 4 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x^{2} (2 x^{2} - 2 y^{2})^{2})\cdot (\sqrt{16 x^{2} + 16 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\sqrt{16 x^{2} + 16 y^{2} + 1} (8 x^{6} - 16 x^{4} y^{2} + 8 x^{2} y^{4})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2_z2", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "e913f58d-4b28-5259-8c0d-76a10fd579d5", "mathematical_fingerprint": "91df744ef2ed73d6940b14504dbdd3ea2478d02a6a1b6b9f03b5fb01251851fa", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161325"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_x2_z2 seed 72

Consider the surface integral of the function $f(x,y,z)=- x^{2} z^{2},$ where the surface $S$ is defined by $z=\sqrt{2} x^{2} - \sqrt{2} y^{2}$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{8 x^{2} + 8 y^{2}} (- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4})$
- $\sqrt{8 x^{2} + 8 y^{2} + 1} (- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4})$
- $\frac{- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4}}{\sqrt{8 x^{2} + 8 y^{2} + 1}}$
- $- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4}$
- $(8 x^{2} + 8 y^{2} + 1) (- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=2 \sqrt{2} x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=- 2 \sqrt{2} y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2 \sqrt{2} x)^2+(- 2 \sqrt{2} y)^2}\,\text{d}A \\  & ={∬}_{D}\,(- x^{2} (\sqrt{2} x^{2} - \sqrt{2} y^{2})^{2})\cdot (\sqrt{8 x^{2} + 8 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,\sqrt{8 x^{2} + 8 y^{2} + 1} (- 2 x^{6} + 4 x^{4} y^{2} - 2 x^{2} y^{4})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2_z2", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "b2e1e7fc-61d1-5742-816b-598eb11510dc", "mathematical_fingerprint": "8290f7a7e2b77d1c9a93e7a5e53b38ab5763e74c2246a98cf4ea45f59f7be5c8", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161325"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_x2yz seed 31

Consider the surface integral of the function $f(x,y,z)=2 x^{2} y z,$ where the surface $S$ is defined by $z=2 x - 2 y$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{3} y}{3} - \frac{4 x^{2} y^{2}}{3}$
- $12 x^{3} y - 12 x^{2} y^{2}$
- $36 x^{3} y - 36 x^{2} y^{2}$
- $4 x^{3} y - 4 x^{2} y^{2}$
- $2 \sqrt{2} (4 x^{3} y - 4 x^{2} y^{2})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2)^2+(-2)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x^{2} y (2 x - 2 y))\cdot (3)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,12 x^{3} y - 12 x^{2} y^{2}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_x2yz", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "6343c8ea-f74a-57bc-97d9-d57b7ed12eba", "mathematical_fingerprint": "ef3d0089ce0c385ad76eb6f46c251b57156b96d775a7aa7ff668c0d01770c6fb", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161314"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_x2yz seed 72

Consider the surface integral of the function $f(x,y,z)=- x^{2} y z,$ where the surface $S$ is defined by $z=\sqrt{2} x - \sqrt{2} y$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 \sqrt{2} x^{3} y + 2 \sqrt{2} x^{2} y^{2}$
- $\sqrt{5} (- \sqrt{2} x^{3} y + \sqrt{2} x^{2} y^{2})$
- $\frac{\sqrt{5} (- \sqrt{2} x^{3} y + \sqrt{2} x^{2} y^{2})}{5}$
- $- \sqrt{2} x^{3} y + \sqrt{2} x^{2} y^{2}$
- $- 5 \sqrt{2} x^{3} y + 5 \sqrt{2} x^{2} y^{2}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x - \sqrt{2} y)=\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x - \sqrt{2} y)=- \sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(\sqrt{2})^2+(- \sqrt{2})^2}\,\text{d}A \\  & ={∬}_{D}\,(- x^{2} y (\sqrt{2} x - \sqrt{2} y))\cdot (\sqrt{5})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,\sqrt{5} (- \sqrt{2} x^{3} y + \sqrt{2} x^{2} y^{2})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_x2yz", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "c6c40fd5-38f0-559a-a371-10699e872e3e", "mathematical_fingerprint": "eb4dbe24f8206730baa0edae617892960103b3b7c30eccf7ad2d5400ec45b6eb", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161314"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_x2y2z seed 31

Consider the surface integral of the function $f(x,y,z)=2 x^{2} y^{2} z,$ where the surface $S$ is defined by $z=2 x^{2} - 2 y^{2}$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{4} y^{2} - 4 x^{2} y^{4}}{\sqrt{16 x^{2} + 16 y^{2} + 1}}$
- $(4 x^{4} y^{2} - 4 x^{2} y^{4}) \sqrt{16 x^{2} + 16 y^{2} + 1}$
- $(4 x^{4} y^{2} - 4 x^{2} y^{4}) (16 x^{2} + 16 y^{2} + 1)$
- $4 x^{4} y^{2} - 4 x^{2} y^{4}$
- $\sqrt{16 x^{2} + 16 y^{2}} (4 x^{4} y^{2} - 4 x^{2} y^{4})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 y^{2})=4 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 y^{2})=- 4 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x)^2+(- 4 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x^{2} y^{2} (2 x^{2} - 2 y^{2}))\cdot (\sqrt{16 x^{2} + 16 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,(4 x^{4} y^{2} - 4 x^{2} y^{4}) \sqrt{16 x^{2} + 16 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2y2z", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "22bbf7b3-2e87-55cb-9833-f4a43b6ec7d1", "mathematical_fingerprint": "272c8ecb3c5ac0c39414e8f3c88d737593d3036e71a583f82b106a981a44764e", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161320"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy quadratic_x2y2z seed 72

Consider the surface integral of the function $f(x,y,z)=- x^{2} y^{2} z,$ where the surface $S$ is defined by $z=\sqrt{2} x^{2} - \sqrt{2} y^{2}$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{8 x^{2} + 8 y^{2}} (- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4})$
- $(- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4}) \sqrt{8 x^{2} + 8 y^{2} + 1}$
- $\frac{- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4}}{\sqrt{8 x^{2} + 8 y^{2} + 1}}$
- $- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4}$
- $(- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4}) (8 x^{2} + 8 y^{2} + 1)$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=2 \sqrt{2} x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x^{2} - \sqrt{2} y^{2})=- 2 \sqrt{2} y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2 \sqrt{2} x)^2+(- 2 \sqrt{2} y)^2}\,\text{d}A \\  & ={∬}_{D}\,(- x^{2} y^{2} (\sqrt{2} x^{2} - \sqrt{2} y^{2}))\cdot (\sqrt{8 x^{2} + 8 y^{2} + 1})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,(- \sqrt{2} x^{4} y^{2} + \sqrt{2} x^{2} y^{4}) \sqrt{8 x^{2} + 8 y^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "quadratic_x2y2z", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "55295ea7-b4c8-57b5-87bd-30bcdd15e42f", "mathematical_fingerprint": "6190480d58d58ecf38b22f9aa5c756834bb6e45fc16b73d4e5b9c9cbbb521df2", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161320"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_y seed 31

Consider the surface integral of the function $f(x,y,z)=2 y,$ where the surface $S$ is defined by $z=2 x - 2 y$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{2 y}{3}$
- $6 y$
- $18 y$
- $2 y$
- $4 \sqrt{2} y$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(2)^2+(-2)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 y)\cdot (3)\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,6 y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_y", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "982c9be9-3478-5fee-b63a-f49c6a3c1c05", "mathematical_fingerprint": "c06e98a3a614fa97f31be13573d60b3878bc0e301e0d06e87b4f2776d345dc03", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161326"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED easy plane_y seed 72

Consider the surface integral of the function $f(x,y,z)=- y,$ where the surface $S$ is defined by $z=\sqrt{2} x - \sqrt{2} y$ for $-1\le x\le 1$ and $0\le y\le 1.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $- 2 y$
- $- \sqrt{5} y$
- $- \frac{\sqrt{5} y}{5}$
- $- y$
- $- 5 y$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sqrt{2} x - \sqrt{2} y)=\sqrt{2},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sqrt{2} x - \sqrt{2} y)=- \sqrt{2}.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(\sqrt{2})^2+(- \sqrt{2})^2}\,\text{d}A \\  & ={∬}_{D}\,(- y)\cdot (\sqrt{5})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}\,- \sqrt{5} y\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "easy", "template": "plane_y", "profile": "measure_conversion", "parameters": {"a": "sqrt(2)", "b": "-sqrt(2)", "k": "-1", "bounds": [-1, 1, 0, 1]}, "seed": 72, "content_id": "3c544a24-5556-585f-85cf-19aba3468e30", "mathematical_fingerprint": "8df47673182dbe940af974c7b9f1ec46dfb4849c1dff8ab1a38183383a4b6553", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": ["q-161326"], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED moderate coupled_xz seed 31

Consider the surface integral of the function $f(x,y,z)=2 x z,$ where the surface $S$ is defined by $z=2 x^{2} - 2 x y - y^{2}$ for $0\le x\le 1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{3} - 4 x^{2} y - 2 x y^{2}}{\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}}$
- $(4 x^{3} - 4 x^{2} y - 2 x y^{2}) \sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}$
- $(4 x^{3} - 4 x^{2} y - 2 x y^{2}) ((- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1)$
- $4 x^{3} - 4 x^{2} y - 2 x y^{2}$
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2}} (4 x^{3} - 4 x^{2} y - 2 x y^{2})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 x y - y^{2})=4 x - 2 y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 x y - y^{2})=- 2 x - 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x - 2 y)^2+(- 2 x - 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x (2 x^{2} - 2 x y - y^{2}))\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(4 x^{3} - 4 x^{2} y - 2 x y^{2})\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-1}^{0}\,(4 x^{3} - 4 x^{2} y - 2 x y^{2}) \sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "moderate", "template": "coupled_xz", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "c": "-1", "bounds": [0, 1, -1, 0]}, "seed": 31, "content_id": "110b824d-3a14-54d9-a818-d0f5c56d3233", "mathematical_fingerprint": "51bc8d0b13ccef3632ef62697c153701975e5b4b13a5261501e6b558cb42f0fd", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED moderate coupled_xz seed 72

Consider the surface integral of the function $f(x,y,z)=x z,$ where the surface $S$ is defined by $z=- x^{2} + x y + y^{2}$ for $0\le x\le 2$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2}} (- x^{3} + x^{2} y + x y^{2})$
- $(- x^{3} + x^{2} y + x y^{2}) \sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}$
- $(- x^{3} + x^{2} y + x y^{2}) ((- 2 x + y)^{2} + (x + 2 y)^{2} + 1)$
- $- x^{3} + x^{2} y + x y^{2}$
- $\frac{- x^{3} + x^{2} y + x y^{2}}{\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(- x^{2} + x y + y^{2})=- 2 x + y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(- x^{2} + x y + y^{2})=x + 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(- 2 x + y)^2+(x + 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(x (- x^{2} + x y + y^{2}))\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- x^{3} + x^{2} y + x y^{2})\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{0}\,(- x^{3} + x^{2} y + x y^{2}) \sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "moderate", "template": "coupled_xz", "profile": "measure_conversion", "parameters": {"a": "-1", "b": "1", "k": "1", "c": "1", "bounds": [0, 2, -1, 0]}, "seed": 72, "content_id": "941608f9-7450-57e0-bee0-5986a809f81c", "mathematical_fingerprint": "f54b9bf1752698a644841fc8d9da27e8bc1587697ec0ce43573aa946feb106a2", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED moderate coupled_yz seed 31

Consider the surface integral of the function $f(x,y,z)=2 y z,$ where the surface $S$ is defined by $z=2 x^{2} - 2 x y - y^{2}$ for $0\le x\le 1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\frac{4 x^{2} y - 4 x y^{2} - 2 y^{3}}{\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}}$
- $(4 x^{2} y - 4 x y^{2} - 2 y^{3}) \sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}$
- $(4 x^{2} y - 4 x y^{2} - 2 y^{3}) ((- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1)$
- $4 x^{2} y - 4 x y^{2} - 2 y^{3}$
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2}} (4 x^{2} y - 4 x y^{2} - 2 y^{3})$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 x y - y^{2})=4 x - 2 y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 x y - y^{2})=- 2 x - 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x - 2 y)^2+(- 2 x - 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 y (2 x^{2} - 2 x y - y^{2}))\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(4 x^{2} y - 4 x y^{2} - 2 y^{3})\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-1}^{0}\,(4 x^{2} y - 4 x y^{2} - 2 y^{3}) \sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "moderate", "template": "coupled_yz", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "c": "-1", "bounds": [0, 1, -1, 0]}, "seed": 31, "content_id": "4d80db13-8f5e-5c4a-b166-fd566e1b48bb", "mathematical_fingerprint": "403e133fa33205497d13579d457587b11e39adb8b47a17bf6d6b4c3251a970d8", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED moderate coupled_yz seed 72

Consider the surface integral of the function $f(x,y,z)=y z,$ where the surface $S$ is defined by $z=- x^{2} + x y + y^{2}$ for $0\le x\le 2$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{2}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2}} (- x^{2} y + x y^{2} + y^{3})$
- $(- x^{2} y + x y^{2} + y^{3}) \sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}$
- $(- x^{2} y + x y^{2} + y^{3}) ((- 2 x + y)^{2} + (x + 2 y)^{2} + 1)$
- $- x^{2} y + x y^{2} + y^{3}$
- $\frac{- x^{2} y + x y^{2} + y^{3}}{\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(- x^{2} + x y + y^{2})=- 2 x + y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(- x^{2} + x y + y^{2})=x + 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(- 2 x + y)^2+(x + 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(y (- x^{2} + x y + y^{2}))\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- x^{2} y + x y^{2} + y^{3})\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{0}\,(- x^{2} y + x y^{2} + y^{3}) \sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "moderate", "template": "coupled_yz", "profile": "measure_conversion", "parameters": {"a": "-1", "b": "1", "k": "1", "c": "1", "bounds": [0, 2, -1, 0]}, "seed": 72, "content_id": "b742bb81-28c4-592d-abea-8f6628e0aba4", "mathematical_fingerprint": "e8cb8d33d639498c087a53d53d14685d1ea227c627f0cac7bde6d0ff2c338d9e", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED hard coupled_two_x seed 31

Consider the surface integral of the function $f(x,y,z)=2 x z - 2 y z^{2},$ where the surface $S$ is defined by $z=2 x^{2} - 2 x y - y^{2}$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2}} (- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5})$
- $\frac{- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5}}{\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}}$
- $((- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1) (- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5})$
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1} (- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5})$
- $- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 x y - y^{2})=4 x - 2 y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 x y - y^{2})=- 2 x - 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x - 2 y)^2+(- 2 x - 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(2 x (2 x^{2} - 2 x y - y^{2}) - 2 y (2 x^{2} - 2 x y - y^{2})^{2})\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5})\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1} (- 8 x^{4} y + 16 x^{3} y^{2} + 4 x^{3} - 4 x^{2} y - 8 x y^{4} - 2 x y^{2} - 2 y^{5})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "hard", "template": "coupled_two_x", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "c": "-1", "l": "-2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "cb84707d-0995-5613-b587-fc810992ee55", "mathematical_fingerprint": "0cd391e45f4b91b06fdd06ef7a1ea477b202390a420db40cef5f148b8e36381a", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED hard coupled_two_x seed 72

Consider the surface integral of the function $f(x,y,z)=x z - y z^{2},$ where the surface $S$ is defined by $z=- x^{2} + x y + y^{2}$ for $0\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{0}^{2}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2}} (- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5})$
- $\frac{- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5}}{\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}}$
- $((- 2 x + y)^{2} + (x + 2 y)^{2} + 1) (- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5})$
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1} (- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5})$
- $- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(- x^{2} + x y + y^{2})=- 2 x + y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(- x^{2} + x y + y^{2})=x + 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(- 2 x + y)^2+(x + 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(x (- x^{2} + x y + y^{2}) - y (- x^{2} + x y + y^{2})^{2})\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5})\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{2}\,\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1} (- x^{4} y + 2 x^{3} y^{2} - x^{3} + x^{2} y^{3} + x^{2} y - 2 x y^{4} + x y^{2} - y^{5})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "hard", "template": "coupled_two_x", "profile": "measure_conversion", "parameters": {"a": "-1", "b": "1", "k": "1", "c": "1", "l": "-1", "bounds": [0, 1, 0, 2]}, "seed": 72, "content_id": "18482e65-29dd-5bec-993e-3ee84b59a71a", "mathematical_fingerprint": "b4b9c44b288b5dfb32311627cbdb01e898960ada7fee030553b5deff20e46a5a", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED hard coupled_two_y seed 31

Consider the surface integral of the function $f(x,y,z)=- 2 x z^{2} + 2 y z,$ where the surface $S$ is defined by $z=2 x^{2} - 2 x y - y^{2}$ for $-2\le x\le -1$ and $-1\le y\le 0.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2}} (- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3})$
- $\frac{- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3}}{\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1}}$
- $((- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1) (- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3})$
- $\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1} (- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3})$
- $- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x^{2} - 2 x y - y^{2})=4 x - 2 y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x^{2} - 2 x y - y^{2})=- 2 x - 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(4 x - 2 y)^2+(- 2 x - 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(- 2 x (2 x^{2} - 2 x y - y^{2})^{2} + 2 y (2 x^{2} - 2 x y - y^{2}))\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3})\cdot (\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{-2}^{-1}{\int }_{-1}^{0}\,\sqrt{(- 2 x - 2 y)^{2} + (4 x - 2 y)^{2} + 1} (- 8 x^{5} + 16 x^{4} y - 8 x^{2} y^{3} + 4 x^{2} y - 2 x y^{4} - 4 x y^{2} - 2 y^{3})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "hard", "template": "coupled_two_y", "profile": "measure_conversion", "parameters": {"a": "2", "b": "-2", "k": "2", "c": "-1", "l": "-2", "bounds": [-2, -1, -1, 0]}, "seed": 31, "content_id": "e3cdbea9-2285-5821-bd53-eebfb525a2a7", "mathematical_fingerprint": "9afa1b25305f0a5a6bd809c3fcafb64c761e96757e865b691a9d98ffedaf6849", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}

---

## GENERATED hard coupled_two_y seed 72

Consider the surface integral of the function $f(x,y,z)=- x z^{2} + y z,$ where the surface $S$ is defined by $z=- x^{2} + x y + y^{2}$ for $0\le x\le 1$ and $0\le y\le 2.$
This surface integral can be written as a repeated integral, as shown below. 

$$
{∬}_{S}f(x,y,z)\,\text{d}S={\int }_{0}^{1}{\int }_{0}^{2}\,\boxed{}\,\,\text{d}y\,\text{d}x
$$

What is the missing expression?

Choices:
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2}} (- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3})$
- $\frac{- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3}}{\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1}}$
- $((- 2 x + y)^{2} + (x + 2 y)^{2} + 1) (- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3})$
- $\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1} (- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3})$
- $- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3}$

Worked solution:
For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(- x^{2} + x y + y^{2})=- 2 x + y,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(- x^{2} + x y + y^{2})=x + 2 y.
$$

Therefore, the surface integral can be written as 

$$
\begin{aligned}{∬}_{S}f(x,y,z)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+(- 2 x + y)^2+(x + 2 y)^2}\,\text{d}A \\  & ={∬}_{D}\,(- x (- x^{2} + x y + y^{2})^{2} + y (- x^{2} + x y + y^{2}))\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={∬}_{D}\,(- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3})\cdot (\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{2}\,\sqrt{(- 2 x + y)^{2} + (x + 2 y)^{2} + 1} (- x^{5} + 2 x^{4} y + x^{3} y^{2} - 2 x^{2} y^{3} - x^{2} y - x y^{4} + x y^{2} + y^{3})\,\,\text{d}y\,\text{d}x.\end{aligned}
$$

Review metadata: {"version": "cartesian-surface-setup-1", "level": "hard", "template": "coupled_two_y", "profile": "measure_conversion", "parameters": {"a": "-1", "b": "1", "k": "1", "c": "1", "l": "-1", "bounds": [0, 1, 0, 2]}, "seed": 72, "content_id": "3dee1d55-54a9-5aa4-a700-a1a9b2b16fd0", "mathematical_fingerprint": "a3c58a4548ab1d17254482e988d81115e71a8a6c698356919242c3321bb02d2d", "eligible_for_learning": true, "evidence_only": false, "bank_interpretation": "complete method-derived dS conversion bank", "source_ids": [], "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "domains": "real polynomial surface on ordered rectangle; positive metric factor", "dependencies": {"python": "3.13.5", "sympy": "1.14.0"}}