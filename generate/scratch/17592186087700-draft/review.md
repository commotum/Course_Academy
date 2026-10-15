# Original source and generated review

Original MA practice is reproduced below with every field-owned Boolean bank and complete worked solution. Raw defects are retained in the original columns; generated originals apply only documented minimal repairs. Each family has a changed-coordinate instance. The last six records demonstrate at least two authored variants of every level. Easy and all variants are uncalibrated.

## Original q-11642 / 17592186087987

Consider the matrices

$$
C=\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix},\,D=\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix},\,E=\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $CD=DC={I}_{3}$
- **II.** $CE=EC={I}_{3}$
- **III.** $E={C}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $E\ne {C}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### original parameter normalized replay

Consider the matrices

$$
C=\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix},\,D=\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix},\,E=\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $CD=DC={I}_{3}$
- **II.** $CE=EC={I}_{3}$
- **III.** $E={C}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}2 & -2 & -1 \\ -1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix}\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}1 & 2 & 1 \\ 0 & 1 & 1 \\ 1 & 2 & 0\end{bmatrix}\begin{bmatrix}2 & -2 & -1 \\ 1 & 1 & 1 \\ 1 & 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $E\ne {C}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### authored changed-parameter same-method source family

Consider the matrices

$$
C=\begin{bmatrix}1 & -1 & 0 \\ -2 & 0 & 1 \\ -2 & 1 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & -1 & 1 \\ 0 & -1 & 1 \\ 2 & -1 & 2\end{bmatrix},\,E=\begin{bmatrix}1 & -1 & -1 \\ 0 & -1 & 1 \\ 2 & -1 & 2\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $CD=DC={I}_{3}$
- **II.** $CE=EC={I}_{3}$
- **III.** $E={C}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}1 & -1 & 0 \\ -2 & 0 & 1 \\ -2 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & 1 \\ 0 & -1 & 1 \\ 2 & -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}1 & -1 & 1 \\ 0 & -1 & 1 \\ 2 & -1 & 2\end{bmatrix}\begin{bmatrix}1 & -1 & 0 \\ -2 & 0 & 1 \\ -2 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}1 & -1 & 0 \\ -2 & 0 & 1 \\ -2 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & -1 \\ 0 & -1 & 1 \\ 2 & -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & 5\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $E\ne {C}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


## Original q-7913 / 17592186088367

Consider the matrices

$$
A=\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix},\,B=\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix},\,C=\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix}\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### original parameter minimal repair

Consider the matrices

$$
A=\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix},\,B=\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix},\,C=\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}3 & -2 & 0 & 0 \\ -4 & 3 & 0 & 0 \\ 0 & 0 & 6 & -5 \\ 0 & 0 & -7 & 6\end{bmatrix}\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}3 & 2 & 0 & 0 \\ 4 & 3 & 0 & 0 \\ 0 & 0 & 6 & 5 \\ 0 & 0 & 7 & 6\end{bmatrix}\begin{bmatrix}-3 & 2 & 0 & 0 \\ 4 & -3 & 0 & 0 \\ 0 & 0 & -6 & 5 \\ 0 & 0 & 7 & -6\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}3 & 0 & 0 & -4 \\ 0 & 6 & 7 & 0 \\ 0 & 5 & 6 & 0 \\ -2 & 0 & 0 & 3\end{bmatrix},\,B=\begin{bmatrix}3 & 0 & 0 & 4 \\ 0 & 6 & -7 & 0 \\ 0 & -5 & 6 & 0 \\ 2 & 0 & 0 & 3\end{bmatrix},\,C=\begin{bmatrix}-3 & 0 & 0 & -4 \\ 0 & -6 & 7 & 0 \\ 0 & 5 & -6 & 0 \\ -2 & 0 & 0 & -3\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}3 & 0 & 0 & -4 \\ 0 & 6 & 7 & 0 \\ 0 & 5 & 6 & 0 \\ -2 & 0 & 0 & 3\end{bmatrix}\begin{bmatrix}3 & 0 & 0 & 4 \\ 0 & 6 & -7 & 0 \\ 0 & -5 & 6 & 0 \\ 2 & 0 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}3 & 0 & 0 & 4 \\ 0 & 6 & -7 & 0 \\ 0 & -5 & 6 & 0 \\ 2 & 0 & 0 & 3\end{bmatrix}\begin{bmatrix}3 & 0 & 0 & -4 \\ 0 & 6 & 7 & 0 \\ 0 & 5 & 6 & 0 \\ -2 & 0 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}3 & 0 & 0 & -4 \\ 0 & 6 & 7 & 0 \\ 0 & 5 & 6 & 0 \\ -2 & 0 & 0 & 3\end{bmatrix}\begin{bmatrix}-3 & 0 & 0 & -4 \\ 0 & -6 & 7 & 0 \\ 0 & 5 & -6 & 0 \\ -2 & 0 & 0 & -3\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & -1\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


