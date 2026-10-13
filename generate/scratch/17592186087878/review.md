# Source originals and generated variants


Raw originals below are evidence, including their recorded anomalies.


## Original q-335402

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-3y=6{e}^{2x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.


**field-2 raw bank**

- `-6{e}^{-x}+C{e}^{-3x}`

- `6{e}^{2x}+C{e}^{3x}`

- `6{e}^{-2x}+C{e}^{-3x}`

- `-6{e}^{2x}+C{e}^{3x}`


**field-1 raw bank**

- `{e}^{2x}`

- `{e}^{3x}`

- `{e}^{-3x}`

- `{e}^{-2x}`


**Raw worked solution**

This equation is already in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-3$ and $Q(x)=6{e}^{2x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -3\,\text{d}x} \\  & ={e}^{-3x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-3x}$ as follows:

$$
\begin{aligned}{e}^{-3x}\cdot (\frac{\text{d}y}{\text{d}x}-3y) & ={e}^{-3x}\cdot 6{e}^{2x} \\ {e}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}-3{e}^{-3x}\cdot y & =6{e}^{-x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-3x}) & =6{e}^{-x} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-3x})\text{d}x & =\int 6{e}^{-x}\,\text{d}x \\ y{e}^{-3x} & =-6{e}^{-x}+C \\ y & =-6{e}^{2x}+C{e}^{3x}\end{aligned}
$$


### Generated variant (authored bank)

## exp_forcing — easy
Profile: `exp_forcing_authored`; parameters: `{'a': 5, 'b': 8, 'r': 1}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-5y=8{e}^{x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $2{e}^{x}+C{e}^{5x}$
- $2{e}^{-x}+C{e}^{-5x}$
- $-2{e}^{x}+C{e}^{5x}$ **correct**
- $-2{e}^{-4x}+C{e}^{-5x}$
**field-1**
- ${e}^{5x}$
- ${e}^{-5x}$ **correct**
- ${e}^{x}$
- ${e}^{-x}$

**Worked solution**

This equation is already in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-5$ and $Q(x)=8{e}^{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -5\,\text{d}x} \\  & ={e}^{-5x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-5x}$ as follows:

$$
\begin{aligned}{e}^{-5x}\cdot (\frac{\text{d}y}{\text{d}x}-5y) & ={e}^{-5x}\cdot 8{e}^{x} \\ {e}^{-5x}\cdot \frac{\text{d}y}{\text{d}x}-5{e}^{-5x}\cdot y & =8{e}^{-4x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-5x}) & =8{e}^{-4x} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-5x})\text{d}x & =\int 8{e}^{-4x}\,\text{d}x \\ y{e}^{-5x} & =-2{e}^{-4x}+C \\ y & =-2{e}^{x}+C{e}^{5x}\end{aligned}
$$


### Generated variant (authored bank)

## exp_forcing — easy
Profile: `exp_forcing_authored`; parameters: `{'a': 2, 'b': 9, 'r': 4}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-2y=9{e}^{4x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{9{e}^{4x}}{2}+C{e}^{2x}$ **correct**
- $-\frac{9{e}^{-4x}}{2}+C{e}^{-2x}$
- $\frac{9{e}^{2x}}{2}+C{e}^{-2x}$
- $-\frac{9{e}^{4x}}{2}+C{e}^{2x}$
**field-1**
- ${e}^{4x}$
- ${e}^{-4x}$
- ${e}^{-2x}$ **correct**
- ${e}^{2x}$

**Worked solution**

This equation is already in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-2$ and $Q(x)=9{e}^{4x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -2\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-2x}$ as follows:

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot 9{e}^{4x} \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =9{e}^{2x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =9{e}^{2x} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int 9{e}^{2x}\,\text{d}x \\ y{e}^{-2x} & =\frac{9{e}^{2x}}{2}+C \\ y & =\frac{9{e}^{4x}}{2}+C{e}^{2x}\end{aligned}
$$


## Original q-339138

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-3y=x{e}^{3x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.


**field-1 raw bank**

- `3\operatorname{ln}⁡x`

- `{e}^{3x}`

- `-3`

- `{e}^{-3x}`


**field-2 raw bank**

- `\frac{x{e}^{-3x}}{2}+C{e}^{-3x}`

- `\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{-3x}`

- `\frac{x{e}^{-3x}}{2}+C{e}^{3x}`

- `\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}`


**Raw worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-3$ and $Q(x)=x{e}^{3x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -3\,\text{d}x} \\  & ={e}^{-3x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-3x}$ as follows:

$$
\begin{aligned}{e}^{-3x}\cdot (\frac{\text{d}y}{\text{d}x}-3y) & ={e}^{-3x}\cdot x{e}^{3x} \\ {e}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}-3{e}^{-3x}\cdot y & =x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-3x}) & =x \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-3x})\text{d}x & =\int x\,\text{d}x \\ y{e}^{-3x} & =\frac{{x}^{2}}{2}+C \\ y & =\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}\end{aligned}
$$


