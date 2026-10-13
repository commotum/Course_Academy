# Altitude generator review

Original raw strings are preserved in source.json. Changed records use the public API. All answers shown here are author review data.


## q-20027 original

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(2,1,2)$, $B(1,2,1)$, $C(3,2,3).$


Original full bank: $\frac{2\sqrt{6}}{3}$, $\frac{\sqrt{6}}{3}$, $\frac{2\sqrt{3}}{3}$, $\frac{2\sqrt{2}}{3}$, $\frac{3\sqrt{6}}{2}$

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j+k)-(2i+j+2k) \\  & =-i+j-k \\  & =⟨-1,1,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j+3k)-(2i+j+2k) \\  & =i+j+k \\  & =⟨1,1,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & 1 & -1 \\ 1 & 1 & 1\end{aligned}| \\  & =|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|i-|\begin{aligned}-1 & -1 \\ 1 & 1\end{aligned}|j+|\begin{aligned}-1 & 1 \\ 1 & 1\end{aligned}|k \\  & =(1\cdot 1-1\cdot (-1))i-((-1)\cdot 1-1\cdot (-1))j+((-1)\cdot 1-1\cdot 1)k \\  & =2i-2k \\  & =⟨2,0,-2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+{0}^{2}+(-2)^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-1)^{2}+{1}^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{2} & =\frac{1}{2}CH\cdot \sqrt{3} \\ 2\sqrt{2} & =CH\cdot \sqrt{3} \\ CH & =\frac{2\sqrt{2}}{\sqrt{3}} \\ CH & =\frac{2\sqrt{6}}{3}.\end{aligned}
$$


### source replay q-20027

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(2,1,2)$, $B(1,2,1)$, $C(3,2,3).$

:answer-field.type/radio
- $\frac{\sqrt{6}}{3}$
- $\frac{3\sqrt{6}}{2}$
- $\frac{2\sqrt{2}}{3}$
- $\frac{2\sqrt{3}}{3}$
- $\frac{2\sqrt{6}}{3}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j+k)-(2i+j+2k) \\  & =-i+j-k \\  & =⟨-1,1,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j+3k)-(2i+j+2k) \\  & =i+j+k \\  & =⟨1,1,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & 1 & -1 \\ 1 & 1 & 1\end{aligned}| \\  & =|\begin{aligned}1 & -1 \\ 1 & 1\end{aligned}|i-|\begin{aligned}-1 & -1 \\ 1 & 1\end{aligned}|j+|\begin{aligned}-1 & 1 \\ 1 & 1\end{aligned}|k \\  & =(1\cdot 1-1\cdot (-1))i-((-1)\cdot 1-1\cdot (-1))j+((-1)\cdot 1-1\cdot 1)k \\  & =2i-2k \\  & =⟨2,0,-2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+{0}^{2}+(-2)^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-1)^{2}+{1}^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{2} & =\frac{1}{2}CH\cdot \sqrt{3} \\ 2\sqrt{2} & =CH\cdot \sqrt{3} \\ CH & =\frac{2\sqrt{2}}{\sqrt{3}} \\ CH & =\frac{2\sqrt{6}}{3}.\end{aligned}
$$


### changed-parameter observed presentation q-20027

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,-1,-1)$, $B(1,2,-5)$, $C(-5,1,-6).$

:answer-field.type/radio
- $\frac{9\sqrt{118}}{8}$
- $\frac{\sqrt{354}}{6}$
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{59}}{2}$
- $\frac{\sqrt{118}}{4}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}CH\cdot \sqrt{34} \\ \sqrt{1003} & =CH\cdot \sqrt{34} \\ CH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ CH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-20028 original

Calculate the length of the altitude $RH$ of the $△PRQ$, if $P(1,-2, 3)$, $Q(3, 2, 3)$, $R(2, 1, 4)$.

> A calculator is required to answer this question.


Original full bank: $\frac{2\sqrt{30}}{5}$, $\frac{\sqrt{6}}{6}$, $\frac{\sqrt{30}}{5}$, $\frac{\sqrt{5}}{5}$, $\frac{\sqrt{30}}{6}$

No source worked solution or correct designation. Reconstruction is authored.


### source replay q-20028

Calculate the length of the altitude $RH$ of the $△PRQ$, if $P(1,-2, 3)$, $Q(3, 2, 3)$, $R(2, 1, 4)$.

> A calculator is required to answer this question.

:answer-field.type/radio
- $\frac{\sqrt{6}}{6}$
- $\frac{\sqrt{30}}{6}$
- $\frac{\sqrt{5}}{5}$
- $\frac{\sqrt{30}}{5}$
- $\frac{2\sqrt{30}}{5}$

Worked solution

Note that the length of the altitude $RH$ can be related to the area of $△\,PRQ$ as follows:

$$
{A}_{△}=\frac{1}{2}RH\cdot PQ
$$

So, to find $RH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(3i+2j+3k)-(i-2j+3k) \\  & =2i+4j \\  & =⟨2,4,0⟩ \\ \overset{\to }{PR} & =r-p \\  & =(2i+j+4k)-(i-2j+3k) \\  & =i+3j+k \\  & =⟨1,3,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 2 & 4 & 0 \\ 1 & 3 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 0 \\ 3 & 1\end{aligned}|i-|\begin{aligned}2 & 0 \\ 1 & 1\end{aligned}|j+|\begin{aligned}2 & 4 \\ 1 & 3\end{aligned}|k \\  & =(4\cdot 1-3\cdot 0)i-(2\cdot 1-1\cdot 0)j+(2\cdot 3-1\cdot 4)k \\  & =4i-2j+2k \\  & =⟨4,-2,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{4}^{2}+(-2)^{2}+{2}^{2}} \\  & =\sqrt{24} \\  & =2\sqrt{6}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PRQ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{6}}{2}=\sqrt{6}.
$$

Let's also compute $PQ$ since it appears in the formula:

$$
\begin{aligned}PQ & =|\overset{\to }{PQ}| \\  & =\sqrt{{2}^{2}+{4}^{2}+{0}^{2}} \\  & =2\sqrt{5}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}RH\cdot PQ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}RH\cdot PQ \\ \sqrt{6} & =\frac{1}{2}RH\cdot 2\sqrt{5} \\ \sqrt{6} & =RH\cdot \sqrt{5} \\ RH & =\frac{\sqrt{6}}{\sqrt{5}} \\ RH & =\frac{\sqrt{30}}{5}.\end{aligned}
$$


### changed-parameter observed presentation q-20028

Calculate the length of the altitude $RH$ of the $△PRQ$, if $P(-2,-1, -1)$, $Q(1, 2, -5)$, $R(-5, 1, -6)$.

> A calculator is required to answer this question.

:answer-field.type/radio
- $\frac{5\sqrt{118}}{12}$
- $\frac{\sqrt{177}}{6}$
- $\sqrt{118}$
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{590}}{12}$

Worked solution

Note that the length of the altitude $RH$ can be related to the area of $△\,PRQ$ as follows:

$$
{A}_{△}=\frac{1}{2}RH\cdot PQ
$$

So, to find $RH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PRQ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $PQ$ since it appears in the formula:

$$
\begin{aligned}PQ & =|\overset{\to }{PQ}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}RH\cdot PQ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}RH\cdot PQ \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}RH\cdot \sqrt{34} \\ \sqrt{1003} & =RH\cdot \sqrt{34} \\ RH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ RH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-128006 original

Calculate the length of the altitude $CH$ of the $△\,ABC,$ if $A(4,-1,1),$ $B(0,-3,4),$ $C(2,1,4).$


Original full bank: $\frac{6\sqrt{33}}{11}$, $\frac{9\sqrt{29}}{29}$, $\frac{18\sqrt{10}}{5}$, $\frac{9\sqrt{10}}{5}$, $\frac{18\sqrt{29}}{29}$

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-3j+4k)-(4i-j+k) \\  & =-4i-2j+3k \\  & =⟨-4,-2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+j+4k)-(4i-j+k) \\  & =-2i+2j+3k \\  & =⟨-2,2,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -4 & -2 & 3 \\ -2 & 2 & 3\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 2 & 3\end{aligned}|i-|\begin{aligned}-4 & 3 \\ -2 & 3\end{aligned}|j+|\begin{aligned}-4 & -2 \\ -2 & 2\end{aligned}|k \\  & =((-2)\cdot 3-2\cdot 3)i-((-4)\cdot 3-(-2)\cdot 3)j+((-4)\cdot 2-(-2)\cdot (-2))k \\  & =-12i+6j-12k \\  & =⟨-12,6,-12⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-12)^{2}+{6}^{2}+(-12)^{2}} \\  & =\sqrt{324} \\  & =18.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{18}{2}=9.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-4)^{2}+(-2)^{2}+{3}^{2}} \\  & =\sqrt{29}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ 9 & =\frac{1}{2}CH\cdot \sqrt{29} \\ 18 & =CH\cdot \sqrt{29} \\ CH & =\frac{18}{\sqrt{29}} \\ CH & =\frac{18\sqrt{29}}{29}.\end{aligned}
$$


### source replay q-128006

Calculate the length of the altitude $CH$ of the $△\,ABC,$ if $A(4,-1,1),$ $B(0,-3,4),$ $C(2,1,4).$

:answer-field.type/radio
- $\frac{9\sqrt{29}}{29}$
- $\frac{18\sqrt{29}}{29}$
- $\frac{9\sqrt{10}}{5}$
- $\frac{18\sqrt{10}}{5}$
- $\frac{6\sqrt{33}}{11}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-3j+4k)-(4i-j+k) \\  & =-4i-2j+3k \\  & =⟨-4,-2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+j+4k)-(4i-j+k) \\  & =-2i+2j+3k \\  & =⟨-2,2,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -4 & -2 & 3 \\ -2 & 2 & 3\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 2 & 3\end{aligned}|i-|\begin{aligned}-4 & 3 \\ -2 & 3\end{aligned}|j+|\begin{aligned}-4 & -2 \\ -2 & 2\end{aligned}|k \\  & =((-2)\cdot 3-2\cdot 3)i-((-4)\cdot 3-(-2)\cdot 3)j+((-4)\cdot 2-(-2)\cdot (-2))k \\  & =-12i+6j-12k \\  & =⟨-12,6,-12⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-12)^{2}+{6}^{2}+(-12)^{2}} \\  & =\sqrt{324} \\  & =18.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{18}{2}=9.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-4)^{2}+(-2)^{2}+{3}^{2}} \\  & =\sqrt{29}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ 9 & =\frac{1}{2}CH\cdot \sqrt{29} \\ 18 & =CH\cdot \sqrt{29} \\ CH & =\frac{18}{\sqrt{29}} \\ CH & =\frac{18\sqrt{29}}{29}.\end{aligned}
$$


### changed-parameter observed presentation q-128006

Calculate the length of the altitude $CH$ of the $△\,ABC,$ if $A(-2,-1,-1),$ $B(1,2,-5),$ $C(-5,1,-6).$

:answer-field.type/radio
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{8555}}{10}$
- $\frac{\sqrt{112926}}{66}$
- $\frac{\sqrt{8555}}{5}$
- $\frac{\sqrt{118}}{4}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}CH\cdot \sqrt{34} \\ \sqrt{1003} & =CH\cdot \sqrt{34} \\ CH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ CH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-128008 original

Calculate the length of the altitude $RH$ of the $△\,PRQ,$ if $P(3,0,4),$ $Q(2,3,1),$ $R(0,3,1).$


Original full bank: $\frac{3\sqrt{38}}{38}$, $\frac{3\sqrt{38}}{19}$, $6$, $\frac{6\sqrt{38}}{19}$, $2$

Note that the length of the altitude $RH$ can be related to the area of $△\,PQR$ as follows:

$$
{A}_{△}=\frac{1}{2}RH\cdot PQ
$$

So, to find $RH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+3j+k)-(3i+4k) \\  & =-i+3j-3j \\  & =⟨-1,3,-3⟩ \\ \overset{\to }{PR} & =r-p \\  & =(3j+k)-(3i+4k) \\  & =-3i+3j-3k \\  & =⟨-3,3,-3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ -1 & 3 & -3 \\ -3 & 3 & -3\end{aligned}| \\  & =|\begin{aligned}3 & -3 \\ 3 & -3\end{aligned}|i-|\begin{aligned}-1 & -3 \\ -3 & -3\end{aligned}|j+|\begin{aligned}-1 & 3 \\ -3 & 3\end{aligned}|k \\  & =(3\cdot (-3)-3\cdot (-3))i-((-1)\cdot (-3)-(-3)\cdot (-3))j+((-1)\cdot 3-(-3)\cdot 3)k \\  & =6j+6k \\  & =⟨0,6,6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{0}^{2}+{6}^{2}+{6}^{2}} \\  & =\sqrt{72} \\  & =6\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{2}}{2}=3\sqrt{2}.
$$

Let's also compute $PQ$ since it appears in the formula:

$$
\begin{aligned}PQ & =|\overset{\to }{PQ}| \\  & =\sqrt{(-1)^{2}+{3}^{2}+(-3)^{2}} \\  & =\sqrt{19}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}RH\cdot PQ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}RH\cdot PQ \\ 3\sqrt{2} & =\frac{1}{2}RH\cdot \sqrt{19} \\ 6\sqrt{2} & =RH\cdot \sqrt{19} \\ RH & =\frac{6\sqrt{2}}{\sqrt{19}} \\ RH & =\frac{6\sqrt{38}}{19}.\end{aligned}
$$


### source replay q-128008

Calculate the length of the altitude $RH$ of the $△\,PRQ,$ if $P(3,0,4),$ $Q(2,3,1),$ $R(0,3,1).$

