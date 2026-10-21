# Originals and generated variants

Basis 1356, immutable source capture. Originals below retain raw source text. Generated variants escape malformed opening system braces; q-32242 also repairs its unstated R1 sign flip. All records use full five-option radio banks.


## q-32242 — original

Consider the following system of equations.

$$
{\begin{aligned} & -x+2y=6 \\  & 2x-3y=13 \\  & 5x-y=45\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system is inconsistent
- The system has a unique solution

Original complete bank: I and III only, III only, None, II only, I only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & 2 & 6 \\ 2 & -3 & 13 \\ 5 & -1 & 45\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & 2 & 6 \\ 2 & -3 & 13 \\ 5 & -1 & 45\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-1 & 2 & 6 \\ 0 & 1 & 25 \\ 5 & -1 & 45\end{aligned}] & {R}_{3} & :={R}_{3}+5{R}_{1} \\  & ∼[\begin{aligned}-1 & 2 & 6 \\ 0 & 1 & 25 \\ 0 & 9 & 75\end{aligned}] & {R}_{3} & :={R}_{3}+(-9){R}_{2} \\  & ∼[\begin{aligned}1 & -2 & -6 \\ 0 & 1 & 25 \\ 0 & 0 & -150\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-150,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & x+4y=9 \\  & -2x-6y=8 \\  & -5x-2y=39\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system is inconsistent
- The system has a unique solution

- None
- I and III only
- I only
- II only
- III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 4 & 9 \\ -2 & -6 & 8 \\ -5 & -2 & 39\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 4 & 9 \\ -2 & -6 & 8 \\ -5 & -2 & 39\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}1 & 4 & 9 \\ 0 & 2 & 26 \\ -5 & -2 & 39\end{aligned}] & {R}_{3} & :={R}_{3}+5{R}_{1} \\  & ∼[\begin{aligned}1 & 4 & 9 \\ 0 & 2 & 26 \\ 0 & 18 & 84\end{aligned}] & {R}_{3} & :={R}_{3}+(-9){R}_{2} \\  & ∼[\begin{aligned}1 & 4 & 9 \\ 0 & 2 & 26 \\ 0 & 0 & -150\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-150,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

## q-42061 — original

Consider the following system of equations.

$$
\{\begin{aligned} & x-3y+z=0 \\  & -4x+6y=2\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent

II. The system has no solution

III. The system is consistent independent

Original complete bank: II only, I and II only, None, I only, III only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & 1 & 0 \\ -4 & 6 & 0 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & 1 & 0 \\ -4 & 6 & 0 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & 1 & 0 \\ 0 & -6 & 4 & 2\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we can to find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement I is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -x-3y+2z=9 \\  & 4x+6y=-18\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent

II. The system has no solution

III. The system is consistent independent

- I and II only
- II only
- III only
- I only
- None

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & -3 & 2 & 9 \\ 4 & 6 & 0 & -18\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & -3 & 2 & 9 \\ 4 & 6 & 0 & -18\end{aligned}] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼[\begin{aligned}-1 & -3 & 2 & 9 \\ 0 & -6 & 8 & 18\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we can to find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement I is true.

## q-131719 — original

Consider the following system of equations.

$$
\{\begin{aligned} & x+4y=-1 \\  & 2x+8y=-2 \\  & -3x-12y=3\end{aligned}
$$

Which of the following statements are true?

I. The system is inconsistent

II. The system is consistent dependent

III. The system has a unique solution

Original complete bank: II only, I only, II and III only, III only, None

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 4 & -1 \\ 2 & 8 & -2 \\ -3 & -12 & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 4 & -1 \\ 2 & 8 & -2 \\ -3 & -12 & 3\end{aligned}] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼[\begin{aligned}1 & 4 & -1 \\ 0 & 0 & 0 \\ -3 & -12 & 3\end{aligned}] & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 4 & -1 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have one free variable, $y.$ That means we can find $x$ in terms of $y.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement II is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -x+4y=-8 \\  & -2x+8y=-16 \\  & 3x-12y=24\end{aligned}
$$

Which of the following statements are true?

I. The system is inconsistent

II. The system is consistent dependent

III. The system has a unique solution

- I only
- II only
- III only
- II and III only
- None

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & 4 & -8 \\ -2 & 8 & -16 \\ 3 & -12 & 24\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & 4 & -8 \\ -2 & 8 & -16 \\ 3 & -12 & 24\end{aligned}] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼[\begin{aligned}-1 & 4 & -8 \\ 0 & 0 & 0 \\ 3 & -12 & 24\end{aligned}] & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼[\begin{aligned}-1 & 4 & -8 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have one free variable, $y.$ That means we can find $x$ in terms of $y.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement II is true.

## q-131723 — original

Consider the following system of equations.

$$
{\begin{aligned} & x-y+z=3 \\  & -3x+3y-3z=10\end{aligned}
$$

Which of the following statements are true?

- The system is inconsistent
- The system has a unique solution
- The system is consistent dependent

Original complete bank: None, II and III only, I only, III only, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -1 & 1 & 3 \\ -3 & 3 & -3 & 10\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -1 & 1 & 3 \\ -3 & 3 & -3 & 10\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & -1 & 1 & 3 \\ 0 & 0 & 0 & 19\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y+0z=19,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement I is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & 2x+y-2z=-2 \\  & -6x-3y+6z=25\end{aligned}
$$

Which of the following statements are true?

- The system is inconsistent
- The system has a unique solution
- The system is consistent dependent

- II and III only
- I only
- None
- II only
- III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 1 & -2 & -2 \\ -6 & -3 & 6 & 25\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 1 & -2 & -2 \\ -6 & -3 & 6 & 25\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}2 & 1 & -2 & -2 \\ 0 & 0 & 0 & 19\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y+0z=19,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement I is true.

## q-131724 — original

Consider the following system of equations.

$$
{\begin{aligned} & x-2y=2 \\  & -3x-4y=3 \\  & 2x-4y=-1\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system has a unique solution
- The system is inconsistent

Original complete bank: I and II only, II only, III only, None, I only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -2 & 2 \\ -3 & -4 & 3 \\ 2 & -4 & -1\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -2 & 2 \\ -3 & -4 & 3 \\ 2 & -4 & -1\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & -2 & 2 \\ 0 & -10 & 9 \\ 2 & -4 & -1\end{aligned}] & {R}_{3} & :={R}_{3}-2{R}_{1} \\  & ∼[\begin{aligned}1 & -2 & 2 \\ 0 & -10 & 9 \\ 0 & 0 & -5\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-5,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -2x+2y=5 \\  & 6x+4y=4 \\  & -4x+4y=5\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system has a unique solution
- The system is inconsistent

- I only
- III only
- None
- I and II only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 2 & 5 \\ 6 & 4 & 4 \\ -4 & 4 & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 2 & 5 \\ 6 & 4 & 4 \\ -4 & 4 & 5\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}-2 & 2 & 5 \\ 0 & 10 & 19 \\ -4 & 4 & 5\end{aligned}] & {R}_{3} & :={R}_{3}-2{R}_{1} \\  & ∼[\begin{aligned}-2 & 2 & 5 \\ 0 & 10 & 19 \\ 0 & 0 & -5\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-5,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

## q-74635 — original

Consider the following system of equations.

$$
{\begin{aligned} & -2x+4y+3z=0 \\  & x+3y=2\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

Original complete bank: II only, I and III only, III only, I and II only, I only

Original worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 4 & 3 & 0 \\ 1 & 3 & 0 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 4 & 3 & 0 \\ 1 & 3 & 0 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+\frac{1}{2}{R}_{1} \\  & ∼[\begin{aligned}-2 & 4 & 3 & 0 \\ 0 & 5 & \frac{3}{2} & 2\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means that  we can find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement III is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -2x-8y-6z=-14 \\  & x-6y=-4\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

- II only
- I and III only
- I and II only
- III only
- I only

Worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & -8 & -6 & -14 \\ 1 & -6 & 0 & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & -8 & -6 & -14 \\ 1 & -6 & 0 & -4\end{aligned}] & {R}_{2} & :={R}_{2}+\frac{1}{2}{R}_{1} \\  & ∼[\begin{aligned}-2 & -8 & -6 & -14 \\ 0 & -10 & -3 & -11\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means that  we can find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement III is true.

## q-74637 — original

Consider the following system of equations

$$
{\begin{aligned} & 2x+3y=-1 \\  & x-2y=1 \\  & -x-5y=2.\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

Original complete bank: I only, II only, I and III only, I and II only, III only

Original worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & 3 & -1 \\ 1 & -2 & 1 \\ -1 & -5 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 3 & -1 \\ 1 & -2 & 1 \\ -1 & -5 & 2\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & -2 & 1 \\ 2 & 3 & -1 \\ -1 & -5 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & -2 & 1 \\ 0 & 7 & -3 \\ -1 & -5 & 2\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼[\begin{aligned}1 & -2 & 1 \\ 0 & 7 & -3 \\ 0 & -7 & 3\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼[\begin{aligned}1 & -2 & 1 \\ 0 & 7 & -3 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
{\begin{aligned}x-2y=1 \\ 7y=-3.\end{aligned}
$$

From the second equation, we get $y=-\frac{3}{7}.$ Substituting this into the first equation, we get

$$
x-2(-\frac{3}{7})=1\,⟹\,x=\frac{1}{7}.
$$

 
So, we conclude that the system is consistent independent. 

As a result, only statement II is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations

$$
\{\begin{aligned} & 4x-6y=-11 \\  & 2x+4y=3 \\  & -2x+10y=14.\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

- I only
- III only
- I and III only
- I and II only
- II only

Worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}4 & -6 & -11 \\ 2 & 4 & 3 \\ -2 & 10 & 14\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}4 & -6 & -11 \\ 2 & 4 & 3 \\ -2 & 10 & 14\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}2 & 4 & 3 \\ 4 & -6 & -11 \\ -2 & 10 & 14\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}2 & 4 & 3 \\ 0 & -14 & -17 \\ -2 & 10 & 14\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼[\begin{aligned}2 & 4 & 3 \\ 0 & -14 & -17 \\ 0 & 14 & 17\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼[\begin{aligned}2 & 4 & 3 \\ 0 & -14 & -17 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
\{\begin{aligned}2x+4y=3 \\ -14y=-17.\end{aligned}
$$

From the second equation, we get $y=\frac{17}{14}.$ Substituting this into the first equation, we get

$$
2x+4(\frac{17}{14})=3\,⟹\,x=-\frac{13}{14}.
$$

 
So, we conclude that the system is consistent independent. 

As a result, only statement II is true.

## q-131718 — original

Consider the following system of equations.

$$
{\begin{aligned} & x-3y+z=2 \\  & -2x+7y+2z=-1\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system has no solution
- The system is consistent independent

Original complete bank: I only, III only, None, I and II only, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & 1 & 2 \\ -2 & 7 & 2 & -1\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & 1 & 2 \\ -2 & 7 & 2 & -1\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & 1 & 2 \\ 0 & 1 & 4 & 3\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we can find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement I is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -x-6y+2z=-2 \\  & 2x+14y+4z=4\end{aligned}
$$

Which of the following statements are true?

- The system is consistent dependent
- The system has no solution
- The system is consistent independent

- III only
- II only
- I only
- I and II only
- None

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & -6 & 2 & -2 \\ 2 & 14 & 4 & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & -6 & 2 & -2 \\ 2 & 14 & 4 & 4\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-1 & -6 & 2 & -2 \\ 0 & 2 & 8 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y,$ and we have one free variable, $z.$ That means we can find $x$ and $y$ in terms of $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement I is true.

## q-74643 — original

Consider the following system of equations

$$
{\begin{aligned} & 3x+2y=8 \\  & x+y=-2 \\  & x+\frac{1}{2}y=5.\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

Original complete bank: II and III only, I and III only, I only, III only, II only

Original worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 2 & 8 \\ 1 & 1 & -2 \\ 1 & \frac{1}{2} & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 2 & 8 \\ 1 & 1 & -2 \\ 1 & \frac{1}{2} & 5\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & 1 & -2 \\ 3 & 2 & 8 \\ 1 & \frac{1}{2} & 5\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & 1 & -2 \\ 0 & -1 & 14 \\ 1 & \frac{1}{2} & 5\end{aligned}] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼[\begin{aligned}1 & 1 & -2 \\ 0 & -1 & 14 \\ 0 & -\frac{1}{2} & 7\end{aligned}] & {R}_{3} & :={R}_{3}+(-\frac{1}{2}){R}_{2} \\  & ∼[\begin{aligned}1 & 1 & -2 \\ 0 & -1 & 14 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
{\begin{aligned}x+y=-2 \\ -y=14.\end{aligned}
$$

From the second equation, we get $y=-14.$ Substituting this into the first equation, we get

$$
x+(-14)=-2\,⟹\,x=12.
$$

 
So,  we conclude that the system is consistent independent.   

As a result, only statement II is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations

$$
\{\begin{aligned} & -3x-4y=5 \\  & -x-2y=-3 \\  & -x-y=4.\end{aligned}
$$

Which of the following statements are true?

- The system has no solution
- The system is consistent independent
- The system is consistent dependent

- II and III only
- III only
- I and III only
- I only
- II only

Worked solution:

To classify the system, we first try to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}-3 & -4 & 5 \\ -1 & -2 & -3 \\ -1 & -1 & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & -4 & 5 \\ -1 & -2 & -3 \\ -1 & -1 & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}-1 & -2 & -3 \\ -3 & -4 & 5 \\ -1 & -1 & 4\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}-1 & -2 & -3 \\ 0 & 2 & 14 \\ -1 & -1 & 4\end{aligned}] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼[\begin{aligned}-1 & -2 & -3 \\ 0 & 2 & 14 \\ 0 & 1 & 7\end{aligned}] & {R}_{3} & :={R}_{3}+(-\frac{1}{2}){R}_{2} \\  & ∼[\begin{aligned}-1 & -2 & -3 \\ 0 & 2 & 14 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
\{\begin{aligned}-x-2y=-3 \\ 2y=14.\end{aligned}
$$

From the second equation, we get $y=7.$ Substituting this into the first equation, we get

$$
-x-2(7)=-3\,⟹\,x=-11.
$$

 
So,  we conclude that the system is consistent independent.   

As a result, only statement II is true.

## q-131720 — original

Consider the following system of equations.

$$
{\begin{aligned} & 2x-6y-2z=4 \\  & 3x-9y-3z=6\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system has no solution
III. The system is consistent dependent

Original complete bank: II and III only, I only, III only, None, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -6 & -2 & 4 \\ 3 & -9 & -3 & 6\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -6 & -2 & 4 \\ 3 & -9 & -3 & 6\end{aligned}] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & -1 & 2 \\ 3 & -9 & -3 & 6\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & -1 & 2 \\ 0 & 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have two free variables, $y$ and $z.$ That means we can find $x$ in terms of $y$ and $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement III is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & 2x+6y-4z=10 \\  & 3x+9y-6z=15\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system has no solution
III. The system is consistent dependent

- None
- III only
- II only
- II and III only
- I only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 6 & -4 & 10 \\ 3 & 9 & -6 & 15\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 6 & -4 & 10 \\ 3 & 9 & -6 & 15\end{aligned}] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & -2 & 5 \\ 3 & 9 & -6 & 15\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & -2 & 5 \\ 0 & 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have two free variables, $y$ and $z.$ That means we can find $x$ in terms of $y$ and $z.$ 

Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*. 

As a result, only statement III is true.

## q-131721 — original

Consider the following system of equations

$$
{\begin{aligned} & x+2y=-1 \\  & 3x+7y=1 \\  & -2x-4y=2.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system has no solution
III. The system is consistent dependent

Original complete bank: II and III only, I only, III only, None, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}1 & 2 & -1 \\ 3 & 7 & 1 \\ -2 & -4 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -1 \\ 3 & 7 & 1 \\ -2 & -4 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -1 \\ 0 & 1 & 4 \\ -2 & -4 & 2\end{aligned}] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -1 \\ 0 & 1 & 4 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
{\begin{aligned}x+2y=-1 \\ y=4.\end{aligned}
$$

From the second equation we have $y=4$ and substituting this into the first equation yields $x=-9.$ So,  we conclude that the system is consistent independent. 

As a result, only statement I is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations

$$
\{\begin{aligned} & 2x-2y=-4 \\  & 6x-7y=-9 \\  & -4x+4y=8.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system has no solution
III. The system is consistent dependent

- III only
- II and III only
- None
- I only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & -2 & -4 \\ 6 & -7 & -9 \\ -4 & 4 & 8\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -2 & -4 \\ 6 & -7 & -9 \\ -4 & 4 & 8\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}2 & -2 & -4 \\ 0 & -1 & 3 \\ -4 & 4 & 8\end{aligned}] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼[\begin{aligned}2 & -2 & -4 \\ 0 & -1 & 3 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
\{\begin{aligned}2x-2y=-4 \\ -y=3.\end{aligned}
$$

From the second equation we have $y=-3$ and substituting this into the first equation yields $x=-5.$ So,  we conclude that the system is consistent independent. 

As a result, only statement I is true.

## q-131722 — original

Consider the following system of equations

$$
{\begin{aligned} & 3x-3y=6 \\  & -2x+y=-3 \\  & 4x-4y=8.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent
II. The system is consistent independent
III. The system has no solution

Original complete bank: I only, III only, None, I and II only, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}3 & -3 & 6 \\ -2 & 1 & -3 \\ 4 & -4 & 8\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & -3 & 6 \\ -2 & 1 & -3 \\ 4 & -4 & 8\end{aligned}] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼[\begin{aligned}1 & -1 & 2 \\ -2 & 1 & -3 \\ 4 & -4 & 8\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}1 & -1 & 2 \\ 0 & -1 & 1 \\ 4 & -4 & 8\end{aligned}] & {R}_{3} & :={R}_{3}-4{R}_{1} \\  & ∼[\begin{aligned}1 & -1 & 2 \\ 0 & -1 & 1 \\ 0 & 0 & 0\end{aligned}] & {R}_{2} & :=-{R}_{2} \\  & ∼[\begin{aligned}1 & -1 & 2 \\ 0 & 1 & -1 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
{\begin{aligned}x-y=2 \\ y=-1.\end{aligned}
$$

From the second equation we have $y=-1$ and substituting this into the first equation yields $x=1.$ So,  we conclude that the system is consistent independent. 

As a result, only statement II is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations

$$
\{\begin{aligned} & -3x-3y=0 \\  & 2x+y=0 \\  & -4x-4y=0.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent
II. The system is consistent independent
III. The system has no solution

- I only
- I and II only
- II only
- None
- III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}-3 & -3 & 0 \\ 2 & 1 & 0 \\ -4 & -4 & 0\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & -3 & 0 \\ 2 & 1 & 0 \\ -4 & -4 & 0\end{aligned}] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼[\begin{aligned}-1 & -1 & 0 \\ 2 & 1 & 0 \\ -4 & -4 & 0\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-1 & -1 & 0 \\ 0 & -1 & 0 \\ -4 & -4 & 0\end{aligned}] & {R}_{3} & :={R}_{3}-4{R}_{1} \\  & ∼[\begin{aligned}-1 & -1 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 0\end{aligned}] & {R}_{2} & :=-{R}_{2} \\  & ∼[\begin{aligned}-1 & -1 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

 

Since any numbers $x$ and $y$ are solutions to the third equation $0x+0y=0$, we can remove this equation from the system. So, the corresponding system is now

$$
\{\begin{aligned}-x-y=0 \\ y=0.\end{aligned}
$$

From the second equation we have $y=0$ and substituting this into the first equation yields $x=0.$ So,  we conclude that the system is consistent independent. 

As a result, only statement II is true.

## q-42020 — original

Consider the following system of equations.

$$
{\begin{aligned} & x+2y=-1 \\  & 3x+y=3 \\  & -2x+y=-2.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent
II. The system has a unique solution
III. The system is inconsistent

Original complete bank: II and III only, I only, III only, I and II only, II only

Original worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & -1 \\ 3 & 1 & 3 \\ -2 & 1 & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:  

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -1 \\ 3 & 1 & 3 \\ -2 & 1 & -2\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -1 \\ 0 & -5 & 6 \\ -2 & 1 & -2\end{aligned}] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -1 \\ 0 & -5 & 6 \\ 0 & 5 & -4\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼[\begin{aligned}1 & 2 & -1 \\ 0 & -5 & 6 \\ 0 & 0 & 2\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=2,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & 2x+2y=-4 \\  & 6x+y=-1 \\  & -4x+y=-1.\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent
II. The system has a unique solution
III. The system is inconsistent

- II only
- III only
- I and II only
- II and III only
- I only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 2 & -4 \\ 6 & 1 & -1 \\ -4 & 1 & -1\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:  

$$
\begin{aligned}M & =[\begin{aligned}2 & 2 & -4 \\ 6 & 1 & -1 \\ -4 & 1 & -1\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}2 & 2 & -4 \\ 0 & -5 & 11 \\ -4 & 1 & -1\end{aligned}] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼[\begin{aligned}2 & 2 & -4 \\ 0 & -5 & 11 \\ 0 & 5 & -9\end{aligned}] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼[\begin{aligned}2 & 2 & -4 \\ 0 & -5 & 11 \\ 0 & 0 & 2\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=2,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

## q-74634 — original

Consider the following system of equations.

$$
\{\begin{aligned} & 2x-y=-1 \\  & 2x-4y=3 \\  & x+y=2\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent

II. The system has a unique solution

III. The system is inconsistent

Original complete bank: II and III only, I only, III only, I and II only, II only

Original worked solution:

To classify the system, we will first try to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & -1 & -1 \\ 2 & -4 & 3 \\ 1 & 1 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -1 & -1 \\ 2 & -4 & 3 \\ 1 & 1 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼[\begin{aligned}2 & -1 & -1 \\ 0 & -3 & 4 \\ 1 & 1 & 2\end{aligned}] & {R}_{3} & :={R}_{3}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & -1 & -1 \\ 0 & -3 & 4 \\ 0 & \frac{3}{2} & \frac{5}{2}\end{aligned}] & {R}_{3} & :={R}_{3}+\frac{1}{2}{R}_{2} \\  & ∼[\begin{aligned}2 & -1 & -1 \\ 0 & -3 & 4 \\ 0 & 0 & \frac{9}{2}\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=\frac{9}{2},$ and it has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

### Generated moderate variant (parameter extension)

Consider the following system of equations.

$$
\{\begin{aligned} & -4x-y=4 \\  & -4x-4y=11 \\  & -2x+y=3\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent

II. The system has a unique solution

III. The system is inconsistent

- II only
- I only
- I and II only
- II and III only
- III only

Worked solution:

To classify the system, we will first try to find its solution. The augmented matrix for this system is 

$$
M=[\begin{aligned}-4 & -1 & 4 \\ -4 & -4 & 11 \\ -2 & 1 & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}-4 & -1 & 4 \\ -4 & -4 & 11 \\ -2 & 1 & 3\end{aligned}] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\  & ∼[\begin{aligned}-4 & -1 & 4 \\ 0 & -3 & 7 \\ -2 & 1 & 3\end{aligned}] & {R}_{3} & :={R}_{3}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}-4 & -1 & 4 \\ 0 & -3 & 7 \\ 0 & \frac{3}{2} & 1\end{aligned}] & {R}_{3} & :={R}_{3}+\frac{1}{2}{R}_{2} \\  & ∼[\begin{aligned}-4 & -1 & 4 \\ 0 & -3 & 7 \\ 0 & 0 & \frac{9}{2}\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=\frac{9}{2},$ and it has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement III is true.

## Authored easy example 1

Consider the following system of equations.

$$
\{\begin{aligned}x+y=-5 \\ 2x+3y=-7\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent dependent
II. The system is inconsistent
III. The system is consistent independent

- I and III only
- I and II only
- III only
- I only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 1 & -5 \\ 2 & 3 & -7\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 1 & -5 \\ 2 & 3 & -7\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & 1 & -5 \\ 0 & 1 & 3\end{aligned}]\end{aligned}
$$

There is a pivot for each variable and no contradictory row. The system has a unique solution, so we conclude that the system is consistent independent.

As a result, only statement III is true.

## Authored easy example 2

Consider the following system of equations.

$$
\{\begin{aligned}x+2y=-4 \\ x+2y=-4\end{aligned}
$$

Which of the following statements are true?

I. The system is inconsistent
II. The system is consistent independent
III. The system is consistent dependent

- I and II only
- I and III only
- I only
- III only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & -4 \\ 1 & 2 & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -4 \\ 1 & 2 & -4\end{aligned}] & {R}_{2}:={R}_{2}+(-1){R}_{1} \\ & ∼[\begin{aligned}1 & 2 & -4 \\ 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. Here there is one free variable, $y$. Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.

As a result, only statement III is true.

## Authored easy example 6

Consider the following system of equations.

$$
\{\begin{aligned}x-y=0 \\ 2x-2y=-4\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is inconsistent
III. The system is consistent dependent

- II only
- I only
- III only
- I and II only
- I and III only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -1 & 0 \\ 2 & -2 & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -1 & 0 \\ 2 & -2 & -4\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & 0 \\ 0 & 0 & -4\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y=-4,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.

## Authored hard example 1

Consider the following system of equations.

$$
\{\begin{aligned}x-2y-3z=4 \\ x-y-4z=7 \\ -2x+2y+7z=-15\end{aligned}
$$

Which of the following statements are true?

I. The system is inconsistent
II. The system is consistent dependent
III. The system is consistent independent

- III only
- I and II only
- I and III only
- II only
- I only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -2 & -3 & 4 \\ 1 & -1 & -4 & 7 \\ -2 & 2 & 7 & -15\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -2 & -3 & 4 \\ 1 & -1 & -4 & 7 \\ -2 & 2 & 7 & -15\end{aligned}] & {R}_{2}:={R}_{2}+(-1){R}_{1} \\ & ∼[\begin{aligned}1 & -2 & -3 & 4 \\ 0 & 1 & -1 & 3 \\ -2 & 2 & 7 & -15\end{aligned}] & {R}_{3}:={R}_{3}+(2){R}_{1} \\ & ∼[\begin{aligned}1 & -2 & -3 & 4 \\ 0 & 1 & -1 & 3 \\ 0 & -2 & 1 & -7\end{aligned}] & {R}_{3}:={R}_{3}+(2){R}_{2} \\ & ∼[\begin{aligned}1 & -2 & -3 & 4 \\ 0 & 1 & -1 & 3 \\ 0 & 0 & -1 & -1\end{aligned}]\end{aligned}
$$

There is a pivot for each variable and no contradictory row. The system has a unique solution, so we conclude that the system is consistent independent.

As a result, only statement III is true.

## Authored hard example 2

Consider the following system of equations.

$$
\{\begin{aligned}x+2y-3z=-1 \\ 2x+5y-9z=0 \\ 2x+6y-12z=2\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is inconsistent
III. The system is consistent dependent

- III only
- I only
- I and III only
- I and II only
- II only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & -3 & -1 \\ 2 & 5 & -9 & 0 \\ 2 & 6 & -12 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -3 & -1 \\ 2 & 5 & -9 & 0 \\ 2 & 6 & -12 & 2\end{aligned}] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & 2 & -3 & -1 \\ 0 & 1 & -3 & 2 \\ 2 & 6 & -12 & 2\end{aligned}] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\ & ∼[\begin{aligned}1 & 2 & -3 & -1 \\ 0 & 1 & -3 & 2 \\ 0 & 2 & -6 & 4\end{aligned}] & {R}_{3}:={R}_{3}+(-2){R}_{2} \\ & ∼[\begin{aligned}1 & 2 & -3 & -1 \\ 0 & 1 & -3 & 2 \\ 0 & 0 & 0 & 0\end{aligned}]\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. Here there is one free variable, $z$. Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.

As a result, only statement III is true.

## Authored hard example 6

Consider the following system of equations.

$$
\{\begin{aligned}x-y+3z=0 \\ -2x+3y-3z=5 \\ -x+3y+3z=6\end{aligned}
$$

Which of the following statements are true?

I. The system is consistent independent
II. The system is inconsistent
III. The system is consistent dependent

- III only
- I and III only
- I and II only
- II only
- I only

Worked solution:

To classify the system, we first need to find its solution. The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -1 & 3 & 0 \\ -2 & 3 & -3 & 5 \\ -1 & 3 & 3 & 6\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -1 & 3 & 0 \\ -2 & 3 & -3 & 5 \\ -1 & 3 & 3 & 6\end{aligned}] & {R}_{2}:={R}_{2}+(2){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & 3 & 0 \\ 0 & 1 & 3 & 5 \\ -1 & 3 & 3 & 6\end{aligned}] & {R}_{3}:={R}_{3}+(1){R}_{1} \\ & ∼[\begin{aligned}1 & -1 & 3 & 0 \\ 0 & 1 & 3 & 5 \\ 0 & 2 & 6 & 6\end{aligned}] & {R}_{3}:={R}_{3}+(-2){R}_{2} \\ & ∼[\begin{aligned}1 & -1 & 3 & 0 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 0 & -4\end{aligned}]\end{aligned}
$$

The final row corresponds to the equation $0x+0y+0z=-4,$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.

As a result, only statement II is true.
