# 3x3 determinant review

Math basis 1356. Originals retain captured evidence. Generated records are labeled; radio options include correct designations for reviewer use only.

## Original q-38128

Find the value of $\begin{vmatrix}2 & 0 & 0 \\ 0 & 7 & 0 \\ 0 & 0 & -3\end{vmatrix}$.

Original answer values: 14, -42, 21, -14, -21.

No worked solution or correct ref supplied.

### Parameterized replay

## Generated easy
Template: `legacy_radio`; bank: `diagonal`; origin: observed.

Find the value of $\begin{vmatrix}2 & 0 & 0 \\ 0 & 7 & 0 \\ 0 & 0 & -3\end{vmatrix}$.

- $-21$
- $-42$ (correct)
- $-14$
- $14$
- $21$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}2 & 0 & 0 \\ 0 & 7 & 0 \\ 0 & 0 & -3\end{aligned}| & =2|\begin{aligned}7 & 0 \\ 0 & -3\end{aligned}|-0|\begin{aligned}0 & 0 \\ 0 & -3\end{aligned}|+0|\begin{aligned}0 & 7 \\ 0 & 0\end{aligned}| \\  & =2(-21-0)+0+0 \\  & =2\cdot (-21) \\  & =-42\end{aligned}
$$

## Original q-9841

Find the value of $\begin{vmatrix}0 & -1 & 3 \\ 2 & 0 & 1 \\ 7 & -1 & 0\end{vmatrix}$.

Original answer values: 32, -13, 47, 0, -15.

No worked solution or correct ref supplied.

### Parameterized replay

## Generated easy
Template: `legacy_radio`; bank: `legacy_zero_diagonal`; origin: observed.

Find the value of $\begin{vmatrix}0 & -1 & 3 \\ 2 & 0 & 1 \\ 7 & -1 & 0\end{vmatrix}$.

- $-15$
- $-13$ (correct)
- $0$
- $32$
- $47$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & -1 & 3 \\ 2 & 0 & 1 \\ 7 & -1 & 0\end{aligned}| & =0|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|-(-1)|\begin{aligned}2 & 1 \\ 7 & 0\end{aligned}|+3|\begin{aligned}2 & 0 \\ 7 & -1\end{aligned}| \\  & =0+1(0-7)+3(-2-0) \\  & =1\cdot (-7)+3\cdot (-2) \\  & =-7-6 \\  & =-13\end{aligned}
$$

## Original q-128309

Find the value of $|\begin{aligned}-2 & 1 & 1 \\ 1 & 4 & 0 \\ 5 & -3 & 1\end{aligned}|.$

