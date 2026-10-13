# Identifying Singular Matrices: review

Database math, basis 1522, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Original captures and preconversion generator artifacts remain in history/basis-1356. Current source records are shown verbatim; all generated records are local review data.

## Original q-128490

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $det(M)=10$
- **II.** $det(M)=-5$
- **III.** $M$ is a singular matrix

 

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}]
$$

Database field keys: I=false, II=false, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ -3\sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|-0|\begin{aligned}0 & 5 \\ -3\sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ -3\sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)-0+\frac{1}{3}(0+9\sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9\sqrt{5} \\  & =-3\sqrt{5}+3\sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $det(M)=10$
- **II.** $det(M)=-5$
- **III.** $M$ is a singular matrix

$$
M=[\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}]
$$

Correct selections: III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}\sqrt{5} & 0 & \frac{1}{3} \\ 0 & 3 & 5 \\ - 3 \sqrt{5} & 3 & 4\end{aligned}| \\  & =\sqrt{5}|\begin{aligned}3 & 5 \\ 3 & 4\end{aligned}|+0|\begin{aligned}0 & 5 \\ - 3 \sqrt{5} & 4\end{aligned}|+\frac{1}{3}|\begin{aligned}0 & 3 \\ - 3 \sqrt{5} & 3\end{aligned}| \\  & =\sqrt{5}(12-15)+0+\frac{1}{3}(0+9 \sqrt{5}) \\  & =\sqrt{5}\cdot (-3)+\frac{1}{3}\cdot 9 \sqrt{5} \\  & =- 3 \sqrt{5}+3 \sqrt{5} \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statement III is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $det(F)=1$
- **III.** $F$ is a singular matrix

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=0$
- **II.** $det(E)=1$
- **III.** $E$ is a singular matrix

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, none of the statements are true.

## Original q-9838

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is a singular matrix
- **III.** $det(F)=-2$

$$
F=[\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}]
$$

Database field keys: I=true, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 5 \\ 7 & 8\end{aligned}|-1|\begin{aligned}3 & 5 \\ 6 & 8\end{aligned}|+2|\begin{aligned}3 & 4 \\ 6 & 7\end{aligned}| \\  & =0-1(24-30)+2(21-24) \\  & =0-1\cdot (-6)+2\cdot (-3) \\  & =6-6 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is a singular matrix
- **III.** $det(F)=-2$

$$
F=[\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 5 \\ 7 & 8\end{aligned}|+(-1)|\begin{aligned}3 & 5 \\ 6 & 8\end{aligned}|+2|\begin{aligned}3 & 4 \\ 6 & 7\end{aligned}| \\  & =0+(-1)(24-30)+2(21-24) \\  & =(-1)\cdot (-6)+2\cdot (-3) \\  & =6-6 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=-6$
- **II.** $E$ is a singular matrix
- **III.** $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is a singular matrix
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128474

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $det(Q)=-5$
- **II.** $det(Q)=1$
- **III.** $Q$ is **not** a singular matrix

$$
Q=[\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}]
$$

Database field keys: I=false, II=false, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}| \\  & =1|\begin{aligned}3 & 1 \\ 5 & 3\end{aligned}|-1|\begin{aligned}2 & 1 \\ 3 & 3\end{aligned}|-1|\begin{aligned}2 & 3 \\ 3 & 5\end{aligned}| \\  & =1(9-5)-1(6-3)-1(10-9) \\  & =1\cdot 4-1\cdot 3-1\cdot 1 \\  & =4-3-1 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $det(Q)=-5$
- **II.** $det(Q)=1$
- **III.** $Q$ is **not** a singular matrix

$$
Q=[\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}1 & 1 & -1 \\ 2 & 3 & 1 \\ 3 & 5 & 3\end{aligned}| \\  & =1|\begin{aligned}3 & 1 \\ 5 & 3\end{aligned}|+(-1)|\begin{aligned}2 & 1 \\ 3 & 3\end{aligned}|+(-1)|\begin{aligned}2 & 3 \\ 3 & 5\end{aligned}| \\  & =1(9-5)+(-1)(6-3)+(-1)(10-9) \\  & =1\cdot 4+(-1)\cdot 3+(-1)\cdot 1 \\  & =4-3-1 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=-6$
- **II.** $det(E)=1$
- **III.** $E$ is **not** a singular matrix

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $det(F)=1$
- **III.** $F$ is **not** a singular matrix

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statement I is true.

## Original q-128476

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=-30$

 

$$
T=[\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}]
$$

Database field keys: I=false, II=true, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ 3 & 1\end{aligned}|-3|\begin{aligned}2 & 1 \\ 1 & 1\end{aligned}|-5|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}| \\  & =1(1-3)-3(2-1)-5(6-1) \\  & =1\cdot (-2)-3\cdot 1-5\cdot 5 \\  & =-2-3-25 \\  & =-30\end{aligned}
$$

 

Since $det(T)=-30\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=-30$

$$
T=[\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}1 & 3 & -5 \\ 2 & 1 & 1 \\ 1 & 3 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ 3 & 1\end{aligned}|+(-3)|\begin{aligned}2 & 1 \\ 1 & 1\end{aligned}|+(-5)|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}| \\  & =1(1-3)+(-3)(2-1)+(-5)(6-1) \\  & =1\cdot (-2)+(-3)\cdot 1+(-5)\cdot 5 \\  & =-2-3-25 \\  & =-30\end{aligned}
$$

 

