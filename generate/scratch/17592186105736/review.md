# Review

Original raw records and generated variants are explicitly labeled. Raw opaque banks are evidence-only. Authored default banks and hard scope are identified in extraction.

## Original q-20051 (raw evidence, ineligible)

Let $a = ⟨3, 1,-3⟩$, $b = ⟨2, 6,-2⟩$ and $c = ⟨0, 1,-4⟩$. Find $a \cdot (b \cdot c)$.

Worked solution ABSENT in source.

Bank: -68, -58, -64, -72, -70; correct: ABSENT

### Generated homogeneous raw replay (evidence-only) observed:q-20051

Let $a = ⟨3, 1,-3⟩$, $b = ⟨4, 12,-4⟩$ and $c = ⟨0, 2,-8⟩$. Find $a \cdot (b \cdot c)$.

- $-256$

- $-288$

- $-232$

- $-272$

- $-280$

### Generated authored bank, independent coordinates omit_terms

Let $a = ⟨5,1,-5⟩$, $b = ⟨1,3,-2⟩$ and $c = ⟨0,2,-3⟩$. Find $a \cdot (b \times c)$.

- $32$

- $-32$

- $0$

- $-7$

- $-35$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}5 & 1 & -5 \\ 1 & 3 & -2 \\ 0 & 2 & -3\end{aligned}| \\  & =5\cdot |\begin{aligned}3 & -2 \\ 2 & -3\end{aligned}|-1\cdot |\begin{aligned}1 & -2 \\ 0 & -3\end{aligned}|+(-5)\cdot |\begin{aligned}1 & 3 \\ 0 & 2\end{aligned}| \\  & =5\cdot (3\cdot (-3)-(-2)\cdot 2)-(1\cdot (-3)-(-2)\cdot 0)+(-5)\cdot (1\cdot 2-3\cdot 0) \\  & =-25+3-10 \\  & =-32.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a = ⟨5,1,-6⟩$, $b = ⟨2,3,-6⟩$ and $c = ⟨0,5,-5⟩$. Find $a \cdot (b \times c)$.

- $-25$

- $35$

- $-125$

- $25$

- $-275$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}5 & 1 & -6 \\ 2 & 3 & -6 \\ 0 & 5 & -5\end{aligned}| \\  & =5\cdot |\begin{aligned}3 & -6 \\ 5 & -5\end{aligned}|-1\cdot |\begin{aligned}2 & -6 \\ 0 & -5\end{aligned}|+(-6)\cdot |\begin{aligned}2 & 3 \\ 0 & 5\end{aligned}| \\  & =5\cdot (3\cdot (-5)-(-6)\cdot 5)-(2\cdot (-5)-(-6)\cdot 0)+(-6)\cdot (2\cdot 5-3\cdot 0) \\  & =75+10-60 \\  & =25.\end{aligned}
$$

## Original q-20056 (raw evidence, ineligible)

Let $p=⟨2,-1,0⟩$, $q=⟨3,-3,2⟩$ and $r=⟨1,-4,1⟩.$ Find $r\cdot (q\times p).$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}1 & -4 & 1 \\ 3 & -3 & 2 \\ 2 & -1 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-3 & 2 \\ -1 & 0\end{aligned}|-(-4)\cdot |\begin{aligned}3 & 2 \\ 2 & 0\end{aligned}|+1\cdot |\begin{aligned}3 & -3 \\ 2 & -1\end{aligned}| \\  & =((-3)\cdot 0-(-1)\cdot 2)+4(3\cdot 0-2\cdot 2)+(3\cdot (-1)-2\cdot (-3)) \\  & =2-16+3 \\  & =-11.\end{aligned}
$$

Bank: -8, 14, -13, 11, -11; correct: ABSENT

Bank: -11, -8, 11, 14, -13; correct: -11

### Generated homogeneous raw replay (evidence-only) observed:q-20056

Let $p=⟨4,-2,0⟩$, $q=⟨6,-6,4⟩$ and $r=⟨1,-4,1⟩.$ Find $r\cdot (q\times p).$

- $-52$

- $44$

- $56$

- $-32$

- $-44$

- $56$

- $-44$

- $44$

- $-52$

- $-32$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}1 & -4 & 1 \\ 6 & -6 & 4 \\ 4 & -2 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-6 & 4 \\ -2 & 0\end{aligned}|-(-4)\cdot |\begin{aligned}6 & 4 \\ 4 & 0\end{aligned}|+1\cdot |\begin{aligned}6 & -6 \\ 4 & -2\end{aligned}| \\  & =((-6)\cdot 0-(-2)\cdot 4)+4(6\cdot 0-4\cdot 4)+(6\cdot (-2)-4\cdot (-6)) \\  & =8-64+12 \\  & =-44.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $p=⟨2,-2,0⟩$, $q=⟨5,-1,3⟩$ and $r=⟨1,-5,1⟩.$ Find $r\cdot (q\times p).$

- $32$

- $-32$

- $4$

- $-38$

- $-2$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}1 & -5 & 1 \\ 5 & -1 & 3 \\ 2 & -2 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-1 & 3 \\ -2 & 0\end{aligned}|-(-5)\cdot |\begin{aligned}5 & 3 \\ 2 & 0\end{aligned}|+1\cdot |\begin{aligned}5 & -1 \\ 2 & -2\end{aligned}| \\  & =((-1)\cdot 0-3\cdot (-2))-(-5)\cdot (5\cdot 0-3\cdot 2)+(5\cdot (-2)-(-1)\cdot 2) \\  & =6-30-8 \\  & =-32.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $p=⟨6,-5,0⟩$, $q=⟨6,-2,3⟩$ and $r=⟨1,-5,1⟩.$ Find $r\cdot (q\times p).$

- $93$

- $15$

- $-123$

- $-93$

- $33$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}1 & -5 & 1 \\ 6 & -2 & 3 \\ 6 & -5 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-2 & 3 \\ -5 & 0\end{aligned}|-(-5)\cdot |\begin{aligned}6 & 3 \\ 6 & 0\end{aligned}|+1\cdot |\begin{aligned}6 & -2 \\ 6 & -5\end{aligned}| \\  & =((-2)\cdot 0-3\cdot (-5))-(-5)\cdot (6\cdot 0-3\cdot 6)+(6\cdot (-5)-(-2)\cdot 6) \\  & =15-90-18 \\  & =-93.\end{aligned}
$$

## Original q-128107 (raw evidence, ineligible)

Let $a=⟨0,9,3⟩,$ $b=⟨3,2,0⟩$ and $c=⟨-1,1,1⟩.$ Find $a\cdot (b\times c).$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 9 & 3 \\ 3 & 2 & 0 \\ -1 & 1 & 1\end{aligned}| \\  & =0\cdot |\begin{aligned}2 & 0 \\ 1 & 1\end{aligned}|-9\cdot |\begin{aligned}3 & 0 \\ -1 & 1\end{aligned}|+3\cdot |\begin{aligned}3 & 2 \\ -1 & 1\end{aligned}| \\  & =0-9(3\cdot 1-(-1)\cdot 0)+3(3\cdot 1-(-1)\cdot 2) \\  & =0-27+15 \\  & =-12.\end{aligned}
$$

Bank: 12, -27, 15, -12, 42; correct: -12

### Generated homogeneous raw replay (evidence-only) observed:q-128107

Let $a=⟨0,9,3⟩,$ $b=⟨6,4,0⟩$ and $c=⟨-2,2,2⟩.$ Find $a\cdot (b\times c).$

- $60$

- $-48$

- $-108$

- $48$

- $168$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 9 & 3 \\ 6 & 4 & 0 \\ -2 & 2 & 2\end{aligned}| \\  & =0\cdot |\begin{aligned}4 & 0 \\ 2 & 2\end{aligned}|-9\cdot |\begin{aligned}6 & 0 \\ -2 & 2\end{aligned}|+3\cdot |\begin{aligned}6 & 4 \\ -2 & 2\end{aligned}| \\  & =0-9(6\cdot 2-(-2)\cdot 0)+3(6\cdot 2-(-2)\cdot 4) \\  & =0-108+60 \\  & =-48.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $a=⟨0,5,5⟩,$ $b=⟨1,3,0⟩$ and $c=⟨-2,2,3⟩.$ Find $a\cdot (b\times c).$

- $-25$

- $25$

- $14$

- $40$

- $-15$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 5 & 5 \\ 1 & 3 & 0 \\ -2 & 2 & 3\end{aligned}| \\  & =0\cdot |\begin{aligned}3 & 0 \\ 2 & 3\end{aligned}|-5\cdot |\begin{aligned}1 & 0 \\ -2 & 3\end{aligned}|+5\cdot |\begin{aligned}1 & 3 \\ -2 & 2\end{aligned}| \\  & =0-5\cdot (1\cdot 3-0\cdot (-2))+5\cdot (1\cdot 2-3\cdot (-2)) \\  & =0-15+40 \\  & =25.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨0,5,6⟩,$ $b=⟨2,3,0⟩$ and $c=⟨-6,5,5⟩.$ Find $a\cdot (b\times c).$

- $-118$

- $33$

- $218$

- $118$

- $-98$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 5 & 6 \\ 2 & 3 & 0 \\ -6 & 5 & 5\end{aligned}| \\  & =0\cdot |\begin{aligned}3 & 0 \\ 5 & 5\end{aligned}|-5\cdot |\begin{aligned}2 & 0 \\ -6 & 5\end{aligned}|+6\cdot |\begin{aligned}2 & 3 \\ -6 & 5\end{aligned}| \\  & =0-5\cdot (2\cdot 5-0\cdot (-6))+6\cdot (2\cdot 5-3\cdot (-6)) \\  & =0-50+168 \\  & =118.\end{aligned}
$$

## Original q-128347 (raw evidence, ineligible)

Let $p=⟨7,4,9⟩,$ $q=⟨1,2,-2⟩$ and $r=⟨3,0,5⟩.$ Find $q\cdot (r\times p).$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 2 & -2 \\ 3 & 0 & 5 \\ 7 & 4 & 9\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 5 \\ 4 & 9\end{aligned}|-2\cdot |\begin{aligned}3 & 5 \\ 7 & 9\end{aligned}|+(-2)\cdot |\begin{aligned}3 & 0 \\ 7 & 4\end{aligned}| \\  & =(0\cdot 9-4\cdot 5)-2(3\cdot 9-7\cdot 5)-2(3\cdot 4-7\cdot 0) \\  & =-20+16-24 \\  & =-28.\end{aligned}
$$

Bank: -60, -28, 12, 20, -20; correct: -28

### Generated homogeneous raw replay (evidence-only) observed:q-128347

Let $p=⟨14,8,18⟩,$ $q=⟨1,2,-2⟩$ and $r=⟨6,0,10⟩.$ Find $q\cdot (r\times p).$

- $48$

- $80$

- $-112$

- $-240$

