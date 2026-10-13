# Number-of-solutions review

Raw captures lack difficulty, correct refs and worked solutions. Completion/level labels below are authored. Literal raw braces remain evidence; normal output escapes the literal system brace.

## Original q-211984

## moderate — raw incomplete evidence

Consider the following system of equations:

${6x + 4y = 6; - 2x - y = 5$

This system of equations has {{field-1}}.

- no solutions
- infinitely many solutions
- a single solution

### Inferred completion at the original parameters

## moderate — authored completion

Consider the following system of equations:

$\{6x + 4y = 6; -2x - y = 5$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the second equation by $3$, then we will get a $-6x$ term that can cancel with the $6x$ term in the first equation:

$$
\{6x + 4y = 6; -2x - y = 5 \mid \mid \cdot (3)
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
6x + 4y &= 6 \\
-6x - 3y &= 15 \\
y &= (6 + 15) \\
y &= 21 \\
y &= 21
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
6x + (4)(21) &= 6 \\
6x &= -78 \\
x &= -13
\end{aligned}
$$

The system has *a single solution*, $(-13,21)$.

### Generated variant

## moderate — authored completion

Consider the following system of equations:

$\{-2x + 3y = -2; 6x + 3y = 8$

This system of equations has {{field-1}}.

- no solutions
- infinitely many solutions
- a single solution

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $3$, then we will get a $-6x$ term that can cancel with the $6x$ term in the second equation:

$$
\{-2x + 3y = -2 \mid \mid \cdot (3); 6x + 3y = 8
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
-6x + 9y &= -6 \\
6x + 3y &= 8 \\
12y &= (-6 + 8) \\
12y &= 2 \\
y &= \frac{1}{6}
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
-2x + (3)(\frac{1}{6}) &= -2 \\
-2x &= - \frac{5}{2} \\
x &= \frac{5}{4}
\end{aligned}
$$

The system has *a single solution*, $(\frac{5}{4},\frac{1}{6})$.

## Original q-237043

## hard — raw incomplete evidence

Consider the following system of equations:

${y - 3x - 2 = 0; 4y - 12x - 8 = 0$

This system of equations has {{field-1}}.

- a single solution
- infinitely many solutions
- no solutions

### Inferred completion at the original parameters

## hard — authored completion

Consider the following system of equations:

$\{y - 3x - 2 = 0; 4y - 12x - 8 = 0$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: infinitely many solutions

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
-3x + y &= 2 \\
-12x + 4y &= 8
\end{aligned}
$$

Notice that if we multiply the first equation by $-4$, then we will get a $12x$ term that can cancel with the $-12x$ term in the second equation:

$$
\{-3x + y = 2 \mid \mid \cdot (-4); -12x + 4y = 8
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:

$$
\begin{aligned}
12x - 4y &= -8 \\
-12x + 4y &= 8 \\
0 &= (-8 + 8) \\
0 &= 0
\end{aligned}
$$

The statement $0=0$ is *always true*. Therefore, we conclude that the system has *infinitely many solutions*.

### Generated variant

## hard — authored completion

Consider the following system of equations:

$\{-y - 3x + 5 = 0; 2y + 6x - 10 = 0$

This system of equations has {{field-1}}.

- infinitely many solutions
- a single solution
- no solutions

Correct: infinitely many solutions

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
-3x - y &= -5 \\
6x + 2y &= 10
\end{aligned}
$$

Notice that if we multiply the first equation by $2$, then we will get a $-6x$ term that can cancel with the $6x$ term in the second equation:

$$
\{-3x - y = -5 \mid \mid \cdot (2); 6x + 2y = 10
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:

$$
\begin{aligned}
-6x - 2y &= -10 \\
6x + 2y &= 10 \\
0 &= (-10 + 10) \\
0 &= 0
\end{aligned}
$$

The statement $0=0$ is *always true*. Therefore, we conclude that the system has *infinitely many solutions*.

## Original q-237046

## moderate — raw incomplete evidence

Consider the following system of equations:

${2x - 5y = 15; 4x - 10y =-10$

This system of equations has {{field-1}}.

- no solutions
- infinitely many solutions
- a single solution

### Inferred completion at the original parameters

## moderate — authored completion

Consider the following system of equations:

$\{2x - 5y = 15; 4x - 10y = -10$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: no solutions

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $-2$, then we will get a $-4x$ term that can cancel with the $4x$ term in the second equation:

$$
\{2x - 5y = 15 \mid \mid \cdot (-2); 4x - 10y = -10
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
-4x + 10y &= -30 \\
4x - 10y &= -10 \\
0 &= (-30 - 10) \\
0 &= -40
\end{aligned}
$$

The statement $0=-40$ is *always false*. Therefore, we conclude that the system has *no solutions*.

### Generated variant

## moderate — authored completion

Consider the following system of equations:

$\{4x - 4y = 10; -x + y = -3$

This system of equations has {{field-1}}.

- infinitely many solutions
- no solutions
- a single solution

Correct: no solutions

Let's start by solving the system using elimination.

Notice that if we multiply the second equation by $4$, then we will get a $-4x$ term that can cancel with the $4x$ term in the first equation:

$$
\{4x - 4y = 10; -x + y = -3 \mid \mid \cdot (4)
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
4x - 4y &= 10 \\
-4x + 4y &= -12 \\
0 &= (10 - 12) \\
0 &= -2
\end{aligned}
$$

The statement $0=-2$ is *always false*. Therefore, we conclude that the system has *no solutions*.

## Generated easy variant 0

## easy — authored completion

Consider the following system of equations:

$\{x - 3y = 2; x - 3y = 2$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: infinitely many solutions

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $-1$, then we will get a $-x$ term that can cancel with the $x$ term in the second equation:

$$
\{x - 3y = 2 \mid \mid \cdot (-1); x - 3y = 2
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:

$$
\begin{aligned}
-x + 3y &= -2 \\
x - 3y &= 2 \\
0 &= (-2 + 2) \\
0 &= 0
\end{aligned}
$$

The statement $0=0$ is *always true*. Therefore, we conclude that the system has *infinitely many solutions*.

## Generated easy variant 1

## easy — authored completion

Consider the following system of equations:

$\{2x - 3y = -4; 2x - 3y = -5$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: no solutions

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $-1$, then we will get a $-2x$ term that can cancel with the $2x$ term in the second equation:

$$
\{2x - 3y = -4 \mid \mid \cdot (-1); 2x - 3y = -5
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
-2x + 3y &= 4 \\
2x - 3y &= -5 \\
0 &= (4 - 5) \\
0 &= -1
\end{aligned}
$$

The statement $0=-1$ is *always false*. Therefore, we conclude that the system has *no solutions*.

## Generated easy variant 5

## easy — authored completion

Consider the following system of equations:

$\{-x + 5y = -12; -x + 3y = 6$

This system of equations has {{field-1}}.

- infinitely many solutions
- a single solution
- no solutions

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $-1$, then we will get a $x$ term that can cancel with the $-x$ term in the second equation:

$$
\{-x + 5y = -12 \mid \mid \cdot (-1); -x + 3y = 6
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
x - 5y &= 12 \\
-x + 3y &= 6 \\
-2y &= (12 + 6) \\
-2y &= 18 \\
y &= -9
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
-x + (5)(-9) &= -12 \\
-x &= 33 \\
x &= -33
\end{aligned}
$$

The system has *a single solution*, $(-33,-9)$.

## Generated moderate variant 0

## moderate — authored completion

Consider the following system of equations:

$\{-2x + 6y = -6; x - 3y = 3$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: infinitely many solutions

Let's start by solving the system using elimination.

Notice that if we multiply the second equation by $2$, then we will get a $2x$ term that can cancel with the $-2x$ term in the first equation:

$$
\{-2x + 6y = -6; x - 3y = 3 \mid \mid \cdot (2)
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:

$$
\begin{aligned}
-2x + 6y &= -6 \\
2x - 6y &= 6 \\
0 &= (-6 + 6) \\
0 &= 0
\end{aligned}
$$

The statement $0=0$ is *always true*. Therefore, we conclude that the system has *infinitely many solutions*.

## Generated moderate variant 1

## moderate — authored completion

Consider the following system of equations:

$\{-4x + 6y = 11; 2x - 3y = -5$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: no solutions

Let's start by solving the system using elimination.

Notice that if we multiply the second equation by $2$, then we will get a $4x$ term that can cancel with the $-4x$ term in the first equation:

$$
\{-4x + 6y = 11; 2x - 3y = -5 \mid \mid \cdot (2)
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
-4x + 6y &= 11 \\
4x - 6y &= -10 \\
0 &= (11 - 10) \\
0 &= 1
\end{aligned}
$$

The statement $0=1$ is *always false*. Therefore, we conclude that the system has *no solutions*.

## Generated moderate variant 5

## moderate — authored completion

Consider the following system of equations:

$\{2x + 4y = -12; -x + 3y = 6$

This system of equations has {{field-1}}.

- infinitely many solutions
- a single solution
- no solutions

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the second equation by $2$, then we will get a $-2x$ term that can cancel with the $2x$ term in the first equation:

$$
\{2x + 4y = -12; -x + 3y = 6 \mid \mid \cdot (2)
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
2x + 4y &= -12 \\
-2x + 6y &= 12 \\
10y &= (-12 + 12) \\
10y &= 0 \\
y &= 0
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
2x + (4)(0) &= -12 \\
2x &= -12 \\
x &= -6
\end{aligned}
$$

The system has *a single solution*, $(-6,0)$.

## Generated hard variant 0

## hard — authored completion

Consider the following system of equations:

$\{-y + x - 3 = 0; 2y - 2x + 6 = 0$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: infinitely many solutions

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
x - y &= 3 \\
-2x + 2y &= -6
\end{aligned}
$$

Notice that if we multiply the first equation by $2$, then we will get a $2x$ term that can cancel with the $-2x$ term in the second equation:

$$
\{x - y = 3 \mid \mid \cdot (2); -2x + 2y = -6
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:

$$
\begin{aligned}
2x - 2y &= 6 \\
-2x + 2y &= -6 \\
0 &= (6 - 6) \\
0 &= 0
\end{aligned}
$$

The statement $0=0$ is *always true*. Therefore, we conclude that the system has *infinitely many solutions*.

## Generated hard variant 1

## hard — authored completion

Consider the following system of equations:

$\{-y + 2x + 5 = 0; 2y - 4x - 11 = 0$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: no solutions

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
2x - y &= -5 \\
-4x + 2y &= 11
\end{aligned}
$$

Notice that if we multiply the first equation by $2$, then we will get a $4x$ term that can cancel with the $-4x$ term in the second equation:

$$
\{2x - y = -5 \mid \mid \cdot (2); -4x + 2y = 11
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
4x - 2y &= -10 \\
-4x + 2y &= 11 \\
0 &= (-10 + 11) \\
0 &= 1
\end{aligned}
$$

The statement $0=1$ is *always false*. Therefore, we conclude that the system has *no solutions*.

## Generated hard variant 5

## hard — authored completion

Consider the following system of equations:

$\{-y + x + 6 = 0; -2y + 4x + 9 = 0$

This system of equations has {{field-1}}.

- no solutions
- a single solution
- infinitely many solutions

Correct: a single solution

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
x - y &= -6 \\
4x - 2y &= -9
\end{aligned}
$$

Notice that if we multiply the first equation by $-4$, then we will get a $-4x$ term that can cancel with the $4x$ term in the second equation:

$$
\{x - y = -6 \mid \mid \cdot (-4); 4x - 2y = -9
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
-4x + 4y &= 24 \\
4x - 2y &= -9 \\
2y &= (24 - 9) \\
2y &= 15 \\
y &= \frac{15}{2}
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
x + (-1)(\frac{15}{2}) &= -6 \\
x &= \frac{3}{2} \\
x &= \frac{3}{2}
\end{aligned}
$$

The system has *a single solution*, $(\frac{3}{2},\frac{15}{2})$.

## Generated signed boundary easy

## easy — authored completion

Consider the following system of equations:

$\{5x - 5y = 12; -5x + 3y = -12$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $1$, then we will get a $5x$ term that can cancel with the $-5x$ term in the second equation:

$$
\{5x - 5y = 12 \mid \mid \cdot (1); -5x + 3y = -12
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
5x - 5y &= 12 \\
-5x + 3y &= -12 \\
-2y &= (12 - 12) \\
-2y &= 0 \\
y &= 0
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
5x + (-5)(0) &= 12 \\
5x &= 12 \\
x &= \frac{12}{5}
\end{aligned}
$$

The system has *a single solution*, $(\frac{12}{5},0)$.

## Generated signed boundary moderate

## moderate — authored completion

Consider the following system of equations:

$\{-2x + 5y = 30; -8x - 10y = -30$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: a single solution

Let's start by solving the system using elimination.

Notice that if we multiply the first equation by $-4$, then we will get a $8x$ term that can cancel with the $-8x$ term in the second equation:

$$
\{-2x + 5y = 30 \mid \mid \cdot (-4); -8x - 10y = -30
$$

When we add the two equations, the $x$ terms cancel, and we can solve for $y$:

$$
\begin{aligned}
8x - 20y &= -120 \\
-8x - 10y &= -30 \\
-30y &= (-120 - 30) \\
-30y &= -150 \\
y &= 5
\end{aligned}
$$

Substituting into the first equation gives:

$$
\begin{aligned}
-2x + (5)(5) &= 30 \\
-2x &= 5 \\
x &= - \frac{5}{2}
\end{aligned}
$$

The system has *a single solution*, $(- \frac{5}{2},5)$.

## Generated signed boundary hard

## hard — authored completion

Consider the following system of equations:

$\{y - 3x - 30 = 0; 4y - 12x + 30 = 0$

This system of equations has {{field-1}}.

- a single solution
- no solutions
- infinitely many solutions

Correct: no solutions

Let's start by solving the system using elimination.

First, rearrange each equation to put the variable terms on the left and the constant on the right:

$$
\begin{aligned}
-3x + y &= 30 \\
-12x + 4y &= -30
\end{aligned}
$$

Notice that if we multiply the first equation by $-4$, then we will get a $12x$ term that can cancel with the $-12x$ term in the second equation:

$$
\{-3x + y = 30 \mid \mid \cdot (-4); -12x + 4y = -30
$$

When we add the two equations, it turns out that both variables cancel, and we obtain a false statement:

$$
\begin{aligned}
12x - 4y &= -120 \\
-12x + 4y &= -30 \\
0 &= (-120 - 30) \\
0 &= -150
\end{aligned}
$$

The statement $0=-150$ is *always false*. Therefore, we conclude that the system has *no solutions*.
