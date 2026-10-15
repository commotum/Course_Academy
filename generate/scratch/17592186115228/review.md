## q-42265

Source and exact replay:

Given that $A,B,$ and $C$ are $4\times 4$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $(AB)C=A(BC)$
- **III.** $AC+BC=(A+B)C$

Let's consider the statements one by one.

- Statement I is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement II is true. Matrix multiplication is associative, so $(AB)C=A(BC)$ in general.

- Statement III is true. Matrix multiplication is distributive, so $(A+B)C=AC+BC,$ and $A(B+C)=AB+AC$ in general.

Therefore, only statements II and III are true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $(AB)C=A(BC)$
- **III.** $AC+BC=(A+B)C$

## q-42266

Source and exact replay:

Given that $A,B,$ and $C$ are $6\times 6$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $(A+B)C=AC+BC$
- **II.** $AB=BA$
- **III.** $A(BC)=(BA)C$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is distributive, so $(A+B)C=AC+BC,$ and $A(B+C)=AB+AC$ in general.

- Statement II is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement III is false. Matrix multiplication is associative, so $(AB)C=A(BC)$ in general. However, since matrix multiplication is not commutative, we have

$$
\begin{aligned}A(BC)=(AB)C\ne (BA)C.\end{aligned}
$$

Therefore, only statement I is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $(A+B)C=AC+BC$
- **II.** $AB=BA$
- **III.** $A(BC)=(BA)C$

## q-130446

Source and exact replay:

Given that $A,B,$ and $C$ are $4\times 4$ matrices which of the following statements are always true?

Select all that apply.

- **I.** ${A}^{2}B=A(AB)$
- **II.** $A(B-C)=AB-CA$
- **III.** $B(CA)=(CB)A$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is associative and  ${A}^{2}B=AAB=A(AB)$ is always true.

- Statement II is false.  Matrix multiplication is distributive and  $A(B-C)=AB-AC.$ However, matrix multiplication is not commutative, so $AC\ne CA$ in general and therefore $A(B-C)\ne AB-CA$, in general.

- Statement III is false. Matrix multiplication is associative and  $B(CA)=(BC)A.$ However, matrix multiplication is not commutative, so $BC\ne CB$ in general and therefore $B(CA)\ne (CB)A$, in general.

Therefore, only statement  I is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices which of the following statements are always true?

Select all that apply.

- **I.** ${A}^{2}B=A(AB)$
- **II.** $A(B-C)=AB-CA$
- **III.** $B(CA)=(CB)A$

## q-130449

Source and exact replay:

Given that $A,B,$ and $C$ are $3\times 3$ matrices, and  ${I}_{3}$ is the $3\times 3$ identity matrix, which of the following statements are always true?

Select all that apply.

- **I.** $AB=A{I}_{3}B$
- **II.** $A(B+{I}_{3})=AB$
- **III.** ${I}_{3}A=A{I}_{3}$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is associative, so $A{I}_{3}B=(A{I}_{3})B=AB.$

- Statement II is false. Matrix multiplication is distributive, so $A(B+{I}_{3})=AB+A{I}_{3}=AB+A.$ However,  $AB+A\ne AB,$ in general.

- Statement III is true. Matrix multiplication is not commutative in general, however, multiplication by the identity matrix is always commutative. In this case, we have  ${I}_{3}A=A{I}_{3}.$

Therefore, only statements I and III are true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, and  ${I}_{2}$ is the $2\times 2$ identity matrix, which of the following statements are always true?

Select all that apply.

- **I.** $AB=A{I}_{2}B$
- **II.** $A(B+{I}_{2})=AB$
- **III.** ${I}_{2}A=A{I}_{2}$

## q-130455

Source and exact replay:

Given that $A,B,$ and $C$ are $6\times 6$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $A(BC)=(AB)C$

- **II.** $A(B-C)=AB-CA$

- **III.** $CA=AC$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is associative and  $A(BC)=(AB)C$ is always true.

