# Original source and generated variants

All original records are preserved separately in source-cases/canonical JSON. Below, original supplied-parameter completed presentations are identified explicitly; q-7908’s placement/key/explanation and the canonical prompt repair are authored, not observed source content. Every changed instance uses the normal parameterized generator, retaining complete source banks and source-specific stage masks. Moderate/hard are authored uncalibrated placements.

## q-11640 original parameters, completed presentation

Consider the matrices

$$
B=\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix},\,C=\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix},\,D=\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & 4 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}-1 & 2 \\ 1 & -1\end{bmatrix}\begin{bmatrix}1 & 2 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-11640 changed easy

Consider the matrices

$$
B=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,C=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-11640 changed moderate

Consider the matrices

$$
B=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,C=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,D=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-11640 changed hard

Consider the matrices

$$
B=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,C=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix},\,D=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-7908 original parameters, completed presentation

Consider the matrices
$A = \begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}, B = \begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}, C = \begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}$.

Which of the following statements are true?

1. $AB = BA = I_{2}$
2. $AC = CA = I_{2}$
3. $B = A^{-1}$

Field banks: selection: None, II only, I and III only, III only, I only

We must check whether each pair multiplies to $I_2$.

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix} \\ & =\begin{bmatrix}-1 & 1 \\ -2 & 0\end{bmatrix}\end{aligned}
$$

Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the correct answer is "II only".

## q-7908 changed easy

Consider the matrices
$A = \begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix}, B = \begin{bmatrix}2 & 0 \\ -1 & 1\end{bmatrix}, C = \begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}$.

Which of the following statements are true?

1. $AB = BA = I_{2}$
2. $AC = CA = I_{2}$
3. $B = A^{-1}$

Field banks: selection: I and III only, None, III only, II only, I only

We must check whether each pair multiplies to $I_2$.

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix}\begin{bmatrix}2 & 0 \\ -1 & 1\end{bmatrix} \\ & =\begin{bmatrix}2 & 0 \\ 0 & 2\end{bmatrix}\end{aligned}
$$

Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix}\begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the correct answer is "II only".

## q-7908 changed moderate

Consider the matrices
$A = \begin{bmatrix}-2 & -2 \\ -1 & -3\end{bmatrix}, B = \begin{bmatrix}-3 & 2 \\ 1 & -2\end{bmatrix}, C = \begin{bmatrix}-\frac{3}{4} & \frac{1}{2} \\ \frac{1}{4} & -\frac{1}{2}\end{bmatrix}$.

Which of the following statements are true?

1. $AB = BA = I_{2}$
2. $AC = CA = I_{2}$
3. $B = A^{-1}$

Field banks: selection: None, III only, II only, I only, I and III only

We must check whether each pair multiplies to $I_2$.

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-2 & -2 \\ -1 & -3\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 1 & -2\end{bmatrix} \\ & =\begin{bmatrix}4 & 0 \\ 0 & 4\end{bmatrix}\end{aligned}
$$

Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-2 & -2 \\ -1 & -3\end{bmatrix}\begin{bmatrix}-\frac{3}{4} & \frac{1}{2} \\ \frac{1}{4} & -\frac{1}{2}\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{3}{4} & \frac{1}{2} \\ \frac{1}{4} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-2 & -2 \\ -1 & -3\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the correct answer is "II only".

## q-7908 changed hard

Consider the matrices
$A = \begin{bmatrix}-\frac{1}{3} & -\frac{1}{3} \\ \frac{1}{2} & -\frac{1}{3}\end{bmatrix}, B = \begin{bmatrix}-\frac{1}{3} & \frac{1}{3} \\ -\frac{1}{2} & -\frac{1}{3}\end{bmatrix}, C = \begin{bmatrix}-\frac{6}{5} & \frac{6}{5} \\ -\frac{9}{5} & -\frac{6}{5}\end{bmatrix}$.

Which of the following statements are true?

1. $AB = BA = I_{2}$
2. $AC = CA = I_{2}$
3. $B = A^{-1}$

Field banks: selection: III only, None, II only, I and III only, I only

