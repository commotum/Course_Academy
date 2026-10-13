# Identifying Singular Matrices: review

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. These are local review records; no registration or writes. Originals are shown verbatim. Generated arithmetic uses exact equivalent formatting and the same number of solution stages. Choice-bank whitespace is preserved.

## Original q-128490 / field 0

Which of the following statements are true regarding the matrix $M$ given below?

- $det(M)=10$
- $det(M)=-5$
- $M$ is a singular matrix

 

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}]
$$

- II only
- III only
- I only
- None of the given statements are true
- I and III only

Original correct designation: None

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|-0|\begin{aligned}0 & 5 \\ -3\sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ -3\sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)-0+\frac{1}{3}(0+9\sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9\sqrt{5} \\  & =-3\sqrt{5}+3\sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $M$ given below?

- $det(M)=10$
- $det(M)=-5$
- $M$ is a singular matrix

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}]
$$

A. II only
B. I only
C. I and III only
D. None of the given statements are true
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|+0|\begin{aligned}0 & 5 \\ - 3 \sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ - 3 \sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)+0+\frac{1}{3}(0+9 \sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9 \sqrt{5} \\  & =- 3 \sqrt{5}+3 \sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Generated variant (moderate, seed 13, moderate_bullets_det_det_singular_6, bank_1)

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $det(F)=1$
- $F$ is a singular matrix

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

A. I and III only
B. I only
C. II only
D. None of the given statements are true
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (moderate, seed 41, moderate_bullets_det_det_singular_6, bank_1)

Which of the following statements are true regarding the matrix $E$ given below?

- $det(E)=0$
- $det(E)=1$
- $E$ is a singular matrix

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. I only
B. None of the given statements are true
C. III only
D. I and III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, none of the statements are true.

## Original q-128490 / field 1

Which of the following statements are true regarding the matrix $M$ given below?

- $det(M)=10$
- $det(M)=-5$
- $M$ is a singular matrix

 

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}]
$$

- None of the given statements are true
- I and III only
- I only
- III only
- II only

Original correct designation: III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|-0|\begin{aligned}0 & 5 \\ -3\sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ -3\sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)-0+\frac{1}{3}(0+9\sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9\sqrt{5} \\  & =-3\sqrt{5}+3\sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $M$ given below?

- $det(M)=10$
- $det(M)=-5$
- $M$ is a singular matrix

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}]
$$

A. II only
B. I only
C. I and III only
D. None of the given statements are true
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|+0|\begin{aligned}0 & 5 \\ - 3 \sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ - 3 \sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)+0+\frac{1}{3}(0+9 \sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9 \sqrt{5} \\  & =- 3 \sqrt{5}+3 \sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Generated variant (moderate, seed 13, moderate_bullets_det_det_singular_6, bank_1)

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $det(F)=1$
- $F$ is a singular matrix

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

A. I and III only
B. I only
C. II only
D. None of the given statements are true
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (moderate, seed 41, moderate_bullets_det_det_singular_6, bank_1)

Which of the following statements are true regarding the matrix $E$ given below?

- $det(E)=0$
- $det(E)=1$
- $E$ is a singular matrix

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. I only
B. None of the given statements are true
C. III only
D. I and III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, none of the statements are true.

## Original q-9838 / field 0

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $F$ is a singular matrix
- $det(F)=-2$

$$
F=[\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}]
$$

- II only
- I and II only
- I only
- III only
- II and III only

Original correct designation: I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 5 \\ 7 & 8\end{aligned}|-1|\begin{aligned}3 & 5 \\ 6 & 8\end{aligned}|+2|\begin{aligned}3 & 4 \\ 6 & 7\end{aligned}| \\  & =0-1(24-30)+2(21-24) \\  & =0-1\cdot (-6)+2\cdot (-3) \\  & =6-6 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $F$ is a singular matrix
- $det(F)=-2$

$$
F=[\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 5 \\ 7 & 8\end{aligned}|+(-1)|\begin{aligned}3 & 5 \\ 6 & 8\end{aligned}|+2|\begin{aligned}3 & 4 \\ 6 & 7\end{aligned}| \\  & =0+(-1)(24-30)+2(21-24) \\  & =(-1)\cdot (-6)+2\cdot (-3) \\  & =6-6 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (easy, seed 13, easy_bullets_det_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $E$ given below?

- $det(E)=-6$
- $E$ is a singular matrix
- $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. III only
B. II only
C. I only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (easy, seed 41, easy_bullets_det_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $F$ is a singular matrix
- $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

A. III only
B. I only
C. II only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128474 / field 0

Which of the following statements are true regarding the matrix $Q$ given below?

- $det(Q)=-5$
- $det(Q)=1$
- $Q$ is **not** a singular matrix

$$
Q=[\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}]
$$

- I and III only
- II only
- III only
- II and III only
- None of the given statements are true

Original correct designation: None of the given statements are true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}| \\  & =1|\begin{aligned}3 & 1 \\ 5 & 3\end{aligned}|-1|\begin{aligned}2 & 1 \\ 3 & 3\end{aligned}|-1|\begin{aligned}2 & 3 \\ 3 & 5\end{aligned}| \\  & =1(9-5)-1(6-3)-1(10-9) \\  & =1\cdot 4-1\cdot 3-1\cdot 1 \\  & =4-3-1 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $Q$ given below?

- $det(Q)=-5$
- $det(Q)=1$
- $Q$ is **not** a singular matrix

$$
Q=[\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}]
$$

A. II only
B. II and III only
C. I and III only
D. None of the given statements are true
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}| \\  & =1|\begin{aligned}3 & 1 \\ 5 & 3\end{aligned}|+(-1)|\begin{aligned}2 & 1 \\ 3 & 3\end{aligned}|+(-1)|\begin{aligned}2 & 3 \\ 3 & 5\end{aligned}| \\  & =1(9-5)+(-1)(6-3)+(-1)(10-9) \\  & =1\cdot 4+(-1)\cdot 3+(-1)\cdot 1 \\  & =4-3-1 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated variant (easy, seed 13, easy_bullets_det_det_nonsingular_6, bank_3)

