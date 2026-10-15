# Zero-matrix review

All originals retain raw evidence in source-cases.json. q-126201 uses the one documented witness correction; two unrated radio originals receive authored solutions and inferred keys. Moderate/hard variants are uncalibrated same-method placements.

## q-11553 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?
$H = \begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix}, G = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, K = \begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$

- $H$ is a zero matrix since *all* its entries are zeros.

- $G$ is a zero matrix since *all* its entries are zeros.

- $K$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${k}_{11}=1\ne 0$).

Therefore, only $H$ and $G$ are zero matrices.

Field selection (:answer-field.type/radio): ["$H$ only", "$H$ and $K$ only", "$H$, $G$, and $K$", "$K$ only", "$H$ and $G$ only"]; correct: $H$ and $G$ only

## q-7827 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?
$A = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 \\ 0 & 1\end{bmatrix}, C = \begin{bmatrix}10 & 0\end{bmatrix}$

- $A$ is a zero matrix since *all* its entries are zeros.

- $B$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${b}_{22}=1\ne 0$).

- $C$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${c}_{11}=10\ne 0$).

Therefore, only $A$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$A$ and $C$ only", "$B$ only", "$C$ only", "$A$ only", "$A$, $B$, and $C$"]; correct: $A$ only

## q-126201 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?

$$
H=\begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,I=\begin{bmatrix}0 & 0 \\ 0.1 & 0.1 \\ 0 & 0\end{bmatrix},\,G=\begin{bmatrix}0\end{bmatrix}
$$

Select all that apply.

- $H$ is a zero matrix since *all* its entries are zeros.

- $I$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${i}_{21}=0.1\ne 0$).

- $G$ is a zero matrix since *all* its entries are zeros.

Therefore, only $H$ and $G$ are zero matrices.