### Generated variant (authored bank)

## exp_cancel — easy
Profile: `exp_cancel_authored`; parameters: `{'a': 5, 'm': 2}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-5y={x}^{2}{e}^{5x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- ${e}^{5x}$
- $-5$
- $5\operatorname{ln}⁡x$
- ${e}^{-5x}$ **correct**
**field-2**
- $\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{-5x}$
- $\frac{{x}^{2}{e}^{-5x}}{3}+C{e}^{5x}$
- $\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{5x}$ **correct**
- $\frac{{x}^{2}{e}^{-5x}}{3}+C{e}^{-5x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-5$ and $Q(x)={x}^{2}{e}^{5x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -5\,\text{d}x} \\  & ={e}^{-5x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-5x}$ as follows:

$$
\begin{aligned}{e}^{-5x}\cdot (\frac{\text{d}y}{\text{d}x}-5y) & ={e}^{-5x}\cdot {x}^{2}{e}^{5x} \\ {e}^{-5x}\cdot \frac{\text{d}y}{\text{d}x}-5{e}^{-5x}\cdot y & ={x}^{2}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-5x}) & ={x}^{2} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-5x})\text{d}x & =\int {x}^{2}\,\text{d}x \\ y{e}^{-5x} & =\frac{{x}^{3}}{3}+C \\ y & =\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{5x}\end{aligned}
$$


### Generated variant (authored bank)

## exp_cancel — easy
Profile: `exp_cancel_authored`; parameters: `{'a': 3, 'm': 1}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-3y=x{e}^{3x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- $3\operatorname{ln}⁡x$
- ${e}^{-3x}$ **correct**
- $-3$
- ${e}^{3x}$
**field-2**
- $\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}$ **correct**
- $\frac{x{e}^{-3x}}{2}+C{e}^{3x}$
- $\frac{x{e}^{-3x}}{2}+C{e}^{-3x}$
- $\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{-3x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-3$ and $Q(x)=x{e}^{3x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -3\,\text{d}x} \\  & ={e}^{-3x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-3x}$ as follows:

$$
\begin{aligned}{e}^{-3x}\cdot (\frac{\text{d}y}{\text{d}x}-3y) & ={e}^{-3x}\cdot x{e}^{3x} \\ {e}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}-3{e}^{-3x}\cdot y & =x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-3x}) & =x \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-3x})\text{d}x & =\int x\,\text{d}x \\ y{e}^{-3x} & =\frac{{x}^{2}}{2}+C \\ y & =\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}\end{aligned}
$$


## Original q-335392

Consider the differential equation
$\frac{dy}{dx} - 2y = x^{2}e^{2x}$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.


**field-1 raw bank**

- `2\ln x`

- `e^{-2x}`

- `-2`

- `e^{2x}`


**field-2 raw bank**

- `\frac{x^{3}e^{2x}}{3} + Ce^{-2x}`

- `\frac{x^{3}e^{2x}}{3} + Ce^{2x}`

- `\frac{x^{2}e^{-2x}}{3} + Ce^{-2x}`

- `\frac{x^{2}e^{-2x}}{3} + Ce^{2x}`


**Raw worked solution**

Not captured; generated solution is authored.


### Generated variant (authored bank)

## exp_cancel_legacy — easy
Profile: `exp_cancel_legacy_authored`; parameters: `{'a': 5, 'm': 2}`.

Consider the differential equation
$\frac{dy}{dx} - 5y = x^{2}e^{5x}$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-1**
- ${e}^{5x}$
- $-5$
- $5\operatorname{ln}⁡x$
- ${e}^{-5x}$ **correct**
**field-2**
- $\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{-5x}$
- $\frac{{x}^{2}{e}^{-5x}}{3}+C{e}^{5x}$
- $\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{5x}$ **correct**
- $\frac{{x}^{2}{e}^{-5x}}{3}+C{e}^{-5x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-5$ and $Q(x)={x}^{2}{e}^{5x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -5\,\text{d}x} \\  & ={e}^{-5x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-5x}$ as follows:

$$
\begin{aligned}{e}^{-5x}\cdot (\frac{\text{d}y}{\text{d}x}-5y) & ={e}^{-5x}\cdot {x}^{2}{e}^{5x} \\ {e}^{-5x}\cdot \frac{\text{d}y}{\text{d}x}-5{e}^{-5x}\cdot y & ={x}^{2}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-5x}) & ={x}^{2} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-5x})\text{d}x & =\int {x}^{2}\,\text{d}x \\ y{e}^{-5x} & =\frac{{x}^{3}}{3}+C \\ y & =\frac{{x}^{3}{e}^{5x}}{3}+C{e}^{5x}\end{aligned}
$$


### Generated variant (authored bank)

## exp_cancel_legacy — easy
Profile: `exp_cancel_legacy_authored`; parameters: `{'a': 3, 'm': 1}`.

