# Original and generated review

All originals replay through the public parameterized API. q-20016 includes a separately authored missing solution and inferred key. Raw q-127908 retains its duplicate wrong alternatives; the repair is shown separately. Generated examples are labelled explicitly.

## Original replay q-20016

Template: `q-20016`; profile: `observed/q-20016`.

Calculate the area of the $△ABC$, if $A(1, 1, 0)$, $B(3, 2, 2)$, $C(1, 2, 1)$.

- $\frac{\sqrt{3}}{2}$
- $3$
- $1$
- $2$
- $\frac{3}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+2j+2k)-(i+j) \\  & =2i+j+2k \\  & =⟨2,1,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+2j+k)-(i+j) \\  & =j+k \\  & =⟨0,1,1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 1 & 2 \\ 0 & 1 & 1\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 1 & 1\end{aligned}|i-|\begin{aligned}2 & 2 \\ 0 & 1\end{aligned}|j+|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|k \\  & =(1\cdot 1-2\cdot 1)i-(2\cdot 1-2\cdot 0)j+(2\cdot 1-1\cdot 0)k \\  & =-i-2j+2k \\  & =⟨-1,-2,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-1)^{2}+(-2)^{2}+{2}^{2}} \\  & =\sqrt{9} \\  & =3.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3}{2}.
$$

## Generated observed template/profile q-20016/37

Template: `q-20016`; profile: `observed/q-20016`.

Calculate the area of the $△ABC$, if $A(-3, 4, -4)$, $B(2, 4, -2)$, $C(0, 0, 1)$.

- $\frac{5\sqrt{33}}{3}$
- $\frac{10\sqrt{33}}{3}$
- $5\sqrt{33}$
- $\frac{\sqrt{275}}{2}$
- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-20016/43

Template: `q-20016`; profile: `observed/q-20016`.

Calculate the area of the $△ABC$, if $A(-4, 0, -2)$, $B(-2, 0, 3)$, $C(-8, 2, 2)$.

- $20$
- $30$
- $\frac{\sqrt{300}}{2}$
- $10$
- $15$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}=15.
$$

## Original replay q-20026

Template: `q-20026`; profile: `observed/q-20026`.

Calculate the area of the $△\,PQR$, if $P(4,7,3)$, $Q(5,6,2)$, $R(3,8,3).$

- $\frac{\sqrt{3}}{2}$
- $2$
- $\frac{\sqrt{2}}{2}$ — correct
- $\sqrt{2}$
- $\sqrt{3}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(5i+6j+2k)-(4i+7j+3k) \\  & =i-j-k \\  & =⟨1,-1,-1⟩ \\ \overset{\to }{PR} & =r-p \\  & =(3i+8j+3k)-(4i+7j+3k) \\  & =-i+j \\  & =⟨-1,1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 1 & -1 & -1 \\ -1 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ 1 & 0\end{aligned}|i-|\begin{aligned}1 & -1 \\ -1 & 0\end{aligned}|j+|\begin{aligned}1 & -1 \\ -1 & 1\end{aligned}|k \\  & =((-1)\cdot 0-1\cdot (-1))i-(1\cdot 0-(-1)\cdot (-1))j+(1\cdot 1-(-1)\cdot (-1))k \\  & =i+j \\  & =⟨1,1,0⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{1}^{2}+{1}^{2}+{0}^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{2}}{2}.
$$

## Generated observed template/profile q-20026/37

Template: `q-20026`; profile: `observed/q-20026`.

Calculate the area of the $△\,PQR$, if $P(-3,4,-4)$, $Q(2,4,-2)$, $R(0,0,1).$

- $\frac{\sqrt{825}}{2}$ — correct
- $\sqrt{825}$
- $5\sqrt{66}$
- $\frac{\sqrt{\frac{2475}{2}}}{2}$
- $\sqrt{\frac{2475}{2}}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-20026/43

Template: `q-20026`; profile: `observed/q-20026`.

Calculate the area of the $△\,PQR$, if $P(-4,0,-2)$, $Q(-2,0,3)$, $R(-8,2,2).$

- $\sqrt{900}$
- $30\sqrt{2}$
- $\frac{\sqrt{1350}}{2}$
- $\frac{\sqrt{900}}{2}$ — correct
- $\sqrt{1350}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-127866

Template: `q-127866`; profile: `observed/q-127866`.

Calculate the area of the $△\,ABC,$ if $A(5,0,5),$ $B(6,-1,4),$ $C(9,1,0).$

- $\frac{13\sqrt{2}}{2}$
- $\frac{\sqrt{31}}{2}$
- $\sqrt{62}$
- $\frac{\sqrt{62}}{2}$ — correct
- $\sqrt{31}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(6i-j+4k)-(5i+5k) \\  & =i-j-k \\  & =⟨1,-1,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(9i+j)-(5i+5k) \\  & =4i+j-5k \\  & =⟨4,1,-5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 1 & -1 & -1 \\ 4 & 1 & -5\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ 1 & -5\end{aligned}|i-|\begin{aligned}1 & -1 \\ 4 & -5\end{aligned}|j+|\begin{aligned}1 & -1 \\ 4 & 1\end{aligned}|k \\  & =((-1)\cdot (-5)-1\cdot (-1))i-(1\cdot (-5)-4\cdot (-1))j+(1\cdot 1-4\cdot (-1))k \\  & =6i+j+5k \\  & =⟨6,1,5⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{6}^{2}+{1}^{2}+{5}^{2}} \\  & =\sqrt{62}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{62}}{2}.
$$

## Generated observed template/profile q-127866/37

Template: `q-127866`; profile: `observed/q-127866`.

Calculate the area of the $△\,ABC,$ if $A(-3,4,-4),$ $B(2,4,-2),$ $C(0,0,1).$

- $\sqrt{825}$
- $\frac{\sqrt{825}}{2}$ — correct
- $\frac{\sqrt{\frac{825}{2}}}{2}$
- $\frac{13\sqrt{\frac{825}{31}}}{2}$
- $\sqrt{\frac{825}{2}}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-127866/43

Template: `q-127866`; profile: `observed/q-127866`.

Calculate the area of the $△\,ABC,$ if $A(-4,0,-2),$ $B(-2,0,3),$ $C(-8,2,2).$

- $\frac{\sqrt{900}}{2}$ — correct
- $\frac{\sqrt{450}}{2}$
- $\frac{13\sqrt{\frac{900}{31}}}{2}$
- $\sqrt{900}$
- $\sqrt{450}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-127908

Template: `q-127908`; profile: `raw/q-127908`.

Calculate the area of the $△\,PQR,$ if $P(2,6,6),$ $Q(4,8,2),$ $R(0,5,6).$

- $\sqrt{21}$ — correct
- $\frac{3\sqrt{17}}{3}$
- $2\sqrt{21}$
- $\sqrt{17}$
- $\frac{\sqrt{21}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(4i+8j+2k)-(2i+6j+6k) \\  & =2i+2j-4k \\  & =⟨2,2,-4⟩ \\ \overset{\to }{PR} & =r-p \\  & =(5j+6k)-(2i+6j+6k) \\  & =-2i-j \\  & =⟨-2,-1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 2 & -4 \\ -2 & -1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & -4 \\ -1 & 0\end{aligned}|i-|\begin{aligned}2 & -4 \\ -2 & 0\end{aligned}|j+|\begin{aligned}2 & 2 \\ -2 & -1\end{aligned}|k \\  & =(2\cdot 0-(-1)\cdot (-4))i-(2\cdot 0-(-2)\cdot (-4))j+(2\cdot (-1)-(-2)\cdot 2)k \\  & =-4i+8j+2k \\  & =⟨-4,8,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-4)^{2}+{8}^{2}+{2}^{2}} \\  & =\sqrt{84} \\  & =2\sqrt{21}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{21}}{2}=\sqrt{21}.
$$