- $-80$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 2 & -2 \\ 6 & 0 & 10 \\ 14 & 8 & 18\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 10 \\ 8 & 18\end{aligned}|-2\cdot |\begin{aligned}6 & 10 \\ 14 & 18\end{aligned}|+(-2)\cdot |\begin{aligned}6 & 0 \\ 14 & 8\end{aligned}| \\  & =(0\cdot 18-8\cdot 10)-2(6\cdot 18-14\cdot 10)-2(6\cdot 8-14\cdot 0) \\  & =-80+64-96 \\  & =-112.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $p=⟨5,2,5⟩,$ $q=⟨1,1,-2⟩$ and $r=⟨5,0,1⟩.$ Find $q\cdot (r\times p).$

- $42$

- $-42$

- $-12$

- $-40$

- $-22$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 1 & -2 \\ 5 & 0 & 1 \\ 5 & 2 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ 2 & 5\end{aligned}|-1\cdot |\begin{aligned}5 & 1 \\ 5 & 5\end{aligned}|+(-2)\cdot |\begin{aligned}5 & 0 \\ 5 & 2\end{aligned}| \\  & =(0\cdot 5-1\cdot 2)-(5\cdot 5-1\cdot 5)+(-2)\cdot (5\cdot 2-0\cdot 5) \\  & =-2-20-20 \\  & =-42.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $p=⟨6,5,5⟩,$ $q=⟨1,5,-6⟩$ and $r=⟨2,0,3⟩.$ Find $q\cdot (r\times p).$

- $35$

- $3$

- $-5$

- $-35$

- $-185$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 5 & -6 \\ 2 & 0 & 3 \\ 6 & 5 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 3 \\ 5 & 5\end{aligned}|-5\cdot |\begin{aligned}2 & 3 \\ 6 & 5\end{aligned}|+(-6)\cdot |\begin{aligned}2 & 0 \\ 6 & 5\end{aligned}| \\  & =(0\cdot 5-3\cdot 5)-5\cdot (2\cdot 5-3\cdot 6)+(-6)\cdot (2\cdot 5-0\cdot 6) \\  & =-15+40-60 \\  & =-35.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $p=⟨4,4,5⟩,$ $q=⟨1,2,-1⟩$ and $r=⟨4,0,1⟩.$ Find $q\cdot (r\times p).$

- $-52$

- $-60$

- $52$

- $-44$

- $-4$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 2 & -1 \\ 4 & 0 & 1 \\ 4 & 4 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ 4 & 5\end{aligned}|-2\cdot |\begin{aligned}4 & 1 \\ 4 & 5\end{aligned}|+(-1)\cdot |\begin{aligned}4 & 0 \\ 4 & 4\end{aligned}| \\  & =(0\cdot 5-1\cdot 4)-2\cdot (4\cdot 5-1\cdot 4)+(-1)\cdot (4\cdot 4-0\cdot 4) \\  & =-4-32-16 \\  & =-52.\end{aligned}
$$

## Original q-18657 (raw evidence, ineligible)

Let $a=⟨-2,0,1⟩$, $b=⟨5,2,-4⟩$ and $c=⟨1,0,3⟩.$ Find $a\cdot (b\times c).$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 0 & 1 \\ 5 & 2 & -4 \\ 1 & 0 & 3\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}2 & -4 \\ 0 & 3\end{aligned}|-0\cdot |\begin{aligned}5 & -4 \\ 1 & 3\end{aligned}|+1\cdot |\begin{aligned}5 & 2 \\ 1 & 0\end{aligned}| \\  & =-2(2\cdot 3-(-4)\cdot 0)-0+(5\cdot 0-2\cdot 1) \\  & =-12-0-2 \\  & =-14.\end{aligned}
$$

Bank: -2, 12, 2, -14, 0; correct: -14

### Generated homogeneous raw replay (evidence-only) observed:q-18657

Let $a=⟨-2,0,1⟩$, $b=⟨10,4,-8⟩$ and $c=⟨2,0,6⟩.$ Find $a\cdot (b\times c).$

- $8$

- $-56$

- $48$

- $-8$

- $0$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 0 & 1 \\ 10 & 4 & -8 \\ 2 & 0 & 6\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}4 & -8 \\ 0 & 6\end{aligned}|-0\cdot |\begin{aligned}10 & -8 \\ 2 & 6\end{aligned}|+1\cdot |\begin{aligned}10 & 4 \\ 2 & 0\end{aligned}| \\  & =-2(4\cdot 6-(-8)\cdot 0)-0+(10\cdot 0-4\cdot 2) \\  & =-48-0-8 \\  & =-56.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $a=⟨-5,0,1⟩$, $b=⟨5,1,-3⟩$ and $c=⟨2,0,2⟩.$ Find $a\cdot (b\times c).$

- $12$

- $-12$

- $-16$

- $-2$

- $-10$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-5 & 0 & 1 \\ 5 & 1 & -3 \\ 2 & 0 & 2\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}1 & -3 \\ 0 & 2\end{aligned}|-0\cdot |\begin{aligned}5 & -3 \\ 2 & 2\end{aligned}|+1\cdot |\begin{aligned}5 & 1 \\ 2 & 0\end{aligned}| \\  & =(-5)\cdot (1\cdot 2-(-3)\cdot 0)-0+(5\cdot 0-1\cdot 2) \\  & =-10+0-2 \\  & =-12.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨-5,0,1⟩$, $b=⟨6,2,-3⟩$ and $c=⟨6,0,5⟩.$ Find $a\cdot (b\times c).$

- $62$

- $-50$

- $38$

- $-62$

- $-38$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-5 & 0 & 1 \\ 6 & 2 & -3 \\ 6 & 0 & 5\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}2 & -3 \\ 0 & 5\end{aligned}|-0\cdot |\begin{aligned}6 & -3 \\ 6 & 5\end{aligned}|+1\cdot |\begin{aligned}6 & 2 \\ 6 & 0\end{aligned}| \\  & =(-5)\cdot (2\cdot 5-(-3)\cdot 0)-0+(6\cdot 0-2\cdot 6) \\  & =-50+0-12 \\  & =-62.\end{aligned}
$$

## Original q-20050 (raw evidence, ineligible)

Let $a=⟨1,3,2⟩$, $b=⟨3,4,1⟩$ and $c=⟨2,0,1⟩.$ Find $a\cdot (b\times c).$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 3 & 2 \\ 3 & 4 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =1\cdot |\begin{aligned}4 & 1 \\ 0 & 1\end{aligned}|-3\cdot |\begin{aligned}3 & 1 \\ 2 & 1\end{aligned}|+2\cdot |\begin{aligned}3 & 4 \\ 2 & 0\end{aligned}| \\  & =(4\cdot 1-0\cdot 1)-3(3\cdot 1-2\cdot 1)+2(3\cdot 0-2\cdot 4) \\  & =4-3-16 \\  & =-15.\end{aligned}
$$

Bank: -15, -17, 17, -14, -19; correct: -15

### Generated homogeneous raw replay (evidence-only) observed:q-20050

Let $a=⟨1,3,2⟩$, $b=⟨6,8,2⟩$ and $c=⟨4,0,2⟩.$ Find $a\cdot (b\times c).$

- $68$

- $-56$

- $-68$

- $-60$

- $-76$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 3 & 2 \\ 6 & 8 & 2 \\ 4 & 0 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}8 & 2 \\ 0 & 2\end{aligned}|-3\cdot |\begin{aligned}6 & 2 \\ 4 & 2\end{aligned}|+2\cdot |\begin{aligned}6 & 8 \\ 4 & 0\end{aligned}| \\  & =(8\cdot 2-0\cdot 2)-3(6\cdot 2-4\cdot 2)+2(6\cdot 0-4\cdot 8) \\  & =16-12-64 \\  & =-60.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $a=⟨1,5,5⟩$, $b=⟨1,3,2⟩$ and $c=⟨2,0,3⟩.$ Find $a\cdot (b\times c).$

- $16$

- $-16$

- $4$

- $-25$

- $-21$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 5 & 5 \\ 1 & 3 & 2 \\ 2 & 0 & 3\end{aligned}| \\  & =1\cdot |\begin{aligned}3 & 2 \\ 0 & 3\end{aligned}|-5\cdot |\begin{aligned}1 & 2 \\ 2 & 3\end{aligned}|+5\cdot |\begin{aligned}1 & 3 \\ 2 & 0\end{aligned}| \\  & =(3\cdot 3-2\cdot 0)-5\cdot (1\cdot 3-2\cdot 2)+5\cdot (1\cdot 0-3\cdot 2) \\  & =9+5-30 \\  & =-16.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨1,5,6⟩$, $b=⟨2,3,6⟩$ and $c=⟨5,0,5⟩.$ Find $a\cdot (b\times c).$

- $-25$

- $20$

- $-5$

- $25$

- $-95$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 5 & 6 \\ 2 & 3 & 6 \\ 5 & 0 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}3 & 6 \\ 0 & 5\end{aligned}|-5\cdot |\begin{aligned}2 & 6 \\ 5 & 5\end{aligned}|+6\cdot |\begin{aligned}2 & 3 \\ 5 & 0\end{aligned}| \\  & =(3\cdot 5-6\cdot 0)-5\cdot (2\cdot 5-6\cdot 5)+6\cdot (2\cdot 0-3\cdot 5) \\  & =15+100-90 \\  & =25.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨1,2,1⟩$, $b=⟨4,1,4⟩$ and $c=⟨4,0,5⟩.$ Find $a\cdot (b\times c).$

- $-7$

- $-63$

- $7$

- $-17$

- $-3$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 1 \\ 4 & 1 & 4 \\ 4 & 0 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}1 & 4 \\ 0 & 5\end{aligned}|-2\cdot |\begin{aligned}4 & 4 \\ 4 & 5\end{aligned}|+1\cdot |\begin{aligned}4 & 1 \\ 4 & 0\end{aligned}| \\  & =(1\cdot 5-4\cdot 0)-2\cdot (4\cdot 5-4\cdot 4)+(4\cdot 0-1\cdot 4) \\  & =5-8-4 \\  & =-7.\end{aligned}
$$

## Original q-20054 (raw evidence, ineligible)

Let $a=⟨1,-1,2⟩$, $b=⟨2,0,3⟩$ and $c=⟨2,4,2⟩.$ Find $a\cdot (b\times c).$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 2 \\ 2 & 0 & 3 \\ 2 & 4 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 3 \\ 4 & 2\end{aligned}|-(-1)\cdot |\begin{aligned}2 & 3 \\ 2 & 2\end{aligned}|+2\cdot |\begin{aligned}2 & 0 \\ 2 & 4\end{aligned}| \\  & =(0\cdot 2-4\cdot 3)+(2\cdot 2-2\cdot 3)+2(2\cdot 4-2\cdot 0) \\  & =-12-2+16 \\  & =2.\end{aligned}
$$

Bank: -3, -4, 2, -12, 0; correct: 2

### Generated homogeneous raw replay (evidence-only) observed:q-20054

Let $a=⟨1,-1,2⟩$, $b=⟨4,0,6⟩$ and $c=⟨4,8,4⟩.$ Find $a\cdot (b\times c).$

- $8$

- $-48$

- $-16$

- $-12$

