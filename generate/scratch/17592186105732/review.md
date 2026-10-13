# Original and generated review

Raw originals are followed by parameterized replay; changed-source-pattern profiles have explicit interpretation limits. Hard examples are authored given-vector tasks. No plots.

## Original q-19983

Calculate the area of the triangle spanned by $a=⟨1,3,2⟩$ and $b=⟨4,1,-2⟩.$

- $\frac{\sqrt{273}}{2}$
- $\frac{\sqrt{285}}{2}$ (source correct)
- $\frac{\sqrt{825}}{2}$
- $\sqrt{177}$
- $\frac{\sqrt{582}}{2}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 3 & 2 \\ 4 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -2\end{aligned}|i-|\begin{aligned}1 & 2 \\ 4 & -2\end{aligned}|j+|\begin{aligned}1 & 3 \\ 4 & 1\end{aligned}|k \\  & =(3\cdot (-2)-1\cdot 2)i-(1\cdot (-2)-4\cdot 2)j+(1\cdot 1-4\cdot 3)k \\  & =-8i+10j-11k \\  & =⟨-8,10,-11⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{(-8)^{2}+{10}^{2}+(-11)^{2}} \\  & =\sqrt{285}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{285}}{2}.
$$

### Parameterized replay

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $a=⟨1,3,2⟩$ and $b=⟨4,1,-2⟩.$

- $\frac{5\sqrt{33}}{2}$
- $\frac{\sqrt{285}}{2}$ (correct)
- $\frac{\sqrt{273}}{2}$
- $\frac{\sqrt{582}}{2}$
- $\sqrt{177}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 3 & 2 \\ 4 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -2\end{aligned}|i-|\begin{aligned}1 & 2 \\ 4 & -2\end{aligned}|j+|\begin{aligned}1 & 3 \\ 4 & 1\end{aligned}|k \\  & =(3\cdot (-2)-1\cdot 2)i-(1\cdot (-2)-4\cdot 2)j+(1\cdot 1-4\cdot 3)k \\  & =-8i+10j-11k \\  & =⟨-8,10,-11⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{(-8)^{2}+{10}^{2}+(-11)^{2}} \\  & =\sqrt{285}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{285}}{2}.
$$

---

### Changed-parameter observed-pattern replay (q-19983, scaling-only scope)

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $a=⟨-2,-6,-4⟩$ and $b=⟨4,1,-2⟩.$

- $5\sqrt{33}$
- $\sqrt{285}$ (correct)
- $\sqrt{273}$
- $\sqrt{582}$
- $2\sqrt{177}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2 & -6 & -4 \\ 4 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}-6 & -4 \\ 1 & -2\end{aligned}|i-|\begin{aligned}-2 & -4 \\ 4 & -2\end{aligned}|j+|\begin{aligned}-2 & -6 \\ 4 & 1\end{aligned}|k \\  & =((-6)\cdot (-2)-1\cdot (-4))i-((-2)\cdot (-2)-4\cdot (-4))j+((-2)\cdot 1-4\cdot (-6))k \\  & =16i-20j+22k \\  & =⟨16,-20,22⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{16}^{2}+(-20)^{2}+{22}^{2}} \\  & =\sqrt{1140}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{285}}{2}=\sqrt{285}.
$$

---

### Changed-parameter observed-pattern replay (q-19983, scaling-only scope)

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $a=⟨3,9,6⟩$ and $b=⟨4,1,-2⟩.$

- $\frac{15\sqrt{33}}{2}$
- $\frac{3\sqrt{285}}{2}$ (correct)
- $\frac{3\sqrt{273}}{2}$
- $\frac{3\sqrt{582}}{2}$
- $3\sqrt{177}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 3 & 9 & 6 \\ 4 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}9 & 6 \\ 1 & -2\end{aligned}|i-|\begin{aligned}3 & 6 \\ 4 & -2\end{aligned}|j+|\begin{aligned}3 & 9 \\ 4 & 1\end{aligned}|k \\  & =(9\cdot (-2)-1\cdot 6)i-(3\cdot (-2)-4\cdot 6)j+(3\cdot 1-4\cdot 9)k \\  & =-24i+30j-33k \\  & =⟨-24,30,-33⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{(-24)^{2}+{30}^{2}+(-33)^{2}} \\  & =\sqrt{2565}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{285}}{2}.
$$

---

## Original q-20003

Calculate the area of the parallelogram spanned by $a = ⟨ - 2,-3,-1⟩$ and $b = ⟨1, 2, 1⟩$.

- $\frac{3\sqrt{3}}{2}$
- $\frac{\sqrt{3}}{2}$
- $\frac{\sqrt{2}}{2}$
- $\frac{3\sqrt{2}}{2}$
- $\sqrt{3}$

No source solution or designation; inferred cross product (-1,1,-1) gives sqrt(3).

### Parameterized replay

## Generated easy — parallelogram_radio_unrated

Calculate the area of the parallelogram spanned by $a = ⟨ - 2,-3,-1⟩$ and $b = ⟨1, 2, 1⟩$.

- $\frac{\sqrt{2}}{2}$
- $\frac{\sqrt{3}}{2}$
- $\frac{3\sqrt{3}}{2}$
- $\sqrt{3}$ (correct)
- $\frac{3\sqrt{2}}{2}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2 & -3 & -1 \\ 1 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}-3 & -1 \\ 2 & 1\end{aligned}|i-|\begin{aligned}-2 & -1 \\ 1 & 1\end{aligned}|j+|\begin{aligned}-2 & -3 \\ 1 & 2\end{aligned}|k \\  & =((-3)\cdot 1-(-1)\cdot 2)i-((-2)\cdot 1-(-1)\cdot 1)j+((-2)\cdot 2-(-3)\cdot 1)k \\  & =-i+j-k \\  & =⟨-1,1,-1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{(-1)^{2}+{1}^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-20003, scaling-only scope)

## Generated easy — parallelogram_radio_unrated

Calculate the area of the parallelogram spanned by $a = ⟨ 4,6,2⟩$ and $b = ⟨1, 2, 1⟩$.

- $\sqrt{2}$
- $\sqrt{3}$
- $3\sqrt{3}$
- $2\sqrt{3}$ (correct)
- $3\sqrt{2}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 6 & 2 \\ 1 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}6 & 2 \\ 2 & 1\end{aligned}|i-|\begin{aligned}4 & 2 \\ 1 & 1\end{aligned}|j+|\begin{aligned}4 & 6 \\ 1 & 2\end{aligned}|k \\  & =(6\cdot 1-2\cdot 2)i-(4\cdot 1-2\cdot 1)j+(4\cdot 2-6\cdot 1)k \\  & =2i-2j+2k \\  & =⟨2,-2,2⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{2}^{2}} \\  & =\sqrt{12}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-20003, scaling-only scope)