Consider the differential equation
$\frac{dy}{dx} - 3y = x^{1}e^{3x}$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-1**
- $3\operatorname{ln}⁡x$
- ${e}^{-3x}$ **correct**
- $-3$
- ${e}^{3x}$
**field-2**
- $\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}$ **correct**
- $\frac{x{e}^{-3x}}{2}+C{e}^{3x}$
- $\frac{x{e}^{-3x}}{2}+C{e}^{-3x}$
- $\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{-3x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-3$ and $Q(x)=x{e}^{3x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -3\,\text{d}x} \\  & ={e}^{-3x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-3x}$ as follows:

$$
\begin{aligned}{e}^{-3x}\cdot (\frac{\text{d}y}{\text{d}x}-3y) & ={e}^{-3x}\cdot x{e}^{3x} \\ {e}^{-3x}\cdot \frac{\text{d}y}{\text{d}x}-3{e}^{-3x}\cdot y & =x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-3x}) & =x \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-3x})\text{d}x & =\int x\,\text{d}x \\ y{e}^{-3x} & =\frac{{x}^{2}}{2}+C \\ y & =\frac{{x}^{2}{e}^{3x}}{2}+C{e}^{3x}\end{aligned}
$$


## Original q-339140

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y=7,\,x>0.
$$

Select the correct options below:

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.


**field-1 raw bank**

- `{x}^{4}`

- `\operatorname{ln}⁡x`

- `\frac{1}{x}`

- `{x}^{5}`


**field-2 raw bank**

- `x+\frac{C}{{x}^{4}}`

- `\frac{7x}{6}+\frac{C}{{x}^{5}}`

- `\frac{7x}{6}+\frac{C}{{x}^{4}}`

- `x+\frac{C}{{x}^{5}}`


**Raw worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=7.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (5/x)\,dx} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{5})} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot 7 \\ {x}^{5}\frac{\text{d}y}{\text{d}x}+5{x}^{4}y & =7{x}^{5}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{5})\,dx & =\int 7{x}^{5}\,\text{d}x \\ y{x}^{5} & =\frac{7{x}^{6}}{6}+C \\ y & =\frac{7x}{6}+\frac{C}{{x}^{5}}.\end{aligned}
$$


### Generated variant (authored bank)

## power_constant — moderate
Profile: `power_constant_authored`; parameters: `{'n': 5, 'b': 8}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y=8,\,x>0.
$$

Select the correct options below:

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- $\operatorname{ln}⁡x$
- $\frac{1}{x}$
- ${x}^{4}$
- ${x}^{5}$ **correct**
**field-2**
- $\frac{4x}{3}+\frac{C}{{x}^{5}}$ **correct**
- $\frac{4x}{3}+\frac{C}{{x}^{4}}$
- $\frac{8x}{5}+\frac{C}{{x}^{5}}$
- $\frac{8x}{5}+\frac{C}{{x}^{4}}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=8.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (5/x)\,dx} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{5})} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot 8 \\ {x}^{5}\frac{\text{d}y}{\text{d}x}+5{x}^{4}y & =8{x}^{5}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{5})\,dx & =\int 8{x}^{5}\,\text{d}x \\ y{x}^{5} & =\frac{8{x}^{6}}{6}+C \\ y & =\frac{4x}{3}+\frac{C}{{x}^{5}}.\end{aligned}
$$


### Generated variant (authored bank)

## power_constant — moderate
Profile: `power_constant_authored`; parameters: `{'n': 3, 'b': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y=3,\,x>0.
$$

Select the correct options below:

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- ${x}^{2}$
- ${x}^{3}$ **correct**
- $\frac{1}{x}$
- $\operatorname{ln}⁡x$
**field-2**
- $x+\frac{C}{{x}^{3}}$
- $\frac{3x}{4}+\frac{C}{{x}^{2}}$
- $x+\frac{C}{{x}^{2}}$
- $\frac{3x}{4}+\frac{C}{{x}^{3}}$ **correct**

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=3.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (3/x)\,dx} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{3})} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot 3 \\ {x}^{3}\frac{\text{d}y}{\text{d}x}+3{x}^{2}y & =3{x}^{3}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{3})\,dx & =\int 3{x}^{3}\,\text{d}x \\ y{x}^{3} & =\frac{3{x}^{4}}{4}+C \\ y & =\frac{3x}{4}+\frac{C}{{x}^{3}}.\end{aligned}
$$


## Original q-334915

Consider the differential equation
$\frac{dy}{dx} + \frac{2}{x}y = 3, x > 0$.

Select the correct options below:

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.


**field-2 raw bank**

- `x + \frac{C}{x^{2}}`

- `x^{2} + \frac{C}{x^{2}}`

- `x^{2} + \frac{C}{x}`

- `x + \frac{C}{x}`


**field-1 raw bank**

- `x^{2}`

- `\frac{1}{x}`

- `\ln x`

- `x`