Since $det(T)=-30\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $T$ is **not** a singular matrix
- **III.** $det(T)=0$

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=5$

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

## Original q-128484

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

 

$$
R=[\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}]
$$

Database field keys: I=true, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}| \\  & =2|\begin{aligned}0 & -1 \\ \sqrt{2} & 4\end{aligned}|-\sqrt{2}|\begin{aligned}\frac{1}{2} & -1 \\ 1 & 4\end{aligned}|+2|\begin{aligned}\frac{1}{2} & 0 \\ 1 & \sqrt{2}\end{aligned}| \\  & =2(0+\sqrt{2})-\sqrt{2}(2+1)+2(\frac{\sqrt{2}}{2}-0) \\  & =2\cdot \sqrt{2}-\sqrt{2}\cdot 3+2\cdot \frac{\sqrt{2}}{2} \\  & =2\sqrt{2}-3\sqrt{2}+\sqrt{2} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

$$
R=[\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}2 & \sqrt{2} & 2 \\ \frac{1}{2} & 0 & -1 \\ 1 & \sqrt{2} & 4\end{aligned}| \\  & =2|\begin{aligned}0 & -1 \\ \sqrt{2} & 4\end{aligned}|+(- \sqrt{2})|\begin{aligned}\frac{1}{2} & -1 \\ 1 & 4\end{aligned}|+2|\begin{aligned}\frac{1}{2} & 0 \\ 1 & \sqrt{2}\end{aligned}| \\  & =2(0+\sqrt{2})+(- \sqrt{2})(2+1)+2(\frac{\sqrt{2}}{2}+0) \\  & =2\cdot \sqrt{2}+(- \sqrt{2})\cdot 3+2\cdot \frac{\sqrt{2}}{2} \\  & =2 \sqrt{2}- 3 \sqrt{2}+\sqrt{2} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=0$
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=0$
- **III.** $det(E)=1$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, none of the statements are true.

## Original q-38179

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not**  a singular matrix
- **III.** $det(E)=-2$

$$
E=[\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}]
$$

Database field keys: I=true, II=false, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}| \\  & =\frac{2}{3}|\begin{aligned}5 & 6 \\ 7 & 8\end{aligned}|-3|\begin{aligned}\frac{2}{3} & 6 \\ \frac{2}{3} & 8\end{aligned}|+4|\begin{aligned}\frac{2}{3} & 5 \\ \frac{2}{3} & 7\end{aligned}| \\  & =\frac{2}{3}(40-42)-3(\frac{16}{3}-\frac{12}{3})+4(\frac{14}{3}-\frac{10}{3}) \\  & =\frac{2}{3}\cdot (-2)-3\cdot \frac{4}{3}+4\cdot \frac{4}{3} \\  & =-\frac{4}{3}-\frac{12}{3}+\frac{16}{3} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=-2$

$$
E=[\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2}{3} & 3 & 4 \\ \frac{2}{3} & 5 & 6 \\ \frac{2}{3} & 7 & 8\end{aligned}| \\  & =\frac{2}{3}|\begin{aligned}5 & 6 \\ 7 & 8\end{aligned}|+(-3)|\begin{aligned}\frac{2}{3} & 6 \\ \frac{2}{3} & 8\end{aligned}|+4|\begin{aligned}\frac{2}{3} & 5 \\ \frac{2}{3} & 7\end{aligned}| \\  & =\frac{2}{3}(40-42)+(-3)(\frac{16}{3}-4)+4(\frac{14}{3}- \frac{10}{3}) \\  & =\frac{2}{3}\cdot (-2)+(-3)\cdot \frac{4}{3}+4\cdot \frac{4}{3} \\  & =- \frac{4}{3}-4+\frac{16}{3} \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $R$ is **not** a singular matrix
- **III.** $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Original q-38182

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $Q$ is **not** a singular matrix
- **II.** $Q$ is a singular matrix
- **III.** $det(Q)=-5$

$$
Q=[\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}]
$$

Database field keys: I=false, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 7 \\ 5 & 8\end{aligned}|-3|\begin{aligned}1 & 7 \\ 2 & 8\end{aligned}|+6|\begin{aligned}1 & 4 \\ 2 & 5\end{aligned}| \\  & =0-3(8-14)+6(5-8) \\  & =0-3\cdot (-6)+6\cdot (-3) \\  & =18-18 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $Q$ given below?

Select all that apply.

- **I.** $Q$ is **not** a singular matrix
- **II.** $Q$ is a singular matrix
- **III.** $det(Q)=-5$

$$
Q=[\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(Q) & =|\begin{aligned}0 & 3 & 6 \\ 1 & 4 & 7 \\ 2 & 5 & 8\end{aligned}| \\  & =0|\begin{aligned}4 & 7 \\ 5 & 8\end{aligned}|+(-3)|\begin{aligned}1 & 7 \\ 2 & 8\end{aligned}|+6|\begin{aligned}1 & 4 \\ 2 & 5\end{aligned}| \\  & =0+(-3)(8-14)+6(5-8) \\  & =(-3)\cdot (-6)+6\cdot (-3) \\  & =18-18 \\  & =0\end{aligned}
$$

Since $det(Q)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is **not** a singular matrix
- **II.** $T$ is a singular matrix
- **III.** $det(T)=0$

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is **not** a singular matrix
- **II.** $F$ is a singular matrix
- **III.** $det(F)=5$

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements I and III are true.

## Original q-69834

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $M$ is a singular matrix
- **II.** $det(M)=1$
- **III.** $det(M)=0$

 

$$
M=[\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}]
$$

