# Distributivity source and generated review

Frozen basis2275. Raw missing grade/key/solution/fields and duplicate legacy fields remain evidence-only. Normal variants below are authored method banks. Hard is authored; calibration remains uncertain.

## Original q-13535

Find $Q + R - (Q + P)$, if

$P = \begin{bmatrix}3 & 4 \\ 2 & 1\end{bmatrix}, Q = \begin{bmatrix}6 & 7 \\ 2 & 3\end{bmatrix}, R = \begin{bmatrix}5 & 6 \\ 6 & 7\end{bmatrix}$.

selection:
- $\begin{bmatrix}1 & 2 \\ 4 & 6\end{bmatrix}$
- $\begin{bmatrix}2 & 2 \\ 3 & 6\end{bmatrix}$
- $\begin{bmatrix}2 & 2 \\ 4 & 5\end{bmatrix}$
- $\begin{bmatrix}2 & 1 \\ 4 & 6\end{bmatrix}$
- $\begin{bmatrix}2 & 2 \\ 4 & 6\end{bmatrix}$

[Absent in raw source]

## Authored method bank at original parameters

Find $Q + R - (Q + P)$, if

$P = \begin{bmatrix}3 & 4 \\ 2 & 1\end{bmatrix}, Q = \begin{bmatrix}6 & 7 \\ 2 & 3\end{bmatrix}, R = \begin{bmatrix}5 & 6 \\ 6 & 7\end{bmatrix}$.

selection:
- $\begin{bmatrix}-2 & -2 \\ -4 & -6\end{bmatrix}$
- $\begin{bmatrix}2 & 2 \\ 4 & 6\end{bmatrix}$ (correct)
- $\begin{bmatrix}8 & 9 \\ 6 & 9\end{bmatrix}$
- $\begin{bmatrix}-4 & -5 \\ 2 & 3\end{bmatrix}$
- $\begin{bmatrix}8 & 10 \\ 8 & 8\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}Q + R - (Q + P) & =Q+R-Q-P \\  & =\cancel{Q}+R-\cancel{Q}-P \\  & =R-P\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}R-P & =\begin{bmatrix}5 & 6 \\ 6 & 7\end{bmatrix}-\begin{bmatrix}3 & 4 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}5-3 & 6-4 \\ 6-2 & 7-1\end{bmatrix} \\  & =\begin{bmatrix}2 & 2 \\ 4 & 6\end{bmatrix}\end{aligned}
$$

## Original q-13536

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix},\,B=\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix},\,C=\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$
- $\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix}$
- $\begin{bmatrix}5 & 7 \\ 7 & 5\end{bmatrix}$
- $\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}$
- $\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}$

selection:
- $\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix}$
- $\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}$ (correct)
- $\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}$
- $\begin{bmatrix}5 & 7 \\ 7 & 5\end{bmatrix}$
- $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix},\,B=\begin{bmatrix}3 & 2 \\ 2 & 3\end{bmatrix},\,C=\begin{bmatrix}5 & 1 \\ 6 & 8\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}12 & 11 \\ 8 & 11\end{bmatrix}$
- $\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}$ (correct)
- $\begin{bmatrix}3 & 5 \\ 2 & 2\end{bmatrix}$
- $\begin{bmatrix}1 & 6 \\ -2 & -3\end{bmatrix}$
- $\begin{bmatrix}-4 & 5 \\ -8 & -11\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}6 & 7 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

## Original q-13550

Find $K+L-(K+J)$, if

$$
J=\begin{bmatrix}5 & 2 \\ 2 & 1\end{bmatrix},\,K=\begin{bmatrix}9 & 8 \\ 2 & 3\end{bmatrix},\,L=\begin{bmatrix}6 & 6 \\ 6 & 6\end{bmatrix}.
$$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}K+L-(K+J) & =K+L-K-J \\  & =\cancel{K}+L-\cancel{K}-J \\  & =L-J\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}L-J & =\begin{bmatrix}6 & 6 \\ 6 & 6\end{bmatrix}-\begin{bmatrix}5 & 2 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}6-5 & 6-2 \\ 6-2 & 6-1\end{bmatrix} \\  & =\begin{bmatrix}1 & 4 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $K+L-(K+J)$, if

