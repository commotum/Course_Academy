# 17592186048337 Subspaces of N-Dimensional Space: Geometric Interpretation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186193876 — Introduction

Recall that a nonempty subset $H\subseteq \mathbb R^n$ is a **subspace** of $\mathbb{R}^n$ if and only if it satisfies the following properties:

- *Closure under vector addition:* 

$\qquad$ If $\mathbf{u}$ and $\mathbf{v}$ are in $H,$ then their sum $\mathbf{u}+\mathbf{v}$ is also in $H.$

- *Closure under scalar multiplication:* 

$\qquad$ If $\mathbf{u}$ is in $H,$ then $c\cdot \mathbf{u}$ is also in $H$ for any scalar number $c.$

In the vector space $\mathbb{R}^n,$ there are two **trivial subspaces**.

- One trivial subspace is the set 

$$
H=\{\mathbf{0}\}
$$

 consisting of just the zero vector. This is a subspace because the sum of two zero vectors is the zero vector, and any multiple of the zero vector is the zero vector.

- Another trivial subspace is the set 

$$
H = \mathbb{R}^n
$$

 consisting of the entire set $\mathbb{R}^n.$ This is a subspace because the sum of two vectors in $\mathbb{R}^n$ is in $\mathbb{R}^n,$ and any multiple of a vector in $\mathbb{R}^n$ is in $\mathbb{R}^n.$



### tutorial 17592186193877 — Non-Trivial Subspaces in Two-Dimensional Space

In $\mathbb{R}^2,$ we have the following theorem:

*The only non-trivial subspaces in $\mathbb{R}^2$ are straight lines that pass through the origin.*

For example, the diagram below shows a subspace in $\mathbb{R}^2.$

![](images/3c/3c0ea9584ae3229a7930c6ef2b53031770a7190b980b5b595cc233cae29ea49d.png)

Let's now consider a few examples of subsets of $\mathbb{R}^2$ that are *not* subspaces of $\mathbb{R}^2$.

![](images/5a/5aac9808e9196653ee54974b495443a95d8913cd0b220a6893acb68ff3b967bb.png)

- Diagram I shows a line that does not pass through the origin. It is *not* a subspace because $\mathbf v$ belongs to the set while $2\mathbf v$ does not. So the set is not closed under scalar multiplication.

- Diagram II is not a subspace because $\mathbf u$ and $\mathbf v$ belong to the set while $\mathbf u+\mathbf v$ does not. So the set is not closed under vector addition.

- Diagram III is not a subspace because $\mathbf v$ belongs to the set while $-\mathbf v$ does not. So the set is not closed under scalar multiplication.



### example 17592186192504 — Identifying Whether Sets Represented Graphically Are Subspaces in Two-Dimensional Space

![](images/72/72329ee334988361174013e7df57452851cd826acf2ffc8b4cead6d750683e73.png)

Which of the diagrams shown above represent subspaces of $\mathbb{R}^2?$

Let's analyze each diagram in turn.

- Diagram I represents the whole plane $\mathbb{R}^2$ without the origin. But every subspace must contain the origin. Therefore, it is *not* a subspace of $\mathbb{R}^2.$

- Diagram II is a line that passes through the origin. Therefore, it is a subspace of $\mathbb{R}^2.$

- Diagram III is a parabola that does not pass through the origin. But every subspace must contain the origin. Therefore, it is *not* a subspace of $\mathbb{R}^2.$

In conclusion, the correct answer is "II only."

### tutorial 17592186193878 — Non-Trivial Subspaces in Three-Dimensional Space

In $\mathbb{R}^3,$ we have the following theorem:

*The only non-trivial subspaces in $\mathbb{R}^3$ are straight lines or planes that pass through the origin.*

For example, the diagram below shows two subspaces in $\mathbb{R}^3.$

![](images/57/57b6625b607537d1c90e849d6ee6ac8480648aa4ad6e3a357bedc8d8408256ad.png)

On the other hand, the sets shown in the diagrams below are *not* subspaces in $\mathbb{R}^3.$

![](images/f4/f4fbaee302e1c25e740f4164841a674243a43197b0f20ddb35d2d41bb4175b68.png)

- Diagram I shows a plane that does not pass through the origin. It is not a subspace because $\mathbf v$ belongs to the set while $2\mathbf v$ does not. So, the set is not closed under scalar multiplication.

- Diagram II shows a line that does not pass through the origin. It is not a subspace because $\mathbf v$ belongs to the set while $2\mathbf v$ does not. So, the set is not closed under scalar multiplication.



### example 17592186192506 — Identifying Whether Sets Represented Graphically Are Subspaces in Three-Dimensional Space