Original answer values: 20, -5, 12, 8, -32.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-2 & 1 & 1 \\ 1 & 4 & 0 \\ 5 & -3 & 1\end{aligned}| & =-2|\begin{aligned}4 & 0 \\ -3 & 1\end{aligned}|-1|\begin{aligned}1 & 0 \\ 5 & 1\end{aligned}|+1|\begin{aligned}1 & 4 \\ 5 & -3\end{aligned}| \\  & =-2(4-0)-1(1-0)-1(-3-20) \\  & =-2\cdot 4-1\cdot 1+1\cdot (-23) \\  & =-8-1-23 \\  & =-32\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero`; origin: observed.

Find the value of $|\begin{aligned}-2 & 1 & 1 \\ 1 & 4 & 0 \\ 5 & -3 & 1\end{aligned}|.$

- $8$
- $-32$ (correct)
- $12$
- $20$
- $-5$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-2 & 1 & 1 \\ 1 & 4 & 0 \\ 5 & -3 & 1\end{aligned}| & =(-2)|\begin{aligned}4 & 0 \\ -3 & 1\end{aligned}|-1|\begin{aligned}1 & 0 \\ 5 & 1\end{aligned}|+1|\begin{aligned}1 & 4 \\ 5 & -3\end{aligned}| \\  & =(-2)(4-0)+(-1)(1-0)+1(-3-20) \\  & =(-2)\cdot 4+(-1)\cdot 1+1\cdot (-23) \\  & =-8-1-23 \\  & =-32\end{aligned}
$$

## Original q-275585

If $A=[\begin{aligned}-5 & 3 & 0 \\ 1 & 7 & 5 \\ 0 & -2 & -3\end{aligned}],$ then $det(A)=${{field-1}}.

Original answer values: 64.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-5 & 3 & 0 \\ 1 & 7 & 5 \\ 0 & -2 & -3\end{aligned}| & =-5|\begin{aligned}7 & 5 \\ -2 & -3\end{aligned}|-3|\begin{aligned}1 & 5 \\ 0 & -3\end{aligned}|+0|\begin{aligned}1 & 7 \\ 0 & -2\end{aligned}| \\  & =-5(-21-(-10))-3(-3-0)+0 \\  & =-5\cdot (-11)-3\cdot (-3) \\  & =55+9 \\  & =64\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}-5 & 3 & 0 \\ 1 & 7 & 5 \\ 0 & -2 & -3\end{aligned}],$ then $det(A)=${{field-1}}.

- $64$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-5 & 3 & 0 \\ 1 & 7 & 5 \\ 0 & -2 & -3\end{aligned}| & =(-5)|\begin{aligned}7 & 5 \\ -2 & -3\end{aligned}|-3|\begin{aligned}1 & 5 \\ 0 & -3\end{aligned}|+0|\begin{aligned}1 & 7 \\ 0 & -2\end{aligned}| \\  & =(-5)(-21-(-10))+(-3)(-3-0)+0 \\  & =(-5)\cdot (-11)+(-3)\cdot (-3) \\  & =55+9 \\  & =64\end{aligned}
$$

## Original q-280387

If $H=[\begin{aligned}0 & 7 & 2 \\ 1 & 0 & -5 \\ 4 & -3 & 0\end{aligned}],$ then $det(H)=${{field-1}}.

Original answer values: -146.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 7 & 2 \\ 1 & 0 & -5 \\ 4 & -3 & 0\end{aligned}| & =0|\begin{aligned}0 & -5 \\ -3 & 0\end{aligned}|-7|\begin{aligned}1 & -5 \\ 4 & 0\end{aligned}|+2|\begin{aligned}1 & 0 \\ 4 & -3\end{aligned}| \\  & =0-7(0-(-20))+2(-3-0) \\  & =-7\cdot (20)+2\cdot (-3) \\  & =-140-6 \\  & =-146\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $H=[\begin{aligned}0 & 7 & 2 \\ 1 & 0 & -5 \\ 4 & -3 & 0\end{aligned}],$ then $det(H)=${{field-1}}.

- $-146$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 7 & 2 \\ 1 & 0 & -5 \\ 4 & -3 & 0\end{aligned}| & =0|\begin{aligned}0 & -5 \\ -3 & 0\end{aligned}|-7|\begin{aligned}1 & -5 \\ 4 & 0\end{aligned}|+2|\begin{aligned}1 & 0 \\ 4 & -3\end{aligned}| \\  & =0+(-7)(0-(-20))+2(-3-0) \\  & =(-7)\cdot 20+2\cdot (-3) \\  & =-140-6 \\  & =-146\end{aligned}
$$

## Original q-280390

If $A=[\begin{aligned}0 & 2 & -3 \\ 0 & 0 & 5 \\ 0 & 0 & 4\end{aligned}],$ then $det(A)=${{field-1}}.

Original answer values: 0.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 2 & -3 \\ 0 & 0 & 5 \\ 0 & 0 & 4\end{aligned}| & =0|\begin{aligned}0 & 5 \\ 0 & 4\end{aligned}|-2|\begin{aligned}0 & 5 \\ 0 & 4\end{aligned}|+(-3)|\begin{aligned}0 & 0 \\ 0 & 0\end{aligned}| \\  & =0-2(0-0)-3(0-0) \\  & =0\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}0 & 2 & -3 \\ 0 & 0 & 5 \\ 0 & 0 & 4\end{aligned}],$ then $det(A)=${{field-1}}.

- $0$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 2 & -3 \\ 0 & 0 & 5 \\ 0 & 0 & 4\end{aligned}| & =0|\begin{aligned}0 & 5 \\ 0 & 4\end{aligned}|-2|\begin{aligned}0 & 5 \\ 0 & 4\end{aligned}|+(-3)|\begin{aligned}0 & 0 \\ 0 & 0\end{aligned}| \\  & =0+(-2)(0-0)+(-3)(0-0) \\  & =0\end{aligned}
$$

## Original q-280393

If $Q=[\begin{aligned}3 & -2 & 5 \\ 4 & 1 & 0 \\ -1 & 3 & 2\end{aligned}],$ then $det(Q)=${{field-1}}.

Original answer values: 87.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}3 & -2 & 5 \\ 4 & 1 & 0 \\ -1 & 3 & 2\end{aligned}| & =3|\begin{aligned}1 & 0 \\ 3 & 2\end{aligned}|-(-2)|\begin{aligned}4 & 0 \\ -1 & 2\end{aligned}|+5|\begin{aligned}4 & 1 \\ -1 & 3\end{aligned}| \\  & =3(1\cdot 2-0\cdot 3)+2(4\cdot 2-0\cdot (-1))+5(4\cdot 3-1\cdot (-1)) \\  & =3(2)+2(8)+5(12+1) \\  & =6+16+5(13) \\  & =6+16+65 \\  & =87\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}3 & -2 & 5 \\ 4 & 1 & 0 \\ -1 & 3 & 2\end{aligned}],$ then $det(Q)=${{field-1}}.

- $87$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}3 & -2 & 5 \\ 4 & 1 & 0 \\ -1 & 3 & 2\end{aligned}| & =3|\begin{aligned}1 & 0 \\ 3 & 2\end{aligned}|-(-2)|\begin{aligned}4 & 0 \\ -1 & 2\end{aligned}|+5|\begin{aligned}4 & 1 \\ -1 & 3\end{aligned}| \\  & =3(1\cdot 2-0\cdot 3)+2(4\cdot 2-0\cdot (-1))+5(4\cdot 3-1\cdot (-1)) \\  & =3(2-0)+2(8-0)+5(12-(-1)) \\  & =3\cdot 2+2\cdot 8+5\cdot 13 \\  & =6+16+65 \\  & =87\end{aligned}
$$

## Original q-280394

If $R=[\begin{aligned}1 & -2 & 0 \\ 4 & 3 & 5 \\ 6 & -1 & 2\end{aligned}],$ then $det(R)=${{field-1}}.

Original answer values: -33.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & -2 & 0 \\ 4 & 3 & 5 \\ 6 & -1 & 2\end{aligned}| & =1|\begin{aligned}3 & 5 \\ -1 & 2\end{aligned}|-(-2)|\begin{aligned}4 & 5 \\ 6 & 2\end{aligned}|+0|\begin{aligned}4 & 3 \\ 6 & -1\end{aligned}| \\  & =1(3\cdot 2-5\cdot (-1))+2(4\cdot 2-5\cdot 6)+0 \\  & =1(6+5)+2(8-30) \\  & =11+2(-22) \\  & =11-44 \\  & =-33\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $R=[\begin{aligned}1 & -2 & 0 \\ 4 & 3 & 5 \\ 6 & -1 & 2\end{aligned}],$ then $det(R)=${{field-1}}.

- $-33$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & -2 & 0 \\ 4 & 3 & 5 \\ 6 & -1 & 2\end{aligned}| & =1|\begin{aligned}3 & 5 \\ -1 & 2\end{aligned}|-(-2)|\begin{aligned}4 & 5 \\ 6 & 2\end{aligned}|+0|\begin{aligned}4 & 3 \\ 6 & -1\end{aligned}| \\  & =1(3\cdot 2-5\cdot (-1))+2(4\cdot 2-5\cdot 6)+0 \\  & =1(6-(-5))+2(8-30)+0 \\  & =1\cdot 11+2\cdot (-22) \\  & =11-44 \\  & =-33\end{aligned}
$$

## Original q-280400

If $W=[\begin{aligned}5 & -2 & 3 \\ -1 & 4 & 6 \\ 2 & -3 & 1\end{aligned}],$ then $det(W)=${{field-1}}.

Original answer values: 69.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}5 & -2 & 3 \\ -1 & 4 & 6 \\ 2 & -3 & 1\end{aligned}| & =5|\begin{aligned}4 & 6 \\ -3 & 1\end{aligned}|-(-2)|\begin{aligned}-1 & 6 \\ 2 & 1\end{aligned}|+3|\begin{aligned}-1 & 4 \\ 2 & -3\end{aligned}| \\  & =5(4\cdot 1-6\cdot (-3))+2((-1)(1)-6\cdot 2)+3((-1)(-3)-4\cdot 2) \\  & =5(4+18)+2(-1-12)+3(3-8) \\  & =5(22)+2(-13)+3(-5) \\  & =110-26-15 \\  & =69\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $W=[\begin{aligned}5 & -2 & 3 \\ -1 & 4 & 6 \\ 2 & -3 & 1\end{aligned}],$ then $det(W)=${{field-1}}.

- $69$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}5 & -2 & 3 \\ -1 & 4 & 6 \\ 2 & -3 & 1\end{aligned}| & =5|\begin{aligned}4 & 6 \\ -3 & 1\end{aligned}|-(-2)|\begin{aligned}-1 & 6 \\ 2 & 1\end{aligned}|+3|\begin{aligned}-1 & 4 \\ 2 & -3\end{aligned}| \\  & =5(4\cdot 1-6\cdot (-3))+2((-1)\cdot 1-6\cdot 2)+3((-1)\cdot (-3)-4\cdot 2) \\  & =5(4-(-18))+2(-1-12)+3(3-8) \\  & =5\cdot 22+2\cdot (-13)+3\cdot (-5) \\  & =110-26-15 \\  & =69\end{aligned}
$$

## Original q-38100

Find the value of $|\begin{aligned}1 & -1 & 2 \\ 0 & 4 & 1 \\ 0 & 0 & 8\end{aligned}|.$

Original answer values: 24, -24, 15, 32, 18.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & -1 & 2 \\ 0 & 4 & 1 \\ 0 & 0 & 8\end{aligned}| & =1|\begin{aligned}4 & 1 \\ 0 & 8\end{aligned}|-(-1)|\begin{aligned}0 & 1 \\ 0 & 8\end{aligned}|+2|\begin{aligned}0 & 4 \\ 0 & 0\end{aligned}| \\  & =1(32-0)+1(0-0)+2(0-0) \\  & =1\cdot 32 \\  & =32\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `upper_triangular`; origin: observed.

Find the value of $|\begin{aligned}1 & -1 & 2 \\ 0 & 4 & 1 \\ 0 & 0 & 8\end{aligned}|.$

- $18$
- $32$ (correct)
- $15$
- $24$
- $-24$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & -1 & 2 \\ 0 & 4 & 1 \\ 0 & 0 & 8\end{aligned}| & =1|\begin{aligned}4 & 1 \\ 0 & 8\end{aligned}|-(-1)|\begin{aligned}0 & 1 \\ 0 & 8\end{aligned}|+2|\begin{aligned}0 & 4 \\ 0 & 0\end{aligned}| \\  & =1(32-0)+1(0-0)+2(0-0) \\  & =1\cdot 32 \\  & =32\end{aligned}
$$

## Original q-38124

Find the value of $|\begin{aligned}1 & 0 & 0 \\ 4 & -1 & 0 \\ 2 & -6 & -4\end{aligned}|.$

Original answer values: 8, 4, -12, -8, 24.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & 0 & 0 \\ 4 & -1 & 0 \\ 2 & -6 & -4\end{aligned}| & =1|\begin{aligned}-1 & 0 \\ -6 & -4\end{aligned}|-0|\begin{aligned}4 & 0 \\ 2 & -4\end{aligned}|+0|\begin{aligned}4 & -1 \\ 2 & -6\end{aligned}| \\  & =1(4-0)-0+0 \\  & =1\cdot 4 \\  & =4\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `lower_triangular`; origin: observed.

Find the value of $|\begin{aligned}1 & 0 & 0 \\ 4 & -1 & 0 \\ 2 & -6 & -4\end{aligned}|.$

- $24$
- $4$ (correct)
- $-8$
- $8$
- $-12$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & 0 & 0 \\ 4 & -1 & 0 \\ 2 & -6 & -4\end{aligned}| & =1|\begin{aligned}-1 & 0 \\ -6 & -4\end{aligned}|-0|\begin{aligned}4 & 0 \\ 2 & -4\end{aligned}|+0|\begin{aligned}4 & -1 \\ 2 & -6\end{aligned}| \\  & =1(4-0)+0+0 \\  & =1\cdot 4 \\  & =4\end{aligned}
$$

## Original q-38174

Find the value of $|\begin{aligned}-1 & 0 & 3 \\ 0 & 5 & 2 \\ 1 & 0 & -4\end{aligned}|.$

Original answer values: -23, 15, -20, 5, 20.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-1 & 0 & 3 \\ 0 & 5 & 2 \\ 1 & 0 & -4\end{aligned}| & =(-1)|\begin{aligned}5 & 2 \\ 0 & -4\end{aligned}|-0|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|+3|\begin{aligned}0 & 5 \\ 1 & 0\end{aligned}| \\  & =-1(-20-0)-0+3(0-5) \\  & =(-1)\cdot (-20)+3\cdot (-5) \\  & =20-15 \\  & =5\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `sparse_two_terms`; origin: observed.

Find the value of $|\begin{aligned}-1 & 0 & 3 \\ 0 & 5 & 2 \\ 1 & 0 & -4\end{aligned}|.$

- $20$
- $5$ (correct)
- $-20$
- $-23$
- $15$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-1 & 0 & 3 \\ 0 & 5 & 2 \\ 1 & 0 & -4\end{aligned}| & =(-1)|\begin{aligned}5 & 2 \\ 0 & -4\end{aligned}|-0|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|+3|\begin{aligned}0 & 5 \\ 1 & 0\end{aligned}| \\  & =(-1)(-20-0)+0+3(0-5) \\  & =(-1)\cdot (-20)+3\cdot (-5) \\  & =20-15 \\  & =5\end{aligned}
$$

## Original q-38176

Find the value of $|\begin{aligned}6 & 0 & 7 \\ 0 & 2 & 0 \\ 1 & 0 & -1\end{aligned}|.$

Original answer values: -12, -14, -2, -26, 2.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}6 & 0 & 7 \\ 0 & 2 & 0 \\ 1 & 0 & -1\end{aligned}| & =6|\begin{aligned}2 & 0 \\ 0 & -1\end{aligned}|-0|\begin{aligned}0 & 0 \\ 1 & -1\end{aligned}|+7|\begin{aligned}0 & 2 \\ 1 & 0\end{aligned}| \\  & =6(-2-0)-0+7(0-2) \\  & =6\cdot (-2)+7\cdot (-2) \\  & =-12-14 \\  & =-26\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `sparse_second_column`; origin: observed.

Find the value of $|\begin{aligned}6 & 0 & 7 \\ 0 & 2 & 0 \\ 1 & 0 & -1\end{aligned}|.$

- $2$
- $-26$ (correct)
- $-2$
- $-12$
- $-14$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}6 & 0 & 7 \\ 0 & 2 & 0 \\ 1 & 0 & -1\end{aligned}| & =6|\begin{aligned}2 & 0 \\ 0 & -1\end{aligned}|-0|\begin{aligned}0 & 0 \\ 1 & -1\end{aligned}|+7|\begin{aligned}0 & 2 \\ 1 & 0\end{aligned}| \\  & =6(-2-0)+0+7(0-2) \\  & =6\cdot (-2)+7\cdot (-2) \\  & =-12-14 \\  & =-26\end{aligned}
$$

## Original q-38180

Find the value of $|\begin{aligned}0 & -1 & 3 \\ 1 & 0 & 2 \\ 3 & -2 & 0\end{aligned}|.$

Original answer values: -12, 0, 6, 12, -6.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & -1 & 3 \\ 1 & 0 & 2 \\ 3 & -2 & 0\end{aligned}| & =0|\begin{aligned}0 & 2 \\ -2 & 0\end{aligned}|-(-1)|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|+3|\begin{aligned}1 & 0 \\ 3 & -2\end{aligned}| \\  & =0+1(0-6)+3(-2-0) \\  & =1\cdot (-6)+3\cdot (-2) \\  & =-6-6 \\  & =-12\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `zero_diagonal`; origin: observed.

Find the value of $|\begin{aligned}0 & -1 & 3 \\ 1 & 0 & 2 \\ 3 & -2 & 0\end{aligned}|.$

- $-6$
- $-12$ (correct)
- $12$
- $0$
- $6$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & -1 & 3 \\ 1 & 0 & 2 \\ 3 & -2 & 0\end{aligned}| & =0|\begin{aligned}0 & 2 \\ -2 & 0\end{aligned}|-(-1)|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|+3|\begin{aligned}1 & 0 \\ 3 & -2\end{aligned}| \\  & =0+1(0-6)+3(-2-0) \\  & =1\cdot (-6)+3\cdot (-2) \\  & =-6-6 \\  & =-12\end{aligned}
$$

## Original q-128308

Find the value of $|\begin{aligned}7 & 1 & -3 \\ 0 & 3 & 1 \\ -3 & 1 & 2\end{aligned}|.$

Original answer values: 12, 1, -1, 5, -19.

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 1 & -3 \\ 0 & 3 & 1 \\ -3 & 1 & 2\end{aligned}| & =7|\begin{aligned}3 & 1 \\ 1 & 2\end{aligned}|-1|\begin{aligned}0 & 1 \\ -3 & 2\end{aligned}|-3|\begin{aligned}0 & 3 \\ -3 & 1\end{aligned}| \\  & =7(6-1)-1(0+3)-3(0+9) \\  & =7\cdot 5-1\cdot 3-3\cdot 9 \\  & =35-3-27 \\  & =5\end{aligned}
$$

### Parameterized replay

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero_b`; origin: observed.