## Generated observed template/profile q-127908/37

Template: `q-127908`; profile: `raw/q-127908`.

Calculate the area of the $△\,PQR,$ if $P(-3,4,-4),$ $Q(2,4,-2),$ $R(0,0,1).$

- $2\sqrt{\frac{825}{4}}$
- $\sqrt{\frac{4675}{28}}$
- $\frac{3\sqrt{\frac{4675}{28}}}{3}$
- $\sqrt{\frac{825}{4}}$ — correct
- $\frac{\sqrt{\frac{825}{4}}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-127908/43

Template: `q-127908`; profile: `raw/q-127908`.

Calculate the area of the $△\,PQR,$ if $P(-4,0,-2),$ $Q(-2,0,3),$ $R(-8,2,2).$

- $\sqrt{\frac{1275}{7}}$
- $\frac{3\sqrt{\frac{1275}{7}}}{3}$
- $\sqrt{225}$ — correct
- $2\sqrt{225}$
- $\frac{\sqrt{225}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}=15.
$$

## Minimal duplicate-bank repair q-127908

Template: `q-127908`; profile: `observed/q-127908`.

Calculate the area of the $△\,PQR,$ if $P(2,6,6),$ $Q(4,8,2),$ $R(0,5,6).$

- $\sqrt{21}$ — correct
- $42$
- $2\sqrt{21}$
- $\sqrt{17}$
- $\frac{\sqrt{21}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(4i+8j+2k)-(2i+6j+6k) \\  & =2i+2j-4k \\  & =⟨2,2,-4⟩ \\ \overset{\to }{PR} & =r-p \\  & =(5j+6k)-(2i+6j+6k) \\  & =-2i-j \\  & =⟨-2,-1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 2 & -4 \\ -2 & -1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & -4 \\ -1 & 0\end{aligned}|i-|\begin{aligned}2 & -4 \\ -2 & 0\end{aligned}|j+|\begin{aligned}2 & 2 \\ -2 & -1\end{aligned}|k \\  & =(2\cdot 0-(-1)\cdot (-4))i-(2\cdot 0-(-2)\cdot (-4))j+(2\cdot (-1)-(-2)\cdot 2)k \\  & =-4i+8j+2k \\  & =⟨-4,8,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-4)^{2}+{8}^{2}+{2}^{2}} \\  & =\sqrt{84} \\  & =2\sqrt{21}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{21}}{2}=\sqrt{21}.
$$

## Original replay q-127913

Template: `q-127913`; profile: `observed/q-127913`.

Calculate the area of the $△\,PQR,$ if $P(6,1,5),$ $Q(5,1,7),$ $R(4,2,0).$

- $\frac{\sqrt{86}}{2}$ — correct
- $\frac{21\sqrt{2}}{2}$
- $\frac{3}{2}$
- $\sqrt{43}$
- $\frac{3\sqrt{13}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(5i+j+7k)-(6i+j+5k) \\  & =-i+2k \\  & =⟨-1,0,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =(4i+2j)-(6i+j+5k) \\  & =-2i+j-5k \\  & =⟨-2,1,-5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ -1 & 0 & 2 \\ -2 & 1 & -5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ 1 & -5\end{aligned}|i-|\begin{aligned}-1 & 2 \\ -2 & -5\end{aligned}|j+|\begin{aligned}-1 & 0 \\ -2 & 1\end{aligned}|k \\  & =(0\cdot (-5)-1\cdot 2)i-((-1)\cdot (-5)-(-2)\cdot 2)j+((-1)\cdot 1-(-2)\cdot 0)k \\  & =-2i-9j-k \\  & =⟨-2,-9,-1⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-2)^{2}+(-9)^{2}+(-1)^{2}} \\  & =\sqrt{86}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{86}}{2}.
$$

## Generated observed template/profile q-127913/37

Template: `q-127913`; profile: `observed/q-127913`.

Calculate the area of the $△\,PQR,$ if $P(-3,4,-4),$ $Q(2,4,-2),$ $R(0,0,1).$

- $\frac{15\sqrt{2838}}{172}$
- $\sqrt{\frac{825}{2}}$
- $\frac{21\sqrt{\frac{825}{43}}}{2}$
- $\frac{\sqrt{825}}{2}$ — correct
- $\frac{3\sqrt{\frac{10725}{86}}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-127913/43

Template: `q-127913`; profile: `observed/q-127913`.

Calculate the area of the $△\,PQR,$ if $P(-4,0,-2),$ $Q(-2,0,3),$ $R(-8,2,2).$

- $\sqrt{450}$
- $\frac{21\sqrt{\frac{900}{43}}}{2}$
- $\frac{\sqrt{900}}{2}$ — correct
- $\frac{45\sqrt{86}}{86}$
- $\frac{3\sqrt{\frac{5850}{43}}}{2}$

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-127915

Template: `q-127915`; profile: `observed/q-127915`.

Calculate the area of the $△\,WXY,$ if $W(3,9,4),$ $X(1,7,3),$ $Y(6,12,8).$

- $3\sqrt{5}$
- $\frac{5\sqrt{2}}{2}$ — correct
- $5$
- $\frac{5}{2}$
- $\sqrt{5}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(i+7j+3k)-(3i+9j+4k) \\  & =-2i-2j-k \\  & =⟨-2,-2,-1⟩ \\ \overset{\to }{WY} & =y-w \\  & =(6i+12j+8k)-(3i+9j+4k) \\  & =3i+3j+4k \\  & =⟨3,3,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ -2 & -2 & -1 \\ 3 & 3 & 4\end{aligned}| \\  & =|\begin{aligned}-2 & -1 \\ 3 & 4\end{aligned}|i-|\begin{aligned}-2 & -1 \\ 3 & 4\end{aligned}|j+|\begin{aligned}-2 & -2 \\ 3 & 3\end{aligned}|k \\  & =((-2)\cdot 4-3\cdot (-1))i-((-2)\cdot 4-3\cdot (-1))j+((-2)\cdot 3-3\cdot (-2))k \\  & =-5i+5j \\  & =⟨-5,5,0⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{(-5)^{2}+{5}^{2}+{0}^{2}} \\  & =5\sqrt{2}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{2}}{2}.
$$

## Generated observed template/profile q-127915/37

Template: `q-127915`; profile: `observed/q-127915`.

Calculate the area of the $△\,WXY,$ if $W(-3,4,-4),$ $X(2,4,-2),$ $Y(0,0,1).$

- $\frac{5\sqrt{66}}{2}$
- $\frac{5\sqrt{66}}{4}$
- $\frac{5\sqrt{33}}{2}$ — correct
- $3\sqrt{\frac{165}{2}}$
- $\sqrt{\frac{165}{2}}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{WY} & =y-w \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-127915/43

Template: `q-127915`; profile: `observed/q-127915`.

Calculate the area of the $△\,WXY,$ if $W(-4,0,-2),$ $X(-2,0,3),$ $Y(-8,2,2).$

- $\frac{15\sqrt{2}}{2}$
- $\frac{5\sqrt{36}}{2}$ — correct
- $3\sqrt{90}$
- $15\sqrt{2}$
- $\sqrt{90}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{WY} & =y-w \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}.
$$

## Original replay q-18581

Template: `q-18581`; profile: `observed/q-18581`.

Calculate the area of the $△\,LMN$, if $L(0,0,1)$, $M(2,1,1)$, $N(3,1,1).$