Field H (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field I (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field G (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-126204 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?

$$
R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,S=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,T=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $R$ is a zero matrix since *all* its entries are zeros.

- $S$ is a zero matrix since *all* its entries are zeros.

- $T$ is a zero matrix since *all* its entries are zeros.

Therefore, $R$, $S$, and $T$ are zero matrices.

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field S (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field T (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68729 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?

$$
T=\begin{bmatrix}0 & 1 \\ 0 & 0\end{bmatrix},\,U=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 1 & 0\end{bmatrix},\,V=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $T$ is *not* a zero matrix since one of its entries is not zero (${t}_{12}=1\ne 0$).

- $U$ is *not* a zero matrix since one of its entries is not zero (${u}_{32}=1\ne 0$).

- $V$ is a zero matrix since *all* its entries are zeros.

Therefore, only $V$ is a zero matrix.

Field T (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field U (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field V (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 1 \\ 1 & 0 \\ 0 & 1\end{bmatrix},\,Q=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $P$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${p}_{21}=1\ne 0$).

- $Q$ is a zero matrix since *all* its entries are zeros.

- $R$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Q$ and $R$ are zero matrices.

Field P (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field R (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68727 — original MA replay; documented repair when present — easy

Which of the following are zero matrices?

$$
W=\begin{bmatrix}0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0\end{bmatrix},\,X=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,Y=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 3 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $W$ is not a zero matrix since some of its entries are not zeros (for instance, ${w}_{22}=1\ne 0$).

- $X$ is a zero matrix since *all* its entries are zeros.

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{33}=3\ne 0$).

Therefore, only $X$ is a zero matrix.

Field W (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field X (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field Y (:answer-field.type/checkbox): ["true", "false"]; correct: false

## e-4390 — canonical restored from original screenshot; authored fields — easy

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,Q=\begin{bmatrix}0 & 0.1 \\ 0.1 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $P$ is a zero matrix since *all* its entries are zeros.

- $Q$ is *not* a zero matrix since some of its entries are not zeros (for instance, $q_{12}=0.1\neq0$).

- $R$ is a zero matrix since *all* its entries are zeros.

Therefore, only $P$ and $R$ are zero matrices.

Field P (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field R (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-11553 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?
$Y = \begin{bmatrix}0 & 0 & 0 & 0\end{bmatrix}, N = \begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}, V = \begin{bmatrix}0 & 3 \\ 0 & 0 \\ 0 & 0 \\ 0.1 & 10\end{bmatrix}$

- $Y$ is a zero matrix since *all* its entries are zeros.

- $N$ is a zero matrix since *all* its entries are zeros.

- $V$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${v}_{41}=0.1\ne 0$).

Therefore, only $Y$ and $N$ are zero matrices.

Field selection (:answer-field.type/radio): ["$Y$ and $N$ only", "$V$ only", "$Y$, $N$, and $V$", "$Y$ only", "$Y$ and $V$ only"]; correct: $Y$ and $N$ only

## q-11553 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?
$O = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0.1 \\ 0 & 3 & 3 & 0\end{bmatrix}$

- $O$ is a zero matrix since *all* its entries are zeros.

- $B$ is a zero matrix since *all* its entries are zeros.

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{14}=0.1\ne 0$).

Therefore, only $O$ and $B$ are zero matrices.

Field selection (:answer-field.type/radio): ["$O$ and $Y$ only", "$O$ only", "$O$, $B$, and $Y$", "$O$ and $B$ only", "$Y$ only"]; correct: $O$ and $B$ only

## q-7827 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?
$Z = \begin{bmatrix}0 \\ 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 3 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}$

- $Z$ is a zero matrix since *all* its entries are zeros.

- $B$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${b}_{41}=3\ne 0$).

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{22}=1\ne 0$).

Therefore, only $Z$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$B$ only", "$Z$ only", "$Z$ and $Y$ only", "$Z$, $B$, and $Y$", "$Y$ only"]; correct: $Z$ only

## q-7827 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?
$S = \begin{bmatrix}0\end{bmatrix}, A = \begin{bmatrix}0 & 1 & 0 & 0 & 0\end{bmatrix}, L = \begin{bmatrix}0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$

- $S$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $L$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${l}_{13}=1\ne 0$).

Therefore, only $S$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$S$ and $L$ only", "$S$ only", "$A$ only", "$L$ only", "$S$, $A$, and $L$"]; correct: $S$ only

## q-126201 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,T=\begin{bmatrix}0 & 10 & 0 \\ 1 & 0 & 0\end{bmatrix},\,N=\begin{bmatrix}0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is a zero matrix since *all* its entries are zeros.

- $T$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${t}_{21}=1\ne 0$).

- $N$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Q$ and $N$ are zero matrices.

Field Q (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field T (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field N (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126201 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}3 & 1 & 0\end{bmatrix},\,Q=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $X$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $Q$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ and $Q$ are zero matrices.

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126204 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,L=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $P$ is a zero matrix since *all* its entries are zeros.

- $R$ is a zero matrix since *all* its entries are zeros.

- $L$ is a zero matrix since *all* its entries are zeros.

Therefore, $P$, $R$, and $L$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field L (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-126204 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,W=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Z$ is a zero matrix since *all* its entries are zeros.

- $W$ is a zero matrix since *all* its entries are zeros.

- $D$ is a zero matrix since *all* its entries are zeros.

Therefore, $Z$, $W$, and $D$ are zero matrices.

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field W (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field D (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68729 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
N=\begin{bmatrix}0 & 0 \\ 1 & 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 0\end{bmatrix},\,X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $N$ is *not* a zero matrix since one of its entries is not zero (${n}_{21}=1\ne 0$).

- $D$ is *not* a zero matrix since one of its entries is not zero (${d}_{21}=1\ne 0$).

- $X$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ is a zero matrix.

Field N (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field D (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68729 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0.1 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}0 & 0 \\ 1 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is *not* a zero matrix since one of its entries is not zero (${q}_{11}=0.1\ne 0$).

- $A$ is *not* a zero matrix since one of its entries is not zero (${a}_{21}=1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ is a zero matrix.

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0.1 \\ 0 & 10 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,M=\begin{bmatrix}0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $P$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${p}_{25}=0.1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

- $M$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ and $M$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field Z (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field M (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
O=\begin{bmatrix}0 & 0 \\ 0 & 10 \\ 0 & 0.1 \\ 0 & 1\end{bmatrix},\,A=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $O$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${o}_{42}=1\ne 0$).

- $A$ is a zero matrix since *all* its entries are zeros.

- $C$ is a zero matrix since *all* its entries are zeros.

Therefore, only $A$ and $C$ are zero matrices.

Field O (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field A (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field C (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68727 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
L=\begin{bmatrix}1 \\ 0.1 \\ 3 \\ 0.1\end{bmatrix},\,B=\begin{bmatrix}0 \\ 0 \\ 0 \\ 0\end{bmatrix},\,H=\begin{bmatrix}1 \\ 1 \\ 3\end{bmatrix}
$$

Select all that apply.

- $L$ is not a zero matrix since some of its entries are not zeros (for instance, ${l}_{21}=0.1\ne 0$).

- $B$ is a zero matrix since *all* its entries are zeros.

- $H$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${h}_{21}=1\ne 0$).

Therefore, only $B$ is a zero matrix.

Field L (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field B (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field H (:answer-field.type/checkbox): ["true", "false"]; correct: false

## q-68727 — authored same-method variant; source-observed easy family or unrated placement — easy

Which of the following are zero matrices?

$$
U=\begin{bmatrix}1 & 0.1 \\ 0.1 & 10\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}10 & 0 & 0.1 \\ 0 & 0 & 0 \\ 0 & 0.1 & 0\end{bmatrix}
$$

Select all that apply.

- $U$ is not a zero matrix since some of its entries are not zeros (for instance, ${u}_{22}=10\ne 0$).

- $R$ is a zero matrix since *all* its entries are zeros.

- $C$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${c}_{11}=10\ne 0$).

Therefore, only $R$ is a zero matrix.

Field U (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field C (:answer-field.type/checkbox): ["true", "false"]; correct: false

## q-11553 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?
$Y = \begin{bmatrix}0 & 0 & 0 & 0\end{bmatrix}, N = \begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}, V = \begin{bmatrix}0 & 3 \\ 0 & 0 \\ 0 & 0 \\ 0.1 & 10\end{bmatrix}$

- $Y$ is a zero matrix since *all* its entries are zeros.

- $N$ is a zero matrix since *all* its entries are zeros.

- $V$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${v}_{41}=0.1\ne 0$).

Therefore, only $Y$ and $N$ are zero matrices.

Field selection (:answer-field.type/radio): ["$Y$ and $N$ only", "$V$ only", "$Y$, $N$, and $V$", "$Y$ only", "$Y$ and $V$ only"]; correct: $Y$ and $N$ only

## q-11553 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?
$O = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0.1 \\ 0 & 3 & 3 & 0\end{bmatrix}$

- $O$ is a zero matrix since *all* its entries are zeros.

- $B$ is a zero matrix since *all* its entries are zeros.

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{14}=0.1\ne 0$).

Therefore, only $O$ and $B$ are zero matrices.

Field selection (:answer-field.type/radio): ["$O$ and $Y$ only", "$O$ only", "$O$, $B$, and $Y$", "$O$ and $B$ only", "$Y$ only"]; correct: $O$ and $B$ only

## q-7827 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?
$Z = \begin{bmatrix}0 \\ 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 3 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}$

- $Z$ is a zero matrix since *all* its entries are zeros.

- $B$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${b}_{41}=3\ne 0$).

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{22}=1\ne 0$).

Therefore, only $Z$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$B$ only", "$Z$ only", "$Z$ and $Y$ only", "$Z$, $B$, and $Y$", "$Y$ only"]; correct: $Z$ only

## q-7827 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?
$S = \begin{bmatrix}0\end{bmatrix}, A = \begin{bmatrix}0 & 1 & 0 & 0 & 0\end{bmatrix}, L = \begin{bmatrix}0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$

- $S$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $L$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${l}_{13}=1\ne 0$).

Therefore, only $S$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$S$ and $L$ only", "$S$ only", "$A$ only", "$L$ only", "$S$, $A$, and $L$"]; correct: $S$ only

## q-126201 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,T=\begin{bmatrix}0 & 10 & 0 \\ 1 & 0 & 0\end{bmatrix},\,N=\begin{bmatrix}0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is a zero matrix since *all* its entries are zeros.

- $T$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${t}_{21}=1\ne 0$).

- $N$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Q$ and $N$ are zero matrices.

Field Q (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field T (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field N (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126201 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}3 & 1 & 0\end{bmatrix},\,Q=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $X$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $Q$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ and $Q$ are zero matrices.

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126204 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,L=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $P$ is a zero matrix since *all* its entries are zeros.

- $R$ is a zero matrix since *all* its entries are zeros.

- $L$ is a zero matrix since *all* its entries are zeros.

Therefore, $P$, $R$, and $L$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field L (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-126204 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,W=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Z$ is a zero matrix since *all* its entries are zeros.

- $W$ is a zero matrix since *all* its entries are zeros.

- $D$ is a zero matrix since *all* its entries are zeros.

Therefore, $Z$, $W$, and $D$ are zero matrices.

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field W (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field D (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68729 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
N=\begin{bmatrix}0 & 0 \\ 1 & 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 0\end{bmatrix},\,X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $N$ is *not* a zero matrix since one of its entries is not zero (${n}_{21}=1\ne 0$).

- $D$ is *not* a zero matrix since one of its entries is not zero (${d}_{21}=1\ne 0$).

- $X$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ is a zero matrix.

Field N (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field D (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68729 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0.1 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}0 & 0 \\ 1 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is *not* a zero matrix since one of its entries is not zero (${q}_{11}=0.1\ne 0$).

- $A$ is *not* a zero matrix since one of its entries is not zero (${a}_{21}=1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ is a zero matrix.

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0.1 \\ 0 & 10 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,M=\begin{bmatrix}0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $P$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${p}_{25}=0.1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

- $M$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ and $M$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field Z (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field M (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
O=\begin{bmatrix}0 & 0 \\ 0 & 10 \\ 0 & 0.1 \\ 0 & 1\end{bmatrix},\,A=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $O$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${o}_{42}=1\ne 0$).

- $A$ is a zero matrix since *all* its entries are zeros.

- $C$ is a zero matrix since *all* its entries are zeros.

Therefore, only $A$ and $C$ are zero matrices.

Field O (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field A (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field C (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68727 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
L=\begin{bmatrix}1 \\ 0.1 \\ 3 \\ 0.1\end{bmatrix},\,B=\begin{bmatrix}0 \\ 0 \\ 0 \\ 0\end{bmatrix},\,H=\begin{bmatrix}1 \\ 1 \\ 3\end{bmatrix}
$$

Select all that apply.

- $L$ is not a zero matrix since some of its entries are not zeros (for instance, ${l}_{21}=0.1\ne 0$).

- $B$ is a zero matrix since *all* its entries are zeros.

- $H$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${h}_{21}=1\ne 0$).

Therefore, only $B$ is a zero matrix.

Field L (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field B (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field H (:answer-field.type/checkbox): ["true", "false"]; correct: false

## q-68727 — authored same-method variant; uncalibrated moderate — moderate

Which of the following are zero matrices?

$$
U=\begin{bmatrix}1 & 0.1 \\ 0.1 & 10\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}10 & 0 & 0.1 \\ 0 & 0 & 0 \\ 0 & 0.1 & 0\end{bmatrix}
$$

Select all that apply.

- $U$ is not a zero matrix since some of its entries are not zeros (for instance, ${u}_{22}=10\ne 0$).

- $R$ is a zero matrix since *all* its entries are zeros.

- $C$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${c}_{11}=10\ne 0$).

Therefore, only $R$ is a zero matrix.

Field U (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field C (:answer-field.type/checkbox): ["true", "false"]; correct: false

## q-11553 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?
$Y = \begin{bmatrix}0 & 0 & 0 & 0\end{bmatrix}, N = \begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}, V = \begin{bmatrix}0 & 3 \\ 0 & 0 \\ 0 & 0 \\ 0.1 & 10\end{bmatrix}$

- $Y$ is a zero matrix since *all* its entries are zeros.

- $N$ is a zero matrix since *all* its entries are zeros.

- $V$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${v}_{41}=0.1\ne 0$).

Therefore, only $Y$ and $N$ are zero matrices.

Field selection (:answer-field.type/radio): ["$Y$ and $N$ only", "$V$ only", "$Y$, $N$, and $V$", "$Y$ only", "$Y$ and $V$ only"]; correct: $Y$ and $N$ only

## q-11553 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?
$O = \begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0.1 \\ 0 & 3 & 3 & 0\end{bmatrix}$

- $O$ is a zero matrix since *all* its entries are zeros.

- $B$ is a zero matrix since *all* its entries are zeros.

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{14}=0.1\ne 0$).

Therefore, only $O$ and $B$ are zero matrices.

Field selection (:answer-field.type/radio): ["$O$ and $Y$ only", "$O$ only", "$O$, $B$, and $Y$", "$O$ and $B$ only", "$Y$ only"]; correct: $O$ and $B$ only

## q-7827 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?
$Z = \begin{bmatrix}0 \\ 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 3 & 0\end{bmatrix}, Y = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}$

- $Z$ is a zero matrix since *all* its entries are zeros.

- $B$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${b}_{41}=3\ne 0$).

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{22}=1\ne 0$).

Therefore, only $Z$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$B$ only", "$Z$ only", "$Z$ and $Y$ only", "$Z$, $B$, and $Y$", "$Y$ only"]; correct: $Z$ only

## q-7827 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?
$S = \begin{bmatrix}0\end{bmatrix}, A = \begin{bmatrix}0 & 1 & 0 & 0 & 0\end{bmatrix}, L = \begin{bmatrix}0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$

- $S$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $L$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${l}_{13}=1\ne 0$).

Therefore, only $S$ is a zero matrix.

Field selection (:answer-field.type/radio): ["$S$ and $L$ only", "$S$ only", "$A$ only", "$L$ only", "$S$, $A$, and $L$"]; correct: $S$ only

## q-126201 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,T=\begin{bmatrix}0 & 10 & 0 \\ 1 & 0 & 0\end{bmatrix},\,N=\begin{bmatrix}0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is a zero matrix since *all* its entries are zeros.

- $T$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${t}_{21}=1\ne 0$).

- $N$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Q$ and $N$ are zero matrices.

Field Q (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field T (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field N (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126201 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}3 & 1 & 0\end{bmatrix},\,Q=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $X$ is a zero matrix since *all* its entries are zeros.

- $A$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${a}_{12}=1\ne 0$).

- $Q$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ and $Q$ are zero matrices.

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-126204 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,L=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $P$ is a zero matrix since *all* its entries are zeros.

- $R$ is a zero matrix since *all* its entries are zeros.

- $L$ is a zero matrix since *all* its entries are zeros.

Therefore, $P$, $R$, and $L$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field L (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-126204 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,W=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Z$ is a zero matrix since *all* its entries are zeros.

- $W$ is a zero matrix since *all* its entries are zeros.

- $D$ is a zero matrix since *all* its entries are zeros.

Therefore, $Z$, $W$, and $D$ are zero matrices.

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field W (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field D (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68729 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
N=\begin{bmatrix}0 & 0 \\ 1 & 0\end{bmatrix},\,D=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 0\end{bmatrix},\,X=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $N$ is *not* a zero matrix since one of its entries is not zero (${n}_{21}=1\ne 0$).

- $D$ is *not* a zero matrix since one of its entries is not zero (${d}_{21}=1\ne 0$).

- $X$ is a zero matrix since *all* its entries are zeros.

Therefore, only $X$ is a zero matrix.

Field N (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field D (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field X (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68729 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
Q=\begin{bmatrix}0.1 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,A=\begin{bmatrix}0 & 0 \\ 1 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $Q$ is *not* a zero matrix since one of its entries is not zero (${q}_{11}=0.1\ne 0$).

- $A$ is *not* a zero matrix since one of its entries is not zero (${a}_{21}=1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ is a zero matrix.

Field Q (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field A (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field Z (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0.1 \\ 0 & 10 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0\end{bmatrix},\,Z=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,M=\begin{bmatrix}0 \\ 0\end{bmatrix}
$$

Select all that apply.

- $P$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${p}_{25}=0.1\ne 0$).

- $Z$ is a zero matrix since *all* its entries are zeros.

- $M$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Z$ and $M$ are zero matrices.

Field P (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field Z (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field M (:answer-field.type/checkbox): ["true", "false"]; correct: true

## q-68725 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
O=\begin{bmatrix}0 & 0 \\ 0 & 10 \\ 0 & 0.1 \\ 0 & 1\end{bmatrix},\,A=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

- $O$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${o}_{42}=1\ne 0$).

- $A$ is a zero matrix since *all* its entries are zeros.

- $C$ is a zero matrix since *all* its entries are zeros.

Therefore, only $A$ and $C$ are zero matrices.

Field O (:answer-field.type/checkbox): ["true", "false"]; correct: false

Field A (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field C (:answer-field.type/checkbox): ["false", "true"]; correct: true

## q-68727 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
L=\begin{bmatrix}1 \\ 0.1 \\ 3 \\ 0.1\end{bmatrix},\,B=\begin{bmatrix}0 \\ 0 \\ 0 \\ 0\end{bmatrix},\,H=\begin{bmatrix}1 \\ 1 \\ 3\end{bmatrix}
$$

Select all that apply.

- $L$ is not a zero matrix since some of its entries are not zeros (for instance, ${l}_{21}=0.1\ne 0$).

- $B$ is a zero matrix since *all* its entries are zeros.

- $H$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${h}_{21}=1\ne 0$).

Therefore, only $B$ is a zero matrix.

Field L (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field B (:answer-field.type/checkbox): ["true", "false"]; correct: true

Field H (:answer-field.type/checkbox): ["true", "false"]; correct: false

## q-68727 — authored same-method variant; uncalibrated hard — hard

Which of the following are zero matrices?

$$
U=\begin{bmatrix}1 & 0.1 \\ 0.1 & 10\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}10 & 0 & 0.1 \\ 0 & 0 & 0 \\ 0 & 0.1 & 0\end{bmatrix}
$$

Select all that apply.

- $U$ is not a zero matrix since some of its entries are not zeros (for instance, ${u}_{22}=10\ne 0$).

- $R$ is a zero matrix since *all* its entries are zeros.

- $C$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${c}_{11}=10\ne 0$).

Therefore, only $R$ is a zero matrix.

Field U (:answer-field.type/checkbox): ["false", "true"]; correct: false

Field R (:answer-field.type/checkbox): ["false", "true"]; correct: true

Field C (:answer-field.type/checkbox): ["true", "false"]; correct: false