We must check whether each pair multiplies to $I_2$.

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{3} & -\frac{1}{3} \\ \frac{1}{2} & -\frac{1}{3}\end{bmatrix}\begin{bmatrix}-\frac{1}{3} & \frac{1}{3} \\ -\frac{1}{2} & -\frac{1}{3}\end{bmatrix} \\ & =\begin{bmatrix}\frac{5}{18} & 0 \\ 0 & \frac{5}{18}\end{bmatrix}\end{aligned}
$$

Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{3} & -\frac{1}{3} \\ \frac{1}{2} & -\frac{1}{3}\end{bmatrix}\begin{bmatrix}-\frac{6}{5} & \frac{6}{5} \\ -\frac{9}{5} & -\frac{6}{5}\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{6}{5} & \frac{6}{5} \\ -\frac{9}{5} & -\frac{6}{5}\end{bmatrix}\begin{bmatrix}-\frac{1}{3} & -\frac{1}{3} \\ \frac{1}{2} & -\frac{1}{3}\end{bmatrix} \\ & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the correct answer is "II only".

## q-102666 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix},\,B=\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix},\,C=\begin{bmatrix}2 & -1 \\ 1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{2}{3} & -\frac{1}{3} \\ \frac{1}{3} & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}2 & -1 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-102666 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix},\,C=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-102666 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix},\,C=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-102666 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-102669 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}3 & 1 \\ -1 & 0\end{bmatrix},\,B=\begin{bmatrix}0 & 1 \\ 1 & 3\end{bmatrix},\,C=\begin{bmatrix}0 & -1 \\ 1 & 3\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ 1 & 3\end{bmatrix} \\  & =\begin{bmatrix}∗ & 6 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}3 & 1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}0 & -1 \\ 1 & 3\end{bmatrix}\begin{bmatrix}3 & 1 \\ -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

## q-102669 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix},\,C=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

## q-102669 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,C=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

## q-102669 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

## q-102670 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}-3 & 2 \\ 2 & -2\end{bmatrix},\,B=\begin{bmatrix}-1 & -1 \\ -1 & -\frac{3}{2}\end{bmatrix},\,C=\begin{bmatrix}-1 & -1 \\ -1 & -3\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-3 & 2 \\ 2 & -2\end{bmatrix}\begin{bmatrix}-1 & -1 \\ -1 & -\frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}-1 & -1 \\ -1 & -\frac{3}{2}\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 2 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-3 & 2 \\ 2 & -2\end{bmatrix}\begin{bmatrix}-1 & -1 \\ -1 & -3\end{bmatrix} \\  & =\begin{bmatrix}∗ & -3 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

## q-102670 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix},\,C=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

## q-102670 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix},\,C=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

## q-102670 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

## q-102673 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}-2 & 2 \\ 1 & 0\end{bmatrix},\,B=\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix},\,C=\begin{bmatrix}0 & 1 \\ \frac{1}{2} & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-2 & 2 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}2 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-2 & 2 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ \frac{1}{2} & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}0 & 1 \\ \frac{1}{2} & 1\end{bmatrix}\begin{bmatrix}-2 & 2 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-102673 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix},\,C=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-102673 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,C=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-102673 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-102674 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}2 & 3 \\ 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-1 & 3 \\ 1 & -2\end{bmatrix},\,C=\begin{bmatrix}-1 & 2 \\ 1 & -3\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}2 & 3 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 3 \\ 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}-1 & 3 \\ 1 & -2\end{bmatrix}\begin{bmatrix}2 & 3 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}2 & 3 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 2 \\ 1 & -3\end{bmatrix} \\  & =\begin{bmatrix}∗ & -5 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-102674 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix},\,C=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-102674 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix},\,C=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-102674 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{2}$

II. $AC=CA={I}_{2}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-102675 original parameters, completed presentation

Consider the matrices

$$
A=\begin{bmatrix}-2 & 4 \\ 0 & -1\end{bmatrix},\,B=\begin{bmatrix}-1 & -2 \\ 0 & -1\end{bmatrix},\,C=\begin{bmatrix}-\frac{1}{2} & -2 \\ 0 & -1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-2 & 4 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-1 & -2 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}2 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-2 & 4 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -2 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{1}{2} & -2 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-2 & 4 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II and III only".

## q-102675 changed easy

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,B=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix},\,C=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II and III only".

## q-102675 changed moderate

Consider the matrices

$$
A=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,B=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,C=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II and III only".

## q-102675 changed hard