- $\frac{\sqrt{2}}{2}$
- $\sqrt{2}$
- $\frac{\sqrt{3}}{2}$
- $\frac{1}{2}$ — correct
- $1$

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2i+j+k)-k \\  & =2i+j \\  & =⟨2,1,0⟩ \\ \overset{\to }{LN} & =n-l \\  & =(3i+j+k)-k \\  & =3i+j \\  & =⟨3,1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 2 & 1 & 0 \\ 3 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 1 & 0\end{aligned}|i-|\begin{aligned}2 & 0 \\ 3 & 0\end{aligned}|j+|\begin{aligned}2 & 1 \\ 3 & 1\end{aligned}|k \\  & =(1\cdot 0-0\cdot 1)i-(2\cdot 0-0\cdot 3)j+(2\cdot 1-1\cdot 3)k \\  & =-k \\  & =⟨0,0,-1⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{0}^{2}+{0}^{2}+(-1)^{2}} \\  & =1.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{1}{2}.
$$

## Generated observed template/profile q-18581/37

Template: `q-18581`; profile: `observed/q-18581`.

Calculate the area of the $△\,LMN$, if $L(-3,4,-4)$, $M(2,4,-2)$, $N(0,0,1).$

- $\frac{\sqrt{2475}}{2}$
- $\frac{5\sqrt{33}}{2}$ — correct
- $\sqrt{1650}$
- $\frac{\sqrt{1650}}{2}$
- $5\sqrt{33}$

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{LN} & =n-l \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-18581/43

Template: `q-18581`; profile: `observed/q-18581`.

Calculate the area of the $△\,LMN$, if $L(-4,0,-2)$, $M(-2,0,3)$, $N(-8,2,2).$

- $15$ — correct
- $\sqrt{1800}$
- $\frac{\sqrt{1800}}{2}$
- $\frac{\sqrt{2700}}{2}$
- $30$

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=15.
$$

## Original replay q-20017

Template: `q-20017`; profile: `observed/q-20017`.

Calculate the area of the $△\,RST$, if $R(3,-2,1)$, $S(2,-2,2)$, $T(1,-3,3).$

- $1$
- $\sqrt{2}$
- $\frac{\sqrt{2}}{2}$ — correct
- $\frac{\sqrt{3}}{2}$
- $2$

First, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(2i-2j+2k)-(3i-2j+k) \\  & =-i+k \\  & =⟨-1,0,1⟩ \\ \overset{\to }{RT} & =t-r \\  & =(i-3j+3k)-(3i-2j+k) \\  & =-2i-j+2k \\  & =⟨-2,-1,2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ -1 & 0 & 1 \\ -2 & -1 & 2\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ -1 & 2\end{aligned}|i-|\begin{aligned}-1 & 1 \\ -2 & 2\end{aligned}|j+|\begin{aligned}-1 & 0 \\ -2 & -1\end{aligned}|k \\  & =(0\cdot 2-(-1)\cdot 1)i-((-1)\cdot 2-(-2)\cdot 1)j+((-1)\cdot (-1)-(-2)\cdot 0)k \\  & =i+k \\  & =⟨1,0,1⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{{1}^{2}+{0}^{2}+{1}^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{2}}{2}.
$$

## Generated observed template/profile q-20017/37

Template: `q-20017`; profile: `observed/q-20017`.

Calculate the area of the $△\,RST$, if $R(-3,4,-4)$, $S(2,4,-2)$, $T(0,0,1).$

- $\frac{\sqrt{825}}{2}$ — correct
- $\frac{\sqrt{\frac{2475}{2}}}{2}$
- $\sqrt{825}$
- $\frac{5\sqrt{66}}{2}$
- $5\sqrt{66}$

First, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{RT} & =t-r \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-20017/43

Template: `q-20017`; profile: `observed/q-20017`.

Calculate the area of the $△\,RST$, if $R(-4,0,-2)$, $S(-2,0,3)$, $T(-8,2,2).$

- $\frac{\sqrt{1350}}{2}$
- $\sqrt{900}$
- $15\sqrt{2}$
- $\frac{\sqrt{900}}{2}$ — correct
- $30\sqrt{2}$

First, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{RT} & =t-r \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-275224

Template: `q-275224`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,ABC$, if $A(-2,0,-1)$, $B(-3,3,-4)$, $C(0,-2,2).$

${A}_{△}=${{field-1}}

- $\frac{\sqrt{34}}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-3i+3j-4k)-(-2i-k) \\  & =-i+3j-3k \\  & =⟨-1,3,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2j+2k)-(-2i-k) \\  & =2i-2j+3k \\  & =⟨2,-2,3⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & 3 & -3 \\ 2 & -2 & 3\end{aligned}| \\  & =|\begin{aligned}3 & -3 \\ -2 & 3\end{aligned}|i-|\begin{aligned}-1 & -3 \\ 2 & 3\end{aligned}|j+|\begin{aligned}-1 & 3 \\ 2 & -2\end{aligned}|k \\  & =(3\cdot 3-(-2)\cdot (-3))i-((-1)\cdot 3-2\cdot (-3))j+((-1)\cdot (-2)-2\cdot 3)k \\  & =3i-3j-4k \\  & =⟨3,-3,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{3}^{2}+(-3)^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{34}}{2}.
$$

## Generated observed template/profile q-275224/37

Template: `q-275224`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,ABC$, if $A(-3,4,-4)$, $B(2,4,-2)$, $C(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-275224/43

Template: `q-275224`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,ABC$, if $A(-4,0,-2)$, $B(-2,0,3)$, $C(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-316361

Template: `q-316361`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,PQR$, if $P(1,-2,0)$, $Q(3,1,-1)$, $R(-1,0,2).$

${A}_{△}=${{field-1}}

- $\sqrt{42}$ — correct

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(3i+j-k)-(i-2j) \\  & =2i+3j-k \\  & =⟨2,3,-1⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-i+2k)-(i-2j) \\  & =-2i+2j+2k \\  & =⟨-2,2,2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 3 & -1 \\ -2 & 2 & 2\end{aligned}| \\  & =|\begin{aligned}3 & -1 \\ 2 & 2\end{aligned}|i-|\begin{aligned}2 & -1 \\ -2 & 2\end{aligned}|j+|\begin{aligned}2 & 3 \\ -2 & 2\end{aligned}|k \\  & =(3\cdot 2-(-1)\cdot 2)i-(2\cdot 2-(-1)\cdot (-2))j+(2\cdot 2-3\cdot (-2))k \\  & =8i-2j+10k \\  & =⟨8,-2,10⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{8}^{2}+(-2)^{2}+{10}^{2}} \\  & =\sqrt{64+4+100} \\  & =\sqrt{168} \\  & =2\sqrt{42}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{42}}{2}=\sqrt{42}.
$$

## Generated observed template/profile q-316361/37

Template: `q-316361`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,PQR$, if $P(-3,4,-4)$, $Q(2,4,-2)$, $R(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{PR} & =r-p \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{64+361+400} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-316361/43

Template: `q-316361`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,PQR$, if $P(-4,0,-2)$, $Q(-2,0,3)$, $R(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{100+784+16} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}=15.
$$

## Original replay q-316362

Template: `q-316362`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-2,1,3)$, $E(0,-1,0)$, $F(2,2,-1).$

${A}_{△}=${{field-1}}