## Generated easy — parallelogram_radio_unrated

Calculate the area of the parallelogram spanned by $a = ⟨ - 6,-9,-3⟩$ and $b = ⟨1, 2, 1⟩$.

- $\frac{3\sqrt{2}}{2}$
- $\frac{3\sqrt{3}}{2}$
- $\frac{9\sqrt{3}}{2}$
- $3\sqrt{3}$ (correct)
- $\frac{9\sqrt{2}}{2}$

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -6 & -9 & -3 \\ 1 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}-9 & -3 \\ 2 & 1\end{aligned}|i-|\begin{aligned}-6 & -3 \\ 1 & 1\end{aligned}|j+|\begin{aligned}-6 & -9 \\ 1 & 2\end{aligned}|k \\  & =((-9)\cdot 1-(-3)\cdot 2)i-((-6)\cdot 1-(-3)\cdot 1)j+((-6)\cdot 2-(-9)\cdot 1)k \\  & =-3i+3j-3k \\  & =⟨-3,3,-3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{(-3)^{2}+{3}^{2}+(-3)^{2}} \\  & =\sqrt{27}.\end{aligned}
$$

---

## Original q-18580

Calculate the area of the triangle spanned by $r=⟨1,-2,3⟩$ and $t=⟨0,1,-2⟩.$

- $\sqrt{6}$
- $\frac{\sqrt{3}}{2}$
- $\frac{\sqrt{6}}{2}$ (source correct)
- $2\sqrt{3}$
- $2\sqrt{6}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ 1 & -2 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -2\end{aligned}|i-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|j+|\begin{aligned}1 & -2 \\ 0 & 1\end{aligned}|k \\  & =((-2)\cdot (-2)-3\cdot 1)i-(1\cdot (-2)-3\cdot 0)j+(1\cdot 1-(-2)\cdot 0)k \\  & =i+2j+k \\  & =⟨1,2,1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{{1}^{2}+{2}^{2}+{1}^{2}} \\  & =\sqrt{6}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{6}}{2}.
$$

### Parameterized replay

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $r=⟨1,-2,3⟩$ and $t=⟨0,1,-2⟩.$

- $\frac{\sqrt{6}}{2}$ (correct)
- $\frac{\sqrt{3}}{2}$
- $\sqrt{6}$
- $2\sqrt{6}$
- $2\sqrt{3}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ 1 & -2 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -2\end{aligned}|i-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|j+|\begin{aligned}1 & -2 \\ 0 & 1\end{aligned}|k \\  & =((-2)\cdot (-2)-3\cdot 1)i-(1\cdot (-2)-3\cdot 0)j+(1\cdot 1-(-2)\cdot 0)k \\  & =i+2j+k \\  & =⟨1,2,1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{{1}^{2}+{2}^{2}+{1}^{2}} \\  & =\sqrt{6}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{6}}{2}.
$$

---

### Changed-parameter observed-pattern replay (q-18580, scaling-only scope)

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $r=⟨-2,4,-6⟩$ and $t=⟨0,1,-2⟩.$

- $\sqrt{6}$ (correct)
- $\sqrt{3}$
- $2\sqrt{6}$
- $4\sqrt{6}$
- $4\sqrt{3}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -2 & 4 & -6 \\ 0 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}4 & -6 \\ 1 & -2\end{aligned}|i-|\begin{aligned}-2 & -6 \\ 0 & -2\end{aligned}|j+|\begin{aligned}-2 & 4 \\ 0 & 1\end{aligned}|k \\  & =(4\cdot (-2)-(-6)\cdot 1)i-((-2)\cdot (-2)-(-6)\cdot 0)j+((-2)\cdot 1-4\cdot 0)k \\  & =-2i-4j-2k \\  & =⟨-2,-4,-2⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-2)^{2}+(-4)^{2}+(-2)^{2}} \\  & =\sqrt{24}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{6}}{2}=\sqrt{6}.
$$

---

### Changed-parameter observed-pattern replay (q-18580, scaling-only scope)

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $r=⟨3,-6,9⟩$ and $t=⟨0,1,-2⟩.$

- $\frac{3\sqrt{6}}{2}$ (correct)
- $\frac{3\sqrt{3}}{2}$
- $3\sqrt{6}$
- $6\sqrt{6}$
- $6\sqrt{3}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ 3 & -6 & 9 \\ 0 & 1 & -2\end{aligned}| \\  & =|\begin{aligned}-6 & 9 \\ 1 & -2\end{aligned}|i-|\begin{aligned}3 & 9 \\ 0 & -2\end{aligned}|j+|\begin{aligned}3 & -6 \\ 0 & 1\end{aligned}|k \\  & =((-6)\cdot (-2)-9\cdot 1)i-(3\cdot (-2)-9\cdot 0)j+(3\cdot 1-(-6)\cdot 0)k \\  & =3i+6j+3k \\  & =⟨3,6,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{{3}^{2}+{6}^{2}+{3}^{2}} \\  & =\sqrt{54}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{6}}{2}.
$$

---

## Original q-19981

Calculate the area of the parallelogram spanned by $u=⟨2,1,-1⟩$ and $v=⟨1,2,0⟩.$

- $\frac{\sqrt{14}}{2}$
- $\frac{\sqrt{14}}{3}$
- $\sqrt{14}$ (source correct)
- $\sqrt{7}$
- $\frac{\sqrt{7}}{2}$

Using the formula, we have

$$
\begin{aligned}u\times v & =|\begin{aligned}i & j & k \\ 2 & 1 & -1 \\ 1 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}1 & -1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}2 & -1 \\ 1 & 0\end{aligned}|j+|\begin{aligned}2 & 1 \\ 1 & 2\end{aligned}|k \\  & =(1\cdot 0-2\cdot (-1))i-(2\cdot 0-1\cdot (-1))j+(2\cdot 2-1\cdot 1)k \\  & =2i-j+3k \\  & =⟨2,-1,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,u\times v\,| \\  & =\sqrt{{2}^{2}+(-1)^{2}+{3}^{2}} \\  & =\sqrt{14}.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_radio_radical

Calculate the area of the parallelogram spanned by $u=⟨2,1,-1⟩$ and $v=⟨1,2,0⟩.$

- $\sqrt{14}$ (correct)
- $\frac{\sqrt{14}}{3}$
- $\frac{\sqrt{14}}{2}$
- $\frac{\sqrt{7}}{2}$
- $\sqrt{7}$

Using the formula, we have

$$
\begin{aligned}u\times v & =|\begin{aligned}i & j & k \\ 2 & 1 & -1 \\ 1 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}1 & -1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}2 & -1 \\ 1 & 0\end{aligned}|j+|\begin{aligned}2 & 1 \\ 1 & 2\end{aligned}|k \\  & =(1\cdot 0-2\cdot (-1))i-(2\cdot 0-1\cdot (-1))j+(2\cdot 2-1\cdot 1)k \\  & =2i-j+3k \\  & =⟨2,-1,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,u\times v\,| \\  & =\sqrt{{2}^{2}+(-1)^{2}+{3}^{2}} \\  & =\sqrt{14}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-19981, scaling-only scope)