Which of the following statements are true regarding the matrix $E$ given below?

- $det(E)=-6$
- $det(E)=1$
- $E$ is **not** a singular matrix

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. None of the given statements are true
B. III only
C. II and III only
D. II only
E. I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated variant (easy, seed 41, easy_bullets_det_det_nonsingular_6, bank_3)

Which of the following statements are true regarding the matrix $D$ given below?

- $det(D)=1$
- $det(D)=0$
- $D$ is **not** a singular matrix

$$
D=[\begin{aligned}0 & -2 & 4 \\ -5 & 4 & 4 \\ 10 & -10 & -4\end{aligned}]
$$

A. II only
B. II and III only
C. None of the given statements are true
D. III only
E. I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}0 & -2 & 4 \\ -5 & 4 & 4 \\ 10 & -10 & -4\end{aligned}| \\  & =0|\begin{aligned}4 & 4 \\ -10 & -4\end{aligned}|+2|\begin{aligned}-5 & 4 \\ 10 & -4\end{aligned}|+4|\begin{aligned}-5 & 4 \\ 10 & -10\end{aligned}| \\  & =0+2(20-40)+4(50-40) \\  & =2\cdot (-20)+4\cdot 10 \\  & =-40+40 \\  & =0\end{aligned}
$$

Since $det(D)=0$, the matrix is singular. 

Therefore, only statement II is true.

## Original q-128476 / field 0

Which of the following statements are true regarding the matrix $T$ given below?

- $T$ is a singular matrix
- $T$ is **not** a singular matrix
- $det(T)=-30$

 

$$
T=[\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}]
$$

- II and III only
- II only
- I only
- III only
- I and III only

Original correct designation: II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ 3 & 1\end{aligned}|-3|\begin{aligned}2 & 1 \\ 1 & 1\end{aligned}|-5|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}| \\  & =1(1-3)-3(2-1)-5(6-1) \\  & =1\cdot (-2)-3\cdot 1-5\cdot 5 \\  & =-2-3-25 \\  & =-30\end{aligned}
$$

 

Since $det(T)=-30\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $T$ given below?

- $T$ is a singular matrix
- $T$ is **not** a singular matrix
- $det(T)=-30$

$$
T=[\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}]
$$

A. II and III only
B. I only
C. I and III only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ 3 & 1\end{aligned}|+(-3)|\begin{aligned}2 & 1 \\ 1 & 1\end{aligned}|+(-5)|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}| \\  & =1(1-3)+(-3)(2-1)+(-5)(6-1) \\  & =1\cdot (-2)+(-3)\cdot 1+(-5)\cdot 5 \\  & =-2-3-25 \\  & =-30\end{aligned}
$$

 

Since $det(T)=-30\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

### Generated variant (easy, seed 13, easy_bullets_singular_nonsingular_det_6, bank_4)

Which of the following statements are true regarding the matrix $T$ given below?

- $T$ is a singular matrix
- $T$ is **not** a singular matrix
- $det(T)=0$

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

A. II only
B. II and III only
C. I and III only
D. III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (easy, seed 41, easy_bullets_singular_nonsingular_det_6, bank_4)

Which of the following statements are true regarding the matrix $F$ given below?

- $F$ is a singular matrix
- $F$ is **not** a singular matrix
- $det(F)=5$

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

A. I only
B. II and III only
C. III only
D. II only
E. I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

## Original q-128484 / field 0

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=0$
- $det(R)=1$

 

$$
R=[\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}]
$$

- I and III only
- I and II only
- I only
- II only
- III only

Original correct designation: I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}| \\  & =2|\begin{aligned}0 & -1 \\ \sqrt{2} & 4\end{aligned}|-\sqrt{2}|\begin{aligned}\frac{1}{2} & -1 \\ 1 & 4\end{aligned}|+2|\begin{aligned}\frac{1}{2} & 0 \\ 1 & \sqrt{2}\end{aligned}| \\  & =2(0+\sqrt{2})-\sqrt{2}(2+1)+2(\frac{\sqrt{2}}{2}-0) \\  & =2\cdot \sqrt{2}-\sqrt{2}\cdot 3+2\cdot \frac{\sqrt{2}}{2} \\  & =2\sqrt{2}-3\sqrt{2}+\sqrt{2} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=0$
- $det(R)=1$

$$
R=[\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}]
$$

A. I only
B. I and III only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}| \\  & =2|\begin{aligned}0 & -1 \\ \sqrt{2} & 4\end{aligned}|+(- \sqrt{2})|\begin{aligned}\frac{1}{2} & -1 \\ 1 & 4\end{aligned}|+2|\begin{aligned}\frac{1}{2} & 0 \\ 1 & \sqrt{2}\end{aligned}| \\  & =2(0+\sqrt{2})+(- \sqrt{2})(2+1)+2(\frac{\sqrt{2}}{2}+0) \\  & =2\cdot \sqrt{2}+(- \sqrt{2})\cdot 3+2\cdot \frac{\sqrt{2}}{2} \\  & =2 \sqrt{2}- 3 \sqrt{2}+\sqrt{2} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (moderate, seed 13, moderate_bullets_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $F$ given below?

- $F$ is a singular matrix
- $det(F)=0$
- $det(F)=1$

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

A. I and II only
B. I and III only
C. I only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (moderate, seed 41, moderate_bullets_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=1$
- $det(R)=0$

$$
R=[\begin{aligned}-1 & 5 & \frac{6}{5} \\ 4 & 4 & -1 \\ 3 & 9 & \frac{1}{5}\end{aligned}]
$$

A. I and III only
B. I only
C. II only
D. III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}-1 & 5 & \frac{6}{5} \\ 4 & 4 & -1 \\ 3 & 9 & \frac{1}{5}\end{aligned}| \\  & =(-1)|\begin{aligned}4 & -1 \\ 9 & \frac{1}{5}\end{aligned}|+(-5)|\begin{aligned}4 & -1 \\ 3 & \frac{1}{5}\end{aligned}|+\frac{6}{5}|\begin{aligned}4 & 4 \\ 3 & 9\end{aligned}| \\  & =(-1)(\frac{4}{5}+9)+(-5)(\frac{4}{5}+3)+\frac{6}{5}(36-12) \\  & =(-1)\cdot \frac{49}{5}+(-5)\cdot \frac{19}{5}+\frac{6}{5}\cdot 24 \\  & =- \frac{49}{5}-19+\frac{144}{5} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

## Original q-38179 / field 0

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is a singular matrix
- $E$ is **not**  a singular matrix
- $det(E)=-2$

$$
E=[\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}]
$$

