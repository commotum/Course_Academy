# Review: exact originals and generated variants

Raw source anomalies are explicitly ineligible. Normal repairs are labeled separately. Hard examples are authored. Every source bank and both solution methods are shown.

## exact raw source replay — q-8739 / quadratic_product

Parameters: `{"sx": 1, "sy": 1}`; profile `raw`; eligible for learning: False.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference **absent**.

- $\frac{dy}{dx} = \frac{x^{2}y}{x^{2} + y^{2}}$
- $\frac{dy}{dx} = \frac{2xy}{x^{2} + y^{2}}$
- $\frac{dy}{dx} = \frac{x^{2}y^{2}}{x^{2} + y^{2}}$
- $\frac{dy}{dx} = \frac{xy^{2}}{x^{2} + y^{2}}$
- $\frac{dy}{dx} = \frac{xy}{x + y}$

Field 1 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{x{y}^{2}}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{x+y}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}{y}^{2}}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{2xy}{{x}^{2}+{y}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}y}{{x}^{2}+{y}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{2xy}{{x}^{2}+{y}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{2xy}{{x}^{2}+{y}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{2xy}{{x}^{2}+{y}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{2(tx)(ty)}{(tx)^{2}+(ty)^{2}} \\  & =\frac{{t}^{2}\cdot 2xy}{{t}^{2}{x}^{2}+{t}^{2}{y}^{2}} \\  & =\text{ }\frac{{t}^{2}\cdot 2xy}{{t}^{2}({x}^{2}+{y}^{2})} \\  & =\frac{2xy}{{x}^{2}+{y}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## supported normal at source parameters — q-8739 / quadratic_product

Parameters: `{"sx": 1, "sy": 1}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}{y}^{2}}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{x+y}$
- $\frac{\text{d}y}{\text{d}x}=\frac{x{y}^{2}}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}y}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{2xy}{{x}^{2}+{y}^{2}}$ **correct**

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{2xy}{{x}^{2}+{y}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{2xy}{{x}^{2}+{y}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{2xy}{{x}^{2}+{y}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{2(tx)(ty)}{(tx)^{2}+(ty)^{2}} \\  & =\frac{{t}^{2}\cdot 2xy}{{t}^{2}{x}^{2}+{t}^{2}{y}^{2}} \\  & =\text{ }\frac{{t}^{2}\cdot 2xy}{{t}^{2}({x}^{2}+{y}^{2})} \\  & =\frac{2xy}{{x}^{2}+{y}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## exact raw source replay — q-14319 / cubic_quotient

Parameters: `{"sx": 1, "sy": 1}`; profile `raw`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}x-{x}^{2}}{{y}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3xy+xy}{{y}^{2}-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{3}-{x}^{2}y+{x}^{3}}{{y}^{3}+1}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}-x{y}^{2}+{y}^{2}}{1+{x}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(tx)^{3}-3(tx)^{2}(ty)+(tx)(ty)^{2}}{(ty)^{3}+(tx)^{3}} \\  & =\frac{{t}^{3}({x}^{3})-{t}^{3}(3{x}^{2}y)+{t}^{3}(x{y}^{2})}{{t}^{3}{y}^{3}+{t}^{3}{x}^{3}} \\  & =\frac{{t}^{3}({x}^{3}-3{x}^{2}y+x{y}^{2})}{{t}^{3}({y}^{3}+{x}^{3})} \\  & =\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## supported normal at source parameters — q-14319 / cubic_quotient

Parameters: `{"sx": 1, "sy": 1}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3xy+xy}{{y}^{2}-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}x-{x}^{2}}{{y}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}-x{y}^{2}+{y}^{2}}{1+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{3}-{x}^{2}y+{x}^{3}}{{y}^{3}+1}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(tx)^{3}-3(tx)^{2}(ty)+(tx)(ty)^{2}}{(ty)^{3}+(tx)^{3}} \\  & =\frac{{t}^{3}({x}^{3})-{t}^{3}(3{x}^{2}y)+{t}^{3}(x{y}^{2})}{{t}^{3}{y}^{3}+{t}^{3}{x}^{3}} \\  & =\frac{{t}^{3}({x}^{3}-3{x}^{2}y+x{y}^{2})}{{t}^{3}({y}^{3}+{x}^{3})} \\  & =\frac{{x}^{3}-3{x}^{2}y+x{y}^{2}}{{y}^{3}+{x}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## exact raw source replay — q-8369 / quadratic_difference

Parameters: `{"sx": 1, "sy": 1}`; profile `raw`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+x}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-x}{{y}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{y-{x}^{2}}{{y}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{y-{x}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{x}^{2}+{y}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(ty)^{2}-(tx)^{2}}{(ty)^{2}+(tx)^{2}} \\  & =\frac{{t}^{2}{y}^{2}-{t}^{2}{x}^{2}}{{t}^{2}{y}^{2}+{t}^{2}{x}^{2}} \\  & =\frac{{t}^{2}({y}^{2}-{x}^{2})}{{t}^{2}({y}^{2}+{x}^{2})} \\  & =\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## supported normal at source parameters — q-8369 / quadratic_difference

Parameters: `{"sx": 1, "sy": 1}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-x}{{y}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+x}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{y-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{y-{x}^{2}}{{y}^{2}+{x}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}-{x}^{2}}{{x}^{2}+{y}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(ty)^{2}-(tx)^{2}}{(ty)^{2}+(tx)^{2}} \\  & =\frac{{t}^{2}{y}^{2}-{t}^{2}{x}^{2}}{{t}^{2}{y}^{2}+{t}^{2}{x}^{2}} \\  & =\frac{{t}^{2}({y}^{2}-{x}^{2})}{{t}^{2}({y}^{2}+{x}^{2})} \\  & =\frac{{y}^{2}-{x}^{2}}{{y}^{2}+{x}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## exact raw source replay — q-8741 / linear_not

Parameters: `{"sx": 1, "sy": 1}`; profile `raw`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=1$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}⁡y-\operatorname{ln}⁡x$
- $\frac{\text{d}y}{\text{d}x}=x$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\operatorname{arctan}⁡(\frac{x}{y})$
- $\frac{\text{d}y}{\text{d}x}=2$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=x.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=x.$

We see that it is a homogeneous polynomial of degree $1.$ Therefore, $f(x,y)$ is a homogeneous function of degree $1.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=x\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =tx=tf(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## supported normal at source parameters — q-8741 / linear_not

Parameters: `{"sx": 1, "sy": 1}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=x$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}⁡y-\operatorname{ln}⁡x$
- $\frac{\text{d}y}{\text{d}x}=1$
- $\frac{\text{d}y}{\text{d}x}=2$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{arctan}⁡(\frac{x}{y})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=x.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=x.$

We see that it is a homogeneous polynomial of degree $1.$ Therefore, $f(x,y)$ is a homogeneous function of degree $1.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=x\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =tx=tf(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## exact raw source replay — q-14322 / constant_offset_not

Parameters: `{"sx": 1, "sy": 1, "x0": 1, "y0": 2, "t": 3}`; profile `raw`; eligible for learning: False.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{x+y}{y})$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}$ **correct**
- $\frac{\text{d}y}{\text{d}x}={e}^{\operatorname{sin}⁡(\frac{x}{y})}$
- $\frac{\text{d}y}{\text{d}x}=\frac{4{x}^{2}y}{{x}^{3}+x{y}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is:

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}.$