- Statement II is false. Matrix multiplication is distributive, so $A(B-C)=AB-AC,$ but $AC\ne CA$ because matrix multiplication is not commutative in general.

- Statement III  is false. Matrix multiplication is not commutative, so $CA\ne AC$ in general.

Therefore, only statement  I is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $A(BC)=(AB)C$

- **II.** $A(B-C)=AB-CA$

- **III.** $CA=AC$

## q-130463

Source and exact replay:

Given that $A$ and $B$  are $8\times 8$ matrices,  and ${I}_{8}$ is the $8\times 8$ identity matrix,  which of the following statements are always true?

Select all that apply.

- **I.** $A{I}_{8}={I}_{8}A$
- **II.** $AB=BA$
- **III.** $A\cdot 2{I}_{8}=2A$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is not commutative in general, however, multiplication by the identity matrix is always commutative. In this case, we have  $A{I}_{8}={I}_{8}A=A.$

- Statement II is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement III is true. Matrix multiplication is distributive, so 

$$
\begin{aligned}A\cdot 2{I}_{8} & =A({I}_{8}+{I}_{8}) \\  & =A{I}_{8}+A{I}_{8} \\  & =A+A \\  & =2A.\end{aligned}
$$

Therefore, only statements I  and III are true.

Dimension preview (same task, rejected as fresh):

Given that $A$ and $B$  are $2\times 2$ matrices,  and ${I}_{2}$ is the $2\times 2$ identity matrix,  which of the following statements are always true?

Select all that apply.

- **I.** $A{I}_{2}={I}_{2}A$
- **II.** $AB=BA$
- **III.** $A\cdot 2{I}_{2}=2A$

## q-130478

Source and exact replay:

Given that $A,B,$ and $C$ are $7\times 7$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $(CA)B=C(BA)$
- **II.** $(A+A)B=2AB$
- **III.** $CB=BC$

Let's consider the statements one by one.

- Statement I  is false. Matrix multiplication is associative and  $(CA)B=C(AB)$ is always true. However,  matrix multiplication is not commutative,   $AB\ne BA$ in general. Therefore, $(CA)B\ne C(BA)$ in general.

- Statement II is true. Matrix multiplication is distributive, so $(A+A)B=AB+AB=2AB$ is always true.

- Statement III is false. Matrix multiplication is not commutative in general, so $CB\ne BC$ in general.

Therefore, only statement II is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $(CA)B=C(BA)$
- **II.** $(A+A)B=2AB$
- **III.** $CB=BC$

## q-42264

Source and exact replay:

Given that $A,B,$ and $C$ are $2\times 2$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$

- **II.** $(AB)C=A(BC)$

- **III.** $A(B-C)=(B-C)A$

Let's consider the statements one by one.

- Statement I is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement II is true. Matrix multiplication is associative, so $(AB)C=A(BC)$ in general.

- Statement III is false. Matrix multiplication is not commutative, so $A(B-C)\ne (B-C)A$ in general.

Therefore, only statement II is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $8\times 8$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$

- **II.** $(AB)C=A(BC)$

- **III.** $A(B-C)=(B-C)A$

## q-42267

Source and exact replay:

Given that $A,B,$ and $C$ are $5\times 5$ matrices, and  ${I}_{5}$ is the $5\times 5$ identity matrix, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $A(B+C)=AB+AC$
- **III.** $B{I}_{5}={I}_{5}B$

Let's consider the statements one by one.

- Statement I is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement II is true. Matrix multiplication is distributive, so $(A+B)C=AC+BC,$ and $A(B+C)=AB+AC$ in general.

- Statement III is true. Matrix multiplication is not commutative in general, however, multiplication by the identity matrix is always commutative. In this case, we have  $B{I}_{5}={I}_{5}B=B.$

Therefore, only statements II and III are true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, and  ${I}_{2}$ is the $2\times 2$ identity matrix, which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $A(B+C)=AB+AC$
- **III.** $B{I}_{2}={I}_{2}B$