## Generated easy — parallelogram_radio_radical

Calculate the area of the parallelogram spanned by $u=⟨-4,-2,2⟩$ and $v=⟨1,2,0⟩.$

- $2\sqrt{14}$ (correct)
- $\frac{2\sqrt{14}}{3}$
- $\sqrt{14}$
- $\sqrt{7}$
- $2\sqrt{7}$

Using the formula, we have

$$
\begin{aligned}u\times v & =|\begin{aligned}i & j & k \\ -4 & -2 & 2 \\ 1 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}-2 & 2 \\ 2 & 0\end{aligned}|i-|\begin{aligned}-4 & 2 \\ 1 & 0\end{aligned}|j+|\begin{aligned}-4 & -2 \\ 1 & 2\end{aligned}|k \\  & =((-2)\cdot 0-2\cdot 2)i-((-4)\cdot 0-1\cdot 2)j+((-4)\cdot 2-1\cdot (-2))k \\  & =-4i+2j-6k \\  & =⟨-4,2,-6⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,u\times v\,| \\  & =\sqrt{(-4)^{2}+{2}^{2}+(-6)^{2}} \\  & =\sqrt{56}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-19981, scaling-only scope)

## Generated easy — parallelogram_radio_radical

Calculate the area of the parallelogram spanned by $u=⟨6,3,-3⟩$ and $v=⟨1,2,0⟩.$

- $3\sqrt{14}$ (correct)
- $\sqrt{14}$
- $\frac{3\sqrt{14}}{2}$
- $\frac{3\sqrt{7}}{2}$
- $3\sqrt{7}$

Using the formula, we have

$$
\begin{aligned}u\times v & =|\begin{aligned}i & j & k \\ 6 & 3 & -3 \\ 1 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}3 & -3 \\ 2 & 0\end{aligned}|i-|\begin{aligned}6 & -3 \\ 1 & 0\end{aligned}|j+|\begin{aligned}6 & 3 \\ 1 & 2\end{aligned}|k \\  & =(3\cdot 0-2\cdot (-3))i-(6\cdot 0-1\cdot (-3))j+(6\cdot 2-1\cdot 3)k \\  & =6i-3j+9k \\  & =⟨6,-3,9⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,u\times v\,| \\  & =\sqrt{{6}^{2}+(-3)^{2}+{9}^{2}} \\  & =\sqrt{126}.\end{aligned}
$$

---

## Original q-19997

Calculate the area of the parallelogram spanned by $f=⟨1,1,-2⟩$ and $g=⟨3,2,1⟩.$

- $3\sqrt{3}$
- $3\sqrt{5}$
- $\frac{2\sqrt{5}}{3}$
- $\frac{5\sqrt{3}}{2}$
- $5\sqrt{3}$ (source correct)

Using the formula, we have

$$
\begin{aligned}f\times g & =|\begin{aligned}i & j & k \\ 1 & 1 & -2 \\ 3 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}1 & -2 \\ 2 & 1\end{aligned}|i-|\begin{aligned}1 & -2 \\ 3 & 1\end{aligned}|j+|\begin{aligned}1 & 1 \\ 3 & 2\end{aligned}|k \\  & =(1\cdot 1-2\cdot (-2))i-(1\cdot 1-3\cdot (-2))j+(1\cdot 2-3\cdot 1)k \\  & =5i-7j-k \\  & =⟨5,-7,-1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,f\times g\,| \\  & =\sqrt{{5}^{2}+(-7)^{2}+(-1)^{2}} \\  & =\sqrt{75} \\  & =5\sqrt{3}.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $f=⟨1,1,-2⟩$ and $g=⟨3,2,1⟩.$

- $\frac{2\sqrt{5}}{3}$
- $3\sqrt{5}$
- $3\sqrt{3}$
- $5\sqrt{3}$ (correct)
- $\frac{5\sqrt{3}}{2}$

Using the formula, we have

$$
\begin{aligned}f\times g & =|\begin{aligned}i & j & k \\ 1 & 1 & -2 \\ 3 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}1 & -2 \\ 2 & 1\end{aligned}|i-|\begin{aligned}1 & -2 \\ 3 & 1\end{aligned}|j+|\begin{aligned}1 & 1 \\ 3 & 2\end{aligned}|k \\  & =(1\cdot 1-2\cdot (-2))i-(1\cdot 1-3\cdot (-2))j+(1\cdot 2-3\cdot 1)k \\  & =5i-7j-k \\  & =⟨5,-7,-1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,f\times g\,| \\  & =\sqrt{{5}^{2}+(-7)^{2}+(-1)^{2}} \\  & =\sqrt{75} \\  & =5\sqrt{3}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-19997, scaling-only scope)

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $f=⟨-2,-2,4⟩$ and $g=⟨3,2,1⟩.$

- $\frac{4\sqrt{5}}{3}$
- $6\sqrt{5}$
- $6\sqrt{3}$
- $10\sqrt{3}$ (correct)
- $5\sqrt{3}$

Using the formula, we have

$$
\begin{aligned}f\times g & =|\begin{aligned}i & j & k \\ -2 & -2 & 4 \\ 3 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}-2 & 4 \\ 2 & 1\end{aligned}|i-|\begin{aligned}-2 & 4 \\ 3 & 1\end{aligned}|j+|\begin{aligned}-2 & -2 \\ 3 & 2\end{aligned}|k \\  & =((-2)\cdot 1-2\cdot 4)i-((-2)\cdot 1-3\cdot 4)j+((-2)\cdot 2-3\cdot (-2))k \\  & =-10i+14j+2k \\  & =⟨-10,14,2⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,f\times g\,| \\  & =\sqrt{(-10)^{2}+{14}^{2}+{2}^{2}} \\  & =\sqrt{300} \\  & =10\sqrt{3}.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-19997, scaling-only scope)

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $f=⟨3,3,-6⟩$ and $g=⟨3,2,1⟩.$

- $2\sqrt{5}$
- $9\sqrt{5}$
- $9\sqrt{3}$
- $15\sqrt{3}$ (correct)
- $\frac{15\sqrt{3}}{2}$

Using the formula, we have