We see that the numerator is NOT a homogeneous polynomial. Therefore, $f(x,y)$ is NOT a homogeneous function.

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

For $x=1$, $y=2$ and $t=3$, for instance, we have

$$
\begin{aligned}f(tx,ty) & =f(2\cdot 1,2\cdot 3) \\  & =f(2,6) \\  & =\frac{{2}^{2}+1}{{6}^{2}+2(6)} \\  & =\frac{5}{48}\end{aligned}
$$

and

$$
\begin{aligned}f(x,y) & =f(1,2) \\  & =\frac{{1}^{2}+1}{{2}^{2}+1(2)} \\  & =\frac{2}{6} \\  & =\frac{1}{3}.\end{aligned}
$$

In other words, there exists at least one combination of values of $x$, $y$ and $t$ for which the identity $f(tx,ty)=f(x,y)$ is not observed.

Hence, the original differential equation is  NOT homogeneous.

## supported normal at source parameters — q-14322 / constant_offset_not

Parameters: `{"sx": 1, "sy": 1, "x0": 1, "y0": 2, "t": 3}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{x+y}{y})$
- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{4{x}^{2}y}{{x}^{3}+x{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}={e}^{\operatorname{sin}⁡(\frac{x}{y})}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is:

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}.$

We see that the numerator has terms of degrees $2$ and $0$, whereas the denominator is homogeneous of degree $2$. The nonzero constant term cannot cancel against this denominator, so the scaling factors cannot cancel. Therefore, $f(x,y)$ is NOT a homogeneous function of degree zero.

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

For $x=1$, $y=2$ and $t=3$, for instance, we have

$$
\begin{aligned}f(tx,ty) & =f(3\cdot 1,3\cdot 2) \\  & =f(3,6) \\  & =\frac{{3}^{2}+1}{{6}^{2}+3(6)} \\  & =\frac{10}{54} \\  & =\frac{5}{27}\end{aligned}
$$

and

$$
\begin{aligned}f(x,y) & =f(1,2) \\  & =\frac{{1}^{2}+1}{{2}^{2}+1(2)} \\  & =\frac{2}{6} \\  & =\frac{1}{3}.\end{aligned}
$$

In other words, there exists at least one combination of values of $x$, $y$ and $t$ for which the identity $f(tx,ty)=f(x,y)$ is not observed.

Hence, the original differential equation is  NOT homogeneous.

## exact raw source replay — q-90597 / quadratic_not

Parameters: `{"sx": 1, "sy": 1}`; profile `raw`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+xy}$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{cos}⁡(\frac{x}{2y})$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{2}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{{x}^{3}}{{y}^{3}})$
- $\frac{\text{d}y}{\text{d}x}=9$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{2}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{y}^{2}}{2}=\frac{1}{2}{y}^{2}.$

We see that it is a homogeneous polynomial of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{y}^{2}}{2}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(ty)^{2}}{2} \\  & ={t}^{2}\cdot \frac{{y}^{2}}{2} \\  & ={t}^{2}f(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## supported normal at source parameters — q-90597 / quadratic_not

Parameters: `{"sx": 1, "sy": 1}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{2}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\operatorname{cos}⁡(\frac{x}{2y})$
- $\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{{x}^{2}+xy}$
- $\frac{\text{d}y}{\text{d}x}=9$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{{x}^{3}}{{y}^{3}})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{y}^{2}}{2}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{y}^{2}}{2}=\frac{1}{2}{y}^{2}.$

