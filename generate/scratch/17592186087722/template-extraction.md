# Template extraction

## Stage 1: specific source descriptions

All 23 raw source prompts, field fragments, complete banks, and full solution prose follow. Raw snapshots remain in source.json; absent components are explicitly marked.

### q-16203

Rating: unrated; authored moderate. Assessed: x,y. Domain: Interval(0, oo). Functions: x=t**2 + 6*t, y=sqrt(t).

Given that a curve is defined parametrically as
$x = t^{2} + 6t, y = \sqrt{t}, t \ge 0$,
what are the ranges of $x$ and $y$?

Full worked solution:

**Absent; authored solution required.**

Field `selection`, :answer-field.type/radio; observed correct: `None`.

- `x \ge 0, y \ge 0` → {'x': 'Interval(0, oo)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \le 9, y \ge 0` → {'x': 'Interval(-oo, 9)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \ge - 9, y \ge 0` → {'x': 'Interval(-9, oo)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \ge 3, y \le 3` → {'x': 'Interval(3, oo)', 'y': 'Interval(-oo, 3)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \le 3, y \le 0` → {'x': 'Interval(-oo, 3)', 'y': 'Interval(-oo, 0)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-16205

Rating: unrated; authored moderate. Assessed: x. Domain: Reals. Functions: x=t**2 - 4*t, y=t**2.

Given that a curve is defined parametrically as
$x = t^{2} - 4t, y = t^{2}, t ∈ (- ∞, ∞)$,
determine the range of $x$.

Full worked solution:

**Absent; authored solution required.**

Field `selection`, :answer-field.type/radio; observed correct: `None`.

- `x \le 5` → {'x': 'Interval(-oo, 5)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \ge - 4` → {'x': 'Interval(-4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \ge - 8` → {'x': 'Interval(-8, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x > 6` → {'x': 'Interval.open(6, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x \le - 4` → {'x': 'Interval(-oo, -4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-16149

Rating: observed moderate. Assessed: x,y. Domain: Reals. Functions: x=t**2 + t, y=t**2 - 2.

Given that a curve is defined parametrically as

$$
x={t}^{2}+t,\,\,\,y={t}^{2}-2,\,t\in (-\infty ,\infty ),
$$

determine the ranges of $x$ and $y.$

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & ={t}^{2}+t \\  & ={(t+\frac{1}{2})}^{2}-{(\frac{1}{2})}^{2} \\  & ={(t+\frac{1}{2})}^{2}-\frac{1}{4}\end{aligned}
$$

Since ${(t+\frac{1}{2})}^{2}\ge 0,$ we can conclude that $x\ge -\frac{1}{4}.$

- To find the range of $y,$ notice that ${t}^{2}\ge 0.$ Therefore, we can conclude that $y\ge -2.$

So, the ranges are $x\ge -\frac{1}{4}$ and $y\ge -2.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge -\frac{1}{4},\,y\ge -2`.

- `x\ge -4,\,y\ge 0` → {'x': 'Interval(-4, oo)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le \frac{1}{2},\,y\le -4` → {'x': 'Interval(-oo, 1/2)', 'y': 'Interval(-oo, -4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le -\frac{1}{2},\,y\ge 1` → {'x': 'Interval(-oo, -1/2)', 'y': 'Interval(1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -\frac{1}{4},\,y\ge -2` → {'x': 'Interval(-1/4, oo)', 'y': 'Interval(-2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge \frac{1}{4},\,y\le -2` → {'x': 'Interval(1/4, oo)', 'y': 'Interval(-oo, -2)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-73604

Rating: observed moderate. Assessed: x. Domain: Interval(0, oo). Functions: x=t**2 - 2*t - 1, y=sqrt(t) - 4.

Given that a curve is defined parametrically as

$$
x={t}^{2}-2t-1,\,\,\,y=\sqrt{t}-4,\,t\ge 0,
$$

determine the range of $x.$

Full worked solution:

To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & ={t}^{2}-2t-1 \\  & ={(t-1)}^{2}-{1}^{2}-1 \\  & ={(t-1)}^{2}-2\end{aligned}
$$

Since ${(t-1)}^{2}\ge 0,$ we can conclude that $x\ge -2.$

**No original fields.** A supported authored radio bank is required; no observed bank count.

### q-123763

Rating: observed moderate. Assessed: x. Domain: Interval(0, oo). Functions: x=2*sqrt(t + 9), y=t + 1.

Given that a curve is defined parametrically as

$$
x=2\sqrt{t+9},\,\,\,y=t+1,\,t\ge 0,
$$

what is the range of $x?$

Full worked solution:

To find the range of $x,$ note that $\sqrt{t+9}\ge 3$ for all $t\ge 0.$ Consequently, $x=2\sqrt{t+9}\ge 6.$

Therefore, we can conclude that $x\ge 6.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge 6`.

- `x\ge 3` → {'x': 'Interval(3, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 6` → {'x': 'Interval(6, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 18` → {'x': 'Interval(18, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 2` → {'x': 'Interval(2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 0` → {'x': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-123764

Rating: observed moderate. Assessed: x. Domain: Interval(1, oo). Functions: x=3*t - 7, y=1 - t.

Given that a curve is defined parametrically as

$$
x=3t-7,\,\,\,y=1-t,\,t\ge 1,
$$

what is the range of $x?$

Full worked solution:

To find the range of $x,$ note that $x=3t-7\ge -4$ for all $t\ge 1.$ 

Consequently, the range of $x$ is $x\ge -4.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge -4`.

- `x\le -4` → {'x': 'Interval(-oo, -4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 3` → {'x': 'Interval(3, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -4` → {'x': 'Interval(-4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 3` → {'x': 'Interval(-oo, 3)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 0` → {'x': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-123765

Rating: observed moderate. Assessed: x. Domain: Interval(-oo, 0). Functions: x=1 - 4*t, y=t**2 - 1.

Given that a curve is defined parametrically as

$$
x=1-4t,\,\,\,y={t}^{2}-1,\,t\le 0,
$$

what is the range of $x?$

Full worked solution:

To find the range of $x,$ note that $x=1-4t\ge 1$ for all $t\le 0.$ 

Consequently, the range of $x$ is $x\ge 1.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge 1`.

- `x\le -2` → {'x': 'Interval(-oo, -2)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 1` → {'x': 'Interval(1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -4` → {'x': 'Interval(-4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 1` → {'x': 'Interval(-oo, 1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 0` → {'x': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-123767

Rating: observed moderate. Assessed: y. Domain: Interval.open(0, oo). Functions: x=1/t, y=1 - t.

Given that a curve is defined parametrically as

$$
x=\frac{1}{t},\,\,\,y=1-t,\,t>0,
$$

what is the range of $y?$

Full worked solution:

To find the range of $y,$ note that $y=1-t<1$ for all $t>0.$ 

Consequently, the range of $y$ is $y<1.$

Field `selection`, :answer-field.type/radio; observed correct: `y<1`.

- `y>-1` → {'y': 'Interval.open(-1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y>1` → {'y': 'Interval.open(1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y<1` → {'y': 'Interval.open(-oo, 1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y<-1` → {'y': 'Interval.open(-oo, -1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y>0` → {'y': 'Interval.open(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-123768

Rating: observed moderate. Assessed: y. Domain: Interval(0, oo). Functions: x=3*t + 2, y=4*sqrt(t) - 1.

Given that a curve is defined parametrically as

$$
x=3t+2,\,\,\,y=4\sqrt{t}-1,\,t\ge 0,
$$

what is the range of $y?$

Full worked solution:

To find the range of $y,$ note that $4\sqrt{t}\ge 0$ for all $t\ge 0.$ Consequently, $y=4\sqrt{t}-1\ge -1.$

Therefore, we can conclude that $y\ge -1.$

Field `selection`, :answer-field.type/radio; observed correct: `y\ge -1`.

- `y\le 4` → {'y': 'Interval(-oo, 4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y\ge 4` → {'y': 'Interval(4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y\ge -1` → {'y': 'Interval(-1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y\le -1` → {'y': 'Interval(-oo, -1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `y\ge 1` → {'y': 'Interval(1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-16199

Rating: observed moderate. Assessed: x. Domain: Reals. Functions: x=t**2 - 2*t, y=3 - t.

Given that a curve is defined parametrically as

$$
x={t}^{2}-2t,\,\,\,y=3-t,\,t\in (-\infty ,\infty ),
$$

determine the range of $x.$

Full worked solution:

To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & ={t}^{2}-2t \\  & ={(t-1)}^{2}-{(1)}^{2} \\  & ={(t-1)}^{2}-1\end{aligned}
$$

Since ${(t-1)}^{2}\ge 0,$ we can conclude that $x\ge -1.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge -1`.

- `x\ge -1` → {'x': 'Interval(-1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -4` → {'x': 'Interval(-4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `-2\le x\le 1` → {'x': 'Interval(-2, 1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `-4\le x\le -2` → {'x': 'Interval(-4, -2)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 0` → {'x': 'Interval(-oo, 0)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-16200

Rating: observed moderate. Assessed: x,y. Domain: Reals. Functions: x=-t**2 + 5*t, y=t**2.

Given that a curve is defined parametrically as

$$
x=5t-{t}^{2},\,\,\,y={t}^{2},\,t\in (-\infty ,\infty ),
$$

determine the ranges of $x$ and $y.$

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & =5t-{t}^{2} \\  & =-({t}^{2}-5t) \\  & =-{(t-\frac{5}{2})}^{2}+{(\frac{5}{2})}^{2} \\  & =-{(t-\frac{5}{2})}^{2}+\frac{25}{4}\end{aligned}
$$

Since ${(t-\frac{5}{2})}^{2}\ge 0,$ we can conclude that $x\le \frac{25}{4}.$

- To find the range of $y,$ notice that ${t}^{2}\ge 0$ for all $t\in (-\infty ,\infty ).$ Consequently, $y\ge 0.$

Therefore, the ranges are $x\le \frac{25}{4}$ and $y\ge 0.$

Field `selection`, :answer-field.type/radio; observed correct: `x\le \frac{25}{4},\,y\ge 0`.

- `x\ge \frac{5}{2},\,y\le -1` → {'x': 'Interval(5/2, oo)', 'y': 'Interval(-oo, -1)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 0,\,y\ge 0` → {'x': 'Interval(-oo, 0)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 5,\,y\ge 2` → {'x': 'Interval(-oo, 5)', 'y': 'Interval(2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 4,\,y\le -2` → {'x': 'Interval(4, oo)', 'y': 'Interval(-oo, -2)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le \frac{25}{4},\,y\ge 0` → {'x': 'Interval(-oo, 25/4)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-276257

Rating: observed moderate. Assessed: x,y. Domain: Interval(-1, oo). Functions: x=5 - 4*t, y=t + 1.

Given that a curve is defined parametrically as

$$
x=5-4t,\,y=t+1,\,t\ge -1.
$$

Determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $x=5-4t\le 9$ for all $t\ge -1.$ Consequently, the range of $x$ is

$$
x\le 9.
$$

- To find the range of $y,$ note that $y=t+1\ge 0$ for all $t\ge -1.$ Consequently, the range of $y$ is

$$
y\ge 0.
$$

Field `field-4`, :answer-field.type/blank; observed correct: `0`.

- `0` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `9`.

- `9` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\le `.

- `\le ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-326259

Rating: observed moderate. Assessed: x,y. Domain: Interval(-oo, 4). Functions: x=2*t - 7, y=3 - t.

Given that a curve is defined parametrically as

$$
x=2t-7,\,y=3-t,\,t\le 4.
$$

Determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $x=2t-7\le 1$ for all $t\le 4.$ Consequently, the range of $x$ is

$$
x\le 1.
$$

- To find the range of $y,$ note that $y=3-t\ge -1$ for all $t\le 4.$ Consequently, the range of $y$ is

$$
y\ge -1.
$$

Field `field-2`, :answer-field.type/blank; observed correct: `1`.

- `1` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\le `.

- `\le ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `-1`.

- `-1` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-326271

Rating: observed moderate. Assessed: x. Domain: Reals. Functions: x=2*t**2 - 4*t, y=t + 1.

Given that a curve is defined parametrically as

$$
x=2{t}^{2}-4t,\,y=t+1,\,t\in (-\infty ,\infty ).
$$

Determine the range of $x.$

$x$
{{field-1}}{{field-2}}

Full worked solution:

To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & =2{t}^{2}-4t \\  & =2({t}^{2}-2t) \\  & =2({t}^{2}-2t+1)-2 \\  & =2(t-1)^{2}-2\end{aligned}
$$

Since $2(t-1)^{2}\ge 0,$ we can conclude that

$$
x\ge -2.
$$

Field `field-2`, :answer-field.type/blank; observed correct: `-2`.

- `-2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-326300

Rating: observed moderate. Assessed: x,y. Domain: Interval(2, oo). Functions: x=3 - t/2, y=3*t**2/4 - 1.

Given that a curve is defined parametrically as

$$
x=3-\frac{1}{2}t,\,y=\frac{3}{4}{t}^{2}-1,\,t\ge 2.
$$

Determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $3-\frac{1}{2}t\le 2$ for all $t\ge 2.$ Consequently, the range of $x$ is

$$
x\le 2.
$$

- To find the range of $y,$ note that $\frac{3}{4}{t}^{2}-1\ge 2$ for all $t\ge 2.$ Consequently, the range of $y$ is

$$
y\ge 2.
$$

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `2`.

- `2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\le `.

- `\le ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `2`.

- `2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-326304

Rating: observed moderate. Assessed: x,y. Domain: Reals. Functions: x=-t**2 + 4*t, y=t**2 + 3.

Given that a curve is defined parametrically as

$$
x=4t-{t}^{2},\,y={t}^{2}+3,\,t\in (-\infty ,\infty ),
$$

determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & =4t-{t}^{2} \\  & =-({t}^{2}-4t) \\  & =-({t}^{2}-4t+4)+4 \\  & =-(t-2)^{2}+4\end{aligned}
$$

Since $-(t-2)^{2}+4\le 4,$ we conclude that the range of $x$ is

$$
x\le 4.
$$

- To find the range of $y,$ notice that ${t}^{2}+3\ge 3.$ Consequently, the range of $y$ is

$$
y\ge 3.
$$

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\le `.

- `\le ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `3`.

- `3` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `4`.

- `4` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-326305

Rating: observed moderate. Assessed: x,y. Domain: Reals. Functions: x=2*t**2 - 4*t, y=(t - 1)**2 + 2.

Given that a curve is defined parametrically as

$$
x=2{t}^{2}-4t,\,y=(t-1)^{2}+2,\,t\in (-\infty ,\infty ),
$$

determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ we can start by completing the square, as follows:

$$
\begin{aligned}x & =2{t}^{2}-4t \\  & =2({t}^{2}-2t) \\  & =2({t}^{2}-2t+1)-2 \\  & =2(t-1)^{2}-2\end{aligned}
$$

Since $2(t-1)^{2}-2\ge -2,$ we conclude that the range of $x$ is

$$
x\ge -2.
$$

- To find the range of $y,$ notice that $(t-1)^{2}+2\ge 2.$ Consequently, the range of $y$ is

$$
y\ge 2.
$$

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `-2`.

- `-2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `2`.

- `2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-327660

Rating: observed moderate. Assessed: x,y. Domain: Interval(-4, oo). Functions: x=t - 5, y=sqrt(t + 4) + 1.

Given that a curve is defined parametrically as

$$
x=t-5,\,y=\sqrt{\,t+4\,}+1,\,t\ge -4,
$$

determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $t-5\ge -9$ for all $t\ge -4.$ Consequently, the range of $x$ is

$$
x\ge -9.
$$

- To find the range of $y,$ note that $\sqrt{t+4}\ge 0$ for all $t\ge -4.$ Consequently, the range of $y$ is

$$
y\ge 1.
$$

Field `field-4`, :answer-field.type/blank; observed correct: `1`.

- `1` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `-9`.

- `-9` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-327851

Rating: observed moderate. Assessed: x,y. Domain: Interval(0, oo). Functions: x=2*sqrt(t) + 1, y=sqrt(t) + 2.

Given that a curve is defined parametrically as

$$
x=\sqrt{4t}+1,\,y=\sqrt{t}+2,\,t\ge 0,
$$

determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $\sqrt{4t}+1\ge 1$ for all $t\ge 0.$ Consequently, the range of $x$ is

$$
x\ge 1.
$$

- To find the range of $y,$ note that $\sqrt{t}+2\ge 2$ for all $t\ge 0.$ Consequently, the range of $y$ is

$$
y\ge 2.
$$

Field `field-3`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `1`.

- `1` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-1`, :answer-field.type/blank; observed correct: `\ge `.

- `\ge ` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `2`.

- `2` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-327852

Rating: observed moderate. Assessed: x,y. Domain: Interval.open(-oo, 8). Functions: x=sqrt(8 - t), y=sqrt(16 - 2*t) + 1.

Given that a curve is defined parametrically as

$$
x=\sqrt{8-t},\,y=\sqrt{16-2t}+1,\,t<8,
$$

determine the ranges of $x$ and $y.$

$x$
{{field-1}}{{field-2}}$,\,y$
{{field-3}}{{field-4}}

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $\sqrt{8-t}>0$ for all $t<8.$ Consequently, the range of $x$ is

$$
x>0.
$$

- To find the range of $y,$ note that $\sqrt{16-2t}+1>1$ for all $t<8.$ Consequently, the range of $y$ is

$$
y>1.
$$

Field `field-1`, :answer-field.type/blank; observed correct: `>`.

- `>` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-4`, :answer-field.type/blank; observed correct: `1`.

- `1` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-2`, :answer-field.type/blank; observed correct: `0`.

- `0` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

Field `field-3`, :answer-field.type/blank; observed correct: `>`.

- `>` → None; Coordinate boundary value times its positive coordinate scale, or unchanged exact inequality-sign fragment.

### q-73623

Rating: observed moderate. Assessed: x,y. Domain: Interval(2, oo). Functions: x=sqrt(t - 2) + 1, y=t**3 + 2.

Given that a curve is defined parametrically as

$$
x=\sqrt{t-2}+1,\,\,\,y={t}^{3}+2,\,t\ge 2,
$$

what are the ranges of $x$ and $y?$

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $\sqrt{t-2}\ge 0$ for all $t\ge 2.$ Consequently, $x=\sqrt{t-2}+1\ge 1.$

- To find the range of $y,$ note that ${t}^{3}\ge 8$ for all $t\ge 2.$ Consequently, $y={t}^{3}+2\ge 8+2=10.$

Therefore, the ranges are $x\ge 1$ and $y\ge 10.$

Field `selection`, :answer-field.type/radio; observed correct: `x\ge 1,\,y\ge 10`.

- `x\ge 1,\,y\ge 10` → {'x': 'Interval(1, oo)', 'y': 'Interval(10, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 1,\,y\le 10` → {'x': 'Interval(-oo, 1)', 'y': 'Interval(-oo, 10)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -1,\,y\ge -2` → {'x': 'Interval(-1, oo)', 'y': 'Interval(-2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 1,\,y\le 10` → {'x': 'Interval(1, oo)', 'y': 'Interval(-oo, 10)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le -1,\,y\ge -2` → {'x': 'Interval(-oo, -1)', 'y': 'Interval(-2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-123769

Rating: observed moderate. Assessed: x,y. Domain: Interval(1, oo). Functions: x=3 - t, y=t + 2.

Given that a curve is defined parametrically as

$$
x=3-t,\,\,\,y=t+2,\,t\ge 1,
$$

determine the ranges of $x$ and $y.$

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $3-t\le 2$ for all $t\ge 1.$ Consequently, $x=3-t\le 2.$

- To find the range of $y,$ note that $t+2\ge 3$ for all $t\ge 1.$ Consequently, $y=t+2\ge 3.$

Therefore, the ranges are $x\le 2$ and $y\ge 3.$

Field `selection`, :answer-field.type/radio; observed correct: `x\le 2,\,y\ge 3`.

- `x\le -3,\,y\ge 2` → {'x': 'Interval(-oo, -3)', 'y': 'Interval(2, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 2,\,y\ge -3` → {'x': 'Interval(-oo, 2)', 'y': 'Interval(-3, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 2,\,y\ge 3` → {'x': 'Interval(-oo, 2)', 'y': 'Interval(3, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge -1,\,y\ge 3` → {'x': 'Interval(-1, oo)', 'y': 'Interval(3, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 3,\,y\le -2` → {'x': 'Interval(3, oo)', 'y': 'Interval(-oo, -2)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

### q-73617

Rating: observed moderate. Assessed: x,y. Domain: Interval(-1, oo). Functions: x=1 - t, y=t**2 - 4.

Given that a curve is defined parametrically as

$$
x=1-t,\,\,\,y={t}^{2}-4,\,t\ge -1,
$$

determine the ranges of $x$ and $y.$

Full worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ note that $1-t\le 2$ for all $t\ge -1.$ Consequently, $x=1-t\le 2.$

- To find the range of $y,$ note that ${t}^{2}\ge 0$ for all $t.$ Consequently, $y={t}^{2}-4\ge -4.$

Therefore, the ranges are $x\le 2$ and $y\ge -4.$

Field `selection`, :answer-field.type/radio; observed correct: `x\le 2,\,y\ge -4`.

- `x\ge -1,\,y\ge 0` → {'x': 'Interval(-1, oo)', 'y': 'Interval(0, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 0,\,y\le -4` → {'x': 'Interval(0, oo)', 'y': 'Interval(-oo, -4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\ge 1,\,y\le -4` → {'x': 'Interval(1, oo)', 'y': 'Interval(-oo, -4)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 4,\,y\ge 1` → {'x': 'Interval(-oo, 4)', 'y': 'Interval(1, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

- `x\le 2,\,y\ge -4` → {'x': 'Interval(-oo, 2)', 'y': 'Interval(-4, oo)'}; Coordinate dilation: each complete interval endpoint multiplied by s_v>0; openness and inequality direction retained. Original scalar bounds remain opaque observed profile constants; no inferred error intent.

## Stage 2: shared pattern

Read each coordinate function on the admissible parameter domain. Evaluate a monotone endpoint or complete the square and check whether its vertex parameter is admissible. Preserve nonnegative square/root facts and distinguish excluded endpoints from attained extrema. Respond with the complete inequality constraints or the original split sign/value fragments. The coordinate images are assessed independently; neither their product nor the answer is a Cartesian equation of the curve.

## Stage 3: component mapping

extraction.json maps every question, field, complete choice, original correct designation, raw expression/domain, raw prose, and transport recipe. There are 13 observed complete radio profiles and nine blank layouts. No bank merging or option pooling is used. Opaque scalar bounds are transported by a positive coordinate dilation as full sets, which faithfully retains an observed expression shape but does not infer the original author error code. Unit-scale replay computes correct sets from the printed prompt and compares every option and observed designation, rather than selecting a known correct option by lookup.

## Stage 4: reusable templates and constraints

Each source recipe masks complete x(t) and y(t) components. At scale 1 the component slot renders its exact source notation. At a positive integer scale, the entire displayed coordinate function receives that scale. Completing-square equations retain the same row sequence. Each nonfinal original arithmetic RHS remains verbatim inside a positive-scale wrapper, preserving unevaluated terms such as −1²−1. Only the final completed-square row distributes that scale, retaining the square and evaluating its constant. Compound coordinate equation/inequality chains likewise retain intermediate sums and evaluate their final endpoint. Every complete coordinate inequality is transported and final numeric endpoints evaluated. Auxiliary square/root/domain facts can remain unscaled. Labels, shared prose, number of math slots, and aligned row counts are preserved. Missing-source solutions are independently authored using the actual displayed scaled functions. Prompts retain the original field layout and answer fragments. Explicit replay uses the normal source recipe/profile, never a returned source-question payload or answer designation lookup.

The positive scale constraint is necessary: negative scale would reverse directions and change profile conditions, and zero would collapse banks. s_x,s_y are independently bounded integers 1..6. Correct images are recomputed from the actual rendered coordinate functions and domain, including admissibility restrictions from both coordinates. The generator rejects the entire five-option bank on duplicate or ambiguous complete sets.

Normal radio output selects the separately labeled authored-endpoint-bank as a complete profile. For a single coordinate, its five operations are: correct set; reverse its direction at the same endpoint; toggle its inclusion; retain only the endpoint as a singleton (endpoint-only domain mistake); or omit its constraint (all real values). For paired coordinates, the five operations are: correct pair; reverse x only; reverse y only; toggle both endpoint inclusions; or retain both endpoints only. The x-only and y-only errors force both coordinate ranges to be assessed. These are documented authored endpoint/domain operations, not recovered source intentions. All five must remain mathematically distinct; no arbitrary scalar perturbations or partial bank replacements are allowed.

Easy and hard templates and explicit bounds are in classification.md. They share this coordinate range method and field shape. No profile asserts an observed missing-level rating.

## Plot extraction / specification (steps 5 and 7)

No mathematical plot occurs in any practice source prompt, option, or worked solution. No parameter-dependent graphics are required. Plot rating none; no renderer and no graphic assets. Lesson introduction and sibling graphing plots are context only.