- $\frac{\sqrt{237}}{2}$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(-j)-(-2i+j+3k) \\  & =2i-2j-3k \\  & =⟨2,-2,-3⟩ \\ \overset{\to }{DF} & =f-d \\  & =(2i+2j-k)-(-2i+j+3k) \\  & =4i+j-4k \\  & =⟨4,1,-4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 2 & -2 & -3 \\ 4 & 1 & -4\end{aligned}| \\  & =|\begin{aligned}-2 & -3 \\ 1 & -4\end{aligned}|i-|\begin{aligned}2 & -3 \\ 4 & -4\end{aligned}|j+|\begin{aligned}2 & -2 \\ 4 & 1\end{aligned}|k \\  & =((-2)\cdot (-4)-(-3)\cdot 1)i-(2\cdot (-4)-(-3)\cdot 4)j+(2\cdot 1-(-2)\cdot 4)k \\  & =11i-4j+10k \\  & =⟨11,-4,10⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{{11}^{2}+(-4)^{2}+{10}^{2}} \\  & =\sqrt{121+16+100} \\  & =\sqrt{237}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{237}}{2}.
$$

## Generated observed template/profile q-316362/37

Template: `q-316362`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-3,4,-4)$, $E(2,4,-2)$, $F(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{DF} & =f-d \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{64+361+400} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-316362/43

Template: `q-316362`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-4,0,-2)$, $E(-2,0,3)$, $F(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{DF} & =f-d \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{100+784+16} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-316363

Template: `q-316363`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(-3,0,1)$, $M(0,2,-2)$, $N(2,-1,0).$

${A}_{△}=${{field-1}}

- $\frac{13\sqrt{2}}{2}$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2j-2k)-(-3i+k) \\  & =3i+2j-3k \\  & =⟨3,2,-3⟩ \\ \overset{\to }{LN} & =n-l \\  & =(2i-j)-(-3i+k) \\  & =5i-j-k \\  & =⟨5,-1,-1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 3 & 2 & -3 \\ 5 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -3 \\ -1 & -1\end{aligned}|i-|\begin{aligned}3 & -3 \\ 5 & -1\end{aligned}|j+|\begin{aligned}3 & 2 \\ 5 & -1\end{aligned}|k \\  & =(2\cdot (-1)-(-3)\cdot (-1))i-(3\cdot (-1)-(-3)\cdot 5)j+(3\cdot (-1)-2\cdot 5)k \\  & =-5i-12j-13k \\  & =⟨-5,-12,-13⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-5)^{2}+(-12)^{2}+(-13)^{2}} \\  & =\sqrt{25+144+169} \\  & =\sqrt{338} \\  & =13\sqrt{2}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{13\sqrt{2}}{2}.
$$

## Generated observed template/profile q-316363/37

Template: `q-316363`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(-3,4,-4)$, $M(2,4,-2)$, $N(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{LN} & =n-l \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{64+361+400} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-316363/43

Template: `q-316363`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(-4,0,-2)$, $M(-2,0,3)$, $N(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{100+784+16} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}.
$$

## Original replay q-316514

Template: `q-316514`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-1,2,0)$, $E(2,0,1)$, $F(1,3,2).$

${A}_{△}=${{field-1}}

- $\frac{3\sqrt{10}}{2}$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(2i+k)-(-i+2j) \\  & =3i-2j+k \\  & =⟨3,-2,1⟩ \\ \overset{\to }{DF} & =f-d \\  & =(i+3j+2k)-(-i+2j) \\  & =2i+j+2k \\  & =⟨2,1,2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 3 & -2 & 1 \\ 2 & 1 & 2\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 1 & 2\end{aligned}|i-|\begin{aligned}3 & 1 \\ 2 & 2\end{aligned}|j+|\begin{aligned}3 & -2 \\ 2 & 1\end{aligned}|k \\  & =((-2)\cdot 2-1\cdot 1)i-(3\cdot 2-2\cdot 1)j+(3\cdot 1-(-2)\cdot 2)k \\  & =-5i-4j+7k \\  & =⟨-5,-4,7⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{(-5)^{2}+(-4)^{2}+{7}^{2}} \\  & =\sqrt{90} \\  & =3\sqrt{10}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{10}}{2}.
$$

## Generated observed template/profile q-316514/37

Template: `q-316514`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-3,4,-4)$, $E(2,4,-2)$, $F(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{DF} & =f-d \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-316514/43

Template: `q-316514`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,DEF$, if $D(-4,0,-2)$, $E(-2,0,3)$, $F(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{DE}$ and $\overset{\to }{DF}:$

$$
\begin{aligned}\overset{\to }{DE} & =e-d \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{DF} & =f-d \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{DE}\times \overset{\to }{DF} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{DE}$ and $\overset{\to }{DF}$ is

$$
\begin{aligned}A & =|\overset{\to }{DE}\times \overset{\to }{DF}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DEF$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}.
$$

## Original replay q-316516

Template: `q-316516`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(1,0,-1)$, $M(3,2,0)$, $N(0,1,3).$

${A}_{△}=${{field-1}}

- $\frac{\sqrt{146}}{2}$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(3i+2j)-(i-k) \\  & =2i+2j+k \\  & =⟨2,2,1⟩ \\ \overset{\to }{LN} & =n-l \\  & =(j+3k)-(i-k) \\  & =-i+j+4k \\  & =⟨-1,1,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 2 & 2 & 1 \\ -1 & 1 & 4\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 1 & 4\end{aligned}|i-|\begin{aligned}2 & 1 \\ -1 & 4\end{aligned}|j+|\begin{aligned}2 & 2 \\ -1 & 1\end{aligned}|k \\  & =(2\cdot 4-1\cdot 1)i-(2\cdot 4-(-1)\cdot 1)j+(2\cdot 1-2\cdot (-1))k \\  & =7i-9j+4k \\  & =⟨7,-9,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{7}^{2}+(-9)^{2}+{4}^{2}} \\  & =\sqrt{146}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{146}}{2}.
$$

## Generated observed template/profile q-316516/37

Template: `q-316516`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(-3,4,-4)$, $M(2,4,-2)$, $N(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{LN} & =n-l \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-316516/43

Template: `q-316516`; profile: `blank`.

Calculate the area ${A}_{△}$ of the $△\,LMN$, if $L(-4,0,-2)$, $M(-2,0,3)$, $N(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-316530

Template: `q-316530`; profile: `blank`.

Calculate the area of the $△\,STU,$ if $S(0,1,2),$ $T(2,3,1),$ $U(4,1,2).$

${A}_{△}=${{field-1}}

- $2\sqrt{5}$ — correct

First, we find the vectors $\overset{\to }{ST}$ and $\overset{\to }{SU}:$

$$
\begin{aligned}\overset{\to }{ST} & =t-s \\  & =(2i+3j+k)-(j+2k) \\  & =2i+2j-k \\  & =⟨2,2,-1⟩ \\ \overset{\to }{SU} & =u-s \\  & =(4i+j+2k)-(j+2k) \\  & =4i+0j+0k \\  & =⟨4,0,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{ST}\times \overset{\to }{SU} & =|\begin{aligned}i & j & k \\ 2 & 2 & -1 \\ 4 & 0 & 0\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 0 & 0\end{aligned}|i-|\begin{aligned}2 & -1 \\ 4 & 0\end{aligned}|j+|\begin{aligned}2 & 2 \\ 4 & 0\end{aligned}|k \\  & =(2\cdot 0-(-1)\cdot 0)i-(2\cdot 0-(-1)\cdot 4)j+(2\cdot 0-2\cdot 4)k \\  & =0i-4j-8k \\  & =⟨0,-4,-8⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{ST}$ and $\overset{\to }{SU}$ is

$$
\begin{aligned}A & =|\overset{\to }{ST}\times \overset{\to }{SU}| \\  & =\sqrt{{0}^{2}+(-4)^{2}+(-8)^{2}} \\  & =\sqrt{16+64} \\  & =\sqrt{80} \\  & =4\sqrt{5}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,STU$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{4\sqrt{5}}{2}=2\sqrt{5}.
$$

## Generated observed template/profile q-316530/37

Template: `q-316530`; profile: `blank`.

Calculate the area of the $△\,STU,$ if $S(-3,4,-4),$ $T(2,4,-2),$ $U(0,0,1).$

${A}_{△}=${{field-1}}

- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{ST}$ and $\overset{\to }{SU}:$

$$
\begin{aligned}\overset{\to }{ST} & =t-s \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{SU} & =u-s \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{ST}\times \overset{\to }{SU} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-0\cdot 3)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{ST}$ and $\overset{\to }{SU}$ is

$$
\begin{aligned}A & =|\overset{\to }{ST}\times \overset{\to }{SU}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{64+361+400} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,STU$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-316530/43

Template: `q-316530`; profile: `blank`.

Calculate the area of the $△\,STU,$ if $S(-4,0,-2),$ $T(-2,0,3),$ $U(-8,2,2).$

${A}_{△}=${{field-1}}

- $15$ — correct

First, we find the vectors $\overset{\to }{ST}$ and $\overset{\to }{SU}:$

$$
\begin{aligned}\overset{\to }{ST} & =t-s \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{SU} & =u-s \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{ST}\times \overset{\to }{SU} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-0\cdot (-4))k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{ST}$ and $\overset{\to }{SU}$ is