- $0$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 2 \\ 4 & 0 & 6 \\ 4 & 8 & 4\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 6 \\ 8 & 4\end{aligned}|-(-1)\cdot |\begin{aligned}4 & 6 \\ 4 & 4\end{aligned}|+2\cdot |\begin{aligned}4 & 0 \\ 4 & 8\end{aligned}| \\  & =(0\cdot 4-8\cdot 6)+(4\cdot 4-4\cdot 6)+2(4\cdot 8-4\cdot 0) \\  & =-48-8+64 \\  & =8.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $a=⟨1,-1,5⟩$, $b=⟨5,0,1⟩$ and $c=⟨3,2,2⟩.$ Find $a\cdot (b\times c).$

- $-55$

- $55$

- $1$

- $57$

- $48$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 5 \\ 5 & 0 & 1 \\ 3 & 2 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ 2 & 2\end{aligned}|-(-1)\cdot |\begin{aligned}5 & 1 \\ 3 & 2\end{aligned}|+5\cdot |\begin{aligned}5 & 0 \\ 3 & 2\end{aligned}| \\  & =(0\cdot 2-1\cdot 2)-(-1)\cdot (5\cdot 2-1\cdot 3)+5\cdot (5\cdot 2-0\cdot 3) \\  & =-2+7+50 \\  & =55.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨1,-1,5⟩$, $b=⟨6,0,2⟩$ and $c=⟨3,6,5⟩.$ Find $a\cdot (b\times c).$

- $-192$

- $0$

- $216$

- $192$

- $228$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 5 \\ 6 & 0 & 2 \\ 3 & 6 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 2 \\ 6 & 5\end{aligned}|-(-1)\cdot |\begin{aligned}6 & 2 \\ 3 & 5\end{aligned}|+5\cdot |\begin{aligned}6 & 0 \\ 3 & 6\end{aligned}| \\  & =(0\cdot 5-2\cdot 6)-(-1)\cdot (6\cdot 5-2\cdot 3)+5\cdot (6\cdot 6-0\cdot 3) \\  & =-12+24+180 \\  & =192.\end{aligned}
$$

## Original q-317312 (raw evidence, ineligible)

Let $a=⟨2,-1,3⟩$, $b=⟨0,4,1⟩$ and $c=⟨-2,1,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & -1 & 3 \\ 0 & 4 & 1 \\ -2 & 1 & 5\end{aligned}| \\  & =2\cdot |\begin{aligned}4 & 1 \\ 1 & 5\end{aligned}|\,-\,(-1)\cdot |\begin{aligned}0 & 1 \\ -2 & 5\end{aligned}|\,+\,3\cdot |\begin{aligned}0 & 4 \\ -2 & 1\end{aligned}| \\  & =2\,(4\cdot 5-1\cdot 1)\,-\,(-1)\,(0\cdot 5-1\cdot (-2))\,+\,3\,(0\cdot 1-4\cdot (-2)) \\  & =2\,(19)\,-\,(-1)\,(2)\,+\,3\,(8) \\  & =38+2+24 \\  & =64.\end{aligned}
$$

Bank: 64; correct: 64

### Generated homogeneous raw replay (evidence-only) observed:q-317312

Let $a=⟨2,-1,3⟩$, $b=⟨0,8,2⟩$ and $c=⟨-4,2,10⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $256$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & -1 & 3 \\ 0 & 8 & 2 \\ -4 & 2 & 10\end{aligned}| \\  & =2\cdot |\begin{aligned}8 & 2 \\ 2 & 10\end{aligned}|\,-\,(-1)\cdot |\begin{aligned}0 & 2 \\ -4 & 10\end{aligned}|\,+\,3\cdot |\begin{aligned}0 & 8 \\ -4 & 2\end{aligned}| \\  & =2\,(8\cdot 10-2\cdot 2)\,-\,(-1)\,(0\cdot 10-2\cdot (-4))\,+\,3\,(0\cdot 2-8\cdot (-4)) \\  & =2\,(76)\,-\,(-1)\,(8)\,+\,3\,(32) \\  & =152+8+96 \\  & =256.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨3,-1,5⟩$, $b=⟨0,5,1⟩$ and $c=⟨-3,2,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $102$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}3 & -1 & 5 \\ 0 & 5 & 1 \\ -3 & 2 & 2\end{aligned}| \\  & =3\cdot |\begin{aligned}5 & 1 \\ 2 & 2\end{aligned}|-(-1)\cdot |\begin{aligned}0 & 1 \\ -3 & 2\end{aligned}|+5\cdot |\begin{aligned}0 & 5 \\ -3 & 2\end{aligned}| \\  & =3\cdot (5\cdot 2-1\cdot 2)-(-1)\cdot (0\cdot 2-1\cdot (-3))+5\cdot (0\cdot 2-5\cdot (-3)) \\  & =3\cdot (8)-(-1)\cdot (3)+5\cdot (15) \\  & =24+3+75 \\  & =102.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,-1,5⟩$, $b=⟨0,6,2⟩$ and $c=⟨-3,6,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $114$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 5 \\ 0 & 6 & 2 \\ -3 & 6 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}6 & 2 \\ 6 & 5\end{aligned}|-(-1)\cdot |\begin{aligned}0 & 2 \\ -3 & 5\end{aligned}|+5\cdot |\begin{aligned}0 & 6 \\ -3 & 6\end{aligned}| \\  & =1\cdot (6\cdot 5-2\cdot 6)-(-1)\cdot (0\cdot 5-2\cdot (-3))+5\cdot (0\cdot 6-6\cdot (-3)) \\  & =1\cdot (18)-(-1)\cdot (6)+5\cdot (18) \\  & =18+6+90 \\  & =114.\end{aligned}
$$

## Original q-317315 (raw evidence, ineligible)

Let $a=⟨1,2,3⟩$, $b=⟨4,0,1⟩$ and $c=⟨-2,-1,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 3 \\ 4 & 0 & 1 \\ -2 & -1 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ -1 & 5\end{aligned}|\,-\,2\cdot |\begin{aligned}4 & 1 \\ -2 & 5\end{aligned}|\,+\,3\cdot |\begin{aligned}4 & 0 \\ -2 & -1\end{aligned}| \\  & =1\,(0\cdot 5-1\cdot (-1))\,-\,2\,(4\cdot 5-1\cdot (-2))\,+\,3\,(4\cdot (-1)-0\cdot (-2)) \\  & =1\,(1)\,-\,2\,(22)\,+\,3\,(-4) \\  & =1-44-12 \\  & =-55.\end{aligned}
$$

Bank: -55; correct: -55

### Generated homogeneous raw replay (evidence-only) observed:q-317315

Let $a=⟨1,2,3⟩$, $b=⟨8,0,2⟩$ and $c=⟨-4,-2,10⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-220$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 3 \\ 8 & 0 & 2 \\ -4 & -2 & 10\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 2 \\ -2 & 10\end{aligned}|\,-\,2\cdot |\begin{aligned}8 & 2 \\ -4 & 10\end{aligned}|\,+\,3\cdot |\begin{aligned}8 & 0 \\ -4 & -2\end{aligned}| \\  & =1\,(0\cdot 10-2\cdot (-2))\,-\,2\,(8\cdot 10-2\cdot (-4))\,+\,3\,(8\cdot (-2)-0\cdot (-4)) \\  & =1\,(4)\,-\,2\,(88)\,+\,3\,(-16) \\  & =4-176-48 \\  & =-220.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,3,5⟩$, $b=⟨5,0,1⟩$ and $c=⟨-3,-2,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-87$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 3 & 5 \\ 5 & 0 & 1 \\ -3 & -2 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ -2 & 2\end{aligned}|-3\cdot |\begin{aligned}5 & 1 \\ -3 & 2\end{aligned}|+5\cdot |\begin{aligned}5 & 0 \\ -3 & -2\end{aligned}| \\  & =1\cdot (0\cdot 2-1\cdot (-2))-3\cdot (5\cdot 2-1\cdot (-3))+5\cdot (5\cdot (-2)-0\cdot (-3)) \\  & =1\cdot (2)-3\cdot (13)+5\cdot (-10) \\  & =2-39-50 \\  & =-87.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,1,5⟩$, $b=⟨6,0,2⟩$ and $c=⟨-3,-6,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-204$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 1 & 5 \\ 6 & 0 & 2 \\ -3 & -6 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 2 \\ -6 & 5\end{aligned}|-1\cdot |\begin{aligned}6 & 2 \\ -3 & 5\end{aligned}|+5\cdot |\begin{aligned}6 & 0 \\ -3 & -6\end{aligned}| \\  & =1\cdot (0\cdot 5-2\cdot (-6))-1\cdot (6\cdot 5-2\cdot (-3))+5\cdot (6\cdot (-6)-0\cdot (-3)) \\  & =1\cdot (12)-1\cdot (36)+5\cdot (-36) \\  & =12-36-180 \\  & =-204.\end{aligned}
$$

## Original q-317316 (raw evidence, ineligible)

Let $a=⟨0,2,5⟩$, $b=⟨3,1,0⟩$ and $c=⟨4,-1,-2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 2 & 5 \\ 3 & 1 & 0 \\ 4 & -1 & -2\end{aligned}| \\  & =0\cdot |\begin{aligned}1 & 0 \\ -1 & -2\end{aligned}|\,-\,2\cdot |\begin{aligned}3 & 0 \\ 4 & -2\end{aligned}|\,+\,5\cdot |\begin{aligned}3 & 1 \\ 4 & -1\end{aligned}| \\  & =0\,(1\cdot (-2)-0\cdot (-1))\,-\,2\,(3\cdot (-2)-0\cdot 4)\,+\,5\,(3\cdot (-1)-1\cdot 4) \\  & =0(-2)\,-\,2\,(-6)\,+\,5\,(-7) \\  & =0+12-35 \\  & =-23.\end{aligned}
$$

Bank: -23; correct: -23

### Generated homogeneous raw replay (evidence-only) observed:q-317316

Let $a=⟨0,2,5⟩$, $b=⟨6,2,0⟩$ and $c=⟨8,-2,-4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-92$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 2 & 5 \\ 6 & 2 & 0 \\ 8 & -2 & -4\end{aligned}| \\  & =0\cdot |\begin{aligned}2 & 0 \\ -2 & -4\end{aligned}|\,-\,2\cdot |\begin{aligned}6 & 0 \\ 8 & -4\end{aligned}|\,+\,5\cdot |\begin{aligned}6 & 2 \\ 8 & -2\end{aligned}| \\  & =0\,(2\cdot (-4)-0\cdot (-2))\,-\,2\,(6\cdot (-4)-0\cdot 8)\,+\,5\,(6\cdot (-2)-2\cdot 8) \\  & =0(-8)\,-\,2\,(-24)\,+\,5\,(-28) \\  & =0+48-140 \\  & =-92.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨0,3,5⟩$, $b=⟨5,1,0⟩$ and $c=⟨3,-2,-2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-35$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 3 & 5 \\ 5 & 1 & 0 \\ 3 & -2 & -2\end{aligned}| \\  & =0\cdot |\begin{aligned}1 & 0 \\ -2 & -2\end{aligned}|-3\cdot |\begin{aligned}5 & 0 \\ 3 & -2\end{aligned}|+5\cdot |\begin{aligned}5 & 1 \\ 3 & -2\end{aligned}| \\  & =0\cdot (1\cdot (-2)-0\cdot (-2))-3\cdot (5\cdot (-2)-0\cdot 3)+5\cdot (5\cdot (-2)-1\cdot 3) \\  & =0\cdot (-2)-3\cdot (-10)+5\cdot (-13) \\  & =0+30-65 \\  & =-35.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨0,1,5⟩$, $b=⟨6,2,0⟩$ and $c=⟨3,-6,-5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-180$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 1 & 5 \\ 6 & 2 & 0 \\ 3 & -6 & -5\end{aligned}| \\  & =0\cdot |\begin{aligned}2 & 0 \\ -6 & -5\end{aligned}|-1\cdot |\begin{aligned}6 & 0 \\ 3 & -5\end{aligned}|+5\cdot |\begin{aligned}6 & 2 \\ 3 & -6\end{aligned}| \\  & =0\cdot (2\cdot (-5)-0\cdot (-6))-1\cdot (6\cdot (-5)-0\cdot 3)+5\cdot (6\cdot (-6)-2\cdot 3) \\  & =0\cdot (-10)-1\cdot (-30)+5\cdot (-42) \\  & =0+30-210 \\  & =-180.\end{aligned}
$$