Find the value of $|\begin{aligned}7 & 1 & -3 \\ 0 & 3 & 1 \\ -3 & 1 & 2\end{aligned}|.$

- $-19$
- $5$ (correct)
- $-1$
- $12$
- $1$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 1 & -3 \\ 0 & 3 & 1 \\ -3 & 1 & 2\end{aligned}| & =7|\begin{aligned}3 & 1 \\ 1 & 2\end{aligned}|-1|\begin{aligned}0 & 1 \\ -3 & 2\end{aligned}|+(-3)|\begin{aligned}0 & 3 \\ -3 & 1\end{aligned}| \\  & =7(6-1)+(-1)(0-(-3))+(-3)(0-(-9)) \\  & =7\cdot 5+(-1)\cdot 3+(-3)\cdot 9 \\  & =35-3-27 \\  & =5\end{aligned}
$$

# Clearly labeled generated variants

Two variants for every observed bank and every applicable level/template; moderate and hard are authored extensions.

## Generated easy
Template: `legacy_radio`; bank: `diagonal`; origin: observed.

Find the value of $\begin{vmatrix}7 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 6\end{vmatrix}$.

- $6$
- $-7$
- $-42$ (correct)
- $-6$
- $7$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 6\end{aligned}| & =7|\begin{aligned}-1 & 0 \\ 0 & 6\end{aligned}|-0|\begin{aligned}0 & 0 \\ 0 & 6\end{aligned}|+0|\begin{aligned}0 & -1 \\ 0 & 0\end{aligned}| \\  & =7(-6-0)+0+0 \\  & =7\cdot (-6) \\  & =-42\end{aligned}
$$