## Original q-11634 / 17592186253256

Consider the matrices

$$
A=\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix},\,C=\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $B={A}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{5}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. 
Therefore, the correct answer is "II only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix},\,C=\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $B={A}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}5 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{5}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{5}\begin{bmatrix}-3 & 1 & 8 \\ 2 & 1 & -2 \\ -2 & -1 & 7\end{bmatrix}\begin{bmatrix}-1 & 3 & 2 \\ 2 & 1 & -2 \\ 0 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. 
Therefore, the correct answer is "II only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}1 & 2 & -2 \\ -1 & 1 & 0 \\ -3 & 2 & -1\end{bmatrix},\,B=\begin{bmatrix}1 & 2 & -2 \\ 1 & 7 & -2 \\ -1 & 8 & -3\end{bmatrix},\,C=\frac{1}{5}\begin{bmatrix}1 & 2 & -2 \\ 1 & 7 & -2 \\ -1 & 8 & -3\end{bmatrix}
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $B={A}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 2 & -2 \\ -1 & 1 & 0 \\ -3 & 2 & -1\end{bmatrix}\begin{bmatrix}1 & 2 & -2 \\ 1 & 7 & -2 \\ -1 & 8 & -3\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & 5\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{5}\begin{bmatrix}1 & 2 & -2 \\ -1 & 1 & 0 \\ -3 & 2 & -1\end{bmatrix}\begin{bmatrix}1 & 2 & -2 \\ 1 & 7 & -2 \\ -1 & 8 & -3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{5}\begin{bmatrix}1 & 2 & -2 \\ 1 & 7 & -2 \\ -1 & 8 & -3\end{bmatrix}\begin{bmatrix}1 & 2 & -2 \\ -1 & 1 & 0 \\ -3 & 2 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. 
Therefore, the correct answer is "II only".


## Original q-11636 / 17592186253257

Consider the matrices

$$
A=\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix},\,C=\frac{1}{7}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AC=CA={I}_{3}$
- **II.** $AD=DA={I}_{3}$
- **III.** $D={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{7}\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{7}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix}\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AD=DA={I}_{3}.$ Computing $AD$, we get

$$
\begin{aligned}AD & =\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & 7 & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $D\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix},\,C=\frac{1}{7}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AC=CA={I}_{3}$
- **II.** $AD=DA={I}_{3}$
- **III.** $D={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{7}\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{7}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix}\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AD=DA={I}_{3}.$ Computing $AD$, we get