## Original q-317317 (raw evidence, ineligible)

Let $a=⟨1,2,3⟩$, $b=⟨4,0,-2⟩$ and $c=⟨5,6,1⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 3 \\ 4 & 0 & -2 \\ 5 & 6 & 1\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & -2 \\ 6 & 1\end{aligned}|\,-\,2\cdot |\begin{aligned}4 & -2 \\ 5 & 1\end{aligned}|\,+\,3\cdot |\begin{aligned}4 & 0 \\ 5 & 6\end{aligned}| \\  & =1\,(0\cdot 1-(-2)\cdot 6)\,-\,2\,(4\cdot 1-(-2)\cdot 5)\,+\,3\,(4\cdot 6-0\cdot 5) \\  & =1\,(12)\,-\,2\,(14)\,+\,3\,(24) \\  & =12-28+72 \\  & =56.\end{aligned}
$$

Bank: 56; correct: 56

### Generated homogeneous raw replay (evidence-only) observed:q-317317

Let $a=⟨1,2,3⟩$, $b=⟨8,0,-4⟩$ and $c=⟨10,12,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $224$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 3 \\ 8 & 0 & -4 \\ 10 & 12 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & -4 \\ 12 & 2\end{aligned}|\,-\,2\cdot |\begin{aligned}8 & -4 \\ 10 & 2\end{aligned}|\,+\,3\cdot |\begin{aligned}8 & 0 \\ 10 & 12\end{aligned}| \\  & =1\,(0\cdot 2-(-4)\cdot 12)\,-\,2\,(8\cdot 2-(-4)\cdot 10)\,+\,3\,(8\cdot 12-0\cdot 10) \\  & =1\,(48)\,-\,2\,(56)\,+\,3\,(96) \\  & =48-112+288 \\  & =224.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,3,5⟩$, $b=⟨5,0,-1⟩$ and $c=⟨3,2,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $13$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 3 & 5 \\ 5 & 0 & -1 \\ 3 & 2 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & -1 \\ 2 & 2\end{aligned}|-3\cdot |\begin{aligned}5 & -1 \\ 3 & 2\end{aligned}|+5\cdot |\begin{aligned}5 & 0 \\ 3 & 2\end{aligned}| \\  & =1\cdot (0\cdot 2-(-1)\cdot 2)-3\cdot (5\cdot 2-(-1)\cdot 3)+5\cdot (5\cdot 2-0\cdot 3) \\  & =1\cdot (2)-3\cdot (13)+5\cdot (10) \\  & =2-39+50 \\  & =13.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,1,5⟩$, $b=⟨6,0,-2⟩$ and $c=⟨3,6,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $156$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 1 & 5 \\ 6 & 0 & -2 \\ 3 & 6 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & -2 \\ 6 & 5\end{aligned}|-1\cdot |\begin{aligned}6 & -2 \\ 3 & 5\end{aligned}|+5\cdot |\begin{aligned}6 & 0 \\ 3 & 6\end{aligned}| \\  & =1\cdot (0\cdot 5-(-2)\cdot 6)-1\cdot (6\cdot 5-(-2)\cdot 3)+5\cdot (6\cdot 6-0\cdot 3) \\  & =1\cdot (12)-1\cdot (36)+5\cdot (36) \\  & =12-36+180 \\  & =156.\end{aligned}
$$

## Original q-317319 (raw evidence, ineligible)

Let $a=⟨2,1,3⟩$, $b=⟨1,4,0⟩$ and $c=⟨6,-1,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & 1 & 3 \\ 1 & 4 & 0 \\ 6 & -1 & 2\end{aligned}| \\  & =2\cdot |\begin{aligned}4 & 0 \\ -1 & 2\end{aligned}|\,-\,1\cdot |\begin{aligned}1 & 0 \\ 6 & 2\end{aligned}|\,+\,3\cdot |\begin{aligned}1 & 4 \\ 6 & -1\end{aligned}| \\  & =2\,(4\cdot 2-0\cdot (-1))\,-\,1\,(1\cdot 2-0\cdot 6)\,+\,3\,(1\cdot (-1)-4\cdot 6) \\  & =2\,(8)\,-\,1\,(2)\,+\,3\,(-25) \\  & =16-2-75 \\  & =-61.\end{aligned}
$$

Bank: -61; correct: -61

### Generated homogeneous raw replay (evidence-only) observed:q-317319

Let $a=⟨2,1,3⟩$, $b=⟨2,8,0⟩$ and $c=⟨12,-2,4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-244$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & 1 & 3 \\ 2 & 8 & 0 \\ 12 & -2 & 4\end{aligned}| \\  & =2\cdot |\begin{aligned}8 & 0 \\ -2 & 4\end{aligned}|\,-\,1\cdot |\begin{aligned}2 & 0 \\ 12 & 4\end{aligned}|\,+\,3\cdot |\begin{aligned}2 & 8 \\ 12 & -2\end{aligned}| \\  & =2\,(8\cdot 4-0\cdot (-2))\,-\,1\,(2\cdot 4-0\cdot 12)\,+\,3\,(2\cdot (-2)-8\cdot 12) \\  & =2\,(32)\,-\,1\,(8)\,+\,3\,(-100) \\  & =64-8-300 \\  & =-244.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨3,1,5⟩$, $b=⟨5,1,0⟩$ and $c=⟨3,-2,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-69$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}3 & 1 & 5 \\ 5 & 1 & 0 \\ 3 & -2 & 2\end{aligned}| \\  & =3\cdot |\begin{aligned}1 & 0 \\ -2 & 2\end{aligned}|-1\cdot |\begin{aligned}5 & 0 \\ 3 & 2\end{aligned}|+5\cdot |\begin{aligned}5 & 1 \\ 3 & -2\end{aligned}| \\  & =3\cdot (1\cdot 2-0\cdot (-2))-1\cdot (5\cdot 2-0\cdot 3)+5\cdot (5\cdot (-2)-1\cdot 3) \\  & =3\cdot (2)-1\cdot (10)+5\cdot (-13) \\  & =6-10-65 \\  & =-69.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,1,5⟩$, $b=⟨6,2,0⟩$ and $c=⟨3,-6,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-230$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 1 & 5 \\ 6 & 2 & 0 \\ 3 & -6 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}2 & 0 \\ -6 & 5\end{aligned}|-1\cdot |\begin{aligned}6 & 0 \\ 3 & 5\end{aligned}|+5\cdot |\begin{aligned}6 & 2 \\ 3 & -6\end{aligned}| \\  & =1\cdot (2\cdot 5-0\cdot (-6))-1\cdot (6\cdot 5-0\cdot 3)+5\cdot (6\cdot (-6)-2\cdot 3) \\  & =1\cdot (10)-1\cdot (30)+5\cdot (-42) \\  & =10-30-210 \\  & =-230.\end{aligned}
$$

## Original q-317320 (raw evidence, ineligible)

Let $a=⟨1,0,2⟩$, $b=⟨3,1,0⟩$ and $c=⟨4,2,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 2 \\ 3 & 1 & 0 \\ 4 & 2 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}1 & 0 \\ 2 & 5\end{aligned}|\,-\,0\cdot |\begin{aligned}3 & 0 \\ 4 & 5\end{aligned}|\,+\,2\cdot |\begin{aligned}3 & 1 \\ 4 & 2\end{aligned}| \\  & =1\,(1\cdot 5-0\cdot 2)\,-\,0\,(3\cdot 5-0\cdot 4)\,+\,2\,(3\cdot 2-1\cdot 4) \\  & =1\,(5)\,-\,0\,(15)\,+\,2\,(2) \\  & =5+0+4 \\  & =9.\end{aligned}
$$

Bank: 9; correct: 9

### Generated homogeneous raw replay (evidence-only) observed:q-317320

Let $a=⟨1,0,2⟩$, $b=⟨6,2,0⟩$ and $c=⟨8,4,10⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $36$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 2 \\ 6 & 2 & 0 \\ 8 & 4 & 10\end{aligned}| \\  & =1\cdot |\begin{aligned}2 & 0 \\ 4 & 10\end{aligned}|\,-\,0\cdot |\begin{aligned}6 & 0 \\ 8 & 10\end{aligned}|\,+\,2\cdot |\begin{aligned}6 & 2 \\ 8 & 4\end{aligned}| \\  & =1\,(2\cdot 10-0\cdot 4)\,-\,0\,(6\cdot 10-0\cdot 8)\,+\,2\,(6\cdot 4-2\cdot 8) \\  & =1\,(20)\,-\,0\,(60)\,+\,2\,(8) \\  & =20+0+16 \\  & =36.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,0,3⟩$, $b=⟨5,5,0⟩$ and $c=⟨1,3,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $40$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 3 \\ 5 & 5 & 0 \\ 1 & 3 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}5 & 0 \\ 3 & 2\end{aligned}|-0\cdot |\begin{aligned}5 & 0 \\ 1 & 2\end{aligned}|+3\cdot |\begin{aligned}5 & 5 \\ 1 & 3\end{aligned}| \\  & =1\cdot (5\cdot 2-0\cdot 3)-0\cdot (5\cdot 2-0\cdot 1)+3\cdot (5\cdot 3-5\cdot 1) \\  & =1\cdot (10)-0\cdot (10)+3\cdot (10) \\  & =10+0+30 \\  & =40.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,0,1⟩$, $b=⟨5,6,0⟩$ and $c=⟨2,3,6⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $39$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 1 \\ 5 & 6 & 0 \\ 2 & 3 & 6\end{aligned}| \\  & =1\cdot |\begin{aligned}6 & 0 \\ 3 & 6\end{aligned}|-0\cdot |\begin{aligned}5 & 0 \\ 2 & 6\end{aligned}|+1\cdot |\begin{aligned}5 & 6 \\ 2 & 3\end{aligned}| \\  & =1\cdot (6\cdot 6-0\cdot 3)-0\cdot (5\cdot 6-0\cdot 2)+1\cdot (5\cdot 3-6\cdot 2) \\  & =1\cdot (36)-0\cdot (30)+1\cdot (3) \\  & =36+0+3 \\  & =39.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,0,4⟩$, $b=⟨1,3,0⟩$ and $c=⟨5,4,4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-32$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 4 \\ 1 & 3 & 0 \\ 5 & 4 & 4\end{aligned}| \\  & =1\cdot |\begin{aligned}3 & 0 \\ 4 & 4\end{aligned}|-0\cdot |\begin{aligned}1 & 0 \\ 5 & 4\end{aligned}|+4\cdot |\begin{aligned}1 & 3 \\ 5 & 4\end{aligned}| \\  & =1\cdot (3\cdot 4-0\cdot 4)-0\cdot (1\cdot 4-0\cdot 5)+4\cdot (1\cdot 4-3\cdot 5) \\  & =1\cdot (12)-0\cdot (4)+4\cdot (-11) \\  & =12+0-44 \\  & =-32.\end{aligned}
$$