- II only
- III only
- I and II only
- I only
- II and III only

Original correct designation: I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}| \\  & =\frac{2}{3}|\begin{aligned}5 & 6 \\ 7 & 8\end{aligned}|-3|\begin{aligned}\frac{2}{3} & 6 \\ \frac{2}{3} & 8\end{aligned}|+4|\begin{aligned}\frac{2}{3} & 5 \\ \frac{2}{3} & 7\end{aligned}| \\  & =\frac{2}{3}(40-42)-3(\frac{16}{3}-\frac{12}{3})+4(\frac{14}{3}-\frac{10}{3}) \\  & =\frac{2}{3}\cdot (-2)-3\cdot \frac{4}{3}+4\cdot \frac{4}{3} \\  & =-\frac{4}{3}-\frac{12}{3}+\frac{16}{3} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is a singular matrix
- $E$ is **not** a singular matrix
- $det(E)=-2$

$$
E=[\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}| \\  & =\frac{2}{3}|\begin{aligned}5 & 6 \\ 7 & 8\end{aligned}|+(-3)|\begin{aligned}\frac{2}{3} & 6 \\ \frac{2}{3} & 8\end{aligned}|+4|\begin{aligned}\frac{2}{3} & 5 \\ \frac{2}{3} & 7\end{aligned}| \\  & =\frac{2}{3}(40-42)+(-3)(\frac{16}{3}-4)+4(\frac{14}{3}- \frac{10}{3}) \\  & =\frac{2}{3}\cdot (-2)+(-3)\cdot \frac{4}{3}+4\cdot \frac{4}{3} \\  & =- \frac{4}{3}-4+\frac{16}{3} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated variant (moderate, seed 13, moderate_bullets_singular_nonsingular_det_6, bank_2)

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is a singular matrix
- $E$ is **not** a singular matrix
- $det(E)=-1$

$$
E=[\begin{aligned}8 \sqrt{5} & -2 & 6 \\ - \sqrt{5} & -5 & 1 \\ 7 \sqrt{5} & -7 & 7\end{aligned}]
$$

A. II only
B. I only
C. I and II only
D. III only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}8 \sqrt{5} & -2 & 6 \\ - \sqrt{5} & -5 & 1 \\ 7 \sqrt{5} & -7 & 7\end{aligned}| \\  & =8 \sqrt{5}|\begin{aligned}-5 & 1 \\ -7 & 7\end{aligned}|+2|\begin{aligned}- \sqrt{5} & 1 \\ 7 \sqrt{5} & 7\end{aligned}|+6|\begin{aligned}- \sqrt{5} & -5 \\ 7 \sqrt{5} & -7\end{aligned}| \\  & =8 \sqrt{5}(-35+7)+2(- 7 \sqrt{5}- 7 \sqrt{5})+6(7 \sqrt{5}+35 \sqrt{5}) \\  & =8 \sqrt{5}\cdot (-28)+2\cdot (- 14 \sqrt{5})+6\cdot 42 \sqrt{5} \\  & =- 224 \sqrt{5}- 28 \sqrt{5}+252 \sqrt{5} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated variant (moderate, seed 41, moderate_bullets_singular_nonsingular_det_6, bank_2)

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is a singular matrix
- $E$ is **not** a singular matrix
- $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. III only
B. I and II only
C. II only
D. I only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Original q-38182 / field 0

Which of the following statements are true regarding the matrix $Q$ given below?

- $Q$ is **not** a singular matrix
- $Q$ is a singular matrix
- $det(Q)=-5$

$$
Q=[\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}]
$$

- III only
- I only
- II and III only
- I and III only
- II only

Original correct designation: II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 7 \\ 5 & 8\end{aligned}|-3|\begin{aligned}1 & 7 \\ 2 & 8\end{aligned}|+6|\begin{aligned}1 & 4 \\ 2 & 5\end{aligned}| \\  & =0-3(8-14)+6(5-8) \\  & =0-3\cdot (-6)+6\cdot (-3) \\  & =18-18 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $Q$ given below?

- $Q$ is **not** a singular matrix
- $Q$ is a singular matrix
- $det(Q)=-5$

$$
Q=[\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}]
$$

A. II and III only
B. I only
C. I and III only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 7 \\ 5 & 8\end{aligned}|+(-3)|\begin{aligned}1 & 7 \\ 2 & 8\end{aligned}|+6|\begin{aligned}1 & 4 \\ 2 & 5\end{aligned}| \\  & =0+(-3)(8-14)+6(5-8) \\  & =(-3)\cdot (-6)+6\cdot (-3) \\  & =18-18 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (easy, seed 13, easy_bullets_nonsingular_singular_det_6, bank_4)

Which of the following statements are true regarding the matrix $T$ given below?

- $T$ is **not** a singular matrix
- $T$ is a singular matrix
- $det(T)=0$

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

A. II only
B. II and III only
C. I and III only
D. III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated variant (easy, seed 41, easy_bullets_nonsingular_singular_det_6, bank_4)

Which of the following statements are true regarding the matrix $F$ given below?

- $F$ is **not** a singular matrix
- $F$ is a singular matrix
- $det(F)=5$

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

A. I only
B. II and III only
C. III only
D. II only
E. I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

## Original q-69834 / field 0

Which of the following statements are true regarding the matrix $M$ given below?

