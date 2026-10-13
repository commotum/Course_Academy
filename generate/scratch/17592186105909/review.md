# Originals and generated variants

Raw preserves one known erroneous basis stage and missing metadata; normal replay corrects/infer/authors them. Source scaling banks are evidence only.

## Original q-128472

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(9, 6, 1)$, $B(9, 7, 2)$, $C(7, 5, 2)$, and $D(7, 8, 3)$.

- $10$
- $2$
- $12$
- $4$
- $8$

Source has no worked solution.

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(9, 6, 1)$, $B(9, 7, 2)$, $C(7, 5, 2)$, and $D(7, 8, 3)$.

- $10$
- $2$
- $12$
- $4$ (correct)
- $8$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(9i+7j+2k)-(9i+6j+k) \\  & =j+k \\  & =⟨0,1,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(7i+5j+2k)-(9i+6j+k) \\  & =-2i-j+k \\  & =⟨-2,-1,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(7i+8j+3k)-(9i+6j+k) \\  & =-2i+2j+2k \\  & =⟨-2,2,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}0 & 1 & 1 \\ -2 & -1 & 1 \\ -2 & 2 & 2\end{aligned}| \\  & =0\cdot |\begin{aligned}-1 & 1 \\ 2 & 2\end{aligned}|-1\cdot |\begin{aligned}-2 & 1 \\ -2 & 2\end{aligned}|+1\cdot |\begin{aligned}-2 & -1 \\ -2 & 2\end{aligned}| \\  & =0\cdot ((-1)\cdot 2-2\cdot 1)+(-1)\cdot ((-2)\cdot 2-(-2)\cdot 1)+1\cdot ((-2)\cdot 2-(-2)\cdot (-1)) \\  & =0\cdot ((-2)-2)+(-1)\cdot ((-4)-(-2))+1\cdot ((-4)-2) \\  & =0+2+(-6) \\  & =-4.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-4|=4.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(20, 11, 3)$, $B(20, 13, 5)$, $C(16, 9, 5)$, and $D(16, 15, 7)$.

- $80$
- $16$
- $96$
- $32$
- $64$

Source has no worked solution.

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(29, 17, 4)$, $B(29, 20, 7)$, $C(23, 14, 7)$, and $D(23, 23, 10)$.

- $270$
- $54$
- $324$
- $108$
- $216$

Source has no worked solution.

---

## Original q-20138

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(1, 2,-1)$, $B(2, 3, 1)$, $C(4, 1, 2)$, and $D(1, 4, 2)$.

- $3$
- $6$
- $9$
- $4$
- $\frac{1}{6}$

Source has no worked solution.

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(1, 2,-1)$, $B(2, 3, 1)$, $C(4, 1, 2)$, and $D(1, 4, 2)$.

- $3$
- $6$ (correct)
- $9$
- $4$
- $\frac{1}{6}$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+3j+k)-(i+2j-k) \\  & =i+j+2k \\  & =⟨1,1,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+j+2k)-(i+2j-k) \\  & =3i-j+3k \\  & =⟨3,-1,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(i+4j+2k)-(i+2j-k) \\  & =2j+3k \\  & =⟨0,2,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 1 & 2 \\ 3 & -1 & 3 \\ 0 & 2 & 3\end{aligned}| \\  & =1\cdot |\begin{aligned}-1 & 3 \\ 2 & 3\end{aligned}|-1\cdot |\begin{aligned}3 & 3 \\ 0 & 3\end{aligned}|+2\cdot |\begin{aligned}3 & -1 \\ 0 & 2\end{aligned}| \\  & =1\cdot ((-1)\cdot 3-2\cdot 3)+(-1)\cdot (3\cdot 3-0\cdot 3)+2\cdot (3\cdot 2-0\cdot (-1)) \\  & =1\cdot ((-3)-6)+(-1)\cdot (9-0)+2\cdot (6-0) \\  & =(-9)+(-9)+12 \\  & =-6.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-6|=6.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(4, 3,-1)$, $B(6, 5, 3)$, $C(10, 1, 5)$, and $D(4, 7, 5)$.

- $24$
- $48$
- $72$
- $32$
- $\frac{4}{3}$

Source has no worked solution.

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $AB^(→)$, $AC^(→)$ and $AD^(→)$, given the points $A(5, 5,-2)$, $B(8, 8, 4)$, $C(14, 2, 7)$, and $D(5, 11, 7)$.

- $81$
- $162$
- $243$
- $108$
- $\frac{9}{2}$

Source has no worked solution.

---

## Original q-128475

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(7,6,4),$ $B(8,5,9),$ $C(7,4,2),$ and $D(5,7,4).$

- $26$
- $22$ (correct)
- $32$
- $14$
- $11$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i+5j+9k)-(7i+6j+4k) \\  & =i-j+5k \\  & =⟨1,-1,5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(7i+4j+2k)-(7i+6j+4k) \\  & =-2j-2k \\  & =⟨0,-2,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+7j+4k)-(7i+6j+4k) \\  & =-2i+j \\  & =⟨-2,1,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & -1 & 5 \\ 0 & -2 & -2 \\ -2 & 1 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-2 & -2 \\ 1 & 0\end{aligned}|-(-1)\cdot |\begin{aligned}0 & -2 \\ -2 & 0\end{aligned}|+5\cdot |\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}| \\  & =((-2)\cdot 0-1\cdot (-2))+(0\cdot 0-(-2)\cdot (-2))+5(0\cdot 1-(-2)\cdot (-2)) \\  & =2-4-20 \\  & =-22.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-22|=22.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(7,6,4),$ $B(8,5,9),$ $C(7,4,2),$ and $D(5,7,4).$

- $26$
- $22$ (correct)
- $32$
- $14$
- $11$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i+5j+9k)-(7i+6j+4k) \\  & =i-j+5k \\  & =⟨1,-1,5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(7i+4j+2k)-(7i+6j+4k) \\  & =-2j-2k \\  & =⟨0,-2,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+7j+4k)-(7i+6j+4k) \\  & =-2i+j \\  & =⟨-2,1,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & -1 & 5 \\ 0 & -2 & -2 \\ -2 & 1 & 0\end{aligned}| \\  & =1\cdot |\begin{aligned}-2 & -2 \\ 1 & 0\end{aligned}|-(-1)\cdot |\begin{aligned}0 & -2 \\ -2 & 0\end{aligned}|+5\cdot |\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}| \\  & =((-2)\cdot 0-1\cdot (-2))+(0\cdot 0-(-2)\cdot (-2))+5(0\cdot 1-(-2)\cdot (-2)) \\  & =2-4-20 \\  & =-22.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-22|=22.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(16,11,9),$ $B(18,9,19),$ $C(16,7,5),$ and $D(12,13,9).$

- $208$
- $176$ (correct)
- $256$
- $112$
- $88$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(18i+9j+19k)-(16i+11j+9k) \\  & =2i-2j+10k \\  & =⟨2,-2,10⟩ \\ \overset{\to }{AC} & =c-a \\  & =(16i+7j+5k)-(16i+11j+9k) \\  & =-4j-4k \\  & =⟨0,-4,-4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(12i+13j+9k)-(16i+11j+9k) \\  & =-4i+2j \\  & =⟨-4,2,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & -2 & 10 \\ 0 & -4 & -4 \\ -4 & 2 & 0\end{aligned}| \\  & =2\cdot |\begin{aligned}-4 & -4 \\ 2 & 0\end{aligned}|-(-2)\cdot |\begin{aligned}0 & -4 \\ -4 & 0\end{aligned}|+10\cdot |\begin{aligned}0 & -4 \\ -4 & 2\end{aligned}| \\  & =2((-4)\cdot 0-2\cdot (-4))+2(0\cdot 0-(-4)\cdot (-4))+10(0\cdot 2-(-4)\cdot (-4)) \\  & =16-32-160 \\  & =-176.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-176|=176.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(23,17,13),$ $B(26,14,28),$ $C(23,11,7),$ and $D(17,20,13).$

- $702$
- $594$ (correct)
- $864$
- $378$
- $297$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(26i+14j+28k)-(23i+17j+13k) \\  & =3i-3j+15k \\  & =⟨3,-3,15⟩ \\ \overset{\to }{AC} & =c-a \\  & =(23i+11j+7k)-(23i+17j+13k) \\  & =-6j-6k \\  & =⟨0,-6,-6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(17i+20j+13k)-(23i+17j+13k) \\  & =-6i+3j \\  & =⟨-6,3,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & -3 & 15 \\ 0 & -6 & -6 \\ -6 & 3 & 0\end{aligned}| \\  & =3\cdot |\begin{aligned}-6 & -6 \\ 3 & 0\end{aligned}|-(-3)\cdot |\begin{aligned}0 & -6 \\ -6 & 0\end{aligned}|+15\cdot |\begin{aligned}0 & -6 \\ -6 & 3\end{aligned}| \\  & =3((-6)\cdot 0-3\cdot (-6))+3(0\cdot 0-(-6)\cdot (-6))+15(0\cdot 3-(-6)\cdot (-6)) \\  & =54-108-540 \\  & =-594.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-594|=594.
$$

---

## Original q-128483

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(5,1,4),$ $B(4,1,7),$ $C(3,1,5),$ and $D(2,3,3).$

- $15$
- $5$
- $12$
- $10$ (correct)
- $14$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i+j+7k)-(5i+j+4k) \\  & =-i+3k \\  & =⟨-1,0,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+j+5k)-(5i+j+4k) \\  & =-2i+k \\  & =⟨-2,0,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+3j+3k)-(5i+j+4k) \\  & =-3i+2j-k \\  & =⟨-3,2,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-1 & 0 & 3 \\ -2 & 0 & 1 \\ -3 & 2 & -1\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}0 & 1 \\ 2 & -1\end{aligned}|-0\cdot |\begin{aligned}-2 & 1 \\ -3 & -1\end{aligned}|+3\cdot |\begin{aligned}-2 & 0 \\ -3 & 2\end{aligned}| \\  & =-(0\cdot (-1)-2\cdot 1)-0+3((-2)\cdot 2-(-3)\cdot 0) \\  & =2-12 \\  & =-10.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-10|=10.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(5,1,4),$ $B(4,1,7),$ $C(3,1,5),$ and $D(2,3,3).$

- $15$
- $5$
- $12$
- $10$ (correct)
- $14$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i+j+7k)-(5i+j+4k) \\  & =-i+3k \\  & =⟨-1,0,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+j+5k)-(5i+j+4k) \\  & =-2i+k \\  & =⟨-2,0,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+3j+3k)-(5i+j+4k) \\  & =-3i+2j-k \\  & =⟨-3,2,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-1 & 0 & 3 \\ -2 & 0 & 1 \\ -3 & 2 & -1\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}0 & 1 \\ 2 & -1\end{aligned}|-0\cdot |\begin{aligned}-2 & 1 \\ -3 & -1\end{aligned}|+3\cdot |\begin{aligned}-2 & 0 \\ -3 & 2\end{aligned}| \\  & =-(0\cdot (-1)-2\cdot 1)-0+3((-2)\cdot 2-(-3)\cdot 0) \\  & =2-12 \\  & =-10.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-10|=10.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(12,1,9),$ $B(10,1,15),$ $C(8,1,11),$ and $D(6,5,7).$

