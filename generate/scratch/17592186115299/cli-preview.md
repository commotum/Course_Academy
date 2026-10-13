Consider the following system of equations.

$$
\{\begin{aligned}x-3y=-5 \\ -x+3y=6\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is inconsistent
III. The system is consistent dependent

- II only
- I and III only
- I only
- III only
- I and II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & -5 \\ -1 & 3 & 6\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & -5 \\ -1 & 3 & 6\end{aligned}] & {R}_{2}:={R}_{2}+(1){R}_{1} \\ & ∼[\begin{aligned}1 & -3 & -5 \\ 0 & 0 & 1\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=1,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

---

Consider the following system of equations.

$$
\{\begin{aligned}x-y=-3 \\ 2x-2y=-6\end{aligned}
$$

Which of the following statements are true?

I. The system is inconsistent
II. The system is consistent dependent
III. The system is consistent independent

- I and III only
- I and II only
- I only
- III only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -1 & -3 \\ 2 & -2 & -6\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -1 & -3 \\ 2 & -2 & -6\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & -3 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. Here there is one free variable, $y$. Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.

As a result, only statement II is true.

---

Consider the following system of equations

$$
\{\begin{aligned} & -2x-4y=1 \\  & -6x-14y=8 \\  & 4x+8y=-2.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system has no solution
III. The system is consistent dependent

- III only
- I only
- II only
- None
- II and III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}-2 & -4 & 1 \\ -6 & -14 & 8 \\ 4 & 8 & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & -4 & 1 \\ -6 & -14 & 8 \\ 4 & 8 & -2\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}-2 & -4 & 1 \\ 0 & -2 & 5 \\ 4 & 8 & -2\end{aligned}] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼[\begin{aligned}-2 & -4 & 1 \\ 0 & -2 & 5 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
\{\begin{aligned}-2x-4y=1 \\ -2y=5.\end{aligned}
$$

From the second equation we have $y=-\frac{5}{2}$ and substituting this into the first equation yields $x=\frac{9}{2}.$ So,  we conclude that the system is consistent independent. 

As a result, only statement I is true.

---

Consider the following system of equations.

$$
\{\begin{aligned} & -x-2y=7 \\  & 2x+3y=11 \\  & 5x+y=40\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system is inconsistent
- The system has a unique solution

- None
- I only
- II only
- III only
- I and III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & -2 & 7 \\ 2 & 3 & 11 \\ 5 & 1 & 40\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & -2 & 7 \\ 2 & 3 & 11 \\ 5 & 1 & 40\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-1 & -2 & 7 \\ 0 & -1 & 25 \\ 5 & 1 & 40\end{aligned}] & {R}_{3} & :={R}_{3}+5{R}_{1} \\  & ∼[\begin{aligned}-1 & -2 & 7 \\ 0 & -1 & 25 \\ 0 & -9 & 75\end{aligned}] & {R}_{3} & :={R}_{3}+(-9){R}_{2} \\  & ∼[\begin{aligned}-1 & -2 & 7 \\ 0 & -1 & 25 \\ 0 & 0 & -150\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-150,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

---

Consider the following system of equations.

$$
\{\begin{aligned}x-3y-3z=-1 \\ 2x-5y-8z=-4 \\ -2x+4y+10z=4\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is inconsistent
III. The system is consistent dependent

- II only
- I only
- III only
- I and III only
- I and II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & -3 & -1 \\ 2 & -5 & -8 & -4 \\ -2 & 4 & 10 & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & -3 & -1 \\ 2 & -5 & -8 & -4 \\ -2 & 4 & 10 & 4\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & -3 & -3 & -1 \\ 0 & 1 & -2 & -2 \\ -2 & 4 & 10 & 4\end{aligned}] & {R}_{3}:={R}_{3}+(2){R}_{1} \\ & ∼[\begin{aligned}1 & -3 & -3 & -1 \\ 0 & 1 & -2 & -2 \\ 0 & -2 & 4 & 2\end{aligned}] & {R}_{3}:={R}_{3}+(2){R}_{2} \\ & ∼[\begin{aligned}1 & -3 & -3 & -1 \\ 0 & 1 & -2 & -2 \\ 0 & 0 & 0 & -2\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y+0z=-2,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

---

Consider the following system of equations.

$$
\{\begin{aligned}x-y+3z=-3 \\ 2x-y+7z=-6 \\ 2x-4y+4z=-6\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is consistent dependent
III. The system is inconsistent

- I and II only
- I and III only
- I only
- II only
- III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -1 & 3 & -3 \\ 2 & -1 & 7 & -6 \\ 2 & -4 & 4 & -6\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -1 & 3 & -3 \\ 2 & -1 & 7 & -6 \\ 2 & -4 & 4 & -6\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & 3 & -3 \\ 0 & 1 & 1 & 0 \\ 2 & -4 & 4 & -6\end{aligned}] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & 3 & -3 \\ 0 & 1 & 1 & 0 \\ 0 & -2 & -2 & 0\end{aligned}] & {R}_{3}:={R}_{3}+(2){R}_{2} \\ & ∼[\begin{aligned}1 & -1 & 3 & -3 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. Here there is one free variable, $z$. Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.

As a result, only statement II is true.