## Generated easy
Template: `legacy_radio`; bank: `diagonal`; origin: observed.

Find the value of $\begin{vmatrix}-5 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 7\end{vmatrix}$.

- $-21$
- $15$
- $21$
- $-105$ (correct)
- $-15$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-5 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 7\end{aligned}| & =(-5)|\begin{aligned}3 & 0 \\ 0 & 7\end{aligned}|-0|\begin{aligned}0 & 0 \\ 0 & 7\end{aligned}|+0|\begin{aligned}0 & 3 \\ 0 & 0\end{aligned}| \\  & =(-5)(21-0)+0+0 \\  & =(-5)\cdot 21 \\  & =-105\end{aligned}
$$

## Generated easy
Template: `legacy_radio`; bank: `legacy_zero_diagonal`; origin: observed.

Find the value of $\begin{vmatrix}0 & 7 & -1 \\ 6 & 0 & 8 \\ -1 & -7 & 0\end{vmatrix}$.

- $-376$
- $342$
- $-14$ (correct)
- $-56$
- $0$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 7 & -1 \\ 6 & 0 & 8 \\ -1 & -7 & 0\end{aligned}| & =0|\begin{aligned}0 & 8 \\ -7 & 0\end{aligned}|-7|\begin{aligned}6 & 8 \\ -1 & 0\end{aligned}|+(-1)|\begin{aligned}6 & 0 \\ -1 & -7\end{aligned}| \\  & =0+(-7)(0-(-8))+(-1)(-42-0) \\  & =(-7)\cdot 8+(-1)\cdot (-42) \\  & =-56+42 \\  & =-14\end{aligned}
$$

## Generated easy
Template: `legacy_radio`; bank: `legacy_zero_diagonal`; origin: observed.

Find the value of $\begin{vmatrix}0 & -5 & 3 \\ 7 & 0 & 6 \\ 6 & -6 & 0\end{vmatrix}$.