- $M$ is a singular matrix
- $det(M)=1$
- $det(M)=0$

 

$$
M=[\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}]
$$

- I and III only
- I only
- I and II only
- II only
- III only

Original correct designation: I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}| \\  & =1|\begin{aligned}2 & 3 \\ 4 & -2\end{aligned}|-(-2)|\begin{aligned}1 & 3 \\ -2 & -2\end{aligned}|+1|\begin{aligned}1 & 2 \\ -2 & 4\end{aligned}| \\  & =1(-4-12)+2(-2+6)+1(4+4) \\  & =1\cdot (-16)+2\cdot 4+1\cdot 8 \\  & =-16+8+8 \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $M$ given below?

- $M$ is a singular matrix
- $det(M)=1$
- $det(M)=0$

$$
M=[\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}]
$$

A. I only
B. I and III only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}| \\  & =1|\begin{aligned}2 & 3 \\ 4 & -2\end{aligned}|+2|\begin{aligned}1 & 3 \\ -2 & -2\end{aligned}|+1|\begin{aligned}1 & 2 \\ -2 & 4\end{aligned}| \\  & =1(-4-12)+2(-2+6)+1(4+4) \\  & =1\cdot (-16)+2\cdot 4+1\cdot 8 \\  & =-16+8+8 \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (easy, seed 13, easy_bullets_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is a singular matrix
- $det(E)=-6$
- $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. III only
B. II only
C. I and III only
D. I only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated variant (easy, seed 41, easy_bullets_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $F$ given below?

- $F$ is a singular matrix
- $det(F)=0$
- $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

A. III only
B. I and III only
C. II only
D. I only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-77477 / field 0

Which of the following statements are true regarding the matrix $S$ given below?

I. $S$ is **not** a singular matrix

II. $S$ is a singular matrix

III. $det(S)=\sqrt{3}$

$$
S=[\begin{aligned}1 & 2 & \,0 \\ 2 & \sqrt{3} & \,\,-1 \\ \sqrt{3} & 4 & \,\,-\sqrt{3}\end{aligned}]
$$

- III only
- II and III only
- I  only
- I and III  only
- II only

Original correct designation: I  only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}1 & 2 & \,0 \\ 2 & \sqrt{3} & \,\,-1 \\ \sqrt{3} & 4 & \,\,-\sqrt{3}\end{aligned}| \\  & =1|\begin{aligned}\sqrt{3} & \,\,-1 \\ 4 & \,\,-\sqrt{3}\end{aligned}|-2|\begin{aligned}2 & \,-1 \\ \sqrt{3} & \,-\sqrt{3}\end{aligned}|+0|\begin{aligned}2 & \sqrt{3} \\ \sqrt{3} & 4\end{aligned}| \\  & =1(-{(\sqrt{3})}^{2}+4)-2(-2\sqrt{3}+\sqrt{3})+0 \\  & =(-3+4)-2\cdot (-\sqrt{3}) \\  & =1+2\sqrt{3}\end{aligned}
$$

Since $det(S)=1+2\sqrt{3}\ne 0$, the matrix is **not ** singular. 

Therefore, only statement I is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $S$ given below?

I. $S$ is **not** a singular matrix

II. $S$ is a singular matrix

III. $det(S)=\sqrt{3}$

$$
S=[\begin{aligned}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{aligned}]
$$

A. II and III only
B. I and III  only
C. I  only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{aligned}| \\  & =1|\begin{aligned}\sqrt{3} & -1 \\ 4 & - \sqrt{3}\end{aligned}|+(-2)|\begin{aligned}2 & -1 \\ \sqrt{3} & - \sqrt{3}\end{aligned}|+0|\begin{aligned}2 & \sqrt{3} \\ \sqrt{3} & 4\end{aligned}| \\  & =1(-3+4)+(-2)(- 2 \sqrt{3}+\sqrt{3})+0 \\  & =(-3+4)+(-2)\cdot (- \sqrt{3}) \\  & =1 + 2 \sqrt{3}\end{aligned}
$$

Since $det(S)=1 + 2 \sqrt{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

### Generated variant (moderate, seed 13, moderate_roman-spaced_nonsingular_singular_det_5, bank_6)

Which of the following statements are true regarding the matrix $R$ given below?

I. $R$ is **not** a singular matrix

II. $R$ is a singular matrix

III. $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

A. II only
B. III only
C. I  only
D. II and III only
E. I and III  only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}\cdot \frac{4}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated variant (moderate, seed 41, moderate_roman-spaced_nonsingular_singular_det_5, bank_6)

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is **not** a singular matrix

II. $E$ is a singular matrix

III. $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. III only
B. I  only
C. II only
D. I and III  only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =(\frac{1}{3}+\frac{4}{3})+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-77478 / field 0

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=0$
- $det(R)=1$

 

$$
R=[\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}]
$$

- I and III only
- I only
- I and II only
- III only
- II and III only

Original correct designation: I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}| \\  & =\frac{3}{5}|\begin{aligned}2 & 3 \\ \frac{1}{2} & 1\end{aligned}|-\frac{2}{5}|\begin{aligned}1 & 3 \\ 0 & 1\end{aligned}|+\frac{1}{5}|\begin{aligned}1 & 2 \\ 0 & \frac{1}{2}\end{aligned}| \\  & =\frac{3}{5}(2-\frac{3}{2})-\frac{2}{5}(1-0)+\frac{1}{5}(\frac{1}{2}-0) \\  & =\frac{3}{5}\cdot \frac{1}{2}-\frac{2}{5}\cdot 1+\frac{1}{5}\cdot \frac{1}{2} \\  & =\frac{3}{10}-\frac{2}{5}+\frac{1}{10} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=0$
- $det(R)=1$

$$
R=[\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}]
$$