$$
\begin{aligned}AD & =\begin{bmatrix}3 & 4 & 0 \\ -2 & 3 & 1 \\ -1 & 1 & 0\end{bmatrix}\begin{bmatrix}1 & 0 & -4 \\ 1 & 0 & 3 \\ -1 & 7 & -17\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & 7 & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $D\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}3 & -1 & 2 \\ -1 & 0 & -1 \\ -4 & 0 & 3\end{bmatrix},\,C=\frac{1}{7}\begin{bmatrix}0 & -3 & -1 \\ -7 & -17 & -1 \\ 0 & -4 & 1\end{bmatrix},\,D=\begin{bmatrix}0 & -3 & -1 \\ -7 & -17 & -1 \\ 0 & -4 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AC=CA={I}_{3}$
- **II.** $AD=DA={I}_{3}$
- **III.** $D={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\frac{1}{7}\begin{bmatrix}3 & -1 & 2 \\ -1 & 0 & -1 \\ -4 & 0 & 3\end{bmatrix}\begin{bmatrix}0 & -3 & -1 \\ -7 & -17 & -1 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\frac{1}{7}\begin{bmatrix}0 & -3 & -1 \\ -7 & -17 & -1 \\ 0 & -4 & 1\end{bmatrix}\begin{bmatrix}3 & -1 & 2 \\ -1 & 0 & -1 \\ -4 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AD=DA={I}_{3}.$ Computing $AD$, we get

$$
\begin{aligned}AD & =\begin{bmatrix}3 & -1 & 2 \\ -1 & 0 & -1 \\ -4 & 0 & 3\end{bmatrix}\begin{bmatrix}0 & -3 & -1 \\ -7 & -17 & -1 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & 7\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $D\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


## Original q-149818 / 17592186275250

Consider the matrices

$$
A=\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix},\,C=\begin{bmatrix}-2 & 2 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 0 & -3 & 3 \\ 0 & 0 & 2 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix}\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix}\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix}\begin{bmatrix}-2 & 2 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 0 & -3 & 3 \\ 0 & 0 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is fasle too.

Therefore, the correct answer is "I only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix},\,C=\begin{bmatrix}-2 & 2 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 0 & -3 & 3 \\ 0 & 0 & 2 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix}\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & -7 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 1 & -2 \\ 0 & 0 & -2 & 5\end{bmatrix}\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}4 & 7 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 2 \\ 0 & 0 & 2 & 1\end{bmatrix}\begin{bmatrix}-2 & 2 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 0 & 0 & -3 & 3 \\ 0 & 0 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 2 & 5 & 0 \\ -7 & 0 & 0 & 4\end{bmatrix},\,B=\begin{bmatrix}4 & 0 & 0 & 1 \\ 0 & 5 & -2 & 0 \\ 0 & -2 & 1 & 0 \\ 7 & 0 & 0 & 2\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 3 & -3 & 0 \\ -2 & 0 & 0 & -2\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 2 & 5 & 0 \\ -7 & 0 & 0 & 4\end{bmatrix}\begin{bmatrix}4 & 0 & 0 & 1 \\ 0 & 5 & -2 & 0 \\ 0 & -2 & 1 & 0 \\ 7 & 0 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}4 & 0 & 0 & 1 \\ 0 & 5 & -2 & 0 \\ 0 & -2 & 1 & 0 \\ 7 & 0 & 0 & 2\end{bmatrix}\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 2 & 5 & 0 \\ -7 & 0 & 0 & 4\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 2 & 5 & 0 \\ -7 & 0 & 0 & 4\end{bmatrix}\begin{bmatrix}1 & 0 & 0 & -1 \\ 0 & 1 & 2 & 0 \\ 0 & 3 & -3 & 0 \\ -2 & 0 & 0 & -2\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & 17 & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


## Original q-149820 / 17592186275251

Consider the matrices

$$
B=\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix},\,C=\begin{bmatrix}1 & 2 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix},\,D=\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{4}$
- **II.** $BD=DB={I}_{4}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}1 & 2 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix} \\  & =\begin{bmatrix}-2 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, the statement I is false.

- Now, we check whether $BD=DB={I}_{4}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


### original parameter minimal repair

Consider the matrices

$$
B=\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix},\,C=\begin{bmatrix}1 & 2 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix},\,D=\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{4}$
- **II.** $BD=DB={I}_{4}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{4}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}1 & 2 & 0 & 0 \\ -1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix} \\  & =\begin{bmatrix}-2 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, the statement I is false.

- Now, we check whether $BD=DB={I}_{4}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}2 & -5 & 0 & 0 \\ -1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}\begin{bmatrix}3 & 5 & 0 & 0 \\ 1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
B=\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 2 & 3 & 0 \\ 0 & 3 & 5 & 0 \\ -5 & 0 & 0 & 3\end{bmatrix},\,C=\begin{bmatrix}4 & 0 & 0 & 1 \\ 0 & 2 & 7 & 0 \\ 0 & 1 & 3 & 0 \\ -2 & 0 & 0 & 1\end{bmatrix},\,D=\begin{bmatrix}3 & 0 & 0 & 1 \\ 0 & 5 & -3 & 0 \\ 0 & -3 & 2 & 0 \\ 5 & 0 & 0 & 2\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{4}$
- **II.** $BD=DB={I}_{4}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{4}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 2 & 3 & 0 \\ 0 & 3 & 5 & 0 \\ -5 & 0 & 0 & 3\end{bmatrix}\begin{bmatrix}4 & 0 & 0 & 1 \\ 0 & 2 & 7 & 0 \\ 0 & 1 & 3 & 0 \\ -2 & 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & -2\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, the statement I is false.