$$
\begin{aligned}f\times g & =|\begin{aligned}i & j & k \\ 3 & 3 & -6 \\ 3 & 2 & 1\end{aligned}| \\  & =|\begin{aligned}3 & -6 \\ 2 & 1\end{aligned}|i-|\begin{aligned}3 & -6 \\ 3 & 1\end{aligned}|j+|\begin{aligned}3 & 3 \\ 3 & 2\end{aligned}|k \\  & =(3\cdot 1-2\cdot (-6))i-(3\cdot 1-3\cdot (-6))j+(3\cdot 2-3\cdot 3)k \\  & =15i-21j-3k \\  & =⟨15,-21,-3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,f\times g\,| \\  & =\sqrt{{15}^{2}+(-21)^{2}+(-3)^{2}} \\  & =\sqrt{675} \\  & =15\sqrt{3}.\end{aligned}
$$

---

## Original q-20004

Calculate the area of the parallelogram spanned by $h=⟨2,0,3⟩$ and $l=⟨4,1,3⟩.$

- $\frac{\sqrt{3}}{2}$
- $\frac{\sqrt{2}}{2}$
- $\frac{7}{2}$
- $5$
- $7$ (source correct)

Using the formula, we have

$$
\begin{aligned}h\times l & =|\begin{aligned}i & j & k \\ 2 & 0 & 3 \\ 4 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}0 & 3 \\ 1 & 3\end{aligned}|i-|\begin{aligned}2 & 3 \\ 4 & 3\end{aligned}|j+|\begin{aligned}2 & 0 \\ 4 & 1\end{aligned}|k \\  & =(0\cdot 3-1\cdot 3)i-(2\cdot 3-4\cdot 3)j+(2\cdot 1-4\cdot 0)k \\  & =-3i+6j+2k \\  & =⟨-3,6,2⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,h\times l\,| \\  & =\sqrt{(-3)^{2}+{6}^{2}+{2}^{2}} \\  & =\sqrt{49} \\  & =7.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $h=⟨2,0,3⟩$ and $l=⟨4,1,3⟩.$

- $\frac{7}{2}$
- $\frac{\sqrt{2}}{2}$
- $\frac{\sqrt{3}}{2}$
- $7$ (correct)
- $5$

Using the formula, we have

$$
\begin{aligned}h\times l & =|\begin{aligned}i & j & k \\ 2 & 0 & 3 \\ 4 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}0 & 3 \\ 1 & 3\end{aligned}|i-|\begin{aligned}2 & 3 \\ 4 & 3\end{aligned}|j+|\begin{aligned}2 & 0 \\ 4 & 1\end{aligned}|k \\  & =(0\cdot 3-1\cdot 3)i-(2\cdot 3-4\cdot 3)j+(2\cdot 1-4\cdot 0)k \\  & =-3i+6j+2k \\  & =⟨-3,6,2⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,h\times l\,| \\  & =\sqrt{(-3)^{2}+{6}^{2}+{2}^{2}} \\  & =\sqrt{49} \\  & =7.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-20004, scaling-only scope)

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $h=⟨-4,0,-6⟩$ and $l=⟨4,1,3⟩.$

- $7$
- $\sqrt{2}$
- $\sqrt{3}$
- $14$ (correct)
- $10$

Using the formula, we have

$$
\begin{aligned}h\times l & =|\begin{aligned}i & j & k \\ -4 & 0 & -6 \\ 4 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}0 & -6 \\ 1 & 3\end{aligned}|i-|\begin{aligned}-4 & -6 \\ 4 & 3\end{aligned}|j+|\begin{aligned}-4 & 0 \\ 4 & 1\end{aligned}|k \\  & =(0\cdot 3-1\cdot (-6))i-((-4)\cdot 3-4\cdot (-6))j+((-4)\cdot 1-4\cdot 0)k \\  & =6i-12j-4k \\  & =⟨6,-12,-4⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,h\times l\,| \\  & =\sqrt{{6}^{2}+(-12)^{2}+(-4)^{2}} \\  & =\sqrt{196} \\  & =14.\end{aligned}
$$

---

### Changed-parameter observed-pattern replay (q-20004, scaling-only scope)

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $h=⟨6,0,9⟩$ and $l=⟨4,1,3⟩.$

- $\frac{21}{2}$
- $\frac{3\sqrt{2}}{2}$
- $\frac{3\sqrt{3}}{2}$
- $21$ (correct)
- $15$

Using the formula, we have

$$
\begin{aligned}h\times l & =|\begin{aligned}i & j & k \\ 6 & 0 & 9 \\ 4 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}0 & 9 \\ 1 & 3\end{aligned}|i-|\begin{aligned}6 & 9 \\ 4 & 3\end{aligned}|j+|\begin{aligned}6 & 0 \\ 4 & 1\end{aligned}|k \\  & =(0\cdot 3-1\cdot 9)i-(6\cdot 3-4\cdot 9)j+(6\cdot 1-4\cdot 0)k \\  & =-9i+18j+6k \\  & =⟨-9,18,6⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,h\times l\,| \\  & =\sqrt{(-9)^{2}+{18}^{2}+{6}^{2}} \\  & =\sqrt{441} \\  & =21.\end{aligned}
$$

---

## Original q-275220

Calculate the area $A$ of the parallelogram spanned by $a=⟨-4,-2,1⟩$ and $b=⟨0,-2,-1⟩.$

$A=${{field-1}}

- $4\sqrt{6}$ (source correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -4 & -2 & 1 \\ 0 & -2 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ -2 & -1\end{aligned}|i-|\begin{aligned}-4 & 1 \\ 0 & -1\end{aligned}|j+|\begin{aligned}-4 & -2 \\ 0 & -2\end{aligned}|k \\  & =((-2)\cdot (-1)-(-2)\cdot 1)i-((-4)\cdot (-1)-0\cdot 1)j+((-4)\cdot (-2)-0\cdot (-2))k \\  & =4i-4j+8k \\  & =⟨4,-4,8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{4}^{2}+(-4)^{2}+{8}^{2}} \\  & =4\sqrt{6}.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_blank_direct

Calculate the area $A$ of the parallelogram spanned by $a=⟨-4,-2,1⟩$ and $b=⟨0,-2,-1⟩.$

$A=${{field-1}}

- $4\sqrt{6}$ (correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -4 & -2 & 1 \\ 0 & -2 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ -2 & -1\end{aligned}|i-|\begin{aligned}-4 & 1 \\ 0 & -1\end{aligned}|j+|\begin{aligned}-4 & -2 \\ 0 & -2\end{aligned}|k \\  & =((-2)\cdot (-1)-(-2)\cdot 1)i-((-4)\cdot (-1)-0\cdot 1)j+((-4)\cdot (-2)-0\cdot (-2))k \\  & =4i-4j+8k \\  & =⟨4,-4,8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{4}^{2}+(-4)^{2}+{8}^{2}} \\  & =4\sqrt{6}.\end{aligned}
$$

---

## Original q-275222

Calculate the area ${A}_{△}$ of the triangle spanned by $a=⟨-2,-1,0⟩$ and $b=⟨-4,2,-2⟩.$

${A}_{△}=${{field-1}}

