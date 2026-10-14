# Review: homogeneous / inhomogeneous ODE recognition

All records are local drafts at math basis 1356. Raw source profiles are evidence-only. Normal generated examples preserve source operative masks. Hard is an authored scope extension.

## Original q-331601

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+2xy=0$
- ${y}^{′}+2xy=4$
- ${y}^{′}+2xy=-y$

Bank: II only, I, II, and III, I and III only, I only, III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+2xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}+2xy=4.
$$

The presence of the constant term $4$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+2xy=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+2xy & =-y \\ {y}^{′}+2xy+y & =0 \\ {y}^{′}+(2x+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I and III only."

### Generated variant (observed_q-331601)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+7{x}^{2}y=0$
- ${y}^{′}+7{x}^{2}y=-8$
- ${y}^{′}+7{x}^{2}y=-3y$

- I and III only
- I, II, and III
- II only
- III only
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8.
$$

The presence of the constant term $-8$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =-3y \\ {y}^{′}+7{x}^{2}y+3y & =0 \\ {y}^{′}+(7{x}^{2}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I and III only."

### Generated variant (observed_q-331601)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+3{x}^{3}y=0$
- ${y}^{′}+3{x}^{3}y=-7$
- ${y}^{′}+3{x}^{3}y=-3y$

- I and III only
- I only
- III only
- II only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7.
$$

The presence of the constant term $-7$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =-3y \\ {y}^{′}+3{x}^{3}y+3y & =0 \\ {y}^{′}+(3{x}^{3}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I and III only."

## Original q-331744

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-xy=0$
- ${y}^{′}-xy=y$
- ${y}^{′}-xy={x}^{3}$

Bank: III only, II only, I only, I, II, and III, I and III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-xy=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-xy & =y \\ {y}^{′}-xy-y & =0 \\ {y}^{′}-(x+1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-xy={x}^{3}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={x}^{3}$ is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."

### Generated variant (observed_q-331744)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-7{x}^{2}y=0$
- ${y}^{′}-7{x}^{2}y=y$
- ${y}^{′}-7{x}^{2}y=-{x}^{3}$

- I only
- II only
- III only
- I and III only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-7{x}^{2}y=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-7{x}^{2}y & =y \\ {y}^{′}-7{x}^{2}y-y & =0 \\ {y}^{′}-(7{x}^{2}+1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-7{x}^{2}y=-{x}^{3}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-{x}^{3}$ is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."

### Generated variant (observed_q-331744)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-3{x}^{3}y=0$
- ${y}^{′}-3{x}^{3}y=y$
- ${y}^{′}-3{x}^{3}y=-x$

- I only
- I, II, and III
- I and III only
- III only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-3{x}^{3}y=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-3{x}^{3}y & =y \\ {y}^{′}-3{x}^{3}y-y & =0 \\ {y}^{′}-(3{x}^{3}+1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-3{x}^{3}y=-x.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-x$ is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."

## Original q-331605

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+{x}^{2}y=3x$
- ${y}^{′}+{x}^{2}y=0$
- ${y}^{′}+{x}^{2}y=y$

Bank: I only, II only, III only, I and II only, I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+{x}^{2}y=3x.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=3x$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+{x}^{2}y=0.
$$

Notice that this equation has the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+{x}^{2}y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+{x}^{2}y & =y \\ {y}^{′}+{x}^{2}y-y & =0 \\ {y}^{′}+({x}^{2}-1)y & =0.\end{aligned}
$$

Since our equation can be written in the form ${y}^{′}+P(x)y=0,$ the equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331605)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+7{x}^{2}y=-8{x}^{2}$
- ${y}^{′}+7{x}^{2}y=0$
- ${y}^{′}+7{x}^{2}y=5y$

- III only
- II only
- I only
- I, II, and III
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

Notice that this equation has the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=5y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =5y \\ {y}^{′}+7{x}^{2}y-5y & =0 \\ {y}^{′}+(7{x}^{2}-5)y & =0.\end{aligned}
$$

Since our equation can be written in the form ${y}^{′}+P(x)y=0,$ the equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331605)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+3{x}^{3}y=-7{x}^{2}$
- ${y}^{′}+3{x}^{3}y=0$
- ${y}^{′}+3{x}^{3}y=y$

- III only
- I and II only
- I, II, and III
- I only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

Notice that this equation has the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =y \\ {y}^{′}+3{x}^{3}y-y & =0 \\ {y}^{′}+(3{x}^{3}-1)y & =0.\end{aligned}
$$

Since our equation can be written in the form ${y}^{′}+P(x)y=0,$ the equation is homogeneous.

Therefore, the correct answer is "I only."

## Original q-331724

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+2{x}^{3}y={x}^{2}$
- ${y}^{′}+2{x}^{3}y=-3y$
- ${y}^{′}+2{x}^{3}y=0$

Bank: III only, I, II, and III, II only, I only, II and III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+2{x}^{3}y={x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+2{x}^{3}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+2{x}^{3}y & =-3y \\ {y}^{′}+2{x}^{3}y+3y & =0 \\ {y}^{′}+(2{x}^{3}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+2{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "II and III only."

### Generated variant (observed_q-331724)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+7{x}^{2}y=-8{x}^{2}$
- ${y}^{′}+7{x}^{2}y=-5y$
- ${y}^{′}+7{x}^{2}y=0$

- II only
- I, II, and III
- III only
- II and III only
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-5y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =-5y \\ {y}^{′}+7{x}^{2}y+5y & =0 \\ {y}^{′}+(7{x}^{2}+5)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "II and III only."

### Generated variant (observed_q-331724)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+3{x}^{3}y=-7{x}^{2}$
- ${y}^{′}+3{x}^{3}y=-y$
- ${y}^{′}+3{x}^{3}y=0$

- II only
- I only
- II and III only
- III only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =-y \\ {y}^{′}+3{x}^{3}y+y & =0 \\ {y}^{′}+(3{x}^{3}+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "II and III only."

## Original q-331725

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-xy=-y$
- ${y}^{′}-xy=0$
- ${y}^{′}-xy=-5y$

Bank: II only, I only, I, II, and III, I and III only, III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-xy=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-xy & =-y \\ {y}^{′}-xy+y & =0 \\ {y}^{′}-(x-1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}-xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-xy=-5y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-xy & =-5y \\ {y}^{′}-xy+5y & =0 \\ {y}^{′}-(x-5)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I, II and III."

### Generated variant (observed_q-331725)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-7{x}^{2}y=-y$
- ${y}^{′}-7{x}^{2}y=0$
- ${y}^{′}-7{x}^{2}y=-3y$

- I, II, and III
- I only
- II only
- III only
- I and III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-7{x}^{2}y=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-7{x}^{2}y & =-y \\ {y}^{′}-7{x}^{2}y+y & =0 \\ {y}^{′}-(7{x}^{2}-1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}-7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-7{x}^{2}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-7{x}^{2}y & =-3y \\ {y}^{′}-7{x}^{2}y+3y & =0 \\ {y}^{′}-(7{x}^{2}-3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I, II and III."

### Generated variant (observed_q-331725)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-3{x}^{3}y=-y$
- ${y}^{′}-3{x}^{3}y=0$
- ${y}^{′}-3{x}^{3}y=-3y$

- I, II, and III
- I and III only
- III only
- II only
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-3{x}^{3}y=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-3{x}^{3}y & =-y \\ {y}^{′}-3{x}^{3}y+y & =0 \\ {y}^{′}-(3{x}^{3}-1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}-3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-3{x}^{3}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-3{x}^{3}y & =-3y \\ {y}^{′}-3{x}^{3}y+3y & =0 \\ {y}^{′}-(3{x}^{3}-3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I, II and III."

## Original q-331727

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+{x}^{2}y=-3y$
- ${y}^{′}+{x}^{2}y=x$
- ${y}^{′}+{x}^{2}y=0$

Bank: I only, III only, I and III only, I, II, and III, II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+{x}^{2}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+{x}^{2}y & =-3y \\ {y}^{′}+{x}^{2}y+3y & =0 \\ {y}^{′}+({x}^{2}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+{x}^{2}y=x.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=x$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I and III only."

### Generated variant (observed_q-331727)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+7{x}^{2}y=-y$
- ${y}^{′}+7{x}^{2}y=-{x}^{3}$
- ${y}^{′}+7{x}^{2}y=0$

- I and III only
- III only
- I only
- II only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =-y \\ {y}^{′}+7{x}^{2}y+y & =0 \\ {y}^{′}+(7{x}^{2}+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-{x}^{3}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-{x}^{3}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I and III only."

### Generated variant (observed_q-331727)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+3{x}^{3}y=-y$
- ${y}^{′}+3{x}^{3}y=-x$
- ${y}^{′}+3{x}^{3}y=0$

- I and III only
- I, II, and III
- II only
- I only
- III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =-y \\ {y}^{′}+3{x}^{3}y+y & =0 \\ {y}^{′}+(3{x}^{3}+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-x.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-x$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I and III only."

## Original q-331728

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-4xy=y$
- ${y}^{′}-4xy=0$
- ${y}^{′}-4xy=9$

Bank: II only, III only, I and II only, I only, I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-4xy=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-4xy & =y \\ {y}^{′}-4xy-y & =0 \\ {y}^{′}-(4x+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-4xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-4xy=9.
$$

The presence of the constant term $9$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

Therefore, the correct answer is "I and II only."

### Generated variant (observed_q-331728)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-7{x}^{2}y=y$
- ${y}^{′}-7{x}^{2}y=0$
- ${y}^{′}-7{x}^{2}y=-1$

- I and II only
- III only
- II only
- I, II, and III
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-7{x}^{2}y=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-7{x}^{2}y & =y \\ {y}^{′}-7{x}^{2}y-y & =0 \\ {y}^{′}-(7{x}^{2}+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-7{x}^{2}y=-1.
$$

The presence of the constant term $-1$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

Therefore, the correct answer is "I and II only."

### Generated variant (observed_q-331728)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}-3{x}^{3}y=y$
- ${y}^{′}-3{x}^{3}y=0$
- ${y}^{′}-3{x}^{3}y=-1$

- I and II only
- I only
- I, II, and III
- II only
- III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}-3{x}^{3}y=y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}-3{x}^{3}y & =y \\ {y}^{′}-3{x}^{3}y-y & =0 \\ {y}^{′}-(3{x}^{3}+1)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{y}^{′}-3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-3{x}^{3}y=-1.
$$

The presence of the constant term $-1$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

Therefore, the correct answer is "I and II only."

## Original q-331729

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+7xy=5$
- ${y}^{′}+7xy=0$
- ${y}^{′}+7xy=-2y$

Bank: II and III only, I, II, and III, III only, II only, I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+7xy=5.
$$

The presence of the constant term $5$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+7xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7xy=-2y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+7xy & =-2y \\ {y}^{′}+7xy+2y & =0 \\ {y}^{′}+(7x+2)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II and III only."

### Generated variant (observed_q-331729)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+7{x}^{2}y=-8$
- ${y}^{′}+7{x}^{2}y=0$
- ${y}^{′}+7{x}^{2}y=-3y$

- III only
- I, II, and III
- II and III only
- I only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8.
$$

The presence of the constant term $-8$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =-3y \\ {y}^{′}+7{x}^{2}y+3y & =0 \\ {y}^{′}+(7{x}^{2}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II and III only."

### Generated variant (observed_q-331729)

Which of the following first-order linear differential equations are homogeneous?

- ${y}^{′}+3{x}^{3}y=-7$
- ${y}^{′}+3{x}^{3}y=0$
- ${y}^{′}+3{x}^{3}y=-3y$

- III only
- II only
- I only
- II and III only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7.
$$

The presence of the constant term $-7$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-3y.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =-3y \\ {y}^{′}+3{x}^{3}y+3y & =0 \\ {y}^{′}+(3{x}^{3}+3)y & =0\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II and III only."

## Original q-331738

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+4xy=2$
- ${y}^{′}+4xy=0$
- ${y}^{′}+4xy=y$

Bank: I, II, and III, III only, II only, I and II only, I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+4xy=2.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=2$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+4xy=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+4xy=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+4xy & =y \\ {y}^{′}+4xy-y & =0 \\ {y}^{′}+(4x-1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331738)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+7{x}^{2}y=-8$
- ${y}^{′}+7{x}^{2}y=0$
- ${y}^{′}+7{x}^{2}y=3y$

- II only
- III only
- I, II, and III
- I only
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=3y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =3y \\ {y}^{′}+7{x}^{2}y-3y & =0 \\ {y}^{′}+(7{x}^{2}-3)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331738)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+3{x}^{3}y=-7$
- ${y}^{′}+3{x}^{3}y=0$
- ${y}^{′}+3{x}^{3}y=3y$

- II only
- I and II only
- I only
- I, II, and III
- III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=3y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =3y \\ {y}^{′}+3{x}^{3}y-3y & =0 \\ {y}^{′}+(3{x}^{3}-3)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

## Original q-331739

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-{x}^{2}y={x}^{3}$
- ${y}^{′}-{x}^{2}y=y$
- ${y}^{′}-{x}^{2}y=0$

Bank: I, II, and III, I only, II only, I and II only, III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-{x}^{2}y={x}^{3}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={x}^{3}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}-{x}^{2}y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}-{x}^{2}y & =y \\ {y}^{′}-{x}^{2}y-y & =0 \\ {y}^{′}-({x}^{2}+1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331739)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-7{x}^{2}y=-8{x}^{2}$
- ${y}^{′}-7{x}^{2}y=5y$
- ${y}^{′}-7{x}^{2}y=0$

- II only
- I only
- I, II, and III
- III only
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-7{x}^{2}y=-8{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}-7{x}^{2}y=5y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}-7{x}^{2}y & =5y \\ {y}^{′}-7{x}^{2}y-5y & =0 \\ {y}^{′}-(7{x}^{2}+5)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331739)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}-3{x}^{3}y=-7{x}^{2}$
- ${y}^{′}-3{x}^{3}y=y$
- ${y}^{′}-3{x}^{3}y=0$

- II only
- I and II only
- III only
- I, II, and III
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}-3{x}^{3}y=-7{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}-3{x}^{3}y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}-3{x}^{3}y & =y \\ {y}^{′}-3{x}^{3}y-y & =0 \\ {y}^{′}-(3{x}^{3}+1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}-3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

## Original q-331742

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+2y=y$
- ${y}^{′}+2y=x$
- ${y}^{′}+2y=0$

Bank: II only, I, II, and III, III only, I and II only, I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+2y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+2y & =y \\ {y}^{′}+2y-y & =0 \\ {y}^{′}+y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+2y=x.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=x$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+2y=0.
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II only."

### Generated variant (observed_q-331742)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+7y=4y$
- ${y}^{′}+7y=-8{x}^{2}$
- ${y}^{′}+7y=0$

- III only
- I, II, and III
- II only
- I only
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+7y=4y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+7y & =4y \\ {y}^{′}+7y-4y & =0 \\ {y}^{′}+3y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+7y=-8{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7y=0.
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II only."

### Generated variant (observed_q-331742)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+3y=5y$
- ${y}^{′}+3y=-7{x}^{2}$
- ${y}^{′}+3y=0$

- III only
- I and II only
- I only
- II only
- I, II, and III

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+3y=5y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+3y & =5y \\ {y}^{′}+3y-5y & =0 \\ {y}^{′}-2y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{y}^{′}+3y=-7{x}^{2}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7{x}^{2}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3y=0.
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II only."

## Original q-331743

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+{x}^{2}y=-2$
- ${y}^{′}+{x}^{2}y=y$
- ${y}^{′}+{x}^{2}y=0$

Bank: III only, I and II only, I, II, and III, II only, I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+{x}^{2}y=-2.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-2$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+{x}^{2}y=y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+{x}^{2}y & =y \\ {y}^{′}+{x}^{2}y-y & =0 \\ {y}^{′}+({x}^{2}-1)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331743)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+7{x}^{2}y=-8$
- ${y}^{′}+7{x}^{2}y=3y$
- ${y}^{′}+7{x}^{2}y=0$

- I, II, and III
- I and II only
- III only
- I only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+7{x}^{2}y=-8.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-8$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+7{x}^{2}y=3y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+7{x}^{2}y & =3y \\ {y}^{′}+7{x}^{2}y-3y & =0 \\ {y}^{′}+(7{x}^{2}-3)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+7{x}^{2}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

### Generated variant (observed_q-331743)

Which of the following first-order linear differential equations are inhomogeneous?

- ${y}^{′}+3{x}^{3}y=-7$
- ${y}^{′}+3{x}^{3}y=3y$
- ${y}^{′}+3{x}^{3}y=0$

- I, II, and III
- II only
- I only
- III only
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{y}^{′}+3{x}^{3}y=-7.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)=-7$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{y}^{′}+3{x}^{3}y=3y.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{y}^{′}+3{x}^{3}y & =3y \\ {y}^{′}+3{x}^{3}y-3y & =0 \\ {y}^{′}+(3{x}^{3}-3)y & =0.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{y}^{′}+3{x}^{3}y=0.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

## Authored missing hard level

Which of the following first-order linear differential equations are inhomogeneous?

- $2{y}^{′}-{x}^{3}y+2{x}^{2}=3y+2{x}^{2}$
- $4{y}^{′}+5xy-x=4y+4x$
- $3{y}^{′}-4{x}^{3}y-{x}^{3}=-y-{x}^{3}$

- III only
- I, II, and III
- II only
- I only
- I and II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
2{y}^{′}-{x}^{3}y+2{x}^{2}=3y+2{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $2$:

$$
\begin{aligned}2{y}^{′}-{x}^{3}y+2{x}^{2} & =3y+2{x}^{2} \\ 2{y}^{′}-{x}^{3}y-3y+2{x}^{2} & =2{x}^{2} \\ 2{y}^{′}+(-{x}^{3}-3)y & =0 \\ {y}^{′}+\frac{-{x}^{3}-3}{2}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
4{y}^{′}+5xy-x=4y+4x.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}+5xy-x & =4y+4x \\ 4{y}^{′}+5xy-4y-x & =4x \\ 4{y}^{′}+(5x-4)y & =5x \\ {y}^{′}+\frac{5x-4}{4}y & =\frac{5x}{4}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{5x}{4}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
3{y}^{′}-4{x}^{3}y-{x}^{3}=-y-{x}^{3}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}-4{x}^{3}y-{x}^{3} & =-y-{x}^{3} \\ 3{y}^{′}-4{x}^{3}y+y-{x}^{3} & =-{x}^{3} \\ 3{y}^{′}+(-4{x}^{3}+1)y & =0 \\ {y}^{′}+\frac{-4{x}^{3}+1}{3}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "II only."

Which of the following first-order linear differential equations are inhomogeneous?

- $4{y}^{′}-4{x}^{2}y+5{x}^{2}=3y-4{x}^{2}$
- $3{y}^{′}-4{x}^{2}y+2{x}^{2}=-5y+2{x}^{2}$
- $2{y}^{′}+3{x}^{2}y+2{x}^{3}=-2y+2{x}^{3}$

- III only
- I and II only
- I, II, and III
- I only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
4{y}^{′}-4{x}^{2}y+5{x}^{2}=3y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}-4{x}^{2}y+5{x}^{2} & =3y-4{x}^{2} \\ 4{y}^{′}-4{x}^{2}y-3y+5{x}^{2} & =-4{x}^{2} \\ 4{y}^{′}+(-4{x}^{2}-3)y & =-9{x}^{2} \\ {y}^{′}+\frac{-4{x}^{2}-3}{4}y & =\frac{-9{x}^{2}}{4}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{-9{x}^{2}}{4}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
3{y}^{′}-4{x}^{2}y+2{x}^{2}=-5y+2{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}-4{x}^{2}y+2{x}^{2} & =-5y+2{x}^{2} \\ 3{y}^{′}-4{x}^{2}y+5y+2{x}^{2} & =2{x}^{2} \\ 3{y}^{′}+(-4{x}^{2}+5)y & =0 \\ {y}^{′}+\frac{-4{x}^{2}+5}{3}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
2{y}^{′}+3{x}^{2}y+2{x}^{3}=-2y+2{x}^{3}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $2$:

$$
\begin{aligned}2{y}^{′}+3{x}^{2}y+2{x}^{3} & =-2y+2{x}^{3} \\ 2{y}^{′}+3{x}^{2}y+2y+2{x}^{3} & =2{x}^{3} \\ 2{y}^{′}+(3{x}^{2}+2)y & =0 \\ {y}^{′}+\frac{3{x}^{2}+2}{2}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

Which of the following first-order linear differential equations are inhomogeneous?

- $3{y}^{′}-{x}^{3}y-4{x}^{2}=-y+5{x}^{2}$
- $5{y}^{′}-{x}^{2}y-4{x}^{2}=2y-4{x}^{2}$
- $4{y}^{′}-2{x}^{2}y-4{x}^{2}=y-4{x}^{2}$

- I, II, and III
- III only
- I and II only
- II only
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
3{y}^{′}-{x}^{3}y-4{x}^{2}=-y+5{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}-{x}^{3}y-4{x}^{2} & =-y+5{x}^{2} \\ 3{y}^{′}-{x}^{3}y+y-4{x}^{2} & =5{x}^{2} \\ 3{y}^{′}+(-{x}^{3}+1)y & =9{x}^{2} \\ {y}^{′}+\frac{-{x}^{3}+1}{3}y & =\frac{9{x}^{2}}{3}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{9{x}^{2}}{3}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
5{y}^{′}-{x}^{2}y-4{x}^{2}=2y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $5$:

$$
\begin{aligned}5{y}^{′}-{x}^{2}y-4{x}^{2} & =2y-4{x}^{2} \\ 5{y}^{′}-{x}^{2}y-2y-4{x}^{2} & =-4{x}^{2} \\ 5{y}^{′}+(-{x}^{2}-2)y & =0 \\ {y}^{′}+\frac{-{x}^{2}-2}{5}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
4{y}^{′}-2{x}^{2}y-4{x}^{2}=y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}-2{x}^{2}y-4{x}^{2} & =y-4{x}^{2} \\ 4{y}^{′}-2{x}^{2}y-y-4{x}^{2} & =-4{x}^{2} \\ 4{y}^{′}+(-2{x}^{2}-1)y & =0 \\ {y}^{′}+\frac{-2{x}^{2}-1}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

Which of the following first-order linear differential equations are inhomogeneous?

- $2{y}^{′}+4xy-5{x}^{2}=2y+5{x}^{2}$
- $4{y}^{′}+5xy+4{x}^{2}=5y+4{x}^{2}$
- $4{y}^{′}+2{x}^{2}y-4x=-y-4x$

- II only
- I and II only
- III only
- I, II, and III
- I only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
2{y}^{′}+4xy-5{x}^{2}=2y+5{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $2$:

$$
\begin{aligned}2{y}^{′}+4xy-5{x}^{2} & =2y+5{x}^{2} \\ 2{y}^{′}+4xy-2y-5{x}^{2} & =5{x}^{2} \\ 2{y}^{′}+(4x-2)y & =10{x}^{2} \\ {y}^{′}+\frac{4x-2}{2}y & =\frac{10{x}^{2}}{2}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{10{x}^{2}}{2}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
4{y}^{′}+5xy+4{x}^{2}=5y+4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}+5xy+4{x}^{2} & =5y+4{x}^{2} \\ 4{y}^{′}+5xy-5y+4{x}^{2} & =4{x}^{2} \\ 4{y}^{′}+(5x-5)y & =0 \\ {y}^{′}+\frac{5x-5}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
4{y}^{′}+2{x}^{2}y-4x=-y-4x.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}+2{x}^{2}y-4x & =-y-4x \\ 4{y}^{′}+2{x}^{2}y+y-4x & =-4x \\ 4{y}^{′}+(2{x}^{2}+1)y & =0 \\ {y}^{′}+\frac{2{x}^{2}+1}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."

Which of the following first-order linear differential equations are inhomogeneous?

- $3{y}^{′}-{x}^{3}y-4{x}^{2}=-y-4{x}^{2}$
- $4{y}^{′}+3{x}^{3}y-4{x}^{2}=2y+4{x}^{2}$
- $4{y}^{′}-2{x}^{2}y-4{x}^{2}=y-4{x}^{2}$

- I only
- III only
- I and II only
- I, II, and III
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
3{y}^{′}-{x}^{3}y-4{x}^{2}=-y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}-{x}^{3}y-4{x}^{2} & =-y-4{x}^{2} \\ 3{y}^{′}-{x}^{3}y+y-4{x}^{2} & =-4{x}^{2} \\ 3{y}^{′}+(-{x}^{3}+1)y & =0 \\ {y}^{′}+\frac{-{x}^{3}+1}{3}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
4{y}^{′}+3{x}^{3}y-4{x}^{2}=2y+4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}+3{x}^{3}y-4{x}^{2} & =2y+4{x}^{2} \\ 4{y}^{′}+3{x}^{3}y-2y-4{x}^{2} & =4{x}^{2} \\ 4{y}^{′}+(3{x}^{3}-2)y & =8{x}^{2} \\ {y}^{′}+\frac{3{x}^{3}-2}{4}y & =\frac{8{x}^{2}}{4}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{8{x}^{2}}{4}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
4{y}^{′}-2{x}^{2}y-4{x}^{2}=y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}-2{x}^{2}y-4{x}^{2} & =y-4{x}^{2} \\ 4{y}^{′}-2{x}^{2}y-y-4{x}^{2} & =-4{x}^{2} \\ 4{y}^{′}+(-2{x}^{2}-1)y & =0 \\ {y}^{′}+\frac{-2{x}^{2}-1}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "II only."