Database field keys: I=true, II=false, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}| \\  & =1|\begin{aligned}2 & 3 \\ 4 & -2\end{aligned}|-(-2)|\begin{aligned}1 & 3 \\ -2 & -2\end{aligned}|+1|\begin{aligned}1 & 2 \\ -2 & 4\end{aligned}| \\  & =1(-4-12)+2(-2+6)+1(4+4) \\  & =1\cdot (-16)+2\cdot 4+1\cdot 8 \\  & =-16+8+8 \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $M$ given below?

Select all that apply.

- **I.** $M$ is a singular matrix
- **II.** $det(M)=1$
- **III.** $det(M)=0$

$$
M=[\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(M) & =|\begin{aligned}1 & -2 & 1 \\ 1 & 2 & 3 \\ -2 & 4 & -2\end{aligned}| \\  & =1|\begin{aligned}2 & 3 \\ 4 & -2\end{aligned}|+2|\begin{aligned}1 & 3 \\ -2 & -2\end{aligned}|+1|\begin{aligned}1 & 2 \\ -2 & 4\end{aligned}| \\  & =1(-4-12)+2(-2+6)+1(4+4) \\  & =1\cdot (-16)+2\cdot 4+1\cdot 8 \\  & =-16+8+8 \\  & =0\end{aligned}
$$

 

Since $det(M)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=-6$
- **III.** $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=0$
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-77477

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is **not** a singular matrix

- **II.** $S$ is a singular matrix

- **III.** $det(S)=\sqrt{3}$

$$
S=[\begin{aligned}1 & 2 & \,0 \\ 2 & \sqrt{3} & \,\,-1 \\ \sqrt{3} & 4 & \,\,-\sqrt{3}\end{aligned}]
$$

Database field keys: I=true, II=false, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}1 & 2 & \,0 \\ 2 & \sqrt{3} & \,\,-1 \\ \sqrt{3} & 4 & \,\,-\sqrt{3}\end{aligned}| \\  & =1|\begin{aligned}\sqrt{3} & \,\,-1 \\ 4 & \,\,-\sqrt{3}\end{aligned}|-2|\begin{aligned}2 & \,-1 \\ \sqrt{3} & \,-\sqrt{3}\end{aligned}|+0|\begin{aligned}2 & \sqrt{3} \\ \sqrt{3} & 4\end{aligned}| \\  & =1(-{(\sqrt{3})}^{2}+4)-2(-2\sqrt{3}+\sqrt{3})+0 \\  & =(-3+4)-2\cdot (-\sqrt{3}) \\  & =1+2\sqrt{3}\end{aligned}
$$

Since $det(S)=1+2\sqrt{3}\ne 0$, the matrix is **not ** singular. 

Therefore, only statement I is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is **not** a singular matrix

- **II.** $S$ is a singular matrix

- **III.** $det(S)=\sqrt{3}$

$$
S=[\begin{aligned}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}1 & 2 & 0 \\ 2 & \sqrt{3} & -1 \\ \sqrt{3} & 4 & - \sqrt{3}\end{aligned}| \\  & =1|\begin{aligned}\sqrt{3} & -1 \\ 4 & - \sqrt{3}\end{aligned}|+(-2)|\begin{aligned}2 & -1 \\ \sqrt{3} & - \sqrt{3}\end{aligned}|+0|\begin{aligned}2 & \sqrt{3} \\ \sqrt{3} & 4\end{aligned}| \\  & =1(-3+4)+(-2)(- 2 \sqrt{3}+\sqrt{3})+0 \\  & =(-3+4)+(-2)\cdot (- \sqrt{3}) \\  & =1 + 2 \sqrt{3}\end{aligned}
$$

Since $det(S)=1 + 2 \sqrt{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is **not** a singular matrix

- **II.** $R$ is a singular matrix

- **III.** $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}\cdot \frac{4}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is **not** a singular matrix

- **II.** $E$ is a singular matrix

- **III.** $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =(\frac{1}{3}+\frac{4}{3})+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-77478

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

 

$$
R=[\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}]
$$

Database field keys: I=true, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}| \\  & =\frac{3}{5}|\begin{aligned}2 & 3 \\ \frac{1}{2} & 1\end{aligned}|-\frac{2}{5}|\begin{aligned}1 & 3 \\ 0 & 1\end{aligned}|+\frac{1}{5}|\begin{aligned}1 & 2 \\ 0 & \frac{1}{2}\end{aligned}| \\  & =\frac{3}{5}(2-\frac{3}{2})-\frac{2}{5}(1-0)+\frac{1}{5}(\frac{1}{2}-0) \\  & =\frac{3}{5}\cdot \frac{1}{2}-\frac{2}{5}\cdot 1+\frac{1}{5}\cdot \frac{1}{2} \\  & =\frac{3}{10}-\frac{2}{5}+\frac{1}{10} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $det(R)=0$
- **III.** $det(R)=1$

