# Original and generated review

Status: working. Originals are immutable basis2275 evidence. Served records below are computed parameterized replays or clearly marked coefficient extensions. Raw omissions and prose are shown separately from served repairs.

No plots are present. Inspect each fixed third/fourth-order target, complete input and every formal-operator stage.

## q-28546 — captured original

Given $h(x)=3{x}^{2}-5x+\frac{3}{x},$ find ${h}^{‴}(x).$

Original field: :answer-field.type/radio

- $-\frac{6}{{x}^{3}}$

- $-\frac{18}{{x}^{4}}$ **original correct**

- $\frac{6}{{x}^{3}}$

- $-\frac{6}{{x}^{4}}+6$

- $\frac{18}{{x}^{4}}$

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}h(x) & =3{x}^{2}-5x+\frac{3}{x} \\  & =3{x}^{2}-5x+3{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{2}-5x+3{x}^{-1}) \\  & =6x-5-3{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{h}^{″}(x) & =\frac{\text{d}}{\text{d}x}(6x-5-3{x}^{-2}) \\  & =6+6{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{h}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6+6{x}^{-3}) \\  & =-18{x}^{-4} \\  & =-\frac{18}{{x}^{4}}.\end{aligned}
$$

### served original parameters

Template polynomial_reciprocal_radio; profile observed-q-28546; scales [1, 1, 1]; difficulty :question.difficulty/moderate.

Given $h(x)=3{x}^{2}-5x+\frac{3}{x},$ find ${h}^{‴}(x).$

- $\frac{18}{{x}^{4}}$

- $\frac{6}{{x}^{3}}$

- $-\frac{18}{{x}^{4}}$ **computed correct**

- $-\frac{6}{{x}^{3}}$

- $-\frac{6}{{x}^{4}}+6$

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}h(x) & =3{x}^{2}-5x+\frac{3}{x} \\  & =3{x}^{2}-5x+3{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{x}^{2}-5x+3{x}^{-1}) \\  & =6x-5-3{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{h}^{″}(x) & =\frac{\text{d}}{\text{d}x}(6x-5-3{x}^{-2}) \\  & =6+6{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{h}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6+6{x}^{-3}) \\  & =-18{x}^{-4} \\  & =-\frac{18}{{x}^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial_reciprocal_radio; profile authored-errors; scales [1, 1, -6]; difficulty :question.difficulty/moderate.

Given $h(x)=3 x^{2} - 5 x - \frac{18}{x},$ find ${h}^{‴}(x).$

- $6 (1 - \frac{6}{x^{3}}) + \frac{36}{x^{3}}$

- $6 x - 5 + \frac{18}{x^{2}}$

- $6 (1 - \frac{6}{x^{3}})$

- $\frac{108}{x^{4}}$ **computed correct**

- $- \frac{108}{x^{4}}$

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}h(x) & =3 x^{2} - 5 x - \frac{18}{x} \\  & =-18{x}^{-1}-5x+3{x}^{2}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-18{x}^{-1}-5x+3{x}^{2}) \\  & =-5+6x+18{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{h}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-5+6x+18{x}^{-2}) \\  & =6-36{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{h}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6-36{x}^{-3}) \\  & =108{x}^{-4} \\  & =\frac{108}{x^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial_reciprocal_radio; profile authored-errors; scales [1, 1, -5]; difficulty :question.difficulty/moderate.

Given $h(x)=3 x^{2} - 5 x - \frac{15}{x},$ find ${h}^{‴}(x).$

- $6 x - 5 + \frac{15}{x^{2}}$

- $- \frac{90}{x^{4}}$

- $6 (1 - \frac{5}{x^{3}})$

- $\frac{90}{x^{4}}$ **computed correct**

- $6 (1 - \frac{5}{x^{3}}) + \frac{30}{x^{3}}$

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}h(x) & =3 x^{2} - 5 x - \frac{15}{x} \\  & =-15{x}^{-1}-5x+3{x}^{2}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}(-15{x}^{-1}-5x+3{x}^{2}) \\  & =-5+6x+15{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{h}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-5+6x+15{x}^{-2}) \\  & =6-30{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{h}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6-30{x}^{-3}) \\  & =90{x}^{-4} \\  & =\frac{90}{x^{4}}.\end{aligned}
$$

## q-28550 — captured original

Given $y = \frac{x^{3}}{4} - \frac{4}{x^{2}}$, find $\frac{d^{3}y}{dx^{3}}$.

Original field: :answer-field.type/radio

- $\frac{3}{2} + \frac{24}{x^{4}}$

- $\frac{3x}{2} - \frac{24}{x^{4}}$

- $\frac{3x}{2} + \frac{24}{x^{5}}$

- $\frac{3}{2} - \frac{96}{x^{5}}$

- $\frac{3}{2} + \frac{96}{x^{5}}$

Original correct designation absent.

Original worked solution absent.

### served original parameters

Template cubic_reciprocal_radio; profile observed-q-28550; scales [1, 1]; difficulty :question.difficulty/moderate.

Given $y = \frac{x^{3}}{4} - \frac{4}{x^{2}}$, find $\frac{d^{3}y}{dx^{3}}$.