:answer-field.type/radio
- $\frac{3\sqrt{38}}{19}$
- $2$
- $\frac{6\sqrt{38}}{19}$
- $6$
- $\frac{3\sqrt{38}}{38}$

Worked solution

Note that the length of the altitude $RH$ can be related to the area of $△\,PQR$ as follows:

$$
{A}_{△}=\frac{1}{2}RH\cdot PQ
$$

So, to find $RH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(2i+3j+k)-(3i+4k) \\  & =-i+3j-3k \\  & =⟨-1,3,-3⟩ \\ \overset{\to }{PR} & =r-p \\  & =(3j+k)-(3i+4k) \\  & =-3i+3j-3k \\  & =⟨-3,3,-3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ -1 & 3 & -3 \\ -3 & 3 & -3\end{aligned}| \\  & =|\begin{aligned}3 & -3 \\ 3 & -3\end{aligned}|i-|\begin{aligned}-1 & -3 \\ -3 & -3\end{aligned}|j+|\begin{aligned}-1 & 3 \\ -3 & 3\end{aligned}|k \\  & =(3\cdot (-3)-3\cdot (-3))i-((-1)\cdot (-3)-(-3)\cdot (-3))j+((-1)\cdot 3-(-3)\cdot 3)k \\  & =6j+6k \\  & =⟨0,6,6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{{0}^{2}+{6}^{2}+{6}^{2}} \\  & =\sqrt{72} \\  & =6\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{2}}{2}=3\sqrt{2}.
$$

Let's also compute $PQ$ since it appears in the formula:

$$
\begin{aligned}PQ & =|\overset{\to }{PQ}| \\  & =\sqrt{(-1)^{2}+{3}^{2}+(-3)^{2}} \\  & =\sqrt{19}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}RH\cdot PQ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}RH\cdot PQ \\ 3\sqrt{2} & =\frac{1}{2}RH\cdot \sqrt{19} \\ 6\sqrt{2} & =RH\cdot \sqrt{19} \\ RH & =\frac{6\sqrt{2}}{\sqrt{19}} \\ RH & =\frac{6\sqrt{38}}{19}.\end{aligned}
$$


### changed-parameter observed presentation q-128008

Calculate the length of the altitude $RH$ of the $△\,PRQ,$ if $P(-2,-1,-1),$ $Q(1,2,-5),$ $R(-5,1,-6).$

:answer-field.type/radio
- $\frac{\sqrt{1121}}{6}$
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{118}}{8}$
- $\frac{\sqrt{1121}}{2}$
- $\frac{\sqrt{118}}{4}$

Worked solution

Note that the length of the altitude $RH$ can be related to the area of $△\,PQR$ as follows:

$$
{A}_{△}=\frac{1}{2}RH\cdot PQ
$$

So, to find $RH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{PQ}$ and $\overset{\to }{PR}:$

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{PR} & =r-p \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{PQ}\times \overset{\to }{PR} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{PQ}$ and $\overset{\to }{PR}$ is

$$
\begin{aligned}A & =|\overset{\to }{PQ}\times \overset{\to }{PR}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,PQR$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $PQ$ since it appears in the formula:

$$
\begin{aligned}PQ & =|\overset{\to }{PQ}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}RH\cdot PQ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}RH\cdot PQ \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}RH\cdot \sqrt{34} \\ \sqrt{1003} & =RH\cdot \sqrt{34} \\ RH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ RH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-128013 original

Calculate the length of the altitude $MH$ of the $△\,LMN,$ if $L(-1,4,1),$ $M(0,3,4),$ $N(1,4,2).$


Original full bank: $\sqrt{3}$, $\sqrt{5}$, $\sqrt{10}$, $\sqrt{2}$, $\sqrt{6}$

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(3j+4k)-(-i+4j+k) \\  & =i-j+3k \\  & =⟨1,-1,3⟩ \\ \overset{\to }{LN} & =n-l \\  & =(i+4j+2k)-(-i+4j+k) \\  & =2i+k \\  & =⟨2,0,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 1 & -1 & 3 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}-1 & 3 \\ 0 & 1\end{aligned}|i-|\begin{aligned}1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}1 & -1 \\ 2 & 0\end{aligned}|k \\  & =((-1)\cdot 1-0\cdot 3)i-(1\cdot 1-2\cdot 3)j+(1\cdot 0-2\cdot (-1))k \\  & =-i+5j+2k \\  & =⟨-1,5,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-1)^{2}+{5}^{2}+{2}^{2}} \\  & =\sqrt{30}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{30}}{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{{2}^{2}+{0}^{2}+{1}^{2}} \\  & =\sqrt{5}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \frac{\sqrt{30}}{2} & =\frac{1}{2}MH\cdot \sqrt{5} \\ \sqrt{30} & =MH\cdot \sqrt{5} \\ MH & =\frac{\sqrt{30}}{\sqrt{5}} \\ MH & =\sqrt{6}.\end{aligned}
$$


### source replay q-128013

Calculate the length of the altitude $MH$ of the $△\,LMN,$ if $L(-1,4,1),$ $M(0,3,4),$ $N(1,4,2).$

:answer-field.type/radio
- $\sqrt{5}$
- $\sqrt{6}$
- $\sqrt{2}$
- $\sqrt{10}$
- $\sqrt{3}$

Worked solution

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(3j+4k)-(-i+4j+k) \\  & =i-j+3k \\  & =⟨1,-1,3⟩ \\ \overset{\to }{LN} & =n-l \\  & =(i+4j+2k)-(-i+4j+k) \\  & =2i+k \\  & =⟨2,0,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 1 & -1 & 3 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}-1 & 3 \\ 0 & 1\end{aligned}|i-|\begin{aligned}1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}1 & -1 \\ 2 & 0\end{aligned}|k \\  & =((-1)\cdot 1-0\cdot 3)i-(1\cdot 1-2\cdot 3)j+(1\cdot 0-2\cdot (-1))k \\  & =-i+5j+2k \\  & =⟨-1,5,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-1)^{2}+{5}^{2}+{2}^{2}} \\  & =\sqrt{30}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{30}}{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{{2}^{2}+{0}^{2}+{1}^{2}} \\  & =\sqrt{5}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \frac{\sqrt{30}}{2} & =\frac{1}{2}MH\cdot \sqrt{5} \\ \sqrt{30} & =MH\cdot \sqrt{5} \\ MH & =\frac{\sqrt{30}}{\sqrt{5}} \\ MH & =\sqrt{6}.\end{aligned}
$$


### changed-parameter observed presentation q-128013

Calculate the length of the altitude $MH$ of the $△\,LMN,$ if $L(-2,-1,-1),$ $M(-5,1,-6),$ $N(1,2,-5).$

:answer-field.type/radio
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{354}}{6}$
- $\frac{\sqrt{59}}{2}$
- $\frac{\sqrt{1770}}{6}$
- $\frac{\sqrt{885}}{6}$

Worked solution

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩ \\ \overset{\to }{LN} & =n-l \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -3 & 2 & -5 \\ 3 & 3 & -4\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 3 & -4\end{aligned}|i-|\begin{aligned}-3 & -5 \\ 3 & -4\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 3 & 3\end{aligned}|k \\  & =(2\cdot (-4)-3\cdot (-5))i-((-3)\cdot (-4)-3\cdot (-5))j+((-3)\cdot 3-3\cdot 2)k \\  & =7i-27j-15k \\  & =⟨7,-27,-15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{7}^{2}+(-27)^{2}+(-15)^{2}} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}MH\cdot \sqrt{34} \\ \sqrt{1003} & =MH\cdot \sqrt{34} \\ MH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ MH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-275225 original

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,0,-1)$, $B(0,-2,-1)$, $C(-3,-2,0).$

$CH=${{field-1}}


Original full bank: $\frac{\sqrt{22}}{2}$

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2j-k)-(-2i-k) \\  & =2i-2j \\  & =⟨2,-2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3i-2j)-(-2i-k) \\  & =-i-2j+k \\  & =⟨-1,-2,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & -2 & 0 \\ -1 & -2 & 1\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ -2 & 1\end{aligned}|i-|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|j+|\begin{aligned}2 & -2 \\ -1 & -2\end{aligned}|k \\  & =((-2)\cdot 1-(-2)\cdot 0)i-(2\cdot 1-(-1)\cdot 0)j+(2\cdot (-2)-(-1)\cdot (-2))k \\  & =-2i-2j-6k \\  & =⟨-2,-2,-6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-2)^{2}+(-2)^{2}+(-6)^{2}} \\  & =\sqrt{44} \\  & =2\sqrt{11}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{11}}{2}=\sqrt{11}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{0}^{2}} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{11} & =\frac{1}{2}CH\cdot 2\sqrt{2} \\ \sqrt{11} & =CH\cdot \sqrt{2} \\ CH & =\frac{\sqrt{11}}{\sqrt{2}} \\ CH & =\frac{\sqrt{22}}{2}.\end{aligned}
$$


### source replay q-275225

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,0,-1)$, $B(0,-2,-1)$, $C(-3,-2,0).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{22}}{2}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2j-k)-(-2i-k) \\  & =2i-2j \\  & =⟨2,-2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3i-2j)-(-2i-k) \\  & =-i-2j+k \\  & =⟨-1,-2,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & -2 & 0 \\ -1 & -2 & 1\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ -2 & 1\end{aligned}|i-|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|j+|\begin{aligned}2 & -2 \\ -1 & -2\end{aligned}|k \\  & =((-2)\cdot 1-(-2)\cdot 0)i-(2\cdot 1-(-1)\cdot 0)j+(2\cdot (-2)-(-1)\cdot (-2))k \\  & =-2i-2j-6k \\  & =⟨-2,-2,-6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-2)^{2}+(-2)^{2}+(-6)^{2}} \\  & =\sqrt{44} \\  & =2\sqrt{11}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{11}}{2}=\sqrt{11}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{0}^{2}} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{11} & =\frac{1}{2}CH\cdot 2\sqrt{2} \\ \sqrt{11} & =CH\cdot \sqrt{2} \\ CH & =\frac{\sqrt{11}}{\sqrt{2}} \\ CH & =\frac{\sqrt{22}}{2}.\end{aligned}
$$


### changed-parameter observed presentation q-275225

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,-1,-1)$, $B(1,2,-5)$, $C(-5,1,-6).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}CH\cdot \sqrt{34} \\ \sqrt{1003} & =CH\cdot \sqrt{34} \\ CH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ CH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316392 original

Calculate the length of the altitude $NP$ of the $△\,LMN$, if $L(3,-1,0)$, $M(0,2,1)$, $N(-2,1,-1).$

$NP=${{field-1}}


Original full bank: $\frac{\sqrt{3230}}{19}$

Note that the length of the altitude $NP$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}\,NP\cdot LM.
$$

So, to find $NP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2j+k)-(3i-j) \\  & =-3i+3j+k \\  & =⟨-3,3,1⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-2i+j-k)-(3i-j) \\  & =-5i+2j-k \\  & =⟨-5,2,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -3 & 3 & 1 \\ -5 & 2 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}-3 & 1 \\ -5 & -1\end{aligned}|j+|\begin{aligned}-3 & 3 \\ -5 & 2\end{aligned}|k \\  & =(3\cdot (-1)-1\cdot 2)i-((-3)\cdot (-1)-1\cdot (-5))j+((-3)\cdot 2-3\cdot (-5))k \\  & =-5i-8j+9k \\  & =⟨-5,-8,9⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-5)^{2}+(-8)^{2}+{9}^{2}} \\  & =\sqrt{170}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{170}}{2}.
$$

Let's also compute $LM$ since it appears in the formula:

$$
\begin{aligned}LM & =|\overset{\to }{LM}| \\  & =\sqrt{(-3)^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{19}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,NP\cdot LM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,NP\cdot LM \\ \frac{\sqrt{170}}{2} & =\frac{1}{2}\,NP\cdot \sqrt{19} \\ \sqrt{170} & =NP\cdot \sqrt{19} \\ NP & =\frac{\sqrt{170}}{\sqrt{19}} \\  & =\frac{\sqrt{3230}}{19}.\end{aligned}
$$


### source replay q-316392

Calculate the length of the altitude $NP$ of the $△\,LMN$, if $L(3,-1,0)$, $M(0,2,1)$, $N(-2,1,-1).$

$NP=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{3230}}{19}$

Worked solution

Note that the length of the altitude $NP$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}\,NP\cdot LM.
$$

So, to find $NP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(2j+k)-(3i-j) \\  & =-3i+3j+k \\  & =⟨-3,3,1⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-2i+j-k)-(3i-j) \\  & =-5i+2j-k \\  & =⟨-5,2,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -3 & 3 & 1 \\ -5 & 2 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}-3 & 1 \\ -5 & -1\end{aligned}|j+|\begin{aligned}-3 & 3 \\ -5 & 2\end{aligned}|k \\  & =(3\cdot (-1)-1\cdot 2)i-((-3)\cdot (-1)-1\cdot (-5))j+((-3)\cdot 2-3\cdot (-5))k \\  & =-5i-8j+9k \\  & =⟨-5,-8,9⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-5)^{2}+(-8)^{2}+{9}^{2}} \\  & =\sqrt{170}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{170}}{2}.
$$

Let's also compute $LM$ since it appears in the formula:

$$
\begin{aligned}LM & =|\overset{\to }{LM}| \\  & =\sqrt{(-3)^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{19}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,NP\cdot LM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,NP\cdot LM \\ \frac{\sqrt{170}}{2} & =\frac{1}{2}\,NP\cdot \sqrt{19} \\ \sqrt{170} & =NP\cdot \sqrt{19} \\ NP & =\frac{\sqrt{170}}{\sqrt{19}} \\  & =\frac{\sqrt{3230}}{19}.\end{aligned}
$$


### changed-parameter observed presentation q-316392

Calculate the length of the altitude $NP$ of the $△\,LMN$, if $L(-2,-1,-1)$, $M(1,2,-5)$, $N(-5,1,-6).$

$NP=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $NP$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}\,NP\cdot LM.
$$