$$
J=\begin{bmatrix}5 & 2 \\ 2 & 1\end{bmatrix},\,K=\begin{bmatrix}9 & 8 \\ 2 & 3\end{bmatrix},\,L=\begin{bmatrix}6 & 6 \\ 6 & 6\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-1 & -4 \\ -4 & -5\end{bmatrix}$
- $\begin{bmatrix}1 & 4 \\ 4 & 5\end{bmatrix}$ (correct)
- $\begin{bmatrix}10 & 12 \\ 6 & 8\end{bmatrix}$
- $\begin{bmatrix}-8 & -4 \\ 2 & 2\end{bmatrix}$
- $\begin{bmatrix}11 & 8 \\ 8 & 7\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}K+L-(K+J) & =K+L-K-J \\  & =\cancel{K}+L-\cancel{K}-J \\  & =L-J\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}L-J & =\begin{bmatrix}6 & 6 \\ 6 & 6\end{bmatrix}-\begin{bmatrix}5 & 2 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}6-5 & 6-2 \\ 6-2 & 6-1\end{bmatrix} \\  & =\begin{bmatrix}1 & 4 \\ 4 & 5\end{bmatrix}\end{aligned}
$$

## Original q-13543

Find $M+O-(N+M)$, if

$$
M=\begin{bmatrix}5 & 5 \\ 0 & 1\end{bmatrix},\,N=\begin{bmatrix}1 & 4 \\ 2 & -1\end{bmatrix},\,O=\begin{bmatrix}8 & 6 \\ 5 & 3\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}7 & 2 \\ 3 & 3\end{bmatrix}$
- $\begin{bmatrix}7 & 1 \\ 3 & 4\end{bmatrix}$
- $\begin{bmatrix}7 & 2 \\ 2 & 4\end{bmatrix}$
- $\begin{bmatrix}7 & 2 \\ 3 & 4\end{bmatrix}$ (correct)
- $\begin{bmatrix}6 & 2 \\ 3 & 4\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}M+O-(N+M) & =M+O-N-M \\  & =\cancel{M}+O-N-\cancel{M} \\  & =O-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}O-N & =\begin{bmatrix}8 & 6 \\ 5 & 3\end{bmatrix}-\begin{bmatrix}1 & 4 \\ 2 & -1\end{bmatrix} \\  & =\begin{bmatrix}8-1 & 6-4 \\ 5-2 & 3-(-1)\end{bmatrix} \\  & =\begin{bmatrix}7 & 2 \\ 3 & 4\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $M+O-(N+M)$, if

$$
M=\begin{bmatrix}5 & 5 \\ 0 & 1\end{bmatrix},\,N=\begin{bmatrix}1 & 4 \\ 2 & -1\end{bmatrix},\,O=\begin{bmatrix}8 & 6 \\ 5 & 3\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-7 & -2 \\ -3 & -4\end{bmatrix}$
- $\begin{bmatrix}7 & 2 \\ 3 & 4\end{bmatrix}$ (correct)
- $\begin{bmatrix}12 & 7 \\ 3 & 5\end{bmatrix}$
- $\begin{bmatrix}2 & -3 \\ 3 & 3\end{bmatrix}$
- $\begin{bmatrix}9 & 10 \\ 7 & 2\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}M+O-(N+M) & =M+O-N-M \\  & =\cancel{M}+O-N-\cancel{M} \\  & =O-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}O-N & =\begin{bmatrix}8 & 6 \\ 5 & 3\end{bmatrix}-\begin{bmatrix}1 & 4 \\ 2 & -1\end{bmatrix} \\  & =\begin{bmatrix}8-1 & 6-4 \\ 5-2 & 3-(-1)\end{bmatrix} \\  & =\begin{bmatrix}7 & 2 \\ 3 & 4\end{bmatrix}\end{aligned}
$$

## Original q-279581

Find $A+B-(C+B)$, if

$$
A=\begin{bmatrix}2 & -5 \\ 7 & 0\end{bmatrix},\,B=\begin{bmatrix}-1 & 4 \\ 3 & 6\end{bmatrix},\,C=\begin{bmatrix}8 & -2 \\ -4 & 1\end{bmatrix}.
$$

| $A+B-(C+B)=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

field-1:
- $-6$ (correct)

field-3:
- $11$ (correct)

field-4:
- $-1$ (correct)

field-2:
- $-3$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}A+B-(C+B) & =A+B-C-B \\  & =A+\cancel{B}-C-\cancel{B} \\  & =A-C\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-C & =\begin{bmatrix}2 & -5 \\ 7 & 0\end{bmatrix}-\begin{bmatrix}8 & -2 \\ -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}2-8 & -5-(-2) \\ 7-(-4) & 0-1\end{bmatrix} \\  & =\begin{bmatrix}-6 & -3 \\ 11 & -1\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $A+B-(C+B)$, if