- $120$
- $40$
- $96$
- $80$ (correct)
- $112$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(10i+j+15k)-(12i+j+9k) \\  & =-2i+6k \\  & =⟨-2,0,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(8i+j+11k)-(12i+j+9k) \\  & =-4i+2k \\  & =⟨-4,0,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(6i+5j+7k)-(12i+j+9k) \\  & =-6i+4j-2k \\  & =⟨-6,4,-2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-2 & 0 & 6 \\ -4 & 0 & 2 \\ -6 & 4 & -2\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}0 & 2 \\ 4 & -2\end{aligned}|-0\cdot |\begin{aligned}-4 & 2 \\ -6 & -2\end{aligned}|+6\cdot |\begin{aligned}-4 & 0 \\ -6 & 4\end{aligned}| \\  & =-2(0\cdot (-2)-4\cdot 2)-0+6((-4)\cdot 4-(-6)\cdot 0) \\  & =16-96 \\  & =-80.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-80|=80.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(17,2,13),$ $B(14,2,22),$ $C(11,2,16),$ and $D(8,8,10).$

- $405$
- $135$
- $324$
- $270$ (correct)
- $378$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(14i+2j+22k)-(17i+2j+13k) \\  & =-3i+9k \\  & =⟨-3,0,9⟩ \\ \overset{\to }{AC} & =c-a \\  & =(11i+2j+16k)-(17i+2j+13k) \\  & =-6i+3k \\  & =⟨-6,0,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i+8j+10k)-(17i+2j+13k) \\  & =-9i+6j-3k \\  & =⟨-9,6,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 0 & 9 \\ -6 & 0 & 3 \\ -9 & 6 & -3\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}0 & 3 \\ 6 & -3\end{aligned}|-0\cdot |\begin{aligned}-6 & 3 \\ -9 & -3\end{aligned}|+9\cdot |\begin{aligned}-6 & 0 \\ -9 & 6\end{aligned}| \\  & =-3(0\cdot (-3)-6\cdot 3)-0+9((-6)\cdot 6-(-9)\cdot 0) \\  & =54-324 \\  & =-270.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-270|=270.
$$

---

## Original q-20145

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,1,2)$, $B(3,3,3)$, $C(-2,-1,3)$, and $D(4,1,4).$

- $20$ (correct)
- $23$
- $\frac{21}{2}$
- $24$
- $29$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+3j+3k)-(2i+j+2k) \\  & =i+2j+k \\  & =⟨1,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-j+3k)-(2i+j+2k) \\  & =-4i-2j+k \\  & =⟨-4,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(4i+j+4k)-(2i+j+2k) \\  & =2i+2k \\  & =⟨2,0,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 2 & 1 \\ -4 & -2 & 1 \\ 2 & 0 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}-2 & 1 \\ 0 & 2\end{aligned}|-2\cdot |\begin{aligned}-4 & 1 \\ 2 & 2\end{aligned}|+1\cdot |\begin{aligned}-4 & -2 \\ 2 & 0\end{aligned}| \\  & =((-2)\cdot 2-0\cdot 1)-2((-4)\cdot 2-2\cdot 1)+((-4)\cdot 0-2\cdot (-2)) \\  & =-4+20+4 \\  & =20.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|20|=20.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,1,2)$, $B(3,3,3)$, $C(-2,-1,3)$, and $D(4,1,4).$

- $20$ (correct)
- $23$
- $\frac{21}{2}$
- $24$
- $29$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+3j+3k)-(2i+j+2k) \\  & =i+2j+k \\  & =⟨1,2,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-j+3k)-(2i+j+2k) \\  & =-4i-2j+k \\  & =⟨-4,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(4i+j+4k)-(2i+j+2k) \\  & =2i+2k \\  & =⟨2,0,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 2 & 1 \\ -4 & -2 & 1 \\ 2 & 0 & 2\end{aligned}| \\  & =1\cdot |\begin{aligned}-2 & 1 \\ 0 & 2\end{aligned}|-2\cdot |\begin{aligned}-4 & 1 \\ 2 & 2\end{aligned}|+1\cdot |\begin{aligned}-4 & -2 \\ 2 & 0\end{aligned}| \\  & =((-2)\cdot 2-0\cdot 1)-2((-4)\cdot 2-2\cdot 1)+((-4)\cdot 0-2\cdot (-2)) \\  & =-4+20+4 \\  & =20.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|20|=20.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(6,1,5)$, $B(8,5,7)$, $C(-2,-3,7)$, and $D(10,1,9).$

- $160$ (correct)
- $184$
- $84$
- $192$
- $232$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i+5j+7k)-(6i+j+5k) \\  & =2i+4j+2k \\  & =⟨2,4,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-3j+7k)-(6i+j+5k) \\  & =-8i-4j+2k \\  & =⟨-8,-4,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(10i+j+9k)-(6i+j+5k) \\  & =4i+4k \\  & =⟨4,0,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 4 & 2 \\ -8 & -4 & 2 \\ 4 & 0 & 4\end{aligned}| \\  & =2\cdot |\begin{aligned}-4 & 2 \\ 0 & 4\end{aligned}|-4\cdot |\begin{aligned}-8 & 2 \\ 4 & 4\end{aligned}|+2\cdot |\begin{aligned}-8 & -4 \\ 4 & 0\end{aligned}| \\  & =2((-4)\cdot 4-0\cdot 2)-4((-8)\cdot 4-4\cdot 2)+2((-8)\cdot 0-4\cdot (-4)) \\  & =-32+160+32 \\  & =160.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|160|=160.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(8,2,7)$, $B(11,8,10)$, $C(-4,-4,10)$, and $D(14,2,13).$

- $540$ (correct)
- $621$
- $\frac{567}{2}$
- $648$
- $783$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(11i+8j+10k)-(8i+2j+7k) \\  & =3i+6j+3k \\  & =⟨3,6,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-4i-4j+10k)-(8i+2j+7k) \\  & =-12i-6j+3k \\  & =⟨-12,-6,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(14i+2j+13k)-(8i+2j+7k) \\  & =6i+6k \\  & =⟨6,0,6⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 6 & 3 \\ -12 & -6 & 3 \\ 6 & 0 & 6\end{aligned}| \\  & =3\cdot |\begin{aligned}-6 & 3 \\ 0 & 6\end{aligned}|-6\cdot |\begin{aligned}-12 & 3 \\ 6 & 6\end{aligned}|+3\cdot |\begin{aligned}-12 & -6 \\ 6 & 0\end{aligned}| \\  & =3((-6)\cdot 6-0\cdot 3)-6((-12)\cdot 6-6\cdot 3)+3((-12)\cdot 0-6\cdot (-6)) \\  & =-108+540+108 \\  & =540.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|540|=540.
$$

---

## Original q-280314

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,0,-2),$ $B(3,-2,1),$ $C(-1,4,-1),$ and $D(2,1,0).$

$V=${{field-1}}

- $14$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i-2j+k)-(i-2k) \\  & =2i-2j+3k \\  & =⟨2,-2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i+4j-k)-(i-2k) \\  & =-2i+4j+k \\  & =⟨-2,4,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+j)-(i-2k) \\  & =i+j+2k \\  & =⟨1,1,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & -2 & 3 \\ -2 & 4 & 1 \\ 1 & 1 & 2\end{aligned}| \\  & =2\cdot |\begin{aligned}4 & 1 \\ 1 & 2\end{aligned}|-(-2)\cdot |\begin{aligned}-2 & 1 \\ 1 & 2\end{aligned}|+3\cdot |\begin{aligned}-2 & 4 \\ 1 & 1\end{aligned}| \\  & =2(8-1)+2(-4-1)+3(-2-4) \\  & =14-10-18 \\  & =-14.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-14|=14.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,0,-2),$ $B(3,-2,1),$ $C(-1,4,-1),$ and $D(2,1,0).$

$V=${{field-1}}

- $14$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i-2j+k)-(i-2k) \\  & =2i-2j+3k \\  & =⟨2,-2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i+4j-k)-(i-2k) \\  & =-2i+4j+k \\  & =⟨-2,4,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+j)-(i-2k) \\  & =i+j+2k \\  & =⟨1,1,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & -2 & 3 \\ -2 & 4 & 1 \\ 1 & 1 & 2\end{aligned}| \\  & =2\cdot |\begin{aligned}4 & 1 \\ 1 & 2\end{aligned}|-(-2)\cdot |\begin{aligned}-2 & 1 \\ 1 & 2\end{aligned}|+3\cdot |\begin{aligned}-2 & 4 \\ 1 & 1\end{aligned}| \\  & =2(8-1)+2(-4-1)+3(-2-4) \\  & =14-10-18 \\  & =-14.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-14|=14.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(4,-1,-3),$ $B(8,-5,3),$ $C(0,7,-1),$ and $D(6,1,1).$

$V=${{field-1}}

- $112$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i-5j+3k)-(4i-j-3k) \\  & =4i-4j+6k \\  & =⟨4,-4,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(7j-k)-(4i-j-3k) \\  & =-4i+8j+2k \\  & =⟨-4,8,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(6i+j+k)-(4i-j-3k) \\  & =2i+2j+4k \\  & =⟨2,2,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & -4 & 6 \\ -4 & 8 & 2 \\ 2 & 2 & 4\end{aligned}| \\  & =4\cdot |\begin{aligned}8 & 2 \\ 2 & 4\end{aligned}|-(-4)\cdot |\begin{aligned}-4 & 2 \\ 2 & 4\end{aligned}|+6\cdot |\begin{aligned}-4 & 8 \\ 2 & 2\end{aligned}| \\  & =4(32-4)+4(-16-4)+6(-8-16) \\  & =112-80-144 \\  & =-112.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-112|=112.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(5,-1,-5),$ $B(11,-7,4),$ $C(-1,11,-2),$ and $D(8,2,1).$

$V=${{field-1}}

- $378$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(11i-7j+4k)-(5i-j-5k) \\  & =6i-6j+9k \\  & =⟨6,-6,9⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i+11j-2k)-(5i-j-5k) \\  & =-6i+12j+3k \\  & =⟨-6,12,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i+2j+k)-(5i-j-5k) \\  & =3i+3j+6k \\  & =⟨3,3,6⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}6 & -6 & 9 \\ -6 & 12 & 3 \\ 3 & 3 & 6\end{aligned}| \\  & =6\cdot |\begin{aligned}12 & 3 \\ 3 & 6\end{aligned}|-(-6)\cdot |\begin{aligned}-6 & 3 \\ 3 & 6\end{aligned}|+9\cdot |\begin{aligned}-6 & 12 \\ 3 & 3\end{aligned}| \\  & =6(72-9)+6(-36-9)+9(-18-36) \\  & =378-270-486 \\  & =-378.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-378|=378.
$$