- $-36$
- $0$
- $18$
- $-306$ (correct)
- $168$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & -5 & 3 \\ 7 & 0 & 6 \\ 6 & -6 & 0\end{aligned}| & =0|\begin{aligned}0 & 6 \\ -6 & 0\end{aligned}|-(-5)|\begin{aligned}7 & 6 \\ 6 & 0\end{aligned}|+3|\begin{aligned}7 & 0 \\ 6 & -6\end{aligned}| \\  & =0+5(0-36)+3(-42-0) \\  & =5\cdot (-36)+3\cdot (-42) \\  & =-180-126 \\  & =-306\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero`; origin: observed.

Find the value of $|\begin{aligned}3 & 8 & 8 \\ -4 & 2 & 0 \\ -5 & -3 & -5\end{aligned}|.$

- $5$
- $-10$
- $-14$ (correct)
- $-6$
- $6$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}3 & 8 & 8 \\ -4 & 2 & 0 \\ -5 & -3 & -5\end{aligned}| & =3|\begin{aligned}2 & 0 \\ -3 & -5\end{aligned}|-8|\begin{aligned}-4 & 0 \\ -5 & -5\end{aligned}|+8|\begin{aligned}-4 & 2 \\ -5 & -3\end{aligned}| \\  & =3(-10-0)+(-8)(20-0)+8(12-(-10)) \\  & =3\cdot (-10)+(-8)\cdot 20+8\cdot 22 \\  & =-30-160+176 \\  & =-14\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero`; origin: observed.

Find the value of $|\begin{aligned}-5 & 3 & 7 \\ 6 & 6 & 0 \\ -6 & -3 & -6\end{aligned}|.$

- $6$
- $18$
- $30$
- $414$ (correct)
- $-36$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-5 & 3 & 7 \\ 6 & 6 & 0 \\ -6 & -3 & -6\end{aligned}| & =(-5)|\begin{aligned}6 & 0 \\ -3 & -6\end{aligned}|-3|\begin{aligned}6 & 0 \\ -6 & -6\end{aligned}|+7|\begin{aligned}6 & 6 \\ -6 & -3\end{aligned}| \\  & =(-5)(-36-0)+(-3)(-36-0)+7(-18-(-36)) \\  & =(-5)\cdot (-36)+(-3)\cdot (-36)+7\cdot 18 \\  & =180+108+126 \\  & =414\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `upper_triangular`; origin: observed.

Find the value of $|\begin{aligned}-3 & 2 & 1 \\ 0 & -1 & 8 \\ 0 & 0 & 6\end{aligned}|.$

- $-162$
- $114$
- $18$ (correct)
- $65$
- $189$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-3 & 2 & 1 \\ 0 & -1 & 8 \\ 0 & 0 & 6\end{aligned}| & =(-3)|\begin{aligned}-1 & 8 \\ 0 & 6\end{aligned}|-2|\begin{aligned}0 & 8 \\ 0 & 6\end{aligned}|+1|\begin{aligned}0 & -1 \\ 0 & 0\end{aligned}| \\  & =(-3)(-6-0)+(-2)(0-0)+1(0-0) \\  & =(-3)\cdot (-6) \\  & =18\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `upper_triangular`; origin: observed.

Find the value of $|\begin{aligned}-3 & -6 & 1 \\ 0 & 6 & 1 \\ 0 & 0 & 1\end{aligned}|.$

- $15$
- $-105$
- $37$
- $-18$ (correct)
- $-24$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-3 & -6 & 1 \\ 0 & 6 & 1 \\ 0 & 0 & 1\end{aligned}| & =(-3)|\begin{aligned}6 & 1 \\ 0 & 1\end{aligned}|-(-6)|\begin{aligned}0 & 1 \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 6 \\ 0 & 0\end{aligned}| \\  & =(-3)(6-0)+6(0-0)+1(0-0) \\  & =(-3)\cdot 6 \\  & =-18\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `lower_triangular`; origin: observed.

Find the value of $|\begin{aligned}7 & 0 & 0 \\ -1 & 6 & 0 \\ 8 & -1 & -7\end{aligned}|.$

- $-245$
- $-588$
- $-294$ (correct)
- $49$
- $-392$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 0 & 0 \\ -1 & 6 & 0 \\ 8 & -1 & -7\end{aligned}| & =7|\begin{aligned}6 & 0 \\ -1 & -7\end{aligned}|-0|\begin{aligned}-1 & 0 \\ 8 & -7\end{aligned}|+0|\begin{aligned}-1 & 6 \\ 8 & -1\end{aligned}| \\  & =7(-42-0)+0+0 \\  & =7\cdot (-42) \\  & =-294\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `lower_triangular`; origin: observed.

Find the value of $|\begin{aligned}4 & 0 & 0 \\ -1 & 6 & 0 \\ -4 & -6 & 1\end{aligned}|.$

- $20$
- $-16$
- $-24$
- $24$ (correct)
- $48$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}4 & 0 & 0 \\ -1 & 6 & 0 \\ -4 & -6 & 1\end{aligned}| & =4|\begin{aligned}6 & 0 \\ -6 & 1\end{aligned}|-0|\begin{aligned}-1 & 0 \\ -4 & 1\end{aligned}|+0|\begin{aligned}-1 & 6 \\ -4 & -6\end{aligned}| \\  & =4(6-0)+0+0 \\  & =4\cdot 6 \\  & =24\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `sparse_two_terms`; origin: observed.

Find the value of $|\begin{aligned}7 & 0 & -1 \\ 0 & 6 & 8 \\ -1 & 0 & -7\end{aligned}|.$

- $6$
- $386$
- $-300$ (correct)
- $-294$
- $294$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 0 & -1 \\ 0 & 6 & 8 \\ -1 & 0 & -7\end{aligned}| & =7|\begin{aligned}6 & 8 \\ 0 & -7\end{aligned}|-0|\begin{aligned}0 & 8 \\ -1 & -7\end{aligned}|+(-1)|\begin{aligned}0 & 6 \\ -1 & 0\end{aligned}| \\  & =7(-42-0)+0+(-1)(0-(-6)) \\  & =7\cdot (-42)+(-1)\cdot 6 \\  & =-294-6 \\  & =-300\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `sparse_two_terms`; origin: observed.

Find the value of $|\begin{aligned}-5 & 0 & 3 \\ 0 & 7 & 6 \\ 6 & 0 & -6\end{aligned}|.$