- $\sqrt{21}$ (source correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2 & -1 & 0 \\ -4 & 2 & -2\end{aligned}| \\  & =|\begin{aligned}-1 & 0 \\ 2 & -2\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -4 & -2\end{aligned}|j+|\begin{aligned}-2 & -1 \\ -4 & 2\end{aligned}|k \\  & =((-1)\cdot (-2)-2\cdot 0)i-((-2)\cdot (-2)-(-4)\cdot 0)j+((-2)\cdot 2-(-4)\cdot (-1))k \\  & =2i-4j-8k \\  & =⟨2,-4,-8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{2}^{2}+(-4)^{2}+(-8)^{2}} \\  & =2\sqrt{21}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{21}}{2}=\sqrt{21}.
$$

### Parameterized replay

## Generated moderate — triangle_blank_direct

Calculate the area ${A}_{△}$ of the triangle spanned by $a=⟨-2,-1,0⟩$ and $b=⟨-4,2,-2⟩.$

${A}_{△}=${{field-1}}

- $\sqrt{21}$ (correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2 & -1 & 0 \\ -4 & 2 & -2\end{aligned}| \\  & =|\begin{aligned}-1 & 0 \\ 2 & -2\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -4 & -2\end{aligned}|j+|\begin{aligned}-2 & -1 \\ -4 & 2\end{aligned}|k \\  & =((-1)\cdot (-2)-2\cdot 0)i-((-2)\cdot (-2)-(-4)\cdot 0)j+((-2)\cdot 2-(-4)\cdot (-1))k \\  & =2i-4j-8k \\  & =⟨2,-4,-8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{2}^{2}+(-4)^{2}+(-8)^{2}} \\  & =2\sqrt{21}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{21}}{2}=\sqrt{21}.
$$

---

## Original q-316345

Calculate the area $A$ of the parallelogram spanned by $a=⟨-3,5,0⟩$ and $b=⟨4,-1,2⟩.$

$A=${{field-1}}

- $5\sqrt{17}$ (source correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 5 & 0 \\ 4 & -1 & 2\end{aligned}| \\  & =|\begin{aligned}5 & 0 \\ -1 & 2\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 4 & 2\end{aligned}|j+|\begin{aligned}-3 & 5 \\ 4 & -1\end{aligned}|k \\  & =(5\cdot 2-0\cdot (-1))i-((-3)\cdot 2-0\cdot 4)j+((-3)\cdot (-1)-5\cdot 4)k \\  & =10i+6j-17k \\  & =⟨10,6,-17⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{10}^{2}+{6}^{2}+(-17)^{2}} \\  & =\sqrt{100+36+289} \\  & =\sqrt{425} \\  & =5\sqrt{17}.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_blank_expanded

Calculate the area $A$ of the parallelogram spanned by $a=⟨-3,5,0⟩$ and $b=⟨4,-1,2⟩.$

$A=${{field-1}}

- $5\sqrt{17}$ (correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 5 & 0 \\ 4 & -1 & 2\end{aligned}| \\  & =|\begin{aligned}5 & 0 \\ -1 & 2\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 4 & 2\end{aligned}|j+|\begin{aligned}-3 & 5 \\ 4 & -1\end{aligned}|k \\  & =(5\cdot 2-0\cdot (-1))i-((-3)\cdot 2-0\cdot 4)j+((-3)\cdot (-1)-5\cdot 4)k \\  & =10i+6j-17k \\  & =⟨10,6,-17⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{10}^{2}+{6}^{2}+(-17)^{2}} \\  & =\sqrt{100+36+289} \\  & =\sqrt{425} \\  & =5\sqrt{17}.\end{aligned}
$$

---

## Original q-316350

Calculate the area $A$ of the parallelogram spanned by $a=⟨1,0,0⟩$ and $b=⟨0,3,4⟩.$

$A=${{field-1}}

- $5$ (source correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 0 & 0 \\ 0 & 3 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 0 \\ 3 & 4\end{aligned}|i-|\begin{aligned}1 & 0 \\ 0 & 4\end{aligned}|j+|\begin{aligned}1 & 0 \\ 0 & 3\end{aligned}|k \\  & =(0\cdot 4-0\cdot 3)i-(1\cdot 4-0\cdot 0)j+(1\cdot 3-0\cdot 0)k \\  & =0i-4j+3k \\  & =⟨0,-4,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{0}^{2}+(-4)^{2}+{3}^{2}} \\  & =\sqrt{0+16+9} \\  & =\sqrt{25} \\  & =5.\end{aligned}
$$

### Parameterized replay

## Generated easy — parallelogram_blank_expanded

Calculate the area $A$ of the parallelogram spanned by $a=⟨1,0,0⟩$ and $b=⟨0,3,4⟩.$

$A=${{field-1}}

- $5$ (correct)

Using the formula, we have

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 0 & 0 \\ 0 & 3 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 0 \\ 3 & 4\end{aligned}|i-|\begin{aligned}1 & 0 \\ 0 & 4\end{aligned}|j+|\begin{aligned}1 & 0 \\ 0 & 3\end{aligned}|k \\  & =(0\cdot 4-0\cdot 3)i-(1\cdot 4-0\cdot 0)j+(1\cdot 3-0\cdot 0)k \\  & =0i-4j+3k \\  & =⟨0,-4,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,a\times b\,| \\  & =\sqrt{{0}^{2}+(-4)^{2}+{3}^{2}} \\  & =\sqrt{0+16+9} \\  & =\sqrt{25} \\  & =5.\end{aligned}
$$

---

## Original q-316355

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨0,5,-1⟩$ and $q=⟨6,0,1⟩.$

${A}_{△}=${{field-1}}

- $\frac{31}{2}$ (source correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 0 & 5 & -1 \\ 6 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}5 & -1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}0 & -1 \\ 6 & 1\end{aligned}|j+|\begin{aligned}0 & 5 \\ 6 & 0\end{aligned}|k \\  & =(5\cdot 1-(-1)\cdot 0)i-(0\cdot 1-(-1)\cdot 6)j+(0\cdot 0-5\cdot 6)k \\  & =5i-6j-30k \\  & =⟨5,-6,-30⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{5}^{2}+(-6)^{2}+(-30)^{2}} \\  & =\sqrt{25+36+900} \\  & =\sqrt{961} \\  & =31.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{31}{2}.
$$

### Parameterized replay

## Generated moderate — triangle_blank_expanded

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨0,5,-1⟩$ and $q=⟨6,0,1⟩.$

${A}_{△}=${{field-1}}

- $\frac{31}{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 0 & 5 & -1 \\ 6 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}5 & -1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}0 & -1 \\ 6 & 1\end{aligned}|j+|\begin{aligned}0 & 5 \\ 6 & 0\end{aligned}|k \\  & =(5\cdot 1-(-1)\cdot 0)i-(0\cdot 1-(-1)\cdot 6)j+(0\cdot 0-5\cdot 6)k \\  & =5i-6j-30k \\  & =⟨5,-6,-30⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{5}^{2}+(-6)^{2}+(-30)^{2}} \\  & =\sqrt{25+36+900} \\  & =\sqrt{961} \\  & =31.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{31}{2}.
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_radical