---

## Original q-280321

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,-3,2),$ $B(4,-1,5),$ $C(-2,0,1),$ and $D(3,-2,3).$

$V=${{field-1}}

- $13$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i-j+5k)-(i-3j+2k) \\  & =3i+2j+3k \\  & =⟨3,2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i+k)-(i-3j+2k) \\  & =-3i+3j-k \\  & =⟨-3,3,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j+3k)-(i-3j+2k) \\  & =2i+j+k \\  & =⟨2,1,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 2 & 3 \\ -3 & 3 & -1 \\ 2 & 1 & 1\end{aligned}| \\  & =3\cdot |\begin{aligned}3 & -1 \\ 1 & 1\end{aligned}|-2\cdot |\begin{aligned}-3 & -1 \\ 2 & 1\end{aligned}|+3\cdot |\begin{aligned}-3 & 3 \\ 2 & 1\end{aligned}| \\  & =3(3\cdot 1-(-1)\cdot 1)-2((-3)\cdot 1-(-1)\cdot 2)+3((-3)\cdot 1-3\cdot 2) \\  & =3(3+1)-2(-3+2)+3(-3-6) \\  & =12+2-27 \\  & =-13.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-13|=13.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,-3,2),$ $B(4,-1,5),$ $C(-2,0,1),$ and $D(3,-2,3).$

$V=${{field-1}}

- $13$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(4i-j+5k)-(i-3j+2k) \\  & =3i+2j+3k \\  & =⟨3,2,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i+k)-(i-3j+2k) \\  & =-3i+3j-k \\  & =⟨-3,3,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j+3k)-(i-3j+2k) \\  & =2i+j+k \\  & =⟨2,1,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 2 & 3 \\ -3 & 3 & -1 \\ 2 & 1 & 1\end{aligned}| \\  & =3\cdot |\begin{aligned}3 & -1 \\ 1 & 1\end{aligned}|-2\cdot |\begin{aligned}-3 & -1 \\ 2 & 1\end{aligned}|+3\cdot |\begin{aligned}-3 & 3 \\ 2 & 1\end{aligned}| \\  & =3(3\cdot 1-(-1)\cdot 1)-2((-3)\cdot 1-(-1)\cdot 2)+3((-3)\cdot 1-3\cdot 2) \\  & =3(3+1)-2(-3+2)+3(-3-6) \\  & =12+2-27 \\  & =-13.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-13|=13.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(4,-7,5),$ $B(10,-3,11),$ $C(-2,-1,3),$ and $D(8,-5,7).$

$V=${{field-1}}

- $104$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(10i-3j+11k)-(4i-7j+5k) \\  & =6i+4j+6k \\  & =⟨6,4,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-j+3k)-(4i-7j+5k) \\  & =-6i+6j-2k \\  & =⟨-6,6,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-5j+7k)-(4i-7j+5k) \\  & =4i+2j+2k \\  & =⟨4,2,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}6 & 4 & 6 \\ -6 & 6 & -2 \\ 4 & 2 & 2\end{aligned}| \\  & =6\cdot |\begin{aligned}6 & -2 \\ 2 & 2\end{aligned}|-4\cdot |\begin{aligned}-6 & -2 \\ 4 & 2\end{aligned}|+6\cdot |\begin{aligned}-6 & 6 \\ 4 & 2\end{aligned}| \\  & =6(6\cdot 2-(-2)\cdot 2)-4((-6)\cdot 2-(-2)\cdot 4)+6((-6)\cdot 2-6\cdot 4) \\  & =6(12+4)-4(-12+8)+6(-12-24) \\  & =96+16-216 \\  & =-104.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-104|=104.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(5,-10,7),$ $B(14,-4,16),$ $C(-4,-1,4),$ and $D(11,-7,10).$

$V=${{field-1}}

- $351$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(14i-4j+16k)-(5i-10j+7k) \\  & =9i+6j+9k \\  & =⟨9,6,9⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-4i-j+4k)-(5i-10j+7k) \\  & =-9i+9j-3k \\  & =⟨-9,9,-3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(11i-7j+10k)-(5i-10j+7k) \\  & =6i+3j+3k \\  & =⟨6,3,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}9 & 6 & 9 \\ -9 & 9 & -3 \\ 6 & 3 & 3\end{aligned}| \\  & =9\cdot |\begin{aligned}9 & -3 \\ 3 & 3\end{aligned}|-6\cdot |\begin{aligned}-9 & -3 \\ 6 & 3\end{aligned}|+9\cdot |\begin{aligned}-9 & 9 \\ 6 & 3\end{aligned}| \\  & =9(9\cdot 3-(-3)\cdot 3)-6((-9)\cdot 3-(-3)\cdot 6)+9((-9)\cdot 3-9\cdot 6) \\  & =9(27+9)-6(-27+18)+9(-27-54) \\  & =324+54-729 \\  & =-351.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-351|=351.
$$

---

## Original q-281023

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,0,2),$ $B(3,4,5),$ $C(6,2,4),$ and $D(5,3,6).$

$V=${{field-1}}

- $23$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+4j+5k)-(i+2k) \\  & =2i+4j+3k \\  & =⟨2,4,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(6i+2j+4k)-(i+2k) \\  & =5i+2j+2k \\  & =⟨5,2,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+3j+6k)-(i+2k) \\  & =4i+3j+4k \\  & =⟨4,3,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 4 & 3 \\ 5 & 2 & 2 \\ 4 & 3 & 4\end{aligned}| \\  & =2\cdot |\begin{aligned}2 & 2 \\ 3 & 4\end{aligned}|-4\cdot |\begin{aligned}5 & 2 \\ 4 & 4\end{aligned}|+3\cdot |\begin{aligned}5 & 2 \\ 4 & 3\end{aligned}| \\  & =2(2\cdot 4-2\cdot 3)-4(5\cdot 4-2\cdot 4)+3(5\cdot 3-2\cdot 4) \\  & =2(8-6)-4(20-8)+3(15-8) \\  & =4-48+21 \\  & =-23.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-23|=23.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,0,2),$ $B(3,4,5),$ $C(6,2,4),$ and $D(5,3,6).$

$V=${{field-1}}

- $23$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+4j+5k)-(i+2k) \\  & =2i+4j+3k \\  & =⟨2,4,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(6i+2j+4k)-(i+2k) \\  & =5i+2j+2k \\  & =⟨5,2,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+3j+6k)-(i+2k) \\  & =4i+3j+4k \\  & =⟨4,3,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 4 & 3 \\ 5 & 2 & 2 \\ 4 & 3 & 4\end{aligned}| \\  & =2\cdot |\begin{aligned}2 & 2 \\ 3 & 4\end{aligned}|-4\cdot |\begin{aligned}5 & 2 \\ 4 & 4\end{aligned}|+3\cdot |\begin{aligned}5 & 2 \\ 4 & 3\end{aligned}| \\  & =2(2\cdot 4-2\cdot 3)-4(5\cdot 4-2\cdot 4)+3(5\cdot 3-2\cdot 4) \\  & =2(8-6)-4(20-8)+3(15-8) \\  & =4-48+21 \\  & =-23.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-23|=23.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(4,-1,5),$ $B(8,7,11),$ $C(14,3,9),$ and $D(12,5,13).$

$V=${{field-1}}

- $184$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i+7j+11k)-(4i-j+5k) \\  & =4i+8j+6k \\  & =⟨4,8,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(14i+3j+9k)-(4i-j+5k) \\  & =10i+4j+4k \\  & =⟨10,4,4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(12i+5j+13k)-(4i-j+5k) \\  & =8i+6j+8k \\  & =⟨8,6,8⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 8 & 6 \\ 10 & 4 & 4 \\ 8 & 6 & 8\end{aligned}| \\  & =4\cdot |\begin{aligned}4 & 4 \\ 6 & 8\end{aligned}|-8\cdot |\begin{aligned}10 & 4 \\ 8 & 8\end{aligned}|+6\cdot |\begin{aligned}10 & 4 \\ 8 & 6\end{aligned}| \\  & =4(4\cdot 8-4\cdot 6)-8(10\cdot 8-4\cdot 8)+6(10\cdot 6-4\cdot 8) \\  & =4(32-24)-8(80-32)+6(60-32) \\  & =32-384+168 \\  & =-184.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-184|=184.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(5,-1,7),$ $B(11,11,16),$ $C(20,5,13),$ and $D(17,8,19).$

$V=${{field-1}}

- $621$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(11i+11j+16k)-(5i-j+7k) \\  & =6i+12j+9k \\  & =⟨6,12,9⟩ \\ \overset{\to }{AC} & =c-a \\  & =(20i+5j+13k)-(5i-j+7k) \\  & =15i+6j+6k \\  & =⟨15,6,6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(17i+8j+19k)-(5i-j+7k) \\  & =12i+9j+12k \\  & =⟨12,9,12⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}6 & 12 & 9 \\ 15 & 6 & 6 \\ 12 & 9 & 12\end{aligned}| \\  & =6\cdot |\begin{aligned}6 & 6 \\ 9 & 12\end{aligned}|-12\cdot |\begin{aligned}15 & 6 \\ 12 & 12\end{aligned}|+9\cdot |\begin{aligned}15 & 6 \\ 12 & 9\end{aligned}| \\  & =6(6\cdot 12-6\cdot 9)-12(15\cdot 12-6\cdot 12)+9(15\cdot 9-6\cdot 12) \\  & =6(72-54)-12(180-72)+9(135-72) \\  & =108-1296+567 \\  & =-621.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-621|=621.
$$

---

## Original q-281025

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(3,0,2),$ $B(5,1,3),$ $C(4,3,5),$ and $D(3,0,5).$

$V=${{field-1}}

- $15$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(5i+1j+3k)-(3i+2k) \\  & =2i+j+k \\  & =⟨2,1,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+3j+5k)-(3i+2k) \\  & =i+3j+3k \\  & =⟨1,3,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i+5k)-(3i+2k) \\  & =3k \\  & =⟨0,0,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 1 & 1 \\ 1 & 3 & 3 \\ 0 & 0 & 3\end{aligned}| \\  & =2\cdot |\begin{aligned}3 & 3 \\ 0 & 3\end{aligned}|-1\cdot |\begin{aligned}1 & 3 \\ 0 & 3\end{aligned}|+1\cdot |\begin{aligned}1 & 3 \\ 0 & 0\end{aligned}| \\  & =2(3\cdot 3-3\cdot 0)-1(1\cdot 3-3\cdot 0)+1(1\cdot 0-3\cdot 0) \\  & =2(9)-1(3)+1(0) \\  & =18-3+0 \\  & =15.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|15|=15.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(3,0,2),$ $B(5,1,3),$ $C(4,3,5),$ and $D(3,0,5).$

$V=${{field-1}}