$$
A=\begin{bmatrix}2 & -5 \\ 7 & 0\end{bmatrix},\,B=\begin{bmatrix}-1 & 4 \\ 3 & 6\end{bmatrix},\,C=\begin{bmatrix}8 & -2 \\ -4 & 1\end{bmatrix}.
$$

| $A+B-(C+B)=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

field-1:
- $-6$ (correct)

field-2:
- $-3$ (correct)

field-3:
- $11$ (correct)

field-4:
- $-1$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}A+B-(C+B) & =A+B-C-B \\  & =A+\cancel{B}-C-\cancel{B} \\  & =A-C\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-C & =\begin{bmatrix}2 & -5 \\ 7 & 0\end{bmatrix}-\begin{bmatrix}8 & -2 \\ -4 & 1\end{bmatrix} \\  & =\begin{bmatrix}2-8 & -5-(-2) \\ 7-(-4) & 0-1\end{bmatrix} \\  & =\begin{bmatrix}-6 & -3 \\ 11 & -1\end{bmatrix}\end{aligned}
$$

## Original q-69623

Find $G+H-(H+F)$, if

$$
F=\begin{bmatrix}2 & -1 & 2 \\ 3 & 4 & 1\end{bmatrix},\,G=\begin{bmatrix}5 & 4 & -5 \\ 1 & -2 & 2\end{bmatrix},\,H=\begin{bmatrix}1 & 3 & -2 \\ 5 & -1 & 4\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}7 & 3 & 7 \\ 4 & -2 & 3\end{bmatrix}$
- $\begin{bmatrix}-2 & -6 & 1 \\ 3 & 5 & -7\end{bmatrix}$
- $\begin{bmatrix}3 & 5 & -7 \\ -2 & -6 & 1\end{bmatrix}$ (correct)
- $\begin{bmatrix}3 & 5 & -7 \\ -4 & 6 & 3\end{bmatrix}$
- $\begin{bmatrix}5 & 3 & -7 \\ -6 & -2 & 1\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}G+H-(H+F) & =G+H-H-F \\  & =G+\cancel{H}-\cancel{H}-F \\  & =G-F\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}G-F & =\begin{bmatrix}5 & 4 & -5 \\ 1 & -2 & 2\end{bmatrix}-\begin{bmatrix}2 & -1 & 2 \\ 3 & 4 & 1\end{bmatrix} \\  & =\begin{bmatrix}5-2 & 4-(-1) & -5-2 \\ 1-3 & -2-4 & 2-1\end{bmatrix} \\  & =\begin{bmatrix}3 & 5 & -7 \\ -2 & -6 & 1\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $G+H-(H+F)$, if

$$
F=\begin{bmatrix}2 & -1 & 2 \\ 3 & 4 & 1\end{bmatrix},\,G=\begin{bmatrix}5 & 4 & -5 \\ 1 & -2 & 2\end{bmatrix},\,H=\begin{bmatrix}1 & 3 & -2 \\ 5 & -1 & 4\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-3 & -5 & 7 \\ 2 & 6 & -1\end{bmatrix}$
- $\begin{bmatrix}3 & 5 & -7 \\ -2 & -6 & 1\end{bmatrix}$ (correct)
- $\begin{bmatrix}4 & 8 & -9 \\ 3 & -7 & 5\end{bmatrix}$
- $\begin{bmatrix}2 & 2 & -5 \\ -7 & -5 & -3\end{bmatrix}$
- $\begin{bmatrix}7 & 3 & -3 \\ 4 & 2 & 3\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}G+H-(H+F) & =G+H-H-F \\  & =G+\cancel{H}-\cancel{H}-F \\  & =G-F\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}G-F & =\begin{bmatrix}5 & 4 & -5 \\ 1 & -2 & 2\end{bmatrix}-\begin{bmatrix}2 & -1 & 2 \\ 3 & 4 & 1\end{bmatrix} \\  & =\begin{bmatrix}5-2 & 4-(-1) & -5-2 \\ 1-3 & -2-4 & 2-1\end{bmatrix} \\  & =\begin{bmatrix}3 & 5 & -7 \\ -2 & -6 & 1\end{bmatrix}\end{aligned}
$$

## Original q-69627

Find $C+V-(N+C)$, if