So, to find $NP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{LN} & =n-l \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $LM$ since it appears in the formula:

$$
\begin{aligned}LM & =|\overset{\to }{LM}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,NP\cdot LM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,NP\cdot LM \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}\,NP\cdot \sqrt{34} \\ \sqrt{1003} & =NP\cdot \sqrt{34} \\ NP & =\frac{\sqrt{1003}}{\sqrt{34}} \\  & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316395 original

Calculate the length of the altitude $UT$ of the $△\,UVW$, if $U(-2,2,0)$, $V(1,-1,2)$, $W(3,0,-1).$

$UT=${{field-1}}


Original full bank: $\frac{\sqrt{4186}}{14}$

Note that the length of the altitude $UT$ can be related to the area of $△\,UVW$ as follows:

$$
{A}_{△}=\frac{1}{2}\,UT\cdot VW.
$$

So, to find $UT,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{VW}$ and $\overset{\to }{VU}:$

$$
\begin{aligned}\overset{\to }{VW} & =w-v \\  & =(3i-k)-(i-j+2k) \\  & =2i+j-3k \\  & =⟨2,1,-3⟩ \\ \overset{\to }{VU} & =u-v \\  & =(-2i+2j)-(i-j+2k) \\  & =-3i+3j-2k \\  & =⟨-3,3,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{VW}\times \overset{\to }{VU} & =|\begin{aligned}i & j & k \\ 2 & 1 & -3 \\ -3 & 3 & -2\end{aligned}| \\  & =|\begin{aligned}1 & -3 \\ 3 & -2\end{aligned}|i-|\begin{aligned}2 & -3 \\ -3 & -2\end{aligned}|j+|\begin{aligned}2 & 1 \\ -3 & 3\end{aligned}|k \\  & =(1\cdot (-2)-(-3)\cdot 3)i-(2\cdot (-2)-(-3)\cdot (-3))j+(2\cdot 3-1\cdot (-3))k \\  & =7i+13j+9k \\  & =⟨7,13,9⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{VW}$ and $\overset{\to }{VU}$ is

$$
\begin{aligned}A & =|\overset{\to }{VW}\times \overset{\to }{VU}| \\  & =\sqrt{{7}^{2}+{13}^{2}+{9}^{2}} \\  & =\sqrt{299}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,UVW$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{299}}{2}.
$$

Let's also compute $VW$ since it appears in the formula:

$$
\begin{aligned}VW & =|\overset{\to }{VW}| \\  & =\sqrt{{2}^{2}+{1}^{2}+(-3)^{2}} \\  & =\sqrt{14}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,UT\cdot VW,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,UT\cdot VW \\ \frac{\sqrt{299}}{2} & =\frac{1}{2}\,UT\cdot \sqrt{14} \\ \sqrt{299} & =UT\cdot \sqrt{14} \\ UT & =\frac{\sqrt{299}}{\sqrt{14}} \\  & =\frac{\sqrt{4186}}{14}.\end{aligned}
$$


### source replay q-316395

Calculate the length of the altitude $UT$ of the $△\,UVW$, if $U(-2,2,0)$, $V(1,-1,2)$, $W(3,0,-1).$

$UT=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{4186}}{14}$

Worked solution

Note that the length of the altitude $UT$ can be related to the area of $△\,UVW$ as follows:

$$
{A}_{△}=\frac{1}{2}\,UT\cdot VW.
$$

So, to find $UT,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{VW}$ and $\overset{\to }{VU}:$

$$
\begin{aligned}\overset{\to }{VW} & =w-v \\  & =(3i-k)-(i-j+2k) \\  & =2i+j-3k \\  & =⟨2,1,-3⟩ \\ \overset{\to }{VU} & =u-v \\  & =(-2i+2j)-(i-j+2k) \\  & =-3i+3j-2k \\  & =⟨-3,3,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{VW}\times \overset{\to }{VU} & =|\begin{aligned}i & j & k \\ 2 & 1 & -3 \\ -3 & 3 & -2\end{aligned}| \\  & =|\begin{aligned}1 & -3 \\ 3 & -2\end{aligned}|i-|\begin{aligned}2 & -3 \\ -3 & -2\end{aligned}|j+|\begin{aligned}2 & 1 \\ -3 & 3\end{aligned}|k \\  & =(1\cdot (-2)-(-3)\cdot 3)i-(2\cdot (-2)-(-3)\cdot (-3))j+(2\cdot 3-1\cdot (-3))k \\  & =7i+13j+9k \\  & =⟨7,13,9⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{VW}$ and $\overset{\to }{VU}$ is

$$
\begin{aligned}A & =|\overset{\to }{VW}\times \overset{\to }{VU}| \\  & =\sqrt{{7}^{2}+{13}^{2}+{9}^{2}} \\  & =\sqrt{299}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,UVW$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{299}}{2}.
$$

Let's also compute $VW$ since it appears in the formula:

$$
\begin{aligned}VW & =|\overset{\to }{VW}| \\  & =\sqrt{{2}^{2}+{1}^{2}+(-3)^{2}} \\  & =\sqrt{14}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,UT\cdot VW,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,UT\cdot VW \\ \frac{\sqrt{299}}{2} & =\frac{1}{2}\,UT\cdot \sqrt{14} \\ \sqrt{299} & =UT\cdot \sqrt{14} \\ UT & =\frac{\sqrt{299}}{\sqrt{14}} \\  & =\frac{\sqrt{4186}}{14}.\end{aligned}
$$


### changed-parameter observed presentation q-316395

Calculate the length of the altitude $UT$ of the $△\,UVW$, if $U(-5,1,-6)$, $V(-2,-1,-1)$, $W(1,2,-5).$

$UT=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $UT$ can be related to the area of $△\,UVW$ as follows:

$$
{A}_{△}=\frac{1}{2}\,UT\cdot VW.
$$

So, to find $UT,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{VW}$ and $\overset{\to }{VU}:$

$$
\begin{aligned}\overset{\to }{VW} & =w-v \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{VU} & =u-v \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{VW}\times \overset{\to }{VU} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{VW}$ and $\overset{\to }{VU}$ is

$$
\begin{aligned}A & =|\overset{\to }{VW}\times \overset{\to }{VU}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,UVW$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $VW$ since it appears in the formula:

$$
\begin{aligned}VW & =|\overset{\to }{VW}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, using ${A}_{△}=\frac{1}{2}\,UT\cdot VW,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}\,UT\cdot VW \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}\,UT\cdot \sqrt{34} \\ \sqrt{1003} & =UT\cdot \sqrt{34} \\ UT & =\frac{\sqrt{1003}}{\sqrt{34}} \\  & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316400 original

Calculate the length of the altitude $VL$ of the $△\,TUV$, if $T(1,0,1)$, $U(3,2,-1)$, $V(-1,1,0).$

$VL=${{field-1}}


Original full bank: $\sqrt{6}$

Note that the length of the altitude $VL$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VL\cdot TU
$$

So, to find $VL,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =(3i+2j-k)-(i+k) \\  & =2i+2j-2k \\  & =⟨2,2,-2⟩ \\ \overset{\to }{TV} & =v-t \\  & =(-i+j)-(i+k) \\  & =-2i+j-k \\  & =⟨-2,1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ 2 & 2 & -2 \\ -2 & 1 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}2 & -2 \\ -2 & -1\end{aligned}|j+|\begin{aligned}2 & 2 \\ -2 & 1\end{aligned}|k \\  & =(2\cdot (-1)-(-2)\cdot 1)i-(2\cdot (-1)-(-2)\cdot (-2))j+(2\cdot 1-2\cdot (-2))k \\  & =0i+6j+6k \\  & =⟨0,6,6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{{0}^{2}+{6}^{2}+{6}^{2}} \\  & =\sqrt{72} \\  & =6\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{2}}{2}=3\sqrt{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{{2}^{2}+{2}^{2}+(-2)^{2}} \\  & =\sqrt{12} \\  & =2\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VL\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VL\cdot TU \\ 3\sqrt{2} & =\frac{1}{2}VL\cdot 2\sqrt{3} \\ 3\sqrt{2} & =VL\cdot \sqrt{3} \\ VL & =\frac{3\sqrt{2}}{\sqrt{3}} \\ VL & =\sqrt{6}.\end{aligned}
$$


### source replay q-316400

Calculate the length of the altitude $VL$ of the $△\,TUV$, if $T(1,0,1)$, $U(3,2,-1)$, $V(-1,1,0).$

$VL=${{field-1}}

:answer-field.type/blank
- $\sqrt{6}$

Worked solution

Note that the length of the altitude $VL$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VL\cdot TU
$$

So, to find $VL,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =(3i+2j-k)-(i+k) \\  & =2i+2j-2k \\  & =⟨2,2,-2⟩ \\ \overset{\to }{TV} & =v-t \\  & =(-i+j)-(i+k) \\  & =-2i+j-k \\  & =⟨-2,1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ 2 & 2 & -2 \\ -2 & 1 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}2 & -2 \\ -2 & -1\end{aligned}|j+|\begin{aligned}2 & 2 \\ -2 & 1\end{aligned}|k \\  & =(2\cdot (-1)-(-2)\cdot 1)i-(2\cdot (-1)-(-2)\cdot (-2))j+(2\cdot 1-2\cdot (-2))k \\  & =0i+6j+6k \\  & =⟨0,6,6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{{0}^{2}+{6}^{2}+{6}^{2}} \\  & =\sqrt{72} \\  & =6\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{6\sqrt{2}}{2}=3\sqrt{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{{2}^{2}+{2}^{2}+(-2)^{2}} \\  & =\sqrt{12} \\  & =2\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VL\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VL\cdot TU \\ 3\sqrt{2} & =\frac{1}{2}VL\cdot 2\sqrt{3} \\ 3\sqrt{2} & =VL\cdot \sqrt{3} \\ VL & =\frac{3\sqrt{2}}{\sqrt{3}} \\ VL & =\sqrt{6}.\end{aligned}
$$


### changed-parameter observed presentation q-316400

Calculate the length of the altitude $VL$ of the $△\,TUV$, if $T(-2,-1,-1)$, $U(1,2,-5)$, $V(-5,1,-6).$

$VL=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $VL$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VL\cdot TU
$$

So, to find $VL,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{TV} & =v-t \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VL\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VL\cdot TU \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}VL\cdot \sqrt{34} \\ \sqrt{1003} & =VL\cdot \sqrt{34} \\ VL & =\frac{\sqrt{1003}}{\sqrt{34}} \\ VL & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316409 original

Calculate the length of the altitude $IP$ of the $△\,HIJ$, if $H(-1,2,0)$, $I(1,1,3)$, $J(0,-2,1).$

$IP=${{field-1}}


Original full bank: $\frac{\sqrt{38}}{2}$

Note that the length of the altitude $IP$ can be related to the area of $△\,HIJ$ as follows:

$$
{A}_{△}=\frac{1}{2}IP\cdot HJ
$$

So, to find $IP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{HJ}$ and $\overset{\to }{HI}:$

$$
\begin{aligned}\overset{\to }{HJ} & =j-h \\  & =(-2j+k)-(-i+2j) \\  & =i-4j+k \\  & =⟨1,-4,1⟩ \\ \overset{\to }{HI} & =i-h \\  & =(i+j+3k)-(-i+2j) \\  & =2i-j+3k \\  & =⟨2,-1,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{HJ}\times \overset{\to }{HI} & =|\begin{aligned}i & j & k \\ 1 & -4 & 1 \\ 2 & -1 & 3\end{aligned}| \\  & =|\begin{aligned}-4 & 1 \\ -1 & 3\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & 3\end{aligned}|j+|\begin{aligned}1 & -4 \\ 2 & -1\end{aligned}|k \\  & =((-4)\cdot 3-1\cdot (-1))i-(1\cdot 3-1\cdot 2)j+(1\cdot (-1)-(-4)\cdot 2)k \\  & =-11i-j+7k \\  & =⟨-11,-1,7⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{HJ}$ and $\overset{\to }{HI}$ is

$$
\begin{aligned}A & =|\overset{\to }{HJ}\times \overset{\to }{HI}| \\  & =\sqrt{(-11)^{2}+(-1)^{2}+{7}^{2}} \\  & =\sqrt{171} \\  & =3\sqrt{19}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,HIJ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{19}}{2}.
$$

Let's also compute $HJ$ since it appears in the formula:

$$
\begin{aligned}HJ & =|\overset{\to }{HJ}| \\  & =\sqrt{{1}^{2}+(-4)^{2}+{1}^{2}} \\  & =\sqrt{18} \\  & =3\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}IP\cdot HJ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}IP\cdot HJ \\ \frac{3\sqrt{19}}{2} & =\frac{1}{2}\,IP\cdot 3\sqrt{2} \\ \sqrt{19} & =\sqrt{2}\,IP \\ IP & =\frac{\sqrt{19}}{\sqrt{2}} \\  & =\frac{\sqrt{38}}{2}.\end{aligned}
$$


### source replay q-316409

Calculate the length of the altitude $IP$ of the $△\,HIJ$, if $H(-1,2,0)$, $I(1,1,3)$, $J(0,-2,1).$

$IP=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{38}}{2}$

Worked solution

Note that the length of the altitude $IP$ can be related to the area of $△\,HIJ$ as follows:

$$
{A}_{△}=\frac{1}{2}IP\cdot HJ
$$

So, to find $IP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{HJ}$ and $\overset{\to }{HI}:$