- $15$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(5i+1j+3k)-(3i+2k) \\  & =2i+j+k \\  & =⟨2,1,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+3j+5k)-(3i+2k) \\  & =i+3j+3k \\  & =⟨1,3,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i+5k)-(3i+2k) \\  & =3k \\  & =⟨0,0,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 1 & 1 \\ 1 & 3 & 3 \\ 0 & 0 & 3\end{aligned}| \\  & =2\cdot |\begin{aligned}3 & 3 \\ 0 & 3\end{aligned}|-1\cdot |\begin{aligned}1 & 3 \\ 0 & 3\end{aligned}|+1\cdot |\begin{aligned}1 & 3 \\ 0 & 0\end{aligned}| \\  & =2(3\cdot 3-3\cdot 0)-1(1\cdot 3-3\cdot 0)+1(1\cdot 0-3\cdot 0) \\  & =2(9)-1(3)+1(0) \\  & =18-3+0 \\  & =15.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|15|=15.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(8,-1,5),$ $B(12,1,7),$ $C(10,5,11),$ and $D(8,-1,11).$

$V=${{field-1}}

- $120$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(12i+1j+7k)-(8i-j+5k) \\  & =4i+2j+2k \\  & =⟨4,2,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(10i+5j+11k)-(8i-j+5k) \\  & =2i+6j+6k \\  & =⟨2,6,6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-j+11k)-(8i-j+5k) \\  & =6k \\  & =⟨0,0,6⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 2 & 2 \\ 2 & 6 & 6 \\ 0 & 0 & 6\end{aligned}| \\  & =4\cdot |\begin{aligned}6 & 6 \\ 0 & 6\end{aligned}|-2\cdot |\begin{aligned}2 & 6 \\ 0 & 6\end{aligned}|+2\cdot |\begin{aligned}2 & 6 \\ 0 & 0\end{aligned}| \\  & =4(6\cdot 6-6\cdot 0)-2(2\cdot 6-6\cdot 0)+2(2\cdot 0-6\cdot 0) \\  & =4(36)-2(12)+2(0) \\  & =144-24+0 \\  & =120.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|120|=120.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(11,-1,7),$ $B(17,2,10),$ $C(14,8,16),$ and $D(11,-1,16).$

$V=${{field-1}}

- $405$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(17i+2j+10k)-(11i-j+7k) \\  & =6i+3j+3k \\  & =⟨6,3,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(14i+8j+16k)-(11i-j+7k) \\  & =3i+9j+9k \\  & =⟨3,9,9⟩ \\ \overset{\to }{AD} & =d-a \\  & =(11i-j+16k)-(11i-j+7k) \\  & =9k \\  & =⟨0,0,9⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}6 & 3 & 3 \\ 3 & 9 & 9 \\ 0 & 0 & 9\end{aligned}| \\  & =6\cdot |\begin{aligned}9 & 9 \\ 0 & 9\end{aligned}|-3\cdot |\begin{aligned}3 & 9 \\ 0 & 9\end{aligned}|+3\cdot |\begin{aligned}3 & 9 \\ 0 & 0\end{aligned}| \\  & =6(9\cdot 9-9\cdot 0)-3(3\cdot 9-9\cdot 0)+3(3\cdot 0-9\cdot 0) \\  & =6(81)-3(27)+3(0) \\  & =486-81+0 \\  & =405.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|405|=405.
$$

---

## Original q-281029

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,1,3),$ $B(0,5,5),$ $C(3,4,5),$ and $D(2,0,2).$

$V=${{field-1}}

- $10$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(5j+5k)-(1j+3k) \\  & =4j+2k \\  & =⟨0,4,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+4j+5k)-(1j+3k) \\  & =3i+3j+2k \\  & =⟨3,3,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+2k)-(1j+3k) \\  & =2i-1j-1k \\  & =⟨2,-1,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}0 & 4 & 2 \\ 3 & 3 & 2 \\ 2 & -1 & -1\end{aligned}| \\  & =0\cdot |\begin{aligned}3 & 2 \\ -1 & -1\end{aligned}|-4\cdot |\begin{aligned}3 & 2 \\ 2 & -1\end{aligned}|+2\cdot |\begin{aligned}3 & 3 \\ 2 & -1\end{aligned}| \\  & =-4(3\cdot -1-2\cdot 2)+2(3\cdot -1-3\cdot 2) \\  & =28-18 \\  & =10.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|10|=10.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,1,3),$ $B(0,5,5),$ $C(3,4,5),$ and $D(2,0,2).$

$V=${{field-1}}

- $10$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(5j+5k)-(1j+3k) \\  & =4j+2k \\  & =⟨0,4,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+4j+5k)-(1j+3k) \\  & =3i+3j+2k \\  & =⟨3,3,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+2k)-(1j+3k) \\  & =2i-1j-1k \\  & =⟨2,-1,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}0 & 4 & 2 \\ 3 & 3 & 2 \\ 2 & -1 & -1\end{aligned}| \\  & =0\cdot |\begin{aligned}3 & 2 \\ -1 & -1\end{aligned}|-4\cdot |\begin{aligned}3 & 2 \\ 2 & -1\end{aligned}|+2\cdot |\begin{aligned}3 & 3 \\ 2 & -1\end{aligned}| \\  & =-4(3\cdot -1-2\cdot 2)+2(3\cdot -1-3\cdot 2) \\  & =28-18 \\  & =10.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|10|=10.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,1,7),$ $B(2,9,11),$ $C(8,7,11),$ and $D(6,-1,5).$

$V=${{field-1}}

- $80$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+9j+11k)-(2i+1j+7k) \\  & =8j+4k \\  & =⟨0,8,4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(8i+7j+11k)-(2i+1j+7k) \\  & =6i+6j+4k \\  & =⟨6,6,4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(6i-j+5k)-(2i+1j+7k) \\  & =4i-2j-2k \\  & =⟨4,-2,-2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}0 & 8 & 4 \\ 6 & 6 & 4 \\ 4 & -2 & -2\end{aligned}| \\  & =0\cdot |\begin{aligned}6 & 4 \\ -2 & -2\end{aligned}|-8\cdot |\begin{aligned}6 & 4 \\ 4 & -2\end{aligned}|+4\cdot |\begin{aligned}6 & 6 \\ 4 & -2\end{aligned}| \\  & =-8(6\cdot -2-4\cdot 4)+4(6\cdot -2-6\cdot 4) \\  & =224-144 \\  & =80.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|80|=80.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,2,10),$ $B(2,14,16),$ $C(11,11,16),$ and $D(8,-1,7).$

$V=${{field-1}}

- $270$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+14j+16k)-(2i+2j+10k) \\  & =12j+6k \\  & =⟨0,12,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(11i+11j+16k)-(2i+2j+10k) \\  & =9i+9j+6k \\  & =⟨9,9,6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-j+7k)-(2i+2j+10k) \\  & =6i-3j-3k \\  & =⟨6,-3,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}0 & 12 & 6 \\ 9 & 9 & 6 \\ 6 & -3 & -3\end{aligned}| \\  & =0\cdot |\begin{aligned}9 & 6 \\ -3 & -3\end{aligned}|-12\cdot |\begin{aligned}9 & 6 \\ 6 & -3\end{aligned}|+6\cdot |\begin{aligned}9 & 9 \\ 6 & -3\end{aligned}| \\  & =-12(9\cdot -3-6\cdot 6)+6(9\cdot -3-9\cdot 6) \\  & =756-486 \\  & =270.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|270|=270.
$$

---

## Original q-281030

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(-1,0,1),$ $B(2,-3,4),$ $C(-2,-2,2),$ and $D(0,-1,5).$

$V=${{field-1}}

- $27$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i-3j+4k)-(-i+1k) \\  & =3i-3j+3k \\  & =⟨3,-3,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2j+2k)-(-i+1k) \\  & =-i-2j+1k \\  & =⟨-1,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-j+5k)-(-i+1k) \\  & =i-j+4k \\  & =⟨1,-1,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & -3 & 3 \\ -1 & -2 & 1 \\ 1 & -1 & 4\end{aligned}| \\  & =3\cdot |\begin{aligned}-2 & 1 \\ -1 & 4\end{aligned}|-(-3)\cdot |\begin{aligned}-1 & 1 \\ 1 & 4\end{aligned}|+3\cdot |\begin{aligned}-1 & -2 \\ 1 & -1\end{aligned}| \\  & =3(-8+1)+3(-4-1)+3(1-(-2)) \\  & =-21-15+9 \\  & =-27.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-27|=27.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(-1,0,1),$ $B(2,-3,4),$ $C(-2,-2,2),$ and $D(0,-1,5).$

$V=${{field-1}}

- $27$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i-3j+4k)-(-i+1k) \\  & =3i-3j+3k \\  & =⟨3,-3,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2j+2k)-(-i+1k) \\  & =-i-2j+1k \\  & =⟨-1,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-j+5k)-(-i+1k) \\  & =i-j+4k \\  & =⟨1,-1,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & -3 & 3 \\ -1 & -2 & 1 \\ 1 & -1 & 4\end{aligned}| \\  & =3\cdot |\begin{aligned}-2 & 1 \\ -1 & 4\end{aligned}|-(-3)\cdot |\begin{aligned}-1 & 1 \\ 1 & 4\end{aligned}|+3\cdot |\begin{aligned}-1 & -2 \\ 1 & -1\end{aligned}| \\  & =3(-8+1)+3(-4-1)+3(1-(-2)) \\  & =-21-15+9 \\  & =-27.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-27|=27.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,-1,3),$ $B(6,-7,9),$ $C(-2,-5,5),$ and $D(2,-3,11).$

$V=${{field-1}}

- $216$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(6i-7j+9k)-(-j+3k) \\  & =6i-6j+6k \\  & =⟨6,-6,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-5j+5k)-(-j+3k) \\  & =-2i-4j+2k \\  & =⟨-2,-4,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i-3j+11k)-(-j+3k) \\  & =2i-2j+8k \\  & =⟨2,-2,8⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}6 & -6 & 6 \\ -2 & -4 & 2 \\ 2 & -2 & 8\end{aligned}| \\  & =6\cdot |\begin{aligned}-4 & 2 \\ -2 & 8\end{aligned}|-(-6)\cdot |\begin{aligned}-2 & 2 \\ 2 & 8\end{aligned}|+6\cdot |\begin{aligned}-2 & -4 \\ 2 & -2\end{aligned}| \\  & =6(-32+4)+6(-16-4)+6(4-(-8)) \\  & =-168-120+72 \\  & =-216.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-216|=216.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(-1,-1,4),$ $B(8,-10,13),$ $C(-4,-7,7),$ and $D(2,-4,16).$

$V=${{field-1}}