## Original q-317322 (raw evidence, ineligible)

Let $a=⟨2,1,0⟩$, $b=⟨0,3,4⟩$ and $c=⟨5,2,1⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & 1 & 0 \\ 0 & 3 & 4 \\ 5 & 2 & 1\end{aligned}| \\  & =2\cdot |\begin{aligned}3 & 4 \\ 2 & 1\end{aligned}|\,-\,1\cdot |\begin{aligned}0 & 4 \\ 5 & 1\end{aligned}|\,+\,0\cdot |\begin{aligned}0 & 3 \\ 5 & 2\end{aligned}| \\  & =2\,(3\cdot 1-4\cdot 2)\,-\,1\,(0\cdot 1-4\cdot 5)\,+\,0\,(0\cdot 2-3\cdot 5) \\  & =2\,(-5)\,-\,1\,(-20)\,+\,0\,(-15) \\  & =-10+20+0 \\  & =10.\end{aligned}
$$

Bank: 10; correct: 10

### Generated homogeneous raw replay (evidence-only) observed:q-317322

Let $a=⟨2,1,0⟩$, $b=⟨0,6,8⟩$ and $c=⟨10,4,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $40$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}2 & 1 & 0 \\ 0 & 6 & 8 \\ 10 & 4 & 2\end{aligned}| \\  & =2\cdot |\begin{aligned}6 & 8 \\ 4 & 2\end{aligned}|\,-\,1\cdot |\begin{aligned}0 & 8 \\ 10 & 2\end{aligned}|\,+\,0\cdot |\begin{aligned}0 & 6 \\ 10 & 4\end{aligned}| \\  & =2\,(6\cdot 2-8\cdot 4)\,-\,1\,(0\cdot 2-8\cdot 10)\,+\,0\,(0\cdot 4-6\cdot 10) \\  & =2\,(-20)\,-\,1\,(-80)\,+\,0\,(-60) \\  & =-40+80+0 \\  & =40.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨3,1,0⟩$, $b=⟨0,5,5⟩$ and $c=⟨1,3,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-10$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}3 & 1 & 0 \\ 0 & 5 & 5 \\ 1 & 3 & 2\end{aligned}| \\  & =3\cdot |\begin{aligned}5 & 5 \\ 3 & 2\end{aligned}|-1\cdot |\begin{aligned}0 & 5 \\ 1 & 2\end{aligned}|+0\cdot |\begin{aligned}0 & 5 \\ 1 & 3\end{aligned}| \\  & =3\cdot (5\cdot 2-5\cdot 3)-1\cdot (0\cdot 2-5\cdot 1)+0\cdot (0\cdot 3-5\cdot 1) \\  & =3\cdot (-5)-1\cdot (-5)+0\cdot (-5) \\  & =-15+5+0 \\  & =-10.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,1,0⟩$, $b=⟨0,5,6⟩$ and $c=⟨2,3,6⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $24$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 1 & 0 \\ 0 & 5 & 6 \\ 2 & 3 & 6\end{aligned}| \\  & =1\cdot |\begin{aligned}5 & 6 \\ 3 & 6\end{aligned}|-1\cdot |\begin{aligned}0 & 6 \\ 2 & 6\end{aligned}|+0\cdot |\begin{aligned}0 & 5 \\ 2 & 3\end{aligned}| \\  & =1\cdot (5\cdot 6-6\cdot 3)-1\cdot (0\cdot 6-6\cdot 2)+0\cdot (0\cdot 3-5\cdot 2) \\  & =1\cdot (12)-1\cdot (-12)+0\cdot (-10) \\  & =12+12+0 \\  & =24.\end{aligned}
$$

## Original q-317325 (raw evidence, ineligible)

Let $a=⟨-1,-2,3⟩$, $b=⟨4,-1,-2⟩$ and $c=⟨1,2,-3⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -2 & 3 \\ 4 & -1 & -2 \\ 1 & 2 & -3\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-1 & -2 \\ 2 & -3\end{aligned}|\,-\,(-2)\cdot |\begin{aligned}4 & -2 \\ 1 & -3\end{aligned}|\,+\,3\cdot |\begin{aligned}4 & -1 \\ 1 & 2\end{aligned}| \\  & =(-1)\,((-1)(-3)-(-2)\cdot 2)\,-\,(-2)\,(4\cdot (-3)-(-2)\cdot 1)\,+\,3\,(4\cdot 2-(-1)\cdot 1) \\  & =(-1)\,(7)\,-\,(-2)\,(-10)\,+\,3\,(9) \\  & =-7-20+27 \\  & =0.\end{aligned}
$$

Bank: 0; correct: 0

### Generated homogeneous raw replay (evidence-only) observed:q-317325

Let $a=⟨-1,-2,3⟩$, $b=⟨8,-2,-4⟩$ and $c=⟨2,4,-6⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $0$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -2 & 3 \\ 8 & -2 & -4 \\ 2 & 4 & -6\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-2 & -4 \\ 4 & -6\end{aligned}|\,-\,(-2)\cdot |\begin{aligned}8 & -4 \\ 2 & -6\end{aligned}|\,+\,3\cdot |\begin{aligned}8 & -2 \\ 2 & 4\end{aligned}| \\  & =(-1)\,((-2)(-6)-(-4)\cdot 4)\,-\,(-2)\,(8\cdot (-6)-(-4)\cdot 2)\,+\,3\,(8\cdot 4-(-2)\cdot 2) \\  & =(-1)\,(28)\,-\,(-2)\,(-40)\,+\,3\,(36) \\  & =-28-80+108 \\  & =0.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,-3,5⟩$, $b=⟨5,-1,-3⟩$ and $c=⟨2,2,-3⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $24$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -3 & 5 \\ 5 & -1 & -3 \\ 2 & 2 & -3\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-1 & -3 \\ 2 & -3\end{aligned}|-(-3)\cdot |\begin{aligned}5 & -3 \\ 2 & -3\end{aligned}|+5\cdot |\begin{aligned}5 & -1 \\ 2 & 2\end{aligned}| \\  & =(-1)\cdot ((-1)\cdot (-3)-(-3)\cdot 2)-(-3)\cdot (5\cdot (-3)-(-3)\cdot 2)+5\cdot (5\cdot 2-(-1)\cdot 2) \\  & =(-1)\cdot (9)-(-3)\cdot (-9)+5\cdot (12) \\  & =-9-27+60 \\  & =24.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,-1,5⟩$, $b=⟨6,-2,-3⟩$ and $c=⟨6,5,-5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $173$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -1 & 5 \\ 6 & -2 & -3 \\ 6 & 5 & -5\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-2 & -3 \\ 5 & -5\end{aligned}|-(-1)\cdot |\begin{aligned}6 & -3 \\ 6 & -5\end{aligned}|+5\cdot |\begin{aligned}6 & -2 \\ 6 & 5\end{aligned}| \\  & =(-1)\cdot ((-2)\cdot (-5)-(-3)\cdot 5)-(-1)\cdot (6\cdot (-5)-(-3)\cdot 6)+5\cdot (6\cdot 5-(-2)\cdot 6) \\  & =(-1)\cdot (25)-(-1)\cdot (-12)+5\cdot (42) \\  & =-25-12+210 \\  & =173.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,-4,1⟩$, $b=⟨3,-5,-4⟩$ and $c=⟨4,3,-4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $13$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -4 & 1 \\ 3 & -5 & -4 \\ 4 & 3 & -4\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-5 & -4 \\ 3 & -4\end{aligned}|-(-4)\cdot |\begin{aligned}3 & -4 \\ 4 & -4\end{aligned}|+1\cdot |\begin{aligned}3 & -5 \\ 4 & 3\end{aligned}| \\  & =(-1)\cdot ((-5)\cdot (-4)-(-4)\cdot 3)-(-4)\cdot (3\cdot (-4)-(-4)\cdot 4)+1\cdot (3\cdot 3-(-5)\cdot 4) \\  & =(-1)\cdot (32)-(-4)\cdot (4)+1\cdot (29) \\  & =-32+16+29 \\  & =13.\end{aligned}
$$

## Original q-73461 (raw evidence, ineligible)

Let $p=⟨3,-2,1⟩$, $q=⟨2,-1,0⟩$ and $r=⟨1,-2,4⟩.$ Find $q\cdot (r\times p).$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}2 & -1 & 0 \\ 1 & -2 & 4 \\ 3 & -2 & 1\end{aligned}| \\  & =2\cdot |\begin{aligned}-2 & 4 \\ -2 & 1\end{aligned}|-(-1)\cdot |\begin{aligned}1 & 4 \\ 3 & 1\end{aligned}|+0\cdot |\begin{aligned}1 & -2 \\ 3 & -2\end{aligned}| \\  & =2((-2)\cdot 1-4\cdot (-2))+(1\cdot 1-4\cdot 3) \\  & =12-11 \\  & =1.\end{aligned}
$$

Bank: 1, 23, -23, 12, -11; correct: 1

### Generated homogeneous raw replay (evidence-only) observed:q-73461

Let $p=⟨6,-4,2⟩$, $q=⟨2,-1,0⟩$ and $r=⟨2,-4,8⟩.$ Find $q\cdot (r\times p).$

- $-92$

- $48$

- $92$

- $4$

- $-44$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}2 & -1 & 0 \\ 2 & -4 & 8 \\ 6 & -4 & 2\end{aligned}| \\  & =2\cdot |\begin{aligned}-4 & 8 \\ -4 & 2\end{aligned}|-(-1)\cdot |\begin{aligned}2 & 8 \\ 6 & 2\end{aligned}|+0\cdot |\begin{aligned}2 & -4 \\ 6 & -4\end{aligned}| \\  & =2((-4)\cdot 2-8\cdot (-4))+(2\cdot 2-8\cdot 6) \\  & =48-44 \\  & =4.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $p=⟨2,-2,3⟩$, $q=⟨5,-1,0⟩$ and $r=⟨5,-1,3⟩.$ Find $q\cdot (r\times p).$

- $-24$

- $24$

- $-14$

- $9$

- $15$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}5 & -1 & 0 \\ 5 & -1 & 3 \\ 2 & -2 & 3\end{aligned}| \\  & =5\cdot |\begin{aligned}-1 & 3 \\ -2 & 3\end{aligned}|-(-1)\cdot |\begin{aligned}5 & 3 \\ 2 & 3\end{aligned}|+0\cdot |\begin{aligned}5 & -1 \\ 2 & -2\end{aligned}| \\  & =5\cdot ((-1)\cdot 3-3\cdot (-2))-(-1)\cdot (5\cdot 3-3\cdot 2) \\  & =15+9 \\  & =24.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $p=⟨6,-5,5⟩$, $q=⟨5,-1,0⟩$ and $r=⟨6,-2,3⟩.$ Find $q\cdot (r\times p).$