$$
C=\begin{bmatrix}10 & -1 \\ 3 & 25 \\ -57 & -23\end{bmatrix},\,V=\begin{bmatrix}5 & 3 \\ 6 & -4 \\ -1 & -8\end{bmatrix},\,N=\begin{bmatrix}1 & -7 \\ 2 & -6 \\ 3 & 5\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}4 & 10 \\ -4 & -13 \\ 4 & 2\end{bmatrix}$
- $\begin{bmatrix}10 & -1 \\ 3 & 25 \\ -57 & -23\end{bmatrix}$
- $\begin{bmatrix}6 & -4 \\ 8 & -10 \\ -4 & -3\end{bmatrix}$
- $\begin{bmatrix}4 & 10 \\ 4 & 2 \\ -4 & -13\end{bmatrix}$ (correct)
- $\begin{bmatrix}4 & 10 \\ 2 & 4 \\ -4 & -13\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}C+V-(N+C) & =C+V-N-C \\  & =\cancel{C}+V-N-\cancel{C} \\  & =V-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}V-N & =\begin{bmatrix}5 & 3 \\ 6 & -4 \\ -1 & -8\end{bmatrix}-\begin{bmatrix}1 & -7 \\ 2 & -6 \\ 3 & 5\end{bmatrix} \\  & =\begin{bmatrix}5-1 & 3-(-7) \\ 6-2 & -4-(-6) \\ -1-3 & -8-5\end{bmatrix} \\  & =\begin{bmatrix}4 & 10 \\ 4 & 2 \\ -4 & -13\end{bmatrix}\end{aligned}
$$

## Authored method bank at original parameters

Find $C+V-(N+C)$, if

$$
C=\begin{bmatrix}10 & -1 \\ 3 & 25 \\ -57 & -23\end{bmatrix},\,V=\begin{bmatrix}5 & 3 \\ 6 & -4 \\ -1 & -8\end{bmatrix},\,N=\begin{bmatrix}1 & -7 \\ 2 & -6 \\ 3 & 5\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-4 & -10 \\ -4 & -2 \\ 4 & 13\end{bmatrix}$
- $\begin{bmatrix}4 & 10 \\ 4 & 2 \\ -4 & -13\end{bmatrix}$ (correct)
- $\begin{bmatrix}14 & 9 \\ 7 & 27 \\ -61 & -36\end{bmatrix}$
- $\begin{bmatrix}-6 & 11 \\ 1 & -23 \\ 53 & 10\end{bmatrix}$
- $\begin{bmatrix}6 & -4 \\ 8 & -10 \\ 2 & -3\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}C+V-(N+C) & =C+V-N-C \\  & =\cancel{C}+V-N-\cancel{C} \\  & =V-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}V-N & =\begin{bmatrix}5 & 3 \\ 6 & -4 \\ -1 & -8\end{bmatrix}-\begin{bmatrix}1 & -7 \\ 2 & -6 \\ 3 & 5\end{bmatrix} \\  & =\begin{bmatrix}5-1 & 3-(-7) \\ 6-2 & -4-(-6) \\ -1-3 & -8-5\end{bmatrix} \\  & =\begin{bmatrix}4 & 10 \\ 4 & 2 \\ -4 & -13\end{bmatrix}\end{aligned}
$$

## Generated q-13535 / easy

Find $Q + R - (Q + P)$, if

$P = \begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix}, Q = \begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix}, R = \begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}$.

selection:
- $\begin{bmatrix}1 & 4 \\ 5 & 3\end{bmatrix}$ (correct)
- $\begin{bmatrix}-1 & -4 \\ -5 & -3\end{bmatrix}$
- $\begin{bmatrix}7 & -2 \\ 11 & -4\end{bmatrix}$
- $\begin{bmatrix}-5 & 10 \\ -1 & 10\end{bmatrix}$
- $\begin{bmatrix}-11 & -2 \\ 9 & -9\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}Q + R - (Q + P) & =Q+R-Q-P \\  & =\cancel{Q}+R-\cancel{Q}-P \\  & =R-P\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}R-P & =\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}-\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix} \\  & =\begin{bmatrix}-5-(-6) & 1-(-3) \\ 7-2 & -3-(-6)\end{bmatrix} \\  & =\begin{bmatrix}1 & 4 \\ 5 & 3\end{bmatrix}\end{aligned}
$$

## Generated q-13535 / easy

Find $Q + R - (Q + P)$, if

$P = \begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix}, Q = \begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix}, R = \begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}$.