- $729$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i-10j+13k)-(-i-j+4k) \\  & =9i-9j+9k \\  & =⟨9,-9,9⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-4i-7j+7k)-(-i-j+4k) \\  & =-3i-6j+3k \\  & =⟨-3,-6,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i-4j+16k)-(-i-j+4k) \\  & =3i-3j+12k \\  & =⟨3,-3,12⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}9 & -9 & 9 \\ -3 & -6 & 3 \\ 3 & -3 & 12\end{aligned}| \\  & =9\cdot |\begin{aligned}-6 & 3 \\ -3 & 12\end{aligned}|-(-9)\cdot |\begin{aligned}-3 & 3 \\ 3 & 12\end{aligned}|+9\cdot |\begin{aligned}-3 & -6 \\ 3 & -3\end{aligned}| \\  & =9(-72+9)+9(-36-9)+9(9-(-18)) \\  & =-567-405+243 \\  & =-729.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-729|=729.
$$

---

## Original q-73744

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(1,1,0)$, $B(-2,1,0)$, $C(3,2,0)$, and $D(1,2,3).$

- $12$
- $9$ (correct)
- $3$
- $6$
- $18$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+j)-(i+j) \\  & =-3i \\  & =⟨-3,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j)-(i+j) \\  & =2i+1j \\  & =⟨2,1,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(i+2j+3k)-(i+j) \\  & =3j+3k \\  & =⟨0,1,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 1 & 3\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}1 & 0 \\ 1 & 3\end{aligned}|-0\cdot |\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|+0\cdot |\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}| \\  & =-3(1\cdot 3-1\cdot 0)-0+0 \\  & =-9.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-9|=9.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(1,1,0)$, $B(-2,1,0)$, $C(3,2,0)$, and $D(1,2,3).$

- $12$
- $9$ (correct)
- $3$
- $6$
- $18$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+j)-(i+j) \\  & =-3i \\  & =⟨-3,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(3i+2j)-(i+j) \\  & =2i+1j \\  & =⟨2,1,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(i+2j+3k)-(i+j) \\  & =j+3k \\  & =⟨0,1,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 1 & 3\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}1 & 0 \\ 1 & 3\end{aligned}|-0\cdot |\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|+0\cdot |\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}| \\  & =-3(1\cdot 3-1\cdot 0)-0+0 \\  & =-9.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-9|=9.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(4,1,1)$, $B(-2,1,1)$, $C(8,3,1)$, and $D(4,3,7).$

- $96$
- $72$ (correct)
- $24$
- $48$
- $144$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+j+k)-(4i+j+k) \\  & =-6i \\  & =⟨-6,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(8i+3j+k)-(4i+j+k) \\  & =4i+2j \\  & =⟨4,2,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(4i+3j+7k)-(4i+j+k) \\  & =6j+6k \\  & =⟨0,2,6⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-6 & 0 & 0 \\ 4 & 2 & 0 \\ 0 & 2 & 6\end{aligned}| \\  & =(-6)\cdot |\begin{aligned}2 & 0 \\ 2 & 6\end{aligned}|-0\cdot |\begin{aligned}4 & 0 \\ 0 & 6\end{aligned}|+0\cdot |\begin{aligned}4 & 2 \\ 0 & 2\end{aligned}| \\  & =-6(2\cdot 6-2\cdot 0)-0+0 \\  & =-72.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-72|=72.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(5,2,1)$, $B(-4,2,1)$, $C(11,5,1)$, and $D(5,5,10).$

- $324$
- $243$ (correct)
- $81$
- $162$
- $486$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-4i+2j+k)-(5i+2j+k) \\  & =-9i \\  & =⟨-9,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(11i+5j+k)-(5i+2j+k) \\  & =6i+3j \\  & =⟨6,3,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+5j+10k)-(5i+2j+k) \\  & =9j+9k \\  & =⟨0,3,9⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-9 & 0 & 0 \\ 6 & 3 & 0 \\ 0 & 3 & 9\end{aligned}| \\  & =(-9)\cdot |\begin{aligned}3 & 0 \\ 3 & 9\end{aligned}|-0\cdot |\begin{aligned}6 & 0 \\ 0 & 9\end{aligned}|+0\cdot |\begin{aligned}6 & 3 \\ 0 & 3\end{aligned}| \\  & =-9(3\cdot 9-3\cdot 0)-0+0 \\  & =-243.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-243|=243.
$$

---

## Original q-73745

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(1,-1,2)$, $B(-2,2,3)$, $C(1,1,1)$, and $D(-1,3,-2).$

- $18$
- $20$
- $22$ (correct)
- $11$
- $16$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+2j+3k)-(i-j+2k) \\  & =-3i+3j+k \\  & =⟨-3,3,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+k)-(i-j+2k) \\  & =2j-k \\  & =⟨0,2,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-i+3j-2k)-(i-j+2k) \\  & =-2i+4j-4k \\  & =⟨-2,4,-4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 3 & 1 \\ 0 & 2 & -1 \\ -2 & 4 & -4\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}2 & -1 \\ 4 & -4\end{aligned}|-3\cdot |\begin{aligned}0 & -1 \\ -2 & -4\end{aligned}|+1\cdot |\begin{aligned}0 & 2 \\ -2 & 4\end{aligned}| \\  & =-3(2\cdot (-4)-4\cdot (-1))-3(0\cdot (-4)-(-2)\cdot (-1))+(0\cdot 4-(-2)\cdot 2) \\  & =12+6+4 \\  & =22.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|22|=22.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(1,-1,2)$, $B(-2,2,3)$, $C(1,1,1)$, and $D(-1,3,-2).$

- $18$
- $20$
- $22$ (correct)
- $11$
- $16$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+2j+3k)-(i-j+2k) \\  & =-3i+3j+k \\  & =⟨-3,3,1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+k)-(i-j+2k) \\  & =2j-k \\  & =⟨0,2,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-i+3j-2k)-(i-j+2k) \\  & =-2i+4j-4k \\  & =⟨-2,4,-4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 3 & 1 \\ 0 & 2 & -1 \\ -2 & 4 & -4\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}2 & -1 \\ 4 & -4\end{aligned}|-3\cdot |\begin{aligned}0 & -1 \\ -2 & -4\end{aligned}|+1\cdot |\begin{aligned}0 & 2 \\ -2 & 4\end{aligned}| \\  & =-3(2\cdot (-4)-4\cdot (-1))-3(0\cdot (-4)-(-2)\cdot (-1))+(0\cdot 4-(-2)\cdot 2) \\  & =12+6+4 \\  & =22.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|22|=22.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(4,-3,5)$, $B(-2,3,7)$, $C(4,1,3)$, and $D(0,5,-3).$

- $144$
- $160$
- $176$ (correct)
- $88$
- $128$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i+3j+7k)-(4i-3j+5k) \\  & =-6i+6j+2k \\  & =⟨-6,6,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+j+3k)-(4i-3j+5k) \\  & =4j-2k \\  & =⟨0,4,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5j-3k)-(4i-3j+5k) \\  & =-4i+8j-8k \\  & =⟨-4,8,-8⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-6 & 6 & 2 \\ 0 & 4 & -2 \\ -4 & 8 & -8\end{aligned}| \\  & =(-6)\cdot |\begin{aligned}4 & -2 \\ 8 & -8\end{aligned}|-6\cdot |\begin{aligned}0 & -2 \\ -4 & -8\end{aligned}|+2\cdot |\begin{aligned}0 & 4 \\ -4 & 8\end{aligned}| \\  & =-6(4\cdot (-8)-8\cdot (-2))-6(0\cdot (-8)-(-4)\cdot (-2))+2(0\cdot 8-(-4)\cdot 4) \\  & =96+48+32 \\  & =176.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|176|=176.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(5,-4,7)$, $B(-4,5,10)$, $C(5,2,4)$, and $D(-1,8,-5).$

- $486$
- $540$
- $594$ (correct)
- $297$
- $432$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-4i+5j+10k)-(5i-4j+7k) \\  & =-9i+9j+3k \\  & =⟨-9,9,3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i+2j+4k)-(5i-4j+7k) \\  & =6j-3k \\  & =⟨0,6,-3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-i+8j-5k)-(5i-4j+7k) \\  & =-6i+12j-12k \\  & =⟨-6,12,-12⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-9 & 9 & 3 \\ 0 & 6 & -3 \\ -6 & 12 & -12\end{aligned}| \\  & =(-9)\cdot |\begin{aligned}6 & -3 \\ 12 & -12\end{aligned}|-9\cdot |\begin{aligned}0 & -3 \\ -6 & -12\end{aligned}|+3\cdot |\begin{aligned}0 & 6 \\ -6 & 12\end{aligned}| \\  & =-9(6\cdot (-12)-12\cdot (-3))-9(0\cdot (-12)-(-6)\cdot (-3))+3(0\cdot 12-(-6)\cdot 6) \\  & =324+162+108 \\  & =594.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|594|=594.
$$

---

## Original q-73746

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(0,1,2)$, $B(-1,0,1)$, $C(1,1,0)$, and $D(3,-1,3).$

- $15$
- $13$ (correct)
- $11$
- $20$
- $16$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+k)-(j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j)-(j+2k) \\  & =i-2k \\  & =⟨1,0,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-j+3k)-(j+2k) \\  & =3i-2j+k \\  & =⟨3,-2,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-1 & -1 & -1 \\ 1 & 0 & -2 \\ 3 & -2 & 1\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|-(-1)\cdot |\begin{aligned}1 & -2 \\ 3 & 1\end{aligned}|+(-1)\cdot |\begin{aligned}1 & 0 \\ 3 & -2\end{aligned}| \\  & =-(0\cdot 1-(-2)\cdot (-2))+(1\cdot 1-3\cdot (-2))-(1\cdot (-2)-3\cdot 0) \\  & =4+7+2 \\  & =13.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|13|=13.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(0,1,2)$, $B(-1,0,1)$, $C(1,1,0)$, and $D(3,-1,3).$

- $15$
- $13$ (correct)
- $11$
- $20$
- $16$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+k)-(j+2k) \\  & =-i-j-k \\  & =⟨-1,-1,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j)-(j+2k) \\  & =i-2k \\  & =⟨1,0,-2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-j+3k)-(j+2k) \\  & =3i-2j+k \\  & =⟨3,-2,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-1 & -1 & -1 \\ 1 & 0 & -2 \\ 3 & -2 & 1\end{aligned}| \\  & =(-1)\cdot |\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|-(-1)\cdot |\begin{aligned}1 & -2 \\ 3 & 1\end{aligned}|+(-1)\cdot |\begin{aligned}1 & 0 \\ 3 & -2\end{aligned}| \\  & =-(0\cdot 1-(-2)\cdot (-2))+(1\cdot 1-3\cdot (-2))-(1\cdot (-2)-3\cdot 0) \\  & =4+7+2 \\  & =13.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|13|=13.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,1,5)$, $B(0,-1,3)$, $C(4,1,1)$, and $D(8,-3,7).$