A. I only
B. I and III only
C. I and II only
D. III only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}| \\  & =\frac{3}{5}|\begin{aligned}2 & 3 \\ \frac{1}{2} & 1\end{aligned}|+(- \frac{2}{5})|\begin{aligned}1 & 3 \\ 0 & 1\end{aligned}|+\frac{1}{5}|\begin{aligned}1 & 2 \\ 0 & \frac{1}{2}\end{aligned}| \\  & =\frac{3}{5}(2- \frac{3}{2})+(- \frac{2}{5})(1+0)+\frac{1}{5}(\frac{1}{2}+0) \\  & =\frac{3}{5}\cdot \frac{1}{2}+(- \frac{2}{5})\cdot 1+\frac{1}{5}\cdot \frac{1}{2} \\  & =\frac{3}{10}- \frac{2}{5}+\frac{1}{10} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (moderate, seed 13, moderate_bullets_singular_det_det_6, bank_7)

Which of the following statements are true regarding the matrix $F$ given below?

- $F$ is a singular matrix
- $det(F)=0$
- $det(F)=1$

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

A. I and II only
B. I and III only
C. I only
D. III only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (moderate, seed 41, moderate_bullets_singular_det_det_6, bank_7)

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is a singular matrix
- $det(R)=1$
- $det(R)=0$

$$
R=[\begin{aligned}-1 & 5 & \frac{6}{5} \\ 4 & 4 & -1 \\ 3 & 9 & \frac{1}{5}\end{aligned}]
$$

A. I and III only
B. I only
C. II and III only
D. III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}-1 & 5 & \frac{6}{5} \\ 4 & 4 & -1 \\ 3 & 9 & \frac{1}{5}\end{aligned}| \\  & =(-1)|\begin{aligned}4 & -1 \\ 9 & \frac{1}{5}\end{aligned}|+(-5)|\begin{aligned}4 & -1 \\ 3 & \frac{1}{5}\end{aligned}|+\frac{6}{5}|\begin{aligned}4 & 4 \\ 3 & 9\end{aligned}| \\  & =(-1)(\frac{4}{5}+9)+(-5)(\frac{4}{5}+3)+\frac{6}{5}(36-12) \\  & =(-1)\cdot \frac{49}{5}+(-5)\cdot \frac{19}{5}+\frac{6}{5}\cdot 24 \\  & =- \frac{49}{5}-19+\frac{144}{5} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

## Original q-77479 / field 0

Which of the following statements are true regarding the matrix $P$ given below?

- $P$ is **not**  a singular matrix
- $P$ is a singular matrix
- $det(P)=-\frac{1}{2}$

$$
P=[\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}]
$$

- I and II only
- II and III only
- III only
- I only
- II only

Original correct designation: II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows: 

$$
\begin{aligned}det(P) & =|\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}| \\  & =\frac{1}{2}|\begin{aligned}2 & \frac{1}{2} \\ 0 & -1\end{aligned}|-1|\begin{aligned}\frac{1}{2} & \frac{1}{2} \\ -1 & -1\end{aligned}|+\frac{1}{2}|\begin{aligned}\frac{1}{2} & 2 \\ -1 & 0\end{aligned}| \\  & =\frac{1}{2}(-2-0)-1(-\frac{1}{2}+\frac{1}{2})+\frac{1}{2}(0+2) \\  & =(-2)\cdot \frac{1}{2}-1\cdot 0+\frac{1}{2}\cdot 2 \\  & =-1+1 \\  & =0\end{aligned}
$$

Since $det(P)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $P$ given below?

- $P$ is **not** a singular matrix
- $P$ is a singular matrix
- $det(P)=- \frac{1}{2}$

$$
P=[\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =|\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}| \\  & =\frac{1}{2}|\begin{aligned}2 & \frac{1}{2} \\ 0 & -1\end{aligned}|+(-1)|\begin{aligned}\frac{1}{2} & \frac{1}{2} \\ -1 & -1\end{aligned}|+\frac{1}{2}|\begin{aligned}\frac{1}{2} & 2 \\ -1 & 0\end{aligned}| \\  & =\frac{1}{2}(-2+0)+(-1)(- \frac{1}{2}+\frac{1}{2})+\frac{1}{2}(0+2) \\  & =\frac{1}{2}\cdot (-2)+(-1)\cdot 0+\frac{1}{2}\cdot 2 \\  & =-1+1 \\  & =0\end{aligned}
$$

Since $det(P)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (moderate, seed 13, moderate_bullets_nonsingular_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $R$ given below?

- $R$ is **not** a singular matrix
- $R$ is a singular matrix
- $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

A. II only
B. III only
C. I and II only
D. II and III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated variant (moderate, seed 41, moderate_bullets_nonsingular_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $E$ given below?

- $E$ is **not** a singular matrix
- $E$ is a singular matrix
- $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. III only
B. I and II only
C. II only
D. I only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-9835 / field 0

Which of the following statements are true regarding the matrix $D$ given below?

- $det(D)=1$
- $D$ is a singular matrix
- $det(D)=0$

 

$$
D=[\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}]
$$

- II and III only
- I only
- III only
- I and II only
- II only

Original correct designation: II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}| \\  & =1|\begin{aligned}4 & 5 \\ 6 & 7\end{aligned}|-2|\begin{aligned}1 & 5 \\ 1 & 7\end{aligned}|+3|\begin{aligned}1 & 4 \\ 1 & 6\end{aligned}| \\  & =1(28-30)-2(7-5)+3(6-4) \\  & =1\cdot (-2)-2\cdot 2+3\cdot 2 \\  & =-2-4+6 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $D$ given below?

- $det(D)=1$
- $D$ is a singular matrix
- $det(D)=0$

$$
D=[\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}| \\  & =1|\begin{aligned}4 & 5 \\ 6 & 7\end{aligned}|+(-2)|\begin{aligned}1 & 5 \\ 1 & 7\end{aligned}|+3|\begin{aligned}1 & 4 \\ 1 & 6\end{aligned}| \\  & =1(28-30)+(-2)(7-5)+3(6-4) \\  & =1\cdot (-2)+(-2)\cdot 2+3\cdot 2 \\  & =-2-4+6 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated variant (easy, seed 13, easy_bullets_det_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $E$ given below?

- $det(E)=-6$
- $E$ is a singular matrix
- $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. III only
B. II only
C. I only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (easy, seed 41, easy_bullets_det_singular_det_6, bank_2)

Which of the following statements are true regarding the matrix $F$ given below?

- $det(F)=0$
- $F$ is a singular matrix
- $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

A. III only
B. I only
C. II only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128478 / field 0

Which of the following statements are true regarding the matrix $F$ given below?

I. $det(F)=-7$
II. $F$ is **not** a singular matrix
III. $det(F)=-2$

$$
F=[\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}]
$$