- Now, we check whether $BD=DB={I}_{4}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 2 & 3 & 0 \\ 0 & 3 & 5 & 0 \\ -5 & 0 & 0 & 3\end{bmatrix}\begin{bmatrix}3 & 0 & 0 & 1 \\ 0 & 5 & -3 & 0 \\ 0 & -3 & 2 & 0 \\ 5 & 0 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}3 & 0 & 0 & 1 \\ 0 & 5 & -3 & 0 \\ 0 & -3 & 2 & 0 \\ 5 & 0 & 0 & 2\end{bmatrix}\begin{bmatrix}2 & 0 & 0 & -1 \\ 0 & 2 & 3 & 0 \\ 0 & 3 & 5 & 0 \\ -5 & 0 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


## Original q-149832 / 17592186275252

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix},\,B=\begin{bmatrix}2 & 1 & -1 \\ -3 & 2 & -1 \\ 3 & -3 & 2\end{bmatrix},\,C=\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{3}$

II. $AC=CA={I}_{3}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix}\begin{bmatrix}2 & 1 & -1 \\ -3 & 2 & -1 \\ 3 & -3 & 2\end{bmatrix} \\  & =\begin{bmatrix}2 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix}\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix}\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix},\,B=\begin{bmatrix}2 & 1 & -1 \\ -3 & 2 & -1 \\ 3 & -3 & 2\end{bmatrix},\,C=\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{3}$

II. $AC=CA={I}_{3}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix}\begin{bmatrix}2 & 1 & -1 \\ -3 & 2 & -1 \\ 3 & -3 & 2\end{bmatrix} \\  & =\begin{bmatrix}2 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix}\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-1 & -1 & 1 \\ -5 & 0 & 1 \\ 7 & 1 & -2\end{bmatrix}\begin{bmatrix}1 & 1 & 1 \\ 3 & 5 & 4 \\ 5 & 6 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}5 & -4 & -3 \\ -6 & 5 & 5 \\ -1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 1 & 3 \\ 3 & 2 & 3 \\ -1 & -1 & 2\end{bmatrix},\,C=\begin{bmatrix}0 & -1 & 5 \\ -1 & -2 & 7 \\ 1 & 1 & -1\end{bmatrix}.
$$

Which of the following statements are true?

I. $AB=BA={I}_{3}$

II. $AC=CA={I}_{3}$

III. $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}5 & -4 & -3 \\ -6 & 5 & 5 \\ -1 & 1 & 1\end{bmatrix}\begin{bmatrix}2 & 1 & 3 \\ 3 & 2 & 3 \\ -1 & -1 & 2\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & 7 \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}5 & -4 & -3 \\ -6 & 5 & 5 \\ -1 & 1 & 1\end{bmatrix}\begin{bmatrix}0 & -1 & 5 \\ -1 & -2 & 7 \\ 1 & 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}0 & -1 & 5 \\ -1 & -2 & 7 \\ 1 & 1 & -1\end{bmatrix}\begin{bmatrix}5 & -4 & -3 \\ -6 & 5 & 5 \\ -1 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


## Original q-149833 / 17592186275253

Consider the matrices

$$
E=\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix},\,F=\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix},\,G=\begin{bmatrix}1 & -3 & 4 \\ 0 & 2 & 3 \\ 3 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $EF=FE={I}_{3}$
- **II.** $FG=GF={I}_{3}$
- **III.** $F={G}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $EF=FE={I}_{3}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\frac{1}{3}\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix}\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $FG=GF={I}_{3}.$ Computing $FG$, we get