- $120$
- $104$ (correct)
- $88$
- $160$
- $128$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-j+3k)-(2i+j+5k) \\  & =-2i-2j-2k \\  & =⟨-2,-2,-2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+j+k)-(2i+j+5k) \\  & =2i-4k \\  & =⟨2,0,-4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-3j+7k)-(2i+j+5k) \\  & =6i-4j+2k \\  & =⟨6,-4,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-2 & -2 & -2 \\ 2 & 0 & -4 \\ 6 & -4 & 2\end{aligned}| \\  & =(-2)\cdot |\begin{aligned}0 & -4 \\ -4 & 2\end{aligned}|-(-2)\cdot |\begin{aligned}2 & -4 \\ 6 & 2\end{aligned}|+(-2)\cdot |\begin{aligned}2 & 0 \\ 6 & -4\end{aligned}| \\  & =-2(0\cdot 2-(-4)\cdot (-4))+2(2\cdot 2-6\cdot (-4))-2(2\cdot (-4)-6\cdot 0) \\  & =32+56+16 \\  & =104.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|104|=104.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,2,7)$, $B(-1,-1,4)$, $C(5,2,1)$, and $D(11,-4,10).$

- $405$
- $351$ (correct)
- $297$
- $540$
- $432$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i-j+4k)-(2i+2j+7k) \\  & =-3i-3j-3k \\  & =⟨-3,-3,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i+2j+k)-(2i+2j+7k) \\  & =3i-6k \\  & =⟨3,0,-6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(11i-4j+10k)-(2i+2j+7k) \\  & =9i-6j+3k \\  & =⟨9,-6,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & -3 & -3 \\ 3 & 0 & -6 \\ 9 & -6 & 3\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}0 & -6 \\ -6 & 3\end{aligned}|-(-3)\cdot |\begin{aligned}3 & -6 \\ 9 & 3\end{aligned}|+(-3)\cdot |\begin{aligned}3 & 0 \\ 9 & -6\end{aligned}| \\  & =-3(0\cdot 3-(-6)\cdot (-6))+3(3\cdot 3-9\cdot (-6))-3(3\cdot (-6)-9\cdot 0) \\  & =108+189+54 \\  & =351.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|351|=351.
$$

---

## Original q-73748

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,-1,0)$, $B(-1,2,-1)$, $C(1,1,2)$, and $D(3,-1,1).$

- $17$
- $7$
- $11$
- $1$
- $5$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+2j-k)-(2i-j) \\  & =-3i+3j-k \\  & =⟨-3,3,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+2k)-(2i-j) \\  & =-i+2j+2k \\  & =⟨-1,2,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-j+k)-(2i-j) \\  & =i+k \\  & =⟨1,0,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 3 & -1 \\ -1 & 2 & 2 \\ 1 & 0 & 1\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}2 & 2 \\ 0 & 1\end{aligned}|-3\cdot |\begin{aligned}-1 & 2 \\ 1 & 1\end{aligned}|+(-1)\cdot |\begin{aligned}-1 & 2 \\ 1 & 0\end{aligned}| \\  & =-3(2\cdot 1-0\cdot 2)-3((-1)\cdot 1-1\cdot 2)-((-1)\cdot 0-1\cdot 2) \\  & =-6+9+2 \\  & =5.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|\,5\,|=5.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(2,-1,0)$, $B(-1,2,-1)$, $C(1,1,2)$, and $D(3,-1,1).$

- $17$
- $7$
- $11$
- $1$
- $5$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+2j-k)-(2i-j) \\  & =-3i+3j-k \\  & =⟨-3,3,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i+j+2k)-(2i-j) \\  & =-i+2j+2k \\  & =⟨-1,2,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-j+k)-(2i-j) \\  & =i+k \\  & =⟨1,0,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & 3 & -1 \\ -1 & 2 & 2 \\ 1 & 0 & 1\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}2 & 2 \\ 0 & 1\end{aligned}|-3\cdot |\begin{aligned}-1 & 2 \\ 1 & 1\end{aligned}|+(-1)\cdot |\begin{aligned}-1 & 2 \\ 1 & 0\end{aligned}| \\  & =-3(2\cdot 1-0\cdot 2)-3((-1)\cdot 1-1\cdot 2)-((-1)\cdot 0-1\cdot 2) \\  & =-6+9+2 \\  & =5.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|\,5\,|=5.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(6,-3,1)$, $B(0,3,-1)$, $C(4,1,5)$, and $D(8,-3,3).$

- $136$
- $56$
- $88$
- $8$
- $40$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3j-k)-(6i-3j+k) \\  & =-6i+6j-2k \\  & =⟨-6,6,-2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i+j+5k)-(6i-3j+k) \\  & =-2i+4j+4k \\  & =⟨-2,4,4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-3j+3k)-(6i-3j+k) \\  & =2i+2k \\  & =⟨2,0,2⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-6 & 6 & -2 \\ -2 & 4 & 4 \\ 2 & 0 & 2\end{aligned}| \\  & =(-6)\cdot |\begin{aligned}4 & 4 \\ 0 & 2\end{aligned}|-6\cdot |\begin{aligned}-2 & 4 \\ 2 & 2\end{aligned}|+(-2)\cdot |\begin{aligned}-2 & 4 \\ 2 & 0\end{aligned}| \\  & =-6(4\cdot 2-0\cdot 4)-6((-2)\cdot 2-2\cdot 4)-2((-2)\cdot 0-2\cdot 4) \\  & =-48+72+16 \\  & =40.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|\,40\,|=40.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(8,-4,1)$, $B(-1,5,-2)$, $C(5,2,7)$, and $D(11,-4,4).$

- $459$
- $189$
- $297$
- $27$
- $135$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-i+5j-2k)-(8i-4j+k) \\  & =-9i+9j-3k \\  & =⟨-9,9,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i+2j+7k)-(8i-4j+k) \\  & =-3i+6j+6k \\  & =⟨-3,6,6⟩ \\ \overset{\to }{AD} & =d-a \\  & =(11i-4j+4k)-(8i-4j+k) \\  & =3i+3k \\  & =⟨3,0,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-9 & 9 & -3 \\ -3 & 6 & 6 \\ 3 & 0 & 3\end{aligned}| \\  & =(-9)\cdot |\begin{aligned}6 & 6 \\ 0 & 3\end{aligned}|-9\cdot |\begin{aligned}-3 & 6 \\ 3 & 3\end{aligned}|+(-3)\cdot |\begin{aligned}-3 & 6 \\ 3 & 0\end{aligned}| \\  & =-9(6\cdot 3-0\cdot 6)-9((-3)\cdot 3-3\cdot 6)-3((-3)\cdot 0-3\cdot 6) \\  & =-162+243+54 \\  & =135.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|\,135\,|=135.
$$

---

## Original q-73753

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(-2,1,1)$, $B(2,1,0)$, $C(1,-1,2)$, and $D(3,-2,-2).$

- $27$
- $37$
- $40$
- $42$
- $35$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+j)-(-2i+j+k) \\  & =4i-k \\  & =⟨4,0,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i-j+2k)-(-2i+j+k) \\  & =3i-2j+k \\  & =⟨3,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j-2k)-(-2i+j+k) \\  & =5i-3j-3k \\  & =⟨5,-3,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 0 & -1 \\ 3 & -2 & 1 \\ 5 & -3 & -3\end{aligned}| \\  & =4\cdot |\begin{aligned}-2 & 1 \\ -3 & -3\end{aligned}|-0\cdot |\begin{aligned}3 & 1 \\ 5 & -3\end{aligned}|+(-1)\cdot |\begin{aligned}3 & -2 \\ 5 & -3\end{aligned}| \\  & =4((-2)\cdot (-3)-1\cdot (-3))-0-(3\cdot (-3)-5\cdot (-2)) \\  & =36-1 \\  & =35.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|35|=35.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(-2,1,1)$, $B(2,1,0)$, $C(1,-1,2)$, and $D(3,-2,-2).$

- $27$
- $37$
- $40$
- $42$
- $35$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+j)-(-2i+j+k) \\  & =4i-k \\  & =⟨4,0,-1⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i-j+2k)-(-2i+j+k) \\  & =3i-2j+k \\  & =⟨3,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j-2k)-(-2i+j+k) \\  & =5i-3j-3k \\  & =⟨5,-3,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 0 & -1 \\ 3 & -2 & 1 \\ 5 & -3 & -3\end{aligned}| \\  & =4\cdot |\begin{aligned}-2 & 1 \\ -3 & -3\end{aligned}|-0\cdot |\begin{aligned}3 & 1 \\ 5 & -3\end{aligned}|+(-1)\cdot |\begin{aligned}3 & -2 \\ 5 & -3\end{aligned}| \\  & =4((-2)\cdot (-3)-1\cdot (-3))-0-(3\cdot (-3)-5\cdot (-2)) \\  & =36-1 \\  & =35.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|35|=35.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(-2,1,3)$, $B(6,1,1)$, $C(4,-3,5)$, and $D(8,-5,-3).$

- $216$
- $296$
- $320$
- $336$
- $280$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(6i+j+k)-(-2i+j+3k) \\  & =8i-2k \\  & =⟨8,0,-2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i-3j+5k)-(-2i+j+3k) \\  & =6i-4j+2k \\  & =⟨6,-4,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i-5j-3k)-(-2i+j+3k) \\  & =10i-6j-6k \\  & =⟨10,-6,-6⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}8 & 0 & -2 \\ 6 & -4 & 2 \\ 10 & -6 & -6\end{aligned}| \\  & =8\cdot |\begin{aligned}-4 & 2 \\ -6 & -6\end{aligned}|-0\cdot |\begin{aligned}6 & 2 \\ 10 & -6\end{aligned}|+(-2)\cdot |\begin{aligned}6 & -4 \\ 10 & -6\end{aligned}| \\  & =8((-4)\cdot (-6)-2\cdot (-6))-0-2(6\cdot (-6)-10\cdot (-4)) \\  & =288-8 \\  & =280.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|280|=280.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB}$, $\overset{\to }{AC}$ and $\overset{\to }{AD}$, given the points $A(-4,2,4)$, $B(8,2,1)$, $C(5,-4,7)$, and $D(11,-7,-5).$

- $729$
- $999$
- $1080$
- $1134$
- $945$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(8i+2j+k)-(-4i+2j+4k) \\  & =12i-3k \\  & =⟨12,0,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i-4j+7k)-(-4i+2j+4k) \\  & =9i-6j+3k \\  & =⟨9,-6,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(11i-7j-5k)-(-4i+2j+4k) \\  & =15i-9j-9k \\  & =⟨15,-9,-9⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}12 & 0 & -3 \\ 9 & -6 & 3 \\ 15 & -9 & -9\end{aligned}| \\  & =12\cdot |\begin{aligned}-6 & 3 \\ -9 & -9\end{aligned}|-0\cdot |\begin{aligned}9 & 3 \\ 15 & -9\end{aligned}|+(-3)\cdot |\begin{aligned}9 & -6 \\ 15 & -9\end{aligned}| \\  & =12((-6)\cdot (-9)-3\cdot (-9))-0-3(9\cdot (-9)-15\cdot (-6)) \\  & =972-27 \\  & =945.\end{aligned}
$$