**Raw worked solution**

Not captured; generated solution is authored.


### Generated variant (authored bank)

## power_constant_legacy — moderate
Profile: `power_constant_legacy_authored`; parameters: `{'n': 5, 'b': 8}`.

Consider the differential equation
$\frac{dy}{dx} + \frac{5}{x}y = 8, x > 0$.

Select the correct options below:

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-2**
- $\frac{4{x}^{2}}{3}+\frac{C}{{x}^{5}}$
- $\frac{4{x}^{2}}{3}+\frac{C}{{x}^{4}}$
- $\frac{4x}{3}+\frac{C}{{x}^{4}}$
- $\frac{4x}{3}+\frac{C}{{x}^{5}}$ **correct**
**field-1**
- $\operatorname{ln}⁡x$
- $\frac{1}{x}$
- ${x}^{4}$
- ${x}^{5}$ **correct**

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=8.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (5/x)\,dx} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{5})} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot 8 \\ {x}^{5}\frac{\text{d}y}{\text{d}x}+5{x}^{4}y & =8{x}^{5}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{5})\,dx & =\int 8{x}^{5}\,\text{d}x \\ y{x}^{5} & =\frac{8{x}^{6}}{6}+C \\ y & =\frac{4x}{3}+\frac{C}{{x}^{5}}.\end{aligned}
$$


### Generated variant (authored bank)

## power_constant_legacy — moderate
Profile: `power_constant_legacy_authored`; parameters: `{'n': 3, 'b': 3}`.

Consider the differential equation
$\frac{dy}{dx} + \frac{3}{x}y = 3, x > 0$.

Select the correct options below:

An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-2**
- $\frac{3x}{4}+\frac{C}{{x}^{2}}$
- $\frac{3{x}^{2}}{4}+\frac{C}{{x}^{2}}$
- $\frac{3x}{4}+\frac{C}{{x}^{3}}$ **correct**
- $\frac{3{x}^{2}}{4}+\frac{C}{{x}^{3}}$
**field-1**
- ${x}^{2}$
- ${x}^{3}$ **correct**
- $\frac{1}{x}$
- $\operatorname{ln}⁡x$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=3.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (3/x)\,dx} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{3})} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot 3 \\ {x}^{3}\frac{\text{d}y}{\text{d}x}+3{x}^{2}y & =3{x}^{3}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{3})\,dx & =\int 3{x}^{3}\,\text{d}x \\ y{x}^{3} & =\frac{3{x}^{4}}{4}+C \\ y & =\frac{3x}{4}+\frac{C}{{x}^{3}}.\end{aligned}
$$


## Original q-335412

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y=\frac{{e}^{x}}{{x}^{3}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.


**field-1 raw bank**

- `\frac{3}{x}`

- `{x}^{3}`

- `{e}^{3/x}`

- `{e}^{{x}^{3}}`


**field-2 raw bank**

- `\frac{{e}^{x}+C}{{x}^{3}}`

- `{x}^{2}({e}^{x}+C)`

- `\frac{{e}^{x}+C}{{x}^{2}}`

- `{x}^{3}({e}^{x}+C)`


**Raw worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{{e}^{x}}{{x}^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (3/x)\,dx} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{3})} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot \frac{{e}^{x}}{{x}^{3}} \\ {x}^{3}\cdot \frac{\text{d}y}{\text{d}x}+3{x}^{2}\cdot y & ={e}^{x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{3})\,dx & =\int {e}^{x}\,\text{d}x \\ y{x}^{3} & ={e}^{x}+C \\ y & =\frac{{e}^{x}+C}{{x}^{3}}\end{aligned}
$$


### Generated variant (authored bank)

## power_exp — moderate
Profile: `power_exp_authored`; parameters: `{'n': 5, 'r': 2}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y=\frac{{e}^{2x}}{{x}^{5}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- ${x}^{5}$ **correct**
- ${e}^{5/x}$
- $\frac{5}{x}$
- ${e}^{{x}^{5}}$
**field-2**
- ${x}^{4}(\frac{{e}^{2x}}{2}+C)$
- $\frac{\frac{{e}^{2x}}{2}+C}{{x}^{4}}$
- ${x}^{5}(\frac{{e}^{2x}}{2}+C)$
- $\frac{\frac{{e}^{2x}}{2}+C}{{x}^{5}}$ **correct**

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=\frac{{e}^{2x}}{{x}^{5}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (5/x)\,dx} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{5})} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot \frac{{e}^{2x}}{{x}^{5}} \\ {x}^{5}\cdot \frac{\text{d}y}{\text{d}x}+5{x}^{4}\cdot y & ={e}^{2x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{5})\,dx & =\int {e}^{2x}\,\text{d}x \\ y{x}^{5} & =\frac{{e}^{2x}}{2}+C \\ y & =\frac{\frac{{e}^{2x}}{2}+C}{{x}^{5}}\end{aligned}
$$


### Generated variant (authored bank)

## power_exp — moderate
Profile: `power_exp_authored`; parameters: `{'n': 3, 'r': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y=\frac{{e}^{3x}}{{x}^{3}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- $\frac{3}{x}$
- ${e}^{{x}^{3}}$
- ${e}^{3/x}$
- ${x}^{3}$ **correct**
**field-2**
- ${x}^{3}(\frac{{e}^{3x}}{3}+C)$
- $\frac{\frac{{e}^{3x}}{3}+C}{{x}^{2}}$
- $\frac{\frac{{e}^{3x}}{3}+C}{{x}^{3}}$ **correct**
- ${x}^{2}(\frac{{e}^{3x}}{3}+C)$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{{e}^{3x}}{{x}^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (3/x)\,dx} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{3})} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot \frac{{e}^{3x}}{{x}^{3}} \\ {x}^{3}\cdot \frac{\text{d}y}{\text{d}x}+3{x}^{2}\cdot y & ={e}^{3x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{3})\,dx & =\int {e}^{3x}\,\text{d}x \\ y{x}^{3} & =\frac{{e}^{3x}}{3}+C \\ y & =\frac{\frac{{e}^{3x}}{3}+C}{{x}^{3}}\end{aligned}
$$