Calculate the area of the parallelogram spanned by $r=⟨1,-2,1⟩$ and $t=⟨2,3,-1⟩.$

- $\sqrt{10}$
- $\sqrt{58}$
- $5\sqrt{2}$
- $\sqrt{59}$ (correct)
- $\frac{\sqrt{59}}{2}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ 1 & -2 & 1 \\ 2 & 3 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 3 & -1\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & -1\end{aligned}|j+|\begin{aligned}1 & -2 \\ 2 & 3\end{aligned}|k \\  & =((-2)\cdot (-1)-1\cdot 3)i-(1\cdot (-1)-1\cdot 2)j+(1\cdot 3-(-2)\cdot 2)k \\  & =-i+3j+7k \\  & =⟨-1,3,7⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-1)^{2}+{3}^{2}+{7}^{2}} \\  & =\sqrt{59}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_radical

Calculate the area of the parallelogram spanned by $r=⟨-2,5,1⟩$ and $t=⟨1,-2,-4⟩.$

- $\frac{\sqrt{374}}{2}$
- $\sqrt{373}$
- $\sqrt{374}$ (correct)
- $5\sqrt{2}$
- $5\sqrt{13}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -2 & 5 & 1 \\ 1 & -2 & -4\end{aligned}| \\  & =|\begin{aligned}5 & 1 \\ -2 & -4\end{aligned}|i-|\begin{aligned}-2 & 1 \\ 1 & -4\end{aligned}|j+|\begin{aligned}-2 & 5 \\ 1 & -2\end{aligned}|k \\  & =(5\cdot (-4)-1\cdot (-2))i-((-2)\cdot (-4)-1\cdot 1)j+((-2)\cdot (-2)-5\cdot 1)k \\  & =-18i-7j-k \\  & =⟨-18,-7,-1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-18)^{2}+(-7)^{2}+(-1)^{2}} \\  & =\sqrt{374}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $r=⟨-3,2,2⟩$ and $t=⟨-3,1,0⟩.$

- $\frac{7}{2}$
- $\sqrt{13}$
- $3\sqrt{5}$
- $7$ (correct)
- $2\sqrt{10}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -3 & 2 & 2 \\ -3 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 1 & 0\end{aligned}|i-|\begin{aligned}-3 & 2 \\ -3 & 0\end{aligned}|j+|\begin{aligned}-3 & 2 \\ -3 & 1\end{aligned}|k \\  & =(2\cdot 0-2\cdot 1)i-((-3)\cdot 0-2\cdot (-3))j+((-3)\cdot 1-2\cdot (-3))k \\  & =-2i-6j+3k \\  & =⟨-2,-6,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-2)^{2}+(-6)^{2}+{3}^{2}} \\  & =\sqrt{49} \\  & =7.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_simplified

Calculate the area of the parallelogram spanned by $p=⟨4,-2,3⟩$ and $q=⟨0,2,-5⟩.$

- $4\sqrt{5}$
- $4\sqrt{30}$ (correct)
- $4\sqrt{29}$
- $2\sqrt{30}$
- $4\sqrt{26}$

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 4 & -2 & 3 \\ 0 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 2 & -5\end{aligned}|i-|\begin{aligned}4 & 3 \\ 0 & -5\end{aligned}|j+|\begin{aligned}4 & -2 \\ 0 & 2\end{aligned}|k \\  & =((-2)\cdot (-5)-3\cdot 2)i-(4\cdot (-5)-3\cdot 0)j+(4\cdot 2-(-2)\cdot 0)k \\  & =4i+20j+8k \\  & =⟨4,20,8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{4}^{2}+{20}^{2}+{8}^{2}} \\  & =\sqrt{480} \\  & =4\sqrt{30}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_unrated

Calculate the area of the parallelogram spanned by $r = ⟨ 1,-2,1⟩$ and $t = ⟨2, 3, -1⟩$.

- $\sqrt{10}$
- $\sqrt{58}$
- $5\sqrt{2}$
- $\sqrt{59}$ (correct)
- $\frac{\sqrt{59}}{2}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ 1 & -2 & 1 \\ 2 & 3 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 3 & -1\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & -1\end{aligned}|j+|\begin{aligned}1 & -2 \\ 2 & 3\end{aligned}|k \\  & =((-2)\cdot (-1)-1\cdot 3)i-(1\cdot (-1)-1\cdot 2)j+(1\cdot 3-(-2)\cdot 2)k \\  & =-i+3j+7k \\  & =⟨-1,3,7⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-1)^{2}+{3}^{2}+{7}^{2}} \\  & =\sqrt{59}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_radio_unrated

Calculate the area of the parallelogram spanned by $r = ⟨ - 2,5,1⟩$ and $t = ⟨1, -2, -4⟩$.

- $\frac{\sqrt{374}}{2}$
- $\sqrt{373}$
- $\sqrt{374}$ (correct)
- $5\sqrt{2}$
- $5\sqrt{13}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -2 & 5 & 1 \\ 1 & -2 & -4\end{aligned}| \\  & =|\begin{aligned}5 & 1 \\ -2 & -4\end{aligned}|i-|\begin{aligned}-2 & 1 \\ 1 & -4\end{aligned}|j+|\begin{aligned}-2 & 5 \\ 1 & -2\end{aligned}|k \\  & =(5\cdot (-4)-1\cdot (-2))i-((-2)\cdot (-4)-1\cdot 1)j+((-2)\cdot (-2)-5\cdot 1)k \\  & =-18i-7j-k \\  & =⟨-18,-7,-1⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-18)^{2}+(-7)^{2}+(-1)^{2}} \\  & =\sqrt{374}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_blank_direct

Calculate the area $A$ of the parallelogram spanned by $r=⟨-3,2,2⟩$ and $t=⟨-3,1,0⟩.$

$A=${{field-1}}

- $7$ (correct)

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -3 & 2 & 2 \\ -3 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 1 & 0\end{aligned}|i-|\begin{aligned}-3 & 2 \\ -3 & 0\end{aligned}|j+|\begin{aligned}-3 & 2 \\ -3 & 1\end{aligned}|k \\  & =(2\cdot 0-2\cdot 1)i-((-3)\cdot 0-2\cdot (-3))j+((-3)\cdot 1-2\cdot (-3))k \\  & =-2i-6j+3k \\  & =⟨-2,-6,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-2)^{2}+(-6)^{2}+{3}^{2}} \\  & =7.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_blank_direct

Calculate the area $A$ of the parallelogram spanned by $p=⟨4,-2,3⟩$ and $q=⟨0,2,-5⟩.$