Therefore, the volume of the corresponding parallelpiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|945|=945.
$$

---

## Original q-128482

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(3,0,1),$ $B(0,-1,3),$ $C(1,-2,2),$ and $D(2,2,1).$

- $7$
- $19$
- $13$
- $5$ (correct)
- $17$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-j+3k)-(3i+k) \\  & =-3i-j+2k \\  & =⟨-3,-1,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i-2j+2k)-(3i+k) \\  & =-2i-2j+k \\  & =⟨-2,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+2j+k)-(3i+k) \\  & =-i+2j \\  & =⟨-1,2,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & -1 & 2 \\ -2 & -2 & 1 \\ -1 & 2 & 0\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}-2 & 1 \\ 2 & 0\end{aligned}|-(-1)\cdot |\begin{aligned}-2 & 1 \\ -1 & 0\end{aligned}|+2\cdot |\begin{aligned}-2 & -2 \\ -1 & 2\end{aligned}| \\  & =-3((-2)\cdot 0-2\cdot 1)+((-2)\cdot 0-(-1)\cdot 1)+2((-2)\cdot 2-(-1)\cdot (-2)) \\  & =6+1-12 \\  & =-5.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-5|=5.
$$

### Normal replay (repairs listed in review metadata)

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(3,0,1),$ $B(0,-1,3),$ $C(1,-2,2),$ and $D(2,2,1).$

- $7$
- $19$
- $13$
- $5$ (correct)
- $17$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-j+3k)-(3i+k) \\  & =-3i-j+2k \\  & =⟨-3,-1,2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(i-2j+2k)-(3i+k) \\  & =-2i-2j+k \\  & =⟨-2,-2,1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+2j+k)-(3i+k) \\  & =-i+2j \\  & =⟨-1,2,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-3 & -1 & 2 \\ -2 & -2 & 1 \\ -1 & 2 & 0\end{aligned}| \\  & =(-3)\cdot |\begin{aligned}-2 & 1 \\ 2 & 0\end{aligned}|-(-1)\cdot |\begin{aligned}-2 & 1 \\ -1 & 0\end{aligned}|+2\cdot |\begin{aligned}-2 & -2 \\ -1 & 2\end{aligned}| \\  & =-3((-2)\cdot 0-2\cdot 1)+((-2)\cdot 0-(-1)\cdot 1)+2((-2)\cdot 2-(-1)\cdot (-2)) \\  & =6+1-12 \\  & =-5.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-5|=5.
$$

---

### Generated observed-domain variant: uniform dilation 2 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(8,-1,3),$ $B(2,-3,7),$ $C(4,-5,5),$ and $D(6,3,3).$

- $56$
- $152$
- $104$
- $40$ (correct)
- $136$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i-3j+7k)-(8i-j+3k) \\  & =-6i-2j+4k \\  & =⟨-6,-2,4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(4i-5j+5k)-(8i-j+3k) \\  & =-4i-4j+2k \\  & =⟨-4,-4,2⟩ \\ \overset{\to }{AD} & =d-a \\  & =(6i+3j+3k)-(8i-j+3k) \\  & =-2i+4j \\  & =⟨-2,4,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-6 & -2 & 4 \\ -4 & -4 & 2 \\ -2 & 4 & 0\end{aligned}| \\  & =(-6)\cdot |\begin{aligned}-4 & 2 \\ 4 & 0\end{aligned}|-(-2)\cdot |\begin{aligned}-4 & 2 \\ -2 & 0\end{aligned}|+4\cdot |\begin{aligned}-4 & -4 \\ -2 & 4\end{aligned}| \\  & =-6((-4)\cdot 0-4\cdot 2)+2((-4)\cdot 0-(-2)\cdot 2)+4((-4)\cdot 4-(-2)\cdot (-4)) \\  & =48+8-96 \\  & =-40.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-40|=40.
$$

---

### Generated observed-domain variant: uniform dilation 3 plus translation; scalar bank intent unresolved

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC}$ and $\overset{\to }{AD},$ given the points $A(11,-1,4),$ $B(2,-4,10),$ $C(5,-7,7),$ and $D(8,5,4).$

- $189$
- $513$
- $351$
- $135$ (correct)
- $459$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i-4j+10k)-(11i-j+4k) \\  & =-9i-3j+6k \\  & =⟨-9,-3,6⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i-7j+7k)-(11i-j+4k) \\  & =-6i-6j+3k \\  & =⟨-6,-6,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(8i+5j+4k)-(11i-j+4k) \\  & =-3i+6j \\  & =⟨-3,6,0⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-9 & -3 & 6 \\ -6 & -6 & 3 \\ -3 & 6 & 0\end{aligned}| \\  & =(-9)\cdot |\begin{aligned}-6 & 3 \\ 6 & 0\end{aligned}|-(-3)\cdot |\begin{aligned}-6 & 3 \\ -3 & 0\end{aligned}|+6\cdot |\begin{aligned}-6 & -6 \\ -3 & 6\end{aligned}| \\  & =-9((-6)\cdot 0-6\cdot 3)+3((-6)\cdot 0-(-3)\cdot 3)+6((-6)\cdot 6-(-3)\cdot (-6)) \\  & =162+27-324 \\  & =-135.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-135|=135.
$$

---

## Authored easy / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,3,2),$, $B(3,3,2),$, $C(2,6,2),$ and $D(0,4,5).$

- $54$
- $\frac{27}{2}$
- $27$ (correct)
- $52$
- $\frac{9}{2}$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+3j+2k)-(3j+2k) \\  & =3i \\  & =⟨3,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+6j+2k)-(3j+2k) \\  & =2i+3j \\  & =⟨2,3,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(4j+5k)-(3j+2k) \\  & =j+3k \\  & =⟨0,1,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 0 & 0 \\ 2 & 3 & 0 \\ 0 & 1 & 3\end{aligned}| \\  & =3\cdot |\begin{aligned}3 & 0 \\ 1 & 3\end{aligned}|-0\cdot |\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|+0\cdot |\begin{aligned}2 & 3 \\ 0 & 1\end{aligned}| \\  & =3\cdot (3\cdot 3-1\cdot 0)+0\cdot (2\cdot 3-0\cdot 0)+0\cdot (2\cdot 1-0\cdot 3) \\  & =3\cdot (9-0)+0\cdot (6-0)+0\cdot (2-0) \\  & =27+0+0 \\  & =27.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|27|=27.
$$

---

## Authored easy / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,2,3),$, $B(3,2,3),$, $C(5,4,3),$ and $D(2,4,4).$

- $2$ (correct)
- $\frac{1}{3}$
- $4$
- $1$
- $20$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+2j+3k)-(2i+2j+3k) \\  & =i \\  & =⟨1,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i+4j+3k)-(2i+2j+3k) \\  & =3i+2j \\  & =⟨3,2,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+4j+4k)-(2i+2j+3k) \\  & =2j+k \\  & =⟨0,2,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 0 & 0 \\ 3 & 2 & 0 \\ 0 & 2 & 1\end{aligned}| \\  & =1\cdot |\begin{aligned}2 & 0 \\ 2 & 1\end{aligned}|-0\cdot |\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|+0\cdot |\begin{aligned}3 & 2 \\ 0 & 2\end{aligned}| \\  & =1\cdot (2\cdot 1-2\cdot 0)+0\cdot (3\cdot 1-0\cdot 0)+0\cdot (3\cdot 2-0\cdot 2) \\  & =1\cdot (2-0)+0\cdot (3-0)+0\cdot (6-0) \\  & =2+0+0 \\  & =2.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|2|=2.
$$

---

## Authored easy / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(1,2,0),$, $B(2,2,0),$, $C(2,5,0),$ and $D(1,5,1).$

$V=${{field-1}}

- $3$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(2i+2j)-(i+2j) \\  & =i \\  & =⟨1,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(2i+5j)-(i+2j) \\  & =i+3j \\  & =⟨1,3,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(i+5j+k)-(i+2j) \\  & =3j+k \\  & =⟨0,3,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 0 & 0 \\ 1 & 3 & 0 \\ 0 & 3 & 1\end{aligned}| \\  & =1\cdot |\begin{aligned}3 & 0 \\ 3 & 1\end{aligned}|-0\cdot |\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|+0\cdot |\begin{aligned}1 & 3 \\ 0 & 3\end{aligned}| \\  & =1\cdot (3\cdot 1-3\cdot 0)+0\cdot (1\cdot 1-0\cdot 0)+0\cdot (1\cdot 3-0\cdot 3) \\  & =1\cdot (3-0)+0\cdot (1-0)+0\cdot (3-0) \\  & =3+0+0 \\  & =3.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|3|=3.
$$

---

## Authored easy / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,2,3),$, $B(3,2,3),$, $C(5,4,3),$ and $D(2,4,4).$

$V=${{field-1}}

- $2$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i+2j+3k)-(2i+2j+3k) \\  & =i \\  & =⟨1,0,0⟩ \\ \overset{\to }{AC} & =c-a \\  & =(5i+4j+3k)-(2i+2j+3k) \\  & =3i+2j \\  & =⟨3,2,0⟩ \\ \overset{\to }{AD} & =d-a \\  & =(2i+4j+4k)-(2i+2j+3k) \\  & =2j+k \\  & =⟨0,2,1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}1 & 0 & 0 \\ 3 & 2 & 0 \\ 0 & 2 & 1\end{aligned}| \\  & =1\cdot |\begin{aligned}2 & 0 \\ 2 & 1\end{aligned}|-0\cdot |\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|+0\cdot |\begin{aligned}3 & 2 \\ 0 & 2\end{aligned}| \\  & =1\cdot (2\cdot 1-2\cdot 0)+0\cdot (3\cdot 1-0\cdot 0)+0\cdot (3\cdot 2-0\cdot 2) \\  & =1\cdot (2-0)+0\cdot (3-0)+0\cdot (6-0) \\  & =2+0+0 \\  & =2.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|2|=2.
$$

---

## Authored moderate / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,0,3),$, $B(3,0,0),$, $C(-2,-2,6),$ and $D(3,-2,2).$

- $24$
- $1$
- $3$
- $12$
- $6$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i)-(3k) \\  & =3i-3k \\  & =⟨3,0,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2j+6k)-(3k) \\  & =-2i-2j+3k \\  & =⟨-2,-2,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j+2k)-(3k) \\  & =3i-2j-k \\  & =⟨3,-2,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 0 & -3 \\ -2 & -2 & 3 \\ 3 & -2 & -1\end{aligned}| \\  & =3\cdot |\begin{aligned}-2 & 3 \\ -2 & -1\end{aligned}|-0\cdot |\begin{aligned}-2 & 3 \\ 3 & -1\end{aligned}|+(-3)\cdot |\begin{aligned}-2 & -2 \\ 3 & -2\end{aligned}| \\  & =3\cdot ((-2)\cdot (-1)-(-2)\cdot 3)+0\cdot ((-2)\cdot (-1)-3\cdot 3)+(-3)\cdot ((-2)\cdot (-2)-3\cdot (-2)) \\  & =3\cdot (2-(-6))+0\cdot (2-9)+(-3)\cdot (4-(-6)) \\  & =24+0+(-30) \\  & =-6.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-6|=6.
$$