$$
\begin{aligned}\overset{\to }{HJ} & =j-h \\  & =(-2j+k)-(-i+2j) \\  & =i-4j+k \\  & =⟨1,-4,1⟩ \\ \overset{\to }{HI} & =i-h \\  & =(i+j+3k)-(-i+2j) \\  & =2i-j+3k \\  & =⟨2,-1,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{HJ}\times \overset{\to }{HI} & =|\begin{aligned}i & j & k \\ 1 & -4 & 1 \\ 2 & -1 & 3\end{aligned}| \\  & =|\begin{aligned}-4 & 1 \\ -1 & 3\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & 3\end{aligned}|j+|\begin{aligned}1 & -4 \\ 2 & -1\end{aligned}|k \\  & =((-4)\cdot 3-1\cdot (-1))i-(1\cdot 3-1\cdot 2)j+(1\cdot (-1)-(-4)\cdot 2)k \\  & =-11i-j+7k \\  & =⟨-11,-1,7⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{HJ}$ and $\overset{\to }{HI}$ is

$$
\begin{aligned}A & =|\overset{\to }{HJ}\times \overset{\to }{HI}| \\  & =\sqrt{(-11)^{2}+(-1)^{2}+{7}^{2}} \\  & =\sqrt{171} \\  & =3\sqrt{19}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,HIJ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{19}}{2}.
$$

Let's also compute $HJ$ since it appears in the formula:

$$
\begin{aligned}HJ & =|\overset{\to }{HJ}| \\  & =\sqrt{{1}^{2}+(-4)^{2}+{1}^{2}} \\  & =\sqrt{18} \\  & =3\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}IP\cdot HJ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}IP\cdot HJ \\ \frac{3\sqrt{19}}{2} & =\frac{1}{2}\,IP\cdot 3\sqrt{2} \\ \sqrt{19} & =\sqrt{2}\,IP \\ IP & =\frac{\sqrt{19}}{\sqrt{2}} \\  & =\frac{\sqrt{38}}{2}.\end{aligned}
$$


### changed-parameter observed presentation q-316409

Calculate the length of the altitude $IP$ of the $△\,HIJ$, if $H(-2,-1,-1)$, $I(-5,1,-6)$, $J(1,2,-5).$

$IP=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $IP$ can be related to the area of $△\,HIJ$ as follows:

$$
{A}_{△}=\frac{1}{2}IP\cdot HJ
$$

So, to find $IP,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{HJ}$ and $\overset{\to }{HI}:$

$$
\begin{aligned}\overset{\to }{HJ} & =j-h \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{HI} & =i-h \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{HJ}\times \overset{\to }{HI} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{HJ}$ and $\overset{\to }{HI}$ is

$$
\begin{aligned}A & =|\overset{\to }{HJ}\times \overset{\to }{HI}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,HIJ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $HJ$ since it appears in the formula:

$$
\begin{aligned}HJ & =|\overset{\to }{HJ}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}IP\cdot HJ,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}IP\cdot HJ \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}\,IP\cdot \sqrt{34} \\ \sqrt{1003} & =\sqrt{34}\,IP \\ IP & =\frac{\sqrt{1003}}{\sqrt{34}} \\  & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316553 original

Calculate the length of the altitude $CK$ of the $△\,ABC,$ if $A(1,0,1),$ $B(4,2,1),$ $C(2,3,2).$

$CK=${{field-1}}


Original full bank: $\frac{\sqrt{806}}{13}$

Note that the length of the altitude $CK$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CK\cdot AB
$$

So, to find $CK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i+2j+k)-(i+k) \\  & =3i+2j+0k \\  & =⟨3,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+3j+2k)-(i+k) \\  & =i+3j+k \\  & =⟨1,3,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 2 & 0 \\ 1 & 3 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 3 & 1\end{aligned}|i-|\begin{aligned}3 & 0 \\ 1 & 1\end{aligned}|j+|\begin{aligned}3 & 2 \\ 1 & 3\end{aligned}|k \\  & =(2\cdot 1-0\cdot 3)i-(3\cdot 1-0\cdot 1)j+(3\cdot 3-2\cdot 1)k \\  & =2i-3j+7k \\  & =⟨2,-3,7⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+(-3)^{2}+{7}^{2}} \\  & =\sqrt{62}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{62}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{13}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}CK\cdot AB,$ we get

$$
\begin{aligned}\frac{\sqrt{62}}{2} & =\frac{1}{2}CK\cdot \sqrt{13} \\ CK & =\frac{\sqrt{62}}{\sqrt{13}} \\ CK & =\frac{\sqrt{806}}{13}.\end{aligned}
$$


### source replay q-316553

Calculate the length of the altitude $CK$ of the $△\,ABC,$ if $A(1,0,1),$ $B(4,2,1),$ $C(2,3,2).$

$CK=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{806}}{13}$

Worked solution

Note that the length of the altitude $CK$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CK\cdot AB
$$

So, to find $CK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i+2j+k)-(i+k) \\  & =3i+2j+0k \\  & =⟨3,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+3j+2k)-(i+k) \\  & =i+3j+k \\  & =⟨1,3,1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 2 & 0 \\ 1 & 3 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 3 & 1\end{aligned}|i-|\begin{aligned}3 & 0 \\ 1 & 1\end{aligned}|j+|\begin{aligned}3 & 2 \\ 1 & 3\end{aligned}|k \\  & =(2\cdot 1-0\cdot 3)i-(3\cdot 1-0\cdot 1)j+(3\cdot 3-2\cdot 1)k \\  & =2i-3j+7k \\  & =⟨2,-3,7⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{2}^{2}+(-3)^{2}+{7}^{2}} \\  & =\sqrt{62}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{62}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{13}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}CK\cdot AB,$ we get

$$
\begin{aligned}\frac{\sqrt{62}}{2} & =\frac{1}{2}CK\cdot \sqrt{13} \\ CK & =\frac{\sqrt{62}}{\sqrt{13}} \\ CK & =\frac{\sqrt{806}}{13}.\end{aligned}
$$


### changed-parameter observed presentation q-316553

Calculate the length of the altitude $CK$ of the $△\,ABC,$ if $A(-2,-1,-1),$ $B(1,2,-5),$ $C(-5,1,-6).$

$CK=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $CK$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CK\cdot AB
$$

So, to find $CK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}CK\cdot AB,$ we get

$$
\begin{aligned}\frac{\sqrt{1003}}{2} & =\frac{1}{2}CK\cdot \sqrt{34} \\ CK & =\frac{\sqrt{1003}}{\sqrt{34}} \\ CK & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316556 original

Calculate the length of the altitude $HK$ of the $△\,GHI,$ if $G(1,1,1),$ $H(3,2,4),$ $I(2,4,2).$

$HK=${{field-1}}


Original full bank: $\frac{3\sqrt{110}}{11}$

Note that the length of the altitude $HK$ can be related to the area of $△\,GHI$ as follows:

$$
{A}_{△}=\frac{1}{2}HK\cdot GI
$$

So, to find $HK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{GI}$ and $\overset{\to }{GH}:$

$$
\begin{aligned}\overset{\to }{GI} & =i-g \\  & =(2i+4j+2k)-(i+j+k) \\  & =i+3j+k \\  & =⟨1,3,1⟩ \\ \overset{\to }{GH} & =h-g \\  & =(3i+2j+4k)-(i+j+k) \\  & =2i+j+3k \\  & =⟨2,1,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{GI}\times \overset{\to }{GH} & =|\begin{aligned}i & j & k \\ 1 & 3 & 1 \\ 2 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 1 & 3\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & 3\end{aligned}|j+|\begin{aligned}1 & 3 \\ 2 & 1\end{aligned}|k \\  & =(3\cdot 3-1\cdot 1)i-(1\cdot 3-1\cdot 2)j+(1\cdot 1-3\cdot 2)k \\  & =8i-j-5k \\  & =⟨8,-1,-5⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{GI}$ and $\overset{\to }{GH}$ is

$$
\begin{aligned}A & =|\overset{\to }{GI}\times \overset{\to }{GH}| \\  & =\sqrt{{8}^{2}+(-1)^{2}+(-5)^{2}} \\  & =3\sqrt{10}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GHI$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{10}}{2}.
$$

Let's also compute $GI$ since it appears in the formula:

$$
\begin{aligned}GI & =|\overset{\to }{GI}| \\  & =\sqrt{{1}^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{11}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}HK\cdot GI,$ we get

$$
\begin{aligned}\frac{3\sqrt{10}}{2} & =\frac{1}{2}HK\cdot \sqrt{11} \\ HK & =\frac{3\sqrt{10}}{\sqrt{11}} \\ HK & =\frac{3\sqrt{110}}{11}.\end{aligned}
$$


### source replay q-316556

Calculate the length of the altitude $HK$ of the $△\,GHI,$ if $G(1,1,1),$ $H(3,2,4),$ $I(2,4,2).$

$HK=${{field-1}}

:answer-field.type/blank
- $\frac{3\sqrt{110}}{11}$

Worked solution

Note that the length of the altitude $HK$ can be related to the area of $△\,GHI$ as follows:

$$
{A}_{△}=\frac{1}{2}HK\cdot GI
$$

So, to find $HK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{GI}$ and $\overset{\to }{GH}:$

$$
\begin{aligned}\overset{\to }{GI} & =i-g \\  & =(2i+4j+2k)-(i+j+k) \\  & =i+3j+k \\  & =⟨1,3,1⟩ \\ \overset{\to }{GH} & =h-g \\  & =(3i+2j+4k)-(i+j+k) \\  & =2i+j+3k \\  & =⟨2,1,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{GI}\times \overset{\to }{GH} & =|\begin{aligned}i & j & k \\ 1 & 3 & 1 \\ 2 & 1 & 3\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 1 & 3\end{aligned}|i-|\begin{aligned}1 & 1 \\ 2 & 3\end{aligned}|j+|\begin{aligned}1 & 3 \\ 2 & 1\end{aligned}|k \\  & =(3\cdot 3-1\cdot 1)i-(1\cdot 3-1\cdot 2)j+(1\cdot 1-3\cdot 2)k \\  & =8i-j-5k \\  & =⟨8,-1,-5⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{GI}$ and $\overset{\to }{GH}$ is

$$
\begin{aligned}A & =|\overset{\to }{GI}\times \overset{\to }{GH}| \\  & =\sqrt{{8}^{2}+(-1)^{2}+(-5)^{2}} \\  & =3\sqrt{10}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GHI$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{10}}{2}.
$$

Let's also compute $GI$ since it appears in the formula:

$$
\begin{aligned}GI & =|\overset{\to }{GI}| \\  & =\sqrt{{1}^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{11}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}HK\cdot GI,$ we get

$$
\begin{aligned}\frac{3\sqrt{10}}{2} & =\frac{1}{2}HK\cdot \sqrt{11} \\ HK & =\frac{3\sqrt{10}}{\sqrt{11}} \\ HK & =\frac{3\sqrt{110}}{11}.\end{aligned}
$$


### changed-parameter observed presentation q-316556

Calculate the length of the altitude $HK$ of the $△\,GHI,$ if $G(-2,-1,-1),$ $H(-5,1,-6),$ $I(1,2,-5).$

$HK=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $HK$ can be related to the area of $△\,GHI$ as follows:

$$
{A}_{△}=\frac{1}{2}HK\cdot GI
$$

So, to find $HK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{GI}$ and $\overset{\to }{GH}:$