We see that it is a homogeneous polynomial of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{y}^{2}}{2}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(ty)^{2}}{2} \\  & ={t}^{2}\cdot \frac{{y}^{2}}{2} \\  & ={t}^{2}f(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## generated easy variant — q-8739 / quadratic_product

Parameters: `{"sx": 1, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{x(9y)}{x+(9y)}$
- $\frac{\text{d}y}{\text{d}x}=\frac{x{(9y)}^{2}}{{x}^{2}+{(9y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}{(9y)}^{2}}{{x}^{2}+{(9y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}(9y)}{{x}^{2}+{(9y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{2x(9y)}{{x}^{2}+{(9y)}^{2}}$ **correct**

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{2x(9y)}{{x}^{2}+{(9y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{2x(9y)}{{x}^{2}+{(9y)}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{2x(9y)}{{x}^{2}+{(9y)}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{2(tx)(t(9y))}{(tx)^{2}+(t(9y))^{2}} \\  & =\frac{{t}^{2}\cdot 2x(9y)}{{t}^{2}{x}^{2}+{t}^{2}{(9y)}^{2}} \\  & =\text{ }\frac{{t}^{2}\cdot 2x(9y)}{{t}^{2}({x}^{2}+{(9y)}^{2})} \\  & =\frac{2x(9y)}{{x}^{2}+{(9y)}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated easy variant — q-8739 / quadratic_product

Parameters: `{"sx": 1, "sy": 3}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{2x(3y)}{{x}^{2}+{(3y)}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}{(3y)}^{2}}{{x}^{2}+{(3y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{x{(3y)}^{2}}{{x}^{2}+{(3y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}(3y)}{{x}^{2}+{(3y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{x(3y)}{x+(3y)}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{2x(3y)}{{x}^{2}+{(3y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{2x(3y)}{{x}^{2}+{(3y)}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{2x(3y)}{{x}^{2}+{(3y)}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{2(tx)(t(3y))}{(tx)^{2}+(t(3y))^{2}} \\  & =\frac{{t}^{2}\cdot 2x(3y)}{{t}^{2}{x}^{2}+{t}^{2}{(3y)}^{2}} \\  & =\text{ }\frac{{t}^{2}\cdot 2x(3y)}{{t}^{2}({x}^{2}+{(3y)}^{2})} \\  & =\frac{2x(3y)}{{x}^{2}+{(3y)}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated easy variant — q-14319 / cubic_quotient

Parameters: `{"sx": 1, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2}}{{(9y)}^{3}+{x}^{3}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}x-{x}^{2}}{{(9y)}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3x(9y)+x(9y)}{{(9y)}^{2}-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}-x{(9y)}^{2}+{(9y)}^{2}}{1+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{3}-{x}^{2}(9y)+{x}^{3}}{{(9y)}^{3}+1}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2}}{{(9y)}^{3}+{x}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2}}{{(9y)}^{3}+{x}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2}}{{(9y)}^{3}+{x}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(tx)^{3}-3(tx)^{2}(t(9y))+(tx)(t(9y))^{2}}{(t(9y))^{3}+(tx)^{3}} \\  & =\frac{{t}^{3}({x}^{3})-{t}^{3}(3{x}^{2}(9y))+{t}^{3}(x{(9y)}^{2})}{{t}^{3}{(9y)}^{3}+{t}^{3}{x}^{3}} \\  & =\frac{{t}^{3}({x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2})}{{t}^{3}({(9y)}^{3}+{x}^{3})} \\  & =\frac{{x}^{3}-3{x}^{2}(9y)+x{(9y)}^{2}}{{(9y)}^{3}+{x}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated easy variant — q-14319 / cubic_quotient

Parameters: `{"sx": 1, "sy": 3}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{3}-{x}^{2}(3y)+{x}^{3}}{{(3y)}^{3}+1}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3x(3y)+x(3y)}{{(3y)}^{2}-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}x-{x}^{2}}{{(3y)}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}-x{(3y)}^{2}+{(3y)}^{2}}{1+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2}}{{(3y)}^{3}+{x}^{3}}$ **correct**

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2}}{{(3y)}^{3}+{x}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2}}{{(3y)}^{3}+{x}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2}}{{(3y)}^{3}+{x}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(tx)^{3}-3(tx)^{2}(t(3y))+(tx)(t(3y))^{2}}{(t(3y))^{3}+(tx)^{3}} \\  & =\frac{{t}^{3}({x}^{3})-{t}^{3}(3{x}^{2}(3y))+{t}^{3}(x{(3y)}^{2})}{{t}^{3}{(3y)}^{3}+{t}^{3}{x}^{3}} \\  & =\frac{{t}^{3}({x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2})}{{t}^{3}({(3y)}^{3}+{x}^{3})} \\  & =\frac{{x}^{3}-3{x}^{2}(3y)+x{(3y)}^{2}}{{(3y)}^{3}+{x}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated easy variant — q-8369 / quadratic_difference

Parameters: `{"sx": 1, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-x}{{(9y)}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{x}^{2}}{{(9y)}^{2}+x}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{x}^{2}}{{(9y)}^{2}+{x}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{x}^{2}}{(9y)-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{(9y)-{x}^{2}}{{(9y)}^{2}+{x}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{x}^{2}}{{x}^{2}+{(9y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(9y)}^{2}-{x}^{2}}{{(9y)}^{2}+{x}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(9y)}^{2}-{x}^{2}}{{(9y)}^{2}+{x}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(9y))^{2}-(tx)^{2}}{(t(9y))^{2}+(tx)^{2}} \\  & =\frac{{t}^{2}{(9y)}^{2}-{t}^{2}{x}^{2}}{{t}^{2}{(9y)}^{2}+{t}^{2}{x}^{2}} \\  & =\frac{{t}^{2}({(9y)}^{2}-{x}^{2})}{{t}^{2}({(9y)}^{2}+{x}^{2})} \\  & =\frac{{(9y)}^{2}-{x}^{2}}{{(9y)}^{2}+{x}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated easy variant — q-8369 / quadratic_difference

Parameters: `{"sx": 1, "sy": 3}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{(3y)-{x}^{2}}{{(3y)}^{2}+{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}-{x}^{2}}{{(3y)}^{2}+{x}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}-{x}^{2}}{{(3y)}^{2}+x}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}-{x}^{2}}{(3y)-{x}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}-x}{{(3y)}^{2}+{x}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}-{x}^{2}}{{x}^{2}+{(3y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(3y)}^{2}-{x}^{2}}{{(3y)}^{2}+{x}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(3y)}^{2}-{x}^{2}}{{(3y)}^{2}+{x}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(3y))^{2}-(tx)^{2}}{(t(3y))^{2}+(tx)^{2}} \\  & =\frac{{t}^{2}{(3y)}^{2}-{t}^{2}{x}^{2}}{{t}^{2}{(3y)}^{2}+{t}^{2}{x}^{2}} \\  & =\frac{{t}^{2}({(3y)}^{2}-{x}^{2})}{{t}^{2}({(3y)}^{2}+{x}^{2})} \\  & =\frac{{(3y)}^{2}-{x}^{2}}{{(3y)}^{2}+{x}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated moderate variant — q-8741 / linear_not

Parameters: `{"sx": 8, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}⁡(9y)-\operatorname{ln}⁡(8x)$
- $\frac{\text{d}y}{\text{d}x}=1$
- $\frac{\text{d}y}{\text{d}x}=(8x)$ **correct**
- $\frac{\text{d}y}{\text{d}x}=2$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{arctan}⁡(\frac{(8x)}{(9y)})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=(8x).
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=(8x).$

We see that it is a homogeneous polynomial of degree $1.$ Therefore, $f(x,y)$ is a homogeneous function of degree $1.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=(8x)\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =t(8x)=tf(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## generated moderate variant — q-8741 / linear_not

Parameters: `{"sx": 7, "sy": 3}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\operatorname{arctan}⁡(\frac{(7x)}{(3y)})$
- $\frac{\text{d}y}{\text{d}x}=(7x)$ **correct**
- $\frac{\text{d}y}{\text{d}x}=1$
- $\frac{\text{d}y}{\text{d}x}=2$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{ln}⁡(3y)-\operatorname{ln}⁡(7x)$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=(7x).
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=(7x).$

We see that it is a homogeneous polynomial of degree $1.$ Therefore, $f(x,y)$ is a homogeneous function of degree $1.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=(7x)\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =t(7x)=tf(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## generated moderate variant — q-14322 / constant_offset_not

Parameters: `{"sx": 2, "sy": 2, "x0": 1, "y0": 2, "t": 2}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{4{(2x)}^{2}(2y)}{{(2x)}^{3}+(2x){(2y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{(2x)(2y)}{{(2x)}^{2}+{(2y)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(2x)}^{2}+1}{{(2y)}^{2}+(2x)(2y)}$ **correct**
- $\frac{\text{d}y}{\text{d}x}={e}^{\operatorname{sin}⁡(\frac{(2x)}{(2y)})}$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{(2x)+(2y)}{(2y)})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is:

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(2x)}^{2}+1}{{(2y)}^{2}+(2x)(2y)}
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(2x)}^{2}+1}{{(2y)}^{2}+(2x)(2y)}.$

We see that the numerator has terms of degrees $2$ and $0$, whereas the denominator is homogeneous of degree $2$. The nonzero constant term cannot cancel against this denominator, so the scaling factors cannot cancel. Therefore, $f(x,y)$ is NOT a homogeneous function of degree zero.

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(2x)}^{2}+1}{{(2y)}^{2}+(2x)(2y)}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

For $x=1$, $y=2$ and $t=2$, for instance, we have

$$
\begin{aligned}f(tx,ty) & =f(2\cdot 1,2\cdot 2) \\  & =f(2,4) \\  & =\frac{{4}^{2}+1}{{8}^{2}+4(8)} \\  & =\frac{17}{96} \\  & =\frac{17}{96}\end{aligned}
$$

and

$$
\begin{aligned}f(x,y) & =f(1,2) \\  & =\frac{{2}^{2}+1}{{4}^{2}+2(4)} \\  & =\frac{5}{24} \\  & =\frac{5}{24}.\end{aligned}
$$

In other words, there exists at least one combination of values of $(2x)$, $(2y)$ and $t$ for which the identity $f(tx,ty)=f(x,y)$ is not observed.

Hence, the original differential equation is  NOT homogeneous.

## generated moderate variant — q-14322 / constant_offset_not

Parameters: `{"sx": 1, "sy": 1, "x0": 1, "y0": 2, "t": 2}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{4{x}^{2}y}{{x}^{3}+x{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}={e}^{\operatorname{sin}⁡(\frac{x}{y})}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{xy}{{x}^{2}+{y}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{x+y}{y})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is:

$$
\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}+1}{{y}^{2}+xy}
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}.$