$A=${{field-1}}

- $4\sqrt{30}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 4 & -2 & 3 \\ 0 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 2 & -5\end{aligned}|i-|\begin{aligned}4 & 3 \\ 0 & -5\end{aligned}|j+|\begin{aligned}4 & -2 \\ 0 & 2\end{aligned}|k \\  & =((-2)\cdot (-5)-3\cdot 2)i-(4\cdot (-5)-3\cdot 0)j+(4\cdot 2-(-2)\cdot 0)k \\  & =4i+20j+8k \\  & =⟨4,20,8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{4}^{2}+{20}^{2}+{8}^{2}} \\  & =4\sqrt{30}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_blank_expanded

Calculate the area $A$ of the parallelogram spanned by $r=⟨-3,2,2⟩$ and $t=⟨-3,1,0⟩.$

$A=${{field-1}}

- $7$ (correct)

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -3 & 2 & 2 \\ -3 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 1 & 0\end{aligned}|i-|\begin{aligned}-3 & 2 \\ -3 & 0\end{aligned}|j+|\begin{aligned}-3 & 2 \\ -3 & 1\end{aligned}|k \\  & =(2\cdot 0-2\cdot 1)i-((-3)\cdot 0-2\cdot (-3))j+((-3)\cdot 1-2\cdot (-3))k \\  & =-2i-6j+3k \\  & =⟨-2,-6,3⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-2)^{2}+(-6)^{2}+{3}^{2}} \\  & =\sqrt{4+36+9} \\  & =\sqrt{49} \\  & =7.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated easy — parallelogram_blank_expanded

Calculate the area $A$ of the parallelogram spanned by $p=⟨4,-2,3⟩$ and $q=⟨0,2,-5⟩.$

$A=${{field-1}}

- $4\sqrt{30}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 4 & -2 & 3 \\ 0 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 2 & -5\end{aligned}|i-|\begin{aligned}4 & 3 \\ 0 & -5\end{aligned}|j+|\begin{aligned}4 & -2 \\ 0 & 2\end{aligned}|k \\  & =((-2)\cdot (-5)-3\cdot 2)i-(4\cdot (-5)-3\cdot 0)j+(4\cdot 2-(-2)\cdot 0)k \\  & =4i+20j+8k \\  & =⟨4,20,8⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{4}^{2}+{20}^{2}+{8}^{2}} \\  & =\sqrt{16+400+64} \\  & =\sqrt{480} \\  & =4\sqrt{30}.\end{aligned}
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $r=⟨-4,1,1⟩$ and $t=⟨6,-4,5⟩.$

- $\sqrt{857}$
- $\frac{\sqrt{857}}{2}$ (correct)
- $\frac{\sqrt{757}}{2}$
- $\frac{\sqrt{181}}{2}$
- $\sqrt{194}$

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -4 & 1 & 1 \\ 6 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -4 & 5\end{aligned}|i-|\begin{aligned}-4 & 1 \\ 6 & 5\end{aligned}|j+|\begin{aligned}-4 & 1 \\ 6 & -4\end{aligned}|k \\  & =(1\cdot 5-1\cdot (-4))i-((-4)\cdot 5-1\cdot 6)j+((-4)\cdot (-4)-1\cdot 6)k \\  & =9i+26j+10k \\  & =⟨9,26,10⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{{9}^{2}+{26}^{2}+{10}^{2}} \\  & =\sqrt{857}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{857}}{2}.
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_radio_radical

Calculate the area of the triangle spanned by $p=⟨2,-3,3⟩$ and $q=⟨-3,-2,1⟩.$

- $\frac{\sqrt{178}}{2}$
- $\frac{\sqrt{299}}{2}$ (correct)
- $\frac{\sqrt{130}}{2}$
- $\frac{\sqrt{290}}{2}$
- $\sqrt{299}$

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 2 & -3 & 3 \\ -3 & -2 & 1\end{aligned}| \\  & =|\begin{aligned}-3 & 3 \\ -2 & 1\end{aligned}|i-|\begin{aligned}2 & 3 \\ -3 & 1\end{aligned}|j+|\begin{aligned}2 & -3 \\ -3 & -2\end{aligned}|k \\  & =((-3)\cdot 1-3\cdot (-2))i-(2\cdot 1-3\cdot (-3))j+(2\cdot (-2)-(-3)\cdot (-3))k \\  & =3i-11j-13k \\  & =⟨3,-11,-13⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{3}^{2}+(-11)^{2}+(-13)^{2}} \\  & =\sqrt{299}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{299}}{2}.
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_blank_direct

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨5,-1,0⟩$ and $q=⟨2,6,-5⟩.$

${A}_{△}=${{field-1}}

- $\frac{3\sqrt{186}}{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 5 & -1 & 0 \\ 2 & 6 & -5\end{aligned}| \\  & =|\begin{aligned}-1 & 0 \\ 6 & -5\end{aligned}|i-|\begin{aligned}5 & 0 \\ 2 & -5\end{aligned}|j+|\begin{aligned}5 & -1 \\ 2 & 6\end{aligned}|k \\  & =((-1)\cdot (-5)-0\cdot 6)i-(5\cdot (-5)-0\cdot 2)j+(5\cdot 6-(-1)\cdot 2)k \\  & =5i+25j+32k \\  & =⟨5,25,32⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{5}^{2}+{25}^{2}+{32}^{2}} \\  & =3\sqrt{186}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{186}}{2}.
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_blank_direct

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨3,-3,2⟩$ and $q=⟨-1,1,-6⟩.$

${A}_{△}=${{field-1}}

- $8\sqrt{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 3 & -3 & 2 \\ -1 & 1 & -6\end{aligned}| \\  & =|\begin{aligned}-3 & 2 \\ 1 & -6\end{aligned}|i-|\begin{aligned}3 & 2 \\ -1 & -6\end{aligned}|j+|\begin{aligned}3 & -3 \\ -1 & 1\end{aligned}|k \\  & =((-3)\cdot (-6)-2\cdot 1)i-(3\cdot (-6)-2\cdot (-1))j+(3\cdot 1-(-3)\cdot (-1))k \\  & =16i+16j \\  & =⟨16,16,0⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{16}^{2}+{16}^{2}+{0}^{2}} \\  & =16\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{16\sqrt{2}}{2}=8\sqrt{2}.
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_blank_expanded

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨5,-1,0⟩$ and $q=⟨2,6,-5⟩.$

${A}_{△}=${{field-1}}

