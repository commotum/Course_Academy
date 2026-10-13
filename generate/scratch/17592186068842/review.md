# Separation generator review

Original replays retain source wording and stages. Generated variants repair “differentiable” to “differential”; the hard family is authored, with no observed hard difficulty label. Equivalent unseparated source equations are intentionally wrong under the separation-form response criterion.

## Original replay q-154678

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x{y}^{2}}{x+1}
$$

- $\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+1}$
- ${y}^{2}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+1}$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{x+1}$
- $(x+1)\cdot \frac{\text{d}y}{\text{d}x}=x{y}^{2}$
- $\frac{x+1}{x}\cdot \frac{\text{d}y}{\text{d}x}={y}^{2}$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=(\frac{x}{x+1})\cdot {y}^{2}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+1}
$$

## Generated rational_product seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{xy}{x+4}
$$

Work on a domain where all displayed expressions are defined.

- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+4}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+4}$
- $(x+4)\cdot \frac{\text{d}y}{\text{d}x}=xy$
- $\frac{x+4}{x}\cdot \frac{\text{d}y}{\text{d}x}=y$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{y}{x+4}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=(\frac{x}{x+4})\cdot y.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+4}
$$

## Generated rational_product seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{xy}{x+3}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+3}$
- $(x+3)\cdot \frac{\text{d}y}{\text{d}x}=xy$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+3}$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{y}{x+3}$
- $\frac{x+3}{x}\cdot \frac{\text{d}y}{\text{d}x}=y$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=(\frac{x}{x+3})\cdot y.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{x+3}
$$

## Original replay q-157692

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={e}^{x+y}
$$

- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{-y}$
- ${e}^{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- ${e}^{x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{y}$
- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{y}$
- ${e}^{-y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{x}\cdot {e}^{y}
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{e}^{y}}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x},
$$

or, equivalently,

$$
{e}^{-y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}.
$$

## Generated exp_sum seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={e}^{x+4y}
$$

Work on a domain where all displayed expressions are defined.

- ${e}^{4y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{-4y}$
- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{4y}$
- ${e}^{-4y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- ${e}^{x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{4y}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{x}\cdot {e}^{4y}
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{e}^{4y}}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x},
$$

or, equivalently,

$$
{e}^{-4y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}.
$$

## Generated exp_sum seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={e}^{x+3y}
$$

Work on a domain where all displayed expressions are defined.

- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{-3y}$
- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{3y}$
- ${e}^{3y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- ${e}^{x}\cdot \frac{\text{d}y}{\text{d}x}={e}^{3y}$
- ${e}^{-3y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{x}\cdot {e}^{3y}
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{e}^{3y}}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x},
$$

or, equivalently,

$$
{e}^{-3y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}.
$$

## Original replay q-158022

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=y{e}^{x}
$$

- ${e}^{-x}\cdot \frac{\text{d}y}{\text{d}x}=y$
- $\frac{{e}^{-x}}{y}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $y\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}$
- ${e}^{x}\cdot \frac{\text{d}y}{\text{d}x}=y$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{x}\cdot y.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{x}
$$

## Generated exp_product seed 33

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=y{e}^{5x}
$$

Work on a domain where all displayed expressions are defined.

- $y\cdot \frac{\text{d}y}{\text{d}x}={e}^{5x}$
- ${e}^{-5x}\cdot \frac{\text{d}y}{\text{d}x}=y$
- ${e}^{5x}\cdot \frac{\text{d}y}{\text{d}x}=y$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{5x}$
- $\frac{{e}^{-5x}}{y}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{5x}\cdot y.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{5x}
$$

## Generated exp_product seed 50

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=y{e}^{4x}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{{e}^{-4x}}{y}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $y\cdot \frac{\text{d}y}{\text{d}x}={e}^{4x}$
- ${e}^{4x}\cdot \frac{\text{d}y}{\text{d}x}=y$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{4x}$
- ${e}^{-4x}\cdot \frac{\text{d}y}{\text{d}x}=y$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={e}^{4x}\cdot y.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={e}^{4x}
$$

## Original replay q-158023

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=x+x{y}^{2}
$$

- $\frac{x}{1+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{1+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=x$
- $(1+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=x$
- $(x+x{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{x+x{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot (1+{y}^{2}).
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{1+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Generated polynomial_factor seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=x+4x{y}^{4}
$$

Work on a domain where all displayed expressions are defined.

- $(x+4x{y}^{4})\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{x}{1+4{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{x+4x{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $(1+4{y}^{4})\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{1+4{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=x$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot (1+4{y}^{4}).
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{1+4{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Generated polynomial_factor seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=x+3x{y}^{2}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{1}{1+3{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{x+3x{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $(x+3x{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=1$
- $(1+3{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{x}{1+3{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot (1+3{y}^{2}).
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{1+3{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Original replay q-158024

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={3}^{x-2y}
$$

- ${3}^{2y-x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- ${3}^{-2y}\cdot \frac{\text{d}y}{\text{d}x}={3}^{x}$
- ${3}^{x}\cdot \frac{\text{d}y}{\text{d}x}={3}^{-2y}$
- ${3}^{2y}\cdot \frac{\text{d}y}{\text{d}x}={3}^{x}$
- ${3}^{-x}\cdot \frac{\text{d}y}{\text{d}x}={3}^{-2y}$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={3}^{x}\cdot {3}^{-2y}
$$

Therefore, we separate the variables as follows:

$$
{3}^{2y}\cdot \frac{\text{d}y}{\text{d}x}={3}^{x}\,.
$$

## Generated base_exp seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={2}^{4x-y}
$$

Work on a domain where all displayed expressions are defined.

- ${2}^{y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}$
- ${2}^{4x}\cdot \frac{\text{d}y}{\text{d}x}={2}^{-y}$
- ${2}^{y-4x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- ${2}^{-y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}$
- ${2}^{-4x}\cdot \frac{\text{d}y}{\text{d}x}={2}^{-y}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={2}^{4x}\cdot {2}^{-y}
$$

Therefore, we separate the variables as follows:

$$
{2}^{y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}\,.
$$

## Generated base_exp seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={2}^{3x-4y}
$$

Work on a domain where all displayed expressions are defined.

- ${2}^{-4y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}$
- ${2}^{4y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}$
- ${2}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}={2}^{-4y}$
- ${2}^{4y-3x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- ${2}^{3x}\cdot \frac{\text{d}y}{\text{d}x}={2}^{-4y}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={2}^{3x}\cdot {2}^{-4y}
$$

Therefore, we separate the variables as follows:

$$
{2}^{4y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}\,.
$$

## Original replay q-158025

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{{2}^{x}}{{y}^{3}}
$$

- $\frac{1}{{y}^{3}}\cdot \frac{\text{d}y}{\text{d}x}={2}^{x}$
- ${2}^{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{3}}$
- ${y}^{3}\cdot \frac{\text{d}y}{\text{d}x}={2}^{x}$
- ${2}^{-x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{3}}$
- $\frac{{y}^{3}}{{2}^{x}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={2}^{x}\cdot \frac{1}{{y}^{3}}.
$$

Therefore, we separate the variables as follows:

$$
{y}^{3}\cdot \frac{\text{d}y}{\text{d}x}={2}^{x}
$$

## Generated exp_quotient seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{{2}^{4x}}{y}
$$

Work on a domain where all displayed expressions are defined.

- ${2}^{-4x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $y\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}$
- ${2}^{4x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $\frac{y}{{2}^{4x}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={2}^{4x}\cdot \frac{1}{y}.
$$

Therefore, we separate the variables as follows:

$$
y\cdot \frac{\text{d}y}{\text{d}x}={2}^{4x}
$$

## Generated exp_quotient seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{{2}^{3x}}{{y}^{4}}
$$

Work on a domain where all displayed expressions are defined.

- ${2}^{3x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{4}}$
- ${2}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{4}}$
- $\frac{{y}^{4}}{{2}^{3x}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}$
- ${y}^{4}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}={2}^{3x}\cdot \frac{1}{{y}^{4}}.
$$

Therefore, we separate the variables as follows:

$$
{y}^{4}\cdot \frac{\text{d}y}{\text{d}x}={2}^{3x}
$$

## Original replay q-158026

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{1+{y}^{2}}}{x}
$$

- $\sqrt{1+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$
- $x\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{1+{y}^{2}}$
- $\frac{x}{\sqrt{1+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{\sqrt{1+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{1+{y}^{2}}$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{x}\cdot \sqrt{1+{y}^{2}}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{\sqrt{1+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}
$$

## Generated sqrt_quotient seed 33

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{5+{y}^{2}}}{x}
$$

Work on a domain where all displayed expressions are defined.

- $x\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{5+{y}^{2}}$
- $\frac{x}{\sqrt{5+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{\sqrt{5+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{5+{y}^{2}}$
- $\sqrt{5+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{x}\cdot \sqrt{5+{y}^{2}}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{\sqrt{5+{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}
$$

## Generated sqrt_quotient seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{1+{y}^{4}}}{x}
$$

Work on a domain where all displayed expressions are defined.

- $x\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{1+{y}^{4}}$
- $\frac{1}{\sqrt{1+{y}^{4}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\sqrt{1+{y}^{4}}$
- $\sqrt{1+{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}$
- $\frac{x}{\sqrt{1+{y}^{4}}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\frac{1}{x}\cdot \sqrt{1+{y}^{4}}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{\sqrt{1+{y}^{4}}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{x}
$$

## Original replay q-158027

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={y}^{2}\operatorname{sin}⁡x
$$

- ${y}^{2}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡x}$
- $\operatorname{csc}⁡x\text{ }\cdot \frac{\text{d}y}{\text{d}x}={y}^{2}$
- $\operatorname{sin}⁡x\cdot \frac{\text{d}y}{\text{d}x}={y}^{2}$
- $\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x$
- $\frac{\operatorname{csc}⁡x}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x\cdot {y}^{2}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x
$$

## Generated trig_product seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={y}^{4}\operatorname{sin}⁡x
$$

Work on a domain where all displayed expressions are defined.

- $\operatorname{csc}⁡x\text{ }\cdot \frac{\text{d}y}{\text{d}x}={y}^{4}$
- ${y}^{4}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡x}$
- $\frac{1}{{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x$
- $\frac{\operatorname{csc}⁡x}{{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\operatorname{sin}⁡x\cdot \frac{\text{d}y}{\text{d}x}={y}^{4}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x\cdot {y}^{4}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x
$$

## Generated trig_product seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}={y}^{3}\operatorname{sin}⁡x
$$

Work on a domain where all displayed expressions are defined.

- ${y}^{3}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{\operatorname{sin}⁡x}$
- $\frac{1}{{y}^{3}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x$
- $\operatorname{csc}⁡x\text{ }\cdot \frac{\text{d}y}{\text{d}x}={y}^{3}$
- $\operatorname{sin}⁡x\cdot \frac{\text{d}y}{\text{d}x}={y}^{3}$
- $\frac{\operatorname{csc}⁡x}{{y}^{3}}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x\cdot {y}^{3}.
$$

Therefore, we separate the variables as follows:

$$
\frac{1}{{y}^{3}}\cdot \frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡x
$$

## Original replay q-158030

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x}{y}
$$

- $\frac{y}{x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $x\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=x$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot \frac{1}{y}.
$$

Therefore, we separate the variables as follows:

$$
y\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Generated simple_quotient seed 33

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x}{{y}^{2}}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{1}{{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=x$
- ${y}^{2}\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{2}}$
- $\frac{{y}^{2}}{x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $x\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{2}}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot \frac{1}{{y}^{2}}.
$$

Therefore, we separate the variables as follows:

$$
{y}^{2}\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Generated simple_quotient seed 50

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x}{{y}^{4}}
$$

Work on a domain where all displayed expressions are defined.

- $x\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{4}}$
- ${y}^{4}\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{{y}^{4}}\cdot \frac{\text{d}y}{\text{d}x}=x$
- $\frac{1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{{y}^{4}}$
- $\frac{{y}^{4}}{x}\cdot \frac{\text{d}y}{\text{d}x}=1$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\frac{\text{d}y}{\text{d}x}=x\cdot \frac{1}{{y}^{4}}.
$$

Therefore, we separate the variables as follows:

$$
{y}^{4}\cdot \frac{\text{d}y}{\text{d}x}=x
$$

## Original replay q-158032

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{3x}{5xy+y}
$$

- $\frac{5xy+y}{3x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{5x+1}{3x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{5x+1}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{5x+1}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{5x+1}{3x}$

A differentiable equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differentiable equation is separable since it can be written as

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3x}{(5x+1)y} \\  & =\frac{3x}{5x+1}\cdot \frac{1}{y}.\end{aligned}
$$

Therefore, we separate the variables as follows:

$$
y\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{5x+1}
$$

## Generated rational_factor seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x}{4xy+y}
$$

Work on a domain where all displayed expressions are defined.

- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{4x+1}$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{4x+1}$
- $\frac{4xy+y}{x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{4x+1}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x+1}{x}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{x}{(4x+1)y} \\  & =\frac{x}{4x+1}\cdot \frac{1}{y}.\end{aligned}
$$

Therefore, we separate the variables as follows:

$$
y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{4x+1}
$$

## Generated rational_factor seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{x}{3xy+4y}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{3x+4}{x}\cdot \frac{\text{d}y}{\text{d}x}=\frac{1}{y}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{3x+4}$
- $y\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x+4}{x}$
- $\frac{3xy+4y}{x}\cdot \frac{\text{d}y}{\text{d}x}=1$
- $\frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{3x+4}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{x}{(3x+4)y} \\  & =\frac{x}{3x+4}\cdot \frac{1}{y}.\end{aligned}
$$

Therefore, we separate the variables as follows:

$$
y\cdot \frac{\text{d}y}{\text{d}x}=\frac{x}{3x+4}
$$

## Authored missing-hard seed 31

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{4x}{4x+2x{y}^{2}+6+3{y}^{2}}
$$

Work on a domain where all displayed expressions are defined.

- $(2x+3)\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x}{2+{y}^{2}}$
- $\frac{1}{2x+3}\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x}{2+{y}^{2}}$
- $(2+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{2x+3}{4x}$
- $\frac{1}{2+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x}{2x+3}$
- $(2+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x}{2x+3}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{4x}{(2x+3)(2+{y}^{2})} \\  & =\frac{4x}{2x+3}\cdot \frac{1}{2+{y}^{2}}.\end{aligned}
$$

Therefore, we separate the variables as follows:

$$
(2+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{4x}{2x+3}
$$

## Authored missing-hard seed 49

Separate the variables in the following differential equation: 

$$
\frac{\text{d}y}{\text{d}x}=\frac{3x}{9x+3x{y}^{2}+6+2{y}^{2}}
$$

Work on a domain where all displayed expressions are defined.

- $\frac{1}{3x+2}\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{3+{y}^{2}}$
- $(3+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{3x+2}$
- $(3x+2)\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{3+{y}^{2}}$
- $\frac{1}{3+{y}^{2}}\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{3x+2}$
- $(3+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x+2}{3x}$

A differential equation is *separable* if it can be written in the form

$$
\frac{\text{d}y}{\text{d}x}=h(x)g(y).
$$

If an equation is separable, we say that the variables are *separated* when it is written in the form

$$
\frac{1}{g(y)}\cdot \frac{\text{d}y}{\text{d}x}=h(x).
$$

Notice that our differential equation is separable since it can be written as

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3x}{(3x+2)(3+{y}^{2})} \\  & =\frac{3x}{3x+2}\cdot \frac{1}{3+{y}^{2}}.\end{aligned}
$$

Therefore, we separate the variables as follows:

$$
(3+{y}^{2})\cdot \frac{\text{d}y}{\text{d}x}=\frac{3x}{3x+2}
$$