$$
\begin{aligned}A & =|\overset{\to }{ST}\times \overset{\to }{SU}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{100+784+16} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,STU$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}=15.
$$

## Original replay q-71106

Template: `q-71106`; profile: `observed/q-71106`.

Calculate the area of the $△\,WXY$, if $W(2,-3,1)$, $X(-2,1,2)$, $Y(3,-1,3).$

- $2\sqrt{10}$
- $\frac{\sqrt{261}}{2}$ — correct
- $\frac{15}{2}$
- $\frac{\sqrt{97}}{2}$
- $\sqrt{261}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(-2i+j+2k)-(2i-3j+k) \\  & =-4i+4j+k \\  & =⟨-4,4,1⟩ \\ \overset{\to }{WY} & =y-w \\  & =(3i-j+3k)-(2i-3j+k) \\  & =i+2j+2k \\  & =⟨1,2,2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ -4 & 4 & 1 \\ 1 & 2 & 2\end{aligned}| \\  & =|\begin{aligned}4 & 1 \\ 2 & 2\end{aligned}|i-|\begin{aligned}-4 & 1 \\ 1 & 2\end{aligned}|j+|\begin{aligned}-4 & 4 \\ 1 & 2\end{aligned}|k \\  & =(4\cdot 2-1\cdot 2)i-((-4)\cdot 2-1\cdot 1)j+((-4)\cdot 2-1\cdot 4)k \\  & =6i+9j-12k \\  & =⟨6,9,-12⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{{6}^{2}+{9}^{2}+{12}^{2}} \\  & =\sqrt{261}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{261}}{2}.
$$

## Generated observed template/profile q-71106/37

Template: `q-71106`; profile: `observed/q-71106`.

Calculate the area of the $△\,WXY$, if $W(-3,4,-4)$, $X(2,4,-2)$, $Y(0,0,1).$

- $\frac{25\sqrt{957}}{58}$
- $\frac{\sqrt{\frac{26675}{87}}}{2}$
- $\frac{\sqrt{825}}{2}$ — correct
- $2\sqrt{\frac{2750}{87}}$
- $\sqrt{825}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{WY} & =y-w \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-2\cdot (-4))i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+{20}^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-71106/43

Template: `q-71106`; profile: `observed/q-71106`.

Calculate the area of the $△\,WXY$, if $W(-4,0,-2)$, $X(-2,0,3)$, $Y(-8,2,2).$

- $\frac{\sqrt{\frac{9700}{29}}}{2}$
- $\frac{\sqrt{900}}{2}$ — correct
- $2\sqrt{\frac{1000}{29}}$
- $\frac{75\sqrt{29}}{29}$
- $\sqrt{900}$

First, we find the vectors $\overset{\to }{WX}$ and $\overset{\to }{WY}:$

$$
\begin{aligned}\overset{\to }{WX} & =x-w \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{WY} & =y-w \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{WX}\times \overset{\to }{WY} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-5\cdot 2)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WX}$ and $\overset{\to }{WY}$ is

$$
\begin{aligned}A & =|\overset{\to }{WX}\times \overset{\to }{WY}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WXY$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-71107

Template: `q-71107`; profile: `observed/q-71107`.

Calculate the area of the $△\,NPQ$, if $N(1,0,1)$, $P(2,2,3)$, $Q(2,1,1).$

- $\frac{5}{2}$
- $2$
- $\frac{\sqrt{3}}{2}$
- $3$
- $\frac{3}{2}$ — correct

First, we find the vectors $\overset{\to }{NP}$ and $\overset{\to }{NQ}:$

$$
\begin{aligned}\overset{\to }{NP} & =p-n \\  & =(2i+2j+3k)-(i+k) \\  & =i+2j+2k \\  & =⟨1,2,2⟩ \\ \overset{\to }{NQ} & =q-n \\  & =(2i+j+k)-(i+k) \\  & =i+j \\  & =⟨1,1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{NP}\times \overset{\to }{NQ} & =|\begin{aligned}i & j & k \\ 1 & 2 & 2 \\ 1 & 1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 1 & 0\end{aligned}|i-|\begin{aligned}1 & 2 \\ 1 & 0\end{aligned}|j+|\begin{aligned}1 & 2 \\ 1 & 1\end{aligned}|k \\  & =(2\cdot 0-1\cdot 2)i-(1\cdot 0-1\cdot 2)j+(1\cdot 1-1\cdot 2)k \\  & =-2i+2j-k \\  & =⟨-2,2,-1⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{NP}$ and $\overset{\to }{NQ}$ is

$$
\begin{aligned}A & =|\overset{\to }{NP}\times \overset{\to }{NQ}| \\  & =\sqrt{(-2)^{2}+{2}^{2}+(-1)^{2}} \\  & =\sqrt{9} \\  & =3.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,NPQ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3}{2}.
$$

## Generated observed template/profile q-71107/37

Template: `q-71107`; profile: `observed/q-71107`.

Calculate the area of the $△\,NPQ$, if $N(-3,4,-4)$, $P(2,4,-2)$, $Q(0,0,1).$

- $\frac{\sqrt{275}}{2}$
- $5\sqrt{33}$
- $\frac{10\sqrt{33}}{3}$
- $\frac{25\sqrt{33}}{6}$
- $\frac{5\sqrt{33}}{2}$ — correct

First, we find the vectors $\overset{\to }{NP}$ and $\overset{\to }{NQ}:$

$$
\begin{aligned}\overset{\to }{NP} & =p-n \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{NQ} & =q-n \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{NP}\times \overset{\to }{NQ} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{NP}$ and $\overset{\to }{NQ}$ is

$$
\begin{aligned}A & =|\overset{\to }{NP}\times \overset{\to }{NQ}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,NPQ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-71107/43

Template: `q-71107`; profile: `observed/q-71107`.

Calculate the area of the $△\,NPQ$, if $N(-4,0,-2)$, $P(-2,0,3)$, $Q(-8,2,2).$

- $30$
- $20$
- $25$
- $\frac{\sqrt{300}}{2}$
- $15$ — correct

First, we find the vectors $\overset{\to }{NP}$ and $\overset{\to }{NQ}:$

$$
\begin{aligned}\overset{\to }{NP} & =p-n \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{NQ} & =q-n \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{NP}\times \overset{\to }{NQ} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{NP}$ and $\overset{\to }{NQ}$ is