selection:
- $\begin{bmatrix}2 & -5 \\ 1 & -1\end{bmatrix}$
- $\begin{bmatrix}12 & -9 \\ 11 & -17\end{bmatrix}$
- $\begin{bmatrix}-9 & -1 \\ -2 & -9\end{bmatrix}$
- $\begin{bmatrix}-7 & 7 \\ -6 & 9\end{bmatrix}$
- $\begin{bmatrix}7 & -7 \\ 6 & -9\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}Q + R - (Q + P) & =Q+R-Q-P \\  & =\cancel{Q}+R-\cancel{Q}-P \\  & =R-P\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}R-P & =\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}-\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix} \\  & =\begin{bmatrix}-1-(-8) & -4-3 \\ 2-(-4) & -9-0\end{bmatrix} \\  & =\begin{bmatrix}7 & -7 \\ 6 & -9\end{bmatrix}\end{aligned}
$$

## Generated q-13550 / easy

Find $K+L-(K+J)$, if

$$
J=\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix},\,K=\begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix},\,L=\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}1 & 4 \\ 5 & 3\end{bmatrix}$ (correct)
- $\begin{bmatrix}-1 & -4 \\ -5 & -3\end{bmatrix}$
- $\begin{bmatrix}7 & -2 \\ 11 & -4\end{bmatrix}$
- $\begin{bmatrix}-5 & 10 \\ -1 & 10\end{bmatrix}$
- $\begin{bmatrix}-11 & -2 \\ 9 & -9\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}K+L-(K+J) & =K+L-K-J \\  & =\cancel{K}+L-\cancel{K}-J \\  & =L-J\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}L-J & =\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}-\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix} \\  & =\begin{bmatrix}-5-(-6) & 1-(-3) \\ 7-2 & -3-(-6)\end{bmatrix} \\  & =\begin{bmatrix}1 & 4 \\ 5 & 3\end{bmatrix}\end{aligned}
$$

## Generated q-13550 / easy

Find $K+L-(K+J)$, if

$$
J=\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix},\,K=\begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix},\,L=\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}2 & -5 \\ 1 & -1\end{bmatrix}$
- $\begin{bmatrix}12 & -9 \\ 11 & -17\end{bmatrix}$
- $\begin{bmatrix}-9 & -1 \\ -2 & -9\end{bmatrix}$
- $\begin{bmatrix}-7 & 7 \\ -6 & 9\end{bmatrix}$
- $\begin{bmatrix}7 & -7 \\ 6 & -9\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}K+L-(K+J) & =K+L-K-J \\  & =\cancel{K}+L-\cancel{K}-J \\  & =L-J\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}L-J & =\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}-\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix} \\  & =\begin{bmatrix}-1-(-8) & -4-3 \\ 2-(-4) & -9-0\end{bmatrix} \\  & =\begin{bmatrix}7 & -7 \\ 6 & -9\end{bmatrix}\end{aligned}
$$

## Generated q-13543 / easy

Find $M+O-(N+M)$, if

$$
M=\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix},\,N=\begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix},\,O=\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-11 & 7 \\ 1 & 4\end{bmatrix}$ (correct)
- $\begin{bmatrix}11 & -7 \\ -1 & -4\end{bmatrix}$
- $\begin{bmatrix}-17 & 4 \\ 3 & -2\end{bmatrix}$
- $\begin{bmatrix}-5 & 10 \\ -1 & 10\end{bmatrix}$
- $\begin{bmatrix}1 & -5 \\ 13 & -10\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}M+O-(N+M) & =M+O-N-M \\  & =\cancel{M}+O-N-\cancel{M} \\  & =O-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}O-N & =\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}-\begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix} \\  & =\begin{bmatrix}-5-6 & 1-(-6) \\ 7-6 & -3-(-7)\end{bmatrix} \\  & =\begin{bmatrix}-11 & 7 \\ 1 & 4\end{bmatrix}\end{aligned}
$$

## Generated q-13543 / easy

Find $M+O-(N+M)$, if

$$
M=\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix},\,N=\begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix},\,O=\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}2 & -5 \\ 1 & -1\end{bmatrix}$
- $\begin{bmatrix}-14 & 1 \\ -7 & -1\end{bmatrix}$
- $\begin{bmatrix}4 & -6 \\ 7 & -17\end{bmatrix}$
- $\begin{bmatrix}6 & 2 \\ 3 & 1\end{bmatrix}$
- $\begin{bmatrix}-6 & -2 \\ -3 & -1\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}M+O-(N+M) & =M+O-N-M \\  & =\cancel{M}+O-N-\cancel{M} \\  & =O-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}O-N & =\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}-\begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix} \\  & =\begin{bmatrix}-1-5 & -4-(-2) \\ 2-5 & -9-(-8)\end{bmatrix} \\  & =\begin{bmatrix}-6 & -2 \\ -3 & -1\end{bmatrix}\end{aligned}
$$