- $126$
- $-210$
- $210$
- $84$ (correct)
- $-306$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-5 & 0 & 3 \\ 0 & 7 & 6 \\ 6 & 0 & -6\end{aligned}| & =(-5)|\begin{aligned}7 & 6 \\ 0 & -6\end{aligned}|-0|\begin{aligned}0 & 6 \\ 6 & -6\end{aligned}|+3|\begin{aligned}0 & 7 \\ 6 & 0\end{aligned}| \\  & =(-5)(-42-0)+0+3(0-42) \\  & =(-5)\cdot (-42)+3\cdot (-42) \\  & =210-126 \\  & =84\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `sparse_second_column`; origin: observed.

Find the value of $|\begin{aligned}7 & 0 & -1 \\ 0 & 6 & 0 \\ 8 & 0 & -1\end{aligned}|.$

- $48$
- $-42$
- $6$ (correct)
- $-90$
- $384$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 0 & -1 \\ 0 & 6 & 0 \\ 8 & 0 & -1\end{aligned}| & =7|\begin{aligned}6 & 0 \\ 0 & -1\end{aligned}|-0|\begin{aligned}0 & 0 \\ 8 & -1\end{aligned}|+(-1)|\begin{aligned}0 & 6 \\ 8 & 0\end{aligned}| \\  & =7(-6-0)+0+(-1)(0-48) \\  & =7\cdot (-6)+(-1)\cdot (-48) \\  & =-42+48 \\  & =6\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `sparse_second_column`; origin: observed.

Find the value of $|\begin{aligned}-6 & 0 & -3 \\ 0 & -6 & 0 \\ 1 & 0 & 6\end{aligned}|.$

- $-18$
- $18$
- $234$
- $198$ (correct)
- $216$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-6 & 0 & -3 \\ 0 & -6 & 0 \\ 1 & 0 & 6\end{aligned}| & =(-6)|\begin{aligned}-6 & 0 \\ 0 & 6\end{aligned}|-0|\begin{aligned}0 & 0 \\ 1 & 6\end{aligned}|+(-3)|\begin{aligned}0 & -6 \\ 1 & 0\end{aligned}| \\  & =(-6)(-36-0)+0+(-3)(0-(-6)) \\  & =(-6)\cdot (-36)+(-3)\cdot 6 \\  & =216-18 \\  & =198\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `zero_diagonal`; origin: observed.

Find the value of $|\begin{aligned}0 & 7 & -1 \\ 6 & 0 & 8 \\ -1 & -7 & 0\end{aligned}|.$

- $56$
- $0$
- $-14$ (correct)
- $42$
- $14$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 7 & -1 \\ 6 & 0 & 8 \\ -1 & -7 & 0\end{aligned}| & =0|\begin{aligned}0 & 8 \\ -7 & 0\end{aligned}|-7|\begin{aligned}6 & 8 \\ -1 & 0\end{aligned}|+(-1)|\begin{aligned}6 & 0 \\ -1 & -7\end{aligned}| \\  & =0+(-7)(0-(-8))+(-1)(-42-0) \\  & =(-7)\cdot 8+(-1)\cdot (-42) \\  & =-56+42 \\  & =-14\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `zero_diagonal`; origin: observed.

Find the value of $|\begin{aligned}0 & -5 & 3 \\ 7 & 0 & 6 \\ 6 & -6 & 0\end{aligned}|.$