- $\frac{3}{2} + \frac{96}{x^{5}}$ **computed correct**

- $\frac{3x}{2} + \frac{24}{x^{5}}$

- $\frac{3x}{2} - \frac{24}{x^{4}}$

- $\frac{3}{2} + \frac{24}{x^{4}}$

- $\frac{3}{2} - \frac{96}{x^{5}}$

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{x^{3}}{4} - \frac{4}{x^{2}}) \\ & =\frac{3 x^{2}}{4} + \frac{8}{x^{3}}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{\text{d}^{2}y}{\text{d}x^{2}} & =\frac{\text{d}}{\text{d}x}(\frac{3 x^{2}}{4} + \frac{8}{x^{3}}) \\ & =3 (\frac{x}{2} - \frac{8}{x^{4}}).\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{\text{d}^{3}y}{\text{d}x^{3}} & =\frac{\text{d}}{\text{d}x}(3 (\frac{x}{2} - \frac{8}{x^{4}})) \\ & =3 (\frac{1}{2} + \frac{32}{x^{5}}).\end{aligned}
$$

### generated signed coefficient variant

Template cubic_reciprocal_radio; profile authored-errors; scales [-6, -6]; difficulty :question.difficulty/moderate.

Given $y =- \frac{3 x^{3}}{2} + \frac{24}{x^{2}}$, find $\frac{d^{3}y}{dx^{3}}$.

- $- \frac{576}{x^{5}}$

- $- \frac{9 x^{2}}{2} - \frac{48}{x^{3}}$

- $9 (- x + \frac{16}{x^{4}})$

- $- 9 (1 + \frac{64}{x^{5}})$ **computed correct**

- $9 (1 + \frac{64}{x^{5}})$

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(- \frac{3 x^{3}}{2} + \frac{24}{x^{2}}) \\ & =- \frac{9 x^{2}}{2} - \frac{48}{x^{3}}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{\text{d}^{2}y}{\text{d}x^{2}} & =\frac{\text{d}}{\text{d}x}(- \frac{9 x^{2}}{2} - \frac{48}{x^{3}}) \\ & =- 9 x + \frac{144}{x^{4}}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{\text{d}^{3}y}{\text{d}x^{3}} & =\frac{\text{d}}{\text{d}x}(- 9 x + \frac{144}{x^{4}}) \\ & =-9 - \frac{576}{x^{5}}.\end{aligned}
$$

### generated signed coefficient variant

Template cubic_reciprocal_radio; profile authored-errors; scales [-6, -5]; difficulty :question.difficulty/moderate.

Given $y =- \frac{3 x^{3}}{2} + \frac{20}{x^{2}}$, find $\frac{d^{3}y}{dx^{3}}$.

- $- \frac{9 x^{2}}{2} - \frac{40}{x^{3}}$

- $3 (3 + \frac{160}{x^{5}})$

- $3 (- 3 x + \frac{40}{x^{4}})$

- $- 3 (3 + \frac{160}{x^{5}})$ **computed correct**

- $- \frac{480}{x^{5}}$

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(- \frac{3 x^{3}}{2} + \frac{20}{x^{2}}) \\ & =- \frac{9 x^{2}}{2} - \frac{40}{x^{3}}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{\text{d}^{2}y}{\text{d}x^{2}} & =\frac{\text{d}}{\text{d}x}(- \frac{9 x^{2}}{2} - \frac{40}{x^{3}}) \\ & =- 9 x + \frac{120}{x^{4}}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{\text{d}^{3}y}{\text{d}x^{3}} & =\frac{\text{d}}{\text{d}x}(- 9 x + \frac{120}{x^{4}}) \\ & =-9 - \frac{480}{x^{5}}.\end{aligned}
$$

## q-28551 — captured original

Given $y=7{x}^{2}-1+\frac{1}{2x}$, find $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}.$

Original answer fields absent.

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}h(x) & =7{x}^{2}-1+\frac{1}{2x} \\  & =7{x}^{2}-1+\frac{{x}^{-1}}{2}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(7{x}^{2}-1+\frac{{x}^{-1}}{2}) \\  & =7(2)x-0+\frac{(-1){x}^{-2}}{2} \\  & =14x-\frac{{x}^{-2}}{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(14x-\frac{{x}^{-2}}{2}) \\  & =14-\frac{(-2){x}^{-3}}{2} \\  & =14+{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}} & =\frac{\text{d}}{\text{d}x}(14+{x}^{-3}) \\  & =0+(-3){x}^{-4} \\  & =-\frac{3}{{x}^{4}}.\end{aligned}
$$

### served original parameters

Template quadratic_constant_reciprocal; profile blank; scales [1, 1, 1]; difficulty :question.difficulty/moderate.

Given $y=7{x}^{2}-1+\frac{1}{2x}$, find $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}.$

$\frac{\text{d}^{3}y}{\text{d}x^{3}}=$
{{field-1}}