![](images/c6/c66cdc8bbddfb00ce69f843b1ce1d12116b2dd82312a34abafa0fb13907110cf.png)

Which of the diagrams shown above represent subspaces of $\mathbb{R}^3?$

Let's analyze each diagram in turn.

- Diagram I  represents a plane that passes through the origin. Therefore, it is a subspace of  $\mathbb{R}^3.$

- Diagram II  represents a line that passes through the origin. Therefore, it is also a subspace of  $\mathbb{R}^3.$

- Diagram III does not represent a subspace. The origin $\mathbf{0}={\left[ \begin{array}{c}0 \\ 0 \\ 0\end{array} \right]}$  clearly lies outside the subset.

So, the correct answer is "I and II only."

### example 17592186192505 — Identifying Whether Sets Represented Using Set Notation Are Subspaces

Consider the subsets $\; \begin{gathered}A=\left\{\begin{gathered} \langle x, y, z \rangle \in \mathbb{R}^3 :\\ x^2=y \end{gathered}\right\}\end{gathered}\;$ and $\; \begin{gathered}B=\\\left\{\begin{gathered} \langle 3-t, -3+t, -6+2t \rangle :\\ t \in \mathbb{R} \end{gathered}\right\}\end{gathered}.\;$ Which of them is a subspace of $\mathbb{R}^3?$

Let's analyze each of the subsets.

- The set $A$ is not a subspace because it is not closed under scalar multiplication. For example, the vector $\mathbf{a}={\left[ \begin{array}{c}1 \\ 1 \\ 0\end{array} \right]}$ belongs to $A,$ but the vector $2\cdot \mathbf{a}={\left[ \begin{array}{c}2 \\ 2 \\ 0\end{array} \right]}$ does not lie in $A$ (because it does not satisfy $x^2=y$).

- The set $B$ represents a line, and a line is a subspace if and only if it passes through the origin. If the origin belongs to this subset, we would have
$$
{\left[ \begin{array}{c}3 - t \\ - 3 + t \\ - 6 + 2 t\end{array} \right]}=
{\left[ \begin{array}{c}0 \\ 0 \\ 0\end{array} \right]},
$$
which gives us