## Generated q-279581 / easy

Find $A+B-(C+B)$, if

$$
A=\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix},\,B=\begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix},\,C=\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}.
$$

| $A+B-(C+B)=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

field-1:
- $-1$ (correct)

field-2:
- $-4$ (correct)

field-3:
- $-5$ (correct)

field-4:
- $-3$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}A+B-(C+B) & =A+B-C-B \\  & =A+\cancel{B}-C-\cancel{B} \\  & =A-C\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-C & =\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix}-\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix} \\  & =\begin{bmatrix}-6-(-5) & -3-1 \\ 2-7 & -6-(-3)\end{bmatrix} \\  & =\begin{bmatrix}-1 & -4 \\ -5 & -3\end{bmatrix}\end{aligned}
$$

## Generated q-279581 / easy

Find $A+B-(C+B)$, if

$$
A=\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix},\,B=\begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix},\,C=\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}.
$$

| $A+B-(C+B)=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

field-1:
- $-7$ (correct)

field-2:
- $7$ (correct)

field-3:
- $-6$ (correct)

field-4:
- $9$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}A+B-(C+B) & =A+B-C-B \\  & =A+\cancel{B}-C-\cancel{B} \\  & =A-C\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-C & =\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix}-\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix} \\  & =\begin{bmatrix}-8-(-1) & 3-(-4) \\ -4-2 & 0-(-9)\end{bmatrix} \\  & =\begin{bmatrix}-7 & 7 \\ -6 & 9\end{bmatrix}\end{aligned}
$$

## Generated q-69623 / easy

Find $G+H-(H+F)$, if

$$
F=\begin{bmatrix}-6 & -3 & 2 \\ -6 & 6 & -6\end{bmatrix},\,G=\begin{bmatrix}6 & -7 & -5 \\ 1 & 7 & -3\end{bmatrix},\,H=\begin{bmatrix}6 & -5 & 0 \\ 9 & 0 & -6\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}12 & -4 & -7 \\ 7 & 1 & 3\end{bmatrix}$ (correct)
- $\begin{bmatrix}-12 & 4 & 7 \\ -7 & -1 & -3\end{bmatrix}$
- $\begin{bmatrix}18 & -9 & -7 \\ 16 & 1 & -3\end{bmatrix}$
- $\begin{bmatrix}6 & 1 & -7 \\ -2 & 1 & 9\end{bmatrix}$
- $\begin{bmatrix}0 & -10 & -3 \\ -5 & 13 & -9\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}G+H-(H+F) & =G+H-H-F \\  & =G+\cancel{H}-\cancel{H}-F \\  & =G-F\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}G-F & =\begin{bmatrix}6 & -7 & -5 \\ 1 & 7 & -3\end{bmatrix}-\begin{bmatrix}-6 & -3 & 2 \\ -6 & 6 & -6\end{bmatrix} \\  & =\begin{bmatrix}6-(-6) & -7-(-3) & -5-2 \\ 1-(-6) & 7-6 & -3-(-6)\end{bmatrix} \\  & =\begin{bmatrix}12 & -4 & -7 \\ 7 & 1 & 3\end{bmatrix}\end{aligned}
$$

## Generated q-69623 / easy

Find $G+H-(H+F)$, if

$$
F=\begin{bmatrix}-8 & 3 & -4 \\ 0 & 5 & -2\end{bmatrix},\,G=\begin{bmatrix}5 & -8 & -1 \\ -4 & 2 & -9\end{bmatrix},\,H=\begin{bmatrix}-2 & 6 & -3 \\ -9 & 1 & -7\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}15 & -17 & 6 \\ 5 & -4 & 0\end{bmatrix}$
- $\begin{bmatrix}11 & -5 & 0 \\ -13 & -2 & -14\end{bmatrix}$
- $\begin{bmatrix}-3 & -5 & -5 \\ -4 & 7 & -11\end{bmatrix}$
- $\begin{bmatrix}-13 & 11 & -3 \\ 4 & 3 & 7\end{bmatrix}$
- $\begin{bmatrix}13 & -11 & 3 \\ -4 & -3 & -7\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}G+H-(H+F) & =G+H-H-F \\  & =G+\cancel{H}-\cancel{H}-F \\  & =G-F\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}G-F & =\begin{bmatrix}5 & -8 & -1 \\ -4 & 2 & -9\end{bmatrix}-\begin{bmatrix}-8 & 3 & -4 \\ 0 & 5 & -2\end{bmatrix} \\  & =\begin{bmatrix}5-(-8) & -8-3 & -1-(-4) \\ -4-0 & 2-5 & -9-(-2)\end{bmatrix} \\  & =\begin{bmatrix}13 & -11 & 3 \\ -4 & -3 & -7\end{bmatrix}\end{aligned}
$$