- $- \frac{3}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}y & =7{x}^{2}-1+\frac{1}{2x} \\  & =7{x}^{2}-1+\frac{{x}^{-1}}{2}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(7{x}^{2}-1+\frac{{x}^{-1}}{2}) \\  & =7(2)x-0+\frac{(-1){x}^{-2}}{2} \\  & =14x-\frac{{x}^{-2}}{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(14x-\frac{{x}^{-2}}{2}) \\  & =14-\frac{(-2){x}^{-3}}{2} \\  & =14+{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}} & =\frac{\text{d}}{\text{d}x}(14+{x}^{-3}) \\  & =0+(-3){x}^{-4} \\  & =-\frac{3}{{x}^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template quadratic_constant_reciprocal; profile blank; scales [1, 1, -6]; difficulty :question.difficulty/moderate.

Given $y=7 x^{2} - 1 - \frac{3}{x}$, find $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}.$

$\frac{\text{d}^{3}y}{\text{d}x^{3}}=$
{{field-1}}

- $\frac{18}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}y & =7 x^{2} - 1 - \frac{3}{x} \\  & =-1-3{x}^{-1}+7{x}^{2}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-1-3{x}^{-1}+7{x}^{2}) \\  & =7\cdot 2x+0+3{x}^{-2} \\  & =3{x}^{-2}+14x.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(3{x}^{-2}+14x) \\  & =14-6{x}^{-3} \\  & =14-6{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}} & =\frac{\text{d}}{\text{d}x}(14-6{x}^{-3}) \\  & =0+(18){x}^{-4} \\  & =\frac{18}{x^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template quadratic_constant_reciprocal; profile blank; scales [1, 1, -5]; difficulty :question.difficulty/moderate.

Given $y=7 x^{2} - 1 - \frac{5}{2 x}$, find $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}.$

$\frac{\text{d}^{3}y}{\text{d}x^{3}}=$
{{field-1}}

- $\frac{15}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}y & =7 x^{2} - 1 - \frac{5}{2 x} \\  & =-1+7{x}^{2}-\frac{5}{2}{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-1+7{x}^{2}-\frac{5}{2}{x}^{-1}) \\  & =7\cdot 2x+0+\frac{5}{2}{x}^{-2} \\  & =14x+\frac{5}{2}{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(14x+\frac{5}{2}{x}^{-2}) \\  & =14-5{x}^{-3} \\  & =14-5{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}} & =\frac{\text{d}}{\text{d}x}(14-5{x}^{-3}) \\  & =0+(15){x}^{-4} \\  & =\frac{15}{x^{4}}.\end{aligned}
$$

## q-310170 — captured original

Given $g(x)=4{x}^{2}+6x-\frac{2}{x},$ we have

${g}^{‴}(x)=$
{{field-1}}

Original field: :answer-field.type/blank