- $-37$

- $-25$

- $-13$

- $37$

- $-77$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}5 & -1 & 0 \\ 6 & -2 & 3 \\ 6 & -5 & 5\end{aligned}| \\  & =5\cdot |\begin{aligned}-2 & 3 \\ -5 & 5\end{aligned}|-(-1)\cdot |\begin{aligned}6 & 3 \\ 6 & 5\end{aligned}|+0\cdot |\begin{aligned}6 & -2 \\ 6 & -5\end{aligned}| \\  & =5\cdot ((-2)\cdot 5-3\cdot (-5))-(-1)\cdot (6\cdot 5-3\cdot 6) \\  & =25+12 \\  & =37.\end{aligned}
$$

## Original q-73462 (raw evidence, ineligible)

Let $p=⟨3,1,2⟩$, $q=⟨1,-2,1⟩$ and $r=⟨4,1,-2⟩.$ Find $r\cdot (q\times p).$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}4 & 1 & -2 \\ 1 & -2 & 1 \\ 3 & 1 & 2\end{aligned}| \\  & =4\cdot |\begin{aligned}-2 & 1 \\ 1 & 2\end{aligned}|-1\cdot |\begin{aligned}1 & 1 \\ 3 & 2\end{aligned}|+(-2)\cdot |\begin{aligned}1 & -2 \\ 3 & 1\end{aligned}| \\  & =4((-2)\cdot 2-1\cdot 1)-(1\cdot 2-1\cdot 3)-2(1\cdot 1-(-2)\cdot 3) \\  & =-20+1-14 \\  & =-33.\end{aligned}
$$

Bank: -14, 10, -30, -33, -20; correct: -33

### Generated homogeneous raw replay (evidence-only) observed:q-73462

Let $p=⟨6,2,4⟩$, $q=⟨2,-4,2⟩$ and $r=⟨4,1,-2⟩.$ Find $r\cdot (q\times p).$

- $-120$

- $-132$

- $40$

- $-56$

- $-80$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}4 & 1 & -2 \\ 2 & -4 & 2 \\ 6 & 2 & 4\end{aligned}| \\  & =4\cdot |\begin{aligned}-4 & 2 \\ 2 & 4\end{aligned}|-1\cdot |\begin{aligned}2 & 2 \\ 6 & 4\end{aligned}|+(-2)\cdot |\begin{aligned}2 & -4 \\ 6 & 2\end{aligned}| \\  & =4((-4)\cdot 4-2\cdot 2)-(2\cdot 4-2\cdot 6)-2(2\cdot 2-(-4)\cdot 6) \\  & =-80+4-56 \\  & =-132.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $p=⟨2,3,1⟩$, $q=⟨1,-3,2⟩$ and $r=⟨5,1,-5⟩.$ Find $r\cdot (q\times p).$

- $87$

- $-87$

- $3$

- $-42$

- $-90$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}5 & 1 & -5 \\ 1 & -3 & 2 \\ 2 & 3 & 1\end{aligned}| \\  & =5\cdot |\begin{aligned}-3 & 2 \\ 3 & 1\end{aligned}|-1\cdot |\begin{aligned}1 & 2 \\ 2 & 1\end{aligned}|+(-5)\cdot |\begin{aligned}1 & -3 \\ 2 & 3\end{aligned}| \\  & =5\cdot ((-3)\cdot 1-2\cdot 3)-(1\cdot 1-2\cdot 2)+(-5)\cdot (1\cdot 3-(-3)\cdot 2) \\  & =-45+3-45 \\  & =-87.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $p=⟨5,5,3⟩$, $q=⟨2,-3,6⟩$ and $r=⟨5,1,-6⟩.$ Find $r\cdot (q\times p).$

- $321$

- $10$

- $69$

- $-321$

- $99$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}5 & 1 & -6 \\ 2 & -3 & 6 \\ 5 & 5 & 3\end{aligned}| \\  & =5\cdot |\begin{aligned}-3 & 6 \\ 5 & 3\end{aligned}|-1\cdot |\begin{aligned}2 & 6 \\ 5 & 3\end{aligned}|+(-6)\cdot |\begin{aligned}2 & -3 \\ 5 & 5\end{aligned}| \\  & =5\cdot ((-3)\cdot 3-6\cdot 5)-(2\cdot 3-6\cdot 5)+(-6)\cdot (2\cdot 5-(-3)\cdot 5) \\  & =-195+24-150 \\  & =-321.\end{aligned}
$$

## Original q-317321 (raw evidence, ineligible)

Let $a=⟨0,2,1⟩$, $b=⟨2,0,3⟩$ and $c=⟨1,4,5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 2 & 1 \\ 2 & 0 & 3 \\ 1 & 4 & 5\end{aligned}| \\  & =0\cdot |\begin{aligned}0 & 3 \\ 4 & 5\end{aligned}|\,-\,2\cdot |\begin{aligned}2 & 3 \\ 1 & 5\end{aligned}|\,+\,1\cdot |\begin{aligned}2 & 0 \\ 1 & 4\end{aligned}| \\  & =0\,(0\cdot 5-3\cdot 4)\,-\,2\,(2\cdot 5-3\cdot 1)\,+\,1\,(2\cdot 4-0\cdot 1) \\  & =0(-12)\,-\,2\,(7)\,+\,1\,(8) \\  & =0-14+8 \\  & =-6.\end{aligned}
$$

Bank: -6; correct: -6

### Generated homogeneous raw replay (evidence-only) observed:q-317321

Let $a=⟨0,2,1⟩$, $b=⟨4,0,6⟩$ and $c=⟨2,8,10⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-24$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 2 & 1 \\ 4 & 0 & 6 \\ 2 & 8 & 10\end{aligned}| \\  & =0\cdot |\begin{aligned}0 & 6 \\ 8 & 10\end{aligned}|\,-\,2\cdot |\begin{aligned}4 & 6 \\ 2 & 10\end{aligned}|\,+\,1\cdot |\begin{aligned}4 & 0 \\ 2 & 8\end{aligned}| \\  & =0\,(0\cdot 10-6\cdot 8)\,-\,2\,(4\cdot 10-6\cdot 2)\,+\,1\,(4\cdot 8-0\cdot 2) \\  & =0(-48)\,-\,2\,(28)\,+\,1\,(32) \\  & =0-56+32 \\  & =-24.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨0,3,1⟩$, $b=⟨5,0,5⟩$ and $c=⟨1,3,2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $0$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 3 & 1 \\ 5 & 0 & 5 \\ 1 & 3 & 2\end{aligned}| \\  & =0\cdot |\begin{aligned}0 & 5 \\ 3 & 2\end{aligned}|-3\cdot |\begin{aligned}5 & 5 \\ 1 & 2\end{aligned}|+1\cdot |\begin{aligned}5 & 0 \\ 1 & 3\end{aligned}| \\  & =0\cdot (0\cdot 2-5\cdot 3)-3\cdot (5\cdot 2-5\cdot 1)+1\cdot (5\cdot 3-0\cdot 1) \\  & =0\cdot (-15)-3\cdot (5)+1\cdot (15) \\  & =0-15+15 \\  & =0.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨0,1,1⟩$, $b=⟨5,0,6⟩$ and $c=⟨2,3,6⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-3$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}0 & 1 & 1 \\ 5 & 0 & 6 \\ 2 & 3 & 6\end{aligned}| \\  & =0\cdot |\begin{aligned}0 & 6 \\ 3 & 6\end{aligned}|-1\cdot |\begin{aligned}5 & 6 \\ 2 & 6\end{aligned}|+1\cdot |\begin{aligned}5 & 0 \\ 2 & 3\end{aligned}| \\  & =0\cdot (0\cdot 6-6\cdot 3)-1\cdot (5\cdot 6-6\cdot 2)+1\cdot (5\cdot 3-0\cdot 2) \\  & =0\cdot (-18)-1\cdot (18)+1\cdot (15) \\  & =0-18+15 \\  & =-3.\end{aligned}
$$

## Original q-275350 (raw evidence, ineligible)

Let $r=⟨-4,-1,2⟩$, $q=⟨-2,3,1⟩$ and $p=⟨5,-2,-1⟩.$ Find $r\cdot (q\times p)$ using a determinant.

$r\cdot (q\times p)=$

$-21$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}-4 & -1 & 2 \\ -2 & 3 & 1 \\ 5 & -2 & -1\end{aligned}| \\  & =(-4)\cdot |\begin{aligned}3 & 1 \\ -2 & -1\end{aligned}|-(-1)\cdot |\begin{aligned}-2 & 1 \\ 5 & -1\end{aligned}|+2\cdot |\begin{aligned}-2 & 3 \\ 5 & -2\end{aligned}| \\  & =(-4)(3\cdot (-1)-(-2)\cdot 1)+((-2)\cdot (-1)-5\cdot 1)+2((-2)\cdot (-2)-5\cdot 3) \\  & =(-4)(-3+2)+(2-5)+2(4-15) \\  & =4-3-22 \\  & =-21.\end{aligned}
$$

Bank: -21; correct: -21

### Generated homogeneous raw replay (evidence-only) observed:q-275350

Let $r=⟨-4,-1,2⟩$, $q=⟨-4,6,2⟩$ and $p=⟨10,-4,-2⟩.$ Find $r\cdot (q\times p)$ using a determinant.

$r\cdot (q\times p)=$

$-84$

- $-84$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}-4 & -1 & 2 \\ -4 & 6 & 2 \\ 10 & -4 & -2\end{aligned}| \\  & =(-4)\cdot |\begin{aligned}6 & 2 \\ -4 & -2\end{aligned}|-(-1)\cdot |\begin{aligned}-4 & 2 \\ 10 & -2\end{aligned}|+2\cdot |\begin{aligned}-4 & 6 \\ 10 & -4\end{aligned}| \\  & =(-4)(6\cdot (-2)-(-4)\cdot 2)+((-4)\cdot (-2)-10\cdot 2)+2((-4)\cdot (-4)-10\cdot 6) \\  & =(-4)(-12+8)+(8-20)+2(16-60) \\  & =16-12-88 \\  & =-84.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $r=⟨-3,-1,5⟩$, $q=⟨-5,1,3⟩$ and $p=⟨2,-2,-3⟩.$ Find $r\cdot (q\times p)$ using a determinant.

$r\cdot (q\times p)=$
{{field-1}}

- $40$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}-3 & -1 & 5 \\ -5 & 1 & 3 \\ 2 & -2 & -3\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}1 & 3 \\ -2 & -3\end{aligned}|-(-1)\cdot |\begin{aligned}-5 & 3 \\ 2 & -3\end{aligned}|+5\cdot |\begin{aligned}-5 & 1 \\ 2 & -2\end{aligned}| \\  & =(-3)\cdot (1\cdot (-3)-3\cdot (-2))-(-1)\cdot ((-5)\cdot (-3)-3\cdot 2)+5\cdot ((-5)\cdot (-2)-1\cdot 2) \\  & =(-3)\cdot (-3+6)-(-1)\cdot (15-6)+5\cdot (10-2) \\  & =-9+9+40 \\  & =40.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $r=⟨-1,-1,5⟩$, $q=⟨-6,2,3⟩$ and $p=⟨6,-5,-5⟩.$ Find $r\cdot (q\times p)$ using a determinant.