Which of the following first-order linear differential equations are inhomogeneous?

- $2{y}^{′}+4xy-5{x}^{2}=2y-5{x}^{2}$
- $3{y}^{′}+5{x}^{2}y+4{x}^{2}=-4y-{x}^{2}$
- $4{y}^{′}-xy+2{x}^{2}=y+2{x}^{2}$

- I, II, and III
- I and II only
- III only
- I only
- II only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
2{y}^{′}+4xy-5{x}^{2}=2y-5{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $2$:

$$
\begin{aligned}2{y}^{′}+4xy-5{x}^{2} & =2y-5{x}^{2} \\ 2{y}^{′}+4xy-2y-5{x}^{2} & =-5{x}^{2} \\ 2{y}^{′}+(4x-2)y & =0 \\ {y}^{′}+\frac{4x-2}{2}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
3{y}^{′}+5{x}^{2}y+4{x}^{2}=-4y-{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}+5{x}^{2}y+4{x}^{2} & =-4y-{x}^{2} \\ 3{y}^{′}+5{x}^{2}y+4y+4{x}^{2} & =-{x}^{2} \\ 3{y}^{′}+(5{x}^{2}+4)y & =-5{x}^{2} \\ {y}^{′}+\frac{5{x}^{2}+4}{3}y & =\frac{-5{x}^{2}}{3}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{-5{x}^{2}}{3}$, which is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
4{y}^{′}-xy+2{x}^{2}=y+2{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}-xy+2{x}^{2} & =y+2{x}^{2} \\ 4{y}^{′}-xy-y+2{x}^{2} & =2{x}^{2} \\ 4{y}^{′}+(-x-1)y & =0 \\ {y}^{′}+\frac{-x-1}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

Therefore, the correct answer is "II only."

Which of the following first-order linear differential equations are inhomogeneous?

- $3{y}^{′}-{x}^{3}y-4{x}^{2}=-y-4{x}^{2}$
- $5{y}^{′}-{x}^{2}y-4{x}^{2}=2y-4{x}^{2}$
- $3{y}^{′}+{x}^{2}y-4{x}^{2}=-y+{x}^{2}$

- I and III only
- I only
- I, II, and III
- II only
- III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
3{y}^{′}-{x}^{3}y-4{x}^{2}=-y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}-{x}^{3}y-4{x}^{2} & =-y-4{x}^{2} \\ 3{y}^{′}-{x}^{3}y+y-4{x}^{2} & =-4{x}^{2} \\ 3{y}^{′}+(-{x}^{3}+1)y & =0 \\ {y}^{′}+\frac{-{x}^{3}+1}{3}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
5{y}^{′}-{x}^{2}y-4{x}^{2}=2y-4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $5$:

$$
\begin{aligned}5{y}^{′}-{x}^{2}y-4{x}^{2} & =2y-4{x}^{2} \\ 5{y}^{′}-{x}^{2}y-2y-4{x}^{2} & =-4{x}^{2} \\ 5{y}^{′}+(-{x}^{2}-2)y & =0 \\ {y}^{′}+\frac{-{x}^{2}-2}{5}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
3{y}^{′}+{x}^{2}y-4{x}^{2}=-y+{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $3$:

$$
\begin{aligned}3{y}^{′}+{x}^{2}y-4{x}^{2} & =-y+{x}^{2} \\ 3{y}^{′}+{x}^{2}y+y-4{x}^{2} & ={x}^{2} \\ 3{y}^{′}+({x}^{2}+1)y & =5{x}^{2} \\ {y}^{′}+\frac{{x}^{2}+1}{3}y & =\frac{5{x}^{2}}{3}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{5{x}^{2}}{3}$, which is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."

Which of the following first-order linear differential equations are inhomogeneous?

- $2{y}^{′}+4xy-5{x}^{2}=2y-5{x}^{2}$
- $4{y}^{′}+5xy+4{x}^{2}=5y+4{x}^{2}$
- $5{y}^{′}+{x}^{2}y-4{x}^{2}=-4y+{x}^{2}$

- II only
- I, II, and III
- I only
- I and III only
- III only

A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
2{y}^{′}+4xy-5{x}^{2}=2y-5{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $2$:

$$
\begin{aligned}2{y}^{′}+4xy-5{x}^{2} & =2y-5{x}^{2} \\ 2{y}^{′}+4xy-2y-5{x}^{2} & =-5{x}^{2} \\ 2{y}^{′}+(4x-2)y & =0 \\ {y}^{′}+\frac{4x-2}{2}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
4{y}^{′}+5xy+4{x}^{2}=5y+4{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $4$:

$$
\begin{aligned}4{y}^{′}+5xy+4{x}^{2} & =5y+4{x}^{2} \\ 4{y}^{′}+5xy-5y+4{x}^{2} & =4{x}^{2} \\ 4{y}^{′}+(5x-5)y & =0 \\ {y}^{′}+\frac{5x-5}{4}y & =0.\end{aligned}
$$

The forcing function is $Q(x)=0$, which is identically zero. Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
5{y}^{′}+{x}^{2}y-4{x}^{2}=-4y+{x}^{2}.
$$

We collect the $y$-terms on the left side and the terms involving only $x$ on the right side, then divide through by $5$:

$$
\begin{aligned}5{y}^{′}+{x}^{2}y-4{x}^{2} & =-4y+{x}^{2} \\ 5{y}^{′}+{x}^{2}y+4y-4{x}^{2} & ={x}^{2} \\ 5{y}^{′}+({x}^{2}+4)y & =5{x}^{2} \\ {y}^{′}+\frac{{x}^{2}+4}{5}y & =\frac{5{x}^{2}}{5}.\end{aligned}
$$

The forcing function is $Q(x)=\frac{5{x}^{2}}{5}$, which is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."