- $180$
- $306$
- $-126$
- $-306$ (correct)
- $0$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & -5 & 3 \\ 7 & 0 & 6 \\ 6 & -6 & 0\end{aligned}| & =0|\begin{aligned}0 & 6 \\ -6 & 0\end{aligned}|-(-5)|\begin{aligned}7 & 6 \\ 6 & 0\end{aligned}|+3|\begin{aligned}7 & 0 \\ 6 & -6\end{aligned}| \\  & =0+5(0-36)+3(-42-0) \\  & =5\cdot (-36)+3\cdot (-42) \\  & =-180-126 \\  & =-306\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero_b`; origin: observed.

Find the value of $|\begin{aligned}7 & -1 & 6 \\ 0 & 8 & -1 \\ -7 & -3 & 2\end{aligned}|.$

- $462$
- $-49$
- $420$ (correct)
- $-462$
- $283$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & -1 & 6 \\ 0 & 8 & -1 \\ -7 & -3 & 2\end{aligned}| & =7|\begin{aligned}8 & -1 \\ -3 & 2\end{aligned}|-(-1)|\begin{aligned}0 & -1 \\ -7 & 2\end{aligned}|+6|\begin{aligned}0 & 8 \\ -7 & -3\end{aligned}| \\  & =7(16-3)+1(0-7)+6(0-(-56)) \\  & =7\cdot 13+1\cdot (-7)+6\cdot 56 \\  & =91-7+336 \\  & =420\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `signed_one_zero_b`; origin: observed.

Find the value of $|\begin{aligned}1 & 6 & 1 \\ 0 & 1 & 4 \\ -1 & 6 & -4\end{aligned}|.$

- $13$
- $-21$
- $3$
- $-51$ (correct)
- $30$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}1 & 6 & 1 \\ 0 & 1 & 4 \\ -1 & 6 & -4\end{aligned}| & =1|\begin{aligned}1 & 4 \\ 6 & -4\end{aligned}|-6|\begin{aligned}0 & 4 \\ -1 & -4\end{aligned}|+1|\begin{aligned}0 & 1 \\ -1 & 6\end{aligned}| \\  & =1(-4-24)+(-6)(0-(-4))+1(0-(-1)) \\  & =1\cdot (-28)+(-6)\cdot 4+1\cdot 1 \\  & =-28-24+1 \\  & =-51\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}|.$

- $-39$
- $75$
- $-37$ (correct)
- $37$
- $-25$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}| & =6|\begin{aligned}-3 & 0 \\ 1 & -1\end{aligned}|-8|\begin{aligned}-7 & 0 \\ 2 & -1\end{aligned}|+(-1)|\begin{aligned}-7 & -3 \\ 2 & 1\end{aligned}| \\  & =6(3-0)+(-8)(7-0)+(-1)(-7-(-6)) \\  & =6\cdot 3+(-8)\cdot 7+(-1)\cdot (-1) \\  & =18-56+1 \\  & =-37\end{aligned}
$$

## Generated easy
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}3 & 6 & 6 \\ -7 & 5 & 0 \\ 1 & -3 & 5\end{aligned}|.$

- $189$
- $441$
- $-381$
- $381$ (correct)
- $-39$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}3 & 6 & 6 \\ -7 & 5 & 0 \\ 1 & -3 & 5\end{aligned}| & =3|\begin{aligned}5 & 0 \\ -3 & 5\end{aligned}|-6|\begin{aligned}-7 & 0 \\ 1 & 5\end{aligned}|+6|\begin{aligned}-7 & 5 \\ 1 & -3\end{aligned}| \\  & =3(25-0)+(-6)(-35-0)+6(21-5) \\  & =3\cdot 25+(-6)\cdot (-35)+6\cdot 16 \\  & =75+210+96 \\  & =381\end{aligned}
$$

## Generated easy
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}],$ then $det(Q)=${{field-1}}.

- $-37$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}| & =6|\begin{aligned}-3 & 0 \\ 1 & -1\end{aligned}|-8|\begin{aligned}-7 & 0 \\ 2 & -1\end{aligned}|+(-1)|\begin{aligned}-7 & -3 \\ 2 & 1\end{aligned}| \\  & =6(3-0)+(-8)(7-0)+(-1)(-7-(-6)) \\  & =6\cdot 3+(-8)\cdot 7+(-1)\cdot (-1) \\  & =18-56+1 \\  & =-37\end{aligned}
$$

## Generated easy
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}0 & 3 & 7 \\ 6 & 0 & 6 \\ -6 & -3 & 0\end{aligned}],$ then $det(A)=${{field-1}}.

- $-234$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 3 & 7 \\ 6 & 0 & 6 \\ -6 & -3 & 0\end{aligned}| & =0|\begin{aligned}0 & 6 \\ -3 & 0\end{aligned}|-3|\begin{aligned}6 & 6 \\ -6 & 0\end{aligned}|+7|\begin{aligned}6 & 0 \\ -6 & -3\end{aligned}| \\  & =0+(-3)(0-(-36))+7(-18-0) \\  & =(-3)\cdot 36+7\cdot (-18) \\  & =-108-126 \\  & =-234\end{aligned}
$$

## Generated easy
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}],$ then $det(Q)=${{field-1}}.

- $-37$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}6 & 8 & -1 \\ -7 & -3 & 0 \\ 2 & 1 & -1\end{aligned}| & =6|\begin{aligned}-3 & 0 \\ 1 & -1\end{aligned}|-8|\begin{aligned}-7 & 0 \\ 2 & -1\end{aligned}|+(-1)|\begin{aligned}-7 & -3 \\ 2 & 1\end{aligned}| \\  & =6((-3)\cdot (-1)-0\cdot 1)+(-8)((-7)\cdot (-1)-0\cdot 2)+(-1)((-7)\cdot 1-(-3)\cdot 2) \\  & =6(3-0)+(-8)(7-0)+(-1)(-7-(-6)) \\  & =6\cdot 3+(-8)\cdot 7+(-1)\cdot (-1) \\  & =18-56+1 \\  & =-37\end{aligned}
$$

## Generated easy
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}0 & 3 & 7 \\ 6 & 0 & 6 \\ -6 & -3 & 0\end{aligned}],$ then $det(A)=${{field-1}}.

- $-234$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}0 & 3 & 7 \\ 6 & 0 & 6 \\ -6 & -3 & 0\end{aligned}| & =0|\begin{aligned}0 & 6 \\ -3 & 0\end{aligned}|-3|\begin{aligned}6 & 6 \\ -6 & 0\end{aligned}|+7|\begin{aligned}6 & 0 \\ -6 & -3\end{aligned}| \\  & =0+(-3)(6\cdot 0-6\cdot (-6))+7(6\cdot (-3)-0\cdot (-6)) \\  & =0+(-3)(0-(-36))+7(-18-0) \\  & =(-3)\cdot 36+7\cdot (-18) \\  & =-108-126 \\  & =-234\end{aligned}
$$

## Generated moderate
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}],$ then $det(Q)=${{field-1}}.

- $364$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}| & =8|\begin{aligned}-8 & -4 \\ 2 & -2\end{aligned}|-(-2)|\begin{aligned}-2 & -4 \\ 3 & -2\end{aligned}|+7|\begin{aligned}-2 & -8 \\ 3 & 2\end{aligned}| \\  & =8(16-(-8))+2(4-(-12))+7(-4-(-24)) \\  & =8\cdot 24+2\cdot 16+7\cdot 20 \\  & =192+32+140 \\  & =364\end{aligned}
$$

## Generated moderate
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $R=[\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}],$ then $det(R)=${{field-1}}.

- $98$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}| & =(-6)|\begin{aligned}7 & -7 \\ -7 & 2\end{aligned}|-4|\begin{aligned}7 & -7 \\ -4 & 2\end{aligned}|+8|\begin{aligned}7 & 7 \\ -4 & -7\end{aligned}| \\  & =(-6)(14-49)+(-4)(14-28)+8(-49-(-28)) \\  & =(-6)\cdot (-35)+(-4)\cdot (-14)+8\cdot (-21) \\  & =210+56-168 \\  & =98\end{aligned}
$$

## Generated moderate
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}],$ then $det(Q)=${{field-1}}.

- $364$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}| & =8|\begin{aligned}-8 & -4 \\ 2 & -2\end{aligned}|-(-2)|\begin{aligned}-2 & -4 \\ 3 & -2\end{aligned}|+7|\begin{aligned}-2 & -8 \\ 3 & 2\end{aligned}| \\  & =8((-8)\cdot (-2)-(-4)\cdot 2)+2((-2)\cdot (-2)-(-4)\cdot 3)+7((-2)\cdot 2-(-8)\cdot 3) \\  & =8(16-(-8))+2(4-(-12))+7(-4-(-24)) \\  & =8\cdot 24+2\cdot 16+7\cdot 20 \\  & =192+32+140 \\  & =364\end{aligned}
$$

## Generated moderate
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $R=[\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}],$ then $det(R)=${{field-1}}.

- $98$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}| & =(-6)|\begin{aligned}7 & -7 \\ -7 & 2\end{aligned}|-4|\begin{aligned}7 & -7 \\ -4 & 2\end{aligned}|+8|\begin{aligned}7 & 7 \\ -4 & -7\end{aligned}| \\  & =(-6)(7\cdot 2-(-7)\cdot (-7))+(-4)(7\cdot 2-(-7)\cdot (-4))+8(7\cdot (-7)-7\cdot (-4)) \\  & =(-6)(14-49)+(-4)(14-28)+8(-49-(-28)) \\  & =(-6)\cdot (-35)+(-4)\cdot (-14)+8\cdot (-21) \\  & =210+56-168 \\  & =98\end{aligned}
$$

## Generated hard
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}],$ then $det(Q)=${{field-1}}.

- $2393$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}| & =7|\begin{aligned}11 & 10 \\ 4 & 10\end{aligned}|-8|\begin{aligned}-4 & 10 \\ 7 & 10\end{aligned}|+(-11)|\begin{aligned}-4 & 11 \\ 7 & 4\end{aligned}| \\  & =7(110-40)+(-8)(-40-70)+(-11)(-16-77) \\  & =7\cdot 70+(-8)\cdot (-110)+(-11)\cdot (-93) \\  & =490+880+1023 \\  & =2393\end{aligned}
$$

## Generated hard
Template: `matrix_blank`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}],$ then $det(A)=${{field-1}}.

- $1276$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}| & =(-8)|\begin{aligned}10 & 9 \\ 7 & -6\end{aligned}|-(-10)|\begin{aligned}-9 & 9 \\ 10 & -6\end{aligned}|+(-4)|\begin{aligned}-9 & 10 \\ 10 & 7\end{aligned}| \\  & =(-8)(-60-63)+10(54-90)+(-4)(-63-100) \\  & =(-8)\cdot (-123)+10\cdot (-36)+(-4)\cdot (-163) \\  & =984-360+652 \\  & =1276\end{aligned}
$$

## Generated hard
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $Q=[\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}],$ then $det(Q)=${{field-1}}.

- $2393$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}| & =7|\begin{aligned}11 & 10 \\ 4 & 10\end{aligned}|-8|\begin{aligned}-4 & 10 \\ 7 & 10\end{aligned}|+(-11)|\begin{aligned}-4 & 11 \\ 7 & 4\end{aligned}| \\  & =7(11\cdot 10-10\cdot 4)+(-8)((-4)\cdot 10-10\cdot 7)+(-11)((-4)\cdot 4-11\cdot 7) \\  & =7(110-40)+(-8)(-40-70)+(-11)(-16-77) \\  & =7\cdot 70+(-8)\cdot (-110)+(-11)\cdot (-93) \\  & =490+880+1023 \\  & =2393\end{aligned}
$$

## Generated hard
Template: `matrix_blank_products`; bank: `None`; origin: not applicable.

If $A=[\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}],$ then $det(A)=${{field-1}}.

- $1276$ (correct)

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}| & =(-8)|\begin{aligned}10 & 9 \\ 7 & -6\end{aligned}|-(-10)|\begin{aligned}-9 & 9 \\ 10 & -6\end{aligned}|+(-4)|\begin{aligned}-9 & 10 \\ 10 & 7\end{aligned}| \\  & =(-8)(10\cdot (-6)-9\cdot 7)+10((-9)\cdot (-6)-9\cdot 10)+(-4)((-9)\cdot 7-10\cdot 10) \\  & =(-8)(-60-63)+10(54-90)+(-4)(-63-100) \\  & =(-8)\cdot (-123)+10\cdot (-36)+(-4)\cdot (-163) \\  & =984-360+652 \\  & =1276\end{aligned}
$$

## Generated moderate
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}|.$

- $84$
- $300$
- $364$ (correct)
- $-364$
- $-148$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}8 & -2 & 7 \\ -2 & -8 & -4 \\ 3 & 2 & -2\end{aligned}| & =8|\begin{aligned}-8 & -4 \\ 2 & -2\end{aligned}|-(-2)|\begin{aligned}-2 & -4 \\ 3 & -2\end{aligned}|+7|\begin{aligned}-2 & -8 \\ 3 & 2\end{aligned}| \\  & =8(16-(-8))+2(4-(-12))+7(-4-(-24)) \\  & =8\cdot 24+2\cdot 16+7\cdot 20 \\  & =192+32+140 \\  & =364\end{aligned}
$$

## Generated moderate
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}|.$

- $434$
- $-1162$
- $-98$
- $98$ (correct)
- $-14$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-6 & 4 & 8 \\ 7 & 7 & -7 \\ -4 & -7 & 2\end{aligned}| & =(-6)|\begin{aligned}7 & -7 \\ -7 & 2\end{aligned}|-4|\begin{aligned}7 & -7 \\ -4 & 2\end{aligned}|+8|\begin{aligned}7 & 7 \\ -4 & -7\end{aligned}| \\  & =(-6)(14-49)+(-4)(14-28)+8(-49-(-28)) \\  & =(-6)\cdot (-35)+(-4)\cdot (-14)+8\cdot (-21) \\  & =210+56-168 \\  & =98\end{aligned}
$$

## Generated hard
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}|.$

- $347$
- $633$
- $2393$ (correct)
- $-2393$
- $139$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}7 & 8 & -11 \\ -4 & 11 & 10 \\ 7 & 4 & 10\end{aligned}| & =7|\begin{aligned}11 & 10 \\ 4 & 10\end{aligned}|-8|\begin{aligned}-4 & 10 \\ 7 & 10\end{aligned}|+(-11)|\begin{aligned}-4 & 11 \\ 7 & 4\end{aligned}| \\  & =7(110-40)+(-8)(-40-70)+(-11)(-16-77) \\  & =7\cdot 70+(-8)\cdot (-110)+(-11)\cdot (-93) \\  & =490+880+1023 \\  & =2393\end{aligned}
$$

## Generated hard
Template: `aligned_radio`; bank: `cofactor_signs`; origin: authored.

Find the value of $|\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}|.$

- $-28$
- $1268$
- $-1276$
- $1276$ (correct)
- $1996$

Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:

$$
\begin{aligned}|\begin{aligned}-8 & -10 & -4 \\ -9 & 10 & 9 \\ 10 & 7 & -6\end{aligned}| & =(-8)|\begin{aligned}10 & 9 \\ 7 & -6\end{aligned}|-(-10)|\begin{aligned}-9 & 9 \\ 10 & -6\end{aligned}|+(-4)|\begin{aligned}-9 & 10 \\ 10 & 7\end{aligned}| \\  & =(-8)(-60-63)+10(54-90)+(-4)(-63-100) \\  & =(-8)\cdot (-123)+10\cdot (-36)+(-4)\cdot (-163) \\  & =984-360+652 \\  & =1276\end{aligned}
$$