---

## Authored moderate / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(3,3,3),$, $B(7,3,1),$, $C(6,-1,0),$ and $D(5,7,7).$

- $\frac{28}{3}$
- $56$ (correct)
- $112$
- $28$
- $128$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(7i+3j+k)-(3i+3j+3k) \\  & =4i-2k \\  & =⟨4,0,-2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(6i-j)-(3i+3j+3k) \\  & =3i-4j-3k \\  & =⟨3,-4,-3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+7j+7k)-(3i+3j+3k) \\  & =2i+4j+4k \\  & =⟨2,4,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 0 & -2 \\ 3 & -4 & -3 \\ 2 & 4 & 4\end{aligned}| \\  & =4\cdot |\begin{aligned}-4 & -3 \\ 4 & 4\end{aligned}|-0\cdot |\begin{aligned}3 & -3 \\ 2 & 4\end{aligned}|+(-2)\cdot |\begin{aligned}3 & -4 \\ 2 & 4\end{aligned}| \\  & =4\cdot ((-4)\cdot 4-4\cdot (-3))+0\cdot (3\cdot 4-2\cdot (-3))+(-2)\cdot (3\cdot 4-2\cdot (-4)) \\  & =4\cdot ((-16)-(-12))+0\cdot (12-(-6))+(-2)\cdot (12-(-8)) \\  & =(-16)+0+(-40) \\  & =-56.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-56|=56.
$$

---

## Authored moderate / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(0,0,3),$, $B(3,0,0),$, $C(-2,-2,6),$ and $D(3,-2,2).$

$V=${{field-1}}

- $6$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(3i)-(3k) \\  & =3i-3k \\  & =⟨3,0,-3⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-2i-2j+6k)-(3k) \\  & =-2i-2j+3k \\  & =⟨-2,-2,3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(3i-2j+2k)-(3k) \\  & =3i-2j-k \\  & =⟨3,-2,-1⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}3 & 0 & -3 \\ -2 & -2 & 3 \\ 3 & -2 & -1\end{aligned}| \\  & =3\cdot |\begin{aligned}-2 & 3 \\ -2 & -1\end{aligned}|-0\cdot |\begin{aligned}-2 & 3 \\ 3 & -1\end{aligned}|+(-3)\cdot |\begin{aligned}-2 & -2 \\ 3 & -2\end{aligned}| \\  & =3\cdot ((-2)\cdot (-1)-(-2)\cdot 3)+0\cdot ((-2)\cdot (-1)-3\cdot 3)+(-3)\cdot ((-2)\cdot (-2)-3\cdot (-2)) \\  & =3\cdot (2-(-6))+0\cdot (2-9)+(-3)\cdot (4-(-6)) \\  & =24+0+(-30) \\  & =-6.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-6|=6.
$$

---

## Authored moderate / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(3,3,3),$, $B(7,3,1),$, $C(6,-1,0),$ and $D(5,7,7).$

$V=${{field-1}}

- $56$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(7i+3j+k)-(3i+3j+3k) \\  & =4i-2k \\  & =⟨4,0,-2⟩ \\ \overset{\to }{AC} & =c-a \\  & =(6i-j)-(3i+3j+3k) \\  & =3i-4j-3k \\  & =⟨3,-4,-3⟩ \\ \overset{\to }{AD} & =d-a \\  & =(5i+7j+7k)-(3i+3j+3k) \\  & =2i+4j+4k \\  & =⟨2,4,4⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}4 & 0 & -2 \\ 3 & -4 & -3 \\ 2 & 4 & 4\end{aligned}| \\  & =4\cdot |\begin{aligned}-4 & -3 \\ 4 & 4\end{aligned}|-0\cdot |\begin{aligned}3 & -3 \\ 2 & 4\end{aligned}|+(-2)\cdot |\begin{aligned}3 & -4 \\ 2 & 4\end{aligned}| \\  & =4\cdot ((-4)\cdot 4-4\cdot (-3))+0\cdot (3\cdot 4-2\cdot (-3))+(-2)\cdot (3\cdot 4-2\cdot (-4)) \\  & =4\cdot ((-16)-(-12))+0\cdot (12-(-6))+(-2)\cdot (12-(-8)) \\  & =(-16)+0+(-40) \\  & =-56.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-56|=56.
$$

---

## Authored hard / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,-3,0),$, $B(-3,-5,-5),$, $C(-1,1,-1),$ and $D(-3,-1,-3).$

- $2$
- $12$ (correct)
- $62$
- $58$
- $20$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-3i-5j-5k)-(2i-3j) \\  & =-5i-2j-5k \\  & =⟨-5,-2,-5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i+j-k)-(2i-3j) \\  & =-3i+4j-k \\  & =⟨-3,4,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-3i-j-3k)-(2i-3j) \\  & =-5i+2j-3k \\  & =⟨-5,2,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-5 & -2 & -5 \\ -3 & 4 & -1 \\ -5 & 2 & -3\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}4 & -1 \\ 2 & -3\end{aligned}|-(-2)\cdot |\begin{aligned}-3 & -1 \\ -5 & -3\end{aligned}|+(-5)\cdot |\begin{aligned}-3 & 4 \\ -5 & 2\end{aligned}| \\  & =(-5)\cdot (4\cdot (-3)-2\cdot (-1))+2\cdot ((-3)\cdot (-3)-(-5)\cdot (-1))+(-5)\cdot ((-3)\cdot 2-(-5)\cdot 4) \\  & =(-5)\cdot ((-12)-(-2))+2\cdot (9-5)+(-5)\cdot ((-6)-(-20)) \\  & =50+8+(-70) \\  & =-12.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-12|=12.
$$

---

## Authored hard / radio variant

Calculate the volume of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(-2,-2,2),$, $B(0,1,6),$, $C(0,-5,6),$ and $D(0,-7,5).$

- $6$
- $28$
- $2$
- $12$ (correct)
- $10$

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(j+6k)-(-2i-2j+2k) \\  & =2i+3j+4k \\  & =⟨2,3,4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5j+6k)-(-2i-2j+2k) \\  & =2i-3j+4k \\  & =⟨2,-3,4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-7j+5k)-(-2i-2j+2k) \\  & =2i-5j+3k \\  & =⟨2,-5,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 3 & 4 \\ 2 & -3 & 4 \\ 2 & -5 & 3\end{aligned}| \\  & =2\cdot |\begin{aligned}-3 & 4 \\ -5 & 3\end{aligned}|-3\cdot |\begin{aligned}2 & 4 \\ 2 & 3\end{aligned}|+4\cdot |\begin{aligned}2 & -3 \\ 2 & -5\end{aligned}| \\  & =2\cdot ((-3)\cdot 3-(-5)\cdot 4)+(-3)\cdot (2\cdot 3-2\cdot 4)+4\cdot (2\cdot (-5)-2\cdot (-3)) \\  & =2\cdot ((-9)-(-20))+(-3)\cdot (6-8)+4\cdot ((-10)-(-6)) \\  & =22+6+(-16) \\  & =12.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|12|=12.
$$

---

## Authored hard / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(2,-3,0),$, $B(-3,-5,-5),$, $C(-1,1,-1),$ and $D(-3,-1,-3).$

$V=${{field-1}}

- $12$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-3i-5j-5k)-(2i-3j) \\  & =-5i-2j-5k \\  & =⟨-5,-2,-5⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-i+j-k)-(2i-3j) \\  & =-3i+4j-k \\  & =⟨-3,4,-1⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-3i-j-3k)-(2i-3j) \\  & =-5i+2j-3k \\  & =⟨-5,2,-3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}-5 & -2 & -5 \\ -3 & 4 & -1 \\ -5 & 2 & -3\end{aligned}| \\  & =(-5)\cdot |\begin{aligned}4 & -1 \\ 2 & -3\end{aligned}|-(-2)\cdot |\begin{aligned}-3 & -1 \\ -5 & -3\end{aligned}|+(-5)\cdot |\begin{aligned}-3 & 4 \\ -5 & 2\end{aligned}| \\  & =(-5)\cdot (4\cdot (-3)-2\cdot (-1))+2\cdot ((-3)\cdot (-3)-(-5)\cdot (-1))+(-5)\cdot ((-3)\cdot 2-(-5)\cdot 4) \\  & =(-5)\cdot ((-12)-(-2))+2\cdot (9-5)+(-5)\cdot ((-6)-(-20)) \\  & =50+8+(-70) \\  & =-12.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|-12|=12.
$$

---

## Authored hard / blank variant

Calculate the volume $V$ of the parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD},$ given the points $A(-2,-2,2),$, $B(0,1,6),$, $C(0,-5,6),$ and $D(0,-7,5).$

$V=${{field-1}}

- $12$ (correct)

First, we find the displacement vectors $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ that span the parallelepiped:

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(j+6k)-(-2i-2j+2k) \\  & =2i+3j+4k \\  & =⟨2,3,4⟩ \\ \overset{\to }{AC} & =c-a \\  & =(-5j+6k)-(-2i-2j+2k) \\  & =2i-3j+4k \\  & =⟨2,-3,4⟩ \\ \overset{\to }{AD} & =d-a \\  & =(-7j+5k)-(-2i-2j+2k) \\  & =2i-5j+3k \\  & =⟨2,-5,3⟩\end{aligned}
$$

Now, to find the volume of the parallelepiped, we need to take the absolute value of the triple product of the above vectors.

Computing the triple product, we have

$$
\begin{aligned}\overset{\to }{AB}\cdot (\overset{\to }{AC}\times \overset{\to }{AD}) & =|\begin{aligned}2 & 3 & 4 \\ 2 & -3 & 4 \\ 2 & -5 & 3\end{aligned}| \\  & =2\cdot |\begin{aligned}-3 & 4 \\ -5 & 3\end{aligned}|-3\cdot |\begin{aligned}2 & 4 \\ 2 & 3\end{aligned}|+4\cdot |\begin{aligned}2 & -3 \\ 2 & -5\end{aligned}| \\  & =2\cdot ((-3)\cdot 3-(-5)\cdot 4)+(-3)\cdot (2\cdot 3-2\cdot 4)+4\cdot (2\cdot (-5)-2\cdot (-3)) \\  & =2\cdot ((-9)-(-20))+(-3)\cdot (6-8)+4\cdot ((-10)-(-6)) \\  & =22+6+(-16) \\  & =12.\end{aligned}
$$

Therefore, the volume of the corresponding parallelepiped spanned by $\overset{\to }{AB},$ $\overset{\to }{AC},$ and $\overset{\to }{AD}$ is

$$
V=|12|=12.
$$