$$
\begin{aligned}\overset{\to }{GI} & =i-g \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{GH} & =h-g \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{GI}\times \overset{\to }{GH} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-(-4)\cdot 2)i-(3\cdot (-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{GI}$ and $\overset{\to }{GH}$ is

$$
\begin{aligned}A & =|\overset{\to }{GI}\times \overset{\to }{GH}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GHI$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $GI$ since it appears in the formula:

$$
\begin{aligned}GI & =|\overset{\to }{GI}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}HK\cdot GI,$ we get

$$
\begin{aligned}\frac{\sqrt{1003}}{2} & =\frac{1}{2}HK\cdot \sqrt{34} \\ HK & =\frac{\sqrt{1003}}{\sqrt{34}} \\ HK & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-316558 original

Calculate the length of the altitude $TK$ of the $△\,RST,$ if $R(4,5,6),$ $S(7,4,5),$ $T(6,8,4).$

$TK=${{field-1}}


Original full bank: $\frac{9\sqrt{22}}{11}$

Note that the length of the altitude $TK$ can be related to the area of $△\,RST$ as follows:

$$
{A}_{△}=\frac{1}{2}TK\cdot RS
$$

So, to find $TK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(7i+4j+5k)-(4i+5j+6k) \\  & =3i-j-k \\  & =⟨3,-1,-1⟩ \\ \overset{\to }{RT} & =t-r \\  & =(6i+8j+4k)-(4i+5j+6k) \\  & =2i+3j-2k \\  & =⟨2,3,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ 3 & -1 & -1 \\ 2 & 3 & -2\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ 3 & -2\end{aligned}|i-|\begin{aligned}3 & -1 \\ 2 & -2\end{aligned}|j+|\begin{aligned}3 & -1 \\ 2 & 3\end{aligned}|k \\  & =((-1)(-2)-(-1)\cdot 3)i-(3(-2)-(-1)\cdot 2)j+(3\cdot 3-(-1)\cdot 2)k \\  & =5i+4j+11k \\  & =⟨5,4,11⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{{5}^{2}+{4}^{2}+{11}^{2}} \\  & =\sqrt{162} \\  & =9\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{9\sqrt{2}}{2}.
$$

Let's also compute $RS$ since it appears in the formula:

$$
\begin{aligned}RS & =|\overset{\to }{RS}| \\  & =\sqrt{{3}^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{11}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}TK\cdot RS,$ we get

$$
\begin{aligned}\frac{9\sqrt{2}}{2} & =\frac{1}{2}TK\cdot \sqrt{11} \\ TK & =\frac{9\sqrt{2}}{\sqrt{11}} \\ TK & =\frac{9\sqrt{22}}{11}.\end{aligned}
$$


### source replay q-316558

Calculate the length of the altitude $TK$ of the $△\,RST,$ if $R(4,5,6),$ $S(7,4,5),$ $T(6,8,4).$

$TK=${{field-1}}

:answer-field.type/blank
- $\frac{9\sqrt{22}}{11}$

Worked solution

Note that the length of the altitude $TK$ can be related to the area of $△\,RST$ as follows:

$$
{A}_{△}=\frac{1}{2}TK\cdot RS
$$

So, to find $TK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(7i+4j+5k)-(4i+5j+6k) \\  & =3i-j-k \\  & =⟨3,-1,-1⟩ \\ \overset{\to }{RT} & =t-r \\  & =(6i+8j+4k)-(4i+5j+6k) \\  & =2i+3j-2k \\  & =⟨2,3,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ 3 & -1 & -1 \\ 2 & 3 & -2\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ 3 & -2\end{aligned}|i-|\begin{aligned}3 & -1 \\ 2 & -2\end{aligned}|j+|\begin{aligned}3 & -1 \\ 2 & 3\end{aligned}|k \\  & =((-1)(-2)-(-1)\cdot 3)i-(3(-2)-(-1)\cdot 2)j+(3\cdot 3-(-1)\cdot 2)k \\  & =5i+4j+11k \\  & =⟨5,4,11⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{{5}^{2}+{4}^{2}+{11}^{2}} \\  & =\sqrt{162} \\  & =9\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{9\sqrt{2}}{2}.
$$

Let's also compute $RS$ since it appears in the formula:

$$
\begin{aligned}RS & =|\overset{\to }{RS}| \\  & =\sqrt{{3}^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{11}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}TK\cdot RS,$ we get

$$
\begin{aligned}\frac{9\sqrt{2}}{2} & =\frac{1}{2}TK\cdot \sqrt{11} \\ TK & =\frac{9\sqrt{2}}{\sqrt{11}} \\ TK & =\frac{9\sqrt{22}}{11}.\end{aligned}
$$


### changed-parameter observed presentation q-316558

Calculate the length of the altitude $TK$ of the $△\,RST,$ if $R(-2,-1,-1),$ $S(1,2,-5),$ $T(-5,1,-6).$

$TK=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $TK$ can be related to the area of $△\,RST$ as follows:

$$
{A}_{△}=\frac{1}{2}TK\cdot RS
$$

So, to find $TK,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{RS}$ and $\overset{\to }{RT}:$

$$
\begin{aligned}\overset{\to }{RS} & =s-r \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{RT} & =t-r \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{RS}\times \overset{\to }{RT} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3(-5)-(-4)\cdot 2)i-(3(-5)-(-4)\cdot (-3))j+(3\cdot 2-3\cdot (-3))k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{RS}$ and $\overset{\to }{RT}$ is

$$
\begin{aligned}A & =|\overset{\to }{RS}\times \overset{\to }{RT}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,RST$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $RS$ since it appears in the formula:

$$
\begin{aligned}RS & =|\overset{\to }{RS}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

Finally, using the formula ${A}_{△}=\frac{1}{2}TK\cdot RS,$ we get

$$
\begin{aligned}\frac{\sqrt{1003}}{2} & =\frac{1}{2}TK\cdot \sqrt{34} \\ TK & =\frac{\sqrt{1003}}{\sqrt{34}} \\ TK & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-71113 original

Calculate the length of the altitude $MH$ of the $△\,LMN$, if $L(3,3,2)$, $M(1,1,2)$, $N(2,2,1).$


Original full bank: $\frac{2\sqrt{2}}{3}$, $\frac{\sqrt{6}}{3}$, $\frac{3\sqrt{6}}{2}$, $\frac{2\sqrt{6}}{3}$, $\frac{2\sqrt{3}}{3}$

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(i+j+2k)-(3i+3j+2k) \\  & =-2i-2j \\  & =⟨-2,-2,0⟩ \\ \overset{\to }{LN} & =n-l \\  & =(2i+2j+k)-(3i+3j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -2 & -2 & 0 \\ -1 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ -1 & -1\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-2 & -2 \\ -1 & -1\end{aligned}|k \\  & =((-2)\cdot (-1)-(-1)\cdot 0)i-((-2)\cdot (-1)-(-1)\cdot 0)j+((-2)\cdot (-1)-(-1)\cdot (-2))k \\  & =2i-2j \\  & =⟨2,-2,0⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{0}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{(-1)^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \sqrt{2} & =\frac{1}{2}MH\cdot \sqrt{3} \\ 2\sqrt{2} & =MH\cdot \sqrt{3} \\ MH & =\frac{2\sqrt{2}}{\sqrt{3}} \\ MH & =\frac{2\sqrt{6}}{3}.\end{aligned}
$$


### source replay q-71113

Calculate the length of the altitude $MH$ of the $△\,LMN$, if $L(3,3,2)$, $M(1,1,2)$, $N(2,2,1).$

:answer-field.type/radio
- $\frac{\sqrt{6}}{3}$
- $\frac{2\sqrt{3}}{3}$
- $\frac{2\sqrt{6}}{3}$
- $\frac{3\sqrt{6}}{2}$
- $\frac{2\sqrt{2}}{3}$

Worked solution

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(i+j+2k)-(3i+3j+2k) \\  & =-2i-2j \\  & =⟨-2,-2,0⟩ \\ \overset{\to }{LN} & =n-l \\  & =(2i+2j+k)-(3i+3j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -2 & -2 & 0 \\ -1 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ -1 & -1\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-2 & -2 \\ -1 & -1\end{aligned}|k \\  & =((-2)\cdot (-1)-(-1)\cdot 0)i-((-2)\cdot (-1)-(-1)\cdot 0)j+((-2)\cdot (-1)-(-1)\cdot (-2))k \\  & =2i-2j \\  & =⟨2,-2,0⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{0}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{(-1)^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \sqrt{2} & =\frac{1}{2}MH\cdot \sqrt{3} \\ 2\sqrt{2} & =MH\cdot \sqrt{3} \\ MH & =\frac{2\sqrt{2}}{\sqrt{3}} \\ MH & =\frac{2\sqrt{6}}{3}.\end{aligned}
$$


### changed-parameter observed presentation q-71113

Calculate the length of the altitude $MH$ of the $△\,LMN$, if $L(-2,-1,-1)$, $M(-5,1,-6)$, $N(1,2,-5).$

:answer-field.type/radio
- $\frac{\sqrt{59}}{2}$
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{354}}{6}$
- $\frac{9\sqrt{118}}{8}$
- $\frac{\sqrt{118}}{4}$

Worked solution

Note that the length of the altitude $MH$ can be related to the area of $△\,LMN$ as follows:

$$
{A}_{△}=\frac{1}{2}MH\cdot LN
$$

So, to find $MH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{LM}$ and $\overset{\to }{LN}:$

$$
\begin{aligned}\overset{\to }{LM} & =m-l \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩ \\ \overset{\to }{LN} & =n-l \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{LM}\times \overset{\to }{LN} & =|\begin{aligned}i & j & k \\ -3 & 2 & -5 \\ 3 & 3 & -4\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 3 & -4\end{aligned}|i-|\begin{aligned}-3 & -5 \\ 3 & -4\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 3 & 3\end{aligned}|k \\  & =(2\cdot (-4)-3\cdot (-5))i-((-3)\cdot (-4)-3\cdot (-5))j+((-3)\cdot 3-3\cdot 2)k \\  & =7i-27j-15k \\  & =⟨7,-27,-15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{LM}$ and $\overset{\to }{LN}$ is

$$
\begin{aligned}A & =|\overset{\to }{LM}\times \overset{\to }{LN}| \\  & =\sqrt{{7}^{2}+(-27)^{2}+(-15)^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,LMN$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $LN$ since it appears in the formula:

$$
\begin{aligned}LN & =|\overset{\to }{LN}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}MH\cdot LN,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}MH\cdot LN \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}MH\cdot \sqrt{34} \\ \sqrt{1003} & =MH\cdot \sqrt{34} \\ MH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ MH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-71115 original

Calculate the length of the altitude $VH$ of the $△\,TUV$, if $T(3,2,3)$, $U(0,1,0)$, $V(2,1,2).$


Original full bank: $\frac{2\sqrt{38}}{19}$, $\frac{\sqrt{19}}{19}$, $2\sqrt{38}$, $\frac{2\sqrt{3}}{19}$, $\frac{2\sqrt{2}}{3}$

Note that the length of the altitude $VH$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VH\cdot TU
$$

So, to find $VH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =j-(3i+2j+3k) \\  & =-3i-j-3k \\  & =⟨-3,-1,-3⟩ \\ \overset{\to }{TV} & =v-t \\  & =(2i+j+2k)-(3i+2j+3k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ -3 & -1 & -3 \\ -1 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}-1 & -3 \\ -1 & -1\end{aligned}|i-|\begin{aligned}-3 & -3 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-3 & -1 \\ -1 & -1\end{aligned}|k \\  & =((-1)\cdot (-1)-(-1)\cdot (-3))i-((-3)\cdot (-1)-(-1)\cdot (-3))j+((-3)\cdot (-1)-(-1)\cdot (-1))k \\  & =-2i+2k \\  & =⟨-2,0,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{(-2)^{2}+{0}^{2}+{2}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{(-3)^{2}+(-1)^{2}+(-3)^{2}} \\  & =\sqrt{19}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VH\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VH\cdot TU \\ \sqrt{2} & =\frac{1}{2}VH\cdot \sqrt{19} \\ 2\sqrt{2} & =VH\cdot \sqrt{19} \\ VH & =\frac{2\sqrt{2}}{\sqrt{19}} \\ VH & =\frac{2\sqrt{38}}{19}.\end{aligned}
$$


### source replay q-71115

Calculate the length of the altitude $VH$ of the $△\,TUV$, if $T(3,2,3)$, $U(0,1,0)$, $V(2,1,2).$

:answer-field.type/radio
- $\frac{\sqrt{19}}{19}$
- $\frac{2\sqrt{2}}{3}$
- $\frac{2\sqrt{3}}{19}$
- $2\sqrt{38}$
- $\frac{2\sqrt{38}}{19}$

Worked solution

Note that the length of the altitude $VH$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VH\cdot TU
$$

So, to find $VH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =j-(3i+2j+3k) \\  & =-3i-j-3k \\  & =⟨-3,-1,-3⟩ \\ \overset{\to }{TV} & =v-t \\  & =(2i+j+2k)-(3i+2j+3k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ -3 & -1 & -3 \\ -1 & -1 & -1\end{aligned}| \\  & =|\begin{aligned}-1 & -3 \\ -1 & -1\end{aligned}|i-|\begin{aligned}-3 & -3 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-3 & -1 \\ -1 & -1\end{aligned}|k \\  & =((-1)\cdot (-1)-(-1)\cdot (-3))i-((-3)\cdot (-1)-(-1)\cdot (-3))j+((-3)\cdot (-1)-(-1)\cdot (-1))k \\  & =-2i+2k \\  & =⟨-2,0,2⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{(-2)^{2}+{0}^{2}+{2}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{2}}{2}=\sqrt{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{(-3)^{2}+(-1)^{2}+(-3)^{2}} \\  & =\sqrt{19}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VH\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VH\cdot TU \\ \sqrt{2} & =\frac{1}{2}VH\cdot \sqrt{19} \\ 2\sqrt{2} & =VH\cdot \sqrt{19} \\ VH & =\frac{2\sqrt{2}}{\sqrt{19}} \\ VH & =\frac{2\sqrt{38}}{19}.\end{aligned}
$$


### changed-parameter observed presentation q-71115

Calculate the length of the altitude $VH$ of the $△\,TUV$, if $T(-2,-1,-1)$, $U(1,2,-5)$, $V(-5,1,-6).$

:answer-field.type/radio
- $\frac{\sqrt{2242}}{6}$
- $\frac{\sqrt{3363}}{38}$
- $\frac{\sqrt{118}}{2}$
- $\frac{19\sqrt{118}}{2}$
- $\frac{\sqrt{59}}{4}$

Worked solution

Note that the length of the altitude $VH$ can be related to the area of $△\,TUV$ as follows:

$$
{A}_{△}=\frac{1}{2}VH\cdot TU
$$

So, to find $VH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{TU}$ and $\overset{\to }{TV}:$

$$
\begin{aligned}\overset{\to }{TU} & =u-t \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{TV} & =v-t \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{TU}\times \overset{\to }{TV} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{TU}$ and $\overset{\to }{TV}$ is

$$
\begin{aligned}A & =|\overset{\to }{TU}\times \overset{\to }{TV}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,TUV$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $TU$ since it appears in the formula:

$$
\begin{aligned}TU & =|\overset{\to }{TU}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}VH\cdot TU,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}VH\cdot TU \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}VH\cdot \sqrt{34} \\ \sqrt{1003} & =VH\cdot \sqrt{34} \\ VH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ VH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-71116 original

Calculate the length of the altitude $ZH$ of the $△\,WYZ$, if $W(2,3,2)$, $Y(1,2,1)$, $Z(1,-1,1).$


Original full bank: $\sqrt{3}$, $\frac{3\sqrt{6}}{2}$, $2\sqrt{3}$, $\sqrt{6}$, $3\sqrt{2}$

Note that the length of the altitude $ZH$ can be related to the area of $△\,WYZ$ as follows:

$$
{A}_{△}=\frac{1}{2}ZH\cdot WY
$$

So, to find $ZH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{WY}$ and $\overset{\to }{WZ}:$

$$
\begin{aligned}\overset{\to }{WY} & =y-w \\  & =(i+2j+k)-(2i+3j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩ \\ \overset{\to }{WZ} & =z-w \\  & =(i-j+k)-(2i+3j+2k) \\  & =-i-4j-k \\  & =⟨-1,-4,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{WY}\times \overset{\to }{WZ} & =|\begin{aligned}i & j & k \\ -1 & -1 & -1 \\ -1 & -4 & -1\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ -4 & -1\end{aligned}|i-|\begin{aligned}-1 & -1 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-1 & -1 \\ -1 & -4\end{aligned}|k \\  & =((-1)\cdot (-1)-(-4)\cdot (-1))i-((-1)\cdot (-1)-(-1)\cdot (-1))j+((-1)\cdot (-4)-(-1)\cdot (-1))k \\  & =-3i+3k \\  & =⟨-3,0,3⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WY}$ and $\overset{\to }{WZ}$ is

$$
\begin{aligned}A & =|\overset{\to }{WY}\times \overset{\to }{WZ}| \\  & =\sqrt{(-3)^{2}+{0}^{2}+{3}^{2}} \\  & =\sqrt{18} \\  & =3\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WYZ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{2}}{2}.
$$