- II and III only
- None of the given statements are true
- I only
- I and II only
- II only

Original correct designation: II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}| \\  & =2|\begin{aligned}2 & 1 \\ 3 & 1\end{aligned}|-8|\begin{aligned}-1 & 1 \\ 5 & 1\end{aligned}|+3|\begin{aligned}-1 & 2 \\ 5 & 3\end{aligned}| \\  & =2(2-3)-8(-1-5)+3(-3-10) \\  & =2\cdot (-1)-8\cdot (-6)+3\cdot (-13) \\  & =-2+48-39 \\  & =7\end{aligned}
$$

Since $det(F)=7$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $F$ given below?

I. $det(F)=-7$
II. $F$ is **not** a singular matrix
III. $det(F)=-2$

$$
F=[\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. None of the given statements are true
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}| \\  & =2|\begin{aligned}2 & 1 \\ 3 & 1\end{aligned}|+(-8)|\begin{aligned}-1 & 1 \\ 5 & 1\end{aligned}|+3|\begin{aligned}-1 & 2 \\ 5 & 3\end{aligned}| \\  & =2(2-3)+(-8)(-1-5)+3(-3-10) \\  & =2\cdot (-1)+(-8)\cdot (-6)+3\cdot (-13) \\  & =-2+48-39 \\  & =7\end{aligned}
$$

Since $det(F)=7$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Generated variant (easy, seed 13, easy_roman_det_nonsingular_det_6, bank_8)

Which of the following statements are true regarding the matrix $E$ given below?

I. $det(E)=-6$
II. $E$ is **not** a singular matrix
III. $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. None of the given statements are true
B. II only
C. I only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated variant (easy, seed 41, easy_roman_det_nonsingular_det_6, bank_8)

Which of the following statements are true regarding the matrix $F$ given below?

I. $det(F)=0$
II. $F$ is **not** a singular matrix
III. $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

A. None of the given statements are true
B. I only
C. II only
D. II and III only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statement I is true.

## Original q-128480 / field 0

Which of the following statements are true regarding the matrix $D$ given below?

I. $D$ is a singular matrix
II. $det(D)=1$
III. $det(D)=0$

$$
D=[\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}]
$$

- I and III only
- I only
- III only
- I and II only
- II only

Original correct designation: I and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}| \\  & =2|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|+3|\begin{aligned}-1 & 3 \\ -3 & 2\end{aligned}|+1|\begin{aligned}-1 & 2 \\ -3 & 5\end{aligned}| \\  & =2(4-15)+3(-2+9)+1(-5+6) \\  & =2\cdot (-11)+3\cdot 7+1\cdot 1 \\  & =-22+21+1 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $D$ given below?

I. $D$ is a singular matrix
II. $det(D)=1$
III. $det(D)=0$

$$
D=[\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}]
$$

A. I only
B. I and III only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}| \\  & =2|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|+3|\begin{aligned}-1 & 3 \\ -3 & 2\end{aligned}|+1|\begin{aligned}-1 & 2 \\ -3 & 5\end{aligned}| \\  & =2(4-15)+3(-2+9)+1(-5+6) \\  & =2\cdot (-11)+3\cdot 7+1\cdot 1 \\  & =-22+21+1 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (easy, seed 13, easy_roman_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is a singular matrix
II. $det(E)=-6$
III. $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

A. III only
B. II only
C. I and III only
D. I only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated variant (easy, seed 41, easy_roman_singular_det_det_6, bank_5)

Which of the following statements are true regarding the matrix $F$ given below?

I. $F$ is a singular matrix
II. $det(F)=0$
III. $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

A. III only
B. I and III only
C. II only
D. I only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128491 / field 0

Which of the following statements are true regarding the matrix $S$ given below?

I. $S$ is a singular matrix
II. $S$ is **not** a singular matrix
III. $det(S)=5+2\sqrt{7}$

$$
S=[\begin{aligned}2\sqrt{7} & 0 & \frac{1}{2} \\ -\sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}]
$$

- II and III only
- I and III only
- I only
- III only
- II only

Original correct designation: II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}2\sqrt{7} & 0 & \frac{1}{2} \\ -\sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}| \\  & =2\sqrt{7}|\begin{aligned}2 & 0 \\ 0 & \sqrt{7}\end{aligned}|-0|\begin{aligned}-\sqrt{7} & 0 \\ 5 & \sqrt{7}\end{aligned}|+\frac{1}{2}|\begin{aligned}-\sqrt{7} & 2 \\ 5 & 0\end{aligned}| \\  & =2\sqrt{7}(2\sqrt{7}-0)-0+\frac{1}{2}(0-10) \\  & =2\sqrt{7}\cdot 2\sqrt{7}+\frac{1}{2}\cdot (-10) \\  & =28-5 \\  & =23\end{aligned}
$$

Since $det(S)=23\ne 0$, the matrix is **not ** singular. 

Therefore, only statement II is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $S$ given below?

I. $S$ is a singular matrix
II. $S$ is **not** a singular matrix
III. $det(S)=5 + 2 \sqrt{7}$

$$
S=[\begin{aligned}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}]
$$