- $\frac{3\sqrt{186}}{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 5 & -1 & 0 \\ 2 & 6 & -5\end{aligned}| \\  & =|\begin{aligned}-1 & 0 \\ 6 & -5\end{aligned}|i-|\begin{aligned}5 & 0 \\ 2 & -5\end{aligned}|j+|\begin{aligned}5 & -1 \\ 2 & 6\end{aligned}|k \\  & =((-1)\cdot (-5)-0\cdot 6)i-(5\cdot (-5)-0\cdot 2)j+(5\cdot 6-(-1)\cdot 2)k \\  & =5i+25j+32k \\  & =⟨5,25,32⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{5}^{2}+{25}^{2}+{32}^{2}} \\  & =\sqrt{25+625+1024} \\  & =\sqrt{1674} \\  & =3\sqrt{186}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{186}}{2}.
$$

---

### Authored default bank / generated variant

## Generated moderate — triangle_blank_expanded

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨3,-3,2⟩$ and $q=⟨-1,1,-6⟩.$

${A}_{△}=${{field-1}}

- $8\sqrt{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ 3 & -3 & 2 \\ -1 & 1 & -6\end{aligned}| \\  & =|\begin{aligned}-3 & 2 \\ 1 & -6\end{aligned}|i-|\begin{aligned}3 & 2 \\ -1 & -6\end{aligned}|j+|\begin{aligned}3 & -3 \\ -1 & 1\end{aligned}|k \\  & =((-3)\cdot (-6)-2\cdot 1)i-(3\cdot (-6)-2\cdot (-1))j+(3\cdot 1-(-3)\cdot (-1))k \\  & =16i+16j \\  & =⟨16,16,0⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{{16}^{2}+{16}^{2}+{0}^{2}} \\  & =\sqrt{256+256+0} \\  & =\sqrt{512} \\  & =16\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{16\sqrt{2}}{2}=8\sqrt{2}.
$$

---

### Authored default bank / generated variant

## Generated hard — triangle_hard_radio

Calculate the area of the triangle spanned by $p=⟨-5,1,-3⟩$ and $q=⟨2,-5,5⟩.$

- $\frac{\sqrt{890}}{2}$
- $\frac{\sqrt{629}}{2}$
- $\frac{\sqrt{461}}{2}$
- $\frac{3\sqrt{110}}{2}$ (correct)
- $3\sqrt{110}$

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ -5 & 1 & -3 \\ 2 & -5 & 5\end{aligned}| \\  & =|\begin{aligned}1 & -3 \\ -5 & 5\end{aligned}|i-|\begin{aligned}-5 & -3 \\ 2 & 5\end{aligned}|j+|\begin{aligned}-5 & 1 \\ 2 & -5\end{aligned}|k \\  & =(1\cdot 5-(-3)\cdot (-5))i-((-5)\cdot 5-(-3)\cdot 2)j+((-5)\cdot (-5)-1\cdot 2)k \\  & =-10i+19j+23k \\  & =⟨-10,19,23⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{(-10)^{2}+{19}^{2}+{23}^{2}} \\  & =\sqrt{100+361+529} \\  & =\sqrt{990} \\  & =3\sqrt{110}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{110}}{2}.
$$

---

### Authored default bank / generated variant

## Generated hard — triangle_hard_radio

Calculate the area of the triangle spanned by $r=⟨-5,-6,3⟩$ and $t=⟨-1,2,5⟩.$

- $2\sqrt{509}$
- $\sqrt{445}$
- $\sqrt{185}$
- $2\sqrt{97}$
- $\sqrt{509}$ (correct)

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -5 & -6 & 3 \\ -1 & 2 & 5\end{aligned}| \\  & =|\begin{aligned}-6 & 3 \\ 2 & 5\end{aligned}|i-|\begin{aligned}-5 & 3 \\ -1 & 5\end{aligned}|j+|\begin{aligned}-5 & -6 \\ -1 & 2\end{aligned}|k \\  & =((-6)\cdot 5-3\cdot 2)i-((-5)\cdot 5-3\cdot (-1))j+((-5)\cdot 2-(-6)\cdot (-1))k \\  & =-36i+22j-16k \\  & =⟨-36,22,-16⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-36)^{2}+{22}^{2}+(-16)^{2}} \\  & =\sqrt{1296+484+256} \\  & =\sqrt{2036} \\  & =2\sqrt{509}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{509}}{2}=\sqrt{509}.
$$

---

### Authored default bank / generated variant

## Generated hard — triangle_hard_blank

Calculate the area ${A}_{△}$ of the triangle spanned by $p=⟨-5,1,-3⟩$ and $q=⟨2,-5,5⟩.$

${A}_{△}=${{field-1}}

- $\frac{3\sqrt{110}}{2}$ (correct)

Using the formula, we have

$$
\begin{aligned}p\times q & =|\begin{aligned}i & j & k \\ -5 & 1 & -3 \\ 2 & -5 & 5\end{aligned}| \\  & =|\begin{aligned}1 & -3 \\ -5 & 5\end{aligned}|i-|\begin{aligned}-5 & -3 \\ 2 & 5\end{aligned}|j+|\begin{aligned}-5 & 1 \\ 2 & -5\end{aligned}|k \\  & =(1\cdot 5-(-3)\cdot (-5))i-((-5)\cdot 5-(-3)\cdot 2)j+((-5)\cdot (-5)-1\cdot 2)k \\  & =-10i+19j+23k \\  & =⟨-10,19,23⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,p\times q\,| \\  & =\sqrt{(-10)^{2}+{19}^{2}+{23}^{2}} \\  & =\sqrt{100+361+529} \\  & =\sqrt{990} \\  & =3\sqrt{110}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{110}}{2}.
$$

---

### Authored default bank / generated variant

## Generated hard — triangle_hard_blank

Calculate the area ${A}_{△}$ of the triangle spanned by $r=⟨-5,-6,3⟩$ and $t=⟨-1,2,5⟩.$

${A}_{△}=${{field-1}}

- $\sqrt{509}$ (correct)

Using the formula, we have

$$
\begin{aligned}r\times t & =|\begin{aligned}i & j & k \\ -5 & -6 & 3 \\ -1 & 2 & 5\end{aligned}| \\  & =|\begin{aligned}-6 & 3 \\ 2 & 5\end{aligned}|i-|\begin{aligned}-5 & 3 \\ -1 & 5\end{aligned}|j+|\begin{aligned}-5 & -6 \\ -1 & 2\end{aligned}|k \\  & =((-6)\cdot 5-3\cdot 2)i-((-5)\cdot 5-3\cdot (-1))j+((-5)\cdot 2-(-6)\cdot (-1))k \\  & =-36i+22j-16k \\  & =⟨-36,22,-16⟩.\end{aligned}
$$

Therefore, the area of the corresponding parallelogram is

$$
\begin{aligned}A & =|\,r\times t\,| \\  & =\sqrt{(-36)^{2}+{22}^{2}+(-16)^{2}} \\  & =\sqrt{1296+484+256} \\  & =\sqrt{2036} \\  & =2\sqrt{509}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{509}}{2}=\sqrt{509}.
$$