- $\frac{12}{{x}^{4}}$ **original correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}g(x) & =4{x}^{2}+6x-\frac{2}{x} \\  & =4{x}^{2}+6x-2{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{g}^{'}(x) & =\frac{\text{d}}{\text{d}x}(4{x}^{2}+6x-2{x}^{-1}) \\  & =8x+6+2{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{''}(x) & =\frac{\text{d}}{\text{d}x}(8x+6+2{x}^{-2}) \\  & =8-4{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(8-4{x}^{-3}) \\  & =12{x}^{-4} \\  & =\frac{12}{{x}^{4}}.\end{aligned}
$$

### served original parameters

Template polynomial_reciprocal_blank; profile blank; scales [1, 1, 1]; difficulty :question.difficulty/moderate.

Given $g(x)=4{x}^{2}+6x-\frac{2}{x},$ we have

${g}^{‴}(x)=$
{{field-1}}

- $\frac{12}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}g(x) & =4{x}^{2}+6x-\frac{2}{x} \\  & =4{x}^{2}+6x-2{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{g}^{'}(x) & =\frac{\text{d}}{\text{d}x}(4{x}^{2}+6x-2{x}^{-1}) \\  & =8x+6+2{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{''}(x) & =\frac{\text{d}}{\text{d}x}(8x+6+2{x}^{-2}) \\  & =8-4{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(8-4{x}^{-3}) \\  & =12{x}^{-4} \\  & =\frac{12}{{x}^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial_reciprocal_blank; profile blank; scales [1, 1, -6]; difficulty :question.difficulty/moderate.

Given $g(x)=4 x^{2} + 6 x + \frac{12}{x},$ we have

${g}^{‴}(x)=$
{{field-1}}

- $- \frac{72}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}g(x) & =4 x^{2} + 6 x + \frac{12}{x} \\  & =4{x}^{2}+6x+12{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{g}^{'}(x) & =\frac{\text{d}}{\text{d}x}(4{x}^{2}+6x+12{x}^{-1}) \\  & =6-12{x}^{-2}+8x.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{''}(x) & =\frac{\text{d}}{\text{d}x}(6-12{x}^{-2}+8x) \\  & =8+24{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(8+24{x}^{-3}) \\  & =-72{x}^{-4} \\  & =- \frac{72}{x^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial_reciprocal_blank; profile blank; scales [1, 1, -5]; difficulty :question.difficulty/moderate.

Given $g(x)=4 x^{2} + 6 x + \frac{10}{x},$ we have

${g}^{‴}(x)=$
{{field-1}}

- $- \frac{60}{x^{4}}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}g(x) & =4 x^{2} + 6 x + \frac{10}{x} \\  & =4{x}^{2}+6x+10{x}^{-1}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{g}^{'}(x) & =\frac{\text{d}}{\text{d}x}(4{x}^{2}+6x+10{x}^{-1}) \\  & =6-10{x}^{-2}+8x.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{''}(x) & =\frac{\text{d}}{\text{d}x}(6-10{x}^{-2}+8x) \\  & =8+20{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(8+20{x}^{-3}) \\  & =-60{x}^{-4} \\  & =- \frac{60}{x^{4}}.\end{aligned}
$$

## q-104294 — captured original

Given $f(x)=2\operatorname{ln}⁡x-8\sqrt{{x}^{5}},$ find ${f}^{‴}(x).$

Original field: :answer-field.type/radio

- $-\frac{6}{{x}^{3}}-60x$

- $\frac{4}{{x}^{2}}-60x$

- $-\frac{6}{{x}^{3}}+\frac{15}{\sqrt{x}}$

- $\frac{1}{{x}^{2}}-\frac{1}{\sqrt{x}}$

- $\frac{4}{{x}^{3}}-\frac{15}{\sqrt{x}}$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}⁡x-8\sqrt{{x}^{5}}) \\  & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}⁡x-8{x}^{5/2}) \\  & =\frac{2}{x}-20{x}^{3/2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(\frac{2}{x}-20{x}^{3/2}) \\  & =\frac{\text{d}}{\text{d}x}(2{x}^{-1}-20{x}^{3/2}) \\  & =-2{x}^{-2}-30{x}^{1/2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-2{x}^{-2}-30{x}^{1/2}) \\  & =4{x}^{-3}-15{x}^{-1/2} \\  & =\frac{4}{{x}^{3}}-\frac{15}{\sqrt{x}}.\end{aligned}
$$

### served original parameters

Template log_radical; profile observed-q-104294; scales [1, 1]; difficulty :question.difficulty/easy.

Given $f(x)=2\operatorname{ln}x-8\sqrt{{x}^{5}},$ find ${f}^{‴}(x).$

- $\frac{4}{{x}^{3}}-\frac{15}{\sqrt{x}}$ **computed correct**

- $-\frac{6}{{x}^{3}}+\frac{15}{\sqrt{x}}$

- $\frac{4}{{x}^{2}}-60x$

- $-\frac{6}{{x}^{3}}-60x$

- $\frac{1}{{x}^{2}}-\frac{1}{\sqrt{x}}$

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}x-8\sqrt{{x}^{5}}) \\  & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}x-8{x}^{5/2}) \\  & =\frac{2}{x}-20{x}^{3/2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(\frac{2}{x}-20{x}^{3/2}) \\  & =\frac{\text{d}}{\text{d}x}(2{x}^{-1}-20{x}^{3/2}) \\  & =-2{x}^{-2}-30{x}^{1/2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-2{x}^{-2}-30{x}^{1/2}) \\  & =4{x}^{-3}-15{x}^{-1/2} \\  & =\frac{4}{{x}^{3}}-\frac{15}{\sqrt{x}}.\end{aligned}
$$

### generated signed coefficient variant

Template log_radical; profile authored-errors; scales [-6, -6]; difficulty :question.difficulty/easy.

Given $f(x)=- 12 \ln{(x )}+48\sqrt{{x}^{5}},$ find ${f}^{‴}(x).$

- $\frac{90}{\sqrt{x}}$

- $120 x^{\frac{3}{2}} - \frac{12}{x}$

- $12 (15 \sqrt{x} + \frac{1}{x^{2}})$

- $6 (- \frac{4}{x^{3}} + \frac{15}{\sqrt{x}})$ **computed correct**

- $- 6 (- \frac{4}{x^{3}} + \frac{15}{\sqrt{x}})$

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 12 \ln{(x )}+48\sqrt{{x}^{5}}) \\  & =\frac{\text{d}}{\text{d}x}(48 x^{\frac{5}{2}} - 12 \ln{(x )}) \\  & =120 x^{\frac{3}{2}} - \frac{12}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(120 x^{\frac{3}{2}} - \frac{12}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-12{x}^{-1}+120{x}^{\frac{3}{2}}) \\  & =12{x}^{-2}+180{x}^{\frac{1}{2}}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(12{x}^{-2}+180{x}^{\frac{1}{2}}) \\  & =-24{x}^{-3}+90{x}^{- \frac{1}{2}} \\  & =- \frac{24}{x^{3}} + \frac{90}{\sqrt{x}}.\end{aligned}
$$

### generated signed coefficient variant

Template log_radical; profile authored-errors; scales [-6, -5]; difficulty :question.difficulty/easy.

Given $f(x)=- 12 \ln{(x )}+40\sqrt{{x}^{5}},$ find ${f}^{‴}(x).$

- $100 x^{\frac{3}{2}} - \frac{12}{x}$

- $- 3 (- \frac{8}{x^{3}} + \frac{25}{\sqrt{x}})$

- $6 (25 \sqrt{x} + \frac{2}{x^{2}})$