$$
\begin{aligned}FG & =\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix}\begin{bmatrix}1 & -3 & 4 \\ 0 & 2 & 3 \\ 3 & 0 & 1\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}-8 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $F\ne {G}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### original parameter normalized replay

Consider the matrices

$$
E=\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix},\,F=\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix},\,G=\begin{bmatrix}1 & -3 & 4 \\ 0 & 2 & 3 \\ 3 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $EF=FE={I}_{3}$
- **II.** $FG=GF={I}_{3}$
- **III.** $F={G}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $EF=FE={I}_{3}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\frac{1}{3}\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix}\begin{bmatrix}1 & -1 & 1 \\ 2 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $FG=GF={I}_{3}.$ Computing $FG$, we get

$$
\begin{aligned}FG & =\frac{1}{3}\begin{bmatrix}1 & 1 & -3 \\ -2 & 1 & 0 \\ 0 & 0 & 3\end{bmatrix}\begin{bmatrix}1 & -3 & 4 \\ 0 & 2 & 3 \\ 3 & 0 & 1\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}-8 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $F\ne {G}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


### authored changed-parameter same-method source family

Consider the matrices

$$
E=\begin{bmatrix}1 & -2 & -2 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix},\,F=\frac{1}{3}\begin{bmatrix}1 & 0 & 2 \\ 0 & 3 & 0 \\ -1 & -3 & 1\end{bmatrix},\,G=\begin{bmatrix}2 & -3 & 0 \\ 0 & 1 & 3 \\ 3 & 4 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $EF=FE={I}_{3}$
- **II.** $FG=GF={I}_{3}$
- **III.** $F={G}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $EF=FE={I}_{3}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\frac{1}{3}\begin{bmatrix}1 & -2 & -2 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 2 \\ 0 & 3 & 0 \\ -1 & -3 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\frac{1}{3}\begin{bmatrix}1 & 0 & 2 \\ 0 & 3 & 0 \\ -1 & -3 & 1\end{bmatrix}\begin{bmatrix}1 & -2 & -2 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $FG=GF={I}_{3}.$ Computing $FG$, we get

$$
\begin{aligned}FG & =\frac{1}{3}\begin{bmatrix}1 & 0 & 2 \\ 0 & 3 & 0 \\ -1 & -3 & 1\end{bmatrix}\begin{bmatrix}2 & -3 & 0 \\ 0 & 1 & 3 \\ 3 & 4 & 1\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & -8\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $F\ne {G}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


## Original q-71876 / 17592186339006

Consider the matrices

$$
C=\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix},\,D=\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}0 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & -2\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{3}$

- **II.** $CE=EC={I}_{3}$

- **III.** $D={C}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}0 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & -2\end{bmatrix} \\  & =\begin{bmatrix}∗ & 3 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### original parameter normalized replay

Consider the matrices

$$
C=\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix},\,D=\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}0 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & -2\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{3}$

- **II.** $CE=EC={I}_{3}$

- **III.** $D={C}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}0 & 1 & 0 \\ 1 & -2 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}2 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}0 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & -2\end{bmatrix} \\  & =\begin{bmatrix}∗ & 3 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
C=\begin{bmatrix}0 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 2\end{bmatrix},\,D=\begin{bmatrix}-2 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 0\end{bmatrix},\,E=\begin{bmatrix}1 & 0 & -1 \\ 0 & -2 & 0 \\ -1 & 0 & 0\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{3}$

- **II.** $CE=EC={I}_{3}$

- **III.** $D={C}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $CD=DC={I}_{3}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}0 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 2\end{bmatrix}\begin{bmatrix}-2 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}-2 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 0\end{bmatrix}\begin{bmatrix}0 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $CE=EC={I}_{3}.$ Computing $CE$, we get

$$
\begin{aligned}CE & =\begin{bmatrix}0 & 0 & -1 \\ 0 & 1 & 0 \\ -1 & 0 & 2\end{bmatrix}\begin{bmatrix}1 & 0 & -1 \\ 0 & -2 & 0 \\ -1 & 0 & 0\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ -3 & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


## Original q-71879 / 17592186339007

Consider the matrices

$$
A=\begin{bmatrix}0 & -1 & -1 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $BC=CB={I}_{3}$