$$
R=[\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}\frac{3}{5} & \frac{2}{5} & \frac{1}{5} \\ 1 & 2 & 3 \\ 0 & \frac{1}{2} & 1\end{aligned}| \\  & =\frac{3}{5}|\begin{aligned}2 & 3 \\ \frac{1}{2} & 1\end{aligned}|+(- \frac{2}{5})|\begin{aligned}1 & 3 \\ 0 & 1\end{aligned}|+\frac{1}{5}|\begin{aligned}1 & 2 \\ 0 & \frac{1}{2}\end{aligned}| \\  & =\frac{3}{5}(2- \frac{3}{2})+(- \frac{2}{5})(1+0)+\frac{1}{5}(\frac{1}{2}+0) \\  & =\frac{3}{5}\cdot \frac{1}{2}+(- \frac{2}{5})\cdot 1+\frac{1}{5}\cdot \frac{1}{2} \\  & =\frac{3}{10}- \frac{2}{5}+\frac{1}{10} \\  & =0\end{aligned}
$$

 

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=0$
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-5 & \sqrt{3} & -3 \\ 8 & 5 \sqrt{3} & 4 \\ 21 & 9 \sqrt{3} & 11\end{aligned}| \\  & =(-5)|\begin{aligned}5 \sqrt{3} & 4 \\ 9 \sqrt{3} & 11\end{aligned}|+(- \sqrt{3})|\begin{aligned}8 & 4 \\ 21 & 11\end{aligned}|+(-3)|\begin{aligned}8 & 5 \sqrt{3} \\ 21 & 9 \sqrt{3}\end{aligned}| \\  & =(-5)(55 \sqrt{3}- 36 \sqrt{3})+(- \sqrt{3})(88-84)+(-3)(72 \sqrt{3}- 105 \sqrt{3}) \\  & =(-5)\cdot 19 \sqrt{3}+(- \sqrt{3})\cdot 4+(-3)\cdot (- 33 \sqrt{3}) \\  & =- 95 \sqrt{3}- 4 \sqrt{3}+99 \sqrt{3} \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=0$
- **III.** $det(E)=1$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, none of the statements are true.

## Original q-77479

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $P$ is **not**  a singular matrix
- **II.** $P$ is a singular matrix
- **III.** $det(P)=-\frac{1}{2}$

$$
P=[\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}]
$$

Database field keys: I=false, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows: 

$$
\begin{aligned}det(P) & =|\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}| \\  & =\frac{1}{2}|\begin{aligned}2 & \frac{1}{2} \\ 0 & -1\end{aligned}|-1|\begin{aligned}\frac{1}{2} & \frac{1}{2} \\ -1 & -1\end{aligned}|+\frac{1}{2}|\begin{aligned}\frac{1}{2} & 2 \\ -1 & 0\end{aligned}| \\  & =\frac{1}{2}(-2-0)-1(-\frac{1}{2}+\frac{1}{2})+\frac{1}{2}(0+2) \\  & =(-2)\cdot \frac{1}{2}-1\cdot 0+\frac{1}{2}\cdot 2 \\  & =-1+1 \\  & =0\end{aligned}
$$

Since $det(P)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $P$ given below?

Select all that apply.

- **I.** $P$ is **not** a singular matrix
- **II.** $P$ is a singular matrix
- **III.** $det(P)=- \frac{1}{2}$

$$
P=[\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(P) & =|\begin{aligned}\frac{1}{2} & 1 & \frac{1}{2} \\ \frac{1}{2} & 2 & \frac{1}{2} \\ -1 & 0 & -1\end{aligned}| \\  & =\frac{1}{2}|\begin{aligned}2 & \frac{1}{2} \\ 0 & -1\end{aligned}|+(-1)|\begin{aligned}\frac{1}{2} & \frac{1}{2} \\ -1 & -1\end{aligned}|+\frac{1}{2}|\begin{aligned}\frac{1}{2} & 2 \\ -1 & 0\end{aligned}| \\  & =\frac{1}{2}(-2+0)+(-1)(- \frac{1}{2}+\frac{1}{2})+\frac{1}{2}(0+2) \\  & =\frac{1}{2}\cdot (-2)+(-1)\cdot 0+\frac{1}{2}\cdot 2 \\  & =-1+1 \\  & =0\end{aligned}
$$

Since $det(P)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is **not** a singular matrix
- **II.** $R$ is a singular matrix
- **III.** $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is **not** a singular matrix
- **II.** $E$ is a singular matrix
- **III.** $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-9835

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $det(D)=1$
- **II.** $D$ is a singular matrix
- **III.** $det(D)=0$

 

$$
D=[\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}]
$$

Database field keys: I=false, II=true, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}| \\  & =1|\begin{aligned}4 & 5 \\ 6 & 7\end{aligned}|-2|\begin{aligned}1 & 5 \\ 1 & 7\end{aligned}|+3|\begin{aligned}1 & 4 \\ 1 & 6\end{aligned}| \\  & =1(28-30)-2(7-5)+3(6-4) \\  & =1\cdot (-2)-2\cdot 2+3\cdot 2 \\  & =-2-4+6 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $det(D)=1$
- **II.** $D$ is a singular matrix
- **III.** $det(D)=0$