$$
\left\{\begin{aligned}3-t &=0 \\ -3+t &=0 \\ -6+2t &=0.\end{aligned}\right.
$$

We see that $t=3$ is the solution to the three equations. So, if we choose $t=3,$ then we find that $\mathbf{0} \in B.$ Therefore, $B$ is a subspace of $\mathbb{R}^3.$

In conclusion, the correct answer is "$B$ only".

### tutorial 17592186193879 — Final Notes About the Set of Real Numbers

Lastly, consider the set $\mathbb{R},$ which belongs to the family of vector spaces $\mathbb{R}^n$ (when $n=1$). This vector space has only two subspaces, both of which are trivial:

- the zero subspace $\{0\},$ which contains only the number $0,$ and

- the whole space $\mathbb{R}$ (or, formally, $\mathbb{R}^1$), which contains all the real numbers.



## Representative practice (first three per skill; full bank in practice.json)

### Identifying Whether Sets Represented Graphically Are Subspaces in Two-Dimensional Space (12 captured questions)

Question 17592186193312 — question.difficulty/easy

Which of the diagrams shown below represent subspaces of ${\mathbb{R}}^{2}?$

Select all that apply.

Solution: Let's analyze each diagram in turn.

- Diagram I does not represent a subspace. The vector $\mathbf{a}=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ lies inside given subset. But

$$
(-1)\cdot \mathbf{a}=\begin{bmatrix}1 \\ -1\end{bmatrix}
$$

lies outside the subset.

- Diagram II does not represent a subspace. The vector $\mathbf{a}=\begin{bmatrix}0 \\ 1\end{bmatrix}$ lies inside given subset. But

$$
(-1)\cdot \mathbf{a}=\begin{bmatrix}0 \\ -1\end{bmatrix}
$$

lies outside the subset.

- Diagram III does not represent a subspace since in does not contain the zero-vector.

So, the correct answer is "None".

Answer ![Diagram III](images/f0/f04fb553eed6853549b0aa6c0f03b05e7f69931d8ba1cfaf0cef2486c82820d7.svg): false

Answer ![Diagram II](images/76/7655da5d10b7ace907bd613342d576a691451532aaa7564a9e17c1b41a66097b.svg): false

Answer ![Diagram I](images/e7/e79e96039bc2ebbe1787345b90a84e42e7410c0ef500dfac37844bdc1a10e756.svg): false

Answer None of the above: true

Question 17592186193383 — question.difficulty/easy

![](images/c9/c9b2c979ee7356d3c8b638ad46cef3733d6c0db70965f1deec24413c5bf2136e.png)

Which of the diagrams shown above represent subspaces of ${\mathbb{R}}^{2}?$?

Solution: Analyze each diagram in turn.

- Diagram I is a disk of radius $1$. It is not closed under scalar multiplication: a nonzero vector in the disk can be multiplied by a sufficiently large scalar to leave the disk.
- Diagram II excludes the origin, shown by the open circle. Every subspace contains the origin, so this is not a subspace.
- Diagram III is the shaded half-plane to the left of the $y$-axis. For example, $\langle-1,0\rangle$ lies in it but its negative $\langle1,0\rangle$ does not. It is not closed under scalar multiplication.

The correct answer is **None**.

Answer selection: None

Question 17592186247149 — question.difficulty/easy

Which of the diagrams shown below represent subspaces of ${\mathbb{R}}^{2}?$

Select all that apply.

Solution: Let's analyze each diagram in turn.

- Diagram I does not represent a subspace. The vector $\mathbf{a}=\begin{bmatrix}1 \\ 1\end{bmatrix}$ lies inside the given subset. But 

$$
(-1)\cdot \mathbf{a}=\begin{bmatrix}-1 \\ -1\end{bmatrix}
$$

lies outside the subset.

- Diagram II represents a set that does not contain the origin. But every subspace must contain the origin, so Diagram II is not a subspace of ${\mathbb{R}}^{2}.$

- Diagram III represents the whole plane ${\mathbb{R}}^{2}$ without the origin. But every subspace must contain the origin, so Diagram III is not a subspace of ${\mathbb{R}}^{2}.$

So, the correct answer is "None."

Answer ![Diagram III](images/84/8480765d37746d4157a336140609e46919f93ceba05aaed2c595cca8c1e1ccb0.svg): false

Answer ![Diagram II](images/54/541aa5367d8bb8bd36ea5811579728513153549aa66066d491357f43c5aad11d.svg): false

Answer ![Diagram I](images/43/435ae803182d813230907411b7104b5239d287d294ec69f5d1a0a4112258518a.svg): false

Answer None of the above: true

### Identifying Whether Sets Represented Graphically Are Subspaces in Three-Dimensional Space (12 captured questions)

Question 17592186193319 — question.difficulty/moderate

Which of the diagrams shown below represent subspaces of ${\mathbb{R}}^{2}$ or ${\mathbb{R}}^{3}?$

Select all that apply.

Solution: Let's analyze each diagram in turn.

- Diagram I does not represent a subspace. The origin $\mathbf{0}=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}$ clearly lies outside the subset.

- Diagram II represents the origin $\mathbf{0}=\begin{bmatrix}0 \\ 0\end{bmatrix}\hspace{-0.167em},\hspace{0.167em}$ which is considered a special (trivial) subspace of ${\mathbb{R}}^{2}.$

- Diagram III represents a line that does not pass through the origin. But every subspace must contain the origin, so the line in Diagram III is not a subspace of ${\mathbb{R}}^{3}.$

So, the correct answer is diagram II only

Answer ![Diagram III](images/90/902a485b7c5d2c3fd940b06123ee5316fb74b5e2a2d969b7bf0562fb15cf1a58.svg): false

Answer ![Diagram II](images/cd/cdc289944ccb8df5531321f0cea6f1cd9e81cc7f194ee13d0db078c47471696a.svg): true

Answer ![Diagram I](images/6e/6e8c180b3963c096afadfcfe590f8cff8ee3859438aab883ef08fa18d35ed503.svg): false

Answer None of the above: false

Question 17592186193384 — question.difficulty/moderate

![](images/15/15da2a7bcb642ecc6f5e8d584e89bee3d1002e6f5e31c85b27db0b337553ebbb.png)

Which of the diagrams shown above represent subspaces of ${\mathbb{R}}^{3}?$?

Solution: Analyze each diagram in turn.

- Diagram I is a plane through the origin, so it is a subspace of $\mathbb R^3$.
- Diagram II is a line through the origin, so it is a subspace of $\mathbb R^3$.
- Diagram III is a line that does not pass through the origin. Since every subspace contains the origin, it is not a subspace.

The correct answer is **I and II only**.

Answer selection: I and II only

Question 17592186247121 — question.difficulty/moderate

Which of the diagrams shown below represent subspaces of ${\mathbb{R}}^{2}$ or ${\mathbb{R}}^{3}?$

Select all that apply.

Solution: Let's analyze each diagram in turn.

- Diagram I does not represent a subspace. The origin $\mathbf{0}=\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}$  clearly lies outside the subset.

