Which of the following statements are true, given that $A$ is a $5\times 5$ matrix and 

$$
\text{Null}(A)=\{\begin{bmatrix}3{x}_{1} \\ -4{x}_{1} \\ 0 \\ -4{x}_{1} \\ {x}_{1}\end{bmatrix}\,|\,{x}_{1}\in R\}?
$$

I. $\text{dim(Null}(A))=0$

II. $A$ is not invertible

III. $\text{rank}(A)=5$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true
Field II: false, true
Field III: false, true

Since $A$ is a $5\times 5$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $\,⇔\,\{\,\begin{aligned} & \text{Col}(A)={R}^{5} \\  & \text{dim(Col}(A))=5=\text{rank}(A) \\  & \text{Null}(A)=\{0\} \\  & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned}$

With that in mind, let's examine each statement in turn.

- Statement I is false. Since 

$$
\text{Null}(A)=\{{x}_{1}\begin{bmatrix}3 \\ -4 \\ 0 \\ -4 \\ 1\end{bmatrix}\,|\,{x}_{1}\in R\}
$$

we conclude that 

$$
\text{dim(Null}(A))=1\ne 0.
$$

- Statement II is true. Since $\text{dim(Null}(A))\ne 0,$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement III is false. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{rank}(A)\ne 5.$

Therefore, the correct answer is "II only."

---

Which of the following statements are true, given that $A$ is a $4\times 4$ matrix and $v=\begin{bmatrix}-3 \\ 1 \\ 1 \\ 0\end{bmatrix}$ is a solution of the equation $Ax=0?$

Select all that apply.

- **I.** $\text{Null}(A)={0}$
- **II.** $A$ is not invertible
- **III.** $\text{Col}(A)\ne {R}^{4}$

Field I: false, true
Field II: false, true
Field III: false, true

Since $A$ is a $4\times 4$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $\,⇔\,{\,\begin{aligned} & \text{Col}(A)={R}^{4} \\  & \text{dim(Col}(A))=4=\text{rank}(A) \\  & \text{Null}(A)={0} \\  & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned}$ 

With that in mind, let's examine each statement in turn. 

- Statement I is false. Since $v\ne 0$ and $Av=0,$ 
then $v\in \text{Null}(A)$ and, therefore, $\text{Null}(A)\ne {0}.$

- Statement II is true. Since $\text{Null}(A)\ne {0},$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement III is true. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{Col}(A)\ne {R}^{4}.$

Therefore, the correct answer is "II and III only."

---

Which of the following statements are true, given that $A$ is a $6\times 6$ matrix and  $det(A)=-4?$

Select all that apply.

- **I.** $A$ is invertible

- **II.** $\text{Null}(A)=\{0\}$

- **III.** $\text{nullity}(A)=6$

Field I: false, true
Field II: false, true
Field III: false, true

Since $A$ is a $6\times 6$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $\,⇔\,\{\,\begin{aligned} & \text{Col}(A)={R}^{6} \\  & \text{dim(Col}(A))=6=\text{rank}(A) \\  & \text{Null}(A)=\{0\} \\  & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned}$

With that in mind, let's examine each statement in turn. 

- Statement I is true. Indeed,   a matrix $A$ is invertible if and only if $det(A)\ne 0.$ Since here we have $det(A)=-4\ne 0,$ our matrix $A$ must be  invertible.

- Statement II is true. Indeed, by the invertible matrix theorem
$A$ is invertible $\,⇔\,\text{Null}(A)=\{0\}.$

- Statement III is false. Since $A$ is invertible,  it must be $\text{nullity}(A)=0.$

Therefore, the correct answer is "I and II only."

---

Which of the following statements are true, given that $A$ is a $5\times 5$ matrix and 

$$
\text{Null}(A)={\begin{bmatrix}3{x}_{1} \\ -{x}_{2} \\ 0 \\ -3{x}_{2} \\ 2{x}_{1}\end{bmatrix}\,|\,{x}_{1},{x}_{2}\in R}?
$$
- **I.** $\text{dim(Null}(A))=0$
- **II.** $A$ is  invertible
- **III.** $\text{Col}(A)\ne {R}^{5}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true
Field II: false, true
Field III: false, true

Since $A$ is a $5\times 5$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $\,⇔\,{\,\begin{aligned} & \text{Col}(A)={R}^{5} \\  & \text{dim(Col}(A))=5=\text{rank}(A) \\  & \text{Null}(A)={0} \\  & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned}$

With that in mind, let's examine each statement in turn.

- Statement I is false. Since 

$$
\text{Null}(A)={{x}_{1}\begin{bmatrix}3 \\ 0 \\ 0 \\ 0 \\ 2\end{bmatrix}+{x}_{2}\begin{bmatrix}0 \\ -1 \\ 0 \\ -3 \\ 0\end{bmatrix}\,|\,{x}_{1},{x}_{2}\in R}
$$

we conclude that 

$$
\text{dim(Null}(A))=2\ne 0.
$$

- Statement II is false. Since $\text{dim(Null}(A))\ne 0,$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement III is true. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{Col}(A)\ne {R}^{5}.$

Therefore, the correct answer is "III only."

---

Which of the following statements are true, given that $A$ is a $4\times 4$ matrix and 

$$
\text{Null}(A)=\{\begin{bmatrix}3{x}_{1} \\ {x}_{2} \\ 0 \\ 3{x}_{1}\end{bmatrix}\,|\,{x}_{1},{x}_{2}\in R\}?
$$

Select all that apply.

- **I.** $\text{dim(Null}(A))=1$

- **II.** $A$ is invertible

- **III.** $\text{rank}(A)<4$

Field I: false, true
Field II: false, true
Field III: false, true

Since $A$ is a $4\times 4$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $\,⇔\,\{\,\begin{aligned} & \text{Col}(A)={R}^{4} \\  & \text{dim(Col}(A))=4=\text{rank}(A) \\  & \text{Null}(A)=\{0\} \\  & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned}$

With that in mind, let's examine each statement in turn.

- Statement I is false. Indeed, since 

$$
\text{Null}(A)=\{{x}_{1}\begin{bmatrix}3 \\ 0 \\ 0 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}0 \\ 1 \\ 0 \\ 0\end{bmatrix}\,|\,{x}_{1},{x}_{2}\in R\}
$$

we conclude that 

$$
\text{dim(Null}(A))=2.
$$

- Statement II is false. Since $\text{dim(Null}(A))\ne 0,$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement III is true. Indeed, since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{rank}(A)\ne 4,$ or equivalently $\text{rank}(A)<4.$

Therefore, the correct answer is "III only."