Consider the matrices

$$
A=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,B=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II and III only".

## q-11637 original parameters, completed presentation

Consider the matrices

$$
C=\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix},\,D=\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix},\,E=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix}\begin{bmatrix}2 & 1 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}0 & 1 \\ 1 & -2\end{bmatrix}\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ -2 & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-11637 changed easy

Consider the matrices

$$
C=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,D=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix},\,E=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-11637 changed moderate

Consider the matrices

$$
C=\begin{bmatrix}1 & -3 \\ 1 & 1\end{bmatrix},\,D=\begin{bmatrix}\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{4} & \frac{1}{4}\end{bmatrix},\,E=\begin{bmatrix}1 & 3 \\ -1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

Field banks: I: true, false; II: false, true; III: true, false

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & -3 \\ 1 & 1\end{bmatrix}\begin{bmatrix}\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{4} & \frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{4} & \frac{1}{4}\end{bmatrix}\begin{bmatrix}1 & -3 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{4} & \frac{1}{4}\end{bmatrix}\begin{bmatrix}1 & 3 \\ -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ -\frac{1}{2} & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-11637 changed hard

Consider the matrices

$$
C=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,D=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix},\,E=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}∗ & \frac{7}{2} \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

## q-71817 original parameters, completed presentation

Consider the matrices

$$
B=\begin{bmatrix}0 & -2 \\ 2 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix},\,D=\begin{bmatrix}0 & \frac{1}{2} \\ -\frac{1}{2} & 0\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}0 & -2 \\ 2 & 0\end{bmatrix}\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}0 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}0 & -2 \\ 2 & 0\end{bmatrix}\begin{bmatrix}0 & \frac{1}{2} \\ -\frac{1}{2} & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}0 & \frac{1}{2} \\ -\frac{1}{2} & 0\end{bmatrix}\begin{bmatrix}0 & -2 \\ 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-71817 changed easy

Consider the matrices

$$
B=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,C=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-71817 changed moderate

Consider the matrices

$$
B=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,C=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,D=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-71817 changed hard

Consider the matrices

$$
B=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,C=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix},\,D=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{2}$
- **II.** $BD=DB={I}_{2}$
- **III.** $D={B}^{-1}$

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $BC=CB={I}_{2}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $BD=DB={I}_{2}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

## q-71818 original parameters, completed presentation

Consider the matrices

$$
E=\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix},\,F=\begin{bmatrix}-\frac{1}{2} & -\frac{1}{2} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix},\,G=\begin{bmatrix}-1 & -1 \\ 1 & -1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -\frac{1}{2} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}-\frac{1}{2} & -\frac{1}{2} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}\begin{bmatrix}-1 & -1 \\ 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}2 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-71818 changed easy

Consider the matrices

$$
E=\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix},\,F=\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix},\,G=\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

Field banks: I: false, true; II: false, true; III: false, true

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}1 & -\frac{2}{3} \\ 0 & \frac{1}{3}\end{bmatrix}\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}1 & 2 \\ 0 & 3\end{bmatrix}\begin{bmatrix}3 & -2 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}3 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-71818 changed moderate

Consider the matrices

$$
E=\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix},\,F=\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix},\,G=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

Field banks: I: false, true; II: false, true; III: true, false

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}\frac{1}{2} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}-1 & -3 \\ 2 & 2\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## q-71818 changed hard

Consider the matrices

$$
E=\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix},\,F=\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix},\,G=\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

Field banks: I: false, true; II: true, false; III: false, true

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}2 & -3 \\ -2 & \frac{3}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}-\frac{1}{2} & -1 \\ -\frac{2}{3} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & 1 \\ \frac{2}{3} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{3} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

## e-4499 original parameters, completed presentation

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

$$
A=\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}.
$$

Field banks: [Canonical has no captured fields]

We must check whether $AB = BA = I_2.$

Computing $AB,$ we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA,$ we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Therefore, $B = A^{-1}.$

## e-4499 changed easy

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

$$
A=\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix},\,B=\begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}.
$$

Field banks: [Canonical has no captured fields]

We must check whether $AB = BA = I_2.$

Computing $AB,$ we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix}\begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA,$ we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}1 & 0 \\ 1 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Therefore, $B = A^{-1}.$