## Original q-335409

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y=\frac{\operatorname{sin}⁡x}{x},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.


**field-2 raw bank**

- `\frac{\operatorname{sin}x}{{x}^{2}}-\frac{\operatorname{cos}x}{x}+\frac{C}{{x}^{2}}`

- `\frac{\operatorname{sin}⁡x}{x}+\frac{\operatorname{cos}⁡x}{{x}^{2}}+\frac{C}{{x}^{2}}`

- `\frac{\operatorname{sin}⁡x}{x}-\frac{\operatorname{cos}⁡x}{{x}^{2}}+\frac{C}{x}`

- `\frac{\operatorname{sin}⁡x}{{x}^{2}}+\frac{\operatorname{cos}⁡x}{x}+\frac{C}{x}`

- `\frac{\operatorname{sin}⁡x}{{x}^{2}}-\frac{\operatorname{cos}⁡x}{x}+\frac{C}{{x}^{2}}`


**field-1 raw bank**

- `\frac{2}{x}`

- `{e}^{{x}^{2}}`

- `{x}^{2}`

- `{e}^{2/x}`


**Raw worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{2}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (2/x)\,\text{d}x} \\  & ={e}^{2\operatorname{ln}⁡x} \\  & ={x}^{2}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{2}$ as follows:

$$
\begin{aligned}{x}^{2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{2}{x}y) & ={x}^{2}\cdot \frac{\operatorname{sin}⁡x}{x} \\ {x}^{2}\frac{\text{d}y}{\text{d}x}+2xy & =x\operatorname{sin}⁡x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{2}) & =x\operatorname{sin}⁡x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{2})\text{d}x & =\int x\operatorname{sin}⁡x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{sin}⁡x,$ and $v=-\operatorname{cos}⁡x.$ Then, we have

$$
\begin{aligned}y{x}^{2} & =\int x\operatorname{sin}⁡x\,\text{d}x \\ y{x}^{2} & =x(-\operatorname{cos}⁡x)-\int (-\operatorname{cos}⁡x)\cdot 1\,\text{d}x \\ y{x}^{2} & =-x\operatorname{cos}⁡x+\int \operatorname{cos}⁡x\,\text{d}x \\ y{x}^{2} & =-x\operatorname{cos}⁡x+\operatorname{sin}⁡x\,+C \\ y & =\frac{\operatorname{sin}⁡x}{{x}^{2}}-\frac{\operatorname{cos}⁡x}{x}+\frac{C}{{x}^{2}}.\end{aligned}
$$


### Generated variant (authored bank)