- $3 (- \frac{8}{x^{3}} + \frac{25}{\sqrt{x}})$ **computed correct**

- $\frac{75}{\sqrt{x}}$

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 12 \ln{(x )}+40\sqrt{{x}^{5}}) \\  & =\frac{\text{d}}{\text{d}x}(40 x^{\frac{5}{2}} - 12 \ln{(x )}) \\  & =100 x^{\frac{3}{2}} - \frac{12}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(100 x^{\frac{3}{2}} - \frac{12}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-12{x}^{-1}+100{x}^{\frac{3}{2}}) \\  & =12{x}^{-2}+150{x}^{\frac{1}{2}}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(12{x}^{-2}+150{x}^{\frac{1}{2}}) \\  & =-24{x}^{-3}+75{x}^{- \frac{1}{2}} \\  & =- \frac{24}{x^{3}} + \frac{75}{\sqrt{x}}.\end{aligned}
$$

## q-310171 — captured original

Find ${g}^{(4)}(x)$ for $g(x)=\operatorname{cos}⁡x+\operatorname{ln}⁡x.$

${g}^{(4)}(x)=$ 
{{field-1}}

Original field: :answer-field.type/blank

- $\operatorname{cos}x-\frac{6}{{x}^{4}}$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(\operatorname{cos}⁡x+\operatorname{ln}⁡x) \\  & =-\operatorname{sin}⁡x+\frac{1}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-\operatorname{sin}⁡x+\frac{1}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-\operatorname{sin}⁡x+{x}^{-1}) \\  & =-\operatorname{cos}⁡x-{x}^{-2}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-\operatorname{cos}⁡x-{x}^{-2}) \\  & =\operatorname{sin}⁡x+2{x}^{-3}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(\operatorname{sin}⁡x+2{x}^{-3}) \\  & =\operatorname{cos}⁡x-6{x}^{-4} \\  & =\operatorname{cos}⁡x-\frac{6}{{x}^{4}}.\end{aligned}
$$

### served original parameters