- **III.** $A={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}0 & -1 & -1 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}∗ & -1 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $A\ne {B}^{-1}$ and statement III is false too.

- Now, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix}\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CB$, we get

$$
\begin{aligned}CB & =\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}0 & -1 & -1 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $BC=CB={I}_{3}$

- **III.** $A={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}0 & -1 & -1 \\ 0 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}∗ & -1 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $A\ne {B}^{-1}$ and statement III is false too.

- Now, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix}\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CB$, we get

$$
\begin{aligned}CB & =\begin{bmatrix}0 & -\frac{1}{2} & -1 \\ 0 & \frac{1}{2} & 0 \\ 1 & \frac{1}{2} & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ -1 & -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & 0 \\ -1 & 1 & 1 \\ 1 & -1 & 0\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & 0 \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{bmatrix},\,C=\begin{bmatrix}\frac{1}{2} & 0 & 0 \\ -\frac{1}{2} & 1 & 1 \\ \frac{1}{2} & -1 & 0\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $BC=CB={I}_{3}$

- **III.** $A={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ -1 & 1 & 1 \\ 1 & -1 & 0\end{bmatrix}\begin{bmatrix}2 & 0 & 0 \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ 1 & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $A\ne {B}^{-1}$ and statement III is false too.

- Now, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}2 & 0 & 0 \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{bmatrix}\begin{bmatrix}\frac{1}{2} & 0 & 0 \\ -\frac{1}{2} & 1 & 1 \\ \frac{1}{2} & -1 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $CB$, we get

$$
\begin{aligned}CB & =\begin{bmatrix}\frac{1}{2} & 0 & 0 \\ -\frac{1}{2} & 1 & 1 \\ \frac{1}{2} & -1 & 0\end{bmatrix}\begin{bmatrix}2 & 0 & 0 \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".


## Original q-7905 / 17592186348160

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $AE=EA={I}_{3}$

- **III.** $B={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AE=EA={I}_{3}.$ Computing $AE$, we get

$$
\begin{aligned}AE & =\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ -10 & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### original parameter normalized replay

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $AE=EA={I}_{3}$

- **III.** $B={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AE=EA={I}_{3}.$ Computing $AE$, we get

$$
\begin{aligned}AE & =\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ -10 & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & -5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $AE=EA={I}_{3}$

- **III.** $B={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & -5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 & -5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AE=EA={I}_{3}.$ Computing $AE$, we get

$$
\begin{aligned}AE & =\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 5 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & 10 \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


## Original q-7907 / 17592186348161

Consider the matrices

$$
B=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix},\,C=\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{3}$
- **II.** $BD=DB={I}_{3}$
- **III.** $D={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{15} & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Note, we check whether $BD=DB={I}_{3}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


### original parameter normalized replay

Consider the matrices

$$
B=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix},\,C=\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{3}$
- **II.** $BD=DB={I}_{3}$
- **III.** $D={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{15} & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Note, we check whether $BD=DB={I}_{3}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 4 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
B=\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,C=\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & 0 \\ -4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $BC=CB={I}_{3}$
- **II.** $BD=DB={I}_{3}$
- **III.** $D={B}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{3}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\frac{1}{15}\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & \frac{1}{15}\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Note, we check whether $BD=DB={I}_{3}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}1 & 0 & 0 \\ -4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 4 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


## Original q-7909 / 17592186348162

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-1 & -1 & -1 \\ -1 & -1 & 0 \\ -1 & -1 & -1\end{bmatrix},\,C=\begin{bmatrix}1 & -1 & -1 \\ 1 & 1 & 0 \\ -1 & -1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $A\ne {C}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}-1 & -1 & -1 \\ -1 & -1 & 0 \\ -1 & -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}-3 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & -1 \\ 1 & 1 & 1 \\ -1 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & -1 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $A\ne {C}^{-1}$ and statement III is true.

Therefore, the correct answer is "III only".


### original parameter minimal repair

Consider the matrices