## power_sin — hard
Profile: `power_sin_authored`; parameters: `{'n': 5, 'r': 2}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y=\frac{\operatorname{sin}⁡2x}{{x}^{4}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\frac{\operatorname{sin}⁡2x}{{x}^{4}}}{4}+\frac{\frac{\operatorname{cos}⁡2x}{{x}^{5}}}{2}+\frac{C}{{x}^{5}}$
- $\frac{\frac{\operatorname{sin}⁡2x}{{x}^{4}}}{4}-\frac{\frac{\operatorname{cos}⁡2x}{{x}^{5}}}{2}+\frac{C}{{x}^{4}}$
- $\frac{\frac{\operatorname{sin}⁡2x}{{x}^{5}}}{4}+\frac{\frac{\operatorname{cos}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{4}}$
- $\frac{\frac{\operatorname{sin}2x}{{x}^{5}}}{4}-\frac{\frac{\operatorname{cos}2x}{{x}^{4}}}{2}+\frac{C}{{x}^{5}}$ **correct**
- $\frac{\frac{\operatorname{sin}⁡2x}{{x}^{5}}}{4}-\frac{\frac{\operatorname{cos}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{4}}$
**field-1**
- ${e}^{{x}^{5}}$
- ${x}^{5}$ **correct**
- $\frac{5}{x}$
- ${e}^{5/x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡2x}{{x}^{4}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (5/x)\,\text{d}x} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot \frac{\operatorname{sin}⁡2x}{{x}^{4}} \\ {x}^{5}\frac{\text{d}y}{\text{d}x}+5{x}^{4}y & =x\operatorname{sin}⁡2x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{5}) & =x\operatorname{sin}⁡2x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{5})\text{d}x & =\int x\operatorname{sin}⁡2x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{sin}⁡2x,$ and $v=-\frac{\operatorname{cos}⁡2x}{2}.$ Then, we have

$$
\begin{aligned}y{x}^{5} & =\int x\operatorname{sin}⁡2x\,\text{d}x \\ y{x}^{5} & =x(-\frac{\operatorname{cos}⁡2x}{2})-\int (-\frac{\operatorname{cos}⁡2x}{2})\cdot 1\,\text{d}x \\ y{x}^{5} & =x(-\frac{\operatorname{cos}⁡2x}{2})+\int \frac{\operatorname{cos}⁡2x}{2}\,\text{d}x \\ y{x}^{5} & =-\frac{x\operatorname{cos}⁡2x}{2}+\frac{\operatorname{sin}⁡2x}{4}\,+C \\ y & =\frac{\frac{\operatorname{sin}⁡2x}{{x}^{5}}}{4}-\frac{\frac{\operatorname{cos}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{5}}.\end{aligned}
$$


### Generated variant (authored bank)

## power_sin — hard
Profile: `power_sin_authored`; parameters: `{'n': 3, 'r': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y=\frac{\operatorname{sin}⁡3x}{{x}^{2}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{3}}}{9}+\frac{\frac{\operatorname{cos}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{2}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{3}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{sin}3x}{{x}^{3}}}{9}-\frac{\frac{\operatorname{cos}3x}{{x}^{2}}}{3}+\frac{C}{{x}^{3}}$ **correct**
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{3}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{2}}}{9}+\frac{\frac{\operatorname{cos}⁡3x}{{x}^{3}}}{3}+\frac{C}{{x}^{3}}$
**field-1**
- $\frac{3}{x}$
- ${e}^{3/x}$
- ${x}^{3}$ **correct**
- ${e}^{{x}^{3}}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡3x}{{x}^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (3/x)\,\text{d}x} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot \frac{\operatorname{sin}⁡3x}{{x}^{2}} \\ {x}^{3}\frac{\text{d}y}{\text{d}x}+3{x}^{2}y & =x\operatorname{sin}⁡3x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{3}) & =x\operatorname{sin}⁡3x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{3})\text{d}x & =\int x\operatorname{sin}⁡3x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{sin}⁡3x,$ and $v=-\frac{\operatorname{cos}⁡3x}{3}.$ Then, we have

$$
\begin{aligned}y{x}^{3} & =\int x\operatorname{sin}⁡3x\,\text{d}x \\ y{x}^{3} & =x(-\frac{\operatorname{cos}⁡3x}{3})-\int (-\frac{\operatorname{cos}⁡3x}{3})\cdot 1\,\text{d}x \\ y{x}^{3} & =x(-\frac{\operatorname{cos}⁡3x}{3})+\int \frac{\operatorname{cos}⁡3x}{3}\,\text{d}x \\ y{x}^{3} & =-\frac{x\operatorname{cos}⁡3x}{3}+\frac{\operatorname{sin}⁡3x}{9}\,+C \\ y & =\frac{\frac{\operatorname{sin}⁡3x}{{x}^{3}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{3}}.\end{aligned}
$$


## Original q-335069

Consider the differential equation
$2\frac{dy}{dx} + y = 3x$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.


**field-1 raw bank**

- `2x`

- `x^{2}`

- `e^{-x/2}`

- `e^{x/2}`


**field-2 raw bank**

- `3x - 2 + Ce^{x/2}`

- `3(x - 2) + Ce^{-x/2}`

- `3(x - 2) + Ce^{x/2}`

- `3x - 2 + Ce^{-x/2}`


**Raw worked solution**

Not captured; generated solution is authored.


### Generated variant (authored bank)

## normalize_linear — hard
Profile: `normalize_linear_authored`; parameters: `{'k': 3, 'b': 5}`.

Consider the differential equation
$3\frac{dy}{dx} + y = 5x$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-1**
- $e^{3x}$
- $e^{-x/3}$
- $\frac{1}{3}$
- $e^{x/3}$ **correct**
**field-2**
- $5(x - 3) + Ce^{-x/3}$ **correct**
- $5(x - 3) + Ce^{x/3}$
- $5x - 3 + Ce^{-x/3}$
- $5x - 3 + Ce^{x/3}$

**Worked solution**

First divide the equation by $3$ to write it in standard form.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{3}y=\frac{5x}{3}
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{3}$ and $Q(x)=\frac{5x}{3}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1/3\,\text{d}x} \\  & ={e}^{x/3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{x/3}$ as follows:

$$
\begin{aligned}{e}^{x/3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{3}y) & ={e}^{x/3}\cdot \frac{5x}{3} \\ {e}^{x/3}\cdot \frac{\text{d}y}{\text{d}x}+\frac{1}{3}{e}^{x/3}\cdot y & =\frac{5x}{3}{e}^{x/3}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{x/3}) & =\frac{5x}{3}{e}^{x/3} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{x/3})\text{d}x & =\int \frac{5x}{3}{e}^{x/3}\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts.

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}={e}^{x/3},$ and $v=3{e}^{x/3}.$ Then, we have