We see that the numerator has terms of degrees $2$ and $0$, whereas the denominator is homogeneous of degree $2$. The nonzero constant term cannot cancel against this denominator, so the scaling factors cannot cancel. Therefore, $f(x,y)$ is NOT a homogeneous function of degree zero.

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{x}^{2}+1}{{y}^{2}+xy}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

For $x=1$, $y=2$ and $t=2$, for instance, we have

$$
\begin{aligned}f(tx,ty) & =f(2\cdot 1,2\cdot 2) \\  & =f(2,4) \\  & =\frac{{2}^{2}+1}{{4}^{2}+2(4)} \\  & =\frac{5}{24} \\  & =\frac{5}{24}\end{aligned}
$$

and

$$
\begin{aligned}f(x,y) & =f(1,2) \\  & =\frac{{1}^{2}+1}{{2}^{2}+1(2)} \\  & =\frac{2}{6} \\  & =\frac{1}{3}.\end{aligned}
$$

In other words, there exists at least one combination of values of $x$, $y$ and $t$ for which the identity $f(tx,ty)=f(x,y)$ is not observed.

Hence, the original differential equation is  NOT homogeneous.

## generated moderate variant — q-90597 / quadratic_not

Parameters: `{"sx": 8, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\operatorname{cos}⁡(\frac{(8x)}{2(9y)})$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}}{{(8x)}^{2}+(8x)(9y)}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}}{2}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=9$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{{(8x)}^{3}}{{(9y)}^{3}})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}}{2}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(9y)}^{2}}{2}=\frac{1}{2}{(9y)}^{2}.$

We see that it is a homogeneous polynomial of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(9y)}^{2}}{2}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(9y))^{2}}{2} \\  & ={t}^{2}\cdot \frac{{(9y)}^{2}}{2} \\  & ={t}^{2}f(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## generated moderate variant — q-90597 / quadratic_not

Parameters: `{"sx": 7, "sy": 3}`; profile `normal`; eligible for learning: True.

Which of the following is NOT a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\operatorname{sin}⁡(\frac{{(7x)}^{3}}{{(3y)}^{3}})$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}}{2}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}}{{(7x)}^{2}+(7x)(3y)}$
- $\frac{\text{d}y}{\text{d}x}=9$
- $\frac{\text{d}y}{\text{d}x}=\operatorname{cos}⁡(\frac{(7x)}{2(3y)})$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is NOT the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(3y)}^{2}}{2}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(3y)}^{2}}{2}=\frac{1}{2}{(3y)}^{2}.$

We see that it is a homogeneous polynomial of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2.$

Hence, the original differential equation is  NOT homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(3y)}^{2}}{2}\,
$$

We can check that this is not homogeneous showing that $f(tx,ty)\ne f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(3y))^{2}}{2} \\  & ={t}^{2}\cdot \frac{{(3y)}^{2}}{2} \\  & ={t}^{2}f(x,y)\,\end{aligned}
$$

Since $f(tx,ty)\ne f(x,y),$ the original differential equation is NOT homogeneous.

## generated hard variant — q-14319 / cubic_quotient

Parameters: `{"sx": 9, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{(9x)}^{3}-3(9x)(9y)+(9x)(9y)}{{(9y)}^{2}-{(9x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9x)}^{2}-(9x){(9y)}^{2}+{(9y)}^{2}}{1+{(9x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}(9x)-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2}}{{(9y)}^{3}+{(9x)}^{3}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{3}-{(9x)}^{2}(9y)+{(9x)}^{3}}{{(9y)}^{3}+1}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2}}{{(9y)}^{3}+{(9x)}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2}}{{(9y)}^{3}+{(9x)}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2}}{{(9y)}^{3}+{(9x)}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(9x))^{3}-3(t(9x))^{2}(t(9y))+(t(9x))(t(9y))^{2}}{(t(9y))^{3}+(t(9x))^{3}} \\  & =\frac{{t}^{3}({(9x)}^{3})-{t}^{3}(3{(9x)}^{2}(9y))+{t}^{3}((9x){(9y)}^{2})}{{t}^{3}{(9y)}^{3}+{t}^{3}{(9x)}^{3}} \\  & =\frac{{t}^{3}({(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2})}{{t}^{3}({(9y)}^{3}+{(9x)}^{3})} \\  & =\frac{{(9x)}^{3}-3{(9x)}^{2}(9y)+(9x){(9y)}^{2}}{{(9y)}^{3}+{(9x)}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated hard variant — q-14319 / cubic_quotient

Parameters: `{"sx": 8, "sy": 4}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{3}-{(8x)}^{2}(4y)+{(8x)}^{3}}{{(4y)}^{3}+1}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(8x)}^{3}-3(8x)(4y)+(8x)(4y)}{{(4y)}^{2}-{(8x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}(8x)-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(8x)}^{2}-(8x){(4y)}^{2}+{(4y)}^{2}}{1+{(8x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2}}{{(4y)}^{3}+{(8x)}^{3}}$ **correct**

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2}}{{(4y)}^{3}+{(8x)}^{3}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2}}{{(4y)}^{3}+{(8x)}^{3}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $3.$ Therefore, $f(x,y)$ is a homogeneous function of degree $3-3=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2}}{{(4y)}^{3}+{(8x)}^{3}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(8x))^{3}-3(t(8x))^{2}(t(4y))+(t(8x))(t(4y))^{2}}{(t(4y))^{3}+(t(8x))^{3}} \\  & =\frac{{t}^{3}({(8x)}^{3})-{t}^{3}(3{(8x)}^{2}(4y))+{t}^{3}((8x){(4y)}^{2})}{{t}^{3}{(4y)}^{3}+{t}^{3}{(8x)}^{3}} \\  & =\frac{{t}^{3}({(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2})}{{t}^{3}({(4y)}^{3}+{(8x)}^{3})} \\  & =\frac{{(8x)}^{3}-3{(8x)}^{2}(4y)+(8x){(4y)}^{2}}{{(4y)}^{3}+{(8x)}^{3}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated hard variant — q-8369 / quadratic_difference

Parameters: `{"sx": 9, "sy": 9}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{(9x)}^{2}}{(9y)-{(9x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9y)}^{2}+(9x)}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-(9x)}{{(9y)}^{2}+{(9x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{(9y)-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9x)}^{2}+{(9y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(9y))^{2}-(t(9x))^{2}}{(t(9y))^{2}+(t(9x))^{2}} \\  & =\frac{{t}^{2}{(9y)}^{2}-{t}^{2}{(9x)}^{2}}{{t}^{2}{(9y)}^{2}+{t}^{2}{(9x)}^{2}} \\  & =\frac{{t}^{2}({(9y)}^{2}-{(9x)}^{2})}{{t}^{2}({(9y)}^{2}+{(9x)}^{2})} \\  & =\frac{{(9y)}^{2}-{(9x)}^{2}}{{(9y)}^{2}+{(9x)}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

## generated hard variant — q-8369 / quadratic_difference

Parameters: `{"sx": 8, "sy": 4}`; profile `normal`; eligible for learning: True.

Which of the following is a first-order homogeneous ordinary differential equation?

Field 0 (selection radio), correct reference present.

- $\frac{\text{d}y}{\text{d}x}=\frac{(4y)-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}}$ **correct**
- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}-{(8x)}^{2}}{{(4y)}^{2}+(8x)}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}-{(8x)}^{2}}{(4y)-{(8x)}^{2}}$
- $\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}-(8x)}{{(4y)}^{2}+{(8x)}^{2}}$

