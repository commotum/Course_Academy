# Singular matrices private draft review

Current basis2484 checkbox records; historical1356 radio evidence is separate and ineligible.

## current source parameter replay q-128490

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $det(M)=10$
- **II.** $det(M)=-5$
- **III.** $M$ is a singular matrix

$$
M=\begin{bmatrix}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{bmatrix}
$$

Correct selections: III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =\begin{vmatrix}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{vmatrix} \\  & =\sqrt{5}\begin{vmatrix}3 & 5 \\ 3 & 4\end{vmatrix}+0\begin{vmatrix}0 & 5 \\ - 3 \sqrt{5} & 4\end{vmatrix}+\frac{1}{3}\begin{vmatrix}0 & 3 \\ - 3 \sqrt{5} & 3\end{vmatrix} \\  & =\sqrt{5}(12-15)+0+\frac{1}{3}(0+9 \sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9 \sqrt{5} \\  & =- 3 \sqrt{5}+3 \sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

---

## changed parameters q-128490

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $det(Q)=\frac{16}{3}$
- **II.** $det(Q)=1$
- **III.** $Q$ is a singular matrix

$$
Q=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(Q)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

---

## changed parameters q-128490

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=\frac{32}{5}$
- **II.** $det(E)=- \sqrt{7} - \frac{3}{5}$
- **III.** $E$ is a singular matrix

$$
E=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(E)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

---

## current source parameter replay q-9838

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is a singular matrix
- **III.** $det(F)=-2$

$$
F=\begin{bmatrix}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{bmatrix}
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =\begin{vmatrix}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{vmatrix} \\  & =0\begin{vmatrix}4 & 5 \\ 7 & 8\end{vmatrix}+(-1)\begin{vmatrix}3 & 5 \\ 6 & 8\end{vmatrix}+2\begin{vmatrix}3 & 4 \\ 6 & 7\end{vmatrix} \\  & =0+(-1)(24-30)+2(21-24) \\  & =(-1)\cdot (-6)+2\cdot (-3) \\  & =6-6 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

---

## changed parameters q-9838

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $det(T)=21$
- **II.** $T$ is a singular matrix
- **III.** $det(T)=36$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-9838

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $det(P)=4$
- **II.** $P$ is a singular matrix
- **III.** $det(P)=20$

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

---

## current source parameter replay q-128474

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $det(Q)=-5$
- **II.** $det(Q)=1$
- **III.** $Q$ is **not** a singular matrix

$$
Q=\begin{bmatrix}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{bmatrix}
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =\begin{vmatrix}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{vmatrix} \\  & =1\begin{vmatrix}3 & 1 \\ 5 & 3\end{vmatrix}+(-1)\begin{vmatrix}2 & 1 \\ 3 & 3\end{vmatrix}+(-1)\begin{vmatrix}2 & 3 \\ 3 & 5\end{vmatrix} \\  & =1(9-5)+(-1)(6-3)+(-1)(10-9) \\  & =1\cdot 4+(-1)\cdot 3+(-1)\cdot 1 \\  & =4-3-1 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, none of the statements are true.

---

## changed parameters q-128474

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $det(T)=21$
- **II.** $det(T)=36$
- **III.** $T$ is **not** a singular matrix

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, none of the statements are true.

---

## changed parameters q-128474

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $det(P)=4$
- **II.** $det(P)=20$
- **III.** $P$ is **not** a singular matrix

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## current source parameter replay q-128476

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=-30$

$$
T=\begin{bmatrix}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =\begin{vmatrix}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{vmatrix} \\  & =1\begin{vmatrix}1 & 1 \\ 3 & 1\end{vmatrix}+(-3)\begin{vmatrix}2 & 1 \\ 1 & 1\end{vmatrix}+(-5)\begin{vmatrix}2 & 1 \\ 1 & 3\end{vmatrix} \\  & =1(1-3)+(-3)(2-1)+(-5)(6-1) \\  & =1\cdot (-2)+(-3)\cdot 1+(-5)\cdot 5 \\  & =-2-3-25 \\  & =-30\end{aligned}
$$

 

Since $det(T)=-30\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## changed parameters q-128476

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=21$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement I is true.

---

## changed parameters q-128476

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=4$

$$
F=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(F)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## current source parameter replay q-128484

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

$$
R=\begin{bmatrix}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{bmatrix}
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =\begin{vmatrix}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{vmatrix} \\  & =2\begin{vmatrix}0 & -1 \\ \sqrt{2} & 4\end{vmatrix}+(- \sqrt{2})\begin{vmatrix}\frac{1}{2} & -1 \\ 1 & 4\end{vmatrix}+2\begin{vmatrix}\frac{1}{2} & 0 \\ 1 & \sqrt{2}\end{vmatrix} \\  & =2(0+\sqrt{2})+(- \sqrt{2})(2+1)+2(\frac{\sqrt{2}}{2}+0) \\  & =2\cdot \sqrt{2}+(- \sqrt{2})\cdot 3+2\cdot \frac{\sqrt{2}}{2} \\  & =2 \sqrt{2}- 3 \sqrt{2}+\sqrt{2} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

---

## changed parameters q-128484

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $Q$ is a singular matrix
- **II.** $det(Q)=\frac{16}{3}$
- **III.** $det(Q)=1$

$$
Q=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(Q)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## changed parameters q-128484

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=\frac{32}{5}$
- **III.** $det(E)=- \sqrt{7} - \frac{3}{5}$

$$
E=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(E)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## current source parameter replay q-38179

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=-2$

$$
E=\begin{bmatrix}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =\begin{vmatrix}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{vmatrix} \\  & =\frac{2}{3}\begin{vmatrix}5 & 6 \\ 7 & 8\end{vmatrix}+(-3)\begin{vmatrix}\frac{2}{3} & 6 \\ \frac{2}{3} & 8\end{vmatrix}+4\begin{vmatrix}\frac{2}{3} & 5 \\ \frac{2}{3} & 7\end{vmatrix} \\  & =\frac{2}{3}(40-42)+(-3)(\frac{16}{3}-4)+4(\frac{14}{3}- \frac{10}{3}) \\  & =\frac{2}{3}\cdot (-2)+(-3)\cdot \frac{4}{3}+4\cdot \frac{4}{3} \\  & =- \frac{4}{3}-4+\frac{16}{3} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

---

## changed parameters q-38179

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=\frac{16}{3}$

$$
T=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(T)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## changed parameters q-38179

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is a singular matrix
- **II.** $N$ is **not** a singular matrix
- **III.** $det(N)=\frac{32}{5}$

$$
N=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(N)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## current source parameter replay q-38182

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $Q$ is **not** a singular matrix
- **II.** $Q$ is a singular matrix
- **III.** $det(Q)=-5$

$$
Q=\begin{bmatrix}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =\begin{vmatrix}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{vmatrix} \\  & =0\begin{vmatrix}4 & 7 \\ 5 & 8\end{vmatrix}+(-3)\begin{vmatrix}1 & 7 \\ 2 & 8\end{vmatrix}+6\begin{vmatrix}1 & 4 \\ 2 & 5\end{vmatrix} \\  & =0+(-3)(8-14)+6(5-8) \\  & =(-3)\cdot (-6)+6\cdot (-3) \\  & =18-18 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-38182

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is **not** a singular matrix
- **II.** $T$ is a singular matrix
- **III.** $det(T)=21$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-38182

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is **not** a singular matrix
- **II.** $F$ is a singular matrix
- **III.** $det(F)=4$

$$
F=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(F)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## current source parameter replay q-69834

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $M$ is a singular matrix
- **II.** $det(M)=1$
- **III.** $det(M)=0$

$$
M=\begin{bmatrix}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =\begin{vmatrix}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{vmatrix} \\  & =1\begin{vmatrix}2 & 3 \\ 4 & -2\end{vmatrix}+2\begin{vmatrix}1 & 3 \\ -2 & -2\end{vmatrix}+1\begin{vmatrix}1 & 2 \\ -2 & 4\end{vmatrix} \\  & =1(-4-12)+2(-2+6)+1(4+4) \\  & =1\cdot (-16)+2\cdot 4+1\cdot 8 \\  & =-16+8+8 \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

---

## changed parameters q-69834

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=21$
- **III.** $det(T)=36$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement I is true.

---

## changed parameters q-69834

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $P$ is a singular matrix
- **II.** $det(P)=4$
- **III.** $det(P)=20$

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## current source parameter replay q-77477

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is **not** a singular matrix

- **II.** $S$ is a singular matrix

- **III.** $det(S)=\sqrt{3}$

$$
S=\begin{bmatrix}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =\begin{vmatrix}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{vmatrix} \\  & =1\begin{vmatrix}\sqrt{3} & -1 \\ 4 & - \sqrt{3}\end{vmatrix}+(-2)\begin{vmatrix}2 & -1 \\ \sqrt{3} & - \sqrt{3}\end{vmatrix}+0\begin{vmatrix}2 & \sqrt{3} \\ \sqrt{3} & 4\end{vmatrix} \\  & =1(-3+4)+(-2)(- 2 \sqrt{3}+\sqrt{3})+0 \\  & =(-3+4)+(-2)\cdot (- \sqrt{3}) \\  & =1 + 2 \sqrt{3}\end{aligned}
$$

Since $det(S)=1 + 2 \sqrt{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

---

## changed parameters q-77477

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is **not** a singular matrix

- **II.** $T$ is a singular matrix

- **III.** $det(T)=\frac{16}{3}$

$$
T=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(T)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## changed parameters q-77477

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix

- **II.** $N$ is a singular matrix

- **III.** $det(N)=\frac{32}{5}$

$$
N=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(N)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## current source parameter replay q-77478

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

$$
R=\begin{bmatrix}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{bmatrix}
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =\begin{vmatrix}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{vmatrix} \\  & =\frac{3}{5}\begin{vmatrix}2 & 3 \\ \frac{1}{2} & 1\end{vmatrix}+(- \frac{2}{5})\begin{vmatrix}1 & 3 \\ 0 & 1\end{vmatrix}+\frac{1}{5}\begin{vmatrix}1 & 2 \\ 0 & \frac{1}{2}\end{vmatrix} \\  & =\frac{3}{5}(2- \frac{3}{2})+(- \frac{2}{5})(1+0)+\frac{1}{5}(\frac{1}{2}+0) \\  & =\frac{3}{5}\cdot \frac{1}{2}+(- \frac{2}{5})\cdot 1+\frac{1}{5}\cdot \frac{1}{2} \\  & =\frac{3}{10}- \frac{2}{5}+\frac{1}{10} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

---

## changed parameters q-77478

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $Q$ is a singular matrix
- **II.** $det(Q)=\frac{16}{3}$
- **III.** $det(Q)=1$

$$
Q=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(Q)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## changed parameters q-77478

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=\frac{32}{5}$
- **III.** $det(E)=- \sqrt{7} - \frac{3}{5}$

$$
E=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(E)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## current source parameter replay q-77479

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $P$ is **not** a singular matrix
- **II.** $P$ is a singular matrix
- **III.** $det(P)=- \frac{1}{2}$

$$
P=\begin{bmatrix}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{vmatrix} \\  & =\frac{1}{2}\begin{vmatrix}2 & \frac{1}{2} \\ 0 & -1\end{vmatrix}+(-1)\begin{vmatrix}\frac{1}{2} & \frac{1}{2} \\ -1 & -1\end{vmatrix}+\frac{1}{2}\begin{vmatrix}\frac{1}{2} & 2 \\ -1 & 0\end{vmatrix} \\  & =\frac{1}{2}(-2+0)+(-1)(- \frac{1}{2}+\frac{1}{2})+\frac{1}{2}(0+2) \\  & =\frac{1}{2}\cdot (-2)+(-1)\cdot 0+\frac{1}{2}\cdot 2 \\  & =-1+1 \\  & =0\end{aligned}
$$

Since $det(P)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-77479

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is **not** a singular matrix
- **II.** $T$ is a singular matrix
- **III.** $det(T)=\frac{16}{3}$

$$
T=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(T)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## changed parameters q-77479

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix
- **II.** $N$ is a singular matrix
- **III.** $det(N)=\frac{32}{5}$

$$
N=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(N)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## current source parameter replay q-9835

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $det(D)=1$
- **II.** $D$ is a singular matrix
- **III.** $det(D)=0$

$$
D=\begin{bmatrix}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =\begin{vmatrix}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{vmatrix} \\  & =1\begin{vmatrix}4 & 5 \\ 6 & 7\end{vmatrix}+(-2)\begin{vmatrix}1 & 5 \\ 1 & 7\end{vmatrix}+3\begin{vmatrix}1 & 4 \\ 1 & 6\end{vmatrix} \\  & =1(28-30)+(-2)(7-5)+3(6-4) \\  & =1\cdot (-2)+(-2)\cdot 2+3\cdot 2 \\  & =-2-4+6 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

---

## changed parameters q-9835

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $det(T)=21$
- **II.** $T$ is a singular matrix
- **III.** $det(T)=36$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-9835

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $det(P)=4$
- **II.** $P$ is a singular matrix
- **III.** $det(P)=20$

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

---

## current source parameter replay q-128478

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=-7$
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=-2$

$$
F=\begin{bmatrix}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =\begin{vmatrix}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{vmatrix} \\  & =2\begin{vmatrix}2 & 1 \\ 3 & 1\end{vmatrix}+(-8)\begin{vmatrix}-1 & 1 \\ 5 & 1\end{vmatrix}+3\begin{vmatrix}-1 & 2 \\ 5 & 3\end{vmatrix} \\  & =2(2-3)+(-8)(-1-5)+3(-3-10) \\  & =2\cdot (-1)+(-8)\cdot (-6)+3\cdot (-13) \\  & =-2+48-39 \\  & =7\end{aligned}
$$

Since $det(F)=7$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## changed parameters q-128478

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $det(T)=21$
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=36$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, none of the statements are true.

---

## changed parameters q-128478

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $det(P)=4$
- **II.** $P$ is **not** a singular matrix
- **III.** $det(P)=20$

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and II are true.

---

## current source parameter replay q-128480

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $D$ is a singular matrix
- **II.** $det(D)=1$
- **III.** $det(D)=0$

$$
D=\begin{bmatrix}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =\begin{vmatrix}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{vmatrix} \\  & =2\begin{vmatrix}2 & 3 \\ 5 & 2\end{vmatrix}+3\begin{vmatrix}-1 & 3 \\ -3 & 2\end{vmatrix}+1\begin{vmatrix}-1 & 2 \\ -3 & 5\end{vmatrix} \\  & =2(4-15)+3(-2+9)+1(-5+6) \\  & =2\cdot (-11)+3\cdot 7+1\cdot 1 \\  & =-22+21+1 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

---

## changed parameters q-128480

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=21$
- **III.** $det(T)=36$

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement I is true.

---

## changed parameters q-128480

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $P$ is a singular matrix
- **II.** $det(P)=4$
- **III.** $det(P)=20$

$$
P=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(P)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## current source parameter replay q-128491

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is a singular matrix
- **II.** $S$ is **not** a singular matrix
- **III.** $det(S)=5 + 2 \sqrt{7}$

$$
S=\begin{bmatrix}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =\begin{vmatrix}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{vmatrix} \\  & =2 \sqrt{7}\begin{vmatrix}2 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 5 & \sqrt{7}\end{vmatrix}+\frac{1}{2}\begin{vmatrix}- \sqrt{7} & 2 \\ 5 & 0\end{vmatrix} \\  & =2 \sqrt{7}(2 \sqrt{7}+0)+0+\frac{1}{2}(0-10) \\  & =2 \sqrt{7}\cdot 2 \sqrt{7}+\frac{1}{2}\cdot (-10) \\  & =28-5 \\  & =23\end{aligned}
$$

Since $det(S)=23\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

---

## changed parameters q-128491

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=\frac{16}{3}$

$$
T=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(T)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## changed parameters q-128491

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is a singular matrix
- **II.** $N$ is **not** a singular matrix
- **III.** $det(N)=\frac{32}{5}$

$$
N=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(N)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## current source parameter replay q-38187

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix
- **II.** $N$ is a singular matrix
- **III.** $det(N)=-1$

$$
N=\begin{bmatrix}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{vmatrix} \\  & =\frac{1}{7}\begin{vmatrix}4 & - \frac{1}{7} \\ 5 & - \frac{1}{7}\end{vmatrix}+(-3)\begin{vmatrix}\frac{1}{7} & - \frac{1}{7} \\ \frac{1}{7} & - \frac{1}{7}\end{vmatrix}+(- \frac{1}{7})\begin{vmatrix}\frac{1}{7} & 4 \\ \frac{1}{7} & 5\end{vmatrix} \\  & =\frac{1}{7}(- \frac{4}{7}+\frac{5}{7})+(-3)(- \frac{1}{49}+\frac{1}{49})+(- \frac{1}{7})(\frac{5}{7}- \frac{4}{7}) \\  & =\frac{1}{7}\cdot \frac{1}{7}+(-3)\cdot 0+(- \frac{1}{7})\cdot \frac{1}{7} \\  & =\frac{1}{49}- \frac{1}{49} \\  & =0\end{aligned}
$$

Since $det(N)=0$, the matrix is singular. 

Therefore, only statement II is true.

---

## changed parameters q-38187

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is **not** a singular matrix
- **II.** $T$ is a singular matrix
- **III.** $det(T)=\frac{16}{3}$

$$
T=\begin{bmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}-1 & \frac{1}{3} & - \frac{2}{3} \\ -3 & 0 & 4 \\ 1 & 0 & 4\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ 0 & 4\end{vmatrix}+(- \frac{1}{3})\begin{vmatrix}-3 & 4 \\ 1 & 4\end{vmatrix}+(- \frac{2}{3})\begin{vmatrix}-3 & 0 \\ 1 & 0\end{vmatrix} \\  & =(-1)(0+0)+(- \frac{1}{3})(-12-4)+(- \frac{2}{3})(0+0) \\  & =(-1)\cdot 0+(- \frac{1}{3})\cdot (-16)+(- \frac{2}{3})\cdot 0 \\  & =\frac{16}{3} \\  & =\frac{16}{3}\end{aligned}
$$

Since $det(T)=\frac{16}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## changed parameters q-38187

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix
- **II.** $N$ is a singular matrix
- **III.** $det(N)=\frac{32}{5}$

$$
N=\begin{bmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =\begin{vmatrix}- \sqrt{7} & 0 & - \frac{1}{5} \\ - \sqrt{7} & -1 & 0 \\ 3 & 0 & \sqrt{7}\end{vmatrix} \\  & =(- \sqrt{7})\begin{vmatrix}-1 & 0 \\ 0 & \sqrt{7}\end{vmatrix}+0\begin{vmatrix}- \sqrt{7} & 0 \\ 3 & \sqrt{7}\end{vmatrix}+(- \frac{1}{5})\begin{vmatrix}- \sqrt{7} & -1 \\ 3 & 0\end{vmatrix} \\  & =(- \sqrt{7})(- \sqrt{7}+0)+0+(- \frac{1}{5})(0+3) \\  & =(- \sqrt{7})\cdot (- \sqrt{7})+(- \frac{1}{5})\cdot 3 \\  & =7- \frac{3}{5} \\  & =\frac{32}{5}\end{aligned}
$$

Since $det(N)=\frac{32}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

---

## current source parameter replay q-69835

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=-3$
- **III.** $T$ is **not** a singular matrix

$$
T=\begin{bmatrix}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{bmatrix}
$$

Correct selections: III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =\begin{vmatrix}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{vmatrix} \\  & =4\begin{vmatrix}2 & 3 \\ -1 & 1\end{vmatrix}+(-2)\begin{vmatrix}1 & 3 \\ -2 & 1\end{vmatrix}+(-1)\begin{vmatrix}1 & 2 \\ -2 & -1\end{vmatrix} \\  & =4(2+3)+(-2)(1+6)+(-1)(-1+4) \\  & =4\cdot 5+(-2)\cdot 7+(-1)\cdot 3 \\  & =20-14-3 \\  & =3\end{aligned}
$$

 

Since $det(T)=3\ne 0$, the matrix is **not** singular. 

Therefore, only statement III is true.

---

## changed parameters q-69835

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=21$
- **III.** $T$ is **not** a singular matrix

$$
T=\begin{bmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{bmatrix}
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}3 & -3 & -1 \\ -3 & 1 & -2 \\ -3 & 3 & 1\end{vmatrix} \\  & =3\begin{vmatrix}1 & -2 \\ 3 & 1\end{vmatrix}+3\begin{vmatrix}-3 & -2 \\ -3 & 1\end{vmatrix}+(-1)\begin{vmatrix}-3 & 1 \\ -3 & 3\end{vmatrix} \\  & =3(1+6)+3(-3-6)+(-1)(-9+3) \\  & =3\cdot 7+3\cdot (-9)+(-1)\cdot (-6) \\  & =21-27+6 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statement I is true.

---

## changed parameters q-69835

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=4$
- **III.** $F$ is **not** a singular matrix

$$
F=\begin{bmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{bmatrix}
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =\begin{vmatrix}-1 & 3 & 4 \\ 0 & 0 & 4 \\ 1 & -2 & 0\end{vmatrix} \\  & =(-1)\begin{vmatrix}0 & 4 \\ -2 & 0\end{vmatrix}+(-3)\begin{vmatrix}0 & 4 \\ 1 & 0\end{vmatrix}+4\begin{vmatrix}0 & 0 \\ 1 & -2\end{vmatrix} \\  & =(-1)(0+8)+(-3)(0-4)+4(0+0) \\  & =(-1)\cdot 8+(-3)\cdot (-4)+4\cdot 0 \\  & =-8+12 \\  & =4\end{aligned}
$$

Since $det(F)=4\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

---

## authored hard extension 

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=0$

$$
T=\begin{bmatrix}\frac{\sqrt{5}}{3} & \frac{4}{3} & \frac{3 \sqrt{5}}{2} \\ \frac{\sqrt{5}}{3} & \frac{4}{3} & \sqrt{5} \\ \frac{2 \sqrt{5}}{3} & \frac{8}{3} & \frac{5 \sqrt{5}}{2}\end{bmatrix}
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =\begin{vmatrix}\frac{\sqrt{5}}{3} & \frac{4}{3} & \frac{3 \sqrt{5}}{2} \\ \frac{\sqrt{5}}{3} & \frac{4}{3} & \sqrt{5} \\ \frac{2 \sqrt{5}}{3} & \frac{8}{3} & \frac{5 \sqrt{5}}{2}\end{vmatrix} \\  & =\frac{\sqrt{5}}{3}\begin{vmatrix}\frac{4}{3} & \sqrt{5} \\ \frac{8}{3} & \frac{5 \sqrt{5}}{2}\end{vmatrix}+(- \frac{4}{3})\begin{vmatrix}\frac{\sqrt{5}}{3} & \sqrt{5} \\ \frac{2 \sqrt{5}}{3} & \frac{5 \sqrt{5}}{2}\end{vmatrix}+\frac{3 \sqrt{5}}{2}\begin{vmatrix}\frac{\sqrt{5}}{3} & \frac{4}{3} \\ \frac{2 \sqrt{5}}{3} & \frac{8}{3}\end{vmatrix} \\  & =\frac{\sqrt{5}}{3}(\frac{10 \sqrt{5}}{3}- \frac{8 \sqrt{5}}{3})+(- \frac{4}{3})(\frac{25}{6}- \frac{10}{3})+\frac{3 \sqrt{5}}{2}(\frac{8 \sqrt{5}}{9}- \frac{8 \sqrt{5}}{9}) \\  & =\frac{\sqrt{5}}{3}\cdot \frac{2 \sqrt{5}}{3}+(- \frac{4}{3})\cdot \frac{5}{6}+\frac{3 \sqrt{5}}{2}\cdot 0 \\  & =\frac{10}{9}- \frac{10}{9} \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

---

## authored hard extension 

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=\frac{7}{4}$

$$
E=\begin{bmatrix}\sqrt{7} & - \frac{2}{3} & \sqrt{7} \\ - \sqrt{7} & - \frac{1}{3} & \frac{3 \sqrt{7}}{4} \\ \sqrt{7} & \frac{4}{3} & - \frac{3 \sqrt{7}}{4}\end{bmatrix}
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =\begin{vmatrix}\sqrt{7} & - \frac{2}{3} & \sqrt{7} \\ - \sqrt{7} & - \frac{1}{3} & \frac{3 \sqrt{7}}{4} \\ \sqrt{7} & \frac{4}{3} & - \frac{3 \sqrt{7}}{4}\end{vmatrix} \\  & =\sqrt{7}\begin{vmatrix}- \frac{1}{3} & \frac{3 \sqrt{7}}{4} \\ \frac{4}{3} & - \frac{3 \sqrt{7}}{4}\end{vmatrix}+\frac{2}{3}\begin{vmatrix}- \sqrt{7} & \frac{3 \sqrt{7}}{4} \\ \sqrt{7} & - \frac{3 \sqrt{7}}{4}\end{vmatrix}+\sqrt{7}\begin{vmatrix}- \sqrt{7} & - \frac{1}{3} \\ \sqrt{7} & \frac{4}{3}\end{vmatrix} \\  & =\sqrt{7}(\frac{\sqrt{7}}{4}- \sqrt{7})+\frac{2}{3}(\frac{21}{4}- \frac{21}{4})+\sqrt{7}(- \frac{4 \sqrt{7}}{3}+\frac{\sqrt{7}}{3}) \\  & =\sqrt{7}\cdot (- \frac{3 \sqrt{7}}{4})+\frac{2}{3}\cdot 0+\sqrt{7}\cdot (- \sqrt{7}) \\  & =- \frac{21}{4}-7 \\  & =- \frac{49}{4}\end{aligned}
$$

Since $det(E)=- \frac{49}{4}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.