Template cos_log; profile blank; scales [1, 1]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=\operatorname{cos}x+\operatorname{ln}x.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $\cos{(x )} - \frac{6}{x^{4}}$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(\operatorname{cos}x+\operatorname{ln}x) \\  & =-\operatorname{sin}x+\frac{1}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-\operatorname{sin}x+\frac{1}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-\operatorname{sin}x+{x}^{-1}) \\  & =-\operatorname{cos}x-{x}^{-2}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-\operatorname{cos}x-{x}^{-2}) \\  & =\operatorname{sin}x+2{x}^{-3}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(\operatorname{sin}x+2{x}^{-3}) \\  & =\operatorname{cos}x-6{x}^{-4} \\  & =\operatorname{cos}x-\frac{6}{{x}^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template cos_log; profile blank; scales [-6, -6]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=- 6 \ln{(x )} - 6 \cos{(x )}.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $6 (- \cos{(x )} + \frac{6}{x^{4}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 6 \ln{(x )} - 6 \cos{(x )}) \\  & =6 \sin{(x )} - \frac{6}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(6 \sin{(x )} - \frac{6}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-6{x}^{-1}+6 \sin{(x )}) \\  & =6{x}^{-2}+6 \cos{(x )}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6{x}^{-2}+6 \cos{(x )}) \\  & =-12{x}^{-3}-6 \sin{(x )}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(-12{x}^{-3}-6 \sin{(x )}) \\  & =-6 \cos{(x )}+36{x}^{-4} \\  & =- 6 \cos{(x )} + \frac{36}{x^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template cos_log; profile blank; scales [-6, -5]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=- 5 \ln{(x )} - 6 \cos{(x )}.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $6 (- \cos{(x )} + \frac{5}{x^{4}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 5 \ln{(x )} - 6 \cos{(x )}) \\  & =6 \sin{(x )} - \frac{5}{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(6 \sin{(x )} - \frac{5}{x}) \\  & =\frac{\text{d}}{\text{d}x}(-5{x}^{-1}+6 \sin{(x )}) \\  & =5{x}^{-2}+6 \cos{(x )}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(5{x}^{-2}+6 \cos{(x )}) \\  & =-10{x}^{-3}-6 \sin{(x )}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(-10{x}^{-3}-6 \sin{(x )}) \\  & =-6 \cos{(x )}+30{x}^{-4} \\  & =- 6 \cos{(x )} + \frac{30}{x^{4}}.\end{aligned}
$$

## q-343075 — captured original

Given $g(x)=2{x}^{5}-3{x}^{3},$ we have

${g}^{‴}(x)=$ 
{{field-1}}.

Original field: :answer-field.type/blank

- $120{x}^{2}-18$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{x}^{5}-3{x}^{3}) \\  & =10{x}^{4}-9{x}^{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(10{x}^{4}-9{x}^{2}) \\  & =40{x}^{3}-18x.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(40{x}^{3}-18x) \\  & =120{x}^{2}-18.\end{aligned}
$$

### served original parameters

Template polynomial; profile blank; scales [1, 1]; difficulty :question.difficulty/easy.

Given $g(x)=2{x}^{5}-3{x}^{3},$ we have

${g}^{‴}(x)=$ 
{{field-1}}.

- $6 (20 x^{2} - 3)$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2{x}^{5}-3{x}^{3}) \\  & =10{x}^{4}-9{x}^{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(10{x}^{4}-9{x}^{2}) \\  & =40{x}^{3}-18x.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(40{x}^{3}-18x) \\  & =120{x}^{2}-18.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial; profile blank; scales [-6, -6]; difficulty :question.difficulty/easy.

Given $g(x)=- 12 x^{5} + 18 x^{3},$ we have

${g}^{‴}(x)=$ 
{{field-1}}.

- $36 (- 20 x^{2} + 3)$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 12 x^{5} + 18 x^{3}) \\  & =- 60 x^{4} + 54 x^{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(- 60 x^{4} + 54 x^{2}) \\  & =- 240 x^{3} + 108 x.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(- 240 x^{3} + 108 x) \\  & =- 720 x^{2} + 108.\end{aligned}
$$

### generated signed coefficient variant

Template polynomial; profile blank; scales [-6, -5]; difficulty :question.difficulty/easy.

Given $g(x)=- 12 x^{5} + 15 x^{3},$ we have

${g}^{‴}(x)=$ 
{{field-1}}.

- $90 (- 8 x^{2} + 1)$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 12 x^{5} + 15 x^{3}) \\  & =- 60 x^{4} + 45 x^{2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(- 60 x^{4} + 45 x^{2}) \\  & =- 240 x^{3} + 90 x.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(- 240 x^{3} + 90 x) \\  & =- 720 x^{2} + 90.\end{aligned}
$$

## q-343086 — captured original

Given $f(x)=\frac{{x}^{5}-{x}^{2}+x}{4{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

Original field: :answer-field.type/blank

- $\frac{3}{2}-\frac{3}{2{x}^{4}}$ **original correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}f(x) & =\frac{{x}^{5}-{x}^{2}+x}{4{x}^{2}} \\  & =\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4x}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4x}) \\  & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4}{x}^{-1}) \\  & =\frac{3{x}^{2}}{4}-\frac{1}{4}{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(\frac{3{x}^{2}}{4}-\frac{1}{4}{x}^{-2}) \\  & =\frac{3x}{2}+\frac{1}{2}{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(\frac{3x}{2}+\frac{1}{2}{x}^{-3}) \\  & =\frac{3}{2}-\frac{3}{2}{x}^{-4} \\  & =\frac{3}{2}-\frac{3}{2{x}^{4}}.\end{aligned}
$$

### served original parameters

Template quotient_sum; profile blank; scales [1, 1, 1]; difficulty :question.difficulty/moderate.

Given $f(x)=\frac{{x}^{5}-{x}^{2}+x}{4{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $\frac{3 (1 - \frac{1}{x^{4}})}{2}$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}f(x) & =\frac{{x}^{5}-{x}^{2}+x}{4{x}^{2}} \\  & =\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4x}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4x}) \\  & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{3}}{4}-\frac{1}{4}+\frac{1}{4}{x}^{-1}) \\  & =\frac{3{x}^{2}}{4}-\frac{1}{4}{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(\frac{3{x}^{2}}{4}-\frac{1}{4}{x}^{-2}) \\  & =\frac{3x}{2}+\frac{1}{2}{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(\frac{3x}{2}+\frac{1}{2}{x}^{-3}) \\  & =\frac{3}{2}-\frac{3}{2}{x}^{-4} \\  & =\frac{3}{2}-\frac{3}{2{x}^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template quotient_sum; profile blank; scales [-6, 1, -6]; difficulty :question.difficulty/moderate.

Given $f(x)=\frac{- 6 x^{5} - x^{2} - 6 x}{4{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $9 (-1 + \frac{1}{x^{4}})$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}f(x) & =\frac{- 6 x^{5} - x^{2} - 6 x}{4{x}^{2}} \\  & =- \frac{3 x^{3}}{2} - \frac{1}{4} - \frac{3}{2 x}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- \frac{3 x^{3}}{2} - \frac{1}{4} - \frac{3}{2 x}) \\  & =\frac{\text{d}}{\text{d}x}(-\frac{1}{4}-\frac{3}{2}{x}^{-1}-\frac{3}{2}{x}^{3}) \\  & =-\frac{9}{2}{x}^{2}+\frac{3}{2}{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-\frac{9}{2}{x}^{2}+\frac{3}{2}{x}^{-2}) \\  & =-9x-3{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-9x-3{x}^{-3}) \\  & =-9+9{x}^{-4} \\  & =-9 + \frac{9}{x^{4}}.\end{aligned}
$$

### generated signed coefficient variant

Template quotient_sum; profile blank; scales [-6, 1, -5]; difficulty :question.difficulty/moderate.

Given $f(x)=\frac{- 6 x^{5} - x^{2} - 5 x}{4{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $3 (-3 + \frac{5}{2 x^{4}})$ **computed correct**

First, notice that we can rewrite the function as follows:

$$
\begin{aligned}f(x) & =\frac{- 6 x^{5} - x^{2} - 5 x}{4{x}^{2}} \\  & =- \frac{3 x^{3}}{2} - \frac{1}{4} - \frac{5}{4 x}\end{aligned}
$$

Now, computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- \frac{3 x^{3}}{2} - \frac{1}{4} - \frac{5}{4 x}) \\  & =\frac{\text{d}}{\text{d}x}(-\frac{1}{4}-\frac{5}{4}{x}^{-1}-\frac{3}{2}{x}^{3}) \\  & =-\frac{9}{2}{x}^{2}+\frac{5}{4}{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-\frac{9}{2}{x}^{2}+\frac{5}{4}{x}^{-2}) \\  & =-9x-\frac{5}{2}{x}^{-3}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-9x-\frac{5}{2}{x}^{-3}) \\  & =-9+\frac{15}{2}{x}^{-4} \\  & =-9 + \frac{15}{2 x^{4}}.\end{aligned}
$$

## q-343089 — captured original

Given $f(x)=3{e}^{x}-\frac{1}{3{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

Original field: :answer-field.type/blank

- $3{e}^{x}+\frac{8}{{x}^{5}}$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-\frac{1}{3{x}^{2}}) \\  & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-\frac{1}{3}{x}^{-2}) \\  & =3{e}^{x}+\frac{2}{3}{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}+\frac{2}{3}{x}^{-3}) \\  & =3{e}^{x}-2{x}^{-4}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-2{x}^{-4}) \\  & =3{e}^{x}+8{x}^{-5} \\  & =3{e}^{x}+\frac{8}{{x}^{5}}.\end{aligned}
$$

### served original parameters

Template exponential_reciprocal; profile blank; scales [1, 1]; difficulty :question.difficulty/easy.

Given $f(x)=3{e}^{x}-\frac{1}{3{x}^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $3 {e}^{x} + \frac{8}{x^{5}}$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-\frac{1}{3{x}^{2}}) \\  & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-\frac{1}{3}{x}^{-2}) \\  & =3{e}^{x}+\frac{2}{3}{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}+\frac{2}{3}{x}^{-3}) \\  & =3{e}^{x}-2{x}^{-4}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(3{e}^{x}-2{x}^{-4}) \\  & =3{e}^{x}+8{x}^{-5} \\  & =3{e}^{x}+\frac{8}{{x}^{5}}.\end{aligned}
$$