$$
\begin{aligned}A & =|\overset{\to }{NP}\times \overset{\to }{NQ}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,NPQ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{30}{2}.
$$

## Original replay q-71109

Template: `q-71109`; profile: `observed/q-71109`.

Calculate the area of the $△\,FGH$, if $F(1,1,2)$, $G(2,2,3)$, $H(1,0,1).$

- $1$
- $\frac{\sqrt{2}}{2}$ — correct
- $\frac{\sqrt{3}}{2}$
- $2\sqrt{2}$
- $\sqrt{2}$

First, we find the vectors $\overset{\to }{FG}$ and $\overset{\to }{FH}:$

$$
\begin{aligned}\overset{\to }{FG} & =g-f \\  & =(2i+2j+3k)-(i+j+2k) \\  & =i+j+k \\  & =⟨1,1,1⟩ \\ \overset{\to }{FH} & =h-f \\  & =(i+k)-(i+j+2k) \\  & =-j-k \\  & =⟨0,-1,-1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{FG}\times \overset{\to }{FH} & =|\begin{aligned}i & j & k \\ 1 & 1 & 1 \\ 0 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -1 & -1\end{aligned}|i-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|j+|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|k \\  & =(1\cdot (-1)-(-1)\cdot 1)i-(1\cdot (-1)-0\cdot 1)j+(1\cdot (-1)-0\cdot 1)k \\  & =j-k \\  & =⟨0,1,-1⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{FG}$ and $\overset{\to }{FH}$ is

$$
\begin{aligned}A & =|\overset{\to }{FG}\times \overset{\to }{FH}| \\  & =\sqrt{{0}^{2}+{1}^{2}+(-1)^{2}} \\  & =\sqrt{2}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,FGH$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{2}}{2}.
$$

## Generated observed template/profile q-71109/37

Template: `q-71109`; profile: `observed/q-71109`.

Calculate the area of the $△\,FGH$, if $F(-3,4,-4)$, $G(2,4,-2)$, $H(0,0,1).$

- $\frac{\sqrt{\frac{2475}{2}}}{2}$
- $2\sqrt{825}$
- $\frac{\sqrt{825}}{2}$ — correct
- $\frac{5\sqrt{66}}{2}$
- $\sqrt{825}$

First, we find the vectors $\overset{\to }{FG}$ and $\overset{\to }{FH}:$

$$
\begin{aligned}\overset{\to }{FG} & =g-f \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{FH} & =h-f \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{FG}\times \overset{\to }{FH} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-3\cdot 2)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{FG}$ and $\overset{\to }{FH}$ is

$$
\begin{aligned}A & =|\overset{\to }{FG}\times \overset{\to }{FH}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,FGH$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{825}}{2}.
$$

## Generated observed template/profile q-71109/43

Template: `q-71109`; profile: `observed/q-71109`.

Calculate the area of the $△\,FGH$, if $F(-4,0,-2)$, $G(-2,0,3)$, $H(-8,2,2).$

- $2\sqrt{900}$
- $\frac{\sqrt{900}}{2}$ — correct
- $15\sqrt{2}$
- $\frac{\sqrt{1350}}{2}$
- $\sqrt{900}$

First, we find the vectors $\overset{\to }{FG}$ and $\overset{\to }{FH}:$

$$
\begin{aligned}\overset{\to }{FG} & =g-f \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{FH} & =h-f \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{FG}\times \overset{\to }{FH} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-(-4)\cdot 5)j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{FG}$ and $\overset{\to }{FH}$ is

$$
\begin{aligned}A & =|\overset{\to }{FG}\times \overset{\to }{FH}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,FGH$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{900}}{2}.
$$

## Original replay q-71111

Template: `q-71111`; profile: `observed/q-71111`.

Calculate the area of the $△\,CDE$, if $C(1,-2,3)$, $D(1,-3,3)$, $E(1,1,1).$

- $2$
- $\sqrt{3}$
- $1$ — correct
- $\sqrt{2}$
- $3$

First, we find the vectors $\overset{\to }{CD}$ and $\overset{\to }{CE}:$

$$
\begin{aligned}\overset{\to }{CD} & =d-c \\  & =(i-3j+3k)-(i-2j+3k) \\  & =-j \\  & =⟨0,-1,0⟩ \\ \overset{\to }{CE} & =e-c \\  & =(i+j+k)-(i-2j+3k) \\  & =3j-2k \\  & =⟨0,3,-2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{CD}\times \overset{\to }{CE} & =|\begin{aligned}i & j & k \\ 0 & -1 & 0 \\ 0 & 3 & -2\end{aligned}| \\  & =|\begin{aligned}-1 & 0 \\ 3 & -2\end{aligned}|i-|\begin{aligned}0 & 0 \\ 0 & -2\end{aligned}|j+|\begin{aligned}0 & -1 \\ 0 & 3\end{aligned}|k \\  & =((-1)\cdot (-2)-3\cdot 0)i-(0\cdot (-2)-0\cdot 0)j+(0\cdot 3-0\cdot (-1))k \\  & =2i \\  & =⟨2,0,0⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{CD}$ and $\overset{\to }{CE}$ is

$$
\begin{aligned}A & =|\overset{\to }{CD}\times \overset{\to }{CE}| \\  & =\sqrt{{2}^{2}+{0}^{2}+{0}^{2}} \\  & =\sqrt{4} \\  & =2.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,CDE$ is

$$
{A}_{△}=\frac{1}{2}A=1.
$$

## Generated observed template/profile q-71111/37

Template: `q-71111`; profile: `observed/q-71111`.

Calculate the area of the $△\,CDE$, if $C(-3,4,-4)$, $D(2,4,-2)$, $E(0,0,1).$

- $\frac{5\sqrt{33}}{2}$ — correct
- $\sqrt{\frac{825}{2}}$
- $\sqrt{\frac{2475}{4}}$
- $5\sqrt{33}$
- $\frac{15\sqrt{33}}{2}$

First, we find the vectors $\overset{\to }{CD}$ and $\overset{\to }{CE}:$

$$
\begin{aligned}\overset{\to }{CD} & =d-c \\  & =(2i+4j-2k)-(-3i+4j-4k) \\  & =5i+2k \\  & =⟨5,0,2⟩ \\ \overset{\to }{CE} & =e-c \\  & =(k)-(-3i+4j-4k) \\  & =3i-4j+5k \\  & =⟨3,-4,5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{CD}\times \overset{\to }{CE} & =|\begin{aligned}i & j & k \\ 5 & 0 & 2 \\ 3 & -4 & 5\end{aligned}| \\  & =|\begin{aligned}0 & 2 \\ -4 & 5\end{aligned}|i-|\begin{aligned}5 & 2 \\ 3 & 5\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 & -4\end{aligned}|k \\  & =(0\cdot 5-(-4)\cdot 2)i-(5\cdot 5-2\cdot 3)j+(5\cdot (-4)-3\cdot 0)k \\  & =8i-19j-20k \\  & =⟨8,-19,-20⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{CD}$ and $\overset{\to }{CE}$ is

$$
\begin{aligned}A & =|\overset{\to }{CD}\times \overset{\to }{CE}| \\  & =\sqrt{{8}^{2}+(-19)^{2}+(-20)^{2}} \\  & =\sqrt{825} \\  & =5\sqrt{33}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,CDE$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5\sqrt{33}}{2}.
$$

## Generated observed template/profile q-71111/43

Template: `q-71111`; profile: `observed/q-71111`.

Calculate the area of the $△\,CDE$, if $C(-4,0,-2)$, $D(-2,0,3)$, $E(-8,2,2).$