$r\cdot (q\times p)=$
{{field-1}}

- $97$

Remember that the scalar triple product $r\cdot (q\times p)$ is just the determinant of the matrix whose rows are given by $r,$ $q,$ and $p.$

So, we have

$$
\begin{aligned}r\cdot (q\times p) & =|\begin{aligned}-1 & -1 & 5 \\ -6 & 2 & 3 \\ 6 & -5 & -5\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}2 & 3 \\ -5 & -5\end{aligned}|-(-1)\cdot |\begin{aligned}-6 & 3 \\ 6 & -5\end{aligned}|+5\cdot |\begin{aligned}-6 & 2 \\ 6 & -5\end{aligned}| \\  & =(-1)\cdot (2\cdot (-5)-3\cdot (-5))-(-1)\cdot ((-6)\cdot (-5)-3\cdot 6)+5\cdot ((-6)\cdot (-5)-2\cdot 6) \\  & =(-1)\cdot (-10+15)-(-1)\cdot (30-18)+5\cdot (30-12) \\  & =-5+12+90 \\  & =97.\end{aligned}
$$

## Original q-20053 (raw evidence, ineligible)

Let $a=⟨-2,2,-3⟩$, $b=⟨2,-1,2⟩$ and $c=⟨-2,1,1⟩.$ Find $a\cdot (b\times c).$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 2 & -3 \\ 2 & -1 & 2 \\ -2 & 1 & 1\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}-1 & 2 \\ 1 & 1\end{aligned}|-2\cdot |\begin{aligned}2 & 2 \\ -2 & 1\end{aligned}|+(-3)\cdot |\begin{aligned}2 & -1 \\ -2 & 1\end{aligned}| \\  & =-2((-1)\cdot 1-1\cdot 2)-2(2\cdot 1-(-2)\cdot 2)-3(2\cdot 1-(-2)\cdot (-1)) \\  & =6-12+0 \\  & =-6.\end{aligned}
$$

Bank: -6, 8, -10, 6, -4; correct: -6

### Generated homogeneous raw replay (evidence-only) observed:q-20053

Let $a=⟨-2,2,-3⟩$, $b=⟨4,-2,4⟩$ and $c=⟨-4,2,2⟩.$ Find $a\cdot (b\times c).$

- $-40$

- $24$

- $32$

- $-24$

- $-16$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 2 & -3 \\ 4 & -2 & 4 \\ -4 & 2 & 2\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}-2 & 4 \\ 2 & 2\end{aligned}|-2\cdot |\begin{aligned}4 & 4 \\ -4 & 2\end{aligned}|+(-3)\cdot |\begin{aligned}4 & -2 \\ -4 & 2\end{aligned}| \\  & =-2((-2)\cdot 2-2\cdot 4)-2(4\cdot 2-(-4)\cdot 4)-3(4\cdot 2-(-4)\cdot (-2)) \\  & =24-48+0 \\  & =-24.\end{aligned}
$$

### Generated authored bank, independent coordinates omit_terms

Let $a=⟨-3,3,-1⟩$, $b=⟨3,-2,2⟩$ and $c=⟨-3,1,2⟩.$ Find $a\cdot (b\times c).$

- $15$

- $-15$

- $-21$

- $-33$

- $21$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-3 & 3 & -1 \\ 3 & -2 & 2 \\ -3 & 1 & 2\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}-2 & 2 \\ 1 & 2\end{aligned}|-3\cdot |\begin{aligned}3 & 2 \\ -3 & 2\end{aligned}|+(-1)\cdot |\begin{aligned}3 & -2 \\ -3 & 1\end{aligned}| \\  & =(-3)\cdot ((-2)\cdot 2-2\cdot 1)-3\cdot (3\cdot 2-2\cdot (-3))+(-1)\cdot (3\cdot 1-(-2)\cdot (-3)) \\  & =18-36+3 \\  & =-15.\end{aligned}
$$

### Generated authored bank, independent coordinates cofactor_signs

Let $a=⟨-3,3,-3⟩$, $b=⟨5,-2,6⟩$ and $c=⟨-6,3,2⟩.$ Find $a\cdot (b\times c).$

- $81$

- $-65$

- $-213$

- $-81$

- $-45$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-3 & 3 & -3 \\ 5 & -2 & 6 \\ -6 & 3 & 2\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}-2 & 6 \\ 3 & 2\end{aligned}|-3\cdot |\begin{aligned}5 & 6 \\ -6 & 2\end{aligned}|+(-3)\cdot |\begin{aligned}5 & -2 \\ -6 & 3\end{aligned}| \\  & =(-3)\cdot ((-2)\cdot 2-6\cdot 3)-3\cdot (5\cdot 2-6\cdot (-6))+(-3)\cdot (5\cdot 3-(-2)\cdot (-6)) \\  & =66-138-9 \\  & =-81.\end{aligned}
$$

## Original q-317318 (raw evidence, ineligible)

Let $a=⟨-1,2,4⟩$, $b=⟨0,3,1⟩$ and $c=⟨2,5,0⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$

$-15$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & 2 & 4 \\ 0 & 3 & 1 \\ 2 & 5 & 0\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}3 & 1 \\ 5 & 0\end{aligned}|\,-\,2\cdot |\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|\,+\,4\cdot |\begin{aligned}0 & 3 \\ 2 & 5\end{aligned}| \\  & =(-1)\,(3\cdot 0-1\cdot 5)\,-\,2\,(0\cdot 0-1\cdot 2)\,+\,4\,(0\cdot 5-3\cdot 2) \\  & =(-1)\,(-5)\,-\,2\,(-2)\,+\,4\,(-6) \\  & =5+4-24 \\  & =-15.\end{aligned}
$$

Bank: -15; correct: -15

### Generated homogeneous raw replay (evidence-only) observed:q-317318

Let $a=⟨-1,2,4⟩$, $b=⟨0,6,2⟩$ and $c=⟨4,10,0⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$

$-60$

- $-60$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & 2 & 4 \\ 0 & 6 & 2 \\ 4 & 10 & 0\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}6 & 2 \\ 10 & 0\end{aligned}|\,-\,2\cdot |\begin{aligned}0 & 2 \\ 4 & 0\end{aligned}|\,+\,4\cdot |\begin{aligned}0 & 6 \\ 4 & 10\end{aligned}| \\  & =(-1)\,(6\cdot 0-2\cdot 10)\,-\,2\,(0\cdot 0-2\cdot 4)\,+\,4\,(0\cdot 10-6\cdot 4) \\  & =(-1)\,(-20)\,-\,2\,(-8)\,+\,4\,(-24) \\  & =20+16-96 \\  & =-60.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,3,5⟩$, $b=⟨0,5,1⟩$ and $c=⟨3,2,0⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-64$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & 3 & 5 \\ 0 & 5 & 1 \\ 3 & 2 & 0\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}5 & 1 \\ 2 & 0\end{aligned}|-3\cdot |\begin{aligned}0 & 1 \\ 3 & 0\end{aligned}|+5\cdot |\begin{aligned}0 & 5 \\ 3 & 2\end{aligned}| \\  & =(-1)\cdot (5\cdot 0-1\cdot 2)-3\cdot (0\cdot 0-1\cdot 3)+5\cdot (0\cdot 2-5\cdot 3) \\  & =(-1)\cdot (-2)-3\cdot (-3)+5\cdot (-15) \\  & =2+9-75 \\  & =-64.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,1,5⟩$, $b=⟨0,6,2⟩$ and $c=⟨3,6,0⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-72$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & 1 & 5 \\ 0 & 6 & 2 \\ 3 & 6 & 0\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}6 & 2 \\ 6 & 0\end{aligned}|-1\cdot |\begin{aligned}0 & 2 \\ 3 & 0\end{aligned}|+5\cdot |\begin{aligned}0 & 6 \\ 3 & 6\end{aligned}| \\  & =(-1)\cdot (6\cdot 0-2\cdot 6)-1\cdot (0\cdot 0-2\cdot 3)+5\cdot (0\cdot 6-6\cdot 3) \\  & =(-1)\cdot (-12)-1\cdot (-6)+5\cdot (-18) \\  & =12+6-90 \\  & =-72.\end{aligned}
$$

## Original q-317313 (raw evidence, ineligible)

Let $a=⟨1,-3,0⟩$, $b=⟨-2,2,0⟩$ and $c=⟨2,0,-4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -3 & 0 \\ -2 & 2 & 0 \\ 2 & 0 & -4\end{aligned}| \\  & =1\cdot |\begin{aligned}2 & 0 \\ 0 & -4\end{aligned}|\,-\,(-3)\cdot |\begin{aligned}-2 & 0 \\ 2 & -4\end{aligned}|\,+\,0\cdot |\begin{aligned}-2 & 2 \\ 2 & 0\end{aligned}| \\  & =1\,(2\cdot (-4)-0\cdot 0)\,-\,(-3)\,((-2)\cdot (-4)-0\cdot 2)\,+\,0\,((-2)\cdot 0-2\cdot 2) \\  & =1\,(-8)\,-\,(-3)\,(8)\,+\,0\,(-4) \\  & =-8+24+0 \\  & =16.\end{aligned}
$$

Bank: 16; correct: 16

### Generated homogeneous raw replay (evidence-only) observed:q-317313

Let $a=⟨1,-3,0⟩$, $b=⟨-4,4,0⟩$ and $c=⟨4,0,-8⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $64$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -3 & 0 \\ -4 & 4 & 0 \\ 4 & 0 & -8\end{aligned}| \\  & =1\cdot |\begin{aligned}4 & 0 \\ 0 & -8\end{aligned}|\,-\,(-3)\cdot |\begin{aligned}-4 & 0 \\ 4 & -8\end{aligned}|\,+\,0\cdot |\begin{aligned}-4 & 4 \\ 4 & 0\end{aligned}| \\  & =1\,(4\cdot (-8)-0\cdot 0)\,-\,(-3)\,((-4)\cdot (-8)-0\cdot 4)\,+\,0\,((-4)\cdot 0-4\cdot 4) \\  & =1\,(-32)\,-\,(-3)\,(32)\,+\,0\,(-16) \\  & =-32+96+0 \\  & =64.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,-3,0⟩$, $b=⟨-5,5,0⟩$ and $c=⟨1,0,-3⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $30$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -3 & 0 \\ -5 & 5 & 0 \\ 1 & 0 & -3\end{aligned}| \\  & =1\cdot |\begin{aligned}5 & 0 \\ 0 & -3\end{aligned}|-(-3)\cdot |\begin{aligned}-5 & 0 \\ 1 & -3\end{aligned}|+0\cdot |\begin{aligned}-5 & 5 \\ 1 & 0\end{aligned}| \\  & =1\cdot (5\cdot (-3)-0\cdot 0)-(-3)\cdot ((-5)\cdot (-3)-0\cdot 1)+0\cdot ((-5)\cdot 0-5\cdot 1) \\  & =1\cdot (-15)-(-3)\cdot (15)+0\cdot (-5) \\  & =-15+45+0 \\  & =30.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨1,-1,0⟩$, $b=⟨-5,6,0⟩$ and $c=⟨2,0,-3⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-3$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & -1 & 0 \\ -5 & 6 & 0 \\ 2 & 0 & -3\end{aligned}| \\  & =1\cdot |\begin{aligned}6 & 0 \\ 0 & -3\end{aligned}|-(-1)\cdot |\begin{aligned}-5 & 0 \\ 2 & -3\end{aligned}|+0\cdot |\begin{aligned}-5 & 6 \\ 2 & 0\end{aligned}| \\  & =1\cdot (6\cdot (-3)-0\cdot 0)-(-1)\cdot ((-5)\cdot (-3)-0\cdot 2)+0\cdot ((-5)\cdot 0-6\cdot 2) \\  & =1\cdot (-18)-(-1)\cdot (15)+0\cdot (-12) \\  & =-18+15+0 \\  & =-3.\end{aligned}
$$