### generated signed coefficient variant

Template exponential_reciprocal; profile blank; scales [-6, -6]; difficulty :question.difficulty/easy.

Given $f(x)=- 18 {e}^{x} + \frac{2}{x^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $- 6 (3 {e}^{x} + \frac{8}{x^{5}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 18 {e}^{x} + \frac{2}{x^{2}}) \\  & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}+2{x}^{-2}) \\  & =-18 {e}^{x}-4{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}-4{x}^{-3}) \\  & =-18 {e}^{x}+12{x}^{-4}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}+12{x}^{-4}) \\  & =-48{x}^{-5}-18 {e}^{x} \\  & =- 18 {e}^{x} - \frac{48}{x^{5}}.\end{aligned}
$$

### generated signed coefficient variant

Template exponential_reciprocal; profile blank; scales [-6, -5]; difficulty :question.difficulty/easy.

Given $f(x)=- 18 {e}^{x} + \frac{5}{3 x^{2}},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $- 2 (9 {e}^{x} + \frac{20}{x^{5}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 18 {e}^{x} + \frac{5}{3 x^{2}}) \\  & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}+\frac{5}{3}{x}^{-2}) \\  & =-18 {e}^{x}-\frac{10}{3}{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}-\frac{10}{3}{x}^{-3}) \\  & =-18 {e}^{x}+10{x}^{-4}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-18 {e}^{x}+10{x}^{-4}) \\  & =-40{x}^{-5}-18 {e}^{x} \\  & =- 18 {e}^{x} - \frac{40}{x^{5}}.\end{aligned}
$$

## q-343114 — captured original

Given $f(x)=2ln⁡x+{x}^{4},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

Original field: :answer-field.type/blank