- $\sqrt{450}$
- $\sqrt{675}$
- $30$
- $15$ — correct
- $45$

First, we find the vectors $\overset{\to }{CD}$ and $\overset{\to }{CE}:$

$$
\begin{aligned}\overset{\to }{CD} & =d-c \\  & =(-2i+3k)-(-4i-2k) \\  & =2i+5k \\  & =⟨2,0,5⟩ \\ \overset{\to }{CE} & =e-c \\  & =(-8i+2j+2k)-(-4i-2k) \\  & =-4i+2j+4k \\  & =⟨-4,2,4⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{CD}\times \overset{\to }{CE} & =|\begin{aligned}i & j & k \\ 2 & 0 & 5 \\ -4 & 2 & 4\end{aligned}| \\  & =|\begin{aligned}0 & 5 \\ 2 & 4\end{aligned}|i-|\begin{aligned}2 & 5 \\ -4 & 4\end{aligned}|j+|\begin{aligned}2 & 0 \\ -4 & 2\end{aligned}|k \\  & =(0\cdot 4-2\cdot 5)i-(2\cdot 4-5\cdot (-4))j+(2\cdot 2-(-4)\cdot 0)k \\  & =-10i-28j+4k \\  & =⟨-10,-28,4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{CD}$ and $\overset{\to }{CE}$ is

$$
\begin{aligned}A & =|\overset{\to }{CD}\times \overset{\to }{CE}| \\  & =\sqrt{(-10)^{2}+(-28)^{2}+{4}^{2}} \\  & =\sqrt{900} \\  & =30.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,CDE$ is

$$
{A}_{△}=\frac{1}{2}A=15.
$$

## Authored easy blank peer 0

Template: `authored_easy_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(2,2,-4)$, $B(2,4,-3)$, $C(3,2,-3).$

${A}_{△}=${{field-1}}

- $\frac{3}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+4j-3k)-(2i+2j-4k) \\  & =2j+k \\  & =⟨0,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j-3k)-(2i+2j-4k) \\  & =i+k \\  & =⟨1,0,1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 0 & 2 & 1 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|j+|\begin{aligned}0 & 2 \\ 1 & 0\end{aligned}|k \\  & =(2\cdot 1-1\cdot 0)i-(0\cdot 1-1\cdot 1)j+(0\cdot 0-2\cdot 1)k \\  & =2i+j-2k \\  & =⟨2,1,-2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}} \\  & =\sqrt{9} \\  & =3.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3}{2}.
$$

## Authored easy blank peer 1

Template: `authored_easy_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(-2,0,-3)$, $B(-2,2,-2)$, $C(0,-1,-3).$

${A}_{△}=${{field-1}}

- $\frac{\sqrt{21}}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+2j-2k)-(-2i-3k) \\  & =2j+k \\  & =⟨0,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-j-3k)-(-2i-3k) \\  & =2i-j \\  & =⟨2,-1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 0 & 2 & 1 \\ 2 & -1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ -1 & 0\end{aligned}|i-|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|j+|\begin{aligned}0 & 2 \\ 2 & -1\end{aligned}|k \\  & =(2\cdot 0-1\cdot (-1))i-(0\cdot 0-1\cdot 2)j+(0\cdot (-1)-2\cdot 2)k \\  & =i+2j-4k \\  & =⟨1,2,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{1}^{2}+{2}^{2}+(-4)^{2}} \\  & =\sqrt{21}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{21}}{2}.
$$

## Authored easy radio peer 0

Template: `authored_easy_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(2,2,-4)$, $B(2,4,-3)$, $C(3,2,-3).$

- $\frac{1}{2}$
- $\frac{3}{2}$ — correct
- $\frac{\sqrt{10}}{2}$
- $3$
- $\frac{9}{2}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+4j-3k)-(2i+2j-4k) \\  & =2j+k \\  & =⟨0,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j-3k)-(2i+2j-4k) \\  & =i+k \\  & =⟨1,0,1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 0 & 2 & 1 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|j+|\begin{aligned}0 & 2 \\ 1 & 0\end{aligned}|k \\  & =(2\cdot 1-1\cdot 0)i-(0\cdot 1-1\cdot 1)j+(0\cdot 0-2\cdot 1)k \\  & =2i+j-2k \\  & =⟨2,1,-2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+{1}^{2}+(-2)^{2}} \\  & =\sqrt{9} \\  & =3.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3}{2}.
$$

## Authored easy radio peer 1

Template: `authored_easy_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(-2,0,-3)$, $B(-2,2,-2)$, $C(0,-1,-3).$

- $\frac{\sqrt{21}}{2}$ — correct
- $\sqrt{21}$
- $\frac{5}{2}$
- $1$
- $\frac{21}{2}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+2j-2k)-(-2i-3k) \\  & =2j+k \\  & =⟨0,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-j-3k)-(-2i-3k) \\  & =2i-j \\  & =⟨2,-1,0⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 0 & 2 & 1 \\ 2 & -1 & 0\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ -1 & 0\end{aligned}|i-|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|j+|\begin{aligned}0 & 2 \\ 2 & -1\end{aligned}|k \\  & =(2\cdot 0-1\cdot (-1))i-(0\cdot 0-1\cdot 2)j+(0\cdot (-1)-2\cdot 2)k \\  & =i+2j-4k \\  & =⟨1,2,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{1}^{2}+{2}^{2}+(-4)^{2}} \\  & =\sqrt{21}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{21}}{2}.
$$

## Authored moderate blank peer 0

Template: `authored_moderate_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(2,2,-4)$, $B(1,5,-2)$, $C(3,1,-2).$

${A}_{△}=${{field-1}}

- $\sqrt{21}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+5j-2k)-(2i+2j-4k) \\  & =-i+3j+2k \\  & =⟨-1,3,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+j-2k)-(2i+2j-4k) \\  & =i-j+2k \\  & =⟨1,-1,2⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & 3 & 2 \\ 1 & -1 & 2\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ -1 & 2\end{aligned}|i-|\begin{aligned}-1 & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}-1 & 3 \\ 1 & -1\end{aligned}|k \\  & =(3\cdot 2-2\cdot (-1))i-((-1)\cdot 2-2\cdot 1)j+((-1)\cdot (-1)-3\cdot 1)k \\  & =8i+4j-2k \\  & =⟨8,4,-2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{8}^{2}+{4}^{2}+(-2)^{2}} \\  & =\sqrt{84} \\  & =2\sqrt{21}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{21}}{2}=\sqrt{21}.
$$

## Authored moderate blank peer 1

Template: `authored_moderate_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(-2,-3,0)$, $B(-6,-1,2)$, $C(0,2,1).$

${A}_{△}=${{field-1}}

- $4\sqrt{11}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-6i-j+2k)-(-2i-3j) \\  & =-4i+2j+2k \\  & =⟨-4,2,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2j+k)-(-2i-3j) \\  & =2i+5j+k \\  & =⟨2,5,1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -4 & 2 & 2 \\ 2 & 5 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 5 & 1\end{aligned}|i-|\begin{aligned}-4 & 2 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-4 & 2 \\ 2 & 5\end{aligned}|k \\  & =(2\cdot 1-2\cdot 5)i-((-4)\cdot 1-2\cdot 2)j+((-4)\cdot 5-2\cdot 2)k \\  & =-8i+8j-24k \\  & =⟨-8,8,-24⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-8)^{2}+{8}^{2}+(-24)^{2}} \\  & =\sqrt{704} \\  & =8\sqrt{11}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{8\sqrt{11}}{2}=4\sqrt{11}.
$$

## Authored moderate radio peer 0