## Original q-317326 (raw evidence, ineligible)

Let $a=⟨-2,0,-1⟩$, $b=⟨-3,-1,4⟩$ and $c=⟨5,-2,-2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 0 & -1 \\ -3 & -1 & 4 \\ 5 & -2 & -2\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}-1 & 4 \\ -2 & -2\end{aligned}|\,-\,0\cdot |\begin{aligned}-3 & 4 \\ 5 & -2\end{aligned}|\,+\,(-1)\cdot |\begin{aligned}-3 & -1 \\ 5 & -2\end{aligned}| \\  & =(-2)\,((-1)(-2)-4\cdot (-2))\,-\,0\,((-3)\cdot (-2)-4\cdot 5)\,+\,(-1)\,((-3)\cdot (-2)-(-1)\cdot 5) \\  & =(-2)\,(10)\,-\,0\,(-14)\,+\,(-1)\,(11) \\  & =-20+0-11 \\  & =-31.\end{aligned}
$$

Bank: -31; correct: -31

### Generated homogeneous raw replay (evidence-only) observed:q-317326

Let $a=⟨-2,0,-1⟩$, $b=⟨-6,-2,8⟩$ and $c=⟨10,-4,-4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-124$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-2 & 0 & -1 \\ -6 & -2 & 8 \\ 10 & -4 & -4\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}-2 & 8 \\ -4 & -4\end{aligned}|\,-\,0\cdot |\begin{aligned}-6 & 8 \\ 10 & -4\end{aligned}|\,+\,(-1)\cdot |\begin{aligned}-6 & -2 \\ 10 & -4\end{aligned}| \\  & =(-2)\,((-2)(-4)-8\cdot (-4))\,-\,0\,((-6)\cdot (-4)-8\cdot 10)\,+\,(-1)\,((-6)\cdot (-4)-(-2)\cdot 10) \\  & =(-2)\,(40)\,-\,0\,(-56)\,+\,(-1)\,(44) \\  & =-80+0-44 \\  & =-124.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-3,0,-1⟩$, $b=⟨-5,-5,1⟩$ and $c=⟨3,-2,-2⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-61$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-3 & 0 & -1 \\ -5 & -5 & 1 \\ 3 & -2 & -2\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}-5 & 1 \\ -2 & -2\end{aligned}|-0\cdot |\begin{aligned}-5 & 1 \\ 3 & -2\end{aligned}|+(-1)\cdot |\begin{aligned}-5 & -5 \\ 3 & -2\end{aligned}| \\  & =(-3)\cdot ((-5)\cdot (-2)-1\cdot (-2))-0\cdot ((-5)\cdot (-2)-1\cdot 3)+(-1)\cdot ((-5)\cdot (-2)-(-5)\cdot 3) \\  & =(-3)\cdot (12)-0\cdot (7)+(-1)\cdot (25) \\  & =-36+0-25 \\  & =-61.\end{aligned}
$$

### Generated authored bank, independent coordinates blank

Let $a=⟨-1,0,-1⟩$, $b=⟨-5,-6,2⟩$ and $c=⟨3,-6,-5⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-90$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & 0 & -1 \\ -5 & -6 & 2 \\ 3 & -6 & -5\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-6 & 2 \\ -6 & -5\end{aligned}|-0\cdot |\begin{aligned}-5 & 2 \\ 3 & -5\end{aligned}|+(-1)\cdot |\begin{aligned}-5 & -6 \\ 3 & -6\end{aligned}| \\  & =(-1)\cdot ((-6)\cdot (-5)-2\cdot (-6))-0\cdot ((-5)\cdot (-5)-2\cdot 3)+(-1)\cdot ((-5)\cdot (-6)-(-6)\cdot 3) \\  & =(-1)\cdot (42)-0\cdot (19)+(-1)\cdot (48) \\  & =-42+0-48 \\  & =-90.\end{aligned}
$$

## Generated easy level preview (observed scope, authored bank)

Let $a=⟨1,0,4⟩$, $b=⟨1,3,0⟩$ and $c=⟨5,4,4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $-32$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 0 & 4 \\ 1 & 3 & 0 \\ 5 & 4 & 4\end{aligned}| \\  & =1\cdot |\begin{aligned}3 & 0 \\ 4 & 4\end{aligned}|-0\cdot |\begin{aligned}1 & 0 \\ 5 & 4\end{aligned}|+4\cdot |\begin{aligned}1 & 3 \\ 5 & 4\end{aligned}| \\  & =1\cdot (3\cdot 4-0\cdot 4)-0\cdot (1\cdot 4-0\cdot 5)+4\cdot (1\cdot 4-3\cdot 5) \\  & =1\cdot (12)-0\cdot (4)+4\cdot (-11) \\  & =12+0-44 \\  & =-32.\end{aligned}
$$

## Generated easy level preview (observed scope, authored bank)

Let $a=⟨1,2,1⟩$, $b=⟨4,1,4⟩$ and $c=⟨4,0,5⟩.$ Find $a\cdot (b\times c).$

- $-7$

- $-63$

- $7$

- $-17$

- $-3$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}1 & 2 & 1 \\ 4 & 1 & 4 \\ 4 & 0 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}1 & 4 \\ 0 & 5\end{aligned}|-2\cdot |\begin{aligned}4 & 4 \\ 4 & 5\end{aligned}|+1\cdot |\begin{aligned}4 & 1 \\ 4 & 0\end{aligned}| \\  & =(1\cdot 5-4\cdot 0)-2\cdot (4\cdot 5-4\cdot 4)+(4\cdot 0-1\cdot 4) \\  & =5-8-4 \\  & =-7.\end{aligned}
$$

## Generated moderate level preview (observed scope, authored bank)

Let $a=⟨-1,-4,1⟩$, $b=⟨3,-5,-4⟩$ and $c=⟨4,3,-4⟩.$ Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $13$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-1 & -4 & 1 \\ 3 & -5 & -4 \\ 4 & 3 & -4\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}-5 & -4 \\ 3 & -4\end{aligned}|-(-4)\cdot |\begin{aligned}3 & -4 \\ 4 & -4\end{aligned}|+1\cdot |\begin{aligned}3 & -5 \\ 4 & 3\end{aligned}| \\  & =(-1)\cdot ((-5)\cdot (-4)-(-4)\cdot 3)-(-4)\cdot (3\cdot (-4)-(-4)\cdot 4)+1\cdot (3\cdot 3-(-5)\cdot 4) \\  & =(-1)\cdot (32)-(-4)\cdot (4)+1\cdot (29) \\  & =-32+16+29 \\  & =13.\end{aligned}
$$

## Generated moderate level preview (observed scope, authored bank)

Let $p=⟨4,4,5⟩,$ $q=⟨1,2,-1⟩$ and $r=⟨4,0,1⟩.$ Find $q\cdot (r\times p).$

- $-52$

- $-60$

- $52$

- $-44$

- $-4$

Remember that the scalar triple product $q\cdot (r\times p)$ is just the determinant of the matrix whose rows are given by $q,$ $r,$ and $p.$

So, we have

$$
\begin{aligned}q\cdot (r\times p) & =|\begin{aligned}1 & 2 & -1 \\ 4 & 0 & 1 \\ 4 & 4 & 5\end{aligned}| \\  & =1\cdot |\begin{aligned}0 & 1 \\ 4 & 5\end{aligned}|-2\cdot |\begin{aligned}4 & 1 \\ 4 & 5\end{aligned}|+(-1)\cdot |\begin{aligned}4 & 0 \\ 4 & 4\end{aligned}| \\  & =(0\cdot 5-1\cdot 4)-2\cdot (4\cdot 5-1\cdot 4)+(-1)\cdot (4\cdot 4-0\cdot 4) \\  & =-4-32-16 \\  & =-52.\end{aligned}
$$

## Generated hard level preview (authored missing-level scope)

Let $a=⟨-5,5,5⟩$, $b=⟨6,-6,-4⟩$, $c=⟨-2,6,-4⟩$. Find $a\cdot (b\times c)$ using a determinant.

$a\cdot (b\times c)=$
{{field-1}}

- $40$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-5 & 5 & 5 \\ 6 & -6 & -4 \\ -2 & 6 & -4\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}-6 & -4 \\ 6 & -4\end{aligned}|-5\cdot |\begin{aligned}6 & -4 \\ -2 & -4\end{aligned}|+5\cdot |\begin{aligned}6 & -6 \\ -2 & 6\end{aligned}| \\  & =(-5)\cdot ((-6)\cdot (-4)-(-4)\cdot 6)-5\cdot (6\cdot (-4)-(-4)\cdot (-2))+5\cdot (6\cdot 6-(-6)\cdot (-2)) \\  & =(-5)\cdot (48)-5\cdot (-32)+5\cdot (24) \\  & =-240+160+120 \\  & =40.\end{aligned}
$$

## Generated hard level preview (authored missing-level scope)

Let $a=⟨-5,5,4⟩$, $b=⟨-5,-5,6⟩$, $c=⟨-5,3,-4⟩$. Find $a\cdot (b\times c)$ using a determinant.

- $-420$

- $-88$

- $420$

- $-410$

- $-170$

Remember that the scalar triple product $a\cdot (b\times c)$ is just the determinant of the matrix whose rows are given by $a,$ $b,$ and $c.$

So, we have

$$
\begin{aligned}a\cdot (b\times c) & =|\begin{aligned}-5 & 5 & 4 \\ -5 & -5 & 6 \\ -5 & 3 & -4\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}-5 & 6 \\ 3 & -4\end{aligned}|-5\cdot |\begin{aligned}-5 & 6 \\ -5 & -4\end{aligned}|+4\cdot |\begin{aligned}-5 & -5 \\ -5 & 3\end{aligned}| \\  & =(-5)\cdot ((-5)\cdot (-4)-6\cdot 3)-5\cdot ((-5)\cdot (-4)-6\cdot (-5))+4\cdot ((-5)\cdot 3-(-5)\cdot (-5)) \\  & =(-5)\cdot (2)-5\cdot (50)+4\cdot (-40) \\  & =-10-250-160 \\  & =-420.\end{aligned}
$$