$$
D=[\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}1 & 2 & 3 \\ 1 & 4 & 5 \\ 1 & 6 & 7\end{aligned}| \\  & =1|\begin{aligned}4 & 5 \\ 6 & 7\end{aligned}|+(-2)|\begin{aligned}1 & 5 \\ 1 & 7\end{aligned}|+3|\begin{aligned}1 & 4 \\ 1 & 6\end{aligned}| \\  & =1(28-30)+(-2)(7-5)+3(6-4) \\  & =1\cdot (-2)+(-2)\cdot 2+3\cdot 2 \\  & =-2-4+6 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=-6$
- **II.** $E$ is a singular matrix
- **III.** $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is a singular matrix
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128478

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=-7$
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=-2$

$$
F=[\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}]
$$

Database field keys: I=false, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}| \\  & =2|\begin{aligned}2 & 1 \\ 3 & 1\end{aligned}|-8|\begin{aligned}-1 & 1 \\ 5 & 1\end{aligned}|+3|\begin{aligned}-1 & 2 \\ 5 & 3\end{aligned}| \\  & =2(2-3)-8(-1-5)+3(-3-10) \\  & =2\cdot (-1)-8\cdot (-6)+3\cdot (-13) \\  & =-2+48-39 \\  & =7\end{aligned}
$$

Since $det(F)=7$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=-7$
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=-2$

$$
F=[\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}2 & 8 & 3 \\ -1 & 2 & 1 \\ 5 & 3 & 1\end{aligned}| \\  & =2|\begin{aligned}2 & 1 \\ 3 & 1\end{aligned}|+(-8)|\begin{aligned}-1 & 1 \\ 5 & 1\end{aligned}|+3|\begin{aligned}-1 & 2 \\ 5 & 3\end{aligned}| \\  & =2(2-3)+(-8)(-1-5)+3(-3-10) \\  & =2\cdot (-1)+(-8)\cdot (-6)+3\cdot (-13) \\  & =-2+48-39 \\  & =7\end{aligned}
$$

Since $det(F)=7$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $det(E)=-6$
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: leave all boxes unchecked

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, none of the statements are true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $det(F)=0$
- **II.** $F$ is **not** a singular matrix
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statement I is true.

## Original q-128480

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $D$ is a singular matrix
- **II.** $det(D)=1$
- **III.** $det(D)=0$

$$
D=[\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}]
$$

Database field keys: I=true, II=false, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}| \\  & =2|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|+3|\begin{aligned}-1 & 3 \\ -3 & 2\end{aligned}|+1|\begin{aligned}-1 & 2 \\ -3 & 5\end{aligned}| \\  & =2(4-15)+3(-2+9)+1(-5+6) \\  & =2\cdot (-11)+3\cdot 7+1\cdot 1 \\  & =-22+21+1 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Parameterized replay

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $D$ is a singular matrix
- **II.** $det(D)=1$
- **III.** $det(D)=0$

$$
D=[\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}2 & -3 & 1 \\ -1 & 2 & 3 \\ -3 & 5 & 2\end{aligned}| \\  & =2|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|+3|\begin{aligned}-1 & 3 \\ -3 & 2\end{aligned}|+1|\begin{aligned}-1 & 2 \\ -3 & 5\end{aligned}| \\  & =2(4-15)+3(-2+9)+1(-5+6) \\  & =2\cdot (-11)+3\cdot 7+1\cdot 1 \\  & =-22+21+1 \\  & =0\end{aligned}
$$

 

Since $det(D)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $det(E)=-6$
- **III.** $det(E)=1$

$$
E=[\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}-4 & 3 & 8 \\ -2 & 6 & -1 \\ 0 & -9 & 10\end{aligned}| \\  & =(-4)|\begin{aligned}6 & -1 \\ -9 & 10\end{aligned}|+(-3)|\begin{aligned}-2 & -1 \\ 0 & 10\end{aligned}|+8|\begin{aligned}-2 & 6 \\ 0 & -9\end{aligned}| \\  & =(-4)(60-9)+(-3)(-20+0)+8(18+0) \\  & =(-4)\cdot 51+(-3)\cdot (-20)+8\cdot 18 \\  & =-204+60+144 \\  & =0\end{aligned}
$$

Since $det(E)=0$, the matrix is singular. 

Therefore, only statement I is true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=0$
- **III.** $det(F)=1$

$$
F=[\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}-3 & -3 & 6 \\ 0 & -3 & -1 \\ -3 & -6 & 5\end{aligned}| \\  & =(-3)|\begin{aligned}-3 & -1 \\ -6 & 5\end{aligned}|+3|\begin{aligned}0 & -1 \\ -3 & 5\end{aligned}|+6|\begin{aligned}0 & -3 \\ -3 & -6\end{aligned}| \\  & =(-3)(-15-6)+3(0-3)+6(0-9) \\  & =(-3)\cdot (-21)+3\cdot (-3)+6\cdot (-9) \\  & =63-9-54 \\  & =0\end{aligned}
$$

Since $det(F)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

## Original q-128491

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is a singular matrix
- **II.** $S$ is **not** a singular matrix
- **III.** $det(S)=5+2\sqrt{7}$

$$
S=[\begin{aligned}2\sqrt{7} & 0 & \frac{1}{2} \\ -\sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}]
$$