- $\frac{4}{{x}^{3}}+24x$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2ln⁡x+{x}^{4}) \\  & =\frac{2}{x}+4{x}^{3} \\  & =2{x}^{-1}+4{x}^{3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(2{x}^{-1}+4{x}^{3}) \\  & =-2{x}^{-2}+12{x}^{2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-2{x}^{-2}+12{x}^{2}) \\  & =4{x}^{-3}+24x \\  & =\frac{4}{{x}^{3}}+24x.\end{aligned}
$$

### served original parameters

Template log_polynomial; profile blank; scales [1, 1]; difficulty :question.difficulty/easy.

Given $f(x)=2lnx+{x}^{4},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $4 (6 x + \frac{1}{x^{3}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2lnx+{x}^{4}) \\  & =\frac{2}{x}+4{x}^{3} \\  & =2{x}^{-1}+4{x}^{3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(2{x}^{-1}+4{x}^{3}) \\  & =-2{x}^{-2}+12{x}^{2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-2{x}^{-2}+12{x}^{2}) \\  & =4{x}^{-3}+24x \\  & =\frac{4}{{x}^{3}}+24x.\end{aligned}
$$

### generated signed coefficient variant

Template log_polynomial; profile blank; scales [-6, -6]; difficulty :question.difficulty/easy.

Given $f(x)=- 6 x^{4} - 12 \ln{(x )},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $- 24 (6 x + \frac{1}{x^{3}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 6 x^{4} - 12 \ln{(x )}) \\  & =- 24 x^{3} - \frac{12}{x} \\  & =-24{x}^{3}-12{x}^{-1}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-24{x}^{3}-12{x}^{-1}) \\  & =-72{x}^{2}+12{x}^{-2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-72{x}^{2}+12{x}^{-2}) \\  & =-144x-24{x}^{-3} \\  & =- 144 x - \frac{24}{x^{3}}.\end{aligned}
$$

### generated signed coefficient variant

Template log_polynomial; profile blank; scales [-6, -5]; difficulty :question.difficulty/easy.

Given $f(x)=- 5 x^{4} - 12 \ln{(x )},$ we have

${f}^{‴}(x)=$ 
{{field-1}}.

- $- 24 (5 x + \frac{1}{x^{3}})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(- 5 x^{4} - 12 \ln{(x )}) \\  & =- 20 x^{3} - \frac{12}{x} \\  & =-20{x}^{3}-12{x}^{-1}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{f}^{″}(x) & =\frac{\text{d}}{\text{d}x}(-20{x}^{3}-12{x}^{-1}) \\  & =-60{x}^{2}+12{x}^{-2}.\end{aligned}
$$

Finally, computing the third derivative, we get

$$
\begin{aligned}{f}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-60{x}^{2}+12{x}^{-2}) \\  & =-120x-24{x}^{-3} \\  & =- 120 x - \frac{24}{x^{3}}.\end{aligned}
$$

## q-343120 — captured original

Find ${g}^{(4)}(x)$ for $g(x)=sin⁡x-{e}^{x}.$

${g}^{(4)}(x)=$ 
{{field-1}}

Original field: :answer-field.type/blank

- $\operatorname{sin}x-{e}^{x}$ **original correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(sin⁡x-{e}^{x}) \\  & =cos⁡x-{e}^{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(cos⁡x-{e}^{x}) \\  & =-sin⁡x-{e}^{x}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-sin⁡x-{e}^{x}) \\  & =-cos⁡x-{e}^{x}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(-cos⁡x-{e}^{x}) \\  & =sin⁡x-{e}^{x}.\end{aligned}
$$

### served original parameters

Template sin_exponential; profile blank; scales [1, 1]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=sinx-{e}^{x}.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $- {e}^{x} + \sin{(x )}$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(sinx-{e}^{x}) \\  & =cosx-{e}^{x}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(cosx-{e}^{x}) \\  & =-sinx-{e}^{x}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(-sinx-{e}^{x}) \\  & =-cosx-{e}^{x}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(-cosx-{e}^{x}) \\  & =sinx-{e}^{x}.\end{aligned}
$$

### generated signed coefficient variant

Template sin_exponential; profile blank; scales [-6, -6]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=6 {e}^{x} - 6 \sin{(x )}.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $6 ({e}^{x} - \sin{(x )})$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(6 {e}^{x} - 6 \sin{(x )}) \\  & =6 {e}^{x} - 6 \cos{(x )}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(6 {e}^{x} - 6 \cos{(x )}) \\  & =6 {e}^{x} + 6 \sin{(x )}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(6 {e}^{x} + 6 \sin{(x )}) \\  & =6 {e}^{x} + 6 \cos{(x )}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(6 {e}^{x} + 6 \cos{(x )}) \\  & =6 {e}^{x} - 6 \sin{(x )}.\end{aligned}
$$

### generated signed coefficient variant

Template sin_exponential; profile blank; scales [-6, -5]; difficulty :question.difficulty/hard.

Find ${g}^{(4)}(x)$ for $g(x)=5 {e}^{x} - 6 \sin{(x )}.$

${g}^{(4)}(x)=$ 
{{field-1}}

- $5 {e}^{x} - 6 \sin{(x )}$ **computed correct**

Computing the first derivative, we get

$$
\begin{aligned}{g}^{′}(x) & =\frac{\text{d}}{\text{d}x}(5 {e}^{x} - 6 \sin{(x )}) \\  & =5 {e}^{x} - 6 \cos{(x )}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}{g}^{″}(x) & =\frac{\text{d}}{\text{d}x}(5 {e}^{x} - 6 \cos{(x )}) \\  & =5 {e}^{x} + 6 \sin{(x )}.\end{aligned}
$$

Computing the third derivative, we get

$$
\begin{aligned}{g}^{‴}(x) & =\frac{\text{d}}{\text{d}x}(5 {e}^{x} + 6 \sin{(x )}) \\  & =5 {e}^{x} + 6 \cos{(x )}.\end{aligned}
$$

Finally, computing the fourth derivative, we get

$$
\begin{aligned}{g}^{(4)}(x) & =\frac{\text{d}}{\text{d}x}(5 {e}^{x} + 6 \cos{(x )}) \\  & =5 {e}^{x} - 6 \sin{(x )}.\end{aligned}
$$