A. II and III only
B. I only
C. I and III only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}| \\  & =2 \sqrt{7}|\begin{aligned}2 & 0 \\ 0 & \sqrt{7}\end{aligned}|+0|\begin{aligned}- \sqrt{7} & 0 \\ 5 & \sqrt{7}\end{aligned}|+\frac{1}{2}|\begin{aligned}- \sqrt{7} & 2 \\ 5 & 0\end{aligned}| \\  & =2 \sqrt{7}(2 \sqrt{7}+0)+0+\frac{1}{2}(0-10) \\  & =2 \sqrt{7}\cdot 2 \sqrt{7}+\frac{1}{2}\cdot (-10) \\  & =28-5 \\  & =23\end{aligned}
$$

Since $det(S)=23\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Generated variant (moderate, seed 13, moderate_roman_singular_nonsingular_det_6, bank_4)

Which of the following statements are true regarding the matrix $R$ given below?

I. $R$ is a singular matrix
II. $R$ is **not** a singular matrix
III. $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

A. II only
B. III only
C. I and III only
D. II and III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated variant (moderate, seed 41, moderate_roman_singular_nonsingular_det_6, bank_4)

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is a singular matrix
II. $E$ is **not** a singular matrix
III. $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. III only
B. I and III only
C. II only
D. I only
E. II and III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Original q-38187 / field 0

Which of the following statements are true regarding the matrix $N$ given below?

I. $N$ is **not** a singular matrix
II. $N$ is a singular matrix
III. $det(N)=-1$

$$
N=[\begin{aligned}\frac{1}{7} & 3 & -\frac{1}{7} \\ \frac{1}{7} & 4 & -\frac{1}{7} \\ \frac{1}{7} & 5 & -\frac{1}{7}\end{aligned}]
$$

- I and III only
- I only
- III only
- I and II only
- II only

Original correct designation: II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =|\begin{aligned}\frac{1}{7} & 3 & -\frac{1}{7} \\ \frac{1}{7} & 4 & -\frac{1}{7} \\ \frac{1}{7} & 5 & -\frac{1}{7}\end{aligned}| \\  & =\frac{1}{7}|\begin{aligned}4 & -\frac{1}{7} \\ 5 & -\frac{1}{7}\end{aligned}|-3|\begin{aligned}\frac{1}{7} & -\frac{1}{7} \\ \frac{1}{7} & -\frac{1}{7}\end{aligned}|+(-\frac{1}{7})|\begin{aligned}\frac{1}{7} & 4 \\ \frac{1}{7} & 5\end{aligned}| \\  & =\frac{1}{7}(-\frac{4}{7}+\frac{5}{7})-3(-\frac{1}{49}+\frac{1}{49})-\frac{1}{7}(\frac{5}{7}-\frac{4}{7}) \\  & =\frac{1}{7}\cdot \frac{1}{7}-3\cdot 0-\frac{1}{7}\cdot \frac{1}{7} \\  & =\frac{1}{49}-\frac{1}{49} \\  & =0\end{aligned}
$$

Since $det(N)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $N$ given below?

I. $N$ is **not** a singular matrix
II. $N$ is a singular matrix
III. $det(N)=-1$

$$
N=[\begin{aligned}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{aligned}]
$$

A. I only
B. I and III only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =|\begin{aligned}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{aligned}| \\  & =\frac{1}{7}|\begin{aligned}4 & - \frac{1}{7} \\ 5 & - \frac{1}{7}\end{aligned}|+(-3)|\begin{aligned}\frac{1}{7} & - \frac{1}{7} \\ \frac{1}{7} & - \frac{1}{7}\end{aligned}|+(- \frac{1}{7})|\begin{aligned}\frac{1}{7} & 4 \\ \frac{1}{7} & 5\end{aligned}| \\  & =\frac{1}{7}(- \frac{4}{7}+\frac{5}{7})+(-3)(- \frac{1}{49}+\frac{1}{49})+(- \frac{1}{7})(\frac{5}{7}- \frac{4}{7}) \\  & =\frac{1}{7}\cdot \frac{1}{7}+(-3)\cdot 0+(- \frac{1}{7})\cdot \frac{1}{7} \\  & =\frac{1}{49}- \frac{1}{49} \\  & =0\end{aligned}
$$

Since $det(N)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (moderate, seed 13, moderate_roman_nonsingular_singular_det_6, bank_5)

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is **not** a singular matrix
II. $E$ is a singular matrix
III. $det(E)=-1$

$$
E=[\begin{aligned}8 \sqrt{5} & -2 & 6 \\ - \sqrt{5} & -5 & 1 \\ 7 \sqrt{5} & -7 & 7\end{aligned}]
$$

A. II only
B. I and III only
C. I and II only
D. III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}8 \sqrt{5} & -2 & 6 \\ - \sqrt{5} & -5 & 1 \\ 7 \sqrt{5} & -7 & 7\end{aligned}| \\  & =8 \sqrt{5}|\begin{aligned}-5 & 1 \\ -7 & 7\end{aligned}|+2|\begin{aligned}- \sqrt{5} & 1 \\ 7 \sqrt{5} & 7\end{aligned}|+6|\begin{aligned}- \sqrt{5} & -5 \\ 7 \sqrt{5} & -7\end{aligned}| \\  & =8 \sqrt{5}(-35+7)+2(- 7 \sqrt{5}- 7 \sqrt{5})+6(7 \sqrt{5}+35 \sqrt{5}) \\  & =8 \sqrt{5}\cdot (-28)+2\cdot (- 14 \sqrt{5})+6\cdot 42 \sqrt{5} \\  & =- 224 \sqrt{5}- 28 \sqrt{5}+252 \sqrt{5} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated variant (moderate, seed 41, moderate_roman_nonsingular_singular_det_6, bank_5)

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is **not** a singular matrix
II. $E$ is a singular matrix
III. $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

A. III only
B. I and II only
C. II only
D. I and III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-69835 / field 0

Which of the following statements are true regarding the matrix $T$ given below?

I. $T$ is a singular matrix
II. $det(T)=-3$
III. $T$ is **not** a singular matrix

 

$$
T=[\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}]
$$

- II and III only
- I only
- III only
- I and II only
- II only