Database field keys: I=false, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}2\sqrt{7} & 0 & \frac{1}{2} \\ -\sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}| \\  & =2\sqrt{7}|\begin{aligned}2 & 0 \\ 0 & \sqrt{7}\end{aligned}|-0|\begin{aligned}-\sqrt{7} & 0 \\ 5 & \sqrt{7}\end{aligned}|+\frac{1}{2}|\begin{aligned}-\sqrt{7} & 2 \\ 5 & 0\end{aligned}| \\  & =2\sqrt{7}(2\sqrt{7}-0)-0+\frac{1}{2}(0-10) \\  & =2\sqrt{7}\cdot 2\sqrt{7}+\frac{1}{2}\cdot (-10) \\  & =28-5 \\  & =23\end{aligned}
$$

Since $det(S)=23\ne 0$, the matrix is **not ** singular. 

Therefore, only statement II is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $S$ given below?

Select all that apply.

- **I.** $S$ is a singular matrix
- **II.** $S$ is **not** a singular matrix
- **III.** $det(S)=5 + 2 \sqrt{7}$

$$
S=[\begin{aligned}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(S) & =|\begin{aligned}2 \sqrt{7} & 0 & \frac{1}{2} \\ - \sqrt{7} & 2 & 0 \\ 5 & 0 & \sqrt{7}\end{aligned}| \\  & =2 \sqrt{7}|\begin{aligned}2 & 0 \\ 0 & \sqrt{7}\end{aligned}|+0|\begin{aligned}- \sqrt{7} & 0 \\ 5 & \sqrt{7}\end{aligned}|+\frac{1}{2}|\begin{aligned}- \sqrt{7} & 2 \\ 5 & 0\end{aligned}| \\  & =2 \sqrt{7}(2 \sqrt{7}+0)+0+\frac{1}{2}(0-10) \\  & =2 \sqrt{7}\cdot 2 \sqrt{7}+\frac{1}{2}\cdot (-10) \\  & =28-5 \\  & =23\end{aligned}
$$

Since $det(S)=23\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is a singular matrix
- **II.** $R$ is **not** a singular matrix
- **III.** $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

Correct selections: I, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements I and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Original q-38187

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix
- **II.** $N$ is a singular matrix
- **III.** $det(N)=-1$

$$
N=[\begin{aligned}\frac{1}{7} & 3 & -\frac{1}{7} \\ \frac{1}{7} & 4 & -\frac{1}{7} \\ \frac{1}{7} & 5 & -\frac{1}{7}\end{aligned}]
$$

Database field keys: I=false, II=true, III=false

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =|\begin{aligned}\frac{1}{7} & 3 & -\frac{1}{7} \\ \frac{1}{7} & 4 & -\frac{1}{7} \\ \frac{1}{7} & 5 & -\frac{1}{7}\end{aligned}| \\  & =\frac{1}{7}|\begin{aligned}4 & -\frac{1}{7} \\ 5 & -\frac{1}{7}\end{aligned}|-3|\begin{aligned}\frac{1}{7} & -\frac{1}{7} \\ \frac{1}{7} & -\frac{1}{7}\end{aligned}|+(-\frac{1}{7})|\begin{aligned}\frac{1}{7} & 4 \\ \frac{1}{7} & 5\end{aligned}| \\  & =\frac{1}{7}(-\frac{4}{7}+\frac{5}{7})-3(-\frac{1}{49}+\frac{1}{49})-\frac{1}{7}(\frac{5}{7}-\frac{4}{7}) \\  & =\frac{1}{7}\cdot \frac{1}{7}-3\cdot 0-\frac{1}{7}\cdot \frac{1}{7} \\  & =\frac{1}{49}-\frac{1}{49} \\  & =0\end{aligned}
$$

Since $det(N)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $N$ given below?

Select all that apply.

- **I.** $N$ is **not** a singular matrix
- **II.** $N$ is a singular matrix
- **III.** $det(N)=-1$

$$
N=[\begin{aligned}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(N) & =|\begin{aligned}\frac{1}{7} & 3 & - \frac{1}{7} \\ \frac{1}{7} & 4 & - \frac{1}{7} \\ \frac{1}{7} & 5 & - \frac{1}{7}\end{aligned}| \\  & =\frac{1}{7}|\begin{aligned}4 & - \frac{1}{7} \\ 5 & - \frac{1}{7}\end{aligned}|+(-3)|\begin{aligned}\frac{1}{7} & - \frac{1}{7} \\ \frac{1}{7} & - \frac{1}{7}\end{aligned}|+(- \frac{1}{7})|\begin{aligned}\frac{1}{7} & 4 \\ \frac{1}{7} & 5\end{aligned}| \\  & =\frac{1}{7}(- \frac{4}{7}+\frac{5}{7})+(-3)(- \frac{1}{49}+\frac{1}{49})+(- \frac{1}{7})(\frac{5}{7}- \frac{4}{7}) \\  & =\frac{1}{7}\cdot \frac{1}{7}+(-3)\cdot 0+(- \frac{1}{7})\cdot \frac{1}{7} \\  & =\frac{1}{49}- \frac{1}{49} \\  & =0\end{aligned}
$$

Since $det(N)=0$, the matrix is singular. 

Therefore, only statement II is true.

### Generated moderate variant, seed 13

Which of the following statements are true regarding the matrix $R$ given below?

Select all that apply.

- **I.** $R$ is **not** a singular matrix
- **II.** $R$ is a singular matrix
- **III.** $det(R)=0$

$$
R=[\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(R) & =|\begin{aligned}- \frac{1}{3} & -1 & 5 \sqrt{3} \\ \frac{5}{3} & 7 & 8 \sqrt{3} \\ - \frac{7}{3} & -9 & 2 \sqrt{3}\end{aligned}| \\  & =(- \frac{1}{3})|\begin{aligned}7 & 8 \sqrt{3} \\ -9 & 2 \sqrt{3}\end{aligned}|+1|\begin{aligned}\frac{5}{3} & 8 \sqrt{3} \\ - \frac{7}{3} & 2 \sqrt{3}\end{aligned}|+5 \sqrt{3}|\begin{aligned}\frac{5}{3} & 7 \\ - \frac{7}{3} & -9\end{aligned}| \\  & =(- \frac{1}{3})(14 \sqrt{3}+72 \sqrt{3})+1(\frac{10 \sqrt{3}}{3}+\frac{56 \sqrt{3}}{3})+5 \sqrt{3}(-15+\frac{49}{3}) \\  & =(- \frac{1}{3})\cdot 86 \sqrt{3}+1\cdot 22 \sqrt{3}+5 \sqrt{3}\cdot \frac{4}{3} \\  & =- \frac{86 \sqrt{3}}{3}+22 \sqrt{3}+\frac{20 \sqrt{3}}{3} \\  & =0\end{aligned}
$$

Since $det(R)=0$, the matrix is singular. 

Therefore, only statements II and III are true.

### Generated moderate variant, seed 41

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is **not** a singular matrix
- **II.** $E$ is a singular matrix
- **III.** $det(E)=0$

$$
E=[\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}]
$$

Correct selections: I

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}1 & 0 & - \frac{2}{3} \\ -3 & 1 & \frac{4}{3} \\ 3 & -1 & \frac{1}{3}\end{aligned}| \\  & =1|\begin{aligned}1 & \frac{4}{3} \\ -1 & \frac{1}{3}\end{aligned}|+0|\begin{aligned}-3 & \frac{4}{3} \\ 3 & \frac{1}{3}\end{aligned}|+(- \frac{2}{3})|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(\frac{1}{3}+\frac{4}{3})+0+(- \frac{2}{3})(3-3) \\  & =1\cdot \frac{5}{3}+(- \frac{2}{3})\cdot 0 \\  & =\frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

Since $det(E)=\frac{5}{3}\ne 0$, the matrix is **not** singular. 

Therefore, only statement I is true.

## Original q-69835

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=-3$
- **III.** $T$ is **not** a singular matrix

 

$$
T=[\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}]
$$