## Generated q-69627 / easy

Find $C+V-(N+C)$, if

$$
C=\begin{bmatrix}-6 & -3 \\ 2 & -6 \\ 6 & -6\end{bmatrix},\,V=\begin{bmatrix}6 & -7 \\ -5 & 1 \\ 7 & -3\end{bmatrix},\,N=\begin{bmatrix}6 & -5 \\ 0 & 9 \\ 0 & -6\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}0 & -2 \\ -5 & -8 \\ 7 & 3\end{bmatrix}$ (correct)
- $\begin{bmatrix}0 & 2 \\ 5 & 8 \\ -7 & -3\end{bmatrix}$
- $\begin{bmatrix}-6 & -5 \\ -3 & -14 \\ 13 & -3\end{bmatrix}$
- $\begin{bmatrix}6 & 1 \\ -7 & -2 \\ 1 & 9\end{bmatrix}$
- $\begin{bmatrix}12 & -12 \\ -5 & 10 \\ 7 & -9\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}C+V-(N+C) & =C+V-N-C \\  & =\cancel{C}+V-N-\cancel{C} \\  & =V-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}V-N & =\begin{bmatrix}6 & -7 \\ -5 & 1 \\ 7 & -3\end{bmatrix}-\begin{bmatrix}6 & -5 \\ 0 & 9 \\ 0 & -6\end{bmatrix} \\  & =\begin{bmatrix}6-6 & -7-(-5) \\ -5-0 & 1-9 \\ 7-0 & -3-(-6)\end{bmatrix} \\  & =\begin{bmatrix}0 & -2 \\ -5 & -8 \\ 7 & 3\end{bmatrix}\end{aligned}
$$

## Generated q-69627 / easy

Find $C+V-(N+C)$, if

$$
C=\begin{bmatrix}-8 & 3 \\ -4 & 0 \\ 5 & -2\end{bmatrix},\,V=\begin{bmatrix}5 & -8 \\ -1 & -4 \\ 2 & -9\end{bmatrix},\,N=\begin{bmatrix}-2 & 6 \\ -3 & -9 \\ 1 & -7\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}15 & -17 \\ 6 & 5 \\ -4 & 0\end{bmatrix}$
- $\begin{bmatrix}-1 & -11 \\ -2 & 5 \\ 6 & -4\end{bmatrix}$
- $\begin{bmatrix}3 & -2 \\ -4 & -13 \\ 3 & -16\end{bmatrix}$
- $\begin{bmatrix}-7 & 14 \\ -2 & -5 \\ -1 & 2\end{bmatrix}$
- $\begin{bmatrix}7 & -14 \\ 2 & 5 \\ 1 & -2\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}C+V-(N+C) & =C+V-N-C \\  & =\cancel{C}+V-N-\cancel{C} \\  & =V-N\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}V-N & =\begin{bmatrix}5 & -8 \\ -1 & -4 \\ 2 & -9\end{bmatrix}-\begin{bmatrix}-2 & 6 \\ -3 & -9 \\ 1 & -7\end{bmatrix} \\  & =\begin{bmatrix}5-(-2) & -8-6 \\ -1-(-3) & -4-(-9) \\ 2-1 & -9-(-7)\end{bmatrix} \\  & =\begin{bmatrix}7 & -14 \\ 2 & 5 \\ 1 & -2\end{bmatrix}\end{aligned}
$$

## Generated q-13536 / moderate

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix},\,B=\begin{bmatrix}6 & -6 \\ 6 & -7\end{bmatrix},\,C=\begin{bmatrix}-5 & 1 \\ 7 & -3\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix}$ (correct)
- $\begin{bmatrix}6 & -15 \\ 14 & -20\end{bmatrix}$
- $\begin{bmatrix}-12 & 3 \\ -4 & 1\end{bmatrix}$
- $\begin{bmatrix}-1 & -4 \\ -5 & -3\end{bmatrix}$
- $\begin{bmatrix}4 & -5 \\ -12 & 0\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}-6 & -3 \\ 2 & -6\end{bmatrix}\end{aligned}
$$

## Generated q-13536 / moderate

Find $(A+B)-C-(B-C)$, if