$$
\begin{aligned}y{e}^{x/3} & =\int \frac{5x}{3}{e}^{x/3}\,\text{d}x \\ y{e}^{x/3} & =\frac{5}{3}\left(x(3{e}^{x/3})-\int 3{e}^{x/3}\,\text{d}x\right) \\ y{e}^{x/3} & =5x{e}^{x/3}-5\int {e}^{x/3}\,\text{d}x \\ y{e}^{x/3} & =5x{e}^{x/3}-15{e}^{x/3}+C \\ y{e}^{x/3} & =5(x-3){e}^{x/3}+C \\ y & =5(x - 3) + Ce^{-x/3}.\end{aligned}
$$


### Generated variant (authored bank)

## normalize_linear — hard
Profile: `normalize_linear_authored`; parameters: `{'k': 2, 'b': 6}`.

Consider the differential equation
$2\frac{dy}{dx} + y = 6x$.
Select the correct options below.
An integrating factor for this equation is $I(x) =$ {{field-1}}.

The general solution is given by $y(x) =$ {{field-2}}.

**field-1**
- $\frac{1}{2}$
- $e^{x/2}$ **correct**
- $e^{-x/2}$
- $e^{2x}$
**field-2**
- $6x - 2 + Ce^{-x/2}$
- $6(x - 2) + Ce^{x/2}$
- $6x - 2 + Ce^{x/2}$
- $6(x - 2) + Ce^{-x/2}$ **correct**

**Worked solution**

First divide the equation by $2$ to write it in standard form.

$$
\frac{\text{d}y}{\text{d}x}+\frac{1}{2}y=3x
$$

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{1}{2}$ and $Q(x)=3x.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int 1/2\,\text{d}x} \\  & ={e}^{x/2}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{x/2}$ as follows:

$$
\begin{aligned}{e}^{x/2}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{1}{2}y) & ={e}^{x/2}\cdot 3x \\ {e}^{x/2}\cdot \frac{\text{d}y}{\text{d}x}+\frac{1}{2}{e}^{x/2}\cdot y & =3x{e}^{x/2}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{x/2}) & =3x{e}^{x/2} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{x/2})\text{d}x & =\int 3x{e}^{x/2}\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts.

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}={e}^{x/2},$ and $v=2{e}^{x/2}.$ Then, we have

$$
\begin{aligned}y{e}^{x/2} & =\int 3x{e}^{x/2}\,\text{d}x \\ y{e}^{x/2} & =\frac{6}{2}\left(x(2{e}^{x/2})-\int 2{e}^{x/2}\,\text{d}x\right) \\ y{e}^{x/2} & =6x{e}^{x/2}-6\int {e}^{x/2}\,\text{d}x \\ y{e}^{x/2} & =6x{e}^{x/2}-12{e}^{x/2}+C \\ y{e}^{x/2} & =6(x-2){e}^{x/2}+C \\ y & =6(x - 2) + Ce^{-x/2}.\end{aligned}
$$


### Authored cosine peer (canonical example e-21742)