Database field keys: I=false, II=false, III=true

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}| \\  & =4|\begin{aligned}2 & 3 \\ -1 & 1\end{aligned}|-2|\begin{aligned}1 & 3 \\ -2 & 1\end{aligned}|-1|\begin{aligned}1 & 2 \\ -2 & -1\end{aligned}| \\  & =4(2+3)-2(1+6)-1(-1+4) \\  & =4\cdot 5-2\cdot 7-1\cdot 3 \\  & =20-14-3 \\  & =3\end{aligned}
$$

 

Since $det(T)=3\ne 0$, the matrix is **not** singular. 

Therefore, only statement III is true.

### Parameterized replay

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=-3$
- **III.** $T$ is **not** a singular matrix

$$
T=[\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}]
$$

Correct selections: III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:  

$$
\begin{aligned}det(T) & =|\begin{aligned}4 & 2 & -1 \\ 1 & 2 & 3 \\ -2 & -1 & 1\end{aligned}| \\  & =4|\begin{aligned}2 & 3 \\ -1 & 1\end{aligned}|+(-2)|\begin{aligned}1 & 3 \\ -2 & 1\end{aligned}|+(-1)|\begin{aligned}1 & 2 \\ -2 & -1\end{aligned}| \\  & =4(2+3)+(-2)(1+6)+(-1)(-1+4) \\  & =4\cdot 5+(-2)\cdot 7+(-1)\cdot 3 \\  & =20-14-3 \\  & =3\end{aligned}
$$

 

Since $det(T)=3\ne 0$, the matrix is **not** singular. 

Therefore, only statement III is true.

### Generated easy variant, seed 13

Which of the following statements are true regarding the matrix $T$ given below?

Select all that apply.

- **I.** $T$ is a singular matrix
- **II.** $det(T)=0$
- **III.** $T$ is **not** a singular matrix

$$
T=[\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}]
$$

Correct selections: I, II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(T) & =|\begin{aligned}-1 & -1 & 5 \\ 5 & 7 & 8 \\ -7 & -9 & 2\end{aligned}| \\  & =(-1)|\begin{aligned}7 & 8 \\ -9 & 2\end{aligned}|+1|\begin{aligned}5 & 8 \\ -7 & 2\end{aligned}|+5|\begin{aligned}5 & 7 \\ -7 & -9\end{aligned}| \\  & =(-1)(14+72)+1(10+56)+5(-45+49) \\  & =(-1)\cdot 86+1\cdot 66+5\cdot 4 \\  & =-86+66+20 \\  & =0\end{aligned}
$$

Since $det(T)=0$, the matrix is singular. 

Therefore, only statements I and II are true.

### Generated easy variant, seed 41

Which of the following statements are true regarding the matrix $F$ given below?

Select all that apply.