$$
A=\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix},\,B=\begin{bmatrix}5 & -2 \\ 5 & -8\end{bmatrix},\,C=\begin{bmatrix}-1 & -4 \\ 2 & -9\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-7 & 7 \\ -6 & 9\end{bmatrix}$
- $\begin{bmatrix}-13 & 5 \\ -9 & 8\end{bmatrix}$
- $\begin{bmatrix}-6 & 11 \\ -8 & 18\end{bmatrix}$
- $\begin{bmatrix}2 & -1 \\ 6 & -16\end{bmatrix}$
- $\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}
$$

We are left with a single matrix. So, the result is 

$$
\begin{aligned}A & =\begin{bmatrix}-8 & 3 \\ -4 & 0\end{bmatrix}\end{aligned}
$$

## Generated authored-hard / hard

Find $(A+B)-C-(B-C+D)$, if

$$
A=\begin{bmatrix}-6 & -3 \\ 2 & -6 \\ 6 & -6\end{bmatrix},\,B=\begin{bmatrix}6 & -7 \\ -5 & 1 \\ 7 & -3\end{bmatrix},\,C=\begin{bmatrix}6 & -5 \\ 0 & 9 \\ 0 & -6\end{bmatrix},\,D=\begin{bmatrix}-4 & 1 \\ -1 & 7 \\ 9 & 6\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-2 & -4 \\ 3 & -13 \\ -3 & -12\end{bmatrix}$ (correct)
- $\begin{bmatrix}2 & 4 \\ -3 & 13 \\ 3 & 12\end{bmatrix}$
- $\begin{bmatrix}4 & -11 \\ -2 & -12 \\ 4 & -15\end{bmatrix}$
- $\begin{bmatrix}-8 & 3 \\ 8 & -14 \\ -10 & -9\end{bmatrix}$
- $\begin{bmatrix}-10 & -2 \\ 1 & 1 \\ 15 & 0\end{bmatrix}$

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C+D) & =A+B-C-B+C-D \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C}-D \\  & =A-D\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-D & =\begin{bmatrix}-6 & -3 \\ 2 & -6 \\ 6 & -6\end{bmatrix}-\begin{bmatrix}-4 & 1 \\ -1 & 7 \\ 9 & 6\end{bmatrix} \\  & =\begin{bmatrix}-6-(-4) & -3-1 \\ 2-(-1) & -6-7 \\ 6-9 & -6-6\end{bmatrix} \\  & =\begin{bmatrix}-2 & -4 \\ 3 & -13 \\ -3 & -12\end{bmatrix}\end{aligned}
$$

## Generated authored-hard / hard

Find $(A+B)-C-(B-C+D)$, if

$$
A=\begin{bmatrix}-8 & 3 \\ -4 & 0 \\ 5 & -2\end{bmatrix},\,B=\begin{bmatrix}5 & -8 \\ -1 & -4 \\ 2 & -9\end{bmatrix},\,C=\begin{bmatrix}-2 & 6 \\ -3 & -9 \\ 1 & -7\end{bmatrix},\,D=\begin{bmatrix}9 & 1 \\ -4 & -1 \\ -9 & -6\end{bmatrix}.
$$

selection:
- $\begin{bmatrix}-22 & 10 \\ 1 & 5 \\ 12 & 13\end{bmatrix}$
- $\begin{bmatrix}-12 & -6 \\ -1 & -3 \\ 16 & -5\end{bmatrix}$
- $\begin{bmatrix}1 & 4 \\ -8 & -1 \\ -4 & -8\end{bmatrix}$
- $\begin{bmatrix}17 & -2 \\ 0 & -1 \\ -14 & -4\end{bmatrix}$
- $\begin{bmatrix}-17 & 2 \\ 0 & 1 \\ 14 & 4\end{bmatrix}$ (correct)

First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:

$$
\begin{aligned}(A+B)-C-(B-C+D) & =A+B-C-B+C-D \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C}-D \\  & =A-D\end{aligned}
$$

We are left with a single subtraction. So, we subtract the corresponding entries of the two matrices:

$$
\begin{aligned}A-D & =\begin{bmatrix}-8 & 3 \\ -4 & 0 \\ 5 & -2\end{bmatrix}-\begin{bmatrix}9 & 1 \\ -4 & -1 \\ -9 & -6\end{bmatrix} \\  & =\begin{bmatrix}-8-9 & 3-1 \\ -4-(-4) & 0-(-1) \\ 5-(-9) & -2-(-6)\end{bmatrix} \\  & =\begin{bmatrix}-17 & 2 \\ 0 & 1 \\ 14 & 4\end{bmatrix}\end{aligned}
$$