$$
A=\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-1 & -1 & -1 \\ -1 & -1 & 0 \\ -1 & -1 & -1\end{bmatrix},\,C=\begin{bmatrix}1 & -1 & -1 \\ 1 & 1 & 0 \\ -1 & -1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $A\ne {C}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}-1 & -1 & -1 \\ -1 & -1 & 0 \\ -1 & -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}-3 & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & -1 \\ 1 & 1 & 0 \\ -1 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & -1 & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $A\ne {C}^{-1}$ and statement III is true.

Therefore, the correct answer is "III only".


### authored changed-parameter same-method source family

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & -1 \\ -1 & 1 & 1 \\ -1 & 1 & 1\end{bmatrix},\,B=\begin{bmatrix}-1 & 0 & 1 \\ 1 & -1 & -1 \\ 1 & -1 & -1\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & -1 \\ 1 & 1 & -1 \\ 1 & -1 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$
- **II.** $AC=CA={I}_{3}$
- **III.** $A\ne {C}^{-1}$

Field I: false, true; correct false.

Field II: false, true; correct false.

Field III: true, false; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & -1 \\ -1 & 1 & 1 \\ -1 & 1 & 1\end{bmatrix}\begin{bmatrix}-1 & 0 & 1 \\ 1 & -1 & -1 \\ 1 & -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & -2 & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{3}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}1 & 0 & -1 \\ -1 & 1 & 1 \\ -1 & 1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & -1 \\ 1 & 1 & -1 \\ 1 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ 1 & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $A\ne {C}^{-1}$ and statement III is true.

Therefore, the correct answer is "III only".


## authored uncalibrated easy

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

$$
A=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -1 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -1 & 1\end{bmatrix}.
$$

- **I.** $B=A^{-1}$

Select the statement if it is true. Leave the box unchecked otherwise.

Field I: true, false; correct false.

Worked solution:

First, we check whether $AB = BA = I_3.$

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -1 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & -1 & 1\end{bmatrix} \\ & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ \\ ∗ & -2 & ∗\end{bmatrix} \\ & \ne {I}_{3}.\,\times \end{aligned}
$$

Therefore, $B\ne A^{-1}.$


## authored uncalibrated easy

Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where

$$
A=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix}.
$$

- **I.** $B=A^{-1}$

Select the statement if it is true. Leave the box unchecked otherwise.

Field I: false, true; correct false.

Worked solution:

First, we check whether $AB = BA = I_3.$

Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 1\end{bmatrix} \\ & =\begin{bmatrix}∗ & ∗ & ∗ \\ ∗ & ∗ & -2 \\ ∗ & ∗ & ∗\end{bmatrix} \\ & \ne {I}_{3}.\,\times \end{aligned}
$$

Therefore, $B\ne A^{-1}.$


## authored uncalibrated moderate

Consider the matrices

$$
A=\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $AB=BA={I}_{3}$

- **II.** $AE=EA={I}_{3}$

- **III.** $B={A}^{-1}$

Field I: false, true; correct true.

Field II: false, true; correct false.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $AB=BA={I}_{3}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}1 & 0 & 0 \\ -5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $B={A}^{-1}$ and statement III is true too.

- Now, we check whether $AE=EA={I}_{3}.$ Computing $AE$, we get

$$
\begin{aligned}AE & =\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 & 0 \\ 5 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ \\ 10 & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".


## authored uncalibrated moderate

Consider the matrices

$$
E=\begin{bmatrix}1 & -1 & -1 \\ 0 & 1 & 0 \\ 2 & -2 & 1\end{bmatrix},\,F=\frac{1}{3}\begin{bmatrix}1 & 3 & 1 \\ 0 & 3 & 0 \\ -2 & 0 & 1\end{bmatrix},\,G=\begin{bmatrix}1 & -4 & -3 \\ -3 & 1 & 0 \\ 0 & -3 & 2\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $EF=FE={I}_{3}$
- **II.** $FG=GF={I}_{3}$
- **III.** $F={G}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: true, false; correct true.

Field II: true, false; correct false.

Field III: false, true; correct false.

Worked solution:

- First, we check whether $EF=FE={I}_{3}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\frac{1}{3}\begin{bmatrix}1 & -1 & -1 \\ 0 & 1 & 0 \\ 2 & -2 & 1\end{bmatrix}\begin{bmatrix}1 & 3 & 1 \\ 0 & 3 & 0 \\ -2 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\frac{1}{3}\begin{bmatrix}1 & 3 & 1 \\ 0 & 3 & 0 \\ -2 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & -1 & -1 \\ 0 & 1 & 0 \\ 2 & -2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} \\  & ={I}_{3}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $FG=GF={I}_{3}.$ Computing $FG$, we get