A first-order ordinary differential equation that is written in the form

$$
\frac{\text{d}y}{\text{d}x}=f(x,y)
$$

is said to be homogeneous if it satisfies the following property:

$$
f(tx,ty)=f(x,y)\,
$$

The only option in which this is the case is

$$
\frac{\text{d}y}{\text{d}x}=\frac{{(4y)}^{2}-{(8x)}^{2}}{{(8x)}^{2}+{(4y)}^{2}}.
$$

We can check this using one of two methods.

**Method 1**

Let $f(x,y)=\frac{{(4y)}^{2}-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}}.$

We see that both the numerator and denominator are homogeneous polynomials of degree $2.$ Therefore, $f(x,y)$ is a homogeneous function of degree $2-2=0.$

Hence, the original differential equation is homogeneous.

**Method 2**

To check this in detail using the definition, we first write:

$$
f(x,y)=\frac{{(4y)}^{2}-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}}
$$

We can check that this is homogeneous showing that $f(tx,ty)=f(x,y),$ as follows:

$$
\begin{aligned}f(tx,ty) & =\frac{(t(4y))^{2}-(t(8x))^{2}}{(t(4y))^{2}+(t(8x))^{2}} \\  & =\frac{{t}^{2}{(4y)}^{2}-{t}^{2}{(8x)}^{2}}{{t}^{2}{(4y)}^{2}+{t}^{2}{(8x)}^{2}} \\  & =\frac{{t}^{2}({(4y)}^{2}-{(8x)}^{2})}{{t}^{2}({(4y)}^{2}+{(8x)}^{2})} \\  & =\frac{{(4y)}^{2}-{(8x)}^{2}}{{(4y)}^{2}+{(8x)}^{2}} \\  & =f(x,y)\end{aligned}
$$

Since $f(tx,ty)=f(x,y),$ the original differential equation is homogeneous.