## power_cos — hard
Profile: `power_cos_authored`; parameters: `{'n': 5, 'r': 2}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y=\frac{\operatorname{cos}⁡2x}{{x}^{4}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\frac{\operatorname{cos}⁡2x}{{x}^{4}}}{4}+\frac{\frac{\operatorname{sin}⁡2x}{{x}^{5}}}{2}+\frac{C}{{x}^{5}}$
- $\frac{\frac{\operatorname{cos}⁡2x}{{x}^{4}}}{4}-\frac{\frac{\operatorname{sin}⁡2x}{{x}^{5}}}{2}+\frac{C}{{x}^{4}}$
- $\frac{\frac{\operatorname{cos}⁡2x}{{x}^{5}}}{4}-\frac{\frac{\operatorname{sin}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{4}}$
- $\frac{\frac{\operatorname{cos}2x}{{x}^{5}}}{4}+\frac{\frac{\operatorname{sin}2x}{{x}^{4}}}{2}+\frac{C}{{x}^{5}}$ **correct**
- $\frac{\frac{\operatorname{cos}⁡2x}{{x}^{5}}}{4}+\frac{\frac{\operatorname{sin}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{4}}$
**field-1**
- ${e}^{{x}^{5}}$
- ${x}^{5}$ **correct**
- $\frac{5}{x}$
- ${e}^{5/x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{5}{x}$ and $Q(x)=\frac{\operatorname{cos}⁡2x}{{x}^{4}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (5/x)\,\text{d}x} \\  & ={e}^{5\operatorname{ln}⁡x} \\  & ={x}^{5}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{5}$ as follows:

$$
\begin{aligned}{x}^{5}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{5}{x}y) & ={x}^{5}\cdot \frac{\operatorname{cos}⁡2x}{{x}^{4}} \\ {x}^{5}\frac{\text{d}y}{\text{d}x}+5{x}^{4}y & =x\operatorname{cos}⁡2x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{5}) & =x\operatorname{cos}⁡2x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{5})\text{d}x & =\int x\operatorname{cos}⁡2x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{cos}⁡2x,$ and $v=\frac{\operatorname{sin}⁡2x}{2}.$ Then, we have

$$
\begin{aligned}y{x}^{5} & =\int x\operatorname{cos}⁡2x\,\text{d}x \\ y{x}^{5} & =x(\frac{\operatorname{sin}⁡2x}{2})-\int (\frac{\operatorname{sin}⁡2x}{2})\cdot 1\,\text{d}x \\ y{x}^{5} & =x(\frac{\operatorname{sin}⁡2x}{2})-\int \frac{\operatorname{sin}⁡2x}{2}\,\text{d}x \\ y{x}^{5} & =\frac{x\operatorname{sin}⁡2x}{2}+\frac{\operatorname{cos}⁡2x}{4}\,+C \\ y & =\frac{\frac{\operatorname{cos}⁡2x}{{x}^{5}}}{4}+\frac{\frac{\operatorname{sin}⁡2x}{{x}^{4}}}{2}+\frac{C}{{x}^{5}}.\end{aligned}
$$


### Authored cosine peer (canonical example e-21742)

## power_cos — hard
Profile: `power_cos_authored`; parameters: `{'n': 3, 'r': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y=\frac{\operatorname{cos}⁡3x}{{x}^{2}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\frac{\operatorname{cos}⁡3x}{{x}^{3}}}{9}-\frac{\frac{\operatorname{sin}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{cos}⁡3x}{{x}^{2}}}{9}-\frac{\frac{\operatorname{sin}⁡3x}{{x}^{3}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{cos}3x}{{x}^{3}}}{9}+\frac{\frac{\operatorname{sin}3x}{{x}^{2}}}{3}+\frac{C}{{x}^{3}}$ **correct**
- $\frac{\frac{\operatorname{cos}⁡3x}{{x}^{3}}}{9}+\frac{\frac{\operatorname{sin}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{2}}$
- $\frac{\frac{\operatorname{cos}⁡3x}{{x}^{2}}}{9}+\frac{\frac{\operatorname{sin}⁡3x}{{x}^{3}}}{3}+\frac{C}{{x}^{3}}$
**field-1**
- $\frac{3}{x}$
- ${e}^{3/x}$
- ${x}^{3}$ **correct**
- ${e}^{{x}^{3}}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{3}{x}$ and $Q(x)=\frac{\operatorname{cos}⁡3x}{{x}^{2}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (3/x)\,\text{d}x} \\  & ={e}^{3\operatorname{ln}⁡x} \\  & ={x}^{3}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{3}$ as follows:

$$
\begin{aligned}{x}^{3}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{3}{x}y) & ={x}^{3}\cdot \frac{\operatorname{cos}⁡3x}{{x}^{2}} \\ {x}^{3}\frac{\text{d}y}{\text{d}x}+3{x}^{2}y & =x\operatorname{cos}⁡3x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{3}) & =x\operatorname{cos}⁡3x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{3})\text{d}x & =\int x\operatorname{cos}⁡3x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{cos}⁡3x,$ and $v=\frac{\operatorname{sin}⁡3x}{3}.$ Then, we have

$$
\begin{aligned}y{x}^{3} & =\int x\operatorname{cos}⁡3x\,\text{d}x \\ y{x}^{3} & =x(\frac{\operatorname{sin}⁡3x}{3})-\int (\frac{\operatorname{sin}⁡3x}{3})\cdot 1\,\text{d}x \\ y{x}^{3} & =x(\frac{\operatorname{sin}⁡3x}{3})-\int \frac{\operatorname{sin}⁡3x}{3}\,\text{d}x \\ y{x}^{3} & =\frac{x\operatorname{sin}⁡3x}{3}+\frac{\operatorname{cos}⁡3x}{9}\,+C \\ y & =\frac{\frac{\operatorname{cos}⁡3x}{{x}^{3}}}{9}+\frac{\frac{\operatorname{sin}⁡3x}{{x}^{2}}}{3}+\frac{C}{{x}^{3}}.\end{aligned}
$$