Original correct designation: III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}| \\  & =4|\begin{aligned}2 & 3 \\ -1 & 1\end{aligned}|-2|\begin{aligned}1 & 3 \\ -2 & 1\end{aligned}|-1|\begin{aligned}1 & 2 \\ -2 & -1\end{aligned}| \\  & =4(2+3)-2(1+6)-1(-1+4) \\  & =4\cdot 5-2\cdot 7-1\cdot 3 \\  & =20-14-3 \\  & =3\end{aligned}
$$

 

Since $det(T)=3\ne 0$, the matrix is **not** singular. 

Therefore, only statement III is true.

### Parameterized original replay

Which of the following statements are true regarding the matrix $T$ given below?

I. $T$ is a singular matrix
II. $det(T)=-3$
III. $T$ is **not** a singular matrix

$$
T=[\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}]
$$

A. II and III only
B. I only
C. I and II only
D. III only
E. II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}| \\  & =4|\begin{aligned}2 & 3 \\ -1 & 1\end{aligned}|+(-2)|\begin{aligned}1 & 3 \\ -2 & 1\end{aligned}|+(-1)|\begin{aligned}1 & 2 \\ -2 & -1\end{aligned}| \\  & =4(2+3)+(-2)(1+6)+(-1)(-1+4) \\  & =4\cdot 5+(-2)\cdot 7+(-1)\cdot 3 \\  & =20-14-3 \\  & =3\end{aligned}
$$

 

Since $det(T)=3\ne 0$, the matrix is **not** singular. 

Therefore, only statement III is true.

### Generated variant (easy, seed 13, easy_roman_singular_det_nonsingular_6, bank_2)

Which of the following statements are true regarding the matrix $T$ given below?

I. $T$ is a singular matrix
II. $det(T)=0$
III. $T$ is **not** a singular matrix

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

A. II only
B. II and III only
C. I and II only
D. III only
E. I only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated variant (easy, seed 41, easy_roman_singular_det_nonsingular_6, bank_2)

Which of the following statements are true regarding the matrix $F$ given below?

I. $F$ is a singular matrix
II. $det(F)=5$
III. $F$ is **not** a singular matrix

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

A. I only
B. II and III only
C. III only
D. II only
E. I and II only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

## Authored hard example / seed 13

Which of the following statements are true regarding the matrix $E$ given below?

I. $E$ is a singular matrix
II. $E$ is **not** a singular matrix
III. $det(E)=0$

$$
E=[\begin{aligned}\frac{2 \sqrt{7}}{5} & \frac{1}{5} & \sqrt{7} \\ \frac{\sqrt{7}}{5} & - \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5} & - \sqrt{7}\end{aligned}]
$$

A. I and II only
B. II only
C. I and III only
D. I only
E. III only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2 \sqrt{7}}{5} & \frac{1}{5} & \sqrt{7} \\ \frac{\sqrt{7}}{5} & - \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5} & - \sqrt{7}\end{aligned}| \\  & =\frac{2 \sqrt{7}}{5}|\begin{aligned}- \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{4}{5} & - \sqrt{7}\end{aligned}|+(- \frac{1}{5})|\begin{aligned}\frac{\sqrt{7}}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & - \sqrt{7}\end{aligned}|+\sqrt{7}|\begin{aligned}\frac{\sqrt{7}}{5} & - \frac{3}{5} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5}\end{aligned}| \\  & =\frac{2 \sqrt{7}}{5}(\frac{3 \sqrt{7}}{5}- \frac{2 \sqrt{7}}{5})+(- \frac{1}{5})(- \frac{7}{5}- \frac{21}{10})+\sqrt{7}(\frac{4 \sqrt{7}}{25}+\frac{9 \sqrt{7}}{25}) \\  & =\frac{2 \sqrt{7}}{5}\cdot \frac{\sqrt{7}}{5}+(- \frac{1}{5})\cdot (- \frac{7}{2})+\sqrt{7}\cdot \frac{13 \sqrt{7}}{25} \\  & =\frac{14}{25}+\frac{7}{10}+\frac{91}{25} \\  & =\frac{49}{10}\end{aligned}
$$

Since $det(E)=\frac{49}{10}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Authored hard example / seed 41

Which of the following statements are true regarding the matrix $D$ given below?

I. $D$ is a singular matrix
II. $D$ is **not** a singular matrix
III. $det(D)=0$

$$
D=[\begin{aligned}- \frac{4 \sqrt{3}}{5} & - \frac{3}{2} & - \sqrt{3} \\ - \frac{2 \sqrt{3}}{5} & -1 & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}]
$$

A. II and III only
B. I and III  only
C. III only
D. II only
E. I  only

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}- \frac{4 \sqrt{3}}{5} & - \frac{3}{2} & - \sqrt{3} \\ - \frac{2 \sqrt{3}}{5} & -1 & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}| \\  & =(- \frac{4 \sqrt{3}}{5})|\begin{aligned}-1 & - \frac{4 \sqrt{3}}{3} \\ - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}|+\frac{3}{2}|\begin{aligned}- \frac{2 \sqrt{3}}{5} & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{4 \sqrt{3}}{3}\end{aligned}|+(- \sqrt{3})|\begin{aligned}- \frac{2 \sqrt{3}}{5} & -1 \\ \frac{\sqrt{3}}{5} & - \frac{1}{2}\end{aligned}| \\  & =(- \frac{4 \sqrt{3}}{5})(\frac{4 \sqrt{3}}{3}- \frac{2 \sqrt{3}}{3})+\frac{3}{2}(\frac{8}{5}+\frac{4}{5})+(- \sqrt{3})(\frac{\sqrt{3}}{5}+\frac{\sqrt{3}}{5}) \\  & =(- \frac{4 \sqrt{3}}{5})\cdot \frac{2 \sqrt{3}}{3}+\frac{3}{2}\cdot \frac{12}{5}+(- \sqrt{3})\cdot \frac{2 \sqrt{3}}{5} \\  & =- \frac{8}{5}+\frac{18}{5}- \frac{6}{5} \\  & =\frac{4}{5}\end{aligned}
$$

Since $det(D)=\frac{4}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.