Let's also compute $WY$ since it appears in the formula:

$$
\begin{aligned}WY & =|\overset{\to }{WY}| \\  & =\sqrt{(-1)^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}ZH\cdot WY,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}ZH\cdot WY \\ \frac{3\sqrt{2}}{2} & =\frac{1}{2}ZH\cdot \sqrt{3} \\ 3\sqrt{2} & =ZH\cdot \sqrt{3} \\ ZH & =\frac{3\sqrt{2}}{\sqrt{3}} \\ ZH & =\sqrt{6}.\end{aligned}
$$


### source replay q-71116

Calculate the length of the altitude $ZH$ of the $△\,WYZ$, if $W(2,3,2)$, $Y(1,2,1)$, $Z(1,-1,1).$

:answer-field.type/radio
- $\frac{3\sqrt{6}}{2}$
- $3\sqrt{2}$
- $\sqrt{6}$
- $2\sqrt{3}$
- $\sqrt{3}$

Worked solution

Note that the length of the altitude $ZH$ can be related to the area of $△\,WYZ$ as follows:

$$
{A}_{△}=\frac{1}{2}ZH\cdot WY
$$

So, to find $ZH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{WY}$ and $\overset{\to }{WZ}:$

$$
\begin{aligned}\overset{\to }{WY} & =y-w \\  & =(i+2j+k)-(2i+3j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩ \\ \overset{\to }{WZ} & =z-w \\  & =(i-j+k)-(2i+3j+2k) \\  & =-i-4j-k \\  & =⟨-1,-4,-1⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{WY}\times \overset{\to }{WZ} & =|\begin{aligned}i & j & k \\ -1 & -1 & -1 \\ -1 & -4 & -1\end{aligned}| \\  & =|\begin{aligned}-1 & -1 \\ -4 & -1\end{aligned}|i-|\begin{aligned}-1 & -1 \\ -1 & -1\end{aligned}|j+|\begin{aligned}-1 & -1 \\ -1 & -4\end{aligned}|k \\  & =((-1)\cdot (-1)-(-4)\cdot (-1))i-((-1)\cdot (-1)-(-1)\cdot (-1))j+((-1)\cdot (-4)-(-1)\cdot (-1))k \\  & =-3i+3k \\  & =⟨-3,0,3⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WY}$ and $\overset{\to }{WZ}$ is

$$
\begin{aligned}A & =|\overset{\to }{WY}\times \overset{\to }{WZ}| \\  & =\sqrt{(-3)^{2}+{0}^{2}+{3}^{2}} \\  & =\sqrt{18} \\  & =3\sqrt{2}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WYZ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{2}}{2}.
$$

Let's also compute $WY$ since it appears in the formula:

$$
\begin{aligned}WY & =|\overset{\to }{WY}| \\  & =\sqrt{(-1)^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}ZH\cdot WY,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}ZH\cdot WY \\ \frac{3\sqrt{2}}{2} & =\frac{1}{2}ZH\cdot \sqrt{3} \\ 3\sqrt{2} & =ZH\cdot \sqrt{3} \\ ZH & =\frac{3\sqrt{2}}{\sqrt{3}} \\ ZH & =\sqrt{6}.\end{aligned}
$$


### changed-parameter observed presentation q-71116

Calculate the length of the altitude $ZH$ of the $△\,WYZ$, if $W(-2,-1,-1)$, $Y(1,2,-5)$, $Z(-5,1,-6).$

:answer-field.type/radio
- $\frac{\sqrt{354}}{2}$
- $\frac{\sqrt{118}}{2}$
- $\frac{\sqrt{59}}{2}$
- $\sqrt{59}$
- $\frac{3\sqrt{118}}{4}$

Worked solution

Note that the length of the altitude $ZH$ can be related to the area of $△\,WYZ$ as follows:

$$
{A}_{△}=\frac{1}{2}ZH\cdot WY
$$

So, to find $ZH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{WY}$ and $\overset{\to }{WZ}:$

$$
\begin{aligned}\overset{\to }{WY} & =y-w \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩ \\ \overset{\to }{WZ} & =z-w \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{WY}\times \overset{\to }{WZ} & =|\begin{aligned}i & j & k \\ 3 & 3 & -4 \\ -3 & 2 & -5\end{aligned}| \\  & =|\begin{aligned}3 & -4 \\ 2 & -5\end{aligned}|i-|\begin{aligned}3 & -4 \\ -3 & -5\end{aligned}|j+|\begin{aligned}3 & 3 \\ -3 & 2\end{aligned}|k \\  & =(3\cdot (-5)-2\cdot (-4))i-(3\cdot (-5)-(-3)\cdot (-4))j+(3\cdot 2-(-3)\cdot 3)k \\  & =-7i+27j+15k \\  & =⟨-7,27,15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{WY}$ and $\overset{\to }{WZ}$ is

$$
\begin{aligned}A & =|\overset{\to }{WY}\times \overset{\to }{WZ}| \\  & =\sqrt{(-7)^{2}+{27}^{2}+{15}^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,WYZ$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $WY$ since it appears in the formula:

$$
\begin{aligned}WY & =|\overset{\to }{WY}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}ZH\cdot WY,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}ZH\cdot WY \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}ZH\cdot \sqrt{34} \\ \sqrt{1003} & =ZH\cdot \sqrt{34} \\ ZH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ ZH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-71117 original

Calculate the length of the altitude $GH$ of the $△\,GSM$, if $S(1,-1,2)$, $G(-2,0,2)$, $M(1,1,0).$


Original full bank: $2\sqrt{19}$, $3\sqrt{2}$, $\sqrt{38}$, $\frac{\sqrt{38}}{2}$, $3\sqrt{38}$

Note that the length of the altitude $GH$ can be related to the area of $△\,GSM$ as follows:

$$
{A}_{△}=\frac{1}{2}GH\cdot SM
$$

So, to find $GH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{SG}$ and $\overset{\to }{SM}:$

$$
\begin{aligned}\overset{\to }{SG} & =g-s \\  & =(-2i+2k)-(i-j+2k) \\  & =-3i+j \\  & =⟨-3,1,0⟩ \\ \overset{\to }{SM} & =m-s \\  & =(i+j)-(i-j+2k) \\  & =2j-2k \\  & =⟨0,2,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{SG}\times \overset{\to }{SM} & =|\begin{aligned}i & j & k \\ -3 & 1 & 0 \\ 0 & 2 & -2\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 2 & -2\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 0 & -2\end{aligned}|j+|\begin{aligned}-3 & 1 \\ 0 & 2\end{aligned}|k \\  & =(1\cdot (-2)-2\cdot 0)i-((-3)\cdot (-2)-0\cdot 0)j+((-3)\cdot 2-0\cdot 1)k \\  & =-2i-6j-6k \\  & =⟨-2,-6,-6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{SG}$ and $\overset{\to }{SM}$ is

$$
\begin{aligned}A & =|\overset{\to }{SG}\times \overset{\to }{SM}| \\  & =\sqrt{(-2)^{2}+(-6)^{2}+(-6)^{2}} \\  & =\sqrt{76} \\  & =2\sqrt{19}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GSM$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{19}}{2}=\sqrt{19}.
$$

Let's also compute $SM$ since it appears in the formula:

$$
\begin{aligned}SM & =|\overset{\to }{SM}| \\  & =\sqrt{{0}^{2}+{2}^{2}+(-2)^{2}} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}GH\cdot SM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}GH\cdot SM \\ \sqrt{19} & =\frac{1}{2}GH\cdot 2\sqrt{2} \\ \sqrt{19} & =GH\cdot \sqrt{2} \\ GH & =\frac{\sqrt{19}}{\sqrt{2}} \\ GH & =\frac{\sqrt{38}}{2}.\end{aligned}
$$


### source replay q-71117

Calculate the length of the altitude $GH$ of the $△\,GSM$, if $S(1,-1,2)$, $G(-2,0,2)$, $M(1,1,0).$

:answer-field.type/radio
- $3\sqrt{2}$
- $3\sqrt{38}$
- $\frac{\sqrt{38}}{2}$
- $\sqrt{38}$
- $2\sqrt{19}$

Worked solution

Note that the length of the altitude $GH$ can be related to the area of $△\,GSM$ as follows:

$$
{A}_{△}=\frac{1}{2}GH\cdot SM
$$

So, to find $GH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{SG}$ and $\overset{\to }{SM}:$

$$
\begin{aligned}\overset{\to }{SG} & =g-s \\  & =(-2i+2k)-(i-j+2k) \\  & =-3i+j \\  & =⟨-3,1,0⟩ \\ \overset{\to }{SM} & =m-s \\  & =(i+j)-(i-j+2k) \\  & =2j-2k \\  & =⟨0,2,-2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{SG}\times \overset{\to }{SM} & =|\begin{aligned}i & j & k \\ -3 & 1 & 0 \\ 0 & 2 & -2\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 2 & -2\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 0 & -2\end{aligned}|j+|\begin{aligned}-3 & 1 \\ 0 & 2\end{aligned}|k \\  & =(1\cdot (-2)-2\cdot 0)i-((-3)\cdot (-2)-0\cdot 0)j+((-3)\cdot 2-0\cdot 1)k \\  & =-2i-6j-6k \\  & =⟨-2,-6,-6⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{SG}$ and $\overset{\to }{SM}$ is

$$
\begin{aligned}A & =|\overset{\to }{SG}\times \overset{\to }{SM}| \\  & =\sqrt{(-2)^{2}+(-6)^{2}+(-6)^{2}} \\  & =\sqrt{76} \\  & =2\sqrt{19}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GSM$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{19}}{2}=\sqrt{19}.
$$

Let's also compute $SM$ since it appears in the formula:

$$
\begin{aligned}SM & =|\overset{\to }{SM}| \\  & =\sqrt{{0}^{2}+{2}^{2}+(-2)^{2}} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}GH\cdot SM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}GH\cdot SM \\ \sqrt{19} & =\frac{1}{2}GH\cdot 2\sqrt{2} \\ \sqrt{19} & =GH\cdot \sqrt{2} \\ GH & =\frac{\sqrt{19}}{\sqrt{2}} \\ GH & =\frac{\sqrt{38}}{2}.\end{aligned}
$$


### changed-parameter observed presentation q-71117

Calculate the length of the altitude $GH$ of the $△\,GSM$, if $S(-2,-1,-1)$, $G(-5,1,-6)$, $M(1,2,-5).$

:answer-field.type/radio
- $3\sqrt{118}$
- $\frac{\sqrt{118}}{2}$
- $2\sqrt{59}$
- $\sqrt{118}$
- $\frac{3\sqrt{2242}}{19}$

Worked solution

Note that the length of the altitude $GH$ can be related to the area of $△\,GSM$ as follows:

$$
{A}_{△}=\frac{1}{2}GH\cdot SM
$$

So, to find $GH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{SG}$ and $\overset{\to }{SM}:$

$$
\begin{aligned}\overset{\to }{SG} & =g-s \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩ \\ \overset{\to }{SM} & =m-s \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{SG}\times \overset{\to }{SM} & =|\begin{aligned}i & j & k \\ -3 & 2 & -5 \\ 3 & 3 & -4\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 3 & -4\end{aligned}|i-|\begin{aligned}-3 & -5 \\ 3 & -4\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 3 & 3\end{aligned}|k \\  & =(2\cdot (-4)-3\cdot (-5))i-((-3)\cdot (-4)-3\cdot (-5))j+((-3)\cdot 3-3\cdot 2)k \\  & =7i-27j-15k \\  & =⟨7,-27,-15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{SG}$ and $\overset{\to }{SM}$ is

$$
\begin{aligned}A & =|\overset{\to }{SG}\times \overset{\to }{SM}| \\  & =\sqrt{{7}^{2}+(-27)^{2}+(-15)^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,GSM$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $SM$ since it appears in the formula:

$$
\begin{aligned}SM & =|\overset{\to }{SM}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}GH\cdot SM,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}GH\cdot SM \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}GH\cdot \sqrt{34} \\ \sqrt{1003} & =GH\cdot \sqrt{34} \\ GH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ GH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## q-71128 original

Calculate the length of the altitude $DH$ of the $△\,DMA$, if $D(-1,2,1)$, $M(-1,0,-1)$, $A(1,-2,1).$


Original full bank: $3\sqrt{2}$, $6\sqrt{2}$, $2\sqrt{6}$, $2\sqrt{2}$, $2\sqrt{3}$

Note that the length of the altitude $DH$ can be related to the area of $△\,DMA$ as follows:

$$
{A}_{△}=\frac{1}{2}DH\cdot MA
$$

So, to find $DH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{MD}$ and $\overset{\to }{MA}:$

$$
\begin{aligned}\overset{\to }{MD} & =d-m \\  & =(-i+2j+k)-(-i-k) \\  & =2j+2k \\  & =⟨0,2,2⟩ \\ \overset{\to }{MA} & =a-m \\  & =(i-2j+k)-(-i-k) \\  & =2i-2j+2k \\  & =⟨2,-2,2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{MD}\times \overset{\to }{MA} & =|\begin{aligned}i & j & k \\ 0 & 2 & 2 \\ 2 & -2 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ -2 & 2\end{aligned}|i-|\begin{aligned}0 & 2 \\ 2 & 2\end{aligned}|j+|\begin{aligned}0 & 2 \\ 2 & -2\end{aligned}|k \\  & =(2\cdot 2-(-2)\cdot 2)i-(0\cdot 2-2\cdot 2)j+(0\cdot (-2)-2\cdot 2)k \\  & =8i+4j-4k \\  & =⟨8,4,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{MD}$ and $\overset{\to }{MA}$ is

$$
\begin{aligned}A & =|\overset{\to }{MD}\times \overset{\to }{MA}| \\  & =\sqrt{{8}^{2}+{4}^{2}+(-4)^{2}} \\  & =\sqrt{96} \\  & =4\sqrt{6}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DMA$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{4\sqrt{6}}{2}=2\sqrt{6}.
$$

Let's also compute $MA$ since it appears in the formula:

$$
\begin{aligned}MA & =|\overset{\to }{MA}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{2}^{2}} \\  & =\sqrt{12} \\  & =2\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}DH\cdot MA,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}DH\cdot MA \\ 2\sqrt{6} & =\frac{1}{2}DH\cdot 2\sqrt{3} \\ 2\sqrt{6} & =DH\cdot \sqrt{3} \\ DH & =\frac{2\sqrt{6}}{\sqrt{3}} \\ DH & =2\sqrt{2}.\end{aligned}
$$


### source replay q-71128

Calculate the length of the altitude $DH$ of the $△\,DMA$, if $D(-1,2,1)$, $M(-1,0,-1)$, $A(1,-2,1).$

:answer-field.type/radio
- $6\sqrt{2}$
- $2\sqrt{3}$
- $2\sqrt{2}$
- $2\sqrt{6}$
- $3\sqrt{2}$

Worked solution

Note that the length of the altitude $DH$ can be related to the area of $△\,DMA$ as follows:

$$
{A}_{△}=\frac{1}{2}DH\cdot MA
$$

So, to find $DH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{MD}$ and $\overset{\to }{MA}:$

$$
\begin{aligned}\overset{\to }{MD} & =d-m \\  & =(-i+2j+k)-(-i-k) \\  & =2j+2k \\  & =⟨0,2,2⟩ \\ \overset{\to }{MA} & =a-m \\  & =(i-2j+k)-(-i-k) \\  & =2i-2j+2k \\  & =⟨2,-2,2⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{MD}\times \overset{\to }{MA} & =|\begin{aligned}i & j & k \\ 0 & 2 & 2 \\ 2 & -2 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 2 \\ -2 & 2\end{aligned}|i-|\begin{aligned}0 & 2 \\ 2 & 2\end{aligned}|j+|\begin{aligned}0 & 2 \\ 2 & -2\end{aligned}|k \\  & =(2\cdot 2-(-2)\cdot 2)i-(0\cdot 2-2\cdot 2)j+(0\cdot (-2)-2\cdot 2)k \\  & =8i+4j-4k \\  & =⟨8,4,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{MD}$ and $\overset{\to }{MA}$ is

$$
\begin{aligned}A & =|\overset{\to }{MD}\times \overset{\to }{MA}| \\  & =\sqrt{{8}^{2}+{4}^{2}+(-4)^{2}} \\  & =\sqrt{96} \\  & =4\sqrt{6}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DMA$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{4\sqrt{6}}{2}=2\sqrt{6}.
$$

Let's also compute $MA$ since it appears in the formula:

$$
\begin{aligned}MA & =|\overset{\to }{MA}| \\  & =\sqrt{{2}^{2}+(-2)^{2}+{2}^{2}} \\  & =\sqrt{12} \\  & =2\sqrt{3}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}DH\cdot MA,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}DH\cdot MA \\ 2\sqrt{6} & =\frac{1}{2}DH\cdot 2\sqrt{3} \\ 2\sqrt{6} & =DH\cdot \sqrt{3} \\ DH & =\frac{2\sqrt{6}}{\sqrt{3}} \\ DH & =2\sqrt{2}.\end{aligned}
$$


### changed-parameter observed presentation q-71128

Calculate the length of the altitude $DH$ of the $△\,DMA$, if $D(-5,1,-6)$, $M(-2,-1,-1)$, $A(1,2,-5).$

:answer-field.type/radio
- $\frac{\sqrt{177}}{2}$
- $\frac{\sqrt{118}}{2}$
- $\frac{3\sqrt{118}}{4}$
- $\frac{\sqrt{354}}{2}$
- $\frac{3\sqrt{118}}{2}$

Worked solution

Note that the length of the altitude $DH$ can be related to the area of $△\,DMA$ as follows:

$$
{A}_{△}=\frac{1}{2}DH\cdot MA
$$

So, to find $DH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{MD}$ and $\overset{\to }{MA}:$

$$
\begin{aligned}\overset{\to }{MD} & =d-m \\  & =(-5i+j-6k)-(-2i-j-k) \\  & =-3i+2j-5k \\  & =⟨-3,2,-5⟩ \\ \overset{\to }{MA} & =a-m \\  & =(i+2j-5k)-(-2i-j-k) \\  & =3i+3j-4k \\  & =⟨3,3,-4⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{MD}\times \overset{\to }{MA} & =|\begin{aligned}i & j & k \\ -3 & 2 & -5 \\ 3 & 3 & -4\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 3 & -4\end{aligned}|i-|\begin{aligned}-3 & -5 \\ 3 & -4\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 3 & 3\end{aligned}|k \\  & =(2\cdot (-4)-3\cdot (-5))i-((-3)\cdot (-4)-3\cdot (-5))j+((-3)\cdot 3-3\cdot 2)k \\  & =7i-27j-15k \\  & =⟨7,-27,-15⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{MD}$ and $\overset{\to }{MA}$ is

$$
\begin{aligned}A & =|\overset{\to }{MD}\times \overset{\to }{MA}| \\  & =\sqrt{{7}^{2}+(-27)^{2}+(-15)^{2}} \\  & =\sqrt{1003} \\  & =\sqrt{1003}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,DMA$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{1003}}{2}=\frac{\sqrt{1003}}{2}.
$$

Let's also compute $MA$ since it appears in the formula:

$$
\begin{aligned}MA & =|\overset{\to }{MA}| \\  & =\sqrt{{3}^{2}+{3}^{2}+(-4)^{2}} \\  & =\sqrt{34} \\  & =\sqrt{34}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}DH\cdot MA,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}DH\cdot MA \\ \frac{\sqrt{1003}}{2} & =\frac{1}{2}DH\cdot \sqrt{34} \\ \sqrt{1003} & =DH\cdot \sqrt{34} \\ DH & =\frac{\sqrt{1003}}{\sqrt{34}} \\ DH & =\frac{\sqrt{118}}{2}.\end{aligned}
$$


## authored easy radio 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(0,2,2)$, $B(-1,0,2)$, $C(-3,4,2).$

:answer-field.type/radio
- $\frac{8}{5}$
- $8$
- $\frac{8\sqrt{5}}{5}$
- $\frac{16\sqrt{5}}{5}$
- $\frac{4\sqrt{5}}{5}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+2k)-(2j+2k) \\  & =-i-2j \\  & =⟨-1,-2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3i+4j+2k)-(2j+2k) \\  & =-3i+2j \\  & =⟨-3,2,0⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & -2 & 0 \\ -3 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ 2 & 0\end{aligned}|i-|\begin{aligned}-1 & 0 \\ -3 & 0\end{aligned}|j+|\begin{aligned}-1 & -2 \\ -3 & 2\end{aligned}|k \\  & =((-2)\cdot 0-2\cdot 0)i-((-1)\cdot 0-(-3)\cdot 0)j+((-1)\cdot 2-(-3)\cdot (-2))k \\  & =-8k \\  & =⟨0,0,-8⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{0}^{2}+{0}^{2}+(-8)^{2}} \\  & =\sqrt{64} \\  & =8.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{8}{2}=4.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-1)^{2}+(-2)^{2}+{0}^{2}} \\  & =\sqrt{5} \\  & =\sqrt{5}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ 4 & =\frac{1}{2}CH\cdot \sqrt{5} \\ 8 & =CH\cdot \sqrt{5} \\ CH & =\frac{8}{\sqrt{5}} \\ CH & =\frac{8\sqrt{5}}{5}.\end{aligned}
$$


## authored easy radio 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,1,-2)$, $B(-1,4,-2)$, $C(-1,-1,-2).$

:answer-field.type/radio
- $\frac{\sqrt{10}}{4}$
- $\frac{\sqrt{10}}{2}$
- $\sqrt{10}$
- $\frac{1}{2}$
- $5$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+4j-2k)-(-2i+j-2k) \\  & =i+3j \\  & =⟨1,3,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i-j-2k)-(-2i+j-2k) \\  & =i-2j \\  & =⟨1,-2,0⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 1 & 3 & 0 \\ 1 & -2 & 0\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ -2 & 0\end{aligned}|i-|\begin{aligned}1 & 0 \\ 1 & 0\end{aligned}|j+|\begin{aligned}1 & 3 \\ 1 & -2\end{aligned}|k \\  & =(3\cdot 0-(-2)\cdot 0)i-(1\cdot 0-1\cdot 0)j+(1\cdot (-2)-1\cdot 3)k \\  & =-5k \\  & =⟨0,0,-5⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{0}^{2}+{0}^{2}+(-5)^{2}} \\  & =\sqrt{25} \\  & =5.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5}{2}=\frac{5}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{1}^{2}+{3}^{2}+{0}^{2}} \\  & =\sqrt{10} \\  & =\sqrt{10}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{5}{2} & =\frac{1}{2}CH\cdot \sqrt{10} \\ 5 & =CH\cdot \sqrt{10} \\ CH & =\frac{5}{\sqrt{10}} \\ CH & =\frac{\sqrt{10}}{2}.\end{aligned}
$$


## authored easy blank 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(0,2,2)$, $B(-1,0,2)$, $C(-3,4,2).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{8\sqrt{5}}{5}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+2k)-(2j+2k) \\  & =-i-2j \\  & =⟨-1,-2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3i+4j+2k)-(2j+2k) \\  & =-3i+2j \\  & =⟨-3,2,0⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -1 & -2 & 0 \\ -3 & 2 & 0\end{aligned}| \\  & =|\begin{aligned}-2 & 0 \\ 2 & 0\end{aligned}|i-|\begin{aligned}-1 & 0 \\ -3 & 0\end{aligned}|j+|\begin{aligned}-1 & -2 \\ -3 & 2\end{aligned}|k \\  & =((-2)\cdot 0-2\cdot 0)i-((-1)\cdot 0-(-3)\cdot 0)j+((-1)\cdot 2-(-3)\cdot (-2))k \\  & =-8k \\  & =⟨0,0,-8⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{0}^{2}+{0}^{2}+(-8)^{2}} \\  & =\sqrt{64} \\  & =8.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{8}{2}=4.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-1)^{2}+(-2)^{2}+{0}^{2}} \\  & =\sqrt{5} \\  & =\sqrt{5}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ 4 & =\frac{1}{2}CH\cdot \sqrt{5} \\ 8 & =CH\cdot \sqrt{5} \\ CH & =\frac{8}{\sqrt{5}} \\ CH & =\frac{8\sqrt{5}}{5}.\end{aligned}
$$


## authored easy blank 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(-2,1,-2)$, $B(-1,4,-2)$, $C(-1,-1,-2).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{10}}{2}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+4j-2k)-(-2i+j-2k) \\  & =i+3j \\  & =⟨1,3,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i-j-2k)-(-2i+j-2k) \\  & =i-2j \\  & =⟨1,-2,0⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 1 & 3 & 0 \\ 1 & -2 & 0\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ -2 & 0\end{aligned}|i-|\begin{aligned}1 & 0 \\ 1 & 0\end{aligned}|j+|\begin{aligned}1 & 3 \\ 1 & -2\end{aligned}|k \\  & =(3\cdot 0-(-2)\cdot 0)i-(1\cdot 0-1\cdot 0)j+(1\cdot (-2)-1\cdot 3)k \\  & =-5k \\  & =⟨0,0,-5⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{0}^{2}+{0}^{2}+(-5)^{2}} \\  & =\sqrt{25} \\  & =5.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{5}{2}=\frac{5}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{1}^{2}+{3}^{2}+{0}^{2}} \\  & =\sqrt{10} \\  & =\sqrt{10}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{5}{2} & =\frac{1}{2}CH\cdot \sqrt{10} \\ 5 & =CH\cdot \sqrt{10} \\ CH & =\frac{5}{\sqrt{10}} \\ CH & =\frac{\sqrt{10}}{2}.\end{aligned}
$$


## authored moderate radio 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(2,-1,0)$, $B(-1,1,0)$, $C(1,1,3).$