- **I.** $F$ is a singular matrix
- **II.** $det(F)=5$
- **III.** $F$ is **not** a singular matrix

$$
F=[\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}]
$$

Correct selections: II, III

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(F) & =|\begin{aligned}1 & 0 & -2 \\ -3 & 1 & 4 \\ 3 & -1 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 4 \\ -1 & 1\end{aligned}|+0|\begin{aligned}-3 & 4 \\ 3 & 1\end{aligned}|+(-2)|\begin{aligned}-3 & 1 \\ 3 & -1\end{aligned}| \\  & =1(1+4)+0+(-2)(3-3) \\  & =1\cdot 5+(-2)\cdot 0 \\  & =5 \\  & =5\end{aligned}
$$

Since $det(F)=5\ne 0$, the matrix is **not** singular. 

Therefore, only statements II and III are true.

## Authored hard example, seed 13

Which of the following statements are true regarding the matrix $E$ given below?

Select all that apply.

- **I.** $E$ is a singular matrix
- **II.** $E$ is **not** a singular matrix
- **III.** $det(E)=0$

$$
E=[\begin{aligned}\frac{2 \sqrt{7}}{5} & \frac{1}{5} & \sqrt{7} \\ \frac{\sqrt{7}}{5} & - \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5} & - \sqrt{7}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(E) & =|\begin{aligned}\frac{2 \sqrt{7}}{5} & \frac{1}{5} & \sqrt{7} \\ \frac{\sqrt{7}}{5} & - \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5} & - \sqrt{7}\end{aligned}| \\  & =\frac{2 \sqrt{7}}{5}|\begin{aligned}- \frac{3}{5} & \frac{\sqrt{7}}{2} \\ \frac{4}{5} & - \sqrt{7}\end{aligned}|+(- \frac{1}{5})|\begin{aligned}\frac{\sqrt{7}}{5} & \frac{\sqrt{7}}{2} \\ \frac{3 \sqrt{7}}{5} & - \sqrt{7}\end{aligned}|+\sqrt{7}|\begin{aligned}\frac{\sqrt{7}}{5} & - \frac{3}{5} \\ \frac{3 \sqrt{7}}{5} & \frac{4}{5}\end{aligned}| \\  & =\frac{2 \sqrt{7}}{5}(\frac{3 \sqrt{7}}{5}- \frac{2 \sqrt{7}}{5})+(- \frac{1}{5})(- \frac{7}{5}- \frac{21}{10})+\sqrt{7}(\frac{4 \sqrt{7}}{25}+\frac{9 \sqrt{7}}{25}) \\  & =\frac{2 \sqrt{7}}{5}\cdot \frac{\sqrt{7}}{5}+(- \frac{1}{5})\cdot (- \frac{7}{2})+\sqrt{7}\cdot \frac{13 \sqrt{7}}{25} \\  & =\frac{14}{25}+\frac{7}{10}+\frac{91}{25} \\  & =\frac{49}{10}\end{aligned}
$$

Since $det(E)=\frac{49}{10}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.

## Authored hard example, seed 41

Which of the following statements are true regarding the matrix $D$ given below?

Select all that apply.

- **I.** $D$ is a singular matrix
- **II.** $D$ is **not** a singular matrix
- **III.** $det(D)=0$

$$
D=[\begin{aligned}- \frac{4 \sqrt{3}}{5} & - \frac{3}{2} & - \sqrt{3} \\ - \frac{2 \sqrt{3}}{5} & -1 & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}]
$$

Correct selections: II

Remember that a square matrix is singular if its determinant is equal to $0.$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}det(D) & =|\begin{aligned}- \frac{4 \sqrt{3}}{5} & - \frac{3}{2} & - \sqrt{3} \\ - \frac{2 \sqrt{3}}{5} & -1 & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}| \\  & =(- \frac{4 \sqrt{3}}{5})|\begin{aligned}-1 & - \frac{4 \sqrt{3}}{3} \\ - \frac{1}{2} & - \frac{4 \sqrt{3}}{3}\end{aligned}|+\frac{3}{2}|\begin{aligned}- \frac{2 \sqrt{3}}{5} & - \frac{4 \sqrt{3}}{3} \\ \frac{\sqrt{3}}{5} & - \frac{4 \sqrt{3}}{3}\end{aligned}|+(- \sqrt{3})|\begin{aligned}- \frac{2 \sqrt{3}}{5} & -1 \\ \frac{\sqrt{3}}{5} & - \frac{1}{2}\end{aligned}| \\  & =(- \frac{4 \sqrt{3}}{5})(\frac{4 \sqrt{3}}{3}- \frac{2 \sqrt{3}}{3})+\frac{3}{2}(\frac{8}{5}+\frac{4}{5})+(- \sqrt{3})(\frac{\sqrt{3}}{5}+\frac{\sqrt{3}}{5}) \\  & =(- \frac{4 \sqrt{3}}{5})\cdot \frac{2 \sqrt{3}}{3}+\frac{3}{2}\cdot \frac{12}{5}+(- \sqrt{3})\cdot \frac{2 \sqrt{3}}{5} \\  & =- \frac{8}{5}+\frac{18}{5}- \frac{6}{5} \\  & =\frac{4}{5}\end{aligned}
$$

Since $det(D)=\frac{4}{5}\ne 0$, the matrix is **not** singular. 

Therefore, only statement II is true.