- Diagram II does not represent a subspace. The origin $\mathbf{0}=\begin{bmatrix}0 \\ 0\end{bmatrix}$  clearly lies outside the subset.

- Diagram III represents a line passing through the origin. Therefore, it is a subspace of  ${\mathbb{R}}^{3}.$

So, the correct answer is diagram III only

Answer ![Diagram III](images/56/56a3b155e245244e60dcb167ea9efb8944ad2b2bac641ec85555df5b2c260e28.svg): true

Answer ![Diagram II](images/b4/b4b3d97fa84dda4d0149738490b0fa4f6454758e399dcdfc83c985c30512c767.svg): false

Answer ![Diagram I](images/6d/6df8dcf7a4343cb8b53273a6dc528f4cea95dcf914200032e3131ca49fa51cad.svg): false

### Identifying Whether Sets Represented Using Set Notation Are Subspaces (17 captured questions)

Question 17592186193313 — question.difficulty/hard

Which of the following sets is a subspace of ${\mathbb{R}}^{3}?$?

1. $\begin{gathered}A=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\x+3y=0\end{gathered}\right\}\end{gathered}$
2. $\begin{gathered}B=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\x=2y+1\end{gathered}\right\}\end{gathered}$
3. $\begin{gathered}C=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\{x}^{2}+{y}^{2}+{z}^{2}\le 0\end{gathered}\right\}\end{gathered}$

Solution: Analyze the three sets in turn.

- $A$ is the solution set of the homogeneous linear equation $x+3y=0$, so it is a plane through the origin and is a subspace.
- $B$ does not contain the zero vector, since $0\ne2(0)+1$. It is not a subspace.
- For real $x,y,z$, each square is nonnegative. Therefore $x^2+y^2+z^2\le0$ holds only for $x=y=z=0$. Thus $C=\{\mathbf0\}$ is the trivial subspace.

The correct answer is **I and III only**.

Answer selection: I and III only

Question 17592186193318 — question.difficulty/moderate

Which of the following sets is a subspace of ${\mathbb{R}}^{2}?$?

1. $\begin{gathered}A=\left\{\begin{gathered}⟨2-t,-4+t⟩\hspace{0.222em}:\\\hspace{0.222em}t\in \mathbb{R}\end{gathered}\right\}\end{gathered}$
2. $\begin{gathered}B=\left\{\begin{gathered}⟨x,y⟩\in {\mathbb{R}}^{2}:\\4x-2y=1\end{gathered}\right\}\end{gathered}$
3. $\begin{gathered}C=\left\{\begin{gathered}⟨x,y⟩\in {\mathbb{R}}^{2}:\\y=0\end{gathered}\right\}\end{gathered}$

Solution: Analyze the three sets in turn.

- For $A$ to contain the origin, both $2-t=0$ and $-4+t=0$ would have to hold. These require $t=2$ and $t=4$, respectively, which is impossible. Thus $A$ is not a subspace.
- $B$ does not contain the origin, since $4(0)-2(0)\ne1$. It is not a subspace.
- $C$ is the $x$-axis, a line through the origin, so it is a subspace.

The correct answer is **III only**.

Answer selection: III only

Question 17592186247150 — question.difficulty/hard

Which of the following sets is a subspace of ${R}^{3}?$

Select all that apply.

Solution: Let's analyze each of the subsets.

- The set $A$ is not a subspace because it does not contain the zero vector. Indeed, $0=⟨0,0,0⟩$ does not satisfy the condition $xyz=1$ since $0\cdot 0\cdot 0\ne 1.$

- The set $B$ is a subspace. It represents a plane, and a plane is a subspace if and only if it passes through the origin. Here, the components of the zero vector $0=⟨0,0,0⟩$ satisfy the equation $x+y-z=0$ since $0+0-0=0.$ So $0$ lies in $B.$

- The set $C$ is not a subspace because it does not contain the zero vector. Indeed, $0=⟨0,0,0⟩$ does not satisfy the condition $y=-1$ since $0\ne -1.$

So, the correct answer is $$
\displaystyle \begin{gathered}B=\left\{\begin{gathered}⟨x,y,z⟩\in {R}^{3}:\\x+y-z=0\end{gathered}\right\}\end{gathered}
$$ only.

Answer $\begin{gathered}A=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\xyz=1\end{gathered}\right\}\end{gathered}$: false

Answer $\begin{gathered}B=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\x+y-z=0\end{gathered}\right\}\end{gathered}$: true

Answer $\begin{gathered}C=\left\{\begin{gathered}⟨x,y,z⟩\in {\mathbb{R}}^{3}:\\y=-1\end{gathered}\right\}\end{gathered}$: false
