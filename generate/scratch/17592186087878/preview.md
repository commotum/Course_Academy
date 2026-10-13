## exp_forcing — easy
Profile: `exp_forcing_authored`; parameters: `{'a': 6, 'b': 4, 'r': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-6y=4{e}^{3x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{4{e}^{-3x}}{3}+C{e}^{-6x}$
- $\frac{4{e}^{3x}}{3}+C{e}^{6x}$
- $-\frac{4{e}^{-3x}}{3}+C{e}^{-6x}$
- $-\frac{4{e}^{3x}}{3}+C{e}^{6x}$ **correct**
**field-1**
- ${e}^{6x}$
- ${e}^{-6x}$ **correct**
- ${e}^{3x}$
- ${e}^{-3x}$

**Worked solution**

This equation is already in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-6$ and $Q(x)=4{e}^{3x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -6\,\text{d}x} \\  & ={e}^{-6x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-6x}$ as follows:

$$
\begin{aligned}{e}^{-6x}\cdot (\frac{\text{d}y}{\text{d}x}-6y) & ={e}^{-6x}\cdot 4{e}^{3x} \\ {e}^{-6x}\cdot \frac{\text{d}y}{\text{d}x}-6{e}^{-6x}\cdot y & =4{e}^{-3x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-6x}) & =4{e}^{-3x} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-6x})\text{d}x & =\int 4{e}^{-3x}\,\text{d}x \\ y{e}^{-6x} & =-\frac{4{e}^{-3x}}{3}+C \\ y & =-\frac{4{e}^{3x}}{3}+C{e}^{6x}\end{aligned}
$$

---

## exp_forcing — easy
Profile: `exp_forcing_authored`; parameters: `{'a': 2, 'b': 2, 'r': 4}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}-2y=2{e}^{4x}.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $-{e}^{4x}+C{e}^{2x}$
- $-{e}^{-4x}+C{e}^{-2x}$
- ${e}^{4x}+C{e}^{2x}$ **correct**
- ${e}^{2x}+C{e}^{-2x}$
**field-1**
- ${e}^{4x}$
- ${e}^{2x}$
- ${e}^{-4x}$
- ${e}^{-2x}$ **correct**

**Worked solution**

This equation is already in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=-2$ and $Q(x)=2{e}^{4x}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int -2\,\text{d}x} \\  & ={e}^{-2x}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={e}^{-2x}$ as follows:

$$
\begin{aligned}{e}^{-2x}\cdot (\frac{\text{d}y}{\text{d}x}-2y) & ={e}^{-2x}\cdot 2{e}^{4x} \\ {e}^{-2x}\cdot \frac{\text{d}y}{\text{d}x}-2{e}^{-2x}\cdot y & =2{e}^{2x}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{e}^{-2x}) & =2{e}^{2x} \\ \int \frac{\text{d}}{\text{d}x}(y{e}^{-2x})\text{d}x & =\int 2{e}^{2x}\,\text{d}x \\ y{e}^{-2x} & ={e}^{2x}+C \\ y & ={e}^{4x}+C{e}^{2x}\end{aligned}
$$

---

## power_constant — moderate
Profile: `power_constant_authored`; parameters: `{'n': 6, 'b': 4}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{6}{x}y=4,\,x>0.
$$

Select the correct options below:

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- $\operatorname{ln}⁡x$
- $\frac{1}{x}$
- ${x}^{5}$
- ${x}^{6}$ **correct**
**field-2**
- $\frac{4x}{7}+\frac{C}{{x}^{5}}$
- $\frac{4x}{7}+\frac{C}{{x}^{6}}$ **correct**
- $\frac{2x}{3}+\frac{C}{{x}^{5}}$
- $\frac{2x}{3}+\frac{C}{{x}^{6}}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{6}{x}$ and $Q(x)=4.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (6/x)\,dx} \\  & ={e}^{6\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{6})} \\  & ={x}^{6}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{6}$ as follows:

$$
\begin{aligned}{x}^{6}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{6}{x}y) & ={x}^{6}\cdot 4 \\ {x}^{6}\frac{\text{d}y}{\text{d}x}+6{x}^{5}y & =4{x}^{6}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{6})\,dx & =\int 4{x}^{6}\,\text{d}x \\ y{x}^{6} & =\frac{4{x}^{7}}{7}+C \\ y & =\frac{4x}{7}+\frac{C}{{x}^{6}}.\end{aligned}
$$

---

## power_constant — moderate
Profile: `power_constant_authored`; parameters: `{'n': 4, 'b': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{4}{x}y=3,\,x>0.
$$

Select the correct options below:

$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-1**
- ${x}^{3}$
- $\operatorname{ln}⁡x$
- ${x}^{4}$ **correct**
- $\frac{1}{x}$
**field-2**
- $\frac{3x}{5}+\frac{C}{{x}^{4}}$ **correct**
- $\frac{3x}{5}+\frac{C}{{x}^{3}}$
- $\frac{3x}{4}+\frac{C}{{x}^{4}}$
- $\frac{3x}{4}+\frac{C}{{x}^{3}}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{4}{x}$ and $Q(x)=3.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,dx} \\  & ={e}^{\int (4/x)\,dx} \\  & ={e}^{4\operatorname{ln}⁡x} \\  & ={e}^{\operatorname{ln}⁡({x}^{4})} \\  & ={x}^{4}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{4}$ as follows:

$$
\begin{aligned}{x}^{4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{4}{x}y) & ={x}^{4}\cdot 3 \\ {x}^{4}\frac{\text{d}y}{\text{d}x}+4{x}^{3}y & =3{x}^{4}\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\int \frac{d}{dx}(y{x}^{4})\,dx & =\int 3{x}^{4}\,\text{d}x \\ y{x}^{4} & =\frac{3{x}^{5}}{5}+C \\ y & =\frac{3x}{5}+\frac{C}{{x}^{4}}.\end{aligned}
$$

---

## power_sin — hard
Profile: `power_sin_authored`; parameters: `{'n': 6, 'r': 3}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{6}{x}y=\frac{\operatorname{sin}⁡3x}{{x}^{5}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{6}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{5}}}{3}+\frac{C}{{x}^{5}}$
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{5}}}{9}+\frac{\frac{\operatorname{cos}⁡3x}{{x}^{6}}}{3}+\frac{C}{{x}^{6}}$
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{5}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{6}}}{3}+\frac{C}{{x}^{5}}$
- $\frac{\frac{\operatorname{sin}3x}{{x}^{6}}}{9}-\frac{\frac{\operatorname{cos}3x}{{x}^{5}}}{3}+\frac{C}{{x}^{6}}$ **correct**
- $\frac{\frac{\operatorname{sin}⁡3x}{{x}^{6}}}{9}+\frac{\frac{\operatorname{cos}⁡3x}{{x}^{5}}}{3}+\frac{C}{{x}^{5}}$
**field-1**
- ${e}^{{x}^{6}}$
- ${x}^{6}$ **correct**
- $\frac{6}{x}$
- ${e}^{6/x}$

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{6}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡3x}{{x}^{5}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (6/x)\,\text{d}x} \\  & ={e}^{6\operatorname{ln}⁡x} \\  & ={x}^{6}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{6}$ as follows:

$$
\begin{aligned}{x}^{6}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{6}{x}y) & ={x}^{6}\cdot \frac{\operatorname{sin}⁡3x}{{x}^{5}} \\ {x}^{6}\frac{\text{d}y}{\text{d}x}+6{x}^{5}y & =x\operatorname{sin}⁡3x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{6}) & =x\operatorname{sin}⁡3x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{6})\text{d}x & =\int x\operatorname{sin}⁡3x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{sin}⁡3x,$ and $v=-\frac{\operatorname{cos}⁡3x}{3}.$ Then, we have

$$
\begin{aligned}y{x}^{6} & =\int x\operatorname{sin}⁡3x\,\text{d}x \\ y{x}^{6} & =x(-\frac{\operatorname{cos}⁡3x}{3})-\int (-\frac{\operatorname{cos}⁡3x}{3})\cdot 1\,\text{d}x \\ y{x}^{6} & =x(-\frac{\operatorname{cos}⁡3x}{3})+\int \frac{\operatorname{cos}⁡3x}{3}\,\text{d}x \\ y{x}^{6} & =-\frac{x\operatorname{cos}⁡3x}{3}+\frac{\operatorname{sin}⁡3x}{9}\,+C \\ y & =\frac{\frac{\operatorname{sin}⁡3x}{{x}^{6}}}{9}-\frac{\frac{\operatorname{cos}⁡3x}{{x}^{5}}}{3}+\frac{C}{{x}^{6}}.\end{aligned}
$$

---

## power_sin — hard
Profile: `power_sin_authored`; parameters: `{'n': 4, 'r': 1}`.

Consider the differential equation

$$
\frac{\text{d}y}{\text{d}x}+\frac{4}{x}y=\frac{\operatorname{sin}⁡x}{{x}^{3}},\,x>0.
$$

Select the correct options below.$\,$ An integrating factor for this equation is $I(x)=$ {{field-1}}.

$\,$ The general solution is given by $y(x)=$ {{field-2}}.

**field-2**
- $\frac{\operatorname{sin}⁡x}{{x}^{3}}+\frac{\operatorname{cos}⁡x}{{x}^{4}}+\frac{C}{{x}^{4}}$
- $\frac{\operatorname{sin}⁡x}{{x}^{4}}+\frac{\operatorname{cos}⁡x}{{x}^{3}}+\frac{C}{{x}^{3}}$
- $\frac{\operatorname{sin}⁡x}{{x}^{3}}-\frac{\operatorname{cos}⁡x}{{x}^{4}}+\frac{C}{{x}^{3}}$
- $\frac{\operatorname{sin}⁡x}{{x}^{4}}-\frac{\operatorname{cos}⁡x}{{x}^{3}}+\frac{C}{{x}^{3}}$
- $\frac{\operatorname{sin}x}{{x}^{4}}-\frac{\operatorname{cos}x}{{x}^{3}}+\frac{C}{{x}^{4}}$ **correct**
**field-1**
- $\frac{4}{x}$
- ${e}^{{x}^{4}}$
- ${e}^{4/x}$
- ${x}^{4}$ **correct**

**Worked solution**

This equation is in the standard form

$$
\frac{\text{d}y}{\text{d}x}+P(x)y=Q(x)
$$

with $P(x)=\frac{4}{x}$ and $Q(x)=\frac{\operatorname{sin}⁡x}{{x}^{3}}.$ We proceed to find an integrating factor $I(x)$ using the definition:

$$
\begin{aligned}I(x) & ={e}^{\int P(x)\,\text{d}x} \\  & ={e}^{\int (4/x)\,\text{d}x} \\  & ={e}^{4\operatorname{ln}⁡x} \\  & ={x}^{4}\end{aligned}
$$

Now, we multiply our differential equation through by $I(x)={x}^{4}$ as follows:

$$
\begin{aligned}{x}^{4}\cdot (\frac{\text{d}y}{\text{d}x}+\frac{4}{x}y) & ={x}^{4}\cdot \frac{\operatorname{sin}⁡x}{{x}^{3}} \\ {x}^{4}\frac{\text{d}y}{\text{d}x}+4{x}^{3}y & =x\operatorname{sin}⁡x\end{aligned}
$$

Finally, we rewrite the left hand side as $\frac{\text{d}}{\text{d}x}(y\cdot I(x))$ and carry out the integration:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(y{x}^{4}) & =x\operatorname{sin}⁡x \\ \int \frac{\text{d}}{\text{d}x}(y{x}^{4})\text{d}x & =\int x\operatorname{sin}⁡x\,\text{d}x\end{aligned}
$$

To solve this integral, we integrate by parts. 

$$
\int u{v}^{′}\,\text{d}x=uv-\int {u}^{′}v\,\text{d}x
$$

Let $u=x,{u}^{′}=1,{v}^{′}=\operatorname{sin}⁡x,$ and $v=-\operatorname{cos}⁡x.$ Then, we have

$$
\begin{aligned}y{x}^{4} & =\int x\operatorname{sin}⁡x\,\text{d}x \\ y{x}^{4} & =x(-\operatorname{cos}⁡x)-\int (-\operatorname{cos}⁡x)\cdot 1\,\text{d}x \\ y{x}^{4} & =-x\operatorname{cos}⁡x+\int \operatorname{cos}⁡x\,\text{d}x \\ y{x}^{4} & =-x\operatorname{cos}⁡x+\operatorname{sin}⁡x\,+C \\ y & =\frac{\operatorname{sin}⁡x}{{x}^{4}}-\frac{\operatorname{cos}⁡x}{{x}^{3}}+\frac{C}{{x}^{4}}.\end{aligned}
$$
