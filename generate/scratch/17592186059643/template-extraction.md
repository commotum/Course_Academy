# Template extraction

## 1. Specific originals

All exact decoded prompt/solution strings, attribute-presence flags, parameters, correct indices and complete banks appear in `template-masks.json`; `source.json` is the original schema-shaped evidence. There are no plots. The source uses function-application U+2061, operatorname and plain braced sin/cos notations. Raw replay keeps them byte for byte. It does not infer an escaping anomaly from JSON display.

### observed_q_1579 / 17592186060072

What is $\frac{\cos x}{1 - \sin x} - \tan x$?

Original argument: `x`; level missing. Source solution absent.

Bank (complete displayed values):

- 1. `\sec^{2} x` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `-\sec x` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `2\sec^{2} x` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `2\sec x` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\sec x` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

### observed_q_23522 / 17592186060226

What is $\cos θ + \frac{\sin^{2} θ}{\cos θ}$?

Original argument: `θ`; level missing. Source solution absent.

Bank (complete displayed values):

- 1. `\sec θ` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\sec θ + 2` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `-\sec θ + 2` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `-\sec θ` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `2\sec θ` — designation unavailable. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

### observed_q_119764 / 17592186253594

Simplify the trigonometric expression $\operatorname{tan}⁡x-\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x}.$

Original argument: `x`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `\frac{1-{cos}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

First, we rewrite the first term using the definition of $\operatorname{tan}⁡x.$ This gives

$$
\operatorname{tan}⁡x-\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x}=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}-\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x}.
$$

Now, we put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}-\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x} & =\frac{\operatorname{sin}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x\operatorname{sin}⁡x}-\frac{(1-\operatorname{cos}⁡x)\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x} \\  & =\frac{{sin}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}-\frac{\operatorname{cos}⁡x-{cos}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x} \\  & =\frac{{sin}^{2}⁡x-(\operatorname{cos}⁡x-{cos}^{2}⁡x)}{\operatorname{sin}⁡x\operatorname{cos}⁡x} \\  & =\frac{{sin}^{2}⁡x-\operatorname{cos}⁡x+{cos}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{{sin}^{2}⁡x-\operatorname{cos}⁡x+{cos}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x} & =\frac{({sin}^{2}⁡x+{cos}^{2}⁡x)-\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x} \\  & =\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}\end{aligned}
$$

Therefore, we conclude that:

$$
\operatorname{tan}⁡x-\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x}=\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}
$$

### observed_q_119767 / 17592186253596

$\frac{\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta }+\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta }=$

Original argument: `\theta`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\operatorname{csc}⁡\theta \operatorname{sec}⁡\theta ` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\operatorname{sin}⁡\theta \operatorname{sec}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `\operatorname{csc}⁡\theta \operatorname{cos}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `2\operatorname{sec}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `2\operatorname{csc}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta }+\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta } & =\frac{\operatorname{sin}⁡\theta \operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta }+\frac{\operatorname{cos}⁡\theta \operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta } \\  & =\frac{{sin}^{2}⁡\theta }{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta }+\frac{{cos}^{2}⁡\theta }{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta } \\  & =\frac{{sin}^{2}⁡\theta +{cos}^{2}⁡\theta }{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta }\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{{sin}^{2}⁡\theta +{cos}^{2}⁡\theta }{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta } & =\frac{1}{\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta } \\  & =\frac{1}{\operatorname{sin}⁡\theta }\cdot \frac{1}{\operatorname{cos}⁡\theta } \\  & =\operatorname{csc}⁡\theta \operatorname{sec}⁡\theta \end{aligned}
$$

Therefore, we conclude that

$$
\frac{\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta }+\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta }=\operatorname{csc}⁡\theta \operatorname{sec}⁡\theta .
$$

### observed_q_119770 / 17592186253599

Simplify the trigonometric expression $\frac{{cos}^{2}⁡x}{1+\operatorname{sin}⁡x}+\operatorname{sin}⁡x.$

Original argument: `x`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\operatorname{cos}⁡x+1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `-\operatorname{sin}⁡x` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `1-\operatorname{sin}⁡x` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `1` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\operatorname{cos}⁡x` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{{cos}^{2}⁡x}{1+\operatorname{sin}⁡x}+\operatorname{sin}⁡x & =\frac{{cos}^{2}⁡x}{1+\operatorname{sin}⁡x}+\frac{\operatorname{sin}⁡x}{1} \\  & =\frac{{cos}^{2}⁡x}{1+\operatorname{sin}⁡x}+\frac{\operatorname{sin}⁡x(1+\operatorname{sin}⁡x)}{1(1+\operatorname{sin}⁡x)} \\  & =\frac{{cos}^{2}⁡x+\operatorname{sin}⁡x(1+\operatorname{sin}⁡x)}{1+\operatorname{sin}⁡x}\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{{cos}^{2}⁡x+\operatorname{sin}⁡x(1+\operatorname{sin}⁡x)}{1+\operatorname{sin}⁡x} & =\frac{{cos}^{2}⁡x+\operatorname{sin}⁡x+{sin}^{2}⁡x}{1+\operatorname{sin}⁡x} \\  & =\frac{({sin}^{2}⁡x+{cos}^{2}⁡x)+\operatorname{sin}⁡x}{1+\operatorname{sin}⁡x} \\  & =\frac{1+\operatorname{sin}⁡x}{1+\operatorname{sin}⁡x} \\  & =1\end{aligned}
$$