## q-75662

Source and exact replay:

Given that $A,B,$ and $C$ are $7\times 7$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $A(B+C)=AC+AB$
- **II.** $A(BC)=(BA)C$
- **III.** $AB=BA$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is distributive, so 

$$
A(B+C)=AB+AC=AC+AB
$$

 since matrix addition is commutative.

- Statement II is false. Matrix multiplication is associative, so $(AB)C=A(BC)$ in general. However, since matrix multiplication is not commutative, we have

$$
\begin{aligned}A(BC)=(AB)C\ne (BA)C.\end{aligned}
$$

- Statement III is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

Therefore, only statement I is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, which of the following statements are always true?

Select all that apply.

- **I.** $A(B+C)=AC+AB$
- **II.** $A(BC)=(BA)C$
- **III.** $AB=BA$

## q-75664

Source and exact replay:

Given that $A$ and $B$  are $4\times 4$ matrices,  and ${I}_{4}$ is the $4\times 4$ identity matrix,  which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $A{I}_{4}={I}_{4}A$
- **III.** $A(B+{I}_{4})=AB+A$

Let's consider the statements one by one.

- Statement I is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement II is true. Matrix multiplication is not commutative in general, however, multiplication by the identity matrix is always commutative. In this case, we have  $A{I}_{4}={I}_{4}A=A.$

- Statement III is true. Matrix multiplication is distributive, so $A(B+{I}_{4})=AB+A{I}_{4}=AB+A$ in general.

Therefore, only statements II  and III are true.

Dimension preview (same task, rejected as fresh):

Given that $A$ and $B$  are $2\times 2$ matrices,  and ${I}_{2}$ is the $2\times 2$ identity matrix,  which of the following statements are always true?

Select all that apply.

- **I.** $AB=BA$
- **II.** $A{I}_{2}={I}_{2}A$
- **III.** $A(B+{I}_{2})=AB+A$

## q-75717

Source and exact replay:

Given that $A,B,$ and $C$ are $6\times 6$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $CB=BC$
- **II.** $A(B-C)=AB-CA$
- **III.** $A(BC)=(AB)C$

Let's consider the statements one by one.

- Statement I is false. Matrix multiplication is not commutative, so $AB\ne BA$ in general.

- Statement II is false. Matrix multiplication is distributive, so $A(B-C)=AB-AC,$ but $AC\ne CA$ because matrix multiplication is not commutative in general.

- Statement III is true. Matrix multiplication is associative and  $A(BC)=(AB)C$ is always true.

Therefore, only statement  III is true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices which of the following statements are always true?

Select all that apply.

- **I.** $CB=BC$
- **II.** $A(B-C)=AB-CA$
- **III.** $A(BC)=(AB)C$

## q-75663

Source and exact replay:

Given that $A,B,$ and $C$ are $4\times 4$ matrices, and ${I}_{4}$ is the $4\times 4$ identity matrix,  which of the following statements are always true?

I. $A{I}_{4}={I}_{4}A$

II. $(CA)B=C(AB)$

III. $BC=CB$

Let's consider the statements one by one.

- Statement I is true. Matrix multiplication is not commutative in general, however, multiplication by the identity matrix is always commutative. In this case, we have  $A{I}_{4}={I}_{4}A=A.$

- Statement II is true. Matrix multiplication is asociative, so $(CA)B=C(AB)$ in general.

- Statement III is false. Matrix multiplication is not commutative, so $BC\ne CB$ in general.

Therefore, only statements I  and II are true.

Dimension preview (same task, rejected as fresh):

Given that $A,B,$ and $C$ are $2\times 2$ matrices, and ${I}_{2}$ is the $2\times 2$ identity matrix,  which of the following statements are always true?

I. $A{I}_{2}={I}_{2}A$

II. $(CA)B=C(AB)$

III. $BC=CB$
