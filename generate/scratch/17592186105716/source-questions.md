# Original source questions — basis 2275

## q-29836

Find the integral of $\frac{3}{5x} + 3x$ with respect to $x$.

Difficulty: unrated

Field: selection :answer-field.type/radio

- $\ln x + \frac{7x^{2}}{2} + C$

- $\frac{3}{5}\ln \mid x \mid + \frac{3x^{2}}{2} + C$

- $\frac{7}{5}\ln \mid x \mid + \frac{5x^{2}}{2} + C$

- $\frac{5}{3}\ln \mid x \mid + \frac{x^{2}}{2} + C$

- $\frac{3}{5}\ln x + \frac{5x^{2}}{2} + C$

Correct: None

Source worked solution absent.

## q-29857

Find the integral of $\frac{2}{x} - \frac{1}{\sqrt{x}}$ with respect to $x$.

Difficulty: unrated

Field: selection :answer-field.type/radio

- $2\ln \mid x \mid - \frac{2}{x} + C$

- $\ln \mid x \mid - x^{1/2} + C$

- $x - 2x^{1/2} + C$

- $2\ln \mid x \mid - 2x^{1/2} + C$

- $\ln \mid x \mid + 2x^{1/2} + C$

Correct: None

Source worked solution absent.

## q-103374

Calculate $\int \frac{3{x}^{2}-6}{2x}\,dx.$

Difficulty: {':db/ident': ':question.difficulty/easy'}

Field: selection :answer-field.type/radio

- $3{x}^{2}+ln⁡|3x|+C$

- $\frac{3}{2}{x}^{2}-ln⁡|3x|+C$

- $\frac{3}{4}{x}^{2}-3ln⁡|x|+C$

- $\frac{3}{4}{x}^{2}-ln⁡|3x|+C$

- $\frac{3}{2}{x}^{2}+3ln⁡|x|+C$