Therefore, we conclude that

$$
\frac{{cos}^{2}⁡x}{2+\operatorname{sin}⁡x}+\operatorname{sin}⁡x=1.
$$

### observed_q_119773 / 17592186253600

$1+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta }=$

Original argument: `\theta`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\frac{2}{1+{sin}^{2}⁡\theta }` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\frac{2}{1+\operatorname{sin}⁡\theta }` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `1+{sin}^{2}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `\frac{1}{1+\operatorname{sin}⁡\theta }` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\frac{1}{1+{sin}^{2}⁡\theta }` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}1+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta } & =\frac{1}{1}+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}} \\  & =\frac{1\cdot (1+{sin}^{2}⁡\theta )}{1\cdot (1+{sin}^{2}⁡\theta )}+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}} \\  & =\frac{1+{sin}^{2}⁡\theta }{1+{sin}^{2}⁡\theta }+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta } \\  & =\frac{1+{sin}^{2}⁡\theta +{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta }\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{1+{sin}^{2}⁡\theta +{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta } & =\frac{1+1}{1+{sin}^{2}⁡\theta } \\  & =\frac{2}{1+{sin}^{2}⁡\theta }\end{aligned}
$$

Therefore, we conclude that

$$
1+\frac{{cos}^{2}⁡\theta }{1+{sin}^{2}⁡\theta }=\frac{2}{1+{sin}^{2}⁡\theta }.
$$

### observed_q_119775 / 17592186253602

Simplify the trigonometric expression $\operatorname{sin}⁡x-\frac{{cos}^{2}⁡x}{1-\operatorname{sin}⁡x}.$

Original argument: `x`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\operatorname{sin}⁡x` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `-\operatorname{sin}⁡x` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `-1` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\operatorname{sin}⁡x+1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\operatorname{sin}⁡x-\frac{{cos}^{2}⁡x}{1-\operatorname{sin}⁡x} & =\frac{\operatorname{sin}⁡x}{1}-\frac{{cos}^{2}⁡x}{1-\operatorname{sin}⁡x} \\  & =\frac{\operatorname{sin}⁡x(1-\operatorname{sin}⁡x)}{1-\operatorname{sin}⁡x}-\frac{{cos}^{2}⁡x}{1-\operatorname{sin}⁡x} \\  & =\frac{\operatorname{sin}⁡x(1-\operatorname{sin}⁡x)-{cos}^{2}⁡x}{1-\operatorname{sin}⁡x}\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{\operatorname{sin}⁡x(1-\operatorname{sin}⁡x)-{cos}^{2}⁡x}{1-\operatorname{sin}⁡x} & =\frac{\operatorname{sin}⁡x-{sin}^{2}⁡x-{cos}^{2}⁡x}{1-\operatorname{sin}⁡x} \\  & =\frac{\operatorname{sin}⁡x-({sin}^{2}⁡x+{cos}^{2}⁡x)}{1-\operatorname{sin}⁡x} \\  & =\frac{\operatorname{sin}⁡x-1}{1-\operatorname{sin}⁡x} \\  & =\frac{-(1-\operatorname{sin}⁡x)}{1-\operatorname{sin}⁡x} \\  & =-1\end{aligned}
$$

Therefore, we conclude that

$$
\operatorname{sin}⁡x-\frac{{cos}^{2}⁡x}{1-\operatorname{sin}⁡x}=-1.
$$

### observed_q_43291 / 17592186329714

Simplify $\frac{\operatorname{cos}⁡\theta }{1-\operatorname{sin}⁡\theta }+\frac{1-\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta }.$

Original argument: `\theta`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `2{sec}^{2}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\operatorname{sec}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `{sec}^{2}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `2\operatorname{sec}⁡\theta ` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `1-\operatorname{sec}⁡\theta ` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{\operatorname{cos}⁡\theta }{1-\operatorname{sin}⁡\theta }+\frac{1-\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta } & =\frac{\operatorname{cos}⁡\theta \operatorname{cos}⁡\theta }{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta }+\frac{(1-\operatorname{sin}⁡\theta )(1-\operatorname{sin}⁡\theta )}{\operatorname{cos}⁡\theta (1-\operatorname{sin}⁡\theta )} \\  & =\frac{{cos}^{2}⁡\theta +{(1-\operatorname{sin}⁡\theta )}^{2}}{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta }\end{aligned}
$$

Finally, we simplify as follows:

$$
\begin{aligned}\frac{{cos}^{2}⁡\theta +{(1-\operatorname{sin}⁡\theta )}^{2}}{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } & =\frac{{cos}^{2}⁡\theta +1-2\operatorname{sin}⁡\theta +{sin}^{2}⁡\theta }{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } \\  & =\frac{({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )+1-2\operatorname{sin}⁡\theta }{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } \\  & =\frac{1+1-2\operatorname{sin}⁡\theta }{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } \\  & =\frac{2-2\operatorname{sin}⁡\theta }{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } \\  & =\frac{2(1-\operatorname{sin}⁡\theta )}{(1-\operatorname{sin}⁡\theta )\operatorname{cos}⁡\theta } \\  & =\frac{2}{\operatorname{cos}⁡\theta } \\  & =2\operatorname{sec}⁡\theta \end{aligned}
$$

Therefore, we conclude that

$$
\frac{\operatorname{cos}⁡\theta }{1-\operatorname{sin}⁡\theta }+\frac{1-\operatorname{sin}⁡\theta }{\operatorname{cos}⁡\theta }=2\operatorname{sec}⁡\theta .
$$

### observed_q_43298 / 17592186329718

$\operatorname{sin}⁡t(\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}+\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})=$

Original argument: `t`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\operatorname{sec}⁡t+1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\operatorname{sec}⁡t` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `-\operatorname{sec}⁡t-1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `-\operatorname{sec}⁡t+1` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `-\operatorname{sec}⁡t` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

First, we expand the parentheses:

$$
\begin{aligned}\operatorname{sin}⁡t(\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}+\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}) & =\operatorname{sin}⁡t\cdot \frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}+\operatorname{sin}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t} \\  & =\frac{\operatorname{cos}⁡t\cdot \operatorname{sin}⁡t}{\operatorname{sin}⁡t}+\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t} \\  & =\frac{\operatorname{cos}⁡t\cdot \cancel{\operatorname{sin}⁡t}}{\cancel{\operatorname{sin}⁡t}}+\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t} \\  & =\operatorname{cos}⁡t+\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t}\end{aligned}
$$

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\operatorname{cos}⁡\theta +\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t} & =\frac{\operatorname{cos}⁡t}{1}+\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t} \\  & =\frac{\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t}{1\cdot \operatorname{cos}⁡t}+\frac{{sin}^{2}⁡t}{\operatorname{cos}⁡t} \\  & =\frac{{cos}^{2}⁡t+{sin}^{2}⁡t}{\operatorname{cos}⁡t}\end{aligned}
$$

Finally, we simplify using the Pythagorean identity, as follows:

$$
\begin{aligned}\frac{{cos}^{2}⁡t+{sin}^{2}⁡t}{\operatorname{cos}⁡t}=\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t\end{aligned}
$$

Therefore, we conclude that

$$
\operatorname{sin}⁡t(\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}+\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})=\operatorname{sec}⁡t.
$$

### observed_q_65254 / 17592186335821

$\frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}+\operatorname{sin}⁡x=$

Original argument: `x`; level moderate. Source solution present.

Bank (complete displayed values):

- 1. `\frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\frac{1-\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `\frac{1}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `\frac{{sin}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\frac{1+\operatorname{sin}⁡x\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}+\operatorname{sin}⁡x & =\frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}+\frac{\operatorname{sin}⁡x}{1} \\  & \frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}+\frac{\operatorname{sin}⁡x(\operatorname{sin}⁡x+\operatorname{cos}⁡x)}{1(\operatorname{sin}⁡x+\operatorname{cos}⁡x)} \\  & =\frac{{cos}^{2}⁡x+\operatorname{sin}⁡x(\operatorname{sin}⁡x+\operatorname{cos}⁡x)}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}\end{aligned}
$$

Finally, we simplify as follows:

$$
\begin{aligned}\frac{{cos}^{2}⁡x+\operatorname{sin}⁡x(\operatorname{sin}⁡x+\operatorname{cos}⁡x)}{\operatorname{sin}⁡x+\operatorname{cos}⁡x} & =\frac{{cos}^{2}⁡x+{sin}^{2}⁡x+\operatorname{sin}⁡x\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x} \\  & =\frac{({cos}^{2}⁡x+{sin}^{2}⁡x)+\operatorname{sin}⁡x\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x} \\  & =\frac{1+\operatorname{sin}⁡x\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}\end{aligned}
$$

Therefore, we conclude that

$$
\frac{{cos}^{2}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}+\operatorname{sin}⁡x=\frac{1+\operatorname{sin}⁡x\operatorname{cos}⁡x}{\operatorname{sin}⁡x+\operatorname{cos}⁡x}.
$$

### observed_q_72715 / 17592186341847

Simplify the trigonometric expression $\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+\operatorname{tan}⁡x.$

Original argument: `x`; level hard. Source solution present.

Bank (complete displayed values):

- 1. `\frac{1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 2. `\frac{2\operatorname{cos}⁡x-1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 3. `\frac{\operatorname{cos}⁡x+1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — designated correct. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 4. `\frac{2\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

- 5. `\frac{\operatorname{cos}⁡x-1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}` — incorrect. Parameterized expression shape: replace complete argument token and optionally dualize sin↔cos, tan↔cot, sec↔csc. Mathematical meaning is parsed exactly; error intention is unresolved.

Complete ordered solution mask:

First, we rewrite the second term using the definition of $\operatorname{tan}⁡x.$ This gives:

$$
\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+\operatorname{tan}⁡x=\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}
$$

We put both terms over a common denominator, and combine the two fractions:

$$
\begin{aligned}\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x} & =\frac{(1+\operatorname{cos}⁡x)\operatorname{cos}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}+\frac{\operatorname{sin}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x\operatorname{sin}⁡x} \\  & =\frac{\operatorname{cos}⁡x+{cos}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}+\frac{{sin}^{2}⁡x}{\operatorname{cos}⁡x\operatorname{sin}⁡x} \\  & =\frac{\operatorname{cos}⁡x+{cos}^{2}⁡x+{sin}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x}\end{aligned}
$$

Finally, we simplify as follows:

$$
\begin{aligned}\frac{\operatorname{cos}⁡x+{cos}^{2}⁡x+{sin}^{2}⁡x}{\operatorname{sin}⁡x\operatorname{cos}⁡x} & =\frac{\operatorname{cos}⁡x+({cos}^{2}⁡x+{sin}^{2}⁡x)}{\operatorname{sin}⁡x\operatorname{cos}⁡x} \\  & =\frac{\operatorname{cos}⁡x+1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}\end{aligned}
$$

Therefore, we conclude that:

$$
\frac{1+\operatorname{cos}⁡x}{\operatorname{sin}⁡x}+\operatorname{tan}⁡x=\frac{\operatorname{cos}⁡x+1}{\operatorname{sin}⁡x\operatorname{cos}⁡x}
$$

## 2. Generalized method

Rewrite any tan/cot into sin/cos, put both terms over a common denominator, retain ordered products and expansion, collect the matching sin² and cos² contributions, use sin²+cos²=1, and simplify on the original nonzero-denominator domain. Source solutions retain all original prose and exact row sequence. The one missing easy family still requires combining two terms; it never gives an already-combined numerator.

## 3. Components and banks

`template-masks.json` fully enumerates prompt, argument, function orientation, solution-presence and difficulty-presence flags, ordered solution, five option masks and any observed correct index. Every option is transformed by the same complete mathematical token recipe. This is a parameterized shape recovery rather than a source-return branch or scalar-answer lookup. Swapping sin and cos changes every numerator, denominator, reciprocal and assessed mathematical object consistently. Its limits are explicit: source option shapes establish reproduction; they do not prove the original author's misconception recipes. Both raw and repaired observed profiles therefore remain evidence-only.

## 4. Reusable masks, bounds and calculations

Fixed: sentences, radio selection field, five complete options and each original mathematical stage sequence. Variable: complete argument token and whole function orientation. Conditional: only the documented source repairs; raw difficulty/solution/correct presence remains absent whenever absent in the original. Source banking stays separate per original. Authored default banks and reduced rational bounds are below. No learner-facing error labels are added.

### Supported repairs and truthful fidelity denominators

- 17592186253599: concluding denominator 2+sin x contradicts printed prompt and all earlier rows, which use 1+sin x. Only that final 2 is repaired to 1. Raw original retained.

- 17592186253600: two intermediate denominators omit theta after sin². Restore the same theta used in prompt and surrounding rows.

- 17592186329718: common-denominator opening contains cos theta in an otherwise t expression. Restore t.

- 17592186335821: second aligned row lacks an equals sign. Insert it.

- 17592186060072 and 17592186060226: no original correct refs, difficulty or solution. Raw replay omits them. Repaired evidence adds independently inferred correct sec and complete formal stages; q1579 receives inferred Moderate and q23522 receives inferred Easy, consistently in the masks, cases, API and repaired record. Raw outputs retain no difficulty attribute. They cannot count as matched original designations or solutions.

Exact source fidelity is 11 prompts/11, 55 displayed choices/55, 11 full banks/11, 9 observed correct designations/9 present, and 9 exact solutions/9 present; 2 original designations and solutions are unavailable. Correctness of raw teaching strings is a separate measure; three sources have incorrect/incomplete mathematics, and a fourth has the missing-equality presentation issue.

### Authored default families and within-level variety

Easy (missing observed level): `a G + a F²/G`, where F/G are sine/cosine in either orientation. Convert a G to a G²/G; combine squared numerator components; apply identity; reduce to a/G. The unrated cos+sin²/cos source directly anchors the simpler common-denominator operation; canonical example and prerequisites justify the method. A reduced rational coefficient changes the assessed answer without adding a new operation. Both terms remain nonzero.

Moderate (observed workload): `a F/G+a G/F` and `a+a G²/(b+F²)`, with b positive in the latter. The former follows the observed crossed-fraction sum; the latter follows observed 1+cos²/(1+sin²). Both combine original terms, form squared numerator components, apply identity and simplify, with the original source family's denominators retained. These are unordered source-anchored alternatives within moderate, not a progression.

Hard (observed workload): `(a+b G)/F+b F/G` with nonzero independent a,b. This retains the observed quotient rewrite, cross denominator, expansion, linear G term and balanced squared terms. No values can remove either defining component. Dual orientation substitutes cot for tan.

All levels: a and applicable b are reduced rationals with nonzero numerator magnitude at most 6, denominator at most 3, and magnitude at most 4. In squared-shift b must be positive. Combined a*b and a±b numerator magnitude is at most 36 and denominator at most 9. Samplers and explicit calls apply identical guards to reduced values, so scaling 8/2 normalizes to 4 while 100/25 also normalizes to 4 (eligible); 7 or denominator 4 is rejected. Arguments and bank aliases are incidental and excluded from meaningful-task fingerprints. Moderate crossed dual orientation is mathematically symmetric and does not inflate its task count. Finite task counts come from exhaustive enumeration in validation.json.

### Authored complete operation banks

Easy: correct a/G; drop denominator to a; use wrong reciprocal a/F; subtract the squared components a(G²−F²)/G; multiply squared components aG²F²/G.

Crossed moderate: correct a/(FG); omit one denominator to a/G; omit the other to a/F; subtract crossed squared components a(F²−G²)/(FG); multiply them aF²G²/(FG).

Squared-shift moderate: correct a(b+1)/(b+F²); omit the standalone term to aG²/(b+F²); drop denominator square to a(b+1)/(b+F); omit the identity contribution to ab/(b+F²); invert the cancellation operation to a(b+F²).

Hard: correct (aG+b)/(FG); omit the linear contribution b/(FG); flip the identity contribution sign (aG−b)/(FG); subtract squared components (aG+b(G²−F²))/(FG); omit the identity contribution aG/(FG).

A complete bank is selected before construction. Every option is parsed, compared as a complete rational trig expression on the original domain and rejected with the entire instance upon equivalence. Explicit invalid parameters raise; samplers retry only complete instances.