$$
\begin{aligned}FG & =\frac{1}{3}\begin{bmatrix}1 & 3 & 1 \\ 0 & 3 & 0 \\ -2 & 0 & 1\end{bmatrix}\begin{bmatrix}1 & -4 & -3 \\ -3 & 1 & 0 \\ 0 & -3 & 2\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}∗ & ∗ & -1 \\ ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{3}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $F\ne {G}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".


## authored uncalibrated hard

Consider the matrices

$$
B=\begin{bmatrix}3 & -5 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix},\,C=\begin{bmatrix}1 & -2 & 0 & 0 \\ 1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix},\,D=\begin{bmatrix}2 & 5 & 0 & 0 \\ 1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $BC=CB={I}_{4}$
- **II.** $BD=DB={I}_{4}$
- **III.** $D={B}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct false.

Field II: false, true; correct true.

Field III: false, true; correct true.

Worked solution:

- First, we check whether $BC=CB={I}_{4}.$ Computing $BC$, we get

$$
\begin{aligned}BC & =\begin{bmatrix}3 & -5 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}1 & -2 & 0 & 0 \\ 1 & 4 & 0 & 0 \\ 0 & 0 & 3 & 1 \\ 0 & 0 & 7 & 2\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & 36 & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, the statement I is false.

- Now, we check whether $BD=DB={I}_{4}.$ Computing $BD$, we get

$$
\begin{aligned}BD & =\begin{bmatrix}3 & -5 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix}\begin{bmatrix}2 & 5 & 0 & 0 \\ 1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $DB$, we get

$$
\begin{aligned}DB & =\begin{bmatrix}2 & 5 & 0 & 0 \\ 1 & 3 & 0 & 0 \\ 0 & 0 & 2 & -3 \\ 0 & 0 & -3 & 5\end{bmatrix}\begin{bmatrix}3 & -5 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 0 & 0 & 5 & 3 \\ 0 & 0 & 3 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $D={B}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".


## authored uncalibrated hard

Consider the matrices

$$
A=\begin{bmatrix}4 & 0 & -7 & 0 \\ 0 & 5 & 0 & -2 \\ -1 & 0 & 2 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}2 & 0 & 7 & 0 \\ 0 & 1 & 0 & 2 \\ 1 & 0 & 4 & 0 \\ 0 & 2 & 0 & 5\end{bmatrix},\,C=\begin{bmatrix}-2 & 0 & -2 & 0 \\ 0 & -3 & 0 & -3 \\ -1 & 0 & 1 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{4}$
- **II.** $AC=CA={I}_{4}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

Field I: false, true; correct true.

Field II: true, false; correct false.

Field III: true, false; correct false.

Worked solution:

- First, we check whether $AB=BA={I}_{4}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}4 & 0 & -7 & 0 \\ 0 & 5 & 0 & -2 \\ -1 & 0 & 2 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix}\begin{bmatrix}2 & 0 & 7 & 0 \\ 0 & 1 & 0 & 2 \\ 1 & 0 & 4 & 0 \\ 0 & 2 & 0 & 5\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}2 & 0 & 7 & 0 \\ 0 & 1 & 0 & 2 \\ 1 & 0 & 4 & 0 \\ 0 & 2 & 0 & 5\end{bmatrix}\begin{bmatrix}4 & 0 & -7 & 0 \\ 0 & 5 & 0 & -2 \\ -1 & 0 & 2 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix} \\  & ={I}_{4}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{4}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}4 & 0 & -7 & 0 \\ 0 & 5 & 0 & -2 \\ -1 & 0 & 2 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix}\begin{bmatrix}-2 & 0 & -2 & 0 \\ 0 & -3 & 0 & -3 \\ -1 & 0 & 1 & 0 \\ 0 & -2 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}-1 & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗ \\ ∗ & ∗ & ∗ & ∗\end{bmatrix} \\  & \ne {I}_{4}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