Template: `authored_moderate_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(1,-1,4)$, $B(-2,-2,1)$, $C(-3,3,3).$

- $253$
- $\frac{\sqrt{506}}{2}$ — correct
- $\frac{11}{2}$
- $\sqrt{506}$
- $\frac{\sqrt{627}}{2}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i-2j+k)-(i-j+4k) \\  & =-3i-j-3k \\  & =⟨-3,-1,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3i+3j+3k)-(i-j+4k) \\  & =-4i+4j-k \\  & =⟨-4,4,-1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -3 & -1 & -3 \\ -4 & 4 & -1\end{aligned}| \\  & =|\begin{aligned}-1 & -3 \\ 4 & -1\end{aligned}|i-|\begin{aligned}-3 & -3 \\ -4 & -1\end{aligned}|j+|\begin{aligned}-3 & -1 \\ -4 & 4\end{aligned}|k \\  & =((-1)\cdot (-1)-(-3)\cdot 4)i-((-3)\cdot (-1)-(-3)\cdot (-4))j+((-3)\cdot 4-(-1)\cdot (-4))k \\  & =13i+9j-16k \\  & =⟨13,9,-16⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{13}^{2}+{9}^{2}+(-16)^{2}} \\  & =\sqrt{506}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{506}}{2}.
$$

## Authored moderate radio peer 1

Template: `authored_moderate_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(-2,-3,0)$, $B(-6,-1,2)$, $C(0,2,1).$

- $352$
- $2$
- $6\sqrt{5}$
- $4\sqrt{11}$ — correct
- $8\sqrt{11}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-6i-j+2k)-(-2i-3j) \\  & =-4i+2j+2k \\  & =⟨-4,2,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2j+k)-(-2i-3j) \\  & =2i+5j+k \\  & =⟨2,5,1⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -4 & 2 & 2 \\ 2 & 5 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ 5 & 1\end{aligned}|i-|\begin{aligned}-4 & 2 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-4 & 2 \\ 2 & 5\end{aligned}|k \\  & =(2\cdot 1-2\cdot 5)i-((-4)\cdot 1-2\cdot 2)j+((-4)\cdot 5-2\cdot 2)k \\  & =-8i+8j-24k \\  & =⟨-8,8,-24⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-8)^{2}+{8}^{2}+(-24)^{2}} \\  & =\sqrt{704} \\  & =8\sqrt{11}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{8\sqrt{11}}{2}=4\sqrt{11}.
$$

## Authored hard blank peer 0

Template: `authored_hard_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(0,3,1)$, $B(2,10,8)$, $C(-4,4,-4).$

${A}_{△}=${{field-1}}

- $3\sqrt{83}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+10j+8k)-(3j+k) \\  & =2i+7j+7k \\  & =⟨2,7,7⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-4i+4j-4k)-(3j+k) \\  & =-4i+j-5k \\  & =⟨-4,1,-5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 7 & 7 \\ -4 & 1 & -5\end{aligned}| \\  & =|\begin{aligned}7 & 7 \\ 1 & -5\end{aligned}|i-|\begin{aligned}2 & 7 \\ -4 & -5\end{aligned}|j+|\begin{aligned}2 & 7 \\ -4 & 1\end{aligned}|k \\  & =(7\cdot (-5)-7\cdot 1)i-(2\cdot (-5)-7\cdot (-4))j+(2\cdot 1-7\cdot (-4))k \\  & =-42i-18j+30k \\  & =⟨-42,-18,30⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-42)^{2}+(-18)^{2}+{30}^{2}} \\  & =\sqrt{2988} \\  & =6\sqrt{83}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{83}}{2}=3\sqrt{83}.
$$

## Authored hard blank peer 1

Template: `authored_hard_blank`; profile: `blank`.

Calculate the area of the $△\,ABC$, if $A(-4,3,0)$, $B(0,8,-4)$, $C(-2,-3,7).$

${A}_{△}=${{field-1}}

- $\frac{\sqrt{2573}}{2}$ — correct

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8j-4k)-(-4i+3j) \\  & =4i+5j-4k \\  & =⟨4,5,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-3j+7k)-(-4i+3j) \\  & =2i-6j+7k \\  & =⟨2,-6,7⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 4 & 5 & -4 \\ 2 & -6 & 7\end{aligned}| \\  & =|\begin{aligned}5 & -4 \\ -6 & 7\end{aligned}|i-|\begin{aligned}4 & -4 \\ 2 & 7\end{aligned}|j+|\begin{aligned}4 & 5 \\ 2 & -6\end{aligned}|k \\  & =(5\cdot 7-(-4)\cdot (-6))i-(4\cdot 7-(-4)\cdot 2)j+(4\cdot (-6)-5\cdot 2)k \\  & =11i-36j-34k \\  & =⟨11,-36,-34⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{11}^{2}+(-36)^{2}+(-34)^{2}} \\  & =\sqrt{2573}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{2573}}{2}.
$$

## Authored hard radio peer 0

Template: `authored_hard_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(0,3,1)$, $B(2,10,8)$, $C(-4,4,-4).$

- $3\sqrt{119}$
- $18$
- $3\sqrt{83}$ — correct
- $6\sqrt{83}$
- $1494$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+10j+8k)-(3j+k) \\  & =2i+7j+7k \\  & =⟨2,7,7⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-4i+4j-4k)-(3j+k) \\  & =-4i+j-5k \\  & =⟨-4,1,-5⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 7 & 7 \\ -4 & 1 & -5\end{aligned}| \\  & =|\begin{aligned}7 & 7 \\ 1 & -5\end{aligned}|i-|\begin{aligned}2 & 7 \\ -4 & -5\end{aligned}|j+|\begin{aligned}2 & 7 \\ -4 & 1\end{aligned}|k \\  & =(7\cdot (-5)-7\cdot 1)i-(2\cdot (-5)-7\cdot (-4))j+(2\cdot 1-7\cdot (-4))k \\  & =-42i-18j+30k \\  & =⟨-42,-18,30⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-42)^{2}+(-18)^{2}+{30}^{2}} \\  & =\sqrt{2988} \\  & =6\sqrt{83}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{83}}{2}=3\sqrt{83}.
$$

## Authored hard radio peer 1

Template: `authored_hard_radio`; profile: `authored_operations`.

Calculate the area of the $△\,ABC$, if $A(-4,3,0)$, $B(0,8,-4)$, $C(-2,-3,7).$

- $\sqrt{2573}$
- $\frac{\sqrt{5073}}{2}$
- $25$
- $\frac{\sqrt{2573}}{2}$ — correct
- $\frac{2573}{2}$

First, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8j-4k)-(-4i+3j) \\  & =4i+5j-4k \\  & =⟨4,5,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-3j+7k)-(-4i+3j) \\  & =2i-6j+7k \\  & =⟨2,-6,7⟩\end{aligned}
$$

Now, using the formula to compute the cross product, we get

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 4 & 5 & -4 \\ 2 & -6 & 7\end{aligned}| \\  & =|\begin{aligned}5 & -4 \\ -6 & 7\end{aligned}|i-|\begin{aligned}4 & -4 \\ 2 & 7\end{aligned}|j+|\begin{aligned}4 & 5 \\ 2 & -6\end{aligned}|k \\  & =(5\cdot 7-(-4)\cdot (-6))i-(4\cdot 7-(-4)\cdot 2)j+(4\cdot (-6)-5\cdot 2)k \\  & =11i-36j-34k \\  & =⟨11,-36,-34⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{11}^{2}+(-36)^{2}+(-34)^{2}} \\  & =\sqrt{2573}.\end{aligned}
$$

Finally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{2573}}{2}.
$$