Correct: {':answer/id': 'a77100c8-1980-51d5-9cdf-fe3f251c5336', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{3}{4}{x}^{2}-3ln\u2061|x|+C', ':db/id': 17592186236865}

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int \frac{3{x}^{2}-6}{2x}\,\text{d}x & =\int (\frac{3{x}^{2}}{2x}-\frac{3}{x})\text{d}x \\  & =\int (\frac{3}{2}x-\frac{3}{x})\text{d}x \\  & =\frac{3}{2}\int x\,\text{d}x-3\int \frac{1}{x}\,\text{d}x \\  & =\frac{3}{4}{x}^{2}-3ln⁡|x|+C.\end{aligned}
$$

## q-103593

Calculate $\int ({x}^{3/2}+\frac{1}{2}{x}^{-1})\,\text{d}x.$

Difficulty: {':db/ident': ':question.difficulty/easy'}

Field: selection :answer-field.type/radio

- $\frac{5}{2}{x}^{3/2}+\frac{1}{2}\operatorname{ln}⁡|x|+C$

- $\frac{5}{2}{x}^{5/2}+2\operatorname{ln}⁡|x|+C$

- $\frac{2}{5}{x}^{5/2}+\frac{1}{2}\operatorname{ln}⁡|x|+C$

- $\frac{3}{2}{x}^{3/2}+2\operatorname{ln}⁡|x|+C$

- $\frac{3}{2}{x}^{5/2}+2\operatorname{ln}⁡|x|+C$

Correct: {':answer/id': 'b7b12b3f-b8dd-53cd-a79b-4f8d64e6c135', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{2}{5}{x}^{5/2}+\\frac{1}{2}\\operatorname{ln}\u2061|x|+C', ':db/id': 17592186236984}

First, we apply the sum rule and get

$$
\int ({x}^{3/2}+\frac{1}{2}{x}^{-1})\,\text{d}x=\int {x}^{3/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{3/2}\,\text{d}x+\frac{1}{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{3/2+1}}{\frac{3}{2}+1}+\frac{1}{2}\operatorname{ln}⁡|x|+C \\  & =\frac{2}{5}{x}^{5/2}+\frac{1}{2}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

## q-29885

Calculate $\int ({x}^{2/3}+\frac{\sqrt{2}}{x})\,\text{d}x.$

Difficulty: {':db/ident': ':question.difficulty/easy'}

Field: selection :answer-field.type/radio

- $\frac{11}{5}{x}^{11/3}+\sqrt{5}\operatorname{ln}⁡|x|+C$

- $\frac{7}{5}{x}^{4/3}+2\operatorname{ln}⁡|x|+C$

- $\frac{3\operatorname{ln}⁡x}{5}{x}^{5/3}+\operatorname{ln}⁡|x|+C$

- $\frac{9}{5}{x}^{7/3}+\sqrt{3}\operatorname{ln}⁡|x|+C$

- $\frac{3}{5}{x}^{5/3}+\sqrt{2}\operatorname{ln}⁡|x|+C$

Correct: {':answer/id': 'd6b38dca-ffa5-5659-aa91-113d55a9cced', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{3}{5}{x}^{5/3}+\\sqrt{2}\\operatorname{ln}\u2061|x|+C', ':db/id': 17592186296395}

First, we apply the sum rule and get

$$
\int ({x}^{2/3}+\frac{\sqrt{2}}{x})\,\text{d}x=\int {x}^{2/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x
$$

Now, using the power rule in the first term, and taking out the coefficient in the second term, we get

$$
\begin{aligned}\int {x}^{2/3}\,\text{d}x+\sqrt{2}\int \frac{1}{x}\,\text{d}x & =\frac{{x}^{2/3+1}}{\frac{2}{3}+1}+\sqrt{2}\operatorname{ln}⁡|x|+C \\  & =\frac{3}{5}{x}^{5/3}+\sqrt{2}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

## q-29886

Find the integral of $2{x}^{7/3}-\frac{1}{3x}$ with respect to $x.$

Difficulty: {':db/ident': ':question.difficulty/easy'}

Field: selection :answer-field.type/radio

- $\frac{3}{5}{x}^{10/3}-\frac{1}{3}ln⁡|x|+C$

- $\frac{5}{2}{x}^{7/3}-3ln⁡|x|+C$

- $\frac{7}{2}{x}^{2/3}-ln⁡|x|+C$

- $\frac{1}{5}{x}^{1/3}-\frac{1}{3}ln⁡|x|+C$

- $\frac{7}{5}{x}^{7/3}-3ln⁡|x|+C$

Correct: {':answer/id': '00628492-eb93-5878-979e-30036d304edf', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{3}{5}{x}^{10/3}-\\frac{1}{3}ln\u2061|x|+C', ':db/id': 17592186295270}

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (2{x}^{7/3}-\frac{1}{3x})\text{d}x & =\int 2{x}^{7/3}\,\text{d}x-\frac{1}{3}\int \frac{1}{x}\,\text{d}x \\  & =2\cdot \frac{{x}^{7/3+1}}{(\frac{7}{3}+1)}-\frac{1}{3}ln⁡|x|+C \\  & =\frac{3}{5}{x}^{10/3}-\frac{1}{3}ln⁡|x|+C.\end{aligned}
$$

## q-29888

Find the integral of $\frac{3}{{x}^{-1}}+3{x}^{-1}$ with respect to $x.$

Difficulty: {':db/ident': ':question.difficulty/easy'}

Field: selection :answer-field.type/radio

- $\frac{3}{2}{x}^{2}+3ln⁡|x|+C$

- $\frac{4}{3}{x}^{2}+5ln⁡|x|+C$

- $\frac{1}{2}{x}^{2}+3ln⁡|x|+C$

- $\frac{2}{3}{x}^{2}+2ln⁡|x|+C$

- $\frac{5}{2}{x}^{2}+4ln⁡|x|+C$

Correct: {':answer/id': '176c0cc3-ba47-5a28-bd33-bd9278429e85', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{3}{2}{x}^{2}+3ln\u2061|x|+C', ':db/id': 17592186295407}

Applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{3}{{x}^{-1}}+3{x}^{-1})\text{d}x & =3\int x\,\text{d}x+3\int \frac{1}{x}\,\text{d}x \\  & =\frac{3}{2}{x}^{2}+3ln⁡|x|+C.\end{aligned}
$$

## q-29915

Find the integral of $\frac{\sqrt{{x}^{3}}}{\sqrt{{x}^{5}}}-5{x}^{-1}$ with respect to $x.$

Difficulty: {':db/ident': ':question.difficulty/hard'}

Field: selection :answer-field.type/radio

- $-5ln⁡|x|+C$

- $-4ln⁡|x|+C$

- $4ln⁡|x|+C$

- $-6x+C$

- $5x+C$

Correct: {':answer/id': '14c3a82a-71bb-5b22-a1d7-5d3ffaa433a8', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-4ln\u2061|x|+C', ':db/id': 17592186295384}

Simplifying the exponents and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int (\frac{\sqrt{{x}^{3}}}{\sqrt{{x}^{5}}}-5{x}^{-1})\text{d}x & =\int \frac{1}{{x}^{5/2-3/2}}\,\text{d}x-5\int \frac{1}{x}\,\text{d}x \\  & =\int \frac{1}{x}\,\text{d}x-5\int \frac{1}{x}\,\text{d}x \\  & =-4\int \frac{1}{x}\,\text{d}x \\  & =-4ln⁡|x|+C.\end{aligned}
$$

## q-49100

Find the integral of ${(2-\frac{1}{x})}^{2}$ with respect to $x.$

Difficulty: {':db/ident': ':question.difficulty/moderate'}

Field: selection :answer-field.type/radio

- $2xln⁡|x|+C$

- $ln⁡|2-\frac{1}{x}|+C$

- $2x-ln⁡|x|+C$

- $4x-4ln⁡|x|-\frac{1}{x}+C$

- ${(2x-ln⁡|x|)}^{2}+C$

Correct: {':answer/id': 'ebfcaae4-3cd8-5b37-ad78-afba74998213', ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4x-4ln\u2061|x|-\\frac{1}{x}+C', ':db/id': 17592186332021}

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(2-\frac{1}{x})}^{2}\text{d}x & =\int (4-\frac{4}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int 4\,\text{d}x-\int \frac{4}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =4\int \text{d}x-4\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =4x-4ln⁡|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =4x-4ln⁡|x|-\frac{1}{x}+C.\end{aligned}
$$