:answer-field.type/radio
- $\sqrt{133}$
- $\frac{\sqrt{1729}}{26}$
- $\frac{2\sqrt{1729}}{13}$
- $\frac{\sqrt{133}}{13}$
- $\frac{\sqrt{1729}}{13}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+j)-(2i-j) \\  & =-3i+2j \\  & =⟨-3,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+3k)-(2i-j) \\  & =-i+2j+3k \\  & =⟨-1,2,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ -1 & 2 & 3\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 2 & 3\end{aligned}|i-|\begin{aligned}-3 & 0 \\ -1 & 3\end{aligned}|j+|\begin{aligned}-3 & 2 \\ -1 & 2\end{aligned}|k \\  & =(2\cdot 3-2\cdot 0)i-((-3)\cdot 3-(-1)\cdot 0)j+((-3)\cdot 2-(-1)\cdot 2)k \\  & =6i+9j-4k \\  & =⟨6,9,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{6}^{2}+{9}^{2}+(-4)^{2}} \\  & =\sqrt{133} \\  & =\sqrt{133}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{133}}{2}=\frac{\sqrt{133}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-3)^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{13} \\  & =\sqrt{13}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{133}}{2} & =\frac{1}{2}CH\cdot \sqrt{13} \\ \sqrt{133} & =CH\cdot \sqrt{13} \\ CH & =\frac{\sqrt{133}}{\sqrt{13}} \\ CH & =\frac{\sqrt{1729}}{13}.\end{aligned}
$$


## authored moderate radio 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,1,1)$, $B(-1,3,1)$, $C(-2,0,-2).$

:answer-field.type/radio
- $2\sqrt{17}$
- $\frac{\sqrt{34}}{4}$
- $\sqrt{17}$
- $\frac{\sqrt{17}}{2}$
- $2\sqrt{34}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+3j+k)-(i+j+k) \\  & =-2i+2j \\  & =⟨-2,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2k)-(i+j+k) \\  & =-3i-j-3k \\  & =⟨-3,-1,-3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -2 & 2 & 0 \\ -3 & -1 & -3\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -1 & -3\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -3 & -3\end{aligned}|j+|\begin{aligned}-2 & 2 \\ -3 & -1\end{aligned}|k \\  & =(2\cdot (-3)-(-1)\cdot 0)i-((-2)\cdot (-3)-(-3)\cdot 0)j+((-2)\cdot (-1)-(-3)\cdot 2)k \\  & =-6i-6j+8k \\  & =⟨-6,-6,8⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-6)^{2}+(-6)^{2}+{8}^{2}} \\  & =\sqrt{136} \\  & =2\sqrt{34}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{34}}{2}=\sqrt{34}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-2)^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{34} & =\frac{1}{2}CH\cdot 2\sqrt{2} \\ \sqrt{34} & =CH\cdot \sqrt{2} \\ CH & =\frac{\sqrt{34}}{\sqrt{2}} \\ CH & =\sqrt{17}.\end{aligned}
$$


## authored moderate blank 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(2,-1,0)$, $B(-1,1,0)$, $C(1,1,3).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{1729}}{13}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+j)-(2i-j) \\  & =-3i+2j \\  & =⟨-3,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+3k)-(2i-j) \\  & =-i+2j+3k \\  & =⟨-1,2,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ -1 & 2 & 3\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 2 & 3\end{aligned}|i-|\begin{aligned}-3 & 0 \\ -1 & 3\end{aligned}|j+|\begin{aligned}-3 & 2 \\ -1 & 2\end{aligned}|k \\  & =(2\cdot 3-2\cdot 0)i-((-3)\cdot 3-(-1)\cdot 0)j+((-3)\cdot 2-(-1)\cdot 2)k \\  & =6i+9j-4k \\  & =⟨6,9,-4⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{6}^{2}+{9}^{2}+(-4)^{2}} \\  & =\sqrt{133} \\  & =\sqrt{133}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{133}}{2}=\frac{\sqrt{133}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-3)^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{13} \\  & =\sqrt{13}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{133}}{2} & =\frac{1}{2}CH\cdot \sqrt{13} \\ \sqrt{133} & =CH\cdot \sqrt{13} \\ CH & =\frac{\sqrt{133}}{\sqrt{13}} \\ CH & =\frac{\sqrt{1729}}{13}.\end{aligned}
$$


## authored moderate blank 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,1,1)$, $B(-1,3,1)$, $C(-2,0,-2).$

$CH=${{field-1}}

:answer-field.type/blank
- $\sqrt{17}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+3j+k)-(i+j+k) \\  & =-2i+2j \\  & =⟨-2,2,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2k)-(i+j+k) \\  & =-3i-j-3k \\  & =⟨-3,-1,-3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -2 & 2 & 0 \\ -3 & -1 & -3\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -1 & -3\end{aligned}|i-|\begin{aligned}-2 & 0 \\ -3 & -3\end{aligned}|j+|\begin{aligned}-2 & 2 \\ -3 & -1\end{aligned}|k \\  & =(2\cdot (-3)-(-1)\cdot 0)i-((-2)\cdot (-3)-(-3)\cdot 0)j+((-2)\cdot (-1)-(-3)\cdot 2)k \\  & =-6i-6j+8k \\  & =⟨-6,-6,8⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-6)^{2}+(-6)^{2}+{8}^{2}} \\  & =\sqrt{136} \\  & =2\sqrt{34}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{2\sqrt{34}}{2}=\sqrt{34}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-2)^{2}+{2}^{2}+{0}^{2}} \\  & =\sqrt{8} \\  & =2\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \sqrt{34} & =\frac{1}{2}CH\cdot 2\sqrt{2} \\ \sqrt{34} & =CH\cdot \sqrt{2} \\ CH & =\frac{\sqrt{34}}{\sqrt{2}} \\ CH & =\sqrt{17}.\end{aligned}
$$


## authored hard radio 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,0,1)$, $B(3,2,-4)$, $C(0,4,4).$

:answer-field.type/radio
- $\sqrt{777}$
- $\frac{\sqrt{2849}}{11}$
- $\frac{\sqrt{777}}{33}$
- $\frac{\sqrt{2849}}{22}$
- $\frac{2\sqrt{2849}}{11}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+2j-4k)-(i+k) \\  & =2i+2j-5k \\  & =⟨2,2,-5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4j+4k)-(i+k) \\  & =-i+4j+3k \\  & =⟨-1,4,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 2 & -5 \\ -1 & 4 & 3\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 4 & 3\end{aligned}|i-|\begin{aligned}2 & -5 \\ -1 & 3\end{aligned}|j+|\begin{aligned}2 & 2 \\ -1 & 4\end{aligned}|k \\  & =(2\cdot 3-4\cdot (-5))i-(2\cdot 3-(-1)\cdot (-5))j+(2\cdot 4-(-1)\cdot 2)k \\  & =26i-j+10k \\  & =⟨26,-1,10⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{26}^{2}+(-1)^{2}+{10}^{2}} \\  & =\sqrt{777} \\  & =\sqrt{777}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{777}}{2}=\frac{\sqrt{777}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{2}^{2}+{2}^{2}+(-5)^{2}} \\  & =\sqrt{33} \\  & =\sqrt{33}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{777}}{2} & =\frac{1}{2}CH\cdot \sqrt{33} \\ \sqrt{777} & =CH\cdot \sqrt{33} \\ CH & =\frac{\sqrt{777}}{\sqrt{33}} \\ CH & =\frac{\sqrt{2849}}{11}.\end{aligned}
$$


## authored hard radio 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,1,1)$, $B(-2,6,-3)$, $C(0,-3,4).$

:answer-field.type/radio
- $\frac{3\sqrt{102}}{5}$
- $3\sqrt{51}$
- $\frac{3\sqrt{51}}{50}$
- $\frac{3\sqrt{102}}{10}$
- $\frac{3\sqrt{102}}{20}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+6j-3k)-(i+j+k) \\  & =-3i+5j-4k \\  & =⟨-3,5,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3j+4k)-(i+j+k) \\  & =-i-4j+3k \\  & =⟨-1,-4,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -3 & 5 & -4 \\ -1 & -4 & 3\end{aligned}| \\  & =|\begin{aligned}5 & -4 \\ -4 & 3\end{aligned}|i-|\begin{aligned}-3 & -4 \\ -1 & 3\end{aligned}|j+|\begin{aligned}-3 & 5 \\ -1 & -4\end{aligned}|k \\  & =(5\cdot 3-(-4)\cdot (-4))i-((-3)\cdot 3-(-1)\cdot (-4))j+((-3)\cdot (-4)-(-1)\cdot 5)k \\  & =-i+13j+17k \\  & =⟨-1,13,17⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-1)^{2}+{13}^{2}+{17}^{2}} \\  & =\sqrt{459} \\  & =3\sqrt{51}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{51}}{2}=\frac{3\sqrt{51}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-3)^{2}+{5}^{2}+(-4)^{2}} \\  & =\sqrt{50} \\  & =5\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{3\sqrt{51}}{2} & =\frac{1}{2}CH\cdot 5\sqrt{2} \\ 3\sqrt{51} & =CH\cdot 5\sqrt{2} \\ CH & =\frac{3\sqrt{51}}{5\sqrt{2}} \\ CH & =\frac{3\sqrt{102}}{10}.\end{aligned}
$$


## authored hard blank 0

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,0,1)$, $B(3,2,-4)$, $C(0,4,4).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{\sqrt{2849}}{11}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+2j-4k)-(i+k) \\  & =2i+2j-5k \\  & =⟨2,2,-5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4j+4k)-(i+k) \\  & =-i+4j+3k \\  & =⟨-1,4,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ 2 & 2 & -5 \\ -1 & 4 & 3\end{aligned}| \\  & =|\begin{aligned}2 & -5 \\ 4 & 3\end{aligned}|i-|\begin{aligned}2 & -5 \\ -1 & 3\end{aligned}|j+|\begin{aligned}2 & 2 \\ -1 & 4\end{aligned}|k \\  & =(2\cdot 3-4\cdot (-5))i-(2\cdot 3-(-1)\cdot (-5))j+(2\cdot 4-(-1)\cdot 2)k \\  & =26i-j+10k \\  & =⟨26,-1,10⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{{26}^{2}+(-1)^{2}+{10}^{2}} \\  & =\sqrt{777} \\  & =\sqrt{777}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{\sqrt{777}}{2}=\frac{\sqrt{777}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{{2}^{2}+{2}^{2}+(-5)^{2}} \\  & =\sqrt{33} \\  & =\sqrt{33}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{\sqrt{777}}{2} & =\frac{1}{2}CH\cdot \sqrt{33} \\ \sqrt{777} & =CH\cdot \sqrt{33} \\ CH & =\frac{\sqrt{777}}{\sqrt{33}} \\ CH & =\frac{\sqrt{2849}}{11}.\end{aligned}
$$


## authored hard blank 1

Calculate the length of the altitude $CH$ of the $△\,ABC$, if $A(1,1,1)$, $B(-2,6,-3)$, $C(0,-3,4).$

$CH=${{field-1}}

:answer-field.type/blank
- $\frac{3\sqrt{102}}{10}$

Worked solution

Note that the length of the altitude $CH$ can be related to the area of $△\,ABC$ as follows:

$$
{A}_{△}=\frac{1}{2}CH\cdot AB
$$

So, to find $CH,$ we first find ${A}_{△}.$ To start, we find the vectors $\overset{\to }{AB}$ and $\overset{\to }{AC}:$

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+6j-3k)-(i+j+k) \\  & =-3i+5j-4k \\  & =⟨-3,5,-4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-3j+4k)-(i+j+k) \\  & =-i-4j+3k \\  & =⟨-1,-4,3⟩\end{aligned}
$$

Now, we have

$$
\begin{aligned}\overset{\to }{AB}\times \overset{\to }{AC} & =|\begin{aligned}i & j & k \\ -3 & 5 & -4 \\ -1 & -4 & 3\end{aligned}| \\  & =|\begin{aligned}5 & -4 \\ -4 & 3\end{aligned}|i-|\begin{aligned}-3 & -4 \\ -1 & 3\end{aligned}|j+|\begin{aligned}-3 & 5 \\ -1 & -4\end{aligned}|k \\  & =(5\cdot 3-(-4)\cdot (-4))i-((-3)\cdot 3-(-1)\cdot (-4))j+((-3)\cdot (-4)-(-1)\cdot 5)k \\  & =-i+13j+17k \\  & =⟨-1,13,17⟩.\end{aligned}
$$

Therefore, the area of the parallelogram spanned by $\overset{\to }{AB}$ and $\overset{\to }{AC}$ is

$$
\begin{aligned}A & =|\overset{\to }{AB}\times \overset{\to }{AC}| \\  & =\sqrt{(-1)^{2}+{13}^{2}+{17}^{2}} \\  & =\sqrt{459} \\  & =3\sqrt{51}.\end{aligned}
$$

The area of the triangle is half of the area of the respective parallelogram. So, the area of $△\,ABC$ is

$$
{A}_{△}=\frac{1}{2}A=\frac{3\sqrt{51}}{2}=\frac{3\sqrt{51}}{2}.
$$

Let's also compute $AB$ since it appears in the formula:

$$
\begin{aligned}AB & =|\overset{\to }{AB}| \\  & =\sqrt{(-3)^{2}+{5}^{2}+(-4)^{2}} \\  & =\sqrt{50} \\  & =5\sqrt{2}.\end{aligned}
$$

 

Finally, using the formula ${A}_{△}=\frac{1}{2}CH\cdot AB,$ we get

$$
\begin{aligned}{A}_{△} & =\frac{1}{2}CH\cdot AB \\ \frac{3\sqrt{51}}{2} & =\frac{1}{2}CH\cdot 5\sqrt{2} \\ 3\sqrt{51} & =CH\cdot 5\sqrt{2} \\ CH & =\frac{3\sqrt{51}}{5\sqrt{2}} \\ CH & =\frac{3\sqrt{102}}{10}.\end{aligned}
$$
